#!/usr/bin/env python3
"""Shared CLI launcher helpers for top-level repository tools."""
from __future__ import annotations

import argparse
import json
import os
import sys
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
HEADING = "examples (real output, captured; counts move with the sources):"


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
        "The biblical text, the citations that address it, and the commentary "
        "keyed to those citations.",
        (
            "citations",
            "commentary-work-index",
            "index-bible",
            "reading-plan",
            "typeset-bible",
        ),
    ),
    (
        "calendar",
        "The liturgical calendars, their precedence rules, and the masses "
        "they carry.",
        (
            "calendar-days",
            "calendar-rubrics",
            "calendar-spine",
            "check-calendar-masses",
            "check-proper-components",
            "mass-propers",
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
    "artwork-library": NOTHING,
    "calendar-days": NOTHING,
    "calendar-rubrics": NOTHING,
    "calendar-spine": NOTHING,
    "check-calendar-masses": NOTHING,
    "check-curriculum-structure": NOTHING,
    "check-generation-metadata": NOTHING,
    "check-promised-deliverables": NOTHING,
    "check-proper-components": NOTHING,
    "check-roman-sanctuary-artwork": NOTHING,
    "check-web-edition": NOTHING,
    "citations": NOTHING,
    "commentary-work-index": NOTHING,
    "harvest": MODEL,
    "index-bible": NOTHING,
    "knox-bible": NETWORK,
    "mass-propers": NOTHING,
    "pdf-review": NOTHING,
    "public-alpha": NOTHING,
    "reading-plan": NOTHING,
    "release-bindings": NOTHING,
    "render-sanctuary-dictionary": NOTHING,
    "research-staleness": NOTHING,
    "source-family-migration": NOTHING,
    "source-inventory": NOTHING,
    "source-library": NOTHING,
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
    for index, example in enumerate(examples):
        if index:
            lines.append("")
        lines.append(f"  $ {example.command}")
        if example.note:
            lines.append(f"    ({example.note})")
        for line in example.output:
            lines.append(f"    {line}")
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


def dump_json(payload: dict[str, object]) -> str:
    return json.dumps(
        {**payload, "v": PROTOCOL_VERSION},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def print_json(payload: dict[str, object], *, stream=sys.stdout) -> None:
    print(dump_json(payload), file=stream)


def fail(message: str, code: str, as_json: bool, status: int, prefix: str) -> int:
    if as_json:
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
    arguments = parser.parse_args(argv)
    verb = getattr(arguments, "command", None) or default_verb
    if verb is None:
        parser.error("missing command")
    handler = handlers.get(verb)
    if handler is None:
        parser.error(f"unknown command: {verb}")

    as_json = bool(getattr(arguments, "json", False))
    try:
        payload = handler(arguments)
    except ModuleNotFoundError as error:
        message = str(error)
        if dependency_message:
            message = f"{message}; {dependency_message}"
        return fail(message, "dependency", as_json, 69, prefix)
    except Exception as error:
        if mapped_errors:
            for exc_type, (code, status) in mapped_errors.items():
                if isinstance(error, exc_type):
                    return fail(
                        str(error) or error.__class__.__name__,
                        code,
                        as_json,
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
            as_json,
            70,
            prefix,
        )
    return renderer(payload, arguments)
