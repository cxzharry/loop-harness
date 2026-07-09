# loop-harness

`loop-harness` is an agent skill for standardizing evidence-backed improvement
loops.

It is designed for humans who use AI agents and vibe code quickly, but still
need clear metrics, benchmarks, run history, and regression protection. Instead
of asking an agent to "make it better" once, `$loop-harness` makes the agent
define what better means, verify the result, persist the evidence, and carry
that context into the next run.

## Install

Install this repository into your agent's skills directory as `$loop-harness`.

Manual install:

```bash
git clone https://github.com/cxzharry/loop-harness <your-skills-dir>/loop-harness
```

Then mention `$loop-harness` when you ask an agent to improve a repo, product
surface, document set, release checklist, metric funnel, or UX flow.

## Basic Usage

Use `$loop-harness` when you want an agent to keep improving something until the
evidence says it should stop.

Example prompts:

- Use `$loop-harness` to improve this onboarding flow. Define the metric,
  criteria, and benchmark with me first, then run until the benchmark passes.
- Use `$loop-harness` to evaluate this docs set in report-only mode. Create the
  criteria and benchmark seeds, but do not change files yet.
- Use `$loop-harness` to continue the existing loop in this repo. Read the prior
  `.loop-harness/` logs first and avoid regressing active benchmark cases.
- Use `$loop-harness` to prepare a recurring check for this repo. Keep the run
  state local to the repo and make sure ticks cannot overlap.

## What It Supports

`loop-harness` helps an agent:

- Define metrics, criteria, acceptance thresholds, benchmark seeds, and
  non-goals before actioning.
- Bootstrap a first run when the repo has no loop history yet.
- Continue later runs from prior state, run logs, active benchmarks, and failed
  attempts.
- Promote real failures into benchmark cases so later runs do not repeat or
  regress them.
- Use Playwright when the target is an app, route, prototype, or browser-visible
  product flow.
- Split independent work into bounded lanes for parallel agents while keeping
  final verification integrated.
- Keep benchmark history scalable with compact indexes plus active and archived
  case files.
- Prepare repo-local scheduler artifacts for recurring checks when requested.

## First Run

On the first run in a repo, the agent should create a `.loop-harness/` workspace
inside that repo. That folder becomes the durable memory for the loop.

The first run usually produces:

- A product loop summary with the target surface, intent, profile, risk gates,
  and verification plan.
- An evaluation contract under `.loop-harness/criteria/current.md`.
- Initial benchmark seeds or active regression cases.
- A run log entry with raw evidence, findings, and benchmark-promotion
  decisions.
- A state file that records what to continue, avoid, or ask next.

If the metric, target, benchmark seed, Playwright flow, or human gate is unclear,
the agent should stop at report-only or evaluation-contract work instead of
making product changes.

## Later Runs

Later runs should start by reading the existing `.loop-harness/` folder.

That lets the agent:

- Load prior failures and active benchmark cases before choosing new work.
- Run matching benchmarks before accepting a change.
- Avoid repeated failed attempts from previous logs.
- Update state, benchmark cases, and run logs after each iteration.
- Stop on success, regression, plateau, budget, environment blocker, or human
  gate.

The expected outcome is a repo that gets safer over time: meaningful failures
become evidence, and durable failures become regression protection.

## Runtime Files

Runtime files belong in the target repository, not in this skill package.

Typical target-repo layout:

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
  runs/archive/
  schedules/
```

`self/loop-runs/` is intentionally ignored in this repository. It may exist
locally for self-development evidence, but it should not be committed or
published.

## Scheduling Outcome

When recurring monitoring is requested, `$loop-harness` can prepare repo-local
scheduler artifacts under `.loop-harness/schedules/`.

It does not automatically install operating-system scheduler jobs. The important
outcome is that scheduled runs are resumable and non-overlapping: each tick
starts fresh, reads saved `.loop-harness/` state, respects locked criteria,
writes logs, and exits if another tick is already running.

## Public Package

This public repo contains reusable skill resources, scripts, templates,
references, and benchmark fixtures.

Product-specific runtime logs, screenshots, scheduler status, and local self-run
evidence should stay in each target repo's `.loop-harness/` folder or in ignored
local files.
