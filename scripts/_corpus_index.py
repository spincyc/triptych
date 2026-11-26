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
from concurrent.futures import ThreadPoolExecutor
import copy
import fcntl
from fnmatch import fnmatchcase
from functools import wraps
from contextlib import contextmanager
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
import threading
import time
import tomllib

from _session_derivations import _ACTIVE, _DERIVATIONS, session_derivations, session_derived

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
    'workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/authority-v5.json',
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
_OPEN, _IO_OPEN = builtins.open, io.open
_PATH_METHODS = {name: getattr(Path, name) for name in ('glob', 'rglob', 'exists', 'is_file', 'is_dir')}
_PATCH_LOCK = threading.RLock()
_PATCH_USERS = 0
_COVERED_PREFIXES = tuple(p + '/' for p in SCOPES)
_COVERED_EXACT = frozenset((*SCOPES, *AUTHORITIES, *EXTRA_INPUTS))
_DIR_CACHE_RELATIVE = '.scratch/corpus-index/dir-stat-v1.json'
_DIR_CACHE_MIN_ENTRIES = 2000
_DIR_CACHE_RACY_NS = 2_000_000_000


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
    if (not isinstance(value, str) or not value or value[0] == '/' or '\\' in value or '\0' in value
            or '//' in value or value in ('.', '..') or value.startswith(('./', '../'))
            or value.endswith(('/.', '/..')) or '/./' in value or '/../' in value):
        raise CorpusIndexError(f'unsafe corpus path: {value!r}')
    return value


def _covered(path):
    if path == INDEX or path.startswith(INDEX + '/') or path == 'release/browser-products.json':
        return False
    if path.startswith('tools/tests/') or path.endswith('.pyc') or '/__pycache__/' in path:
        return False
    if path.startswith(_COVERED_PREFIXES) or path in _COVERED_EXACT:
        return True
    return '/' not in path and (
        path.startswith('requirements') and path.endswith('.txt')
        or path.endswith(('.lock', '-lock.json')))


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


_DEFAULT_SAFE_READ = _safe_read


def _git(root, *arguments):
    env = {**os.environ, 'GIT_OPTIONAL_LOCKS': '0', 'GIT_NO_LAZY_FETCH': '1'}
    result = subprocess.run(['git', '-C', str(root), *arguments], capture_output=True, env=env)
    if result.returncode:
        raise CorpusIndexError('corpus index requires a Git checkout: ' + result.stderr.decode(errors='replace').strip())
    return result.stdout


def _git_together(root, *commands):
    """Run independent read-only Git queries concurrently; fail as ``_git`` does."""
    env = {**os.environ, 'GIT_OPTIONAL_LOCKS': '0', 'GIT_NO_LAZY_FETCH': '1'}
    processes = []
    try:
        for arguments in commands:
            processes.append(subprocess.Popen(['git', '-C', str(root), *arguments],
                                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env))
        results = [process.communicate() for process in processes]
    finally:
        for process in processes:
            if process.poll() is None:
                process.kill()
                process.wait()
    for process, (_, stderr) in zip(processes, results):
        if process.returncode:
            raise CorpusIndexError('corpus index requires a Git checkout: ' + stderr.decode(errors='replace').strip())
    return [stdout for stdout, _ in results]


def _exclude_rules_hash(root, git_dir: Path, nested_ignores: tuple[str, ...] = ()):
    """Hash all ignore rules that affect untracked discovery inside covered scopes."""
    digest = hashlib.sha256()
    candidates = [root / '.gitignore', git_dir / 'info' / 'exclude']
    for rel in sorted(nested_ignores):
        candidates.append(root / rel)
    # Include core.excludesFile if configured (or default XDG ignore file).
    env = {**os.environ, 'GIT_OPTIONAL_LOCKS': '0', 'GIT_NO_LAZY_FETCH': '1'}
    cfg = subprocess.run(['git', '-C', str(root), 'config', '--path', '--get', 'core.excludesFile'],
                         capture_output=True, text=True, env=env)
    if cfg.returncode == 0 and cfg.stdout.strip():
        candidates.append(Path(cfg.stdout.strip()))
    else:
        xdg = os.environ.get('XDG_CONFIG_HOME') or os.path.expanduser('~/.config')
        candidates.append(Path(xdg) / 'git' / 'ignore')
    for candidate in candidates:
        digest.update(str(candidate).encode('utf-8') + b'\0')
        try:
            st = os.lstat(candidate)
            if stat.S_ISREG(st.st_mode):
                with _OPEN(candidate, 'rb') as handle:
                    digest.update(handle.read())
            else:
                digest.update(b'<non-regular>')
        except OSError:
            digest.update(b'<missing>')
        digest.update(b'\0')
    return digest.hexdigest()


def _collect_covered_dirs(root: Path, entries: dict) -> tuple[list[list], list[str]]:
    """Collect (rel_dir, dev, ino, mtime_ns, ctime_ns) for every covered dir."""
    root_str = str(root)
    dirs: set[str] = {''}
    for scope in SCOPES:
        parts = scope.split('/')
        for i in range(1, len(parts) + 1):
            dirs.add('/'.join(parts[:i]))
    for path in entries:
        slash = path.rfind('/')
        while slash > 0:
            parent = path[:slash]
            if parent in dirs:
                break
            dirs.add(parent)
            slash = parent.rfind('/')
    nested_ignores = sorted(p for p in entries if p.endswith('/.gitignore') or p == '.gitignore')
    # Also scan SCOPES directories that exist on disk to pick up empty dirs.
    rows = []
    for rel in sorted(dirs):
        target = root_str if not rel else f'{root_str}/{rel}'
        try:
            st = os.lstat(target)
            if not stat.S_ISDIR(st.st_mode):
                rows.append([rel, None])
            else:
                rows.append([rel, st.st_dev, st.st_ino, st.st_mtime_ns, st.st_ctime_ns])
        except OSError:
            rows.append([rel, None])
    return rows, nested_ignores


def _untracked_via_dir_cache(root: Path, entries: dict) -> bytes | None:
    """Use directory ctime/mtime stamps to avoid walking 66k unchanged dirs.

    In POSIX/Linux, creating, deleting, or renaming any entry inside a directory
    updates its kernel-maintained st_ctime_ns (which unprivileged utime cannot
    forge). Any directory within a 2s racy window, any changed directory, any
    changed ignore rule, or any missing/corrupt cache falls back to git ls-files.
    """
    cache_path = root / _DIR_CACHE_RELATIVE
    if cache_path.is_symlink():
        return None
    try:
        raw = cache_path.read_bytes()
        cached = json.loads(raw)
    except (OSError, ValueError):
        return None
    if (not isinstance(cached, dict) or cached.get('version') != 1
            or cached.get('root') != str(root) or cached.get('scopes') != list(SCOPES)
            or not isinstance(cached.get('dirs'), list)
            or not isinstance(cached.get('saved_ns'), int)
            or not isinstance(cached.get('nested_ignores'), list)
            or not isinstance(cached.get('untracked'), list)):
        return None
    git_dir = Path(_git(root, 'rev-parse', '--git-dir').decode('utf-8').strip())
    if not git_dir.is_absolute():
        git_dir = root / git_dir
    if cached.get('rules_sha256') != _exclude_rules_hash(root, git_dir, tuple(cached['nested_ignores'])):
        return None
    racy_floor = cached['saved_ns'] - _DIR_CACHE_RACY_NS
    root_str = str(root)
    known_dirs: set[str] = set()
    changed_dirs: list[str] = []
    root_changed = False
    for row in cached['dirs']:
        rel = row[0]
        known_dirs.add(rel)
        target = root_str if not rel else f'{root_str}/{rel}'
        try:
            st = os.lstat(target)
        except OSError:
            if row[1] is not None:
                if not rel:
                    root_changed = True
                else:
                    changed_dirs.append(rel)
            continue
        if not stat.S_ISDIR(st.st_mode):
            return None
        if (row[1] is None
                or st.st_dev != row[1] or st.st_ino != row[2]
                or st.st_mtime_ns != row[3] or st.st_ctime_ns != row[4]
                or st.st_ctime_ns >= racy_floor or st.st_mtime_ns >= racy_floor):
            if not rel:
                root_changed = True
            else:
                changed_dirs.append(rel)
    # Any newly tracked directory not yet in the cache must also be checked.
    for path in entries:
        slash = path.rfind('/')
        if slash > 0:
            parent = path[:slash]
            if parent not in known_dirs:
                changed_dirs.append(parent)
                known_dirs.add(parent)
    # Previously discovered untracked files' parents must be re-checked.
    for rel_file in cached['untracked']:
        slash = rel_file.rfind('/')
        if slash > 0:
            changed_dirs.append(rel_file[:slash])
        else:
            root_changed = True
    extra_untracked: list[bytes] = []
    if root_changed:
        # Inspect immediate root entries only (sub-millisecond) rather than
        # walking all 64k subdirectories under src/sources/works/.
        try:
            with os.scandir(root_str) as root_listing:
                for entry in root_listing:
                    name = entry.name
                    if name in ('.git', '.scratch', 'build', '.gitignore'):
                        continue
                    if entry.is_dir(follow_symlinks=False):
                        if name in SCOPES and name not in known_dirs:
                            changed_dirs.append(name)
                    elif _covered(name) and name not in entries:
                        extra_untracked.append(name.encode('utf-8'))
        except OSError:
            return None
    changed_dirs = sorted(set(changed_dirs))
    if len(changed_dirs) > 256:
        return None
    out_chunks = extra_untracked
    if changed_dirs:
        # Check if any changed dir introduced a new .gitignore file.
        for rel in changed_dirs:
            if os.path.lexists(f'{root_str}/{rel}/.gitignore') and f'{rel}/.gitignore' not in cached['nested_ignores']:
                return None
        res = _git(root, 'ls-files', '--others', '--exclude-standard', '-z', '--', *changed_dirs)
        if res:
            out_chunks.append(res.rstrip(b'\0'))
    return b'\0'.join(chunk for chunk in out_chunks if chunk)


def _save_dir_cache(root: Path, entries: dict, untracked_bytes: bytes, started_ns: int) -> None:
    try:
        git_dir = Path(_git(root, 'rev-parse', '--git-dir').decode('utf-8').strip())
        if not git_dir.is_absolute():
            git_dir = root / git_dir
        rows, nested_ignores = _collect_covered_dirs(root, entries)
        rules_sha = _exclude_rules_hash(root, git_dir, tuple(nested_ignores))
        untracked_list = sorted({
            item.decode('utf-8') for item in untracked_bytes.split(b'\0')
            if item and _covered(item.decode('utf-8'))
        })
        payload = {
            'version': 1,
            'root': str(root),
            'scopes': list(SCOPES),
            'saved_ns': started_ns,
            'rules_sha256': rules_sha,
            'nested_ignores': nested_ignores,
            'untracked': untracked_list,
            'dirs': rows,
        }
        cache_path = root / _DIR_CACHE_RELATIVE
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=cache_path.parent,
                                             prefix='.dir-stat-', delete=False) as handle:
                tmp = Path(handle.name)
                json.dump(payload, handle, separators=(',', ':'))
            os.replace(tmp, cache_path)
            tmp = None
        finally:
            if tmp is not None:
                tmp.unlink(missing_ok=True)
    except OSError:
        pass


def _parse_staged(staged: bytes) -> dict:
    entries = {}
    for item in staged.split(b'\0'):
        if not item:
            continue
        header, raw_path = item.split(b'\t', 1)
        path = raw_path.decode('utf-8')
        if not _covered(path):
            continue
        _relative(path)
        mode, oid, stage = header.decode('ascii').split()
        if stage != '0' or mode not in ('100644', '100755'):
            raise CorpusIndexError(f'unmerged or non-regular corpus input: {path}')
        entries[path] = (mode, oid)
    return entries


def _git_state(root):
    # Fast path for large repositories: overlap the staged/modified Git queries
    # with the disposable dir-ctime untracked check when the cache is present.
    cache_path = Path(root) / _DIR_CACHE_RELATIVE
    if cache_path.is_file() and not cache_path.is_symlink():
        staged, changed = _git_together(
            root, ('ls-files', '--stage', '-z'), ('ls-files', '--modified', '--deleted', '-z'))
        entries = _parse_staged(staged)
        untracked = None
        if len(entries) >= _DIR_CACHE_MIN_ENTRIES:
            untracked = _untracked_via_dir_cache(Path(root), entries)
        if untracked is None:
            started_ns = time.time_ns()
            untracked = _git(root, 'ls-files', '--others', '--exclude-standard', '-z')
            if len(entries) >= _DIR_CACHE_MIN_ENTRIES:
                _save_dir_cache(Path(root), entries, untracked, started_ns)
    else:
        started_ns = time.time_ns()
        staged, changed, untracked = _git_together(
            root, ('ls-files', '--stage', '-z'), ('ls-files', '--modified', '--deleted', '-z'),
            ('ls-files', '--others', '--exclude-standard', '-z'))
        entries = _parse_staged(staged)
        if len(entries) >= _DIR_CACHE_MIN_ENTRIES:
            _save_dir_cache(Path(root), entries, untracked, started_ns)
    dirty = set()
    for blob in (changed, untracked):
        if not blob:
            continue
        for item in blob.split(b'\0'):
            if not item:
                continue
            path = item.decode('utf-8')
            if _covered(path):
                dirty.add(_relative(path))
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
            if relative not in active[1] and len(active) > 3:
                active[3].add(relative)
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
            if len(active) > 3:
                active[3].discard(relative)
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
        is_outer = outer is None or outer[0] is not self
        dependencies = {} if is_outer else outer[1]
        failures = [] if is_outer else outer[2]
        meta_only = set() if is_outer else (outer[3] if len(outer) > 3 else set())
        token = _ACTIVE.set((self, dependencies, failures, meta_only))
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
            if is_outer:
                self._last_metadata_only = {p: dependencies[p] for p in meta_only if p in dependencies}
            with _PATCH_LOCK:
                _PATCH_USERS -= 1
                if _PATCH_USERS == 0:
                    builtins.open, io.open = _OPEN, _IO_OPEN
                    for name, method in _PATH_METHODS.items():
                        setattr(Path, name, method)
            if failures:
                _poison(failures[0])
                raise failures[0]


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


def _safe_read_at(directory: int, leaf: str, relative: str):
    """Read one regular file from an already-opened O_NOFOLLOW parent dir_fd."""
    try:
        descriptor = os.open(leaf, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        with _IO_OPEN(descriptor, 'rb', closefd=True) as source:
            before = os.fstat(source.fileno())
            if not stat.S_ISREG(before.st_mode):
                raise CorpusIndexError(f'corpus input is not a regular file: {relative}')
            result = source.read()
            after = os.fstat(source.fileno())
            if (before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
                    after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                raise CorpusIndexError(f'corpus input changed while reading: {relative}')
            return result, '100755' if before.st_mode & stat.S_IXUSR else '100644'
    except OSError as error:
        raise CorpusIndexError(f'missing or unsafe corpus input {relative}: {error.strerror}') from error


def _parallel_hash_and_parse(root: Path, paths: list[str], oid_length: int) -> dict[str, tuple[list, list | None]]:
    """Read, hash and parse source records via held dir_fd subtrees in parallel."""
    tree: dict = {}
    for path in paths:
        node = tree
        *directories, leaf = path.split('/')
        for directory in directories:
            node = node.setdefault(directory, {})
        node[leaf] = None
    workers = max(1, min(8, (getattr(os, 'process_cpu_count', os.cpu_count)() or 4)))

    def process_file(directory: int, leaf: str, path: str, out: dict):
        data, mode = _safe_read_at(directory, leaf, path)
        oid = _blob(data, oid_length)
        row = [path, _sha(data), len(data), mode, oid]
        record = None
        if _SOURCE_PATH.fullmatch(path):
            try:
                value = tomllib.loads(data.decode('utf-8'))
            except (ValueError, UnicodeError) as error:
                raise CorpusIndexError(f'invalid source record: {path}') from error
            identifier, kind = value.get('id'), value.get('record_type')
            if kind not in KINDS or not isinstance(identifier, str) or not identifier.startswith(kind + '.'):
                raise CorpusIndexError(f'invalid canonical record identity: {path}')
            record = [identifier, kind, path, _dependencies(value)]
        out[path] = (row, record)

    def walk(directory: int, children: dict, prefix: str, out: dict, allow_parallel: bool):
        subdirs = []
        for leaf, descendants in children.items():
            name = prefix + leaf
            if descendants is None:
                process_file(directory, leaf, name, out)
            else:
                subdirs.append((leaf, descendants, name))

        def walk_child(leaf: str, descendants: dict, name: str, target: dict, child_parallel: bool):
            try:
                child = os.open(leaf, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            except OSError as error:
                raise CorpusIndexError(f'missing or unsafe corpus input {name}: {error.strerror}') from error
            try:
                walk(child, descendants, name + '/', target, child_parallel)
            finally:
                os.close(child)

        if allow_parallel and workers > 1 and len(subdirs) >= 16:
            def run_sub(item):
                local = {}
                walk_child(item[0], item[1], item[2], local, False)
                return local

            with ThreadPoolExecutor(max_workers=min(workers, len(subdirs))) as pool:
                for local in pool.map(run_sub, subdirs):
                    out.update(local)
        else:
            for leaf, descendants, name in subdirs:
                walk_child(leaf, descendants, name, out, allow_parallel)

    results: dict[str, tuple[list, list | None]] = {}
    root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        walk(root_fd, tree, '', results, workers > 1)
    finally:
        os.close(root_fd)
    return results


def _generate(root, *, full=False, validate_readers=True):
    entries, changed = _current_state(root)
    prior = None
    if not full and (root / INDEX / 'index.json').exists():
        prior = CorpusIndex(root, _bind=False)
    shards, groups, records, file_rows = {}, {}, {}, {}
    hashed = parsed = reused = 0
    oid_length = len(next(iter(entries.values()))[1]) if entries else 40
    precomputed = {}
    if full and _safe_read is _DEFAULT_SAFE_READ and len(entries) >= 256:
        batch_paths = [path for path in sorted(entries) if path not in changed]
        precomputed = _parallel_hash_and_parse(root, batch_paths, oid_length)
    for path, (mode, oid) in sorted(entries.items()):
        previous = None
        from_precomputed = False
        if prior is not None:
            try:
                previous = prior._file_row(path)
            except KeyError:
                pass
        if (previous is not None and previous[3:] == [mode, oid]
                and (path not in changed or _sha(changed[path]) == previous[1])):
            row = previous
            reused += 1
        elif path in precomputed:
            from_precomputed = True
            row, pre_record = precomputed.pop(path)
            entries[path] = (row[3], row[4])
            hashed += 1
            if pre_record is not None:
                parsed += 1
                if pre_record[0] in records:
                    raise CorpusIndexError(f'duplicate source record ID: {pre_record[0]}')
                records[pre_record[0]] = pre_record
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
        if _SOURCE_PATH.fullmatch(path) and not from_precomputed:
            if previous is row:
                if not hasattr(prior, '_by_path'):
                    prior._by_path = {prior.record_path(identifier): prior._record_row(identifier)
                                      for identifier in prior.records()}
                record = prior._by_path.get(path)
                if record is None:
                    raise CorpusIndexError(f'source record absent from prior index: {path}')
            else:
                # Parse the exact bytes that produced this row's hash above.
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
    del prior, precomputed, changed
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


def _refresh_unlocked(root, *, full=False, check=False, expected_identity=None):
    root = Path(root).absolute()
    output, report = _generate(root, full=full or check)
    if expected_identity is not None and _sha(output['index.json']) != expected_identity:
        raise CorpusIndexError('canonical corpus changed during reader verification; check again')
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


def refresh(root, *, full=False, check=False, readers=False, jobs=1):
    root = Path(root).absolute()
    with _maintenance_lock(root):
        if readers:
            from _reader_index import maintain
            return maintain(root, full=full, check=check, jobs=jobs)
        return _refresh_unlocked(root, full=full, check=check)


def main(argv=None, *, examples=()):
    from _tooling import with_examples

    parser = argparse.ArgumentParser(description=__doc__)
    with_examples(parser, examples)
    parser.add_argument('command', choices=('refresh', 'check'))
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--full', action='store_true', help='independently hash and parse every input')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--readers', action='store_true', help='derive/replay every thin reader index before the canonical index')
    parser.add_argument('--jobs', type=int, metavar='N',
                        help='concurrent workers for check --readers (default: up to three)')
    args = parser.parse_args(argv)
    if args.jobs is not None and (args.command != 'check' or not args.readers or args.jobs < 1):
        parser.error('--jobs requires check --readers and a positive integer')
    parallel_check = args.command == 'check' and args.readers
    available = getattr(os, 'process_cpu_count', os.cpu_count)() or 1
    jobs = args.jobs or (min(3, available) if parallel_check else 1)
    try:
        report = refresh(args.root, full=args.full, check=args.command == 'check', readers=args.readers, jobs=jobs)
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
