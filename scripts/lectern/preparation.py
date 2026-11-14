"""Check the corpus index once, for the loading screen and the reading session."""
from __future__ import annotations

import asyncio

from .repo import ROOT, Refused


def check_index():
    """Return the checked committed lookup index; refuse a stale or missing one.

    Selected records load when requested. Nothing here repairs the index or
    builds products.
    """
    from _corpus_index import CorpusIndex, CorpusIndexError

    try:
        return CorpusIndex(ROOT)
    except (CorpusIndexError, OSError) as error:
        raise Refused(f"indexed reading data is unavailable: {error}") from error


async def prepare_products() -> None:
    """Check off the event loop, then open the reading session on that check.

    The check is a bounded Git scan with no child producers. Cancelling the
    loading screen stops waiting for it; the scan's result is then discarded.
    """
    from . import bridge

    index = await asyncio.to_thread(check_index)
    bridge.BRIDGE_PROCESS.adopt(index)
