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

The build figures below describe checkpoint `150a86200` and its frozen inputs.

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

## Containment and current-selection follow-up

The subsequent aggregate reached one missing containment edge for the new
historical English *Divini illius Magistri* witness. That exact constituent is
now registered under its existing journal container, with the 1930 issue,
printed pages, segment and source hash pinned. Two newly confirmed Bullarium
source-order failures are also explicit research holdings. All 192 container
pins and other entries remain unchanged. Containment now passes with 6,348
constituents; source-library and family checks pass without changing review
states.

All 507 earlier withdrawals are unchanged, and the negative inventory now has
509 exact current-reader withdrawals. The final long-token selection compiles
successfully with its own revision and full-source fidelity. The new plan has
5,825 successful PDFs across 11,696 pages, no missing or failed current builds,
and 712 exclusions. Page review and source-boundary corrections remain open.

After these repairs, `make -o check-act-history check-sources` passes.
Act-history freshness remains independently established by its exact owning
generator output comparison. This reports the source aggregate precisely;
it does not claim a full repository or deployment check.

## Initial installed release

The first scoped installation contains 424 exact reviewed PDFs and 1,338
pages: 391 Vatican Latin readers, 31 original historical English readers,
and Quanta cura/Syllabus as two separate constituents. The PDFs total
11,023,424 bytes. The release record is `release/papal-documents.json`,
SHA-256 `59a1b12085cefc428a44147bd0f48c7a22de594e758585c8ecf37c62147cd6cc`;
64 content-addressed metadata/report files retain its durable evidence.

All installed paths and PDF hashes pass the owning checker, and the installed
source rows remain valid against the later current plan. A separate comparison
proves all 424 selected rows and all 1,607 source dependency files match
published checkpoint `408070d3e`. The release's complete plan remains a frozen
snapshot; later changes to uninstalled families do not imply their acceptance.
No other historical family is installed by this initial release.

The installer preserves exactly the supplied review scope when replaying a
prepared transaction. Its additional scope regression and independent delta
checks pass. No source wording or existing PDF bytes changed during copying.

## Expanded scoped installation

The next scoped release contains 453 reviewed PDFs and 1,563 pages:
392 Vatican Latin readers, 59 historical English witnesses and the two
Quanta/Syllabus constituents. The PDFs total 12,462,192 bytes; the release record
has SHA-256 `2d092f6443cf1fb9868fd230aae693f46c371d3950d96f5e229bc560194b5dc5`.
All 424 previous PDFs remain unchanged; 29 additions contribute 225 pages.
The 86 content-addressed input/report archives pass exact-hash and private-path
checks. The owning installer check reports a valid release with every selected
reader current against its frozen source plan. Explicitly identified English
fragments remain fragments. No Bullarium, Acta or continuation reader is
installed by this scope.

The completed finite English review adds only the six-page Quinquagesimo ante
anno witness, bringing the installed set to 454 PDFs and 1,569 pages
(12,506,149 bytes). All 453 preceding PDFs and source selections remain
unchanged. The release record has SHA-256
`5b48e5f35a7e00402f1fe36769baf418ecd01aa4b603de56f3f30e51d8a63816`;
91 exact input/report archives preserve its evidence. English review now
covers 60 readers and 433 pages. The refreshed installation includes the new
global source corrections and withdrawals in its provenance without admitting
an Acta, Bullarium or continuation PDF.
