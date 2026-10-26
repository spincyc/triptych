# Judgment artifact review — 2026-10-25

**Verdict: ACCEPT.** The final GPT `articles/faith/four-last-things-02-judgment` PDF and generated web edition pass artifact review. No material visual, conversion, metadata, or navigation defect remains. This review covers the exact candidate bytes below; source-content acceptance is recorded separately in `judgment-cold.md`. Installation and publication remain the coordinator's work.

| Accepted item | SHA-256 |
| --- | --- |
| `src/gpt/articles/faith/four-last-things-02-judgment/main.tex` | `94b02eb66c3fdbaf226a606b83ab7482f8ba18849f87e881357896d1e5f5dd6e` |
| `build/gpt/articles/faith/four-last-things-02-judgment.pdf` | `6b8269712df1a6a9740253294adb79afe33bcd654adf9d096194e07330e6a357` |
| `.scratch/flt-judgment-artifacts/final/web/gpt/articles/faith/four-last-things-02-judgment.md` | `5a4ca1467e16d8609bc79e775396bb959086940c4969a999c27e49ac0af1c73e` |
| `.scratch/flt-judgment-artifacts/final/site/web/gpt/articles/faith/four-last-things-02-judgment.html` | `0d89311c2c891d0a633b9ce9e17f821b9a5babe8c87a136fb4cb4d96eee0f936` |

The tracked and displayed revision is `2026-10-25T20:37:59Z`. The PDF has 24 US Letter pages and is 359,594 bytes, approximately 14.63 KiB per page. Neither repository size-review trigger is reached. The approximately 25-page extent is naturally typeset; this artifact review does not substitute pagination for the separate content judgment.

**PDF evidence.** Rasters were generated exclusively with `tools/pdf-review`, using dedicated replaceable destinations and a lane-owned cache. All 24 original candidate page rasters were individually opened and visually inspected at reading scale, in addition to both contact sheets. The final source removed one repeated sentence and refreshed the revision. A separate final raster run established that pages 2–20 are byte-identical to those already inspected; final pages 1 and 21–24 were individually reopened. Thus every final page is covered by inspected raster bytes, with all changed pages freshly inspected. The two iterations remain separately retained under `.scratch/flt-judgment-artifacts/rasters/` and `.scratch/flt-judgment-artifacts/final/rasters/`; `final/raster-comparison.json` records the comparison.

Page 1 has a legible title, series navigation, and settled contents. Pages 2–20 preserve consistent prose density and margins. The headings beginning low on pages 11 and 14 have following prose and are not stranded. Final page 21's new section heading has three following lines; page 22's final substantive heading likewise has following prose. Pages 23–24 retain the scope appendix and all references. Page 24 places the revision and readable rights colophon after references on the same physical page, without overlap, clipping, or a rights-only spill page. No clipped line, broken glyph, excessive gap, dense apparatus collision, or sparse spill page was found.

The settled log has no fatal error, undefined reference, overfull box, or rerun request. Its one `Underfull \hbox (badness 10000)` at log line 1041 reports an empty box after the metadata import. Inspection of the final page resolves that warning as visually harmless. All eleven Type 1 font subsets are embedded, subsetted, and Unicode mapped. PDF title and subject identify this work; modification time agrees with the tracked UTC revision. The metadata gate confirms no reader-visible internal model/provenance data or automatic PDF date/trailer-ID defect. The PDF is unencrypted and has no JavaScript; it is untagged, with the reflowed HTML supplying the accessible reading alternative.

The anchor gate passes all 16 contents entries and 16 bookmarks on their own heading anchors. Final named destinations and visible contents agree, including sections 13 and 14 now beginning on pages 21 and 22. Decoding PDF object streams confirms four relative `GoToR` annotations to the correct Death, Judgment, Hell, and Heaven PDF filenames. The external CDF, *Spe salvi*, and CC BY links are retained. This lane did not modify installed PDF mirrors or claim that installation had already occurred.

**Web fidelity and browser evidence.** `tools/web-edition --provider gpt --output .scratch/flt-judgment-artifacts/final/web articles/faith/four-last-things-02-judgment` generated the accepted Markdown using Python 3.14.8, Pandoc, and the required Markdown 3.10.3 environment, with that environment's `bin` prepended to `PATH`. Conversion and its internal audits succeeded. The declaration remains eligible and opts into contents.

The current `tools/public-alpha` `rewrite_links` and `render_page` functions rendered the generated Markdown with the actual current layout, CSS, locked Markdown extensions, and perpetual public authorization settings. No stylesheet or simplified rendering substitute was introduced. Unchanged assets and companion pages were borrowed read-only from `build/public-alpha/site`; its CSS hash equals the current source CSS hash below. Only the target HTML was newly rendered. No whole-site build or shared release/data mutation was performed.

All 179 rendered content blocks other than the expanded subtitle match normalized extracted PDF text. The expanded subtitle reproduces the PDF's subject metadata; the print title page uses the shorter `Judgment`. A reverse coverage check leaves only the short print subtitle, `Contents`, section/appendix numbers, and contents page numbers unmatched. The 14 substantive sections, two terminal sections, 11 reference entries, inline citations and qualifications, revision, rights notice, and series navigation survive. There are no figures, tables, footnotes, or block quotations requiring a separate conversion treatment. The final cut is reflected in both artifacts.

Chromium **156.0.8078.47**, driven by ChromeDriver over a scratch-only local HTTP server, inspected the accepted HTML at these actual CSS viewports:

| Viewport | Document scroll width | Overflowing elements | Contents links clicked |
| --- | ---: | ---: | ---: |
| 1440 × 900 | 1425 px | 0 | 16 |
| 393 × 852 | 378 px | 0 | 16 |
| 320 × 800 | 305 px | 0 | 16 |

The 15 px difference is the vertical scrollbar. All 48 contents clicks reached the correct fragment and placed its heading at the top of the viewport. There are no duplicate IDs, missing fragment targets, browser console errors, or missing local links. Clicks to Death, Hell, and Heaven loaded the expected companion titles. All 12 non-fragment local links, including the current article and site chrome, resolve against the baseline-backed scratch tree. Companion content acceptance belongs to its respective review.

All 18 screenshots were opened and inspected: `top`, `body`, `middle`, `scope`, `references`, and `end` at each of the three viewports. Title, long headings, references, inline citation ranges, revision wrapping, colophon, and site footer remain legible. Body type is 16.64 px at every tested width; narrow layouts require no sideways panning. Screenshots and DOM/navigation evidence are retained under `final/screenshots/` and `final/browser-report.json`. Browser session deletion and local server/driver cleanup completed.

**Reproducibility records.** Full applicable editorial, repository, articles, and web-editions guidance and the tool registry were read before review scripts were written. These render-relevant inputs were hashed from the reviewed tree:

| Input | SHA-256 |
| --- | --- |
| Judgment `generation-metadata.tex` | `4f87b040c1a781ae4583a7043741b0a2091b7eddd57646efca5bc7542fcfe0ff` |
| Judgment `references.tex` | `b6b02fa8aa7bff83c1a472f4c8c17ba00193231c12e9acd8d28d1f3558f4021a` |
| Judgment `web-edition.toml` | `aab32c749cba0a88a6f8c0c39bc2d8ec4863ff6f57fb22764ad22cff72320d67` |
| `src/gpt/articles/faith/four-last-things-shared/format.tex` | `98eea2ad1b83ae442f74c8688ae4695f8bf5aef17b63d8ebdafdffee70c9136d` |
| `src/common/preamble.tex` | `4471c68736e6d1bfd95032159e1aabd75f7d925b51a3b3dbfdb6e915eb79179b` |
| `tools/web-edition` | `10c10959da1485d0d95773234f2d615ee21c3139896b430ebea7614f5ca52d57` |
| `scripts/web-shim.tex` | `33abd8946680492c3d45785bbf7c39afea1c047d62bed8b57fd0b0e13a56545e` |
| `tools/public-alpha` | `e8d28ee9ddf942225010a249574b67cbe38fb9dfee37e223df102aa7155a6331` |
| `scripts/_markdown_render.py` | `be0ffcd9d3d0b789f633be2938c07c9076d44d72eb3b6c5eb65b93307e6fa648` |
| `release/public-alpha/layout.html` | `6687546feca2e378e57917fa44ed908c5abfa49f4499731c95316f1d34b3d9eb` |
| `release/public-alpha/assets/site.css` | `004f8a18f127c2fbced58190c458b7b2819f12da065431c13fd69abf927dcb47` |
| `requirements-public-alpha.txt` | `59bd4c5252324612c6ce5a27f4a4ba4e62aa4cc76bc3d974a29b45491c97c762` |

The installed Markdown 3.10.3 package's `__init__.py` hashes to `75fcf0c1da46f4bf102c43c1a4b14f207c7f04dd39e9a657a7dc5989f4f16085`. `final/hashes.json` and `final/runtime.json` retain the complete manifest and runtime observations. `final/checks.json` records numeric exit status **0** for final metadata, PDF-anchor, web-eligibility, PDF-info, font, destination, URL, and Pandoc-version checks, with individual logs. PDF rasterizer versions and fingerprint are in `final/rasters/review-run.json`; conversion output, text comparisons, decoded companion links, and warning disposition are also retained in this lane's scratch evidence. No source, installed publication, shared release record, or shared web data was edited by this lane; only this durable report was added.
