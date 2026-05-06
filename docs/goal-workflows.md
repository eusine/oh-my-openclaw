# Goal workflows

Oh My OpenClaw imports the useful part of OMX v0.16.0 goal-mode work: long-running missions need durable artifacts, explicit acceptance criteria, and fresh completion reconciliation.

OpenClaw does **not** copy Codex hidden goal state or tmux hook assumptions here. The portable contract is:

1. write the goal state under `.oh-my-openclaw/goals/`;
2. define acceptance criteria and validation before execution;
3. execute one goal or one evaluator loop at a time unless dependencies prove safe parallelism;
4. checkpoint outcomes with evidence;
5. complete only after re-reading the durable artifacts and fresh validation output.

## Included goal skills

- `ultragoal` — durable multi-goal planning and sequential execution.
- `performance-goal` — evaluator-gated performance optimization.
- `autoresearch-goal` — source-backed research with professor/critic rubric checks.

## Layout

```text
.oh-my-openclaw/
  goals/
    ultragoal/
      brief.md
      goals.json
      ledger.jsonl
      evidence/
    performance/<slug>/
      objective.md
      state.json
      ledger.jsonl
      evidence/
    autoresearch/<slug>/
      mission.json
      rubric.md
      sources.jsonl
      ledger.jsonl
      report.md
```

## Completion rule

Do not claim a goal is complete because a shell command exited or the assistant believes the work is done. Completion needs a fresh read of artifacts plus the declared validation evidence.
