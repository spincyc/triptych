# Independent rereview — PASS within the seven-file repair scope

The two initial findings are resolved. No new blocking finding was found in the
frozen converter repair or bounded shared-renderer extraction. This disposition
accepts that implementation scope; it does not accept either Sunday's source
placement, research, theology, PDFs, web installation, release, or deployment.

## Finding dispositions

1. **Complete-publication anchor uniqueness: resolved.** The original
   `title-inline-collision` fixture now raises `ConversionError: duplicate
   schema-2 rendered proper anchor(s): proper-collect`. The final title,
   subtitle, normalized body, and explicit inline IDs are inspected together
   using the site's actual Markdown primitive. An independently added accented
   title (`Próper collect`) also refuses the duplicate actual-site ID.
2. **Unresolved proper links silently reduced to prose: resolved.** The original
   `missing-link` fixture and styled variant now raise
   `ConversionError: unresolved schema-2 proper fragment(s): proper-typo`
   before cleanup. Valid explicit heading and paragraph links survive. Additional
   checks cover styled, percent-encoded, and raw-HTML unresolved proper links.

Both original reproduction scripts were rerun against the frozen implementation
with all new fixtures and logs under `rereview/`; the initial review, fixtures,
outputs and logs remain intact.

## Extraction assessment

`tools/public-alpha` and `tools/web-edition` call the same imported
`render_markdown` function. The new helper owns exactly the former six
extensions, exact Markdown-version check, and Markdown-to-HTML primitive.
Public-alpha retains its existing source preprocessing, table-header scopes,
fence guard, and layout wrapper. The helper receives the caller's repository
root. There is no reverse CLI dependency and no `tmt.json` change.

Independent parser comparison agrees with the actual site's IDs for accented
headings, repeated slugs (`repeated_1`), numbered headings, explicit heading
IDs, inline IDs, and footnotes. Code and comment ID examples do not satisfy the
rendered anchor inventory. Missing package import, missing distribution,
wrong installed version, absent exact pin, duplicate pins, and wrong pinned
version all refuse. Source labels remain mechanically checked for exact
manifest coverage and multiplicity; their semantic placement remains an
owning source review judgment.

The new helper is present in the actual `FIXED_ARTIFACT_INPUT_PATHS` and
`site_source_paths()` result (22,113 recognized inputs at this check).
Subtracting only the helper from the actual recognized set reports precisely
that missing input, and a stale helper digest is rejected by the real binding
checker. Release-manifest refresh remains coordinator-owned pending integration;
this review did not alter or certify those manifests.

The guidance delta remains minimal: the explicit source-label rule has one
owner in `guidance/web-editions.md`; the three-document profile links to it.
The repair does not infer liturgical roles from biblical headings or combine
calendar families.

## Verification

All commands ran from the repository root. Python runs and `tmt check` used
`TMPDIR="$PWD/.scratch/anchors-cold-review/rereview"` and
`PYTHONDONTWRITEBYTECODE=1`. Relative script paths below are within
`.scratch/anchors-cold-review/rereview/`.

| Command | Exit | Actual result |
| --- | ---: | --- |
| `/usr/bin/python3 -m unittest tools.tests.test_web_edition_conversion tools.tests.test_web_edition tools.tests.test_public_alpha` | 1 | 199 tests: 198 passed, one error, zero assertion failures, no skips reported. `unit-tests.log`. The 83 web tests pass; the full 116-test public-alpha suite has the pending-publication error described below. |
| `/usr/bin/python3 .scratch/anchors-cold-review/rereview/baseline_public_alpha_tests.py` | 1 | Exact `78d8ce505` public-alpha tool and test sources: 114 tests, 113 passed, the same one error. `baseline-public-alpha-tests.log`. This runs against the same present publication inputs, rather than pretending the whole checkout is historical. |
| `/usr/bin/python3 .scratch/anchors-cold-review/rereview/probe.py` | 0 | All 19 original diagnostic fixtures completed; `probe.log` and `probe-results-initial.json`. |
| `/usr/bin/python3 .scratch/anchors-cold-review/rereview/probe_extra.py` | 0 | All 10 additional original fixtures completed; `probe-extra.log` and `probe-results-extra.json`. Diagnostic exit 0 means completion; recorded acceptance/refusal states establish each result. |
| `/usr/bin/python3 .scratch/anchors-cold-review/rereview/independent_checks.py` | 0 | 11 independent checks passed, including real-site IDs, lock refusal, shared callable identity, and actual artifact-input coverage. `independent-checks.log` and `.json`. |
| `/usr/bin/python3 .scratch/anchors-cold-review/rereview/render_compare.py` | 0 | 144/144 complete `render_source_page` HTML outputs byte-identical to the exact `78d8ce505` renderer: 25 fixed pages and 119 tracked web publications. `render-comparison.json` contains input/output hashes; both HTML sets are retained under `rendered-source/`. |
| `/usr/bin/python3 .scratch/anchors-cold-review/rereview/legacy_compare.py` | 0 | 20/20 extant schema-1 conversions byte-identical to the Git-extracted `78d8ce505` converter. `legacy-comparison.json` and `.log`. |
| `"$HOME/.local/bin/tmt" check` | 0 | `ok`; the executable was resolved and invoked by its absolute path. `tmt-check.log`. |
| `git diff --exit-code 78d8ce505 -- tmt.json` | 0 | Registry unchanged. |
| In-memory Python `compile()` over the five implementation/test files | 0 | 5/5 compile; no cache files created. |
| `git diff --check -- tools/web-edition tools/tests/test_web_edition_conversion.py tools/public-alpha tools/tests/test_public_alpha.py guidance/web-editions.md guidance/liturgy/propers-three-documents.md` | 0 | No whitespace errors. |
| `sha256sum --check .scratch/anchors-cold-review/rereview/subjects.sha256` | 0 | All seven subjects match the coordinator's freeze; exact copies retained under `frozen/`. |

The single suite error is
`PublicAlphaTest.test_no_site_page_renders_a_fence_as_running_prose`, subtest
`web/gpt/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a.md`.
It raises `FileNotFoundError` because that declared eligible web edition is
intentionally awaiting legitimate generation/review/installation. The exact
old tool and old test reproduce the same error on the same path. It is not
caused by this extraction, and no fixture or publication was fabricated to
make the total green. The coordinator should rerun that owning case after the
real installation.

Two review-harness adjustments are preserved, not hidden. The first full-HTML
comparison incorrectly passed raw catalog source directly to `render_page` and
hit the existing internal-marker guard (exit 1); the corrected comparison uses
both versions' real `render_source_page` preprocessing with the same explicit
inclusion set drawn from the pages' PDF links. Its first script/log remain as
`render_compare_initial.py` and `render-comparison-initial.log`. The first
standalone baseline-test runner omitted the repository root from `sys.path`,
causing nine harness import errors in addition to the real pending-publication
error (114 tests, ten errors, exit 1). Adding that import path to the scratch
runner leaves only the reproduced real error. The initial runner/log are kept
with `_initial` / `-initial` names.

## Limits

The 144-page comparison proves complete generated HTML byte parity on the same
current source inputs in preview mode, including page preprocessing and layout.
It is not browser, screenshot, responsive, accessibility, PDF, full-site-build,
release, or deployment review. No such acceptance was requested or asserted.
The not-yet-installed postconciliar web edition is outside that parity set.
The pre-existing source scanner's handling of literal TeX-label examples and
nested edition branches remains as documented in the initial report; those
probes refuse safely and this bounded extraction does not broaden that parser.

Only `.scratch/anchors-cold-review/` was written by this reviewer. Initial
`review-initial.md` remains SHA-256
`c8e3437e1bb30ab0fa4b7ba85bd8843b48f74d88781ce5acf4a59ca9b7a184df`.

## Frozen subject hashes

```text
d945021413b26de9a8b2e1c961caed9035c742a3802ccf9339001c28ba215d7b  tools/web-edition
e3b715f61a6ad9d67bbe96f39182e7bcbeb31aa7975f13798736b64184844735  tools/tests/test_web_edition_conversion.py
d74e56ea19a9d4aa81b0c4cf06bd7b110cdf0ac87c5b2a10320821b0c958f37a  scripts/_markdown_render.py
5618b1d040e6010f544649fafa6a5fa9bea3944550a647ef5a3c7a96e0f87839  tools/public-alpha
4cc0bb0e7d76d5af1a4ded758c547b94eb9a5ce2d342f7ee425594f45bbf5802  tools/tests/test_public_alpha.py
b786dea6d618896926cd7c2a5762f161c11dfee5092ffa463233f6f96ead47d6  guidance/web-editions.md
a9ab0db78a697cb2519ce0aa3a3b9569ddf83ec4d97cb09b0f0f4bf67f6f97a4  guidance/liturgy/propers-three-documents.md
```
