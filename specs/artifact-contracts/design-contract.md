# Design Artifact Contract

Producer: `design-doc`
Consumers: `pre-coding-check`, coding Skills, test Skills, `tzh-review`
Default path: `docs/requirements/<requirement-id>/design.md`

## Required Fields

- `requirement_id`
- `tapd_id`
- `branch`
- `commit_sha` or `Unknown`
- `source_prd`
- `domain_model`
- `state_machine`
- `api_contracts`
- `dubbo_contracts`
- `database_changes`
- `cache_changes`
- `mq_events`
- `permissions`
- `error_codes`
- `observability`
- `test_strategy`
- `rollback_plan`
- `task_breakdown`
- `unknowns`

## API Contract Rule

HTTP/BFF APIs should use OpenAPI 3.x. Internal Dubbo contracts must use an explicit Dubbo contract section and must not be disguised as HTTP APIs.
