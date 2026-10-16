# Recovery of the earlier missal history corpus

Checked 2026-10-16. Paths prefixed `lt-hist:` refer to the independently retained predecessor corpus; other source paths are relative to Triptych. This report records filesystem inspection, existing project audit dispositions, and verified current Triptych commit identities. It does not revalidate historical or legal claims. No predecessor scripts or Git commands were run, and no source text was copied.

This is the recovery checkpoint, before the agreed-scope expansion on the same
date. Its measured counts and renderer limits describe that checkpoint. The
current catalogue, acquired witnesses, corpus export and rendered preview are
recorded in [the work register](../../../PROJECT-WORK.md#all-rite-missal-timeline-recovery-and-expansion-2026-10-16).

## What survives and how the two attempts relate

The predecessor `lt-hist` remains on disk. Its top level has no `.git` directory; `lt-hist:build/roman-liturgy-history/.git` exists as the generated research artifact. Its README, importer scripts, version metadata and section bodies were inspected. The original approach makes a linear, one-commit-per-version history, replacing each language tree or applying an explicit partial overlay. It shifts Git dates +10,000 years. Its outputs distinguish liturgy trees, source-text companions, and promulgation-only notes.

Triptych is the later, act-keyed successor rather than a second copy of that linear corpus. The source `src/sources/inventories/latin-missal-acts-v1.toml` explicitly identifies lt-hist OCR as evidence; `roman-holy-week-acts-v1.toml` supplies the base. Triptych replaces edition-only ancestry with cited acts, printed-station exceptions, several independent roots, parallel traditions, documented receptions and deterministic changes to identified liturgical units. Both the current interactive map and generated Git-history tool survive. Core generator/inventory/guidance files are byte-identical across the inspected sibling clones and backup snapshot; no restoration over the current files is needed.

The inherited text problem remains substantial. The predecessor has 140 Markdown section files across 25 version directories, but these are large raw OCR slices with `section`, `source`, `text_status`, `language` and `source_lines` front matter. The importer selects numeric windows: the 1570 Temporal is lines 20001–30324, Ordinary 30325–40000, and Canon 40001–50000. Actual body inspection confirms OCR, not a normalized prayer/formulary model. A named section is not proof its window matches the book’s structural boundary. No stable per-oratio identifiers, complete normalized formularies, or checked line-level collation was found in this predecessor structure.

Triptych improves the data model but remains a tracer: the Holy Week base has 38 units, only two with a nonempty `text` field and 36 carrying incipits; the Latin extension adds 15 incipit units and no full-text values. The two fields together contain 414 characters; their presence is not proof of complete prayers. All 53 base units retain an OCR-only review state. Its installed Latin graph has 59 stations on 17 lines, but claims no text units for the non-Roman uses and no complete Canon, chant or lectionary. Therefore neither surviving attempt is a complete normalized historical missal corpus.

## Exact predecessor version inventory

Counts and byte sizes below are measured from actual `lt-hist:versions/<id>/sections/**/*.md` files, including front matter. “Audit” is the existing Triptych audit verdict, not a conclusion from lt-hist’s self-declared public-domain labels. Source routes, paths and SHA-256 values are in [the metadata inventory](missal-timeline-recovery-files-v1.toml).

| Version ID | Sections | Section bytes | Actual stored state | Audit |
| --- | ---: | ---: | --- | --- |
| `1570-missale-romanum-latin` | 8 | 1,637,533 | raw OCR | admissible |
| `1604-missale-romanum-latin` | 3 | 2,025,476 | raw OCR | admissible |
| `1806-roman-missal-english` | 6 | 1,470,732 | raw OCR | admissible |
| `1843-roman-missal-english` | 8 | 1,722,800 | raw OCR | admissible |
| `1862-missale-romanum-latin` | 8 | 2,505,130 | raw OCR | admissible |
| `1920-missale-romanum-latin` | 12 | 2,919,877 | raw OCR | withdrawn |
| `1937-lasance-new-roman-missal-english` | 11 | 4,387,635 | raw OCR | admissible |
| `1955-holy-week-reform-source-needed` | 2 | 44,831 | companion/instrument OCR | undecided |
| `1962-missale-romanum-latin` | 15 | 2,791,264 | raw OCR | undecided |
| `1963-sacrosanctum-concilium` | 1 | 276 | metadata only | undecided |
| `1969-missale-romanum` | 1 | 357 | metadata only | undecided |
| `1969-ordo-lectionum-missae-latin` | 5 | 638,559 | companion/instrument OCR | excluded |
| `1970-general-instruction-order-of-mass-english` | 3 | 147,587 | companion/instrument OCR | excluded |
| `1970-missale-romanum-source-located` | 11 | 1,134,095 | raw OCR | excluded |
| `1972-nlc-interim-roman-missal-english` | 4 | 643,883 | companion/instrument OCR | excluded |
| `1974-sacramentary-english-source-located` | 1 | 305 | restricted-source note only | excluded |
| `1975-missale-romanum-editio-typica-altera-source-located` | 1 | 22,035 | partial OCR overlay | excluded |
| `1981-ordo-lectionum-missae-editio-typica-altera-latin` | 6 | 848,729 | companion/instrument OCR | excluded |
| `1985-sacramentary-english-source-located` | 1 | 305 | restricted-source note only | excluded |
| `1988-ordo-cantus-missae-editio-typica-altera-latin` | 7 | 303,502 | companion/instrument OCR | excluded |
| `1994-sacramentary-supplement-source-located` | 1 | 245 | restricted-source note only | excluded |
| `1998-icel-revised-sacramentary-source-located` | 4 | 4,480,683 | companion/instrument OCR | excluded |
| `2002-missale-romanum-editio-typica-tertia-source-located` | 11 | 1,322,332 | raw OCR | excluded |
| `2008-missale-romanum-reimpressio-emendata-source-located` | 1 | 285 | copyrighted-source note only | excluded |
| `2011-roman-missal-third-edition-english-source-located` | 9 | 1,995,778 | raw OCR | excluded |

Current measurement: 140 sections, 31,044,234 section bytes; 28 download files, 40,454,037 bytes; 31 source-manifest entries. The audit formerly counted 29 downloads; this inspection counts 28 and does not infer which old count or later change explains the difference. The 1894 Pustet download has no version row, so version count alone is not a full download inventory.

## Misidentification and rights boundaries already recorded

The owning record is `src/sources/inventories/lt-hist-rights-audit-v1.toml`: six admissible, one withdrawn, fourteen excluded and four undecided. Its five age-based admissible witnesses are 1570, 1604, 1806, 1843 and 1862; the Lasance witness is separately admitted on the recorded non-renewal basis with two lettered insert ranges removed. That Lasance artifact is identified in the later audit as approximately 1955–56 printing, not a 1937 printing. The 1862 is a concrete Pustet printing, not a typical edition.

The “1920” OCR was withdrawn: the audit identifies later additions and a post-1970 printing. Its filename and promulgation date cannot authenticate its printed contents. The 1962 row remains undecided in this audit; it names a particular IA item and explicitly refuses to equate it with another facsimile by title alone. Undecided status also applies to the 1955 AAS excerpt and the 1963/1969 instrument-only milestones.

Fourteen modern rows are excluded by that project audit; ten nevertheless have OCR section bytes in lt-hist. The other four are notes for 1974, 1985, 1994 and 2008. The 2002 source PDF physically exists at `lt-hist:sources/downloads/latin_missal2002.pdf`; a text-only copying assumption would miss it. The 1975 payload is merely the Ordo Missae partial overlay and cannot represent the full typical edition.

The predecessor README says modern English texts are absent, but actual 1998 and 2011 sections exist and have the measured sizes above. Its metadata labels are therefore unreliable as distribution authority. The audit specifically forbids transplanting `text_status`, source manifest, metadata JSON or section front matter, even for otherwise admissible material. It also forbids fetching, merging, cherry-picking, submoduling or subtree-merging the generated repository because historical objects would carry excluded bytes. This recovery did none of those actions.

## Verified Triptych recovery anchors

| Current commit | Evidence |
| --- | --- |
| `8c1ba03db47011c31eb54758cf7002a7da542ca9` | settled time-machine vision |
| `eda308a50f32e22974e471045b29edf5a615a016` | act-keyed station model |
| `b018cdeb5c849e44a7e838ad7e23504de5816fc4` | Holy Week tracer |
| `3fe07a52ff2192f4aeecbd08f4a1bf0c8f1ebe4a` | interactive history map |
| `744bffbc196c486b514243df3ba6c15ae7665279` | Latin Missal and parallel-use expansion |
| `1d6a020db6b35ebc233c3e60202ca75645785435` | printed-map DOT source |
| `387dec5f44f228c2b47b80c827c268e49b5aa4c8` | documented cross-line reception |

No predecessor commit IDs or tags are asserted: only its filesystem was inspected. The archived task journal records TASK-127 as queued and TASK-130 as blocked on written authority for replaceable, force-pushed derived repositories; these are historical task states, not current authorization decisions. The printed-map implementation emits DOT and apparatus but explicitly leaves label placement outside its current function, so a finished poster is not established by its existence.

## Safe continuation

1. Keep Triptych’s current act graph, provenance vocabulary, rights markers and generator as the starting point. Recover historical rationale from the cited commits rather than importing older branches over current files.
2. Use the metadata inventory as discovery input. Retain version, edition, printing, language, use, witness and act as distinct identities. Explicitly record unresolved ancestry instead of chaining books by date.
3. For already admitted witnesses, prefer Triptych’s fresh, registered acquisitions and corrected derivatives. The audit says all six surviving admissible witnesses were independently reacquired; raw predecessor imports are unnecessary for those bytes.
4. For additional witnesses, establish edition identity and permitted reuse before any named-file extraction. Discard predecessor rights front matter, retain acquisition hashes and locators, and register the independent basis. Do not copy excluded or undecided payloads by default.
5. Build actual normalized texts against page-identified witnesses, unit by unit, with verification and measured coverage. Treat raw OCR windows as finding aids, never as a checked minimal-diff corpus.
6. Expand catalogue coverage separately from text coverage, then derive Git histories, interactive maps and print outputs from the canonical evidence. Publishing or replacing generated repositories remains a separate consequential action.

## Reproduced engine and repaired comparison

The engine audit reproduced the Latin slice as 59 commits, 59 act tags and
17 branches. `git fsck --strict` passed. The slice contains 33 promulgated
and 26 printed stations, 15 roots, 45 edges, 43 witnesses, five Mass groups,
53 base units and 55 departures. Fifteen branch tips contain no liturgical
units. No tracked slice currently declares a cross-line reception.

The browser projection reproduces exactly: 505 files across three slices,
118 stations and 23 lines. Those totals include canon law and the overlapping
Holy Week tracer; they are not distinct missal-version counts.

The 1955 Holy Week station produces 38 changed files, 67 insertions and
83 deletions. Default Git rename detection finds six renames, including the
`Spiritum` reslot at 89% similarity. This verifies the stable-unit approach at
the tracer's limited extent, not the historical accuracy of every retained word.

The `commonality` command previously counted Mass headers and ordering files
as units. It now reports actual units and structural files separately while
preserving its original file-level JSON arrays. The Roman `typica` /
`usus-antiquior` pair has 18 identical and two differing units, with 11 units
only in the latter line; nine structural files agree and one differs. Five
new regression tests cover actual unit changes, empty lines, heading-only
changes, canon-law containers and CLI labels. Together with 56 existing
withholding, reception and projection tests, all 61 pass. The shell smoke
gate, registry check and exact projection check also pass. Fresh emission
retains byte-identical commit IDs and refs after this comparison-only repair.

Run from the repository root:

```sh
mkdir -p .scratch/recovery
tools/act-history check --source src/sources/inventories/latin-missal-acts-v1.toml --json
tools/act-history emit --source src/sources/inventories/latin-missal-acts-v1.toml --out .scratch/recovery/latin-missal --json
git -C .scratch/recovery/latin-missal fsck --strict
git -C .scratch/recovery/latin-missal show --stat act/maxima-redemptionis-1955
tools/act-history commonality --source src/sources/inventories/latin-missal-acts-v1.toml --repo .scratch/recovery/latin-missal typica usus-antiquior
tools/act-history structure --check
tools/act-history plate --source src/sources/inventories/latin-missal-acts-v1.toml --out .scratch/recovery/plate
```

`emit` replaces its named output directory on a rerun. The generated repository
is a disposable projection; do not import it or the predecessor's historical
objects into Triptych by fetch, merge, cherry-pick, submodule or subtree.
Only deliberate extraction of named working-tree files is an admissible
content-transfer route, under the owning source records. No generated history
was published or force-pushed by this recovery.

The `plate` command generated DOT successfully. No rendered printed map was
verified: the expected `octi` renderer is unavailable. The existing timestamp
scheme remains unchanged; its clone-local commit-graph setting does not travel
to downstream clones, so its previously recorded maintenance hazard remains.

## Visualizer repair and verification limit

The existing browser now distinguishes explicitly declared reception from
ordinary parent links, with a hollow connector, interchange ring and the
relationship's instrument, citation and basis. A geometric crossing or a parent
on another line alone does not become a reception. SVG station controls are
exposed as a group, and text-state labels identify recorded units rather than
complete missals. Shared ancestry alone no longer implies identical text.

Eighteen browser syntax, page-build and collision checks pass. The 22 existing
reception-generator tests pass, as does the directly invoked static map-label
assertion. A bounded independent code review found one stale label assertion;
that assertion and its explanation were corrected and the static method passed.
No corpus stations or historical reception claims were added by the UI repair.

The three new browser regression tests use the generator's explicitly
constructed reception fixture. All three attempts failed before browser
assertions because the environment denied the harness's local socket listener.
A direct Chromium startup was also denied a required socket operation before
opening a blank page. Consequently desktop/mobile rendering, keyboard behavior,
accessibility-tree exposure and forced-colors presentation remain unverified.
The patch is a candidate for those checks, not a visually accepted release.
No release bindings were refreshed and no website was deployed.

The complete `make check-sources` gate, `tmt check` and `git diff --check`
pass. The full promised-deliverables validator still reports 32 missing
installed-PDF findings from the checkout baseline. Comparing against the
unchanged baseline ledger and work register yields no new or resolved findings;
the overall ledger gate is not reported as passing.

## Expanded research, still distinct from acquired books

[Eastern research](eastern-eucharistic-books-timeline-v1.toml) adds 30
candidate records backed by 17 source records, with five further lead groups
and six access failures. [Western research](western-eucharistic-books-timeline-v1.toml)
adds 33 candidate records and 17 source records alongside the existing Latin
inventories. Candidate rows include translations, partial books, complementary
volumes and unresolved leads: 63 rows do not mean 63 distinct missal recensions.
Neither inventory is exhaustive or promotes its candidates to graph stations.
No new complete service books were acquired or collated in this research pass.

The [existing-text audit](missal-timeline-text-reuse-2026-10-16.md) identifies
1,068 reusable Latin proper bodies in the 1962 editorial projection, an
explicitly antecedent 1861 Cummiskey Ordinary, and 15 existing tracked OCR
artifacts representing 14 edition identities. All 15 artifact hashes match
their manifests. These holdings are considerably larger than the act-history
tracer, but none supplies a complete verified structured missal. They must not
be backfilled into earlier historical states by calendar inheritance.

Complete source authentication, the full historical inventory and normalized
full-text reconstruction remain outstanding. After this recovery checkpoint,
the maintainer agreed to the historical and language boundary recorded in
[time-machine §11](../../../guidance/time-machine.md#11-historical-and-language-scope-agreed-2026-10-16).
