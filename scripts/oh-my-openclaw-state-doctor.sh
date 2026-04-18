#!/usr/bin/env bash
# oh-my-openclaw-state-doctor.sh
# Inspect and optionally clean up Oh My OpenClaw workflow state files.
# Usage: bash scripts/oh-my-openclaw-state-doctor.sh [--clean-stale] [--clean-completed]

set -euo pipefail

WORKSPACE="${OH_MY_OPENCLAW_WORKSPACE:-$(dirname "$0")/..}"
STATE_DIR="$WORKSPACE/.oh-my-openclaw/state"
STALE_HOURS=48

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

CLEAN_STALE=false
CLEAN_COMPLETED=false

for arg in "$@"; do
  case "$arg" in
    --clean-stale)     CLEAN_STALE=true ;;
    --clean-completed) CLEAN_COMPLETED=true ;;
    --help|-h)
      echo "Usage: oh-my-openclaw-state-doctor.sh [--clean-stale] [--clean-completed]"
      echo ""
      echo "  --clean-stale      Remove state files that are active but >48h old (or missing updated_at)"
      echo "  --clean-completed  Remove state files with active: false"
      exit 0
      ;;
  esac
done

if [[ ! -d "$STATE_DIR" ]]; then
  echo "No .oh-my-openclaw/state/ directory found at: $STATE_DIR"
  echo "No Oh My OpenClaw state to inspect."
  exit 0
fi

ACTIVE_COUNT=0
STALE_COUNT=0
COMPLETED_COUNT=0
CORRUPT_COUNT=0

echo ""
echo -e "${BOLD}Oh My OpenClaw State Doctor${RESET}"
echo -e "State dir: ${CYAN}$STATE_DIR${RESET}"
echo -e "Stale threshold: ${CYAN}${STALE_HOURS}h${RESET}"
echo ""

PARSE_PY=$(cat <<'PYEOF'
import json, sys, os
from datetime import datetime, timezone

stale_hours = float(sys.argv[1])
state_file = sys.argv[2]

try:
    with open(state_file) as f:
        d = json.load(f)
except Exception:
    print("CORRUPT")
    sys.exit(0)

active = d.get('active', False)
mode = d.get('mode') or os.path.basename(state_file).replace('-state.json', '')
phase = d.get('current_phase', 'unknown')
iteration = d.get('iteration', '')
task = (d.get('task_description') or '').replace('\n', ' ')

raw_ts = d.get('updated_at') or d.get('started_at') or ''
has_updated_at = bool(d.get('updated_at'))

age_str = 'unknown'
is_stale = False

if raw_ts:
    try:
        ts = datetime.fromisoformat(raw_ts.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        age_s = (now - ts).total_seconds()
        age_h = int(age_s // 3600)
        age_m = int((age_s % 3600) // 60)
        if age_h >= 24:
            age_d = age_h // 24
            age_str = f"{age_d}d {age_h % 24}h ago"
        else:
            age_str = f"{age_h}h {age_m}m ago"
        is_stale = age_s > stale_hours * 3600
    except Exception:
        age_str = f"unparseable ({raw_ts[:20]})"

no_updated_at_warn = "yes" if (active and not has_updated_at) else "no"
print(f"{'True' if active else 'False'}|{mode}|{phase}|{iteration}|{age_str}|{task}|{'True' if is_stale else 'False'}|{no_updated_at_warn}")
PYEOF
)

for state_file in "$STATE_DIR"/*-state.json; do
  [[ -f "$state_file" ]] || continue
  filename="$(basename "$state_file")"
  [[ "$filename" == _* ]] && continue

  result=$(python3 -c "$PARSE_PY" "$STALE_HOURS" "$state_file" 2>/dev/null || echo "CORRUPT")

  if [[ "$result" == "CORRUPT" ]]; then
    echo -e "  ${RED}[CORRUPTED]${RESET} $filename, could not parse JSON"
    (( CORRUPT_COUNT++ )) || true
    continue
  fi

  IFS='|' read -r is_active mode phase iteration age_str task is_stale no_updated_at <<< "$result"
  iter_str=""
  [[ -n "$iteration" ]] && iter_str=" iter=$iteration"

  if [[ "$is_active" == "True" ]]; then
    if [[ "$is_stale" == "True" ]]; then
      echo -e "  ${YELLOW}[STALE]   ${RESET} ${BOLD}$mode${RESET} | phase: $phase$iter_str | last: $age_str"
      [[ -n "$task" ]] && echo -e "            task: $task"
      (( STALE_COUNT++ )) || true
      if $CLEAN_STALE; then
        rm "$state_file"
        echo -e "            ${RED}-> removed${RESET}"
      fi
    else
      echo -e "  ${GREEN}[ACTIVE]  ${RESET} ${BOLD}$mode${RESET} | phase: $phase$iter_str | last: $age_str"
      [[ -n "$task" ]] && echo -e "            task: $task"
      if [[ "$no_updated_at" == "yes" ]]; then
        echo -e "            ${YELLOW}! no updated_at, staleness tracking degraded${RESET}"
      fi
      (( ACTIVE_COUNT++ )) || true
    fi
  else
    echo -e "  ${CYAN}[DONE]    ${RESET} $mode | phase: $phase | last: $age_str"
    (( COMPLETED_COUNT++ )) || true
    if $CLEAN_COMPLETED; then
      rm "$state_file"
      echo -e "            ${CYAN}-> removed${RESET}"
    fi
  fi
done

for summary in "$STATE_DIR"/_*.md "$STATE_DIR"/_*.json; do
  [[ -f "$summary" ]] && echo -e "  ${CYAN}[SUMMARY] ${RESET} $(basename "$summary")"
done

echo ""
echo -e "${BOLD}Summary:${RESET} ${GREEN}${ACTIVE_COUNT} active${RESET} | ${YELLOW}${STALE_COUNT} stale${RESET} | ${CYAN}${COMPLETED_COUNT} completed${RESET} | ${RED}${CORRUPT_COUNT} corrupted${RESET}"

if (( STALE_COUNT > 0 )) && ! $CLEAN_STALE; then
  echo ""
  echo -e "  To remove stale states: ${CYAN}bash scripts/oh-my-openclaw-state-doctor.sh --clean-stale${RESET}"
fi
if (( COMPLETED_COUNT > 0 )) && ! $CLEAN_COMPLETED; then
  echo -e "  To remove completed states: ${CYAN}bash scripts/oh-my-openclaw-state-doctor.sh --clean-completed${RESET}"
fi
echo ""
