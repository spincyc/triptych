# Editorial Standard

## Purpose and scope

*Triptych: Catholic Studies in Faith, Worship, and Law* is a source-first library of study documents. Its collections may include liturgical preparation guides, expositions of liturgical ordinaries, theological reference works, and discursive articles on faith or canon law. This standard governs every collection. A genre or edition profile may add stricter requirements, but it may not weaken the common requirements below.

The documents are aids to study, prayerful understanding, and responsible research. They are not official liturgical books, critical editions, catechisms, magisterial acts, canonical opinions, or substitutes for competent pastoral or legal advice. State a more specific limitation when a document's subject or intended use makes one necessary.

## Profile before template

Identify a document's collection, genre, governing editions, jurisdiction, and intended reader before researching or drafting it. Then use the relevant profile linked from `AGENTS.md`. The profile governs matters such as required sections, source records, catalog identifiers, page architecture, liturgical elements, and review gates.

Do not apply one genre's structure by analogy to another. In particular:

- a proper guide may require a complete formulary map and facsimile collation;
- an ordinary exposition requires an edition-identified order of worship and must distinguish invariant text from rubrical or selectable material;
- a theological reference work may need a title page, table of contents, lexicon, or reusable appendices;
- a discursive article should use an argument appropriate to its question rather than a liturgical page template;
- a canon-law article must identify its legal system, jurisdiction, sources, and effective date and must account for later amendments and authentic interpretations.

When no suitable profile exists, define and review one before creating a repeatable document series. A one-off work may record its local structure in its research scope, provided it still satisfies this common standard.

## Authority and claim discipline

Keep these classes visibly distinguishable in research and publication:

- **Verified source text:** wording checked in the identified primary edition or official witness.
- **Checked quotation or paraphrase:** a claim verified at an exact locus in an identified source.
- **Source-grounded synthesis:** an editorial conclusion demonstrably supported by the verified evidence.
- **Editorial or AI proposal:** an original analogy, extension, hypothesis, or application not established by the cited authorities.
- **Unverified lead:** a proposed source or connection that remains research-only and cannot support a published claim or appear as though it were used.

Do not turn thematic resemblance into direct exegesis, disciplinary practice into doctrine, a theological opinion into settled teaching, or a plausible legal reading into binding law. Attribute disagreement and uncertainty at the claim they affect. Never invent a quotation, citation, historical fact, legal rule, consensus, source search, or verification event.

Original proposals may be useful, but their editorial boundary must be unmistakable. A profile may prescribe a dedicated speculative section; otherwise label the proposal locally. A global notice does not excuse false attribution or contradiction of established text, doctrine, or law.

## Sources and verification

Prefer primary, official, edition-identified, and stable sources. Use searchable texts, OCR, aggregations, quotation sites, and secondary citations as finding aids until the underlying source is checked. Cite the exact work, edition or version, and locus needed to reproduce the claim. Record stable links and access dates when online evidence is material.

Source selection is claim-driven rather than quota-driven. Search broadly enough to test the governing claims, preserve serious alternatives, and disclose material limits; stop accumulating sources that merely repeat the same point. A profile may require dedicated retrieval, verification, or research records. Those records are tracked editorial sources, not disposable build artifacts.

For liturgical material, identify the rite, form or use, typical edition, calendar, language, translation, territory, and other variables needed to know which text is appointed. For canon law, identify the applicable code or body of law, jurisdiction, promulgating authority, effective or as-of date, amendments, and any material particular law. Do not describe mutable law or current liturgical discipline as timeless.

Keep quotations no longer than the argument requires. Observe copyright and source-site terms; the ability to retrieve a text does not establish permission to republish it. Do not vendor complete third-party scans, corpora, or bulk OCR when a focused source record and stable citation are sufficient.

## Research record

Preserve enough of the evidence state to make the work auditable without publishing private reasoning or a diary of searches. A research scope should record, as relevant:

- the question, included and excluded material, and governing editions;
- primary and secondary corpora consulted;
- source roles and exact loci;
- material disagreements, uncertainties, substitutions, and unresolved issues;
- consequential negative results and rejected or unverified leads;
- the document's jurisdiction and as-of date when the subject can change;
- review performed and review still outstanding.

Machine-specific paths, hostnames, network addresses, credentials, tokens, session identifiers, and private chain-of-thought do not belong in source records or published metadata.

## AI generation metadata

Every AI-generated or substantially AI-revised document records the final generation event once. Placement belongs to the document profile. A profile may designate a mechanically derived companion as inheriting the named canonical source’s provenance only when the companion contains no independent generated prose and the catalog makes that relationship explicit. Use the compact form unless a profile requires additional fields:

```text
Generated: YYYY-MM-DD
Model: exact exposed model identifier; qualifier=value; unexposed: specifically unavailable model details
Agent/runtime: product and material role(s); exposed client/build version; interface; unexposed: specifically unavailable runtime details
```

Preserve the complete model label and every exposed qualifier verbatim. Label client versions as client versions, not model or server versions. Group contributors that share the same model and runtime; distinguish contributors only when material metadata differs. Never guess an unavailable identifier or include identifying machine information. Refresh the metadata when a document is substantially revised or finally regenerated in a different environment.

Store provenance in `generation-metadata.tex` beside each canonical `main.tex`, using the shared `\AIGenerationDate` and `\AIModelContribution` commands, and import that record exactly once at the profile-appointed display location. A mechanically derived companion instead stores and imports one `\AIInheritedGenerationMetadata` declaration naming its canonical source. Do not handwrite display fields in `main.tex`, substitute build-time environment values for historical provenance, or let a later generic family label overwrite an exact identifier or qualifier already known. When materially contributing agents differ in model, qualifier set, or runtime, retain separate contribution records within the one displayed provenance block.

The metadata gate is a publication requirement. It must reject a missing or duplicate record, a generic family-only model label, an empty or malformed qualifier field, omission of a qualifier known to be exposed by a recorded model, an invalid inheritance target, legacy handwritten fields, absent PDF title or subject metadata, and a rendered PDF that omits or reorders a structured field. A validator cannot discover a fact the runtime did not expose; record a specifically named unavailable component rather than inventing it, but never mark an exposed value unavailable.

## Editorial maturity and review

Do not collapse generation provenance, source evaluation, theological review, legal review, and production quality into one maturity claim. A document may be well typeset and still await source or expert review. Catalog status must report these dimensions separately using the definitions in the applicable profile.

Use calibrated language such as `working draft`, `source-audited`, `theologically reviewed`, or `canonically reviewed` only when the corresponding event is recorded. Internal source checking is not independent theological or canonical review. The absence of review must remain visible where readers could otherwise infer it.

## Publication quality

### Typographic hierarchy and visible labels

Let typography carry hierarchy without narrating its own devices. When a surrounding heading and the fields inside a callout already identify its function, use an untitled frame rather than adding a generic wrapper such as `Dogmatic object and boundary`, `Dossier boundary`, `The day's axis`, or `Compact source panel`. A repeated meta-label is not made useful merely because its wording is accurate.

When a repeated callout divides its content into two or more stable semantic fields, give every field a concise visible identifier and use the same identifiers in every instance. A container title, fixed field order, paragraph break, change of type style, column position, or border does not substitute for those field identifiers; the container itself may remain untitled when its function is already clear. This rule applies to macro arguments and other source-level sections, not merely to visibly separated paragraphs. Do not manufacture field labels for continuous prose or treat every bullet or paragraph as a separate field.

Retain a visible title when it contributes information that line weight, position, and field labels cannot convey: an exact authority or ecclesial status, a content-bearing thesis, a safety warning, a contrast such as `Do not confuse`, a source attribution, or a copyright and approval notice. Table headers and local labels that distinguish materially different claims remain necessary. Typography may mark importance or relationship, but it must never be treated as establishing doctrinal authority, source status, or juridical force by itself.

During the final visual edit, scan headings, callouts, table headers, legends, and repeated dossier forms independently of the body prose. Remove labels duplicated by the immediately surrounding structure, while preserving every label needed for navigation, accessibility, authority classification, or safe interpretation.

Before installing a publishable artifact:

- verify every material quotation, attribution, factual assertion, and cited locus;
- distinguish inherited teaching, historical judgment, editorial synthesis, and original proposal;
- remove duplication, padding, unsupported links, and unused references;
- confirm that headings, tables, diagrams, and callouts clarify the argument at ordinary print size;
- keep visual distinctions intelligible in monochrome unless a profile explicitly requires color;
- compile for the number of passes required to resolve references and contents;
- inspect the build log for fatal errors, undefined references, overflow, and layout warnings;
- visually inspect every page for clipping, unreadable density, split headings, artificial whitespace, and sparse spill pages;
- confirm that generation metadata and any edition, jurisdiction, or as-of statement describe the installed artifact;
- install the reviewed PDF under the mirrored `doc/` path and keep all intermediates under `build/`.

Profile-specific acceptance criteria remain mandatory in addition to this list.
