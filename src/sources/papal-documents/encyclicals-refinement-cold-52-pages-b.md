# Independent PDF subset review — packet 52, pages-b

PDF subset status: **PASS**. Whole PDF status: **UNASSIGNED**. Source intake status: **UNASSIGNED**.

This is the fresh pages-b observer under the explicit long-PDF role protocol. Assigned and actually inspected reader pages are **13–24**, twelve pages of the 24-page final PDF. Pages 1–12 have no individual visual judgment from this role. Contact-sheet thumbnails outside the assigned range do not establish coverage. No producer or other observer acceptance is inherited, and no prior visual review is reused.

Canonical subset report target (left unwritten by this observer): `src/sources/papal-documents/encyclicals-refinement-cold-52-pages-b.md`.

## Exact reviewed inputs

- Document: `papal.pius-x.hf-p-x-enc-19070908-pascendi-dominici-gregis.acqr-1907-english`; language `en`; title “Pascendi Dominici Gregis — damaged historical English witness”.
- Final PDF: `.scratch/pascendi-english-recovery/reader/1907-09-08-papal-pius-x-hf-p-x-enc-19070908-pascendi-dominici-gregis-acqr-1907-english-2d48437b-en/1907-09-08-papal-pius-x-hf-p-x-enc-19070908-pascendi-dominici-gregis-acqr-1907-english-2d48437b-en.pdf`; SHA-256 `06b622ef09fc4a907d3449bc089aff4ab8d5795ea90056bb901e6642a3f17fa3`; actual page count 24; size 158,499 bytes.
- Source text: `src/sources/works/journals/american-catholic-quarterly-review/editions/1907-volume-32/artifacts/boston-pascendi-english-319308afc17b/text.txt`; SHA-256 `319308afc17b723c6a47fd2d9cbd1a7e29f0222d85cfc0503c19d2adbfd4f144`.
- Receipt: `.scratch/pascendi-english-recovery/reader/receipt.json`; SHA-256 `97f7284878b54d68fa13cf20f7d4ef6785e24e7808d4d752ab36e4bab4051d40`.
- Frozen manifest: `.scratch/pascendi-english-recovery/reader/frozen-manifest.json`; SHA-256 `023162c76c565c90125cf437c20bca56c427d65404278cee3302cf932dad49dc`.
- Packet SHA-256 `72681fe09eefcf8b24c8f08f528f515daf1f052a9aada06b97015dafe6061217`; role-protocol SHA-256 `46d50e848afb908f9507ff30b68d382001f3a33a1d0294a87ba20a7c35bd7b5a`; generic brief SHA-256 `6a1aa4da7df4b21b53617a1065405644d5f3ae08fccb0e02adbbb3fbe08d221d`.

Hashes were independently checked before inspection and rechecked at completion. The exact packet source row equals its matching frozen-manifest row. Receipt PDF/source/page-count pins agree. Selected source/controller/artifact and current helper pins match. Both contact sheets and each assigned page/thumbnail match the pinned output and cache-copy hashes, PDF identity, renderer fingerprint and cache key. No raster was regenerated or shared cache altered.

## Actual visual evidence

Both contact sheets were opened, then each page 13–24 was opened individually using `tools.view_image(detail="original")` and displayed with `image(detail="auto")`, one image per call. Each image path, SHA-256, actual view method, time, finding and verdict was persisted immediately after its view in `page-observations.json`. Every individual raster is 1700×2200 pixels. The evidence file records the exact twelve page pins and the two overview pins.

| Reader page | Result | Direct observation |
| --- | --- | --- |
| 13 | PASS | Historian/critic continuation; attached criticism heading; clear columns. |
| 14 | PASS | Bible-criticism heading attached; continuous sentence and column joins. |
| 15 | PASS | Apologist heading attached; normal flow and intact edges. |
| 16 | PASS | Subjective-arguments and reformer headings attached; OCR blemishes remain legible. |
| 17 | PASS | Heresies heading attached; coherent column join and even leading. |
| 18 | PASS | Cause-of-modernism and propagandism headings attached; literal OCR part label retained. |
| 19 | PASS | Propagandism continues coherently; dense quoted text remains legible. |
| 20 | PASS | Remedies transition and first remedy fit; literal OCR numeral/punctuation retained. |
| 21 | PASS | Second/third remedy headings and following paragraphs stay together. |
| 22 | PASS | Censorship/editors headings attached; no body/reference collision. |
| 23 | PASS | Congresses/watch-committee headings attached; continuous quoted directions. |
| 24 | PASS | Seventh remedy, true closing/date/subscription and separated terminal apparatus all fit. |

No material layout blocker was found in the assigned subset. Roman body text, leading, column gutters and folios remain readable. Headings have following text; no clipped lines, glyph boxes, overlap, fused note blocks or apparatus-only spill was observed. Successive page and column transitions were directly checked within the assigned range. No claim is made for the page 12/13 visual boundary.

Page 24 contains substantive source text in both columns: continuation of remedy VI, remedy VII, the closing exhortation and apostolic benediction, the St. Peter’s/Rome dating clause for 8 September 1907 (fifth pontifical year), and `PIUS X., POPE.`. A short rule separates the smaller Source apparatus. Its damage/OCR limitations and the compact common license-boundary colophon are legible. This is a source-bearing final page, with no further apparatus-only page.

Literal OCR defects remain visible, including broken word divisions, stray punctuation and imperfect heading numerals. Direct source-byte checking confirms `PART I.` twice and `PART Il. REMEDIES.` (capital I, lowercase l). These were preserved rather than repaired by the typesetter. They qualify text quality; this PASS does not assert corrected wording or canonical numbering.

## Independent mechanical verification

Fresh uncached `validate_document(source_row, root=repo)` and `pdf_body_fidelity(pdf, validated, 24)` used the exact current `scripts/_typeset_papal.py` SHA-256 `1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146`. Fidelity PASS: 127,960 source characters, 105,911 normalized characters, 200 permitted layout hyphens; source begins on page 1 and ends on page 24. This verifies content-stream source order for the complete selected text, without extending this role’s visual coverage.

`pdfinfo` confirms 24 unencrypted letter pages, PDF 1.7 and expected title, Pius X author, English subject and render-revision timestamps. `pdffonts` reports all four Latin Modern fonts embedded, subset and Unicode-mapped. `pdfinfo -f 1 -l 24 -box`, source-fidelity extraction and `pdftops -level3` parse the page tree/content/resources successfully. `qpdf` is unavailable, so no qpdf result is claimed. The PDF is untagged; no PDF/UA conformance is asserted. Exact commands, exit statuses, metadata and bounded logs are in `verification.json` and the named adjacent logs.

## Limits and disposition

This PDF presents a **damaged historical English witness** with disclosed printed p. 705 damage and ordinary uncorrected OCR. It cannot establish complete-act English coverage or a fully image-collated edition. Page 24 visibly discloses this limit. This role did not inspect native historical source images, replay the expensive source OCR package, determine historical intake/rights, or perform lexical collation. Those decisions belong to the separately assigned source role. Selected-document validation does not grant new rights clearance.

The subset is ready for coordinator assembly only with the disjoint actual pages 1–12 observer and the separate source-intake judgment on the same PDF/source/receipt pins. Whole-PDF visual acceptance, source intake, installation and deployment remain outside this report. Only this observer’s scratch directory was written; the canonical report target remains unwritten.
