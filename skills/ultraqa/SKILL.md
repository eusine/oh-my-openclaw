---
name: ultraqa
description: "QA cycling — build, test, fix, repeat until all tests pass or cycle limit reached. Used internally by autopilot Phase 3."
argument-hint: "[--cycles N] [--fail-fast] [--commands 'build lint test']"
user-invocable: true
---

<Purpose>
UltraQA is a QA cycling workflow. It runs build and test commands, collects failures, fixes them via parallel executor subagents, and repeats until all tests pass or the cycle limit is reached. It stops early and reports when the same error persists across 3 consecutive cycles (indicating a fundamental issue that needs human intervention).
</Purpose>

<Use_When>
- After implementation, to verify and fix all build/test failures
- User says "ultraqa", "qa cycling", "run qa", "fix all tests"
- Called internally by `autopilot` for Phase 3 QA
- After a refactor or large change where test failures are expected
</Use_When>

<Do_Not_Use_When>
- Codebase has no test suite — provide a note and offer to write tests first
- A single specific test failure needs debugging — use `waza-hunt` for root cause analysis
- Task is pure code generation with no testing component
</Do_Not_Use_When>

<Why_This_Exists>
After implementation, there are typically several failing tests. Fixing them one at a time is slow. UltraQA runs all checks simultaneously, identifies all failures in one pass, fixes them in parallel, and re-verifies — reducing the total number of round-trips needed to reach a clean state.
</Why_This_Exists>

<Execution_Policy>
- Run all check commands simultaneously (build, lint, typecheck, test)
- Collect ALL failures from a single pass before fixing any of them
- Fix independent failures in parallel via parallel executor subagents
- Re-run FULL check suite after fixes — do not run partial checks
- Track consecutive failure patterns: if the same error appears 3 times, flag as fundamental
- Stop when all checks pass or cycle limit reached (default 5 cycles, configurable)
- Use `--fail-fast` to stop at first cycle with any failure (useful for quick iterations)
</Execution_Policy>

<Steps>

## Phase 0: Setup

1. Identify the check commands (from package.json, Makefile, or project conventions):
   - Build command (e.g., `npm run build`, `cargo build`, `make build`)
   - Lint command (e.g., `npm run lint`, `ruff check .`)
   - Type-check command (e.g., `tsc --noEmit`, `mypy .`)
   - Test command (e.g., `npm test`, `pytest`, `cargo test`)
2. Initialize cycle state:

```json
{
  "active": true,
  "mode": "ultraqa",
  "current_phase": "qa",
  "cycle": 0,
  "max_cycles": 5,
  "started_at": "<ISO timestamp>",
  "failure_history": {},
  "consecutive_same_failures": {}
}
```

3. Write initial state to `.oh-my-openclaw/state/ultraqa-state.json`.

## Phase 1: Run Full Check Suite

Run ALL check commands simultaneously:
- Build
- Lint
- Type-check
- Test

Collect ALL output from each command.

Update state: increment `cycle`.

## Phase 2: Analyze Failures

1. Parse output from all check commands.
2. Categorize failures:
   - **Build failures**: compilation errors, missing modules
   - **Lint failures**: style violations, unused imports
   - **Type errors**: type mismatches, missing types
   - **Test failures**: assertion errors, runtime exceptions
3. Group related failures (same root cause → fix together).
4. For each unique error signature, check `consecutive_same_failures`:
   - If count >= 3 → mark as **fundamental blocker** (stop and report)
5. Update `failure_history` in state.

## Phase 3: Fix Failures in Parallel

For each independent failure group, spawn a parallel executor subagent:
- Pass the error output, the relevant file(s), and full context
- Each subagent fixes its assigned failure group
- Subagents run simultaneously when their targets are independent

For failures with dependencies (e.g., type error requires build fix first):
- Fix in the correct order (build → type → test)
- Do not attempt test fixes before build passes

After all fixes are applied, update `failure_history`.

## Phase 4: Re-verify

Run the FULL check suite again (not just the commands that previously failed).

If all checks pass → proceed to Phase 5 (Success).
If failures remain:
- Check if cycle < max_cycles → return to Phase 1
- Check if cycle >= max_cycles → stop and report with final failure state
- If `--fail-fast` is set → stop immediately and report

## Phase 5: Success

1. Update state: `active: false`, `current_phase: "complete"`, `completed_at: "<timestamp>"`
2. Delete `.oh-my-openclaw/state/ultraqa-state.json`
3. Report:
   - Total cycles run
   - What was fixed
   - Final test/build output (last clean run)

</Steps>

<Stop_Conditions>
- **Fundamental blocker:** same error signature appears in 3 consecutive cycles → stop, report the specific failing test/command and error message, ask for guidance
- **Cycle limit reached:** `cycle >= max_cycles` (default 5) → stop, report all remaining failures
- **`--fail-fast` flag:** stop at end of first cycle with any remaining failures
- **User cancellation:** "stop", "cancel", "abort" → stop, preserve state
</Stop_Conditions>

<State_Management>
State file: `{workspace}/.oh-my-openclaw/state/ultraqa-state.json`

- **On start:** write initial state
- **After each cycle:** update `cycle`, `failure_history`, `consecutive_same_failures`
- **On success:** set `active: false`, `completed_at`, delete state file
- **On fundamental blocker:** set `active: false`, `blocked: true`, preserve failure details
</State_Management>

<Tool_Usage>
- Run check commands via bash execution
- Spawn parallel executor subagents for independent failure fixes
- Read error output files to parse failures
- Write state updates to `.oh-my-openclaw/state/ultraqa-state.json` after each cycle
</Tool_Usage>

<Flags>
- `--cycles N`: override max cycles (default 5)
- `--fail-fast`: stop at first cycle with any failure
- `--commands 'cmd1 cmd2 cmd3'`: override which commands to run (space-separated)
</Flags>
