from __future__ import annotations

import importlib.machinery
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "tools" / "check-proper-components"
loader = importlib.machinery.SourceFileLoader("proper_components", str(PATH))
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)


def write_component_tree(provider: Path, *, document: str = "proper",
                         appointed_modes: str = '["research"]',
                         treatment_modes: str = '["research"]',
                         integrated_modes: str = '["synthesis"]',
                         integrated: bool = True, swap_tail: bool = False,
                         extra: str = "") -> Path:
    """Write a valid schema-1 leaf at provider/document; return its manifest."""
    leaf = provider / document
    leaf.mkdir(parents=True)
    for name in (
        "main.tex", "synthesis.tex", "appointed.tex", "treatment.tex",
        "brief.tex", "integrated.tex", "grounded.tex", "exploratory.tex",
        "notable.tex", "terminal.tex", "brief-refs.tex",
    ):
        (leaf / name).write_text("% fixture\n", encoding="utf-8")
    components = [
        ("appointed", "appointed-text", "appointed.tex", appointed_modes),
        ("treatment", "proper-treatment", "treatment.tex", treatment_modes),
        ("brief", "brief-synthesis", "brief.tex", '["research", "synthesis"]'),
        ("integrated", "integrated-commentary", "integrated.tex",
         integrated_modes),
        ("grounded", "source-grounded-synthesis", "grounded.tex",
         '["research", "synthesis"]'),
        ("notable", "notable-quotable", "notable.tex",
         '["research", "synthesis"]'),
        ("exploratory", "exploratory-synthesis", "exploratory.tex",
         '["research", "synthesis"]'),
        ("terminal", "terminal-apparatus", "terminal.tex",
         '["research", "synthesis"]'),
    ]
    if not integrated:
        components = [item for item in components if item[0] != "integrated"]
    if swap_tail:
        keys = [item[0] for item in components]
        notable, exploratory = keys.index("notable"), keys.index("exploratory")
        components[notable], components[exploratory] = (
            components[exploratory], components[notable]
        )
    blocks = []
    for key, kind, path, modes in components:
        references = '["brief-refs.tex"]' if key == "brief" else "[]"
        blocks.append(
            f'[[components]]\nkey = "{key}"\nkind = "{kind}"\n'
            f'path = "{path}"\nmodes = {modes}\ndepends_on = []\n'
            f'element_keys = ["introit", "gospel"]\nreferences = {references}\n'
        )
    manifest = (
        f'schema = 1\nrecord_type = "proper-components"\ndocument = "{document}"\n'
        'entrypoint = "main.tex"\nsynthesis_entrypoint = "synthesis.tex"\n'
        'appointed_text_completeness = "complete"\n' + extra +
        'element_keys = ["introit", "gospel"]\n'
        f'[outputs]\nresearch = "{document}"\nsynthesis = "{document}-synthesis"\n'
        f'web = "{document}"\ncanonical_label = "Full PDF"\n'
        'synthesis_label = "Synthesis PDF"\n\n' + "\n".join(blocks) +
        '\n[[relations]]\nkey = "opening-to-gospel"\n'
        'element_keys = ["introit", "gospel"]\n'
        'evidence = ["source-grounded-synthesis"]\n'
    )
    path = leaf / "proper-components.toml"
    path.write_text(manifest, encoding="utf-8")
    return path


def write_aux(path: Path, start: int, end: int, following: int) -> Path:
    path.write_text(
        f"\\newlabel{{triptych:brief-synthesis:start}}{{{{}}{{{start}}}}}\n"
        f"\\newlabel{{triptych:brief-synthesis:end}}{{{{}}{{{end}}}}}\n"
        f"\\newlabel{{triptych:brief-synthesis:next}}{{{{}}{{{following}}}}}\n",
        encoding="utf-8",
    )
    return path


NOTABLE = "The Propers: Notable and Quotable"
EXPLORATORY = "The Propers: Interpretive Possibilities"
TAILS = {"NI": (NOTABLE, EXPLORATORY), "IN": (EXPLORATORY, NOTABLE)}

# Stands in for poppler: the fixture "PDF" is already its own text.
FAKE_PDFTOTEXT = """#!/bin/sh
for argument do
    case "$argument" in
        *.pdf) exec cat "$argument" ;;
    esac
done
exit 1
"""


def write_pdf_text(path: Path, tail: str = "NI") -> Path:
    """Write the text a built edition's PDF yields, with its tail in that order."""
    first, second = TAILS[tail]
    path.write_text(
        "\fThe Propers: Themes and Movement\nBody.\n"
        f"\f{first}\nBody.\n{second}\nBody.\n\fReferences\n",
        encoding="utf-8",
    )
    return path


class ProperComponentTests(unittest.TestCase):
    def component_tree(self, directory: str, **options):
        provider = Path(directory) / "src" / "gpt"
        return write_component_tree(provider, **options), provider

    def test_manifest_enforces_agreed_mode_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            path, provider = self.component_tree(directory)
            module.audit_manifest(path, provider)

    def test_synthesis_must_omit_appointed_text(self):
        with tempfile.TemporaryDirectory() as directory:
            path, provider = self.component_tree(
                directory, appointed_modes='["research", "synthesis"]'
            )
            with self.assertRaisesRegex(ValueError, "appointed-text"):
                module.audit_manifest(path, provider)

    def test_synthesis_must_omit_proper_by_proper_treatment(self):
        with tempfile.TemporaryDirectory() as directory:
            path, provider = self.component_tree(
                directory, treatment_modes='["research", "synthesis"]'
            )
            with self.assertRaisesRegex(ValueError, "proper-treatment"):
                module.audit_manifest(path, provider)

    def test_integrated_commentary_is_synthesis_only(self):
        with tempfile.TemporaryDirectory() as directory:
            path, provider = self.component_tree(
                directory, integrated_modes='["research", "synthesis"]'
            )
            with self.assertRaisesRegex(ValueError, "integrated-commentary"):
                module.audit_manifest(path, provider)

    def test_profile_order_puts_notable_before_exploratory(self):
        with tempfile.TemporaryDirectory() as directory:
            path, provider = self.component_tree(directory)
            module.audit_manifest(path, provider)

    def test_legacy_order_remains_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            path, provider = self.component_tree(directory, swap_tail=True)
            module.audit_manifest(path, provider)

    def test_tail_components_must_follow_grounded_synthesis(self):
        for legacy in (False, True):
            with self.subTest(legacy=legacy), tempfile.TemporaryDirectory() as directory:
                path, provider = self.component_tree(directory, swap_tail=legacy)
                text = path.read_text(encoding="utf-8")
                blocks = text.split("[[components]]")
                blocks[5], blocks[6] = blocks[6], blocks[5]
                path.write_text("[[components]]".join(blocks), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "component order"):
                    module.audit_manifest(path, provider)

    def test_rights_limited_text_requires_research_label(self):
        with tempfile.TemporaryDirectory() as directory:
            path, provider = self.component_tree(directory)
            text = path.read_text(encoding="utf-8")
            text = text.replace(
                'appointed_text_completeness = "complete"',
                'appointed_text_completeness = "rights-limited"',
            )
            path.write_text(text, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Research PDF"):
                module.audit_manifest(path, provider)

    def test_exact_two_page_markers(self):
        with tempfile.TemporaryDirectory() as directory:
            aux = Path(directory) / "guide.aux"
            aux.write_text(
                "\\newlabel{triptych:brief-synthesis:start}{{}{3}}\n"
                "\\newlabel{triptych:brief-synthesis:end}{{}{4}}\n"
                "\\newlabel{triptych:brief-synthesis:next}{{}{5}}\n",
                encoding="utf-8",
            )
            module.validate_brief_pages(aux)

    def test_rejects_displaced_brief_synthesis(self):
        # Adjacent at 4, 5, 6 is exactly what a page-1 overflow produces:
        # every anchor is where the profile puts it relative to the others
        # and none is where the profile puts it.
        with tempfile.TemporaryDirectory() as directory:
            aux = Path(directory) / "guide.aux"
            aux.write_text(
                "\\newlabel{triptych:brief-synthesis:start}{{}{4}}\n"
                "\\newlabel{triptych:brief-synthesis:end}{{}{5}}\n"
                "\\newlabel{triptych:brief-synthesis:next}{{}{6}}\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "begin on page 3"):
                module.validate_brief_pages(aux)

    def test_rejects_spilled_brief_synthesis(self):
        with tempfile.TemporaryDirectory() as directory:
            aux = Path(directory) / "guide.aux"
            aux.write_text(
                "\\newlabel{triptych:brief-synthesis:start}{{}{3}}\n"
                "\\newlabel{triptych:brief-synthesis:end}{{}{5}}\n"
                "\\newlabel{triptych:brief-synthesis:next}{{}{6}}\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "exactly two"):
                module.validate_brief_pages(aux)



class PrintedTailOrderTests(unittest.TestCase):
    """Both profiles print Notable and Quotable before Interpretive Possibilities."""

    def test_reader_order_passes(self):
        module.validate_tail_order(f"{NOTABLE}\nBody.\n{EXPLORATORY}\n")

    def test_reversed_tail_is_refused(self):
        with self.assertRaisesRegex(ValueError, "Notable and Quotable first"):
            module.validate_tail_order(f"{EXPLORATORY}\nBody.\n{NOTABLE}\n")

    def test_heading_after_a_page_break_is_found(self):
        # pdftotext opens each page with a form feed.
        with self.assertRaisesRegex(ValueError, "Notable and Quotable first"):
            module.validate_tail_order(
                "\fInterpretive Possibilities Across the Propers\nBody.\n"
                f"\f{NOTABLE}\n"
            )

    def test_a_mention_in_prose_is_not_a_heading(self):
        module.validate_tail_order(
            "See The Propers: Interpretive Possibilities below.\n"
            f"{NOTABLE}\n{EXPLORATORY}\n"
        )

    def test_missing_heading_is_refused(self):
        with self.assertRaisesRegex(ValueError, "no Notable and Quotable heading"):
            module.validate_tail_order(f"{EXPLORATORY}\n")

CURRENT_1962 = "liturgy/roman-rite/1962/propers/temporal/proper"
LEGACY_1962 = "liturgy/roman-rite/1962/propers/temporal/legacy"
POSTCONCILIAR = ("liturgy/roman-rite/postconciliar/"
                 "roman-missal-third-edition-en-us-2011/propers/temporal/proper")


class ResearchEditionPageTests(unittest.TestCase):
    """The expansive study keeps the concise study's fixed pages 1-5.

    Both 1962 and postconciliar profiles put the brief synthesis on pages 3-4
    of the research edition as well as its companion, so the same markers and
    the same start page apply. Only a legacy research edition, named by its
    own manifest, keeps an older order; even it keeps the two-page extent.
    """

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.provider = self.root / "src" / "gpt"
        stub = self.root / "bin" / "pdftotext"
        stub.parent.mkdir()
        stub.write_text(FAKE_PDFTOTEXT, encoding="utf-8")
        stub.chmod(0o755)
        self.environment = dict(os.environ,
                                PATH=f"{stub.parent}:{os.environ['PATH']}")

    def check(self, document: str, pages: tuple[int, int, int],
              edition: str = "research", tail: str | None = "NI",
              ) -> subprocess.CompletedProcess[str]:
        aux = write_aux(self.root / "guide.aux", *pages)
        if tail is not None:
            write_pdf_text(aux.with_suffix(".pdf"), tail)
        return subprocess.run(
            [sys.executable, str(PATH), "--root", str(self.root), "--provider", "gpt",
             "--document", document, "--edition", edition, "--aux", str(aux)],
            capture_output=True, text=True, check=False, env=self.environment,
        )

    def test_displaced_research_edition_is_refused(self):
        write_component_tree(self.provider, document=CURRENT_1962)
        result = self.check(CURRENT_1962, (4, 5, 6))
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("begin on page 3", result.stderr)

    def test_research_edition_on_its_fixed_pages_passes(self):
        write_component_tree(self.provider, document=CURRENT_1962)
        result = self.check(CURRENT_1962, (3, 4, 5))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("legacy", result.stdout)

    def test_legacy_1962_manifest_exempts_its_research_start_page(self):
        # A 1962 schema-1 manifest without integrated-commentary is the
        # profile's legacy manifest; 49-ninth-after-pentecost is one.
        write_component_tree(self.provider, document=LEGACY_1962,
                             integrated=False, swap_tail=True)
        result = self.check(LEGACY_1962, (17, 18, 19))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("legacy reader order", result.stdout)

    def test_legacy_exemption_keeps_the_two_page_extent(self):
        write_component_tree(self.provider, document=LEGACY_1962, integrated=False)
        result = self.check(LEGACY_1962, (17, 19, 20))
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("exactly two", result.stderr)

    def test_legacy_exemption_does_not_reach_the_synthesis_companion(self):
        write_component_tree(self.provider, document=LEGACY_1962, integrated=False)
        result = self.check(LEGACY_1962, (17, 18, 19), edition="synthesis")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("begin on page 3", result.stderr)

    def test_undeclared_postconciliar_manifest_is_held_to_page_3(self):
        # Postconciliar schema-1 manifests have no integrated commentary, so
        # that absence marks nothing and cannot exempt one.
        write_component_tree(self.provider, document=POSTCONCILIAR, integrated=False)
        result = self.check(POSTCONCILIAR, (7, 8, 9))
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("begin on page 3", result.stderr)

    def test_declared_legacy_order_exempts_its_research_start_page(self):
        write_component_tree(self.provider, document=POSTCONCILIAR, integrated=False,
                             extra='reader_order = "legacy"\n')
        result = self.check(POSTCONCILIAR, (7, 8, 9))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("declared reader_order", result.stdout)

    def test_research_edition_printing_interpretive_first_is_refused(self):
        write_component_tree(self.provider, document=CURRENT_1962)
        result = self.check(CURRENT_1962, (3, 4, 5), tail="IN")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("Notable and Quotable first", result.stderr)

    def test_synthesis_companion_printing_interpretive_first_is_refused(self):
        write_component_tree(self.provider, document=CURRENT_1962)
        result = self.check(CURRENT_1962, (3, 4, 5), edition="synthesis", tail="IN")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("Notable and Quotable first", result.stderr)

    def test_edition_without_the_gallery_heading_is_refused(self):
        write_component_tree(self.provider, document=CURRENT_1962)
        pdf = self.root / "guide.pdf"
        pdf.write_text(f"{EXPLORATORY}\n", encoding="utf-8")
        result = self.check(CURRENT_1962, (3, 4, 5), tail=None)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("no Notable and Quotable heading", result.stderr)

    def test_undeclared_postconciliar_manifest_is_held_to_the_printed_tail(self):
        # gpt pc-s44 years B and C: postconciliar schema 1, nothing declared.
        write_component_tree(self.provider, document=POSTCONCILIAR, integrated=False,
                             swap_tail=True)
        for edition in ("research", "synthesis"):
            with self.subTest(edition=edition):
                result = self.check(POSTCONCILIAR, (3, 4, 5), edition=edition, tail="IN")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("Notable and Quotable first", result.stderr)

    def test_legacy_manifest_keeps_its_tail_in_both_editions(self):
        # Both 49s print Interpretive Possibilities first in both editions.
        write_component_tree(self.provider, document=LEGACY_1962,
                             integrated=False, swap_tail=True)
        for edition in ("research", "synthesis"):
            with self.subTest(edition=edition):
                result = self.check(LEGACY_1962, (3, 4, 5), edition=edition, tail="IN")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("not held ahead of Interpretive", result.stdout)

    def test_declared_legacy_order_exempts_its_tail(self):
        write_component_tree(self.provider, document=POSTCONCILIAR, integrated=False,
                             extra='reader_order = "legacy"\n')
        result = self.check(POSTCONCILIAR, (3, 4, 5), edition="synthesis", tail="IN")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("declared reader_order", result.stdout)

    def test_named_document_without_its_pdf_is_refused(self):
        # A build names its document, so a missing PDF is an error, not a skip.
        write_component_tree(self.provider, document=CURRENT_1962)
        result = self.check(CURRENT_1962, (3, 4, 5), tail=None)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("no built PDF beside", result.stderr)

    def test_aux_without_document_says_the_order_is_unchecked(self):
        # With no manifest there is no legacy status to apply, so only the
        # pages are checked, and the tool says so.
        aux = write_aux(self.root / "guide.aux", 3, 4, 5)
        result = subprocess.run(
            [sys.executable, str(PATH), "--root", str(self.root), "--provider", "gpt",
             "--aux", str(aux)],
            capture_output=True, text=True, check=False, env=self.environment,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("printed order", result.stderr)
        self.assertIn("is not checked", result.stderr)

    def test_revised_manifest_cannot_declare_a_legacy_order(self):
        path = write_component_tree(self.provider, document=CURRENT_1962,
                                    extra='reader_order = "legacy"\n')
        with self.assertRaisesRegex(ValueError, "integrated-commentary"):
            module.audit_manifest(path, self.provider)

    def test_reader_order_has_one_value(self):
        path = write_component_tree(self.provider, document=POSTCONCILIAR,
                                    integrated=False, extra='reader_order = "modern"\n')
        with self.assertRaisesRegex(ValueError, "reader_order"):
            module.audit_manifest(path, self.provider)


FAKE_PDFLATEX = r"""#!/bin/sh
output_directory=
job_name=
for argument do
    case "$argument" in
        -output-directory=*) output_directory=${argument#*=} ;;
        -jobname=*) job_name=${argument#*=} ;;
    esac
done
mkdir -p "$output_directory"
printf '%%PDF-1.5 fixture %s\n' "$job_name" > "$output_directory/$job_name.pdf"
case "${MAKE_TEST_TAIL:-NI}" in
    NI) printf 'The Propers: Notable and Quotable\nThe Propers: Interpretive Possibilities\n' ;;
    IN) printf 'The Propers: Interpretive Possibilities\nThe Propers: Notable and Quotable\n' ;;
esac >> "$output_directory/$job_name.pdf"
set -- $MAKE_TEST_BRIEF_PAGES
{
    printf '\\newlabel{triptych:brief-synthesis:start}{{}{%s}}\n' "$1"
    printf '\\newlabel{triptych:brief-synthesis:end}{{}{%s}}\n' "$2"
    printf '\\newlabel{triptych:brief-synthesis:next}{{}{%s}}\n' "$3"
} > "$output_directory/$job_name.aux"
"""


class ResearchBuildTests(unittest.TestCase):
    """The real Makefile research rule, with TeX and metadata stubbed out."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copy2(ROOT / "Makefile", self.root / "Makefile")
        (self.root / "tools").mkdir()
        (self.root / "scripts").mkdir()
        # Copies, not links: the checker finds its repository from its own path.
        shutil.copy2(PATH, self.root / "tools/check-proper-components")
        for name in ("_proper_components.py", "_tooling.py"):
            shutil.copy2(ROOT / "scripts" / name, self.root / "scripts" / name)
        self.executable("tools/tpt", "#!/usr/bin/env python3\n"
                        "import os, sys\n"
                        "root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n"
                        "target = os.path.join(root, 'tools', sys.argv[1])\n"
                        "if not os.path.exists(target):\n"
                        "    raise SystemExit(127)\n"
                        "os.execv(target, [target] + sys.argv[2:])\n")
        self.executable("tools/check-generation-metadata", "#!/bin/sh\nexit 0\n")
        self.executable("bin/pdfinfo", "#!/bin/sh\nexit 0\n")
        self.executable("bin/pdftotext", FAKE_PDFTOTEXT)
        pdflatex = self.executable("bin/fake-pdflatex", FAKE_PDFLATEX)
        self.provider = self.root / "src" / "gpt"
        self.environment = dict(os.environ, PDFLATEX=str(pdflatex),
                                PATH=f"{self.root / 'bin'}:{os.environ['PATH']}")

    def executable(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        path.chmod(0o755)
        return path

    def build(self, document: str, pages: tuple[int, int, int],
              tail: str = "NI") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["make", "--no-print-directory", f"build/gpt/{document}.pdf"],
            cwd=self.root, env=dict(self.environment,
                                    MAKE_TEST_BRIEF_PAGES=" ".join(map(str, pages)),
                                    MAKE_TEST_TAIL=tail),
            capture_output=True, text=True, check=False,
        )

    def test_displaced_research_edition_fails_its_build(self):
        write_component_tree(self.provider, document=CURRENT_1962)
        result = self.build(CURRENT_1962, (4, 5, 6))
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("begin on page 3", result.stderr)
        self.assertFalse((self.root / f"build/gpt/{CURRENT_1962}.pdf").exists())

    def test_research_edition_on_its_fixed_pages_builds(self):
        write_component_tree(self.provider, document=CURRENT_1962)
        result = self.build(CURRENT_1962, (3, 4, 5))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Proper component manifests valid: 1.", result.stdout)
        self.assertTrue((self.root / f"build/gpt/.metadata/{CURRENT_1962}.ok").is_file())

    def test_research_edition_printing_interpretive_first_fails_its_build(self):
        write_component_tree(self.provider, document=CURRENT_1962)
        result = self.build(CURRENT_1962, (3, 4, 5), tail="IN")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("Notable and Quotable first", result.stderr)
        self.assertFalse((self.root / f"build/gpt/{CURRENT_1962}.pdf").exists())

    def test_legacy_research_edition_builds_by_exemption(self):
        write_component_tree(self.provider, document=LEGACY_1962, integrated=False)
        result = self.build(LEGACY_1962, (17, 18, 19))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("legacy reader order", result.stdout)

    def test_document_without_manifest_is_never_checked(self):
        article = self.provider / "articles/faith/essay"
        article.mkdir(parents=True)
        (article / "main.tex").write_text("% article\n", encoding="utf-8")
        result = self.build("articles/faith/essay", (4, 5, 6))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("Proper component", result.stdout + result.stderr)
        self.assertTrue((self.root / "build/gpt/articles/faith/essay.pdf").is_file())


if __name__ == "__main__":
    unittest.main()
