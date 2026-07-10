# Phase 2 Change Report

Updated: 2026-07-10

## 1. Executive Summary

Phase 2 established a minimum AI Coding delivery loop from PRD to release gate while preserving existing high-value assets, especially `tzh-review`.

Resolved P0 items:

- Formal review decision conflict.
- CommonMapper/BaseMapper active-template conflict.
- Missing quality threshold source.
- Missing artifact contracts and Gate model.
- Missing PRD, pre-coding, BFF, frontend, and workflow entry assets.

Partially resolved:

- Full automatic consumption of all test evidence by `tzh-review` requires deeper Skill enhancement after pilot evidence format stabilizes.
- Duplicate command copies remain for install compatibility, guarded by validation.

## 2. File Change Summary

| File | Operation | Reason |
| --- | --- | --- |
| `config/quality-thresholds.yaml` | Added | Single quality threshold source |
| `rules/java-mapper-rule.md` | Added | Canonical Mapper rule |
| `gates/README.md` | Added | Shared Gate result model |
| `specs/artifact-contracts/*` | Added | PRD/design/task/test/review/release contracts |
| `WORKFLOW.md` | Added | End-to-end workflow |
| `skills/prd-authoring` | Added | PRD minimum capability |
| `skills/pre-coding-check` | Added | Pre-coding gate |
| `skills/new-bff` | Added | BFF capability |
| `skills/new-page` | Added | Frontend capability |
| `skills/deliver-requirement` | Added | Workflow orchestration |
| `commands/deliver-requirement.md` | Added | Thin workflow entry |
| `scripts/validate-assets.ps1` | Added | Deterministic validation |
| `scripts/validate-skills.ps1` | Added | Skill metadata validation |
| `ci/examples/jenkins/Jenkinsfile` | Added | CI integration example |

## 3. Key Decisions

- `tzh-review` remains the formal quality decision source.
- `formal-review` cannot change risk grade, Unknowns, or final decision.
- `CommonMapper` is the Mapper canonical rule.
- `config/quality-thresholds.yaml` is the threshold source.
- `UNKNOWN` and `NOT_EXECUTED` are never equivalent to `PASS`.
- AI can prepare evidence, but QA/release owners retain final human sign-off.

## 4. Remaining Work

- Pilot the workflow on real business changes.
- Connect project CI outputs into `self-test-report-contract.md`.
- Extend `tzh-review` auto-discovery of evidence once real report paths stabilize.
- Decide whether to add AGENTS.md compatibility templates in a later, focused change.
