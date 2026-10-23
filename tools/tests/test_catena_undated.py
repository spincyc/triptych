"""Explicitly unestablished composition dates never become guessed years."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _catena  # noqa: E402
if __package__:
    from .test_catena import CatenaFixture  # noqa: E402
else:
    from test_catena import CatenaFixture  # noqa: E402

ROOT = _catena.ROOT
REASON = (
    "The consulted printing identifies this homily but supplies no composition "
    "date; its 1871 publication date and the author's death in 430 do not date "
    "the text. This review has established no numeric date."
)


class UndatedAdmissionTests(CatenaFixture):
    passage_id = "passage.augustine.de-civitate-dei.dods-1871.11.7"
    edition_path = "src/sources/works/augustine/de-civitate-dei/editions/dods-1871/"
    work_path = "src/sources/works/augustine/de-civitate-dei/work.toml"

    def declare(self, **overrides: object) -> None:
        values = {
            "text_date": None,
            "text_date_basis": None,
            "composition_date_unestablished": REASON,
        }
        values.update(overrides)
        self.write_edges(**values)
        _catena._SOURCES_CACHE.pop(self.root, None)

    def work_date(self, value: str) -> None:
        path = self.root / self.work_path
        path.write_text(path.read_text() + "composed = " + json.dumps(value) + "\n")
        _catena._SOURCES_CACHE.pop(self.root, None)

    def change_passage(self, before: str, after: str) -> None:
        path = self.root / self.edition_path / "passages/11.7.toml"
        path.write_text(path.read_text().replace(before, after))
        _catena._SOURCES_CACHE.pop(self.root, None)

    def test_bare_missing_date_is_still_refused_by_check_and_emit(self) -> None:
        self.write_edges(text_date=None, text_date_basis=None)
        self.assertIn("dated by nothing", " ".join(self.errors()))
        with self.assertRaises(_catena.CatenaError):
            _catena.fragments_for_book(self.root, "Gen")

    def test_nonempty_explicit_reason_admits_direct_controller(self) -> None:
        self.declare()
        self.assertEqual(self.errors(), [])
        row = _catena.fragments_for_book(self.root, "Gen")[0]
        self.assertIsNone(row["date"])
        self.assertEqual(row["composition_date_status"], "unestablished")
        self.assertEqual(row["composition_date_basis"], REASON)
        self.assertEqual(row["date_basis"], REASON)

    def test_malformed_or_blank_reason_is_never_an_implicit_unknown(self) -> None:
        for value in (None, False, 398, [], {}, "", " \n\t "):
            with self.subTest(value=value):
                self.declare(composition_date_unestablished=value)
                self.assertIn("must be a nonempty plain-text", " ".join(self.errors()))
                with self.assertRaises(_catena.CatenaError):
                    _catena.fragments_for_book(self.root, "Gen")

    def test_numeric_override_and_explicit_unknown_are_contradictory(self) -> None:
        self.declare(text_date=417, text_date_basis="The text is dated independently.")
        self.assertIn("cannot accompany a numeric text_date", " ".join(self.errors()))

    def test_known_work_date_rejects_unknown_declaration(self) -> None:
        self.work_date("c. 401-415")
        self.declare()
        self.assertIn("contradicts", " ".join(self.errors()))

    def test_a_later_work_date_requires_review_of_the_unknown_declaration(self) -> None:
        self.declare()
        self.assertEqual(self.errors(), [])
        self.work_date("401")
        self.assertIn("remove the stale declaration", " ".join(self.errors()))
        with self.assertRaises(_catena.CatenaError):
            _catena.fragments_for_book(self.root, "Gen")

    def test_text_date_basis_without_integer_override_is_still_refused(self) -> None:
        for value in ("An unsupported date explanation.", "", False, [], {}):
            with self.subTest(value=value):
                self.declare(text_date_basis=value)
                self.assertIn("text_date it does not have", " ".join(self.errors()))

    def test_wrong_type_override_cannot_be_ignored_in_favor_of_unknown(self) -> None:
        for value in ("398", 398.0, True, [], {}):
            with self.subTest(value=value):
                self.declare(text_date=value)
                self.assertIn("text_date must be an integer year", " ".join(self.errors()))

    def test_publication_death_and_review_numbers_never_supply_a_date(self) -> None:
        self.declare()
        row = _catena.fragments_for_book(self.root, "Gen")[0]
        self.assertIsNone(row["date"])
        self.assertNotIn(row["date"], (1871, 430))
        self.assertIsNone(_catena.fragment_year({}, {
            "date": "1871", "death": 430, "description": "Reviewed in 2026.",
        }))

    def test_unsupported_composed_notation_requires_explicit_limit(self) -> None:
        self.work_date("saec. VIII in.")
        self.write_edges(text_date=None, text_date_basis=None)
        self.assertIn("dated by nothing", " ".join(self.errors()))
        self.declare()
        self.assertEqual(self.errors(), [])
        self.assertIsNone(_catena.fragments_for_book(self.root, "Gen")[0]["date"])

    def test_unknown_date_changes_no_text_identity_voice_rights_or_extent(self) -> None:
        dated = _catena.fragments_for_book(self.root, "Gen")[0]
        self.declare()
        undated = _catena.fragments_for_book(self.root, "Gen")[0]
        for key, value in dated.items():
            if key not in {"date", "date_basis"}:
                self.assertEqual(undated[key], value, key)

    def test_dated_rows_keep_prior_date_fields_and_no_optional_metadata(self) -> None:
        row = _catena.fragments_for_book(self.root, "Gen")[0]
        self.assertEqual(row["date"], 417)
        self.assertEqual(row["date_basis"], "Books XI-XIV were issued about 417.")
        self.assertNotIn("composition_date_status", row)
        self.assertNotIn("composition_date_basis", row)
        shared, slim = _catena._fold_shared([row])
        self.assertNotIn("composition_date_status", shared["0"])
        self.assertNotIn("composition_date_basis", shared["0"])
        self.assertNotIn("composition_date_status", slim[0])

    def test_existing_numeric_work_and_override_paths_are_preserved(self) -> None:
        self.work_date("c. 401-415")
        self.write_edges(text_date=None, text_date_basis=None)
        self.assertEqual(self.errors(), [])
        self.assertEqual(_catena.fragments_for_book(self.root, "Gen")[0]["date"], 401)
        self.write_edges(text_date=417, text_date_basis="This particular text is later.")
        self.assertEqual(self.errors(), [])
        self.assertEqual(_catena.fragments_for_book(self.root, "Gen")[0]["date"], 417)
        self.write_edges(text_date=401)
        self.assertIn("restates text_date", " ".join(self.errors()))

    def test_dated_chain_and_secondary_unknown_order_are_deterministic(self) -> None:
        self.declare()
        data = _catena.load_edges(self.root)
        undated = data["fragments"][0]
        rows = []
        original = (self.root / self.edition_path / "passages/11.7.toml").read_text()
        for suffix, year in (("z", None), ("late", 417), ("a", None), ("early", 400)):
            row = copy.deepcopy(undated)
            row["passage_id"] = self.passage_id + "." + suffix
            if year is not None:
                row.pop("composition_date_unestablished")
                row["text_date"] = year
                row["text_date_basis"] = "This particular text has a sourced year."
            rows.append(row)
            self.write(self.edition_path + f"passages/{suffix}.toml", original.replace(
                self.passage_id, row["passage_id"],
            ))
        data["fragments"] = rows
        import yaml
        self.write(str(_catena.EDGES_RELATIVE), yaml.safe_dump(data))
        self.assertEqual(self.errors(), [])
        first = _catena.fragments_for_book(self.root, "Gen")
        second = _catena.fragments_for_book(self.root, "Gen")
        self.assertEqual(first, second)
        self.assertEqual([row["id"].rsplit(".", 1)[1] for row in first], ["early", "late", "a", "z"])
        self.assertEqual([row["date"] for row in first], [400, 417, None, None])

    def test_unknown_reason_is_shared_and_reaches_lazy_date_apparatus(self) -> None:
        self.declare(composition_date_unestablished="  " + REASON + "  ")
        self.write(str(_catena.MODEL_RELATIVE), (ROOT / _catena.MODEL_RELATIVE).read_text())
        directory, files, _written = _catena._structure_files(self.root, self.root / "out")
        index = json.loads(files[directory / "index.json"])
        folder = next(book["path"] for book in index["canon"] if book["token"] == "Gen")
        chapter_name = _catena._canon.chapter_name(1, index["chapter_digits"])
        spine = json.loads(files[directory / folder / chapter_name])
        source = spine["sources"][spine["fragments"][0]["source"]]
        self.assertIsNone(source["date"])
        self.assertEqual(source["composition_date_status"], "unestablished")
        self.assertEqual(source["composition_date_basis"], REASON)
        payload = json.loads(files[directory / "text" / (self.passage_id + ".json")])
        self.assertEqual(payload["date_basis"], REASON)

    def test_unknown_without_text_is_still_refused(self) -> None:
        self.declare()
        self.change_passage(
            'text = "And first of all, indeed, light was made by the word of God."', 'text = ""',
        )
        self.assertIn("has no text", " ".join(self.errors()))

    def test_unknown_without_controller_is_still_refused(self) -> None:
        self.declare()
        self.change_passage('artifact_id = "artifact.augustine.de-civitate-dei.dods-1871.body"', "")
        self.assertIn("reaches no artifact", " ".join(self.errors()))

    def test_unknown_with_restricted_rights_is_still_refused(self) -> None:
        self.declare()
        path = self.root / self.edition_path / "artifacts/body/artifact.toml"
        path.write_text(path.read_text().replace('rights_status = "public-domain"', 'rights_status = "unknown"'))
        self.assertIn("may not be published", " ".join(self.errors()))

    def test_unknown_with_false_author_is_still_refused(self) -> None:
        self.declare()
        path = self.root / self.work_path
        path.write_text(path.read_text().replace('responsible = "Augustine of Hippo"', 'responsible = "Someone Else"'))
        self.assertIn("two identity spaces disagree", " ".join(self.errors()))

    def test_unknown_with_false_translation_credit_is_still_refused(self) -> None:
        self.declare()
        path = self.root / self.edition_path / "edition.toml"
        path.write_text(path.read_text().replace('translators = ["Marcus Dods"]', "translators = []"))
        self.assertIn("names no translator", " ".join(self.errors()))

    def test_unknown_does_not_relax_canonical_numbering_or_extent(self) -> None:
        self.declare(numbering="hebrew")
        self.assertIn("not 'vulgate'", " ".join(self.errors()))
        self.declare(extent={
            "token": "Gen", "first_chapter": 1, "first_verse": 3,
            "last_chapter": 1, "last_verse": 100,
        })
        self.assertTrue(self.errors())

    def test_segment_controlled_unknown_uses_exact_borrowed_rights(self) -> None:
        self.declare()
        self.write("src/sources/works/npnf/container/editions/printing/artifacts/body/artifact.toml", '''
            schema = 2
            record_type = "artifact"
            id = "artifact.npnf.container.body"
            edition_id = "edition.npnf.container.printing"
            rights_status = "public-domain"
            rights_basis = "The exact printing's recorded basis."
        ''')
        self.write(self.edition_path + "segments/constituent.toml", '''
            schema = 2
            record_type = "segment"
            id = "segment.augustine.de-civitate-dei.dods-1871.constituent"
            edition_id = "edition.augustine.de-civitate-dei.dods-1871"
            artifact_id = "artifact.npnf.container.body"
        ''')
        self.change_passage(
            'artifact_id = "artifact.augustine.de-civitate-dei.dods-1871.body"',
            'segment_id = "segment.augustine.de-civitate-dei.dods-1871.constituent"',
        )
        self.assertEqual(self.errors(), [])
        row = _catena.fragments_for_book(self.root, "Gen")[0]
        self.assertIsNone(row["date"])
        self.assertEqual(row["rights"], "public-domain")
        path = self.root / "src/sources/works/npnf/container/editions/printing/artifacts/body/artifact.toml"
        path.write_text(path.read_text().replace('rights_status = "public-domain"', 'rights_status = "unknown"'))
        self.assertIn("may not be published", " ".join(self.errors()))


if __name__ == "__main__":
    unittest.main()
