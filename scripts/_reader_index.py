"""One maintenance gate for thin reader metadata and its canonical derivation.

Each surface proof is two aggregate hashes, never a second file-hash inventory.
Canonical source membership and exact generator code bind the input; complete
metadata membership binds the output. Generic corpus refresh refuses a stale
proof. Reader opening compares the same proof with already-bound root metadata,
without replaying a producer or walking source files. All adapters below are
explicit maintenance operations, never reader startup dependencies.
"""
from __future__ import annotations

from argparse import Namespace
from contextlib import contextmanager
import hashlib
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
import os
from pathlib import Path
import sys

PROOF = 'src/index/readers.json'
SCHEMA = 'triptych-reader-derivations/v1'
# Source scopes mirror the full producer recipes. Code is deliberately a
# conservative common scope until narrower closures have independent audits.
COMMON = ('scripts', 'tools')
SURFACES = {
    'commentary': ('src/sources', 'src/web/browser/catena/catena-model.js'),
    'sources': ('src/sources', 'src/gpt', 'src/claude', 'src/common', 'web'),
    'liturgy': ('src/sources', 'src/gpt', 'src/claude'),
    'history': ('src/sources', 'src/gpt', 'src/claude', 'src/common', 'web',
                'guidance/liturgical-text-publication-policy.md'),
    'documents': ('src', 'web', 'release/publications', 'workflows/fragments',
                  'workflows/pipelines', 'workflows/schema',
                  'guidance/liturgy/postconciliar-propers-registry.md'),
}
ORDER = ('commentary', 'sources', 'liturgy', 'history', 'documents')
OUTPUTS = {
    'commentary': ('src/index/commentary',),
    'sources': ('src/index/sources',),
    'liturgy': ('src/index/propers', 'src/index/reader-manifests.json'),
    'history': ('src/index/history',),
    'documents': ('src/index/documents',),
}
COLD_CACHE_FLAGS = ('TRIPTYCH_LIBRARY_CACHE', 'TRIPTYCH_CORPUS_CACHE',
                    'TRIPTYCH_YAML_CACHE', 'TRIPTYCH_CONTAINMENT_CACHE',
                    'TRIPTYCH_SOURCE_LIBRARY_CACHE')


def _under(path, prefix):
    return path == prefix or path.startswith(prefix + '/')


def surface_for(path):
    return next((surface for surface, prefixes in OUTPUTS.items()
                 if any(_under(path, prefix) for prefix in prefixes)), None)


def fingerprints(file_rows):
    """Canonical inputs for all surfaces, including ones not generated yet."""
    from _corpus_index import AUTHORITIES
    sources = {}
    scopes = {}
    for surface in ORDER:
        source = hashlib.sha256()
        source.update(json.dumps([SCHEMA, surface, COMMON, SURFACES[surface]], separators=(',', ':')).encode())
        sources[surface] = source
        scopes[surface] = tuple(prefix + '/' for prefix in (*COMMON, *SURFACES[surface]))
    for path, row in sorted(file_rows.items()):
        if path.startswith('src/index/'):
            continue
        encoded = f'{path}\0{row[1]}\0{row[2]}\n'.encode()
        common = path in AUTHORITIES or '/' not in path
        for surface, prefixes in scopes.items():
            if common or path.startswith(prefixes) or path in SURFACES[surface] or path in COMMON:
                sources[surface].update(encoded)
    return {surface: source.hexdigest() for surface, source in sources.items()}


def bindings(file_rows, inputs=None):
    """Bind indexed SHA-256/size rows; callers already checked canonical bytes."""
    inputs = fingerprints(file_rows) if inputs is None else inputs
    result = {}
    outputs = {}
    for path in sorted(path for path in file_rows if path.startswith('src/index/')):
        surface = surface_for(path)
        if surface is not None:
            outputs.setdefault(surface, []).append(path)
    for surface, paths in outputs.items():
        target = hashlib.sha256()
        for path in paths:
            row = file_rows[path]
            target.update(f'{path}\0{row[1]}\0{row[2]}\n'.encode())
        result[surface] = {'inputs': inputs[surface], 'outputs': target.hexdigest(), 'files': len(paths)}
    return result


def _proof(root):
    from _corpus_index import _safe_read, CorpusIndexError
    try:
        raw, _ = _safe_read(root, PROOF, 16 * 1024)
        value = json.loads(raw)
        if not isinstance(value, dict) or value.get('schema') != SCHEMA or not isinstance(value.get('surfaces'), dict):
            raise ValueError('invalid proof')
        return value['surfaces']
    except (ValueError, TypeError, CorpusIndexError):
        return {}


def validate_bindings(root, expected):
    from _corpus_index import CorpusIndexError
    actual = _proof(root)
    changed = sorted(set(expected) | set(actual))
    changed = [name for name in changed if expected.get(name) != actual.get(name)]
    if changed:
        raise CorpusIndexError('stale reader derivation (' + ', '.join(changed)
                               + '); run tools/corpus-index refresh --readers')


def _tool(root, name):
    loader = SourceFileLoader('_reader_index_' + name.replace('-', '_'), str(root / 'tools' / name))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


@contextmanager
def _cold_caches(root):
    values = {key: '0' for key in COLD_CACHE_FLAGS}
    values['TRIPTYCH_LIBRARY_CACHE_DIR'] = str(root / '.scratch/corpus-index/library')
    previous = {key: os.environ.get(key) for key in values}
    os.environ.update(values)
    try:
        yield
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def build_surface(surface, root, index, *, check=False):
    """Return exact bytes through the owning producers, with no rendering copies."""
    with _cold_caches(root):
        return _build_surface(surface, root, index, check=check)


def _build_surface(surface, root, index, *, check=False):
    if surface == 'commentary':
        import _reader_commentary_products as owner
        import _reader_bibles as bibles
        return {bibles.METADATA_PATH: owner._json(bibles.build_metadata(root)),
                owner.CATALOG_PATH: owner._json(owner.build_catalog(root))}
    if surface == 'sources':
        owner = _tool(root, 'source-reader')
        works = owner.corpus(owner.load(Namespace(strict=True)))
        files = owner.discovery_files(owner.spine(works, owner.tally(works)))
        return {'src/index/sources/' + name: body.encode('utf-8') for name, body in files.items()}
    if surface == 'liturgy':
        from _reader_products import build_reader_indexes
        return build_reader_indexes(root, index=index)
    if surface == 'history':
        import _reader_history_products as owner
        return {owner.INDEX_PATH: owner._json(owner.build_index(root), indent=1)}
    if surface == 'documents':
        import _reader_publication_products as owner
        anchor = None
        if check:
            anchor = json.loads((root / owner.READERS).read_bytes())['generation_commit']
        return owner.build_reader_indexes(root, generation_commit=anchor)
    raise ValueError(f'unknown reader index surface: {surface}')


def _write(root, path, data):
    from _corpus_index import _relative, CorpusIndexError
    path = _relative(path)
    target = root / path
    # Authoring must not follow an index-directory or output symlink either.
    for parent in (target, *target.parents):
        if parent == root:
            break
        if parent.is_symlink():
            raise CorpusIndexError(f'unsafe reader index output: {path}')
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists() or target.read_bytes() != data:
        target.write_bytes(data)


def _surface_files(surface, root, index, *, check):
    from _corpus_index import CorpusIndexError
    files = build_surface(surface, root, index, check=check)
    if not files or any(surface_for(path) != surface or not isinstance(data, bytes)
                        for path, data in files.items()):
        raise CorpusIndexError(f'invalid {surface} reader-index producer membership')
    existing = {path for path in index.paths('src/index/') if surface_for(path) == surface}
    return files, existing


def _check_surface(surface, root, index):
    from _corpus_index import CorpusIndexError, _safe_read
    files, existing = _surface_files(surface, root, index, check=True)
    if existing != set(files):
        raise CorpusIndexError(f'stale {surface} reader index membership')
    for path, data in files.items():
        if _safe_read(root, path)[0] != data:
            raise CorpusIndexError(f'stale {surface} reader index: {path}')


def _check_worker(surface, root, identity):
    # Parallel reader-surface workers share one host; keep nested pools bounded.
    os.environ['PYTHON_CPU_COUNT'] = '1'
    from _corpus_index import CorpusIndex, CorpusIndexError
    index = CorpusIndex(root, _bind=False)
    if index.identity != identity:
        raise CorpusIndexError('corpus index changed during reader verification')
    _check_surface(surface, root, index)


def _check_all(root, jobs):
    from _corpus_index import CorpusIndex, _refresh_unlocked
    index = CorpusIndex(root)
    if jobs == 1:
        for surface in ORDER:
            _check_surface(surface, root, index)
        report = _refresh_unlocked(root, check=True, expected_identity=index.identity)
    else:
        # Submit heaviest surfaces first and overlap the read-only full corpus
        # hash/parse check beside the surface workers, still surfacing any
        # surface mismatch before accepting the report.
        from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
        from multiprocessing import get_context
        priority = {'documents': 0, 'commentary': 1, 'sources': 2, 'history': 3, 'liturgy': 4}
        scheduled = sorted(ORDER, key=lambda name: priority.get(name, 99))
        # A fresh interpreter needs no fork-server socket in the caller's TMPDIR.
        with (ProcessPoolExecutor(max_workers=min(jobs, len(scheduled)), mp_context=get_context('spawn')) as pool,
              ThreadPoolExecutor(max_workers=1) as full_check):
            checks = [pool.submit(_check_worker, surface, root, index.identity) for surface in scheduled]
            refresh_future = full_check.submit(_refresh_unlocked, root, check=True, expected_identity=index.identity)
            for check in checks:
                check.result()
            report = refresh_future.result()
    return {**report, 'reader_surfaces': list(ORDER), 'reader_reused': []}


def maintain(root, *, full=False, check=False, jobs=1):
    """Replay every read-only check, or refresh changed surfaces in dependency order."""
    from _corpus_index import (CorpusIndex, CorpusIndexError, _generate,
                               _refresh_unlocked, _json)
    if check:
        return _check_all(root, jobs)
    snapshot, _ = _generate(root, full=full, validate_readers=False)
    index = CorpusIndex(root, _bind=False, _snapshot=snapshot)
    prior = _proof(root)
    before = index.manifest['readers']
    before_inputs = index.manifest['reader_inputs']
    selected = [surface for surface in ORDER if full or prior.get(surface) != before.get(surface)
                or surface not in before]
    for surface in selected:
        files, existing = _surface_files(surface, root, index, check=False)
        for path, data in files.items():
            _write(root, path, data)
        for path in existing - set(files):
            (root / path).unlink()
        # Later surfaces may consume metadata just generated by an owner.
        snapshot, _ = _generate(root, full=full, validate_readers=False)
        index = CorpusIndex(root, _bind=False, _snapshot=snapshot)
    final_snapshot, _ = _generate(root, full=full, validate_readers=False)
    final_manifest = json.loads(final_snapshot['index.json'])
    final = final_manifest['readers']
    if final_manifest['reader_inputs'] != before_inputs:
        raise CorpusIndexError('canonical inputs changed during reader derivation; refresh again')
    _write(root, PROOF, _json({'schema': SCHEMA, 'surfaces': final}))
    report = _refresh_unlocked(root, full=full)
    return {**report, 'reader_surfaces': selected, 'reader_reused': [name for name in ORDER if name not in selected]}
