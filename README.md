# Oh My OpenClaw

A lightweight workflow harness for OpenClaw.

Oh My OpenClaw packages a durable orchestration layer around common agent workflows like deep requirements interviews, consensus planning, persistent execution, parallel work, QA cycling, and multi-worker teams.

## Lineage

This project is not pretending to have appeared out of thin air.

Oh My OpenClaw is an OpenClaw-native migration and cleanup of the earlier **OMX** workflow layer. The goal here is to preserve the useful workflow ideas, repackage them for OpenClaw, and make the public repo cleaner than the original private workspace it came from.

If you share, fork, or announce this project, credit the original OMX author as part of that lineage.

## What this repo is

- a public, cleaned-up extraction of the workflow layer
- a migration of OMX workflow ideas into an OpenClaw-shaped public package
- skill-first orchestration patterns for OpenClaw
- minimal helper scripts for runtime state hygiene and local dispatch

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

## Runtime layout

```
.oh-my-openclaw/
  state/
  context/
  plans/
  logs/
```

## Migration notes in one paragraph

The public product name is **Oh My OpenClaw**, but the historical lineage still matters. Some older notes, discussions, and operating habits may still refer to **OMX**, `.omx/`, or **madmax** mode. In this repo, those older terms are documented rather than hidden.

## Docs included

- `docs/overview.md`
- `docs/workflows.md`
- `docs/terminology.md`
- `docs/state-model.md`
- `docs/compatibility.md`
- `docs/legacy-migration.md`
- `docs/default-markdown-files.md`
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

Run `scripts/privacy-scan.sh`, smoke-test the copied skills in a clean workspace, then replace `LICENSE` with the license you actually want to ship.
