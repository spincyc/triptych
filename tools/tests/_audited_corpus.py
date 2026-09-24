"""The 1962 proper leaves as the 2026-09-24 house-voice audit found them.

Several tests of `check-content-preflight` were written against defects the
published corpus carried: reader-facing sentences whose subject was the guide
or its apparatus, and exploratory proposals that stated no "what the
element-by-element reading misses" field. On 2026-09-24 a maintainer-authorized
audit repaired every proper leaf of both providers, beginning with e8217e665
(gpt 49) and including 6dab788c8 (claude 51), fd53bccbb (claude 53) and
e11d8b618 (gpt 52). From then on a test pinned to a live leaf either failed on
the repair or, reading an empty list of refusals, passed while measuring
nothing.

So the detections are held over the tree at `AUDITED_COMMIT`, whose 1962
propers are byte for byte the ones the first repair started from (the one
commit between them touches only postconciliar leaves), read from history
rather than copied into a fixture
that could drift from it, and the live tree is held to its repaired state by
tests of its own. `tools/tests/test_house_voice.py` and
`tests/tools/check-content-preflight.test` hold an earlier specimen the same
way, and for the same reason.

Only the leaves' own trees and the three shared `src/common` inputs the
schema-2 leaves `\\input` are extracted. The two prose checks, and the edition
graph under them, read nothing else; a check that reads the source library
cannot be run against this tree and is not.
"""

from __future__ import annotations

import io
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

AUDITED_COMMIT = "860d6d902704beb507744a0d0f4e86ff19affa31"
AUDITED_PATHS = (
    "src/common",
    "src/claude/liturgy/roman-rite/1962/propers",
    "src/gpt/liturgy/roman-rite/1962/propers",
)


def audited_tree(case: type[unittest.TestCase]) -> Path:
    """A repository root holding the audited corpus, removed with `case`.

    A checkout without git history skips; a history that has lost the commit
    fails, because it would otherwise measure nothing and say so in green.
    """
    git = ["git", "-C", str(ROOT)]
    if shutil.which("git") is None or subprocess.run(
            [*git, "rev-parse", "--git-dir"], capture_output=True).returncode:
        raise unittest.SkipTest("the audited corpus is read from git history")
    archive = subprocess.run(
        [*git, "archive", "--format=tar", AUDITED_COMMIT, "--",
         *AUDITED_PATHS],
        capture_output=True)
    if archive.returncode:
        raise AssertionError(
            f"the audited corpus is not at {AUDITED_COMMIT}: "
            f"{archive.stderr.decode(errors='replace').strip()}")
    root = Path(tempfile.mkdtemp(prefix="audited-corpus-"))
    case.addClassCleanup(shutil.rmtree, root, ignore_errors=True)
    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as tar:
        tar.extractall(root, filter="data")
    return root
