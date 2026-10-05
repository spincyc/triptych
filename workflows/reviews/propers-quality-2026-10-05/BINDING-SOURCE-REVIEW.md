# Independent review: binding evidence in chronology seals

**Verdict: PASS.** The shared code/dependency defect RES-001 is repaired. There is no remaining blocker from this review to the driver's regeneration, validation, and fresh sealing of `research-0001`. This is a code/dependency disposition: it neither accepts the actual proper's fresh research nor grants publication approval. The old research packet must not be repaired or accepted in place.

## Reviewed snapshot

Reviewed immutable package `build/agent-handoffs/20261005T150831Z-chronology-binding-source-seal/` and its sibling ZIP. The six-file incremental patch is relative to the previously reviewed `20261005T142638Z-typed-chronology-anchor-context-rereview` snapshot; the integrated patch compares with `b373dd5db96ea67b1975b27de411cfd6cf2e1ee6`. Read HANDOFF, REVIEW_REQUEST, checks, sources, the entire incremental patch, surrounding query/filter/aggregation/trace/seal code, the pre-repair evidence, impact data, and relevant supplied logs.

All **23 current owner hashes matched** the frozen package, and `python3 -m zipfile -t` passed. The hash comparison with the prior package shows exactly the six declared owners: five changed existing files and the new binding-source test file. Dates, bindings, source records, manifest, sealed helpers, preflight, and reader renderer have unchanged hashes. Earlier frozen packages and review dispositions remain separate evidence.

## Provenance and filtering

- `Assertion.binding_sources` has a default-empty tuple and is populated at all three event-binding construction routes: normal preferred-system query, native-system query, and broad whole-Psalm fallback. Composition-unit assertions retain the empty default. The proper adapter accepts an older assertion object lacking the new field.
- Binding evidence remains distinct from `claim.sources`. The actual Psalm 118 result retains Haydock's passage only as the Davidic-attribution warrant; Corbett and his retained article remain the authorities for the reference reign dates. This repair adds no chronology assertion and does not promote a source note into a date.
- Existing scope checks precede assertion construction. Native queries retain only matching native scopes; the broad fallback excludes verse-scoped preferred-system bindings. Existing profile/answerability/cascade selection still determines the returned assertions. Nonmatching bindings and suppressed profile candidates do not acquire a new path into the seal. Preserved evidence remains inspectable only through the existing explicit evidence mode.
- Shared/native deduplication preserves its existing assertion identity and counts while unioning warrants from matching routes. Native-only routes remain separate as before. Date-claim sources are not combined by this operation.
- Proper aggregation unions binding warrants from every retained route without adding them to date identity. The common assertion intersection is unchanged: a locus-specific assertion cannot become an element-wide Date claim. Its warrant is nevertheless retained in the audit union and correctly included in research evidence. Explicit profile comparisons remain filtered to their requested subject/relation and common loci.
- The internal field is excluded from generated record and annotation payloads. The trace includes both date sources and binding warrants from the default audit claims, requested comparisons, and historical-context candidates, then uses the existing source resolver. Bible witnesses remain explicit `source_files`; library identifiers remain in the cited-source list.

## Actual automatic source closure

Independently called the real `_proper_study.chronology_reads` for the upcoming GPT proper. It now returns the Psalm 118 Haydock passage without consulting or augmenting the leaf's local source bindings. Independently resolving that ID yields the passage TOML and its edition, artifact, and work records. This is the retained local closure; it does not claim that the remote facsimile PDF itself is installed or newly verified.

Compared with the prior frozen trace, exactly two library IDs are added: the Psalm 118 passage and the existing Catholic Encyclopedia Daniel artifact. No library ID is removed. The additional explicit Bible files are Douay John 4, Psalm 107, and Psalm 144. These match the author's supplied impact result. Evidence: `actual-trace-check.json` beside this report.

The independently rerun source-only invalidation regression uses the real trace's ID and copies the actual registered source closure to an isolated fixture. Its local source-bindings file is empty. It narrows the automatic-read hook to that already-established source and edits only the copied warrant TOML; precisely that file's research-input fingerprint changes. The unchanged `review_inputs` code incorporates these fingerprints into the research seal. This demonstrates evidence-only invalidation without relying on a locally added binding or altering a live source.

The exact-source-set assertions remain exact equality checks. Their expected binding evidence is obtained from selected core queries before proper aggregation, so the test does not merely repeat the adapter's source collection. Existing fail-closed tests for unregistered IDs and invalid read locations also pass.

## Independent validation

Using the locked renderer virtualenv on PATH, bytecode disabled, and the review scratch directory for temporary files, ran:

```text
python3 -m unittest tools.tests.test_chronology_binding_sources \
  tools.tests.test_proper_chronology_reads \
  tools.tests.test_chronology_anchor_context -v
```

**35 tests passed in 12.908 seconds.** Full log: `focused-tests.log`. This includes ten new binding-route/aggregation/seal tests and the existing read-set, schema, historical-context, and forged-promotion checks.

Independently regenerated the upcoming proper's chronology record and TeX annotation in memory and compared each with the prior frozen package: both are byte-identical. No production file was written. The supplied broader impact result reports all 16 record/annotation pairs unchanged; that entire comparison was not rerun. Supplied evidence records 377 broader tests, a current 528-row pinned-base manifest, and all 20 captured examples passing. No new concern warranted repeating the broader suite.

## Disposition and limits

No findings remain in this bounded repair. The driver may regenerate/check and freshly seal `research-0001`, then obtain the separate actual-research disposition. Existing historical accepted leaves, prior research seals, source approvals, and publication approvals are not advanced by this PASS. The 588 B.C. printed-page limitation and all earlier source bounds remain unchanged.

This reviewer made no tracked, production-leaf, source-register, inventory, approval, or Git edits. Durable reviewer evidence is confined to `.scratch/chronology-review-2026-10-05/binding-source-review/`.
