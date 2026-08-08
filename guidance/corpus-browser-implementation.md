# Corpus browser implementation

## 1. Status and scope

This document is the Claude implementation lane's technical record for the
corpus-wide redesign of Triptych's non-PDF web surfaces. It states how those
surfaces are actually built at base commit `c27d6915319785686d1df6a1401a489aa9921f6f`,
what will stop an implementation that does not know it, and in what order the
work can be done so that each step can be verified before the next begins.

It owns the architecture: the three page pipelines, the single layout template,
the shared stylesheet and script, the seven browser instruments, the generated
data layer they read, and the gates that admit or refuse a change to any of
them.

It does not own the visual or product contract. Which colours, which typography,
which navigation model, whether the corpus reader keeps or hides the site
chrome, whether a global search box exists at all — those are decisions for the
design lane, and this document names them as decisions rather than making them.
Where a decision is required before an implementation step can proceed, the step
says so.

It does not own liturgical semantics. `guidance/liturgy-browser-vision.md`
continues to govern browser-visible liturgical reading, navigation, study,
comparison, responsive behaviour, accessibility, performance, printing, and
sharing on the Day and Propers entrances, and its fourteen product invariants
bind any site-wide design that touches them.
`guidance/liturgy-browser-roadmap.md` remains the liturgy execution record and
may not weaken a vision invariant. `guidance/liturgy-reader-state.md` owns the
frozen v1 reader-state contract and the permanent legacy-URL inventory.
`guidance/web-data.md` owns everything the browser fetches from `src/web/data/`.
`guidance/web-editions.md` owns the tracked Markdown web editions of
publications — a document the corpus master plan's own read-list omits, and
which governs exactly what its long-form-reader lane proposes to change.

Two notes on where this document sits. First, `guidance/corpus-browser-vision.md`
and `guidance/corpus-browser-roadmap.md` do not exist at the base commit; the
guidance directory holds twenty-five files and none of them names the corpus
browser. Creating them is greenfield work, and `AGENTS.md`'s routing table is how
a later agent finds an owning document — a new guidance family that is not
routed to from `AGENTS.md` is unreachable by the discipline that makes the rest
of the system work. Second, `guidance/corpus-browser-master-plan.md` is tracked
one commit past the base, at `b0e052037`; a lane branching from `c27d69153` will
not see it.

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
`make public-site` on this host exited 0 in 5.1 s and produced 441 MB and 144
HTML pages (39 non-web-edition routes plus 105 web editions).

`wrap_in_layout()` is already the single shell application point. A shared
corpus shell is an extension of an existing seam, not a new architecture. What
the seam currently carries is thin: the layout's primary navigation offers three
links — Home, About, Feedback — and names no section and no instrument.

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

**`src/web/browser/liturgy/reader-shell.js`** (296 lines) is the strongest
candidate for promotion into `shared/`. Its own first line says what it is:
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

Hoisting `majorSelector`, `headingSelector` and `defaultGroup` into `options`
makes the file corpus-neutral with no behaviour change. Two existing tests
already protect its neutrality:
`test_shared_shell_remains_one_entrance_neutral_implementation`
(`tools/tests/test_propers_reader_integration.py:95`) and
`test_day_and_propers_use_the_exact_same_shell_files` (`:84`).

Its companion `reader-shell.css` (207 lines) is a foundation rather than a
competing shell: it has no colour identity, consuming `--panel`,
`--section-line` and `--focus` from browser-core, and it is the only definer of
`--reader-safe-{top,right,bottom,left}`, which four other files consume. Three
things in it are worth lifting whole: the `--reader-shell-height` plus safe-area
token set with its matching `scroll-padding-block`/`padding-bottom` pair
(`:11`, `:16`), which is why an anchor never lands under the fixed bar; the
universal shrink rule `.reader-surface, .reader-surface * { min-width: 0;
overflow-wrap: anywhere; }` (`:76`), which is the single line making "every
surface reports `scrollWidth <= clientWidth`" hold; and the three-tier
breakpoint ladder — 72rem side rails, 52rem bottom sheets, 25rem single column.

Two caveats on the shell before it is lifted. The desktop rails at
`reader-shell.css:176-189` are visually pinned but still `showModal()` dialogs,
so the page behind them is not focusable, selectable or scrollable — which
contradicts the accepted disposition in
`guidance/liturgy-reader-shell-prototype.md` that a wide-desktop Study rail is
a *pinned nonmodal*. Retrofitting a non-modal mode means splitting `open()` into
modal and inline paths. And the file cannot be moved while the liturgy reader
deliverable that owns it is in progress; see §13.

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
links, not landmark nesting.

One correction, because this document earlier let two separate things be read as
one. The layout's own skip link **is** present and **does** point at an element
that exists, on all thirteen routes. The gate's twenty-seven
`skip-link-targets-existing-element` failures are therefore not a missing or
dangling skip link. They are a focus trap: `propers-reader.js:1020` calls
`readerShell.open('browse', …)` on load when no formulary is deep-linked, and
`reader-shell.js:220` opens that surface with `showModal()`, so the rest of the
document is inert and Tab never reaches the skip link at all. It affects
`/liturgy/index.html`, `/liturgy/propers-reader.html` and
`/liturgy/reader-visual-reset-propers.html`. No generator change can fix it: it
is instrument-owned and both files sit inside the protected reader deliverable,
so it belongs to that deliverable and to no corpus lane. The stripped-skip-link
finding above stands and is a separate, milder matter about which landmark the
surviving link targets.

And `history.js:341-348` sets `role="img"` on the
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

The Source Library uses a strict four-level dotted scheme, and it is the only
part of the corpus with a designed identifier grammar:

```
work.<author-slug>.<work-slug>
edition.<author-slug>.<work-slug>.<imprint-slug>
artifact.<author>.<work>.<edition>.<name>-<hash8>
passage.<author>.<work>.<edition>.<locus-slug>
```

A passage id is directly addressable as
`structure/sources/text/<passage_id>.json`, which is what makes the one live
cross-instrument link work: `catena.js:519` writes
`../sources/#passage=<encoded id>` and `sources.js:594` reads it. That handler,
`followPassage()` (`sources.js:576-590`), fetches the passage's own text file and
reads `work_id`/`edition_id` off it rather than decomposing the id. That is the
right construction and must survive any redesign.

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

### The source graph is containment plus untyped foreign keys

A grep across `structure/sources/index.json` and all 655 edition files returns
**zero hits** for `cites`, `quotes`, `comments_on`, `translation_of`,
`edition_of`, `artifact_of`, `passage_of`, `used_by`, `governs`, `changes`,
`supersedes`, `appointed_in`, and for the generic `relation`, `relationships`,
`edges`, `links`. There is no named-edge vocabulary in the served Source Library
data. The graph is expressed entirely by nesting and by untyped foreign keys:
`works[].editions[]` nesting plus `work_id`; `artifacts[]` nesting plus
`edition_id` on all 1,467 upstream artifact records; `passage.edition_id` on all
2,751 passages; `passage.artifact_id` on 2,613 of them; `passage.segment_id` on
138.

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

- **Containment**, everywhere: work → edition → artifact → passage; slice →
  station → unit; work → edition in the document catalogue.
- **Passage → controlling artifact**, and **passage → segment**, as explicit
  foreign keys.
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

**Withheld prose is never sent to the browser.** A non-readable passage carries
no `text_path` and no file exists under `structure/sources/text/`. There is no
URL the page could fetch. `sources.js:26-29` states the consequence: "a page bug
cannot publish a withheld text, because the words were never sent to the browser
in the first place." Any redesign that introduces a text-fetch layer must
preserve that shape: the absence of a path, not a flag the client is trusted to
honour.

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
So does the structural browser-HTML lint in `browser_page_parts()`, which is the
closest thing to an HTML validator the repository has.

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

The default Chrome binary in the harnesses is
`/usr/bin/google-chrome-stable`, which does not exist on this host;
`TRIPTYCH_CHROME` overrides it, and `Makefile:72-76` documents that.

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

With `make public-preview` run first — five seconds, exit 0 — and with no flag
change and the same `TRIPTYCH_CHROME=/usr/bin/chromium`, the picture inverts:

| Harness | Assertions | Exit |
| --- | --- | --- |
| `liturgy_reader_shell_browser.mjs` | **18 of 18 pass** | 0 |
| `day_reader_integration_browser.mjs` | 39 of 41 pass | 1 |
| `propers_reader_integration_browser.mjs` | 30 of 32 pass | 1 |
| `liturgy_reader_visual_reset_browser.mjs` | 22 of 25 pass | 1 |

Chromium is not the problem and never was: `/usr/bin/chromium` 151.0.7922.108
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
CSS**, and there is no JS, CSS or HTML linter in the repository; none can be
installed, because the host has node but no npm, npx, deno or bun.

### The measured baseline

The coordinator ran these at the base commit. They are first-hand.

| Command | Exit | Result |
| --- | --: | --- |
| `make public-site` | 0 | 5.1 s; artifact 441 MB, 144 HTML pages (39 non-web-edition routes + 105 web editions) |
| `python3 tools/tpt public-alpha verify --deployment-target github-pages` | 0 | artifact accepted for Pages |
| all 144 built routes over `python3 -m http.server` | — | every route returns HTTP 200 |
| `python3 -m unittest discover -s tools/tests` | 1 | Ran 1226 tests in 466 s: 14 failures, 13 errors, 8 skipped |
| `TRIPTYCH_CHROME=/usr/bin/chromium … liturgy_reader_shell_browser.mjs` | 1 | several assertions fail, including "real Proper renderer did not produce enough sections" |
| `… liturgy_reader_visual_reset_browser.mjs` | 1 | 0 of 25 assertions pass, all "Timed out waiting for … readiness" |
| `… day_reader_integration_browser.mjs` | 1 | exits without emitting parseable JSON |
| `… propers_reader_integration_browser.mjs` | 1 | zero assertions run |

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

Host: node v26.7.0, chromium 151.0.7922.108, chromedriver 151. No npm, npx, deno
or bun; no Playwright, no Selenium. Whether the four harness failures are a
chromium-versus-chrome difference or genuine staleness is **not yet
determined**, and determining it is step 2 of §11.

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

**And the operational one.** Several agents share one working copy and therefore
one git index. On 2026-08-01 a one-file guidance edit committed with a bare
`git commit` carried another lane's staged deletions — 62 files, 49,029 lines of
the catena's browser structure — into a push. Always name paths on commit:
`git commit -m "…" -- <path> [<path> …]`, `git status --short` before,
`git show HEAD --stat` after.

## 11. Proposed implementation sequencing

Each step is independently verifiable and none requires a visual decision before
that decision exists. Steps 1–4 are prerequisites; 5–9 are the shared foundation
(master plan §8 lane **B0**/**B1**); 10 onward unblock the per-surface lanes.

**1. Establish the honest baseline. Depends on nothing.** Record the 14 failures
and 13 errors from `python3 -m unittest discover -s tools/tests` as the
pre-existing state, with the per-module breakdown in §9, in the lane's tracked
record. Verify: the same counts reproduce in a clean checkout at
`c27d69153`. This exists so that no later step can be credited with a
regression it did not cause, and so that no later step can hide behind the red.

**2. Give the four Chromium harnesses a target that runs them. Depends on 1.**
This step was originally written as "determine why they fail"; that is now
answered in §9 and the answer is that they do not fail. They need
`make public-preview` first, and with it they return 18/18, 39/41, 30/32 and
22/25 under `/usr/bin/chromium`. What remains is mechanical: a
`check-browser-harnesses` target that depends on `public-preview`, resolves
`TRIPTYCH_CHROME` and skips with a stated reason when no browser resolves,
reads `propers_reader_integration`'s report from stderr where that harness
writes it, and stays out of `check:` for the same reason `check-browser-gate`
does. Verify: the target reproduces the four counts above. Do not adjust an
assertion to raise them — the seven that fail are one real finding about
absence notices, and §13-C1 governs who may act on it. Until a target exists,
every browser-visible change is being made without the oracle that was sitting
in the tree the whole time.

**3. Wire a narrow browser-model gate into `make check`. Depends on 2.** Add a
`check-browser-models` target running the subset of `tools/tests` that exercises
JS under node — `test_law_page.py`, `test_liturgy_reader_state.py`,
`test_mass_ordinary.py`, the reader-integration string suites — and append it to
`check:`. Verify: `make check-browser-models` exits with the same pass/fail set
as the corresponding modules under `check-tests`. Do not wire all of
`check-tests` into `check` in the same step: 466 s and a known-red baseline is a
separate decision for the maintainer.

**4. Add a blanket `node --check` sweep and a static browser-HTML lint. Depends
on 3.** A ten-line `tools/tests/test_browser_syntax.py` running `node --check`
over every `src/web/browser/**/*.js` closes the seven files that no check parses
today. A second small test calls the existing `browser_page_parts()` over every
browser page so head-whitelist and whole-document violations fail at
`make check` instead of at build. Both use logic that already exists. Verify:
introducing a deliberate syntax error in a scratch copy fails the test.

**5. Fix the four hazards that block a shared shell. Depends on 4.** These are
prerequisites, not improvements. (a) Give `T.fail` and `T.showBanner` a target
argument or landmark lookup, so they stop hard-coding `#reading` and `#banner`;
five `<main>` ids exist and law and history currently get a silent no-op.
(b) Rename history's change-row `.field` to `.change-field` in `history.js`,
`history.css` and the markup together, removing the load-order dependency.
(c) Rename texts' record card off `.detail` in `texts.js` and `texts.css`,
removing the deliberate shadow of `browser-core.css:556-564`. (d) Scope
`day-missal.css`'s six unscoped `body > .site-header` blocks to the page.
Verify: each is a mechanical rename or signature change with an unchanged
rendered DOM; capture before/after at 393×852 and 1440×900 on the affected
routes. None of these makes a visual decision.

**6. Promote `reader-shell.js` and `reader-shell.css` to `shared/`. Depends on
5, and on the liturgy deliverable in §13-C1 being closed or the files being
explicitly carved out.** Add `majorSelector`, `headingSelector` and
`defaultGroup` to `options`, defaulted to today's values, and move the file
unchanged otherwise. Two `<script src>` path edits. Verify: the two neutrality
tests at `tools/tests/test_propers_reader_integration.py:84,95` still pass; the
Day and Propers harnesses produce identical assertion sets before and after;
`make refresh-release-bindings ONLY="<the moved paths>"`. **This is the single
highest-value, lowest-risk move in the lane and it unblocks lanes E, F, G, H and
I**, each of which otherwise re-derives a worse subset of it.

**7. Add the shared primitives that already have shared CSS. Depends on 6.**
`Triptych.lazyBlock(summary, path, render)` (23 lines, two call sites, emits
`.fold`/`.fold-summary`/`.fold-body`/`.placeholder`/`.error`, all already styled
shared); `Triptych.memoJSON(path)` replacing five near-copies, with an optional
counter hook so `window.dayReaderDebug.loads` keeps working for the harness;
`Triptych.citations(row)`; and one act-record vocabulary module carrying
`EDGE_WORDS`, `CITATION_WORDS`, `STATE_WORDS`, `facts()`, `whatHappened()`,
`lineLabel()` and `magnitude()` with the label differences as parameters.
Attaching the render token to `memoJSON` gives law and history the
overtaken-render discipline sources already has. Verify: the `none-claimed`
gloss appears on all 26 affected history stations; `magnitude` agrees between
the two pages; no visual change elsewhere.

**8. Add the shared accessibility blocks that no instrument outside liturgy
has. Depends on 6.** A `@media (forced-colors: active)` token remap in
`browser-core.css`, modelled on `reader-instrument.css:703-729`, which gives six
instruments high-contrast support they do not have and cannot regress liturgy
(whose own block is more specific). Extend the shared
`prefers-reduced-motion` block with `html { scroll-behavior: auto }` and delete
the four reader copies. Add a shared `@media print` block. Verify: the harnesses'
existing forced-colors and reduced-motion emulation, run per route.

**9. Build the design-system regression harness (lane B1). Depends on 2 and 8.**
Extract the CDP boot plus console/request/HTTP/accessible-name collection that
all four `.mjs` files already implement into one shared module, and add a thin
per-route harness over all thirteen published browser pages. Assert only
design-neutral invariants: no console error, no failed request, no unnamed
`button`/`link`/`radio`/`combobox`/`textbox` node, no horizontal document
overflow at 320 CSS px, every interactive target ≥44×44 px, nothing clipped at
400% zoom. Capture the {320, 393, 768, 1280} × {default, forced-colors,
reduced-motion, print, 400%} matrix per route as evidence. **Skip cleanly when
`TRIPTYCH_CHROME` resolves to nothing**, exactly as the PyYAML-gated targets
skip today, because the browser is deliberately excluded from the installed
dependency set. Do not add pixel-diff baselines: a baseline *is* a visual
decision, and it has not been made. Verify: the harness reproduces today's
known-good states and reports today's known defects — the nested `<main>`, the
`role="img"` pruning, the sources 320px overflow, the texts 320px overflow —
rather than passing them.

**10. Emit one generated site navigation. Depends on 5 and on the design lane's
decision about whether the liturgy routes keep site chrome.** Add a marker to
`layout.html`, a `site_navigation(source_relative, output_relative)` function
beside `navigation_state()`/`breadcrumb()` holding one ordered destination list,
and one replacement entry in `wrap_in_layout` — three steps touching two files,
applied identically to all three producers. Then delete the seven hand-written
footer link paragraphs, which fixes fifteen missing edges by construction, and
change `reader_shelf()` to read `works[].catalog_page` out of `corpus.json`
instead of its fourteen-rule substring table, which removes a second derivation
and fixes the one measured disagreement
(`web/claude/liturgy/roman-rite/comparative/two-missals-one-sacrifice.md`
breadcrumbs to `library/liturgy.html` while the catalogue says
`library/faith.html`). Verify: `make verify-public-preview` passes
`verify_links` with every new link resolving from every depth; a unit test over
`site_navigation()`; `aria-current` behaviour reviewed against the three
existing assertions at `tools/tests/test_public_alpha.py:300-320`, which
currently assert that 121 pages claim to be Home. **The blocking design decision
is `reader-instrument.css:40-45`**: a nav placed inside `.site-header` is hidden
on the six liturgy routes.

**11. Resolve the nested `<main>`. Depends on 10.** Either have `layout.html`
not wrap browser pages in its own `<main>`, or have `render_browser_page` emit
the page's landmark as a `<div>` while the repository-opened copy keeps `<main>`.
Restore a meaningful skip target while doing it. Verify: a landmark assertion in
the per-route harness from step 9, run against the *built* artifact rather than
the repository page — which is the gap that let this defect pass every gate.

**12. Split `browser-core.js`. Depends on 7.** Move the bible/loci/propers half
(`:202-625` and `:1010-1408`, including the inline fallback chapters) into
`shared/browser-scripture.js`. Five of nine reading pages stop downloading
~35 KB they never call. Verify: a `<script src>` change across seven pages, no
behaviour change, harness assertion sets unchanged, bindings refreshed.

**13. Per-surface lanes (C2, D1, E1, F1, G1, H1, I1). Depend on 6, 7, 8, 9.**
Each consumes the shared shell rather than re-deriving it. Four items are
sequencing prerequisites inside specific lanes rather than shared work:
`plan-model.js` must be converted to the UMD form the other models use and its
`prose()` renderer extracted into the view before any script-order change, or a
reorder breaks it silently with no check that would notice; `history/graph-model.js`
must be extracted as a UMD sibling of `reader-model.js` before the history map
is touched, because `layout()` is the most intricate derivation in the corpus
and the only one with no check at all; texts needs a per-document hash key
before a catalogue redesign, because today `open()` writes nothing to the URL
and a reader who finds a document and copies the address sends a filtered list;
and catena's two offline-fallback promises (`catena.js:970`, `texts.js:391` call
`setInlineNotice` and never `addInlineFiles`) must be fixed or dropped before a
shell centralises the banner, or the shell centralises a promise two pages
cannot keep.

**14. Search index feasibility (J1) and implementation (J2). Depend on 9 and on
the design lane's result taxonomy.** J1 is a measurement, not a build: the
minimal title-and-identifier index is ~7,000 objects and ~100 KB gzipped, which
is smaller than one propers file, and full text is a different order. A
generated index is a new writer under `src/web/data/` and must, in the same
commit, add its line to the writer block in `guidance/web-data.md`, register a
tool via `tmt new`, add `tests/tools/<id>.test`, and prove additivity. **The
scoping hazard is stated in the catena's own footer**: text not fetched is not
in the document, so a search box that appears to search the catena but reaches
only the 1.66 MB of spines and not the 5.99 MB of prose is a fluent wrong answer
of exactly the kind this repository is built against. Either search states its
scope per instrument on the page, or it does not ship. Index only on
`readable == true` **and** presence of `text_path`, and never index `notes`,
`context` or `rights_basis` from a passage whose rights are `restricted`,
`licensed` or `unresolved` — 903 records whose `notes` field sometimes quotes
the withheld source.

**15. Cross-object relationship links (K1). Depends on 13 and on §7.**
Implement only the edges that exist. If the design calls for `used_by`, that is
a generator change to `tools/source-reader` to project the 1,854 bindings, under
`guidance/sources.md`, before any UI work — not a UI inference.

**16. Acceptance and integration (L1, L2, M0).** L1 and L2 consume the step-9
harness. M0 requires a full local `make public-site` plus
`public-alpha verify --deployment-target github-pages` before any push, because
`make check` does not build the site and a shell change can pass `check` and
fail in CI. Note that pushing `main` *is* the deploy authorization, and see
§13-C4 on who holds it.

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
No release hashes were updated for that phase. Mitigation: do not touch those
six files until the deliverable is closed or the corpus lane is explicitly
carved out of it in the ledger, with a new or superseding requirement rather
than a silent scope expansion. Step 6 is the only step that needs them, and it
is the only step that should wait.

**R2. A stylesheet reorganisation breaking a page that never mentions the
selector.** Evidence: `history.css:240`'s `.field` wins over the shared control
`.field` purely by load order, and the file says so; `day-missal.css:51` restyles
`body > .site-header` unscoped on four published pages; `texts.css:191-199`
shadows the shared `.detail` by restating every declaration; `browser-core.css`'s
global `:focus-visible` (`:202-205`) is injected after `site.css` and therefore
overrides the site header's own focus treatment on every browser page.
Mitigation: step 5 does the renames before anything is moved, each as an isolated
commit with before/after captures.

**R3. Flipping the dual-context guard.** Evidence: `browser-core.css:134`
`body:not(:has(> .site-header))` switches the whole page between "inside the site
layout" and "opened from the repository," drawing eighteen declarations in the
second case. A shell that introduces a wrapper element between `body` and
`.site-header`, or adds a `.site-header` to a repository page, silently flips it
— which is the regression the guard was written to fix. Mitigation: treat the
selector as a contract; if it must change, change it deliberately and everywhere
at once, and add a test that opens a browser page from the repository.

**R4. Shipping a change that passes `make check` and fails at deploy.**
Evidence: `verify_links` and the browser-HTML structural lint run only under
`verify`; `94ae83386` records a deploy refused for `catena/index.html: broken
local link: ../law/` because the directory existed in the working tree and not
in the committed tree; `fd833311e` records the same link surviving in six pages
an hour after being removed from one; `c8863b50a` records a Pages failure caused
by a research survey written where `source-library validate` forbids it, which
no local check caught. Mitigation: run `make public-preview &&
make verify-public-preview` locally before every push, and never link a page
whose files are untracked.

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
any added persistent vertical chrome on the two liturgy reading routes must be
re-measured at 393×852 and 320×852 and re-run through the roadmap's acceptance
capture matrix before it lands. If more chrome is genuinely required, that is a
vision amendment, not an implementation detail.

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
that left conflict markers in 14 paths. Mitigation: always
`git commit -- <paths>`; `make refresh-release-bindings ONLY="<paths>"`, never
`ADOPT=1` while others work.

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
figures in §6 before adopting it, and fix the cheaper problem first —
`day-reader.js:377-381`'s single `Promise.all`, which discards the early paint
`day.js` deliberately implements.

**R12. The 15-minute CI ceiling.** Evidence: five recorded Pages runs
(`31104342722`, `31106008011`, `31107294462`, `31110517661`, `31113461987`) built
and uploaded a verified artifact and then failed or were cancelled at
`deploy-pages` polling. Build plus verify already SHA-256 a 20,441-file artifact
at least three times and re-render 144 pages twice; per-page work added to
`wrap_in_layout` is paid twice. Mitigation: keep per-page shell work cheap, and
remember that a timed-out run is not a failed change — but also that it is not a
successful deployment and never supersedes an accepted parity run.

## 13. Open conflicts returned for disposition

The guidance-constraints lane catalogued these as C-numbers against its own
reading of the master plan. They are restated here self-containedly; a future
reader has no access to that lane's report. Each names the conflict, the
evidence on both sides, and the safer reading — but the disposition is the
coordinator's or the maintainer's, not this document's.

**C1 — The corpus redesign collides with an in-progress liturgy deliverable that
explicitly forecloses it and owns the same files.** The ledger entry
`liturgy-reader-live-ritual-flow-2026-08-07` is `in_progress` with all six
requirements `open`, and its evidence paths are `reader-shell.js` and
`reader-instrument.css`. `PROJECT-WORK.md:196` states that "Search, Study,
Compare, print redesign, **public-navigation redesign**, candidate/oracle
cleanup, source/translation/recension expansion, and a new visual direction
remain separate and unauthorized," and the roadmap adds that "public navigation
was not redesigned … their cleanup is deferred and unauthorized. No automatic
reader phase follows this closeout. Any future production reader work begins
from the live canonical pages under separate planning and authorization." The
governing rule is that an unmet requirement may not be weakened or deleted; it
is superseded by a new requirement or waived with both a `waiver_reason` and a
`waiver_authority`. Safer reading: the corpus redesign does not touch
`reader-shell.js`, `reader-instrument.css`, `liturgy/day.html` or
`liturgy/index.html`, and does not redesign public navigation, without explicit
user authorization recorded in the ledger. **This is the cleanest place for the
corpus lanes to be sequenced behind, or explicitly carved out of, the in-flight
deliverable, and it is the single decision that most affects §11's ordering.**

**C2 — Global search versus the measured 181-pixel first viewport.** The plan
puts a global corpus search or jump affordance on every non-PDF page, plus a
desktop command palette and a mobile full-screen search sheet. Against that: the
liturgy vision's invariant that the reader shell "never becomes permanent
dashboard chrome or consumes the reading surface"; the invariant that "the first
useful viewport contains real liturgical content on representative desktop and
mobile screens"; the rejected anti-pattern "permanent dashboard chrome around a
reading"; the accepted four-action bar with the statement that "Settings holds
infrequent configuration, not common navigation"; and the accepted behaviour
that only one modal surface may open at a time — a command palette would be a
fifth modal competing with Date/Browse, Contents, Mode and Details. The measured
stake: at 393×852 the accepted shell is 59 px and first liturgical content sits
at **181 px**, and removing one diagnostic row is what moved it from 255 px.
Note also that Propers search is an unstarted roadmap workstream with its own
gates. Safer reading: a site-wide search entry point on the liturgy routes
belongs in the site header, which is already a distinct landmark from the reader
shell; it must not join the four-action bar, must not become a second modal that
can coexist with an auxiliary surface, and must not preempt the Propers search
contract. Anything more is a vision amendment.

**C3 — The seven fixed portals versus a redesigned homepage.** The plan proposes
replacing the homepage with a map of the corpus organised by task — "Read
today", "Find a text", "Trace a source", "Follow commentary", "See what
changed", "Look up a canon" — with section and library discovery below. Against
that: `guidance/repository.md:299-312` states that `README.md` "is a terse
reader landing page and the section index," and that "the root landing tables
expose exactly seven reader portals, in this order and with these muted
liturgical-color identities: white Faith, gold Scripture, red Liturgy, green
History, violet Formation, rose Mary, and black Law," and further that "the root
tables do not promote a subsection already contained by a portal, a child
catalog, or an individual publication to a peer row." Mechanically, the homepage
is generated from `README.md` through `PAGE_MAP`, and `page_body_markdown`
(`:2056`) matches the exact three-line preamble `# Triptych` / tagline /
`## Library` — reword that preamble and the transform silently no-ops and the
page regains a duplicate title. Safer reading: task entrances are permissible
above or beside the seven-portal table, as a distinct block, provided the seven
keep their identity, order and colours and nothing is promoted to a peer row.
Restructuring the portal table itself is a `guidance/repository.md` amendment
and must be recorded there in the same commit.

**C4 — Standing commit and push authority in `AGENTS.md` is granted to Codex
sessions only.** The master plan assigns Claude the production implementation,
coding and test ownership, including lane M0, "integration / cutover … full
gates + Pages verification." But `AGENTS.md:77-83` grants standing authority to
create ordinary coherent commits and to push validated checkpoints to
`origin/main` to **direct Codex sessions**; `guidance/repository.md:273-283` and
`guidance/promised-deliverables.md:54-56` say the same. The word `claude` in
`repository.md:36` denotes a document provider branch, not a session authority.
And a push to `origin/main` *is* the deploy authorization. Safer reading: a
Claude implementation lane commits locally on its own branch and treats push,
`origin/main` integration, and any Pages-triggering action as requiring explicit
user authorization. Do not read a lane assignment in a plan as conferring the
standing authority a different document grants to a different agent.

**C5 — The plan never names `guidance/web-editions.md`, which owns exactly what
its long-form-reader lane would change.** That document requires: no second
editable copy of a publication's text; no content added and none silently
omitted, with any material omission declared in the record's rationale *and*
visibly in the edition; the rights colophon and the reader-facing revision
timestamp reproduced on the page a reader actually reaches, without which the
edition is not publishable; a `web-edition.toml` per leaf, so nothing defaults to
eligible by silence. Safer reading: treat it as controlling for that lane; a
long-form reader is a rendering change to the generator and the stylesheet,
never an edit of tracked `web/<provider>/*.md`; re-run
`make check-web-editions-current` after any converter touch.

**C6 — Durable knowledge in `build/agent-continuity/` contradicts
`guidance/repository.md`'s rule for `build/`, while being current practice.**
`repository.md:20-22` says `build/` "contains only ignored, reproducible
intermediates," and that anything required to understand, verify or reproduce a
publication belongs under `src/`. `.gitignore` contains `/build/`. Yet 1,415
files under `build/` are force-tracked, including
`build/agent-continuity/liturgy-reader-visual-plan.md`, which the roadmap calls
"the canonical acceptance and execution record" and which three ledger entries
name as `owner`. Safer reading: put durable corpus-redesign knowledge in tracked
guidance and `PROJECT-WORK.md` — the owners those documents intend — and use
`build/agent-continuity/` only as a working aid; or record the exception
explicitly in `guidance/repository.md` in the same commit that relies on it.

**C7 — The roadmap's milestone framing was overtaken by the cutover and never
reconciled.** `guidance/liturgy-browser-roadmap.md:376-381` says M1–M5 are
internal and "may not advertise an incomplete mode set," and that "M6 is the
first public reader release governed by the complete four-mode product
contract." The accepted public cutover at `9b5f21c0c` shipped the visual
foundation publicly with Read and Day Missal only; Study, Compare, Propers
Missal mode and search remain later boundaries. Safer reading: do not cite M6 as
a gate still ahead of the live reader; treat the live canonical readers as
production surfaces already governed by the vision invariants, with the missing
modes as advertised-coverage limits. The roadmap needs a reconciling row, and
only the coordinator may write it.

**C8 — Two screenshot matrices.** The plan suggests 1440×1000, 1024×768,
768×1024, 393×852, 320×800. The roadmap requires 1440×900, 1024×768, 768×1024,
393×852 and **exact 320 CSS-pixel reflow**, and the accepted evidence is
measured at 1440×900 and 320×852. Using the plan's figures produces evidence not
comparable with the accepted baselines. Safer reading: for any liturgy surface
the roadmap matrix governs; keeping one matrix site-wide avoids a second source
of truth.

**C9 — A faceted catalogue against "exactly one owning catalog; do not
cross-list."** `guidance/repository.md:306,373` gives each installed publication
exactly one owning catalog under `library/`, and `tools/public-alpha:236-239`
implements the counting so that "a Read link never adds or moves a publication's
one home." Safer reading: the faceted catalogue is a browser surface under
`src/web/browser/texts/`, not a `library/*.md` catalog page; it may surface Read
links and generated metadata freely but must not introduce a second `pdf/…` link
home for any leaf.

**C10 — Webfonts, icon libraries and non-HTML/CSS/JS assets cannot be shipped by
the current generator.** See §10. The accepted precedent is explicit: "the
candidate adds no framework, package, font, icon library, or build system," and
the Instrument mark is a three-stroke CSS mark. Safer reading: design to system
font stacks and CSS-drawn marks; a font is a generator change plus a bindings
refresh plus a rights record, as a separate authorized work unit.

**C11 — A generated search index is a new writer under `src/web/data/` and must
be recorded there.** `guidance/web-data.md:452-468` lists the ten writers and
says to check the directory listing against that block rather than the reverse,
because "a directory with no line here is a writer nobody recorded." Safer
reading: an index lane adds its writer line, registers the tool, adds the smoke
test, and proves additivity, all in the same commit.

**C12 — "Related corpus objects" mostly do not exist as structured edges.** See
§7. The plan is self-aware about this and assigns the verification to the
implementation lane. Safer reading: enumerate the existing edges before
designing the panel; any new edge type is a schema change under
`guidance/sources.md`, `guidance/catena.md` or `guidance/act-histories.md`.

**C13 — Rights progressive disclosure.** The plan proposes deferring
hash and legal detail so ordinary readers do not confront it first, and
separately rejects "weakening rights/provenance detail to make the interface
cleaner." Against the first: the acknowledgement rule at the point of use, the
vision's requirement that "rights status, required acknowledgement, withheld
text, and the reason for unavailability travel with the affected text," and the
rule that absence and its named reason survive the renderer. Safer reading:
progressive disclosure may defer hashes, artifact provenance and extended rights
apparatus; it may not defer a required licence acknowledgement, a withheld-text
reason, or a typed absence. Draw that line explicitly in whatever site-wide
vision is written.

**C14 — Creating new guidance without routing to it.** `AGENTS.md:24-27` says
the guidance family exists and "nothing else routes to them — read the one that
owns what you are about to touch, before touching it," and its routing table at
`:29-42` is how a later agent finds the owning document. Safer reading: a new
`guidance/corpus-browser-*.md` must include a routing row in `AGENTS.md` in the
same commit, or it is unreachable by the discipline the rest of the system
depends on.

**C15 — Local reading progress.** The plan proposes optional local-only reading
progress. The liturgy vision's non-goals exclude user accounts and offline
applications, and its precedence rule is that remembered preferences may not
override an explicit URL or turn an unsupported state into a supported one, and
that a link must work with storage unavailable. Safer reading: local-only
progress is not an account and is permissible, but it must be storage-optional,
must never outrank an explicit URL, and the capability should be stated in the
new site-wide vision rather than assumed. Note the existing precedent: only the
Propers controller persists anything (`propers-reader.js:206`, `:1105`, key
`triptych:liturgy:propers`); Day deliberately remembers nothing, and a harness
assertion locks that in.

**C16 — Worktree discipline.** The plan forbids git worktrees and requires
separate full checkouts; `guidance/repository.md:506-507` prefers `git worktree`
over stashing; `CONTRIBUTING.md:25` says the current checkout is the ordinary
workspace and an agent does not administer worktrees itself. No real
contradiction: the guidance advice is a stash alternative for one agent inside a
shared checkout, and the plan's rule is about parallel-lane isolation. Separate
full checkouts satisfy both. But separate checkouts do not remove the shared-index
hazard when two agents share one directory.

## 14. Coordinator dispositions, and what they settle

Section 13 listed sixteen conflicts and returned them for judgment. The
coordinator answered them on 2026-08-08 in the v2 master plan as amendments
D1–D20, and that review also disposed of the foundation lanes: A0, A1 and the
Claude reconnaissance accepted; A2 accepted with these amendments; A3 accepted
as foundation *direction* rather than pixel acceptance of any production route;
A4 accepted with bounded-Jump and protected-liturgy amendments; the neutral
static and browser gates accepted for integration.

Only the parts that bind implementation are restated here, because a decision a
future agent cannot find is a decision that will be re-litigated. The full text
lives in the master plan. Where an amendment closed a §13 conflict, the conflict
is named so nobody reopens it without new evidence.

| Closes | Amendment | What it binds in code |
| --- | --- | --- |
| C1, and §12 R1 | D2, D18 | `reader-shell.js`, `reader-instrument.css`, canonical `liturgy/day.html` and `liturgy/index.html` are a protected surface family until the Live Reader ritual-flow deliverable closes. No fifth primary action, no second modal owner, no literal corpus masthead above the reader, no print redesign, no site-wide Search in the reader shell. §11 step 6 — promoting `reader-shell.js` to `shared/` — is therefore **withdrawn, not deferred**: reuse its ideas, not the owned file. |
| C2 | D13 | Jump is a bounded fixture. Production search is J0→J1→J2 and no route may present a title fixture as global search. The 181-pixel first-viewport measurement stands as the constraint any later search entry point must respect. |
| C3 | D7 | The seven editorial portals keep their names, order and colour identities. Task entrances go beside or above them. Changing the portal table itself is a `guidance/repository.md` amendment in the same commit. The generator's `README.md` preamble transform must not be broken silently. |
| C4 | D19 | Claude may commit and push its assigned feature branches. Neither agent may merge or push `main`, or trigger public cutover. Never force-push. |
| C5 | D9 | `guidance/web-editions.md` is controlling for the publication Reader lane. No second editable copy of publication prose; no edit of `web/<provider>/*.md` for presentation; rights colophon and revision identity preserved; re-run the currency checks after any converter change. |
| C6 | D10 | Durable truth lives in the tracked guidance and ledger, not in `build/agent-continuity/*`. That directory may still carry handoffs, screenshots and temporary continuity, but no fact required by a future agent may live there alone. |
| C8 | D11 | One site-wide matrix: 1440×900, 1024×768, 768×1024, 393×852, 320×852 — plus 200% text, exact 320-pixel reflow, 400% where meaningful, keyboard-only, forced colors, reduced motion, print where not delegated to the PDF, no-JavaScript truth, and console/network/HTTP/accessible-name checks. No pixel-diff baseline before a real-data surface has independent visual acceptance. |
| C9 | D1, D8 | `/texts/` is labelled **Publications** and the route is not renamed. A faceted Publications surface is a discovery view; each publication keeps exactly one owning catalogue and one canonical PDF home. |
| C10 | D12 | No webfont, no icon library, no framework migration, no root-relative link, no new asset type the generator rejects. Design to system stacks and CSS-drawn marks. |
| C11 | D13 | A generated search index is a new writer under `src/web/data/` and carries its writer line, tool registration, smoke test and additivity proof in the same commit. |
| C12 | D14 | Only proven edges may be shown: containment, passage→artifact/segment, Catena fragment→Scripture locus, Catena passage→Source Library passage, act descent and change, document→catalogue page, Mass→propers→Scripture. `translation_of`, `used_by`, `derived_from`, canon correspondences and Law→Source citations are **not** to be synthesised. Each is a schema and generator work unit first. |
| C13 | D15 | Progressive disclosure may defer hashes, extended provenance, long rights apparatus and secondary metadata. It may never defer the licence acknowledgement at point of use, a withheld-text reason, a typed absence or unread or unsupported or invalid state, or the distinction between availability and redistribution. These must survive semantically, not merely as a colour or a class. |
| C15 | D16 | Local reading progress is deferred. If it returns it is storage-optional and an explicit URL always wins. Day keeps its deliberate no-memory behaviour. |
| C16 | D20 | Separate full checkouts, never worktrees, never two agents in one working directory. |
| — | D3 | "Independent treatment" is the human-facing label for separately produced provider treatments; "parallel treatment" is the relationship label when two are intentionally connected. Provider is always explicit metadata. Never call these Source Library editions unless they satisfy the edition model. |
| — | D5 | The token direction is accepted as roles, not frozen pixels. Type sizes, masthead density and spacing may move on real-data evidence. No production design may depend on a font being installed. |
| — | D6 | Top-level destinations: Publications, Sources, Scripture, Liturgy, History, Law, Commentary. The wordmark is a Home affordance. Density may collapse to a Menu earlier than any prototype suggests — but not by shrinking text. |
| C7, C14 | — | Still open. The roadmap's M6 framing was overtaken by the shipped cutover and needs a reconciling row, and a new `guidance/corpus-browser-*.md` family still needs its `AGENTS.md` routing rows. Both are writes to files this lane does not own; see §15. |

D17 restates this document's own findings as accepted engineering debt and adds
the instruction that matters most: fix them incrementally, with path-specific
commits and before-and-after gates. It is not authority for a browser-stack
rewrite, and §11's larger extractions stay proposals until a surface lane needs
them.

## 15. What this lane does not own

Two records that ought to carry part of the story cannot be written from here
without creating a second owner for one fact, which is exactly what D10
forbids.

`guidance/corpus-browser-roadmap.md` is the design lane's ledger and exists on
its branch, not on this one. Writing a second copy here would guarantee a
conflict at integration and leave two answers to the same question. The B0/B1
rows belong in that file, written once, by whoever holds the integration
branch. This lane supplies the row content in its handoff so that recording it
is a paste rather than a re-derivation.

The `AGENTS.md` routing rows for the full `guidance/corpus-browser-*` family
have the same shape of problem: this branch added the row for this document
alone, because it is the only one of the family that exists here. The remaining
rows land with the files they route to.

## 16. Two extractions, prepared and not landed

The hardening wave was told to prepare a reusable plan for shared accessibility
helpers and for the duplicated history/law utilities, and not to land either.
Both are recorded here at the point where the evidence was fresh, because a
plan derived once and then lost is a plan derived twice.

### 16.1 The act-record vocabulary is one vocabulary stored twice

`history.js` and `law.js` each carry their own `CITATION_WORDS`, `STATE_WORDS`
and `EDGE_WORDS` maps and their own `facts()`, `whatHappened()` and
`lineLabel()`. `magnitude()` exists only in history. These are not similar
functions that happen to resemble each other; they are the same act-record
vocabulary, copied.

The copy has already cost a reader something. At `af2c961`, law's
`CITATION_WORDS` holds four entries and history's holds three. The three they
share are byte-identical. History's is law's map minus `'none-claimed'`, and
because the gloss was missing, every station whose citation state is
`none-claimed` rendered a dangling em dash where the corpus had something to
say. That is the whole argument for the extraction, and it is worth more than
any appeal to tidiness: the duplication did not merely risk drift, it silently
dropped a term and shipped.

The extraction is one new `src/web/browser/shared/act-vocabulary.js` in the
UMD shape the tested models already use — `catena-model.js`, `catalogue-model.js`
and `reader-model.js` are the precedents, and all three are replayed under node
from Python tests. It exports the three maps and the four functions, with the
label differences between the two pages passed in as parameters rather than
branched on inside. Both pages then import it and delete their copies.

Why it is not landed here: it touches `law.js`, which no bounded hardening fix
otherwise needs, and it is a real refactor rather than a rename. D17 is explicit
that the findings are engineering debt to be paid incrementally with
path-specific commits, not licence for a browser-stack rewrite. It belongs to
whichever of `impl/history` or `impl/law` moves first, and that branch owns
both sides of it. Until then the equality of the two maps is held by a test, so
the specific failure that already happened cannot happen again.

### 16.2 The accessibility blocks that six instruments do not have

Measured at `af2c961`, counting `@media` blocks per stylesheet:

| Stylesheet | `forced-colors` | `prefers-reduced-motion` | `@media print` |
| --- | --: | --: | --: |
| `shared/browser-core.css` | 0 | 1 | 0 |
| `catena/catena.css` | 0 | 2 | 0 |
| `history/history.css` | 0 | 0 | 0 |
| `law/law.css` | 0 | 0 | 0 |
| `sources/sources.css` | 0 | 0 | 0 |
| `texts/texts.css` | 0 | 0 | 0 |
| `scripture/scripture.css` | 0 | 0 | 0 |

Every `forced-colors` block in the repository is in the liturgy files. Six
instruments have no high-contrast handling at all, and no instrument outside
liturgy has a print rule.

The fix is a token remap in `browser-core.css` under
`@media (forced-colors: active)`, modelled on the block in
`reader-instrument.css`, which is read-only to this lane but may be read. It
cannot regress liturgy, whose own block is more specific and wins. The
reduced-motion block in `browser-core.css` should absorb
`html { scroll-behavior: auto }` so the per-instrument copies can go, and a
shared `@media print` block should exist so that a page with no print opinion
still prints its content rather than its chrome.

Why it is not landed here: `browser-core.css` is one of the 53 files under
`src/web/browser/` bound by SHA-256 in `release/public-alpha.json`, it is
loaded by all fourteen browser pages, and a token remap is the kind of change
whose correctness is judged by looking at seven surfaces in forced-colors mode.
That is a visual acceptance, and no visual contract has been accepted. It
belongs to the shared-shell wave, where the same commit can carry the remap and
the evidence. The gate already exercises `forced-colors` at 393×852 on every
route, so the day someone lands it, the before-and-after is one command.

## 17. What lets the surface branches run at the same time

The next wave splits into `impl/library`, `impl/reader`, `impl/catena`,
`impl/sources`, `impl/history`, `impl/law`, `impl/scripture` and `impl/search`,
plus the sublanes `impl/browser-gates`, `impl/shell` and `impl/structural-fixes`.
Whether they can genuinely run in parallel is a property of the tree, not of the
plan, so it was measured.

### 17.1 The coupling is looser than the plan assumes

Every non-liturgy page loads exactly two things: `shared/browser-core.*` and the
files in its own entrance directory. There is no cross-entrance *asset*
reference anywhere. `browser-core.js` contains no header, navigation, footer,
masthead or breadcrumb construction at all — zero matches.

Two consequences follow, and both correct the plan.

**B0 does not block the six instrument lanes.** The shared shell is built at the
generator seam, not in `browser-core.js`, so nothing an instrument lane does to
its own directory waits on it. The plan's dependency column says otherwise.

**The unblocking that §11 step 6 promised never arrives, and was never needed.**
That step proposed promoting `reader-shell.js` into `shared/` and claimed it
would unblock lanes E, F, G, H and I. D2 withdrew the step, because the file
belongs to the liturgy deliverable. Those five lanes were not blocked in the
first place. Five are simultaneously parallel-safe today.

What *is* coupled across entrances is links, not assets: seven hand-written
footer link lists, no two alike, fifteen of the forty-nine possible edges
missing. Editing them does not conflict — they are in different files — but they
drift, which is what produced the missing edges. Replacing them with one
generated navigation is a single change touching all seven, and therefore
belongs to `impl/shell` alone and to no surface lane.

### 17.2 The files that actually conflict, in order

| Rank | Path | Why it conflicts | The discipline that fixes it |
| --- | --- | --- | --- |
| 1 | `release/public-alpha.json` | `rights_record_sha256` at line 22 is rewritten by every refresh. The hash rows are path-sorted and merge cleanly; that one line never does. | Treat as generated: regenerate, never merge. Better, move the derived line out of the merged record. |
| 2 | `release/rights/public-alpha-2026-07-15.md` | Moves in lockstep with the record above. | Same. |
| 3 | `tools/public-alpha` | Six branches need it, but only at three hot spots: the page-class map, the layout replacements, and the constants block. | Single owner: `impl/shell`. Surfaces register through an ordered list rather than editing the tool. |
| 4 | `release/public-alpha/assets/site.css` | 562 lines on all 144 pages, and it owns the section colours. | Per-kind stylesheet — blocked today by §17.3. |
| 5 | `Makefile` | `.PHONY`, `help` and `check` pack three or four target names per line, so two branches adding a gate collide on the same line. | One name per line. |
| 6 | `shared/browser-core.{css,js}` | 33 distinct `T.*` members used outside liturgy across 751 non-liturgy call sites. | Single owner, additive only. |
| 7 | `PROJECT-WORK.md`, `promised-deliverables.toml` | Both prepend, and the marker/id pairing binds them to each other. | Append at end, one subsection per lane. |

`src/web/browser/liturgy/**` — 27 files, 14,588 lines — belongs to no lane at
all under D2 and D18, and twelve of its paths are named as promised-deliverable
evidence, so they cannot even be moved.

One lane is misnamed. `impl/reader` owns no file under `src/web/browser/`; its
entire diff lands in `tools/public-alpha` and `site.css`. It is a foundation
lane wearing a surface lane's name, and scheduling it beside `impl/shell`
rather than beside the instrument lanes avoids a guaranteed collision on both
files.

### 17.3 The single change that would reduce future conflict most

A site-level asset is registered in six places: the layout marker, the
`wrap_in_layout` replacement key, the fixed-input path set, the copy tuple, the
expected-artifact list, and the static-source list. That is why nobody splits
`site.css`, and why every visual change to the home page, the long-form reader
and the shared chrome has to land in one 562-line file that four or five
branches want at once.

One `site_assets()` derived once and consumed by all six makes a per-kind
stylesheet a one-line change. It also closes a gap worth naming on its own: the
roughly forty browser CSS and JS files copied into the artifact are checked for
presence but never compared to their source, so a copy that silently diverged
would pass verification.

This is the derive-once rule in `guidance/the-shape.md` applied to the one place
the repository still restates a list six times. It is not a visual decision and
it needs no design contract.

### 17.4 Refreshing the release bindings without signing someone else's work

Fifty-three files under `src/web/browser/` are SHA-256-bound. The refresh is the
likeliest way two parallel branches corrupt each other, because an unfiltered
run signs whatever a sibling has mid-flight, and a signature means someone
reviewed those bytes.

The procedure: be the only agent in your own checkout; refresh immediately
before the landing commit, never mid-flight; confirm `git status --short` shows
only your paths; then

    make refresh-release-bindings ONLY="src/web/browser/<surface>"

`ONLY` alone cannot see a file you *added* or *deleted*, because the refresh
iterates the recorded set. Adding or removing a browser `.html`, `.css` or `.js`
needs `ADOPT=1 ONLY="…"` — and then an audit, because `ADOPT=1` will also adopt
a sibling's new files and retire paths they deleted.

Verify with `make check-release-bindings`, then `make public-preview` and
`make verify-public-preview`, which is the only place link verification runs.
Never use `ADOPT=1` without `ONLY`, and never run `approve-release`. On a merge
conflict in either record, take either side and re-run the filtered refresh: the
hash is a pure function of the tree, so the record is derived, not negotiated.

### 17.5 What each branch must run, and what is already red

`make check` takes about 310 seconds and is red at the base on
`check-tool-registry` and `check-examples`. `check-browser-gate` takes about 74
seconds and reports 1,583 passes against 146 failures on the three known publish
defects. Both rednesses are inherited.

The rule that follows is the one that matters for parallel work: **compare
failure sets, never exit codes.** Every branch here will see a non-zero exit
from gates it did not break, and a lane that reads exit status alone will either
panic or, worse, learn to ignore the gate.
