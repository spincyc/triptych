# Studiorum Ducem — independent cold review, packet 36

Reviewed 2026-10-30. **Bounded SOURCE RECOVERY: PASS. PDF: PASS, all 9 pages freshly inspected.** No blocking source or layout finding was identified within the review extent below. These are separate decisions about the exact replacement source and reader bytes. The producer's completed JSON report supplied provenance, not independent acceptance.

| Exact input | SHA-256 / extent |
| --- | --- |
| Packet 36 | `7f97d2e0bf48fc7e819544c21f667c4135bc1de1ce9f6e95e0904a4d77419a65` |
| Reviewed English PDF | `43c3054dc2a567c6febba74a1759d471e110b1efd03bfa2177a44a609955293e`; 9 pages; 69,370 bytes |
| Receipt | `46f95d87d016efb95472e4d05d61aa0c4fefb73bc1d220142bd400fa137f4304` |
| Frozen input manifest | `9c8415878a68a7eb71220418483dd488370d83e0997669cb1e6d07355a46191e` |
| Selected source text | `6c720368bacc86d4fd618243863b184b4048aff4e28e57be1a589f1a61bd4e51`; 42,305 bytes; physical LF lines 1–877 |
| Retained facsimile parent | `045e449fa79f45d63a351dc7ce3b98df0f146eb24d603d3c9f2b683d8670e699`; 304 native pages |
| Retained OCR replay package | `fc1655a843ea3288cbc963bdaf6675b16877d290b32792265b07853ba8b7f2f7` |
| Recipe / replay implementation | `c58936126947ee102472c18b9c537e1bed9933742ce28f1a82c28978f02ed133` / `44a41e99bc3c8d45ab8c697f73e0bbef9df33880ea05727463416d0db15d85e8` |

The PDF is the packet's exact `pdf_path` for `papal.pius-xi.hf-p-xi-enc-19230629-studiorum-ducem`, language `en`, titled *Studiorum Ducem — historical abridged English translation*. Its complete source row equals the matching frozen manifest row. Revision `2026-10-30T15:31:58Z` comes from the manifest's top-level `revision`; its absence as a row field is intentional. The segment is the schema-2 `ryan-fresh-image-ocr-6c720368bacc` historical abridged translation, controlling source LF lines 1–877. Exact segment and artifact metadata match their packet pins.

## Independent source recovery

I freshly opened full native facsimile renders 120, 122, 128, 129, 132, 133, 134, 135 and 148, and additionally opened the exact OCR crops of 122 and 134. These native renders are tied to the actual retained parent by the successful full replay. I read the corresponding raw TXT for the opening, closing and six formerly noisy pages, checked the excluded running-head lines for all 28 continuation pages, and independently assembled every raw TXT stream in printed-page order. No source words were supplied or corrected by this review.

| Bounded gate | Direct finding and disposition |
| --- | --- |
| Native 128/129, printed 78/79; selected LF 243–306; PDF 3 | The native bottom `Ecu-` continues with `menical Council` on the next leaf. The fresh OCR and reader preserve that continuation without the former intervening `Fa` debris. PASS for this sustained-noise span. |
| Native 132/133, printed 82/83; selected LF 369–429; PDF 4 | The native last line ends `remote from`; the next leaf begins `it, until finally`. Fresh OCR and PDF retain the prose without the former interposed graphic-noise stretch. PASS for this sustained-noise span. |
| Native 134/135, printed 84/85; selected LF 431–491; PDF 4–5 | The native last line ends `Wherefore St.`; the next leaf begins `Thomas is the chief master`. Fresh OCR and PDF retain that continuation without the prior sustained marginal debris. PASS for this sustained-noise span. |
| Native 122 crop | Full image 1190×1795; crop x=155, y=0, w=1015, h=1640. Comparing the full page with the actual crop shows complete leftmost and rightmost body letters, and all body lines. Outside-body left-margin marks are excluded. PASS for crop safety. |
| Native 134 crop | Full image 1194×1788; crop x=165, y=0, w=970, h=1640. Full-page and crop inspection shows complete body letters and final `Wherefore St.` line, while the separate left-margin marks remain outside the crop. PASS for crop safety. |
| Opening / closing | Native 120, printed 70, contains the historical heading and opening `We have commanded`; the crop retains both. Native 148, printed 98, contains the blessing continuation, dated Roman closing and `PIUS XI.` subscription. The crop retains the complete closing. These appear in PDF 1 and 8–9. |

Identity evidence was independently rendered directly from actual parent PDF pages 5, 6 and 9 at 300 dpi as JPEG quality 95, with no crop or resize, into the exclusive reviewer scratch. I read these direct-parent images instead of relying on the producer's convenience JPEG mapping. Page 5 identifies *The Encyclicals of Pius XI*, introduction and translation by James H. Ryan, B. Herder Book Co., St. Louis and London, 1927. Page 6 states United States printing and copyright 1927. Page 9 explicitly says the translator did not translate and reproduce the appended prayer to St. Thomas. These facts support the existing edition identity and its recorded historical-publication basis; this review supplies no new jurisdiction-wide rights opinion.

The result remains a **historical abridged English translation**. Recovering the complete printed constituent, pp. 70–98, does not recover the omitted prayer or make this a complete-act English translation.

## Mechanical and provenance checks

- All 256 packet path/hash/size checks passed, including the current helper path+SHA pins, producer evidence, source/controller metadata, all 29 full PNGs, crops, raw TXT and TSV files, recipe, replay script, identity references and reader raster inputs. This count includes repeated evidence paths, not 256 distinct artifacts.
- The canonical replay ZIP's recipe equals the pinned producer recipe byte for byte, and all declared package input members match their hashes. The exact retained recognition-model package `eeb957f8653327f43959be56cffbd891146f1eaea1f8dd7f5d87a39e5dafdd05`, its artifact identity and the English model `7d4322bd2a7749724879683fc3912cb542f19906c83bcc1a52132556427170b2` match the recipe. All three executable tool hashes match.
- After reading the pinned `replay.py`, I ran it against the actual retained parent and model package, with its output and temporary directory under the exclusive reviewer scratch. It exited 0 after reproducing all 29 full-image, crop, TXT and TSV hashes for native pages 120–148, then the exact reading hash. Independently comparing each declared rectangular crop with its full render also returned pixel equality for all 29 pages.
- My separate assembly drops zero initial lines on native 120 and exactly the running-head/folio line plus following blank on 121–148; the exclusions were read and recorded. It joins the stripped page streams with two LFs and terminates with LF. Its 42,305 bytes equal the canonical text and replay output exactly. No dehyphenation, lexical repair or translation was applied.
- Current uncached `validate_document(source_row, root=repo)` passed. Current `pdf_body_fidelity(pdf, validated, 9)` passed with method `pdf-raw-source-aware-line-hyphen-nfkc-v3`: 34,540 normalized source characters, 49 permitted layout hyphens, source coverage from PDF 1 through 9.
- Current `env PYTHONDONTWRITEBYTECODE=1 TRIPTYCH_LIBRARY_CACHE=0 tools/source-library validate` exited 0 with no diagnostics. The producer's historical Aeterni sibling failure is absent from this fresh run. Schema 2 and artifact `page_count` passed current validation.
- `pdfinfo` and `pdffonts` exited 0: 9 unencrypted Letter pages, correct title/English subject/Pius XI author, revision-consistent dates, and four embedded, subset, Unicode-mapped Latin Modern fonts. The sole disclosed underfull-box warning produces no visible clipping or collision.
- The raster cache receipt, renderer fingerprint and exact PDF association match. All 19 original cache files and their 19 presented output counterparts match their recorded hashes and sizes and each other. Raster reuse supplied images; no prior visual acceptance was reused.

Every Python import and source-library invocation in this review used `PYTHONDONTWRITEBYTECODE=1 TRIPTYCH_LIBRARY_CACHE=0`. The replay reads the pinned producer package and writes only its new scratch output and temporary files. No canonical source, producer file, shared cache, manifest, installed PDF or Git state was changed.

## Fresh every-page PDF judgment

I opened the exact contact sheet and individually opened current page rasters 1–9 at original resolution, one image per display. All pages received a fresh judgment; reused pages and reuse proofs are empty.

| PDF page | Inspection |
| --- | --- |
| 1 | Title, pope, act date, English language and abridged status are clear. Historical opening and heading are present. Two-column reading order and body margins are clear. |
| 2 | Continuous two-column body, paragraphs and inline historical citations are legible; no clipping, collision or glyph boxes. |
| 3 | Native 128/129 continuation is readable without sustained junk. The retained hard hyphen and source-page paragraph break are visible. |
| 4 | Native 132/133 continuation is readable; quotations and citations remain distinguishable within the prose. |
| 5 | Native 134/135 continuation is readable. The source-page break after `St.` is a paragraph boundary, not a fused source note or missing body. |
| 6 | Body remains legible. Isolated literal OCR errors, including trailing `nn` and `Tmas`, remain; they do not form a sustained unreadable stretch. |
| 7 | Body and citations retain normal column order and usable spacing. No missing-glyph boxes, overlaps or clipped lines observed. |
| 8 | Numbered historical privileges, blessing and dated closing remain readable and ordered. |
| 9 | Sparse but source-bearing: the historical `PIUS XI.` subscription precedes a rule and compact, legible source/rights apparatus. This is not an apparatus-only final page. The sparse subscription is an explicit PASS qualification. |

## Qualifications and limits

Ordinary uncorrected OCR remains, including `syn` on PDF 1, `terni` on PDF 2, `Tmas` and isolated `nn` on PDF 6, punctuation artifacts, printed hard line-end hyphens, and paragraph boundaries at historical page joins. This review accepts the bounded recovery from the former sustained-noise defects and the legibility of the exact reader; it does not certify a corrected transcription.

Full-resolution native inspection covered only the nine constituent pages listed above and the three directly rendered identity leaves, with additional full-resolution crop views for 122 and 134. All 29 constituent pages were mechanically pinned and replayed; this is not a claim of visual inspection or lexical collation of every native page. No whole-translation accuracy audit, whole-source word-by-word collation, physical-original authentication, new rights clearance, installation or deployment is certified. No historical source evidence state was promoted.

The exact `report.md` bytes are intended for `src/sources/papal-documents/encyclicals-refinement-cold-36.md`; the coordinator owns copying and integration. `reviews.json` binds that canonical target to this report's final SHA-256. `verification.json` retains the reproducible pin, assembly, replay, cache, source-validation, fidelity and page-inspection evidence in the exclusive reviewer scratch.
