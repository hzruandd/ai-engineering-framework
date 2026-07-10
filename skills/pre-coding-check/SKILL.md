---
name: pre-coding-check
description: Validate PRD and design artifacts before coding. Use before new-crud, new-api, add-field, fix-cache, new-bff, or new-page when coding should consume existing requirement/design outputs.
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[requirement-id] [design-file]"
---

# Pre-coding Check

## Purpose

Prevent unsupported large coding by checking that the PRD, design, acceptance criteria, module, API, DB, permissions, and test strategy are available.

## Inputs

- `docs/requirements/<requirement-id>/prd.md`
- `docs/requirements/<requirement-id>/design.md`
- Optional user-provided target module

## Outputs

- `docs/deliveries/<requirement-id>/tasks.md`
- Gate result with `PASS`, `FAIL`, `WARN`, `UNKNOWN`, `NOT_APPLICABLE`, or `NOT_EXECUTED`

## Checks

1. Requirement ID and TAPD ID exist.
2. Acceptance criteria exist and are testable.
3. Design references the PRD.
4. Target module and project are identified.
5. API contract or Dubbo contract is present when interface changes are required.
6. DB contract is present when tables, fields, SQL, or mapper changes are required.
7. Permission and tenant isolation are addressed for external or BFF changes.
8. Test strategy maps to acceptance criteria.
9. Rollback and verification are present for DB/core changes.

## Blocking Rules

- Core business coding without PRD or design: `FAIL`.
- Missing DB rollback for DB change: `FAIL`.
- Missing test strategy for core acceptance criteria: `UNKNOWN` and stop.
