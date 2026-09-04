"""Apply one backfill lane proposal to the repository, deterministically.

Emits, for one lane:
  * one Pustet 1862 passage per mass (the public-domain antecedent locus)
  * one 1962 target passage per mass (the reading witness)
  * one editorial-projection artifact per lane, holding every matched body
  * one projection passage per matched oration
  * one provenance ledger row per matched oration
  * the body itself in roman-1962/propers.yaml, replacing its text_status

Non-matched orations are NOT published.  Their text_status reason is retyped
from rights-withheld -- which asserts something about the 1962 edition the
repository's own rights record denies -- to witness-gap against the witness
actually consulted.
"""
import hashlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from orthography import normalise

REPO = "/home/ksh/git/worktrees/triptych/proper-54/spincyc/triptych"
PROJ_EDITION = "2026-09-03-editorial-projection"
PROJ_DIR = f"{REPO}/src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/{PROJ_EDITION}"
PUSTET_DIR = f"{REPO}/src/sources/works/catholic-church/missale-romanum/editions/pustet-ratisbon-1862"
TARGET_DIR = f"{REPO}/src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962"
PUSTET_ART = "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf"
MAME_ART = "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.ia-scan-pdf-9873693a"
MAME_SHA = "9873693a2937c6a573ed050351b30c545b7464b87b06390785e504fb0aac7005"
MAME_EDITION = "edition.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam"
MAME_DIR = f"{REPO}/src/sources/works/catholic-church/missale-romanum/editions/1922-tours-mame-editio-quarta-iuxta-typicam"


def antecedent_is_mame(rows):
    """Whether a mass's antecedent is the Mame rather than the Pustet.

    Some formularies are simply not in the 1862: Holy Family was granted in
    1893 and made universal in 1921, so the only public-domain witness that
    carries it is the 1922 Mame. Emitting a Pustet passage for one of those
    produces a passage with no line ranges, which the source library rejects
    -- correctly, since it would be citing a book that does not print the text.
    """
    joined = " ".join((r.get("antecedent_locus") or "") + " " + (r.get("notes") or "") for r in rows)
    low = joined.lower()
    return ("mame" in low or "1922" in low) and not re.search(r"lines?\s+\d+\s*[-–]\s*\d+", joined)
PUSTET_SHA = "f34bc7cf9293ffb353159e94118f4316bb4cc0a60230b315904dc77ba2502162"
TARGET_ART = "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
TARGET_SHA = "648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a"
SURFACES = '["web", "download", "print", "cli", "corpus-data", "public-git"]'


# Recognisers turn printed accents into digits and currency signs and confuse
# letter pairs, so a lane that stores what a text layer read -- rather than what
# the page says -- offers OCR damage as a publishable body.  Two lanes did.
# Nothing downstream would catch it: the string is well-formed Latin-looking
# text and hashes fine.  This refuses it at the door.
OCR_JUNK = re.compile(r"[A-Za-z]*[0-9£&§¢®©][A-Za-z]+|[A-Za-z]+[0-9£&§¢®©][A-Za-z]*")
OCR_SUSPECT = ("ii", "rn", "vv")
OCR_SAFE = {
    # real Latin words that trip the digraph heuristic
    "remedii", "mysteriis", "gaudii", "auxilii", "ministerii", "sacrificii",
    "beneficii", "iudicii", "judicii", "obsequii", "imperii", "silentii",
    "principii", "consilii", "exercitii", "martyrii", "eii", "ii",
    "alternis", "aeternis", "supernis", "paternis", "internis", "hodiernis",
}

# The damage screen is the repository's, not a copy: scripts/_latin_body_damage.py
# is what check-calendar-masses runs, so a body this applier accepts is one the
# checker accepts. The two had already drifted once -- the applier still refused
# a question mark after the committed screen had learned to allow a real one.
sys.path.insert(0, os.path.join(REPO, "scripts"))
from _latin_body_damage import body_damage as ocr_damage  # noqa: E402

def sha256(t): return hashlib.sha256(t.encode("utf-8")).hexdigest()
def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def esc(s):
    # Lanes quote their own working notes into these fields, and a note built
    # from a pdftotext extraction can carry the page separator \x0c straight
    # through. TOML refuses it, and the whole ledger then reads as zero rows --
    # which is how it surfaced: a "missing entry" for one proper, when in fact
    # nothing in the file was readable. Strip every control character except
    # the newline and tab that TOML's own escaping handles.
    s = "".join(" " if ord(c) < 32 and c not in "\n\t" else c for c in s)
    return s.replace("\\", "\\\\").replace('"', '\\"')

def wrap(text, width=76, indent=""):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(indent + cur); cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur: lines.append(indent + cur)
    return lines


def resolve_occurrences(matched):
    """Attach the calendar occurrence number to every proposal entry.

    A mass may print several propers under one name -- palm-sunday has seven
    Procession Antiphons -- and the provenance ledger keys on occurrence, so a
    positional guess is not good enough.  Entries are assigned in calendar
    order to the withheld slots of that name, then each assignment is CHECKED
    against the calendar's own incipit; a mismatch is fatal rather than
    silently landing a body against the wrong slot.
    """
    import yaml
    cal = yaml.safe_load(open(f"{REPO}/src/sources/calendars/roman-1962/propers.yaml"))
    slots = {}
    for section in cal["sections"].values():
        for m in section.get("masses") or []:
            seen = {}
            for pr in m.get("propers") or []:
                if not isinstance(pr, dict):
                    continue
                name = pr.get("name")
                seen[name] = seen.get(name, 0) + 1
                ts = pr.get("text_status")
                withheld = isinstance(ts, dict) and any(
                    r.get("kind") == "rights-withheld" for r in ts.get("reasons") or []
                )
                # A slot this backfill has already landed carries text instead of
                # a withheld status.  Counting it too keeps regeneration
                # idempotent, so the source records can be rebuilt after landing.
                gap = isinstance(ts, dict) and any(
                    r.get("kind") == "witness-gap" for r in ts.get("reasons") or []
                )
                if withheld or gap or pr.get("text"):
                    slots.setdefault((m["key"], name), []).append(
                        (seen[name], (pr.get("incipit") or "").strip())
                    )
    used = {}
    for o in matched:
        key = (o["mass"], o["proper"])
        i = used.get(key, 0)
        avail = slots.get(key) or []
        if i >= len(avail):
            raise SystemExit(f"{o['mass']}/{o['proper']}: no withheld slot left to claim")
        occ, incipit = avail[i]
        used[key] = i + 1
        if incipit:
            # Fold the differences that are real but harmless: the stored
            # incipits spell oe where the typica spells ae (coelestia against
            # caelestia), i against j, and a chant proper's body legitimately
            # opens with its own formula -- "Alleluia, alleluia. V." or "V." --
            # before the words the incipit quotes.  Containment near the head
            # still catches a body landed against the wrong slot, which is what
            # this guard exists for.
            def fold(t):
                t = t.lower().replace("oe", "e").replace("ae", "e").replace("j", "i")
                return re.sub(r"[^a-z ]", " ", re.sub(r"\s+", " ", t)).replace("  ", " ").strip()
            want, got = fold(incipit), fold(o["_body"])[:200]
            probe = " ".join(want.split()[:4])
            if probe and probe not in got:
                # In practice this fires on recogniser damage in the opening
                # words -- a truncated word, a marginal number welded in, a
                # mangled drop capital -- so quarantine the entry and carry on
                # rather than halting a lane over one bad string.
                o["_reject"] = (
                    f"body does not carry the calendar incipit {incipit!r} near its "
                    f"head; got {o['_body'][:70]!r}"
                )
        o["_occ"] = occ
    return matched

def main(lane):
    prop = json.load(open(f"{REPO}/.scratch/backfill/{lane}/proposal.json"))
    season = prop.get("season", lane)
    matched = [o for o in prop["orations"] if o["verdict"] == "matched"]
    other   = [o for o in prop["orations"] if o["verdict"] != "matched"]
    if not matched:
        print(f"{lane}: no matched orations"); return

    # ---- normalise bodies, keep per-oration record -------------------------
    unmapped_all = []
    for o in matched:
        body, un = normalise(" ".join((o["target_text_1962"] or "").split()))
        o["_body"] = body
        unmapped_all += un
    if unmapped_all:
        raise SystemExit(f"{lane}: unmapped j-candidates {sorted(set(unmapped_all))}")
    damaged = {}
    for o in matched:
        hits = ocr_damage(o["_body"])
        if hits:
            damaged[f"{o['mass']}/{o['proper']}"] = hits
    if damaged:
        lines = "\n".join(f"    {k}: {', '.join(v)}" for k, v in sorted(damaged.items()))
        raise SystemExit(
            f"{lane}: {len(damaged)} target body(ies) carry recogniser damage and "
            f"will not be landed.\n{lines}\n"
            "  These are text-layer readings, not page readings. Send the lane back "
            "to re-read them on a page image."
        )
    resolve_occurrences(matched)
    rejected = [o for o in matched if o.get("_reject")]
    if rejected:
        matched = [o for o in matched if not o.get("_reject")]
        other += rejected
        for o in rejected:
            o["verdict"] = "blocked"
        print(f"  {lane}: {len(rejected)} entry(ies) quarantined on the incipit check")

    # ---- projection artifact text -----------------------------------------
    stanzas, ranges, cursor = [], {}, 1
    for o in matched:
        lines = wrap(o["_body"])
        ranges[(o["mass"], o["proper"], o.get("_occ"))] = (cursor, cursor + len(lines) - 1)
        stanzas.append("\n".join(lines)); cursor += len(lines) + 1
    art_text = "\n\n".join(stanzas) + "\n"
    art_sha = hashlib.sha256(art_text.encode("utf-8")).hexdigest()
    art_slug = art_sha[:8]
    art_name = f"{slug(lane)}-orations-{art_slug}"
    art_id = f"artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-09-03.{art_name}"
    ad = f"{PROJ_DIR}/artifacts/{art_name}"
    os.makedirs(ad, exist_ok=True)
    open(f"{ad}/{art_name}.txt", "w", encoding="utf-8").write(art_text)

    masses = sorted({o["mass"] for o in matched})
    # A lane may mix antecedents: 87 of gap-seasonal-1's orations rest on the
    # Pustet and 3 on the Mame, because the 1862 does not carry Holy Family at
    # all. The projection must name every witness it actually stands on.
    for one_mass in masses:
        rows_for = [o for o in matched if o["mass"] == one_mass]
        pd_artifact = MAME_ART if antecedent_is_mame(rows_for) else PUSTET_ART
        for one in rows_for:
            one["_pd_art"] = pd_artifact
    used_pd = sorted({o["_pd_art"] for o in matched})
    open(f"{ad}/artifact.toml", "w", encoding="utf-8").write(f'''schema = 1
record_type = "artifact"
id = "{art_id}"
edition_id = "edition.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-09-03"
artifact_type = "editorial-projection"
media_type = "text/plain; charset=utf-8"
storage = "tracked"
rights_status = "project-created"
rights_basis = "Triptych created the bounded selection, transcription layout, normalization decisions, and collation record and offers those editorial contributions under CC BY 4.0. The underlying Latin prayers are public domain in the United States because the separately registered Pustet printing was published at Ratisbon in 1862. Triptych claims no exclusive right in those underlying words. The target-edition comparison selects only mechanical punctuation, project orthography, and the conclusion as printed, within the preexisting formulas; no page image, layout, rubric, marginal number, or other 1962-only matter is reproduced."
rights_jurisdiction = "United States"
provenance = "Created by Triptych on 2026-09-03 for the {season} lane of the seasonal-oration backfill, from the registered Pustet 1862 passages named below and the exact 1962 facsimile passages, the latter read as page images rather than through a text layer. This artifact is a project editorial projection over those witnesses, not an edition of either Missal."
retrieved = "2026-09-03"
sha256 = "{art_sha}"
byte_size = {len(art_text.encode("utf-8"))}
path = "{ad.replace(REPO + "/", "")}/{art_name}.txt"
projected_from = [
{chr(10).join(f'  "{one}",' for one in used_pd)}
  "{TARGET_ART}",
]
transformation = "Select only the proper orations of {", ".join(masses)} as the 1862 Pustet prints them; join printed line wraps; remove stress accents; expand printed ae/oe ligatures to ae/oe; normalise the target's consonantal i to the calendar's declared j orthography; omit headings, rubrics, marginal numbers, layout, and the 1862's own pre-1955 Secunda Oratio, Alia Secreta, Alia Postcommunio and Tertia ad libitum; and apply the controlling 1962 printing's punctuation and its conclusion at the length that printing sets it. No lexical petition, proper name or clause is supplied from the later witness."
indexable = true
encoding = "utf-8"
notes = "Scope is closed at the {len(matched)} orations listed in the passages of this edition bearing the {slug(lane)} prefix. The separate Pustet 1862 and 1962 passages remain the historical and target witnesses; this project-created artifact owns only the editorial projection. The 1862's ornamental drop capitals are destroyed by that scan's recogniser, so the opening word of many antecedent readings is reconstructed from the visible tail and from the 1570 or 1604 at the same place; every such reconstruction is named in its own ledger row and is never absorbed silently into a reading."
''')

    # ---- per-mass antecedent and target passages ---------------------------
    for mass in masses:
        rows = [o for o in matched if o["mass"] == mass]
        anteloci = "; ".join(f"{o['proper']} at {o['antecedent_locus']}" for o in rows)
        tgtloci  = "; ".join(f"{o['proper']} at {o['target_locus']}" for o in rows)
        use_mame = rows[0]["_pd_art"] == MAME_ART
        pid = (f"passage.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.{slug(mass)}-orations"
               if use_mame else
               f"passage.catholic-church.missale-romanum.pustet-ratisbon-1862.{slug(mass)}-orations")
        lr = []
        for o in rows:
            m = re.findall(r"lines?\s+(\d+)\s*[-–]\s*(\d+)", o["antecedent_locus"])
            if m: lr.append([int(m[-1][0]), int(m[-1][1])])
        # The schema requires sorted, non-overlapping ranges, and the prayers of
        # one 1962 formulary are NOT in that order in a pre-1955 book -- three of
        # the Vigil's four prophecy collects sit at the 1862's 4th, 8th and 12th.
        # Sort and merge; the per-proper loci in `locus` keep the correspondence.
        lr.sort()
        merged = []
        for a, b in lr:
            if merged and a <= merged[-1][1] + 1:
                merged[-1][1] = max(merged[-1][1], b)
            else:
                merged.append([a, b])
        lr = merged
        if use_mame:
            os.makedirs(f"{MAME_DIR}/passages", exist_ok=True)
            open(f"{MAME_DIR}/passages/{slug(mass)}-orations.toml", "w", encoding="utf-8").write(f'''schema = 1
record_type = "passage"
id = "{pid}"
edition_id = "{MAME_EDITION}"
artifact_id = "{MAME_ART}"
artifact_sha256 = "{MAME_SHA}"
locus = "{esc(anteloci)}"
states = ["cataloged", "acquired", "inspected", "verified"]
context = "The proper orations of {mass} as the 1922 Tours Mame prints them, cited as the public-domain antecedent showing that the 1962 typical edition's wording at this formulary is preexisting material under 17 U.S.C. 103(b). The 1862 Pustet does not carry this formulary at all, so the Mame is the antecedent here rather than a corroborating second witness."
verified_on = "2026-09-03"
notes = "Read on page images rendered from the exact identified Internet Archive scan of the 1922 Mame, whose artifact record states a public-domain rights status on a book first published at Tours in 1922. That artifact is registered as remote and the repository holds no payload; it was fetched once against its registered hash for this collation. Internet Archive viewer leaf n maps to artifact page n+1 at every checked locus."
''')
        else:
            open(f"{PUSTET_DIR}/passages/{slug(mass)}-orations.toml", "w", encoding="utf-8").write(f'''schema = 2
record_type = "passage"
id = "{pid}"
edition_id = "edition.catholic-church.missale-romanum.pustet-ratisbon-1862"
artifact_id = "{PUSTET_ART}"
artifact_sha256 = "{PUSTET_SHA}"
locus = "{esc(anteloci)}"
physical_line_ranges = {json.dumps(lr)}
states = ["cataloged", "acquired", "inspected"]
context = "The proper orations of {mass} as the 1862 Pustet prints them, cited as the public-domain antecedent showing that the 1962 typical edition's wording at this formulary is preexisting material under 17 U.S.C. 103(b)."
notes = "Loci are over this artifact's retained text layer; no page image of the 1862 was read, its per-leaf image artifacts being remote and not covering this run. That layer destroys ornamental drop capitals and loses occasional syllables at column breaks; where a word of this formulary is affected the ledger row for that oration names it and cites the 1570 or 1604 at the same place. This record makes the wording addressable by identity over these exact bytes, which the artifact's own record requires before it may be cited as anything but a finding aid. The 1862 is a pre-1955 recension and prints its own second and third orations beside these; those are not part of this passage."
''')
        tid = f"passage.catholic-church.missale-romanum.vatican-typica-1962.temporal-{slug(mass)}-orations"
        open(f"{TARGET_DIR}/passages/temporal-{slug(mass)}-orations.toml", "w", encoding="utf-8").write(f'''schema = 1
record_type = "passage"
id = "{tid}"
edition_id = "edition.catholic-church.missale-romanum.vatican-typica-1962"
artifact_id = "{TARGET_ART}"
artifact_sha256 = "{TARGET_SHA}"
locus = "{esc(tgtloci)}"
states = ["cataloged", "acquired", "inspected", "verified"]
context = "The proper orations of {mass} in the controlling 1962 typical edition. This is the target transcription witness for their wording, pointing and conclusion length; it is not the rights authority for publishing them."
verified_on = "2026-09-03"
notes = "Read on page images rendered from the exact identified CMAA facsimile, not through its embedded text layer, which drops ornamental initials and misreads marginal numbers. An independent machine reading of the Benziger 1962 conformed printing was taken alongside; where the two parted the page image settled it, and the page image agreed with the facsimile's own layer in every recorded case. Publication rights come from a separately registered public-domain witness and from 17 U.S.C. 103(b); see src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml."
''')

    # ---- projection passages + ledger rows --------------------------------
    ledger_rows = []
    for o in matched:
        lo, hi = ranges[(o["mass"], o["proper"], o.get("_occ"))]
        pslug = f"{slug(o['mass'])}-{slug(o['proper'])}"
        if o["_occ"] > 1: pslug += f"-{o['_occ']}"
        ppid = f"passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-09-03.{pslug}"
        body_sha = sha256(o["_body"] + "\n")
        o["_body_sha"] = body_sha
        open(f"{PROJ_DIR}/passages/{pslug}.toml", "w", encoding="utf-8").write(f'''schema = 1
record_type = "passage"
id = "{ppid}"
edition_id = "edition.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-09-03"
artifact_id = "{art_id}"
artifact_sha256 = "{art_sha}"
locus = "{esc(o['mass'])}, {esc(o['proper'])}; editorial-projection artifact physical lines {lo}-{hi}; antecedent {esc(o['antecedent_locus'])}; target {esc(o['target_locus'])}"
physical_line_ranges = [[{lo}, {hi}]]
states = ["cataloged", "acquired", "inspected", "verified"]
context = "Exact project-created editorial-projection passage for the Roman-1962 {esc(o['mass'])} {esc(o['proper'])}."
verified_on = "2026-09-03"
notes = "The selected lines hash as the retained calendar body {body_sha}. The artifact manifest owns every 1862-to-target transformation; the separate historical and target passages remain the witnesses."
''')
        diffs = "; ".join(o.get("differences") or []) or "none recorded"
        corr = o.get("corroboration") or "none attempted"
        conf = o.get("confidence", "high")
        note = (o.get("notes") or "").strip()
        ev = (f"The project-owned projection passage reproduces the retained calendar body hash exactly. Its artifact manifest records the bounded public-domain 1862 Pustet antecedent, the separate 1962 target, and every editorial transformation; neither witness is represented as owning the projected bytes. The 1962 reading was established on that edition's page images rather than its text layer, cross-read against the Benziger conformed printing. Differences from the antecedent: {diffs}. Corroboration: {corr}.")
        if conf != "high" and note:
            ev += f" Recorded limitation: {note}"
        ledger_rows.append(f'''[[entries]]
mass = "{o['mass']}"
form = ""
proper = "{o['proper']}"
course = ""
cycle = ""
occurrence = {o["_occ"]}
text_sha256 = "{body_sha}"
provenance_status = "collated"
source_id = "{ppid}"
source_date = "2026-09-03 project editorial projection; antecedent Pustet Ratisbon 1862"
locator = "editorial-projection artifact physical lines {lo}-{hi}; antecedent {esc(o['antecedent_locus'])}"
relationship = "editorial-projection-exact-to-target"
verification_source_id = "passage.catholic-church.missale-romanum.vatican-typica-1962.temporal-{slug(o['mass'])}-orations"
verification_locator = "{esc(o['target_locus'])}"
transformations = ["join printed line wraps", "remove stress accents", "expand printed ae/oe ligatures to ae/oe", "normalise consonantal i to the calendar's j orthography", "apply the target printing's punctuation", "carry the target's conclusion at its printed length"]
provenance_evidence = "{esc(ev)}"
provenance_authority = "Triptych editorial projection verified by page-image collation against the 1962 target edition"
provenance_confidence = "{conf}"
publication_status = "permitted"
publication_basis = "public-domain"
surfaces = {SURFACES}
publication_source_ids = ["{art_id}", "{o.get("_pd_art", PUSTET_ART)}"]
publication_locator = "{'Tours Mame 1922' if o.get('_pd_art') == MAME_ART else 'Pustet Ratisbon 1862'}, {esc(o['antecedent_locus'])}; artifact rights_status public-domain"
publication_evidence = "The wording is preexisting material of the 1962 typical edition under 17 U.S.C. 103(b), which gives a revised edition no exclusive right in material it did not contribute. The independent registered public-domain witness is the tracked 1862 Pustet text artifact. The position is settled for the repository at src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml, which names the seasonal orations as preexisting material and requires exactly this pairing of 103(b) with a public-domain witness."

''')
    out = {"lane": lane, "artifact_id": art_id, "matched": len(matched),
           "other": [{"mass": o["mass"], "proper": o["proper"], "verdict": o["verdict"]} for o in other],
           "ledger_rows": ledger_rows,
           "bodies": [{"mass": o["mass"], "proper": o["proper"], "occurrence": o["_occ"], "body": o["_body"],
                       "sha": o["_body_sha"], "target_locus": o["target_locus"],
                       "antecedent_locus": o["antecedent_locus"], "confidence": o.get("confidence","high")}
                      for o in matched]}
    json.dump(out, open(f"{REPO}/.scratch/backfill/{lane}/applied.json", "w"), indent=1)
    print(f"{lane}: {len(matched)} matched -> records written; {len(other)} not published")

if __name__ == "__main__":
    main(sys.argv[1])
