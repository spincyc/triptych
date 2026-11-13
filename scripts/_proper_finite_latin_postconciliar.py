"""Route two separately reviewed finite methods without combining their authority.

The six-owner and ten-owner validators own their unchanged, disjoint scopes.
Recognition alone never grants permission. Mixed signatures fail closed, and
an unrecognized study-reconstruction claim cannot fall through a public guard.
"""
from hashlib import sha256
from pathlib import Path

import _proper_finite_latin_20261112_postconciliar as six
import _proper_finite_latin_20261113_postconciliar_ten as ten

_METHODS = (six, ten)


def _matching(kind, *args, **kwargs):
    return tuple(method for method in _METHODS
                 if getattr(method, 'claims_' + kind)(*args, **kwargs))


def claims_row(row):
    return bool(_matching('row', row))


def claims_artifact(artifact):
    return bool(_matching('artifact', artifact))


def claims_reading(passage, artifact, **selected):
    return bool(_matching('reading', passage, artifact, **selected))


def claims_public(latin):
    return bool(_matching('public', latin))


def _unique(methods, operation, *args, **kwargs):
    if len(methods) != 1:
        return ['Postconciliar finite Latin requires one exact, separately adopted method']
    return getattr(methods[0], operation)(*args, **kwargs)


def row_problems(row):
    return _unique(_matching('row', row), 'row_problems', row)


def authority_problems(root, *, row):
    return _unique(_matching('row', row), 'authority_problems', root)


def source_problems(row, sources, *, effective_calendar=''):
    return _unique(_matching('row', row), 'source_problems', row, sources,
                   effective_calendar=effective_calendar)


def artifact_problems(root, artifact, *, sources=None):
    return _unique(_matching('artifact', artifact), 'artifact_problems', root,
                   artifact, sources=sources)


def reading_problems(root, passage, artifact, *, sources=None, **selected):
    return _unique(_matching('reading', passage, artifact, **selected),
                   'reading_problems', root, passage, artifact,
                   sources=sources, **selected)


def public_scope(latin):
    matches = [scope for method in _METHODS
               if (scope := method.public_scope(latin)) is not None]
    return matches[0] if len(matches) == 1 else None


def cache_fingerprint(root):
    digest = sha256(Path(__file__).read_bytes())
    for method in _METHODS:
        digest.update(method.cache_fingerprint(root).encode('ascii'))
    return digest.hexdigest()
