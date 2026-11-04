---
name: web-verify
description: Verify the web app: typecheck, build, run the dev server against the live backend, and look at the pages in a browser. Use after any change in /web.
---

# Verify the web app

1. Backend: `curl -s http://127.0.0.1:8060/telecom-tmf-bss/health`. If it is down, run the restart-all command.
2. Static checks, in `web/`: `npm run typecheck` and `npm run build`. Fix errors before continuing.
3. Dev server: follow the web-start command (port 5173, pid in `.run/web.pid`, log in `.run/web.log`).
4. Through the proxy: `curl -s -X POST http://127.0.0.1:5173/telecom-tmf-bss/product-catalog/graphql -H 'content-type: application/json' -d '{"query":"{ productOfferingList { id } }"}'` must return data.
5. Look at the pages in a browser if one is available (the built-in browser or Claude in Chrome skills): open `http://127.0.0.1:5173/`, check the changed pages at phone width (about 390 px) and desktop width, click the main flow (browse, open an offer, add to cart, open the cart, remove an item), and read the browser console for errors.
6. If no browser tool is available but Google Chrome is installed, take headless screenshots and look at them with the Read tool (images are shown visually). Write them to the scratchpad directory, one per page and width:
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=8000 --window-size=390,1400 --screenshot=<scratchpad>/home-mobile.png http://127.0.0.1:5173/`
   Repeat with `--window-size=1280,1000` for desktop. `--virtual-time-budget` lets the React app load its data before the shot. Check the design against the web-design skill (palette, per-page checklist, guardrails), and fix what looks wrong.
   Chrome's command-line screenshot has a minimum window width, so it crops phone-width pages. For real phone width, clicking through flows, light mode, reduced motion and console errors, use `browser-check.mjs` in this skill folder: it drives headless Chrome through the DevTools protocol with Node's built-in WebSocket (`node .claude/skills/web-verify/browser-check.mjs <scratchpad> [modes]`) and prints a JSON summary. It is written for the offers, cart and detail flow; adapt the ids and selectors when pages change. Its helper `waitFor` returns false for DOM elements (they cannot be serialised), so test with expressions that return booleans.
7. If you cannot look at the pages at all, say so, and report only what steps 1 to 4 proved. Do not claim the UI looks right without looking.
8. Report: checks run, what passed, what failed, anything not verified.

Do not write test files unless the user asks.
