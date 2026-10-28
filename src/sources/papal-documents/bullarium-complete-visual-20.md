# Complete Bullarium visual review — batch 20

Reviewed 2026-10-26 against frozen receipt SHA-256
`7b987ba5c631098869c8d1e6cfac14fb9bff2498e81b906c8100432e17f4f5c6`.

All **30 assigned PDFs / 69 individual pages** were opened with `view_image`
at readable full-page resolution using the existing `tools/pdf-review` rasters.
No contact-sheet-only coverage is claimed. Current PDF SHA-256 values were
measured before and after inspection; all 30 matched both times and matched
the assigned hashes below. No PDF, retained source or generated body was edited,
and no raster run was started by this review.

**Disposition: pass-layout-qualified for every assigned document.** No physical
clipping, overlapping text, title/body collision, introduced missing glyph or
apparatus-only terminal spill was observed. Column continuations and terminal
source/rights apparatus remain visually distinguishable and within the page
margins. Unbalanced final columns and sparse endings are retained composition
limitations. In particular, volume 12 unit 0057 p. 3, volume 14 unit 0140 p. 2,
and volume 21 unit 0179 p. 5 retain dating/closing text before their apparatus;
none was accepted merely on the presence of a running head or page debris.

Source OCR is visibly damaged throughout this batch: malformed words in titles
and issuers, punctuation clusters, running-head/page-label debris and stray
short lines remain. For every document whose inspected pages show black
squares, literal U+25A0 occurrences were confirmed in the generated body TeX;
these are qualified source-text findings, not evidence of a newly missing font
glyph. This does not establish the underlying historical printing's glyphs.

Volume 10 unit 0108 pp. 2–4 includes extended Italian clauses under the compact
**Latin** label. Its language description therefore needs this explicit
qualification; the present review does not alter that label or source wording.
Volume 24 unit 0112 p. 4 also preserves inconsistent visible dating strings
(1739 and 1738), without an inferred correction.

The existing mechanical text-fidelity passes are assignment evidence, not a new
comparison performed here. This is visual layout acceptance of the listed
bytes only: it is not historical image collation, authentication, a completeness
claim beyond the selected bounds, rights reassessment, installation or
publication approval. Retained OCR and language qualifications remain open for
any later textual or metadata review.

## Exact coverage and findings

The page numbers below are physical reading-PDF pages. Every page in every
listed range was individually opened and inspected. Hashes are full SHA-256.

| Document ID | Reviewed PDF SHA-256 (before = after = assigned) | Pages inspected | Disposition | Concrete observations |
| --- | --- | --- | --- | --- |
| `bullarium.volume-02.unit-0071.part-02` | `d6c7027f99ab16213ef5515c244303ce17a89ef4bd293d194fc58581b6698a5d` | 1 | `pass-layout-qualified` | p. 1: damaged OCR is visible in the title/issuer and in short running-head/date fragments; a black square appears in the synopsis. Layout and terminal source/rights remain clear. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-02.unit-0237` | `b6bef8b5f468c1082b08ac174fa2ee28f65211abbac8af7c9adef014c34d81ef` | 1–2 | `pass-layout-qualified` | pp. 1–2: substantial retained OCR debris includes punctuation clusters and running-head fragments; p. 2 keeps signatures, dating and terminal apparatus without clipping. |
| `bullarium.volume-03.unit-0101` | `c35eaecb297def6a19039b365f80d015e27d2790763aef215e3869e6a35381b4` | 1 | `pass-layout-qualified` | p. 1: title spacing and terminal running-head/date strings remain OCR-damaged; the short body and source/rights apparatus fit cleanly in the left column. |
| `bullarium.volume-05.unit-0043.part-01` | `561d9915e4e3f083f002b9152b2f72a13ed1e938db368b729947a4a7f70ba0ad` | 1 | `pass-layout-qualified` | p. 1: retained OCR debris includes issuer spelling, punctuation clusters and a black square in the left column; two-column body and terminal apparatus remain within margins. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-05.unit-0043.part-02` | `18749b009f540a87b28474a3a9a665078f65c96f7aeef95aeec81d9f274413d6` | 1–2 | `pass-layout-qualified` | p. 1: OCR punctuation clusters and a black square remain in the body; p. 2 contains source clauses, dating and readable source/rights apparatus with ample white space. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-08.unit-0003` | `fe167b52b1906523186b6e8f74f9db546bd45279f3c17f1c1017420d8145ac2e` | 1–3 | `pass-layout-qualified` | pp. 1–3: damaged title words, punctuation clusters and running-head fragments remain literal OCR; source and rights apparatus finish on p. 3 without a separate page. |
| `bullarium.volume-08.unit-0092` | `bacb771668154bb4cab18cb473d260436364912e5e37ca53e030dbe70d3d542a` | 1–2 | `pass-layout-qualified` | p. 1: long OCR-damaged title wraps in three lines without clipping; p. 2 opens with punctuation debris and a black square, then dating and terminal apparatus. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-10.unit-0051.part-01` | `12ed6c20a2a3ebedc7251621298d5ee5fe15f149a7b9315caa29b778fd6a2868` | 1–2 | `pass-layout-qualified` | p. 1: five-line OCR-damaged title and a body square fit within margins; p. 2 has a heavily garbled passage in the left column, with clear dating/source/rights on the right. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-10.unit-0108` | `6a0e31508c569894170bb2f41c696b021e1ab7ed00607f201f92eefcf37f4b2f` | 1–8 | `pass-layout-qualified` | pp. 1–8: dense clauses and subscriptions remain separated in two columns; black squares are visible on pp. 3–4 and 7–8 amid OCR debris. The retained Italian clauses on pp. 2–4 occur inside the witness labeled Latin; this review does not normalize or authenticate that language metadata. Sparse final subscription marks precede the apparatus on p. 8, without an apparatus-only page. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-11.unit-0104` | `4655b0361444ed6f68da3e2b2515cf727d7d35d8e8a132dde9c55f4b4227d14c` | 1 | `pass-layout-qualified` | p. 1: three-line title, body and terminal source/rights remain distinct; OCR punctuation clusters and running-head/date fragments interrupt the source wording. |
| `bullarium.volume-12.unit-0057` | `a45166b7ee36469add153ac68301fa84b09e28488ce5e7143ad25186fe16ab5c` | 1–3 | `pass-layout-qualified` | pp. 1–2: retained title/issuer and running-head strings are OCR-damaged; p. 3 contains only the source dating/closing strings before source/rights apparatus, so it is sparse but not apparatus-only. |
| `bullarium.volume-12.unit-0184` | `dd29b89af90463fabb3948a421a914627ae7845ff6caf8a1e6411c42e9020e5f` | 1–2 | `pass-layout-qualified` | pp. 1–2: literal-looking black squares occur in source notes/body amid OCR damage; body, closing and source/rights apparatus remain unclipped. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-13.unit-0116` | `5ba7b94811c00918b8d7cea346935dce6440e5c48fa34c65a0c2a4dfdeab855c` | 1–4 | `pass-layout-qualified` | pp. 1–3: OCR-damaged issuer/title and running-head/date strings remain; p. 3 has a black square amid dots in the right column. p. 4 retains closing clauses and dating ahead of clear apparatus. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-13.unit-0208` | `c9d480fb4b4e26d38d7bda8c299b20ecb4714cb81f31f1d2d7c616f8680a785b` | 1 | `pass-layout-qualified` | p. 1: damaged title/issuer strings, running heads and clause fragments remain literal; source/rights apparatus fits below the closing in the right column. |
| `bullarium.volume-13.unit-0212` | `ab88ea3b042b971598611b6d8650566c308c6802cfbc5d39c64d501345789b87` | 1–2 | `pass-layout-qualified` | p. 1: title wraps in four lines without collision; running-head fragments and a body square remain OCR-qualified. p. 2 finishes body and dating before clear source/rights apparatus. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-14.unit-0140` | `d3e29aa71819fa7c994efcb883e4131f1f9b4b9f5bf65809dc5c0432375c2fba` | 1–2 | `pass-layout-qualified` | p. 1: black-square clusters and OCR-damaged title/issuer remain visible; p. 2 holds the short retained source dating line and running-head fragment before apparatus, so its sparse ending is not apparatus-only. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-15.unit-0102` | `a183dfc0a88561c5a963b02041caf83f5f701208a871b5053677a3e3f58bd408` | 1–2 | `pass-layout-qualified` | p. 1: a square, dots, short clause fragments and running heads remain OCR-qualified; p. 2 retains a substantive final clause and dating before clear source/rights apparatus. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-15.unit-0144.part-01` | `c6a81a054d875edfbaa838001f7846766999167b655b8eb41380797bce6b918b` | 1 | `pass-layout-qualified` | p. 1: title and running-head/edition debris are OCR-damaged; the body and terminal source/rights apparatus remain clearly separated. |
| `bullarium.volume-16.unit-0032` | `a7bd027eeaf6e6e9739d3de6c8ea8ecdfdd55a7dcf71e620c211f9332cc17dd5` | 1–2 | `pass-layout-qualified` | pp. 1–2: title/word substitutions, running-head/date fragments and short stray strings remain OCR-qualified; body, dating and compact terminal apparatus fit within the two-column layout. |
| `bullarium.volume-16.unit-0248` | `22d43cdcabc8ab0952551e8bb1dbe5e2395d78a66c12779c1555e33b9db68475` | 1–3 | `pass-layout-qualified` | pp. 1–3: retained title, short clause/heading fragments and running heads show OCR damage; dense clauses, historical notes and terminal source/rights apparatus have clear margins. |
| `bullarium.volume-17.unit-0047` | `0ce8af0f7c00785f5489369527cef5d1ca030316fbefeb028a38cf18e3973a3b` | 1–2 | `pass-layout-qualified` | pp. 1–2: numbered source clauses remain readable in normal two-column succession despite OCR substitutions and running-head fragments; closing/dating and apparatus fit on p. 2. |
| `bullarium.volume-17.unit-0120` | `b0ff2bcd4c81c88dcfc6334da8eb4097ba517a31049d3a064215cf9d0b0d426e` | 1 | `pass-layout-qualified` | p. 1: three-line OCR-damaged title and short running-head/stray strings remain; final dating and source/rights fit below the right-column source text. |
| `bullarium.volume-18.unit-0102` | `ddc5858cd3efca9e96a011fcaf69ee9ca47cc3ecaf958b3dfa8899e81af7d993` | 1–2 | `pass-layout-qualified` | p. 1: five-line OCR-damaged title remains fully on-page with body separation; p. 2 includes closing, subscription and register note before clear terminal apparatus. |
| `bullarium.volume-20.unit-0112` | `d087369c02e6e2d55e0abb48e09e46e334abbdb6d74aea7e0d39df82b5627762` | 1–2 | `pass-layout-qualified` | p. 1: retained OCR square cluster appears near the opening and running-head fragments interrupt body; p. 2 contains a final source clause and dating before the compact apparatus. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-21.unit-0109` | `882a8a49d6237283ed2c5b13d4a9d7da0e955143451a4f2b25db904b54a2bb89` | 1 | `pass-layout-qualified` | p. 1: the three-line title is intact geometrically; source OCR includes a body square and running-head fragments. The apparatus continues from left column to right on the same page without clipping. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-21.unit-0179` | `8241317fe688f540bc3ffa6113a2502cbb43ad6cebf0bd0a3c7122ecc75fbb7f` | 1–5 | `pass-layout-qualified` | pp. 1–4: long title includes a literal backslash on its own line; OCR substitutions, running heads and a square on p. 4 remain visible. p. 5 contains the retained dating clause before source/rights, so the sparse ending is source-bearing. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-21.unit-0190` | `d2d816e4b099d5e6debb7875f9b1a1265026860892b2ee51dee66996f53b1dd8` | 1–2 | `pass-layout-qualified` | pp. 1–2: five-line OCR-damaged title, historical notes and running-head/date fragments remain; two-column body and final dating/source/rights are geometrically clear. |
| `bullarium.volume-22.unit-0109` | `0a3ba70a838abda28bb419dd78b30fb1c031066b70449ecf66988058c99b323b` | 1–3 | `pass-layout-qualified` | pp. 1–2: literal backslash in title, body squares/dots and running-head fragments remain OCR-qualified; p. 3 ends substantive clauses and dating before source/rights apparatus. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-22.unit-0231` | `b84703e0933fc819c98ceed74051333e00850b7e0d08e26ad73838d1cac57d10` | 1–2 | `pass-layout-qualified` | p. 1: a body square, damaged words and running-head fragments remain; p. 2 keeps final clauses, dating and historical notes ahead of unclipped apparatus. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |
| `bullarium.volume-24.unit-0112` | `d2168354ee98389b77b7767159c21f68cf19c255bfbb8ec71ed73672ca5254a6` | 1–4 | `pass-layout-qualified` | pp. 1–3: five-line OCR-damaged title and body punctuation/squares remain literal; p. 4 contains substantive final clauses and dating before clear source/rights apparatus. The visible dating strings are inconsistent (1739 and 1738); no historical correction is inferred. Literal U+25A0 black square(s) confirmed in generated body TeX; not classified as introduced missing glyphs. |

The normalized page-path ledger and before/after measurements are retained in
`.scratch/bullarium_visual_review/complete/batch-20/review/result.json`.
The durable identity and coverage record is the table above; scratch evidence
may be removed by workspace tidying.
