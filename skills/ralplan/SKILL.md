---
name: ralplan
description: "Consensus planning with planner → architect → critic deliberation cycle. Produces a PRD and test spec before any code is written. Use for anything beyond a simple fix."
argument-hint: "[--quick|--deep|--deliberate|--direct] <task description or spec path>"
user-invocable: true
---

<Purpose>
Ralplan is a structured consensus planning workflow. It runs a planner → architect → critic deliberation cycle to produce a high-quality implementation plan (PRD + test spec) before any execution begins. Multiple perspectives catch problems early, when they are cheap to fix.
</Purpose>

<Use_When>
- User says "ralplan", "consensus plan", "plan this before building", "plan --consensus"
- The task requires non-trivial implementation across multiple files or systems
- You want architectural validation before committing to an approach
- A deep-interview spec exists and needs to be turned into a concrete execution plan
- The request is large enough that a misaligned plan would be costly to fix
</Use_When>

<Do_Not_Use_When>
- Task is a simple bug fix or single-file change — delegate directly to an executor
- Requirements are still vague — run `deep-interview` first to clarify
- User asks to "just do it" with clear enough scope — use `ralph` or direct execution
- Task is a quick query or investigation with no implementation needed
</Do_Not_Use_When>

<Why_This_Exists>
Planning quality determines execution quality. A plan reviewed by only the planner misses architectural blind spots, over-engineering risks, and test coverage gaps. A planner → architect → critic cycle catches these before implementation, producing a plan that multiple perspectives have validated.
</Why_This_Exists>

<Pre_Execution_Gate>
Before starting the planning cycle, apply the pre-execution gate:

**Intercept condition:** the request has ≤15 effective words AND no concrete anchors (no file paths, no function names, no system names, no acceptance criteria, no constraint statements).

Examples that trigger the gate:
- "build something cool"
- "improve the API"
- "make it faster"

When triggered, do NOT proceed to planning. Instead:
1. Explain that the request needs more specificity for ralplan to produce a useful plan.
2. Ask one targeted clarifying question to identify the most important missing anchor.
3. Optionally offer to run `deep-interview` for full Socratic clarification.

**Bypass:** Prefix the request with `force:` or `!` to skip the gate and start planning immediately. Example: `force: improve the API`.

If a deep-interview spec exists at `.oh-my-openclaw/specs/deep-interview-{slug}.md`, skip the gate — the spec is already the anchor.
</Pre_Execution_Gate>

<Depth_Profiles>
- **Quick (`--quick`)**: planner only, no critic round — fast plan for low-risk tasks
- **Standard (default)**: full planner → architect → critic cycle
- **Deep (`--deep`)**: standard cycle + additional adversarial review round
- **Deliberate (`--deliberate`)**: RALPLAN-DR structured deliberation — highest rigor for high-stakes decisions
- **Direct (`--direct <spec-path>`)**: skip the interview/expansion, use the provided spec as input directly
</Depth_Profiles>

<Steps>

## Phase 0: Pre-Context Intake

1. Apply the **Pre-Execution Gate** (see above).
2. Derive task slug from request.
3. Check for existing spec: `.oh-my-openclaw/specs/deep-interview-{slug}.md` — if found, use it as planning input.
4. Check for existing plan: `.oh-my-openclaw/plans/ralplan-{slug}*.md` — if found and `--resume`, continue from last state.
5. Load or create context snapshot at `.oh-my-openclaw/context/{slug}-{timestamp}.md`.
6. Initialize state — write to `.oh-my-openclaw/state/ralplan-state.json`:

```json
{
  "active": true,
  "mode": "ralplan",
  "current_phase": "planning",
  "started_at": "<ISO timestamp>",
  "state": {
    "slug": "<slug>",
    "profile": "quick|standard|deep|deliberate",
    "input_spec": "<path or null>",
    "review_iteration": 0,
    "max_review_iterations": 5,
    "planner_complete": false,
    "architect_complete": false,
    "critic_complete": false,
    "approved": false
  }
}
```

## Phase 1: Planner — Generate PRD + Test Spec

Spawn a planner subagent (architect tier) to produce:

1. **PRD (Product Requirements Document)** covering:
   - Problem statement and motivation
   - Goals and non-goals
   - Functional requirements (numbered, testable)
   - Non-functional requirements (performance, security, compatibility)
   - Constraints and dependencies
   - Success criteria (how completion will be verified)
   - Out-of-scope items

2. **Test Spec** covering:
   - Unit test cases for each functional requirement
   - Integration test cases
   - Edge cases and failure modes
   - Acceptance test criteria

Output artifacts:
- `.oh-my-openclaw/plans/prd-{slug}.md`
- `.oh-my-openclaw/plans/test-spec-{slug}.md`

Update state: `planner_complete: true`.

### User Feedback Gate (optional)

If `--pause-after-planning` is set or the user previously asked to review plans before continuing:
- Present the PRD summary to the user
- Collect feedback
- Revise PRD before proceeding to architect review

## Phase 2: Architect — Technical Validation

Spawn an architect subagent to review the PRD and produce a technical implementation plan:

1. Review PRD for architectural soundness:
   - Is the approach technically feasible given existing constraints?
   - Are there missing dependencies or integration points?
   - Is the scope appropriately bounded?
   - Are there architectural risks or anti-patterns?

2. Produce technical specification:
   - Implementation approach and component breakdown
   - Data flow and API contracts
   - File/module structure changes
   - Migration or rollback plan (if applicable)
   - Performance and security considerations

Output artifact: `.oh-my-openclaw/plans/tech-spec-{slug}.md`

Update state: `architect_complete: true`.

## Phase 3: Critic — Adversarial Review

Spawn a critic subagent to challenge both the PRD and technical spec:

1. Attack the plan from adversarial angles:
   - What assumptions could be wrong?
   - What are the highest-risk implementation steps?
   - What is missing from the test spec?
   - Where could the plan fail silently?
   - What would need to change if a key assumption breaks?

2. Rate the plan: **APPROVED**, **NEEDS_REVISION**, or **REJECTED**

3. If **NEEDS_REVISION**:
   - List specific issues with priority (blocking vs. minor)
   - Return to Phase 1 with targeted revision guidance
   - Increment `review_iteration` counter
   - If `review_iteration >= max_review_iterations` (default 5): stop and escalate to user

4. If **REJECTED** (fundamental problem): stop, report what cannot be resolved without new requirements, offer to re-run `deep-interview`.

5. If **APPROVED**: proceed to Phase 4.

Update state: `critic_complete: true` (or `review_iteration++` if cycling).

## Phase 4: Deep Deliberation (if `--deliberate`)

For high-stakes decisions, run RALPLAN-DR structured deliberation:

1. Identify the top 3 contentious decisions in the plan.
2. For each decision, force explicit consideration of:
   - Best-case assumption
   - Worst-case assumption
   - Most likely outcome
   - Reversibility if wrong
3. Planner and architect subagents must explicitly agree or disagree on each.
4. Record decisions and rationale in `.oh-my-openclaw/plans/decisions-{slug}.md`.

## Phase 5: Final Approval Gate

1. Present the approved plan summary to the user (PRD, tech spec, test spec highlights).
2. Offer execution options:
   - **`autopilot`**: full automated pipeline (recommended for complex tasks)
   - **`ralph`**: persistent single-owner execution
   - **`team`**: coordinated parallel execution
   - **`ultrawork`**: parallel execution batch (no persistence)
   - **Revise plan**: return to planner with new constraints
3. Update state: `approved: true`, `active: false`, `completed_at: "<timestamp>"`.

</Steps>

<Output_Artifacts>
- `.oh-my-openclaw/plans/prd-{slug}.md` — Product Requirements Document
- `.oh-my-openclaw/plans/test-spec-{slug}.md` — Test specification
- `.oh-my-openclaw/plans/tech-spec-{slug}.md` — Technical implementation plan
- `.oh-my-openclaw/plans/decisions-{slug}.md` — Key decisions log (deliberate mode only)
</Output_Artifacts>

<State_Management>
State file: `{workspace}/.oh-my-openclaw/state/ralplan-state.json`

- **On start:** write initial state with `active: true`
- **On each phase:** update `current_phase` and phase-specific flags
- **On revision cycle:** increment `review_iteration`
- **On completion:** set `active: false`, `approved: true`, `completed_at`
- **On resume:** read existing state and continue from last phase
</State_Management>

<Tool_Usage>
- Spawn planner subagent for Phase 1 (architect tier, thorough)
- Spawn architect subagent for Phase 2 (thorough)
- Spawn critic subagent for Phase 3 (thorough, opus tier for --deliberate)
- Write plan artifacts to `.oh-my-openclaw/plans/` using file write tools
- Use file read tools to load existing specs and context
</Tool_Usage>

<Flags>
- `--quick`: planner only, skip architect and critic rounds
- `--deep`: standard cycle + additional adversarial review round
- `--deliberate`: RALPLAN-DR structured deliberation (highest rigor)
- `--direct <spec>`: use provided spec as direct planning input, skip expansion
- `--pause-after-planning`: stop for user review after planner phase
</Flags>
