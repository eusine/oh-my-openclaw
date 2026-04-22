---
name: ultrawork
description: "Parallel execution engine — fires multiple subagents simultaneously for independent tasks. High-throughput task completion without persistence loops."
argument-hint: "<task list or description of parallel work>"
user-invocable: true
---

<Purpose>
Ultrawork is a parallel execution engine that runs multiple subagents simultaneously for independent tasks. It is a component, not a standalone persistence mode — it provides parallelism and smart model routing but not persistence, verification loops, or state management.

Use ultrawork when you have a clear set of independent tasks and want to execute them simultaneously. For guaranteed completion with verification, use `ralph` instead (ralph includes ultrawork-style parallelism). For a full autonomous pipeline, use `autopilot`.
</Purpose>

<Use_When>
- Multiple independent tasks can run simultaneously
- User says "ulw", "ultrawork", or explicitly wants parallel execution
- You need to delegate several independent tasks to subagents at once
- Task benefits from concurrent execution and the user will manage completion
- Called internally by `ralph` and `autopilot` for their execution phases
</Use_When>

<Do_Not_Use_When>
- Task requires guaranteed completion with verification loops — use `ralph` instead
- Task requires full autonomous pipeline — use `autopilot` instead
- There is only one sequential task with no parallelism opportunity — delegate directly
- User needs session persistence for resume — use `ralph`
</Do_Not_Use_When>

<Why_This_Exists>
Sequential task execution wastes time when tasks are independent. Ultrawork enables firing multiple subagents simultaneously and routing each to the right complexity tier, reducing total execution time while controlling quality. It is designed as a composable component that ralph and autopilot layer on top of.
</Why_This_Exists>

<Execution_Policy>
- Fire all independent subagent calls simultaneously — never serialize independent work
- Route each task to the appropriate complexity tier (see Model Routing below)
- Use background execution for long-running operations (builds, installs, tests)
- Run quick checks (file reads, git status, simple commands) in the foreground
- Track task completion — collect results from all parallel workers before declaring done
- Treat safe continuation as the default, not a handoff moment; do not end worker orchestration with weak optional phrasing when the next local step is still clear
</Execution_Policy>

<Model_Routing>
Route subtasks by complexity:

| Complexity | Examples | Tier |
|---|---|---|
| Simple | File reads, lookups, definitions, single-function edits | Standard |
| Standard | Feature implementation, test writing, refactoring | Standard |
| Complex | Architecture review, security audit, cross-system refactoring | Thorough |

Subagent role routing:
- **executor**: general implementation work
- **debugger**: root cause analysis and bug fixing
- **test-engineer**: test writing and test strategy
- **architect**: architectural review and design decisions
- **code-reviewer**: code quality review
- **security-reviewer**: security vulnerability review
- **style-reviewer**: formatting and convention review
- **writer**: documentation writing
- **explore**: codebase investigation and fact-gathering
</Model_Routing>

<Steps>

## Step 1: Classify Tasks by Independence

1. Parse the task description and identify individual subtasks.
2. Classify each subtask:
   - **Parallel-safe:** no dependency between them → can launch simultaneously
   - **Sequential:** depends on output of another task → must wait for prerequisite
3. Build a dependency graph if needed.

## Step 2: Route to Correct Subagent Tiers

For each subtask:
1. Determine appropriate agent role (executor, debugger, architect, etc.)
2. Determine complexity tier (standard or thorough)
3. Prepare the subtask description with full context

## Step 3: Fire Independent Tasks Simultaneously

Launch ALL parallel-safe subtasks at once:
- Do not wait for one to complete before launching the next
- Pass full task context to each subagent — do not assume shared state
- Each subagent should be self-contained and not rely on outputs from parallel siblings

## Step 4: Run Dependent Tasks Sequentially

For tasks with prerequisites:
1. Wait for the prerequisite subtask to complete
2. Pass the prerequisite output to the dependent task
3. Launch the dependent task

## Step 5: Background Long Operations

For builds, package installs, and test suites expected to run >30 seconds:
1. Launch in background
2. Continue with other parallel tasks while waiting
3. Collect results when the background operation completes

## Step 6: Lightweight Verification (when all tasks complete)

Run a quick sanity check when all subtasks report completion:
- Build/typecheck passes (if code was changed)
- Affected tests pass (run the subset related to changed code)
- No new errors introduced
- Key output files exist and have expected content

Report results and any failures found.

</Steps>

<State_Management>
Ultrawork is stateless by design — it does not persist mode state. For stateful persistence, use `ralph`.

If called from within ralph or autopilot, those modes manage the outer state. Ultrawork only needs to track in-flight subagent results within a single session.
</State_Management>

<Tool_Usage>
- Spawn subagents in parallel for parallel-safe tasks — never serialize independent work
- Use background execution for long-running operations
- Use foreground execution for quick checks and file operations
- Collect results from all parallel workers before the verification step
</Tool_Usage>

<Examples>
<Good>
Tasks: "write unit tests for auth.ts, write unit tests for payment.ts, write unit tests for notification.ts"
Why: All three are independent, fire simultaneously.
</Good>

<Good>
Tasks: "run linter, run type-checker, run security scan"
Why: All three checks are independent, run in parallel.
</Good>

<Bad>
Tasks: "implement login feature, then write tests for it"
Why: Tests depend on the implementation. Implement first, then write tests. This is sequential, not parallel.
</Bad>
</Examples>
