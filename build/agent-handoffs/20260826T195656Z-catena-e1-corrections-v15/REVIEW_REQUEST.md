# Review request — E1 Catena correction V15

**A fresh independent review is asked for, at the candidate head of
`impl/catena-wave-1-e1-corrections-v15`, against the exact parent
`69f2575421ba976271c936b1abd4b39dbe8b98fd`.** Nothing in this package records
an acceptance, and no disposition is claimed by it. The review this lane
answers is `0d11766ec232b2b4e46a7d1b0ada56ef22370004` on
`review/catena-wave-1-e1-corrections-v14-independent`, which answered
**CHANGES REQUIRED**.

This asks only what needs judgment from outside this lane. Everything this
lane believes it proved is in `CLAIM-CLOSURE.md` with its evidence, the
figures are in `claims.json` and `DERIVED-CLAIMS.md`, and the commands are in
`checks.txt`; none of them is repeated here.

## Blockers

### 1. Ownership through pending transport, completion and body application

The defect was that ownership held at address resolution and was lost
immediately after it: the resolved path went to a module-scope map keyed on
the path, holding the unresolved promise, and a second row at the same address
was handed the first row's answer. The shape chosen here is an owner object —
`M.rowTransport(row)`, one frozen owner per projected row, carrying the row,
the projection that made it and the address it asks — with the record taken at
the sink by `M.bodyAsked(row, content)`, which names the projection, the row
and the value written.

Two questions, and they are separable.

**Is the owner object the right identity to hold work against?** It closes
reconstruction-by-path, which is what leaked. It also means nothing outside
the projection can ask about work at an address at all, and it inherits the
previous lane's copy-refusal rule: a row this model did not project gets no
owner, so a caller holding a *copy* of a projected row starts no transport and
applies no body. That rule was a blocking question in the previous review and
is unchanged here; it now governs three more operations than it did.

**Is recording at the sink acceptable in shipped bytes?** `M.bodyAsked` is
asked at the body application in production code, not in the harness, for the
same reason the previous lane's identity recorder was: a record taken beside
the effect proves what the consumer received, and a record taken in a harness
proves what a second call returns. That argument has now been used twice to
put an observation seam into a shipped browser source. Is it still the right
trade, or does the ownership proof belong somewhere the page does not carry?

### 2. Same-path isolation, and genuine lateness

The rule is that a path may key only a **settled** answer, and the map
receives the promise from inside that promise's own settle handler, so no
unresolved value is reachable by path at any instant. Two consequences are
deliberate and both are judgment calls.

**Concurrent same-path requests are no longer deduplicated.** Two owners at
one address do two pieces of transport where the parent did one. Sharing
in-flight work by path is the exact mechanism that leaked, so it was removed
rather than repaired. On the tracked corpus the cost is nil — no chapter of
the 562 holds two fragments on one text address — so the question is about a
corpus this project may later hold, not about today's pages. Is removal
the right answer, or should in-flight sharing be reintroduced keyed on
something that cannot be reconstructed from the address — with the isolation
then resting on that key rather than on the absence of sharing?

**The first settled answer at a path is not displaced by a request released
later.** A slow request resolving after a fast one leaves the standing answer
alone. Is first-settled-wins correct for this page, or should a genuinely late
answer be allowed to replace an earlier one — and if so, under whose
ownership does the replacement render?

### 3. Safe sharing of a fulfilled immutable value

The closure is a rule about *what* may be shared, not a ban on sharing.
A settled, immutable value with no owner-specific content is shared
deliberately: the substitute record the page uses for a spine it cannot read
is created once per name and reused across rows and projections, and the
settled path map hands the same fulfilled body to a later asker rather than
retrieving it again.

Is the immutability-and-no-owner-specific-content boundary sufficient? The
finding this lane answers is precisely a case of sharing something outside
that boundary, so the boundary is doing real work and a reviewer should test
it rather than accept it. Specifically: is per-name reuse of the substitute
record right, or should each projection mint its own so that no object at all
crosses a projection edge?

### 4. Exact reproducible evidence and provenance

The previous review found eight defects in the evidence, enumerated in
`PROVENANCE.md`; six of them are defects in the pipeline's own tools, and they are
fixed here rather than explained: two browser-gate commands recorded
`ELIDED`; the load-bearing parent-replay command recorded `PROSE`;
`logs/compare-gate.py` labelled unexecuted despite its own assembly transcript; a
combined `16`-and-`11` label mixing invocation rows with unique-tool rows; a history claiming
`complete` and `append-only` while omitting a set-aside cohort and the P10
rows and while disclosing a row replacement; and a mechanical `COMPLETE`
verdict that tested none of those. The root causes were the capitalised
English word `JSON` inside a quoted `echo` note the battery composes — not a
filename, and not the exempt `$WORKSPACE` and `$EVIDENCE` symbols — and `cp`
missing from the classifier's list of command heads.

**Is the command record now readable end to end?** The specific ask is that
the reviewer confirm from `checks.txt` that no command is elided or described
as prose where its text can be shown, that the parent replay in particular is
recorded verbatim, and that the executed-tool accounting counts one kind of
row. A classifier that was wrong about three commands may still be wrong about
a fourth, and this lane's own verdict on it is not independent.

**Is the corrected history's disclosure complete?** This lane set no cohort
aside, and nothing in its ledger has been taken out or rewritten; it says so
where the previous package could not.
It did retire one attempt ledger — the batteries were started once against a
head a records correction then superseded — and `PROVENANCE.md` and
`LIMITATIONS.md` state that, with the retired file's byte count and digest, and
state that no figure in this package comes from it. The post-seal rows now
reach the ledger slice beside the archive; the member sealed inside it is
written before those rows exist and cannot be reopened without rewriting a
sealed archive, so that boundary is structural and stated rather than fixed. Is
that disclosure the right disposition, and is a retired ledger disclosed by
digest an acceptable substitute for one that was never opened?

## Optional feedback

- **Three paragraphs of page prose were relocated into the unbudgeted model**
  to hold `src/web/browser/catena/catena.js` under a 13,000 gzipped ceiling with 28 bytes of headroom
  at the parent: why a 200 that is not a spine is not an empty chapter, why
  neither the paragraph layer nor its index may decide the page, and what the
  absence disclosure may say. One-line pointers stay behind. No ceiling was
  raised. Whether the page or the model is the right home for that prose is a
  judgment this lane made under a budget, and it is disclosed in
  `LIMITATIONS.md` rather than presented as neutral.
- **The observation claim is deliberately narrower than the previous lane's
  prose implied.** What is claimed is that no consumer runs a hostile value
  accessor and no consumer reaches past the projection to observe the record
  again — not that the record is observed once. `Object.hasOwn` is counted as
  an observation because it is `[[GetOwnProperty]]`, which is why the per-key
  figure is three. Confirmation that this is the right claim, or a correction
  to it, is welcome.
- **Two vectors close proof gaps rather than defects.** The nested EDITION
  accessor case and the observation accounting both pass at the parent. They
  are recorded as coverage, and the eight new methods that pass at both
  endpoints are recorded the same way. If any of them reads as a claimed
  closure anywhere in this package, that is a defect in the package and worth
  naming.
- **The unbudgeted model grew again**, 39,724 to 41,077 gzipped whole. This
  lane discloses it and raises no ceiling. Whether the model and the combined
  route payload need a governed ceiling remains the budget owner's question,
  and it has now been carried forward by more lanes than have answered it.
