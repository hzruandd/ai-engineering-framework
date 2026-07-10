# BFF Review Checklist

Use when changes touch BFF Controller, VO, permission, aggregation, or downstream calls.

- BFF module is correctly identified.
- Downstream services are called via `@DubboReference`.
- Request and Response VO do not expose internal entities unnecessarily.
- Parameter validation and permission checks are present.
- Error mapping is consistent with frontend/API contract.
- Tenant, parking lot, merchant, and user isolation are preserved.
- BFF tests or `NOT_EXECUTED` evidence are recorded.
