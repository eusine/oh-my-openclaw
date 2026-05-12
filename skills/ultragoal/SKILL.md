---
name: ultragoal
description: "Create and execute durable repo-native multi-goal plans with OpenClaw artifact reconciliation."
argument-hint: "<brief or goal file>"
user-invocable: true
---

# Ultragoal Workflow

Use when the user asks for `ultragoal`, durable multi-goal planning, sequential goal execution, or a long task that should be split into explicit auditable objectives.

## Purpose

`ultragoal` turns a brief into durable repo/workspace artifacts and executes one auditable story at a time. It imports the useful OMX v0.16.4 goal-mode hardening, but translates it to OpenClaw:

- OpenClaw owns durable state and evidence under `.oh-my-openclaw/goals/ultragoal/`.
- The default plan shape is aggregate: one whole-run objective in `goals.json`, with per-story progress tracked by OpenClaw artifacts and ledger events.
- Subagents may execute individual goals, but the leader owns reconciliation and final judgment.
- Completion requires fresh artifact/test/review evidence, not assistant prose or shell-only optimism.

## Artifacts

- `.oh-my-openclaw/goals/ultragoal/brief.md`
- `.oh-my-openclaw/goals/ultragoal/goals.json`
- `.oh-my-openclaw/goals/ultragoal/ledger.jsonl`
- optional per-goal evidence under `.oh-my-openclaw/goals/ultragoal/evidence/<goal-id>/`

In aggregate mode, `goals.json` must also include:

- `goal_mode: "aggregate"`
- `objective`: the whole-run objective and acceptance boundary
- `active_goal_id`: the current OpenClaw story
- `final_quality_gate`: required verification, cleanup, and review evidence for final completion

## Flow

1. Capture the brief and success criteria.
2. Create `goals.json` with the aggregate objective plus ordered goals, dependencies, acceptance criteria, expected artifacts, and validation commands/checks.
3. Execute exactly one ready goal at a time unless dependencies prove safe parallelism.
4. For each goal:
   - inspect current state before acting;
   - implement only the required scope;
   - run the declared validation or the smallest meaningful substitute;
   - write a ledger entry with status `complete`, `blocked`, or `failed` and evidence paths.
5. For intermediate goals, checkpoint completion only after re-reading evidence for that story; do not claim whole-run completion yet.
6. Before marking the overall workflow complete, run the final quality gate:
   - targeted verification for the final state;
   - AI-slop cleanup or a documented no-op cleanup pass for relevant changed files;
   - post-cleanup verification;
   - code review with a clean outcome.
7. If final review is non-clean, append a blocker-resolution goal and keep the workflow active instead of claiming completion.
8. If any goal is blocked/failed, report the specific blocker and leave the ledger resumable.

## Goal JSON shape

```json
{
  "version": 1,
  "goal_mode": "aggregate",
  "objective": "whole-run objective and acceptance boundary",
  "active_goal_id": "goal-001",
  "goals": [
    {
      "id": "goal-001",
      "title": "short objective",
      "status": "pending",
      "depends_on": [],
      "acceptance": ["observable pass condition"],
      "expected_artifacts": ["path/or/state"],
      "validation": ["test/lint/build/inspection command or check"],
      "evidence": []
    }
  ],
  "final_quality_gate": {
    "required": true,
    "verification": [],
    "cleanup": null,
    "review": null
  }
}
```

## Constraints

- Do not invent hidden goal state. The files above are the source of truth.
- Do not mark a goal complete until the declared acceptance criteria are actually satisfied.
- Do not mark the whole ultragoal complete until every story is complete and the final quality gate has concrete evidence.
- Treat non-clean final review as new work, not as a footnote.
- Do not continue past destructive, external-production, payment, credential, or privacy-sensitive steps without approval.
- Keep ledger entries append-only where practical so interrupted work can be audited.
