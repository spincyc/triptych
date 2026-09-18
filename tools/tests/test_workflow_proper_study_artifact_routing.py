"""Review seal checkpoints using real engine transitions and fixture verdicts."""
from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from _workflow import WorkflowEngine, WorkflowError

DOCUMENT = 'liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost'
CONTENT_REVIEWS = ['research-review', 'study-review', 'synthesis-review', 'homily-review']
OWNERS = ['research', 'author-study', 'derive-synthesis', 'derive-homily']


class EngineFixture:
    """No production content, compilation, review, or acceptance is asserted."""
    def __init__(self, case, mutate=None):
        parent = ROOT / 'build/test-tmp'
        parent.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix='artifact-routing-', dir=parent)
        case.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        shutil.copytree(ROOT / 'workflows', self.root / 'workflows')
        path = self.root / 'workflows/pipelines/proper-study.json'
        self.workflow = json.loads(path.read_text())
        self.workflow['document_discovery'].pop('validator')
        # Hash actual fixture source bytes at dispatch and validation, without
        # substituting engine sealing, result validation, or routing methods.
        (self.root / 'seal.py').write_text(
            'import hashlib,json,pathlib,sys\n'
            'print(json.dumps({"sha256":hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest()}))\n')
        (self.root / 'check.py').write_text(
            'import pathlib,sys\n'
            'pathlib.Path("artifact-check-ran").write_text("checked")\n'
            'sys.exit(int(pathlib.Path("artifact-check-fails").exists()))\n')
        self.inputs = {}
        for stage in self.workflow['stages']:
            if 'review_input_command' in stage:
                name = stage['id'].removesuffix('-review') + '.tex'
                self.inputs[stage['id']] = self.root / name
                self.inputs[stage['id']].write_text('original reviewed fixture bytes\n')
                stage['review_input_command'] = f'python3 seal.py {name}'
            for check in stage.get('checks', []):
                check['command'] = 'python3 check.py' if stage['id'] == 'artifact-gates' else 'true'
        if mutate:
            mutate(self.workflow)
        path.write_text(json.dumps(self.workflow))
        self.engine = WorkflowEngine(self.root, self.root / 'workflows')
        self.engine.standing_findings_root = None
        self.stages = {stage['id']: stage for stage in self.workflow['stages']}
        with patch.object(self.engine, 'get_repo_commit', return_value='a' * 40):
            self.run_id = self.engine.seed('proper-study', {'proper': DOCUMENT})['run_id']
        self.visited = []

    def state(self):
        return self.engine.load_state(self.run_id)

    def advance(self):
        state = self.state()
        sid = state['current_stage']
        self.visited.append(sid)
        if self.stages[sid]['type'] == 'gate':
            return self.engine.advance(self.run_id, run_gate=True)
        body = {'stage': sid, 'iteration': state['packet_hashes'][-1]['iteration'],
                'disposition': 'PASS', 'summary': 'Isolated fixture verdict only.'}
        if self.stages[sid]['type'] == 'evaluator':
            body['findings'] = []
        forwarded = state.get('findings_forwarded_ids', {}).get(sid, [])
        if forwarded:
            body['finding_dispositions'] = [{'id': value, 'outcome': 'repaired'} for value in forwarded]
        path = self.root / 'result.json'
        path.write_text(json.dumps(body))
        return self.engine.advance(self.run_id, result_path=str(path))

    def drive_to(self, target):
        for _ in range(100):
            current = self.state()['current_stage']
            if current == target:
                return
            if current in ('ACCEPTED', 'BLOCKED'):
                raise AssertionError(f'reached {current} before {target}')
            self.advance()
        raise AssertionError(f'did not reach {target}')

    def last_result(self):
        return json.loads((self.root / self.state()['result_hashes'][-1]['path']).read_text())


def artifact_stage(workflow):
    return next(stage for stage in workflow['stages'] if stage['id'] == 'artifact-gates')


class ScopeValidationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        shutil.copytree(ROOT / 'workflows', self.root / 'workflows')
        self.path = self.root / 'workflows/pipelines/proper-study.json'
        self.workflow = json.loads(self.path.read_text())
        self.engine = WorkflowEngine(self.root, self.root / 'workflows')

    def load(self, workflow):
        self.path.write_text(json.dumps(workflow))
        return self.engine.load_workflow('proper-study')

    def test_explicit_scope_requires_unique_nonempty_string_list(self):
        for invalid in (None, [], '', 'study-review', True, [None], [[]], [''],
                        ['study-review', 'study-review']):
            with self.subTest(invalid=invalid):
                workflow = copy.deepcopy(self.workflow)
                artifact_stage(workflow)['review_input_stages'] = invalid
                with self.assertRaisesRegex(WorkflowError, 'review_input_stages'):
                    self.load(workflow)

    def test_scope_rejects_unknown_nonreview_and_unsealed_evaluator(self):
        for invalid in ('absent-review', 'author-study', 'artifact-gates', 'study-review'):
            with self.subTest(invalid=invalid):
                workflow = copy.deepcopy(self.workflow)
                artifact_stage(workflow)['review_input_stages'] = [invalid]
                if invalid == 'study-review':
                    next(s for s in workflow['stages'] if s['id'] == invalid).pop('review_input_command')
                with self.assertRaisesRegex(WorkflowError, 'review_input_stages'):
                    self.load(workflow)

    def test_scope_only_allowed_on_verifying_gate(self):
        for sid in ('artifact-gates', 'author-study', 'study-review'):
            with self.subTest(stage=sid):
                workflow = copy.deepcopy(self.workflow)
                stage = next(s for s in workflow['stages'] if s['id'] == sid)
                stage.pop('verify_review_inputs', None)
                stage['review_input_stages'] = ['research-review']
                with self.assertRaisesRegex(WorkflowError, 'review_input_stages'):
                    self.load(workflow)

    def test_proper_gate_selects_content_only_and_terminal_keeps_all(self):
        workflow = self.load(self.workflow)
        self.assertEqual(artifact_stage(workflow)['review_input_stages'], CONTENT_REVIEWS)
        publication = next(s for s in workflow['stages'] if s['id'] == 'publication-gates')
        self.assertTrue(publication['verify_review_inputs'])
        self.assertNotIn('review_input_stages', publication)


class ArtifactRoutingTests(unittest.TestCase):
    def test_first_pass_checks_content_without_demanding_future_visual_or_web(self):
        fixture = EngineFixture(self)
        fixture.drive_to('artifact-gates')
        self.assertNotIn('visual-review', fixture.visited)
        self.assertNotIn('web-review', fixture.visited)
        fixture.advance()
        self.assertEqual(fixture.state()['current_stage'], 'visual-review')
        self.assertTrue((fixture.root / 'artifact-check-ran').is_file())
        fixture.drive_to('ACCEPTED')

    def test_build_edits_route_earliest_owner_before_checks_and_repeat_downstream(self):
        for index, reviewer in enumerate(CONTENT_REVIEWS):
            with self.subTest(reviewer=reviewer):
                fixture = EngineFixture(self)
                fixture.drive_to('build-artifacts')
                # Layout bytes are sealed too. Changing all later owners also
                # proves earliest-owner routing when several seals are stale.
                for changed in CONTENT_REVIEWS[index:]:
                    fixture.inputs[changed].write_text('layout changed: \\setlength{\\parskip}{6pt}\n')
                fixture.advance()
                fixture.advance()
                self.assertEqual(fixture.state()['current_stage'], OWNERS[index])
                self.assertFalse((fixture.root / 'artifact-check-ran').exists())
                self.assertEqual([f['location'] for f in fixture.last_result()['findings']], CONTENT_REVIEWS[index:])
                self.assertNotIn('visual-review', fixture.visited)
                self.assertNotIn('generate-web', fixture.visited)
                self.assertNotIn('install-publication', fixture.visited)
                fixture.drive_to('ACCEPTED')
                for position, (author, review) in enumerate(zip(OWNERS, CONTENT_REVIEWS)):
                    expected = 2 if position >= index else 1
                    self.assertEqual(fixture.visited.count(author), expected, author)
                    self.assertEqual(fixture.visited.count(review), expected, review)
                self.assertEqual(fixture.visited.count('build-artifacts'), 2)
                self.assertEqual(fixture.visited.count('visual-review'), 1)
                self.assertEqual(fixture.visited.count('web-review'), 1)

    def test_scope_order_controls_findings_but_owner_routes_keep_their_priority(self):
        def reverse(workflow):
            artifact_stage(workflow)['review_input_stages'] = list(reversed(CONTENT_REVIEWS))
        fixture = EngineFixture(self, reverse)
        fixture.drive_to('artifact-gates')
        for reviewer in CONTENT_REVIEWS:
            fixture.inputs[reviewer].write_text('changed')
        fixture.advance()
        self.assertEqual([f['location'] for f in fixture.last_result()['findings']], list(reversed(CONTENT_REVIEWS)))
        self.assertEqual(fixture.state()['current_stage'], 'research')

    def test_artifact_failure_keeps_build_retry(self):
        fixture = EngineFixture(self)
        fixture.drive_to('artifact-gates')
        (fixture.root / 'artifact-check-fails').touch()
        fixture.advance()
        self.assertEqual(fixture.state()['current_stage'], 'build-artifacts')
        self.assertEqual(fixture.last_result()['findings'][0]['check'], 'reviewed-artifact-snapshot')
        (fixture.root / 'artifact-check-fails').unlink()
        fixture.drive_to('ACCEPTED')
        self.assertEqual(fixture.visited.count('study-review'), 1)

    def test_rebuilt_artifact_skips_old_visual_seal_until_new_visual_review(self):
        fixture = EngineFixture(self)
        fixture.drive_to('publication-gates')
        fixture.inputs['visual-review'].write_bytes(b'rebuilt PDF fixture bytes')
        fixture.advance()
        self.assertEqual(fixture.state()['current_stage'], 'build-artifacts')
        fixture.advance()
        fixture.advance()
        self.assertEqual(fixture.state()['current_stage'], 'visual-review')
        fixture.drive_to('ACCEPTED')
        self.assertEqual(fixture.visited.count('study-review'), 1)
        self.assertEqual(fixture.visited.count('visual-review'), 2)
        self.assertEqual(fixture.visited.count('web-review'), 2)

    def test_scoped_terminal_gate_cannot_weaken_independent_final_all_seals_audit(self):
        def scope_terminal(workflow):
            next(s for s in workflow['stages'] if s['id'] == 'publication-gates')['review_input_stages'] = CONTENT_REVIEWS
        fixture = EngineFixture(self, scope_terminal)
        fixture.drive_to('publication-gates')
        fixture.inputs['visual-review'].write_text('changed after accepted visual review')
        with self.assertRaisesRegex(WorkflowError, 'STALE-VISUAL-REVIEW'):
            fixture.advance()
        self.assertNotEqual(fixture.state()['disposition'], 'ACCEPTED')


if __name__ == '__main__':
    unittest.main()
