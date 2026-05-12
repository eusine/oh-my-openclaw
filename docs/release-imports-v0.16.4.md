# Release Import Notes: OMX v0.16.1-v0.16.4

Checked upstream `Yeachan-Heo/oh-my-codex` through tag `v0.16.4` on 2026-05-12.

## Imported

- Ultragoal aggregate-mode guidance: one whole-run objective with per-story durable OpenClaw checkpoints.
- Final completion hardening: cleanup/deslop evidence, post-cleanup verification, and clean review before whole-run completion.
- Session authority guidance: session-scoped workflow state wins over stale root/global markers.
- Approved handoff guidance: planning/team/Ralph handoffs should preserve approved context references, launch hints, and verification expectations.
- Deep-interview fact routing guidance: discoverable facts should be gathered from code/research before asking the user for judgment.

## Deliberately Not Imported

- Raw Codex goal-tool mutation behavior.
- Tmux runtime and pane/HUD implementation details.
- Codex native hook setup, feature-flag migration, and MCP registry defaults.
- Raw `.omx/wiki/` storage. OpenClaw durable project knowledge should use repo-visible docs or `oh-my-openclaw-wiki/` when a project wiki is desired.

## Local Translation

The portable behavior is expressed as OpenClaw skill/document contracts under `.oh-my-openclaw/`:

- `.oh-my-openclaw/goals/` for durable goal artifacts.
- `.oh-my-openclaw/state/` for resumable workflow state.
- OpenClaw-native subagents and session tasks instead of tmux workers.
- Review and validation evidence before final completion claims.
