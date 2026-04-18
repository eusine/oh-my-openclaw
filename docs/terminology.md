# Terminology

## Product name

- **Oh My OpenClaw**: the public workflow layer packaged in this repo
- **OMX**: the earlier workflow layer this repo migrates from

## Runtime directory

- **`.oh-my-openclaw/`**: runtime state, plans, context snapshots, and logs
- **`.omx/`**: the older runtime path you may still see in historical notes or private workspaces

## Workflows

- `deep-interview`: clarify ambiguous work before building
- `ralplan`: produce a reviewed implementation plan
- `ralph`: keep executing until the task is actually done
- `autopilot`: run the full workflow pipeline
- `ultrawork`: execute independent tasks in parallel
- `ultraqa`: run QA loops until the result is clean
- `team`: coordinate multiple workers on one larger task

## Execution profile term

- **autonomy mode**: a high-autonomy local execution profile name for setups that want an explicit maximum-autonomy lane
- **madmax**: the older blunt-name term for a maximum-autonomy execution profile. This repo does not hide the term, but treats it as lineage or compatibility vocabulary rather than the primary product name.
