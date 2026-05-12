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

Use when you want the strict reviewed delivery loop: `ralplan -> ralph -> code-review`. A non-clean review returns to `ralplan` with review findings as planning input; do not patch around review findings outside the loop.

## ultragoal

Use when a long task should be split into durable auditable goals with explicit acceptance criteria, dependencies, ledgers, and completion evidence.

New ultragoal runs default to an aggregate whole-run objective with per-story OpenClaw ledger checkpoints. Final completion requires targeted verification, cleanup/deslop evidence, post-cleanup verification, and a clean review. Non-clean review becomes a new blocker-resolution story.

## performance-goal

Use when the objective is measurable optimization and no work should start until an evaluator contract and baseline exist.

## autoresearch-goal

Use when a research mission needs durable source records, a professor/critic rubric, and a source-backed final report.

## ultrawork

Use when you have several independent tasks that can run in parallel.

## ultraqa

Use when implementation exists and you want build, lint, test, and fix cycles.

## team

Use when the task can be decomposed across several coordinated workers.
In OpenClaw terms, that means one leader session coordinating detached worker subagents and then merging the results.

## visual-ralph

Use when the task is frontend/UI implementation with a visual target: generated mockup, static reference, or live URL baseline. Visual Ralph requires an approved reference before implementation, then loops Ralph-style code edits through `visual-verdict`, screenshots, and optional pixel diff evidence until the UI matches and the design system is reproducible.

## visual-verdict

Use inside visual implementation loops when a generated screenshot must be judged against one or more reference images. It returns strict JSON with a 0-100 score, pass/revise/fail verdict, concrete differences, and next-edit suggestions.

## Comparison

| Workflow | Best when | Main pattern |
|---|---|---|
| `deep-interview` | the request is vague | clarify first |
| `ralplan` | the plan is expensive to get wrong | deliberate before building |
| `ralph` | one owner should keep pushing until done | persistent single-owner execution |
| `team` | parallel workers genuinely help | leader + worker subagents |
| `visual-ralph` | UI implementation needs visual fidelity | approved reference -> Ralph -> verdict loop |
| `visual-verdict` | screenshot/reference comparison is needed | strict JSON visual QA |
| `autopilot` | implementation needs reviewed autonomous delivery | ralplan -> ralph -> code-review |
| `ultragoal` | long work needs durable auditable objectives | goals.json + ledger + evidence |
| `performance-goal` | optimization must be evaluator-gated | baseline -> patch -> measure -> regressions |
| `autoresearch-goal` | research must be source-backed and rubric-checked | mission -> sources -> critic -> report |
