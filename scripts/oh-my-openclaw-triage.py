#!/usr/bin/env python3
"""Advisory PASS/LIGHT/HEAVY prompt triage for Oh My OpenClaw.

This stays advisory. It classifies natural-language prompts, persists only the
last non-PASS decision, and helps suppress repetitive follow-up nudges once a
route is already obvious.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


TRIVIAL_PATTERNS = [
    re.compile(r'^(?:hi+|hey|hello|thanks?|thank\s+you|yes|no|ok(?:ay)?|sure|great|good|got\s+it|sounds?\s+good|yep|yup|nope|cool|awesome|perfect)\.?$'),
]

OPT_OUT_PHRASES = (
    'just chat',
    'plain answer',
    'no workflow',
    "don't route",
    'do not route',
    "don't use a skill",
    'do not use a skill',
    'talk through',
    'explain only',
)

EXPLORE_STARTERS = (
    'explain ',
    'what ',
    'where ',
    'why ',
    'how does ',
    'how do ',
    'how is ',
    'tell me about ',
    'describe ',
    'show me how ',
    'can you explain ',
    'could you explain ',
)

DESIGNER_STARTERS = (
    'make the button',
    'style ',
    'color ',
    'adjust spacing',
    'ui ',
    'change the color',
    'change the font',
    'change the style',
    'update the style',
    'update the design',
    'change the design',
    'change the layout',
    'update the layout',
)

VISUAL_DESIGN_TERMS = (
    re.compile(r'\b(?:ui|ux|visual|style|styling|css|layout|spacing|color|font|typography)\b'),
    re.compile(r'\b(?:button|page|screen|panel|modal|form|navbar|sidebar|header|footer|card|component)\b'),
)

BROAD_DESIGN_STARTERS = ('redesign ',)
STRUCTURAL_REDESIGN_TERMS = (
    re.compile(r'\b(?:auth|authentication|authorization|flow|pipeline|deployment|deploy|architecture|system|api|backend|database|data|schema|orm|infra|infrastructure)\b'),
)

EXECUTOR_ANCHOR_PATTERNS = (
    re.compile(r'\bsrc\/[\w./\-]+\.\w+\b'),
    re.compile(r'\blib\/[\w./\-]+\.\w+\b'),
    re.compile(r'\btest\/[\w./\-]+\.\w+\b'),
    re.compile(r'\bspec\/[\w./\-]+\.\w+\b'),
    re.compile(r'\bline\s+\d+\b'),
    re.compile(r'\brename\b.+\bin\b'),
    re.compile(r'\bfix\s+typo\s+in\b'),
    re.compile(r'\badd\b.+\bto\s+line\s+\d+\b'),
)

HEAVY_IMPERATIVE_VERBS = (
    'add ',
    'implement ',
    'refactor ',
    'build ',
    'create ',
    'migrate ',
    'rewrite ',
    'redesign ',
    'integrate ',
    'set up ',
    'configure ',
    'extract ',
    'split ',
    'merge ',
    'update ',
    'remove ',
    'delete ',
    'replace ',
    'convert ',
    'generate ',
    'scaffold ',
    'deploy ',
    'automate ',
)

HEAVY_WORD_THRESHOLD = 5
SHORT_QUESTION_WORD_LIMIT = 10
ANCHORED_EDIT_WORD_LIMIT = 15
CLARIFYING_STARTERS = ('yes', 'no', 'yeah', 'nope', 'ok', 'okay', 'the ', 'that', 'those', 'it')
DEFAULT_STATE_ROOT = Path('.oh-my-openclaw/state')
STATE_FILENAME = 'prompt-routing-state.json'


@dataclass
class TriageDecision:
    lane: str
    reason: str
    destination: str | None = None


@dataclass
class TriageState:
    version: int
    last_triage: dict | None
    suppress_followup: bool

    def as_dict(self) -> dict:
        return {
            'version': self.version,
            'last_triage': self.last_triage,
            'suppress_followup': self.suppress_followup,
        }


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def normalize_prompt(prompt: str) -> str:
    return prompt.strip().lower()


def word_count(prompt: str) -> int:
    return len(prompt.split()) if prompt else 0


def prompt_signature(prompt: str) -> str:
    return 'sha256:' + hashlib.sha256(prompt.encode('utf-8')).hexdigest()


def triage_prompt(prompt: str) -> TriageDecision:
    normalized = normalize_prompt(prompt)
    count = word_count(normalized)

    if not normalized:
        return TriageDecision(lane='PASS', reason='empty_input')

    if any(pattern.match(normalized) for pattern in TRIVIAL_PATTERNS):
        return TriageDecision(lane='PASS', reason='trivial_acknowledgement')

    if any(phrase in normalized for phrase in OPT_OUT_PHRASES):
        return TriageDecision(lane='PASS', reason='explicit_opt_out')

    if any(normalized.startswith(starter) for starter in EXPLORE_STARTERS):
        return TriageDecision(lane='LIGHT', destination='explore', reason='question_or_explanation')
    if count <= SHORT_QUESTION_WORD_LIMIT and normalized.endswith('?'):
        return TriageDecision(lane='LIGHT', destination='explore', reason='short_question')

    if any(normalized.startswith(starter) for starter in BROAD_DESIGN_STARTERS) and any(pattern.search(normalized) for pattern in STRUCTURAL_REDESIGN_TERMS):
        return TriageDecision(lane='HEAVY', destination='autopilot', reason='structural_redesign_goal')

    if any(normalized.startswith(starter) for starter in DESIGNER_STARTERS):
        return TriageDecision(lane='LIGHT', destination='designer', reason='visual_styling_prompt')
    if any(normalized.startswith(starter) for starter in BROAD_DESIGN_STARTERS) and any(pattern.search(normalized) for pattern in VISUAL_DESIGN_TERMS):
        return TriageDecision(lane='LIGHT', destination='designer', reason='visual_styling_prompt')

    if count <= ANCHORED_EDIT_WORD_LIMIT and any(pattern.search(normalized) for pattern in EXECUTOR_ANCHOR_PATTERNS):
        return TriageDecision(lane='LIGHT', destination='executor', reason='anchored_edit')

    if count > HEAVY_WORD_THRESHOLD and any(normalized.startswith(verb) for verb in HEAVY_IMPERATIVE_VERBS):
        return TriageDecision(lane='HEAVY', destination='autopilot', reason='long_imperative_goal')

    return TriageDecision(lane='PASS', reason='ambiguous_short_prompt')


def resolve_state_path(root: Path, session_id: str | None) -> Path:
    if session_id:
        return root / 'sessions' / session_id / STATE_FILENAME
    return root / STATE_FILENAME


def read_state(root: Path, session_id: str | None) -> TriageState | None:
    path = resolve_state_path(root, session_id)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text())
    except Exception:
        return None
    if not isinstance(payload, dict):
        return None
    return TriageState(
        version=1 if payload.get('version') != 1 else payload['version'],
        last_triage=payload.get('last_triage'),
        suppress_followup=bool(payload.get('suppress_followup')),
    )


def write_state(root: Path, session_id: str | None, state: TriageState) -> Path:
    path = resolve_state_path(root, session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state.as_dict(), indent=2, ensure_ascii=False) + '\n')
    return path


def should_suppress_followup(previous: TriageState | None, current_prompt: str, *, current_has_keyword: bool = False) -> bool:
    if current_has_keyword:
        return False
    if previous is None or previous.last_triage is None or not previous.suppress_followup:
        return False
    prompt = normalize_prompt(current_prompt)
    return any(prompt.startswith(token) for token in CLARIFYING_STARTERS)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Advisory prompt triage for Oh My OpenClaw.')
    parser.add_argument('--state-root', default=None, help='State root. Defaults to .oh-my-openclaw/state')
    parser.add_argument('--session-id', default=None, help='Optional session id for session-scoped prompt-routing state')
    sub = parser.add_subparsers(dest='command', required=True)

    classify = sub.add_parser('classify', help='Classify a prompt without writing state')
    classify.add_argument('prompt', nargs='+')

    record = sub.add_parser('record', help='Classify a prompt and persist the last non-PASS triage decision')
    record.add_argument('prompt', nargs='+')
    record.add_argument('--turn-id', default=None)
    record.add_argument('--suppress-followup', dest='suppress_followup', action='store_true', default=True)
    record.add_argument('--no-suppress-followup', dest='suppress_followup', action='store_false')

    status = sub.add_parser('status', help='Show the current triage state')

    clear = sub.add_parser('clear', help='Delete the remembered triage decision')

    suppress = sub.add_parser('should-suppress', help='Check whether a follow-up prompt should suppress another triage nudge')
    suppress.add_argument('prompt', nargs='+')
    suppress.add_argument('--keyword', action='store_true', default=False, help='Bypass suppression when keyword routing already applies')

    return parser.parse_args()


def print_json(data: object) -> None:
    json.dump(data, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write('\n')


def main() -> int:
    args = parse_args()
    root = Path(args.state_root) if args.state_root else DEFAULT_STATE_ROOT

    if args.command == 'classify':
        prompt = ' '.join(args.prompt)
        decision = triage_prompt(prompt)
        print_json({'lane': decision.lane, 'destination': decision.destination, 'reason': decision.reason})
        return 0

    if args.command == 'record':
        prompt = ' '.join(args.prompt)
        normalized = normalize_prompt(prompt)
        decision = triage_prompt(prompt)
        payload = {'lane': decision.lane, 'destination': decision.destination, 'reason': decision.reason, 'written': False}
        if decision.lane != 'PASS' and decision.destination is not None:
            turn_id = args.turn_id or now_iso()
            state = TriageState(
                version=1,
                last_triage={
                    'lane': decision.lane,
                    'destination': decision.destination,
                    'reason': decision.reason,
                    'prompt_signature': prompt_signature(normalized),
                    'turn_id': turn_id,
                    'created_at': now_iso(),
                },
                suppress_followup=bool(args.suppress_followup),
            )
            path = write_state(root, args.session_id, state)
            payload['written'] = True
            payload['path'] = str(path)
            payload['state'] = state.as_dict()
        print_json(payload)
        return 0

    if args.command == 'status':
        state = read_state(root, args.session_id)
        print_json(state.as_dict() if state else {'version': 1, 'last_triage': None, 'suppress_followup': False})
        return 0

    if args.command == 'clear':
        path = resolve_state_path(root, args.session_id)
        if path.exists():
            path.unlink()
        print_json({'cleared': True, 'path': str(path)})
        return 0

    if args.command == 'should-suppress':
        prompt = ' '.join(args.prompt)
        state = read_state(root, args.session_id)
        suppress = should_suppress_followup(state, prompt, current_has_keyword=args.keyword)
        print_json({'suppress': suppress, 'reason': 'clarifying_followup' if suppress else 'no_match'})
        return 0

    raise SystemExit(f'unknown command: {args.command}')


if __name__ == '__main__':
    raise SystemExit(main())
