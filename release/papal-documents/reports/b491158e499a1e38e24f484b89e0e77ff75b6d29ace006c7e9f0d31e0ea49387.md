# Aeterni Patris: independent cold review, packet 38

**SOURCE RECOVERY/ORDER: PASS. PDF: PASS, all 9 pages.** No material blocker was found within the assigned source-recovery, ordering, and reading-layout scope. These are independent judgments of the exact replacement bytes below; earlier source or PDF reviews supply no visual acceptance here.

| Identity | Exact reviewed value |
| --- | --- |
| Document | `acta.ass.012.ass-012-act-002`, Latin; Leo XIII, 1879-08-04, *Aeterni Patris Unigenitus Filius* |
| Packet SHA-256 | `7038df3d91006cd4ea14e6c1481c5083f634b584c6c98a7d49f743ee93155ddc` |
| Source SHA-256 | `60f42818f98eeb6303acfe7f595169cd8138cb6e065fa0f6050ddd8cc9598932` |
| PDF SHA-256 | `a43b7c06ac82fd30235b6582c5929cbdf128826af512b2f1319332baa7772160` |
| PDF extent | 9 Letter pages, 71,572 bytes |
| Receipt SHA-256 | `abad3b4218a75cf70add5b9bfc4cfabaf868dc4302755d1f633692bfd20c1b0f` |
| Frozen manifest SHA-256 | `02980284a29028028f9736f5c6a3aa05790e85eaa8bb3662442a08b21b97e129` |
| Deterministic recovery recipe SHA-256 | `99bd7f54ad36b45be57aae0ae46829701ca67675a1a5e5f69bc1d3211f1fec86` |

The reviewed PDF is the packet's `readers-final` PDF under `.scratch/aeterni-missing-note-recovery/`. The final canonical report destination is `src/sources/papal-documents/encyclicals-refinement-cold-38.md`; the reviewer leaves that destination unwritten for coordinator integration.

## SOURCE RECOVERY/ORDER — PASS

The original parent PDF, SHA-256 `017009649925ced58e3f51a80eac34dc0f858a8e4b06e6992bf6e663e56b8993`, and the 19-page native excerpt were independently hashed. Complete `pdftotext -raw` stdout and the prescribed default ElementTree page serialization from `-bbox-layout` were freshly compared for every parent page 97–115 against excerpt pages 1–19. All 19 raw-text hashes, bbox hashes, and page mappings match. This establishes the excerpt's text and geometry mapping, including the existing raster cache; it does not establish that the reconstructed text is a facsimile of the original printing.

All 17 native note regions were freshly viewed as individual quality-95 JPEG crops made only in reviewer scratch from the pinned native rasters. Native pages 97, 110, and 115 were also opened individually at original resolution to inspect opening/protocol, bitmap placement, closing, signature, and final-note context. Each old note group was independently matched to its native bbox WORD identities and values, with every native note WORD used once. The retained 57 source slices exhaust all 35 selected old note LF rows, without gaps or overlapping byte ranges, and are each used once. The verification record retains all 409 native note WORD identities, boxes, exact slice values, and slice order. Two-column groups keep every left-column cell before the right column; the single-column groups retain their whole blocks.

| Native page | Old source LF rows | Fresh geometry and order judgment |
| --- | --- | --- |
| 97 | 3933 | PASS: single Matthew citation; journal footer furniture is distinct. |
| 98 | 3976 | PASS: left note 1, then right note 2. |
| 99 | 4016–4018 | PASS: left notes 1–2, including the `1. VII, c 3.` continuation of note 2, then right notes 3–4. |
| 100 | 4057–4060 | PASS: left notes 1–4, then right notes 5–7. |
| 101 | 4100–4103 | PASS: left notes 1–3, then right notes 4–5. The separately positioned damaged raised `1` and `(5` remain literal, without label repair. |
| 102 | 4144–4145 | PASS: left notes 1–2, then right notes 3–4; the complete *Apostolici regiminis* citation remains together. |
| 103 | 4188 | PASS: single Marcellinus citation. |
| 104 | 4229–4230 | PASS: left notes 1–2, then right note 3. |
| 105 | 4273 | PASS: left note 1, then right note 2. |
| 106 | 4315–4316 | PASS: left notes 1–2, then right note 3. |
| 107 | 4358 | PASS: single *Triumph antis* citation; old word division remains literal. |
| 108 | 4399–4400 | PASS: left note 1, then the complete right note 2; separately positioned `n`, `ä`, and `e` remain literal in their disclosed OCR order. |
| 109 | 4442 | PASS: single *In Ordine* citation; damaged `fi)` remains literal. |
| 110 | 4481–4486 | PASS: notes 1–3, recovered bitmap note 4, then damaged old note 5 with its top-right `Cancell. Univ. Tolos.` continuation, followed by notes 6–8. The `Aug. 1752.` line continues note 7. The old raised `a` remains literal. |
| 111 | 4528 | PASS: single Beza–Bucerus citation. |
| 112 | 4569–4570 | PASS: left notes 1–2, then right note 3; damaged labels and words remain literal. |
| 115 | 4690 | PASS: one final historical citation block containing notes 1–3, after the actual dating and signature. |

The pinned MIT replay implementation was read before execution. The superseded metadata-dependent recipe was not executed. Fresh deterministic replay checked its input, model, tool, and helper hashes, extracted the exact bitmap PNG, recreated the stripped crop, ran the pinned Tesseract model and options, reproduced the raw OCR and TSV, replayed all 17 old note groups, and matched the complete final source hash. An independent assembly from the explicit slices also matches the replay and canonical source. All 745 selected BODY LF rows retain their exact bytes and original order; their concatenated SHA-256 is `1afe583e0ccfa45053d13e3a20a2e692223d999138bb53ae4965a1220691dc60`. All 780 originally selected LF rows are accounted for by those body rows and the 35 note rows.

The missing note's original pixel mapping was independently checked against the full parent, not inferred from a producer statement: parent page 110 has exactly one 228×71 one-bit image, ordinal 0, object 443, at 200 dpi. Fresh extraction from the parent reproduces PNG SHA-256 `419ddfe70959c624024247b518d1d09852fefad172d9edf0ae92c83f87c1d3b6`. Parent and retained witness PBM pixel bits are identical: 2,059 bytes, SHA-256 `d709f1aa5129bfb3bf1d7b48c55ae3e5dba038e065b8c8cc84951ff11e4ce7cc`. The actual parent bitmap and freshly replayed deterministic crop were both opened at original resolution. The visible reading agrees with the fresh raw OCR bytes `(4) Bulla Verbo Dei.\n` (21 bytes, SHA-256 `a9a485ed3c45c038bf67541ea6c818075b64adbc409602969a55ea98f0d5d7de`). The crop exactly matches SHA-256 `b0faf50c9b6ed374e7494a2a7186377bd7b6d200a7bf5675905df4e9892586db`.

Those 21 raw OCR bytes plus two added LF bytes are inserted at ordered-old byte offset 34,322, between the existing notes 3 and 5. Removing exactly that addition restores ordered-old SHA-256 `330934c25e431e620929f7139b5e889c7bb0b58f0329a3bf6b7dd47791692961`. The replacement is explicitly a new composed derivative; **the final source is not a global permutation of the old bytes**. No old lexical repair, abbreviation expansion, or silent label normalization was made or accepted. The prior source and failed PDF `a765646c…` remain historical records, with the replacement explicitly identified by the frozen supersession.

## PDF — PASS, pages 1–9

The pinned reader contact sheet and each of the nine current full-page rasters were freshly opened, individually, at original resolution with automatic image detail. No prior visual review was reused. Reader rasters are cache reuse only. The complete source-to-PDF check was independently rerun through the pinned current `validate_document` and `pdf_body_fidelity`: PASS, 46,197 source characters, 38,449 normalized characters, 223 allowed layout hyphens, source-bearing pages 1–9.

| Reader page | Fresh full-page finding |
| --- | --- |
| 1 | PASS: compact title, pope, date, and Latin identification; complete protocol/address and opening; separate native-page 97–98 notes. The long original capital address remains within its column. |
| 2 | PASS: normal left-then-right continuation; native-page 99–100 note blocks are separate and legible, including note 2's continuation. |
| 3 | PASS: native-page 101–102 notes are distinct paragraphs; damaged label fragments remain visible and literal. |
| 4 | PASS: native-page 103–104 note blocks are distinct from the surrounding body. |
| 5 | PASS: native-page 105–106 notes retain their order and separate paragraphs. Disclosed old OCR debris remains literal. |
| 6 | PASS: native-page 107–108 notes remain separate; the raised-letter OCR sequence is retained without clipping or substitution. |
| 7 | PASS: recovered `(4) Bulla Verbo Dei.` is visible after note 3 and before the old note 5. Note 5's continuation is complete. Notes 7–8 continue normally at the next column top; the subsequent Beza–Bucerus citation is separate. |
| 8 | PASS: native-page 112 notes remain separate; ordinary two-column body flow. |
| 9 | PASS: substantial source text, concluding blessing, actual dating clause, `LEO PP. XIII.`, and final historical citation block precede the ruled project apparatus and compact rights colophon. This is a source-bearing final page. |

No clipping, overprint, missing rendered glyph, material note/body fusion, reversed column flow, or apparatus-only final page was observed. Notes retained at historical source-page breaks sometimes interrupt a continued body sentence; the direct TeX `\par` evidence and full-page views show these as separate note paragraphs, consistent with the source-order policy. The single underfull-box warning (badness 2837, original capital address on page 1) has no observed clipping or overlap. No fatal, undefined-reference, missing-character, or overflow warning was found in the final log.

`pdfinfo`, `pdffonts`, and text extraction succeed. The PDF is unencrypted PDF 1.7; its title, author, language subject, and revision timestamps agree with the frozen row. All four font subsets are embedded and Unicode mapped. Its size is below both repository size-review triggers. No qpdf executable was available, so no qpdf check is claimed.

## Verification and limits

Fresh verification made 258 pinned-file checks with zero mismatches, including packet/brief, full frozen row equality, segment/controller metadata, artifact manifests/payloads, current helpers, retained recipe/spec/source review, final producer JSON, delivery pins, reader/native raster files, cache-object files, and cache receipt identity. Recipe tool and model pins were independently checked as well. Schema-2 artifact `page_count` is supported by the current library: fresh **uncached whole-library validation exited 0**, reporting artifact=10,896, corpus=5, edition=14,277, passage=9,140, segment=10,873, work=10,925, bindings=4,398. Every Python/source-library invocation used `PYTHONDONTWRITEBYTECODE=1 TRIPTYCH_LIBRARY_CACHE=0`; no implicit shared library cache write was requested. The final retained producer proof was checked as producer evidence, not used as independent acceptance.

Actual visual source inspection comprises all 17 native note regions, full native pages 97/110/115, the actual extracted historical note bitmap, and the deterministic crop. The **bitmap note alone** is checked as historical image content. The surrounding native PDF is a hybrid archival OCR reconstruction; neither these page views nor exact replay establishes whole-act original-print glyph identity or lexical collation. Disclosed OCR defects and unusual word divisions remain. This review grants no independent translation, historical-edition identity, new rights clearance, whole-source lexical, installation, release, or deployment approval. It closes the assigned source-recovery/order and exact nine-page PDF review gates only.

Reproduction and complete mechanical evidence are retained in reviewer scratch as `verify.py`, `verification.json`, `source-library-validation.txt`, the deterministic replay outputs, and individually named native-note crops. Only the coordinator owns admission, canonical copying, and installation.
