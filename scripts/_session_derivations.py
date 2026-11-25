"""Session-scoped derivation reuse shared between indexed reading and producers.

Kept free of index-maintenance imports so producers that opt into per-session
reuse do not pull corpus-maintenance or publication tools into their static
code closure.
"""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
import copy
import pickle

_ACTIVE: ContextVar[tuple | None] = ContextVar('corpus_verified_reads', default=None)
_DERIVATIONS: ContextVar[dict | None] = ContextVar('corpus_session_derivations', default=None)


def _freeze(value):
    try:
        return True, pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
    except (pickle.PicklingError, TypeError, AttributeError):
        return False, copy.deepcopy(value)


def _thaw(frozen):
    pickled, payload = frozen
    if pickled:
        return pickle.loads(payload)
    return copy.deepcopy(payload)


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
    index, dependencies, failures = active[0], active[1], active[2]
    outer_meta = active[3] if len(active) > 3 else None
    held = cache.get(key)
    if held is not None:
        frozen, inputs, meta_inputs = held
        for relative in inputs:
            index.read(relative)
        for relative in meta_inputs:
            index.metadata(relative)
        return _thaw(frozen)
    consumed, consumed_meta, poisoned = {}, set(), len(failures)
    token = _ACTIVE.set((index, consumed, failures, consumed_meta))
    try:
        value = compute()
    finally:
        _ACTIVE.reset(token)
        for relative, digest in consumed.items():
            if outer_meta is not None:
                if relative in consumed_meta and relative not in dependencies:
                    outer_meta.add(relative)
                elif relative not in consumed_meta:
                    outer_meta.discard(relative)
            dependencies[relative] = digest
    if len(failures) == poisoned:
        full_reads = tuple(p for p in consumed if p not in consumed_meta)
        meta_reads = tuple(p for p in consumed if p in consumed_meta)
        cache[key] = (_freeze(value), full_reads, meta_reads)
    return value
