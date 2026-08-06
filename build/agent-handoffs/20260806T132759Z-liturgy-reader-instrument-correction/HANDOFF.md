# Liturgical Instrument Round 1 shell correction handoff

- Reviewed commit: `50288ddf9759f56e8a25e4907d8de25e27e25e8f`
- Shell correction: `ab89758e3f3ee165e0141e3605be88051450134b`
- Latest continuity checkpoint: `3873bd99cb308432404378c665dbcb3246144c9e`
- Selected direction: Liturgical Instrument
- Review state: candidate; narrow independent re-review open
- Production-integration execution: unauthorized pending re-review
- Public cutover: unauthorized
- Latest successful Pages run: `31098741792` for the reviewed pre-correction handoff
- Corrected Pages attempts: `31104342722` failed, `31106008011` failed,
  `31107294462` cancelled after verified artifact uploads
- Deployed Day: `https://spincyc.github.io/triptych/liturgy/reader-visual-reset-day.html?design=instrument`
- Deployed Propers: `https://spincyc.github.io/triptych/liturgy/reader-visual-reset-propers.html?design=instrument`

## Outcome

The 1024 shell now transitions directly from the accepted external rail to an
opaque, square, shadowless edge dock, and final content clears its permanent
reserve. At the required 200%-text state, the permanent actions become a
labeled 2×2 grid with whole words, large targets, accessible names, and no
horizontal overflow. The accepted reading measure and text position are
pixel-identical in measured regression states. Modal behavior, focus, forced
colors, normal mobile rhythm, the 1440 rail, and the 320 layout are unchanged.

The authoritative Chromium run passes 15/15 assertions across 54 captures.
The narrow package retains both blocker baselines, 11 corrected original-pixel
states, exact comparison geometry, raw capture metadata, browser results, and
two inspected contact sheets. Capture paths, queries, hashes, and measurements
are exact; only the ephemeral loopback origin is normalized to
`https://preview.invalid` for the tracked review record.

## Deployment disposition

Every corrected Pages attempt passed checkout, locked dependencies, source
verification, public build, GitHub Pages compatibility verification,
configuration, and artifact upload. GitHub then timed out or canceled each job
during deploy-pages polling. Public Day and Propers remain HTTP 200/noindex but
serve reviewed CSS `337a8ce54b0af40eacc8c03425df3bddedb793b804afc49a16aee8cbe73d24eb`,
not corrected CSS `850e1acacb6f487a5c2f3118388b3fce7b96f9db667e783ba35cdef7d9918b48`.
Corrected deployed parity is therefore an explicit external blocker, not a
claimed pass. The runnable package contains the corrected asset and requires no
external request.

## Integrity

- `INSTRUCTIONS.md`: `aac369494856665f3c7dd69c2371680a2b25453d54716e34f1352a65b91b0ef4`
- canonical instruction: `aac369494856665f3c7dd69c2371680a2b25453d54716e34f1352a65b91b0ef4`
- `PLAN-AND-CONTINUITY.md`: `bdf29db80d51e48bd40cf9d81b6dea0ef6edff728e00a97e5dbfe93dff3d2d13`
- canonical continuity: `bdf29db80d51e48bd40cf9d81b6dea0ef6edff728e00a97e5dbfe93dff3d2d13`
- both canonical/handoff pairs: byte-identical by `cmp`

`MANIFEST.sha256` covers every directory file except itself and was generated
last. Its verification, ZIP test, and single-top-level-directory result are in
`checks.txt`.

## Artifact inventory

- exact reviewer message: `REVIEW-ROUND-1.md` and `PLAN-AND-CONTINUITY.md`
- decisions and request: `VISUAL-DECISIONS.md`, `REVIEW_REQUEST.md`
- evidence: `BEFORE-AFTER.md`, `MEASUREMENTS.md`, `evidence/`
- implementation record: `changes.patch`, `changed-files.txt`, `source/`
- executable snapshot: `candidate/`
- checks and bounded stops: `checks.txt`, `logs/`

No independent acceptance is claimed.
