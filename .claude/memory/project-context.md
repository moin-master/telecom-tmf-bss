# Project memory

Stable facts. Update when they change.

- Telecom BSS proof of concept: TM Forum Open APIs over GraphQL. Python 3.12+, FastAPI, Strawberry, SQLAlchemy, SQLite, blinker events, uv.
- Architecture: `uv` workspace, one separate Python project per TM Forum API under `services/`, a `host` app that mounts them all on ONE port (8060) under `/telecom-tmf-bss/<path>`, a `shared` library. Each service has its own SQLite file. Services call each other only through `client.py`.
- Docs: docs/project-routing.md (names, paths), docs/project-architecture.md (dependencies, events), docs/project-tech-stack.md, docs/project-proposal.md.
- Layout of files: .claude/rules/project-layout.md.
- Planning first, code only on explicit request. Reads, then errors, then writes.
- The user removed proposal sections 7 to 10 on purpose; do not re-add them.
