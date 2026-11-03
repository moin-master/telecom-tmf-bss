---
name: scaffold-service
description: Create a new service as its own Python project in the uv workspace and register it with the host app. Use when starting a TM Forum API service for the first time.
---

# Scaffold a service

Input: service name from docs/project-routing.md (for example `order`). Layout is in `.claude/rules/project-layout.md`.

1. Look up the name, TMF number and URL path in docs/project-routing.md. Stop if the name is not there.
2. If the workspace root `pyproject.toml` does not exist, run `uv init --bare` and add `[tool.uv.workspace] members = ["host", "shared", "services/*"]`. Create `shared` and `host` projects the same way when missing.
3. `uv init --package services/<name> --name <name>`; rename the package folder to `<pkg>` (hyphens to underscores) if needed.
4. Add dependencies: `uv add --package <name> fastapi strawberry-graphql sqlalchemy` and `uv add --package <name> --editable ./shared`.
5. Create the files listed in the layout (`app.py`, `models.py`, `repository.py`, `service.py`, `client.py`, `schema.py`, `events.py`, `seed.py`) with `create_app()` returning an ASGI app that serves `/graphql`, and a `/health` route.
6. Register the service in `host/src/host/main.py`: mount `create_app()` at its path from the routing table.
7. Run `uv sync` and `uv run python -c "import <pkg>.app"` to prove it imports. Start the host and request `/telecom-tmf-bss/<path>/health`.

Keep the scaffold empty of business logic; the implementation flow adds it.
