# Goal workflows

Oh My OpenClaw imports the useful part of OMX v0.16.4 goal-mode work: long-running missions need durable artifacts, explicit acceptance criteria, fresh completion reconciliation, and review evidence before final completion.

OpenClaw does **not** copy Codex hidden goal state or tmux hook assumptions here. The portable contract is:

1. write the goal state under `.oh-my-openclaw/goals/`;
2. define acceptance criteria and validation before execution;
3. execute one goal or one evaluator loop at a time unless dependencies prove safe parallelism;
4. checkpoint outcomes with evidence;
5. complete only after re-reading durable artifacts, fresh validation output, cleanup evidence, and final review evidence.

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

For `ultragoal`, the default plan shape is aggregate: one whole-run objective, many OpenClaw ledger stories. Intermediate stories can complete with story-level evidence, but whole-run completion requires the final quality gate:

- targeted verification for the final state;
- cleanup/deslop pass or a documented no-op when no relevant cleanup exists;
- post-cleanup verification;
- clean code-review outcome.

If final review is non-clean, append a blocker-resolution goal and continue instead of marking the run complete.
