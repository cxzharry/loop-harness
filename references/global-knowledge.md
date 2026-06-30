# Global Local Knowledge

Use this reference when a loop should reuse local knowledge across repos without bloating the skill package.

## Folders

- Skill package: `~/.codex/skills/loop-harness/` for code, scripts, templates, and concise defaults.
- Repo runtime: `<repo>/.loop-harness/` for state, run-log, active repo benchmarks, handoffs, and worktree maps.
- Global local knowledge: `~/.codex/loop-harness/knowledge/` for reusable criteria, benchmark seeds, candidate findings, and promoted general knowledge.

Expected global layout:

```text
~/.codex/loop-harness/knowledge/
  registry.json
  inbox/
    candidate-knowledge.jsonl
    blocked-knowledge.jsonl
  promoted/
    global-knowledge.jsonl
```

## Discovery Selection

During Discovery, select a subset instead of loading the whole global store:

```bash
python3 <skill-dir>/scripts/select_knowledge.py \
  --repo <repo> \
  --profile ux-product \
  --intent UX_OPTIMIZE \
  --surface web-route
```

Selection order:

1. Repo-local active benchmarks in `<repo>/.loop-harness/PRODUCT_LOOP_BENCHMARK.md`.
2. Global local registry at `~/.codex/loop-harness/knowledge/registry.json`, if present.
3. Built-in minimal fallback criteria inside `select_knowledge.py`.

Record selected criteria and benchmark seeds in `.loop-harness/PRODUCT_LOOP_STATE.md`. Global seeds are not active repo benchmarks until a repo-local finding provides evidence.

## Registry Shape

```json
{
  "version": 1,
  "criteria_packs": [
    {
      "id": "ux-web-route-basic",
      "profiles": ["ux-product"],
      "intents": ["UX_OPTIMIZE"],
      "surfaces": ["web-route"],
      "criteria": ["Use Playwright for browser-visible verification."],
      "benchmark_seeds": [
        {
          "id": "playwright-route-evidence",
          "matching_rule": "Browser-visible route verification.",
          "expected_result": "URL, viewport, flow steps, and assertions are recorded."
        }
      ]
    }
  ]
}
```

## Global Promotion Gate

Promote globally only after repo-local persistence:

1. Append `Raw Run Result`, `Finding`, and `Benchmark Promotion` to `.loop-harness/product-loop-run-log.md`.
2. Promote durable repo protection to `.loop-harness/PRODUCT_LOOP_BENCHMARK.md`.
3. Run:

```bash
python3 <skill-dir>/scripts/promote_global_knowledge.py --repo <repo>
```

Default behavior writes only to `~/.codex/loop-harness/knowledge/inbox/candidate-knowledge.jsonl` when the gate passes. Use `--promote` only after explicit human approval or a separate review has confirmed the finding is generally reusable.

The gate blocks missing evidence, env blockers, non-promoted repo findings, inactive repo benchmarks, and likely domain-specific findings. Domain-specific failures stay in the repo-local benchmark.
