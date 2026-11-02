# Classic papal reader review E — direct baseline recovery

Review date: 2026-10-30. Both exact PDFs **PASS**, subject to the source limitations below. This is a fresh independent page and source-boundary review; no earlier inspection or acceptance was reused. No source, generator, reader, manifest, release, or installed artifact was changed.

Canonical report target: `src/sources/papal-documents/encyclicals-direct-baseline-recovery-e.md`.

## Exact reviewed set

| Document | Language | Reader pages individually inspected | Result | Exact PDF SHA-256 |
| --- | --- | --- | --- | --- |
| Quanta cura — de praecipuis erroribus aetatis (`pius-ix-acta.volume-03.line-00021313.part-18`) | Latin (`la`) | 1, 2, 3, 4, 5 | PASS | `94b30a049dcdcd6fbe2237f5eafe40d80f4306e1e01f93033318a0743582bdd2` |
| Omnem sollicitudinem (`acta.ass.007.ass-007-act-016`) | Latin (`la`) | 1, 2, 3 | PASS | `1c5f2e914c3de0453057fa73b83bacd867d3d1bdcdc00597c7f66c6d17985c79` |

Quanta cura is 45,599 bytes; Omnem sollicitudinem is 33,616 bytes. Every reader page was opened as its own full-size raster using original detail. Contact sheets were not used to establish coverage. Reused pages and reuse proofs are empty for both documents.

## Identity, source fidelity, and PDF checks

The packet SHA-256 is `54672822f9e8619bfbf274d8c532138d0ecb5f1c635612424666405f11796824`. The complete frozen manifest matches `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`; the complete receipt matches `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`. For each document, its entire matching frozen source row equals the packet `source_row`, and its entire matching receipt document equals the packet `receipt_row`. This was whole-object equality, not equality of a reduced list of fields.

All source payload, segment-manifest, source-controller record, available controller-payload, PDF, and reader-raster pins matched. The raster-run manifest matches `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02`; each matching entry has the exact PDF hash and page count. Every file listed in the two per-PDF raster cache manifests was checked for exact SHA-256 and byte size.

Fresh read-only source validation and full body fidelity were rerun with bytecode writes disabled:

```python
sys.path.insert(0, 'scripts')
validated = validate_document(packet_document['source_row'], Path.cwd())
pdf_body_fidelity(Path(packet_document['pdf_path']), validated, packet_document['pages'])
```

Both returned `pass` with method `pdf-raw-source-aware-line-hyphen-nfkc-v3`, exactly matching the frozen receipt. Quanta cura: 21,473 source characters, 17,995 normalized characters, 81 layout hyphens, source-bearing pages 1–5. Omnem: 12,826 source characters, 8,815 normalized characters, 44 layout hyphens, source-bearing pages 1–3. This check permits declared whitespace/compatibility normalization and source-aware physical line-end hyphens; it does not establish lexical correctness of OCR.

`/usr/bin/pdfinfo`, `/usr/bin/pdffonts`, and `/usr/bin/pdftotext` in both `-raw` and `-layout` modes completed with exit status 0 for each reader. Page counts are 5 and 3; both PDFs are unencrypted PDF 1.7, US letter, with no JavaScript or forms. Metadata titles, papal authors, and Latin subjects agree with the selected records. Creation/modification timestamps correspond to the frozen revision `2026-10-30T02:56:48Z`. Both readers use embedded, subset, Unicode-mapped Latin Modern fonts: Roman 17 regular, Roman 10 regular, Roman 8 bold and regular. Raw extraction and individual page views confirm normal left-column then right-column continuation, with no omitted or duplicated body blocks found.

The complete `.log`, `.pass-1.txt`, and `.pass-2.txt` files were scanned, including all lines rather than a tail. Initial PageLabels/cross-reference/rerunfilecheck notices settle on pass 2. Quanta's only final diagnostic is `Underfull \hbox (badness 1466) in paragraph at lines 256--284`; individual page inspection found no corresponding unreadable spacing or overflow. Omnem's final log and pass 2 have no warnings. No fatal errors, undefined references, overfull boxes, or unresolved rerun notices remain.

| Document | Complete log lines read (.log / pass 1 / pass 2) | .log SHA-256 | Pass 1 SHA-256 | Pass 2 SHA-256 |
| --- | --- | --- | --- | --- |
| Quanta cura — de praecipuis erroribus aetatis | 481 / 81 / 68 | `635a68d549ace7dd4027727eea90d445751c3e1cc6a158ff084a36be02508cfe` | `3ca84ad5592344ef274a640e4ed47e236764b68140a940a420bdba40221f998e` | `56cfdd6135f11fc3e3ddc6b89e249e444e0ce1416d37931d7fd2c3f0360f9c2a` |
| Omnem sollicitudinem | 472 / 72 / 61 | `b42e03ef08cc65e0107369d2c98cef6f8e3d2e88fccdbd66b0200c36dc8ec267` | `708ea2ed0bf3590ae314122f7c59fa672ad9b8eccc532a9b84dba0289302749b` | `c79f05cbe694a0bd86f2db5d57cc39443e4589e86751158b616d5b80f0d6d3ac` |

## Quanta cura: exact native witness and extent

The witness used was the complete 753-page, 22,962,145-byte IA PDF `piiixpontificis00ixgoog.pdf`, SHA-256 `d6e0225470b9d8da07c9dc60ac152edf4fbfcf0140a9145913c57ab2036fb6db`, registered as the same 1864 Rome IA edition's `imprint-d6e0225470b9` artifact. The different DCO Google-facsimile delivery was not substituted. This PDF is diagnostic native evidence; its unresolved whole-wrapper redistribution scope is not a grant to redistribute it.

The exact XML correspondence witness matches `f96407d3d9b9db0894e4a2a5b5d43b7da561b06bdcea091bbb8e60e269d5cb1d`; the scandata matches `7f61e16c2c22284563d4febf29ac53d66fce1ab3d46739e62d124c1844a59bdb`; the tracked line map matches `441fb23325324a554e3b6d5a81f7f7eb6f39bbc1bf90a136d69625e12110a9f5`. Whole OCR whitespace tokens equal all 150,455 trimmed XML WORD values. These mechanical correspondences identify pages and exact wording; they do not collate that wording against printed glyphs.

Individually opened native artifact pages **696–710**, including all fourteen selected act pages and the following page. The selected LF26036–26559 ranges map to native pages 696–709. The page-map label sequence is 687–700; native labels were checked in the images. Native page 702's last header digit visually resembles an 8 although the map supplies 693 and the neighboring labels are 692 and 694; the OCR line likewise has 698. This review preserves that pagination ambiguity and relies on exact artifact ordinals. It does not silently repair a printed or OCR label.

The opening retains the episcopal address, `PIUS PP. IX.`, salutation, and body. The final native page 709 retains the blessing, Roman dating clause (8 December 1864), pontificate year, and historical Bernard note. Reader page 5 likewise contains substantive closing text and the note before the terminal apparatus; its sparseness is acceptable.

All fourteen internal source gaps were checked using the raw LF contexts and native pages, with retained text on both sides: LF26070–26073; 26108; 26144; 26180; 26217; 26253; 26289; 26328; 26365; 26402–26405; 26452; 26489; 26523; and 26529. They remove page numbers, the gathering signature 44, blanks, or nonlexical scan/digitizer noise. No missing substantive body or note was found at those gaps. The act's boundary follows the dated closing and Bernard note. Native page 710 begins a new, separately headed `SYLLABVS`; the reader does not claim to include this neighboring constituent. The bound reviewed unit is the selected printing's Quanta cura body, not all associated material in the historical dispatch or volume.

Native page-foot notes on pages 699–701, 703, 705–706, 708–709 remain in source order and occupy separate reader paragraphs. Body continuations appear after explicit paragraph boundaries on both sides of these blocks. Examples include the `liberta-` / `tem` continuation around the Mirari citations on reader page 2 and the `omnibus` / `sese` continuation around the Cyprian citation on page 4. A historical page-break interruption is not, by itself, body-note fusion. No sustained body/note fusion, clipping, overlap, or nonsensical reordered stream was found.

Nonblocking transcription limitations: the native decorative Q is absent from the OCR opening (`uanta` on reader page 1); the OCR preserves damaged letter readings in the address and body, unusual dash/hard-hyphen spacing, and damaged citation glyphs such as the Quo graviora note on reader page 3. These are visible limitations of the explicitly uncorrected and uncollated OCR. They prevent treating this as a corrected text or an image-collated edition. The body remains readable within that declared scope.

## Omnem sollicitudinem: exact native witness and extent

The complete native delivery is the 784-page Vatican `ASS-07-1872-73-ocr.pdf`, SHA-256 `c8e55379b19d1ce60da3ee00560dab1e064004e23bc3fe6694c7a16f63dfbc8d`, 3,253,406 bytes. It is an **OCR reconstruction**, not an original facsimile. Its renderings cannot independently establish the original printing's exact glyphs or typography.

A fresh complete `/usr/bin/pdftotext -layout` extraction matches its registered parent SHA-256 `80d8a1e72a90b04e35c4933a12a33bf1e2dd7352ea59701671a47bea1591d49a`. Retaining exactly historical LF49–31751 with LF joins and one terminal LF reproduces the whole tracked historical derivative SHA-256 `5b64eabc613113dd83fb03b0798d99c1644d274f3a8d6482cdd97b803624f03d`.

Individually opened native artifact pages **629–634**, located in the complete layout extraction. The opening page at ordinal 629 has no visible printed page number; following pages visibly carry 630–634. It begins with the journal rubric, papal heading, `EPISTOLA`, episcopal address, salutation and incipit. The selected record begins at the papal heading and omits the generic journal rubric. The final native page 634 contains the blessing, `MDCCCLXXIV`, pontificate year and `PIUS PP. IX.` signature. Reader page 3 preserves them before the apparatus. It is a genuine source-bearing final page.

All five internal gaps (historical derivative LF25535, 25580, 25620, 25661 and 25698) omit only formfeed/page-number/running-head furniture. The retained preceding and following body or historical note contexts were checked. Native historical notes on ordinals 629–632 remain separate paragraphs in the reader, in source order; the source's continuing body resumes across explicit paragraph boundaries. No neighboring act, substantive omission, sustained fusion, or material whitespace unreadability was found.

The native reconstruction itself carries letterspaced names/emphasis and broken line-end forms. Those survive extraction as strings such as `Q u a`, `C l e - mens`, and `N o s`; the reader also retains OCR/name-glyph errors. This is acceptable only as the disclosed mechanical OCR reading edition. No lexical correction or original-facsimile collation is claimed.

The registered nominal ASS 7 (1872–73) identity, act date 1874-05-13, and edition's 1915 title-leaf evidence with its conflicting ANNO OCR remain distinct. The source note's shorthand “ASS 7 (1872)” does not resolve those conflicts. This review confirms the selected reconstruction's dating clause but does not silently correct the container chronology or authenticate the original publication.

## Review method, retained evidence, and limits

Bounded native PDFs were extracted using `/usr/bin/pdfseparate -f 696 -l 710` and `-f 629 -l 634` from the verified whole deliveries. Only the repository helper rendered them:

```sh
PYTHONDONTWRITEBYTECODE=1 tools/pdf-review \
  --output .scratch/direct-baseline-recovery/child-e/native-rasters \
  --cache .scratch/direct-baseline-recovery/child-e/native-cache --jobs 1 \
  .scratch/direct-baseline-recovery/child-e/native-pages/*.pdf
```

The helper completed with exit 0. All 21 resulting native pages were individually opened at original detail. No inherited native or reader views count toward this review. All native rasters were below 1 MB, so no display recompression was needed.

This is full reader-page visual review plus bounded native opening/final/notes/exclusion checks. It is not whole lexical collation, historical authentication, a rights reanalysis, or proof that either record exhausts every related document. Mechanical fidelity leaves source errors untouched. PASS concerns these exact PDFs as accurately disclosed OCR readers, within the exact source selections.

Scratch evidence: `checks.json` SHA-256 `0963e4bc1dc46ff60dca534e54116f2ed2862f7910ba45160319636aa07ef4cf`; `native-pins.json` SHA-256 `ff07ba2c7872d55477a37dc40ced366d34ff588ddab181449884a0bcc13ae037`; `native-display-manifest.json` SHA-256 `cf68080e077b2ae4302022fdda6f36007e6f6d2cf4e8d20a76c0e86105f16e96`. Each resides in `.scratch/direct-baseline-recovery/child-e/`, alongside complete extracted reader text, boundary contexts, native maps and isolated review outputs. The generic ZIP handoff was not requested for this assigned scratch-result lane; no ZIP was created. No live process handles or remaining blocking checks exist.

## Source and segment pins

| Document | Complete source payload SHA-256 | Segment manifest SHA-256 |
| --- | --- | --- |
| `pius-ix-acta.volume-03.line-00021313.part-18` | `3a788e20d82b5eb754d99242edaf43006aa915d8ebdfd9e1a62e73a1804e19f8` | `8ca009cd3baf37c4c5ce973ba41ea32838d7ece2d8b60992f9027c2fb5b3d5c8` |
| `acta.ass.007.ass-007-act-016` | `5b64eabc613113dd83fb03b0798d99c1644d274f3a8d6482cdd97b803624f03d` | `7190fb4d612d9f8e47ace52c18cf21a1f38eeb745f0bbb338a6f7e9edfb9a8bd` |

All source-controller record pins verified:

- `artifact.papal-collections.pii-ix-acta-pars-prima-volume-3.1864-rome-ia-mul.ocr-3a788e20d82b` — record `66c11581ea1a606c756724ebf8b064593347cdeaf59ade39e16eea8354278eda`; payload `3a788e20d82b5eb754d99242edaf43006aa915d8ebdfd9e1a62e73a1804e19f8`.
- `artifact.acta-papal-archives.ass.007.historical-text-5b64eabc` — record `e1e76f696f273de386f3c8952065aa619bc172bcd11368cf3268bc25a17bc804`; payload `5b64eabc613113dd83fb03b0798d99c1644d274f3a8d6482cdd97b803624f03d`.
- `artifact.acta-papal-archives.ass.007.extracted-text-80d8a1e7` — record `51d16c24e01a769c95b7669c6baad17bd5167fb9de140624c11a3a4662d330a8`; payload `80d8a1e72a90b04e35c4933a12a33bf1e2dd7352ea59701671a47bea1591d49a`.
- `artifact.acta-papal-archives.ass.007.vatican-pdf-c8e55379` — record `faea31adccca8e32585972fdca244de8ad07dc60ee435cd5a19e57e9d60a8a71`; payload `c8e55379b19d1ce60da3ee00560dab1e064004e23bc3fe6694c7a16f63dfbc8d`.
