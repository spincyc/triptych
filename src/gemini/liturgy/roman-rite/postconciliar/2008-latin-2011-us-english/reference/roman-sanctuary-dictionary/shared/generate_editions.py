#!/usr/bin/env python3
"""Deterministic validator and four-edition TeX projection engine for the
Postconciliar Illustrated Dictionary of the Roman Sanctuary
(2008 Latin third typical edition / 2011 US English Roman Missal).

Single canonical owner:
  - shared/schema/inventory-schema.toml
  - shared/schema/plates-and-editions.toml
  - shared/objects/**/*.toml
  - research/artwork-manifest.toml
  - shared/artwork/graphite/*.png

Projects deterministically with zero prose drift into:
  - comprehensive/sections/*.tex
  - altar-server/sections/*.tex
  - sacristan/sections/*.tex
  - general-reader/sections/*.tex
  - research/object-inventory.md

Usage:
  python3 .../shared/generate_editions.py --write
  python3 .../shared/generate_editions.py --check
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import tomllib
from pathlib import Path

OWNER = Path(__file__).resolve().parents[1]
REPO_REL_OWNER = "liturgy/roman-rite/postconciliar/2008-latin-2011-us-english/reference/roman-sanctuary-dictionary"
SCHEMA_PATH = OWNER / "shared/schema/inventory-schema.toml"
PLATES_PATH = OWNER / "shared/schema/plates-and-editions.toml"
ARTWORK_MANIFEST_PATH = OWNER / "research/artwork-manifest.toml"
OBJECTS_DIR = OWNER / "shared/objects"

FORBIDDEN_READER_PATTERNS = (
    (r"\(\s*gloss\s*:", "printed (gloss: ...) label"),
    (r"\bnot a definition\b", "defensive hedging phrase 'not a definition'"),
    (r"\bdefines nothing\b", "defensive hedging phrase 'defines nothing'"),
    (r"\bno magisterial act addresses\b", "defensive hedging phrase"),
    (r"\blater Christians believed\b", "distancing secular phrasing"),
    (r"\ba devotional reading might see\b", "distancing secular phrasing"),
    (r"\bfrom a modern perspective\b", "distancing secular phrasing"),
    (r"\bthis study\b", "editorial self-narration 'this study'"),
    (r"\bin these pages\b", "editorial self-narration 'in these pages'"),
    (r"\bmethodologically\b", "AI/methodological jargon"),
    (r"\bit is important to distinguish\b", "editorial self-narration"),
    (r"\bwe have chosen to emphasize\b", "editorial self-narration"),
    (r"\bformulary\b", "production jargon 'formulary'"),
    (r"\bpublic-alpha\b|\balpha release\b|\bbounded alpha\b", "internal release state in reader-facing prose"),
)

MINISTER_LABELS = {
    "bishop": "Bishop",
    "priest": "Priest",
    "deacon": "Deacon",
    "instituted-acolyte": "Instituted acolyte",
    "instituted-lector": "Instituted lector",
    "extraordinary-minister": "Extraordinary minister of Holy Communion",
    "altar-server": "Altar server",
    "sacristan": "Sacristan",
    "faithful": "Faithful",
    "subdeacon-historical": "Subdeacon (pre-1973 Latin Rite)",
}

SERVER_BOUNDARY_LABELS = {
    "handles": "Server handles directly",
    "carries": "Server carries in procession or movement",
    "presents": "Server carries and presents to priest or deacon",
    "prepares": "Server prepares or sets in place before or during Mass",
    "moves-only-by-direction": "Server moves only at celebrant's or sacristan's direction",
    "recognizes-only": "Server recognizes only; does not handle",
    "clergy-reserved": "Clergy-reserved; server does not touch",
    "superseded-historical": "Historically superseded; not used in current practice",
}

SCOPE_LABELS = {
    "universal-roman": "Universal Roman law",
    "territorial-usccb": "USCCB territorial adaptation",
    "diocesan-or-local": "Diocesan or local selection",
    "customary": "Documented custom",
    "historically-superseded": "Historically superseded postconciliar form",
}


def tex_escape(text: str) -> str:
    """Escape plain UTF-8 prose cleanly for pdflatex and pandoc web conversion."""
    out = text.replace("\\", r"\textbackslash{}")
    for ch, rep in (
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
        ("—", "---"),
        ("–", "--"),
        ("“", "``"),
        ("”", "''"),
        ("‘", "`"),
        ("’", "'"),
    ):
        out = out.replace(ch, rep)
    return out


def format_ministers(roles: list[str]) -> str:
    return ", ".join(MINISTER_LABELS[r] for r in roles)


def check_reader_prose(field_name: str, text: str, obj_id: str, errors: list[str]) -> None:
    for pattern, label in FORBIDDEN_READER_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            errors.append(f"{obj_id}.{field_name}: forbidden reader prose ({label})")


def load_and_validate() -> tuple[dict, dict, dict, dict[str, dict], list[str]]:
    errors: list[str] = []
    schema = tomllib.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    plates_cfg = tomllib.loads(PLATES_PATH.read_text(encoding="utf-8"))
    art_manifest = tomllib.loads(ARTWORK_MANIFEST_PATH.read_text(encoding="utf-8"))

    enums = schema["controlled_enums"]
    patterns = schema["id_patterns"]
    obj_id_re = re.compile(patterns["object_id"])
    plate_id_re = re.compile(patterns["plate_id"])
    art_id_re = re.compile(patterns["artwork_id"])
    note_key_re = re.compile(patterns["note_key"])

    # Validate artwork manifest and actual PNG files on disk
    art_by_id: dict[str, dict] = {}
    for art in art_manifest.get("artworks", []):
        aid = art["id"]
        if not art_id_re.match(aid):
            errors.append(f"artwork-manifest: invalid artwork id {aid!r}")
        if aid in art_by_id:
            errors.append(f"artwork-manifest: duplicate artwork id {aid!r}")
        art_by_id[aid] = art
        rel_path = art["normalized"]["path"]
        img_path = OWNER / rel_path
        if not img_path.is_file():
            errors.append(f"artwork-manifest: missing PNG {rel_path}")
        else:
            actual_sha = hashlib.sha256(img_path.read_bytes()).hexdigest()
            expected_sha = art["normalized"]["sha256"]
            if actual_sha != expected_sha:
                errors.append(f"artwork-manifest: sha256 mismatch for {rel_path}: {actual_sha} != {expected_sha}")
            actual_bytes = img_path.stat().st_size
            if actual_bytes != art["normalized"]["bytes"]:
                errors.append(f"artwork-manifest: byte size mismatch for {rel_path}")

    # Validate plates config
    plates_by_id: dict[str, dict] = {}
    for plate in plates_cfg.get("plates", []):
        pid = plate["id"]
        if not plate_id_re.match(pid):
            errors.append(f"plates-and-editions: invalid plate id {pid!r}")
        if pid in plates_by_id:
            errors.append(f"plates-and-editions: duplicate plate id {pid!r}")
        if plate["artwork_id"] not in art_by_id:
            errors.append(f"plates-and-editions: plate {pid} references unknown artwork {plate['artwork_id']!r}")
        plates_by_id[pid] = plate

    # Load and validate all canonical object TOML files
    obj_files = sorted(OBJECTS_DIR.rglob("*.toml"))
    if not obj_files:
        errors.append("No canonical object TOML files found under shared/objects/")
    objects: dict[str, dict] = {}
    seen_notes: set[str] = set()
    allowed_top_keys = {
        "schema_version", "id", "category", "sort_order", "plate_id",
        "composition_plate_ids", "plate_position",
        "preferred_english_name", "latin_headword",
        "alternate_english_names", "alternate_latin_names", "pronunciation_key",
        "edition_disposition", "identification", "ministers_and_handling",
        "audience_text", "relationships", "symbolism", "counterpart_1962",
        "historical_transition", "audiences", "sources",
    }

    for path in obj_files:
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.relative_to(OWNER)}: TOML parse error: {exc}")
            continue
        unknown = set(data.keys()) - allowed_top_keys
        if unknown:
            errors.append(f"{path.relative_to(OWNER)}: unknown top-level keys {sorted(unknown)}")
        oid = data.get("id", "")
        if not obj_id_re.match(oid):
            errors.append(f"{path.relative_to(OWNER)}: invalid id {oid!r}")
        if oid in objects:
            errors.append(f"{path.relative_to(OWNER)}: duplicate object id {oid!r}")
        if data.get("schema_version") != 1:
            errors.append(f"{oid}: schema_version must be 1")
        cat = data.get("category", "")
        if cat not in enums["categories"]:
            errors.append(f"{oid}: invalid category {cat!r}")

        ed = data.get("edition_disposition", {})
        disp = ed.get("disposition", "")
        if disp not in enums["dispositions"]:
            errors.append(f"{oid}: invalid disposition {disp!r}")
        if ed.get("scope_level") not in enums["scope_levels"]:
            errors.append(f"{oid}: invalid scope_level {ed.get('scope_level')!r}")
        if ed.get("edition_locale") != "2008-latin-2011-us-english":
            errors.append(f"{oid}: edition_locale must be 2008-latin-2011-us-english")

        ht = data.get("historical_transition", {})
        is_sup = bool(ht.get("is_superseded", False))
        if disp == "superseded" or cat == "superseded-postconciliar" or is_sup:
            if not (disp == "superseded" and cat == "superseded-postconciliar" and is_sup):
                errors.append(f"{oid}: superseded forms must consistently set disposition='superseded', category='superseded-postconciliar', is_superseded=true")
            for k in ("period_range", "controlling_act", "current_status"):
                if not str(ht.get(k, "")).strip():
                    errors.append(f"{oid}: superseded record missing historical_transition.{k}")
        else:
            pid = data.get("plate_id", "")
            if pid not in plates_by_id:
                errors.append(f"{oid}: current object references unknown plate_id {pid!r}")
            if not str(data.get("plate_position", "")).strip():
                errors.append(f"{oid}: current object missing plate_position")

        mh = data.get("ministers_and_handling", {})
        for r in mh.get("ordinary_ministers", []):
            if r not in enums["ministers"]:
                errors.append(f"{oid}: invalid ordinary_minister {r!r}")
        for r in mh.get("prepares", []):
            if r not in enums["ministers"]:
                errors.append(f"{oid}: invalid prepares role {r!r}")
        if mh.get("server_boundary") not in enums["server_boundaries"]:
            errors.append(f"{oid}: invalid server_boundary {mh.get('server_boundary')!r}")

        sym = data.get("symbolism", {})
        if sym.get("evidence_class") not in enums["symbolism_evidence_classes"]:
            errors.append(f"{oid}: invalid symbolism.evidence_class {sym.get('evidence_class')!r}")
        if sym.get("has_sourced_symbolism") and not (str(sym.get("text", "")).strip() and str(sym.get("attribution", "")).strip()):
            errors.append(f"{oid}: has_sourced_symbolism=true requires non-empty text and attribution")

        c62 = data.get("counterpart_1962", {})
        if c62.get("relationship") not in enums["counterpart_1962_relationships"]:
            errors.append(f"{oid}: invalid counterpart_1962.relationship {c62.get('relationship')!r}")

        src = data.get("sources", {})
        nkey = src.get("note_key", "")
        if not note_key_re.match(nkey):
            errors.append(f"{oid}: invalid note_key {nkey!r}")
        if nkey in seen_notes:
            errors.append(f"{oid}: duplicate note_key {nkey!r}")
        seen_notes.add(nkey)
        if not src.get("primary_loci"):
            errors.append(f"{oid}: empty sources.primary_loci")

        # Editorial prose checks across all reader-facing fields
        ident = data.get("identification", {})
        aud = data.get("audience_text", {})
        for fname, val in (
            ("identification.summary", ident.get("summary", "")),
            ("identification.appearance", ident.get("appearance", "")),
            ("identification.placement_and_use", ident.get("placement_and_use", "")),
            ("edition_disposition.territorial_note", ed.get("territorial_note", "")),
            ("ministers_and_handling.server_boundary_summary", mh.get("server_boundary_summary", "")),
            ("ministers_and_handling.safety_warning", mh.get("safety_warning", "")),
            ("audience_text.altar_server", aud.get("altar_server", "")),
            ("audience_text.sacristan", aud.get("sacristan", "")),
            ("audience_text.general_reader", aud.get("general_reader", "")),
            ("symbolism.text", sym.get("text", "")),
            ("counterpart_1962.comparison", c62.get("comparison", "")),
        ):
            if val:
                check_reader_prose(fname, str(val), oid, errors)

        objects[oid] = data

    # Validate cross-object references
    for oid, data in objects.items():
        rels = data.get("relationships", {})
        for field in ("confusable_with", "related_objects"):
            for ref in rels.get(field, []):
                if ref not in objects:
                    errors.append(f"{oid}: relationships.{field} references unknown object {ref!r}")

    return schema, plates_cfg, art_manifest, objects, errors


def render_plate_block(plate: dict, art: dict, hero: bool = False) -> str:
    """Render a monochrome graphite plate in print with a complete accessible
    textual equivalent in the web-active \\else branch."""
    rel_img = f"{REPO_REL_OWNER}/{art['normalized']['path']}"
    width_opt = "width=0.96\\linewidth,height=4.25in,keepaspectratio" if hero else "width=0.92\\linewidth,height=3.55in,keepaspectratio"
    lines = [
        f"\\PCDPlateHeader{{{tex_escape(plate['header_label'])}}}{{{tex_escape(plate['scale_notice'])}}}",
        "\\ifdefined\\TriptychPrintEdition",
        "\\begin{center}",
        f"\\includegraphics[{width_opt}]{{{rel_img}}}",
        "\\end{center}",
        f"\\PCDPositionKey{{{tex_escape(plate['position_key'])}}}",
        "\\else",
        f"\\textbf{{Visual Plate Summary ({tex_escape(plate['header_label'])}, {tex_escape(plate['scale_notice'])}):}} {tex_escape(plate['web_alt_description'])}",
        "",
        f"\\textbf{{Reading order and object placement:}} {tex_escape(plate['position_key'])}",
        "\\fi",
        "",
    ]
    return "\n".join(lines)


def render_color_key(plates_cfg: dict) -> str:
    """Render the monochrome liturgical-color pattern key (GIRM 346 USCCB)."""
    rows_print = []
    rows_web = []
    for item in plates_cfg["liturgical_colors"]:
        name = tex_escape(item["name"])
        pattern_label = tex_escape(item["monochrome_pattern"])
        seasons = tex_escape(item["usage"])
        swatch = item["tikz_swatch"]
        rows_print.append(f"\\textbf{{{name}}} & {swatch}\\ {pattern_label} & {seasons} \\\\")
        rows_web.append(f"\\textbf{{{name}}} & {pattern_label} & {seasons} \\\\")

    return "\n".join([
        "\\subsection*{Monochrome Key for Liturgical Vestment Colors}",
        "In monochrome graphite plates, vestment and textile colors appointed in the General Instruction of the Roman Missal (no.~346, with United States adaptations) are named in words and keyed below rather than encoded by tint alone.",
        "",
        "\\ifdefined\\TriptychPrintEdition",
        "{\\footnotesize\\begin{longtable}{>{\\raggedright\\arraybackslash}p{0.14\\linewidth}>{\\raggedright\\arraybackslash}p{0.27\\linewidth}>{\\raggedright\\arraybackslash}p{0.52\\linewidth}}",
        "\\toprule",
        "\\textbf{Color} & \\textbf{Monochrome key} & \\textbf{Appointed occasions (US 2011 GIRM 346)} \\\\",
        "\\midrule",
        "\\endhead",
        *rows_print,
        "\\bottomrule",
        "\\end{longtable}}",
        "\\else",
        "{\\footnotesize\\begin{longtable}{>{\\raggedright\\arraybackslash}p{0.14\\linewidth}>{\\raggedright\\arraybackslash}p{0.25\\linewidth}>{\\raggedright\\arraybackslash}p{0.54\\linewidth}}",
        "\\toprule",
        "\\textbf{Color} & \\textbf{Print pattern key} & \\textbf{Appointed occasions (US 2011 GIRM 346)} \\\\",
        "\\midrule",
        "\\endhead",
        *rows_web,
        "\\bottomrule",
        "\\end{longtable}}",
        "\\fi",
        "",
    ])


def render_disposition_key() -> str:
    return "\n".join([
        "\\subsection*{Reading the Status Tags}",
        "Each entry names its status for the 2008 Latin third typical edition of the Roman Missal as implemented in the 2011 United States edition (as of 2026-11-25). "
        "\\PCDTag{required} marks an item prescribed by universal Roman law; "
        "\\PCDTag{provided} marks an item expressly appointed for a rite, ministry, or occasion; "
        "\\PCDTag{permitted} and \\PCDTag{optional} mark lawful choices governed by rubric or celebrant judgment; "
        "\\PCDTag{territorial adaptation} marks a norm established by the United States Conference of Catholic Bishops; "
        "\\PCDTag{customary} marks widespread parish practice distinct from universal prescription; and "
        "\\PCDTag{superseded} appears exclusively in the chronological historical section.",
        "",
    ])


def render_object_entry(obj: dict, objects: dict[str, dict], edition: str) -> str:
    eng = tex_escape(obj["preferred_english_name"])
    lat = tex_escape(obj["latin_headword"])
    ed = obj["edition_disposition"]
    disp = tex_escape(ed["disposition"])
    nkey = tex_escape(obj["sources"]["note_key"])
    ident = obj["identification"]
    mh = obj["ministers_and_handling"]
    sym = obj["symbolism"]
    c62 = obj["counterpart_1962"]
    rels = obj["relationships"]
    aud = obj["audience_text"]

    alt_parts = []
    if obj.get("alternate_english_names"):
        alt_parts.append("; ".join(tex_escape(x) for x in obj["alternate_english_names"]))
    if obj.get("alternate_latin_names"):
        alt_parts.append("; ".join(f"\\textit{{{tex_escape(x)}}}" for x in obj["alternate_latin_names"]))

    conf_names = [tex_escape(objects[cid]["preferred_english_name"]) for cid in rels.get("confusable_with", [])]

    lines = [
        f"\\label{{{obj['id']}}}",
        f"\\PCDEntryHead{{{eng}}}{{{lat}}}{{{disp}}}{{{nkey}}}",
    ]
    if alt_parts:
        alt_joined = "; ".join(alt_parts)
        lines.append(f"\\PCDField{{Also called}}{{{alt_joined}}}")

    pos_line = tex_escape(obj.get("plate_position", ""))
    scope_lbl = SCOPE_LABELS[ed["scope_level"]]

    if edition == "comprehensive":
        lines.append(f"{tex_escape(ident['summary'])} {tex_escape(ident['appearance'])}")
        lines.append("")
        lines.append(f"\\PCDField{{Plate position and status}}{{{pos_line} ({tex_escape(scope_lbl)})}}")
        lines.append(f"\\PCDField{{Placement and liturgical use}}{{{tex_escape(ident['placement_and_use'])}}}")
        if ed.get("territorial_note"):
            lines.append(f"\\PCDField{{United States norm}}{{{tex_escape(ed['territorial_note'])}}}")
        lines.append(
            f"\\PCDField{{Ministers and server boundary}}{{Ordinary ministers: {tex_escape(format_ministers(mh['ordinary_ministers']))}. "
            f"{tex_escape(SERVER_BOUNDARY_LABELS[mh['server_boundary']])}: {tex_escape(mh['server_boundary_summary'])}}}"
        )
        if mh.get("safety_warning"):
            lines.append(f"\\PCDSafety{{{tex_escape(mh['safety_warning'])}}}")
        if conf_names:
            lines.append(f"\\PCDField{{Distinguish from}}{{{', '.join(conf_names)}}}")
        if sym.get("has_sourced_symbolism"):
            lines.append(f"\\PCDField{{Symbolism}}{{{tex_escape(sym['text'])} ({tex_escape(sym['attribution'])})}}")
        lines.append(
            f"\\PCDField{{1962 Roman Missal counterpart}}{{\\PCDTag{{{tex_escape(c62['relationship'])}}} {tex_escape(c62['comparison'])}}}"
        )

    elif edition == "altar-server":
        lines.append(f"{tex_escape(aud['altar_server'])}")
        lines.append("")
        lines.append(f"\\PCDField{{Where to look on the plate}}{{{pos_line}}}")
        lines.append(
            f"\\PCDField{{Handling boundary}}{{\\textbf{{{tex_escape(SERVER_BOUNDARY_LABELS[mh['server_boundary']])}.}} "
            f"{tex_escape(mh['server_boundary_summary'])} (Ordinary ministers: {tex_escape(format_ministers(mh['ordinary_ministers']))}.)}}"
        )
        if mh.get("safety_warning"):
            lines.append(f"\\PCDSafety{{{tex_escape(mh['safety_warning'])}}}")
        if conf_names:
            lines.append(f"\\PCDField{{Do not confuse with}}{{{', '.join(conf_names)}}}")

    elif edition == "sacristan":
        lines.append(f"{tex_escape(aud['sacristan'])}")
        lines.append("")
        lines.append(f"\\PCDField{{Plate position and norm}}{{{pos_line} ({tex_escape(scope_lbl)})}}")
        lines.append(f"\\PCDField{{Placement and use}}{{{tex_escape(ident['placement_and_use'])}}}")
        if ed.get("territorial_note"):
            lines.append(f"\\PCDField{{United States norm}}{{{tex_escape(ed['territorial_note'])}}}")
        lines.append(
            f"\\PCDField{{Prepared and handled by}}{{Prepares: {tex_escape(format_ministers(mh['prepares']))}. "
            f"Ministers in use: {tex_escape(format_ministers(mh['ordinary_ministers']))}.}}"
        )
        if mh.get("safety_warning"):
            lines.append(f"\\PCDSafety{{{tex_escape(mh['safety_warning'])}}}")
        if conf_names:
            lines.append(f"\\PCDField{{Distinguish from}}{{{', '.join(conf_names)}}}")

    elif edition == "general-reader":
        lines.append(f"{tex_escape(aud['general_reader'])}")
        lines.append("")
        lines.append(f"\\PCDField{{On the plate}}{{{pos_line}}}")
        if sym.get("has_sourced_symbolism"):
            lines.append(f"\\PCDField{{Symbolism}}{{{tex_escape(sym['text'])} ({tex_escape(sym['attribution'])})}}")
        lines.append(
            f"\\PCDField{{Relation to the 1962 Missal}}{{\\PCDTag{{{tex_escape(c62['relationship'])}}} {tex_escape(c62['comparison'])}}}"
        )

    lines.append("\\PCDEntryRule")
    lines.append("")
    return "\n".join(lines)


def render_superseded_entry(obj: dict) -> str:
    eng = tex_escape(obj["preferred_english_name"])
    lat = tex_escape(obj["latin_headword"])
    ht = obj["historical_transition"]
    nkey = tex_escape(obj["sources"]["note_key"])
    ident = obj["identification"]
    c62 = obj["counterpart_1962"]
    return "\n".join([
        f"\\label{{{obj['id']}}}",
        f"\\PCDHistHead{{{eng}}}{{{lat}}}{{{tex_escape(ht['period_range'])} --- {tex_escape(ht['controlling_act'])}}}{{{nkey}}}",
        f"{tex_escape(ident['summary'])}",
        "",
        f"\\PCDField{{Current discipline (2008/2011)}}{{{tex_escape(ht['current_status'])}}}",
        f"\\PCDField{{1962 comparison}}{{\\PCDTag{{{tex_escape(c62['relationship'])}}} {tex_escape(c62['comparison'])}}}",
        "\\PCDEntryRule",
        "",
    ])


def render_ministry_table(plates_cfg: dict) -> str:
    rows = []
    for row in plates_cfg["ministry_distinctions"]:
        rows.append(
            f"\\textbf{{{tex_escape(row['minister'])}}} & {tex_escape(row['vesture'])} & {tex_escape(row['sanctuary_role'])} \\\\"
        )
    return "\n".join([
        "\\subsection*{Distinct Ministers in the Postconciliar Sanctuary}",
        "The General Instruction of the Roman Missal distinguishes ordained ministers, instituted lay ministries, extraordinary ministers of Holy Communion, and altar servers. Each office carries its own vesture and handling boundary, and none is interchangeable with another.",
        "",
        "{\\footnotesize\\begin{longtable}{>{\\raggedright\\arraybackslash}p{0.20\\linewidth}>{\\raggedright\\arraybackslash}p{0.28\\linewidth}>{\\raggedright\\arraybackslash}p{0.45\\linewidth}}",
        "\\toprule",
        "\\textbf{Minister} & \\textbf{Appointed vesture} & \\textbf{Sanctuary and handling role} \\\\",
        "\\midrule",
        "\\endhead",
        *rows,
        "\\bottomrule",
        "\\end{longtable}}",
        "",
    ])


def render_pronunciation_appendix(selected: list[dict]) -> str:
    seen = set()
    rows = []
    for obj in sorted(selected, key=lambda o: o["latin_headword"].casefold()):
        lat = obj["latin_headword"]
        if lat in seen or not obj.get("pronunciation_key"):
            continue
        seen.add(lat)
        rows.append(
            f"\\textit{{{tex_escape(lat)}}} & {tex_escape(obj['pronunciation_key'])} & {tex_escape(obj['preferred_english_name'])} \\\\"
        )
    return "\n".join([
        "\\section{Pronunciation of Commonly Spoken Latin Terms}",
        "Ecclesiastical (Roman) Latin pronunciation for Latin sanctuary headwords. Capitalized syllables take the primary stress.",
        "",
        "{\\footnotesize\\begin{longtable}{>{\\raggedright\\arraybackslash}p{0.28\\linewidth}>{\\raggedright\\arraybackslash}p{0.34\\linewidth}>{\\raggedright\\arraybackslash}p{0.31\\linewidth}}",
        "\\toprule",
        "\\textbf{Latin term} & \\textbf{Ecclesiastical pronunciation} & \\textbf{English headword} \\\\",
        "\\midrule",
        "\\endhead",
        *rows,
        "\\bottomrule",
        "\\end{longtable}}",
        "",
    ])


def render_indexes(selected: list[dict], plates_by_id: dict[str, dict]) -> str:
    eng_rows = []
    for obj in sorted(selected, key=lambda o: o["preferred_english_name"].casefold()):
        pid = obj.get("plate_id", "")
        plabel = plates_by_id[pid]["short_label"] if pid in plates_by_id else "Historical section"
        lat_raw = obj["latin_headword"]
        if "no Latin typical edition" in lat_raw:
            lat_cell = "--- (no Latin typical edition)"
        else:
            lat_cell = f"\\textit{{{tex_escape(lat_raw)}}}"
        eng_rows.append(
            f"{tex_escape(obj['preferred_english_name'])} & {lat_cell} & {tex_escape(plabel)} & {tex_escape(obj['sources']['note_key'])} \\\\"
        )
    lat_rows = []
    for obj in sorted(selected, key=lambda o: o["latin_headword"].casefold()):
        lat_raw = obj["latin_headword"]
        if "no Latin typical edition" in lat_raw:
            continue
        pid = obj.get("plate_id", "")
        plabel = plates_by_id[pid]["short_label"] if pid in plates_by_id else "Historical section"
        lat_rows.append(
            f"\\textit{{{tex_escape(lat_raw)}}} & {tex_escape(obj['preferred_english_name'])} & {tex_escape(plabel)} & {tex_escape(obj['sources']['note_key'])} \\\\"
        )
    return "\n".join([
        "\\section{English--Latin and Latin--English Indexes}",
        "\\subsection*{English to Latin}",
        "{\\footnotesize\\begin{longtable}{>{\\raggedright\\arraybackslash}p{0.31\\linewidth}>{\\raggedright\\arraybackslash}p{0.31\\linewidth}>{\\raggedright\\arraybackslash}p{0.23\\linewidth}>{\\raggedright\\arraybackslash}p{0.08\\linewidth}}",
        "\\toprule",
        "\\textbf{English} & \\textbf{Latin} & \\textbf{Location} & \\textbf{Note} \\\\",
        "\\midrule",
        "\\endhead",
        *eng_rows,
        "\\bottomrule",
        "\\end{longtable}}",
        "",
        "\\subsection*{Latin to English}",
        "{\\footnotesize\\begin{longtable}{>{\\raggedright\\arraybackslash}p{0.31\\linewidth}>{\\raggedright\\arraybackslash}p{0.31\\linewidth}>{\\raggedright\\arraybackslash}p{0.23\\linewidth}>{\\raggedright\\arraybackslash}p{0.08\\linewidth}}",
        "\\toprule",
        "\\textbf{Latin} & \\textbf{English} & \\textbf{Location} & \\textbf{Note} \\\\",
        "\\midrule",
        "\\endhead",
        *lat_rows,
        "\\bottomrule",
        "\\end{longtable}}",
        "",
    ])


def render_chronology_table(plates_cfg: dict) -> str:
    rows = []
    for row in plates_cfg["chronology"]:
        rows.append(
            f"\\textbf{{{tex_escape(row['date'])}}} & {tex_escape(row['act'])} & {tex_escape(row['sanctuary_effect'])} \\\\"
        )
    return "\n".join([
        "\\section{Chronological Postconciliar Change Table (1963--2021)}",
        "Principal promulgated acts governing postconciliar sanctuary furnishings, sacred vessels, linens, books, vesture, and ministry distinctions from the Second Vatican Council through the 2011 United States implementation and its 2018--2021 official companions and emendations.",
        "",
        "{\\footnotesize\\begin{longtable}{>{\\raggedright\\arraybackslash}p{0.15\\linewidth}>{\\raggedright\\arraybackslash}p{0.33\\linewidth}>{\\raggedright\\arraybackslash}p{0.45\\linewidth}}",
        "\\toprule",
        "\\textbf{Date} & \\textbf{Promulgated act or edition} & \\textbf{Sanctuary and object effect} \\\\",
        "\\midrule",
        "\\endhead",
        *rows,
        "\\bottomrule",
        "\\end{longtable}}",
        "",
    ])


def render_keyed_notes(selected: list[dict]) -> str:
    rows = []
    for obj in sorted(selected, key=lambda o: o["sources"]["note_key"]):
        nkey = tex_escape(obj["sources"]["note_key"])
        eng = tex_escape(obj["preferred_english_name"])
        loci = "; ".join(tex_escape(x) for x in obj["sources"]["primary_loci"])
        c62_locus = tex_escape(obj["counterpart_1962"]["locus_1962"])
        sym_attr = obj["symbolism"].get("attribution", "")
        extra = f" 1962 counterpart: {c62_locus}." if c62_locus else ""
        if sym_attr:
            extra += f" Symbolism: {tex_escape(sym_attr)}."
        rows.append(f"\\textbf{{{nkey}}} & \\textbf{{{eng}}} & {loci}.{extra} \\\\")
    return "\n".join([
        "\\section{Keyed Source Notes}",
        "Each bracketed key on the plates resolves to the governing edition loci and 1962 comparison witnesses below.",
        "",
        "{\\footnotesize\\begin{longtable}{>{\\raggedright\\arraybackslash}p{0.08\\linewidth}>{\\raggedright\\arraybackslash}p{0.24\\linewidth}>{\\raggedright\\arraybackslash}p{0.61\\linewidth}}",
        "\\toprule",
        "\\textbf{Key} & \\textbf{Entry} & \\textbf{Governing loci and 1962 comparison} \\\\",
        "\\midrule",
        "\\endhead",
        *rows,
        "\\bottomrule",
        "\\end{longtable}}",
        "",
    ])


def render_scope_and_references(plates_cfg: dict, edition_meta: dict, current_count: int, superseded_count: int) -> str:
    refs_blocks = []
    for group in plates_cfg["references"]:
        refs_blocks.append(f"\\subsection*{{{tex_escape(group['heading'])}}}")
        refs_blocks.append("\\begin{itemize}")
        for entry in group["entries"]:
            refs_blocks.append(f"\\item {tex_escape(entry)}")
        refs_blocks.append("\\end{itemize}")

    if superseded_count > 0:
        coverage_para = (
            f"\\textbf{{Coverage and boundaries.}} Within this reference corpus, {current_count} principal sanctuary furnishings, "
            f"sacred vessels, linens, liturgical books, service items, and vestments of Mass and closely joined rites are documented "
            f"alongside {superseded_count} historically superseded postconciliar provisions. Episcopal and pontifical insignia "
            "(miter, crosier, pectoral cross, ring, zucchetto, gremiale, bugia), full Paschal Triduum apparatus "
            "(Paschal candle, Easter fire brazier, Good Friday adoration cross veil), funeral pall and catafalque, "
            "and specialized rites of dedication and ordination remain outside the present scope and are reserved for future "
            "expansion rather than treated by conjecture."
        )
        c62_sentence = (
            "Forms belonging to the 1962 Roman Missal appear only in explicit comparison fields and keyed source notes, "
            "never as postconciliar norms."
        )
    else:
        coverage_para = (
            f"\\textbf{{Coverage and boundaries.}} Within this practical reference, {current_count} principal sanctuary furnishings, "
            "sacred vessels, linens, liturgical books, service items, and vestments of Mass and closely joined rites are documented "
            "for active parish service; historically superseded postconciliar forms and full 1962 Roman Missal comparisons are "
            "collected separately in the comprehensive adult reference edition. Episcopal and pontifical insignia "
            "(miter, crosier, pectoral cross, ring, zucchetto, gremiale, bugia), full Paschal Triduum apparatus "
            "(Paschal candle, Easter fire brazier, Good Friday adoration cross veil), funeral pall and catafalque, "
            "and specialized rites of dedication and ordination remain outside the present scope and are reserved for future "
            "expansion rather than treated by conjecture."
        )
        c62_sentence = (
            "Counterpart references to the 1962 Roman Missal are restricted to the Keyed Source Notes "
            "(with full side-by-side comparisons in the comprehensive adult reference edition) and are never imported as postconciliar norms."
        )

    return "\n".join([
        "\\section{Scope, Edition, and Qualifications}",
        f"\\textbf{{Governing edition and jurisdiction.}} Entries in the {tex_escape(edition_meta['edition_noun'])} describe the Roman Rite as governed by the \\textit{{Missale Romanum}}, \\textit{{editio typica tertia}} (2002; \\textit{{reimpressio emendata}}, 2008), and its \\textit{{Institutio Generalis Missalis Romani}} (GIRM), together with the approved English edition for the United States of America, \\textit{{The Roman Missal, Third Edition}} (effective First Sunday of Advent, 27 November 2011), the adaptations approved by the United States Conference of Catholic Bishops (USCCB), the 2021 emendations incorporated in the official USCCB GIRM (Prot.~n.~228/20; Prot.~n.~394/21, 22 October 2021), and the 2021 amendment of canon 230 \\S1 (\\textit{{Spiritus Domini}}, 10 January 2021). Norms are stated as of 2026-11-25.",
        "",
        coverage_para,
        "",
        f"\\textbf{{Separation of universal law, territorial adaptation, and custom.}} Universal provisions of the Latin typical edition (including choices entrusted to the Diocesan Bishop, such as tabernacle placement at GIRM 315), approved United States adaptations (solid wood fixed altars at GIRM 301, festive under-cloths at GIRM 304, sacred-vessel materials at GIRM 329, lay ministerial attire at GIRM 339, Communion under both kinds at GIRM 283 and the USCCB Norms, and funeral and solemn vestment colors at GIRM 346e and 346h), diocesan or celebrant options, and documented parish custom are distinguished throughout. {c62_sentence}",
        "",
        "\\textbf{Rights, visual provenance, and reliance boundary.} All ten monochrome graphite plates are original project-created illustrations normalized to 8-bit grayscale on pure white ground; no third-party scans, photographs, or copyrighted illustrations are reproduced. English descriptions paraphrase official liturgical law in original prose without reproducing protected ICEL liturgical prayer texts or rubrical formulations verbatim. English Scripture quotations follow the public-domain Douay--Rheims (Challoner) text. The approved Roman Missal and diocesan directives remain the governing liturgical law; study and preparation notes here carry no official, liturgical, or magisterial authority.",
        "",
        "\\phantomsection",
        "\\section*{References}",
        "\\addcontentsline{toc}{section}{References}",
        *refs_blocks,
        "",
    ])


def render_server_quick_table(current_objs: list[dict]) -> str:
    rows = []
    for obj in current_objs:
        mh = obj["ministers_and_handling"]
        rows.append(
            f"\\textbf{{{tex_escape(obj['preferred_english_name'])}}} & {tex_escape(SERVER_BOUNDARY_LABELS[mh['server_boundary']])} & {tex_escape(mh['server_boundary_summary'])} \\\\"
        )
    return "\n".join([
        "\\section{Altar Server Quick-Reference Handling Chart}",
        "A category-ordered summary of all forty sanctuary objects, distinguishing what an altar server prepares, carries, or presents from what remains reserved to clergy or instituted ministers.",
        "",
        "{\\footnotesize\\begin{longtable}{>{\\raggedright\\arraybackslash}p{0.23\\linewidth}>{\\raggedright\\arraybackslash}p{0.27\\linewidth}>{\\raggedright\\arraybackslash}p{0.43\\linewidth}}",
        "\\toprule",
        "\\textbf{Object} & \\textbf{Boundary} & \\textbf{Practical rule} \\\\",
        "\\midrule",
        "\\endhead",
        *rows,
        "\\bottomrule",
        "\\end{longtable}}",
        "",
    ])


def render_sacristan_checklist(plates_cfg: dict) -> str:
    blocks = [
        "\\section{Sacristy Preparation Checklist by Liturgical Moment}",
        "Practical verification sequence grounded in GIRM 117--119, 304--316, 327--349, and the 2011 United States adaptations.",
        "",
    ]
    for group in plates_cfg["sacristan_checklist"]:
        blocks.append(f"\\subsection*{{{tex_escape(group['stage'])}}}")
        blocks.append("\\begin{itemize}")
        for item in group["items"]:
            blocks.append(f"\\item {tex_escape(item)}")
        blocks.append("\\end{itemize}")
    blocks.append("")
    return "\n".join(blocks)


def render_1962_continuity_table(current_objs: list[dict]) -> str:
    rows = []
    for obj in current_objs:
        c62 = obj["counterpart_1962"]
        rows.append(
            f"\\textbf{{{tex_escape(obj['preferred_english_name'])}}} & \\PCDTag{{{tex_escape(c62['relationship'])}}} & {tex_escape(c62['comparison'])} \\\\"
        )
    return "\n".join([
        "\\subsection*{Summary of Continuity and Change from the 1962 Roman Missal}",
        "{\\footnotesize\\begin{longtable}{>{\\raggedright\\arraybackslash}p{0.21\\linewidth}>{\\raggedright\\arraybackslash}p{0.19\\linewidth}>{\\raggedright\\arraybackslash}p{0.53\\linewidth}}",
        "\\toprule",
        "\\textbf{Object} & \\textbf{Relationship} & \\textbf{Direct edition comparison} \\\\",
        "\\midrule",
        "\\endhead",
        *rows,
        "\\bottomrule",
        "\\end{longtable}}",
        "",
    ])


def render_object_inventory_md(objects: dict[str, dict], plates_by_id: dict[str, dict]) -> str:
    ordered = sorted(objects.values(), key=lambda o: (o["sort_order"], o["id"]))
    current = [o for o in ordered if not o["historical_transition"].get("is_superseded")]
    superseded = [o for o in ordered if o["historical_transition"].get("is_superseded")]
    lines = [
        "# Canonical Object Inventory",
        "",
        "> Derived mechanically from `shared/objects/**/*.toml` by `shared/generate_editions.py`.",
        "> Do not hand-edit this table; update the canonical TOML records and re-run `--write`.",
        "",
        f"- **Declared edition-locale:** `2008-latin-2011-us-english` (*Missale Romanum* 2002/2008 + US Roman Missal 2011)",
        f"- **As-of date:** 2026-11-25",
        f"- **Total canonical records:** {len(ordered)} ({len(current)} current postconciliar sanctuary objects + {len(superseded)} historically superseded postconciliar forms)",
        "",
        "## Current Postconciliar Sanctuary Objects",
        "",
        "| ID | English | Latin | Category | Disposition | Server Boundary | 1962 Counterpart | Plate | Note |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for o in current:
        pl = plates_by_id[o["plate_id"]]["short_label"]
        lines.append(
            f"| `{o['id']}` | {o['preferred_english_name']} | *{o['latin_headword']}* | `{o['category']}` | "
            f"`{o['edition_disposition']['disposition']}` | `{o['ministers_and_handling']['server_boundary']}` | "
            f"`{o['counterpart_1962']['relationship']}` | {pl} | {o['sources']['note_key']} |"
        )
    lines += [
        "",
        "## Historically Superseded Postconciliar Forms (Chronological Separation)",
        "",
        "| ID | Form | Latin | Period | Controlling Act | Disposition | Note |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for o in superseded:
        ht = o["historical_transition"]
        lines.append(
            f"| `{o['id']}` | {o['preferred_english_name']} | *{o['latin_headword']}* | "
            f"{ht['period_range']} | {ht['controlling_act']} | `{o['edition_disposition']['disposition']}` | {o['sources']['note_key']} |"
        )
    lines.append("")
    return "\n".join(lines)


def build_all_outputs(plates_cfg: dict, art_manifest: dict, objects: dict[str, dict]) -> dict[Path, str]:
    plates_by_id = {p["id"]: p for p in plates_cfg["plates"]}
    art_by_id = {a["id"]: a for a in art_manifest["artworks"]}
    ordered = sorted(objects.values(), key=lambda o: (o["sort_order"], o["id"]))
    current_all = [o for o in ordered if not o["historical_transition"].get("is_superseded")]
    superseded_all = [o for o in ordered if o["historical_transition"].get("is_superseded")]

    def objs_for_cat(cat: str, edition_key: str) -> list[dict]:
        return [o for o in current_all if o["category"] == cat and o["audiences"].get(edition_key, False)]

    def objs_by_ids(ids: list[str], edition_key: str) -> list[dict]:
        return [objects[i] for i in ids if objects[i]["audiences"].get(edition_key, False)]

    outputs: dict[Path, str] = {}
    outputs[OWNER / "research/object-inventory.md"] = render_object_inventory_md(objects, plates_by_id)

    # ------------------------------------------------------------------
    # 1. COMPREHENSIVE ADULT REFERENCE EDITION
    # ------------------------------------------------------------------
    comp_dir = OWNER / "comprehensive/sections"
    comp_meta = plates_cfg["editions"]["comprehensive"]

    outputs[comp_dir / "00-key-and-sanctuary.tex"] = "\n".join([
        "\\section{The Postconciliar Roman Sanctuary}",
        tex_escape(comp_meta["opening_prose"]),
        "",
        render_plate_block(plates_by_id["pc-plt-01-sanctuary"], art_by_id["pc-art-01-sanctuary-composition"], hero=True),
        tex_escape(comp_meta["sanctuary_reading_prose"]),
        "",
        render_disposition_key(),
        render_color_key(plates_cfg),
    ])

    outputs[comp_dir / "10-sanctuary-furnishings.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Sanctuary Furnishings}",
        tex_escape(plates_cfg["category_intros"]["sanctuary-furnishings"]),
        "",
        render_plate_block(plates_by_id["pc-plt-02-furnishings"], art_by_id["pc-art-02-altar-ambo-chair"]),
        *[render_object_entry(o, objects, "comprehensive") for o in objs_for_cat("sanctuary-furnishings", "comprehensive")],
    ])

    outputs[comp_dir / "20-sacred-vessels.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Sacred Vessels and Communion Vessels}",
        tex_escape(plates_cfg["category_intros"]["sacred-vessels"]),
        "",
        render_plate_block(plates_by_id["pc-plt-03-vessels"], art_by_id["pc-art-03-sacred-vessels"]),
        *[render_object_entry(o, objects, "comprehensive") for o in objs_for_cat("sacred-vessels", "comprehensive")],
    ])

    outputs[comp_dir / "30-altar-linens.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Altar and Vessel Linens}",
        tex_escape(plates_cfg["category_intros"]["linens"]),
        "",
        render_plate_block(plates_by_id["pc-plt-04-linens"], art_by_id["pc-art-04-white-linens"]),
        *[render_object_entry(o, objects, "comprehensive") for o in objs_for_cat("linens", "comprehensive")],
    ])

    outputs[comp_dir / "40-liturgical-books.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Liturgical Books and Stands}",
        tex_escape(plates_cfg["category_intros"]["liturgical-books"]),
        "",
        render_plate_block(plates_by_id["pc-plt-05-books"], art_by_id["pc-art-05-liturgical-books"]),
        *[render_object_entry(o, objects, "comprehensive") for o in objs_for_cat("liturgical-books", "comprehensive")],
    ])

    service_non_incense = [
        "pc-obj-processional-cross", "pc-obj-altar-candles",
        "pc-obj-sanctuary-bells", "pc-obj-aspergillum-aspersorium",
    ]
    incense_ids = ["pc-obj-thurible", "pc-obj-incense-boat"]
    outputs[comp_dir / "50-service-and-incense.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Service Equipment and Incense}",
        tex_escape(plates_cfg["category_intros"]["service-and-incense"]),
        "",
        render_plate_block(plates_by_id["pc-plt-06-service"], art_by_id["pc-art-06-service-cruets-bells"]),
        *[render_object_entry(o, objects, "comprehensive") for o in objs_by_ids(service_non_incense, "comprehensive")],
        "\\clearpage",
        "\\subsection{Incense Equipment}",
        render_plate_block(plates_by_id["pc-plt-07-incense"], art_by_id["pc-art-07-incense-set"]),
        *[render_object_entry(o, objects, "comprehensive") for o in objs_by_ids(incense_ids, "comprehensive")],
    ])

    ordained_vesture = ["pc-obj-alb", "pc-obj-cincture", "pc-obj-amice", "pc-obj-stole", "pc-obj-chasuble", "pc-obj-dalmatic"]
    choir_solemn_vesture = ["pc-obj-cassock-surplice", "pc-obj-cope", "pc-obj-humeral-veil"]
    outputs[comp_dir / "60-vesture-and-ministry.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Vesture and Ministry Distinctions}",
        tex_escape(plates_cfg["category_intros"]["vesture-and-ministry"]),
        "",
        render_ministry_table(plates_cfg),
        "\\clearpage",
        "\\subsection{Ordained Vesture at Mass}",
        render_plate_block(plates_by_id["pc-plt-08-vesture-ordained"], art_by_id["pc-art-08-priest-deacon-vesture"]),
        *[render_object_entry(o, objects, "comprehensive") for o in objs_by_ids(ordained_vesture, "comprehensive")],
        "\\clearpage",
        "\\subsection{Choir Dress and Solemn Ceremonial Vesture}",
        render_plate_block(plates_by_id["pc-plt-09-vesture-choir-solemn"], art_by_id["pc-art-09-black-cassock-surplice-cope"]),
        *[render_object_entry(o, objects, "comprehensive") for o in objs_by_ids(choir_solemn_vesture, "comprehensive")],
    ])

    outputs[comp_dir / "70-communion-and-adjacent.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Communion Under Both Kinds and Sacramental Vessels}",
        tex_escape(plates_cfg["category_intros"]["sacramental-adjacent"]),
        "",
        render_plate_block(plates_by_id["pc-plt-10-communion-sacramental"], art_by_id["pc-art-10-communion-triduum-vessels"]),
        *[render_object_entry(o, objects, "comprehensive") for o in objs_for_cat("sacramental-adjacent", "comprehensive")],
    ])

    outputs[comp_dir / "80-superseded-postconciliar.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Historically Superseded Postconciliar Forms (1967--2011)}",
        tex_escape(plates_cfg["category_intros"]["superseded-postconciliar"]),
        "",
        *[render_superseded_entry(o) for o in superseded_all],
    ])

    outputs[comp_dir / "90-pronunciation-and-indexes.tex"] = "\n".join([
        "\\clearpage",
        render_pronunciation_appendix(ordered),
        "\\clearpage",
        render_indexes(ordered, plates_by_id),
    ])

    outputs[comp_dir / "95-chronology-and-notes.tex"] = "\n".join([
        "\\clearpage",
        render_chronology_table(plates_cfg),
        "\\clearpage",
        render_keyed_notes(ordered),
    ])

    outputs[comp_dir / "98-scope-and-references.tex"] = "\n".join([
        "\\clearpage",
        render_scope_and_references(plates_cfg, comp_meta, len(current_all), len(superseded_all)),
    ])

    # ------------------------------------------------------------------
    # 2. ALTAR SERVER VISUAL DICTIONARY
    # ------------------------------------------------------------------
    srv_dir = OWNER / "altar-server/sections"
    srv_meta = plates_cfg["editions"]["altar-server"]
    srv_objs = [o for o in current_all if o["audiences"].get("altar_server", False)]

    outputs[srv_dir / "00-server-key-and-sanctuary.tex"] = "\n".join([
        "\\section{Serving in the Postconciliar Sanctuary}",
        tex_escape(srv_meta["opening_prose"]),
        "",
        render_plate_block(plates_by_id["pc-plt-01-sanctuary"], art_by_id["pc-art-01-sanctuary-composition"], hero=True),
        "\\subsection*{Knowing What You Handle and What Only Clergy Handle}",
        "An altar server encounters many sacred things around the sanctuary, including vessels and books reserved strictly to the priest, deacon, or instituted acolyte. "
        "Each entry below marks whether you prepare, carry, or present the item, move it only when directed, or recognize it without touching it.",
        "",
    ])

    outputs[srv_dir / "10-sanctuary-and-furnishings.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Sanctuary Places and Furnishings}",
        render_plate_block(plates_by_id["pc-plt-02-furnishings"], art_by_id["pc-art-02-altar-ambo-chair"]),
        *[render_object_entry(o, objects, "altar-server") for o in objs_for_cat("sanctuary-furnishings", "altar_server")],
    ])

    outputs[srv_dir / "20-vessels-and-linens.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Sacred Vessels and Altar Linens}",
        render_plate_block(plates_by_id["pc-plt-03-vessels"], art_by_id["pc-art-03-sacred-vessels"]),
        *[render_object_entry(o, objects, "altar-server") for o in objs_for_cat("sacred-vessels", "altar_server")],
        "\\clearpage",
        "\\subsection{Altar and Vessel Linens}",
        render_plate_block(plates_by_id["pc-plt-04-linens"], art_by_id["pc-art-04-white-linens"]),
        *[render_object_entry(o, objects, "altar-server") for o in objs_for_cat("linens", "altar_server")],
    ])

    outputs[srv_dir / "30-books-service-incense.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Liturgical Books, Service Items, and Incense}",
        render_plate_block(plates_by_id["pc-plt-05-books"], art_by_id["pc-art-05-liturgical-books"]),
        *[render_object_entry(o, objects, "altar-server") for o in objs_for_cat("liturgical-books", "altar_server")],
        "\\clearpage",
        "\\subsection{Processional and Service Equipment}",
        render_plate_block(plates_by_id["pc-plt-06-service"], art_by_id["pc-art-06-service-cruets-bells"]),
        *[render_object_entry(o, objects, "altar-server") for o in objs_by_ids(service_non_incense, "altar_server")],
        "\\clearpage",
        "\\subsection{Thurible, Charcoal, and Incense Boat}",
        render_plate_block(plates_by_id["pc-plt-07-incense"], art_by_id["pc-art-07-incense-set"]),
        *[render_object_entry(o, objects, "altar-server") for o in objs_by_ids(incense_ids, "altar_server")],
    ])

    outputs[srv_dir / "40-vesture-and-ministers.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Recognizing Ministers and Vestments}",
        render_ministry_table(plates_cfg),
        "\\clearpage",
        render_plate_block(plates_by_id["pc-plt-08-vesture-ordained"], art_by_id["pc-art-08-priest-deacon-vesture"]),
        *[render_object_entry(o, objects, "altar-server") for o in objs_by_ids(ordained_vesture, "altar_server")],
        "\\clearpage",
        render_plate_block(plates_by_id["pc-plt-09-vesture-choir-solemn"], art_by_id["pc-art-09-black-cassock-surplice-cope"]),
        *[render_object_entry(o, objects, "altar-server") for o in objs_by_ids(choir_solemn_vesture, "altar_server")],
        "\\clearpage",
        render_plate_block(plates_by_id["pc-plt-10-communion-sacramental"], art_by_id["pc-art-10-communion-triduum-vessels"]),
        *[render_object_entry(o, objects, "altar-server") for o in objs_for_cat("sacramental-adjacent", "altar_server")],
    ])

    outputs[srv_dir / "90-apparatus.tex"] = "\n".join([
        "\\clearpage",
        render_server_quick_table(srv_objs),
        "\\clearpage",
        render_pronunciation_appendix(srv_objs),
        "\\clearpage",
        render_indexes(srv_objs, plates_by_id),
        "\\clearpage",
        render_keyed_notes(srv_objs),
        "\\clearpage",
        render_scope_and_references(plates_cfg, srv_meta, len(srv_objs), 0),
    ])

    # ------------------------------------------------------------------
    # 3. SACRISTAN VISUAL DICTIONARY
    # ------------------------------------------------------------------
    sac_dir = OWNER / "sacristan/sections"
    sac_meta = plates_cfg["editions"]["sacristan"]
    sac_objs = [o for o in current_all if o["audiences"].get("sacristan", False)]

    outputs[sac_dir / "00-sacristan-key-and-sanctuary.tex"] = "\n".join([
        "\\section{Sanctuary Preparation and Furnishings}",
        tex_escape(sac_meta["opening_prose"]),
        "",
        render_plate_block(plates_by_id["pc-plt-01-sanctuary"], art_by_id["pc-art-01-sanctuary-composition"], hero=True),
        render_color_key(plates_cfg),
        "\\clearpage",
        render_plate_block(plates_by_id["pc-plt-02-furnishings"], art_by_id["pc-art-02-altar-ambo-chair"]),
        *[render_object_entry(o, objects, "sacristan") for o in objs_for_cat("sanctuary-furnishings", "sacristan")],
    ])

    outputs[sac_dir / "10-vessels-and-communion.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Sacred Vessels, Communion Arrangement, and Holy Oils}",
        render_plate_block(plates_by_id["pc-plt-03-vessels"], art_by_id["pc-art-03-sacred-vessels"]),
        *[render_object_entry(o, objects, "sacristan") for o in objs_for_cat("sacred-vessels", "sacristan")],
        "\\clearpage",
        render_plate_block(plates_by_id["pc-plt-10-communion-sacramental"], art_by_id["pc-art-10-communion-triduum-vessels"]),
        *[render_object_entry(o, objects, "sacristan") for o in objs_for_cat("sacramental-adjacent", "sacristan")],
    ])

    outputs[sac_dir / "20-linens-and-books.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Altar Linens and Liturgical Books}",
        render_plate_block(plates_by_id["pc-plt-04-linens"], art_by_id["pc-art-04-white-linens"]),
        *[render_object_entry(o, objects, "sacristan") for o in objs_for_cat("linens", "sacristan")],
        "\\clearpage",
        render_plate_block(plates_by_id["pc-plt-05-books"], art_by_id["pc-art-05-liturgical-books"]),
        *[render_object_entry(o, objects, "sacristan") for o in objs_for_cat("liturgical-books", "sacristan")],
    ])

    outputs[sac_dir / "30-service-incense-vesture.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Service Equipment, Incense, and Vesture Preparation}",
        render_plate_block(plates_by_id["pc-plt-06-service"], art_by_id["pc-art-06-service-cruets-bells"]),
        *[render_object_entry(o, objects, "sacristan") for o in objs_by_ids(service_non_incense, "sacristan")],
        "\\clearpage",
        render_plate_block(plates_by_id["pc-plt-07-incense"], art_by_id["pc-art-07-incense-set"]),
        *[render_object_entry(o, objects, "sacristan") for o in objs_by_ids(incense_ids, "sacristan")],
        "\\clearpage",
        render_plate_block(plates_by_id["pc-plt-08-vesture-ordained"], art_by_id["pc-art-08-priest-deacon-vesture"]),
        *[render_object_entry(o, objects, "sacristan") for o in objs_by_ids(ordained_vesture, "sacristan")],
        "\\clearpage",
        render_plate_block(plates_by_id["pc-plt-09-vesture-choir-solemn"], art_by_id["pc-art-09-black-cassock-surplice-cope"]),
        *[render_object_entry(o, objects, "sacristan") for o in objs_by_ids(choir_solemn_vesture, "sacristan")],
    ])

    outputs[sac_dir / "90-apparatus.tex"] = "\n".join([
        "\\clearpage",
        render_sacristan_checklist(plates_cfg),
        "\\clearpage",
        render_pronunciation_appendix(sac_objs),
        "\\clearpage",
        render_indexes(sac_objs, plates_by_id),
        "\\clearpage",
        render_keyed_notes(sac_objs),
        "\\clearpage",
        render_scope_and_references(plates_cfg, sac_meta, len(sac_objs), 0),
    ])

    # ------------------------------------------------------------------
    # 4. GENERAL READER VISUAL DICTIONARY
    # ------------------------------------------------------------------
    gen_dir = OWNER / "general-reader/sections"
    gen_meta = plates_cfg["editions"]["general-reader"]
    gen_objs = [o for o in current_all if o["audiences"].get("general_reader", False)]

    outputs[gen_dir / "00-sanctuary-and-furnishings.tex"] = "\n".join([
        "\\section{Inside the Postconciliar Roman Sanctuary}",
        tex_escape(gen_meta["opening_prose"]),
        "",
        render_plate_block(plates_by_id["pc-plt-01-sanctuary"], art_by_id["pc-art-01-sanctuary-composition"], hero=True),
        render_color_key(plates_cfg),
        "\\clearpage",
        render_plate_block(plates_by_id["pc-plt-02-furnishings"], art_by_id["pc-art-02-altar-ambo-chair"]),
        *[render_object_entry(o, objects, "general-reader") for o in objs_for_cat("sanctuary-furnishings", "general_reader")],
    ])

    outputs[gen_dir / "10-vessels-and-linens.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Sacred Vessels and Altar Linens}",
        render_plate_block(plates_by_id["pc-plt-03-vessels"], art_by_id["pc-art-03-sacred-vessels"]),
        *[render_object_entry(o, objects, "general-reader") for o in objs_for_cat("sacred-vessels", "general_reader")],
        "\\clearpage",
        render_plate_block(plates_by_id["pc-plt-04-linens"], art_by_id["pc-art-04-white-linens"]),
        *[render_object_entry(o, objects, "general-reader") for o in objs_for_cat("linens", "general_reader")],
    ])

    outputs[gen_dir / "20-books-service-incense.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Books, Processional Items, and Incense}",
        render_plate_block(plates_by_id["pc-plt-05-books"], art_by_id["pc-art-05-liturgical-books"]),
        *[render_object_entry(o, objects, "general-reader") for o in objs_for_cat("liturgical-books", "general_reader")],
        "\\clearpage",
        render_plate_block(plates_by_id["pc-plt-06-service"], art_by_id["pc-art-06-service-cruets-bells"]),
        *[render_object_entry(o, objects, "general-reader") for o in objs_by_ids(service_non_incense, "general_reader")],
        "\\clearpage",
        render_plate_block(plates_by_id["pc-plt-07-incense"], art_by_id["pc-art-07-incense-set"]),
        *[render_object_entry(o, objects, "general-reader") for o in objs_by_ids(incense_ids, "general_reader")],
    ])

    outputs[gen_dir / "30-vesture-and-communion.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Vestments, Ministries, and Communion Vessels}",
        render_plate_block(plates_by_id["pc-plt-08-vesture-ordained"], art_by_id["pc-art-08-priest-deacon-vesture"]),
        *[render_object_entry(o, objects, "general-reader") for o in objs_by_ids(ordained_vesture, "general_reader")],
        "\\clearpage",
        render_plate_block(plates_by_id["pc-plt-09-vesture-choir-solemn"], art_by_id["pc-art-09-black-cassock-surplice-cope"]),
        *[render_object_entry(o, objects, "general-reader") for o in objs_by_ids(choir_solemn_vesture, "general_reader")],
        "\\clearpage",
        render_plate_block(plates_by_id["pc-plt-10-communion-sacramental"], art_by_id["pc-art-10-communion-triduum-vessels"]),
        *[render_object_entry(o, objects, "general-reader") for o in objs_for_cat("sacramental-adjacent", "general_reader")],
    ])

    outputs[gen_dir / "40-postconciliar-continuity.tex"] = "\n".join([
        "\\clearpage",
        "\\section{Continuity with the 1962 Missal and Postconciliar Developments}",
        render_1962_continuity_table(gen_objs),
        "\\subsection*{Historically Superseded Postconciliar Forms (1967--2011)}",
        *[render_superseded_entry(o) for o in superseded_all],
    ])

    outputs[gen_dir / "90-apparatus.tex"] = "\n".join([
        "\\clearpage",
        render_pronunciation_appendix(gen_objs + superseded_all),
        "\\clearpage",
        render_indexes(gen_objs + superseded_all, plates_by_id),
        "\\clearpage",
        render_keyed_notes(gen_objs + superseded_all),
        "\\clearpage",
        render_scope_and_references(plates_cfg, gen_meta, len(gen_objs), len(superseded_all)),
    ])

    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate canonical TOML sanctuary objects and project four dictionary editions.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Validate canonical records and write all generated sections and inventory.")
    mode.add_argument("--check", action="store_true", help="Validate canonical records and verify zero drift across all generated files.")
    args = parser.parse_args(argv)

    _, plates_cfg, art_manifest, objects, errors = load_and_validate()
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    outputs = build_all_outputs(plates_cfg, art_manifest, objects)

    if args.write:
        for path, content in sorted(outputs.items()):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        current = sum(1 for o in objects.values() if not o["historical_transition"].get("is_superseded"))
        sup = len(objects) - current
        print(f"Generated {len(outputs)} files from {len(objects)} canonical records ({current} current + {sup} superseded) and {len(art_manifest['artworks'])} verified plates.")
        return 0

    drift = []
    for path, expected in sorted(outputs.items()):
        if not path.is_file():
            drift.append(f"MISSING: {path.relative_to(OWNER)}")
        elif path.read_text(encoding="utf-8") != expected:
            drift.append(f"DRIFT: {path.relative_to(OWNER)}")
    if drift:
        for d in drift:
            print(f"ERROR: {d}", file=sys.stderr)
        return 1

    current = sum(1 for o in objects.values() if not o["historical_transition"].get("is_superseded"))
    sup = len(objects) - current
    print(f"OK: {len(objects)} canonical records ({current} current + {sup} superseded), {len(art_manifest['artworks'])} verified monochrome plates, {len(outputs)} generated files in sync.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
