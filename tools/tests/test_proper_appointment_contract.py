"""Source-owned appointment coordinates, overrides and shared CLI execution."""
from __future__ import annotations

import argparse
import copy
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
MODULE_ROOT = Path(os.environ.get("TRIPTYCH_APPOINTMENT_MODULE_ROOT", ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(MODULE_ROOT / "scripts"))
import _calendars as C


def tool(name):
    loader = importlib.machinery.SourceFileLoader("_contract_" + name.replace("-", "_"), str(MODULE_ROOT / "tools" / name))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    loader.exec_module(mod)
    for key, value in list(vars(mod).items()):
        if isinstance(value, Path) and value.is_relative_to(MODULE_ROOT):
            setattr(mod, key, ROOT / value.relative_to(MODULE_ROOT))
    mod.ROOT = ROOT
    return mod


MP = tool("mass-propers")
CHECK = tool("check-calendar-masses")
TODAY = tool("mass-today")
TODAY.SEATING_MODEL = Path(os.environ.get("TRIPTYCH_APPOINTMENT_SEATING", ROOT / "src/web/browser/liturgy/ordinary-seating.js"))
SOURCE = C.load_document(ROOT / "src/sources/calendars", "roman-1962", effective=False)
FACTS = {"fixture-season": {"edition": "roman-1962", "values": ["paschal", "outside"], "season_values": {"eastertide": "paschal", "advent": "outside", "lent": "outside", "unsettled": None}, "basis": "Technical fixture: explicit source enum transport, without a calendar calculation."}}
COMMON = "commune-virginum-4"
ANCHOR = {"mass": COMMON, "form_id": "main", "proper": "Gospel", "occurrence": 1}


def fixture():
    source = copy.deepcopy(SOURCE)
    source.setdefault("proper_appointment_facts", {}).update(copy.deepcopy(FACTS))
    mass = C.mass_index(source)[COMMON]
    for proper in mass["propers"]:
        proper.pop("ordinary_disposition", None)
        if proper["name"] in ("Gospel", "Gospel (vel)"):
            proper["ordinary_disposition"] = {"kind": "alternative", "group": "gospel", "option": "principal" if proper["name"] == "Gospel" else "other", "anchor": dict(ANCHOR), "basis": "The held Common prints these two explicit Gospel alternatives."}
        if proper["name"] == "Gradual":
            proper["ordinary_disposition"] = {"kind": "conditional", "group": "fixture-gradual", "basis": FACTS["fixture-season"]["basis"], "when": {"fact": "fixture-season", "in": ["outside"]}}
    return source, mass


class ShapeTests(unittest.TestCase):
    def test_fact_and_disposition_shapes_are_closed(self):
        source, mass = fixture()
        self.assertEqual(C.validate_proper_appointment_facts(FACTS, "roman-1962"), FACTS)
        for proper in mass["propers"]:
            if "ordinary_disposition" in proper:
                value = proper["ordinary_disposition"]
                self.assertEqual(MP.public_ordinary_disposition(value), value)
        for facts in ({}, {"bad": {**FACTS["fixture-season"], "edition": "other"}}, {"bad": {**FACTS["fixture-season"], "values": ["paschal", "paschal"]}}, {"bad": {**FACTS["fixture-season"], "season_values": {"lent": "unknown"}}}):
            with self.subTest(facts=facts), self.assertRaises(ValueError):
                C.validate_proper_appointment_facts(facts, "roman-1962")
        good = mass["propers"][3]["ordinary_disposition"]
        for value in ({**good, "anchor": ANCHOR}, {**good, "option": "other"}, {**good, "when": {"fact": "fixture-season", "in": []}}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                C.validate_ordinary_disposition(value)

    def test_handauthored_identity_and_unknown_fact_are_refused(self):
        source, mass = fixture()
        mass["propers"][0]["appointment_identity"] = ANCHOR
        self.assertTrue(C.resolve_propers(source, mass)[1])
        del mass["propers"][0]["appointment_identity"]
        mass["propers"][3]["ordinary_disposition"]["when"]["fact"] = "unknown"
        self.assertTrue(C.resolve_propers(source, mass)[1])
        problems = []
        CHECK.check_proper("fixture", {"name": "Gospel", "source": "composed", "text": "technical fixture", "appointment_identity": ANCHOR}, problems)
        self.assertTrue(any("unrecognised" in problem for problem in problems))


class ResolverTests(unittest.TestCase):
    def test_wrapper_identity_and_terminal_wording_owner_stay_distinct(self):
        source, mass = fixture()
        entries, problems = C.resolve_propers(source, mass, appointments=True)
        self.assertEqual(problems, [])
        gospel = next((proper, provenance) for _, proper, provenance in entries if proper["name"] == "Gospel")
        self.assertEqual(gospel[0]["appointment_identity"], ANCHOR)
        self.assertEqual(gospel[1]["mass"], "commune-non-virginum-1")
        self.assertEqual(MP.source_slot_identity(source, mass, "", gospel[0], gospel[1])[:3], ("commune-non-virginum-1", "main", "Gospel"))
        self.assertNotIn("appointment_identity", entries[0][1])
        self.assertNotIn("appointment_identity", mass["propers"][7])
        default, problems = C.resolve_propers(source, mass)
        self.assertEqual(problems, [])
        self.assertNotIn("appointment_identity", default[7][1])
        self.assertIs(default[0][1], mass["propers"][0])

    def test_nonadjacent_anchor_is_valid_but_legacy_run_stays_strict(self):
        source, mass = fixture()
        later = mass["propers"].pop(8)
        mass["propers"].append(later)
        self.assertEqual(C.resolve_propers(source, mass)[1], [])
        for proper in mass["propers"]:
            if proper.get("ordinary_disposition", {}).get("kind") == "alternative":
                del proper["ordinary_disposition"]["anchor"]
        self.assertTrue(any("contiguous" in problem for problem in C.resolve_propers(source, mass)[1]))

    def test_explicit_replacement_removes_exact_group_at_anchor_and_keeps_local_owner(self):
        source, common = fixture()
        local_coord = {"mass": "fixture-own-gospel", "form_id": "main", "proper": "Gospel", "occurrence": 1}
        local = {"key": "fixture-own-gospel", "propers": [{"name": "Gospel", "takes_from": {"mass": "commune-virginum-3", "proper": "Gospel"}}], "takes_from": {"mass": COMMON, "appointment_overrides": [{"mass": COMMON, "form_id": "main", "group": "gospel", "state": "replaced", "by": [local_coord], "basis": "Technical fixture exercises an exact own-appointment replacement."}]}}
        source["sections"]["sanctoral"]["masses"].append(local)
        entries, problems = C.resolve_propers(source, local, appointments=True)
        self.assertEqual(problems, [])
        self.assertEqual([p["name"] for _, p, _ in entries][7:9], ["Gospel", "Offertory"])
        proper, provenance = entries[7][1:]
        self.assertEqual(proper["appointment_identity"], local_coord)
        self.assertEqual(proper["appointment_replacement"]["anchor"], ANCHOR)
        self.assertEqual(proper["appointment_replacement"]["source_group"], {"mass": COMMON, "form_id": "main", "id": "gospel"})
        self.assertNotIn("ordinary_disposition", proper)
        self.assertEqual(provenance["mass"], "commune-virginum-3")
        self.assertEqual(provenance["proper"], "Gospel")
        del local["takes_from"]["appointment_overrides"]
        self.assertTrue(any("collides" in problem for problem in C.resolve_propers(source, local)[1]))

    def test_bad_anchor_and_override_coordinate_refuse(self):
        source, mass = fixture()
        for proper in mass["propers"]:
            if proper.get("ordinary_disposition", {}).get("kind") == "alternative":
                proper["ordinary_disposition"]["anchor"]["occurrence"] = 2
        self.assertTrue(any("anchor" in problem for problem in C.resolve_propers(source, mass)[1]))
        with self.assertRaises(ValueError):
            C.validate_appointment_coordinate({**ANCHOR, "occurrence": True})
        problems = []
        CHECK.check_reference("fixture", {"mass": COMMON, "appointment_overrides": []}, problems, on_proper=True)
        self.assertTrue(problems)

    def test_single_conditional_group_replacement_does_not_inherit_old_condition(self):
        source, common = fixture()
        coordinate = {"mass": "fixture-own-gradual", "form_id": "main", "proper": "Gradual", "occurrence": 1}
        local = {"key": "fixture-own-gradual", "propers": [{"name": "Gradual", "takes_from": {"mass": "commune-doctorum-pontificis", "proper": "Gradual"}}], "takes_from": {"mass": COMMON, "appointment_overrides": [{"mass": COMMON, "form_id": "main", "group": "fixture-gradual", "state": "replaced", "by": [coordinate], "basis": "Technical exact-coordinate replacement fixture."}]}}
        source["sections"]["sanctoral"]["masses"].append(local)
        entries, problems = C.resolve_propers(source, local, appointments=True)
        self.assertEqual(problems, [])
        proper, provenance = entries[3][1:]
        self.assertEqual(proper["appointment_identity"], coordinate)
        self.assertEqual(proper["appointment_replacement"]["anchor"]["proper"], "Gradual")
        self.assertNotIn("ordinary_disposition", proper)
        self.assertEqual(provenance["mass"], "commune-doctorum-pontificis")

    def test_single_proper_wording_reference_does_not_inherit_target_applicability(self):
        source, common = fixture()
        local = {"key": "fixture-wording-only", "propers": [{"name": "Gradual", "takes_from": {"mass": COMMON, "proper": "Gradual"}}]}
        source["sections"]["sanctoral"]["masses"].append(local)
        entries, problems = C.resolve_propers(source, local, appointments=True)
        self.assertEqual(problems, [])
        proper, provenance = entries[0][1:]
        self.assertNotIn("ordinary_disposition", proper)
        self.assertNotIn("appointment_identity", proper)
        self.assertEqual(provenance["mass"], COMMON)
        self.assertEqual(MP.source_slot_identity(source, local, "", proper, provenance), (COMMON, "main", "Gradual", 1))


class ProducerAndCliTests(unittest.TestCase):
    def test_show_and_daily_transport_preserve_source_facts_and_origin_identity(self):
        source, mass = fixture()
        arguments = argparse.Namespace(root=str(ROOT / "src/sources/calendars"), calendar="roman-1962", mass=COMMON, lang="la", witness=None, bible=None, bible_root=str(ROOT / "src/sources/bibles"), form=None)
        payload = {"calendar": "roman-1962", "edition": source["edition"], "psalm_numbering": "vulgate", "kind": "common", "mass": mass, "_document": source}
        with patch.object(MP, "find_mass", return_value=payload), patch.object(MP, "translation_overlay", return_value=({}, {}, [], {})), patch.object(MP, "publication_records", return_value=({}, [])):
            shown = MP.run_show_one(arguments)
        self.assertEqual(shown["proper_appointment_facts"], source["proper_appointment_facts"])
        daily = TODAY.propers_of("roman-1962", COMMON, arguments, payload=shown)
        self.assertEqual(daily["proper_appointment_facts"], source["proper_appointment_facts"])
        self.assertEqual(daily["propers"][7]["appointment_identity"], ANCHOR)
        self.assertEqual(daily["_proper_source_indices"], list(range(len(daily["propers"]))))
        self.assertEqual(len(daily["propers"]), len(shown["appointed"]))

    def test_producer_exposes_only_needed_exact_coordinates_and_facts(self):
        source, mass = fixture()
        source.pop("citation_divergences", None)
        # The producer is exercised in memory, never by structure generation.
        selected = copy.deepcopy(source)
        selected["sections"] = {"common": {"kind": "common", "masses": [mass]}}
        # Keep reference owners available to the resolver, but do not emit their
        # whole production catalogue in this focused producer fixture.
        with patch.object(MP, "load_calendar", return_value=source), patch.object(MP, "masses_of", return_value=[("common", mass)]), patch.object(MP, "translation_overlay", return_value=({}, {}, [], {})), patch.object(MP, "publication_records", return_value=({}, [])), patch.object(MP._oration_execution, "load_sources", return_value={}), patch.object(MP._name_execution, "load_name_sources", return_value={}):
            structure = MP.calendar_structure(ROOT / "src/sources/calendars", "roman-1962", MP.book_tokens())
        self.assertEqual(structure["proper_appointment_facts"], source["proper_appointment_facts"])
        rows = structure["masses"][0]["propers"]
        self.assertEqual(sum("appointment_identity" in row for row in rows), 3)
        self.assertEqual(rows[7]["appointment_identity"], ANCHOR)
        self.assertEqual(rows[7]["taken_from"]["mass"], "commune-non-virginum-1")
        encoded = json.dumps(structure)
        for private in ("_appointment_identity", "_appointment_replacement", "source_proper"):
            self.assertNotIn(json.dumps(private) + ":", encoded)

    def test_cli_uses_shared_fact_evaluation_and_retains_original_indices(self):
        source, mass = fixture()
        entries, problems = C.resolve_propers(source, mass, appointments=True)
        self.assertEqual(problems, [])
        rows = [{"proper": {**proper, "form_id": "main"}, "sourceIndex": i + 20} for i, (_, proper, _) in enumerate(entries)]
        snapshot = copy.deepcopy(rows)
        context = {"calendar": "roman-1962", "entrance": "day", "date": "2026-04-08", "season": "eastertide", "facts": FACTS, "choices": {"main/gospel": "principal"}}
        result = TODAY.mass_events(None, rows, None, {}, context)
        self.assertEqual(rows, snapshot)
        self.assertEqual(result["proper_appointment_selections"]["main/gospel"], {"state": "selected", "option": "principal"})
        self.assertEqual(result["proper_appointment_inactive"][0]["sourceIndex"], 23)
        choice = next(event for event in result["events"] if event["kind"] == "proper_choice")
        self.assertEqual(choice["sourceIndex"], 27)
        self.assertEqual(choice["selection"]["option"], "principal")
        context["season"] = None
        unknown = TODAY.mass_events(None, rows, None, {}, context)
        self.assertEqual(unknown["proper_appointment_unresolved"][0]["sourceIndex"], 23)

    def test_cli_exact_qualified_selector_refuses_wrong_axes_and_duplicates(self):
        mass = {"key": "fixture-mass"}
        valid = "proper-choice/roman-1962/fixture-mass/main/gospel=principal"
        self.assertEqual(TODAY.proper_appointment_context_for("roman-1962", mass, {}, [valid])["choices"], {"main/gospel": "principal"})
        for values in ([valid, valid], [valid.replace("roman-1962", "postconciliar")], [valid.replace("fixture-mass", "other")], ["gospel=principal"]):
            with self.subTest(values=values), self.assertRaises(TODAY.Refused):
                TODAY.proper_appointment_context_for("roman-1962", mass, {}, values)

    def test_cli_shared_replacement_seat_guard_refuses_mismatch(self):
        proper = {"name": "Collect", "source": "composed", "text_status": {"state": "unavailable", "scope": "proper-body"}, "form_id": "main", "appointment_identity": {"mass": "fixture-own", "form_id": "main", "proper": "Collect", "occurrence": 1}, "appointment_replacement": {"source_group": {"mass": COMMON, "form_id": "main", "id": "gospel"}, "anchor": ANCHOR, "basis": "Technical negative fixture: a different functional seat is not a permitted group replacement."}}
        with self.assertRaises(TODAY.Refused):
            TODAY.mass_events(None, [{"proper": proper, "sourceIndex": 7}], None, {}, {"calendar": "roman-1962", "entrance": "day", "facts": {}, "choices": {}})

    def test_mixed_owned_body_or_gap_is_never_masked_by_Bible_components(self):
        verses = [{"ref": "Psalms 4:8", "text": "Technical Bible-component fixture."}]
        mixed = {"source": "mixed", "verses": verses, "text_status": {"state": "unavailable", "scope": "proper-body"}}
        bible = {"id": "fixture-bible", "language": "la"}
        unavailable = TODAY.language_projection(mixed, "la", bible)
        self.assertEqual(unavailable["status"], "unavailable")
        self.assertNotIn("delegated_to", unavailable)
        held = {"source": "mixed", "verses": verses, "text": "Technical owned-body fixture."}
        selected = TODAY.language_projection(held, "la", bible)
        self.assertEqual(selected["status"], "full-text")
        self.assertEqual(selected["texts"][0]["text"], held["text"])
        pure = TODAY.language_projection({"source": "scripture", "verses": verses}, "la", bible)
        self.assertEqual(pure["status"], "scripture-delegated")


class RecensionBoundaryTests(unittest.TestCase):
    def test_foreign_season_rules_are_not_inherited_but_legacy_rows_and_words_are(self):
        source, common = fixture()
        legacy = {"key": "fixture-legacy", "propers": [{"name": "Gospel", "source": "scripture", "verses": [], "ordinary_disposition": {"kind": "alternative", "group": "legacy", "option": "one", "basis": "Technical legacy fixture"}}, {"name": "Gospel (vel)", "source": "scripture", "verses": [], "ordinary_disposition": {"kind": "alternative", "group": "legacy", "option": "two", "basis": "Technical legacy fixture"}}]}
        base = {"calendar": "roman-1962", "proper_appointment_facts": FACTS, "sections": {"common": {"kind": "common", "masses": [common, legacy]}}}
        before = copy.deepcopy(base)
        target = {"calendar": "roman-pre-1955", "sections": {}}
        merged = C._apply_departures(target, base, "roman-1962")
        self.assertEqual(base, before)
        self.assertNotIn("proper_appointment_facts", merged)
        inherited = C.mass_index(merged)
        self.assertEqual(len(inherited[COMMON]["propers"]), len(common["propers"]))
        for original, projected in zip(common["propers"], inherited[COMMON]["propers"]):
            self.assertEqual({k: v for k, v in original.items() if k != "ordinary_disposition"}, {k: v for k, v in projected.items() if k != "ordinary_disposition"})
            if C._new_appointment(original):
                self.assertEqual(getattr(projected, "appointment_applicability")["state"], "unresolved")
                self.assertEqual(getattr(projected, "appointment_applicability")["source_edition"], "roman-1962")
                if original["ordinary_disposition"]["kind"] == "conditional":
                    self.assertNotIn("ordinary_disposition", projected)
                else:
                    self.assertEqual(set(projected["ordinary_disposition"]), {"kind", "group", "option", "basis"})
        self.assertEqual(inherited[legacy["key"]]["propers"], legacy["propers"])
        own = copy.deepcopy(common)
        own["departure"] = "replaced"
        own["departure_basis"] = "Technical independent target-authored appointment fixture"
        target["proper_appointment_facts"] = {key: dict(value, edition="roman-pre-1955") for key, value in FACTS.items()}
        target["sections"] = {"common": {"kind": "common", "masses": [own]}}
        independently_authored = C._apply_departures(target, base, "roman-1962")
        self.assertEqual(C.mass_index(independently_authored)[COMMON]["propers"], own["propers"])
        self.assertEqual(independently_authored["proper_appointment_facts"], target["proper_appointment_facts"])


if __name__ == "__main__":
    unittest.main()
