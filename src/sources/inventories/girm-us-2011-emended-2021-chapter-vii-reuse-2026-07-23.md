# United States GIRM Chapter VII Reuse Review

Reviewed on 2026-07-23.

This record documents the bounded canonicalization and reuse proof for the
current United States English General Instruction material inside
`family.roman-missal.third-edition-latin-us-english`. It supplements the family
ledger and does not itself create a source identity, evidence state, or
publication binding. The proof covers the exact official online edition notice
and Chapter VII, especially nos. 363 and 365(a)--(d); it does not canonicalize
the whole mixed Latin, United States English, Missal, GIRM, and amendment
cluster.

## Identity and edition boundary

The *Institutio Generalis Missalis Romani* is registered as a separate work
related to the *Missale Romanum*, not as another edition of the altar book. Its
stable numbered locus system, translations, territorial adaptations, amendment
history, and independent web delivery make that separation useful and
truthful.

The bounded edition is the United States English state published with *The
Roman Missal*, Third Edition in 2011 and represented online with the
emendations promulgated on 22 October 2021. The official landing notice also
records the separate confirmation of the no. 54 emendation, the confirmations
of the Roman Missal and United States adaptations, and the territorial and
rights identity. This state is distinct from:

- the Latin third typical edition and its 2008 emended reprint;
- the obsolete 2003 United States English web presentation;
- an exact publisher-specific 2011 United States altar book; and
- later amendments, other territories, and other languages.

The state is current only through the 2026-07-23 access and review. Its stable
edition ID does not use `latest` or `current`; a materially changed official
version requires a new edition or artifact decision.

## Exact artifacts and rights

Two exact official USCCB responses were acquired twice, with byte-identical
results on the repeated acquisition:

- the 53,102-byte landing and table-of-contents response, SHA-256
  `8ec0eb3daf080812411c88b9c73a3828063c831b4657062849c905adef4268a3`;
  and
- the 58,199-byte Chapter VII response containing nos. 352--367, SHA-256
  `7b7656491b5a72bfa3bb4b907cb091a5fa5aa9c9947a4716c74120b02b64dddf`.

The landing notice identifies protected ICEL excerpts and United States
adaptations and states the USCCB all-rights-reserved restriction. No
redistribution permission was established. Both artifacts are therefore
first-class `restricted` records: their exact identities, retrieval routes,
hashes, byte sizes, provenance, and limitations are reusable, but their HTML
payloads are not tracked. The landing is not mislabeled as the complete text,
and Chapter VII is not mislabeled as the complete split-HTML presentation.

## Passage normalization

The official online-edition notice is an exact currentness and rights control.
Chapter VII supplies five independently addressable checked passages:

- no. 363, governing proper orations and the stated Ordinary Time weekday
  alternatives;
- no. 365(a), Eucharistic Prayer I;
- no. 365(b), Eucharistic Prayer II;
- no. 365(c), Eucharistic Prayer III; and
- no. 365(d), Eucharistic Prayer IV and its invariable Preface.

The protected wording was inspected against the consumer claims but was not
retained or centrally transcribed. Each passage remains pinned to its exact
artifact. Keeping the four subdivisions of no. 365 separate prevents a
metadata correction to one rule from needlessly invalidating consumers of the
others, while an exact Chapter VII artifact change still reaches all five.

## Reviewed consumers

Ten publications consume the bounded source state:

1. the postconciliar *Order of Mass* exposition binds the online-edition notice
   and all four no. 365 subdivisions;
2. the seven Year A proper guides for Ordinary Time Weeks XI--XVII each bind
   the notice, no. 363, no. 365(b), and no. 365(d); and
3. the Most Holy Trinity and Most Holy Body and Blood of Christ guides each
   bind the notice, no. 363, and no. 365(d).

The Week XI--XVII checks preserve two different consequences: eligible ferial
use of a formulary is permitted rather than automatic under no. 363, and
Eucharistic Prayer II may use its own or another qualifying Preface under no.
365(b), while Eucharistic Prayer IV remains a conditional unresolved branch
with its own Preface under no. 365(d). The two solemnity guides use no. 365(d)
in the opposite direction: their appointed proper Prefaces exclude Eucharistic
Prayer IV. No consumer turns a permitted or excluded path into a claim about
what occurred at an undocumented celebration.

Review found no contradiction requiring rendered-text correction. Existing
claims were sufficiently bounded, so this slice changes only source identity,
audit records, and publication bindings; no TeX or installed PDF changed.

## Acceptance proof

The source graph validates with 36 artifacts, 4 corpora, 16 editions, 49
passages, 2 segments, 9 works, and 230 bindings.

Reverse-use lookup returns:

- ten currentness consumers for the online-edition notice;
- nine proper-guide consumers for no. 363;
- one exposition consumer for each of nos. 365(a) and 365(c);
- eight consumers for no. 365(b), consisting of the exposition and seven
  Ordinary Time proper guides; and
- ten consumers for no. 365(d), consisting of the exposition and nine proper
  guides.

Three run-local mirrors of the actual graph validated the correction-propagation
boundary:

- changing valid landing-artifact metadata produced exactly ten stale
  currentness fingerprints;
- changing valid Chapter VII artifact metadata produced exactly twenty-nine
  stale fingerprints across no. 363 and nos. 365(a)--(d); and
- changing only valid no. 365(d) passage metadata produced exactly ten stale
  fingerprints while leaving the parallel no. 363 and no. 365(a)--(c)
  consumers current.

These tests prove that shared official state and shared rule corrections reach
every reviewed consumer while independently normalized subdivisions do not
create needless cross-invalidation.

## Remaining family work

This proof deliberately leaves the broad family open. The next exact reusable
slice is the 2002 Latin *Missale Romanum* artifact and the separately owned 2008
*Notitiae* variation-list container, with page-ranged passages for the
Ordinary Time, Trinity, Corpus Christi, and calendar consumers. The 2008
variation list must not be represented as the complete 2008 altar-book
artifact.

Later work should separately normalize the Latin GIRM states, the no. 54 and
other amendment acts, additional United States GIRM chapters when consumers
need their loci, the complete split-HTML presentation if a genuine full-corpus
proof is undertaken, and a lawfully identified publisher-specific 2011 United
States altar-book artifact. Several legacy links to the 2003 Holy See
presentation also require currentness review rather than silent reuse as the
2021-emended state.
