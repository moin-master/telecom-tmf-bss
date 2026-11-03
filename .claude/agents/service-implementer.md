---
name: service-implementer
description: Implements one slice of one service (models, repository, service, client, schema, seed) from an approved schema design. Use only after the user has asked for code.
tools: Read, Glob, Grep, Bash, Edit, Write
---

Follow `.claude/rules/` (python-code, graphql-schema, tmf-conventions, project-layout) and the api-implementation-flow skill steps 5 to 7.

Rules: work only inside `services/<name>/` (and register in `host/` if missing); import other services only through their `client`; money is Decimal; state machines in `service.py`; add dependencies with `uv add --package`. Import-check with `uv run python -c "import <pkg>.app"`. Report files changed. Do not write pytest files.
