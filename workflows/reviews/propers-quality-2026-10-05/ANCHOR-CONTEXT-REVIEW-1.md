# Independent review of typed historical anchor context

**Verdict: changes required before chronology sealing.** The source bounds and typed projection pass this bounded review. One semantic-audit omission and one reader-facing wording correction remain. This is not publication, historical-leaf regeneration, or research-seal acceptance.

## Reviewed snapshot and scope

Reviewed the immutable `build/agent-handoffs/20261005T141251Z-typed-chronology-anchor-context/` package and sibling ZIP, against incremental base `3967091cb2ca97c663f6f8c6fd63c82b561e88ea`; integrated comparison is `b373dd5db96ea67b1975b27de411cfd6cf2e1ee6`. The package's 21 owner hashes matched the working files when checked. Those hashes and the packaged patches identify the reviewed state independently of subsequent shared-checkout work.

Read HANDOFF, REVIEW_REQUEST, checks, sources, impact, the full incremental patch, new tests, generated schema-4 record, TeX/text projection, computation-read JSON, and actual Pandoc output. Inspected the provided table raster. Applicable chronology/source guidance was read in full earlier in this review task and its subsequent changes inspected. Earlier source findings remain applicable because the passage records and underlying source evidence are unchanged. No tracked files, production leaves, registers, inventories, or Git state were changed by this reviewer.

## Required corrections

### 1. Include `context_qualification` in semantic claim rereview

Location: `scripts/chronology_review_diff.py:155` (`WORKER` claim serialization), `:287` (`FIELDS_MANIFEST`), and `:303` (`FIELDS_FULL`).

The new source-owned qualification field is omitted from the worker's serialized claim and both comparison views. Consequently a qualification-only edit is invisible to the semantic claim diff and rereview-manifest generator. This is material: the field carries the printed-page verification limitation immediately beside the displayed 588 B.C. alternative.

Reproduction used the actual worker `claim()` function and the real `israel.exile.third-captivity` claim at index 3. Changing only its `context_qualification` from:

> Petavius table reported by Sloet; retained transcription checked, printed-page verification still pending

to `Petavius table reported by Sloet` yielded identical serialized claims and empty results from `diff_claims` with both `FIELDS_MANIFEST` and `FIELDS_FULL`. The reviewer evidence is `anchor-semantic-diff-repro.json` beside this report. Existing canonical-output freshness checks still catch an altered generated artifact; that separate protection does not supply the missing semantic claim rereview.

Required result: serialize the field with a historical-loader-compatible empty fallback, compare it in both semantic views, and add a regression proving qualification-only addition/change/removal is reported. An older serialized claim or loader without the field must remain equivalent to an empty qualification. Regenerate the affected rereview manifest and verify it is current; do not silently accept those newly visible changes.

### 2. Use historical language in the parish-facing text

Location: `scripts/_proper_chronology.py:1393` (`_group_heading`) and `:1436` (`_anchor_caution`), with corresponding rendered-output tests.

The visible phrases “Anchor context,” “after this anchor,” and “the boundary may fall within the same year” expose the data model to the reader. The distinction is substantively correct but needlessly difficult in a dense Date cell.

Required result: display “Historical background” and explain the before/after relationship using “this historical event” or equivalent plain language. Explain explicitly that the represented event may occur within the same calendar year as the named historical event. Preserve direction, every date and source qualification, the non-composition limitation, and the typed internal `anchor-context` relation. Reinspect the generated table and web text after this display-only correction.

## Findings that pass

- The Psalm 136 represented lament remains after the destruction of Jerusalem. The four dates describe that named historical event, not the Psalm's utterance, performance, or composition. This meaningfully supplies historical context without inventing a Psalm date or converting a broad era into an occasion.
- A.M. 3416 remains Haydock reporting Ussher, without conversion. The 586, 587, and 588 B.C. alternatives remain distinct. The 588 claim visibly retains its transcription-checked/printed-page-pending caveat. The retained contradictory 536 B.C. claim is excluded from answer context even in evidence mode.
- Context follows only one named event boundary. It does not expand recursively, through durations or composition units, or into another evidence profile. Disposition and answerability filtering apply independently to the parent and candidates. Context is exported for a proper only when its parent assertion belongs to every appointed locus.
- The same-year limitation is retained. The code does not turn “after” into a next-year lower endpoint, combine alternative years into a fabricated range, or perform arithmetic on A.M.
- Schema 4 stores context separately from ordinary/publication claims, retaining parent, direction, candidate sources, basis, note, and qualification. Noncontext records retain schema 2/3 behavior. Canonical regeneration validates the new record and annotations; context does not grant global permission to print those years as Psalm dates.
- Generated TeX seals context in separate helper macros. Preflight rejects qualification removal, direct handwritten internal-helper calls, and forged promotion to passage/composition dates. Web conversion preserves the complete visible payload.
- The computation-read trace includes the exact union of ordinary, comparison, and context sources. The new context obligations include the Haydock Psalm 70 passage and Reid, Meistermann, Schets, and Sloet artifacts, rather than only the Psalm 136 source. Existing ancestry resolution remains in use. The supplied record contains 17 source IDs and 1,569 read paths; research sealing must be regenerated from this new result after acceptance.
- The supplied table raster is legible, without visible clipping; alternatives and caveats survive. This is a macro/table smoke check, not acceptance of final full-study or concise-study pagination.
- The measured incremental historical impact is zero existing record/annotation snapshot changes. The integrated earlier lane still lists 15 annotation snapshots (14 active; one withdrawn) and seven audit records as later rereview obligations. No prior accepted output was rewritten by this refinement, and this review grants no such authority.

## Independent validation and limits

Executed with the required root virtualenv on PATH, bytecode disabled, and temporary files confined to reviewer scratch:

```text
python3 -m unittest tools.tests.test_chronology_anchor_context \
  tools.tests.test_web_edition_conversion.WebEditionConversionTests.test_generated_anchor_context_keeps_qualified_dates_through_pandoc -v
```

Result: **10 tests passed**, 4.061 seconds. Full output: `anchor-focused-tests.log`. This covers filtering, typed separation, schema compatibility, exact source-set tracing, mixed-locus boundaries, canonical validation, forged-date refusal, and Pandoc preservation.

All 21 packaged owner hashes passed verification. The ZIP passed `python3 -m zipfile -t` (`unzip` is unavailable). The semantic-diff reproduction above independently exposes a gap not covered by those ten tests.

The author's 585-test broad pass, chronology/coverage validation, 20-example replay, and zero-incremental-impact measurement are recorded package evidence; the entire broad suite and historical impact generator were not rerun without a new concern. No new source acquisition or new independent printed-page verification of the 588 B.C. table was performed. Its caveat remains necessary. Final proper PDFs, source/research seal regeneration, and any historical rereview remain driver-owned work after the two corrections receive bounded recheck.
