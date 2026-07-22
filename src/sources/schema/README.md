# Source Manifest Schema

`scripts/source-library` is the executable schema and validator. Version 1 was
frozen on 2026-07-22 after the complete-source City of God tracer exercised its
identity, artifact, corpus, passage, binding, rights, search, fingerprint, and
impact semantics. It uses five source record types and one publication-local
binding record:

- `work`
- `edition`
- `artifact`
- `passage`
- `corpus`
- `bindings`

Every source record has `schema = 1`, `record_type`, and an immutable `id`.
Bindings have `schema = 1`, `record_type = "bindings"`, `document`, and one or
more `[[bindings]]` tables. Unknown fields are rejected so a misspelling cannot
silently erase provenance or rights information.

Canonical manifests occupy only the documented work, edition, artifact,
passage, and corpus paths. Stable IDs do not derive from directory names, but a
nested record must reference the work or edition that physically encloses it.
Work-level relations are cross-references, not evidence-dependency ancestry.

Artifact records separate exact bytes from identity. A tracked artifact has an
affirmative rights status and basis, applicable jurisdiction for public-domain
or legal-exception claims, retrieval date, SHA-256, byte size, one payload below
its own manifest, and a public URL, local provenance statement, or parent
artifact. A derivative also names its transformation. `indexable = true`
requires a tracked searchable media type, `encoding = "utf-8"`, and bytes that
decode accordingly. Every `derived_from` input has an exact SHA-256 so the
transformation input is reproducible. Remote, restricted, and unavailable
records never smuggle payload paths into the repository.

An exact artifact that embeds a relative reference to a separately manifested
companion uses `support_artifacts`, an array of tables with `artifact_id` and
`embedded_reference`. The reference must be a safe relative path occurring
literally in the parent bytes. It must already be in canonical POSIX form and
must not contain percent encoding, traversal, dot segments, empty segments, a
URI authority, query, or fragment. The target must be a different exact tracked
artifact in the same edition. Support artifacts enter dependency ancestry and
fingerprints but do not silently become corpus members or search inputs. This
mapping lets a later materializer restore the source package layout while each
canonical artifact retains one payload owner.

```toml
support_artifacts = [
  { artifact_id = "artifact.example.edition.figure-1", embedded_reference = "figure-1.jpg" },
]
```

Corpus members are unique artifact IDs with exact hashes. The validator locks
the member set with:

```text
sha256(UTF-8 sorted lines: ARTIFACT_ID<TAB>ARTIFACT_SHA256<LF>)
```

The stored value is `sha256:<digest>`. Adding a later artifact to an edition
therefore does not silently enlarge an existing corpus search.

A passage in any state beyond `cataloged` names its controlling `artifact_id`
and copies that artifact's bare 64-character digest into `artifact_sha256`. A
verified passage also records `verified_on`. An inspected or verified passage
whose controlling artifact is indexable records one or more 1-based inclusive
`physical_line_ranges`; validation requires the pairs to be positive, ordered,
non-overlapping, and within the exact artifact. A passage `text` is a checked
excerpt, not a punctuation-normalized quotation: it requires ordered
`transcription_segments`, each identifying an exact raw-line substring inside
the ranges, and is unavailable for non-indexable image or PDF artifacts until a
separate checked locator model exists. Whitespace-joining those segments must
reproduce `text` exactly. Physical lines are delimited only by LF bytes; a CR is
content unless it immediately precedes the LF terminator. This permits XML tags
or intervening apparatus lines to remain in the artifact without inventing an
implicit markup-stripping policy.

```toml
physical_line_ranges = [[120, 148], [151, 179]]
text = "An exact excerpt crossing two raw lines;"
transcription_segments = [
  { line = 132, text = "An exact excerpt" },
  { line = 133, text = "crossing two raw lines;" },
]
```

Passage records do not accept `searched` as a source state because a query is a
publication-local research event. A binding may record a search over a ranged
passage, and the command-line search then examines only its declared physical
lines while rechecking the entire controlling artifact's hash and size.

A searched binding requires `search_scope`, `searched_on`, `query`, `method`, a
canonical `search_mode`, and `matching_line_count`. Schema version 1 modes are
`raw-line-literal-casefold-v1` and
`raw-line-literal-case-sensitive-v1`. Validation replays the query against the
exact artifact, ranged passage, or corpus and requires the recorded
matching-line count to agree.
A `negative-search` requires zero matching lines and only `text/plain` search
representations; register a plain-text derivative when markup or layout impairs
content search. The built-in modes examine literal text within one physical
LF-delimited UTF-8 line at a time. They do not establish absence across line
breaks, normalized whitespace, inflection, synonyms, or translations. Direct
textual use binds a passage or supplies explicit loci. A verified binding
records `verified_on`.

Bindings with any of `acquired`, `searched`, `inspected`, or `verified` also
carry a canonical `source_fingerprint`; `cataloged`-only bindings do not. The
fingerprint is `sha256:` followed by the SHA-256 of compact
UTF-8 JSON containing the complete TOML record and the IDs and recursively
computed fingerprints of its evidence dependencies. JSON object keys and
dependency IDs are sorted; work `relations` remain non-dependency
cross-references. Derived inputs and support artifacts are evidence
dependencies. Compute the value with:

```sh
scripts/source-library fingerprint SOURCE_ID
```

Changing the bound record or any exact ancestor then makes the binding stale
until its consumer is reviewed. The fingerprint proves which metadata and
artifact hashes were reviewed; it does not itself prove that the source was
read or a claim was correct. Availability, acquisition, search, inspection,
and verification remain separate states.

`indexable = true` is only a checked capability of an artifact, not evidence
that an index was built. The `indexed` evidence state is reserved and rejected
in schema version 1 until an index receipt or reproducible recipe can name its
date, method version, exact coverage, and registered derivative.

IDs contain lowercase ASCII letters, digits, dots, and hyphens. Recommended
forms are:

```toml
id = "work.augustine.de-civitate-dei"
id = "edition.augustine.de-civitate-dei.npnf-dods"
id = "artifact.augustine.de-civitate-dei.npnf-dods.plain-text"
id = "passage.augustine.de-civitate-dei.npnf-dods.10.6"
id = "corpus.augustine.de-civitate-dei.complete-english"
```

The validator's tests contain minimal complete fixtures and adversarial rights,
ownership, type, graph, snapshot, and search cases. Every implementation change
must update this file and those tests in the same commit when their documented
surface is affected. Changing accepted fields, manifest meaning, fingerprint
inputs, or search-receipt semantics requires the schema-version decision in
`guidance/sources.md` and a changelog entry.
