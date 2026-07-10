# Phase 2 Migration Map

Updated: 2026-07-10

| Current file | Issue | Operation | Target/canonical source | Compatibility | Risk |
| --- | --- | --- | --- | --- | --- |
| `commands/formal-review.md` | Could weaken formal review | Rewrite role boundary | `skills/tzh-review` | Keep command name as summary entry | Low |
| `global-settings/.claude/commands/formal-review.md` | Duplicate weak rules | Rewrite role boundary | `skills/tzh-review` | Keep install copy | Low |
| `commands/new-crud.md` | BaseMapper conflict | Update in place | `rules/java-mapper-rule.md` | Same command name | Low |
| `skills/new-crud/SKILL.md` | BaseMapper conflict | Update in place | `rules/java-mapper-rule.md` | Same Skill | Medium |
| `skills/java-guide/*` | BaseMapper conflict | Update active examples | `rules/java-mapper-rule.md` | Same Skill | Medium |
| `commands/deliver-requirement.md` | Missing orchestration entry | Add | `skills/deliver-requirement` | New entry | Low |
| `skills/prd-authoring` | Missing PRD capability | Add | PRD contract | New Skill | Low |
| `skills/pre-coding-check` | Missing pre-coding gate | Add | artifact contracts | New Skill | Low |
| `skills/new-bff` | Missing BFF capability | Add | design/OpenAPI contracts | New Skill | Low |
| `skills/new-page` | Missing frontend capability | Add | UI contract | New Skill | Low |
| `config/quality-thresholds.yaml` | Threshold drift | Add | this file | Referenced by gates | Low |
| `scripts/validate-assets.ps1` | No deterministic validation | Add | scripts | Windows compatible | Low |
