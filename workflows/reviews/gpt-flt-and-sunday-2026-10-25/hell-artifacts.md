# Hell — independent artifact review, 2026-10-25

**Disposition: ACCEPT** for the final build PDF and generated web candidate identified below. This accepts typesetting, conversion fidelity, navigation and basic visual usability. Independent source/content review is separately owned. Installation and deployment are coordinator work; this lane changed no source, installed publication, release record, shared renderer or data.

## Exact accepted snapshot

- Provider/document: `gpt:articles/faith/four-last-things-03-hell`.
- Final revision: `2026-10-25T20:42:32Z`.
- Source `main.tex`: SHA-256 `f0297747467df2701088eafa241df938176bf168f4f49500273299698a1b041f`.
- Build PDF `build/gpt/articles/faith/four-last-things-03-hell.pdf`: SHA-256 `08ecee9dbefaa7f4a112dda80548d1a476559c24293ae17768872b4f2bb58df3`; **25 pages, 360,273 bytes**.
- Accepted generated Markdown: `.scratch/flt-hell-artifacts/final/web/gpt/articles/faith/four-last-things-03-hell.md`, SHA-256 `671deaa16efe7d82a9c234a06a53465bcfa65fc4272e0f4aedf41971a09baea7`.
- Accepted scratch HTML: `.scratch/flt-hell-artifacts/final/site/web/gpt/articles/faith/four-last-things-03-hell.html`, SHA-256 `8c83dd15dd9ddf54076cd60fa5b0065b036b782b2e4f7b37abd0236dec10d10e`; 95,531 bytes.

The HTML was produced by importing the actual current `tools/public-alpha`, applying its `rewrite_links`, and calling its `render_page` with the canonical source/output identities and current authorization. It uses the actual layout and stylesheet, without a substitute page shell or editorial changes to the generated Markdown. Only this document was generated and rendered. The scratch HTTP server used the existing baseline site for other destinations; that demonstrates link reachability, not currency acceptance for those destinations.

## PDF evidence

`tools/pdf-review` generated all 25 page rasters and both bounded contact sheets in a dedicated replaceable output directory. Every initial full page raster **1–25** was opened and visually inspected, as were both contact sheets. The first reviewed PDF was `3a7bf4a5cd89b91e53203bd82259b3b0518133b4090c0d2972ffd6be6d295624`. After the source correction and timestamp refresh, a distinct final iteration was rasterized. Exact raster comparison found **only pages 8 and 25 changed**; both final pages were reopened at full size. The other 23 final pages are byte-identical to the previously opened pages. `final/page-comparison.json` records every raster identity.

| Pages | Actual visual review |
| --- | --- |
| 1 | Title, four companion links and all sixteen contents entries are clear; no clipped line or unintended page break. |
| 2–7 | Body and first four section headings remain legible and consistently spaced. Paragraph continuations are coherent; no heading is stranded. |
| 8–13 | Eternity, mortal sin, scandal and mercy sections show no overlap, clipped text or sparse body spill. Final page 8 contains the corrected Augustine sentence and maintains the same pagination. |
| 14–20 | Augustine, Ignatius, Aquinas, Francis and Teresa sections retain their quotations, italics and citation text. Headings on pages 14, 17 and 20 have following prose. |
| 21–23 | Closing application and complete received prayer remain readable; attribution follows the quotation on page 23. |
| 24–25 | Terminal scope precedes fifteen reference entries. Page 25 continues three substantive references, then one revision timestamp and a compact readable colophon; it is not a rights-only page. The final colophon has no overlap or clipping. |

The final metadata and anchor commands exited **0**:

```sh
PATH=".scratch/publication-prep/venv/bin:$PATH" tools/check-generation-metadata --provider gpt --pdf articles/faith/four-last-things-03-hell build/gpt/articles/faith/four-last-things-03-hell.pdf
PATH=".scratch/publication-prep/venv/bin:$PATH" tools/check-pdf-anchors --json build/gpt/articles/faith/four-last-things-03-hell
PATH=".scratch/publication-prep/venv/bin:$PATH" tools/check-web-edition --provider gpt --document articles/faith/four-last-things-03-hell
```

`pdfinfo`, `pdffonts`, `pdfinfo -dests`, `pdftotext -layout`, and `pdftohtml -xml -hidden` all exited 0. The PDF is unencrypted Letter, PDF 1.7, with the expected title and subject; its modification date equals the declared final UTC revision. No build-clock creation date is present. All eleven font entries are embedded subsets with Unicode maps. Extraction preserves the body, fifteen references, received prayer, one timestamp and rights notice. The source/rendered metadata gate accepts the deterministic-date and provenance boundary. The PDF is not tagged; this review does not claim PDF accessibility conformance.

All **16 contents entries and 16 bookmarks** pass their own-anchor check. Actual PDF destinations put sections 1–14 on pages **2, 3, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22**, and both appendices on page **24**, matching the printed contents and visible headings. The four companion PDF actions retain their correct sibling filenames and page-1 destinations. Source and web navigation identify the same four essays, using HTML filenames in the web edition.

The final LaTeX log has no fatal error, overfull box, undefined reference or unresolved rerun warning. Its one terminal `Underfull \hbox (badness 10000)` after generation metadata is visually resolved: the actual final timestamp and colophon are clear and unoverlapped. It does not warrant a source/layout change. The PDF is about **14.1 KiB/page** and below **1 MiB**; neither size trigger applies. There is no publication artwork to normalize.

## Source, PDF and web fidelity

Generation used the pinned Python environment and the registered converter, exit **0**:

```sh
PATH=".scratch/publication-prep/venv/bin:$PATH" .scratch/publication-prep/venv/bin/python tools/web-edition --provider gpt --output .scratch/flt-hell-artifacts/final/web articles/faith/four-last-things-03-hell
```

A separate bounded comparison expanded this leaf's references and removed only its known typesetting commands. The complete normalized source body and references equal the generated web text **in order**. All **197** post-title/navigation web blocks (headings, prose, quotation, reference items, timestamp and colophon) match the extracted final PDF. Normalization disregards whitespace, punctuation and typographic Unicode differences; the page review and targeted quotation/citation inspection supply the visual check those normalized comparisons cannot provide. All fourteen body headings and both appendix headings survive. No silent omission, additional argument or changed quotation was found. The final Augustine correction and timestamp occur in source, PDF, Markdown and rendered HTML.

The actual renderer produces sixteen functioning contents links, the complete four-essay navigation, one visible revision timestamp, the received prayer and attribution, the full terminal scope and bibliography, and the rights colophon. There is no exposed TeX, provenance ledger or new editorial wrapper.

## Chromium evidence

Real **Chromium 156.0.8078.47** rendered the final current-template HTML at **1440×900, 393×852 and 320×852**. At each width, screenshots of the top, body, eternity section, received prayer and final apparatus were captured; substantive body, prayer, corrected section and final timestamp/rights views were opened for visual inspection, with top/navigation composition also checked. The terminal apparatus and quotation reflow cleanly. No column, citation or code-form rights pointer extends beyond the document.

| Viewport | Document scroll width | Main landmarks | Contents/targets | Unnamed controls |
| --- | ---: | ---: | ---: | ---: |
| 1440×900 | 1425 px | 1 | 16/16 | 0 |
| 393×852 | 378 px | 1 | 16/16 | 0 |
| 320×852 | 305 px | 1 | 16/16 | 0 |

The browser reserves 15 px for its vertical scrollbar. Every contents link was activated at all three widths; all sixteen updated to the correct fragment, and the heading landed at the viewport top. Keyboard Enter activation also reaches the first section. All twelve local navigation links returned **HTTP 200**, including Death, Judgment, Hell, Heaven and the owning Faith catalogue. Browser exception, failed-request and HTTP-error collections are empty. The page contains no enhancement JavaScript, so its content, contents, companion links and rights remain static.

Additional 320px captures exercised forced colors/reduced motion and 200% root text. Both retain no horizontal overflow; enlarged site chrome becomes tall. These supplementary checks are not a claim of a complete browser/accessibility certification. There was no real-device, assistive-technology or browser-print review, and no remote source-link revalidation in this artifact lane.

The inherited current reader has an in-flow contents box and shelf breadcrumb rather than the future Reader controls; provider-qualified PDF access is supplied by the owning catalogue. As the coordinator confirmed, redesigning that renderer is outside this prose revision. The revision breaks no existing navigation or fidelity contract.

Scratch evidence lives under `.scratch/flt-hell-artifacts/final/`: metadata/anchor/eligibility logs, PDF info/fonts/destinations/extraction, raster comparison, `snapshot-checks.json`, `browser-checks.json`, and screenshots. Prior snapshot evidence is retained separately. No whole-site build or release write was performed.

## Pinned rendering inputs

Toolchain: Python **3.14.8**, Python Markdown **3.10.3**, Pandoc **3.11**, Chromium **156.0.8078.47**, Node **26.12.1**, pdfTeX **1.40.29**, Poppler **26.10.0**. Pandoc executable SHA-256: `17e3f1234c97baf09be4becb17d51b6c8a788d162bd688b321462cdb055a9984`. Chromium executable SHA-256: `7a4de480c3e409b528bd71c58e0c27b6ec5295bdfbc9d1aca1368ccc70d08ee7`.

| Input | SHA-256 |
| --- | --- |
| `tools/public-alpha` | `e8d28ee9ddf942225010a249574b67cbe38fb9dfee37e223df102aa7155a6331` |
| `scripts/_markdown_render.py` | `be0ffcd9d3d0b789f633be2938c07c9076d44d72eb3b6c5eb65b93307e6fa648` |
| `release/public-alpha/layout.html` | `6687546feca2e378e57917fa44ed908c5abfa49f4499731c95316f1d34b3d9eb` |
| `release/public-alpha/assets/site.css` | `004f8a18f127c2fbced58190c458b7b2819f12da065431c13fd69abf927dcb47` |
| `requirements-public-alpha.txt` | `59bd4c5252324612c6ce5a27f4a4ba4e62aa4cc76bc3d974a29b45491c97c762` |
| `tools/web-edition` | `10c10959da1485d0d95773234f2d615ee21c3139896b430ebea7614f5ca52d57` |
| `scripts/web-shim.tex` | `33abd8946680492c3d45785bbf7c39afea1c047d62bed8b57fd0b0e13a56545e` |
| `src/common/preamble.tex` | `4471c68736e6d1bfd95032159e1aabd75f7d925b51a3b3dbfdb6e915eb79179b` |
| `src/gpt/articles/faith/four-last-things-shared/format.tex` | `98eea2ad1b83ae442f74c8688ae4695f8bf5aef17b63d8ebdafdffee70c9136d` |
| `src/gpt/articles/faith/four-last-things-03-hell/main.tex` | `f0297747467df2701088eafa241df938176bf168f4f49500273299698a1b041f` |
| `src/gpt/articles/faith/four-last-things-03-hell/generation-metadata.tex` | `1024769c45fb2dc6c2d18c0a624d623cc50acc207b14076b0a0c817f57997c92` |
| `src/gpt/articles/faith/four-last-things-03-hell/references.tex` | `9f1a9b1f78b5d30866747ca52a75e4aa21d4db4439244ec43f1493bd735c9773` |
| `src/gpt/articles/faith/four-last-things-03-hell/web-edition.toml` | `17cbeb94ad4dc5deed90ddf6baf60ce1571f5fbd5bfa7a1086e3ae24c8f477e8` |
| `scripts/_corpus.py` | `db21c0050f83260ebd7a4bce9aea0d72876cecbae2e7b6807c3051dbd0678cfc` |
| `scripts/_proper_components.py` | `bbc722ecaf1d60ea85e786aac7d5b8eedc2bad7be05606eda10470e26c74fb82` |
| `scripts/_scanning.py` | `ac55e8cff701b5d95bf3e582d9b09c49ec3614a7a1a97921dde74f94203108d1` |
| `scripts/_tooling.py` | `d019123d6498b5fc3bfdde1259b7ef6b8aae848bf053053deb402423c2ea85f0` |

The PDF-review renderer fingerprint is `cb6bc6758b165c50bba7f68d7b5e1df5cc66fa3e0aad97361992b67d97cea2ba`; its cache receipt records exact raster tools, review font and settings. Acceptance is restricted to the exact PDF/Markdown/HTML bytes above; render-affecting changes require the corresponding renewed review.
