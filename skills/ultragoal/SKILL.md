---
name: ultragoal
description: "Create and execute durable repo-native multi-goal plans with OpenClaw artifact reconciliation."
argument-hint: "<brief or goal file>"
user-invocable: true
---

# Ultragoal Workflow

Use when the user asks for `ultragoal`, durable multi-goal planning, sequential goal execution, or a long task that should be split into explicit auditable objectives.

## Purpose

`ultragoal` turns a brief into durable repo/workspace artifacts and executes one goal at a time. It imports the OMX v0.16.0 goal-mode idea, but translates it to OpenClaw:

- OpenClaw owns durable state and evidence under `.oh-my-openclaw/goals/ultragoal/`.
- Subagents may execute individual goals, but Hina/the leader owns reconciliation and final judgment.
- Completion requires fresh artifact/test evidence, not assistant prose or shell-only optimism.

## Artifacts

- `.oh-my-openclaw/goals/ultragoal/brief.md`
- `.oh-my-openclaw/goals/ultragoal/goals.json`
- `.oh-my-openclaw/goals/ultragoal/ledger.jsonl`
- optional per-goal evidence under `.oh-my-openclaw/goals/ultragoal/evidence/<goal-id>/`

## Flow

1. Capture the brief and success criteria.
2. Create `goals.json` with ordered goals, dependencies, acceptance criteria, expected artifacts, and validation commands/checks.
3. Execute exactly one ready goal at a time unless dependencies prove safe parallelism.
4. For each goal:
   - inspect current state before acting;
   - implement only the required scope;
   - run the declared validation or the smallest meaningful substitute;
   - write a ledger entry with status `complete`, `blocked`, or `failed` and evidence paths.
5. Before marking the overall workflow complete, re-read the artifacts and validation outputs for every goal.
6. If any goal is blocked/failed, report the specific blocker and leave the ledger resumable.

## Goal JSON shape

```json
{
  "version": 1,
  "goals": [
    {
      "id": "goal-001",
      "title": "short objective",
      "status": "pending",
      "depends_on": [],
      "acceptance": ["observable pass condition"],
      "expected_artifacts": ["path/or/state"],
      "validation": ["test/lint/build/inspection command or check"]
    }
  ]
}
```

## Constraints

- Do not invent hidden goal state. The files above are the source of truth.
- Do not mark a goal complete until the declared acceptance criteria are actually satisfied.
- Do not continue past destructive, external-production, payment, credential, or privacy-sensitive steps without approval.
- Keep ledger entries append-only where practical so interrupted work can be audited.
