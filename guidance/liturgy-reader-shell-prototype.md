# Responsive liturgy reader-shell prototype decision record

## Status and boundary

Status: **M2 candidate pending external review**, measured 2026-08-04.

The candidate is an internal, unlinked, noindex route at
`src/web/browser/liturgy/prototypes/reader-shell/`. It does not alter the Day or
Propers production routes, add public URL keys or selector options, change
liturgical data, integrate the M1 modules into production, or implement the
later Missal, Study, Compare, search, and recension engines.

The shell consumes the existing generated preview corpus through
`browser-core.js` and its `renderProper` path. It validates M1 fixture records
with `reader-state.js`; fixture provenance is exposed only while entrance,
edition, date or formulary, Bible, and oration identity still match. A changed
selection keeps the real rendered text but suppresses the now-mismatched
fixture apparatus explicitly.

## Variants tested

Both variants use one DOM, state table, renderer adapter, Contents model, panel
manager, and mode control. Only deep-scroll reachability differs.

- **Persistent:** the four-action bar remains fixed at the viewport bottom.
  Every global action remains one activation away. It occupies 58–59 CSS
  pixels, including practical 56–58 pixel action targets.
- **Scroll-reveal:** the same bar recedes after downward reading and returns on
  upward scroll, keyboard focus, or the fixed 44-pixel `Reader actions`
  affordance. From a fully receded deep-scroll state, a reader using that
  affordance needs two activations to open a panel rather than one.

Reduced motion removes the transition. Both variants retain document padding,
safe-area offsets, focus visibility, and semantic scroll restoration.

## Measured behavior

The real-Chromium matrix covers 1440×900, 1024×768, 768×1024, 393×852, and
320×852, with persistent and reveal variants at the top, deep scroll, each
auxiliary surface, Propers, and unavailable coverage. Additional captures cover
postconciliar, Study, Browse, Compare, unresolved choice, bilingual, keyboard
focus, safe-area, reduced-motion, and print states.

| Viewport | Shell height | Reading width | Approx. characters/line | First liturgical content | Horizontal overflow |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1440×900 | 58 px | 571 px | 65 | 314 px | 0 px |
| 1024×768 | 58 px | 571 px | 65 | 313 px | 0 px |
| 768×1024 | 58 px | 571 px | 65 | 270 px | 0 px |
| 393×852 | 59 px | 361 px | 41 | 255 px | 0 px |
| 320×852 | 59 px | 288 px | 33 | 284 px | 0 px |

At 393×852 the celebration identity, quiet edition/date/coverage context, and
the beginning of the real Introit are all present before the first viewport
ends. At 320 CSS pixels every action remains inside the visual viewport; the
page has no horizontal scroll, bilingual and Compare units stack, and 200%
text enlargement retains all four action targets. The reading column does not
move horizontally during initialization. The final captured initialization
uses a hidden-until-resolved shell to avoid an avoidable loading-placeholder
layout shift.

At deep scroll, persistent takes one activation to reach any global surface.
Reveal returns automatically on upward scroll; through its always-present
affordance it takes one activation to restore the shell and a second to choose
an action. No variant requires returning to the document top.

## Auxiliary behavior

Contents is derived from the rendered semantic locations. Read exposes Proper
units; the long Missal shell adds prototype-labelled major divisions. It
tracks the current section, supports ordinary keyboard button navigation,
moves and focuses the selected heading, and restores the invoking control on
dismissal.

On wide desktop, Contents and Study occupy unused outer margins as slim modal
rails; they do not narrow the 68ch reading measure. They remain modal because
the accepted interaction requirement suppresses background interaction while
an auxiliary surface is open. On tablet and mobile, every auxiliary interface
uses the same native-dialog manager as a bottom sheet. Only one can open at a
time. Opening, Escape, close controls, selection, focus return, and scroll and
semantic-location restoration are asserted in Chromium.

Study is one surface for Why here, rubrics, calendar outcome, rank/precedence,
commemorations/displacements, provenance, rights/availability/typed coverage,
and historical links. It uses fixture-backed fields only where they are held;
unavailable fields and prototype-only layout material say so rather than
inventing a claim.

## Recommendation

Advance **the quiet persistent variant** as the M2 implementation direction,
subject to external review. Its measured 58–59 pixel cost preserves real text
in the first mobile viewport, does not alter the reading measure, and keeps all
four accepted actions one activation away at every semantic position. The
reveal behavior is reliable, but its minimal affordance saves little physical
height and makes a panel two activations away at deep scroll. That trade is not
justified by the measured result.

The scroll-reveal implementation should remain review evidence, not a
production preference or URL contract. A later integration may retest a hybrid
only if it preserves one-action access rather than merely changing the hiding
animation.

## Print and performance disposition

Print hides the prototype flag, action bar, reveal affordance, dialogs, and
error chrome. It retains celebration/formulary identity, date where applicable,
edition, explicitly selected universal locality, language/Ordinary context,
coverage, and liturgical sections without empty rail space. The representative
Letter PDF is four pages and tagged; every page is included in the review
raster/contact evidence.

The candidate adds no framework, package, font, icon library, or build system.
Raw prototype assets are approximately 56 KB JavaScript, 18 KB CSS, and 7 KB
HTML; gzip proxies are approximately 13 KB and 4 KB for JavaScript and CSS.
The default state makes 18 resource requests in the local review build, of
which four are prototype-specific (`reader-shell.js`, `reader-shell.css`, the
M1 fixture, and the M1 contract). Opening Study makes no additional request:
its DOM is built on demand from already validated state. Compare fixture
content is fetched only after a Compare URL or mode transition is requested.

## Intentionally deferred

- production use of M1 state/adapters or any new production URL key;
- the continuous Ordinary/Missal renderer and full Study apparatus model;
- semantic Compare correspondence and unresolved-choice resolution;
- Propers search/indexing and new recension or calendar/data coverage;
- final canonicalization of configuration, mode, and semantic-location URLs;
- nonmodal desktop Study behavior, which would conflict with the present
  modal-background requirement and needs a later explicit interaction choice;
- any public release, selector exposure, or claim that M2 is accepted.
