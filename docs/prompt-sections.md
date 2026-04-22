# Prompt Sections

These are the bounded prompt regions the optimizer can touch without rewriting the whole persona blob.

## What belongs here
- directive task-answering rules
- clarification discipline
- tool-selection guidance
- style guardrails
- progress-reporting rules
- section-by-section changes with a clear rollback boundary
- drift checks that keep section edits from spilling into other layers

## What does not belong here
- whole-persona rewrites
- runtime policy blobs
- broad behavior changes with no review boundary
- raw memory mutation
- section edits that quietly rewrite unrelated prompt regions

## Working rule
Keep each section small enough that a human can understand what changed in one glance.

## Drift checks
Before promoting a prompt-section change, check these explicitly.

- it still reads like a bounded section edit, not a whole-prompt rewrite
- it does not mutate memory or runtime policy by stealth
- the reason for the section change is named in plain language
- a reviewer can point at the exact section that changed without diff-hunting the whole persona blob
