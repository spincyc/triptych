"""Thin-index correctness, incremental work and fail-closed reader regressions."""
from contextlib import contextmanager
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import _corpus_index as corpus
import _reader_index as readers


class CorpusIndexTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / '.scratch/corpus-index'
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git('init', '-q')
        self.work = 'src/sources/works/author/a-different-path/work.toml'
        self.payload = 'src/sources/works/author/a-different-path/editions/one/artifacts/text/body.txt'
        self.put(self.work, 'schema=1\nrecord_type="work"\nid="work.permanent-identity"\ntitle="Never duplicate this prose"\n')
        self.put(self.payload, 'Original whole source\n')
        self.put('src/sources/corpora/collection.toml', 'schema=1\nrecord_type="corpus"\nid="corpus.stable"\nmembers=[]\n')
        self.put('scripts/example.py', 'print("example")\n')
        self.put('.gitignore', '.scratch/\n')
        self.git('add', '.')
        self.git('-c', 'user.name=Index Test', '-c', 'user.email=index@example.invalid', 'commit', '-qm', 'fixture')
        corpus.refresh(self.root)

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args], check=True, capture_output=True).stdout

    def put(self, path, text):
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding='utf-8')

    def test_ids_come_from_records_and_prose_is_not_copied(self):
        index = corpus.CorpusIndex(self.root)
        self.assertEqual(index.record_path('work.permanent-identity'), self.work)
        self.assertEqual(index.record_id_for_path(self.work), 'work.permanent-identity')
        self.assertEqual(index.record_kind('corpus.stable'), 'corpus')
        self.assertEqual(index.records('corpus'), ('corpus.stable',))
        self.assertEqual(index.record('work.permanent-identity')['title'], 'Never duplicate this prose')
        self.assertEqual(index.read(self.payload), b'Original whole source\n')
        for file in (self.root / corpus.INDEX).rglob('*'):
            if file.is_file():
                self.assertNotIn(b'Never duplicate', file.read_bytes())
                self.assertNotIn(b'Original whole source', file.read_bytes())
        with self.assertRaises(KeyError):
            index.record('work.missing')

    def test_startup_does_not_read_clean_source_bodies(self):
        original = corpus._safe_read
        accessed = []
        def observe(root, relative, limit=None):
            accessed.append(relative)
            return original(root, relative, limit)
        with patch.object(corpus, '_safe_read', side_effect=observe):
            index = corpus.CorpusIndex(self.root)
        self.assertEqual(accessed, [corpus.INDEX + '/index.json'])
        with patch.object(Path, 'rglob', side_effect=AssertionError('walk')):
            self.assertEqual(index.paths(prefix='scripts/', suffix='.py'), ('scripts/example.py',))

    def test_membership_ignores_body_edits_but_binds_paths_ids_and_joins(self):
        before = corpus.CorpusIndex(self.root).membership_identity
        self.put(self.payload, 'Different length and content, same canonical path\n')
        corpus.refresh(self.root)
        self.assertEqual(corpus.CorpusIndex(self.root).membership_identity, before)
        self.put('src/added.txt', 'A new discovery candidate\n')
        corpus.refresh(self.root)
        added = corpus.CorpusIndex(self.root).membership_identity
        self.assertNotEqual(added, before)
        (self.root / 'src/added.txt').unlink()
        corpus.refresh(self.root)
        self.assertEqual(corpus.CorpusIndex(self.root).membership_identity, before)
        self.put(self.work, (self.root / self.work).read_text().replace('work.permanent-identity', 'work.changed-identity'))
        corpus.refresh(self.root)
        changed_id = corpus.CorpusIndex(self.root).membership_identity
        self.assertNotEqual(changed_id, before)
        edition = 'src/sources/works/author/a-different-path/editions/one/edition.toml'
        self.put(edition, 'schema=1\nrecord_type="edition"\nid="edition.stable"\nwork_id="work.changed-identity"\n')
        corpus.refresh(self.root)
        previous_join = corpus.CorpusIndex(self.root).membership_identity
        self.put(edition, (self.root / edition).read_text().replace('work.changed-identity', 'work.other-parent'))
        corpus.refresh(self.root)
        self.assertNotEqual(corpus.CorpusIndex(self.root).membership_identity, previous_join)

    def test_reader_cancellation_stops_before_any_canonical_open(self):
        index = corpus.CorpusIndex(self.root)
        index._reader_cancelled = threading.Event()
        index._reader_cancelled.set()
        with patch.object(corpus, '_safe_read', side_effect=AssertionError('opened after cancellation')):
            for operation in (lambda: index.read(self.payload), lambda: index.metadata(self.payload),
                              lambda: index.paths('src/'), lambda: index.record('work.permanent-identity')):
                with self.assertRaisesRegex(corpus.CorpusIndexError, '^reading was cancelled$'):
                    operation()

    def test_deterministic_refresh_and_independent_full_check(self):
        before = {p.relative_to(self.root / corpus.INDEX): p.read_bytes()
                  for p in (self.root / corpus.INDEX).rglob('*') if p.is_file()}
        report = corpus.refresh(self.root)
        self.assertEqual(report['parsed'], 0)
        self.assertEqual(report['hashed'], 0)
        self.assertEqual(report['reused'], 4)
        corpus.refresh(self.root, check=True)
        self.assertEqual(before, {p.relative_to(self.root / corpus.INDEX): p.read_bytes()
                                 for p in (self.root / corpus.INDEX).rglob('*') if p.is_file()})
        self.put(self.work, (self.root / self.work).read_text().replace('Never duplicate', 'Changed'))
        report = corpus.refresh(self.root)
        self.assertEqual(report['parsed'], 1)
        self.assertEqual(report['hashed'], 1)
        corpus.refresh(self.root, check=True)
        repeated = corpus.refresh(self.root)
        self.assertEqual(repeated['parsed'], 0)
        self.assertEqual(repeated['reused'], 4)

    def test_dirty_and_committed_change_add_delete_refuse_stale_index(self):
        for operation in ('edit', 'add', 'delete'):
            with self.subTest(operation=operation):
                if operation == 'edit':
                    self.put(self.payload, 'Changed whole source\n')
                elif operation == 'add':
                    self.put('src/new.txt', 'Added\n')
                else:
                    (self.root / self.payload).unlink()
                with self.assertRaisesRegex(corpus.CorpusIndexError, 'stale corpus index'):
                    corpus.CorpusIndex(self.root)
                self.git('add', 'src')
                with self.assertRaisesRegex(corpus.CorpusIndexError, 'stale corpus index'):
                    corpus.CorpusIndex(self.root)
                corpus.refresh(self.root)
                corpus.CorpusIndex(self.root)

    def test_each_read_checks_same_size_body_even_restored_mtime(self):
        index = corpus.CorpusIndex(self.root)
        path = self.root / self.payload
        prior = path.stat()
        data = path.read_bytes()
        path.write_bytes(b'X' + data[1:])
        os.utime(path, ns=(prior.st_atime_ns, prior.st_mtime_ns))
        with self.assertRaisesRegex(corpus.CorpusIndexError, 'stale corpus input'):
            index.read(self.payload)

    def test_symlink_escape_and_traversal_rejected(self):
        index = corpus.CorpusIndex(self.root)
        for path in ('../outside', '/etc/passwd', 'src/../other', 'src//other'):
            with self.assertRaises(corpus.CorpusIndexError):
                index.read(path)
        (self.root / self.payload).unlink()
        (self.root / self.payload).symlink_to('/etc/passwd')
        with self.assertRaisesRegex(corpus.CorpusIndexError, 'unsafe corpus input'):
            index.read(self.payload)

    def test_verified_opens_and_dependencies(self):
        index = corpus.CorpusIndex(self.root)
        self.put('unindexed.txt', 'not admitted')
        with index.verified_reads() as dependencies:
            self.assertEqual((self.root / self.payload).read_text(), 'Original whole source\n')
            with open(self.root / self.payload, 'rb') as handle:
                self.assertEqual(handle.read(8), b'Original')
        self.assertEqual(dependencies, {self.payload: corpus._sha(b'Original whole source\n')})
        with self.assertRaisesRegex(corpus.CorpusIndexError, 'unindexed'):
            with index.verified_reads():
                with self.assertRaisesRegex(corpus.CorpusIndexError, 'unindexed'):
                    (self.root / 'unindexed.txt').read_text()
        self.assertEqual((self.root / 'unindexed.txt').read_text(), 'not admitted')

    def test_nested_context_metadata_and_read_only_streams(self):
        index = corpus.CorpusIndex(self.root)
        with index.verified_reads() as outer:
            with index.verified_reads() as inner:
                self.assertIs(outer, inner)
                index.metadata(self.work)
                with open(self.root / self.payload, 'rb') as source:
                    self.assertFalse(source.writable())
                    with self.assertRaises(io.UnsupportedOperation):
                        source.write(b'bad')
        self.assertEqual(set(outer), {self.work, self.payload})
        with self.assertRaisesRegex(corpus.CorpusIndexError, 'read-only'):
            with index.verified_reads():
                open(self.root / self.payload, 'r+')

    def test_discovery_uses_index_including_missing_files(self):
        index = corpus.CorpusIndex(self.root)
        (self.root / self.payload).unlink()
        with self.assertRaisesRegex(corpus.CorpusIndexError, 'missing or unsafe'):
            with index.verified_reads():
                self.assertTrue((self.root / self.payload).exists())
                self.assertTrue((self.root / self.payload).is_file())
                self.assertTrue((self.root / self.payload).parent.is_dir())
                self.assertEqual(list((self.root / 'src/sources/works').glob('*/*/work.toml')),
                                 [self.root / self.work])
                self.assertEqual(list((self.root / 'src').rglob('body.txt')), [self.root / self.payload])
                (self.root / self.payload).read_bytes()
        self.assertFalse((self.root / self.payload).exists())

    def test_integrity_failure_cannot_be_swallowed_into_a_projection(self):
        index = corpus.CorpusIndex(self.root)
        self.put(self.payload, 'Changed under an active reader')
        with self.assertRaisesRegex(corpus.CorpusIndexError, 'stale corpus input'):
            with index.verified_reads():
                try:
                    index.read(self.payload)
                except ValueError:
                    pass  # Existing producers sometimes convert validation errors to data.

    def test_nested_integrity_poison_propagates_and_domain_errors_remain_normal(self):
        index = corpus.CorpusIndex(self.root)
        with index.verified_reads():
            try:
                raise ValueError('an ordinary domain refusal')
            except ValueError:
                pass
        with self.assertRaisesRegex(corpus.CorpusIndexError, 'unindexed'):
            with index.verified_reads():
                try:
                    with index.verified_reads():
                        try:
                            index.read('src/unindexed.txt')
                        except ValueError:
                            pass
                except ValueError:
                    pass

    def test_preexisting_shard_failure_is_poisoned_during_metadata_lookup(self):
        index = corpus.CorpusIndex(self.root)
        failure = corpus.CorpusIndexError('corrupt metadata')
        with self.assertRaisesRegex(corpus.CorpusIndexError, 'corrupt metadata'):
            with index.verified_reads():
                with patch.object(corpus, '_safe_read', side_effect=failure):
                    try:
                        index.metadata(self.payload)
                    except ValueError:
                        pass

    def test_corrupt_shard_and_duplicate_id_fail(self):
        index = corpus.CorpusIndex(self.root)
        shard = self.root / corpus.INDEX / corpus._path_shard(self.payload)
        shard.write_bytes(shard.read_bytes() + b'[]\n')
        with self.assertRaisesRegex(corpus.CorpusIndexError, 'corrupt'):
            index.read(self.payload)
        self.put('src/sources/works/author/second/work.toml', (self.root / self.work).read_text())
        with self.assertRaisesRegex(corpus.CorpusIndexError, 'duplicate'):
            corpus.refresh(self.root, full=True)

    def _surface(self, surface, root, index, *, check=False):
        prefix = readers.OUTPUTS[surface][0]
        return {prefix + '/fixture.json': json.dumps({
            'surface': surface, 'source': corpus._sha((root / self.work).read_bytes())
        }).encode()}

    def test_surface_maintenance_disables_stat_caches_and_restores_environment(self):
        def cold(surface, root, index, *, check=False):
            self.assertTrue(all(os.environ.get(key) == '0' for key in readers.COLD_CACHE_FLAGS))
            self.assertEqual(os.environ['TRIPTYCH_LIBRARY_CACHE_DIR'],
                             str(self.root / '.scratch/corpus-index/library'))
            return {'src/index/sources/fixture.json': b'{}'}
        with patch.dict(os.environ, {'TRIPTYCH_LIBRARY_CACHE': '1', 'TRIPTYCH_LIBRARY_CACHE_DIR': 'old-cache'}):
            with patch.object(readers, '_build_surface', side_effect=cold):
                readers.build_surface('sources', self.root, None, check=True)
            self.assertEqual(os.environ['TRIPTYCH_LIBRARY_CACHE'], '1')
            self.assertEqual(os.environ['TRIPTYCH_LIBRARY_CACHE_DIR'], 'old-cache')

    def test_reader_orchestration_skips_unchanged_and_full_check_replays(self):
        with patch.object(readers, 'build_surface', side_effect=self._surface) as builder:
            initial = corpus.refresh(self.root, readers=True)
            self.assertEqual(initial['reader_surfaces'], list(readers.ORDER))
            self.assertEqual(builder.call_count, len(readers.ORDER))
            index = corpus.CorpusIndex(self.root)
            with index.verified_reads() as dependencies:
                self.assertEqual(json.loads(index.read('src/index/commentary/fixture.json'))['surface'], 'commentary')
            self.assertEqual(set(dependencies), {'src/index/commentary/fixture.json'})
            builder.reset_mock()
            warm = corpus.refresh(self.root, readers=True)
            self.assertEqual(warm['reader_surfaces'], [])
            builder.assert_not_called()
            corpus.refresh(self.root, readers=True, check=True)
            self.assertEqual(builder.call_count, len(readers.ORDER))

    def test_generic_refresh_cannot_bless_stale_reader_derivation(self):
        with patch.object(readers, 'build_surface', side_effect=self._surface):
            corpus.refresh(self.root, readers=True)
            self.put(self.work, (self.root / self.work).read_text().replace('Never duplicate', 'Changed'))
            with self.assertRaisesRegex(corpus.CorpusIndexError, 'stale reader derivation'):
                corpus.refresh(self.root)
            corpus.refresh(self.root, readers=True)
            corpus.CorpusIndex(self.root).read('src/index/sources/fixture.json')
            self.put('src/index/sources/fixture.json', '{}')
            with self.assertRaisesRegex(corpus.CorpusIndexError, 'stale reader derivation'):
                corpus.refresh(self.root)

    def test_generic_refresh_refuses_removal_of_all_reader_metadata(self):
        with patch.object(readers, 'build_surface', side_effect=self._surface):
            corpus.refresh(self.root, readers=True)
        for surface in readers.ORDER:
            for file in (self.root / readers.OUTPUTS[surface][0]).rglob('*.json'):
                file.unlink()
        with self.assertRaisesRegex(corpus.CorpusIndexError, 'stale reader derivation'):
            corpus.refresh(self.root)

    def test_unread_guidance_edit_needs_no_reader_rebuild(self):
        with patch.object(readers, 'build_surface', side_effect=self._surface) as builder:
            corpus.refresh(self.root, readers=True)
            self.put('guidance/unread.md', 'Editorial clarification')
            builder.reset_mock()
            corpus.refresh(self.root)
            corpus.refresh(self.root, readers=True)
            builder.assert_not_called()

    def test_change_during_reader_generation_is_refused(self):
        count = 0
        def racing(surface, root, index, *, check=False):
            nonlocal count
            result = self._surface(surface, root, index, check=check)
            count += 1
            if count == 1:
                self.put(self.work, (self.root / self.work).read_text().replace('Never duplicate', 'Changed'))
            return result
        with patch.object(readers, 'build_surface', side_effect=racing):
            with self.assertRaisesRegex(corpus.CorpusIndexError, 'changed during reader derivation'):
                corpus.refresh(self.root, readers=True)


if __name__ == '__main__':
    unittest.main()
