# Oh My OpenClaw

A lightweight workflow harness for OpenClaw.

Oh My OpenClaw packages a durable orchestration layer around common agent workflows like deep requirements interviews, consensus planning, persistent execution, parallel work, QA cycling, and multi-worker teams.

## Telegram-first quickstart

For many OpenClaw users, the real working surface is chat, often Telegram, not a local CLI.

1. copy the skills and scripts from this repo into your OpenClaw workspace
2. create the `.oh-my-openclaw/` runtime directories
3. add the workflow snippet from `examples/AGENTS-snippet.md`
4. start from chat with a natural request such as:
   - "먼저 물어보고 시작해"
   - "계획 먼저"
   - "이거 끝까지 해봐"
   - "병렬로 나눠서 처리해"

Minimal shell setup:

```bash
mkdir -p .oh-my-openclaw/state/questions
mkdir -p .oh-my-openclaw/state/question-obligations
mkdir -p .oh-my-openclaw/state/sessions
mkdir -p .oh-my-openclaw/context
mkdir -p .oh-my-openclaw/plans
mkdir -p .oh-my-openclaw/logs
```

## Lineage

This project is not pretending to have appeared out of thin air.

Oh My OpenClaw is an OpenClaw-native migration and cleanup of the earlier **OMX** workflow layer. The goal here is to preserve the useful workflow ideas, repackage them for OpenClaw, and make the public repo cleaner than the original private workspace it came from.

If you share, fork, or announce this project, credit the original OMX author as part of that lineage.

## Credit note

Keep the lineage explicit when you publish or announce the repo.

- Suggested wording: "Oh My OpenClaw is an OpenClaw-native migration of the earlier OMX workflow layer. Credit to the original OMX author for the original lineage."
- If you want a direct tag in README, release notes, or social posts, replace the wording above with the real original-author handle.

## What this repo is

- a public, cleaned-up extraction of the workflow layer
- a migration of OMX workflow ideas into an OpenClaw-shaped public package
- the integration surface for a broader Oh My OpenClaw operating layer, including workflow orchestration and human-gated self-improvement lanes
- skill-first orchestration patterns for OpenClaw
- minimal helper scripts for runtime state hygiene, local dispatch, structured blocking-question records, advisory prompt triage, and normalized run outcomes
- a documented archive-plus-shim cutover path for replacing an older OMX-named live workspace

## What this repo is not

- your whole private workspace
- session logs, memory, or personal runtime state
- a drop-in export of every internal experiment

## Included workflows

- `deep-interview`
- `ralplan`
- `ralph`
- `autopilot`
- `ultrawork`
- `ultraqa`
- `team`

## Self-improvement direction

Oh My OpenClaw is not only a workflow wrapper. The intended direction is to absorb the useful parts of Hermes-style self-evolution and combine them with the already-migrated OMX workflow surface.

That means the long-term target is a human-gated improvement system that can optimize skills, tool descriptions, prompt sections, helper docs, and guarded code lanes using conversation evidence, eval datasets, and review packs rather than vague “agent reflection” alone.

## Included helpers

- `scripts/dispatch-openclaw-turn.sh`
- `scripts/evolver-safe.sh`
- `scripts/oh-my-openclaw-state-doctor.sh`
- `scripts/oh-my-openclaw-question.py`
- `scripts/oh-my-openclaw-run-outcome.py`
- `scripts/oh-my-openclaw-triage.py`

## Runtime layout

```
.oh-my-openclaw/
  state/
    questions/
    question-obligations/
    prompt-routing-state.json
    sessions/
      <session-id>/prompt-routing-state.json
  context/
  plans/
  logs/
```

## Migration notes in one paragraph

The public product name is **Oh My OpenClaw**, but the historical lineage still matters. Some older notes, discussions, and operating habits may still refer to **OMX**, `.omx/`, or **madmax** mode. In this repo, those older terms are documented rather than hidden.

In a real workspace, the clean cutover pattern is not "rename everything and pray". Archive the old OMX surface, install the new workflow names, keep only thin compatibility shims where needed, and move live runtime state to `.oh-my-openclaw/`.

## Docs included

- `docs/artifact-types.md`
- `docs/overview.md`
- `docs/quickstart.md`
- `docs/workflows.md`
- `docs/terminology.md`
- `docs/state-model.md`
- `docs/compatibility.md`
- `docs/evolver-safe.md`
- `docs/legacy-migration.md`
- `docs/default-markdown-files.md`
- `docs/openclaw-official-alignment.md`
- `docs/openclaw-integration.md`
- `docs/openclaw-config.md`
- `docs/openclaw-skill-self-evolution-mvp.md`
- `docs/prompt-sections.md`
- `docs/release-imports-v0.14.0.md`
- `docs/release-imports-v0.14.4.md`
- `docs/routing-rules.md`
- `docs/self-improvement.md`
- `docs/team-operating-model.md`
- `docs/telegram-workflows.md`
- `docs/private-vs-public.md`
- `docs/install.md`

## Included templates

- `templates/default-md/AGENTS.example.md`
- `templates/default-md/SOUL.example.md`
- `templates/default-md/USER.example.md`
- `templates/default-md/MEMORY.example.md`
- `templates/default-md/TOOLS.example.md`
- `templates/default-md/HEARTBEAT.example.md`
- `templates/default-md/IDENTITY.example.md`

## Persona guidance

Do not treat `SOUL.md` as fluff only. A strong `SOUL.md` should include explicit anti-pattern rules, not just vibe words.

Good examples:
- ban exaggeration
- ban flattery
- ban unnecessary verbosity
- ban vague answers
- ban weak endings like "if you want" or "I can help with that"

If your runtime has a separate personality overlay and you want `SOUL.md` to be the primary voice, disable the extra overlay and let the markdown file lead.

## Included examples

- `examples/AGENTS-snippet.md`
- `examples/team-prompts.md`
- `examples/telegram-prompts.md`

## Important caveat

This repo contains the workflow layer, not necessarily every surrounding runtime hook used in a private workspace. If your setup depends on a keyword detector, tmux hook, or other bootstrap glue, document or ship that separately.

## Public repo checklist

- private workspace files stripped
- public namespace fully aligned to `Oh My OpenClaw`
- runtime state standardized under `.oh-my-openclaw/`
- helper scripts renamed for public packaging
- legacy migration notes isolated to one document
- sanitized state examples included
- GitHub smoke check included
- README documents OMX lineage and credit expectations

## Before publishing

Run `scripts/privacy-scan.sh` and smoke-test the copied skills in a clean workspace or isolated profile.

Important: do the smoke test from a real OpenClaw workspace or isolated profile. A random clone directory by itself is not a meaningful install check.
