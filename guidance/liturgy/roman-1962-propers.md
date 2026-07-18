# Roman Missal 1962 Proper-Guide Profile

This profile governs source-first guides to temporal, ritual, votive, and other proper formularies in the 1962 *Missale Romanum*. It does not govern calendar assembly, the Ordinary or Order of Mass, postconciliar propers, standalone theological references, or discursive articles. Use `guidance/liturgy/roman-1962-assembly.md` for edition-specific assembly and calendar questions. Universal evidence, metadata, review, rights, and publication rules remain in `guidance/editorial.md`; repository paths and build rules remain in `guidance/repository.md`.

Each guide is a hand-missal companion, not an official liturgical text, critical edition, homily, or substitute for the cited sources. It should help a reader perceive the appointed texts as one ordered liturgical action while keeping verified text, documented history and reception, editorial synthesis, and exploratory proposal distinct.

## Collection Identity

- The temporal series uses 52 Sunday identities in a stable Lent-first repository order: `01` is the First Sunday of Lent and `52` is Quinquagesima. These IDs are catalog identities, not the occurrence schedule of a civil year.
- `46R` through `49R` identify the resumed Third through Sixth Sundays after Epiphany. Each is a separately sourced formulary variant under its shared ordinal because it combines the relevant Epiphany orations, Epistle, and Gospel with the chants appointed for resumed use after Pentecost.
- `F` identifies a general-calendar feast assigned to Sunday without a stable temporal ordinal. Verify its printed place and occurrence rule; do not invent a permanent Sunday number for a fixed-date, movable, or local feast.
- `M` identifies a ritual, votive, or other non-Sunday guide. The prefix does not state rank, permission, or authority to replace an occurring Mass.
- Identify every work by the 1962 edition, printed formulary heading and rank, place in the book, and governing occurrence or use rule—not by filename or a modern civil date. Do not merge distinct formularies. Record seasonal substitutions, ritual additions, blessings, or alternate conclusions wherever they govern the guide.

## Source Records and Text Control

Each guide leaf keeps its source and audit records beside `main.tex`:

```text
propers/retrieved.txt
propers/verified.md
research/scope.md
```

- `retrieved.txt` preserves a focused machine-readable pull, including OCR errors and enough boundary text to identify the formulary. It is an unedited finding aid, not publication text.
- `verified.md` preserves the facsimile-collated appointed text in liturgical order, including seasonal and ritual variants. Its provenance identifies the missal edition; printed heading and rank; retrieval URL, source identifier, and date; printed pages and digital leaves; checksum when available; facsimile URL; verification status and date; and unresolved discrepancies.
- `research/scope.md` records the sources, languages and corpora searched; claim roles; material negative results; rejected or unresolved leads; competing historical judgments; and operational qualifications displaced from the PDF. It is an audit record, not a diary.

Use the following public witnesses unless a better edition-identified witness is documented:

1. The CMAA [1962 *Missale Romanum* facsimile](https://media.churchmusicassociation.org/pdf/missale62.pdf) controls Latin text, rubrics, rank, references, and formulary boundaries. Cite the printed missal page, not only the digital page.
2. The Internet Archive [full-text OCR](https://archive.org/download/MissaleRomanum1962RomanMissalColorLatin/Missale-Romanum-1962-Roman-Missal-color-latin_djvu.txt) locates headings and passages but never controls published wording.
3. The Internet Archive [image item](https://archive.org/details/MissaleRomanum1962RomanMissalColorLatin) is a secondary image witness for unclear readings. OCR and images derived from one item are not independent witnesses.

Visually collate every published Latin form, rubric, citation, and boundary against the controlling facsimile. Check an unclear reading against a second image witness; disclose substitutions and disagreements; never silently blend witnesses. Keep only focused extracts in the repository. Psalm citations use the missal's Vulgate/Septuagint numbering first, with the common modern number in parentheses where it differs.

Study every appointed text in full and read each direct biblical passage in its complete literary context. Every appointed element must contribute to the guide; add, substitute, or locally define cues for Tracts, Sequences, ritual prayers, blessings, and other actual texts rather than forcing a ten-row Sunday template.

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
2. `The Propers: Themes and Movement`
3. `The Propers: Detailed Commentary`
4. `The Propers: Interpretive Possibilities`
5. `Sacramental Appendix` when required
6. `Appendix: Scriptural and Historical Coordinates`
7. `Appendix: Scope and Qualifications`
8. `References`
9. `Generation Metadata`

Do not front-load a chronology, historical dossier, status panel, research boundary, date range, source survey, or general qualification. Put work-wide bounds and qualifications in the terminal appendices so the reader reaches the proper's argument immediately. Keep a qualification beside a claim only when it materially changes that claim.

### Page 1: Propers map and four senses

Map every actual appointed element in liturgical order. For an ordinary Sunday this normally means Introit, Collect, Epistle, Gradual, Alleluia or Tract, Gospel, Offertory, Secret, Communion, and Postcommunion; include a Sequence or ritual text when appointed. The map presents the proper, its incipit or reference, its scriptural or grammatical axis, and a concise demonstrable connection.

Immediately follow it with exactly four rows: **Literal**, **Allegorical**, **Moral**, and **Anagogical**. Ground each synthesis in appointed text or documented reception. Page 1 contains no work-wide historical, geographic, chronological, search, rights, or review apparatus.

Later proper-focused headings may use quiet parenthetical cues in liturgical order: *Int.*, *Coll.*, *Ep.*, *Grad.*, *All.* or *Tr.*, *Seq.*, *Gosp.*, *Off.*, *Sec.*, *Comm.*, and *Postcomm.* Define additional ritual cues locally.

### Themes, commentary, and exploration

`The Propers: Themes and Movement` immediately follows page 1 and occupies two readable pages. Open with a one- or two-sentence thesis and, when useful, one orienting form of no more than four primary stages. Use three to five functional units that account for every appointed element and let a signpost-only scan recover the thesis, movement, decisive evidence, and principal limits. This section contains only source-grounded claims.

`The Propers: Detailed Commentary` supplies the exegesis, textual comparison, reception, doctrinal distinctions, disagreement, and claim-local qualifications that prove and refine the synthesis. Give each substantial claim one fullest home; remove repeated quotations, recaps, thin subsections, and stretched links.

`The Propers: Interpretive Possibilities` begins with one compact notice identifying its contents as exploratory editorial or AI proposals, not sourced historical intent or attributed teaching. It has no required number or length. It may state that no responsible proposal is offered. Proposals must remain textually anchored, theologically plausible, aware of serious alternatives, and free of invented facts, quotations, or attributions.

### Sacramental appendix

When a ritual Mass is celebrated with or specifically for a non-Eucharistic sacrament, import the relevant canonical one-page summary from `src/gpt/theology/sacraments/summaries/` after `The Propers: Interpretive Possibilities`. Use the full sacramental treatise and its sources for research; the summary is a retrieval aid, not the research ceiling. Do not infer historical formulary intent from general sacramental theology without a source.

## Terminal Apparatus

### Appendix: Scriptural and Historical Coordinates

Inventory every distinct directly appointed biblical passage once, in Catholic canonical order and then verse order; consolidate repetitions and do not mislabel loose echoes in composed orations as direct quotations. Use the columns `Proper`, `Citation`, `Location`, and `Date`. The citation cell does not reproduce Scripture.

For each passage, distinguish traditional attribution from historical judgment and give the author or compositional horizon, first audience, composition place and date or range, relevant life stage, and place in Israel's and salvation history. A Gospel dossier separately identifies the narrated event's locating citations, place, and approximate date so composition and event are not conflated. Distinguish writer, event, and recipient geography; give present-day equivalents where useful; state uncertainty and responsible alternatives. Put these chronological, geographic, and historical bounds here rather than before the guide's argument.

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
- every direct biblical passage has complete-context research and one historically qualified terminal dossier, with composition, narrated event, audience, geography, chronology, tradition, and modern judgment kept distinct;
- every attribution and historical, doctrinal, or reception claim has an exact source and locus, while source-grounded synthesis and exploratory proposal remain visibly distinct;
- the guide follows the fixed reader order, reaches its argument on page 1, and places work-wide bounds, date ranges, source limits, rights, review status, and qualifications only in the terminal apparatus;
- a required sacramental summary is imported from the canonical fragment, `References` contains only used sources, and generation metadata is accurate and terminal; and
- the universal editorial, rights, build, warning, visual-review, installation, and publication gates pass for every affected consumer.
