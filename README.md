# loop-harness

Codex skill for running evidence-backed optimization loops on products, prototypes, docs, release checklists, metric funnels, UX flows, and engineering-quality surfaces.

The loop structure is:

1. Discovery
2. Handoff
3. Verification
4. Persistence
5. Scheduling

The skill is designed for repeated, stateful work. It records the evidence, decisions, run logs, benchmarks, and scheduler artifacts needed to continue safely across later runs.

## Install

Install the skill into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R loop-harness ~/.codex/skills/loop-harness
```

The expected installed path is usually:

```text
~/.codex/skills/loop-harness
```

## Basic Usage

Example prompts:

```text
Use $loop-harness to improve this onboarding flow until the Playwright smoke passes.
```

```text
Use $loop-harness to run a report-only loop on this docs set and persist findings under .loop-harness/.
```

```text
Use $loop-harness to set up a scheduled loop artifact for this repo with a daily cadence and manual tick support.
```

The skill will normally scaffold repo-local runtime files before actioning:

```bash
python3 ~/.codex/skills/loop-harness/scripts/init_loop.py <target-repo>
```

## Runtime Artifacts

Runtime state belongs in the target repository under `.loop-harness/`. Do not write run state back into the skill package.

Typical artifact layout:

```text
.loop-harness/
  PRODUCT_LOOP.md
  PRODUCT_LOOP_STATE.md
  PRODUCT_LOOP_BENCHMARK.md
  AGENT_HANDOFF.md
  product-loop-budget.md
  product-loop-run-log.md
  worktree-map.md
  criteria/current.md
  agent-tasks/
  benchmarks/active/
  benchmarks/archive/
  runs/
  runs/archive/
  schedules/
```

Use `.loop-harness/criteria/current.md` to lock the evaluation contract before actioning. Use `product-loop-run-log.md` for raw run results, findings, and benchmark-promotion notes after each iteration.

## Watchdog

`scripts/watchdog.py` manages repo-local scheduler artifacts and manual ticks. It writes configuration, schedule files, status, logs, and locks under the target repo's `.loop-harness/` tree.

It does not automatically install operating-system scheduler jobs. The `setup` command generates artifacts such as launchd plist or cron text files that can be reviewed and installed separately if desired.

Common commands:

```bash
python3 ~/.codex/skills/loop-harness/scripts/watchdog.py setup --repo <target-repo> --command "<loop command>" --cadence daily
python3 ~/.codex/skills/loop-harness/scripts/watchdog.py status --repo <target-repo>
python3 ~/.codex/skills/loop-harness/scripts/watchdog.py pause --repo <target-repo>
python3 ~/.codex/skills/loop-harness/scripts/watchdog.py resume --repo <target-repo>
python3 ~/.codex/skills/loop-harness/scripts/watchdog.py tail --repo <target-repo>
python3 ~/.codex/skills/loop-harness/scripts/watchdog.py tick --repo <target-repo>
python3 ~/.codex/skills/loop-harness/scripts/watchdog.py uninstall --repo <target-repo>
```

For `run-until-done` ticks, the watchdog requires `.loop-harness/criteria/current.md` to contain a locked contract. Lock files prevent overlapping ticks.

## Validation

Useful validation commands for this repo:

```bash
python3 benchmark/test_tooling_regressions.py
python3 benchmark/run_pressure_eval.py --transcripts benchmark/fixtures/pass
python3 scripts/product_loop_audit.py assets/templates --min-level L2
python3 -m py_compile scripts/*.py benchmark/*.py
```

`self/loop-runs/` is intentionally ignored. It can hold local self-development run artifacts, but it should not be committed or published.

For target repositories, validate generated loop artifacts with:

```bash
python3 ~/.codex/skills/loop-harness/scripts/product_loop_audit.py <target-repo>/.loop-harness --min-level L2
python3 ~/.codex/skills/loop-harness/scripts/validate_run_log_entry.py <target-repo>/.loop-harness/product-loop-run-log.md
```

## Public Safety

This repository should contain the reusable skill, scripts, templates, and documentation only. Product-specific runtime artifacts, run logs, scheduler status, screenshots, and local evidence should live in each target repository under `.loop-harness/` and should be reviewed before publishing.
