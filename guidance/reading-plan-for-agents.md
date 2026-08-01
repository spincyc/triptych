# Reading plan and commentary harvest: agent guidance

Operating rules for `src/sources/reading-plans/` and `src/sources/commentary/`.
Terse by design. For the subject matter itself, read
[`docs/reading-and-commentary.md`](../docs/reading-and-commentary.md).

Authority order: `guidance/sources.md` owns the source contract;
`guidance/web-data.md` owns the fragment/structure/rights layering;
`src/sources/commentary/README.md` owns the discovery-index schema and the
harvest contract; this file owns nothing — it points at the owners and states
what breaks.

All figures below were recomputed on 2026-08-01 against
`narrative-spine.yaml` `sha256:60d16a28…` and `harvest-ledger.yaml`
`sha256:84bb33ec…`. Every figure names the command that produces it. Recompute
before quoting; do not trust a number in prose over a number you measured.

---

## Part one — the reading plan

### Ownership

| Concern | Owner | Never |
| --- | --- | --- |
| Plan content: readings, tiers, periods, prose | `src/sources/reading-plans/narrative-spine.yaml` | anywhere else |
| Reference validity, tier partition, order continuity | `tools/reading-plan check` | hand-checking |
| Numbering conversion, browser JSON | `tools/reading-plan structure` | in the browser |
| Verse-level truth | the tracked Douay-Rheims artifacts | a chapter-length table |
| Regression gate | `tests/tools/reading-plan.test` | ad-hoc scripts |

Invoke through `tools/tpt`, never the implementation path directly.

### Data model

`triptych-reading-plan/v1`. Required top-level keys, enforced by `check`:
`schema`, `title`, `canon`, `numbering`, `tiers`, `omissions`, `precedents`,
`periods`.

```
periods[]      key (stable, opaque), label (display only), summary, readings[]
readings[]     order (global 1..N), tier, title, book, ranges[], note?
ranges[]       {begin: {chapter, verse}, end: {chapter, verse}}   end defaults to begin
tiers          {landmarks|story|full-account: {readings: <cumulative int>, label, description}}
```

- `numbering: vulgate`. `canon: catholic-73`.
- `book` is the `modern_name` column of the Douay book index (`1 Samuel`, not
  `1 Kings`).
- `order` is global and continuous across all periods, not per period.

### Invariants

1. **Tiers are cumulative.** A reading records the tier at which it *first*
   appears. Reading tier T means taking T and every tier above it. Therefore
   `tiers[T].readings` is a running total, not a count of readings bearing that
   tier.
2. **Every declared tier is entered by at least one reading**, and every tier a
   reading claims is declared. Both directions are checked; a tier nobody enters
   would silently offer an empty pass.
3. **`order` runs `1..N` with no gaps or repeats.**
4. **No verse is covered by two readings.** Not enforced by `check`. Currently
   holds: 0 doubly-covered verse cells.
5. **Every endpoint exists in the printed verse text** of the tracked Challoner
   edition — a real verse, not merely a plausible chapter. Enforced.
6. **All eight Easter Vigil ranges are present at the Missal's exact extents.**
   Not enforced. Currently holds.
7. **Period `key` is stable and opaque; `label` is display only.** Labels have
   already been rewritten once for rights reasons without moving a reading. Do
   not encode meaning into a key, and do not renumber a key when a label changes.

### Measured state

```sh
tools/tpt reading-plan check --format json
```
→ `narrative-spine: 357 readings`, status ok.

| Quantity | Value |
| --- | --- |
| Readings / periods / books / chapters touched | 357 / 12 / 31 / 454 |
| Entering each tier (landmarks, story, full-account) | 36, 75, 246 |
| Cumulative tier totals | 36, 111, 357 |
| Verses per tier | 1,210 / 3,675 / 13,867 |
| Share of canon per tier | 3.38% / 10.26% / 38.73% |
| Canon denominator | 35,804 verses, 73 books, 1,334 chapters |
| Readings carrying a note | 106 of 357 |
| Psalm readings (all carry a Hebrew-equivalent note) | 16 |

Recompute tiers and coverage:

```sh
python3 - <<'PY'
import yaml, csv, collections
from pathlib import Path
A = Path("src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts")
tsv = lambda p: list(csv.DictReader(p.open(encoding="utf-8", newline=""), delimiter="\t"))
tok = {r["modern_name"]: r["token"] for r in tsv(next(A.glob("book-index-*/book-index.tsv")))}
verses = collections.defaultdict(set)
for p in sorted(A.glob("verse-text-*/*.tsv")):
    for r in tsv(p): verses[r["book"]].add((int(r["chapter"]), int(r["verse"])))
total = sum(len(v) for v in verses.values())
doc = yaml.safe_load(Path("src/sources/reading-plans/narrative-spine.yaml").read_text())
readings = [r for p in doc["periods"] for r in p["readings"]]
def cells(r):
    t = tok[r["book"]]; out = set()
    for s in r["ranges"]:
        b = s["begin"]; e = s.get("end") or b
        for (c, v) in verses[t]:
            if c < b["chapter"] or c > e["chapter"]: continue
            if c == b["chapter"] and b.get("verse") and v < b["verse"]: continue
            if c == e["chapter"] and e.get("verse") and v > e["verse"]: continue
            out.add((t, c, v))
    return out
print("canon verses", total)
seen, dup = set(), 0
for i, name in enumerate(("landmarks", "story", "full-account")):
    want = set(("landmarks", "story", "full-account")[:i+1])
    sel = set().union(*(cells(r) for r in readings if r["tier"] in want))
    n = sum(1 for r in readings if r["tier"] in want)
    ch = {(t, c) for (t, c, _) in sel}
    print(f"{name}: readings={n} verses={len(sel)} pct={100*len(sel)/total:.2f} chapters={len(ch)} books={len({t for t,_ in ch})}")
for r in readings:
    for c in cells(r):
        dup += c in seen; seen.add(c)
print("doubly covered verse cells:", dup)
PY
```

### Omission figures

Counted on the 73-book canon (35,804 verses). All are verse counts from the
tracked Douay text, not estimates.

| Class | Verses | Share |
| --- | --- | --- |
| Prophets (incl. Lamentations, Baruch, Daniel) | 5,875 | 16.41% |
| Wisdom and poetical | 6,881 | 19.22% |
| Epistles (21, incl. Hebrews) | 2,763 | 7.72% |
| Those three together | 15,519 | 43.34% |
| Genealogies and registers dropped | 309 | 0.86% |
| Leviticus + Ex 25–31, 35–40 + Num 1–9, 26–30 + Deut 12–26 | 2,217 | 6.19% |
| Genealogies + law blocks together | 2,526 | 7.06% |

**Never quote a 66-book percentage against a 73-book denominator or the
reverse.** The canon in force is declared in the file (`canon: catholic-73`).
State which denominator any figure uses.

**Known discrepancy in the tracked prose.** `narrative-spine.yaml` states 297
verses (0.8%) for genealogies and registers. The list it gives immediately below
that figure sums to **309** (0.86%): 297 is that list minus Genesis 22:20–24 (5)
and Genesis 25:12–18 (7), both of which the plan does in fact drop. Prefer 309.
Do not silently patch the file for this without authority; it is a one-word prose
fix, not a data defect.

**Not reproducible from this repository:** the 334-chapter "consensus narrative
spine" and its 30.7% share. That is a measurement over four external published
schemes. Do not present it as checkable, and do not attempt to reconstruct it by
obtaining those schemes' lists.

### Rights rules

- The four modern schemes (Ascension Great Adventure, Zondervan *The Story*,
  Tyndale, BibleProject) are **protected compilations**. You may record measured
  facts about their overlap. You may not copy any chapter list, sequence,
  division into readings, title, note, or set of period labels.
- Ascension's twelve period names were used verbatim in an early draft and have
  been removed. **Do not reintroduce them.** The forbidden set is Early World,
  Desert Wanderings, Royal Kingdom, Divided Kingdom, Return, Messianic
  Fulfilment, The Church, taken together as a scheme. The replacements are the
  ordinary scholarly terms now in `label`.
- Knecht, *A Practical Commentary on Holy Scripture* (1910) and Schuster, *Bible
  History* (19th-c. English editions) are public domain and may be drawn on
  directly.
- The reading plan itself carries **references only**. Do not embed verse text.
  Rights live one layer down, in the verse-text artifacts — see
  `guidance/web-data.md`.

### Failure modes

| Symptom | Cause | Detection |
| --- | --- | --- |
| A tier silently offers an empty pass | tier declared with no reading entering at it | `reading-plan check` (enforced both directions) |
| `tiers[T].readings` disagrees with reality | someone treated the cumulative total as a per-tier count | `tests/tools/reading-plan.test` |
| A reading addresses nothing | endpoint verse not printed in the Challoner edition | `reading-plan check` |
| A psalm resolves to real, wrong verses | Vulgate reference read as Hebrew | `structure` resolves both systems ahead of the browser; a failure carries `unresolved` and *no* loci |
| A psalm reading split at a false seam | the psalter concordance's inscription boundary | asserted in `tests/tools/reading-plan.test` |
| Stale browser JSON | `src/web/data/structure/readings/narrative-spine.json` not regenerated after a plan edit | none — regenerate after every edit |

`structure` refuses to write anything if `check` would fail, and creates no
output directory on refusal. Rely on that; do not pre-clean.

### Verification

```sh
tools/tpt reading-plan check                                  # exit 0
tools/tpt reading-plan structure --out src/web/data           # regenerate browser JSON
sh tests/tools/reading-plan.test                              # prints "ok"
```

`reading-plan` is **not** in `make check`. Run `sh tests/tools/reading-plan.test`
explicitly after any edit to the plan or the tool.

---

## Part two — the commentary harvest

### Ownership

| Concern | Owner | Never |
| --- | --- | --- |
| What a model said, with identity and date | `src/sources/commentary/harvest-ledger.yaml` | inferred |
| Worklist of loci short of target runs | `harvest plan --corpus … --by-chapter` | guessed |
| Asking the model | `harvest ask --corpus … --runs 3` | any other tool or verb |
| Which model a run is stamped with | the answer, via `harvest ask` | asserted about it |
| Ingesting one run | `harvest record --results --model --audited-on` | hand-editing the ledger |
| Confidence | `harvest promote` — appearances ÷ runs | a score from the model |
| The passage→works lookup | `passage-commentary-index.yaml` | written by hand |
| Entry to the source library | human review under `guidance/sources.md` | a harvest alone |

**`harvest ask` is the only verb in this repository that calls a model, and
`knox-bible` the only tool that opens a socket.** Everything else is
deterministic, and the nondeterminism stays confined to the tracked ledger,
tagged with `model` and `audited_on`. Do not add a model call anywhere else:
`tpt --list` groups both under `acquisition` precisely so a reader can answer
"does this spend anything outside my machine" by where a tool appears, and
`tools/tests/test_tool_registry.py` fails on any tool whose body and declaration
disagree.

Until 2026-07-31 the tool called nothing and the harvest ran by hand outside it.
That was not the safer arrangement it looked like: `record --model X
--audited-on Y` stamped a run with whatever an operator typed, so the ledger's
provenance was an assertion rather than an observation — the failure this
repository treats as worst, a reference that resolves successfully and wrongly.
`ask` takes both stamps from the response: the date from the clock, and the
model from the `model` each assistant message declares. Not from the run's
`modelUsage` tally, which names a helper model beside the answering one and
cannot say which wrote the answer. `--model opus` is a request, and an alias;
what reaches the ledger is what answered.

### Data model

`triptych-commentary-harvest/v1`.

```
runs[]         run_id = "{audited_on}-{model}-{sha256(cleaned)[:8]}"
               model, audited_on, passage_count, passages{}
passages{}     "<Book> <chapter>" -> [work, …]     (empty list is meaningful)
work           author, title, role, death_year, aliases[]?, work_id?
```

- `role` ∈ `church-father | saint | saintly | pope | doctor |
  ecclesiastical-writer`. Enforced at
  `record`.
- `death_year` must be an integer ≤ **1900**. Enforced at `record` — the cutoff
  is a field so it is checkable afterwards, never only a prompt.
- Runs are stored sorted by `run_id`; re-recording an identical run is a no-op.
  A run is keyed by what it said, so two runs that answered identically are one
  run here — right, but it means N runs asked is not N runs recorded. `ask`
  reports the difference as `identical_runs`; confidence is appearances ÷ runs,
  so an unnoticed collapse is a wrong number rather than a missing one.
- **A locus is one chapter, never wider.** `--by-chapter` enforces it.
  `Isaiah 63:16-64:7` becomes `Isaiah 63` and `Isaiah 64`. Wider grouping drops
  works commenting on only one chapter and the loss is invisible.

### Current ledger state

```sh
tools/tpt harvest plan --corpus src/sources/commentary/mass-commentary-corpus.yaml \
  --by-chapter --json          # → total 525, pending 0, cutoff_year 1900
tools/tpt harvest promote --audited-on <date> --dry-run --json
```

The 525 loci are the ones both missals' propers cite. The corpus is wider —
1,600 passages, of which 1,591 are chapter-matched. Read the
scale before starting: `ask --dry-run` reports the query count, and it is one
query per passage per run.

```sh
tools/tpt harvest ask --corpus src/sources/commentary/mass-commentary-corpus.yaml \
  --by-chapter --runs 3 --dry-run     # what it would ask, of how many; spends nothing
tools/tpt harvest ask --corpus src/sources/commentary/mass-commentary-corpus.yaml \
  --by-chapter --runs 3 --limit 20    # then record each results file it names
```

These figures were measured after the first six runs and are kept because the
corroboration analysis below rests on them. **The ledger now holds 13 runs**;
re-derive rather than quoting the table.

| Quantity, as at 6 runs | Value |
| --- | --- |
| Runs in ledger | 6 |
| Pilot runs (2026-07-30, 7 verse-range loci) | 3 |
| Full passes (2026-07-31, 491 chapter loci) | 3 |
| Model on all six | `claude-opus-5` |
| Attributions, three full passes | 15,803 (5,927 + 4,963 + 4,913) |
| Attributions, all six runs | 16,058 |
| Corpus references collapsing to those 491 loci | 1,296 across 128 masses |
| Distinct (locus, author) | 6,511 |
| Distinct (locus, author, title) | 10,293 |

The corpus itself has since grown to **196 masses, all covered**.

### The corroboration measurement

| Matched on | ≥2 of 3 passes | All 3 |
| --- | --- | --- |
| Author | 5,095 / 6,511 = **78.3%** | 61.8% |
| Author **and** title | 3,635 / 10,293 = **35.3%** | 18.2% |

Gap **42.9 points**. Pairwise two-pass gaps: 41.0, 41.0, 44.3 — the gap is
systematic, not sampling noise, and adding passes does not close it.

Interpretation to carry forward: **the research is sound; the identity matching
is the weak link.** 54.9% of corroborated (locus, author) pairs carry more than
one title spelling. 79 distinct authors produced 718 distinct title spellings.
Nicholas of Lyra: 1,470 attributions, 1 title. Denis the Carthusian: 1,470
attributions, 92 titles (per-book *enarrationes* named as whole or as part —
genuine bibliographic ambiguity, not error).

Recompute:

```sh
python3 - <<'PY'
import yaml, collections
from pathlib import Path
led = yaml.safe_load(Path("src/sources/commentary/harvest-ledger.yaml").read_text())
full = [r for r in led["runs"] if r["passage_count"] == 491]
n = lambda s: str(s or "").casefold().strip()
def rate(keyf):
    hits = collections.Counter()
    for r in full:
        for k in {(p,) + keyf(w) for p, ws in r["passages"].items() for w in ws}: hits[k] += 1
    ge2 = sum(1 for v in hits.values() if v >= 2)
    return ge2, len(hits), 100 * ge2 / len(hits)
print("passes", len(full), "attributions",
      sum(len(w) for r in full for w in r["passages"].values()))
a = rate(lambda w: (n(w["author"]),));            print("author      %d/%d = %.1f%%" % a)
b = rate(lambda w: (n(w["author"]), n(w["title"])));print("author+title %d/%d = %.1f%%" % b)
print("gap %.1f points" % (a[2] - b[2]))
print("empty in all three:", [p for p in full[0]["passages"]
                              if all(not r["passages"][p] for r in full)])
PY
```

Match keys **casefolded and stripped**, as `tools/harvest` does. Exact-string
matching gives 32.4% on author+title (a 45.8-point gap) and is the wrong figure.

### Extent gating — verified convergence

The three passes independently respected these real extents. Treat any future
pass that violates one as suspect.

| Work | Extent | Ledger behaviour |
| --- | --- | --- |
| Aquinas, *Postilla super Psalmos* | to Psalm 54 | on all 45 harvested psalm loci ≤ 54, none of the 78 above |
| Jerome on Jeremias | breaks off ~ch. 32 | on Jer 1, 17, 20, 23, 29, 31; never 33 or 38 |
| Origen on Matthew | survives from 13:36 | on Mt 13–28 only; never on the eleven loci at 1–11 |
| Gregory, *Homiliae in Hiezechihelem* | chs. 1–4 and 40 only | of eight Ezechiel loci, chapter 2 alone |
| Cornelius a Lapide | nothing on Job or the Psalms | 0 of 89 Job attributions, 0 of 4,399 Psalms attributions; present across 58 other books |

**Agreement on a negative:** `4 Esdras 2` is the only locus empty in all three
passes. It is harvested because both missals cite 4 Esdras 2:36–37 (Introit /
Entrance Antiphon, Tuesday within the Octave of Pentecost). 4 Esdras is not
among the Douay index's 73 books. An empty list here is correct; do not "fix" it.

### Promotion happened

**This section said promotion was blocked and the index was a stub
(`passages: []`). Both have since been overtaken.** The index now holds **562
passages carrying 9,083 work entries** — 579 distinct author-and-title pairs,
184 authors, 61 books — promoted from 13 runs [verified 2026-08-01]. The
reasoning below is kept because it is why the alias table exists, and because
the splitting it describes is still what the confidence figures mean.

Promotion from 6 runs would have written 9,034 works across 497 passages.
Because only 35.3% of (author, title) pairs corroborate, a large share of those
entries are one work split across two titles, each fragment scoring 0.33 or 0.67
instead of the 1.0 the work earned. Splitting also demotes both halves below
genuinely weaker works, which corrupts the ranking the acquisition list exists
to produce. Visible in `harvest propers --top 15`: **Denis the Carthusian holds
four of the top fifteen slots** under four titles.

Open tasks, in order:

1. ~~Populate a **work-identity registry**~~ — **the alias half is done.**
   `src/sources/commentary/work-aliases.yaml` is tracked and derived by
   `tools/tpt harvest aliases --rebuild`, with `genesis-work-aliases.yaml`
   beside it. What remains is the reconciliation to the `work.*` identities
   `tools/source-library` uses: **`work_id` is still null on all 9,083 entries**
   [verified], so deduplication still falls back to the string
   `"author | title"`. That is the open item, not the alias data.
2. Decide the **whole-versus-part titling rule** for per-book commentaries and
   apply it as aliases.
3. Reconcile the **two locus granularities**: three pilot runs use verse-range
   keys (`Psalms 24:1-24:3`), the three full passes use chapter keys
   (`Psalms 24`). They do not collide, which is why promotion reports 497
   passages for 491 harvested loci.
4. Then promote with a confidence floor and review into the vault under
   `guidance/sources.md`.

### Failure modes

| Symptom | Cause | Note |
| --- | --- | --- |
| **A recorded run vanishes** | `record` and `promote` do load → mutate → whole-file `_dump`. Two processes writing the ledger concurrently: the loser's write reverts the winner's runs. Observed 2026-07-31: the ledger dropped from 6 runs to 3 and was restored a minute later. | **Silent.** Only a run count or file size reveals it. Never run two harvest mutations at once; check `runs:` count before and after. |
| One work counted twice | title variance, no `work_id`, no alias | silent — appears as two lower-confidence entries |
| Confidence divided by the wrong denominator | `promote` uses runs *for that passage*, not total runs; pilot and full loci have different denominators | silent |
| A work outside its real extent | model error | not detectable by the tool; check against the extent table above |
| `harvest promote` exits non-zero | **defect:** the text renderer iterates `payload["works"]`, which `run_promote` returns as an `int` → `TypeError`. Non-dry-run `_dump`s the index *before* the crash. | use `--json`; treat a text-mode promote as having already written the file |
| A locus silently loses works | a reference grouped across chapters | always pass `--by-chapter` |
| A post-1900 work enters | — | cannot: `record` rejects `death_year > 1900` |

### Verification

```sh
sh tests/tools/harvest.test                    # prints "ok"
sh tests/tools/commentary-work-index.test
tools/tpt harvest plan --corpus src/sources/commentary/mass-commentary-corpus.yaml \
  --by-chapter --json                          # pending should be 0
tools/tpt harvest promote --audited-on <date> --dry-run --json   # --json is required
tools/tpt harvest propers --top 20             # the acquisition list as it stands
```

`harvest` is **not** in `make check`. Run its test explicitly.

### Standing caveat

The harvest is **model-generated leads requiring collation**. Not citations, not
evidence, not scholarship. Its product is an acquisition list — which works to
obtain — with a measured agreement figure per entry. Say so wherever it is
surfaced.
