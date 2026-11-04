---
name: web-page-build
description: Build or extend a page or feature of the React web app in /web from an existing API, following the pages roadmap and UI conventions. Use for home page, offer detail, cart and later screens.
---

# Build a page

Input: the screen or feature (for example "home page of offers"). Use web-api-client for data. The backend API must exist first; if it does not, say so and stop.

## Steps

1. Read docs/project-routing.md and the service's `schema.py` for the fields available.
2. Write the `.graphql` operations and run codegen (web-api-client).
3. Build the page in `src/pages/`, with reusable parts in `src/components/`. One component per file.
4. Handle all four states on every data view: loading (skeleton), error (message and retry), empty (helpful text) and data.
5. Wire the route in `src/App.tsx` and the nav link if it is a top-level page.
6. Check with web-verify, then report what was built and what is missing.

## Pages roadmap

Implement only the pages whose APIs exist. Add the next row when the backend feature is merged.

| Page | Route | API | Status |
|------|-------|-----|--------|
| Home: grid of offers | `/` | `productOfferingList`, `categoryList` | first |
| Offer detail | `/offers/:id` | `productOffering` | with home |
| Cart | `/cart` | `shoppingCart`, `addCartItem`, `removeCartItem` | with home |
| Checkout, orders | later | order service | when built |
| Account, bills, usage | later | customer, billing, usage | when built |

### Home page

- A grid of offer cards: name, short description, category, a price summary (monthly fee and one-time fee, taken from `productOfferingPrice`), and an "Add to cart" button.
- Controls: search by name (`filter.name`), category chips (`categoryList`, filter `categoryId`), "load more" using `offset` and `limit`.
- Clicking a card opens the offer detail page (specification characteristics, all prices, categories, add to cart with quantity).
- The header cart link shows the item count and goes to `/cart`.

### Cart page

- Lines with name, quantity, line price, remove button; totals from `cartTotalPrice`, one-time and per month shown separately.
- Empty cart shows a link back to the offers.
- Checkout is a disabled placeholder until the order service exists.

## UI conventions

Read the web-design skill first: the storefront is clean and minimal, lemon yellow on white or blackish gray, and every page must pass its per-page checklist and guardrails.

- Mobile-first layout with CSS grid, 16 px page gutters, no horizontal scroll at phone width.
- Colours, spacing, radius, shadows and motion as CSS variables in `src/styles/tokens.css`.
- Semantic HTML, labels on inputs, buttons for actions and links for navigation. Do not rely on colour alone.
- Show prices with the currency, exactly as the API returns them.
- Filters, search and sort that live in the URL must keep the scroll position: pass `preventScrollReset: true` to `setSearchParams` (and to `navigate` or `Link`) for in-page changes. Without it the router scrolls to the top on every URL change. Navigating to a different page should still scroll to the top.
- Do not add libraries for things CSS or the platform can do.
- After the first version, look at it (web-verify), then revise at least once before reporting.
