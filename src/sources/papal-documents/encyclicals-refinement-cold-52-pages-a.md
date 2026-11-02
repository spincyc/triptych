# Pascendi independent reader subset review: pages-a

Role: **pages-a**. Assigned and actually inspected reader pages: **1–12 of 24**, each opened individually at full resolution. `pdf_subset_status: PASS`; `whole_pdf_status: UNASSIGNED`; `source_intake_status: UNASSIGNED`.

This is a mechanical edition of a **damaged historical English witness**, not complete-act English coverage. No producer acceptance is inherited. This report approves only the assigned rendered page subset and does not establish translation accuracy, lexical collation, historical-source identity, rights clearance, installation, or deployment.

## Exact reviewed inputs

| Input | SHA-256 |
| --- | --- |
| Final reader PDF | `06b622ef09fc4a907d3449bc089aff4ab8d5795ea90056bb901e6642a3f17fa3` |
| Selected source text | `319308afc17b723c6a47fd2d9cbd1a7e29f0222d85cfc0503c19d2adbfd4f144` |
| Typesetting receipt | `97f7284878b54d68fa13cf20f7d4ef6785e24e7808d4d752ab36e4bab4051d40` |
| Frozen manifest | `023162c76c565c90125cf437c20bca56c427d65404278cee3302cf932dad49dc` |
| Packet 52 | `72681fe09eefcf8b24c8f08f528f515daf1f052a9aada06b97015dafe6061217` |
| Long-PDF role protocol | `46d50e848afb908f9507ff30b68d382001f3a33a1d0294a87ba20a7c35bd7b5a` |
| Current `scripts/_typeset_papal.py` | `1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146` |

PDF: `.scratch/pascendi-english-recovery/reader/1907-09-08-papal-pius-x-hf-p-x-enc-19070908-pascendi-dominici-gregis-acqr-1907-english-2d48437b-en/1907-09-08-papal-pius-x-hf-p-x-enc-19070908-pascendi-dominici-gregis-acqr-1907-english-2d48437b-en.pdf`. Actual page count is **24**; byte size is **158499**. Source: `src/sources/works/journals/american-catholic-quarterly-review/editions/1907-volume-32/artifacts/boston-pascendi-english-319308afc17b/text.txt`. Receipt: `.scratch/pascendi-english-recovery/reader/receipt.json`. Frozen manifest: `.scratch/pascendi-english-recovery/reader/frozen-manifest.json`.

The packet source row equals the matching frozen-manifest row in full. Receipt PDF/source/page-count/manifest bindings match. All 53 recorded pins, including source controller, retained recipe/replay inputs, current helpers, renderer receipt, contact sheets, and assigned output/cache rasters, matched their exact hashes and sizes and were rechecked after visual inspection. Cache renderer fingerprint `cb6bc6758b165c50bba7f68d7b5e1df5cc66fa3e0aad97361992b67d97cea2ba` binds the same 24-page PDF; no raster generation was rerun or cache mutated.

## Actual visual inspection

The pinned `contact-sheets/sheet-001.png` overview was opened. It contains thumbnails 1–20; only assigned pages 1–12 were judged, and pages 13–20 receive no acceptance from appearing there. Each page 1–12 was then opened separately using `tools.view_image` with `detail=original`, forwarded as one image with `detail=auto`. Every actual page observation, image path, image SHA-256, view method, finding, verdict and timestamp was persisted immediately after that view. There is no prior-review reuse.

| Reader page | Verdict | Direct finding |
| --- | --- | --- |
| 1 | PASS | Title, English/date/issuer, source address and salutation fit; damaged opening remains visible. |
| 2 | PASS | Division/Part I and philosophy headings remain attached; column and page continuation fit. |
| 3 | PASS | Religious-history heading fits; literal yen-like OCR mark remains legible. |
| 4 | PASS | Dogmas/evolution headings fit; literal OCR anomalies remain. |
| 5 | PASS | Believer heading retains following lines; two-column continuation fits. |
| 6 | PASS | Tradition and faith/science headings fit; literal Zaitn ana OCR phrase remains. |
| 7 | PASS | Theologian heading fits; source block split modern-/ists and inline Methods heading remain literal. |
| 8 | PASS | Dogma/sacraments heading and paragraphs fit in continuous column order. |
| 9 | PASS | Scriptures/Church headings and inline citation fit; continuous column order. |
| 10 | PASS | Church/state and magisterium headings fit; Latin potes-/tatem continues across columns. |
| 11 | PASS | Evolution heading and dense paragraphs fit; continuous column and page order. |
| 12 | PASS | Historian/critic heading fits; page-end continuation beyond the subset remains unassigned. |

The title visibly identifies the damaged historical English witness and directly gives Pius X, 1907-09-08 and English. The source title, full episcopal address and papal salutation remain visible. Normal left-column to right-column flow and successive-page continuity within pages 1–12 were checked. Roman typography, source headings, indentation, citations and bottom lines are legible; no clipped body, line overlap or missing-glyph boxes were observed. No material layout blocker was found.

The substantive duplicated/substituted line and broken continuation from printed p.705 remain visible in the opening. Literal OCR spelling, punctuation, source word divisions and some awkward retained paragraph boundaries remain elsewhere. These are qualifications of the declared damaged OCR witness, not a claim of repaired wording. Nothing in this review supplies missing words or treats it as complete English coverage.

## Independent mechanical checks

Using `PYTHONDONTWRITEBYTECODE=1 TRIPTYCH_LIBRARY_CACHE=0`, the current pinned helper was imported and `validate_document(source_row, root=repo)` followed by `pdf_body_fidelity(pdf, validated, 24)` was run independently. Result: **pass**, method `pdf-raw-source-aware-line-hyphen-nfkc-v3`, 127960 selected source characters, 105911 normalized characters, 200 allowed physical line-end layout hyphens, source-bearing extent pages 1–24. This verifies mechanical text fidelity and does not visually approve unassigned pages.

`pdfinfo` and `pdffonts` exited 0. Metadata identifies the correct title, English and Pius X. Creation and modification timestamps both equal the tracked render revision `2026-10-30T13:40:55Z`. All four Latin Modern fonts are embedded subsets with Unicode mappings. The unencrypted, untagged PDF is 612 × 792 points. Ghostscript parsed and processed all 24 pages with its nullpage device and `-dPDFSTOPONERROR`, exit 0 and no diagnostics. `qpdf` is unavailable on PATH and in the personal fallback directory; PDF structure was checked with Ghostscript and the independent Poppler parsing instead.

No fresh global source-library validation was needed for this bounded page role; direct uncached document validation passed and no old sibling failure was inherited. No expensive source OCR replay was run.

## Review limits and handoff

Pages **13–24 were not opened individually or accepted** by this role. The source closing, final historical notes, terminal apparatus and rights colophon therefore remain unassigned here. No native source image was opened; primary issue identity, publication facts, damaged-print diagnosis, recovery replay and rights/intake judgment belong to the separate source role. The separate pages-b role owns pages 13–24. Whole-PDF acceptance requires the coordinator to verify the disjoint actual observation union 1–24 and the separate source judgment.

Evidence: `page-observations.json` SHA-256 `df3342ef9cf02fa7f62753b0856312cccb9677635d2243ee833dda823d2b10b7` and `verification.json` SHA-256 `ec6454d56e1b85b724335363579f31c8bb9e80fd8fb3b3d43a6328dc49e27af4` in this report's scratch directory. The canonical subset report target is `src/sources/papal-documents/encyclicals-refinement-cold-52-pages-a.md`; this reviewer did not write that target. Only the assigned scratch directory was changed; no canonical source, producer file, shared cache, code, Git state, installation or release record was changed.
