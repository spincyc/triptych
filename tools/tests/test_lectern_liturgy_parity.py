"""Terminal controls retain the production reader's semantic selections."""
from __future__ import annotations

import importlib.util
import asyncio
import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lectern import bridge  # noqa: E402
from lectern.repo import Refused  # noqa: E402


def words(blocks: list[dict]) -> str:
    return " ".join(run["text"] for block in blocks for run in block["runs"])


@unittest.skipUnless(shutil.which("node"), "the browser models require node")
class LiturgyParityTests(unittest.TestCase):
    def test_global_epiphany_choice_preserves_other_territory_and_share(self) -> None:
        selection = {"mass": "epiphany", "form": "vigil", "ordinary": True}
        rows = bridge.call("liturgy", "day", "postconciliar", "2027-01-03", selection)["rows"]
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(not row.get("failed") and row.get("events") for row in rows))
        self.assertEqual(sum(row["mass"]["key"] == "epiphany" for row in rows), 1)
        route = bridge.call("liturgy", "readerUrl", "day", "postconciliar", "2027-01-03", selection)
        self.assertIn("form=vigil", route)
        self.assertEqual(bridge.call("liturgy", "openReaderLink", "https://mystago.gy/" + route, "day")["intent"]["mass"], "epiphany")
        studied = bridge.call("liturgy", "studyDay", "postconciliar", "2027-01-03", selection)
        self.assertEqual(len(studied), len(rows))

    def test_territorial_headings_keep_the_explicit_displaced_reading_and_its_standing(self) -> None:
        view = bridge.call("liturgy", "day", "postconciliar", "2027-01-03", {"mass": "most-holy-name-jesus"})
        self.assertTrue(view["multiple"])
        for row in view["rows"]:
            self.assertEqual(row["heading"]["title"], row["mass"]["name"])
            self.assertEqual(row["resolved"]["standing"], "displaced")
            self.assertNotEqual(row["title"], row["branch"]["winner"]["name"])

    def test_first_and_last_weekday_prayer_owners_keep_their_own_official_sources(self) -> None:
        for owner, fragment in (("ot-1", "#Y01"), ("ot-34", "#Y34")):
            day = bridge.call("liturgy", "day", "postconciliar", "2027-01-12",
                              {"ordinary": True, "orationMass": owner})
            row = day["rows"][0]
            self.assertEqual(row["mass"]["key"], "ot-1-tuesday")
            self.assertEqual(row["orationSelection"]["owner"], owner)
            self.assertTrue(any(link["language"] == "en" and link["url"].endswith(fragment)
                                and "Collect" in link["prayer_roles"] for link in row["orationWitnessLinks"]))
            self.assertEqual({e["slot"] for e in row["events"] if f"proper/postconciliar/{owner}/" in e["id"]},
                             {"Collect", "Prayer over the Offerings", "Prayer after Communion"})

    def test_published_antiphon_sources_belong_to_the_selected_occurrence_and_language(self) -> None:
        from lectern.missal import event_source_readings

        antiphonary = "https://www.liturgyoffice.org.uk/Missal/Music/Antiphonary.pdf#page="
        all_souls = bridge.call("liturgy", "propers", "postconciliar", "commemoration-all-faithful-departed-all-souls",
                                 {"form": "second", "orations": "en", "textDisplay": "latin-and-selected"})
        for role, fragment in (("Entrance Antiphon", "cj0"), ("Communion Antiphon", "cj1")):
            event = next(e for e in all_souls["events"] if e.get("slot") == role)
            self.assertEqual({link["language"]:link["url"] for _, link in event_source_readings(event)},
                             {"en": antiphonary + "143", "la": "https://www.clerus.org/bibliaclerusonline/en/gls.htm#" + fragment})
        choice = "proper-choice/postconciliar/easter-2/main/entrance-antiphon"
        for option in ("1-peter-2-2", "4-esdras-2-36-37"):
            result = bridge.call("liturgy", "propers", "postconciliar", "easter-2",
                                 {"properChoices": {choice: option}, "orations": "en", "textDisplay": "latin-and-selected"})
            event = next(e for e in result["events"] if e["id"] == choice)
            sources = {(link["language"], link["url"]) for _, link in event_source_readings(event)}
            latin = ("la", "https://www.clerus.org/bibliaclerusonline/en/glg.htm#h0")
            if option == "4-esdras-2-36-37":
                self.assertEqual(sources, {latin, ("en", antiphonary + "60")})
            else:
                self.assertNotIn(latin, sources)

    def test_ordinary_sources_follow_rendered_elements_and_selected_eucharistic_prayer(self) -> None:
        from lectern.missal import witness_label

        pdf = "https://www.liturgyoffice.org.uk/Missal/Text/EP2-A4.pdf#page=1"
        for variant in ("ep-ii", "ep-iii"):
            selected = bridge.call("liturgy", "propers", "postconciliar", "advent-1",
                                   {"ordinary": True, "cycle": "A", "variants": {"eucharistic-prayer": variant}})
            links = selected["ordinaryWitnessLinks"]
            self.assertEqual(pdf in {r["url"] for r in links}, variant == "ep-ii")
            linked_elements = [e["id"] for e in selected["events"]
                               if any(r["url"] == pdf for r in e.get("sourceLinks", []))]
            self.assertEqual(linked_elements, ["ordinary-element/prex-eucharistica/prex-eucharistica-ii"]
                             if variant == "ep-ii" else [])
            card = next(r for r in links if set(r.get("languages", [])) == {"en", "la"})
            self.assertIn("Latin", witness_label(card))
            self.assertIn("English", witness_label(card))
            self.assertTrue(all(r["scope"] == "ordinary" for r in links))
        friday = bridge.call("liturgy", "day", "postconciliar", "2027-03-26", {"ordinary": True})
        self.assertEqual(friday["rows"][0]["ordinaryWitnessLinks"], [])
        read = bridge.call("liturgy", "propers", "postconciliar", "advent-1", {})
        self.assertEqual(read["ordinaryWitnessLinks"], [])

    def test_ep_iv_is_readable_for_the_principal_ordinary_sunday_only(self) -> None:
        options = {"ordinary": True, "variants": {"eucharistic-prayer": "ep-iv"}}
        pdf = "https://www.liturgyoffice.org.uk/Missal/Text/EP4-A4.pdf#page=1"
        for request in (options, {**options, "mass": "ot-9"}):
            rows = bridge.call("liturgy", "day", "postconciliar", "2027-05-30", request)["rows"]
            self.assertEqual(
                [row["mass"]["key"] for row in rows], ["ot-9", "corpus-christi"])
            for row in rows:
                appointed = row["mass"]["key"] == "ot-9"
                self.assertEqual(pdf in {r["url"] for r in row["ordinaryWitnessLinks"]}, appointed)
                self.assertEqual(any(e["id"].endswith("/prex-eucharistica-iv") for e in row["events"]), appointed)
        displaced = bridge.call("liturgy", "day", "postconciliar", "2028-08-06",
                                {**options, "mass": "ot-18"})["rows"][0]
        self.assertEqual(displaced["resolved"]["standing"], "displaced")
        self.assertEqual(displaced["mass"]["key"], "ot-18")
        self.assertNotIn(pdf, {r["url"] for r in displaced["ordinaryWitnessLinks"]})
        for date in ("2026-11-29", "2027-01-12", "2028-08-06"):
            row = bridge.call("liturgy", "day", "postconciliar", date, options)["rows"][0]
            self.assertNotIn(pdf, {r["url"] for r in row["ordinaryWitnessLinks"]})
            self.assertIn("prex-eucharistica/prex-eucharistica-iv", [r["element"] for r in row["ordinaryUnresolved"]])
        standalone = bridge.call("liturgy", "propers", "postconciliar", "ot-9", options)
        self.assertNotIn(pdf, {r["url"] for r in standalone["ordinaryWitnessLinks"]})

    def test_selected_maundy_dismissal_is_the_only_one_printed_in_missal_mode(self) -> None:
        from lectern.missal import events
        from lectern.widgets import Ink

        prefix = "proper-choice/roman-1962/mass-of-the-lords-supper/main/"
        for selected, wanted, other in (("solemn", "Dismissal at the solemn Mass", "Dismissal at the permitted Low Mass"),
                                        ("authorized-low-mass", "Dismissal at the permitted Low Mass", "Dismissal at the solemn Mass")):
            day = bridge.call("liturgy", "day", "roman-1962", "2027-03-25", {"mass": "mass-of-the-lords-supper",
                              "ordinary": True, "properChoices": {prefix + "maundy-dismissal": selected}})
            row = day["rows"][0]
            self.assertEqual(row["mass"]["key"], "mass-of-the-lords-supper")
            ink = Ink()
            events(ink, {**row, "state": day["state"], "ordinary": day["ordinary"]})
            self.assertIn(wanted, ink.content().plain)
            self.assertNotIn(other, ink.content().plain)

    def test_private_passion_blessing_has_its_spoken_text_and_priest_cue(self) -> None:
        from lectern.missal import blocks
        from lectern.widgets import Ink

        request_id = "ordinary-element/oblatio/iube-domine-benedicere"
        options = {"ordinary": True, "ordinaryLang": "en", "textDisplay": "latin-and-selected"}
        for date in ("2027-03-21", "2027-03-23", "2027-03-24"):
            row = bridge.call("liturgy", "day", "roman-1962", date, options)["rows"][0]
            event = next(item for item in row["events"] if item["id"] == request_id)
            ink = Ink()
            blocks(ink, event["blocks"])
            for prayer in ("Jube Dómine benedícere.", "Vouchsafe, O Lord, to bless me."):
                self.assertRegex(ink.content().plain, r"P\s+" + re.escape(prayer))
        choices = {"proper-choice/roman-1962/palm-sunday/main/palm-mass-gospel": "second-or-third-low-mass-gospel"}
        alternate = bridge.call("liturgy", "day", "roman-1962", "2027-03-21",
                                options | {"properChoices": choices})["rows"][0]
        self.assertIn(request_id, {event["id"] for event in alternate["events"]})
        self.assertIn("ordinary-element/oblatio/dominus-vobiscum-ante-evangelium",
                      {event["id"] for event in alternate["events"]})
        requiem = bridge.call("liturgy", "day", "roman-1962", "2027-11-02",
                              options | {"mass": "commemoratione-omnium-fidelium-defunctorum", "form": "first"})["rows"][0]
        self.assertTrue(requiem["events"])
        self.assertNotIn(request_id, {event["id"] for event in requiem["events"]})

    def test_off_date_votive_chants_stay_separate_from_dated_appointments(self) -> None:
        from lectern.dialogs import MissalSource

        key = "beatae-mariae-virginis-reginae"
        view = bridge.call("liturgy", "propers", "roman-1962", key, {})
        chant, = view["votiveChants"]
        self.assertEqual(chant["label"], "Tract after Septuagesima")
        self.assertEqual(chant["common"]["reading"], "held-chant")
        self.assertTrue(chant["source"]["url"].endswith("#page=622"))
        choice = bridge.call("liturgy", "votiveChant", "roman-1962", key, chant["id"],
                             {"orations": "en", "textDisplay": "latin-and-selected"})
        dialog = MissalSource(chant["label"], chant["source"], choice["blocks"], chant["common"])
        for phrase in ("Gaude, Maria Virgo", "1861", "Held chant", "#page=622"):
            self.assertIn(phrase, dialog.body.plain)
        feast = bridge.call("liturgy", "day", "roman-1962", "2027-05-31", {"mass": key})
        self.assertFalse(any(row.get("votiveChants") for row in feast["rows"]))
        self.assertFalse(any(one.get("slot") == "Tract" for row in feast["rows"] for one in row["events"]))
        with self.assertRaises(Refused):
            bridge.call("liturgy", "votiveChant", "roman-1962", "advent-1", chant["id"], {})

    def test_easter_vigil_uses_its_own_mass_frame_and_source_consultations(self) -> None:
        options = {"ordinary": True, "orations": "en", "textDisplay": "latin-and-selected"}
        day = bridge.call("liturgy", "day", "roman-1962", "2027-03-27", options)["rows"][0]
        standalone = bridge.call("liturgy", "propers", "roman-1962", "easter-vigil", options)
        for result in (day, standalone):
            events = result["events"]
            order = [e.get("slot") or e["id"].removeprefix("ordinary-element/") for e in events]
            names = ["Blessing of the New Fire", "Litany of the Saints, second part",
                     "praeparatio/kyrie-eleison", "praeparatio/gloria-in-excelsis", "Collect", "Epistle",
                     "Alleluia", "Gospel", "oblatio/gloria-patri", "Secret", "Preface of the Easter Vigil",
                     "praefatio/sanctus-post-praefationem", "Communicantes of the Easter Vigil",
                     "canon/communicantes-continuatio", "canon/hanc-igitur-pascha-pentecoste",
                     "communio/domine-jesu-christe-fili-dei-vivi", "communio/perceptio-corporis-tui",
                     "conclusio/corpus-tuum-domine", "Antiphon and Psalm at Lauds", "Benedictus",
                     "Postcommunion", "Easter dismissal", "conclusio/placeat-tibi-sancta-trinitas",
                     "conclusio/benedicat-vos-omnipotens-deus"]
            self.assertEqual(order[0], names[0])
            self.assertEqual([order.index(name) for name in names], sorted(order.index(name) for name in names))
            for omitted in ("praeparatio/judica-me-deus", "praeparatio/confiteor-sacerdotis",
                            "oblatio/credo-in-unum-deum", "oblatio/rubrica-offertorium",
                            "communio/agnus-dei", "communio/domine-jesu-christe-qui-dixisti",
                            "conclusio/initium-sancti-evangelii", "conclusio/dominus-vobiscum-ite-missa-est"):
                self.assertNotIn(omitted, order)
            self.assertTrue(any(link.get("rite_opening") and link["url"].endswith("#page=263")
                                for link in result["missalWitnessLinks"]))
            links_by_role = {event["slot"]: {link["language"]: link["url"] for link in event["sourceConsultations"]}
                             for event in events if event.get("sourceConsultations")}
            for role, latin, english in (("Preface of the Easter Vigil", 315, 2),
                                         ("Communicantes of the Easter Vigil", 294, 2),
                                         ("Easter dismissal", 296, 3)):
                self.assertTrue(links_by_role[role]["la"].endswith(f"#page={latin}"))
                self.assertEqual(links_by_role[role]["en"],
                                 f"https://extraordinaryform.org/masses/EasterVigilM20.pdf#page={english}")

    def test_1962_requiem_and_passiontide_use_their_appointed_ordinary(self) -> None:
        def reading(day, **choices):
            view = bridge.call("liturgy", "day", "roman-1962", day, {
                "ordinary": True, "orations": "en", "textDisplay": "latin-and-selected", **choices})
            row = view["rows"][0]
            self.assertFalse(row.get("failed"))
            return row, {event["id"].removeprefix("ordinary-element/"): event
                         for event in row["events"] if event["kind"] == "ordinary-element"}

        for form in ("first", "second", "third"):
            row, held = reading("2027-11-02", mass="commemoratione-omnium-fidelium-defunctorum", form=form)
            self.assertIn("praeparatio/introibo-ad-altare-dei", held)
            self.assertIn("praeparatio/adjutorium-nostrum", held)
            self.assertIn("conclusio/placeat-tibi-sancta-trinitas", held)
            self.assertIn("conclusio/requiescant-in-pace", held)
            for key in ("praeparatio/judica-me-deus", "praeparatio/introibo-ad-altare-dei-repetitio",
                        "oblatio/gloria-patri", "oblatio/dominus-sit-in-corde-meo", "oblatio/per-evangelica-dicta",
                        "communio/agnus-dei", "communio/domine-jesu-christe-qui-dixisti",
                        "conclusio/dominus-vobiscum-ite-missa-est", "conclusio/benedicat-vos-omnipotens-deus"):
                self.assertNotIn(key, held)
            agnus = words(held["communio/agnus-dei-defunctorum"]["blocks"])
            self.assertIn("give unto them rest forevermore", agnus)
            self.assertIn("dona eis réquiem sempitérnam", agnus)
            greeting = held["conclusio/dominus-vobiscum-defunctorum"]["text"]
            self.assertEqual(greeting["text"], "The Lord be with you.\nR. And with thy spirit.")
            self.assertIn("conclusio/initium-sancti-evangelii", [u["element"] for u in row["ordinaryUnresolved"]])

        _, passion = reading("2027-03-14")
        _, saint = reading("2027-03-19", mass="s-ioseph-sponsi-beatae-mariae-virginis")
        for key in ("praeparatio/judica-me-deus", "praeparatio/introibo-ad-altare-dei-repetitio", "oblatio/gloria-patri"):
            self.assertNotIn(key, passion)
            self.assertIn(key, saint)
        for normal in (passion, saint):
            self.assertIn("conclusio/benedicat-vos-omnipotens-deus", normal)
            self.assertIn("communio/agnus-dei", normal)
            self.assertNotIn("communio/rubrica-agnus-dei-in-missis-defunctorum", normal)
            self.assertNotIn("conclusio/requiescant-in-pace", normal)

        for form in ("night", "dawn", "day"):
            _, held = reading("2026-12-25", mass="nativitate-domini-octave", form=form)
            self.assertEqual("conclusio/initium-sancti-evangelii" in held, form != "day")

    def test_memorial_prayer_sources_respect_the_dated_season_and_feria(self) -> None:
        for date, mass, group in (("2027-07-16", "our-lady-mount-carmel", "mary-ordinary"),
                                  ("2027-02-11", "our-lady-lourdes", "mary-lent-local")):
            row = bridge.call("liturgy", "day", "postconciliar", date, {"mass": mass})["rows"][0]
            sources = row["mass"]["memorialPrayerSources"]
            self.assertEqual([one["id"] for one in sources["groups"]], [group])
            if group == "mary-lent-local":
                self.assertTrue(sources["groups"][0]["qualification"])
            independent = bridge.call("liturgy", "propers", "postconciliar", mass, {})["mass"]["memorialPrayerSources"]
            self.assertEqual(len(independent["groups"]), 5)
        sunday = bridge.call("liturgy", "day", "postconciliar", "2029-07-15",
                             {"mass": "saint-bonaventure-bishop-doctor-church"})["rows"][0]
        self.assertFalse(sunday.get("memorialFeria"))

    def test_january_prayers_follow_each_local_epiphany_in_the_reader_frame(self) -> None:
        date = "2027-01-05"
        names = ["Collect", "Prayer over the Offerings", "Prayer after Communion"]
        anchors = ["ritus-initiales/collecta", "praeparatio-donorum/super-oblata", "ritus-communionis/post-communionem"]
        for ordinary in (False, True):
            day = bridge.call("liturgy", "day", "postconciliar", date,
                              {"orations": "en", "textDisplay": "latin-and-selected", "ordinary": ordinary})
            self.assertEqual([r["januarySelection"]["phase"] for r in day["rows"]],
                             ["before-epiphany", "after-epiphany"])
            for row in day["rows"]:
                events = row["events"]
                prayers = [event for event in events if event["kind"] == "january-prayer"]
                self.assertEqual([event["slot"] for event in prayers], names)
                for event, anchor in zip(prayers, anchors):
                    self.assertIn("/2/" + row["januarySelection"]["phase"] + "/", event["id"])
                    self.assertIn("Latin Missal", words(event["blocks"]))
                    if ordinary:
                        self.assertEqual(events[events.index(event) - 1]["id"], "ordinary-element/" + anchor)
            early, late = (next(e for e in r["events"] if e["kind"] == "january-prayer") for r in day["rows"])
            self.assertNotEqual(words(early["blocks"]), words(late["blocks"]))
        memorial = bridge.call("liturgy", "day", "postconciliar", "2027-01-07",
                               {"mass": "saint-raymond-penyafort-priest"})
        self.assertTrue(all(r["memorialFeria"]["january"]["weekday"] == 4 for r in memorial["rows"]))

    def test_the_ordinary_language_default_matches_both_page_owners(self) -> None:
        default = bridge.call("liturgy", "opening")["defaultOrdinaryLanguage"]
        for name in ("day-reader.js", "propers-reader.js"):
            source = (ROOT / "src/web/browser/liturgy" / name).read_text()
            found = re.search(r"\{\s*'ordinary-lang':\s*'([^']+)'\s*\}", source)
            self.assertIsNotNone(found, name)
            self.assertEqual(default, found.group(1), name)

    def test_ordinary_choice_and_language_are_independent_of_orations(self) -> None:
        options = {"orations": "la", "ordinary": True, "ordinaryLang": "en",
                   "variants": {"eucharistic-prayer": "ep-ii"}, "cycle": "A"}
        direct = bridge.call("liturgy", "propers", "postconciliar", "advent-1", options)
        self.assertEqual(direct["ordinary"]["selection"]["eucharistic-prayer"], "ep-ii")
        ordinary = [row for row in direct["events"] if row["kind"] == "ordinary-element"]
        self.assertTrue(ordinary)
        self.assertTrue(all(row["text"]["language"] == "en" for row in ordinary))
        self.assertTrue(any(row["id"].endswith("/prex-eucharistica-ii") for row in ordinary))
        self.assertFalse(any(row["id"].endswith(("/prex-eucharistica-i", "/prex-eucharistica-iii", "/prex-eucharistica-iv"))
                             for row in ordinary))
        day = bridge.call("liturgy", "day", "postconciliar", "2026-11-29", options)
        self.assertEqual(day["ordinary"]["selection"]["eucharistic-prayer"], "ep-ii")
        self.assertTrue(all(row["text"]["language"] == "en" for row in day["rows"][0]["events"]
                            if row["kind"] == "ordinary-element"))

    def test_an_unsupported_ordinary_option_is_refused(self) -> None:
        with self.assertRaisesRegex(Refused, "explicit Ordinary option"):
            bridge.call("liturgy", "propers", "roman-1962", "advent-1",
                        {"ordinary": True, "variants": {"eucharistic-prayer": "ep-ii"}})

    def test_bilingual_keeps_both_languages_in_the_production_rendering(self) -> None:
        view = bridge.call("liturgy", "propers", "roman-1962", "pentecost",
                           {"orations": "en", "ordinary": True, "ordinaryLang": "en",
                            "textDisplay": "latin-and-selected"})
        proper = next(row for row in view["events"] if row.get("slot") == "Collect")
        self.assertIn("Latin", words(proper["blocks"]))
        self.assertIn("English", words(proper["blocks"]))
        ordinary = next(row for row in view["events"] if row["kind"] == "ordinary-element"
                        and "text-side-label" in str(row.get("blocks")))
        self.assertIn("Latin", words(ordinary["blocks"]))
        self.assertIn("English", words(ordinary["blocks"]))

    def test_witnesses_belong_to_the_selected_mass_and_have_selectable_ids(self) -> None:
        view = bridge.call("liturgy", "propers", "postconciliar", "advent-2", {"orations": "en", "cycle": "A"})
        witnesses = view["mass"]["witnesses"]
        self.assertTrue(witnesses)
        self.assertTrue(all(one["id"] and one["available"] > 0 for one in witnesses))
        self.assertTrue(any(one["id"] == "project-created" for one in witnesses))
        picked = bridge.call("liturgy", "propers", "postconciliar", "advent-2",
                             {"orations": "en", "cycle": "A", "witness": "project-created"})
        self.assertEqual(picked["state"]["witness"], "project-created")

    def test_study_uses_the_production_source_and_seating_apparatus(self) -> None:
        blocks = bridge.call("liturgy", "studyPropers", "roman-1962", "pentecost", {})
        said = words(blocks)
        for label in ("Study this selection", "Propers is date-independent", "Functional slot", "Source record"):
            self.assertIn(label, said)
        self.assertIn("proper-structure", said)
        branches = bridge.call("liturgy", "studyDay", "roman-1962", "2026-05-24", {})
        self.assertIn("Calendar result", words(branches[0]["blocks"]))
        self.assertIn("2026-05-24", words(branches[0]["blocks"]))

    def test_propers_comparisons_stay_date_independent_and_keep_their_peers(self) -> None:
        cases = [
            ("advent-1", {"cycle": "A"}, "oration-language", "la", "en"),
            ("transfiguration-lord", {}, "lectionary-cycle", "A", "B"),
            ("advent-1", {"cycle": "A"}, "bible-edition", "douay-rheims", "clementine-vulgate"),
        ]
        view = bridge.call("liturgy", "propers", "postconciliar", "ot-12-thursday", {"cycle": "I"})
        offer = next(one for one in view["comparisonOffers"] if one["dimension"] == "reading-alternative")
        cases.append(("ot-12-thursday", {"cycle": "I"}, "reading-alternative",
                      offer["options"][0]["id"], offer["options"][1]["id"]))
        for key, options, dimension, primary, peer in cases:
            with self.subTest(dimension=dimension):
                compared = bridge.call("liturgy", "comparePropers", "postconciliar", key, options,
                                       {"dimension": dimension, "primary": primary, "peer": peer})
                self.assertIsNone(compared["calendarResult"])
                self.assertEqual(compared["semantic"]["dimension"], dimension)
                self.assertEqual(compared["semantic"]["anchor"]["correspondingFormulary"], key)
                self.assertTrue(compared["blocks"])
                self.assertEqual(compared["selection"]["peer"], peer)

    def test_compare_does_not_choose_a_missing_peer_or_resolve_an_open_choice(self) -> None:
        with self.assertRaisesRegex(Refused, "two distinct held peers"):
            bridge.call("liturgy", "comparePropers", "postconciliar", "advent-1", {},
                        {"dimension": "oration-language", "primary": "la", "peer": "la"})
        with self.assertRaisesRegex(Refused, "choices that remain unresolved"):
            bridge.call("liturgy", "comparePropers", "postconciliar", "ot-12-thursday", {"cycle": "I"},
                        {"dimension": "oration-language", "primary": "la", "peer": "en"})

    def test_reader_urls_round_trip_languages_options_location_and_legacy_pairs(self) -> None:
        options = {"orations": "en", "ordinary": True, "ordinaryLang": "la", "cycle": "A",
                   "textDisplay": "latin-and-selected", "companion": "clementine-vulgate",
                   "variants": {"eucharistic-prayer": "ep-ii"},
                   "location": "proper/postconciliar/transfiguration-lord/001",
                   "urlLegacy": {"unknown": [{"key": "retained-note", "value": "a & b"}], "inert": []}}
        route = bridge.call("liturgy", "readerUrl", "propers", "postconciliar", "transfiguration-lord", options, None)
        self.assertIn("type=christological", route)
        self.assertIn("retained-note=a%20%26%20b", route)
        target = bridge.call("liturgy", "openReaderLink", "https://mystago.gy/" + route.replace("index.html", "propers-reader.html"), "day")
        self.assertEqual(target["entrance"], "propers")
        intent = target["intent"]
        for key in ("orations", "ordinary", "ordinaryLang", "cycle", "textDisplay", "companion", "variants", "location", "urlLegacy"):
            self.assertEqual(intent[key], options[key], key)
        reshared = bridge.call("liturgy", "readerUrl", "propers", intent["calendar"], intent["mass"], intent, None)
        self.assertEqual(reshared, route)

    def test_compare_urls_round_trip_both_entrances(self) -> None:
        cases = [("propers", "postconciliar", "transfiguration-lord",
                  {"dimension": "lectionary-cycle", "primary": "A", "peer": "B"}),
                 ("day", "roman-1962", "2026-10-25", {"peer": "roman-pre-1955"})]
        for entrance, calendar, anchor, selection in cases:
            with self.subTest(entrance=entrance):
                route = bridge.call("liturgy", "readerUrl", entrance, calendar, anchor, {}, selection)
                result = bridge.call("liturgy", "openReaderLink", "https://mystago.gy/" + route, entrance)
                self.assertEqual(result["entrance"], entrance)
                if entrance == "propers":
                    self.assertEqual(result["intent"]["comparison"], selection)
                else:
                    self.assertTrue(result["intent"]["comparing"])
                    self.assertEqual(result["intent"]["peer"], selection["peer"])

    def test_url_import_does_not_discard_invalid_locations_or_custom_data(self) -> None:
        for value, reason in [("#date=2026-05-24&missal=roman-1962&location=proper/no-such-event", "semantic location"),
                              ("?data=https://example.test/other#date=2026-05-24", "custom browser data root")]:
            with self.subTest(value=value), self.assertRaisesRegex(Refused, reason):
                bridge.call("liturgy", "openReaderLink", value, "day")
        browse = bridge.call("liturgy", "openReaderLink", "https://mystago.gy/liturgy/", "day")
        self.assertEqual(browse["entrance"], "propers")
        self.assertTrue(browse["intent"]["browse"])
        self.assertNotIn("mass", browse["intent"])

    def test_the_latin_bible_companion_uses_its_own_numbering_and_rendering(self) -> None:
        view = bridge.call("liturgy", "propers", "roman-1962", "pentecost", {"companion": "clementine-vulgate"})
        self.assertEqual(view["state"]["scriptureCompanion"], {"id": "clementine-vulgate", "numbering": "vulgate"})
        self.assertTrue(any("scripture-pair" in str(row.get("blocks")) for row in view["events"]))
        with self.assertRaisesRegex(Refused, "must be a held Latin Bible"):
            bridge.call("liturgy", "propers", "roman-1962", "pentecost", {"companion": "douay-rheims"})

    def test_native_source_paths_supply_exact_admitted_choice_requests(self) -> None:
        view = bridge.call("liturgy", "propers", "postconciliar", "baptism-of-the-lord", {"cycle": "B"})
        (path,) = view["sourcePaths"]
        alternate = next(one for one in path["options"] if one["id"] == "year-b-optional")
        forbidden = next(one for one in path["options"] if one["id"] == "year-c-optional")
        self.assertFalse(alternate["unavailable"])
        self.assertTrue(forbidden["unavailable"])
        self.assertIsNone(forbidden["properChoices"])
        chosen = bridge.call("liturgy", "propers", "postconciliar", "baptism-of-the-lord",
                             {"cycle": "B", "properChoices": alternate["properChoices"]})
        self.assertEqual(chosen["sourcePaths"][0]["selection"]["option"], "year-b-optional")
        self.assertIn("Source reading path", words(chosen["sourcePaths"][0]["blocks"]))
        self.assertTrue(chosen["events"])

    def test_source_path_request_keeps_independent_choices(self) -> None:
        view = bridge.call("liturgy", "propers", "postconciliar", "advent-1-monday", {})
        first = next(one for one in view["sourcePaths"][0]["options"] if not one["unavailable"])
        chosen = bridge.call("liturgy", "propers", "postconciliar", "advent-1-monday",
                             {"properChoices": first["properChoices"]})
        second = next(one for one in chosen["sourcePaths"][1]["options"] if not one["unavailable"])
        self.assertTrue(all(second["properChoices"][key] == value for key, value in first["properChoices"].items()))


@unittest.skipUnless(importlib.util.find_spec("textual") and shutil.which("node"), "Textual and node are required")
class SurfaceParityTests(unittest.IsolatedAsyncioTestCase):
    async def test_all_souls_communion_source_opens_both_exact_editions(self) -> None:
        from unittest.mock import patch
        from lectern.app import TriptychApp
        from lectern.dialogs import MissalSource, Pick
        from lectern.snapshot import _settle
        from lectern.surfaces.propers import Propers

        app = TriptychApp(start="propers", intent={"calendar": "postconciliar", "form": "second",
                          "mass": "commemoration-all-faithful-departed-all-souls", "orations": "en"})
        async with app.run_test(size=(80, 30)) as pilot:
            await _settle(app, pilot)
            reader = app.query_one(Propers)
            target = next(e["id"] for e in reader.view["events"] if e.get("slot") == "Communion Antiphon")
            await pilot.press("i")
            await _settle(app, pilot)
            index = next(i for i, (key, _) in enumerate(app.screen.options) if key == target)
            await pilot.press("home", *(["down"] * index), "enter")
            await _settle(app, pilot)
            for language, ending in (("English", "#page=143"), ("Latin", "#cj1")):
                await pilot.press("ctrl+o")
                await _settle(app, pilot)
                self.assertIsInstance(app.screen, Pick)
                matches = [i for i, (_, label) in enumerate(app.screen.options) if " · " + language + " · " in label]
                self.assertEqual(len(matches), 1)
                await pilot.press("home", *(["down"] * matches[0]), "enter")
                await _settle(app, pilot)
                self.assertIsInstance(app.screen, MissalSource)
                self.assertTrue(app.screen.url.endswith(ending))
                with patch.object(app, "open_url") as opened:
                    await pilot.press("o")
                    opened.assert_called_once_with(app.screen.url)
                await pilot.press("escape")
                await _settle(app, pilot)

    async def test_votive_chant_settings_open_the_qualified_bilingual_common(self) -> None:
        from textual.widgets import OptionList
        from lectern.app import TriptychApp
        from lectern.dialogs import MissalSource
        from lectern.snapshot import _settle

        app = TriptychApp(start="propers", intent={"calendar": "roman-1962", "orations": "en",
                          "mass": "beatae-mariae-virginis-reginae", "textDisplay": "latin-and-selected"})
        async with app.run_test(size=(80, 30)) as pilot:
            await _settle(app, pilot)
            await pilot.press("comma")
            await _settle(app, pilot)
            options = app.screen.options
            index = next(i for i, (key, _) in enumerate(options) if key == "votive_chants")
            listing = app.screen.query_one(OptionList)
            listing.highlighted = listing.get_option_index(str(index))
            await pilot.press("enter")
            await _settle(app, pilot)
            self.assertEqual(app.screen.title_text, "Seasonal and votive chants")
            await pilot.press("home", "enter")
            await _settle(app, pilot)
            self.assertIsInstance(app.screen, MissalSource)
            self.assertTrue(app.screen.url.endswith("#page=622"))
            self.assertIn("Gaude, Maria Virgo", app.screen.body.plain)
            self.assertIn("1861", app.screen.body.plain)
            await pilot.press("escape")

    async def test_omitting_a_lenten_prayer_releases_a_witness_used_only_there(self) -> None:
        from textual.widgets import OptionList
        from lectern.app import TriptychApp
        from lectern.snapshot import _settle
        from lectern.surfaces.day import Day
        from lectern.surfaces.propers import Propers

        for mass, date in (("lent-1-saturday", "2027-02-20"), ("lent-2-friday", "2027-02-26")):
            group = f"proper-choice/postconciliar/{mass}/main/prayer-over-the-people"
            for entrance, surface in (("propers", Propers), ("day", Day)):
                settings = {"calendar": "postconciliar", "mass": mass, "ordinary": True, "orations": "en",
                            "witness": "project-created", "properChoices": {group: "pray"}}
                if entrance == "day":
                    settings["date"] = date
                app = TriptychApp(start=entrance, intent=settings)
                async with app.run_test(size=(80, 30)) as pilot:
                    await _settle(app, pilot)
                    reader = app.query_one(surface)
                    self.assertEqual(reader.selection()["witness"], "project-created")
                    await pilot.press("s")
                    await _settle(app, pilot)
                    def is_omit(value):
                        if entrance == "day":
                            return value[2:4] == ("proper-choice", (group, "omit"))
                        return value == ("proper-choice", group, "omit")
                    index = next(i for i, (key, _) in enumerate(app.screen.options) if is_omit(key))
                    app.screen.query_one(OptionList).highlighted = index
                    await pilot.press("enter")
                    await _settle(app, pilot)
                    self.assertNotIn("witness", reader.selection())
                    view = reader.view if entrance == "propers" else reader.views["postconciliar"]["rows"][0]
                    event = next(one for one in view["events"] if one["id"] == group)
                    self.assertEqual(event["selection"]["option"], "omit")
                    omitted = next(option for option in event["options"] if option["id"] == "omit")
                    self.assertEqual(omitted["members"], [])

    async def test_vigil_facsimile_opens_at_the_rite_and_the_current_prayer(self) -> None:
        from unittest.mock import patch
        from lectern.app import TriptychApp
        from lectern.dialogs import MissalSource, Pick, Pick
        from lectern.snapshot import _settle
        from lectern.surfaces.day import Day
        from textual.widgets import OptionList

        app = TriptychApp(start="day", intent={"calendar": "roman-1962", "date": "2027-03-27", "ordinary": True})
        async with app.run_test(size=(80, 30)) as pilot:
            await _settle(app, pilot)
            day = app.query_one(Day)
            await pilot.press("comma")
            self.assertIsInstance(app.screen, Pick)
            index = next(i for i, (key, _) in enumerate(app.screen.options) if key == "rite_source")
            await pilot.press("home", *(["down"] * index), "enter")
            await _settle(app, pilot)
            self.assertIsInstance(app.screen, MissalSource)
            self.assertTrue(app.screen.url.endswith("#page=263"))
            await pilot.press("escape", "i")
            target = next(e["id"] for e in day.source_rows()[0]["events"] if e["slot"] == "Preface of the Easter Vigil")
            index = next(i for i, (key, _) in enumerate(app.screen.options) if key == target)
            app.screen.query_one(OptionList).highlighted = index
            await pilot.press("enter")
            await _settle(app, pilot)
            for label, page in (("Latin", "#page=315"), ("English", "#page=2")):
                await pilot.press("ctrl+o")
                await _settle(app, pilot)
                self.assertIsInstance(app.screen, Pick)
                index = next(i for i, (_, title) in enumerate(app.screen.options) if label in title)
                app.screen.query_one(OptionList).highlighted = index
                await pilot.press("enter")
                await _settle(app, pilot)
                self.assertIsInstance(app.screen, MissalSource)
                self.assertTrue(app.screen.url.endswith(page))
                with patch.object(app, "open_url") as opened:
                    await pilot.press("o")
                    opened.assert_called_once_with(app.screen.url)
                await pilot.press("escape")
                await _settle(app, pilot)

    async def test_exact_missal_witness_can_be_opened_and_copied_from_settings(self) -> None:
        from unittest.mock import patch
        from lectern.app import TriptychApp
        from lectern.dialogs import MissalSource
        from lectern.snapshot import _settle
        from lectern.surfaces.day import Day
        from lectern.surfaces.propers import Propers

        for surface, target in [(Day, {"date": "2026-11-29"}), (Propers, {"mass": "commune-doctorum-ecclesiae"})]:
            app = TriptychApp(start=surface.label.lower(), intent={"calendar": "postconciliar", **target})
            async with app.run_test(size=(60, 16)) as pilot:
                await _settle(app, pilot)
                reader = app.query_one(surface)
                link = reader.source_rows()[0]["missalWitnessLinks"][0]
                self.assertTrue(link["url"].startswith("https://"))
                await pilot.press("comma", "end", "enter")
                if not isinstance(app.screen, MissalSource):
                    await pilot.press("home", "enter")
                self.assertIsInstance(app.screen, MissalSource)
                self.assertIn(link["url"], app.screen.body.plain)
                self.assertIn(link["locus"], app.screen.body.plain)
                self.assertIn(link["source_id"], app.screen.body.plain)
                self.assertIn(link["edition_label"], app.screen.body.plain)
                with patch.object(app, "open_url") as opened, patch.object(app, "copy_to_clipboard") as copied:
                    await pilot.press("o", "c")
                    opened.assert_called_once_with(link["url"])
                    copied.assert_called_once_with(link["url"])
                await pilot.press("escape")
                await _settle(app, pilot)
                await pilot.press("d")
                await _settle(app, pilot)
                self.assertIn(link["url"], app.screen.body.plain)

    async def test_last_weekday_prayer_owner_is_visible_and_opens_its_source(self) -> None:
        from lectern.app import TriptychApp
        from lectern.dialogs import MissalSource
        from lectern.snapshot import _settle, _text
        from lectern.surfaces.day import Day
        from textual.widgets import OptionList

        app = TriptychApp(start="day", intent={"calendar": "postconciliar", "date": "2027-01-12"})
        async with app.run_test(size=(60, 16)) as pilot:
            await _settle(app, pilot)
            day = app.query_one(Day)
            await pilot.press("s", "end")
            listing = app.screen.query_one(OptionList)
            self.assertGreater(listing.scroll_y, 0)
            self.assertIn("Week XXXIV", _text(app, styles=False))
            await pilot.press("enter")
            await _settle(app, pilot)
            row = day.source_rows()[0]
            self.assertEqual(row["orationSelection"]["owner"], "ot-34")
            self.assertTrue(row["orationWitnessLinks"])
            await pilot.press("comma", "end", "enter")
            if not isinstance(app.screen, MissalSource):
                index = next(i for i, (_, label) in enumerate(app.screen.options)
                             if "Prayers from Week XXXIV" in label)
                app.screen.query_one(OptionList).highlighted = index
                await pilot.press("enter")
            self.assertIn(row["orationWitnessLinks"][0]["url"], app.screen.body.plain)
            self.assertIn("Prayers from Week XXXIV", app.screen.body.plain)
            await pilot.press("escape", "i")
            target = next(e["id"] for e in row["events"] if e.get("slot") == "Collect")
            index = next(i for i, (key, _) in enumerate(app.screen.options) if key.endswith(target))
            app.screen.query_one(OptionList).highlighted = index
            await pilot.press("enter")
            await _settle(app, pilot)
            await pilot.press("ctrl+o")
            await _settle(app, pilot)
            self.assertIsInstance(app.screen, MissalSource)
            self.assertEqual(app.screen.url, "https://rmhealey.com/docs/RMU/#Y34")

    async def test_memorial_prayer_source_controls_open_independent_common_and_ferial_roles(self) -> None:
        from lectern.app import TriptychApp
        from lectern.dialogs import Pick
        from lectern.snapshot import _settle
        from lectern.surfaces.day import Day
        from lectern.surfaces.propers import Propers

        key = "saint-bonaventure-bishop-doctor-church"
        app = TriptychApp(start="day", intent={"calendar": "postconciliar", "date": "2027-07-15", "ordinary": True})
        async with app.run_test(size=(80, 30)) as pilot:
            await _settle(app, pilot)
            day = app.query_one(Day)
            row = day.source_rows()[0]
            self.assertEqual(row["mass"]["key"], key)
            collect = next(event["id"] for event in row["events"] if event.get("slot") == "Collect")

            async def pick(identifier) -> None:
                self.assertIsInstance(app.screen, Pick)
                index = next(i for i, (value, _) in enumerate(app.screen.options) if value == identifier)
                await pilot.press("home", *(["down"] * index), "enter")
                await _settle(app, pilot)

            for role, group, form, owner in (
                    ("Prayer over the Offerings", "church-doctors", "doctors-2", "commune-doctorum-ecclesiae"),
                    ("Prayer after Communion", "pastors-bishop", "pastor-bishop-1", "commune-pastorum"),
                    ("Prayer after Communion", "current-feria", "ot-34", "ot-34")):
                await pilot.press("comma")
                await pick("memorial/" + role)
                await pick(group)
                if group == "current-feria":
                    self.assertEqual(len(app.screen.options), 34)
                await pick(form)
                propers = app.query_one(Propers)
                self.assertEqual(propers.view["key"], owner)
                selected = next(event["id"] for event in propers.view["events"] if event.get("slot") == role)
                self.assertEqual(propers.navigation.focused[0], selected)
                app.action_surface("day")
                await _settle(app, pilot)
                self.assertEqual(day.source_rows()[0]["mass"]["key"], key)
                self.assertIn(collect, [event["id"] for event in day.source_rows()[0]["events"]])

    async def test_memorial_only_translation_witness_does_not_follow_its_common_prayer(self) -> None:
        from contextlib import nullcontext
        from unittest.mock import patch
        from lectern.app import TriptychApp
        from lectern.dialogs import MissalSource, Pick
        from lectern.snapshot import _settle
        from lectern.surfaces.propers import Propers

        role = "Prayer over the Offerings"
        app = TriptychApp(start="propers", intent={"calendar": "postconciliar", "orations": "en",
                              "mass": "saint-hilary-bishop-doctor-church", "witness": "project-created"})
        async with app.run_test(size=(80, 30)) as pilot:
            await _settle(app, pilot)
            propers = app.query_one(Propers)
            self.assertEqual(propers.view["state"]["witness"], "project-created")
            await pilot.press("comma")
            for choice in ("memorial/" + role, "church-doctors", "doctors-2"):
                self.assertIsInstance(app.screen, Pick)
                index = next(i for i, (value, _) in enumerate(app.screen.options) if value == choice)
                await pilot.press("home", *(["down"] * index), "enter")
                await _settle(app, pilot)
            self.assertEqual(propers.view["key"], "commune-doctorum-ecclesiae")
            self.assertIsNone(propers.view["state"].get("witness"))
            target = next(e["id"] for e in propers.view["events"] if e.get("slot") == role)
            self.assertEqual(propers.navigation.focused[0], target)
            await pilot.press("ctrl+o")
            self.assertIsInstance(app.screen, MissalSource)
            self.assertEqual(app.screen.url, "https://rmhealey.com/docs/RMU/#CDC2")
            self.assertIn(role, app.screen.body.plain)
            self.assertIn("Australian Liturgy (2021)", app.screen.body.plain)
            self.assertIn("Restricted rights", app.screen.body.plain)
            with patch.object(app, "open_url") as opened, patch.object(app, "suspend", return_value=nullcontext()), \
                    patch("lectern.dialogs.terminal_browser", return_value="/usr/bin/lynx"), \
                    patch("lectern.dialogs.subprocess.run") as ran:
                await pilot.press("o", "t")
                opened.assert_called_once_with(app.screen.url)
                ran.assert_called_once_with(["/usr/bin/lynx", app.screen.url], check=False)

    async def test_standalone_january_prayers_require_weekday_and_epiphany_phase(self) -> None:
        from unittest.mock import patch
        from lectern.app import TriptychApp
        from lectern.dialogs import JanuaryReading, Pick
        from lectern.snapshot import _settle

        app = TriptychApp(start="propers", intent={"calendar": "postconciliar", "mass": "christmas-january-4",
                                                   "orations": "en", "textDisplay": "latin-and-selected"})
        async with app.run_test(size=(80, 30)) as pilot:
            await _settle(app, pilot)
            await pilot.press("comma")
            for choice in ("january_prayers", 2, "after-epiphany"):
                self.assertIsInstance(app.screen, Pick)
                index = next(i for i, (value, _) in enumerate(app.screen.options) if value == choice)
                await pilot.press("home", *(["down"] * index), "enter")
                await _settle(app, pilot)
            self.assertIsInstance(app.screen, JanuaryReading)
            self.assertEqual(app.screen.title_text, "Tuesday after Epiphany")
            self.assertIn("English antiphons only", app.screen.body.plain)
            self.assertIn("Prayer after Communion", app.screen.body.plain)
            source = app.screen.reading
            with patch.object(app, "open_url") as opened:
                self.assertIn("U.S. English missal prayers", app.screen.body.plain)
                self.assertIn("Restricted rights", app.screen.body.plain)
                self.assertNotEqual(source["english_prayer_url"], source["english_url"])
                await pilot.press("o", "a", "e", "r")
                self.assertEqual([args.args[0] for args in opened.call_args_list],
                                 [source["latin_url"], source["english_url"], source["english_prayer_url"], source["rule_url"]])

    async def test_missal_reading_keys_settings_and_pane_focus(self) -> None:
        from lectern.app import TriptychApp
        from lectern.dialogs import Pick
        from lectern.snapshot import _settle, _text
        from lectern.surfaces.day import Day
        from lectern.surfaces.propers import Propers

        for surface, target in [(Day, {"date": "2026-11-29"}), (Propers, {"mass": "advent-1", "cycle": "A"})]:
            for size in [(60, 16), (140, 40)]:
                with self.subTest(surface=surface.label, size=size):
                    app = TriptychApp(start=surface.label.lower(), intent={
                        "calendar": "postconciliar", "ordinary": True, **target})
                    async with app.run_test(size=size) as pilot:
                        await _settle(app, pilot)
                        reader = app.query_one(surface)
                        pane = reader.reading_panel()
                        self.assertIs(app.focused, pane)
                        page = pane.scrollable_content_region.height - 1
                        for key, offset in [("down", 1), ("pagedown", page + 1), ("pageup", 1), ("up", 0)]:
                            await pilot.press(key)
                            self.assertEqual(pane.scroll_y, offset, key)
                        await pilot.press("comma", "end")
                        self.assertIsInstance(app.screen, Pick)
                        self.assertIn("Latin companion", _text(app, styles=False))
                        await pilot.press("escape", "f")
                        await _settle(app, pilot)
                        self.assertIs(app.focused, reader.query_one(reader.BROWSE))
                        if size == (60, 16):
                            for width, height in [(140, 40), size]:
                                await pilot.resize_terminal(width, height)
                                await _settle(app, pilot)
                                self.assertIs(app.focused, reader.query_one(reader.BROWSE))
                        await pilot.press("f")
                        await _settle(app, pilot)
                        self.assertIs(app.focused, pane)

    def test_declared_versicle_response_and_priest_cues_share_spacing_and_ink(self) -> None:
        from lectern.missal import blocks
        from lectern.widgets import Ink

        runs = [("℣.", ["vr-glyph"]), ("℟", ["cue-mark"]), ("P", ["cue-mark"]),
                ("Priest", ["speaker-tag", "is-priest"])]
        fallback = blocks(Ink(), [{"runs": [
            {"text": "Composed text — not scripture · Latin", "classes": ["composed-label"]},
            {"text": "Orémus."}]}], missal_mode=True)
        self.assertEqual(fallback.content().plain, "Latin\nOrémus.\n")
        for source, classes in runs:
            with self.subTest(source=source):
                ink = blocks(Ink(), [{"runs": [{"text": source, "classes": classes},
                                               {"text": "  Held words."}]}])
                cue = "P" if source == "Priest" else source
                self.assertEqual(ink.parts[0], (cue + "  ", "bold $rubric"))
                self.assertEqual(ink.content().plain, cue + "  Held words.\n")

    def test_specialized_ordinary_frame_status_remains_visible_in_the_reading(self) -> None:
        from lectern.missal import ordinary_conditions
        from lectern.widgets import Ink

        for date in ("2027-03-25", "2027-03-26", "2027-03-27"):
            row = bridge.call("liturgy", "day", "roman-1962", date, {"ordinary": True})["rows"][0]
            ink = Ink()
            ordinary_conditions(ink, row, compact=True)
            has_frame = any(event["kind"] == "ordinary-element" for event in row["events"])
            self.assertEqual(has_frame, date != "2027-03-26")
            if has_frame:
                self.assertNotIn("Specialized Ordinary unavailable", ink.content().plain)
                self.assertTrue(any(link.get("rite_opening") for link in row["missalWitnessLinks"]))
            else:
                self.assertIn("No Mass Ordinary for this rite", ink.content().plain)

    async def test_day_ordinary_picker_applies_a_choice_without_a_formulary_row(self) -> None:
        from lectern.app import TriptychApp
        from lectern.dialogs import Pick
        from lectern.snapshot import _settle
        from lectern.surfaces.day import Day
        from textual.widgets import OptionList

        app = TriptychApp(start="day", intent={"calendar": "postconciliar", "date": "2026-11-29",
                                               "ordinary": True})
        async with app.run_test(size=(80, 30)) as pilot:
            await _settle(app, pilot)
            day = app.query_one(Day)
            await pilot.press("s")
            await _settle(app, pilot)
            self.assertIsInstance(app.screen, Pick)
            target = ("eucharistic-prayer", "ep-ii")
            picker = app.screen.query_one(OptionList)
            picker.highlighted = next(index for index, (value, _) in enumerate(app.screen.options)
                                      if value[2:4] == ("ordinary-variant", target))
            await pilot.press("enter")
            await _settle(app, pilot)
            view = day.views["postconciliar"]
            self.assertEqual(view["ordinary"]["selection"][target[0]], target[1])
            ids = [item["id"] for item in view["rows"][0]["events"]]
            self.assertIn("ordinary-element/prex-eucharistica/prex-eucharistica-ii", ids)
            self.assertNotIn("ordinary-element/prex-eucharistica/te-igitur", ids)

    async def test_day_witness_choices_belong_to_a_resolved_form_and_branch(self) -> None:
        from lectern.app import TriptychApp
        from lectern.dialogs import Pick
        from lectern.snapshot import _settle
        from lectern.surfaces.day import Day
        from textual.widgets import OptionList

        app = TriptychApp(start="day", intent={"calendar": "postconciliar", "date": "2027-05-09",
                                               "orations": "en"})
        async with app.run_test(size=(80, 30)) as pilot:
            await _settle(app, pilot)
            day = app.query_one(Day)
            rows = day.views["postconciliar"]["rows"]
            resolved = next(row for row in rows if not row.get("primaryDayChoice"))
            unresolved = next(row for row in rows if row.get("primaryDayChoice"))
            self.assertEqual(unresolved["mass"]["witnesses"], [])
            await pilot.press("w")
            await _settle(app, pilot)
            self.assertIsInstance(app.screen, Pick)
            options = [(value, label) for value, label in app.screen.options if value[1]]
            self.assertTrue(options)
            for (territory, _), label in options:
                self.assertEqual(territory, resolved["option"])
                self.assertIn(resolved["heading"]["label"], label)
            app.screen.query_one(OptionList).highlighted = 1
            await pilot.press("enter")
            await _settle(app, pilot)
            selection = day.selection()
            self.assertEqual((selection["territory"], selection["witness"]), options[0][0])
            (selected,) = day.views["postconciliar"]["rows"]
            self.assertEqual(selected["option"], resolved["option"])
            self.assertNotIn("failed", selected)

    async def test_commemorated_st_isidore_can_be_read_while_a_conditional_observance_stays_open(self) -> None:
        from lectern.app import TriptychApp
        from lectern.snapshot import _settle
        from lectern.surfaces.day import Day
        from textual.widgets import OptionList

        key = "s-isidori-episcopi-confessoris-ecclesiae-doctoris"
        for iso in ("2031-04-04", "2036-04-04"):
            with self.subTest(date=iso):
                app = TriptychApp(start="day", intent={"calendar": "roman-1962", "date": iso, "ordinary": True})
                async with app.run_test(size=(80, 30)) as pilot:
                    await _settle(app, pilot)
                    day = app.query_one(Day)
                    self.assertEqual(day.source_rows()[0]["primaryDayChoice"], "seven-sorrows-where-devotions-are-held")
                    await pilot.press("s")
                    index = next(i for i, (v, label) in enumerate(app.screen.options)
                                 if v[3] == key and "commemorated" in label)
                    app.screen.query_one(OptionList).highlighted = index
                    await pilot.press("enter")
                    await _settle(app, pilot)
                    row = day.source_rows()[0]
                    self.assertEqual(row["mass"]["key"], key)
                    self.assertEqual(row["resolved"]["standing"], "commemorated")
                    self.assertEqual(row["title"], row["mass"]["name"])
                    self.assertTrue(row["events"])

    async def test_unsettled_occurrence_can_be_read_without_appointing_a_mass(self) -> None:
        from lectern.app import TriptychApp
        from lectern.dialogs import Pick
        from lectern.snapshot import _settle
        from lectern.surfaces.day import Day
        from textual.widgets import OptionList

        calendar, date = "postconciliar", "2033-06-24"
        app = TriptychApp(start="day", intent={"calendar": calendar, "date": date})
        async with app.run_test(size=(80, 30)) as pilot:
            await _settle(app, pilot)
            day = app.query_one(Day)
            view = day.views[calendar]
            self.assertEqual(view["title"], "Choose a formulary to read")
            self.assertFalse(view["day"]["branches"][0]["settled"])
            self.assertIsNone(view["day"]["branches"][0]["winner"])
            self.assertEqual(view["rows"][0]["events"], [])
            await pilot.press("s")
            await _settle(app, pilot)
            self.assertIsInstance(app.screen, Pick)
            options = [(index, value) for index, (value, _) in enumerate(app.screen.options)
                       if value[2] == "calendar-reading"]
            self.assertEqual({value[3] for _, value in options},
                             {"ot-12-friday", "most-sacred-heart-jesus", "nativity-saint-john-baptist"})
            app.screen.query_one(OptionList).highlighted = next(
                index for index, value in options if value[3] == "most-sacred-heart-jesus")
            await pilot.press("enter")
            await _settle(app, pilot)
            (row,) = day.views[calendar]["rows"]
            self.assertEqual(Day.resolved_key(row), "most-sacred-heart-jesus")
            self.assertEqual(row["resolved"]["standing"], "unresolved")
            self.assertFalse(row["branch"]["settled"])
            self.assertIsNone(row["branch"]["winner"])
            self.assertTrue(row["events"])
            self.assertIn(row["branch"]["unsettled"][0]["why"], day.query_one("#day-text-a").content.plain)

    async def test_day_can_reselect_source_mass_and_forms_with_cli_event_parity(self) -> None:
        from lectern.app import TriptychApp
        from lectern.dialogs import Pick
        from lectern.snapshot import _settle
        from lectern.surfaces.day import Day
        from textual.widgets import OptionList

        cases = [
            ("postconciliar", "2026-10-19", "calendar-formulary",
             "saint-paul-cross-priest", "ot-29-monday", None, "pentecost"),
            ("roman-1962", "2026-12-25", "proper-form",
             "night", "day", "nativitate-domini-octave", "first"),
            ("roman-1962", "2026-11-02", "proper-form",
             "first", "third", "commemoratione-omnium-fidelium-defunctorum", "night"),
        ]
        for calendar, date, kind, first, second, mass, foreign in cases:
            with self.subTest(calendar=calendar, date=date):
                app = TriptychApp(start="day", intent={"calendar": calendar, "date": date,
                                      "ordinary": True, "ordinaryLang": "la", "orations": "la"})
                async with app.run_test(size=(120, 40)) as pilot:
                    await _settle(app, pilot)
                    day = app.query_one(Day)
                    for target in (first, second):
                        await pilot.press("s")
                        await _settle(app, pilot)
                        self.assertIsInstance(app.screen, Pick)
                        offered = [(index, value) for index, (value, _) in enumerate(app.screen.options)
                                   if value[2].startswith(kind)]
                        self.assertNotIn(foreign, [value[3] for _, value in offered])
                        matches = [index for index, value in offered if value[3] == target]
                        self.assertEqual(len(matches), 1, (target, offered))
                        app.screen.query_one(OptionList).highlighted = matches[0]
                        await pilot.press("enter")
                        await _settle(app, pilot)
                        row = day.views[calendar]["rows"][0]
                        self.assertNotIn("failed", row)
                        wanted_mass = mass or target
                        wanted_form = target if mass else "main"
                        self.assertEqual(Day.resolved_key(row), wanted_mass)
                        self.assertEqual(row["resolved"].get("form") or "main", wanted_form)
                        direct = bridge.call("liturgy", "day", calendar, date, day.options_for(calendar))
                        events = [(event["id"], event["kind"]) for event in row["events"]]
                        self.assertEqual(events, [(event["id"], event["kind"])
                                                  for event in direct["rows"][0]["events"]])
                        arguments = [sys.executable, str(ROOT / "tools/mass-today"), "show",
                                     "--calendar", calendar, "--date", date,
                                     "--expanded", "--lang", "la", "--format", "json"]
                        if mass:
                            arguments.extend(["--form", target])
                        else:
                            arguments.extend(["--mass", target])
                        done = await asyncio.to_thread(subprocess.run, arguments, cwd=ROOT,
                                                       capture_output=True, text=True, timeout=90)
                        self.assertEqual(done.returncode, 0, done.stderr)
                        selected = next(item for item in json.loads(done.stdout)["days"][0]["masses"]
                                        if item["key"] == wanted_mass)
                        self.assertEqual(selected["selected_form"], wanted_form)
                        self.assertEqual(events, [(event["id"], event["kind"])
                                                  for event in selected["expanded_events"]])
                    invalid = dict(day.options_for(calendar))
                    invalid["form" if mass else "mass"] = foreign
                    rejected = bridge.call("liturgy", "day", calendar, date, invalid)["rows"][0]
                    self.assertIn("failed", rejected)
                    self.assertNotIn("events", rejected)

    async def test_day_compare_waits_for_layout_and_keeps_the_corresponding_unit(self) -> None:
        from lectern.app import TriptychApp
        from lectern.snapshot import _settle
        from lectern.surfaces.day import Day

        app = TriptychApp(start="day", intent={"calendar": "roman-1962", "date": "2026-10-25"})
        async with app.run_test(size=(80, 30)) as pilot:
            await _settle(app, pilot)
            day = app.query_one(Day)
            await pilot.press("i", "down", "down", "enter", "m")
            await _settle(app, pilot)
            await pilot.press("o", "v")
            await _settle(app, pilot)
            self.assertFalse((day.compared or {}).get("refused"))
            self.assertEqual(day.compare_current(), "compare/proper/collect")
            await pilot.press("i", "end", "enter")
            await _settle(app, pilot)
            self.assertEqual(day.compare_current(), day.compare_locations[-1][0])

    async def test_contents_preserves_its_unit_across_bilingual_reflow_and_share(self) -> None:
        from lectern.app import TriptychApp
        from lectern.snapshot import _settle
        from lectern.surfaces.propers import Propers
        from lectern.surface import shown
        from textual.widgets import Input

        app = TriptychApp(start="propers", intent={"calendar": "roman-1962", "mass": "pentecost"})
        async with app.run_test(size=(80, 30)) as pilot:
            await _settle(app, pilot)
            propers = app.query_one(Propers)
            self.assertEqual(propers.ordinary_language, "en")
            chosen = propers.navigation.entries[3][0]
            await pilot.press("i", "down", "down", "down", "down", "enter")
            await _settle(app, pilot)
            box, text = propers.query_one("#propers-reading"), propers.query_one("#propers-text")
            self.assertEqual(propers.navigation.current(box, text), chosen)
            await pilot.press("B")
            await _settle(app, pilot)
            self.assertEqual(propers.navigation.current(box, text), chosen)
            await pilot.press("u")
            await _settle(app, pilot)
            self.assertIn("location=proper%2Froman-1962%2Fpentecost%2F004", app.clipboard)
            await pilot.press("escape", "slash")
            await _settle(app, pilot)
            self.assertTrue(propers.query_one("#propers-query", Input).has_focus)
            self.assertTrue(shown(app.focused))

    async def test_last_contents_target_survives_the_scroll_boundary(self) -> None:
        from lectern.app import TriptychApp
        from lectern.snapshot import _settle
        from lectern.surfaces.propers import Propers

        app = TriptychApp(start="propers", intent={"calendar": "postconciliar", "mass": "transfiguration-lord"})
        async with app.run_test(size=(120, 40)) as pilot:
            await _settle(app, pilot)
            propers = app.query_one(Propers)
            propers.comparison = {"dimension": "lectionary-cycle", "primary": "A", "peer": "B"}
            propers.again()
            await _settle(app, pilot)
            wanted = propers.navigation.entries[-1][0]
            await pilot.press("i", "end", "enter")
            await _settle(app, pilot)
            self.assertEqual(propers.navigation.current(propers.query_one("#propers-reading"),
                                                       propers.query_one("#propers-text")), wanted)
            await pilot.press("u")
            await _settle(app, pilot)
            self.assertIn("location=" + wanted.replace("/", "%2F"), app.clipboard)

    async def test_a_day_link_preserves_its_semantic_reading_in_propers(self) -> None:
        from lectern.app import TriptychApp
        from lectern.snapshot import _settle
        from lectern.surfaces.day import Day
        from lectern.surfaces.propers import Propers

        app = TriptychApp(start="day", intent={"calendar": "roman-1962", "date": "2026-05-24"})
        async with app.run_test(size=(120, 40)) as pilot:
            await _settle(app, pilot)
            day = app.query_one(Day)
            day.orations = "en"
            day.bible = "clementine-vulgate"
            day.text_display = "latin-and-selected"
            day.ordinary = True
            day.ordinary_language = "la"
            day.selection()["witness"] = "edition.edward-caswall.lyra-catholica.london-1849"
            day.load()
            await _settle(app, pilot)
            day.action_propers()
            await _settle(app, pilot)
            propers = app.query_one(Propers)
            self.assertEqual(propers.reading[:2], ("roman-1962", "pentecost"))
            state = propers.view["state"]
            self.assertEqual((state["orations"], state["bible"], state["ordinaryLang"], state["textDisplay"]),
                             ("en", "clementine-vulgate", "la", "latin-and-selected"))
            self.assertEqual(state["witness"], day.selection()["witness"])
            self.assertTrue(state["ordinary"])


if __name__ == "__main__":
    unittest.main()
