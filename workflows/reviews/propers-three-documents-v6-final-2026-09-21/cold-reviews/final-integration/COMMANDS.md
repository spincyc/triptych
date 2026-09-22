# Commands used

Run from the repository root:

```sh
python3 -m unittest -q tools.tests.test_propers_format tools.tests.test_proper_components tools.tests.test_content_preflight_study tools.tests.test_chronology tools.tests.test_web_edition_conversion tools.tests.test_workflow_proper_study
python3 scripts/_proper_study.py check --provider <gpt|claude> --document <each exact 1962 or postconciliar id> --date 2026-09-20 --phase publication --require-presentation --require-format
make check-web-editions-current
make public-site
tools/tpt source-library validate
tools/tpt source-inventory check --review src/sources/inventories/classification-review-v1.toml src/sources/inventories/publications-v1.toml
tools/tpt source-inventory check --review src/sources/inventories/claude-classification-review-v1.toml src/sources/inventories/claude-publications-v1.toml
tools/tpt source-family-migration check
tools/tpt document-library structure --check
tools/tpt source-reader structure --check
make check-release-bindings
make check-publication-inventories
make check-promised-deliverables
git diff --check
```

Additional inline Python audits recomputed all artifact hashes/sizes/pages,
compared every archived packet/result/seed/state byte with `build/tpt-runs`,
compared fresh workflow status/replay bytes, scanned active rite paths, checked
all 15 ancillary editions through Pandoc, and parsed the built *Assembling the
Mass* HTML ancestor stack for checkbox attachment.
