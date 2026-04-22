# Oh My OpenClaw Self-Evolution MVP

Status: revived for migration  
Date: 2026-04-14
Updated: 2026-04-20

## Reference upstream

Reference upstream for the new migration lane:
- `external/hermes-agent-self-evolution/`
- upstream repo: `https://github.com/NousResearch/hermes-agent-self-evolution`

Migration stance:
- reuse Hermes-style evaluation loop ideas aggressively, not just the narrow early MVP slice
- merge them with the existing Oh My OpenClaw workflow layer under the **Oh My OpenClaw** brand
- keep OpenClaw-native filesystem layout and human review gates
- treat skills, tool descriptions, prompt sections, workflow docs, helper prompts, and guarded code lanes as valid long-term optimization targets

## Goal

Turn self-evolution into a real **Oh My OpenClaw operating capability**, not just a narrow skill-tuning experiment.

The system should be able to:
- discover recurring friction from conversations, memory, git history, and eval traces
- convert that friction into explicit optimization targets
- improve the right layer, which may be a skill, tool description, prompt section, helper document, routing rule, or guarded code path
- produce reviewable candidate changes with evidence instead of vague self-reflection
- keep humans in control of promotion, rollback, and safety boundaries

Phase 1 still matters, but it is now explicitly understood as the first live lane inside a broader stack.

Current live status as of 2026-04-20:
- `autopilot`, `ralph`, and `deep-interview` are the active first live skill targets
- phase 2 tool-description optimization has already landed a first local promotion
- phase 3 prompt-section evolution and phase 4 guarded code scaffolding both have live promoted local slices
- phase 5 now emits a `next_focus` recommendation instead of stopping at a passive queue
- the next structural step is to widen target discovery and import more of the Hermes operating model into the Oh My OpenClaw surface

## Non-goals

- No silent live auto-merge to production artifacts
- No uncontrolled background self-modification loop
- No bypass of human review for risky or irreversible changes
- No model-fine-tuning pipeline
- No replacing official memory, wiki, or QMD workflows
- No pretending every improvement should target the core OpenClaw runtime first

## Why not a full port

A full Hermes port would likely drag in orchestration assumptions that do not fit OpenClaw well: different runtime boundaries, different memory policy, different skills layout, and different safety expectations.

OpenClaw already has strong primitives, sessions, skills, markdown docs, an official memory-wiki plus QMD knowledge path, and explicit human approval. The MVP should reuse those instead of recreating Hermes end to end.

Recommendation: port the loop, not the whole substrate.

## Operating scope

The live work is no longer framed as “skill-only self-evolution”.

### Current implemented lane

Phase 1 remains the first mature live lane: **skill-instruction evolution**.

In scope today:
- choose target skills with measurable behavior
- store benchmark tasks and expected rubrics
- run baseline evals
- ask a model to propose instruction-only improvements
- materialize candidates as markdown diffs
- re-run evals and compare to baseline
- keep winning candidates in a review queue for human merge

### Wider target surface we are explicitly importing

Beyond phase 1, the Oh My OpenClaw self-evolution stack should cover:
- tool descriptions and parameter guidance
- selected system-prompt sections with clear rollback boundaries
- helper prompts, mutation briefs, gate docs, and routing heuristics
- reusable workflow documents and state contracts
- guarded code lanes where tests and bug repros exist
- detection layers that mine conversation history, memory, git history, and run artifacts for new improvement opportunities

### Out of scope even after widening

- autonomous rollout straight into live production behavior without review
- edits to arbitrary unregistered files with no artifact boundary
- “improve everything” mutation with no measurable target or rollback path

## Recommended options

### Option A, minimal
Run a manual batch script that evaluates one skill, proposes one candidate, and writes a patch preview.
- Effort: low
- Risk: low
- Good for: proving the loop works

### Option B, recommended MVP
Add a small local pipeline for dataset -> eval -> candidate generation -> re-eval -> review artifact.
- Effort: medium
- Risk: moderate but controllable
- Good for: actual repeated use without large platform changes

### Option C, broader port
Recreate Hermes-style autonomous optimizer with schedulers, broader mutation targets, and automated promotion.
- Effort: high
- Risk: high
- Not recommended now

## Chosen approach

**Option B**.

It is large enough to validate real improvement, but small enough to keep rollback cheap. If the optimizer is noisy, we can discard candidate docs and keep all production skills unchanged.

## Attack check on the recommendation

- Dependency failure: if model generation fails, eval-only mode still works and no skill changes are proposed.
- Scale explosion: dataset growth will first stress eval runtime, not production behavior. Keep phase 1 capped to a few skills and tens of tasks.
- Rollback cost: near zero, because output is just candidate markdown patches until a human merges them.
- Premise collapse: the fragile assumption is that instruction edits alone can move metrics. If false, phase 1 still yields a clean eval harness, which is useful by itself.

## Directory mapping, Hermes -> OpenClaw

This is conceptual mapping, not a file-for-file port.

| Hermes concept | OpenClaw MVP home |
|---|---|
| evolution loop / optimizer | `scripts/self_evolve.py` or `scripts/self_evolve.ts` |
| seed prompts / mutation targets | `skills/<skill>/SKILL.md` |
| benchmark tasks | `state/self-evolution/datasets/<skill>.jsonl` |
| eval outputs / metrics | `state/self-evolution/runs/<timestamp>/` |
| candidate generations | `state/self-evolution/candidates/<timestamp>/` |
| approved improvements | normal edits to `skills/.../SKILL.md` via human review |
| experiment notes | `docs/openclaw-skill-self-evolution-mvp.md` and follow-up docs |
| durable learnings | official memory wiki page/synthesis or workspace state doc after human acceptance |

If a reusable package emerges later, move runtime code into `scripts/` plus a small helper module. Do not invent a large new service for phase 1.

## Core components to build

1. **Dataset loader**
   - Reads benchmark cases for a target skill
   - Case includes prompt, allowed tools, expected rubric, and failure checks

2. **Eval runner**
   - Runs baseline behavior for each case
   - Produces structured outputs: score, notes, token/runtime cost, hard-fail flags

3. **Candidate generator**
   - Takes current `SKILL.md`, failure summary, and constraints
   - Produces revised instruction text only
   - Must not touch runtime code or global policies

4. **Patch materializer**
   - Writes candidate skill variants and unified diffs
   - Keeps originals untouched

5. **Comparator**
   - Re-runs evals on candidates
   - Requires non-regression on hard gates and net gain on target metric

6. **Review pack generator**
   - Emits concise markdown summary: baseline vs candidate, failures fixed, regressions, diff link

## Eval and data pipeline

```text
skill SKILL.md
   -> benchmark dataset
   -> baseline eval run
   -> failure summary
   -> candidate instruction revision
   -> candidate eval run
   -> compare against baseline
   -> review pack
   -> human approve or discard
```

Minimum dataset shape:
- `case_id`
- `target_skill`
- `user_input`
- `expected_signals`
- `forbidden_signals`
- `score_rubric`
- optional `gold_answer` or `reference_notes`

Metrics for MVP:
- pass rate
- average rubric score
- hard-fail count
- cost per run
- regression count vs baseline

## Constraints and gates

Hard gates:
- no automatic merge to live `SKILL.md`
- no edits outside approved target skill files
- no degradation on safety/tool-compliance cases
- all candidate changes must be diffable and human-readable
- every run logged under `state/self-evolution/runs/`
- redact or sanitize conversation-derived, memory-derived, and review-pack evidence before it becomes a durable dataset, candidate context, or review artifact

Soft gates:
- only evolve one skill family at a time
- cap candidate count per run, for example 3 to 5
- prefer larger batch evals over chatty per-case mutation loops
- document accepted learnings in the official memory wiki or state after merge

## Recommended rollout

1. Start with one high-leverage but low-risk skill, ideally a planning or writing skill.
2. Build a small hand-curated dataset, around 20 to 40 cases.
3. Run baseline and verify the scorer catches obvious failures.
4. Generate at most 3 candidates per run.
5. Human reviews the best candidate diff and summary.
6. Merge only after non-regression on safety and style checks.
7. Add a second skill only after the first lane produces at least one clear win.

## 1-week MVP plan

### Day 1
- Pick first target skill
- Define eval rubric and dataset schema
- Create initial 20 to 40 benchmark cases

### Day 2
- Implement dataset loader and baseline eval runner
- Save structured run artifacts under `state/self-evolution/`

### Day 3
- Implement candidate generator for `SKILL.md` revisions only
- Add patch materialization and diff output

### Day 4
- Implement candidate re-eval and comparator
- Add hard non-regression gates

### Day 5
- Run first full end-to-end experiment on one skill
- Inspect false positives and tighten rubric

### Day 6
- Add review-pack markdown output
- Clean up prompts, logging, and run naming

### Day 7
- Decide go/no-go for phase 2
- If go, merge one reviewed improvement and document lessons learned

## Final recommendation

## Phase 2 slice

The first phase-2 step should stay narrow: add a small artifact registry so the loop can target registered documents instead of only a skill path.

Recommended first supported artifact types:
- `skill_instruction`, for `skills/*/SKILL.md`
- `prompt_template`, for mutation briefs like `docs/self-evolution/candidate-prompt.md`
- `constraint_doc`, for human-reviewed gate files like `state/self-evolution/constraints/phase1-gates.yaml`

Keep the same gates:
- registry-backed target selection
- candidate files written under `state/self-evolution/candidates/`
- no in-place edits to live artifacts
- human review pack required before any merge

This gives OpenClaw one reusable abstraction layer without jumping to repo-wide self-modification.

## Integration update, 2026-04-20

The target shape is to bring over the useful parts of Hermes-style self-evolution and integrate them into **Oh My OpenClaw** as one coherent OpenClaw-native system.

In practice that means:

- treat Hermes as a source of optimizer architecture, dataset ideas, prompt-section targeting, tool-description evolution, monitoring concepts, and guarded code-evolution patterns
- treat the existing Oh My OpenClaw workflow layer as the source of live workflow ergonomics, operator-facing routines, and runtime helper patterns already centered on `.oh-my-openclaw/`
- unify both into one OpenClaw-native system instead of keeping “workflow” and “self-evolution” as separate mental products

## Final recommendation

Build Oh My OpenClaw self-evolution as a **local, human-gated operating-system improvement layer**.

Start with the already-working live lanes, but do not conceptually trap the system at skill tuning. The real target is broader: a repo-aware, memory-aware, conversation-aware improvement loop that can discover friction, choose the right artifact boundary, generate reviewable candidates, and keep getting sharper over time.
