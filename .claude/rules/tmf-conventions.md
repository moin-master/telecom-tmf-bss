# TM Forum conventions

- The spec snapshot in `specs/<repo>/` (v5 `*.oas.yaml`; v4 swagger JSON for TMF641, TMF676, TMF700) is the source of truth. Read it before designing a service; do not rely on memory for fields. Details and licence: specs/README.md.
- Specs come from the `tmforum-apis` GitHub organisation. Repository names start with the TMF number, for example `TMF620_ProductCatalog`.
- The snapshot is not updated. The v5 versus v4 choice for TMF641, TMF676 and TMF700 is still open; ask before designing those services.
- State machines are defined by the spec text, not the swagger files.
- Keep TM Forum names and structure for resources the scenario uses; skip fields it does not need and list the skipped fields in the service's notes.
- Events mirror TM Forum notification names (for example `ProductOrderStateChangeEvent`) but are in-process signals.
- Record each spec decision once, in docs/, not in code comments.
