# Validation record

Validated on 2026-08-26. The v0.21 checkpoint and the recovered scene corpus
pass their structural, identity, and repository-integration checks.
Repository-wide checks also expose unrelated inherited drift recorded below.

## Canonical corpus

Run from this directory:

```sh
./validate.py
./render-storyboards.py --check
```

Result:

```text
PASS: v0.21 corpus (12 checksummed retained assets)
PASS: recovered scene corpus (197 scenes, 50 checksummed authored files, 21 storyboards)
PASS: 21 storyboards are current
```

The validator performs these checks on the transported checkpoint:

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

And these on the recovered scene corpus:

- parses `scenes/inventory.yaml`, the four contract files, and all 21 section
  files, and proves the registry and the section files implement each other
  exactly — same cluster, order, title, condition, file and linkage;
- proves `order` is dense and 1-based over all 197 scenes, that the
  predecessor/successor chain is coherent, and that every conditional block
  reconnects through a `bypass_successor` declared on the scene that gates it;
- resolves every enumerated value against the vocabularies it reads out of
  `scenes/schema.md`, and every anchor, mensa position, viewpoint, condition
  and invariant id against `geometry.yaml`, `conditions.yaml` and
  `invariants.yaml`;
- proves each scene lists the priest, AC1 and AC2 exactly once, cites at least
  one invariant, and cites only invariants whose declared range governs its
  cluster;
- proves `depth_rank` agrees with the depth of each actor's anchor, so a scene
  cannot silently invert who stands nearer the viewer, while still allowing two
  actors at one depth to differ in rank — which is how the two post-ablution
  crossings record who is in front;
- proves every variant is marked `baseline: false`, and that the Missal's
  reading orientation is `priest-reads-facing-left` wherever it appears;
- refuses each named stale contradiction, listed under **Contradiction guard**
  below; and
- verifies every hash in `MANIFEST-AUTHORED.sha256` and proves it covers the
  authored layer exactly, with nothing missing and nothing stale.

`render-storyboards.py --check` separately proves that all 21 tracked
storyboards are byte-identical to what the current scene corpus generates, so a
storyboard cannot drift from the records it projects.

## Recovered corpus shape

| Measure | Value |
| --- | --- |
| Scenes | 197, `LM-001A` through `LM-140C` |
| Clusters | 125 |
| Span | Prayers at the Foot of the Altar through the Leonine prayers and the recessional |
| Conditional scenes | 14, in three blocks: Gloria in excelsis, Credo, Leonine prayers |
| Declared variants | 19 across 15 scenes: 7 seasonal, 7 Requiem, 3 serving-profile, 1 local custom, 1 exposition |
| Serving-profile parameters left open | 85, each an explicit `unresolved` entry |
| Bell cues | 11 |
| Server responses | 81 |
| Object state records | 1326 |

Every scene is repository-authored recovery, derived only from the approved
handoff summary and `recovery/approved-choreography-baseline.md`. No scene was
reconstructed from the older `altar-server-guides/` tree.

## Contradiction guard

`validate.py` fails the corpus outright if any scene asserts one of these,
each of which the approved baseline rejects:

| Rejected | Where the guard bites |
| --- | --- |
| AC2 moving the Missal before the Gospel | LM-029 to LM-035 |
| AC1 moving the Missal after the ablutions | LM-136 |
| AC2 assisting the post-Communion ablutions, or supplying the water | LM-136A, LM-136B |
| The first ablution not of wine, or the second not of water | LM-136A, LM-136B |
| A first crossing with AC1 in front, or a second with AC2 in front | LM-136C, LM-136E |
| Three rings concentrated at an elevation, or any ring by AC2 | the six Consecration cues |
| Fewer than three AC1 rings at the priestly *Domine, non sum dignus* | LM-134C |
| A bell at the minor elevation | LM-112C |
| Both servers assisting the ascent, or neither | LM-013B |
| A priest-only sign of the cross at the Indulgentiam | LM-010A |
| The Gloria in excelsis said anywhere but the centre | LM-022 to LM-024 |
| The corporal handled at the Offertory, it being already unfolded | LM-054 to LM-078 |
| A dismissal conditioned on whether the Gloria was said | LM-138B |

The supplied `LOW-MASS-END-BRANCHES-1962-v0.1.yaml` ended with a bare mapping
key and could not parse. Its byte-identical SHA-256-verified form is retained as
`transport-originals/LOW-MASS-END-BRANCHES-1962-v0.1.yaml.transport-invalid`.
The canonical `.yaml` adds only the missing `: yes`; `validate.py` verifies that
exact transformation. Thus every file presented as a canonical YAML input
parses, while the transport defect remains reproducible.

## Vector and raster assets

All 21 generated structural storyboards passed `xmllint --noout` and a real
`rsvg-convert` raster conversion. They are 2448 pixels wide with a height set
by their content; the largest, `01-prayers-at-the-foot-v0.1.svg`, renders at
2448 by 3851, and the smallest, `17-ablutions-and-coordinated-transfer-v0.1.svg`,
at 2448 by 1306. No raster projection of them is tracked: they are generated
review projections, and `render-storyboards.py --check` is the durable proof
that they are current.

These storyboards carry labels. That is deliberate and does not breach the
wordless-plate rule of `guidance/liturgy/roman-1962-pictorial-dictionaries.md`,
which governs publication-facing illustration. These are structural review
projections of the deterministic-skeleton stage, not plates.

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

A full repository sweep for the sixteen named contradictions was then run over
every tracked `.md`, `.tex`, `.toml`, `.yaml`, `.py` and `.svg` file. Eleven of
the sixteen have no contradiction anywhere in the repository. The five that do
— the elevation bell grouping, the conditional *Domine, non sum dignus* rings,
the second-ablution liquid, the post-ablution transfer object, and an
unrestricted alb assistance — are confined to pre-checkpoint records, which are
fenced rather than rewritten:

- the LM-136/LM-137 v0.1 PNG remains segregated under `review-history/`; and
- fifteen pre-checkpoint records now carry a `Historical / pre-v0.21` notice in
  their own text: `altar-server-guides/shared/low-mass-ceremony.tex` and
  `low-mass-diagrams.tex` as `%` comments that cannot change rendered output;
  the eight `altar-server-guides/research/` records, the two `01-low-mass*`
  guide maps and the two `01-low-mass*` staleness reviews as Markdown
  blockquotes; `roman-sanctuary-dictionary/research/low-mass-chronology-audit.md`
  likewise; and `roman-sanctuary-dictionary/.../altar-bells.toml` as an
  extension of its existing `editorial_note`.

The notice names the four bell, ablution and transfer divergences explicitly
and points at the governing guidance, so a reader who arrives at one of those
files by search learns at once that it is not an input to this lane. The two
staleness reviews carry an added sentence saying that their "no disagreement"
verdicts mean agreement with the guide's own teaching model, not with the v0.21
baseline — without it those files read as positive verification of the
superseded choices. `guidance/liturgy/roman-1962-pictorial-dictionaries.md`,
which governs the chronology audit and previously carried no fence at all,
gained a `Relationship to the pictographic structural checkpoint` section.

Every one of those edits is additions-only; no existing sentence was rewritten,
corrected, or removed, no PDF was rebuilt, and the guides were not republished.
The owner README and `guidance/liturgy/roman-1962-server-training.md` continue
to state the fence from the pictographic side.

## Repository checks

The following checkpoint-relevant checks pass:

- `git diff --check`;
- `tools/tpt check-promised-deliverables`, and
  `--require-complete mass-pictographic-low-mass-scene-corpus`;
- `tools/tpt source-inventory check`, after
  `source-inventory refresh --audited-on 2026-08-26`;
- `python3 -m unittest tools.tests.test_source_inventory` (31 tests);
- `python3 -m unittest tools.tests.test_low_mass_model` (4 tests); and
- `python3 -m unittest tools.tests.test_mass_pictographic_corpus` (10 tests),
  the new suite that runs this owner's validator and storyboard check inside
  `make check-tests`, and asserts the locked corrections independently of the
  validator that enforces them.

### One check that could not be cleared

`tools/tpt source-family-migration refresh` **refuses to run**:

```text
source-family-migration error: ... pinned canonical_catalog_snapshot is stale
```

That snapshot was already stale before this work, and the only flag that gets
past it, `--accept-canonical-catalog`, may be used only after the human ledger
review `guidance/sources.md` requires. Forcing it was declined.

The consequence is recorded rather than hidden: the ledger's
`inventory_snapshot` and five `review_units[*].surface_snapshot` values are now
stale, because this change altered the `.md` and `.tex` surface they are
computed from. No partial write was made — the refresh errored before writing,
so `source-family-migration-v1.toml` is untouched. Clearing this needs the
separate human family review, after which one refresh settles every entry at
once.

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
