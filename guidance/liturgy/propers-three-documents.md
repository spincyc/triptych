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
form-specific branches. This profile owns schema 2's reader-facing sequence
and extent. The maintainer subsequently specified a 20–50-page expansive study
and an approximately 10–12-page concise study retaining the established first
four pages. The concise opening below adopts those pages without reinstating
the old mandatory cultural gallery or exploratory-proposal quotas. The older
two-document requirements remain
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
beneath that same postconciliar edition tree. The edition's formula-dispositions
row names its exact canonical shared owner; the research dependency must equal
that directory or descend from it. A provider-neutral or similarly named
`propers/.../shared/` path does not satisfy this requirement. Build, installed
PDF, and web paths mirror the respective canonical identity. There is no common
Sunday leaf above these roots. Check indirect dependencies as well as direct
imports: this boundary covers every oration, chant, reading, and optional
branch, not only the Gospel or the final document title.

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
release record. The canonical study supplies the sole web edition under the
[web-edition profile](../web-editions.md), including its appointed-text anchors.
Shared evidence and exact quotations have one owner; a prose passage belongs to the
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

Every lane's declared `sources` path belongs beneath the same leaf's
`research/` directory. Its bytes are research evidence and are also included
in the immutable study-review input seal. Moving the record outside that owner
or changing it after either acceptance invalidates the applicable review.

### The formulary is a compilation

This is settled for every proper and is not re-established Sunday by Sunday.
A Mass formulary is a liturgical compilation. Its chants, orations and
lessons have separate origins and were assigned to the day, and sometimes
reassigned, over a long history; the assembled Mass is a different object
from any of its parts. Patristic and later exegesis comments on the
constituent texts, such as a psalm, a prophecy or a Gospel pericope. It is
reception of that text, not of the Mass. A reading of the whole formulary is
therefore the editor's synthesis. Where a named liturgical commentator
expounds the Mass of the day as his books gave it, that is a distinct witness:
documented reception of the compilation as he received it, which may differ
from the governing edition's assignment.

Research therefore does not investigate a formulary's compilation history to
show that a whole-Mass reading lacks compositional warrant, and no review asks
for that demonstration. Record compilation history only where a specific fact
changes a claim. Examples are a documented deliberate pairing, a commentator
whose Mass had another Gospel or chant, or a textual form that only the
compilation explains. The distinction lives in the records.
`research/interpretations.md` labels cross-element connections as editorial
synthesis, and the studies attribute to each Father only what he said of his
own passage. Reader-facing prose does not disclaim a compiler's intention: the
[1962 profile's evidence rule](roman-1962-propers.md#evidence-and-claim-discipline)
is satisfied by not asserting one. In postconciliar Ordinary Time the premise
holds with added force, because the semi-continuous readings and shared Missal
prayers follow independent courses.

Declare controlling external source owners in
`research/review-dependencies.toml`; its paths must remain beneath `src/`.
Registered bindings already seal their source ancestry and available payloads.
Global guidance, `THIRD_PARTY.md`, and workflow review receipts remain governing
controls or audit references; do not list them as external source owners.
Explicitly declare controlling rights inventories, permission evidence, and
collation records beneath `src/` unless registered binding ancestry already
reaches them. A prose link in a source record does not add a sealed dependency.
For v3 research review, the engine separately seals the chronology computation
code and applicable identity registry. These are computation inputs, not entries
in the source-owner declaration; historical review contracts retain their
original seal shape.

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
substantively on at least two distinct patristic or saintly authors, as
[Liturgical commentators](#liturgical-commentators) defines them. A second
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
dispute. A coherent whole-Mass reading is editorial synthesis over a
compilation, as [above](#the-formulary-is-a-compilation).

### Liturgical commentators

A liturgical commentator expounds a Mass or office as a whole, as Rupert of
Deutz, Honorius, Sicard, Durandus, Schuster and *The Liturgical Year* do, or
preaches the Sunday's readings as a cycle, as Anthony of Padua and Alphonsus
Liguori did. His witness is reception of the compilation as his books gave it,
and it is used in that role.

Identify his Mass by its elements, never by its Sunday number. Compare the
Introit, Collect, Epistle, Gospel and other elements he names with the
governing edition's; `commentary-work-index formulary` reports that comparison
from `src/sources/commentary/formulary-loci.yaml`. Record in
`research/scope.md` his own heading beside the elements that match and those
that differ. A commentator's "eighteenth Sunday" is evidence only for the
elements it shares with this formulary.

Where his Mass had another Gospel or another chant, record the difference in
`research/scope.md`, where it keeps the studies from asserting anything about
the formulary's history, and in at most one clause of the expansive study's
scope appendix. In reader-facing prose, cite him only for what he says of an
element this formulary shares. Never cite him in support of a connection
between that element and this formulary's Gospel, which his Mass did not set
beside it. The readings, the concise study and the homily do not mention his
other Gospel, his other chants or the Mass they belonged to: a 1962 guide is
not the place for other Masses. Where his books place this formulary's Gospel
on another Sunday, what he says of it there is reception of that Gospel. Cite
it at that locus, without narrating the Sunday on which he read it.

Standing decides what a commentator may carry.
`src/sources/inventories/author-standing-v1.toml` records each author's
standing and its basis. The two authors an interpretation requires are
Fathers of the Church, canonized saints (Doctors among them) and the Blessed,
provided that at least one of the two is a Father or a canonized saint. A
Venerable, a Servant of God or any other orthodox ecclesiastical writer is
never one of the two. He may be a reading's principal witness to the Mass as a
Mass, and may support any claim his checked locus makes, provided two eligible
authors carry the reading. A censured writer, and a writer outside Catholic
communion, supplies structural and contextual evidence only. Record the
censure, and never cite a writer for the point on which he was censured.

Attribute words to the writer the locus inventory names. A posthumous
continuation published under a founder's series name is the continuator's and
is cited as the continuation. Research first submitted for review before
2026-09-22 is not reopened for this subsection alone. The maintainer's
decisions behind this subsection, and their reasoning, are recorded in
[the plan of 2026-09-22](liturgical-commentators-plan-2026-09-22.md).

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
is a useful planning range, not a quota. The finished expansive PDF occupies
20–50 physical pages, including its terminal apparatus. Evidence and reader
value determine the treatment within that range; reviewers must reject a thin
outline masquerading as expansive or repetition used to reach the minimum.

Historical orientation can accompany the passage or occupy a terminal
appendix. A date asserted for Scripture still comes from the shared chronology
corpus under [its profile](../scripture-chronology.md). The expansive study has
no fixed page-2 dossier. Its concise companion does, as specified below;
neither invents a date to fill a position. Chronological claims needed by the
concise opening must already have a reviewed home in the same owner's research
and expansive study, conveniently as a shared terminal historical appendix.
Terminal scope,
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

The finished concise PDF targets 10–12 physical pages, including the opening
four pages and terminal apparatus. The earlier 1,500–2,500-word and one-third
planning limits are superseded. Concision means selecting and integrating the
long study's strongest explanations; it does not mean a five-page abstract.
After the opening, develop the interpretive differences through the actual
exegetical reasoning and pertinent whole-formulary connections. Do not reach
the target through enlarged type, repeated summaries or copied appendices.

### The first four pages

Physical page 1 contains the complete propers map in liturgical order, followed
immediately by exactly four overview rows: **Literal**, **Allegorical**,
**Moral**, and **Anagogical**. Include every appointed element and identify
options as options. This brief orientation does not replace each expansive
interpretation's own four senses or erase differences developed in the concise
argument. No preceding cover shifts the physical page positions.

Physical page 2 contains only **Scriptural Date and Location**. Follow the
owning family's established dossier and evidence rules: the
[1962 dossier](roman-1962-propers.md#page-2-scriptural-date-and-location) or
the [postconciliar reader sequence](postconciliar-propers.md#reader-facing-order).
Inventory each distinct directly appointed biblical passage once, in canonical
then verse order, and distinguish composition, attributed setting, narrated
event, and reception. Use the canonical chronology tool's generated record and
annotations, including its alternatives, relation labels and unresolved states.
Do not reuse another Sunday's dates or substitute hand-authored date labels.
When the study needs to place another evidence profile beside the default
answer, declare that exact element/profile/relation/subject selection in
`research/chronology-profile-comparisons.toml` before regenerating. The
generated comparison remains visibly distinct from the default cascade; prose
must not splice a separately queried date into the default Date cell or its
explanation.
Postconciliar query inputs identify that edition's own verified appointments
through the adapter specified in the [chronology profile](../scripture-chronology.md).
Research review must inspect the new chronology and its controlling sources;
a formerly date-free study's approval does not cover newly added dates.

Physical pages 3 and 4 contain **The Propers: Themes and Movement**, a substantive
two-page source-grounded argument. Open with a direct thesis and develop the
whole formulary's movement. Both pages must earn their extent through readable
argument rather than decorative space or displaced apparatus. Physical page 5
begins the developed interleaved commentary. Its cross-proper questions deepen
and compare the earlier movement instead of repeating it. This restores only
the opening sequence; the remaining pages follow this three-document contract.

### Declared presentation and physical-page evidence

New `proper-study` runs require schema 2's
`presentation_contract = "interpretive-pagination-v1"`. Its `[presentation]`
table names distinct component keys for `inventory`, `overview`, `chronology`,
`themes`, and `commentary`. The first four are `front-matter` components
available in synthesis mode; the last is its synthesis-only
`integrated-commentary`. An opening component may also be used within the
same owner's research study. The inventory binds every appointed element key.
The chronology component declares `research/chronology-annotations.tex` as a
reference, imports those generated definitions once, and uses the required
`\chronodate{element-key}{\chronologyannotation{element-key}}` cells.

Use `zref-user` and `zref-abspage` in the concise entrypoint so settled auxiliary
evidence records physical pages, independent of printed page counters. Place
`\zlabel{triptych:concise:<role>:start}` and the corresponding `:end` around
the actual inventory, overview, chronology and themes content. Mark each
overview row with `triptych:concise:sense:literal`, `:allegorical`, `:moral`,
or `:anagogical`, respectively; each complete marker includes that same prefix.
Use `triptych:concise:commentary:start` at the beginning of the developed
commentary. The component checker owns the exact marker validation.

The artifact gates require inventory and overview on physical page 1,
chronology on page 2, themes beginning on 3 and ending on 4, and commentary
beginning on 5, together with the two PDF length ranges. They also require
settled references. These checks prove placement and declared coverage; cold
review must still judge the actual map, dates, four senses, argument and beauty.
Historical schema-1 and schema-2 publications without this explicit contract
retain their original validation rules. A new run cannot omit the contract to
evade the revised requirement, and old accepted results are not restamped.

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

The maintainer restored the established house typography on 21 September 2026:
Latin Modern, an 11-point article, 0.75-inch margins and monochrome printing.
`src/common/propers-format.tex` owns proper-specific presentation; it is imported
immediately after `common/preamble` and does not change unrelated publications.
Leaf files supply title and running-head fields and substantive components,
not font packages, geometry, title implementations or local table environments.
Discretionary Palatino/Pagella and enlarged single-column homilies are
superseded. New runs declare `format_contract = "propers-format-v1"`.
Historical manifests remain valid until explicitly migrated.

Use `\propertitle{title}{subtitle}{edition}{occasion}` for the full-width
opening. The first field is the liturgical Sunday or formulary name, the
second is an optional upright descriptive subtitle, and the last two fields
give edition/date/use metadata. The macro owns the title page's plain style
and spacing; leaf files do not add page-style commands around it. Use the
shared map/overview/dossier environments for tabular content,
`\properlane{stable-key}{descriptive title}` for each expansive interpretation,
ordinary subsections for its arguments, and one `fourSenses` description
block with Literal, Allegorical, Moral and Anagogical items. Citations remain
in ordinary footnotes or precise prose references with shared type treatment.
Each lane develops its own argument; it does not repeat the concise work's
four-page opening.

The homily alone also imports `common/propers-homily`. Its one
`properhomily` environment encloses only the literal spoken-component import,
after the title and before the terminal apparatus. It sets two columns in the
same Latin Modern body type and ends with a page break. Keep this import out of
both study entrypoints and their web input graph.

The homily environment owns the semantic `Homily` running head. Leaf files use
`\runninghead{...}` for any other short interior head; they do not call
`\markright`, `\fancyhead` or page-style primitives directly.

Import the spoken component exactly once, inside `properhomily`, and each
homily terminal-apparatus component exactly once after it. Do not duplicate
either component elsewhere to influence pagination. Leaf entrypoints and
components must not reset shared page dimensions such as text width, text
height, margins, paper size or column measure; make pagination repairs by
editing real content boundaries and ordinary page-break hints.

Entrypoints contain literal unconditional `\input{...}` commands in reading
order. The template formats content; it must not hide imports behind macros,
conditionals or computed paths. Concise components retain their literal zref
markers and named presentation roles. Page positions and extent remain governed
above, not inferred from a template call. Existing source prose is preserved
in a formatting migration; new chronology still requires a fresh source review.

The component gate, content-review seal, TeX recorder audit, and canonical web
conversion use one recursively resolved semantic source graph. A computed or
otherwise executable file-input mechanism outside its literal graph fails
before review, and recorder-only or converter-only sources fail the downstream
gate. Leaf sources may configure only the documented title/running-head fields;
they must not define, alias, redefine, or undefine shared format commands or
either control sequence of a shared environment. Generated chronology helpers
are the sole narrowly checked definition exception.

Full-page inspection, log and extraction checks, embedded-font checks, metadata,
substantive-text preservation and build/install byte identity remain mandatory.
Do not enlarge type, pad pages or suppress evidence to meet page targets.
No ornamental image is required.

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
