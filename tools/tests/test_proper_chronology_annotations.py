#!/usr/bin/env python3
"""The proper chronology publication projection is complete and stable."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "proper-chronology"
sys.path.insert(0, str(ROOT / "scripts"))

import _chronology as corpus  # noqa: E402
import _proper_chronology as chronology  # noqa: E402

COLLECTION = "liturgy/roman-rite/1962/propers"
FIFTEENTH = f"{COLLECTION}/temporal/55-fifteenth-after-pentecost"
FOURTEENTH = f"{COLLECTION}/temporal/54-fourteenth-after-pentecost"
TRINITY = f"{COLLECTION}/temporal/39-trinity-sunday"
EIGHTH = f"{COLLECTION}/temporal/48-eighth-after-pentecost"
NINTH = f"{COLLECTION}/temporal/49-ninth-after-pentecost"
NATIVITY_OCTAVE = f"{COLLECTION}/temporal/07-sunday-within-octave-of-nativity"


class AnnotationProjectionTests(unittest.TestCase):
    def run_command(
        self, command: str, *arguments: str
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(TOOL), command, *arguments],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def run_tool(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return self.run_command("annotations", *arguments)

    def payload(self, document: str = FIFTEENTH) -> dict:
        done = self.run_tool("--document", document, "--format", "json")
        self.assertEqual(done.returncode, 0, done.stderr)
        return json.loads(done.stdout)

    def test_proper_55_is_grouped_without_collapsing_its_candidates(self) -> None:
        payload = self.payload()
        by_key = {element["key"]: element for element in payload["elements"]}
        dossier = chronology.dossier(FIFTEENTH)

        self.assertEqual(len(by_key), 7)
        self.assertEqual(by_key["introit"]["groups"][0]["status"], "preferred")
        self.assertEqual(
            by_key["introit"]["groups"][0]["claims"][0]["display_label"],
            "Before c. 165 B.C.",
        )

        epistle = by_key["epistle"]["groups"]
        self.assertEqual([group["relation"] for group in epistle],
                         ["composition"])
        self.assertIn(epistle[0]["status"], ("preferred", "disputed"))

        projected = [
            claim
            for element in payload["elements"]
            for group in element["groups"]
            for claim in group["claims"]
        ]
        source = [
            claim
            for element in dossier.elements
            for claim in element.publication_claims
        ]
        self.assertEqual(
            sorted((claim["relation"], claim["subject"], claim["label"],
                    claim["disposition"], claim["profile"])
                   for claim in projected),
            sorted((claim.relation, claim.subject, claim.label, claim.disposition)
                   + (claim.profile,) for claim in source),
        )
        disputed = [
            claim for claim in projected if claim["disposition"] == "disputed"
        ]
        self.assertGreaterEqual(len(disputed), 4)
        self.assertIn("(1 and 2 Corinthians; Galatians), 56",
                      {claim["label"] for claim in projected})

    def test_gospel_has_a_narrated_event_group(self) -> None:
        payload = self.payload()
        gospel = next(
            element for element in payload["elements"]
            if element["key"] == "gospel"
        )
        self.assertEqual(
            [group["relation"] for group in gospel["groups"]],
            ["composition", "narrated-event"],
        )

    def test_gospel_without_an_event_gets_an_explicit_gap(self) -> None:
        dossier = chronology.dossier(FIFTEENTH)
        gospel = dossier.element("gospel")
        self.assertIsNotNone(gospel)
        composition = tuple(
            claim
            for claim in gospel.publication_claims
            if claim.relation == "composition"
        )
        without_event = chronology.Dossier(
            document=dossier.document,
            calendar=dossier.calendar,
            mass=dossier.mass,
            system=dossier.system,
            profile=dossier.profile,
            state=dossier.state,
            reason=dossier.reason,
            elements=(
                gospel._replace(
                    claims=composition,
                    publication_claims=composition,
                ),
            ),
        )
        projected = chronology.annotations(without_event).elements[0]
        event = projected.groups[1]
        self.assertEqual(event.relation, "narrated-event")
        self.assertEqual(event.status, "research-pending")
        self.assertEqual(event.claims, ())
        self.assertIn("no event date", event.reason)

    def test_partial_locus_gospel_event_is_a_nonuniform_gap(self) -> None:
        payload = self.payload(NATIVITY_OCTAVE)
        gospel = next(
            element for element in payload["elements"]
            if element["key"] == "gospel"
        )
        event = next(
            group for group in gospel["groups"]
            if group["relation"] == "narrated-event"
        )
        self.assertEqual(event["status"], chronology.NONUNIFORM)
        self.assertEqual(event["claims"], [])
        self.assertIn(
            "No single narrated-event assertion applies across every cited locus",
            event["reason"],
        )
        rendered = self.run_tool(
            "--document", NATIVITY_OCTAVE, "--format", "text"
        )
        self.assertEqual(rendered.returncode, 0, rendered.stderr)
        self.assertIn(
            "Event -- No single narrated-event assertion applies across every "
            "cited locus.",
            rendered.stdout,
        )
        self.assertNotIn("No narrated-event date in the chronology corpus",
                         rendered.stdout)

    def test_source_and_display_labels_remain_distinct(self) -> None:
        payload = self.payload()
        gospel = next(
            element for element in payload["elements"]
            if element["key"] == "gospel"
        )
        relative = next(
            claim for claim in gospel["groups"][0]["claims"]
            if claim["precision"] == "relative"
        )
        self.assertEqual(
            relative["label"],
            "before the end of the Roman imprisonment, when the Acts was finished",
        )
        self.assertEqual(
            relative["display_label"],
            "Before the end of the Roman imprisonment, when the Acts was finished",
        )
        self.assertEqual(relative["date"],
                         "before the Acts of the Apostles, and therefore before "
                         "the end of the Roman imprisonment, and not as late as "
                         "the destruction of Jerusalem")
        self.assertEqual(relative["profile"], "catholic-traditional-v1")
        text = self.run_tool("--document", FIFTEENTH, "--format", "text")
        self.assertEqual(text.returncode, 0, text.stderr)
        self.assertIn(
            "Before the end of the Roman imprisonment, when the Acts was finished.",
            text.stdout,
        )
        self.assertNotIn("imprisonment…", text.stdout)

    def test_century_notation_never_prints_its_unasserted_endpoints(self) -> None:
        cases = {
            "Job.1.1": (
                "Probably sometime between the seventh and fifth centuries B.C.",
                "B.C. 700–401",
            ),
            "2Esd.12.11": (
                "If the list is authorial, the author's work dates to the first "
                "decades of the fourth century B.C.",
                "B.C. 400–301",
            ),
        }
        for locus, (expected, forbidden) in cases.items():
            with self.subTest(locus=locus):
                _status, _reason, claims = chronology._claims_at(
                    locus, None, None
                )
                claim = next(
                    claim
                    for claim in claims
                    if claim.date in ("700 B.C. to 401 B.C.",
                                      "400 B.C. to 301 B.C.")
                )
                rendered = chronology.concise_display_label(claim)
                self.assertEqual(rendered, expected)
                self.assertNotEqual(rendered, forbidden)

        # Proper 55's actual year ranges remain concise because their source
        # labels state years; they are not whole-century notation envelopes.
        displays = {
            claim["display_label"]
            for element in self.payload()["elements"]
            for group in element["groups"]
            for claim in group["claims"]
        }
        self.assertIn("A.D. 49–50", displays)
        self.assertIn("c. A.D. 90–100", displays)

    def test_record_header_scopes_the_generated_display_exception(self) -> None:
        rendered = chronology.render(chronology.dossier(FIFTEENTH))
        header = rendered.partition("\nschema = ")[0]
        self.assertIn(
            "only value a manually authored\n# guide may display", header
        )
        self.assertIn("sole permitted display exception", header)
        self.assertIn("proper-chronology annotations", header)
        self.assertIn("retains the raw\n# `label` and claim `profile`", header)
        self.assertIn("No manual consumer may mint or edit one", header)
        self.assertIn("`claims` are the full audit union", header)
        self.assertIn("`publication_claims`", header)
        self.assertIn("exact across-all-loci intersection", header)

    def test_omitted_profile_records_the_effective_corpus_default(self) -> None:
        expected = corpus.load().default_profile
        dossier = chronology.dossier(FIFTEENTH)
        self.assertEqual(dossier.profile, expected)

        record = self.run_command("record", "--document", FIFTEENTH)
        self.assertEqual(record.returncode, 0, record.stderr)
        self.assertEqual(tomllib.loads(record.stdout)["profile"], expected)

        projection = self.payload()
        self.assertEqual(projection["profile"], expected)
        self.assertNotEqual(projection["profile"], "")

    def test_explicit_leaf_profile_is_preserved(self) -> None:
        selected = "catholic-traditional-v1"
        dossier = chronology.dossier(FIFTEENTH, profile=selected)
        self.assertEqual(dossier.profile, selected)
        self.assertEqual(
            {claim.profile for element in dossier.elements for claim in element.claims},
            {selected},
        )
        done = self.run_tool(
            "--document", FIFTEENTH, "--profile", selected, "--format", "json"
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(json.loads(done.stdout)["profile"], selected)
        record = self.run_command(
            "record", "--document", FIFTEENTH, "--profile", selected
        )
        self.assertEqual(record.returncode, 0, record.stderr)
        self.assertEqual(tomllib.loads(record.stdout)["profile"], selected)

    def test_loci_reports_the_effective_profile_in_both_formats(self) -> None:
        default = corpus.load().default_profile
        omitted = self.run_command("loci", "--document", FIFTEENTH, "--json")
        self.assertEqual(omitted.returncode, 0, omitted.stderr)
        self.assertEqual(json.loads(omitted.stdout)["profile"], default)
        omitted_plain = self.run_command("loci", "--document", FIFTEENTH)
        self.assertEqual(omitted_plain.returncode, 0, omitted_plain.stderr)
        self.assertEqual(
            omitted_plain.stdout.splitlines()[0], f"profile: {default}"
        )

        selected = "catholic-traditional-v1"
        explicit = self.run_command(
            "loci", "--document", FIFTEENTH, "--profile", selected, "--json"
        )
        self.assertEqual(explicit.returncode, 0, explicit.stderr)
        self.assertEqual(json.loads(explicit.stdout)["profile"], selected)

        plain = self.run_command(
            "loci", "--document", FIFTEENTH, "--profile", selected
        )
        self.assertEqual(plain.returncode, 0, plain.stderr)
        self.assertEqual(plain.stdout.splitlines()[0], f"profile: {selected}")

    def test_nondefault_profiles_are_inspection_only_for_artifacts(self) -> None:
        selected = "catholic-traditional-v1"
        default = corpus.load().default_profile
        self.assertNotEqual(selected, default)
        for command in ("record", "annotations"):
            for action in ("--write", "--check"):
                with self.subTest(command=command, action=action):
                    # The deliberately nonexistent provider makes this safe
                    # even if the guard regresses: no live leaf can be written.
                    done = self.run_command(
                        command,
                        "--document", FIFTEENTH,
                        "--provider", "definitely-missing",
                        "--profile", selected,
                        action,
                    )
                    self.assertNotEqual(done.returncode, 0)
                    self.assertIn(f"profile '{selected}' is inspection-only",
                                  done.stderr)
                    self.assertIn(f"default profile '{default}'", done.stderr)

    def test_help_states_the_fixed_publication_profile_policy(self) -> None:
        for command in ("record", "annotations"):
            with self.subTest(command=command):
                done = self.run_command(command, "--help")
                self.assertEqual(done.returncode, 0, done.stderr)
                help_text = " ".join(done.stdout.split())
                self.assertIn("non-default profiles are inspection-only",
                              help_text)
                self.assertIn("default-profile", help_text)

    def test_audit_claims_and_element_wide_publication_intersection_are_distinct(self) -> None:
        trinity = chronology.dossier(TRINITY).element("introit")
        self.assertIsNotNone(trinity)
        self.assertEqual(len(trinity.claims), 2)
        self.assertEqual(trinity.publication_claims, ())
        self.assertEqual(trinity.status, "composition-only")
        self.assertEqual(trinity.publication_status, chronology.NONUNIFORM)
        self.assertIn("element-wide Date cell", trinity.publication_reason)

        gradual = chronology.dossier(EIGHTH).element("gradual")
        self.assertIsNotNone(gradual)
        subjects = {claim.subject for claim in gradual.claims}
        self.assertIn("israel.monarchy.david-flight-from-absalom", subjects)
        self.assertIn("israel.monarchy.david-in-the-desert-of-maon", subjects)
        self.assertIn("israel.exile.first-captivity", subjects)
        publication_subjects = {
            claim.subject for claim in gradual.publication_claims
        }
        self.assertIn(
            "israel.monarchy.david-flight-from-absalom", publication_subjects
        )
        self.assertNotIn(
            "israel.monarchy.david-in-the-desert-of-maon", publication_subjects
        )
        self.assertNotIn("israel.exile.first-captivity", publication_subjects)
        self.assertEqual(gradual.status, "dated")
        absalom = next(
            claim
            for claim in gradual.publication_claims
            if claim.subject == "israel.monarchy.david-flight-from-absalom"
        )
        self.assertEqual(
            {(reach.locus, reach.scope) for reach in absalom.reaches},
            {("Ps.30.3", "Ps.30"), ("Ps.70.1", "Ps.62 Ps.70")},
        )

        gospel = chronology.dossier(NINTH).element("gospel")
        self.assertIsNotNone(gospel)
        self.assertEqual(
            {claim.relation for claim in gospel.claims},
            {"composition", "prophetic-referent"},
        )
        self.assertEqual(
            {claim.relation for claim in gospel.publication_claims},
            {"composition"},
        )
        self.assertEqual(gospel.status, "dated")
        self.assertEqual(gospel.publication_status, "composition-only")

    def test_attestation_only_status_survives_publication_projection(self) -> None:
        dossier = chronology.dossier(FIFTEENTH)
        introit = dossier.element("introit")
        self.assertIsNotNone(introit)
        attestation = introit.claims[0]._replace(
            relation="textual-attestation"
        )
        held, status, reason = chronology._common_claims(
            [(attestation.reaches[0].locus, "attestation-only", "", [attestation])]
        )
        self.assertEqual(status, "attestation-only")
        element = introit._replace(
            status="attestation-only",
            reason=reason,
            claims=held,
            publication_status=status,
            publication_reason=reason,
            publication_claims=held,
        )
        projection = chronology.annotations(
            dossier._replace(elements=(element,))
        ).elements[0]
        self.assertEqual(projection.status, "attestation-only")
        self.assertEqual(projection.groups[0].relation, "textual-attestation")

    def test_record_preserves_full_audit_and_reach_provenance(self) -> None:
        parsed = tomllib.loads(chronology.render(chronology.dossier(EIGHTH)))
        self.assertEqual(parsed["schema"], 2)
        gradual = next(
            element for element in parsed["elements"]
            if element["key"] == "gradual"
        )
        self.assertEqual(gradual["status"], "dated")
        self.assertEqual(gradual["publication_status"], "dated")
        self.assertIn(
            "israel.monarchy.david-in-the-desert-of-maon",
            {claim["subject"] for claim in gradual["claims"]},
        )
        absalom = next(
            claim for claim in gradual["publication_claims"]
            if claim["subject"]
            == "israel.monarchy.david-flight-from-absalom"
        )
        self.assertEqual(
            {
                (reach["locus"], reach["scope"], reach["inherited"])
                for reach in absalom["reaches"]
            },
            {
                ("Ps.30.3", "Ps.30", True),
                ("Ps.70.1", "Ps.62 Ps.70", True),
            },
        )

        ninth = tomllib.loads(chronology.render(chronology.dossier(NINTH)))
        gospel = next(
            element for element in ninth["elements"]
            if element["key"] == "gospel"
        )
        self.assertIn(
            "prophetic-referent",
            {claim["relation"] for claim in gospel["claims"]},
        )
        self.assertNotIn(
            "prophetic-referent",
            {claim["relation"] for claim in gospel["publication_claims"]},
        )

    def test_annotation_json_carries_every_publication_reach(self) -> None:
        payload = self.payload(EIGHTH)
        gradual = next(
            element for element in payload["elements"]
            if element["key"] == "gradual"
        )
        absalom = next(
            claim
            for group in gradual["groups"]
            for claim in group["claims"]
            if claim["subject"]
            == "israel.monarchy.david-flight-from-absalom"
        )
        self.assertEqual(
            {
                (reach["locus"], reach["scope"], reach["inherited"])
                for reach in absalom["reaches"]
            },
            {
                ("Ps.30.3", "Ps.30", True),
                ("Ps.70.1", "Ps.62 Ps.70", True),
            },
        )

    def test_all_formats_are_byte_stable(self) -> None:
        for output_format in ("text", "json", "tex"):
            with self.subTest(format=output_format):
                first = self.run_tool(
                    "--document", FIFTEENTH, "--format", output_format
                )
                second = self.run_tool(
                    "--document", FIFTEENTH, "--format", output_format
                )
                self.assertEqual(first.returncode, 0, first.stderr)
                self.assertEqual(second.returncode, 0, second.stderr)
                self.assertEqual(first.stdout.encode(), second.stdout.encode())

    def test_tex_keeps_every_raw_claim_but_renders_the_display_label(self) -> None:
        payload = self.payload()
        done = self.run_tool("--document", FIFTEENTH, "--format", "tex")
        self.assertEqual(done.returncode, 0, done.stderr)
        rendered = done.stdout
        self.assertIn(
            r"\newcommand{\chronologyannotationclaim}[6]{#6}", rendered
        )
        self.assertIn(
            r"\newcommand{\chronologyannotationreach}[3]{}", rendered
        )
        self.assertIn(
            r"\newcommand{\chronologyannotationgroup}[3]{#3}", rendered
        )
        self.assertIn(
            r"\newcommand{\chronologyannotation}[1]{%", rendered
        )
        self.assertNotIn(r"\providecommand{\chronologyannotation", rendered)
        for element in payload["elements"]:
            self.assertEqual(
                rendered.count(
                    f"triptychchronologyannotation@{element['key']}\\endcsname"
                ),
                1,
            )
            for group in element["groups"]:
                for claim in group["claims"]:
                    raw = chronology.tex_escape(claim["label"])
                    display = chronology.tex_escape(claim["display_label"])
                    self.assertIn(f"{{{raw}}}{{{display}}}", rendered)

        # These are the exact compact forms that replace Proper 55's widest
        # copied source labels; all alternatives remain present above.
        self.assertIn("{A.D. 56}", rendered)
        self.assertIn(
            "{Before the end of the Roman imprisonment, when the Acts was finished}",
            rendered,
        )
        self.assertIn(
            "{composition}{catholic-traditional-v1}{disputed}", rendered
        )
        self.assertNotIn("B.C..", rendered)
        self.assertNotIn("imprisonment....", rendered)
        self.assertIn(
            "\\chronologyannotationgroup{narrated-event}{",
            rendered,
        )

        eighth = self.run_tool("--document", EIGHTH, "--format", "tex")
        self.assertEqual(eighth.returncode, 0, eighth.stderr)
        self.assertIn(
            r"\chronologyannotationreach{Ps.30.3}{Ps.30}{true}",
            eighth.stdout,
        )
        self.assertIn(
            r"\chronologyannotationreach{Ps.70.1}{Ps.62 Ps.70}{true}",
            eighth.stdout,
        )

    def test_textual_attestation_has_a_publication_label(self) -> None:
        self.assertEqual(
            chronology._relation_label("textual-attestation"),
            "Textual attestation",
        )

    def test_tex_escapes_every_argument_metacharacter(self) -> None:
        self.assertEqual(
            chronology.tex_escape(r"\{}#$%&_^~–—…"),
            (r"\textbackslash{}\{\}\#\$\%\&\_\textasciicircum{}"
             r"\textasciitilde{}-----..."),
        )

    def test_preferred_status_is_not_relabelled_disputed(self) -> None:
        payload = self.payload(FOURTEENTH)
        offertory = next(
            element for element in payload["elements"]
            if element["key"] == "offertory"
        )
        setting = next(
            group for group in offertory["groups"]
            if group["relation"] == "superscription-setting"
        )
        self.assertEqual(setting["relation"], "superscription-setting")
        self.assertEqual(setting["status"], "preferred")
        self.assertEqual(len(setting["claims"]), 1)

    def test_write_and_check_hold_the_generated_tex_exactly(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "src" / "gpt" / FIFTEENTH
            target.parent.mkdir(parents=True)
            shutil.copytree(ROOT / "src" / "gpt" / FIFTEENTH, target)
            (root / "src" / "sources").symlink_to(ROOT / "src" / "sources")
            annotation_file = target / chronology.ANNOTATIONS_RECORD
            annotation_file.unlink(missing_ok=True)

            default = corpus.load().default_profile
            common = (
                "--root", str(root), "--provider", "gpt",
                "--document", FIFTEENTH, "--profile", default,
            )
            missing = self.run_tool(*common, "--check")
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("does not exist", missing.stderr)

            written = self.run_tool(*common, "--write")
            self.assertEqual(written.returncode, 0, written.stderr)
            self.assertTrue(annotation_file.is_file())
            expected = self.run_tool(
                "--document", FIFTEENTH, "--format", "tex"
            )
            self.assertEqual(annotation_file.read_bytes(),
                             expected.stdout.encode())

            current = self.run_tool(*common, "--check")
            self.assertEqual(current.returncode, 0, current.stderr)

            # The sibling audit record has the same fixed publication-profile
            # contract, including when the default is stated explicitly.
            record_file = target / chronology.RECORD
            record_file.unlink(missing_ok=True)
            record_write = self.run_command("record", *common, "--write")
            self.assertEqual(record_write.returncode, 0, record_write.stderr)
            self.assertEqual(
                tomllib.loads(record_file.read_text(encoding="utf-8"))["profile"],
                default,
            )
            record_check = self.run_command("record", *common, "--check")
            self.assertEqual(record_check.returncode, 0, record_check.stderr)

            annotation_file.write_text(
                annotation_file.read_text(encoding="utf-8") + "% edited\n",
                encoding="utf-8",
            )
            drifted = self.run_tool(*common, "--check")
            self.assertNotEqual(drifted.returncode, 0)
            self.assertIn("not the current chronology annotation projection",
                          drifted.stderr)

    def test_non_tex_write_or_check_is_refused(self) -> None:
        for action in ("--write", "--check"):
            with self.subTest(action=action):
                done = self.run_tool(
                    "--document", FIFTEENTH, "--format", "json", action
                )
                self.assertNotEqual(done.returncode, 0)
                # --format json makes errors machine-readable.
                self.assertEqual(json.loads(done.stderr)["code"], "refused")


if __name__ == "__main__":
    unittest.main()
