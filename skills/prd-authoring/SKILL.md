---
name: prd-authoring
description: Create or improve Tingzhihui parking-domain PRDs with structured scope, user stories, business rules, Given-When-Then acceptance criteria, rollout and rollback requirements. Use before design or coding when a requirement is vague or lacks a PRD artifact.
allowed-tools: Read, Glob, Grep, Write, Edit
argument-hint: "[requirement-id] [tapd-id]"
---

# PRD Authoring

## Inputs

- Raw requirement or TAPD summary
- Existing business context
- Optional target project/module

## Outputs

- `docs/requirements/<requirement-id>/prd.md`
- Unknown list for product confirmation

## Required Sections

Use `templates/city-parking-prd-template.md`.

The PRD must include background, goals, non-goals, user roles, business scope, main flow, exception flows, business rules, permissions, data metrics, user stories, Given-When-Then acceptance criteria, non-functional requirements, compatibility, rollout, rollback, telemetry, risks, release criteria, and unknowns.

## Failure Handling

If business scope, acceptance criteria, or permissions cannot be confirmed, write `Unknown` and route to PRD Gate. Do not invent business rules.
