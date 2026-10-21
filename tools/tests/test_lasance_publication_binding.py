"""The registered Lasance1945 basis does not clear arbitrary later witnesses."""
from __future__ import annotations

import copy
from pathlib import Path
import tomllib
import unittest

from tools.tests import test_calendar_translation_overlay as overlay_tests

ROOT = Path(__file__).resolve().parents[2]


class LasancePublicationBindingTests(unittest.TestCase):
    def setUp(self):
        # Reuse the current dual-binding fixture; do not fork its TSV/body
        # contract or manufacture a real liturgical payload for this test.
        self.fixture = overlay_tests.PublicationBindingTests(
            'test_valid_dual_binding_keeps_remote_page_proof_separate')
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        self.checker = self.fixture.checker
        self.records = self.fixture.records
        self.entry = self.fixture.entry
        self.edition = self.checker.LASANCE_1945_EDITION
        self.page = self.checker.LASANCE_1945_PAGE_ARTIFACT
        self.rights = self.checker.LASANCE_1945_RIGHTS_ARTIFACT
        self.records[self.edition] = self.records.pop(self.fixture.edition_id)
        self.records[self.edition].data['date'] = '1945'
        self.records[self.page] = self.records.pop(self.fixture.page_artifact_id)
        self.records[self.page].data['sha256'] = self.checker.LASANCE_1945_PAGE_SHA256
        for item in self.records.values():
            if 'edition_id' in item.data:
                item.data['edition_id'] = self.edition
        self.records[self.fixture.page_passage_id].data.update(
            artifact_id=self.page, artifact_sha256=self.checker.LASANCE_1945_PAGE_SHA256)
        self.records[self.fixture.publication_artifact_id].data['derived_from'] = self.page
        self.records[self.rights] = overlay_tests.record(
            'artifact', edition_id=self.edition,
            sha256=self.checker.LASANCE_1945_RIGHTS_SHA256,
            rights_status='public-domain', rights_jurisdiction='United States', storage='tracked')
        self.entry.update(artifact_id=self.page, witness='lasance-1945')
        self.entry['translations'][0]['source_id'] = self.edition
        self.witnesses = {'lasance-1945': dict(
            source_id=self.edition, artifact_id=self.rights, rights='public-domain',
            caution='Original 1945 expression only; both lettered insert ranges excluded.')}

    def publication(self, entry=None, witnesses=None):
        return self.checker.overlay_entry_publication_problems(
            'entry', self.entry if entry is None else entry,
            self.witnesses if witnesses is None else witnesses)

    def source(self, entry=None):
        return self.checker.overlay_entry_source_problems(
            'entry', self.entry if entry is None else entry, self.witnesses)

    def test_truthful_pdf_derived_body_uses_separate_registered_rights_owner(self):
        self.assertEqual(self.publication(), [])
        self.assertEqual(self.source(), [])
        self.assertEqual(self.records[self.page].data['rights_status'], 'unresolved')
        self.assertEqual(self.records[self.page].data['storage'], 'remote')
        self.assertNotEqual(self.entry['publication_artifact_id'], self.page)

    def test_declared_correction_of_approved_ocr_is_also_supported(self):
        self.records[self.fixture.publication_artifact_id].data['derived_from'] = self.rights
        self.assertEqual(self.publication(), [])

    def test_unknown_later_edition_and_unapproved_source_row_fail(self):
        for date in ('1937', '1955', '1962'):
            with self.subTest(date=date):
                self.records[self.edition].data['date'] = date
                self.assertIn('registered Lasance1945', '\n'.join(self.publication()))
        self.records[self.edition].data['date'] = '1945'
        publication = self.records[self.fixture.publication_artifact_id].data
        publication['edition_id'] = 'edition.other.1945'
        self.records['edition.other.1945'] = overlay_tests.record('edition', date='1945')
        self.assertIn('registered Lasance1945', '\n'.join(self.publication()))
        publication['edition_id'] = self.edition
        for field, value in [('source_id', 'edition.other.1945'),
                             ('artifact_id', self.page), ('rights', 'permission')]:
            with self.subTest(field=field):
                witnesses = copy.deepcopy(self.witnesses)
                witnesses['lasance-1945'][field] = value
                self.assertIn('registered Lasance1945', '\n'.join(self.publication(witnesses=witnesses)))
        self.assertIn('registered Lasance1945', '\n'.join(self.publication(witnesses={})))
        entry = copy.deepcopy(self.entry)
        entry['witness'] = 'another-lasance-book'
        self.assertIn('registered Lasance1945', '\n'.join(self.publication(entry)))

    def test_rights_anchor_cannot_be_replaced_by_a_freeform_pd_claim(self):
        item = self.records[self.rights]
        for field, value in [('sha256', '0' * 64), ('rights_status', 'unresolved'),
                             ('rights_jurisdiction', 'elsewhere'), ('storage', 'remote'),
                             ('edition_id', 'edition.other.1945')]:
            with self.subTest(field=field):
                original = item.data[field]
                item.data[field] = value
                item.data['rights_basis'] = 'This is public domain; permission granted.'
                self.assertIn('registered Lasance1945', '\n'.join(self.publication()))
                item.data[field] = original

    def test_wrong_derivation_or_changed_private_pdf_identity_fails(self):
        artifact = self.records[self.fixture.publication_artifact_id].data
        for parent in (None, 'artifact.unknown', 'artifact.other-work.1945'):
            with self.subTest(parent=parent):
                artifact['derived_from'] = parent
                self.assertIn('registered Lasance1945', '\n'.join(self.publication()))
        artifact['derived_from'] = self.page
        self.records[self.page].data['sha256'] = '0' * 64
        self.assertIn('registered Lasance1945', '\n'.join(self.publication()))

    def test_all_existing_exact_payload_and_same_edition_checks_still_apply(self):
        artifact = self.records[self.fixture.publication_artifact_id].data
        for field, value, diagnostic in [
            ('rights_status', 'unresolved', 'public-domain rights_status'),
            ('rights_jurisdiction', 'elsewhere', 'United States rights jurisdiction'),
            ('storage', 'remote', 'must be tracked'),
        ]:
            with self.subTest(field=field):
                original = artifact[field]
                artifact[field] = value
                self.assertIn(diagnostic, '\n'.join(self.publication()))
                artifact[field] = original
        entry = copy.deepcopy(self.entry)
        entry['translations'][0]['text'] = 'A different or negative variant.'
        self.assertIn('does not exactly equal', '\n'.join(self.publication(entry)))
        entry = copy.deepcopy(self.entry)
        entry['publication_artifact_sha256'] = '0' * 64
        self.assertIn('does not match', '\n'.join(self.publication(entry)))
        entry = copy.deepcopy(self.entry)
        entry['publication_artifact_id'] = self.page
        self.assertIn('independent of the page-image proof', '\n'.join(self.publication(entry)))
        passage = self.records[self.fixture.publication_passage_id].data
        passage['edition_id'] = 'edition.other.1945'
        self.assertIn('same edition', '\n'.join(self.publication()))
        passage['edition_id'] = self.edition
        passage['physical_line_ranges'] = [[1, 1]]
        self.assertIn('exactly one TSV data line', '\n'.join(self.publication()))

    def test_lettered_insert_loci_and_unverified_page_proofs_remain_rejected(self):
        for page in ('1298a', '1298n', '1302a', '1302d'):
            with self.subTest(page=page):
                entry = copy.deepcopy(self.entry)
                entry['printed_page'] = page
                self.assertIn('requires printed_page', '\n'.join(self.source(entry)))
        self.records[self.fixture.page_passage_id].data['states'] = ['inspected']
        self.assertIn('dated verified passage', '\n'.join(self.source()))

    def test_registered_metadata_matches_only_the_existing_approved_owner(self):
        owner = ROOT / 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945'
        artifact = tomllib.loads((owner / 'artifacts/new-roman-missal-text-80b34759/artifact.toml').read_text())
        edition = tomllib.loads((owner / 'edition.toml').read_text())
        page = tomllib.loads((owner / 'artifacts/internet-archive-facsimile-pdf-6cf3c3d0/artifact.toml').read_text())
        rights = tomllib.loads((ROOT / 'src/sources/inventories/lasance-new-roman-missal-rights-v1.toml').read_text())
        self.assertEqual((artifact['id'], artifact['sha256'], artifact['edition_id']),
                         (self.rights, self.checker.LASANCE_1945_RIGHTS_SHA256, self.edition))
        self.assertEqual((artifact['rights_status'], artifact['rights_jurisdiction'], artifact['storage']),
                         ('public-domain', 'United States', 'tracked'))
        self.assertEqual((edition['id'], edition['date']), (self.edition, '1945'))
        self.assertEqual((page['id'], page['sha256'], page['rights_status']),
                         (self.page, self.checker.LASANCE_1945_PAGE_SHA256, 'unresolved'))
        registration = next(r for r in rights['registrations'] if r['id'] == 'revised-edition-1945')
        self.assertEqual(registration['regnum'], 'A 192159')
        self.assertIs(registration['renewal_found'], False)


if __name__ == '__main__':
    unittest.main()
