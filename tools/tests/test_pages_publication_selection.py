"""Run Pages' source commands with real Make and isolated boundary doubles.

Every source gate is observable, can fail, and accepts only its source
invocation. The owning suites validate tool behavior and release selection;
this suite never repeats their full corpus builds.
"""
from __future__ import annotations

from collections import Counter
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]

# Independent coverage contract: changing the gate requires a coverage decision.
SOURCE_COMMANDS = {
    ("scripts/_act_history_projection_receipt.py", "check"),
    ("tools/tpt", "document-schema", "check", "--include-sources"),
    ("tools/tpt", "artifact-store", "check"),
    ("tools/tpt", "document-library", "check"),
    ("tools/tpt", "document-library", "structure", "--check"),
    ("tools/tpt", "source-library", "validate"),
    ("tools/tpt", "source-reader", "structure", "--check-receipt"),
    ("tools/tpt", "calendar-days", "check"),
    ("tools/tpt", "check-calendar-masses"),
    ("tools/tpt", "mass-propers", "structure", "--check"),
    ("tools/tpt", "calendar-rubrics", "check"),
    ("tools/tpt", "mass-ordinary", "check"),
}
RIGHTS_TESTS = {
    "test_hash_only_registry_is_complete_and_well_formed",
    "test_allowlist_exactly_matches_tracked_curriculum_sources",
    "test_unavailable_dispositions_cover_affected_stable_ids",
    "test_scanner_is_location_and_surface_sensitive",
    "test_tex_control_words_cannot_hide_a_window",
}


class DeploymentFixture:
    """No real print program, package install, cache restore or network runs."""

    def setUp(self):
        scratch = ROOT / ".scratch/deployment-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="source-pages-", dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.write("Makefile", (ROOT / "Makefile").read_text(encoding="utf-8"))
        self.write("src/gpt/study/main.tex", "Canonical source, with no installed PDF.\n")
        self.write("src/gpt/held/main.tex", "Held canonical source.\n")
        self.write("src/common/preamble.tex", "% fixture\n")
        self.bin = self.root / "bin"
        self.log = self.root / "commands.jsonl"
        self.env = {**os.environ, "PATH": f"{self.bin}{os.pathsep}{os.environ['PATH']}",
                    "GITHUB_WORKSPACE": str(self.root), "PYTHONDONTWRITEBYTECODE": "1",
                    "DEPLOYMENT_TEST_LOG": str(self.log), "DEPLOYMENT_TEST_ROOT": str(self.root),
                    "DEPLOYMENT_TEST_SOURCE_COMMANDS": json.dumps(sorted(SOURCE_COMMANDS)),
                    "DEPLOYMENT_TEST_RIGHTS": json.dumps(sorted(RIGHTS_TESTS))}
        for name in ("MAKEFLAGS", "MFLAGS", "MAKELEVEL", "MAKEOVERRIDES"):
            self.env.pop(name, None)
        python = self.write("bin/python", f"#!{sys.executable}\n" + r'''
import json
import os
from pathlib import Path
import sys

args = sys.argv[1:]
root = Path(os.environ["DEPLOYMENT_TEST_ROOT"])
with open(os.environ["DEPLOYMENT_TEST_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps(args) + "\n")
allowed = {tuple(command) for command in json.loads(os.environ["DEPLOYMENT_TEST_SOURCE_COMMANDS"])}
if tuple(args) in allowed:
    if " ".join(args) == os.environ.get("DEPLOYMENT_TEST_FAIL"):
        raise SystemExit("deliberate source gate failure")
elif args[:3] == ["-m", "unittest", "-v"]:
    actual = {name.rsplit(".", 1)[-1] for name in args[3:]}
    if actual != set(json.loads(os.environ["DEPLOYMENT_TEST_RIGHTS"])):
        raise SystemExit("deployment must run exactly the source-only rights cases")
elif args[:3] == ["-m", "pip", "install"]:
    if "-r" not in args or any("tex" in part.lower() for part in args):
        raise SystemExit("unexpected deployment dependency install")
elif args[:2] == ["tools/tpt", "check-proper-components"] and args[-1] in {"--list-synthesis", "--list-homily"}:
    pass  # Make's parse-time discovery, not PDF compilation.
elif args == ["tools/tpt", "public-alpha", "build"]:
    target = root / "build/public-alpha/site/index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("<html><body>source fixture</body></html>\n")
elif args == ["tools/tpt", "public-alpha", "verify", "--deployment-target", "github-pages"]:
    if not (root / "build/public-alpha/site/index.html").is_file():
        raise SystemExit("verification ran before the source artifact existed")
else:
    raise SystemExit("unexpected or print-dependent deployment command: " + repr(args))
''')
        python.chmod(0o755)
        (self.bin / "python3").symlink_to(python.name)
        for name in ("pdflatex", "xelatex", "lualatex", "pdfinfo", "pdftotext",
                     "pdftoppm", "pacman", "apt-get", "docker", "curl", "wget", "gh"):
            tool = self.write(f"bin/{name}", "#!/bin/sh\n"
                              f"echo 'forbidden deployment executable: {name}' >&2\nexit 99\n")
            tool.chmod(0o755)

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def commands(self):
        return [tuple(json.loads(line)) for line in self.log.read_text().splitlines()] if self.log.exists() else []

    def shell(self, script, *, env=None):
        return subprocess.run(["bash", "-euo", "pipefail", "-c", script], cwd=self.root,
                              env=env or self.env, capture_output=True, text=True, timeout=30)

    def pages(self):
        return yaml.safe_load((ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8"))

    def run_pages_commands(self, *, env=None):
        for step in self.pages()["jobs"]["deploy"]["steps"]:
            if "run" in step:
                result = self.shell(step["run"], env=env)
                if result.returncode:
                    return result
        return result


class PagesPublicationSelectionTests(DeploymentFixture, unittest.TestCase):
    def test_tracked_pdf_blocks_source_publication(self):
        subprocess.run(["git", "init", "-q", "-b", "feature/no-pdfs"], cwd=self.root,
                       check=True, capture_output=True)
        self.write("unexpected.PdF", "%PDF-fixture\n")
        subprocess.run(["git", "add", "--force", "unexpected.PdF"], cwd=self.root,
                       check=True, capture_output=True)
        result = self.shell("make")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Tracked PDFs must be preserved outside Git", result.stderr)
        self.assertFalse((self.root / "build/public-alpha/site/index.html").exists())

    def test_tracked_archives_block_source_publication(self):
        subprocess.run(["git", "init", "-q", "-b", "feature/no-pdfs"], cwd=self.root,
                       check=True, capture_output=True)
        for name in ("hidden.ZiP", "hidden.ZiP.PaRt-001"):
            with self.subTest(name=name):
                self.write(name, "binary archive fixture\n")
                subprocess.run(["git", "add", "--force", name], cwd=self.root,
                               check=True, capture_output=True)
                result = self.shell("make")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Tracked binary archives must be preserved outside Git", result.stderr)
                self.assertFalse((self.root / "build/public-alpha/site/index.html").exists())
                subprocess.run(["git", "rm", "--force", name], cwd=self.root,
                               check=True, capture_output=True)

    def test_plain_make_defaults_to_the_source_site_without_typesetting(self):
        result = self.shell("make")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.root / "build/public-alpha/site/index.html").is_file())
        self.assertEqual(list(self.root.rglob("*.pdf")), [])
        for command in SOURCE_COMMANDS:
            with self.subTest(command=command):
                self.assertEqual(self.commands().count(command), 1)

    def test_actual_pages_commands_run_each_source_gate_once_without_pdf_outputs(self):
        self.assertFalse((self.root / "pdf").exists())
        result = self.run_pages_commands()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        commands = self.commands()
        for command in SOURCE_COMMANDS:
            with self.subTest(command=command):
                self.assertEqual(Counter(commands)[command], 1)
        rights = [command for command in commands if command[:3] == ("-m", "unittest", "-v")]
        self.assertEqual(len(rights), 1)
        build = ("tools/tpt", "public-alpha", "build")
        verify = ("tools/tpt", "public-alpha", "verify", "--deployment-target", "github-pages")
        self.assertEqual(commands.count(build), 1)
        self.assertEqual(commands.count(verify), 1)
        for command in SOURCE_COMMANDS:
            self.assertLess(commands.index(command), commands.index(build))
        self.assertLess(commands.index(rights[0]), commands.index(build))
        self.assertLess(commands.index(build), commands.index(verify))
        self.assertFalse((self.root / "pdf").exists())
        self.assertEqual(list(self.root.rglob("*.pdf")), [])

    def test_each_new_source_gate_failure_prevents_artifact_construction(self):
        for gate in (
            "scripts/_act_history_projection_receipt.py check",
            "tools/tpt document-schema check --include-sources", "tools/tpt artifact-store check",
            "tools/tpt source-library validate",
            "tools/tpt source-reader structure --check-receipt",
        ):
            with self.subTest(gate=gate):
                self.log.unlink(missing_ok=True)
                shutil.rmtree(self.root / "build", ignore_errors=True)
                result = self.run_pages_commands(env={**self.env, "DEPLOYMENT_TEST_FAIL": gate})
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("deliberate source gate failure", result.stderr)
                self.assertNotIn(("tools/tpt", "public-alpha", "build"), self.commands())
                self.assertFalse((self.root / "build/public-alpha/site").exists())

    def test_pages_never_restores_print_artifacts_or_installs_a_print_toolchain(self):
        steps = self.pages()["jobs"]["deploy"]["steps"]
        actions = [step["uses"].partition("@")[0] for step in steps if "uses" in step]
        self.assertEqual(actions, ["actions/checkout", "actions/setup-python", "actions/configure-pages",
                                   "actions/upload-pages-artifact", "actions/deploy-pages"])
        upload = next(step for step in steps if step.get("uses", "").startswith("actions/upload-pages-artifact@"))
        self.assertEqual(upload["with"]["path"], "build/public-alpha/site")
        self.assertTrue(upload["with"]["include-hidden-files"])
        checkout = next(step for step in steps if step.get("uses", "").startswith("actions/checkout@"))
        self.assertFalse(checkout["with"]["persist-credentials"])


if __name__ == "__main__":
    unittest.main()
