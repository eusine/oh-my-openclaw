#!/usr/bin/env python3
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name('oh-my-openclaw-question.py')


class OhMyOpenClawQuestionTests(unittest.TestCase):
    def test_required_question_blocks_until_answered(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'questions'
            obligation_root = Path(tmp) / 'question-obligations'
            created = subprocess.run(
                [
                    'python3', str(SCRIPT),
                    '--root', str(root),
                    '--obligation-root', str(obligation_root),
                    'ask', '--workflow', 'deep-interview', '--slug', 'demo', '--required', 'What matters most?',
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(created.stdout)
            qid = payload['record']['question_id']
            obligation_id = payload['obligation']['obligation_id']

            blockers = subprocess.run(
                ['python3', str(SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'blockers', '--workflow', 'deep-interview', '--slug', 'demo'],
                capture_output=True,
                text=True,
            )
            self.assertEqual(blockers.returncode, 10)
            blocker_payload = json.loads(blockers.stdout)
            self.assertEqual(blocker_payload['count'], 1)
            self.assertEqual(blocker_payload['blockers'][0]['question_id'], qid)

            obligation_blockers = subprocess.run(
                ['python3', str(SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'obligation-blockers', '--workflow', 'deep-interview', '--slug', 'demo'],
                capture_output=True,
                text=True,
            )
            self.assertEqual(obligation_blockers.returncode, 10)
            obligation_payload = json.loads(obligation_blockers.stdout)
            self.assertEqual(obligation_payload['count'], 1)
            self.assertEqual(obligation_payload['blockers'][0]['obligation_id'], obligation_id)

            answered = subprocess.run(
                ['python3', str(SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'answer', qid, 'The', 'alerting', 'flow'],
                capture_output=True,
                text=True,
                check=True,
            )
            answered_payload = json.loads(answered.stdout)
            self.assertEqual(answered_payload['status'], 'answered')
            self.assertEqual(answered_payload['answer'], 'The alerting flow')

            blockers_after = subprocess.run(
                ['python3', str(SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'blockers', '--workflow', 'deep-interview', '--slug', 'demo'],
                capture_output=True,
                text=True,
            )
            self.assertEqual(blockers_after.returncode, 0)
            self.assertEqual(json.loads(blockers_after.stdout)['count'], 0)

            obligation_blockers_after_answer = subprocess.run(
                ['python3', str(SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'obligation-blockers', '--workflow', 'deep-interview', '--slug', 'demo'],
                capture_output=True,
                text=True,
            )
            self.assertEqual(obligation_blockers_after_answer.returncode, 10)
            self.assertEqual(json.loads(obligation_blockers_after_answer.stdout)['count'], 1)

            satisfied = subprocess.run(
                ['python3', str(SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'satisfy-obligation', obligation_id, '--question-id', qid],
                capture_output=True,
                text=True,
                check=True,
            )
            satisfied_payload = json.loads(satisfied.stdout)
            self.assertEqual(satisfied_payload['status'], 'satisfied')
            self.assertEqual(satisfied_payload['question_id'], qid)
            self.assertEqual(satisfied_payload['resolution'], 'consumed')
            self.assertIsNotNone(satisfied_payload['satisfied_at'])

            obligation_blockers_after_satisfy = subprocess.run(
                ['python3', str(SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'obligation-blockers', '--workflow', 'deep-interview', '--slug', 'demo'],
                capture_output=True,
                text=True,
            )
            self.assertEqual(obligation_blockers_after_satisfy.returncode, 0)
            self.assertEqual(json.loads(obligation_blockers_after_satisfy.stdout)['count'], 0)

    def test_clear_marks_resolution_and_clears_pending_obligation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'questions'
            obligation_root = Path(tmp) / 'question-obligations'
            created = subprocess.run(
                [
                    'python3', str(SCRIPT),
                    '--root', str(root),
                    '--obligation-root', str(obligation_root),
                    'ask', '--workflow', 'deep-interview', '--slug', 'demo', '--required', 'Need a preference?',
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(created.stdout)
            qid = payload['record']['question_id']
            obligation_id = payload['obligation']['obligation_id']

            cleared = subprocess.run(
                ['python3', str(SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'clear', qid, '--resolution', 'consumed-by-interview'],
                capture_output=True,
                text=True,
                check=True,
            )
            clear_payload = json.loads(cleared.stdout)
            self.assertEqual(clear_payload['record']['status'], 'cleared')
            self.assertEqual(clear_payload['record']['resolution'], 'consumed-by-interview')
            self.assertIsNotNone(clear_payload['record']['cleared_at'])
            self.assertEqual(clear_payload['obligation']['status'], 'cleared')
            self.assertEqual(clear_payload['obligation']['clear_reason'], 'consumed-by-interview')

            obligation_status = subprocess.run(
                ['python3', str(SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'obligation-status', obligation_id],
                capture_output=True,
                text=True,
                check=True,
            )
            obligation_payload = json.loads(obligation_status.stdout)
            self.assertEqual(obligation_payload['status'], 'cleared')
            self.assertEqual(obligation_payload['clear_reason'], 'consumed-by-interview')

    def test_answered_pending_lists_answered_required_question_with_pending_obligation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'questions'
            obligation_root = Path(tmp) / 'question-obligations'
            created = subprocess.run(
                [
                    'python3', str(SCRIPT),
                    '--root', str(root),
                    '--obligation-root', str(obligation_root),
                    'ask', '--workflow', 'deep-interview', '--slug', 'scope-test', '--required', 'Which scope?',
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(created.stdout)
            qid = payload['record']['question_id']
            obligation_id = payload['obligation']['obligation_id']

            subprocess.run(
                ['python3', str(SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'answer', qid, 'First pass only'],
                capture_output=True,
                text=True,
                check=True,
            )

            pending = subprocess.run(
                ['python3', str(SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'answered-pending', '--workflow', 'deep-interview', '--slug', 'scope-test'],
                capture_output=True,
                text=True,
            )
            self.assertEqual(pending.returncode, 10)
            pending_payload = json.loads(pending.stdout)
            self.assertEqual(pending_payload['count'], 1)
            self.assertEqual(pending_payload['answered_pending'][0]['question']['question_id'], qid)
            self.assertEqual(pending_payload['answered_pending'][0]['obligation']['obligation_id'], obligation_id)

            subprocess.run(
                ['python3', str(SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'satisfy-obligation', obligation_id, '--question-id', qid],
                capture_output=True,
                text=True,
                check=True,
            )
            clear = subprocess.run(
                ['python3', str(SCRIPT), '--root', str(root), '--obligation-root', str(obligation_root), 'answered-pending', '--workflow', 'deep-interview', '--slug', 'scope-test'],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(json.loads(clear.stdout)['count'], 0)

    def test_invalid_record_id_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'questions'
            obligation_root = Path(tmp) / 'question-obligations'
            result = subprocess.run(
                [
                    'python3', str(SCRIPT),
                    '--root', str(root),
                    '--obligation-root', str(obligation_root),
                    'status', '../escape',
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('invalid question_id', result.stderr + result.stdout)


if __name__ == '__main__':
    unittest.main()
