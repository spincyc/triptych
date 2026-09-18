# Independent breadcrumb-label addendum — PASS

Reviewed only the two `reader_shelf()` display-string corrections in
`tools/public-alpha:3245–3246`:

- `Traditional Latin Mass` becomes `1962 Missal`.
- `Novus Ordo` becomes `Postconciliar Missal`.

These names implement `guidance/editorial.md`'s apparatus-naming rule. That same
rule expressly preserves the established library filenames. The exact source
diff contains only the two display strings; route selectors, destinations,
layout, article content and rendering logic are unchanged. This is publication
Reader apparatus under the already-read web-edition and corpus-browser
contracts, not a change to the protected Day/Propers liturgy instrument or to
liturgical source interpretation. No additional source/rite-profile judgment
is claimed.

The baseline was extracted independently with `git show HEAD:tools/public-alpha`
at commit `1ae49f43f1c0b6f777a963889a985c1d6cfeccfc`; its hash matches the
previously reviewed renderer. A byte comparison proves the new file is exactly
that baseline with the two approved string replacements.

Four independent full `render_page` comparisons cover both `gpt` and `claude`,
each with an existing tracked 1962 proper and postconciliar proper. Every
rendered breadcrumb has the required neutral label and unchanged relative
library destination. In each case, replacing only that one breadcrumb text
node makes the entire before/after HTML byte-identical; every `href`, `src`,
and `id` remains unchanged. The actual HTML, focused diffs and per-input/output
hashes are retained beside this report.

## Commands and outcomes

Commands ran from the repository root. Python invocations used
`TMPDIR="$PWD/.scratch/anchors-cold-review/breadcrumb-addendum"` and
`PYTHONDONTWRITEBYTECODE=1`.

| Command | Exit | Result |
| --- | ---: | --- |
| `git show HEAD:tools/public-alpha > .scratch/anchors-cold-review/breadcrumb-addendum/before-public-alpha` | 0 | Independently recovered the exact prior renderer. |
| `/usr/bin/python3 -m unittest tools.tests.test_public_alpha.PublicAlphaTest.test_reader_breadcrumb_uses_owning_subject_shelf` | 0 | One test passed. This existing test covers the Catholic Exorcism shelf; the four comparisons below directly exercise the changed routes. `test.log`. |
| `/usr/bin/python3 .scratch/anchors-cold-review/breadcrumb-addendum/check.py` | 0 | Exact two-string source delta and 4/4 affected full-render comparisons passed; all URLs, IDs and remaining HTML unchanged. `comparison.log`, `comparison.json`, retained HTML and diffs. |
| `git diff --check -- tools/public-alpha` | 0 | No whitespace errors. |

## Exact subject and limits

- Before SHA-256: `5618b1d040e6010f544649fafa6a5fa9bea3944550a647ef5a3c7a96e0f87839`
- Reviewed SHA-256: `ac4d7145e7b9886042db03c1a4a38923386bf002956602f06186f0674d860251`
- Machine-readable record: `subject-hashes.json`.

The earlier 144-page HTML parity finding remains a historical result for the
prior shared-renderer extraction ending at `5618…`. This addendum deliberately
accepts the two breadcrumb text differences; it does not claim current
byte-parity with that earlier renderer.

No browser visual review, real Sunday source judgment, PDF review, full-site
acceptance or release/deployment check was performed. The known full-suite
error for the not-yet-installed postconciliar canonical web edition remains
pending legitimate installation; no unrelated suite was rerun. The actual web
reviewers retain their final browser recapture and acceptance responsibilities.
Release binding and review archival remain coordinator-owned.

This reviewer wrote only `.scratch/anchors-cold-review/breadcrumb-addendum/`.
No subject, source, publication, workflow, release record, Git index or history
was changed.
