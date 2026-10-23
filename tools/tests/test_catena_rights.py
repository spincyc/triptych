"""Required source-controller notices travel beside licensed commentary words."""
from __future__ import annotations

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
NOTICE = (
    "  Augustine of Hippo; transcription by the named source contributors. "
    "CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/. "
    "Changes: wiki markup removed; Latin spellings retained.\n"
)


class RequiredCommentaryNoticeTests(CatenaFixture):
    passage_id = "passage.augustine.de-civitate-dei.dods-1871.11.7"
    work_id = "work.augustine.de-civitate-dei"
    edition = "src/sources/works/augustine/de-civitate-dei/editions/dods-1871/"
    artifact_id = "artifact.augustine.de-civitate-dei.dods-1871.body"

    def artifact(self, *, status: str = "licensed", licence: str = "CC-BY-SA-4.0",
                 notice: object = NOTICE, omit_notice: bool = False) -> None:
        data = (
            'schema = 1\nrecord_type = "artifact"\n'
            f'id = "{self.artifact_id}"\n'
            'edition_id = "edition.augustine.de-civitate-dei.dods-1871"\n'
            f'rights_status = {json.dumps(status)}\nlicense = {json.dumps(licence)}\n'
        )
        if not omit_notice:
            data += "rights_basis = " + json.dumps(notice, ensure_ascii=False) + "\n"
        self.write(self.edition + "artifacts/body/artifact.toml", data)
        _catena._SOURCES_CACHE.pop(self.root, None)

    def row(self) -> dict:
        return _catena.fragments_for_book(self.root, "Gen")[0]

    def files(self) -> tuple[dict, dict]:
        self.write(str(_catena.MODEL_RELATIVE), (ROOT / _catena.MODEL_RELATIVE).read_text())
        directory, files, _ = _catena._structure_files(self.root, self.root / "out")
        payload = json.loads(files[directory / "text" / (self.passage_id + ".json")])
        index = json.loads(files[directory / "index.json"])
        folder = next(book["path"] for book in index["canon"] if book["token"] == "Gen")
        spine = json.loads(files[directory / folder / _catena._canon.chapter_name(
            1, index["chapter_digits"],
        )])
        return payload, spine

    def test_public_domain_words_and_metadata_gain_no_optional_notice(self) -> None:
        row = self.row()
        self.assertNotIn("acknowledgement", row)
        payload, spine = self.files()
        self.assertEqual(set(payload), {"id", "text", "basis", "date_basis"})
        self.assertNotIn("acknowledgement", json.dumps(spine))

    def test_licensed_notice_is_the_exact_controller_text(self) -> None:
        before = self.row()
        self.artifact()
        self.assertEqual(self.errors(), [])
        row = self.row()
        self.assertEqual(row.pop("acknowledgement"), NOTICE)
        before["rights"] = "licensed"
        self.assertEqual(row, before)

    def test_notice_travels_only_with_lazy_words_and_preserves_word_count(self) -> None:
        self.artifact()
        row = self.row()
        payload, spine = self.files()
        self.assertEqual(payload["acknowledgement"], NOTICE)
        self.assertEqual(payload["text"], row["text"])
        self.assertEqual(payload["basis"], row["basis"])
        self.assertNotIn(NOTICE, json.dumps(spine))
        self.assertEqual(spine["fragments"][0]["text_words"], len(row["text"].split()))

    def test_missing_notice_refuses_check_and_projection_without_fallback(self) -> None:
        self.artifact(omit_notice=True)
        self.assertIn("records no rights_basis", " ".join(self.errors()))
        with self.assertRaisesRegex(_catena.CatenaError, "required acknowledgement"):
            self.row()

    def test_empty_or_malformed_licensed_notice_is_never_coerced(self) -> None:
        for notice in ("", " \n\t ", 17, False, ["invented credit"]):
            with self.subTest(notice=notice):
                self.artifact(notice=notice)
                self.assertIn("records no rights_basis", " ".join(self.errors()))
                with self.assertRaises(_catena.CatenaError):
                    self.row()

    def test_optional_public_domain_basis_does_not_become_a_licence_notice(self) -> None:
        self.artifact(status="public-domain", notice=NOTICE)
        self.assertEqual(self.errors(), [])
        self.assertNotIn("acknowledgement", self.row())

    def test_restricted_licence_is_not_admitted_by_adding_a_notice(self) -> None:
        self.artifact(licence="CC-BY-NC-ND-4.0")
        self.assertIn("may not be published", " ".join(self.errors()))

    def test_protected_artifact_is_not_admitted_by_adding_a_notice(self) -> None:
        self.artifact(status="in-copyright")
        self.assertIn("may not be published", " ".join(self.errors()))

    def test_notice_does_not_replace_the_explicit_words_gate(self) -> None:
        self.artifact()
        path = self.root / self.edition / "passages/11.7.toml"
        path.write_text(path.read_text().replace(
            'text = "And first of all, indeed, light was made by the word of God."',
            'text = ""',
        ))
        _catena._SOURCES_CACHE.pop(self.root, None)
        self.assertIn("has no text", " ".join(self.errors()))

    def test_borrowed_segment_uses_its_controlling_container_notice(self) -> None:
        container_id = "artifact.npnf.container.body"
        segment_id = "segment.augustine.de-civitate-dei.dods-1871.constituent"
        self.write(
            "src/sources/works/npnf/container/editions/printing/artifacts/body/artifact.toml",
            'schema = 2\nrecord_type = "artifact"\n'
            f'id = "{container_id}"\n'
            'edition_id = "edition.npnf.container.printing"\n'
            'rights_status = "licensed"\nlicense = "CC-BY-SA-4.0"\n'
            "rights_basis = " + json.dumps(NOTICE) + "\n",
        )
        self.write(self.edition + "segments/constituent.toml",
                   'schema = 2\nrecord_type = "segment"\n'
                   f'id = "{segment_id}"\n'
                   'edition_id = "edition.augustine.de-civitate-dei.dods-1871"\n'
                   f'artifact_id = "{container_id}"\n')
        path = self.root / self.edition / "passages/11.7.toml"
        path.write_text(path.read_text().replace("schema = 1", "schema = 2").replace(
            f'artifact_id = "{self.artifact_id}"', f'segment_id = "{segment_id}"',
        ))
        _catena._SOURCES_CACHE.pop(self.root, None)
        self.assertEqual(self.errors(), [])
        self.assertEqual(self.row()["acknowledgement"], NOTICE)

    def test_notice_requirement_uses_the_source_reader_owned_statuses(self) -> None:
        owner = _catena._source_reader()
        self.assertIn("licensed", owner.ATTRIBUTION_REQUIRED)
        self.assertEqual(_catena._rights_notice({"rights_status": "licensed", "rights_basis": NOTICE}),
                         {"acknowledgement": NOTICE})


if __name__ == "__main__":
    unittest.main()
