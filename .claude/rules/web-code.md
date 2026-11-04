---
paths:
  - "web/**"
---

# Web code rules

- React with TypeScript in strict mode. No `any`; use generated GraphQL types.
- Function components and hooks only. One component per file, named like the file.
- Server data goes through TanStack Query hooks in `src/hooks/`. Components do not call `fetch` or the GraphQL client directly.
- GraphQL operations live in `.graphql` files; generated code is committed and never edited by hand.
- The UI calls the backend through the relative URL `/telecom-tmf-bss/...` (Vite proxy). No hard-coded host or port, no CORS workarounds.
- Money is a string from the API. Display only; never do arithmetic on prices in the browser.
- The anonymous cart id is stored in `localStorage` (`bss.cartId`) inside try/catch.
- No secrets in the web code. Nothing in `web/` reads `.env` files from the backend.
- Accessibility basics on every screen: semantic elements, labels, focus styles, keyboard use, `prefers-reduced-motion` respected.
- Visual design follows the web-design skill: clean and minimal, lemon yellow (#FFF700) on white or blackish gray, always dark text on lemon.
- Add a dependency only when the platform or existing libraries cannot do the job; say why in the PR.
- No tests until the user asks (same as the backend).
