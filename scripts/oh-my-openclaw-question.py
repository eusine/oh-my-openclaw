#!/usr/bin/env python3
"""Structured question + question-obligation helper for Oh My OpenClaw.

This gives the workflow layer an owned question record even when the runtime
only has plain chat turns. It keeps pending questions durable under
`.oh-my-openclaw/state/questions/` and tracks required-question obligations
under `.oh-my-openclaw/state/question-obligations/` so deep-interview and
future workflows can block, resume, and clear interactive obligations
explicitly.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


DEFAULT_ROOT = Path('.oh-my-openclaw/state/questions')
DEFAULT_OBLIGATION_ROOT = Path('.oh-my-openclaw/state/question-obligations')
RECORD_ID_PATTERN = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]*$')


def validate_record_id(record_id: str, *, label: str = 'record id') -> str:
    value = (record_id or '').strip()
    if not value:
        raise SystemExit(f'{label} is required')
    if not RECORD_ID_PATTERN.fullmatch(value):
        raise SystemExit(f'invalid {label}: {record_id}')
    return value


@dataclass
class JsonStore:
    root: Path

    def ensure(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)

    def path_for(self, record_id: str) -> Path:
        safe_id = validate_record_id(record_id)
        return self.root / f'{safe_id}.json'

    def load(self, record_id: str) -> dict:
        path = self.path_for(record_id)
        if not path.exists():
            raise SystemExit(f'record not found: {record_id}')
        return json.loads(path.read_text())

    def save(self, record: dict, *, key: str) -> Path:
        self.ensure()
        path = self.path_for(record[key])
        path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n')
        return path

    def records(self) -> list[dict]:
        if not self.root.exists():
            return []
        items: list[dict] = []
        for path in sorted(self.root.glob('*.json')):
            try:
                items.append(json.loads(path.read_text()))
            except Exception:
                continue
        return items


@dataclass
class QuestionStore(JsonStore):
    def save(self, record: dict) -> Path:
        return super().save(record, key='question_id')


@dataclass
class ObligationStore(JsonStore):
    def save(self, record: dict) -> Path:
        return super().save(record, key='obligation_id')


@dataclass
class Stores:
    questions: QuestionStore
    obligations: ObligationStore


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def make_slug_prefix(value: str | None, *, fallback: str) -> str:
    prefix = (value or fallback).strip().lower().replace(' ', '-')
    prefix = ''.join(ch for ch in prefix if ch.isalnum() or ch == '-') or fallback
    return prefix


def make_question_id(slug: str | None) -> str:
    prefix = make_slug_prefix(slug, fallback='question')
    stamp = datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')
    return f'{prefix}-{stamp}-{uuid4().hex[:8]}'


def make_obligation_id(workflow: str, slug: str | None) -> str:
    prefix = make_slug_prefix(f'{workflow}-question-{slug or "required"}', fallback='question-obligation')
    stamp = datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')
    return f'{prefix}-{stamp}-{uuid4().hex[:8]}'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Manage structured question records for Oh My OpenClaw workflows.')
    parser.add_argument('--root', default=os.environ.get('OH_MY_OPENCLAW_QUESTION_ROOT'), help='Question state directory. Defaults to .oh-my-openclaw/state/questions')
    parser.add_argument('--obligation-root', default=os.environ.get('OH_MY_OPENCLAW_OBLIGATION_ROOT'), help='Question-obligation state directory. Defaults to .oh-my-openclaw/state/question-obligations')
    sub = parser.add_subparsers(dest='command', required=True)

    ask = sub.add_parser('ask', help='Create a pending question record')
    ask.add_argument('prompt', nargs='+', help='Question prompt text')
    ask.add_argument('--workflow', default='deep-interview')
    ask.add_argument('--slug')
    ask.add_argument('--interview-id')
    ask.add_argument('--required', action='store_true', default=False)
    ask.add_argument('--renderer', default='plain-chat')
    ask.add_argument('--channel')
    ask.add_argument('--question-id')
    ask.add_argument('--obligation-id')

    answer = sub.add_parser('answer', help='Attach an answer to a question record')
    answer.add_argument('question_id')
    answer.add_argument('answer', nargs='*')
    answer.add_argument('--from-stdin', action='store_true')

    clear = sub.add_parser('clear', help='Mark a question as cleared/resolved')
    clear.add_argument('question_id')
    clear.add_argument('--resolution', default='resolved')

    cancel = sub.add_parser('cancel', help='Cancel a question')
    cancel.add_argument('question_id')
    cancel.add_argument('--reason', default='canceled')

    status = sub.add_parser('status', help='Show a single question record')
    status.add_argument('question_id')

    ls = sub.add_parser('list', help='List question records')
    ls.add_argument('--status')
    ls.add_argument('--workflow')
    ls.add_argument('--slug')

    blockers = sub.add_parser('blockers', help='List unresolved required questions')
    blockers.add_argument('--workflow')
    blockers.add_argument('--slug')

    answered_pending = sub.add_parser('answered-pending', help='List answered questions whose required obligations are still pending/active')
    answered_pending.add_argument('--workflow')
    answered_pending.add_argument('--slug')

    obligate = sub.add_parser('obligate', help='Create or refresh a pending required-question obligation')
    obligate.add_argument('--workflow', default='deep-interview')
    obligate.add_argument('--slug')
    obligate.add_argument('--interview-id')
    obligate.add_argument('--question-id')
    obligate.add_argument('--required', action='store_true', default=False)
    obligate.add_argument('--obligation-id')
    obligate.add_argument('--source', default='oh-my-openclaw-question')

    satisfy = sub.add_parser('satisfy-obligation', help='Mark a question obligation as satisfied after consumption')
    satisfy.add_argument('obligation_id')
    satisfy.add_argument('--question-id')
    satisfy.add_argument('--resolution', default='consumed')

    clear_obligation = sub.add_parser('clear-obligation', help='Clear a question obligation without satisfying it')
    clear_obligation.add_argument('obligation_id')
    clear_obligation.add_argument('--reason', default='handoff')

    obligation_status = sub.add_parser('obligation-status', help='Show a single question obligation')
    obligation_status.add_argument('obligation_id')

    obligation_list = sub.add_parser('obligations', help='List question obligations')
    obligation_list.add_argument('--status')
    obligation_list.add_argument('--workflow')
    obligation_list.add_argument('--slug')
    obligation_list.add_argument('--question-id')

    obligation_blockers = sub.add_parser('obligation-blockers', help='List unresolved required-question obligations')
    obligation_blockers.add_argument('--workflow')
    obligation_blockers.add_argument('--slug')

    return parser.parse_args()


def stores_from_args(args: argparse.Namespace) -> Stores:
    question_root = Path(args.root) if args.root else DEFAULT_ROOT
    obligation_root = Path(args.obligation_root) if args.obligation_root else DEFAULT_OBLIGATION_ROOT
    return Stores(
        questions=QuestionStore(root=question_root),
        obligations=ObligationStore(root=obligation_root),
    )


def print_json(data: object) -> None:
    json.dump(data, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write('\n')


def create_or_refresh_obligation(stores: Stores, *, workflow: str, slug: str | None, interview_id: str | None, question_id: str | None, required: bool, obligation_id: str | None = None, source: str = 'oh-my-openclaw-question') -> tuple[dict, Path]:
    timestamp = now_iso()
    record = None
    path = None
    if obligation_id:
        obligation_path = stores.obligations.path_for(obligation_id)
        if obligation_path.exists():
            record = stores.obligations.load(obligation_id)
    if record is None:
        record = {
            'obligation_id': obligation_id or make_obligation_id(workflow, slug),
            'workflow': workflow,
            'slug': slug,
            'interview_id': interview_id,
            'question_id': question_id,
            'required': bool(required),
            'source': source,
            'status': 'pending',
            'requested_at': timestamp,
            'updated_at': timestamp,
            'satisfied_at': None,
            'cleared_at': None,
            'resolution': None,
            'clear_reason': None,
        }
    else:
        record.update({
            'workflow': workflow,
            'slug': slug,
            'interview_id': interview_id,
            'question_id': question_id,
            'required': bool(required),
            'source': source,
            'status': 'pending',
            'updated_at': timestamp,
            'satisfied_at': None,
            'cleared_at': None,
            'resolution': None,
            'clear_reason': None,
        })
    path = stores.obligations.save(record)
    return record, path


def maybe_clear_pending_obligation(stores: Stores, obligation_id: str | None, *, reason: str) -> dict | None:
    if not obligation_id:
        return None
    obligation_path = stores.obligations.path_for(obligation_id)
    if not obligation_path.exists():
        return None
    record = stores.obligations.load(obligation_id)
    if record.get('status') != 'pending':
        return record
    timestamp = now_iso()
    record['status'] = 'cleared'
    record['clear_reason'] = reason
    record['cleared_at'] = timestamp
    record['updated_at'] = timestamp
    stores.obligations.save(record)
    return record


def cmd_ask(args: argparse.Namespace, stores: Stores) -> int:
    question_id = validate_record_id(args.question_id, label='question_id') if args.question_id else make_question_id(args.slug)
    created_at = now_iso()
    obligation = None
    obligation_path = None
    if args.required:
        obligation, obligation_path = create_or_refresh_obligation(
            stores,
            workflow=args.workflow,
            slug=args.slug,
            interview_id=args.interview_id,
            question_id=question_id,
            required=True,
            obligation_id=validate_record_id(args.obligation_id, label='obligation_id') if args.obligation_id else None,
        )
    record = {
        'question_id': question_id,
        'workflow': args.workflow,
        'slug': args.slug,
        'interview_id': args.interview_id,
        'prompt': ' '.join(args.prompt).strip(),
        'required': bool(args.required),
        'renderer': args.renderer,
        'channel': args.channel,
        'status': 'pending',
        'created_at': created_at,
        'updated_at': created_at,
        'answered_at': None,
        'cleared_at': None,
        'answer': None,
        'resolution': None,
        'obligation_id': obligation['obligation_id'] if obligation else None,
    }
    path = stores.questions.save(record)
    payload = {'record': record, 'path': str(path)}
    if obligation and obligation_path:
        payload['obligation'] = obligation
        payload['obligation_path'] = str(obligation_path)
    print_json(payload)
    return 0


def cmd_answer(args: argparse.Namespace, stores: Stores) -> int:
    record = stores.questions.load(validate_record_id(args.question_id, label='question_id'))
    answer_text = sys.stdin.read().strip() if args.from_stdin else ' '.join(args.answer).strip()
    if not answer_text:
        raise SystemExit('answer text is required')
    ts = now_iso()
    record['answer'] = answer_text
    record['answered_at'] = ts
    record['updated_at'] = ts
    record['status'] = 'answered'
    stores.questions.save(record)
    print_json(record)
    return 0


def cmd_clear(args: argparse.Namespace, stores: Stores) -> int:
    record = stores.questions.load(validate_record_id(args.question_id, label='question_id'))
    ts = now_iso()
    record['status'] = 'cleared'
    record['resolution'] = args.resolution
    record['cleared_at'] = ts
    record['updated_at'] = ts
    stores.questions.save(record)
    obligation = maybe_clear_pending_obligation(stores, record.get('obligation_id'), reason=args.resolution)
    payload = {'record': record, 'obligation': obligation}
    print_json(payload)
    return 0


def cmd_cancel(args: argparse.Namespace, stores: Stores) -> int:
    record = stores.questions.load(validate_record_id(args.question_id, label='question_id'))
    ts = now_iso()
    record['status'] = 'canceled'
    record['resolution'] = args.reason
    record['updated_at'] = ts
    stores.questions.save(record)
    obligation = maybe_clear_pending_obligation(stores, record.get('obligation_id'), reason=args.reason)
    payload = {'record': record, 'obligation': obligation}
    print_json(payload)
    return 0


def _filtered_records(records: list[dict], *, status: str | None = None, workflow: str | None = None, slug: str | None = None) -> list[dict]:
    out = []
    for record in records:
        if status and record.get('status') != status:
            continue
        if workflow and record.get('workflow') != workflow:
            continue
        if slug and record.get('slug') != slug:
            continue
        out.append(record)
    return out


def _filtered_obligations(records: list[dict], *, status: str | None = None, workflow: str | None = None, slug: str | None = None, question_id: str | None = None) -> list[dict]:
    out = []
    for record in records:
        if status and record.get('status') != status:
            continue
        if workflow and record.get('workflow') != workflow:
            continue
        if slug and record.get('slug') != slug:
            continue
        if question_id and record.get('question_id') != question_id:
            continue
        out.append(record)
    return out


def cmd_status(args: argparse.Namespace, stores: Stores) -> int:
    print_json(stores.questions.load(validate_record_id(args.question_id, label='question_id')))
    return 0


def cmd_list(args: argparse.Namespace, stores: Stores) -> int:
    records = _filtered_records(stores.questions.records(), status=args.status, workflow=args.workflow, slug=args.slug)
    print_json(records)
    return 0


def cmd_blockers(args: argparse.Namespace, stores: Stores) -> int:
    records = _filtered_records(stores.questions.records(), workflow=args.workflow, slug=args.slug)
    blockers = [
        record for record in records
        if record.get('required') and record.get('status') == 'pending'
    ]
    print_json({'count': len(blockers), 'blockers': blockers})
    return 10 if blockers else 0


def cmd_answered_pending(args: argparse.Namespace, stores: Stores) -> int:
    records = _filtered_records(stores.questions.records(), workflow=args.workflow, slug=args.slug)
    obligations_by_question = {
        record.get('question_id'): record
        for record in stores.obligations.records()
        if record.get('question_id') and record.get('required') and record.get('status') == 'pending'
    }
    answered = []
    for record in records:
        obligation = obligations_by_question.get(record.get('question_id'))
        if not obligation:
            continue
        if record.get('required') and record.get('status') == 'answered':
            answered.append({'question': record, 'obligation': obligation})
    print_json({'count': len(answered), 'answered_pending': answered})
    return 10 if answered else 0


def cmd_obligate(args: argparse.Namespace, stores: Stores) -> int:
    obligation, path = create_or_refresh_obligation(
        stores,
        workflow=args.workflow,
        slug=args.slug,
        interview_id=args.interview_id,
        question_id=validate_record_id(args.question_id, label='question_id') if args.question_id else None,
        required=bool(args.required),
        obligation_id=validate_record_id(args.obligation_id, label='obligation_id') if args.obligation_id else None,
        source=args.source,
    )
    print_json({'record': obligation, 'path': str(path)})
    return 0


def cmd_satisfy_obligation(args: argparse.Namespace, stores: Stores) -> int:
    record = stores.obligations.load(validate_record_id(args.obligation_id, label='obligation_id'))
    ts = now_iso()
    record['status'] = 'satisfied'
    record['question_id'] = validate_record_id(args.question_id, label='question_id') if args.question_id else record.get('question_id')
    record['resolution'] = args.resolution
    record['satisfied_at'] = ts
    record['updated_at'] = ts
    record['cleared_at'] = None
    record['clear_reason'] = None
    stores.obligations.save(record)
    print_json(record)
    return 0


def cmd_clear_obligation(args: argparse.Namespace, stores: Stores) -> int:
    record = stores.obligations.load(validate_record_id(args.obligation_id, label='obligation_id'))
    ts = now_iso()
    record['status'] = 'cleared'
    record['clear_reason'] = args.reason
    record['cleared_at'] = ts
    record['updated_at'] = ts
    stores.obligations.save(record)
    print_json(record)
    return 0


def cmd_obligation_status(args: argparse.Namespace, stores: Stores) -> int:
    print_json(stores.obligations.load(validate_record_id(args.obligation_id, label='obligation_id')))
    return 0


def cmd_obligations(args: argparse.Namespace, stores: Stores) -> int:
    records = _filtered_obligations(
        stores.obligations.records(),
        status=args.status,
        workflow=args.workflow,
        slug=args.slug,
        question_id=validate_record_id(args.question_id, label='question_id') if args.question_id else None,
    )
    print_json(records)
    return 0


def cmd_obligation_blockers(args: argparse.Namespace, stores: Stores) -> int:
    blockers = [
        record for record in _filtered_obligations(stores.obligations.records(), workflow=args.workflow, slug=args.slug)
        if record.get('required') and record.get('status') == 'pending'
    ]
    print_json({'count': len(blockers), 'blockers': blockers})
    return 10 if blockers else 0


def main() -> int:
    args = parse_args()
    stores = stores_from_args(args)
    command = args.command
    if command == 'ask':
        return cmd_ask(args, stores)
    if command == 'answer':
        return cmd_answer(args, stores)
    if command == 'clear':
        return cmd_clear(args, stores)
    if command == 'cancel':
        return cmd_cancel(args, stores)
    if command == 'status':
        return cmd_status(args, stores)
    if command == 'list':
        return cmd_list(args, stores)
    if command == 'blockers':
        return cmd_blockers(args, stores)
    if command == 'answered-pending':
        return cmd_answered_pending(args, stores)
    if command == 'obligate':
        return cmd_obligate(args, stores)
    if command == 'satisfy-obligation':
        return cmd_satisfy_obligation(args, stores)
    if command == 'clear-obligation':
        return cmd_clear_obligation(args, stores)
    if command == 'obligation-status':
        return cmd_obligation_status(args, stores)
    if command == 'obligations':
        return cmd_obligations(args, stores)
    if command == 'obligation-blockers':
        return cmd_obligation_blockers(args, stores)
    raise SystemExit(f'unknown command: {command}')


if __name__ == '__main__':
    raise SystemExit(main())
