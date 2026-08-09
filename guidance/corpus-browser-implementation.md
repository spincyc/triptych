# Corpus browser implementation

## 1. Status and scope

This is the binding technical architecture and risk record for Triptych's
non-PDF corpus browser. Its measurements were taken from base commit
`c27d6915319785686d1df6a1401a489aa9921f6f`; the implementation reconnaissance
was reviewed at immutable head
`af2c9613ccda48679face4e43f59c002f93056ef`. Refresh a measurement when the
release contents or relevant implementation change, but do not discard the
architectural findings merely because their base SHA is historical.

The coordinator accepted the B0/B1 reconnaissance and neutral static/browser
gates as implementation input, subject to D1--D20 in
`guidance/corpus-browser-master-plan.md`. A3 is foundation direction, not
pixel-level acceptance of a production route. B0's technical seams and B1's
design-neutral gates are guidance for a later implementation branch. **This
guidance import changes no production HTML, CSS, JavaScript, generator, data,
or release binding and authorizes no production mutation on the Wave 1 design
branch.** Isolated `noindex` prototypes and their tests remain non-production
evidence under the boundary below.

This document owns the technical account of the three page pipelines, the
single layout template, the shared stylesheet and script, the seven browser
instruments, the generated data layer they read, and the gates that admit or
refuse a change to any of them. It does not independently authorize a proposed
refactor or production edit.

It does not own the visual or product contract. The corpus-browser vision,
roadmap, master plan, and the owning surface guidance decide typography,
navigation, composition, Search, and contextual navigation. Reader, Catalogue,
and Instrument are accepted archetypes with shared roles and behavior, not a
universal layout. Exact type sizes, spacing, masthead density, visible-link
count, and route composition remain subject to real-data visual acceptance.

It does not own liturgical semantics. `guidance/liturgy-browser-vision.md`
continues to govern browser-visible liturgical reading, navigation, study,
comparison, responsive behaviour, accessibility, performance, printing, and
sharing on the Day and Propers entrances, and its product invariants bind any
site-wide design that approaches them. `guidance/liturgy-browser-roadmap.md`
remains the liturgy execution record and may not weaken a vision invariant.
`guidance/liturgy-reader-state.md` owns the frozen v1 reader-state contract and
the permanent legacy-URL inventory. `guidance/web-data.md` owns everything the
browser fetches from `src/web/data/`. `guidance/web-editions.md` controls the
long-form publication Reader and forbids a second editable prose copy.

### Protected Liturgy boundary

The Live Reader -- Ritual Flow & Orientation deliverable remains independently
in progress. For this integration and Wave 1 corpus work, **every production
file under `src/web/browser/liturgy/` is read-only**, together with its release
bindings, reader-state fixtures, and owning tests. The non-negotiable protected
set includes `reader-shell.js`, `reader-instrument.css`, canonical `day.html`
and `index.html`, their controllers, and their print and state behavior. Do not
promote or move `reader-shell.js`; reuse its ideas only. Do not add a fifth
reader action, a second modal owner, a literal corpus masthead, corpus Search,
or new persistent chrome to Day or Propers. If the owning liturgy work closes,
re-read the resulting mainline state and obtain the liturgy-specific authority
and visual acceptance required by D2 and D18 before touching a former seam.

Durable corpus-browser facts belong in the tracked master plan, vision,
roadmap, this document, owning surface guidance, `PROJECT-WORK.md`, and the
promise ledger. Ignored handoffs and screenshots may support review but may not
be the sole owner of a decision.

## 2. The three pipelines and the one wrapper

There is exactly one site generator: `tools/public-alpha`, a single executable
Python file of 3,553 lines with four verbs (`check`, `prepare`, `build`,
`verify`). Every Makefile site target is a thin wrapper around one of them, and
`tools/tpt public-alpha X` resolves to `tools/public-alpha X`.

Every HTML page the deployed site serves is produced by `wrap_in_layout()` at
`tools/public-alpha:2414`, which substitutes `{{…}}` markers into the single
template `release/public-alpha/layout.html` (40 lines). Its docstring states the
intent plainly: every page a reader can reach comes through here, whichever way
its content was produced, so the header, navigation, footer, stylesheet and
robots metadata cannot differ between one page and the next. `wrap_in_layout`
asserts that no `{{UPPER}}` marker survives substitution, so adding a marker to
the template without adding its replacement key is a hard build failure. The
reverse — a replacement key with no marker — is silently ignored.

Three producers feed it.

**Markdown to HTML.** Twenty-five fixed pages from `PAGE_MAP`
(`tools/public-alpha:168`) — `README.md`, `ABOUT.md`, `CONTRIBUTING.md`,
`LICENSE`, `THIRD_PARTY.md`, three `docs/*.md`, sixteen `library/*.md`, and
`release/public-alpha/404.md` — plus 105 web editions from tracked
`web/<provider>/<leaf>.md`. The Markdown pipeline is `render_page`
(`:2381`): Python-Markdown with six extensions (`tables`, `sane_lists`, `toc`,
`footnotes`, `attr_list`, `fenced_code`) and no third-party extension. The
`Markdown==3.10.3` pin is enforced at render time by
`require_locked_markdown_dependency()` (`:843`), which parses
`requirements-public-alpha.txt`, insists on exactly one exact pin, and raises if
the installed version differs. A version bump fails the build, not just the lock
diff.

**Standalone HTML to HTML.** The thirteen browser pages under
`src/web/browser/<entrance>/*.html` are authored as whole `<!doctype html>`
documents so a developer can open them off disk, and are then dismantled and
re-wrapped at build time by `browser_page_parts()` (`:2526`) and
`render_browser_page()` (`:2625`). The page's stylesheet links become
`{{HEAD_EXTRA}}`, injected after `site.css`; its `<script src>` tags become
`{{BODY_EXTRA}}`, injected after the layout's footer; its own `.skip-link` is
stripped, because the layout supplies one; and `section-<colour>` plus the
page's body class are appended to `<main>`'s class list. Copying these pages
instead of rendering them is a recorded failure — `tools/public-alpha:616-624`
records that it "left the reading pages without the site's header, navigation,
footer and stylesheet," so a reader who followed a link from the library
arrived somewhere that did not look like the same site.

**Structured data to HTML.** One page, `library/sanctuary-picture-dictionary.html`,
composed in Python from TOML records by `render_pictorial_gallery` (`:2672`).

Everything else in the artifact is `shutil.copyfile`: PDFs, licence texts,
`site.css`, the two PNGs, the gallery images, the whole of `src/web/data/`, and
the browser CSS and JS.

**No hand-authored HTML reaches the artifact unmodified.** There is no exception.
`verify_output` (`:3029`) compares the built file set against
`expected_artifact_files()` (`:1701`) and fails on any missing *or extra* path,
and re-renders every generated page during verification to compare it byte for
byte with what was built.

### Route ownership

| URL path | Kind | Source | Entry point |
| --- | --- | --- | --- |
| `/index.html` | Markdown | `README.md` | `PAGE_MAP:168` → `render_source_page:2648` |
| `/about.html`, `/contributing.html`, `/license.html`, `/third-party.html`, `/404.html` | Markdown | repository root, `release/public-alpha/404.md` | same |
| `/docs/{bibles,the-mass,reading-and-commentary}.html` | Markdown | `docs/*.md` | same |
| `/library/<16 shelves>.html` | Markdown | `library/*.md` | `render_source_page` → `filter_catalog:1821` → `rewrite_links:1973` → `remove_private_catalog_columns:2006` |
| `/library/sanctuary-picture-dictionary.html` | Generated | artwork manifest TOML | `render_pictorial_gallery:2672` |
| `/web/<provider>/<leaf>.html` ×105 | Markdown | tracked `web/**/*.md` | `document_pages:294` → `render_source_page` |
| `/liturgy/{index,day,day-reader,propers-reader,reader-visual-reset-day,reader-visual-reset-propers}.html` | Standalone HTML | `src/web/browser/liturgy/` | `web_browser_pages:616` → `render_browser_page:2625` |
| `/scripture/{index,track}.html` | Standalone HTML | `src/web/browser/scripture/` | same |
| `/catena/index.html`, `/history/index.html`, `/texts/index.html`, `/sources/index.html`, `/law/index.html` | Standalone HTML | `src/web/browser/<entrance>/` | same |
| `/shared/browser-core.{css,js}`, `/<entrance>/*.{css,js}` | Copy | `src/web/browser/` | `web_data_files:663` |
| `/browse/**` (19,956 files) | Copy | `src/web/data/**` + `src/sources/bibles/<id>/chapters/**` | `assemble_web_data:3356` |
| `/pdf/**` (192), `/assets/**` (103), `/LICENSES/*.txt` | Copy | repository | `build_site:3371` |
| `/PUBLICATION-MANIFEST.json`, `/robots.txt`, `/SHA256SUMS`, `/.nojekyll` | Generated | — | `build_site` |

`WEB_BROWSER_ENTRANCES` (`tools/public-alpha:152`) is a fixed tuple of seven —
`liturgy`, `scripture`, `catena`, `history`, `texts`, `sources`, `law`. There
are nine directories under `src/web/browser/`; `shared/` holds the shared
stylesheet and script and has no page, and `fixture/` is an unpublished JSON
sample corpus reachable only through `?data=fixture`. A new top-level surface
directory requires a tool change, and `BROWSER_SECTION_COLOURS` (`:2590`) has
an import-time guard (`:2616`) that aborts the tool if an entrance lacks a
colour, so a new entrance is a two-place change by construction.

The measured artifact at this commit is 20,441 files: `browse/` 19,956, `pdf/`
192, `web/` 105, `assets/` 103, and roughly 144 HTML pages. A build of
`make public-site` in the measured clean checkout exited 0 in 5.1 s and produced 441 MB and 144
HTML pages (39 non-web-edition routes plus 105 web editions).

`wrap_in_layout()` is already the single shell application point. A shared
corpus shell is an extension of an existing seam, not a new architecture. What
the seam currently carries is thin: the layout's primary navigation offers three
links — Home, About, Feedback — and names no section and no instrument.

### Binding delivery and prototype contexts

There are two contexts, and evidence must name which one it exercises.

1. **Production and B1 verification use the generated artifact.** Run
   `make public-preview` before a preview-dependent browser harness and serve
   `build/public-alpha/preview/`, including its generated `/browse/**` tree.
   The Day, Propers, and visual-reset harnesses otherwise receive 404 responses
   from their hard-coded preview data root and time out while waiting for a
   readiness state that cannot occur. Repository-source HTML is useful for
   authoring checks but is not the deployed artifact and cannot prove wrapper,
   landmark, skip-link, relative-link, or generated-data behavior. Before any
   later integration or push, build and run `public-alpha verify
   --deployment-target github-pages` against the artifact.
2. **Wave 1 design evidence may use an isolated injected overlay.** Build and
   serve the real preview, load the real route and real generated data, and
   inject one namespaced prototype stylesheet/script layer from the review
   harness or an isolated `noindex` prototype. The overlay must not rewrite or
   copy production prose, invent replacement records, patch the built artifact,
   edit a production browser asset, or become a second data model. It preserves
   public paths, hash/query state, canonical PDF links, rights and absence
   states, and actual awkward corpus values. Synthetic fixtures may test a
   bounded interaction but are not visual acceptance evidence. The injected
   layer is disposable evidence, not the B0 shell and not proof of no-JavaScript
   behavior.

The eventual production B0 shell belongs at the existing generator/layout seam,
with route-specific policy and no literal shell injection into protected
Liturgy. All public navigation and asset links must remain relative from the
root, `docs/`, `library/`, and deep `web/<provider>/...` routes because GitHub
Pages serves the project under `/triptych/`; a leading `/` is invalid. The site
remains static and serverless. With JavaScript unavailable, every route must
still identify itself, preserve its core static truth and legal/source context,
offer canonical PDF access where applicable, and make direct URLs useful.

## 3. What is actually shared today

Four files.

**`release/public-alpha/layout.html`** (40 lines) — skip link, `site-header`
with the Triptych mark and brand, the three-link primary nav, a
`{{BREADCRUMB}}` slot, `<main id="main-content" class="{{PAGE_CLASS}}">`, and a
`site-footer` carrying the non-official disclaimer, Licensing and Third-party
links, and the GitHub-feedback privacy note.

**`release/public-alpha/assets/site.css`** (562 lines) — the one site-wide
stylesheet, loaded on every page. It owns the section colour identity:
`.section-toned` plus eight `.section-<colour>` classes at `:141-226`, which is
where the six `--section-*` custom properties actually get their values.

**`src/web/browser/shared/browser-core.css`** (860 lines) — the reading area,
loaded first on every browser page. It defines nineteen distinct custom
properties, of which the six `--section-*` are deliberately neutral fallbacks
meant to be overridden by `site.css`. Its 55-line header comment is a candid
design note recording why: an earlier `catena.css` shipped a violet
(`#7d5cb8`/`#5b4088`) that was not the site's `.section-violet`
(`#5a3f96`/`#3e2b6b`), and quoted a contrast ratio measured on the wrong one.
Twelve labelled component sections cover the skip link, page header, banner,
controls, reading area, citations, the record panel, detail lists, change
cards, basis blocks, folds, and the footer.

**`src/web/browser/shared/browser-core.js`** (1,482 lines) — a classic script,
an IIFE assigned to `window.Triptych`. There is no build step, no bundler, no ES
module anywhere in the tree, and no `<script>` tag carries `type="module"`,
`defer`, or `async`. Load order is source order, and load order is the module
system. There is no `init()`: loading the file reads `location.search` once,
resolves the data root once (default `../browse`, `?data=fixture` →
`../fixture`), and creates the chapter cache.

Adoption of the shared pair is total. All fourteen HTML pages under
`src/web/browser/` — thirteen published plus the unpublished prototype — load
`browser-core.css` first and `browser-core.js` first.

Adoption of the API is lopsided. `window.Triptych` exports **51 members**. (Two
recon lanes reported 45 and 44 respectively; counting the returned object
literal at `browser-core.js:1415-1481` at this SHA gives 51, and that is the
figure to use.) A count of `T.*` references across `src/web/browser/**/*.js`
gives 1,153 call sites — the recon lane's figure was 1,109, and the difference
is a regex boundary, not a disagreement about the code. Both counts agree that
**`T.el` alone is 752 of them**: two-thirds of every use of the shared library
is one `createElement` wrapper. Below that, `T.clear` 64, `T.fillSelect` 42,
`T.loadJSON` 27, `T.fail` 22, `T.titleCase` 21, `T.statusLine` 19. Everything
rarer is essentially liturgy-and-scripture only.

Three consequences follow. The bible, loci and propers half of
`browser-core.js` — roughly 60% of 58 KB, including about 4 KB of inline
fallback chapters — is downloaded and parsed by sources, law, history and texts
for nothing. The render-token discipline (`beginRender`/`isCurrentRender`) is
used by liturgy, scripture, catena and sources, and not by law or history, which
guard concurrency with a promise cache that memoises but does not discard an
overtaken render. And the shared library is a bag of helpers rather than a
shell: nothing in `browser-core.js` builds a header, a footer, a nav, or a
breadcrumb, and a grep for `page-footer|site-header|breadcrumb|nav` over it
returns nothing.

**`src/web/browser/liturgy/reader-shell.js`** (296 lines) demonstrates the
strongest reusable interaction ideas, but D2 and D18 prohibit promoting,
moving, or editing it during the current corpus wave. Its own first line says:
"Reusable persistent reader shell. It owns interaction, never liturgy." It is a
factory discovering its own DOM by data attributes — `[data-reader-shell]`,
`[data-reader-action]`, `[data-reader-surface]`, `[data-reader-close]`,
`[data-reader-contents]`, `[data-reader-locus-major]`, `[data-semantic-location]`
— and returning a frozen eight-method API. It owns one modal at a time
(`:207`), native `<dialog>.showModal()` with the browser's own focus trap
(`:216`), `cancel` interception so Escape always runs the restore path
(`:278-281`), focus return to the invoker with `preventScroll` (`:200-202`),
scroll and semantic-location preservation across open and close (`:191-198`),
rAF-throttled current-section tracking against a viewport line at
`clamp(80, innerHeight*0.38, 280)`, `aria-current="location"` on the contents
entry, and a running locus that hides itself when the real heading is already
visible. It has two callers, `day-reader.js:9` and `propers-reader.js:8`.

Its liturgical coupling is exactly three points in 296 lines:

- `reader-shell.js:63-67` — the major-unit and heading selectors are hardcoded
  as `.ordinary-division` and
  `:scope > .proper-name, :scope > .ordinary-head, :scope > h2, :scope > h3`.
- `reader-shell.js:89` — `majorHeadingVisible` tests
  `active.element.matches('.ordinary-division')`.
- `reader-shell.js:243` — the contents group defaults to the string
  `'Proper of the Mass'`.

The reconnaissance found that hoisting `majorSelector`, `headingSelector` and
`defaultGroup` into `options` could make the file corpus-neutral. That remains
a finding, not an authorized change. Two existing tests document its intended
neutrality:
`test_shared_shell_remains_one_entrance_neutral_implementation`
(`tools/tests/test_propers_reader_integration.py:95`) and
`test_day_and_propers_use_the_exact_same_shell_files` (`:84`).

Its companion `reader-shell.css` (207 lines) provides useful precedent rather
than a corpus-shell implementation: it has no colour identity, consuming `--panel`,
`--section-line` and `--focus` from browser-core, and it is the only definer of
`--reader-safe-{top,right,bottom,left}`, which four other files consume. Three
things in it are worth expressing independently in a non-liturgy shell: the
`--reader-shell-height` plus safe-area
token set with its matching `scroll-padding-block`/`padding-bottom` pair
(`:11`, `:16`), which is why an anchor never lands under the fixed bar; the
universal shrink rule `.reader-surface, .reader-surface * { min-width: 0;
overflow-wrap: anywhere; }` (`:76`), which is the single line making "every
surface reports `scrollWidth <= clientWidth`" hold; and the three-tier
breakpoint ladder — 72rem side rails, 52rem bottom sheets, 25rem single column.

One further reason not to lift the shell mechanically is that the desktop rails at
`reader-shell.css:176-189` are visually pinned but still `showModal()` dialogs,
so the page behind them is not focusable, selectable or scrollable — which
contradicts the accepted disposition in
`guidance/liturgy-reader-shell-prototype.md` that a wide-desktop Study rail is
a *pinned nonmodal*. Retrofitting a non-modal mode means splitting `open()` into
modal and inline paths. B0 must instead implement a non-liturgy corpus shell at
the generator seam and reuse only independently expressed ideas. The protected
Liturgy files cannot move while their owning deliverable is in progress.

## 4. Where the drift is

**Token shadowing.** Nineteen custom properties are defined in the shared
stylesheet. Fifty-four custom-property declarations exist across the seven
instrument directories, thirty-seven of them in shipped files. **Twenty-eight
shipped tokens actively shadow a shared concept under a different name**: the
fourteen `--instrument-*` tokens in `reader-instrument.css:7-20` and the
fourteen `--vr-*` tokens in `reader-visual-reset.css:7-20`. Both sets restate
ink, soft, faint, paper, panel, line, accent, accent-soft, focus, serif, sans
and mono as hard-coded hexes with no relation to `--section-accent` or to
`site.css`. `--instrument-focus: #1f5d8b` is a blue focus ring on a red liturgy
page.

Both sets also redeclare `--reader-shell-height` at `:root` as `4.25rem`,
later in the cascade than `reader-shell.css:3`'s `3.65rem`, so the 3.65rem is
dead on every production reader page. The `instrument` block of the study
(`reader-visual-reset.css:463-470`) is byte-for-byte the production palette
(`reader-instrument.css:10-17`): `#f4f1ea`, `#faf8f2`, `#1d211f`, `#555e59`,
`#747d77`, `#cfd3ce`, `#8f292b`, `#efe3e1`. That is how `reader-instrument.css`
came to exist — the accepted direction was copied out of the study rather than
extracted from it.

Beyond tokens: three competing font-stack triples, of which the instrument and
vr triples are identical to each other and neither matches core; four reading
measures (`--measure: 65ch`, `--missal-measure: 40.5rem`, the prototype's
`--reader-measure: 68ch`, and a hard-coded `52rem` in two files); two focus
colours; and nine distinct max-width breakpoints across a seven-page product
(22, 25, 30, 32, 34, 40, 47.5, 52, 71.999 rem), three of which — 32, 34 and 40 —
are within 6rem of each other and do the same job. `site.css` breaks at 760px
and 900px while every browser file breaks in rem, so a shell reflowing at 52rem
inside a site reflowing at 47.5rem produces a two-step reflow.

**Seven hand-written, mutually inconsistent footer nav lists.** Every
page-header instrument closes with a hand-maintained paragraph of links to its
siblings, and no two are alike in membership, order or phrasing:

| Page | Links | Count |
| --- | --- | --- |
| `catena/index.html:112-117` | Story of Salvation, Propers, Missal Changed, Code, Source Library, Every Document | 6 |
| `history/index.html:80-84` | Today's Missal, Propers, Code, Source Library, Every Document | 5 |
| `law/index.html:142-146` | Missal Changed, Source Library, Propers, Catena Omnia, Every Document | 5 |
| `scripture/index.html:57-65` | Propers, Missal Changed, Every Document, Source Library, Code (as running prose) | 5 |
| `scripture/track.html:81-83` | the plan, Propers, Every Document | 3 |
| `sources/index.html:124-130` | Today's Missal, Propers, Story of Salvation, Catena, Missal Changed, Code, Every Document | 7 |
| `texts/index.html:102-108` | Today's Missal, Propers, Story of Salvation, Catena, Missal Changed, Code, Source Library | 7 |

Fifteen of forty-nine possible instrument-to-instrument edges are missing.
"Today's Missal" — the landing page's headline destination — appears in three of
seven. `texts/index.html:108` has a trailing space after the last link and no
separator, which is the cosmetic evidence that these are kept by hand. The six
liturgy pages have no footer at all.

**Three incompatible `link()` signatures.** `plan.js:53-57` takes
`(text, href, className)`; `texts.js:82-86` takes `(className, href, text)`;
`track.js:133-137` takes `(text, over, className)`. Five lines each, arguments in
three different orders.

**A duplicated `languageName` that has already diverged.** `catena.js:60-75`
carries its own `LANGUAGE_NAMES` map beside the exported one at
`browser-core.js:1026-1038`. Catena's adds `grc, el, he, syr, it, es` and falls
back to the raw code; the shared one adds `pl` and falls back to
`String(code).toUpperCase()`. `T.languageName('grc')` returns `"GRC"` and
catena's returns `"Greek"`. Sixteen lines, live drift, and the shared one is
exported — this is not a scoping necessity.

**Three hand-rolled hash routers.** Catena (`catena.js:893-904`, `:997-1010`,
`:1026-1032`), scripture track (`track.js:107-131`, `:658-663`, `:832-866`) and
texts (`texts.js:67-76`, `:334-341`, `:380-388`) each re-implement declare-keys /
read-into-controls / write-back over one `T.readHash`/`T.writeHash` pair. Two
concrete defects follow. `texts.js:410` binds `render` to the find box's `input`
event and `render` ends in `T.writeHash`, which assigns `window.location.hash`;
typing `augustine` pushes nine history entries. `track.js` writes a hash on every
`commit()`, so walking the 357-reading full-account track leaves 357 Back
presses behind. `sources.js:684-688` does the same per keystroke. No page uses
`pushState`/`replaceState` outside liturgy.

**Function clones.** Fourteen cross-file JS function pairs are ≥70% line-similar.
The duplication is tightly localised to two pairs. Between `history.js` and
`law.js`: `fragment` (132 bytes, byte-identical), `citations` (505 bytes,
identical but for the parameter name), `lazyBlock` (819 bytes, identical but for
one intermediate `const`), `facts` (1,065 bytes, three lines apart),
`lineLabel`, `whatHappened`, `renderState` (2,430 bytes), and three constant
tables. Between `day-reader.js` and `propers-reader.js`: `detailsLinkSection`
(14 lines, identical), `definitionList`, `replaceReading`,
`refreshDetailsAfterOutcome`, `load`, `semanticProjection` — about 65 lines
verbatim or near-verbatim between the two files the reader shell was extracted
for. Five separate memoised-JSON-fetch implementations exist
(`history.js:271`, `law.js:96`, `day-reader.js:108`, `propers-reader.js:86`,
`day.js:261`) and `catena.js` open-codes a sixth.

The `history.js`/`law.js` divergence has already produced a live bug.
`history.js:443-447` copies `CITATION_WORDS` from `law.js:218-223` and omits the
`'none-claimed'` key. In `latin-missal.json`, the default slice, `act_citation`
is `none-claimed` on 26 of 59 stations, so **44% of the default history view
renders `Instrument read: none-claimed — ` with a dangling em dash and no
gloss**. The page that needs the sentence most is the one missing it. A second,
quieter divergence: `history.js:321-326` keeps a private `magnitude` that
hardcodes `masses_touched` and omits `interpretations`, disagreeing with
`code-model.js:353-360` about how big an act was.

**Orphan JS.** `web_data_files()` (`tools/public-alpha:662-690`) copies every
`.js` in each entrance directory whether or not any HTML loads it. Three files
ship and are never loaded: `liturgy/liturgy.js` (29.5 KB, the entire pre-cutover
Propers page), `liturgy/reading-contents.js` (3.8 KB), and
`liturgy/proper-placement-notes.js` (2.7 KB) — about 36 KB of dead weight.
`day.js` (85 KB) *is* loaded on `day.html` for roughly 1.4 KB of exported
renderer surface: it self-gates at `:1720-1721` (`if (!reading || !controls)
return;`) so that ~60 KB of legacy page controller stays unreachable while
`TriptychOrdinaryRenderer` (`:1413`) reaches `day-reader.js:10`. Twenty-four of
the twenty-seven element ids `day.js` looks up do not exist in `day.html`.
Adding those ids, or "fixing" the missing ones, un-gates 1,400 lines of page
logic on a page that does not want it.

**Near-duplicate HTML.** `day.html` and `day-reader.html` share 179 of 181
lines; `liturgy/index.html` and `propers-reader.html` share 166 of 168. In both
cases the difference is two lines — a description plus `<title>Day</title>`
against a robots directive plus `<title>Day — Triptych</title>`. Both copies
publish, and because `document_title()` (`:2155`) appends `· Triptych`, the two
retained copies publish as `Day — Triptych · Triptych` and
`Propers — Triptych · Triptych`. The reader masthead block is duplicated across
six files, the four-button action nav with its inline SVGs across four full and
two partial copies, and the `page-footer` construct across seven. The skip-link
line appears in thirteen files with nine distinct target ids and phrasings, and
every one of them is stripped at publish.

## 5. The unscoped-selector and chrome-suppression hazards

Four selectors decide the behaviour of pages that never mention them. Each is a
place where a stylesheet reorganisation would produce a change nobody asked for.

**`day-missal.css` restyles the site header, unscoped.** Six rules beginning at
`src/web/browser/liturgy/day-missal.css:51` re-lay-out `body > .site-header` —
grid columns, gap, min-height, padding, the triptych mark's geometry, brand font
sizes, nav gap — with no page-scoping selector at all, plus further unscoped
blocks in the 47.5rem media query at `:604` and the print block at `:730`. The
file is loaded by four published pages. Pulled into a shared bundle, it silently
restyles the header of every page on the site. This is the most dangerous file
in the tree.

**`reader-instrument.css:40-45` deletes the site chrome.**

```css
body:has(.reader-instrument) > .site-header,
body:has(.reader-instrument) > .release-banner,
body:has(.reader-instrument) > .site-footer,
.page-shell:has(.reader-instrument) > .breadcrumb { display: none; }
```

`reader-visual-reset.css:40-45` does the same for its own class. The consequence
is concrete and currently live: **`liturgy/day.html` and `liturgy/index.html`
publish with no site navigation, no breadcrumb, no footer, no Licensing link and
no Feedback link.** The only outbound link on either page is the masthead word
"Triptych" pointing at `../index.html`. The flagship route — the one the landing
page bolds as "Today's Missal" — is also the only route with no legal notice and
no feedback path. Whether the corpus reader keeps site chrome (and liturgy
regresses) or hides it (and six other instruments change) is the central product
question of the redesign, and it is not a CSS question.

That masthead link is also broken in the repository. There is no
`src/web/browser/index.html`, so opening `day.html` off disk — which
`browser_page_parts` explicitly documents the pages as authored to support, and
which the `body:not(:has(> .site-header))` guard at `browser-core.css:134`
exists to serve — gives a 404 on the only link the page has.

**`history.css`'s `.field` collides with the shared control bar and works by
load order.** `browser-core.css:287` styles `.field` as a control in the bar
above a reading page: a label over a select, sized for a thumb.
`src/web/browser/history/history.css:240` styles `.field` as a line of one
change — a name, an old value, an arrow, a new value — on a page that has no
control bar at all. The stylesheet's own comment at `:226-239` says it out loud:
the two "have nothing in common but the word," this file re-declares `display`
and `gap` over the shared rule, the leftovers are inert, "it renders correctly
by luck rather than by construction, and the fix is a rename — `.change-field` —
which is a change to `history.js` and so is not made here." **Any shared-shell
work that reorders stylesheet loading, or adds a `.field` rule after
`history.css`, silently breaks every change row on the page.**

Two related name collisions sit beside it. `texts.css:191-199` deliberately
restates every declaration of `browser-core.css:556-564` so that the shared
`.detail` — the history and law record panel — cannot reach the texts page,
where `.detail` is a different component. Both files document it as a name
collision and both say the fix is a rename in `texts.js`. Introducing a shared
component library without doing that rename first will re-collide. And eight
class-name pairs still name one component twice: law's `.panel`/`.panel-title`/
`.panel-block`/`.block-title`/`.stop`/`.stop-head`/`.stop-kinds`/`.weak` against
history's `.detail`/`.detail-title`/`.detail-section`/`.detail-section-title`/
`.change`/`.change-head`/`.change-kinds`/`.detail-weak`. The de-duplication was
done at the selector-list level, and `browser-core.css:543-548` says the rename
is the right next step and belongs in a commit that moves the HTML and the
JavaScript with it.

**`browser-core.js` `fail()` hard-codes `#reading`.**

```js
function fail(text) {
  const reading = document.getElementById('reading');
  if (!reading) return;
  …
}
```

`browser-core.js:294-301`. Only catena, scripture (both pages), sources and
texts use `id="reading"`. History's main is `#map`, law's is `#canon`, and all
six liturgy pages use `#reader-document`. `T.fail` is therefore a silent no-op
on law and history today — neither calls it — and any shared error or
empty-state primitive that routes errors through it would make those pages fail
silently. `showBanner` (`:261`) has the same hard-coded `#banner` problem.
Fixing this is a prerequisite for a shared error component, and the five
different `<main>` ids are the reason it was never fixed.

`T.fail` has a second defect where it *is* used. `sources.js:229` calls it when
an edition has no recorded file; `fail` clears `#reading`, which contains both
`#finder` and `#reader`, so `elements.finder` and `elements.reader` (`:53-54`)
then point at detached nodes and every subsequent render writes into nothing.
The page does not recover without a reload.

Two further hazards belong here because they are structural rather than
cosmetic. The published pages nest `<main>` inside `<main>`: `layout.html:29`
wraps `{{CONTENT}}` in `<main id="main-content">` and every browser page
contributes its own `<main>`. Two `main` landmarks, invalid HTML, and — because
`tools/public-alpha:2559` strips the page's skip link — the surviving skip
target is the outer wrapper rather than the reading document. Every browser page
is affected. No harness catches it, because every Chromium harness loads the
repository or preview page and the preview-build assertions test robots and
links, not landmark nesting. And `history.js:341-348` sets `role="img"` on the
map's `<svg>`, which prunes all descendants from the accessibility tree — the 59
station groups at `:372-379` carry `role="button"`, `tabindex="0"` and full
`aria-label`s, and none of it is exposed. A screen-reader user tabs through 59
unlabelled focus stops.

## 6. Payload and performance baseline

Method: a Python walk of `src/web/data/` recorded `len(bytes)` per file and
`len(gzip.compress(raw, level=9, mtime=0))`. gzip -9 is slightly smaller than a
typical server default, so these are floors. For each route the controller's
boot path was read to identify what is fetched before the primary content region
can render, against what is fetched only on a later reader action. Bible chapter
fragments are counted at their measured median of ~1.3 KB gz because they are
part of first paint wherever verse text appears. JS and CSS are excluded from
the data budget and listed separately.

`src/web/data/` totals 10,569 files, 52,562,237 bytes, 11,929,381 bytes gzipped.
Every one of those files is tracked in git; nothing in the directory is built at
deploy time. `du -sh` reports 88 MB, which is block-allocation overhead from
5,548 tiny paragraph files.

| Route | First-load data (gzip) | Composition | Lazy |
| --- | --: | --- | --- |
| `liturgy/day.html` | ~324 KB (~358 KB with Ordinary) | `rubrics/index` 712 + `ordinary/index` 277 + `bibles.json` 552 + `rubrics/roman-1962` 23,526 + `calendar/roman-1962/<y>` 10,810 = 35.9 KB to name the day; then `propers/roman-1962` 288,329 for any text | bible chapters ~1.3 KB each |
| `liturgy/day-reader.html` | ~324 KB (~358 KB with Ordinary) | same files, but `rubrics`+`calendar`+`propers` in one `Promise.all` (`day-reader.js:377-381`) — **no early paint** | bible chapters |
| `liturgy/index.html` | ~289 KB | `propers/index` 202 + `bibles.json` 552 + `propers/roman-1962` 288,329 | bible chapters; a missal switch costs a further 240,558 or 112,583 |
| `liturgy/propers-reader.html` | ~289 KB | as above | as above |
| `sources/index.html` | ~62.8 KB | `sources/index.json` 62,811 alone | edition file median 1,366 / max 16,017; passage text median 742 / max 97,088 |
| `texts/index.html` | ~35.8 KB | `documents/corpus.json` 35,842 alone | nothing — one file, no second fetch |
| `scripture/index.html`, `track.html` | ~21.3 KB | `readings/narrative-spine` 20,786 + `bibles.json` 552 | bible chapters |
| `history/index.html` | ~13.4 KB | `act-history/index` 172 + `latin-missal.json` 13,188 | `units.json` 1,840; fragments median 388, max 4,756 |
| `law/index.html` | ~12.9 KB | `code-of-canon-law.json` 12,935 | `units.json` 9,067; fragments median 759, max 9,429 |
| `catena/index.html` | ~8.4 KB | `catena/index` 5,592 + `bibles.json` 552 + `paragraphs/index` 325 + chapter spine median 639 + bible chapter ~1,300 | fragment text median 764, max 96,789 |

Three routes are flagged.

**`liturgy/day.html` at 324 KB gz, 358 KB with the Ordinary on.** The cost is
`structure/propers/roman-1962.json`, 3,960,669 bytes raw. `day.js` fetches it
last, deliberately, so 36 KB gets a named celebration on screen and the megabyte
lands behind it. `guidance/web-data.md:122-123` already names the propers
structure as the next split candidate.

**`liturgy/day-reader.html` at the same size and worse in shape.**
`day-reader.js:377-381` puts rubrics, calendar and propers into one
`Promise.all`, so the deferral `day.js` implements is absent and the reader
waits on all 324 KB before anything renders. That looks like a regression
against `day.js`'s documented ordering.

**`liturgy/index.html` and `liturgy/propers-reader.html` at ~289 KB**, just
under the 300 KB line and only because the 1962 propers compress 13.7:1. Any
growth pushes both over.

Uncompressed first-load for the four liturgy routes is 4.1–4.3 MB, which matters
on any deployment serving these files without content-encoding. Note also that a
per-mass split would lose most of the compression ratio: the propers files
compress so well precisely because they are `indent=1` pretty-printed and
structurally repetitive, and `structure/paragraphs/` demonstrates the opposite
end — 5,548 files of ~142 bytes each compress 1.23:1 in aggregate because each
pays a gzip header and gets no cross-file dictionary. **Any per-mass split must
be measured, not assumed.**

The catena is the model the guidance already argues from.
`guidance/web-data.md:86-124` records the measurement: a 605,923-byte book file
became a chapter-addressed spine plus content-addressed payload, so Genesis 40
now costs 2,745 bytes — 0.45% of what it was. The rule that produced it is that
a file is cut at the natural unit of the thing inside it, never at the shape of
one view of it, and everything is collapsed by default. The trade is stated on
the page rather than hidden: text not fetched is not in the document, so
find-in-page cannot reach it, which is why each fragment's length is printed
beside its name. Catena's measured first load is 8.4 KB gz, the smallest of the
nine routes.

No stated numeric ceiling exists for `src/web/data/`. The budget discipline is
measured and argued, not quotaed. `guidance/liturgy-browser-vision.md:420-428`
sets Core Web Vitals as a release gate at the 75th percentile — LCP ≤ 2.5 s,
INP ≤ 200 ms, CLS ≤ 0.1, evaluated separately for mobile and desktop — and
requires route-specific resource and main-thread budgets from a measured
baseline: "a prototype may choose the numbers; it may not ship without them."

## 7. What the data layer can and cannot support

### Identifier schemes

Source Library identifiers have stable dotted type prefixes, but the remainder
is an opaque, variable-length repository identifier rather than a grammar a
browser may safely decompose. The following are independent identifier
examples, not hierarchy levels. Work owns Edition; Artifact, Segment, and
Passage are edition-owned sibling record types. Representative shapes include:

```
work.<author-slug>.<work-slug>
edition.<author-slug>.<work-slug>.<imprint-slug>
artifact.<opaque-stable-components>
passage.<author>.<work>.<edition>.<locus-slug>
```

A readable passage id is directly addressable as
`structure/sources/text/<passage_id>.json`; the public projection does not yet
provide an equivalent metadata-only locator for a known non-readable passage.
The readable path is what makes the one live cross-instrument link work:
`catena.js:519` writes
`../sources/#passage=<encoded id>` and `sources.js:594` reads it. That handler,
`followPassage()` (`sources.js:576-590`), fetches the passage's own text file and
reads `work_id`/`edition_id` off it rather than decomposing the id. That is the
right construction for readable text and must survive any redesign; a later
generator change needs a rights-safe locator record for non-readable passages
rather than teaching the browser to parse opaque ids.

Scripture citations exist in four coexisting forms: the display grammar
(`"Psalms 97:3-4,2"`, never parsed in the browser), the book token (`"Ps"`,
`"Matt"` — the key in the fragment path, still capitalised), the resolved loci
(`{"vulgate":[{"chapter":97,"first":3,"last":4}…],"hebrew":[…]}`), and a
path-only catena form (`structure/catena/53-cor-1/013.json` — canon position,
lowercase slug with the ordinal last, chapter padded to `chapter_digits`).

Act-history uses slug-plus-year station ids (`quoniam-nulla-1317`), dotted
liturgy unit ids (`coena.missa.introitus`), and hyphenated law unit ids
(`cceo-c-1`).

Two gaps matter. **Mass keys are unique within a calendar and not across
calendars**, so a typed key needs `(calendar, key)`. And **documents have no
opaque id at all**: a document edition is identified by its PDF path
(`pdf/claude/articles/canon-law/…pdf`), and any typed search would have to
synthesise a key — provider plus section plus path stem is the obvious one —
because none is written down.

### The source graph separates ownership from controller foreign keys

A grep across `structure/sources/index.json` and all 655 edition files returns
**zero hits** for `cites`, `quotes`, `comments_on`, `translation_of`,
`edition_of`, `artifact_of`, `passage_of`, `used_by`, `governs`, `changes`,
`supersedes`, `appointed_in`, and for the generic `relation`, `relationships`,
`edges`, `links`. There is no named-edge vocabulary in the served Source Library
data. The projection expresses ownership through Work-to-Edition nesting and
edition identifiers on the sibling records: `edition_id` on all 1,467 upstream
Artifact records and on all 2,751 Passages. It expresses Passage control through
`passage.artifact_id` on 2,613 records and `passage.segment_id` on 138.

The public projection expresses Work-to-Edition ownership and the Edition's
sibling Artifact, Segment, and Passage records. A Passage additionally names
its controlling Artifact directly or its controlling Segment. Those foreign
keys express control and source evidence, not Artifact-to-Passage or
Segment-to-Passage containment. A Segment may resolve to an Artifact truthfully
owned under another Work.

`translation_of` is the load-bearing absence. The page's own prose says "a Greek
original, Migne's Latin and a public-domain English translation are three
editions and never one work with three texts"
(`sources/index.html:100-107`) — and no edition record names a source edition.
`translators` is a list of human names, not a pointer. So the page can say who
translated an edition and cannot say what they translated from, and it renders
the Latin and the English as two peer rows with no relation between them.

### Three real upstream edges the generator drops

| Edge | Upstream | Records | In `src/web/data/`? |
| --- | --- | --: | --- |
| Artifact → Artifact `derived_from` | `src/sources/works/**/artifacts/*.toml` | 651 of 1,467 | no |
| Artifact → Artifact `projected_from` | same | 1 | no |
| Work → Work `relations` (untyped list of work ids) | `src/sources/works/**/work.toml` | 115 of 491 | no |

These are not missing from the model; they are present upstream and are not
projected. The web artifact block emits twelve keys and none of them is
`derived_from`.

### The 1,854 typed bindings that never reach the browser

`guidance/sources.md:69-72` defines a **binding** as a publication-local
declaration that an identified source or corpus was used, searched, or retained
as a lead, at stated loci and in a stated role. There are **134
`source-bindings.toml` files under `src/**/research/`, carrying 1,854 binding
entries** from 97 documents to 1,109 distinct source objects, each with a typed
`role` and its own `loci[]`, `states[]` and prose `context`:

| Role | n | | Target kind | n |
| --- | --: | --- | --- | --: |
| `direct-witness` | 492 | | `passage.*` | 661 |
| `official-control` | 463 | | `edition.*` | 212 |
| `textual-control` | 301 | | `artifact.*` | 197 |
| `reception` | 180 | | `work.*` | 30 |
| `context` | 161 | | `segment.*` | 8 |
| `translation-control` | 115 | | `corpus.*` | 1 |
| `lead` | 72 | | | |
| `bibliographic` | 32 | | | |
| `currentness-control` | 20 | | | |
| `analogue` | 18 | | | |

**None of it is in `src/web/data/`.** `tools/source-reader` never reads
bindings. So the Source Library browser cannot answer "what in this project used
this edition, and how" — the question a `used_by` edge exists to answer, and the
one that most distinguishes an evidence record from a library catalogue. The
omission is at the generator, not the page.

### What a cross-corpus relationship UI can show

Plainly: a relationship UI can only draw edges that exist. Today those are:

- **Structural ownership**: work → edition, with artifact, segment, and passage
  as edition-owned siblings; slice → station → unit; work → edition in the
  document catalogue.
- **Passage → controlling artifact**, or **passage → segment → controlling
  artifact**, as explicit foreign-key evidence. The controlling artifact may
  belong under a different work, so presentation must not infer containment
  from the selected passage's work alone.
- **Catena fragment → scripture locus**, the one typed validated edge, derived
  once in `catena-model.js` and replayed under node by `catena check`.
- **Catena passage → Source Library passage**, by shared passage id, already
  implemented as the `#passage=` handoff.
- **Act → act descent** (`station.parents[]` with `parent_kind` stating why the
  edge is drawn, and `via_unrepresented[]` recording that the descent crosses an
  edition the record does not hold), **act → unit change**
  (`station/<file>.json` `units[]` with `state ∈ {entered, changed, gone}`, the
  diff computed once by the generator), **act → container change**, **unit →
  its own history**, and **line ↔ line commonality** derived by the generator.
- **Document → catalogue page**, via `works[].catalog_page`.
- **Mass → propers → resolved scripture loci**, and **calendar date → mass key**
  by reference rather than copy.

Not available: `translation_of` between editions; `used_by` from a publication
to a source; `derived_from` between artifacts; work-level `relations`;
`corresponds_to` between canons of different Codes — that schema exists
(`row.correspondence[]`) and is **empty on all 169 index rows**, so `law.js`
always renders the "maps this canon onto no canon of any other Code" branch; and
`cites` between Law and the Source Library, which exists today only as prose:
53 occurrences of `passage.<id>` strings embedded in free-text `cited[].basis`
fields across `structure/act-history/**`, three distinct ids, **none of which
resolves to a served text file**, because the referenced passages are all
withheld.

Two data-layer defects a relationship UI will trip over. The law slice declares
`group_word: "division"` but emits its containers under the key `mass` on all
169 index rows, and the page only works because `C.groupOf`
(`code-model.js:91-97`) falls back through `row.division || row.mass` — the
generator is emitting liturgy vocabulary into a law slice and the browser is
quietly compensating. And `structure/catena/text/` and `structure/sources/text/`
hold 1,351 files with identical basenames and the same passage text in different
envelopes; **only the sources copy carries rights fields**. An index built by
walking `structure/` ingests each of those passages twice. Deduplicate on the
passage id and prefer the sources copy, which is the superset at 1,630.

For sizing: a title-and-identifier index across works, editions, readable
passages, documents, masses, catena fragments, stations, units and readings is
roughly 7,000 objects, ~500 KB raw, ~100 KB gzipped — smaller than one propers
structure file. Full text over the readable prose is a different order:
`structure/sources/text/` alone is 6.72 MB raw / 2.77 MB gz, plus 34.8 MB of
bible fragments.

## 8. Rights and absence must survive any redesign

### Where the rule lives

`tools/source-reader:222-345`, the function `reading_of()`. Its docstring is
explicit: "THE ONE PLACE THE RIGHTS RULE IS APPLIED. Every verb calls this; none
of them repeats the test. The refusals are ordered from the most general to the
most particular so that a reader is told the governing reason rather than an
incidental one."

Six withheld codes, in refusal order, with the counts present in the served data:

| Code | Condition | Count |
| --- | --- | --: |
| `uncontrolled` | no artifact controls the passage | 0 |
| `rights` | `rights_status` not distributable | 885 |
| `storage` | storage is `remote`, `restricted` or `unavailable` | 157 |
| `not-prose` | line-bounded into a non-prose media type | 61 |
| `no-payload` | tracked but the payload could not be read | 0 |
| `no-transcription` | neither transcription nor line bounds | 18 |
| — | readable | 1,630 of 2,751 |

The generator self-checks the invariant: `tools/source-reader:976-987` refuses
to emit a row that is `readable` under non-distributable rights or from
non-tracked storage, and refuses any withheld row with no stated reason.

**No separate withheld passage-text payload is sent to the browser.** A
non-readable passage carries no `text_path` and no file exists under
`structure/sources/text/`, so the page cannot fetch a standalone transcription
for that passage. That narrower guarantee is important, but the current edition
projection also carries `context` and `notes` before the readable decision; some
non-readable records therefore expose source wording in metadata. Canon 7 is a
known exact example and is excluded from the Wave 1 withholding oracle. A later
generator change needs rights-reviewed public metadata fields or omission rules,
plus tests covering every non-readable row. Any redesign that introduces a
text-fetch layer must preserve the absence of a withheld text path and must not
mistake that invariant for proof that every other projected field is safe.

### What the current UI carries that a redesign could flatten

**Law draws three states apart, deliberately.** `code-model.js:380-403` states
the contract: "Three states, never two: words present; words this record never
carried; and words that exist and may not be published here. The last two look
identical in the data — both are an empty string — and are told apart only by
whether a reason is carried." `bodyNode` (`law.js:147-167`) renders them three
ways. `.canon-withheld` prints **`Text withheld here. `** in bold plus the
reason, on `--section-wash` with a 3px accent left border; `law.css:140-152` is
emphatic that this is "deliberately NOT faint: a withholding is a statement the
reader is meant to read, not a greyed-out absence to skim past." `.canon-unread`
prints "This record carries this canon's identity and place and has not read its
words," italic and faint, and `law.css:169-177` says the two are "drawn
differently so the two can never be mistaken for each other."

Beside them sits `establishedNote` (`law.js:133-145`): where the words are
withheld, the page still names the act that established the text now in force,
as a clickable act link — "Text established by *Mitis Iudex* (2015-08-15). The
words are not here; which act put them there is." The file header (`:54-59`)
explains that this is how a lawyer cites a canon he cannot quote. It is the most
valuable piece of rights-aware UI in the corpus.

**History conflates withheld and unread.** `history.js:500-506`:

```js
function value(text, missing, withheld) {
  if (text) return T.el('span', 'value', text);
  if (withheld) return T.el('span','value value-absent','withheld here: ' + withheld);
  return T.el('span', 'value value-absent', missing);
}
```

Both non-present states render in `.value-absent` — italic, `--ink-faint`, the
same class. The only difference is the string prefix. Law draws them apart on
purpose; history draws them the same. **Unifying the two is a fix, and it should
unify toward Law** — but it is a fix that changes what history looks like, so it
needs the maintainer's assent, not a refactor's.

**The distinction is discarded at the DOM boundary.** `bodyOf` returns
`{state: PRESENT|WITHHELD|UNREAD}` and the DOM carries only a CSS class — no
`data-state`, no ARIA. Copy the text out, or render it where the stylesheet does
not load, and a rights withholding and an unread canon become the same
sentence-shaped grey. Emitting `data-state="withheld"` alongside the class costs
nothing and makes the truth survive a restyle. The same loss happens one layer
earlier: `passage.withheld`, the six-value taxonomy, is never rendered and never
filterable — the page shows only the prose `reason`, so a reader cannot ask for
everything withheld for *rights* as opposed to *storage*.

**Four further guarantees the Source Library currently carries.** Provenance is
shown for a refusal exactly as for a text (`renderProvenance`,
`sources.js:480-505`, called from both branches, with the comment "the reader
weighing a refusal needs the same facts as the reader weighing a text"). The
dropdown states readability before the reader navigates — each option reads
"— not shown here" rather than promising text it will not deliver. The finder
card states it before the reader opens the edition. And a licence travels above
the words: `passage.acknowledgement` renders as a `<strong>Licence: </strong>`
block *above* the prose, deliberately, so a copied selection carries the
condition. Twelve passages have one.

**The rest of the corpus's absence vocabulary.** History records
`via_unrepresented[]` as a dashed connector plus prose plus a legend entry —
descent crossing an edition the record does not hold, drawn broken rather than
joined. `unestablished[].marker` prints as a `<pre>` **in place of** inherited
words, because carrying them forward would assert that nothing changed.
`station_kind` distinguishes `promulgated` from `printed` — an act ordered it
versus a book merely differs — read and never inferred, with the count verb
switching from "changed" to "differ" and a caveat paragraph accompanying every
printed station's diff. Interpretation is its own card kind with no
before/after, because an interpretation is not a change. Catena renders per-work
rights absences with a separate `partial` line so that "partly public domain"
reads as an offer rather than an excuse. Texts flags an unrecorded title on the
card, in the panel, and in CSS, so a path cannot pass for a name.

The generated data layer imposes matching rules. An Ordinary element carrying
neither text nor a stated reason is a hard failure — "a silent gap is the one
thing this layer must never emit" — and the two absences (ICEL-held English
against untranscribed Latin) are kept apart; collapsing them into one "missing"
is forbidden. The language control deliberately offers a language nothing is
held in, so that choosing an empty language shows the reader, at every element
and at the place it falls due, under which recorded reason it is empty; hiding
empty languages from a selector regresses a fixed bug. The `licensed-free`
acknowledgement is emitted beside every text it covers, at the point of use and
not in a footer, "because a reader who copies a prayer out must carry the
condition with it."

That last rule is the one most at risk from a progressive-disclosure redesign.
Progressive disclosure may defer hashes, artifact provenance and extended rights
apparatus. It may **not** defer a required licence acknowledgement, a
withheld-text reason, or a typed absence.

## 9. Verification: what exists, what runs, and what is red

### The suite

`tools/tests/` holds 53 `test_*.py` files using the Python standard library's
`unittest` — no pytest, no plugins, no config file, no `conftest.py`, no
`package.json`, no `node_modules`. Registering a new Python test is dropping
`tools/tests/test_<thing>.py` in place; discovery finds it. A second tree,
`tests/tools/`, holds 34 POSIX-`sh` smoke tests, one per registered tool, run by
`tools/tests/test_tool_registry.py`.

Tools under `tools/` have no `.py` extension and are loaded with
`importlib.machinery.SourceFileLoader`; the canonical pattern is
`tools/tests/test_liturgy_reader_shell.py:31-40`.

### `check-tests` is not in `make check`

`Makefile:842-843` is the only target that runs the suite:

```
check-tests:
	@$(PYTHON) -m unittest discover -s tools/tests
```

`make check` (`Makefile:737-742`) aggregates eighteen targets and
`check-tests` is not among them. Nor is it mentioned anywhere in `guidance/` or
`AGENTS.md`; a grep for the target name across Markdown and Python returns
nothing outside the Makefile. The entire unit suite — every JS model test, every
liturgy reader gate, all 34 shell smoke tests — is opt-in. Four JS files are
exercised by `make check`: `assembly-model.js` (via `check-calendar-rubrics`),
`catena-model.js` (`check-catena`), `reader-model.js` (`check-source-reader`) and
`catalogue-model.js` (`check-document-catalogue`). Everything else needs
`make check-tests`.

### `verify_links` runs only under `verify` and in CI

`make check` does no link checking. `check-public-alpha` runs
`public-alpha check`, which is manifest validation plus a policy summary and
renders no page. `verify_links()` (`tools/public-alpha:2802`) — a stdlib
`html.parser` sweep that rejects root-relative hrefs as non-portable, rejects
links escaping the artifact, resolves directories to `index.html`, requires
every local target to exist, and requires every `#fragment` to exist in the
destination's parsed ids — runs only under `public-alpha verify`, i.e.
`make verify-public-site`, `make verify-public-preview`, and the Pages workflow.
At the measured base, so did the structural browser-HTML lint in
`browser_page_parts()`, the closest thing to an HTML validator in the
repository. Commit `71875b741a20bd86f2895718e4a8eba57fff4a96` later prototyped
the accepted `check-browser-static` target so authored-page splitting and
JavaScript syntax can fail during `make check`; that selective integration is
not integrated by this guidance-only change. `verify_links` itself and
generated-artifact behavior still require build/verify.

Two consequences. A shell change that emits a wrong href passes `make check` and
fails at deploy. And every runtime-constructed link is unverified in any case:
`verify_links` parses static HTML, so the catalogue's links to all 105 web
editions, all 186 PDFs and all 16 library shelves — built with `createElement`
in `texts.js:128,131,153` — are checked by nothing.

### Four Chromium harnesses that no target invokes

`tools/tests/*_browser.mjs` — 5,949 lines across four files — spawn real
Chromium `--headless=new`, serve the repository over an ephemeral `node:http`
server, drive the reader pages over a hand-written Chrome DevTools Protocol
client, and already gate on console errors, failed requests, HTTP errors and
unnamed interactive accessibility nodes from `Accessibility.getFullAXTree`. They
already implement viewport override, 400% page zoom via
`Emulation.setPageScaleFactor`, forced-colors and reduced-motion emulation,
print media, `Input.dispatchKeyEvent` for Tab and Escape, a layout-shift
`PerformanceObserver`, an armed response gate for race testing, sha256 asset
identity, and screenshot capture named by state and viewport. Zero third-party
dependencies.

| Harness | Lines | Route |
| --- | --: | --- |
| `day_reader_integration_browser.mjs` | 2,536 | Day, 40 named assertions |
| `liturgy_reader_visual_reset_browser.mjs` | 1,399 | the visual oracle, 24 governed assertions over 113 captures |
| `propers_reader_integration_browser.mjs` | 1,039 | Propers, 32 assertions |
| `liturgy_reader_shell_browser.mjs` | 975 | the unserved prototype route |

**No Makefile target, no CI step, and no Python test executes any of them.** The
only automated contact is `node --check`, syntax only, from two Python tests.
`check-promised-deliverables` verifies that the `.mjs` paths exist; it does not
run them. `.github/workflows/pages.yml` — the only workflow — runs
`make check-deployment-sources`, `make public-site`, and
`public-alpha verify --deployment-target github-pages`. No browser, no node, no
`make check`, no `make check-tests`.

The harnesses' configured default browser executable was unavailable in the
measured environment; `TRIPTYCH_CHROME` overrides it, and `Makefile:72-76`
documents that seam.

The immutable implementation branch later added a separate
generated-artifact gate and a `check-browser-gate` target, plus a
`check-browser-static` syntax/page-splitting gate. Those are accepted
design-neutral B1 inputs for selective integration, not changes made by this
guidance-only import, and they do not invoke or replace these four
Liturgy-specific harnesses. The generated-artifact gate must be updated to the
D11 matrix (`1440x900` and `320x852`, not its exploratory `1440x1000` and
`320x800`) before it becomes acceptance evidence.

**They work, and their real prerequisite is written down nowhere.** Run against
a checkout that has not built the preview artifact, all four fail in ways that
look like rot: 0 of 25 assertions, every one "Timed out waiting for … readiness";
a harness that emits no report at all; a harness that appears to run zero
assertions. None of that is what it looks like. Three of the four fetch from
`build/public-alpha/preview/` — `liturgy_reader_visual_reset_browser.mjs:15-16`
hardcodes `/build/public-alpha/preview/liturgy/` and
`/build/public-alpha/preview/browse`, and `day_reader_integration_browser.mjs:16`
and `propers_reader_integration_browser.mjs:16` hardcode the same data root — so
the server answers every request 404, the pages never reach ready, and the
timeout is the symptom rather than the fault. `day_reader_integration` waits for
a document titled `Day — Triptych`; a 404 body is `text/plain`, so it throws
before writing its report and stdout is empty. `propers_reader_integration`
writes its report to **stderr**, so reading stdout alone shows nothing and looks
like a harness that ran nothing.

With `make public-preview` run first — five seconds, exit 0 — and with
`TRIPTYCH_CHROME` set to a discovered Chromium executable, the picture inverts:

| Harness | Assertions | Exit |
| --- | --- | --- |
| `liturgy_reader_shell_browser.mjs` | **18 of 18 pass** | 0 |
| `day_reader_integration_browser.mjs` | 39 of 41 pass | 1 |
| `propers_reader_integration_browser.mjs` | 30 of 32 pass | 1 |
| `liturgy_reader_visual_reset_browser.mjs` | 22 of 25 pass | 1 |

Chromium is not the problem and never was: the discovered browser executable
drives all four correctly, `setPageScaleFactor` and forced-colors emulation
included. The launch flags are exonerated. What was missing is a prerequisite no
harness states, no Makefile target expresses and no comment mentions — which is
exactly why four working harnesses read as broken. Any target that runs them
must depend on `public-preview`, and a harness serving the artifact should fail
loudly on a 404 at its own data root instead of waiting out a readiness flag
that cannot arrive.

**The seven residual failures are one finding, not seven.** Every one is a
coverage-or-absence notice the page no longer renders: "partial coverage stays
explicit and subordinate to held text" (`true !== false`); two assertions
matching `/not yet transcribed/i` against an empty string; "explicit readable
formulary and material coverage remain explicit"; one matching
`/not held|not yet transcribed/i` against an empty string; and "partial
production coverage produces one concise reliance notice", twice. They fall
across three harnesses and they all say the same thing: the text that declares
what is *not* held is absent where the accepted contract puts it.

That is the invariant this repository is built around — a page that shows
nothing where a prayer belongs has told the reader the Mass omits it. The
in-progress ritual-flow phase set out to make source and apparatus notes
quieter, and these seven assertions are the accepted contract for how quiet they
may become. This document does not diagnose it: `day-reader.js`,
`propers-reader.js` and `reader-instrument.css` are that deliverable's evidence
paths and are not this lane's to touch. It is recorded because nothing was
running these harnesses, so nothing had reported it.

### JS with no test at all

Of 26 non-fixture browser JS files, twelve are executed under node by some
check, seven are asserted only as source strings, and seven have no test
whatsoever: `catena.js` (42 KB), `history.js` (51 KB), `texts.js` (16 KB),
`scripture/track.js` (32 KB), `scripture/plan.js` (9.1 KB),
`scripture/plan-model.js` (19 KB — a *model* with no coverage and no node
consumer), and effectively `law.js` (59 KB, named in a filename list with no
assertion on its content) and `sources.js` (26 KB, one script-tag presence
check). Their only automated notice is a SHA-256 in `release/public-alpha.json`,
which reports drift, not correctness. **No test executes, parses, or lints any
CSS**, and there is no JS, CSS or HTML linter in the repository; the measured
tool roster included Node but not npm, npx, deno, or bun.

### The measured baseline

The coordinator ran these at the base commit. They are first-hand.

| Command | Exit | Result |
| --- | --: | --- |
| `make public-site` | 0 | 5.1 s; artifact 441 MB, 144 HTML pages (39 non-web-edition routes + 105 web editions) |
| `python3 tools/tpt public-alpha verify --deployment-target github-pages` | 0 | artifact accepted for Pages |
| all 144 built routes over `python3 -m http.server` | — | every route returns HTTP 200 |
| `python3 -m unittest discover -s tools/tests` | 1 | Ran 1226 tests in 466 s: 14 failures, 13 errors, 8 skipped |
| after `make public-preview`: `TRIPTYCH_CHROME=<discovered-browser> … liturgy_reader_shell_browser.mjs` | 0 | 18 of 18 assertions pass |
| after `make public-preview`: `… day_reader_integration_browser.mjs` | 1 | 39 of 41 assertions pass |
| after `make public-preview`: `… propers_reader_integration_browser.mjs` | 1 | 30 of 32 assertions pass; report is on stderr |
| after `make public-preview`: `… liturgy_reader_visual_reset_browser.mjs` | 1 | 22 of 25 assertions pass |

The unit-suite failures were reproduced identically in a clean separate checkout
at base SHA `c27d69153`:

| Test module | Failures | Errors |
| --- | --: | --: |
| `test_public_alpha` | — | 8 |
| `test_index_bible` | — | 5 |
| `test_day_reader_integration` | 2 | — |
| `test_day_missal_integration` | 2 | — |
| `test_propers_reader_integration` | 2 | — |
| `test_mass_ordinary` | 1 | — |
| `test_tool_registry` | 7 | — |

**The red baseline is pre-existing at the base commit.** An implementation lane
inherits it and must not be measured against green. It also must not close it by
recapturing transcripts or blessing a screening count: the repository's own
gates are non-green honestly at the stored-example transcript replay and at
`make check-source-family-screening` (144 unscreened review units), and
`PROJECT-WORK.md:153` states the rule — "Record the count; do not close it by
writing it down."

The earlier zero-assertion/time-out symptoms came from running without the
preview artifact, reading the wrong output stream, or both; they are not a
Chromium-versus-Chrome diagnosis and must not be repeated as a red baseline.
The remaining seven assertion failures are the one already-recorded finding
about absence and partial-coverage notices. The measured tool roster included
Node and Chromium, but not npm, npx, deno, bun, Playwright, or Selenium.

## 10. Constraints that will stop an implementation

**The file-type allowlist.** `verify_output` (`tools/public-alpha:3062`) admits
`TEXT_SUFFIXES = {".html", ".css", ".txt", ".json", ".js"}` (`:249`) plus `.png`,
plus `.pdf`, plus the named files `.nojekyll`, `SHA256SUMS`, `robots.txt`,
`_headers`. A `.svg`, `.woff2`, `.ico`, `.webmanifest`, `.map` or `.jpg` is
rejected outright. Separately, `WEB_BROWSER_SUFFIXES = (".html", ".css", ".js")`
(`:160`) and the browser copy is a non-recursive `glob("*")`, so there is no
mechanism to ship a webfont, SVG sprite, image or JSON asset from a browser
directory at all, and no mechanism to ship anything from a subdirectory. This is
also why `src/web/browser/liturgy/prototypes/` is unpublished. Design to system
font stacks and CSS-drawn marks; a webfont is a generator change plus a bindings
refresh plus a rights record for the font, which is a separate authorized work
unit.

**The 1 MB per-page HTML ceiling.** `PREVIEW_DOCUMENT_LIMIT = 1_000_000`
(`tools/public-alpha:3264`), enforced at `:3304` against every HTML page. A
shell that inlines CSS or a nav manifest into every page multiplies across 144
pages and can push a long web edition over.

**Root-relative hrefs are banned.** `verify_links` (`:2812`) rejects any `href`
beginning `/` as "root-relative link is not portable" — the site is served at
`/triptych/`, a project subpath. Every shell link must be built with
`relative_link()` (`:2071`) and must resolve from every depth: root, `docs/`,
`library/`, and `web/<provider>/<deep>/`.

**The browser-page `<head>` whitelist.** `BROWSER_HEAD_ALLOWED_RE` (`:2510`)
permits only comments, `<meta charset="utf-8">`, viewport, `description`,
`robots`, `<title>`, and `<link rel="stylesheet" href="…">`. A preload, an
inline `<style>`, a `modulepreload`, a canonical link, or a `<template>` is a
hard build failure rather than a silent drop. `BROWSER_SCRIPT_RE` (`:2503`)
matches only the bare `<script src="…"></script>` form: a `type="module"` or
`defer` script would not be extracted and would be left inside `<main>`. A page
must declare at least one stylesheet and at least one script. If a shared shell
adds head content to browser pages, this whitelist must be widened first.

**Six places a site-level asset must be registered.** Nothing derives the
site-level asset list the way `web_data_files()` derives the browser one. A
second `release/public-alpha/assets/*` served on every page requires: (1) the
marker in `layout.html`; (2) the matching key in `wrap_in_layout`'s replacements
(`:2465-2490`); (3) `FIXED_ARTIFACT_INPUT_PATHS` (`:198`); (4) the hardcoded copy
tuple at `:3385`; (5) the hardcoded `expected` set in `expected_artifact_files`
(`:1725-1734`); and (6) `static_sources` in `verify_output` (`:3140`), without
which the copy is never content-verified. Deriving this list once would remove
the whole class of error. Note that browser CSS and JS are *already* in that
unverified half: `verify_web_data` (`:2875`) hashes only files under
`output/browse`, and `static_sources` lists `site.css`, the two PNGs, the
licences and the reading-plan PDFs — so the ~40 browser CSS/JS files are checked
for presence but not for content against their hash-bound sources. The roadmap
has been compensating by hand with post-deploy byte-parity checks.

**The SHA-256 release bindings.** `release/public-alpha.json` carries 375
`site_sources` path-to-hash pairs, among them **53 files under
`src/web/browser/**`** plus `src/web/data/bibles.json` (54 under `src/web/` in
total), `release/public-alpha/layout.html`,
`release/public-alpha/assets/site.css`, and `tools/public-alpha` itself.
(One recon lane reported 53 and another 54; both are right about different
things, and the counts above are what the file contains at this SHA.)
`site_source_binding_errors()` (`:2971`) differences the record against
`site_source_paths()` (`:769`) **in both directions**, so an unrecorded input
and a recorded-but-unread path are both errors. A new `shared/foo.css` is picked
up automatically by `web_data_files()` and therefore fails `verify` until
re-approved. The fix is `make refresh-release-bindings ADOPT=1` — never a
hand-edited hash — and never `ADOPT=1` while another lane is working, because
several agents share one working copy. `release/rights/public-alpha-2026-07-15.md`
moves with it.

**Promised-deliverable paths that cannot be deleted.**
`tools/check-promised-deliverables` fails if any `owner` path or any `pass`
evidence path is missing. That mechanically forbids deleting the retained
candidate and oracle routes, which is the enforcement behind "candidate/oracle
cleanup is deferred and unauthorized":

```
src/web/browser/liturgy/{day,index,day-reader,propers-reader}.html
src/web/browser/liturgy/{day-reader,propers-reader,reader-shell,reader-state,
                         reader-state-adapters,reader-visual-reset}.js
src/web/browser/liturgy/{reader-shell,reader-instrument,reader-visual-reset}.css
src/web/browser/liturgy/reader-visual-reset-{day,propers}.html
src/web/browser/liturgy/prototypes/reader-shell/
release/public-alpha.json     release/rights/public-alpha-2026-07-15.md
tools/tests/{day_reader_integration,propers_reader_integration,
             liturgy_reader_shell,liturgy_reader_visual_reset}_browser.mjs
tools/tests/test_{day_missal_integration,day_reader_integration,
             liturgy_reader_shell,liturgy_reader_state,
             liturgy_reader_visual_reset,propers_reader_integration}.py
tools/tests/fixtures/liturgy-reader-state/v1
```

The checker also requires exactly one `<!-- promised-deliverable: <id> -->`
marker in `PROJECT-WORK.md` per ledger id, and refuses `state = "complete"` while
any requirement is `open` or `blocked`.

**Four `contains`-pinned SHA literals in `guidance/liturgy-browser-roadmap.md`.**
Rewriting that file must preserve them verbatim:
`86a9816c1bffdcbdd09469f5f8d005c666a8045e`,
`1e4587dfe04a11c18e996a16f7fbbdb54bc744a4`,
`c1a590f5854215d68d167d9040e188f41762663e`,
`75234e72c402f0b25a681fbe074da70d895f7274`
(`promised-deliverables.toml:464, 518, 571, 696`). Two more `contains` needles
pin literal sentences into `guidance/repository.md` (`:900`, `:909`).

**Reader-state v1's frozen field vocabulary.** The meaning of
`triptych-liturgy-reader-state/v1` is frozen at snapshot
`c1a590f5854215d68d167d9040e188f41762663e`. The top-level field vocabulary is
closed in code: unknown fields fail, and v1 has no implicit extension data. An
optional field may be added only when absence remains valid and every consumer
preserves it safely. Renaming a field, narrowing or broadening an identity,
reinterpreting a state, or making an optional field required requires a new
version, and validators reject an unknown version. The permanent legacy-URL
inventory is equally fixed: Day hash keys `date, missal, bible, orations, why,
ordinary, ordinary-lang, rubrics, mass` plus manifest-declared Ordinary variant
keys (currently `eucharistic-prayer`), query key `data`; Propers hash keys
`missal, type, mass, bible, orations, cycle, alternative, translation-witness`,
query keys `data, missals`. New keys are additive only; an old key must never be
reused with a changed meaning.

**Two further mechanical facts.** No file under `src/web/data/` may be anything
but JSON (`tools/public-alpha:696-700`). And a published path is a reference
other people hold: on 2026-08-01 a rename broke Catena Omnia's URL and it
returned 404 on the live site until the replacement landed. There is no redirect
mechanism anywhere in the repository — no `CNAME`, no `_redirects`, no
meta-refresh — and the cutover record explicitly rejected redirects, renames and
build aliases in favour of same-path promotion.

**And the operational one.** D20 resolves the shared-index hazard: parallel
lanes use separate full repository directories and never share a working
directory or index. A 2026-08-01 one-file guidance edit committed with a bare
`git commit` carried another lane's staged deletions — 62 files and 49,029
lines — into a push. Separate clones prevent that cross-lane case; each lane
still names paths on commit, checks `git status --short` before, and checks the
resulting commit afterward. This project does not use worktrees.

## 11. B0/B1 implementation guidance -- not work on this branch

The following is the accepted technical sequence for a later implementation
branch created from the exact integrated foundation head. This document is not
an authorization to mutate production. B0/B1 establish
shared non-liturgy seams and design-neutral gates; they do not settle the final
composition of Home, Publications, the publication Reader, Catena, or the
Source Library.

### B0 -- shared non-liturgy foundation

1. **Record the inherited baseline without normalizing it.** Re-run the
   applicable checks on the implementation branch and distinguish inherited
   failures from changes introduced there. A known-red check is a finding, not
   authority to change unrelated source, recapture a transcript, or weaken an
   assertion.
2. **Integrate the neutral static gate selectively.** The
   `71875b741a20bd86f2895718e4a8eba57fff4a96` work parses every browser
   JavaScript file with `node --check` and feeds every authored browser page
   through the existing `browser_page_parts()` parser. This is a cheap,
   design-neutral gate. Integrate its focused Makefile/test changes rather than
   treating the implementation branch as a merge unit.
3. **Establish the corpus shell at the one generator/layout seam.** Generate
   route and domain identity from one ordered source of truth. Add non-liturgy
   masthead, navigation, and one Menu/overlay owner through
   `wrap_in_layout()` and its existing relative-path machinery. The shell is
   route-policy-driven: canonical Day and Propers receive no visible literal
   corpus masthead and no new modal owner. Do not promote `reader-shell.js`.
4. **Preserve static truth and delivery constraints.** Identity, core content,
   canonical PDF links, source/legal truth, and direct URL usefulness survive
   without JavaScript. Links resolve relatively from every route depth and
   under the GitHub Pages `/triptych/` subpath. Do not add a webfont, icon
   library, framework, rejected asset type, server requirement, or oversized
   inlined payload.
5. **Repair only the structural defects required by the shared seam.** Resolve
   nested `<main>` landmarks and skip-link/first-focus behavior at the lowest
   safe generator seam. Fix measured 320-CSS-pixel overflow in Sources and
   Publications without global overflow suppression. Keep interactive targets
   and accessible names testable. Treat selector collisions, duplicated
   helpers, hash-history growth, and the missing history gloss as path-specific
   follow-up debt, not a browser-stack rewrite.
6. **Apply accepted token roles, not prototype pixels.** Use the warm-paper,
   near-black, restrained-oxblood, blue-focus, serif-reading, UI-sans, quiet-rule
   roles in the appropriate shared non-liturgy CSS seam. System/local fallbacks
   must work; exact sizes, spacing, density, and breakpoints remain subject to
   real-data captures and surface acceptance.

Do not split `browser-core.js` for aesthetics, build Search early, infer a
relationship, edit publication prose, change a public path/hash key, or enter
any protected Liturgy production file. Small extractions are later
path-specific work only when measured, dependency-safe, and independently
tested.

### B1 -- design-neutral verification

1. Selectively integrate the built-artifact gate from
   `67ae7d32d4685d296ac9a180e466a949c87eec55`. It must exercise the artifact a
   reader receives, not merely repository HTML. Run `make public-site` for its
   default root, or point `TRIPTYCH_REVIEW_ROOT` explicitly at a completed
   preview artifact.
2. Add an explicit target for the four existing Liturgy harnesses only in the
   owning implementation lane. It depends on `make public-preview`, resolves
   `TRIPTYCH_CHROME`, reads the Propers report from stderr, and fails loudly
   when the preview or its `/browse` data root is absent. The accepted
   prerequisite finding is the 18/18, 39/41, 30/32, and 22/25 run in §9; do not
   restore the pre-preview timeout story.
3. Exercise generated-artifact routes and representative real states at
   1440x900, 1024x768, 768x1024, 393x852, and 320x852, plus 200% text, exact
   320-CSS-pixel reflow, meaningful 400% zoom/reflow, keyboard-only operation,
   forced colors, reduced motion, browser print where the web surface owns it,
   and no-JavaScript/static truth.
4. Gate console errors and defect warnings, failed requests and HTTP failures,
   unnamed interactive accessibility nodes, a single valid main landmark,
   working skip/first-focus semantics, URL/hash compatibility, GitHub
   Pages-style subpath loading, 320px overflow, and required primary target
   sizes. Use the real generated data and rights/absence states.
5. Do not add pixel-diff baselines before the real-data surface has independent
   visual acceptance. Browser-unavailable hosts skip with an explicit reason;
   an available browser reports current defects rather than hiding them.

### Later surface and corpus work

Per-surface production follows accepted C0/C1, D0, E0, and F0 evidence and the
owning guidance. The publication Reader remains a renderer/style change under
`guidance/web-editions.md`, never a prose fork. Search remains J0 -> J1 -> J2:
typed UX first, measured public-only static index second, selected
implementation last. Relationship UI exposes only the proven categories in
D14; a new edge begins as a schema/generator work unit. Acceptance still
requires a full local artifact build and
`public-alpha verify --deployment-target github-pages`; neither that
verification nor a feature-branch checkpoint authorizes merge to main or Pages
publication.

## 12. Risks

**R1. Editing files owned by an in-progress deliverable.** Evidence:
`liturgy-reader-live-ritual-flow-2026-08-07` is `in_progress` with all six
requirements `open`; its evidence paths are
`src/web/browser/liturgy/reader-shell.js` and
`src/web/browser/liturgy/reader-instrument.css`; its only implementation commit
`85abf971e` is an explicit work-in-progress checkpoint written after an
emergency shutdown, and it modified `day.html`, `index.html`, `day-reader.js`,
`propers-reader.js`, `reader-shell.js` and `reader-instrument.css` and was
pushed, so the live canonical readers carry unreviewed ritual-flow code today.
No release hashes were updated for that phase. Mitigation: this integration and
Wave 1 corpus work touch no production file under `src/web/browser/liturgy/`
and no Liturgy binding, fixture, controller, test, or data owner. A later lane
may enter only after the deliverable closes or a carve-out and its acceptance
authority are recorded explicitly.

**R2. A stylesheet reorganisation breaking a page that never mentions the
selector.** Evidence: `history.css:240`'s `.field` wins over the shared control
`.field` purely by load order, and the file says so; `day-missal.css:51` restyles
`body > .site-header` unscoped on four published pages; `texts.css:191-199`
shadows the shared `.detail` by restating every declaration; `browser-core.css`'s
global `:focus-visible` (`:202-205`) is injected after `site.css` and therefore
overrides the site header's own focus treatment on every browser page.
Mitigation: a later implementation performs any required rename before moving
shared CSS, as its own path-specific commit with before/after real-route gates;
this guidance change performs neither.

**R3. Flipping the dual-context guard.** Evidence: `browser-core.css:134`
`body:not(:has(> .site-header))` switches the whole page between "inside the site
layout" and "opened from the repository," drawing eighteen declarations in the
second case. A shell that introduces a wrapper element between `body` and
`.site-header`, or adds a `.site-header` to a repository page, silently flips it
— which is the regression the guard was written to fix. Mitigation: treat the
selector as a contract; if it must change, change it deliberately and everywhere
at once, and add a test that opens a browser page from the repository.

**R4. Shipping a change that passes `make check` and fails at deploy.**
Evidence: at the measured base, `verify_links` and browser-page splitting were
not both exercised by `make check`; the accepted static gate moves authored-page
parsing earlier, but generated links and artifact-only defects still require
build, verify, and the generated-artifact browser gate. `94ae83386` records a
deploy refused for `catena/index.html: broken
local link: ../law/` because the directory existed in the working tree and not
in the committed tree; `fd833311e` records the same link surviving in six pages
an hour after being removed from one; `c8863b50a` records a Pages failure caused
by a research survey written where `source-library validate` forbids it, which
no local check caught. Mitigation: run `make public-preview &&
make verify-public-preview`, the relevant generated-artifact browser gate, and
the final GitHub-Pages-target verification before any authorized push; never
link a page whose files are untracked.

**R5. Adding an asset the artifact will not accept.** Evidence: the file-type
allowlist and the six-place registration in §10. Mitigation: design to system
fonts and CSS marks; if an asset type is genuinely required, treat it as its own
authorized work unit with a rights record.

**R6. Regressing the liturgy first viewport.** Evidence: the accepted geometry
is measured and protected — shell height 58–59 px, first liturgical content at
**181 px at 393×852**, reading width 571 px desktop / 361 px at 393×852 / 288 px
at 320×852, zero horizontal overflow at every measured viewport; removing a
diagnostic row is what moved first content from 255 px to 181 px. The vision
invariant is that the first useful viewport contains real liturgical content and
that the reader shell "never becomes permanent dashboard chrome." Mitigation:
the current corpus wave adds no persistent chrome to either Liturgy route. Any
future proposal is a separately authorized Liturgy vision/acceptance decision,
not a B0 implementation detail.

**R7. Breaking a published URL or a hash key.** Evidence: the Catena Omnia 404;
the absence of any redirect mechanism; the explicit rejection of redirects and
build aliases at cutover; the frozen legacy-URL inventory; and the live
cross-instrument contract `catena.js:519` → `sources.js:594`. Note also
`catena.js:896-903`'s deliberate *refusal* to translate a legacy `language=` key
into `voice=` — an inbound `#language=en` is ignored and the page opens on
"Everything held" rather than guessing. A generic key-alias facility invites
someone to "fix" that. It is not a bug. Mitigation: additive keys only; inventory
every current key into a compatibility fixture before changing parsing; preserve
`track.js:839-842`'s rule that a hash naming none of the page's keys is not
navigation, or the skip link starts navigating.

**R8. Committing another lane's staged work.** Evidence: the 2026-08-01 bare
`git commit` that pushed 62 files and 49,029 deleted lines, and the bad stash pop
that left conflict markers in 14 paths. Mitigation: D20 requires separate full
checkouts; also use path-scoped commits and path-scoped binding refreshes.

**R9. A search or relationship UI asserting an edge that does not exist.**
Evidence: §7's zero-hit grep for every named edge; the empty `correspondence`
array on all 169 law index rows; the `passage.<id>` strings living in free-text
`basis` fields; the catena's stated find-in-page limitation. Mitigation:
enumerate the edges before designing the panel; a new edge type is a schema
change under its owning guidance, not a UI inference.

**R10. Flattening a rights or absence distinction while tidying.** Evidence:
§8. The specific losses available today are unifying history's withheld and
unread toward the faint treatment rather than toward Law's; deferring a licence
acknowledgement into a disclosure; and dropping the state at the DOM boundary
where only a CSS class carries it. Mitigation: emit `data-state` alongside the
class; treat the point-of-use acknowledgement as non-deferrable; unify toward
Law and get the maintainer's assent for the visible change.

**R11. Splitting the propers file and making the payload worse.** Evidence:
`structure/propers/roman-1962.json` compresses 13.7:1 because it is
pretty-printed and repetitive; `structure/paragraphs/` compresses 1.23:1 across
5,548 small files. Mitigation: measure a candidate split against the gzip
figures in §6 before adopting it. The `day-reader.js:377-381` single
`Promise.all` remains a measured finding inside protected Liturgy, not an
authorized corpus fix.

**R12. The 15-minute CI ceiling.** Evidence: five recorded Pages runs
(`31104342722`, `31106008011`, `31107294462`, `31110517661`, `31113461987`) built
and uploaded a verified artifact and then failed or were cancelled at
`deploy-pages` polling. Build plus verify already SHA-256 a 20,441-file artifact
at least three times and re-render 144 pages twice; per-page work added to
`wrap_in_layout` is paid twice. Mitigation: keep per-page shell work cheap, and
remember that a timed-out run is not a failed change — but also that it is not a
successful deployment and never supersedes an accepted parity run.

## 13. Resolved C1--C16 dispositions

The implementation reconnaissance returned C1--C16 for coordinator review.
They are no longer open questions. The following D1--D20 dispositions are
binding; later work must not restore the pre-review "safer reading" language
as unresolved status.

**C1 -- protected Liturgy collision: resolved by D2 and D18.** The corpus wave
does not supersede Live Reader -- Ritual Flow & Orientation. Every Liturgy
production file is protected for this integration and Wave 1 work. At minimum,
do not edit or move `reader-shell.js`, `reader-instrument.css`, canonical
`day.html` or `index.html`, their controllers, state behavior, release
bindings, fixtures, or owning tests. Do not add a fifth action, second modal,
literal corpus masthead, Search, or print redesign. If the owner closes, inspect
the new main state before requesting a liturgy-specific change.

**C2 -- global Search versus the Liturgy first viewport: resolved by D2 and
D13.** A4 Jump is a bounded fixture, not Search. Production Search follows J0,
J1, then J2 and does not enter the reader shell. A future quiet Liturgy
exit/context affordance may use an already accepted seam such as Details or a
terminal/footer treatment only after separate Liturgy visual acceptance. The
accepted first viewport remains protected.

**C3 -- task-oriented Home versus seven portals: resolved by D7.** Prototype a
task-oriented entrance above or beside the seven editorial portals. Preserve
Faith, Scripture, Liturgy, History, Formation, Mary, and Law in their current
order and color identities unless real-data evidence supports an explicit
`guidance/repository.md` amendment. Do not silently break the README
transform or turn Home into a dashboard.

**C4 -- branch and publication authority: resolved by D19.** Assigned agents
may create and push coherent project feature/integration branch checkpoints.
This plan does not authorize merging or pushing main, triggering public
cutover, force-pushing, or rewriting shared history. GitHub Pages publication
remains an explicit later decision even when local Pages verification passes.

**C5 -- long-form web-edition ownership: resolved by D9.**
`guidance/web-editions.md` controls the publication Reader. Change rendering,
not `web/<provider>/*.md` prose; preserve the visible rights colophon,
revision identity, declared omissions, stable anchors, and canonical PDF; rerun
web-edition currency checks after converter or renderer changes.

**C6 -- durable continuity location: resolved by D10.** Required project truth
lives in the tracked corpus master plan, vision, roadmap, implementation record,
owning surface guidance, `PROJECT-WORK.md`, and promise ledger. An ignored or
force-tracked `build/agent-continuity/**` artifact may support a handoff but is
never the sole owner of a decision.

**C7 -- stale Liturgy milestone framing: bounded by D2 and D18.** The live
canonical readers are production surfaces governed by their accepted vision;
missing modes remain coverage limits. This corpus project neither rewrites the
Liturgy roadmap nor treats an old M6 description as permission to change those
routes.

**C8 -- competing screenshot matrices: resolved by D11.** The site-wide matrix
is 1440x900, 1024x768, 768x1024, 393x852, and 320x852, plus 200% text, exact
320-CSS-pixel reflow, meaningful 400% zoom/reflow, keyboard, forced colors,
reduced motion, applicable browser print, no JavaScript, and
console/network/HTTP/accessible-name checks. A more specific accepted surface
may add evidence but may not silently replace this matrix. Pixel baselines wait
for independent real-data visual acceptance.

**C9 -- faceted Publications versus one owning catalogue: resolved by D1 and
D8.** Keep route `/texts/` and label it Publications. It is a discovery view
that may aggregate metadata, facets, browser-read links, formats, and
treatments. It is not a second canonical publication home or a second owning
PDF catalogue.

**C10 -- unavailable fonts/assets: resolved by D5 and D12.** Use robust
system/local font stacks and CSS-native marks. Do not add a webfont dependency,
icon library, framework migration, generator-rejected asset type, root-relative
link, server dependency, or unmeasured payload. A font or new asset type is a
separate rights-plus-generator work unit.

**C11 -- Search index as an unrecorded writer: resolved by D13.** Do not build
Search in B0. After typed real-object UX is accepted, J1 measures a public-only
static index for rights leakage, payload, latency, memory, multilingual
behavior, and route state. J2 implements only the selected design and records
any new `src/web/data/` writer, tool, smoke test, and additivity contract under
`guidance/web-data.md`.

**C12 -- unsupported Related edges: resolved by D14.** The safe categories are
explicit containment; passage to artifact/segment; Catena fragment to Scripture
locus; Catena passage to Source Library passage; act descent/change/history;
document to catalogue; and Mass to propers to resolved Scripture. Do not infer
`translation_of`, `used_by`, `derived_from`, canon correspondences,
Law-to-Source citations, or generic recommendations. A new edge begins as a
schema/generator change under its owning guidance.

**C13 -- rights under progressive disclosure: resolved by D15.** Hashes,
extended artifact provenance, long legal apparatus, and secondary technical
metadata may be deferred. A required licence acknowledgement at point of use, a
withheld-text reason, typed absence/unread/unsupported/invalid state, and the
availability-versus-redistribution distinction may not. Preserve these
semantically in data and DOM, not only with color or a CSS class.

**C14 -- unreachable guidance: resolved by D10 and repository routing.** Durable
corpus guidance must be tracked and routed from `AGENTS.md` in the same
coherent integration. A new file that no applicable routing rule tells agents
to read is not a complete guidance change.

**C15 -- local reading progress: resolved by D16.** Defer it from the current
foundation wave. If later accepted for long-form publications, storage is
optional and an explicit URL wins. Do not add persistence to Day; its
no-memory behavior is intentional.

**C16 -- worktree policy: resolved by D20.** Parallel lanes use separate full
repository directories, never worktrees and never a shared working
directory/index.

Coordinator amendments also settle the foundation vocabulary around these
conflicts. D3 uses **Independent treatment** as the human-facing label,
**Parallel treatment** only as a relationship label, and explicit provider
metadata. D4 accepts Reader, Catalogue, and Instrument as archetypes rather than
one layout. D5 accepts token roles rather than synthetic prototype pixels. D6
accepts the seven-destination information architecture while leaving visible
desktop count and geometry to real evidence. D17 records the architecture
findings as incremental engineering debt and explicitly forbids turning B0 into
a browser-stack rewrite.
