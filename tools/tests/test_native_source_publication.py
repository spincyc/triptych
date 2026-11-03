"""The publisher admits only exact, owned shared-source transport bytes."""
import copy
import gzip
import unittest
from unittest.mock import patch

from . import test_native_tex_publication as publication_fixture
from . import test_native_print_bundles as source_fixture
import _native_print_bundles as bundles
import _native_tex_publication as publication


class NativeSourcePublicationTests(unittest.TestCase):
    def setUp(self):
        self.source = source_fixture.NativeSourceBundleTests()
        self.source.setUp()
        self.addCleanup(self.source.doCleanups)
        self.publisher = publication_fixture.NativeTeXPublicationTest()
        with patch('tools.tests.test_native_tex_publication.SCRATCH', self.source.root / '.scratch/publication'):
            self.publisher.setUp()
        self.addCleanup(self.publisher.doCleanups)
        style = self.source.root / 'src/common/preamble.tex'
        style.write_bytes(style.read_bytes() * 100)
        original = self.source.prepare()
        self.assets = {}
        self.bundle = bundles._externalize(original, self.assets,
            shared_text={row['sha256'] for row in original['files']})

    def build(self, bundle=None, assets=None):
        bundle = self.bundle if bundle is None else bundle
        assets = dict(self.assets if assets is None else assets)
        bundle = copy.deepcopy(bundle)
        bundle.pop('content_sha256', None)
        bundle['content_sha256'] = bundles._sha(bundles.canonical(bundle))
        body = bundles.canonical(bundle) + b'\n'
        route = 'native-tex/sources/' + bundle['content_sha256'] + '.json'
        assets[route] = body
        catalog = {'schema': bundles.CATALOG_SCHEMA, 'source_revision': self.source.revision,
                   'bundles': {self.source.identity: {'route': route, 'sha256': bundles._sha(body), 'bytes': len(body)}},
                   'assets': assets, 'source_paths': ['src/gpt/work/main.tex']}
        return self.publisher.build(documents=self.source.documents, source_catalog=catalog)

    def test_exact_source_packs_and_raw_fallback_objects_are_published(self):
        result = self.build()
        for route, body in self.assets.items():
            self.assertEqual(result['assets'][route]['body'], body)
            self.assertEqual(result['assets'][route]['kind'], 'source-pack' if '/source-packs/' in route else 'source-text')
        self.assertFalse(any(route.endswith('.pdf') for route in result['assets']))
        self.assertEqual(set(result['selections']), {self.source.identity})

    def test_missing_unowned_and_modified_source_assets_refuse_publication(self):
        for mode in ('missing-pack', 'missing-raw', 'modified-pack', 'modified-raw', 'extra'):
            with self.subTest(mode=mode):
                assets = dict(self.assets)
                pack = next(route for route in assets if '/source-packs/' in route)
                raw = next(route for route in assets if '/assets/' in route)
                if mode == 'missing-pack': del assets[pack]
                if mode == 'missing-raw': del assets[raw]
                if mode == 'modified-pack': assets[pack] += b'x'
                if mode == 'modified-raw': assets[raw] += b'x'
                if mode == 'extra': assets['native-tex/source-packs/' + 'f' * 64 + '.bin'] = b'extra'
                with self.assertRaises(publication.NativeTeXPublicationError):
                    self.build(assets=assets)

    def test_self_consistent_outer_pin_cannot_hide_invalid_expansion_or_members(self):
        for mode in ('gzip', 'expansion', 'member'):
            with self.subTest(mode=mode):
                changed, assets = copy.deepcopy(self.bundle), dict(self.assets)
                pack = changed['sourcePacks'][0]
                old = 'native-tex/' + pack['href'][3:]
                payload = b'invalid gzip' if mode == 'gzip' else gzip.compress(
                    b'x' * (pack['expanded_bytes'] + (1 if mode == 'expansion' else 0)), mtime=0)
                pack.update(sha256=bundles._sha(payload), bytes=len(payload))
                pack['href'] = '../source-packs/' + pack['sha256'] + '.bin'
                del assets[old]
                assets['native-tex/' + pack['href'][3:]] = payload
                with self.assertRaises(publication.NativeTeXPublicationError):
                    self.build(bundle=changed, assets=assets)

    def test_duplicate_missing_unknown_and_overlapping_pack_inventory_is_rejected(self):
        for mutate in (lambda pack: pack['files'].append(dict(pack['files'][0])),
                       lambda pack: pack['files'].clear(),
                       lambda pack: pack['files'][0].update(sha256='f' * 64),
                       lambda pack: pack['files'][0].update(offset=1)):
            changed = copy.deepcopy(self.bundle)
            mutate(changed['sourcePacks'][0])
            with self.assertRaises(publication.NativeTeXPublicationError):
                self.build(bundle=changed)


if __name__ == '__main__':
    unittest.main()
