#!/usr/bin/env python3
"""Regression tests for loop-harness deterministic tooling."""

from __future__ import annotations

import plistlib
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd or ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


class ToolingRegressionTests(unittest.TestCase):
    def scaffold(self, tmp: Path) -> Path:
        completed = run(["python3", "scripts/init_loop.py", str(tmp)])
        self.assertEqual(completed.returncode, 0, completed.stdout)
        return tmp / ".loop-harness"

    def test_controller_does_not_pass_negated_pass_text(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            self.scaffold(tmp)
            completed = run(
                [
                    "python3",
                    "scripts/run_loop_controller.py",
                    "--repo",
                    str(tmp),
                    "--command",
                    'printf "not PASS\\n"',
                    "--plateau-patience",
                    "1",
                ]
            )
            self.assertEqual(completed.returncode, 3, completed.stdout)
            self.assertIn("STOP PLATEAU", completed.stdout)

    def test_controller_requires_verdict_at_line_start(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            self.scaffold(tmp)
            completed = run(
                [
                    "python3",
                    "scripts/run_loop_controller.py",
                    "--repo",
                    str(tmp),
                    "--command",
                    'printf "not verdict=PASS\\n"',
                    "--plateau-patience",
                    "1",
                ]
            )
            self.assertEqual(completed.returncode, 3, completed.stdout)

    def test_controller_promotes_terminal_failure_to_benchmark(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            artifact_root = self.scaffold(tmp)
            completed = run(
                [
                    "python3",
                    "scripts/run_loop_controller.py",
                    "--repo",
                    str(tmp),
                    "--command",
                    'printf "SCORE=1\\n"; exit 1',
                    "--target-score",
                    "8",
                    "--plateau-patience",
                    "1",
                ]
            )
            self.assertEqual(completed.returncode, 3, completed.stdout)
            benchmark = (artifact_root / "PRODUCT_LOOP_BENCHMARK.md").read_text(encoding="utf-8")
            self.assertIn("## Regression Case: controller-", benchmark)
            self.assertIn("- Status: active", benchmark)
            validated = run(["python3", "scripts/validate_run_log_entry.py", str(artifact_root / "product-loop-run-log.md")])
            self.assertEqual(validated.returncode, 0, validated.stdout)

    def test_audit_allows_progress_partial_entries_without_promotion(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            self.scaffold(tmp)
            command = (
                "python3 -c '"
                "import os, sys; "
                "i=int(os.environ.get(\"LOOP_ITERATION\", \"1\")); "
                "score=6+i; "
                "print(f\"metric={score}\"); "
                "print(\"PASS\" if i >= 2 else \"PARTIAL\"); "
                "sys.exit(0 if i >= 2 else 1)'"
            )
            completed = run(
                [
                    "python3",
                    "scripts/run_loop_controller.py",
                    "--repo",
                    raw,
                    "--command",
                    command,
                    "--target-score",
                    "8",
                ]
            )
            self.assertEqual(completed.returncode, 0, completed.stdout)
            audited = run(["python3", "scripts/product_loop_audit.py", raw, "--min-level", "L2"])
            self.assertEqual(audited.returncode, 0, audited.stdout)
            self.assertIn("OK no failed iterations require active regression cases yet", audited.stdout)

    def test_pressure_eval_fails_when_agent_command_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            completed = run(
                [
                    "python3",
                    "benchmark/run_pressure_eval.py",
                    "--case",
                    "ui_requires_playwright",
                    "--agent-command",
                    'cat benchmark/fixtures/pass/ui_requires_playwright.md; exit 42',
                    "--generated-transcripts",
                    raw,
                ]
            )
            self.assertNotEqual(completed.returncode, 0, completed.stdout)
            self.assertIn("agent command failed", completed.stdout.lower())

    def test_pressure_eval_blocks_plural_separate_iterations(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            transcript = Path(raw) / "multi_lane_single_iteration_plan.md"
            transcript.write_text(
                "\n".join(
                    [
                        "run-until-done",
                        "Batch type: multi-lane",
                        "execution batch",
                        "Lane decomposition",
                        "Lane id: lane-docs-copy",
                        "Lane id: lane-unit-test",
                        "Lane id: lane-playwright-smoke",
                        "Allowed files/surfaces",
                        "Dependencies",
                        "Verification command",
                        "Owner",
                        "Parallelization strategy",
                        "Independence rationale",
                        "Integrated verification",
                        "Next iteration only if integrated batch verification fails.",
                        "I will treat each known independent lane as separate iterations.",
                    ]
                ),
                encoding="utf-8",
            )
            completed = run(
                [
                    "python3",
                    "benchmark/run_pressure_eval.py",
                    "--case",
                    "multi_lane_single_iteration_plan",
                    "--transcripts",
                    raw,
                ]
            )
            self.assertNotEqual(completed.returncode, 0, completed.stdout)
            self.assertIn("Forbidden hits", completed.stdout)

    def test_pressure_eval_rejects_unjustified_sequential_batch_for_independent_lanes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            transcript = Path(raw) / "multi_lane_single_iteration_plan.md"
            transcript.write_text(
                "\n".join(
                    [
                        "run-until-done",
                        "Batch type: sequential",
                        "execution batch",
                        "Lane decomposition",
                        "Lane id: lane-docs-copy",
                        "Lane id: lane-unit-test",
                        "Lane id: lane-playwright-smoke",
                        "Allowed files/surfaces",
                        "Dependencies",
                        "Verification command",
                        "Owner",
                        "Parallelization strategy",
                        "Independence rationale",
                        "Integrated verification",
                        "Next iteration starts if integrated batch verification fails.",
                    ]
                ),
                encoding="utf-8",
            )
            completed = run(
                [
                    "python3",
                    "benchmark/run_pressure_eval.py",
                    "--case",
                    "multi_lane_single_iteration_plan",
                    "--transcripts",
                    raw,
                ]
            )
            self.assertNotEqual(completed.returncode, 0, completed.stdout)
            self.assertIn("Missing", completed.stdout)

    def test_launchd_scheduler_writes_valid_plist_with_shell_operators(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            completed = run(
                [
                    "python3",
                    "scripts/install_scheduler.py",
                    "--repo",
                    raw,
                    "--kind",
                    "launchd",
                    "--cadence",
                    "hourly",
                    "--command",
                    "echo a && echo b",
                    "--label",
                    "x",
                ]
            )
            self.assertEqual(completed.returncode, 0, completed.stdout)
            plist_path = Path(completed.stdout.strip())
            with plist_path.open("rb") as handle:
                data = plistlib.load(handle)
            self.assertEqual(data["ProgramArguments"], ["/bin/zsh", "-lc", "echo a && echo b"])

    def test_cron_daily_uses_valid_daily_expression(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            completed = run(
                [
                    "python3",
                    "scripts/install_scheduler.py",
                    "--repo",
                    raw,
                    "--kind",
                    "cron",
                    "--cadence",
                    "daily",
                    "--command",
                    "echo ok",
                    "--label",
                    "x",
                ]
            )
            self.assertEqual(completed.returncode, 0, completed.stdout)
            cron = Path(completed.stdout.strip()).read_text(encoding="utf-8")
            self.assertTrue(cron.startswith("0 0 * * * "), cron)

    def test_include_skill_does_not_select_unmatched_critical_cases(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            self.scaffold(Path(raw))
            completed = run(
                [
                    "python3",
                    "scripts/select_benchmarks.py",
                    "--repo",
                    raw,
                    "--profile",
                    "nonexistent",
                    "--intent",
                    "none",
                    "--surface",
                    "none",
                    "--include-skill",
                    "--require",
                ]
            )
            self.assertNotEqual(completed.returncode, 0, completed.stdout)
            self.assertIn("Selected 0 benchmark case", completed.stdout)

    def test_l2_audit_fails_without_batch_planning_fields(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            artifact_root = self.scaffold(Path(raw))
            for name in ["PRODUCT_LOOP.md", "PRODUCT_LOOP_STATE.md", "AGENT_HANDOFF.md"]:
                path = artifact_root / name
                filtered = [
                    line
                    for line in path.read_text(encoding="utf-8").splitlines()
                    if not any(
                        marker in line.lower()
                        for marker in [
                            "batch planning",
                            "batch type",
                            "lane decomposition",
                            "lane ids",
                            "lane dependencies",
                            "parallelization rationale",
                            "parallelization strategy",
                            "deferred lane rationale",
                        ]
                    )
                ]
                path.write_text("\n".join(filtered) + "\n", encoding="utf-8")
            completed = run(["python3", "scripts/product_loop_audit.py", raw, "--min-level", "L2"])
            self.assertNotEqual(completed.returncode, 0, completed.stdout)
            self.assertIn("batch planning", completed.stdout.lower())


if __name__ == "__main__":
    unittest.main()
