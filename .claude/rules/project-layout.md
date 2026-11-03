# Project layout (proposed)

Status: proposed. Change here once when the layout is decided; commands and skills refer to this file.

A `uv` workspace: every service is its own Python project, mounted by a host app on one port (see docs/project-routing.md).

```
pyproject.toml              workspace root, members: host, shared, services/*
host/
  pyproject.toml
  src/host/main.py          FastAPI app; mounts each service at /<path>; combined /graphql
  src/host/combined.py      customer 360 schema, calls services through their clients
shared/
  pyproject.toml
  src/shared/               config (BSS_*), TM Forum error shape, event bus, db helpers
services/<name>/            <name> is the module name from docs/project-routing.md
  pyproject.toml            depends on shared and on other services only for their client
  src/<pkg>/                <pkg> = <name> with hyphens replaced by underscores
    app.py                  create_app() returning the ASGI app for this service
    models.py               SQLAlchemy tables, owned by this service
    repository.py           only place that touches the session
    service.py              business rules and state machine
    client.py               public interface other services call (in-process now)
    schema.py               Strawberry types, inputs, resolvers
    events.py               signals this service publishes
    seed.py                 seed data
  data/<name>.db            SQLite file (gitignored)
specs/                      TM Forum spec snapshot, committed, not updated (see specs/README.md)
payloads/<name>/            generated sample payloads
.run/                       pid files for restart commands (gitignored)
tests/<name>/               only when tests are requested
```

Names, TMF numbers and URL paths come from docs/project-routing.md. Do not invent new ones.

Standalone debug port for a service: 8060 plus its 1-based row number in the routing table (party 8061, customer 8062, and so on).
