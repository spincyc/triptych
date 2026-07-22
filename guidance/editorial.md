# Editorial Standard

## Governing priorities

Triptych is a source-first library of Catholic study documents. Apply these priorities in order:

1. identify the work, reader, governing authority, edition, locale, jurisdiction, and applicable profile;
2. verify the evidence needed for each consequential claim and preserve disagreement or uncertainty;
3. write the subject, argument, narrative, prayer, or usable guide before editorial apparatus;
4. move work-wide bounds, methods, and qualifications to terminal appendices while keeping claim-local caveats beside their claims;
5. audit rights, provenance, metadata, structure, and every rendered page before installation or release.

A genre profile may add stricter requirements but may not weaken this standard. Profiles are delta specifications: do not import another genre's template, repeat universal rules, or substitute layout conventions for source judgment. Define or revise a profile before multiplying a repeatable series for which none fits.

These publications aid study, prayerful understanding, and responsible research. They are not official liturgical books, critical editions, catechisms, magisterial acts, canonical opinions, or substitutes for competent pastoral or legal advice.

## Reader-first structure

After a title page and table of contents, if used, begin with substantive content. Do not make readers cross an evidence key, scope statement, chronology, terminology boundary, legal-assumptions block, or review disclaimer to reach the work.

Put work-wide controls in a terminal `Scope and Qualifications` appendix or the profile's equivalent. It owns:

- coverage, corpus, completeness, period, date, geography, language, rite, edition, jurisdiction, and as-of bounds;
- global terminology, evidence classes, method, source hierarchy, legal assumptions, and unresolved questions;
- global translation, rights, currentness, review, and use qualifications; and
- an orientation timeline when its chief purpose is to bound or navigate rather than advance the account.

Keep that appendix concise and linked from the contents. References contain bibliography and source-local role or rights notes, not a second statement of the global method. Generation metadata is the final content block, after references, and no exposition follows it. The common legal notice is a subordinate final-page colophon, not exposition, an appendix, or a separate section.

A thesis or governing question is substantive and may open the body. Operational facts needed at the point of use—such as the selected liturgical branch, recitation order, or applicable rule—stay there. A one-line title-page non-authority warning is permitted only for immediate reliance risk and must point to the terminal appendix rather than repeat it.

The appendix never absorbs a qualification that changes a particular claim. Keep disputed attribution, material uncertainty, branch dependence, jurisdictional difference, source status, and other local limits beside the affected claim.

## Evidence and claims

Keep these states distinct in research and publication:

- **verified source text** — wording checked in an identified primary edition or official witness;
- **checked quotation or paraphrase** — the published claim checked at an exact locus;
- **source-grounded synthesis** — an editorial conclusion demonstrably supported by checked evidence;
- **editorial or AI proposal** — an original application, analogy, extension, or hypothesis, labeled locally; and
- **unverified lead** — research-only material that cannot support a published claim.

Do not invent a fact, quotation, citation, source search, verification event, consensus, doctrine, or law. Do not turn resemblance into exegesis, discipline into doctrine, opinion into settled teaching, or plausible legal analysis into binding law. A global disclaimer never cures false attribution or overstatement.

Prefer primary, official, edition-identified, stable sources. OCR, searchable transcriptions, aggregations, quotation sites, and secondary citations are finding aids until the underlying witness is checked. Cite enough edition/version and locus information to reproduce the claim; record stable links and access dates where online evidence matters.

When an external source is registered for repository-wide reuse, follow
`guidance/sources.md`. Cataloging, acquiring, indexing, searching, inspecting,
and verifying are distinct states. Full-work availability never implies that a
publication examined the whole work, and a reusable source note never replaces
the publication's claim-level judgment.

Research is claim-driven, not quota-driven. Search broadly enough to test the governing claims, serious alternatives, and gaps; stop collecting sources that merely repeat a point. Preserve consequential negative results and disclose unresolved records rather than filling them by inference.

Do not introduce a weak, prejudicial, sensational, conspiratorial, or otherwise extraneous claim merely to reject it. If an argument is not needed to understand the work's subject, a retained source, or a material reception history, omit it from reader-facing prose and audit records instead of creating a corrective callout, disclaimer, or rejected-lead inventory. When an error or harmful reception is materially within scope, explain its evidentiary role and analyze it directly and proportionately.

Liturgical claims identify the rite, use or form, typical edition, calendar, language, translation, territory, and other variables needed to know what is appointed. Canon-law claims identify the body of law, jurisdiction, promulgating authority, effective or as-of date, amendments, authentic interpretations, and material particular law. Mutable discipline is never presented as timeless.

## Rights, quotation, and received prayer

Quote only what the argument requires. Record the known author, source, attribution, license, permission, public-domain basis, or legal exception at the nearest useful source record. Online availability, age, official status, and citation do not establish permission. Do not place complete scans, bulk OCR, or third-party corpora in publication leaves when a focused record and stable citation suffice. A lawful, reasonably sized source acquired for genuine repository-wide reuse may instead enter the provider-neutral source library under `guidance/sources.md`; acquisition alone does not justify quotation or publication use.

The repository license does not relicense Scripture, official or liturgical text, received prayers or hymns, third-party translations, quotations, images, fonts, or other external material. Put a local notice wherever excluded wording could reasonably be mistaken for project-owned expression.

Render the common reuse-and-rights notice once as a compact, legible colophon on the same physical final page as the terminal content. It must never force a rights-only page. Keep work-specific rights detail in the scope appendix, source record, or beside the affected material rather than enlarging or duplicating the common notice.

Every text offered for vocal prayer or ritual recitation must reproduce an identified historical, approved, liturgical, or otherwise received witness. Neither the project nor an AI contributor may compose, translate, paraphrase, modernize, conflate, or materially adapt such a text. Use an exact identified human translation with recorded status and rights; otherwise omit it. Expand an explicit abbreviation only from the same witness or a governing edition it incorporates, and record both loci. Commentary may explain a prayer but must remain visibly distinct and must not function as a substitute translation.

## Audit records and generation metadata

Keep enough tracked evidence to reproduce editorial judgments without publishing private reasoning or a search diary. The applicable profile defines filenames; collectively the records identify the question and material exclusions, governing editions, source roles and loci, substitutions, disagreements, consequential negative results, material unresolved leads, jurisdiction/currentness, rights, completed review, and outstanding review. Never record credentials, private reasoning, host or user identity, machine paths, network data, or session identifiers.

Every canonical publication keeps `generation-metadata.tex` beside `main.tex` and imports it exactly once at the terminal display point. Its first active declaration is one `\AIDocumentRevisionTimestamp{YYYY-MM-DDTHH:MM:SSZ}`, followed by one or more `\AIModelContribution` declarations. A profile may permit a prose-free mechanical companion to declare `\AIInheritedGenerationMetadata` from one named canonical source while displaying its own timestamp once.

The timestamp is the whole-second UTC time when the publishable render source was finalized. Update every affected consumer when render-relevant source or an imported fragment changes. Never derive it from Git, file metadata, build time, environment, or a content hash. Preserve every exposed model qualifier and client/runtime fact verbatim; name unavailable components specifically and never guess them. Separate contributions when model, qualifiers, or material runtime differ. Keep contributions using the same model and qualifiers adjacent: their shared model/configuration is displayed once, while every distinct agent/runtime record remains visible. Never repeat an exact contribution declaration.

The metadata gate rejects missing, duplicate, noninitial, malformed, or non-UTC timestamps; exact duplicate contribution declarations; generic family-only model labels; missing exposed qualifiers; invalid inheritance; handwritten display substitutes; missing PDF title/subject; PDF dates inconsistent with the tracked revision; automatic creation dates or trailer IDs; and omitted, duplicated, or reordered visible fields. It also requires one visible model/configuration line for each adjacent group sharing that identity, rather than repeating it for every contribution.

## Review and publication gate

Generation provenance, source audit, specialist review, theological or canonical review, production review, and exact-snapshot distribution approval are separate states. Use labels such as `source-audited` or `theologically reviewed` only when the corresponding event is recorded. Internal checking is not independent review; production quality is not ecclesiastical approval.

Typography serves navigation and meaning. Remove wrapper labels already supplied by the surrounding heading, but retain labels that convey authority, attribution, safety, contrast, accessibility, or stable semantic fields. Give repeated multi-field forms consistent visible field names. Do not use typography to imply doctrinal or juridical force.

Before installing a publication:

- verify the reader-first order, terminal apparatus, every material claim and citation, source/proposal boundaries, and absence of unused references or padding;
- confirm rights, attribution, edition, jurisdiction, as-of, review, and generation records describe the artifact;
- compile enough passes to settle contents and references; reject fatal errors, undefined references, overflow, and unresolved layout warnings;
- generate bounded review rasters with `make review-pdfs` or `scripts/pdf-review` and visually inspect every page, using full-size pages where contact-sheet scale is insufficient;
- check clipping, density, heading splits, tables, callouts, artificial whitespace, sparse spill pages, monochrome legibility, PDF structure, embedded fonts, metadata, and extracted text; confirm the final-page rights colophon is readable, unclipped, non-overlapping, and has not created a spill page; and
- install only the reviewed PDF at its mirrored `doc/` path, leaving intermediates under ignored `build/`.

Profile-specific gates remain mandatory.
