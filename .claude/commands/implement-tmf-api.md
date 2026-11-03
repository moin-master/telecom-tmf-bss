---
description: Implement a TM Forum API in a service, one slice at a time
argument-hint: <service> <TMF number> [reads|errors|writes]
---

The user is explicitly asking to write code for this service only.

Parse $ARGUMENTS as: service name, TMF number, optional slice (default reads). Check the service name and TMF number match docs/project-routing.md; if they do not, stop and say so.

Follow the api-implementation-flow skill. Use the orchestrator agent when the service has dependencies that are not implemented yet; otherwise work directly.
