# Working agreement for code

## Pipeline for every new requirement

Any new requirement, however small, goes through these steps in order. Stop at the end of each step and wait for the user before the next one.

1. **TMF check.** Read the relevant spec in `specs/` (not memory) and report what TM Forum defines for it: resources, fields, allowed values, examples. Say where the spec is silent or differs from the request.
2. **TMF-based proposal.** Turn the check and the user's answers into a proposal: the decision recorded in docs/ (decisions live in docs/project-proposal.md), the schema design table, and the planned code changes (services, files, slice, skipped spec fields). Open points are listed with a suggested default. Create the GitHub issue only after the user agrees.
3. **Approval.** The user approves the proposal, or says to start writing code. A vague "ok" is not approval for code; ask once.
4. **Code.** Implement only what the proposal says, one service and one slice. Leave the changes uncommitted in the working tree, list the files to review, and report test results.
5. **Review, then commit.** The user reviews the code. Commit, push and PR only when the user asks.

- CLAUDE.md still applies: no application code until the user says to write code. Running `/implement-tmf-api <service> <api>` counts as that instruction for the named service only, and only after steps 1 to 3 are done for that requirement.
- No tests until asked. `/test-api` calls the running app and reports; it does not create pytest files unless asked.
- One service and one slice at a time. Slice order: reads, then errors, then writes.
- Stay inside this repository. Never commit `data/`, `.env`, `.run/` or `.venv/`. `specs/` is committed (fixed snapshot, Apache 2.0, see specs/README.md); do not edit its files.
- Do not push, merge or delete branches unless asked. Exception: once a PR is merged, delete its feature branch locally and on the remote.
- Issues and PRs follow the templates in `.github/`: issue with acceptance criteria first, then a feature branch, a commit that lists the criteria covered and how to test (written when the user asks for the commit), and a PR that closes the issue. No "Generated with" footer.
- When a decision changes, update docs/ (decisions live in docs/project-proposal.md).
- Do not restore or revert content the user removed from docs on purpose; check `git status` first.
