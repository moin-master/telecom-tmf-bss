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

The technologies used (Python, GraphQL, SQLite and the rest) are listed in [project-tech-stack.md](project-tech-stack.md).

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
