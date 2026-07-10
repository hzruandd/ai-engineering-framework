# Gate Model

Version: 1.0.0
Updated: 2026-07-10

This directory defines the shared Gate model used by PRD, design, pre-coding, build, test, security, DB/SQL, review, and release checks.

## Result Enum

| Result | Meaning | Default handling |
| --- | --- | --- |
| PASS | Evidence satisfies the gate | Continue |
| FAIL | Blocking condition is observed | Stop |
| WARN | Non-blocking issue or waiver candidate | Continue only with recorded owner |
| UNKNOWN | Required evidence cannot be confirmed | Stop for core gates |
| NOT_APPLICABLE | Gate does not apply to this change | Continue |
| NOT_EXECUTED | Gate was not run | Stop for required gates |

## Required Fields

Every gate result must include:

- `gate_id`
- `requirement_id`
- `tapd_id`
- `branch`
- `commit_sha` or `Unknown`
- `status`
- `evidence`
- `unknowns`
- `blockers`
- `waivers`
- `owner`
- `generated_at`

## Required Gates

| Gate | Purpose | Blocking examples |
| --- | --- | --- |
| PRD Gate | Validate requirement completeness | Missing acceptance criteria |
| UI Gate | Validate interaction contract | Missing page state for frontend change |
| Design Gate | Validate technical design | Missing API/DB contract |
| Pre-coding Gate | Stop unsupported large coding | Missing module, table, interface, or test strategy |
| Build Gate | Verify compile/build | Build failed or not executed |
| Test Gate | Verify test evidence | Critical tests not executed |
| Security Gate | Verify security controls | Auth, tenant isolation, or sensitive-data issue |
| DB/SQL Gate | Verify database changes | Dangerous DDL/DML without rollback |
| Review Gate | Formal quality decision | P0 or unresolved P1 |
| Release Gate | Release readiness | Unknown rollback, deployment, or verification plan |
