"""Fail-closed invariants for the Pustet/1962 Roman Common collation."""

from __future__ import annotations

import copy
import hashlib
import tomllib
import unittest
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
CALENDAR = ROOT / "src/sources/calendars/roman-1962/propers.yaml"
COLLATION = (
    ROOT
    / "src/sources/inventories/roman-1962-pustet-common-collation-v1.toml"
)
SIDECAR = (
    ROOT
    / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml"
)
SOURCE_ROOT = ROOT / "src/sources/works"

EXACT_OUTCOME = "collated-exact-after-mechanical-normalization"
NONEXACT_OUTCOME = "collated-non-exact"
KEY_FIELDS = ("mass", "form", "proper", "course", "cycle", "occurrence")
TARGET_EDITION_ID = "edition.catholic-church.missale-romanum.vatican-typica-1962"
UNAVAILABLE_STATUS = {
    "state": "unavailable",
    "scope": "proper-body",
    "reasons": [{"kind": "rights-withheld", "source_id": TARGET_EDITION_ID}],
}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def live_propers() -> dict[tuple[object, ...], dict]:
    document = yaml.safe_load(CALENDAR.read_text(encoding="utf-8"))
    rows: dict[tuple[object, ...], dict] = {}
    for section in document["sections"].values():
        for mass in section.get("masses") or []:
            occurrences: Counter[tuple[str, str, str, str]] = Counter()
            for proper in mass.get("propers") or []:
                partial = (
                    "",
                    str(proper["name"]),
                    str(proper.get("course") or ""),
                    str(proper.get("cycle") or ""),
                )
                occurrences[partial] += 1
                key = (
                    str(mass["key"]),
                    *partial,
                    occurrences[partial],
                )
                rows[key] = proper
    return rows


def source_ids() -> set[str]:
    ids: set[str] = set()
    for path in SOURCE_ROOT.rglob("*.toml"):
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError:
            continue
        record_id = data.get("id")
        if isinstance(record_id, str):
            ids.add(record_id)
    return ids


def comparison_preimage(row: dict) -> str:
    values = [
        str(row[field])
        for field in (*KEY_FIELDS, "target_text_sha256", "verification_text_sha256", "outcome")
    ]
    return "\t".join(values) + "\n"


def inventory_errors(
    record: dict,
    registered_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    rows = record.get("comparisons") or []
    keys = [tuple(row.get(field) for field in KEY_FIELDS) for row in rows]
    if len(rows) != 17:
        errors.append(f"expected 17 comparisons, got {len(rows)}")
    if len(set(keys)) != len(keys):
        errors.append("comparison identities are not unique")
    outcomes = Counter(row.get("outcome") for row in rows)
    if outcomes != Counter({NONEXACT_OUTCOME: 16, EXACT_OUTCOME: 1}):
        errors.append(f"unexpected outcomes: {outcomes}")

    for field in ("target_artifact_id", "verification_edition_id"):
        if record.get(field) not in registered_ids:
            errors.append(f"unregistered {field}")

    for key, row in zip(keys, rows, strict=True):
        label = f"{key[0]}/{key[2]}"
        if digest(comparison_preimage(row)) != row.get("comparison_sha256"):
            errors.append(f"{label}: stale comparison_sha256")
        if row.get("target_passage_id") not in registered_ids:
            errors.append(f"{label}: unregistered target_passage_id")
        for field in ("verification_source_ids", "verification_passage_ids"):
            source_ids = row.get(field) or []
            if not source_ids:
                errors.append(f"{label}: empty {field}")
            for source_id in source_ids:
                if source_id not in registered_ids:
                    errors.append(f"{label}: unregistered {field} member")
        if row.get("provenance_disposition") != "collated":
            errors.append(f"{label}: provenance is not collated")
        if row.get("outcome") == EXACT_OUTCOME:
            required = {"strip-stress-accents", "expand-print-ligatures", "join-line-breaks"}
            if not required <= set(row.get("transformations") or []):
                errors.append(f"{label}: exact row omits mechanical transformations")
            if row.get("target_text_sha256") != row.get("verification_text_sha256"):
                errors.append(f"{label}: exact row hashes differ")
            verification_text = row.get("verification_text")
            if not isinstance(verification_text, str):
                errors.append(f"{label}: exact row lacks verification_text")
            elif digest(verification_text) != row.get("verification_text_sha256"):
                errors.append(f"{label}: stale verification_text_sha256")
            if row.get("differences"):
                errors.append(f"{label}: exact row records substantive differences")
            if row.get("publication_disposition") != "unresolved":
                errors.append(f"{label}: exact row publication is not unresolved")
            if row.get("publication_basis") != "unresolved":
                errors.append(f"{label}: exact row basis is not unresolved")
        else:
            if row.get("target_text_sha256") == row.get("verification_text_sha256"):
                errors.append(f"{label}: non-exact row hashes agree")
            if not row.get("differences"):
                errors.append(f"{label}: non-exact row lacks a difference")
            if row.get("publication_disposition") != "withheld":
                errors.append(f"{label}: non-exact row is not withheld")
            if row.get("publication_basis") != "non-exact-historical-witness":
                errors.append(f"{label}: non-exact row has the wrong basis")
    return errors


def sidecar_errors(
    record: dict,
    sidecar: dict,
    registered_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    defaults = sidecar.get("defaults") or {}
    expected_defaults = {
        "provenance_status": "unresolved",
        "publication_status": "unresolved",
        "publication_basis": "unresolved",
        "surfaces": [],
    }
    if defaults != expected_defaults:
        errors.append(f"unexpected sidecar defaults: {defaults}")

    rows_by_key: dict[tuple[object, ...], list[dict]] = {}
    for row in sidecar.get("entries") or []:
        key = tuple(row.get(field) for field in KEY_FIELDS)
        rows_by_key.setdefault(key, []).append(row)

    for comparison in record.get("comparisons") or []:
        key = tuple(comparison.get(field) for field in KEY_FIELDS)
        label = f"{key[0]}/{key[2]}"
        matches = rows_by_key.get(key, [])
        if len(matches) != 1:
            errors.append(f"{label}: expected one sidecar row, got {len(matches)}")
            continue
        row = matches[0]
        # SUPERSEDED 2026-09-03. The sidecar rows for these seventeen were
        # rewritten when the bodies were published on the 1922 Mame, so they no
        # longer carry this record's own body_status, relationship, source ids
        # or comparison hash -- they carry the projection's. That is the change,
        # not a defect. What this record asserts about the PUSTET is unaffected
        # and is still checked: its own hashes, loci and outcomes, above.
        if record.get("superseded_on"):
            publication = row.get("publication_status", defaults.get("publication_status"))
            basis = row.get("publication_basis", defaults.get("publication_basis"))
            surfaces = row.get("surfaces", defaults.get("surfaces"))
            if publication != "permitted":
                errors.append(f"{label}: sidecar publication is not permitted")
            if basis != "public-domain":
                errors.append(f"{label}: sidecar publication basis is not public-domain")
            if not surfaces:
                errors.append(f"{label}: sidecar has no serving surfaces")
            continue

        if row.get("text_sha256") != comparison.get("target_text_sha256"):
            errors.append(f"{label}: sidecar target hash differs")
        if row.get("body_status") != "removed":
            errors.append(f"{label}: sidecar body is not removed")
        if row.get("provenance_status", defaults.get("provenance_status")) != "collated":
            errors.append(f"{label}: sidecar provenance is not collated")
        if row.get("relationship") != comparison.get("outcome"):
            errors.append(f"{label}: sidecar relationship differs")
        if row.get("source_id") != record.get("target_artifact_id"):
            errors.append(f"{label}: sidecar target source differs")
        if row.get("source_id") not in registered_ids:
            errors.append(f"{label}: unregistered sidecar source_id")
        verification_source_id = row.get("verification_source_id")
        if verification_source_id not in (
            comparison.get("verification_passage_ids") or []
        ):
            errors.append(f"{label}: sidecar verification source differs")
        if verification_source_id not in registered_ids:
            errors.append(f"{label}: unregistered sidecar verification_source_id")
        evidence = (
            "src/sources/inventories/"
            "roman-1962-pustet-common-collation-v1.toml "
            f"comparison_sha256={comparison.get('comparison_sha256')}"
        )
        if row.get("provenance_evidence") != evidence:
            errors.append(f"{label}: sidecar comparison hash differs")

        publication = row.get(
            "publication_status", defaults.get("publication_status")
        )
        basis = row.get("publication_basis", defaults.get("publication_basis"))
        surfaces = row.get("surfaces", defaults.get("surfaces"))
        # SUPERSEDED 2026-09-03. These seventeen are published, on the 1922
        # Mame, under the rule that a witness must carry the same WORDS and not
        # the same string -- see guidance/propers-for-agents.md, "A
        # transformation changes how a word is spelled; a variant changes which
        # word is said". This record's findings about the PUSTET stand unaltered
        # and are still checked above: its hashes, its loci and its outcomes.
        # What is no longer asserted is that a non-exact Pustet page keeps a body
        # off every surface, because the repository publishes its own declared
        # orthography and has never served an exact 1962 string anywhere.
        if publication != "permitted":
            errors.append(f"{label}: sidecar publication is not permitted")
        if basis != "public-domain":
            errors.append(f"{label}: sidecar publication basis is not public-domain")
        if not surfaces:
            errors.append(f"{label}: sidecar has no serving surfaces")
    return errors


def calendar_errors(
    record: dict,
    propers: dict[tuple[object, ...], dict],
    registered_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    for comparison in record.get("comparisons") or []:
        key = tuple(comparison.get(field) for field in KEY_FIELDS)
        label = f"{key[0]}/{key[2]}"
        proper = propers.get(key)
        if proper is None:
            errors.append(f"{label}: no live proper identity")
            continue
        # Superseded with the sidecar checks above: each of the seventeen now
        # carries its body rather than a rights-withheld status.
        if "text" not in proper:
            errors.append(f"{label}: published body is absent")
        if "takes_from" in proper:
            errors.append(f"{label}: published body is inherited")
        if proper.get("text_status") is not None:
            errors.append(f"{label}: a published body still carries a text_status")
    return errors


def collation_errors(
    record: dict,
    propers: dict[tuple[object, ...], dict],
    sidecar: dict,
    registered_ids: set[str],
) -> list[str]:
    return [
        *inventory_errors(record, registered_ids),
        *sidecar_errors(record, sidecar, registered_ids),
        *calendar_errors(record, propers, registered_ids),
    ]


class RomanPustetCommonCollationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record = tomllib.loads(COLLATION.read_text(encoding="utf-8"))
        cls.propers = live_propers()
        cls.registered = source_ids()
        cls.sidecar = tomllib.loads(SIDECAR.read_text(encoding="utf-8"))

    def test_seventeen_rows_are_hash_bound_registered_and_served(self) -> None:
        self.assertEqual(
            collation_errors(
                self.record,
                self.propers,
                self.sidecar,
                self.registered,
            ),
            [],
        )

    def test_inventory_target_hash_mutation_breaks_both_links(self) -> None:
        record = copy.deepcopy(self.record)
        exact = next(
            row for row in record["comparisons"] if row["outcome"] == EXACT_OUTCOME
        )
        exact["target_text_sha256"] = "0" * 64
        errors = collation_errors(
            record,
            self.propers,
            self.sidecar,
            self.registered,
        )
        self.assertIn(
            "missa-de-s-maria-in-sabbato-2/Communion: stale comparison_sha256",
            errors,
        )
        # The sidecar arm of this pair went when the seventeen were published:
        # see the supersession gate in sidecar_errors. What a mutation of the
        # record's own target hash still breaks is the record's internal
        # consistency, which is the half this file can still speak for.
        self.assertIn(
            "missa-de-s-maria-in-sabbato-2/Communion: exact row hashes differ",
            errors,
        )

    def test_the_sidecar_link_is_deliberately_no_longer_asserted(self) -> None:
        """Superseded 2026-09-03, and recorded rather than quietly dropped.

        This record bound each of the seventeen to a sidecar row carrying its
        own hash, relationship and source ids. When the bodies were published on
        the 1922 Mame those rows became projection rows, so the binding is gone
        by design, and a mutation of a sidecar hash is no longer this record's
        to detect. What the record still says about the PUSTET -- its own
        hashes, loci and outcomes -- is unchanged and still checked.
        """
        self.assertTrue(self.record.get("superseded_on"))
        self.assertIn(
            "transformation changes how a word is spelled",
            self.record.get("superseded_by", ""),
        )
        sidecar = copy.deepcopy(self.sidecar)
        row = next(
            row
            for row in sidecar["entries"]
            if (row["mass"], row["proper"])
            == ("missa-de-s-maria-in-sabbato-2", "Communion")
        )
        row["text_sha256"] = "0" * 64
        self.assertEqual([], sidecar_errors(self.record, sidecar, self.registered))

    def test_exact_verification_text_mutation_is_detected(self) -> None:
        record = copy.deepcopy(self.record)
        exact = next(
            row for row in record["comparisons"] if row["outcome"] == EXACT_OUTCOME
        )
        exact["verification_text"] = exact["verification_text"].replace(
            "aeterni", "sempiterni"
        )
        errors = inventory_errors(record, self.registered)
        self.assertIn(
            "missa-de-s-maria-in-sabbato-2/Communion: stale verification_text_sha256",
            errors,
        )

    def test_exact_row_uses_only_lossless_mechanical_normalization(self) -> None:
        exact = [
            row for row in self.record["comparisons"] if row["outcome"] == EXACT_OUTCOME
        ]
        self.assertEqual(len(exact), 1)
        row = exact[0]
        self.assertEqual(
            (row["mass"], row["proper"]),
            ("missa-de-s-maria-in-sabbato-2", "Communion"),
        )
        self.assertEqual(
            row["transformations"],
            ["strip-stress-accents", "expand-print-ligatures", "join-line-breaks"],
        )
        self.assertEqual(digest(row["verification_text"]), row["verification_text_sha256"])
        self.assertEqual(row["verification_text_sha256"], row["target_text_sha256"])
        self.assertEqual(row["differences"], [])


if __name__ == "__main__":
    unittest.main()
