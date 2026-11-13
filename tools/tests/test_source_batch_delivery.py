"""Source-batch guards require exact local bytes after binary delivery migration."""
import copy
import json
from pathlib import Path
import sys
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from tools.tests import _source_batch_guards as G
from tools.tests import test_source_batch_guards as baseline
import _artifact_store as store


class DeliveryGuardTests(unittest.TestCase):
    write = baseline.SourceBatchGuardTests.write
    save = baseline.SourceBatchGuardTests.save
    tearDown = baseline.SourceBatchGuardTests.tearDown
    def setUp(self):
        baseline.SourceBatchGuardTests.setUp(self)
        self.prefix = 'src/sources/works/francis-xavier-lasance/book/editions/1900-print/artifacts/scan/'
        self.payload = self.prefix + 'source.pdf'
        self.metadata = self.prefix + 'artifact.toml'
        self.body = b'%PDF-1.4\nexact evidence only\n'
        sha = G.digest(self.body)
        self.entry = {'path': self.payload, 'sha256': sha, 'bytes': len(self.body),
                      'kind': 'source-evidence', 'media_type': 'application/pdf',
                      'archive': 'a' * 64, 'member': self.payload}
        self.index = {'schema': store.SCHEMA, 'archives': [
            {'id': 'a' * 64, 'name': 'fixture.tar', 'sha256': 'a' * 64,
             'bytes': 10000, 'delivery': 'offline-only', 'urls': []}],
            'artifacts': [self.entry]}
        self.write(store.INDEX_PATH, json.dumps(self.index).encode())
        self.write(self.metadata, (
            'record_type = "artifact"\nstorage = "tracked"\n'
            'rights_status = "public-domain"\nrights_basis = "Synthetic old printing"\n'
            'rights_jurisdiction = "United States"\n'
            f'path = "{self.payload}"\nsha256 = "{sha}"\nbyte_size = {len(self.body)}\n'
            'media_type = "application/pdf"\nindexable = false\n').encode())
        self.cache = store.cache_path(self.root, self.entry)
        self.cache.parent.mkdir(parents=True)
        self.cache.write_bytes(self.body)
        self.pins = json.loads((self.root / self.manifest).read_bytes())
        self.pins += [{'path': self.payload, 'post_sha256': sha},
                      {'path': self.metadata, 'post_sha256': G.digest((self.root / self.metadata).read_bytes())},
                      {'path': store.INDEX_PATH, 'post_sha256': G.digest((self.root / store.INDEX_PATH).read_bytes())}]
        self.data['english_baseline_source_files'] = {self.payload: sha, self.metadata: G.digest((self.root / self.metadata).read_bytes())}
        self.data['english_historical_source_files'] = dict(self.data['english_baseline_source_files'])
        self.bind_pins()

    def bind_pins(self):
        raw = json.dumps(self.pins).encode()
        self.write(self.manifest, raw)
        self.data['source_input_manifest_sha256'] = G.digest(raw)
        receipt = json.dumps({'status': 'accepted', 'scope': 'missal-source-batch',
                              'source_input_manifest_sha256': G.digest(raw)}).encode()
        self.write(self.receipt, receipt)
        self.data['acceptance']['receipt_sha256'] = G.digest(receipt)
        self.save()

    def test_delivery_verified_cache_replays_namespace_without_fetch(self):
        with mock.patch.object(store, 'urlopen', side_effect=AssertionError('network forbidden')) as network:
            self.assertEqual(G.historical_english_source_files(), self.data['english_historical_source_files'])
            network.assert_not_called()
        self.assertFalse((self.root / self.payload).exists())

    def test_delivery_missing_or_corrupt_cache_refuses(self):
        self.cache.unlink()
        with self.assertRaisesRegex(AssertionError, 'accepted source input missing or invalid'):
            G.fixture()
        self.cache.write_bytes(self.body + b'changed')
        with self.assertRaisesRegex(AssertionError, 'accepted source input missing or invalid'):
            G.fixture()

    def test_delivery_changed_index_refuses_warm_and_cold(self):
        G.historical_english_source_files()
        self.write(store.INDEX_PATH, json.dumps(self.index).encode() + b' ')
        with self.assertRaisesRegex(AssertionError, 'exact accepted external delivery index bytes'):
            G.historical_english_source_files()
        G.fixture.cache_clear()
        with self.assertRaisesRegex(AssertionError, 'exact accepted external delivery index bytes'):
            G.fixture()

    def test_delivery_matching_metadata_cannot_replace_missing_bytes(self):
        self.cache.unlink()
        with mock.patch.object(store, 'resolve', wraps=store.resolve) as resolve:
            with self.assertRaises(AssertionError):
                G.fixture()
            resolve.assert_called_once_with(self.root, self.payload, fetch=False)

    def test_delivery_wrong_owner_rights_refuses(self):
        self.write(self.metadata, (self.root / self.metadata).read_bytes().replace(b'public-domain', b'restricted'))
        for row in self.pins:
            if row['path'] == self.metadata:
                row['post_sha256'] = G.digest((self.root / self.metadata).read_bytes())
        self.bind_pins()
        with self.assertRaisesRegex(AssertionError, 'accepted source input missing or invalid'):
            G.fixture()

    def test_delivery_extra_external_namespace_path_refuses(self):
        G.historical_english_source_files()
        other = copy.deepcopy(self.entry)
        other['path'] = other['member'] = self.prefix + 'unlisted.pdf'
        self.index['artifacts'].append(other)
        self.write(store.INDEX_PATH, json.dumps(self.index).encode())
        for row in self.pins:
            if row['path'] == store.INDEX_PATH:
                row['post_sha256'] = G.digest((self.root / store.INDEX_PATH).read_bytes())
        self.bind_pins()
        with self.assertRaisesRegex(AssertionError, 'external source input must belong'):
            G.historical_english_source_files()


if __name__ == "__main__":
    unittest.main()
