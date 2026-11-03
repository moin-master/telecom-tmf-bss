# Project proposal: Telecom BSS

Status: **draft for discussion**. Items marked *proposed* or *open* are not yet decided.

## 1. Goal

Build a proof of concept that implements a realistic telecom order-to-cash scenario using TM Forum Open API resource models, served over GraphQL, with SQLite as storage. The result should be understandable end to end and structured so it can later grow into a real application.

## 2. Why GraphQL on top of TM Forum APIs

TM Forum Open APIs are REST/JSON, one API per domain (catalog, customer, ordering, inventory, billing, and so on). A client that needs a complete picture, such as a support agent screen showing a customer, their products, open orders, latest bill and tickets, must call many APIs and stitch the results.

GraphQL lets the client describe that picture in one request while the server resolves each part from its own domain.

## 3. Scenario

1. A catalog admin defines product specifications and offerings with prices.
2. A customer registers and gets a billing account.
3. The customer browses offerings and adds some to a shopping cart.
4. Checkout turns the cart into a product order.
5. The order is fulfilled: a service is created, resources (for example a SIM and a number) are allocated, and a shipment is created for physical items.
6. When the order completes, the product appears in the customer's product inventory.
7. Usage records are generated (simulated).
8. A billing cycle run produces a customer bill with applied rates.
9. The customer pays the bill.
10. Optionally the customer raises a trouble ticket.
11. A customer 360 query reads across all of the above.

## 4. TM Forum APIs in scope

| Area | API | Notes |
|------|-----|-------|
| Product catalog | TMF620 Product Catalog Management | specifications, offerings, prices |
| Customer registry | TMF629 Customer Management, TMF632 Party Management | |
| Accounts | TMF666 Account Management | billing accounts, billing cycle specification |
| Shopping cart | TMF663 Shopping Cart | |
| Ordering | TMF622 Product Ordering | order state machine |
| Service fulfilment | TMF641 Service Ordering, TMF638 Service Inventory | |
| Resources | TMF639 Resource Inventory | SIM, phone number |
| Shipment | TMF700 Shipping Order Management | *to be verified against the specs* |
| Product inventory | TMF637 Product Inventory | what the customer owns |
| Usage | TMF635 Usage Management | simulated records |
| Billing | TMF678 Customer Bill Management | bill cycles, bills, applied rates |
| Payment | TMF676 Payment Management | |
| Support (optional) | TMF621 Trouble Ticket | |

The exact resources and fields will be confirmed by reading the specifications (see open decisions).

## 5. Architecture (proposed)

A **modular monolith**: one Python application, one package per TM Forum domain, one SQLite database, one GraphQL schema.

### Technology stack

| Layer | Choice | Status |
|-------|--------|--------|
| Language | Python 3.12+ | decided |
| API style | GraphQL | decided |
| Database | SQLite (embedded, file-based) | proposed |
| GraphQL library | Strawberry (code-first, uses type hints), alternative Ariadne (schema-first) | open |
| Web framework | FastAPI (Strawberry mounts into it) | proposed |
| Persistence | SQLAlchemy 2.x | proposed |
| Validation / models | Pydantic where useful | proposed |
| Package and environment management | uv | proposed |

Module rules, the service block diagram, dependencies and event flow are in [project-architecture.md](project-architecture.md).

Path to a real application:

- SQLite to a production database (for example PostgreSQL) through configuration, since SQLAlchemy abstracts the engine.
- A module replaced by calls to a real TM Forum service, with the GraphQL schema unchanged.
- A module split into its own service if needed.

Alternatives considered: microservices per domain with a GraphQL gateway (more realistic, much heavier), and a monolith that also exposes TM Forum REST endpoints (closer to the standard, doubles the API work).

## 6. Technical considerations

| Topic | Approach (proposed) |
|-------|---------------------|
| State machines (order, product, ticket) | enforced in the service layer; defined by spec text, not the swagger files |
| Order orchestration | event-driven inside the monolith, synchronous first for clarity |
| Billing | simple: monthly recurring charges plus usage; no tax, proration or discounts initially |
| Money and time | `decimal.Decimal` for amounts, timezone-aware `datetime` (UTC) for timestamps |
| Billing cycle trigger | an on-demand mutation (for example `runBillingCycle`) before any scheduler |
| Storage | SQLite file so data survives restarts; seed data in SQL scripts or a Python seed module |
| Polymorphism (`@type`), reference objects (`href`), free-form values, PATCH semantics | one agreed policy per issue, written down once |
| Scope creep | fixed slice order below |

## 7. Phases

Same incremental style as the earlier project: reads first, then errors, then writes.

| Stage | Content |
|-------|---------|
| 0 | Project skeleton, docs, `CLAUDE.md`, skills, TM Forum conventions |
| 1 | Read-only GraphQL over seed data for all modules, ending with the customer 360 query |
| 2 | Search, filters and pagination |
| 3 | Exception handling in TM Forum error style |
| 4 | Mutations for the happy path: catalog, cart, order, fulfilment, inventory |
| 5 | Usage, billing cycle run, bill, payment |
| 6 | Optional: batching (DataLoader), subscriptions for events, tests |

## 8. Working agreement

- Discussion and planning first. **No code is written until explicitly requested.**
- No unit or integration tests until requested.
- Keep it simple and incremental; this is a learning project that can grow.

## 9. Open decisions

| # | Decision | Current leaning |
|---|----------|-----------------|
| 1 | Architecture | modular monolith |
| 2 | Spec version, v4 or v5 | open |
| 3 | Fidelity to TM Forum schemas (strict with refs, `@type`, `href`, or simplified with TM Forum names and flat ids) | simplified, leaning |
| 4 | Order of delivery: which modules go into the first slice | catalog, customer, account, cart, order, product inventory first; service, resource, shipment, usage and billing next |
| 5 | Download and read the specifications before designing the schema | open |
| 6 | Shipment: the TMF700 API or a simplified shipment concept | open |
| 7 | Pagination style (offset/limit as in TM Forum, or page/size) | offset/limit, leaning |
| 8 | Identifier format (readable strings such as `CUS-1001`) | readable strings, leaning |
| 9 | Database | SQLite via SQLAlchemy, swappable later |
| 10 | Python GraphQL library: Strawberry or Ariadne | Strawberry, leaning |
| 11 | Language and stack | **Python + GraphQL + SQLite** (replaces the earlier Java/Spring Boot plan) |

## 10. Risks

- The scenario spans many resources; building API by API instead of slice by slice would stall.
- State machines and orchestration take real design effort.
- Billing logic can grow without bound if not kept simple.
- Matching the TM Forum specs in detail can consume the project; fidelity needs a deliberate limit.
