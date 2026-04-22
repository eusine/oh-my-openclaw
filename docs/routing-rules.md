# Routing Rules

This doc captures the local ranking logic for the broader Oh My OpenClaw skeleton.

## Current priority order
1. open human-actionable issues
2. evidence-backed opportunities
3. stale stable lanes
4. generic cleanup

## Evidence-backed opportunities
Prefer these when the discovery layer has real friction items from:
- conversations
- memory notes
- git churn
- run artifacts
- review packs

When the stable lanes are already green, evidence-backed opportunities beat freshness-only revisits.

## Revisit logic
If nothing is open, prefer the stable lane with the highest revisit value, using:
- validation age
- run age
- promotion scarcity

## Reporting rule
Write next-focus output in plain language.

- say what rose to the top
- say why now
- say what got deprioritized

Do not hide the call behind abstract internal jargon or a generic "all-stable" shrug.

## Hard rule
Never let the queue forget about evidence just because a phase is currently green.
