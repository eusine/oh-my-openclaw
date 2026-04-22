#!/usr/bin/env bash
set -euo pipefail

root_dir="${1:-$(pwd)}"

patterns=(
  '/Users/'
  '/home/'
  '.openclaw/workspace'
  '127.0.0.1'
  'local.invalid'
  'api_key'
  'OPENAI_API_KEY'
  'ANTHROPIC_API_KEY'
)

exclude_globs=(
  '!/.git'
  '!.git'
  '!node_modules'
  '!dist'
  '!scripts/privacy-scan.sh'
  '!.github/workflows/smoke.yml'
)

echo "Privacy scan root: $root_dir"
found=0
for pattern in "${patterns[@]}"; do
  args=()
  for glob in "${exclude_globs[@]}"; do
    args+=(--glob "$glob")
  done
  if rg -n --hidden "${args[@]}" "$pattern" "$root_dir" >/tmp/oh-my-openclaw-privacy-scan.out 2>/dev/null; then
    echo ""
    echo "Pattern hit: $pattern"
    cat /tmp/oh-my-openclaw-privacy-scan.out
    found=1
  fi
done

if [[ "$found" -eq 1 ]]; then
  echo ""
  echo "Privacy scan failed. Review the hits above before publishing."
  exit 1
fi

echo "No denylist hits found."
