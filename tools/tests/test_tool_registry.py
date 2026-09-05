"""Registry drift: tmt.json, tools/, and the Makefile must agree.

Every failure here has shipped at least once. The Makefile invoked a tool by
its filename rather than its registry id, the registry advertised a tool with
no implementation, and a tool body moved without its callers.

Two of these guard what `--help` says rather than what a tool does. Both exist
because the failure they catch is the one this repository treats as worse than
a crash: help text that looks right and is wrong. A verb with no worked example
sends a reader to run the command twice to find out what it did, and a tool
that no `--list` group claims disappears from the only listing a reader reads.
"""

from __future__ import annotations

import functools
import importlib.machinery
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _parallel import gather  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "tmt.json"
TOOLS = ROOT / "tools"
LAUNCHER = ROOT / "tools" / "tpt"

# tmt ignores subdirectories and these companion suffixes when scanning tools/.
COMPANION_SUFFIXES = (".md", ".test")
# tmt's registry validator caps the field.
PURPOSE_LIMIT = 80
# scripts/_tooling.py owns the heading; asserting on it here rather than on
# prose means a reworded example cannot silently stop being checked.
EXAMPLES_HEADING = "examples (real invocations; `make check-examples` replays each one):"
INVOCATION = re.compile(r"^\s+\$ \S", re.M)
NO_EXAMPLE = "no runnable example:"
VERBS = re.compile(r"positional arguments:\n\s+\{([a-z0-9,\-]+)\}")
MINIMUM_EXAMPLES = 2


def registry() -> dict[str, dict]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["tools"]


@functools.lru_cache(maxsize=None)
def help_text(*argv: str) -> str:
    """What `tpt <argv> --help` prints, asked of the launcher once.

    Four tests in `WorkedExampleTests` each walk every registered tool and
    every verb of it, and each walk asked the launcher again for help pages the
    walk before had already read: 41 tools and their verbs, four times over,
    around 40 seconds of launcher processes to read text that cannot change
    while the suite runs. A failure still reports the same text, because it is
    the same text.
    """
    result = subprocess.run(
        [str(LAUNCHER), *argv, "--help"], capture_output=True, text=True, cwd=ROOT,
    )
    if result.returncode != 0:
        raise AssertionError(f"{' '.join(argv)} --help failed: {result.stderr}")
    return result.stdout


@functools.lru_cache(maxsize=None)
def resolved_path(name: str) -> subprocess.CompletedProcess:
    """What `tpt --path <name>` answers, asked of the launcher once.

    Three tests below ask the launcher to resolve every registered id --- is it
    executable, is it its own basename, is every implementation registered ---
    and each asked again for all 41. The answer cannot differ between them.
    """
    return subprocess.run(
        [str(LAUNCHER), "--path", name], capture_output=True, text=True, cwd=ROOT,
    )


def setUpModule() -> None:
    """Fill the help-text cache once, in parallel, before anything reads it.

    Six tests here walk every registered tool and every verb of it. With
    `help_text` memoized they ask the launcher once rather than six times, but
    that once was still 41 tools and their verbs one after another, and a cold
    `tpt --help` is two interpreters. Nothing depends on the order they are
    fetched in, so they are fetched together and every test after this reads
    memory.

    Failures are deliberately not raised here: a tool whose `--help` exits
    non-zero must fail in the test that asks about that tool, naming it, not in
    a module fixture that stops all six.
    """
    def safely(argv: tuple[str, ...]) -> None:
        try:
            help_text(*argv)
        except AssertionError:
            pass

    names = sorted(registry())
    gather(resolved_path, names)
    gather(safely, [(name,) for name in names])

    def verbs(name: str) -> list[str]:
        """The tool's verbs, or none where its help could not be read.

        Guarded for the same reason `safely` is, and it was not: a tool whose
        `--help` exits non-zero was swallowed above and then raised here,
        erroring every test in the module at `setUpModule` instead of failing
        the one test that asks about that tool, under its own subTest.
        """
        try:
            return verbs_of(help_text(name))
        except AssertionError:
            return []

    gather(safely, [(name, verb) for name in names for verb in verbs(name)])


def verbs_of(text: str) -> list[str]:
    found = VERBS.search(text)
    return found.group(1).split(",") if found else []


def section_of(text: str) -> str:
    head, marker, tail = text.partition(EXAMPLES_HEADING)
    if not marker:
        raise AssertionError(f"no examples section:\n{text}")
    return tail


class ToolRegistryTests(unittest.TestCase):
    def test_every_id_resolves_to_an_executable(self) -> None:
        for name in registry():
            with self.subTest(tool=name):
                resolved = resolved_path(name)
                self.assertEqual(resolved.returncode, 0, resolved.stderr)
                path = Path(resolved.stdout.strip())
                self.assertTrue(path.is_file(), f"{name}: {path} is not a file")
                self.assertTrue(os.access(path, os.X_OK), f"{name}: {path} not executable")

    def test_every_implementation_is_registered(self) -> None:
        """Every file under tools/ is the implementation of a registered id.

        `resolved` does not depend on the file being checked, so it is built
        once. It used to be built inside the loop, which asked the launcher to
        resolve all 41 registered ids once per file on disk --- 1,681 launcher
        processes to answer a question 41 answer, and 68 seconds, which was the
        slowest single test in the suite. The set is the same set and the
        assertion is the same assertion.
        """
        registered = set(registry())
        resolved = {
            Path(resolved_path(name).stdout.strip()).name for name in registered
        }
        for path in sorted(TOOLS.iterdir()):
            if not path.is_file() or path.name.endswith(COMPANION_SUFFIXES):
                continue
            with self.subTest(tool=path.name):
                self.assertIn(path.name, resolved)

    def test_no_id_can_shadow_a_launcher_option(self) -> None:
        """The launcher's own controls are dash-prefixed; ids must not be."""
        self.assertEqual([n for n in registry() if n.startswith("-")], [])

    def test_launcher_self_check_agrees_with_the_filesystem(self) -> None:
        result = subprocess.run(
            [str(LAUNCHER), "--check"], capture_output=True, text=True, cwd=ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_purposes_fit_the_registry_cap(self) -> None:
        for name, record in registry().items():
            with self.subTest(tool=name):
                self.assertLessEqual(len(record["purpose"]), PURPOSE_LIMIT)

    def test_makefile_invokes_only_registered_ids(self) -> None:
        known = set(registry())
        text = (ROOT / "Makefile").read_text(encoding="utf-8")
        called = set(re.findall(r"tools/tpt\s+([a-z][a-z0-9-]*)", text))
        self.assertTrue(called, "no tpt invocations found; did the Makefile change shape?")
        self.assertEqual(called - known, set())

    def test_workflow_invokes_only_registered_ids(self) -> None:
        workflow = ROOT / ".github" / "workflows" / "pages.yml"
        called = set(re.findall(r"tools/tpt\s+([a-z][a-z0-9-]*)",
                                workflow.read_text(encoding="utf-8")))
        self.assertEqual(called - set(registry()), set())

    def test_unknown_tool_fails_without_a_traceback(self) -> None:
        result = subprocess.run(
            [str(LAUNCHER), "no-such-tool"], capture_output=True, text=True, cwd=ROOT,
        )
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_usage_names_every_verb_the_tool_accepts(self) -> None:
        """The registry usage string is hand-maintained, so it drifts.

        Read the verbs from the tool's own --help rather than by feeding the
        parser a junk positional, which would invoke the mutating tools.
        """
        entries = registry()
        for name, record in entries.items():
            with self.subTest(tool=name):
                helped = subprocess.run(
                    [str(LAUNCHER), name, "--help"],
                    capture_output=True, text=True, cwd=ROOT,
                )
                self.assertEqual(helped.returncode, 0, helped.stderr)
                section = re.search(
                    r"positional arguments:\n\s+\{([a-z0-9,\-]+)\}", helped.stdout
                )
                if section is None:
                    continue
                declared = record["usage"]
                for verb in section.group(1).split(","):
                    self.assertIn(verb, declared, f"{name}: usage omits {verb!r}")

    def test_no_tool_hardcodes_an_absolute_path(self) -> None:
        # public-alpha searches published content for leaked machine-local
        # paths, so the pattern itself must contain the literal.
        allowed = {"public-alpha"}
        for name in registry():
            with self.subTest(tool=name):
                body = (TOOLS / name).read_text(encoding="utf-8", errors="replace")
                self.assertNotIn(str(ROOT), body)
                if name not in allowed:
                    self.assertNotIn("/home/", body)

    def test_every_id_is_its_own_basename(self) -> None:
        """tmt resolves an entry only at tools/<id>; an alias would break it."""
        for name in registry():
            with self.subTest(tool=name):
                result = resolved_path(name)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(Path(result.stdout.strip()), TOOLS / name)


class WorkedExampleTests(unittest.TestCase):
    """Every verb shows what it prints, so nobody has to run it twice.

    The rule is two invocations per verb. The single exception is a verb no
    machine here can run — a licensed root, a network fetch — which must say so
    in the help rather than show an invented transcript; that is what the
    `no runnable example:` line is, and it buys the verb one example instead of
    two, never zero.

    These count invocations; they say nothing about whether a transcript is
    still what the tool prints. That is scripts/replay_examples.py, which runs
    every captured invocation and compares it line for line — `make
    check-examples`, which `make check` runs. Until it existed, two transcripts
    had been wrong for weeks with everything here green.
    """

    def sections(self, name: str) -> list[tuple[str, str]]:
        """(label, examples section) for everything this tool must document.

        A verb declared with argparse subparsers owns a help page and so a
        section of its own. `public-alpha` declares its four instead as one
        positional choice, which argparse gives no per-verb help at all; there
        the whole set shares the top-level section, and the floor rises to
        match rather than the rule quietly not applying.
        """
        top = help_text(name)
        verbs = verbs_of(top)
        if not verbs:
            return [(name, section_of(top))]
        own = [(f"{name} {verb}", help_text(name, verb)) for verb in verbs]
        if all(text == top for _, text in own):
            return [(f"{name} (all {len(verbs)} verbs share one help page)",
                     section_of(top), len(verbs))]  # type: ignore[list-item]
        return [(label, section_of(text)) for label, text in own]

    def test_every_verb_shows_at_least_two_real_invocations(self) -> None:
        for name in registry():
            for entry in self.sections(name):
                label, section = entry[0], entry[1]
                multiplier = entry[2] if len(entry) > 2 else 1
                with self.subTest(target=label):
                    shown = len(INVOCATION.findall(section))
                    floor = 1 if NO_EXAMPLE in section else MINIMUM_EXAMPLES
                    self.assertGreaterEqual(
                        shown, floor * multiplier,
                        f"{label}: {shown} example(s); the rule is "
                        f"{MINIMUM_EXAMPLES} a verb, or one beside a "
                        f"{NO_EXAMPLE!r} line",
                    )

    def test_a_verb_bearing_tool_points_at_its_verbs(self) -> None:
        """The top-level help of a verb-bearing tool must not be a dead end."""
        for name in registry():
            top = help_text(name)
            verbs = verbs_of(top)
            if not verbs or all(help_text(name, verb) == top for verb in verbs):
                continue
            with self.subTest(tool=name):
                self.assertIn("<verb> --help", section_of(top))

    def test_every_shown_invocation_names_its_own_tool(self) -> None:
        """A pasted transcript from the wrong tool is the defect to catch."""
        for name in registry():
            for entry in self.sections(name):
                for line in entry[1].splitlines():
                    stripped = line.strip()
                    if not stripped.startswith("$ "):
                        continue
                    with self.subTest(tool=name, command=stripped):
                        self.assertIn(name, stripped)

    def test_a_shared_help_page_still_names_every_verb(self) -> None:
        """No verb may hide behind its siblings' transcripts."""
        for name in registry():
            top = help_text(name)
            verbs = verbs_of(top)
            if not verbs or any(help_text(name, verb) != top for verb in verbs):
                continue
            section = section_of(top)
            for verb in verbs:
                with self.subTest(tool=name, verb=verb):
                    self.assertIn(f"{name} {verb}", section)


class ListingGroupTests(unittest.TestCase):
    """`tpt --list` groups by purpose, and the grouping cannot drift.

    tmt validates registry entries against a closed key set, so tmt.json cannot
    carry a `group` field; the table lives in tools/tpt instead. Nothing but
    these assertions and `tpt --check` keeps the two in step.
    """

    def listing(self, *extra: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [str(LAUNCHER), "--list", *extra], capture_output=True, text=True, cwd=ROOT,
        )

    def test_every_registered_tool_lands_in_exactly_one_group(self) -> None:
        result = self.listing("--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)
        self.assertEqual({row["name"] for row in rows}, set(registry()))
        for row in rows:
            with self.subTest(tool=row["name"]):
                self.assertIsNotNone(
                    row["group"], f"{row['name']}: add it to GROUPS in tools/tpt"
                )

    def test_the_listing_prints_groups_rather_than_one_flat_column(self) -> None:
        result = self.listing()
        self.assertEqual(result.returncode, 0, result.stderr)
        groups = {
            row["group"] for row in json.loads(self.listing("--json").stdout)
        }
        self.assertGreater(len(groups), 1, "a single group is not a grouping")
        for group in groups:
            with self.subTest(group=group):
                self.assertIn(f"{group}:", result.stdout)
        self.assertNotIn("ungrouped", result.stdout)

    def test_the_acquisition_group_states_where_its_output_may_not_go(self) -> None:
        """The licensed text it retrieves may not land in the checkout, and the
        note has to say so — that constraint is why the group exists, even now
        that it also holds the tool which spends on a model rather than a
        socket."""
        result = self.listing()
        section = result.stdout.split("acquisition:", 1)
        self.assertEqual(len(section), 2, "no acquisition group in the listing")
        note = section[1].split("\n\n", 1)[0]
        self.assertIn("never enters the repository", " ".join(note.split()))

    def test_the_launcher_check_fails_on_a_tool_no_group_claims(self) -> None:
        """The guard has to fail on a real gap, not merely exist."""
        loader = importlib.machinery.SourceFileLoader("tpt_launcher", str(LAUNCHER))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        launcher = importlib.util.module_from_spec(spec)
        loader.exec_module(launcher)
        problems = launcher.check_groups({**registry(), "brand-new-tool": {}})
        self.assertTrue(
            any("brand-new-tool" in problem for problem in problems),
            f"an ungrouped tool passed the check: {problems}",
        )
        self.assertEqual(launcher.check_groups(registry()), [])


class ReachTests(unittest.TestCase):
    """What a tool reaches is declared, and the declaration is checked.

    Exactly one registered tool opens a socket and exactly one calls a model.
    That is the property a reader is being asked to trust before running
    anything, and a convention alone would not keep it: a tool that grows a
    `urlopen` and forgets its declaration has to fail here, or the listing
    starts lying.

    The patterns are deliberately crude. A body that mentions `urlopen` in a
    string it never calls will fail this test, and the fix is to declare the
    reach or stop mentioning it — which is the right trade when the alternative
    is a silent network call.

    They are also a floor, not a proof. A model can be reached by shelling out
    as easily as by importing an SDK, which is how `harvest` reaches one, so the
    model patterns cover the CLI form too — but no grep can enumerate every way
    a subprocess might spend money, and the declaration remains the claim these
    only defend.
    """

    NETWORK_CALLS = re.compile(
        r"\b("
        r"urlopen|urllib\.request|urllib\.error"
        r"|requests\.(?:get|post|put|patch|delete|head|request|Session)"
        r"|httpx\.|aiohttp\.|http\.client|socket\.(?:socket|create_connection)"
        r"|ftplib|smtplib|telnetlib|paramiko"
        r")"
    )
    MODEL_CALLS = re.compile(
        r"\b("
        r"anthropic|openai|Anthropic\(|OpenAI\("
        r"|messages\.create|chat\.completions|generate_content"
        r"|ollama|litellm|langchain"
        # Shelling out to an agent CLI: the named constant a tool holds it in,
        # or the command written out with its non-interactive flag.
        r"|claude_cli|claude\s+(?:-p|--print)\b"
        r")",
        re.I,
    )

    def declarations(self) -> dict[str, str]:
        rows = json.loads(subprocess.run(
            [str(LAUNCHER), "--list", "--json"], capture_output=True, text=True, cwd=ROOT,
        ).stdout)
        return {row["name"]: row["reaches"] for row in rows}

    def body(self, name: str) -> str:
        """The tool's own code, without full-line comments or its transcripts.

        A captured example prints what a tool did, and prose explains why; a
        call is neither. Scanning them would make an accurate warning about the
        network read as a network call.
        """
        text = (TOOLS / name).read_text(encoding="utf-8", errors="replace")
        head, marker, tail = text.partition("\nEXAMPLES = {")
        if marker:
            text = head + tail.partition("\n}\n")[2]
        return "\n".join(
            line for line in text.splitlines() if not line.lstrip().startswith("#")
        )

    def test_every_tool_declares_what_it_reaches(self) -> None:
        declared = self.declarations()
        self.assertEqual(set(declared), set(registry()))
        for name, reach in declared.items():
            with self.subTest(tool=name):
                self.assertIn(reach, ("network", "model", "nothing"))

    def test_a_tool_that_opens_a_socket_declares_the_network(self) -> None:
        declared = self.declarations()
        for name in registry():
            with self.subTest(tool=name):
                found = self.NETWORK_CALLS.search(self.body(name))
                if declared[name] == "network":
                    self.assertIsNotNone(
                        found,
                        f"{name} declares the network but makes no call; "
                        "declare 'nothing' instead",
                    )
                else:
                    self.assertIsNone(
                        found,
                        f"{name} reaches the network via {found.group(0) if found else ''!r} "
                        "but does not declare it; set REACHES in scripts/_tooling.py",
                    )

    def test_a_tool_that_calls_a_model_declares_it(self) -> None:
        declared = self.declarations()
        for name in registry():
            with self.subTest(tool=name):
                found = self.MODEL_CALLS.search(self.body(name))
                if declared[name] == "model":
                    self.assertIsNotNone(found, f"{name} declares a model but calls none")
                else:
                    self.assertIsNone(
                        found,
                        f"{name} calls a model via {found.group(0) if found else ''!r} "
                        "but does not declare it; set REACHES in scripts/_tooling.py",
                    )

    def test_exactly_two_tools_reach_outside_and_the_listing_says_so(self) -> None:
        """The measured fact, and the sentence a reader is shown, must agree.

        Two, and which two, is the whole claim: `harvest ask` calls a model and
        `knox-bible` opens a socket, and nothing else does either. A third name
        appearing here is a tool that started spending outside this machine, and
        it should have to be added deliberately rather than noticed later.
        """
        declared = self.declarations()
        outward = sorted(n for n, r in declared.items() if r != "nothing")
        self.assertEqual(outward, ["harvest", "knox-bible"], "the reach story has changed")
        self.assertEqual(declared["harvest"], "model")
        self.assertEqual(declared["knox-bible"], "network")
        listing = subprocess.run(
            [str(LAUNCHER), "--list"], capture_output=True, text=True, cwd=ROOT,
        ).stdout
        self.assertIn("reaches the network: knox-bible", listing)
        self.assertIn("calls a model: harvest", listing)
        self.assertIn(
            "No other registered tool reaches the network or calls a model", listing
        )

    def test_the_acquisition_group_claims_every_outward_tool(self) -> None:
        rows = {
            row["name"]: row for row in json.loads(subprocess.run(
                [str(LAUNCHER), "--list", "--json"],
                capture_output=True, text=True, cwd=ROOT,
            ).stdout)
        }
        for name, row in rows.items():
            with self.subTest(tool=name):
                if row["reaches"] != "nothing":
                    self.assertEqual(row["group"], "acquisition")

    def test_harvest_names_the_one_verb_of_it_that_calls_a_model(self) -> None:
        """Six of its seven verbs reach nothing; the help must say which is which.

        `record` carries its own sentence, because that is the verb holding
        --model and a reader who jumps straight to it never sees the tool's
        preamble — and because after `ask` landed, `record`'s --model is the one
        place left where a run could still be stamped by hand.
        """
        for argv, wanted in (
            (("harvest",), "One verb calls a model: `ask`, and nothing else here"),
            (("harvest", "ask"), "The only verb here that reaches outside this machine."),
            (("harvest", "record"), "Nothing here calls a model or opens a socket."),
        ):
            with self.subTest(target=" ".join(argv)):
                flattened = " ".join(help_text(*argv).split())
                self.assertIn(wanted, flattened)

    def test_ask_is_dry_runnable_without_reaching_anything(self) -> None:
        """The verb that spends must be answerable about what it would spend.

        A `claude` that records having been run shadows the real one, so this
        asserts the dry run did not invoke it rather than assuming so. Emptying
        PATH instead would prove nothing: the launcher's own `env python3`
        could not resolve either, and the failure would look the same.
        """
        with tempfile.TemporaryDirectory() as scratch:
            shim, marker = Path(scratch) / "claude", Path(scratch) / "asked"
            shim.write_text(f'#!/bin/sh\necho "$@" >{marker}\n', encoding="utf-8")
            shim.chmod(0o755)
            shadowed = {**os.environ, "PATH": f"{scratch}{os.pathsep}{os.environ['PATH']}"}
            result = subprocess.run(
                [str(LAUNCHER), "harvest", "ask", "--passage", "Psalms 24",
                 "--runs", "3", "--dry-run", "--json"],
                capture_output=True, text=True, cwd=ROOT, env=shadowed,
            )
            self.assertFalse(marker.exists(), "a dry run invoked the model CLI")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "dry-run")
        self.assertEqual(payload["queries"], payload["passages"] * payload["runs"])
        self.assertIn("Psalms 24", payload["prompt"])


class ToolSmokeTests(unittest.TestCase):
    """tests/tools/<id>.test are tmt's stable-gate smoke tests."""

    def test_every_registered_tool_has_a_smoke_test(self) -> None:
        missing = sorted(
            name for name in registry()
            if not (ROOT / "tests" / "tools" / f"{name}.test").is_file()
        )
        self.assertEqual(missing, [], f"tools without a smoke test: {missing}")

    def test_smoke_tests_are_executable(self) -> None:
        for script in sorted((ROOT / "tests" / "tools").glob("*.test")):
            with self.subTest(test=script.name):
                self.assertTrue(os.access(script, os.X_OK))

    def test_shell_smoke_tests_pass(self) -> None:
        """Run all forty, concurrently, and assert each one exactly as before.

        Between them these scripts start 421 cold tools, and a tool composes
        others as further processes, so nearly all of the wall time is this
        process waiting on another. Run one after another it was the longest
        thing in the suite by a wide margin.

        They are safe to overlap because each already builds its own sandbox:
        thirty-nine call `mktemp -d` and write only inside it, and the fortieth
        (`tpt.test`) only reads the registry. Nothing here writes into the
        repository, which was checked rather than assumed --- and it is the
        property to re-check before adding a script that wants a fixed path.

        Threads rather than processes because `subprocess.run` waits with the
        GIL released. Every assertion stays where it was: the scripts are run
        concurrently, then judged one at a time, so a failure still names its
        own script through `subTest` and reports that script's own output.
        """
        suite = sorted((ROOT / "tests" / "tools").glob("*.test"))
        self.assertTrue(suite, "no shell smoke tests found")

        def run(script: Path) -> subprocess.CompletedProcess:
            return subprocess.run(
                ["sh", str(script)], capture_output=True, text=True, cwd=ROOT,
            )

        workers = min(len(suite), (os.cpu_count() or 1) * 2)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(run, suite))

        for script, result in zip(suite, results):
            with self.subTest(test=script.name):
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
