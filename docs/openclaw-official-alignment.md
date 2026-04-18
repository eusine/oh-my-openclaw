# OpenClaw Official Alignment

Oh My OpenClaw is strongest when it adopts OpenClaw's actual runtime model instead of recreating an older system verbatim.

## Subagents

OpenClaw subagents are background runs spawned from an existing run. They announce their result back to the requester channel when finished.

Practical implication:
- team execution should use subagents as workers
- the main session should stay the orchestrator
- completion should be push-driven, not based on polling loops

## Background tasks

OpenClaw background tasks are a ledger for detached work.

Practical implication:
- use tasks to inspect, debug, cancel, or audit detached work
- do not treat tasks as the main interaction model for the user

## Hooks

OpenClaw hooks are event-driven automations around lifecycle events like startup, reset, and bootstrap.

Practical implication:
- use hooks for setup glue and maintenance automation
- do not build the core team runtime inside hooks

## Telegram-specific implication

Telegram is a good main control surface for natural-language workflow orchestration.
That means the best migration is not a HUD clone. It is a leader chat plus background workers plus concise announce-driven updates.

## Migration test

A team workflow is aligned when:
- leader logic stays in the main session
- workers are detached subagents
- completion comes back through announces
- tasks are audit surfaces
- hooks stay auxiliary
