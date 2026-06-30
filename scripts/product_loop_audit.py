#!/usr/bin/env python3
"""Audit product loop readiness artifacts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FILES = {
    "loop": "PRODUCT_LOOP.md",
    "state": "PRODUCT_LOOP_STATE.md",
    "log": "product-loop-run-log.md",
    "benchmark": "PRODUCT_LOOP_BENCHMARK.md",
    "budget": "product-loop-budget.md",
    "handoff": "AGENT_HANDOFF.md",
    "worktree": "worktree-map.md",
}
FILE_FALLBACKS = {
    "log": ["product-loop-run-log.template.md"],
}

PHASES = ["discovery", "handoff", "verification", "persistence", "scheduling"]
PROFILES = [
    "ux-product",
    "metrics-growth",
    "engineering-quality",
    "content-docs",
    "release-readiness",
]
GATES = ["human gate", "denylist", "kill switch", "budget"]
BUDGET_FIELDS = ["max runs", "max actioning changes", "kill switch", "escalation"]
RUN_UNTIL_DONE_BUDGET_FIELDS = ["plateau patience", "token", "time budget", "wall-clock", "kill switch"]
ITERATION_FIELDS = ["execution mode", "current iteration", "target", "latest verdict", "stop condition"]
INTENT_FIELDS = ["intent", "primary metric", "baseline window", "user confirmations"]
PLAYWRIGHT_FIELDS = ["playwright", "url", "viewport", "flow steps", "assertions"]
PROMOTION_FIELDS = ["promotion", "state", "benchmark"]
RUN_LOG_FINDING_FIELDS = [
    "raw run result",
    "finding",
    "finding id",
    "symptom",
    "evidence",
    "root cause/hypothesis",
    "reproduction steps",
    "severity",
    "confidence",
    "benchmark promotion",
    "promotion decision",
    "benchmark case id",
]
BENCHMARK_FIELDS = ["known-good flows", "regression checks", "do not regress"]
ORCHESTRATION_FIELDS = [
    "execution strategy",
    "parallel agents",
    "agent handoff",
    "agent tasks",
    "worktree isolation",
    "worktree map",
    "conflict review",
    "integration verification",
]
REGRESSION_CASE_FIELDS = [
    "regression case",
    "error class",
    "trigger condition",
    "expected result",
    "failure evidence",
    "matching rule",
    "owner profile",
    "last failed",
    "last passed",
    "status: active",
]
FAILURE_VERDICTS = ["fail", "regression", "partial", "env", "unknown"]
STOP_CONDITIONS = ["success", "exhausted", "plateau", "regression", "budget", "human_gate", "env", "unknown"]
PATTERN_FILE = "product-loop-patterns.json"
STARTER_DIRS = [
    "minimal-l1-report-only",
    "assisted-l2-product-fix",
    "scheduled-l3-product-loop",
]
OPTIONAL_FILES = {"handoff", "worktree"}
PLACEHOLDER_CASE_IDS = {"sample-case-id", "<stable-id>", "stable-id", ""}


CASE_HEADING_RE = re.compile(r"^##\s+Regression Case:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
FIELD_RE = re.compile(r"^-[ \t]*([^:]+):[ \t]*(.*?)[ \t]*$", re.IGNORECASE | re.MULTILINE)
VERDICT_RE = re.compile(r"\bverdict\s*:\s*(fail|regression|partial|env|unknown)\b", re.IGNORECASE)
RUN_LOG_ENTRY_RE = re.compile(r"^###\s+\d{4}-\d{2}-\d{2}t\d{2}:\d{2}:\d{2}z\b", re.IGNORECASE | re.MULTILINE)
NEGATED_EVIDENCE_RE = re.compile(
    r"("
    r"\b(no|missing|absent)[^\n]{0,80}\b("
    r"human gate|denylist|kill switch|budget|playwright|assertions|verification|promotion|benchmark|"
    r"finding|raw run result|benchmark promotion|execution strategy|worktree map|conflict review|integration verification"
    r")\b"
    r"|"
    r"\b("
    r"human gate|denylist|kill switch|budget|playwright|assertions|verification|promotion|benchmark|"
    r"finding|raw run result|benchmark promotion|execution strategy|worktree map|conflict review|integration verification"
    r")[^\n]{0,80}\b(not run|not executed|not filled|not available|listed but not filled|placeholder only)\b"
    r")",
    re.IGNORECASE,
)
POLICY_LINE_RE = re.compile(
    r"("
    r"\b(do not|don't|should not|must not|not yet present)\b"
    r"|rule:|baseline value:|symptom:|trigger condition:|reproduction steps:|failure evidence:"
    r"|\bcode review found\b|\bpre-fix\b|\bfailed as expected\b|\bkeep schema detection separate\b|\bdid not require\b"
    r")",
    re.IGNORECASE,
)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").lower()
    except FileNotFoundError:
        return ""


def read_artifact(root: Path, key: str, filename: str) -> str:
    content = read(root / filename)
    if content:
        return content
    for fallback in FILE_FALLBACKS.get(key, []):
        content = read(root / fallback)
        if content:
            return content
    return ""


def has_positive_field(content: str, field: str) -> bool:
    pattern = re.compile(re.escape(field), re.IGNORECASE)
    for line in content.splitlines():
        if not pattern.search(line):
            continue
        if not NEGATED_EVIDENCE_RE.search(line):
            return True
    return False


def present_fields(content: str, fields: list[str]) -> list[str]:
    return [field for field in fields if has_positive_field(content, field)]


def normalize_label(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def structured_field_hits(content: str, fields: list[str]) -> list[str]:
    field_labels = {normalize_label(label) for label, _value in FIELD_RE.findall(content)}
    headings = {
        normalize_label(match.group(1))
        for match in re.finditer(r"^#{2,6}\s+(.+?)\s*$", content, re.IGNORECASE | re.MULTILINE)
    }
    hits: list[str] = []
    for field in fields:
        normalized = normalize_label(field)
        if normalized in field_labels or normalized in headings:
            hits.append(field)
    return hits


def negated_evidence_claims(content: str) -> list[str]:
    claims: list[str] = []
    for line in content.splitlines():
        if POLICY_LINE_RE.search(line):
            continue
        if NEGATED_EVIDENCE_RE.search(line):
            claims.append(line.strip())
    return claims


def load_patterns(root: Path) -> list[dict]:
    candidates = [root / PATTERN_FILE, root / "assets" / "templates" / PATTERN_FILE]
    candidates.extend(parent / "assets" / "templates" / PATTERN_FILE for parent in root.parents)
    for candidate in candidates:
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            continue
        patterns = data.get("patterns", [])
        if isinstance(patterns, list):
            return [p for p in patterns if isinstance(p, dict)]
    return []


def has_failed_iteration(log_content: str) -> bool:
    if VERDICT_RE.search(log_content):
        return True
    return any(f"latest verdict: {verdict}" in log_content for verdict in FAILURE_VERDICTS)


def parse_regression_cases(benchmark_content: str) -> list[dict[str, object]]:
    matches = list(CASE_HEADING_RE.finditer(benchmark_content))
    cases: list[dict[str, object]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(benchmark_content)
        block = benchmark_content[start:end]
        fields = {key.strip().lower(): value.strip() for key, value in FIELD_RE.findall(block)}
        cases.append({"id": match.group(1).strip().lower(), "fields": fields})
    return cases


def is_real_active_regression_case(case: dict[str, object]) -> bool:
    case_id = str(case.get("id", "")).strip().lower()
    if case_id in PLACEHOLDER_CASE_IDS:
        return False
    fields = case.get("fields", {})
    if not isinstance(fields, dict):
        return False

    status = fields.get("status", "").strip().lower()
    error_class = fields.get("error class", "").strip().lower()
    required_non_empty = [
        "source run-log entry",
        "trigger condition",
        "expected result",
        "failure evidence",
        "matching rule",
        "last failed",
    ]

    return (
        status == "active"
        and error_class in {
            "ui_regression",
            "runtime_error",
            "metric_regression",
            "content_drift",
            "env_blocker",
            "scope_regression",
        }
        and all(fields.get(field, "").strip() for field in required_non_empty)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Product repo or folder to audit")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    score = 0
    findings: list[str] = []

    contents = {key: read_artifact(root, key, filename) for key, filename in FILES.items()}

    for key, filename in FILES.items():
        if contents[key]:
            if key not in OPTIONAL_FILES:
                score += 12
            else:
                score += 3
            findings.append(f"OK {filename} present")
        else:
            if key in OPTIONAL_FILES:
                findings.append(f"WARN {filename} not present; required when dispatching agents or worktrees")
            else:
                findings.append(f"MISS {filename}")

    combined = "\n".join(contents.values())
    negated_evidence_hits = negated_evidence_claims(combined)

    phase_hits = present_fields(combined, PHASES)
    score += len(phase_hits) * 5
    missing_phases = sorted(set(PHASES) - set(phase_hits))
    if missing_phases:
        findings.append(f"MISS phases: {', '.join(missing_phases)}")
    else:
        findings.append("OK all five phases referenced")

    profile_hits = present_fields(combined, PROFILES)
    score += min(10, len(profile_hits) * 3)
    if profile_hits:
        findings.append(f"OK profiles: {', '.join(profile_hits)}")
    else:
        findings.append("WARN no optimization profile named")

    gate_hits = present_fields(combined, GATES)
    score += len(gate_hits) * 4
    missing_gates = sorted(set(GATES) - set(gate_hits))
    if missing_gates:
        findings.append(f"WARN missing gates: {', '.join(missing_gates)}")
    else:
        findings.append("OK budget, kill switch, denylist, and human gate present")

    budget_hits = present_fields(contents["budget"], BUDGET_FIELDS)
    score += len(budget_hits) * 2
    missing_budget_fields = sorted(set(BUDGET_FIELDS) - set(budget_hits))
    if missing_budget_fields:
        findings.append(f"WARN budget fields incomplete: {', '.join(missing_budget_fields)}")
    else:
        findings.append("OK budget fields cover caps, kill switch, and escalation")

    run_until_done_budget_hits = [
        field for field in RUN_UNTIL_DONE_BUDGET_FIELDS
        if has_positive_field(contents["budget"], field) or has_positive_field(combined, field)
    ]
    score += min(6, len(run_until_done_budget_hits) * 2)
    has_plateau_patience = has_positive_field(combined, "plateau patience")
    has_safety_budget = any(has_positive_field(combined, field) for field in ["token", "time budget", "wall-clock", "kill switch"])
    missing_run_until_done_budget_fields = []
    if not has_plateau_patience:
        missing_run_until_done_budget_fields.append("plateau patience")
    if not has_safety_budget:
        missing_run_until_done_budget_fields.append("safety budget or kill switch")
    if missing_run_until_done_budget_fields:
        findings.append(f"WARN run-until-done safety fields incomplete: {', '.join(missing_run_until_done_budget_fields)}")
    else:
        findings.append("OK run-until-done safety budget and plateau patience present")

    iteration_hits = present_fields(combined, ITERATION_FIELDS)
    score += len(iteration_hits) * 2
    missing_iteration_fields = sorted(set(ITERATION_FIELDS) - set(iteration_hits))
    if missing_iteration_fields:
        findings.append(f"WARN run-until-done fields incomplete: {', '.join(missing_iteration_fields)}")
    else:
        findings.append("OK run-until-done state fields present")

    intent_hits = present_fields(combined, INTENT_FIELDS)
    score += len(intent_hits) * 2
    missing_intent_fields = sorted(set(INTENT_FIELDS) - set(intent_hits))
    if missing_intent_fields:
        findings.append(f"WARN intent/metric confirmation fields incomplete: {', '.join(missing_intent_fields)}")
    else:
        findings.append("OK intent and metric confirmation fields present")

    playwright_hits = present_fields(combined, PLAYWRIGHT_FIELDS)
    score += len(playwright_hits) * 2
    missing_playwright_fields = sorted(set(PLAYWRIGHT_FIELDS) - set(playwright_hits))
    if missing_playwright_fields:
        findings.append(f"WARN Playwright verification fields incomplete: {', '.join(missing_playwright_fields)}")
    else:
        findings.append("OK Playwright verification fields present")

    promotion_hits = present_fields(contents["log"], PROMOTION_FIELDS)
    score += len(promotion_hits) * 2
    missing_promotion_fields = sorted(set(PROMOTION_FIELDS) - set(promotion_hits))
    if missing_promotion_fields:
        findings.append(f"WARN log promotion fields incomplete: {', '.join(missing_promotion_fields)}")
    else:
        findings.append("OK run-log promotion fields present")

    finding_hits = structured_field_hits(contents["log"], RUN_LOG_FINDING_FIELDS)
    score += min(8, len(finding_hits))
    missing_finding_fields = sorted(set(RUN_LOG_FINDING_FIELDS) - set(finding_hits))
    if missing_finding_fields:
        findings.append(f"WARN run-log finding schema incomplete: {', '.join(missing_finding_fields)}")
    else:
        findings.append("OK run-log raw result, finding, and benchmark promotion schema present")

    benchmark_hits = present_fields(contents["benchmark"], BENCHMARK_FIELDS)
    score += len(benchmark_hits) * 2
    missing_benchmark_fields = sorted(set(BENCHMARK_FIELDS) - set(benchmark_hits))
    if missing_benchmark_fields:
        findings.append(f"WARN benchmark fields incomplete: {', '.join(missing_benchmark_fields)}")
    else:
        findings.append("OK benchmark promotion fields present")

    orchestration_hits = present_fields(combined, ORCHESTRATION_FIELDS)
    score += len(orchestration_hits) * 2
    missing_orchestration_fields = sorted(set(ORCHESTRATION_FIELDS) - set(orchestration_hits))
    if missing_orchestration_fields:
        findings.append(f"WARN execution orchestration fields incomplete: {', '.join(missing_orchestration_fields)}")
    else:
        findings.append("OK execution orchestration fields present")

    regression_case_hits = present_fields(contents["benchmark"], REGRESSION_CASE_FIELDS)
    score += min(10, len(regression_case_hits))
    missing_regression_case_fields = sorted(set(REGRESSION_CASE_FIELDS) - set(regression_case_hits))
    if missing_regression_case_fields:
        findings.append(f"WARN regression case schema incomplete: {', '.join(missing_regression_case_fields)}")
    else:
        findings.append("OK regression case schema present")

    failed_iterations_present = has_failed_iteration(contents["log"])
    real_active_regression_cases = [
        case for case in parse_regression_cases(contents["benchmark"])
        if is_real_active_regression_case(case)
    ]
    missing_promoted_regression_cases = failed_iterations_present and not real_active_regression_cases
    if missing_promoted_regression_cases:
        findings.append("MISS failed iterations exist but no active promoted regression case was found")
    elif failed_iterations_present:
        score += min(5, len(real_active_regression_cases) * 5)
        findings.append(f"OK active promoted regression cases: {len(real_active_regression_cases)}")
    else:
        findings.append("OK no failed iterations require active regression cases yet")

    stop_hits = present_fields(combined, STOP_CONDITIONS)
    score += min(8, len(stop_hits))
    missing_stop_conditions = sorted(set(STOP_CONDITIONS) - set(stop_hits))
    if missing_stop_conditions:
        findings.append(f"WARN stop conditions incomplete: {', '.join(missing_stop_conditions)}")
    else:
        findings.append("OK run-until-done stop conditions present")

    patterns = load_patterns(root)
    if patterns:
        valid_patterns = [
            p for p in patterns
            if p.get("id") and p.get("cost") and set(PHASES).issubset(set(p.get("phases", [])))
        ]
        score += min(8, len(valid_patterns) * 2)
        findings.append(f"OK pattern registry: {len(valid_patterns)}/{len(patterns)} patterns with cost + five phases")
    else:
        findings.append("WARN no product-loop-patterns.json registry found")

    starter_roots = [root, root / "assets" / "templates"]
    starter_roots.extend(parent / "assets" / "templates" for parent in root.parents)
    starter_hits = [
        starter for starter in STARTER_DIRS
        if any((candidate_root / starter).is_dir() for candidate_root in starter_roots)
    ]
    score += min(6, len(starter_hits) * 2)
    if starter_hits:
        findings.append(f"OK starter modes: {', '.join(starter_hits)}")
    else:
        findings.append("WARN no L1/L2/L3 starter mode templates found")

    has_state_activity = "last run: never" not in contents["state"] and "last run:" in contents["state"]
    if has_state_activity:
        score += 6
        findings.append("OK state has run activity")
    else:
        findings.append("WARN no proven state activity")

    has_run_log_entries = bool(RUN_LOG_ENTRY_RE.search(contents["log"]))
    if has_run_log_entries:
        score += 7
        findings.append("OK run log has entries")
    else:
        findings.append("WARN no real run-log entries")

    if negated_evidence_hits:
        findings.append(f"MISS negated evidence claims present: {len(negated_evidence_hits)}")

    score = min(score, 100)
    if not (has_state_activity and has_run_log_entries):
        score = min(score, 87)
    if missing_promoted_regression_cases:
        score = min(score, 89)
    if negated_evidence_hits:
        score = min(score, 59)
    if (
        score >= 80
        and not missing_phases
        and not missing_gates
        and not missing_budget_fields
        and not missing_run_until_done_budget_fields
        and not missing_iteration_fields
        and not missing_intent_fields
        and not missing_playwright_fields
        and not missing_promotion_fields
        and not missing_finding_fields
        and not missing_benchmark_fields
        and not missing_orchestration_fields
        and not missing_regression_case_fields
        and not missing_promoted_regression_cases
        and not missing_stop_conditions
        and has_state_activity
        and has_run_log_entries
    ):
        level = "L3"
    elif score >= 60 and "verification" in phase_hits:
        level = "L2"
    elif score >= 38 and contents["state"]:
        level = "L1"
    else:
        level = "L0"

    print(f"Product Loop Readiness: {score}/100 {level}")
    for finding in findings:
        print(f"- {finding}")

    return 0 if score >= 38 else 2


if __name__ == "__main__":
    raise SystemExit(main())
