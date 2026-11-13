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
    'commentary': ('src/sources',),
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


def _input(surface, path):
    if path.startswith('src/index/'):
        return False
    from _corpus_index import AUTHORITIES
    return (any(_under(path, prefix) for prefix in (*COMMON, *SURFACES[surface]))
            or path in AUTHORITIES or '/' not in path)


def fingerprints(file_rows):
    """Canonical inputs for all surfaces, including ones not generated yet."""
    result = {}
    for surface in ORDER:
        source = hashlib.sha256()
        source.update(json.dumps([SCHEMA, surface, COMMON, SURFACES[surface]], separators=(',', ':')).encode())
        for path, row in sorted(file_rows.items()):
            if _input(surface, path):
                source.update(f'{path}\0{row[1]}\0{row[2]}\n'.encode())
        result[surface] = source.hexdigest()
    return result


def bindings(file_rows, inputs=None):
    """Bind indexed SHA-256/size rows; callers already checked canonical bytes."""
    inputs = fingerprints(file_rows) if inputs is None else inputs
    result = {}
    for surface in ORDER:
        outputs = [path for path in sorted(file_rows) if surface_for(path) == surface]
        if not outputs:
            continue
        target = hashlib.sha256()
        for path in outputs:
            row = file_rows[path]
            target.update(f'{path}\0{row[1]}\0{row[2]}\n'.encode())
        result[surface] = {'inputs': inputs[surface], 'outputs': target.hexdigest(), 'files': len(outputs)}
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


def maintain(root, *, full=False, check=False):
    """Called under corpus-index's one writer lock; skip unchanged derivations."""
    from _corpus_index import (CorpusIndex, CorpusIndexError, _generate,
                               _refresh_unlocked, _json, _safe_read)
    snapshot, _ = _generate(root, full=full and not check, validate_readers=False)
    index = CorpusIndex(root, _bind=False, _snapshot=snapshot)
    prior = _proof(root)
    before = index.manifest['readers']
    before_inputs = index.manifest['reader_inputs']
    selected = [surface for surface in ORDER if check or full or prior.get(surface) != before.get(surface)
                or surface not in before]
    rebuilt = []
    for surface in selected:
        files = build_surface(surface, root, index, check=check)
        if not files or any(surface_for(path) != surface or not isinstance(data, bytes)
                            for path, data in files.items()):
            raise CorpusIndexError(f'invalid {surface} reader-index producer membership')
        existing = set(index.paths('src/index/'))
        existing = {path for path in existing if surface_for(path) == surface}
        if check:
            if existing != set(files):
                raise CorpusIndexError(f'stale {surface} reader index membership')
            for path, data in files.items():
                if _safe_read(root, path)[0] != data:
                    raise CorpusIndexError(f'stale {surface} reader index: {path}')
        else:
            for path, data in files.items():
                _write(root, path, data)
            for path in existing - set(files):
                (root / path).unlink()
            # Later surfaces may consume metadata just generated by an owner.
            snapshot, _ = _generate(root, validate_readers=False)
            index = CorpusIndex(root, _bind=False, _snapshot=snapshot)
        rebuilt.append(surface)
    final_snapshot, _ = _generate(root, validate_readers=False)
    final_manifest = json.loads(final_snapshot['index.json'])
    final = final_manifest['readers']
    if final_manifest['reader_inputs'] != before_inputs:
        raise CorpusIndexError('canonical inputs changed during reader derivation; refresh again')
    if check:
        validate_bindings(root, final)
    else:
        _write(root, PROOF, _json({'schema': SCHEMA, 'surfaces': final}))
    report = _refresh_unlocked(root, full=full, check=check)
    return {**report, 'reader_surfaces': rebuilt, 'reader_reused': [name for name in ORDER if name not in rebuilt]}
