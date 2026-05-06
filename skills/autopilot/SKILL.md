---
name: autopilot
description: "Strict autonomous loop: ralplan -> ralph -> code-review, with review-gated return to planning."
argument-hint: "<idea, task description, issue, or spec path>"
user-invocable: true
---

<Purpose>
Autopilot is the strict autonomous delivery loop for non-trivial implementation work. Its primary contract is exactly:

```text
ralplan -> ralph -> code-review
```

If `code-review` is not clean, Autopilot returns to `ralplan` with the review findings as first-class planning input, then continues again through `ralph` and `code-review` until the review is clean or a hard blocker is reported.
</Purpose>

<Use_When>
- User wants hands-off execution from a concrete idea, issue, PRD, or requirements artifact to reviewed code.
- User says `autopilot`, `auto pilot`, `autonomous`, `build me`, `create me`, `make me`, `full auto`, or `handle it all`.
- Task needs planning, implementation, verification, and code review with automatic follow-up when review is not clean.
</Use_When>

<Do_Not_Use_When>
- User wants to explore options or brainstorm — use `ralplan` or a lightweight planning pass.
- User says `just explain`, `draft only`, or `what would you suggest` — respond conversationally.
- User wants a single focused code change — use `ralph` or direct execution.
- User wants only review/critique of existing code — use `code-review`.
</Do_Not_Use_When>

<Strict_Loop_Contract>
Autopilot must not run a separate broad expansion/planning/execution/QA/validation lifecycle as its primary behavior. It delegates those concerns to the canonical phases below:

1. **Phase `ralplan` — consensus planning gate**
   - Ground the task with pre-context intake.
   - Produce or update PRD / technical plan / test-spec artifacts.
   - When returning from a non-clean review, include `return_to_ralplan_reason` and review findings as planning input.
   - Required handoff artifact: an approved plan/test spec suitable for `ralph`.

2. **Phase `ralph` — implementation + verification loop**
   - Implement from the approved `ralplan` artifacts.
   - Own implementation, tests, build/lint/typecheck evidence, and verification.
   - Required handoff artifact: implementation evidence and changed-file summary suitable for `code-review`.

3. **Phase `code-review` — merge-readiness gate**
   - Review the diff/artifacts produced by `ralph`.
   - A clean review means final recommendation `APPROVE` with architectural status `CLEAR`.
   - `COMMENT`, `REQUEST CHANGES`, architectural `WATCH`/`BLOCK`, or unresolved findings are not clean.
   - If not clean, increment the review cycle, persist `review_verdict`, set `return_to_ralplan_reason`, and transition back to `ralplan`.

The only normal terminal state is `complete` after a clean code review. Cancellation, blocked credentials, repeated unrecoverable failures, or explicit user stop may terminate earlier with preserved state.
</Strict_Loop_Contract>

<OpenClaw_Translation>
This skill imports the portable workflow behavior from OMX without copying Codex/tmux runtime assumptions.

- Runtime state lives under `.oh-my-openclaw/`, not `.omx/`.
- Use OpenClaw first-class tools and subagents (`sessions_spawn`, tests, file inspection, and direct evidence) rather than raw tmux/hook assumptions.
- External/public/destructive writes still require user approval.
- Keep one user-facing thread; delegate work only when it materially improves speed or quality.
</OpenClaw_Translation>

<Pre_Context_Intake>
Before Phase `ralplan` starts or resumes:
1. Derive a task slug from the request.
2. Reuse the latest relevant `.oh-my-openclaw/context/{slug}-*.md` snapshot when available.
3. If none exists, create `.oh-my-openclaw/context/{slug}-{timestamp}.md` (UTC `YYYYMMDDTHHMMSSZ`) with:
   - task statement
   - desired outcome
   - known facts/evidence
   - constraints
   - unknowns/open questions
   - likely codebase touchpoints
4. If ambiguity remains high, inspect the codebase/docs first, then ask one blocking question or run a quick `deep-interview` only when ambiguity would cause costly rework.
5. Carry the snapshot path in Autopilot state and all handoff artifacts.
</Pre_Context_Intake>

<State_Management>
State file: `.oh-my-openclaw/state/autopilot-state.json`.

Recommended shape:

```json
{
  "mode": "autopilot",
  "active": true,
  "current_phase": "ralplan",
  "iteration": 1,
  "review_cycle": 0,
  "max_iterations": 10,
  "phase_cycle": ["ralplan", "ralph", "code-review"],
  "handoff_artifacts": {
    "context_snapshot_path": ".oh-my-openclaw/context/<slug>-<timestamp>.md",
    "ralplan": null,
    "ralph": null,
    "code_review": null
  },
  "review_verdict": null,
  "return_to_ralplan_reason": null,
  "updated_at": "<ISO timestamp>"
}
```

- On every write, update `updated_at`.
- Use atomic writes: write a temp file, then rename to final path.
- On `ralplan -> ralph`, persist approved planning/test artifacts.
- On `ralph -> code-review`, persist implementation/test evidence.
- On clean review, set `active:false`, `current_phase:"complete"`, `completed_at`, and `review_verdict.clean:true`.
- On non-clean review, increment `iteration` and `review_cycle`, set `current_phase:"ralplan"`, persist review artifacts, and set `return_to_ralplan_reason`.
- On cancellation, preserve progress for resume rather than deleting handoff artifacts.
</State_Management>

<Continuation_And_Resume>
When the user says `continue`, `resume`, or `keep going` while Autopilot is active, read `autopilot-state.json` and continue from `current_phase`:

- `ralplan`: update planning from current handoffs and any `return_to_ralplan_reason`.
- `ralph`: execute the approved plan and record fresh verification evidence.
- `code-review`: review the current diff and decide clean vs return-to-ralplan.
- `complete`: report completion evidence; do not restart.

Do not restart discovery or discard handoff artifacts on continuation.
</Continuation_And_Resume>

<Execution_Policy>
- Always execute phases in order: `ralplan`, then `ralph`, then `code-review`.
- Never skip directly from vague/freeform expansion to implementation.
- A non-clean `code-review` always returns to `ralplan`; do not patch findings ad hoc outside the loop.
- Continue automatically through safe reversible phase transitions.
- Ask only for destructive, external-production, credential-gated, or materially preference-dependent branches.
- Stop and report when the same review or verification failure recurs across 3 review cycles with no meaningful new plan.
</Execution_Policy>

<Final_Checklist>
- [ ] `ralplan` produced/updated approved planning artifacts.
- [ ] `ralph` implemented and verified the plan with fresh evidence.
- [ ] `code-review` returned a clean verdict (`APPROVE` + `CLEAR`).
- [ ] `review_verdict.clean` is true and `return_to_ralplan_reason` is null.
- [ ] Tests/build/lint/typecheck evidence is available in handoff artifacts.
- [ ] Autopilot state is marked `complete` or cancellation/blocker state is preserved coherently.
- [ ] User receives a concise summary with plan, implementation, verification, and review evidence.
</Final_Checklist>
