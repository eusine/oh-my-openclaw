#!/usr/bin/env python3
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


QUESTION_SCRIPT = Path(__file__).with_name('oh-my-openclaw-question.py')
RUN_OUTCOME_SCRIPT = Path(__file__).with_name('oh-my-openclaw-run-outcome.py')


class OhMyOpenClawDeepInterviewFlowTests(unittest.TestCase):
    def test_answered_required_question_can_be_consumed_before_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'questions'
            obligation_root = Path(tmp) / 'question-obligations'
            state = Path(tmp) / 'deep-interview-state.json'
            state.write_text(json.dumps({
                'active': True,
                'mode': 'deep-interview',
                'current_phase': 'deep-interview',
                'state': {
                    'slug': 'handoff-demo',
                    'prompt_safe_summary_status': 'recorded',
                    'run_outcome': 'continue',
                },
            }))

            created = subprocess.run(
                [
                    'python3', str(QUESTION_SCRIPT),
                    '--root', str(root),
                    '--obligation-root', str(obligation_root),
                    'ask', '--workflow', 'deep-interview', '--slug', 'handoff-demo', '--required',
                    'What must stay out of scope?',
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(created.stdout)
            qid = payload['record']['question_id']
            oid = payload['obligation']['obligation_id']

            subprocess.run(
                ['python3', str(QUESTION_SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'answer', qid, 'No payment changes'],
                capture_output=True,
                text=True,
                check=True,
            )

            pending = subprocess.run(
                ['python3', str(QUESTION_SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'answered-pending', '--workflow', 'deep-interview', '--slug', 'handoff-demo'],
                capture_output=True,
                text=True,
            )
            self.assertEqual(pending.returncode, 10)
            self.assertEqual(json.loads(pending.stdout)['answered_pending'][0]['question']['answer'], 'No payment changes')

            subprocess.run(
                ['python3', str(QUESTION_SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'satisfy-obligation', oid, '--question-id', qid, '--resolution', 'consumed-before-handoff'],
                capture_output=True,
                text=True,
                check=True,
            )
            blockers = subprocess.run(
                ['python3', str(QUESTION_SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'obligation-blockers', '--workflow', 'deep-interview', '--slug', 'handoff-demo'],
                capture_output=True,
                text=True,
            )
            self.assertEqual(blockers.returncode, 0)
            self.assertEqual(json.loads(blockers.stdout)['count'], 0)

            state_payload = json.loads(state.read_text())
            state_payload['active'] = False
            state_payload['run_outcome'] = 'finish'
            state.write_text(json.dumps(state_payload))
            outcome = subprocess.run(
                ['python3', str(RUN_OUTCOME_SCRIPT), 'apply', str(state), '--now-iso', '2026-04-24T10:00:00Z'],
                capture_output=True,
                text=True,
                check=True,
            )
            outcome_payload = json.loads(outcome.stdout)
            self.assertEqual(outcome_payload['state']['run_outcome'], 'finish')
            self.assertFalse(outcome_payload['state']['active'])


if __name__ == '__main__':
    unittest.main()
