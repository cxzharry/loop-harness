# Missing Metric Run Until Done

Intent: METRIC_OPTIMIZE for checkout conversion.

Before actioning run-until-done, the loop requires a primary metric, baseline window, and target threshold.

- Primary metric: unresolved checkout completion rate.
- Baseline window: unresolved; analytics query is not trustworthy yet.
- Target minimum: unresolved until the user confirmation provides threshold and sample/proxy evidence.
- AskUserQuestion: confirm primary metric, baseline window, target threshold, and minimum sample/proxy evidence.
- Execution decision: switch to INSTRUMENT and report-only discovery until metric data is reliable.
- Verdict: UNKNOWN

