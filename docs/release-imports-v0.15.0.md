# OMX release import pass, based on oh-my-codex v0.15.0

Reviewed on 2026-04-26 against upstream release:
- v0.15.0, published 2026-04-26: https://github.com/Yeachan-Heo/oh-my-codex/releases/tag/v0.15.0

Upstream note: v0.15.0 reports that v0.14.4 is not an ancestor of the current dev release candidate, so its verified reachable base is v0.14.3 while v0.14.4 remains historical release context. Oh My OpenClaw had already imported the v0.14.4-facing model/default and workflow notes, so this pass focused on the new OpenClaw-relevant v0.15.0 surface.

## Upstream themes

- First-party Codex plugin packaging and marketplace metadata.
- Codex App compatibility paths that avoid tmux-only runtime assumptions.
- Visual Ralph as a first-class UI implementation workflow.
- Setup install-mode selection and plugin-vs-legacy cleanup.
- Native agent/model routing contracts around `gpt-5.5`, `gpt-5.4-mini`, and `gpt-5.3-codex-spark`.
- Hook/runtime reliability: Stop hook parseability, notification fallback watchers, derived watchers, stale tmux sockets, team identity, and CI silence protection.
- Windows/tmux question rendering and Rust explore-harness compatibility.

## What landed in Oh My OpenClaw

### 1. Visual Ralph workflow

Added an OpenClaw-native Visual Ralph orchestration skill for frontend/UI implementation from generated references, static references, or live URL baselines.

Translation choices:
- `web-clone` is treated as a legacy use case inside Visual Ralph rather than a separate OpenClaw workflow.
- `$ralph`, `$visual-verdict`, and `$imagegen` references were translated to OpenClaw skill/tool language.
- Runtime paths moved from `.omx/...` to `.oh-my-openclaw/...`.
- The approval boundary is explicit: generate or capture the reference first, then stop for user approval before implementation.

Added:
- `skills/visual-ralph/SKILL.md`
- `public/oh-my-openclaw/skills/visual-ralph/SKILL.md`
- `public/oh-my-openclaw/docs/visual-ralph.md`

### 2. Visual Verdict skill

Added a strict JSON visual QA skill for screenshot/reference comparison. It standardizes `score`, `verdict`, `category_match`, `differences`, `suggestions`, and `reasoning`, with a default pass threshold of 90+.

Added:
- `skills/visual-verdict/SKILL.md`
- `public/oh-my-openclaw/skills/visual-verdict/SKILL.md`

### 3. Public workflow docs updated

Updated README, workflow docs, and AGENTS snippet so Visual Ralph and Visual Verdict are visible in the public package surface.

Updated:
- `public/oh-my-openclaw/README.md`
- `public/oh-my-openclaw/docs/workflows.md`
- `public/oh-my-openclaw/examples/AGENTS-snippet.md`

## Deliberately not importing as-is

- Codex plugin packaging and marketplace descriptors: OpenClaw's plugin/skill delivery surface is different and should not copy Codex App packaging blindly.
- Native Codex hook/runtime assets: OpenClaw has first-class tools, sessions, cron, and channel delivery; tmux/Codex hook assumptions should stay upstream-specific until mapped deliberately.
- Setup install-mode migration: useful conceptually, but Oh My OpenClaw currently ships as a skill/helper package rather than an `omx setup` CLI.
- Windows/tmux renderer details: not relevant to the current OpenClaw-native public package.
- Rust explore harness binaries: no OpenClaw-native consumer in this repo yet.

## Audit matrix

| Upstream change | Oh My OpenClaw decision | Status | Notes |
|---|---|---:|---|
| Visual Ralph workflow | Import and translate to OpenClaw-native paths/tools | DONE | New `visual-ralph` skill plus docs |
| Visual Verdict | Import as structured JSON visual QA skill | DONE | New `visual-verdict` skill |
| Live URL clone routing | Fold into Visual Ralph | DONE | Avoids reviving standalone web-clone assumptions |
| First-party Codex plugin bundle | Do not import directly | SKIPPED | Needs OpenClaw packaging design first |
| Setup plugin-vs-legacy mode | Track as design reference | BACKLOG | Could become an OpenClaw installer doc later |
| Native agent/model routing defaults | Already aligned from v0.14.4 pass | DONE | Keep `gpt-5.5` frontier guidance |
| Hook/runtime hardening | Track selectively | BACKLOG | Only import after OpenClaw-native event mapping |
| Windows/tmux/Rust harness details | Do not import | SKIPPED | Upstream runtime-specific |

## Remaining backlog after this pass

1. Add an OpenClaw-native visual smoke fixture once a small frontend sample app exists in the public repo.
2. Decide whether Oh My OpenClaw should grow a real installer/setup command or stay docs-plus-skills for now.
3. Revisit upstream hook/runtime hardening only when there is a concrete OpenClaw state/event seam to map onto.
