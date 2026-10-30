# Independent cold review: packet 46 — Octobri Mense

**PASS: one Latin reader, all five pages freshly inspected.** The separate **EXTRA-RANGE OWNERSHIP/EXTENT decision is PASS** for restoring raw LF7848–7851 to this Octobri Mense selection. No blocker remains in this bounded review. This decision does not close the separately owned Duellorum correction, source admission, new rights clearance, installation or deployment.

## Exact reviewed state

Document `acta.ass.024.ass-024-005`, Leo XIII, 1891-09-22, *Epistola encyclica de Mariae Virginis Rosario*, Latin, five pages.

| Input | SHA-256 |
| --- | --- |
| Packet 46 | `fe356960eeaee4c57f11d7476d7a62671bd04c830e077752de50641bff0004c4` |
| Reviewer brief | `6a1aa4da7df4b21b53617a1065405644d5f3ae08fccb0e02adbbb3fbe08d221d` |
| Current PDF | `a4934ac07a28db2ca2caba177c55b55a594a729f90ed2cf852f5d638ef1f0c73` |
| Selected source | `3da7b523c3161cd6d05e6b186a17282bd3405751a9ca38353540b73d98fbb736` |
| Receipt | `7f4f3d82188d3d64390c9832c0af02b6c8cdda5f607c892a5d76fe2482ff2bc2` |
| Frozen manifest | `c237f87cf938c0bb74dfb0adbe72b1a6a0b8c6fa4a4ada9fe8fa90aa87406649` |
| Historical-text parent | `040fa780d381758f432e740ecfe4cee01143cc43aceb357677177ec4458a5215` |
| Whole native PDF parent | `82946251fed109b469f90a22ec02cd6b6f9fed1ff657b743e093afab3fbfc6b4` |
| Eleven-page native excerpt | `5f73cbb21b39469d36c7a95946c9a500c55121022e29bfe8ecc564f203d7e99d` |
| LF partition spec | `91b2937292394d197d7666a52be357b7d7a80d879006e3d150d3f2b3099913d5` |

The packet source row equals the matching frozen-manifest row in full and the proposed-current row. Controller and artifact TOML metadata equal the packet objects; payloads, helper paths and hashes, source pinset, receipts, native evidence, raster cache receipts and each listed output/cache file match. The current source schemas were also hashed. All 129 recorded file checks remained stable at final recheck; this count includes duplicate path checks and raster files. The PDF is 51,796 bytes and actually has five letter-size pages. Evidence: `pins.json`, `final-byte-check.json`, `pdfinfo.txt`, `pdffonts.txt` in this review directory.

## EXTRA-RANGE OWNERSHIP/EXTENT — PASS

I freshly viewed the native 193–203 contact overview and every native page 193–203 individually at original resolution. Native 193 identifies the Rosary encyclical and its Octobri mense incipit. The continuous Rosary body leads on native 202 into native 203. On 203 the body reference to earlier prescriptions and sacred indulgences ends with `(1)` at raw LF7811, at bbox y54.0849–62.8149. The closing blessing follows, then the dated Roman subscription at raw LF7832–7833 and `LEO P P . XIII.` at raw LF7835 (bbox y349.2849–358.0149).

An ornamental divider and a distinct heading about the German and Austro-Hungarian bishops and dueling start the following act. Its visible opening is raw LF7839–7846 and contains no note callout. The bottom `(1)` note at raw LF7848–7851 has bbox `[50.6, 499.089, 358.81577, 533.469]`. It cites *Supremi Apostolatus*, *Superiore anno*, *Inter plurimos*, and *Quamquam pluries*, the Rosary enactments relevant to the earlier indulgence reference. The matching callout, the note's content, the preserved Rosary closing, and the separate following-act boundary jointly establish positive ownership. Its physical placement below the following act's opening does not make it Duellorum's note.

The new specification has exactly twelve ranges: the prior eleven ranges unchanged, followed only by `[7848,7851]`. Independent direct byte accounting proves that all prior selected non-LF bytes remain in their original order as a prefix, followed by precisely those four added source lines. It excludes the interposed Duellorum heading/opening and ornamental furniture. No whole-old-selection byte equality is asserted: this is an explicitly enlarged selection. No Duellorum record was edited, reviewed for closure, or claimed complete.

## LF partition and note membership — PASS

The declared operation inserts empty LF records around raw LF7513–7515 and the restored LF7848–7851 note. The registered current `tools/papal-source-notes check` read-only replay passed, and an independent `derive` to this review directory reproduced the exact 26,112 bytes and 451 LF records. `scripts/_papal_source_notes.py` was used at its current pinned SHA `a0b31d45f498bec3a12a29cdff28da38f3e01cc02c50e5de8a9a65e4a82a9d57`; no helper archive was copied.

On native 195, the three small page-foot references at raw LF7513–7515 are visibly distinct from the preceding body. The current body TeX has explicit paragraph termination before and after them, and reader page 2 visibly sets the group as an indented paragraph before the resumed `affirmare` body. The restored terminal note likewise has its own paragraph after the separately terminated subscription on reader page 5.

All nine native note groups were inspected on native 194, 195, 196, 197, 199, 200, 201, 202 and 203. Each independently selected page-foot WORD region matches its exact raw LF note range when whitespace is ignored; actual word boxes and raw line hashes are retained in `note-geometry-evidence.json`. Existing note order and historical page-break positions remain. Literal damaged labels and numbering discrepancies remain disclosed; the review does not correct them or infer substitute anchors.

The existing whole parent was found at the source-pinset pointer and authenticated by hash. For all eleven parent pages 193–203 against excerpt pages 1–11, complete `pdftotext -raw` stdout bytes and the first page element from `-bbox-layout`, serialized with default ElementTree settings exactly as `NATIVE_PROOF_METHOD.md` prescribes, are byte-equal. Individual proof hashes are in `native-parent-excerpt-proof.json`; native203 context boxes are in `native203-line-geometry.json`. This authenticates the excerpt mapping, not an original-print facsimile.

## PDF visual decision — PASS

The current reader contact sheet and pages 1, 2, 3, 4 and 5 were freshly displayed individually using the original-resolution raster bytes, one image per call. No earlier visual acceptance or producer inspection was reused. `views.json` records actual observations.

The title, Leo XIII/date and Latin identification are clear. Two columns continue in ordinary reading order. Paragraphs and source notes remain separable; no clipping, overlap, lost glyph, or apparatus-only page was found. Page 5 contains substantial source text, the closing, dating clause, subscription and complete restored note, followed by the compact source notice and rights colophon under a rule. It is source-bearing and requires no sparse-page exception. The foreign Duellorum body is absent.

The retained OCR word spacing is conspicuous across all five pages, including split and letter-spaced forms. It increases reading effort but does not prevent reading the text or distinguishing the notes. Damaged wording and note labels remain source limitations, visibly disclosed in the terminal notice. This is a qualified acceptance of the mechanical reader, not lexical approval.

## Independent mechanical checks and limits

With `PYTHONDONTWRITEBYTECODE=1 TRIPTYCH_LIBRARY_CACHE=0`, current pinned `scripts/_typeset_papal.py` SHA `1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146` successfully ran `validate_document` and `pdf_body_fidelity`. Fidelity passed for the complete body, 21,289 normalized characters and 61 permitted layout hyphens, beginning on page 1 and ending on page 5. All four font subsets are embedded with Unicode mappings. Title, author, Latin subject and revision metadata agree with the frozen row; creation/modification timestamps correspond to its tracked revision. The existing compile log contains no overflow, undefined-reference, warning or fatal-error match.

The actual current whole-library `tools/source-library validate` was run uncached and returned exit 0: artifact=11108, corpus=5, edition=14304, passage=9532, segment=10882, work=10944, bindings=4398. Both environment variables were present for every Python import and source-library invocation in this lane; no shared cache was mutated, removed or restored. Exact command/output and independent results are retained in `verification.json` and `library-validation-final.txt`.

The source inspected is the identified Vatican archival OCR reconstruction. This bounded review establishes the repaired note membership, extent, LF partition, source order, mechanical PDF fidelity and every-page usability against those pinned bytes. It does not establish whole-original-print identity or lexical collation, translation accuracy, a new rights determination, general source admission, installation, or deployment. Only this assigned scratch directory was written. The canonical report target `src/sources/papal-documents/encyclicals-refinement-cold-46.md` remains unwritten for coordinator integration.
