# Production review — Claude angelology

Review date: 30 September 2026. Publication: *The Angels: Nature, Knowledge,
Will, Fall, Order, and Ministry*. Revision timestamp: `2026-09-30T19:11:32Z`.

## Text and research

The body has 25 sections in the profile's reader order: Scripture; the faith
of the Church; the writings before Christ (the Septuagint, the Jewish
writings outside the canon, Philo, and the Greek poets and philosophers) and
their reception by the Fathers; the Greek Fathers before Dionysius, the
Latin Fathers with Augustine, the fifteen chapters of the *Celestial
Hierarchy*, and the Fathers and Doctors after Dionysius to Bonaventure; every
article of ST I qq. 50–64 and 106–114 in the *Summa*'s order, one graded
dossier per question; Christ, Mary, and the angels (with III q. 8 a. 4,
q. 30, q. 59 a. 6); the disputed questions after Aquinas; the Byzantine line;
the liturgy; devotion and its regulation; the saints and the holy angels; and
the angels in the order of the universe. Fifteen appendices follow, with the
scope appendix, references, and generation metadata.

`research/question-inventory.md` holds 124 articles (the 118 of the two
question ranges and six Tertia Pars articles), and the article census
projects it. The order inventory, terminology audit (275 consolidated rows),
source audit, and `research/source-bindings.toml` (288 bindings over 159
newly registered works and existing records) carry the evidence. Drafting
lanes read their witnesses at their loci in the public editions the source
audit names; each lane's quotations were checked against its cached witness,
and a whole-book pass removed the compiler's English renderings from
quotation marks, leaving the original with a plain gloss.

The maintainer's 30 September 2026 directions — a declarative voice at each
degree of determination, an expansive patristic account, an authentic
Catholic treatise, and research into continuity with pre-Christian writings —
are recorded in the profile ("Voice and determination"; the corpus paragraph
on pre-Christian writings) and in `research/scope.md`, and the whole body was
revised to them.

Every contribution is by Opus 5.5 (Factory Droid on 29 September; Claude Code
and Opus 5.5 subagents on 30 September), as the generation metadata records.
This is AI research and review; no independent human theological,
clerical, or ecclesiastical review has been performed or is claimed.

## PDF build and visual review

`make doc DOC=theology/angelology PROVIDER=claude` passes with no overfull
boxes and no undefined references; the one underfull box is in the terminal
generation-metadata block. The 369-page PDF embeds all 19 fonts; title and
subject metadata are present; the text layer carries about 290,000 words;
the rights colophon and revision timestamp close the book.

Every page was inspected at full size (200 dpi rasters from
`tools/pdf-review`) in four passes by independent review lanes:

| Pass | Pages | Lanes | Findings | Disposition |
| --- | --- | --- | --- | --- |
| 1 | 375 | 5 | 216 | applied (with book-wide pattern fixes), a few applied differently with recorded reasons |
| 2 | 373 | 5 | 144 | applied; one rejected (the witness's own punctuation) |
| 3 | 368 | 5 | 36 | applied; one kept as the 1870 witness prints it |
| 4 | 196 changed pages of 369 | 3 | 0 | clean |

After pass 3 the page bodies were compared by hash with the page number
masked: 173 pages were identical to pages already reviewed, and the 196 that
changed (mostly by reflow) were inspected in pass 4.

After the web review, the fifteen *Celestial Hierarchy* chapter labels
moved inside the `\chchapter` macro so the converter can tie each label to
its heading, and the revision timestamp was renewed. All 368 pages before
the colophon rasterize byte-identically to the reviewed pages; the final
page, which carries the new timestamp, was inspected.

Installed PDF SHA-256:
`7d641c0b2ecdb5ebf84a3376e37eda9a12feca7500a7cccfce40a4f5cfae84c7`.
`make install-doc` installed exactly the reviewed build's bytes at
`pdf/claude/theology/angelology.pdf`.

## Web edition

`tools/web-edition` generated `web/claude/theology/angelology.md` with the
pinned Python Markdown. A review lane compared it with the PDF: all 731
contents entries in order; all 68 tables with every row and cell (6,192
cells); 223 quotations, 31 footnotes, and 33 dossier frames; the rights
colophon and revision timestamp; no converter damage; 69 of 70 random
passages and the first and last paragraphs of every section matched word
for word, the rest differing only by the two faults below.

- References to appendices printed pandoc's running section numbers
  (26–41) where the PDF prints letters. `tools/web-edition` now letters any
  reference to a label defined after `\appendix`, with regression tests;
  the converter suites pass (155 tests). The same correction changed one
  line in each of two other tracked editions,
  `web/claude/theology/mariology/rosary.md` and
  `web/gpt/theology/heresies/heresies-in-catholic-history.md`, each now
  printing the appendix letter its PDF prints; both were reinstalled and
  their release bindings refreshed.
- Eleven references to *Celestial Hierarchy* chapters printed the raw
  label; the labels now sit inside the chapter macro.

After both fixes no numbered appendix reference and no raw label remains,
and `make check-web-editions-current` regenerates every tracked edition of
both providers byte-identically. Installed web edition SHA-256:
`23c29b69f321a0275d68548c6e88d20262a9a75acc252cc47a8b90d47e680a39`.

## Gates

`make check-sources`, `make check-metadata PROVIDER=claude`,
`make check-web-editions PROVIDER=claude`, `make check-document-catalogue`,
`make check-web-editions-current`, and `tools/release-bindings status`
(exact) pass. The release record `release/publications/claude/theology/angelology.json`
is `alpha` under the standing public-alpha authorization, and the Faith
catalog's angelology row links both editions under their exact titles. The
work is on the feature branch; nothing was merged to `main` or deployed.

## Evidence ceilings carried forward

- Many Latin and Greek texts were read in archive.org OCR of Migne and other
  printings and were not collated with modern critical editions (among them
  Gregory's *Homilies* 34 via Hurter and Wikisource, Jerome in PL 25–26,
  Honorius in PL 172, Bonaventure's Quaracchi volumes, and PG 29 and 44).
- 233 bindings are catalog-level: the bytes read remain in the working
  cache, not in the source library.
- Some authorities are known only through the *Summa*'s citation of them
  and are attributed that way.
