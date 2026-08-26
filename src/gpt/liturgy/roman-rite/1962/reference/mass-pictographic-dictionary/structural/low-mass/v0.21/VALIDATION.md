# Validation record

Validated on 2026-08-26. The v0.21 checkpoint passes its structural,
identity, and repository-integration checks. Repository-wide checks also expose
unrelated inherited drift recorded below.

## Canonical corpus

Run from the repository root:

```sh
src/gpt/liturgy/roman-rite/1962/reference/mass-pictographic-dictionary/structural/low-mass/v0.21/validate.py
```

Result:

```text
PASS: v0.21 corpus (12 checksummed retained assets)
```

The validator performs these checks:

- parses `corpus.yaml` and both canonical source YAML files with PyYAML;
- verifies all paths and cross-file `source`, `superseded_by`, provenance, and
  canonical-repair references in `corpus.yaml`;
- verifies every hash in `MANIFEST.sha256`;
- confirms the package identity recorded in `corpus.yaml`;
- checks the approved spoken/two-server boundary, AC1-only service and object
  state, coordinated crossing order, 1962 dismissal branches, and not-started
  artistic state;
- checks the locked role, Missal-orientation, bell, ablution, crossing, and
  dismissal statements remain in the authoritative handoff summary; and
- parses the SVG as XML, expands its compressed labels, and proves that its 11
  scene IDs exactly match `corpus.yaml` and the current raster projection.

The supplied `LOW-MASS-END-BRANCHES-1962-v0.1.yaml` ended with a bare mapping
key and could not parse. Its byte-identical SHA-256-verified form is retained as
`transport-originals/LOW-MASS-END-BRANCHES-1962-v0.1.yaml.transport-invalid`.
The canonical `.yaml` adds only the missing `: yes`; `validate.py` verifies that
exact transformation. Thus every file presented as a canonical YAML input
parses, while the transport defect remains reproducible.

## Vector and raster assets

The retained SVG passed both XML validation and a real raster conversion:

```sh
xmllint --noout sources/LM-137-140-final-low-mass-storyboard-v0.1.svg
rsvg-convert sources/LM-137-140-final-low-mass-storyboard-v0.1.svg -o <scratch-output>.png
```

The render was 2460 by 2140 RGB pixels. ImageMagick decoded all four retained
PNGs without warning:

| Classification | Asset | Dimensions |
| --- | --- | --- |
| current | `LM-134-135-priest-communion-storyboard-v0.2.png` | 2440 x 2060 |
| current | `LM-137-140-final-low-mass-storyboard-v0.1.png` | 2460 x 2140 |
| history | `LM-134-135-priest-communion-storyboard-v0.1.png` | 2440 x 2030 |
| history | `LM-136-137-ablutions-communion-antiphon-storyboard-v0.1.png` | 2440 x 2060 |

All four PNGs were also inspected visually at review resolution. The current
projections are readable and consistent with their classifications. The old
LM-136/LM-137 projection visibly carries superseded ablution choreography and
therefore remains only under `review-history/`.

## Contradiction audit

Case-insensitive searches covered the new owner and the existing sibling
altar-server guide for the five named stale patterns. The authoritative YAML
contains none of the rejected baselines: it assigns no ablution role to AC2,
assigns the post-ablution Missal to AC2, defines no generic book-server role,
and contains no Gloria-controlled dismissal branch. The final SVG's reference
to `no Gloria = Benedicamus Domino` explicitly rejects that shortcut and is
not a competing rule.

Two historical or pre-checkpoint locations do contain superseded choices, and
are intentionally fenced from current inputs:

- the LM-136/LM-137 v0.1 PNG is segregated under `review-history/`; and
- the existing `altar-server-guides/research/scope.md` and
  `altar-server-guides/shared/low-mass-ceremony.tex` use an earlier selected
  bell grouping, Communion condition, second-ablution liquid, and transfer
  object.

The new owner README and `guidance/liturgy/roman-1962-server-training.md`
explicitly state that those guide records are not source material for the
v0.21 pictographic lane. They were not rewritten or republished in this
preservation task.

## Repository checks

The following checkpoint-relevant checks pass:

- `git diff --check`;
- `tools/tpt check-promised-deliverables`;
- `tools/tpt source-inventory check`; and
- `python3 -m unittest tools.tests.test_source_inventory -v` (31 tests).

The repository-wide `make check` remains red on an untouched stale Claude web
edition at
`web/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s42-sixteenth-sunday-in-ordinary-time-year-a.md`.
A keep-going run additionally reaches the repository's existing stale calendar
and example transcripts. `make check-sources` clears the new owner's source
inventory and migration-review-unit integration, then remains red because the
pre-existing source-family ledger's pinned canonical catalog predates many
reviewed family memberships. Separately, `tmt check` reports the same eight
undeclared sibling-tool dependencies present before this import. None of those
inherited findings is changed by the pictographic checkpoint.
