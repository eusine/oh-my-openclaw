#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
state_file="$root_dir/.oh-my-openclaw/state/autonomy-toggle.json"

usage() {
  cat >&2 <<'EOF'
Usage: dispatch-openclaw-turn.sh [--force-autonomy] [--print-command] [--session-id ID] <message...>

Dispatches a local OpenClaw turn. When the autonomy toggle is on, the command
automatically runs through `--profile autonomy`.
EOF
  exit 64
}

autonomy_enabled() {
  python3 - "$state_file" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
if not path.exists():
    raise SystemExit(1)

data = json.loads(path.read_text())
raise SystemExit(0 if data.get("enabled") else 1)
PY
}

force_autonomy=0
print_command=0
session_id=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force-autonomy)
      force_autonomy=1
      shift
      ;;
    --print-command)
      print_command=1
      shift
      ;;
    --session-id)
      [[ $# -ge 2 ]] || usage
      session_id="$2"
      shift 2
      ;;
    --)
      shift
      break
      ;;
    -*)
      usage
      ;;
    *)
      break
      ;;
  esac
done

[[ $# -ge 1 ]] || usage
message="$*"

cmd=(openclaw)
if [[ "$force_autonomy" -eq 1 ]] || autonomy_enabled; then
  cmd+=(--profile autonomy)
fi

cmd+=(agent --local --agent main)
if [[ -n "$session_id" ]]; then
  cmd+=(--session-id "$session_id")
fi
cmd+=(--message "$message" --json)

if [[ "$print_command" -eq 1 ]]; then
  printf '%q ' "${cmd[@]}"
  printf '\n'
  exit 0
fi

exec "${cmd[@]}"
