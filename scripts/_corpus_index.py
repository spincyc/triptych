"""Thin canonical addresses, hashes and source-record identities; never prose.

Startup compares Git index metadata plus dirty files, without historical blob
reads or whole-corpus hashing. Every consumed body is SHA-256 checked. Full
``check`` independently hashes all files. Membership is a reader-session
snapshot: reopen after adding/removing files. Refresh parses only changed
manifests. Source approval and publication gates remain independent.
"""
from __future__ import annotations

import argparse
import builtins
import copy
import fcntl
from fnmatch import fnmatchcase
from functools import wraps
from contextlib import contextmanager
from contextvars import ContextVar
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import threading
import tomllib

INDEX = 'src/index/corpus'
SCHEMA = 'triptych-corpus-index/v1'
ROOT_LIMIT = 512 * 1024
SHARD_LIMIT = 4 * 1024 * 1024
TOTAL_LIMIT = 64 * 1024 * 1024
KINDS = frozenset(('work', 'edition', 'artifact', 'segment', 'passage', 'corpus'))
SCOPES = ('src', 'scripts', 'tools', 'guidance', 'release', 'web', 'library',
          'workflows/fragments', 'workflows/pipelines', 'workflows/schema')
EXTRA_INPUTS = ('LICENSE', 'THIRD_PARTY.md')
# Reviewed authority records the proper text pipeline reads by fixed path.
# Mirrors the authority lists in _browser_product_recipes (2026-11-13).
AUTHORITIES = (
    'workflows/reviews/missal-english-completion-2026-10-29/roman-1962/finite-latin-authority-v2.json',
    'workflows/reviews/missal-english-completion-2026-11-12/postconciliar/lent-two-orations/actor-authority-v1.json',
    'workflows/reviews/missal-reader-completion-2026-10-26/gregem-damasus-qualified-rights-adoption.json',
    'workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/authority-v2.json',
    'workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/authority-v4.json',
    'workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/next-cohort/1946-formula-metadata-successor-review.json',
    'workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/next-cohort/data-source-review.json',
    'workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/next-cohort/final-authority-successor-delta.json',
    'workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/next-cohort/osp-source-frame-rebindings.json',
    'workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/next-cohort/osp-source-review.json',
    'workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/next-cohort/osp-spirit-metadata-review.json',
    'workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/next-cohort/osp-spirit-source-hooks.json',
    'workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/next-cohort/same-witness-formula-derivations.json',
    'workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/next-cohort/same-witness-formula-review.json',
    'workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/next-cohort/translation-binding-locator-successor-review.json',
    'workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/pius-secret/independent-family-review.json',
    'workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/pius-secret/source-family-proposal.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/ferial-three/evidence/recipient-carrier-english-amendment.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/ferial-three/evidence/recipient-carrier-source-amendment.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/latin-two-holy-name/activation-plan.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/latin-two-holy-name/holy-name-locator-declaration.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/latin-two-holy-name/independent-case-1.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/latin-two-holy-name/independent-case-2.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/latin-two-holy-name/independent-case-3.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/latin-two-holy-name/independent-selected-review.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/latin-two-holy-name/latin-correction-declarations.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/latin-two-holy-name/root-admission.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/latin-two-holy-name/source-metadata-successor.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/oration-endings/study-conclusions/modern-legacy-26-review.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/oration-endings/study-conclusions/roman-study-3-review.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/pius-secret/expression-merits-admission.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/pius-secret/finite-latin-authority-v6.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/pius-secret/selected-source-comparison.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/pius-secret/source-and-english-review.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/postconciliar-six/finite-latin-authority.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/postconciliar-six/root-code-adoption.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/postconciliar-ten/body-merits-adoption.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/postconciliar-ten/code-runtime-adoption.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/postconciliar-ten/finite-latin-authority.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/postconciliar-ten/source-contract-adoption.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/roman-six/finite-latin-authority-v4.json',
    'workflows/reviews/missal-reader-resume-2026-11-12/roman-six/source-and-english-review.json',
    'workflows/reviews/modern-source-completion-2026-11-13/ordinary-time-six/independent-latin-review.json',
    'workflows/reviews/modern-source-completion-2026-11-13/ordinary-time-six/root-source-admission.json',
    'workflows/reviews/reader-completion-2026-10-26/finite-name-two-authority.json',
    'workflows/reviews/reader-completion-2026-10-26/finite-name-two-root-adoption.json',
    'workflows/reviews/reader-completion-2026-10-26/oration-execution-six-authority.json',
)
_SOURCE_PATH = re.compile(
    r'src/sources/(?:works/[^/]+/[^/]+/(?:work\.toml|editions/[^/]+/'
    r'(?:edition\.toml|artifacts/[^/]+/artifact\.toml|(?:segments|passages)/[^/]+\.toml))'
    r'|corpora/[^/]+\.toml)\Z')
_ACTIVE: ContextVar[tuple | None] = ContextVar('corpus_verified_reads', default=None)
_DERIVATIONS: ContextVar[dict | None] = ContextVar('corpus_session_derivations', default=None)
_OPEN, _IO_OPEN = builtins.open, io.open
_PATH_METHODS = {name: getattr(Path, name) for name in ('glob', 'rglob', 'exists', 'is_file', 'is_dir')}
_PATCH_LOCK = threading.RLock()
_PATCH_USERS = 0


def _poison(error):
    active = _ACTIVE.get()
    if active is not None and all(previous is not error for previous in active[2]):
        active[2].append(error)


class CorpusIndexError(ValueError):
    """Missing, unsafe, malformed or stale index/input."""

    def __init__(self, *arguments):
        super().__init__(*arguments)
        _poison(self)


def _integrity_operation(function):
    @wraps(function)
    def guarded(*arguments, **keywords):
        try:
            return function(*arguments, **keywords)
        except CorpusIndexError as error:
            _poison(error)
            raise
    return guarded


def _json(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode()


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _relative(value):
    if not isinstance(value, str) or not value or '\\' in value or '\0' in value:
        raise CorpusIndexError(f'unsafe corpus path: {value!r}')
    if PurePosixPath(value).is_absolute() or any(p in ('', '.', '..') for p in value.split('/')):
        raise CorpusIndexError(f'unsafe corpus path: {value!r}')
    return value


def _covered(path):
    if path == INDEX or path.startswith(INDEX + '/') or path == 'release/browser-products.json':
        return False
    if path.startswith('tools/tests/') or path.endswith('.pyc') or '/__pycache__/' in path:
        return False
    return (any(path == p or path.startswith(p + '/') for p in SCOPES)
            or path in AUTHORITIES or path in EXTRA_INPUTS or ('/' not in path and (
                path.startswith('requirements') and path.endswith('.txt')
                or path.endswith(('.lock', '-lock.json')))))


def _group(path):
    parts = path.split('/')
    if path.startswith('src/sources/works/'):
        return '/'.join(parts[:4])
    if path.startswith('src/') and len(parts) > 3:
        return '/'.join(parts[:3])
    return parts[0] if len(parts) > 1 else '@root'


def _path_shard(path):
    return 'paths/' + _sha(_group(path).encode())[:20] + '-' + str(int(_sha(path.encode())[0], 16) % 4) + '.jsonl'


def _id_shard(identifier):
    return 'records/' + _sha(identifier.encode())[:2] + '.jsonl'


def _safe_read(root, relative, limit=None):
    """O_NOFOLLOW at every component, including final regular-file check."""
    parts = _relative(relative).split('/')
    directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            os.close(directory)
            directory = child
        descriptor = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        with _IO_OPEN(descriptor, 'rb', closefd=True) as source:
            before = os.fstat(source.fileno())
            if not stat.S_ISREG(before.st_mode):
                raise CorpusIndexError(f'corpus input is not a regular file: {relative}')
            if limit is not None and before.st_size > limit:
                raise CorpusIndexError(f'corpus metadata exceeds size budget: {relative}')
            result = source.read() if limit is None else source.read(limit + 1)
            after = os.fstat(source.fileno())
            if (before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
                    after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                raise CorpusIndexError(f'corpus input changed while reading: {relative}')
            if limit is not None and len(result) > limit:
                raise CorpusIndexError(f'corpus metadata exceeds size budget: {relative}')
            return result, '100755' if before.st_mode & stat.S_IXUSR else '100644'
    except OSError as error:
        raise CorpusIndexError(f'missing or unsafe corpus input {relative}: {error.strerror}') from error
    finally:
        os.close(directory)


def _git(root, *arguments):
    env = {**os.environ, 'GIT_OPTIONAL_LOCKS': '0', 'GIT_NO_LAZY_FETCH': '1'}
    result = subprocess.run(['git', '-C', str(root), *arguments], capture_output=True, env=env)
    if result.returncode:
        raise CorpusIndexError('corpus index requires a Git checkout: ' + result.stderr.decode(errors='replace').strip())
    return result.stdout


def _git_state(root):
    entries = {}
    for item in _git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not item:
            continue
        header, raw_path = item.split(b'\t', 1)
        path = raw_path.decode('utf-8')
        if not _covered(path):
            continue
        _relative(path)
        mode, oid, stage = header.decode().split()
        if stage != '0' or mode not in ('100644', '100755'):
            raise CorpusIndexError(f'unmerged or non-regular corpus input: {path}')
        entries[path] = (mode, oid)
    dirty = {_relative(item.decode('utf-8')) for item in _git(
        root, 'ls-files', '--modified', '--deleted', '--others', '--exclude-standard', '-z'
    ).split(b'\0') if item and _covered(item.decode('utf-8'))}
    return entries, dirty


def _blob(data, oid_length=40):
    algorithm = hashlib.sha256 if oid_length == 64 else hashlib.sha1
    return algorithm(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def _binding(entries):
    digest = hashlib.sha256()
    for path, (mode, oid) in sorted(entries.items()):
        digest.update(f'{mode} {oid}\t{path}\0'.encode())
    return digest.hexdigest()


def _membership(paths, records):
    """Discovery identity: paths and source graph joins, excluding body hashes."""
    digest = hashlib.sha256(b'triptych-corpus-membership/v1\0')
    for path in sorted(paths):
        digest.update(_json(['path', path]))
    for identifier, record in sorted(records.items()):
        digest.update(_json(['record', *record]))
    return digest.hexdigest()


def _current_state(root):
    entries, dirty = _git_state(root)
    changed = {}
    oid_length = len(next(iter(entries.values()))[1]) if entries else 40
    for path in sorted(dirty):
        try:
            data, mode = _safe_read(root, path)
        except CorpusIndexError:
            if path in entries and not os.path.lexists(root / path):
                entries.pop(path)
                continue
            raise
        entries[path] = (mode, _blob(data, oid_length))
        changed[path] = data
    return entries, changed


def _dependencies(data):
    result = []
    for name in ('work_id', 'edition_id', 'artifact_id', 'segment_id', 'derived_from'):
        if isinstance(data.get(name), str):
            result.append(data[name])
    for name in ('members', 'projected_from'):
        if isinstance(data.get(name), list):
            result.extend(item for item in data[name] if isinstance(item, str))
    for support in data.get('support_artifacts', []):
        if isinstance(support, dict) and isinstance(support.get('artifact_id'), str):
            result.append(support['artifact_id'])
    return sorted(set(result))


class CorpusIndex:
    """One checked membership snapshot; bodies are verified on each access."""

    def __init__(self, root, *, _bind=True, _snapshot=None):
        self.root = Path(root).absolute()
        self._snapshot = _snapshot
        raw = _snapshot['index.json'] if _snapshot is not None else _safe_read(self.root, INDEX + '/index.json', ROOT_LIMIT)[0]
        try:
            self.manifest = json.loads(raw)
        except (ValueError, UnicodeError) as error:
            raise CorpusIndexError('invalid corpus index root; run tools/corpus-index refresh') from error
        m = self.manifest
        if (not isinstance(m, dict) or m.get('schema') != SCHEMA
                or m.get('scopes') != list(SCOPES) or m.get('authorities') != list(AUTHORITIES)
                or not isinstance(m.get('shards'), dict) or not isinstance(m.get('groups'), dict)):
            raise CorpusIndexError('invalid corpus index contract; run tools/corpus-index refresh')
        self.identity = _sha(raw)
        self._path_cache, self._record_cache = {}, {}
        self._groups = m['groups']
        self._checked_readers = set()
        if _bind:
            current, _ = _current_state(self.root)
            if _binding(current) != m.get('binding'):
                raise CorpusIndexError('stale corpus index; run tools/corpus-index refresh')

    @property
    def membership_identity(self):
        """Invalidate discovery-dependent caches on paths, IDs or changed joins.

        This deliberately excludes content hashes and sizes: an unrelated body
        edit does not discard a selected payload whose own read hashes match.
        """
        value = self.manifest.get('membership')
        if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{64}', value):
            raise CorpusIndexError('corpus membership identity is missing; run tools/corpus-index refresh')
        return value

    def _check_cancelled(self):
        event = getattr(self, '_reader_cancelled', None)
        if event is not None and event.is_set():
            raise CorpusIndexError('reading was cancelled')

    @_integrity_operation
    def _shard(self, name, record=False):
        self._check_cancelled()
        cache = self._record_cache if record else self._path_cache
        if name in cache:
            return cache[name]
        descriptor = self.manifest['shards'].get(name)
        if descriptor is None:
            return {}
        data = (self._snapshot[name] if self._snapshot is not None
                else _safe_read(self.root, INDEX + '/' + _relative(name), SHARD_LIMIT)[0])
        if len(data) != descriptor[1] or _sha(data) != descriptor[0]:
            raise CorpusIndexError(f'corrupt corpus index shard: {name}')
        try:
            rows = [json.loads(line) for line in data.splitlines()]
            result = {row[0]: row for row in rows}
            if len(result) != len(rows) or any(not isinstance(row, list) or len(row) != (4 if record else 5) for row in rows):
                raise ValueError('invalid rows')
        except (ValueError, TypeError, IndexError, UnicodeError) as error:
            raise CorpusIndexError(f'invalid corpus index shard: {name}') from error
        cache[name] = result
        return result

    def _file_row(self, relative):
        relative = _relative(os.fspath(relative))
        return self._shard(_path_shard(relative))[relative]

    @_integrity_operation
    def metadata(self, relative):
        """Return (SHA-256, size) without reading the body."""
        self._check_cancelled()
        row = self._file_row(relative)
        active = _ACTIVE.get()
        if active is not None and active[0] is self:
            active[1][relative] = row[1]
        return row[1], row[2]

    @_integrity_operation
    def read(self, relative):
        self._check_cancelled()
        relative = _relative(os.fspath(relative))
        if relative.startswith('src/index/') and self._snapshot is None:
            from _reader_index import PROOF, surface_for
            surface = surface_for(relative)
            if surface is not None and surface not in self._checked_readers:
                # This is a freshness guard, not a rendered payload input. A
                # fresh proof can change while selected metadata bytes remain
                # identical. Validate it on access without making every cache
                # depend on one shared receipt for all reader families.
                try:
                    proof_row = self._file_row(PROOF)
                except KeyError as error:
                    raise CorpusIndexError('reader derivation proof is missing; run tools/corpus-index refresh --readers') from error
                proof_bytes, _ = _safe_read(self.root, PROOF, 16 * 1024)
                if len(proof_bytes) != proof_row[2] or _sha(proof_bytes) != proof_row[1]:
                    raise CorpusIndexError('stale reader derivation proof; run tools/corpus-index refresh --readers')
                try:
                    proof = json.loads(proof_bytes)
                    expected = self.manifest.get('readers', {}).get(surface)
                    if (not isinstance(proof, dict) or expected is None
                            or not isinstance(proof.get('surfaces'), dict)
                            or proof['surfaces'].get(surface) != expected):
                        raise ValueError('mismatched derivation')
                except (ValueError, KeyError, TypeError) as error:
                    raise CorpusIndexError('stale reader discovery; run tools/corpus-index refresh --readers') from error
                self._checked_readers.add(surface)
        try:
            row = self._file_row(relative)
        except KeyError as error:
            raise CorpusIndexError(f'unindexed canonical input: {relative}') from error
        data, _ = _safe_read(self.root, relative)
        if len(data) != row[2] or _sha(data) != row[1]:
            raise CorpusIndexError(f'stale corpus input: {relative}; run tools/corpus-index refresh')
        active = _ACTIVE.get()
        if active is not None and active[0] is self:
            active[1][relative] = row[1]
        return data

    @_integrity_operation
    def paths(self, prefix='', suffix=None):
        self._check_cancelled()
        if prefix:
            _relative(prefix.rstrip('/'))
        selected = []
        for group, names in self._groups.items():
            if prefix and group != '@root' and not (prefix.startswith(group + '/') or group.startswith(prefix) or prefix == group):
                continue
            for name in names:
                selected.extend(path for path in self._shard(name)
                                if path.startswith(prefix) and (suffix is None or path.endswith(suffix)))
        return tuple(sorted(selected))

    def _record_row(self, identifier):
        return self._shard(_id_shard(identifier), record=True)[identifier]

    def record_path(self, identifier):
        return self._record_row(identifier)[2]

    def record_kind(self, identifier):
        return self._record_row(identifier)[1]

    def record_dependencies(self, identifier):
        return tuple(self._record_row(identifier)[3])

    @_integrity_operation
    def record_id_for_path(self, relative):
        self._file_row(relative)
        if not _SOURCE_PATH.fullmatch(relative):
            raise KeyError(relative)
        value = tomllib.loads(self.read(relative).decode('utf-8'))
        identifier = value.get('id')
        if not isinstance(identifier, str) or self.record_path(identifier) != relative:
            raise CorpusIndexError(f'source record identity differs from index: {relative}')
        return identifier

    @_integrity_operation
    def record(self, identifier):
        row = self._record_row(identifier)
        source = self.read(row[2])
        try:
            value = tomllib.loads(source.decode('utf-8'))
        except (ValueError, UnicodeError) as error:
            raise CorpusIndexError(f'invalid source record: {row[2]}') from error
        if value.get('id') != identifier or value.get('record_type') != row[1]:
            raise CorpusIndexError(f'source record identity differs from index: {row[2]}')
        return value

    def records(self, kind=None):
        return tuple(sorted(identifier for name in self.manifest['shards'] if name.startswith('records/')
                            for identifier, row in self._shard(name, record=True).items()
                            if kind is None or row[1] == kind))

    @contextmanager
    def verified_reads(self):
        """Yield path→SHA-256 dependencies; verify each canonical open in context.

        ContextVar isolates callers/threads; scratch and installed libraries use
        ordinary I/O. Unindexed repository inputs fail explicitly.
        """
        global _PATCH_USERS
        outer = _ACTIVE.get()
        dependencies = outer[1] if outer is not None and outer[0] is self else {}
        failures = outer[2] if outer is not None and outer[0] is self else []
        token = _ACTIVE.set((self, dependencies, failures))
        with _PATCH_LOCK:
            if _PATCH_USERS == 0:
                builtins.open, io.open = _verified_open, _verified_io_open
                for name, method in _INDEXED_PATH_METHODS.items():
                    setattr(Path, name, method)
            _PATCH_USERS += 1
        try:
            yield dependencies
        finally:
            _ACTIVE.reset(token)
            with _PATCH_LOCK:
                _PATCH_USERS -= 1
                if _PATCH_USERS == 0:
                    builtins.open, io.open = _OPEN, _IO_OPEN
                    for name, method in _PATH_METHODS.items():
                        setattr(Path, name, method)
            if failures:
                _poison(failures[0])
                raise failures[0]


@contextmanager
def session_derivations(cache):
    """Let ``session_derived`` reuse whole derivations within one reader session.

    The caller owns *cache* for one ``CorpusIndex`` lifetime. Maintenance,
    checks and publication builds never enter this context, so each of their
    derivations runs exactly as written.
    """
    token = _DERIVATIONS.set(cache)
    try:
        yield
    finally:
        _DERIVATIONS.reset(token)


def session_derived(key, compute):
    """Return ``compute()``, reusing an identical earlier derivation in session.

    *key* names the derivation and every argument it depends on other than
    verified canonical reads. A selected reader projection can need the same
    calendar-wide derivation for every Mass it opens: reuse is limited to
    that within one ``session_derivations`` and ``verified_reads`` context.
    Reuse re-reads and verifies every canonical input the first computation
    consumed and records each as the caller's own dependency, as the
    computation would have. A computation that failed or poisoned the session
    is not kept, and callers receive independent objects.
    """
    cache, active = _DERIVATIONS.get(), _ACTIVE.get()
    if cache is None or active is None:
        return compute()
    index, dependencies, failures = active
    held = cache.get(key)
    if held is not None:
        value, inputs = held
        for relative in inputs:
            index.read(relative)
        return copy.deepcopy(value)
    consumed, poisoned = {}, len(failures)
    token = _ACTIVE.set((index, consumed, failures))
    try:
        value = compute()
    finally:
        _ACTIVE.reset(token)
        dependencies.update(consumed)
    if len(failures) == poisoned:
        cache[key] = (copy.deepcopy(value), tuple(consumed))
    return value


class _ReadOnlyBytes(io.BytesIO):
    def writable(self):
        return False

    def write(self, value):
        raise io.UnsupportedOperation('verified canonical input is read-only')

    def writelines(self, value):
        raise io.UnsupportedOperation('verified canonical input is read-only')

    def truncate(self, size=None):
        raise io.UnsupportedOperation('verified canonical input is read-only')

    def getbuffer(self):
        return super().getbuffer().toreadonly()


def _open_verified(original, file, mode='r', buffering=-1, encoding=None, errors=None,
                   newline=None, closefd=True, opener=None):
    active = _ACTIVE.get()
    if active is None or isinstance(file, int):
        return original(file, mode, buffering, encoding, errors, newline, closefd, opener)
    index = active[0]
    absolute = Path(os.path.abspath(os.fsdecode(file)))
    try:
        relative = absolute.relative_to(index.root).as_posix()
    except ValueError:
        return original(file, mode, buffering, encoding, errors, newline, closefd, opener)
    if relative.split('/', 1)[0] in ('.scratch', '.git', 'build'):
        return original(file, mode, buffering, encoding, errors, newline, closefd, opener)
    if any(flag in mode for flag in 'wax+'):
        raise CorpusIndexError(f'canonical inputs are read-only during projection: {relative}')
    if opener is not None or not closefd:
        raise CorpusIndexError(f'unsupported canonical input open: {relative}')
    stream = _ReadOnlyBytes(index.read(relative))
    stream.name = str(file)
    if 'b' in mode:
        return stream
    return io.TextIOWrapper(stream, encoding=encoding or 'utf-8', errors=errors, newline=newline)


def _verified_open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    return _open_verified(_OPEN, file, mode, buffering, encoding, errors, newline, closefd, opener)


def _verified_io_open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    return _open_verified(_IO_OPEN, file, mode, buffering, encoding, errors, newline, closefd, opener)


def _indexed_relative(path):
    active = _ACTIVE.get()
    if active is None:
        return None
    index = active[0]
    try:
        relative = Path(os.path.abspath(path)).relative_to(index.root).as_posix()
    except ValueError:
        return None
    if relative == '.':
        return index, ''
    if relative.split('/', 1)[0] in ('.scratch', '.git', 'build'):
        return None
    return index, relative


def _indexed_exists(path, **kwargs):
    selected = _indexed_relative(path)
    if selected is None:
        return _PATH_METHODS['exists'](path, **kwargs)
    return _indexed_is_file(path, **kwargs) or _indexed_is_dir(path, **kwargs)


def _indexed_is_file(path, **kwargs):
    selected = _indexed_relative(path)
    if selected is None:
        return _PATH_METHODS['is_file'](path, **kwargs)
    index, relative = selected
    if not relative:
        return False
    try:
        index._file_row(relative)
        return True
    except KeyError:
        return False


def _indexed_is_dir(path, **kwargs):
    selected = _indexed_relative(path)
    if selected is None:
        return _PATH_METHODS['is_dir'](path, **kwargs)
    index, relative = selected
    return not relative or bool(index.paths(prefix=relative + '/'))


def _matches(parts, pattern):
    if not pattern:
        return not parts
    if pattern[0] == '**':
        return _matches(parts, pattern[1:]) or bool(parts) and _matches(parts[1:], pattern)
    return bool(parts) and fnmatchcase(parts[0], pattern[0]) and _matches(parts[1:], pattern[1:])


def _indexed_glob(path, pattern, **kwargs):
    selected = _indexed_relative(path)
    if selected is None:
        yield from _PATH_METHODS['glob'](path, pattern, **kwargs)
        return
    index, relative = selected
    pattern = os.fspath(pattern)
    if not pattern or pattern.startswith('/') or '..' in pattern.split('/'):
        raise CorpusIndexError(f'unsupported indexed glob: {pattern!r}')
    if kwargs.get('case_sensitive') is False or kwargs.get('recurse_symlinks'):
        raise CorpusIndexError('indexed discovery is case-sensitive and refuses symlinks')
    prefix = relative + '/' if relative else ''
    candidates = set()
    directories = set()
    for item in index.paths(prefix=prefix):
        tail = item[len(prefix):]
        candidates.add(tail)
        parts = tail.split('/')
        directories.update('/'.join(parts[:end]) for end in range(1, len(parts)))
    candidates.update(directories)
    directory_only = pattern.endswith('/')
    pattern_parts = pattern.rstrip('/').split('/')
    for item in sorted(candidates):
        if (not directory_only or item in directories) and _matches(item.split('/'), pattern_parts):
            yield index.root / prefix / item


def _indexed_rglob(path, pattern, **kwargs):
    if _indexed_relative(path) is None:
        yield from _PATH_METHODS['rglob'](path, pattern, **kwargs)
    else:
        yield from _indexed_glob(path, '**/' + os.fspath(pattern), **kwargs)


_INDEXED_PATH_METHODS = {'glob': _indexed_glob, 'rglob': _indexed_rglob,
                         'exists': _indexed_exists, 'is_file': _indexed_is_file, 'is_dir': _indexed_is_dir}


def _generate(root, *, full=False, validate_readers=True):
    entries, changed = _current_state(root)
    prior = None
    if not full and (root / INDEX / 'index.json').exists():
        prior = CorpusIndex(root, _bind=False)
    shards, groups, records, file_rows = {}, {}, {}, {}
    hashed = parsed = reused = 0
    oid_length = len(next(iter(entries.values()))[1]) if entries else 40
    for path, (mode, oid) in sorted(entries.items()):
        previous = None
        if prior is not None:
            try:
                previous = prior._file_row(path)
            except KeyError:
                pass
        if (previous is not None and previous[3:] == [mode, oid]
                and (path not in changed or _sha(changed[path]) == previous[1])):
            row = previous
            reused += 1
        else:
            data = changed.get(path)
            if data is None:
                data, mode = _safe_read(root, path)
            hashed += 1
            oid = _blob(data, oid_length)
            entries[path] = (mode, oid)
            row = [path, _sha(data), len(data), mode, oid]
        name = _path_shard(path)
        file_rows[path] = row
        shards.setdefault(name, []).append(row)
        groups.setdefault(_group(path), set()).add(name)
        if _SOURCE_PATH.fullmatch(path):
            if previous is row:
                if not hasattr(prior, '_by_path'):
                    prior._by_path = {prior.record_path(identifier): prior._record_row(identifier)
                                      for identifier in prior.records()}
                record = prior._by_path.get(path)
                if record is None:
                    raise CorpusIndexError(f'source record absent from prior index: {path}')
            else:
                data = changed.get(path)
                if data is None:
                    data, _ = _safe_read(root, path)
                try:
                    value = tomllib.loads(data.decode('utf-8'))
                except (ValueError, UnicodeError) as error:
                    raise CorpusIndexError(f'invalid source record: {path}') from error
                identifier, kind = value.get('id'), value.get('record_type')
                if kind not in KINDS or not isinstance(identifier, str) or not identifier.startswith(kind + '.'):
                    raise CorpusIndexError(f'invalid canonical record identity: {path}')
                record = [identifier, kind, path, _dependencies(value)]
                parsed += 1
            if record[0] in records:
                raise CorpusIndexError(f'duplicate source record ID: {record[0]}')
            records[record[0]] = record
    for identifier, row in sorted(records.items()):
        shards.setdefault(_id_shard(identifier), []).append(row)
    output = {}
    for name, rows in sorted(shards.items()):
        data = b''.join(_json(row) for row in rows)
        if len(data) > SHARD_LIMIT:
            raise CorpusIndexError(f'corpus shard exceeds {SHARD_LIMIT} bytes: {name}')
        output[name] = data
    manifest = {'schema': SCHEMA, 'scopes': list(SCOPES), 'authorities': list(AUTHORITIES),
                'extra_inputs': list(EXTRA_INPUTS),
                'binding': _binding(entries), 'membership': _membership(entries, records),
                'files': len(entries), 'records': len(records),
                'groups': {key: sorted(value) for key, value in sorted(groups.items())},
                'shards': {name: [_sha(data), len(data)] for name, data in output.items()}}
    from _reader_index import bindings, fingerprints, validate_bindings
    manifest['reader_inputs'] = fingerprints(file_rows)
    manifest['readers'] = bindings(file_rows, manifest['reader_inputs'])
    if validate_readers:
        validate_bindings(root, manifest['readers'])
    output['index.json'] = _json(manifest)
    if len(output['index.json']) > ROOT_LIMIT or sum(map(len, output.values())) > TOTAL_LIMIT:
        raise CorpusIndexError(f"corpus index exceeds metadata budget: root={len(output['index.json'])}, total={sum(map(len, output.values()))}")
    return output, {'files': len(entries), 'records': len(records), 'hashed': hashed,
                    'parsed': parsed, 'reused': reused, 'bytes': sum(map(len, output.values())),
                    'root_bytes': len(output['index.json'])}


def _refresh_unlocked(root, *, full=False, check=False):
    root = Path(root).absolute()
    output, report = _generate(root, full=full or check)
    destination = root / INDEX
    existing = {path.relative_to(destination).as_posix() for path in destination.rglob('*') if path.is_file()}
    if check:
        if existing != set(output):
            raise CorpusIndexError('corpus index membership differs; run tools/corpus-index refresh')
        for name, data in output.items():
            actual, _ = _safe_read(root, INDEX + '/' + name, ROOT_LIMIT if name == 'index.json' else SHARD_LIMIT)
            if actual != data:
                raise CorpusIndexError(f'stale corpus index {name}; run tools/corpus-index refresh')
    else:
        for name, data in output.items():
            path = destination / name
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists() and path.read_bytes() == data:
                continue
            path.write_bytes(data)
        for name in existing - set(output):
            (destination / name).unlink()
    return {'status': 'ok', **report}


@contextmanager
def _maintenance_lock(root):
    directory = Path(root) / '.scratch/corpus-index'
    directory.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(directory / 'refresh.lock', os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        os.close(descriptor)


def refresh(root, *, full=False, check=False, readers=False):
    root = Path(root).absolute()
    with _maintenance_lock(root):
        if readers:
            from _reader_index import maintain
            return maintain(root, full=full, check=check)
        return _refresh_unlocked(root, full=full, check=check)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('refresh', 'check'))
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--full', action='store_true', help='independently hash and parse every input')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--readers', action='store_true', help='derive/replay every thin reader index before the canonical index')
    args = parser.parse_args(argv)
    try:
        report = refresh(args.root, full=args.full, check=args.command == 'check', readers=args.readers)
    except (CorpusIndexError, OSError, ValueError) as error:
        if args.json:
            print(_json({'v': 1, 'status': 'error', 'code': 'invalid-index', 'error': str(error)}).decode(), end='', file=sys.stderr)
        else:
            print(f'corpus-index: {error}', file=sys.stderr)
        return 1
    if args.json:
        print(_json({'v': 1, **report}).decode(), end='')
    else:
        print(f"corpus-index: {report['files']} files, {report['records']} records, {report['bytes']} metadata bytes; ok")
    return 0
