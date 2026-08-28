# Reusable Source Library

This contract governs repository-wide external-source identity, acquisition,
storage, search, verification, and reuse under `src/sources/`. It supplements
the universal editorial and repository standards and the profile governing each
publication. It does not turn Triptych into a critical-edition publisher,
replace a publication's claim-level source audit, or weaken any genre-specific
evidence, rights, currentness, or review requirement.

## Governing priorities

Apply these priorities in order:

1. identify the intellectual work, edition or expression, delivery artifact,
   language, locus system, and rights basis without conflating them;
2. keep distributable, reasonably sized, reusable source material in the
   repository so an ordinary clone remains a useful research environment;
3. distinguish material that is available or searchable from material actually
   inspected, verified, and used for a particular claim;
4. share stable source identity and checked textual evidence while keeping each
   publication's evidentiary role, interpretation, sufficiency judgment, and
   qualifications local; and
5. make source corrections and changed mutable witnesses discoverable to every
   consumer without silently rewriting their arguments.

The source library is provider-neutral. External works and artifacts do not
belong to a provider branch merely because a provider-assisted publication
first used them.

## Identity model

Keep the following objects distinct:

- **Work** — the abstract intellectual or documentary work, act, book, article,
  collection, manuscript, webpage, or other source object. A work record owns
  its stable identity, responsible creator or promulgating body, titles,
  language history, conventional locus grammar, and work-level relationships.
- **Edition** — a materially identified edition, recension, translation,
  expression, official version, dated web state, or other form whose wording or
  authority can differ. An edition records editors or translators, publication
  facts, language, date, jurisdiction or authority where applicable, and its
  relation to the work.
- **Artifact** — exact acquired or remotely identified bytes: a scan, PDF,
  image, HTML response, EPUB, XML file, OCR transcription, diplomatic text, or
  normalized derivative. An artifact records its cryptographic hash when bytes
  were acquired, provenance, retrieval route and date, media type, extent,
  rights status, storage disposition, derivation relationships, and any
  first-class mapping from an embedded relative reference to a separately
  owned support artifact.
- **Segment** — a bounded constituent of exactly one controlling artifact,
  attributed to the work and edition that the constituent actually represents.
  Use a segment when an anthology, collected volume, archival bundle, or other
  container artifact belongs to one work while a bounded extent within it
  witnesses another. The segment records machine-checkable line or artifact
  page bounds without moving, duplicating, or falsely re-owning the container
  bytes.
- **Passage** — an addressable locus in an edition. A version 2 passage chooses
  exactly one artifact or segment controller; version 1 retains its frozen
  controller rules. A passage record may preserve a checked transcription,
  page or line map, discrepancy, or verification event. It never erases the
  edition and exact artifact that control it.
- **Corpus** — a versioned, explicit search boundary. Schema version 1 members
  are exact, hashed artifact records; broader intellectual scope belongs in the
  corpus description rather than a dynamically expanding work or edition
  pointer. Schema version 2 does not change this artifact-only corpus model. A
  corpus name alone never implies completeness beyond its declared members and
  snapshot.
- **Binding** — a publication-local declaration that an identified source or
  corpus was used, searched, or retained as a lead at stated loci and in a
  stated role. Bindings belong beside the publication's research records.

**A derivative and a projection are different edges.** `derived_from` means
these bytes were transformed into those bytes — an OCR of a scan, a
normalisation of a transcription — and stays inside one edition, because that is
what a derivative is. `projected_from` names *testimony*: the witnesses a rule
was applied over to infer something the edition does not carry itself. It
crosses editions by construction and must, since a projection drawn only from
the edition it describes would have nothing to draw on.

The Douay-Rheims carries no paragraph marks — zero pilcrows in 5.8 MB — so its
paragraphing is projected from the King James and the World English Bible, which
are other editions necessarily. Recording those under `derived_from` would claim
the projection was made out of the Douay-Rheims's own bytes; pointing it instead
at something in-edition that did not produce it would make the record lie in
order to satisfy a check. A projection with no stated witnesses is
unfalsifiable, so the field may not be empty, and each entry must be an artifact
this library holds.

### Which date belongs to which object

A work and an edition each have a date, and they are dates of different events.
The identity model above kept them distinct without ever saying so, and the
silence produced the divergence it was bound to.

- **A work's date is when it was written.** A work is composed once. Augustine's
  *De Genesi ad litteram* is c. 401–415. It is not 1841.
- **An edition's date is when that edition was printed or translated**, because
  that is the event an edition *is*. 1841 is Migne's. This is also the date the
  edition's path is prefixed with under "Ownership and paths" below — a path to
  a printing is about the printing.
- **Bible translations are the exception, and it is deliberate.** For them the
  translation is the thing: the Douay-Rheims is a 1582–1610 work and the King
  James a 1611 one, dated by the act of translating. Dating them to the
  composition of Genesis would be absurd, and no other class of work is dated
  this way.
- **A composition date that is a range or disputed is recorded as a range with
  its basis**; one that is unknown is recorded unknown. Absence is data and has
  somewhere to live.

**A composition date is never inferred from a printing date.** That inference is
the defect of [the shape](the-shape.md) §1 in its exact form — a date that
resolves successfully and wrongly — and it is silent, because the wrong century
is a well-formed integer.

The consequence for consumers is the reason this matters. Anything ordering or
filtering by *when this was written* reads the **work's** date; anything asking
*which printing is this* reads the **edition's**. The catena's chain is ordered
oldest first, so reading the printing date puts a Reformation commentary ahead
of a Father.

The divergence, as found: `work.toml` for *De Genesi ad litteram* carries **no
date field at all** — no work record in the library does — its Migne edition
carries `date = "1841"`, and the catena renders the work at 415 from
`text_date` in `src/sources/commentary/fragment-loci.yaml`, restated once per
fragment. One work, two dates, in two subsystems, with nothing reconciling them,
and the library holding neither.

Stable IDs are lowercase, machine-readable, and independent of URLs, mutable
titles, filesystem moves, and provider names. A changed URL does not create a
new work. Materially changed bytes do create a new artifact identity; a changed
translation, recension, or official version ordinarily creates a new edition.
Never make `latest`, `current`, or an access host part of a supposedly permanent
work identity.

## Ownership and paths

Tracked source-library records use this hierarchy:

```text
src/sources/
  README.md
  schema/
  works/<namespace>/<work>/
    work.toml
    editions/<edition>/
      edition.toml
      artifacts/<artifact>/
        artifact.toml
        <distributable source files when retained>
      segments/<segment>.toml
      passages/<passage>.toml
  corpora/<corpus>.toml
  calendars/<calendar>/propers.yaml        # every mass of that calendar
  calendars/<calendar>/rubrics.yaml        # the companion rubric registry
  inventories/
  bibles/
  commentary/
  reading-plans/
```

`calendars/` holds the normalized YAML indexes of mass formularies and their
ordered propers, one directory per calendar (`roman-1962`, `postconciliar`,
`roman-pre-1955`)
and one `propers.yaml` in each, whose `sections` map holds every mass of that
calendar — seasonal, common, marian, christological and sanctoral alike. The
`common` section is the Commune Sanctorum, which this repository held nothing of
until 2026-07-31; its masses carry no date and are reached only by reference
from a saint's day. Each file
declares the
`triptych-calendar-masses/v1` schema, the controlling edition, its ordering
rule, the registry that owns its identities, its citation and orthography
conventions, and its verification state. `tools/tpt check-calendar-masses`
validates them and runs inside `make check`.

### Quote every scalar that holds liturgical text

**Any YAML scalar carrying a title, incipit, name, note, citation or prayer text
is quoted.** Not "quoted when it looks like it needs it" — always, because the
character that breaks it is ordinary Latin punctuation and the failure is
silent.

An unquoted scalar ends at its first `:` in a block mapping and at its first `,`
inside a flow mapping. The remainder does not vanish; it becomes a **second
mapping key with a null value**, which is well-formed YAML, parses cleanly, and
looks like a field nobody recognises.

Four instances of this one class landed on 2026-08-01:

- unquoted commas cut five notes in `roman-1962/rubrics.yaml` in half, and four
  truncated citations plus a rubric label that lost "which nevertheless yields to
  an occurring Sunday" shipped to the browser;
- a comma split `Manete in me, et ego in vobis` into `incipit: Manete in me`
  beside `et ego in vobis: null`, and the page served the truncated antiphon;
- a colon closed the pre-1955 calendar entirely; and
- a calendar was briefly unparseable mid-write.

**The structural gap: nothing enumerates unrecognised keys on a proper.**
`check-calendar-masses.check_reference` does enumerate unknown fields — but only
inside a `takes_from` mapping, which is the one place the schema happens to have
a closed field list. `check_proper` reads the keys it knows and ignores the rest,
so `et ego in vobis: null` sitting beside `incipit` passes every gate. Until a
proper's keys are closed and checked against that closure, a split scalar
announces itself nowhere: it is [the shape](the-shape.md) §1 in the storage
layer, a reference that resolves successfully and wrongly. Closing it is open
work, and quoting is the discipline that stands in for it meanwhile.

**A mass or proper names where its text is printed instead of reprinting it.**
`takes_from` on a mass takes the whole formulary; on a proper it names a single
proper of another mass. A record that takes its text this way carries none of
its own — not the incipit, not a translation — and `check-calendar-masses`
refuses one that does. `_calendars.resolve_propers` resolves the reference once
for the validator and for the browser alike, so the reference a gate accepts and
the reference a page renders cannot come apart. The field exists because the
schema could not previously say "this mass takes that text": the four resumed
Sundays after the Epiphany held one set of orations twice and the two copies had
already drifted five ways. [The proper data guide](propers-for-agents.md) owns
the field's grammar and the defects it closed.

An index is a planning and cross-reference spine, not a source of record: it
carries no artifact hash and proves nothing on its own. A publication still
binds the edition and artifact that control each text through
`research/source-bindings.toml`, and a claim still needs its own verified
passage. Treat every citation and text in an index as an unverified lead until
collated against the controlling edition, and keep each file's
`open_collation_items` current rather than silently harmonizing a known
divergence.

Sunday and Triduum series are ordered by the liturgical year from the First
Sunday of Advent. Sanctoral series — Marian, Christological, and saints'
feasts — are ordered by calendar date from 1 January. All of them are sections
of the calendar's single `propers.yaml`, never separate files.
Neither ordering asserts rank, precedence, or the occurrence schedule of any
civil year.

`<namespace>` identifies the responsible author, body, collection, or other
stable owner needed to avoid collisions; it is not a theological or editorial
classification. Put an artifact at the narrowest work and edition owner that
truthfully identifies it. Do not duplicate identical bytes under several
publication leaves or source records.

**Anything with an inherent order sorts in that order in a directory listing.**
A listing is the first index anyone reads, and one that arrives alphabetically
when its subject is chronological or canonical makes a reader reconstruct the
order in their head every time.

So a path component carrying an ordered thing is prefixed with what orders it,
padded to a fixed width:

- **An edition of a source is prefixed with its date**, printing year first:
  `1611-king-james-version`, `1899-douay-rheims-american`, `1962-...`. Several
  editions carry a date today as a *suffix* and others carry none, so the
  listing is chronological nowhere.
- **A missal or other witness is prefixed with its print date**, for the same
  reason and in the same form.
- **A book of scripture is prefixed with its canonical position**, `01-gen`,
  and a numbered book puts the ordinal last, `46-cor-1`, so that every book of
  one name groups together and a listing reads as the canon rather than as an
  alphabet.
- **A chapter file is zero-padded** to the width the longest book in the canon
  requires, so `010` follows `009`.

Paths are lowercase throughout. Display casing — *Genesis*, *1 Corinthians* —
belongs in the text a reader sees and never in a path: a capitalised path
inherits every casing question with it, and a case-insensitive filesystem makes
two such paths one file on one machine and two on another.

Two limits on all of this, and both matter more than the convention itself.

**A path is not an identity.** Stable IDs are independent of filesystem moves,
as stated above, so date-prefixing a directory must not silently re-key the
record that lives in it, break a citation, or rename a published artifact. A
citation still addresses `1 Cor 13:4`. Where an id and a path have been the same
string, separating them is the work, and it is not done by renaming a directory.
On 2026-08-22 the maintainer authorized a one-time override of this rule for
the 1962 and postconciliar proper-guide renumber from Lent-first to Advent-first
liturgical-year order: all published leaf paths, PDFs, web editions, and release
records were renamed in that commit. This paragraph records the exception; the
standing rule remains unchanged for every other case.

**Derive the prefix; never type it beside the fact.** The date is already in the
edition record and the canonical position is already in the tracked book index.
A prefix hand-written next to the field it restates is a second source of truth
that will disagree with the first, and only one of the two will be read.

A segment lives beneath the edition of the constituent it identifies, and its
`edition_id` must name that enclosing edition. Its one `artifact_id` may point
across the work boundary to a container artifact under the container's truthful
owner. The segment pins that artifact's exact SHA-256 and records
`segment_type`, evidence states, context, and at least one bounded locator:
`physical_line_ranges` or `artifact_page_ranges`. `segment_type` is an open
kebab-case description such as `constituent-work`, not a closed subject
taxonomy. This cross-work evidence edge does not make the container artifact
part of the constituent work. Keep structural ownership traversal through the
segment's edition distinct from evidence-dependency traversal through its
artifact.

Each publication that enters the source system keeps
`research/source-bindings.toml` beside its existing profile-required records.
The binding file supplements rather than replaces `scope.md`, `source-audit.md`,
passage matrices, edition manifests, or other human-readable records.

Generated reverse indexes, full-text search databases, reports, caches, and
other reproducible derivatives belong under ignored `build/sources/`. They are
not authoritative inputs. A retained normalized or diplomatic text needed by
future research is an artifact under `src/sources/`, not a build cache.

## Repository-first acquisition and storage

Project research uses only publicly reachable sources. Do not purchase an
edition, use a paid subscription, request or store access credentials, or ask
the maintainer to fund source access. Public reachability does not establish
rights, authority, edition identity, reliability, or verification: apply every
ordinary source and artifact gate below. If a necessary witness is not
publicly reachable, pursue proportionate public primary, official, library,
catalog, and critical-edition alternatives and record the unresolved access
and evidence boundary rather than inventing a check.

**Retrieve whole documents.** When a document is retrieved at all, retrieve the
entire document. Never pull a fragment where the whole is pullable: not the one
chapter a question needs, not the first page of a paginated view, not the prefix
of a bulk file that a reader truncated. If a source offers a complete download
beside a per-section view, take the complete one.

The reason is that a partial retrieval and a short document are
indistinguishable afterwards. A file that stops at Psalm 27 looks exactly like a
file about Psalms 1–27, and a claim measured against it reads as a claim about
the whole. That is this library's governing failure — a source that resolves
successfully and wrongly — arriving through the retrieval rather than through the
citation. It has already happened here: a check against an external versification
standard truncated at Psalm 27, so a statement about a 5.8 MB file rested on a
fifth of it. The lane labelled its finding corroboration rather than proof, which
was right, but the retrieval should not have stopped.

Where the whole genuinely cannot be had — paywalled beyond a point, rate-limited,
or served only in fragments — record the exact bound reached and why, and mark
the artifact's completeness explicitly. A bounded retrieval, declared, is a
usable source. A bounded retrieval, undeclared, is a false one.

**Resolve a source's aliases before retrieving it.** A work is rarely catalogued
once. It carries a Latin title and a vernacular one, an incipit that stands in
for a title, an author named in Latin, in Greek, in the vernacular and by see or
epithet, a Migne volume number, and often a modern editor's short form. Search
the aliases first, and drive the retrieval from all of them rather than from the
one string a question happened to use.

Two failures follow from skipping this, and they pull in opposite directions.
The first is a false absence: the work is held, or reachable, under a name
nobody searched, and the lane records "no text available" for something that was
available all along. The second is a false duplicate: the same work arrives twice
under two names, the two copies drift, and nothing compares them — which has
already happened here, where four Sundays' orations were held a second time and
the copies had silently diverged in five ways before anything noticed.

Put each durable alias at the identity level it describes. Record alternate
work titles and incipits in `work.alternate_titles`; record edition-specific
titles, editors, publishers, series, volumes, and catalogue forms in the
edition's identity fields or `notes`. Those declarations establish known
identity; they do not assert that a retrieval actually tried the names.

The aliases actually tried are acquisition provenance. When an artifact was
identified, record the exact query strings, repository or endpoint, material
hits or misses, and search bound in that artifact's `provenance`; lengthy
supporting detail may remain in `notes`. When no artifact was identified, or
one campaign covered multiple candidates, record the same evidence in the
owning acquisition audit or inventory. Do not invent a placeholder artifact to
hold a negative search. A later reader must be able to distinguish a work that
is genuinely unreachable within the recorded bound from one sought under the
wrong name.

**Source text must never route through a model.** Retrieval fetches and retains
whole byte streams, hashes them, and seeks within them locally. A model in the
retrieval path does not merely risk truncating a document; it will silently
rewrite one. Demonstrated here on 2026-07-31: asked for a verbatim text, one
route returned Basil's *Hexaemeron* exactly and, from the same host under the
same instruction, returned a **paraphrase** of Gregory of Nyssa. A paraphrase
presented as a father's words, under his name, is the worst failure this library
can produce — worse than an empty page, because the reader has no way to see it.

The same route also truncated a 7.2 MB file to its front matter and refused a
whole public-domain homily as too long while serving the same homily three
sections at a time. Truncation there was detectable only by fetching twice and
comparing prefixes. None of these are visible in the output: each returns
well-formed text of the right kind.

Retrieval and redistribution are separate acts, and this rule governs only the
first. Retrieve in full; then let the rights record decide the disposition. A
work that may be read and not republished is `remote` or `restricted` below —
and it is now the whole of that work whose hash and bounds are recorded, rather
than an arbitrary slice of it.

Use these storage dispositions:

- **tracked** — the exact artifact is lawful to distribute from the repository,
  reasonably sized, and materially improves reproducibility or reuse;
- **remote** — the exact artifact is not retained because of demonstrated size,
  duplication, or a stable authoritative/public delivery route, but its
  retrieval location, acquired hash when known, and rights status are recorded;
- **restricted** — lawful project access does not include repository
  redistribution; tracked metadata may identify the artifact, but its bytes
  must not enter Git, build products, tests, fixtures, or public artifacts; and
- **unavailable** — the record identifies an expected or previously consulted
  object whose exact bytes cannot presently be obtained or authenticated.

Default to `tracked` for lawful, reasonably sized plain text and other reusable
artifacts. Do not introduce a separate object service, credential requirement,
large-file extension, or dedicated data repository until measured source size
or rights constraints justify the contribution and distribution cost. A remote
artifact that is necessary to reproduce a consequential claim must have an
honest access limitation; a hash proves identity, not continuing availability.

Record rights per artifact, not merely per abstract work. Distinguish the
underlying public-domain text from a host's markup, annotations, typography,
database, or newly created transcription. Record the known public-domain
jurisdiction and basis, license, permission, legal exception, restriction, or
unresolved status. `tracked` requires an affirmative recorded distribution
basis; online availability and successful download are insufficient.

**Settle a recurring rights question once, in a rights record.** Where the same
question governs a whole body of material and keeps being reopened, the answer
belongs in one file under `src/sources/inventories/`, with its citations, the
routes examined and refused, and what would change if the position changed. A
rights position stated only in prose, in three places, in three wordings, is
three positions. `liturgical-english-rights-v1.toml` records the material facts
for the English of the postconciliar Roman Missal; the governing presumption and
per-surface procedure are in `liturgical-text-publication-policy.md`. The record
exists because the question had been answered independently at least three
times and the reasons had been kept nowhere. A rights record is not
legal advice and states its jurisdiction; it is the project's own reading, held
to the same standard as any other claim, and citable so that the next reader
inherits the reasoning instead of the conclusion.

Segments have no independent storage disposition or rights declaration. They
inherit both from their one controlling artifact, and a segment cannot make
restricted or remote bytes trackable. When a schema version 2 artifact records
`page_count`, that count describes the exact artifact and bounds any segment
`artifact_page_ranges`; it is not a claim about the pagination printed within
the source.

Preserve exact acquired bytes when they serve as an evidence artifact. Put
normalization, corrected OCR, extracted text, page maps, tokenization, and other
derivatives in separate artifacts linked to their inputs. Do not silently
correct raw OCR or represent a normalized derivative as a facsimile. A
derivative's parent artifact must have an exact hash; a URL or mutable identity
alone does not reproducibly identify the transformation input.
Every tracked payload must remain beneath its own artifact manifest, be the only
payload owned by that manifest, and be covered by the manifest's rights record.
Unmanifested files and duplicate retained bytes fail validation.

Do not rewrite exact source bytes merely to make an embedded relative link fit
the canonical library layout. Map the literal reference to its separately
manifested exact support artifact. The mapping participates in dependency and
fingerprint impact while leaving search-corpus membership explicit. A source
package can then be materialized with its original relative filenames without
duplicating the canonical bytes. Treat the stored reference literally: it must
be an undecoded canonical relative POSIX path, with no percent encoding,
traversal, dot or empty segments, URI authority, query, or fragment.

## Research and verification states

Availability and evidentiary review are orthogonal. Use these terms exactly:

- **cataloged** — identity metadata exists;
- **acquired** — exact bytes were obtained and hashed or an authenticated
  remote object was checked;
- **indexable** — validation has established that an exact tracked text
  artifact can be searched by the registered raw-line mechanism; this is a
  capability, not an assertion that an index was built;
- **searched** — a recorded query or method was run over a named corpus,
  artifact snapshot, or machine-ranged segment or passage for a stated research
  question;
- **inspected** — a person or agent read the identified passage and the stated
  amount of surrounding context; and
- **verified** — wording, attribution, edition identity, or a publication claim
  received the source- and profile-appropriate direct check.

These labels are cumulative only when the record actually establishes each
one. Possession is not reading; search capability is not search; a search hit
is not inspection; inspection of a transcription is not image collation;
checking one passage is not examination of a work or author-wide corpus.

Both schema versions reserve and reject an `indexed` evidence state until an
index receipt or reproducible recipe can identify its date, stable method,
exact source coverage, and retained derivative. Model reusable normalized text
or a retained search index as its own derived artifact in the meantime.

An OCR, normalized text, search index, concordance, or embedding remains a
discovery aid unless separately verified as the profile requires. Semantic or
vector search may suggest passages but cannot establish absence, wording, or
attribution by itself.

## Central evidence and publication-local judgment

Centralize only facts and evidence that genuinely remain true across consumers:

- work, edition, translation, artifact, and locus identity;
- a constituent segment's exact container artifact and physical bounds;
- artifact provenance, hash, retrieval, language, rights, and derivation;
- checked transcription and page or line correspondence;
- source-local discrepancies and verification events; and
- bounded source notes whose wording and status are themselves reviewed.

Keep these matters publication-local:

- the claim for which a passage is used;
- direct-witness, textual-control, contextual, reception, analogue,
  negative-search, or lead status;
- interpretation, synthesis, disagreement, and doctrinal or legal significance;
- whether the evidence is sufficient for that publication's wording; and
- claim-local uncertainty, jurisdiction, currentness, and limiting context.

A reusable source card, paraphrase, topic label, or extracted proposition is a
project-created editorial artifact, not the external source itself. It requires
its own owner, provenance, review state, and consumer relationship. No consumer
may cite such a card as though it independently verified the underlying text.

## Bindings and search records

A source binding identifies the publication, work, edition, artifact, segment,
passage, or corpus when material, exact loci where known, source role,
verification state, and enough context to distinguish a checked passage from a
bare citation. It may also name a local claim key or research-matrix row.
Schema version 1 does not require a machine ID for every sentence; profiles may
require claim-level bindings for consequential claims or structured
inventories.

Use a schema version 2 binding file when any binding directly names a schema
version 2 record, including a segment or a version 2 passage. A version 2
binding file may continue to bind version 1 sources; raising the binding schema
does not migrate or reinterpret those sources. A schema version 1 binding may
name only version 1 records.

Any binding that records acquisition, search, inspection, or verification pins
the complete bound record and its evidence ancestors with the schema-defined
source fingerprint. Its represented artifact, ranged segment, ranged passage,
or corpus boundary must have exact hashes; a segment or passage search also
requires validated physical-line ranges. Search additionally requires
registered indexable bytes, a canonical tool mode, and a replayed matching-line
count. Verification records its date. A changed fingerprint is a consumer
review obligation, not permission to copy a new value mechanically.
Catalog-only leads have no fingerprint because no exact witness has yet been
reviewed.

An indexable segment with `physical_line_ranges` is searchable only within
those ranges of its exact controlling artifact. A segment that has only
`artifact_page_ranges` is not searchable by the repository's raw-line modes.
A passage controlled by a segment remains inside both that segment's bounds
and the exact artifact hash pinned by the segment and passage. A version 2
passage may use `artifact_page_ranges` under the same containment rule, but a
page-only passage is likewise not raw-line searchable. These limits are
evidence boundaries, not claims that the constituent is complete beyond the
declared ranges.

When a publication makes a work-wide, author-wide, completeness, originality,
or negative-search claim, bind a versioned corpus or artifact snapshot and
record the material search boundary, languages, methods, and limitations.
Phrase negative results as bounded and correctable. A literal search cannot
exclude synonyms, inflection, paraphrase, translation difference, damaged OCR,
unindexed material, or unsearched languages. The repository's built-in search
is narrower still: it tests literal text within each LF-delimited physical
UTF-8 line and does not cross line or raw-markup boundaries. Use an exact
registered normalized derivative for broader content search, and never promote
an empty raw-line result into a semantic absence claim. Both schema versions
accept a `negative-search` binding only over exact `text/plain` search
representations, and validation replays its zero-result receipt. Register a
normalized plain-text derivative when source markup or layout would frustrate
content search.

References and reader-facing prose continue to cite a human-usable work,
edition, and locus. Stable source IDs support audit and tooling; they do not
replace intelligible citations.

## Dependencies, corrections, and freshness

Maintain separate dependency classes:

- **render dependencies** rebuild publications whose visible bytes import or
  render a shared source; and
- **evidence dependencies** identify publications whose claims or audits rely
  on a source record, passage, segment, artifact, or corpus.

A segment's structural owner is the work reached through its enclosing
`edition_id`; source-family and locus checks use that ownership. Its evidence
dependencies include the exact controlling artifact even when that artifact is
owned by another work. Fingerprints, reverse uses, and impact therefore follow
the container evidence without changing the constituent's intellectual
identity. A passage likewise follows its edition for ownership and its one
artifact or segment controller for evidence freshness.

A changed research record need not rebuild an unchanged PDF, but it must make
affected consumers discoverable. Source tooling reports reverse uses and impact
without automatically editing, accepting, or rebuilding consumers. A source
correction creates a review obligation; it does not silently change a
publication's conclusion.

Artifacts are immutable by identity. Correct metadata in place only when the
artifact identity remains exact and the correction is auditable. Changed bytes
receive a new artifact record and consumers remain pinned until reviewed.
Mutable official texts, law, institutional pages, and current facts require a
dated edition or artifact state and retain every profile-specific currentness
rule.

## Schema stability

Schema version 1 was frozen on 2026-07-22 after the complete-source City of God
tracer. Its accepted manifest and binding fields, record meanings, evidence
states, dependency and fingerprint inputs, corpus snapshot rule, passage-line
semantics, and search-receipt modes form one compatibility boundary.

Schema version 2 is a narrow additive layer for truthful constituent ownership
inside an exact artifact, including a separately owned container artifact. It
adds the `segment` record, permits `page_count` on a version 2 artifact, permits
a version 2 passage to choose exactly one `artifact_id` or `segment_id`, and
requires version 2 bindings when they directly name version 2 records. A
version 2 passage retains `artifact_sha256`, which is always the bare digest of
the ultimate controlling artifact whether the passage names it directly or
through a segment. Corpora remain schema version 1 artifact-only snapshots. No
valid version 1 manifest, binding, fingerprint, search result, or receipt
changes meaning.

Do not silently reinterpret a version 1 record. A change that adds or removes
accepted fields, changes the meaning or fingerprint of valid data, changes
search results or receipt replay, or makes a valid version 1 record mean
something materially different requires an explicit schema-version decision.
Use a new schema version when old and new meanings cannot be applied together
without ambiguity, and make migration explicit rather than mechanically
rewriting consumer review pins.

An implementation or documentation correction may remain version 1 only when
it enforces the already documented contract without assigning a new meaning to
valid data. It must include a regression test and a schema changelog entry when
the observable validator or query behavior changes. Pure diagnostic output may
evolve compatibly when it does not alter manifests, bindings, fingerprints, or
research receipts.

## Reading the library

Four registered tools reach this library, and they do different jobs:

| Tool | What it is for |
| --- | --- |
| `source-library` | validate and query the records themselves |
| `source-reader` | read the corpus — search it, step through a work passage by passage, and write `structure/sources` for the browser, under each record's own rights |
| `source-inventory` | the publication-source inventory and its classification review |
| `source-family-migration` | the reviewed family-migration ledger |

`source-reader` is the one that serves text, so it is the one bound by rights:
a record with no publishable basis is projected as identity and absence, never
as bytes. `tools/tpt source-reader list` reports the library's current extent —
works, editions, artifacts, passages, and how many of those are readable here —
and is the derivation to quote rather than a count typed into prose.

## Migration and gates

Migrate through a dual-record period:

1. inventory existing source occurrences without moving or deleting them;
2. create and validate central identities and artifacts;
3. add publication bindings while existing research records remain operative;
4. compare bindings with citations and local audits;
5. remove only duplicated identity or provenance after coverage is proven; and
6. retain local roles, interpretations, limits, and consequential negative
   results permanently.

For an ordinary source-bearing change, refresh and review in this order:

1. run `tools/tpt source-inventory refresh --audited-on YYYY-MM-DD` after the
   publication or its owned source surface changes;
2. review any new or unresolved publication in
   the provider's classification review (`classification-review-v1.toml` for
   GPT or `claude-classification-review-v1.toml` for Claude), then rerun
   `tools/tpt source-inventory classify --review PATH` when its broad source
   strata change;
3. run `tools/tpt source-family-migration refresh --audited-on YYYY-MM-DD`, and
   manually review any new family presence rather than expecting refresh to
   infer it;
4. use `--accept-canonical-catalog` only after the source library validates and
   every family with canonical IDs has received the ledger review required
   below, including families whose own manifests did not change; and
5. run `make check-sources` before finalizing the change.

`make check-sources` is the normal, non-completion gate: it validates the
canonical source graph and bindings, replays the exhaustive inventory, and
checks the family ledger while permitting honestly pending review units. Run
`make check-source-family-screening` only as the explicit family-screening
completion audit; it fails until every exact review-unit surface is
`family-screened`.
Neither target asserts atomic citation coverage, and neither is an implicit PDF
build dependency.

The migration inventory is a separate audit contract, not a source-manifest
record type and not an extension of frozen source schema version 1. It must
enumerate the exact `main.tex` publication universe, explicit nonpublication
research owners, inherited and mixed ownership edges, and the complete textual
authoring surface outside global typesetting primitives, each with a content
hash. This conservative superset includes legacy source-bearing records and
rendered claim surfaces. It may preserve legacy words such as
“checked” or “verified” as quoted audit history, but its own states must not
promote them into source-library evidence states.

Classify inventory candidates on independent axes: intellectual source family,
identity confidence, artifact availability, mutability, rights-review state,
evidence ceiling, and migration disposition. Access hosts are delivery routes,
not source families. Exact URL, DOI, title, or byte-hash clusters are discovery
evidence only; merge them into one work or edition only after the identity has
been reviewed. Ambiguity is a valid inventory result and must remain visible.

An inventory is complete structurally when every publication and source-bearing
record is represented and its snapshot replays. That does not mean every
citation has been semantically disaggregated, every edition identified, every
artifact acquired, or every claim verified. Close those dimensions explicitly
through reviewed source-family dispositions and publication bindings.

Keep a structural migration separate from any substantive correction it
uncovers. A wrong locus, attribution, quotation, legal state, or theological
claim receives its own source-aware content revision and every profile-required
build and review step.

Before enforcing complete coverage, the validator may accept an explicit
migration mode that checks only records already entered into the source system.
Schema-final enforcement must reject duplicate or malformed IDs, dangling
relationships, hash mismatches, undeclared or impermissibly tracked artifact
rights, invalid loci, missing binding targets, and machine-local data. It must
also report orphan sources, unbound candidate citations, stale evidence
dependencies, and ambiguous legacy identities without silently resolving them.

Adding source-library records alone does not require a PDF build. Any change to
rendered citations, references, source excerpts, or imported source cards does.
Build, inspect, and install every affected publication under its own profile.
