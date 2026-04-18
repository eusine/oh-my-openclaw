# Team Operating Model

Oh My OpenClaw should treat team execution as an OpenClaw-native orchestration pattern, not as a cosplay clone of older tmux-first runtimes.

## Core mapping

- **main session** = leader or orchestrator
- **subagents** = workers
- **completion announce** = how worker results flow back
- **background tasks** = detached-work ledger
- **hooks** = lifecycle glue, not the main team runtime

## Why this matters

A true migration does not just copy old names or vibes. It rebuilds the operating model on top of the primitives OpenClaw actually provides.

For team execution, that means using:
- `sessions_spawn` for worker creation
- OpenClaw subagent announces for result delivery
- `openclaw tasks` for audit or intervention
- hooks only for lightweight automation around the edges

## Telegram-first team model

When Telegram is the main user-facing surface:

- the Telegram chat stays the leader surface
- workers run in the background as subagents
- worker completions come back through announces
- the coordinator rewrites those results into concise user-facing updates
- the user should not need to micromanage worker session ids

This is different from a thread-heavy desktop workflow. That is fine. It is the correct fit for Telegram.

## Recommended flow

1. user asks for a big task in chat
2. coordinator decides the work is partitionable
3. coordinator decomposes the task into non-overlapping partitions
4. coordinator spawns workers with `sessions_spawn`
5. workers complete and announce back
6. coordinator merges, verifies, and reports back in the main chat

## When to use team

Use `team` when:
- work is naturally partitionable
- multiple owners can proceed independently
- merge and verification cost is lower than serial execution time

Do not use `team` when:
- the task is mostly sequential
- one owner needs to keep the whole thing in their head
- the work would thrash from constant coordination

## `ralph` vs `team` vs `autopilot`

### `ralph`
Use when one persistent owner should keep pushing to completion.

### `team`
Use when parallel workers genuinely help.

### `autopilot`
Use when the whole pipeline should be managed end-to-end, and let it choose whether the execution phase should stay single-owner or fan out into a team.

## Tasks are not the boss

OpenClaw tasks are useful, but they are not the main runtime.
They are the ledger that tracks detached work.

Use them for:
- audit
- cancellation
- debugging
- checking whether detached work is stale or failed

Do not design the user experience around polling task ids all day.

## Hooks are not the boss either

Hooks are useful for:
- startup glue
- bootstrap reminders
- session lifecycle helpers
- extra memory capture

They are not the right place to build the actual team operating model.

## Official alignment

This model follows the OpenClaw direction described in the official docs for:
- subagents
- background tasks
- hooks

See:
- https://docs.openclaw.ai/tools/subagents
- https://docs.openclaw.ai/automation/tasks
- https://docs.openclaw.ai/cli/hooks
