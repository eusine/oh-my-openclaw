---
name: ultrawork
description: "Parallel execution engine for high-throughput task completion with lightweight evidence"
argument-hint: "<task list or description of parallel work>"
user-invocable: true
---

<Purpose>
Ultrawork is a parallel execution engine for high-throughput task completion. It is a component, not a standalone persistence mode: it provides parallelism, context discipline, and smart delegation guidance, but not Ralph's persistence loop, architect sign-off, or long-running completion guarantees.

Use ultrawork when independent work can run concurrently and close with lightweight evidence. For guaranteed completion with verification, use `ralph` instead. For a full autonomous pipeline, use `autopilot`.
</Purpose>

<Use_When>
- Multiple independent tasks can run simultaneously
- User says `ulw`, `ultrawork`, or explicitly wants parallel execution
- Task benefits from concurrent execution plus lightweight evidence before wrap-up
- A direct-tool lane can run beside one or more background evidence lanes without entering Ralph
- Called internally by `ralph` and `autopilot` for their execution phases
</Use_When>

<Do_Not_Use_When>
- Task requires guaranteed completion with persistence, architect verification, or deslop/reverification — use `ralph` instead
- Task requires a full autonomous pipeline — use `autopilot` instead
- There is only one sequential task with no parallelism opportunity — execute directly or delegate to a single executor
- The request is still in plan-consensus mode — keep planning artifacts in `ralplan` until execution is explicitly authorized
- User needs session persistence for resume — use `ralph`, which adds persistence on top of ultrawork
</Do_Not_Use_When>

<Why_This_Exists>
Sequential task execution wastes time when tasks are independent. Ultrawork keeps the execution branch fast while tightening the protocol: gather enough context first, define pass/fail acceptance criteria before editing, decide deliberately between local execution and delegation, and finish with evidence rather than vibes.
</Why_This_Exists>

<Execution_Policy>
- Gather enough context before implementation: task intent, desired outcome, constraints, likely touchpoints, and uncertainties that would change the execution path.
- If uncertainty is still material after a quick repo read, run a focused evidence pass before editing.
- Define pass/fail acceptance criteria before launching execution lanes. Include the command, artifact, or manual check that proves success.
- Prefer direct tool work when the task is small, coupled, or blocked on immediate local context. Delegate only when the work is independent enough to benefit from parallel execution.
- When useful, run a direct-tool lane and one or more background evidence lanes at the same time. Evidence lanes can cover docs, tests, regression mapping, or bounded repo analysis.
- Fire independent subagent calls simultaneously — never serialize independent work.
- Always pass `model` explicitly when spawning subagents when the tool supports it.
- Auto-delegate a researcher/evidence lane when official docs, version-aware framework guidance, best practices, or external dependency behavior materially affect task correctness.
- Use background execution for operations over ~30 seconds: installs, builds, long tests, crawls.
- Run quick commands such as git status, file reads, and simple checks in the foreground.
- Default to concise, evidence-dense progress and completion reporting. If a lane is speculative or blocked, say so explicitly.
- Treat newer user task updates as local overrides for the active workflow branch while preserving earlier non-conflicting constraints.
- If the user says `continue` after ultrawork already has a clear next step, continue the current execution branch instead of restarting planning or asking for reconfirmation.
</Execution_Policy>

<Steps>
1. **Context + certainty check**
   - State the task intent in one sentence.
   - List constraints and unknowns that could invalidate a quick fix.
   - If confidence is low, explore first and narrow the task before editing.
2. **Define acceptance criteria before execution**
   - What must be true at the end?
   - Which command or artifact proves it?
   - Which manual QA check is required, if any?
3. **Classify the work by dependency shape**
   - Independent tasks → parallel lanes.
   - Shared-file or prerequisite-heavy tasks → local execution or staged lanes.
4. **Choose self vs delegate deliberately**
   - Work locally when the next step depends on immediate repo context, shared files, or tight iteration.
   - Delegate when the task slice is bounded, independent, and materially improves throughput.
5. **Run execution lanes**
   - Direct-tool lane for immediate implementation or verification work.
   - Background evidence lanes for tests, docs, repo analysis, or regression checks.
6. **Run dependent tasks sequentially**
   - Wait for prerequisites before launching dependent work.
7. **Close with lightweight evidence**
   - Build/typecheck passes when relevant.
   - Affected tests pass.
   - Manual QA notes are recorded when the task needs a human-visible or behavior-level check.
   - No new errors introduced.
</Steps>

<Tool_Usage>
- Use `sessions_spawn` for independent subagent lanes; spawn independent lanes in parallel when possible.
- Use LOW/mini-style delegation for simple lookups and bounded evidence gathering.
- Use STANDARD delegation for implementation and regression work.
- Use THOROUGH delegation for complex analysis, architecture review, or risky multi-file changes.
- Prefer a direct-tool lane when the immediate next step is blocked on local context.
- Prefer background evidence lanes when you can learn something useful in parallel with implementation.
- Use background execution for package installs, builds, and test suites expected to run long.
- Use foreground execution for quick status checks and file operations.
</Tool_Usage>

<State_Management>
Ultrawork is lightweight and normally stateless. If the run needs resume semantics, promote the task to `ralph` or an explicit OpenClaw task/session.

If called from `ralph` or `autopilot`, those modes own persistent state under `.oh-my-openclaw/state/`. Ultrawork tracks in-flight lane results only within the current execution branch.
</State_Management>

<Examples>
<Good>
Two-track execution with acceptance criteria up front:

```
Acceptance criteria:
- `npm run build` passes
- targeted regression test passes
- manual QA note captured for user-visible behavior

Direct-tool lane:
- update the skill or implementation file

Background evidence lane:
- spawn test-engineer to map changed-path regression coverage
```

Why good: context is grounded first, acceptance criteria are explicit, and implementation runs beside a bounded evidence lane.
</Good>

<Good>
Correct self-vs-delegate judgment:

```
Shared-file edit in progress across one implementation file and its test → keep implementation local.
Independent regression mapping for keyword-detector coverage → delegate to a test-engineer lane.
```

Why good: shared-file work stays local; independent evidence work fans out.
</Good>

<Bad>
Parallelizing before the task is grounded:

```
spawn executor: "Implement whatever seems necessary"
spawn test-engineer: "Figure out how to test it later"
```

Why bad: no context snapshot, no pass/fail target, and delegation starts before the work is shaped.
</Bad>

<Bad>
Claiming success without evidence or manual QA:

```
Made the changes. Ultrawork should be updated now.
```

Why bad: no verification output, no acceptance evidence, and no manual QA note when the behavior is user-visible.
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- When ultrawork is invoked directly, apply lightweight verification only: build/typecheck when relevant, affected tests, and manual QA notes when needed.
- Ralph owns persistence, architect verification, deslop, and the full verified-completion promise. Do not claim those guarantees from direct ultrawork alone.
- If a task fails repeatedly across retries, report the issue rather than retrying indefinitely.
- Escalate to the user when tasks have unclear dependencies, conflicting requirements, or a materially branching acceptance target.
</Escalation_And_Stop_Conditions>

<Final_Checklist>
- [ ] Task intent and constraints were grounded before editing
- [ ] Pass/fail acceptance criteria were stated before execution
- [ ] Parallel lanes were used only for independent work
- [ ] Build/typecheck passes when relevant
- [ ] Affected tests pass
- [ ] Manual QA notes recorded when behavior is user-visible
- [ ] No new errors introduced
- [ ] Completion claim stays inside ultrawork's lightweight-verification boundary
</Final_Checklist>

<Advanced>
## Relationship to Other Modes

```
ralph (persistence + verified completion wrapper)
 └─ includes: ultrawork
    └─ provides: high-throughput execution + lightweight evidence

autopilot (autonomous execution)
 └─ includes: ralph
    └─ includes: ultrawork
```

Ultrawork is the parallelism and execution-discipline layer. Ralph adds persistence, architect verification, deslop, and retry-until-done behavior. Autopilot adds the broader autonomous lifecycle pipeline.
</Advanced>
