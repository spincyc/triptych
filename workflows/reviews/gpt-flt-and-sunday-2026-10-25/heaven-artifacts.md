# Heaven artifact review — 2026-10-25

**Disposition: ACCEPT.** The final GPT Heaven build and generated web edition pass this independent mechanical, visual, navigation, and conversion-fidelity review. No artifact correction is required. Content and theological acceptance are recorded separately in `heaven-cold.md`.

This receipt supersedes the artifact inspection of the earlier `20:28:00Z` candidate. The accepted render source was finalized at **2026-10-25T20:38:01Z**. The reviewer regenerated and inspected the final PDF rasters and web rendering after the three bounded source corrections. Sources and installed publications remained read-only; installation, whole-site verification, and publication belong to the coordinator.

## Exact accepted identities

| Artifact | SHA-256 |
| --- | --- |
| `src/gpt/articles/faith/four-last-things-04-heaven/main.tex` | `11c1fddde04e322df45be718b1611b025628a5b580292a740302e7965a197b02` |
| `generation-metadata.tex` in that leaf | `65054695ad46a0234d3460c3c37ac1b0b77c0f8a37bc6935fd2dbb748a63f8c7` |
| `references.tex` in that leaf | `993c9b1a2c05e9897829d129a78e19ab17225226af7a3a81fa2ee92968a6a0ad` |
| `build/gpt/articles/faith/four-last-things-04-heaven.pdf` | `5b4e4a79034c1ff022f4b9a96b23f26e9740bfc94428ef870154ec03eb8028de` |
| Generated Markdown at `.scratch/flt-heaven-artifacts/final/web/gpt/articles/faith/four-last-things-04-heaven.md` | `dec881d9a77a2382722a837de3394fc61b0e261f7eb24148240b98e6a907006e` |
| Rendered HTML at `.scratch/flt-heaven-artifacts/final/preview/web/gpt/articles/faith/four-last-things-04-heaven.html` | `07393a149ffd54800bf66f9187161544243cf5a766f5aa167431b67a8d9defe2` |

## PDF findings

All **23 final pages** were opened individually from the `tools/pdf-review` output; the final page was additionally opened at original raster resolution. Page 1 has the title, series navigation, and all 18 contents entries. Pages 2–21 sustain the essay; page 22 concludes its argument before the scope appendix and references. Section headings remain attached to following prose. No clipping, overlapping text, missing glyph, stranded heading, artificial blank page, or unreadable density was found.

Page 23 contains four substantive reference entries, the single correct revision timestamp, and a compact, readable rights colophon. Its rule and text do not overlap or clip. The colophon has not created a rights-only spill page. The remaining white area is ordinary terminal-page space.

The settled log contains no fatal error, undefined reference, overfull box, or other warning beyond one `Underfull \hbox (badness 10000)` at terminal lines 3–306. The log shows an empty box (`[]`) immediately after the generation-metadata input. The final-page inspection disposes of this warning: neither the timestamp nor the colophon has stretched, broken, or missing text.

`pdfinfo` reports Letter pages, PDF 1.7, no encryption, forms, or JavaScript, and the intended title and subject. The generation gate accepts the source and PDF, including their matching revision date and absence of reader-visible production metadata. All 11 font entries are embedded, subsetted, and have Unicode mappings. Extracted text is legible and complete. `check-pdf-anchors` accepts **18 contents entries and 18 bookmarks**; the PDF destination listing agrees with the visually inspected heading pages. PDF link extraction retains the four relative series PDF targets and all nine external reference/license URLs.

The PDF is **352,356 bytes**, **14.96 KiB per page**. Neither the 1 MiB nor the 75 KiB-per-page investigation trigger is reached. There is no publishing artwork requiring a separate raster-size audit.

## Web findings

The edition was regenerated with the pinned Python environment using:

```sh
tools/web-edition --provider gpt --output .scratch/flt-heaven-artifacts/final/web articles/faith/four-last-things-04-heaven
```

The scratch review helper called the current `tools/public-alpha.render_page` at the actual canonical output path with the current layout and stylesheet. It used Python **3.14.8**, Python-Markdown **3.10.3**, Pandoc **3.11**, and the site's exact `tables`, `sane_lists`, `def_list`, `toc`, `footnotes`, `attr_list`, and `fenced_code` extensions. Unchanged baseline site pages supplied destinations for shell and sibling links; this does not constitute review of those siblings' final revisions.

All **142 source prose/reference paragraphs** match both extracted PDF text and rendered web text after normalization of typography, line wrapping, hyphenation, and PDF page folios. All 16 body headings, the scope appendix, 12 reference entries, timestamp, and rights notice survive conversion. The web's full title and descriptive subtitle preserve the publication's identity. No undeclared omission, added substantive prose, raw TeX, or Markdown debris was found.

Chromium **156.0.8078.47** rendered the final HTML at **1440×1000**, **393×852**, and **320×760**. All **27 screenshots** were inspected: page top, title/contents, series navigation, opening body, vision, Beatitudes, justice, references, and terminal colophon at each width. The shell, long title, contents links, body, reference list, and rights notice reflow legibly. At 320 px the timestamp wraps without losing characters.

Each viewport has 18 contents links and no missing fragment, duplicate ID, element overflow, or rendering debris. All **54 contents-link clicks** were exercised and allowed to settle; each intended heading reached within 0.49 px of the viewport top. All four series links resolved at each width. Local link paths exist. The browser console is empty. Document scroll widths are 1425, 393, and 320 px respectively; there is no horizontal overflow.

## Rendering dependencies and evidence

| Dependency | SHA-256 |
| --- | --- |
| `tools/public-alpha` | `e8d28ee9ddf942225010a249574b67cbe38fb9dfee37e223df102aa7155a6331` |
| `scripts/_markdown_render.py` | `be0ffcd9d3d0b789f633be2938c07c9076d44d72eb3b6c5eb65b93307e6fa648` |
| `release/public-alpha/layout.html` | `6687546feca2e378e57917fa44ed908c5abfa49f4499731c95316f1d34b3d9eb` |
| `release/public-alpha/assets/site.css` | `004f8a18f127c2fbced58190c458b7b2819f12da065431c13fd69abf927dcb47` |
| `requirements-public-alpha.txt` | `59bd4c5252324612c6ce5a27f4a4ba4e62aa4cc76bc3d974a29b45491c97c762` |
| `tools/web-edition` | `10c10959da1485d0d95773234f2d615ee21c3139896b430ebea7614f5ca52d57` |
| `scripts/web-shim.tex` | `33abd8946680492c3d45785bbf7c39afea1c047d62bed8b57fd0b0e13a56545e` |

Final evidence is under `.scratch/flt-heaven-artifacts/final/`: `rasters/review-run.json` binds the PDF and raster renderer; `fidelity.json` records paragraph comparisons and dependency hashes; `browser-evidence.json` records viewport, DOM, navigation, and console checks; `screenshots/` contains the inspected images; `final-checks.json` records final identities, local link checks, and screenshot hashes. Earlier iteration evidence remains at the parent scratch directory and does not approve the final bytes.

The focused generation-metadata, PDF-anchor, web-declaration, raster-generation, conversion, rendering, and browser checks all completed with exit status 0. No whole-site build, installation, commit, push, or deployment was performed in this review lane.
