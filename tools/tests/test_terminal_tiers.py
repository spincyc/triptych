"""The terminal capability layer: the tier table, and what each tier prints.

This suite must pass on any machine, from any terminal, in CI and on a laptop,
and it must cover terminals nobody here has. That rules out running anything
through a pty and reading what comes back: the answer would depend on the
tester's own `TERM` and locale, and the one terminal that would never be
covered is the dumb one the layer exists for.

So capability is an ARGUMENT and not an ambient fact. `resolve_style` is a
function of (stream encoding, isatty, TERM, NO_COLOR) and returns a tier;
`Style` is a function of (content, tier) and returns text. Both are called
directly here, with the environment described rather than arranged.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from _ordinary_text import element_lines  # noqa: E402
from _tooling import (  # noqa: E402
    PLAIN,
    RICH,
    UNICODE,
    Style,
    fold_to_ascii,
    resolve_style,
    run_verb_cli,
)


class FakeStream:
    """A stream described by the two things detection is allowed to ask."""

    def __init__(self, encoding: str = "utf-8", tty: bool = False) -> None:
        self.encoding = encoding
        self._tty = tty

    def isatty(self) -> bool:
        return self._tty


def flags(**named) -> argparse.Namespace:
    return argparse.Namespace(**named)


class DetectionTests(unittest.TestCase):
    """One table, every terminal this project claims to support."""

    CASES = (
        # (what it is, encoding, tty, TERM, NO_COLOR, tier, colour)
        ("a modern terminal", "utf-8", True, "xterm-256color", None, RICH, True),
        ("a modern terminal, NO_COLOR", "utf-8", True, "xterm-256color", "1", RICH, False),
        ("an old but named terminal", "utf-8", True, "vt100", None, RICH, True),
        # A terminal that advertises nothing gets nothing: this is the dumb
        # terminal the whole layer exists for.
        ("a dumb terminal", "utf-8", True, "dumb", None, PLAIN, False),
        ("a terminal with no TERM at all", "utf-8", True, "", None, PLAIN, False),
        # A pipe or a file has no cursor and no colour, but its encoding is its
        # encoding and carries the glyphs perfectly well.
        ("a utf-8 pipe", "utf-8", False, "xterm-256color", None, UNICODE, False),
        ("a utf-8 file, no terminal at all", "utf-8", False, "", None, UNICODE, False),
        # Where the stream cannot carry the glyphs, nothing else matters.
        ("an ascii pipe", "ascii", False, "xterm-256color", None, PLAIN, False),
        ("an ascii terminal", "ascii", True, "xterm-256color", None, PLAIN, False),
        ("a latin-1 terminal", "iso-8859-1", True, "xterm", None, PLAIN, False),
        ("a stream declaring no encoding", None, False, "xterm", None, PLAIN, False),
    )

    def test_the_table(self) -> None:
        for what, encoding, tty, term, no_colour, tier, colour in self.CASES:
            with self.subTest(terminal=what):
                environ = {"TERM": term}
                if no_colour:
                    environ["NO_COLOR"] = no_colour
                style = resolve_style(
                    flags(), stream=FakeStream(encoding, tty), environ=environ
                )
                self.assertEqual(style.tier, tier)
                self.assertEqual(style.colour, colour)

    def test_plain_is_reachable_whatever_is_detected(self) -> None:
        """The maintainer's second message: an operator who says plain means plain."""
        for what, encoding, tty, term, _, _, _ in self.CASES:
            with self.subTest(terminal=what):
                style = resolve_style(
                    flags(plain=True),
                    stream=FakeStream(encoding, tty),
                    environ={"TERM": term},
                )
                self.assertEqual(style.tier, PLAIN)
                self.assertFalse(style.colour)

    def test_a_named_tier_overrides_detection_in_both_directions(self) -> None:
        # Asking for the glyphs on a dumb terminal is allowed: the operator can
        # see their own screen and this cannot.
        style = resolve_style(
            flags(style=RICH), stream=FakeStream("ascii", False), environ={"TERM": "dumb"}
        )
        self.assertEqual(style.tier, RICH)
        style = resolve_style(
            flags(style=UNICODE), stream=FakeStream("utf-8", True), environ={"TERM": "xterm"}
        )
        self.assertEqual(style.tier, UNICODE)
        self.assertFalse(style.colour)

    def test_no_colour_never_removes_a_distinction(self) -> None:
        """Colour is decoration; the words and the rule carry the meaning."""
        bare = Style(RICH, colour=False)
        coloured = Style(RICH, colour=True)
        self.assertEqual(
            [line for line in bare.heading("Collect", rule="-")],
            ["Collect", "-------"],
        )
        self.assertIn("Collect", coloured.heading("Collect", rule="-")[0])


class FoldTests(unittest.TestCase):
    def test_nothing_above_0x7f_survives(self) -> None:
        sample = "— – … ‘’ “” · § ¶ © † ‡ ✠ ☧ → ‹› æ Æ œ Œ ℣ ℟ é è ë"
        folded = fold_to_ascii(sample)
        self.assertTrue(folded.isascii(), folded)

    def test_the_marks_a_reader_needs_survive_the_fold(self) -> None:
        self.assertEqual(fold_to_ascii("℣ Dominus — ℟ Amen…"), "V. Dominus -- R. Amen...")
        self.assertEqual(fold_to_ascii("beatæ Mariæ"), "beatae Mariae")

    def test_an_unknown_character_becomes_a_visible_question(self) -> None:
        """A character that cannot be shown says so, rather than raising."""
        self.assertEqual(fold_to_ascii("☃"), "?")


class SettingTests(unittest.TestCase):
    """Every tier draws the same distinctions; only the decoration differs."""

    RUBRIC = {
        "key": "conclusio/rubrica-inclinatus-ante-altare",
        "kind": "rubric",
        "name": None,
        "latin_incipit": None,
        "locus": "xx",
        "speaker": None,
        "absent": {"english": None, "latin": "latin-not-transcribed"},
        "translations": [
            {"lang": "en", "text": "Bowing before the Altar, the Priest says", "source_id": "s"}
        ],
    }
    PRAYER = {
        "key": "conclusio/placeat-tibi",
        "kind": "prayer",
        "name": "Placeat tibi sancta Trinitas",
        "latin_incipit": "Placeat tibi",
        "locus": "xx",
        "speaker": "priest",
        "absent": {"english": None, "latin": "latin-not-transcribed"},
        "translations": [
            {"lang": "en", "text": "Let the performance of my homage be pleasing", "source_id": "s"}
        ],
    }
    WITHHELD = {
        "key": "ritus-initiales/salutatio",
        "kind": "dialogue",
        "name": "The Greeting",
        "latin_incipit": "Dominus vobiscum",
        "locus": None,
        "speaker": "all",
        "absent": {
            "english": "approved-english-publication-restriction",
            "latin": "latin-not-transcribed",
        },
        "translations": [],
    }

    def tiers(self) -> tuple[Style, ...]:
        return (Style(PLAIN), Style(UNICODE), Style(RICH, colour=True))

    def test_a_rubric_reads_as_a_rubric_in_every_tier(self) -> None:
        """The Placeat defect: an action must never read as a line of a prayer."""
        for style in self.tiers():
            with self.subTest(tier=style.tier):
                rubric = "\n".join(element_lines(self.RUBRIC, "en", style))
                prayer = "\n".join(element_lines(self.PRAYER, "en", style))
                self.assertIn("[ Bowing before the Altar", rubric)
                self.assertNotIn("[ Let the performance", prayer)
                self.assertIn("Placeat tibi sancta Trinitas", prayer)

    def test_a_hidden_rubric_is_hidden_and_nothing_else_is(self) -> None:
        for style in self.tiers():
            with self.subTest(tier=style.tier):
                self.assertEqual(
                    element_lines(self.RUBRIC, "en", style, show_rubrics=False), []
                )
                self.assertNotEqual(
                    element_lines(self.PRAYER, "en", style, show_rubrics=False), []
                )

    def test_an_absence_states_its_typed_reason_in_every_tier(self) -> None:
        for style in self.tiers():
            with self.subTest(tier=style.tier):
                shown = "\n".join(element_lines(self.WITHHELD, "en", style))
                self.assertIn(
                    "absent: approved-english-publication-restriction", shown
                )

    def test_plain_carries_no_byte_above_0x7f(self) -> None:
        style = Style(PLAIN)
        for element in (self.RUBRIC, self.PRAYER, self.WITHHELD):
            shown = "\n".join(element_lines(element, "en", style))
            self.assertTrue(shown.isascii(), shown)

    def test_the_versicle_glyphs_appear_only_where_the_stream_carries_them(self) -> None:
        spoken = dict(self.PRAYER, kind="dialogue")
        spoken["translations"] = [
            {"lang": "en", "text": "V. The Lord be with you. R. And with thy spirit.",
             "source_id": "s"}
        ]
        plain = "\n".join(element_lines(spoken, "en", Style(PLAIN)))
        rich = "\n".join(element_lines(spoken, "en", Style(RICH)))
        self.assertIn("V. The Lord", plain)
        self.assertTrue(plain.isascii(), plain)
        self.assertIn("\u2123 The Lord", rich)
        self.assertIn("℟ And with", rich)


class FoldedWriterTests(unittest.TestCase):
    """The plain tier holds for a tool that has never heard of it."""

    def test_the_wrapper_folds_whatever_is_written_through_it(self) -> None:
        from _tooling import _Folded

        buffer = io.StringIO()
        writer = _Folded(buffer)
        writer.write("roman-1962 — advent…\n")
        self.assertEqual(buffer.getvalue(), "roman-1962 -- advent...\n")


class RendererFailureTests(unittest.TestCase):
    """A renderer gets the same controlled diagnostics as its handler."""

    @staticmethod
    def parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(prog="example")
        show = parser.add_subparsers(dest="command").add_parser("show")
        show.add_argument("--json", action="store_true")
        show.add_argument("--format", choices=("text", "json", "yaml"), default="text")
        return parser

    @staticmethod
    def handler(_arguments: argparse.Namespace) -> dict[str, str]:
        return {"status": "ok"}

    @staticmethod
    def broken_renderer(
        _payload: object, _arguments: argparse.Namespace
    ) -> int:
        raise ValueError("renderer broke")

    def run_broken(self, *argv: str, **extra) -> int:
        return run_verb_cli(
            parser=self.parser(),
            handlers={"show": self.handler},
            renderer=self.broken_renderer,
            prefix="example",
            argv=list(argv),
            **extra,
        )

    def test_machine_renderer_failure_is_structured_and_nonzero(self) -> None:
        error = io.StringIO()
        with redirect_stderr(error):
            status = self.run_broken("show", "--json")
        self.assertEqual(status, 70)
        self.assertEqual(
            json.loads(error.getvalue()),
            {
                "code": "internal",
                "error": "renderer broke",
                "status": "error",
                "v": 1,
            },
        )
        self.assertNotIn("Traceback", error.getvalue())

    def test_format_machine_renderer_failures_are_structured_and_nonzero(self) -> None:
        for output_format in ("json", "yaml"):
            with self.subTest(format=output_format):
                error = io.StringIO()
                with redirect_stderr(error):
                    status = self.run_broken("show", "--format", output_format)
                self.assertEqual(status, 70)
                self.assertEqual(
                    json.loads(error.getvalue()),
                    {
                        "code": "internal",
                        "error": "renderer broke",
                        "status": "error",
                        "v": 1,
                    },
                )

    def test_plain_renderer_failure_restores_stdout(self) -> None:
        output = io.StringIO()
        error = io.StringIO()
        held = sys.stdout
        with patch.object(sys, "stdout", output), redirect_stderr(error):
            wrapped = sys.stdout
            status = self.run_broken("show", "--plain")
            self.assertIs(sys.stdout, wrapped)
        self.assertIs(sys.stdout, held)
        self.assertEqual(status, 70)
        self.assertEqual(error.getvalue(), "example: renderer broke\n")

    def test_renderer_failure_uses_the_mapped_error_contract(self) -> None:
        error = io.StringIO()
        with redirect_stderr(error):
            status = self.run_broken(
                "show", "--json", mapped_errors={ValueError: ("input", 2)}
            )
        self.assertEqual(status, 2)
        self.assertEqual(json.loads(error.getvalue())["code"], "input")

    def test_handler_failure_keeps_the_same_mapped_error_contract(self) -> None:
        def broken_handler(_arguments: argparse.Namespace) -> object:
            raise ValueError("handler broke")

        error = io.StringIO()
        with redirect_stderr(error):
            status = run_verb_cli(
                parser=self.parser(),
                handlers={"show": broken_handler},
                renderer=lambda _payload, _arguments: 0,
                prefix="example",
                argv=["show", "--json"],
                mapped_errors={ValueError: ("input", 2)},
            )
        self.assertEqual(status, 2)
        self.assertEqual(json.loads(error.getvalue())["code"], "input")

    def test_format_machine_handler_failures_keep_the_mapped_error_contract(self) -> None:
        def broken_handler(_arguments: argparse.Namespace) -> object:
            raise ValueError("handler broke")

        for output_format in ("json", "yaml"):
            with self.subTest(format=output_format):
                error = io.StringIO()
                with redirect_stderr(error):
                    status = run_verb_cli(
                        parser=self.parser(),
                        handlers={"show": broken_handler},
                        renderer=lambda _payload, _arguments: 0,
                        prefix="example",
                        argv=["show", "--format", output_format],
                        mapped_errors={ValueError: ("input", 2)},
                    )
                self.assertEqual(status, 2)
                self.assertEqual(json.loads(error.getvalue())["code"], "input")

    def test_format_machine_dependency_failures_are_structured(self) -> None:
        def missing_dependency(_arguments: argparse.Namespace) -> object:
            raise ModuleNotFoundError("No module named 'example_dependency'")

        for output_format in ("json", "yaml"):
            with self.subTest(format=output_format):
                error = io.StringIO()
                with redirect_stderr(error):
                    status = run_verb_cli(
                        parser=self.parser(),
                        handlers={"show": missing_dependency},
                        renderer=lambda _payload, _arguments: 0,
                        prefix="example",
                        argv=["show", "--format", output_format],
                        dependency_message="install example-dependency",
                    )
                self.assertEqual(status, 69)
                payload = json.loads(error.getvalue())
                self.assertEqual(payload["code"], "dependency")
                self.assertIn("install example-dependency", payload["error"])

    def test_traceback_opt_in_still_raises_renderer_errors(self) -> None:
        with patch.dict(os.environ, {"TPT_TRACEBACK": "1"}):
            with self.assertRaisesRegex(ValueError, "renderer broke"):
                self.run_broken("show", "--json")


if __name__ == "__main__":
    unittest.main()
