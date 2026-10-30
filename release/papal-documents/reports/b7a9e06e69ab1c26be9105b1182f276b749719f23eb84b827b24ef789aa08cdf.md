# Spiritus Paraclitus: fresh cold visual review

Final status: **PASS**, with retained-transcription qualifications below. This review covers only packet `baseline-recovery-02`: `papal.benedict-xv.hf-ben-xv-enc-15091920-spiritus-paraclitus`, Latin, Benedict XV, 1920-09-15. It accepts the inspected layout of these exact bytes; it does not certify the historical wording or rights assessment.

## Exact artifact and coverage

- PDF: `.scratch/encyclical-classic/readers-fixed/1920-09-15-papal-benedict-xv-hf-ben-xv-enc-15091920-spiritus-paraclitus-0900f2cb-la/1920-09-15-papal-benedict-xv-hf-ben-xv-enc-15091920-spiritus-paraclitus-0900f2cb-la.pdf`
- PDF SHA-256: `c70d985478baef912ab6e3e93c3febd0ed270b822b91ee9f060944ece62409ca`
- Actual PDF extent: **15 pages**, independently checked with `pdfinfo`.
- Fresh contact-sheet inspection: **pages 1–15**, individually examined in existing `contact-sheets/sheet-001.png`.
- Additional full-size raster views: **pages 1, 6, 13, 14, 15**. These cover identification/opening, dense body composition, the transcription anomalies near the ending, subscription, historical reference notes, and terminal apparatus.
- Reused pages: **none**. Reuse proofs: **none**. No inspection or acceptance was inherited from old checkpoints.
- Raster directory: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1920-09-15-papal-benedict-xv-hf-ben-xv-enc-15091920-spiritus-paraclitus-0900f2cb-la/1920-09-15-papal-benedict-xv-hf-ben-xv-enc-15091920-spiritus-paraclitus-0900f2cb-la`. All 31 files named in its cache record, including the contact sheet and 15 full-size pages, were checked against their recorded hashes and sizes. This is byte verification, separate from the fresh visual inspection above.

## Findings and qualifications

The two-column text runs in normal reading order. The title, responsible pope, act date and language are clear. Body columns have consistent gutters, indents, leading and justified composition. The inspected pages show no clipping, overlap, displaced heading, material orphan/widow defect, fused note/body paragraph, or materially unreadable rendered passage. Dense pages 2–13 remain visually contained in the contact sheet; page 6 was additionally checked full size.

Page 1 retains the protocol and salutation. Its left-column ending “in hac” continues at the top of the right column with “alma Urbe”; the transition is readable. The long all-capital address has wider justification in places. The receipt records two underfull-hbox warnings at generated TeX lines 18–19. The corresponding rendered identification/address remains contained and legible; these warnings do not establish a blocking defect in the viewed output.

Page 13 contains literal transcription anomalies, including `spiritúzn` and `gloliabatwr`, that also occur in the pinned source at physical LF lines 45 and 49 and body TeX lines 75 and 81. Page 1's `PATHIAHCHAS` likewise occurs at source LF line 7. These isolated corruptions are a substantive limitation of the disclosed uncollated transcription. They are visibly readable as retained text and do not amount to a materially unreadable passage in this layout review. No corrections or historical verbal collation were attempted. The paragraph break after “et Romani cives” on page 13 is present in the source LF 47/49 and body TeX LF 78/81; it is not note fusion.

Page 14 retains the final body, dating clause and `BENEDICTUS PP. XV` subscription, followed by historical references (1)–(75). Page 15 retains references (76)–(144): (76)–(127) occupy the left column, then (128)–(144) the right. Its remaining right-column space contains a compact, clearly separated source/rights colophon after a short rule. This final page is source-bearing, not a page solely of project apparatus. Wrapped reference lines remain legible and contained. Literal reference (128) wording `Postumiauus npud Sulp. Sov.` is retained from source LF 311/body TeX LF 474 and is not a layout-induced fusion.

The note boundary check used literal LF counting only: the source contains 343 LF characters and no form feeds. All 144 numbered reference paragraphs have one matching source line and one matching body TeX line. Each has an explicit preceding and following TeX paragraph boundary. In particular, source subscription LF 55 maps to body TeX LF 90–91 ending `\par}`; note (1) begins at source LF 57/body TeX LF 93 and ends with `\par` at body TeX LF 94. The last note (144) is source LF 343/body TeX LF 522, followed by `\par` at line 523. The rendered views of pages 14–15 agree with these separate blocks. There is no note-interruption or fusion finding here.

## Verification evidence

`pin-verification.json` records **842 passing checks**. These verify the exact PDF, receipt, frozen manifest, source text, body TeX, hashed source-pinset sidecar, original packet, controller records, raster run manifest, and cached raster file pins. The sidecar source row exactly equals the frozen row; its receipt row exactly equals the current matching receipt row. Both source controller record hashes match. The normalized transcription payload hash was checked; the restricted parent HTML has no retained payload path in the sidecar, so only its controller metadata was checked.

- Receipt SHA-256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`
- Frozen manifest SHA-256: `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`
- Source text SHA-256: `49ebcf2e9126ac556c4d5d7a0a5fd13518584f774e174fc2226f36287e50fd9e`
- Body TeX SHA-256: `a3e3d1009b53381609da5c0b9eebc39753b03733c38450e2214f9336fdc8dd32`
- Source-pinset SHA-256: `0f4cb7502b6b539ddd4fd80ba96be87bed1f091a7bb8463c56682dc2a24614ff`
- Raster run manifest SHA-256: `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02`
- Render revision: `2026-10-30T02:56:48Z`

Fresh `pdfinfo`, `pdffonts`, and raw `pdftotext` checks completed successfully. The PDF is an unencrypted 15-page letter-size PDF with the expected title and author; all four listed Latin Modern fonts are embedded. The repository's existing `pdf_body_fidelity` function was rerun read-only with the pinned source. It passed using `pdf-raw-source-aware-line-hyphen-nfkc-v3`, accounting for 341 layout hyphens and matching source extent from page 1 through page 15. Its result matches the receipt. Mechanical fidelity does not certify the correctness of source words.

## Limits and ownership

This is a cold visual acceptance of one exact PDF, with the page coverage stated above. The supplied source note identifies an **uncollated normalized web transcription** of Acta Apostolicae Sedis 12 (1920), pp. 385–422. No whole-source verbal/image collation, translation assessment, rights reassessment, compilation, rerendering, rerasterization, installation, installed-mirror comparison or Git operation was performed. `qpdf` was unavailable, so no qpdf structural check was run; `pdfinfo`, font inspection and extraction succeeded. Source/PDF mechanical text fidelity and visible layout acceptance remain separate from historical accuracy and distribution authority.

All created evidence is confined to `.scratch/encyclical-baseline-recovery-02/`. Existing PDFs, sources, controller records, manifests, shared rasters and caches were read only. The final report is intended to be copied byte-for-byte to `src/sources/papal-documents/encyclicals-baseline-recovery-02.md`.
