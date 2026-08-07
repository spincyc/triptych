# Liturgical Instrument public-cutover acceptance gates

## Authorization boundary

These are gates for a later separately authorized execution. Passing them does
not itself authorize a push, public navigation change, or cutover. The execution
agent must begin from the independently accepted compatibility/plan SHA with a
clean synchronized main. Compatibility commit `3f3949617` resolves the prior
four public-contract dispositions, but cutover execution remains unauthorized
until narrow review accepts those bytes and the regenerated patch.

## Repository preflight

Record exact command, exit code, concise result, and qualification for:

```sh
git status --short
git rev-parse HEAD
git rev-parse main
git rev-parse origin/main
git ls-remote origin refs/heads/main

python3 -m unittest -v \
  tools.tests.test_day_missal_integration \
  tools.tests.test_day_reader_integration \
  tools.tests.test_liturgy_reader_shell \
  tools.tests.test_liturgy_reader_state \
  tools.tests.test_mass_ordinary \
  tools.tests.test_propers_reader_integration \
  tools.tests.test_liturgy_reader_visual_reset \
  tools.tests.test_public_alpha

node --check src/web/browser/liturgy/day-reader.js
node --check src/web/browser/liturgy/propers-reader.js
node --check src/web/browser/liturgy/reader-state.js
node --check tools/tests/day_reader_integration_browser.mjs
node --check tools/tests/propers_reader_integration_browser.mjs
node --check tools/tests/liturgy_reader_shell_browser.mjs
node --check tools/tests/liturgy_reader_visual_reset_browser.mjs

node tools/tests/day_reader_integration_browser.mjs
node tools/tests/propers_reader_integration_browser.mjs
node tools/tests/liturgy_reader_shell_browser.mjs
node tools/tests/liturgy_reader_visual_reset_browser.mjs

tools/tpt check-promised-deliverables
tools/tpt --check
make check-release-bindings
git diff --check
tools/tpt public-alpha check
tools/tpt public-alpha build
tools/tpt public-alpha verify --deployment-target github-pages
make check
```

Expected task-owned results are Day 40/40, Propers 32/32, shared shell 18/18,
governed Instrument assertions 24/24, focused Python all green, exact release
bindings, and locked public-alpha check/build/verify all green. The Day result
must include literal reload and Back/Forward coverage for `why=1` and the
multi-territorial fixture; the visual run must retain the mobile capture
scrolled to the second territorial branch.
`make check` may retain only the already disclosed unrelated stored
example-transcript divergence; its exact exit and stop must be recorded and it
must not be called green. Do not recapture or bless unrelated transcripts.

Before commit, inspect `git status`, the exact staged diff, the outgoing range,
and every newly reachable object. No path outside the independently authorized
cutover/test/release/tracking/handoff set may be staged.

## Canonical-route compatibility harness

The later harness must run against the actual staged/built canonical filenames,
not substitute candidate URLs. It must compare equivalent canonical screenshots
and semantic/browser measurements to the accepted production-reader candidates
and, for visual composition, the accepted Instrument oracle.

Required Day states:

- Read at 1440×900, 1024×768, 768×1024, 393×852;
- Missal at 1440×900, 1024×768, 393×852, 320×852;
- deep-scroll Missal;
- Roman partial coverage;
- postconciliar partial-English desktop/mobile;
- explicit first/default date, Roman 1962, postconciliar, Bible, oration,
  Ordinary, Ordinary language/option, readable formulary;
- direct governing deep link, reload, Back/Forward, malformed state,
  incomplete coverage, modal open/close, and semantic-location restoration.

Required Propers states:

- Read desktop/mobile;
- Browse desktop/mobile;
- Roman seasonal and a verified supported sanctoral formulary;
- postconciliar representative;
- missal/Bible/orations, reload, direct deep link, Back/Forward, malformed and
  unsupported selection, modal open/close, selector behavior;
- any approved public cycle/alternative/translation-witness URL states.

Required shell/accessibility states:

- Date open 1024×768;
- Browse open desktop/mobile;
- Contents open 393×852;
- Mode open 393×852;
- Details open 1440×900;
- 200% text at 393×852;
- keyboard focus and forced colors at 393×852;
- reduced motion at 393×852;
- no horizontal overflow at every required state;
- four named one-step actions with at least 44px targets where governed.

Every capture records exact canonical URL/hash, viewport, effective CSS width,
scroll, identity, mode/outcome, semantic location, focus, geometry, reading
measure, first-principal-text position, overflow, console errors, failed
requests, HTTP errors, duplicate IDs, unnamed controls, and target sizes.

## Visual oracle and parity thresholds

- Equivalent canonical and accepted-candidate states must be materially
  identical: same Instrument stylesheets, DOM hooks, 636px/about-75-character
  Read measure at 768×1024, accepted first-principal-text hierarchy, rail/dock,
  warning hierarchy, ritual cue geometry, narrow title, and mobile rhythm.
- No comparison begins from the old public reader’s geometry.
- Route-specific title, description, robots, counterpart navigation, and an
  independently approved compatibility message are the only intentional
  differences and must be enumerated before capture.
- Any CSS, masthead, typography, measure, ritual, warning, source, or renderer
  delta is a blocker, not “close enough.”

## Publication and indexing gate

The exact cutover source set must have explicit maintainer byte authorization
before release bindings are refreshed. `tools/tpt public-alpha prepare` may
inventory candidate hashes but confers no approval. Refresh only authorized
paths; update `release/public-alpha.json`, the rights-record source table, and
its digest together.

In the built public artifact verify:

- canonical Day and Propers have intended public titles/descriptions,
  `index, follow`, correct absolute OG URLs, and the selected canonical-link
  policy;
- `/liturgy/` and `/liturgy/index.html` remain the explicitly accepted existing
  GitHub Pages host alias for the same built Propers document; no new
  build-pipeline canonical-link parser is introduced by cutover;
- retained `day-reader.html`, `propers-reader.html`, and oracle pages are
  statically noindex/noarchive and carry no public OG/canonical advertising;
- all relative CSS, JS, Home, counterpart, data, and contextual links resolve;
- query and hash text survives without redirect semantics;
- artifact checksums and source bindings match exact files.

No service worker, new CDN, runtime dependency, redirect infrastructure, or
asset pipeline may be introduced merely for cutover.

## Deployment gate

The exact intended cutover commit must have a successful GitHub Pages run with
checkout, locked setup, source verification, public build, Pages compatibility,
upload, and deploy all successful. A polling timeout, queued stop, cancellation,
or success tied to a different SHA is not acceptable.

Direct deployed checks, first cache-bypassed and again after at least 600
seconds, must prove:

- HTTP 200 for canonical base routes and governing deep links;
- deployed/source byte parity for every changed HTML/CSS/JS and release record;
- correct title, description, robots, canonical/OG URL, ETag, Last-Modified,
  and observed cache headers;
- required data/assets return expected status and bytes;
- no console error, failed required request, unexpected HTTP failure,
  duplicate ID, unnamed interactive control, or required overflow;
- reload, Back/Forward, modal focus, semantic location, and valid hash state
  remain correct;
- retained candidates/oracle remain available and noindex;
- repository-owned navigation still reaches canonical filenames.

Any mixed-cache incompatibility is an immediate rollback trigger. Do not claim
deployed cutover until both verification passes and the exact successful Pages
run are recorded.

## Independent acceptance stop

After deployment evidence, stop for independent public-cutover review. Do not
remove or redirect candidate/oracle routes, delete legacy controllers, rename
assets, update navigation labels broadly, begin Study/Compare/search, or clean
up provisional compatibility code until the cutover is independently accepted
and a later cleanup phase is separately authorized.
