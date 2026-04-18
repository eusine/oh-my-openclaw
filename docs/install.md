# Install Notes

## Goal

Use this repo as a clean workflow layer on top of an existing OpenClaw workspace.

If your main working surface is Telegram, read `docs/quickstart.md` and `docs/telegram-workflows.md` before overthinking CLI setup.

## Suggested placement

- copy `skills/*` into your workspace skill directory
- copy `scripts/*` into your workspace helper scripts directory
- keep runtime artifacts under `.oh-my-openclaw/`

This repo is meant to be copied into a real OpenClaw workspace. A bare git clone in an arbitrary directory is not the same thing as a live workspace install.

## Expected runtime directories

```bash
mkdir -p .oh-my-openclaw/state
mkdir -p .oh-my-openclaw/context
mkdir -p .oh-my-openclaw/plans
mkdir -p .oh-my-openclaw/logs
```

## Optional profile convention

If you want a named maximum-autonomy lane, use an `autonomy` profile in your own OpenClaw setup.

If your existing setup already uses the older `madmax` profile name, that is fine too. The important thing is the behavior, not pretending the old term never existed.

## Integration idea

Add a short snippet to your workspace instructions so the assistant knows:

- the available workflows
- where runtime state lives
- when to resume an active workflow instead of restarting it

See `examples/AGENTS-snippet.md`.

For a more complete OpenClaw placement guide, read `docs/openclaw-integration.md`.

## Smoke-test recommendation

Do the smoke test in a disposable OpenClaw workspace or isolated profile, not just by `cd`-ing into a random clone and running `openclaw` there.

Good smoke test:
- copy the files into a clean workspace
- create `.oh-my-openclaw/state`, `context`, `plans`, and `logs`
- add the AGENTS snippet
- run `scripts/privacy-scan.sh`
- run `bash -n` against the helper scripts
- confirm OpenClaw sees the installed skills from the real workspace

Bad smoke test:
- clone this repo elsewhere
- run `openclaw status` from that directory
- assume that means the repo is correctly installed

## Customizing your default markdown files

Use the sanitized starter files in `templates/default-md/` and adapt them to your own workspace.

Read `docs/default-markdown-files.md` before filling them in, especially if you plan to keep the repo public.
