# README Agent-First Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite `README.md` as a platform-neutral, agent-first guide for humans who use AI agents and vibe code.

**Architecture:** Keep this as a documentation-only change with one regression-test update. The README becomes the human-facing entrypoint; `SKILL.md`, `references/`, scripts, and templates remain the technical contract.

**Tech Stack:** Markdown, Python `unittest`, existing `benchmark/test_tooling_regressions.py`, existing GitHub public repo.

---

## File Structure

- Modify `README.md`: replace the current README with an outcome-first, platform-neutral README.
- Modify `benchmark/test_tooling_regressions.py`: strengthen the existing public hygiene regression so README cannot drift back to vendor-specific wording or long command-reference style.
- Do not modify `SKILL.md`, `references/`, scripts, templates, or benchmark fixtures for this README rewrite.
- Do not re-add or track `self/loop-runs/`; it remains ignored local-only state.

### Task 1: Strengthen README Public-Hygiene Regression

**Files:**
- Modify: `benchmark/test_tooling_regressions.py`
- Test: `benchmark/test_tooling_regressions.py`

- [ ] **Step 1: Update the existing public-hygiene test**

Replace the body of `test_public_release_hygiene_has_docs_and_no_local_paths` with this complete body:

```python
    def test_public_release_hygiene_has_docs_and_no_local_paths(self) -> None:
        self.assertTrue((ROOT / "README.md").is_file())
        self.assertTrue((ROOT / "LICENSE").is_file())
        self.assertIn("MIT License", (ROOT / "LICENSE").read_text(encoding="utf-8"))

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("$loop-harness", readme)
        self.assertIn("<your-skills-dir>/loop-harness", readme)
        self.assertIn("agent skill", readme.lower())
        self.assertIn("metrics", readme.lower())
        self.assertIn("criteria", readme.lower())
        self.assertIn("benchmark", readme.lower())
        self.assertIn("first run", readme.lower())
        self.assertIn("later runs", readme.lower())
        self.assertIn("does not automatically install operating-system scheduler jobs", readme)
        self.assertNotIn("Codex", readme)
        self.assertNotIn("Claude", readme)
        self.assertNotIn("~/.codex", readme)
        self.assertNotIn("## Watchdog", readme)
        self.assertNotIn("## Validation", readme)
        self.assertNotIn("scripts/watchdog.py setup", readme)
        self.assertNotIn("validate_run_log_entry.py", readme)

        self.assertIn("self/loop-runs/", (ROOT / ".gitignore").read_text(encoding="utf-8"))
        if (ROOT / ".git").exists():
            tracked_self_runs = run(["git", "ls-files", "self/loop-runs"])
            self.assertEqual(tracked_self_runs.returncode, 0, tracked_self_runs.stdout)
            self.assertEqual(tracked_self_runs.stdout.strip(), "")
        else:
            self.assertFalse((ROOT / "self" / "loop-runs").exists())

        text_file_suffixes = {".md", ".py", ".json", ".yaml", ".yml", ".toml", ".txt"}
        text_file_names = {".gitignore", "LICENSE"}
        forbidden = [
            re.compile("/" + r"Users/[^\\s`'\"]+"),
            re.compile(r"\\b" + "hai" + r"do\\b", re.IGNORECASE),
            re.compile("gho" + r"_[A-Za-z0-9_]+"),
            re.compile("github" + r"_pat_[A-Za-z0-9_]+"),
            re.compile(r"sk-[A-Za-z0-9]{20,}"),
            re.compile(r"api[_-]?key\\s*=", re.IGNORECASE),
            re.compile(r"password\\s*=", re.IGNORECASE),
            re.compile(r"token\\s*=", re.IGNORECASE),
        ]

        for path in ROOT.rglob("*"):
            if path.is_dir():
                continue
            if any(part in {".git", ".worktrees", "__pycache__"} for part in path.parts):
                continue
            if path.suffix.lower() not in text_file_suffixes and path.name not in text_file_names:
                continue
            text = path.read_text(encoding="utf-8")
            for pattern in forbidden:
                self.assertIsNone(pattern.search(text), f"{pattern.pattern} matched {path.relative_to(ROOT)}")
```

- [ ] **Step 2: Run the targeted test and verify it fails**

Run:

```bash
python3 benchmark/test_tooling_regressions.py ToolingRegressionTests.test_public_release_hygiene_has_docs_and_no_local_paths
```

Expected before the README rewrite: `FAIL`, with an assertion caused by vendor-specific install wording or missing `<your-skills-dir>/loop-harness`.

- [ ] **Step 3: Commit the RED test only if working in a separate implementation branch**

If the implementation worker is committing every micro-step, commit this RED test:

```bash
git add benchmark/test_tooling_regressions.py
git commit -m "test: require platform-neutral README"
```

If working directly on `main`, skip this commit and include the test with the README rewrite commit.

### Task 2: Replace README With Agent-First Content

**Files:**
- Modify: `README.md`
- Test: `benchmark/test_tooling_regressions.py`

- [ ] **Step 1: Replace `README.md` with the approved content**

Replace the full file with:

````markdown
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
````

- [ ] **Step 2: Run the targeted test and verify it passes**

Run:

```bash
python3 benchmark/test_tooling_regressions.py ToolingRegressionTests.test_public_release_hygiene_has_docs_and_no_local_paths
```

Expected: `OK`.

- [ ] **Step 3: Check README for long lines**

Run:

```bash
awk 'length($0)>100 {print FNR ":" length($0) ":" $0}' README.md
```

Expected: no output. If there is output, wrap prose lines or convert prompt examples to wrapped bullets.

### Task 3: Run Public Package Verification

**Files:**
- Verify: `README.md`
- Verify: `benchmark/test_tooling_regressions.py`

- [ ] **Step 1: Run focused public README gates**

Run:

```bash
python3 benchmark/test_tooling_regressions.py ToolingRegressionTests.test_public_release_hygiene_has_docs_and_no_local_paths
SKILL_CREATOR_DIR="${SKILL_CREATOR_DIR:-$HOME/.codex/skills/.system/skill-creator}"
python3 "$SKILL_CREATOR_DIR/scripts/quick_validate.py" "$PWD"
```

Expected:

- Public hygiene test prints `OK`.
- `quick_validate.py` prints `Skill is valid!`.

- [ ] **Step 2: Run broader source gates**

Run:

```bash
python3 benchmark/test_tooling_regressions.py
python3 benchmark/run_pressure_eval.py --transcripts benchmark/fixtures/pass
python3 scripts/product_loop_audit.py assets/templates --min-level L2
python3 -m py_compile scripts/*.py benchmark/*.py
```

Expected:

- Tooling regression suite passes.
- Pressure eval reports all 19 pass fixtures at `10.0/10`.
- Template audit reports `Product Loop Readiness: 100/100 L2`.
- `py_compile` exits 0.

- [ ] **Step 3: Run public text leak scan**

Run:

```bash
LOCAL_ROOT_PATTERN='/'"Users"
LOCAL_USER_PATTERN='hai'"do"
GH_SHORT_PATTERN='gho''_'
GH_PAT_PATTERN='github''_pat_'
SECRET_PATTERN="sk-[A-Za-z0-9]{20,}|api[_-]?key\\s*=|password\\s*=|token\\s*="
if rg -n "$LOCAL_ROOT_PATTERN|$LOCAL_USER_PATTERN|$GH_SHORT_PATTERN|$GH_PAT_PATTERN|$SECRET_PATTERN" -g '!self/loop-runs/**' -g '!__pycache__' -g '!*.pyc' -g '!*.png' -g '!*.jpg' -g '!*.jpeg' -g '!*.gif'; then exit 1; else echo 'public text scan PASS'; fi
```

Expected: `public text scan PASS`.

### Task 4: Sync Installed Copy And Commit

**Files:**
- Modify installed copy outside git: `$HOME/.codex/skills/loop-harness`
- Commit source repo changes

- [ ] **Step 1: Sync installed copy without local self-run artifacts**

Run:

```bash
INSTALLED_SKILL_DIR="${INSTALLED_SKILL_DIR:-$HOME/.codex/skills/loop-harness}"
rm -rf "$INSTALLED_SKILL_DIR/self/loop-runs"
rsync -a --delete --exclude '.git' --exclude '.worktrees' --exclude '__pycache__' --exclude 'self/loop-runs' "$PWD/" "$INSTALLED_SKILL_DIR/"
```

Expected: command exits 0.

- [ ] **Step 2: Verify installed copy**

Run:

```bash
SKILL_CREATOR_DIR="${SKILL_CREATOR_DIR:-$HOME/.codex/skills/.system/skill-creator}"
INSTALLED_SKILL_DIR="${INSTALLED_SKILL_DIR:-$HOME/.codex/skills/loop-harness}"
python3 "$SKILL_CREATOR_DIR/scripts/quick_validate.py" "$INSTALLED_SKILL_DIR"
python3 "$INSTALLED_SKILL_DIR/benchmark/test_tooling_regressions.py"
python3 "$INSTALLED_SKILL_DIR/benchmark/run_pressure_eval.py" --transcripts "$INSTALLED_SKILL_DIR/benchmark/fixtures/pass"
```

Expected:

- Installed quick validate prints `Skill is valid!`.
- Installed tooling regression suite passes.
- Installed pressure eval reports all 19 pass fixtures at `10.0/10`.

- [ ] **Step 3: Commit README rewrite**

Run:

```bash
git add README.md benchmark/test_tooling_regressions.py
git commit -m "Rewrite README for agent-first usage"
```

Expected: commit succeeds.

- [ ] **Step 4: Push**

Run:

```bash
git push
```

Expected: `main` pushes to `origin/main`.
