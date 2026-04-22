# State Model

Runtime state lives under `.oh-my-openclaw/`.

```text
.oh-my-openclaw/
  state/
    questions/
    question-obligations/
    prompt-routing-state.json
    sessions/
      <session-id>/
        prompt-routing-state.json
  context/
  plans/
  logs/
```

## Principles

- state files should include `updated_at`
- active workflows should be resumable
- blocking user questions should have owned records under `.oh-my-openclaw/state/questions/`
- required-question consumption should have a fail-closed ledger under `.oh-my-openclaw/state/question-obligations/`
- advisory triage should stay advisory, and only remember the latest non-PASS route
- runtime outputs should stay out of version control
- examples in `examples/state/` are schemas, not live data

## Important caveat

This repo documents the workflow state model, but the surrounding hook or keyword-detector implementation may live outside this repo in your own OpenClaw setup.

## Question records

Use `scripts/oh-my-openclaw-question.py` when a workflow must block on a user answer.
The question record belongs to the workflow layer, not to a transient chat bubble.
That lets resume, Stop gating, and follow-up state survive chat interruptions.

Recommended question lifecycle:
- `ask` when the blocking question is created
- `answer` when the user replies and the workflow captures the raw answer
- `satisfy-obligation` after the workflow actually consumes the answer into durable workflow state
- `clear` or `clear-obligation` when the question is being resolved by handoff, cancellation, or abandonment
- `blockers` for unanswered required questions
- `obligation-blockers` before stopping or handing off, so answered-but-unconsumed required questions still block correctly

## Question obligations

Required questions now have a second layer beyond the question record itself.
A question can be `answered` while its obligation is still `pending`.
That is deliberate. It prevents a required user answer from being dropped during resume or handoff before the workflow has actually consumed it.

Recommended deep-interview fields:
- `pending_question_id`
- `pending_question_obligation_id`
- `question_state_root`
- `question_obligation_root`

## Run-outcome contract

Use `scripts/oh-my-openclaw-run-outcome.py` to normalize workflow terminal vs resumable state.

Canonical outcomes:
- non-terminal: `progress`, `continue`
- terminal: `finish`, `blocked_on_user`, `failed`, `cancelled`

Legacy aliases such as `completed`, `blocked`, `needs_input`, `canceled`, and `resumable` are normalized onto that smaller contract.
This keeps resume checks and stop behavior consistent even when helper scripts or older state writers use slightly different wording.

## Advisory prompt triage state

Use `scripts/oh-my-openclaw-triage.py` for PASS/LIGHT/HEAVY routing hints.

Rules:
- triage is advisory only
- PASS decisions do not write state
- LIGHT and HEAVY decisions may persist the latest route under `prompt-routing-state.json`
- short clarifying follow-ups can suppress repeated route nudges
- keyword routing should bypass suppression when a direct workflow trigger is already obvious

## Migration caveat

If you are cutting over from an older OMX-named workspace, treat top-level `.omx/state/*` files as legacy residue unless you have deliberately chosen to keep a bridge. Do not leave stale OMX markers in place and then wonder why resume logic feels haunted.
