# Isaiah relation repair and proper-study chronology

Status: corpus correction independently reviewed and adopted; consumer
artifacts remain under repair. This is not acceptance of the revised
publications.

## Independent source review, 21 September 2026

A fresh reviewer with no authoring history inspected the frozen handoff
`build/agent-handoffs/20260921T141201Z-isaiah-relation-repair` (directory and
verified ZIP) against the complete retained article texts of Souvay (1910),
Jacquier (1911) and Durand (1912) and the complete freshly acquired NABRE
Isaiah, Matthew and Psalms introductions, whose hashes it verified against the
new artifact records. All four blocking questions resolved in the
correction's favor:

1. The traditional-attribution repair is supported: Souvay's 740–701 B.C.
   bounds the ministry (with his own hedged "appear to be"), his collection
   hypothesis is tentative and limited to chapters 1–35, and the 1908
   Pontifical Biblical Commission response grounds the whole-book
   attribution. The ministry era is re-related, not rewritten.
2. The NABRE horizon supports the chapters 40–55 scope, the `prophecy-given`
   relation, and the before-return anchor used for existence only, with no
   invented endpoint; the source's "generally attributed" hedge is retained.
3. The critical Matthew bound preserves the source's probabilistic frame
   (post-A.D. 70, probably at least a decade later, no minted endpoint); the
   traditional composition alternatives are byte-untouched, and each recorded
   qualification is verbatim in Jacquier and Durand.
4. The consumer boundary is complete at the frozen base: Claude PC-S51-A's
   record and annotations were the only committed consumers; historical
   ledgers correctly remain unrewritten. The reviewer added one derived-
   artifact remark: the installed Claude PC-S51-A web edition still renders
   the withdrawn composition label and must be regenerated at republication
   as part of the consumer repair.

The reviewer's limits: it did not re-run the test suite (whose results the
package records), collate facsimiles, or re-fetch the USCCB pages over the
network. Its verdict adopts the corpus data only; publication acceptance for
every affected dossier, PDF and web edition remains a separate, pending gate.

## Defect and correction

`composition.book-of-isaias` returned 740–701 B.C. over the whole book,
although its own note admitted that these were ministry dates. Charles
Souvay's *Isaias*, *Catholic Encyclopedia* VIII (1910), distinguishes the
ministry in **Life** from the collections discussed later. The tentative
collection hypothesis concerns the first collection, chapters 1–35. It cannot
date Isaiah 55 or the completed book.

The unit is withdrawn. The same source label now belongs to
`israel.prophets.isaias-traditional-era`, bound to the book under
`traditional-attribution`. The subject explicitly identifies the ministry.
The end is an apparent last prophecy, not the prophet's death. Existing
narrated-event and prophetic-referent bindings remain unchanged.

The inspected witness is the retained article-text extraction:
`artifact.catholic-encyclopedia.volume-8.new-york-1910.newadvent-08179b-d4ee13fd-article-text`.
The whole article was read, especially **Life**, **First Isaias**, and
**Second Isaias**. No fresh facsimile collation is claimed.

## Separate critical evidence

The complete official NABRE Isaiah, Psalms and Matthew introductions were
freshly acquired and read on 21 September 2026. Exact response identities,
retrieval limits and summaries are under the source library's
`2026-09-21-english-usccb-web` edition. Protected payloads are not tracked,
included in handoffs, or copied into publication bodies.

- Isaiah: the source generally attributes chapters 40–55 to an anonymous
  poet prophesying toward the end of the Babylonian exile. The new
  `israel.exile.second-isaias-oracles` binding uses `prophecy-given`, not
  composition. Its open boundary is anchored to the return from captivity;
  no absolute year is borrowed from that event. Independent review must
  specifically assess that anchor and the scope.
- Matthew: `critical.gospel-of-matthew` holds the source's post-A.D. 70
  composition boundary. Its probable later-decade qualification and
  probabilistic argument remain explicit. The traditional profile and the
  default cascade's traditional composition alternatives are unchanged.
- Psalms: fresh inspection corroborates the existing pre-Maccabean limit.
  It establishes neither precise individual dates nor a final-assembly date.
  The older corpus source pin is not silently replaced by the new retrieval.

## Matthew's traditional alternatives

Jacquier's **Time and place of composition**, in the retained 1911 article,
and Durand's **The New Testament**, in the retained 1912 article, were
reinspected. Their qualifications already live in the corpus and must be
visible in the revised dossiers:

- about 40–42 depends on an admittedly unreliable dispersal tradition;
- about 60–68 is a conditional alternative reckoning;
- about 64–67 comes from an interpretation of Irenaeus that Jacquier calls
  inconclusive;
- 40–45 reports Catholic scholarship in 1911, not today's consensus;
- about 50 concerns Durand's Aramaic original; he leaves the Greek rendering
  undated.

## Consumer boundary

Searching current source files outside `evaluations/` for the withdrawn unit
identifies one existing publication consumer: Claude PC-S51-A, in its
`research/chronology.toml` and `research/chronology-annotations.tex`. Its
scope and source bindings also describe the misclassified claim. Both its
expansive and concise dossiers consume those annotations and require fresh
review and rebuilds. The new GPT PC-S51-A dossier is not an existing consumer
and must be independently authored and reviewed.

The current executable seam is `_proper_chronology.py` and its postconciliar
input adapter. No browser renderer imports `_chronology` directly.
`coverage.tsv` and the pinned profile-contract re-review manifest are derived
current views and are regenerated. Prior correction tables, cold-review
reports, immutable acceptance packets and inert GPT proposal archives remain
historical evidence, not current approvals, and are not rewritten.

The four proper-study leaves also need the source-specific Matthew
qualifications and adequate geography. New dossiers and their publication
reviews remain open; corpus validation alone does not meet those obligations.
