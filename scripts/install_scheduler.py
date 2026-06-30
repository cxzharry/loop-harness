#!/usr/bin/env python3
"""Generate local scheduler files for a loop-harness run."""

from __future__ import annotations

import argparse
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
        path.write_text(
            f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>{args.label}</string>
  <key>WorkingDirectory</key><string>{repo}</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/zsh</string>
    <string>-lc</string>
    <string>{args.command}</string>
  </array>
  <key>StartInterval</key><integer>{interval}</integer>
  <key>StandardOutPath</key><string>{repo / DEFAULT_ARTIFACT_DIR / 'schedules' / (args.label + '.out.log')}</string>
  <key>StandardErrorPath</key><string>{repo / DEFAULT_ARTIFACT_DIR / 'schedules' / (args.label + '.err.log')}</string>
</dict>
</plist>
""",
            encoding="utf-8",
        )
        print(path)
    else:
        path = schedule_dir / f"{args.label}.cron"
        minutes = max(1, interval // 60)
        path.write_text(f"*/{minutes} * * * * cd {shlex.quote(str(repo))} && {args.command}\n", encoding="utf-8")
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
