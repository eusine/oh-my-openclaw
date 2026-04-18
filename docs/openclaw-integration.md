# OpenClaw Integration

This repo is designed to sit on top of an existing OpenClaw workspace.

## Main idea

Use OpenClaw as the runtime and messaging layer.
Use Oh My OpenClaw as the workflow layer.

For many users, the main working surface will be Telegram or another chat channel, not a local CLI.

## Recommended placement

- copy `skills/*` into your workspace skill directory
- copy `scripts/*` into your workspace helper scripts directory
- keep runtime outputs under `.oh-my-openclaw/`
- keep filled-in personal markdown files private

## Private vs public split

Public repo:
- workflow skills
- helper scripts
- sanitized templates
- setup guides

Private workspace:
- filled-in `SOUL.md`, `USER.md`, `MEMORY.md`, `TOOLS.md`, `HEARTBEAT.md`
- live runtime state
- personal preferences and machine-specific notes

## Telegram-first operating model

A typical flow looks like this:

1. the user sends a natural-language request in Telegram
2. the assistant decides whether the task needs clarification, planning, execution, QA, or team coordination
3. the workflow state is persisted under `.oh-my-openclaw/`
4. the assistant returns progress, blockers, or completion updates back into Telegram

## Recommended workflow mapping

- vague request -> `deep-interview`
- expensive or risky implementation -> `ralplan`
- clear bounded task -> `ralph`
- many independent tasks -> `ultrawork`
- failing implementation or validation cycle -> `ultraqa`
- decomposable multi-worker task -> `team`
- full end-to-end hands-off build -> `autopilot`

## Runtime directories

```bash
mkdir -p .oh-my-openclaw/state
mkdir -p .oh-my-openclaw/context
mkdir -p .oh-my-openclaw/plans
mkdir -p .oh-my-openclaw/logs
```

## Good integration habits

- keep public templates sanitized
- document old OMX terms instead of pretending they never existed
- prefer concise chat updates over noisy status spam
- design workflows for interruption and resume
- treat Telegram as the main control surface when that matches real usage
- keep `SOUL.md` concrete, with explicit anti-pattern bans, instead of using only mood words
- if your runtime adds a separate personality overlay, disable it when you want `SOUL.md` to remain the primary style layer

## Team execution alignment

If you want the migration to feel real, align team execution with OpenClaw's official runtime model.

- main session = orchestrator
- subagents = workers
- task records = ledger
- hooks = auxiliary glue

See `docs/openclaw-official-alignment.md` and `docs/team-operating-model.md`.
