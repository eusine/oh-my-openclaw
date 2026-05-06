---
name: autoresearch-goal
description: "Durable professor-critic research workflow with source-backed OpenClaw artifacts."
argument-hint: "<research mission>"
user-invocable: true
---

# Autoresearch Goal

Use when a research mission should be durable, source-backed, and checked by an explicit rubric/critic loop.

## Boundary

- This is not raw web browsing and not a deprecated `omx autoresearch` launch surface.
- OpenClaw owns durable artifacts under `.oh-my-openclaw/goals/autoresearch/<slug>/`.
- Fresh or mutable claims require live retrieval from primary/reliable sources.
- Completion requires a passing rubric verdict and source-backed synthesis.

## Artifacts

- `mission.json` — topic, scope, questions, freshness requirements, and constraints.
- `rubric.md` — what counts as a complete, reliable answer.
- `sources.jsonl` — source URL/path, retrieval date, credibility note, and claim coverage.
- `ledger.jsonl` — professor/critic verdicts and revisions.
- `report.md` — final synthesis with citations and unresolved uncertainty.

## Flow

1. Create the mission and rubric.
2. Gather sources using the appropriate retrieval lane for the target.
3. Extract claims with dates, source identity, and confidence.
4. Run a critic pass against the rubric:
   - `pass`: all required questions answered with adequate evidence;
   - `fail`: missing source coverage, weak reasoning, or stale facts;
   - `blocked`: access/credential/paywall/tooling limit prevents completion.
5. Revise until the rubric passes or a real blocker is named.
6. Final answer must summarize findings, cite sources/artifacts, and state remaining uncertainty.

## Completion gate

Assistant prose alone is not sufficient. A completed autoresearch goal needs `report.md`, source records, and a passing critic/rubric ledger entry.
