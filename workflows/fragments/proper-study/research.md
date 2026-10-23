# Establish the evidence and defensible interpretations

Preserve the context's authorized publication mode. For reference-only work,
declare it in `research/scope.md` and both appointed-source records; follow the
1962 profile's locator/audit record contract instead of retaining full pulls or
transcriptions. Record actual inspection outcomes and unresolved checks, never
infer collation from a locator. The complete appointment and reception research
remain required, and every claim must rest on evidence actually inspected.

Read and verify `research/context.md`; correct a contextual error from evidence.
Complete the governing edition's source records, rights audit, and every
appointed element's bounded reception search. Read complete biblical contexts,
direct patristic exegesis, and relevant medieval or later saintly reception.
Resolve existing holdings through uncapped `commentary-work-index discover`
for every appointed passage and `formulary` for the target Mass, as the Catena
guidance requires. Register or reuse exact sources lawfully and keep valid
`research/source-bindings.toml`; never invent a binding ID. Every source
actually read or used must reach an exact artifact, segment, passage or corpus,
with honest evidence states and the reviewed source fingerprint. A work or
edition catalog entry alone cannot represent a checked witness. Keep genuinely
uninspected bibliography as `lead`, without claiming acquisition or inspection.

Keep complete retrieval receipts and bytes in this run's assigned scratch area
until the following `source-registration` stage finishes. Give that worker the
actual receipt locations in your result's `notes`, and put durable URL, edition,
hash, size, retrieval date, native checked loci, rights and extent findings in
the research records. Do not put machine paths in tracked files. Registration
retains lawful reusable bytes in `src/sources/`, and registers restricted
identities and hashes without their bytes. A bibliography-only citation does
not finish the reusable-source handoff in this version of the workflow.

Identify every checked reception witness for source registration, including
analogues, liturgical commentators and sources omitted from the final prose.
The next stage records each binding in `research/source-dispositions.toml`:
an admitted, validated passage/Scripture edge; a durable deferral with concrete
missing criteria and the source's actual Scripture relation; a reasoned
rejection; a non-commentary use; or an explicitly uninspected lead. Acquiring
an artifact, finding a harvest attribution, or verifying a claim never by itself
admits a fragment. Keep the source's native locus and the Scripture it actually
expounds distinct from this Mass's appointed passage.

Write `research/scope.md` with precise checked loci, witness roles, material
disagreements, negative searches, unresolved leads, rights, and evidence bounds.
Write `research/interpretations.md` with two to five proposed coherent readings:
each one's controlling claim, compatible authors and their reasoning, a
contribution from every appointed element, its four senses, important limits,
and concrete comparison with the other readings. Distinguish verified author
interpretation from the editor's whole-formulary synthesis. If fewer than two
defensible readings emerge, research again rather than invent a second one.

Apply the three-document profile's comparison of exegetical questions in that
record before drafting: show the inference that distinguishes each reading,
and address the appointed texts' consequential difficulties. Do not substitute
different titles for different arguments.
Apply the profile's passage-level difficulty test: record the appointed words,
the principal witnesses' actual inferences, and what their different answers
change. A searchable holding or a source list does not establish this reading.

Preserve real disputes and identify complementary differences honestly. The
goal is source-first interpretive depth, not a quota of names. Missing support
requires the proportionate second search the editorial standard specifies.
Prepare the concise study's required page-2 chronology through the canonical
`proper-chronology` record and annotations commands. Use this family's own
verified appointments and the owning adapter; preserve partial-verse and
adaptation limits, alternatives, event/composition distinctions and absent
dates. Follow the chronology profile for postconciliar appointment query inputs.
Prepare the `orientation-v2` rows as the chronology profile directs. Inspect
their actual passage scope and dated subjects before handing them to an author;
the concise table must not print a composite element's dates beside one of its
constituent passages or repeat identical dates for nested Gospel forms.
Before the component manifest exists, generate them with
`tools/tpt proper-chronology annotations --provider {provider} --document {proper} --presentation orientation-v2 --write`.
For Psalms, verify the traditional attribution and any identified occasion or
remembered event separately from composition; an era attached to an author is
not an event date. Inspect a composition-only answer for missing event evidence,
and preserve an unresolved occasion when the sources supply none.
Inspect the controlling chronology source owners in this research boundary.
A prior date-free study's approval does not cover new date claims.
Provide those claims a reviewed home in the expansive study as well, such as
a same-owner terminal historical appendix. Complete these records before
drafting reader-facing study prose. A fresh research reviewer follows.

On reentry, address all research-owned findings and update every affected
source or interpretation record. Downstream authoring and reviews will rerun.
Return the actual records written and concrete remaining limitations.

Before cold review, write `research/review-dependencies.toml` with a `paths`
array of repository-relative source files or directories that this research
reads outside its leaf. Include the canonical same-family shared Missal owner
for postconciliar work and any controlling same-family registry records. An
empty array is valid when all evidence is local or already bound by source ID.
The engine also seals the leaf's entire `research/`, `propers/`, and `instance/`
evidence, excluding mutable production/review receipts, and the exact ancestry
and available payload bytes of every registered binding. For the chronology it
seals every file the record and annotations computation opens outside the leaf,
and every source the chronology record cites, with that source's ancestry and
available payload; these need no declaration. The reviewer verifies that this
dependency declaration includes all other controlling external evidence.
