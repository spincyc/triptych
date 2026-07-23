# Justin First Apology ANF Volume 1 Reuse Review

Reviewed on 2026-07-23.

This record documents the completed bounded
`family.justin-martyr.first-apology-anf1-1887` reuse proof. It distinguishes
the anthology container from its constituent translation, preserves the exact
raw and facsimile representations, binds six publications only to the chapters
they actually use, and tests both direct and cross-constituent change
propagation. It records audit results; the canonical source records and
publication-local bindings remain the machine-enforced identities and evidence
states.

## Container, constituent, and exact artifacts

The source model preserves two identities that a flat bibliography would
conflate:

- *The Ante-Nicene Fathers*, volume 1 is the anthology container and owns the
  exact digitized artifacts; and
- Justin Martyr's conventionally named *First Apology* is the constituent
  work, with the Dods--Reith English as its own translated edition linked to
  bounded segments of those container artifacts.

The scanned introductory note on printed p. 160 calls Dods and Reith the
translators. Coxe's American introductory and bracketed editorial matter
remains distinct from Justin's text. The edition itself records the historical
question about the literary relation and ordering of the two extant apologies;
the canonical identity does not claim to resolve that question.

The complete translated body of chapters 1--68 is bounded in two exact
representations:

- the tracked 3,551,901-byte Internet Archive raw OCR, SHA-256
  `12cdc519c642b446cb4c6c3ba0bad9a2288687937975df6ca4c8b42aa6d92d84`,
  physical lines 16,858--20,282; and
- the remote 58,025,655-byte Internet Archive facsimile PDF, SHA-256
  `b50e358eebf85f06794c4dba16777eb6d27a35688a6c7a828b46c9d2190be8cc`,
  artifact pages 181--204 / printed pp. 163--186.

The final inclusive facsimile page also begins the appended Epistle of Adrian
after chapter 68 ends. That appended text is excluded by the segment's stated
constituent boundary; the page-only facsimile locator cannot express a
sub-page cut. The OCR segment ends exactly before the appended epistle heading.

The tracked automated page-number map confirms printed p. 163 at scan leaf
181, p. 183 at leaf 203, p. 185 at leaf 205, and p. 186 at leaf 206. Its leaf
sequence jumps from 187 to 190 between printed pp. 169 and 170, while the exact
PDF omits those two scan leaves. Direct inspection therefore establishes PDF
p. 201 for printed p. 183, p. 203 for printed p. 185, and p. 204 for printed
p. 186. The factual page map remains an auxiliary locating artifact rather
than a textual witness or evidence controller.

The public-domain and storage review already recorded for the ANF volume
applies unchanged: the raw OCR and page map remain tracked, while the much
larger facsimile remains remote as a storage-policy decision. New Advent's
later presentation is not the exact Buffalo artifact and is not assumed to be
textually identical to this edition without a separate collation.

## Passage normalization

Each presently selected locus has two passage records:

- an inspected OCR locator whose exact physical ranges and a short
  transcription segment make raw-text checking reproducible; and
- a verified facsimile passage whose artifact pages control edition identity,
  pagination, wording, attribution, and visible context.

The paired loci are chapters 61, 65, 66, and 67. Their checked boundaries are:

| Locus | OCR physical lines | Printed pages | Artifact PDF pages |
| --- | --- | --- | --- |
| 61 | 19,820--19,826; 19,844--19,897 | 183 | 201 |
| 65 | 20,082--20,110; 20,129--20,133 | 185 | 203 |
| 66 | 20,135--20,166 | 185 | 203 |
| 67 | 20,168--20,175; 20,210--20,244 | 185--186 | 203--204 |

The split OCR ranges follow the newspaper-column extraction order around
footnotes, page headers, and continuations without assigning Coxe's notes to
Justin. The paired records deliberately do not collapse OCR into facsimile,
decide among later confessional interpretations, or imply a critical Greek
text.

The complete constituent segments make later work-wide examination possible,
but their presence does not assert that any publication searched, read, or
verified the whole apology. Each publication must still bind the exact
passages it used and retain its local evidentiary role, interpretation,
sufficiency judgment, and qualifications.

## Consumer integration and claim calibration

Six publications now reuse the normalized constituent:

- `articles/faith/the-due-return`;
- `liturgy/roman-rite/1962/ordinary/00-ordinary-of-the-mass`;
- `liturgy/roman-rite/postconciliar/2008-latin-2011-us-english/ordinary/00-order-of-mass`;
- `theology/mariology/rosary`;
- `theology/sacraments`; and
- `theology/sacraments-at-a-glance`.

Each publication binds the complete OCR segment only as a cataloged and
acquired lead. Those six bindings make the larger constituent discoverable
without claiming a whole-work search or inspection. Passage-level OCR and
facsimile bindings are symmetric: chapter 61 has three consumers, chapter 65
has five, chapter 66 has four, and chapter 67 has six. The eighteen OCR
passage bindings remain inspected locator aids; the matching eighteen
facsimile bindings are the verified direct witnesses. Together with the six
complete-segment leads, the proof adds forty-two publication bindings.

Consumer comparison found and corrected four material overstatements:

- the 1962 history now attributes Malachi 1:11 reception to the *Didache*
  rather than to Justin and uses only Justin 65 and 67;
- the postconciliar matrix no longer says Justin identifies the president as
  receiving before distribution;
- the sacramental treatise says “presidential and diaconal ministry” and does
  not infer the president's ordination status; and
- the shared baptism summary assigns pouring to the *Didache*, regeneration
  and Trinitarian washing to Justin, Paschal immersion to Cyril, and Christ as
  principal minister to Augustine rather than blending the witnesses.

Rendered reference lists distinguish the Dods--Reith Buffalo 1887 artifact
from New Advent's later Kevin Knight--revised presentation.

## Reverse use, impact, and mutation proof

Reverse-use inspection confirms the expected chapter fan-out above on both
representations. At the shared-container level, the OCR artifact reaches
thirty-three publication bindings and twelve descendant source records; the
facsimile reaches twenty-five publication bindings and the same twelve
descendants. Both reach seven publications because the prior Irenaeus proof
and this Justin proof correctly share the anthology artifacts. The eight
additional OCR impacts are two existing Irenaeus segment leads and six new
Justin complete-segment leads; no publication binds a facsimile segment as if
it had inspected the complete work.

Three isolated copies of the source tree tested branch-specific staleness with
valid metadata-only mutations:

- changing Justin chapter 67's OCR passage invalidated exactly its six
  consumer fingerprints;
- changing the shared ANF OCR artifact invalidated exactly thirty-three
  fingerprints across both constituent families; and
- changing the shared ANF facsimile artifact invalidated exactly twenty-five
  fingerprints across both constituent families.

Each mutated tree failed only on the expected fingerprint requirements. The
unmodified source graph validates.

## Publication and acceptance results

Claim corrections, source records, bindings, and generation metadata received
settled and forced deterministic builds. Review rasters and contact sheets were
generated through `scripts/pdf-review`, and every one of the 242 rendered pages
was visually inspected. One independent pass found a short split in the
postconciliar “One Eucharistic Prayer” callout; a local page-space guard moved
the complete box to page 35, after which fresh full-page and downstream
contact-sheet review passed.

| Publication | Pages | Installed PDF SHA-256 |
| --- | ---: | --- |
| *The Due Return* | 14 | `4728bfe336ad7f5984d0c0c027b33b2c04c95e35666c2bc9a22443391a6a6664` |
| 1962 *Ordinary of the Mass* | 42 | `5f813ba5c135b8171305081780308d10d39f5c9127d5375c404f5f8ff253ee9d` |
| Postconciliar *Order of Mass* | 77 | `6622f7fac4b364d1d8321d662f37524f73a06eea11e8c708cbf1716b1018580a` |
| *The Rosary* | 28 | `13b681d49a80f54b25fd9e48c5a727681e06884308a7705460425135c3062548` |
| *The Seven Sacraments* | 71 | `ad94b6c4330e71e258a18239074598892745a59039870193bf08a063cbabde6e` |
| *The Seven Sacraments at a Glance* | 10 | `9abffab8b97bf7139430cc7ae80bba109adf0df374653db07da8a3c79c39f04c` |

The final graph validates with 38 artifacts, 4 corpora, 26 editions, 78
passages, 10 segments, 17 works, and 320 bindings. `make check-sources` passes;
the source-library, inventory, and family-migration suites pass all 85 tests.
The reviewed family ledger assigns the anthology-container presence to seven
publication owners and the Justin constituent presence to its six consumers,
with every retained `trace-scan` path replayable under the recorded patterns.
Each installed PDF is byte-identical to its reviewed build. These are internal
source and production checks, not external specialist or ecclesiastical
approval, and no release clearance is claimed for the changed bytes.
