# Acerbo nimis — independent English reader review

**PASS** for the exact six-page ACQR 1905 English reader identified below. All six reader pages were individually opened at their original raster resolution and inspected in this review. The historical English printing, complete source-to-PDF fidelity, source boundaries, apparatus ownership and readable layout support acceptance as a mechanical OCR reading edition with the stated limitations. No blocking finding remains.

## Exact scope and pins

| Item | Exact value |
| --- | --- |
| Document | `papal.pius-x.hf-p-x-enc-15041905-acerbo-nimis.acqr-1905-english` |
| Language and reader pages | `en`; 6 |
| Reviewed PDF SHA-256 | `dc813b5d3b2447777ead80386e53b1e68fc80f94a27d43e5869a3638e3db8b90` |
| PDF size | 51,480 bytes |
| Review packet SHA-256 | `c0896a0a2ffdd1f0356454f6d3eee3d86b04e0de27bd020a4b4300b2be35d48a` |
| Entire receipt SHA-256 | `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e` |
| Frozen manifest SHA-256 | `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342` |
| English source SHA-256 | `55104820e9870021e04597a9656697bbd18340de9876e871952b9574359d9745` |
| Selected segment manifest SHA-256 | `e95f70191b4686164186d7e273fdb1d853ef5cb6be23dc8d73813f35c57cbdaa` |
| Render revision | `2026-10-30T02:56:48Z` |
| Shared raster run SHA-256 | `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02` |
| Canonical report target | `src/sources/papal-documents/encyclicals-direct-baseline-recovery-h.md` |

The packet's entire `source_row` equals the exact id/language row in the frozen manifest. Its entire `receipt_row` equals the exact id/language document in the whole pinned receipt. These are whole-object comparisons, not comparisons of selected fields. PDF, source, segment, controller manifests and payloads, frozen manifest, complete receipt and shared raster-run pins all passed fresh hashing. The raster cache identifies this PDF hash and six pages; all listed full pages, thumbnails and contact sheet match their recorded hashes and sizes. Only individual full pages count as visual coverage here. No earlier checkpoint, page observation or acceptance was reused: `reused_pages` and `reuse_proofs` are empty.

The two packet controller manifests and payloads were checked, then the source package's four support mappings were followed to their independently hashed payloads: whole raw OCR, native title image, boundary-review JSON and extraction recipe. The controlling English-reading artifact manifest hashes to `bd8e20cc68d13dc8e9b4f01a7588981247662f5807a4630936a0d23edc40fe7b`; the source-package manifest hashes to `3d3364d435261aa7a611da9be460f7666316077f344e39e3421b18aa0ac63036`. Package payload `9ac67a4890d26f06bc66f94fe319aed9aa254a2c8e693fd10efaed5afb46695d` maps exactly to the manifest's support declarations. The review JSON was context, not inherited visual evidence.

This acceptance belongs to this English witness alone. The separate Latin ASS reader `acta.ass.037.ass-037-l023300` is not a replacement, supersession or source of English wording. Identity was established from the English Pius X heading and universal episcopal address, catechetical body, signature and 15 April 1905 dating, together with the printing context; a shared incipit alone was not used.

## Fresh mechanical checks

From the repository root, the lane ran with `PYTHONDONTWRITEBYTECODE=1`, inserted `scripts` into `sys.path`, imported the existing read-only `scripts/_typeset_papal.py`, then called `validate_document(source_row, Path.cwd())` and `pdf_body_fidelity(Path(pdf_path), validated, 6)`.

The fresh result is **pass**, method `pdf-raw-source-aware-line-hyphen-nfkc-v3`: 26,295 source characters, 21,571 normalized characters, 33 additional physical-layout hyphens, source first page 1 and last page 6. It equals the receipt's complete text-fidelity object. This covers the whole selected text, including headings, address, all six regulations, inline citations, closing, signature and dating; it is not a sampled check. Its declared whitespace, Unicode compatibility and physical line-end hyphen allowances do not establish corrected OCR or full print collation.

The extraction recipe was replayed mechanically from the full raw OCR at exact inclusive physical LF lines 22847–23338. All nine omitted whole-line strings and their LF-inclusive SHA-256 values matched. Whitespace was normalized within the original blank-line blocks, blocks were joined with one blank line, and a final LF was retained. The replayed output hashes to the exact English source `55104820e9870021e04597a9656697bbd18340de9876e871952b9574359d9745`. No source words were rewritten by a model.

`/usr/bin/pdfinfo`, `/usr/bin/pdffonts`, and both `/usr/bin/pdftotext -layout` and `-raw` completed with exit 0. The reader is an unencrypted PDF 1.7, six letter pages, rotation 0, with no forms or JavaScript. Title is Acerbo nimis, subject identifies the English papal source edition, author is Pius X. Creation/modification time agrees with the tracked revision. All four Latin Modern font subsets are embedded, subsetted and have Unicode mappings. The 51,480-byte PDF is below both repository size investigation thresholds. Text extraction and visual inspection agree on left-column-then-right-column order, then the next page. The PDF is untagged; no accessibility conformance claim is made.

The complete final `.log` (495 lines), pass-1 transcript (84 lines) and pass-2 transcript (74 lines) were read by the diagnostic script. No fatal error, missing glyph, undefined reference or overfull box was found. First-pass PageLabels, label and outline rerun requests clear by pass 2. One underfull hbox, badness 1701 at body lines 48–49, persists. It corresponds to the start of reader page 2, the paragraph beginning “knowledge of divine things”. That paragraph was individually inspected; spacing is readable and no clipping or overflow results, so the warning is dispositioned as nonblocking. Log hashes are:

| File | SHA-256 |
| --- | --- |
| Final log | `b7f62969f23e4a67908c6755bb5e00809d4f0e3ade6b1c791b57a6b49a48a0e7` |
| Pass 1 | `39123d2fa59f28575a5221ce4c93b4a41da55f7ebe06197aba9607eab9891221` |
| Pass 2 | `3e9b77ead6fcfbcb14b5f01de10145c8484314d0e0bcfa6996f08c0d7161c4b1` |

## Actual individual reader-page inspection

Each entry records an actual individual full-size image inspection during this review, using `view_image` with `detail: original`, one image per tool call. Shared reader PNGs were read only. Contact sheets did not substitute for these observations.

| Reader page | Observation |
| --- | --- |
| 1 | Compact title clearly says Acerbo nimis, Pius X, 1905-04-15 and English. Historical heading, addressee, greeting and opening are present. Two columns have clear margins and gutter; left-column continuation into the right column is orderly. The right column ends with the foundation-of-holiness paragraph continuing onto page 2. Isolated retained OCR includes `t^e` and `feach`, and source word breaks such as `intel- lectual`; these do not produce sustained unreadable text. No neighboring Latin wording enters the English body. |
| 2 | Continues “knowledge of divine things” with its inline reference, followed by the argument for religious instruction and the duty of pastors. Both columns remain readable, with no note/body collision. The blank-block break between “humility of” and “soul” matches the native page boundary. The underfull first paragraph remains legible. Final text reaches instruction of the faithful in sacred things in normal order. |
| 3 | Continues the value and priestly obligation of catechesis, then Trent and Benedict XIV. Both halves of the native `accept-`/`able` and `Con-`/`stitution` interruptions remain present, as separate inherited source blocks. The long catechist paragraph is continuous prose without interleaved notes. `inteUigent` and the damaged “address” token are isolated OCR defects, not missing-font failures. Clear gutter and unclipped lower lines; last paragraph continues on page 4. |
| 4 | Continues the catechesis argument, the faith/instruction discussion, and the directive introducing the regulations. Regulations I, II and III are complete; IV begins at the foot of the right column and continues on page 5. Roman numerals are visible and in order. No omitted section, collided line or apparent marginal/body fusion. |
| 5 | Completes IV, includes V and VI, and continues the implementation, preparation and concluding exhortation. VI's split between “the” and “young” preserves both sides of native pp. 433/434. Source forms including `Hstlessly`, `yo effort` and final `arid` remain disclosed OCR, with intelligible surrounding sentences. The right column ends during the benediction, continuing onto page 6. No severe text stretch, clipping, note fusion or lost numbered regulation. |
| 6 | The continuation completes the genuine benediction, then `Pius X., Pope.`, then St. Peter's, Rome, April 15, 1905 and the second pontifical year. Signature-before-date order is literal to the English printing. The page is sparse but source-bearing. A rule separates the smaller project source/rights colophon; it accurately identifies OCR limitations, historical English publication and unrecorded translator. It is not an apparatus-only extra page. |

Individually inspected pages: **1, 2, 3, 4, 5, 6**. Reused pages: **none**.

## Native publication and boundary evidence

The complete native download was prepared before dispatch; that acquisition was not treated as inspection. This lane independently rehashed the entire 57,295,996-byte, 856-page PDF to `c9678ae4b56518b19278d57afcd88867c2bc525e454bc63d8f0f734441139d43`. Its SHA-1 `2b3927183ef65b84fc609bc31e8b12638a4b2383` and MD5 `ecc1c37521fdb7dddb5fb59bf4ba9369` agree with the full cached provider metadata, SHA-256 `7775873cf5aca553e5393af9ec7063bcff8ca41fea1db38a3921b0cd68d4c9ad`. Acquisition URL: `https://archive.org/download/americancatholic30philuoft/americancatholic30philuoft.pdf`. The acquisition receipt records complete response and exit 0; no download was relaunched.

The complete raw OCR was independently hashed to `2abc21119ef49fa7c02db9f7c5783cd16ef5a92f29851d3daf393d8ff49efb50`; complete XML to `1a0d6f9e7515b2c70663a67c1915667c0c49079776eb95adca6fd96725547f1c`; raw acquisition receipt to `0372064881c0273425eb57131118294dd43dc7ddefc0ce71d86ccdf12fa7a424`. Native PDF ordinals were located using full-PDF `pdftotext -layout`, then confirmed against visible printed folios. XML leaf/artifact ordinals were not assumed to be PDF ordinals.

Bounded PDFs for actual native ordinals **7, 435, 444–454** were extracted with `/usr/bin/pdfseparate`, then rasterized only through `tools/pdf-review --jobs 1`, using the lane's isolated output and cache directories. All 13 single-page PDFs and raster-cache hashes were checked. Original-resolution JPEG quality-95 view derivatives kept the native rasters' dimensions, 1353×2200 for the article and issue pages, 1316×2200 for the annual title. Each of those 13 native images was individually opened. No complete-volume rasterization was performed.

| Native PDF ordinal | Visible evidence actually inspected |
| --- | --- |
| 7 | Annual title: The American Catholic Quarterly Review, volume XXX, January to October 1905, Philadelphia; Ryan is credited as director, not translator. |
| 435 | Issue masthead: volume XXX, July 1905, no. 119, with a 1905 publication/copyright statement. The Latin opening is used only for issue/identity context. |
| 444 / printed 426 | Latin closing, Latin date and Pius PP. X signature end above a separating rule; the distinct English heading, universal address, greeting and body start below it. The English extraction begins at raw LF 22847, not in the Latin closing. |
| 445–450 / printed 427–432 | Body in single native columns, running heads separate above it. Every page's top/bottom ownership and the suspicious OCR/page-break loci were checked. No separate footnotes or marginal summaries occur; references belong inline. |
| 451 / printed 433 | Regulations I–V and the start of VI, with complete Roman-numeral sequence and VI continuing across the page boundary. |
| 452 / printed 434 | Completes VI and continues exhortation/preparation; confirms that the reader's `Hstlessly` and `yo effort` are OCR defects against the printing. Neither was silently repaired. |
| 453 / printed 435 | Final exhortation and inline I Peter reference, benediction, Pius X signature, then complete English date and pontifical year. |
| 454 / printed 436 | A new, unrelated Schiller-centenary article begins; none belongs to this reader. |

The outer source start has two explicit sides: raw LF 22838–22844 finishes the neighboring Latin printing (closing, date, signature), blank lines 22845–22846 precede the English heading at 22847. The English heading/address lead into the greeting at 22860 and body at 22862. The outer end likewise has both sides: benediction 23328–23333, blank 23334, English signature 23335, blank 23336, date 23337–23338, blanks 23339–23340, then the unrelated running head 23341 and Schiller heading 23343/body 23345. These are distinct printing boundaries, not an incipit-based language replacement.

## Excluded running heads: both retained block boundaries

Each exclusion is one complete running-head line. The table names the exact raw-LF block on each side, including the blank-line bounds, and the semantic relationship. `boundary-evidence.json` preserves the complete machine-derived text of both blocks. Native images of both adjacent printed pages were inspected for every entry. There is no excluded substantive gap or missing note. The recipe preserves blank-block interruptions, including native word splits, instead of inventing a new join.

| Excluded raw LF / printed head | Before block; blank LFs before head | After block; blank LF after head | Both-side disposition |
| --- | --- | --- | --- |
| 22888 / 427 | 22872–22885; 22886–22887 | 22890–22923; 22889 | Prior paragraph ends with Osee reference; next paragraph begins “In fact”. Both complete boundaries retained. |
| 22938 / 428 | 22934–22935; 22936–22937 | 22940–22943; 22939 | Same sentence crosses native pages: “Apostle declared, the” → “knowledge of divine things”. Both fragments remain separate, readable blocks. |
| 22991 / 429 | 22983–22988; 22989–22990 | 22993–23005; 22992 | Same paragraph: “humility of” → “soul”. Both source blocks retained. |
| 23043 / 430 | 23038–23040; 23041–23042 | 23045–23051; 23044 | Same word/sentence: `accept-` → `able to God`; both fragments retained, no omitted body text. |
| 23094 / 431 | 23090–23091; 23092–23093 | 23096–23120; 23095 | Same word/quotation: `Con-` → `stitution Etsi minime`; both fragments retained. |
| 23143 / 432 | 23122–23140; 23141–23142 | 23145–23151; 23144 | Same quotation/sentence: “and shall” → “prosper”; both source blocks retained. |
| 23193 / 433 | 23177–23190; 23191–23192 | 23195–23199; 23194 | Prior paragraph ends “imbued with faith”; new paragraph begins “He needs Christian formation”. Both paragraph boundaries retained. |
| 23249 / 434 | 23245–23246; 23247–23248 | 23251–23261; 23250 | Regulation VI crosses native pages: “than do the” → “young”. Its continuation and full remainder are retained. |
| 23300 / 435 | 23288–23297; 23298–23299 | 23302–23311; 23301 | Same preparation paragraph: “any real” → “fruit for souls”. Both source blocks retained. |

The isolated word breaks and the explicit blank-block interruptions do not constitute fused body/notes. No sustained nonsensical sequence, interleaved apparatus or materially unreadable whitespace was found after inspection of both sides. They remain limitations of the accurately labeled OCR reader.

## Notes, findings and limits

No separate historical footnote or endnote occurs in the English pp. 426–435. All references encountered there, including Trent/Benedict XIV, Scripture, Pontifical and Gregory references, are inline historical source content and remain in order. The rule-delimited terminal colophon is project apparatus and visibly distinguishes its source/rights/typography information from the papal wording. No modern source commentary enters the body. The 1905 annual title and July issue evidence agree with the recorded historical United States publication basis; this review does not purport to offer a new legal opinion.

1. **Minor, nonblocking; reader pages 1–5:** disclosed OCR recognition errors and original broken-word forms remain. Native checks confirm representative defects rather than correcting them. These bytes are acceptable for the declared mechanical OCR reader, with no claim to corrected text.
2. **Informational; reader pages 1–5:** nine running heads were removed exactly; inherited blank-block breaks sometimes interrupt a sentence or word. Both sides are present and readable. There is no body/note fusion and no missing source block.
3. **Informational; reader page 2:** the underfull hbox was visually dispositioned; no overflow, clipping or material readability failure results.
4. **Informational; reader page 6:** sparseness is supported by genuine source closing, subscription and dating before the project colophon.

This is a fresh exact-byte fidelity and visual/extent review of the historical English printing. It is not full word-for-word print-image collation, a new English translation, or certification of every English sentence against the Latin act. Translator remains unrecorded. Original OCR punctuation, spelling, source word breaks and some page-boundary paragraph interruptions persist. Acceptance does not promote the source's evidence state, substitute the Latin witness, install bytes or authorize a release.

The lane wrote only `.scratch/direct-baseline-recovery/child-h/`. `report.md` is the immutable proposed content for the canonical target, with its SHA-256 recorded by `reviews.json`. Supporting reproducibility evidence is `audit.py`, `verification.json`, `audit-result.txt`, `boundary-evidence.json`, `replayed-reading.txt`, reader text/metadata outputs, `native-image-map.json`, `native-raster.log`, and the isolated native PDFs/rasters/view derivatives. The native raster helper completed with exit 0 and has no live handle; the acquisition also has no live handle. No canonical source, manifest, PDF, shared raster/cache, code, helper, Git, install or release write was made by this lane. No general handoff ZIP was created: this assigned scratch-result lane returns its report and machine-readable review directly to the coordinator.
