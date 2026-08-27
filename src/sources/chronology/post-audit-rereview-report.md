# Targeted cold re-review — post-audit chronology corrections

```text
review target:        214797e78   (branch feature/bible-dating, == HEAD)
audited corpus:       2330d63a5   (what the cold audit reviewed)
correction start:     9d3dd2fc0   (the commit that added the audit artifacts)
origin/main:          2778285849f2973ea89d1cfd5b2751ed4ae58e54
branch advanced beyond the target: no
```

**A limitation to state first, because it bears on how much weight this review
carries.** The lane that made these corrections and the lane writing this review
run in the same session. That is not independence in the sense the deliverable's
`independent-source-audit` requirement means. What independence there is comes
from elsewhere: every one of the 92 rows was reviewed by a **fresh agent with no
memory of why the correction was made**, working only from the manifest, the
ledger's claims and the sources; and the reviewers were told in terms not to
trust the ledger, the tests, or the correction report. Several of the findings
below are defects in the correcting lane's own work, found by those reviewers and
confirmed at source here. But a genuinely cold reviewer should still repeat this.

## Manifest

| | |
| --- | --- |
| path | `src/sources/chronology/post-audit-rereview-manifest.tsv` |
| expected rows | 92 |
| reviewed rows | **92** |
| missing | none |
| duplicates | none |

The manifest was checked for the thing it would be easiest to fake: whether it
is a real diff or a convenience sample. It is real. Loading both corpora through
`scripts/_chronology.py` and diffing the loaded objects — not the YAML text, so a
reformat could not hide a change — gives 63 changed claims, 7 changed bindings
and 6 changed gap rows. The manifest carries exactly 63, 7 and 6, and the set
difference is empty in both directions for all three kinds.

## Results

| | |
| --- | --- |
| rows reviewed | 114 (92 manifest + 8 withdrawn findings + 14 whole-corpus checks) |
| PASS | **91** |
| CHANGES_REQUIRED | **23** — 0 critical, 9 major, 14 minor |
| BLOCKED_SOURCE_UNAVAILABLE | 0 |
| BLOCKED_SOURCE_INSUFFICIENT | 0 |

**No critical defect survives, and the corrections to the audited defects are
overwhelmingly right.** What fails is a second layer: five of the failures are in
records and prose the correction lane *created*, and three are places where it
corrected one half of a finding and left the other.

## The critical correction — Flood to Call of Abraham: PASS

All nine required checks verified from source and production data.

The table row is *"Hence, number of years from Flood to Call of Abraham"*, reached
from the row above it by *"Add for age of Abraham at time of his call: 75"*. Genesis
12:4 in the tracked Douay gives the seventy-five. The birth carried four claims at
`2330d63a5` and carries one now; a grep for 367, 1017 and 1147 across the whole
corpus hits only the `call-of-abram` block and the birth's own historical note.
The three remain distinct text-family alternatives, rank-6, beneath the rank-1
Genesis claim, which satisfies §4.4 on rank alone. `query Gen.12.4` returns all
four; `query Gen.11.26` returns only the 720-year claim.

The regression test was proved to bite, twice, against copies in scratch: restoring
the pre-correction state verbatim fails it, and duplicating the three claims back
onto the birth while the call keeps them also fails it. Both limbs of the guard work.

## The native-span gate: PASS

Verified by construction rather than by reading the tests. A probe unit scoped to
greek Ecclus 36:1–16 carrying the date the Vulgate unit already holds — first locus
refusing the concordance, interior locus 36:16 mapping safely and duplicating — is
**refused by the loader, naming 36:16**. The audited predicate re-run verbatim over
the same scopes produces **zero refusals**: it probed 36:1, got a refusal, and
admitted the span entire. The control, the same probe narrowed to 36:1–15 with no
safely-mapping locus inside, loads — so the gate refuses duplication rather than
nativeness. A native `hebrew` Psalm 51 unit is refused through the renumbering
branch, and an unknown system is refused with a typed reason naming the admissible
set. The implementation derives its systems from `_projection`, `_psalms` and
`_deuterocanon`; the only literal system names in `_chronology.py` are a routing
hop-path, not a second roster.

Greek Sirach survives and is exact: the witness prints **1 356** loci, of which
**1 355** refuse the Vulgate and exactly one, 36:16, carries safely — and at that
one locus both units answer, the Greek translation's date beside the Vulgate's.
That is §3.0.1's closing rule working, and not a duplicated fact: the cited article
separates the two acts itself.

## Mapping status and chronology status: PASS

The seven native loci were each verified as real text in its own witness file
rather than inferred from a range, and each answers `mapping: textually-distinct`
with `chronology: research-pending`. Non-coercion was shown four ways, including
by authoring a native gap row on a copy and watching the chronology axis move to
`undated-in-tradition` while mapping stayed `textually-distinct` — which proves
`research-pending` is §9's un-authored default here and not a dead end.

The three dismissed non-loci are genuinely not text. The tracked World English
Catholic witness runs Esther 4:5 → 4:7 and 9:4 → 9:6 and 9:29 → 9:31, the
edition's own alias table carries `not-in-this-edition` rows saying so in words,
and extracting `2330d63a5` shows `_printed` already returned 2 094 without them
while `_system_loci` returned 2 131 with them. They were an artefact of the
chapter densification, correctly dismissed.

## RR-090 — Howlett's 958 B.C.: **CHANGES_REQUIRED**

The directions require an explicit ruling and this is it.

Howlett **asserts** the figure in his own voice, and the sentence names its own
ground: *"We conclude, therefore, that the date of the Exodus was about 1277, the
monarchy was founded by Saul, 1020; David mounted the throne, 1002; Solomon in
962, and the Temple was begun, 958 B.C."* The "therefore" refers to a paragraph
that is modern-critical from end to end — "almost a consensus of scientific
opinion", "Assyriologists and Egyptologists agree" citing Driver, Ramses II
"from 1348-1281 (Sayce)", the concession "we are left with only about 327 years,
as against 480 required by 1 Kings 6:1", and finally "Wellhausen and Stade regard
6:1 as a late insertion". Of the Catholic reading Howlett says the opposite: *"For
the Catholic, that passage seems to settle the question."* 958 is 962 less four
regnal years and 962 descends from the 1277; the article gives it no independent
traditional ground.

§4.1 says the profile "is not normalised to modern archaeological, Egyptological,
Assyriological or critical-historical chronology". §4.3 says modern critical
chronology is "not consulted", and grants an express reporting licence to Ussher
**by name** and to nothing else — which is exactly why claim #2 on this same
event, Howlett printing Ussher's 1010, stands and this one cannot. `alternate` is
a disposition among claims already admitted; it opens no admission route past
§4.3. And the correction lane withdrew 1277 and 1020 from this one sentence as
modern-critical while keeping 958 from the same sentence. One sentence cannot be
two profiles.

**Required correction:** withdraw `israel.monarchy.temple-begun#5` from
`catholic-traditional-v1` — remove it, do not re-dispose it — and record the
figure and the profile boundary in the event's subject note, in the shape
`israel.exodus.the-exodus`'s note already uses. A rank-1 preferred claim and five
alternates remain, so nothing structural breaks.

**Ruled with it:** `temple-begun#4`, Howlett's "about 969", rests on the same
reconstruction and should be settled in the same breath. It differs only in that
969 has independent traditional support from Sloet's table, carried separately as
claim #3 under a different artifact.

## The eight withdrawn findings

Six upheld, two rejected.

**Upheld.** V-008, V-012 and V-013 are loci that do not exist, verified past the
function to the tracked bytes. LEAD-001, LEAD-002 and P-012 are one misquotation
three auditors found and one correction closed — settled here by rendering
Haydock facsimile page 776 at 300 dpi and reading the column as an image, because
the retained OCR misreads the disputed numerals ("8405" for 3405, "A.M:" for
A. M.). The page prints *"…under Joakim, A. M. 3398, the second, under Jechonias,
3405, and the last, when the city was destroyed and Sedecias was taken, 3416
Usher."* The production strings now quote it verbatim.

**Rejected — WD-A4-017 (major).** The withdrawal's central ground is that the
audit asked for a shape the model cannot express, because an event must carry a
non-empty `dates` list. That is no longer true, and it was made untrue *by the
same lane*: `scripts/_chronology.py` now says in terms that an event may carry no
claim, and `israel.monarchy.saul-accession` is exactly that at HEAD. The audit's
shape is expressible and was not applied. Worse, the claim anchors on
`israel.exile.ezechiel.ministry`, which is its own `parent` — the container —
and `Date.anchor` returns it, which §10.0's "Containment is not offset" exists to
prevent.

**Rejected — WD-F-021 (minor).** The guidance does defeat the finding's first
limb: "Changed bytes receive a new artifact record and consumers remain pinned
until reviewed." But the finding was disjunctive and its second limb is untouched
— neither later record says it is a re-retrieval, and five Pentateuch gap rows
still cite one article under two ids without disclosure. That is deferral, not
defeat.

## What the correction lane created and got wrong

Five failures are in records and prose the lane itself wrote.

- **Five of six newly registered articles misname their own article** (major).
  Every hash and byte size is exact, but the `notes` citations were taken from the
  Genesis gap row's list of *index entries* and shifted by one against the article
  numbers. The pages' own citation lines read Alston "General Chapter" (06412b),
  Gigot "Generation" (06412c), "Genesareth" (06413a), Mershman "Genesius"
  (06413c), Thurston "Use of Numbers in the Church" (11151a). `gaps.yaml` has the
  titles right, so the record and the row citing it now disagree. The false
  citations are published downstream in the derived web JSON.
- **The two registered index pages disclaim the exhaustiveness the work record
  claims for them** (major). `g.htm` prints "This list represents only a tiny
  fraction of articles available on the New Advent website"; the unabridged index
  is `g-ce.htm`, three times the size, with no such disclaimer. The work record
  asserts these pages list "every article the encyclopedia carries under that
  letter", and the Numbers gap row says "its full index for N" to consumers. The
  negative itself survives — neither unabridged index carries a Genesis article,
  and the N index carries only "Numbers, Use of, in the Church" — but the
  registered evidence does not establish it. That is §15.1(4) recurring inside the
  correction made to answer §15.1(4).
- **Three duplicate mapping keys** (minor), in `events.yaml` and `composition.yaml`,
  left by edits applied as string replacement while other edits moved the same
  region — the same origin as the Ps 70 truncation the lane self-reported. Every
  duplicated pair is identical, so no value is wrong, and that is the problem:
  PyYAML silently keeps the last, so `validate`, 92 tests and the coverage build
  all pass over a corpus that is invalid YAML 1.2.
- **The governing contract still forbids what production holds** (major). §6 reads
  "an id, a title, an optional parent, and one or more dated claims", while the
  loader now permits zero and one event uses it.
- **A note carried to a new subject without being re-read** (minor): the claim that
  780 years is "wider than the whole antediluvian disagreement" is false — the same
  article gives 1656 / 1307 / 2242, a spread of 935.

Plus three places where half a finding was applied: the Abdias note now withholds
the ground for leaving a rival opinion unauthored; the Micheas withdrawal's
comment overstates the article's silence; and a dependency count went stale inside
the same lane that made it stale.

## Coverage — reproduced

| Vulgate/Clementine primary | |
| --- | --- |
| total | **35809** — recounted from the canonical edition's own chapter files |
| dated | 12541 |
| composition-only | 16504 |
| undated-in-tradition | 6764 |
| research-pending | 0 |

| Additional native | printed | shared | already counted | additional |
| --- | --- | --- | --- | --- |
| `greek` | 2156 | 800 | 0 | **1356** |
| `hebrew` | 2528 | 2528 | 0 | **0** |
| `world-english-catholic` | 2094 | 730 | 1358 | **6** |

Declared universe **37 171**, reproduced independently. For every system the
tool's `printed_loci` equals what the witness prints, and shared + already-counted
+ additional equals printed exactly, so no alias is double-counted. Walking every
printed locus of every native system, **none answers a mapping word or an
unknown status**. `septuagint`, `nova-vulgata` and `nab` are reported
`enumerable: false` with a reason.

## Structural validation — re-measured

| Gate | Result |
| --- | --- |
| chronology tests | 92 / 92 |
| validate / check | clean; 1 882 coverage rows, table current |
| source-library | 540 works, 722 editions, 1 918 artifacts |
| promised-deliverables | ledger valid |
| `check-examples` | 4 diverged — the inherited set |
| `tmt check` | the same 8 undeclared siblings, none chronology |
| `make -k check` | the same 4 targets |
| full suite | 1 828 tests, 36 failures — **byte-identical failure set** to the correction lane's measurement |

The failure comparison was reproduced by name, not accepted: the set at the review
target diffs empty against the set the correction lane reported.

## The report's stale self-reference

`post-audit-correction-report.md` names `correction final HEAD: 15213f79ca…`
while the target is `214797e78`, six commits later. Verified: no chronology YAML,
no coverage table and no `scripts/` file changed in those six. It is bookkeeping,
not a chronology defect, and belongs in a closeout lane. One qualification — one
of the six, `bff00167f`, changed a shell gate's assertion rather than only
recording measurements, so the report's implicit "nothing but recording" is
slightly too strong.

## Promised deliverable — `scripture-chronology-corpus-2026-08-26`, `in_progress`

**`translation-independent-identity` — RECOMMEND PASS.** All five criteria hold
and the fifth was verified by construction, not by reading the tests: the gate
refuses a span whose first locus is valid and whose interior is not, and the
audited predicate demonstrably admits the same span. Greek Sirach remains native
and exact; the Psalter renumbering remains refused; an unknown system is typed and
refused; chronology identity is keyed to no edition. None of the failing rows in
this review touches this requirement.

**`exhaustive-coverage` — RECOMMEND PASS, with the reasoning exposed for the
maintainer to overrule.** Read strictly, the criterion asks five things and all
five now hold: the universe is named; every Vulgate locus reaches exactly one
typed status and none is silently undated; every additional native locus is
accounted for without counting an alias as new Scripture; mapping status is
reported as its own axis rather than as a chronology status — the defect this
requirement was reopened for; and the report distinguishes substantive,
composition-only, multi-assertion, alternative-bearing, research-gap and
mapping-refused without a headline percentage. **The criterion nowhere requires
zero `research-pending`**: it requires a research-gap *category*, and the seven
native loci occupy it honestly. The correction lane's own note read the criterion
more strictly than it is written and kept the requirement open on that reading.
Erring toward open is the safe direction, but this review is asked to judge
against the criterion as written, and as written it is met. If the maintainer
intends the stricter reading, the criterion should say so rather than be enforced
by a note.

**`independent-source-audit` — KEEP OPEN.** Twenty-three rows failed, nine of them
major, and one of the two mandated architecture rulings went against the corpus.
Beyond that, the reviewer of record here is not independent of the corrector.

## Overall

```text
CHANGES_REQUIRED
```

The audited defects were, with few exceptions, corrected well and at source; the
critical correction is right in all nine of its required particulars, and both
architecture defects are genuinely fixed and provable by construction. But
RR-090 is a live profile leak — a modern-critical figure standing under
`catholic-traditional-v1` from the same sentence as two the lane withdrew — and
the correction lane introduced a second layer of provenance defects in the records
it created to close the first. One material failing row is enough, and there are
twenty-three.

## Next safe lane

A bounded correction lane addressing only the failed rows, in this order:

1. **RR-090**, and `temple-begun#4` in the same breath;
2. **WD-A4-017** — apply the audit's shape, which the model now expresses;
3. the eight source records the lane created — five misnamed articles, two
   mis-characterised index pages, and the work record's exhaustiveness claim —
   rebuilding the derived web view in the same commit;
4. guidance §6, so the contract admits the claimless event production holds;
5. the three duplicate mapping keys, **and a strict-duplicate-key check**, because
   nothing in the current gate can see them;
6. the remaining prose: the antediluvian comparison, the Abdias ground, the
   Micheas comment, the Leviticus closing clause, the stale dependency count, the
   stale final-HEAD reference, and the manifest's `why` column, which labels three
   re-anchorings as `changed:note`.

Then another cold re-review of every changed row — by a reviewer that is not this
session.

**DO NOT MERGE.** This review authorizes no merge and no propers integration.
