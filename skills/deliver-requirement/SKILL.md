---
name: deliver-requirement
description: Orchestrate the city-parking AI Coding delivery workflow from requirement to release gate. Use when users ask to deliver a requirement, continue a delivery, inspect delivery state, or run the end-to-end AI Coding workflow.
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
argument-hint: "[requirement-id] [tapd-id] [stage]"
---

# Deliver Requirement

## Purpose

Coordinate the minimum end-to-end workflow without duplicating specialist logic. This Skill locates artifacts, checks the current stage, calls the relevant Skill, and stops at failed gates.

## Inputs

- Requirement description or `requirement_id`
- Optional `tapd_id`
- Optional target stage
- Existing artifacts under `docs/requirements/<requirement-id>/` or `docs/deliveries/<requirement-id>/`

## Outputs

- `docs/deliveries/<requirement-id>/delivery-state.yaml`
- Next-step summary
- Gate result summary
- Unknowns and blockers

## Workflow

1. Read `WORKFLOW.md`.
2. Locate `delivery-state.yaml`; create it only if this is a new requirement.
3. Locate PRD, design, tasks, test plan, self-test report, diff report, and review report.
4. Determine current stage.
5. Call the specialist Skill for the next missing stage:
   - PRD: `prd-authoring`
   - Design: `design-doc`
   - Pre-coding: `pre-coding-check`
   - TDD/test planning: `generate-tests`
   - Backend: `new-crud`, `new-api`, `add-field`, `fix-cache`
   - BFF: `new-bff`
   - Frontend: `new-page`
   - Self-test: `self-test`
   - Formal review: `tzh-review`
6. Stop on `FAIL`, core `UNKNOWN`, or required `NOT_EXECUTED`.
7. Update the delivery state.

## Boundaries

- Do not perform formal quality decision. Use `tzh-review`.
- Do not hide failed or unexecuted tests.
- Do not generate code for large/core changes without PRD and design artifacts.

## Example

```text
/deliver-requirement requirement_id=REQ-20260710-001 tapd=TAPD-123456 stage=continue
```
