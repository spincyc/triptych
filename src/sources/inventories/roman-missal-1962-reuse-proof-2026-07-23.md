# 1962 Roman Missal Passage-Reuse Proof

Reviewed on 2026-07-23.

This record documents the first multi-publication passage-reuse proof for
`family.roman-missal.1962`. It supplements the migration ledger. It is not a
source manifest, does not create a binding, and does not promote a publication
merely because its legacy records cite the same edition or artifact.

## Boundary and witness decision

The proof is deliberately limited to the complete Pentecost Sequence,
*Veni, Sancte Spiritus*. The canonical library identifies the Vatican typical
1962 edition and an exact CMAA facsimile PDF by byte length and SHA-256. The
facsimile remains remote because its rights status is unresolved; no source
payload is added to the repository.

The complete sequence, including its printed beginning and ending, was visually
checked at printed page 357, artifact PDF page 438, leaf 437. The checked source
controls received wording and passage boundary. The curriculum's analytical
three-line stanza display, omitted print accents, translation, scansion, and
attribution remain separately identified course apparatus rather than source
features.

The shared passage fingerprint is
`sha256:245badad1d1a62153cc9ac0858dabaaae4606b1c214ab2a703330464b7554042`.

The Benziger *iuxta typicam* edition remains a distinct canonical edition with
distinct artifacts. This proof makes no claim of identity between its page
presentation or paratext and the Vatican typical facsimile.

## Consumer review

Two Ecclesiastical Latin publications now bind the same passage identity:

1. `curriculums/ecclesiastical-latin/04-advanced/poetry/06-rhythmic-hymnody-and-sequences`;
2. `curriculums/ecclesiastical-latin/04-advanced/poetry/07-poetic-commentary`.

Both already imported one authoritative shared received-text macro for the
complete sequence. Their reviewed artifact-level bindings were retargeted to
the exact passage without changing rendered text, local analytical purpose, or
publication ownership.

Other Missal consumers were not promoted merely to enlarge the reuse count.
The P5 module uses only a bounded middle selection. P8 uses the complete
sequence as an analogue in a different teaching task. M16 uses only its first
four lines, while M18 and Review III bind complete formularies rather than this
passage alone. Each remains a later, separately reviewable passage or
publication-binding decision.

The Ascension novena was also excluded. Its controlling sequence witness is
the 2005 *Compendium Eucharisticum*, not this Missal artifact.

## Acceptance proof

The source graph validates with both consumers sharing the passage fingerprint.
Reverse-use lookup on the passage returns exactly those two publications, while
impact lookup from the controlling artifact reaches the passage and both
consumers.

The generic two-consumer invalidation regression proves the schema mechanism.
This migration additionally replays that mutation against a run-local mirror of
the actual graph: changing valid shared passage metadata must produce exactly
two stale diagnostics, one for each real consumer, with one common replacement
fingerprint.

No rendered publication source or installed PDF changed. The proof registers
one exact remote-PDF passage and promotes only the two publication-local
bindings whose existing evidence and imported text match that boundary.
