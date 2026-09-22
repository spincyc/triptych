# Command evidence

All commands ran from the repository root. Repeated provider/document/edition
commands were dispatched independently in parallel; each exit was inspected.

## Unit and integration suites

```sh
python3 -m unittest -q \
  tools.tests.test_content_preflight_study \
  tools.tests.test_proper_components_v2 \
  tools.tests.test_proper_pagination \
  tools.tests.test_propers_format \
  tools.tests.test_web_edition \
  tools.tests.test_web_edition_conversion \
  tools.tests.test_workflow_proper_study \
  tools.tests.test_workflow_proper_study_artifact_routing \
  tools.tests.test_workflow_proper_study_recipes \
  tools.tests.test_workflow_scope_and_publication
```

Initial exit 1: 308 tests, one failure and three errors from the noncanonical
`Slug` fixture header. Final exit 0 after the routed fixture correction: 308
tests, OK, 31.653 seconds.

```sh
python3 -m unittest -q \
  tools.tests.test_makefile \
  tools.tests.test_pages_publication_selection \
  tools.tests.test_proper_chronology_postconciliar \
  tools.tests.test_workflow_adversarial \
  tools.tests.test_workflow_advisory_ownership \
  tools.tests.test_workflow_chronology \
  tools.tests.test_workflow_content_preflight \
  tools.tests.test_workflow_research_fanout \
  tools.tests.test_workflow_shared_reviser \
  tools.tests.test_workflow_source_registration \
  tools.tests.test_workflow_synthesis_preflight
```

Exit 0: 346 tests, OK, 132.918 seconds.

The 12 newly added regression test IDs covering shared-input preflight,
lane-source ownership and sealing, all shared controls, computed/obfuscated
inputs and aliases, trailing whitespace, canonical owners, substring spoofing,
and exact registry rows were also run directly. Exit 0: 12 tests, OK, 1.771
seconds.

```sh
python3 .scratch/repair-v6-adversarial-gaps/adversarial_probes.py
```

Exit 0: B1 computed and `^^` input attacks rejected; B2 direct, `^^`, and
command-copy aliases rejected; B3 seal changed; B4 neutral spoof and
qualification-row spoof rejected.

## Live checks

For every combination of provider in `gpt claude`, document in the current
1962 and postconciliar v6 leaves, and edition in `research synthesis homily`:

```sh
tools/check-content-preflight \
  --provider PROVIDER --document DOCUMENT --edition EDITION

python3 scripts/_proper_study.py check \
  --provider PROVIDER --document DOCUMENT \
  --phase content --edition EDITION \
  --require-presentation --require-format
```

Results: 144/144 content checks and 12/12 wrapper invocations passed.

Exact postconciliar owner resolution and `research_dependencies()` were called
directly for GPT and Claude. Both returned the canonical week-25 owner; closure
counts were 1,964 and 1,842.

For each of the four live leaves:

```sh
tools/tpt web-edition \
  --provider PROVIDER \
  --output .scratch/cold-review-v6-robustness-final/web \
  DOCUMENT
```

All four exited 0. The following returned exit 1 with no output, which is the
expected `rg` no-match result:

```sh
rg -n '[[:blank:]]+$' \
  .scratch/cold-review-v6-robustness-final/web -g '*.md'
```

`artifact_state()` was called for all four leaves; all four succeeded and
therefore reconciled each mode's recorder inputs with the semantic graph. The
full artifact wrapper was then run for all four:

```sh
python3 scripts/_proper_study.py check \
  --provider PROVIDER --document DOCUMENT \
  --phase artifacts --require-presentation --require-format
```

Three exited 0. GPT postconciliar stopped on its expected active-run visual
receipt drift; the exact three differing hashes are in `REPORT.md`.

## Static checks and hashes

```sh
python3 -m py_compile \
  scripts/_proper_components.py scripts/_proper_study.py \
  tools/check-content-preflight tools/web-edition \
  tools/tests/test_content_preflight_study.py \
  tools/tests/test_proper_components_v2.py \
  tools/tests/test_proper_pagination.py \
  tools/tests/test_propers_format.py \
  tools/tests/test_web_edition_conversion.py \
  tools/tests/test_workflow_proper_study.py

jq empty workflows/pipelines/proper-study.json

git diff --check -- \
  scripts/_proper_components.py scripts/_proper_study.py \
  tools/check-content-preflight tools/web-edition \
  tools/tests/test_content_preflight_study.py \
  tools/tests/test_proper_components_v2.py \
  tools/tests/test_proper_pagination.py \
  tools/tests/test_propers_format.py \
  tools/tests/test_web_edition_conversion.py \
  tools/tests/test_workflow_proper_study.py \
  guidance/liturgy/propers-three-documents.md guidance/web-editions.md
```

All exited 0.
