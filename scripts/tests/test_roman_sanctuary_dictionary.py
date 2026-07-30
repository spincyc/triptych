import subprocess
import importlib.machinery
import importlib.util
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "lib" / "roman-sanctuary-dictionary"
DICTIONARY_ROOT = ROOT / "src/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary"
SCHEMA = DICTIONARY_ROOT / "shared/schema/inventory-schema.toml"
SELECTIONS = DICTIONARY_ROOT / "shared/schema/edition-selections.toml"
ARTWORK_MANIFEST = DICTIONARY_ROOT / "research/artwork-manifest.toml"
RECORDS = DICTIONARY_ROOT / "shared/objects"


def load_generator():
    loader = importlib.machinery.SourceFileLoader("dictionary_generator", str(SCRIPT))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


GENERATOR = load_generator()


class DictionaryGeneratorTests(unittest.TestCase):
    def test_only_canonical_alpha_assets_are_selectable(self):
        manifest = {
            "asset_files": [
                {"path": "shared/consumer.png", "state": "consumer-eligible"},
                {"path": "shared/canonical.png", "state": "canonical-alpha-eligible"},
                {"path": "shared/held.png", "state": "held"},
                {"path": "shared/rejected.png", "state": "rejected"},
            ]
        }
        self.assertEqual(
            GENERATOR.canonical_alpha_assets(manifest),
            {"shared/canonical.png"},
        )

    def generate(self, output: Path, selections: Path = SELECTIONS) -> None:
        subprocess.run(
            [
                str(SCRIPT),
                "--schema", str(SCHEMA),
                "--selections", str(selections),
                "--artwork-manifest", str(ARTWORK_MANIFEST),
                "--records", str(RECORDS),
                "--output", str(output),
            ],
            check=True,
        )

    def test_one_canonical_alpha_view_excludes_unverified_records(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            alpha = (output / "ed-comprehensive.tex").read_text()
            sidecar = (output / "ed-comprehensive.alpha-admissions.toml").read_text()
            omissions = (output / "ed-comprehensive.alpha-omissions.tex").read_text()
            self.assertIn('status = "alpha"', sidecar)
            self.assertIn('distribution_state = "public-alpha"', sidecar)
            self.assertIn("obj-altar-missal", alpha)
            self.assertIn(r"\RSDObjectRecord{obj-altar-cloths}", alpha)
            self.assertIn(
                r"\RSDObjectRecord{obj-altar-cruet}",
                alpha,
            )
            self.assertIn(
                r"\RSDObjectRecord{obj-communion-plate}",
                alpha,
            )
            self.assertIn(r"\RSDObjectRecord{obj-sacristy-cross}", alpha)
            self.assertIn(r"\RSDObjectRecord{obj-sacristy-bell}", alpha)
            self.assertNotIn(r"\RSDObjectRecord{obj-sacristy-lavatory}", alpha)
            self.assertIn(
                r"{Latin term not asserted}",
                alpha,
            )
            self.assertIn(r"\RSDObjectRecord{obj-chalice}", alpha)
            self.assertIn(r"\RSDObjectRecord{obj-paten}", alpha)
            self.assertIn(r"\RSDObjectRecord{obj-epistle-book}", alpha)
            self.assertIn(r"\RSDObjectRecord{obj-gospel-book}", alpha)
            self.assertNotIn(r"\RSDAlphaOmission{obj-chalice}", omissions)
            self.assertNotIn(r"\RSDAlphaOmission{obj-paten}", omissions)
            isolated_paten = (
                "shared/artwork/pencil/"
                "RPD-FIG-sacred-vessels-0006-iso-paten-v2.png"
            )
            comparison = (
                "shared/artwork/pencil/"
                "RPD-FIG-sacred-vessels-0003-comparison-paten-exemplar.png"
            )
            paten_record = alpha.split(r"\RSDObjectRecord{obj-paten}", 1)[1].split(
                r"\RSDEndObjectRecord", 1
            )[0]
            chalice_record = alpha.split(r"\RSDObjectRecord{obj-chalice}", 1)[1].split(
                r"\RSDEndObjectRecord", 1
            )[0]
            self.assertIn(isolated_paten, paten_record)
            self.assertNotIn(comparison, paten_record)
            self.assertNotIn(comparison, chalice_record)
            self.assertFalse((output / "ed-comprehensive.review.tex").exists())
            self.assertFalse((output / "ed-comprehensive.review-admissions.toml").exists())

    def test_qualifications_are_not_repeated_on_entry_or_coverage_pages(self):
        shell = (DICTIONARY_ROOT / "shared/publication-shell.tex").read_text()
        renderer = (DICTIONARY_ROOT / "shared/generated-record-renderer.tex").read_text()
        format_source = (DICTIONARY_ROOT / "shared/dictionary-format.tex").read_text()
        title = format_source.split(r"\newcommand{\DictionaryTitle}", 1)[1].split(
            r"\newcommand{\DictionaryNoteKey}", 1
        )[0]
        self.assertNotIn(r"\footnotesize\bfseries ALPHA", title)
        self.assertNotIn("source-audited objects", title)
        self.assertNotIn("official liturgical book", title)
        self.assertIn(r"\textbf{Scope.}", format_source)
        self.assertNotIn("ALPHA RECORD", renderer)
        self.assertNotIn("Evidence caveat", renderer)
        self.assertNotIn(r"\section{Coverage}", shell)

    def test_release_status_is_not_reader_facing(self):
        format_source = (DICTIONARY_ROOT / "shared/dictionary-format.tex").read_text()
        shell = (DICTIONARY_ROOT / "shared/publication-shell.tex").read_text()
        self.assertNotIn(r"\footnotesize\bfseries ALPHA", format_source)
        self.assertNotIn("This alpha edition includes only", format_source)
        self.assertIn("This edition includes only", format_source)
        self.assertNotIn("alpha pictorial dictionary", shell.lower())

        for leaf in (
            "comprehensive",
            "altar-server",
            "sacristan",
            "mc-trainer",
            "general-reader",
            "pontifical-ceremonies",
        ):
            source = (DICTIONARY_ROOT / leaf / "main.tex").read_text()
            self.assertNotRegex(source, r"(?i)RSDEditionLine\}\{[^}]*alpha")
            self.assertNotRegex(source, r"(?i)pdftitle=\{[^}]*alpha")

    def test_communion_plate_uses_only_the_isolated_asset(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            isolated = (
                "shared/artwork/pencil/"
                "RPD-FIG-sacred-vessels-0007-iso-communion-plate.png"
            )
            comparison = (
                "shared/artwork/pencil/"
                "RPD-FIG-sacred-vessels-0004-communion-plate-paten-comparison.png"
            )
            for edition in (
                "ed-comprehensive",
                "ed-general-reader",
                "ed-sacristan",
                "ed-mc-trainer",
                "ed-pontifical",
                "ed-altar-server",
            ):
                text = (output / f"{edition}.tex").read_text()
                record = text.split(
                    r"\RSDObjectRecord{obj-communion-plate}", 1
                )[1].split(r"\RSDEndObjectRecord", 1)[0]
                self.assertIn(isolated, record, edition)
                self.assertNotIn(comparison, record, edition)
                self.assertNotIn("{obj-paten}", record, edition)

    def test_generated_editions_use_only_isolated_paten_artwork(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            isolated = (
                "shared/artwork/pencil/"
                "RPD-FIG-sacred-vessels-0006-iso-paten-v2.png"
            )
            comparison = (
                "shared/artwork/pencil/"
                "RPD-FIG-sacred-vessels-0003-comparison-paten-exemplar.png"
            )
            for edition in (
                "ed-comprehensive",
                "ed-general-reader",
                "ed-sacristan",
                "ed-mc-trainer",
                "ed-pontifical",
                "ed-altar-server",
            ):
                text = (output / f"{edition}.tex").read_text()
                record = text.split(r"\RSDObjectRecord{obj-paten}", 1)[1].split(
                    r"\RSDEndObjectRecord", 1
                )[0]
                self.assertIn(isolated, record, edition)
                self.assertNotIn(comparison, text, edition)

    def test_reader_renderer_keeps_record_ids_out_of_entry_headings(self):
        renderer = (
            DICTIONARY_ROOT / "shared/generated-record-renderer.tex"
        ).read_text()
        self.assertIn(r"\newcommand{\RSDLatinAndKeyLine}[2]{#1\par}", renderer)
        self.assertNotIn(r"\RSDLatinKeyLineBox", renderer)
        self.assertNotIn(r"\DictionaryNoteKey{#2}", renderer)
        self.assertEqual(
            renderer.count(
                r"\RSDLatinAndKeyLine{\RSDLatinHeadword}{\RSDObjectID}"
            ),
            4,
        )

    def test_comprehensive_opening_uses_dated_sanctuary_witness(self):
        main = (DICTIONARY_ROOT / "comprehensive/main.tex").read_text()
        self.assertIn("One sanctuary, seen whole", main)
        self.assertIn(
            "RPD-FIG-sanctuary-0001-ecce-homo-chapel-rijks-graphite.png",
            main,
        )
        self.assertIn("A witness, not a model.", main)
        self.assertIn("not a standard", main)
        self.assertIn(r"\textbf{Altar crucifix}", main)
        self.assertIn("vary with the class of Mass", main)
        self.assertIn("Three altar cards", main)
        self.assertIn("Rubricae generales Missalis Romani", main)
        self.assertNotIn("What the Missal places together", main)
        self.assertNotIn("Central cross with crucifix", main)
        self.assertNotIn(
            "RPD-FIG-altar-appointments-0104-sanctuary-relationships-alpha.png",
            main,
        )
        artwork_manifest = ARTWORK_MANIFEST.read_text()
        retired_asset = artwork_manifest.split(
            'id = "file-rpd-sanctuary-relationships-alpha"', 1
        )[1].split("[[asset_files]]", 1)[0]
        self.assertIn('state = "rejected"', retired_asset)

    def test_canonical_output_is_deterministic_and_audience_specific(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            first = (output / "ed-sacristan.tex").read_bytes()
            self.generate(output)
            self.assertEqual(first, (output / "ed-sacristan.tex").read_bytes())
            text = first.decode()
            self.assertIn(r"\RSDObjectRecord{obj-altar-missal}", text)
            self.assertIn(r"\RSDSelectedAudienceNote{Prepare the Missal", text)
            self.assertIn(r"\RSDObjectRecord{obj-altar-cloths}", text)
            self.assertIn(
                r"\RSDSelectedAudienceNote{Prepare three clean blessed cloths",
                text,
            )
            self.assertIn(r"\RSDObjectRecord{obj-altar-cruet}", text)
            self.assertIn(
                r"\RSDSelectedAudienceNote{Prepare the wine and water vessels",
                text,
            )
            self.assertIn(r"\RSDObjectRecord{obj-communion-plate}", text)
            self.assertIn(
                r"\RSDSelectedAudienceNote{Prepare the Communion plate",
                text,
            )
            self.assertIn(r"\RSDObjectRecord{obj-sacristy-cross}", text)
            self.assertIn(
                r"\RSDSelectedAudienceNote{Confirm the locally appointed focus",
                text,
            )
            self.assertIn(r"\RSDObjectRecord{obj-sacristy-bell}", text)
            self.assertNotIn(r"\RSDObjectRecord{obj-sacristy-lavatory}", text)
            self.assertIn(
                r"\RSDSelectedAudienceNote{Identify the local bell",
                text,
            )
            self.assertNotIn("editorial-proposal", text)
            self.assertIn(r"\RSDObjectRecord{obj-epistle-book}", text)
            self.assertIn(r"\RSDObjectRecord{obj-gospel-book}", text)
            self.assertIn(
                r"\RSDSelectedAudienceNote{Prepare the lesson book",
                text,
            )
            self.assertIn(
                r"\RSDSelectedAudienceNote{Prepare the Gospel book",
                text,
            )

    def test_five_generic_editions_use_declared_dense_section_order(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            expectations = {
                "ed-comprehensive": (
                    r"\RSDHeterodoxFivePlateStart{Church And Sanctuary}{1}",
                    r"\RSDBalancedFourPlateStart{Related Ceremonies}{1}",
                ),
                "ed-sacristan": (
                    r"\RSDDensePlateStart{Sanctuary And Altar Preparation}{1}",
                    r"\RSDDensePlateStart{Vessels Linens And Books}{1}",
                ),
                "ed-mc-trainer": (
                    r"\RSDHeterodoxFivePlateStart"
                    r"{Vesting And Sacred Ministers}{1}",
                    r"\RSDDensePlateStart{Books And Supports}{1}",
                ),
                "ed-general-reader": (
                    r"\RSDDensePlateStart{Sanctuary}{1}",
                    r"\RSDDensePlateStart{Objects And Linens}{1}",
                ),
                "ed-pontifical": (
                    r"\RSDBalancedTwoTallPlateStart"
                    r"{Furnishings And Books}{1}",
                    r"\RSDRelationshipThreePlateStart"
                    r"{Ministers And Object Transfers}{1}",
                ),
                "ed-altar-server": (
                    r"\RSDDensePlateStart{Sanctuary Orientation}{1}",
                    r"\RSDDensePlateStart{Objects Around The Server}{1}",
                ),
            }
            for edition, markers in expectations.items():
                text = (output / f"{edition}.tex").read_text()
                positions = [text.index(marker) for marker in markers]
                self.assertEqual(positions, sorted(positions), edition)
                self.assertIn(r"\RSDDensePlateRowBreak", text)
                self.assertIn(r"\RSDDensePlateCellBreak", text)
            for edition in (
                "ed-comprehensive", "ed-altar-server",
            ):
                text = (output / f"{edition}.tex").read_text()
                self.assertNotIn(r"\RSDStoryPlateStart", text)

    def test_pontifical_uses_relationship_led_plate_plan(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            first = (output / "ed-pontifical.tex").read_bytes()
            self.generate(output)
            self.assertEqual(first, (output / "ed-pontifical.tex").read_bytes())
            text = first.decode()
            self.assertEqual(
                text.count(r"\RSDStoryPlateStart{Pontifical Vesture}{1}"), 1
            )
            self.assertEqual(
                text.count(
                    r"\RSDBalancedTwoTallPlateStart{Pontifical Vesture}{2}"
                ),
                1,
            )
            self.assertIn(
                r"\RSDBalancedTwoTallPlateStart{Furnishings And Books}{1}",
                text,
            )
            self.assertIn(
                r"\RSDDensePlateStart{Furnishings And Books}{3}",
                text,
            )
            self.assertIn(r"\RSDObjectRecord{obj-episcopal-throne}", text)
            self.assertIn(r"\RSDObjectRecord{obj-faldstool}", text)
            transfer_two = text.split(
                r"\RSDDensePlateStart{Ministers And Object Transfers}{3}", 1
            )[1].split(r"\RSDDensePlateEnd", 1)[0]
            self.assertEqual(
                tuple(
                    line.split("{", 1)[1].split("}", 1)[0]
                    for line in transfer_two.splitlines()
                    if line.startswith(r"\RSDObjectRecord{")
                ),
                (
                    "obj-acolyte-candlestick",
                    "obj-purificator",
                    "obj-lavabo-towel",
                    "obj-lavabo-basin",
                    "obj-communion-plate",
                    "obj-candle-lighter-extinguisher",
                ),
            )
            transfer_pairs = (
                (
                    5,
                    ("obj-aspergillum", "obj-holy-water-vessel"),
                ),
                (
                    6,
                    ("obj-basilical-conopaeum", "obj-ombrellino"),
                ),
            )
            for plate_number, expected_ids in transfer_pairs:
                marker = (
                    r"\RSDBalancedTwoTallPlateStart"
                    rf"{{Ministers And Object Transfers}}{{{plate_number}}}"
                )
                plate = text.split(marker, 1)[1].split(
                    r"\RSDBalancedTwoTallPlateEnd", 1
                )[0]
                actual_ids = tuple(
                    line.split("{", 1)[1].split("}", 1)[0]
                    for line in plate.splitlines()
                    if line.startswith(r"\RSDObjectRecord{")
                )
                self.assertEqual(actual_ids, expected_ids)
            rendered_ids = [
                line.split("{", 1)[1].split("}", 1)[0]
                for line in text.splitlines()
                if line.startswith(r"\RSDObjectRecord{")
            ]
            self.assertEqual(len(rendered_ids), len(set(rendered_ids)))

    def test_general_reader_uses_exact_heterodox_plate_plan(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            first = (output / "ed-general-reader.tex").read_bytes()
            self.generate(output)
            self.assertEqual(first, (output / "ed-general-reader.tex").read_bytes())
            text = first.decode()
            self.assertEqual(
                text.count(r"\RSDStoryPlateStart{Vestments And Insignia}{1}"), 1
            )
            self.assertEqual(
                text.count(
                    r"\RSDStoryTallPlateStart{Vestments And Insignia}{2}"
                ), 1
            )
            self.assertEqual(
                text.count(r"\RSDRelationshipThreePlateStart{Sanctuary}{2}"), 1
            )
            self.assertEqual(
                text.count(r"\RSDStoryTallPlateStart{Objects And Linens}{4}"), 1
            )
            self.assertEqual(
                text.count(
                    r"\RSDBalancedFourPlateStart{Objects And Linens}{5}"
                ), 1
            )
            self.assertNotIn(r"\RSDStoryPlateStart{Objects And Linens}", text)
            sanctuary_triptych = text.split(
                r"\RSDRelationshipThreePlateStart{Sanctuary}{2}", 1
            )[1].split(r"\RSDRelationshipThreePlateEnd", 1)[0]
            sanctuary_triptych_ids = [
                line.split("{", 1)[1].split("}", 1)[0]
                for line in sanctuary_triptych.splitlines()
                if line.startswith(r"\RSDObjectRecord{")
            ]
            self.assertEqual(
                sanctuary_triptych_ids,
                [
                    "obj-altar-cloths",
                    "obj-missal-cushion",
                    "obj-missal-stand",
                ],
            )
            self.assertEqual(sanctuary_triptych.count(r"\RSDTallCardNext"), 1)
            self.assertEqual(
                sanctuary_triptych.count(r"\RSDRelationshipCardNext"), 2
            )
            self.assertEqual(
                sanctuary_triptych.count(r"\RSDRelationshipThreePlateCellBreak"),
                1,
            )
            self.assertEqual(
                sanctuary_triptych.count(r"\RSDRelationshipThreePlateRightBreak"),
                1,
            )
            story = text.split(
                r"\RSDStoryPlateStart{Vestments And Insignia}{1}", 1
            )[1].split(r"\RSDStoryPlateEnd", 1)[0]
            dalmatic_story = text.split(
                r"\RSDStoryTallPlateStart{Vestments And Insignia}{2}", 1
            )[1].split(r"\RSDStoryTallPlateEnd", 1)[0]
            story_ids = [
                line.split("{", 1)[1].split("}", 1)[0]
                for line in story.splitlines()
                if line.startswith(r"\RSDObjectRecord{")
            ]
            dalmatic_story_ids = [
                line.split("{", 1)[1].split("}", 1)[0]
                for line in dalmatic_story.splitlines()
                if line.startswith(r"\RSDObjectRecord{")
            ]
            self.assertEqual(
                story_ids,
                [
                    "obj-chasuble",
                    "obj-amice",
                    "obj-alb",
                    "obj-cincture",
                    "obj-maniple",
                ],
            )
            self.assertEqual(
                dalmatic_story_ids,
                [
                    "obj-dalmatic",
                    "obj-priest-stole",
                    "obj-deacon-stole",
                    "obj-tunicle",
                ],
            )
            self.assertEqual(text.count(r"\RSDStoryHeroNext"), 1)
            self.assertEqual(text.count(r"\RSDStoryCompanionsStart"), 1)
            self.assertEqual(dalmatic_story.count(r"\RSDStoryTallHeroNext"), 1)
            self.assertEqual(
                dalmatic_story.count(r"\RSDStoryTallCompanionsStart"), 1
            )
            self.assertEqual(
                dalmatic_story.count(r"\RSDStoryTallCompanionBreak"), 2
            )
            self.assertEqual(text.count(r"\RSDStoryTallHeroNext"), 2)
            self.assertEqual(text.count(r"\RSDStoryTallCompanionsStart"), 2)
            self.assertEqual(text.count(r"\RSDBalancedFourFilledPlateRowBreak"), 1)
            self.assertEqual(text.count(r"\RSDQuadCardNext"), 4)
            rendered_ids = [
                line.split("{", 1)[1].split("}", 1)[0]
                for line in text.splitlines()
                if line.startswith(r"\RSDObjectRecord{")
            ]
            self.assertEqual(len(rendered_ids), 43)
            self.assertEqual(len(set(rendered_ids)), 43)
            for object_id in story_ids + dalmatic_story_ids:
                self.assertEqual(
                    text.count(f"\\RSDObjectRecord{{{object_id}}}"), 1, object_id
                )

    def test_mc_trainer_uses_exact_nine_plate_semantic_plan(self):
        expected_plates = (
            (
                "obj-amice", "obj-alb", "obj-cincture", "obj-maniple",
                "obj-priest-stole",
            ),
            ("obj-chasuble", "obj-deacon-stole", "obj-dalmatic", "obj-tunicle"),
            (
                "obj-credence-table", "obj-lectern", "obj-sacristy-cross",
                "obj-sanctuary-lamp", "obj-sedilia",
            ),
            (
                "obj-altar-missal", "obj-missal-stand", "obj-missal-cushion",
                "obj-altar-cloths", "obj-epistle-book",
                "obj-gospel-book",
            ),
            (
                "obj-altar-candle", "obj-altar-candlestick",
                "obj-acolyte-candlestick", "obj-elevation-torch",
                "obj-candle-lighter-extinguisher", "obj-altar-bells",
                "obj-sacristy-bell",
            ),
            (
                "obj-chalice", "obj-paten", "obj-corporal", "obj-purificator",
                "obj-chalice-pall", "obj-chalice-veil", "obj-burse",
            ),
            (
                "obj-altar-cruet", "obj-lavabo-basin", "obj-lavabo-towel",
                "obj-communion-plate",
            ),
            (
                "obj-processional-cross", "obj-incense-boat-and-spoon",
                "obj-thurible",
                "obj-aspergillum", "obj-holy-water-vessel",
                "obj-basilical-conopaeum", "obj-ombrellino",
            ),
        )
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            text = (output / "ed-mc-trainer.tex").read_text()
            actual_ids = tuple(
                line.split("{", 1)[1].split("}", 1)[0]
                for line in text.splitlines()
                if line.startswith(r"\RSDObjectRecord{")
            )
            expected_ids = tuple(
                object_id for plate in expected_plates for object_id in plate
            )
            self.assertEqual(actual_ids, expected_ids)
            self.assertEqual(len(actual_ids), 45)
            self.assertEqual(len(set(actual_ids)), 45)
            self.assertEqual(text.count(r"\RSDDensePlateStart"), 1)
            self.assertEqual(text.count(r"\RSDStoryPlateStart"), 1)
            self.assertEqual(text.count(r"\RSDRelationshipThreePlateStart"), 0)
            self.assertIn(
                r"\RSDBalancedFourPlateStart"
                r"{Vesting And Sacred Ministers}{2}", text
            )
            self.assertIn(
                r"\RSDDenseSevenPlateStart"
                r"{Processions And Special Ceremonies}{1}",
                text,
            )
            self.assertEqual(text.count(r"\RSDDenseSevenPlateStart"), 3)
            self.assertNotIn(r"\RSDBalancedThreeTallPlateStart", text)
            self.assertEqual(text.count(r"\RSDBalancedFourPlateStart"), 2)
            self.assertEqual(text.count(r"\RSDDenseSevenPlateRowBreak"), 3)
            self.assertEqual(text.count(r"\RSDDenseSevenPlateCellBreak"), 15)
            self.assertEqual(text.count(r"\RSDSevenCardNext"), 21)
            self.assertNotIn("People Roles And Stations", text)
            self.assertIn("Books And Supports", text)
            self.assertIn("Lights And Signals", text)
            self.assertIn("Prepared Chalice", text)

    def test_sacristan_preparation_uses_exact_heterodox_plate_plan(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            text = (output / "ed-sacristan.tex").read_text()
            first_marker = (
                r"\RSDDensePlateStart{Sanctuary And Altar Preparation}{1}"
            )
            section = first_marker + text.split(first_marker, 1)[1].split(
                r"\RSDDensePlateStart{Vessels Linens And Books}{1}", 1
            )[0]
            expected_plates = (
                (
                    "obj-credence-table",
                    "obj-lectern",
                    "obj-sacristy-cross",
                    "obj-sanctuary-lamp",
                    "obj-sedilia",
                    "obj-altar-candle",
                ),
                (
                    "obj-altar-candlestick",
                    "obj-altar-cloths",
                    "obj-missal-cushion",
                    "obj-missal-stand",
                    "obj-acolyte-candlestick",
                    "obj-altar-bells",
                ),
                (
                    "obj-processional-cross",
                    "obj-elevation-torch",
                    "obj-candle-lighter-extinguisher",
                    "obj-sacristy-bell",
                ),
                (
                    "obj-lavabo-basin",
                    "obj-altar-cruet",
                    "obj-communion-plate",
                ),
            )
            markers = (
                (
                    r"\RSDDensePlateStart"
                    r"{Sanctuary And Altar Preparation}{1}",
                    r"\RSDDensePlateEnd",
                ),
                (
                    r"\RSDDensePlateStart"
                    r"{Sanctuary And Altar Preparation}{2}",
                    r"\RSDDensePlateEnd",
                ),
                (
                    r"\RSDStoryTallPlateStart"
                    r"{Sanctuary And Altar Preparation}{3}",
                    r"\RSDStoryTallPlateEnd",
                ),
                (
                    r"\RSDRelationshipThreePlateStart"
                    r"{Sanctuary And Altar Preparation}{4}",
                    r"\RSDRelationshipThreePlateEnd",
                ),
            )
            actual_plates = []
            for marker, end_marker in markers:
                plate = section.split(marker, 1)[1].split(end_marker, 1)[0]
                actual_plates.append(
                    tuple(
                        line.split("{", 1)[1].split("}", 1)[0]
                        for line in plate.splitlines()
                        if line.startswith(r"\RSDObjectRecord{")
                    )
                )
            self.assertEqual(tuple(actual_plates), expected_plates)
            planned_ids = [
                object_id for plate in actual_plates for object_id in plate
            ]
            self.assertEqual([len(plate) for plate in actual_plates], [6, 6, 4, 3])
            self.assertEqual(len(planned_ids), 19)
            self.assertEqual(len(set(planned_ids)), 19)
            self.assertEqual(section.count(r"\RSDStoryTallHeroNext"), 1)
            self.assertEqual(section.count(r"\RSDStoryTallCompanionsStart"), 1)
            self.assertEqual(
                section.count(r"\RSDRelationshipThreePlateCellBreak"), 1
            )
            self.assertEqual(
                section.count(r"\RSDRelationshipThreePlateRightBreak"), 1
            )
            for object_id in planned_ids:
                self.assertEqual(
                    text.count(f"\\RSDObjectRecord{{{object_id}}}"), 1, object_id
                )
            self.assertEqual(
                section.count(r"\RSDFieldCardNext"),
                12,
            )

            self.assertIn(
                r"\RSDBalancedTwoTallPlateStart"
                r"{Vessels Linens And Books}{3}",
                text,
            )
            self.assertIn(
                r"\RSDRelationshipThreePlateStart"
                r"{Vestments And Insignia}{2}",
                text,
            )
            self.assertIn(
                r"\RSDBalancedFourPlateStart"
                r"{Special Ceremony Equipment}{1}",
                text,
            )
            special = text.split(
                r"\RSDBalancedFourPlateStart"
                r"{Special Ceremony Equipment}{1}",
                1,
            )[1].split(r"\RSDBalancedFourFilledPlateEnd", 1)[0]
            special_ids = tuple(
                line.split("{", 1)[1].split("}", 1)[0]
                for line in special.splitlines()
                if line.startswith(r"\RSDObjectRecord{")
            )
            self.assertEqual(
                special_ids,
                (
                    "obj-aspergillum",
                    "obj-holy-water-vessel",
                    "obj-basilical-conopaeum",
                    "obj-ombrellino",
                ),
            )
            self.assertEqual(special.count(r"\RSDQuadCardNext"), 4)
            story = section.split(
                r"\RSDStoryTallPlateStart"
                r"{Sanctuary And Altar Preparation}{3}",
                1,
            )[1].split(r"\RSDStoryTallPlateEnd", 1)[0]
            self.assertEqual(story.count(r"\RSDSpacedCardNext"), 3)

    def test_general_reader_objects_and_linens_use_exact_dense_plate_plan(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            text = (output / "ed-general-reader.tex").read_text()
            first_marker = r"\RSDDensePlateStart{Objects And Linens}{1}"
            section = first_marker + text.split(first_marker, 1)[1].split(
                r"\RSDStoryPlateStart{Vestments And Insignia}{1}", 1
            )[0]
            expected_plates = (
                (
                    "obj-chalice",
                    "obj-paten",
                    "obj-burse",
                    "obj-chalice-pall",
                    "obj-chalice-veil",
                    "obj-corporal",
                ),
                (
                    "obj-purificator",
                    "obj-lavabo-towel",
                    "obj-epistle-book",
                    "obj-gospel-book",
                    "obj-altar-missal",
                ),
                (
                    "obj-altar-bells",
                    "obj-lavabo-basin",
                    "obj-communion-plate",
                    "obj-altar-cruet",
                    "obj-acolyte-candlestick",
                    "obj-elevation-torch",
                ),
                (
                    "obj-processional-cross",
                    "obj-sacristy-bell",
                    "obj-incense-boat-and-spoon",
                    "obj-thurible",
                ),
                (
                    "obj-aspergillum",
                    "obj-holy-water-vessel",
                    "obj-basilical-conopaeum",
                    "obj-ombrellino",
                ),
            )
            actual_plates = []
            for plate_number in range(1, 6):
                if plate_number in {1, 3}:
                    marker = (
                        rf"\RSDDensePlateStart{{Objects And Linens}}"
                        rf"{{{plate_number}}}"
                    )
                    end_marker = r"\RSDDensePlateEnd"
                elif plate_number == 2:
                    marker = (
                        r"\RSDHeterodoxFivePlateStart{Objects And Linens}{2}"
                    )
                    end_marker = r"\RSDHeterodoxFivePlateEnd"
                elif plate_number == 4:
                    marker = (
                        r"\RSDStoryTallPlateStart{Objects And Linens}{4}"
                    )
                    end_marker = r"\RSDStoryTallPlateEnd"
                else:
                    marker = (
                        rf"\RSDBalancedFourPlateStart{{Objects And Linens}}"
                        rf"{{{plate_number}}}"
                    )
                    end_marker = r"\RSDBalancedFourFilledPlateEnd"
                plate = section.split(marker, 1)[1].split(end_marker, 1)[0]
                actual_plates.append(
                    tuple(
                        line.split("{", 1)[1].split("}", 1)[0]
                        for line in plate.splitlines()
                        if line.startswith(r"\RSDObjectRecord{")
                    )
                )
            self.assertEqual(tuple(actual_plates), expected_plates)
            planned_ids = [
                object_id for plate in actual_plates for object_id in plate
            ]
            self.assertEqual([len(plate) for plate in actual_plates], [6, 5, 6, 4, 4])
            self.assertEqual(len(planned_ids), 25)
            self.assertEqual(len(set(planned_ids)), 25)
            self.assertEqual(
                section.count(r"\RSDBalancedFourPlateStart{Objects And Linens}"),
                1,
            )
            self.assertEqual(
                section.count(r"\RSDBalancedFourFilledPlateRowBreak"), 1
            )
            story_tall = section.split(
                r"\RSDStoryTallPlateStart{Objects And Linens}{4}", 1
            )[1].split(r"\RSDStoryTallPlateEnd", 1)[0]
            self.assertEqual(story_tall.count(r"\RSDStoryTallHeroNext"), 1)
            self.assertEqual(
                story_tall.count(r"\RSDStoryTallCompanionsStart"), 1
            )
            self.assertEqual(
                story_tall.count(r"\RSDStoryTallCompanionBreak"), 2
            )
            self.assertEqual(story_tall.count(r"\RSDSpacedCardNext"), 3)
            semantic_pairs = section.split(
                r"\RSDBalancedFourPlateStart{Objects And Linens}{5}", 1
            )[1].split(r"\RSDBalancedFourFilledPlateEnd", 1)[0]
            self.assertEqual(semantic_pairs.count(r"\RSDQuadCardNext"), 4)
            self.assertEqual(
                semantic_pairs.count(r"\RSDBalancedFourPlateCellBreak"), 2
            )
            self.assertEqual(
                semantic_pairs.count(r"\RSDBalancedFourFilledPlateRowBreak"), 1
            )
            for object_id in planned_ids:
                self.assertEqual(
                    text.count(f"\\RSDObjectRecord{{{object_id}}}"), 1, object_id
                )

    def test_comprehensive_uses_exact_density_plate_plan(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            first = (output / "ed-comprehensive.tex").read_bytes()
            self.generate(output)
            self.assertEqual(first, (output / "ed-comprehensive.tex").read_bytes())
            text = first.decode()
            expected_plates = (
                (
                    r"\RSDHeterodoxFivePlateStart{Church And Sanctuary}{1}",
                    r"\RSDHeterodoxFivePlateEnd",
                    (
                        "obj-credence-table", "obj-lectern",
                        "obj-sacristy-cross", "obj-sanctuary-lamp",
                        "obj-sedilia",
                    ),
                ),
                (
                    r"\RSDHeterodoxFivePlateStart{Altar And Appointments}{1}",
                    r"\RSDHeterodoxFivePlateEnd",
                    (
                        "obj-altar-candle", "obj-altar-candlestick",
                        "obj-altar-cloths", "obj-missal-cushion",
                        "obj-missal-stand",
                    ),
                ),
                (
                    r"\RSDBalancedFourPlateStart{Linens And Textiles}{1}",
                    r"\RSDBalancedFourFilledPlateEnd",
                    (
                        "obj-chalice", "obj-paten", "obj-burse",
                        "obj-chalice-pall",
                    ),
                ),
                (
                    r"\RSDBalancedFourPlateStart{Linens And Textiles}{2}",
                    r"\RSDBalancedFourFilledPlateEnd",
                    (
                        "obj-chalice-veil", "obj-corporal",
                        "obj-purificator", "obj-lavabo-towel",
                    ),
                ),
                (
                    r"\RSDDensePlateStart{Service Objects}{1}",
                    r"\RSDDensePlateEnd",
                    (
                        "obj-acolyte-candlestick", "obj-altar-bells",
                        "obj-lavabo-basin",
                        "obj-candle-lighter-extinguisher",
                        "obj-communion-plate", "obj-altar-cruet",
                    ),
                ),
                (
                    r"\RSDHeterodoxFivePlateStart{Service Objects}{2}",
                    r"\RSDHeterodoxFivePlateEnd",
                    (
                        "obj-elevation-torch", "obj-sacristy-bell",
                        "obj-processional-cross",
                        "obj-incense-boat-and-spoon", "obj-thurible",
                    ),
                ),
                (
                    r"\RSDHeterodoxFivePlateStart{Priestly Vestments}{1}",
                    r"\RSDHeterodoxFivePlateEnd",
                    (
                        "obj-amice", "obj-alb", "obj-cincture",
                        "obj-maniple", "obj-priest-stole",
                    ),
                ),
                (
                    r"\RSDBalancedFourPlateStart{Priestly Vestments}{2}",
                    r"\RSDBalancedFourFilledPlateEnd",
                    (
                        "obj-chasuble", "obj-deacon-stole",
                        "obj-dalmatic", "obj-tunicle",
                    ),
                ),
            )
            for start, end, expected_ids in expected_plates:
                plate = text.split(start, 1)[1].split(end, 1)[0]
                actual_ids = tuple(
                    line.split("{", 1)[1].split("}", 1)[0]
                    for line in plate.splitlines()
                    if line.startswith(r"\RSDObjectRecord{")
                )
                self.assertEqual(actual_ids, expected_ids)
            for section in ("Church And Sanctuary", "Altar And Appointments"):
                plate = text.split(
                    rf"\RSDHeterodoxFivePlateStart{{{section}}}{{1}}", 1
                )[1].split(r"\RSDHeterodoxFivePlateEnd", 1)[0]
                self.assertEqual(plate.count(r"\RSDDiagnosticCardNext"), 3)
                self.assertEqual(plate.count(r"\RSDWideCardNext"), 2)
                self.assertEqual(
                    plate.count(r"\RSDHeterodoxFivePlateRowBreak"), 1
                )
            self.assertGreaterEqual(text.count(r"\RSDDiagnosticCardNext"), 18)
            rendered_ids = [
                line.split("{", 1)[1].split("}", 1)[0]
                for line in text.splitlines()
                if line.startswith(r"\RSDObjectRecord{")
            ]
            self.assertEqual(len(rendered_ids), len(set(rendered_ids)))

    def test_text_only_lavatory_is_held_from_every_generated_edition(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            for edition in (
                "ed-comprehensive", "ed-sacristan", "ed-mc-trainer",
                "ed-general-reader", "ed-pontifical", "ed-altar-server",
            ):
                text = (output / f"{edition}.tex").read_text()
                self.assertNotIn(r"\RSDObjectRecord{obj-sacristy-lavatory}", text)

    def test_epistle_and_gospel_books_use_distinct_ceremonial_artwork(self):
        renderer = (
            DICTIONARY_ROOT / "shared/generated-record-renderer.tex"
        ).read_text()
        self.assertNotIn(r"\RSDTeXNativeBookArtwork", renderer)
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "out"
            self.generate(output)
            for edition in (
                "ed-comprehensive", "ed-sacristan", "ed-mc-trainer",
                "ed-general-reader", "ed-pontifical", "ed-altar-server",
            ):
                text = (output / f"{edition}.tex").read_text()
                self.assertIn(
                    "RPD-FIG-books-0006-epistle-book-in-use-alpha.png", text
                )
                self.assertIn(
                    "RPD-FIG-books-0007-gospel-book-in-use-v2-alpha.png", text
                )

    def test_shared_artwork_uses_data_driven_render_owner(self):
        renderer = (
            DICTIONARY_ROOT / "shared/generated-record-renderer.tex"
        ).read_text()
        self.assertNotIn("obj-chalice", renderer)
        self.assertNotIn("art-paten-catalog-exemplar-comparison", renderer)
        self.assertIn(r"\ifdefstring{\RSDObjectID}{#8}", renderer)

    def test_unknown_record_field_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            records = root / "records"
            records.mkdir()
            fixture = (
                DICTIONARY_ROOT / "shared/schema/object.example.toml"
            ).read_text().replace(
                "schema_version = 1",
                "schema_version = 1\nunknown = true",
                1,
            )
            (records / "bad.toml").write_text(fixture)
            result = subprocess.run(
                [
                    str(SCRIPT),
                    "--schema", str(SCHEMA),
                    "--selections", str(SELECTIONS),
                    "--artwork-manifest", str(ARTWORK_MANIFEST),
                    "--records", str(records),
                    "--output", str(root / "out"),
                ],
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown top-level field", result.stderr)


if __name__ == "__main__":
    unittest.main()
