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

1. extract the public repo first
2. test the new names in a clean sandbox
3. add aliases only where a live workspace still needs them
4. migrate live runtime paths after you have verified resume behavior
