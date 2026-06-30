#!/usr/bin/env python3
"""Read a metric source and decide PASS/FAIL/UNKNOWN for loop verification."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from statistics import mean
from typing import Any


def load_values(path: Path, metric: str) -> list[float]:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix == ".json":
        data = json.loads(text)
        if isinstance(data, dict):
            value = data.get(metric)
            if isinstance(value, list):
                return [float(item) for item in value]
            if value is not None:
                return [float(value)]
        if isinstance(data, list):
            values: list[float] = []
            for item in data:
                if isinstance(item, dict) and metric in item:
                    values.append(float(item[metric]))
            return values
    if suffix == ".csv":
        values = []
        for row in csv.DictReader(text.splitlines()):
            if metric in row and row[metric] not in {"", None}:
                values.append(float(row[metric]))
        return values
    return [float(match.group(1)) for match in re.finditer(rf"{re.escape(metric)}\s*[:=]\s*(-?\d+(?:\.\d+)?)", text)]


def compare(value: float, target: float, direction: str) -> str:
    if direction == "decrease":
        return "PASS" if value <= target else "FAIL"
    return "PASS" if value >= target else "FAIL"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="JSON, CSV, or text metric source.")
    parser.add_argument("--metric", required=True)
    parser.add_argument("--target", type=float, required=True)
    parser.add_argument("--direction", choices=["increase", "decrease"], default="increase")
    parser.add_argument("--aggregate", choices=["latest", "mean", "min", "max"], default="latest")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    values = load_values(Path(args.source), args.metric)
    if not values:
        result: dict[str, Any] = {
            "verdict": "UNKNOWN",
            "metric": args.metric,
            "reason": "metric not found",
            "values": [],
        }
    else:
        aggregate_value = {
            "latest": values[-1],
            "mean": mean(values),
            "min": min(values),
            "max": max(values),
        }[args.aggregate]
        result = {
            "verdict": compare(float(aggregate_value), args.target, args.direction),
            "metric": args.metric,
            "value": aggregate_value,
            "target": args.target,
            "direction": args.direction,
            "aggregate": args.aggregate,
            "values": values,
        }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"{result['verdict']} {args.metric}: {result.get('value', 'n/a')} target={args.target}")
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
