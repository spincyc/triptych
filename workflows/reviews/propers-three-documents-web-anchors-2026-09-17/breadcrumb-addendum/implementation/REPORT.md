# Liturgical breadcrumb label correction

Implementation is frozen for independent review; no acceptance is claimed.

## Change

Only two reader_shelf() display strings in tools/public-alpha changed:

- Traditional Latin Mass → 1962 Missal
- Novus Ordo → Postconciliar Missal

This applies the apparatus naming rule in guidance/editorial.md. Published library filenames, URLs, route matching, layout, and article content are unchanged. No test source changes were needed for this two-string correction. The complete patch is change.patch.

## Exact subject

- Before SHA-256: 5618b1d040e6010f544649fafa6a5fa9bea3944550a647ef5a3c7a96e0f87839
- After SHA-256: ac4d7145e7b9886042db03c1a4a38923386bf002956602f06186f0674d860251
- Subject: tools/public-alpha

## Verification

Commands run from repository root; Python commands used TMPDIR="$PWD/.scratch/components/breadcrumb-labels" and PYTHONDONTWRITEBYTECODE=1.

| Command | Exit | Result |
| --- | ---: | --- |
| python3 .scratch/components/breadcrumb-labels/compare.py | 0 | Four actual render_page before/after comparisons, one existing tracked publication per provider and missal family: only the expected breadcrumb label changes. All href/src values and every remaining HTML byte are unchanged. |
| python3 -m unittest tools.tests.test_public_alpha.PublicAlphaTest.test_reader_breadcrumb_uses_owning_subject_shelf | 0 | One owning breadcrumb test passed. |
| git diff --check -- tools/public-alpha | 0 | No whitespace errors. |

comparison.json records the four source paths and before/after HTML hashes. The exact HTML outputs, isolated diffs, comparison script, comparison.log, and test.log are retained beside this report. before-public-alpha preserves the exact supplied baseline for reproduction. subjects.sha256 identifies the frozen implementation.

## Limits

No source, Markdown publication, PDF, workflow, release, catalog, layout, route, staging or Git history was changed. This checked local rendered HTML, not deployed pages or browser visual acceptance. No unrelated full suite or deployment build was run. The uninstalled new postconciliar canonical web publication was not used or represented as installed. Both production reviewers still own their final browser recapture and independent disposition.
