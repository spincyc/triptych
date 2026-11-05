# Source/reader workflow audit before PC-S58-A production

Reviewed 5 November 2026 against main `c57e60ef3d` before seeding the GPT
Thirty-second Sunday in Ordinary Time production.

The active `proper-study` path already explicitly used source mode for checks,
review seals and final acceptance. It bypassed PDF building, installation and
visual review. The retired `proper` and `proper-finish` definitions remain
historical records and were not rewritten. The separate deployment
`print-compile` job tests admitted native source bundles and discards its PDFs;
it is not a maintained PDF publication corpus or print-layout approval.

Version 18 corrects the remaining authoring instructions inherited from the
earlier publication model:

- Publication and release identities, outputs and labels derive from their
  canonical paths and records. Authors no longer repeat those fields.
- Document-type regions place proper components by key; section paths stay
  solely in the component manifest.
- Revision timestamps derive from Git. Authoring stages no longer request a
  tracked finalization timestamp, which the metadata gate rejects.
- Each of the three outputs has a generated reader under the same leaf's web
  declaration. The canonical reader receives workflow inspection; a companion
  is converter-verified unless its own actual inspection is recorded.

Correct explicitly repeated derived fields remain backward-compatible;
their former instruction was a duplication risk, not proof of an immediate
runtime failure. The timestamp and component-placement instructions conflicted
with the current authoring rules.

A subsequent runtime check found that adding the required completed-inspection
receipt to `web-edition.toml` changed the source/render identities and therefore
invalidated the same web review. The schema now projects only the three
operational inspection fields at their admitted locations out of those
identities. Reader decisions and actual source/output bytes remain bound, and
the full declaration remains validated. Four regressions exercise receipt
stability and refusal of changed reader decisions, unrelated fields, source
text and converted output.

The converter also derives an uncommitted edition's revision from the current
time. The coordinator must therefore commit reviewed sources before dispatching
web conversion; the current packet checks this prerequisite. This preserves
the revision policy rather than weakening byte-identity checks.

## Verification

The following focused unittest selections passed: 28 tests, zero skips.
Temporary fixture directories were redirected to the audit's ignored scratch
area without changing production code or fixture behavior.

```text
tools.tests.test_proper_study_source_mode
tools.tests.test_workflow_proper_study.DefinitionTests
tools.tests.test_proper_study_postconciliar_identity
tools.tests.test_workflow_proper_study_recipes.IsolatedRecipeTests.test_real_conversion_lands_at_snapshot_path_once_per_provider
```

They exercise source-only acceptance and stale review refusal, workflow
definitions, exact postconciliar identity/adoption, and real conversion and
snapshot paths for both providers. `git diff --check` passed. Separately,
the new dated GPT identity passed the source-mode scope check. After the runtime
repair, the complete document-schema suite and the focused selections passed
62 tests, zero skips. The first version-18 bootstrap was left at its initial
scope gate before any production dispatch; the corrected source checkpoint
receives a fresh run identity.

This audit approves starting the corrected workflow. It supplies no research,
content, web, print or deployment acceptance for the new Sunday publication.
