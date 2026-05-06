# OMX release import pass, based on oh-my-codex v0.15.1 through v0.16.0

Reviewed on 2026-05-06 against upstream releases:

- v0.15.1, published 2026-04-29: https://github.com/Yeachan-Heo/oh-my-codex/releases/tag/v0.15.1
- v0.15.2, published 2026-04-30: https://github.com/Yeachan-Heo/oh-my-codex/releases/tag/v0.15.2
- v0.15.3, published 2026-05-02: https://github.com/Yeachan-Heo/oh-my-codex/releases/tag/v0.15.3
- v0.16.0, published 2026-05-06: https://github.com/Yeachan-Heo/oh-my-codex/releases/tag/v0.16.0

Latest upstream checked: `Yeachan-Heo/oh-my-codex` tag `v0.16.0`.

## Upstream themes

### v0.15.1

- Operator-controlled direct vs tmux launch policy.
- Passive read-only state operations.
- Team DAG dependency remapping.
- Plugin/setup recovery and stale surface cleanup.
- Stop lifecycle and hook/runtime reliability fixes.

### v0.15.2

- GPT-5.5 prompt-surface alignment.
- Code-reviewer root-cause discipline: reject masking workaround fixes.
- Autopilot three-phase review-gated loop: `ralplan -> ralph -> code-review`.
- Guided question UX and response-contract preservation.
- Pipeline and MCP/plugin runtime hardening.

### v0.15.3

- Team/Ralph startup, shutdown, and same-cwd session isolation reliability.
- Approved handoff validation and narrowly retained execution context.
- Planning/Ralph lifecycle hardening and stale Stop-block cleanup.
- Setup/plugin/config guardrails.
- Oversized GPT-5.5 context warnings and ai-slop-cleaner fallback guidance.

### v0.16.0

- Native Codex goal-mode workflows: `ultragoal`, `performance-goal`, and `autoresearch-goal`.
- Snapshot-reconciled completion to prevent shell-only false completion.
- Deprecated skill delivery cleanup.
- Runtime reliability around Team/Ralph handoffs, question batch handshakes, Stop hooks, boxed state routing, Discord/proxy docs, and package pipeline templates.

## What landed in Oh My OpenClaw

### 1. Autopilot strict loop alignment

Public `autopilot` was updated from the older broad five-phase lifecycle to the upstream 0.15.2+ strict loop contract:

```text
ralplan -> ralph -> code-review
```

OpenClaw translation choices:

- State path is `.oh-my-openclaw/state/autopilot-state.json`, not `.omx/state`.
- OpenClaw tools/subagents own execution; Codex/tmux hook assumptions were not copied.
- Non-clean review always returns to `ralplan`; ad hoc patching outside the loop is explicitly disallowed.
- Resume behavior is phase-aware and preserves handoff artifacts.

Updated:

- `skills/autopilot/SKILL.md`
- `public/oh-my-openclaw/skills/autopilot/SKILL.md`
- `public/oh-my-openclaw/docs/workflows.md`

### 2. Goal workflow family, OpenClaw-native translation

Added OpenClaw-native versions of the v0.16.0 goal workflow family:

- `ultragoal` — durable multi-goal planning and sequential execution.
- `performance-goal` — evaluator-gated performance optimization.
- `autoresearch-goal` — professor/critic source-backed research.

Translation choices:

- Durable state lives under `.oh-my-openclaw/goals/`.
- No hidden Codex goal state is assumed.
- Completion requires fresh artifact reads and validation evidence.
- `autoresearch-goal` keeps live retrieval/source-citation discipline instead of reviving deprecated direct `omx autoresearch` behavior.

Added:

- `skills/ultragoal/SKILL.md`
- `skills/performance-goal/SKILL.md`
- `skills/autoresearch-goal/SKILL.md`
- `public/oh-my-openclaw/skills/ultragoal/SKILL.md`
- `public/oh-my-openclaw/skills/performance-goal/SKILL.md`
- `public/oh-my-openclaw/skills/autoresearch-goal/SKILL.md`
- `public/oh-my-openclaw/docs/goal-workflows.md`

### 3. Workflow catalog/docs refresh

Updated public workflow lists and AGENTS snippet so goal workflows are visible and Autopilot is described as the strict review-gated loop rather than an unconstrained lifecycle.

Updated:

- `public/oh-my-openclaw/README.md`
- `public/oh-my-openclaw/docs/workflows.md`
- `public/oh-my-openclaw/examples/AGENTS-snippet.md`

## Deliberately not importing as-is

- Codex hidden `/goal` tool calls (`get_goal`, `create_goal`, `update_goal`) because OpenClaw does not expose the same first-class goal API in this workspace.
- Direct `omx` CLI launch-policy changes, tmux launch controls, and Codex hook internals.
- Plugin marketplace/setup internals that are Codex-specific.
- GitHub package pipeline templates as executable automation; those require a separate public-write/PR authority design.
- Discord webhook/bot setup docs beyond noting the upstream change, because OpenClaw already has channel-specific Discord docs and token handling.

## Audit matrix

| Upstream change | Oh My OpenClaw decision | Status | Notes |
|---|---|---:|---|
| Autopilot review-gated loop | Import and translate | DONE | `ralplan -> ralph -> code-review` |
| Goal workflows | Import concept, translate state/evidence model | DONE | No hidden Codex goal state |
| Snapshot completion reconciliation | Import as artifact/evidence completion rule | DONE | Fresh artifact/test evidence required |
| Team/Ralph runtime reliability | Keep as skill guidance and OpenClaw subagent discipline | PARTIAL | Runtime hook internals skipped |
| Guided question UX | Already covered by existing question helper flow | TRACKED | No new script needed this pass |
| Setup/plugin/tmux internals | Skip | SKIPPED | Runtime-specific upstream assumptions |
| GitHub package pipeline templates | Track design reference | BACKLOG | Requires public write policy |
| Discord/proxy docs | Track only | BACKLOG | OpenClaw docs own channel config |

## Remaining backlog after this pass

1. Add script-level helpers for `.oh-my-openclaw/goals/*` if the artifact workflow becomes common enough to justify automation.
2. Add a clean OpenClaw package-pipeline design before importing upstream GitHub issue/PR automation.
3. Revisit Team/Ralph runtime hardening only where OpenClaw session/subagent state exposes a matching seam.
