#!/usr/bin/env python3
"""Run a test's independent fan-out at once instead of one at a time.

Most of what this suite spends is not computation. A test that checks a rule
holds for every calendar, every language, every registered tool or every
published leaf runs one cold `tpt` per coordinate, and a cold `tpt` is two
interpreters before it reaches the question. Those invocations do not depend on
each other --- that is what makes the loop a matrix rather than a sequence ---
so the waiting can overlap even though the asserting cannot.

`gather` is the whole of it: map a callable over items, keep the results in the
order the items came in, and hand them back. The assertions that follow are
unchanged and still run one at a time, in the same order, so a failure names
the same coordinate and prints the same output as before. Only the waiting is
shared.

Threads rather than processes: every caller here is waiting on
`subprocess.run`, which releases the GIL for the whole wait.

Two rules for using it, both learned the hard way in this repository:

- The work must be independent. Two isolation defects in this suite were
  invisible until tests ran at once --- one planted a colliding workflow id in
  `workflows/pipelines/` and one rewrote a tracked fragment in place --- and
  each then broke whichever unrelated test was reading that file. If the items
  write anywhere but their own sandbox, they are not a fan-out.
- Assert afterwards, never inside. `unittest` assertions raise, and an
  exception inside a worker is a failure attributed to the wrong place. Collect
  first, judge second.
"""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, Sequence, TypeVar

T = TypeVar("T")
R = TypeVar("R")

# Twice the cores: these workers are waiting on child processes rather than
# using a core each, and the suite itself already runs several of these at once.
DEFAULT_WORKERS = (os.cpu_count() or 4) * 2


def gather(
    function: Callable[[T], R],
    items: Iterable[T],
    *,
    workers: int | None = None,
) -> list[R]:
    """`[function(item) for item in items]`, with the waiting overlapped.

    Results keep the order of `items`. An exception raised by `function` for
    one item is re-raised here, as it would have been in the serial loop.
    """
    ordered: Sequence[T] = list(items)
    if len(ordered) < 2:
        return [function(item) for item in ordered]
    limit = workers or min(len(ordered), DEFAULT_WORKERS)
    with ThreadPoolExecutor(max_workers=limit) as pool:
        return list(pool.map(function, ordered))
