# Telecom BSS

A proof of concept of a telecom Business Support System (BSS), built on **TM Forum Open APIs**, exposed through **GraphQL**, and stored in **SQLite**.

Status: **planning only. No code yet.**

## What this is

A learning and demonstration project that walks one complete telecom scenario, from the product catalog to the customer's bill:

```
Catalog -> Offering -> Shopping cart -> Order -> Fulfilment (service, resource, shipment)
        -> Product inventory -> Usage -> Billing cycle -> Bill -> Payment
```

A single GraphQL query should be able to read across all of it (a "customer 360" view), which is where GraphQL helps over the underlying REST-style TM Forum APIs.

## Planned stack

- Python 3.12+, FastAPI, Strawberry (GraphQL)
- SQLAlchemy with SQLite (swappable to a real database later)
- Layers: GraphQL resolver -> service -> repository

Full list in [docs/project-tech-stack.md](docs/project-tech-stack.md).

## Documents

| Document | Purpose |
|----------|---------|
| [docs/project-proposal.md](docs/project-proposal.md) | What we are building, why, scope, architecture, phases and open decisions |

More docs will be added here as the plan firms up.

## Working agreement

Planning and discussion come first. Code is written only when explicitly asked (see [CLAUDE.md](CLAUDE.md)).

## Related

[java-graphql](../java-graphql) is the earlier library-domain project used to learn Spring for GraphQL. It is unrelated to this one and stays as it is.
