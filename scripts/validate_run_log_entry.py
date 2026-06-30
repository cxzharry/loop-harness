#!/usr/bin/env python3
"""Validate the latest product-loop-run-log.md entry."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ENTRY_RE = re.compile(r"^###\s+(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\s*$", re.MULTILINE)
SECTION_RE = re.compile(r"^#{4}\s+(.+?)\s*$", re.MULTILINE)
FIELD_RE = re.compile(r"^-\s*([^:]+):\s*(.*?)\s*$", re.MULTILINE)
BAD_VALUES = {"", "-", "n/a", "na", "todo", "tbd", "pending", "not filled", "unknown"}
FAIL_VERDICTS = {"fail", "regression", "partial", "env", "unknown"}

REQUIRED = {
    "Raw Run Result": [
        "Profile",
        "Discovery signals",
        "Handoff",
        "Selected intervention",
        "Execution strategy",
        "Verification evidence",
        "Verdict",
        "Next scheduling decision",
    ],
    "Finding": [
        "Finding id",
        "Error class",
        "Symptom",
        "Evidence",
        "Root cause/hypothesis",
        "Reproduction steps",
        "Severity",
        "Confidence",
        "Status",
    ],
    "Benchmark Promotion": [
        "Promotion decision",
        "Benchmark case id",
        "Matching rule",
        "Expected result",
        "Verification command",
        "Status",
    ],
}


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def real(value: str) -> bool:
    value = normalize(value)
    return value not in BAD_VALUES and not value.startswith("<")


def latest_entry(text: str) -> tuple[str, str] | None:
    matches = list(ENTRY_RE.finditer(text))
    if not matches:
        return None
    match = matches[-1]
    end = matches[-1 + 1].start() if False else len(text)
    return match.group(1), text[match.end() : end]


def parse_sections(entry: str) -> dict[str, dict[str, str]]:
    matches = list(SECTION_RE.finditer(entry))
    sections: dict[str, dict[str, str]] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(entry)
        fields = {normalize(label): value.strip() for label, value in FIELD_RE.findall(entry[start:end])}
        sections[match.group(1).strip()] = fields
    return sections


def validate(path: Path, require_promotion_on_fail: bool) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    entry = latest_entry(text)
    errors: list[str] = []
    if entry is None:
        return {"ok": False, "errors": ["no timestamped run-log entry found"], "path": str(path)}

    timestamp, body = entry
    sections = parse_sections(body)
    for section, fields in REQUIRED.items():
        if section not in sections:
            errors.append(f"missing section: {section}")
            continue
        parsed = sections[section]
        for field in fields:
            value = parsed.get(normalize(field))
            if value is None:
                errors.append(f"missing field: {section}.{field}")
            elif not real(value):
                errors.append(f"empty field: {section}.{field}")

    raw = sections.get("Raw Run Result", {})
    finding = sections.get("Finding", {})
    promotion = sections.get("Benchmark Promotion", {})
    verdict = normalize(raw.get("verdict", ""))
    next_decision = normalize(raw.get("next scheduling decision", ""))
    promotion_decision = normalize(promotion.get("promotion decision", ""))
    promotion_status = normalize(promotion.get("status", ""))
    finding_status = normalize(finding.get("status", ""))

    if verdict in FAIL_VERDICTS and next_decision != "run_again_now" and require_promotion_on_fail:
        if promotion_decision != "promoted":
            errors.append("failed verdict must have Benchmark Promotion.Promotion decision: promoted")
        if promotion_status != "active":
            errors.append("failed verdict must have Benchmark Promotion.Status: active")
        if finding_status not in {"promoted", "open"}:
            errors.append("failed verdict must keep Finding.Status open or promoted")

    return {
        "ok": not errors,
        "timestamp": timestamp,
        "path": str(path),
        "verdict": raw.get("verdict", ""),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", help="Path to product-loop-run-log.md")
    parser.add_argument("--allow-unpromoted-fail", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate(Path(args.log), not args.allow_unpromoted_fail)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        status = "PASS" if result["ok"] else "FAIL"
        print(f"{status} latest run-log entry: {result.get('timestamp', 'none')}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
