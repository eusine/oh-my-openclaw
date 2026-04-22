# Evolver safe mode

Run Evolver inside this OpenClaw workspace with outbound network denied and network-sensitive features disabled.

## Command

```bash
scripts/evolver-safe.sh
scripts/evolver-safe.sh --review
scripts/evolver-safe.sh --loop
EVOLVE_BRIDGE=true scripts/evolver-safe.sh
EVOLVE_STRATEGY=innovate scripts/evolver-safe.sh --loop
```

## What this wrapper does

- denies all network access with `sandbox-exec`
- clears ambient auth tokens from the process env
- disables Hub, worker, validator, auto issue reporting, and self PR paths
- uses this workspace's `memory/` as input
- writes Evolver state under `memory/evolution/evolver-safe/`
- writes logs under `logs/evolver/`

## Notes

- This is local-only mode.
- OpenClaw can still interpret `sessions_spawn(...)` text printed by Evolver when you opt in with `EVOLVE_BRIDGE=true`.
- If Evolver upstream changes its outbound behavior, the sandbox should still block actual network egress.
