# Global Knowledge Selects Subset

Discovery used ~/.codex/loop-harness/knowledge/ as a local global knowledge store.

- Tool: select_knowledge.py
- Profile: ux-product
- Intent: UX_OPTIMIZE
- Surface: web-route
- Selection: subset matching by profile, intent, and surface.
- Selected criteria: Playwright route evidence, visual-quality checks, and no critical slop.
- Benchmark seeds: route evidence seed and mobile overflow seed.
- Persistence: selected criteria and benchmark seeds are recorded in .loop-harness/PRODUCT_LOOP_STATE.md.
- Fallback: if registry.json is absent, built-in fallback criteria are used.
- Safety: global seeds are not active benchmark cases without repo-local evidence.

