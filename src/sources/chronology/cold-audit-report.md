# Cold independent source audit — Scripture chronology corpus

**Audited corpus: `2330d63a5`** (`feature/bible-dating`), the immutable target
named in the audit directions. `origin/feature/bible-dating` was at exactly that
commit when the audit began and had not advanced beyond it; the working tree was
clean. `origin/main` was `2778285849f2973ea89d1cfd5b2751ed4ae58e54`, one commit
ahead of the branch's merge-base `22528396af94b146621fb59ae2a67061af31e088`.
Nothing in the chronology corpus was changed by this lane.

This is a **review lane**. No chronology data, code, test, guidance file or
promise state was edited. The findings below record what a second reader found
by reopening the sources; they do not repair anything.

## How the sources were reopened

Every non-Scripture source record the corpus cites was re-fetched from its
registered `source_url` and hashed: **127 records, all of them reopened** — 115
New Advent web artifacts and 12 Haydock passage records, the latter all standing
on one facsimile PDF. That PDF (327 MB, `sha256 9d2dd602…`) **matches its
registered artifact hash exactly**, and the nineteen distinct PDF pages the
passage records name were extracted to text and read. Scripture was read from
the tracked Douay-Rheims chapter files, never from recollection. **No claim in
this audit is blocked for want of a source**: `BLOCKED_SOURCE_UNAVAILABLE` and
`BLOCKED_SOURCE_INSUFFICIENT` are both zero.

**On the New Advent hashes.** 96 of the 121 re-fetched pages hash differently
from their registered `sha256`. Every one of those differs by *exactly* −359
bytes, uniformly, across articles of every size — New Advent's page template
lost 359 bytes of boilerplate after the population wave. Two consecutive
fetches of the same page agree byte for byte, and the article text is
unchanged. **This is a site change, not a corpus defect, and it is not a
finding.** It is recorded here because a later reviewer will otherwise
rediscover it and misread it.

## What "reproduced" means below

Every count in this report was re-derived by this lane from the pinned commit
with the repository's own tools, not taken from the prior lane's report.

## Totals

Every finding was put through an independent pass briefed to refute it, and most
findings through two. **Where the two passes split, the finding is held
standing** — 35 findings are in that position, so the standing count is the
conservative reading, not the confident one.

| | |
| --- | --- |
| finding rows written | 564 |
| distinct factual claims inspected | 324 |
| binding scopes inspected | 94 |
| source records reopened | 127 (115 New Advent web artifacts, 12 Haydock passage records over one hash-verified facsimile) |
| source families | Catholic Encyclopedia, Haydock Douay-Rheims, tracked Douay-Rheims, Eusebius, Jerome, Augustine |
| authority ranks represented | 1 (Scripture), 3 (Haydock), 4 (Eusebius / Jerome / Augustine), 6 (Catholic Encyclopedia) |
| **PASS** | **392** |
| CHANGES_REQUIRED raised | 172 |
| — refuted on verification | **68** |
| — standing | **104 rows, 84 distinct defects** |
| distinct defects by severity | **1 critical (over 3 claims), 42 major, 38 minor** |
| BLOCKED_SOURCE_UNAVAILABLE | 0 |
| BLOCKED_SOURCE_INSUFFICIENT | 0 |

**There is exactly one critical defect.** It occupies five finding rows across
three claims — the Flood-to-Abram figures on `israel.patriarchs.birth-of-abram`
#0, #1 and #2 — because three auditors found it separately and the lead found it
again. It was confirmed twice at source and once by arithmetic against the anchor
event's own A.M. figure. Every other surviving defect is major or minor.

**Two in five raised findings did not survive.** That is worth stating as
plainly as the defects, because it is the measure of how much a single-pass audit
would have overstated. The refutations were not procedural: they turned on the
contract permitting what was flagged — a hedge preserved structurally rather than
in a label, an A.M. figure kept in its printed era, an opinion recorded *as*
reported, `disputed` doing exactly the work §4.4 designed it for, and a
`relative` date carrying no magnitude to resolve wrongly.

Rates are given as counts, not as a corpus-wide precision percentage. The sample
is stratified by `(precision, disposition)`, it deliberately excludes the
high-risk classes, and 72 claims license no percentage over 458. **After
verification, 15 of the 72 sampled claims still carry a defect** — none critical,
and the kinds are dispositions the source does not support, quotations that are
not verbatim, and hedges dropped from a display label. That is a corpus whose
research is broadly sound and whose encoding discipline is not yet uniform.

## Results by audit class

Every high-risk class was inspected **completely**, not sampled. "Raised" is what
an auditor filed; "standing" is what survived an independent pass briefed to
refute it.

| Class | Inspected | PASS | Raised | Standing |
| --- | --- | --- | --- | --- |
| durations / relative offsets — all 217 | 218 | 178 | 40 | 16 (3 critical, 9 major, 4 minor) |
| Psalm settings + all setting bindings | 34 | 28 | 6 | 3 (2 major, 1 minor) |
| native non-Vulgate chronology | 5 | 1 | 4 | 3 (1 major, 2 minor) |
| traditional-vs-modern divergence | 62 | 40 | 22 | 16 (1 critical, 8 major, 7 minor) |
| negative / silence claims — all 20 gap rows | 21 | 13 | 8 | 6 (6 minor) |
| previously corrected §15.1 defects — all 10 | 16 | 11 | 5 | 5 (5 minor) |
| binding scopes + Ezechiel | 54 | 48 | 6 | 2 (1 major, 1 minor) |
| named-system identity | 9 | 5 | 4 | 3 (1 major, 2 minor) |
| profile boundary + provenance | 37 | 18 | 19 | 5 (2 major, 3 minor) |
| coverage universe | 18 | 3 | 15 | 14 (13 major, 1 minor) |
| **deterministic sample — all 72** | 72 | 46 | 26 | **15 (6 major, 9 minor)** |
| lead's own findings | 18 | 1 | 17 | 16 (1 critical, 7 major, 8 minor) |

Three rows deserve comment rather than a number.

**The sample.** 26 of 72 sampled claims raised a defect; **15 survived**. The
directions ask this to be said plainly rather than converted into a corpus-wide
precision figure, and it will not be: the sample is stratified by
`(precision, disposition)`, it deliberately excludes the high-risk classes, and
72 claims license no percentage over 458. What it licenses is a statement about
kind. None of the 15 is critical. They are dispositions the source does not
support, quotations that are not verbatim, and hedges dropped from a display
label — a corpus whose research is broadly sound and whose encoding discipline is
not yet uniform.

**Coverage shows 14 standing because each affected locus is its own row.** There
are two underlying defects — the ten native loci carrying a mapping word where a
chronology status belongs, and the densified enumeration — not fourteen.

**The duration class fell from 40 raised to 16.** That is the largest correction
verification made, and it has one cause, stated next.

### One structural fact that bounds every anchor finding

A `relative` date in this corpus carries **only** `{of, statement, note}` —
`scripts/_chronology.py` rejects any other key — so it has no signed magnitude
and **nothing computes from it**. The figures a reader sees ("367 years from the
flood", "after forty years") live in the prose `statement` and `label`.

This is why so many anchor findings fell: where a finding alleged that an offset
"resolves N years wrong", there is no N to resolve. The corpus's own guidance
records the same constraint at §10.0 — *"Nothing computed with them, which is the
only reason no wrong date had yet been produced."*

It does not make a wrong anchor harmless. A claim whose `statement` attaches a
figure to the wrong subject is a false statement displayed to a consumer, and the
first consumer that *does* compute — which is what the `relative` precision exists
to permit — inherits every one of them. But the distinction decides severity, and
this report applies it: an anchor defect is **major** where the displayed claim is
false, **minor** where the structure is wrong but the displayed words are the
source's own.

## The audit manifest

`src/sources/chronology/cold-audit-manifest.tsv` exists, is documented in its own
header, and holds **72 data rows** under one header row. Every one of the 72 ids
resolves to a real authored claim; the declared `precision`, `disposition` and
`sources` on every row match the corpus exactly; and no id appears twice. Seven
subjects contribute more than one row — different dated alternatives of one
subject, which are genuinely different factual claims — so the 72 rows cover 63
distinct subjects.

**The sample is deterministic and was not steered.** Implementing the header's
stated rule — strata of `(precision, disposition)`, ordered within each by
`sha256(seed + id)` with the recorded seed, round-robined in sorted strata order
until 72 are taken — over the 458 authored claims reproduces **71 of the 72 rows**.
Supplying one further exclusion reproduces **all 72 ids in the file's exact
order**. A sample that reproduces in order cannot have been hand-picked, and the
file's claim that "nothing here was hand-picked" is **verified**.

**But the file's claim to be "reproducible from this file alone" is false.** The
missing exclusion is every claim of `israel.exile.third-captivity`. It is
principled — `PROJECT-WORK.md` names four excluded high-risk classes, one being
the Psalm historical-settings, and `third-captivity` is the event the Psalm 88
historical-setting binds to — but that predicate lives in `PROJECT-WORK.md`, not
in the file, and a reviewer working from the file alone cannot derive it. The
exact reproducing predicate is: exclude `precision == "duration"`, and exclude
every claim of a subject a Psalm `historical-setting` binds to.

**The complete-inspection set is not tracked anywhere.** The prior report
describes 72 sampled claims *and* 57 for complete inspection; the tracked file
holds only the 72 and says the high-risk classes are excluded from it. This lane
had to re-derive the classes from the corpus itself — 217 duration/relative
claims (47 `duration`, 170 `relative`), 11 `historical-setting` + 15
`superscription-setting` + 23 `prophetic-referent` bindings, 20 gap rows, and the
single native non-Vulgate assertion. Nothing stops a later reviewer deriving a
different set from the same words. `PROJECT-WORK.md`'s own arithmetic for that
set does not add up either: it says the four classes total 57 and then lists
47 + 9 + 2 + 1 = 59.

## Coverage, reproduced

The Vulgate/Clementine primary universe reproduces **exactly** as the prior lane
reported it, and the load-time accounting gate makes the zero a checked zero:

| Vulgate/Clementine primary universe | Reproduced |
| --- | --- |
| total | 35 809 |
| `dated` (substantive) | 12 406 |
| `composition-only` | 16 687 |
| `undated-in-tradition` | 6 716 |
| `research-pending` | **0** |
| of the substantive: direct only | 3 646 |
| inherited only | 7 354 |
| both | 1 406 |

The additional-native figures do **not** reproduce, and the repository already
contradicts itself about them:

| System | Reported | Printed by the witness | Correct additional |
| --- | --- | --- | --- |
| `greek` | 1 391 | 2 156 loci (Ecclus 1 356) | **1 356** |
| `hebrew` | 0 | 2 528, all shared | 0 |
| `world-english-catholic` | 9 | 2 094 | **6** |
| declared universe | 37 209 | | **37 171** |

`_chronology._system_loci` builds each chapter as `range(low, high + 1)` from
`_deuterocanon._extents`, which keeps only the first and last verse number the
witness prints. Every verse number the witness *skips* is invented back — 38 in
`greek`, 37 in `world-english-catholic`. The 35 invented Greek Ecclesiasticus
loci are precisely the Latin pluses that the corpus's own cited article calls
"foreign not only to the Greek, but also to the Hebrew text", so the count turns
Latin expansions into Greek Scripture and then reports a composition date as
applying to them.

The corrected figure is not new information to this repository: **`scripts/_chronology.py`'s
own module docstring and `src/sources/chronology/composition.yaml` both say
"1 355 of its 1 356 loci"**, while `guidance/scripture-chronology.md` §3.0.1 and
§9.3, `PROJECT-WORK.md` and the coverage report all carry 1 391. Two figures for
one fact are live in one repository — `guidance/the-shape.md` §2, inside the very
number the `exhaustive-coverage` requirement turns on.

### The native loci with no chronology status

Ten, enumerated independently by this lane and matching the prior report's count.
Each carries `textually-distinct` — a **mapping** answer — in the place a
chronology status belongs, which is the axis confusion §3.0.1 was written to end,
surviving in the derived coverage view.

| System | Locus | Recommended next disposition |
| --- | --- | --- |
| `greek` | `EsthGr.15.10` | should be `research-pending` — no ranked source has been inspected for it |
| `world-english-catholic` | `Dan.3.71` | should be `research-pending` |
| `world-english-catholic` | `Esth.1.1` | should be `research-pending` |
| `world-english-catholic` | `Esth.3.13` | should be `research-pending` |
| `world-english-catholic` | `Esth.4.6` | should be `research-pending` |
| `world-english-catholic` | `Esth.5.1` | should be `research-pending` |
| `world-english-catholic` | `Esth.5.2` | should be `research-pending` |
| `world-english-catholic` | `Esth.8.13` | should be `research-pending` |
| `world-english-catholic` | `Esth.9.5` | should be `research-pending` |
| `world-english-catholic` | `Esth.9.30` | should be `research-pending` |

Under the corrected enumeration the count falls from ten to **seven** (one
`greek`, six `world-english-catholic`); three of the nine
`world-english-catholic` entries are among the invented loci.

They cannot be given a status today, and the reason is structural rather than
editorial: `_native_assertions` reads only units and bindings, and the gap loop
in `chronology()` sits downstream of a *successful* conversion, so a native locus
that refuses the Vulgate can reach no authored gap row at all. **A correction
lane cannot close these ten by authoring data; it must first give them a route.**

`exhaustive-coverage` is therefore **OPEN**, which is where the ledger already
has it. The gap is explicit and bounded and no fact is silently asserted over it.

## Structural validation, re-measured

Every gate below was run by this lane at `2330d63a5`, and every comparison is
against the branch's own merge-base `22528396a` in a separate worktree.

| Gate | Result |
| --- | --- |
| `scripture-chronology validate` | valid: 1 profile, 276 events, 60 composition units, 374 bindings, 20 gaps, 73 books |
| `scripture-chronology check` | coverage table current: 1 877 rows |
| `scripture-chronology coverage` | reproduced exactly; see below |
| chronology tests (`test_chronology.py`) | **84/84 OK** |
| full suite, branch | 1 820 tests, 23 failures + 13 errors = **36** |
| full suite, base `22528396a` | 1 736 tests, 24 failures + 13 errors = **37** |
| `make -k check`, branch | 4 targets fail |
| `make -k check`, base | **the same 4 targets fail** |
| `tmt check` | fails: 8 tools use a sibling without declaring it in `requires`; none is chronology |

**There are no branch-only test failures.** Comparing the two failure lists
name by name, the branch introduces none and the base carries one the branch
does not (`test_shell_smoke_tests_pass` on `pdf-review.test`, which needs a
built PDF the fresh base worktree has no copy of — an environment difference,
not a code one). The test-count difference, 1 820 − 1 736 = 84, is exactly the
chronology suite this branch adds.

**This corrects the tracked handoff.** PROJECT-WORK.md records "One branch
regression against `origin/main`" — `test_shell_smoke_tests_pass` on
`source-family-migration.test`. That test fails **identically at the
merge-base**, with the same two errors (`pinned canonical_catalog_snapshot is
stale`, `pinned inventory_snapshot is stale`) naming the base worktree's own
path. It is an inherited failure, not a branch regression. The handoff's own
next sentence half-says so; the label above it does not.

**The stale source-family snapshot has correctly not been refreshed.** Re-pinning
asserts that the review the pin stands for has happened. This audit is a review
of the *chronology corpus*, not of the 128 source artifacts the pin covers, so it
does not discharge that pin, and this lane has not touched it. The four
`make -k check` failures — `check-web-editions-current`, `check-sources`,
`check-tool-registry`, `check-examples` — are all inherited and none is
chronology. All eleven captured `scripture-chronology` CLI examples replay `ok`.

Two figures in the handoff's own accounting of these gates do not reproduce:
it reports `check-examples` diverging on 4 examples on the branch and **24** on
base; this lane measures 4 on the branch and **6** on base.

## The ten defects §15.1 says this corpus once had

Every one re-audited from source. The corrections are real: **nine of the ten
underlying defects are genuinely fixed**, and the five residues below change no
factual result.

| # | Old defect | Current state | Result |
| --- | --- | --- | --- |
| 1 | a quotation from memory (Gen 18:10) | the tracked Douay wording is now stored; a corpus-wide sweep of 1 014 quoted spans against retained evidence found the fix held here | **PASS**, with residues (below) |
| 2 | a wrong relative anchor (Jacob's twenty years) | re-anchored; Genesis 29–31 read in the tracked text confirms it | **PASS** |
| 3 | a figure the source reports, not asserts (both Esdras, "as most critics think") | units withdrawn, typed silence in their place, both gap rows sound | **PASS** |
| 4 | a claim about a source with no retained retrieval (four articles) | replaced; "Adam" and "Sara" now handled correctly, both reopened and checked | **PASS**, one wording residue |
| 5 | a refusal gone stale mid-wave (two psalms, one superscription) | the two now agree | **PASS**, one consistency residue |
| 6 | a duration encoded as an offset (47 claims) | 47 `duration` claims, none carrying an anchor, none carrying endpoints | **PASS** |
| 7 | authorship promoted to occasion (Ps 21) | withdrawn; the `prophetic-referent` survives | **PASS** |
| 8 | directness confused with applicability (Ezechiel's 271) | status now asks what applies; 271 reproduces exactly | **PASS** |
| 9 | a textually distinct locus treated as undated (Greek Ecclus) | two axes, both returned | **PASS** |
| 10 | a wrong route enshrined in a test (WEC's 2 131 loci) | route corrected; no test asserts the old refusal | **PASS** |

**The five residues.** A Scripture quotation in a `retrospective-event` note still
differs from the tracked Douay; the Haydock captivities quotation substitutes
"Jerusalem" for the page's "the city" inside quotation marks (found independently
three times over); the Habacuc basis drops the source's own "It seems, however,
that"; the Genesis gap row characterises as the encyclopedia's own a figure that
is three-quarters Scripture's; and one bracketed superscription list is applied to
two psalms and not to four others it names equally.

**The lesson of §15.1(1) has been learned unevenly, and that is the honest
summary.** A machine sweep of every quoted span of 25 characters or more in every
`basis`, `note` and gap `reason` — 1 014 of them — against the retained article
text, the Haydock pages and the tracked Douay, found the overwhelming majority
verbatim. The exceptions cluster in one place: quotation marks placed around the
repository's *own* prose, or around a paraphrase, in a position where a reader
takes them for the source's words.

## Psalm settings, and the one rule Ps 21 and Ps 88 stand under

Complete class: **all 11** `historical-setting` bindings, **all 15**
`superscription-setting` bindings, and the **8** Psalm `prophetic-referent`
bindings — 34 targets, none skipped. Six raised change; twenty-eight pass.

**Psalm 21 (Vulgate) / Psalm 22 (Hebrew).** No `historical-setting` survives, and
none of any kind. Verified three ways: no `historical-setting` or
`superscription-setting` binding in the corpus has `Ps.21` in scope; a live query
at `Ps.21.1` and `Ps.21.19` returns *only* `prophetic-referent` to the Crucifixion
(and an `utterance` at `Ps.21.2`); and `composition.yaml` holds no unit for it.
The Passion referent is separately source-supported and survives the withdrawal
intact, which is what §8 says should happen — removing a `historical-setting`
does not disturb a `prophetic-referent` over the same psalm. Christological
fulfilment was **not** used anywhere as evidence for a Davidic occasion.

**Psalm 88 (Vulgate) / Psalm 89 (Hebrew).** Still refuses an authorship-derived
setting, and still says so in its own note.

**The one rule.** *Attribution is not occasion.* Ps 88 refused to convert "of
Ethan" into an occasion; Ps 21 had converted "of David" plus the years David
reigned into one, and that was withdrawn on 2026-08-27. Both now stand under §8's
single sentence — "traditional authorship or attribution ALONE never establishes
a `historical-setting`" — and the corpus is consistent across them. What
distinguishes a surviving setting from a withdrawn one is whether an inspected
source *identifies an occasion*, not how confidently it names an author.

The six that raised change are not failures of that rule. The two major ones are:
a whole-book `historical-setting` over **Daniel** that reaches verses set seventy
years later (above), and **Psalm 30**, where the single cited Haydock page offers
*five* mutually exclusive settings and settles none — "David composed it when he
was obliged to flee from court … or in the desert of Maon … though some refer
this psalm to the conspiracy of Absalom … or to the unpremeditated fall of David
… or to the captives" — and one of the five is bound, unhedged, as the answer.
§4.4 says preserve the disagreement. The remaining four are quotation and
citation defects that change no factual result.

## Ezechiel's inherited applicability — PASS

Reproduced independently: Ezechiel has 1 272 verses, **all** of them `dated`;
1 001 are reached by one of the fifteen narrower `prophecy-given` bindings, and
**exactly 271** are reached by the whole-book binding alone. The prior lane's
figure is right to the verse.

Every one of the six required checks holds:

1. the underlying assertion is source-supported — the cited article bounds the
   ministry's beginning and gives it a stated minimum length, and treats the
   whole book as the prophet's own prophecy;
2. the authored scope genuinely covers those verses, because every oracle of the
   book was uttered inside that ministry;
3. the query marks the provenance `inherited`, verified per verse;
4. coverage counts them as substantively chronologized — Ezechiel's split is 813
   inherited-only and 459 both, none direct-only;
5. they are not described as directly authored anywhere;
6. `composition-only` stays separate: the book's own composition silence is a
   distinct gap row, and an assertion beats a gap.

This is the §15.1(8) correction working as intended, and the whole-book scope is
not too broad for the evidence.

**The parallel Daniel binding is not.** `historical-setting` over the whole book
of Daniel to `israel.exile.first-captivity` fails the same test: the cited
article dates the *man's* deportation and then follows his career on to the eve
of Cyrus's conquest; it never says the book's occasion is that deportation. The
consequence is concrete — `Dan.10.1`, a verse reading "In the third year of
Cyrus, king of the Persians", is answered with a historical setting of "the third
year of the reign of Joakim", about seventy years out. Ezechiel earns its
whole-book scope because Ezechiel reckons from its deportation throughout ("the
fifth year of the captivity of king Joachin", "the five and twentieth year of our
captivity"). Daniel does not.

## Named-system architecture — independently tested

Not read off the tests. Each path was exercised against the corpus, and the
load-time gate was proved by injecting a violating scope into a **copy** of the
corpus in `.scratch` (never `src/`) and reading the loader's actual error.

**Shared-system path — holds.** `query Ps.51.3 --system hebrew` returns
`asked = Ps.51.3`, `locus = Ps.50.3`, `mapping = {status: shared, reached:
Ps.50.3}`, and an assertions array **identical** to `query Ps.50.3`. The Miserere
is authored once, at `Ps.50`, and reached through `_psalms.convert_point`. No
duplicate authored data exists for it.

**The §3.0 load gate is real — and unsound at one locus.** Injecting a `hebrew`
Psalm 51 scope into a copy of `bindings.yaml`, and again into a copy of
`composition.yaml`, makes the loader refuse both: sharing is possible there, so a
native scope is inadmissible, exactly as §3.0 says. But the gate probes a span at
its **first** locus only. The Greek Ecclesiasticus scope is whole-book; its first
locus (1:1) refuses the Vulgate, so the scope is admitted — while `Ecclus 36:16`,
inside that same scope, *does* carry safely to `Ecclus 36:18`. The rule is right;
its enforcement does not cover the span.

The consequence is smaller than it looks, and it is worth being exact, because
one auditor overstated it. At `Ecclus.36.16 --system greek` the shared path wins
and the answer returned is the **Vulgate** unit's ("between 190 and 170 B.C." and
"about 280 B.C."), byte-identical to querying `Ecclus.36.18`. The Greek
translation's 132 B.C. is *not* returned. **No wrong date reaches a consumer**, so
this is a gate that fails to enforce the rule it exists for — major, not critical.

**Distinct-native path — holds.** `query Ecclus.35.1 --system greek` returns both
axes at once: `mapping = {status: textually-distinct, reached: null}` and
`chronology_status = composition-only` carrying the native claim. No Vulgate locus
is manufactured; native assertions are gathered before conversion is attempted,
and on refusal the Answer keeps the `greek` locus. This is §3.0.1 working.

**Unknown system — holds, at both boundaries.** `--system septuagint` and an
invented name are both refused with a typed reason naming the admissible set;
`query Matt.1.1 --system hebrew` is refused with "`hebrew` does not number
`Matt`; it addresses `['Ps']`", so the **(system, book)** pairing rule is enforced
too. Refusals are returned, never raised, as §12 requires.

**Edition independence — holds.** No chronology schema admits an `edition` key.
Scope keys are `{system, book, chapter, through, first, last}`; claim keys are
`{profile, disposition, date, basis, sources, note}`; `chronology()` and the CLI
take a `--system`, never an edition. Chronology identity is keyed to the
addressing system, not to Douay-Rheims, Knox, WEB or any other surface edition.

### Recommendation

`translation-independent-identity`: **KEEP OPEN.** Four of the five criteria are
independently confirmed and the architecture is sound in design. It should not be
accepted while the gate that makes the "author once at the preferred locus" rule
binding is provably incomplete over a span, and while the coverage view that
reports the named-system universe is inflated by loci the witnesses do not print.
Both are bounded, mechanical fixes; neither requires re-research. This is a
recommendation, not a change: this lane has not edited the promise state.

## Negative and silence claims — all 20 gap rows

Complete class, and the class where this audit most had to correct itself.
Roughly half the defects first raised here did not survive verification.

The discipline §15.1(4) demanded has plainly been learned. The Genesis row names
thirteen source records; the Numbers row sweeps the book end to end, enumerates
every dateline it found, and then names the one passage it reaches that is *not*
covered, so the row cannot be misread as covering it. That is better evidence
practice than most published apparatus, and this audit says so before saying what
is wrong with it.

**What was raised and fell.** The **Amos** row was charged with a false
exhaustiveness claim, on the ground that the page carries "the eighth century
B.C." twice. Verification refuted it on better reasoning than the charge: the
first occurrence is inside the reporting clause itself — "the prophecy of Osee
which is *commonly ascribed* to the same (the eighth) century B.C." — and is
about a different book; the second says the book "furnishes us with most valuable
information concerning the beliefs of the eighth century B.C.", which is content,
not composition. "Jeroboam II (c. 781-741 B.C.)" really is the only from-to
numeral pair on the page. The row is right. The **Exodus** row was charged with
suppressing the article's March–April statement; the corpus already holds that
statement, as a sourced `alternate` claim with the hedge preserved.

**What survives, and it turns on one word.** The rows divide by the verb they
chose. Rows saying the encyclopedia *attaches* no year are accurate — that is a
statement about the encyclopedia's own act, and §4.3 does not oblige a row to
enumerate what it refuses. Rows saying the article *prints* no year are not, and
two do: **Ecclesiastes**, whose page prints Grätz's "under King Herod (40-4
B.C.)" and Hitzig's "about the year 200" in a paragraph actually headed "The time
of the composition of our book"; and **Deuteronomy**, whose Pentateuch article
prints "discovered in the temple 621 B.C." and "after D had been completed in the
sixth century B.C.". The corpus is right not to *author* those figures — they are
other men's, and §4.3 excludes them. It is wrong to say they are absent, and the
corpus's own Exodus row shows it knows the difference: "The years the article
prints are other men's, not its own."

**The unretained half stands, at minor.** Leviticus's `09207a`, Genesis's
`06412b / 06412c / 06413a / 06413c` and the index page for G, and Numbers's
`11151a` and the index for N appear nowhere among the 114 registered
Catholic Encyclopedia artifacts — only in `gaps.yaml` itself. This lane retrieved
the index for N independently and **the characterisation is exactly right**: the
index runs "Nubia … Numbers, Use of, in the Church … Numismatics", with no article
on the book. But a reviewer working from tracked data could not have established
that, which is §15.1(4) in its milder form — register and retain what you
characterise, *including when what you are recording is a silence*. The retained
Deuteronomy stub `04761b` is the corpus's own correct pattern. One incidental
error: the Numbers row's "the neighbouring article numbers are unassigned" is
false — `11150a` is "Francis Nugent" and `11152a` is "Numismatics"; only `11151b`
returns 404.

**No row claims broad traditional silence on one or two sources.** Every row is
scoped to what it inspected and names those articles, so the harder failure the
directions ask about — "this inspected source gives no date" inflated into
"traditional Catholic sources give no date" — does **not** occur anywhere. Every
gap row names at least one source record and every record it names exists; §9.2's
hard gate holds.

## The six claims the prior lane left ambiguous

Directions forbid "ambiguous, needs disposition" surviving this report. Each of
the six is dispositioned below with the source wording that decides it.

**First, a correction this audit had to make to itself.** Several auditors
recommended `CHANGES_REQUIRED_CONTAINED_SPAN` for claims that state containment
rather than an offset. Verification refuted that whole family, on a ground worth
recording: **there is no such precision.** `PRECISIONS` is closed — `day`,
`month-day`, `year`, `approximate-year`, `range`, `interval`, `relative`,
`duration` — and none of them expresses "somewhere inside this span" for a point
event. `duration` requires whole positive units and these state no length;
`interval` requires absolute endpoints and these have none. `relative` carrying
the verse's own words and **no offset value** is the only admissible structure,
and it is what the corpus already uses. A reviewer who asks for a shape the
vocabulary does not hold is asking the author to invent one, which §5's "synonyms
may not [be added]" forbids in spirit.

That refutation lands on four claims raised in this audit and on the lead's own
recommendation for `demand-for-a-king`. It is recorded here rather than buried,
because it is the single most consequential thing verification changed.

| Claim | Source semantics | Stored semantics | Disposition |
| --- | --- | --- | --- |
| `israel.judges.period#0` | Acts 13:20 attaches the 450 years to what *precedes* the judges; the claim's own subject note says the two figures the Douay carries "are **both durations**" | `relative`, anchored on `israel.monarchy.saul-accession` — the period's own terminus, and itself resting on a modern-critical figure | **CHANGES_REQUIRED_DURATION** — re-type as `duration`, which dissolves the anchor and the chain hanging off it |
| `israel.monarchy.absalom-revolt#0` | 2 Kings 15:7, "And after forty years", states no origin; Haydock treats the figure as a manuscript problem | `relative`, anchored on `israel.monarchy.david-reign`, which no source measures from | **CHANGES_REQUIRED_RELATIVE** — de-anchor, or anchor on an origin a ranked source names |
| `israel.exodus.moses-in-madian#0` | — | — | **PASS_AS_AMBIGUOUS** |
| `israel.exodus.moses-in-madian#1` | — | — | **PASS_AS_AMBIGUOUS** |
| `israel.wilderness.mara-and-elim#0` | Exodus 15–16 and Numbers 33:8 measure the three days from the passage of the Red Sea | `relative`, anchored on an event that is not the measured-from point | **CHANGES_REQUIRED_RELATIVE** — author the Red Sea crossing and re-anchor |
| `israel.conquest.war-against-the-kings-of-chanaan#0` | Josue 11:18 states the length of the warring itself — "Josue made war a long time against these kings" | that length sits in the `relative` payload with an anchor, so a query prints "a long time" beside "The crossing of the Jordan" | **CHANGES_REQUIRED_DURATION** in kind, but "a long time" is not a whole positive number and so cannot become `precision: duration` either; it is sequence-only and the claim must say so, as the adjacent `division-of-the-land` claim correctly does |

The two Madian claims stand. The ambiguity the prior lane flagged is in the
*subject* — one event id denoting both the flight and the shepherd years — and
each claim's temporal payload is what its source supports. A typed ambiguity the
source genuinely leaves open is the right answer, and here the corpus has it.

`israel.judges.period#0` is the worst of the six. Its own subject note records
that both figures the text carries are durations, and the claim is nonetheless
stored `relative` with an anchor — §10.0 and §15.1(6) verbatim, **surviving the
very 47-claim migration that was meant to catch exactly this.** A consumer
combining its published `label` ("As it were, after four hundred and fifty
years") with its anchor's date reads 570 B.C. for the period of the Judges. The
anchor is wrong twice over: it names the period's terminus rather than its
origin, and that terminus is itself dated from a modern-critical reconstruction.

## The "four dispositioned wrong anchors"

`PROJECT-WORK.md` records that "Four wrong anchors were also dispositioned rather
than changed; they are named in `.scratch/audit/durations.md` §3.1." Two problems
with the record, and then the substance.

**The record is one command from gone.** `.scratch/` is excluded in
`.git/info/exclude` and `wt tidy` deletes it without asking. The tracked
acceptance record for this question points at an untracked scratch file.

**§3.1 names fourteen, not four.** This lane re-derived every one against the
corpus at HEAD rather than trusting either number, and then put each result
through an independent pass briefed to refute it.

| Claim | Current production anchor | Result |
| --- | --- | --- |
| `israel.judges.jephte-three-hundred-years#0` | *(none — migrated to `duration`)* | **PASS** |
| `israel.monarchy.isboseth-reign#0` | *(none — migrated to `duration`)* | **PASS** |
| `israel.judges.ark-at-cariathiarim#0` | `israel.judges.ark-comes-to-cariathiarim` *(new event)* | **PASS** |
| `israel.exile.burning-of-the-temple#0` | `israel.exile.nabuchodonosor-accession` *(new event)* | **PASS** |
| `israel.exile.deportations-of-nabuchodonosor#0` | `israel.exile.nabuchodonosor-accession` | **PASS** |
| `israel.restoration.second-temple-completed` | *(none — retyped `month-day`/`year`)* | **PASS** |
| `apostolic-age.return-of-saint-john-from-patmos#0` | `apostolic-age.exile-of-saint-john-to-patmos` | **PASS** — refuted on verification: the anchor is dated "the reign of Domitian (81-96)", whose terminus *is* Domitian's death, the statement carries Eusebius's own words naming that death, and no magnitude exists to resolve wrongly |
| `israel.exodus.the-plagues-of-egypt#1` | `israel.exodus.the-exodus` | **PASS** on the anchor; a separate minor label defect stands |
| `israel.wilderness.encampment-at-sinai#0` | `israel.exodus.the-exodus` | **PASS** |
| `israel.restoration.nehemias-tidings-of-jerusalem#0` | `israel.restoration.walls-forbidden-by-artaxerxes` | **CHANGES_REQUIRED** — 2 Esdras 1:1's "twentieth year" is the twentieth of **Artaxerxes' reign**; the lane re-anchored onto a second wrong anchor |
| `israel.exodus.the-plagues-of-egypt#0` | `israel.exodus.moses-before-pharao` | **CHANGES_REQUIRED** — Exodus 7:25 measures from **the striking of the river**, which the corpus holds no event for |
| `israel.judges.period#0` | `israel.monarchy.saul-accession` | **CHANGES_REQUIRED** — the period's own terminus, itself dated from a modern-critical figure; and the claim should be a `duration` at all |
| `composition.psalm-73#0` | `israel.exile.third-captivity` | **CHANGES_REQUIRED** — carries the absolute "after 586 B.C." in a display string only |
| `composition.psalms-of-the-sons-of-korah#0` | `israel.restoration.decree-of-cyrus` | **CHANGES_REQUIRED** — names **two** bounds ("between the days of Isaias and the return"); the shape holds one, and the Isaias end is silently dropped |

So of §3.1's fourteen: **nine are genuinely fixed** — seven by the correction
lane and two more that this audit initially re-raised and verification cleared —
and **five still carry an anchor the evidence contradicts**, one of them a
re-anchoring onto a second wrong anchor.

Directions §11 case **A** therefore applies, on a smaller set than first
appeared. The phrase "wrong anchor" does not survive this report unresolved:
every one of the fourteen is named above with its result, and every surviving
defect has its correct measured-from point recorded in `cold-audit-findings.tsv`.

Beyond §3.1's list, the complete sweep of all 217 `relative` and `duration`
claims raised further anchor candidates; most were refuted. What survived is in
the findings table under `audit_class` `B-wrong-anchor`.


## Material findings

Critical and major findings in full; minor ones listed by line. The complete
table, with the full note on every row, is `cold-audit-findings.tsv`.

### A2-002 — **critical**

- **claim:** `event:israel.patriarchs.birth-of-abram#0`
- **class:** A-duration-relative — relative-offset-wrong-terminus
- **source locus:** Catholic Encyclopedia III (1908), "Biblical Chronology", section 4 'The flood to the birth of Abraham', closing row of the genealogical table and the sentence following it
- **stored:** precision relative; subject israel.patriarchs.birth-of-abram; anchor israel.primeval.deluge; "367 years from the flood, in the Hebrew"
- **source supports:** relative offset, but with a different terminus: the encyclopedia's own table labels this figure "Hence, number of years from Flood to Call of Abraham", reaching 367 only after the row "Add for age of Abraham at time of his call" adds 75. The Hebrew figure the source supports is Flood -> CALL of Abram, not Flood -> BIRTH of Abram.
- **evidence:** Years from birth of Sem / to birth of Abraham | Deduct years of Sem's / age at time of flood | Add for age of Abraham / at time of his call | Hence, number of years from Flood to Call of Abraham -- 392 / 100 / 292 / 75 / 367 (Hebrew), 1042 / 100 / 942 / 75 / 1017 (Samaritan), 1172 / 100 / 1072 / 75 / 1147 (Sept.) ... "Again, however, the numbers in the table above differ in the Hebrew, Samaritan , and Septuagint , being respectively 367, 1017, and 1147"
- **required correction:** Re-subject this claim to israel.patriarchs.call-of-abram (anchor israel.primeval.deluge unchanged), or, if it is to stay on the birth, replace the figure with the table's pre-addition subtotal (292 Hebrew / 942 Samaritan / 1072 Septuagint). As stored the corpus overstates the Flood-to-birth interval by exactly the seventy-five years of Genesis 12:4, and double-counts them against event:israel.patriarchs.call-of-abram#0, which already adds seventy-five years to the birth.

### A2-003 — **critical**

- **claim:** `event:israel.patriarchs.birth-of-abram#1`
- **class:** A-duration-relative — relative-offset-wrong-terminus
- **source locus:** Catholic Encyclopedia III (1908), "Biblical Chronology", section 4 'The flood to the birth of Abraham', closing row of the genealogical table and the sentence following it
- **stored:** precision relative; subject israel.patriarchs.birth-of-abram; anchor israel.primeval.deluge; "1017 years from the flood, in the Samaritan"
- **source supports:** relative offset, but with a different terminus: the encyclopedia's own table labels this figure "Hence, number of years from Flood to Call of Abraham", reaching 1017 only after the row "Add for age of Abraham at time of his call" adds 75. The Samaritan figure the source supports is Flood -> CALL of Abram, not Flood -> BIRTH of Abram.
- **evidence:** Years from birth of Sem / to birth of Abraham | Deduct years of Sem's / age at time of flood | Add for age of Abraham / at time of his call | Hence, number of years from Flood to Call of Abraham -- 392 / 100 / 292 / 75 / 367 (Hebrew), 1042 / 100 / 942 / 75 / 1017 (Samaritan), 1172 / 100 / 1072 / 75 / 1147 (Sept.) ... "Again, however, the numbers in the table above differ in the Hebrew, Samaritan , and Septuagint , being respectively 367, 1017, and 1147"
- **required correction:** Re-subject this claim to israel.patriarchs.call-of-abram (anchor israel.primeval.deluge unchanged), or, if it is to stay on the birth, replace the figure with the table's pre-addition subtotal (292 Hebrew / 942 Samaritan / 1072 Septuagint). As stored the corpus overstates the Flood-to-birth interval by exactly the seventy-five years of Genesis 12:4, and double-counts them against event:israel.patriarchs.call-of-abram#0, which already adds seventy-five years to the birth.

### A2-004 — **critical**

- **claim:** `event:israel.patriarchs.birth-of-abram#2`
- **class:** A-duration-relative — relative-offset-wrong-terminus
- **source locus:** Catholic Encyclopedia III (1908), "Biblical Chronology", section 4 'The flood to the birth of Abraham', closing row of the genealogical table and the sentence following it
- **stored:** precision relative; subject israel.patriarchs.birth-of-abram; anchor israel.primeval.deluge; "1147 years from the flood, in the Septuagint"
- **source supports:** relative offset, but with a different terminus: the encyclopedia's own table labels this figure "Hence, number of years from Flood to Call of Abraham", reaching 1147 only after the row "Add for age of Abraham at time of his call" adds 75. The Septuagint figure the source supports is Flood -> CALL of Abram, not Flood -> BIRTH of Abram.
- **evidence:** Years from birth of Sem / to birth of Abraham | Deduct years of Sem's / age at time of flood | Add for age of Abraham / at time of his call | Hence, number of years from Flood to Call of Abraham -- 392 / 100 / 292 / 75 / 367 (Hebrew), 1042 / 100 / 942 / 75 / 1017 (Samaritan), 1172 / 100 / 1072 / 75 / 1147 (Sept.) ... "Again, however, the numbers in the table above differ in the Hebrew, Samaritan , and Septuagint , being respectively 367, 1017, and 1147"
- **required correction:** Re-subject this claim to israel.patriarchs.call-of-abram (anchor israel.primeval.deluge unchanged), or, if it is to stay on the birth, replace the figure with the table's pre-addition subtotal (292 Hebrew / 942 Samaritan / 1072 Septuagint). As stored the corpus overstates the Flood-to-birth interval by exactly the seventy-five years of Genesis 12:4, and double-counts them against event:israel.patriarchs.call-of-abram#0, which already adds seventy-five years to the birth.

### E1-007 — **critical**

- **claim:** `event:israel.patriarchs.birth-of-abram#0`
- **class:** E — wrong-terminus-materially-false-interval
- **source locus:** "Biblical Chronology", section "The flood to the birth of Abraham", the genealogical table and the sentence following it
- **stored:** The birth of Abram is 367 years from the Flood in the Hebrew (precision relative, anchor israel.primeval.deluge, statement '367 years from the flood, in the Hebrew').
- **source supports:** 367 is the table's total from the Flood to the CALL of Abraham, reached by adding 75 (Abraham's age at his call) to 292. The Hebrew figure the table gives from the Flood to the BIRTH of Abraham is 292.
- **evidence:** Years from birth of Sem to birth of Abraham Deduct years of Sem's age at time of flood Add for age of Abraham at time of his call Hence, number of years from Flood to Call of Abraham 392 100 1042 100 1172 100 292 75 942 75 1072 75 367 1017 1147 Again, however, the numbers in the table above differ in the Hebrew, Samaritan , and Septuagint , being respectively 367, 1017, and 1147
- **required correction:** Withdraw 367 from israel.patriarchs.birth-of-abram, or re-subject it to israel.patriarchs.call-of-abram, which this corpus already holds. If a Flood-to-birth figure is wanted, the source's own Hebrew figure is 292 ('392 ... deduct 100'), authored as such with its own basis. The identical defect stands on the sibling claims #1 (1017) and #2 (1147), which are the same table row for the Samaritan and the Septuagint; they are outside this package and need the same correction.

### LEAD-009 — **critical**

- **claim:** `event:israel.patriarchs.birth-of-abram#0, #1, #2`
- **class:** A-relative-offset / wrong-terminus — relative-offset-attached-to-the-wrong-terminus
- **source locus:** Howlett, "Biblical Chronology", CE vol. 3 (1908), section 4 "The flood to the birth of Abraham", the genealogical table and its final row
- **stored:** Three relative claims on event israel.patriarchs.BIRTH-of-abram, anchored on israel.primeval.deluge, with statements "367 years from the flood, in the Hebrew", "1017 ... in the Samaritan", "1147 ... in the Septuagint".
- **source supports:** The article's own table computes those three figures to the CALL of Abraham, not to his birth. Its penultimate row is "Add for age of Abraham at time of his call: 75 / 75 / 75" and its final row is labelled "Hence, number of years from Flood to Call of Abraham: 367 / 1017 / 1147". The Flood-to-BIRTH figures are the row above: 292 / 942 / 1072.
- **evidence:** CE 03731a table, verbatim rows: "Years from birth of Sem to birth of Abraham 392 / 1042 / 1172"; "Deduct years of Sem's age at time of flood 100 / 100 / 100" [= 292 / 942 / 1072]; "Add for age of Abraham at time of his call 75 / 75 / 75"; "Hence, number of years from Flood to Call of Abraham 367 / 1017 / 1147". Narrative: "the numbers in the table above differ in the Hebrew, Samaritan, and Septuagint, being respectively 367, 1017, and 1147".
- **required correction:** Move all three claims to israel.patriarchs.call-of-abram (the anchor israel.primeval.deluge is correct), or keep them on the birth and replace the figures with the table's own Flood-to-birth row, 292 / 942 / 1072. Then correct the note on #0: the source does NOT leave the terminus ambiguous — only its section heading says "birth"; the table that yields the numbers says "Call". Also re-check that nothing downstream now double-counts, since the corpus already holds call-of-abram at +75 years from birth-of-abram on Genesis 12:4.

### A2-026 — **major**

- **claim:** `event:israel.judges.period#0`
- **class:** A-duration-relative — ambiguous-temporal-semantics
- **source locus:** Acts.13.20 (in context Acts.13.17-21)
- **stored:** precision relative; subject israel.judges.period; anchor israel.monarchy.saul-accession; statement "he gave unto them judges, until Samuel the prophet, as it were, after four hundred and fifty years"; label "As it were, after four hundred and fifty years"
- **source supports:** The tracked Douay text will not settle relative against duration, and settles neither on Saul. Its punctuation attaches the four hundred and fifty years to what precedes - the choosing of the fathers, the sojourn in Egypt, the forty years in the desert and the division of Chanaan (Acts 13:17-19) - and then begins the judges afterwards: 'And after these things, he gave unto them judges'. On that reading the figure is a span ENDING before the judges begin, and the verse gives the judges no length and no offset from anything. Saul is not introduced until the next verse and nothing is measured from his accession on any reading.
- **evidence:** Acts.13.17 The God of the people of Israel chose our fathers and exalted the people when they were sojourners in the land of Egypt: And with an high arm brought them out from thence: / Acts.13.18 And for the space of forty years endured their manners in the desert: / Acts.13.19 And, destroying seven nations in the land of Chanaan, divided their land among them by lot. / Acts.13.20 As it were, after four hundred and fifty years. And after these things, he gave unto them judges, until Samuel the prophet. / Acts.13.21 And after that they desired a king: and God gave them Saul the son of Cis, a man of the tribe of Benjamin, forty years.
- **required correction:** Do not remove the claim. The label "As it were, after four hundred and fifty years" is verbatim, hedged and correctly typed retrospective-event, and 15.4 forbids resolving an ambiguity the source left. Remove relative.of (see A2-029) and either re-state relative.statement in the Douay's own order or reduce it to the verbatim clause, so the machine string stops asserting the punctuation the claim's own note disclaims.

### A2-029 — **major**

- **claim:** `event:israel.judges.period#0`
- **class:** B-wrong-anchor — wrong-relative-anchor
- **source locus:** Acts.13.20 (in context Acts.13.17-21)
- **stored:** relative.of = israel.monarchy.saul-accession
- **source supports:** Nothing in Acts 13:20 is measured from Saul's accession. On the tracked Douay punctuation the four hundred and fifty years run from God's choosing of the fathers and the sojourn in Egypt (Acts 13:17) to the division of Chanaan by lot (Acts 13:19), and the judges follow 'after these things'. If the figure is to keep an anchor at all, the correct one is the beginning of that span - the sojourn in Egypt, israel.egypt.sojourn, or the Exodus, israel.exodus.the-exodus, at its far end - and the judges stand at the END of it, never four hundred and fifty years after the monarchy Saul founded.
- **evidence:** Acts.13.19 And, destroying seven nations in the land of Chanaan, divided their land among them by lot. / Acts.13.20 As it were, after four hundred and fifty years. And after these things, he gave unto them judges, until Samuel the prophet. / Acts.13.21 And after that they desired a king: and God gave them Saul the son of Cis, a man of the tribe of Benjamin, forty years.
- **required correction:** Remove the anchor israel.monarchy.saul-accession. Saul enters the discourse only at Acts 13:21 and is the terminus of the judges, not their origin; anchoring on him inverts the whole sequence. See A2-026 for the recommended disposition of the claim as a whole.

### A3-006 — **major**

- **claim:** `event:israel.monarchy.absalom-revolt#0`
- **class:** B-wrong-anchor — wrong-relative-anchor
- **source locus:** 2 Kings (2 Samuel) 15:7; Haydock commentary on 2 Kings 15, PDF page 430 / printed p. 400
- **stored:** precision relative; relative.of = israel.monarchy.david-reign; statement 'after forty years'; label 'And after forty years'
- **source supports:** RELATIVE OFFSET OF FORTY YEARS WITH NO ORIGIN STATED IN THE VERSE. The Douay text says only 'And after forty years' and names nothing to count from. The only inspected source that supplies an origin, the Haydock commentary the claim's own note invokes, gives two candidate origins and NEITHER is the start of David's reign: Vatable counts from the people's petition for a king, Salien from David's first anointing; the same note reports that the number is probably a corruption of 'four'.
- **evidence:** 2Kings.15.7 (tracked Douay) 'And after forty years, Absalom said to king David: Let me go, and pay my vows which I have vowed to the Lord in Hebron.' Haydock, note on Ver. 7: 'Forty, which Vatable dates from the time when the people petitioned for a king; Salien, from the first anointing of David. M.--It is probable enough that this number has been substituted instead of four, which Josephus, Theodoret, Syr. Arab. and many Latin MSS. read'. Haydock, note on Ver. 1: 'Absalom's ambition could not wait patiently for the death of his father, who was not yet sixty [years] old, and had been first anointed forty years before, v. 7.' Salien.
- **required correction:** Sound as to the anchor. The last sentence overstates: the claim's note already carries the manuscript problem ("treats 'after forty years' as a manuscript problem and cites Salien and Usher on it. The number must not be presented as settled"); naming 'four' explicitly is an improvement, not a required correction.

### A3-027 — **major**

- **claim:** `event:israel.restoration.nehemias-tidings-of-jerusalem#0`
- **class:** B-wrong-anchor — wrong-relative-anchor
- **source locus:** 2 Esdras (Nehemias) 1:1; Van Hoonacker, 'Book of Nehemiah', Catholic Encyclopedia vol. 10 (New York, 1911)
- **stored:** precision relative; relative.of = israel.restoration.walls-forbidden-by-artaxerxes; statement 'in the month of Casleu, in the twentieth year'
- **source supports:** RELATIVE OFFSET MEASURED FROM THE KING'S ACCESSION. 'The twentieth year' is a regnal year of Artaxerxes: Scripture says 'in the twentieth year' and Van Hoonacker glosses it 'in the twentieth year of the king'. Neither source measures anything from the forcible stopping of the work; Van Hoonacker in fact narrates the stopping of the work as an earlier event and separately supplies the king's own dates (Artaxerxes I, B.C. 465-24) and the resulting year, B.C. 445.
- **evidence:** 2Esd.1.1 'The words of Nehemias the son of Helchias. And it came to pass in the month of Casleu, in the twentieth year, as I was in the castle of Susa,' Van Hoonacker: 'Nehemiah, the son of Helchias, relates how, at the court of Artaxerxes at Susa where he fulfilled the office of the king's cup-bearer, he received the news of this calamity in the twentieth year of the king (Nehemiah 1)'. Same article: 'especially during the first half of the reign of Artaxerxes I (B. C. 465-24)' and 'the first mission of Nehemiah fell in the year B.C. 445. The Aramaic papyri of Elephantine, recently published by Sachau, put this date beyond the shadow of a do
- **required correction:** Re-anchor on the origin the sources actually count from. Author israel.restoration.artaxerxes-accession (Van Hoonacker's own 'Artaxerxes I (B. C. 465-24)' is a retained, ranked statement of it) and set relative.of to it, so that 'the twentieth year' is measured from the first year of the king. Failing that, remove the regnal year from relative.statement/date_str and carry it in the label only, expressing the relation to the calamity as the sequence it is -- but do not leave a numbered regnal offset anchored on an event that is not its origin.

### A4-004 — **major**

- **claim:** `event:israel.exodus.the-plagues-of-egypt#0`
- **class:** B-wrong-anchor — wrong-relative-anchor
- **source locus:** Exodus 7:25; Exodus 9:31-32
- **stored:** precision 'relative', anchor israel.exodus.moses-before-pharao ("Moses' first approach to Pharao", Exodus 5), statement/label "And seven days were fully ended, after that the Lord struck the river"
- **source supports:** SOURCE CLASS: contained duration/span. Exodus 7:25 measures seven days FROM the striking of the river, i.e. from the first plague at Exodus 7:20-21, not from Moses' first approach to Pharao. The seven days are an interval INSIDE the series, not an offset of the series from the audience of Exodus 5.
- **evidence:** And seven days were fully ended, after that the Lord struck the river. [Ex.7.25] / The flax therefore, and the barley were hurt, because the barley was green, and the flax was now bolled; But the wheat, and other winter corn were not hurt, because they were lateward. [Ex.9.31-32] / [Ex.7.20-21 context: the striking of the river is the first plague, which follows the audience of Ex 5 and the rod-serpent sign of Ex 7:8-13]
- **required correction:** Correct anchor is the striking of the river (the first plague, Ex 7:20-21), which this corpus holds no event for. Either author that event and anchor the seven days on it, or keep israel.exodus.moses-before-pharao as a bare sequence anchor and move the seven days out of the statement/label into a contained interval, so that anchor + "seven days" cannot be read as 'seven days after Moses' first approach to Pharao'.

### A4-006 — **major**

- **claim:** `event:israel.wilderness.mara-and-elim#0`
- **class:** B-wrong-anchor — wrong-relative-anchor
- **source locus:** Exodus 15:22; Numbers 33:8 (context Num 33:3-8)
- **stored:** precision 'relative', anchor israel.exodus.the-exodus ("The Exodus from Egypt"), statement "they marched three days through the wilderness, and found no water", label "three days through the wilderness"
- **source supports:** SOURCE CLASS: relative offset, but measured FROM THE RED SEA. Exodus 15:22 counts the three days from the bringing of Israel from the Red Sea; Numbers 33:8 counts them from the passage through the midst of the sea. Neither counts them from the departure out of Egypt.
- **evidence:** And Moses brought Israel from the Red Sea, and they went forth into the wilderness of Sur: and they marched three days through the wilderness, and found no water. [Ex.15.22] / And departing from Phihahiroth, they passed through the midst of the sea into the wilderness: and having marched three days through the desert of Etham, they camped in Mara. [Num.33.8] / Now the children of Israel departed from Ramesses ... And they camped in Soccoth. And from Soccoth they came into Etham ... Departing from thence they came over against Phihahiroth [Num.33.3-7]
- **required correction:** Correct anchor is the passage of the Red Sea (Exodus 14; Numbers 33:8), which this corpus holds no event for. Author that event and anchor the three days on it; do not leave israel.exodus.the-exodus carrying a three-day count, because Numbers 33:3-7 puts Soccoth, Etham and Phihahiroth between the departure and the sea.

### A4-017 — **major**

- **claim:** `event:israel.exile.ezechiel.death-of-the-prophets-wife#0`
- **class:** A-duration-relative — containment-encoded-as-relative-anchor
- **source locus:** Ezechiel 24:15-18; Catholic Encyclopedia, "Ezekiel"
- **stored:** precision 'relative', anchor israel.exile.ezechiel.ministry ("The prophetic ministry of Ezechiel among the exiles by the river Chobar"), statement/label "So I spoke to the people in the morning, and my wife died in the evening"
- **source supports:** SOURCE CLASS: sequence only, within a single unnamed day. Ezechiel 24:15 opens with the book's undated revelation formula and Ezechiel 24:18 states only a morning-to-evening order; Scripture gives the episode no year, month or day and no measured distance from anything.
- **evidence:** And the word of the Lord came to me, saying: [Ezech.24.15] / Son of man, behold I take from thee the desire of thy eyes with a stroke, and thou shalt not lament, nor weep; neither shall thy tears run down. [Ezech.24.16] / Sigh in silence, make no mourning for the dead [Ezech.24.17] / So I spoke to the people in the morning, and my wife died in the evening: and I did in the morning as he had commanded me. [Ezech.24.18]
- **required correction:** Drop relative.of; keep the containment where it already is (parent: israel.exile.ezechiel.ministry) and carry the morning-to-evening sequence in the note, with typed silence and a gap row for the unplaced position, per §10.0 "Containment is not offset." The refusal to borrow the Ezech 24:1 dateline is correct and stands.

### A6-021 — **major**

- **claim:** `event:israel.conquest.war-against-the-kings-of-chanaan#0`
- **class:** A-duration-relative — duration-encoded-as-offset
- **source locus:** Jos.11.18 (with Jos.11.23)
- **stored:** precision relative; anchor israel.conquest.crossing-of-the-jordan; statement "Josue made war a long time against these kings"; label "a long time"
- **source supports:** Duration, unquantified: Josue waged war a long TIME - a length of the warring itself, not an interval from the crossing of the Jordan. The Vulgate is unambiguous: "Multo tempore pugnavit Josue contra reges istos." Nothing in the chapter measures the war from the passage of the Jordan.
- **evidence:** Jos.11.18: Josue made war a long time against these kings. || clementine-vulgate Jos.11.18: Multo tempore pugnavit Josue contra reges istos. || Jos.11.23: So Josue took all the land ... And the land rested from wars.
- **required correction:** Stop carrying the war's own length as the offset payload. Because "a long time" is not a whole positive number it cannot become precision duration either, so keep precision relative on the crossing ONLY as a sequence statement (the war follows the passage of the Jordan) and move "Josue made war a long time against these kings" into basis/note as the unquantified length it is - or type the length as silence with a gap row. Either way label must not read "a long time" beside an anchor.

### A8-007 — **major**

- **claim:** `event:israel.wilderness.mary-stricken-at-haseroth#0`
- **class:** B-wrong-anchor — anchor-not-at-interval-start
- **source locus:** Catholic Encyclopedia vol. 1, "Aaron"
- **stored:** precision=relative; anchor=israel.wilderness.encampment-at-sinai; statement "A few months later, when the Hebrews reached Haseroth, the second station after Mount Sinai"; label "A few months later".
- **source supports:** relative offset of a few months measured from the Levitical legislation at Sinai (the sentences the article's "later" follows), reaching an episode that Scripture places AFTER the departure from Sinai. The anchor named is a roughly eleven-month SPAN, and the offset does not run from that span's start.
- **evidence:** CE "Aaron": "A few months later, when the Hebrews reached Haseroth, the second station after Mount Sinai, Aaron fell into a new fault." | Num.33.16-17: "But departing also from the desert of Sinai, they came to the graves of lust. And departing from the graves of lust, they camped in Haseroth." | Num.10.11: "The second year, in the second month, the twentieth day of the month, the cloud was taken up from the tabernacle of the covenant."
- **required correction:** Re-anchor on israel.wilderness.departure-from-sinai, which the article's own "the second station after Mount Sinai" counts from and which the corpus already holds at Num.10.11; if the encampment is kept, the relative statement must say the offset runs from its end. Quotation, hedge and note are otherwise correct.

### B-043 — **major**

- **claim:** `binding:prophecy-given:israel.divided-kingdom.fall-of-samaria@Mich.4,Mich.5`
- **class:** B-binding-scope — composition-evidence-used-for-prophecy-given
- **source locus:** Catholic Encyclopedia vol. 10, "Book of Micheas"
- **stored:** prophecy-given over Micheas 4-5 pointing at the fall of Samaria, so a query at Mich 4:1 answers prophecy-given 'B.C. 721', 'was not taken till 722 B.C.', 'The fall of Samaria in 722 or 721' and 'B.C. 722-1'.
- **source supports:** The article makes a COMPOSITION statement about chapters 4-5, hedged twice, and places them SHORTLY AFTER the fall, not at it.
- **evidence:** The difference of tone and contents clearly show that 4-5 must have been composed in other circumstances than 1-3. They probably date from shortly after the fall of Samaria in 722 B.C.
- **required correction:** CHANGES_REQUIRED_RELATION

### C-002 — **major**

- **claim:** `binding:historical-setting Dan -> israel.exile.first-captivity`
- **class:** C — over-broad scope
- **source locus:** CE 'Daniel', biography section
- **stored:** historical-setting over the WHOLE BOOK of Daniel to israel.exile.first-captivity (the deportation in the third/fourth year of Joakim).
- **source supports:** CE places DANIEL THE MAN's deportation at that date and traces his career onward to Cyrus; it does not assert that the whole book's historical occasion is that single deportation.
- **evidence:** CE 'Daniel': "When still a youth, probably about fourteen years of age, he was carried captive to Babylon by Nabuchodonosor in the fourth year of the reign of Joakim (605 B.C. )." and, of the same prophet's later life, "The incident which brought him to public notice again was the scene of revelry in Baltasar's palace, on the eve of Cyrus's conquest of Babylon (538 B.C. )." | Dan.10.1 (tracked Douay): "In the third year of Cyrus, king of the Persians, a word was revealed to Daniel, surnamed Baltassar" | Dan.7.1: "In the first year of Baltasar, king of Babylon" | Dan.9.1: "In the first year of Darius, the son of Assuerus"
- **required correction:** Restrict the historical-setting scope to Dan.1, or rebind the whole book to a period event (israel.exile.seventy-years). The regnal note and both CE quotations are accurate; only the extent is unsupported.

### C-009 — **major**

- **claim:** `binding:historical-setting Ps.30 -> israel.monarchy.david-in-the-desert-of-maon`
- **class:** C — suppressed sourced alternative; one of several mutually exclusive readings asserted as preferred
- **source locus:** Haydock Ps 30:1, artifact p. 742 (visible printed p. 706)
- **stored:** historical-setting on Ps 30 to David in the desert of Maon, `preferred`, single-valued. A consumer querying Ps.30.1 receives exactly one line: "historical-setting A. M. 2945, A. C. 1059 preferred inherited israel.monarchy.david-in-the-desert-of-maon".
- **source supports:** The cited page preserves FIVE mutually exclusive settings for this psalm and settles none of them. It gives no ground for preferring Maon over the rest.
- **evidence:** Haydock, Ps 30:1 note, artifact p. 742: "David composed it when he was obliged to flee from court, (1 K. xix. 1. and xxvii. 1. C.) or in the desert of Maon, seeing himself in the most imminent danger; (1 K. xxiii. 25. Kimchi. Du Pin) though some refer this psalm to the conspiracy of Absalom, (Theod. M.) or to the unpremeditated fall of David, (Euseb,) or to the captives. S. Chrys." | Ps.30.1 (tracked Douay): "Unto the end, a psalm for David, in an ecstasy." | events.yaml: "- id: israel.monarchy.david-flight-from-absalom ... date: precision: relative ... label: \"when he fled from the face of his son Absalom\""
- **required correction:** Author the Absalom reading as a second historical-setting binding on Ps.30 to israel.monarchy.david-flight-from-absalom (§4.4: preserve the disagreement; §15.1(5): add, do not harmonize), or, if the corpus will not carry alternatives on a binding, withdraw the Maon binding and leave Ps 30 with typed silence. The note's stated ground for excluding Absalom - that the page "does not say which of the two markers standing inside 2 Kings 15 is meant" - does not survive checking: a binding carries no date at all (§6), the corpus already holds `israel.monarchy.david-flight-from-absalom` as a single event, that event's own claim is RELATIVE ("when he fled from the face of his son Absalom") and carries no marker to choose between, and the corpus binds two other psalms (Ps 3/142 and Ps 62/70) to it on exactly this kind of evidence. The real selection criterion was 'which alternative happens to have an event already', which is corpus convenience, not source authority.

### D-003 — **major**

- **claim:** `unit:composition.book-of-ecclesiasticus.greek#0`
- **class:** D — native universe enumerated densely rather than from the text; 35 Greek verse numbers the witness does not print are counted as additional Scripture and reported as composition-only under this unit; two contradictory figures for one fact
- **source locus:** scripts/_chronology.py:1792 _system_loci; guidance/scripture-chronology.md sections 3.0.1 and 9.3
- **stored:** coverage native_systems.greek: printed_loci 2194, additional_loci 1391, by_status {composition-only: 1390, textually-distinct: 1}; guidance section 3.0.1 'the Greek Ecclesiasticus: 1 391 of its loci refuse the Vulgate'; section 9.3 'the corrected universe is 35 809 + 1 391 (greek) + 9 (world-english-catholic) + 0 (hebrew) = 37 209'
- **source supports:** The tracked Greek witness prints 1356 Ecclus loci, of which 1355 refuse the Vulgate. The correct native universe is 35 809 + 1 356 (greek) + 6 (world-english-catholic) + 0 (hebrew) = 37 171.
- **evidence:** _deuterocanon._printed('greek')[('Ecclus',1,5)] is None and [('Ecclus',1,7)] is None, while _chronology._system_loci('greek') yields ('Ecclus',1,5) and ('Ecclus',1,7). The RV Apocrypha prints Sirach 1:4 'Wisdom hath been created before all things, And the understanding of prudence from everlasting.' and then 1:6 'To whom hath the root of wisdom been revealed? And who hath known her shrewd counsels?'
- **required correction:** The corpus already contradicts itself on this fact and the finding's side is the sourced one: src/sources/chronology/composition.yaml:1409 says "The concordance refuses 1 355 of the Greek book's 1 356 loci" while guidance §3.0.1 says "1 391 of its loci refuse the Vulgate" and §9.3 totals 37 209.

### E1-008 — **major**

- **claim:** `event:israel.exodus.the-exodus#0`
- **class:** E — traditional-figure-denied-preferred
- **source locus:** "Biblical Chronology", section "Birth of Abraham to the Exodus"
- **stored:** The Exodus in 1490 B.C., the traditional computation; disposition DISPUTED, so it is not displayed first.
- **source supports:** The article computes 1490 B.C. in its own voice from 3 Kings 6:1 and Ussher's regnal years, and later sets it aside for a modern figure it names as not traditional.
- **evidence:** For ( 1 Kings 6:1 ) the fourth year of King Solomon is said to have fallen in the 480th year after the Exodus; and Ussher dates the reign of King Solomon from 1014-975 B.C. But as the Temple was begun in the fourth year of that king, or in 1010, the Exodus took place in the year 1490 B.C. How do these results square with the teaching of science ?
- **required correction:** Prefer the traditional reckoning on this subject under the explicit-note clause of §4.4; profiles.yaml's own non-authority rule ('not used to adjust a traditional date') and §17's 'not a place to smuggle one in' are both violated by letting the modern figure's `disputed` disposition strip it. The note's 'reached independently of it' is separately unsupported: this corpus's burning-bush (#0 on israel.exodus.burning-bush) and moses-before-pharao claims both state the Haydock 'A. C. 1491' apparatus is an Usher-attributed reckoning, and the encyclopedia's 1490 is built on Ussher's regnal years.

### E1-009 — **major**

- **claim:** `event:israel.exodus.the-exodus#1`
- **class:** E — modern-critical-chronology-inside-traditional-profile
- **source locus:** "Biblical Chronology", section "The Exodus to the building of Solomon's Temple"
- **stored:** The Exodus about 1277 B.C., authored under profile catholic-traditional-v1 with disposition disputed.
- **source supports:** Howlett concludes for about 1277 on Egyptological grounds (Sayce, Driver, the Tel-el-amarna tablets, Meneptah) and says in terms that it is not the traditional date.
- **evidence:** Hence we are driven to his immediate successor, Meneptah, at earliest, and to about the year 1277 (Early History of the Hebrews, 150) for the date of the Exodus. ... We conclude, therefore, that the date of the Exodus was about 1277, the monarchy was founded by Saul, 1020; David mounted the throne, 1002; Solomon in 962, and the Temple was begun, 958 B.C. ... This is not the traditional date of the Exodus, but as Father Hummelauer (Genesis, p. 29) says, it is the conclusion of most men in these days.
- **required correction:** Move it to a modern profile with its own id (§4.1), or re-dispose it `alternate` beneath a preferred traditional claim. It may not stay `disputed`. The Ussher carve-out in profiles.yaml ('may be reported where a ranked Catholic source itself reports it') is written only for Protestant chronologies; the modern-critical entry has no such clause and says flatly 'Not consulted, not used to adjust a traditional date.'

### E1-010 — **major**

- **claim:** `event:israel.exodus.the-exodus#2`
- **class:** E — rank-1-scripture-disposed-below-rank-6
- **source locus:** 3Kings.6.1, tracked Douay-Rheims
- **stored:** The Exodus 480 years before the beginning of the Temple (precision relative, anchor israel.monarchy.temple-begun); disposition DISPUTED.
- **source supports:** The tracked Douay text states the interval exactly as quoted; nothing in a higher-ranked source contradicts it.
- **evidence:** And it came to pass in the four hundred and eightieth year after the children of Israel came out of the land of Egypt, in the fourth year of the reign of Solomon over Israel, in the month Zio, (the same is the second month) he began to build a house to the Lord.
- **required correction:** Prefer this claim on israel.exodus.the-exodus and demote the 440 to `alternate` with its provenance, as the same variant is already handled by a note on temple-begun ('This corpus prints the Douay number and picks neither'). The inconsistency is the corpus's own: the same variant was authored as a claim on one subject and as a note on the other, and only that choice flips the disposition.

### E1-016 — **major**

- **claim:** `event:israel.monarchy.saul-accession#0`
- **class:** E — modern-critical-figure-is-the-profile-s-only-answer
- **source locus:** "Biblical Chronology", section "The Exodus to the building of Solomon's Temple", closing sentence
- **stored:** The monarchy founded under Saul in 1020 B.C.; disposition ALTERNATE, and the only claim on the subject, so the profile displays nothing first and returns this figure alone.
- **source supports:** Howlett concludes for 1020 in his own voice, as part of the same Egyptological reconstruction that yields his 1277 for the Exodus.
- **evidence:** We conclude, therefore, that the date of the Exodus was about 1277, the monarchy was founded by Saul, 1020; David mounted the throne, 1002; Solomon in 962, and the Temple was begun, 958 B.C. ... We have fixed roughly the date of the revolt of the Ten Tribes for the year 936 B.C. But the traditional date is 975
- **required correction:** Remove the figure from catholic-traditional-v1 (§4.1: a modern chronology is a separate profile with its own id) and, if no ranked traditional source dates Saul's accession, author a gaps.yaml row naming the sources inspected so the subject reaches undated-in-tradition. `tools/tpt scripture-chronology query 1Kings.11.15` currently returns 'the monarchy was founded by Saul, 1020\talternate' as the only date, so the subject note's 'this profile does not display it first' describes an intention the mechanism does not carry out — a lone `alternate` names nothing it is alternate to.

### E1-018 — **major**

- **claim:** `event:israel.monarchy.absalom-revolt#0`
- **class:** E — unsourced-relative-anchor
- **source locus:** 2Kings.15.7, tracked Douay-Rheims; Haydock note at 'Ver. 7. Forty', artifact PDF page 430
- **stored:** Absalom's move to Hebron 'after forty years', precision relative, ANCHOR israel.monarchy.david-reign; disposition PREFERRED.
- **source supports:** The verse states 'And after forty years' and names no terminus a quo. The only ranked commentary inspected for this corpus gives two rival termini, neither of them the beginning of David's reign, and reports that the number may be a corruption of 'four'.
- **evidence:** And after forty years, Absalom said to king David: Let me go, and pay my vows which I have vowed to the Lord in Hebron. [Douay-Rheims 2Kings.15.7] ... Vur. 7. Forty, which Vatable dates from the time when the people petitioned for a king; Salien, from the first anointing of David. M.--It is probable enough that this number has been substituted instead of four, which Josephus, Theodoret, [...] to be altered by some correcting hand, from four to forty. Kennicott. [Haydock, artifact PDF page 430]
- **required correction:** Drop israel.monarchy.david-reign as the anchor. Either record the interval without an anchor and say in the note that Scripture states no terminus a quo, or anchor it on a terminus a ranked source actually supplies and name that source - Haydock at 2 Kings 15:7 offers Vatable's 'the time when the people petitioned for a king' and Salien's 'the first anointing of David'. Add to the note that the same commentary reports the reading 'four' for 'forty'.

### E2-007 — **major**

- **claim:** `event:israel.exile.second-captivity#0`
- **class:** E — lower-rank-preferred-while-rank-1-speaks
- **source locus:** Ps.70.1, commentary note, artifact PDF page 776 (printed p. 740), lines 40-41
- **stored:** A.M. 3405, disposition **preferred**, i.e. the profile's displayed-first date for the second captivity of Juda, taken from Usher's chronology as printed by the Haydock edition (rank 3). The only other claim on the subject, 597 B.C. from the CE (rank 6), is `alternate`.
- **source supports:** The page supports the figure: Usher's chronology, printed in a rank-3 Catholic edition, gives the second captivity under Jechonias as A.M. 3405. It does not support that figure occupying the preferred slot, because rank 1 is not silent on this event: the tracked Douay at 4 Kings 24:12 dates it regnally, and the subject's own note quotes that verse.
- **evidence:** This first captivity happened under Joakim, A.M: 3398, the second, under Jechonias, 8405, and the last, when the city was destroyed and Sedecias was taken, 3416 Usher. | 4 Kings 24:12 (tracked Douay): "And Joachin, king of Juda, went out to the king of Babylon, he, and his mother, and his servants, and his nobles, and his eunuchs: and the king of Babylon received him in the eighth year of his reign."
- **required correction:** Demote the A.M. 3405 claim to `alternate` and author the rank-1 regnal claim from 4 Kings 24:8 and 24:12 as `preferred`, exactly as `israel.exile.first-captivity` already does with Dan 1:1. (Sec. 4.4 forbids leaving every claim on a subject without a disposition, so the demotion and the rank-1 claim must land together.) Separately, correct the basis quotation: it prints "the second under Jechonias as A.M. 3405", which is the repository's context prose; the page reads "the second, under Jechonias, 3405".

### E3-009 — **major**

- **claim:** `unit:composition.book-of-abdias#0`
- **class:** E — reported-third-party-opinion-stored-as-the-profile's-preferred-claim (§15.1(3), §4.4)
- **source locus:** Gigot, "Abdias", section "Date of the prophecy of Abdias"
- **stored:** Abdias composed 900-801 B.C. (interval), disposition PREFERRED under catholic-traditional-v1, label "about the reign of Joram (ninth century B.C.)"; a consumer query on Abd.1.1 returns "about the reign of Joram (ninth century B.C.) preferred".
- **source supports:** The article asserts only that scholars do not agree, that a named group of writers (Keil, Orelli, Vigouroux, Trochon, Lesetre) assigns the book to about the reign of Joram, and that on THEIR argument "it is inferred" that it originated about the middle of the ninth century. It closes by listing three leading opinions and declining to choose among them.
- **evidence:** Besides the shortness of the book of Abdias and its lack of a detailed title such as is usually prefixed to the prophetical writings of the Old Testament , there are various reasons, literary and exegetical , which prevents scholars from agreeing upon the date of its composition. Many among them (Keil, Orelli, Vigouroux, Trochon, Lesêtre, etc.) assign its composition to about the reign of Joram (ninth century B.C.). ... But such reference to this latter capture of the Jewish capital is ruled out, we are told, by the fact that ... Hence it is inferred that the prophecy of Abdias originated between the reign of Joram and the time of Joel and Am
- **required correction:** Change the disposition to disputed (solo-disputed is an established pattern in this corpus — life-of-christ.baptism, .public-ministry-begins, .last-supper and israel.monarchy.birth-of-david all carry a single disputed claim), or withdraw the unit and record typed silence as was done for both books of Esdras. Keep the year band and the label; do not author the Babylonian-Captivity or later opinions, which the source prints with no year.

### E3-010 — **major**

- **claim:** `unit:composition.book-of-jonas#0`
- **class:** E — lifetime-of-the-prophet-promoted-to-a-composition-date; no composition date exists in the source (§15.1(7), §15.1(3), §4.4)
- **source locus:** Driscoll, "Jonah", closing paragraph on authorship
- **stored:** Jonas composed 800-701 B.C. (interval), disposition PREFERRED, label "the eighth century B.C."; a consumer query on Jon.1.1 returns "the eighth century B.C. preferred" as the composition date of the book.
- **source supports:** The article states NO date for the writing of the book. Its only eighth-century figure is a hedged parenthesis about the PROPHET'S LIFETIME ("who is supposed to have lived in the eighth century B.C."), and it stands inside a sentence whose main clause denies that the book claims Jonah as its writer. The article's only other dated statement is about the narrated events: the reign of Asurdanil or Asurnirar, 770-745 B.C.
- **evidence:** Jewish tradition assumed that the Prophet Jonah was the author of the book bearing his name, and the same has been generally maintained by the Christian writers who defend the historical character of the narrative. But it may be remarked that nowhere does the book itself claim to have been written by the Prophet (who is supposed to have lived in the eighth century B.C.), and most modern scholars, for various reasons, assign the date of the composition to a much later epoch, probably the fifth century B.C.
- **required correction:** Withdraw unit:composition.book-of-jonas#0 and record typed silence for the composition of Jonas (the source gives no date of writing), exactly as was done for both books of Esdras under §15.1(3). If any claim is retained from this article it must be re-typed as what the source actually says — the prophet's supposed lifetime, or the narrated-event statement "the reign of either Asurdanil or Asurnirar (770-745 B.C.)" — and never carried as `composition` and never `preferred`. Any route from "Jewish tradition assumed that the Prophet Jonah was the author" to a date of writing is an authorship-to-occasion inference the same sentence refuses, and would at most be a §10 `derivation` with its own rule and inputs. Do not substitute the article's "probably the fifth century B.C.", which is in "most modern scholars" voice and is excluded by §4.3.

### LEAD-010 — **major**

- **claim:** `event:apostolic-age.return-of-saint-john-from-patmos#0; event:israel.judges.period#0; unit:composition.psalm-73#0; unit:composition.psalms-of-the-sons-of-korah#0; event:israel.exodus.the-plagues-of-egypt#1; event:israel.wilderness.encampment-at-sinai#0`
- **class:** B-wrong-anchor-dispositions — known-wrong-anchor-left-in-production; acceptance-evidence-in-an-untracked-file
- **source locus:** see the per-claim rows raised by the class-A auditors
- **stored:** PROJECT-WORK.md records "7 anchors corrected" and "Four wrong anchors were also dispositioned rather than changed; they are named in `.scratch/audit/durations.md` §3.1."
- **source supports:** §3.1 names FOURTEEN wrong anchors, not four. Seven were genuinely corrected in production (jephte-three-hundred-years and isboseth-reign migrated to duration with the anchor removed; ark-at-cariathiarim, burning-of-the-temple and deportations-of-nabuchodonosor re-anchored on two newly authored anchor events; second-temple-completed de-anchored; the-plagues-of-egypt#0 re-anchored and re-stated). SIX still carry in production the anchor §3.1 itself shows is wrong, and at least one of the seven "corrections" landed on a second wrong anchor.
- **evidence:** PROJECT-WORK.md: "Four wrong anchors were also dispositioned rather than changed; they are named in `.scratch/audit/durations.md` §3.1." — §3.1 opens: "Fourteen claims whose `of:` does not name the thing the number is measured from, or names nothing measurable at all."
- **required correction:** Disposition each of the six by name and act on it, per the corrections the class-A rows carry. Then move the four/fourteen anchor dispositions out of `.scratch/audit/durations.md` into tracked evidence: `.scratch/` is excluded in `.git/info/exclude` and `wt tidy` deletes it without asking, so the record PROJECT-WORK.md points at for this acceptance question is one command from gone. Also correct "Four wrong anchors" to the true count.

### LEAD-011 — **major**

- **claim:** `scripts/_chronology.py::_system_loci; guidance/scripture-chronology.md §3.0.1 and §9.3; coverage --json native_systems`
- **class:** coverage-universe — native-universe-enumerated-densely-rather-than-from-the-text; two-figures-for-one-fact
- **source locus:** scripts/_chronology.py:1792-1823
- **stored:** Coverage reports greek additional_loci = 1391 and world-english-catholic additional_loci = 9, giving a corrected declared universe of 35809 + 1391 + 9 + 0 = 37209. guidance §3.0.1 states "1 391 of its loci refuse the Vulgate"; §9.3 states the corrected universe is 37 209; PROJECT-WORK.md repeats both.
- **source supports:** _system_loci builds each chapter as range(low, high+1) from _deuterocanon._extents, which holds only the FIRST and LAST verse number the witness prints. Every verse number the witness skips is invented back. Measured against _deuterocanon._printed: greek prints 2156 loci but is enumerated as 2194 (38 invented — Ecclus 35, SgThree 3); world-english-catholic prints 2094 but is enumerated as 2131 (37 invented — Ecclus 34, Esth 3). Recomputed over printed loci only: greek additional 1356 (1355 composition-only + 1 textually-distinct), wec additional 6, universe 35809 + 1356 + 6 + 0 = 37171.
- **evidence:** scripts/_chronology.py:1820-1822 — "for (token, chapter), (low, high) in sorted(extents.items()): out.extend((token, chapter, verse) for verse in range(low, high + 1))". Measured: greek printed=2156 dense=2194; wec printed=2094 dense=2131. The invented Greek Ecclus loci (1:5, 1:7, 1:21, 3:19, 3:25, 10:21, 11:15-16, 13:14, 16:15-16, 17:5/9/16/18/21, 18:3, 19:18/19/21, 20:3, 22:9-10, 24:18/24, 25:12, 26:19-27) are the Latin pluses the cited Gigot article calls "foreign not only to the Greek, but also to the Hebrew text".
- **required correction:** Enumerate _system_loci from _deuterocanon._printed(system) rather than from the min..max span of _extents, exactly as _extents' own docstring warns ("Read from the text, never declared... a ceiling that is derived cannot be wrong without the text being wrong" — but a FLOOR-to-CEILING fill is neither). Then correct guidance §3.0.1 (1 391 → 1 355 of 1 356), guidance §9.3 (1 391 → 1 356, 9 → 6, 37 209 → 37 171), PROJECT-WORK.md's coverage tables, and rebuild coverage.tsv. The count of native loci lacking a chronology status falls from 10 to 7 (1 greek + 6 world-english-catholic).

### LEAD-013 — **major**

- **claim:** `event:israel.exile.second-captivity#0`
- **class:** profile-authority-rank — lower-rank-preferred-while-rank-1-speaks; one-source-sentence-dispositioned-three-ways
- **source locus:** 4 Kings 24:12
- **stored:** The SECOND captivity carries Usher's Anno Mundi figure, transmitted by the Haydock edition (rank 3), as the profile's `preferred` claim: A.M. 3405.
- **source supports:** Rank 1 is not silent: 4 Kings 24:12 reads "the king of Babylon received him in the eighth year of his reign", and no claim is authored from it. `query 4Kings.24.12` returns only "A.M. 3405 preferred / 597 B.C. alternate" — on the very verse that carries Scripture's own regnal dating. guidance §4.2: "A lower rank is consulted only where every higher rank is silent." THE THIRD CAPTIVITY IS WITHDRAWN FROM THIS FINDING: verification showed rank 1 IS authored there, as preferred and direct claims on the sibling events israel.exile.final-siege (4 Kings 25:1-2) and israel.exile.burning-of-the-temple (4 Kings 25:8-9). `query 4Kings.25.8` returns the regnal claim preferred and direct beside A.M. 3416. Re-authoring it on the parent event would be the duplication §6 forbids.
- **evidence:** 4 Kings 24:12 — "And Joachin, king of Juda, went out to the king of Babylon, he, and his mother, and his servants, and his nobles, and his eunuchs: and the king of Babylon received him in the eighth year of his reign." 4 Kings 25:8 — "In the fifth month, the seventh day of the month, the same is the nineteenth year of the king of Babylon, came Nabuzardan…"
- **required correction:** Author the rank-1 regnal claim from 4 Kings 24:12 for the second captivity and make it `preferred`, demoting A.M. 3405 to `alternate` — exactly the shape israel.exile.first-captivity already has, and exactly what the third captivity already achieves through its sibling events. The two changes must land together, since §4.4 refuses a subject on which no claim carries a disposition.

### LEAD-014 — **major**

- **claim:** `event:israel.exodus.the-exodus#0..#3`
- **class:** E-traditional-vs-modern-divergence — inadmissible-modern-figure-admitted-as-a-co-equal-disputed-claim; rank-1-thereby-demoted
- **source locus:** Howlett, "Biblical Chronology", CE vol. 3 (1908), the Exodus section; 3 Kings 6:1
- **stored:** Four claims on one subject, ALL `disputed`: #0 the traditional 1490 B.C.; #1 the encyclopedist's modern-critical "about 1277"; #2 the rank-1 interval of 3 Kings 6:1; #3 the Septuagint's 440-year variant of the same verse. Under §4.4 nothing on the subject can be `preferred` while any claim is `disputed`, so this profile displays no accepted date for the Exodus.
- **source supports:** Every one of the four is quoted accurately, and the corpus labels the modern figure honestly — its note carries the source's own boundary sentence ("This is not the traditional date of the Exodus") and states outright that it is "never to be displayed as the tradition's date". The defect is structural, not a misquotation: admitting a figure §4.1 excludes from this profile, as a `disputed` claim, is what pushes rank-1 Scripture out of `preferred` under §4.4.
- **evidence:** The claim's own note: "The profile boundary in the source's own words: 'This is not the traditional date of the Exodus, but as Father Hummelauer (Genesis, p. 29) says, it is the conclusion of most men in these days.' ... It is a 1908 encyclopedist following the Egyptologists and is never to be displayed as the tradition's date." guidance §4.1: "A modern chronology, if ever wanted, is a separate profile with its own id — never a silent correction of this one."
- **required correction:** Adopt the lead's action - move 'about 1277' out of catholic-traditional-v1, keep the encyclopedia's staging of the two reckonings in the subject note, re-dispose 3 Kings 6:1 (#2) preferred with #0 alternate, and fold the Septuagint 440 (#3) into #2 as a textual variant of the one verse. Two reinforcements the finding does not use. First, 4.3 grants an EXPRESS reporting licence to Ussher ('may be reported where a ranked Catholic source itself prints his figures') and grants none to modern critical chronology, so the corpus's own defence of #0 - Ussher's regnal years reported by a rank-6 Catholic work - is precisely the licence #1 lacks. Second, the corpus already treats the same Howlett sentence three different ways: 958 B.C. is an alternate under israel.monarchy.temple-begun beside a preferred rank-1 claim, 1020 B.C. is an alternate under israel.monarchy.saul-accession whose note says 'this profile does not display it first', and only 1277 is disputed - and disputed is the one disposition that, by 4.4, demotes the rank-1 verse. Aligning the Exodus with the treatment the corpus already gives the other two figures from the same sentence fixes the defect with no new policy.

### LEAD-015 — **major**

- **claim:** `event:israel.monarchy.demand-for-a-king#0 -> event:israel.judges.period#0 -> event:israel.monarchy.saul-accession`
- **class:** B-wrong-anchor (emergent) — anchor-chain-resolves-an-event-from-its-own-consequence
- **source locus:** 1 Kings 8:1-5; Acts 13:20
- **stored:** A two-hop anchor chain: demand-for-a-king is stored as an offset from israel.judges.period, which is itself stored as an offset from israel.monarchy.saul-accession.
- **source supports:** The demand for a king is what BRINGS ABOUT Saul's accession — 1 Kings 8 is the demand, 1 Kings 10 the election. The chain therefore positions an event from its own consequence, two hops away. Neither hop is source-supported: Acts 13:20 measures nothing from Saul's accession, and 1 Kings 8:1 gives only "when Samuel was old".
- **evidence:** 1 Kings 8:5 (tracked Douay) — the elders say to Samuel: "make us a king, to judge us, as all nations have." Acts 13:20 (tracked Douay) — "As it were, after four hundred and fifty years. And after these things, he gave unto them judges, until Samuel the prophet."
- **required correction:** Fix hop two first, as the lead says, but on the stronger ground and with a different first move. israel.judges.period#0 is not merely wrongly anchored: guidance 10 defines relative as 'an offset: N units after/before a named anchor event', the label supplies the N ('four hundred and fifty years') and the anchor supplies the event (saul-accession at 1020 B.C.), so a consumer combining the two fields the corpus publishes reads 570 B.C. for the period of the Judges. The subject's own note already says the figure is a DURATION, so this is 10.0 and 15.1(6) verbatim, surviving the very migration that moved 47 sibling claims out of relative - re-type it as precision: duration with statement and no anchor. That alone dissolves the chain, since demand-for-a-king would then hang on a duration and no longer reach saul-accession. Note also that the anchor is doubly wrong: saul-accession stands at the interval's END, contra 15.1(2), and its only claim is Howlett's 1020 B.C., the same modern-critical sentence LEAD-014 is about, marked alternate with a note saying the profile does not display it - so the chain resolves the Judges from a figure the profile itself declines to prefer. Finally, the lead's proposed re-typing of demand-for-a-king 'as containment' is not implementable as written: 10.0 defines within only on duration ('a duration may say what it sits within'), and demand-for-a-king is a point event, so either extend the model or leave it as a relative naming judges.period with no offset, which is what it already is and is harmless once hop two is fixed.

### LEAD-016 — **major**

- **claim:** `binding:narrated-event:life-of-christ.crucifixion@Matt.27.33-54`
- **class:** binding-scope — binding scope reaches one verse whose own words place its action later
- **source locus:** Matthew 27:53
- **stored:** The Crucifixion narrated-event binding runs Matt.27.33-54, so Matt 27:52-53 — the saints' bodies rising and coming out of the tombs — sits inside the scope and is answered with the Crucifixion's day-precision claims.
- **source supports:** Matthew 27:53 reads "And coming out of the tombs AFTER HIS RESURRECTION, came into the holy city and appeared to many." The coming out and the entering are placed after the Resurrection by the verse itself, and are answered with the Crucifixion's day-precision claims.
- **evidence:** Matt 27:53 (tracked Douay): "And coming out of the tombs after his resurrection, came into the holy city and appeared to many." `tools/tpt scripture-chronology query Matt.27.53` answers: narrated-event | the 14th of Nisan, on a Friday | disputed | DIRECT | life-of-christ.crucifixion.
- **required correction:** Narrow the Matthew range so 27:53 falls outside the Crucifixion binding, or state in the binding's note why the pericope is bound whole. The other seven boundaries are correct and must not be disturbed.

### LEAD-017 — **major**

- **claim:** `unit:composition.book-of-jonas#0`
- **class:** E-semantic-type/profile — a prophet's lifetime promoted to a composition date and marked preferred; a hedged reported form treated as an assertion
- **source locus:** Driscoll, "Jonah", CE vol. 8 (1910), the authorship paragraph
- **stored:** A `preferred` composition claim for the Book of Jonas: precision interval, 800 B.C. to 701 B.C., label "the eighth century B.C.". `tools/tpt scripture-chronology query Jon.1.1` returns it as the profile's composition date.
- **source supports:** The article gives NO date for the writing. Its only eighth-century figure is a hedged parenthesis about the PROPHET'S LIFETIME, sitting inside a sentence whose main clause denies that the book claims Jonah as its writer: "nowhere does the book itself claim to have been written by the Prophet (who is supposed to have lived in the eighth century B.C.)". The article's only other B.C. figures date the narrated events, not the writing.
- **evidence:** CE 08497b, verbatim: "Jewish tradition assumed that the Prophet Jonah was the author of the book bearing his name… But it may be remarked that nowhere does the book itself claim to have been written by the Prophet (who is supposed to have lived in the eighth century B.C.), and most modern scholars, for various reasons, assign the date of the composition to a much later epoch, probably the fifth century B.C."
- **required correction:** Withdraw unit:composition.book-of-jonas#0 and record typed silence for the composition of Jonas, exactly as was done for both books of Esdras under §15.1(3). If anything is retained it must be re-typed as the prophet's lifetime or as the narrated events, never as composition and never `preferred`. Do NOT substitute the article's "probably the fifth century B.C.": that is the modern-scholars voice §4.3 excludes.

### N-006 — **major**

- **claim:** `translation-independent-identity/A+B/gate-soundness-and-greek-sirach-extent`
- **class:** architecture-acceptance — over-broad-native-scope + unsound-load-gate; wrong text's composition date returned to a consumer
- **source locus:** greek Ecclus.36.16 (== vulgate Ecclus.36.18)
- **stored:** composition.book-of-ecclesiasticus.greek is scoped to the WHOLE Greek book, on the stated ground that "sharing is impossible" and that "the load-time gate would refuse this scope if it did not".
- **source supports:** False at one locus, and the query answers about the wrong text there. The repository's own concordance carries greek Ecclus 36:16 SAFELY to vulgate Ecclus 36:18 — one deliberate, verified row. The §3.0 gate probes each span at `span.first or 1` only, so a whole-book span is tested at Ecclus 1:1 (which refuses) and the shareable locus at 36:16 is never seen; the scope is admitted. At query time `chronology()` then takes the SHARED path for greek Ecclus.36.16, discards the native assertions it had already gathered, and returns the Vulgate unit's dates. Result: `query Ecclus.36.15 --system greek` -> textually-distinct / 'about 132 B.C.' (the Greek translation); `query Ecclus.36.16 --system greek` -> mapping 'shared', locus Ecclus.36.18, and 'composition.book-of-ecclesiasticus = 190 B.C. to 170 B.C.' plus the 'about 280 B.C.' alternate — the Hebrew original's dates, which the corpus's own note says "must not be conflated" with the Greek translation's; `query Ecclus.36.17 --system greek` -> back to 'about 132 B.C.'. A consumer asking the Greek text at 36:16 receives a date of a different text and a different answer than at the verses either side of it. Exhaustive scan: this is the only such locus in the shipped corpus (1 of 1 391 greek Ecclus loci). No test in tools/tests/test_chronology.py (84 tests) touches it.
- **evidence:** concordance row: "vulgate\tEcclus\t36\t18\tgreek\tEcclus\t36\t16\tone-to-one\treward them that patiently wait for thee\tgive reward unto them that wait for\testablished by reading the verse: the introit Da pacem Domine sustinentibus te is Vulgate 36:18 and Greek 36:16, and Greek 36:18 is the proverb of the belly" — corpus comment: "This unit is admissible precisely because sharing is impossible. The concordance refuses 1 355 of the Greek book's 1 356 loci ... and the load-time gate would refuse this scope if it did not." — observed: "greek Ecclus.36.16 -> composition-only shared | ['composition.book-of-ecclesiasticus=190 B.C. to 170 B.C.', 'c
- **required correction:** Two changes. (1) Make the §3.0 gate sound: probe every locus a native span covers, not `span.first or 1`, so a span containing ANY safely-corresponding locus is refused at load. (2) Narrow composition.book-of-ecclesiasticus.greek so it does not claim Ecclus 36:16 — or decide, and state, which text's date 36:16 carries and author it there. Either way the whole-book span must stop asserting an extent the corpus's own concordance contradicts. Correct the false comment at composition.yaml:1408-1412 in the same change.

### P-004 — **major**

- **claim:** `event:israel.exodus.the-exodus#1`
- **class:** profile-boundary/modern-criticism — modern-critical figure held level with a rank-1 scriptural statement
- **source locus:** 'Biblical Chronology', section 'The Exodus to the building of Solomon's Temple'
- **stored:** The Exodus, about 1277 B.C., disposition DISPUTED - i.e. carried at the same disposition as 3 Kings 6:1's own statement on the same subject.
- **source supports:** Howlett concludes for about 1277 B.C. on Sayce's, Driver's and Wellhausen's Egyptological and Assyriological grounds, and says in the same section that this is not the traditional date.
- **evidence:** We conclude, therefore, that the date of the Exodus was about 1277, the monarchy was founded by Saul, 1020; David mounted the throne, 1002; Solomon in 962, and the Temple was begun, 958 B.C.
- **required correction:** Change the disposition of this claim to `alternate`. The profile names 'Modern critical, archaeological, Egyptological and Assyriological chronology' a non-authority; carrying Howlett's Egyptological reconstruction as `disputed` beside event:israel.exodus.the-exodus#2 makes it the equal of Scripture's own statement in the query's ordering and forbids any claim on the subject being preferred (§4.4). The same corpus already contains the correct handling of the identical figure at event:israel.monarchy.temple-begun#5, where Howlett's '958 B.C.' from this same paragraph is `alternate` under a preferred rank-1 claim.

### P-011 — **major**

- **claim:** `event:israel.exile.second-captivity#0`
- **class:** profile-boundary/rank-1 — rank-1 statement omitted, so a rank-3 printing of Ussher's Anno Mundi figure is displayed first at the verse that dates the event
- **source locus:** Ps.70.1 note; artifact PDF page 776, printed p. 740
- **stored:** A.M. 3405 is the PREFERRED claim for the second captivity of Juda, and no rank-1 claim exists on that subject.
- **source supports:** Haydock prints Usher's A.M. 3405 for the second captivity. Scripture dates the same event at 4 Kings 24:12, 'in the eighth year of his reign', and at 24:8 gives Joachin's age and three-month reign; neither is authored as a claim.
- **evidence:** And Joachin, king of Juda, went out to the king of Babylon, he, and his mother, and his servants, and his nobles, and his eunuchs: and the king of Babylon received him in the eighth year of his reign.
- **required correction:** Author the rank-1 claim from 4 Kings 24:12 on israel.exile.second-captivity, mark it `preferred`, and demote this A.M. 3405 claim to `alternate` - exactly the shape israel.exile.first-captivity already has (Dan 1:1 preferred over A.M. 3398). Until then a consumer running `tools/tpt scripture-chronology query 4Kings.24.12` receives 'A.M. 3405 preferred' and never sees the verse's own 'in the eighth year of his reign'.

### S1-003 — **major**

- **claim:** `unit:composition.third-book-of-kings#0`
- **class:** S — conditional figure detached from an antecedent the source only reports, then given the preferred disposition (SS4.3 / SS15.1(3)); the resulting date also contradicts the article's own unconditional terminus
- **source locus:** Schets, "Third and Fourth Books of Kings", CE vol. 8 (1910), authorship and date paragraphs
- **stored:** Composition of the whole book of 3 Kings; disposition PREFERRED; precision approximate-year; 587 B.C.; label "not long before, or shortly after, the fall of Jerusalem (587 B.C.)". Delivered to consumers on every verse of 3Kings as the profile's first and only composition answer.
- **source supports:** The article asserts unconditionally only that "The Books of Kings were not completed in their present form before the middle of the Exile", and grounds that on Joachim's release in 562. The 587 figure appears solely inside a conditional whose antecedent the article does not endorse - "If Jeremias be indeed the author" - the authorship itself being reported from the Babylonian Talmud and from exegetes ("Not a few among both older and more recent exegetes consider this probable"). The article does not date the writing of 3 Kings to 587 B.C.
- **evidence:** The Books of Kings were not completed in their present form before the middle of the Exile. Indeed 2 Kings 25:27-30 , relates that Joachim was released from bondage (562) ... According to the Babylonian Talmud (Baba bathra, fol. 15, 1), the Prophet Jeremias is the author. Not a few among both older and more recent exegetes consider this probable. ... If Jeremias be indeed the author, it must be accepted as probable that he wrote the book not long before, or shortly after, the fall of Jerusalem (587 B.C. ); the last verses (xxv, 27-30) have possibly been added by a different hand.
- **required correction:** Withdraw the 587 B.C. figure as the preferred composition date of 3 Kings (and identically of 4 Kings) and author a gaps.yaml row naming this artifact, or at minimum demote to disputed with a note stating that the article's only unconditional statement — a whole-book terminus later than 587 — is what the source actually asserts. Confirmed live: `tools/tpt scripture-chronology query 3Kings.10.1` and `4Kings.10.1` both return "composition | not long before, or shortly after, the fall of Jerusalem (587 B.C.) | preferred | inherited". §15.1(3) is the named precedent (the Esdras 300 B.C. units).

### S1-010 — **major**

- **claim:** `unit:composition.book-of-osee#1`
- **class:** S — superscription-setting authored as composition (SS5, SS8, SS15 'never promote a superscription to a composition date'); the assertion is also about prophesying, not writing
- **source locus:** Cales, "Osee", CE vol. 11 (1911), section "Time of his ministry"
- **stored:** A COMPOSITION claim over the whole book of Osee; disposition alternate; precision range; 750 to 725 B.C.; label "from about 750 to 725 B.C."; the claim's own note says it is "the range the superscription gives" and that "A title is evidence about a setting, not proof of a year."
- **source supports:** The sentence is expressly title-derived and is about the period during which Osee PROPHESIED, not about when the book was written: "According to the title of the book, Osee prophesied during the reign of Jeroboam II ... hence from about 750 to 725 B.C." The article then sets the title aside as unsatisfactory. It says nothing about the date of writing or compilation.
- **evidence:** According to the title of the book, Osee prophesied during the reign of Jeroboam II in Israel , and in the time of Ozias , Joatham, Achaz , and Ezechias , kings of Juda, hence from about 750 to 725 B.C. The title, however, is not quite satisfactory and does not seem to be the original one, or, at least, to have been preserved in its primitive form.
- **required correction:** Withdraw this claim from composition.book-of-osee. If the title-derived range is to be kept - and it should be, it is real evidence - author it under the relation the guidance names for it, superscription-setting, via an event and a bindings.yaml row (the corpus already holds 26 such rows), scoped to the title verse Os.1.1 rather than to every verse of the book; prophecy-given is the alternative if the intended subject is the ministry. It must not stand as a composition date.

### S2-012 — **major**

- **claim:** `unit:composition.book-of-jonas#0`
- **class:** S — authorship-converted-into-composition-date
- **source locus:** Driscoll, "Jonah", CE vol. 8 (1910), on the authorship of the book; retained text line 48
- **stored:** COMPOSITION of the whole book of Jonas dated interval 800 B.C. to 701 B.C., label "the eighth century B.C.", date_str "800 B.C. to 701 B.C."; disposition PREFERRED and the only claim on the unit.
- **source supports:** The article dates no writing at all. It records the traditional authorship, attaches the eighth century to the PROPHET'S LIFETIME in a parenthesis hedged with "supposed", and in the very same sentence observes that the book nowhere claims to have been written by the Prophet.
- **evidence:** Jewish tradition assumed that the Prophet Jonah was the author of the book bearing his name, and the same has been generally maintained by the Christian writers who defend the historical character of the narrative. But it may be remarked that nowhere does the book itself claim to have been written by the Prophet (who is supposed to have lived in the eighth century B.C.), and most modern scholars, for various reasons, assign the date of the composition to a much later epoch, probably the fifth century B.C.
- **required correction:** Withdraw the structured date and hold the unit as typed silence (undated-in-tradition) with the authorship recorded in prose, OR re-type it as a derivation carrying its rule and inputs (traditional authorship + the prophet's supposed lifetime -> a composition window), visibly derived wherever displayed per 10 and 11. It may not stand as a sourced, preferred composition interval: no ranked source inspected here asserts a date for the writing of Jonas, and the corpus's own note concedes it. The 770-745 B.C. sentence in the same article is a narrated-event statement about the incidents and is not a substitute basis for this claim.

### S5-007 — **major**

- **claim:** `unit:composition.book-of-abdias#0`
- **class:** S-sample — a reported third-party opinion is displayed as the profile's `preferred` composition date on a subject the source expressly leaves undecided, and two material rival opinions from the same section are dropped on a stated ground that the retained text falsifies (§4.3, §4.4, §15.1(3))
- **source locus:** Gigot, "Abdias", CE vol. 1 (New York 1907), section "Date of the prophecy of Abdias"
- **stored:** precision interval, 900 B.C. to 801 B.C., scope book Abd, disposition PREFERRED, label "about the reign of Joram (ninth century B.C.)"; sole claim on the unit.
- **source supports:** Gigot does not assert this date. He reports it as the first of "the three leading forms of opinion which prevail at the present day", attributing it to Keil, Orelli, Vigouroux, Trochon and Lesetre, and marks the whole argument as reported ("we are told", "it is claimed", "it is inferred", "is said also to be confirmed"). He declines to decide.
- **evidence:** Many among them (Keil, Orelli, Vigouroux, Trochon, Lesetre, etc.) assign its composition to about the reign of Joram (ninth century B.C.). | Other scholars, among whom may be mentioned Meyrick, Jahn, Ackerman , Allioli , etc., refer the composition of the book to about the time of the Babylonian Captivity , some three centuries after King Joram. | The only other seizure of Jerusalem to which Abdias (11-14) could be understood to refer would be that which occurred during the lifetime of the prophet Jeremias and was effected by Nabuchodonosor (588-587 B.C.). | These, then are the three leading forms of opinion which prevail at the present day r
- **required correction:** Change the disposition to `disputed` - the source names three leading opinions and settles none, so under §4.4 nothing on this subject may be preferred - and author the rival opinions the same section supplies rather than dropping them. The note's ground for dropping them ("the source prints no year for either") is not correct: the article prints "Nabuchodonosor (588-587 B.C.)" for the capture of Jerusalem that the second opinion pins the book to, and states the second opinion in explicitly relative terms ("some three centuries after King Joram") which the corpus's own `relative` precision carries - it uses precisely that shape for Josue and for the birth of Abram elsewhere in this same package.

### S6-007 — **major**

- **claim:** `unit:composition.second-book-of-machabees#0`
- **class:** S-sample — over-broad-scope-contradicted-by-the-same-source
- **source locus:** "The Books of Machabees" (Bechtel, vol. 9, 1910), II Mach., sections "Contents" and "Author and date"
- **stored:** precision approximate-year, about 124 B.C., preferred, relation composition, scope {book: 2Mach} - the WHOLE book, all 15 chapters, reaching every verse by inheritance.
- **source supports:** Bechtel dates the EPITOME - "The book itself", ii, 20-xv, 40 - to about 124 B.C. The same article dates the two prefixed letters separately: the first (i, 1-10a) is itself "dated in the year 188 of the Seleucid era (i.e. 124 B.C.)", and the second (i, 10b-ii, 19) "must have been written soon after the death of Antiochus ... therefore about 163 B.C." The whole-book scope therefore asserts about 124 B.C. over the 55 verses 2Mach 1:1-2:19, and for 2Mach 1:10-2:19 the same source says about 163 B.C.
- **evidence:** "The second letter must have been written soon after the death of Antiochus, before the exact circumstances concerning it had become known in Jerusalem , therefore about 163 B.C." And: "The book itself begins with an elaborate preface (ii, 20-33) in which the author after mentioning that his work is an epitome of the larger history in five books of Jason of Cyrene states his motive in writing the book". And: "The first (i, 1-10a), dated in the year 188 of the Seleucid era (i.e. 124 B.C.)".
- **required correction:** Narrow this unit's scope to the epitome, 2Mach.2.20-15.40, and author separate units for the two prefixed letters: 2Mach.1.1-1.10 for the first letter ("dated in the year 188 of the Seleucid era (i.e. 124 B.C.)") and 2Mach.1.10-2.19 for the second ("therefore about 163 B.C."), each quoting the article. Douay boundaries verified: 2Mach 2:20 opens the epitomizer's preface ("Now as concerning Judas Machabeus ..."), 2Mach 1 has 36 verses, 2Mach 15 ends at verse 40, matching the article's own "ii, 20-xv, 40".

### S6-009 — **major**

- **claim:** `unit:composition.book-of-daniel#0`
- **class:** S-sample — period-gloss-stored-as-composition-date-while-the-source-own-composition-interval-is-dropped
- **source locus:** "Book of Daniel" (Gigot, vol. 4, 1908), section "Authorship and date of composition"
- **stored:** precision interval, 586 B.C. to 536 B.C., label "during the Exile (586-536 B.C.)", disposition preferred, relation composition, scope {book: Dan} - the whole book, deuterocanonical portions included by inheritance.
- **source supports:** 586-536 B.C. is Gigot's parenthetical gloss on the words "the Exile" inside the question he is framing. Two sentences later the same article states the traditional position's own date of writing: it "admits 570-536 B.C. as its date of composition". The corpus stored the period gloss as the composition interval and did not store, or anywhere record, the composition interval the article actually prints.
- **evidence:** "Over against this time-honoured position which ascribes to Daniel the authorship of the book which bears his name, and admits 570-536 B.C. as its date of composition, stands a comparatively recent theory which has been widely accepted by contemporary scholars." The stored figure comes instead from the framing question: "Is this sole writer the Prophet Daniel who composed the work during the Exile (586-536 B.C.), or, on the contrary, some author, now unknown ..."
- **required correction:** Author the preferred composition interval as 570-536 B.C. with the article's own words in the label ("admits 570-536 B.C. as its date of composition"), keeping 586-536 B.C. only in the note as the article's gloss on the Exile. Separately, because the traditional view as the article states it covers "the whole work, AS FOUND IN THE HEBREW BIBLE", either narrow this unit's scope or author the narrower units its own note contemplates over the deuterocanonical portions (Dan.3.24-90, Dan.13, Dan.14), which the whole-book scope now reaches with a claim the source does not make about them.

### V-004 — **major**

- **claim:** `coverage.native.greek.EsthGr.15.10`
- **class:** coverage-gap — mapping-status-standing-in-for-chronology-status
- **source locus:** greek | EsthGr.15.10
- **stored:** coverage --json files this locus under native_systems.greek.by_status as `textually-distinct`; `tools/tpt scripture-chronology query EsthGr.15.10 --system greek --json` returns "chronology_status":"textually-distinct" with "assertions":[].
- **source supports:** `textually-distinct` is a MAPPING answer, not a chronology status. The corpus holds NO chronology assertion and NO authored gap row for this locus, and none can currently be authored for it on the native path. IN SUPPORTED UNIVERSE BECAUSE: `_system_loci('greek')` enumerates the tracked Revised Version 1895 witness's printed extents, which include EsthGr 15:1-16. `to_canonical` refuses it because the concordance row is a MERGE, not an absence: `vulgate Esth 15:13-14 -> greek EsthGr 15:10 [merged-right]`, and to_canonical refuses a point->run conversion. A refusal for any reason is counted as `additional_loci`, i.e. as new Scripture. LACKS A STATUS BECAUSE: No authored scope in the corpus names this system+book. `_chronology.chronology()` for a non-preferred system calls `_native_assertions`, which walks ONLY `corpus.units` and `corpus.bindings` filtered to spans whose `system` equals the asked system; the only such scope in the whole corpus is `scope: {system: greek, book: Ecclus}` (src/sources/chronology/composition.yaml:1415). `corpus.gaps` are NEVER consulted on the native path - the gap loop (scripts/_chronology.py:1676) is reached only after to_canonical() succeeded - so no `undated-in-tradition` row could reach this locus either. With native == () the function returns the Unresolved from to_canonical, and `native_coverage` (scripts/_chronology.py:1888) files `reached.status` - the MAPPING word - into its per-system `by_status` table.
- **evidence:** vulgate Esth 15 13-14 greek EsthGr 15 10 merged-right ... the Vulgate divides "thou shalt not die" from "come near then, and touch the sceptre"; the Greek holds both in one verse
- **required correction:** Disposition: mapping-only alias / duplicate. -- Its text is Vulgate Esth 15:13-14, which is IN the primary universe and answers `composition-only` today. 9.3: "An alternate numbering of a safely corresponding locus is **not** new Scripture and is not counted." A merged-right correspondence IS a recorded correspondence; the refusal is a point-vs-run artefact of the API, not a statement that the Greek carries text the Vulgate lacks.

### V-005 — **major**

- **claim:** `coverage.native.world-english-catholic.Dan.3.71`
- **class:** coverage-gap — mapping-status-standing-in-for-chronology-status
- **source locus:** world-english-catholic | Dan.3.71
- **stored:** coverage --json files this locus under native_systems.world-english-catholic.by_status as `textually-distinct`; `tools/tpt scripture-chronology query Dan.3.71 --system world-english-catholic --json` returns "chronology_status":"textually-distinct" with "assertions":[].
- **source supports:** `textually-distinct` is a MAPPING answer, not a chronology status. The corpus holds NO chronology assertion and NO authored gap row for this locus, and none can currently be authored for it on the native path. IN SUPPORTED UNIVERSE BECAUSE: `_system_loci` enumerates the tracked World English Bible Catholic Edition's Daniel 3 extent, which prints v.71. The WEC->greek hop is `not-recorded`, so `to_canonical` returns textually-distinct; the `same_text_as_a_system_already_counted` probe re-asks the identical WEC->greek question and gets the identical refusal, so it does not catch it either. LACKS A STATUS BECAUSE: No authored scope in the corpus names this system+book. `_chronology.chronology()` for a non-preferred system calls `_native_assertions`, which walks ONLY `corpus.units` and `corpus.bindings` filtered to spans whose `system` equals the asked system; the only such scope in the whole corpus is `scope: {system: greek, book: Ecclus}` (src/sources/chronology/composition.yaml:1415). `corpus.gaps` are NEVER consulted on the native path - the gap loop (scripts/_chronology.py:1676) is reached only after to_canonical() succeeded - so no `undated-in-tradition` row could reach this locus either. With native == () the function returns the Unresolved from to_canonical, and `native_coverage` (scripts/_chronology.py:1888) files `reached.status` - the MAPPING word - into its per-system `by_status` table.
- **evidence:** greek world-english-catholic Dan 3 71 not-recorded ..."O you cold and heat": this edition prints one couplet of cold where the Greek prints two, and nothing in the tracked text settles which of the Greek's 45 and 49 this is
- **required correction:** Disposition: mapping-only alias / duplicate. -- WEC Dan 3:71 reads "O you cold and heat, bless the Lord! Praise and exalt him above all forever!"; the tracked Clementine Vulgate prints the same couplet at Dan 3:67, "O ye cold and heat, bless the Lord, praise and exalt him above all for ever." - a primary-universe locus that already answers `dated` (3 assertions, composition + historical-setting). Nothing new is being counted. NOTE ALSO: the row's reason names greek SgThree 1:45 and 1:49, and the tracked greek witness prints NEITHER; it prints the cold couplet inside SgThree 1:48 ("O ye light and darkness ... O ye cold and heat ..."). The stated ambiguity is between two verse numbers the witness does not print.

### V-006 — **major**

- **claim:** `coverage.native.world-english-catholic.Esth.1.1`
- **class:** coverage-gap — mapping-status-standing-in-for-chronology-status
- **source locus:** world-english-catholic | Esth.1.1
- **stored:** coverage --json files this locus under native_systems.world-english-catholic.by_status as `textually-distinct`; `tools/tpt scripture-chronology query Esth.1.1 --system world-english-catholic --json` returns "chronology_status":"textually-distinct" with "assertions":[].
- **source supports:** `textually-distinct` is a MAPPING answer, not a chronology status. The corpus holds NO chronology assertion and NO authored gap row for this locus, and none can currently be authored for it on the native path. IN SUPPORTED UNIVERSE BECAUSE: Printed by the WEC witness (2105 characters). The WEC->greek hop is `not-recorded`; both the to_canonical route and the already-counted probe ask that same hop, so the locus falls through to `additional_loci`. LACKS A STATUS BECAUSE: No authored scope in the corpus names this system+book. `_chronology.chronology()` for a non-preferred system calls `_native_assertions`, which walks ONLY `corpus.units` and `corpus.bindings` filtered to spans whose `system` equals the asked system; the only such scope in the whole corpus is `scope: {system: greek, book: Ecclus}` (src/sources/chronology/composition.yaml:1415). `corpus.gaps` are NEVER consulted on the native path - the gap loop (scripts/_chronology.py:1676) is reached only after to_canonical() succeeded - so no `undated-in-tradition` row could reach this locus either. With native == () the function returns the Unresolved from to_canonical, and `native_coverage` (scripts/_chronology.py:1888) files `reached.status` - the MAPPING word - into its per-system `by_status` table.
- **evidence:** greek Esth 1 1 world-english-catholic Esth 1 1 not-recorded ...this edition prints the whole of addition A inside its 1:1, so no number here addresses a verse of it
- **required correction:** Disposition: mapping-only alias / duplicate. -- The verse is a CONTAINER, not new text: it opens "[In the second year of the reign of Ahasuerus the great king, on the first day of Nisan, Mordecai ... saw a vision." (addition A = Vulgate Esth 11:2-12:6) and closes "...two chamberlains.] And it came to pass after these things in the days of Ahasuerus" (= Vulgate Esth 1:1). Both halves are in the primary universe and both answer `composition-only`. What is missing is a locus of its own, which is a granularity fact about this edition, not additional Scripture.

### V-007 — **major**

- **claim:** `coverage.native.world-english-catholic.Esth.3.13`
- **class:** coverage-gap — mapping-status-standing-in-for-chronology-status
- **source locus:** world-english-catholic | Esth.3.13
- **stored:** coverage --json files this locus under native_systems.world-english-catholic.by_status as `textually-distinct`; `tools/tpt scripture-chronology query Esth.3.13 --system world-english-catholic --json` returns "chronology_status":"textually-distinct" with "assertions":[].
- **source supports:** `textually-distinct` is a MAPPING answer, not a chronology status. The corpus holds NO chronology assertion and NO authored gap row for this locus, and none can currently be authored for it on the native path. IN SUPPORTED UNIVERSE BECAUSE: Printed by the WEC witness (2086 characters). Same `not-recorded` WEC->greek hop; same fall-through. LACKS A STATUS BECAUSE: No authored scope in the corpus names this system+book. `_chronology.chronology()` for a non-preferred system calls `_native_assertions`, which walks ONLY `corpus.units` and `corpus.bindings` filtered to spans whose `system` equals the asked system; the only such scope in the whole corpus is `scope: {system: greek, book: Ecclus}` (src/sources/chronology/composition.yaml:1415). `corpus.gaps` are NEVER consulted on the native path - the gap loop (scripts/_chronology.py:1676) is reached only after to_canonical() succeeded - so no `undated-in-tradition` row could reach this locus either. With native == () the function returns the Unresolved from to_canonical, and `native_coverage` (scripts/_chronology.py:1888) files `reached.status` - the MAPPING word - into its per-system `by_status` table.
- **evidence:** greek Esth 3 13 world-english-catholic Esth 3 13 not-recorded ...this edition prints the whole of addition B inside its 3:13
- **required correction:** Disposition: mapping-only alias / duplicate. -- Container again: ordinary Esth 3:13 ("The message was sent by couriers throughout the kingdom of Ahasuerus...") plus the whole of addition B, which is Vulgate Esth 13:1-7 - primary universe, `composition-only` today.

### V-008 — **major**

- **claim:** `coverage.native.world-english-catholic.Esth.4.6`
- **class:** coverage-gap — mapping-status-standing-in-for-chronology-status
- **source locus:** world-english-catholic | Esth.4.6
- **stored:** coverage --json files this locus under native_systems.world-english-catholic.by_status as `textually-distinct`; `tools/tpt scripture-chronology query Esth.4.6 --system world-english-catholic --json` returns "chronology_status":"textually-distinct" with "assertions":[].
- **source supports:** `textually-distinct` is a MAPPING answer, not a chronology status. The corpus holds NO chronology assertion and NO authored gap row for this locus, and none can currently be authored for it on the native path. IN SUPPORTED UNIVERSE BECAUSE: NOT PRINTED BY ANY WITNESS. `_system_loci` builds each system's universe from `_deuterocanon._extents`, which records only the LOWEST and HIGHEST verse number in a chapter, and then fills the whole integer range: `out.extend((token, chapter, verse) for verse in range(low, high + 1))` (scripts/_chronology.py:1817). WEC Esther 4 runs 1-47 with 6 missing, so verse 6 is manufactured. The manufactured locus then reaches no concordance row and is banked as new Scripture. LACKS A STATUS BECAUSE: No authored scope in the corpus names this system+book. `_chronology.chronology()` for a non-preferred system calls `_native_assertions`, which walks ONLY `corpus.units` and `corpus.bindings` filtered to spans whose `system` equals the asked system; the only such scope in the whole corpus is `scope: {system: greek, book: Ecclus}` (src/sources/chronology/composition.yaml:1415). `corpus.gaps` are NEVER consulted on the native path - the gap loop (scripts/_chronology.py:1676) is reached only after to_canonical() succeeded - so no `undated-in-tradition` row could reach this locus either. With native == () the function returns the Unresolved from to_canonical, and `native_coverage` (scripts/_chronology.py:1888) files `reached.status` - the MAPPING word - into its per-system `by_status` table.
- **evidence:** greek Esth 4 6 world-english-catholic absent-right ...this edition does not print Esther 4:6
- **required correction:** Disposition: should be excluded from supported universe. -- The corpus's own tracked concordance states in words that this edition does not print the verse, and the coverage report counts it as additional native Scripture anyway. `_deuterocanon._printed('world-english-catholic')` has no ('Esth',4,6) key. (The concordance itself is sound: its tiling gate checks only PRINTED verses, so the hole is entirely in `_system_loci`.)

### V-009 — **major**

- **claim:** `coverage.native.world-english-catholic.Esth.5.1`
- **class:** coverage-gap — mapping-status-standing-in-for-chronology-status
- **source locus:** world-english-catholic | Esth.5.1
- **stored:** coverage --json files this locus under native_systems.world-english-catholic.by_status as `textually-distinct`; `tools/tpt scripture-chronology query Esth.5.1 --system world-english-catholic --json` returns "chronology_status":"textually-distinct" with "assertions":[].
- **source supports:** `textually-distinct` is a MAPPING answer, not a chronology status. The corpus holds NO chronology assertion and NO authored gap row for this locus, and none can currently be authored for it on the native path. IN SUPPORTED UNIVERSE BECAUSE: Printed by the WEC witness (1228 characters). Same `not-recorded` WEC->greek hop; same fall-through. LACKS A STATUS BECAUSE: No authored scope in the corpus names this system+book. `_chronology.chronology()` for a non-preferred system calls `_native_assertions`, which walks ONLY `corpus.units` and `corpus.bindings` filtered to spans whose `system` equals the asked system; the only such scope in the whole corpus is `scope: {system: greek, book: Ecclus}` (src/sources/chronology/composition.yaml:1415). `corpus.gaps` are NEVER consulted on the native path - the gap loop (scripts/_chronology.py:1676) is reached only after to_canonical() succeeded - so no `undated-in-tradition` row could reach this locus either. With native == () the function returns the Unresolved from to_canonical, and `native_coverage` (scripts/_chronology.py:1888) files `reached.status` - the MAPPING word - into its per-system `by_status` table.
- **evidence:** greek Esth 5 1-2 world-english-catholic Esth 5 1-2 not-recorded ...this edition prints the whole of addition D inside its 5:1 and 5:2
- **required correction:** Disposition: mapping-only alias / duplicate. -- Addition D, which the Vulgate prints at Esth 15:4-19 - primary universe, `composition-only` today (checked at Esth.15.5, Esth.15.13, Esth.15.14). Same text, one edition's division.

### V-010 — **major**

- **claim:** `coverage.native.world-english-catholic.Esth.5.2`
- **class:** coverage-gap — mapping-status-standing-in-for-chronology-status
- **source locus:** world-english-catholic | Esth.5.2
- **stored:** coverage --json files this locus under native_systems.world-english-catholic.by_status as `textually-distinct`; `tools/tpt scripture-chronology query Esth.5.2 --system world-english-catholic --json` returns "chronology_status":"textually-distinct" with "assertions":[].
- **source supports:** `textually-distinct` is a MAPPING answer, not a chronology status. The corpus holds NO chronology assertion and NO authored gap row for this locus, and none can currently be authored for it on the native path. IN SUPPORTED UNIVERSE BECAUSE: Printed by the WEC witness (400 characters). Second half of the same `not-recorded` addition-D row. LACKS A STATUS BECAUSE: No authored scope in the corpus names this system+book. `_chronology.chronology()` for a non-preferred system calls `_native_assertions`, which walks ONLY `corpus.units` and `corpus.bindings` filtered to spans whose `system` equals the asked system; the only such scope in the whole corpus is `scope: {system: greek, book: Ecclus}` (src/sources/chronology/composition.yaml:1415). `corpus.gaps` are NEVER consulted on the native path - the gap loop (scripts/_chronology.py:1676) is reached only after to_canonical() succeeded - so no `undated-in-tradition` row could reach this locus either. With native == () the function returns the Unresolved from to_canonical, and `native_coverage` (scripts/_chronology.py:1888) files `reached.status` - the MAPPING word - into its per-system `by_status` table.
- **evidence:** greek Esth 5 1-2 world-english-catholic Esth 5 1-2 not-recorded ...this edition prints the whole of addition D inside its 5:1 and 5:2
- **required correction:** Disposition: mapping-only alias / duplicate. -- "And having raised the golden sceptre, he laid it upon her neck, and embraced her..." - the Vulgate's Esth 15:15ff. Already counted.

### V-011 — **major**

- **claim:** `coverage.native.world-english-catholic.Esth.8.13`
- **class:** coverage-gap — mapping-status-standing-in-for-chronology-status
- **source locus:** world-english-catholic | Esth.8.13
- **stored:** coverage --json files this locus under native_systems.world-english-catholic.by_status as `textually-distinct`; `tools/tpt scripture-chronology query Esth.8.13 --system world-english-catholic --json` returns "chronology_status":"textually-distinct" with "assertions":[].
- **source supports:** `textually-distinct` is a MAPPING answer, not a chronology status. The corpus holds NO chronology assertion and NO authored gap row for this locus, and none can currently be authored for it on the native path. IN SUPPORTED UNIVERSE BECAUSE: Printed by the WEC witness (4034 characters). Same `not-recorded` WEC->greek hop; same fall-through. LACKS A STATUS BECAUSE: No authored scope in the corpus names this system+book. `_chronology.chronology()` for a non-preferred system calls `_native_assertions`, which walks ONLY `corpus.units` and `corpus.bindings` filtered to spans whose `system` equals the asked system; the only such scope in the whole corpus is `scope: {system: greek, book: Ecclus}` (src/sources/chronology/composition.yaml:1415). `corpus.gaps` are NEVER consulted on the native path - the gap loop (scripts/_chronology.py:1676) is reached only after to_canonical() succeeded - so no `undated-in-tradition` row could reach this locus either. With native == () the function returns the Unresolved from to_canonical, and `native_coverage` (scripts/_chronology.py:1888) files `reached.status` - the MAPPING word - into its per-system `by_status` table.
- **evidence:** greek Esth 8 13 world-english-catholic Esth 8 13 not-recorded ...this edition prints the whole of addition E inside its 8:13
- **required correction:** Disposition: mapping-only alias / duplicate. -- Container: ordinary Esth 8:13 plus the whole of addition E = Vulgate Esth 16:1-24 - primary universe, `composition-only` today (checked at Esth.16.1).

### V-012 — **major**

- **claim:** `coverage.native.world-english-catholic.Esth.9.5`
- **class:** coverage-gap — mapping-status-standing-in-for-chronology-status
- **source locus:** world-english-catholic | Esth.9.5
- **stored:** coverage --json files this locus under native_systems.world-english-catholic.by_status as `textually-distinct`; `tools/tpt scripture-chronology query Esth.9.5 --system world-english-catholic --json` returns "chronology_status":"textually-distinct" with "assertions":[].
- **source supports:** `textually-distinct` is a MAPPING answer, not a chronology status. The corpus holds NO chronology assertion and NO authored gap row for this locus, and none can currently be authored for it on the native path. IN SUPPORTED UNIVERSE BECAUSE: NOT PRINTED BY ANY WITNESS. Manufactured the same way as Esth 4:6 by the range-fill in `_system_loci`; WEC Esther 9 runs 1-32 with 5 and 30 missing. LACKS A STATUS BECAUSE: No authored scope in the corpus names this system+book. `_chronology.chronology()` for a non-preferred system calls `_native_assertions`, which walks ONLY `corpus.units` and `corpus.bindings` filtered to spans whose `system` equals the asked system; the only such scope in the whole corpus is `scope: {system: greek, book: Ecclus}` (src/sources/chronology/composition.yaml:1415). `corpus.gaps` are NEVER consulted on the native path - the gap loop (scripts/_chronology.py:1676) is reached only after to_canonical() succeeded - so no `undated-in-tradition` row could reach this locus either. With native == () the function returns the Unresolved from to_canonical, and `native_coverage` (scripts/_chronology.py:1888) files `reached.status` - the MAPPING word - into its per-system `by_status` table.
- **evidence:** greek Esth 9 5 world-english-catholic absent-right ...this edition does not print Esther 9:5
- **required correction:** Disposition: should be excluded from supported universe. -- `_printed('world-english-catholic')` has no ('Esth',9,5) key. The greek witness does print Esth 9:5 and the Vulgate prints Esth 9:5; both are already accounted for on their own axes.

### V-013 — **major**

- **claim:** `coverage.native.world-english-catholic.Esth.9.30`
- **class:** coverage-gap — mapping-status-standing-in-for-chronology-status
- **source locus:** world-english-catholic | Esth.9.30
- **stored:** coverage --json files this locus under native_systems.world-english-catholic.by_status as `textually-distinct`; `tools/tpt scripture-chronology query Esth.9.30 --system world-english-catholic --json` returns "chronology_status":"textually-distinct" with "assertions":[].
- **source supports:** `textually-distinct` is a MAPPING answer, not a chronology status. The corpus holds NO chronology assertion and NO authored gap row for this locus, and none can currently be authored for it on the native path. IN SUPPORTED UNIVERSE BECAUSE: NOT PRINTED BY ANY WITNESS. Manufactured by the same range-fill. LACKS A STATUS BECAUSE: No authored scope in the corpus names this system+book. `_chronology.chronology()` for a non-preferred system calls `_native_assertions`, which walks ONLY `corpus.units` and `corpus.bindings` filtered to spans whose `system` equals the asked system; the only such scope in the whole corpus is `scope: {system: greek, book: Ecclus}` (src/sources/chronology/composition.yaml:1415). `corpus.gaps` are NEVER consulted on the native path - the gap loop (scripts/_chronology.py:1676) is reached only after to_canonical() succeeded - so no `undated-in-tradition` row could reach this locus either. With native == () the function returns the Unresolved from to_canonical, and `native_coverage` (scripts/_chronology.py:1888) files `reached.status` - the MAPPING word - into its per-system `by_status` table.
- **evidence:** greek Esth 9 30 world-english-catholic absent-right ...this edition does not print Esther 9:30
- **required correction:** Disposition: should be excluded from supported universe. -- `_printed('world-english-catholic')` has no ('Esth',9,30) key.

### V-014 — **major**

- **claim:** `coverage.native.printed_loci-includes-unprinted`
- **class:** coverage-gap — fabricated-loci-in-declared-universe
- **source locus:** native_systems.greek.printed_loci / native_systems.world-english-catholic.printed_loci
- **stored:** greek printed_loci 2194; world-english-catholic printed_loci 2131.
- **source supports:** The tracked witnesses print 2156 and 2094. `_system_loci` derives each system's universe from `_extents`, which keeps only min and max verse per chapter, then fills the whole integer range - manufacturing 38 greek loci and 37 world-english-catholic loci that no witness prints. 35 of the greek phantoms are Greek Ecclesiasticus loci that are then banked as `additional_loci` and DATED `composition-only` by the greek Ecclus unit (e.g. `query Ecclus.10.21 --system greek` returns "about 132 B.C." for a verse the Revised Version does not print). 3 of the world-english-catholic phantoms (Esth 4:6, 9:5, 9:30) are banked as additional native Scripture.
- **evidence:** scripts/_chronology.py: `out.extend((token, chapter, verse) for verse in range(low, high + 1))` // scripts/_deuterocanon.py `_extents`: "The first and last verse number the witness prints in each chapter."
- **required correction:** Build each system's universe from `_deuterocanon._printed(system).keys()` rather than from the min-max range fill in `_system_loci`, so a chapter with a hole in its numbering does not manufacture verses. Then re-derive `printed_loci` and `additional_loci`.

### V-015 — **major**

- **claim:** `coverage.native.additional_loci-overcounted`
- **class:** coverage-gap — overcounted-universe
- **source locus:** native_systems.greek.additional_loci=1391, native_systems.world-english-catholic.additional_loci=9
- **stored:** 1391 additional greek loci and 9 additional world-english-catholic loci are new Scripture outside the primary universe; declared universe 37209.
- **source supports:** Measured breakdown: greek 1391 = Ecclus 1390 + EsthGr 15:10. Of the 1390 Ecclus, 35 are phantom (V-014), leaving 1355 real - exactly the figure composition.yaml itself states. EsthGr 15:10 is a recorded merged-right correspondence to Vulgate Esth 15:13-14, i.e. the same text renumbered, which 9.3 says is not counted. Of the 9 world-english-catholic, 3 are phantom and 6 are containers holding text already counted in the primary universe (Vulgate Esth 1:1, 11:2-12:6, 13:1-7, 15:4-19, 16:1-24, Dan 3:67). By 9.3's own definition the corrected total is 35809 + 1355 + 0 + 0 = 37164, not 37209.
- **evidence:** guidance 9.3: "loci a system prints that the concordance refuses to carry to the preferred system, and which are therefore additional text rather than the same text renumbered. An alternate numbering of a safely corresponding locus is **not** new Scripture and is not counted." // composition.yaml: "The concordance refuses 1 355 of the Greek book's 1 356 loci" // guidance 3.0.1: "1 391 of its loci refuse the Vulgate"
- **required correction:** Recount `additional_loci` from printed loci only, and treat a recorded merged/split correspondence and a container locus holding already-counted text as `same_text_as_a_system_already_counted` rather than as additional Scripture. Then restate 9.3's total. Also correct 3.0.1's "1 391 of its loci refuse the Vulgate" - that is the whole-greek additional figure, not Ecclesiasticus's; composition.yaml's own "refuses 1 355 of the Greek book's 1 356 loci" is the correct one.

### V-016 — **major**

- **claim:** `coverage.native.no-authoring-route`
- **class:** coverage-gap — unauthorable-status
- **source locus:** all ten statusless native loci
- **stored:** Guidance 9 lists `undated-in-tradition` as authorable in gaps.yaml and 9.2 records that ten native loci have no chronology status.
- **source supports:** Those ten cannot be given one today, and for two independent structural reasons. (a) `_native_assertions` reads only units and bindings; the gap loop in `chronology()` is downstream of a SUCCESSFUL to_canonical, so a gap row scoped `{system: greek, ...}` or `{system: world-english-catholic, ...}` would never be reached by any of these ten. (b) For greek EsthGr 15:10 the block is harder still: `scripture_systems()` lets the greek system address 'EsthGr', but `_scope` refuses any scope whose book is not in `_canon` - "'EsthGr' is not a book of the canon" - and EsthGr is not. No unit, binding or gap naming EsthGr can load at all.
- **evidence:** scripts/_chronology.py `_scope`: `raise ChronologyError(f"{spot}: {token!r} is not a book of the canon; see scripts/_canon.py")` // `_native_assertions` docstring: "What was authored in the asked locus's OWN system, at its own locus." - its body iterates `corpus.units` and `corpus.bindings` only.
- **required correction:** Before any of the ten can be dispositioned as `undated-in-tradition` or `research-pending`, (1) make `chronology()` consult native-scoped gap rows on the native path, and (2) resolve the EsthGr contradiction - either admit EsthGr to the canon token list or stop letting `scripture_systems()` claim greek addresses it.


### Minor findings (49)

Prose, citation and metadata defects that change no factual result.

- **A2-028** `event:israel.judges.heli-judgeship#0` — unretained-source-characterised
- **A4-005** `event:israel.exodus.the-plagues-of-egypt#1` — over-broad-scope-in-display-label
- **A4-013** `event:israel.exile.ezechiel.call#0` — unmarked-elision-in-quoted-statement
- **A7-017** `event:israel.judges.capture-of-the-ark#0` — duration-figure-used-as-the-label-of-a-positional-claim
- **B-039** `binding:prophetic-referent:life-of-christ.nativity@Mich.5.2 AND @Mich.` — duplicate-overlapping-binding
- **C-006** `binding:superscription-setting Ps.53 -> israel.monarchy.david-in-the-d` — quotation not verbatim (terminal punctuation altered inside quotation marks)
- **D-004** `unit:composition.book-of-ecclesiasticus.greek#0` — authored scope does not reach one locus inside it; native assertion computed then discarded when the mapping s
- **D-005** `unit:composition.book-of-ecclesiasticus.greek#0` — stale user-facing example note contradicted by the expected output printed two lines above it
- **E1-006** `event:israel.primeval.deluge#0` — quotation-not-verbatim
- **E2-001** `event:israel.monarchy.temple-begun#2` — basis-and-note-mischaracterise-the-source
- **E2-003** `event:israel.monarchy.temple-begun#4` — false-internal-citation-in-note
- **E2-004** `event:israel.monarchy.temple-begun#5` — false-internal-citation-in-note
- **E2-006** `event:israel.exile.first-captivity#0` — repository-prose-set-inside-quotation-marks
- **E2-008** `event:israel.exile.third-captivity#0` — lower-rank-preferred-while-rank-1-speaks; quotation not verbatim
- **E2-012** `unit:composition.gospel-of-matthew#0` — quotation-attributed-to-an-article-that-does-not-contain-it
- **F-001** `gaps.undated-in-tradition.Lev` — unretained-source-characterisation; unqualified negative
- **F-005** `gaps.undated-in-tradition.Eccles` — overstated-silence; uncounted reported figures
- **F-010** `gaps.undated-in-tradition.Deut` — unqualified negative; sibling-row inconsistency
- **F-012** `gaps.undated-in-tradition.Gen` — unretained-source-characterisation; unqualified negative
- **F-013** `gaps.undated-in-tradition.Num` — unretained-source-characterisation; unqualified negative
- **F-021** `gaps.undated-in-tradition.Deut` — duplicate artifact identity; inconsistent citation across sibling rows
- **G-002** `binding:israel.wilderness.manna/retrospective-event/Ps.77.23-25+Ps.104` — quotation-not-from-tracked-text
- **G-006** `event:israel.monarchy.temple-begun#2` — source-mischaracterisation
- **G-008** `gaps.yaml#11 (Gen, undated-in-tradition) - the sentence characterising` — over-strong-characterisation-of-a-retained-source
- **G-010** `event:israel.monarchy.david-in-the-cave#0 (note)` — stale-refusal-left-in-place
- **G-015** `tools/scripture-chronology QUERY example note (Ecclus.35.1 --system gr` — stale-refusal-enshrined-in-documentation
- **LEAD-001** `event:israel.exile.third-captivity#0` — misquotation-inside-quotation-marks
- **LEAD-002** `event:israel.exile.second-captivity#0` — misquotation-inside-quotation-marks
- **LEAD-003** `src/sources/chronology/cold-audit-manifest.tsv` — unreproducible-documented-selection-rule
- **LEAD-004** `src/sources/chronology/cold-audit-manifest.tsv` — complete-inspection-set-not-tracked
- **LEAD-007** `event:apostolic-age.death-of-herod-agrippa#0; event:apostolic-age.jewi` — quoted-source-not-named
- **LEAD-008** `gap:Num` — unretained-evidence-behind-a-negative-claim
- **LEAD-012** `unit:composition.book-of-ecclesiasticus.greek#0 (scope {system: greek,` — unsound-load-gate-probes-only-the-span-start; native-scope-covers-a-shareable-locus
- **LEAD-018** `event:life-of-christ.crucifixion (subject note, src/sources/chronology` — quotation from memory, in quotation marks, between two accurate quotations (§15.1(1))
- **N-008** `translation-independent-identity/separate-axes/native-coverage-histogr` — mapping status reported as a chronology status in the derived coverage view
- **N-009** `translation-independent-identity/B/tool-example-note` — stale user-facing documentation contradicting the shipped behaviour and §3.0.1
- **P-012** `event:israel.exile.third-captivity#0` — quotation not verbatim
- **P-020** `event:apostolic-age.exile-of-saint-john-to-patmos#0` — patristic work mis-named in a note; three quoted sources not named among the claim's source records
- **P-025** `event:israel.monarchy.birth-of-david#0` — a passage record exists at the exact locus and is not named
- **S1-001** `event:israel.monarchy.temple-begun#4` — note-prose inaccurate about the source's own layout
- **S2-003** `event:life-of-christ.finding-in-the-temple#0` — quotation-not-verbatim-in-tracked-text
- **S2-008** `unit:composition.gospel-of-john#0` — date-precision-shape
- **S2-009** `event:apostolic-age.second-arrest-of-saint-paul#0` — unsupported-approximation
- **S3-001** `event:life-of-christ.crucifixion#6` — quotation-from-memory (guidance 15.1(1)); scripture quotation does not match the tracked Douay text at the loc
- **S4-005** `event:life-of-christ.crucifixion#5` — quotation not verbatim in the tracked text at the locus it is attributed to (15.1(1)); the date itself is soun
- **S4-011** `event:israel.judges.capture-of-the-ark#0` — the display label of a relative claim is the anchor's duration, so the rendered answer states a length where t
- **S6-002** `event:israel.exile.first-captivity#0` — quoted-string-is-repository-prose-not-source-words
- **S6-011** `event:apostolic-age.saint-paul-first-roman-captivity#1` — hedge-not-preserved-on-the-begin-endpoint
- **V-017** `coverage.native.named-systems-omitted` — unenumerated-system-omitted


## Raised and refuted (68)

Raised by an auditor and did not survive independent re-reading. Recorded so a
correction lane does not re-raise them without new evidence.

- **A1-005** `event:life-of-christ.flight-into-egypt#1` — No hedge was dropped: the label is the source's own words verbatim, and the 'probable' hedge attaches to Herod's death-year, which the claim's basis quotes in full and the anchor event carries structurally as an approximate-year.
- **A1-020** `event:apostolic-age.flight-of-the-christians-from-jerusalem#0` — The corpus stores Eusebius's own phrase 'before the war' unaltered, quotes the whole sentence in the basis so the grammar the finding relies on is visible to any reader, and states in the note that Eusebius gives no interval; guid
- **A1-021** `event:apostolic-age.flight-of-the-christians-from-jerusalem#1` — The very disclosure the finding asks for is already stored on the claim - note: 'The article's dated sentence is about Gallus's arrival on 30 October 66; the withdrawal is placed after it without a date of its own' - and the claim
- **A1-023** `event:apostolic-age.return-of-saint-john-from-patmos#0` — Not §15.1(2): the relative statement carries Eusebius's own words naming Domitian's death, and the anchor apostolic-age.exile-of-saint-john-to-patmos is itself dated 'the reign of the Emperor Domitian (81-96)', whose terminus IS t
- **A2-007** `event:israel.patriarchs.covenant-of-circumcision#0` — No defect: the temporal assertion is Abraham's ninety-nine years, which Gen.17.24 alone states and which the claim names as its source; Gen.17.25 is adjacent context quoted verbatim from this repository's tracked Douay and named b
- **A2-010** `event:israel.egypt.descent#0` — The finding's premise is false - the encyclopedia article is a registered source-library artifact (src/sources/works/catholic-encyclopedia/volume-3/editions/new-york-1908/artifacts/newadvent-03731a-f5f96f04/artifact.toml) and is q
- **A2-014** `event:israel.exodus.the-exodus#2` — Nothing is inverted, because a relative date in this model carries only {of, statement, note} and no signed magnitude - scripts/_chronology.py rejects any other key - so the direction lives entirely in the prose, and the prose is 
- **A2-015** `event:israel.exodus.the-exodus#3` — Same refutation: the relative structure encodes no direction to invert, the statement is the encyclopedia's sentence verbatim, the anchor israel.monarchy.temple-begun is correct, and a live query returns the source's words unchang
- **A2-022** `event:israel.wilderness.moses-final-discourse#0` — The finding concedes the anchor and the offset are correct, so no §15.1(2) defect exists; Deut.1.3 is quoted verbatim and the claim's note already ties the reckoning to the same era as Aaron's death, which is Numbers 33:38 - a sou
- **A2-025** `event:israel.conquest.calebs-inheritance#0` — The anchor is not an unlocated span: israel.wilderness.forty-years-in-the-desert is grounded on Numbers 14:33-34 and its own note says the forty years are 'a sentence pronounced at the return of the spies, and are counted from tha
- **A3-009** `event:israel.monarchy.temple-begun#0` — Refuted: the contract permits this. The label carries the verse's own words in full and the 480-year clause names its own origin inside the quoted text -- "after the children of Israel came out of the land of Egypt" -- so it canno
- **A3-010** `event:israel.monarchy.temple-finished#0` — Refuted: nothing false or computable is produced. The claim is typed relative because its primary assertion is the regnal offset, the anchor is right, and the seven years appears only as descriptive prose inside relative.statement
- **A4-009** `event:israel.wilderness.promulgation-of-the-law#0` — Refuted: the claim's own note already says what is measured and from what -- the third day is counted from the sanctifying commanded at Exodus 19:10 -- and Exodus states no interval at all between 19:1 and 19:10, so the arrival at
- **A5-025** `event:israel.primeval.division-of-the-earth#0` — The contract's closed precision vocabulary has no contained-span type, `duration` is structurally unavailable because "in his days" is not a whole positive number of units, and `interval` requires absolute endpoints, so `relative`
- **A6-013** `event:israel.egypt.butler-and-baker#0` — The direction and the terminus do reach the consumer: `tools/tpt scripture-chronology query Gen.40.5 --json` returns date = "After two years Pharao had a dream", Gen 41:1 verbatim, and §10 makes the short label a display string th
- **A6-020** `event:israel.conquest.sending-of-the-spies-to-jericho#0` — The finding's own preferred correction is already what the corpus did - the event's authored scope is Jos.1.10-18 together with Jos.2.1-24, so the order at Jos 1:10-11 that the three days are actually measured from stands inside t
- **A6-023** `event:israel.conquest.last-charge-and-death-of-josue#0` — The peace Jos 23:1 measures from is Jos 21:42, not Jos 11:23 - the Vulgate wording is a direct echo ("pax in omnes per circuitum nationes" / "subjectis in gyro nationibus universis"), whereas Jos 11:23 reads "quievitque terra a pr
- **A7-015** `event:israel.judges.samuel-at-silo#0` — The corpus already types this as containment in its own words and supplies no quantity; the recommended CONTAINED_SPAN precision does not exist in the closed vocabulary and `duration.within` is unavailable because Scripture states
- **A7-016** `event:israel.judges.call-of-samuel#0` — Same structural refutation as A7-015 - no contained-span precision exists and no length is stated, so containment is carried by a relative claim with the verses verbatim and no offset - and the note already says the two temporal w
- **A7-020** `event:israel.monarchy.demand-for-a-king#0` — Containment again, and the claim says so in terms: the label is the verse's own "when Samuel was old", no offset value exists, and the note states that the old age "is a point in the period of the judges and not a year, and the co
- **A7-022** `event:israel.monarchy.deliverance-of-jabes-galaad#0` — The finding's factual premise about the corpus is false - israel.monarchy.saul-accession is scoped in bindings.yaml to exactly 1Kings.10.17-27 plus 11.14-15, i.e. the assembly and election by lot at Maspha, with the private anoint
- **A7-024** `event:israel.monarchy.news-of-sauls-death#0` — The claim already records, in its note, the very distinction the finding demands, and the label is the source's own words naming Siceleg so it cannot be read as "the third day after Saul's death"; the anchor is the one the verse i
- **A7-025** `event:israel.monarchy.isboseth-reign#0` — The synchronism is the source's own: 2 Kings 2:10 states that during Isboseth's two years "only the house of Juda followed David" and 2:11 gives that same Juda reign at Hebron as seven years and six months, so "while" reproduces t
- **A8-008** `event:israel.monarchy.david-delivered-from-his-enemies#0` — The contract's `relative` shape is `of` + prose `statement` with no numeric offset, it is the corpus's sanctioned and ubiquitous form for an occasion held relative to an event, and this claim's own note discloses in terms the very
- **B-016** `binding:prophecy-given:israel.exile.final-siege@Ezech.24` — prophecy-given (when the oracle was uttered) and narrated-event (when the wife died) are different relations that §5 requires be kept as two assertions on one locus, and the corpus does exactly that: the chapter's oracle carries t
- **B-020** `binding:historical-setting:israel.exile.first-captivity@Dan` — historical-setting is defined by §5 as "the occasion tradition associates with the text", not as a claim that any verse narrates it; CE grounds the whole-book association by making the book the sole source of the man's life and be
- **B-023** `binding:narrated-event:life-of-christ.crucifixion@Matt.27.33-54,Mark.1` — Everything the finding says should be outside the scope already is: the four ranges begin at Augustine's own Golgotha verse and stop at the centurion, and the corpus's note excludes the way to Calvary, the burial and the hour of t
- **B-044** `binding:prophecy-given:israel.restoration.temple-work-resumed@Zach.1-8` — The scope is not over-broad but exactly the extent the source itself treats as one unit: CE calls chapters 1-8 "Part first", gives it one occasion in its own voice, and dates part second thirty-five years later - which is why the 
- **C-004** `binding:superscription-setting Ps.50 -> israel.monarchy.david-repentan` — A binding carries no date (§6) and its `sources` are optional in the loader (`_sources(entry, where, required=False)`), the quoted Commission language is verbatim in a registered, retained artifact of this repository so the claim 
- **C-010** `binding:historical-setting Ps.62,Ps.70 -> israel.monarchy.david-flight` — The note attributes the quoted words to "the verified Haydock record at Ps 70:1", and that record - a registered source-library passage record, which §11 names as a source record in its own right - carries the string verbatim in i
- **C-030** `binding:superscription-setting Ps.58 -> israel.monarchy.saul-reign` — The stored sentence is true as written - CE 'King David' dates no episode of David's life - and the general frame the finding produces is printed in reported voice ("According to the usual chronology") and immediately qualified, w
- **D-002** `unit:composition.book-of-ecclesiasticus.greek#0` — The contract puts the display string beside the structure and never inside it; the authored label carries Gigot's one-sided hedge verbatim, the CLI's human output prints that label, and "about 132 B.C." is a generic rendering of t
- **E1-020** `event:israel.monarchy.temple-begun#0` — The machine truth is the structure and it names exactly one anchor, the right one; the second interval is not duplicated here as a claim but appears only inside a quotation of the verse that names its own terminus, and it is separ
- **E2-010** `event:israel.restoration.nehemias-mission#0` — The hedge is not severed: the basis quotes Howlett's whole sentence including "But it is commonly held that", the note names the hedge as his in his own words, and the disposition is `disputed`, so nothing reaches a consumer as se
- **E2-016** `unit:composition.gospel-of-matthew#4` — The attribution is not severed from the claim: the basis quotes "In our day opinion is rather divided. Catholic critics, in general, favour the years 40-45" verbatim and then says in terms that this is the position the article att
- **E2-020** `unit:composition.epistle-to-philemon#0` — The step the finding calls undisclosed is disclosed in the claim itself - the basis says the article "places it among the captivity letters of the first Roman imprisonment" and the note says the window "is stated of Colossians, Ep
- **E3-006** `unit:composition.book-of-esther#0` — No widening is smuggled: 485 and 425 are the only regnal years the article itself prints for those two reigns, the label reproduces the source's sentence including "at the end of the reign of Xerxes I" verbatim, and `interval` mea
- **E3-014** `unit:composition.book-of-malachias#0` — No Sec. 4.3 figure is in play and no wrong result reaches a consumer: the article asserts the same date in its own voice in the same section, "about 450 B.C.", which falls inside the stored interval and inside the stored label "ab
- **F-009** `gaps.undated-in-tradition.Amos` — Refuted: neither eighth-century sentence is the article dating the book in its own voice - the first is expressly reported ('commonly ascribed') and is about Osee, not Amos, and the second says only that the book informs us of eig
- **F-011** `gaps.undated-in-tradition.Ex` — Refuted outright: nothing is suppressed - the corpus already carries the March-April sentences as a queryable alternate narrated-event on israel.exodus.the-plagues-of-egypt, quoting them in full with the article's own refusal pres
- **LEAD-006** `unit:composition.first-epistle-of-st-john#0; unit:composition.second-e` — Refuted on the fact the finding turns on: I re-retrieved CE 08435a and Drum does not refuse to date these epistles - he denies certainty and then states a probable date that agrees with Durand's window - so there is no suppressed 
- **N-007** `translation-independent-identity/B/stated-loci-counts` — Half the finding is measurably false and its correction would introduce an error: composition.yaml's "1 355 of the Greek book's 1 356 loci" is EXACT against the witness edition's printed verses (greek Ecclus prints 1 356 loci; 1 3
- **P-005** `event:israel.exodus.the-exodus#2` — No defect in this claim: the finding's own source_supported_assertion concedes the Douay is quoted correctly (verified against the tracked text), and §4.4 expressly designs `disputed` to block preference — the claim's own note sta
- **P-006** `event:israel.exodus.the-exodus#3` — The encyclopedia asserts the Septuagint reading in its OWN voice, twice, not in a third party's, so §4.3/§15.1(3) does not exclude it; a forty-year divergence in the pivotal interval is a chronological assertion, and §4.4 and §15(
- **P-026** `unit:composition.book-of-micheas.chapters-1-3#0` — Not a duplicate: the two records carry DIFFERENT sha256 and byte_size (16554 vs 16195 — the 359-byte New Advent template delta the lead already holds), and were registered by two different lanes in two different commits, which is 
- **P-027** `unit:composition.book-of-micheas.chapters-4-5#0` — Same refutation as P-026 on the identical pair: the twin records differ by hash and byte_size, not by nothing, and sources.md expressly provides that changed bytes receive a new artifact record while existing consumers stay pinned
- **P-028** `unit:composition.book-of-nahum.chapters-2-3#0` — The contract expressly provides for this: 'Materially changed bytes do create a new artifact identity' and 'Changed bytes receive a new artifact record and consumers remain pinned until reviewed.' The two records carry different s
- **P-029** `event:israel.exodus.moses-in-madian#1` — The contract expressly provides for this: 'Materially changed bytes do create a new artifact identity' and 'Changed bytes receive a new artifact record and consumers remain pinned until reviewed.' The two records carry different s
- **P-030** `event:israel.wilderness.jethro-and-the-judges#0` — The contract expressly provides for this: 'Materially changed bytes do create a new artifact identity' and 'Changed bytes receive a new artifact record and consumers remain pinned until reviewed.' The two records carry different s
- **P-031** `gap:Mich.6-7` — The contract expressly provides for this: 'Materially changed bytes do create a new artifact identity' and 'Changed bytes receive a new artifact record and consumers remain pinned until reviewed.' The two records carry different s
- **P-032** `gap:Nah.1` — The contract expressly provides for this: 'Materially changed bytes do create a new artifact identity' and 'Changed bytes receive a new artifact record and consumers remain pinned until reviewed.' The two records carry different s
- **P-033** `gap:Deut` — The contract expressly provides for this: 'Materially changed bytes do create a new artifact identity' and 'Changed bytes receive a new artifact record and consumers remain pinned until reviewed.' The two records carry different s
- **P-034** `gap:Ex` — The contract expressly provides for this: 'Materially changed bytes do create a new artifact identity' and 'Changed bytes receive a new artifact record and consumers remain pinned until reviewed.' The two records carry different s
- **P-035** `gap:Gen` — The contract expressly provides for this: 'Materially changed bytes do create a new artifact identity' and 'Changed bytes receive a new artifact record and consumers remain pinned until reviewed.' The two records carry different s
- **P-036** `gap:Num` — The contract expressly provides for this: 'Materially changed bytes do create a new artifact identity' and 'Changed bytes receive a new artifact record and consumers remain pinned until reviewed.' The two records carry different s
- **P-037** `gap:Lev` — The contract expressly provides for this: 'Materially changed bytes do create a new artifact identity' and 'Changed bytes receive a new artifact record and consumers remain pinned until reviewed.' The two records carry different s
- **S3-002** `event:israel.conquest.first-pasch-in-the-land#0` — Nothing is loosely named or uncheckable: the basis names "Josue 5:10-12" and the note names "Josue 4:19" and "Exodus 16:35" by exact locus, every quoted string is verbatim tracked Douay, the contract requires only that a claim "na
- **S3-004** `event:apostolic-age.jewish-revolt-against-rome#0` — The finding's load-bearing assertion is false: the 66 material from CE 08344a is held in the corpus as its own sourced dated claim, event apostolic-age.arrival-of-cestius-gallus-at-jerusalem, precision day 30 October 66, naming th
- **S3-009** `event:israel.primeval.creation#0` — Section 4.3 expressly permits precisely this: Ussher's figures may be reported where a ranked Catholic source prints them, recorded as that source's testimony - which is what the claim does, naming CE 03738a as the source of recor
- **S3-011** `event:israel.monarchy.temple-begun#6` — Section 11's "do not name a source loosely" governs source identity - work, edition, artifact and inspected locus - and the basis names all four precisely and quotes the sentence verbatim; "opens" describes where the article's his
- **S4-004** `unit:composition.book-of-sophonias#0` — The warrant the finding asks to be added is already the second half of the stored basis, quoted verbatim; the article's own opening line dates the writing to the same era; and "the article does not narrow further within the reign"
- **S4-009** `event:apostolic-age.council-of-jerusalem#4` — The disposition is semantically right and the finding's fix would be wrong: Galatians 2:1 is a rank-1 Scriptural relative offset that is not in the encyclopedia's four-way dispute over the year, so marking it disputed would assert
- **S5-003** `event:apostolic-age.saint-paul-first-visit-to-jerusalem#1` — Prat's own voice hedges the whole reconstruction - "as far as they may be assigned approximate dates ... give no precise results", a fixed point "not yet been indicated with certainty", and a table of "all certain or probable data
- **S5-005** `unit:composition.acts-of-the-apostles#0` — The finding's premise is false: the unit note already records Jerome's De viris illustribus 7 testimony and states exactly why it yields no authorable figure - it is a regnal reckoning with no A.D. year, and converting it would be
- **S5-009** `event:israel.exile.sedecias-reign#0` — Both prongs fail: the rank-1 eleven-year reign is already held and sourced to 4Kings.24.18 and Jer.52.1 in bindings.yaml, and the event note asserts no conflict at all - Meistermann's "succeeded his nephew" and the tracked Douay's
- **S5-010** `event:apostolic-age.saint-paul-first-mission#0` — Howlett declares in his own words that he cannot date the first journey, so the note's "gives no date for this journey at all" is precisely accurate and "beginning its own reckoning with the second" is true of the journeys he does
- **S5-011** `unit:composition.book-of-josue#1` — The contested phrase is scoped by its own sentence to what the article gives for the date of writing ("it prints no year of any era for it"), and the second figure is quoted in full in the sibling claim's note as "the theory of th
- **V-018** `exhaustive-coverage.verdict` — The defect it flags does not exist: the corpus already records exhaustive-coverage as OPEN for precisely the reason the finding gives, so there is no PASS verdict to correct and its recommended action is already discharged; the su

## Overall disposition

```text
CHANGES_REQUIRED
```

The audit directions make this mechanical: *one material factual defect is
enough.* After adversarial verification removed two in five raised findings,
**84 distinct defects survive: one critical, 42 major, 38 minor.** The load-bearing ones:

- **A materially false interval, in three claims.** The Flood-to-Abram figures
  367 / 1017 / 1147 are attached to Abram's **birth**. The encyclopedia's own
  table row that produces them is labelled *"Hence, number of years from Flood to
  Call of Abraham"*, and reaches them only after a row that adds Abraham's
  seventy-five years at his call; the Flood-to-birth row is 292 / 942 / 1072. The
  arithmetic settles it independently: the anchor event carries A.M. 1656, and
  1656 + 292 = 1948, the traditional A.M. year of Abraham's birth, while
  1656 + 367 = 2023, his call. Three auditors found it separately; two
  verification passes confirmed it; the claim's own note concedes the table
  "reaches Abraham's call" and keeps the birth anyway.
- **A prophet's lifetime promoted to a composition date, and preferred.** Jonas
  is dated 800–701 B.C. `preferred`, where the cited article gives no date for the
  writing and its only eighth-century figure is a hedged parenthesis — *"who is
  supposed to have lived in the eighth century B.C."* — inside a sentence whose
  main clause denies the book claims Jonah as its writer. The claim's own note
  concedes every element; the disposition contradicts the note.
- **Scripture outranked by a printing of Ussher.** At 4 Kings 24:12 — *"the king
  of Babylon received him in the eighth year of his reign"* — the query returns
  only "A.M. 3405 preferred", with no rank-1 claim authored, while the *first*
  captivity, from the same sentence of the same page, correctly has Daniel 1:1
  preferred above its A.M. figure.
- **Five anchors the evidence contradicts, still in production**, one of them a
  re-anchoring onto a second wrong anchor; and `israel.judges.period#0`, whose own
  subject note records that both figures the text carries are *durations*, stored
  `relative` with an anchor — §10.0 surviving the very 47-claim migration meant to
  catch it.
- **The declared universe is inflated by loci the witnesses do not print**, and
  the repository already holds the correct figure in two places while guidance and
  `PROJECT-WORK.md` hold the wrong one.
- **§15.1(1) has recurred.** The Crucifixion note quotes *"from the sixth hour to
  the ninth hour"* as Mark 15:33. No verse of the tracked Douay reads that. It
  sits between two quotations that are exact — which is precisely what makes it
  invisible, and precisely what §15.1(1) warns of.

None of this is a verdict on the project's ambition or on the profile it chose.
The model is sound and the distinctions §5 exists to hold are being held. The
Psalter rule is applied consistently in both directions. Ezechiel's inherited
scope is earned to the verse. All 47 duration migrations are correct. The
named-system architecture works as designed on four of its five criteria. Thirteen
of twenty gap rows are clean, and the evidence discipline behind the Genesis and
Numbers rows is better than most published apparatus. **The corpus is close.** It
is not yet a safe canonical dependency, which is the only question this lane was
asked.

### Promised deliverable — `scripture-chronology-corpus-2026-08-26`, `in_progress`

The ledger's three open requirements are still open, and this lane found no
discrepancy between the tracked state and the corpus.

| Requirement | Recommendation |
| --- | --- |
| `translation-independent-identity` | **KEEP OPEN** — four of five criteria independently confirmed; the §3.0 gate probes a span's first locus only, and the coverage view reporting the named-system universe counts verses no witness prints |
| `exhaustive-coverage` | **OPEN** — ten native loci carry a mapping word where a chronology status belongs, and no route exists by which a correction lane could author one |
| `independent-source-audit` | **KEEP OPEN** — this audit is that audit, and its disposition is CHANGES_REQUIRED |

This lane **recommends** and does not mutate. No requirement state, no chronology
datum, no guidance file and no test was edited.

### Next safe lane

A bounded correction lane addressing only the enumerated findings, in this order,
because the later ones depend on the earlier:

1. the critical and major factual defects, claim by claim from `cold-audit-findings.tsv`;
2. the anchor dispositions — the five still wrong and the two re-anchored wrongly;
3. the mechanical fixes — `_system_loci` over printed loci, the §3.0 gate over
   whole spans — and the guidance and `PROJECT-WORK.md` figures that follow;
4. a route by which a native locus can reach an authored gap row, **before**
   anyone attempts the ten;
5. the quotation and citation residues.

Then a targeted cold re-review of every changed claim and of any class the
corrections touch. **No merge and no propers integration is authorized by this
review lane.** Maintainer disposition follows the audit.

## What this audit did not do

- It did not change any chronology datum, code path, test, guidance file, or
  promise state. Every defect below is recorded, not repaired.
- It did not re-pin the stale source-family migration snapshot. That pin covers
  128 source artifacts; this audit reviewed the chronology corpus, which is a
  different question, and refreshing the pin would assert a review nobody has
  performed.
- It did not add chronology, integrate propers, or merge anything.
- It did not correct traditional dates because modern chronology differs. Under
  `catholic-traditional-v1` that divergence is a profile boundary, not an error,
  and the audit question was only ever whether the corpus encoded the tradition
  and its actual sources faithfully.

## Note on the ambiguous and anchor dispositions

The directions forbid the unresolved phrase "wrong anchor" surviving this
report, and forbid "ambiguous, needs disposition" as a disposition. Every
relative and duration claim in the corpus — all 217 — was inspected
individually rather than sampled, and each ambiguous case carries one of the
five named dispositions with the source wording that decides it. Those rows are
in `findings.tsv` under `audit_class` `A-duration-relative` and
`B-wrong-anchor`.
