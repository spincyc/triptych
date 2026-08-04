# Responsive liturgy reader-shell prototype decision record

## Status and boundary

Status: **M2 accepted**, measured and externally accepted 2026-08-04. Candidate
`68becc59b396aca830c233b88ec74991563603d1` was reviewed through handoff
`20260804T101952Z-liturgy-reader-shell-prototype`; the *M2 prototype
changes-requested disposition* retained the quiet persistent direction and
requested three bounded corrections. Correction
`75234e72c402f0b25a681fbe074da70d895f7274` was reviewed through handoff
`20260804T142747Z-liturgy-reader-shell-corrections`; the *M2 responsive
reader-shell acceptance and closeout disposition* accepted the corrected M2
direction.

**Accepted — the quiet persistent reader shell is the M2 direction. Complete
Read states are free of diagnostic noise, all auxiliary surfaces reflow
without internal horizontal scrolling, and temporary Details is distinct from
wide-desktop pinned Study and mobile Study sheets. Production Day and Propers
routes remain unchanged.**

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
| 1440×900 | 58 px | 571 px | 65 | 240 px | 0 px |
| 1024×768 | 58 px | 571 px | 65 | 239 px | 0 px |
| 768×1024 | 58 px | 571 px | 65 | 196 px | 0 px |
| 393×852 | 59 px | 361 px | 41 | 181 px | 0 px |
| 320×852 | 59 px | 288 px | 33 | 228 px | 0 px |

At 393×852 the celebration identity, quiet edition/date context, and
the beginning of the real Introit are all present before the first viewport
ends. Removing the complete-state diagnostic row moved the first real Proper
from 255 to 181 pixels at 393×852 and from 284 to 228 pixels at 320×852,
without reserving an empty gap. Partial, unavailable, or mismatched states
retain a concise visible reliance notice. At 320 CSS pixels every action
remains inside the visual viewport; the
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

The fourth global action is **Details**, distinct from the Study mode. In Read,
Missal, and Compare, Details is a temporary modal inspection surface. In Study
mode on wide desktop, the same apparatus becomes a pinned, nonmodal right rail:
the 68ch reading measure does not move, the page remains focusable, selectable,
and scrollable, and the rail follows the current semantic location. Date or
Browse, Contents, and Mode remain temporary modal surfaces. On tablet and
mobile, Study uses the same reversible native-dialog sheet as Details because
there is insufficient width for simultaneous columns; closing it leaves Study
mode explicit and returns focus and semantic position.

Every surface and surface body was measured directly at 1440×900, 1024×768,
768×1024, 393×852, and 320×852, plus 200% text enlargement. Each reports
`scrollWidth <= clientWidth`. Forms use one shrinkable column, native controls
fill but do not exceed it, long Browse labels wrap, and Study renders labeled
fields, wrapping source identifiers, and compact coverage lists rather than raw
machine-shaped output. Only one modal surface can open at a time. Opening,
Escape, close controls, selection, focus return, and scroll and semantic-
location restoration are asserted in Chromium.

The Study apparatus is one structure for Why here, rubrics, calendar outcome,
rank/precedence, commemorations/displacements, provenance,
rights/availability/typed coverage, and historical links. It uses
fixture-backed fields only where they are held; unavailable fields and
prototype-only layout material say so rather than inventing a claim.

## Recommendation

Advance **the quiet persistent variant** as the accepted M2 implementation
direction. External review directed that scroll-reveal remain prototype
evidence. Its measured 58–59 pixel
cost preserves real text in the first mobile viewport, does not alter the
reading measure, and keeps all four accepted actions one activation away at
every semantic position. The
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
edition, universal locality, language/Ordinary context, any material coverage
limitation, and liturgical sections without empty rail space. Complete states
do not print an absence-of-problems notice or internal fixture terminology.
The representative Letter PDF is four pages and tagged; every page is included
in the review raster/contact evidence.

The candidate adds no framework, package, font, icon library, or build system.
Raw corrected prototype assets are approximately 60 KB JavaScript, 19 KB CSS,
and 7 KB HTML; gzip proxies are approximately 14 KB and 4.4 KB for JavaScript
and CSS.
The default state makes 18 resource requests in the local review build, of
which four are prototype-specific (`reader-shell.js`, `reader-shell.css`, the
M1 fixture, and the M1 contract). Opening the apparatus makes no additional
request: its DOM is built on demand from already validated state. Temporary
Details and pinned Study share that same structure. Compare fixture content is
fetched only after a Compare URL or mode transition is requested.

## Intentionally deferred

- production use of M1 state/adapters or any new production URL key;
- the continuous Ordinary/Missal renderer and full Study apparatus model;
- semantic Compare correspondence and unresolved-choice resolution;
- Propers search/indexing and new recension or calendar/data coverage;
- final canonicalization of configuration, mode, and semantic-location URLs;
- the production data and rendering contract for the pinned contextual Study
  rail beyond this fixture-backed shell behavior;
- any public release or selector exposure; M2 acceptance does not authorize
  production integration.
