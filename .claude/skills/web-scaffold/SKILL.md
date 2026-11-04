---
name: web-scaffold
description: Create the React + TypeScript web app in /web (Vite, router, data fetching, GraphQL codegen, dev proxy to the backend). Use once, when web/ does not exist yet.
---

# Scaffold the web app

The UI lives in `web/` at the repo root. Stack (see docs/project-tech-stack.md): React, TypeScript, Vite, React Router, TanStack Query, graphql-request, GraphQL Code Generator. Plain CSS with variables, no UI framework, until the user asks for one. The look is set by the web-design skill (palette, type, motion); read it before writing styles.

1. Stop if `web/package.json` exists; use web-page-build instead.
2. `npm create vite@latest web -- --template react-ts`, then in `web/`: `npm install`.
3. `npm install react-router-dom @tanstack/react-query graphql graphql-request`
4. `npm install -D @graphql-codegen/cli @graphql-codegen/client-preset`
5. `vite.config.ts`: dev server on port 5173 with a proxy so the browser never calls another origin (the backend has no CORS):
   `server.proxy['/telecom-tmf-bss'] = { target: 'http://127.0.0.1:8060', changeOrigin: true }`
6. Folders under `web/src/`: `api/` (client, generated types, operations per service), `pages/`, `components/`, `hooks/`, `styles/`, `lib/` (format, errors).
7. `src/api/client.ts`: one `GraphQLClient` per service, URL `/telecom-tmf-bss/<path>/graphql` (relative, so the proxy works). Paths come from docs/project-routing.md.
8. `codegen.ts` and `npm run codegen`: see the web-api-client skill. One output folder per service, because services reuse type names such as `Money`.
9. App shell: `QueryClientProvider`, `BrowserRouter`, a header (brand, nav, cart link with item count) and a footer, routes for `/`, `/offers/:id`, `/cart`, and a 404 route.
10. Scripts in `package.json`: `dev`, `build`, `typecheck` (`tsc -p tsconfig.app.json --noEmit`; the Vite template uses project references, so plain `tsc -b --noEmit` does not fit), `codegen` (`graphql-codegen --config codegen.ts`).
    Run with `npm create vite@latest web -- --template react-ts --no-interactive` so it does not prompt.
11. Add `web/node_modules/`, `web/dist/` and `*.tsbuildinfo` to `.gitignore`. Commit generated types so a build does not need the backend.
12. Verify with the web-verify skill, then report what was created.

Do not add a test framework, state library or CSS framework unless asked.
