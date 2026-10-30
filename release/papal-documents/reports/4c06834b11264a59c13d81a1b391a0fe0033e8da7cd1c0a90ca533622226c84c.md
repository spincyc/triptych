# Classic papal reader independent review B

Reviewed 2026-10-30. Canonical report destination: `src/sources/papal-documents/encyclicals-direct-baseline-recovery-b.md`. This report is delivered from the assigned scratch review lane; no canonical source, PDF, receipt, manifest, raster, helper, release, or Git state was changed.

**Result: PASS for both exact selected normalized-web readers, with the bounded source qualifications below.** This evaluates readable rendering and complete fidelity to the pinned web-transcription artifacts. It does not certify diplomatic agreement or completeness against every feature of the historical printing. The source notes explicitly identify uncollated normalized web transcriptions; neither the source nor this review is promoted to full image collation. No prior reviewer status or page coverage was inherited, and no page reuse was claimed.

## Frozen identity and mechanical checks

Packet SHA-256: `3c114e7d83929bc7875334a60ea6215bb826b59724e4c3685e8c1514aee8ec1d`.

Common frozen manifest: `.scratch/encyclical-classic/readers-fixed/frozen-manifest.json`, SHA-256 `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`.

Whole receipt: `.scratch/encyclical-classic/readers-fixed/receipt.json`, SHA-256 `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`. Generator `typeset-papal`, version 2; revision `2026-10-30T02:56:48Z`. Its input-manifest hash and both selected revisions agree. The receipt contains failures for other documents; neither assigned key has a receipt error. This is not an acceptance of the entire receipt's document set.

For each `(id, language)` below, the **whole** frozen manifest row equals packet `source_row`, and the **whole** matching receipt row equals packet `receipt_row`; these were equality assertions over complete decoded objects. The PDF, source payload, receipt, manifest, all source-controller record bytes and available controller payloads match their exact packet pins. The two HTML controllers are restricted metadata records without retained payload paths; their record hashes, IDs, parent hashes, and declared storage/type agree. No fresh HTML acquisition or independent re-extraction from those historical HTML bytes was performed.

The full source-to-PDF checks were rerun read-only using `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python`, `sys.path.insert(0, 'scripts')`, `_typeset_papal.validate_document(source_row, Path.cwd())`, then `_typeset_papal.pdf_body_fidelity(Path(pdf_path), validated_doc, pages)`. Both returned the complete recorded fidelity objects, including physical-line-only discretionary hyphens. Module SHA-256: `1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146`.

| Reader / language | PDF SHA-256 | Pages / source-bearing extent | Source SHA-256 | Fidelity |
| --- | --- | --- | --- | --- |
| Sancta Dei Civitas / la | `0f309481e418f66fdad1107d83ecd45caf1edcfc6041e0d5da92a414bd377a0e` | 3 / 1–3 | `d546bd01d32abb27f46ef6fd836b240b82c68c22ec850451984160084d7dc0aa` | PASS; 14329 source characters, 12408 normalized, 88 layout hyphens |
| Quam Aerumnosa / la | `d2b07b50a84ad994a3a8756b1fdc6b8300c6fed3fb0dea1838b6d5240aade26d` | 2 / 1–2 | `4e47267683fd19b0898d8a7345859f7d4e8859801e8b08ab1b972cbbd3e95373` | PASS; 7144 source characters, 6161 normalized, 37 layout hyphens |

`/usr/bin/pdfinfo`, `/usr/bin/pdffonts`, and `/usr/bin/pdftotext -layout` ran successfully on both readers. Both are unencrypted PDF 1.7, US Letter, rotation 0, and have the correct Leo XIII author, Latin subject, title and revision-derived dates. The sizes are 36,939 bytes and 27,904 bytes respectively. Every listed font is embedded, subsetted Latin Modern with Unicode mapping; no substitute or missing font is reported. The PDFs are untagged, which this review does not treat as a claim of tagged accessibility.

All lines of each final `.log` and both `.pass-1.txt` / `.pass-2.txt` files were scanned. No fatal error, undefined reference, overflow/overfull box, or missing-character diagnostic was found. Pass 1 has ordinary PageLabels, changed-label and rerunfilecheck requests; pass 2 and the final logs contain no unresolved warning. Exact log paths, line counts and hashes are retained in `mechanical-checks.json`; `sancta-pdfinfo.txt`, `sancta-pdffonts.txt`, `sancta-layout.txt`, and the corresponding `quam-*` files retain the mechanical output. No build or rerender was run.

The existing shared raster run manifest SHA-256 is `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02`. Its selected PDF rows match exact PDF hashes, paths and page counts. Each per-document `review-cache.json` matches the PDF hash and page count; every listed raster/contact-sheet/thumbnail file hash and size was checked. Reader inspection used only each full 1700×2200 page PNG, not contact sheets or thumbnails.

## Actual reader page inspection

Each listed page was opened individually with `view_image(detail='original')`, one image per tool call, with MIME-correct `image(..., 'auto')` forwarding. These are fresh visible inspections.

| Reader | Page | Observation |
| --- | --- | --- |
| Sancta Dei Civitas | 1 | Compact title, issuer/date/language, retained all-capital protocol, and opening text are visible. Two columns continue left to right: `Duo haec` → `munia quae...`. The spaced-letter protocol is present in the source. No clipping, overlap, missing glyph or overflowing line. |
| Sancta Dei Civitas | 2 | Dense but legible justified columns, indented paragraphs and clear gutter. The prior quotation continues into the page; left-to-right column continuation follows the body. No visible interference with the footer or column boundary. |
| Sancta Dei Civitas | 3 | Both columns contain genuine source body. Final exhortation, blessing, complete dating clause and `LEO PP. XIII` remain above the smaller source/rights apparatus. The rule and colophon are legible and do not force a project-only page. |
| Quam Aerumnosa | 1 | Title, source heading, protocol and salutation are visible. The body continues normally from left `na-` to right `scentibus...`. No clipping, collisions or visibly broken glyphs. |
| Quam Aerumnosa | 2 | Substantial genuine source body continues in the left column through the blessing, dating clause and retained `LEONE PP. XIII`. The right column contains compact terminal apparatus. Its unused lower space is acceptable: this final page is source-bearing and is not an apparatus-only extra page. The retained `XIII` in the first paragraph is a source qualification recorded below. |

Reader pages actually inspected: Sancta `[1,2,3]`; Quam `[1,2]`. Reused pages: none.

## Native witness identity and bounded inspection

The complete local native PDFs were hashed before extraction and agree with the registered native artifact and `publication-approvals.json` historical-witness pins. Whole-document `/usr/bin/pdftotext -layout` extraction was written only into this lane. Native page counts were checked with `/usr/bin/pdfinfo`. The identified printed pages happen to equal artifact ordinals; this was checked from the extracted page heads and visible rasters rather than inferred from filenames.

These Vatican `-ocr.pdf` files are **OCR reconstructions, not an asserted original facsimile**. The visible images below establish what these exact reconstructions show. They do not establish every glyph of the nineteenth-century printing.

| Native witness | Complete PDF hash | Bytes / artifact pages | Native pages actually viewed, both printed and ordinal |
| --- | --- | --- | --- |
| ASS XIII (1880–1881) | `4b841f737ce46d8c98e0f22a74619ff4ab458d5b9fb500735c17ab7e5bee0f89` | 2,541,144 / 592 | 241, 242, 248 |
| ASS XXI (1888–1889) | `b21166843473d5b7b147de3e217fceb3ad8094561ceadebca456611325c5d980` | 3,212,945 / 768 | 258, 259, 260 |

Sancta uses **ASS XIII, pp. 241–248**. The modern web bibliography's “XXIII” is a disclosed delivery typo, not a competing source identity. Quam uses ASS XXI, pp. 258–260.

Only the six bounded pages above were extracted with `/usr/bin/pdfseparate` into `native-pages/` and rasterized using the repository helper with isolated output/cache and `--jobs 1`. The helper completed successfully. Each was then converted to a deterministic JPEG at quality 95 without resizing (1550×2200) in this lane to keep image context bounded. All six JPEGs were actually opened individually at original resolution with MIME-correct image forwarding. Exact bounded-PDF, helper PNG, inspection JPEG hashes and native controller record hashes are in `native-evidence.json`. No shared native or reader raster/cache was changed.

### Sancta: native opening, ending and notes

The selected normalized text has 16 blank-line-delimited blocks. At the opening, its protocol/address block ends `CVM APOSTOLICA SEDE HABENTIBVS`; a separate block then starts `Sancta Dei civitas quae est Ecclesia...`. Native p. 241 places a visible `LEO PAPA XIII`, `VENERABILES FRATRES`, and `salvtem et apostolicam benedictionem` between those loci. The reconstruction's `LEO PAPA XIII` is visible despite being absent from its layout-text extraction. This is an **opening difference between the selected web witness and the historical reconstruction**, not renderer omission; it is a bounded source-scope qualification. The retained source is not a diplomatic copy of that printing.

Native p. 241 has the separate page-foot Isaiah reference after a superscript following `extendat`; the body continues `Haec autem christianarum gentium...`. The selected web source instead reads `extendat (Is. Liv, 2). Haec autem...` in its opening paragraph. Native p. 242 similarly has five page-foot references (Romans, Luke, 1 Corinthians, Matthew/Luke, Acts). Their surrounding body anchors and following continuations are identifiable in the selected source: `verbum Christi (Rom. X, 14, 17). Istud autem...`; `facultatibus suis (Luc. VIII, 3), et Paullus...`; `Evangelio vivant (I Cor. IX, 14). Pari modo...`; `messem suam (Matth. IX, 38, Luc. X, 2): primosque...`; and `verbum tuum (Act. IV, 29). Duo haec...`.

Thus the retained source deliberately presents those references inline. They are coherent parenthetical citations at their anchors, with both preceding and following body context; this is not evidence of an OCR note block accidentally fused into an unrelated body paragraph. The reader preserves the web witness's note presentation. Native p. 242's opening body paragraph ends `varietate locorum temporumque diversitate.` before the indented `Cum aetate nostra...`; these are separate source blocks and visually separated reader paragraphs.

At the ending, native p. 248 and reader p. 3 retain the `Certa fiducia nitimur...` paragraph through `in Domino impertimus`, followed by a separately delimited `Datum Romae...` clause and `LEO PP. XIII`. The native then starts a distinct notice heading and later a different letter; neither is silently joined to this reader. No terminal body, dating or subscription loss was found at this checked boundary. Native pp. 243–247 were mechanically extracted as part of the full volume and read as text for context, but were **not** visually inspected; no full-work lexical or image collation is claimed.

### Quam: native opening, ending and paragraph boundaries

The selected source has 12 blank-line-delimited blocks. Native p. 258 and reader p. 1 retain the heading identifying the American bishops, `LEO PP. XIII`, the `Venerabiles Fratres...` salutation and `Quam aerumnosa...` incipit. The opening body paragraph ends `quae ducit ad interitum.` before the indented `In his autem malis...`; these are also separate retained source blocks. On native p. 259, `In his...` finishes with `pessimi quique inolescunt.` before the indented `Haec omnia...`. The source and reader preserve that separation.

Native p. 259's long `Haec omnia...` unit ends `dispensatores mysteriorum Dei.` before the separate indented `Inter alumnos...` paragraph. This is also a clean source/reader block boundary. That paragraph continues from native p. 259's `italis parentibus` to p. 260's `natos, recipi...`; the retained source/reader p. 2 instead has `italis parentibus XIII natos`. The extra `XIII` is an isolated source-transcription anomaly at this checked boundary. It was not introduced by typesetting; neither its origin nor a correct replacement is inferred here.

On native p. 260 the `Inter alumnos...` paragraph continues through `studiose retulerit.`; `Ex hoc autem opere...` begins a new indented paragraph. Retained source blocks preserve these two sides. The latter paragraph ends the blessing `peramanter Domino impertimus.`, followed by the dating clause and subscription. The native subscription is `LEO PP. XIII`; the selected web source and reader retain `LEONE PP. XIII`. This is a second isolated transcription/edition difference. The date, blessing and subscription extent are present rather than truncated. No separate native footnote block was visible on the three inspected Quam pages. Stray OCR punctuation in that reconstruction is not treated as a missing historical note without a corresponding note body.

## Findings and acceptance limits

- **Minor source-scope qualification, Sancta reader p. 1:** the bounded native opening includes the extra papal-name and salutation blocks described above. PASS applies to the identified normalized web witness; it must not be represented as diplomatic completeness against the ASS printing.
- **Informational source-presentation qualification, Sancta reader p. 1:** native page-foot Bible references occur as coherent inline references in the retained web witness. The surrounding paragraph evidence does not establish accidental fusion. No new note anchors or note reconstruction are approved by this review.
- **Minor retained source anomaly, Quam reader p. 2:** `italis parentibus XIII natos` differs from the checked native page-boundary continuation. The whole selected-source body remains legible; this isolated anomaly is disclosed, not silently corrected.
- **Minor retained subscription difference, Quam reader p. 2:** selected `LEONE PP. XIII` versus native reconstruction `LEO PP. XIII`. No renderer omission or ending loss is involved.

These bounded differences do not establish sustained nonsensical text or accidental body/notes interleaving. They remain source qualifications under the readers' explicit uncollated-web disclosures, and do not block the rendering PASS. A historical critical or corrected edition would require a separately identified, source-supported correction and renewed byte-bound review; this lane makes no such edition.

No full source-to-native lexical collation, original-facsimile collation, rights-law reassessment, external-source freshness check, installation, or review of any other PDF is claimed. The affirmative distribution basis was checked as the existing pinned artifact/approval evidence; it was not broadened. No source correction is requested as a condition of this specific retained-web rendering acceptance.

## Review-lane artifacts and execution state

`report.md` is the final human-readable report. `reviews.json` carries exactly the two assigned `(id, language)` records with the report hash and canonical destination. `mechanical-checks.json` and `native-evidence.json` retain detailed check and image pins. Text extracts, metadata/font reports, bounded native PDFs and their isolated review cache/rasters remain scratch-only.

No generic handoff directory or ZIP was created: the assigned deliverable is this scratch-only review result lane, not a new outbound handoff package. The native helper's execution session completed with exit 0. No tool or subprocess handle remains live, and no blocker prevents this lane's completion.
