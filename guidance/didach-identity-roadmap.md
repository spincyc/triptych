# didach.ai identity roadmap

## Status

The governing future origin is `https://didach.ai/`. The identity described in
`guidance/didach-identity.md` is a review candidate, not an accepted production
identity. This roadmap owns execution evidence, review questions, disposition,
and the next safe action. It does not own the durable design rules themselves.

## Work unit ID0 — identity and root corpus design

| Field | Value |
| --- | --- |
| State | In progress |
| Branch | `ux/didach-identity` |
| Base | `origin/main@fc3092de98fee56ab09c406ade257e84e7633e45` |
| Foundation inspected | `3b5938a0dba88831763ec09c762ae1572007a27e` |
| Wave 1 inspected | `e42b9287485a5a6d18ad8a528ab0f0f3f0024ff9` |
| Review fixes inspected | `c66c143643ff75a6cd54afdbe1fcd6eac0aca1b6` |
| Durable identity owner | `guidance/didach-identity.md` |
| Research owner | `guidance/didach-identity-research.md` |
| Prototype | `src/web/browser/prototypes/didach-identity/` |
| Matrix | `tools/tests/fixtures/didach-identity-prototype-matrix-v1.json` |
| Browser harness | `tools/tests/didach_identity_prototype_browser.mjs` |
| Production boundary | No URLs, DNS, Pages config, release binding, public asset, PDF, publication, canonical Liturgy, merge, or deployment change |

### Candidate completion gates

- The accepted and still-candidate design boundaries are explicit.
- Linguistic, theological, product, scholarly, typographic, accessibility,
  discoverability, rights, and adjacent-name research is tracked with sources.
- One recommended public name and hierarchy is shown, not a theme gallery.
- Real Home, Publications, Reader, Catena, and Sources data exercises the
  identity without copying publication or source prose into the prototype.
- Naming, masthead, Home, footer, 404/empty/rights states, icon, social card,
  responsive, forced-color, no-JavaScript, and print consequences are visible.
- C0, C1, D0, and E0 remain compositionally intact; F0/shell correction remains
  labelled candidate; Liturgy bytes remain identical.
- Focused static and browser gates pass, every screenshot is inspected at full
  resolution, and the review ZIP has one root and a verified manifest.
- Automated 320-CSS-pixel reflow is distinguished from diagnostic CDP page
  scale; the still-required native-browser 400% zoom check is disclosed rather
  than claimed as candidate evidence.
- The feature branch is pushed without a Pages deployment.

Reaching these gates changes the ledger state to `candidate`, never `complete`.
Independent acceptance and the separately authorized production migration are
still outstanding.

## Open identity questions

| ID | Blocking | Evidence | Candidate recommendation | Decision owner |
| --- | --- | --- | --- | --- |
| IQ-1 public name | Yes | identity sheet; Home wide/mobile; research naming section | exact lowercase `didach.ai`; no Didach or Didach AI UI alias | Independent identity reviewer |
| IQ-2 adjacent-name risk | Yes for launch | research collision record | preserve exact spelling and descriptor; obtain real legal/name clearance before launch | Maintainer/legal review |
| IQ-3 `.ai` prominence | Yes | masthead, Reader, card captures | same face/size/weight/color; context changes the whole mark | Independent identity reviewer |
| IQ-4 Triptych role | Yes | footer, Reader colophon, transition spec | project/repository/legal/history only; one temporary provenance sentence | Maintainer and identity reviewer |
| IQ-5 wordmark | Yes | identity sheet; fallback and forced-color captures | live editorial-serif text; no companion logo | Independent identity reviewer |
| IQ-6 small icon | Yes | typographic direction at 16/32/180/192/512 plus `d`/`d.` comparison; final geometry still open | strengthened lowercase `d`; no dot at 16; no independent symbol | Independent identity reviewer |
| IQ-7 social card | Yes | exact generic 1200×630 specimen and metadata section; object, long-title, and multilingual production variants remain open | deterministic scholarly folio; review text-in-image/platform tradeoff before defining the full family | Independent identity reviewer |
| IQ-8 Home | Yes | before/after five-viewports; task and portal captures | corpus-first H1, six task entrances, seven portals, later trust copy | Independent product reviewer |
| IQ-9 shared shell | Yes | non-Liturgy wide/compact captures | wordmark Home; one current place; distinct Browse/Menu and Jump | Independent product/accessibility reviewer |
| IQ-10 protected Liturgy consequence | Yes before any implementation | unchanged Liturgy oracle plus written atomic before/after | replace in place only after liturgy-specific approval; no added shell or action | Liturgy coordinator/reviewer |
| IQ-11 dark mode | No | light and forced-color captures | remain light; defer dark until whole-site token review | Maintainer |
| IQ-12 public cutover | Yes before implementation | transition/metadata sections | one coordinated later migration; no identity-lane URL change | Maintainer/deployment owner |
| IQ-13 native zoom and platform evidence | No for candidate; yes before production acceptance | exact 320-CSS-pixel reflow plus explicitly diagnostic CDP page-scale captures | conduct real native-browser 400% zoom and cross-platform assistive-technology checks after a production implementation exists; do not treat CDP scale as a substitute | Independent accessibility reviewer |

## Evidence ledger

- 2026-08-08: feature branch created exactly from current `origin/main`; unrelated
  untracked `directions` preserved.
- 2026-08-08: accepted UX and Wave-1 branches inspected without wholesale merge.
- 2026-08-08: identity promise recorded before implementation.
- 2026-08-08: linguistic, naming-collision, scholarly-library, academic-press,
  digital-humanities, metadata, accessibility, asset-rights, and repository-owner
  research synthesized in tracked guidance.
- 2026-08-08: real-route prototype and its dependency-free Chromium/static
  harness selectively derived from the review-fix seam under a new noindex,
  structurally unpublished path.

The final candidate-state commit precedes packaging so the handoff can bind one
exact immutable head without a self-referential repackage loop. The handoff
records that head, commit list, checks, capture count, basename, and push
verification. A sibling checksum file and the final report record the completed
ZIP digest; no file inside the ZIP claims its container's self-referential hash.
Append the independent disposition here when one is actually received;
`requested; pending` is the only truthful pre-review disposition.

## Next safe action

Finish and inspect the focused browser matrix, commit and push only the exact
`ux/didach-identity` candidate, then package a fresh ignored handoff and request
independent review of IQ-1 through IQ-10 and IQ-12, plus explicit affirmation of
IQ-11's dark-mode deferral and IQ-13's production-acceptance boundary. Do not
modify production identity consumers until that disposition is recorded and a
separate implementation task is authorized.
