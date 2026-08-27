# Post-audit correction report — Scripture chronology corpus

```text
audited corpus:            2330d63a5
cold audit artifacts:      src/sources/chronology/cold-audit-report.md
                           src/sources/chronology/cold-audit-findings.tsv
                           (unchanged by this lane)
correction starting HEAD:  9d3dd2fc0   the commit that added those artifacts
correction final HEAD:     15213f79ca956f11ec8fb0844c6d25ec418af34a
```

The cold independent source audit of `2330d63a5` returned `CHANGES_REQUIRED`:
104 standing findings over 84 distinct defects — one critical, 42 major, 38
minor — after two in five raised findings had already been refuted by its own
adversarial verification. This lane consumed all 104.

## Dispositions

| | |
| --- | --- |
| standing findings | 104 |
| fixed | **96** |
| withdrawn after new evidence | 8 |
| blocked by source | 0 |
| left to maintainer disposition | 0 |
| unresolved | **0** |

By severity: 5 critical, 50 major, 49 minor —
of which 5 / 46 / 45 were fixed outright.

The eight withdrawals each rest on evidence stronger than the audit's, and each
names it in the ledger. Three (`V-008`, `V-012`, `V-013`) are loci that do not
exist: the World English Catholic witness prints no Esther 4:6, 9:5 or 9:30, and
they entered the universe only through the enumeration defect the audit itself
identified in `V-014`. Three (`LEAD-001`, `LEAD-002`, `P-012`) are one
misquotation found by three auditors and corrected once. One (`F-021`) is the
duplicate-artifact charge, which `guidance/sources.md` settles against the
finding — *"Changed bytes receive a new artifact record and consumers remain
pinned until reviewed."* One (`A4-017`) asked for a shape the closed `PRECISIONS`
vocabulary does not hold.

## The critical defect

The Catholic Encyclopedia's Flood-to-Abraham table totals 367 / 1017 / 1147
under a row it labels **"Hence, number of years from Flood to Call of Abraham"**,
reached from the row above by *"Add for age of Abraham at time of his call: 75"*.
All three sat on Abram's **birth**, overstating every one by exactly those
seventy-five years, and reading perfectly. The anchor settles it without appeal
to the label: the Deluge is held at A.M. 1656, and 1656 + 292 is the traditional
year of the birth while 1656 + 367 is the call.

The three are now alternates on `israel.patriarchs.call-of-abram`, beneath the
rank-1 Genesis 12:4 claim that outranks them and does not disagree with them —
that one measures the call from the birth, these measure it from the Flood.
Birth and call remain two events. The regression test asserts the shape rather
than the years and is verified to fail against a corpus with the old anchor
restored.

## The two architecture defects

**The §3.0 gate proved something about verse one.** It probed `span.first or 1`,
so a native span whose opening refused the concordance was admitted entire
however its interior behaved. It now walks every locus the witness prints inside
the span. It also asked the wrong question of the locus it did check:
mappability was standing in for duplication, and the two come apart at greek
Ecclus 36:16, where the fact authored natively is the date of the *Greek
translation*, which the Vulgate unit does not hold and could not. The gate now
asks the module that owns each system which kind it is — a psalter renumbering
is one psalter under two numbers and may never date natively where the
concordance carries; a witness to another text may, unless it would restate a
claim the preferred locus already holds. A successful mapping no longer discards
a native assertion.

**A mapping word stood where a chronology status belongs.** Ten native loci
answered `textually-distinct` to "is this dated?" with no route to anything else,
because `_native_assertions` reads only units and bindings, the gap loop sits
downstream of a successful conversion, and `_scope` refused every scope naming
`EsthGr` — a book the Greek witness prints and `_canon` has no row for. Native
scopes are now bounded by their own witness, an unmappable locus consults native
gap rows and otherwise reaches §9's honest default, and the CLI keys its exit on
whether it got chronology rather than on which kind of nothing it got. Three of
the ten were never loci.

## Coverage, recomputed

| Vulgate/Clementine primary | at 2330d63a5 | now |
| --- | --- | --- |
| total | 35 809 | **35 809** |
| dated | 12 406 | **12 541** |
| composition-only | 16 687 | **16 504** |
| undated-in-tradition | 6 716 | **6 764** |
| research-pending | 0 | **0** |
| direct-only / inherited-only / both | 3 646 / 7 354 / 1 406 | **3 610 / 7 526 / 1 405** |
| multiple relations | 7 944 | **7 882** |
| alternatives | 12 897 | **13 776** |

| Additional native | printed | shared | already counted | additional | statuses |
| --- | --- | --- | --- | --- | --- |
| `greek` | 2 156 | 800 | 0 | **1 356** | 1 355 composition-only, 1 research-pending |
| `hebrew` | 2 528 | 2 528 | 0 | **0** | wholly shared |
| `world-english-catholic` | 2 094 | 730 | 1 358 | **6** | 6 research-pending |

Declared universe **37 171**, down from 37 209 — and 37 171 is the figure this
repository already held in `_chronology`'s own docstring and in `composition.yaml`.
`septuagint`, `nova-vulgata` and `nab` are now reported `enumerable: false`
rather than omitted, as §9.3 requires. **No locus anywhere answers a mapping
word to a chronology question.**

The Vulgate movement is entirely accounted for: Jonas's 48 verses from
composition-only to undated-in-tradition when its composition unit was withdrawn
for typed silence, Osee re-authored as `prophecy-given` over the book, Micheas
4-5 losing a binding whose only warrant was composition evidence, and the verses
narrating Saul's accession falling back to their book's composition chronology
when the modern reconstruction that was the profile's only answer for it was
withdrawn.

## Promise state

The deliverable remains `in_progress`, and all three requirements remain open.

- `translation-independent-identity` — **READY_FOR_REREVIEW**. All five criteria
  hold, the fifth for the first time. This lane authored the corrections and may
  not accept its own work.
- `exhaustive-coverage` — **still open**, now for a reason its own criterion
  names rather than for a defect: seven native loci are `research-pending`
  because no ranked source has been inspected for them, and this lane invented
  no date to close them.
- `independent-source-audit` — **open**. An author correcting findings is not an
  independent acceptance.

## Left to the maintainer

`israel.monarchy.temple-begun#5` still carries Howlett's 958 B.C. as an
`alternate` beneath rank-1 Scripture. It comes from the same sentence as the
1277 B.C. Exodus figure and the 1020 B.C. Saul figure this lane withdrew as
modern-critical, and consistency may want the same treatment. But a cold auditor
examined this claim and passed it, and its position under a rank-1 `preferred`
claim is materially different from theirs. It is row `RR-092` of the re-review
manifest rather than a unilateral withdrawal.

## Artifacts

| Path | Rows |
| --- | --- |
| `src/sources/chronology/post-audit-corrections.tsv` | 104 — every standing finding exactly once |
| `src/sources/chronology/post-audit-rereview-manifest.tsv` | 92 — every changed claim, scope, gap row and hard case |

The re-review manifest is derived, not sampled: it is the diff of the loaded
corpus at HEAD against the loaded corpus at `2330d63a5`, plus the architecture
and hard cases named by contract. The next cold reviewer inspects 100% of it.

## What this lane did not do

No new population. No propers, Catena, web or PDF integration. No merge. The two
cold-audit artifacts are unchanged. The stale `source-family-migration` pin is
not refreshed — this lane reviewed chronology, which is a different question, so
it discharges nothing there.
