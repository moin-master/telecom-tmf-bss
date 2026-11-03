---
description: Restart the host app that serves every service on port 8060
---

1. Stop any running host: read `.run/host.pid`; if the process is alive, `kill` it. Also free the port: `lsof -ti :8060` and kill only processes whose command is uvicorn.
2. `mkdir -p .run`.
3. Start in the background: `uv run uvicorn host.main:app --host 127.0.0.1 --port 8060 > .run/host.log 2>&1 & echo $! > .run/host.pid` (run with `run_in_background`).
4. Wait until `curl -s http://127.0.0.1:8060/telecom-tmf-bss/health` succeeds (up to 15 seconds). If it fails, show the last 30 lines of `.run/host.log`.
5. Report the PID and the base URL.

If `host/` does not exist yet, say so and stop.
