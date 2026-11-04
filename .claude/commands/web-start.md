---
description: Start or restart the web dev server on port 5173
---

1. If `web/package.json` does not exist, say so and suggest the web-scaffold skill; stop.
2. Stop the old server: read `.run/web.pid`; if the process is alive, `kill` it. Free port 5173 only if a node process holds it (`lsof -ti :5173`).
3. If `web/node_modules` is missing, run `npm install` in `web/`.
4. `mkdir -p .run`, then start in the background from `web/`: `npm run dev -- --host 127.0.0.1 --port 5173 > ../.run/web.log 2>&1 & echo $! > ../.run/web.pid` (run with `run_in_background`).
5. Wait until `curl -s http://127.0.0.1:5173/` succeeds (up to 15 seconds); otherwise show the last 30 lines of `.run/web.log`.
6. Remind that the backend must be running too (`/restart-all`). Report the URL `http://127.0.0.1:5173/`.
