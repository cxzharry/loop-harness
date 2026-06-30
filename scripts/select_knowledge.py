#!/usr/bin/env python3
"""Select loop-harness criteria from repo-local and global local knowledge."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


DEFAULT_GLOBAL_ROOT = Path.home() / ".codex" / "loop-harness" / "knowledge"
DEFAULT_ARTIFACT_DIR = ".loop-harness"

BUILTIN_PACKS: list[dict[str, Any]] = [
    {
        "id": "builtin-ux-web-route",
        "profiles": ["ux-product"],
        "intents": ["UX_OPTIMIZE"],
        "surfaces": ["web-route", "web-app", "prototype"],
        "criteria": [
            "Use Playwright for route verification when the surface can be opened.",
            "Record URL, viewport, flow steps, assertions, and console/network evidence.",
            "For visual quality, require design-taste-frontend plus design-slop-ban.",
            "Block PASS when text overflows, controls clip, or critical slop is present.",
        ],
        "benchmark_seeds": [
            {
                "id": "builtin-web-route-playwright-evidence",
                "matching_rule": "Browser-visible route or prototype verification.",
                "expected_result": "Playwright evidence includes URL, viewport, flow steps, and assertions.",
            }
        ],
    },
    {
        "id": "builtin-engineering-quality",
        "profiles": ["engineering-quality"],
        "intents": ["ENGINEERING_QUALITY"],
        "surfaces": ["codebase", "repo", "test-suite"],
        "criteria": [
            "Run focused verification for the changed behavior.",
            "Run broader verification when shared code or contracts changed.",
            "Reject PASS when tests were skipped, weakened, or replaced by claims.",
        ],
        "benchmark_seeds": [
            {
                "id": "builtin-focused-verification-required",
                "matching_rule": "Engineering-quality change with executable verification available.",
                "expected_result": "Focused verification runs and records pass/fail evidence.",
            }
        ],
    },
]


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def normalize(value: str) -> str:
    return value.strip().lower()


def matches(values: list[str], requested: str) -> bool:
    normalized = {normalize(value) for value in values}
    requested_normalized = normalize(requested)
    return not normalized or "*" in normalized or requested_normalized in normalized


def pack_matches(pack: dict[str, Any], profile: str, intent: str, surface: str) -> bool:
    return (
        matches([str(v) for v in pack.get("profiles", [])], profile)
        and matches([str(v) for v in pack.get("intents", [])], intent)
        and matches([str(v) for v in pack.get("surfaces", [])], surface)
    )


def load_global_packs(global_root: Path) -> list[dict[str, Any]]:
    registry = load_json(global_root / "registry.json")
    packs = registry.get("criteria_packs", [])
    if not isinstance(packs, list):
        return []
    return [pack for pack in packs if isinstance(pack, dict)]


def read_repo_benchmark(repo: Path) -> str:
    candidates = [
        repo / DEFAULT_ARTIFACT_DIR / "PRODUCT_LOOP_BENCHMARK.md",
        repo / "PRODUCT_LOOP_BENCHMARK.md",
    ]
    for candidate in candidates:
        try:
            return candidate.read_text(encoding="utf-8")
        except FileNotFoundError:
            continue
    return ""


def select_pack_sources(
    packs: list[dict[str, Any]],
    profile: str,
    intent: str,
    surface: str,
    source_name: str,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for pack in packs:
        if pack_matches(pack, profile, intent, surface):
            selected.append({"source": source_name, **pack})
    return selected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=os.getcwd(), help="Product repo root")
    parser.add_argument("--profile", required=True)
    parser.add_argument("--intent", required=True)
    parser.add_argument("--surface", required=True)
    parser.add_argument("--global-root", default=str(DEFAULT_GLOBAL_ROOT))
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    global_root = Path(args.global_root).expanduser().resolve()
    global_packs = load_global_packs(global_root)

    selected = select_pack_sources(global_packs, args.profile, args.intent, args.surface, "global-local")
    if not selected:
        selected = select_pack_sources(BUILTIN_PACKS, args.profile, args.intent, args.surface, "builtin-fallback")

    criteria: list[dict[str, str]] = []
    benchmark_seeds: list[dict[str, Any]] = []
    for pack in selected:
        pack_id = str(pack.get("id", "unknown-pack"))
        source = str(pack.get("source", "unknown"))
        for criterion in pack.get("criteria", []):
            criteria.append({"id": pack_id, "source": source, "text": str(criterion)})
        for seed in pack.get("benchmark_seeds", []):
            if isinstance(seed, dict):
                benchmark_seeds.append({"source": source, "pack_id": pack_id, **seed})
            else:
                benchmark_seeds.append({"source": source, "pack_id": pack_id, "id": str(seed)})

    result = {
        "profile": args.profile,
        "intent": args.intent,
        "surface": args.surface,
        "global_root": str(global_root),
        "repo": str(repo),
        "selection_mode": "subset-matching",
        "selected_packs": [
            {"id": str(pack.get("id", "unknown-pack")), "source": str(pack.get("source", "unknown"))}
            for pack in selected
        ],
        "criteria": criteria,
        "benchmark_seeds": benchmark_seeds,
        "repo_benchmark_present": bool(read_repo_benchmark(repo).strip()),
        "state_instruction": "Record selected criteria and benchmark seeds in .loop-harness/PRODUCT_LOOP_STATE.md; do not activate seeds without repo-local evidence.",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
