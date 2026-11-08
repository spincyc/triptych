"""A finite noncommercial grant cannot license neighboring or substituted text."""
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import _catena
import _reviewed_permissions as policy


class ReviewedPermissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = _catena.load_sources(ROOT)
        cls.artifact = cls.sources.artifacts[policy.ARTIFACT_ID]
        cls.passages = [p for p in cls.sources.passages.values()
                        if p.get('artifact_id') == policy.ARTIFACT_ID]
        cls.reader = _catena._source_reader()

    def library(self, artifact=None, root=ROOT):
        artifact = artifact or self.artifact
        return SimpleNamespace(root=root, records={artifact['id']: SimpleNamespace(data=artifact)})

    def test_actual_passages_and_notice_reach_both_readers(self):
        self.assertEqual(len(self.passages), 3)
        for passage in self.passages:
            self.assertEqual(policy.problems(ROOT, self.artifact, passage), [])
            reading = self.reader.reading_of(self.library(), passage)
            self.assertTrue(reading['readable'], reading)
            self.assertEqual(reading['text'], passage['text'])
            work = dict.fromkeys(('id', 'title', 'author', 'category', 'languages',
                                  'alternate_titles', 'description'))
            expression = dict.fromkeys(('id', 'title', 'language', 'date', 'year',
                                        'publication', 'editors', 'translators', 'authority', 'jurisdiction'))
            expression.update(passages=[{**passage, 'reading': reading}], artifacts=[self.artifact])
            edition = self.reader.edition_payload(work, expression)
            self.assertEqual(edition['passages'][0]['acknowledgement'], self.artifact['rights_basis'])
            self.assertEqual(edition['artifacts'][0]['rights_basis'], self.artifact['rights_basis'])
            self.assertEqual(_catena._rights_notice(self.artifact)['acknowledgement'],
                             self.artifact['rights_basis'])
            self.assertEqual(_catena._passage_errors(self.sources, 'test', passage['id'],
                             'work.origen.homiliae-in-ezechielem', root=ROOT), [])
        self.assertNotIn('permission', self.reader.DISTRIBUTABLE_RIGHTS)
        self.assertIn('permission', self.reader.ATTRIBUTION_REQUIRED)

    def test_changed_identity_license_notice_status_or_payload_hash_refused(self):
        for key, value in [('id', 'artifact.other'), ('license', 'LicenseRef-Other'),
                           ('rights_basis', 'Attribution without the condition'),
                           ('rights_status', 'public-domain'), ('sha256', '0' * 64),
                           ('storage', 'remote')]:
            with self.subTest(key=key):
                artifact = {**self.artifact, key: value}
                self.assertTrue(policy.problems(ROOT, artifact))

    def test_inline_substitution_and_unpinned_or_reordered_selection_refused(self):
        for change in [{'text': 'Invented words'}, {'artifact_sha256': '0' * 64},
                       {'physical_line_ranges': [[1, 2]]},
                       {'transcription_segments': [{'line': 567, 'text': 'Invented'}]}]:
            passage = {**self.passages[0], **change}
            self.assertTrue(policy.problems(ROOT, self.artifact, passage))
            self.assertFalse(self.reader.reading_of(self.library(), passage)['readable'])

    def test_unknown_permission_is_withheld_even_with_known_license(self):
        artifact = {**self.artifact, 'id': 'artifact.unreviewed'}
        passage = {**self.passages[0], 'artifact_id': artifact['id']}
        self.assertFalse(self.reader.reading_of(self.library(artifact), passage)['readable'])

    def test_missing_changed_inventory_or_payload_refused(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.scratch/lane-linkage') as tmp:
            root = Path(tmp)
            inventory = root / policy.INVENTORY
            inventory.parent.mkdir(parents=True)
            self.assertTrue(policy.problems(root, self.artifact))
            shutil.copyfile(ROOT / policy.INVENTORY, inventory)
            self.assertTrue(policy.problems(root, self.artifact))
            payload = root / self.artifact['path']
            payload.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / self.artifact['path'], payload)
            self.assertEqual(policy.problems(root, self.artifact), [])
            payload.write_bytes(payload.read_bytes() + b'changed')
            self.assertTrue(policy.problems(root, self.artifact))
            inventory.write_text('{}')
            self.assertTrue(policy.problems(root, self.artifact))

    def test_complete_pdf_and_other_permissions_remain_withheld(self):
        for artifact in self.sources.artifacts.values():
            if artifact.get('edition_id') == self.artifact['edition_id'] and artifact['id'] != policy.ARTIFACT_ID:
                passage = {'artifact_id': artifact['id'], 'text': 'not distributable'}
                self.assertFalse(self.reader.reading_of(self.library(artifact), passage)['readable'])


if __name__ == '__main__':
    unittest.main()
