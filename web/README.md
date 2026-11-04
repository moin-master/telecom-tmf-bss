# VIBE mobile (web)

React + TypeScript storefront for the Telecom BSS APIs. Offers and prices are read live from the product-catalog service; the cart uses the shopping-cart service. No login: the cart id is kept in `localStorage`.

## Run

The backend must be running first (`uv run uvicorn bss_host.main:app --host 127.0.0.1 --port 8060` from the repo root).

```bash
cd web
npm install
npm run dev        # http://127.0.0.1:5173
```

The dev server proxies `/telecom-tmf-bss` to the backend, so the browser never calls another origin.

## Scripts

| Script | What it does |
|--------|--------------|
| `npm run dev` | dev server on port 5173 |
| `npm run build` | typecheck and production build into `dist/` |
| `npm run typecheck` | TypeScript check only |
| `npm run codegen` | regenerate GraphQL types from the running backend (`src/api/generated/`, committed) |
| `npm run lint` | oxlint |

## Layout

- `src/api/` GraphQL client, `.graphql` operations per service, generated types
- `src/hooks/` data hooks (offers, cart)
- `src/pages/` Home, Offer detail, Cart
- `src/components/` UI pieces
- `src/styles/` design tokens and CSS
- `src/lib/` formatting, errors, category themes

Design direction: `.claude/skills/web-design/SKILL.md` (lemon yellow on white and blackish gray).
