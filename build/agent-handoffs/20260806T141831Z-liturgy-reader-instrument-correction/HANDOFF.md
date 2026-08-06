# Liturgical Instrument Round 1 shell correction handoff

- Reviewed commit: `50288ddf9759f56e8a25e4907d8de25e27e25e8f`
- Shell correction: `ab89758e3f3ee165e0141e3605be88051450134b`
- Deployed handoff checkpoint: `c388ab42dfc4f5c7d49abc71596d6bb511af5742`
- Selected direction: Liturgical Instrument
- Review state: candidate; narrow independent re-review open
- Production-integration execution: unauthorized pending re-review
- Public cutover: unauthorized
- Successful corrected Pages run: `31109086658` for
  `c388ab42dfc4f5c7d49abc71596d6bb511af5742`
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

After three repository-clean artifact uploads stopped in GitHub deployment
polling, run `31109086658` completed successfully at 2026-08-06T14:17:40Z.
Direct Day and Propers are HTTP 200/noindex. Deployed CSS
`850e1acacb6f487a5c2f3118388b3fce7b96f9db667e783ba35cdef7d9918b48`
and JS `eb1c1dd5c0c9c7076b74f2187627dc56e39963429212c0a51872df0ea98a9679`
byte-match source. Corrected deployed parity passes.

## Integrity

- `INSTRUCTIONS.md`: `aac369494856665f3c7dd69c2371680a2b25453d54716e34f1352a65b91b0ef4`
- canonical instruction: `aac369494856665f3c7dd69c2371680a2b25453d54716e34f1352a65b91b0ef4`
- `PLAN-AND-CONTINUITY.md`: `d37812b567e461b900f88d843dbd9cabe45f1a14bb8705a3fdbcd435d7784a55`
- canonical continuity: `d37812b567e461b900f88d843dbd9cabe45f1a14bb8705a3fdbcd435d7784a55`
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
