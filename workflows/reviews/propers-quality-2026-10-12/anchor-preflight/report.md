# Independent review: early canonical web conversion

**Verdict: PASS.**
No blocking defect found in the four-file version-11 candidate. This is an
independent review of the workflow repair, not approval of the Sunday's study,
PDFs, web edition, or a replacement production run.

Reviewed against `df85e9726d5ea45d47af231814efe0585c703399` on
`feature/propers/codex`. The candidate includes uncommitted changes to
`workflows/pipelines/proper-study.json`,
`workflows/fragments/proper-study/author-study.md`, and `workflows/OPERATOR.md`,
plus new `tools/tests/test_workflow_study_web_preflight.py`.
`reviewed-state.json` identifies their exact reviewed SHA-256 hashes.
The reviewer did not author or edit those files.

## Findings

- The production check invokes the real `tools/tpt web-edition` converter.
  Native `_run_gate` judges its exit status, emits the blocking finding
  `GATE-STUDY-WEB-CONVERSION`, and uses the existing `author-study` failure
  transition. The success transition remains `study-review`; unchanged retry
  budgets can still terminate repeated failures as `BLOCKED`.
- The engine supplies `run.run_id` from its own state, refuses collisions in
  that reserved namespace, and substitutes shell-quoted values in one pass.
  An independent probe of the actual command preserved spaces, shell syntax,
  and a nested placeholder as one literal document argument. The illustrative
  `\label{proper-<element-key>}` survives fragment substitution unchanged.
- Converter source and rendered checks remain the sole mechanical owners.
  Author placement instructions match `guidance/web-editions.md`: one explicit
  target per declared element, including alternatives, located at its text or
  rights-safe locator. Semantic placement still requires source review.
- Conversion follows `main.tex` and its active canonical include graph. A
  successful fixture had declared but physically absent synthesis/homily
  entrypoints and components. No web receipt, installed `web/` directory, or
  default `build/web/` output was created.
- Output is written only after successful audits. A pre-existing probe file
  remained on a failed conversion, but the native gate still failed and
  returned to authoring. Repair reran conversion and preserved the earlier
  iteration's failure log. Reusing this disposable path cannot supply a PASS.
- The exact Markdown lock is enforced, rather than silently bypassing rendered
  checks. Both a wrong dependency version and an unavailable pandoc returned
  to authoring. The latter produced no converted output or review packet.
- The version and author fragment change the workflow digest. Native source
  binding rejects a changed workflow for an existing run; linear BLOCKED is
  terminal. A fresh version-11 run is required. No candidate edit changes the
  engine, converter, historical validator, result schema, or legacy `proper`
  pipeline. Existing converter regressions, including schema-1 behavior, pass.

**Resolved documentation observation:** the initial operator prose described
per-check logs too broadly. The unchanged engine writes them after a subprocess
returns; a 300-second timeout or execution `OSError` instead produces a
structured blocking finding. The coordinator qualified the sentence to
completed commands and explicitly described timeout/launch failures. The
reviewer inspected that final wording against `_run_gate`; it is accurate.
The recorded operator hash binds this corrected version. No finding remains
open, and no engine or test change was needed.

## Verification

All commands ran from the repository root. Tests used pandoc 3.11 and the
provided Markdown 3.10.3 dependency directory. For reproducibility, set
`PYTHONPATH` to the **absolute** path of
`.scratch/tlm-2026-10-04/generate-web-0000/dependencies`, `TMPDIR` to the absolute
review scratch directory, and `PYTHONDONTWRITEBYTECODE=1`.

| Check | Exit | Result |
| --- | --- | --- |
| `python3 -m unittest tools.tests.test_workflow_study_web_preflight -v` | 0 | 9 tests passed; real converter and native gate transitions. |
| `python3 -m unittest tools.tests.test_workflow_proper_study tools.tests.test_workflow_engine.RunIdentitySubstitutionTests tools.tests.test_workflow_adversarial.WorkflowSourceBindingTests tools.tests.test_workflow_adversarial.GateTests tools.tests.test_web_edition_conversion -v` | 0 | 197 tests passed; routing, source binding, quoting, converter and legacy regressions. |
| Two independent fixture probes, using the candidate's fixture and unchanged native engine | 0 | Missing pandoc fails closed; actual command substitution and fragment label preservation pass. |
| `git diff --check -- workflows/pipelines/proper-study.json workflows/fragments/proper-study/author-study.md workflows/OPERATOR.md tools/tests/test_workflow_study_web_preflight.py` | 0 | No whitespace errors in tracked candidate diff. |
| `git diff --quiet HEAD -- scripts/_workflow.py scripts/_proper_study.py tools/web-edition scripts/_markdown_render.py workflows/pipelines/proper.json` | 0 | Engine, converter, renderer, study validator and legacy pipeline unchanged. |

The first new-suite invocation used a relative `PYTHONPATH`: exit 1, three of
nine tests failed because the subprocess fixture changed directory and selected
host Markdown 3.11. Correcting only the environment to the absolute pinned path
produced the passing nine-test result. This is evidence of the enforced pin,
not a candidate regression. Scratch logs retain both attempts.

Review scratch evidence is under
`.scratch/propers-20261018/anchor-preflight-review/`: `new-tests.log`,
`new-tests-pinned.log`, `existing-tests.log`, and `independent-probes.log`.
The tests are meaningful bounded integration coverage: unrelated scholarship,
review seals and gates are explicitly stubbed in the new fixture, while the
new command, converter, dependency checks, and engine routing execute normally.

## Limits and disposition

No production workflow was seeded or advanced, and no manuscript, proof,
receipt, or historical run was edited. No actual 17-anchor manuscript repair
or full production acceptance is claimed. The current blocked-run result was
read as context; the complete historical archive and unrelated worktree changes
were outside the review scope. This lane wrote only its report, reviewed hashes,
and disposable scratch evidence; it made no commit or push.

The coordinator may adopt the reviewed workflow repair, preserving the terminal
version-10 evidence and obtaining fresh verdicts in a newly seeded version-11
run. The earlier report is not a substitute for any subsequent production gate.
