"""Selected Sources products through the canonical reader's rights projection."""
from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
from functools import lru_cache
from pathlib import Path

from _indexed_source_library import Library


@lru_cache(maxsize=1)
def _reader():
    path = Path(__file__).resolve().parents[1] / 'tools/source-reader'
    loader = importlib.machinery.SourceFileLoader('_selected_source_reader', str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


def resolve(relative: str, root: Path, index) -> bytes | None:
    prefix = 'structure/sources/'
    if not relative.startswith(prefix):
        return None
    reader = _reader()
    if relative == prefix + 'index.json' or (
            relative.startswith(prefix + 'catalogue/') and relative.endswith('.json')):
        return index.read('src/index/sources/' + relative[len(prefix):])
    passage_id = None
    if relative.startswith(prefix + 'text/') and relative.endswith('.json'):
        passage_id = relative[len(prefix + 'text/'):-5]
        if not reader.SAFE_ID.fullmatch(passage_id) or index.record_kind(passage_id) != 'passage':
            raise ValueError(f'Unknown Sources passage: {passage_id}')
        edition_id = index.record(passage_id)['edition_id']
    else:
        if not relative.startswith(prefix + 'editions/') or not relative.endswith('.json'):
            raise ValueError(f'Unknown Sources route: {relative}')
        route = Path(relative[len(prefix + 'editions/'):])
        directory = 'src/sources/works/' + route.parent.as_posix() + '/'
        library = Library(root, index, ())
        matches = []
        for path in index.paths(directory, suffix='/edition.toml'):
            ident = index.record_id_for_path(path)
            if ident is None or index.record_kind(ident) != 'edition':
                continue
            candidate = index.record(ident)
            if (reader.work_directory(library, candidate['work_id']) +
                    reader.edition_stem(library, candidate)) == relative[len(prefix):]:
                matches.append(ident)
        if len(matches) != 1:
            raise ValueError(f'Unknown Sources edition route: {relative}')
        edition_id = matches[0]
    edition = index.record(edition_id)
    work_id = edition['work_id']
    # A directory scopes enumeration, never foreign-controller lookup. The
    # canonical record's edition_id is still checked by the pure projection.
    directory = Path(index.record_path(edition_id)).parent.as_posix() + '/'
    ids = {work_id, edition_id}
    if passage_id is not None:
        ids.add(passage_id)
    else:
        for path in index.paths(directory, suffix='.toml'):
            try:
                ident = index.record_id_for_path(path)
            except KeyError:  # Artifact payloads can themselves be TOML, without being library records.
                continue
            if ident is not None:
                ids.add(ident)
    works = reader._corpus(Library(root, index, sorted(ids)))
    work = next(one for one in works if one['id'] == work_id)
    projected = next(one for one in work['editions'] if one['id'] == edition_id)
    if passage_id is None:
        body = reader.edition_payload(work, projected)
    else:
        passage = next((one for one in projected['passages'] if one['id'] == passage_id), None)
        if passage is None or not passage['reading']['readable']:
            raise ValueError(f'Sources passage is not readable: {passage_id}')
        body = reader.text_payload(work, projected, passage)
    return reader._serialise(body).encode('utf-8')
