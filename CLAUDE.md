# CLAUDE.md

Telecom BSS: a proof of concept of a telecom business support system using TM Forum Open APIs, GraphQL (Spring for GraphQL) and H2. See README.md and docs/project-proposal.md.

## Working agreement

- This project is in the **planning** stage. Discuss and write documents first.
- **Do not write application code (Java, schema, SQL, build files) until the user explicitly says to start writing code.** Showing code in chat for review is also only done when asked.
- Do not write tests until asked.
- Keep it simple and incremental; reads first, then errors, then writes.

## Decisions

The decision list lives in docs/project-proposal.md (section 9). Update it there when a decision is made rather than recording it here.

## Intended stack (once coding starts)

Java 21, Spring Boot, Spring for GraphQL, Spring Data JPA, H2, Lombok. Layering: GraphQL controller -> service -> repository. Modules never access another module's repositories.
