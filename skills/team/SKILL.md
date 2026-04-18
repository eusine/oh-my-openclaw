---
name: team
description: "Coordinated parallel execution using OpenClaw's native subagent system. Decomposes a task into partitions and runs up to 6 concurrent workers sharing a task manifest."
argument-hint: "[N:agent-type] <task description or spec path>"
user-invocable: true
---

<Purpose>
Team orchestrates coordinated parallel execution using OpenClaw's native subagent model. It decomposes a task into partitions, spawns multiple worker subagents with `sessions_spawn`, coordinates their progress, and merges results when all workers complete.

Team is the right choice for large tasks where the work is naturally partitionable and multiple parallel owners can work without blocking each other.
</Purpose>

<Use_When>
- User says "team", "swarm", "coordinated team", "coordinated swarm"
- Task is large enough to benefit from true parallel ownership (multiple files, multiple subsystems)
- Work can be cleanly decomposed into independent partitions
- There is a coordinator role (Hina/orchestrator) managing multiple executor workers
- Called by `autopilot` Phase 2 when task is large enough to justify team execution
</Use_When>

<Do_Not_Use_When>
- Task is sequential by nature (each step depends on the previous) — use `ralph` instead
- Task is small enough for a single focused executor — delegate directly
- Workers would need to constantly share state or coordinate heavily — overhead exceeds benefit
- Task requires exactly one owner for quality consistency — use `ralph`
</Do_Not_Use_When>

<Why_This_Exists>
Some tasks are genuinely large — implementing a full feature across multiple subsystems, migrating a large codebase, or processing many independent files. Sequential execution wastes time when work is naturally parallel. Team provides coordinated parallel ownership where each worker has a clear partition and reports back to a coordinator.
</Why_This_Exists>

<Execution_Policy>
- Maximum 6 concurrent workers (constrained by `maxConcurrent=8` in OpenClaw config; reserve capacity for coordinator and verification)
- Default worker count: 3 (adjust based on task decomposability)
- Each worker owns a non-overlapping partition — no shared mutable state between workers
- Coordinator (main session / orchestrator) manages overall progress and user-facing synthesis
- Prefer OpenClaw-native subagent announces over polling loops; completion should come back to the requester channel automatically
- Treat OpenClaw background tasks as the activity ledger, not as the primary team control plane
- Use hooks only for lightweight lifecycle glue, not as the core team runtime
- After all workers complete, coordinator runs a merge + verification pass
- If a worker fails, coordinator reassigns its partition to another worker or handles directly
</Execution_Policy>

<Steps>

## Phase 0: Pre-Context Intake

1. Derive task slug.
2. Check for existing spec: `.oh-my-openclaw/specs/deep-interview-{slug}.md` or `.oh-my-openclaw/plans/ralplan-*.md` — use if found.
3. Determine worker count N (default 3, max 6):
   - Parse from `N:agent-type` argument syntax if provided
   - Otherwise infer from task size (number of subsystems, files, or feature areas)
4. Determine agent role for workers (default: `executor`):
   - `executor` for implementation tasks
   - `debugger` for debugging/analysis tasks
   - `test-engineer` for test writing tasks
   - `architect` for design/analysis tasks

## Phase 1: Task Decomposition

Spawn an architect subagent to decompose the task into N parallel partitions:

1. Analyze the full task scope.
2. Identify N non-overlapping, independently executable partitions.
3. For each partition:
   - Clear description of what to implement
   - Specific files/modules to work on (no overlap with other partitions)
   - Acceptance criteria for this partition
   - Dependencies on other partitions (should be none or minimal)
4. Write team manifest to `.oh-my-openclaw/state/team/{team-id}/config.json`:

```json
{
  "team_id": "<uuid>",
  "task_slug": "<slug>",
  "worker_count": 3,
  "agent_role": "executor",
  "spec_path": ".oh-my-openclaw/specs/<slug>.md",
  "partitions": [
    {
      "id": "w1",
      "description": "...",
      "files": ["..."],
      "acceptance_criteria": ["..."]
    }
  ],
  "started_at": "<ISO timestamp>"
}
```

5. Write per-worker status files (initial state):
   - `.oh-my-openclaw/state/team/{team-id}/worker-1.json` → `{status: "pending", partition: "w1"}`
   - (repeat for each worker)

## Phase 2: Spawn Workers in Parallel

Launch all N worker subagents simultaneously:

Each worker receives:
- Its assigned partition description
- The full task context (spec path, constraints, acceptance criteria)
- Its partition's specific files and scope
- Instructions to write status updates to its status file
- Instructions NOT to modify files outside its assigned partition

Workers execute independently and write to `.oh-my-openclaw/state/team/{team-id}/worker-N.json`:
```json
{
  "status": "in_progress|complete|failed",
  "worker_id": "w1",
  "started_at": "...",
  "completed_at": "...",
  "files_modified": ["..."],
  "notes": "..."
}
```

## Phase 3: Monitor and Handle Failures

While workers are running, the coordinator:

1. Monitors subagent completion announces and inspects task/subagent state on-demand when intervention is needed.
2. If a worker reports `failed`:
   - Read its error notes
   - Decide: reassign partition to another worker, or handle directly
   - Update the manifest and restart work on that partition
3. If all workers report `complete` → proceed to Phase 4.
4. If a worker is stuck on a short task, inspect the relevant subagent/task and restart if needed.

For Telegram-first usage, the main chat remains the leader surface. Workers do not become their own persistent user-facing chats. They report back through OpenClaw's announce path and the coordinator rewrites updates in normal assistant voice.

## Phase 4: Merge and Integration Check

After all workers complete:

1. Read all worker status files to confirm completion.
2. Run integration checks:
   - Build the full project (not just individual partitions)
   - Run the integration test suite
   - Check for conflicts between worker outputs (import collisions, naming conflicts)
3. Fix any integration issues found (coordinator handles these directly or spawns a fix subagent).

## Phase 5: Verification Pass

Spawn parallel verification subagents:
- **Code-reviewer**: review the combined output for quality
- **Test-engineer**: verify test coverage across all partitions

If issues are found: create targeted fix tasks and re-run the affected portion.

## Phase 6: Completion

1. Update manifest: all workers `complete`, verification passed.
2. Clean up state files: archive to `.oh-my-openclaw/state/team/{team-id}/archive/`.
3. Report:
   - What each worker implemented (by partition)
   - Files created/modified per partition
   - Integration check results
   - Verification outcomes

## OpenClaw alignment notes

- Use `sessions_spawn` for worker creation, because OpenClaw subagents are the native detached-work primitive.
- Expect one completion announce per worker back to the requester path instead of building a custom HUD-first runtime.
- Use `openclaw tasks` for audit, debugging, and cancellation when detached work misbehaves, not as a scheduler.
- Use hooks for supporting automation only. Do not turn hooks into the main team execution surface.
- On Telegram, prefer one leader chat plus background workers. Thread-bound persistent team UX is not the primary path there.

</Steps>

<State_Management>
State directory: `{workspace}/.oh-my-openclaw/state/team/{team-id}/`

Files:
- `config.json` — team manifest with partitions
- `worker-{n}.json` — per-worker status (pending/in_progress/complete/failed)
- `coordinator.json` — overall team progress

On completion: archive to `.oh-my-openclaw/state/team/{team-id}/archive/`.
</State_Management>

<Tool_Usage>
- Spawn architect subagent for Phase 1 decomposition
- Spawn N worker subagents simultaneously for Phase 2 (parallel)
- Inspect tasks/subagent state on-demand during Phase 3 when debugging or intervening
- Run bash commands for build and integration tests in Phase 4
- Spawn parallel reviewer subagents for Phase 5 verification
- Write state to `.oh-my-openclaw/state/team/` using file write tools
</Tool_Usage>

<Argument_Syntax>
- `3:executor <task>` — spawn 3 executor workers for the given task
- `5:test-engineer <task>` — spawn 5 test-engineer workers
- `<task>` — use default (3 executor workers)
</Argument_Syntax>

<Constraints>
- Maximum 6 concurrent workers (openclaw subagent concurrency limit)
- Workers must have non-overlapping file scopes — enforce in the decomposition step
- Coordinator should not implement — only orchestrate and verify
- If decomposition produces highly dependent partitions, use `ralph` instead
</Constraints>
