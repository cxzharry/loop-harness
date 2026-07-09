#!/usr/bin/env python3
"""Small watchdog CLI for scheduled loop-harness ticks."""

from __future__ import annotations

import argparse
import json
import plistlib
import shlex
import subprocess
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_ARTIFACT_DIR = ".loop-harness"
DEFAULT_LABEL = "local.loop-harness"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def artifact_root(repo: Path) -> Path:
    return repo / DEFAULT_ARTIFACT_DIR


def schedule_dir(repo: Path) -> Path:
    return artifact_root(repo) / "schedules"


def paths(repo: Path, label: str) -> dict[str, Path]:
    root = artifact_root(repo)
    schedules = schedule_dir(repo)
    watchdog = root / "watchdog"
    return {
        "root": root,
        "schedules": schedules,
        "watchdog": watchdog,
        "config": watchdog / "config.json",
        "status": watchdog / "status.json",
        "paused": watchdog / "paused",
        "lock": watchdog / "run.lock",
        "out": schedules / f"{label}.out.log",
        "err": schedules / f"{label}.err.log",
        "plist": schedules / f"{label}.plist",
        "cron": schedules / f"{label}.cron",
    }


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def cadence_to_start_interval(cadence: str) -> int:
    table = {"hourly": 3600, "daily": 86400, "weekly": 604800}
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


def load_config(repo: Path, label: str = DEFAULT_LABEL) -> dict:
    config_path = paths(repo, label)["config"]
    if not config_path.exists():
        raise SystemExit(f"missing config: {config_path}")
    return read_json(config_path)


def write_status(repo: Path, label: str, data: dict) -> None:
    status = {
        "label": label,
        "repo": str(repo),
        "updated_at": utc_now(),
    }
    status.update(data)
    write_json(paths(repo, label)["status"], status)


def scheduler_command_parts(repo: Path, label: str) -> list[str]:
    skill_dir = Path(__file__).resolve().parents[1]
    return [
        "python3",
        str(skill_dir / "scripts" / "watchdog.py"),
        "tick",
        "--repo",
        str(repo),
        "--label",
        label,
    ]


def scheduler_command(repo: Path, label: str) -> str:
    return " ".join(shlex.quote(part) for part in scheduler_command_parts(repo, label))


def write_schedule(repo: Path, label: str, kind: str, cadence: str, command: str) -> Path:
    all_paths = paths(repo, label)
    all_paths["schedules"].mkdir(parents=True, exist_ok=True)
    if kind == "launchd":
        path = all_paths["plist"]
        data = {
            "Label": label,
            "WorkingDirectory": str(repo),
            "ProgramArguments": scheduler_command_parts(repo, label),
            "StartInterval": cadence_to_start_interval(cadence),
            "StandardOutPath": str(all_paths["out"]),
            "StandardErrorPath": str(all_paths["err"]),
        }
        with path.open("wb") as handle:
            plistlib.dump(data, handle)
        return path
    path = all_paths["cron"]
    path.write_text(f"{cadence_to_cron(cadence)} cd {shlex.quote(str(repo))} && {command}\n", encoding="utf-8")
    return path


def command_setup(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    all_paths = paths(repo, args.label)
    all_paths["root"].mkdir(parents=True, exist_ok=True)
    all_paths["schedules"].mkdir(parents=True, exist_ok=True)
    all_paths["watchdog"].mkdir(parents=True, exist_ok=True)
    tick_command = scheduler_command(repo, args.label)
    schedule_path = write_schedule(repo, args.label, args.kind, args.cadence, tick_command)
    config = {
        "label": args.label,
        "repo": str(repo),
        "command": args.command,
        "mode": args.mode,
        "cadence": args.cadence,
        "kind": args.kind,
        "schedule_path": str(schedule_path),
        "tick_command": tick_command,
        "created_at": utc_now(),
    }
    write_json(all_paths["config"], config)
    print(f"wrote config: {all_paths['config']}")
    print(f"wrote schedule: {schedule_path}")
    return 0


def criteria_locked(repo: Path) -> bool:
    criteria = artifact_root(repo) / "criteria" / "current.md"
    if not criteria.exists():
        return False
    return "Contract status: locked" in criteria.read_text(encoding="utf-8")


def command_tick(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    label = args.label
    all_paths = paths(repo, label)
    config = load_config(repo, label)
    mode = "run-until-done" if args.run_until_done else config.get("mode", "report-only")

    if all_paths["paused"].exists():
        write_status(repo, label, {"state": "skipped", "decision": "skipped_paused", "reason": "paused"})
        print(f"{label}: skipped, paused")
        return 0
    if all_paths["lock"].exists():
        write_status(repo, label, {"state": "skipped", "decision": "skipped_overlap", "reason": "lock_exists"})
        print(f"{label}: skipped overlap, lock exists")
        return 0
    if mode == "run-until-done" and not criteria_locked(repo):
        write_status(
            repo,
            label,
            {"state": "blocked", "decision": "blocked_unlocked_criteria", "reason": "criteria_not_locked"},
        )
        print(f"{label}: refused, criteria/current.md is not locked")
        return 2

    all_paths["lock"].write_text(f"{utc_now()}\n", encoding="utf-8")
    started_at = utc_now()
    try:
        result = subprocess.run(
            config["command"],
            cwd=repo,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.stdout:
            with all_paths["out"].open("a", encoding="utf-8") as handle:
                handle.write(result.stdout)
        if result.stderr:
            with all_paths["err"].open("a", encoding="utf-8") as handle:
                handle.write(result.stderr)
        write_status(
            repo,
            label,
            {
                "state": "ran",
                "decision": "ran",
                "started_at": started_at,
                "finished_at": utc_now(),
                "returncode": result.returncode,
                "command": config["command"],
                "mode": mode,
            },
        )
        print(f"{label}: ran, returncode={result.returncode}")
        return result.returncode
    finally:
        all_paths["lock"].unlink(missing_ok=True)


def command_status(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    label = args.label
    all_paths = paths(repo, label)
    config = read_json(all_paths["config"]) if all_paths["config"].exists() else {}
    status = read_json(all_paths["status"]) if all_paths["status"].exists() else {}
    print(f"label: {label}")
    print(f"repo: {repo}")
    print(f"configured: {'yes' if config else 'no'}")
    if config:
        print(f"mode: {config.get('mode', 'report-only')}")
        print(f"cadence: {config.get('cadence', 'unknown')}")
        print(f"kind: {config.get('kind', 'unknown')}")
        print(f"command: {config.get('command', '')}")
        print(f"schedule: {config.get('schedule_path', '')}")
    print(f"paused: {'yes' if all_paths['paused'].exists() else 'no'}")
    print(f"locked: {'yes' if all_paths['lock'].exists() else 'no'}")
    if status:
        if status.get("decision"):
            print(f"decision: {status['decision']}")
        print(f"last state: {status.get('state', 'unknown')}")
        if status.get("last_tick"):
            print(f"last tick: {status['last_tick']}")
        print(f"last updated: {status.get('updated_at', 'unknown')}")
        if status.get("detail"):
            print(f"detail: {status['detail']}")
        if "returncode" in status:
            print(f"last returncode: {status['returncode']}")
        if status.get("reason"):
            print(f"reason: {status['reason']}")
    else:
        print("last state: never run")
    return 0


def command_pause(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    paused = paths(repo, args.label)["paused"]
    paused.parent.mkdir(parents=True, exist_ok=True)
    paused.write_text(f"{utc_now()}\n", encoding="utf-8")
    print(f"{args.label}: paused")
    return 0


def command_resume(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    paths(repo, args.label)["paused"].unlink(missing_ok=True)
    print(f"{args.label}: resumed")
    return 0


def tail_text(path: Path, lines: int) -> str:
    if not path.exists():
        return "(missing)\n"
    content = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return "\n".join(content[-lines:]) + ("\n" if content else "")


def command_tail(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    all_paths = paths(repo, args.label)
    print(f"==> {all_paths['out']} <==")
    print(tail_text(all_paths["out"], args.lines), end="")
    print(f"==> {all_paths['err']} <==")
    print(tail_text(all_paths["err"], args.lines), end="")
    return 0


def command_uninstall(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    config_path = paths(repo, args.label)["config"]
    label = args.label
    if config_path.exists():
        label = read_json(config_path).get("label", label)
    all_paths = paths(repo, label)
    for key in ("config", "status", "plist", "cron", "paused", "lock"):
        all_paths[key].unlink(missing_ok=True)
    print(f"{args.label}: uninstalled")
    return 0


def add_repo_label(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo", required=True)
    parser.add_argument("--label", default=DEFAULT_LABEL)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command_name", required=True)

    setup = subparsers.add_parser("setup")
    add_repo_label(setup)
    setup.add_argument("--command", required=True)
    setup.add_argument("--mode", choices=["report-only", "run-until-done"], default="report-only")
    setup.add_argument("--cadence", default="daily")
    setup.add_argument("--kind", choices=["launchd", "cron"], default="launchd")
    setup.set_defaults(func=command_setup)

    tick = subparsers.add_parser("tick")
    add_repo_label(tick)
    tick.add_argument("--run-until-done", action="store_true")
    tick.set_defaults(func=command_tick)

    status = subparsers.add_parser("status")
    add_repo_label(status)
    status.set_defaults(func=command_status)

    pause = subparsers.add_parser("pause")
    add_repo_label(pause)
    pause.set_defaults(func=command_pause)

    resume = subparsers.add_parser("resume")
    add_repo_label(resume)
    resume.set_defaults(func=command_resume)

    tail = subparsers.add_parser("tail")
    add_repo_label(tail)
    tail.add_argument("--lines", type=int, default=40)
    tail.set_defaults(func=command_tail)

    uninstall = subparsers.add_parser("uninstall")
    add_repo_label(uninstall)
    uninstall.set_defaults(func=command_uninstall)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
