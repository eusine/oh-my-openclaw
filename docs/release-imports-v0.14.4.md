# OMX release import pass, based on oh-my-codex v0.14.1-v0.14.4

Reviewed on 2026-04-24 against upstream releases:
- v0.14.1, published 2026-04-21: https://github.com/Yeachan-Heo/oh-my-codex/releases/tag/v0.14.1
- v0.14.2, published 2026-04-21: https://github.com/Yeachan-Heo/oh-my-codex/releases/tag/v0.14.2
- v0.14.3, published 2026-04-22: https://github.com/Yeachan-Heo/oh-my-codex/releases/tag/v0.14.3
- v0.14.4, published 2026-04-24: https://github.com/Yeachan-Heo/oh-my-codex/releases/tag/v0.14.4

## Upstream themes

### v0.14.1 — interactive reliability hardening
- Deep-interview Stop gating stays blocked while required question obligations remain pending.
- Question UI/session reliability was hardened around reused sessions and failed detached launches.
- Lifecycle normalization moved toward one shared run-outcome contract.
- Setup/update refresh became safer around managed `AGENTS.md`.

### v0.14.2 — fast-follow operator reliability
- Korean 2-set drift for `ulw` was normalized upstream as an ultrawork shorthand concern.
- Deep-interview guidance now waits for background question terminals before continuing.
- Failed question launches clear stale enforcement markers.
- Session-scoped clear/tombstone behavior prevents legacy root fallback state from leaking.

### v0.14.3 — latest interactive execution hardening
- Deep-interview gained prompt-safe summary gates for oversized context and answered-round reconciliation to avoid re-prompt loops.
- Ultrawork protocol was refreshed around context grounding, pass/fail acceptance criteria, direct-tool vs delegated lanes, and lightweight evidence.
- Canonical supervisor runtime event contracts were added upstream.
- Native Stop/autopilot stale-state loops and visible question rendering were hardened.

### v0.14.4 — default frontier lane update
- Default frontier model moved to `gpt-5.5`.
- Mini/spark seams intentionally stayed exact upstream.
- Setup/config/docs were aligned around `gpt-5.5` defaults and `250000 / 200000` context guidance.

## What landed in Oh My OpenClaw

### 1. Deep-interview oversized-context summary gate
OpenClaw-native deep-interview guidance now requires preflight context intake before the first interview question and blocks ambiguity scoring/handoff until oversized initial context has a prompt-safe summary.

Updated:
- `skills/deep-interview/SKILL.md`
- `public/oh-my-openclaw/skills/deep-interview/SKILL.md`

### 2. Answered-question reconciliation before re-prompting
Added `answered-pending` to the structured question helper. This lists answered required questions whose obligations are still pending, so deep-interview can consume the answer and satisfy the obligation instead of asking the same round again after resume/Stop/retry paths.

Updated:
- `scripts/oh-my-openclaw-question.py`
- `public/oh-my-openclaw/scripts/oh-my-openclaw-question.py`
- `scripts/test_oh_my_openclaw_question.py`
- `public/oh-my-openclaw/scripts/test_oh_my_openclaw_question.py`

### 3. Ultrawork protocol refresh
Reworked ultrawork around the upstream v0.14.3 protocol shape while translating OMX-specific mechanics to OpenClaw:
- context + certainty check before editing
- explicit pass/fail acceptance criteria before execution
- deliberate self-vs-delegate choice
- direct-tool lane plus background evidence lanes
- lightweight evidence boundary so direct ultrawork does not overclaim Ralph-level persistence/verification

Updated:
- `skills/ultrawork/SKILL.md`
- `public/oh-my-openclaw/skills/ultrawork/SKILL.md`

### 4. Frontier model alignment
The live OpenClaw config already defaults `main` to `openai-codex/gpt-5.5`. This pass aligns the dedicated `codex-local` lane and local notes with upstream v0.14.4's frontier default while preserving mini/spark guidance as separate lanes.

Updated:
- `~/.openclaw/openclaw.json`
- `TOOLS.md`

## Deliberately not importing as-is

- Native OMX tmux renderer internals: OpenClaw uses Telegram/session tools and should keep structured question state portable.
- OMX MCP state tools: Oh My OpenClaw persists under `.oh-my-openclaw/state/` and uses small helper scripts instead.
- Project-local `CODEX_HOME` machinery: useful upstream, but this workspace's Codex/OpenClaw harnessing is configured through OpenClaw agents and runtime config.
- Windows psmux / BusyBox cleanup details: not relevant to this macOS OpenClaw lane today.

## Migration rule from this pass

Import upstream lifecycle behavior, not upstream runtime assumptions. Keep the OpenClaw surface native: structured state files, OpenClaw sessions/subagents, explicit verification, and no hidden return to top-level `.omx` runtime paths.

## 2차 audit matrix

| Upstream change | Oh My OpenClaw decision | Status | Notes |
|---|---|---:|---|
| Required-question Stop gating remains blocked while obligations are pending | Keep structured obligation ledger and `obligation-blockers` checks | DONE | Landed in v0.14.0 pass; revalidated in this pass |
| Answered deep-interview rounds should not re-prompt after resume/Stop/retry | Add `answered-pending` and require consuming answered records before asking again | DONE | Covered by helper tests |
| Oversized deep-interview context needs prompt-safe summary before scoring/handoff | Add summary gate to deep-interview state and execution policy | DONE | Skill-level contract; no runtime hook needed yet |
| Background question terminals must be awaited before continuing | Translate to OpenClaw guidance: wait for background session/tool result before scoring or handoff | DONE | Native tmux renderer not imported |
| Korean 2-set `ulw` drift (`ㅕㅣㅈ`) | Treat as ultrawork alias in advisory triage and docs | DONE | Covered by triage test |
| Ultrawork protocol refresh | Replace old “fire tasks” guidance with context/acceptance/self-vs-delegate/evidence-lane protocol | DONE | OpenClaw-native sessions/subagents, no OMX state MCP |
| Default frontier model `gpt-5.5` | Align live `codex-local` and docs while preserving mini/spark lanes | DONE | Config backup recorded in workspace memory |
| Canonical supervisor runtime event contracts | Track as design reference, not import as runtime code yet | BACKLOG | Needs OpenClaw-native event mapping before code |
| Session-scoped clear/tombstone precedence | Track as future state-doctor hardening | BACKLOG | Current state helpers are file-based and simpler |
| Setup/update managed `AGENTS.md` repair | Skip for now | SKIPPED | OpenClaw owns bootstrap/config refresh differently |
| OMX tmux renderer, HUD, psmux, BusyBox cleanup | Do not import | SKIPPED | Runtime-specific to upstream OMX |
| Project-local `CODEX_HOME` | Do not import directly | SKIPPED | OpenClaw agents/runtime config own this lane |

## Remaining backlog after 2차

1. Define an OpenClaw-native supervisor event schema only if workflow state needs external observers beyond helper scripts.
2. Extend `oh-my-openclaw-state-doctor.sh` with session-scoped tombstone/clear precedence if stale root state recurs.
3. Add an integration smoke that simulates a deep-interview answer being recorded, consumed, and handed off to `ralplan` without re-prompting.
4. Periodically re-run this release-import audit when upstream OMX cuts a new minor release.
