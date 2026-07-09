# Evaluation Contract

Use this self-loop contract for the current loop-harness hardening run.

Contract status: locked

## Product Surface

- Surface: loop-harness skill package
- User flow: author updates skill behavior, scaffolds target-repo loop artifacts, runs self benchmarks, syncs installed skill
- Intent: ENGINEERING_QUALITY
- Profiles: engineering-quality, content-docs

## Metric

- Primary metric: source and installed validation pass rate
- Baseline window: before 2026-07-09 scale and evaluation-contract hardening
- Target: all deterministic source and installed validation commands pass
- Target minimum: 100% of required validation commands pass
- Direction: binary-pass
- Source: local command output from tooling regression tests, pressure eval, audits, selector, cost check, quick_validate, and py_compile
- Sample/window caveat: skill-package self-development has no browser product surface

## Acceptance Criteria

- Criterion: new target repos scaffold `.loop-harness/criteria/current.md`, `benchmarks/active/`, `benchmarks/archive/`, and `runs/archive/`
- Evidence required: tooling regression test and scaffold pressure fixture pass
- Pass threshold: PASS
- Non-applicability rule: none for target-repo scaffold behavior

- Criterion: actioning requires a locked repo-local evaluation contract with metric/rubric, acceptance criteria, benchmark seeds, and Playwright flow when applicable
- Evidence required: pressure case `evaluation_contract_before_action` passes
- Pass threshold: PASS
- Non-applicability rule: report-only/evaluation-contract bootstrap is allowed when the contract is not locked

- Criterion: promoted active benchmark cases can scale out of `PRODUCT_LOOP_BENCHMARK.md`
- Evidence required: controller writes full cases to `benchmarks/active/`, selector reads active split files, audit counts active split files, and archive files are ignored
- Pass threshold: PASS
- Non-applicability rule: old loop roots without split directories may keep legacy inline cases

## Benchmark seeds

- Seed id: evaluation_contract_before_action
- Matching rule: changes touch pre-action loop requirements, criteria/current.md, operation docs, or templates
- Expected result: actioning is blocked until `Contract status: locked`
- Verification command: `python3 benchmark/run_pressure_eval.py --case evaluation_contract_before_action --transcripts benchmark/fixtures/pass`
- Activation rule: promoted by this self run

- Seed id: split_active_benchmark_files
- Matching rule: changes touch benchmark storage, controller promotion, selector, audit, or retention docs
- Expected result: active split case files are selected and audited; archive files are ignored
- Verification command: `python3 benchmark/run_pressure_eval.py --case split_active_benchmark_files --transcripts benchmark/fixtures/pass`
- Activation rule: promoted by this self run

## Browser Verification

- Playwright required for app verification: no
- URL or route: not_applicable
- Viewports: not_applicable
- Flow steps: not_applicable
- Assertions: not_applicable
- Screenshot/trace expectation: not_applicable

## User Confirmations

- Metric confirmed: inferred from user request to self-fix loop-harness until clean
- Target confirmed: all deterministic validation commands pass
- Human gates: none for local skill-package edits and installed skill sync
- Non-goals: no live browser product route, no production deployment
- Last reviewed: 2026-07-09T04:17:58Z
