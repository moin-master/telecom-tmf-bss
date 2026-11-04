# Working agreement for code

- CLAUDE.md still applies: no application code until the user says to write code. Running `/implement-tmf-api <service> <api>` counts as that instruction for the named service only.
- No tests until asked. `/test-api` calls the running app and reports; it does not create pytest files unless asked.
- One service and one slice at a time. Slice order: reads, then errors, then writes.
- Stay inside this repository. Never commit `data/`, `.env`, `.run/` or `.venv/`. `specs/` is committed (fixed snapshot, Apache 2.0, see specs/README.md); do not edit its files.
- Do not push, merge or delete branches unless asked. Exception: once a PR is merged, delete its feature branch locally and on the remote.
- Issues and PRs follow the templates in `.github/`: issue with acceptance criteria first, then a feature branch, a commit that lists the criteria covered and how to test, and a PR that closes the issue. No "Generated with" footer.
- When a decision changes, update docs/ (decisions live in docs/project-proposal.md).
- Do not restore or revert content the user removed from docs on purpose; check `git status` first.
