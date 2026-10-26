"""Stable replacement identities retain their edition and calendar-family bounds."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _proper_chronology_inputs as inputs
import _proper_study as study

EDITION = "roman-missal-third-edition-en-us-2011"
PREFIX = f"liturgy/roman-rite/postconciliar/{EDITION}/propers"
DOCUMENT = f"{PREFIX}/general-calendar/pc-r07-all-saints-abc"


class ReplacementIdentityTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/pc-r-workflow-support/identity-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        path = self.root / inputs.REGISTRY
        path.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / inputs.REGISTRY, path)
        self.proper_root = self.root / "src/gpt" / PREFIX
        self.registry = self.proper_root / "registry"
        self.registry.mkdir(parents=True)
        self.owner = self.proper_root / "general-calendar/shared/formularies/pc-r07-all-saints/propers/verified.md"
        self.owner.parent.mkdir(parents=True)
        self.owner.write_text("Same-edition replacement formulary audit.\n")
        self.plan = self.root / "guidance/liturgy/propers-production-plan.md"
        self.plan.write_text(f"- Authorized 2026-10-25: provider `gpt`, identity `{DOCUMENT}`.\n")
        self.dispositions = self.registry / "formula-dispositions.md"
        self.row = ("| `PC-R07` | `PC-R07-ABC` | `pc-r07-all-saints-abc` | 667 | "
                    "[Owner](../general-calendar/shared/formularies/pc-r07-all-saints/propers/verified.md) | "
                    "Adopted for the authorized study; edition limits remain in the owner. |\n")
        self.header = ("| Parent | Formula key | Full publication slug | Lectionary | Canonical owner | Disposition |\n"
                       "| --- | --- | --- | --- | --- | --- |\n")
        self.dispositions.write_text(self.header + self.row)

    def test_replacement_registry_controls_formula_slug_family_and_owner(self):
        cases = (
            ("pc-r07-all-saints-abc", "PC-R07-ABC", "pc-r07-all-saints"),
            ("pc-r01-presentation-of-the-lord-abc-sunday", "PC-R01-ABC-O-SUNDAY",
             "pc-r01-presentation-of-the-lord"),
            ("pc-r04-transfiguration-of-the-lord-year-b-sunday", "PC-R04-B-O-SUNDAY",
             "pc-r04-transfiguration-of-the-lord"),
            ("pc-r05-assumption-of-the-blessed-virgin-mary-abc-vigil", "PC-R05-ABC-VIGIL",
             "pc-r05-assumption-of-the-blessed-virgin-mary"),
        )
        for slug, formula, stem in cases:
            document = f"{PREFIX}/general-calendar/{slug}"
            with self.subTest(formula=formula):
                target = inputs.registered_target(document, self.root)
                self.assertEqual(target.formula, formula)
                self.assertEqual(target.owner, f"general-calendar/shared/formularies/{stem}/propers/verified.md")
                self.assertEqual(study.identity(self.root, document), "library/novus-ordo-liturgy.md")

    def test_wrong_family_unregistered_forms_and_noncanonical_paths_refuse(self):
        for invalid in (
            DOCUMENT.replace("general-calendar", "temporal"),
            DOCUMENT.replace("general-calendar", "ritual"),
            DOCUMENT.replace("pc-r07", "pc-r99"),
            DOCUMENT.replace("all-saints", "all-souls"),
            DOCUMENT.replace("-abc", "-year-a"),
            DOCUMENT + "-vigil", DOCUMENT + "-sunday", "/" + DOCUMENT,
            DOCUMENT.replace("/propers/", "/propers/../propers/"),
            f"{PREFIX}/general-calendar/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a",
            f"{PREFIX}/temporal/pc-t01-evening-mass-of-the-lords-supper-abc",
            f"{PREFIX}/general-calendar/pc-w01-invented-abc",
        ):
            with self.subTest(document=invalid), self.assertRaises(ValueError):
                study.identity(self.root, invalid)

    def test_scope_bootstraps_authorized_identity_before_context_creates_owner(self):
        self.dispositions.unlink()
        self.owner.unlink()
        self.assertEqual(study.scope(self.root, "gpt", DOCUMENT), "library/novus-ordo-liturgy.md")
        for provider, document in (("claude", DOCUMENT),
                                   ("gpt", DOCUMENT.replace(EDITION, "another-edition"))):
            with self.subTest(provider=provider, document=document), self.assertRaises(ValueError):
                study.scope(self.root, provider, document)

    def disposition(self, document=DOCUMENT):
        target = inputs.registered_target(document, self.root)
        inputs.replacement_disposition(self.root, self.proper_root, target)

    def test_chronology_adoption_requires_exact_edition_row_and_owner(self):
        self.disposition()
        for before, after in (
            ("`PC-R07-ABC`", "`PC-R07-A`"),
            ("`pc-r07-all-saints-abc`", "`pc-r07-all-saints-year-a`"),
            ("Adopted for", "Unresolved for"),
            ("../general-calendar/shared/", "../temporal/shared/"),
            ("formularies/pc-r07-all-saints/", "formularies/pc-r06-exaltation-of-the-holy-cross/"),
            ("../general-calendar/", "../../../../other-edition/propers/general-calendar/"),
            ("../general-calendar/", "../general-calendar/./"),
        ):
            with self.subTest(after=after):
                self.dispositions.write_text(self.header + self.row.replace(before, after))
                with self.assertRaises(ValueError):
                    self.disposition()
        self.dispositions.write_text(self.header + self.row)
        self.owner.unlink()
        with self.assertRaisesRegex(ValueError, "missing appointment dependency"):
            self.disposition()

    def test_duplicate_and_incidental_registry_mentions_do_not_adopt_target(self):
        for content in (
            self.header + self.row + self.row,
            self.header + self.row.replace("`PC-R07-ABC`", "`PC-R06-ABC-O-SUNDAY`")
            .replace("`pc-r07-all-saints-abc`", "`pc-r06-exaltation-of-the-holy-cross-abc-sunday`")
            .replace("Adopted for", "Adopted; see `PC-R07-ABC` and `pc-r07-all-saints-abc` for"),
        ):
            self.dispositions.write_text(content)
            with self.assertRaisesRegex(ValueError, "exact adopted edition registry disposition"):
                self.disposition()

    def test_all_souls_stable_alternatives_do_not_select_an_edition_expansion(self):
        document = (f"{PREFIX}/general-calendar/"
                    "pc-r08-commemoration-of-all-the-faithful-departed-abc-formulary-1")
        self.plan.write_text(f"- Authorized 2026-10-25: provider `gpt`, identity `{document}`.\n")
        self.dispositions.write_text("PC-R08: unresolved; neither expansion adopted.\n")
        with self.assertRaisesRegex(ValueError, "exact adopted edition registry disposition"):
            self.disposition(document)


if __name__ == "__main__":
    unittest.main()
