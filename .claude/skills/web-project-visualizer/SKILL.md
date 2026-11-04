---
name: web-project-visualizer
description: Add an "Explore" section to the web app that visualizes the project: service health, API operations from live schemas, module dependencies and events, and spec coverage. Use when the user wants to see the APIs and the project in the UI.
---

# Project visualizer ("Explore" section)

A developer-facing area of the web app, under `/explore`, separate from the customer pages. It reads live data where it can and static project data otherwise. Each view is small; add them one at a time.

| View | Route | Source |
|------|-------|--------|
| Service board | `/explore` | `GET /telecom-tmf-bss/health` (lists mounted services) and each `GET /telecom-tmf-bss/<path>/health`; show UP or DOWN, path, TMF number and a link to the service's GraphiQL |
| API catalogue | `/explore/apis/:service` | GraphQL introspection (`__schema`) of that service: queries, mutations, their arguments and return types, grouped and searchable |
| Try it | inside the API catalogue | a small form per operation that runs it against the service and shows the JSON response and `errors` extensions |
| Dependency map | `/explore/map` | modules and `Depends on` from docs/project-architecture.md, drawn as an SVG graph; implemented services highlighted, planned ones greyed |
| Event flow | `/explore/events` | event table from docs/project-architecture.md section 4: publisher, consumers, effect |
| Spec coverage | `/explore/specs` | table of the 15 TMF APIs from specs/README.md: version kept, service status (implemented / planned) |

## How

1. Static project data (dependencies, events, spec list) goes in `web/src/data/project.ts`, copied from the docs once. Update it in the same change as the docs; add a comment naming the source doc.
2. The service list for the board comes from the host health endpoint, so a newly mounted service appears without UI changes. Map a path to its TMF number with the static table.
3. Introspection uses a plain `fetch` of the standard introspection query; do not generate types for it.
4. Draw the map with inline SVG laid out in columns by dependency depth. No graph library unless asked.
5. Follow web-page-build for states and conventions, and web-api-client for errors.
6. Verify with web-verify.
