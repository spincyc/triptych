# Liturgical Instrument public-cutover rollback

## Purpose

This is the operational rollback for the selected in-place canonical route
promotion. It uses ordinary commits and GitHub Pages. It never rewrites
history, force-pushes, deletes candidate/oracle surfaces, or edits data to make
a failed reader appear healthy.

## Immediate rollback triggers

Rollback immediately if any of these occurs on the intended deployed commit:

- a required canonical Day or Propers deep link changes meaning, loses state on
  reload/Back/Forward, or stops resolving with HTTP 200;
- valid `why`, locality, option, formulary, or incomplete-coverage state becomes
  recursive, silently falls back, or fabricates content;
- canonical composition materially diverges from the accepted production
  candidate at an equivalent state;
- semantic location, modal focus entry/Escape/inertness/restoration, or one-step
  action access regresses;
- required CSS/JS/data requests fail, console errors appear, or deployed bytes
  disagree with the cutover commit;
- canonical routes are noindex, retained candidate/oracle routes advertise as
  canonical/indexable, or OG/canonical metadata names the wrong surface;
- unnamed controls, duplicate IDs, target-size failures, horizontal overflow,
  forced-colors, reduced-motion, zoom/reflow, or keyboard-focus failures occur;
- Pages does not report a successful deployment for the exact intended commit;
- the 600-second mixed-cache window exposes an incompatible old-HTML/new-JS or
  new-HTML/old-JS combination.

## Mechanism

1. Identify the exact ordinary cutover commit (and any immediately coupled
   exact release-binding commit) from the cutover continuity record.
2. Run `git revert --no-edit <cutover-commit>` for a one-commit cutover. If a
   separately pushed release-binding commit is not contained in that commit,
   revert it in the same ordinary rollback series in reverse order. Do not
   reset, amend, rebase, or force-push.
3. Run the release/publication checks against the reverted tree. The release
   manifest and rights-record digest must describe the restored canonical
   bytes; do not leave the accepted hash record pointing at reverted files.
4. Push the ordinary revert commit(s) to `origin/main` after inspecting the
   exact outgoing range and public disclosure boundary.
5. Require a successful Pages run for the exact revert tip. A workflow polling
   stop is not a successful rollback deployment.

## Deployment verification

Verify first with cache-busting query parameters and `Cache-Control: no-cache`,
then repeat after at least the advertised 600-second freshness window:

```text
/liturgy/day.html?rollback=<revert-sha>#date=2026-08-05&missal=roman-1962&bible=douay-rheims
/liturgy/index.html?rollback=<revert-sha>#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims
```

Required rollback observations:

- HTTP 200 and restored canonical HTML/source hashes;
- canonical index/description/social metadata restored;
- legacy Day and Propers controller assets byte-match the revert tip;
- direct load, reload, Back/Forward, and the two governing hashes resolve;
- no console, failed required request, unexpected HTTP, duplicate-ID, unnamed
  control, or horizontal-overflow problem;
- public navigation still points to canonical filenames;
- retained candidate and oracle routes remain HTTP 200 and noindex.

Record the Pages run number, exact revert SHA, route response headers, asset
hashes, verification UTC, and any cache still serving the superseded cutover.
Do not call rollback complete while the deployed artifact or cache check is
unverified.

## Retained fallback surfaces

`day-reader.html`, `propers-reader.html`, and both accepted visual-reset oracle
routes remain present and unchanged through the initial cutover acceptance
window. Legacy `day.js`, `liturgy.js`, legacy CSS, renderers, adapters, and data
also remain tracked. Initial cutover does not combine route promotion with
candidate/prototype cleanup, controller renaming, data migration, or visual
refactoring.

## Recovery acceptance

The rollback is accepted only when main, origin/main, and remote main agree on
the revert tip; Pages succeeds for that tip; canonical direct/deep-link checks
pass twice across the cache window; and the continuity/tracking record states
that public cutover is rolled back. A later retry requires a new reviewed plan
update and separate authorization.
