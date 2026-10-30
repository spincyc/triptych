# Fresh cold PDF review — baseline recovery 10

Completed packet: 3/3 documents; 12/12 pages. Each reported page was viewed freshly in its existing contact sheet and full-resolution page raster. No prior checkpoint inspection is inherited.

Canonical destination: `src/sources/papal-documents/encyclicals-baseline-recovery-10.md`.
Render revision: `2026-10-30T02:56:48Z`. Receipt SHA-256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

| Document | Language | Pages | Actual pages / full-size views | Status | PDF SHA-256 |
| --- | --- | ---: | --- | --- | --- |
| Insignes Deo aeterno (`acta.ass.028.ass-028-l25349`) | la | 4 | 1–4 / 1–4 | PASS | `7b776d26f70e5bee6bc1f959260ac924b05ef487b686dde603273b79df4a8a52` |
| Iampridem (`papal.leo-xiii.hf-l-xiii-enc-06011886-iampridem`) | la | 4 | 1–4 / 1–4 | PASS | `e24c7d6b0d4df6be065e061f4bdbfea882fbd5bd63d927038ca4d31702447a1d` |
| Laetitiae Sanctae (`papal.leo-xiii.hf-l-xiii-enc-08091893-laetitiae-sanctae`) | la | 4 | 1–4 / 1–4 | PASS | `af786c197856e143e9456b6910c159b48916203f298b9245b7b1004165e4aadd` |

For every completed document, programmatic checks verified exact PDF, receipt, frozen manifest, source text, body TeX, sidecar pinset, optional segment manifest, and raster-run hashes; complete frozen-source and receipt rows match the sidecar rows. All source-controller record hashes and identities, declared payload hashes, available payload bytes, raster/thumbnail/contact-sheet bytes and sizes, raster PDF/page pins and renderer fingerprint match. Restricted ancestor payloads are unavailable and were not fetched or claimed verified. Detailed check records are the corresponding `doc-NN-pins.json` files. `pdfinfo` confirms four Letter pages, expected title/author/language, no encryption and no suspect flag; all four embedded Latin Modern font subsets per PDF have Unicode maps. The frozen receipt reports source-aware text-fidelity PASS with no document warnings; this review does not claim a fresh whole-source collation or fidelity replay.

## Insignes Deo aeterno

PASS with retained-OCR qualifications. Normal left-column then right-column reading order, restrained title/identification, justified text, paragraph indents, page numbers, margins and compact terminal apparatus are intact. The final page retains the substantive closing, dating clause and `LEO PP. XIII`; the right column holds source and rights notices. No clipping, overlap, isolated heading, blank or apparatus-only page was found.

The source visibly retains broad OCR letter spacing and source-line hyphen fragments (for example `c u m`, `multi- plicet`, and `p r a e c i p u e -`); these slow reading but remained decipherable on all four full-size pages. This acceptance does not certify those source words.

On page 1 the Clemens XIII note interrupts the body after `pristino fulgens` and before `honore`. Literal source LF 25429 is the note, with body continuation at 25432; body TeX LF 88 is `\par`, LF 90 is the note, LF 91 is `\par`, and LF 93 resumes `honore`. On page 3 the `(1)`–`(4)` note block precedes `suadere`: source LF 25595–25598 and continuation LF 25601; body TeX LF 255 and 261 are explicit `\par` around note LF 257–260, followed by `suadere` at LF 263. Both rendered blocks were inspected at full size and remain legible and separate. The sentence interruption is retained source order, not demonstrated note fusion. Opening source LF 25344 matches the source heading; closing source LF 25661–25665 matches the dating clause and subscription (body TeX LF 323–328).

Actual inspection: contact sheet `contact-sheets/sheet-001.png`; full-size rasters `pages/page-1.png` through `pages/page-4.png` within `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1896-05-01-acta-ass-028-ass-028-l25349-d061eeb5-la/1896-05-01-acta-ass-028-ass-028-l25349-d061eeb5-la`.

Source SHA-256: `9d724e374e7e18e9100778a8714c07cb4f9124039cbd3718543d2d907f25aac4`. Body TeX SHA-256: `304574586b8c327dd0fd4c36b149d384f5b9f95562d45160063e5fc311b0f0ee`. Pin verification: `54` checks passed.

## Iampridem

PASS. Every page was freshly viewed in the contact sheet and at full resolution. The source address/subject heading stays together at the opening; the title, Leo XIII, 1886-01-06 and Latin identification are clear. Justified text reads in normal two-column order with consistent paragraph indents and line spacing. Both densely set middle pages remain legible, including the inline citations on page 2 (Ignatius) and page 3 (Rom. XIII, 5). No footnote block, fused note, clipping, overlap, orphan heading, blank page or apparatus-only page was found.

The final page retains the blessing, `Datum Romae apud S. Petrum, die VI Ian. a. MDCCCLXXXVI. Pontificatus Nostri Octavo.` and `LEO PP. XIII` before the compact source/rights colophon. Source literal LF 1–5 matches the opening heading and incipit; source LF 37–41 matches the blessing, dating and subscription at body TeX LF 63–70. The source transcription retains the visibly anomalous `fbrtunentur` on page 4 (source LF 33 / body TeX LF 57); it is legible and remains an uncollated-source qualification, not a demonstrated layout defect.

Actual inspection: contact sheet `contact-sheets/sheet-001.png`; full-size rasters `pages/page-1.png` through `pages/page-4.png` within `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1886-01-06-papal-leo-xiii-hf-l-xiii-enc-06011886-iampridem-564cc654-la/1886-01-06-papal-leo-xiii-hf-l-xiii-enc-06011886-iampridem-564cc654-la`.

Source SHA-256: `4f3ad592cb17b53b73e0f45fa39f98b01732c13aafd33819db00c35ef973fd9a`. Body TeX SHA-256: `704f00cc0e1aaccbcb350e43a354c2b4a956ad893476551dec07276c8ef85acd`. Pin verification: `50` checks passed.

## Laetitiae Sanctae

PASS with opening-spacing and sparse-ending qualifications. All four pages were freshly inspected in the existing contact sheet and at full resolution. Clear title/Leo XIII/date/Latin identification precedes the retained uppercase source headings, salutation and incipit. Short headings are flush left. The longer 223-character uppercase salutation (source LF 9 / body TeX LF 21–22) is justified and has wide word spacing, especially in its first lines, but remains legible and contained; it is not isolated from its source body. Middle pages keep consistent justified text, normal column order, paragraph indents and readable inline biblical citations. No clipping, overlap, fused historical note, blank page or isolated heading was found.

The final page is sparse, with a blank right column, but its left column includes real continuation beginning `assequi`, the closing blessing, the dating clause for 8 September 1893 and `LEO PP. XIII`, followed by the compact source/rights colophon. This is a source-bearing sparse ending, not an apparatus-only page. Source literal LF 1–11 agrees with the opening source structure and incipit (body TeX LF 9–24); source LF 25–31 agrees with the continuation, closing and subscription (body TeX LF 45–55). No separate historical footnote block appears in this witness.

Actual inspection: contact sheet `contact-sheets/sheet-001.png`; full-size rasters `pages/page-1.png` through `pages/page-4.png` within `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1893-09-08-papal-leo-xiii-hf-l-xiii-enc-08091893-laetitiae-sanctae-5fde687d-la/1893-09-08-papal-leo-xiii-hf-l-xiii-enc-08091893-laetitiae-sanctae-5fde687d-la`.

Source SHA-256: `938e0d2ba7ea4c7062f2a140b0a9a59f08a6dbd74fb6d0888d4e3429bf12a32c`. Body TeX SHA-256: `2961061e87b752ce6f3668364213610862cf52b6ea4b11c0be5a2425e90ef002`. Pin verification: `50` checks passed.

## Limits

This is layout acceptance of the exact frozen bytes above, including stated qualifications. It does not certify Latin wording, translation accuracy, rights, historical completeness, image collation, or source admission. Literal LF counting is used for source loci; form feed adds no LF. No rasters, PDFs, sources, canonical reports, release records, shared caches or Git state were changed. No pages were reused; each row has `reused_pages: []` and `reuse_proofs: []`.
