#!/usr/bin/env python3
"""Score real loop-harness pressure-test transcripts."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any


BENCHMARK_DIR = Path(__file__).resolve().parent
SECTION_RE = re.compile(r"^#{2,6}\s+(.+?)\s*$", flags=re.MULTILINE)
FIELD_RE = re.compile(r"^-\s*([^:]+):\s*(.*?)\s*$", flags=re.MULTILINE)
NEGATED_REQUIRED_RE = re.compile(
    r"\b(skip|skipped|skipping|not run|not executed|not used|not applied|omitted|bypassed|superficial|superficially)\b",
    flags=re.IGNORECASE,
)
BAD_FIELD_VALUES = {
    "",
    "-",
    "none",
    "n/a",
    "na",
    "not applicable",
    "not_applicable",
    "pending",
    "tbd",
    "todo",
    "unknown",
    "not run",
    "not executed",
    "not filled",
}


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def is_negated_required_match(text: str, match: re.Match[str]) -> bool:
    start = max(0, match.start() - 80)
    end = min(len(text), match.end() + 80)
    context = text[start:end]
    return NEGATED_REQUIRED_RE.search(context) is not None


def matches_required(pattern: str, text: str) -> bool:
    for match in re.finditer(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
        if not is_negated_required_match(text, match):
            return True
    return False


def matches_forbidden(pattern: str, text: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) is not None


def normalize_label(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def parse_sections(text: str) -> dict[str, str]:
    matches = list(SECTION_RE.finditer(text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[normalize_label(match.group(1))] = text[start:end]
    return sections


def parse_fields(section_text: str) -> dict[str, str]:
    return {
        normalize_label(label): value.strip()
        for label, value in FIELD_RE.findall(section_text)
    }


def has_real_field_value(value: str) -> bool:
    normalized = normalize_label(value)
    if normalized in BAD_FIELD_VALUES:
        return False
    if re.search(r"\b(not run|not executed|not filled|placeholder only|listed but not filled)\b", normalized):
        return False
    return True


def check_required_sections(case: dict[str, Any], transcript: str) -> list[str]:
    missing: list[str] = []
    sections = parse_sections(transcript)
    for requirement in case.get("required_sections", []):
        section_name = normalize_label(str(requirement.get("name", "")))
        section_text = sections.get(section_name)
        if section_text is None:
            missing.append(f"section missing: {section_name}")
            continue

        fields = parse_fields(section_text)
        for field_name in requirement.get("required_fields", []):
            normalized_field = normalize_label(str(field_name))
            value = fields.get(normalized_field)
            if value is None:
                missing.append(f"field missing: {section_name}.{normalized_field}")
            elif not has_real_field_value(value):
                missing.append(f"field empty: {section_name}.{normalized_field}")
    return missing


def score_case(case: dict[str, Any], transcript_dir: Path) -> dict[str, Any]:
    transcript_path = transcript_dir / case["transcript"]
    transcript = read_text(transcript_path)
    required = case.get("required_patterns", [])
    forbidden = case.get("forbidden_patterns", [])

    missing = [pattern for pattern in required if not matches_required(pattern, transcript)]
    missing.extend(check_required_sections(case, transcript))
    forbidden_hits = [pattern for pattern in forbidden if matches_forbidden(pattern, transcript)]
    required_count = len(required) + sum(
        1 + len(requirement.get("required_fields", []))
        for requirement in case.get("required_sections", [])
    )
    score = 0.0 if not required_count else 10.0 * (required_count - len(missing)) / required_count

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


def run_agent_case(case: dict[str, Any], command: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    case_file = BENCHMARK_DIR / "cases" / f"{case['id']}.md"
    transcript_path = output_dir / case["transcript"]
    env = os.environ.copy()
    env["LOOP_PRESSURE_CASE_ID"] = str(case["id"])
    env["LOOP_PRESSURE_CASE_FILE"] = str(case_file)
    env["LOOP_PRESSURE_SKILL_DIR"] = str(BENCHMARK_DIR.parent)
    completed = subprocess.run(
        command,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        check=False,
    )
    transcript_path.write_text(completed.stdout, encoding="utf-8")
    return transcript_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(BENCHMARK_DIR / "manifest.json"))
    parser.add_argument("--transcripts", default=str(BENCHMARK_DIR / "transcripts"))
    parser.add_argument("--case", action="append", dest="case_ids")
    parser.add_argument(
        "--agent-command",
        help="Run this command once per selected case and score its captured transcript. "
        "The command receives LOOP_PRESSURE_CASE_ID, LOOP_PRESSURE_CASE_FILE, and LOOP_PRESSURE_SKILL_DIR.",
    )
    parser.add_argument("--generated-transcripts", default=str(BENCHMARK_DIR / "transcripts" / "generated"))
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

    if args.agent_command:
        generated_dir = Path(args.generated_transcripts)
        for case in cases:
            run_agent_case(case, args.agent_command, generated_dir)
        transcript_dir = generated_dir
        results = [score_case(case, transcript_dir) for case in cases]

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
