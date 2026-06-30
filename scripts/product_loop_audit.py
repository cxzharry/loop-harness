#!/usr/bin/env python3
"""Audit product loop readiness artifacts."""

from __future__ import annotations

import argparse
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


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").lower()
    except FileNotFoundError:
        return ""


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

    if "last run: never" not in contents["state"] and "last run:" in contents["state"]:
        score += 6
        findings.append("OK state has run activity")
    else:
        findings.append("WARN no proven state activity")

    if "###" in contents["log"] and "yyyy-mm-dd" not in contents["log"]:
        score += 7
        findings.append("OK run log has entries")
    else:
        findings.append("WARN no real run-log entries")

    score = min(score, 100)
    if score >= 80 and not missing_phases and not missing_gates:
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
