# Legacy Migration

This document exists only for people migrating from the older OMX naming.

## Naming map

- `OMX` -> `Oh My OpenClaw`
- `.omx/` -> `.oh-my-openclaw/`
- `omx-autopilot` -> `autopilot`
- `omx-ralplan` -> `ralplan`
- `omx-ralph` -> `ralph`
- `omx-ultrawork` -> `ultrawork`
- `omx-ultraqa` -> `ultraqa`
- `omx-team` -> `team`
- `omx-deep-interview` -> `deep-interview`
- `madmax` -> `autonomy`

## Recommended cutover

1. archive the old workflow surface first, do not hard-delete it
2. install the new names in a clean sandbox or disposable workspace
3. replace live skill directories with the new ones
4. replace helper scripts with the new names
5. leave aliases only where a live workspace still needs them
6. migrate runtime paths after you have verified resume behavior

## Practical live-workspace recipe

- archive `skills/omx-*`
- archive any legacy helper scripts such as `scripts/openclaw-agent.sh` and `scripts/omx-state-doctor.sh`
- copy in:
  - `skills/autopilot`
  - `skills/deep-interview`
  - `skills/ralph`
  - `skills/ralplan`
  - `skills/team`
  - `skills/ultraqa`
  - `skills/ultrawork`
  - `scripts/dispatch-openclaw-turn.sh`
  - `scripts/oh-my-openclaw-state-doctor.sh`
- recreate old entrypoints only as thin forwarding shims if needed
- create `.oh-my-openclaw/state`, `context`, `plans`, and `logs`
- inspect `.omx/state/` and archive stale or completed residue so it does not masquerade as active live state later

## What to keep, what to kill

Keep:
- lineage notes about OMX
- a compatibility shim when some other local tool still calls the old path
- archived legacy state for rollback or forensics

Kill:
- live writes continuing into `.omx/`
- old skills remaining on the active skill path beside the new ones
- stale state that makes resume detection lie to you
