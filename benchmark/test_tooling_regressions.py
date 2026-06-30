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


if __name__ == "__main__":
    unittest.main()
