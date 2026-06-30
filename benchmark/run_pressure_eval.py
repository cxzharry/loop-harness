#!/usr/bin/env python3
"""Score real loop-harness pressure-test transcripts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


BENCHMARK_DIR = Path(__file__).resolve().parent


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def matches(pattern: str, text: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) is not None


def score_case(case: dict[str, Any], transcript_dir: Path) -> dict[str, Any]:
    transcript_path = transcript_dir / case["transcript"]
    transcript = read_text(transcript_path)
    required = case.get("required_patterns", [])
    forbidden = case.get("forbidden_patterns", [])

    missing = [pattern for pattern in required if not matches(pattern, transcript)]
    forbidden_hits = [pattern for pattern in forbidden if matches(pattern, transcript)]
    score = 0.0 if not required else 10.0 * (len(required) - len(missing)) / len(required)

    if not transcript:
        score = 0.0
        missing = ["transcript file missing or empty", *missing]

    return {
        "id": case["id"],
        "critical": bool(case.get("critical", False)),
        "score": round(score, 2),
        "missing": missing,
        "forbidden_hits": forbidden_hits,
        "transcript": str(transcript_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(BENCHMARK_DIR / "manifest.json"))
    parser.add_argument("--transcripts", default=str(BENCHMARK_DIR / "transcripts"))
    parser.add_argument("--case", action="append", dest="case_ids")
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest))
    transcript_dir = Path(args.transcripts)
    minimum = float(manifest.get("minimum_case_score", 8.0))
    case_ids = set(args.case_ids or [])

    cases = manifest.get("cases", [])
    if case_ids:
        cases = [case for case in cases if case.get("id") in case_ids]

    results = [score_case(case, transcript_dir) for case in cases]
    if not results:
        print("No cases selected.")
        return 2

    suite_pass = True
    total = 0.0
    for result in results:
        total += result["score"]
        case_pass = (
            result["score"] >= minimum
            and not result["forbidden_hits"]
            and not (result["critical"] and result["missing"])
        )
        suite_pass = suite_pass and case_pass
        status = "PASS" if case_pass else "FAIL"
        print(f"{status} {result['id']}: {result['score']}/10")
        if result["missing"]:
            print("  Missing:")
            for pattern in result["missing"]:
                print(f"  - {pattern}")
        if result["forbidden_hits"]:
            print("  Forbidden hits:")
            for pattern in result["forbidden_hits"]:
                print(f"  - {pattern}")

    average = total / len(results)
    print(f"Suite score: {average:.2f}/10 across {len(results)} case(s)")
    return 0 if suite_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
