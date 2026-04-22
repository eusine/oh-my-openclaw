#!/usr/bin/env python3
"""Shared run-outcome contract for Oh My OpenClaw workflow state.

This keeps stop/continue semantics consistent across helper scripts, workflow
state writers, and future detached/background runners.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


TERMINAL_RUN_OUTCOMES = ('finish', 'blocked_on_user', 'failed', 'cancelled')
NON_TERMINAL_RUN_OUTCOMES = ('progress', 'continue')
RUN_OUTCOMES = NON_TERMINAL_RUN_OUTCOMES + TERMINAL_RUN_OUTCOMES

RUN_OUTCOME_ALIASES = {
    'finish': 'finish',
    'finished': 'finish',
    'complete': 'finish',
    'completed': 'finish',
    'done': 'finish',
    'blocked': 'blocked_on_user',
    'blocked-on-user': 'blocked_on_user',
    'blocked_on_user': 'blocked_on_user',
    'needs-input': 'blocked_on_user',
    'needs_input': 'blocked_on_user',
    'needs input': 'blocked_on_user',
    'waiting_on_user': 'blocked_on_user',
    'failed': 'failed',
    'fail': 'failed',
    'error': 'failed',
    'cancelled': 'cancelled',
    'canceled': 'cancelled',
    'cancel': 'cancelled',
    'aborted': 'cancelled',
    'abort': 'cancelled',
    'progress': 'progress',
    'continue': 'continue',
    'continued': 'continue',
    'resumable': 'continue',
    'resume': 'continue',
}

TERMINAL_PHASE_TO_RUN_OUTCOME = {
    'complete': 'finish',
    'completed': 'finish',
    'done': 'finish',
    'blocked': 'blocked_on_user',
    'blocked_on_user': 'blocked_on_user',
    'blocked-on-user': 'blocked_on_user',
    'needs_input': 'blocked_on_user',
    'needs-input': 'blocked_on_user',
    'failed': 'failed',
    'cancelled': 'cancelled',
    'canceled': 'cancelled',
    'cancel': 'cancelled',
}


@dataclass
class OutcomeResult:
    ok: bool
    state: dict[str, Any] | None = None
    outcome: str | None = None
    warning: str | None = None
    error: str | None = None


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def normalize_value(value: Any) -> str:
    return value.strip().lower() if isinstance(value, str) else ''


def normalize_run_outcome(value: Any) -> OutcomeResult:
    normalized = normalize_value(value)
    if not normalized:
        return OutcomeResult(ok=True)
    if normalized in RUN_OUTCOMES:
        return OutcomeResult(ok=True, outcome=normalized)
    alias = RUN_OUTCOME_ALIASES.get(normalized)
    if alias:
        warning = None
        if alias != normalized:
            warning = f'normalized legacy run outcome "{value}" -> "{alias}"'
        return OutcomeResult(ok=True, outcome=alias, warning=warning)
    return OutcomeResult(ok=False, error=f'run_outcome must be one of: {", ".join(RUN_OUTCOMES)}')


def infer_run_outcome(candidate: dict[str, Any]) -> str:
    explicit = normalize_run_outcome(candidate.get('run_outcome'))
    if explicit.outcome:
        return explicit.outcome

    phase = normalize_value(candidate.get('current_phase'))
    if phase and phase in TERMINAL_PHASE_TO_RUN_OUTCOME:
        return TERMINAL_PHASE_TO_RUN_OUTCOME[phase]

    if candidate.get('active') is True:
        return 'continue'
    if isinstance(candidate.get('completed_at'), str) and candidate.get('completed_at').strip():
        return 'finish'
    if candidate.get('active') is False:
        return 'finish'
    return 'continue'


def is_terminal_run_outcome(value: Any) -> bool:
    normalized = normalize_run_outcome(value)
    return normalized.outcome in TERMINAL_RUN_OUTCOMES


def apply_run_outcome_contract(candidate: dict[str, Any], *, now_value: str | None = None) -> OutcomeResult:
    next_state = dict(candidate)
    normalized = normalize_run_outcome(next_state.get('run_outcome'))
    if not normalized.ok:
        return normalized

    outcome = normalized.outcome or infer_run_outcome(next_state)
    next_state['run_outcome'] = outcome
    effective_now = now_value or now_iso()

    if outcome in TERMINAL_RUN_OUTCOMES:
        if next_state.get('active') is True:
            return OutcomeResult(ok=False, error=f'terminal run outcome "{outcome}" requires active=false')
        next_state['active'] = False
        if not (isinstance(next_state.get('completed_at'), str) and next_state['completed_at'].strip()):
            next_state['completed_at'] = effective_now
    else:
        if next_state.get('active') is False:
            return OutcomeResult(ok=False, error=f'non-terminal run outcome "{outcome}" requires active=true')
        next_state['active'] = True
        if isinstance(next_state.get('completed_at'), str) and next_state['completed_at'].strip():
            del next_state['completed_at']

    return OutcomeResult(ok=True, state=next_state, outcome=outcome, warning=normalized.warning)


def should_continue_run(candidate: dict[str, Any]) -> bool:
    return not is_terminal_run_outcome(infer_run_outcome(candidate))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Normalize and validate Oh My OpenClaw run outcomes.')
    sub = parser.add_subparsers(dest='command', required=True)

    normalize = sub.add_parser('normalize', help='Normalize a run-outcome value')
    normalize.add_argument('value')

    infer = sub.add_parser('infer', help='Infer run_outcome from a state JSON file or stdin')
    infer.add_argument('source', nargs='?')

    apply = sub.add_parser('apply', help='Apply the run-outcome contract to a state JSON file or stdin')
    apply.add_argument('source', nargs='?')
    apply.add_argument('--now-iso')

    should_continue = sub.add_parser('should-continue', help='Return whether a run should continue')
    should_continue.add_argument('source', nargs='?')

    return parser.parse_args()


def load_state(source: str | None) -> dict[str, Any]:
    if source and source != '-':
        raw = Path(source).read_text()
    else:
        raw = sys.stdin.read()
    raw = raw.strip()
    if not raw:
        raise SystemExit('state JSON is required via stdin or file path')
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise SystemExit('state JSON must be an object')
    return data


def print_json(data: object) -> None:
    json.dump(data, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write('\n')


def main() -> int:
    args = parse_args()
    if args.command == 'normalize':
        result = normalize_run_outcome(args.value)
        payload = {'ok': result.ok, 'outcome': result.outcome, 'warning': result.warning, 'error': result.error}
        print_json(payload)
        return 0 if result.ok else 1

    if args.command == 'infer':
        state = load_state(args.source)
        print_json({'outcome': infer_run_outcome(state)})
        return 0

    if args.command == 'apply':
        state = load_state(args.source)
        result = apply_run_outcome_contract(state, now_value=args.now_iso)
        payload = {'ok': result.ok, 'state': result.state, 'outcome': result.outcome, 'warning': result.warning, 'error': result.error}
        print_json(payload)
        return 0 if result.ok else 1

    if args.command == 'should-continue':
        state = load_state(args.source)
        outcome = infer_run_outcome(state)
        print_json({'should_continue': should_continue_run(state), 'run_outcome': outcome})
        return 0

    raise SystemExit(f'unknown command: {args.command}')


if __name__ == '__main__':
    raise SystemExit(main())
