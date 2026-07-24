# Gaudium et spes and AAS 58 Reuse Review

Reviewed on 2026-07-23.

This record documents the completed bounded normalization of *Gaudium et
spes* within `family.vatican-ii.acts` and its reuse of the volume 58 component
of `family.acta.aas-ass`. It makes complete official witnesses centrally
identifiable for later expansive examination, binds current publications only
at the loci they actually use, and proves cross-publication propagation by
mutating run-local copies of the real source graph. The canonical manifests
and publication-local bindings remain the machine-enforced records.

## Identity boundaries

The graph distinguishes the pastoral constitution from its expressions and
container:

- *Gaudium et spes* is one intellectual work, solemnly promulgated on 7
  December 1965 and comprising numbered articles 1--93;
- the dated English and Latin Vatican web states are separate editions and
  exact HTML artifacts;
- the Latin constituent printed in *Acta Apostolicae Sedis* 58 (1966) is a
  separate edition represented as one segment of the existing exact volume
  artifact; and
- *Acta Apostolicae Sedis* volume 58 remains an official-gazette container
  containing many distinct acts, not another identity for the Constitution.

The English web response includes the preliminary note explaining the
Constitution's two parts, the complete numbered body, and consolidated notes,
but omits the promulgation and subscription material. The Latin web response
also includes the promulgation formula and date, legal-vacation notice,
subscriptions, and final attestations. Those delivery differences remain
explicit instead of being collapsed into one generic “Vatican text.”

## Exact artifacts, extent, and rights

Three exact Holy See artifacts control the normalized records:

| Artifact | Extent | SHA-256 |
| --- | ---: | --- |
| English *Gaudium et spes* HTML response | 238,757 bytes | `23b935b99bdaa1cd8bc5ee0951f418672d1d246d008d026ada56e1d01861c12d` |
| Latin *Gaudium et spes* HTML response | 231,512 bytes | `bc2b1022686fb3a6dc6e1afebc244569abe133bd554999dfbe9dfdccf57b73f5` |
| Holy See AAS 58 OCR PDF | 1,279 pages; 5,944,403 bytes | `69c27224cde7f27547e18c544f5b99064793ada9509ebc902b20fa548e15bac8` |

The Vatican archive, press, and content-delivery aliases recorded by the
artifact manifests returned byte-identical responses where tested. The
complete AAS constituent begins with its heading and article 1 on printed p.
1025. Article 93 ends on p. 1115, where the promulgation material begins;
subscriptions and attestations continue through p. 1120. The preceding decree
ends on p. 1024, and the next issue begins on p. 1121. These boundaries were
checked against the exact artifact. Its OCR remains a locating aid rather than
an independently authoritative transcription.

The Vatican portal's legal notice did not establish repository redistribution
permission. All three artifact identities are therefore `restricted` and
nonretained: the repository stores exact hashes, byte or page extent,
provenance, boundaries, and dependency records, but not the payloads.

## Expansive availability and bounded use

The complete dated English and Latin web states and complete Latin AAS
constituent are centrally identifiable for later work-wide examination.
That availability does not imply that every consumer inspected or relied on
the whole Constitution.

The reusable English passage records cover articles 1--93, 1, 4, 11, 16--22,
27--29, 36, 42--43, 47--52, and 74--76. The complete-text node is used only as
a bounded control by the council article. Narrower records govern claims about
solidarity and the signs of the times, freedom and atheism, equal dignity,
temporal autonomy, marriage and family, and political community. The AAS
branch separately records the complete numbered Latin body. No publication is
represented as using the Latin or AAS witness merely because those witnesses
are available centrally.

The council article also makes a broader claim about the absence of the names
Communism and Freemasonry from all sixteen promulgated Vatican II documents.
This proof establishes the absence only within the exact complete English
*Gaudium et spes* body. It does not encode a `negative-search` binding: the
restricted HTML is not an exact registered plain-text search representation,
and one constitution cannot prove a sixteen-document corpus claim. A
versioned, searchable corpus of all sixteen acts remains a separate later
proof.

## Reviewed consumers and exclusions

Fourteen *Gaudium et spes* binding rows across eight publications now share
the normalized identities. Ten rows across six publications are fingerprinted
verified uses:

- the natural-law article uses articles 36 and 74--76 as official controls;
- the council article uses the complete body as a bounded control and
  articles 16--22 for its direct analysis;
- the providence article uses article 17 within the inspected 16--22 window;
- the Aquinas biography uses articles 27 and 29 as later reception;
- the postconciliar Order of Mass exposition uses articles 1, 4, and 11; and
- the Seventeenth Sunday, Year A guide uses article 22 as later doctrinal
  context rather than direct exegesis or evidence of selection intent.

Four rows preserve an honest catalog ceiling: the natural-law bibliography's
article 16 and articles 42--43 references, the heresies reference's work-level
entry, and the sacramental treatise's articles 47--52 marriage bibliography.
Central verification of those passages does not retroactively create
publication-local inspection or reliance. The sacramental at-a-glance
companion and 1962 Nuptial Mass do not import the treatise's bibliography and
therefore do not inherit a binding.

Review also qualified two local audit statements. The council article now
separates the completed within-*Gaudium et spes* check from the still-unproved
sixteen-document claim. The providence article now distinguishes what article
17 supports from the Catechism's more exact teaching on reason, will,
voluntariness, and responsibility.

## Reverse use and mutation proof

The unmodified graph validates. Nine isolated copies of the actual source tree
then received valid metadata-only mutations:

| Mutated node | Stale fingerprints | Publications | Unexpected diagnostics |
| --- | ---: | ---: | ---: |
| English *Gaudium et spes* artifact | 10 | 6 | 0 |
| English articles 1--93 passage | 1 | 1 | 0 |
| English articles 16--22 passage | 3 | 3 | 0 |
| English articles 27--29 passage | 1 | 1 | 0 |
| English article 36 passage | 1 | 1 | 0 |
| English articles 47--52 passage | 0 | 0 | 0 |
| *Gaudium et spes* work | 10 | 6 | 0 |
| Latin AAS articles 1--93 passage | 0 | 0 | 0 |
| Existing AAS 58 container artifact | 1 | 1 | 0 |

The passage mutations invalidate only their exact verified consumers. The
English artifact and work mutations reach all ten verified rows in six
publications but not the four catalog-only rows, which have no inspection
fingerprint to stale. Mutating centrally verified articles 47--52 or the Latin
AAS passage reaches no publication, proving that expansive storage does not
falsely become publication use. The AAS 58 mutation reaches the one existing
publication binding that depends on that shared container: La Salette's
separate p. 445 Index notification. It does not turn any *Gaudium et spes*
consumer into an AAS-based consumer.

## Acceptance results

No rendered source changed. The canonical manifests, publication bindings,
local research audits, family ledger, and this proof record are non-rendering
inputs under the repository contract, so no PDF rebuild or installed-PDF
change was required.

The completed source graph contains 49 artifacts, 4 corpora, 49 editions, 132
passages, 20 segments, 27 works, and 475 bindings. The family ledger assigns
all new identities to `family.vatican-ii.acts` while reusing the already
canonical AAS 58 artifact owned by `family.acta.aas-ass`. Remaining conciliar
acts and the separate complete sixteen-document search corpus stay open for
later proofs. These are internal source and production checks, not external
specialist or ecclesiastical approval.
