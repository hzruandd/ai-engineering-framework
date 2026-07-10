# Industry Practice Mapping For Phase 2

Updated: 2026-07-10

This file maps external practice to current engineering changes. It is not a standalone research report.

| Current issue | Reference | External practice | Fit | Decision | Planned files |
| --- | --- | --- | --- | --- | --- |
| Missing Spec layer | GitHub `spec-kit`, ByteLighting SDD | Specify -> Plan -> Implement -> Validate | High | Adapt | `specs/artifact-contracts/`, `WORKFLOW.md` |
| Skill sprawl risk | `superpowers`, Codex Skills lists | Modular Skills with workflow boundaries | Medium | Adapt | `skills/deliver-requirement`, `skills/pre-coding-check` |
| Cross-tool context | `agents.md` | Shared project instructions | Medium | Pilot later | migration map, project template plan |
| Tests after coding | Meituan unit testing article | Unit-test safety net and TDD | High | Adopt | `skills/generate-tests`, `config/quality-thresholds.yaml` |
| Formal review conflict | Current `tzh-review` | Evidence-first Gate, no preset pass | High | Adopt current asset | `commands/formal-review.md`, `skills/tzh-review` |
| Over-complex multi-agent | agency agent libraries | Specialist roles and orchestration | Low for phase 2 | Reference only | `WORKFLOW.md` boundaries |
| Awesome-list imports | awesome skills lists | Discovery catalog | Medium | Reference only | governance docs |

## Rejected Practices

- Bulk importing high-star Skills: creates trigger conflicts and maintenance load.
- Multi-agent DAG as default: too costly before real pilot data.
- Treating generated tests as passed tests: violates evidence requirements.
- Putting all rules into one huge prompt: increases context cost and conflict risk.
