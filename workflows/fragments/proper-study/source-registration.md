# Retain the research for the shared corpus

Read `guidance/sources.md`, `guidance/catena.md` and
`guidance/reading-plan-for-agents.md`. This stage owns reusable source
registration and the leaf's `research/source-bindings.toml` and
`research/source-dispositions.toml`; it may correct their supporting research
audit, but it does not author the studies. Read the research worker's result
and its scratch retrieval receipts, then reconcile the complete checked-witness
and reception matrix in `research/scope.md`. Include inspected witnesses even
when no final quotation or interpretation uses them. Do not let a bibliography
entry stand in for registration.

Check aliases and container holdings before creating records. Reuse truthful
work, edition and exact artifact identities; verify retrieval hashes and
measured extents against the actual bytes. Register every source actually read.
Retain lawful, reasonably sized reusable source bytes by default. Record the
particular reason for `remote`, `restricted` or `unavailable`; rights can forbid
retention without excusing identity registration. Never reconstruct missing
bytes or claim inspection from a receipt. Seek the original and a lawful
English edition as the generic source-registration contract directs. Preserve
existing fingerprint pins until the consumer's changed evidence is reread.

For checked biblical commentary, admit a reusable excerpt when its natural
extent, attribution, edition, exact controller, wording, rights, original or
translation voice, and text date are established under the owning source and
Catena checks. Store its verified passage and text under `src/sources/works/`
and its canonical Scripture edge in `commentary/fragment-loci.yaml`. Derive
chapter display from that natural extent. A harvest lead is L1, an acquired
holding L2, and only the checked passage with its validated edge is L3. Never
manufacture an L1 harvest run or a date, translation, text, extent or verification
to fill the gap. An analogue is anchored to the Scripture its author actually
expounds, which can differ from the appointed passage that led this study to it.

Write `research/source-dispositions.toml` using this independent workflow
schema. It does not add fields to source-library manifests or bindings:

```toml
schema = 1
contract = "proper-study-source-dispositions-v1"
document = "<this exact canonical document id>"
numbering = "vulgate"

[[sources]]
id = "<stable witness-and-locus key>"
binding_index = 1
binding_sha256 = "<digest of the complete current binding, from binding-digests>"
source_id = "<exact source_id of that one-based binding>"
source_fingerprint = "<that binding's actual reviewed fingerprint>"
locus = "<checked address in the author's own work, with context read>"
relationship = "direct-exegesis"
disposition = "deferred"
reason = "<why this candidate cannot yet be admitted>"
missing_criteria = ["<specific check still needed>"]
scripture_extents = [{ token = "Gen", first_chapter = 1, first_verse = 3, last_chapter = 1, last_verse = 5 }]
```

Replace the example's extent with the actual source's range in canonical
Vulgate numbering. Each binding has at least one row; separate checked loci
may share a binding, but every row has a unique stable `id`. The native `locus`
never supplies a Scripture extent. Use these dispositions:

- `admitted`: name existing verified `passage_ids = ["passage.…"]` controlled
  by the bound witness. Omit `scripture_extents` and `missing_criteria`: the
  canonical edge alone owns the admitted extent. The Catena validator must
  accept the text, identity, attribution, language, date, rights and edge.
- `deferred`: retain the exact witness pin, native checked locus, relationship,
  canonical candidate `scripture_extents`, concrete `missing_criteria` and
  reason in this durable queue. Admission work remains visible here; a generic
  pending note is insufficient. If the source's Scripture reach is genuinely
  unresolved, use `scripture_extents = []` and include the literal criterion
  `scripture-extent`. Do not infer it from the leaf's appointment.
- `rejected`: retain the same candidate identification and the concrete failed
  criteria and reason. Rejection of corpus admission does not erase valid
  publication-local evidence or change its evidence state.
- `not-commentary`: use `relationship = "not-commentary"`, with the actual
  checked source, native locus and reason; omit passage and Scripture fields.
- `lead`: use `relationship = "lead"` only for a `role = "lead"` catalog-only
  binding. Omit fingerprint, passage, Scripture and missing-criteria fields.
  State its non-use and uncertainty in `reason`; never relabel a read witness
  as a lead to bypass registration.

For the first three dispositions, `relationship` is `direct-exegesis`,
`analogue`, `doctrinal-illumination` or `liturgical-commentary`, describing
this study's use without changing what Scripture the source actually addresses.
Keep these roles separate from availability and verification states. The
`binding_sha256` pins the whole local binding, including role, native loci,
states and context; two uses of the same artifact are not interchangeable.
Obtain its actual digest with:

```sh
python3 scripts/_proper_study.py binding-digests --provider {provider} --document {proper}
```

Reread and reconcile a changed local use before replacing either pin. No
disposition grants reproduction rights.

Run the handoff check after writing the records:

```sh
python3 scripts/_proper_study.py source-dispositions --provider {provider} --document {proper}
```

After source-registration changes, run `tools/source-library validate`,
`make source-projection` and `make check-sources`; regenerate the Catena
structure and paragraphs when an edge or passage changes, using its owning
guidance. The following preflight mechanically requires the source projection
to be current. Return the actual registered source and admitted passage IDs,
the retained deferred or rejected keys and missing criteria, and the checks
performed. Missing research evidence goes back to research; do not invent it.

This handoff is mandatory in new `proper-study` version-15 runs and research
seal v5. Historical bindings and v3/v4 seals keep their original meaning; do not
restamp old accepted work or bulk-promote historical leads. A substantive new
research run adopts the new contract by independently checking reused evidence.
