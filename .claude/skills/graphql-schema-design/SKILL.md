---
name: graphql-schema-design
description: Derive a Strawberry GraphQL schema for a service from its TM Forum spec and the project's schema rules. Use before writing schema.py.
---

# Design the GraphQL schema from a spec

Inputs: service name, TMF number, slice (reads, errors or writes).

1. Read `.claude/rules/graphql-schema.md` and the service's spec in `specs/`.
2. List the resources the scenario needs (docs/project-proposal.md section 3). Drop the rest.
3. For each resource write: type name, fields with GraphQL types, which fields are references to other services (resolved through their `client`), enum values for state.
4. For the reads slice define `<resource>(id)` and `<resource>List(offset, limit, filter)`. Add create/patch/delete only for the writes slice.
5. Define input types for filters and mutations separately from output types.
6. Output a table in the reply (type, field, GraphQL type, source) plus a list of spec fields skipped and why. Do not write code unless the user asked for implementation.
