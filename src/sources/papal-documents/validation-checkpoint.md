# Papal source checkpoint, 2026-10-26

This source and tooling checkpoint leaves source corrections, individual
reconstruction and complete PDF review in progress. It does not declare the
historical corpus complete or approve a site deployment.

The Vatican inventory contains 2,814 index records. Acta contains 10,041
records: 2,634 registered complete printed witnesses, 7,314 metadata-only
records and 93 unresolved records, including the separately bounded surviving
Ad universam fragment. Its initial render selection contains 2,628 witnesses
in six languages. Index rows, historical witnesses and distinct acts are
different counts.

Source-library validation passes with 7,867 works, 10,662 editions, 9,736
artifacts, 7,099 segments, 8,786 passages and 4,231 bindings. Containment passes
for 162 containers and 4,688 constituent entries. Existing journal identities,
constituents and review pins are preserved. All 163 source-family review units
remain pending, with no admitted family records; refreshing the catalog pin
does not claim those units have been reviewed.

The regenerated browser projection contains 14,582 JSON files. Its existing
3,919 readable text payloads are byte-identical. Strict rights/model validation,
projection freshness and 31 focused reader tests pass. New holdings do not
automatically become readable browser passages. Casti connubii remains
restricted metadata with no passages.

Saved compilation results are initial, hash-specific batches:

| Batch | Successful PDFs | Pages | Remaining disposition |
| --- | ---: | ---: | --- |
| Vatican Latin | 392 | 1,140 | Source, metadata and layout replacements pending. |
| Historical English, encoding-repaired snapshot | 31 | 210 | Final all-page review reconciliation pending. |
| Quanta cura and Syllabus | 2 | 9 | All nine pages reviewed at their recorded hashes. |
| Bullarium initial complete-witness selection | 1,633 | 3,872 | One incomplete extent and language/layout findings require supersession. |
| Bullarium initial historical fragments | 28 | 69 | All pages reviewed; reader-apparatus replacements pending. |
| Acta initial attempt | 2,588 | 4,428 | Forty failed builds and additional long titles require separate correction. |

Compilation and source-to-PDF comparison do not establish print-image
collation, clean OCR, authenticated authorship or complete underlying act
wording. Initial receipts and PDFs remain preserved. Final selection must apply
exact supersessions and page-review evidence; a rejected or missing review
does not become a layout pass merely because a PDF exists.

Focused discovery, acquisition, rights, identity, export, typesetting,
collection and source-schema tests pass. Executed source-card and browser
collection checks are recorded in their owning reports. The collector verifies
local output hashes, frozen inputs, review reports and full page coverage,
and suppresses rejected PDF links.

An independent comparison against exact base commit
`d67e2259c3ee87cdd78608330b86e2c300443da6` found eight identical pre-existing
smoke failures: calendar masses, chronology preflight, promised-deliverable
installed-PDF evidence, document-library installed page counts, the Douay-Rheims
index, a mass-propers typed reason, public-alpha installed PDFs and the bound
Markdown package version. Mass-today and missal-coverage passed in both
snapshots. The task's containment omissions and stale source-family/source
reader projections were separately identified and repaired. Exact comparison
outputs are retained under `.scratch/core_review/baseline/`.

The aggregate source check initially stopped at act-history comparison
provenance drift. The owning generator has now refreshed exactly 31 comparison
records: 124 hash/size fields for the changed source-library and tooling
implementation. Deep comparison proves every other value unchanged. The base
check passes; this was a task-caused provenance update, not an inherited
failure. No clean result for every aggregate repository gate is claimed.

Post-1740 continuation volumes, Benedict XIV's Bullarium, Gregory XVI/Pius IX
Acta and additional historically printed English translations have separate
acquisition and boundary-review work. Possessing those inputs does not add
complete acts or readers to this checkpoint. The [coverage audit](coverage-audit.md)
records printing, extent, language and access gaps.

## Recovery integration checkpoint

The later source snapshot has 9,489 works, 12,362 editions, 10,025 artifacts,
8,761 segments and 8,793 passages. Its 49,435 canonical manifests retain the
same before/after byte fingerprint
`6948f8262ecddd29b1edbdb179a6f3c58818ef23b6f4f68d60def0f80537f26d`.
The source-reader projection now contains 16,282 files: 1,700 additions and
53 updates. All 3,919 existing readable payloads remain byte-identical; all
seven Casti artifacts remain restricted, with no reader text emitted.
Strict source-library, reader and freshness checks, both publication
inventories and 31 reader tests pass. The family catalog pin is current while
all 163 review units remain pending and no family or atomic-citation coverage
is asserted.

The current source plan selects 5,827 readers after 710 exclusions, including
507 confirmed source-order withdrawals. Exact frozen receipts account for
5,826 successful PDFs and 11,697 pages, plus one long-token layout failure.
An independently checked, source-preserving repair succeeds; its canonical
selection remains pending. Further sealed admissions and page reviews are
outside these frozen build counts. Visual audit reconciliation and first
installation remain in progress. A mechanical scan also found probable
modern-wrapper inclusions in continuation selections; those require source
classification and explicit correction before release acceptance.

The final focused source, geometry, acquisition, export, typesetting,
selection, collection and installation suite passes 374 tests. The registry
check and all 14 typesetter examples pass. Independent reproductions verify
the repairs for altered page-witness staging, lost reviewed discoveries,
collection input overwrites and interrupted installer writes. Source artifacts
and earlier PDFs remain preserved. Character geometry is a tested Python API;
its local demonstration does not admit a whole act or create an active reader.

The owning act-history generator refreshed 31 comparison records, changing
only 62 source-library implementation hash/size values. All other values and
the other 526 projection files are unchanged. The subsequent aggregate used
`make -o check-act-history check-sources`, with act-history freshness proved
separately, and stopped at the then-stale 1,753 reader projections. Those
projections are now repaired and checked independently. Later aggregate gates
were not reached; this checkpoint does not claim a complete aggregate pass.
