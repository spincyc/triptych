> Historical snapshot: this report concerns the initial local base. Read
> [the disposition](RECORD.md) and [current-main comparison](CURRENT-MAIN-REVIEW.md)
> before treating a finding as current.

# Independent controls review — 5 October 2026

Final verdict after focused recheck: **PASS**. The single research/review
wording conflict identified in the initial review is repaired.
The homily coverage correction and regression tests are sound. No substantive
code, stage-order, effort, or historical-compatibility defect was found.

Reviewed the focused patch in
`build/agent-handoffs/20261005T123449Z-propers-quality-controls/changes.patch`
against base `a53e262d00d2658ac079801b07b26deeffb05a6d`. At inspection, the
current diff over those eleven paths matched that patch byte-for-byte.
Sibling chronology implementation and data changes were excluded from the
review judgment. No tracked files were changed.

## Initial finding — resolved

**P2 — Preserve different supported answers to the same exegetical question.**
`workflows/fragments/proper-study/research-review.md:26–28` asks whether each
reading answers a **distinct exegetical question**, claiming the profile
requires this. The profile instead permits readings distinguished by emphasis,
identification, movement, or consequence
(`guidance/liturgy/propers-three-documents.md:178–183`). Its new paragraph asks
for each reading's particular question, checked reasoning, and distinguishing
consequence, and says to compare the answers (`:185–193`). Different questions
are one way to develop distinct readings; different supported answers or
inferences concerning the same question also satisfy that contract.

As written, a research reviewer can send defensible interpretations back for
invented differentiation merely because they address the same textual
difficulty. This changes the substantive acceptance standard beyond the
intended refusal of repeated generic applications. The same ambiguity appears
in `author-study.md:20–22`, `study-review.md:14–16`, and the new version-8
paragraph in `workflows/OPERATOR.md`.

Minimal repair: ask for a **particular** or **clear** exegetical question, and
attach the distinctness requirement to the readings' developed arguments,
inferences, movement, or consequences. For example, the reviewer can ask:
“Does each proposed reading answer a particular exegetical question through a
developed inference, and do the readings differ materially in reasoning,
movement, or consequence?” Align the author/study-review references and version
summary with that meaning. No new numerical or lexical gate is needed.

## Other conclusions

- The homily change permits a nonempty subset while preserving validation of
  unknown, duplicate, and malformed keys. Full coverage remains mandatory for
  appointed texts, proper treatment, concise commentary, lane declarations,
  and lane-component unions. The real preflight delegates to this validator.
- The new tests cover the selective homily through that preflight, empty and
  unknown homily coverage, and incomplete study coverage. Existing tests retain
  coverage of complete lanes, staging, ownership, and include graphs.
- The homily text-substitution judgment is useful, keeps ordinary applications
  and selective preaching possible, and does not alter the established
  requirement for a meaningful Gospel/other Scripture/prayer relation. Its
  surrounding instructions still make rhetorical techniques discretionary.
- The v8 change alters only the version in the pipeline definition. Existing
  source binding refuses advancement under changed definitions; terminal
  records keep their original identity and integrity reporting. No historical
  publication is made invalid by permitting selective homily coverage.

## Verification

Tests ran in a copied code/workflow tree beneath this review's exclusive
scratch directory, with the repository's `src/` available by read-only use of
a symlink. Test temporary files stayed beneath the review scratch tree.

- `python3 -m unittest tools.tests.test_proper_components_v2 tools.tests.test_workflow_proper_study tools.tests.test_content_preflight_study tools.tests.test_workflow_effort_levels`
  — exit 1, 150 tests, 149 passed. Sole failure: the reported unregistered
  **Leo the Great** in the existing GPT pc-s53 manifest. The registry and that
  manifest have no changes against HEAD; this is unrelated to the patch.
  Full output: `tests.log`.
- `python3 -m unittest tools.tests.test_workflow_proper_study_recipes.IsolatedRecipeTests.test_version_change_preserves_terminal_integrity_not_active_recompilation`
  — exit 0, one test passed. Full output: `version-test.log`.
- `cmp` between the handoff patch and the current focused diff — exit 0.

This is a controls review, not approval of future research, publication prose,
or rendered PDFs. Those remain the forthcoming run's independent reviews.

## Revised-patch disposition

Reviewed the replacement snapshot
`build/agent-handoffs/20261005T125322Z-propers-quality-controls-revised/changes.patch`.
The current focused diff matches that snapshot byte-for-byte. Comparing the
original and revised patches shows only the four requested prose repairs:
research-review, author-study, study-review, and OPERATOR.

The research review now asks for a **particular** question and a **distinct
argument, movement or consequence**. Both author-study and study-review
explicitly permit different readings to answer the same question. The version
summary likewise distinguishes questions from distinctive arguments or
inferences. This removes the unnecessary distinct-question requirement while
preserving the intended refusal of merely relabeled, repetitive applications.
No further findings remain in the focused controls patch.

The checker, tests, pipeline version, and remaining reviewed files are unchanged
from the original reviewed snapshot. The prior test evidence therefore stands;
no broad test rerun was needed for these four prose corrections. Final approval
is bounded to these controls and remains subject to separate chronology
validation and the forthcoming production run's ordinary independent reviews.
