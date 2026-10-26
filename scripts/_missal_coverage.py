"""Public, text-free Missal coverage shared by generators and audit commands.

Callers supply already resolved, publication-filtered units. This module never
resolves a calendar, grants publication rights, or infers target fidelity from
the existence of a body. Identity, occurrence, and witness counts are separate.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
from urllib.parse import quote, unquote
import tomllib

SCHEMA = "triptych-missal-coverage/v1"
UNIT_SCHEMA = "triptych-missal-unit-coverage/v1"
LANGUAGES = ("la", "en")
AVAILABILITIES = (
    "available", "not-publishable", "not-sourced", "unresolved",
    "inapplicable", "absent-in-witness",
)
RELATIONSHIPS = (
    "exact-target", "historical-antecedent", "study-translation",
    "bible-reconstruction", "unresolved",
)
COLLATIONS = ("collated", "uncollated", "not-applicable", "unresolved")


def identity(*parts: object) -> str:
    return ":".join(quote(str(part), safe="-._") for part in parts)


def relationship(row: dict) -> str:
    """Only source-declared relations establish fidelity; unknown stays unknown."""
    explicit = row.get("coverage_relationship")
    if explicit in RELATIONSHIPS:
        return explicit
    if row.get("rights") == "project-created":
        return "study-translation"
    relation = row.get("witness_relation") or row.get("relation")
    if relation == "antecedent":
        return "historical-antecedent"
    if relation == "own":
        return "exact-target"
    return "unresolved"


# A Latin body's own provenance record names how its words relate to the
# target edition. Only a relationship that is itself declared exact TO THE
# TARGET, and recorded as collated, is the target's wording: under the
# 2026-09-03 rule in guidance/propers-for-agents.md (words, never strings) such
# a projection is word-exact, so it counts as `exact-target`. An exact
# transcription of some other witness, an identified but uncollated body, or a
# body this calendar inherits from another one keeps its own, weaker relation.
LATIN_TARGET_RELATIONSHIPS = frozenset({"editorial-projection-exact-to-target"})
LATIN_COLLATIONS = {"collated": "collated", "identified": "uncollated",
                    "unresolved": "unresolved"}


def is_witness_state_body(latin: object) -> bool:
    """A source-validated, permitted body with an explicitly bounded witness claim.

    This maps the owning publication decision; it does not grant permission or
    verify a source record itself. Unknown/uncollated context stays inherited.
    """
    if not isinstance(latin, dict):
        return False
    context = latin.get("target_context") or {}
    provenance = latin.get("provenance") or {}
    publication = latin.get("publication") or {}
    from _proper_target_overrides import is_public_context
    return (is_public_context(context)
            and latin.get("withheld") is False
            and publication.get("status") == "permitted"
            and publication.get("basis") in {"public-domain", "project-created", "permission", "licensed"}
            and provenance.get("status") == "collated"
            and provenance.get("relationship") in LATIN_TARGET_RELATIONSHIPS)


def latin_evidence(latin: object, *, inherited: bool = False) -> dict:
    """Map one public Latin record to coverage terms without reading the text.

    `inherited` marks a body carried from another calendar's corpus (a
    recension's `text_from`). Its collation was made against that calendar's
    target, not this one, so it is uncollated here and never exact-target.
    """
    latin = latin if isinstance(latin, dict) else {}
    provenance = latin.get("provenance") if isinstance(latin.get("provenance"), dict) else {}
    publication = latin.get("publication") if isinstance(latin.get("publication"), dict) else {}
    basis = str(publication.get("basis") or "unresolved")
    if is_witness_state_body(latin):
        # Exact to the identified Bonn witness, without upgrading generic
        # pre-1955 dates or the nominal 1920 target to exact-target wording.
        return {"relationship": "unresolved", "collation": "collated",
                "publication_basis": basis}
    if inherited:
        return {"relationship": "unresolved", "collation": "uncollated",
                "publication_basis": basis}
    collation = LATIN_COLLATIONS.get(str(provenance.get("status") or ""), "unresolved")
    exact = (collation == "collated"
             and provenance.get("relationship") in LATIN_TARGET_RELATIONSHIPS)
    return {"relationship": "exact-target" if exact else "unresolved",
            "collation": collation, "publication_basis": basis}


# The typed reasons of a source-side translation absence, mapped to coverage
# availability. `no-exemplar` says no exact exemplar is bound to the slot, so
# the slot is not sourced; `rights-withheld` is an affirmative restriction.
# `witness-gap` stays `unresolved` in the Propers: their sidecars use it both
# for a checked absence or variant in the named witness and for an identity
# not yet established against it, and the reason alone cannot tell them apart.
ABSENCE_KIND_AVAILABILITY = {
    "rights-withheld": "not-publishable",
    "no-exemplar": "not-sourced",
    "witness-gap": "unresolved",
}


def source_absence(kinds: object) -> str | None:
    """One availability for a language's typed source-side absence reasons."""
    states = {ABSENCE_KIND_AVAILABILITY.get(str(kind), "unresolved")
              for kind in (kinds or ())}
    if not states:
        return None
    if "not-publishable" in states:
        return "not-publishable"
    return next(iter(states)) if len(states) == 1 else "unresolved"


def witness(row: dict, witnesses: dict) -> dict:
    source_id = str(row.get("source_id") or "")
    metadata = witnesses.get((row.get("lang"), source_id)) or witnesses.get(source_id) or {}
    canonical = str(metadata.get("source_id") or source_id)
    # Only identifiers on surviving public translation rows may be offered.
    # Metadata can identify a restricted artifact for internal resolution.
    aliases = sorted({source_id, canonical})
    declared = row
    if not any(row.get(key) for key in ("coverage_relationship", "witness_relation", "relation")) \
            and metadata.get("witness_relation"):
        # A witness row may declare its relation to this calendar's target once
        # for every body it supplies; an entry's own relation still wins.
        declared = dict(row, witness_relation=metadata["witness_relation"])
    return {
        "id": canonical or "project-created",
        "source_id": canonical,
        "label": str(metadata.get("label") or row.get("source_label") or
                     canonical or "This project"),
        "aliases": aliases,
        "relationship": relationship(declared),
        "collation": row.get("collation") if row.get("collation") in COLLATIONS
        else ("not-applicable" if row.get("relation") == "own" else "unresolved"),
        "publication_basis": str(row.get("rights") or "unresolved"),
    }


def absence(owner: dict, lang: str, kinds: object = None) -> str:
    """Classify an absence; export its class only, never its evidence.

    `kinds` are the typed source-side reasons the generator holds for this
    language (`no-exemplar`, `witness-gap`, `rights-withheld`). Without them
    the public projection is all there is, and its `unavailable` stays
    `unresolved`.
    """
    rows = (owner.get("unavailable_translations") or [])
    untranslated = owner.get("untranslated") or []
    if isinstance(untranslated, dict):
        untranslated = [untranslated]
    if isinstance(untranslated, list):
        rows = list(rows) + untranslated
    states = {row.get("state") for row in rows
              if isinstance(row, dict) and row.get("lang") == lang}
    latin = owner.get("latin") or {}
    if "rights-restricted" in states or (
        lang == "la" and latin.get("state") == "rights-restricted"
    ):
        return "not-publishable"
    typed = source_absence(kinds)
    if typed:
        return typed
    if "unavailable" in states:
        # The public state alone does not say why the body is unavailable.
        return "unresolved"
    if lang == "la" and (latin.get("withheld") or
                          latin.get("state") == "unavailable"):
        return "unresolved"
    if (owner.get("text_status") or {}).get("state") == "unavailable":
        return "unresolved"
    return "not-sourced"


def unit(owner: dict, *, target_id: str, occurrence_id: str,
         witnesses: dict | None = None, cycle_family: str | None = None,
         cycle: str = "all", component: str | None = None,
         latin_relation: str | None = None,
         latin_inherited: bool = False,
         translation_relation: str | None = None,
         ordinary_absences: dict[str, str] | None = None,
         absence_kinds: dict[str, list[str]] | None = None) -> dict:
    """Classify one body or Scripture owner after its publication filter.

    The Latin body's relationship, collation and publication basis come from
    its own `latin` record (`latin_evidence`); `latin_relation` overrides only
    the relationship, for a caller that already holds a classified report.
    """
    witnesses = witnesses or {}
    if component is None:
        component = "scripture" if owner.get("source") == "scripture" else "proper-body"
    body_languages = None
    if component == "scripture":
        scoped = set()
        for row in owner.get("untranslated") or []:
            target = row.get("target") or {}
            prefix = unquote(target_id.split(":")[0]).split(":")[:2]
            expected = identity(identity(*prefix, target.get("mass"), target.get("form_id"),
                                         target.get("proper"), target.get("occurrence")),
                                cycle_family or "all", target.get("cycle"))
            if target.get("extent") == "body" and expected == target_id:
                scoped.add(row.get("lang"))
        if scoped:
            body_languages = sorted(scoped)
            component = "proper-body"
    languages = []
    for lang in LANGUAGES:
        published = [row for row in owner.get("translations") or []
                     if row.get("lang") == lang and row.get("text")]
        offered = {}
        witness_bodies = {}
        for row in published:
            projection = dict(row)
            if translation_relation and "coverage_relationship" not in projection:
                projection["coverage_relationship"] = translation_relation
            one = witness(projection, witnesses)
            key = one["id"]
            if key in witness_bodies and witness_bodies[key] != row["text"]:
                raise ValueError(f"conflicting bodies for canonical Missal witness {key}")
            witness_bodies[key] = row["text"]
            if key in offered:
                previous = offered[key]
                # Aliases are one witness; conflicting grades must not be upgraded.
                previous["aliases"] = sorted(set(previous["aliases"] + one["aliases"]))
                if previous["relationship"] != one["relationship"]:
                    previous["relationship"] = "unresolved"
                if previous["publication_basis"] != one["publication_basis"]:
                    previous["publication_basis"] = "unresolved"
                if previous["collation"] != one["collation"]:
                    previous["collation"] = "unresolved"
            else:
                offered[key] = one
        source_body = lang == "la" and bool(owner.get("text"))
        relations = {one["relationship"] for one in offered.values()}
        rights = {one["publication_basis"] for one in offered.values()}
        collations = {one["collation"] for one in offered.values()}
        if source_body:
            # Text was admitted upstream; that alone identifies neither its
            # relation to the target nor its rights basis. Its record does.
            evidence = latin_evidence(owner.get("latin"), inherited=latin_inherited)
            relations.add(latin_relation or evidence["relationship"])
            rights.add(evidence["publication_basis"])
            collations.add(evidence["collation"])
        if component == "scripture" or (body_languages is not None and lang not in body_languages):
            availability, relation, right = "unresolved", "bible-reconstruction", "unresolved"
        elif source_body or offered:
            availability = "available"
            relation = next(iter(relations)) if len(relations) == 1 else "unresolved"
            right = next(iter(rights)) if len(rights) == 1 else "unresolved"
        else:
            availability = (ordinary_absences or {}).get(lang) or absence(
                owner, lang, (absence_kinds or {}).get(lang))
            relation, right = "unresolved", "unresolved"
            if availability == "not-publishable":
                right = "restricted"
        languages.append({
            "lang": lang, "availability": availability,
            "relationship": relation, "publication_basis": right,
            "collation": next(iter(collations)) if len(collations) == 1 else "unresolved",
            "witnesses": sorted(offered.values(), key=lambda row: row["id"]),
        })
    result = {
        "schema": UNIT_SCHEMA, "target_id": target_id,
        "occurrence_id": occurrence_id, "component": component,
        "cycle_family": cycle_family, "cycle": cycle, "languages": languages,
    }
    if body_languages is not None:
        result["body_languages"] = body_languages
    if component != "scripture" and owner.get("citations"):
        result["scripture_component"] = {
            "target_id": identity(target_id, "scripture"),
            "occurrence_id": identity(occurrence_id, "scripture"),
            "relationship": "bible-reconstruction", "availability": "unresolved",
            "publication_basis": "unresolved",
        }
    validate_body_languages(result)
    return result


def validate_body_languages(unit: dict) -> None:
    """The optional language-only body scope is closed and additive."""
    if "body_languages" not in unit:
        return
    if (unit["body_languages"] != ["en"]
            or unit.get("component") != "proper-body"
            or not isinstance(unit.get("scripture_component"), dict)):
        raise ValueError("language-only body coverage requires body_languages=['en'] and a separate Scripture component")


def summarize(units: list[dict], scope: str) -> dict:
    """Aggregate typed unit reports; repetitions never increase target counts."""
    by_occurrence = {}
    for one in units:
        if one.get("schema") != UNIT_SCHEMA:
            raise ValueError("Missal coverage unit has an unsupported schema")
        validate_body_languages(one)
        key = one["occurrence_id"]
        if key in by_occurrence and one != by_occurrence[key]:
            raise ValueError(f"conflicting Missal coverage occurrence {key}")
        by_occurrence[key] = one
    units = list(by_occurrence.values())
    bodies = [one for one in units if one["component"] != "scripture"]
    scripture = [one for one in units if one["component"] == "scripture"]
    mixed = [one for one in bodies if one.get("scripture_component")]
    languages = []
    alternatives = set()
    for lang in LANGUAGES:
        language_bodies = [one for one in bodies
                           if lang in one.get("body_languages", LANGUAGES)]
        availability = Counter({key: 0 for key in AVAILABILITIES})
        relations = Counter({key: 0 for key in RELATIONSHIPS})
        collations = Counter({key: 0 for key in COLLATIONS})
        available_targets, exact_targets = set(), set()
        offered: dict[str, dict] = {}
        exact_occurrences = 0
        for one in language_bodies:
            row = next(row for row in one["languages"] if row["lang"] == lang)
            if row["availability"] not in AVAILABILITIES or row["relationship"] not in RELATIONSHIPS:
                raise ValueError("Missal coverage unit has an unknown classification")
            availability[row["availability"]] += 1
            relations[row["relationship"]] += 1
            collations[row["collation"]] += 1
            if row["availability"] == "available":
                available_targets.add(one["target_id"])
                if row["relationship"] == "exact-target" or any(
                    witness["relationship"] == "exact-target" for witness in row["witnesses"]
                ):
                    exact_targets.add(one["target_id"])
                    exact_occurrences += 1
            for item in row["witnesses"]:
                alternatives.add((one["target_id"], lang, item["id"]))
                entry = offered.setdefault(item["id"], {
                    "id": item["id"], "source_id": item["source_id"],
                    "label": item["label"], "aliases": set(), "target_ids": set(),
                    "occurrence_ids": set(), "relationships": set(), "publication_bases": set(),
                    "collations": set(),
                })
                entry["aliases"].update(item["aliases"])
                entry["target_ids"].add(one["target_id"])
                entry["occurrence_ids"].add(one["occurrence_id"])
                entry["relationships"].add(item["relationship"])
                entry["publication_bases"].add(item["publication_basis"])
                entry["collations"].add(item["collation"])
        witnesses = []
        for item in sorted(offered.values(), key=lambda row: row["id"]):
            witnesses.append({
                key: sorted(value) if isinstance(value, set) else value
                for key, value in item.items() if key not in {"target_ids", "occurrence_ids"}
            } | {"targets": len(item["target_ids"]),
                 "available_targets": len(item["target_ids"]),
                 "occurrences": len(item["occurrence_ids"]),
                 "available": len(item["occurrence_ids"])})
        languages.append({
            "lang": lang, "targets": len({one["target_id"] for one in language_bodies}),
            "occurrences": len(language_bodies), "available": availability["available"],
            "available_targets": len(available_targets),
            "exact_target": exact_occurrences, "exact_target_targets": len(exact_targets),
            "scripture_targets": len({one["target_id"] for one in scripture} | {
                one["scripture_component"]["target_id"] for one in mixed
            }),
            "scripture_occurrences": len(scripture) + len(mixed),
            "mixed_targets": len({one["target_id"] for one in mixed
                                  if lang in one.get("body_languages", LANGUAGES)}),
            "mixed_occurrences": sum(lang in one.get("body_languages", LANGUAGES)
                                     for one in mixed),
            "availability": dict(availability), "relationships": dict(relations),
            "collations": dict(collations),
            "witnesses": witnesses,
        })
    return {
        "schema": SCHEMA, "scope": scope,
        "denominator": "represented-units",
        "count_basis": {
            "canonical_targets": "distinct source-owned targets within this recension",
            "occurrences": "appointed units, including distinct cycle owners",
            "witness_alternatives": "distinct published translation witnesses per target and language",
        },
        "counts": {"canonical_targets": len({one["target_id"] for one in units}),
                   "occurrences": len(units), "witness_alternatives": len(alternatives)},
        "languages": languages,
    }


FILE_CONSTANTS = ("count_basis", "denominator")


def nested(report: dict) -> dict:
    """A summary nested inside a file whose own report states its constants.

    `count_basis` and `denominator` do not vary between summaries; the
    file-level report states them once instead of once per Mass.
    """
    return {key: value for key, value in report.items() if key not in FILE_CONSTANTS}


def proper_units(mass: dict) -> list[dict]:
    result = []
    for proper in mass.get("propers") or []:
        if isinstance(proper.get("coverage"), dict):
            result.append(proper["coverage"])
        for family in ("cycles", "weekday_cycles"):
            for owner in (proper.get(family) or {}).values():
                if isinstance(owner.get("coverage"), dict):
                    result.append(owner["coverage"])
    return result


def validate_summary(report: object) -> None:
    """Reject a drifting accounting partition at the CLI composition boundary."""
    if not isinstance(report, dict) or report.get("schema") != SCHEMA:
        raise ValueError("unsupported Missal coverage summary")
    def count(value: object) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("Missal coverage counts must be nonnegative integers")
        return value
    counts = report.get("counts")
    if not isinstance(counts, dict) or set(counts) != {
        "canonical_targets", "occurrences", "witness_alternatives"
    }:
        raise ValueError("Missal coverage summary has no exact counting units")
    for value in counts.values():
        count(value)
    if counts["canonical_targets"] > counts["occurrences"]:
        raise ValueError("canonical targets exceed occurrences")
    languages = report.get("languages")
    if not isinstance(languages, list) or [row.get("lang") for row in languages] != list(LANGUAGES):
        raise ValueError("Missal coverage summary must declare Latin and English")
    witness_alternatives = 0
    for row in languages:
        for field in ("targets", "occurrences", "available", "available_targets",
                      "exact_target", "exact_target_targets", "scripture_targets",
                      "scripture_occurrences", "mixed_targets", "mixed_occurrences"):
            count(row.get(field))
        for field, keys in (("availability", AVAILABILITIES), ("relationships", RELATIONSHIPS),
                            ("collations", COLLATIONS)):
            values = row.get(field)
            if not isinstance(values, dict) or set(values) != set(keys):
                raise ValueError(f"Missal coverage {field} has unknown or missing states")
            if sum(count(value) for value in values.values()) != row["occurrences"]:
                raise ValueError(f"Missal coverage {field} does not partition occurrences")
        if row["available"] != row["availability"]["available"] or not (
            row["exact_target"] <= row["available"] <= row["occurrences"]
            and row["exact_target_targets"] <= row["available_targets"] <= row["targets"]
            and row["available_targets"] <= row["available"]
            and row["mixed_occurrences"] <= min(row["occurrences"], row["scripture_occurrences"])
            and row["mixed_targets"] <= min(row["targets"], row["scripture_targets"])
            and row["occurrences"] + row["scripture_occurrences"] - row["mixed_occurrences"] == counts["occurrences"]
            and row["targets"] + row["scripture_targets"] - row["mixed_targets"] == counts["canonical_targets"]
        ):
            raise ValueError("Missal coverage numerator or denominator is inconsistent")
        witnesses = row.get("witnesses")
        if not isinstance(witnesses, list):
            raise ValueError("Missal coverage witness summary must be an array")
        seen = set()
        for witness in witnesses:
            if not isinstance(witness, dict) or not isinstance(witness.get("id"), str) or not witness["id"]:
                raise ValueError("Missal coverage witness requires a nonempty ID")
            if witness["id"] in seen:
                raise ValueError("duplicate Missal coverage witness")
            seen.add(witness["id"])
            for field in ("targets", "available_targets", "occurrences", "available"):
                count(witness.get(field))
            if not (
                witness["targets"] == witness["available_targets"] <= row["available_targets"]
                and witness["occurrences"] == witness["available"] <= row["available"]
                and witness["targets"] <= witness["occurrences"]
            ):
                raise ValueError("Missal witness coverage exceeds available units")
            for field, allowed in (("relationships", set(RELATIONSHIPS)), ("collations", set(COLLATIONS))):
                values = witness.get(field)
                if not isinstance(values, list) or not values or len(values) != len(set(values)) or not set(values) <= allowed:
                    raise ValueError(f"invalid Missal witness {field}")
            for field in ("aliases", "publication_bases"):
                values = witness.get(field)
                if not isinstance(values, list) or not values or any(not isinstance(value, str) for value in values) or len(values) != len(set(values)):
                    raise ValueError(f"invalid Missal witness {field}")
            witness_alternatives += witness["targets"]
    if witness_alternatives != counts["witness_alternatives"]:
        raise ValueError("Missal witness alternatives do not partition canonical witness targets")


def expectations(path: Path, calendar: str, masses: list[dict]) -> dict:
    """Join a separately sourced heterogeneous inventory, never invent its extent."""
    if not path.exists():
        return {"state": "unresolved", "reason": "expected-inventory-not-recorded",
                "slices": [], "targets": [], "boundaries": []}
    document = tomllib.loads(path.read_text(encoding="utf-8"))
    if document.get("schema") != "triptych-missal-expected-targets/v1":
        raise ValueError("unsupported expected Missal target inventory schema")
    kinds = {"celebration", "commemoration", "common", "cycle", "preface",
             "ordinary-option", "form", "exceptional-rite", "exceptional-rite-unit",
             "prayer-set", "collect-category", "form-referral", "text-slot"}
    slice_ids = set()
    if not isinstance(document.get("targets"), list):
        raise ValueError("expected Missal inventory requires targets array")
    if any(not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]
           for row in document["targets"]):
        raise ValueError("expected Missal targets require nonempty IDs")
    inventory_targets = {row["id"]: row for row in document["targets"]}
    for section in ("slices", "targets", "boundaries"):
        if not isinstance(document.get(section), list):
            raise ValueError(f"expected Missal inventory requires {section} array")
        ids = set()
        for row in document[section]:
            if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
                raise ValueError(f"expected Missal {section} require nonempty IDs")
            if row["id"] in ids:
                raise ValueError(f"duplicate expected Missal {section} ID {row['id']}")
            ids.add(row["id"])
            if section == "slices":
                required = ("calendar", "recension_id", "territory", "date_range", "basis")
                if any(not isinstance(row.get(key), str) or not row[key] for key in required):
                    raise ValueError("expected Missal slice omits scope or evidence basis")
                if row.get("enumeration_state") not in {"complete-within-slice", "partial", "unresolved"}:
                    raise ValueError("unknown expected Missal enumeration state")
                for field in ("source_refs", "languages"):
                    values = row.get(field)
                    if not isinstance(values, list) or not values or any(
                        not isinstance(value, str) or not value for value in values
                    ) or len(values) != len(set(values)):
                        raise ValueError(f"expected Missal slice requires unique {field}")
            else:
                if row.get("slice_id") not in slice_ids:
                    raise ValueError("expected Missal target or boundary has an unknown slice")
                allowed = kinds | ({"text-slots", "forms-and-cycles"} if section == "boundaries" else set())
                if row.get("kind") not in allowed:
                    raise ValueError("unknown expected Missal target kind")
                if section == "targets":
                    if row.get("identity_state") not in {"established", "target-correspondence-unresolved"}:
                        raise ValueError("unknown expected Missal identity state")
                    for field in ("calendar_mass_key", "form_id", "cycle", "cycle_family",
                                  "parent_id", "source_form_key"):
                        if field in row and (not isinstance(row[field], str) or not row[field]):
                            raise ValueError(f"invalid expected Missal {field} join")
                    # Three relations once shared `form_id` (2026-10-19). Each
                    # now has its own field, so a join can never be read as a
                    # parent reference or the reverse: `form_id` names a form
                    # of the joined calendar mass and exists only beside
                    # `calendar_mass_key`; `parent_id` names the containing
                    # target in this inventory; `source_form_key` is a
                    # source-local formulary key that joins nothing.
                    if "form_id" in row and "calendar_mass_key" not in row:
                        raise ValueError(
                            "expected Missal form_id joins a calendar mass's form and "
                            "requires calendar_mass_key; a parent reference is parent_id"
                        )
                    proper_name = row.get("calendar_proper_name")
                    proper_occurrence = row.get("calendar_proper_occurrence")
                    appointment = row.get("calendar_ordinary_appointment")
                    option = row.get("calendar_ordinary_option")
                    parent = inventory_targets.get(row.get("parent_id"))
                    # A category's source-only slot may stay unresolved. Once
                    # it names any calendar join, require the complete own
                    # Collect address before generic Mass/form classification.
                    if (
                        row["kind"] == "text-slot"
                        and parent and parent.get("kind") == "collect-category"
                        and (
                            parent.get("calendar_mass_key")
                            or any(field in row for field in (
                                "calendar_mass_key", "form_id", "cycle", "cycle_family",
                                "calendar_proper_name", "calendar_proper_occurrence",
                                "calendar_ordinary_appointment", "calendar_ordinary_option",
                            ))
                        )
                        and not (
                            row.get("calendar_mass_key") and row.get("form_id")
                            and proper_name == "Collect"
                        )
                    ):
                        raise ValueError(
                            "expected Missal Collect category join requires explicit "
                            "calendar_mass_key, form_id and calendar_proper_name Collect"
                        )
                    if "calendar_proper_occurrence" in row and (
                        not proper_name or type(proper_occurrence) is not int
                        or proper_occurrence < 1
                    ):
                        raise ValueError(
                            "expected Missal calendar_proper_occurrence requires "
                            "calendar_proper_name and a positive integer"
                        )
                    if any(value is not None for value in (proper_name, appointment, option)):
                        if row["kind"] != "text-slot" or bool(proper_name) == bool(appointment):
                            raise ValueError("expected Missal text-slot requires one calendar unit join")
                        if proper_name is not None and (not isinstance(proper_name, str) or not proper_name):
                            raise ValueError("invalid expected Missal calendar_proper_name")
                        if appointment is not None and (not isinstance(appointment, str) or not appointment):
                            raise ValueError("invalid expected Missal calendar_ordinary_appointment")
                        if bool(option) != bool(appointment) or (option is not None and not isinstance(option, str)):
                            raise ValueError("expected Missal ordinary appointment requires its option")
                        if not row.get("calendar_mass_key") and not (parent and parent.get("calendar_mass_key")):
                            raise ValueError("expected Missal calendar unit join requires a joined Mass")
                        # A sanctoral source may enumerate an own Collect
                        # beneath a collect-category rather than a full form.
                        # Preserve that independently sourced hierarchy; only
                        # an explicit Mass/form-qualified Collect join can use it.
                        direct_collect = bool(
                            parent and parent.get("kind") == "collect-category"
                            and proper_name == "Collect"
                            and row.get("calendar_mass_key") and row.get("form_id")
                        )
                        if parent and parent.get("kind") != "form" and not direct_collect:
                            raise ValueError(
                                "expected Missal calendar unit join requires a parent form"
                                " or explicitly joined Collect category"
                            )
                        if parent and row.get("calendar_mass_key") and (
                            (not direct_collect or parent.get("calendar_mass_key"))
                            and row["calendar_mass_key"] != parent.get("calendar_mass_key")
                        ):
                            raise ValueError("expected Missal calendar unit join disagrees with its parent form")
                    if row.get("cycle") and row["cycle"] not in {"A", "B", "C", "ABC", "I", "II", "I-II"}:
                        raise ValueError("unknown expected Missal cycle")
                    if row.get("cycle_family") and row["cycle_family"] not in {"sunday", "weekday", "cycles", "weekday_cycles"}:
                        raise ValueError("unknown expected Missal cycle family")
                elif row.get("state") not in {"unenumerated", "inapplicable"}:
                    raise ValueError("unknown expected Missal boundary state")
        if section == "slices":
            slice_ids = ids
        if section == "targets":
            for row in document[section]:
                parent = row.get("parent_id")
                if parent is not None and (parent == row["id"] or parent not in ids):
                    raise ValueError(
                        f"expected Missal target {row['id']} names no other target as parent_id"
                    )
    slices =[row for row in document.get("slices", []) if row.get("calendar") == calendar]
    selected = {row["id"] for row in slices}
    by_key = {str(row["key"]): row for row in masses}
    by_registry = {str(row.get("registry")): row for row in masses if row.get("registry")}
    targets = []
    seen = set()
    for target in document.get("targets", []):
        if target.get("slice_id") not in selected:
            continue
        key = target.get("id")
        if not isinstance(key, str) or not key or key in seen:
            raise ValueError("expected Missal targets require unique nonempty IDs")
        seen.add(key)
        parent = inventory_targets.get(target.get("parent_id")) or {}
        lookup = str(target.get("calendar_mass_key") or (
            parent.get("calendar_mass_key") if target["kind"] == "text-slot" and (
                target.get("calendar_proper_name") or target.get("calendar_ordinary_appointment"))
            else "") or "")
        mass = by_key.get(lookup) or by_registry.get(lookup)
        if target.get("identity_state") != "established":
            state = "unresolved"
        elif not lookup:
            state = "unresolved"
        elif mass is None:
            state = "not-represented"
        else:
            state = "represented"
            # A printed text slot inherits the independently inventoried
            # parent form. Otherwise a missing long/Vigil form could borrow
            # the same-named Proper in the short/Day form.
            form_id = target.get("form_id") or (
                parent.get("form_id") if target["kind"] == "text-slot" else None
            )
            forms = mass.get("forms") or []
            form_ids = {form.get("id") for form in forms} if forms else {"main"}
            if form_id and form_id not in form_ids:
                state = "not-represented"
            elif target.get("calendar_proper_name"):
                selected_propers = mass.get("propers") or []
                if form_id and forms:
                    selected_propers = next((form.get("propers") or [] for form in forms
                                             if form.get("id") == form_id), [])
                matching_propers = [proper for proper in selected_propers
                                    if proper.get("name") == target["calendar_proper_name"]]
                occurrence = target.get("calendar_proper_occurrence")
                if occurrence is not None:
                    # Source-qualified ordinal among all exact-name nodes in
                    # this joined form, not a body-only provenance ordinal.
                    matching_propers = matching_propers[occurrence - 1:occurrence]
                if len(matching_propers) != 1:
                    state = "not-represented"
            elif target.get("calendar_ordinary_appointment"):
                appointed = (mass.get("ordinary_appointments") or {}).get(
                    target["calendar_ordinary_appointment"])
                if not isinstance(appointed, dict) or appointed.get("option") != target["calendar_ordinary_option"]:
                    state = "not-represented"
            elif target.get("cycle"):
                selected_mass = dict(mass)
                if form_id:
                    selected_mass["propers"] = [proper for proper in mass.get("propers") or []
                                                if (proper.get("form_id") or "main") == form_id]
                family = {"sunday": "cycles", "weekday": "weekday_cycles"}.get(
                    target.get("cycle_family"), target.get("cycle_family")
                )
                cycles = {one["cycle"] for one in proper_units(selected_mass)
                          if not family or one["cycle_family"] == family}
                expected_cycles = {"A", "B", "C"} if target["cycle"] == "ABC" else (
                    {"I", "II"} if target["cycle"] == "I-II" else {target["cycle"]}
                )
                if not expected_cycles <= cycles:
                    state = "not-represented"
        classified = {"id": key, "slice_id": target["slice_id"],
                      "kind": target["kind"], "state": state,
                      "mass": mass["key"] if mass else None}
        # Keep the independently named form even when no held calendar unit
        # corresponds to this slot. A missing Mass must not erase its target.
        if target["kind"] == "text-slot" and parent.get("kind") == "form":
            mass_key = target.get("calendar_mass_key") or parent.get("calendar_mass_key")
            if mass_key:
                classified["calendar_mass_key"] = mass_key
                classified["form_id"] = target.get("form_id") or parent.get("form_id") or "main"
        targets.append(classified)
    summaries = []
    for slice_row in slices:
        rows = [row for row in targets if row["slice_id"] == slice_row["id"]]
        summaries.append({
            "id": slice_row["id"], "enumeration_state": slice_row["enumeration_state"],
            **{key: slice_row[key] for key in (
                "calendar", "recension_id", "territory", "languages",
                "date_range", "source_refs", "basis"
            )},
            "kinds": [{"kind": kind, "states": dict(Counter(
                row["state"] for row in rows if row["kind"] == kind
            ))} for kind in sorted({row["kind"] for row in rows})],
        })
    boundaries = [{"id": row["id"], "slice_id": row["slice_id"],
                   "kind": row["kind"], "state": row["state"]}
                  for row in document.get("boundaries", []) if row.get("slice_id") in selected]
    return {"state": "classified", "as_of": str(document.get("as_of") or ""),
            "whole_inventory_state": "unresolved" if any(
                row["state"] == "unenumerated" for row in boundaries
            ) or any(row["enumeration_state"] != "complete-within-slice" for row in slices)
            else "bounded-slices-only",
            "review_ref": document.get("review_ref"),
            "slices": summaries, "targets": targets, "boundaries": boundaries}


TARGET_STATES = ("represented", "not-represented", "unresolved")
BOUNDED_FORM_SLOT_SCOPE = "inventoried-source-text-slots-for-joined-form"


def bounded_form_text_slots(report: dict) -> list[dict]:
    """Summarize independently inventoried slots of each calendar-joined form.

    An exact count is warranted only for the selected source slices marked
    complete within their stated scope. It counts source slot targets, not all
    prayers in a rendered Mass, wording availability, or the whole Missal.
    Unjoined source targets remain visible as unresolved correspondence.
    """
    slices = {row["id"]: row for row in report.get("slices") or []}
    groups: dict[tuple[str, str], list[dict]] = {}
    for target in report.get("targets") or []:
        if target["kind"] != "text-slot" or not target.get("calendar_mass_key"):
            continue
        key = (target["calendar_mass_key"], target["form_id"])
        groups.setdefault(key, []).append(target)
    result = []
    for (mass_key, form_id), targets in sorted(groups.items()):
        source_slices = [{"id": slice_id,
                          "enumeration_state": slices[slice_id]["enumeration_state"]}
                         for slice_id in sorted({row["slice_id"] for row in targets})]
        exact = all(row["enumeration_state"] == "complete-within-slice"
                    for row in source_slices)
        counts = Counter(row["state"] for row in targets)
        result.append({
            "calendar": slices[source_slices[0]["id"]]["calendar"],
            "mass": mass_key, "form": form_id,
            "scope": BOUNDED_FORM_SLOT_SCOPE,
            "denominator_state": "bounded" if exact else "unresolved",
            "expected": len(targets) if exact else None,
            "lower_bound": len(targets),
            "represented": counts["represented"],
            "not_represented": counts["not-represented"],
            "unresolved": counts["unresolved"],
            "source_slices": source_slices,
            "whole_form_state": "unresolved",
        })
    validate_bounded_form_text_slots(result)
    return result


def validate_bounded_form_text_slots(rows: object) -> None:
    """Validate the narrow per-form evidence passed between report owners."""
    if not isinstance(rows, list):
        raise ValueError("bounded form text slots must be an array")
    previous = None
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("bounded form text slot row must be an object")
        key = tuple(row.get(field) for field in ("calendar", "mass", "form"))
        if any(not isinstance(value, str) or not value for value in key):
            raise ValueError("bounded form text slot row requires calendar, mass, and form")
        if previous is not None and key <= previous:
            raise ValueError("bounded form text slot rows require unique sorted form keys")
        previous = key
        if row.get("scope") != BOUNDED_FORM_SLOT_SCOPE or row.get("whole_form_state") != "unresolved":
            raise ValueError("bounded form text slot scope must retain unresolved whole-form extent")
        counts = [row.get(field) for field in (
            "lower_bound", "represented", "not_represented", "unresolved")]
        if any(type(value) is not int or value < 0 for value in counts):
            raise ValueError("bounded form text slot counts must be nonnegative integers")
        if sum(counts[1:]) != counts[0] or counts[0] == 0:
            raise ValueError("bounded form text slot states must partition observed targets")
        slices = row.get("source_slices")
        if not isinstance(slices, list) or not slices:
            raise ValueError("bounded form text slot row requires source slices")
        ids = []
        for source in slices:
            if not isinstance(source, dict) or not isinstance(source.get("id"), str) or not source["id"]:
                raise ValueError("bounded form text slot source requires an ID")
            if source.get("enumeration_state") not in {"complete-within-slice", "partial", "unresolved"}:
                raise ValueError("bounded form text slot source has unknown enumeration state")
            ids.append(source["id"])
        if ids != sorted(set(ids)):
            raise ValueError("bounded form text slot source IDs must be unique and sorted")
        exact = all(source["enumeration_state"] == "complete-within-slice" for source in slices)
        if exact:
            if (row.get("denominator_state") != "bounded" or
                    type(row.get("expected")) is not int or row["expected"] != counts[0]):
                raise ValueError("complete source slices require the bounded observed denominator")
        elif row.get("denominator_state") != "unresolved" or row.get("expected") is not None:
            raise ValueError("incomplete source slices cannot claim an exact denominator")


def published_expectations(report: dict) -> dict:
    """Project `expectations()` for generated data without one row per target.

    The per-target rows were most of a structure file's coverage bytes and no
    page reads them. The projection keeps every slice and boundary, exact
    per-state totals, and the identity of each expected target that no held
    Mass represents, so a missing identity stays visible in the public data.
    The full classification remains `expectations()`'s return.

    Slice `source_refs` stay in the tracked inventory and are not published:
    they name repository records, including restricted editions' artifact
    records, which public data must not carry as rights context.
    """
    targets = report.get("targets") or []
    states = Counter(row["state"] for row in targets)
    if set(states) - set(TARGET_STATES):
        raise ValueError("expected Missal target has an unknown state")
    projected = {key: value for key, value in report.items() if key != "targets"}
    projected["slices"] = [
        {key: value for key, value in row.items() if key != "source_refs"}
        for row in report.get("slices") or []
    ]
    projected["target_states"] = {state: states[state] for state in TARGET_STATES}
    projected["not_represented"] = [
        {"id": row["id"], "slice_id": row["slice_id"], "kind": row["kind"]}
        for row in targets if row["state"] == "not-represented"
    ]
    return projected
