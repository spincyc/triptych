"""Exercise mass-propers' real main parser without dispatching any handler."""
from __future__ import annotations

import argparse
import contextlib
import importlib.machinery
import importlib.util
import io
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


ROOT = Path(os.environ.get("MASS_PROPERS_REPOSITORY_ROOT", Path(__file__).resolve().parents[2]))
TOOL = Path(os.environ.get("MASS_PROPERS_UNDER_TEST", ROOT / "tools" / "mass-propers"))
sys.path.insert(0, str(ROOT / "scripts"))
loader = importlib.machinery.SourceFileLoader("mass_propers_cli_under_test", str(TOOL))
spec = importlib.util.spec_from_loader(loader.name, loader)
assert spec is not None
mass_propers = importlib.util.module_from_spec(spec)
loader.exec_module(mass_propers)

from _tooling import add_style_flags


class MassPropersCliOptions(unittest.TestCase):
    verbs = ("show", "list", "structure", "census")
    options = (
        ("--root", "root", "/explicit/calendars", "/later/calendars"),
        ("--calendar", "calendar", "roman-1962", "roman-pre-1955"),
        ("--format", "format", "json", "yaml"),
        ("--bible", "bible", "douay-rheims", "clementine"),
        ("--lang", "lang", "en", "la"),
        ("--witness", "witness", "first-witness", "last-witness"),
        ("--bible-root", "bible_root", "/explicit/bibles", "/later/bibles"),
        ("--out", "out", "/explicit/output", "/later/output"),
        ("--doc-root", "doc_root", "/explicit/docs", "/later/docs"),
    )
    flags = ("write", "check", "verbose", "json")

    def parse(self, argv):
        captured = []

        def capture(**kwargs):
            add_style_flags(kwargs["parser"])
            arguments = kwargs["parser"].parse_args(kwargs["argv"])
            captured.append((arguments, arguments.command or kwargs["default_verb"]))
            return 37

        # Every handler is guarded too: dispatch would be a test error, never a write.
        with patch.object(mass_propers, "run_verb_cli", capture), contextlib.ExitStack() as stack:
            for verb in self.verbs:
                stack.enter_context(patch.object(mass_propers, "run_" + verb, side_effect=AssertionError("handler dispatched")))
            self.assertEqual(mass_propers.main(argv), 37)
        self.assertEqual(len(captured), 1)
        return captured[0]

    def test_explicit_scalar_options_before_each_verb(self):
        for verb in self.verbs:
            for option, dest, first, _ in self.options:
                with self.subTest(verb=verb, option=option):
                    args, effective = self.parse([option, first, verb])
                    self.assertEqual(getattr(args, dest), first)
                    self.assertEqual(effective, verb)

    def test_explicit_scalar_options_after_each_verb(self):
        for verb in self.verbs:
            for option, dest, first, _ in self.options:
                with self.subTest(verb=verb, option=option):
                    args, _ = self.parse([verb, option, first])
                    self.assertEqual(getattr(args, dest), first)

    def test_later_scalar_value_wins_across_verb(self):
        for verb in self.verbs:
            for option, dest, first, last in self.options:
                with self.subTest(verb=verb, option=option):
                    args, _ = self.parse([option, first, verb, option, last])
                    self.assertEqual(getattr(args, dest), last)

    def test_last_scalar_wins_within_either_side(self):
        for option, dest, first, last in self.options:
            for argv in ([option, first, option, last, "structure"], ["structure", option, first, option, last]):
                with self.subTest(argv=argv):
                    args, _ = self.parse(argv)
                    self.assertEqual(getattr(args, dest), last)

    def test_flags_survive_before_each_verb(self):
        for verb in self.verbs:
            for flag in self.flags:
                with self.subTest(verb=verb, flag=flag):
                    args, _ = self.parse(["--" + flag, verb])
                    self.assertIs(getattr(args, flag), True)

    def test_flags_work_after_each_verb(self):
        for verb in self.verbs:
            for flag in self.flags:
                with self.subTest(verb=verb, flag=flag):
                    args, _ = self.parse([verb, "--" + flag])
                    self.assertIs(getattr(args, flag), True)

    def test_mass_repetitions_survive_before_each_verb(self):
        for verb in self.verbs:
            with self.subTest(verb=verb):
                args, _ = self.parse(["--mass", "advent-1", "--mass", "advent-2", verb])
                self.assertEqual(args.mass, ["advent-1", "advent-2"])

    def test_mass_repetitions_work_after_each_verb(self):
        for verb in self.verbs:
            with self.subTest(verb=verb):
                args, _ = self.parse([verb, "--mass", "advent-1", "--mass", "advent-2"])
                self.assertEqual(args.mass, ["advent-1", "advent-2"])

    def test_mixed_mass_selections_accumulate_in_argv_order(self):
        for verb in self.verbs:
            with self.subTest(verb=verb):
                args, _ = self.parse(["--mass", "earlier-1", "--mass", "earlier-2", verb, "--mass", "later-1", "--mass", "later-2"])
                self.assertEqual(args.mass, ["earlier-1", "earlier-2", "later-1", "later-2"])

    def test_mass_selection_does_not_leak_between_main_calls(self):
        first, _ = self.parse(["--mass", "advent-1", "show", "--mass", "advent-2"])
        second, _ = self.parse(["show", "--mass", "lent-1"])
        empty, _ = self.parse(["show"])
        self.assertEqual(first.mass, ["advent-1", "advent-2"])
        self.assertEqual(second.mass, ["lent-1"])
        self.assertIsNone(empty.mass)

    def test_defaults_remain_present_for_each_verb_and_default_verb(self):
        expected = dict(
            root=str(mass_propers.DEFAULT_ROOT), calendar=None, mass=None,
            format="text", bible=None, lang="la", witness=None,
            bible_root=str(mass_propers.BIBLE_ROOT), out="src/web/data",
            doc_root=str(mass_propers.ROOT), write=False, check=False,
            verbose=False, json=False,
        )
        for argv in ([], *([verb] for verb in self.verbs)):
            with self.subTest(argv=argv):
                args, effective = self.parse(argv)
                for dest, value in expected.items():
                    self.assertEqual(getattr(args, dest), value, dest)
                self.assertEqual(effective, argv[0] if argv else "show")

    def test_options_without_a_verb_keep_default_show(self):
        argv = [item for option, _, value, _ in self.options for item in (option, value)]
        argv.extend(("--mass", "advent-1", "--check"))
        args, effective = self.parse(argv)
        self.assertEqual(effective, "show")
        for _, dest, value, _ in self.options:
            self.assertEqual(getattr(args, dest), value)
        self.assertEqual(args.mass, ["advent-1"])
        self.assertTrue(args.check)

    def test_invalid_format_still_refused_on_either_side(self):
        for argv in (["--format", "invalid", "structure"], ["structure", "--format", "invalid"]):
            with self.subTest(argv=argv), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    self.parse(argv)
                self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
