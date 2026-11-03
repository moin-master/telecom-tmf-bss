---
name: payload-generation
description: Generate realistic sample request payloads and seed rows for a TM Forum resource from its spec. Use for API testing and seed data.
---

# Generate test payloads

Inputs: service name, resource, optional count.

1. Read the resource schema in the service's spec under `specs/` and the service's `schema.py` if it exists.
2. Produce JSON payloads in the GraphQL input shape (camelCase, TM Forum names) with valid values: readable ids (`CUS-1001`), ISO 8601 UTC timestamps, `Decimal` amounts as strings with two decimals, valid enum states.
3. Generate three kinds: `valid-minimal`, `valid-full`, and `invalid-*` (missing required field, wrong enum, illegal state transition). Invalid ones carry the expected error code in a `_expect` field.
4. References to other services use ids that exist in their seed data; check `seed.py` of the target service.
5. Save to `payloads/<service>/<resource>-<kind>.json`. Print the list of files created.
