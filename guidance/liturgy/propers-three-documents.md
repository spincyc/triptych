# Three documents from one Sunday's propers

## Scope and authority

On 17 September 2026 the maintainer requested a new propers production
contract: an expansive study containing two to five coherent interpretations,
a concise comparison of those interpretations, and a homily ready to speak.
This profile governs new and substantially revised proper studies in both
Roman Rite collections. It is the successor to the two-document presentation,
implemented by `proper-study` and `proper-components.toml` schema 2.

The [1962 profile](roman-1962-propers.md) and
[postconciliar profile](postconciliar-propers.md) continue to own identities,
governing editions, occurrence, source control, rights, language, and
form-specific branches. This profile replaces their reader-facing sequence,
fixed pagination, one collective four-senses table, mandatory cultural gallery,
and exploratory-proposal quotas for schema 2. Those older requirements remain
in force for schema-1 publications and the legacy `proper` and `proper-finish`
workflows. A new contract does not silently invalidate previously reviewed
documents or reopen the collection's production boundary.

[Editorial](../editorial.md), [repository](../repository.md),
[sources](../sources.md), and [calendar computation](calendar-computation.md)
standards continue to govern. A homily is newly authorized authored preaching
prose; it is not a newly composed prayer or a substitute liturgical text.

## Separate liturgical paths

The maintainer explicitly required the 1962 and postconciliar production paths
never to cross. Each run resolves exactly one calendar family and one proper
identity. Its context, appointed texts, optional branches, research judgments,
interpretive lanes, three documents, review evidence, and publication records
belong exclusively to that family. The same civil Sunday does not supply a
correspondence between the two calendars or authorize a combined interpretation.

The workflow selects the family from the canonical identity before resolving
the date. It uses only that family's profile, calendar, Missal, Lectionary
where applicable, source owner, and reader catalog. It rejects a liturgical
owner or authored proper component imported from the other family. Shared
engine, typesetting, and review code may serve both paths; provider-neutral
Scripture and patristic sources may be independently cited where pertinent.
Those shared facilities never transfer an appointment, a cycle, a rubrical
choice, or another proper guide's editorial interpretation across the boundary.

The separation is physical as well as editorial. Every 1962 document family
is rooted at `src/<provider>/liturgy/roman-rite/1962/propers/`; every
postconciliar family is rooted at
`src/<provider>/liturgy/roman-rite/postconciliar/<edition-locale>/propers/`.
Keep context, evidence judgments, all three authored documents, and durable
reviews beneath the owning leaf. A postconciliar shared Missal formulary stays
beneath that same postconciliar edition tree. Build, installed PDF, and web
paths mirror the respective canonical identity. There is no common Sunday
leaf above these roots. Check indirect dependencies as well as direct imports:
this boundary covers every oration, chant, reading, and optional branch, not
only the Gospel or the final document title.

## One owner, three reading experiences

One canonical leaf owns its research, exact source loci, interpretation audit,
prose components, and generation record. It produces:

| Output | Entrypoint | Purpose |
| --- | --- | --- |
| Research study, bare document ID | `main.tex` | Develop two to five complete and distinguishable interpretations. |
| Concise study, `-synthesis` | `synthesis.tex` | Interleave those interpretations around the questions an educated reader will ask. |
| Homily, `-homily` | `homily.tex` | Speak one intelligible, exegetical, pastorally fruitful argument. |

The companions are deliberately authored condensations and applications within
the same owner, not independently researched leaves. Each has its own declared
components and title, is separately built and reviewed, and receives its own
release record. The canonical study supplies the sole web edition. Shared
evidence and exact quotations have one owner; a prose passage belongs to the
output whose reader it serves. Do not pad a short work with the full study's
appendices or duplicate the full study verbatim to make a companion.

## Research before interpretation

Resolve the celebration, edition, territory, civil date, and applicable branches
before drafting. Record a complete ordered inventory of appointed texts and
the role of optional texts. Study each biblical unit in its literary context,
then direct ancient exegesis and later saintly reception. The older profiles'
passage-by-passage reception and lawful-text controls remain mandatory.

`research/scope.md` records the bounded reception sweep, checked sources and
loci, direct exegesis versus doctrinal illumination, unresolved evidence and
rights. `research/interpretations.md` records each interpretation's claim,
authors, exact supporting loci, the reasoning connecting the whole formulary,
its four senses, differences within and between interpretations, and which
connections are editorial synthesis. An author need not comment on every
proper; do not attribute the editor's complete Mass synthesis to an author who
only explained one passage. A catena supplies leads, not proof that its named
author or underlying work has been checked.

Declare controlling external source owners in
`research/review-dependencies.toml`; its paths must remain beneath `src/`.
Registered bindings already seal their source ancestry and available payloads.
Global guidance, `THIRD_PARTY.md`, and workflow review receipts remain governing
controls or audit references; do not list them as external source owners.
Explicitly declare controlling rights inventories, permission evidence, and
collation records beneath `src/` unless registered binding ancestry already
reaches them. A prose link in a source record does not add a sealed dependency.

At initial submission and after a research repair, audit the complete chain of
adopted authorities in the context, instance, formulary, source and rights
records. Include calendar and rubric authorities used to select permitted
branches. For each controlling authority, verify that its exact source owner
appears in the compiled research seal, following a summary inventory through
to any underlying records that govern its conclusion. Keep excluded leads
distinct from adopted evidence when determining this boundary.

Group compatible *arguments*, not reputations, periods, nationalities, or
quotations sharing a word. An author may contribute to several interpretations
when different checked passages support them. Each interpretation draws
substantively on at least two distinct patristic or saintly authors. A second
name without a developed contribution does not meet this requirement. The authors
must agree on its controlling claims; preserve any narrower disagreement
beside the relevant claim. If a central disagreement would undo the argument,
separate the readings or revise the argument. Do not invent a historical school,
unanimity, conflict, or a second interpretation merely to meet the numerical
minimum. Return to research if fewer than two defensible interpretations exist.

An interpretation can differ by governing emphasis, exegetical identification,
movement, or theological consequence. Complementary readings need not be rival
doctrines. Explain that relationship concretely. Neither smooth incompatible
identifications into one account nor dramatize complementary emphases as a
dispute. In Ordinary Time, a coherent theological reading of the whole Mass
does not prove that its semi-continuous readings and common orations were
historically composed as one thematic unit.

## The expansive study

Open with substantive prose introducing the Sunday's question and a compact
map of its appointed elements. Give the lawful study texts or rights-safe
locators in a convenient reading position. Clearly identify historical English
and, in postconciliar work, the public-domain study translation rather than the
approved proclaimed wording. Titles name the Missal and Sunday precisely.

Develop two to five substantial interpretations in sequence, with descriptive
titles that say what each reading finds. Each must:

- state a unifying interpretation of the whole formulary;
- explain the literal contexts and the actual reasoning of its principal
  witnesses, with exact usable citations;
- let every appointed element contribute, including orations and minor chants,
  without forcing each into an implausibly identical theme;
- address the strongest relevant difficulty or alternative; and
- conclude with its own distinct distillation of the literal, allegorical,
  moral, and anagogical senses.

The literal sense concerns what the texts assert in context; the allegorical
sense their fulfillment in Christ and his body; the moral sense the life of
conversion and charity; the anagogical sense their final fulfillment. A list
of virtues is not four senses. The spiritual senses remain anchored in the
literal text and checked reception. No single global table substitutes for the
four senses of each interpretation. Stable lane keys in the manifest and audit
make the correspondence inspectable; technical keys need not appear in prose.

Conclude with a short comparison showing what the interpretations share and
where their answers differ. Give each substantial argument one fullest home.
Depth means explaining why an author reads the text as he does and what that
reading changes, not accumulating names or repeating the same application.
For an ordinary Sunday, roughly 6,000–10,000 words of substantive exposition
is a useful planning range, not a quota. Evidence and reader value decide the
actual extent; reviewers must reject a thin outline masquerading as expansive.

Historical orientation can accompany the passage or occupy a terminal
appendix. A date asserted for Scripture still comes from the shared chronology
corpus under [its profile](../scripture-chronology.md). Schema 2 requires no
physical page-2 dossier and never invents a date to fill one. Terminal scope,
used references, generation timestamp, and compact rights colophon remain.

## The concise study

Write only after the expansive study passes cold review. Organize around a
small number of cross-proper questions or movements. Within each, place the
relevant authors and alternative answers beside one another, so the reader
can follow an actual comparison. Successive miniature summaries headed
"Lane 1", "Lane 2", and "Lane 3" do not interleave the alternatives.

Preserve every interpretation's controlling claim, the important agreements
and differences, and the four-sense distinctions where they materially change
understanding. Use brief attribution and precise source notes. A reader should
understand the alternatives without opening the long work, while the full
argument remains available there. Qualifications that affect truth survive
compression. Introduce no new source-dependent claim: a needed new claim goes
back through research and review of the expansive study.

Aim ordinarily for about 1,500–2,500 words, with substantive prose at most
roughly one third of the study. A longer or shorter treatment is acceptable
when the owning audit explains the reader's need. No mandatory two-page layout
or copied research apparatus substitutes for concision.

## The homily

Write after both studies pass cold review. Address an adult parish assembly
unless the task names another audience. Default to approximately 10–12 minutes
at an unhurried speaking pace; record the spoken word count and estimated pace
in the production audit. A timed human delivery is a distinct event and must
never be claimed merely from that estimate.

The spoken body must be ready to read verbatim. It is continuous preaching,
not an outline, commentary about preaching, stage directions, a lesson plan,
or a string of quotations. It need not rehearse every scholarly alternative.
Choose one coherent argument, or a demonstrably compatible combination, and
preserve any difference that matters to that argument. Explain what the
appointed texts say and why, including a meaningful relation between Gospel,
other Scripture, and the Mass's prayer. Let the larger research inform the
whole without reciting an inventory of every minor proper.

Use pedagogical techniques where they serve this text and this audience:
concrete imagery, a well-formed question, narrative development, contrast,
analogy with its limits, plain explanation of a difficult word, measured
repetition, a return to the opening image, and a specific practicable response.
The requirement is pertinent pedagogy, not every technique in every homily.
Move from attention through understanding toward conversion and hope. Do not
manufacture anecdotes, quotations, personal experiences, miraculous events,
clerical identity, or a Father's approval of the editor's application.

Separate a brief source-and-delivery note from the spoken body. Keep inline
scholarly apparatus and reader instructions out of the speech; name a Father
naturally when useful. Put exact loci, connection to reviewed interpretations,
audience, word count, and rehearsal findings in the terminal note or audit.
Conclude as preaching; any actual recited prayer must be an exact received
human witness under the universal prayer rule.

The [Homiletic Directory](https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20140629_direttorio-omiletico_en.html),
nos. 6–15 and 25 (checked 17 September 2026), supplies the liturgical
orientation: exegesis and catechesis serve proclamation; the readings and
prayers lead through Christ's Paschal mystery to Eucharistic participation and
daily life. This governs the homily's movement without turning it into a
scholarly lecture. It supplies no claim that an AI has prayed, heard this
congregation, or exercised the ordained ministry.

## Composition and review

Beauty follows from a legible, deliberate hierarchy: warm restrained type,
comfortable measure, generous but purposeful margins, quiet running furniture,
and meaningful breaks. Design each output for its use. The study needs
navigation; the concise work needs visible relationships; the homily needs
comfortable type and paragraphs that can be recovered at a glance while
speaking. Do not shrink type, leave conspicuous blank pages, or add decorative
material to satisfy a page target. Full-page inspection, log and extraction
checks, metadata, font embedding, and build/install byte identity remain
mandatory. No ornamental image is required.

`proper-study` runs source resolution and research, cold research review,
study authoring and cold review, concise authoring and cold review, homily
authoring and cold review, build and cold visual review, then canonical web
conversion, review, installation and publication gates. Each substantive
deliverable receives a fresh reviewer with no authoring conversation history.
Give the reviewer the task contract, artifact, evidence, and exact criteria,
not the author's defense or a desired verdict. Review each output on its own
terms as well as against its upstream source.

Findings identify a location, concrete defect, required result, and the owner
that can fix it. Missing evidence returns to research; an invalid whole-proper
argument returns to the study; compression returns to the concise document;
oral clarity returns to the homily. An upstream change invalidates downstream
judgments and requires their regeneration or explicit re-review. Changes to
rendered content invalidate visual acceptance. Never edit an accepted run's
state or submit a manufactured pass to advance it.

Record substantial defects exposed by a real run and promote repeatable
lessons into a gate, fragment, or this profile. Keep run-specific review
dispositions in `research/production-review.md`, including iterations, source
limits, substantive word counts, rendered page counts, checked artifacts and
hashes, and remaining limitations. If a workflow change invalidates its pinned
digest, seed a new run from the corrected contract and independently inspect
reused evidence; a rerun may reuse verified research, never an unearned verdict.

## Mechanical and judgment gates

Schema 2 declares `calendar = "roman-1962"` or `calendar = "postconciliar"`,
matching the canonical document path, and rejects cross-family imports.
It names exactly three PDF outputs, their local entrypoints, the
canonical web owner, stable element keys, and ordered components with mode
membership. Its two to five `[[lanes]]` records name stable keys, authors,
existing source-audit paths, component keys, all four senses, and coverage of
every appointed element. The checker verifies records and include reachability;
it does not prove theological agreement or quality merely from declared keys.

Cold reviewers decide those semantic questions. Acceptance requires real
source support, coherent and distinct interpretations, truthful comparisons,
four senses for each interpretation, meaningful whole-formulary coverage,
genuine concision, a speakable exegetical homily, and satisfactory composition.
The terminal program gate verifies all three installed PDFs, their exact
reviewed artifacts and current sources, provenance, canonical web edition,
correct family catalog, release records, and available publication checks.
One beautiful document, three existing files, or a successful build is not the
three-document deliverable.
