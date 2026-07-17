# Historical Accounts

## Scope and collection

This profile governs repeatable, source-first historical monographs whose principal task is to reconstruct the development, transmission, and reception of a text, institution, practice, event, or movement. Historical accounts belong beneath `src/gpt/history/<series>/<numbered-document>/`; another provider uses the same taxonomy beneath its own provider directory. They have one catalog home on `library/historical-accounts.md` and do not become faith, liturgy, or law publications merely because those fields occur in the history.

Use another profile when the governing task is doctrinal exposition, a liturgical formulary or Order of Mass, current canon law, a devotional guide, or ecclesial judgment of a claimed apparition. A historical account may contain bounded theological, liturgical, or canonical modules, but it must name the additional profile or source rules that govern those modules and must not let a historical practice establish present doctrine or law by itself.

Series directories and reader-facing identifiers are stable. Use a descriptive lowercase series slug and a two-digit ordinal in each publication leaf, such as `history/biblical-translations/01-septuagint`. The matching catalog identifier combines a short series prefix and that ordinal, such as `BT-01`. An ordinal records series order, not a claim about importance or chronology.

## Historical identity and question

Before research, record the subject, period, geography, communities, languages, institutions, intended reader, governing question, and terminal date. When the subject is a translation or edition, also identify:

- the source language and recoverable source-text families;
- the target language and historically relevant registers;
- whether the familiar title names one act, several translations, a revision, a corpus, or a later edition;
- named and anonymous translators, revisers, patrons, and transmitting communities, with their status qualified;
- the manuscripts, artifacts, editions, or institutional acts that define the account's principal stages; and
- later uses of the title that must not be projected backward.

The opening of the publication states a governing thesis and begins the historical account. It must tell the reader when a conventional one-event story has to be replaced by a history of several acts, books, recensions, or communities, but the work-wide limits of what the surviving evidence can prove belong in the terminal apparatus. A qualification that changes a particular historical claim remains beside that claim.

## Evidence and historiography

Build the account from distinguishable layers of evidence:

1. **Contemporary or near-contemporary evidence:** manuscripts, papyri, inscriptions, colophons, correspondence, prefaces, official acts, and securely dated material objects.
2. **Ancient or medieval narrative witness:** what a named author says, at the author's date and for the author's purpose. A witness to reception is not automatically an eyewitness to origins.
3. **Later institutional memory and reception:** liturgical, conciliar, papal, scholarly, confessional, or popular claims that establish how the past was received, even when they cannot independently establish the originating event.
4. **Modern historical reconstruction:** critical editions and professional scholarship used to date, compare, and interpret the earlier evidence. Record live disagreements and avoid manufacturing a consensus.

For each important origin story, separate the narrative's exact claim, its earliest extant form, later amplifications, corroborated historical core, and elements that remain literary, legendary, disputed, or unrecoverable. Do not dismiss a tradition merely because it contains literary shaping; do not call literary coherence corroboration.

Textual history is book- and witness-specific. A difference between versions may arise from a different source text, translation technique, exegesis, revision, harmonization, scribal change, or editorial reconstruction. Do not choose among those explanations without evidence. Avoid phrases such as “the original text” when the claim actually concerns an earliest recoverable form, a translator's source text, a critical edition, or one manuscript family.

Official ecclesiastical sources establish the act, status, or reception they actually express. They do not replace historical or text-critical evidence for earlier centuries. Conversely, modern historical scholarship does not determine a source's theological or juridical authority.

## Required source records

Every publication leaf contains:

- `main.tex` and `generation-metadata.tex`;
- a `sections/` directory organized by the account's actual argument;
- `research/scope.md`, recording identity, included and excluded periods, terminology, source boundary, material uncertainties, rights review, and review state;
- `research/source-audit.md`, giving exact bibliographic metadata, stable links and access dates for online evidence, source roles, loci actually checked, and unused or unverified leads; and
- `research/evidence-map.md`, aligning the principal chronological or interpretive claims with their evidence class, exact witness, degree of confidence, and material qualification.

These are editorial records, not a search diary. A catalog entry links the three reader-facing research records separately. Focused extracts may be retained only when necessary and lawful; complete third-party books, scans, or OCR corpora are not document assets.

Treat an evidentiary gap as a research task, not a decorative disclaimer. For every principal claim supported only by a late, secondary, hostile, or uncertain witness, search the reasonably accessible primary, official, manuscript-catalog, critical-edition, and professional-scholarly record that could materially improve it. Record the source families checked, consequential negative result, and remaining gap in `source-audit.md` or `evidence-map.md`; do not add repetitive search narration to the publication.

## Publication architecture

Each account includes a title page, a table of contents, and then the governing thesis and substantive history. It does not front-load structured provenance, study limitations, an evidence key, or a method chapter. The reader-facing order ordinarily includes:

- a concise governing question or thesis followed immediately by the political, linguistic, material, and religious setting;
- the origin evidence and its historiographical limits;
- a periodized account of production, revision, transmission, and reception;
- representative textual or material case studies that test the larger account;
- corrections to misleading shorthand integrated where the relevant evidence is discussed rather than collected in an opening claim audit;
- a conclusion that answers the governing question;
- a terminal `Scope, Method, and Historical Coordinates` appendix containing the subject and corpus boundary, included and excluded periods, geographic and linguistic bounds, terminology, evidence classes, source hierarchy, method, terminal or as-of date, global uncertainties, rights and review limits;
- a dated timeline appendix that distinguishes event, witness, edition, and later judgment;
- references grouped by source function; and
- terminal structured generation metadata.

This list is a coverage rule, not a fixed set of section titles. The apparatus and timeline may be separate appendices or adjacent parts of one appendix block, but neither is repeated before the narrative. Tables and timelines must remain readable at ordinary print size, and the narrative must explain rather than merely duplicate them. Dates and qualifications that are facts of the narrative remain where they are needed; the appendix owns the work-wide range and framing rules.

## Translation, quotation, and rights

Do not create a project translation of ancient, biblical, liturgical, or official text for display. Quote only an identified human translation whose edition and rights basis are recorded, or paraphrase the claim with an exact locus. A public-domain translation may be used sparingly, with its translator and edition named; public-domain status is not inferred from age alone. Modern translations and scholarship are summarized rather than reproduced except for short, necessary quotations.

The local scope and source audit identify all third-party quotations, manuscript images, facsimiles, and edition-specific wording. A work without incorporated images should say so. The standard detached-publication rights notice remains mandatory.

## Status and completion gate

Catalog language keeps four dimensions separate: internal source audit, independent historical or text-critical review, any additional theological or canonical review, and production inspection. “Source-audited” requires the completed records above and exact checking of the claims used in publication; it does not imply independent specialist review.

Before installation:

- confirm that the familiar title and series identifier are used consistently;
- test every major chronological claim against the evidence map;
- distinguish contemporaneous evidence, retrospective narrative, reception, and modern reconstruction at the claim affected;
- verify dates, names, manuscript or edition identifiers, quotations, and cited loci;
- preserve material disputes, negative results, and book-specific variation;
- confirm that the substantive history begins immediately after the title and contents and that work-wide bounds, method, evidence key, timeline, currentness, and limitations occur only in the terminal appendix block;
- pursue and record material source gaps rather than leaving reasonably searchable primary or official evidence unchecked;
- complete quotation and link-rights review;
- run the universal metadata and publication checks, including terminal provenance;
- inspect the build log and every rendered page; and
- install the reviewed PDF at its exact mirrored `doc/gpt/history/` path.

Independent specialist review remains explicitly outstanding until a named review event is recorded.
