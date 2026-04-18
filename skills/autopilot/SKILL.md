---
name: autopilot
description: "Full autonomous execution from idea to working code. Handles requirements expansion, consensus planning, parallel implementation, QA cycling, and multi-perspective validation."
argument-hint: "<idea, task description, or spec path>"
user-invocable: true
---

<Purpose>
Autopilot takes a brief product idea and autonomously handles the full lifecycle: requirements analysis, technical design, planning, parallel implementation, QA cycling, and multi-perspective validation. It produces working, verified code from a 2-3 line description.
</Purpose>

<Use_When>
- User wants end-to-end autonomous execution from an idea to working code
- User says "autopilot", "auto pilot", "autonomous", "build me", "create me", "make me", "full auto", "handle it all", or "I want a/an..."
- Task requires multiple phases: planning, coding, testing, and validation
- User wants hands-off execution and is willing to let the system run to completion
</Use_When>

<Do_Not_Use_When>
- User wants to explore options or brainstorm, use a lightweight thinking pass instead
- User says "just explain", "draft only", or "what would you suggest" — respond conversationally
- User wants a single focused code change — use `ralph` or delegate to an executor subagent
- User wants to review or critique an existing plan, use a review pass instead
- Task is a quick fix or small bug — use direct executor delegation
</Do_Not_Use_When>

<Why_This_Exists>
Most non-trivial software tasks require coordinated phases: understanding requirements, designing a solution, implementing in parallel, testing, and validating quality. Autopilot orchestrates all of these phases automatically so the user can describe what they want and receive working code without managing each step.
</Why_This_Exists>

<Execution_Policy>
- Each phase must complete before the next begins
- Parallel execution is used within phases where possible (Phase 2 and Phase 4)
- QA cycles repeat up to 5 times; if the same error persists 3 times, stop and report the fundamental issue
- Validation requires approval from all reviewers; rejected items get fixed and re-validated
- If a deep-interview spec exists, use it as high-clarity phase input instead of re-expanding from scratch
- If input is too vague for reliable expansion, offer/trigger `deep-interview` first
- Default to concise, evidence-dense progress and completion reporting
- Continue through clear, low-risk, reversible next steps automatically; ask only when the next step is materially branching, destructive, or preference-dependent
</Execution_Policy>

<Steps>

## Pre-Context Intake (required before Phase 0)

1. Derive a task slug from the request.
2. Load the latest relevant snapshot from `.oh-my-openclaw/context/{slug}-*.md` when available.
3. If no snapshot exists, create `.oh-my-openclaw/context/{slug}-{timestamp}.md` (UTC `YYYYMMDDTHHMMSSZ`) with:
   - Task statement
   - Desired outcome
   - Known facts/evidence
   - Constraints
   - Unknowns/open questions
   - Likely codebase touchpoints
4. If ambiguity remains high, use direct file search tools for brownfield facts, then run `deep-interview --quick <task>` before proceeding.
5. Initialize state — write to `.oh-my-openclaw/state/autopilot-state.json`:

```json
{
  "active": true,
  "mode": "autopilot",
  "current_phase": "expansion",
  "started_at": "<ISO timestamp>",
  "state": {
    "slug": "<slug>",
    "context_snapshot_path": ".oh-my-openclaw/context/<slug>-<timestamp>.md",
    "qa_cycle": 0,
    "max_qa_cycles": 5,
    "validation_round": 0,
    "max_validation_rounds": 3
  }
}
```

## Phase 0 — Expansion: Turn the idea into a detailed spec

- If `.oh-my-openclaw/specs/deep-interview-{slug}.md` exists: reuse it and skip redundant expansion
- If prompt is highly vague: route to `deep-interview --quick` for clarification
- Spawn analyst subagent (thorough tier): extract requirements
- Spawn architect subagent (thorough tier): create technical specification
- Output: `.oh-my-openclaw/plans/autopilot-spec.md`
- Update state: `current_phase: "planning"`

## Phase 1 — Planning: Create implementation plan from spec

- Spawn architect subagent (thorough tier): create plan (no interview, direct mode)
- Spawn critic subagent (thorough tier): validate plan
- Revise plan if critic raises blocking issues
- Output: `.oh-my-openclaw/plans/autopilot-impl.md`
- Update state: `current_phase: "execution"`

## Phase 2 — Execution: Implement the plan

Delegate using `ralph` for persistence or `ultrawork` for parallel batch:

- Route subtasks by complexity:
  - Simple lookups/writes → executor (standard tier)
  - Standard implementation → executor (standard tier)
  - Complex analysis/refactoring → executor (thorough tier) or architect
- Run independent tasks in parallel simultaneously
- Background long-running operations (builds, installs)
- Update state: `current_phase: "qa"` when implementation complete

## Phase 3 — QA: Cycle until all tests pass

Run `ultraqa` internally:

1. Build → lint → test
2. Collect failures
3. Fix failures via parallel executor subagents
4. Re-run to verify
5. Repeat up to `max_qa_cycles` (default 5)
6. If same error persists across 3 cycles → stop and report fundamental issue
7. Update state: `current_phase: "validation"` when QA passes

## Phase 4 — Validation: Multi-perspective review in parallel

Spawn all reviewers simultaneously:

- **Architect subagent**: functional completeness review
- **Security-reviewer subagent**: vulnerability check
- **Code-reviewer subagent**: quality review

All must approve. On rejection:
1. Fix the specific issues raised
2. Increment `validation_round`
3. Re-validate with the reviewing subagent
4. If `validation_round >= max_validation_rounds` → stop and escalate to user

Update state: `current_phase: "cleanup"` when all reviewers approve.

## Phase 5 — Cleanup: Clear state and report

1. Update state: `active: false`, `current_phase: "complete"`, `completed_at: "<timestamp>"`
2. Remove or archive `.oh-my-openclaw/state/autopilot-state.json`
3. Report completion:
   - Summary of what was built
   - Files created/modified
   - Test results
   - Validation outcomes
   - Any known follow-up items

</Steps>

<State_Management>
State file: `{workspace}/.oh-my-openclaw/state/autopilot-state.json`

- **On start:** write initial state with `active: true`, `current_phase: "expansion"`, `updated_at: <ISO timestamp>`
- **On phase transitions:** update `current_phase` and **always update `updated_at`**
- **On QA cycles:** increment `qa_cycle`, update `updated_at`
- **On validation rounds:** increment `validation_round`, update `updated_at`
- **On completion:** set `active: false`, `completed_at`, `updated_at`
- **On resume:** read existing state, verify phase output artifacts exist before continuing, then continue from last phase

**`updated_at` is required on every write.** The oh-my-openclaw harness hook uses it to distinguish live vs abandoned states (> 48h = stale warning).

**Atomic write pattern:** write state to a temp file (`.oh-my-openclaw/state/autopilot-state.json.tmp`), then rename to final path. This prevents partial-write corruption on crash.

**Resume verification:** before resuming a phase, confirm its expected output exists (e.g., phase `execution` should have `.oh-my-openclaw/plans/autopilot-impl.md`). If output is missing, re-run that phase rather than skipping it.
</State_Management>

<Escalation_And_Stop_Conditions>
- Stop when the same QA error persists across 3 cycles (fundamental issue)
- Stop when validation keeps failing after `max_validation_rounds` rounds
- Stop when user says "stop", "cancel", or "abort"
- If requirements were too vague and expansion produces an unclear spec, pause and redirect to `deep-interview`
</Escalation_And_Stop_Conditions>

<Final_Checklist>
- [ ] All 5 phases completed (Expansion, Planning, Execution, QA, Validation)
- [ ] All validators approved in Phase 4
- [ ] Tests pass (verified with fresh test run output)
- [ ] Build succeeds (verified with fresh build output)
- [ ] State files cleaned up
- [ ] User informed of completion with summary of what was built
</Final_Checklist>

<Examples>
<Good>
User: "autopilot A REST API for a bookstore inventory with CRUD operations using TypeScript"
Why: Specific domain, clear features, technology constraint. Autopilot has enough to expand into a full spec.
</Good>

<Good>
User: "build me a CLI tool that tracks daily habits with streak counting"
Why: Clear product concept with a specific feature. "build me" trigger activates autopilot.
</Good>

<Bad>
User: "fix the bug in the login page"
Why: Single focused fix, not a multi-phase project. Use direct executor delegation or ralph instead.
</Bad>

<Bad>
User: "what are some good approaches for adding caching?"
Why: Exploration or brainstorming request. Respond conversationally or use a lightweight thinking pass.
</Bad>
</Examples>

<Tool_Usage>
- Spawn analyst subagent (thorough) for Phase 0 requirements extraction
- Spawn architect subagent (thorough) for Phase 0 spec + Phase 1 plan
- Spawn critic subagent (thorough) for Phase 1 validation
- Use `ralph` or `ultrawork` for Phase 2 execution delegation
- Use `ultraqa` for Phase 3 QA cycling
- Spawn architect, security-reviewer, code-reviewer subagents in parallel for Phase 4
- Use file write tools for all artifact creation under `.oh-my-openclaw/`
</Tool_Usage>

<Recommended_Clarity_Pipeline>
For ambiguous requests, prefer:

```
deep-interview → ralplan → autopilot
```

- `deep-interview`: ambiguity-gated Socratic requirements
- `ralplan`: consensus planning (planner/architect/critic)
- `autopilot`: execution + QA + validation
</Recommended_Clarity_Pipeline>
