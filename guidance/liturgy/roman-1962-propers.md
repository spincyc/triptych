# Roman Missal 1962 Proper-Guide Profile

This profile governs source-first guides to temporal, ritual, votive, and other proper formularies in the 1962 *Missale Romanum*. It does not govern calendar assembly, the Ordinary or Order of Mass, postconciliar propers, standalone theological references, or discursive articles. Use `guidance/liturgy/roman-1962-assembly.md` for edition-specific assembly and calendar questions. Universal evidence, metadata, review, rights, and publication rules remain in `guidance/editorial.md`; repository paths and build rules remain in `guidance/repository.md`.

Each guide is a hand-missal companion, not an official liturgical text, critical edition, homily, or substitute for the cited sources. It should help a reader perceive the appointed texts as one ordered liturgical action while keeping verified text, documented history and reception, editorial synthesis, and exploratory proposal distinct.

## Collection Identity

- The temporal series uses 52 Sunday identities in a stable Lent-first repository order: `01` is the First Sunday of Lent and `52` is Quinquagesima. These IDs are catalog identities, not the occurrence schedule of a civil year.
- `46R` through `49R` identify the resumed Third through Sixth Sundays after Epiphany. Each is a separately sourced formulary variant under its shared ordinal because it combines the relevant Epiphany orations, Epistle, and Gospel with the chants appointed for resumed use after Pentecost. [Calendar computation](calendar-computation.md) owns the arithmetic that decides how many are resumed in a given year; the Missal's own rubric decides which and in what order.
- `F` identifies a general-calendar feast assigned to Sunday without a stable temporal ordinal. Verify its printed place and occurrence rule; do not invent a permanent Sunday number for a fixed-date, movable, or local feast.
- `M` identifies a ritual, votive, or other non-Sunday guide. The prefix does not state rank, permission, or authority to replace an occurring Mass.
- Identify every work by the 1962 edition, printed formulary heading and rank, place in the book, and governing occurrence or use rule—not by filename or a modern civil date. Do not merge distinct formularies. Record seasonal substitutions, ritual additions, blessings, or alternate conclusions wherever they govern the guide.

### Canonical temporal registry

This profile owns the stable series. The reader catalog and production plan
must reproduce this order exactly; neither may infer, rename, or renumber it.

| IDs | Formularies, in order |
| --- | --- |
| 01–06 | First, Second, Third, and Fourth Sundays of Lent; First Sunday of the Passion; Second Sunday of the Passion (Palm Sunday) |
| 07–14 | Easter Sunday; Low Sunday; Second, Third, Fourth, and Fifth Sundays after Easter; Sunday after the Ascension; Pentecost Sunday |
| 15–23 | Trinity Sunday; Second through Ninth Sundays after Pentecost |
| 24–38 | Tenth through Twenty-third Sundays after Pentecost; Twenty-fourth and Last Sunday after Pentecost |
| 39–45 | First through Fourth Sundays of Advent; Sunday within the Octave of the Nativity; First Sunday after the Epiphany (Holy Family); Second Sunday after the Epiphany |
| 46–52 | Third through Sixth Sundays after the Epiphany; Septuagesima; Sexagesima; Quinquagesima |

The separately sourced resumed variants are `46R`, `47R`, `48R`, and `49R`,
the Third through Sixth Sundays after the Epiphany resumed after Pentecost.
They are subordinate variants of the shared ordinal, not four additional
members of the 52-item spine. Fixed or movable universal feasts that can
replace a temporal Sunday remain in the `F` series and never renumber this
registry. `M01` and later `M` identities remain a separate non-Sunday series.

### Sacred Triduum identities

The stable Sunday temporal series remains `01`--`52`. The following permanent
non-Sunday identities complete the 1962 Sacred Triduum without renumbering or
reinterpreting that series:

| ID | Required slug stem | 1962 identity |
| --- | --- | --- |
| T01 | `t01-mass-of-the-lords-supper` | Mass of the Lord's Supper |
| T02 | `t02-solemn-liturgical-action-of-the-passion-and-death-of-the-lord` | Solemn Liturgical Action of the Passion and Death of the Lord |
| T03 | `t03-easter-vigil` | Easter Vigil |

Each is one planned proper-guide target under `propers/temporal/`. These are
edition-identified English catalog names, not an attempt to impose the
postconciliar taxonomy on the 1962 books. A source audit retains a collation
note if the controlling edition's exact printed capitalization differs.
Reader-facing catalogs print only the celebration names, not the stable `T`
identifiers.

## Source Records and Text Control

Each guide leaf keeps its source and audit records beside `main.tex`:

```text
propers/retrieved.txt
propers/verified.md
research/scope.md
```

- `retrieved.txt` preserves a focused machine-readable pull, including OCR errors and enough boundary text to identify the formulary. It is an unedited finding aid, not publication text.
- `verified.md` preserves the facsimile-collated appointed text in liturgical order, including seasonal and ritual variants. Its provenance identifies the missal edition; printed heading and rank; retrieval URL, source identifier, and date; printed pages and digital leaves; checksum when available; facsimile URL; verification status and date; and unresolved discrepancies.
- `research/scope.md` records the sources, languages and corpora searched; claim roles; material negative results; material rejected or unresolved leads; competing historical judgments; and operational qualifications displaced from the PDF. It is an audit record, not a diary.

Use the following public witnesses unless a better edition-identified witness is documented:

1. The CMAA [1962 *Missale Romanum* facsimile](https://media.churchmusicassociation.org/pdf/missale62.pdf) controls Latin text, rubrics, rank, references, and formulary boundaries. Cite the printed missal page, not only the digital page.
2. The Internet Archive [full-text OCR](https://archive.org/download/MissaleRomanum1962RomanMissalColorLatin/Missale-Romanum-1962-Roman-Missal-color-latin_djvu.txt) locates headings and passages but never controls published wording.
3. The Internet Archive [image item](https://archive.org/details/MissaleRomanum1962RomanMissalColorLatin) is a secondary image witness for unclear readings. OCR and images derived from one item are not independent witnesses.

Visually collate every published Latin form, rubric, citation, and boundary against the controlling facsimile. Check an unclear reading against a second image witness; disclose substitutions and disagreements; never silently blend witnesses. Keep only focused extracts in the repository. Psalm citations use the missal's Vulgate/Septuagint numbering first, with the common modern number in parentheses where it differs.

Study every appointed text in full and read each direct biblical passage in its complete literary context. Every appointed element must contribute to the guide; add, substitute, or locally define cues for Tracts, Sequences, ritual prayers, blessings, and other actual texts rather than forcing a ten-row Sunday template.

For every new or substantially revised guide, maintain a passage-by-passage reception matrix in `research/scope.md`. Give each distinct appointed passage or material scriptural adaptation one row, name every proper that uses it, and record: direct ancient exegesis checked; medieval, Doctoral, or later saintly reception checked; works, loci, languages, and corpora searched; how any retained witness is used; and material negative results. Search direct commentaries, homilies, and psalm expositions before broader doctrinal or liturgical reuse. Sample both Greek and Latin traditions where relevant and available, then medieval Doctors and later canonized exegetes or spiritual writers. A catena may map leads, but verify the underlying work and locus before publication.

“Broad” means that every appointed passage receives a documented search across the major reasonably accessible patristic and saintly corpora relevant to it; “deep” means that the guide explains and, where useful, compares the reasoning of checked witnesses rather than stacking names or aphorisms. Retain at least one direct witness for a passage when one is located and more than one where they materially differ or develop the reading. When no responsible direct witness is found, say which corpora were checked and use any illuminating reuse only under that label. Never claim to have found all witnesses everywhere; state the bounded search and preserve a discoverable omission for later research.

## Published Text and English

### Component architecture

New and substantially revised guides are authored once in a
canonical leaf with `proper-components.toml`. The bare ID produces the
complete research PDF and the sole complete HTML edition. A mechanical
`-synthesis` PDF companion is compiled from the same source; it is not another
leaf and owns no prose, audit record, or web declaration.

The manifest gives every appointed element a stable lowercase kebab-case key
and every ordered component a path, output modes, dependencies, bound element
keys, and component-scoped reference files. Every cross-element synthesis
relation names at least two element keys and one or more controlled evidence
classes. An included component may never depend on an omitted component.

The full research sequence is: the existing pages 1 and 2; lawful complete
appointed text; `Each Proper in Full`, including the bounded patristic and
saintly reception sweep for each element; an exactly two-page `The Propers:
Themes and Movement`; unbounded `Source-Grounded Synthesis Across the
Propers`; unbounded `Interpretive Possibilities Across the Propers`; `The
Propers: Notable and Quotable`; and terminal apparatus. The synthesis
companion retains pages 1 and 2, the two-page brief synthesis, the complete
source-grounded synthesis, the complete exploratory synthesis, notable
quotations, and terminal apparatus. It omits complete appointed texts. It may
retain the element-by-element sweep when that commentary is needed for a
substantive, evidence-bearing synthesis rather than a thin digest; declare
that component in `synthesis` mode and keep its prose, citations, transitions,
and references complete.

Because the 1962 canonical edition supplies the complete appointed texts under
the recorded rights basis, its catalog label is `Full PDF`; the companion is
`Synthesis PDF`.

The brief synthesis marks its first page, second page, and the first following
page with `triptych:brief-synthesis:start`,
`triptych:brief-synthesis:end`, and `triptych:brief-synthesis:next`.
After references settle, `scripts/check-proper-components --aux` must prove
that these occupy pages N, N+1, and N+2. Forced breaks alone do not satisfy the
exact-two-page gate.

English is never composed, translated, adapted, or paraphrased by the
guide. It is quoted from a registered public-domain witness and
attributed at first use and in the references:

- Scriptural elements — introit, gradual, alleluia, tract, offertory,
  communion, epistle, gospel — take the Douay–Rheims (Challoner), which
  is the English of the Vulgate the missal prints. Resolve the psalm
  locus in the missal's Vulgate numbering, not the modern one; a guide
  that silently crosses the two numbering systems has published the
  wrong verses.
- Orations — collect, secret, postcommunion, and any other non-scriptural
  proper text — take a registered public-domain hand missal, cited by
  formulary rather than by page. Where a missal's Sunday numbering or
  formulary boundaries differ from the 1962 books, resolve the mismatch
  and disclose it; do not assume correspondence.

Where no public-domain English exists for an element, say so and give
the Latin incipit with a description of what the prayer asks. Do not
supply a rendering of the project's own. Translations under copyright —
the ICEL Missal, the Knox Bible, the Jerusalem and New Jerusalem Bibles,
the RSV and NRSV, the NABRE, the Grail psalms — are never reproduced,
at any length that would substitute for the book.

## Evidence and Claim Discipline

Research is claim-driven, not quota-driven. Prefer primary, official, edition-identified, and direct sources. For each retained witness, identify the author, work, exact locus, edition or stable link, and source role. Distinguish direct exegesis of an appointed passage from doctrinal illumination. A catena, anthology, search result, OCR transcription, or secondary citation is only a lead until the underlying source and attribution are checked. Preserve material disagreement and uncertainty rather than manufacturing consensus.

Classify substantial claims as follows:

1. **Textual observation:** directly verifiable in an appointed text and its context.
2. **Documented historical orientation:** a sourced authorship, date, place, audience, geography, chronology, or salvation-historical judgment, with material alternatives preserved.
3. **Documented reception:** explicitly taught by an identified and checked patristic, saintly, doctrinal, or liturgical witness.
4. **Source-grounded synthesis:** a restrained conclusion demonstrably supported by the first three classes.
5. **Exploratory proposal:** a new analogy, symbolic extension, cross-proper connection, compositional inference, application, or theological proposal not established by the evidence.

The first four classes may appear in source-grounded sections. The fifth appears only in `The Propers: Interpretive Possibilities`. An unverified lead supports no published claim. Never put an editorial proposal in a source's mouth, imply consensus by proximity, or use the four-senses table to conceal an unsupported inference.

## Reader-Facing Order

Use this fixed macro-order:

1. Page 1: Propers map and four senses
2. Page 2: `Scriptural Date and Location`
3. `The Propers: Themes and Movement`
4. `The Propers: Detailed Commentary`
5. `The Propers: Notable and Quotable`
6. `The Propers: Interpretive Possibilities`
7. `Sacramental Appendix` when required
8. `Appendix: Scope and Qualifications`
9. `References`
10. `Generation Metadata`

The page-2 sheet is the sole exception to terminal historical apparatus. Do not front-load any other chronology, status panel, research boundary, date range, source survey, or general qualification. Put work-wide bounds and qualifications in the terminal appendices. Keep a qualification beside a claim only when it materially changes that claim.

### Page 1: Propers map and four senses

Map every actual appointed element in liturgical order. For an ordinary Sunday this normally means Introit, Collect, Epistle, Gradual, Alleluia or Tract, Gospel, Offertory, Secret, Communion, and Postcommunion; include a Sequence or ritual text when appointed. The map presents the proper, its incipit or reference, its scriptural or grammatical axis, and a concise demonstrable connection.

Immediately follow it with exactly four rows: **Literal**, **Allegorical**, **Moral**, and **Anagogical**. Ground each synthesis in appointed text or documented reception. Page 1 contains no work-wide historical, geographic, chronological, search, rights, or review apparatus.

Later proper-focused headings may use quiet parenthetical cues in liturgical order: *Int.*, *Coll.*, *Ep.*, *Grad.*, *All.* or *Tr.*, *Seq.*, *Gosp.*, *Off.*, *Sec.*, *Comm.*, and *Postcomm.* Define additional ritual cues locally.

### Page 2: Scriptural date and location

Begin and end physical page 2 with forced page boundaries. It contains only `Scriptural Date and Location` and always occupies exactly one page. Inventory every distinct directly appointed biblical passage once, in Catholic canonical order and then verse order; consolidate repetitions and do not mislabel loose echoes in composed orations as direct quotations. Use the columns `Proper`, `Citation`, `Location`, and `Date`. The citation cell does not reproduce Scripture.

Use a two-tier dossier table. Set the table in `\footnotesize` with top-aligned ragged-right columns of `0.14`, `0.18`, `0.35`, and `0.16\linewidth`, `\LTpre` of `0.15em`, `\LTpost` of zero, and `\arraystretch` of `1.02`. The first row of each dossier is a concise four-field summary: inherited or conventional orientation belongs in the short `Location` and `Date` cells, not multi-sentence qualification. Follow it with `\cmidrule(lr){1-4}` and a full-width ragged-right explanatory row of `0.92\linewidth` that gives historical judgment, audience, life stage, uncertainty, and claim-local sources. End ordinary dossier rows with `0.1em` of breathing space and use `\midrule` only between complete dossiers. When a passage narrates an event, place a separately labeled italic event row between two `\cmidrule(lr){1-4}` rules before the full-width explanation. This summary-row-plus-spanning-dossier hierarchy is the standard; change measurements only when the complete inventory cannot remain legible after the hierarchy and evidence have been preserved.

For each passage, distinguish traditional attribution from historical judgment and give the author or compositional horizon, first audience, composition place and date or range, relevant life stage, and place in Israel's and salvation history. A Gospel dossier separately identifies the narrated event's locating citations, place, and approximate date so composition and event are not conflated. Distinguish writer, event, and recipient geography; give present-day equivalents where useful; state uncertainty and responsible alternatives. Keep source-role disputes and operational research detail in `research/scope.md`, and keep global edition, jurisdiction, rights, search, currentness, and review qualifications in the terminal scope appendix. If the complete inventory does not fit legibly, redesign its dossiers or table rather than spill, omit evidence, or move unrelated apparatus onto page 2.

### Themes, commentary, and exploration

`The Propers: Themes and Movement` begins on page 3, immediately after the page-2 sheet, and occupies exactly two readable pages. `The Propers: Detailed Commentary` therefore begins on page 5. Open the thematic section with a one- or two-sentence thesis and, when useful, one orienting form of no more than four primary stages. Use three to five functional units that account for every appointed element and let a signpost-only scan recover the thesis, movement, decisive evidence, and principal limits. This section contains only source-grounded claims.

`The Propers: Detailed Commentary` supplies the exegesis, textual comparison, reception, doctrinal distinctions, disagreement, and claim-local qualifications that prove and refine the synthesis. Treat every appointed scriptural passage and every composed proper substantively. For Scripture, move from complete canonical context through direct patristic exegesis to later saintly reception, explaining each witness's actual interpretive move and comparing real differences or developments. For composed texts, distinguish verbal echo, doctrinal illumination, and documented liturgical reception. Give each substantial claim one fullest home; remove repeated quotations, recaps, thin subsections, name lists, and stretched links.

`The Propers: Notable and Quotable` is a required compact gallery of three to five non-obvious afterlives of wording from the scriptural propers. Each entry pairs a short exact phrase from an appointed biblical text with a documented later use that changes its register or force: cultural, humorous, ironic, idiomatic, literary, political, institutional, visual, scientific, commercial, or another surprising reuse. Identify the proper, later user or work, context and exact locus; then explain the turn in meaning. Prefer a varied gallery and include humorous, ironic, or deliberate reversal where a verified example exists.

Straight exegesis, doctrinal or devotional reception, an independently similar phrase, and a bare quotation, title, motto, artwork, or musical setting do not qualify. Those materials belong in detailed commentary or references unless the later use demonstrably redirects, contests, jokes with, secularizes, or otherwise makes unexpected work of the appointed wording. Verify the verbal link and later context in a primary source or reliable edition; describe an echo as an echo unless dependence is documented; keep protected excerpts brief. The `Notable-and-quotable audit` in `research/scope.md` records both texts and loci, relationship strength, wording check, context, translation and rights status, cultural payoff, limiting qualification, and material negative results. Quote aggregators and attribution sites are leads only. Never invent a weak example to fill the gallery.

`The Propers: Interpretive Possibilities` is a required discovery section, not a recap. Begin with one compact notice identifying its contents as exploratory editorial or AI proposals, not sourced historical intent or attributed teaching. Give four to six substantial proposals. Each must join at least two precisely named appointed elements; state the connecting mechanism and the theological, intellectual, spiritual, or pastoral fruit; identify what the ordinary element-by-element reading misses; and end with the strongest material limit, alternative, or disconfirming condition. Prefer non-obvious multi-step relations across different ritual moments, literary units, images, verbs, temporal movements, or sacramental actions. Reject generic applications, decorative symbolism, numerology without textual control, and restatements of the detailed commentary.

Before retaining a proposal, search the guide's checked corpus and run a targeted precedent search for its distinctive conjunction. Record an `Interpretive-proposal audit` in `research/scope.md` naming the anchors, mechanism, nearest located precedent or analogue, search boundary, and controlling limit. Classify the novelty result as `precedent located`, `near analogue located`, or `not located in the checked corpus`. The last formula is bounded and correctable; never claim that a connection is universally unknown, unprecedented, first, or authored by the model. A daring proposal may remain when the precedent search is negative, but evidence, doctrine, authorized branches, literal senses, and historical uncertainty still control it.

### Sacramental appendix

When a ritual Mass is celebrated with or specifically for a non-Eucharistic sacrament, import the relevant canonical one-page summary from `src/<provider>/theology/sacraments/summaries/` after `The Propers: Interpretive Possibilities`. Use the full sacramental treatise and its sources for research; the summary is a retrieval aid, not the research ceiling. Do not infer historical formulary intent from general sacramental theology without a source.

## Terminal Apparatus

### Appendix: Scope and Qualifications

Give one terse account of edition and formulary identity, text-verification state, source scope, included and excluded material, geographic and chronological bounds not already carried by the historical appendix, search limits, rights boundary, review state, and material global qualifications. Point to `propers/verified.md` and `research/scope.md`. Leave retrieval mechanics, checksums, query detail, discarded leads, and operational audit in those records. Do not duplicate this apparatus earlier or inside `References`.

### References and metadata

`References` contains only sources actually used, with exact loci sufficient to verify their claims, and immediately precedes `Generation Metadata`. Do not retain unused leads or sources used only by deleted material.

`Generation Metadata` is terminal and imports the leaf's structured `generation-metadata.tex`. Follow the universal metadata standard; refresh the UTC revision timestamp and accurately append materially distinct AI contributions without erasing prior contribution history.

## Profile Gates

Before publication, verify that:

- the catalog ID, printed identity, rank, occurrence or use rule, seasonal and ritual variants, and formulary boundaries are sourced rather than inferred;
- `retrieved.txt`, `verified.md`, and `research/scope.md` are complete, coherent, tracked, and free of machine-local data;
- every published Latin form has been visually collated against the identified facsimile and every appointed element contributes to the map, synthesis, and substantive commentary;
- every direct biblical passage has complete-context research and one historically qualified page-2 dossier, with composition, narrated event, audience, geography, chronology, tradition, and modern judgment kept distinct;
- the research scope has a complete passage-by-passage reception matrix, the major relevant Greek and Latin patristic and later saintly corpora have been searched within stated bounds, every located witness is checked at its work and locus, direct exegesis is distinguished from illuminating reuse, and material negative results are recorded;
- the notable-and-quotable section has three to five source- and locus-identified, non-obvious cultural, humorous, ironic, idiomatic, literary, political, institutional, visual, scientific, commercial, or comparable reuses of wording from the scriptural propers; every verbal relation and contextual turn is verified and audited, patristic or devotional excerpts remain in detailed commentary, and no bare title, motto, artwork, or musical setting pads the section;
- the interpretive section contains four to six non-recapitulatory, multi-element proposals and the research scope records each proposal's anchors, mechanism, targeted precedent result, fruit, and strongest limit without claiming universal novelty;
- every attribution and historical, doctrinal, or reception claim has an exact source and locus, while source-grounded synthesis and exploratory proposal remain visibly distinct;
- the guide follows the fixed reader order, keeps the complete date/location sheet alone on physical page 2, begins its two-page thematic movement on page 3 and detailed commentary on page 5, and places all other work-wide bounds, source limits, rights, review status, and qualifications only in the terminal apparatus;
- a required sacramental summary is imported from the canonical fragment, `References` contains only used sources, and generation metadata is accurate and terminal; and
- the universal editorial, rights, build, warning, visual-review, installation, and publication gates pass for every affected consumer.
