#!/usr/bin/env python3
"""Run the unit-test suite across every core this machine has.

`python -m unittest discover` ran all 127 modules in one process on one
thread. The suite's cost is not arithmetic: it is cold tool invocations and
the processes the tools start to compose each other, so almost every second
was one process waiting on another. That parallelises about as well as work
ever does.

The unit of work is the module; `_units` says why, and what splitting finer
cost when it was measured. Modules here are independent by construction ---
each builds its own `tempfile` sandbox.

Units are dispatched longest-first from the durations of the previous run,
recorded in `build/test-durations.json`. The suite is lopsided enough that
this matters: dispatched alphabetically, the longest unit can be picked up
last and run alone while every other worker has finished.

Running tests at once does not make an isolated test flaky; it reveals a test
that was never isolated. Two here were not, and both are fixed rather than
serialised: one planted a colliding workflow id in `workflows/pipelines/` and
one rewrote a tracked fragment in place, and each broke whichever unrelated
test happened to be reading that file at the time. Prefer finding the third
one to running the suite serially again.

This changes where tests run and nothing about what they assert. Failures and
errors are reported with the same tracebacks `unittest` produces, and `-j1`
runs everything in this process, which is what to use under a debugger.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
import time
import unittest
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tools" / "tests"
DURATIONS = ROOT / "build" / "test-durations.json"


def _units(pattern: str) -> list[str]:
    """Everything to run, as dotted names `unittest` can load.

    The module, not the class and not the test. Splitting by class was tried,
    for the good reason that one module holds the run's longest pole:
    `test_tool_registry` carries the forty shell scripts in one class and a
    hundred registry assertions in others. Measured, it was worse twice over.
    The 118 modules became 502 units whose `setUpClass` fixtures and module
    imports were then built per class rather than per module, and the suite's
    total work rose from 785s to 1194s --- more than the finer split could win
    back. It also broke a test: several workflow classes inherit helpers, and
    a fixture, from classes in *other* modules, and separating them put the
    two halves in different processes with different temporary trees.

    So: modules, which are what the classes in them already assume they share.
    """
    return [
        f"tools.tests.{path.stem}"
        for path in sorted(TESTS.glob(pattern))
        if path.name.startswith("test_")
    ]


def _run_unit(name: str) -> dict:
    """Run one unit here and return only what the parent can pickle.

    A unit that cannot be imported is reported as an error rather than raised,
    so one broken module leaves every other result intact instead of tearing
    down the pool.
    """
    started = time.perf_counter()
    stream = io.StringIO()
    try:
        suite = unittest.defaultTestLoader.loadTestsFromName(name)
    except Exception as error:  # noqa: BLE001 - an unimportable module is a failure
        return {
            "module": name,
            "run": 0,
            "seconds": time.perf_counter() - started,
            "failures": [],
            "errors": [(name, f"could not import {name}: {error!r}")],
            "skipped": 0,
        }
    result = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)
    return {
        "module": name,
        "run": result.testsRun,
        "seconds": time.perf_counter() - started,
        "failures": [(str(test), trace) for test, trace in result.failures],
        "errors": [(str(test), trace) for test, trace in result.errors],
        "skipped": len(result.skipped),
    }


def _recorded_durations() -> dict[str, float]:
    try:
        return json.loads(DURATIONS.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _record_durations(results: list[dict]) -> None:
    try:
        DURATIONS.parent.mkdir(parents=True, exist_ok=True)
        DURATIONS.write_text(
            json.dumps(
                {row["module"]: round(row["seconds"], 3) for row in sorted(
                    results, key=lambda row: row["module"]
                )},
                indent=1,
            ),
            encoding="utf-8",
        )
    except OSError:
        pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="run-tests",
        description="Run tools/tests across every core.",
    )
    parser.add_argument(
        "-j", "--jobs", type=int, default=0,
        help="worker processes; 0 (the default) picks one per core",
    )
    parser.add_argument(
        "-p", "--pattern", default="test_*.py",
        help="which modules to run, as a filename glob",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="also print the slowest modules",
    )
    arguments = parser.parse_args(argv)

    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))

    modules = _units(arguments.pattern)
    if not modules:
        print(f"nothing to run matched {arguments.pattern}", file=sys.stderr)
        return 1

    recorded = _recorded_durations()
    modules.sort(key=lambda name: -recorded.get(name, 0.0))

    jobs = arguments.jobs or min(len(modules), os.cpu_count() or 1)
    started = time.perf_counter()
    if jobs == 1:
        results = [_run_unit(name) for name in modules]
    else:
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            results = list(pool.map(_run_unit, modules))
    elapsed = time.perf_counter() - started

    _record_durations(results)

    failures = [(row["module"], *pair) for row in results for pair in row["failures"]]
    errors = [(row["module"], *pair) for row in results for pair in row["errors"]]
    for kind, rows in (("FAIL", failures), ("ERROR", errors)):
        for module, test, trace in rows:
            print("=" * 70)
            print(f"{kind}: {test}  [{module}]")
            print("-" * 70)
            print(trace)

    if arguments.verbose:
        for row in sorted(results, key=lambda row: -row["seconds"])[:15]:
            print(f"  {row['seconds']:7.2f}s  {row['module']}", file=sys.stderr)

    total = sum(row["run"] for row in results)
    skipped = sum(row["skipped"] for row in results)
    print(
        f"\nRan {total} tests in {elapsed:.2f}s "
        f"({len(modules)} units across {jobs} workers, {skipped} skipped)"
    )
    if failures or errors:
        print(f"FAILED (failures={len(failures)}, errors={len(errors)})")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
