# Missal chronology cold review, 17 October 2026

The review concerns the corrected chronology at
`7fcf8aacb2db404d6910475c4ea30d226b13e2be`, delivered in
`20261017T034400Z-missal-chronology-cold-review`. It asks whether a reader can
follow the Roman, Ruthenian and Cistercian progressions in print and the live
timeline without inferring connections from proximity. It does not reopen the
all-rite census, acquire missing books or establish complete native texts.

**Recommendation: accept the three requested reader progressions.** Independent
print, live-browser and model review found no remaining reproducible progression
blocker. Final maintainer judgment remains distinct from this recommendation.

## Findings and corrections

One medium-severity validator defect was confirmed and corrected. Three
same-role documented states A [1400,1500], B [1000,1450], C [1100,1200], linked
A → B → C, passed the adjacent-bound checks even though no nondecreasing dates
could satisfy the whole path. The current dossiers contain no such path.

`verify_progression` now propagates the strongest feasible lower bound during
its existing topological traversal. Propagation follows documented edges with
matching date roles, including undated intermediates. Different-role and
provisional edges impose no date constraint. Authored dates remain unchanged.
The error names the conflicting source and target states. The regression covers
the impossible chain, a feasible equality case, an undated bridge, a different
role and a provisional boundary.

Independent reinspection found no defect in the correction. The new regression
fails against the frozen pre-fix implementation and passes after the change;
all 30 stage tests pass. An independent exhaustive-date-assignment oracle
agrees on 2,000 generated five-state DAGs, including convergence, duplicate
edges, equality, unknown dates and the two constraint boundaries. The oracle
reports 1,873 feasible and 127 infeasible cases. Inputs remain unchanged.

## Print recommendation

The focused print review supports acceptance of the requested progressions.
The reviewer opened nine chronology pages and nine evidence pages as actual
PDF rasters. The coordinator also inspected H002, H019 and H023.

| Sequence | Inspected sheets | Reader result |
| --- | --- | --- |
| Roman | H002–H006; evidence E098–E099 | T043 identifies the Venice 1570/Rome 1604 priestly blessing difference, retains the pontifical exception and uninspected Rome 1570 boundary. T044 states the issuing act's correction policy and its missing passage collation. The June/December 1962 distinction and onward H003 → H004/H005 → H006 references use explicit state and transition keys. |
| Ruthenian | H019 with H017; evidence E003, E070–E072 | Provisional T011, documented T012, reception T013 and witness-succession T014 are distinguishable. No link is invented across the 1733–1905 research gap. S024/H017 supplies an explicit off-sheet source for S030/H019. |
| Cistercian | H023; evidence E077–E079 | T022 supplies concrete before/after evidence between S043 and S044, with partial-text coverage and the bounded prayer/rubric collation stated locally. Institutional revision is separate from direct copying of the particular 1606 witness. |

Actual chronology PDF pages opened: 1, 5–9, 20, 22 and 26 (9 of 43).
Actual evidence PDF pages opened: 3, 70–72, 77–79 and 98–99 (9 of 153).
This focused pass is not a new visual inspection of all 196 pages. Native chart
sizes are A3 landscape/A2 portrait; the index and evidence companion are A4.
No physical printing or tagged-PDF accessibility review was performed.

An apparent H017 tick-label collision was investigated and rejected: a
150-dpi focused render and PDF bounding boxes show approximately 59 points
between the 1758 and 1759 labels. No renderer change was warranted.

## Live browser recommendation

The live Chromium review also supports bounded reader acceptance. Five named
lanes were exercised in chart and list modes at 1440 CSS pixels. Ten direct
stage selections at 393 pixels focused their evidence and returned by keyboard
to the exact control. Transition return, the June 1962 → 1970 cross-recension
link, browser Back/Forward and Cistercian comparison disclosure passed.

Reproduction routes relative to `/history/` include:

- Roman: `?view=timeline#stage=roman-stages-1604&presentation=list`,
  `#stage=roman-stages-1634&presentation=list`,
  `#stage=roman-stages-1962-june&presentation=list`,
  `#stage=roman-stages-1962-december&presentation=list`, and
  `#stage=roman-stages-1969-1970&presentation=list` (retain `?view=timeline`).
- Ruthenian: `?view=timeline#tradition=byzantine-ruthenian&presentation=list`
  and `?view=timeline#stage=byzantine-stages:ruth1942&presentation=list`.
- Cistercian:
  `?view=timeline#transition=cistercian-1606-1657-revision&presentation=chart`
  and `?view=timeline#stage=cistercian-1606-1657-1657&presentation=list`.

The first harness recorded 73 passing assertions and three failed zoom-setup
assertions: Chromium ignored a profile preference and remained at 100%.
Those three captures do not establish 400% behavior. A separate follow-up used
Chrome's own zoom setting and passed nine assertions: all three selected
traditions reported device-pixel ratio 4, a 360-pixel CSS viewport, and equal
356-pixel document client/scroll widths; exact keyboard return also passed.
Fresh screenshots confirm the enlarged headings remain readable.

At 320 pixels with 200% text, the page reflows without page-level overflow.
A suspected Cistercian heading crop was disproved by settled character-range
measurements and a fresh screenshot; the final letters wrap to the next line.
The chart has intentional internal horizontal scrolling and an explicit list
alternative. No browser product edit was required. Served HTML, CSS, JavaScript
and catalogue were bound by hash to the package and source.

This is history-preview acceptance, not full-site, spoken-screen-reader,
hardware-touch or complete WCAG acceptance. External source destinations were
not followed. The retained console log covers only the final initial-harness
session and contains a missing favicon; no whole-run console-clean claim is made.

## Model and evidence boundaries

All authored fields agree between canonical dossiers and the browser projection:
32 traditions, 127 sources, 97 states, 54 transitions and 78 gaps. The corrected
validator accepts all 12 dossiers and produces the same history object. T043
and T044 retain their distinct inspected-witness and act-described evidence
boundaries. Ruthenian 1940 publication, 1941 attestation/implementation and 1942
assembly remain separate; the Cistercian collation remains partial. This pass
checked internal consistency and declared evidence, not original-source
recollation or specialist historical acceptance.

## Verification

- Input transport: all 1,339 SHA-256 entries match; the ZIP's CRC, 1,340-file
  member set and every member's bytes match the directory.
- Focused regression: 223 tests run, 222 pass and one optional transport-parity
  test is skipped.
- `act-history structure --check`: 531 files current after refreshing 25
  comparisons. Only the validator's `byte_size` and `sha256` in `tool_inputs`
  change; all reader content is identical.
- `make check-sources`: passes. `tmt check`: passes.
- Fresh print build: all 196 SVG pages are byte-identical to the previous
  reviewed build; PDF differences are confined to trailer identifiers. The
  previously reviewed PDF bytes are retained.
- Browser HTML, JavaScript, CSS and catalogue remain byte-identical to the
  reviewed input package.

The full promised-deliverable ledger has exactly the same 32 missing
installed-PDF findings as the pre-change ledger, verified by byte comparison.
No new finding was added. Validating the exact review-deliverable entry in an
isolated ledger with `--require-complete` passes: one tracked, one complete.

## Disposition and delivery

Independent review, corrections and immutable transport delivery are complete.
The reviewed implementation is
`35864a63a486ce1a252c70487a68b991f81c2f26`, pushed to
`origin/feature/missal-timeline`. Its transport directory is
`.scratch/agent-handoffs/20261017T105920Z-missal-chronology-acceptance/`;
the sibling ZIP is
`.scratch/agent-handoffs/20261017T105920Z-missal-chronology-acceptance.zip`.
Both were created successfully. All 692 checksum entries match, and the
693-file ZIP passes CRC, exact member-set and byte-equality verification.
Its SHA-256 is
`23367c2ed023218e9212159971dce7a04e82b4a2e0ac08e91aa522b39523ffa6`.
The package preserves the reviewed commit's report; this later delivery record
closes that report's then-pending assembly step without changing the package.

The recommendations do not substitute for
final maintainer reader judgment. No newly discovered recension has displaced
the existing original-book collation priorities in this bounded review.
The broader historical catalogue, witnesses and complete texts,
continuous generated history, and map acceptance remain open under
`all-rite-missal-timeline-2026-10-16`.
