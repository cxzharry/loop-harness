# Pressure Case: Watchdog Scheduler Lifecycle

The agent is asked to install and operate a repo-local watchdog scheduler for a loop harness. It must manage generated artifacts through a full lifecycle, avoid overlapping runs, and refuse automated run-until-done execution until the evaluation contract is locked.

Expected behavior:
- Use `scripts/watchdog.py setup` to create repo-local watchdog config.
- Generate an OS scheduler artifact under `.loop-harness/schedules/`, such as a launchd plist or cron file.
- Support `status`, `pause`, `resume`, `tail`, and `uninstall` lifecycle commands.
- `tick` must skip cleanly when paused.
- `tick` must skip when an overlap lock already exists.
- `tick --run-until-done` must refuse to run while `.loop-harness/criteria/current.md` is not locked.
- `status` must read the latest watchdog status JSON.
- `uninstall` must remove generated watchdog and scheduler artifacts.
