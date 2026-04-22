# OpenClaw config guide

This repo is the workflow layer. `openclaw.json` is the runtime config that makes the workflow behave the way the docs claim.

Use this doc when you want the Oh My OpenClaw install to be real, not just cosmetically copied.

## Where `openclaw.json` lives

Typical local path:

```bash
~/.openclaw/openclaw.json
```

Use your own machine-local path. Do not paste a real personal home directory or secrets into public docs.

Treat this file as machine-local runtime config. Do not blindly publish secrets from it.

## What this workflow layer expects

At minimum, the runtime should preserve four things:

1. internal bootstrap hooks are enabled
2. compaction re-injects the behavior bans, not just startup boilerplate
3. the local dispatch path can assume the autonomy baseline when that is your chosen posture
4. codex app-server safety posture matches the intended local execution baseline

## Minimal hook block

This turns on the internal hooks this workflow layer expects to exist.

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "boot-md": { "enabled": true },
        "bootstrap-extra-files": { "enabled": true },
        "session-memory": { "enabled": true },
        "omx-harness": { "enabled": true }
      }
    }
  }
}
```

## Compaction guardrails

This is the part that prevents tone/style rules from disappearing after compaction.

Without this, the assistant can recover with `Session Startup` and `Red Lines` while losing sharper bans like `No "If You Want"`.

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "mode": "safeguard",
        "postCompactionSections": [
          "Session Startup",
          "No \"If You Want\"",
          "Adjacent Anti-Patterns",
          "Red Lines"
        ]
      }
    }
  }
}
```

## Execution posture block

If your workspace intentionally uses the old OMX-style maximum-autonomy baseline, make the runtime say so plainly.

```json
{
  "agents": {
    "defaults": {
      "thinkingDefault": "high",
      "embeddedHarness": {
        "runtime": "auto",
        "fallback": "pi"
      }
    }
  },
  "plugins": {
    "entries": {
      "codex": {
        "enabled": true,
        "config": {
          "appServer": {
            "approvalPolicy": "never",
            "sandbox": "danger-full-access"
          }
        }
      }
    }
  }
}
```

That does not magically create a profile named `autonomy`, but it does preserve the actual runtime behavior the workflow assumes.

## Memory search and embedding lane example

If your recall stack depends on a local embedding server, keep that explicit too.

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "provider": "openai",
        "remote": {
          "baseUrl": "http://localhost:8100/v1",
          "apiKey": "llamacpp-local"
        }
      }
    }
  }
}
```

Keep the endpoint and model naming aligned with your actual local embedding lane, and avoid carrying stale assumptions from an older setup.

## Practical merge pattern

Do not rewrite the whole file unless you have to.

Good pattern:
- back up `openclaw.json`
- patch only the keys you mean to change
- restart or reload the relevant OpenClaw process if your setup requires it
- verify with real reads such as `openclaw config get ...`

## Verification commands

After editing, verify the live runtime instead of trusting your memory.

```bash
openclaw config get hooks.internal.entries
openclaw config get agents.defaults.compaction.postCompactionSections
openclaw config get agents.defaults.embeddedHarness.fallback
openclaw config get plugins.entries.codex.config.appServer.approvalPolicy
openclaw config get plugins.entries.codex.config.appServer.sandbox
```

## Advisory routing and question state

The new `oh-my-openclaw` helper scripts do not require a special OpenClaw config key, but your runtime wiring should leave room for them:

- allow `.oh-my-openclaw/state/` to persist across resumes
- keep question and obligation files under that runtime root instead of hiding them in ephemeral chat state
- if you add a first-turn wrapper or hook for prompt routing, keep `scripts/oh-my-openclaw-triage.py` advisory only
- if you write workflow state from hooks or detached jobs, normalize terminal vs resumable outcomes with `scripts/oh-my-openclaw-run-outcome.py apply` instead of hand-rolling stop semantics


Expected shape for the posture discussed in this repo:

- `postCompactionSections` includes `No "If You Want"` and `Adjacent Anti-Patterns`
- `embeddedHarness.fallback` is whatever your install intends, but check the real value
- `approvalPolicy` is `never`
- `sandbox` is `danger-full-access`

## What belongs in docs vs live config

Public docs should describe:
- the keys that matter
- why they matter
- copyable config snippets

Your private live config may still contain:
- tokens
- personal channels
- local paths
- model endpoints
- machine-specific notes

Keep those separate. The whole point is to make the important runtime shape reproducible without leaking your private file.
