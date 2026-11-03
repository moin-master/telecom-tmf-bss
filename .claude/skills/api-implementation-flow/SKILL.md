---
name: api-implementation-flow
description: End-to-end flow for implementing one TM Forum API in one service, from spec to tested slice. Use when implementing or extending a service.
---

# API implementation flow

Input: service name and TMF API (for example `order TMF622`) and slice (default: reads).

1. **Confirm scope.** Check the service in docs/project-routing.md and its dependencies in docs/project-architecture.md. Note which other services it needs (their `client` must exist or be stubbed).
2. **Spec.** Run the clone-tmf-spec skill.
3. **Scaffold.** If `services/<name>` is missing, run the scaffold-service skill.
4. **Schema.** Run the graphql-schema-design skill for the slice and show the table. Wait for approval on a first slice of a new service.
5. **Models, repository, service, client.** Implement in that order following `.claude/rules/python-code.md`. State machines come from the spec text.
6. **Resolvers.** Implement `schema.py`, wire into `create_app()`.
7. **Seed.** Add `seed.py` rows; load at startup.
8. **Payloads and test.** Run payload-generation, restart the host, run api-testing.
9. **Report.** Summarise files changed, skipped spec fields, test results, open questions. Update docs/ if a decision was made.

Slice order: reads, then errors, then writes. Stop after each slice.
