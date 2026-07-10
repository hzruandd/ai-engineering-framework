# Design Review Checklist

Use when a technical design artifact exists or should exist.

- Design references the PRD.
- Domain model, state changes, API/Dubbo contracts, DB changes, cache, MQ, permissions, error codes, observability, tests, and rollback are covered where applicable.
- HTTP/BFF contracts use OpenAPI 3.x where possible.
- Dubbo internal contracts are not disguised as HTTP APIs.
- Missing design evidence for core changes is at least `P1` until confirmed.
