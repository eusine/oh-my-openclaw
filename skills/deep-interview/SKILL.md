---
name: deep-interview
description: "Socratic deep interview with mathematical ambiguity gating before planning or execution. Use when requirements are vague, ambiguous, or missing concrete acceptance criteria."
argument-hint: "[--quick|--standard|--deep] [--autoresearch] <idea or vague description>"
user-invocable: true
---

<Purpose>
Deep Interview is an intent-first Socratic clarification loop before planning or implementation. It turns vague ideas into execution-ready specifications by asking targeted questions about why the user wants a change, how far it should go, what should stay out of scope, and what may be decided without confirmation.
</Purpose>

<Use_When>
- The request is broad, ambiguous, or missing concrete acceptance criteria **and** one reasonable assumption or one targeted clarifying question would still leave major cost/risk of misalignment
- The user says "deep interview", "interview me", "ask me everything", "don't assume", or "ouroboros"
- The user wants to avoid misaligned implementation from underspecified requirements
- You need a requirements artifact before handing off to `ralplan`, `autopilot`, `ralph`, or `team`
</Use_When>

<Do_Not_Use_When>
- The request already has concrete file/symbol targets and clear acceptance criteria
- The user explicitly asks to skip planning/interview and execute immediately
- The user asks for lightweight brainstorming only, use a lightweight thinking pass instead
- A complete PRD/plan already exists and execution should start
- One reasonable assumption would unblock execution safely
- A single high-leverage clarifying question would make the task actionable enough to proceed
</Do_Not_Use_When>

<Why_This_Exists>
Execution quality is usually bottlenecked by intent clarity, not just missing implementation detail. A single expansion pass often misses why the user wants a change, where the scope should stop, which tradeoffs are unacceptable, and which decisions still require user approval. This workflow applies Socratic pressure + quantitative ambiguity scoring so orchestration modes begin with an explicit, testable, intent-aligned spec.
</Why_This_Exists>

<Depth_Profiles>
- **Quick (`--quick`)**: fast pre-PRD pass; target threshold `<= 0.30`; max rounds 5
- **Standard (`--standard`, default)**: full requirement interview; target threshold `<= 0.20`; max rounds 12
- **Deep (`--deep`)**: high-rigor exploration; target threshold `<= 0.15`; max rounds 20
- **Autoresearch (`--autoresearch`)**: same interview rigor as Standard, but specialized for research mission handoff and `.oh-my-openclaw/specs/` artifact generation

If no flag is provided, use **Standard**.

<Mode_Flags>
- **`--autoresearch`**: switch the interview into research-intake mode. The interview should converge on a clear research mission, write canonical artifacts under `.oh-my-openclaw/specs/`, and preserve the explicit `refine further` vs `launch` boundary for downstream intake.
</Mode_Flags>
</Depth_Profiles>

<Execution_Policy>
- Treat deep-interview as a last-mile clarification workflow, not the default response to ordinary incompleteness
- Before entering deep-interview, first ask: can I safely proceed by making one reasonable assumption or by asking one targeted clarifying question? If yes, do that instead
- Never auto-route into deep-interview solely because the prompt is short, casual, or lacks a full spec
- Ask ONE question per round (never batch multiple questions in one round)
- Ask about intent and boundaries before implementation detail
- Target the weakest clarity dimension each round after applying stage-priority rules below
- Treat every answer as a claim to pressure-test: the next question should demand evidence, expose a hidden assumption, force a tradeoff, or reframe root cause vs symptom rather than settling for surface-level clarification only
- Do not rotate to a new clarity dimension just for coverage when the current answer is still vague; stay on the same thread until one layer deeper, one assumption clearer, or one boundary tighter
- Before crystallizing, complete at least one explicit pressure pass that revisits an earlier answer with a deeper or tradeoff-focused follow-up
- Gather codebase facts via direct file read/search tools before asking the user about internals
- Reduce user effort: ask only the highest-leverage unresolved question; never ask the user for codebase facts that can be discovered directly
- For brownfield work, prefer evidence-backed confirmation questions: "I found X in Y. Should this change follow that pattern?"
- Use AskUserQuestion for each interview round when available; if unavailable, create a structured question record with `scripts/oh-my-openclaw-question.py ask ...`, let required questions mint a linked question obligation automatically, then ask the same single question in plain chat with the question id attached
- Re-score ambiguity after each answer and show progress transparently
- Do not hand off to execution while ambiguity remains above threshold unless user explicitly opts to proceed with warning
- Do not crystallize or hand off while `Non-goals` or `Decision Boundaries` remain unresolved, even if the weighted ambiguity threshold is met
- If a complete PRD or execution-ready plan already exists, do not redo discovery unless the user explicitly asks for another clarification pass
- Respect requested depth profile behavior, especially quick-mode thresholds and round limits
- Persist mode state for resume safety (write to `.oh-my-openclaw/state/deep-interview-state.json`)
</Execution_Policy>

<Steps>

## Phase 0: Preflight Context Intake

1. Parse the input and derive a short task slug (lowercase, hyphenated).
2. Attempt to load the latest relevant context snapshot from `.oh-my-openclaw/context/{slug}-*.md`.
3. If no snapshot exists, create a minimum context snapshot with:
   - Task statement
   - Desired outcome
   - Stated solution (what the user asked for)
   - Probable intent hypothesis (why they likely want it)
   - Known facts/evidence
   - Constraints
   - Unknowns/open questions
   - Decision-boundary unknowns
   - Likely codebase touchpoints
4. Save snapshot to `.oh-my-openclaw/context/{slug}-{timestamp}.md` (UTC `YYYYMMDDTHHMMSSZ`).

## Phase 1: Initialize

1. Parse input and depth profile (`--quick|--standard|--deep`).
2. Detect project context:
   - Use file read/search tools to classify **brownfield** (existing codebase) vs **greenfield**.
   - For brownfield, collect relevant codebase context before questioning.
3. Initialize state — write to `.oh-my-openclaw/state/deep-interview-state.json`:

```json
{
  "active": true,
  "mode": "deep-interview",
  "current_phase": "deep-interview",
  "started_at": "<ISO timestamp>",
  "state": {
    "interview_id": "<uuid>",
    "profile": "quick|standard|deep",
    "type": "greenfield|brownfield",
    "initial_idea": "<user input>",
    "rounds": [],
    "current_ambiguity": 1.0,
    "threshold": 0.3,
    "max_rounds": 5,
    "challenge_modes_used": [],
    "codebase_context": null,
    "current_stage": "intent-first",
    "current_focus": "intent",
    "context_snapshot_path": ".oh-my-openclaw/context/<slug>-<timestamp>.md",
    "pending_question_id": null,
    "pending_question_obligation_id": null,
    "question_state_root": ".oh-my-openclaw/state/questions",
    "question_obligation_root": ".oh-my-openclaw/state/question-obligations",
    "run_outcome": "continue"
  }
}
```

4. Announce kickoff with profile, threshold, and current ambiguity.

## Phase 2: Socratic Interview Loop

Repeat until ambiguity `<= threshold`, pressure pass complete, readiness gates explicit, user exits with warning, or max rounds reached.

### 2a) Generate next question

Use:
- Original idea
- Prior Q&A rounds
- Current dimension scores
- Brownfield context (if any)
- Activated challenge mode injection (Phase 3)

Target the lowest-scoring dimension, but respect stage priority:
- **Stage 1 — Intent-first:** Intent, Outcome, Scope, Non-goals, Decision Boundaries
- **Stage 2 — Feasibility:** Constraints, Success Criteria
- **Stage 3 — Brownfield grounding:** Context Clarity (brownfield only)

Follow-up pressure ladder after each answer:
1. Ask for a concrete example, counterexample, or evidence signal behind the latest claim
2. Probe the hidden assumption, dependency, or belief that makes the claim true
3. Force a boundary or tradeoff: what would you explicitly not do, defer, or reject?
4. If the answer still describes symptoms, reframe toward essence / root cause before moving on

Prefer staying on the same thread for multiple rounds when it has the highest leverage.

Detailed dimensions:
- **Intent Clarity** — why the user wants this
- **Outcome Clarity** — what end state they want
- **Scope Clarity** — how far the change should go
- **Constraint Clarity** — technical or business limits that must hold
- **Success Criteria Clarity** — how completion will be judged
- **Context Clarity** — existing codebase understanding (brownfield only)

`Non-goals` and `Decision Boundaries` are mandatory readiness gates. Ask about them early.

### 2b) Ask the question

Before sending the question:
- create or update a question record under `.oh-my-openclaw/state/questions/` with `scripts/oh-my-openclaw-question.py ask --workflow deep-interview --slug <slug> --interview-id <uuid> --required ...`
- if the question is required, persist the returned `obligation_id` into `pending_question_obligation_id` as the fail-closed ledger entry
- persist the returned `question_id` into `pending_question_id`
- if AskUserQuestion is unavailable, include the question id in the plain-chat prompt so resume and Stop gating stay anchored to the owned record

Present to the user:

```
Round {n} | Target: {weakest_dimension} | Ambiguity: {score}% | Question ID: {question_id}

{question}
```

### 2c) Score ambiguity

Score each weighted dimension in `[0.0, 1.0]` with justification + gap.

**Greenfield:** `ambiguity = 1 - (intent × 0.30 + outcome × 0.25 + scope × 0.20 + constraints × 0.15 + success × 0.10)`

**Brownfield:** `ambiguity = 1 - (intent × 0.25 + outcome × 0.20 + scope × 0.20 + constraints × 0.15 + success × 0.10 + context × 0.10)`

Readiness gates:
- `Non-goals` must be explicit
- `Decision Boundaries` must be explicit
- A pressure pass must be complete (at least one earlier answer revisited with evidence, assumption, or tradeoff follow-up)
- If either gate is unresolved or pressure pass is incomplete, continue even when weighted ambiguity is below threshold

### 2d) Report progress

Show weighted breakdown table, readiness-gate status, and next focus dimension.

### 2e) Persist state

Append round result and updated scores to `.oh-my-openclaw/state/deep-interview-state.json`.
When the user answers, record it with `scripts/oh-my-openclaw-question.py answer <question_id> ...`. After the answer has been consumed into the interview state, satisfy the linked obligation with `scripts/oh-my-openclaw-question.py satisfy-obligation <obligation_id> --question-id <question_id>`, then clear `pending_question_id` and `pending_question_obligation_id`.

### 2f) Round controls

- Do not offer early exit before the first explicit assumption probe and one persistent follow-up
- Round 4+: allow explicit early exit with risk warning
- Soft warning at profile midpoint (round 3/6/10 depending on profile)
- Hard cap at profile `max_rounds`

## Phase 3: Challenge Modes (assumption stress tests)

Use each mode once when applicable. Normal escalation tools, not rare rescue moves:

- **Contrarian** (round 2+ or immediately when an answer rests on untested assumption): challenge core assumptions
- **Simplifier** (round 4+ or when scope expands faster than outcome clarity): probe minimal viable scope
- **Ontologist** (round 5+ and ambiguity > 0.25, or when user keeps describing symptoms): ask for essence-level reframing

Track used modes in state to prevent repetition.

## Phase 4: Crystallize Artifacts

When threshold is met (or user exits with warning / hard cap):

1. Write interview transcript summary to `.oh-my-openclaw/interviews/{slug}-{timestamp}.md`
2. Write execution-ready spec to `.oh-my-openclaw/specs/deep-interview-{slug}.md`

Spec should include:
- Metadata (profile, rounds, final ambiguity, threshold, context type)
- Context snapshot reference/path
- Clarity breakdown table
- Intent (why the user wants this)
- Desired Outcome
- In-Scope
- Out-of-Scope / Non-goals
- Decision Boundaries (what may be decided without confirmation)
- Constraints
- Testable acceptance criteria
- Assumptions exposed + resolutions
- Pressure-pass findings
- Brownfield evidence vs inference notes
- Technical context findings
- Full or condensed transcript

### Autoresearch specialization

When invoked with `--autoresearch`, focus the interview on research mission clarity:
- **Accepted inputs:** topic, evaluator, keep-policy, slug, existing mission draft, prior evaluator examples
- **Required focus:** mission clarity, evaluator readiness, keep policy, slug/session naming
- **Canonical artifact path:** `.oh-my-openclaw/specs/deep-interview-autoresearch-{slug}.md`
- **Launch artifact bundle:** `.oh-my-openclaw/specs/autoresearch-{slug}/mission.md`, `sandbox.md`, `result.json`
- **Mark as not launch-ready** while evaluator command contains `<...>`, `TODO`, `TBD`, `REPLACE_ME`, `CHANGEME`
- **result.json** should carry finalized `topic`, `evaluatorCommand`, `keepPolicy`, `slug`, `launchReady`, `blockedReasons`
- **Confirmation bridge:** offer at least `refine further` and `launch`; do not launch until user explicitly confirms

## Phase 5: Execution Bridge

Present execution options after artifact generation. Treat the spec as requirements source of truth and preserve intent, non-goals, decision boundaries, acceptance criteria, and residual-risk warnings across the handoff.

### 1. `ralplan` (Recommended)
- **Input:** `.oh-my-openclaw/specs/deep-interview-{slug}.md`
- **When:** Requirements are clear, but architectural validation / consensus planning still desirable
- **Consumer:** Treats the spec as requirements source of truth; does not repeat the interview

### 2. `autopilot`
- **Input:** `.oh-my-openclaw/specs/deep-interview-{slug}.md`
- **When:** Clarified spec is strong enough for direct planning + execution without additional consensus gate

### 3. `ralph`
- **Input:** `.oh-my-openclaw/specs/deep-interview-{slug}.md`
- **When:** Task benefits from persistent sequential completion pressure

### 4. `team`
- **Input:** `.oh-my-openclaw/specs/deep-interview-{slug}.md`
- **When:** Task is large, multi-lane, or blocker-sensitive enough to justify coordinated parallel execution

### 5. Refine further
- **When:** Residual ambiguity is too high or the user wants stronger clarity

**Residual-Risk Rule:** If the interview ended via early exit, hard-cap completion, or above-threshold proceed-with-warning, explicitly preserve that residual-risk state in the handoff so the downstream skill knows it inherited a partially clarified brief.

**IMPORTANT:** Deep-interview is a requirements mode. On handoff, invoke the selected skill. **Do NOT implement directly** inside deep-interview.

</Steps>

<State_Management>
State file: `{workspace}/.oh-my-openclaw/state/deep-interview-state.json`

- **On start:** write state JSON with `active: true` and `run_outcome: "continue"`
- **On each round:** update `rounds` array, `current_ambiguity`, and any `pending_question_obligation_id`
- **On completion:** update `active: false`, set `completed_at`, and normalize `run_outcome` through `scripts/oh-my-openclaw-run-outcome.py apply`
- **On handoff:** preserve state for downstream skill context and fail closed if `obligation-blockers` still reports a pending required question
- **On resume:** read existing state file and continue from last round
</State_Management>

<Tool_Usage>
- Use file read and search tools (Read, Grep, Glob) for codebase fact gathering — do not ask the user for facts that can be discovered directly
- Use AskUserQuestion for each interview round when available; otherwise use `scripts/oh-my-openclaw-question.py` to own the question lifecycle and fall back to plain-text single-question turns
- Write artifacts using file write tools to `.oh-my-openclaw/` paths in the workspace
- Use `scripts/oh-my-openclaw-question.py blockers --workflow deep-interview --slug <slug>` before stopping if you only need unanswered question records
- Use `scripts/oh-my-openclaw-question.py obligation-blockers --workflow deep-interview --slug <slug>` before stopping or handing off so answered-but-unconsumed required questions still block correctly
- Use `scripts/oh-my-openclaw-run-outcome.py apply` when writing terminal vs resumable deep-interview state so downstream resume logic sees one normalized contract
</Tool_Usage>
