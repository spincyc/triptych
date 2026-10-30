# Independent cold review: English imprint qualifications, packet 31

**PASS — two PDFs, four pages freshly inspected individually, two contact sheets inspected, no source/layout/metadata blocker within the assigned scope.** This is an apparatus qualification audit and fresh review of the exact replacement PDFs. Original packet 06 root-owned source-body/extent/rights acceptance remains separate.

| Reader | Exact PDF SHA-256 | Actual pages | Individually inspected |
| --- | --- | --- | --- |
| Exultavit cor nostrum, English | `a2a2fec1066b36352686d7f4dfe7abcb81715948d6eb8de9feb8c3f3ad18c2cd` | 2 | 1, 2 |
| Cum Sancta Mater, English | `9eb25fe87aedf6eceece6fcb6675450b3d9b724fcacd939e688e6006c4aa0e31` | 2 | 1, 2 |

The shared final receipt is SHA-256 `b3793282ebe2ad0262dffa94bdb71a612aa39a3bc00db17ae1d4201d3ef23b92`; the final frozen/selection manifest is `20e6f12cc4b266108a7d44098d4c2a684c2bd6c6b7323c85be718b93493bb428`. Both full packet source rows equal their frozen rows and the proposed current rows. PDF hashes, receipt entries, revisions, actual page counts, all pinned controllers and payloads, and both raster-cache receipts and their output/cache files matched. The verification artifact records 80 distinct exact file pins.

## Apparatus qualification audit

**PASS.** CIHM 51176's retained catalogue response (SHA-256 `55ceda09fd5938f26b04eedce44cd9d216c2f6d1e1b3118c342ebf2e99e6697e`) gives publication year 1859 and `[Kingston, Ont? : s.n.]`. I freshly inspected the retained native Horan wrapper, source PDF page 3, which dates his pastoral at Kingston on 9 June 1859. That is an issuing-location/date statement, not a printer's imprint. Cum Sancta Mater's final notice accurately preserves 1859 as corroborated, Kingston as an inferred printing place, and the printed imprint and publisher as unknown.

CIHM 52209's retained catalogue response (SHA-256 `31eaf9b916b483127b8fd11932786dfe6544dd82252ff24d4859226351492ee1`) gives publication year 1852, publisher `[S.l. : s.n.]`, and tentative city `[Quebec?`. I freshly inspected the native Turgeon wrapper, source PDF page 7 / printed page 6, dated at the Archiepiscopal Palace of Quebec on 23 April 1852. Quebec is established there as the wrapper issuer's location; it does not establish a printing imprint. Exultavit's final notice accurately identifies publication in 1852 and printing place/publisher unknown, with Quebec tentative. Its controlling notes and rights-basis metadata explicitly distinguish the wrapper location. The compact PDF notice does not turn that location into a proved imprint.

I independently compared all **ten** old/new TOML snapshots listed in `metadata_qualification_scope`: two segment controllers, four work/container editions, and four OCR/native artifact records. Exact old/new hashes and sizes matched. Parsed comparisons and literal line diffs found only the declared `context`, `notes`, `publication`, and `rights_basis` assignments changed. All other bytes and fields, including source selections, IDs, payload ownership, historical transformation descriptions and their pins, remained unchanged. The updated field texts consistently preserve the two qualifications above. Segment schema 2, OCR artifact schema 1, and native artifact schema 2 agree with their exact pinned records.

## Source and PDF checks

Both source rows changed only `source_note`, `rights_basis`, `witness`, and `revision` against the preserved old rows. Old/new row hashes matched the packet. Source payloads and selection bounds remain unchanged: Exultavit uses LF ranges 1–36, 39–76, 78–116, 118–119, 122–154; Cum uses 28–58 and 64–98. The current body TeX matches both preserved prior render sets byte for byte:

- Exultavit: `75a544f348b66bcb43a9c1c6b1e8afe634549be956fbf3296a92af5b261eb8f1`.
- Cum: `c8ccfe7aabfe784383f7a17912748f1f14f4a975d9aa65f8d7be36977b1fa8c0`.

With `PYTHONDONTWRITEBYTECODE=1` and `TRIPTYCH_LIBRARY_CACHE=0`, I independently ran pinned `scripts/_typeset_papal.py` (`1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146`) through `validate_document(source_row, root=repo)` and `pdf_body_fidelity(pdf, validated, 2)`. Both returned `pass`, matching the exact receipts: Exultavit 9,197 source characters / 7,580 normalized, 16 layout hyphens; Cum 5,082 / 4,140, 7 layout hyphens. Both begin source text on page 1 and finish it on page 2.

`pdfinfo` parses both as two-page letter-size PDF 1.7 files with correct titles, Pius IX attribution and English subject; no encryption, JavaScript, form or suspect flag. Four Latin Modern font subsets per PDF are embedded and have Unicode maps. Creation/modification timestamps correspond to the pinned 2026-10-30T15:20:25Z render revision. Current logs have only the disclosed underfull-box warnings; no overfull box, missing-character, undefined-control-sequence or LaTeX-error marker was found.

## Fresh visual findings

Each existing PNG was opened one image per call using `view_image(detail="original")`, then displayed with its original MIME and automatic detail. I inspected both reader contact sheets and all four full-page rasters. No prior visual acceptance was reused.

| Reader/page | Observation |
| --- | --- |
| Exultavit 1 | Clear title, issuer/date/language and historical heading; readable two-column text with ordinary left-to-right column flow, margins and footer. Disclosed OCR spelling and broken words remain literal. |
| Exultavit 2 | Body continues in both columns through the dated closing and `PIUS IX. Pope`; the terminal notice and colophon are separated by a rule and fit clearly. The inherited `He re-` / `gards` paragraph division is visible, readable and unchanged. |
| Cum 1 | Historical address and salutation remain visible before the body. Two columns, margins and footer are readable without clipping, overlap or apparent glyph loss. OCR word divisions and misreadings remain disclosed source limitations. |
| Cum 2 | Sparse but source-bearing: the closing sentence and dating clause precede the source notice. The literal `185)` is disclosed. Imprint qualification and colophon fit without overlap; this is not an apparatus-only final page. |

No new historical source notes or body material were introduced. The fresh native inspection was limited to the two dated wrapper pages needed for these apparatus claims. I did not repeat the earlier act-page collation or inherit it as fresh inspection.

## Scope and integration qualification

The live shared historical-English manifest has advanced from the producer's baseline hash `8a0e25285e36af6f685dbfdb8d3c51f8bac50623cd7dd3b099f745f89cdc6627` to observed hash `4324c2ab23739542e51b6b40332f6a196d6f6f1de7f63b35829d9876221f205f` (71,175 bytes). Both assigned live rows equal the exact packet rows. Root confirmed this is its authorized adoption of the two final rows; the producer's earlier “shared manifest preserved” statement describes its historical production event, not the state after root integration. This is not an acceptance blocker.

Producer raw review JSON was retained and hash checked as author evidence; its `pass` fields supplied no independent page coverage. This review certifies the bounded apparatus qualifications and the four inspected PDF pages only. It grants no new translation-accuracy, whole-print lexical-collation, original-print identity or rights certification, and no installation or deployment approval. No tracked, producer, source, PDF, cache, release or Git state was written. All review outputs are confined to the assigned scratch directory.
