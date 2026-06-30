# global_knowledge_selects_subset

## Prompt

```text
Use loop-harness to improve a web route in a repo that has global local loop knowledge available.
```

## Fixture

`~/.codex/loop-harness/knowledge/registry.json` exists with criteria packs for multiple profiles and surfaces.

## Expected Behavior

- Use `scripts/select_knowledge.py`.
- Match by intent, profile, and surface.
- Select a subset of criteria and benchmark seeds.
- Record selected criteria in `.loop-harness/PRODUCT_LOOP_STATE.md`.
- Treat global benchmark seeds as seeds only, not active repo benchmarks without repo-local evidence.
- Fall back to built-in defaults if the global registry is absent.

## Critical Failures

- Loads all global knowledge into context.
- Turns a global seed into an active benchmark without repo-local evidence.
- Ignores global criteria when a matching pack exists.

