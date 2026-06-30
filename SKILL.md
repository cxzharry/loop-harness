---
name: loop-harness
description: Autonomous product optimization loop harness for improving live products, prototypes, docs, and engineering quality over repeated runs. Use when Codex should discover product improvement opportunities, prioritize them, form hypotheses, hand off bounded interventions, verify evidence, persist learnings, and decide whether to schedule the next loop across UX, growth metrics, engineering quality, content/docs, or release readiness.
---

# Loop Harness

Use this skill to run controlled product optimization loops. A loop must improve a product with evidence, not generate generic recommendations.

## Core Rule

Every run follows exactly five phases:

1. Discovery
2. Handoff
3. Verification
4. Persistence
5. Scheduling

Do not skip a phase. If a phase lacks evidence, record the gap and route the run to instrumentation, human handoff, or report-only mode.

## Start Of Run

1. Identify the product surface: app, route, prototype, docs, repo, release, or metric area.
2. Load existing loop artifacts if present:
   - `PRODUCT_LOOP.md`
   - `PRODUCT_LOOP_STATE.md`
   - `product-loop-run-log.md`
   - `product-loop-budget.md`
3. If artifacts are missing and the user wants an ongoing loop, scaffold from `assets/templates/`.
4. Select one or more optimization profiles. See `references/profiles.md`.
5. Select a product loop pattern when cadence or recurring scope matters. See `references/patterns.md` and `assets/templates/product-loop-patterns.json`.
6. Run `scripts/product_loop_audit.py <repo-or-folder>` when artifacts exist or after scaffolding.
7. Run `scripts/product_loop_cost.py --pattern <pattern-id> --level L1|L2|L3 --cadence <interval>` before scheduling recurring loops.

## Phase 1: Discovery

Find real signals before proposing work.

Allowed signal sources:
- UX/browser inspection, screenshots, user flows, accessibility checks.
- Product metrics, funnel data, analytics, event logs, user feedback.
- Bugs, CI failures, errors, performance traces, release smoke results.
- Docs, onboarding, support requests, PRD/prototype mismatches.
- Existing `PRODUCT_LOOP_STATE.md` watchlist, failed attempts, and human decisions.

Rules:
- Prefer real data. If data is missing, propose instrumentation or a report-only discovery pass.
- Separate signal from interpretation.
- Record noise and ignored items so the next run does not rediscover them.

Output:
```markdown
### Discovery
- Signals inspected:
- New findings:
- Existing state changes:
- Noise ignored:
- Data gaps:
```

## Phase 2: Handoff

Convert findings into one bounded intervention.

For each candidate, score:
- Impact: expected product/user/business value.
- Confidence: evidence strength.
- Effort: implementation and verification cost.
- Risk: potential harm, ambiguity, reversibility.

Choose at most one primary intervention per loop unless the user explicitly asks for batch work. Write a hypothesis:

```markdown
If we change <surface/intervention>, then <target user/product outcome> should improve because <evidence>.
Success evidence: <metric/check/rubric>.
Rollback/escalation: <condition>.
```

Handoff must define owner boundary, files/surfaces, denylisted areas, acceptance evidence, and whether the loop is report-only, assisted, or actioning.

Human approval is required for pricing, payments, auth, permissions, secrets, destructive migrations, irreversible data changes, legal/compliance, brand-sensitive copy, or major product direction.

## Phase 3: Verification

Verify the intervention independently from the implementation story.

Use profile-specific verification from `references/verification.md`. Typical checks:
- Browser smoke, screenshots, visual comparison, accessibility.
- Tests, lint, typecheck, build, CI, performance.
- Metric query, event validation, funnel sanity check.
- Content clarity review, link validation, PRD/prototype alignment.

Rules:
- The implementer cannot mark its own work done without evidence.
- If verification cannot run, mark `ESCALATE_HUMAN` or `NEEDS_INSTRUMENTATION`.
- Do not accept screenshots, test claims, or metric claims without source details.

Verdicts:
- `PASS`: evidence supports the hypothesis or the bounded acceptance criteria.
- `PARTIAL`: improvement exists but follow-up is needed.
- `FAIL`: evidence rejects the change or risk is too high.
- `UNKNOWN`: required evidence is missing.

## Phase 4: Persistence

Write durable state outside the conversation.

Update:
- `PRODUCT_LOOP_STATE.md`: current opportunities, selected intervention, status, failed attempts, human decisions, next action.
- `product-loop-run-log.md`: append-only run summary with timestamp, profile, signals, action, verification, verdict, next schedule decision.

Persist failed hypotheses and what not to retry. Preserve useful learnings even when no code/docs change was made.

## Phase 5: Scheduling

Decide the next loop action:
- `stop_success`: goal met or no valuable next action.
- `run_again_now`: cheap high-confidence follow-up exists.
- `schedule`: cadence is useful and budget allows it.
- `pause`: missing data, budget, reviewer, or unsafe context.
- `escalate`: human decision required.

Use `product-loop-budget.md` for max runs, max changes, max subagents, daily token cap, and kill switch. High-frequency loops need early exit when no actionable signal exists.

## Output Format

End each run with:

```markdown
## Loop Harness Report

### Profile
<profiles used>

### Discovery
<signals and findings>

### Handoff
<chosen intervention, hypothesis, scope, risk gate>

### Verification
<commands/checks/data sources, verdict>

### Persistence
<files updated or reason not updated>

### Scheduling
<next action and rationale>
```

## References

- Read `references/profiles.md` when selecting optimization profiles.
- Read `references/patterns.md` when choosing a reusable product loop pattern.
- Read `references/scoring.md` when ranking candidates or judging readiness.
- Read `references/verification.md` before accepting an intervention.
- Read `references/state-schema.md` before creating or updating loop artifacts.
- Read `references/failure-modes.md` when a loop stalls, repeats, or becomes unsafe.

## Validation

After creating or changing loop artifacts, run:

```bash
python3 <skill-dir>/scripts/product_loop_audit.py <product-repo-or-folder>
python3 <skill-dir>/scripts/product_loop_cost.py --pattern daily-product-triage --level L1 --cadence 1d
```

For skill package validation, run:

```bash
python3 /Users/haido/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>
```
