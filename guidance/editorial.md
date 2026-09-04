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

## No side in what is described

The library documents what was and what is. Where the Church has spoken, the act
stands as it stands: this project records it, dates it, cites it, and does not
grade it. It carries no position on whether a reform was an improvement, whether
one recension is preferable to another, or which of two lawful uses a reader
should prefer — and it does not arrive at one by implication, through the order
things are listed in, the adjectives attached to them, or the terms chosen to
name them.

This is a constraint on the writing, not a reticence about the facts. Say plainly
what a revision changed, what it removed, what it left, and what was said about
it at the time, with the sources. A reader who wants to judge is owed the
evidence to judge with; they are not owed our judgement wearing the costume of a
finding.

What the rule constrains is comparison: between rites, recensions, editions,
uses, and reforms, where the library takes no position on which is better. It
is not a posture of neutrality toward the Catholic reading of Scripture, and it
never asks a writer to stand outside the tradition to describe it. The next
section owns that question.

Three practical consequences, each of which has already decided a question here:

- **Naming is where partisanship enters first.** Terms in live polemical use —
  "Novus Ordo", "Traditional Latin Mass", "Extraordinary Form", "Ordinary Form" —
  are not used to label a thing in the apparatus, because a control a reader
  cannot argue with should not take a side. Name a book by its own title and
  date: "1962 Missal", "Postconciliar Missal".

  The rule governs what the apparatus **calls** a thing: headings, titles,
  labels, controls, and prose in our own voice. It does not forbid *reporting*
  that a term is in use — "these books are widely called the *Novus Ordo*" is
  documenting what is, which the paragraph above requires. Two `library/` pages
  carried the polemical terms as their headings while the portal that links them
  already used the neutral names; on 2026-08-01 the headings were corrected to
  match the portal and each page now names the common term once as usage.

  **Their filenames were not changed, and that is the rule's limit.**
  `library/novus-ordo-liturgy.md` and `library/traditional-latin-mass.md` are
  published URLs, bound by hash into the release record and named by some thirty
  publication records. A path already published is a reference other people
  hold, and breaking it to satisfy a naming rule trades a label nobody misreads
  for a 404 — which this repository did to Catena Omnia the same day and had to
  undo. A path is not a claim; a heading is. Rename the heading.
- **A structural choice is not an editorial one.** The pre-1955 book is the base
  of `recensions.md` because it came first and a descendant cannot derive its
  ancestor. That is chronology, and it implies nothing about merit.
- **Where the sources disagree, carry the disagreement.** Preserving it is
  already required above; the point here is that a dispute is not resolved by
  choosing the side the writer finds congenial and omitting the other.

Public-alpha publication has six concerns: source integrity, rights and lawful
distribution, safety, reproducibility and artifact identity, mechanical
validity, and basic visual usability. A publication that satisfies those
concerns may enter the alpha without a specialist, clerical, intended-reader,
physical-use, or ecclesiastical review process. Do not create deferred gates,
pending-review placeholders, or repeated qualifications for reviews that are
not part of the current workflow. Any future external-review system is a
separate project and confers no status until that system is deliberately
defined and a completed event is recorded.

## Speaking from within the tradition

Scripture, liturgy, doctrine, patristic reception, typology, and saintly
interpretation are presented from within the Catholic tradition that produced
them, not from a stance outside it. The governing voice is Catholic,
affirmative, tradition-inhabiting, source-disciplined, and historically
responsible: it explains an inherited reading in the theological grammar that
reading uses, and attributes it to the witness who taught it. Modern
skepticism is not the neutral default that a theological claim must be
translated into before it can be written down.

Write "The Fathers read", "Augustine identifies", "the liturgy presents", "the
Church receives", "the traditional reading sees", "the typology joins", with
source attribution where the claim needs it. Do not write "later Christians
believed", "a devotional reading might see", "the Fathers understandably
interpreted", "although tradition claimed", "the Church came to read this as",
or "from a modern perspective this is problematic" where straightforward
attribution says the same thing. Those forms hold an inherited interpretation
at arm's length by their grammar, whatever the sentence goes on to concede.
Do not apologise for typology, doctrine, sacramental interpretation, or
saintly reception merely because they are theological.

Three things this rule does not touch, each of them already required by the
evidence standard below:

- **Historical-critical fact.** Modern critical judgement may qualify
  authorship, dating, textual history, historical setting, manuscript
  evidence, and any other factual claim; where a profile requires both a
  traditional attribution and a modern critical horizon, report both
  accurately and tersely. What it may not become is the hermeneutical judge of
  Catholic theological interpretation. A date is a fact about a text, not a
  verdict on how the Church reads it.
- **Genuine disagreement.** Where Catholic or historical sources actually
  disagree, the disagreement is reported and attributed to the sources that
  hold it. Unanimity is never manufactured, and a dispute is not resolved by
  omitting the inconvenient side.
- **Cultural afterlife.** Secular, ironic, political, literary, hostile, or
  contesting reuse of scriptural wording is a historical fact about that
  wording, and belongs wherever a profile provides for it. It is documented
  rather than purged for being secular, and it is not the governing
  interpretive voice of the work.

When a sentence is doubtful, look at its grammatical subject. A qualifying
sentence is legitimate when its subject is a source, a text, a witness, or a
fact: "Augustine's lemma is not the chant's", "the psalm's modern critical
date is later than the traditional one", "Theodoret answers differently".
The same sentence is the defect when its subject is the guide, the reading, or
an evidence class: "this guide does not press the typology", "the reading is
documented reception, not a replacement for the literal sense". The first
tells the reader something about the material; the second tells the reader
something about the writer.

## Reader-first structure

After a title page and table of contents, if used, begin with substantive content. Do not make readers cross an evidence key, scope statement, chronology, terminology boundary, legal-assumptions block, or review disclaimer to reach the work.

Put work-wide controls in a terminal `Scope and Qualifications` appendix or the profile's equivalent. It owns:

- coverage, corpus, completeness, period, date, geography, language, rite, edition, jurisdiction, and as-of bounds;
- global terminology, evidence classes, method, source hierarchy, legal assumptions, and unresolved questions;
- global translation, rights, currentness, review, and use qualifications; and
- an orientation timeline when its chief purpose is to bound or navigate rather than advance the account.

Keep that appendix concise and linked from the contents. References contain bibliography and source-local role or rights notes, not a second statement of the global method. Generation metadata is the final content block, after references, and no exposition follows it. The common legal notice is a subordinate final-page colophon, not exposition, an appendix, or a separate section.

A work states its present scope, completion limits, review facts, and
non-approval or reliance qualifications directly in that terminal appendix.
Internal release and distribution states such as `alpha`, `hold`, `review`,
and `published` are not reader-facing content: do not print them on title
pages, in running matter, in explanatory prose, in catalogs, or in web-edition
banners. Production review uses the same reader-facing composition intended
for publication, without a temporary status mark that must later be removed.

A thesis or governing question is substantive and may open the body. Operational facts needed at the point of use—such as the selected liturgical branch, recitation order, or applicable rule—stay there. Safety warnings and legally necessary notices remain immediately visible wherever delayed notice could expose a reader to harm or materially misstate the law; this terminal-apparatus rule never displaces them. A one-line title-page non-authority warning is permitted only for immediate reliance risk and must point to the terminal appendix rather than repeat it.

The appendix never absorbs a qualification that changes a particular claim. Keep disputed attribution, material uncertainty, branch dependence, jurisdictional difference, source status, and other local limits beside the affected claim.

## State the finding, not the process that produced it

Reader-facing prose presents conclusions, arguments, interpretations,
evidence, and the qualifications a claim needs in order to be accurate. It
does not narrate the editorial principles behind those conclusions, the
methodological restraint exercised, the reason one emphasis was preferred to
another, the internal decision rules followed, the research process
undertaken, the interpretive policy applied, the boundaries of the production
workflow, or why the writer is entitled to make the claim at all.

Write "The Introit establishes exile as the formulary's opening condition" and
"Augustine reads the psalm as the cry of the pilgrim Church". Do not write "It
is important to distinguish", "The guiding principle here is",
"Methodologically, this section", "We have chosen to emphasize", or "This
interpretation should be approached cautiously because", unless a local
qualification is genuinely required to make the claim accurate.

The carve-out is the paragraph above: a qualification that materially changes
the truth of a local claim stays beside that claim, briefly. Everything else —
method, search bounds, evidence classes, corpora checked, negative results,
and the reasoning that produced an editorial judgement — belongs in the
terminal apparatus and in the profile's audit records. A work whose prose
repeatedly explains its own caution machinery has moved the appendix into the
body.

Naming the discipline is itself the defect. Prose that says a difference was
retained rather than silently harmonised, that a negative result is bounded
and correctable, that a reading is documented reception rather than a
replacement for the literal sense, or that an observation does not prove a
compiler's intention, is narrating compliance where it should simply be
compliant. Carry the difference and attribute it; state the negative result;
attribute the reception; claim no intention. A constraint on what may be
asserted is satisfied by not asserting it, never by disclaiming it in the
reader's hearing.

The desired movement is research thoroughly, qualify internally, and then
state the resulting conclusion directly. It is never research less and assert
more: this rule governs how a finding is written, and weakens no requirement
about how it was found.

### A screen finds some of this, and judgement is still yours

`tools/tpt check-content-preflight --check house-voice` reads a proper leaf's
reader-facing sections and refuses the forms of this defect that are lexically
marked: retrieval mechanics and checksums in the body, the guide's own pages
and apparatus as a grammatical subject, the source library or this repository
as one, a count labelled rather than stated, and the harmonisation and
evidence-class disclaimers this section names. It masks what the rule protects
— `References`, `Appendix: Scope and Qualifications`, the page-2 sheet, and the
exploratory notice and limit fields of the proposals — because a screen that
refuses those would be enforcing the opposite of the rule.

Two things follow, and the second matters more.

It is partial by construction. A sentence whose subject is the guide without
naming it, an instruction addressed to a future writer, and the hypothetical
guide of "a guide reporting only that would have flattened" all pass it. A
leaf the screen accepts has not been found compliant; it has been found to
carry none of the forms the screen knows.

And what it reports is a sentence to rewrite, never a sentence to delete. Every
difference, negative result, bound and attribution stands after the repair —
this rule is satisfied by changing the grammatical subject, and is never
satisfied by dropping what the sentence was about. A length heuristic tried
against the Latin bodies once ended with a worker deleting `es`, `Da`, `O` and
`qui` from a prayer, which is why `scripts/_latin_body_damage.py` carries its
false positives in its tests and why this screen carries a negative corpus in
`tools/tests/test_house_voice.py`. Add a rule to it only with the prose it must
not refuse.

## Illustration and page composition

When a publication uses illustrations, compose each page or spread as one
designed visual field rather than a sequence of repeated image cards. Vary
scale, crop, placement, grouping, and the relationship of image to text
according to the subject while preserving a clear reading order, accurate
identification, accessible labels, and legibility at the intended print size.
An asymmetric, overlapping, inset, marginal, or other heterodox layout is
welcome when it strengthens discovery or comparison; visual novelty never
excuses ambiguity, clipping, crowding, or decorative padding.

Integrate unframed artwork into the page ground. Use transparency or a
background matched to the publication stock, and remove crop rectangles,
mismatched whites, scanning halos, corner discoloration, and hard tonal edges.
Retain a visible image boundary only as an intentional frame, facsimile, or
full-bleed treatment with a clear editorial purpose. Review illustrated pages
at full size and under enough contrast to expose seams and floating
rectangles.

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
`guidance/sources.md`, which owns the evidence states and their exact names —
cataloged, acquired, indexable, searched, inspected, verified — and reserves and
rejects `indexed`. Those are machine-readable source-library states; the five
editorial classes above are prose distinctions, and the two vocabularies share
the word "verified" without sharing its meaning. Full-work availability never implies that a
publication examined the whole work, and a reusable source note never replaces
the publication's claim-level judgment.

Research is claim-driven, not quota-driven. Search broadly enough to test the governing claims, serious alternatives, and gaps; stop collecting sources that merely repeat a point. Preserve consequential negative results and disclose unresolved records rather than filling them by inference.

Missing, incomplete, or unbound evidence is a research signal, not by itself a
reason to narrow or remove a material claim. Before materially narrowing,
removing, or recasting a claim because support has not been found, perform and
record a second research pass directed at the expected primary, official,
critical-edition, catalog, and specialist source families for that claim.
Recheck likely variant terminology, languages, edition numbering, and
transmission or jurisdictional boundaries. The audit record must name the
families and loci pursued, distinguish unavailable or unchecked evidence from a
bounded negative result, and state what the second pass changed. Rights,
privacy, safety, relevance, and demonstrated falsity may independently require
removal; record that distinct reason rather than describing it as absent
evidence. After a proportionate second pass, narrow or remove a claim that
remains unsupported rather than preserving it by speculation.

Do not introduce a weak, prejudicial, sensational, conspiratorial, or otherwise extraneous claim merely to reject it. If an argument is not needed to understand the work's subject, a retained source, or a material reception history, omit it from reader-facing prose and audit records instead of creating a corrective callout, disclaimer, or rejected-lead inventory. When an error or harmful reception is materially within scope, explain its evidentiary role and analyze it directly and proportionately.

Liturgical claims identify the rite, use or form, typical edition, calendar, language, translation, territory, and other variables needed to know what is appointed. Canon-law claims identify the body of law, jurisdiction, promulgating authority, effective or as-of date, amendments, authentic interpretations, and material particular law. Mutable discipline is never presented as timeless.

## Rights, quotation, and received prayer

Quote only what the argument requires. Record the known author, source, attribution, license, permission, public-domain basis, or legal exception at the nearest useful source record. Online availability, age, official status, and citation do not establish permission. Do not place complete scans, bulk OCR, or third-party corpora in publication leaves when a focused record and stable citation suffice. A lawful, reasonably sized source acquired for genuine repository-wide reuse may instead enter the provider-neutral source library under `guidance/sources.md`; acquisition alone does not justify quotation or publication use.

The repository license does not relicense Scripture, official or liturgical text, received prayers or hymns, third-party translations, quotations, images, fonts, or other external material. Put a local notice wherever excluded wording could reasonably be mistaken for project-owned expression.

Render the common reuse-and-rights notice once as a compact, legible colophon on the same physical final page as the terminal content. It must never force a rights-only page. Keep work-specific rights detail in the scope appendix, source record, or beside the affected material rather than enlarging or duplicating the common notice.

Every text offered for vocal prayer or ritual recitation must reproduce an identified historical, approved, liturgical, or otherwise received witness. Neither the project nor an AI contributor may compose, translate, paraphrase, modernize, conflate, or materially adapt such a text. Use an exact identified human translation with recorded status and rights; otherwise omit it. Expand an explicit abbreviation only from the same witness or a governing edition it incorporates, and record both loci. Commentary may explain a prayer but must remain visibly distinct and must not function as a substitute translation.

## Audit records and generation metadata

Keep enough tracked evidence to reproduce editorial judgments without publishing private reasoning or a search diary. The applicable profile defines filenames; collectively the records identify the question and material exclusions, governing editions, source roles and loci, substitutions, disagreements, consequential negative results, material unresolved leads, jurisdiction/currentness, rights, completed review, and outstanding review. Never record credentials, private reasoning, host or user identity, machine paths, network data, or session identifiers.

Every canonical publication keeps `generation-metadata.tex` beside `main.tex` and imports it exactly once at the terminal display point. Its first active declaration is one `\AIDocumentRevisionTimestamp{YYYY-MM-DDTHH:MM:SSZ}`, its second is one `\AIGenerationProvenance{workflow-id}{workflow-version}{workflow-digest}{run-id}{seed-commit}{install-commit}`, and those are followed by one or more `\AIModelContribution` declarations. The declarations are the complete tracked audit record. Their rendered form displays only the revision timestamp; model identity, qualifiers, effort, client/runtime, and contribution history are not reader-facing publication content. A profile may permit a prose-free mechanical companion to declare `\AIInheritedGenerationMetadata` from one named canonical source while displaying its own timestamp once.

The generation-provenance record states what produced the document and what the
project state was at that point. Each of its six fields is either a value or the
literal `unknown`, and `unknown` is a record rather than a placeholder: it says
the fact was not recoverable. Never write a digest, a run id, or a commit that
was not read from the run or from the repository's own history, and never carry
a digest, run id, or seed commit without the workflow it belongs to. A run id
here is the engine's deterministic hash of workflow, version, seed commit and
normalized arguments; it identifies a run and never a session, a host, a user,
or a machine path, and nothing that does may enter the record. The seed commit
is the commit a run was pinned to when it was seeded and is never rechecked
against HEAD, so it states the repository the run was bound to; the install
commit states where the produced artifact entered the tree. The two are
different facts and neither is inferred from the other. The record renders
nothing, so adding it to a document leaves that document's PDF byte-identical.
Comparing what a document records against what the project declares now is
advisory display only: it never blocks a build, a check, or a release, it grants
no authority to rebuild, reinstall, or re-review, and it is not the research
staleness ledger, which asks a different question of different inputs under
`guidance/staleness.md`. A document that records no origin makes no such
comparison and is shown none.

The timestamp is the whole-second UTC time when the publishable render source was finalized. Update every affected consumer when render-relevant source or an imported fragment changes. Never derive it from Git, file metadata, build time, environment, or a content hash. Preserve every exposed model qualifier and client/runtime fact verbatim in the tracked declarations; name unavailable components specifically and never guess them. Every provider's model disclosures meet the same standard: exact model identifiers, exposed qualifiers reproduced verbatim, and specific naming of unexposed components. Separate tracked contributions when model, qualifiers, or material runtime differ, keep contributions using the same model and qualifiers adjacent, and never repeat an exact contribution declaration.

The rendered publication displays the revision timestamp once, without a
standalone `Generation Metadata` or `AI Generation Metadata` wrapper heading.
It does not display model identity, qualifiers, effort, agent instances,
client/runtime records, contribution counts, or other internal production
history. Do not publish prompts, process narration, machine or session data, or
a chronological agent/runtime ledger in a PDF or web edition. Keep audit
detail that is safe and necessary for reproducibility in the tracked
declarations or owning research and production records.

The metadata gate rejects missing, duplicate, noninitial, malformed, or non-UTC timestamps; a missing, duplicated, misplaced, or malformed generation-provenance record; a provenance field carried without the workflow it belongs to; exact duplicate contribution declarations; generic family-only model labels; missing exposed qualifiers in the tracked record; invalid inheritance; handwritten display substitutes; missing PDF title/subject; PDF dates inconsistent with the tracked revision; automatic creation dates or trailer IDs; a missing or duplicated visible revision timestamp; reader-visible model, qualifier, effort, or runtime metadata; and a generation-provenance workflow digest, run id, seed commit, or install commit reaching the rendered page. The workflow id and the workflow version are not scanned for: they are an ordinary word and a small integer, a match against extracted text would be an accident rather than a leak, and a gate that treated one as a leak rejected every propers document in the corpus.

## Alpha publication gate

Generation provenance, source audit, production validation, alpha eligibility,
and deployment are separate states. Use `source-audited` only when the
corresponding source event is recorded. `Alpha` means that the six public-alpha
concerns above pass for the current artifact; it does not mean complete, final,
official, or approved by an external authority. `Published` describes
deployment of a verified alpha artifact, not promotion to a higher editorial or
ecclesiastical state.

Typography serves navigation and meaning. Remove wrapper labels already supplied by the surrounding heading, but retain labels that convey authority, attribution, safety, contrast, accessibility, or stable semantic fields. Give repeated multi-field forms consistent visible field names. Do not use typography to imply doctrinal or juridical force.

Where a profile separates source-grounded and exploratory synthesis, that
boundary is structural. A relation record names at least two stable
source-element keys and one or more evidence classes. Textual observation,
documented historical orientation, documented reception, and source-grounded
synthesis may support the source-grounded component. Exploratory proposal
belongs only in the expressly exploratory component. “Authoritative
synthesis” must not imply that project-created analysis has magisterial
authority.

Before installing a publication:

- verify the reader-first order, terminal apparatus, every material claim and citation, source/proposal boundaries, and absence of unused references or padding;
- confirm rights, attribution, edition, jurisdiction, as-of, review, and generation records describe the artifact;
- compile enough passes to settle contents and references; reject fatal errors, undefined references, overflow, and unresolved layout warnings;
- generate review rasters as `guidance/repository.md` requires and visually inspect every page;
- check clipping, density, heading splits, tables, callouts, artificial whitespace, sparse spill pages, monochrome legibility, PDF structure, embedded fonts, metadata, and extracted text; confirm the final-page rights colophon is readable, unclipped, non-overlapping, and has not created a spill page; and
- install only the reviewed PDF at its mirrored `pdf/` path, leaving intermediates under ignored `build/`.

Profile-specific gates remain mandatory.
