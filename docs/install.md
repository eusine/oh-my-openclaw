# Install Notes

## Goal

Use this repo as a clean workflow layer on top of an existing OpenClaw workspace.

If your main working surface is Telegram, read `docs/quickstart.md` and `docs/telegram-workflows.md` before overthinking CLI setup.

## Suggested placement

- copy `skills/*` into your workspace skill directory
- copy `scripts/*` into your workspace helper scripts directory
- keep runtime artifacts under `.oh-my-openclaw/`

If you are replacing an existing OMX-named live setup, do not hard-delete first. Archive the old surface, install the new one, then leave only the minimum compatibility shims you still need.

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

If you are migrating an OMX-descended setup where `madmax/full` was the normal baseline, keep that behavior as the default and treat `autonomy` as the live label for the same posture, not as a rare break-glass mode.

## Integration idea

Add a short snippet to your workspace instructions so the assistant knows:

- the available workflows
- where runtime state lives
- when to resume an active workflow instead of restarting it

See `examples/AGENTS-snippet.md`.

For a more complete OpenClaw placement guide, read `docs/openclaw-integration.md`.
For the runtime config keys that make the install actually behave that way, read `docs/openclaw-config.md`.

## Live cutover pattern

The least-annoying migration pattern in a real workspace is:

1. archive legacy `skills/omx-*`
2. copy in the new workflow skills (`autopilot`, `deep-interview`, `ralph`, `ralplan`, `team`, `ultraqa`, `ultrawork`)
3. install `scripts/dispatch-openclaw-turn.sh` and `scripts/oh-my-openclaw-state-doctor.sh`
4. keep old entrypoints only as thin shims if your workspace still calls them
5. create `.oh-my-openclaw/{state,context,plans,logs}`
6. inspect old `.omx/state/` residue so stale markers do not confuse later resume logic

This is the difference between a rename and an actual cutover.

## Smoke-test recommendation

Do the smoke test in a disposable OpenClaw workspace or isolated profile, not just by `cd`-ing into a random clone and running `openclaw` there.

Good smoke test:
- copy the files into a clean workspace
- create `.oh-my-openclaw/state`, `context`, `plans`, and `logs`
- add the AGENTS snippet
- run `scripts/privacy-scan.sh`
- run `bash -n` against the helper scripts
- confirm OpenClaw sees the installed skills from the real workspace
- if migrating a live OMX workspace, verify any old shim path forwards into the new scripts and does not still write fresh state under `.omx/`

Bad smoke test:
- clone this repo elsewhere
- run `openclaw status` from that directory
- assume that means the repo is correctly installed

## Customizing your default markdown files

Use the sanitized starter files in `templates/default-md/` and adapt them to your own workspace.

Read `docs/default-markdown-files.md` before filling them in, especially if you plan to keep the repo public.
