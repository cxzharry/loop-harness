#!/usr/bin/env python3
"""Select repo-local and skill benchmark cases relevant to a loop run."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_ARTIFACT_DIR = ".loop-harness"
CASE_RE = re.compile(r"^##\s+Regression Case:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
FIELD_RE = re.compile(r"^-\s*([^:]+):\s*(.*?)\s*$", re.MULTILINE)


def resolve_artifact_root(repo: Path) -> Path:
    if (repo / "PRODUCT_LOOP_BENCHMARK.md").exists():
        return repo
    return repo / DEFAULT_ARTIFACT_DIR


def words(*values: str) -> set[str]:
    joined = " ".join(value for value in values if value)
    return {part for part in re.split(r"[^a-z0-9_.:/-]+", joined.lower()) if part}


def parse_regression_cases(path: Path) -> list[dict[str, Any]]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    matches = list(CASE_RE.finditer(text))
    cases: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end]
        fields = {label.strip().lower(): value.strip() for label, value in FIELD_RE.findall(block)}
        status = fields.get("status", "").lower()
        if status and status != "active":
            continue
        cases.append(
            {
                "id": match.group(1).strip(),
                "source": str(path),
                "type": "repo-regression",
                "owner_profile": fields.get("owner profile", ""),
                "surface": fields.get("surface/url", ""),
                "matching_rule": fields.get("matching rule", ""),
                "verification_command": fields.get("verification command", ""),
                "expected_result": fields.get("expected result", ""),
                "score": 0,
                "fields": fields,
            }
        )
    return cases


def load_skill_cases() -> list[dict[str, Any]]:
    manifest = SKILL_DIR / "benchmark" / "manifest.json"
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    cases: list[dict[str, Any]] = []
    for case in data.get("cases", []):
        case_id = str(case.get("id", ""))
        description = str(case.get("description", ""))
        cases.append(
            {
                "id": case_id,
                "source": str(manifest),
                "type": "skill-pressure",
                "owner_profile": "",
                "surface": "",
                "matching_rule": description,
                "verification_command": f"python3 {SKILL_DIR}/benchmark/run_pressure_eval.py --case {case_id}",
                "expected_result": "case score >= manifest minimum and no forbidden hits",
                "critical": bool(case.get("critical", False)),
                "score": 0,
            }
        )
    return cases


def score_case(case: dict[str, Any], query_terms: set[str], critical_only: bool) -> dict[str, Any]:
    haystack = words(
        str(case.get("id", "")),
        str(case.get("owner_profile", "")),
        str(case.get("surface", "")),
        str(case.get("matching_rule", "")),
        str(case.get("expected_result", "")),
    )
    overlap = sorted(haystack & query_terms)
    score = len(overlap)
    if critical_only and not case.get("critical", False) and case.get("type") == "skill-pressure":
        score = -1
    selected = score > 0 or (case.get("critical", False) and case.get("type") == "skill-pressure")
    enriched = dict(case)
    enriched["score"] = score
    enriched["matched_terms"] = overlap
    enriched["selected"] = selected
    return enriched


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--profile", default="")
    parser.add_argument("--intent", default="")
    parser.add_argument("--surface", default="")
    parser.add_argument("--metric", default="")
    parser.add_argument("--files", nargs="*", default=[])
    parser.add_argument("--include-skill", action="store_true")
    parser.add_argument("--critical-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--require", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    artifact_root = resolve_artifact_root(repo)
    query_terms = words(args.profile, args.intent, args.surface, args.metric, " ".join(args.files))

    cases = parse_regression_cases(artifact_root / "PRODUCT_LOOP_BENCHMARK.md")
    if args.include_skill:
        cases.extend(load_skill_cases())
    selected = [
        scored
        for scored in (score_case(case, query_terms, args.critical_only) for case in cases)
        if scored["selected"]
    ]
    selected.sort(key=lambda item: (item["score"], bool(item.get("critical"))), reverse=True)

    result = {
        "repo": str(repo),
        "artifact_root": str(artifact_root),
        "query": {
            "profile": args.profile,
            "intent": args.intent,
            "surface": args.surface,
            "metric": args.metric,
            "files": args.files,
        },
        "selected_count": len(selected),
        "cases": selected,
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Selected {len(selected)} benchmark case(s)")
        for case in selected:
            print(f"- {case['id']} [{case['type']}] score={case['score']} source={case['source']}")
    if args.require and not selected:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
