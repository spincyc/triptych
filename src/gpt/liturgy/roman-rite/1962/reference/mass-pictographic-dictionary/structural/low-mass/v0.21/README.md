# Spoken 1962 Low Mass structural checkpoint v0.21

Status: **structural pass complete and human-approved through v0.21, and the
detailed scene corpus is complete**.

Publication-quality artistic rendering: **not started**.

This directory holds two layers, and the distinction is load-bearing. The
**transported** layer — `handoff/`, `sources/`, `review/`, `review-history/`
and `transport-originals/` — is supplied bytes, preserved unchanged. The
**repository-owned** layer — this file, `VALIDATION.md`, `corpus.yaml`,
`MANIFEST.sha256`, `validate.py`, and the later `scenes/`, `recovery/`,
`storyboards/` and `render-storyboards.py` — is written here. Every authored
file says so in its own `provenance` field, and the authored corpus is
checksummed separately in `MANIFEST-AUTHORED.sha256` rather than folded into the
transport manifest. See [`recovery/recovery-notes.md`](recovery/recovery-notes.md).

This directory preserves the useful contents of the supplied
`mass-pictographic-handoff-v0.21.tar.gz` package and adds repository-owned
routing, classification, checksums, and validation. The transport archive
itself is not tracked because it would duplicate every retained payload.
One supplied YAML file had a missing final mapping delimiter; its original
bytes are retained under `transport-originals/`, while the authoritative copy
under `sources/` has the minimal serialization repair described below.

## Authority order

1. [`handoff/HANDOFF-SUMMARY.md`](handoff/HANDOFF-SUMMARY.md) is the
   authoritative approval record for this checkpoint.
2. [`recovery/approved-choreography-baseline.md`](recovery/approved-choreography-baseline.md)
   preserves the approved scene-by-scene choreography verbatim. It refines the
   handoff summary and never overrides it.
3. [`scenes/`](scenes/) is the machine-readable structural corpus recovered
   from 1 and 2. [`scenes/inventory.yaml`](scenes/inventory.yaml) is its spine:
   every canonical scene exactly once, in reading order.
4. [`corpus.yaml`](corpus.yaml) classifies the retained files and maps their
   scene coverage without changing the imported bytes.
5. `sources/` contains the current machine-readable YAML and deterministic SVG
   supplied in the handoff.
6. `storyboards/` contains structural review projections generated from
   `scenes/`. They are regenerated, never hand-edited, and never authority.
7. `review/current/` contains durable raster review projections. They help a
   later agent see what was approved, but do not replace the structured
   sources.
8. `review-history/` contains useful superseded projections. Nothing in that
   directory may control choreography, object state, or a new render.
9. `transport-originals/` preserves a byte-identical supplied file when a
   parsing defect required a distinct canonical copy.

The embedded `status: structural-review` in
`LOW-MASS-END-BRANCHES-1962-v0.1.yaml` records that file's earlier local state.
The later v0.21 handoff approval governs the checkpoint; the imported file is
not reinterpreted to change that status.

The supplied ending-branches file ended with a bare mapping key and therefore
was invalid YAML. The canonical source adds only `: yes` to that key, matching
the key's imperative wording and the surrounding `yes`/`no` convention. The
invalid original is preserved byte-for-byte at
`transport-originals/LOW-MASS-END-BRANCHES-1962-v0.1.yaml.transport-invalid`.
The suffix prevents tooling from mistaking that provenance record for a
canonical YAML input; no branch or choreography value was otherwise changed.

## Locked baseline

The handoff summary owns the complete wording. A continuing agent must retain
at least these constraints:

- the form is the spoken 1962 Roman Low Mass with two servers;
- Acolyte 1 is the Epistle-side acolyte and Acolyte 2 is the Gospel-side
  acolyte;
- Acolyte 1 transfers the Missal to the Gospel side before the Gospel;
- Acolyte 2 returns the Missal to the Epistle side only after the vessels are
  cleansed;
- the Missal is always oriented so the priest reads facing left;
- priest and servers begin side-to-side, the servers turn inward and bow for
  their Confiteor response, and the altar shows all steps;
- all three sign themselves at the Indulgentiam;
- only Acolyte 1 gives the specified ascent assistance, and the priest says
  the Gloria standing at the altar center;
- the spoken-Low-Mass Consecration profile has one warning bell, then one ring
  at the first genuflection, one at the elevation, and one at the second
  genuflection for each species; a minor-elevation bell is not baseline;
- after the Consecration the priest retains the approved thumb/index discipline
  until the finger ablutions, apart from handling the Sacred Host;
- during the Pater noster the priest looks at the Sacred Host, and during the
  Agnus Dei he strikes his breast three times with the three free fingers;
- Acolyte 1 rings once at each of the three priestly *Domine, non sum dignus*
  openings;
- Acolyte 1 alone serves the ablutions: first wine with the chalice on the
  altar, then water with the priest holding the chalice while Acolyte 1 steps
  down one step;
- after the vessels are cleansed, Acolyte 1 carries the chalice cloth to the
  Gospel side while Acolyte 2 carries the Missal to the Epistle side; Acolyte
  2 leads the first crossing, the priest receives the cloth, Acolyte 1 leads
  the second crossing, and both resume their ordinary kneeling positions; and
- the normal 1962 dismissal is *Ite, missa est*; *Benedicamus Domino* is used
  when another function or procession follows, and Requiems use
  *Requiescant in pace*. Gloria presence does not select the dismissal.

Where the final storyboard uses the compressed label `chalice veil / chalice
cloth`, the handoff summary and the structured
`post_ablution_transfer.first_acolyte` value control: the approved object is
the chalice cloth. Do not expand that wording by inference.

## Asset disposition

Current sources and projections:

- two YAML files: the ablution/service/object state and the 1962 ending
  branches;
- one SVG deterministic storyboard source for LM-137 through LM-140;
- one corrected LM-134/LM-135 raster review sheet; and
- the raster projection of the LM-137 through LM-140 SVG.

`MANIFEST.sha256` covers the retained handoff payloads, the canonical repaired
YAML, and the preserved invalid original. The original archive identity is
recorded in `corpus.yaml`.

Historical review records:

- `LM-134-135-priest-communion-storyboard-v0.1.png` is superseded by v0.2,
  which records Acolyte 1's three *Domine, non sum dignus* bell cues; and
- `LM-136-137-ablutions-communion-antiphon-storyboard-v0.1.png` predates the
  approved AC1-only ablution and coordinated-crossing correction. It assigns
  Acolyte 2 part of the ablution service and must never be used as current
  choreography.

The handoff certifies completion of the whole structural pass, but the
transport archive contained standalone detailed assets only for late scenes,
concentrated on LM-134 through LM-140. Earlier approved scenes were attested by
the handoff summary alone and were not present in the package as standalone
YAML, SVG, or PNG files.

That gap is closed. `scenes/` now carries the whole spoken Low Mass as
machine-readable scene records, recovered from the handoff summary and the
preserved approved choreography. The older sibling `altar-server-guides/`
records were **not** used, and must still never be substituted for approved
material without a separate human reconciliation. They now carry a
`Historical / pre-v0.21` notice in their own text so that fence is visible from
inside each of them.

## Validation

From this directory, run:

```sh
./validate.py              # the whole checkpoint, transported and authored
./render-storyboards.py --check   # prove the storyboards match the corpus
```

Both also run from the repository root by their full path.

For the transported checkpoint the validator parses the canonical YAML and SVG,
checks retained-asset hashes, resolves the manifest's cross-file links,
compares SVG and projection scene IDs, and asserts the structured state against
the approved handoff invariants.

For the recovered corpus it additionally proves that `scenes/inventory.yaml`
and the section files implement each other exactly; that `order` is dense and
the predecessor/successor chain is coherent; that every conditional block
reconnects through a declared `bypass_successor`; that every enumerated value,
anchor, viewpoint, condition and invariant resolves; that each scene lists all
three actors and cites only invariants that govern its cluster; and that no
scene asserts any of the named stale contradictions — the rejected bell
groupings, the wrong Missal or ablution roles, the wrong crossing order, a
priest-only Indulgentiam, the Gloria at the Missal, a corporal unfolded at the
Offertory, or a Gloria-conditioned dismissal.

See `VALIDATION.md` for image checks, the contradiction audit, and the
inherited repository-wide check baseline.

## Next artistic lane

The next fresh human-guided session should consume `scenes/inventory.yaml` in
`order`, the scene records it names, `sources/`, the current review
projections, and the handoff summary. It should begin with a sanctuary
master/style anchor and then proceed through opening rites, ascent and
ordinary, readings, Offertory, Canon and Consecration, Communion and ablutions,
and concluding rites. Every resulting plate must retain its structural scene
IDs and metadata linkage.

That lane creates the first publication-quality graphite/pencil assets. It
does not revise the approved structural choreography. The 1962 sung forms,
pontifical forms, postconciliar forms, object compendium, and final site/manual
integration remain unstarted here.
