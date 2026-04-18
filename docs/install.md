# Install Notes

## Goal

Use this repo as a clean workflow layer on top of an existing OpenClaw workspace.

## Suggested placement

- copy `skills/*` into your workspace skill directory
- copy `scripts/*` into your workspace helper scripts directory
- keep runtime artifacts under `.oh-my-openclaw/`

## Expected runtime directories

```bash
mkdir -p .oh-my-openclaw/state
mkdir -p .oh-my-openclaw/context
mkdir -p .oh-my-openclaw/plans
mkdir -p .oh-my-openclaw/logs
```

## Optional profile convention

If you want a named maximum-autonomy lane, use an `autonomy` profile in your own OpenClaw setup.

## Integration idea

Add a short snippet to your workspace instructions so the assistant knows:

- the available workflows
- where runtime state lives
- when to resume an active workflow instead of restarting it

See `examples/AGENTS-snippet.md`.
