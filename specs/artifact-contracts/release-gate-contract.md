# Release Gate Artifact Contract

Producer: Release Gate
Consumers: release owner, operations, `tzh-review`
Default path: `docs/deliveries/<requirement-id>/release-gate.md`

Required fields:

- requirement_id
- tapd_id
- branch
- commit_sha
- review_report
- build_result
- test_result
- db_sql_result
- security_result
- deployment_plan
- rollback_plan
- post_release_verification
- approver
- status
- unknowns
- blockers
- waivers
