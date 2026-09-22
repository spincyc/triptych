# Proper-study v6 robustness final cold review

## Verdict: PASS

The shared v6 hardening closes B1–B4 and the later follow-up cases on the
reviewed snapshot. I inspected the implementation independently, replayed the
repair probe, ran the exact focused and adjacent module sets, exercised all
four live provider/rite leaves in all three modes, regenerated all four web
editions into isolated scratch output, and reconciled the live TeX recorder
inputs with the shared semantic graph.

One live artifact receipt is intentionally pending outside this verdict: the
GPT postconciliar production run has advanced its research metadata, PDF, and
log but has not yet reached its new build-artifacts/visual-snapshot stage. The
current recorder and semantic graph agree; the old visual receipt does not yet
attest to those new production bytes. Exact details are recorded below.

## Required results

### B1 — executable TeX input is fail-closed

PASS. `include_graph()` applies `audit_executable_tex()` to every reachable
leaf-owned TeX file before accepting its literal import graph. Computed control
sequences, TeX `^^` character-code notation, nonliteral/conditional imports,
and file-execution commands outside literal `\input{...}` / `\include{...}`
edges are refused.

The executable probe rejects both `\csname input\endcsname{proper/unowned}`
and `\^^69nput{proper/unowned}`. The compiled regressions first prove that both
forms render the undeclared prose under pdfLaTeX, then prove that the component
gate rejects them. Literal current imports remain accepted in all 12 live
provider/rite/mode wrapper invocations.

### B2 — shared format ownership cannot be locally replaced

PASS. Every leaf source in the accepted graph is definition-free except for
the two named configuration commands and the narrowly checked generated
chronology helper. The audit rejects command and environment definitions,
primitive aliases/definitions/undefinitions, computed definitions,
`ExplSyntaxOn`/catcode routes, and LaTeX command-copy aliases.

The regression derives every command and both begin/end controls for every
environment from the real shared templates, then verifies that local `\let`
replacement or undefinition is rejected. Compiled attacks prove that
`\^^6cet` and `\RenewCommandCopy` can replace the homily columns before the
checker refuses them. The compiled positive template exercises the shared
title, lane, four-senses block, normal/comparison tables, and homily columns.

### B3 — lane-source bytes are sealed

PASS. `lane_source_paths()` requires every declared source to resolve beneath
the canonical leaf's `research/` owner. Study review adds those resolved paths
to its hashed file set. The unit regression and repair probe both mutate
`research/sources.md` and observe a changed study seal.

### B4 — the exact postconciliar shared owner is required

PASS. The resolver selects exactly one row through the canonical `Full
publication slug` column, extracts exactly one `shared/.../propers/verified.md`
target, confines it to the target provider, edition, formulary family, and
authorized layout, and requires a dependency equal to or beneath that owner.

The positive tests accept temporal-week and general-calendar owners. Negative
tests reject a provider-neutral substring spoof and a target slug mentioned
only in another row's Qualification cell. Live resolution returns the exact
week-25 owner for both providers:

- GPT: `src/gpt/.../propers/temporal/shared/ordinary-time/weeks/25`
  with 1,964 dependency files.
- Claude: `src/claude/.../propers/temporal/shared/ordinary-time/weeks/25`
  with 1,842 dependency files.

## Follow-up results

- The live `house-voice` regression is fixed. All 144 repository-backed
  content checks passed: 12 checks for research, synthesis, and homily across
  GPT/Claude and 1962/postconciliar. GPT postconciliar research passed with 11
  reader-facing files.
- All 12 live v6 content-wrapper invocations passed with both presentation and
  format contracts required. This also proves that the current generated
  chronology `\ifcsname` / `\csname` / generated-definition allowlist remains
  usable for both rites and providers.
- All four isolated web conversions passed their source-graph comparison. A
  direct final-output scan found no trailing spaces or tabs. Markdown hard
  breaks are emitted as semantic `<br>` elements.
- `artifact_state()` succeeded for all four live leaves. That operation compares
  each research/synthesis/homily `.fls` recorder set with `include_graph()`;
  all four semantic graphs reconciled. It found 27 render inputs for GPT 1962,
  27 for GPT postconciliar, 27 for Claude 1962, and 28 for Claude
  postconciliar. The study seals and web converter use the same graph walker.

## Verification

- Final focused suite: **308/308 passed** in 31.653 seconds.
- Exact adjacent suite: **346/346 passed** in 132.918 seconds.
- Repair-specific focused regressions: **12/12 passed** in 1.771 seconds.
- Post-fix B1–B4 executable probe: **8 expected rejects/seal changes**, exit 0.
- Live content matrix: **144/144 checks passed**.
- Live v6 wrapper matrix: **12/12 passed**.
- Isolated live web conversion: **4/4 passed**; trailing-whitespace scan found
  zero matches.
- Live semantic/recorder graph reconciliation: **4/4 passed**.
- Live artifact receipt gate: **3/4 passed**. The sole non-pass is the expected
  active-run GPT postconciliar visual snapshot described below.
- `python3 -m py_compile`, `jq empty workflows/pipelines/proper-study.json`, and
  scoped `git diff --check`: passed.

The first focused replay correctly exposed a repair-fixture regression: four
chronology-seal assertions failed because the fixture wrote a `Slug` header
while the hardened resolver requires `Full publication slug`. After that
fixture was corrected, the exact 308-test replay passed. This review did not
silently discount that failure.

The repair report also records two unrelated live-corpus count failures from an
earlier concurrent state. They did not reproduce on the final reviewed
snapshot: the exact adjacent set, including both pinned corpus-refusal tests,
passed all 346 tests.

## Pending production-stage visual receipt

The GPT postconciliar artifact gate currently reports that built bytes differ
from the old visual snapshot. The recorder graph itself reconciles. The stale
receipt differs from current production state in exactly these entries:

- research PDF: recorded `e2d698ef242d4ca790e4ad218c1dcfd798db555f79f0dccacf0d2c30cb8bdf49`,
  current `8bdebdd9171173b9cfa5861bbeded5e85fa4cecb64893d7cafad7b8df0d59678`;
- `generation-metadata.tex`: recorded
  `2ef56593ca0910b18fde4a2e5e70ab32ba91d40b36ef1ae59dd8a67b050359ef`,
  current `e03c0ea890ccd9a21453405a17f7993ad7ca6902763a5d8cfbe2f82ea061eb65`;
- research log: recorded
  `4dc46fe5ceafee37654937e23f47f356a26c5d103efd9bff5644092c44feac5f`,
  current `b034efe0406a9a6adacb2ae0f1d38c5ab5b6bac03b4d2d58ea6e2570c64cbd84`.

The active production run owns the forthcoming build-artifacts and exact-byte
visual review. This does not reopen B1–B4 or indicate a semantic-graph mismatch.

## Review boundary

The subject commit was
`8a75235b19732d91579a66b05ff0f470ed43777a`. The checkout contained many
pre-existing and concurrent provider/research changes. This cold review edited
no tracked file; it wrote only
`.scratch/cold-review-v6-robustness-final/`. Commands are in `COMMANDS.md` and
reviewed subject hashes are in `SUBJECT-HASHES.sha256`.
