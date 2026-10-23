Phase 3 V2 cold review, 2026-10-23. Disposition: ACCEPT for the bounded Propers/Catena presentation patch. The V1 hold for the clipped 80×24 author list is resolved. No remaining actionable finding was found in this changed scope.

Accepted proposal: `.scratch/resume-tui-design/phase3/v2/proposal.patch`, SHA-256 `22570c0b45a9546b2a9a0987fd1f5f7c8d2a3a2095fce46d5aed1b46c588f345`. It changes only the two TUI presenter files and adds the focused compact-reader regression test. The baseline presenter tree is ff07e4bd9e7d6377dbe841334483bf97ff4c62bc. The prior V1 hold, screenshots, signatures and evidence remain intact.

| Accepted postimage | SHA-256 |
| --- | --- |
| `scripts/lectern/surfaces/catena.py` | `8ddcc5713370e5767ae43dc69e653597d04c5ef98e79e48dff7a742febbc16f3` |
| `scripts/lectern/surfaces/propers.py` | `2af6664e8af8275d633ee45d5cb10d7d54773dd56996ed32a7f216996a36b95d` |
| `tools/tests/test_lectern_compact.py` | `4fb9047ab177e688d5f603d1ff51a79b5adbeb3c9fee591566211abfd0c8c628` |

The original Propers issue is repaired by removing the duplicate inline shortcut. The complete calendar names now fit in one row at 120/180 columns; the `c` binding, footer and help remain available. Actual 80/120/180-column runs preserve the selected reading and complete model/body contents while calendar browsing and search retain visible focus.

Compact Catena gives Scripture and chain 74 content columns instead of 27 and 43. The compact Enter hint explains how to open the held author and fragment. V2 also allocates remaining chain height to its list; only a compact surface below 27 rows suppresses the optional hint and reserves enough space for the chain/right column. The real 80×24 initial author list now occupies `[3,13,74,4]`, entirely within the same chain content rectangle; the unestablished-date heading and John Chrysostom are visibly drawn. The selected fragment's two-line extent/language/word-count row is drawn too. Focus mode and restore preserve that selection.

Independent verification:

- All four new compact-reader tests pass in 12.266 seconds in the isolated V2 candidate with bytecode writes disabled.
- The separate `exercise_short_v2.py` actual-key run passes nine checked states: initial author, selected fragment, both `f` transitions, resize 80×24 → 80×30 → 120×40 → 180×40 → 80×24, and return from Sources. Every focused list rectangle is within the chain's content. Enter opens the exact held fragment; n/p walks and restores both modal bodies; `s` opens the exact Sources passage and return to Catena retains the selected fragment. Text/SVG/geometry and stable Catena source hash are in `v2-short-runtime.{json,txt,svg}` and `v2-80x24.{json,txt,svg}`.
- The independent regular-height run passes Propers at 80/120/180 and Catena focus, Tab traversal, Scripture/acquisition scrolling, author/fragment navigation, resize, every declared voice, next Bible, next/previous chapter, and Source return. The paired V1/V2 results preserve all Proper view/body hashes, complete Scripture widgets, full acquisition notices, both fragment bodies, exact source destination, voice results, Bible/chapter results and recorded geometry (`v2-runtime.json`, `v2-comparison-and-pins.json`).
- All ten supplied V1/V2 short-terminal native Chromium PNGs were inspected, after the twenty original before/after images had been inspected. All nine regular V2 PNGs independently match V1 byte-for-byte, and all six regular geometry/body/location records match. This preserves the previously reviewed wide layout and fragment modals.
- The proposal, all three postimage pins and the owner's proposal receipt were independently checked. The 116 canonical reader/browser code pins were unchanged when checked before integration. No whole-data hashing or source-acquisition review was repeated.

The patch changes layout, a help sentence, and a UI instruction; it does not change adapters, formatters, shared browser renderers, canonical URL handling, dialogue-role policy, source availability, acknowledgement/refusal wording, or data. Exact source/notice/modal results were compared independently. Newly installed English source work and any subsequent generated-data or licensed-acknowledgement changes retain their separate review requirements; they are not accepted by this layout disposition.

Evidence and proposal hashes are recorded in `v2-final-manifest.json`. Root was told it may integrate this exact accepted V2 patch. This is an AI visual/code/interaction review, not human terminal approval or expanded whole-product/fidelity acceptance. This lane made no canonical source or index changes, commits or pushes; every new artifact is under its own phase 3 scratch directory.
