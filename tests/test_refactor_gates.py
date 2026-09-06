"""Execute the real refactor routing/outcomes with fixture verifier results.

Requires Praxec and PyYAML. External effects and the model are excluded; the
continuation runtime itself is tested in the paired Praxec PR.
"""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
FLOW = yaml.safe_load((ROOT / "orchestrators/flow.refactor.god-file.yaml").read_text())["workflows"]["flow.refactor.god-file"]

class GateTests(unittest.TestCase):
    def start(self, passed, diagnostics, iteration=1, state="build_gate"):
        states = {k: copy.deepcopy(FLOW['states'][k]) for k in ('build_gate', 'done', 'unresolved', 'needs_human')}
        # Stop at repair dispatch. No producer is called by these routing tests.
        states['fixing'] = {'terminal': True}
        definition = {'initialState': state, 'initialContext': {
            'build_passed': passed, 'diagnostics_available': diagnostics,
            'build_issues': 'fixture', 'fix_iter': iteration,
        }, 'outcomes': FLOW['outcomes'], 'states': states}
        with tempfile.TemporaryDirectory(prefix='praxec-gate-test-') as td:
            root = Path(td)
            config = {'version': '1.0.0', 'praxec': {'_writableRepos': [{'root': td, 'push': False}]},
                      'store': {'kind': 'sqlite', 'path': str(root / 'state.db')}, 'workflows': {'task': definition}}
            path = root / 'gateway.yaml'
            path.write_text(json.dumps(config))
            result = subprocess.run(['praxec', 'command', '--config', str(path), json.dumps({'definitionId': 'task'})],
                                    capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            response = json.loads(result.stdout)
            self.assertNotIn('error', response, response.get('error'))
            return response

    def test_green_build_reaches_verified_success(self):
        result = self.start(True, True)
        self.assertEqual(result['workflow']['state'], 'done')
        self.assertEqual(result['result']['status'], 'succeeded')

    def test_missing_diagnostics_parks_before_model(self):
        self.assertEqual(self.start(False, False)['workflow']['state'], 'needs_human')

    def test_real_diagnostics_reach_bounded_repair(self):
        self.assertEqual(self.start(False, True)['workflow']['state'], 'fixing')
        self.assertEqual(self.start(False, True, 4)['workflow']['state'], 'needs_human')

    def test_acknowledged_unresolved_build_cannot_be_success(self):
        target = FLOW['states']['needs_human']['transitions']['review_scope']['target']
        result = self.start(False, False, state=target)
        self.assertEqual(result['result']['status'], 'failed')

if __name__ == '__main__':
    unittest.main()
