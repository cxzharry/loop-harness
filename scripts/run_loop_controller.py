#!/usr/bin/env python3
"""Run a command-backed loop until PASS or a recorded stop condition."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_ARTIFACT_DIR = ".loop-harness"
PASS_LINE_RE = re.compile(r"^\s*PASS\s*$", re.IGNORECASE)
PASS_VERDICT_LINE_RE = re.compile(r"^\s*verdict\s*[:=]\s*PASS\b", re.IGNORECASE)
SCORE_RE = re.compile(r"\b(?:score|metric)\s*[:=]\s*(-?\d+(?:\.\d+)?)\b", re.IGNORECASE)


def resolve_artifact_root(repo: Path) -> Path:
    if (repo / "product-loop-run-log.md").exists():
        return repo
    return repo / DEFAULT_ARTIFACT_DIR


def run_command(command: str, repo: Path, iteration: int) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["LOOP_REPO"] = str(repo)
    env["LOOP_ITERATION"] = str(iteration)
    return subprocess.run(
        command,
        cwd=repo,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        check=False,
    )


def extract_score(output: str) -> float | None:
    matches = SCORE_RE.findall(output)
    if not matches:
        return None
    return float(matches[-1])


def output_has_pass_verdict(output: str) -> bool:
    return any(PASS_LINE_RE.search(line) or PASS_VERDICT_LINE_RE.search(line) for line in output.splitlines())


def one_line(value: str) -> str:
    compact = re.sub(r"\s+", " ", value.strip())
    return compact[:500] if compact else "none"


def append_regression_case(
    benchmark_path: Path,
    *,
    case_id: str,
    timestamp: str,
    profile: str,
    command: str,
    output: str,
    stop: str,
) -> None:
    benchmark_path.parent.mkdir(parents=True, exist_ok=True)
    evidence = one_line(output)
    block = f"""

## Regression Case: {case_id}

- Source run-log entry: {timestamp}
- Error class: scope_regression
- Surface/URL: command-backed loop
- Trigger condition: controller command stopped with {stop}
- Playwright steps: not_applicable
- Expected result: command reaches explicit PASS verdict or target score before stop condition
- Failure evidence: {evidence}
- Matching rule: rerun `{command}` when profile={profile} or command-backed loop behavior changes
- Owner profile: {profile}
- Last failed: {timestamp}
- Last passed:
- Status: active
"""
    current = benchmark_path.read_text(encoding="utf-8") if benchmark_path.exists() else "# Product Loop Benchmark\n"
    if f"## Regression Case: {case_id}" in current:
        return
    with benchmark_path.open("a", encoding="utf-8") as handle:
        handle.write(block)


def append_log(
    log_path: Path,
    *,
    profile: str,
    iteration: int,
    command: str,
    output: str,
    verdict: str,
    stop: str,
    score: float | None,
) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    digest = hashlib.sha1(f"{timestamp}:{iteration}:{verdict}:{output}".encode("utf-8")).hexdigest()[:10]
    safe_output = one_line(output)
    stopped_failure = verdict != "PASS" and stop != "run_again_now"
    error_class = "scope_regression" if stopped_failure else "none"
    finding_status = "promoted" if stopped_failure else "not_applicable"
    promotion_decision = "promoted" if stopped_failure else "not_promoted"
    promotion_status = "active" if stopped_failure else "not_applicable"
    benchmark_case_id = f"controller-{digest}" if stopped_failure else "not_applicable"
    severity = "medium" if stopped_failure else "none"
    benchmark_promoted = f"PRODUCT_LOOP_BENCHMARK.md#{benchmark_case_id}" if stopped_failure else "not_applicable"
    if stopped_failure:
        append_regression_case(
            log_path.parent / "PRODUCT_LOOP_BENCHMARK.md",
            case_id=benchmark_case_id,
            timestamp=timestamp,
            profile=profile,
            command=command,
            output=output,
            stop=stop,
        )
    entry = f"""
### {timestamp}

#### Raw Run Result

- Profile: {profile}
- Discovery signals: command-backed loop iteration {iteration}
- Handoff: controller executed bounded command `{command}`
- Selected intervention: external action command
- Execution strategy: run-until-done controller
- Agent tasks: none
- Worktree map: not_applicable
- Conflict review: not_applicable
- Integration verification: controller command completed with exit code evidence
- Verification evidence: exit/output score={score if score is not None else 'n/a'}
- Playwright evidence: not_applicable
- Error output: {safe_output}
- Failed assertions: {safe_output if verdict != 'PASS' else 'none'}
- Verdict: {verdict}
- Files changed: controller did not inspect diff
- Next scheduling decision: {stop}

#### Finding

- Finding id: controller-{digest}
- Error class: {error_class}
- Symptom: {verdict}
- Evidence: {safe_output}
- Root cause/hypothesis: command output determines loop state
- Reproduction steps: rerun `{command}` from {log_path.parent.parent}
- Severity: {severity}
- Confidence: high
- Status: {finding_status}

#### Benchmark Promotion

- Promotion decision: {promotion_decision}
- Benchmark case id: {benchmark_case_id}
- Matching rule: controller command `{command}` must not stop with {stop}
- Expected result: command reaches PASS or target score
- Verification command: {command}
- Status: {promotion_status}
- State promoted: stop={stop}
- Benchmark promoted: {benchmark_promoted}
"""
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(entry)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--command", required=True, help="Action/verification command to execute each iteration.")
    parser.add_argument("--benchmark-command", help="Optional command that must pass before every iteration.")
    parser.add_argument("--target-score", type=float)
    parser.add_argument("--plateau-patience", type=int, default=3)
    parser.add_argument("--max-iterations", type=int, default=0, help="0 means no fixed cap; plateau/budget stops still apply.")
    parser.add_argument("--profile", default="engineering-quality")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    artifact_root = resolve_artifact_root(repo)
    log_path = artifact_root / "product-loop-run-log.md"
    best_score: float | None = None
    plateau_count = 0
    iteration = 0

    while True:
        iteration += 1
        if args.max_iterations and iteration > args.max_iterations:
            print("STOP BUDGET: max iterations reached")
            return 2

        if args.benchmark_command:
            benchmark = run_command(args.benchmark_command, repo, iteration)
            if benchmark.returncode != 0:
                append_log(
                    log_path,
                    profile=args.profile,
                    iteration=iteration,
                    command=args.benchmark_command,
                    output=benchmark.stdout,
                    verdict="REGRESSION",
                    stop="regression",
                    score=None,
                )
                print("STOP REGRESSION: benchmark command failed")
                print(benchmark.stdout)
                return 1

        completed = run_command(args.command, repo, iteration)
        output = completed.stdout
        score = extract_score(output)
        passed = completed.returncode == 0 and output_has_pass_verdict(output)
        if args.target_score is not None and score is not None:
            passed = completed.returncode == 0 and score >= args.target_score

        if score is not None:
            if best_score is None or score > best_score:
                best_score = score
                plateau_count = 0
            else:
                plateau_count += 1
        elif not passed:
            plateau_count += 1

        if passed:
            append_log(
                log_path,
                profile=args.profile,
                iteration=iteration,
                command=args.command,
                output=output,
                verdict="PASS",
                stop="stop_success",
                score=score,
            )
            print(f"PASS iteration={iteration} score={score if score is not None else 'n/a'}")
            return 0

        if plateau_count >= args.plateau_patience:
            append_log(
                log_path,
                profile=args.profile,
                iteration=iteration,
                command=args.command,
                output=output,
                verdict="PARTIAL",
                stop="plateau",
                score=score,
            )
            print(f"STOP PLATEAU iteration={iteration} best_score={best_score}")
            return 3

        append_log(
            log_path,
            profile=args.profile,
            iteration=iteration,
            command=args.command,
            output=output,
            verdict="PARTIAL",
            stop="run_again_now",
            score=score,
        )
        print(f"CONTINUE iteration={iteration} score={score if score is not None else 'n/a'}")


if __name__ == "__main__":
    raise SystemExit(main())
