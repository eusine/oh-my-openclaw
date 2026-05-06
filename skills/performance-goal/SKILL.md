---
name: performance-goal
description: "Run an evaluator-gated performance optimization workflow with durable OpenClaw artifacts."
argument-hint: "<objective + evaluator contract>"
user-invocable: true
---

# Performance Goal Workflow

Use when a task is specifically about improving speed, latency, memory, throughput, cost, or another measurable performance target.

## Contract

- State lives under `.oh-my-openclaw/goals/performance/<slug>/`.
- No optimization starts until an evaluator command/check and pass/fail contract exist.
- Completion requires a passing evaluator checkpoint plus regression evidence.
- If the evaluator is flaky or unavailable, record `blocked` instead of claiming success.

## Required artifacts

- `objective.md` — target, constraints, baseline, and non-goals.
- `state.json` — current status, baseline, best result, and last validation.
- `ledger.jsonl` — each attempt, measurement, regression check, and decision.
- `evidence/` — benchmark output, profiler notes, screenshots, or test logs.

## Agent loop

1. Define the objective and evaluator contract.
2. Measure baseline before changing code.
3. Make small reversible changes.
4. Run the evaluator and relevant regression tests.
5. Record each pass/fail/blocker with evidence.
6. Stop when the target is met, the budget is exhausted, or a blocker is real.

## Completion gate

A performance goal is incomplete unless:

- the evaluator contract has a passing checkpoint;
- regression tests/checks relevant to the touched surface pass;
- the before/after evidence is recorded under the workflow directory;
- the final answer names the measured improvement and any tradeoffs.
