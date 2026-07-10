# Phase 2 Target Architecture

Updated: 2026-07-10

```mermaid
flowchart TB
  Req["Raw Requirement / TAPD"] --> PRD["PRD Skill"]
  PRD --> PRDGate["PRD Gate"]
  PRDGate --> Design["Design Contract"]
  Design --> DesignGate["Design Gate"]
  DesignGate --> PreCoding["Pre-coding Check"]
  PreCoding --> TDD["TDD / Test Plan"]
  TDD --> Coding["Backend / BFF / Frontend Skills"]
  Coding --> Build["Build Gate"]
  Build --> Test["Test Gate / Self-test"]
  Test --> Diff["Diff Report"]
  Diff --> Review["tzh-review Formal Gate"]
  Review --> Release["Release Gate"]
```

## Asset Responsibilities

| Asset | Responsibility |
| --- | --- |
| CLAUDE.md | Core hard rules and navigation |
| Rule | Stable constraints such as Java Mapper rule |
| Spec | Artifact contracts and structured delivery outputs |
| Skill | Reusable execution capability |
| Command | Thin user entry |
| Workflow | Multi-stage orchestration |
| Gate | Deterministic pass/block semantics |
| Template | Standard output skeleton |
| Script | Deterministic validation |
| Evaluation | Effectiveness test cases |

## Single Decision Source

`tzh-review` is the only formal quality decision source for Tingzhihui release review. `formal-review` can summarize or format, but cannot change risk grade, Unknowns, or the final decision.
