# Independent baseline continuation review — packet 21

Outcome: **8 PASS / 0 CHANGES_REQUIRED** with the specific source-OCR qualifications below. Fresh coverage is **8 PDFs / 39 of 39 pages**. All 39 pages were viewed on the existing contact sheets and all 39 were also opened at full raster resolution. No prior inspection claims or acceptance decisions were inherited.

## Exact evidence and checks

- Packet: `.scratch/encyclical-ready-package/baseline-review-packets/21.json`; SHA256 `d4c039a1faf68cd0c3645a59dc983906688bdce66b9360cb16d0651f47a49d61`.
- Canonical report destination: `src/sources/papal-documents/encyclicals-baseline-continuation-21.md`. The coordinator may copy these exact report bytes there.
- Receipt SHA256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
- Frozen input-manifest SHA256: `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`.
- Raster-manifest SHA256: `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02`.
- All 205 pin checks passed: common brief; exact PDF, receipt and frozen manifest bytes; exact source payload and segment where present; every source-controller record and available retained payload; receipt and frozen source-row equality; PDF/raster page counts; raster PDF binding; hashes of every cached full page, thumbnail and contact sheet. Restricted upstream payloads have no local payload path and were not reacquired.
- The existing repository `pdf_body_fidelity` check was independently rerun read-only against the complete selected LF ranges/source for all eight readers. All passed; every selected source begins on page 1 and ends on the actual final page. Source endings were also checked visually against the selected source. This confirms retained text order/completeness relative to those inputs, not correctness of OCR.
- `pdfinfo` and `pdffonts` succeeded for every PDF: unencrypted PDF 1.7, letter pages, expected title/issuer/language metadata, four embedded fonts each, tracked modification time 2026-10-30T02:56:48Z. Extracted word boxes remain inside their media boxes. No visual column collision, clipping, overlap, missing glyph or project-apparatus-only page was found.
- Pin and mechanical evidence is in `pin-verification.json`, `pdf-verification.json` and `pdf-N-info.txt` / `pdf-N-fonts.txt` beside this report. Existing raster directories were only read. No renderer, reraster, installation, canonical edit, Git mutation or delegation was performed.

## Coverage and dispositions

| Reader | Language | Pages viewed on contact sheet | Pages opened full-size | Status | Exact PDF SHA256 |
| --- | --- | --- | --- | --- | --- |
| Aeterni Patris (`papal.leo-xiii.hf-l-xiii-enc-04081879-aeterni-patris`) | la | 1, 2, 3, 4, 5, 6, 7, 8, 9 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | PASS | `1a60751dc29ce982d7f0762944ca4fe33bd3d3afd1fd148717f455540d2c2e77` |
| Rite Expiatis (`papal.pius-xi.hf-p-xi-enc-19260430-rite-expiatis`) | la | 1, 2, 3, 4, 5, 6, 7, 8, 9 | 1, 2, 3, 4, 5, 6, 7, 8, 9 | PASS | `0d4231c5552d04af2b1d951cb25a6bd472cbd9c044fbb2671eb6bafb2bb64133` |
| Rerum Omnium Perturbationem (`papal.pius-xi.hf-p-xi-enc-26011923-rerum-omnium-perturbationem`) | la | 1, 2, 3, 4, 5, 6 | 1, 2, 3, 4, 5, 6 | PASS | `b7d65b7763555759b1dd7b42ea2c86efff21b14501dbf8b41148fe7e51a3028f` |
| PIE PP. XI NOS   CHERS FILS ET VÉNÉRABLES FRÈRES SALUT ET BÉNÉDICTION APOSTOLIQUE (`acta.aas.016.aas-016-l00298`) | fr | 1, 2, 3, 4 | 1, 2, 3, 4 | PASS | `47ed1dc6c3c91688aaea3200a0df5c23818c85f5eb5e32b5d044ec1ea779ac70` |
| Pergrata (`papal.leo-xiii.hf-l-xiii-enc-14091886-pergrata`) | la | 1, 2, 3, 4 | 1, 2, 3, 4 | PASS | `730c4971dfcf019b0d759f9c3e3cbe0fbe709ad68ce14fee7f368fa7e88400f7` |
| Augustissimae Virginis Mariae (`papal.leo-xiii.hf-l-xiii-enc-12091897-augustissimae-virginis-mariae`) | la | 1, 2, 3 | 1, 2, 3 | PASS | `1a9ab41c0a3c32cf8e019b2a58508f062050c018b4a2a3a845c8850f28b0e47e` |
| Litterae de die expiationis in suffragium animarum in Purgatorio (`acta.ass.020.ass-020-010`) | la | 1, 2 | 1, 2 | PASS | `f2a28722db1d0dd5e8aa95ed1eab0171287a1bfa856284afa4b11ce3b9e83b51` |
| Congratulations to the American Hierarchy (`papal.leo-xiii.hf-l-xiii-enc-15041902-in-amplissimo`) | en | 1, 2 | 1, 2 | PASS | `f0f8a78e2081d293a3d8e41fc5bbb64d399da9ea4e8a620da85ebd0371af6149` |

Each document used its packet `raster_dir`, `contact-sheets/sheet-001.png`, and `pages/page-N.png`. The full-size opens include every first/final, dense, sparse, note-bearing and suspicious page. `individually_inspected_pages` records actual fresh inspection; `reused_pages` and `reuse_proofs` are empty.

## Findings by reader

### 1. Aeterni Patris — PASS

- **info**, page(s) 9: The sparse final page contains substantial historical closing prose, the 4 August 1879 dating clause and LEO PP. XIII before compact project apparatus; it is source-bearing.

Source limitation: Historical witness: Acta Sanctae Sedis 12 (1879-1880), pp. 97-115. Uncollated normalized web transcription; source wording and numbering retained apart from the explicitly recorded corrections and apparatus exclusions.

### 2. Rite Expiatis — PASS

- **info**, page(s) 9: Historical references [1]–[35] remain separate, legible entries following the dating clause and PIUS PP. XI. Their continuation from the left to the right column is clear.

Source limitation: Historical witness: Acta Apostolicae Sedis 18 (1926), pp. 153-175. Uncollated normalized web transcription; source wording and numbering retained apart from the explicitly recorded corrections and apparatus exclusions.

### 3. Rerum Omnium Perturbationem — PASS

- **info**, page(s) 6: Sparse final page retains the end of the blessing, the 26 January 1923 dating clause, PIUS PP. XI and individually addressable historical references (1)–(12).

Source limitation: Historical witness: Acta Apostolicae Sedis 15 (1923), pp. 49-63. Uncollated normalized web transcription; source wording and numbering retained apart from the explicitly recorded corrections and apparatus exclusions.

### 4. PIE PP. XI NOS   CHERS FILS ET VÉNÉRABLES FRÈRES SALUT ET BÉNÉDICTION APOSTOLIQUE — PASS

- **warning**, page(s) 3, 4: Bounded source-OCR defects remain in the historical notes: p4 has “II Machab., xin, 1%” and a marker rendered as “«”. The reference paragraphs remain separate from the body; p3 references 1–4 are recognizable within one permitted source-note block. The notes are not fused into a body paragraph, and no sustained unreadable passage was found. Citation accuracy is outside this visual acceptance.
- **warning**, page(s) 3: One nonword OCR punctuation row (: : — -"- : — -) appears between body ré- and concilier at the lower left column. It interrupts a word across a source-boundary paragraph break, but the surrounding sentence remains readily readable. Extent: one punctuation row and one split word, not a sustained unreadable body passage.
- **info**, page(s) 4: The ending blessing, 18 January 1924 dating clause and . PIUS P P . XI remain present above the terminal references; no source-ending loss or apparatus-only page was found.

Source limitation: AAS 16 (1924). Exact mechanical UTF-8 pdftotext -layout ranges. Original OCR spelling, spacing, internal source notes, signatures and dating clauses retained. No facsimile collation; printed page labels left unknown rather than inferred from PDF page ordinals. Boundaries and every interior excluded gap received independent review; exact source rows were restored where an earlier header classifier had omitted semantic text.

### 5. Pergrata — PASS

- **info**, page(s) 4: Sparse final page carries real closing prose, the 14 September 1886 dating clause and LEO PP. XIII; the identification date agrees with the visible source closing. The longer source note and URL remain within the column.

Source limitation: Historical witness: Acta Sanctae Sedis 19 (1886-1887), pp. 209-215. Uncollated normalized web transcription; source wording and numbering retained apart from the explicitly recorded corrections and apparatus exclusions. The official indexes give conflicting act dates. The reviewed act date is 1886-09-14, identified at https://www.vatican.va/archive/ass/documents/ASS-19-1886-87-ocr.pdf printed p. 215, closing dating clause.

### 6. Augustissimae Virginis Mariae — PASS

- **info**, page(s) 1, 3: The literal source divider on p1 is retained publishing furniture. The final blessing, 12 September 1897 dating clause and LEO PP. XIII are legible on p3 before compact apparatus.

Source limitation: Historical witness: Acta Sanctae Sedis 30 (1897-1898), pp. 129-135. Uncollated normalized web transcription; source wording and numbering retained apart from the explicitly recorded corrections and apparatus exclusions.

### 7. Litterae de die expiationis in suffragium animarum in Purgatorio — PASS

- **warning**, page(s) 1: Bounded retained OCR garble occurs at the protocol “U T T U M S Sanctissimi” and individual body loci “Quod anniversari us-Sacerdotii .Nostri”, “D mi i num -Nostrum Iesum Christum”, and “iunge- i-etur”. The damage affects a short protocol label and scattered words/divisions, not a sustained body passage; the surrounding Latin paragraphs remain usable. Acceptance does not certify these readings or infer lexical corrections.
- **info**, page(s) 2: The very sparse final page genuinely retains the historical dating-clause continuation (solemni Paschatis an. MDCCCLXXXVIII Pontificatus Nostri undecimo) and LEO PP. XIII. Its sparseness is acceptable; it is not a project-apparatus-only page.

Source limitation: ASS 20 (1887). Exact LF ranges of the separately hashed pdftotext -layout UTF-8 Unix derivative; Vatican OCR reconstruction, not original-print facsimile or collated transcription.

### 8. Congratulations to the American Hierarchy — PASS

- **warning**, page(s) 1: Recognizable retained transcription defects include “CathOUcity”, “ApostoHc”, and the duplicated phrase “the but, on the but”. These require no inferred correction in this visual review; they remain a source-quality limitation. The surrounding prose and two-column reading order remain usable.
- **info**, page(s) 2: Sparse final page retains the historical closing two paragraphs through “an augury of divine gifts.” The identified chapter source ends there; no added papal subscription is expected or invented.

Source limitation: Historical English web transcription of the 1903 Benziger edition; individual translator unidentified. Residual OCR errors remain; full image collation is outstanding.

## Acceptance limits

This review accepts the eight readers as visually usable source reading editions of their pinned, expressly uncollated witnesses. It does not certify source accuracy, translation accuracy, complete recovery of the historical printing, or distribution rights. The French reader retains one bounded punctuation intrusion, malformed note readings and markers; its notes remain separate source blocks and its prose is substantially readable. The ASS 20 reader has a short garbled protocol label and scattered damaged words, while its body remains substantially usable. These exact defects warrant explicit source-quality qualifications, but do not establish sustained unreadability, body/note paragraph fusion, lost text or a geometry failure. No lexical correction or new note anchor is inferred by this acceptance.

No source ending loss, blank page, clipping, overlap, column-order reversal, sustained unreadable passage, unreadable project colophon, or project-only terminal page was identified. Sparse final pages are qualified individually above because they retain historical prose, notes, dating clauses or subscriptions.
