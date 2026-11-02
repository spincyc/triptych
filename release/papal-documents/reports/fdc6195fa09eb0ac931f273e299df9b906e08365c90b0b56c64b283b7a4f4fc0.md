# Independent cold review — packet 26b

PASS for the three-page Latin reader of **DE CONSOCIATIONIBUS DIOECESANIS**, Pius XI, 1924-01-18 (`acta.aas.016.aas-016-l00032`, `la`). No blocking source-boundary or layout finding was found within this review's stated bounds.

The exact reviewed PDF is `.scratch/encyclical-notes-12/readers/1924-01-18-acta-aas-016-aas-016-l00032-af276ffa-la/1924-01-18-acta-aas-016-aas-016-l00032-af276ffa-la.pdf`: **37,605 bytes**, **3 actual pages**, SHA-256 `d389df956a2410b8e8d804dc9858ca115468f46861fb99e828b0d30154ef72b6`.

This is a fresh independent inspection. Reader pages **1, 2, and 3** were each opened separately from their full-resolution page rasters using original-image loading and automatic display detail, after inspecting their contact sheet. No prior visual acceptance was reused. The native evidence contact sheet and its full-resolution page were also opened separately: subset page 1, independently mapped to actual parent PDF page **11**. No new raster generation or cache mutation occurred.

| Reader page | Direct visual finding |
| --- | --- |
| 1 | Title, pope, date, and Latin identification are clear. The full address/protocol and opening are present. The long initial paragraph has widely justified all-capital lines and literal OCR spacing, but remains legible. Both columns, margins and page number are clear; no clipped or overlapping text was observed. |
| 2 | Both columns continue in reading order. Paragraph starts and column endings remain distinguishable. Source hyphens and OCR word divisions are visible; no overlap, clipping or missing-glyph box was observed. |
| 3 | Source-bearing text continues in both columns. The existing `I PETR.` note remains a visibly separate block at its retained source-page break, interrupting `vestro-` / `rum` in the preserved source order. The dating clause and `PIUS PP. XI` remain intact. The repaired Hebr./Ps./Cor./Mach. note material begins as its own indented paragraph after the subscription. A rule separates the smaller terminal source apparatus; the rights colophon is legible. This is not an apparatus-only final page. |

The compilation log contains 11 underfull hbox warnings in the opening paragraph, matching the receipt. Their visible effect is the wide protocol spacing described above; direct inspection found it readable. The log scan found no overfull box, fatal/LaTeX error, undefined reference/control sequence, or missing-character diagnostic.

All **40 unique packet-pinned files** checked independently matched their SHA-256 and declared size where supplied. This includes the exact brief, source payloads and artifact records, segment controller, retained partition specification, current helper implementations, frozen/source-selection manifests, receipt, producer evidence files, native parent and excerpt PDFs, review runs, cache receipts, and every listed reader/native raster. Producer evidence was treated as provenance, not acceptance. The frozen manifest contains exactly one matching id/language row, fully equal to the packet's `source_row`. The selected segment TOML and all packet artifact TOML metadata equal their pinned packet objects. Receipt source/artifact/segment/ranges, PDF path/hash/page count and render revision agree with the selected row.

| Controlling input | Independently verified SHA-256 |
| --- | --- |
| Frozen manifest | `3a0c1859166f6eec988dc66426072e15d874a21d3f7b50064c02d42ef63c0258` |
| Render receipt | `2944e41897681eb4afc0cc49ff8ea036f984f292b8367df4af483f0e3e4f46f5` |
| Selected derivative text | `2d212df64e84a104949179b211325752a625e156aaa1106a7a68f86fe7cc9d67` |
| Segment controller | `0fcdf1dc01e8ce0dfe18efcd21bd65c85ec766f55eccc195b9a9be8e03783ce6` |
| LF partition spec | `281998a4fb2f4ff9d9adc26abb31265306b8ac859ea03d5c877dece08575babd` |
| `scripts/_papal_source_notes.py` | `a0b31d45f498bec3a12a29cdff28da38f3e01cc02c50e5de8a9a65e4a82a9d57` |
| `scripts/_typeset_papal.py` | `1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146` |

The independent read-only replay was:

```sh
PYTHONDONTWRITEBYTECODE=1 tools/papal-source-notes check --spec src/sources/works/holy-see/acta-apostolicae-sedis/editions/1924-acta-aas-016/artifacts/note-spec-consociationibus-la-281998a4fb2f/spec.json --out src/sources/works/holy-see/acta-apostolicae-sedis/editions/1924-acta-aas-016/artifacts/note-blocks-consociationibus-la-2d212df64e84/text.txt --json
```

It exited 0 with `status: pass`, one note group, 14,362 derivative bytes and 260 physical LF records. Selected non-LF bytes and source order are preserved; selected non-LF SHA-256 is `924e8d5d3ce022bbf059fba10a81cfa827d86624c4f7e76666132c4289f69da0`. An independent direct byte comparison also confirmed equality after removing only LF between the prior selection, derivative and selected derivative ranges.

With `PYTHONDONTWRITEBYTECODE=1`, the pinned current typesetter's `validate_document(source_row, root=repo_path)` passed its selected-document/source-controller validation, yielding 12 blocks and 14,327 selected source characters. The independent `pdf_body_fidelity(pdf_path, validated, 3)` replay passed using `pdf-raw-source-aware-line-hyphen-nfkc-v3`: 11,731 normalized source characters, 76 permitted line-ending layout hyphens, source beginning on page 1 and ending on page 3. This checks the entire selected source stream in PDF content-stream order with the declared normalization; it is not lexical collation.

`pdfinfo` reads a three-page Letter PDF 1.7 without encryption, suspect structure, forms or JavaScript. Its title, author and language subject agree with the row. Creation and modification dates both equal the pinned revision `2026-10-30T11:59:25Z`. `pdffonts` reports four Latin Modern fonts, all embedded, subset and Unicode-mapped. No font or structure blocker was found in these checks.

Native parent `.scratch/papal_pius_xi_review/AAS-16-1924-ocr.pdf` independently hashes to `ff70624da45b0b1bbd8700308147bcfdd3082420433b19d8144d26dc220b659d` and has 564 pages. The exact one-page excerpt hashes to `df6c18527407fa80e3ac6c8dbd65bee6a9a522b8cce0f21546910e99ca4c6206`. Actual parent page 11 and excerpt page 1 independently produce equal complete `pdftotext -raw -enc UTF-8` stdout, SHA-256 `0a39a5891a4d41e9c941368d66b92abbfd00772f449a016415fe9752ec592973`. Their first parsed `pdftotext -bbox-layout` page elements, serialized with standard-library `ElementTree.tostring` defaults including the tail, are byte-equal and hash to `1b974dcd8e7255c2fdafd643581c340a92539e5d67ea34813bb798b2673a0cae`. All 272 word values and coordinate attribute records are independently equal.

The directly viewed native page has one body column, a dating clause, the subscription, and six smaller-type note rows below it. Subscription boxes end at y=577.6435 pt; notes begin at y=589.85155 pt and end at y=662.293 pt on a 510.25 × 737 pt page. This geometry supports treating original historical LF **283–293** as a separate note block after LF **282**, `PIUS PP. XI`. The exact LF-free anchors independently match: LF 282 `d7c98bead90431deaa33a50aeb072c943692d781668f1306ef78435a7c10f1d1`; LF 283 `b50e8185e5da7741c78cf91f8dbbac0c3e4990304d6d66bdec2f282419aa6d87`; LF 293 `3127406d077bf261174032cebea07bdf94d1546895599157a08786a5a81c9ba3`. The generated body TeX explicitly ends the subscription paragraph before the note paragraph, and the reader image independently confirms their visible separation.

Source inspection was bounded to actual native parent page **11**, the historical text's physical LF **20–65** and **233–299**, all excluded interior page-head gaps at LF **57–58, 94–95, 131–132, 168, 206–207, 245**, and the ending boundary at LF **294–296**. The prior segment and selected edition records and the complete generated body TeX were read. Excluded gaps contain running heads/page labels; LF 296 begins the following translation label. The complete selected text received mechanical byte and PDF-fidelity comparisons. Native page 10 and other native source pages did not receive visual collation in this lane.

This PASS covers the assigned exact reader bytes, every reader page and the bounded source-note repair checks above. It does not certify translation accuracy, whole-source lexical accuracy, original-print glyph identity, new historical-source identity/intake or rights clearance, installation or deployment. The native PDF is an archival OCR reconstruction; literal OCR errors, awkward word divisions, source-page interruptions and reference marks remain. Existing source rights/evidence states were checked for agreement, not promoted. No separately assigned special acceptance gate was supplied in this packet. All writes are confined to the exclusive reviewer scratch; the coordinator must copy these exact report bytes to the packet's canonical report path.
