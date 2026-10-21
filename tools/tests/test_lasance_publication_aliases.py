"""Use the real consumer source-id/artifact-id alias shape, without local ids."""
from __future__ import annotations

import copy
import unittest

from tools.tests import test_lasance_publication_consumer as consumer_tests


class LasancePublicationAliasTests(unittest.TestCase):
    def setUp(self):
        self.fixture = consumer_tests.LasancePublicationConsumerTests(
            'test_exact_pdf_derived_lasance_body_reaches_the_cli_contract')
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        row = dict(id='lasance-1945', **self.fixture.fixture.witnesses['lasance-1945'])
        # This is translation_overlay's actual shape: it records local_id in
        # a separate set and exposes only source_id/artifact_id map aliases.
        self.aliases = {row[field]: row for field in ('source_id', 'artifact_id')}
        self.assertNotIn('lasance-1945', self.aliases)

    def test_actual_alias_shape_reaches_consumer_without_a_local_id_key(self):
        self.fixture.validate(witnesses=self.aliases)

    def test_alias_presence_cannot_replace_exact_named_source_identity(self):
        edition = self.fixture.fixture.edition
        for field, value in [('id', 'another-lasance-book'),
                             ('source_id', 'edition.other.1945'),
                             ('artifact_id', self.fixture.fixture.page),
                             ('rights', 'permission')]:
            with self.subTest(field=field):
                aliases = copy.deepcopy(self.aliases)
                aliases[edition][field] = value
                with self.assertRaisesRegex(ValueError, 'registered Lasance1945'):
                    self.fixture.validate(witnesses=aliases)


if __name__ == '__main__':
    unittest.main()
