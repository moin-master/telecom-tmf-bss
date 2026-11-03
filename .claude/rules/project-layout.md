# Project layout (proposed)

Status: proposed. Change here once when the layout is decided; commands and skills refer to this file.

A `uv` workspace: every service is its own Python project, mounted by a host app on one port (see docs/project-routing.md).

```
pyproject.toml              workspace root, members: host, shared, services/*
host/
  pyproject.toml            project bss-host
  src/bss_host/main.py      FastAPI app; mounts each service at /<path>; combined /graphql later
  src/bss_host/combined.py  customer 360 schema, calls services through their clients (later)
shared/
  pyproject.toml            project bss-shared
  src/bss_shared/           config (BSS_*), clock, db helpers (UtcDateTime, DecimalText, sqlite_url),
                            errors (TmfError), pagination, graphql (DtoConverter: DTO -> Strawberry type);
                            event bus later
services/<name>/            <name> is the module name from docs/project-routing.md
  pyproject.toml            depends on shared and on other services only for their client
  src/<pkg>/                <pkg> = <name> with hyphens replaced by underscores
    app.py                  create_app() returning the ASGI app; calls init_db() (mounted apps skip lifespan)
    db.py                   engine, SessionLocal, init_db() (create tables, seed when empty)
    models.py               SQLAlchemy tables, owned by this service (own Base per service)
    repository.py           only place that touches the session
    service.py              business rules and state machine; maps rows to DTOs
    dto.py                  plain dataclasses returned by service and client (no ORM objects)
    client.py               public interface other services call (in-process now)
    schema.py               Strawberry types, inputs, resolvers
    events.py               signals this service publishes (when it has any)
    seed.py                 seed data
  data/<name>.db            SQLite file (gitignored)
specs/                      TM Forum spec snapshot, committed, not updated (see specs/README.md)
payloads/<name>/            generated sample payloads
.run/                       pid files for restart commands (gitignored)
tests/<name>/               only when tests are requested
```

Names, TMF numbers and URL paths come from docs/project-routing.md. Do not invent new ones.

Standalone debug port for a service: 8060 plus its 1-based row number in the routing table (party 8061, customer 8062, and so on).
