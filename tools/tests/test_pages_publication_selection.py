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
    ("tools/tpt", "browser-products", "build"),
    ("tools/tpt", "document-schema", "check", "--include-sources"),
    ("tools/tpt", "artifact-store", "check"),
    ("tools/tpt", "snapshot-store", "check"),
    ("scripts/_papal_input_receipt.py", "check"),
    ("tools/tpt", "document-library", "check"),
    ("tools/tpt", "source-library", "validate"),
    ("tools/tpt", "calendar-days", "check"),
    ("tools/tpt", "check-calendar-masses"),
    ("tools/tpt", "mass-propers", "structure", "--check"),
    ("tools/tpt", "calendar-rubrics", "check"),
    ("tools/tpt", "mass-ordinary", "check"),
}
AUDIT_COMMANDS = {
    ("scripts/_act_history_projection_receipt.py", "check"),
    ("tools/tpt", "source-reader", "structure", "--check-receipt"),
}
GENERATED_CONSUMERS = {
    ("tools/tpt", "document-schema", "check", "--include-sources"),
    ("tools/tpt", "document-library", "check"),
    ("tools/tpt", "calendar-days", "check"),
    ("tools/tpt", "mass-propers", "structure", "--check"),
    ("tools/tpt", "calendar-rubrics", "check"),
    ("tools/tpt", "mass-ordinary", "check"),
}
CACHE_ACTION = "55cc8345863c7cc4c66a329aec7e433d2d1c52a9"
PRODUCT_IDENTITY = "a" * 64
PRINT_IDENTITY = "b" * 64
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
        scratch = ROOT / ".scratch/prepared-publisher/ci-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="source-pages-", dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.write("Makefile", (ROOT / "Makefile").read_text(encoding="utf-8"))
        self.write("src/gpt/study/main.tex", "Canonical source, with no installed PDF.\n")
        self.write("src/gpt/held/main.tex", "Held canonical source.\n")
        self.write("src/common/preamble.tex", "% fixture\n")
        # The real workflow's presence probe runs unchanged. Descriptor authority
        # and bytes are checked at the browser-products boundary, not this stub.
        self.write("scripts/_browser_products.py", '''import json
from pathlib import Path
def load_manifest(root):
    return json.loads((root / "release/browser-products.json").read_text())
def cache_directory(root):
    return root / "build/browser-data"
''')
        self.bin = self.root / "bin"
        self.log = self.root / "commands.jsonl"
        self.env = {**os.environ, "PATH": f"{self.bin}{os.pathsep}{os.environ['PATH']}",
                    "GITHUB_WORKSPACE": str(self.root), "PYTHONDONTWRITEBYTECODE": "1",
                    "DEPLOYMENT_TEST_LOG": str(self.log), "DEPLOYMENT_TEST_ROOT": str(self.root),
                    "DEPLOYMENT_TEST_SOURCE_COMMANDS": json.dumps(sorted(SOURCE_COMMANDS | AUDIT_COMMANDS)),
                    "DEPLOYMENT_TEST_GENERATED_CONSUMERS": json.dumps(sorted(GENERATED_CONSUMERS | AUDIT_COMMANDS)),
                    "DEPLOYMENT_TEST_PRODUCT_IDENTITY": PRODUCT_IDENTITY,
                    "GITHUB_OUTPUT": str(self.root / "workflow-output"),
                    "GITHUB_PATH": str(self.root / "workflow-path"),
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
generated = {tuple(command) for command in json.loads(os.environ["DEPLOYMENT_TEST_GENERATED_CONSUMERS"])}
ready = root / "build/browser-data/verified-ready"
if " ".join(args) == os.environ.get("DEPLOYMENT_TEST_FAIL"):
    raise SystemExit("deliberate source gate failure")
if args == ["-"]:
    exec(compile(sys.stdin.read(), "workflow-stdin", "exec"))
elif args == ["tools/tpt", "browser-products", "key"]:
    print(os.environ["DEPLOYMENT_TEST_PRODUCT_IDENTITY"])
elif args == ["tools/tpt", "browser-products", "build"]:
    ready.parent.mkdir(parents=True, exist_ok=True)
    ready.write_text("exact current products verified; no evidence downloads\n")
elif args == ["tools/tpt", "browser-products", "prune"]:
    if not ready.is_file():
        raise SystemExit("cache retention ran before product verification")
elif args == ["scripts/_browser_cache_bootstrap.py", "--fetch"]:
    if os.environ.get("DEPLOYMENT_TEST_BOOTSTRAP_PRINT") == "1":
        (root / "build/browser-data" / ("b" * 64) / "data").mkdir(parents=True)
elif args == ["scripts/_install_web_print_pandoc.py", "--fetch", "--bin-dir", ".scratch/web-print-toolchain/bin"]:
    pass  # Pinned package and binary authentication have their own fixture tests.
elif args == ["scripts/_web_print_assets.py", "hydrate", "--fetch"]:
    pass  # Explicit source-bound delivery; publication itself cannot fetch.
elif args == ["scripts/_web_print_marks.py", "hydrate", "--fetch"]:
    pass  # The separate source-mark face is needed only by a cold print family.
elif args == ["scripts/_native_tex_assets.py", "hydrate", "--fetch"]:
    pass  # Verify browser compiler inputs; no compiler executes in deployment.
elif tuple(args) in allowed:
    if tuple(args) in generated and not ready.is_file():
        raise SystemExit("generated consumer ran before browser product preparation")
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
    if not ready.is_file():
        raise SystemExit("publication ran before product verification")
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

    def run_pages_commands(self, *, env=None, cache_hit=False):
        descriptor = self.root / "release/browser-products.json"
        if not descriptor.exists():
            self.write("release/browser-products.json", json.dumps({"products": [
                {"id": "print-editions", "key": PRINT_IDENTITY},
                {"id": "calendar-days", "key": "c" * 64},
            ]}))
        for step in self.pages()["jobs"]["deploy"]["steps"]:
            if cache_hit and step.get("if") == "steps.browser-cache.outputs.cache-hit != 'true'":
                continue
            if step.get("if") == "steps.browser-print.outputs.required == 'true'":
                outputs = Path((env or self.env)["GITHUB_OUTPUT"]).read_text().splitlines()
                required = [line for line in outputs if line.startswith("required=")][-1]
                if required != "required=true":
                    continue
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

    def test_tracked_browser_products_and_historical_snapshots_block_publication(self):
        subprocess.run(["git", "init", "-q", "-b", "feature/no-pdfs"], cwd=self.root,
                       check=True, capture_output=True)
        for name, error in (
            ("src/web/data/unexpected.json", "Generated browser products must live in the validated content cache"),
            ("release/papal-documents/inputs/unexpected.json", "Historical papal input snapshots must be preserved outside Git"),
            ("build/browser-data/unexpected.json", "Browser product caches must remain untracked"),
        ):
            with self.subTest(name=name):
                self.write(name, '{"unexpected": true}\n')
                subprocess.run(["git", "add", "--force", name], cwd=self.root,
                               check=True, capture_output=True)
                result = self.shell("make")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(error, result.stderr)
                self.assertFalse((self.root / "build/public-alpha/site/index.html").exists())
                subprocess.run(["git", "rm", "--force", name], cwd=self.root,
                               check=True, capture_output=True)

    def test_ignored_untracked_browser_cache_does_not_block_publication(self):
        subprocess.run(["git", "init", "-q", "-b", "feature/no-pdfs"], cwd=self.root,
                       check=True, capture_output=True)
        self.write(".gitignore", "build/\n")
        result = self.shell("make")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        ready = "build/browser-data/verified-ready"
        self.assertTrue((self.root / ready).is_file())
        ignored = subprocess.run(["git", "check-ignore", ready], cwd=self.root,
                                 capture_output=True, text=True, check=True)
        self.assertEqual(ignored.stdout.strip(), ready)
        tracked = subprocess.run(["git", "ls-files", "--", "build/browser-data"], cwd=self.root,
                                 capture_output=True, text=True, check=True)
        self.assertEqual(tracked.stdout, "")

    def test_plain_make_defaults_to_the_source_site_without_typesetting(self):
        result = self.shell("make")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.root / "build/public-alpha/site/index.html").is_file())
        self.assertEqual(list(self.root.rglob("*.pdf")), [])
        for command in SOURCE_COMMANDS:
            with self.subTest(command=command):
                self.assertEqual(self.commands().count(command), 1)
        self.assertFalse(AUDIT_COMMANDS & set(self.commands()))

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
        prepared = ("tools/tpt", "browser-products", "build")
        for command in GENERATED_CONSUMERS:
            self.assertLess(commands.index(prepared), commands.index(command))
        for command in SOURCE_COMMANDS:
            self.assertLess(commands.index(command), commands.index(build))
        self.assertLess(commands.index(rights[0]), commands.index(build))
        runtime = ("scripts/_native_tex_assets.py", "hydrate", "--fetch")
        self.assertEqual(commands.count(runtime), 1)
        self.assertLess(commands.index(runtime), commands.index(build))
        self.assertLess(commands.index(build), commands.index(verify))
        self.assertFalse(AUDIT_COMMANDS & set(commands))
        self.assertFalse((self.root / "pdf").exists())
        self.assertEqual(list(self.root.rglob("*.pdf")), [])

    def test_each_new_source_gate_failure_prevents_artifact_construction(self):
        for gate in ["scripts/_native_tex_assets.py hydrate --fetch",
                     "tools/tpt browser-products key", "scripts/_browser_cache_bootstrap.py --fetch",
                     "scripts/_install_web_print_pandoc.py --fetch --bin-dir .scratch/web-print-toolchain/bin",
                     "scripts/_web_print_assets.py hydrate --fetch",
                     "scripts/_web_print_marks.py hydrate --fetch",
                     *sorted(" ".join(command) for command in SOURCE_COMMANDS)]:
            with self.subTest(gate=gate):
                self.log.unlink(missing_ok=True)
                Path(self.env["GITHUB_OUTPUT"]).unlink(missing_ok=True)
                shutil.rmtree(self.root / "build", ignore_errors=True)
                result = self.run_pages_commands(env={**self.env, "DEPLOYMENT_TEST_FAIL": gate})
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("deliberate source gate failure", result.stderr)
                self.assertNotIn(("tools/tpt", "public-alpha", "build"), self.commands())
                self.assertFalse((self.root / "build/public-alpha/site").exists())

    def test_consumers_prepare_products_once_before_serial_or_parallel_reads(self):
        for jobs in ("-j1", "-j4"):
            with self.subTest(jobs=jobs):
                self.log.unlink(missing_ok=True)
                shutil.rmtree(self.root / "build", ignore_errors=True)
                result = self.shell(f"make {jobs} check-document-schemas check-document-catalogue check-source-projection check-act-history-receipt")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                commands = self.commands()
                prepared = ("tools/tpt", "browser-products", "build")
                self.assertEqual(commands.count(prepared), 1)
                for consumer in GENERATED_CONSUMERS & set(commands):
                    self.assertLess(commands.index(prepared), commands.index(consumer))
                for audit in AUDIT_COMMANDS:
                    self.assertEqual(commands.count(audit), 1)
                    self.assertLess(commands.index(prepared), commands.index(audit))

    def test_invalid_product_identity_never_reaches_cache_preparation(self):
        for identity in ("", "not-a-content-hash", PRODUCT_IDENTITY + "\nextra=untrusted"):
            with self.subTest(identity=identity):
                self.log.unlink(missing_ok=True)
                result = self.run_pages_commands(env={**self.env, "DEPLOYMENT_TEST_PRODUCT_IDENTITY": identity})
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Invalid browser product content identity", result.stderr)
                self.assertNotIn(("tools/tpt", "browser-products", "build"), self.commands())

    def test_exact_cache_hit_still_verifies_products_and_skips_cache_retention(self):
        ready = self.root / "build/browser-data/verified-ready"
        ready.parent.mkdir(parents=True)
        ready.write_text("restored candidate bytes, still requiring verification\n")
        (ready.parent / PRINT_IDENTITY / "data").mkdir(parents=True)
        result = self.run_pages_commands(cache_hit=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        commands = self.commands()
        self.assertEqual(commands.count(("tools/tpt", "browser-products", "build")), 1)
        self.assertEqual(commands.count(("scripts/_native_tex_assets.py", "hydrate", "--fetch")), 1)
        self.assertNotIn(("tools/tpt", "browser-products", "prune"), commands)
        self.assertNotIn(("tools/tpt", "document-library", "structure", "--check"), commands)
        self.assertNotIn(("tools/tpt", "act-history", "structure", "--check"), commands)
        self.assertFalse(AUDIT_COMMANDS & set(commands))
        self.assertFalse(any(command[0] in {"scripts/_install_web_print_pandoc.py", "scripts/_web_print_assets.py", "scripts/_web_print_marks.py"}
                             for command in commands))

    def test_bootstrapped_print_family_skips_compiler_and_asset_delivery_on_actions_miss(self):
        result = self.run_pages_commands(env={**self.env, "DEPLOYMENT_TEST_BOOTSTRAP_PRINT": "1"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        commands = self.commands()
        self.assertIn(("scripts/_browser_cache_bootstrap.py", "--fetch"), commands)
        self.assertFalse(any(command[0] in {"scripts/_install_web_print_pandoc.py", "scripts/_web_print_assets.py", "scripts/_web_print_marks.py"}
                             for command in commands))
        self.assertIn(("tools/tpt", "browser-products", "build"), commands)

    def test_cold_print_dependencies_precede_product_build_and_warm_presence_is_not_authority(self):
        result = self.run_pages_commands()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        commands = self.commands()
        compiler = ("scripts/_install_web_print_pandoc.py", "--fetch", "--bin-dir", ".scratch/web-print-toolchain/bin")
        assets = ("scripts/_web_print_assets.py", "hydrate", "--fetch")
        marks = ("scripts/_web_print_marks.py", "hydrate", "--fetch")
        build = ("tools/tpt", "browser-products", "build")
        self.assertLess(commands.index(compiler), commands.index(build))
        self.assertLess(commands.index(assets), commands.index(build))
        self.assertLess(commands.index(assets), commands.index(marks))
        self.assertLess(commands.index(marks), commands.index(build))
        (self.root / "build/browser-data" / PRINT_IDENTITY / "data").mkdir(parents=True)
        self.log.unlink()
        Path(self.env["GITHUB_OUTPUT"]).unlink()
        result = self.run_pages_commands(cache_hit=True, env={**self.env, "DEPLOYMENT_TEST_FAIL": " ".join(build)})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("deliberate source gate failure", result.stderr)
        self.assertNotIn(compiler, self.commands())
        self.assertNotIn(assets, self.commands())
        self.assertNotIn(marks, self.commands())
        self.assertNotIn(("tools/tpt", "public-alpha", "verify", "--deployment-target", "github-pages"), self.commands())

    def test_cache_keys_are_content_addressed_and_candidates_are_verified_before_save(self):
        steps = self.pages()["jobs"]["deploy"]["steps"]
        by_name = {step["name"]: step for step in steps}
        restore = by_name["Restore browser product candidates"]
        save = by_name["Save verified browser products"]
        self.assertEqual(restore["uses"], f"actions/cache/restore@{CACHE_ACTION}")
        self.assertEqual(save["uses"], f"actions/cache/save@{CACHE_ACTION}")
        self.assertEqual(restore["with"]["path"], "build/browser-data")
        self.assertEqual(save["with"]["path"], restore["with"]["path"])
        self.assertEqual(save["with"]["key"], restore["with"]["key"])
        self.assertEqual(restore["with"]["key"],
                         "triptych-browser-products-v1-${{ steps.browser-products.outputs.identity }}")
        self.assertEqual(restore["with"]["restore-keys"].strip(), "triptych-browser-products-v1-")
        names = [step["name"] for step in steps]
        self.assertLess(names.index("Identify exact browser products"), names.index(restore["name"]))
        self.assertLess(names.index(restore["name"]), names.index("Validate sources and build public artifact"))
        self.assertLess(names.index("Retain verified current browser products"), names.index(save["name"]))
        self.assertLess(names.index("Validate sources and build public artifact"),
                        names.index("Retain verified current browser products"))
        self.assertLess(names.index(save["name"]), names.index("Verify artifact and GitHub Pages compatibility"))
        self.assertEqual(save["if"], "steps.browser-cache.outputs.cache-hit != 'true'")

    def test_pages_assembles_browser_compiler_assets_without_executing_pdf_toolchain(self):
        steps = self.pages()["jobs"]["deploy"]["steps"]
        actions = [step["uses"].partition("@")[0] for step in steps if "uses" in step]
        self.assertEqual(actions, ["actions/checkout", "actions/setup-python", "actions/cache", "actions/cache/restore",
                                   "actions/cache/save", "actions/configure-pages",
                                   "actions/upload-pages-artifact", "actions/deploy-pages"])
        upload = next(step for step in steps if step.get("uses", "").startswith("actions/upload-pages-artifact@"))
        self.assertEqual(upload["with"]["path"], "build/public-alpha/site")
        self.assertTrue(upload["with"]["include-hidden-files"])
        checkout = next(step for step in steps if step.get("uses", "").startswith("actions/checkout@"))
        self.assertFalse(checkout["with"]["persist-credentials"])
        runtime = next(step for step in steps if step["name"] == "Restore native TeX runtime candidates")
        self.assertEqual(runtime["uses"], f"actions/cache@{CACHE_ACTION}")
        self.assertEqual(runtime["with"]["path"], ".scratch/native-tex-runtime")
        self.assertEqual(runtime["with"]["key"],
                         "triptych-native-tex-v1-${{ hashFiles('src/common/native-tex-runtime.json') }}")
        converter = next(step for step in steps if step["name"] == "Install pinned HTML converter for cold print preparation")
        assets = next(step for step in steps if step["name"] == "Hydrate source-bound assets for cold print preparation")
        marks = next(step for step in steps if step["name"] == "Hydrate source-bound marks for cold print preparation")
        self.assertEqual(converter["if"], "steps.browser-print.outputs.required == 'true'")
        self.assertEqual(assets["if"], converter["if"])
        self.assertEqual(marks["if"], converter["if"])
        commands = "\n".join(step.get("run", "") for step in steps)
        self.assertNotRegex(commands, r"(?i)\b(?:texlive|pdflatex|xelatex|lualatex|pdfinfo|poppler|docker|apt-get|pacman)\b")


if __name__ == "__main__":
    unittest.main()
