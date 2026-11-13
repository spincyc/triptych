"""Separately sourced conclusions for a closed set of Roman 1962 prayers.

Literal proper and translation bodies are never edited. A descriptor provides
an independently sourced formula; execution still requires the actual prayer's
final position in its appointed group. The older six RG110 mappings are separate.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import tomllib

METHOD_ID = "roman-1962-rg115-conclusion-execution-20261112"
PUBLIC_SCHEMA = "triptych-oration-conclusion-source/v1"
AUTHORITY_PATH = "workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/authority-v2.json"
# Activated by the adjacent root-adoption-v2.json technical amendment; v1 retains the source merits review.
AUTHORITY_SHA256 = "c5fb8fb02eb062a53cdb5d316bb476f5586550691ce6a613e8cf2889241b4f43"
SOURCE_ID = "edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945"
TABLE_PATH = "src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/artifacts/resume-orations-conclusion-table-2026-10-23-7dbb4a25/conclusions.json"
TABLE_SHA256 = "7dbb4a258065ce0ba7d6d203be9e2593637b1e98dd2c123ffac10355e1bbb934"
TABLE_PASSAGE = "passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.resume-orations-conclusion-table-2026-10-23-transcription"
RULE_PASSAGE = "passage.catholic-church.missale-romanum.vatican-typica-1962.rubricae-generales-conclusions-115-116-20261112"
GROUP_RULE = "RGMR 436-437; 442-443; 480; 505"
NATIVE_FIELDS = {"target", "binding_sha256", "latin_proof_sha256", "english_sha256", "latin_sha256", "family", "english_cue_start", "latin_cue_start", "candidate_sha256", "public_sha256"}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(value):
    if not isinstance(value, (str, bytes)):
        value = canonical(value)
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError("oration conclusion: " + message)


def utf16(value):
    return len(value.encode("utf-16-le")) // 2


def browser_pin_section(declaration, authority_sha256):
    """Mechanical validation data; the reviewed authority remains its owner."""
    pins = {canonical(row["target"]): row["public_sha256"] for row in declaration["records"]}
    return ("  // BEGIN GENERATED CONCLUSION PINS — derived from the single finite authority.\n"
            + "  const GENERATED_AUTHORITY_SHA256 = " + json.dumps(authority_sha256) + ";\n"
            + "  const PUBLIC_PINS = Object.freeze(" + json.dumps(pins, ensure_ascii=False, sort_keys=True, indent=2) + ");\n"
            + "  // END GENERATED CONCLUSION PINS")


def formula_words(value):
    """Only the reviewed formula spellings, never arbitrary petition folding."""
    value = value.casefold().replace("jesum", "iesum").replace("eumdem", "eundem").replace("ejusdem", "eiusdem")
    return re.findall(r"[a-z]+", value)


def authority(repository):
    require(bool(AUTHORITY_SHA256), "finite conclusion authority is not activated")
    raw = (Path(repository) / AUTHORITY_PATH).read_bytes()
    require(sha(raw) == AUTHORITY_SHA256, "authority changed; a successor requires review")
    value = json.loads(raw)
    require(value.get("schema") == "triptych-finite-oration-conclusion-authority/v1" and value.get("method_id") == METHOD_ID, "unknown authority")
    rows = value.get("records")
    require(isinstance(rows, list) and rows, "empty finite authority")
    indexed = {}
    for row in rows:
        require(isinstance(row, dict) and set(row) == NATIVE_FIELDS, "unknown finite record fields")
        target = row["target"]
        require(isinstance(target, list) and len(target) == 5 and target[1] == "main" and target[2] in {"Collect", "Secret", "Postcommunion"} and target[3:] == ["all", 1], "unreviewed target shape")
        key = tuple(target)
        require(key not in indexed, "duplicate target")
        indexed[key] = row
    return value, indexed


def public_projection(native, english, latin, binding, formula):
    en_start, la_start = native["english_cue_start"], native["latin_cue_start"]
    require(type(en_start) is int and 0 < en_start < len(english), "invalid English partition")
    require(type(la_start) is int and 0 < la_start < len(latin), "invalid Latin partition")
    require(english[en_start:] == formula["short_english"], "source cue differs from its own table")
    require(native["family"] == formula["key"], "selected formula family differs")
    latin_cue = formula_words(latin[la_start:])
    require(bool(latin_cue) and formula_words(formula["full_latin"])[:len(latin_cue)] == latin_cue, "complete literal Latin cue is not this formula's reviewed prefix")
    target = native["target"]
    return {
        "schema": PUBLIC_SCHEMA, "method_id": METHOD_ID, "target": target,
        "calendar": "roman-1962", "source_id": SOURCE_ID,
        "source_text_sha256": native["english_sha256"],
        "target_latin_sha256": native["latin_sha256"],
        "translation_binding_sha256": native["binding_sha256"],
        "target_proof_sha256": native["latin_proof_sha256"],
        "formula_table_sha256": TABLE_SHA256,
        "family": native["family"], "rule_passage_id": RULE_PASSAGE,
        "formula_passage_id": TABLE_PASSAGE,
        "source_publication_passage_id": binding["publication_passage_id"],
        "languages": {
            "en": {"body_sha256": sha(english), "offset_units": "utf16", "cue_start": utf16(english[:en_start]), "cue_end": utf16(english), "cue": english[en_start:], "full_conclusion": formula["full_english"]},
            "la": {"body_sha256": sha(latin), "offset_units": "utf16", "cue_start": utf16(latin[:la_start]), "cue_end": utf16(latin), "cue": latin[la_start:], "full_conclusion": formula["full_latin"]},
        },
        "response": {"speaker": "response", "text": "Amen."},
        "context": {"mass_category": "good-friday-liturgy" if target[0] == "good-friday" else "mass-of-office", "required_slot": target[2], "required_group_role": "final-conclusion-provider", "particular_ending": False},
        "source_preserved": True,
        "qualification": "Conclusion supplied separately from the checked historical formula table under the 1962 conclusion rule. The original printed cue remains in the source quotation. Latin formula spelling remains that of its identified historical source.",
    }


def validate_public(value, repository, *, authority_rows=None):
    require(isinstance(value, dict), "public descriptor is not an object")
    if authority_rows is None:
        _, authority_rows = authority(repository)
    target = value.get("target")
    require(isinstance(target, list), "missing public target")
    native = authority_rows.get(tuple(target))
    require(native is not None and sha(value) == native["public_sha256"], "unlisted or changed public descriptor")
    return value


def load_sources(calendar_root, calendar, owner):
    if calendar != "roman-1962" or not AUTHORITY_SHA256:
        return {}
    calendar_root = Path(calendar_root)
    repository = calendar_root.resolve().parents[2]
    declaration, expected = authority(repository)
    table_bytes = (repository / TABLE_PATH).read_bytes()
    require(sha(table_bytes) == TABLE_SHA256, "historical formula table changed")
    formulas = {row["key"]: row for row in json.loads(table_bytes)["formulas"]}
    source_ids = set()
    for control in declaration["source_records"]:
        relative = Path(control["path"])
        require(not relative.is_absolute() and ".." not in relative.parts and relative.parts[:2] == ("src", "sources"), "source control outside library")
        raw = (repository / relative).read_bytes()
        require(sha(raw) == control["sha256"], "source rule/table record changed")
        source_record = tomllib.loads(raw.decode())
        require(source_record.get("id") == control["id"], "source control identity changed")
        source_ids.add(control["id"])
    require({RULE_PASSAGE, TABLE_PASSAGE} <= source_ids, "rule and formula controls required")
    document = owner.load_calendar(calendar_root, calendar)
    masses = {mass["key"]: mass for _, mass in owner.masses_of(document)}
    overlay_path = calendar_root.parent / "inventories/roman-1962-proper-translations-v1.toml"
    ledger = tomllib.loads(overlay_path.read_text())
    entries = {owner.translation_record_identity(row, document): row for row in ledger["entries"]}
    proof_path = calendar_root.parent / "inventories/roman-1962-proper-latin-provenance-v1.toml"
    proofs = tomllib.loads(proof_path.read_text())["entries"]
    proof_index = {(row["mass"], owner.form_id_for_label(masses[row["mass"]], row.get("form", "")), row["proper"], row.get("cycle") or "all", row["occurrence"]): row for row in proofs}
    result = {}
    for key, native in expected.items():
        binding = entries.get(key)
        require(binding is not None and sha(binding) == native["binding_sha256"], "complete translation binding changed")
        translations = [row for row in binding["translations"] if row.get("source_id") == SOURCE_ID and row.get("lang") == "en"]
        require(len(translations) == 1, "unique own-witness English required")
        english = translations[0]["text"]
        require(sha(english) == native["english_sha256"], "English source changed")
        matching = [row for row in masses[key[0]].get("propers", []) if row.get("name") == key[2] and row.get("text")]
        require(len(matching) == 1, "unique direct source proper required")
        latin = matching[0]["text"]
        proof = proof_index.get(key)
        require(sha(latin) == native["latin_sha256"] and proof is not None and proof.get("text_sha256") == native["latin_sha256"] and sha(proof) == native["latin_proof_sha256"], "complete target Latin or proof changed")
        require(native["family"] in formulas, "unknown formula family")
        public = public_projection(native, english, latin, binding, formulas[native["family"]])
        result[key] = validate_public(public, repository, authority_rows=expected)
    return result


def execute(value, text, *, repository, calendar, target, language, witness, group_final, mass_category="mass-of-office", authority_rows=None):
    """Execute only a checked final prayer; callers own appointment/group proof."""
    validate_public(value, repository, authority_rows=authority_rows)
    require(calendar == value["calendar"] and list(target) == value["target"], "wrong calendar or source owner")
    require(language in value["languages"], "unsupported language")
    require(language != "en" or witness == value["source_id"], "different English witness")
    require(group_final is True and mass_category == value["context"]["mass_category"], "unproved conclusion context")
    part = value["languages"][language]
    require(sha(text) == part["body_sha256"], "source prayer changed")
    raw = text.encode("utf-16-le")
    start, end = part["cue_start"] * 2, part["cue_end"] * 2
    require(end == len(raw) and raw[start:end].decode("utf-16-le") == part["cue"], "source partition changed")
    return {"execution_extent": {"state": "source-derived-complete", "method_id": METHOD_ID, "source_text_sha256": sha(text), "target": value["target"]}, "source_text": text, "priest_text": raw[:start].decode("utf-16-le") + part["full_conclusion"], "response": value["response"], "source_hooks": [value["rule_passage_id"], value["formula_passage_id"], value["source_publication_passage_id"]]}


def execute_group(context, *, repository, authority_rows=None):
    """Atomically project one actual, source-owned conclusion group.

    The adapter supplies the existing seating plan, never a renderer's guess.
    Group 1 is the principal unit; group 2 contains all admitted commemorations.
    Only its final member supplies a formula and response. No partial execution
    survives when even one member cannot be bound to its source and context.
    """
    try:
        require(context.get("calendar") == "roman-1962" and context.get("rule") == GROUP_RULE, "unproved grouping rule")
        groups = context.get("groups")
        require(isinstance(groups, list) and groups, "missing conclusion group")
        number = groups[0]["conclusion_group"]
        require(number in (1, 2) and all(group["conclusion_group"] == number for group in groups), "mixed conclusion groups")
        positions = [group["position"] for group in groups]
        require(positions == ([1] if number == 1 else list(range(2, 2 + len(groups)))) and len(groups) <= 2, "unbound group order")
        require(all(group["conclusion_final"] is (index == len(groups) - 1) for index, group in enumerate(groups)), "wrong conclusion provider unit")
        slot = groups[0]["slot"]
        members = []
        for group in groups:
            require(group["slot"] == slot, "mixed prayer families")
            rows = group["members"]
            require(group["kind"] in ({"principal", "inseparable"} if number == 1 else {"commemoration", "inseparable"}), "unbound group kind")
            require(isinstance(rows, list) and len(rows) == (2 if group["kind"] == "inseparable" else 1), "unbound member order")
            for member in rows:
                require(member["target"][2] == slot, "member source slot differs")
                result = execute(member["source"], member["text"], repository=repository, calendar=context["calendar"], target=member["target"], language=member["language"], witness=member.get("witness"), group_final=True, mass_category=context.get("massCategory", "mass-of-office"), authority_rows=authority_rows)
                members.append({"id": member["id"], "language": member["language"], "source": member["source"], **result})
        require(len({member["id"] for member in members}) == len(members), "duplicate member")
        require(len({member["language"] for member in members}) == 1, "mixed execution languages")
        for member in members[:-1]:
            cut = member["source"]["languages"][member["language"]]["cue_start"]
            member["priest_text"] = member["source_text"].encode("utf-16-le")[:cut * 2].decode("utf-16-le")
        result_rows = [{"id": member["id"], "source_text": member["source_text"], "priest_text": member["priest_text"], "role": "conclusion-provider" if index == len(members)-1 else "petition", "source_hooks": member["source_hooks"]} for index, member in enumerate(members)]
        return {"schema": "triptych-oration-conclusion-group/v1", "state": "source-derived-complete", "execution_extent": {"state": "source-derived-complete", "method_id": METHOD_ID}, "conclusion_group": number, "slot": slot, "members": result_rows, "response": {**members[-1]["response"], "provider_id": members[-1]["id"]}}
    except (ValueError, KeyError, TypeError, IndexError, OSError, UnicodeError):
        return {"schema": "triptych-oration-conclusion-group/v1", "state": "unresolved", "execution_extent": {"state": "unresolved", "method_id": METHOD_ID}, "reasons": ["conclusion-group-source-or-context-unbound"], "members": []}
