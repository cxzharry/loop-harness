# Product Loop Budget

Max runs per day: 3
Max runs per week: 10
Max iterations per opportunity: 3
Max actioning changes per run: 1
Max subagent/tool-heavy checks per run: 4
Token or time budget: 120000 tokens or 60 minutes
Kill switch: stop on repeated validation failure, installed/source divergence, or scope expansion beyond benchmark support
Escalation: ask user before enabling scheduled unattended pressure evals

## Cost Notes

- Manual behavior benchmark runs require real transcripts and should not be scheduled without a stable transcript-producing harness.
- High-frequency scheduling is not enabled for this self-loop.
