---
description: Restart one service (host by default, or a standalone debug instance)
argument-hint: <service name> [--standalone]
---

Services are mounted in the host app, so by default restarting one service restarts the host: follow the restart-all command, then check `/telecom-tmf-bss/<path>/health` for the named service.

With `--standalone`: run only that service on its debug port (8060 plus its row number in docs/project-routing.md).
1. Free the port if a uvicorn process holds it (`lsof -ti :<port>`).
2. Start `uv run --package <name> uvicorn <pkg>.app:app --host 127.0.0.1 --port <port>` in the background, log to `.run/<name>.log`, pid to `.run/<name>.pid`.
3. Check `http://127.0.0.1:<port>/health` and report.

Stop and say so if the service name is not in docs/project-routing.md or its project does not exist yet.
