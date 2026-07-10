# Self-test Report Artifact Contract

Producer: `self-test`
Consumers: `tzh-review`, Test Gate, Release Gate
Default path: `docs/deliveries/<requirement-id>/self-test-report.md`

Required fields:

- requirement_id
- tapd_id
- branch
- commit_sha
- test_type
- command
- environment
- started_at
- finished_at
- status: PASS | FAIL | WARN | UNKNOWN | NOT_APPLICABLE | NOT_EXECUTED
- passed
- failed
- skipped
- coverage
- acceptance_criteria_mapping
- unknowns
- artifacts

Rule: generated test code is not evidence of test pass. Only executed commands with recorded results can be counted as passed.
