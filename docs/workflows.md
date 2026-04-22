# Workflows

## Action-first default

Across workflows, the default is:

- continue through clear, low-risk, reversible local work
- ask only when blocked, destructive, irreversible, credential-gated, or materially scope-changing
- avoid weak permission-handoff endings that turn a clear next step into unnecessary user approval theater

## deep-interview

Use when the request is still ambiguous and you need crisp requirements before building.

## ralplan

Use when the task is large enough that planning mistakes would be expensive.

## ralph

Use when the task is clear and you want one persistent owner to keep iterating until done.

## autopilot

Use when you want the full pipeline: expansion, planning, execution, QA, and validation.
It may keep execution with one owner or fan out into `team` when the implementation phase is naturally partitionable.

## ultrawork

Use when you have several independent tasks that can run in parallel.

## ultraqa

Use when implementation exists and you want build, lint, test, and fix cycles.

## team

Use when the task can be decomposed across several coordinated workers.
In OpenClaw terms, that means one leader session coordinating detached worker subagents and then merging the results.

## Comparison

| Workflow | Best when | Main pattern |
|---|---|---|
| `deep-interview` | the request is vague | clarify first |
| `ralplan` | the plan is expensive to get wrong | deliberate before building |
| `ralph` | one owner should keep pushing until done | persistent single-owner execution |
| `team` | parallel workers genuinely help | leader + worker subagents |
| `autopilot` | the whole lifecycle should be managed end to end | expansion -> planning -> execution -> QA -> validation |
