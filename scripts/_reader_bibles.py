"""Indexed Bible addressing with the source owner's resolver and lazy text.

The tracked table contains verse bounds and holes, never Scripture wording.
Alias interpretation, open ranges and refusals remain index-bible's methods.
"""
from __future__ import annotations

from collections.abc import Mapping
from contextlib import contextmanager
from pathlib import Path
import json
import threading

import _loci
import _projection
import _psalms

METADATA_PATH = "src/index/commentary/bibles.json"
SCHEMA = "triptych-reader-bible-addresses/v1"
READ_LOCK = threading.RLock()


def build_metadata(root: Path) -> dict:
    """Derive address metadata from each offered edition's canonical TSVs."""
    register = _loci._bible_register()
    editions = {}
    for identifier, record in sorted(register.EDITIONS.items()):
        if not record.get("publishable"):
            continue
        artifacts = Path(root) / "src/sources/works" / record["artifacts"]
        original = register.Bible(artifacts)
        books = {}
        for (token, chapter), (low, high) in sorted(original.chapters.items()):
            holes = [verse for verse in range(low, high + 1)
                     if (token, chapter, verse) not in original.verses]
            books.setdefault(token, {})[str(chapter)] = [low, high, *holes]
        editions[identifier] = books
    return {"schema": SCHEMA, "editions": editions}


class _Verses(Mapping):
    def __init__(self, index, edition: str, books: dict) -> None:
        self.index, self.edition, self.books = index, edition, books
        self.loaded = {}

    def __contains__(self, point):
        token, chapter, verse = point
        bounds = self.books.get(token, {}).get(str(chapter))
        return (bounds is not None and bounds[0] <= verse <= bounds[1]
                and verse not in bounds[2:])

    def __getitem__(self, point):
        if point not in self:
            raise KeyError(point)
        token, chapter, verse = point
        key = token, chapter
        if key not in self.loaded:
            path = f"src/sources/bibles/{self.edition}/chapters/{token}/{chapter}.json"
            payload = json.loads(self.index.read(path))
            if payload.get("book") != token or payload.get("chapter") != chapter:
                raise ValueError(f"{path}: chapter identity differs from its address")
            self.loaded[key] = payload["verses"]
        return self.loaded[key][str(verse)]

    def __iter__(self):
        for token, chapters in self.books.items():
            for chapter, bounds in chapters.items():
                for verse in range(bounds[0], bounds[1] + 1):
                    if verse not in bounds[2:]:
                        yield token, int(chapter), verse

    def __len__(self):
        return sum(bounds[1] - bounds[0] + 1 - len(bounds[2:])
                   for chapters in self.books.values() for bounds in chapters.values())


def metadata(index) -> dict:
    document = json.loads(index.read(METADATA_PATH))
    if document.get("schema") != SCHEMA or not isinstance(document.get("editions"), dict):
        raise ValueError(f"{METADATA_PATH}: invalid Bible address index")
    return document


def bible(root: Path, index, edition: str, *, addresses=None):
    """Return the ordinary Bible resolver with indexed presence and lazy verses."""
    addresses = metadata(index) if addresses is None else addresses
    register = _loci._bible_register()
    record = register.EDITIONS.get(edition)
    if record is None or not record.get("publishable"):
        raise KeyError(edition)
    books = addresses["editions"][edition]
    artifacts = Path(root) / "src/sources/works" / record["artifacts"]
    result = register.Bible.__new__(register.Bible)
    result.books = register.load_books(artifacts)
    result.verses = _Verses(index, edition, books)
    result.aliases = register.load_aliases(artifacts)
    result.alias_notes = {row.cited_locus: row.note
                          for row in _projection.alias_rows(artifacts.parent)
                          if not row.resolves_to}
    result.chapters = {(token, int(chapter)): tuple(bounds[:2])
                       for token, chapters in books.items()
                       for chapter, bounds in chapters.items()}
    result._load_open_bounds()
    return result


@contextmanager
def bible_context(root: Path, index):
    """Scope shared citation resolution to this indexed root and fresh readers.

    The lock serializes scoped resolver changes; restoration prevents the batch
    producer from inheriting an interactive resolver or another root's caches.
    """
    with READ_LOCK, _bible_context(root, index) as selected:
        yield selected


@contextmanager
def _bible_context(root: Path, index):
    addresses = metadata(index)
    register = _loci._bible_register()
    prior_bible, prior_root = _loci._edition_bible, register.SOURCE_ROOT
    prior_concordance = _psalms.CONCORDANCE_ROOT
    resolved = {}

    def selected(identifier):
        if identifier not in resolved:
            resolved[identifier] = bible(root, index, identifier, addresses=addresses)
        return resolved[identifier]

    _loci._edition_bible = selected
    register.SOURCE_ROOT = Path(root) / "src/sources/works"
    _psalms.CONCORDANCE_ROOT = register.SOURCE_ROOT / "english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts"
    for function in (_psalms._concordance, _psalms.witness_merges, _psalms._english):
        function.cache_clear()
    _loci.edition_readers.cache_clear()
    try:
        yield selected
    finally:
        _loci._edition_bible, register.SOURCE_ROOT = prior_bible, prior_root
        _psalms.CONCORDANCE_ROOT = prior_concordance
        for function in (_psalms._concordance, _psalms.witness_merges, _psalms._english):
            function.cache_clear()
        _loci.edition_readers.cache_clear()
