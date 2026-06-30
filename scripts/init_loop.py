#!/usr/bin/env python3
"""Scaffold repo-local loop-harness artifacts."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_DIR = SKILL_DIR / "assets" / "templates"
DEFAULT_ARTIFACT_DIR = ".loop-harness"

TEMPLATE_FILES = {
    "PRODUCT_LOOP.md": "PRODUCT_LOOP.md",
    "PRODUCT_LOOP_STATE.md": "PRODUCT_LOOP_STATE.md",
    "PRODUCT_LOOP_BENCHMARK.md": "PRODUCT_LOOP_BENCHMARK.md",
    "product-loop-budget.md": "product-loop-budget.md",
    "AGENT_HANDOFF.md": "AGENT_HANDOFF.md",
    "worktree-map.md": "worktree-map.md",
    "product-loop-run-log.template.md": "product-loop-run-log.md",
}


def copy_template(src: Path, dst: Path, force: bool) -> str:
    if dst.exists() and not force:
        return "kept"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return "created" if not dst.exists() else "updated"


def scaffold(repo: Path, artifact_dir: str, force: bool) -> dict[str, str]:
    root = repo.resolve()
    target = root / artifact_dir
    target.mkdir(parents=True, exist_ok=True)
    (target / "agent-tasks").mkdir(exist_ok=True)
    (target / "schedules").mkdir(exist_ok=True)

    results: dict[str, str] = {}
    for src_name, dst_name in TEMPLATE_FILES.items():
        src = TEMPLATE_DIR / src_name
        dst = target / dst_name
        existed = dst.exists()
        if existed and not force:
            results[dst_name] = "kept"
            continue
        shutil.copyfile(src, dst)
        results[dst_name] = "updated" if existed else "created"
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", help="Product repo root to scaffold.")
    parser.add_argument("--artifact-dir", default=DEFAULT_ARTIFACT_DIR)
    parser.add_argument("--force", action="store_true", help="Overwrite existing artifacts.")
    args = parser.parse_args()

    repo = Path(args.repo)
    if not repo.exists():
        parser.error(f"repo does not exist: {repo}")
    if not repo.is_dir():
        parser.error(f"repo is not a directory: {repo}")

    results = scaffold(repo, args.artifact_dir, args.force)
    print(f"Loop harness artifacts: {repo.resolve() / args.artifact_dir}")
    for name, status in sorted(results.items()):
        print(f"{status}: {name}")
    print("created: agent-tasks/")
    print("created: schedules/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
