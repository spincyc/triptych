"""Three-document preflight scopes preserve evidence checks and legacy gates."""

import importlib.machinery
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools/check-content-preflight"
LOADER = importlib.machinery.SourceFileLoader("study_preflight", str(TOOL))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
PREFLIGHT = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(PREFLIGHT)
DOCUMENT = "liturgy/roman-rite/1962/propers/temporal/54-fourteenth-after-pentecost"


class StudyPreflightTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/preflight"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.leaf = self.root / "src/gpt" / DOCUMENT
        self.leaf.mkdir(parents=True)
        (self.leaf / "sections").mkdir()
        (self.leaf / "research").mkdir()
        (self.leaf / "proper-components.toml").write_text("schema = 2\n")
        self.run = dict(workflow_id="proper-study", workflow_version="1",
                        workflow_digest="a" * 64, run_id="0123456789abcdef",
                        seed_commit="b" * 40)
        self.write_provenance()
        for edition, entry in (("research", "main.tex"),
                               ("synthesis", "synthesis.tex"),
                               ("homily", "homily.tex")):
            (self.leaf / entry).write_text(
                f"\\input{{{DOCUMENT}/sections/{edition}}}\n")
            self.write(edition, "\\section*{Mercy}\nAugustine teaches mercy.\n")
        PREFLIGHT.flag_defined.cache_clear()

    def write(self, edition, text):
        (self.leaf / f"sections/{edition}.tex").write_text(text)

    def write_provenance(self, workflow="proper-study", version="1"):
        (self.leaf / "generation-metadata.tex").write_text(
            f"\\AIGenerationProvenance{{{workflow}}}{{{version}}}"
            f"{{{self.run['workflow_digest']}}}{{{self.run['run_id']}}}"
            f"{{{self.run['seed_commit']}}}{{unknown}}\n")

    def check(self, name, edition="research"):
        return PREFLIGHT.CHECKS[name](self.leaf, self.root, edition)

    def corpus(self):
        (self.root / "src/sources").symlink_to(ROOT / "src/sources")
        found = PREFLIGHT._corpus_answer(self.leaf, self.root)
        (self.leaf / "research/chronology.toml").write_text(
            PREFLIGHT._wiring().render(found))
        return found

    def test_homily_is_in_whole_leaf_voice_check_and_its_own_scope(self):
        self.write("homily", "\\section*{Mercy}\nAugustine teaches mercy. "
                   "This guide has composed nothing.\n")
        for edition in ("homily", "leaf"):
            problems, _ = self.check("house-voice", edition)
            self.assertTrue(problems)
            self.assertIn("sections/homily.tex", " ".join(problems))
        for edition in ("research", "canonical", "synthesis"):
            self.assertEqual(self.check("house-voice", edition)[0], [])

    def test_early_research_scope_does_not_need_future_companions(self):
        (self.leaf / "synthesis.tex").unlink()
        (self.leaf / "homily.tex").unlink()
        self.assertEqual(self.check("house-voice")[0], [])
        self.assertEqual(self.check("house-voice", "leaf")[0], [])
        result = subprocess.run(
            [sys.executable, str(TOOL), "--root", str(self.root),
             "--document", DOCUMENT, "--edition", "homily", "--check", "house-voice"],
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("homily", result.stderr)

    def test_homily_cannot_borrow_research_citation_to_support_unused_reference(self):
        self.write("homily", "\\section*{Mercy}\nMercy restores the sinner.\n"
                   "\\section*{References}\n\\begin{itemize}\n"
                   "\\item Augustine, Enarrationes.\n\\end{itemize}\n")
        self.assertTrue(self.check("references-used", "homily")[0])
        self.write("homily", (self.leaf / "sections/homily.tex").read_text().replace(
            "Mercy restores", "Augustine teaches that mercy restores"))
        self.assertEqual(self.check("references-used", "homily")[0], [])

    def test_unknown_homily_source_identifier_is_rejected(self):
        self.write("homily", r"\texttt{work.invented.authority}" + "\n")
        self.assertTrue(self.check("identifiers-resolve", "homily")[0])
        self.assertEqual(self.check("identifiers-resolve", "research")[0], [])

    def test_homily_cannot_quote_a_witness_declared_unquoted(self):
        self.write("homily", "\\begin{namedtranslation}{Guéranger, The Liturgical Year}\n"
                   "A borrowed saying.\n\\end{namedtranslation}\n"
                   "\\section*{References}\n\\begin{itemize}\n"
                   "\\item Prosper Guéranger, \\work{The Liturgical Year}. "
                   "Summarised only.\n\\end{itemize}\n")
        self.assertTrue(self.check("unquoted-not-quoted", "homily")[0])

    def test_restricted_translation_control_stays_rejected(self):
        library = self.root / "src/sources/works/probe"
        library.mkdir(parents=True)
        source = "artifact.invented.protected-edition.text"
        (library / "artifact.toml").write_text(
            f'id = "{source}"\nrecord_type = "artifact"\n'
            'storage = "restricted"\nrights_status = "restricted"\n')
        (self.leaf / "research/source-bindings.toml").write_text(
            f'[[bindings]]\nsource_id = "{source}"\nrole = "translation-control"\n')
        self.assertTrue(self.check("restricted-not-reproduced", "homily")[0])

    def test_missing_binding_record_stays_rejected(self):
        self.assertTrue(self.check("bindings-valid", "homily")[0])

    def test_unregistered_binding_is_rejected_by_source_library(self):
        (self.root / "src/sources/works").mkdir(parents=True)
        (self.leaf / "research/source-bindings.toml").write_text(
            'schema = 1\nrecord_type = "bindings"\n'
            f'document = "{DOCUMENT}"\n[[bindings]]\n'
            'source_id = "work.invented.authority"\nrole = "context"\n'
            'loci = ["chapter 1"]\nstates = ["cataloged"]\n')
        problems, _ = self.check("bindings-valid", "homily")
        self.assertTrue(problems)
        self.assertIn("work.invented.authority", " ".join(problems))

    def test_bogus_run_provenance_stays_rejected_in_every_edition(self):
        for edition in ("research", "synthesis", "homily"):
            self.assertEqual(PREFLIGHT.check_provenance_matches_run(
                self.leaf, self.root, self.run, edition)[0], [])
        self.write_provenance(workflow="proper", version="29")
        for edition in ("research", "synthesis", "homily"):
            self.assertTrue(PREFLIGHT.check_provenance_matches_run(
                self.leaf, self.root, self.run, edition)[0])

    def test_structural_house_rule_applies_without_legacy_version_number(self):
        self.write("homily", "\\section*{Governing thesis}\nMercy restores.\n")
        self.assertTrue(self.check("structural-meta-labels", "homily")[0])
        self.assertEqual(self.check("structural-meta-labels", "research")[0], [])

    def test_no_date_table_record_or_annotation_is_required_when_no_date_prints(self):
        for edition in ("research", "synthesis", "homily"):
            for check in ("chronology-record-current", "chronology-annotations-current",
                          "chronology-claims-supported"):
                with self.subTest(edition=edition, check=check):
                    self.assertEqual(self.check(check, edition)[0], [])

    def test_one_corpus_claim_needs_no_other_elements_date_cells(self):
        self.corpus()
        self.write("homily", r"\chronology{composition.gospel-of-matthew}"
                   r"{composition}{about the year 50}" + "\n")
        self.assertEqual(self.check("chronology-claims-supported", "homily")[0], [])
        self.assertEqual(self.check("chronology-record-current", "homily")[0], [])
        (self.leaf / "research/chronology.toml").unlink()
        self.assertTrue(self.check("chronology-record-current", "homily")[0])

    def test_invented_corpus_date_in_homily_is_rejected(self):
        self.corpus()
        self.write("homily", r"\chronology{composition.gospel-of-matthew}"
                   r"{composition}{about the year 51}" + "\n")
        self.assertTrue(self.check("chronology-claims-supported", "homily")[0])
        self.assertEqual(self.check("chronology-claims-supported", "research")[0], [])

    def test_carried_chronology_record_cannot_be_forged(self):
        self.corpus()
        path = self.leaf / "research/chronology.toml"
        path.write_text(path.read_text() + "\n# a hand alteration\n")
        self.assertTrue(self.check("chronology-record-current")[0])

    def test_optional_generated_annotations_stay_current_without_forcing_table(self):
        found = self.corpus()
        wiring = PREFLIGHT._wiring()
        path = self.leaf / "research/chronology-annotations.tex"
        path.write_text(wiring.render_annotations_tex(wiring.annotations(found)))
        self.assertEqual(self.check("chronology-annotations-current")[0], [])
        self.assertEqual(self.check("chronology-claims-supported")[0], [])
        path.write_text(path.read_text() + "\n% forged projection\n")
        self.assertTrue(self.check("chronology-annotations-current")[0])

    def test_same_supported_date_can_recur_in_separate_publications(self):
        self.corpus()
        text = (r"\chronodate{gospel}{\chronology{composition.gospel-of-matthew}"
                r"{composition}{about the year 50}}" + "\n")
        self.write("research", text)
        self.write("homily", text)
        self.assertEqual(self.check("chronology-claims-supported", "leaf")[0], [])

    def test_legacy_proper_29_still_requires_record_annotations_and_date_cells(self):
        self.corpus()
        (self.leaf / "proper-components.toml").write_text("schema = 1\n")
        self.write_provenance(workflow="proper", version="29")
        self.assertTrue(self.check("chronology-claims-supported")[0])
        self.assertTrue(self.check("chronology-annotations-current")[0])
        (self.leaf / "research/chronology.toml").unlink()
        self.assertTrue(self.check("chronology-record-current")[0])

    def test_schema_two_does_not_apply_old_exploratory_field_template(self):
        self.write("research", "\\section*{The Propers: Interpretive Possibilities}\n"
                   "\\begin{proposal}{Mercy}\nMercy restores.\n\\end{proposal}\n")
        self.assertEqual(self.check("proposal-fields")[0], [])
        (self.leaf / "proper-components.toml").write_text("schema = 1\n")
        self.assertTrue(self.check("proposal-fields")[0])

    def test_lane_coverage_uses_new_contract_before_companions_exist(self):
        (self.leaf / "synthesis.tex").unlink()
        (self.leaf / "homily.tex").unlink()
        manifest = (
            'schema = 2\nrecord_type = "proper-components"\n'
            'calendar = "roman-1962"\n'
            f'document = "{DOCUMENT}"\nentrypoint = "main.tex"\n'
            'synthesis_entrypoint = "synthesis.tex"\nhomily_entrypoint = "homily.tex"\n'
            'appointed_text_completeness = "complete"\nelement_keys = ["introit", "gospel"]\n'
            f'[outputs]\nresearch = "{DOCUMENT}"\nsynthesis = "{DOCUMENT}-synthesis"\n'
            f'homily = "{DOCUMENT}-homily"\nweb = "{DOCUMENT}"\n'
            'canonical_label = "Full PDF"\nsynthesis_label = "Synthesis PDF"\n'
            'homily_label = "Homily PDF"\n')
        components = [("texts", "appointed-text", ["research"]),
                      ("commentary", "proper-treatment", ["research"]),
                      ("mercy", "interpretive-lane", ["research"]),
                      ("hope", "interpretive-lane", ["research"]),
                      ("concise", "integrated-commentary", ["synthesis"]),
                      ("spoken", "homily", ["homily"]),
                      ("apparatus", "terminal-apparatus", ["research", "synthesis", "homily"])]
        for key, kind, modes in components:
            manifest += (
                f'[[components]]\nkey = "{key}"\nkind = "{kind}"\n'
                f'path = "sections/{key}.tex"\nmodes = {modes!r}\n'
                'element_keys = ["introit", "gospel"]\ndepends_on = []\nreferences = []\n')
        for key in ("mercy", "hope"):
            manifest += (
                f'[[lanes]]\nkey = "{key}"\nauthors = ["Augustine", "Ambrose"]\n'
                'sources = ["research/scope.md"]\n'
                'senses = ["literal", "allegorical", "moral", "anagogical"]\n'
                f'element_keys = ["introit", "gospel"]\ncomponent_keys = ["{key}"]\n')
        path = self.leaf / "proper-components.toml"
        path.write_text(manifest)
        self.assertEqual(self.check("relation-coverage")[0], [])
        # Merely listing a Gospel in the lane cannot supply missing component coverage.
        path.write_text(manifest.replace(
            'path = "sections/hope.tex"\nmodes = [\'research\']\n'
            'element_keys = ["introit", "gospel"]',
            'path = "sections/hope.tex"\nmodes = [\'research\']\n'
            'element_keys = ["introit"]'))
        with self.assertRaisesRegex(ValueError, "coverage"):
            self.check("relation-coverage")


if __name__ == "__main__":
    unittest.main()
