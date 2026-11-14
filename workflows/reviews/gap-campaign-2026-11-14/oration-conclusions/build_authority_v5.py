"""Reproducible successor of the finite oration-conclusion authority (v4 -> v5).

v5 keeps v4's scope and every v4 record and field. For exactly the records named in DECLARED it recomputes, from the
repository's current source records, every hash v4 pinned for them: the calendar proper (proper_sha256 and
body_fidelity.canonical_proper_sha256), the Latin proof row (latin_proof_sha256), the translation binding, the
selected body and its cue offsets, each source control's pinned hash (relocating a JSON pointer whose list index
moved, by record identity), and the public descriptor hash. Any other drift is refused, and every undeclared record
is checked unchanged by the repository's own loaders.

It then writes, deterministically:
  workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/authority-v5.json
  workflows/reviews/missal-reader-resume-2026-11-12/english-editorial-readings/authority-v3.json (+ successor review)
  workflows/reviews/gap-campaign-2026-11-14/oration-conclusions/v5-successor-receipt.json (text-free)
  workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/root-adoption-v5.json (activation record)
and updates the pins in scripts/_oration_endings.py, src/web/browser/liturgy/oration-conclusions.js and the two
authority path lists (scripts/_browser_product_recipes.py, scripts/_corpus_index.py).

Usage (repository root):
  python3 workflows/reviews/gap-campaign-2026-11-14/oration-conclusions/build_authority_v5.py          # write
  python3 workflows/reviews/gap-campaign-2026-11-14/oration-conclusions/build_authority_v5.py --check  # verify only
If a declared record's source later changes (for example an English correction after review), re-run without
--check; to add a record, add it to DECLARED with its justification.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.machinery
import importlib.util
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import _oration_endings as endings  # noqa: E402
import _oration_conclusion_supplement as supplement  # noqa: E402

HERE = "workflows/reviews/gap-campaign-2026-11-14/oration-conclusions"
V4 = "workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/authority-v4.json"
V4_SHA256 = "b26fe7863979e300ea47ad925e22d77d783dd76a418672b516eba73cac166744"
V5 = "workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/authority-v5.json"
ED = "workflows/reviews/missal-reader-resume-2026-11-12/english-editorial-readings"
ED_V2, ED_V2_SHA256 = f"{ED}/authority-v2.json", "231c2cfa81cc193060d5d00ab85882b0b1ae2c4b3b22a9380df524931c1de1d3"
ED_V3, ED_REVIEW = f"{ED}/authority-v3.json", f"{ED}/gap-campaign-v5-ending-successor-review.json"
RECEIPT = f"{HERE}/v5-successor-receipt.json"
ADOPTION = "workflows/reviews/missal-reader-completion-2026-11-12/oration-conclusions/root-adoption-v5.json"
PY, JS = "scripts/_oration_endings.py", "src/web/browser/liturgy/oration-conclusions.js"
LISTS = ("scripts/_browser_product_recipes.py", "scripts/_corpus_index.py")
HELD = "workflows/reviews/gap-campaign-2026-11-14/postconciliar/held-v5-admission.json"

_HELD_JUST = "Latin body admitted (gap campaign 2026-11-14, held-v5 installation, coordinator authorization); receipt " + HELD
DECLARED = {
    ("postconciliar", "ascension", "day", "Collect", "all", 2): _HELD_JUST + " (lane index p3#24)",
    ("postconciliar", "epiphany", "day", "Collect", "all", 1): _HELD_JUST + " (lane index p1#55)",
    **{("postconciliar", f"ot-{n}", "main", "Collect", "all", 1): _HELD_JUST + f" (lane index p4#{i})"
       for n, i in ((2, 26), (3, 29), (7, 39), (9, 44), (12, 51), (20, 70), (21, 71), (24, 79), (26, 86), (27, 89),
                    (28, 92), (29, 95), (30, 97), (31, 100), (32, 103), (33, 104))},
    ("roman-1962", "low-sunday", "main", "Secret", "all", 1): ("Latin proof row re-sourced from Pustet 1862 (prints qui) to Mame 1922 p. 373 (cui), "
                                                               "DECISIONS 7f; body bytes unchanged; receipt " + HELD),
}
LATIN_NOW_HELD = "not-in-this-english-only-record"


def sha(value):
    return endings.sha(value)


def canonical(value):
    return endings.canonical(value)


def utf16(text):
    return len(text.encode("utf-16-le")) // 2


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def owner_module():
    loader = importlib.machinery.SourceFileLoader("_v5_owner", str(ROOT / "tools/mass-propers"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class Context:
    def __init__(self):
        self.owner = owner_module()
        self.root = ROOT / "src/sources/calendars"
        self.docs, self.masses, self.files = {}, {}, {}

    def document(self, calendar):
        if calendar not in self.docs:
            doc = self.owner.load_calendar(self.root, calendar)
            self.docs[calendar] = doc
            self.masses[calendar] = {m["key"]: m for _, m in self.owner.masses_of(doc)}
        return self.docs[calendar]

    def parsed(self, path):
        if path not in self.files:
            raw = (ROOT / path).read_bytes()
            value = tomllib.loads(raw.decode()) if path.endswith(".toml") else (json.loads(raw) if path.endswith(".json") else None)
            self.files[path] = (raw, value)
        return self.files[path]


def control_value(ctx, control):
    raw, parsed = ctx.parsed(control["path"])
    if "json_pointer" in control:
        return hashlib.sha256(canonical(supplement.pointer(parsed, control["json_pointer"])).encode()).hexdigest()
    return hashlib.sha256(raw).hexdigest()


def relocate(ctx, control, calendar, target):
    """A pointer control whose list index moved: find the same record by identity in the same list."""
    raw, parsed = ctx.parsed(control["path"])
    ptr = control["json_pointer"]
    m = re.fullmatch(r"/(\w+)/(\d+)", ptr)
    if not m:
        return None
    rows = parsed[m.group(1)]
    doc = ctx.document(calendar)
    kind = control.get("kind")
    want = tuple(target)
    for index, row in enumerate(rows):
        try:
            if kind == "translation-binding":
                same = ctx.owner.translation_record_identity(row, doc) == want
            elif kind == "latin-proof":
                mass = ctx.masses[calendar].get(row.get("mass"))
                same = mass is not None and (row["mass"], ctx.owner.form_id_for_label(mass, row.get("form", "")), row["proper"],
                                             row.get("cycle") or "all", row["occurrence"]) == want
            else:
                return None
        except Exception:
            same = False
        if same:
            return f"/{m.group(1)}/{index}"
    return None


def recompute_supplemental(ctx, row, changes):
    calendar, target = row["calendar"], row["target"]
    doc = ctx.document(calendar)
    proper = supplement.direct_source(ctx.owner, doc, ctx.masses[calendar], target)
    public = row["public"]
    fidelity_before = copy.deepcopy(public.get("body_fidelity", {}))
    for language, native in row["languages"].items():
        new = native
        before = copy.deepcopy(native)
        for control in new["source_controls"]:
            if "json_pointer" in control and control.get("kind") in ("translation-binding", "latin-proof"):
                moved = relocate(ctx, control, calendar, target)
                if moved and moved != control["json_pointer"]:
                    control["json_pointer"] = moved
            control["sha256"] = control_value(ctx, control)
        new["proper_sha256"] = sha(proper)
        if language == "la":
            text = proper.get("text")
            proofs = [c for c in new["source_controls"] if c.get("kind") == "latin-proof"]
            if proofs:
                _, parsed = ctx.parsed(proofs[0]["path"])
                new["latin_proof_sha256"] = sha(supplement.pointer(parsed, proofs[0]["json_pointer"]))
        else:
            bindings = [c for c in new["source_controls"] if c.get("kind") == "translation-binding"]
            if len(bindings) != 1:
                raise SystemExit(f"{calendar} {target} {language}: needs exactly one translation-binding control")
            _, parsed = ctx.parsed(bindings[0]["path"])
            binding = supplement.pointer(parsed, bindings[0]["json_pointer"])
            if ctx.owner.translation_record_identity(binding, doc) != tuple(target):
                raise SystemExit(f"{calendar} {target}: translation binding identity differs")
            new["translation_binding_sha256"] = sha(binding)
            held = [t for t in binding["translations"] if t.get("lang") == "en" and (t.get("source_id") or "") == (native["source_id"] or "")]
            if len(held) != 1:
                raise SystemExit(f"{calendar} {target}: English witness not unique")
            text = held[0]["text"]
        part = public["languages"][language]
        if not isinstance(text, str) or not text.endswith(part["cue"]):
            raise SystemExit(f"{calendar} {target} {language}: body no longer ends with its reviewed cue")
        new["body_sha256"] = sha(text)
        new["cue_end"] = utf16(text)
        new["cue_start"] = utf16(text[: len(text) - len(part["cue"])])
        part.update(body_sha256=new["body_sha256"], cue_start=new["cue_start"], cue_end=new["cue_end"])
        fidelity = public.get("body_fidelity", {}).get(language)
        if isinstance(fidelity, dict):
            for key, value in (("canonical_proper_sha256", new["proper_sha256"]), ("source_body_sha256", new["body_sha256"]),
                               ("binding_sha256", new.get("translation_binding_sha256"))):
                if key in fidelity and value is not None:
                    fidelity[key] = value
            has_latin = isinstance(proper.get("text"), str) and bool(proper["text"].strip())
            if "canonical_latin_body_available" in fidelity and fidelity["canonical_latin_body_available"] != has_latin:
                fidelity["canonical_latin_body_available"] = has_latin
                if has_latin and "la" not in row["languages"] and fidelity.get("latin_execution_verdict") == "not-supported-no-held-body":
                    fidelity["latin_execution_verdict"] = LATIN_NOW_HELD
                fidelity["successor_2026_11_14"] = {
                    "canonical_latin_body_available": has_latin,
                    "basis": "Latin body admitted from a public-domain witness after this review (gap campaign 2026-11-14; " + HELD + ").",
                    "latin_execution": "This record remains English-only; the admitted Latin body prints its own target conclusion cue and is not executed here.",
                    "holds": "The review's holds are retained as recorded; the hold no-canonical-latin-body-or-latin-execution is superseded for the Latin body only.",
                }
        for key in sorted(set(before) | set(new)):
            if key == "source_controls":
                for i, (a, b) in enumerate(zip(before["source_controls"], new["source_controls"])):
                    for field in ("sha256", "json_pointer"):
                        if a.get(field) != b.get(field):
                            changes.append({"field": f"languages.{language}.source_controls[{i}].{field}", "path": b["path"], "kind": b.get("kind"),
                                            "old": a.get(field), "new": b.get(field)})
            elif before.get(key) != new.get(key):
                changes.append({"field": f"languages.{language}.{key}", "old": before.get(key), "new": new.get(key)})
    for language, after in public.get("body_fidelity", {}).items():
        prior = fidelity_before.get(language, {})
        for key in sorted(set(prior) | set(after)):
            if prior.get(key) != after.get(key):
                value = after.get(key)
                changes.append({"field": f"public.body_fidelity.{language}.{key}", "old": prior.get(key),
                                "new": value if not isinstance(value, dict) else "added (successor annotation, text-free)"})
    old_public = row["public_sha256"]
    row["public_sha256"] = sha(public)
    if old_public != row["public_sha256"]:
        changes.append({"field": "public_sha256", "old": old_public, "new": row["public_sha256"]})


def recompute_native(ctx, row, changes):
    doc = ctx.document("roman-1962")
    masses = ctx.masses["roman-1962"]
    key = tuple(row["target"])
    ledger = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml").read_text())
    binding = next(r for r in ledger["entries"] if ctx.owner.translation_record_identity(r, doc) == key)
    english = next(r["text"] for r in binding["translations"] if r.get("source_id") == endings.SOURCE_ID and r.get("lang") == "en")
    latin = next(r["text"] for r in masses[key[0]].get("propers", []) if r.get("name") == key[2] and r.get("text"))
    proofs = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml").read_text())["entries"]
    proof = next(r for r in proofs if r["mass"] == key[0] and r["proper"] == key[2]
                 and (r["mass"], ctx.owner.form_id_for_label(masses[r["mass"]], r.get("form", "")), r["proper"],
                      r.get("cycle") or "all", r["occurrence"]) == key)
    formulas = {f["key"]: f for f in json.loads((ROOT / endings.TABLE_PATH).read_bytes())["formulas"]}
    formula = formulas[row["family"]]
    before = dict(row)
    if not english.endswith(formula["short_english"]):
        raise SystemExit(f"{key}: English no longer ends with its formula cue")
    row.update(binding_sha256=sha(binding), latin_proof_sha256=sha(proof), english_sha256=sha(english), latin_sha256=sha(latin),
               english_cue_start=len(english) - len(formula["short_english"]))
    if proof.get("text_sha256") != row["latin_sha256"]:
        raise SystemExit(f"{key}: proof row does not own the current Latin body")
    if before["latin_sha256"] != row["latin_sha256"]:
        raise SystemExit(f"{key}: Latin body changed; latin_cue_start needs review")
    row["public_sha256"] = sha(endings.public_projection(row, english, latin, binding, formula))
    for field in sorted(row):
        if before[field] != row[field]:
            changes.append({"field": field, "old": before[field], "new": row[field]})


def build():
    ctx = Context()
    v4_raw = (ROOT / V4).read_bytes()
    if hashlib.sha256(v4_raw).hexdigest() != V4_SHA256:
        raise SystemExit("authority-v4 changed")
    v5 = json.loads(v4_raw)
    seen, record_changes = set(), []
    for row in v5["records"]:
        key = ("roman-1962", *row["target"])
        if key in DECLARED:
            changes = []
            recompute_native(ctx, row, changes)
            record_changes.append({"calendar": "roman-1962", "section": "records", "target": row["target"], "justification": DECLARED[key], "changes": changes})
            seen.add(key)
    for row in v5["supplemental_records"]:
        key = (row["calendar"], *row["target"])
        if key in DECLARED:
            changes = []
            recompute_supplemental(ctx, row, changes)
            record_changes.append({"calendar": row["calendar"], "section": "supplemental_records", "target": row["target"], "justification": DECLARED[key], "changes": changes})
            seen.add(key)
    missing = set(DECLARED) - seen
    if missing:
        raise SystemExit(f"declared records absent from v4: {sorted(missing)}")
    v5["successor"] = {
        "of": {"path": V4, "sha256": V4_SHA256},
        "recorded_on": "2026-11-14",
        "scope": "v4 scope unchanged. Exactly the declared records are recomputed from the current source records; every other record and field is byte-equivalent.",
        "builder": f"{HERE}/build_authority_v5.py",
        "receipt": RECEIPT,
    }
    v5_text = dump(v5)
    v5_sha = hashlib.sha256(v5_text.encode()).hexdigest()

    # editorial display authority successor (pins the ending authority)
    ed2_raw = (ROOT / ED_V2).read_bytes()
    if hashlib.sha256(ed2_raw).hexdigest() != ED_V2_SHA256:
        raise SystemExit("editorial authority v2 changed")
    ed = json.loads(ed2_raw)
    publics = {canonical([r["calendar"], *r["target"]]) if "calendar" in r else canonical(r["target"]): r["public_sha256"]
               for r in v5["records"] + v5["supplemental_records"]}
    for rec in ed["records"]:
        if publics.get(canonical(rec["target"])) is None:
            raise SystemExit(f"editorial record {rec['target']} has no v5 owner")
    changed_targets = {canonical(c["target"]) for c in record_changes}
    if any(canonical(rec["target"]) in changed_targets for rec in ed["records"]):
        raise SystemExit("a display-corrected record changed; the editorial authority needs a new review, not a successor")
    review = {
        "schema": "triptych-finite-display-ending-successor-review/v1",
        "scope": "Exact three previously adopted display corrections; the ending-authority successor v5 changes none of their records.",
        "predecessor_ending_authority_sha256": V4_SHA256,
        "successor_ending_authority": {"path": V5, "sha256": v5_sha},
        "predecessor_editorial_authority": {"path": ED_V2, "sha256": ED_V2_SHA256},
        "unchanged_original_records": len(v5["records"]) - sum(1 for c in record_changes if c["section"] == "records"),
        "changed_ending_records": [{"calendar": c["calendar"], "target": c["target"]} for c in record_changes],
        "unchanged_display_records": ed["records"],
        "recorded_on": "2026-11-14",
        "builder": f"{HERE}/build_authority_v5.py",
    }
    review_text = dump(review)
    ed["ending_authority_sha256"] = v5_sha
    ed["ending_authority_successor_review"] = {"path": ED_REVIEW, "sha256": hashlib.sha256(review_text.encode()).hexdigest()}
    ed_text = dump(ed)
    ed_sha = hashlib.sha256(ed_text.encode()).hexdigest()

    # code pins
    py = (ROOT / PY).read_text(encoding="utf-8")
    py = re.sub(r'^AUTHORITY_PATH = ".*"$', f'AUTHORITY_PATH = "{V5}"', py, count=1, flags=re.M)
    py = re.sub(r'^AUTHORITY_SHA256 = ".*"$', f'AUTHORITY_SHA256 = "{v5_sha}"', py, count=1, flags=re.M)
    js = (ROOT / JS).read_text(encoding="utf-8")
    js = re.sub(r"const ACTIVE_AUTHORITY_SHA256 = '[0-9a-f]*';", f"const ACTIVE_AUTHORITY_SHA256 = '{v5_sha}';", js, count=1)
    section = endings.browser_pin_section(v5, v5_sha)
    js = re.sub(r"  // BEGIN GENERATED CONCLUSION PINS.*?  // END GENERATED CONCLUSION PINS", lambda _m: section, js, count=1, flags=re.S)
    js = re.sub(r"const ACTIVE_DISPLAY_AUTHORITY_SHA256 = '[0-9a-f]*';", f"const ACTIVE_DISPLAY_AUTHORITY_SHA256 = '{ed_sha}';", js, count=1)
    js = re.sub(r'const GENERATED_DISPLAY_AUTHORITY_SHA256 = "[0-9a-f]*";', f'const GENERATED_DISPLAY_AUTHORITY_SHA256 = "{ed_sha}";', js, count=1)
    js = re.sub(r'const DISPLAY_ENDING_AUTHORITY_SHA256 = "[0-9a-f]*";', f'const DISPLAY_ENDING_AUTHORITY_SHA256 = "{v5_sha}";', js, count=1)
    lists = {}
    for path in LISTS:
        text = (ROOT / path).read_text(encoding="utf-8")
        if V5 not in text:
            text = re.sub(r"^(\s*)(['\"])" + re.escape(V4) + r"\2,\n", lambda m: m.group(0) + f"{m.group(1)}{m.group(2)}{V5}{m.group(2)},\n", text, count=1, flags=re.M)
        lists[path] = text

    receipt = {
        "schema": "triptych-oration-conclusion-authority-successor-receipt/v1",
        "recorded_on": "2026-11-14",
        "authorization": "Gap-campaign coordinator, 2026-11-14: oration-conclusion authority v5 successor plus installation of the held items, after batches 3-5 and the integrate-1962 lane merged.",
        "text_free": "Hashes, identities and reasons only; no prayer wording.",
        "predecessor": {"path": V4, "sha256": V4_SHA256},
        "successor": {"path": V5, "sha256": v5_sha},
        "editorial_display_successor": {"predecessor": {"path": ED_V2, "sha256": ED_V2_SHA256}, "successor": {"path": ED_V3, "sha256": ed_sha},
                                        "review": {"path": ED_REVIEW, "sha256": ed["ending_authority_successor_review"]["sha256"]}},
        "builder": {"path": f"{HERE}/build_authority_v5.py", "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    "recompute": f"python3 {HERE}/build_authority_v5.py", "check": f"python3 {HERE}/build_authority_v5.py --check"},
        "unchanged": {"records": len(v5["records"]) - sum(1 for c in record_changes if c["section"] == "records"),
                      "supplemental_records": len(v5["supplemental_records"]) - sum(1 for c in record_changes if c["section"] == "supplemental_records"),
                      "formula_catalog": len(v5["formula_catalog"])},
        "changed_records": record_changes,
        "code_pins": {PY: ["AUTHORITY_PATH", "AUTHORITY_SHA256"],
                      JS: ["ACTIVE_AUTHORITY_SHA256", "GENERATED CONCLUSION PINS section", "ACTIVE_DISPLAY_AUTHORITY_SHA256",
                           "GENERATED_DISPLAY_AUTHORITY_SHA256", "DISPLAY_ENDING_AUTHORITY_SHA256"],
                      **{p: ["authority path list: v5 added after v4"] for p in LISTS}},
    }
    receipt_text = dump(receipt)
    adoption = {
        "schema": "triptych-oration-conclusion-successor-activation/v1",
        "date": "2026-11-14",
        "authorization": "Gap-campaign coordinator authorized this successor and the installation of the held items (2026-11-14). Built by the integrate lane with the reproducible builder named below; this record is the activation record adjacent to the authority, as v2-v4 were.",
        "independent_review": "An independent fidelity review was running when this successor was built. If it corrects a pinned record, re-run the builder; no record outside the declared set may change.",
        "authority": {"path": V5, "sha256": v5_sha, "predecessor": {"path": V4, "sha256": V4_SHA256}},
        "editorial_display_authority": {"path": ED_V3, "sha256": ed_sha},
        "receipt": {"path": RECEIPT, "sha256": hashlib.sha256(receipt_text.encode()).hexdigest()},
        "postimages": {p: hashlib.sha256(t.encode()).hexdigest() for p, t in ((PY, py), (JS, js), *lists.items())},
        "limits": [
            "No record outside the declared set changes; v4's scope, formulas and execution rules are unchanged.",
            "The 18 postconciliar records remain English-only conclusion records; the admitted Latin bodies print their own target cues and are not executed by them.",
            "Browser products, release bindings and the corpus index are refreshed separately by the coordinator.",
        ],
    }
    outputs = {V5: v5_text, f"{ED_REVIEW}": review_text, ED_V3: ed_text, PY: py, JS: js, **lists, RECEIPT: receipt_text, ADOPTION: dump(adoption)}
    return outputs, v5_sha, record_changes


def validate():
    """The repository's own loaders accept v5 for both calendars (undeclared records unchanged)."""
    import importlib
    importlib.reload(endings)
    owner = owner_module()
    root = ROOT / "src/sources/calendars"
    _, rows = endings.authority(ROOT)
    loaded = {}
    for calendar in ("roman-1962", "postconciliar"):
        loaded.update({(calendar, *k) if len(k) == 5 else k: v for k, v in endings.load_sources(root, calendar, owner).items()})
    return len(rows), len(loaded)


def main():
    check = "--check" in sys.argv[1:]
    outputs, v5_sha, changes = build()
    stale = [p for p, text in outputs.items() if not (ROOT / p).exists() or (ROOT / p).read_text(encoding="utf-8") != text]
    if check:
        if stale:
            raise SystemExit("stale: " + ", ".join(stale))
        print(f"v5 {v5_sha} current; {len(changes)} declared records; loaders accept {validate()}")
        return
    for path, text in outputs.items():
        (ROOT / path).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / path).write_text(text, encoding="utf-8")
    print(f"wrote {len(stale)} files; v5 {v5_sha}; {len(changes)} declared records; loaders accept {validate()}")


if __name__ == "__main__":
    main()
