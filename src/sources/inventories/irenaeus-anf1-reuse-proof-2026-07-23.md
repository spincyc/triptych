# Irenaeus ANF Volume 1 Reuse Review

Reviewed on 2026-07-23.

This record documents the bounded canonicalization and reuse proof for
`family.irenaeus.adversus-haereses-anf1-1887`. It supplements the family
ledger and does not itself create a source identity, evidence state, or
publication binding. The broader `family.patristics.anf-npnf-schaff` series
remains unresolved; this proof covers only the Roberts--Rambaut English
*Against Heresies* as printed in ANF volume 1 at Buffalo in 1887.

## Container, constituent, and exact artifacts

The source model preserves two identities that a flat bibliography would
conflate:

- *The Ante-Nicene Fathers*, volume 1 is the anthology container and owns the
  exact digitized artifacts; and
- Irenaeus's *Adversus haereses* is the constituent work, with the
  Roberts--Rambaut English as its own translated edition linked to bounded
  segments of those container artifacts.

The scanned title leaf prints Buffalo, 1887; the following leaf carries an
1885 copyright notice. The translation attribution at printed p. 310 says
that Alexander Roberts translated Books I--II and that William H. Rambaut
supplied the groundwork for Book III and the continued portion of Book IV.
Coxe's American editorial matter remains distinct from Irenaeus's text.

The complete translated body, from its heading through the last note before
the separately collected fragments, is bounded in two exact representations:

- the tracked 3,551,901-byte Internet Archive raw OCR, SHA-256
  `12cdc519c642b446cb4c6c3ba0bad9a2288687937975df6ca4c8b42aa6d92d84`,
  physical lines 37,256--73,656; and
- the remote 58,025,655-byte Internet Archive facsimile PDF, SHA-256
  `b50e358eebf85f06794c4dba16777eb6d27a35688a6c7a828b46c9d2190be8cc`,
  artifact pages 333--585 / printed pp. 315--567.

The exact 106,256-byte automated page-number map is also tracked, SHA-256
`8ab2289d2fd18b814d4f7d6fcc18f7fceca2a5a269023fd35ca68659b301a51a`.
It makes printed-page and artifact-page correspondence reusable without
pretending that pagination metadata is a textual witness or evidence
controller.

The public-domain review supports retaining the raw OCR and factual page map.
The much larger facsimile remains remote as a storage-policy decision, not
because it is an external or second-class source. New Advent's Kevin Knight
revision is a distinct later presentation and is not treated as the same
artifact or edition.

## Passage normalization

Each used locus has two passage records:

- an inspected OCR locator whose exact physical ranges and a short
  transcription segment make raw-text search and checking reproducible; and
- a verified facsimile passage whose artifact pages control edition identity,
  pagination, wording, attribution, and visible context.

The paired loci are IV.13.1--4, IV.14.1, IV.14.2, IV.14.3, IV.17.1, and
IV.18.1--6. The pairs deliberately do not collapse OCR into facsimile or imply
a critical Greek or Latin text.

The complete constituent segments permit later work-wide examination, but
their presence does not assert that either publication searched, read, or
verified the whole translation. The publication bindings separately state
which passages were actually inspected and why.

## Reviewed consumers and claim correction

Two publications consume this exact family:

1. `articles/faith/at-the-end-of-every-why` binds IV.13.1--4 and IV.14.1 in
   both OCR and facsimile form; and
2. `articles/faith/the-due-return` binds IV.14.1--3, IV.17.1, and IV.18.1--6
   in both forms.

The shared IV.14.1 pair therefore has two reviewed consumers. Other pairs
remain claim-local to one of the two publications. Other occurrences of
Irenaeus, ANF, or NPNF are not promoted to this exact edition and passage set
without their own review.

The exact check found one substantive citation defect in *The Due Return*:
the phrase about instruction of a people “prone to turn to idols” belongs to
IV.14.3, not only to the former IV.17.1 and IV.18.1--6 citation. The article,
references, scope, audit, bindings, reviewed PDF, and installed PDF now carry
the corrected locus. A replayable literal search of the retained raw OCR for
the source's doubled-space form of `prone  to  turn  to  idols` returns exactly
one physical line, 60,907.

## Acceptance proof

The source graph validates with 34 artifacts, 4 corpora, 15 editions, 43
passages, 2 segments, 8 works, and 191 bindings. Reverse-use lookup on either
IV.14.1 passage returns exactly the two publications above. Impact lookup from
the OCR artifact reaches the OCR constituent segment, all six OCR passage
records, and nine reviewed bindings; impact from the facsimile artifact
reaches its constituent segment, all six facsimile passages, and seven
reviewed bindings.

Three run-local mirrors of the actual graph validated before mutation:

- changing valid metadata on the shared IV.14.1 OCR passage produced exactly
  two stale consumer fingerprints, both requiring the same replacement;
- changing valid metadata on the whole-volume OCR artifact produced exactly
  nine stale fingerprints across its segment and passage descendants; and
- changing valid metadata on the facsimile artifact produced exactly seven
  stale fingerprints across only the facsimile descendants.

The separate OCR and facsimile mutation results prove that a changed ancestor
invalidates every reviewed downstream use in its branch without falsely
invalidating the parallel witness branch.

Both affected publications received settled deterministic builds, clean log
and font checks, contact-sheet and all-page visual review, and exact
installation. The resulting PDFs are:

- *At the End of Every Why*: 10 pages, SHA-256
  `b71d103fe159990d37cba24373ff56fcc2f90eb09b43bb7dd0dcc8c789524e7f`;
  and
- *The Due Return*: 14 pages, SHA-256
  `5b63556bf23cea4fd2846cbfad8adf9bb0938d17111d4c6f2da0ef2bfa2315c6`.

This proof establishes first-class reuse for one constituent edition and its
current reviewed loci. It does not complete the ANF/NPNF series, inspect every
page of the anthology or constituent, establish an author-wide interpretation,
or substitute this English translation for a critical edition.
