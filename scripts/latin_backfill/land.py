"""Land applied lane results into propers.yaml and the provenance ledger.

matched      -> body published; text_status replaced by notes + text
absent       -> reason retyped rights-withheld => witness-gap against the
                witness actually consulted.  The 1862 predates the feast; that
                is a gap in our witnesses, not a claim about the 1962 edition.
variant,
new-matter   -> left as rights-withheld, which is now the CORRECT disposition:
                the target's wording really is matter the 1962 (or 1955)
                contributed and no pre-1931 witness carries it.
"""
import json, re, sys, glob, os
REPO = "/home/ksh/git/worktrees/triptych/proper-54/spincyc/triptych"
CAL = f"{REPO}/src/sources/calendars/roman-1962/propers.yaml"
LEDGER = f"{REPO}/src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml"
PUSTET_ART = "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf"

# Width must match apply_lane.wrap exactly: the projection artifact and the
# calendar body are the same bytes, and a different wrap makes them hash apart.
def wrap(text, width=76, indent=" " * 10):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(indent + cur); cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur: lines.append(indent + cur)
    return "\n".join(lines)


def proper_slots(block_lines, proper):
    """Index every `- name: <proper>` slot in a mass block, in file order.

    Returns [(start, text_status_start, text_status_end)].  Works for
    source: composed and for source: mixed, whose verses list sits between the
    source line and the text_status block, which a flat regex cannot span.
    """
    out = []
    heads = [i for i, l in enumerate(block_lines)
             if l.startswith("      - name: ") and l[len("      - name: "):].strip() == proper]
    for h in heads:
        end = len(block_lines)
        for j in range(h + 1, len(block_lines)):
            if block_lines[j].startswith("      - name: "):
                end = j; break
        # A slot is replaceable either as an unavailable text_status block or,
        # for a body this backfill has already landed, as its notes+text block.
        # A repair lane rewrites the second kind: the string was damaged, the
        # collation behind it was not.
        ts = None
        for j in range(h + 1, end):
            if block_lines[j] == "        text_status:":
                ts = j; break
        if ts is None:
            for j in range(h + 1, end):
                if block_lines[j].startswith("        notes:") or block_lines[j] == "        text: |":
                    ts = j; break
        if ts is None:
            out.append((h, None, None)); continue
        te = end
        for j in range(ts + 1, end):
            line = block_lines[j]
            if not line.strip():
                continue
            if line.startswith("          "):
                continue
            if line.startswith("        ") and line.strip().split(":")[0] in {
                "notes", "text", "text_status"
            }:
                continue
            te = j; break
        out.append((h, ts, te))
    return out

def mass_span(lines, key):
    s = next(i for i, l in enumerate(lines) if l.strip() == f"- key: {key}")
    for i in range(s + 1, len(lines)):
        st = lines[i].lstrip()
        if st.startswith("- key: ") and (len(lines[i]) - len(st)) <= (len(lines[s]) - len(lines[s].lstrip())):
            return s, i
    return s, len(lines)

TS = (r"        text_status:\n          state: unavailable\n          scope: proper-body\n"
      r"          reasons:\n          - kind: rights-withheld\n"
      r"            source_id: edition\.catholic-church\.missale-romanum\.vatican-typica-1962\n")

def land(lanes):
    lines = open(CAL, encoding="utf-8").read().split("\n")
    ledger = open(LEDGER, encoding="utf-8").read()
    n_body = n_gap = 0
    all_rows = []
    for lane in lanes:
        ap = json.load(open(f"{REPO}/.scratch/backfill/{lane}/applied.json"))
        all_rows += ap["ledger_rows"]
        by_mass = {}
        for b in ap["bodies"]:
            by_mass.setdefault(b["mass"], []).append(b)
        for mass, rows in by_mass.items():
            s, e = mass_span(lines, mass)
            block = "\n".join(lines[s:e]) + "\n"
            blines = block.rstrip("\n").split("\n")
            # Land in reverse file order so earlier indices stay valid.
            plan = []
            for b in rows:
                slots = proper_slots(blines, b["proper"])
                withheld = [t for t in slots if t[1] is not None]
                idx = b.get("occurrence_index")
                cand = [t for t in withheld]
                if not cand:
                    raise SystemExit(f"{mass}/{b['proper']}: no text_status slot in propers.yaml")
                plan.append((cand, b))
            claimed = {}
            for cand, b in plan:
                k = b["proper"]
                i = claimed.get(k, 0)
                if i >= len(cand):
                    raise SystemExit(f"{mass}/{b['proper']}: slots exhausted")
                claimed[k] = i + 1
                b["_slot"] = cand[i]
            for cand, b in sorted(plan, key=lambda x: -x[1]["_slot"][1]):
                h, ts, te = b["_slot"]
                notes = (f"Printed locus {b['target_locus']}. Preexisting material under 17 U.S.C. "
                         f"103(b), corroborated in the tracked public-domain Pustet Ratisbon 1862 at "
                         f"{b['antecedent_locus']}.")
                # A folded block scalar, because these notes quote the Missal's
                # own rubrics and therefore contain ": " and apostrophes, which
                # a plain YAML scalar cannot carry.
                repl = (["        notes: >-"] + wrap(notes).split("\n")
                        + ["        text: |"] + wrap(b["body"]).split("\n"))
                blines[ts:te] = repl
                n_body += 1
            block = "\n".join(blines) + "\n"
            lines[s:e] = block.rstrip("\n").split("\n")
        # absent -> witness-gap, but ONLY where the ledger row is a bare removed
        # stub. A row carrying a collated finding is destroyed by the retype --
        # a witness-gap proper owns no removed body, so its row goes with it --
        # and that finding is often the more valuable record. St Albert's
        # Collect is the case: `collated-exact` against the 1962 facsimile with
        # a Lasance 1945 passage as evidence, withheld only for want of a
        # public-domain basis. A lane's `absent` verdict is about public-domain
        # witnesses; it is not a reason to discard a target collation, and for a
        # saint canonised in 1931 rights-withheld remains the honest type.
        rich = set()
        for m in re.finditer(r'\[\[entries\]\]\n(.*?)(?=\n\[\[entries\]\]|\Z)', ledger, re.S):
            blk = m.group(1)
            if 'provenance_status = "collated"' in blk or "publication_evidence" in blk:
                g = lambda f: (re.search(rf'^{f} = "([^"]*)"', blk, re.M) or [None, ""])[1]
                rich.add((g("mass"), g("proper")))
        for o in ap["other"]:
            if o["verdict"] != "absent":
                continue
            if (o["mass"], o["proper"]) in rich:
                print(f"  keeping {o['mass']}/{o['proper']} rights-withheld: its ledger row carries a collated finding")
                continue
            s, e = mass_span(lines, o["mass"])
            block = "\n".join(lines[s:e]) + "\n"
            blines = block.rstrip("\n").split("\n")
            done = False
            for h, ts, te in proper_slots(blines, o["proper"]):
                if ts is None or done:
                    continue
                seg = blines[ts:te]
                if any("kind: rights-withheld" in x for x in seg):
                    blines[ts:te] = [
                        x.replace("- kind: rights-withheld", "- kind: witness-gap")
                         .replace("source_id: edition.catholic-church.missale-romanum.vatican-typica-1962",
                                  f"source_id: {PUSTET_ART}")
                        for x in seg
                    ]
                    n_gap += 1; done = True
            if done:
                lines[s:e] = ("\n".join(blines)).split("\n")

    open(CAL, "w", encoding="utf-8").write("\n".join(lines))

    # ledger: replace the removed stub for each landed body
    n_led = 0
    for row in all_rows:
        mass = re.search(r'^mass = "([^"]+)"', row, re.M).group(1)
        proper = re.search(r'^proper = "([^"]+)"', row, re.M).group(1)
        occ = re.search(r'^occurrence = (\d+)', row, re.M).group(1)
        pat = re.compile(r'\[\[entries\]\]\nmass = "' + re.escape(mass) + r'"\nform = ""\nproper = "'
                         + re.escape(proper) + r'"\ncourse = ""\ncycle = ""\noccurrence = ' + occ
                         # The final entry of the file has no trailing blank line.
                         + r'\ntext_sha256 = "[0-9a-f]{64}"\nbody_status = "removed"\n(?:\n|\Z)')
        ledger, k = pat.subn(lambda m: row if m.group(0).endswith('\n\n') else row.rstrip('\n') + '\n', ledger, count=1)
        if k == 0:
            # A row that was typed witness-gap owns no removed body, so the
            # ledger holds no stub for it. Publishing one is an insert, not a
            # replacement.
            if not ledger.endswith("\n\n"):
                ledger = ledger.rstrip("\n") + "\n\n"
            ledger += row
        elif k != 1:
            raise SystemExit(f"ledger: {mass}/{proper} occ{occ} matched {k} stubs")
        n_led += 1
    open(LEDGER, "w", encoding="utf-8").write(ledger)
    print(f"landed {n_body} bodies, {n_led} ledger rows, {n_gap} reasons retyped to witness-gap")

if __name__ == "__main__":
    land(sys.argv[1:])
