"""Registry drift: tmt.json, tools/, and the Makefile must agree.

Every failure here has shipped at least once. The Makefile invoked a tool by
its filename rather than its registry id, the registry advertised a tool with
no implementation, and a tool body moved without its callers.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "tmt.json"
TOOLS = ROOT / "tools"
LAUNCHER = ROOT / "tools" / "tpt"

# tools/tpt's own verbs. A registry id matching one would shadow it.
LAUNCHER_VERBS = {"list", "tools", "run", "help", "path"}
# tmt ignores subdirectories and these companion suffixes when scanning tools/.
COMPANION_SUFFIXES = (".md", ".test")
# tmt's registry validator caps the field.
PURPOSE_LIMIT = 80


def registry() -> dict[str, dict]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["tools"]


class ToolRegistryTests(unittest.TestCase):
    def test_every_id_resolves_to_an_executable(self) -> None:
        for name in registry():
            with self.subTest(tool=name):
                resolved = subprocess.run(
                    [str(LAUNCHER), "path", name],
                    capture_output=True, text=True, cwd=ROOT,
                )
                self.assertEqual(resolved.returncode, 0, resolved.stderr)
                path = Path(resolved.stdout.strip())
                self.assertTrue(path.is_file(), f"{name}: {path} is not a file")
                self.assertTrue(os.access(path, os.X_OK), f"{name}: {path} not executable")

    def test_every_implementation_is_registered(self) -> None:
        registered = set(registry())
        for path in sorted(TOOLS.iterdir()):
            if not path.is_file() or path.name.endswith(COMPANION_SUFFIXES):
                continue
            with self.subTest(tool=path.name):
                resolved = {
                    Path(subprocess.run(
                        [str(LAUNCHER), "path", name],
                        capture_output=True, text=True, cwd=ROOT,
                    ).stdout.strip()).name
                    for name in registered
                }
                self.assertIn(path.name, resolved)

    def test_no_id_shadows_a_launcher_verb(self) -> None:
        self.assertEqual(set(registry()) & LAUNCHER_VERBS, set())

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
                result = subprocess.run(
                    [str(LAUNCHER), "path", name], capture_output=True, text=True, cwd=ROOT,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(Path(result.stdout.strip()), TOOLS / name)


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
        suite = sorted((ROOT / "tests" / "tools").glob("*.test"))
        self.assertTrue(suite, "no shell smoke tests found")
        for script in suite:
            with self.subTest(test=script.name):
                result = subprocess.run(
                    ["sh", str(script)], capture_output=True, text=True, cwd=ROOT,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
