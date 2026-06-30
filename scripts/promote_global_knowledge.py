#!/usr/bin/env python3
"""Gate repo-local findings before writing global loop-harness knowledge candidates."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_GLOBAL_ROOT = Path.home() / ".codex" / "loop-harness" / "knowledge"
DEFAULT_ARTIFACT_DIR = ".loop-harness"
REQUIRED_ARTIFACTS = [
    "PRODUCT_LOOP_STATE.md",
    "product-loop-run-log.md",
    "PRODUCT_LOOP_BENCHMARK.md",
]
BAD_VALUES = {"", "-", "none", "n/a", "na", "not_applicable", "unknown", "todo", "tbd"}
BLOCKED_ERROR_CLASSES = {"env_blocker"}
DOMAIN_SPECIFIC_HINTS = re.compile(r"\b(localhost|repo-specific|project-specific|customer-specific)\b", re.IGNORECASE)
ENTRY_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
SECTION_RE = re.compile(r"^####\s+(.+?)\s*$", re.MULTILINE)
FIELD_RE = re.compile(r"^-[ \t]*([^:]+):[ \t]*(.*?)[ \t]*$", re.MULTILINE)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def resolve_artifact_root(repo_or_artifact_root: Path) -> Path:
    if all((repo_or_artifact_root / name).exists() for name in REQUIRED_ARTIFACTS):
        return repo_or_artifact_root
    nested = repo_or_artifact_root / DEFAULT_ARTIFACT_DIR
    if all((nested / name).exists() for name in REQUIRED_ARTIFACTS):
        return nested
    return nested


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def real_value(value: str) -> bool:
    return normalize(value) not in BAD_VALUES


def latest_entry(log_text: str) -> str:
    matches = list(ENTRY_RE.finditer(log_text))
    if not matches:
        return ""
    start = matches[0].start()
    end = matches[1].start() if len(matches) > 1 else len(log_text)
    return log_text[start:end]


def parse_sections(entry: str) -> dict[str, dict[str, str]]:
    matches = list(SECTION_RE.finditer(entry))
    sections: dict[str, dict[str, str]] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(entry)
        block = entry[start:end]
        sections[normalize(match.group(1))] = {
            normalize(key): value.strip()
            for key, value in FIELD_RE.findall(block)
        }
    return sections


def evaluate_gate(sections: dict[str, dict[str, str]]) -> tuple[bool, list[str], dict[str, str]]:
    finding = sections.get("finding", {})
    promotion = sections.get("benchmark promotion", {})
    merged = {**finding, **{f"promotion.{key}": value for key, value in promotion.items()}}

    reasons: list[str] = []
    required_finding = ["finding id", "error class", "symptom", "evidence", "root cause/hypothesis", "reproduction steps", "status"]
    required_promotion = ["promotion decision", "benchmark case id", "matching rule", "expected result", "verification command", "status"]

    for field in required_finding:
        if not real_value(finding.get(field, "")):
            reasons.append(f"missing finding.{field}")
    for field in required_promotion:
        if not real_value(promotion.get(field, "")):
            reasons.append(f"missing benchmark promotion.{field}")

    if normalize(finding.get("error class", "")) in BLOCKED_ERROR_CLASSES:
        reasons.append("env blocker is not globally reusable by default")
    if normalize(promotion.get("promotion decision", "")) != "promoted":
        reasons.append("repo-local benchmark was not promoted")
    if normalize(promotion.get("status", "")) != "active":
        reasons.append("repo-local benchmark is not active")

    domain_text = " ".join(
        [
            finding.get("symptom", ""),
            finding.get("evidence", ""),
            promotion.get("matching rule", ""),
            promotion.get("expected result", ""),
        ]
    )
    if DOMAIN_SPECIFIC_HINTS.search(domain_text):
        reasons.append("finding appears domain-specific; keep repo-local unless manually generalized")

    return not reasons, reasons, merged


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Product repo root")
    parser.add_argument("--global-root", default=str(DEFAULT_GLOBAL_ROOT))
    parser.add_argument("--promote", action="store_true", help="Write to promoted/global-knowledge.jsonl instead of inbox candidates")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    artifact_root = resolve_artifact_root(repo)
    global_root = Path(args.global_root).expanduser().resolve()
    log_path = artifact_root / "product-loop-run-log.md"
    entry = latest_entry(read_text(log_path))
    sections = parse_sections(entry)
    passed, reasons, fields = evaluate_gate(sections)

    status = "candidate" if passed else "blocked"
    target = "promoted/global-knowledge.jsonl" if args.promote and passed else "inbox/candidate-knowledge.jsonl"
    if args.promote and not passed:
        status = "blocked"
        target = "inbox/blocked-knowledge.jsonl"

    payload = {
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repo": str(repo),
        "artifact_root": str(artifact_root),
        "source_log": str(log_path),
        "status": status,
        "promotion_mode": "promoted" if args.promote and passed else "candidate-inbox",
        "gate_passed": passed,
        "gate_reasons": reasons,
        "finding_id": fields.get("finding id", ""),
        "error_class": fields.get("error class", ""),
        "benchmark_case_id": fields.get("promotion.benchmark case id", ""),
        "matching_rule": fields.get("promotion.matching rule", ""),
        "expected_result": fields.get("promotion.expected result", ""),
        "verification_command": fields.get("promotion.verification command", ""),
    }

    if not args.dry_run:
        append_jsonl(global_root / target, payload)

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
