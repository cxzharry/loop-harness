---
name: loop-harness
description: Autonomous product optimization loop harness for improving live products, prototypes, docs, and engineering quality over repeated runs. Use when Codex should discover product improvement opportunities, prioritize them, form hypotheses, hand off bounded interventions, verify evidence, persist learnings, and decide whether to schedule the next loop across UX, growth metrics, engineering quality, content/docs, or release readiness.
---

# Loop Harness

Run controlled product optimization loops with evidence. Use this skill to improve a product, prototype, doc set, release, or engineering-quality surface through repeated Discovery -> Handoff -> Verification -> Persistence -> Scheduling iterations.

## Non-Negotiables

- Execute all five phases every iteration: Discovery, Handoff, Verification, Persistence, Scheduling.
- Prefer real product signals over generic recommendations.
- There is no `action-once` mode. Any actioning work uses `run-until-done` and stops only on a recorded stop condition.
- If an app, route, local dev server, deployed page, or prototype must be verified, use Playwright. Static inspection alone cannot produce `PASS`.
- UX/UI visual-quality work needs Playwright plus `design-taste-frontend` and `design-slop-ban` checks when the surface can be opened.
- Failed, regressed, partial-defect, ENV, or UNKNOWN iterations must append raw evidence plus a structured finding to `product-loop-run-log.md`, then promote durable failures into `PRODUCT_LOOP_BENCHMARK.md`.
- Do not create separate `error-log.md`, `findings.md`, or `run-log-error.md`.
- Run matching active benchmark cases before accepting new optimization.
- Persist state before scheduling the next iteration.
- In target repos, store persistent loop artifacts under `.loop-harness/` by default; do not scatter them across the repo root.

## First Load

Read `references/operation.md` before running a loop. Then load only the relevant references below:

- `references/profiles.md`: choose `ux-product`, `metrics-growth`, `engineering-quality`, `content-docs`, or `release-readiness`.
- `references/patterns.md`: choose a reusable cadence/scope pattern.
- `references/scoring.md`: rank candidates, readiness, verdicts, and run-until-done criteria.
- `references/verification.md`: verify interventions, Playwright/browser evidence, UX taste/slop gates, benchmark gates, and parallel-agent integration.
- `references/state-schema.md`: create or update loop artifacts, finding schema, benchmark regression cases, handoff files, and worktree maps.
- `references/global-knowledge.md`: load local global criteria/seeds and gate reusable finding promotion.
- `references/failure-modes.md`: diagnose stalled, unsafe, generic, or repeating loops.

## Start Checklist

1. State the detected intent and product surface in one line.
2. Use `.loop-harness/` as the loop artifact root unless the user explicitly selects another folder.
3. Load existing artifacts if present: `.loop-harness/PRODUCT_LOOP.md`, `.loop-harness/PRODUCT_LOOP_STATE.md`, `.loop-harness/product-loop-run-log.md`, `.loop-harness/PRODUCT_LOOP_BENCHMARK.md`, and `.loop-harness/product-loop-budget.md`.
4. Scaffold missing ongoing-loop artifacts into `.loop-harness/` from `assets/templates/` when needed.

```bash
python3 <skill-dir>/scripts/init_loop.py <product-repo-root>
```

5. Select profile(s), pattern, execution mode, target, safety budget, plateau patience, stop conditions, and human gates.
6. Select matching active benchmark cases before actioning:

```bash
python3 <skill-dir>/scripts/select_benchmarks.py --repo <repo> --profile <profile> --intent <intent> --surface <surface> --include-skill --require
```

7. Select matching local global knowledge when useful:

```bash
python3 <skill-dir>/scripts/select_knowledge.py --repo <repo> --profile <profile> --intent <intent> --surface <surface>
```

8. Ask the user only for unresolved metric, target, surface, human-gate, or schedule decisions that cannot be safely inferred.
9. Run artifact audit after scaffold/artifact changes:

```bash
python3 <skill-dir>/scripts/product_loop_audit.py <product-repo-root-or-.loop-harness> --min-level L2
```

Use `--min-level L3` for scheduled/unattended loops. Use `--strict` for CI or release gates. Hard misses such as negated evidence or missing promoted active regression cases must exit non-zero.

## Execution Modes

- `report-only`: discover, verify signals, persist state, and stop without source changes.
- `run-until-done`: repeat the full five-phase loop until success, regression, budget, plateau, human gate, environment blocker, or unknown-data stop condition.
- `scheduled`: run on cadence; each tick may be report-only or run-until-done within budget.

Before actioning, confirm or infer:
- measurable target or locked acceptance rubric;
- `target_min`;
- safety budget or kill switch;
- plateau patience;
- stop conditions;
- human gates.

For command-backed unattended loops, use the controller instead of a one-shot command:

```bash
python3 <skill-dir>/scripts/run_loop_controller.py --repo <repo> --benchmark-command "<benchmark-cmd>" --command "<action-or-verification-cmd>" --target-score <score>
```

## Parallel Work

Use a single agent unless domains are independent. If using parallel agents, record tasks in `.loop-harness/AGENT_HANDOFF.md` or `.loop-harness/agent-tasks/`, isolate file-changing work in worktrees when possible, write `.loop-harness/worktree-map.md`, review conflicts, and verify integrated work in the coordinator workspace before any `PASS`.

## Verification Gates

Always verify independently from the implementation story:
- Run matching active benchmark cases first.
- Run profile-specific tests, build, lint, metric, doc, browser, or Playwright checks.
- For metric loops, use an objective source when available:

```bash
python3 <skill-dir>/scripts/metrics_adapter.py --source <json-csv-or-text> --metric <name> --target <number> --direction increase
```

- For browser-visible product work, record URL, viewport, flow steps, assertions, errors, and screenshots/traces when useful.
- Use `assets/templates/playwright-loop-smoke.spec.ts` as the reusable Playwright smoke template when the repo has no stronger browser test.
- For visual-quality work, record taste/slop score `>=8/10` and no critical slop violation, or record why the full taste rubric is not applicable and what equivalent checks were used.
- If verification cannot run, use `UNKNOWN`, `ENV`, `ESCALATE_HUMAN`, or `NEEDS_INSTRUMENTATION`; do not mark `PASS`.

## Persistence Contract

After every iteration:
- Append one run-log entry with `Raw Run Result`, `Finding`, and `Benchmark Promotion` blocks.
- Promote durable state to `.loop-harness/PRODUCT_LOOP_STATE.md`.
- Promote reusable checks or failures to `.loop-harness/PRODUCT_LOOP_BENCHMARK.md`.
- Update `.loop-harness/AGENT_HANDOFF.md`, `.loop-harness/agent-tasks/`, and `.loop-harness/worktree-map.md` when agents/worktrees are used.
- Record failed hypotheses and what not to retry.
- If a finding may be reusable beyond the repo, gate it through `scripts/promote_global_knowledge.py`; do not write runtime learning into the skill package.
- Validate the latest run-log entry before claiming persistence is complete:

```bash
python3 <skill-dir>/scripts/validate_run_log_entry.py <repo>/.loop-harness/product-loop-run-log.md
```

## Scheduling

End each iteration with one next action:
- `stop_success`
- `run_again_now`
- `schedule`
- `pause`
- `escalate`

Use `.loop-harness/product-loop-budget.md` for max runs, max changes, subagent/tool-heavy check caps, token/time budget, and kill switch.

When scheduling is requested, generate the local scheduler artifact under `.loop-harness/schedules/`:

```bash
python3 <skill-dir>/scripts/install_scheduler.py --repo <repo> --command "<loop command>" --cadence daily --kind launchd
```

## Output Shape

End each run with a concise Loop Harness Report:

- Intent
- Profile
- Discovery
- Handoff
- Verification
- Persistence
- Scheduling
- Iteration State

Include run-log timestamp, state fields promoted, error classification, matched benchmark cases, benchmark verdict, created/updated regression case id, handoff/worktree updates, and evidence retained for future regression checks.

## Validation

After changing loop artifacts or this skill, run the relevant gates:

```bash
python3 <skill-dir>/scripts/product_loop_audit.py <product-repo-root-or-.loop-harness> --min-level L2
python3 <skill-dir>/scripts/product_loop_cost.py --pattern daily-product-triage --level L1 --cadence 1d
python3 <skill-dir>/scripts/select_benchmarks.py --repo <product-repo-root> --profile ux-product --intent UX_OPTIMIZE --surface web-route --include-skill
python3 <skill-dir>/scripts/select_knowledge.py --repo <product-repo-root> --profile ux-product --intent UX_OPTIMIZE --surface web-route
python3 <skill-dir>/benchmark/run_pressure_eval.py --transcripts <skill-dir>/benchmark/fixtures/pass
python3 /Users/haido/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>
```

For loop-harness self-development, source and installed skill should both pass:

```bash
python3 scripts/product_loop_audit.py self/loop-runs --min-level L3
python3 scripts/product_loop_audit.py assets/templates --min-level L2
```
