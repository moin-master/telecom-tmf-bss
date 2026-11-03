Closes #

## Summary

<!-- What changed and why, in two or three sentences. -->

## Acceptance criteria

<!-- Copy from the issue and tick what is done and verified. -->

- [ ] AC1
- [ ] AC2

## How to test

```bash
uv sync
uv run uvicorn bss_host.main:app --host 127.0.0.1 --port 8060
```

<!-- Exact queries or commands and the expected result. -->

## Notes

<!-- Decisions made, spec fields skipped, out of scope, follow-ups. -->

## Checklist

- [ ] Docs updated if a decision changed (`docs/`)
- [ ] Only the named service and its client are touched; no cross-service imports of models or repositories
- [ ] Money is `Decimal` and timestamps are UTC
- [ ] No database files, `.env` or `.run/` committed
