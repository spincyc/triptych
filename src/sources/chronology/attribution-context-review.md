# Traditional attribution and passage dates — 2026-09-09

The recent GPT proper guides 54–56 showed a general Psalm composition bound
where the reader also needed the traditional Davidic frame. Their generated
annotations faithfully reproduced the corpus: it had no relation for an
attributed figure's era independent of composition or a named occasion.
The comprehensive coverage gate could be satisfied by “before c. 165 B.C.”
without answering that additional question. This was an omission of context,
not evidence that David belonged to the second century B.C.

## Evidence and correction

The new `traditional-attribution` relation connects an inspected attribution
to a named temporal subject. It does not assert authorship as historical fact,
date the received text, or identify an otherwise unknown episode. The subject
`israel.monarchy.david-traditional-era` holds Corbett's regnal reference once;
the six Psalm scopes reach it through bindings carrying their title witnesses.

John Corbett, “David, King,” *Catholic Encyclopedia* IV (1908), printed p. 642,
opening paragraph, reports the “usual chronology”: birth in 1085 and reign
from 1055 to 1015 B.C. He immediately distinguishes a later reckoning prompted
by Assyrian inscriptions. The existing source is
`passage.catholic-encyclopedia.volume-4.new-york-1908.corbett-david-usual-chronology`.
Its source record identifies artifact page 722 and the earlier facsimile
collation. This revision inspected that record and the retained article text,
not a newly retrieved facsimile. The retained text is under the same edition,
artifact `newadvent-04642b-f1c0bed3-article-text`, line 3.

The range remains `reported-traditional` and `disputed`, following the existing
birth-of-David claim's treatment of the same sentence and competing reckoning.
Its source label is retained; its displayed subject names the reign in the
usual chronology. No rounded year 1000, inferred lifetime, or conversion of
Anno Mundi is introduced. A regnal reference orients the attributed figure;
Psalm 33's pre-accession escape is not placed inside those regnal years.
The existing forty-year reign duration and all previous event claims remain
unchanged.

| Vulgate Psalm (Hebrew number) | Inspected title witness | Disposition |
| --- | --- | --- |
| 33 (34) | Douay 33:1: David, change of countenance before Achimelech | Attribution added; existing Geth title-setting retained. |
| 39 (40) | Douay 39:1: a psalm for David | Attribution added; no occasion inferred. |
| 70 (71) | Douay 70:1: David, sons of Jonadab, former captives | Attribution added; separate Davidic and captivity settings retained. |
| 83 (84) | Douay 83:1: sons of Core | No David binding; Korahite composition claim retained. |
| 85 (86) | Douay 85:1: a prayer for David | Attribution added; no crisis inferred. |
| 91 (92) | Douay 91:1: Sabbath canticle | No named author in the inspected title. |
| 94 (95) | Clementine 94:1: *Laus cantici ipsi David* | Attribution added. The Douay heading omits it; Hebrews 4:7 corroborates reception “in David.” |
| 97 (98) | Douay 97:1: a psalm for David | Attribution added; distinct Nativity referent retained. |
| 101 (102) | Douay 101:1: prayer of an afflicted poor man | No named author in the inspected title. |
| 117 (118) | Douay 117:1 has no author heading | No title-derived David binding. |

These are findings about the inspected titles, not denials of Davidic reception
elsewhere or a complete Psalter authorship census. The title text is available
in `src/sources/bibles/<edition>/chapters/Ps/<number>.json`. All six Hebrew
queries reach the same shared chronology through the existing concordance.

## Earlier Old Testament checks

Genesis 12:4 already returns the call of Abram as `narrated-event`: his age of
75 and three traditional Flood-to-call intervals, not dates of Genesis's
composition. Its inspected composition gap distinguishes Mosaic attribution
from a dated act of writing. Exodus 3:1–2 already reaches the burning-bush
event through the registered Haydock Exodus 3 passage (printed p. 75,
artifact page 103). Its printed A.M./A.C. figures remain as recorded, with
their existing apparatus discrepancies; no composition date is inferred.
Tests also exercise Joshua 6:20, 3 Kings 6:1 and 1 Maccabees 4:52, where
event chronology and textual chronology coexist. The publication projection
now leads with these events before the text's composition history.

A separate concern remains for `composition.book-of-wisdom`: Gigot's retained
“Book of Wisdom” article, `newadvent-15666a-999fbc07-article-text.txt`, lines
23–35, dates the persecution the writer has in view to two possible Ptolemaic
reigns and allows later publication. The corpus's strict composition intervals
may therefore overstate those writing bounds. This is a source-relation review
finding, not a corrected or accepted date. The same article distinguishes the
Solomonic literary persona from actual authorship, so this revision gives
Wisdom no automatic date for Solomon's lifetime.

## Publication boundary

The generated annotations put traditional attribution and identified settings
or events before textual history, preserving every applicable claim and its
profile, disposition, source label and locus reach. Different subjects under
one relation remain distinct groups. Attribution alone never counts as an
event date; attribution plus composition retains `composition-only` status.
Guidance owns the enduring rule; tests enforce the projection and exclusions.
GPT 54–56 and the held Claude 54 consumer are refreshed together. The Claude
hold and its unrelated editorial findings are not cleared by this revision.
Build, visual and integration results are recorded in `PROJECT-WORK.md`.

## Rendered review and installed artifacts

All eight affected PDFs were rebuilt and visually reviewed: every page in
bounded contact sheets, with the date dossiers, changed reference pages and
colophons reopened at full resolution. GPT 54–56 retain full/synthesis counts
20/14, 16/12 and 20/13; held Claude 54 retains 61/34. Every date dossier remains
on page 2. The wider Date columns, concise explanatory prose and bold relation
labels keep those distinctions readable. GPT 55 uses the common compact rights
notice to preserve its final-page bottom margin.

The canonical web editions preserve each displayed date, source qualification,
reference and colophon. The reader template was inspected in Chromium at 1280,
375 and 320 pixels: no page-level overflow, duplicate IDs or broken internal
fragments. GPT dossiers reflow into stacked entries; the held Claude edition
retains its existing horizontally scrolling table. Its existing PDF URL-control
text defect (full p. 55 / synthesis p. 28) and sparse scope tail (full p. 54 /
synthesis p. 27) remain recorded; this correction does not release that edition.

The following hashes identify the visually reviewed PDFs installed locally.
PDFs are reproduced from tracked source during deployment, not committed.

| Provider / proper | Edition | Pages | SHA-256 |
| --- | --- | ---: | --- |
| gpt 54 | Full | 20 | `fba11f7a3d5444576af4efb40c9e06c2bcda37d6e47524828fe80069bd8d3b8f` |
| gpt 54 | Synthesis | 14 | `9de6340484b905972e86c6c4bfdcab2ea8eb148ba9406efb6a7259ea50dd293c` |
| gpt 55 | Full | 16 | `a834e2746a1c8b10bcb699975cedd6fd8ee4ca023e6ee9fbdfce913d3d77d6c1` |
| gpt 55 | Synthesis | 12 | `5250b81ba6bb6a9dd4e06c56db041a9d141d9744490e7b6875e9fcbc2c290ff4` |
| gpt 56 | Full | 20 | `5ae7d6f65d46a3fcfd7f6f0a08a24747c3cf208d90356d223e11934bb1ff7bee` |
| gpt 56 | Synthesis | 13 | `e4cc43275bd9f7880278d538313927d1627932c51507f4878bee4c782e2647ea` |
| claude 54 | Full | 61 | `2d6c9a136beb598692d1976c13b2f7c1a3fc5e105a1a7a1274231db5cc1a024d` |
| claude 54 | Synthesis | 34 | `679050fcb9baf0b4b3630467253a14e44a0da57bdc331c1dcceabb621e4c15e0` |

Reviewed canonical web editions:

| Provider / proper | SHA-256 |
| --- | --- |
| gpt 55 | `b6a7d30e8e2eeb6aecfb05ea8c81da69fdb319e059686bcb47d92b166a69ad5e` |
| gpt 56 | `2bda5806d1904ef917029b37f6d6bb010b683fb2825e569058233d6183c971f0` |
| gpt 54 | `6fe991c397da5f29613804efbd60e4a0d59ee9020c5d8d79893b6f5ea188c29d` |
| claude 54 | `6d669b27a0afe09f10b874354d8ed3102ac5c145d03a19f39365601ff3935320` |

## Validation

The 258-test chronology suite, 29-test annotation suite, 56-test workflow
chronology suite, 38-test web converter suite and derivation-lineage test pass.
The generated profile-contract review manifest retains its pinned base and
all 507 earlier cases; its only added cases are this temporal claim and binding.
A fresh checkout may need `git fetch origin
c1dee9fc0ddfea3ea06d951c7ad25d05b75b0341` before running the two historical
manifest tests. The fetch restores the comparison input; it does not change
the workspace branch or the manifest's base.

All content-preflight checks pass for GPT 54–56. The source, inventory,
publication catalogue and release-binding checks are recorded in the owning
`PROJECT-WORK.md` entry.

The final `make check` and `make check-sources` pass. All 239 runnable captured
examples replay without divergence or tracked-state writes; six intentionally
exempt and three unavailable sample-PDF examples remain explicitly reported.
