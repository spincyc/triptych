"""Three-document preflight scopes preserve evidence checks and legacy gates."""

import importlib.machinery
import importlib.util
import subprocess
import sys
import tempfile
import tomllib
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

    def write_profile_comparison(self, profile="catholic-critical-v1",
                                 subject="critical.gospel-of-matthew"):
        path = self.leaf / "research/chronology-profile-comparisons.toml"
        path.write_text(
            'schema = 1\n'
            'record_type = "proper-chronology-profile-comparisons"\n'
            f'document = "{DOCUMENT}"\n\n'
            '[[comparisons]]\n'
            'key = "critical-matthew-composition"\n'
            'element = "gospel"\n'
            f'profile = "{profile}"\n'
            'relation = "composition"\n'
            f'subject = "{subject}"\n'
        )
        return path

    def shared_date_wrapper(self):
        (self.leaf / "proper-components.toml").write_text(
            'schema = 2\nformat_contract = "propers-format-v1"\n')
        owner = self.root / "src/common/propers-format.tex"
        owner.parent.mkdir()
        owner.write_text(r"\newcommand{\chronodate}[2]{#2}" + "\n")
        for entry in ("main.tex", "synthesis.tex", "homily.tex"):
            path = self.leaf / entry
            path.write_text("\\input{common/propers-format}\n"
                            "\\begin{document}\n" + path.read_text())
        return owner

    def wrapper_problems(self, edition="leaf"):
        return PREFLIGHT._date_cell_wrapper_integrity(
            self.leaf, self.root, edition)

    def test_shared_date_wrapper_and_legacy_owner(self):
        (self.leaf / "format.tex").write_text(
            r"\newcommand{\chronodate}[2]{#2}" + "\n")
        self.assertEqual(self.wrapper_problems(), [])
        self.shared_date_wrapper()
        self.assertIn("redefines", " ".join(self.wrapper_problems()))
        (self.leaf / "format.tex").write_text("% local content fields only\n")
        self.assertEqual(self.wrapper_problems(), [])

    def test_shared_date_wrapper_cannot_discard_or_replace_annotation(self):
        owner = self.shared_date_wrapper()
        for definition in (r"\newcommand{\chronodate}[2]{}",
                           r"\newcommand{\chronodate}[2]{Forged}",
                           r"\newcommand{\chronodate}[2]{#1}"):
            with self.subTest(definition=definition):
                owner.write_text(definition + "\n")
                self.assertIn("canonical definitions",
                              " ".join(self.wrapper_problems()))

    def test_shared_date_wrapper_rejects_leaf_shadow_and_missing_owner(self):
        owner = self.shared_date_wrapper()
        self.write("research", r"\renewcommand{\chronodate}[2]{Forged}")
        self.assertIn("redefines", " ".join(self.wrapper_problems()))
        self.write("research", "Ordinary prose.")
        owner.unlink()
        self.assertIn("missing date-cell wrapper owner",
                      " ".join(self.wrapper_problems()))

    def test_shared_date_wrapper_requires_each_entrypoint_import(self):
        self.shared_date_wrapper()
        entry = self.leaf / "synthesis.tex"
        original = entry.read_text()
        for text in (
            original.replace(r"\input{common/propers-format}", ""),
            original + "\n\\input{common/propers-format}\n",
            original.replace("\\input{common/propers-format}\n", "") +
            "\n\\input{common/propers-format}\n",
        ):
            with self.subTest(text=text):
                entry.write_text(text)
                self.assertIn("synthesis.tex", " ".join(self.wrapper_problems()))
                self.assertEqual(self.wrapper_problems("research"), [])

    def test_unknown_format_contract_cannot_select_an_unchecked_owner(self):
        (self.leaf / "proper-components.toml").write_text(
            'schema = 2\nformat_contract = "invented"\n')
        with self.assertRaisesRegex(ValueError, "format_contract"):
            self.wrapper_problems()

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

    def test_profile_comparison_is_generated_but_never_merged_into_default(self):
        source = self.write_profile_comparison()
        found = self.corpus()
        gospel = found.element("gospel")
        self.assertNotIn(
            "critical.gospel-of-matthew",
            {claim.subject for claim in gospel.publication_claims},
        )
        self.assertEqual(len(found.profile_comparisons), 1)
        comparison = found.profile_comparisons[0]
        self.assertEqual(comparison.requested_profile, "catholic-critical-v1")
        self.assertEqual(comparison.relation, "composition")
        self.assertEqual(comparison.subject, "critical.gospel-of-matthew")
        self.assertEqual({claim.profile for claim in comparison.claims},
                         {"catholic-critical-v1"})
        self.assertTrue(all(claim.sources for claim in comparison.claims))
        self.assertEqual(found.comparison_dependencies[0][0],
                         source.relative_to(self.root).as_posix())

        wiring = PREFLIGHT._wiring()
        record = tomllib.loads(wiring.render(found))
        self.assertEqual(record["schema"], 3)
        carried = record["profile_comparisons"][0]
        self.assertEqual(carried["requested_profile"], "catholic-critical-v1")
        self.assertEqual(carried["claims"][0]["profile"],
                         "catholic-critical-v1")
        self.assertTrue(carried["claims"][0]["sources"])
        projected = wiring.annotations(found)
        group = next(
            group for element in projected.elements if element.key == "gospel"
            for group in element.groups if group.requested_profile
        )
        self.assertEqual(group.requested_profile, "catholic-critical-v1")
        payload = wiring.annotation_payload(projected)
        self.assertEqual(payload["schema"], 3)
        comparison_group = next(
            group for element in payload["elements"] if element["key"] == "gospel"
            for group in element["groups"] if group["requested_profile"]
        )
        self.assertTrue(comparison_group["claims"][0]["sources"])
        tex = wiring.render_annotations_tex(projected)
        self.assertIn(r"\chronologyannotationcomparisongroup"
                      r"{catholic-critical-v1}{composition}", tex)
        self.assertIn(r"\chronologyannotationcomparisonclaim"
                      r"{critical.gospel-of-matthew}{composition}"
                      r"{catholic-critical-v1}{catholic-critical-v1}", tex)

    def test_profile_comparison_refuses_a_cascade_or_missing_selection(self):
        self.write_profile_comparison(profile="catholic-comprehensive-v1")
        (self.root / "src/sources").symlink_to(ROOT / "src/sources")
        with self.assertRaisesRegex(ValueError, "evidence profile"):
            PREFLIGHT._corpus_answer(self.leaf, self.root)
        self.write_profile_comparison(subject="critical.missing")
        with self.assertRaisesRegex(ValueError, "returns no 'composition'"):
            PREFLIGHT._corpus_answer(self.leaf, self.root)

    def test_manual_era_dates_absent_from_record_are_rejected_in_prose(self):
        self.write_provenance(version="6")
        self.corpus()
        cases = (
            "The introduction gives a post-A.D.~70 date.",
            "The introduction gives A.D.~70.",
            "The introduction gives a ``post-A.D.~70 date''.",
        )
        for text in cases:
            with self.subTest(text=text):
                self.write("research", text + "\n")
                problems, _ = self.check("chronology-claims-supported", "research")
                self.assertTrue(problems)
                self.assertIn("manual chronology date", " ".join(problems))

    def test_manual_era_date_declared_by_comparison_is_supported(self):
        self.write_profile_comparison()
        self.corpus()
        self.write("research", "The introduction gives a ``post-A.D.~70 date''.\n")
        self.assertEqual(
            self.check("chronology-claims-supported", "research")[0], []
        )

    def test_comparison_boundary_does_not_authorize_opposite_or_overprecise_prose(self):
        self.write_profile_comparison()
        self.corpus()
        for printed in (
            "pre-A.D.~70", "before A.D.~70", "A.D.~70", "about A.D.~70"
        ):
            with self.subTest(printed=printed):
                self.write("research", f"The introduction gives {printed}.\n")
                problems, _ = self.check("chronology-claims-supported", "research")
                self.assertIn("manual chronology date", " ".join(problems))
        self.write("research", "The introduction gives after A.D.~70.\n")
        self.assertEqual(
            self.check("chronology-claims-supported", "research")[0], []
        )

    def test_approximate_default_claim_does_not_authorize_exact_prose(self):
        self.write_provenance(version="6")
        self.corpus()
        self.write("research", "The article gives A.D.~38--45.\n")
        problems, _ = self.check("chronology-claims-supported", "research")
        self.assertIn("manual chronology date", " ".join(problems))
        self.write("research", "The article gives about A.D.~38--45.\n")
        self.assertEqual(
            self.check("chronology-claims-supported", "research")[0], []
        )

    def test_manual_dates_without_an_era_are_rejected(self):
        self.write_provenance(version="6")
        self.corpus()
        for printed in (
            "about 140--142", "c.~140", "140--142", "between 140 and 142"
        ):
            with self.subTest(printed=printed):
                self.write("research", f"\\dossierprose{{The proposed date is {printed}.}}\n")
                problems, _ = self.check("chronology-claims-supported", "research")
                self.assertIn("omits its era", " ".join(problems))

    def test_nearby_era_date_does_not_hide_an_era_less_date(self):
        self.write_provenance(version="6")
        self.corpus()
        for prose in (
            "about A.D.~50 is early; about 140--142 is later",
            "about 140--142 is later than about A.D.~50",
        ):
            with self.subTest(prose=prose):
                self.write("research", f"\\dossierprose{{{prose}.}}\n")
                problems, _ = self.check("chronology-claims-supported", "research")
                self.assertIn("'about 140-142' omits its era", " ".join(problems))

    def test_era_adjoining_the_same_span_is_not_reported_as_omitted(self):
        self.write_provenance(version="6")
        self.corpus()
        for printed in ("about A.D.~140--142", "about 140--142 A.D."):
            with self.subTest(printed=printed):
                self.write("research", f"\\dossierprose{{Dated {printed}.}}\n")
                problems, _ = self.check("chronology-claims-supported", "research")
                joined = " ".join(problems)
                self.assertIn("absent from this proper's generated", joined)
                self.assertNotIn("omits its era", joined)

    def test_verse_and_chapter_spans_are_not_manual_dates(self):
        self.write_provenance(version="6")
        self.corpus()
        self.write(
            "research",
            "The dossier cites Matthew 20:17--19 and chapters 40--55.\n",
        )
        self.assertEqual(
            self.check("chronology-claims-supported", "research")[0], []
        )

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
