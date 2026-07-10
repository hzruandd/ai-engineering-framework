# Test Evidence Review Checklist

Use for build, unit test, integration test, self-test, coverage, and CI evidence.

- Evidence includes command, environment, start/end time, status, and artifact path.
- Acceptance criteria map to test cases.
- Generated tests are distinguished from executed tests.
- Critical tests with `NOT_EXECUTED` block formal PASS unless there is an approved waiver.
- Core `UNKNOWN` test evidence is at least `P1`.
- Coverage is checked against `config/quality-thresholds.yaml`.
