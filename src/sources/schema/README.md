# Source Manifest Schema

`scripts/source-library` is the executable schema and validator. Version 1 is
provisional until the first complete-source tracer has exercised and frozen
it. It uses five source record types and one publication-local binding record:

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

Corpus members are unique artifact IDs with exact hashes. The validator locks
the member set with:

```text
sha256(UTF-8 sorted lines: ARTIFACT_ID<TAB>ARTIFACT_SHA256<LF>)
```

The stored value is `sha256:<digest>`. Adding a later artifact to an edition
therefore does not silently enlarge an existing corpus search.

A passage in any state beyond `cataloged` names its controlling `artifact_id`
and copies that artifact's bare 64-character digest into `artifact_sha256`. A
verified passage also records `verified_on`. Passage records do not accept the
`searched` state because schema version 1 has no machine-enforced passage byte
or line range; bind the exact artifact or corpus search instead.

A searched binding requires `search_scope`, `searched_on`, `query`, `method`, a
canonical `search_mode`, and `matching_line_count`. Schema version 1 modes are
`raw-line-literal-casefold-v1` and
`raw-line-literal-case-sensitive-v1`. Validation replays the query against the
exact artifact or corpus and requires the recorded matching-line count to agree.
A `negative-search` requires zero matching lines and only `text/plain` search
representations; register a plain-text derivative when markup or layout impairs
content search. The built-in modes examine literal text within one physical
UTF-8 line at a time. They do not establish absence across line breaks,
normalized whitespace, inflection, synonyms, or translations. Direct textual
use binds a passage or supplies explicit loci. A verified binding records
`verified_on`.

Bindings with any of `acquired`, `searched`, `inspected`, or `verified` also
carry a canonical `source_fingerprint`; `cataloged`-only bindings do not. The
fingerprint is `sha256:` followed by the SHA-256 of compact
UTF-8 JSON containing the complete TOML record and the IDs and recursively
computed fingerprints of its evidence dependencies. JSON object keys and
dependency IDs are sorted; work `relations` remain non-dependency
cross-references. Compute the value with:

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
ownership, type, graph, snapshot, and search cases. During the provisional
tracer period, a schema adjustment must update this file and those tests in the
same commit. After the freeze checkpoint, changing accepted fields or semantics
requires a schema-version decision under `guidance/sources.md`.
