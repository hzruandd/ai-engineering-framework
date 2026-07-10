# Acceptance Criteria Guide

Use checkable criteria. Prefer Given-When-Then:

```text
Given a monthly-card user has an active contract
When the user renews for one month
Then the system extends the end date by one calendar month and records a payment trace.
```

Every core criterion must map to at least one test case in `test-plan-contract.md`.
