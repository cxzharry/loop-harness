#!/usr/bin/env python3
"""Regression tests for loop-harness deterministic tooling."""

from __future__ import annotations

import plistlib
import json
import re
import shutil
import subprocess
import tempfile
import time
import unittest
import urllib.request
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


def watchdog(args: list[str]) -> subprocess.CompletedProcess[str]:
    return run(["python3", "scripts/watchdog.py", *args])


class ToolingRegressionTests(unittest.TestCase):
    def scaffold(self, tmp: Path) -> Path:
        completed = run(["python3", "scripts/init_loop.py", str(tmp)])
        self.assertEqual(completed.returncode, 0, completed.stdout)
        return tmp / ".loop-harness"

    def write_review_candidates(self, tmp: Path) -> Path:
        candidates = {
            "surface": "onboarding flow",
            "intent": "UX_OPTIMIZE",
            "profiles": ["ux-product"],
            "metrics": [
                {
                    "id": "activation_completion",
                    "title": "Activation completion rate",
                    "description": "Use when success depends on users completing the target flow.",
                    "recommended": True,
                },
                {
                    "id": "visual_clarity",
                    "title": "Visual clarity score",
                    "description": "Use when hierarchy, readability, and trust are the main target.",
                    "recommended": False,
                },
            ],
            "criteria": [
                {
                    "id": "ux_acceptance",
                    "title": "UX acceptance criteria",
                    "description": "Checks task clarity, text fit, control affordance, and mobile behavior.",
                    "recommended": True,
                }
            ],
            "benchmark": [
                {
                    "id": "playwright_critical_flow",
                    "title": "Playwright critical-flow smoke",
                    "description": "Runs the target route and flow with real browser assertions.",
                    "recommended": True,
                }
            ],
        }
        path = tmp / "review-candidates.json"
        path.write_text(json.dumps(candidates), encoding="utf-8")
        return path

    def test_public_release_hygiene_has_docs_and_no_local_paths(self) -> None:
        self.assertTrue((ROOT / "README.md").is_file())
        self.assertTrue((ROOT / "LICENSE").is_file())
        self.assertIn("MIT License", (ROOT / "LICENSE").read_text(encoding="utf-8"))

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("$loop-harness", readme)
        self.assertIn("<your-skills-dir>/loop-harness", readme)
        self.assertIn("agent skill", readme.lower())
        self.assertIn("metrics", readme.lower())
        self.assertIn("criteria", readme.lower())
        self.assertIn("benchmark", readme.lower())
        self.assertIn("first run", readme.lower())
        self.assertIn("later runs", readme.lower())
        self.assertIn("does not automatically install operating-system scheduler jobs", readme)
        self.assertNotIn("Codex", readme)
        self.assertNotIn("Claude", readme)
        self.assertNotIn("~/.codex", readme)
        self.assertNotIn("## Watchdog", readme)
        self.assertNotIn("## Validation", readme)
        self.assertNotIn("scripts/watchdog.py setup", readme)
        self.assertNotIn("validate_run_log_entry.py", readme)

        self.assertIn("self/loop-runs/", (ROOT / ".gitignore").read_text(encoding="utf-8"))
        if (ROOT / ".git").exists():
            tracked_self_runs = run(["git", "ls-files", "self/loop-runs"])
            self.assertEqual(tracked_self_runs.returncode, 0, tracked_self_runs.stdout)
            self.assertEqual(tracked_self_runs.stdout.strip(), "")
        else:
            self.assertFalse((ROOT / "self" / "loop-runs").exists())

        text_file_suffixes = {".md", ".py", ".json", ".yaml", ".yml", ".toml", ".txt"}
        text_file_names = {".gitignore", "LICENSE"}
        forbidden = [
            re.compile("/" + "Users/" + r"[^\s`'\"]+"),
            re.compile(r"\b" + "hai" + "do" + r"\b", re.IGNORECASE),
            re.compile("gh" + "o_" + r"[A-Za-z0-9_]+"),
            re.compile("github" + "_pat_" + r"[A-Za-z0-9_]+"),
            re.compile(r"sk-[A-Za-z0-9]{20,}"),
            re.compile(r"api[_-]?key\s*=", re.IGNORECASE),
            re.compile(r"password\s*=", re.IGNORECASE),
            re.compile(r"token\s*=", re.IGNORECASE),
        ]
        forbidden_samples = [
            (forbidden[0], "/" + "Users/example/path"),
            (forbidden[1], "hai" + "do"),
            (forbidden[2], "gh" + "o_" + "sampletoken"),
            (forbidden[3], "github" + "_pat_" + "sampletoken"),
            (forbidden[5], "api" + "_key = value"),
            (forbidden[5], "api" + "-key=value"),
            (forbidden[6], "pass" + "word = value"),
            (forbidden[7], "tok" + "en = value"),
        ]
        for pattern, sample in forbidden_samples:
            self.assertIsNotNone(pattern.search(sample), f"{pattern.pattern} did not match sample")

        for path in ROOT.rglob("*"):
            if path.is_dir():
                continue
            if any(part in {".git", ".worktrees", "__pycache__"} for part in path.parts):
                continue
            if path.suffix.lower() not in text_file_suffixes and path.name not in text_file_names:
                continue
            text = path.read_text(encoding="utf-8")
            for pattern in forbidden:
                self.assertIsNone(pattern.search(text), f"{pattern.pattern} matched {path.relative_to(ROOT)}")

    def test_review_contract_renders_lean_human_selection_ui(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            artifact_root = self.scaffold(tmp)
            candidates = self.write_review_candidates(tmp)
            rendered = run(
                [
                    "python3",
                    "scripts/review_contract.py",
                    "render",
                    "--repo",
                    raw,
                    "--candidates",
                    str(candidates),
                ]
            )
            self.assertEqual(rendered.returncode, 0, rendered.stdout)
            review_html = artifact_root / "review" / "evaluation-contract.html"
            self.assertTrue(review_html.is_file(), rendered.stdout)
            html = review_html.read_text(encoding="utf-8")
            self.assertIn("Metrics", html)
            self.assertIn("Criteria", html)
            self.assertIn("Benchmark", html)
            self.assertNotIn("Rubric", html)
            self.assertIn("Activation completion rate (Recommended)", html)
            self.assertIn("data-group=\"metrics\"", html)
            self.assertIn("data-group=\"criteria\"", html)
            self.assertIn("data-group=\"benchmark\"", html)
            self.assertIn("<button class=\"no", html)
            self.assertLess(html.index("<button class=\"no"), html.index("<button class=\"yes"))
            self.assertIn("data-recommended=\"true\" data-choice=\"yes\"", html)
            self.assertIn("data-recommended=\"false\" data-choice=\"no\"", html)

    def test_review_contract_server_saves_selection_and_confirm_locks_criteria(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            artifact_root = self.scaffold(tmp)
            candidates = self.write_review_candidates(tmp)
            process = subprocess.Popen(
                [
                    "python3",
                    "scripts/review_contract.py",
                    "serve",
                    "--repo",
                    raw,
                    "--candidates",
                    str(candidates),
                    "--host",
                    "127.0.0.1",
                    "--port",
                    "0",
                    "--once",
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            try:
                assert process.stdout is not None
                server_info = json.loads(process.stdout.readline())
                selection = {
                    "items": [
                        {"group": "metrics", "id": "activation_completion", "accepted": True},
                        {"group": "metrics", "id": "visual_clarity", "accepted": False},
                        {"group": "criteria", "id": "ux_acceptance", "accepted": True},
                        {"group": "benchmark", "id": "playwright_critical_flow", "accepted": True},
                    ]
                }
                request = urllib.request.Request(
                    f"{server_info['url']}/selection",
                    data=json.dumps(selection).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(request, timeout=5) as response:
                    saved = json.loads(response.read().decode("utf-8"))
                self.assertTrue(saved["ok"])
                for _attempt in range(30):
                    if process.poll() is not None:
                        break
                    time.sleep(0.05)
                self.assertEqual(process.wait(timeout=5), 0)
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait(timeout=5)
                if process.stdout is not None:
                    process.stdout.close()

            selection_path = artifact_root / "review" / "evaluation-contract-selection.json"
            self.assertTrue(selection_path.is_file())
            selected = json.loads(selection_path.read_text(encoding="utf-8"))
            accepted_ids = {item["id"] for item in selected["items"] if item["accepted"]}
            self.assertEqual(
                accepted_ids,
                {"activation_completion", "ux_acceptance", "playwright_critical_flow"},
            )

            confirmed = run(["python3", "scripts/review_contract.py", "confirm", "--repo", raw, "--yes"])
            self.assertEqual(confirmed.returncode, 0, confirmed.stdout)
            criteria = (artifact_root / "criteria" / "current.md").read_text(encoding="utf-8")
            self.assertIn("Contract status: locked", criteria)
            self.assertIn("Activation completion rate", criteria)
            self.assertIn("UX acceptance criteria", criteria)
            self.assertIn("playwright_critical_flow", criteria)
            self.assertIn("CLI confirmed: yes", criteria)

    def test_skill_requires_brainstormed_html_selection_before_actioning(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        operation = (ROOT / "references" / "operation.md").read_text(encoding="utf-8")
        template = (ROOT / "assets" / "templates" / "criteria" / "current.md").read_text(encoding="utf-8")
        combined = "\n".join([skill, operation, template])
        self.assertIn("human-confirmed evaluation contract", combined)
        self.assertIn("review_contract.py", combined)
        self.assertIn("Metrics", combined)
        self.assertIn("Criteria", combined)
        self.assertIn("Benchmark", combined)
        self.assertIn("CLI confirmed: yes", combined)
        self.assertNotIn("Do not ask when a safe default exists", operation)

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
            active_cases = list((artifact_root / "benchmarks" / "active").glob("controller-*.md"))
            self.assertEqual(len(active_cases), 1, benchmark)
            split_case = active_cases[0].read_text(encoding="utf-8")
            self.assertIn("## Regression Case: controller-", split_case)
            self.assertIn("- Status: active", split_case)
            self.assertIn(f"benchmarks/active/{active_cases[0].name}", benchmark)
            self.assertNotIn("## Regression Case: controller-", benchmark)
            self.assertIn("- Status: active", benchmark)
            validated = run(["python3", "scripts/validate_run_log_entry.py", str(artifact_root / "product-loop-run-log.md")])
            self.assertEqual(validated.returncode, 0, validated.stdout)

    def test_audit_counts_split_active_regression_cases(self) -> None:
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
                    'printf "SCORE=1\\n"; exit 1',
                    "--target-score",
                    "8",
                    "--plateau-patience",
                    "1",
                ]
            )
            self.assertEqual(completed.returncode, 3, completed.stdout)
            audited = run(["python3", "scripts/product_loop_audit.py", raw, "--min-level", "L2"])
            self.assertEqual(audited.returncode, 0, audited.stdout)
            self.assertIn("OK active promoted regression cases: 1", audited.stdout)

    def test_audit_ignores_archived_regression_cases(self) -> None:
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
            active_cases = list((artifact_root / "benchmarks" / "active").glob("controller-*.md"))
            self.assertEqual(len(active_cases), 1)
            shutil.move(str(active_cases[0]), artifact_root / "benchmarks" / "archive" / active_cases[0].name)

            audited = run(["python3", "scripts/product_loop_audit.py", raw, "--min-level", "L2"])
            self.assertNotEqual(audited.returncode, 0, audited.stdout)
            self.assertIn("no active promoted regression case", audited.stdout)

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

    def test_watchdog_setup_writes_config_and_launchd_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            artifact_root = self.scaffold(Path(raw))
            completed = watchdog(
                [
                    "setup",
                    "--repo",
                    raw,
                    "--kind",
                    "launchd",
                    "--cadence",
                    "hourly",
                    "--label",
                    "loop.watchdog.test",
                    "--command",
                    "printf PASS",
                ]
            )
            self.assertEqual(completed.returncode, 0, completed.stdout)

            config_path = artifact_root / "watchdog" / "config.json"
            self.assertTrue(config_path.is_file(), completed.stdout)
            config = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertEqual(config["kind"], "launchd")
            self.assertEqual(config["cadence"], "hourly")
            self.assertEqual(config["label"], "loop.watchdog.test")
            self.assertEqual(config["command"], "printf PASS")

            plists = list((artifact_root / "schedules").glob("*.plist"))
            self.assertEqual(len(plists), 1, completed.stdout)
            with plists[0].open("rb") as handle:
                plist = plistlib.load(handle)
            self.assertEqual(plist["Label"], "loop.watchdog.test")
            self.assertIn("scripts/watchdog.py", " ".join(plist["ProgramArguments"]))
            self.assertIn("tick", plist["ProgramArguments"])

    def test_watchdog_tick_skips_when_paused(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            artifact_root = self.scaffold(Path(raw))
            setup = watchdog(["setup", "--repo", raw, "--command", "printf SHOULD_NOT_RUN"])
            self.assertEqual(setup.returncode, 0, setup.stdout)
            paused = watchdog(["pause", "--repo", raw])
            self.assertEqual(paused.returncode, 0, paused.stdout)

            completed = watchdog(["tick", "--repo", raw])
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertIn("paused", completed.stdout.lower())
            self.assertFalse((artifact_root / "watchdog" / "run.lock").exists())
            latest_status = artifact_root / "watchdog" / "status.json"
            self.assertTrue(latest_status.is_file(), completed.stdout)
            status = json.loads(latest_status.read_text(encoding="utf-8"))
            self.assertEqual(status["decision"], "skipped_paused")

    def test_watchdog_tick_refuses_run_until_done_without_locked_criteria(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            artifact_root = self.scaffold(Path(raw))
            criteria = artifact_root / "criteria" / "current.md"
            self.assertIn("Contract status: draft | locked", criteria.read_text(encoding="utf-8"))
            setup = watchdog(["setup", "--repo", raw, "--command", "printf PASS"])
            self.assertEqual(setup.returncode, 0, setup.stdout)

            completed = watchdog(["tick", "--repo", raw, "--run-until-done"])
            self.assertNotEqual(completed.returncode, 0, completed.stdout)
            self.assertIn("criteria/current.md", completed.stdout)
            self.assertIn("locked", completed.stdout.lower())
            status = json.loads((artifact_root / "watchdog" / "status.json").read_text(encoding="utf-8"))
            self.assertEqual(status["decision"], "blocked_unlocked_criteria")

    def test_watchdog_tick_skips_overlap_lock(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            artifact_root = self.scaffold(Path(raw))
            setup = watchdog(["setup", "--repo", raw, "--command", "printf SHOULD_NOT_RUN"])
            self.assertEqual(setup.returncode, 0, setup.stdout)
            lock_path = artifact_root / "watchdog" / "run.lock"
            lock_path.parent.mkdir(parents=True, exist_ok=True)
            lock_path.write_text("existing run\n", encoding="utf-8")

            completed = watchdog(["tick", "--repo", raw])
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertIn("overlap", completed.stdout.lower())
            self.assertEqual(lock_path.read_text(encoding="utf-8"), "existing run\n")
            status = json.loads((artifact_root / "watchdog" / "status.json").read_text(encoding="utf-8"))
            self.assertEqual(status["decision"], "skipped_overlap")

    def test_watchdog_status_reads_latest_status_json(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            artifact_root = self.scaffold(Path(raw))
            status_path = artifact_root / "watchdog" / "status.json"
            status_path.parent.mkdir(parents=True, exist_ok=True)
            status_path.write_text(
                '{"decision": "skipped_paused", "last_tick": "2026-07-09T00:00:00Z", "detail": "paused by user"}\n',
                encoding="utf-8",
            )

            completed = watchdog(["status", "--repo", raw])
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertIn("skipped_paused", completed.stdout)
            self.assertIn("2026-07-09T00:00:00Z", completed.stdout)
            self.assertIn("paused by user", completed.stdout)

    def test_watchdog_uninstall_removes_generated_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            artifact_root = self.scaffold(Path(raw))
            setup = watchdog(
                [
                    "setup",
                    "--repo",
                    raw,
                    "--kind",
                    "launchd",
                    "--cadence",
                    "daily",
                    "--label",
                    "loop.watchdog.uninstall",
                    "--command",
                    "printf PASS",
                ]
            )
            self.assertEqual(setup.returncode, 0, setup.stdout)
            self.assertTrue((artifact_root / "watchdog" / "config.json").exists())
            self.assertTrue(list((artifact_root / "schedules").glob("*.plist")))

            completed = watchdog(["uninstall", "--repo", raw])
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertFalse((artifact_root / "watchdog" / "config.json").exists())
            self.assertFalse(list((artifact_root / "schedules").glob("*.plist")))

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

    def test_scaffold_creates_runtime_criteria_and_archive_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            artifact_root = self.scaffold(Path(raw))

            self.assertTrue((artifact_root / "criteria" / "current.md").is_file())
            self.assertTrue((artifact_root / "benchmarks" / "active").is_dir())
            self.assertTrue((artifact_root / "benchmarks" / "archive").is_dir())
            self.assertTrue((artifact_root / "runs").is_dir())
            self.assertTrue((artifact_root / "runs" / "archive").is_dir())

            criteria = (artifact_root / "criteria" / "current.md").read_text(encoding="utf-8")
            self.assertIn("Evaluation Contract", criteria)
            self.assertIn("Contract status: draft | locked", criteria)
            self.assertIn("Primary metric", criteria)
            self.assertIn("Acceptance Criteria", criteria)
            self.assertIn("Benchmark seeds", criteria)

    def test_select_benchmarks_reads_split_active_case_files(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            artifact_root = self.scaffold(Path(raw))
            split_case = artifact_root / "benchmarks" / "active" / "checkout-visible-flow.md"
            split_case.write_text(
                "\n".join(
                    [
                        "## Regression Case: checkout-visible-flow",
                        "",
                        "- Source run-log entry: 2026-07-09T00:00:00Z",
                        "- Error class: ui_regression",
                        "- Surface/URL: checkout web-route",
                        "- Trigger condition: checkout submit button regresses",
                        "- Playwright steps: open checkout and submit",
                        "- Expected result: checkout completes",
                        "- Failure evidence: submit button was hidden",
                        "- Matching rule: checkout web-route ux-product activation",
                        "- Owner profile: ux-product",
                        "- Last failed: 2026-07-09T00:00:00Z",
                        "- Last passed: 2026-07-09T00:00:00Z",
                        "- Status: active",
                    ]
                ),
                encoding="utf-8",
            )

            completed = run(
                [
                    "python3",
                    "scripts/select_benchmarks.py",
                    "--repo",
                    raw,
                    "--profile",
                    "ux-product",
                    "--intent",
                    "UX_OPTIMIZE",
                    "--surface",
                    "checkout web-route",
                    "--metric",
                    "activation",
                    "--require",
                ]
            )
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertIn("checkout-visible-flow", completed.stdout)
            self.assertIn("benchmarks/active/checkout-visible-flow.md", completed.stdout)

    def test_select_benchmarks_ignores_archive_case_files(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            artifact_root = self.scaffold(Path(raw))
            archived_case = artifact_root / "benchmarks" / "archive" / "checkout-visible-flow.md"
            archived_case.write_text(
                "\n".join(
                    [
                        "## Regression Case: checkout-visible-flow",
                        "",
                        "- Source run-log entry: 2026-07-09T00:00:00Z",
                        "- Error class: ui_regression",
                        "- Surface/URL: checkout web-route",
                        "- Trigger condition: checkout submit button regresses",
                        "- Playwright steps: open checkout and submit",
                        "- Expected result: checkout completes",
                        "- Failure evidence: submit button was hidden",
                        "- Matching rule: checkout web-route ux-product activation",
                        "- Owner profile: ux-product",
                        "- Last failed: 2026-07-09T00:00:00Z",
                        "- Last passed: 2026-07-09T00:00:00Z",
                        "- Status: active",
                    ]
                ),
                encoding="utf-8",
            )

            completed = run(
                [
                    "python3",
                    "scripts/select_benchmarks.py",
                    "--repo",
                    raw,
                    "--profile",
                    "ux-product",
                    "--intent",
                    "UX_OPTIMIZE",
                    "--surface",
                    "checkout web-route",
                    "--metric",
                    "activation",
                    "--require",
                ]
            )
            self.assertNotEqual(completed.returncode, 0, completed.stdout)
            self.assertIn("Selected 0 benchmark case", completed.stdout)
            self.assertNotIn("checkout-visible-flow", completed.stdout)

    def test_pressure_eval_covers_evaluation_contract_before_action(self) -> None:
        completed = run(
            [
                "python3",
                "benchmark/run_pressure_eval.py",
                "--case",
                "evaluation_contract_before_action",
                "--transcripts",
                "benchmark/fixtures/pass",
            ]
        )
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertIn("PASS evaluation_contract_before_action", completed.stdout)

    def test_templates_include_scale_retention_archive_guidance(self) -> None:
        benchmark = (ROOT / "assets" / "templates" / "PRODUCT_LOOP_BENCHMARK.md").read_text(encoding="utf-8")
        run_log = (ROOT / "assets" / "templates" / "product-loop-run-log.template.md").read_text(encoding="utf-8")
        state_schema = (ROOT / "references" / "state-schema.md").read_text(encoding="utf-8")

        self.assertIn("benchmarks/active/<case-id>.md", benchmark)
        self.assertIn("benchmarks/archive/<case-id>.md", benchmark)
        self.assertNotIn("## Regression Case: sample-case-id", benchmark)
        self.assertIn("runs/archive/", run_log)
        self.assertIn("runs/archive/", state_schema)

    def test_audit_fails_when_latest_run_log_entry_is_unstructured(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            artifact_root = self.scaffold(Path(raw))
            log_path = artifact_root / "product-loop-run-log.md"
            with log_path.open("a", encoding="utf-8") as handle:
                handle.write(
                    "\n### 2099-01-01T00:00:00Z\n\n"
                    "- Profile: engineering-quality\n"
                    "- Verdict: PASS\n"
                    "- Next scheduling decision: stop_success\n"
                )

            completed = run(["python3", "scripts/product_loop_audit.py", str(artifact_root), "--min-level", "L3"])
            self.assertNotEqual(completed.returncode, 0, completed.stdout)
            self.assertIn("latest run-log entry invalid", completed.stdout.lower())

    def test_skill_frontmatter_description_is_trigger_only(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
        self.assertIsNotNone(match)
        description = match.group(1).strip().strip('"')
        self.assertTrue(description.startswith("Use when "), description)
        self.assertNotRegex(description, r"\b(prioritize|hypotheses|verify evidence|persist learnings|schedule the next loop)\b")

    def test_operation_uses_canonical_next_actions(self) -> None:
        text = (ROOT / "references" / "operation.md").read_text(encoding="utf-8")
        self.assertIn("`stop_success`", text)
        self.assertIn("`run_again_now`", text)
        self.assertNotIn("`NEXT_ITERATION`", text)
        self.assertNotIn("`REPLAN`", text)

    def test_select_benchmarks_matches_skill_package_self_development(self) -> None:
        completed = run(
            [
                "python3",
                "scripts/select_benchmarks.py",
                "--repo",
                str(ROOT),
                "--profile",
                "engineering-quality",
                "--intent",
                "ENGINEERING_QUALITY",
                "--surface",
                "skill-package",
                "--include-skill",
                "--require",
            ]
        )
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertIn("strict_run_log_validator", completed.stdout)


if __name__ == "__main__":
    unittest.main()
