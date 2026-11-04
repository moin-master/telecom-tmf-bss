---
paths:
  - "services/**/*.py"
  - "host/**/*.py"
  - "shared/**/*.py"
  - "tests/**/*.py"
---

# Python code rules

- Python 3.12+, type hints everywhere.
- Money is `decimal.Decimal`, never float. Timestamps are timezone-aware UTC `datetime`.
- Layering inside a service: resolver (`schema.py`) -> `service.py` -> `repository.py`. Resolvers hold no business logic; repositories hold no rules.
- A service never imports another service's `models`, `repository` or `service`. It imports only the other service's `client` and passes ids and plain values.
- Each service owns its Mongita database folder. No shared collections, no cross-database queries.
- Events go through `shared` (blinker). Publish after the state change is committed; consumers call their own `service.py`.
- State machines (order, product, ticket) live in `service.py`; reject illegal transitions with the shared TM Forum style error.
- No global mutable state except the engine and event signals.
- Add dependencies with `uv add --package <name>`, never `pip install`.
- Keep functions short and names plain. Match the comment density of surrounding code; comment the why, not the what.
- Lint and format with Ruff once configured: `uv run ruff check` and `uv run ruff format`.
