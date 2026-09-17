# Raster-destination guidance cold review — 2026-09-17

Verdict: **PASS**. No blockers or required amendments in the seven-line addition at `guidance/repository.md:344–349`.

Exact subject SHA-256: `acb2fb6ccba61911093ed1cb663b65fbd38de6b8c6090a925a3c71991c0f81f6`.

Reviewed above HEAD `53fbb228615420f45446f6c8a6eb457da2ce115d`. Earlier review reports remain unchanged.

## Findings and basis

- **The replacement warning is accurate.** `tools/pdf-review:1515–1602` prepares the requested batch in a new sibling staging directory and then calls `install_artifact_directory(staged_output, output, output.parent)`. The installer at lines 1040–1067 renames any existing destination aside, replaces it with the staged directory, and deletes the previous tree after success. It does not merge new rasters into the old output. Unrelated logs, proofs, or evidence already under `--output` are therefore removed on a successful replacement.
- **The destination rule addresses that behavior directly.** A dedicated child for each stage and iteration keeps the helper's replaceable contents separate from earlier evidence and sibling work. Keeping logs and other evidence outside that child also protects them during a retry. The example remains beneath the existing run artifact namespace and does not change canonical PDF or publication paths.
- **The frozen example remains usable with this clarification.** `workflows/fragments/proper-study/build-artifacts.md:18` supplies `build/tpt-runs/<run-id>/artifacts` as the example output root. The new paragraph explicitly treats that root as a namespace when it contains other work, resolving the unsafe literal use without changing the required helper, its resource controls, the three-PDF batch, or any inspection obligation. The fragment already requires recording the actual artifact paths for the next reviewer.
- **No inspected workflow schema or gate fixes the raster location.** The `artifact-gates` stage calls `scripts/_proper_study.py check --phase artifacts`; `artifacts()` compares the recorded PDF/render-input snapshot with the current one and validates metadata. The visual seal uses `artifact_state()`. These checks identify PDFs and render inputs, not a raster directory. The visual-review schema declares findings and review results without a raster-path constraint, and its fragment asks the reviewer to open the generated sheets and pages and name the artifacts actually reviewed. The dedicated child is compatible with those requirements.
- **The scope is proportionate.** The paragraph adds an output-ownership rule for a destructive replacement operation. It creates no new acceptance stage, review claim, source owner, or publication format. The immediately preceding requirement to inspect every rendered page remains controlling; choosing a safe destination does not itself establish visual acceptance.

## Checks and limits

Read the focused repository-guidance diff, `run_review()` and `install_artifact_directory()`, the build/visual-review fragments, visual-review schema, artifact and visual pipeline stages, and their Python checks. A focused search across workflow schemas, proper-study fragments/pipeline, workflow code, and the proper-study helper found the example output path in the build fragment and no enforced raster destination. `git diff --check -- guidance/repository.md` returned exit status 0. Rechecked the subject hash before delivery.

Inspected `tools/pdf-review` SHA-256: `3797128b9e275149267b610af82855322688a0846769e2d230394b3472e331dc`.

This review did not run the renderer, reproduce the reported lost files, validate recovery of any earlier evidence, or inspect rendered pages. It accepts the guidance delta's accuracy and compatibility with the inspected contracts only. Only this scratch report was created; no subject, frozen workflow, schema, fragment, or tracked review was edited. No commits or delegation.
