---
name: web-api-client
description: Write typed GraphQL operations for a backend service in /web, generate TypeScript types from the running schema, and handle the TM Forum error shape. Use whenever the UI needs data from, or writes to, an API.
---

# Typed API client for the web app

Backend endpoints (docs/project-routing.md): `/telecom-tmf-bss/<path>/graphql`, for example `product-catalog` and `shopping-cart`. The UI always uses the relative URL; Vite proxies it to port 8060.

## Operations

- Put each operation in `web/src/api/<service>/<name>.graphql`, written against the service's schema. Ask only for the fields the screen shows.
- Use query variables, never string building.
- Wrap each operation in a hook in `web/src/hooks/` (`useQuery` for reads, `useMutation` for writes). Use stable query keys such as `['offerings', filter, offset]`. After a mutation, set the returned cart into the query cache or invalidate it.

## Codegen

1. The backend must be running (`/restart-all`).
2. `codegen.ts` has one entry per service, because services reuse type names (`Money`, `Ref`) with different shapes:
   `schema: 'http://127.0.0.1:8060/telecom-tmf-bss/<path>/graphql'`, `documents: 'src/api/<service>/**/*.graphql'`, output `src/api/generated/<service>/` with the `client` preset.
   Set `presetConfig: { fragmentMasking: false }` (use fragment fields directly) and `config: { useTypeImports: true, scalars: { DateTime: 'string', Decimal: 'string' } }`. Without `useTypeImports` the generated files fail `typecheck` because the Vite template enables `verbatimModuleSyntax`.
3. `npm run codegen` after changing an operation or when the backend schema changes. Commit the generated files.
4. Operation names become exports: `query Offers` gives `OffersDocument` and `OffersQuery`. Pass the document to `client.request(OffersDocument, variables)` and the result is typed.

## Data rules

- Money and other decimals arrive as strings (`"25.00"`). Show them with `Intl.NumberFormat(undefined, { style: 'currency', currency: unit })`. Never add or multiply prices in the browser: totals come from the API (`cartTotalPrice`).
- Dates arrive as ISO 8601 UTC; format them for display only.
- Lists use `offset` and `limit` (default 20, maximum 100). Show a "load more" or page control rather than loading everything.

## Errors

graphql-request throws a `ClientError`. Read `error.response.errors[0].extensions` for `{ code, reason, status }` and `message`. Put one helper in `src/lib/errors.ts` that returns `{ code, status, message }`.

- `NotFound` (404): for an offer, show "not available"; for a cart, drop the stored cart id and start a new cart.
- `BadRequest` (400): show the message next to the control that caused it.
- Network failure: show a retry button.

## Anonymous cart

- The cart id is the visitor's only credential. Keep it in `localStorage` under `bss.cartId`; wrap access in try/catch (it can throw in private windows).
- Create the cart lazily on the first "Add to cart", not on page load.
