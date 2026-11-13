"""Lazy source records from the verified corpus index, without a graph scan.

Iteration can be restricted to an edition's owned records. Foreign controller
lookups remain possible: a segment does not transfer its artifact's ownership.
This is a reading view, not a replacement for source-library validation.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Record:
    path: Path
    record_type: str
    record_id: str
    data: dict[str, Any]


class Records(Mapping[str, Record]):
    def __init__(self, root: Path, index, ids=None) -> None:
        self.root = Path(root)
        self.index = index
        self.ids = tuple(ids) if ids is not None else None
        self._held: dict[str, Record] = {}

    def __getitem__(self, ident: str) -> Record:
        if ident not in self._held:
            self._held[ident] = Record(
                self.root / self.index.record_path(ident),
                self.index.record_kind(ident), ident, self.index.record(ident))
        return self._held[ident]

    def __iter__(self) -> Iterator[str]:
        return iter(self.ids if self.ids is not None else self.index.records())

    def __len__(self) -> int:
        return len(self.ids if self.ids is not None else self.index.records())


class Library:
    def __init__(self, root: Path, index, ids=None) -> None:
        self.root = Path(root)
        self.source_root = self.root / 'src/sources'
        self.publication_roots = [self.root / 'src/gpt', self.root / 'src/claude']
        self.records = Records(self.root, index, ids)
        self.errors: list[str] = []


class _DataRecords(Mapping[str, dict]):
    def __init__(self, index) -> None:
        self.index = index
        self._held: dict[str, dict] = {}

    def __getitem__(self, ident: str) -> dict:
        if ident not in self._held:
            self._held[ident] = dict(self.index.record(ident),
                                     record_type=self.index.record_kind(ident), id=ident)
        return self._held[ident]

    def __iter__(self) -> Iterator[str]:
        return iter(self.index.records())

    def __len__(self) -> int:
        return len(self.index.records())


def indexed_records(index) -> Mapping[str, dict]:
    """The dictionary-valued record view used by publication-rights owners."""
    return _DataRecords(index)
