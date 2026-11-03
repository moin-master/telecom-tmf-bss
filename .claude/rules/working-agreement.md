# Working agreement for code

- CLAUDE.md still applies: no application code until the user says to write code. Running `/implement-tmf-api <service> <api>` counts as that instruction for the named service only.
- No tests until asked. `/test-api` calls the running app and reports; it does not create pytest files unless asked.
- One service and one slice at a time. Slice order: reads, then errors, then writes.
- Stay inside this repository. Never commit `data/`, `.env`, `specs/`, `.run/` or `.venv/`.
- Do not push, merge or delete branches unless asked.
- When a decision changes, update docs/ (decisions live in docs/project-proposal.md).
- Do not restore or revert content the user removed from docs on purpose; check `git status` first.
