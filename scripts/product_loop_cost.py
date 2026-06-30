#!/usr/bin/env python3
"""Estimate product loop cost from the bundled pattern registry."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REGISTRY = Path(__file__).resolve().parents[1] / "assets" / "templates" / "product-loop-patterns.json"
LEVEL_MULTIPLIER = {"L1": 1.0, "L2": 2.4, "L3": 3.2}


def runs_per_day(cadence: str) -> float:
    value = cadence.strip().lower()
    if value in {"manual", "on-release", "on-demand"}:
        return 0.0
    match = re.fullmatch(r"(\d+)(m|h|d|w)", value)
    if not match:
        raise ValueError("cadence must look like 15m, 2h, 1d, 1w, manual, on-demand, or on-release")
    amount = int(match.group(1))
    unit = match.group(2)
    if amount <= 0:
        raise ValueError("cadence amount must be positive")
    if unit == "m":
        return 1440 / amount
    if unit == "h":
        return 24 / amount
    if unit == "d":
        return 1 / amount
    if unit == "w":
        return 1 / (amount * 7)
    raise AssertionError(unit)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", required=True, help="Pattern id from product-loop-patterns.json")
    parser.add_argument("--level", choices=sorted(LEVEL_MULTIPLIER), default="L1")
    parser.add_argument("--cadence", default=None, help="Override cadence, e.g. 1d, 2h, 1w")
    parser.add_argument("--registry", default=str(REGISTRY), help="Path to product-loop-patterns.json")
    args = parser.parse_args()

    registry = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    patterns = {p["id"]: p for p in registry.get("patterns", [])}
    if args.pattern not in patterns:
        available = ", ".join(sorted(patterns))
        raise SystemExit(f"Unknown pattern {args.pattern!r}. Available: {available}")

    pattern = patterns[args.pattern]
    cost = pattern["cost"]
    cadence = args.cadence or str(pattern.get("cadence", "manual")).split("-")[0]
    daily_runs = runs_per_day(cadence)

    if args.level == "L1":
        tokens_per_run = int(cost["tokens_report"])
    elif args.level == "L2":
        tokens_per_run = int(cost["tokens_action"])
    else:
        tokens_per_run = int(cost["tokens_action"] * LEVEL_MULTIPLIER["L3"])

    daily_tokens = int(tokens_per_run * daily_runs) if daily_runs else tokens_per_run
    cap = int(cost["suggested_daily_cap"])
    status = "OK" if daily_runs == 0 or daily_tokens <= cap else "OVER_CAP"

    print(f"Pattern: {pattern['id']} ({pattern['name']})")
    print(f"Level: {args.level}")
    print(f"Cadence: {cadence}")
    print(f"Runs/day: {daily_runs:.2f}" if daily_runs else "Runs/day: manual/event")
    print(f"Estimated tokens/run: {tokens_per_run}")
    print(f"Estimated tokens/day: {daily_tokens}")
    print(f"Suggested daily cap: {cap}")
    print(f"Early exit required: {str(cost.get('early_exit_required', False)).lower()}")
    print(f"Status: {status}")

    return 0 if status == "OK" else 2


if __name__ == "__main__":
    raise SystemExit(main())
