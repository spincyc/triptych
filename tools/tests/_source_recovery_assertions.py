"""Exact current source-epoch assertions for historical regression tests.

The accepted source manifest chooses each current state. These helpers grant no
publication permission and never treat a body and an absence as interchangeable.
"""
from __future__ import annotations

import tomllib
from functools import lru_cache

from tools.tests import _source_batch_guards as source_batch


ENGLISH_LEDGER = "src/sources/inventories/roman-1962-proper-translations-v1.toml"


@lru_cache(maxsize=1)
def _current_latin_records():
    from _proper_latin import publication_records

    records, problems = publication_records(
        source_batch.ROOT / "src/sources/calendars", "roman-1962")
    source_batch.require(not problems, "current Latin publication records: " + str(problems))
    source_batch.assert_current_latin(records)
    return records


@lru_cache(maxsize=1)
def _current_roman_document():
    import _calendars

    document = _calendars.load_document(
        source_batch.ROOT / "src/sources/calendars", "roman-1962")
    source_batch.assert_live_baseline_bodies(document)
    return document


def assert_current_latin_body_or_gap(testcase, mass, proper, node, *, form="",
                                     occurrence=1):
    """Keep a reviewed exact body or the source's exact typed witness gap.

    The accepted fixture decides which state is required. A newly present body
    must reproduce its accepted hash and pass the real six-surface permission
    join; an absent owner never permits invented wording or a weaker gap.
    """
    from _proper_latin import LatinKey, SURFACES, decision_for, text_sha256

    key = LatinKey(mass, form, proper, "", "", occurrence)
    expected = source_batch.fixture()["latin_current_bodies"].get(
        source_batch.key_string(key))
    records = _current_latin_records()
    if expected is None:
        document = _current_roman_document()
        masses = [one for section in document["sections"].values()
                  for one in section.get("masses", []) if one["key"] == mass]
        testcase.assertEqual(1, len(masses), mass)
        groups = [{"name": "", "propers": masses[0].get("propers", [])}]
        groups += masses[0].get("forms", [])
        owners = [owner for group in groups if group.get("name", "") == form
                  for owner in group["propers"] if owner["name"] == proper]
        testcase.assertGreaterEqual(len(owners), occurrence, key)
        status = owners[occurrence - 1]["text_status"]
        testcase.assertEqual((status["state"], status["scope"]),
                             ("unavailable", "proper-body"))
        testcase.assertTrue(status["reasons"])
        testcase.assertNotIn(key, records)
        testcase.assertNotIn("text", node)
        testcase.assertIn("text_status", node)
        testcase.assertEqual(status, node["text_status"])
        return "unavailable"
    testcase.assertEqual("present", expected["state"], key)
    testcase.assertNotIn("text_status", node)
    testcase.assertIn("text", node)
    testcase.assertIsInstance(node["text"], str)
    testcase.assertEqual(expected["body_sha256"], text_sha256(node["text"]), key)
    testcase.assertTrue(decision_for(key, node["text"], records).permits(SURFACES), key)
    return "present"


def english_identity(row):
    return (row["mass"], row.get("form_id", "main"), row["proper"],
            row.get("cycle", "all"), row.get("occurrence", 1))


def _english_owners(ledger, key):
    return [(group, row) for group in ("entries", "untranslated")
            for row in ledger.get(group, []) if english_identity(row) == key
            and row.get("lang", "en") == "en" and row.get("extent", "body") == "body"]


@lru_cache(maxsize=1)
def _english_ledger_from_raw(raw):
    return tomllib.loads(raw.decode())


def assert_current_english_owner(testcase, key, ledger, propers, overlay,
                                 witnesses, *, latin_sha256=None,
                                 independent_oracles=()):
    """Require the one accepted current dictionary and its literal publication.

    Optional independent oracle groups contain ``(oracle-map, artifact-id, hash)``;
    their values begin with the Latin and English body hashes. A caller supplying
    them requires exactly one matching source oracle for each admitted body.
    """
    accepted = source_batch.fixture()
    raw = (source_batch.ROOT / ENGLISH_LEDGER).read_bytes()
    source_batch.require(source_batch.digest(raw) == accepted["files"][ENGLISH_LEDGER]["after_sha256"],
                         "entire accepted English ledger before state assertion")
    source_batch.assert_current_english_entries(overlay)
    expected = _english_owners(_english_ledger_from_raw(raw), key)
    testcase.assertEqual(1, len(expected), key)
    owned = _english_owners(ledger, key)
    testcase.assertEqual(expected, owned, key)
    group, entry = owned[0]
    if group == "entries":
        testcase.assertIn(key, overlay)
        if independent_oracles:
            matches = [(oracles[key], artifact, digest)
                       for oracles, artifact, digest in independent_oracles if key in oracles]
            testcase.assertEqual(1, len(matches), key)
            oracle, artifact, digest = matches[0]
            if latin_sha256 is not None:
                testcase.assertEqual(oracle[0], latin_sha256)
            testcase.assertEqual(artifact, entry["publication_artifact_id"])
            testcase.assertEqual(digest, entry["publication_artifact_sha256"])
            testcase.assertEqual(oracle[1], source_batch.digest(entry["translations"][0]["text"]))
        propers.validate_translation_publication_binding(
            entry, source_batch.ROOT / "src/sources/calendars",
            source_batch.ROOT / ENGLISH_LEDGER, witnesses)
    else:
        testcase.assertNotIn(key, overlay)
        testcase.assertEqual("unavailable", entry["availability"])
        testcase.assertTrue(entry["reason"]["kind"])
    return group, entry
