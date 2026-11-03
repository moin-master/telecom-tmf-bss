---
name: api-testing
description: Exercise a running service's GraphQL endpoint with generated payloads and report pass or fail. Use after implementing or changing an API; does not create pytest files.
---

# API testing

Inputs: service name, optional resource.

1. Confirm the host is up: `curl -s http://127.0.0.1:8060/telecom-tmf-bss/<path>/health`. If not, run the restart-all command first.
2. Load payloads from `payloads/<service>/`; run the payload-generation skill if none exist.
3. For each payload send the matching query or mutation with `curl -sS -X POST http://127.0.0.1:8060/telecom-tmf-bss/<path>/graphql -H 'content-type: application/json' -d '{"query": ..., "variables": ...}'`.
4. Check: valid payloads return data and no `errors`; invalid ones return the `_expect` error code; reads return created data; list calls honour offset and limit.
5. Report a table: case, expected, actual, pass or fail. On failure show the response body and the likely cause. Do not edit code unless asked.
