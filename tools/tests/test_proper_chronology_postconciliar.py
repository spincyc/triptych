"""Edition-owned appointments reach neutral chronology without a 1962 import."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _proper_chronology as chronology
import _proper_chronology_inputs as inputs

DOCUMENT = ("liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/"
            "propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a")
LEGACY = "liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost"


class PostconciliarChronologyTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/postconciliar-chronology/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.leaf = self.root / "src/gpt" / DOCUMENT
        self.owner = self.leaf.parent / "shared/ordinary-time/weeks/25/propers/verified.md"
        self.local_owner = self.leaf / "propers/verified.md"
        self.input = self.leaf / inputs.INPUT
        self.registry = self.leaf.parent.parent / "registry"
        self.write(self.root / inputs.REGISTRY, (ROOT / inputs.REGISTRY).read_text())
        self.write(self.owner, "Same-edition Week 25 appointment audit.\n")
        self.write(self.local_owner, "Same-edition cycle A appointment audit.\n")
        self.write(self.registry / "README.md", "Edition registry.\n")
        self.write(self.registry / "formula-dispositions.md",
                   f"| `PC-S51-A` | `{self.leaf.name}` | Adopted. |\n")
        self.rows = [
            ("entrance", self.owner, [("Psalm 37:39-40", "hebrew", "identified-basis")]),
            ("collect", self.owner, []),
            ("first-reading", self.local_owner, [("Isaiah 55:6-9", "vulgate", "appointed")]),
            ("responsorial-psalm", self.local_owner,
             [("Psalm 145:2-3, 8-9, 17-18", "hebrew", "appointed"),
              ("Psalm 145:18a", "hebrew", "response")]),
            ("second-reading", self.local_owner, [("Philippians 1:20c-24, 27a", "vulgate", "appointed")]),
            ("acclamation", self.local_owner, [("Cf. Acts 16:14b", "vulgate", "adaptation")]),
            ("gospel", self.local_owner, [("Matthew 20:1-16a", "vulgate", "appointed")]),
            ("offerings", self.owner, []),
            ("communion-ps119", self.owner, [("Psalm 119:4-5", "hebrew", "appointed")]),
            ("communion-jn10", self.owner, [("John 10:14", "vulgate", "appointed")]),
            ("after-communion", self.owner, []),
        ]
        self.keys = [row[0] for row in self.rows]
        self.write(self.leaf / "proper-components.toml",
                   f'schema = 2\ndocument = "{DOCUMENT}"\ncalendar = "postconciliar"\n'
                   f'element_keys = {json.dumps(self.keys)}\n')
        self.write(self.leaf / "instance/manifest.md", "\n".join(
            f"| {n} | {key} | required or appointed alternative |"
            for n, key in enumerate(self.keys, 1)))
        self.write(self.input, self.input_text())
        corpus = self.root / "src/sources/chronology"
        corpus.parent.mkdir(parents=True, exist_ok=True)
        corpus.symlink_to(ROOT / "src/sources/chronology", target_is_directory=True)

    def write(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")

    def input_text(self):
        q = json.dumps
        lines = ['schema = 1', 'record_type = "proper-chronology-inputs"',
                 f'document = {q(DOCUMENT)}', 'calendar = "postconciliar"',
                 'formula = "PC-S51-A"',
                 f'shared_owner = {q(self.owner.relative_to(self.root).as_posix())}']
        for key, owner, citations in self.rows:
            lines += ['', '[[elements]]', f'key = {q(key)}', f'name = {q(key)}',
                      f'owner = {q(owner.relative_to(self.root).as_posix())}', 'citations = [']
            for ref, system, kind in citations:
                lines.append('{ ref = ' + q(ref) + ', citation = ' + q(ref.removeprefix('Cf. '))
                             + ', system = ' + q(system) + ', kind = ' + q(kind) + ' },')
            lines.append(']')
            if not citations:
                lines.append('non_scriptural_reason = "Composed oration, no appointed citation."')
        return '\n'.join(lines) + '\n'

    def dossier(self):
        return chronology.dossier(DOCUMENT, root=self.root, provider="gpt")

    def run_cli(self, command, *args):
        return subprocess.run([sys.executable, str(ROOT / "tools/proper-chronology"),
                               command, "--document", DOCUMENT, "--provider", "gpt",
                               "--root", str(self.root), *args], cwd=ROOT,
                              text=True, capture_output=True, check=False)

    def test_exact_owning_keys_citations_numbering_and_query_boundary(self):
        # There is deliberately no calendar fixture: this adapter must never
        # consult either family's generic calendar for edition appointments.
        with patch.object(chronology, "_calendar_document", side_effect=AssertionError("calendar import")):
            found = self.dossier()
        self.assertEqual((found.calendar, found.mass, found.system),
                         ("postconciliar", "PC-S51-A", "vulgate"))
        self.assertEqual([element.key for element in found.elements], self.keys)
        self.assertEqual(found.element("entrance").loci, ("Ps.36.39", "Ps.36.40"))
        self.assertEqual(found.element("communion-ps119").loci, ("Ps.118.4", "Ps.118.5"))
        self.assertEqual(found.element("communion-jn10").loci, ("John.10.14",))
        self.assertEqual(found.element("responsorial-psalm").loci,
                         tuple(f"Ps.144.{n}" for n in (2, 3, 8, 9, 17, 18)))
        self.assertEqual(found.element("acclamation").refs, ("Cf. Acts 16:14b",))
        self.assertEqual(found.element("second-reading").loci,
                         tuple(f"Phil.1.{n}" for n in (20, 21, 22, 23, 24, 27)))
        self.assertEqual(found.element("gospel").refs, ("Matthew 20:1-16a",))
        self.assertTrue(any("whole-verse query envelope" in note for note in found.appointment_notes))
        self.assertTrue(any("identified-basis" in note for note in found.appointment_notes))
        self.assertEqual(sum(bool(element.loci) for element in found.elements), 8)

    def test_corpus_relations_candidates_and_missing_event_survive(self):
        found = self.dossier()
        annotation = chronology.annotations(found)
        for element in annotation.elements:
            claims = [claim for group in element.groups for claim in group.claims]
            expected = found.element(element.key).publication_claims
            fields = lambda claim: (claim.subject, claim.relation, claim.profile,
                                     claim.label, claim.disposition, claim.reaches)
            self.assertCountEqual([fields(claim) for claim in claims],
                                  [fields(claim) for claim in expected])
        gospel = next(element for element in annotation.elements if element.key == "gospel")
        gap = next(group for group in gospel.groups if group.relation == "narrated-event")
        self.assertEqual((gap.status, gap.claims), ("research-pending", ()))
        acclamation = next(element for element in annotation.elements if element.key == "acclamation")
        self.assertEqual({group.relation for group in acclamation.groups},
                         {"narrated-event", "composition"})

    def test_cli_writes_checks_and_detects_each_appointment_dependency_drift(self):
        for command in ("record", "annotations"):
            done = self.run_cli(command, "--write")
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertEqual(self.run_cli(command, "--check").returncode, 0)
        data = tomllib.loads((self.leaf / chronology.RECORD).read_text())
        for dependency in data["appointment_dependencies"]:
            path = self.root / dependency["path"]
            original = path.read_text()
            try:
                path.write_text(original + "\n# changed appointment audit\n")
                for command in ("record", "annotations"):
                    done = self.run_cli(command, "--check")
                    self.assertEqual(done.returncode, 1, (dependency, done.stdout, done.stderr))
            finally:
                path.write_text(original)

    def test_research_without_components_then_authoring_preserves_exact_bytes(self):
        component_path = self.leaf / "proper-components.toml"
        manifest = component_path.read_text()
        component_path.unlink()
        before = self.dossier()
        expected = {
            chronology.RECORD: chronology.render(before).encode(),
            chronology.ANNOTATIONS_RECORD: chronology.render_annotations_tex(
                chronology.annotations(before)).encode(),
        }
        for command in ("record", "annotations"):
            done = self.run_cli(command, "--write")
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertEqual(self.run_cli(command, "--check").returncode, 0)
        for addition in (
            "",
            '\n[[components]]\nkey = "opening"\npath = "sections/opening.tex"\n'
            'modes = ["research", "synthesis"]\n',
            '\n[[components]]\nkey = "opening"\npath = "sections/revised-opening.tex"\n'
            'modes = ["synthesis"]\n\n[presentation]\npages = [1, 2, 3, 4]\n',
        ):
            with self.subTest(addition=addition):
                component_path.write_text(manifest + addition)
                after = self.dossier()
                self.assertEqual(chronology.render(after).encode(), expected[chronology.RECORD])
                self.assertEqual(chronology.render_annotations_tex(chronology.annotations(after)).encode(),
                                 expected[chronology.ANNOTATIONS_RECORD])
                for command in ("record", "annotations"):
                    done = self.run_cli(command, "--check")
                    self.assertEqual(done.returncode, 0, done.stderr)
                for filename, content in expected.items():
                    self.assertEqual((self.leaf / filename).read_bytes(), content)
        self.assertNotIn(component_path.relative_to(self.root).as_posix(),
                         dict(after.appointment_dependencies))

    def test_existing_component_identity_and_inventory_edits_refuse(self):
        path = self.leaf / "proper-components.toml"
        original = path.read_text()
        for before, after in (
            (DOCUMENT, DOCUMENT.replace("-year-a", "-year-b")),
            ('calendar = "postconciliar"', 'calendar = "roman-1962"'),
            ('"entrance", "collect"', '"collect", "entrance"'),
            ('"acclamation", ', ''),
        ):
            with self.subTest(after=after):
                self.assertIn(before, original)
                path.write_text(original.replace(before, after))
                with self.assertRaisesRegex(ValueError, "component"):
                    self.dossier()
        path.write_text(original)

    def test_corpus_answer_drift_still_invalidates_both_generated_artifacts(self):
        corpus = self.root / "src/sources/chronology"
        corpus.unlink()
        shutil.copytree(ROOT / "src/sources/chronology", corpus)
        for command in ("record", "annotations"):
            done = self.run_cli(command, "--write")
            self.assertEqual(done.returncode, 0, done.stderr)
        composition_path = corpus / "composition.yaml"
        data = yaml.safe_load(composition_path.read_text())
        unit = next(item for item in data["units"] if item["id"] == "composition.gospel-of-matthew")
        unit["dates"][0]["date"]["label"] += " (fixture correction)"
        composition_path.write_text(yaml.safe_dump(data, sort_keys=False))
        for command, refusal in (("record", "not what the corpus now answers"),
                                 ("annotations", "not the current chronology annotation projection")):
            done = self.run_cli(command, "--check")
            self.assertEqual(done.returncode, 1, done.stderr)
            self.assertIn(refusal, done.stderr)

    def test_wrong_family_provider_formula_and_owner_refuse(self):
        original = self.input.read_text()
        replacements = [
            ('calendar = "postconciliar"', 'calendar = "roman-1962"'),
            ('formula = "PC-S51-A"', 'formula = "PC-S51-B"'),
            ('formula = "PC-S51-A"', 'formula = "PC-S99-A"'),
            ('weeks/25/propers/verified.md', 'weeks/24/propers/verified.md'),
            ('roman-missal-third-edition-en-us-2011/propers/temporal/shared',
             'other-edition/propers/temporal/shared'),
        ]
        for before, after in replacements:
            with self.subTest(after=after):
                self.input.write_text(original.replace(before, after))
                with self.assertRaises(ValueError):
                    self.dossier()
        self.input.write_text(original)
        with self.assertRaises(ValueError):
            chronology.dossier(DOCUMENT, root=self.root, provider="claude")
        for document in (DOCUMENT.replace("postconciliar", "byzantine"),
                         DOCUMENT.replace("/temporal/", "/ritual/"),
                         "liturgy/roman-rite/byzantine/propers/temporal/57-not-a-1962-mass"):
            with self.assertRaises(ValueError):
                chronology.dossier(document, root=self.root, provider="gpt")

    def test_complete_partition_and_explicit_non_scriptural_reason_required(self):
        original = self.input.read_text()
        for before, after in [('key = "acclamation"', 'key = "gospel"'),
                              ('non_scriptural_reason = "Composed oration, no appointed citation."', ''),
                              ('kind = "adaptation"', 'kind = "appointed"'),
                              ('system = "hebrew"', 'system = "nova-vulgata"'),
                              ('Psalm 119:4-5', 'Psalm 119:400-500'),
                              ('kind = "appointed"', 'kind = "appointed", date = "A.D. 50"')]:
            with self.subTest(after=after):
                self.input.write_text(original.replace(before, after))
                with self.assertRaises(ValueError):
                    self.dossier()
        self.input.write_text(original)
        instance = self.leaf / "instance/manifest.md"
        instance.write_text(instance.read_text().replace("| 1 | entrance |", "| 1 | different |"))
        with self.assertRaisesRegex(ValueError, "instance inventory"):
            self.dossier()

    def test_out_of_bounds_cross_chapter_endpoints_refuse_before_expansion(self):
        original = self.input.read_text()
        for citation in ("Matthew 20:100-21:2", "Matthew 20:1-21:0",
                         "Matthew 20:100-21:0", "Matthew 20:100",
                         "Matthew 0:1-1:2", "Matthew 28:20-29:0"):
            with self.subTest(citation=citation):
                self.input.write_text(original.replace("Matthew 20:1-16a", citation))
                with self.assertRaisesRegex(ValueError, "bounds|counts no verses"):
                    self.dossier()
                done = self.run_cli("loci", "--json")
                self.assertEqual(done.returncode, 1, done.stdout)
        self.input.write_text(original)

    def test_valid_cross_chapter_and_whole_chapter_queries_keep_every_verse(self):
        original = self.input.read_text()
        for citation, expected in (
            ("Matthew 20:34-21:2", ("Matt.20.34", "Matt.21.1", "Matt.21.2")),
            ("Matthew 20", tuple(f"Matt.20.{verse}" for verse in range(1, 35))),
        ):
            with self.subTest(citation=citation):
                self.input.write_text(original.replace("Matthew 20:1-16a", citation))
                self.assertEqual(self.dossier().element("gospel").loci, expected)

    def test_owner_symlink_cannot_hide_a_different_family(self):
        foreign = self.root / "src/gpt/liturgy/roman-rite/1962/propers/owner.md"
        self.write(foreign, self.owner.read_text())
        self.owner.unlink()
        self.owner.symlink_to(foreign)
        with self.assertRaisesRegex(ValueError, "different owner"):
            self.dossier()

    def test_another_registered_formula_uses_only_its_own_explicit_inputs(self):
        # A synthetic fixture proves that identity handling is registry-based,
        # without claiming these fixture citations are that Sunday's appointments.
        document = DOCUMENT.replace("pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a",
                                    "pc-s42-sixteenth-sunday-in-ordinary-time-year-b")
        leaf = self.root / "src/gpt" / document
        shutil.copytree(self.leaf, leaf)
        for suffix in (inputs.INPUT, "proper-components.toml"):
            path = leaf / suffix
            path.write_text(path.read_text().replace(DOCUMENT, document)
                            .replace("PC-S51-A", "PC-S42-B").replace("weeks/25/", "weeks/16/"))
        owner = leaf.parent / "shared/ordinary-time/weeks/16/propers/verified.md"
        self.write(owner, "Synthetic same-family Week 16 appointment fixture.\n")
        self.write(self.registry / "formula-dispositions.md",
                   f"| `PC-S42-B` | `{leaf.name}` | Adopted fixture. |\n")
        found = chronology.dossier(document, root=self.root, provider="gpt")
        self.assertEqual(found.mass, "PC-S42-B")
        self.assertEqual(found.calendar, "postconciliar")
        paths = {path for path, digest in found.appointment_dependencies}
        self.assertIn(owner.relative_to(self.root).as_posix(), paths)
        self.assertNotIn(self.owner.relative_to(self.root).as_posix(), paths)

    def test_legacy_record_schema_and_projection_are_unchanged(self):
        found = chronology.dossier(LEGACY)
        self.assertEqual(found.calendar, "roman-1962")
        self.assertEqual(found.appointment_dependencies, ())
        record = chronology.render(found)
        self.assertEqual(tomllib.loads(record)["schema"], 2)
        self.assertNotIn("appointment_dependencies", record)
        self.assertNotIn("appointment_notes", record)
        self.assertNotIn("appointment-dependency", chronology.render_annotations_tex(chronology.annotations(found)))


if __name__ == "__main__":
    unittest.main()
