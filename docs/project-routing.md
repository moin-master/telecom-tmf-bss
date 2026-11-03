# Project routing

Status: **draft for discussion**. Modules and dependencies are in [project-architecture.md](project-architecture.md).

All modules are reached through one host and one port, under one context path. The module is chosen by the path after it, so there are no per-service ports to manage.

Base URL: `http://127.0.0.1:8060/telecom-tmf-bss`

Host, port (8060) and context path are set in configuration.

## Routes

Paths are relative to the base URL. Each module lives under its path, and its GraphQL endpoint is `<path>/graphql`: POST runs a query or mutation, GET in a browser opens the explorer. The module path stays free for other endpoints such as `/order/health`.

| Module path | Module | TM Forum API |
|------|--------|--------------|
| /party | party | TMF632 |
| /customer | customer | TMF629 |
| /account | account | TMF666 |
| /product-catalog | catalog | TMF620 |
| /shopping-cart | cart | TMF663 |
| /order | order | TMF622 |
| /service-order | service-order | TMF641 |
| /service-inventory | service-inventory | TMF638 |
| /resource | resource | TMF639 |
| /shipment | shipment | TMF700 |
| /product-inventory | product-inventory | TMF637 |
| /usage | usage | TMF635 |
| /billing | billing | TMF678 |
| /payment | payment | TMF676 |
| /ticket | ticket | TMF621 |
| (none) | combined schema, at `/graphql` | customer 360 across modules |

Examples:

- `http://127.0.0.1:8060/telecom-tmf-bss/order/graphql`
- `http://127.0.0.1:8060/telecom-tmf-bss/graphql` (combined)

## Notes

- One Python application mounts each module's GraphQL router under its path.
- Paths are for outside clients; modules call each other through Python service interfaces.
- If modules are split into separate processes later, a reverse proxy keeps these URLs and forwards each path to the module's own port.
