# PRD Artifact Contract

Producer: `prd-authoring`
Consumers: `design-doc`, `pre-coding-check`, `deliver-requirement`, `tzh-review`
Default path: `docs/requirements/<requirement-id>/prd.md`

## Required Fields

- `requirement_id`
- `tapd_id`
- `branch`
- `generated_at`
- `author`
- `background`
- `goals`
- `non_goals`
- `users`
- `business_scope`
- `main_flow`
- `exception_flows`
- `business_rules`
- `permissions`
- `data_metrics`
- `acceptance_criteria`
- `non_functional_requirements`
- `rollback_requirements`
- `release_criteria`
- `unknowns`

## Validation Rules

- Every acceptance criterion must use Given-When-Then or an equivalent checkable format.
- `unknowns` must not be deleted because a field is inconvenient to answer.
- Core business PRDs must include permissions, data metrics, rollback, and release criteria.
