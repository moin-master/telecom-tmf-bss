# Project tech stack: Telecom BSS

Status: **draft for discussion**. This is the single list of technologies used in the project. Why they were chosen and which decisions are open is tracked in [project-proposal.md](project-proposal.md); how the modules fit together is in [project-architecture.md](project-architecture.md).

Status values: **decided** (agreed), **proposed** (my suggestion, not yet agreed), **open** (undecided), **later** (not needed until a later stage).

## 1. Application

| Area | Technology | Status | Notes |
|------|------------|--------|-------|
| Language | Python 3.12+ | decided | |
| API style | GraphQL | decided | one schema per service plus a combined schema, no REST endpoints |
| Project structure | `uv` workspace, one project per service plus a host app | decided | host mounts every service on one port |
| GraphQL library | Strawberry | open | code-first, uses type hints; alternative is Ariadne (schema-first), proposal decision 10 |
| Web framework | FastAPI | proposed | hosts the GraphQL endpoint; Strawberry mounts into it |
| Persistence | SQLAlchemy 2.x | proposed | ORM and database abstraction |
| Validation / models | Pydantic | proposed | where useful, for example input checking |
| Money and time | `decimal.Decimal`, timezone-aware `datetime` (UTC) | proposed | no floats for money |

## 2. Data

| Area | Technology | Status | Notes |
|------|------------|--------|-------|
| Database | SQLite | proposed | embedded, file-based, no separate server; swappable later through SQLAlchemy |
| Seed data | SQL scripts or a Python seed module | open | loaded at startup for the read-only stages |
| Production database | PostgreSQL | later | example target only, not decided |

## 3. Integration and events

| Area | Technology | Status | Notes |
|------|------------|--------|-------|
| Service-to-service calls | client interface per service, in-process now | decided | HTTP implementation later; never through another service's repository |
| Events | in-process event bus using blinker | decided | named signals (for example `order_accepted`), synchronous by default, `send_async` available; not an external broker |
| Message broker | Kafka or similar | later | only if modules are split into separate services |

## 4. Standards

| Area | Standard | Status | Notes |
|------|----------|--------|-------|
| Domain APIs | TM Forum Open APIs: TMF620, TMF621, TMF622, TMF629, TMF632, TMF635, TMF637, TMF638, TMF639, TMF641, TMF663, TMF666, TMF676, TMF678, TMF700 | decided | list and notes in proposal section 4; TMF700 exists in the tmforum-apis repos (v4.0.0 only) |
| Spec version | TM Forum v5 (OpenAPI yaml) | decided | snapshot in `specs/`, see specs/README.md; the tmforum-apis repos have no v5 file for TMF641, TMF676 and TMF700, so those three are open |

## 5. Web UI

Lives in `web/`. Shows the offers, cart and later screens, plus an "Explore" area that visualizes the services and APIs. Built step by step as each API is implemented.

| Area | Technology | Status | Notes |
|------|------------|--------|-------|
| UI library | React with TypeScript | proposed | strict mode |
| Build and dev server | Vite | proposed | port 5173; proxies `/telecom-tmf-bss` to the backend on 8060, so no CORS is needed |
| Routing | React Router | proposed | |
| Server data | TanStack Query | proposed | caching and loading states |
| GraphQL client | graphql-request | proposed | small; one client per service |
| Types | GraphQL Code Generator (client preset) | proposed | one output folder per service; generated files committed |
| Styling | plain CSS with variables | proposed | no UI framework until needed |
| Node | Node 24, npm | in use | |

## 6. Tooling

| Area | Technology | Status | Notes |
|------|------------|--------|-------|
| Package and environment management | uv | proposed | `pyproject.toml`, `uv.lock`, `.venv/` |
| Version control | Git, GitHub | decided | repository `moin-master/telecom-tmf-bss`, branch `main` |
| Editor | VS Code with Claude Code | in use | |
| Testing | pytest | later | no tests until requested |
| Lint and format | Ruff | later | not chosen yet |
| Documentation | Markdown, ASCII diagrams | decided | in `docs/` |
