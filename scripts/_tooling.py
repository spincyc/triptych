#!/usr/bin/env python3
"""Shared CLI launcher helpers for top-level repository tools."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import sys
import unicodedata
from typing import Callable, NamedTuple, Sequence

PROTOCOL_VERSION = 1

CommandHandler = Callable[[argparse.Namespace], object]
OutputRenderer = Callable[[object, argparse.Namespace], int]

# A transcript that has been shortened must say so in the transcript itself,
# or a reader counts four lines of output where the tool printed four hundred.
# Two markers, both counted rather than vague:
#   "... 396 more lines"   dropped lines
#   "... [+2314 chars]"    one line cut short
ELISION = "..."

# One heading, so a reader who has seen one tool's examples recognizes every
# other tool's, and so a test can find the section without parsing prose.
#
# The heading no longer says "real output, captured", because the help page no
# longer prints the output. The capture is still real and still captured — it
# is held in each tool's EXAMPLES table and replayed line for line by
# scripts/replay_examples.py, which is the only thing that ever proved the
# claim. What changed is who reads it: a reader opening `--help` wants the
# command to copy, and printing 25 lines of transcript under each of a verb's
# two examples buried the verb list under a page of output. The transcript is
# data for the replay; the help page is for the reader.
HEADING = "examples (real invocations; `make check-examples` replays each one):"


# --- The tool listing's grouping -------------------------------------------
#
# Twenty-nine tools in one alphabetical column told a reader nothing about what
# any of them was for, so `tpt --list` prints them by purpose.
#
# The table lives here, outside tools/, for two reasons that between them rule
# out every other home. It cannot be a `group` field in tmt.json, because tmt
# validates each registry entry against a closed key set — purpose, stage,
# usage, config, idempotent, json, lang, mutates, origin, requires — and an
# unknown key is a hard failure:
#
#     FAIL registry: tools['tpt'].group: unknown key
#
# And it cannot sit in tools/tpt, because tmt reads a bare sibling id in a tool
# body as an undeclared dependency, so a table naming all twenty-nine would
# make the launcher claim to depend on every one of them:
#
#     FAIL tpt: uses sibling 'harvest' without declaring it in requires
#
# So this is the one table. `tpt --check` proves it names every registered id
# exactly once, which is what stops it drifting from the registry it describes.
GROUPS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    (
        "acquisition",
        "Retrieval from outside the project. This is the only group that "
        "reaches outside your machine at all, and no tool in any other group "
        "makes a network call or calls a model. knox-bible fetches licensed "
        "text and what it writes never enters the repository: every verb of it "
        "refuses a destination inside this checkout. harvest spends on a model "
        "in one verb, `ask`, and what comes back lands in a dated ledger that "
        "records which model said it and when.",
        ("harvest", "knox-bible"),
    ),
    (
        "scripture",
        "The biblical text, the citations that address it, the commentary "
        "keyed to those citations, and when the text and its events are dated.",
        (
            "citations",
            "commentary-work-index",
            "index-bible",
            "reading-plan",
            "scripture-chronology",
            "typeset-bible",
        ),
    ),
    (
        "calendar",
        "The liturgical calendars, their precedence rules, and the masses "
        "they carry.",
        (
            "act-history",
            "audit-latin-body-substitutions",
            "calendar-days",
            "calendar-rubrics",
            "calendar-spine",
            "check-calendar-masses",
            "check-content-preflight",
            "check-proper-components",
            "check-proper-identity",
            "mass-ordinary",
            "mass-propers",
            "mass-today",
            "proper-chronology",
        ),
    ),
    (
        "sources",
        "Where a publication's material came from, and whether the research "
        "behind it is still current.",
        (
            "research-staleness",
            "source-family-migration",
            "source-inventory",
            "source-library",
            "source-reader",
        ),
    ),
    (
        "artwork",
        "Repository-owned publishing artwork and the pictorial dictionaries "
        "that draw on it.",
        (
            "artwork-library",
            "check-roman-sanctuary-artwork",
            "render-sanctuary-dictionary",
            "source-first-cartographic-artwork",
        ),
    ),
    (
        "release",
        "Building, validating and publishing what a reader actually sees.",
        (
            "check-curriculum-structure",
            "check-generation-metadata",
            "check-promised-deliverables",
            "check-web-edition",
            "complete-missal",
            "document-library",
            "pdf-review",
            "public-alpha",
            "release-bindings",
            "web-edition",
        ),
    ),
    (
        "launcher",
        "Finding and running the tools themselves.",
        ("tpt",),
    ),
)

GROUP_OF = {name: group for group, _, names in GROUPS for name in names}


# --- What each tool reaches ------------------------------------------------
#
# A reader deciding whether to run something wants one question answered before
# any other: does this spend anything outside my machine? Two ways it could —
# a network call, or a model — so each tool declares which, and the honest
# current answer is that exactly one does either, and both sit in the same
# group so the listing answers the question by where a tool appears.
#
# `knox-bible` is the only tool that opens a socket: it retrieves the licensed
# Knox text from its publisher, one chapter a request, and refuses to write
# anywhere inside the repository. Nothing else in tools/ contains urlopen,
# urllib.request, a requests call, http.client or a socket.
#
# `harvest` is the only tool that calls a model, and only in its `ask` verb,
# which runs the `claude` CLI once per passage per run. Everything else it does
# reads the ledger `ask` feeds. Until 2026-07-31 it called nothing: the harvest
# ran outside it and `record --model ... --audited-on ...` stamped a run with
# whatever an operator typed. Moving the call inside is what lets both stamps be
# taken from the answer instead of asserted about it.
#
# This lives beside GROUPS, and for the same reason: tmt.json's entry keys are
# a closed set, so a `reaches` field there is a hard `tmt check` failure. The
# declaration is only worth as much as the check behind it, and that check is
# in tools/tests/test_tool_registry.py, which greps each tool for the call
# patterns above and fails when a body and its declaration disagree.
NETWORK = "network"
MODEL = "model"
NOTHING = "nothing"

REACHES: dict[str, str] = {
    "act-history": NOTHING,
    "artwork-library": NOTHING,
    "audit-latin-body-substitutions": NOTHING,
    "calendar-days": NOTHING,
    "calendar-rubrics": NOTHING,
    "calendar-spine": NOTHING,
    "check-calendar-masses": NOTHING,
    "check-content-preflight": NOTHING,
    "check-curriculum-structure": NOTHING,
    "check-generation-metadata": NOTHING,
    "check-promised-deliverables": NOTHING,
    "check-proper-components": NOTHING,
    "check-proper-identity": NOTHING,
    "check-roman-sanctuary-artwork": NOTHING,
    "check-web-edition": NOTHING,
    "citations": NOTHING,
    "commentary-work-index": NOTHING,
    "complete-missal": NOTHING,
    "document-library": NOTHING,
    "harvest": MODEL,
    "index-bible": NOTHING,
    "knox-bible": NETWORK,
    "mass-ordinary": NOTHING,
    "mass-propers": NOTHING,
    "mass-today": NOTHING,
    "pdf-review": NOTHING,
    "proper-chronology": NOTHING,
    "public-alpha": NOTHING,
    "reading-plan": NOTHING,
    "release-bindings": NOTHING,
    "render-sanctuary-dictionary": NOTHING,
    "research-staleness": NOTHING,
    "scripture-chronology": NOTHING,
    "source-family-migration": NOTHING,
    "source-first-cartographic-artwork": NOTHING,
    "source-inventory": NOTHING,
    "source-library": NOTHING,
    "source-reader": NOTHING,
    "tpt": NOTHING,
    "typeset-bible": NOTHING,
    "web-edition": NOTHING,
}

REACH_LABEL = {
    NETWORK: "reaches the network",
    MODEL: "calls a model",
    NOTHING: "",
}


class Example(NamedTuple):
    """One invocation that was actually run, with what it actually printed.

    ``output`` holds captured lines verbatim, in the order a terminal shows
    them, with the two ELISION markers above as the only permitted edits. No
    line may be composed: help text that shows output the tool does not
    produce is worse than help text with no example at all.

    ``note`` carries the one thing a transcript cannot show — that the verb
    writes, what it wrote, or which precondition the invocation assumed.
    """

    command: str
    output: Sequence[str] = ()
    note: str = ""


def format_examples(
    examples: Sequence[Example],
    *,
    unavailable: str = "",
) -> str:
    """Render examples as an argparse epilog.

    ``unavailable`` replaces the transcript when no invocation can honestly be
    shown here — a licensed root this repository may not hold, or a network
    fetch. Saying so plainly beats inventing a command.
    """
    lines = [HEADING]
    if unavailable:
        lines.append("  no runnable example: " + unavailable.strip())
        if not examples:
            return "\n".join(lines)
        lines.append("")
    for example in examples:
        lines.append(f"  $ {example.command}")
        # The note is the one thing the transcript could never show — that the
        # verb writes, what it wrote, which precondition it assumed — so it
        # stays where the reader is looking. The transcript itself does not:
        # it is captured, stored and replayed, and reprinting it here made the
        # help page a wall of output nobody asked for.
        if example.note:
            lines.append(f"    ({example.note})")
        if not example.output:
            lines.append("    (prints nothing)")
    return "\n".join(lines)


def with_examples(
    parser: argparse.ArgumentParser,
    examples: Sequence[Example] = (),
    *,
    unavailable: str = "",
) -> argparse.ArgumentParser:
    """Attach captured examples to ``parser`` and return it.

    Kept in the shared launcher module so that the shape of an example is
    decided once rather than reinvented in each tool.
    """
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.epilog = format_examples(examples, unavailable=unavailable)
    return parser


def examples_live_on_the_verbs(
    parser: argparse.ArgumentParser,
    prog: str,
) -> argparse.ArgumentParser:
    """Point a verb-bearing tool's top-level help at its per-verb examples.

    Repeating every verb's transcript here would bury the verb list under a
    page of output, and the reader who wants an example wants one verb's.
    """
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.epilog = (
        f"{HEADING}\n"
        f"  each verb carries its own, run against this repository:\n"
        f"    $ {prog} <verb> --help"
    )
    return parser


# --- What the far end can actually show ------------------------------------
#
# Until this existed, nothing in this module asked. `mass-today show` prints
# nine em-dashes and five ellipses for a single Sunday, and it printed them at
# a VT100, into a pipe, and into a file under an ASCII locale alike: mojibake
# in the first case and a UnicodeEncodeError in the last. Neither was
# hypothetical and neither was any tool's own fault, because the question —
# what can the stream on the other end carry — is a property of the run and
# not of the tool. So it is answered once, here, for all of them.
#
# THREE TIERS, and what decides each:
#
#   plain    ASCII and nothing else. `V.` and `R.`, `--`, `...`, no colour.
#            Reached by `--plain` REGARDLESS OF DETECTION, because detection
#            is a guess and an operator who says plain means plain; and
#            reached by detection when the stream's encoding cannot carry the
#            glyphs, or when a terminal advertises no capabilities at all.
#   unicode  The glyphs, decided by the STREAM'S ENCODING and not by TERM: a
#            UTF-8 pipe into a file carries ℣ perfectly well with no terminal
#            at the other end at all.
#   rich     Headings, rules and colour, when the stream is a tty AND the
#            terminal names itself. Colour honours NO_COLOR, and is never the
#            only carrier of meaning: every distinction it draws is also drawn
#            in words, so a monochrome reader loses decoration and no fact.
#
# THE MACHINE PATHS ARE UNTOUCHED. `--json` is a contract other tools consume
# and `--format yaml` is read by programs; both bypass this entirely, so their
# bytes do not move with the terminal they happen to be printed at.
PLAIN, UNICODE, RICH = "plain", "unicode", "rich"
STYLES = ("auto", PLAIN, UNICODE, RICH)

# The fold, written down rather than computed, because "what does this
# character become without Unicode" is an editorial decision per character and
# a decomposition would silently drop the ones that carry meaning. Every entry
# is a character these tools or these sources actually print; the census that
# produced the list ran over tools/ and over the served structure files.
FOLD = {
    "—": "--",   # em dash, the separator this project's output leans on
    "–": "-",
    "…": "...",
    "‘": "'",
    "’": "'",
    "“": '"',
    "”": '"',
    " ": " ",
    "·": "-",    # the middle dot used between fields
    "§": "sec.",
    "¶": "para.",
    "©": "(c)",
    "†": "+",    # dagger
    "‡": "++",
    "✠": "+",    # the maltese cross of a blessing
    "☧": "Chi-Rho",
    "→": "->",
    "‹": "<",
    "›": ">",
    "æ": "ae",
    "Æ": "AE",
    "œ": "oe",
    "Œ": "OE",
    "℣": "V.",   # ℣ and ℟ are introduced by the tiers above, and fold
    "℟": "R.",   # back to the letters the book itself prints
    "ℤ": "V.",
}

VERSICLE = "℣"
RESPONSE = "℟"

# Colour, by role rather than by hue, so a caller names what a thing IS.
_SGR = {
    "heading": "1",       # bold
    "rule": "2",          # dim
    "note": "2",
    "said": "1",
    "withheld": "3",      # italic where the terminal has it
}


def fold_to_ascii(text: str) -> str:
    """A string as an ASCII terminal can print it, losing decoration only.

    Anything not in the table is decomposed and stripped of its accents, which
    is right for `Iesú` and wrong for nothing this corpus holds; what survives
    both passes becomes `?`, because a byte a stream cannot encode raises
    rather than prints, and a visible `?` is the honest report of a character
    that could not be shown.
    """
    out = []
    for character in str(text):
        if ord(character) < 128:
            out.append(character)
            continue
        replacement = FOLD.get(character)
        if replacement is not None:
            out.append(replacement)
            continue
        decomposed = unicodedata.normalize("NFKD", character)
        kept = "".join(one for one in decomposed if not unicodedata.combining(one))
        out.append(kept if kept.isascii() and kept else "?")
    return "".join(out)


class Style:
    """The one decision about what this run may print, passed to renderers.

    A renderer asks it for a heading or a mark; it does not ask what tier it
    is in. That is deliberate: the moment a renderer branches on the tier, the
    three tiers become three renderers and the plain one is the one nobody
    looks at.
    """

    def __init__(self, tier: str = UNICODE, colour: bool = False) -> None:
        self.tier = tier
        self.colour = bool(colour) and tier == RICH

    @property
    def plain(self) -> bool:
        return self.tier == PLAIN

    def text(self, value: object) -> str:
        """Any string, made safe for this stream."""
        return fold_to_ascii(value) if self.plain else str(value)

    def dash(self) -> str:
        return "--" if self.plain else "—"

    def sgr(self, value: str, role: str) -> str:
        code = _SGR.get(role)
        if not self.colour or not code:
            return value
        return f"\033[{code}m{value}\033[0m"

    def heading(self, value: str, *, rule: str = "") -> list[str]:
        """A heading, and under it the rule the caller asked for.

        The rule is drawn in EVERY tier, because a rule is ASCII and because it
        is the carrier that survives when weight and colour do not: a reader on
        a monochrome VT100 must still be able to tell a heading from a prayer.
        Weight and colour are added on top where the terminal has them, and
        nothing is ever carried by them alone.
        """
        shown = self.text(value)
        lines = [self.sgr(shown, "heading")]
        if rule:
            lines.append(self.sgr(rule * len(shown), "rule"))
        return lines

    def note(self, value: str) -> str:
        return self.sgr(self.text(value), "note")

    def said(self, value: str) -> str:
        return self.sgr(self.text(value), "said")

    def versicled(self, value: str) -> str:
        """`V.` and `R.` as the glyphs, where the stream can carry them.

        Only those two letters, and only as whole marks at a line's head or
        after a sentence, which is where the books print them. Nothing here
        tries to decide who is speaking: the 1861 book's `P.`/`R.` column
        mixes a person with a position in a dialogue, the browser says so at
        length, and a terminal guessing at it would be a second answer to a
        question that already has one.
        """
        if self.plain:
            return self.text(value)
        out = str(value)
        for mark, glyph in (("V.", VERSICLE), ("R.", RESPONSE)):
            out = out.replace(f"\n{mark} ", f"\n{glyph} ")
            if out.startswith(f"{mark} "):
                out = glyph + out[len(mark):]
            out = out.replace(f" {mark} ", f" {glyph} ")
        return out


def stream_carries_unicode(stream: object) -> bool:
    """Whether this stream's own encoding can carry the glyphs."""
    encoding = getattr(stream, "encoding", None)
    if not encoding:
        return False
    try:
        (VERSICLE + "—…").encode(encoding)
    except (LookupError, UnicodeEncodeError):
        return False
    return True


def resolve_style(
    arguments: argparse.Namespace | None = None,
    *,
    stream=None,
    environ: dict | None = None,
) -> Style:
    """The tier this run prints in, and whether it may use colour.

    Order matters and is the whole of the policy: an explicit request wins
    over every detection, because detection is a guess.
    """
    stream = sys.stdout if stream is None else stream
    environ = os.environ if environ is None else environ
    wanted = getattr(arguments, "style", None) or "auto"
    if getattr(arguments, "plain", False):
        wanted = PLAIN
    colour = not environ.get("NO_COLOR")

    if wanted != "auto":
        return Style(wanted, colour)
    if not stream_carries_unicode(stream):
        return Style(PLAIN, False)
    try:
        interactive = bool(stream.isatty())
    except (AttributeError, ValueError):
        interactive = False
    if not interactive:
        # A pipe or a file: no cursor, no colour, but the encoding is the
        # encoding and it can carry the glyphs.
        return Style(UNICODE, False)
    term = str(environ.get("TERM") or "").strip()
    if term in ("", "dumb"):
        # A terminal that advertises nothing gets nothing. This is the older
        # and dumber terminal the whole tier exists for.
        return Style(PLAIN, False)
    return Style(RICH, colour)


def add_style_flags(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Give a parser and every verb under it the two capability flags.

    Both are declared with SUPPRESS defaults so that `tool --plain verb` and
    `tool verb --plain` mean the same thing: an ordinary default on a verb
    parser overwrites what the top-level parser already put in the namespace,
    which would make the flag work in one position and be silently discarded
    in the other.
    """
    for one in _parser_tree(parser):
        for flag, options in (
            (
                "--plain",
                {
                    "action": "store_true",
                    "help": "print ASCII only, whatever the terminal reports",
                },
            ),
            (
                "--style",
                {
                    "choices": STYLES,
                    "help": "force an output tier (default: auto-detected)",
                },
            ),
        ):
            try:
                one.add_argument(flag, default=argparse.SUPPRESS, **options)
            except argparse.ArgumentError:
                pass
    return parser


def _parser_tree(parser: argparse.ArgumentParser) -> list[argparse.ArgumentParser]:
    found = [parser]
    for action in parser._actions:  # noqa: SLF001 - argparse exposes no public walk
        choices = getattr(action, "choices", None)
        if isinstance(action, argparse._SubParsersAction) and isinstance(choices, dict):
            for child in choices.values():
                if isinstance(child, argparse.ArgumentParser) and child not in found:
                    found.extend(_parser_tree(child))
    return found


class _Folded:
    """A stdout that folds to ASCII, installed only for the plain tier.

    It sits around the renderer rather than inside every `print` in thirty-four
    tools, which is the difference between a rule that holds and a rule each
    tool remembers. The machine paths never reach it.
    """

    def __init__(self, stream) -> None:
        self._stream = stream

    def write(self, value: str) -> int:
        return self._stream.write(fold_to_ascii(value))

    def __getattr__(self, name):
        return getattr(self._stream, name)


def dump_json(payload: dict[str, object]) -> str:
    return json.dumps(
        {**payload, "v": PROTOCOL_VERSION},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def print_json(payload: dict[str, object], *, stream=sys.stdout) -> None:
    text = dump_json(payload)
    # The bytes do not move with the terminal — except where the stream cannot
    # carry them at all, and there the choice is between an escaped-but-valid
    # JSON document and a UnicodeEncodeError. Same data, same parse.
    if not stream_carries_unicode(stream):
        text = json.dumps(
            {**payload, "v": PROTOCOL_VERSION},
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        )
    print(text, file=stream)


def fail(message: str, code: str, machine: bool, status: int, prefix: str) -> int:
    if machine:
        print_json(
            {
                "code": code,
                "error": message,
                "status": "error",
            },
            stream=sys.stderr,
        )
    else:
        print(f"{prefix}: {message}", file=sys.stderr)
    return status


def run_verb_cli(
    *,
    parser: argparse.ArgumentParser,
    handlers: dict[str, CommandHandler],
    renderer: OutputRenderer,
    prefix: str,
    argv: list[str] | None,
    default_verb: str | None = None,
    dependency_message: str | None = None,
    mapped_errors: dict[type[BaseException], tuple[str, int]] | None = None,
) -> int:
    add_style_flags(parser)
    arguments = parser.parse_args(argv)
    verb = getattr(arguments, "command", None) or default_verb
    if verb is None:
        parser.error("missing command")
    handler = handlers.get(verb)
    if handler is None:
        parser.error(f"unknown command: {verb}")

    as_json = bool(getattr(arguments, "json", False))
    # Machine output bypasses the capability layer entirely: `--json` is a
    # contract other tools read and `--format yaml` is read by programs, and
    # neither may move a byte because of the terminal it happened to be
    # printed at. Every other path gets the resolved tier, which the renderer
    # takes as an argument rather than detecting for itself — that is what
    # lets a test ask for all three tiers from any machine.
    machine = as_json or str(getattr(arguments, "format", "") or "") in ("json", "yaml")
    arguments.style_resolved = resolve_style(arguments) if not machine else Style(UNICODE, False)

    try:
        payload = handler(arguments)
        if machine or not arguments.style_resolved.plain:
            return renderer(payload, arguments)
        # The plain tier holds for every one of the thirty-four tools,
        # including the thirty-three that have never heard of it, which is
        # what a fold around the renderer buys and a per-tool rule does not.
        held = sys.stdout
        sys.stdout = _Folded(held)  # type: ignore[assignment]
        try:
            return renderer(payload, arguments)
        finally:
            sys.stdout = held
    except ModuleNotFoundError as error:
        message = str(error)
        if dependency_message:
            message = f"{message}; {dependency_message}"
        return fail(message, "dependency", machine, 69, prefix)
    except Exception as error:
        if mapped_errors:
            for exc_type, (code, status) in mapped_errors.items():
                if isinstance(error, exc_type):
                    return fail(
                        str(error) or error.__class__.__name__,
                        code,
                        machine,
                        status,
                        prefix,
                    )
        # An unmapped exception is a defect, not a data-validation failure.
        # The friendly one-line form makes the two indistinguishable, so keep
        # an escape hatch for diagnosing one.
        if os.environ.get("TPT_TRACEBACK"):
            raise
        return fail(
            str(error) or error.__class__.__name__,
            "internal",
            machine,
            70,
            prefix,
        )


def tree_fingerprint(roots) -> tuple[str, int]:
    """Identify these directory trees by every file's path, mtime and size.

    The disk caches under `build/` are keyed by this, so it runs in every tool
    process that reads a cached derivation and its cost is paid whether the
    cache hits or not. That makes it worth doing properly: `os.scandir` carries
    the directory entry's stat with it on the platforms that provide one, where
    `os.walk` plus a separate `os.lstat` asks the kernel twice, and building a
    relative path per file cost more than hashing the absolute one. Over the
    19,092 files of `src/sources` that is 0.094s against 0.041s.

    Deterministic by construction: entries are sorted by name at every level,
    and directories are descended in that order. `os.scandir` returns whatever
    order the filesystem keeps, and this digest is order-dependent, so an
    unsorted walk would fingerprint an unchanged tree differently on each call
    and never hit the cache it guards.

    Symlinked directories are not followed --- a link out of the tree is not
    part of the tree --- and an entry that disappears mid-walk is skipped
    rather than raising, because a cache key is not the place to fail.
    """
    digest = hashlib.sha256()
    counted = 0

    def descend(directory: str) -> None:
        nonlocal counted
        try:
            entries = sorted(os.scandir(directory), key=lambda entry: entry.name)
        except OSError:
            return
        directories = []
        for entry in entries:
            try:
                if entry.is_dir(follow_symlinks=False):
                    directories.append(entry.path)
                    continue
                stat = entry.stat(follow_symlinks=False)
            except OSError:
                continue
            digest.update(
                f"{entry.path}\0{stat.st_mtime_ns}\0{stat.st_size}\0".encode("utf-8")
            )
            counted += 1
        for path in directories:
            descend(path)

    for root in roots:
        digest.update(f"\0root:{root}\0".encode("utf-8"))
        descend(str(root))
    return digest.hexdigest(), counted


def cached_json(directory, key: str, build, *, keep: int = 2):
    """`build()`, kept as JSON under *directory* and reused while *key* holds.

    The pattern this repository now uses in four places, written once. A tool
    answers one question in a fresh process and re-derives the whole corpus to
    do it; the derivation depends on tracked inputs that a key --- normally a
    `tree_fingerprint` --- identifies exactly. `build/` is where
    `guidance/repository.md` says caches live, and `make clean` clears them.

    Written only when it survives the round trip: a value reaches the cache
    only if `json.loads(json.dumps(value)) == value`. That gate is not
    ceremony. JSON has no dates and no integer keys, and a projection that came
    back with a string where a date went in would be a derivation that resolved
    successfully and wrongly, which is the one defect `guidance/the-shape.md`
    says this repository exists to refuse. A value that cannot survive is
    simply never cached and is rebuilt as it always was.

    The entry is written aside and renamed, because the suite runs these in
    parallel and a half-written entry read by a sibling is a wrong answer.

    `keep` is two because only the current key is ever read again --- the key
    IS the inputs --- and these entries are tens of megabytes each. The spare
    one exists so that hopping between two branches does not rebuild every
    time; a third would only be disk.
    """
    import json as _json

    entry = pathlib.Path(directory) / f"{key}.json"
    try:
        return _json.loads(entry.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pass

    value = build()
    try:
        encoded = _json.dumps(value)
        if _json.loads(encoded) == value:
            entry.parent.mkdir(parents=True, exist_ok=True)
            aside = entry.with_suffix(f".{os.getpid()}.tmp")
            aside.write_text(encoded, encoding="utf-8")
            os.replace(aside, entry)
            prune_cache(entry.parent, keep)
    except (OSError, TypeError, ValueError, RecursionError):
        pass
    return value


def prune_cache(directory, keep: int, pattern: str = "*.json") -> None:
    """Keep the newest *keep* entries under *directory*, delete the rest.

    Only the current key is ever read again --- the key is the inputs --- so a
    handful is generous; the spares exist so that hopping between two branches
    does not rebuild every time. `pattern` is `**/*.json` for the caches that
    sha-shard their entries into subdirectories.

    One implementation because there were three, and deleting one of them by
    accident left `load_library` calling a name that no longer existed. That
    only fired on the cache-write path, so a warm checkout never saw it.
    """
    try:
        entries = sorted(
            (path for path in pathlib.Path(directory).glob(pattern) if path.is_file()),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
    except OSError:
        return
    for stale in entries[keep:]:
        try:
            stale.unlink()
        except OSError:
            pass


def code_fingerprint(*paths) -> str:
    """Identify the code a cached derivation was produced by.

    A cache keyed only on its data inputs answers from before the derivation
    changed: edit the function that builds a projection and the previous
    projection is served until somebody runs `make clean`. That is the same
    stale answer the data key exists to prevent, one level up, and it bites
    whoever is editing the code --- the person least able to see why.

    The files' mtime and size rather than their bytes, because this runs on
    every cache lookup and the question is only "is this the same code".
    """
    digest = hashlib.sha256()
    for path in paths:
        try:
            stat = os.stat(path)
        except OSError:
            digest.update(f"\0absent:{path}\0".encode("utf-8"))
            continue
        digest.update(f"\0{path}\0{stat.st_mtime_ns}\0{stat.st_size}\0".encode("utf-8"))
    return digest.hexdigest()[:16]
