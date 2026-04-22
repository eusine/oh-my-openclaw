# Oh My OpenClaw Self-Improvement Contract

This is the local operating-layer skeleton, not a magical autopilot fairy tale.

## Goal
Turn friction into evidence, evidence into opportunities, opportunities into reviewable candidates, and candidates into human-gated promotion.

This is not a skill-only loop and not a docs-only loop. It is an operating-layer contract, but every mutation still has to stay narrow and reviewable.

## Layers
1. **Discovery**
   - mine conversations, memory, git churn, run artifacts, and review packs
   - sanitize or redact sensitive material before it becomes a reusable artifact
   - normalize repeated friction into opportunity records

2. **Dataset building**
   - convert opportunities into sample, holdout, and golden cases
   - keep per-target manifests explicit

3. **Mutation**
   - target only registered artifacts
   - keep candidate diffs narrow and readable

4. **Triage**
   - rank open issues first
   - then rank evidence-backed opportunities
   - only then revisit stale stable lanes

5. **Promotion**
   - no auto-merge
   - every promotion leaves lineage and review evidence
   - rollback stays explicit

## Boundaries
- OpenClaw-native paths only.
- No live runtime mutation without a registry entry.
- No promotion of raw conversation, memory, or review-pack material without an explicit sanitize/redact pass.
- No “improve everything” broad rewrite.
- No skill-only framing or docs-only discovery when the real friction points at routing, state, or guarded code.
- If the right fix is a new helper doc or routing rule, make that the target.
- If the right fix is a guarded code target, keep it explicit, bounded, and reviewable.

## Current target families
- skill instructions
- prompt templates
- prompt sections
- helper docs
- routing rules
- state contracts
- guarded code targets

Selection rule: pick the smallest registered artifact that actually closes the friction. Do not pretend a doc tweak is enough when the evidence really points at a guarded code lane.

## Output contract
Every run should leave behind:
- discovery artifacts
- dataset manifests
- candidate diffs
- review packs
- triage queue updates
- lineage or rollback records when promotion happens

Before any of those artifacts become durable inputs for future mutation or public review, run a sanitize/redact pass so they do not carry raw private conversation or memory content forward by accident.
