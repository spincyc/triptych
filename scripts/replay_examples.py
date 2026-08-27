#!/usr/bin/env python3
"""Replay every captured example in tools/ against what its tool prints now.

Each tool's help ends with a transcript under the heading scripts/_tooling.py
owns, which calls the lines below it "real output, captured". Until this ran,
nothing checked that claim: tools/tests/test_tool_registry.py counted lines
beginning with a "$ " prompt, so a transcript could be stale, or composed, and
stay green. Two were. `tpt --list` stopped printing its recorded fourth line at
2a00eeba, and `research-staleness status` recorded 25 stale documents against a
real 51, under a leading identity that was no longer the first one printed.

What a capture may leave out, and what the replay makes of each omission:

    "... N more lines"   the run must print exactly N further lines
    "... [+K chars]"     the line must continue for exactly K more characters
    "<repo>"             stands for this checkout's own path

Everything else is compared literally, digits included. The heading warns that
"counts move with the sources", and they do — but that is a fact about the tree
a capture was taken from, not a licence for the number to be wrong now. When
the sources move, `make recapture-examples` re-runs the invocation and rewrites
the transcript from the run, keeping the elisions the author chose. No line
here is ever edited by hand.

Four declarations narrow the rule, each one naming a single invocation rather
than a tool, and each one printed on every run:

  VOLATILE  a line that varies with the machine and not with the sources, with
            the pattern the run must still match. pdf-review prints the host's
            free memory and core count; nothing else does.
  EXEMPT    an invocation that must not be run: it reaches a model or the
            network, or it writes tracked release state.
  REQUIRES  an invocation whose precondition this checkout may not hold, such
            as a built PDF or the locked dependency set.
  STALE     a transcript already known to be wrong when this landed, with what
            moved. It can only shrink: an entry that starts matching fails.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
COMPANION_SUFFIXES = (".md", ".test")

MORE_LINES = re.compile(r"^\.\.\. (\d+) more lines?$")
CUT_SHORT = re.compile(r"^(.*)\.\.\. \[\+(\d+) chars\]$")
REPO = "<repo>"

# --- Preconditions ---------------------------------------------------------
#
# Several captures were taken in sequence, each one standing on what the last
# wrote: `artwork-library identify build/example-art.png` reads the file the
# normalize example creates, and `citations encode --root build/example-cal`
# wants a copy of the calendars to rewrite. A replay that skipped the setup
# would report a divergence that says nothing about the transcript, so each
# tool's scratch paths are removed and rebuilt before its captures run.
SCRATCH: dict[str, tuple[str, ...]] = {
    "artwork-library": ("build/example-art.png",),
    "calendar-days": ("build/example-days",),
    "calendar-rubrics": ("build/example-web",),
    "citations": ("build/example-cal",),
    "commentary-work-index": ("build/example-corpus.yaml",),
    "document-library": ("build/example-catalogue",),
    "harvest": ("build/example-harvest", "build/example-discovery.yaml"),
    "index-bible": ("build/example-index", "build/example-bibles"),
    "mass-propers": ("build/example-propers",),
    "pdf-review": ("build/example-review",),
    "reading-plan": ("build/example-reading",),
    "render-sanctuary-dictionary": (
        "build/example-sanctuary",
        "build/example-empty-objects",
    ),
    "source-family-migration": ("build/example-migration.toml",),
    "source-inventory": ("build/example-inventory.toml", "build/example-review.toml"),
    "typeset-bible": ("build/example-typeset",),
    "web-edition": ("build/example-web-edition",),
}

PREPARE: dict[str, tuple[object, ...]] = {
    "artwork-library": (
        "tools/artwork-library normalize "
        "src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/shared/artwork/"
        "pencil/ASG-ART-015-lm-elevation-stations.png build/example-art.png",
    ),
    # `check` reads the browser files `structure` writes, and the rubrics it
    # checks are keyed to the day files calendar-days writes beside them.
    "calendar-rubrics": (
        "tools/calendar-days structure --out build/example-web",
        "tools/calendar-rubrics structure --out build/example-web",
    ),
    "citations": (("copy", "src/sources/calendars", "build/example-cal"),),
    # Rebuilding the real ledger needs the table's reviewed identity decisions.
    # Seed the untracked target with that review before the example derives its
    # groups; an empty target can only rediscover the machine edges and must
    # correctly refuse every naming conflict that requires human judgment.
    "harvest": (
        ("mkdir", "build/example-harvest"),
        (
            "copy-file",
            "src/sources/commentary/work-aliases.yaml",
            "build/example-harvest/aliases.yaml",
        ),
    ),
    "render-sanctuary-dictionary": (("mkdir", "build/example-empty-objects"),),
    # The capture records the second run, which is the one that reports
    # `unchanged`; a first render into an empty tree writes instead.
    "typeset-bible": (
        "tools/typeset-bible render --bible clementine-vulgate --out build/example-typeset",
        "tools/typeset-bible render --volume narrative-spine-landmarks-douay-rheims "
        "--out build/example-typeset",
    ),
}

# --- What is never run -----------------------------------------------------
#
# Keyed by the exact invocation, never by tool, so that a verb's siblings stay
# checked. Every entry is printed on every run: an exemption nobody sees is the
# failure this replay exists to end.
EXEMPT: dict[str, str] = {
    "tools/harvest ask --passage 'Psalms 24' --runs 1 --top 5 --out build/example-harvest":
        "calls a model, once a passage a run; the only invocation in tools/ that spends",
    "tools/harvest record --ledger build/example-harvest/ledger.yaml"
    " --results build/example-results.yaml --model claude-opus-5 --audited-on 2026-07-31":
        "reads the results file only `harvest ask` writes, and `ask` calls a model",
    "tools/harvest record --ledger build/example-harvest/ledger.yaml"
    " --results build/example-results.yaml --model claude-opus-5 --audited-on 2026-07-31"
    " --format json":
        "reads the results file only `harvest ask` writes, and `ask` calls a model",
    "tools/knox-bible fetch --root build/knox":
        "the one verb that opens a socket; it refuses this root before fetching, but a "
        "replay must not be one edit away from retrieving licensed text",
    "tools/release-bindings refresh":
        "rewrites tracked release/ bindings, which the deploy requires to be exact",
    "tools/release-bindings migrate-publications":
        "rewrites tracked release/publications records whenever one is in an older shape",
}

# --- What this checkout may not be able to run -----------------------------
#
# Not an exemption: the invocation is replayed wherever its precondition holds,
# and reported by name wherever it does not.
REQUIRES: dict[str, tuple[str, str]] = {
    "tools/artwork-library check-pdf build/core-last-20.pdf": (
        "path:build/core-last-20.pdf",
        "a built PDF; no target produces this one, so a fresh clone has no copy",
    ),
    "tools/artwork-library check-pdf --strict-review-triggers build/core-last-20.pdf": (
        "path:build/core-last-20.pdf",
        "a built PDF; no target produces this one, so a fresh clone has no copy",
    ),
    "tools/pdf-review --output build/example-review build/core-last-20.pdf": (
        "path:build/core-last-20.pdf",
        "a built PDF; no target produces this one, so a fresh clone has no copy",
    ),
    "tools/public-alpha build --preview": (
        "pins:requirements-public-alpha.txt",
        "the locked renderer; public-alpha refuses to build against any other version",
    ),
    "tools/public-alpha verify --preview": (
        "pins:requirements-public-alpha.txt",
        "the locked renderer; the tree to verify is the one `build --preview` writes",
    ),
    "tools/public-alpha verify --preview --deployment-target github-pages": (
        "pins:requirements-public-alpha.txt",
        "the locked renderer; the refusal is raised after the renderer check",
    ),
}

# --- Lines that vary with the machine --------------------------------------
#
# One line at a time, with the shape it must still hold. A pattern that matched
# anything would be an exemption wearing a regex, so each one pins every field
# that is not a property of this host.
HOST_PLAN = (
    re.compile(
        r"^pdf-review: host-available=[\d.]+ GiB, cgroup-headroom=\S+, "
        r"effective=[\d.]+ GiB, reserve=1\.00 GiB, per-worker=1\.00 GiB, "
        r"cpu-cap=\d+, jobs=\d+(, workers=\d+)?$"
    ),
    "free memory and core count are facts about the host, not the sources",
)

VOLATILE: dict[str, dict[int, tuple[re.Pattern[str], str]]] = {
    "tools/pdf-review --explain": {1: HOST_PLAN},
    "tools/pdf-review --output build/example-review build/core-last-20.pdf": {1: HOST_PLAN},
}


# --- Transcripts already known to be stale ---------------------------------
#
# A debt list, not an exemption list, and the difference is enforced: an entry
# whose invocation starts matching again is a failure telling you to delete it,
# so this table can only shrink. Every entry is printed on every run with what
# moved, and `scripts/replay_examples.py --recapture --tool <id>` is how one
# leaves.
#
# This table is empty after the complete-Missal recovery: the stale projections,
# alias review, and changed tool behavior were all reconciled before recapture.
STALE: dict[str, str] = {}


@dataclass(frozen=True)
class Capture:
    """One recorded invocation, and where its transcript sits in the source."""

    tool: str
    verb: str
    command: str
    output: tuple[str, ...]
    note: str
    line: int
    span: tuple[int, int] | None
    indent: int

    @property
    def label(self) -> str:
        return f"{self.tool}:{self.line} $ {self.command}"


@dataclass
class Result:
    capture: Capture
    status: str
    problems: tuple[str, ...] = ()
    reason: str = ""
    seconds: float = 0.0
    actual: tuple[str, ...] = ()
    exit_status: int = 0


def tool_paths() -> list[Path]:
    return [
        path
        for path in sorted(TOOLS.iterdir())
        if path.is_file() and not path.name.endswith(COMPANION_SUFFIXES)
    ]


def captures_of(path: Path) -> list[Capture]:
    """Read EXAMPLES out of a tool without importing it.

    Parsing rather than importing keeps the replay from running module-level
    code in twenty-nine tools to find out what they claim to print.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"))
    declared = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            getattr(target, "id", None) == "EXAMPLES" for target in node.targets
        ):
            declared = node.value
    if declared is None:
        raise AssertionError(f"{path.name}: no EXAMPLES table")
    if not isinstance(declared, ast.Dict):
        raise AssertionError(f"{path.name}: EXAMPLES is not a mapping of verb to examples")

    found: list[Capture] = []
    for key_node, value_node in zip(declared.keys, declared.values):
        verb = ast.literal_eval(key_node)
        if not isinstance(value_node, ast.Tuple):
            raise AssertionError(f"{path.name}: EXAMPLES[{verb!r}] is not a tuple")
        for call in value_node.elts:
            if not (isinstance(call, ast.Call) and getattr(call.func, "id", "") == "Example"):
                raise AssertionError(f"{path.name}: EXAMPLES[{verb!r}] holds a non-Example")
            positional = list(call.args)
            keyword = {word.arg: word.value for word in call.keywords}
            command_node = positional[0] if positional else keyword["command"]
            output_node = (
                positional[1] if len(positional) > 1 else keyword.get("output")
            )
            note_node = positional[2] if len(positional) > 2 else keyword.get("note")
            found.append(
                Capture(
                    tool=path.name,
                    verb=verb,
                    command=ast.literal_eval(command_node),
                    output=tuple(ast.literal_eval(output_node)) if output_node else (),
                    note=ast.literal_eval(note_node) if note_node else "",
                    line=call.lineno,
                    span=(
                        (output_node.lineno, output_node.end_lineno)
                        if output_node is not None
                        else None
                    ),
                    indent=output_node.col_offset if output_node is not None else 0,
                )
            )
    return found


def captures(names: list[str] | None = None) -> list[Capture]:
    found: list[Capture] = []
    for path in tool_paths():
        if names and path.name not in names:
            continue
        found.extend(captures_of(path))
    return found


def run(command: str) -> tuple[list[str], int]:
    """Run one invocation and return what a terminal would have shown.

    stderr is merged into stdout because that is what the captures hold: half
    of them are refusals, and a refusal that printed to stderr sits in the
    transcript exactly where the terminal put it. COLUMNS is pinned because
    argparse wraps to it, and several captures are `--help` output.
    """
    completed = subprocess.run(
        shlex.split(command),
        cwd=ROOT,
        env={**os.environ, "COLUMNS": "80", "LC_ALL": "C.UTF-8", "TZ": "UTC"},
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=900,
    )
    text = completed.stdout
    if not text:
        return [], completed.returncode
    lines = text[:-1].split("\n") if text.endswith("\n") else text.split("\n")
    return lines, completed.returncode


def compare(capture: Capture, actual: list[str]) -> list[str]:
    volatile = VOLATILE.get(capture.command, {})
    problems: list[str] = []
    for index, recorded in enumerate(capture.output):
        line = recorded.replace(REPO, str(ROOT))
        more = MORE_LINES.match(line)
        if more:
            remaining = len(actual) - index
            if remaining != int(more.group(1)):
                problems.append(
                    f"line {index + 1}: the transcript ends claiming {more.group(1)} "
                    f"more line(s); the run printed {remaining}"
                )
            return problems
        if index >= len(actual):
            problems.append(
                f"line {index + 1}: recorded {line!r}, but the run stopped printing"
            )
            return problems
        declared = volatile.get(index + 1)
        if declared is not None:
            pattern, reason = declared
            if not pattern.search(actual[index]):
                problems.append(
                    f"line {index + 1}: declared volatile ({reason}) but the run's line "
                    f"no longer matches the declared shape: {actual[index]!r}"
                )
            continue
        cut = CUT_SHORT.match(line)
        if cut:
            head, dropped = cut.group(1), int(cut.group(2))
            if not actual[index].startswith(head):
                problems.append(
                    f"line {index + 1}: recorded {line!r}\n"
                    f"{' ' * 12}the run printed {actual[index][:len(head)]!r}"
                )
            elif len(actual[index]) - len(head) != dropped:
                problems.append(
                    f"line {index + 1}: recorded a line cut at +{dropped} chars; "
                    f"the run's line continues for {len(actual[index]) - len(head)}"
                )
            continue
        if actual[index] != line:
            problems.append(
                f"line {index + 1}: recorded {line!r}\n"
                f"{' ' * 12}the run printed {actual[index]!r}"
            )
    if len(actual) > len(capture.output):
        problems.append(
            f"the run printed {len(actual) - len(capture.output)} line(s) beyond the "
            f"{len(capture.output)} recorded, and nothing said the transcript was cut"
        )
    return problems


def unmet(requirement: str) -> bool:
    kind, _, value = requirement.partition(":")
    if kind == "path":
        return not (ROOT / value).exists()
    if kind == "pins":
        return not pins_installed(ROOT / value)
    raise AssertionError(f"unknown requirement kind: {requirement}")


def pins_installed(requirements: Path) -> bool:
    from importlib import metadata

    for raw in requirements.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or "==" not in line:
            continue
        name, _, wanted = line.partition("==")
        try:
            if metadata.version(name.strip()) != wanted.strip():
                return False
        except metadata.PackageNotFoundError:
            return False
    return True


def prepare(tool: str) -> None:
    for relative in SCRATCH.get(tool, ()):
        target = ROOT / relative
        shutil.rmtree(target, ignore_errors=True)
        target.unlink(missing_ok=True)
    for step in PREPARE.get(tool, ()):
        if isinstance(step, tuple) and step[0] == "copy":
            shutil.copytree(ROOT / step[1], ROOT / step[2])
        elif isinstance(step, tuple) and step[0] == "copy-file":
            shutil.copy2(ROOT / step[1], ROOT / step[2])
        elif isinstance(step, tuple) and step[0] == "mkdir":
            (ROOT / step[1]).mkdir(parents=True, exist_ok=True)
        else:
            run(str(step))


def tracked_differences() -> set[str]:
    """Every tracked path that differs from HEAD, staged or not.

    `git status --porcelain` also reports the untracked output these examples
    write under build/, and folds a rename into one line with an arrow in it.
    This asks the narrower question a mutation guard needs.
    """
    found: set[str] = set()
    for staged in ([], ["--cached"]):
        result = subprocess.run(
            ["git", "diff", "--name-only", "--no-renames", "-z"] + staged,
            cwd=ROOT, capture_output=True, text=True,
        )
        found.update(name for name in result.stdout.split("\0") if name)
    return found


class TrackedGuard:
    """Undo, and attribute, a write an example makes to tracked state.

    Half of these invocations write. Every one was captured against a scratch
    path under build/, and the ones that would rewrite tracked release bindings
    are in EXEMPT — but that is a claim about the transcripts, and this is what
    holds it. Checking once at the end of the run named the paths without naming
    the invocation that wrote them, and left the tree dirty for whoever ran it;
    it also compared `git status` lines, so a second write to a file that was
    already modified moved no line and was invisible.

    Asking after every example gives the invocation away and bounds the damage
    to one of them. The bytes of what is already dirty are recorded up front, so
    a file carrying someone's uncommitted work is put back as it was rather than
    reverted to HEAD.
    """

    def __init__(self) -> None:
        self.dirty = tracked_differences()
        self.recorded = {name: self.content(name) for name in self.dirty}

    @staticmethod
    def content(name: str) -> bytes | None:
        path = ROOT / name
        return path.read_bytes() if path.is_file() else None

    def wrote(self) -> list[str]:
        """The tracked paths written since the last ask, restored to what they were."""
        touched = sorted(
            (tracked_differences() - self.dirty)
            | {name for name in self.dirty if self.content(name) != self.recorded[name]}
        )
        for name in touched:
            if name in self.dirty:
                path = ROOT / name
                if self.recorded[name] is None:
                    path.unlink(missing_ok=True)
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(self.recorded[name])
            else:
                # It matched HEAD before this example ran, so HEAD is what it was.
                subprocess.run(
                    ["git", "checkout", "--", name],
                    cwd=ROOT, capture_output=True,
                )
        return touched


def replay(names: list[str] | None = None, *, echo: bool = False) -> list[Result]:
    guard = TrackedGuard()
    results: list[Result] = []
    for path in tool_paths():
        if names and path.name not in names:
            continue
        prepare(path.name)
        written = guard.wrote()
        if written:
            raise SystemExit(
                f"replay-examples: preparing {path.name} wrote tracked state, which "
                "PREPARE may not do; the writes were undone:\n  " + "\n  ".join(written)
            )
        for capture in captures_of(path):
            result = replay_one(capture)
            written = guard.wrote()
            if written:
                result.status = "wrote-tracked"
                result.problems = tuple(
                    f"wrote tracked {name} (undone)" for name in written
                )
            results.append(result)
            if echo:
                print(rendered(results[-1]), flush=True)
    return results


def replay_one(capture: Capture) -> Result:
    exempt = EXEMPT.get(capture.command)
    if exempt:
        return Result(capture, "exempt", reason=exempt)
    required = REQUIRES.get(capture.command)
    if required and unmet(required[0]):
        return Result(capture, "not-run", reason=f"{required[1]} ({required[0]})")
    started = time.monotonic()
    try:
        actual, exit_status = run(capture.command)
    except subprocess.TimeoutExpired:
        return Result(capture, "diverged", problems=("the run did not finish in 900s",))
    elapsed = time.monotonic() - started
    problems = compare(capture, actual)
    known = STALE.get(capture.command)
    if known:
        status = "stale" if problems else "recovered"
    else:
        status = "diverged" if problems else "match"
    return Result(
        capture,
        status,
        problems=tuple(problems),
        reason=known or "",
        seconds=elapsed,
        actual=tuple(actual),
        exit_status=exit_status,
    )


def rendered(result: Result) -> str:
    mark = {
        "match": "  ok    ",
        "diverged": "  DIFF  ",
        "stale": "  stale ",
        "recovered": "  FIXED ",
        "exempt": "  exempt",
        "not-run": "  absent",
        "wrote-tracked": "  WROTE ",
    }[result.status]
    return f"{mark}  {result.capture.command}"


# --- Recapture -------------------------------------------------------------


def recaptured(capture: Capture, actual: list[str]) -> list[str]:
    """The new transcript: this run's lines, cut where the old one cut them.

    The elisions are the author's editorial judgement about what a reader needs
    to see, so they survive; only what the tool prints is refreshed.
    """
    fresh: list[str] = []
    for index, recorded in enumerate(capture.output):
        more = MORE_LINES.match(recorded)
        if more:
            remaining = len(actual) - index
            if remaining > 0:
                fresh.append(f"... {remaining} more line" + ("s" if remaining != 1 else ""))
            return fresh
        if index >= len(actual):
            return fresh
        line = actual[index]
        cut = CUT_SHORT.match(recorded)
        if cut:
            # The width is measured on the real line, so that "[+K chars]" counts
            # what the tool printed rather than what the redaction shortened.
            width = len(cut.group(1).replace(REPO, str(ROOT)))
            if len(line) > width:
                shown = line[:width].replace(str(ROOT), REPO)
                fresh.append(f"{shown}... [+{len(line) - width} chars]")
                continue
        fresh.append(line.replace(str(ROOT), REPO))
    fresh.extend(line.replace(str(ROOT), REPO) for line in actual[len(capture.output):])
    return fresh


def names_a_sibling(capture: Capture, lines: list[str]) -> str:
    """A sibling id the new transcript would introduce into the tool's body.

    tmt reads a bare sibling id anywhere in a tool as an undeclared dependency,
    so a refreshed transcript that happens to print one turns `tmt check` red
    with a message about `requires` that has nothing to do with the change.
    Cutting the transcript a line earlier is the fix, and that is a decision for
    whoever is recapturing rather than something to write and leave behind.
    """
    siblings = {path.name for path in tool_paths()} - {capture.tool}
    before = "\n".join(capture.output)
    after = "\n".join(lines)
    for sibling in sorted(siblings):
        pattern = re.compile(rf"(?<![\w-]){re.escape(sibling)}(?![\w-])")
        if pattern.search(after) and not pattern.search(before):
            return sibling
    return ""


def rewrite(capture: Capture, lines: list[str]) -> None:
    if capture.span is None:
        raise AssertionError(
            f"{capture.label}: the capture records no output, so there is nothing to "
            "rewrite; add the transcript by hand from a real run"
        )
    path = TOOLS / capture.tool
    source = path.read_text(encoding="utf-8").splitlines(keepends=True)
    pad = " " * capture.indent
    body = [f"{pad}(\n"]
    body.extend(f"{pad}    {json.dumps(line, ensure_ascii=False)},\n" for line in lines)
    body.append(f"{pad}),\n")
    # The span covers the tuple; the trailing comma that follows it in the call
    # is on the closing line, and the rendered block above restores it.
    start, end = capture.span
    tail = source[end - 1].rstrip("\n")
    if not tail.rstrip().endswith(","):
        body[-1] = f"{pad})\n"
    path.write_text(
        "".join(source[: start - 1] + body + source[end:]), encoding="utf-8"
    )


def recapture(names: list[str] | None = None, *, accept_failing: bool = False) -> int:
    """Rewrite diverged transcripts from real runs, to a fixed point.

    A `--help` capture contains its own tool's transcripts, so refreshing one
    can change what another prints; the loop settles that rather than leaving
    the second pass for whoever runs the check next.
    """
    changed_total = 0
    for attempt in range(5):
        changed = 0
        for path in tool_paths():
            if names and path.name not in names:
                continue
            prepare(path.name)
            # One rewrite moves every later capture in the file, so each is
            # located again by position rather than written from a stale span.
            pending = [
                position
                for position, one in enumerate(captures_of(path))
                if replay_one(one).status == "diverged"
            ]
            for position in pending:
                capture = captures_of(path)[position]
                result = replay_one(capture)
                if result.status != "diverged":
                    continue
                fresh = recaptured(capture, list(result.actual))
                if list(capture.output) == fresh:
                    print(f"  unfixable  {capture.label}")
                    for problem in result.problems:
                        print(f"             {problem}")
                    continue
                # A transcript refreshed from a command that now fails is the
                # one case where recapture can turn a caught regression into a
                # documented one: the check goes green and the tool stays
                # broken. It has already nearly happened — a model change made
                # `calendar-rubrics check` fail its own solved case, and the
                # refreshed transcript recorded the failure as the expectation.
                #
                # Half these captures are refusals and legitimately exit
                # non-zero, so this cannot simply refuse. It makes the operator
                # say so, which is the difference between a refusal that is the
                # point and one that is the news.
                if result.exit_status != 0 and not accept_failing:
                    print(
                        f"  refused    {capture.label}\n"
                        f"             the command now exits {result.exit_status}; recording that "
                        f"would make the transcript expect a failure.\n"
                        f"             Fix the tool, or rerun with --accept-failing if the "
                        f"refusal is what the example shows."
                    )
                    continue
                sibling = names_a_sibling(capture, fresh)
                if sibling:
                    print(
                        f"  refused    {capture.label}\n"
                        f"             the refreshed transcript prints {sibling!r}, and "
                        f"tmt reads a bare sibling id in a tool body as an undeclared\n"
                        f"             dependency; end the transcript before that line "
                        f"and run this again"
                    )
                    continue
                rewrite(capture, fresh)
                print(f"  recaptured {capture.label}")
                changed += 1
        changed_total += changed
        if not changed:
            break
        print(f"pass {attempt + 1}: {changed} transcript(s) rewritten")
    return changed_total


# --- Reporting -------------------------------------------------------------


def report(results: list[Result], *, stream=sys.stdout) -> int:
    diverged = [r for r in results if r.status == "diverged"]
    recovered = [r for r in results if r.status == "recovered"]
    stale = [r for r in results if r.status == "stale"]
    exempt = [r for r in results if r.status == "exempt"]
    absent = [r for r in results if r.status == "not-run"]
    wrote = [r for r in results if r.status == "wrote-tracked"]
    volatile = sum(len(lines) for lines in VOLATILE.values())

    if wrote:
        print(
            "\nwrote tracked state, which no capture may do; the writes were undone:",
            file=stream,
        )
        for result in wrote:
            print(f"  $ {result.capture.command}", file=stream)
            for problem in result.problems:
                print(f"    {problem}", file=stream)

    for result in diverged:
        print(f"\n{result.capture.label}", file=stream)
        for problem in result.problems:
            print(f"    {problem}", file=stream)
    for result in recovered:
        print(
            f"\n{result.capture.label}\n    this transcript replays exactly again; "
            f"drop it from STALE in scripts/replay_examples.py\n    (recorded as: "
            f"{result.reason})",
            file=stream,
        )

    if stale:
        print("\nknown stale, replayed and still diverging:", file=stream)
        for result in stale:
            print(f"  $ {result.capture.command}", file=stream)
            print(f"    {result.reason}", file=stream)
    if exempt:
        print("\nnever replayed, by invocation:", file=stream)
        for result in exempt:
            print(f"  $ {result.capture.command}", file=stream)
            print(f"    {result.reason}", file=stream)
    if absent:
        print("\nnot runnable in this checkout:", file=stream)
        for result in absent:
            print(f"  $ {result.capture.command}", file=stream)
            print(f"    {result.reason}", file=stream)

    print(
        f"\nreplay-examples: {len(results)} captured example(s); "
        f"{len(results) - len(exempt) - len(absent)} replayed, "
        f"{len(diverged) + len(recovered)} diverged, {len(stale)} known stale, "
        f"{len(exempt)} never run, {len(absent)} unrunnable here, "
        f"{len(wrote)} wrote tracked state, "
        f"{volatile} volatile line(s) declared",
        file=stream,
    )
    return 1 if diverged or recovered or wrote else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="replay-examples",
        description="Replay the captured examples in tools/ against real runs.",
    )
    parser.add_argument("--tool", action="append", dest="tools", metavar="ID")
    parser.add_argument(
        "--accept-failing",
        action="store_true",
        help="recapture a transcript even where the command now exits non-zero",
    )
    parser.add_argument("--json", action="store_true", help="one object per example")
    parser.add_argument(
        "--recapture",
        action="store_true",
        help="rewrite diverged transcripts in place from real runs",
    )
    arguments = parser.parse_args(argv)

    if arguments.recapture:
        return 0 if recapture(arguments.tools, accept_failing=arguments.accept_failing) >= 0 else 1

    results = replay(arguments.tools, echo=not arguments.json)
    if arguments.json:
        print(
            json.dumps(
                [
                    {
                        "tool": r.capture.tool,
                        "verb": r.capture.verb,
                        "command": r.capture.command,
                        "status": r.status,
                        "reason": r.reason,
                        "problems": list(r.problems),
                        "seconds": round(r.seconds, 2),
                    }
                    for r in results
                ],
                ensure_ascii=False,
                indent=1,
            )
        )
        return 1 if any(r.status in ("diverged", "recovered") for r in results) else 0
    return report(results)


if __name__ == "__main__":
    raise SystemExit(main())
