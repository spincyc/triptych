# Dignitatis humanae and AAS 58 Reuse Review

Reviewed on 2026-07-23.

This record documents the bounded normalization of *Dignitatis humanae*
within `family.vatican-ii.acts` and its reuse of the volume 58 component of
`family.acta.aas-ass`. It makes complete official witnesses centrally
identifiable for later expansive examination, binds current publications only
at the passages they actually use, and proves cross-publication propagation by
mutating run-local copies of the real source graph. The canonical manifests
and publication-local bindings remain the machine-enforced records.

## Identity boundaries

The graph distinguishes the declaration from its expressions and container:

- *Dignitatis humanae* is one intellectual work, solemnly promulgated on 7
  December 1965 and comprising numbered articles 1--15;
- the dated English and Latin Vatican web states are separate editions and
  exact HTML artifacts;
- the Latin constituent printed in *Acta Apostolicae Sedis* 58 (1966) is a
  separate edition represented as one segment of the existing exact volume
  artifact; and
- *Acta Apostolicae Sedis* volume 58 remains an official-gazette container
  containing many distinct acts, not another identity for the Declaration.

The English web response contains the complete numbered body and consolidated
notes, but no promulgation or subscription material. The Latin web response
also contains the promulgation formula and date and a partial subscription
block ending with Cardinal Callori di Vignale. The remaining subscriptions and
final attestations printed in the *Acta* are absent. Those delivery differences
remain explicit instead of being collapsed into one generic “Vatican text.”

## Exact artifacts, extent, and rights

Three exact Holy See artifacts control the normalized records:

| Artifact | Extent | SHA-256 |
| --- | ---: | --- |
| English *Dignitatis humanae* HTML response | 42,080 bytes | `0ce2da9b19709aebb79da3d4110bb5b7dd18234c27adf629dd01724eb0bffd61` |
| Latin *Dignitatis humanae* HTML response | 44,177 bytes | `1e87183e8fa26cd5c7e5d40aff48fe640f6e9a9db53dc346bfc89375bff26611` |
| Holy See AAS 58 OCR PDF | 1,279 pages; 5,944,403 bytes | `69c27224cde7f27547e18c544f5b99064793ada9509ebc902b20fa548e15bac8` |

The Vatican archive, press, and content-delivery aliases recorded by the
artifact manifests returned byte-identical responses where available and
tested. The complete AAS constituent begins with its heading and article 1 on
printed p. 929. Article 15 ends and the promulgation material begins on p. 941;
subscriptions and attestations continue through p. 946. The next decree begins
on p. 947. These boundaries were checked against the exact artifact. Its OCR
remains a locating aid rather than an independently authoritative
transcription.

The Vatican portal's legal notice did not establish repository redistribution
permission. All three artifact identities are therefore `restricted` and
nonretained: the repository stores exact hashes, byte or page extent,
provenance, boundaries, and dependency records, but not the payloads.

## Expansive availability and bounded use

The complete dated English and Latin web states and complete Latin AAS
constituent are centrally identifiable for later work-wide examination. That
availability does not imply that every consumer inspected or relied on the
whole Declaration.

The reusable English passage records cover articles 1--15, 1--3, 4--7, and
10--13. The complete-text node is centrally verified but has no publication
binding. The three narrower records govern claims about duties toward truth
and civil immunity, religious communities and public order, faith's freedom
and noncoercive witness, contrary Christian conduct, and the freedom of the
Church. The AAS branch separately records the complete numbered Latin body.
No publication is represented as using the Latin or AAS witness merely
because those witnesses are available centrally.

Article 3 note 3 cites Thomas Aquinas, *Summa theologiae* I-II, q. 91, a. 1
and q. 93, aa. 1--2. That source-of-source relation is recorded as a discovery
lead; it does not make a publication using *Dignitatis humanae* a direct
consumer of Thomas or certify that the publication inspected the underlying
passages.

## Reviewed consumers and publication follow-up

Eight binding rows across five publications now share the normalized English
identities:

- the natural-law article uses articles 1--3, 4--7, and 10--13 as official
  doctrinal controls;
- the council article uses articles 1--3 to distinguish civil immunity from
  indifferentism and continuing duties toward truth;
- the Freemasonry article uses articles 1--3 for the same civil/doctrinal
  distinction without treating the Declaration as evidence about the
  canonical prohibition itself;
- the Aquinas biography uses articles 1--3 and 10--13 only as later reception,
  not as a historical witness to Thomas; and
- the heresies reference uses articles 1--3 as a later positive doctrinal
  control, not as the target-side censure instrument for nineteenth-century
  indifferentism.

No bibliography-only publication, shared-section importer, or companion
inherits use. References to religious liberty in the Bellarmine and Tertullian
biographies, the SSPX history, and a 1962 proper remain excluded because their
claims do not actually depend on this source.

The review also surfaced two reader-facing citation defects for a later
content revision. The natural-law reference combines the Declaration and
*Gaudium et spes* but supplies loci only for the latter. The heresies
bibliography omits the Declaration even though its body and audit records use
articles 1--2. Neither defect changes the publication-local evidence
dependency recorded here; both should be corrected with their rendered PDFs
in a separately reviewed content revision.

## Reverse use and mutation proof

The unmodified graph validates. Eight isolated copies of the actual source tree
then received valid metadata-only mutations:

| Mutated node | Stale fingerprints | Publications | Unexpected diagnostics |
| --- | ---: | ---: | ---: |
| English *Dignitatis humanae* artifact | 8 | 5 | 0 |
| English articles 1--15 passage | 0 | 0 | 0 |
| English articles 1--3 passage | 5 | 5 | 0 |
| English articles 4--7 passage | 1 | 1 | 0 |
| English articles 10--13 passage | 2 | 2 | 0 |
| *Dignitatis humanae* work | 8 | 5 | 0 |
| Latin AAS articles 1--15 passage | 0 | 0 | 0 |
| Existing AAS 58 container artifact | 1 | 1 | 0 |

The passage mutations invalidate only their exact verified consumers. The
English artifact and work mutations reach all eight verified rows in five
publications. Mutating the complete English passage or the Latin AAS passage
reaches no publication, proving that expansive storage does not falsely become
publication use. The AAS 58 mutation reaches the one existing publication
binding that depends on that shared container: La Salette's separate p. 445
Index notification. It does not turn any *Dignitatis humanae* consumer into an
AAS-based consumer.

## Acceptance results

No rendered source changed. The canonical manifests, publication bindings,
family ledger, and this proof record are non-rendering inputs under the
repository contract, so no PDF rebuild or installed-PDF change was required.

The completed source graph contains 51 artifacts, 4 corpora, 52 editions, 137
passages, 21 segments, 28 works, and 483 bindings. The family ledger assigns
all new identities to `family.vatican-ii.acts` while reusing the already
canonical AAS 58 artifact owned by `family.acta.aas-ass`. Remaining conciliar
acts and the separate complete sixteen-document search corpus stay open for
later proofs. These are internal source and production checks, not external
specialist or ecclesiastical approval.
