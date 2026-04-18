# Oh My OpenClaw

A lightweight workflow harness for OpenClaw.

Oh My OpenClaw packages a durable orchestration layer around common agent workflows like deep requirements interviews, consensus planning, persistent execution, parallel work, QA cycling, and multi-worker teams.

## What this repo is

- a public, cleaned-up extraction of the workflow layer
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

## Docs included

- `docs/overview.md`
- `docs/workflows.md`
- `docs/terminology.md`
- `docs/state-model.md`
- `docs/compatibility.md`
- `docs/legacy-migration.md`
- `docs/private-vs-public.md`
- `docs/install.md`

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

## Before publishing

Smoke-test the copied skills in a clean workspace, then replace `LICENSE` with the license you actually want to ship.
