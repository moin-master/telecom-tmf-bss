# CLAUDE.md

Telecom BSS: a proof of concept of a telecom business support system using TM Forum Open APIs, GraphQL and SQLite. See README.md and docs/project-proposal.md.

## Working agreement

- This project is in the **planning** stage. Discuss and write documents first.
- **Do not write application code (Python, schema, SQL, build files) until the user explicitly says to start writing code.** Showing code in chat for review is also only done when asked.
- Do not write tests until asked.
- Keep it simple and incremental; reads first, then errors, then writes.

## Intended stack (once coding starts)

Listed in docs/project-tech-stack.md (Python 3.12+, FastAPI, Strawberry, SQLAlchemy, SQLite). Layering: GraphQL resolver -> service -> repository. Modules never access another module's repositories.
