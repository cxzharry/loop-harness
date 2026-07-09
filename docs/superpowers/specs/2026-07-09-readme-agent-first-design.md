# README Agent-First Design

Date: 2026-07-09
Status: approved for planning review

## Goal

Rewrite the public `README.md` for humans who know how to use AI agents and
vibe code, but do not want a command reference. The README should explain why
`$loop-harness` exists, what outcomes it creates, and how a human should ask an
agent to use it.

## Audience

- Human users who work through AI agents.
- Vibe coders who iterate quickly and need guardrails against lost context,
  unclear success criteria, and repeated regressions.
- Readers who need to understand the skill before reading scripts or internal
  references.

## Positioning

Use platform-neutral wording. Do not describe the project as a Codex-specific or
Claude-specific skill. Preferred terms:

- `agent skill`
- `skill`
- `AI agent`
- `$loop-harness`

Core message:

`$loop-harness` standardizes agent-driven improvement loops so vibe-coded work
can be evaluated, repeated, persisted, and protected from regression.

## README Structure

1. `# loop-harness`
   - One short value proposition.
   - Explain the problem: agent work can lose context, skip benchmarks, or
     repeat old failures.
   - Explain the answer: define metrics/criteria/benchmarks, verify with
     evidence, persist state, and promote durable failures into regression
     protection.

2. `## Install`
   - Keep install short.
   - Say: install this repository into your agent's skills directory as
     `$loop-harness`.
   - Include one optional command:

     ```bash
     git clone https://github.com/cxzharry/loop-harness <your-skills-dir>/loop-harness
     ```

   - Do not hard-code a vendor-specific skills path in the README body.

3. `## Basic Usage`
   - Do not use long command blocks.
   - Use short bullet examples for prompts:
     - first-time loop with metrics/criteria/benchmark definition;
     - report-only evaluation without file changes;
     - continuing an existing loop from `.loop-harness/`;
     - recurring monitoring or scheduler artifact setup.

4. `## What It Supports`
   - List capabilities from the user's point of view:
     - define metrics, criteria, benchmark seeds, acceptance thresholds, and
       non-goals;
     - bootstrap first run state;
     - continue later runs from logs and active benchmarks;
     - promote failures into regression cases;
     - use Playwright when product UI verification is needed;
     - split independent lanes for parallel agents;
     - keep benchmark history scalable;
     - prepare repo-local scheduler artifacts when requested.

5. `## First Run`
   - Explain that the first run creates `.loop-harness/` in the target repo.
   - Explain expected first-run outcomes:
     - product loop summary;
     - criteria/current evaluation contract;
     - benchmark seeds or active regression cases;
     - run log entry;
     - state file.
   - Make clear that if metric/target/benchmark/Playwright flow/human gate is
     unclear, the agent should stop at report-only or evaluation-contract work.

6. `## Later Runs`
   - Explain that later runs must read `.loop-harness/` first.
   - Explain expected behavior:
     - load active benchmark cases;
     - run matching benchmarks before accepting changes;
     - avoid repeated attempts from prior logs;
     - update state, benchmark, and run log;
     - stop on success, regression, plateau, budget, environment blocker, or
       human gate.

7. `## Runtime Files`
   - Explain that runtime files live in the target repo under `.loop-harness/`.
   - Show a compact tree if useful.
   - Mention that `self/loop-runs/` is local-only and ignored.

8. `## Scheduling Outcome`
   - Explain the outcome, not command syntax.
   - Scheduled runs use persisted `.loop-harness/` state and avoid overlapping
     ticks.
   - Do not claim the skill automatically installs operating-system scheduler
     jobs.

9. `## Public Package`
   - Explain that the public repo contains reusable skill resources, scripts,
     templates, references, and fixtures only.
   - Product runtime logs, screenshots, scheduler status, and local self-run
     evidence must stay in target repos or ignored local files.

## Content Rules

- Do not mention Codex or Claude in README positioning.
- Do not include a `Watchdog` command reference section.
- Do not include a `Validation` command reference section.
- Avoid long code blocks that cause horizontal scrolling.
- Use outcome-first language.
- Keep examples in normal Markdown bullets where possible so GitHub wraps them.
- Keep the README concise enough for a human to skim before asking an agent to
  use the skill.

## Acceptance Checks

- `README.md` uses platform-neutral wording.
- Install section has one optional manual command with `<your-skills-dir>`.
- Basic usage includes first run, report-only, later run, and scheduled run
  prompt examples.
- README explains metrics/criteria/benchmark definition before actioning.
- README explains first-run and later-run behavior clearly.
- README explains expected outcomes, not just internal headings.
- README does not expose long watchdog or validation command blocks.
- Existing public-hygiene regression still passes after the README update.

