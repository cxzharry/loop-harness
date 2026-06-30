#!/usr/bin/env python3
"""Audit product loop readiness artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FILES = {
    "loop": "PRODUCT_LOOP.md",
    "state": "PRODUCT_LOOP_STATE.md",
    "log": "product-loop-run-log.md",
    "budget": "product-loop-budget.md",
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
PATTERN_FILE = "product-loop-patterns.json"
STARTER_DIRS = [
    "minimal-l1-report-only",
    "assisted-l2-product-fix",
    "scheduled-l3-product-loop",
]


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").lower()
    except FileNotFoundError:
        return ""


def load_patterns(root: Path) -> list[dict]:
    candidates = [
        root / PATTERN_FILE,
        root / "assets" / "templates" / PATTERN_FILE,
    ]
    for candidate in candidates:
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            continue
        patterns = data.get("patterns", [])
        if isinstance(patterns, list):
            return [p for p in patterns if isinstance(p, dict)]
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Product repo or folder to audit")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    score = 0
    findings: list[str] = []

    contents = {key: read(root / filename) for key, filename in FILES.items()}

    for key, filename in FILES.items():
        if contents[key]:
            score += 12
            findings.append(f"OK {filename} present")
        else:
            findings.append(f"MISS {filename}")

    combined = "\n".join(contents.values())

    phase_hits = [phase for phase in PHASES if phase in combined]
    score += len(phase_hits) * 5
    missing_phases = sorted(set(PHASES) - set(phase_hits))
    if missing_phases:
        findings.append(f"MISS phases: {', '.join(missing_phases)}")
    else:
        findings.append("OK all five phases referenced")

    profile_hits = [profile for profile in PROFILES if profile in combined]
    score += min(10, len(profile_hits) * 3)
    if profile_hits:
        findings.append(f"OK profiles: {', '.join(profile_hits)}")
    else:
        findings.append("WARN no optimization profile named")

    gate_hits = [gate for gate in GATES if gate in combined]
    score += len(gate_hits) * 4
    missing_gates = sorted(set(GATES) - set(gate_hits))
    if missing_gates:
        findings.append(f"WARN missing gates: {', '.join(missing_gates)}")
    else:
        findings.append("OK budget, kill switch, denylist, and human gate present")

    budget_hits = [field for field in BUDGET_FIELDS if field in contents["budget"]]
    score += len(budget_hits) * 2
    missing_budget_fields = sorted(set(BUDGET_FIELDS) - set(budget_hits))
    if missing_budget_fields:
        findings.append(f"WARN budget fields incomplete: {', '.join(missing_budget_fields)}")
    else:
        findings.append("OK budget fields cover caps, kill switch, and escalation")

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

    starter_hits = [
        starter for starter in STARTER_DIRS
        if (root / starter).is_dir() or (root / "assets" / "templates" / starter).is_dir()
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

    has_run_log_entries = "###" in contents["log"] and "yyyy-mm-dd" not in contents["log"]
    if has_run_log_entries:
        score += 7
        findings.append("OK run log has entries")
    else:
        findings.append("WARN no real run-log entries")

    score = min(score, 100)
    if not (has_state_activity and has_run_log_entries):
        score = min(score, 87)
    if (
        score >= 80
        and not missing_phases
        and not missing_gates
        and not missing_budget_fields
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
