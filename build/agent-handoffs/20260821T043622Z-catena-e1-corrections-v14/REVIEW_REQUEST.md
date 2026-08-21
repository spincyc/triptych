# Review request — E1 Catena correction V14

This asks only what needs judgment from outside this lane. Everything this lane
believes it proved is in `CLAIM-CLOSURE.md` with its evidence, and the figures
are in `checks.txt`; neither is repeated here.

## Blockers

1. **The V13 review this lane answers has no published ref.** `origin` carries
   no `review/catena-wave-1-e1-corrections-v13-independent`. A branch of that
   name exists only in a local reviewer checkout, standing at the reviewed head
   `6cc85e1a1dea317a48c0bfcfd6f774201ea3a6c3` with no review commit on it. So
   this lane's account of the disposition, its findings and its exact next
   action cannot be checked against the review itself. Every earlier lane in
   this series named a review SHA; this one cannot. Is the correction
   nevertheless reviewable on its own terms — the parent replay, the read
   counts, the identity roster and the sinks are all reproducible without the
   review — or must the review be published before a V14 disposition can be
   recorded?

2. **An accessor at a nested source key now makes the whole chapter
   unreadable.** V13 invoked the getter for voices and editions and declined it
   for fragment provenance; the review named the contradiction and required one
   authority rule. This lane chose the stronger of the two rules — decline by
   descriptor, never invoke — which means a member the page cannot read makes
   the chapter unreadable, exactly as an unreadable `sources` root already did.
   That is fail-closed and coherent, and it is also a semantic widening: data
   that V13 rendered (with an empty provenance line) now renders as "the
   commentary record did not load". No tracked corpus record uses an accessor,
   so the sample corpus is unaffected. Is fail-closed the right side of that
   trade, or should an accessor-backed source be dropped as one unreadable
   member while its siblings stand?

3. **A row this model did not project resolves no address.** `textAsked`
   refuses an address to any object not in the row registry, which closes
   ownership but also means a caller holding a *copy* of a projected row — the
   replay harness's own `forceRow` does exactly this — resolves nothing. That is
   deliberate and it is the mechanism the ownership proof rests on. Is refusing
   the copy correct, or should the model resolve an address for any row whose
   fields it would have produced?

4. **The mutation half of the immutability probe runs for one scenario.**
   Freezing is read-only and reported everywhere; the thirteen real assignment
   attempts run only for `v14-authority-graph`, because at the parent an
   unfrozen lead or blocked entry really does move and a probe running on every
   snapshot would plant its own evidence across the file. Is one scenario
   enough for the mutation claim, or should the probe run wherever the
   structure exists and restore in every case?

## Optional feedback

- `chapterWitness` is a test-only observation seam in production code. With no
  recorder installed every call is one `if` on a `null` and the page's
  semantics are unchanged, and `guidance/external-review-handoffs.md` says
  nothing about test hooks in shipped browser sources. Is the seam acceptable
  where it stands, or does the identity proof belong somewhere the page does
  not carry?
- The unbudgeted model grew again, 36,679 to 39,724 gzipped whole. This lane
  discloses it and does not raise a ceiling. Whether the model and the combined
  route payload need a governed ceiling remains the budget owner's question,
  and it has now been carried forward by four lanes.
