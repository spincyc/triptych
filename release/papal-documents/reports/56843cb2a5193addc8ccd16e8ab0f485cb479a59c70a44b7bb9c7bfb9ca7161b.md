# Gibbons Latin: independent cold acceptance

PASS for **acta.ass.034.ass-034-l025156 / la**, the exact two-page candidate reviewed on 2026-10-30. This is a source-readonly cold review; no prior judgment or page inspection was reused. Intended canonical report destination: `src/sources/papal-documents/encyclicals-spacing06-cold-gibbons.md`; that destination was not written.

| Binding | SHA-256 |
| --- | --- |
| PDF | `e059d908247f567747dc28804c0214cd4feb1ffcea2f7acd9b08595af27ef81b` |
| Source | `752985e59338dc91e6f84b4fb110b07c1cf0a790c140666f58558bc8aaf93e6e` |
| Producer and frozen manifest | `88db699dfd1da70f3d60abef9f3829be4e1b736f1c407b3feb6c8991078b76b4` |
| Receipt | `352c4963fc8ebe0842fa95aa8c7b3aa8e2a553fed8fa1945f473b290cc626964` |
| Native full PDF | `64a68e6efcbf01054672a6bccb274a8ce1dcce4241149ce342d4d478c6786ea8` |
| Recipe | `68be144c4d1fef61bf1b604d801c726fa6ceb2c3bcb356f445974fa3299f3bdc` |

All reader pages 1–2 and native artifact pages 623–625 were individually opened as original PNG rasters with `view_image(detail="original")` and `image(...,"auto")`. Reader images are 1700×2200; native images 1524×2200. No page reuse, contact-sheet substitution, image conversion or OCR proxy. Fresh full-PDF native renders are byte-identical to the inspected excerpt rasters. Exact raster pins, MIME, dimensions and actual observations are retained in `view-evidence.json` and `observations.md`.

| Page | Actual observation |
| --- | --- |
| Reader 1 | Source title, address and In amplissimo opening present; coherent left-to-right columns through Demum,. No clipping, overlap, glyph boxes or note/body fusion. |
| Reader 2 | Continues ne gratae voluntatis; blessing, complete 15 April 1902 dating clause and LEO PP. XIII. precede source/rights apparatus. Genuine source-bearing final page; blank right column is harmless. |
| Native 623 | Letter title, full salutation and opening in one body column; ends ita vobis. No footnote or marginal summary. Reconstructed printed numeral reads 625. |
| Native 624 | Continues populisque vestris and ends testimonium recidit. One body column, no historical note. Running LITTERAE and numeral excluded. |
| Native 625 | His de omnibus, blessing, dating and subscription end this letter. A separate Antistitum letter / Beatissime Pater begins below; it and the journal footer remain excluded. |

The executable prior selection is preserved exactly: parent LF 25151–25190, 25192–25232, 25234–25243. It includes the source title and complete closing. No historical footnote occurs in this selected extent. Neighboring text starts at LF 25247. The predecessor `historical-text.toml` prose inconsistently calls LF 25248 terminal while its actual ranges end at 25243; current executable bounds and this reader correctly exclude the next letter. No source record was changed.

Fresh full-PDF `pdftotext -raw` extraction equals the retained native raw bytes. Independent replay finds 87 unique same-page LF identities, each with literal native WORD/glyph bbox evidence; two widely spaced address baselines require grouping XML fragments with exactly equal yMin/yMax. Only native whitespace is borrowed: all 4,481 non-whitespace characters, LF records, blank records, selection order and glyph order are preserved. There are no retained-source exceptions or native stream-order differences. The current tracked helper is pinned at `7c7393f6b366bc986e7d106d217a769fabba5a48edd645a7bd02b463eb64d82c`, licensed MIT by LICENSE, and was reused without copying.

Producer/frozen complete-row equality, exact receipt binding, narrow schema/controller ownership and payload hashes pass. Independent current `pdf_body_fidelity` passes on both pages with 29 permitted layout hyphens; current generated TeX/body match; build warnings are empty. PDF metadata identifies Leo XIII / Latin, page count is two, and all four Latin Modern fonts are embedded, subset and Unicode-mapped. Detailed commands, diagnostic qualifications and evidence pins: `checks.txt`, `verification.json` (SHA-256 `3cfaaafd2ee99db97e282d6e5a7fca781e17ca1d88579a477168c6a9f04c9963`), and `independent-line-word-map.json`.

Nonblocking qualifications: literal source hard-line hyphens remain frequent within reflowed lines; isolated OCR defects include Xlii, uteris, fiorenti, doubled punctuation and spaced s u m m u m. They do not produce sustained nonsense, fusion or material unreadability in the inspected reader. Native printed numerals are inconsistent across the reconstruction; artifact page numbering controls coverage. This is acceptance of the exact OCR-derived reader and whitespace provenance, with no original-print, full lexical collation, historical authentication, installation or publication claim. Whole-source-graph PASS is coordinator-supplied evidence, not an independently rerun census. No blocking finding remains within this exact candidate scope.
