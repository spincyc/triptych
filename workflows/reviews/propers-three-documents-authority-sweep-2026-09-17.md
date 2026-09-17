# Authority-sweep guidance cold review — 2026-09-17

Verdict: **PASS**. No blocking findings or required amendments in the paragraph at `guidance/liturgy/propers-three-documents.md:103–109`, beginning “At initial submission and after a research repair.”

Exact subject SHA-256: `f63469851b13ee588bc04d5d849272aeacf8e96f68563b8ac45910d38c3b04d7`.

Reviewed above HEAD `ee1e418843b27cbb3538f1a60f5cf7f60d2dc5a9`. The focused diff contains eight added lines and no deletions. Earlier review reports remain unchanged.

## Findings and basis

- **The requirement matches the implementation's limits.** `scripts/_proper_study.py:218–229` combines the leaf's research, instance, and formulary records with declared external dependencies and registered binding ancestry. Lines 281–284 compile their paths and hashes. Neither this code nor `tools/source-library:904–935` discovers an authority merely because an included summary mentions it. Requiring the author or reviewer to compare every adopted controlling authority with the compiled seal addresses that exact limitation without claiming automatic semantic discovery.
- **The sweep covers the relevant authority classes.** The paragraph expressly reaches context, instance, formulary, source, and rights records, including calendar and rubric authorities used to select permitted branches. It requires following a summary inventory to the underlying records that control its conclusion. Including the summary's bytes alone therefore cannot satisfy the requirement when the actual decision depends on another owner.
- **The scope is bounded and consistent.** “Adopted” and “controlling” limit the sweep to the evidence relied upon; the last sentence preserves the distinction from excluded leads. This does not authorize removing bindings the engine already includes. Read with lines 94–101, it also does not reclassify global guidance, `THIRD_PARTY.md`, or workflow review receipts as external source owners. Source-specific rights evidence still enters through a reached binding ancestor or an explicit dependency beneath `src/`.
- **Repair timing and existing workflow agree.** The initial-submission and post-repair audit makes the requirement recur when evidence changes. `workflows/fragments/proper-study/research.md` already requires all controlling external evidence in the dependency declaration and reviewer verification of its completeness. Both research stages include `proper-study/contract.md`, which requires reading the profile completely. This paragraph makes that existing obligation concrete; it adds no manifest field, review-result field, stage, or transition.
- **The source rules remain intact.** `guidance/sources.md` distinguishes reusable evidence from publication-local sufficiency judgments and requires affected consumers to remain discoverable. Following the actual source owner preserves that distinction; it does not promote a summary into independent verification or replace claim-level review with a hash check.

## Checks and limits

Read the focused profile diff, its adjoining dependency rules, `research_dependencies()`, `bound_evidence()`, the research branch of `review_inputs()`, the source-library ancestry function, governing source rules, and the relevant workflow fragments and stage configuration. `git diff --check -- guidance/liturgy/propers-three-documents.md` returned exit status 0. Rechecked the subject hash before delivery.

Supporting code hashes remain `d1fc61e47a08d8b39f2d5f95b25802b1e9748f48767e36c1517ce25ca75f2fe3` for `scripts/_proper_study.py` and `092afe66161760f85431a4607def60b44af4b7c7370eb6f6953d50601cc4eee1` for `tools/source-library`.

This is guidance acceptance only. No complete live research seal, adopted-authority inventory, source sufficiency, rights merits, publication, or run acceptance was verified, and no tests were executed. The paragraph defines the audit; this review does not certify that either publication has performed it. Only this scratch report was created. No subject edits, frozen workflow edits, commits, or delegation.
