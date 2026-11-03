---
name: clone-tmf-spec
description: Clone a TM Forum Open API specification repository into specs/ and summarise its resources, operations and state machine. Use when a service needs the TMF spec before design or implementation.
---

# Clone and read a TM Forum spec

Input: a TMF number (for example `TMF622`).

1. Check `specs/` for a folder starting with the number. If present, it is a fixed snapshot (no `.git`, never pulled; see specs/README.md): skip to step 4.
2. Find the repo: `gh api orgs/tmforum-apis/repos --paginate --jq '.[].name' | grep '^TMF622'`. If several match, list them and ask which.
3. Clone shallow: `git clone --depth 1 https://github.com/tmforum-apis/<repo> specs/<repo>`, then delete the nested `.git`, keep `LICENSE`, and add the spec to specs/README.md. Only clone a new spec when the user asks.
4. Locate the OpenAPI/swagger JSON and any user guide or README in the folder.
5. Report, in at most one screen: spec version, top-level resources, operations per resource, key fields, state values and allowed transitions (from the guide text, not the swagger), notification events.
6. Note any v4 or v5 mismatch with the project's chosen version (see docs/).

Do not copy spec files into the repo outside `specs/`.
