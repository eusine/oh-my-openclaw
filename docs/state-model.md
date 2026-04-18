# State Model

Runtime state lives under `.oh-my-openclaw/`.

```text
.oh-my-openclaw/
  state/
  context/
  plans/
  logs/
```

## Principles

- state files should include `updated_at`
- active workflows should be resumable
- runtime outputs should stay out of version control
- examples in `examples/state/` are schemas, not live data

## Important caveat

This repo documents the workflow state model, but the surrounding hook or keyword-detector implementation may live outside this repo in your own OpenClaw setup.
