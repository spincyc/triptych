# Low Mass fidelity review — 2026-11-08

**Result: accepted for the exact worktree proofs below, with no unresolved
review finding.** This is a fresh review of the Low Mass corrections, based on
HEAD `a3ca7d224295ceb1c5eaad5c94b609fd34fa63d1` and the current source changes.
The 2026-11-07 expansion approval was not carried forward. Both PDFs bear an
uncommitted-source revision stamp; this record does not approve later rebuilt
bytes or deployed output.

## Exact proof identities and inspection extent

| Proof | Pages | Bytes | SHA256 |
| --- | ---: | ---: | --- |
| Child, `01-low-mass--16e8efc97738b101.pdf` | 44 | 8745169 | `22cda6bca52a3d68761720ad190d7d9b1cd87897e112432995f6df7f15837bfe` |
| Trainer, `01-low-mass-trainer-manual--7ac6525bb427ae12.pdf` | 44 | 8767988 | `6f9108383e1c3a01420481be4355aabab288179f8937bded2f486bf447005e1e` |

The independent reviewer personally inspected all 44 child candidate pages
individually at original raster resolution, with a 2200-pixel maximum page
dimension. Candidate PDF SHA256 was
`edad1e89df87d8e7f54f6959e8775dfa3c47d84b357db6d402262063a5976860`.
For the final child proof, pages **22, 23, 28, 32, and 44** were personally
reinspected. Independent recomputation of all 44 PNG hashes confirmed that
the other 39 pages were byte-identical to the reviewed candidate pages.

The guide owner independently reports individual full-size inspection of all
44 trainer candidate pages, followed by direct inspection of the same five
changed final pages and exact PNG identity for the other 39. This is attributed
coverage, not the independent reviewer's personal inspection. The parent
reviewer additionally inspected trainer pages **15, 16, 20, 22, 26, 27, 33, 34,
35, 40, and 41**, then rechecked final page **22** and accepted the corrected
foot support. The independent reviewer personally inspected final trainer
pages **7, 8, and 24** to resolve text-extraction exceptions.

All 13 final isolated drawings, **ASG-ART-039–048 and 050–052**, were personally
inspected at original resolution, including the final normalized 041 and
revised 043–045. Their exact identities and provenance are recorded in the
[artwork manifest](../../../src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/research/artwork-manifest.md).
The artwork receipt hash below binds the reviewed set without duplicating its
individual asset table.

## Corrections verified in the actual pages

| Area | Final result and relevant child pages |
| --- | --- |
| Arrival and departure | The priest carries the covered chalice; arrival, facing the altar, and reverence are distinct actions. Carried-object continuity is visible on 3, 41, and 42. |
| Gospel | Second remains on the floor; First waits at the Gospel opening station until the reading begins, then returns to his normal floor place. The book route and centre marker agree with the instructions on 14–16. |
| Offertory and cruets | First's rise, veil receipt, securing it, and rejoining Second are explicit on 18–19. The handle points toward the priest; the kiss meets the lower handle attachment, clear of the spout, on 20–21. The waiting wide view precedes the handoff detail, so these are expressly successive moments. |
| Lavabo | Water, bowl, towel, hands, and role assignments agree. Final 22 moves the whole group inward so First's outer shoe is supported by Step 2. The change preserves the group’s hand relationships. |
| Elevations and return | Host and chalice grips, hem support, bell hand, and facing are consistent on 26–27. Final 28 explicitly carries the bell back without ringing and sets it on Step 2; the labelled station matches the subsequent joined hands. |
| Initial purification | On 33, priest and First stand on the predella and the priest holds the chalice. First retains the waiting water cruet while pouring wine; the rejected empty-hand candidate is absent. |
| Finger ablutions | On 34–35, the priest remains on the predella and First stands one step below at the Epistle side. The chalice rests on the altar, wine precedes water, and the wide views and details use the same action artwork. Revised ledge geometry fits the fixed altar surface, without introducing a second lower altar. |
| Subsequent movements | Final 32 explicitly tells Second to rise when First leaves for the cruets, accounting for his standing wait before the later book move. Book and veil routes and finish states agree on 36–37. |
| Last Gospel | The priest faces left on 40, with the servers and their movement instructions consistent with the selected model. |
| Legibility and flow | Final 23 moves the ARTICLES RESET label clear of the centre marker. Across the reviewed pages, no remaining clipped label, unreadable caption, orphaned action caption, or conflicting altar architecture was found. |

The unused one-cruet ablution-wait draft was removed. It cannot now imply that
First has lost the second cruet. Neutral standing figures identify waiting
stations; the action drawings supply the specified handwork. No remaining
isolated anatomy, contact, object-continuity, or step-level contradiction was
found in the reviewed uses.

## Source checks, parity, and limits

The independent reviewer read the current server-training profile, the source
auditor's decisions, shared scene/diagram source, changed ceremony sections,
and relevant inventory rows. A personally viewed primary-source raster of
Missale Romanum, printed page LVII, confirmed the stale LM-017 citation:
Low Mass Gospel material belongs to VI.1–2; VI.4 begins the Solemn Epistle
material. The inventory citation was corrected accordingly.

The broader fresh facsimile collation belongs to the source auditor. Its
distinction between freshly checked sources and the earlier, unrecovered
Laurence J. O’Connell allocation check is retained in the
[fidelity record](../../../src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/research/low-mass-fidelity-2026-11-08.md).
This review checks consistency with that selected teaching model; it does
not claim a fresh independent collation of every ceremonial source.

Both editions have 44 pages. The guide owner's comparison checks per-page
normalized word multisets in the main text regions, not ordered text equality.
Its only differences were full-width continuation headings on pages 7, 8,
and 24 that cross the trainer extraction boundary. Personal full-page
inspection confirmed those headings are present. The common ceremony source
also keeps the action sequence shared. The guide owner reports six passing
Low Mass model tests, both content schema checks with `--phase content
--run-gates`, and successful native builds without overfull or underfull
diagnostics.

This is screen-proof acceptance. There was no physical printing trial or live
site/browser review in this lane. Generated pictures remain instructional
illustrations. Genuflections, bows, and adaptation to an actual sanctuary
still require rehearsal; the station figures do not claim to depict every
intermediate body position.

## Evidence binding

All paths below are repository-relative. Scratch evidence is transient; the
identities and extent above are retained here, with canonical production and
artwork records in the source tree.

| Evidence | SHA256 |
| --- | --- |
| `shared/low-mass-ceremony.tex` under the altar-server-guides source root | `1420500a9bb475c70c842ee71788a371b0bc07f8b998180d10db4497921ebf51` |
| `shared/low-mass-diagrams.tex` under the same root | `66b6fd878dba2234cd33d145ed044f2e10db963c8d36ad5df82a50d946969aec` |
| `.scratch/low-mass-fidelity/artwork/final-assets.json` | `01d828ee23f2585f0b1b122e130a99e1e7f9c6dfb52d49371da58a1591c45ae1` |
| `.scratch/low-mass-fidelity/review/child-final-visual-review.json` | `ccf07f9143139748651f499b061c2cff574cdc17b3ac00816dd82f3505c6d915` |
| `.scratch/low-mass-fidelity/guide-layout/proof-transfer.json` | `d86b2556957f6eeb05b6356d2b0927d9645eeb13254787221468211a4b6c9ab1` |

Final PDFs and canonical `.print.json` receipts are in
`.scratch/low-mass-fidelity/guide-layout/final-01-low-mass/` and
`.scratch/low-mass-fidelity/guide-layout/final-01-low-mass-trainer-manual/`.
Per-page hashes are retained in the review receipt; the trainer coverage and
source hashes are also recorded in `guide-layout/guide-layout-review.json`.
