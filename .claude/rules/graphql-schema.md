---
paths:
  - "services/**/schema.py"
  - "host/**/combined.py"
---

# GraphQL schema rules

- Strawberry, code-first. One schema per service, served at `/<path>/graphql`; the combined schema is at `/graphql`.
- Type and field names follow the TM Forum resource names in camelCase (`ProductOrder`, `orderItem`, `billingAccount`). Do not rename for taste.
- Ids are readable strings (for example `CUS-1001`). Every resource has `id`; `href` is derived, not stored.
- Links to another service's resource are fields that resolve through that service's `client`, not copied data.
- Queries: `<resource>(id)` and `<resource>List(offset, limit, filter)`. Mutations: `create<Resource>`, `patch<Resource>`, `delete<Resource>`. Offset/limit pagination.
- `@type` / `@baseType` polymorphism, free-form characteristics and PATCH semantics follow the single policy written in docs/; do not decide per service.
- Errors use one shape (code, reason, message, status) as in TM Forum error responses, defined once in `shared`.
- Reads first, then errors, then writes: no mutations before the read slice for the service exists.
