# Independent rereview of repaired historical context

**Verdict: PASS. Both findings from `anchor-context-review.md` are resolved. The chronology review hold is lifted: the driver may now regenerate the actual new proper's research artifacts and refresh their research seal using this reviewed projection.** Actual leaf validation and final full-study/concise-study pagination remain driver responsibilities; this is not publication approval or approval to rewrite earlier accepted leaves.

## Frozen state reviewed

Reviewed `build/agent-handoffs/20261005T142638Z-typed-chronology-anchor-context-rereview/` and its sibling ZIP, with incremental base and observed HEAD `3967091cb2ca97c663f6f8c6fd63c82b561e88ea`. Read `review-repair.md`, HANDOFF, REVIEW_REQUEST, checks, the repair's full difference from the prior package patch, the new worker regressions, manifest diff, actual Pandoc output, and the revised table raster. The prior frozen package `20261005T141251Z` and the prior changes-required disposition remain separate records.

All **22 frozen owner hashes matched** the working files. The ZIP passed `python3 -m zipfile -t`. Compared with the prior package, the additional owner is `scripts/chronology_review_diff.py`; the six changed existing owners are the guidance, proper display, manifest, query display, anchor tests, and web conversion tests. The corpus query implementation, source events, source passage records, preflight, component macros, and web renderer are unchanged from the previously reviewed semantic snapshot. Thus the previous source-bound and security findings remain applicable; the rereview does not reuse a previous acceptance for the repaired audit or display behavior.

## Finding 1 resolved: qualification is part of semantic rereview

`scripts/chronology_review_diff.py` now serializes `context_qualification` through the actual revision worker with `getattr(c, "context_qualification", "")`. `FIELDS_MANIFEST` compares it with missing serialized values equivalent to empty, and `FIELDS_FULL` inherits that field. These changes address both sides of the original omission.

The new tests execute the actual worker function definitions, rather than a test-only serializer. Independently rerunning them proves that qualification-only addition, shortening that removes the 588 B.C. page-verification caveat, and removal each report exactly `changed:context_qualification` in both semantic views. A historical claim object without the attribute serializes successfully as empty, and an older serialized object missing the key compares equal to an explicit empty field. No false historical change is introduced.

Independently checked the regenerated manifest against the prior base: it retains **528 rows**, the same ordered review IDs and case IDs, and all prior review references. Exactly five rows differ: PC-148 through PC-151 add `context_qualification` to the `change` reasons; PC-520 changes only `changed_in_lane` to record the repaired differ. The preserved 536 B.C. row is unchanged. This exposes review obligations without granting new approval.

`python3 scripts/build_profile_contract_manifest.py --check` passed against its unchanged pinned base `8e26a1769133255e04a9619a40e47886f402ce8f`. Evidence: `anchor-rereview-manifest.log` and `anchor-rereview-snapshot-check.json` beside this report.

## Finding 2 resolved: reader-facing historical language

The generated heading now reads “Historical background.” The prose places the represented event “after this historical event,” distinguishes the named event's dates from the passage and its composition, and says “Both events could occur in the same year.” This retains the direction and same-year precision without asking the parish reader to interpret anchor/boundary implementation vocabulary.

The actual Pandoc output and inspected table raster retain the named destruction of Jerusalem, A.M. 3416 with Haydock reporting Ussher and no conversion, distinct 586/587/588 B.C. alternatives, all source attributions, and the 588 printed-page-verification-pending caveat. The contradictory 536 B.C. claim is absent. All text is visible without clipping in the supplied smoke table. The rendered context still does not give a date for the Psalm's composition, performance, or utterance.

## Independent checks and remaining scope

With the locked virtualenv on PATH, bytecode disabled, and temporary files directed to reviewer scratch, ran:

```text
python3 -m unittest tools.tests.test_chronology_anchor_context \
  tools.tests.test_web_edition_conversion.WebEditionConversionTests.test_generated_anchor_context_keeps_qualified_dates_through_pandoc -v
```

**12 tests passed in 4.120 seconds.** Log: `anchor-rereview-focused-tests.log`. In addition to the repaired semantic differ, the rerun covers one-hop/profile/disposition filtering, exclusion of preserved contradictions, schema 2/3 compatibility and schema 4 separation, common-locus qualification, exact source-set tracing, canonical output validation, forged-date refusal, and Pandoc preservation.

The author's 587-test broad pass and 20-example replay are package evidence, not independently repeated results. No reason emerged to repeat that full suite. No tracked file, production leaf, source inventory, register, or Git state was edited by this reviewer.

The 588 B.C. value remains limited to the existing retained-transcription check; this review supplies no new printed-page verification. Its visible caveat must remain. The new research seal must include the newly computed context source reads. The documented historical rereview obligations remain open: no old accepted output is silently refreshed or approved by this PASS.
