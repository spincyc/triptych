"""The CLI uses the same narrow rights route and retains exact payload checks."""
from __future__ import annotations

import copy
import hashlib
from pathlib import Path
import unittest

from tools.tests import test_calendar_translation_overlay as overlay_tests
from tools.tests import test_lasance_publication_binding as binding_tests


class LasancePublicationConsumerTests(unittest.TestCase):
    def setUp(self):
        self.fixture = binding_tests.LasancePublicationBindingTests(
            'test_truthful_pdf_derived_body_uses_separate_registered_rights_owner')
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.propers = overlay_tests.load_propers()
        self.entry = self.fixture.entry
        self.entry.update(mass='fixture-mass', form_id='main', proper='Collect', cycle='all', occurrence=1)
        payload = self.fixture.fixture.payload
        payload.write_text('mass\tform_id\tproper\tenglish\nfixture-mass\tmain\tCollect\tExact body.\n')
        digest = hashlib.sha256(payload.read_bytes()).hexdigest()
        self.entry['publication_artifact_sha256'] = digest
        records = self.fixture.records
        records[self.fixture.fixture.publication_artifact_id].data['sha256'] = digest
        records[self.fixture.fixture.publication_passage_id].data['artifact_sha256'] = digest
        for key in (self.fixture.fixture.page_passage_id, self.fixture.fixture.publication_passage_id):
            records[key].data['locus'] = 'fixture-mass main Collect'
        self.records = {key: dict(id=key, record_type=value.record_type, **value.data)
                        for key, value in records.items()}
        self.propers._source_library_records = lambda root: (self.records, [])
        self.calendar_root = self.fixture.fixture.root / 'src/sources/calendars'

    def validate(self, entry=None, witnesses=None):
        self.propers.validate_translation_publication_binding(
            self.entry if entry is None else entry, self.calendar_root,
            Path('fixture-inventory'),
            self.fixture.witnesses if witnesses is None else witnesses)

    def test_exact_pdf_derived_lasance_body_reaches_the_cli_contract(self):
        self.validate()
        self.assertEqual(self.records[self.fixture.page]['rights_status'], 'unresolved')
        self.assertEqual(self.records[self.fixture.page]['storage'], 'remote')

    def test_wrong_rights_owner_or_unknown_later_edition_cannot_reach_cli(self):
        self.records[self.fixture.edition]['date'] = '1955'
        with self.assertRaisesRegex(ValueError, 'registered Lasance1945'):
            self.validate()
        self.records[self.fixture.edition]['date'] = '1945'
        self.records[self.fixture.edition]['record_type'] = 'artifact'
        with self.assertRaisesRegex(ValueError, 'registered Lasance1945'):
            self.validate()
        self.records[self.fixture.edition]['record_type'] = 'edition'
        with self.assertRaisesRegex(ValueError, 'registered Lasance1945'):
            self.validate(witnesses={})
        self.records[self.fixture.rights]['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'registered Lasance1945'):
            self.validate()

    def test_body_hash_target_line_and_actual_parent_guards_remain(self):
        entry = copy.deepcopy(self.entry)
        entry['translations'][0]['text'] = 'A different or negative variant.'
        with self.assertRaises(ValueError):
            self.validate(entry)
        entry = copy.deepcopy(self.entry)
        entry['publication_artifact_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'hash is stale'):
            self.validate(entry)
        passage = self.records[self.fixture.fixture.publication_passage_id]
        passage['physical_line_ranges'] = [[1, 1]]
        with self.assertRaisesRegex(ValueError, 'one TSV body line'):
            self.validate()
        passage['physical_line_ranges'] = [[2, 2]]
        entry = copy.deepcopy(self.entry)
        entry['proper'] = 'Secret'
        with self.assertRaisesRegex(ValueError, 'does not match translation target'):
            self.validate(entry)
        self.records[self.fixture.fixture.publication_artifact_id]['derived_from'] = self.fixture.rights
        with self.assertRaisesRegex(ValueError, 'not derived from the verification artifact'):
            self.validate()


if __name__ == '__main__':
    unittest.main()
