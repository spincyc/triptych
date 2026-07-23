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
belong to `src/gpt/` merely because a GPT-assisted publication first used them.

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
- **Passage** — an addressable locus in an edition or artifact. A passage record
  may preserve a checked transcription, page or line map, discrepancy, or
  verification event. It never erases the edition and artifact that control it.
- **Corpus** — a versioned, explicit search boundary. Schema version 1 members
  are exact, hashed artifact records; broader intellectual scope belongs in the
  corpus description rather than a dynamically expanding work or edition
  pointer. A corpus name alone never implies completeness beyond its declared
  members and snapshot.
- **Binding** — a publication-local declaration that an identified source or
  corpus was used, searched, or retained as a lead at stated loci and in a
  stated role. Bindings belong beside the publication's research records.

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
  corpora/<corpus>.toml
  inventories/
```

`<namespace>` identifies the responsible author, body, collection, or other
stable owner needed to avoid collisions; it is not a theological or editorial
classification. Put an artifact at the narrowest work and edition owner that
truthfully identifies it. Do not duplicate identical bytes under several
publication leaves or source records.

Each publication that enters the source system keeps
`research/source-bindings.toml` beside its existing profile-required records.
The binding file supplements rather than replaces `scope.md`, `source-audit.md`,
passage matrices, edition manifests, or other human-readable records.

Generated reverse indexes, full-text search databases, reports, caches, and
other reproducible derivatives belong under ignored `build/sources/`. They are
not authoritative inputs. A retained normalized or diplomatic text needed by
future research is an artifact under `src/sources/`, not a build cache.

## Repository-first acquisition and storage

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
  artifact snapshot, or machine-ranged passage for a stated research question;
- **inspected** — a person or agent read the identified passage and the stated
  amount of surrounding context; and
- **verified** — wording, attribution, edition identity, or a publication claim
  received the source- and profile-appropriate direct check.

These labels are cumulative only when the record actually establishes each
one. Possession is not reading; search capability is not search; a search hit
is not inspection; inspection of a transcription is not image collation;
checking one passage is not examination of a work or author-wide corpus.

Schema version 1 reserves and rejects an `indexed` evidence state until an
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

A source binding identifies the publication, work, edition or artifact when
material, exact loci where known, source role, verification state, and enough
context to distinguish a checked passage from a bare citation. It may also name
a local claim key or research-matrix row. Schema version 1 does not require a
machine ID for every sentence; profiles may require claim-level bindings for
consequential claims or structured inventories.

Any binding that records acquisition, search, inspection, or verification pins
the complete bound record and its evidence ancestors with the schema-defined
source fingerprint. Its represented artifact, ranged passage, or corpus
boundary must have exact hashes; a passage search also requires validated
physical-line ranges. Search additionally requires registered indexable bytes,
a canonical tool mode, and a replayed matching-line count. Verification records
its date. A changed fingerprint is a consumer review obligation, not permission
to copy a new value mechanically. Catalog-only leads have no fingerprint
because no exact witness has yet been reviewed.

When a publication makes a work-wide, author-wide, completeness, originality,
or negative-search claim, bind a versioned corpus or artifact snapshot and
record the material search boundary, languages, methods, and limitations.
Phrase negative results as bounded and correctable. A literal search cannot
exclude synonyms, inflection, paraphrase, translation difference, damaged OCR,
unindexed material, or unsearched languages. The repository's built-in search
is narrower still: it tests literal text within each LF-delimited physical
UTF-8 line and does not cross line or raw-markup boundaries. Use an exact
registered normalized derivative for broader content search, and never promote
an empty raw-line result into a semantic absence claim. Schema version 1 accepts a
`negative-search` binding only over exact `text/plain` search representations,
and validation replays its zero-result receipt. Register a normalized
plain-text derivative when source markup or layout would frustrate content
search.

References and reader-facing prose continue to cite a human-usable work,
edition, and locus. Stable source IDs support audit and tooling; they do not
replace intelligible citations.

## Dependencies, corrections, and freshness

Maintain separate dependency classes:

- **render dependencies** rebuild publications whose visible bytes import or
  render a shared source; and
- **evidence dependencies** identify publications whose claims or audits rely
  on a source record, passage, artifact, or corpus.

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

## Migration and gates

Migrate through a dual-record period:

1. inventory existing source occurrences without moving or deleting them;
2. create and validate central identities and artifacts;
3. add publication bindings while existing research records remain operative;
4. compare bindings with citations and local audits;
5. remove only duplicated identity or provenance after coverage is proven; and
6. retain local roles, interpretations, limits, and consequential negative
   results permanently.

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
