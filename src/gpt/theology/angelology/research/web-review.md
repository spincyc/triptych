# Web-edition review

Reviewed on 29 September 2026 against the source revision
`2026-09-29T21:48:19Z` and the installed 62-page PDF. The web edition is a
reviewed conversion of the canonical TeX, with no hand-edited publication prose
or declared material omissions.

## Artifact identity

| Artifact | SHA-256 |
| --- | --- |
| `web/gpt/theology/angelology.md` | `34d3c866336e843930bcec50f5d0ae0881131378b7294f2ab0672038e81c75a6` |
| `pdf/gpt/theology/angelology.pdf` | `f2bd6116ad41e7459ce0ab48bebf6327844dc82676908960c77f893617959bec` |
| Reader HTML rendered by the repository's `public-alpha` renderer | `a5647cbfda774b0ebb0f06c1efe01a1ad00855aa901bd012f7b2cf66851ebe23` |

Conversion used the repository tool, installed Pandoc, and the bound
`Markdown==3.10.3` renderer. The installed Markdown is byte-identical to the
accepted generated file. The HTML above was rendered in an isolated review
subset with the actual site template and assets; it is not a claim that a full
release artifact was built, verified, or deployed.

## Fidelity and navigation

The reviewed output retains 36 tables, 286 table rows, all 118 article-census
rows, and 184 footnotes. All 26 dossiers retain their Summa, Grade, and
Authorities fields; the 18 recorded Contrary opinion fields remain present.
The comparative order ranks, citations, Dionysian chapter concordance, and
calendar and name tables retain their cell content. The names table does not
repeat its continuation header. No raw TeX, duplicate HTML identifiers, or
unresolved internal fragments remain. Revision timestamp and rights colophon
each appear exactly once.

The bibliography's scripture-index link uses its descriptive title, avoiding
the converter's numeric rendering of an alphabetical appendix reference.
The final source separates the metadata group from the preceding spacing
command by a blank line; this preserves the timestamp in Pandoc's output.

The orders, article census, concordance, and question headings were inspected
in Chromium at desktop and narrow widths. Footnote navigation reached `#fn:1`
and returned through its backlink to `#fnref:1` at 1440 and 320 CSS pixels.
At 320 pixels the existing table presentation scrolls horizontally within the
reading plane; all columns remain available and the document does not overflow.

## Browser gate and bounds

The final HTML passed 104 of 120 assertions in the existing
`corpus_browser_gate.mjs`, over one route and nine viewport/emulation states;
12 assertions were inapplicable and skipped. The four failures are the existing
shared-shell 44-by-44-pixel target-size checks for Triptych, Faith, Licensing,
and Third-party material, repeated across four handset states. Their status as
a shared design dependency is recorded in
`guidance/corpus-browser-implementation.md`, section 20.2, FP1.

The gate passed console and request health, internal links, landmarks, heading
identity, accessible control names, focus and tab traversal, no-script static
content, project-subpath startup, and 320-pixel document reflow. The current
shared publication renderer supplies no Contents interface and does not label
its horizontally scrolling tables as focusable regions. Those existing Reader
limitations were observed, not repaired or represented as passing controls.
No site generator, stylesheet, shared browser asset, or converter was changed.

The focused document-library check confirms the title and 62-page installed
extent. The document catalogue and source-reader projection were regenerated;
their currentness checks passed. The source-reader rights check retained all
2,134 withheld passages with stated reasons. These mechanical and browser
checks do not assert independent human theological review.
