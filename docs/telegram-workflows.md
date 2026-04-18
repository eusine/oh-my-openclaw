# Telegram Workflows

Oh My OpenClaw works well when Telegram is the main human-facing surface.

## Why Telegram-first matters

The user is not usually opening a terminal to micromanage workflows.
They are sending short instructions, approvals, corrections, and follow-up nudges in chat.

That means the workflow layer should optimize for:
- short prompts
- resumable context
- low-noise updates
- simple branching choices
- clear completion messages

## Natural-language entrypoints

These are all reasonable Telegram-style ways to start work:

- "이거 끝까지 해봐"
- "먼저 물어보고 시작해"
- "계획 먼저 잡아"
- "테스트 깨진 거 다 정리해"
- "병렬로 나눠서 처리해"

The assistant should map those to the appropriate workflow rather than forcing command-heavy usage.

## Suggested conversation patterns

### Clarify first
- user: "이 기능 좀 제대로 만들어줘"
- assistant uses `deep-interview`

### Plan first
- user: "이건 크니까 계획 먼저"
- assistant uses `ralplan`

### Just execute
- user: "이 계획대로 끝까지 밀어"
- assistant uses `ralph` or `team`

### Full hands-off lane
- user: "처음부터 끝까지 알아서"
- assistant uses `autopilot`

## Good update style

Prefer:
- one short start message
- milestone updates only when something meaningful changes
- one blocker message when input is truly needed
- one completion message with concrete outcomes

Avoid:
- noisy play-by-play narration
- repetitive "still working" messages
- dumping internal state that the user did not ask for

## Suggested choice prompts

When a branching decision matters, use short options like:

- 계속
- 계획 먼저
- 더 물어보기
- 여기서 멈추고 요약
- 직접 입력

## Resume language

A Telegram user should be able to say things like:

- "아까 그거 이어서"
- "지난 계획 기준으로 계속"
- "멈췄던 작업 재개"
- "요약만 줘"

The workflow layer should treat these as first-class resume patterns, not as unusual edge cases.

## Stop and redirect patterns

Useful stop phrases include:

- "그만"
- "취소"
- "여기까지"
- "계획만 남겨"

## Recommendation

If you want Oh My OpenClaw to feel more like OMX in practice, improve the Telegram interaction loop before building fancy status surfaces.
