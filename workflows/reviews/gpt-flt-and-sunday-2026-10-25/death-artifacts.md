# Death — independent artifact review, 2026-10-25

**Disposition: ACCEPT** for the exact candidate PDF, Markdown, and rendered HTML below. No artifact blocker was found. This acceptance covers visual production and conversion fidelity; the independent content/source judgment has its own receipt. Installation and whole-site release verification remain with the coordinator.

## Reviewed snapshot

The review used the uncommitted death revision on workspace branch `feature/propers/codex`, with repository HEAD `24c1b7ce1781f79937f57b66c221b0ed82e219d9`. The frozen source and build hashes matched the assignment before review and at completion. Revision timestamp: `2026-10-25T20:34:12Z`. Governing profiles read: `guidance/editorial.md`, `guidance/repository.md`, `guidance/articles.md`, and `guidance/web-editions.md`, with the repository instructions and tool registry.

| Accepted artifact | SHA-256 |
| --- | --- |
| `build/gpt/articles/faith/four-last-things-01-death.pdf` | `8ca2a8d9d519561cb04bbbeb8eaa2d49d16874f30c1219c0f26f247c3b9cc223` |
| `.scratch/flt-death-artifacts/web/gpt/articles/faith/four-last-things-01-death.md` | `7b7c2f747253e0efcc25cf5f2bd87a83f88e6f4181ffbe3a441cd1c67c66f121` |
| `.scratch/flt-death-artifacts/site/web/gpt/articles/faith/four-last-things-01-death.html` | `95aeb1ff019d71781b46c680f123c98c0ade0766c59688d1c4e198abd31d3246` |

The candidate PDF is 24 US Letter pages and 361,055 bytes (about 14.7 KiB per page). Neither PDF size investigation trigger is reached. No publishing raster or illustration is embedded in this text publication. Review PNGs are transient proof images.

The installed mirrors were read-only and still held the earlier revision during this review: PDF SHA-256 `5928264144ab871f1506faa901fe9de56fa5a07843e8a9cba5661886921e4a65`; Markdown SHA-256 `8241301a75ed49cd95d5325588eb40767576da120badb6f439efcf959816ca55`. Those installed bytes are not the accepted candidates in this receipt. The coordinator must install the accepted bytes and verify identity afterward.

## PDF inspection

`tools/pdf-review --output .scratch/flt-death-artifacts/pdf-rasters --cache .scratch/flt-death-artifacts/pdf-cache build/gpt/articles/faith/four-last-things-01-death.pdf` completed successfully. Every page raster, **01 through 24**, was opened and visually inspected individually; contact sheets were not substituted for page inspection. Page 24 was additionally opened at original 1700 × 2200 resolution to inspect the small terminal type.

| Pages | Observed disposition |
| --- | --- |
| 1 | Title, four-essay navigation, and all 19 contents entries fit on one page; page labels are legible. |
| 2–8 | Opening exposition, Augustine, Christology, fear, and baptism: consistent margins and readable type; ordinary paragraph continuations; no clipping or misplaced headings. |
| 9–16 | Personal continuity, uncertain hour, penitent thief, relinquishment, Cyprian, and Polycarp: intact paragraphs, citations, and emphasis. The section-8 heading near the foot of page 9 has accompanying body text and its destination on the same page. |
| 17–22 | Sacraments, accompaniment, grief, annual meditation, and conclusion: sustained readable text; no artificial sparse spill pages, overlapping matter, or heading-only pages. |
| 23–24 | Conclusion proceeds to scope and references in source order. Bibliography continues normally across the page boundary. Revision timestamp and compact rights colophon share page 24 with terminal content; both are readable, unclipped, and non-overlapping. No rights-only page. |

`pdfinfo` reports PDF 1.7, 24 pages, no encryption, no JavaScript, and no suspicious structure. It is untagged. All 11 font entries are embedded, subsetted Latin Modern Type 1 fonts with Unicode mapping; no missing or substituted glyphs were observed. Title and subject match the declared metadata. The modification date corresponds to the tracked UTC revision; no creation date is emitted.

The settled log contains no fatal error, undefined reference, overfull box, or rerun request. Its sole layout warning is `Underfull \\hbox (badness 10000)` for an **empty** box at the terminal metadata/rights boundary (`lines 3--340`). Page 24 and the extracted text were checked directly; the empty box has no visible spacing, clipping, or content loss. The warning is disposed of by that inspection.

`tools/check-pdf-anchors build/gpt/articles/faith/four-last-things-01-death` exits 0: 19 contents lines and 19 bookmarks, all on their own heading anchors. The `.toc`, `.out`, `pdfinfo -dests`, and rendered headings agree on the 17 numbered sections and two appendices. The PDF contains the expected four relative companion-PDF links, two Vatican source links, and the CC BY link; `pdftohtml -xml` preserves their actual targets. The PDF companion links are mechanically correct sibling filenames; final installed sibling identity is a coordinator check.

## Web conversion and browser review

With the pinned publication Python on `PATH`, `tools/web-edition --provider gpt --output .scratch/flt-death-artifacts/web articles/faith/four-last-things-01-death` exits 0. The targeted eligibility and rendered metadata gates also exit 0:

- `tools/check-web-edition --provider gpt --document articles/faith/four-last-things-01-death`: one eligible leaf.
- `tools/check-generation-metadata --provider gpt --pdf articles/faith/four-last-things-01-death build/gpt/articles/faith/four-last-things-01-death.pdf`: one valid canonical metadata record.

The complete generated Markdown was compared with the source and PDF. A supplemental paragraph audit covers **all 159 source prose and reference paragraphs**, including the terminal scope and all 13 bibliography entries. Each occurs exactly once in normalized PDF extraction and HTML, and the complete 159-paragraph sequence in HTML equals the source sequence. Normalization folds typographical ligatures and punctuation and ignores print line wrapping; it does not purport to certify punctuation by itself. Visual PDF review and inspection of generated/rendered text supply that complementary check. Heading labels, references, biblical numbering qualifications, italic titles, the revision timestamp, and the full common rights wording survive. No omitted appendix, unexplained extra exposition, raw TeX, or leaked model/provenance metadata was found.

The scratch HTML is rendered through the **current** `tools/public-alpha` functions `rewrite_links` and `render_page`, using the actual current layout, stylesheet, and locked Python Markdown 3.10.3 dependency. No hand-made HTML approximation or whole-site build was used. Existing baseline site files supply only neighboring routes for link navigation; they do not supply the reviewed death content. The web subtitle is the PDF's declared subject metadata; print title formatting and section numbers are adapted for reflow.

Chromium `156.0.8078.47` was driven through its DevTools protocol at **1440 × 1000**, **393 × 852**, and **320 × 852**. At each width, screenshots of the title/contents, first substantive section, Polycarp section, and terminal rights/footer were opened and inspected. All 12 screenshots show legible reflow and clear heading/paragraph distinction. The long title and long contents labels wrap at narrow widths. The 320px revision timestamp wraps within the reading column without loss. No horizontal clipping or overlap was observed.

At each viewport, DOM checks found 19 H2 headings, exactly 19 contents links with existing targets, no duplicate IDs, one visible revision timestamp, and no element crossing the horizontal viewport. Document scroll/client widths are 1425/1425, 393/393, and 320/320 respectively (desktop scrollbar accounts for the first width). Every contents link was actually clicked and allowed to settle; each brought its own target heading to within 0.5 CSS px of the top. Judgment, Hell, and Heaven links were clicked at all three widths and opened the correct baseline sibling routes and titles. This verifies navigation targets, not the revised contents of those independent articles. No JavaScript exception was captured. This was a local file-backed visual/navigation check; no hosted deployment or network availability claim is made.

## Source and render identity

Acceptance is invalidated by a render-relevant change to the accepted source or these dependencies. A future installation may retain this receipt only when it reproduces the exact accepted artifacts.

| Input | SHA-256 |
| --- | --- |
| `src/gpt/articles/faith/four-last-things-01-death/main.tex` | `4a02d4c12e8403f0f1032f9cd765ae74ca876f5cb5b968fae5f9630026a71bf3` |
| `src/gpt/articles/faith/four-last-things-01-death/references.tex` | `f70d8534b1f50fea3923dc191d0a5172abf936a4dccfa6961897fe9ddb9620d7` |
| `src/gpt/articles/faith/four-last-things-01-death/generation-metadata.tex` | `33aff3b19cfc35441c857ddd296b6cc32cc3b8db5df19381a1994fba8d322118` |
| `src/gpt/articles/faith/four-last-things-01-death/web-edition.toml` | `09e34512dd6dd8da6af7abd36c07e276f1271021bc435d4ed72ba8ecb5d74077` |
| `src/gpt/articles/faith/four-last-things-shared/format.tex` | `98eea2ad1b83ae442f74c8688ae4695f8bf5aef17b63d8ebdafdffee70c9136d` |
| `src/common/preamble.tex` | `4471c68736e6d1bfd95032159e1aabd75f7d925b51a3b3dbfdb6e915eb79179b` |
| `tools/web-edition` | `10c10959da1485d0d95773234f2d615ee21c3139896b430ebea7614f5ca52d57` |
| `scripts/web-shim.tex` | `33abd8946680492c3d45785bbf7c39afea1c047d62bed8b57fd0b0e13a56545e` |
| `tools/public-alpha` | `e8d28ee9ddf942225010a249574b67cbe38fb9dfee37e223df102aa7155a6331` |
| `scripts/_markdown_render.py` | `be0ffcd9d3d0b789f633be2938c07c9076d44d72eb3b6c5eb65b93307e6fa648` |
| `release/public-alpha/layout.html` | `6687546feca2e378e57917fa44ed908c5abfa49f4499731c95316f1d34b3d9eb` |
| `release/public-alpha/assets/site.css` | `004f8a18f127c2fbced58190c458b7b2819f12da065431c13fd69abf927dcb47` |
| `requirements-public-alpha.txt` | `59bd4c5252324612c6ce5a27f4a4ba4e62aa4cc76bc3d974a29b45491c97c762` |

## Evidence and limits

All mutable review work is under `.scratch/flt-death-artifacts/`: `pdf-rasters/` (24 individually viewed pages plus bounded contact sheets and renderer receipt), `web/` (accepted generated Markdown), `site/` (accepted target HTML with exact current assets and baseline neighboring routes), `screenshots/` (12 inspected viewport captures), and `audit/` (PDF information/fonts/destinations/links, log screen, anchor gate, full paragraph audit, dependency hashes, and browser interaction/DOM receipt). `render_audit.py` and `browser_review.mjs` retain the task-local reproduction commands. The PDF-review renderer fingerprint is `cb6bc6758b165c50bba7f68d7b5e1df5cc66fa3e0aad97361992b67d97cea2ba`.

No source, installed output, release record, shared data, or unrelated tracked file was changed by this review. No commit, push, deployment, whole-site build, specialist approval, or content/source reacceptance is claimed. Independent review artifacts are transient; this tracked receipt preserves the disposition and exact identities.
