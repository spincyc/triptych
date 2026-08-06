# Liturgical Instrument public-cutover route map

## Boundary

This map describes repository state at
`7b7044dea7f5c35a2d32ff85f26eb5b182bf40ef`. It distinguishes the public
contract from replaceable implementation details. It does not authorize or
apply a route, navigation, indexing, candidate, oracle, or cutover change.

## Canonical public contract

| Entrance | Canonical URL | Required stable state carrier | Current source |
| --- | --- | --- | --- |
| Day | `/liturgy/day.html` | query `data`; hash date, missal, Bible, orations, apparatus, Ordinary language/option, readable formulary | `src/web/browser/liturgy/day.html` |
| Propers | `/liturgy/index.html` (also served byte-identically at `/liturgy/`) | query `data` and `missals`; hash missal, type, mass, Bible, orations | `src/web/browser/liturgy/index.html` |

The filenames, valid hash meanings, relative `../browse` data root, direct
reload, and Back/Forward behavior are public contract. The current disclosure
DOM, legacy controller filenames, card styling, and first-item implementation
defaults are implementation detail unless a separately recorded compatibility
decision says otherwise.

These existing URLs must remain directly resolvable without redirects:

```text
/liturgy/day.html#date=2026-08-05&missal=roman-1962&bible=douay-rheims
/liturgy/index.html#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims
```

Representative compatibility URLs are:

```text
# Day: another date and explicit Read
/liturgy/day.html#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&ordinary=0

# Day: postconciliar Missal with a legitimate option
/liturgy/day.html#date=2026-11-29&missal=postconciliar&bible=douay-rheims&orations=la&ordinary=1&ordinary-lang=en&eucharistic-prayer=ep-ii

# Day: incomplete Roman coverage
/liturgy/day.html#date=2026-08-06&missal=roman-1962&bible=douay-rheims&orations=la&ordinary=1

# Day: malformed explicit edition (must fail closed under the accepted reader)
/liturgy/day.html#date=2026-08-02&missal=not-a-missal&bible=douay-rheims

# Propers: Roman seasonal
/liturgy/index.html#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims

# Propers: supported sanctoral representative
/liturgy/index.html#missal=roman-1962&type=sanctoral&mass=s-hilarii-episcopi-confessoris-ecclesiae-doctoris&bible=douay-rheims

# Propers: malformed formulary (must fail closed under the accepted reader)
/liturgy/index.html#missal=roman-1962&type=seasonal&mass=not-a-mass&bible=douay-rheims
```

The exact supported sanctoral key is revalidated from the built structure by
the later execution gate before use; a missing key is a fixture error, not
permission to select a nearby Mass.

## Actual entry-point and loading graph

### Canonical Day

- HTML: `src/web/browser/liturgy/day.html`.
- CSS, in order: `../shared/browser-core.css`, `liturgy.css`, `day.css`,
  `day-missal.css`.
- JavaScript, in order: `../shared/browser-core.js`, `assembly-model.js`,
  `ordinary-seating.js`, `reading-contents.js`,
  `proper-placement-notes.js`, `day.js`.
- DOM/controller owner: `day.js` requires `#reading` and `#controls` and owns
  the current settings/disclosures, resolution, hash writes, and render.
- Data: `?data=` is parsed by `browser-core.js`; default `../browse`.
- Default: local civil date, first rubrics-index calendar (currently
  postconciliar), first Bible, Latin orations, Propers-only, rubrics latent-on.
- URL/history: `T.writeHash` replaces an empty first visit with an explicit
  selection by assigning `location.hash`; later external hash changes rerender.
- Document title: source title `Today’s Missal`; the controller does not update
  it for the selected celebration.

### Accepted Day candidate

- HTML: `src/web/browser/liturgy/day-reader.html`.
- CSS, in order: canonical Day CSS plus `reader-shell.css`, `day-reader.css`,
  and last-loaded `reader-instrument.css`.
- JavaScript, in order: core, assembly, seating, legacy `day.js` (renderer
  export only), `reader-state.js`, `reader-state-adapters.js`,
  `reader-shell.js`, `day-reader.js`.
- `day.js` safely does not initialize because the candidate has no legacy
  `#reading`/`#controls` pair.
- Default: local civil date, declared Propers default (currently Roman 1962),
  first Bible, Latin orations, Read. Day deliberately ignores remembered state.
- URL/history: strict legacy parsing, explicit-invalid fail-closed behavior,
  `pushState`/`replaceState`, `popstate`/`hashchange`, semantic-location and
  focus restoration.
- Candidate-only behavior: JavaScript inserts noindex only when no robots meta
  exists; deployed layout already supplies one, so this does not make the raw
  deployed HTML noindex. The source and runtime title/diagnostics retain
  “internal candidate” wording.
- Deferred current features: `why=1` and multi-territorial outcomes link to
  `day.html`; that becomes a self-link if the controller is promoted unchanged.

### Canonical Propers

- HTML: `src/web/browser/liturgy/index.html`.
- CSS: `../shared/browser-core.css`, `liturgy.css`, `day-missal.css`.
- JavaScript: `../shared/browser-core.js`, `reading-contents.js`, `liturgy.js`.
- Data: default `../browse`; optional `?missals=` limits discovery.
- Default: manifest landing edition, then first available type and formulary;
  no remembered preference.
- URL/history: writes five legacy keys; hash change selects a valid requested
  value and otherwise keeps/falls back to current state.
- Document title: source title `The Propers of the Mass`; the controller does
  not update it per formulary.

### Accepted Propers candidate

- HTML: `src/web/browser/liturgy/propers-reader.html`.
- CSS: core, `liturgy.css`, `reader-shell.css`, `propers-reader.css`,
  `reader-instrument.css`.
- JavaScript: core, seating, state, adapters, shell, `propers-reader.js`.
- Default: URL, then remembered missal/Bible/orations, then repository defaults;
  an absent type/mass opens canonical Browse and selects no formulary by order.
- URL/history: strict fail-closed explicit state, `pushState`, coalesced
  `popstate`/`hashchange`; Browse writes the five legacy public keys.
- Candidate option keys `_candidate-cycle`, `_candidate-alternative`, and
  `_candidate-translation-witness` are implemented but are not an approved
  public URL spelling in `guidance/liturgy-reader-state.md`.
- Source/runtime title and diagnostics retain “internal candidate” wording.

## Shared state, shell, adapter, and renderer owners

| Concern | Owner retained through cutover |
| --- | --- |
| data-root and Proper rendering primitives | `src/web/browser/shared/browser-core.js` |
| Day calendar derivation | `assembly-model.js` and generated rubrics/calendar data |
| semantic state and legacy parser | `reader-state.js` |
| Day/Propers semantic adapters | `reader-state-adapters.js` |
| Ordinary rendering export | `day.js` |
| one Ordinary seating path | `ordinary-seating.js` |
| modal/focus/location shell | `reader-shell.js` |
| accepted presentation | `reader-instrument.css` loaded last |
| Day orchestration/race ownership | `day-reader.js` |
| Propers orchestration/Browse ownership | `propers-reader.js` |

## Publication, robots, and static hosting

`tools/public-alpha` renders every top-level `src/web/browser/liturgy/*.html`
through `release/public-alpha/layout.html` and copies every top-level CSS/JS
asset. Relative paths remain valid after an in-place canonical HTML promotion.
Every changed served source requires an exact binding update in
`release/public-alpha.json` and its rights-record digest.

Public HTML without a source robots declaration receives `index, follow`, an
absolute Open Graph URL, and social metadata. The accepted candidate source
pages currently omit robots metadata; therefore their deployed raw HTML is
`index, follow`, even though their JavaScript intended noindex. The oracle pages
correctly declare the repository noindex directive in source. The cutover must
make retained candidate routes statically noindex and leave canonical pages
indexable. No service worker, webmanifest, Cache API, sitemap, or route rewrite
exists.

GitHub Pages serves HTML, CSS, and JavaScript with `Cache-Control: max-age=600`,
ETag, and Last-Modified. Assets are not content-addressed. Both forward cutover
and rollback must tolerate a ten-minute mixed-cache window; route controllers
must be compatible with both old candidate and new canonical markup, and parity
must be checked once with cache bypass and again after expiry.

## Navigation into and out of the readers

Repository links already target canonical URLs. No href needs a route change.
The complete classification is in
`build/agent-continuity/liturgy-reader-cutover-navigation-map.md`.

Canonical Day and Propers currently contain direct cross-entrance and context
footer links. The accepted Instrument hides the generated site header/footer
and contains only its Triptych Home masthead link. An in-place promotion thus
removes direct cross-entrance/context links unless the cutover explicitly
preserves them. This is a navigation disposition, not a CSS cleanup.

## Material compatibility findings

1. Valid explicit core deep links map to the accepted readers with the same
   relative data paths and semantic identities.
2. Explicit invalid state changes from legacy fallback to accepted fail-closed
   behavior; this is an accepted intentional difference, not a reason to weaken
   the accepted contract.
3. Empty Day changes its current edition default from postconciliar to the
   accepted reader’s Roman 1962 repository default; independent cutover review
   must expressly accept or reject that reader-visible change.
4. Empty Propers changes from arbitrary first formulary to the accepted Browse
   entrance; this is an accepted intentional difference required by the vision.
5. `why=1`, territorial fallback, provisional Propers option keys, and direct
   cross-entrance navigation require explicit decisions before execution.
6. Retained candidates require source-level noindex; canonical routes require
   public title/description/indexing and must not inherit candidate wording.
