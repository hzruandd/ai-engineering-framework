# Review Report Artifact Contract

Producer: `tzh-review`
Consumers: release approver, QA, delivery owner
Default path: `docs/deliveries/<requirement-id>/review-report.md` or `智慧停车生态_代码评审报告_v1.4_<date>.md`

Required fields:

- requirement_id
- tapd_id
- branch
- baseline
- commit_sha
- diff_scope
- evidence_table
- test_evidence
- db_evidence
- security_evidence
- risks
- unknowns
- decision
- action_items
- release_conditions

Decision rule: `tzh-review` is the only formal quality decision source for Tingzhihui release review.
