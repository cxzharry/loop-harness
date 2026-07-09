## Transcript

I installed the watchdog with `scripts/watchdog.py setup --repo /tmp/product-repo --kind launchd --cadence hourly --label product.loop.watchdog --command "python3 scripts/run_loop_controller.py --repo /tmp/product-repo --command 'npm test'"`. The setup wrote `.loop-harness/watchdog/config.json` and generated the OS scheduler artifact `.loop-harness/schedules/product.loop.watchdog.plist` for launchd.

Lifecycle commands covered: setup, status, pause, resume, tail, uninstall.

I checked `scripts/watchdog.py status --repo /tmp/product-repo`; status read the latest `.loop-harness/watchdog/status.json` and reported the current decision, timestamp, cadence, paused flag, and last log path.

Pause behavior: `scripts/watchdog.py tick --repo /tmp/product-repo` observes the paused state after `scripts/watchdog.py pause --repo /tmp/product-repo`. Because the watchdog was paused, tick records decision `skipped_paused` and does not run the command. I then used `scripts/watchdog.py resume --repo /tmp/product-repo` to clear the pause state.

For lock/no-overlap protection, I verified that an existing `.loop-harness/watchdog/run.lock` makes `scripts/watchdog.py tick --repo /tmp/product-repo` skip with decision `skipped_overlap`; the existing lock is preserved and no second loop starts.

For the criteria gate, I ran `scripts/watchdog.py tick --repo /tmp/product-repo --run-until-done` while `.loop-harness/criteria/current.md` was still draft. The watchdog refused run-until-done with decision `blocked_unlocked_criteria` and required `Contract status: locked` before scheduler-driven action.

I inspected logs with `scripts/watchdog.py tail --repo /tmp/product-repo --lines 40`, which read the latest watchdog log path from status JSON. Finally, I ran `scripts/watchdog.py uninstall --repo /tmp/product-repo`; uninstall removed generated artifacts including `.loop-harness/watchdog/config.json`, `.loop-harness/watchdog/run.lock`, and `.loop-harness/schedules/product.loop.watchdog.plist`.
