# TM Forum conventions

- The cloned spec in `specs/<repo>/` (swagger/OpenAPI JSON plus user guide) is the source of truth. Read it before designing a service; do not rely on memory for fields.
- Specs come from the `tmforum-apis` GitHub organisation. Repository names start with the TMF number, for example `TMF620_ProductCatalog`.
- Spec version (v4 or v5) is an open decision. Do not mix versions. If it is not recorded in docs/, ask before the first clone.
- State machines are defined by the spec text, not the swagger files.
- Keep TM Forum names and structure for resources the scenario uses; skip fields it does not need and list the skipped fields in the service's notes.
- Events mirror TM Forum notification names (for example `ProductOrderStateChangeEvent`) but are in-process signals.
- Record each spec decision once, in docs/, not in code comments.
