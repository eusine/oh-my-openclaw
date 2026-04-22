# Default Markdown Files Guide

This guide explains the core markdown files many OpenClaw workspaces use as their human-facing operating layer.

The point is simple:
- keep the repo public
- keep your actual life private
- make customization explicit instead of smuggling personal context into examples

## Recommended files

### `AGENTS.md`
Use this as the workspace operating manual.

Put here:
- startup rules
- workflow routing rules
- delegation policy
- repo-wide guardrails
- what should stay private
- agentic behavior rules like minimum authority, reversibility, and when to pause for confirmation
- intent-interpretation rules so the assistant avoids both dumbly literal and overreaching behavior

Do not put here:
- personal diary material
- API keys
- exact home paths unless truly required

### `SOUL.md`
Use this for persona, tone, and conversational style.

Put here:
- voice
- rhythm
- attitude
- what kind of assistant you want to be
- explicit anti-pattern bans for tone and phrasing
- what helpfulness means in practice
- honesty norms like calibrated confidence and no deceptive framing
- the core character traits that should stay stable across contexts

Good examples of bans:
- no exaggeration
- no flattery
- no unnecessary verbosity
- no vague answers
- no weak endings like "if you want" or "I can help with that"
- no hedge-everything safety theater when a clear, honest answer is appropriate

If your runtime also has a separate personality layer, disable it when you want `SOUL.md` to remain the primary voice.

Do not put here:
- private relationship history
- anything you would not want copied into another workspace by accident

### `USER.md`
Use this for safe, practical user preferences.

Put here:
- preferred name
- timezone
- broad collaboration preferences
- stable habits that make the assistant better

Do not put here:
- sensitive personal data
- passwords
- financial or medical secrets
- details that should not ship in a public repo

### `MEMORY.md`
Use this for curated long-term memory.

Put here:
- stable facts worth remembering
- durable decisions
- standing preferences
- boundaries

Do not put here:
- raw logs
- secrets unless you intentionally accept that risk
- noisy short-term notes better kept in daily files

### `TOOLS.md`
Use this for machine or environment notes.

Put here:
- local aliases
- hostnames you are comfortable storing locally
- preferred devices or voices
- setup-specific tips

Do not publish this file unchanged if it contains your real infrastructure.

### `HEARTBEAT.md`
Use this for proactive caretaker behavior.

Put here:
- what should be checked silently
- when to interrupt the user
- what “all good” means
- recurring maintenance responsibilities

### `IDENTITY.md` (optional)
Use this when you want a short identity card separate from `SOUL.md`.

## How the core files differ

- `SOUL.md` defines character, tone, honesty, and the style of helpfulness
- `AGENTS.md` defines operating rules, permissions, workflow behavior, and guardrails
- `USER.md` defines safe practical preferences about the human being helped
- `MEMORY.md` stores curated durable facts, not raw chatter

A good split keeps the assistant from sounding one way while behaving another.

## Safe public workflow

1. keep real files in your private workspace
2. publish only templates and guides
3. avoid committing filled-in personal versions
4. run a privacy scan before pushing

## Included templates

See `templates/default-md/` for sanitized starter files.
