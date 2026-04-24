#!/usr/bin/env python3
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name('oh-my-openclaw-triage.py')


class OhMyOpenClawTriageTests(unittest.TestCase):
    def test_classifies_light_and_heavy_prompts(self) -> None:
        explain = subprocess.run(
            ['python3', str(SCRIPT), 'classify', 'explain', 'this', 'function'],
            capture_output=True,
            text=True,
            check=True,
        )
        explain_payload = json.loads(explain.stdout)
        self.assertEqual(explain_payload['lane'], 'LIGHT')
        self.assertEqual(explain_payload['destination'], 'explore')

        heavy = subprocess.run(
            ['python3', str(SCRIPT), 'classify', 'add', 'dark', 'mode', 'toggle', 'to', 'the', 'settings', 'page'],
            capture_output=True,
            text=True,
            check=True,
        )
        heavy_payload = json.loads(heavy.stdout)
        self.assertEqual(heavy_payload['lane'], 'HEAVY')
        self.assertEqual(heavy_payload['destination'], 'autopilot')

    def test_record_writes_non_pass_state_and_status_reads_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            record = subprocess.run(
                [
                    'python3', str(SCRIPT),
                    '--state-root', tmp,
                    '--session-id', 'sess-1',
                    'record', 'fix', 'typo', 'in', 'src/foo.ts',
                    '--turn-id', 'turn-123',
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(record.stdout)
            self.assertTrue(payload['written'])
            self.assertEqual(payload['lane'], 'LIGHT')
            self.assertEqual(payload['destination'], 'executor')

            status = subprocess.run(
                ['python3', str(SCRIPT), '--state-root', tmp, '--session-id', 'sess-1', 'status'],
                capture_output=True,
                text=True,
                check=True,
            )
            status_payload = json.loads(status.stdout)
            self.assertEqual(status_payload['last_triage']['destination'], 'executor')
            self.assertEqual(status_payload['last_triage']['turn_id'], 'turn-123')

    def test_should_suppress_clarifying_followup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [
                    'python3', str(SCRIPT),
                    '--state-root', tmp,
                    '--session-id', 'sess-1',
                    'record', 'add', 'dark', 'mode', 'toggle', 'to', 'the', 'settings', 'page',
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            suppress = subprocess.run(
                ['python3', str(SCRIPT), '--state-root', tmp, '--session-id', 'sess-1', 'should-suppress', 'yes,', 'that', 'one'],
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(suppress.stdout)
            self.assertTrue(payload['suppress'])
            self.assertEqual(payload['reason'], 'clarifying_followup')

    def test_pass_prompt_does_not_write_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            record = subprocess.run(
                ['python3', str(SCRIPT), '--state-root', tmp, 'record', 'thanks'],
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(record.stdout)
            self.assertFalse(payload['written'])

            status = subprocess.run(
                ['python3', str(SCRIPT), '--state-root', tmp, 'status'],
                capture_output=True,
                text=True,
                check=True,
            )
            status_payload = json.loads(status.stdout)
            self.assertIsNone(status_payload['last_triage'])

    def test_korean_two_set_ulw_alias_routes_to_ultrawork(self) -> None:
        result = subprocess.run(
            ['python3', str(SCRIPT), 'classify', 'ㅕㅣㅈ', 'tests', 'and', 'lint'],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload['lane'], 'LIGHT')
        self.assertEqual(payload['destination'], 'ultrawork')
        self.assertEqual(payload['reason'], 'ultrawork_keyword')


if __name__ == '__main__':
    unittest.main()
