# City of God Passage-Reuse Proof

Reviewed on 2026-07-23.

This record documents the first multi-publication reuse proof for
`family.augustine.de-civitate-dei`. It supplements the migration ledger. It is
not a source manifest, does not create a binding, and does not promote a
publication merely because its legacy records cite the same work.

## Boundary and witness decision

The proof is deliberately limited to *City of God* 10.5--6. The canonical
library already retains and fingerprints:

- the complete 1871 English edition edited and translated principally by
  Marcus Dods;
- the complete 1899--1900 Hoffmann CSEL 40 Latin edition in TEI; and
- one inspected 10.5--6 passage in each edition, including both complete
  chapter bodies and their recorded apparatus or detached notes.

The publications originally used the later NPNF/New Advent English
presentation. That is a distinct witness. The retained 1871 Dods passage and
the CSEL Latin passage were therefore read anew against each publication's
actual claim. They supplement and control the legacy witness; they do not
silently replace it or alter the reader-facing citation.

The shared source fingerprints are:

| Passage | Fingerprint |
| --- | --- |
| Dods 1871, 10.5--6 | `sha256:656887cdeca9dd94a0c1de3e15400368956fa27922c7e981ce60aa90688d671c` |
| Hoffmann CSEL 40, 10.5--6 | `sha256:f6e1e889bb4f2198ccebab9d7119d2edb9160c51892a0bc4fc9b8a202ab617b4` |

## Consumer review

Six publications now bind the same two passage identities:

1. `articles/faith/the-due-return`, the original tracer consumer;
2. `liturgy/roman-rite/1962/propers/temporal/39-trinity-sunday`;
3. `liturgy/roman-rite/1962/propers/temporal/41-second-after-pentecost`;
4. `liturgy/roman-rite/1962/propers/temporal/45-fifth-after-pentecost`;
5. `liturgy/roman-rite/1962/propers/temporal/47-seventh-after-pentecost`; and
6. `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s26-most-holy-trinity-year-a`.

The five newly promoted consumers use the passage as bounded doctrinal
illumination, not as direct commentary on their liturgical formularies. The
review checked the claims about visible and interior sacrifice, divine
non-need, mercy, bodily and personal offering, the renewed mind, the redeemed
city, and Christ the High Priest against the exact retained witnesses and
their complete chapter context.

`liturgy/roman-rite/1962/propers/temporal/49-ninth-after-pentecost` retains a
catalog-only work binding. Its research scope names 10.5--6 as a broad control,
but the rendered guide does not rely on that source. It was not promoted merely
to enlarge the reuse count.

Four promoted publications also cite 10.20. That locus remains a separate
catalog-only work binding until an exact 10.20 passage is registered and
reviewed. The 10.5--6 fingerprint therefore cannot be mistaken for coverage of
the combined citation.

## Acceptance proof

The source graph validates with all six consumers sharing each passage
fingerprint. Reverse-use lookup on either passage returns the six reviewed
publications, while impact lookup from the controlling artifact reaches the
passage and the same consumers without changing their publication-local roles
or interpretations.

The generic two-consumer invalidation regression already proves the schema
mechanism. This migration additionally replayed it against a run-local mirror
of the actual graph. Changing valid shared passage metadata produced exactly
six stale diagnostics, one for each real consumer, and every diagnostic
required the same replacement fingerprint.

No source bytes, canonical manifests, rendered publication text, or installed
PDF changed. The proof promotes only publication-local evidence bindings and
preserves every legacy audit and citation during the dual-record migration.
