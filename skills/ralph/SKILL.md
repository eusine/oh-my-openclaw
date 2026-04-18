---
name: ralph
description: "Persistence loop — keeps working on a task until done or a real blocker found. Iterates: delegate in parallel → verify → fix → repeat. The workhorse for single-owner completion tasks."
argument-hint: "[--prd] [--no-deslop] <task description or spec path>"
user-invocable: true
---

<Purpose>
Ralph is a persistent single-owner completion loop. It takes a task and keeps working on it — delegating subtasks to subagents in parallel, verifying results, fixing failures, and iterating — until the task is done or a fundamental blocker is discovered.

Ralph is not autopilot. It is the execution and persistence engine. Use ralph directly when you have a clear task and want maximum persistence without the full planning overhead of autopilot.
</Purpose>

<Use_When>
- User says "ralph", "don't stop", "must complete", "keep going", "keep working until done"
- A clear task exists with acceptance criteria but no need for full consensus planning
- Autopilot Phase 2 (execution) delegates to ralph for persistent subtask completion
- A deep-interview spec or ralplan output is ready for execution
- Long-running work that may need multiple iterations to complete
</Use_When>

<Do_Not_Use_When>
- The task is ambiguous — run `deep-interview` first
- The task needs architectural consensus — use `ralplan` first
- The task requires full pipeline automation — use `autopilot`
- The task is a simple single-step action — delegate directly to an executor subagent
</Do_Not_Use_When>

<Why_This_Exists>
Complex tasks rarely complete in a single pass. Tools fail, tests reveal issues, implementations need adjustment. Ralph provides the persistence layer that keeps work moving forward through these normal obstacles, with verification gates to ensure quality before declaring completion.
</Why_This_Exists>

<Execution_Policy>
- Delegate independent subtasks to subagents in parallel — never serialize parallel-safe work
- Background long-running operations (builds, installs, tests) using background execution
- Verify after every execution round before moving to the next iteration
- Fix issues found during verification before reporting completion
- Apply deslop pass by default after execution (skip with `--no-deslop`)
- Iterate until all acceptance criteria are met or a fundamental blocker is discovered
- If the same failure recurs across 3 consecutive iterations, stop and report the fundamental issue
- Persist state after each iteration for session resume safety
</Execution_Policy>

<Steps>

## Phase 0: Pre-Context Intake

1. Derive a task slug from the request.
2. Check for existing state at `.oh-my-openclaw/state/ralph-state.json` — if `active: true`, this is a **resume**:
   - Load prior progress, completed subtasks, current iteration count
   - Continue from where work stopped, do not restart
3. If no prior state, check for a spec at `.oh-my-openclaw/specs/deep-interview-{slug}.md` or `.oh-my-openclaw/plans/*.md` — reuse if found.
4. If `--prd` flag is set, check `.oh-my-openclaw/specs/` for an existing PRD and use it as the acceptance criteria source.
5. Load or create context snapshot at `.oh-my-openclaw/context/{slug}-{timestamp}.md`:
   - Task statement and acceptance criteria
   - Known codebase touchpoints
   - Constraints and non-goals
6. Initialize state — write to `.oh-my-openclaw/state/ralph-state.json`:

```json
{
  "active": true,
  "mode": "ralph",
  "current_phase": "intake",
  "iteration": 0,
  "max_iterations": 20,
  "started_at": "<ISO timestamp>",
  "task_description": "<task>",
  "acceptance_criteria": [],
  "completed_subtasks": [],
  "failed_attempts": {},
  "context_snapshot_path": ".oh-my-openclaw/context/<slug>-<timestamp>.md"
}
```

## Phase 1: Review Progress

At the start of each iteration:

1. Read current state from `.oh-my-openclaw/state/ralph-state.json`.
2. Assess what has been completed (read relevant files, run quick checks).
3. Identify what remains — generate a concrete subtask list for this iteration.
4. Check if all acceptance criteria are met → if yes, jump to Phase 6 (Verify Completion).
5. Update state: increment `iteration`, update `current_phase: "execution"`.

## Phase 2: Delegate in Parallel

1. Classify subtasks by independence:
   - **Parallel-safe:** no dependency between them → launch all simultaneously
   - **Sequential:** has prerequisites → run after dependencies complete
2. Route subtasks to the appropriate subagent role:
   - Simple lookups/writes → executor (standard)
   - Complex implementation → executor (thorough)
   - Analysis/debugging → debugger
   - Test writing → test-engineer
3. Spawn parallel subagents for parallel-safe tasks simultaneously.
4. Collect results from all parallel workers before proceeding.
5. Update `completed_subtasks` in state.

## Phase 3: Background Long Operations

For builds, package installs, or test suites that take >30 seconds:

1. Launch in background using appropriate background execution.
2. Continue with other subtasks while waiting.
3. Collect results when background operations complete.
4. Do not block iteration on long ops when other work can proceed.

## Phase 4: Task Completion Gate

After each execution round:

1. Review what was just completed.
2. Check explicit acceptance criteria: are all met?
3. Run a quick sanity check (read key files, check for obvious errors).
4. If all criteria met → proceed to Phase 5 (Verification).
5. If not met → identify gaps, update state, return to Phase 1 for next iteration.
6. **Failure tracking:** if a subtask failed this iteration, increment its `failed_attempts` counter. If count reaches 3, flag it as a fundamental blocker.

## Phase 5: Verify Completion

When acceptance criteria appear met:

1. Run the verification suite — build, lint, relevant tests.
2. Read key output files to confirm correctness.
3. If all checks pass → proceed to Phase 6 (Architect Verification).
4. If checks fail → identify root cause, add failed items back to subtask list, return to Phase 1.

## Phase 6: Architect Verification Pass

1. Spawn an architect subagent to review the completed work:
   - Does the implementation match the stated intent and non-goals?
   - Are there architectural concerns or technical debt introduced?
   - Are there missing edge cases?
2. If architect approves → proceed to Phase 7.
3. If architect raises issues → fix them, re-verify (Phase 5), then re-run architect check.

## Phase 7: Deslop Pass (unless `--no-deslop`)

1. Spawn a code-simplifier subagent to clean up AI-generated verbosity:
   - Remove unnecessary comments
   - Simplify redundant logic
   - Normalize formatting inconsistencies
2. Verify that deslop pass did not break functionality (quick re-test).
3. If `--no-deslop` flag was set, skip this phase entirely.

## Phase 8: Regression Re-Verification

1. Run full test suite one final time with a clean environment.
2. Confirm all tests pass after the deslop pass.
3. If any regressions found → fix them before proceeding.

## Phase 9: Completion

1. Update state: `active: false`, `current_phase: "complete"`, `completed_at: "<timestamp>"`.
2. Report completion with:
   - Summary of what was built/changed
   - Files modified
   - Test results
   - Any known residual issues or follow-up recommendations
3. Delete or archive `.oh-my-openclaw/state/ralph-state.json`.

</Steps>

<Escalation_And_Stop_Conditions>
- **Fundamental blocker:** same subtask fails across 3 consecutive iterations → stop, report root cause, ask for guidance
- **Architect rejection loop:** architect rejects more than 3 times → stop, report architectural conflict
- **Iteration limit:** reached `max_iterations` (default 20) → stop, report current state
- **User cancellation:** user says "stop", "cancel", or "abort" → stop, preserve state for resume
- **Unrecoverable test failure:** catastrophic failure that cannot be fixed without new requirements → stop, report
</Escalation_And_Stop_Conditions>

<State_Management>
State file: `{workspace}/.oh-my-openclaw/state/ralph-state.json`

- **On start:** write initial state JSON with `active: true`, `iteration: 0`, `updated_at: <ISO timestamp>`
- **On each iteration:** update `iteration`, `completed_subtasks`, `failed_attempts`, `current_phase`, **and always update `updated_at`**
- **On completion:** set `active: false`, `completed_at`, `updated_at`
- **On resume:** read existing state, verify `current_phase` matches actual filesystem state, continue from last iteration
- **On cancellation:** preserve state with current progress and `updated_at` for later resume

**`updated_at` is required on every write.** The oh-my-openclaw harness hook uses it to distinguish live vs abandoned states (> 48h = stale warning).

**Atomic write pattern:** write state to a temp file (`.oh-my-openclaw/state/ralph-state.json.tmp`), then rename to final path. This prevents partial-write corruption on crash.

**Resume verification:** when resuming from a prior session, do a quick sanity check — read key output files or run a fast check to confirm that claimed `completed_subtasks` actually reflect filesystem state. If there is a discrepancy, correct the state before proceeding.
</State_Management>

<Tool_Usage>
- Use parallel subagent spawning for parallel-safe subtasks — never serialize independent work
- Use background execution for builds, installs, and test suites
- Use file read/search tools (Read, Grep, Glob) for verification and progress checks
- Write state updates to `.oh-my-openclaw/state/ralph-state.json` after each significant action
</Tool_Usage>

<Flags>
- `--prd`: treat `.oh-my-openclaw/specs/` PRD as the canonical acceptance criteria source
- `--no-deslop`: skip the deslop pass (Phase 7)
</Flags>
