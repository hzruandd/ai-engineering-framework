---
name: new-bff
description: Create or modify BFF API layers for city-parking projects. Use for RestController, Request/Response VO, validation, permissions, DubboReference calls, DTO/VO conversion, aggregation, OpenAPI, and BFF tests.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
argument-hint: "[requirement-id] [api-name]"
---

# New BFF

## Inputs

- PRD and design artifacts
- OpenAPI contract
- Downstream Dubbo contract
- Existing project conventions

## Outputs

- Controller, Request VO, Response VO
- Validation and permission checks
- `@DubboReference` downstream call
- DTO/VO conversion
- Error mapping
- OpenAPI update
- Unit or BFF interface tests
- Test evidence or `NOT_EXECUTED`

## Rules

- Identify the real BFF module before generating code.
- Do not add HTTP controllers to downstream services.
- Keep Controller thin; aggregation and conversion may live in BFF service/application layer according to project convention.
- Preserve tenant, parking lot, merchant, and user permission boundaries.

## Validation

Run build and relevant tests when available. If not available, write `NOT_EXECUTED` evidence and pass it to `tzh-review`.
