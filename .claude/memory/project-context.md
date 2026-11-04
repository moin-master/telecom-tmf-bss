# Project memory

Stable facts. Update when they change.

- Telecom BSS proof of concept: TM Forum Open APIs over GraphQL. Python 3.12+, FastAPI, Strawberry, SQLAlchemy, SQLite, blinker events, uv.
- Architecture: `uv` workspace, one separate Python project per TM Forum API under `services/`, a `host` app that mounts them all on ONE port (8060) under `/telecom-tmf-bss/<path>`, a `shared` library. Each service has its own SQLite file. Services call each other only through `client.py`.
- Docs: docs/project-routing.md (names, paths), docs/project-architecture.md (dependencies, events), docs/project-tech-stack.md, docs/project-proposal.md.
- Layout of files: .claude/rules/project-layout.md.
- Specs: `specs/` holds a committed, never-updated snapshot of TM Forum specs (v5 yaml for 12 APIs; v4 swagger JSON for TMF641, TMF676, TMF700). Apache 2.0. See specs/README.md.
- Web UI: planned in `web/` (React, TypeScript, Vite, proxy to port 8060). Storefront is "Lemon Mobile": clean and minimal, lemon yellow #FFF700 (paletadecolores.org) on white (light) or blackish gray (dark), always dark text on lemon; rules in the web-design skill (the user rejected a neon dark Gen-Z look and a pastel Gen-Z look). Home page is a grid of offers with search and category filter; the cart is created on the first "Add to cart". Skills: web-scaffold, web-api-client, web-page-build, web-project-visualizer, web-verify. Pages are added as each backend API is merged.
- Planning first, code only on explicit request. Reads, then errors, then writes.
- The user removed proposal sections 7 to 10 on purpose; do not re-add them.
