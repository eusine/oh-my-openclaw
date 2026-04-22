#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
WORKSPACE_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
EVOLVER_DIR="$WORKSPACE_DIR/external/evolver"
SAFE_HOME="$WORKSPACE_DIR/.cache/evolver-safe-home"
EVOLUTION_DIR="$WORKSPACE_DIR/memory/evolution/evolver-safe"
EVOLVER_LOGS_DIR="$WORKSPACE_DIR/logs/evolver"
SANDBOX_PROFILE="$WORKSPACE_DIR/.tmp/evolver-network-deny.sb"
PATH_BASE="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
SAFE_EVOLVE_BRIDGE="${EVOLVE_BRIDGE:-false}"
SAFE_EVOLVE_STRATEGY="${EVOLVE_STRATEGY:-}"
SAFE_EVOLVER_SESSION_SCOPE="${EVOLVER_SESSION_SCOPE:-}"
SAFE_AGENT_NAME="${AGENT_NAME:-main}"

if [[ ! -f "$EVOLVER_DIR/index.js" ]]; then
  echo "[evolver-safe] Missing evolver install at $EVOLVER_DIR" >&2
  exit 1
fi

mkdir -p "$SAFE_HOME" "$EVOLUTION_DIR" "$EVOLVER_LOGS_DIR" "$WORKSPACE_DIR/.tmp"

cat > "$SANDBOX_PROFILE" <<'EOF'
(version 1)
(allow default)
(deny network*)
EOF

cd "$WORKSPACE_DIR"

exec /usr/bin/env -i \
  HOME="$SAFE_HOME" \
  PATH="$PATH_BASE" \
  LANG="${LANG:-en_US.UTF-8}" \
  LC_ALL="${LC_ALL:-en_US.UTF-8}" \
  TERM="${TERM:-xterm-256color}" \
  CI="1" \
  NODE_OPTIONS="--require $WORKSPACE_DIR/scripts/evolver-safe-preload.cjs" \
  OPENCLAW_WORKSPACE="$WORKSPACE_DIR" \
  AGENT_NAME="$SAFE_AGENT_NAME" \
  EVOLVER_REPO_ROOT="$EVOLVER_DIR" \
  MEMORY_DIR="$WORKSPACE_DIR/memory" \
  EVOLUTION_DIR="$EVOLUTION_DIR" \
  EVOLVER_LOGS_DIR="$EVOLVER_LOGS_DIR" \
  A2A_HUB_URL="" \
  EVOMAP_HUB_URL="" \
  A2A_NODE_ID="" \
  EVOMAP_NODE_ID="" \
  A2A_NODE_SECRET="" \
  EVOMAP_API_KEY="" \
  GITHUB_TOKEN="" \
  GH_TOKEN="" \
  GITHUB_PAT="" \
  EVOLVER_AUTO_ISSUE="false" \
  EVOLVER_SELF_PR="false" \
  EVOLVER_VALIDATOR_ENABLED="false" \
  EVOLVE_BRIDGE="$SAFE_EVOLVE_BRIDGE" \
  EVOLVE_STRATEGY="$SAFE_EVOLVE_STRATEGY" \
  EVOLVER_SESSION_SCOPE="$SAFE_EVOLVER_SESSION_SCOPE" \
  WORKER_ENABLED="0" \
  EVOMAP_PROXY="0" \
  A2A_TRANSPORT="offline" \
  EVOLVER_LEAK_CHECK="block" \
  NPM_CONFIG_UPDATE_NOTIFIER="false" \
  npm_config_update_notifier="false" \
  NO_UPDATE_NOTIFIER="1" \
  /usr/bin/sandbox-exec -f "$SANDBOX_PROFILE" node "$EVOLVER_DIR/index.js" "$@"
