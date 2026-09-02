"""The replay's own declarations, and the comparison it rests on.

Running all of the captured invocations is `make check-examples`, which `make
check` runs; it takes minutes and belongs there rather than in every suite run.
What belongs here is what costs nothing and must hold whatever else happens:
that every declaration narrowing the replay names a real capture, that nothing
is exempted by tool, that the comparison fails on the three things it exists to
catch, and that `make check` still invokes the replay at all.

That last one is the point of the exercise, and it is now the whole of it: the
help page prints the invocations and no longer the transcripts, so the replay
is the only reader a capture has. The convention this guards was once enforced
by a test that counted lines
beginning with a "$ " prompt, so nothing noticed when `tpt --list` stopped
printing its recorded fourth line, or when `research-staleness status` recorded
25 stale documents against a real 51. A replay nobody runs would be the same
failure in a new place.
"""

from __future__ import annotations

import ast
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import replay_examples as replay  # noqa: E402


def capture(command: str, output: tuple[str, ...]) -> replay.Capture:
    return replay.Capture(
        tool="example", verb="", command=command, output=output, note="",
        line=1, span=None, indent=0,
    )


class DeclarationTests(unittest.TestCase):
    """Nothing may narrow the replay without naming something that exists."""

    def setUp(self) -> None:
        self.commands = {found.command for found in replay.captures()}

    def test_every_narrowing_declaration_names_a_captured_invocation(self) -> None:
        for table, name in (
            (replay.EXEMPT, "EXEMPT"),
            (replay.REQUIRES, "REQUIRES"),
            (replay.VOLATILE, "VOLATILE"),
            (replay.STALE, "STALE"),
        ):
            for command in table:
                with self.subTest(table=name, command=command):
                    self.assertIn(
                        command, self.commands,
                        f"{name} names an invocation no tool captures; a stale "
                        "declaration silences an example that no longer exists",
                    )

    def test_nothing_is_exempted_by_tool(self) -> None:
        """A verb whose siblings cannot run must still be checked itself."""
        for path in replay.tool_paths():
            found = replay.captures_of(path)
            exempt = [one for one in found if one.command in replay.EXEMPT]
            with self.subTest(tool=path.name):
                self.assertLess(
                    len(exempt), len(found),
                    f"{path.name}: every capture is exempt, which is a tool-wide "
                    "exemption wearing per-invocation clothes",
                )

    def test_the_never_replayed_set_is_exactly_the_declared_one(self) -> None:
        """Adding one must be a decision, not a diff nobody reads."""
        self.assertEqual(
            sorted(replay.EXEMPT),
            sorted(
                [
                    "tools/harvest ask --passage 'Psalms 24' --runs 1 --top 5"
                    " --out build/example-harvest",
                    "tools/harvest record --ledger build/example-harvest/ledger.yaml"
                    " --results build/example-results.yaml --model claude-opus-5"
                    " --audited-on 2026-07-31",
                    "tools/harvest record --ledger build/example-harvest/ledger.yaml"
                    " --results build/example-results.yaml --model claude-opus-5"
                    " --audited-on 2026-07-31 --format json",
                    "tools/knox-bible fetch --root build/knox",
                    "tools/release-bindings refresh",
                    "tools/release-bindings migrate-publications",
                ]
            ),
        )

    def test_every_outward_reaching_verb_is_among_them(self) -> None:
        """The two tools that spend outside this machine, by their spending verb."""
        self.assertTrue(any("harvest ask --passage" in one for one in replay.EXEMPT))
        self.assertTrue(any("knox-bible fetch" in one for one in replay.EXEMPT))

    def test_every_exemption_says_why(self) -> None:
        for command, reason in replay.EXEMPT.items():
            with self.subTest(command=command):
                self.assertGreater(len(reason.split()), 5, "an exemption must argue")

    def test_every_known_stale_transcript_says_what_moved_and_when(self) -> None:
        for command, note in replay.STALE.items():
            with self.subTest(command=command):
                self.assertRegex(note, r"^\d{4}-\d{2}-\d{2}: ", "date the observation")
                self.assertGreater(len(note.split()), 6, "say what moved")


class ComparisonTests(unittest.TestCase):
    """The guard has to fail on a real gap, not merely exist."""

    def test_a_changed_line_is_a_divergence(self) -> None:
        one = capture("tools/example", ("alpha", "beta"))
        self.assertEqual(replay.compare(one, ["alpha", "beta"]), [])
        self.assertTrue(replay.compare(one, ["alpha", "gamma"]))

    def test_a_count_that_moved_is_a_divergence(self) -> None:
        """The failure this whole replay exists for: 25 recorded against 51 real."""
        one = capture("tools/example", ("first", "... 24 more lines"))
        self.assertEqual(replay.compare(one, ["first"] + ["x"] * 24), [])
        self.assertTrue(replay.compare(one, ["first"] + ["x"] * 50))

    def test_a_cut_line_must_continue_for_exactly_what_it_claims(self) -> None:
        one = capture("tools/example", ("abc... [+3 chars]",))
        self.assertEqual(replay.compare(one, ["abcdef"]), [])
        self.assertTrue(replay.compare(one, ["abcdefgh"]))
        self.assertTrue(replay.compare(one, ["xyzdef"]))

    def test_output_beyond_the_transcript_is_a_divergence(self) -> None:
        one = capture("tools/example", ("alpha",))
        self.assertTrue(replay.compare(one, ["alpha", "and one more"]))

    def test_a_transcript_that_outruns_the_command_is_a_divergence(self) -> None:
        one = capture("tools/example", ("alpha", "beta"))
        self.assertTrue(replay.compare(one, ["alpha"]))

    def test_the_repo_placeholder_stands_for_this_checkout(self) -> None:
        one = capture("tools/example", ("<repo>/tools/tpt",))
        self.assertEqual(replay.compare(one, [f"{replay.ROOT}/tools/tpt"]), [])
        self.assertTrue(replay.compare(one, ["/somewhere/else/tools/tpt"]))

    def test_a_volatile_line_still_has_to_hold_its_shape(self) -> None:
        """Declaring a line volatile buys the numbers, not the line."""
        command = "tools/pdf-review --explain"
        one = capture(command, ("pdf-review: host-available=1.00 GiB, ...",))
        pattern = replay.VOLATILE[command][1][0]
        self.assertTrue(
            pattern.search(
                "pdf-review: host-available=94.73 GiB, cgroup-headroom=unknown, "
                "effective=94.73 GiB, reserve=1.00 GiB, per-worker=1.00 GiB, "
                "cpu-cap=24, jobs=24"
            )
        )
        self.assertEqual(
            replay.compare(
                one,
                [
                    "pdf-review: host-available=7.00 GiB, cgroup-headroom=unknown, "
                    "effective=7.00 GiB, reserve=1.00 GiB, per-worker=1.00 GiB, "
                    "cpu-cap=8, jobs=8"
                ],
            ),
            [],
        )
        self.assertTrue(replay.compare(one, ["pdf-review: something else entirely"]))

    def test_the_harvest_dry_run_date_is_volatile_but_iso_shaped(self) -> None:
        command = "tools/harvest ask --passage 'Psalms 24' --runs 1 --top 5 --dry-run"
        one = capture(command, ("audited_on: 2026-08-27",))
        self.assertEqual(replay.compare(one, ["audited_on: 2026-08-28"]), [])
        self.assertTrue(replay.compare(one, ["audited_on: today"]))


class MachineryTests(unittest.TestCase):
    """One real invocation, so the replay is not merely well-declared."""

    def test_a_refusal_replays_exactly(self) -> None:
        found = [
            one
            for one in replay.captures(["tpt"])
            if one.command == "tools/tpt --path no-such-tool"
        ]
        self.assertEqual(len(found), 1, "tpt no longer captures its unknown-id refusal")
        result = replay.replay_one(found[0])
        self.assertEqual(result.status, "match", result.problems)

    def test_recapture_refuses_to_write_a_sibling_id_into_a_tool(self) -> None:
        """tmt reads one as an undeclared dependency; `tpt --list` prints one."""
        found = [
            one for one in replay.captures(["tpt"]) if one.command == "tools/tpt --list"
        ][0]
        self.assertEqual(replay.names_a_sibling(found, list(found.output)), "")
        self.assertEqual(
            replay.names_a_sibling(
                found, [*found.output, "  call or calls a model. knox-bible fetches"]
            ),
            "knox-bible",
        )

    def test_recapture_keeps_the_elisions_it_was_given(self) -> None:
        one = capture("tools/example", ("kept", "cut a... [+1 chars]", "... 2 more lines"))
        self.assertEqual(
            replay.recaptured(one, ["kept", "cut abcd", "x", "y", "z"]),
            ["kept", "cut a... [+3 chars]", "... 3 more lines"],
        )


class GateTests(unittest.TestCase):
    """`make check` has to run the replay, or none of the above matters."""

    def test_make_check_depends_on_the_replay(self) -> None:
        text = (ROOT / "Makefile").read_text(encoding="utf-8")
        recipe = re.search(r"\ncheck:((?:.*\\\n)*.*)\n", text)
        self.assertIsNotNone(recipe, "no `check` target; did the Makefile change shape?")
        self.assertIn("check-examples", recipe.group(1))

    def test_make_check_depends_on_calendar_day_freshness(self) -> None:
        text = (ROOT / "Makefile").read_text(encoding="utf-8")
        recipe = re.search(r"\ncheck:((?:.*\\\n)*.*)\n", text)
        self.assertIsNotNone(recipe, "no `check` target; did the Makefile change shape?")
        prerequisites = recipe.group(1)
        self.assertIn("check-calendar-days", prerequisites)
        self.assertLess(
            prerequisites.index("check-calendar-days"),
            prerequisites.index("check-calendar-rubrics"),
        )

    def test_calendar_day_target_invokes_check_mode(self) -> None:
        text = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertRegex(
            text,
            r"\ncheck-calendar-days:\n(?:\t.*\\\n)*"
            r"\t\t\$\(PYTHON\) tools/tpt calendar-days check; \\",
        )

    def test_deployment_source_gate_checks_every_generated_missal_layer(self) -> None:
        text = (ROOT / "Makefile").read_text(encoding="utf-8")
        heading = re.search(r"\ncheck-deployment-sources:([^\n]*)\n", text)
        self.assertIsNotNone(heading, "check-deployment-sources has no target")
        self.assertIn("check-act-history", heading.group(1))
        self.assertRegex(
            text,
            r"\ncheck-act-history:\n\t@\$\(PYTHON\) tools/tpt act-history structure --check\n",
        )
        recipe = re.search(
            r"\ncheck-deployment-sources:[^\n]*\n((?:\t.*\n)+)",
            text,
        )
        self.assertIsNotNone(recipe, "check-deployment-sources has no recipe")
        body = recipe.group(1)
        commands = (
            "$(SOURCE_READER_TOOL) check",
            "$(SOURCE_READER_TOOL) structure --check",
            "tools/tpt calendar-days check",
            "tools/tpt check-calendar-masses",
            "tools/tpt mass-propers structure --check",
            "tools/tpt calendar-rubrics check",
            "tools/tpt mass-ordinary check",
        )
        positions = []
        for command in commands:
            with self.subTest(command=command):
                self.assertIn(command, body)
                positions.append(body.index(command))
        self.assertEqual(sorted(positions), positions)

    def test_pages_installs_every_deployment_gate_python_dependency(self) -> None:
        """Trace the workflow's Python tool closure back to its exact locks.

        setup-python supplies an interpreter, not third-party modules. Merely
        asserting that a particular requirements filename appears would repeat
        the 2026-08-27 defect under a new name: the Pages gate grew PyYAML-backed
        commands while its install step still named only the renderer lock.
        Derive the invoked tools from the workflow and Make recipes, walk their
        local imports, and require every external import to be owned by a lock
        that the workflow actually installs.
        """
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(
            encoding="utf-8"
        )
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        installed_locks = set(
            re.findall(r"-r\s+(requirements-[a-z0-9-]+\.txt)", workflow)
        )
        self.assertTrue(installed_locks, "Pages installs no requirement lock")

        distribution_imports = {
            "markdown": {"markdown"},
            "pyyaml": {"yaml"},
        }
        installed_imports: set[str] = set()
        for relative in sorted(installed_locks):
            path = ROOT / relative
            self.assertTrue(path.is_file(), f"Pages names missing lock {relative}")
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.partition("#")[0].strip()
                if not line:
                    continue
                pinned = re.fullmatch(r"([A-Za-z0-9_.-]+)==[^\s]+", line)
                self.assertIsNotNone(
                    pinned,
                    f"{relative} has an unpinned entry: {line}",
                )
                distribution = re.sub(r"[-_.]+", "-", pinned.group(1)).lower()
                self.assertIn(
                    distribution,
                    distribution_imports,
                    f"declare the import name supplied by {pinned.group(1)}",
                )
                installed_imports.update(distribution_imports[distribution])

        make_targets = set(
            re.findall(r"\brun:\s+make\s+([a-z][a-z0-9-]*)", workflow)
        )
        self.assertEqual(
            {"check-deployment-sources", "public-site"} - make_targets,
            set(),
        )
        tool_variables = dict(
            re.findall(
                r"^([A-Z_]+_TOOL)\s*:=\s*tools/tpt\s+([a-z][a-z0-9-]*)",
                makefile,
                flags=re.MULTILINE,
            )
        )
        tool_ids = set(
            re.findall(r"tools/tpt\s+([a-z][a-z0-9-]*)", workflow)
        )
        for target in make_targets:
            recipe = re.search(
                rf"^{re.escape(target)}:[^\n]*\n((?:\t.*\n)+)",
                makefile,
                flags=re.MULTILINE,
            )
            self.assertIsNotNone(recipe, f"workflow invokes missing target {target}")
            body = recipe.group(1)
            tool_ids.update(re.findall(r"tools/tpt\s+([a-z][a-z0-9-]*)", body))
            for variable in re.findall(r"\$\(([A-Z_]+_TOOL)\)", body):
                self.assertIn(variable, tool_variables)
                tool_ids.add(tool_variables[variable])

        pending = [ROOT / "tools/tpt"] + [
            ROOT / "tools" / tool_id for tool_id in sorted(tool_ids)
        ]
        seen: set[Path] = set()
        external_imports: set[str] = set()
        while pending:
            path = pending.pop()
            if path in seen:
                continue
            seen.add(path)
            self.assertTrue(path.is_file(), f"deployment tool is missing: {path}")
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imported = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(
                        alias.name.partition(".")[0] for alias in node.names
                    )
                elif (
                    isinstance(node, ast.ImportFrom)
                    and node.level == 0
                    and node.module
                ):
                    imported.add(node.module.partition(".")[0])
            for module in imported:
                if module == "__future__" or module in sys.stdlib_module_names:
                    continue
                local = ROOT / "scripts" / f"{module}.py"
                if local.is_file():
                    pending.append(local)
                else:
                    external_imports.add(module)

        self.assertEqual(
            external_imports,
            installed_imports,
            "Pages deployment imports and explicitly installed locks disagree",
        )

    def test_the_replay_target_exists_and_invokes_the_script(self) -> None:
        text = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertRegex(
            text, r"\ncheck-examples:\n\t@?\$\(PYTHON\) scripts/replay_examples\.py"
        )


if __name__ == "__main__":
    unittest.main()
