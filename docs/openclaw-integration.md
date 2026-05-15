# OpenClaw Integration

This repo is designed to sit on top of an existing OpenClaw workspace.

For the concrete `openclaw.json` keys that make this integration real, read `docs/openclaw-config.md` too.

## Main idea

Use OpenClaw as the runtime and messaging layer.
Use Oh My OpenClaw as the workflow layer.

For many users, the main working surface will be Telegram or another chat channel, not a local CLI.

## Recommended placement

- copy `skills/*` into your workspace skill directory
- copy `scripts/*` into your workspace helper scripts directory
- keep runtime outputs under `.oh-my-openclaw/`, including owned question records under `.oh-my-openclaw/state/questions/`
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
3. the workflow state is persisted under `.oh-my-openclaw/`, and any blocking user question is persisted under `.oh-my-openclaw/state/questions/`
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
mkdir -p .oh-my-openclaw/state/questions
mkdir -p .oh-my-openclaw/state/question-obligations
mkdir -p .oh-my-openclaw/state/sessions
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
- if your `AGENTS.md` uses sectioned behavior bans, make compaction re-inject them too, not just startup/safety boilerplate

## Compaction guardrails

If you rely on `AGENTS.md` sections like `No "If You Want"` or `Adjacent Anti-Patterns`, make sure post-compaction reinjection includes them.

A practical OpenClaw config pattern is:

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

Otherwise the assistant can recover the session with startup/safety context while losing the sharper anti-pattern bans that actually shape the tone.

## Team execution alignment

If you want the migration to feel real, align team execution with OpenClaw's official runtime model.

- main session = orchestrator
- subagents = workers
- task records = ledger
- hooks = auxiliary glue

See `docs/openclaw-official-alignment.md` and `docs/team-operating-model.md`.

## Raw OMX Notification Bridge

Upstream OMX also documents an OpenClaw / generic notification gateway path for raw `omx` CLI sessions. Treat that as a legacy/raw OMX bridge, not as the primary Oh My OpenClaw runtime.

Use it only when a real upstream OMX session should emit hook events into an OpenClaw or Clawdbot surface.

Activation gates:

- `HOOKS_TOKEN`: bearer token for OpenClaw hook endpoints; keep it in env, not hardcoded JSON
- `OMX_OPENCLAW=1`: required for OpenClaw-backed OMX dispatch
- `OMX_OPENCLAW_COMMAND=1`: required in addition for command gateways
- `OMX_OPENCLAW_COMMAND_TIMEOUT_MS=120000`: optional global command timeout; gateway timeout wins over env, env wins over the 5000ms default

Config precedence:

1. `notifications.openclaw` wins
2. `custom_webhook_command` / `custom_cli_command` are ignored
3. raw OMX should warn so behavior stays deterministic

For hook-driven agent turns, keep instructions structured and parseable:

    [session-end|exec]
    project={{projectName}} session={{sessionId}} tmux={{tmuxSession}} reason={{reason}}
    성과: 완료 결과 1~2문장
    검증: 확인/테스트 결과
    다음: 후속 액션 1~2개

Useful tokens:

- `{{sessionId}}` for cross-log traceability
- `{{tmuxSession}}` when the event came from an OMX tmux session
- `{{projectName}}`
- `{{question}}` for `ask-user-question`
- `{{reason}}` for `session-end`

OpenClaw HTTP gateway shape:

    {
      "notifications": {
        "enabled": true,
        "openclaw": {
          "enabled": true,
          "gateways": {
            "local": {
              "type": "http",
              "url": "https://OPENCLAW_GATEWAY_HOST/hooks/agent",
              "headers": {
                "Authorization": "Bearer ${HOOKS_TOKEN}"
              }
            }
          },
          "hooks": {
            "session-end": {
              "enabled": true,
              "gateway": "local",
              "instruction": "[session-end|exec]\nproject={{projectName}} session={{sessionId}} tmux={{tmuxSession}} reason={{reason}}\n성과: 완료 결과\n검증: 확인 결과\n다음: 후속 액션"
            },
            "ask-user-question": {
              "enabled": true,
              "gateway": "local",
              "instruction": "[ask-user-question|exec]\nsession={{sessionId}} tmux={{tmuxSession}} question={{question}}\n핵심질문: 필요한 답변\n영향: 미응답 시 영향\n권장응답: 가장 빠른 답변 형태"
            }
          }
        }
      }
    }

Command gateways are useful when the hook should trigger an agent turn rather than a plain webhook post.

Operational rules:

- keep templates simple; command templates interpolate `{{instruction}}`
- set gateway timeout to `120000` for agent-turn delivery
- append `|| true` so hook delivery failure does not block the raw OMX session
- append to `.jsonl` logs for auditability
- use concrete channel ids or platform-native stable targets instead of fragile aliases

Wake smoke:

    curl -sS -X POST https://OPENCLAW_GATEWAY_HOST/hooks/wake \
      -H "Authorization: Bearer ${HOOKS_TOKEN}" \
      -H "Content-Type: application/json" \
      -d '{"text":"OMX wake smoke test","mode":"now"}'

Delivery smoke:

    curl -sS -o /tmp/omx-openclaw-agent-check.json -w "HTTP %{http_code}\n" \
      -X POST https://OPENCLAW_GATEWAY_HOST/hooks/agent \
      -H "Authorization: Bearer ${HOOKS_TOKEN}" \
      -H "Content-Type: application/json" \
      -d '{"message":"OMX delivery verification","instruction":"OMX delivery verification","event":"session-end","sessionId":"manual-check"}'

Pass signals:

- `/hooks/wake` returns JSON with `ok: true`
- `/hooks/agent` returns HTTP 2xx with an accepted response body

Failure hints:

- `401/403`: missing or invalid bearer token
- `404`: wrong hook path
- `5xx`: gateway/runtime issue
- timeout or connection refused: gateway, host, port, or firewall issue
- command gateway disabled: check `OMX_OPENCLAW=1` and `OMX_OPENCLAW_COMMAND=1`
- command killed by `SIGTERM`: raise the gateway timeout

This bridge does not replace the OpenClaw Codex harness. It is for upstream OMX hook events. The normal Oh My OpenClaw workflow remains channel message -> OpenClaw -> Codex harness turn -> `.oh-my-openclaw/` workflow state -> OpenClaw subagents/sessions/tasks.
