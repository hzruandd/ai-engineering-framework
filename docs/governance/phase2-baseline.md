# Phase 2 Baseline

Updated: 2026-07-10
Branch at start: `feat/ai-coding-engineering-v1`
Implementation branch: `feat/ai-coding-engineering-phase2`

## Git State

- Existing untracked items before phase 2 included `docs/` and `test.md`.
- These were treated as user/workspace changes and not deleted.
- Recent HEAD: `021d9e8 Merge #2 into master from release/v1.1.0`.

## Current Asset Structure

| Asset | Current location | Notes |
| --- | --- | --- |
| Global rules | `global-settings/.claude/CLAUDE.md` | Contains canonical CommonMapper rule |
| Commands | `commands/`, `global-settings/.claude/commands/` | Duplicate command copies exist for installation compatibility |
| Skills | `skills/*/SKILL.md` | 22 existing Skills plus phase 2 additions |
| Project templates | `project-templates/tzh-parkinglot` | Parking project context |
| MCP docs | `mcp/` | Playwright, Fetch, MySQL, Sequential Thinking |
| Review gate | `skills/tzh-review` | Protected high-value formal review asset |

## Confirmed Issues

- `formal-review` contained language that favored pass decisions and P0 avoidance.
- Active CRUD and Java guide assets still referenced `BaseMapper`.
- Coverage thresholds existed in multiple places.
- No single quality threshold config existed.
- PRD, pre-coding, BFF, frontend, Gate, and artifact contracts were missing.
- Validation scripts were missing.

## Protected Assets

- `skills/tzh-review`
- DB review checklists
- Security review checklists
- Business domain review checklist
- v1.4 review report template
- `db-sql-gate -> db-sql-review` progressive loading pattern
- Existing parking domain project template

## Implementation Scope

This phase implements minimum executable assets and conflict fixes. Deep rewrites of all legacy command copies and all generated examples are deferred where a canonical source plus validator can prevent drift.
