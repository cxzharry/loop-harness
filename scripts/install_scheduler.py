#!/usr/bin/env python3
"""Generate local scheduler files for a loop-harness run."""

from __future__ import annotations

import argparse
import plistlib
import shlex
from pathlib import Path


DEFAULT_ARTIFACT_DIR = ".loop-harness"


def cadence_to_start_interval(cadence: str) -> int:
    table = {
        "hourly": 3600,
        "daily": 86400,
        "weekly": 604800,
    }
    if cadence in table:
        return table[cadence]
    if cadence.endswith("m"):
        return int(cadence[:-1]) * 60
    if cadence.endswith("h"):
        return int(cadence[:-1]) * 3600
    if cadence.endswith("d"):
        return int(cadence[:-1]) * 86400
    raise ValueError(f"unsupported cadence: {cadence}")


def cadence_to_cron(cadence: str) -> str:
    if cadence == "hourly":
        return "0 * * * *"
    if cadence == "daily":
        return "0 0 * * *"
    if cadence == "weekly":
        return "0 0 * * 0"
    if cadence.endswith("m"):
        minutes = int(cadence[:-1])
        if not 1 <= minutes <= 59:
            raise ValueError("minute cron cadence must be between 1m and 59m")
        return f"*/{minutes} * * * *"
    if cadence.endswith("h"):
        hours = int(cadence[:-1])
        if not 1 <= hours <= 23:
            raise ValueError("hour cron cadence must be between 1h and 23h")
        return f"0 */{hours} * * *"
    if cadence.endswith("d"):
        days = int(cadence[:-1])
        if days != 1:
            raise ValueError("cron day cadence supports daily only; use launchd for multi-day intervals")
        return "0 0 * * *"
    raise ValueError(f"unsupported cadence: {cadence}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--command", required=True)
    parser.add_argument("--cadence", default="daily")
    parser.add_argument("--kind", choices=["launchd", "cron"], default="launchd")
    parser.add_argument("--label", default="local.loop-harness")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    schedule_dir = repo / DEFAULT_ARTIFACT_DIR / "schedules"
    schedule_dir.mkdir(parents=True, exist_ok=True)
    interval = cadence_to_start_interval(args.cadence)

    if args.kind == "launchd":
        path = schedule_dir / f"{args.label}.plist"
        data = {
            "Label": args.label,
            "WorkingDirectory": str(repo),
            "ProgramArguments": ["/bin/zsh", "-lc", args.command],
            "StartInterval": interval,
            "StandardOutPath": str(repo / DEFAULT_ARTIFACT_DIR / "schedules" / f"{args.label}.out.log"),
            "StandardErrorPath": str(repo / DEFAULT_ARTIFACT_DIR / "schedules" / f"{args.label}.err.log"),
        }
        with path.open("wb") as handle:
            plistlib.dump(data, handle)
        print(path)
    else:
        path = schedule_dir / f"{args.label}.cron"
        path.write_text(f"{cadence_to_cron(args.cadence)} cd {shlex.quote(str(repo))} && {args.command}\n", encoding="utf-8")
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
