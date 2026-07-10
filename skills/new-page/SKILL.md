---
name: new-page
description: Create or modify frontend pages for city-parking projects after detecting the actual frontend stack. Use for Vue, TypeScript, admin console, WeChat mini-program pages, API binding, page states, validation, tests, and UI acceptance checklist.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
argument-hint: "[requirement-id] [page-name]"
---

# New Page

## Inputs

- PRD
- UI/interaction contract
- OpenAPI contract
- Existing frontend project conventions

## Outputs

- Page/component files matching the detected stack
- API client integration
- Loading, empty, error, disabled, and permission states
- Form validation
- Telemetry checklist
- Unit/E2E checklist or tests
- Manual UI acceptance checklist

## Rules

- Detect stack before writing code. Do not generate generic React/Vue code that does not match the target project.
- If visual assets or Figma mapping are missing, record required assets and manual UI checks. Do not claim visual completion.
- Prefer existing components and API utilities.

## Failure Handling

- If the frontend project or stack cannot be identified, stop and return `UNKNOWN`.
- If tests or build cannot run in the current environment, record `NOT_EXECUTED`, the attempted command, and the reason.
- Do not claim visual, accessibility, or E2E readiness without evidence or explicit manual acceptance items.
