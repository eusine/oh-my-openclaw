# OMX release import pass, based on oh-my-codex v0.14.0

Reviewed on 2026-04-20 against these upstream releases:
- v0.14.0, published 2026-04-19: https://github.com/Yeachan-Heo/oh-my-codex/releases/tag/v0.14.0
- v0.13.2, published 2026-04-18: https://github.com/Yeachan-Heo/oh-my-codex/releases/tag/v0.13.2
- v0.13.0, published 2026-04-16: https://github.com/Yeachan-Heo/oh-my-codex/releases/tag/v0.13.0
- v0.12.6, published 2026-04-13: https://github.com/Yeachan-Heo/oh-my-codex/releases/tag/v0.12.6

## What landed in this pass

### 1. Structured blocking-question ownership
Imported from the `omx question` direction in v0.14.0.

What changed:
- added `scripts/oh-my-openclaw-question.py`
- introduced `.oh-my-openclaw/state/questions/` as a first-class runtime path
- updated `deep-interview` so fallback question turns create owned question records and persist `pending_question_id`

### 2. Deep-interview question obligations
Imported as an OpenClaw-native ledger rather than a byte-for-byte OMX port.

What changed:
- added `.oh-my-openclaw/state/question-obligations/`
- required questions now mint linked obligations automatically from `oh-my-openclaw-question.py ask --required ...`
- added `satisfy-obligation`, `clear-obligation`, `obligations`, and `obligation-blockers` commands
- updated `deep-interview` guidance so answered-but-unconsumed required questions still block stop or handoff

Why it mattered:
- a question can be answered in chat before the workflow has actually consumed that answer
- the obligation layer prevents that answer from being silently lost during resume or handoff

### 3. Shared run-outcome contract
Imported as a small Python helper instead of a full runtime transplant.

What changed:
- added `scripts/oh-my-openclaw-run-outcome.py`
- normalized terminal vs non-terminal workflow states around `progress`, `continue`, `finish`, `blocked_on_user`, `failed`, and `cancelled`
- preserved compatibility aliases such as `completed`, `blocked`, `needs_input`, `canceled`, and `resumable`
- updated deep-interview state guidance and docs to use the normalized contract

Why it mattered:
- stop and resume semantics were starting to drift across helper scripts and workflow docs
- one small contract is cheaper than debugging five slightly different meanings of “done”

### 4. Advisory triage routing
Imported as a lightweight helper, not as magical auto-routing.

What changed:
- added `scripts/oh-my-openclaw-triage.py`
- implemented PASS/LIGHT/HEAVY classification with `explore`, `executor`, `designer`, and `autopilot` destinations
- added optional persisted prompt-routing state and follow-up suppression for short clarifying replies
- documented the state shape under `.oh-my-openclaw/state/prompt-routing-state.json` and session-scoped variants

Why it mattered:
- the workflow layer already had routing rules, but no reusable advisory classifier for natural-language starts
- Telegram-first setups benefit from a hinting layer, but they do not need spooky hidden automation

### 5. Autoresearch hard-deprecation cleanup
Imported as documentation cleanup rather than a new executable surface.

What changed:
- clarified that the public OpenClaw-native path is `deep-interview --autoresearch`, not a revived standalone `omx autoresearch` command story
- kept the public package skill-first and validator-gated

### 6. Action-first / blocked-only asking contract
Imported as prompt-and-skill guidance instead of a native Codex-hook transplant.

What changed:
- strengthened the public `AGENTS.example.md` and `examples/AGENTS-snippet.md` with explicit safe-branch auto-continue guidance
- updated the core execution workflows (`autopilot`, `ralph`, `ultrawork`, `ultraqa`, `team`) so they keep moving on safe reversible branches instead of drifting into permission-handoff phrasing
- documented the public rule in `docs/workflows.md`

Why it mattered:
- the public workflow layer already leaned action-first, but it did not state the blocked-only asking boundary crisply enough
- weak endings like `if you want` make the system feel hesitant even when the next local step is already authorized and obvious

## Deliberately not importing as-is

### `omx adapt`
Useful upstream, but it is a different surface. OpenClaw already has its own runtime, gateway, session, and memory integration shape.

### Explore harness binaries
Those belong to the upstream runtime package, not this lightweight workflow repo.

### OMX-specific HUD or tmux internals
Only import behavior that survives the OpenClaw-native cut. Do not drag private OMX runtime assumptions back into the public package.

## Rule from this pass

Before improving a workflow skill, check whether upstream OMX already solved the surrounding lifecycle problem. If yes, import the lifecycle first, then tune the skill.
