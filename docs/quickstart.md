# Quickstart

## Telegram-first quickstart

1. install or copy the Oh My OpenClaw skills and scripts into your OpenClaw workspace
2. create the `.oh-my-openclaw/` runtime directories
3. add the workflow snippet to your workspace instructions
4. open your usual chat surface, for many users this will be Telegram
5. start with a natural request such as:
   - "먼저 물어보고 시작해"
   - "계획 먼저"
   - "이거 끝까지 해봐"
   - "병렬로 나눠서 처리해"

## Minimal setup shell

```bash
mkdir -p .oh-my-openclaw/state
mkdir -p .oh-my-openclaw/context
mkdir -p .oh-my-openclaw/plans
mkdir -p .oh-my-openclaw/logs
```

## Sanity checks

- the skills exist in your workspace
- the runtime directories exist
- your private markdown files are not being published accidentally
- the assistant knows where workflow state should live

## Next reads

- `docs/openclaw-integration.md`
- `docs/openclaw-official-alignment.md`
- `docs/team-operating-model.md`
- `docs/telegram-workflows.md`
- `examples/telegram-prompts.md`
