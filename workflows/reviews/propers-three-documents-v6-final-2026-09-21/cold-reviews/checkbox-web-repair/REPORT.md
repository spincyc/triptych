# Ancillary web checkbox repair

Date: 2026-09-22

## Verdict

PASS. The web converter now preserves every print-only `\checkbox` call as a
semantic empty-checkbox glyph (`☐`). The 1962 assembly worksheet's sixteen
table markers and eight independent-review list markers survive conversion;
the previously emitted bare `-` blocks are absent. The TeX publication source
and PDF behavior were not changed.

## Implementation

- `scripts/web-shim.tex` defines `\checkbox` as `☐` before leaf-local print
  definitions. Pandoc keeps the first macro definition, so the converter sees
  semantic content instead of the local empty `\fbox`/`\rule` geometry.
- `tests/tools/web-edition.test` converts the real assembly worksheet, derives
  the expected count from `sections/95-checklist.tex`, checks exact count
  preservation, and proves a marker remains attached to one table row and one
  list item.
- `web/gpt/liturgy/roman-rite/1962/reference/assembling-the-mass.md` was
  regenerated from the unchanged source and installed byte-for-byte from
  `build/web/...`.
- `release/public-alpha.json` and
  `release/rights/public-alpha-2026-07-15.md` were refreshed through
  `tools/tpt release-bindings refresh --only
  web/gpt/liturgy/roman-rite/1962/reference/assembling-the-mass.md`. The shared
  files already contained the parent task's other pending binding changes; the
  scoped refresh recorded this web edition and its derived rights-record hash.

No file beneath `src/gpt/liturgy/roman-rite/1962/reference/assembling-the-mass/`
was modified.

## Evidence

- Source checkbox calls: 24
- Installed web checkbox glyphs: 24
- Installed web SHA-256:
  `0dd56df65e0d96db9b0e2451c683a7e03d448df7bc1de887f70b997081186196`
- `cmp` between generated and installed Markdown: exact
- Lines containing only `-` in installed Markdown: 0

## Verification

- `tests/tools/web-edition.test`: PASS
- `make check-web-editions-current`: PASS, all tracked editions current
- `tools/tpt release-bindings status`: PASS, 0 stale bindings
- `make check-release-bindings`: PASS, 0 stale bindings
- `git diff --check`: PASS
- `/home/ksh/.local/bin/tmt check --json`: PASS, no failures or warnings

No commit was made.
