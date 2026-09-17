# Initial independent review — CHANGES_REQUIRED

Scope: frozen `tools/web-edition`, `tools/tests/test_web_edition_conversion.py`,
`guidance/web-editions.md`, and `guidance/liturgy/propers-three-documents.md`
against `78d8ce505`. The review did not alter those subjects or any publication,
workflow run, staged entry, installed output, or global build output. All created
resources are under `.scratch/anchors-cold-review/`; every Python conversion/test
invocation set `TMPDIR="$PWD/.scratch/anchors-cold-review"` and
`PYTHONDONTWRITEBYTECODE=1`.

## Findings

1. **P2 — Validate the complete rendered publication, including its title.**
   `tools/web-edition:993` captures anchors from Pandoc's body output; lines
   1016–1021 add the publication title only after the uniqueness audit. The
   valid schema-2 fixture `fixtures/title-inline-collision/` has
   `pdftitle={Proper collect}` and exactly one explicit source-owned
   `\label{proper-collect}` immediately before the Collect paragraph. Conversion
   succeeds. Rendering its final Markdown with the actual
   `tools/public-alpha` `render_page` function produces two
   `id="proper-collect"` targets, one on the H1 and one on the paragraph span.
   The retained fragment now encounters the H1 first.
   **Required result:** audit the complete final publication using anchor
   behavior corresponding to the actual site; either produce exactly one
   correct proper target or refuse the conversion. Add a regression exercising
   title collision with an inline paragraph target. Owner: converter/tests.

2. **P2 — Refuse unresolved explicit proper fragment links in schema 2.**
   `tools/web-edition:601–609` retains the legacy unlink-on-missing behavior even
   when a schema-2 anchor inventory is supplied. In
   `fixtures/missing-link/`, the manifest and source correctly declare
   `proper-collect`, but `\hyperref[proper-typo]{the Collect}` names no target.
   Conversion succeeds and changes it to the plain words `the Collect`; the
   later audit cannot detect a link already erased. A styled link reproduces
   the same loss (`fixtures/proper-missing-ref-styled/`).
   **Required result:** preserve valid schema-2 inline fragments and fail
   explicitly for unresolved proper fragment targets before unlinking them;
   leave schema-1 behavior unchanged. Add the corresponding negative test.
   Owner: converter/tests.

## Verification and evidence

Commands below run from the repository root. Python commands use the two
variables stated above.

| Command | Exit | Result |
| --- | ---: | --- |
| `/usr/bin/python3 -m unittest tools.tests.test_web_edition_conversion tools.tests.test_web_edition` | 0 | 80 tests, 6.726 seconds, OK, no skips reported; `unit-tests-initial.log`. |
| `/usr/bin/python3 .scratch/anchors-cold-review/probe.py` | 0 | 19 diagnostic fixtures; `probe-initial.log` and `probe-results-initial.json`. The script records acceptance/refusal and actual site IDs, so exit 0 means probes completed, not that the subject passed. |
| `/usr/bin/python3 .scratch/anchors-cold-review/probe_extra.py` | 0 | 10 further diagnostic fixtures; `probe-extra.log` and `probe-results-extra.json`; includes the actual-site duplicate-ID reproduction. Same exit qualification. |
| `git show 78d8ce505:tools/web-edition > .scratch/anchors-cold-review/before-web-edition` | 0 | Baseline tool obtained independently from Git. |
| `/usr/bin/python3 .scratch/anchors-cold-review/legacy_compare.py` | 0 | All 20 extant schema-1 publications regenerated with both tools; 20/20 outputs byte-identical. Script adapted from the author's comparison with only the scratch destination changed; baseline bytes were freshly extracted. Per-publication hashes in `legacy-comparison.json`; log in `legacy-comparison.log`. |
| `sha256sum --check .scratch/anchors-cold-review/initial-subjects.sha256` | 0 | All four reviewed subjects unchanged at final check. |
| `git diff --check -- tools/web-edition tools/tests/test_web_edition_conversion.py guidance/web-editions.md guidance/liturgy/propers-three-documents.md` | 0 | No whitespace errors. |

The probes independently confirm active print/synthesis branch selection and
comment exclusion; preservation of valid explicit heading, paragraph, and
ordinary inline-label links; and safe refusal of missing/duplicate/undeclared
source labels and macro-discarded/duplicated/undeclared rendered proper labels.
HTML ID examples inside code do not satisfy rendered coverage. Verbatim TeX
label examples can trigger source-label errors, and nested edition conditionals
are not reliably selected by the inherited regex parser; both examples refused
safely and do not support an additional acceptance finding here.

Pandoc and the actual site do not have an identical general anchor model:
repeated automatic headings use `other-1` versus `other_1`, and numbered
unnumbered headings and footnotes differ too. Source-owned explicit proper
labels worked in the tested supported heading/paragraph cases. A Pandoc body
inventory alone therefore does not prove complete final-site correspondence.

The guidance delta is small, keeps the detailed rule under the web-edition
owner, distinguishes source placement judgment from conversion fidelity, and
does not introduce cross-calendar role inference. Its claim of unique rendered
targets awaits finding 1's repair.

No schema-2 leaf acceptance was inferred from this converter review. The
current sources' missing anchors were an explicitly pending author repair,
not a regression. No theological, source-evidence, whole-formulary editorial,
new PDF, visual, or publication acceptance was performed or claimed.

## Frozen subject hashes

```text
45f7f09ccc7c12531ffa7cca4cefd00cd4cbca7c987f05e666bdcffcacae0748  tools/web-edition
3e4e8e1d01365ef6ede5439f59767b5a1156dbeacb42a757cc40d0d7762e104e  tools/tests/test_web_edition_conversion.py
b786dea6d618896926cd7c2a5762f161c11dfee5092ffa463233f6f96ead47d6  guidance/web-editions.md
a9ab0db78a697cb2519ce0aa3a3b9569ddf83ec4d97cb09b0f0f4bf67f6f97a4  guidance/liturgy/propers-three-documents.md
```

Setup note: the author's `subjects.sha256` listed
`e8c903dd835fd00b618745299ff513409c675b012a3995b39bff6e34133a6af5`
for the three-document profile. The coordinator confirmed a line-wrap-only edit
before this review, designated the actual `a9ab…` bytes as the subject, and
held all four files unchanged thereafter. Initial/current hashes above are the
reviewed state; the stale manifest was not treated as proof of the subject.
