"""Finite, language-specific conclusion records in the next reviewed cohort.

This module does not appoint prayers or infer an ending from prose. Its single
authority owner supplies exact public descriptors and complete source controls.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import _calendars

PUBLIC_SCHEMA = "triptych-oration-conclusion-source/v2"
METHOD_ID = "missal-finite-oration-conclusion-execution-20261112-v2"
CALENDARS = {"roman-1962", "postconciliar"}
MODES = {"table-derived", "source-complete", "source-local-formula", "original-study-from-held-Latin"}
NATIVE_FIELDS = {"calendar", "target", "languages", "public_sha256", "public"}
LANGUAGE_FIELDS = {"source_id", "proper_sha256", "translation_binding_sha256", "latin_proof_sha256", "body_sha256", "formula_id", "cue_start", "cue_end", "cue_sha256", "full_conclusion_sha256", "source_controls", "candidate_packet", "cohort"}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(value):
    if not isinstance(value, (str, bytes)):
        value = canonical(value)
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError("oration conclusion supplement: " + message)


def pointer(document, value):
    """Read a strict RFC6901 pointer; a missing or malformed part refuses."""
    require(isinstance(value, str) and (not value or value.startswith("/")), "invalid JSON pointer")
    for raw in value.split("/")[1:]:
        for index, char in enumerate(raw):
            require(char != "~" or index + 1 < len(raw) and raw[index + 1] in "01", "invalid pointer escape")
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(document, list):
            require(token == "0" or token.isascii() and token.isdecimal() and not token.startswith("0"), "invalid array pointer")
            position = int(token)
            require(position < len(document), "array pointer outside source")
            document = document[position]
        else:
            require(isinstance(document, dict) and token in document, "pointer missing from source")
            document = document[token]
    return document


def index(declaration):
    rows = declaration.get("supplemental_records", [])
    require(isinstance(rows, list), "supplemental records are not a list")
    indexed = {}
    for row in rows:
        require(isinstance(row, dict) and set(row) in (NATIVE_FIELDS, NATIVE_FIELDS | {"constraints"}), "unknown supplemental record fields")
        calendar, target = row["calendar"], row["target"]
        require(calendar in CALENDARS and isinstance(target, list) and len(target) == 5, "unbound calendar/target")
        require(all(isinstance(part, str) and part for part in target[:4]) and type(target[4]) is int and target[4] > 0, "invalid source identity")
        languages = row["languages"]
        require(isinstance(languages, dict) and languages and set(languages) <= {"en", "la"}, "unbound language set")
        public = row["public"]
        require(isinstance(public, dict) and public.get("schema") == PUBLIC_SCHEMA and public.get("method_id") == METHOD_ID, "unknown public schema")
        require(public.get("calendar") == calendar and public.get("target") == target and set(public.get("languages", {})) == set(languages), "public identity differs")
        require(sha(public) == row["public_sha256"], "public descriptor differs")
        for language, native in languages.items():
            require(isinstance(native, dict) and set(native) in (LANGUAGE_FIELDS, LANGUAGE_FIELDS | {"constraints"}), "unknown language record fields")
            part = public["languages"][language]
            require(part.get("body_sha256") == native["body_sha256"] and part.get("offset_units") == "utf16", "public body identity differs")
            require(part.get("cue_start") == native["cue_start"] and part.get("cue_end") == native["cue_end"] and sha(part.get("cue")) == native["cue_sha256"], "public partition differs")
            require(sha(part.get("full_conclusion")) == native["full_conclusion_sha256"], "public formula differs")
            require(part.get("conclusion_mode") in MODES, "unreviewed conclusion mode")
        key = (calendar, *target)
        require(key not in indexed, "duplicate supplemental owner")
        indexed[key] = row
    return indexed


def validate_public(value, indexed):
    require(isinstance(value, dict) and value.get("schema") == PUBLIC_SCHEMA and value.get("method_id") == METHOD_ID, "unknown descriptor")
    target = value.get("target")
    require(isinstance(target, list) and len(target) == 5, "missing target")
    native = indexed.get((value.get("calendar"), *target))
    require(native is not None and sha(value) == native["public_sha256"], "unlisted or changed descriptor")
    return value


def source_controls(repository, controls, *, read_bytes=None, cache=None):
    require(isinstance(controls, list) and controls, "missing source controls")
    result = []
    for control in controls:
        require(isinstance(control, dict) and set(control) <= {"path", "sha256", "kind", "json_pointer", "id"} and {"path", "sha256"} <= set(control), "unknown source control")
        path = Path(control["path"])
        require(not path.is_absolute() and ".." not in path.parts and (path.parts[:2] == ("src", "sources") or path.parts[:2] == ("workflows", "reviews")), "control is not a durable source or review record")
        cached = cache.get(str(path)) if cache is not None else None
        raw = cached[0] if cached is not None else (read_bytes(path) if read_bytes is not None else (Path(repository) / path).read_bytes())
        parsed = None
        if "json_pointer" in control:
            require(path.suffix in {".json", ".toml"}, "pointer requires a structured source")
            document = cached[1] if cached is not None else (_calendars.parse_toml(raw) if path.suffix == ".toml" else json.loads(raw))
            parsed = pointer(document, control["json_pointer"])
            require(hashlib.sha256(canonical(parsed).encode()).hexdigest() == control["sha256"], "pointed source record changed")
        else:
            require(sha(raw) == control["sha256"], "source control changed")
            if path.suffix == ".toml":
                parsed = cached[1] if cached is not None else _calendars.parse_toml(raw)
            elif path.suffix == ".json":
                parsed = cached[1] if cached is not None else json.loads(raw)
        if cache is not None and cached is None:
            cache[str(path)] = (raw, document if "json_pointer" in control else parsed)
        if "id" in control:
            require(isinstance(parsed, dict) and parsed.get("id") == control["id"], "source record identity changed")
        result.append((control.get("kind", "source-record"), parsed))
    return result


def direct_source(owner, document, masses, target):
    mass = masses.get(target[0])
    require(mass is not None, "source mass absent")
    matches = []
    for label, proper in owner.propers_of(mass):
        if proper.get("takes_from") or proper.get("name") != target[2] or owner.form_id_for_label(mass, label) != target[1]:
            continue
        identity = owner.source_slot_identity(document, mass, label, proper, None, owner_masses=masses)
        if (identity[0], identity[1], identity[2], target[3], identity[3]) == tuple(target):
            matches.append(proper)
    require(len(matches) == 1 and target[3] == "all", "source form/cycle/occurrence unbound")
    return matches[0]


def load_sources(repository, calendar_root, calendar, owner, declaration, *, read_bytes=None):
    indexed = index(declaration)
    rows = [row for key, row in indexed.items() if key[0] == calendar]
    if not rows:
        return {}
    document = owner.load_calendar(Path(calendar_root), calendar)
    masses = {mass["key"]: mass for _, mass in owner.masses_of(document)}
    result = {}
    cache = {}
    for native in rows:
        target = native["target"]
        proper = direct_source(owner, document, masses, target)
        public = native["public"]
        for language, control in native["languages"].items():
            require(sha(proper) == control["proper_sha256"], "complete source proper changed")
            sources = source_controls(repository, control["source_controls"], read_bytes=read_bytes, cache=cache)
            if language == "la":
                text = proper.get("text")
                proofs = [value for kind, value in sources if kind == "latin-proof"]
                require(len(proofs) == 1 and sha(proofs[0]) == control["latin_proof_sha256"], "complete Latin proof missing or changed")
                proof = proofs[0]
                require(isinstance(proof, dict), "Latin proof is not a source record")
                require(proof.get("mass") == target[0] and owner.form_id_for_label(masses[target[0]], proof.get("form", "")) == target[1] and proof.get("proper") == target[2] and (proof.get("cycle") or "all") == target[3] and proof.get("occurrence") == target[4] and proof.get("text_sha256") == control["body_sha256"], "Latin proof source identity differs")
            else:
                bindings = [value for kind, value in sources if kind == "translation-binding"]
                require(len(bindings) == 1 and sha(bindings[0]) == control["translation_binding_sha256"], "complete translation binding missing or changed")
                binding = bindings[0]
                require(isinstance(binding, dict), "translation binding is not a source record")
                require(owner.translation_record_identity(binding, document) == tuple(target), "translation binding source identity differs")
                held = binding.get("translations")
                require(isinstance(held, list) and all(isinstance(row, dict) for row in held), "translation rows are not source records")
                translations = [row for row in held if row.get("lang") == "en" and (row.get("source_id") or "") == (control["source_id"] or "")]
                require(len(translations) == 1, "selected English witness is not unique")
                text = translations[0].get("text")
                require((public.get("source_id") or "") == (control["source_id"] or ""), "public body witness differs")
            require(isinstance(text, str) and sha(text) == control["body_sha256"], "original source body changed")
            part = public["languages"][language]
            raw = text.encode("utf-16-le")
            require(type(control["cue_start"]) is int and type(control["cue_end"]) is int, "source partition needs integer offsets")
            start, end = control["cue_start"] * 2, control["cue_end"] * 2
            require(0 < start < end == len(raw), "source partition outside body")
            require(raw[start:end].decode("utf-16-le") == part["cue"], "source partition changed")
        result[tuple(target)] = validate_public(public, indexed)
    return result
