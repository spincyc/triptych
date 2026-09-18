"""Execute Pages' actual plan and install scripts against an isolated corpus.

Real release selection and GNU make; fake typesetting and PDF bytes. Held
targets deliberately fail. Neither branch may reach them, even from cache.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = yaml.safe_load((ROOT / ".github/workflows/pages.yml").read_text())
STEPS = {step["name"]: step for step in WORKFLOW["jobs"]["deploy"]["steps"]}
PLAN = "Plan the typesetting against the PDF cache"
COLD = "Prepare the container build script"
WARM = "Install the restored corpus without the typesetting toolchain"
STORE = "Record the typeset PDFs in the store"
PROVIDERS = ("claude", "gpt")
SELECTED = (
    "legacy-release", "legacy-review", "overridden-alpha",
    "study", "study-homily", "study-synthesis",
)
HELD = ("held", "held-homily", "held-synthesis", "overridden-held")


class PagesPublicationSelectionTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/recovery-pages"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="selection-", dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.runner = self.root / "runner"
        self.plan = self.runner / "triptych-plan"
        self.store = self.runner / "triptych-pdf-store"
        self.bin = self.root / "bin"
        self.runner.mkdir()
        self.bin.mkdir()
        self.write("tools/public-alpha", (ROOT / "tools/public-alpha").read_text())
        (self.root / "scripts").symlink_to(ROOT / "scripts", target_is_directory=True)
        self.manifest = {
            "schema_version": 2, "provider": "gpt",
            "providers": ["gpt", "claude"], "publications": [],
        }
        for provider in PROVIDERS:
            for leaf in ("study", "held"):
                for entry in ("main", "synthesis", "homily"):
                    self.write(f"src/{provider}/{leaf}/{entry}.tex", f"{leaf} {entry}\n")
                self.write(f"src/{provider}/{leaf}/proper-components.toml", f"""
schema = 2
record_type = "proper-components"
document = "{leaf}"
appointed_text_completeness = "complete"
[outputs]
research = "{leaf}"
synthesis = "{leaf}-synthesis"
homily = "{leaf}-homily"
web = "{leaf}"
canonical_label = "Full PDF"
synthesis_label = "Synthesis PDF"
homily_label = "Homily PDF"
""")
                for document in (leaf, f"{leaf}-synthesis", f"{leaf}-homily"):
                    self.record(provider, document, "alpha" if leaf == "study" else "hold")
            for document, status in (
                ("legacy-review", "review"), ("legacy-release", "release"),
                ("overridden-held", "release"), ("overridden-alpha", "hold"),
            ):
                self.write(f"src/{provider}/{document}/main.tex", document + "\n")
                self.manifest["publications"].append({
                    "id": document if provider == "gpt" else f"{provider}:{document}",
                    "status": status,
                })
            self.record(provider, "overridden-held", "hold")
            self.record(provider, "overridden-alpha", "alpha")
        self.write_manifest()
        self.write("Makefile", """
PROVIDER ?= gpt
PDFLATEX ?= pdflatex
DOCUMENTS := """ + " ".join(reversed(SELECTED + HELD)) + """
.PHONY: list install FORCE
list:
\t@printf '%s\\n' $(DOCUMENTS)
install: $(addprefix pdf/$(PROVIDER)/,$(addsuffix .pdf,$(DOCUMENTS)))
\t@printf 'install %s: %s\\n' '$(PROVIDER)' '$(DOCUMENTS)' >> install.log
pdf/$(PROVIDER)/%.pdf: build/$(PROVIDER)/%.pdf FORCE
\t@test "$$(cat '$<')" = 'validated $(PROVIDER) $*' || { echo 'metadata validation failed' >&2; exit 1; }
\t@mkdir -p '$(@D)'
\t@cp '$<' '$@'
build/$(PROVIDER)/%.pdf:
\t@case '$*' in held*|overridden-held) echo 'held target reached' >&2; exit 1;; esac
\t@$(PDFLATEX) '$*'
\t@mkdir -p '$(@D)'
\t@printf 'validated %s %s\\n' '$(PROVIDER)' '$*' > '$@'
""" + "\n".join(
            f"build/$(PROVIDER)/{document}.pdf: src/$(PROVIDER)/{owner}/{entry}.tex"
            for document, owner, entry in (
                [(doc, doc, "main") for doc in
                 ("study", "held", "legacy-release", "legacy-review",
                  "overridden-held", "overridden-alpha")]
                + [(f"{leaf}-{mode}", leaf, mode)
                   for leaf in ("study", "held") for mode in ("synthesis", "homily")]
            )
        ) + "\n")
        for tool in ("pdflatex", "pacman"):
            script = self.write(f"bin/{tool}", "#!/bin/sh\n"
                                f"printf '%s\\n' '{tool}' >> toolchain.log\n")
            script.chmod(0o755)
        self.env = {
            **os.environ, **WORKFLOW["env"],
            "PATH": f"{self.bin}{os.pathsep}{os.environ['PATH']}",
            "GITHUB_WORKSPACE": str(self.root), "RUNNER_TEMP": str(self.runner),
            "GITHUB_OUTPUT": str(self.runner / "outputs"),
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        # Do not let a parent make/test runner inject goals or overrides.
        for name in ("MAKEFLAGS", "MFLAGS", "MAKELEVEL"):
            self.env.pop(name, None)

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def record(self, provider, document, status):
        return self.write(f"release/publications/{provider}/{document}.json", json.dumps({
            "schema_version": 1, "id": document, "status": status,
            "catalog": "library/test.md",
            "authorization": None if status == "hold" else "standing",
        }))

    def write_manifest(self):
        self.write("release/public-alpha.json", json.dumps(self.manifest))

    def run_shell(self, script, *, env=None, success=True):
        result = subprocess.run(
            ["bash", "-euo", "pipefail", "-c", script],
            cwd=self.root, env=env or self.env, capture_output=True, text=True,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def step(self, name, **kwargs):
        return self.run_shell(STEPS[name]["run"], **kwargs)

    def plan_run(self, **kwargs):
        (self.runner / "outputs").write_text("")
        return self.step(PLAN, **kwargs)

    def outputs(self):
        return dict(line.split("=", 1) for line in
                    (self.runner / "outputs").read_text().splitlines())

    def keys(self):
        return json.loads((self.plan / "keys.json").read_text())

    def seed_cache(self):
        self.plan_run()
        for provider, documents in self.keys().items():
            for document, key in documents.items():
                (self.store / f"{key}.pdf").write_text(f"validated {provider} {document}\n")
        self.plan_run()
        self.assertEqual(self.outputs()["typesetting"], "none")

    def cold_install(self, **kwargs):
        self.step(COLD)
        env = {
            **self.env, "TRIPTYCH_BAKED": "1",
            "TRIPTYCH_PROVIDERS": (self.plan / "providers.txt").read_text().strip(),
            "TRIPTYCH_MAKE_FLAGS": (self.plan / "make-flags.txt").read_text().strip(),
            "TRIPTYCH_PLAN": str(self.plan),
        }
        return self.run_shell(
            'bash "$RUNNER_TEMP/triptych-toolchain/build.sh"', env=env, **kwargs
        )

    def assert_selection(self):
        self.assertEqual((self.plan / "providers.txt").read_text(), "claude gpt\n")
        self.assertEqual(set(self.keys()), set(PROVIDERS))
        for provider in PROVIDERS:
            self.assertEqual(
                (self.plan / f"documents-{provider}.txt").read_text(),
                " ".join(SELECTED) + "\n",
            )
            self.assertEqual(set(self.keys()[provider]), set(SELECTED))

    def assert_installed(self):
        actual = {
            path.relative_to(self.root / "pdf").with_suffix("").as_posix()
            for path in (self.root / "pdf").rglob("*.pdf")
        }
        self.assertEqual(actual, {f"{p}/{d}" for p in PROVIDERS for d in SELECTED})
        self.assertEqual(set((self.root / "install.log").read_text().splitlines()), {
            f"install {p}: {' '.join(SELECTED)}" for p in PROVIDERS
        })

    def test_cold_cache_installs_only_included_outputs_for_both_providers(self):
        self.plan_run()
        self.assert_selection()
        self.assertEqual(self.outputs()["documents_to_build"], "12")
        self.assertEqual(self.outputs()["typesetting"], "required")
        self.cold_install()
        self.assert_installed()
        self.step(STORE)
        self.assertEqual(len(list(self.store.glob("*.pdf"))), 12)

    def test_full_hit_installs_same_selection_without_typesetting(self):
        self.seed_cache()
        self.assert_selection()
        self.assertEqual(self.outputs()["cache_hits"], "12")
        self.step(WARM)
        self.assert_installed()
        self.assertFalse((self.root / "toolchain.log").exists())

    def test_mixed_hit_preserves_the_selection_in_container_branch(self):
        self.seed_cache()
        (self.store / f"{self.keys()['gpt']['study-homily']}.pdf").unlink()
        self.plan_run()
        self.assertEqual(self.outputs()["documents_to_build"], "1")
        self.assertEqual(self.outputs()["cache_hits"], "11")
        self.cold_install()
        self.assert_installed()

    def test_held_cache_entry_is_neither_restored_nor_retained(self):
        self.seed_cache()
        retired = self.store / ("0" * 64 + ".pdf")
        retired.write_text("old held artifact")
        self.plan_run()
        self.step(WARM)
        self.step(STORE)
        self.assert_installed()
        self.assertFalse(retired.exists())
        self.assertFalse((self.root / "build/claude/held-synthesis.pdf").exists())

    def test_cache_hit_is_still_validated_before_install(self):
        self.seed_cache()
        (self.root / "build/gpt/study.pdf").write_text("invalid metadata")
        result = self.step(WARM, success=False)
        self.assertIn("metadata validation failed", result.stderr)
        self.assertFalse((self.root / "pdf/gpt/study.pdf").exists())

    def test_missing_approved_output_fails_cache_only_install(self):
        self.seed_cache()
        (self.root / "build/gpt/study-homily.pdf").unlink()
        result = self.step(WARM, success=False)
        self.assertIn("The cache plan and the build graph disagree", result.stderr)

    def test_missing_document_plan_fails_both_branches(self):
        self.seed_cache()
        (self.plan / "documents-claude.txt").unlink()
        self.step(WARM, success=False)
        self.cold_install(success=False)
        self.assertFalse((self.root / "install.log").exists())

    def test_hold_only_provider_has_an_explicit_empty_selection(self):
        for document in SELECTED + HELD:
            self.record("gpt", document, "hold")
        self.plan_run()
        self.assertEqual((self.plan / "documents-gpt.txt").read_text(), "\n")
        self.cold_install()
        self.assertFalse((self.root / "pdf/gpt").exists())
        self.step(STORE)
        self.plan_run()
        self.assertEqual(self.outputs()["typesetting"], "none")
        self.step(WARM)
        self.assertFalse((self.root / "pdf/gpt").exists())

    def test_missing_inventory_is_not_treated_as_hold(self):
        (self.root / "release/publications/claude/study-homily.json").unlink()
        result = self.plan_run(success=False)
        self.assertIn("manifest/source mismatch", result.stderr)
        self.assertIn("study-homily", result.stderr)
        self.assertFalse((self.plan / "keys.json").exists())

    def test_inventory_without_a_source_fails_even_when_held(self):
        self.record("gpt", "missing-source", "hold")
        result = self.plan_run(success=False)
        self.assertIn("manifest/source mismatch", result.stderr)
        self.assertIn("missing-source", result.stderr)

    def test_unknown_legacy_status_is_not_silently_excluded(self):
        self.manifest["publications"][0]["status"] = "unknown"
        self.write_manifest()
        result = self.plan_run(success=False)
        self.assertIn("invalid publication status", result.stderr)

    def test_missing_legacy_status_is_not_silently_excluded(self):
        self.manifest["publications"][0].pop("status")
        self.write_manifest()
        result = self.plan_run(success=False)
        self.assertIn("missing publication status", result.stderr)

    def test_unknown_local_status_is_rejected_by_the_owner(self):
        self.record("claude", "held", "unknown")
        result = self.plan_run(success=False)
        self.assertIn("invalid status", result.stderr)

    def test_undeclared_source_provider_is_rejected(self):
        self.write("src/other/extra/main.tex", "extra\n")
        result = self.plan_run(success=False)
        self.assertIn("undeclared source providers", result.stderr)

    def test_make_must_account_for_companions_even_when_held(self):
        path = self.root / "Makefile"
        path.write_text(path.read_text().replace("held-homily ", "", 1))
        result = self.plan_run(success=False)
        self.assertIn("make/source mismatch", result.stderr)

    def test_local_make_install_default_still_includes_held_sources(self):
        result = self.run_shell("make install PROVIDER=gpt", success=False)
        self.assertIn("held target reached", result.stderr)

    def test_container_mounts_the_same_plan_read_only(self):
        run = STEPS["Typeset the outstanding PDFs in the pinned container"]["run"]
        self.assertIn(
            '--volume "${RUNNER_TEMP}/triptych-plan:/triptych-plan:ro"', run
        )
        self.assertIn('--env "TRIPTYCH_PLAN=/triptych-plan"', run)
        self.assertEqual(STEPS[WARM]["if"], "steps.plan.outputs.typesetting == 'none'")
        self.assertEqual(STEPS[COLD]["if"], "steps.plan.outputs.typesetting != 'none'")


if __name__ == "__main__":
    unittest.main()
