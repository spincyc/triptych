#!/usr/bin/env python3
"""Refuse a tree that tracks a path its own ignore rules exclude.

`/build/` has been the first line of `.gitignore` since the repository's first
commit, and twenty-six commits nevertheless committed build output beneath it.
The rule was never wrong and was never enforced. `.gitignore` governs what Git
*adds*; it says nothing about what the index already holds, and `git add -f` is
a one-word override with no second gate behind it. The tree carried the result
for months, and the ignore rule went on reading as though it were true.

This is that second gate. One question, asked of Git rather than of a list:

    git ls-files -c -i --exclude-standard

names every path in the index that the active ignore rules match. It must come
back empty. A non-empty answer names files the repository simultaneously
declares disposable and preserves forever, which is a contradiction it should
not be able to hold quietly.

The check is worth exactly as much as the rules it reads, and `--exclude-standard`
reads `.gitignore` files out of the working tree rather than out of the index.
A partial or sparse checkout can therefore leave a tracked ignore file
unmaterialised, and the check would then pass by never having read the rule
that would have failed it -- the one failure mode a guard must not have. So
every ignore file the index tracks is required to be present before the
question is asked at all: a rule that cannot be read is an error, never a pass.

    python3 scripts/check_tracked_ignored_paths.py

Exit 0 when the index holds nothing the ignore rules match, 1 when it does, and
2 when the check could not be run as specified. Nothing is written, and neither
the index nor the working tree is changed.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PROGRAM = "scripts/check_tracked_ignored_paths.py"

# Matches the root `.gitignore` and any nested one: Git pathspec wildcards are
# not path-separator aware, so a single pattern covers every depth.
IGNORE_FILE_PATHSPEC = "*.gitignore"

# The exceptions `guidance/external-review-handoffs.md` contemplates when it says
# handoff artifacts "are not committed unless the task expressly requires that
# exception". These roots are that exception, exercised deliberately, and the
# test suite depends on it: `test_tracked_agent_handoffs_have_no_protected_text_payload`
# asserts `tracked_files("build/agent-handoffs")` is non-empty, with the docstring
# "Review bundles are tracked downloads, not a bypass around source policy."
#
# They are allowlisted here rather than un-ignored in `.gitignore`, because the
# value of `/build/` is that build output cannot be added by accident; rewriting
# it as `/build/*` plus re-inclusions would hand that back. The narrow list keeps
# `git add` refusing everything under `build/` while letting this check stay
# meaningful about the rest.
#
# Captured content, not reproducible output: browser screenshots and captured
# logs under the handoff trees, and hand-written continuity notes beside them.
# Nothing regenerates these, which is why they are tracked at all.
TRACKED_BY_EXCEPTION = (
    "build/agent-handoffs/",
    "build/agent-continuity/",
    "build/agent-instructions",
)


def partition_by_exception(paths: list[str]) -> tuple[list[str], list[str]]:
    """Split tracked-and-ignored paths into the sanctioned ones and the rest.

    A prefix match is deliberate: the exception is granted to the evidence trees
    as wholes, since a handoff is only intelligible with every file it captured.
    """
    allowed = [p for p in paths if p.startswith(TRACKED_BY_EXCEPTION)]
    return allowed, [p for p in paths if not p.startswith(TRACKED_BY_EXCEPTION)]


def stale_exceptions(allowed: list[str]) -> list[str]:
    """Allowlist entries nothing matches any more.

    An exception that has outlived the files it was written for is a rule that
    can only ever weaken the next check, so name it rather than carry it.
    """
    return [root for root in TRACKED_BY_EXCEPTION
            if not any(p.startswith(root) for p in allowed)]


class GitError(RuntimeError):
    """Git could not answer the question this check is built on."""


def git(repo: Path, *arguments: str) -> str:
    """Run one read-only Git command, or say precisely why it could not run."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:  # git itself is absent
        raise GitError(f"cannot run git: {exc}") from exc
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "no output"
        raise GitError(f"`git {' '.join(arguments)}` failed: {detail}")
    return result.stdout


def nul_separated(output: str) -> list[str]:
    """Paths as Git emits them under `-z`: never quoted, never ambiguous."""
    return [entry for entry in output.split("\0") if entry]


def unreadable_ignore_files(repo: Path, toplevel: Path) -> list[str]:
    """Tracked ignore files this checkout did not materialise.

    Each one is a rule the index says exists and `--exclude-standard` will not
    read, so its absence is the difference between "nothing is ignored and
    tracked" and "nothing that the rules I happened to read would have caught".
    """
    tracked = nul_separated(git(repo, "ls-files", "-z", "--", IGNORE_FILE_PATHSPEC))
    return [relative for relative in tracked if not (toplevel / relative).is_file()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fail when the index tracks a path the ignore rules exclude.",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=REPO,
        help="repository to check (default: the one holding this script)",
    )
    arguments = parser.parse_args(argv)

    try:
        toplevel = Path(git(arguments.repo, "rev-parse", "--show-toplevel").strip())
        unreadable = unreadable_ignore_files(arguments.repo, toplevel)
        if unreadable:
            print(
                f"{PROGRAM}: {len(unreadable)} tracked ignore file(s) are not "
                "present in this checkout, so their rules were never read:",
                file=sys.stderr,
            )
            for relative in unreadable:
                print(f"  {relative}", file=sys.stderr)
            print(
                "\nCheck out the whole repository, or widen the sparse-checkout "
                "patterns to include every tracked ignore file. A rule this "
                "check cannot read is not a rule it may report as satisfied.",
                file=sys.stderr,
            )
            return 2
        tracked_ignored = nul_separated(
            git(arguments.repo, "ls-files", "-z", "-c", "-i", "--exclude-standard")
        )
    except GitError as exc:
        print(f"{PROGRAM}: {exc}", file=sys.stderr)
        return 2

    allowed, offending = partition_by_exception(tracked_ignored)

    # Reported, never fatal, and never before the offences. An exception that
    # matches nothing is untidy; a tracked build artifact is the thing this
    # check exists to catch, and a housekeeping note must not be able to hide
    # one or to fail a tree whose only fault is an allowlist entry left behind.
    for root in stale_exceptions(allowed):
        print(
            f"{PROGRAM}: note: allowlisted exception {root!r} matches no tracked "
            "path; drop it from TRACKED_BY_EXCEPTION once that is deliberate.",
            file=sys.stderr,
        )

    if not offending:
        note = (
            f" {len(allowed)} tracked under the recorded review-evidence exception."
            if allowed
            else ""
        )
        print(
            f"{toplevel}: no tracked path matches the repository's ignore rules"
            f" outside the recorded exceptions.{note}"
        )
        return 0

    print(
        f"{PROGRAM}: {len(offending)} tracked path(s) match the "
        "repository's own ignore rules and are not a recorded exception:",
        file=sys.stderr,
    )
    for relative in offending:
        print(f"  {relative}", file=sys.stderr)
    print(
        "\nEvery one of these was committed through `git add -f`, which "
        "overrides the ignore rule at add time and leaves nothing behind to "
        "catch it afterwards. Untrack them, keeping the working-tree copies:"
        "\n"
        "\n    git rm --cached -- <path>..."
        "\n"
        "\nIf a path genuinely belongs in the repository, narrow the ignore "
        "rule that matches it instead of forcing the add, so the rule and the "
        "index agree.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
