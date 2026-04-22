# Artifact Types

These are the registered optimization targets for the Oh My OpenClaw self-improvement scaffold.

## Supported types
- `skill_instruction`, skill-level behavior docs like `skills/*/SKILL.md`
- `prompt_template`, reusable prompt or mutation template docs
- `prompt_section`, bounded sections inside a larger prompt doc
- `helper_doc`, operator-facing docs that shape behavior indirectly
- `routing_rule`, docs that control triage and handoff behavior
- `constraint_doc`, gate and policy docs used by review packs
- `state_contract`, JSON or markdown state contract documents
- `code_target`, guarded code-lane target registry entries

## Rules
- Every target must be registered before mutation.
- Candidate diffs must stay inside the registered target.
- Human review is mandatory before promotion.
- If a target can be solved by a smaller doc or routing change, prefer that.

## Registration shape
Each registry entry should name:
- id
- type
- path
- target_label
- description

That is enough for the local scaffold. Fancy metadata can come later.
