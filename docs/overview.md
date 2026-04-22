# Overview

Oh My OpenClaw is a workflow layer for OpenClaw.

It is also a migration story. The repo takes ideas that previously lived under the OMX workflow layer and ports them into a cleaner OpenClaw-native public package.

It packages reusable skill instructions and a small amount of helper tooling around a simple idea: some requests need more than a one-shot answer. They need an explicit workflow with state, checkpoints, and resumability.

This repo focuses on that layer only.

It does not try to publish a whole personal workspace, private memory system, or session runtime.

## Good entrypoints

- `README.md` for the quick picture and install shape
- `docs/quickstart.md` for Telegram-first setup
- `docs/workflows.md` for workflow selection
- `docs/state-model.md` for runtime state and blocking-question contracts
- `docs/routing-rules.md` and `docs/prompt-sections.md` for the newer routing and prompt-surface pieces
- `docs/self-improvement.md` and `docs/openclaw-skill-self-evolution-mvp.md` for the self-improvement direction
