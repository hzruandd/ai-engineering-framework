# Phase 2 Remediation Tracker

Updated: 2026-07-10

| ID | Source | Issue | Priority | Files | Exists now | External practice basis | Decision | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P0-1 | review | Missing PRD/UI starting artifacts | P0 | `skills/prd-authoring`, `specs/artifact-contracts` | Yes | SDD, spec-kit | Add minimum PRD and UI contract path | FIXED | Added PRD Skill and PRD/design contracts |
| P0-2 | review | No true TDD mode | P0 | `skills/generate-tests`, `WORKFLOW.md` | Yes | Meituan TDD | Add TDD rules and evidence contract | PARTIALLY_FIXED | Workflow and contracts added; deep Skill rewrite deferred |
| P0-3 | review | Missing BFF/frontend minimum assets | P0 | `skills/new-bff`, `skills/new-page` | Yes | full-stack AI delivery | Add minimum Skills | FIXED | Added BFF and page Skills |
| P0-4 | review | Formal review conflict | P0 | `commands/formal-review.md`, `commands/tzh-review.md` | Yes | evidence-first review | Make `tzh-review` sole formal decision source | FIXED | `formal-review` now summary/format only |
| P0-5 | review | Review does not consume test evidence | P0 | `specs/artifact-contracts`, `skills/tzh-review` | Partially | Quality Gate | Add test/self-test contracts | PARTIALLY_FIXED | Contracts added; full auto-discovery requires later Skill tuning |
| P0-6 | review | Design and coding lack contract | P0 | `specs/artifact-contracts`, `skills/pre-coding-check` | Yes | spec-kit | Add artifact contracts and pre-coding check | FIXED | Added contracts and Skill |
| P0-7 | review | CommonMapper/BaseMapper conflict | P0 | `rules/java-mapper-rule.md`, Java docs and templates | Yes | single source of truth | CommonMapper is canonical | FIXED | Added rule and updated active templates |
| P0-8 | review | Missing quantifiable Gate | P0 | `config/quality-thresholds.yaml`, `gates/` | Yes | CI/Gate practice | Add threshold config and Gate enum | FIXED | Added config and Gate model |
| G-1 | review | Duplicate command sources | P1 | `commands/`, `global-settings/.claude/commands/` | Yes | canonical source | Keep compatible copies, validate drift | PARTIALLY_FIXED | Validation script checks duplicate command drift |
| G-2 | review | Skill metadata and permission drift | P1 | `skills/*/SKILL.md` | Yes | Skill engineering | Add validator | PARTIALLY_FIXED | Added validation script |
| G-3 | review | CI examples missing | P1 | `ci/examples/jenkins` | Yes | CI Gate | Add Jenkins example | FIXED | Added example Jenkinsfile |
| G-4 | review | Validation script missing | P1 | `scripts/validate-assets.ps1`, `scripts/validate-skills.ps1` | Yes | deterministic checks | Add PowerShell checks | FIXED | Added scripts |
