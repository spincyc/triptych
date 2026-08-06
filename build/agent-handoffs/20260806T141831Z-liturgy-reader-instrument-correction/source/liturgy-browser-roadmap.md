# Dynamic Missal and Propers browser roadmap

## Status

This is the evolving execution record for the product governed by
[the liturgy-browser vision](liturgy-browser-vision.md). It records the current
baseline, gaps, parallel workstreams, dependencies, acceptance gates, and
progress. Update it when evidence or implementation changes. Do not weaken a
vision invariant here.

This roadmap does not authorize liturgical data, source acquisition,
publication, deployment, or release on its own. Each workstream remains subject
to the guidance that owns its data and artifacts.

## Current deployed baseline

Baseline date: **2026-08-03**. The unchanged production-browser and deployed
review baseline is `18256c51e72099b64bb1b9a6b17db9b6257e7ebf` (`Add Proper
placement notes`). The governing documents were committed at `bc7de4114`, the
external-review protocol at `4236f21bf`, and this execution record includes the
subsequent five-blocker correction disposition recorded in the progress ledger.

The current product has two public routes:

- `liturgy/day.html` resolves a civil date through generated calendar and
  rubrics data, then renders one or more readable formularies either directly
  or seated in a generated Ordinary.
- `liturgy/index.html` selects a missal, type, and formulary and renders its
  ordered Propers independently of a date.

The pages use generated manifests and structures for Bibles, calendars,
rubrics, Propers, and Ordinaries. `assembly-model.js` supplies shared calendar
resolution; `ordinary-seating.js` supplies shared seats and semantic Mass
events to browser and CLI paths; `browser-core.js` supplies shared text and
Proper rendering. The pages share the Reading Missal stylesheet and generated
Contents module, but retain separate HTML shells and orchestration scripts.

At this baseline:

- Day discovers public missals from the rubrics manifest, currently
  postconciliar and Roman 1962. The Propers manifest also exposes the
  calendar-independent `roman-pre-1955` formulary projection.
- A first Day visit uses today, the first repository-provided rubrics-manifest
  entry, the first Bible-manifest entry, Latin orations, Read-like
  Propers-only output, and visible-rubric state if the Ordinary is later
  enabled. A first Propers visit uses the manifest default and then the first
  available type and Mass. Neither route remembers preferences.
- URL hashes already carry most selection state, and a valid Propers deep link
  renders immediately. Existing hash semantics are a compatibility asset.
- Settings, Notices, and Contents are native, initially closed document-flow
  disclosures above the reading. Date navigation is inside Settings.
- Contents is generated from the rendered DOM. On Day with the Ordinary off it
  contains only `Beginning`; with the Ordinary on it lists Ordinary divisions
  and seated Propers. It does not track the current location.
- Day can render a complete semantic Mass event stream, display calendar
  resolution and source details, and add source-backed mechanical placement
  notes to seated Propers. These scholarly features do not yet share one
  interaction model and are not present consistently on Propers.
- Print removes interactive chrome and paginates the rendered reading, but it
  prints whatever apparatus and repeated unavailability material is present in
  the reading DOM rather than composing a deliberate print edition by mode.

This description is evidence, not a default contract. The intended defaults
are those in the vision.

## Deployed review, 2026-08-03

The retained Phase 4–9 reports, measurements, screenshots, and print artifacts
support review at 1440×900, 1024×768, 768×1024, and 393×852 across Settings,
Notices, Contents, Propers-only, Ordinary, Why, Roman 1962, postconciliar, and
print states. The retrospective external-review package contains no matching
320-pixel capture or measurement report and no artifact supporting the former
34-page current-print claim. Those exact figures are not treated as retained
baseline evidence; 320-pixel reflow remains a future acceptance gate.

Evidence-backed findings:

- The closed default reflowed at every width with no horizontal page scrolling.
- At 393×852 the Roman 1962 first view contained the celebration identity and
  real liturgical content.
- Opening Day Settings at 393×852 made the form consume most of the initial
  screen and turned common date movement into part of a large configuration
  task.
- Day Contents in Propers-only output contained one item, `Beginning`; it is not
  yet useful navigation for the default mode.
- Propers Contents correctly listed its eleven rendered semantic destinations,
  but it remained a document-flow list and did not report the current unit.
- Roman 1962 and postconciliar Ordinary states had no horizontal overflow, but
  repeated unavailable-text messages became more visually prominent than the
  liturgical hierarchy. The postconciliar populated Notices state also placed a
  large availability message before the reading.
- Retained Letter print was mechanically usable and removed chrome, but the
  screen DOM's repeated withheld-text and source-detail material still needs a
  mode-aware print hierarchy, not only print CSS hiding controls.

## Critical assessment

### Strengths that must not regress

- The celebration or formulary title is the dominant page identity.
- The default page is calm and text-led, with restrained controls and useful
  first view on desktop and mobile.
- The reading measure, line height, continuous vertical flow, responsive
  reflow, and current print legibility provide a strong foundation.
- Day derives calendar decisions from generated source-backed structures and
  preserves competing celebrations, dispositions, cycles, choices, and
  unresolved states.
- Shared event traversal and seating already give browser and CLI a semantic
  parity boundary.
- Propers and Day already share Proper rendering, Reading Missal vocabulary,
  and stable URL-driven selection.
- Missing, withheld, and unsupported text is explicit rather than silently
  replaced.
- Existing tests protect event order, rendered text, URL behavior, focus on
  Contents jumps, print hiding, duplicate IDs, console cleanliness, and
  horizontal overflow across representative widths.

### Problems the redesign must solve

Reading Missal v1 is a successful baseline, not the final product. Settings,
Notices, and Contents are currently document-flow disclosures rather than a
mature reader shell. Common date navigation should not remain buried in
Settings. Contents must become location-aware and responsive.

The current scholarly apparatus lacks one coherent interaction model. Calendar
resolution, source preambles, rubrical details, placement notes, availability
notices, How the Missal Changed, and the Source Library are separate surfaces
with different placement and discovery. The existing empty desktop scholarly
margin is useful space for a contextual Study rail, but only when the selected
unit has relevant material.

Large and repeated unavailable-text messages should not overwhelm the
liturgical hierarchy. They must remain explicit, source-specific, and
accessible while using summary-plus-claim-local markers where repetition adds
no new fact. Source honesty and explicit incompleteness outrank visual
smoothness.

Day and Propers must share components and modes without losing their distinct
purposes. Today they share lower-level helpers and styling but not one reader
state, shell, navigation model, apparatus model, or complete semantic rendering
pipeline. Advanced features must be discoverable without making the default
page resemble a dashboard.

Mobile is not a reduced desktop layout. It requires accessible sheets or
dialogs, stacked comparison and bilingual fragments, useful touch targets,
safe-area handling, and preserved reading position. Desktop side margins are
not a reason to compress mobile text or expand long forms above it.

No silent cross-recension or cross-locale fallback is acceptable. A route that
cannot satisfy the requested edition, locality, translation, cycle, alternative,
or Ordinary must refuse or mark partial coverage rather than choose a smoother
neighbor.

## Capability and coverage matrix

`Present` means a current public path carries the capability. `Partial` means
the data or behavior exists but coverage, consistency, or reader access is
incomplete. `Gap` means the shared reader does not yet provide it.

| Capability | Baseline | Required destination |
| --- | --- | --- |
| Civil-date navigation | Present inside Day Settings and keyboard/date controls | Primary Day action outside full Settings; remembered preference never replaces explicit date. |
| Temporal and sanctoral resolution | Present for public rubrics calendars | Preserve candidates, precedence, dispositions, omissions, and uncertainty in shared Study. |
| Dated recensions and effective ranges | Partial: recension projection exists; Day and Propers expose different sets | Edition-aware selection with explicit effective and coverage bounds in both entrances. |
| Territorial and local calendars | Partial in calendar structures and resolved branches; public coverage is narrow | Explicit user selection, no geolocation inference, stable URL state, and branch fixtures. |
| Rank, color, season, week, and cycle | Present in generated resolution; presentation varies | Shared identity summary and contextual Study details. |
| Competing celebrations and commemorations | Present in Day resolution; subordinate texts remain incomplete in some cases | Complete source-backed disposition and text ownership, or explicit partial status. |
| All readable formularies for a day | Present through the dynamic formulary selector | Primary, understandable access with each selection linkable and no hidden arbitrary choice. |
| Multiple Bible editions | Present | Shared selection and source/numbering labels in all modes. |
| Versification and psalter distinctions | Partial but source-modeled, with explicit refusal paths | Expose relevant distinction in Study and preserve identical browser/CLI resolution. |
| Original and translated Proper text | Present with uneven coverage | Bilingual fragment pairing, witness selection, rights, and per-unit availability. |
| Oration language and rights | Present with partial translations | Shared language/witness control and concise coverage summary without invented translations. |
| Ordinary language and variants | Present for generated inventories; many words are withheld or untranscribed | Honest edition-specific Missal rendering, point-of-choice options, and compact repeated-absence treatment. |
| Speaker, action, rubric, seat, and locus | Partial in Ordinary events and Day placement notes | One semantic hierarchy and Study apparatus across both entrances. |
| Source citations, witnesses, and pages | Partial across reading, preamble, and Source Library | Contextual source summaries with stable Source Library links and verified-locus status. |
| Calendar-decision explanations | Present on Day when Why is enabled | Study mode with a coherent disclosure and focus model. |
| Act and change histories | Present as a separate generated product | Contextual semantic links from Study and Compare; no duplicated history graph. |
| Recension comparison | Gap in the liturgy reader | Semantic-slot comparison with explicit additions, omissions, alternatives, sources, and act links. |
| Partial and unsupported coverage | Present but visually repetitive and not uniformly classified | First-class coverage states, concise summary, claim-local reason, and fail-closed selection. |
| Propers browse and search | Gap: nested selects and arbitrary initial formulary | Meaningful browse/search by structured fields, stable result URLs, and scoped no-result states. |
| Stable deep links | Present for current hash keys | Versioned, canonical semantic state with backward-compatible parsing. |
| Sharing | Partial: browser URL can be copied | Explicit share action, canonical URL, stable semantic anchors, and readable unfurl/title metadata. |
| Print and PDF | Present mechanically | Mode-aware, independently usable composition with required identity, rights, source, and coverage context. |
| Browser/generated-data/CLI/test parity | Strong partial foundation through assembly, seating, and event tests | One fixture contract covering identity, semantic events, text, source, options, and failure states. |

## Architectural gaps between Day and Propers

| Boundary | Current gap | Required boundary |
| --- | --- | --- |
| Reader state | Separate orchestration and different defaults | One validated semantic state model with entrance-specific required fields and URL serialization. |
| Object identity | Day begins with a resolved branch; Propers begins with nested list selection | One edition-qualified formulary identity, with optional date-resolution context. |
| Event rendering | Day can traverse a seated Mass; Propers renders an unseated Proper list | Shared semantic event/component renderer capable of direct Propers and continuous Missal views. |
| Shell | Repeated HTML disclosures and page-specific control grids | Shared responsive shell for primary actions, panels, focus, scroll restoration, status, and safe areas. |
| Modes | Feature toggles and page-specific apparatus | Explicit Read, Missal, Study, and Compare state with shared transitions. |
| Navigation | DOM-generated static buttons; default Day has only Beginning | Semantic, location-aware Contents generated from the object actually rendered. |
| Apparatus | Margins, preambles, details, notices, and placement notes are separate idioms | One contextual Study model linking decision, placement, provenance, rights, and history. |
| Discovery | Day date selector; Propers select cascade | Distinct date navigation and formulary browse/search feeding the same reader. |
| Coverage | Several free-form unavailable messages | Typed coverage result shared by rendering, search, URL validation, CLI, and tests. |
| Comparison | No shared comparator | Semantic-slot correspondence derived before visual layout. |

## Parallel workstreams

These workstreams proceed concurrently where their dependencies permit. They
are not new historical phase numbers.

### W1 — Shared reader and rendering foundation

- Define the edition-qualified liturgical object, entrance context, semantic
  event/slot contract, coverage result, and source hooks.
- Extract shared state validation, URL serialization, rendering components,
  status handling, and event traversal without changing liturgical resolution.
- Prove that current Day, Propers, and `mass-today --expanded` fixtures produce
  the same identity, order, text, variants, provenance keys, and absences.
- Encode entrance-specific Compare anchors and an explicit unresolved-choice
  result that cannot collapse to manifest or array order.
- Preserve additive generated data and lazy loading.

Dependencies: vision committed; existing assembly, seating, browser-core, and
generated schemas. W1 is the principal dependency for modes and comparison,
but shell prototypes may use adapters before extraction is complete.

### W2 — Responsive reader shell and navigation

- Prototype the four primary actions and quiet mode control at wide,
  intermediate, mobile, zoomed, and print widths.
- Move common Day navigation out of full Settings.
- Implement location-aware semantic Contents, optional wide navigation and
  Study rails, single-panel intermediate behavior, and mobile sheets/dialogs.
- Keep Date or Browse, Contents, Mode, and Details reliably revealable from a
  deeply scrolled semantic location without permanent dashboard chrome,
  reading-surface compression, or an obscured focused element.
- Preserve reading location and focus through open, close, rerender, route, and
  mode changes.

Dependencies: vision and representative fixtures. Can prototype in parallel
with W1; production integration depends on shared state and semantic locations.

### W3 — Read, Missal, Study, and Compare modes

- Make mode explicit, URL-addressable, and shared by Day and Propers.
- Retain Read's first-viewport and calm-reading baseline.
- Generalize continuous Ordinary seating for the shared Missal renderer.
- Consolidate decision, placement, source, rights, and coverage material in
  Study without duplicating source records.
- Build comparison from semantic correspondence before building parallel or
  stacked layouts.

Dependencies: W1 event/state contract; W2 shell interaction contract. Read and
Missal can stabilize before the full Study and Compare apparatus.

### W4 — Source and calendar apparatus

- Define contextual summaries and stable links for calendar reasons, rubrics,
  seats, witnesses, pages/loci, rights, availability, acts, and change history.
- Type absence and partial-coverage reasons instead of relying on repeated
  presentation strings.
- Keep unsafe reliance warnings visible while making repeated routine gaps
  compact and accessible.
- Confirm every exposed fact is carried by current generated data or add a
  source-owned schema change under the appropriate guidance.

Dependencies: W1 source and coverage hooks. Can inventory data gaps and design
the Study information model in parallel with W2.

### W5 — Propers browse and search

- Build a generated, additive search index over structured title, saint,
  incipit, season, type, citation, calendar use/date, and source identities.
- Give a new visitor a useful browse/search entry; preserve immediate rendering
  for valid deep links.
- Keep same-named edition objects distinct and expose coverage before opening.
- Link a formulary to supported Day occurrences without making one date its
  identity.

Dependencies: W1 identity and URL contract. Search-index work and prototype
research can proceed in parallel with shell work.

### W6 — Semantic comparison and historical-change integration

- Define correspondence keys for Ordinary divisions/elements, Proper slots,
  cycles, alternatives, and exceptional units.
- Define Day comparison around a fixed civil date and explicitly selected
  territorial context, with each recension resolving independently and
  calendar-result differences shown before semantic-unit correspondence.
- Define Propers comparison around corresponding edition-qualified formularies
  independently of a date; known calendar uses remain contextual links.
- Distinguish absence, unavailable text, differently seated material, and a
  genuine act-backed change.
- Link corresponding changes to How the Missal Changed and their source acts.
- Test parallel desktop and paired-stack mobile/bilingual presentations.

Dependencies: W1 semantic contract, W3 mode mechanics, W4 source/act hooks, and
at least two source-honest comparison fixtures. It must not wait for every
recension to be complete.

### W7 — Recension and territorial coverage

- Expand source-grounded formularies, dated recensions, effective ranges,
  territorial/local calendars, solved cases, and explicit partial boundaries.
- Maintain per-witness attestation, rights, calendar, Ordinary, browser, CLI,
  and test parity.
- Add no public selector whose label overstates its supported extent.
- Supply representative coverage fixtures to every other workstream.

Dependencies: source acquisition and the owning calendar/recension guidance,
not completion of the visual redesign.

**Historical Phase 10 placement.** Existing Phase 10 work on the Pius XII/1956
recension belongs in W7. Documentation stabilization through the vision and
this roadmap precedes further Phase 10 implementation; M0 and this correction
complete that documentation prerequisite once externally accepted. The
universal source model is:

```text
verified pre-1955 base text and structures
  + the official 1955 decree
  + applicable subsequent official decrees and authentic responses
  = a source-grounded 1956–1960 recension state
```

The Sacred Congregation of Rites' [*De rubricis ad simpliciorem formam
redigendis*](https://www.vatican.va/archive/aas/documents/AAS-47-1955-ocr.pdf),
23 March 1955, AAS 47 (1955), pp. 218–224, directs use of the liturgical books
as they then existed, applies its enumerated changes, leaves matters not
expressly named unchanged, takes effect 1 January 1956, and forbids publishers
to innovate meanwhile. [*Rubricarum
instructum*](https://www.vatican.va/content/john-xxiii/la/motu_proprio/documents/hf_j-xxiii_motu-proprio_19600725_rubricarum-instructum.html),
AAS 52 (1960), pp. 593–595, makes the new code obligatory on 1 January 1961 and
ends the 1955 decree's force that day.

After the official acts and inherited base material for a narrow slice are
verified, W7 may build an internal, typed-partial-coverage vertical slice in
parallel with W1 and W2. The verified but inaccessible 1956 Benziger printing
remains a valuable validation witness for publisher arrangement and American
or local supplements; it is not a universal implementation prerequisite. The
whole visual redesign is likewise not a prerequisite. Recension work must obey
the vision's partial-coverage, fail-closed source honesty, stable identity, and
shared-rendering rules, and the state remains absent from the ordinary public
selector until advertised coverage, Ordinary extent, locality, rights, and
tests are honest.

### W8 — Accessibility, performance, and print

- Establish automated and manual accessibility baselines for both entrances
  and all mode transitions.
- Measure route data, parse/render cost, LCP candidates, interaction latency,
  and layout shifts; set budgets before production shell integration.
- Build mode-aware print composition and independently usable PDF review.
- Exercise reduced motion, forced colors, safe areas, zoom, text enlargement,
  screen readers, keyboard, touch, and slow-device/network conditions.

Dependencies: begins with baseline measurement immediately; every workstream
must meet its gates continuously rather than defer them to release.

### W9 — Migration, regression, and release verification

- Preserve and test legacy Day and Propers hashes while introducing canonical
  shared state.
- Maintain versioned fixtures, screenshot baselines, semantic parity hashes,
  console/network checks, and release bindings.
- Prepare and record the external-review package required for each major visual
  milestone before acceptance.
- Verify public-preview and public-site artifacts, links, source bindings,
  rights, and exact deployed SHA before release.
- Stage rollouts so a new shell or mode can be disabled without changing
  liturgical data or invalidating links.

Dependencies: continuous. A release checkpoint integrates completed slices
from the other workstreams; it does not wait for unrelated coverage expansion.

## Integration milestones and dependencies

Milestones are cross-workstream checkpoints, not sequential development lanes
and not replacements for historical phases.

M1–M5 are internal integration milestones. They may be privately previewed and
externally reviewed, but they are not public releases and may not advertise an
incomplete mode set. The existing public reader and every currently supported
function remain intact while those milestones develop behind fixtures or a
reversible preview boundary. M6 is the first public reader release governed by
the complete four-mode product contract and all world-class gates.

| Milestone | Integrated result | Required inputs |
| --- | --- | --- |
| M0 — Governing contract | Vision, roadmap, routing, baseline evidence, correction disposition, and no production change | `bc7de4114`, `4236f21bf`, retrospective review, this correction commit, and its external acceptance |
| M1 — Semantic parity contract | Versioned fixture schema and shared identity/event/source/coverage assertions for existing Day, Propers, and CLI | W1, W4, W9 |
| M2 — Shell prototype decision | Tested wide/intermediate/mobile/zoom/print prototypes; bounded choices resolved; no liturgical data change | W2, W8, representative W9 fixtures |
| M3 — Shared Read and Missal slice | Both entrances use shared state, semantic renderer, navigation, and Read/Missal modes for Roman 1962 and postconciliar fixtures | W1, W2, first half of W3, W8, W9 |
| M4 — Study, discovery, and coverage slice | Shared Study apparatus, compact typed coverage, Propers browse/search, source/history links | W3, W4, W5, W8, W9 |
| M5 — Compare slice | Semantic recension/translation/cycle/alternative comparison in parallel and stacked forms | W3, W4, W6, qualifying W7 fixtures, W8, W9 |
| M6 — Release-quality reader | All world-class gates pass for the advertised coverage; compatible URLs and independently usable print ship | All applicable workstreams |

Phase 10 may advance official-act collation, inherited-base verification, and
exact-printing validation after the corrected M0 contract is externally
accepted. It may produce a narrow internal typed-partial-coverage fixture after
its own source gates and does not depend on M2–M6. A public 1956–1960 recension
selector depends on its complete advertised coverage and release gates, not on
an inaccessible printing alone or merely on the first reader redesign release.

## External-review handoff gate

Before M2, or any M3–M6 checkpoint containing browser-visible change, is marked
accepted, create and externally review the unique package required by the
[external-review handoff protocol](external-review-handoffs.md). Its screenshot
set follows this roadmap's required routes, states, and viewports; its review
request identifies the precise blocking acceptance judgments. Record the
handoff basename, reviewer disposition, and resolution of every blocker in the
progress ledger or owning tracked acceptance record. Creating the package alone
does not satisfy the gate.

## Acceptance gates

Every implementation slice passes the gates for the capabilities it affects.
M1–M5 remain internal and do not fail merely because a later mode is not yet
integrated; they preserve every current public function and do not advertise
the incomplete product. M6 passes the complete product contract and all gates
before public release. “No change” to liturgical data is proved by semantic
fixture parity, not assumed from a visual diff.

### Product and semantic gates

- Day and Propers identify and render the same edition-qualified formulary and
  semantic units consistently.
- Read, Missal, Study, and Compare are each one clear action away on both
  entrances, with Read initially active and visually dominant.
- At every semantic reading location, Date or Browse, Contents, Mode, and Study
  are reachable without returning to the document beginning or losing that
  location.
- Today and real text appear immediately in a first Day visit; a valid Propers
  deep link renders immediately; a new Propers visit opens browse/search.
- Date navigation is available outside full Settings.
- Contents reports the current semantic unit and only actual destinations.
- Position and focus survive auxiliary panels, supported state changes, and
  mode transitions according to a documented rule.
- No unsupported selection falls through to another recension, locality,
  translation, cycle, alternative, formulary, or Ordinary.
- No coequal unresolved authorized option is selected by manifest or array
  order; the choice appears at its semantic point.

### Source, data, and parity gates

- Every rendered unit and decision carries stable source/provenance and typed
  coverage data adequate for Study and tests.
- Browser, generated data, CLI, and tests agree on identity, selected branches,
  event order, text, sources, rights state, and explicit absence.
- Search results and deep links resolve the same stable formulary identities as
  the generator.
- Day comparison holds date and territorial context fixed, resolves each
  recension independently, exposes calendar-result differences first, and then
  aligns semantic units. Propers comparison aligns corresponding
  edition-qualified formularies without introducing a date. Both leave
  one-sided units explicit.
- Source, calendar, recension, versification, rights, and release checks owned
  by affected guidance pass.

### Responsive and visual gates

- The default 1440×900 and 393×852 first views show identity and real text.
- 1024×768 and 768×1024 use one reading column and at most one auxiliary panel.
- No horizontal page scroll or lost functionality occurs at 320 CSS pixels,
  400% zoom, or 200% text enlargement.
- Wide rails never compress the reading below its usable measure and are absent
  or empty when irrelevant.
- Deep-scroll access to the four primary actions is reliably revealable without
  permanent dashboard chrome, reading-surface compression, or covered focused
  content at every supported width.
- Mobile sheets/dialogs preserve safe areas, focused controls, and reading
  location. Compare and bilingual fragments stack by corresponding unit.
- Missing-text treatment is unmistakable but subordinate to the celebration
  and available liturgical text.

### Accessibility gates

- WCAG 2.2 AA automated checks report no applicable violations, followed by
  manual review of structure, language changes, contrast, focus order,
  focus-not-obscured, names/roles/states, status announcements, and reflow.
- Every core path is complete with keyboard alone and with touch alone.
- Keyboard, touch, and screen-reader runs prove that the four primary actions
  can be revealed and dismissed from a deeply scrolled location with focus and
  semantic location preserved.
- Disclosures, sheets, and dialogs follow the applicable WAI pattern, including
  expanded state, Escape behavior, focus containment where modal, and focus
  restoration.
- Representative screen-reader runs cover Day selection, Propers search,
  Contents navigation, every mode, options, coverage warnings, comparison, and
  print access.
- Forced colors and reduced motion retain meaning and operation.

### Performance gates

- Field data, when sufficient, meets the current good Core Web Vitals at the
  75th percentile separately for mobile and desktop: LCP ≤2.5 s, INP ≤200 ms,
  CLS ≤0.1.
- Reproducible lab tests enforce the same direction before field data exists,
  including throttled mobile and warm/cold-cache deep links.
- Route-specific transfer, request-count, main-thread, and rendered-DOM budgets
  are recorded at M2 and enforced thereafter.
- Read does not fetch the Ordinary, comparison peers, or full Study/source
  records until needed. Valid deep links do not incur an arbitrary-formulary
  render first.

### Print, URL, and release gates

- Print hides all interactive chrome and preserves independent edition, date or
  formulary, locality, language, cycle/alternative, source, rights, and coverage
  context.
- Print review includes text extraction and visual inspection of every page for
  representative short, long, bilingual, partial, and comparison cases.
- Canonical URLs reproduce semantic state in a storage-free session. Legacy
  URLs pass compatibility fixtures and canonicalization changes no selection.
- Public-preview and public-site builds, link/fragment verification, release
  bindings, console/network review, and exact deployed-SHA verification pass.

## Visual-regression strategy

The visual suite is fixture-driven. It never changes production data merely to
manufacture a screenshot state. A state absent from public data uses a lawful,
explicit test fixture that exercises the same renderer and declares that it is
not public coverage.

Every release candidate captures at least:

- 1440×900, 1024×768, 768×1024, 393×852, and exact 320 CSS-pixel reflow;
- Day and Propers with the reader shell closed;
- each route deeply scrolled, with the four primary actions revealed and
  dismissed while asserting semantic location, focus, and unobscured content;
- each auxiliary surface open, one at a time, with focus and scroll assertions;
- Read, Missal, Study, and Compare;
- Roman 1962 and postconciliar;
- a pre-1955 or other qualifying comparison state;
- a Day comparison whose recensions resolve the fixed date to different
  celebrations, a date-independent Propers comparison of corresponding
  formularies, and a coequal unresolved option that requires user choice;
- Ordinary off and on; Why/rubrics closed and open;
- bilingual paired and stacked text;
- populated routine Notice, immediate-reliance warning, partial recension,
  unsupported date, unavailable translation, missing Ordinary, competing
  celebration, commemoration, cycle, alternative, local calendar, and
  territorial branch;
- light/dark only if both are actually supported, plus forced colors and reduced
  motion regardless; and
- screen and print/PDF output.

Pixel diffs protect composition and regressions but do not approve correctness.
Each fixture also asserts title, semantic unit IDs and order, accessible names
and states, focus target, scroll position rule, URL, overflow, console/network
errors, and source/coverage identity. Reviewers inspect the first viewport and
every printed page rather than accepting a contact sheet alone.

## URL and compatibility migration

1. Inventory every current Day and Propers hash key and add it to permanent
   compatibility fixtures before changing parsing.
2. Define one shared semantic state schema with entrance-specific requirements.
   Keep route identity explicit; do not make a missing date distinguish Day from
   Propers by accident.
3. Parse legacy hashes into that state, validate against generated manifests,
   and serialize one canonical URL. Invalid requested values produce an
   explicit unsupported state, not a default substitution.
4. Introduce additive keys for mode, locality, semantic location, comparison
   dimension and sides, and any newly linkable option. Do not reuse an old key
   with changed meaning.
5. Keep old links working through parsing or a documented redirect for at least
   the supported life of the published corpus. Preserve unrecognized keys while
   a compatible older client may own them only when doing so is safe.
6. Test URL precedence over remembered preferences and storage-free behavior.
7. Update share metadata and canonical links only after semantic-state fixtures
   pass on the deployed artifact.

The exact spelling of new keys and whether canonical state remains in the hash
or moves partly to query/path is an M1 prototype decision. Compatibility,
explicit entrance identity, and reproducibility are not open decisions.

## Print and sharing strategy

Print is generated from the same semantic object and selected mode, with a
print-specific composition layer. Read print emphasizes appointed text; Missal
print preserves the continuous order; Study print includes only explicitly
selected apparatus or a concise appendix; Compare print preserves paired
semantic units and clear edition headings. Interactive open/closed state alone
must not accidentally determine whether essential print context exists.

The Share action copies a canonical semantic URL and provides a descriptive
title naming the celebration or formulary and edition. Day shares include the
date and locality; Propers shares do not invent a date. Compare shares name the
dimension and both sides. Sharing never embeds unpublished text or bypasses a
rights restriction.

## Data and rendering parity

One fixture record must be sufficient to ask all consumers the same questions:

| Assertion | Browser | Generated data | CLI | Tests |
| --- | --- | --- | --- | --- |
| Object and edition identity | Visible title/meta and URL | Stable keys/manifests | Named result | Exact equality |
| Calendar result and branch | Day Study | Calendar/rubrics result | `mass-today` | Solved case |
| Semantic event and seat order | Read/Missal/Contents | Proper/Ordinary structures | Expanded event stream | Ordered IDs/hash |
| Text, language, cycle, alternative | Rendered fragment | Source fragment and selection | Printed/structured output | Exact text/selection |
| Source, witness, locus, rights | Study/link/print context | Source identities and coverage | Structured detail | Join and refusal assertions |
| Missing or unsupported material | Typed summary and claim marker | Typed coverage result | Explicit refusal | No-fallback assertion |

Presentation-only adapters may differ. No consumer may re-derive a liturgical
choice, reparse translated labels to find a slot, or manufacture a source fact.

## Coverage and recension expansion

Coverage work is incremental and may ship independently when its advertised
boundary is complete and honest. Each increment names the exact dated book or
act state, locality, calendar span, supported formularies, Ordinary extent,
translations, rights, and unresolved material. Public discovery must not imply
more.

Representative regression coverage eventually includes Roman 1962,
postconciliar, pre-1955, the source-grounded 1956–1960 middle state when
available, territorial/local overlays, cycles, alternatives, commemorations,
competing celebrations, resumed Sundays, partial recensions, unsupported dates,
and exceptional rites that do not fit an ordinary Mass frame.

The Phase 10.1 ordinary-Sunday vertical slice remains a useful internal parity
target after the official acts and the inherited pre-1955 base text and
structures required for that slice are verified. Applicable later official
decrees and authentic responses must also be collated. The slice may then use
an internal stable identity, source registration, and typed partial-coverage
boundary without claiming a complete printed edition. It uses the shared
renderer rather than edition-specific UI.

Inspection of the selected 1956 Benziger printing proceeds in parallel as
validation of arrangement, local supplements, Ordinary loci, and witness-level
text. It remains necessary for claims about that printing and any American or
local coverage, but not for universal changes already established by the
official acts and inherited base. No ordinary public selector appears until the
advertised calendar span, formularies, Ordinary extent, locality, rights, and
tests are complete and explicit.

## Current next action

The M0 documentation and correction gate passed external review on 2026-08-03.
The accepted implementation boundary now starts these independent actions in
parallel:

Independent visual review selected **Liturgical Instrument** as the production
visual foundation. Quiet Folio and Contemporary Reader remain frozen comparison
references rather than ingredients for a compromise or a new direction. The
selection does not revoke M1–M3 or W3 semantic, state, renderer, seating,
one-action access, focus, reflow, fail-closed, source-honesty, or
production-isolation acceptance, and it does not authorize public cutover.

The selected foundation completed the first evidence phase of its bounded
visual-correction pass. Work units A–C supply an integrated control shell,
earlier Missal text, one controlled Read axis, subordinate partial-coverage
treatment, an authored masthead, and finished mobile ritual spacing and
division wrapping. Work unit D supplies full-matrix inspection, governed-check
dispositions, successful Pages verification, and the immutable handoff at
`build/agent-handoffs/20260806T112813Z-liturgy-reader-instrument-correction/`.
Independent review round 1 confirmed six original findings and retained only
the floating 1024-pixel shell plus its related 200%-text label fragmentation.
The narrow follow-up now transitions directly from the accepted 72rem rail to
an opaque square edge dock, with a root-font-aware labeled 2×2 extreme-reflow
state. Its 54-capture run passes 15/15 assertions; a new immutable handoff and
independent re-review remain. Production-integration planning may proceed, but
execution remains deferred until that review passes. The canonical correction
plan and reviewer mailbox are tracked at
`build/agent-continuity/liturgy-reader-visual-plan.md`.

1. M1's W1/W9 shared semantic fixture and URL-state contract is accepted at
   correction `c6b8070ae76e75153448895a19a0b916c18806ea` plus final micro-fix
   `c1a590f5854215d68d167d9040e188f41762663e`. Any production integration or
   further W1/W9 slice requires separate scope.
2. W2 and M2 are **accepted** at corrected implementation
   `75234e72c402f0b25a681fbe074da70d895f7274`. The quiet persistent shell is
   the direction for Date or Browse, Contents, Mode, and Details. Complete Read
   states omit diagnostic noise; every auxiliary surface reflows without
   internal horizontal scrolling; temporary Details is distinct from pinned
   nonmodal wide-desktop Study and reversible tablet/mobile Study sheets. The
   internal noindex prototype remains evidence, including its non-preferred
   scroll-reveal variant. The measured decision record is
   [the reader-shell prototype record](liturgy-reader-shell-prototype.md).
   W3 now has one reversible, unlinked Day Read-mode integration candidate at
   `liturgy/day-reader.html`. The reusable shell owns interaction only; the Day
   adapter crosses the accepted M1 boundary and reuses production assembly,
   fragment fetching, and Proper rendering. Supported legacy state retains its
   meaning, later-mode state is handed intact to the unchanged live route, and
   invalid explicit state fails closed. It does not replace or alter the live
   Day route. External review accepted the architecture and requested bounded
   legacy-state, transition-clearing, weekday, and human-facing Details
   corrections. Those corrections are represented in the compact handoff
   `20260804T173010Z-day-reader-shell-integration-corrections`. M3 is accepted
   after final micro-fix `c604edb8a1fffb1e5c0981798800ecb801258e7c` made the
   existing render serial authoritative across delayed success and failure
   paths. Deterministic Chromium races prove that a superseded valid or failed
   request cannot replace a newer valid or invalid result, including during
   Back navigation. Live Day and Propers remain unchanged; Propers integration,
   later modes, public navigation and cutover, and recension work remain
   outside that accepted Day slice. A second W3 entrance now enters the same
   shell at `liturgy/propers-reader.html`: it
   selects a formulary without a civil date, crosses the accepted M1 Propers
   adapter, and reuses the production Proper renderer. Its Browse, cycle and
   alternative, transition, responsive, accessibility, and print evidence is
   externally accepted after the bounded correction at
   `1e4587dfe04a11c18e996a16f7fbbdb54bc744a4`. It does not reopen the accepted
   Day slice or start public cutover, later modes, search, or recension work.
   The distinct **Day Missal-mode integration** is now accepted at
   `86a9816c1bffdcbdd09469f5f8d005c666a8045e`. It extends only the existing
   unlinked Day candidate: `ordinary=1` renders the production Ordinary through
   the production renderer and M1 assembly/seating event stream, while
   `ordinary=0` retains Read and valid latent Ordinary preferences. Settled
   Chromium evidence proves deterministic outcome chrome, semantic location,
   inline Eucharistic Prayer focus, render ownership, and neutral duplicate-key
   rejection without changing the accepted M3 record, accepted Propers Read
   entrance, or any public route. Study, Compare, Propers Missal mode, search,
   cutover, and recension coverage remain later boundaries.
3. W7 verifies the pre-1955 base and official acts for the narrow Phase 10
   slice, while exact-printing acquisition continues in parallel as validation
   rather than a universal prerequisite.

No prototype chooses liturgical defaults or creates data to fill a review
state. M1–M5 remain internal; M6 is the first public redesigned reader release.

## Progress ledger

Historical phase names and numbering are preserved. Rows that produced no
tracked commit say so rather than borrowing a neighboring SHA.

| Date | Historical work | Result | Commit reference |
| --- | --- | --- | --- |
| 2026-08-02 | Phase 4, Step 1 — continuous missal presentation | Added the continuous reading surface and retained rendered text parity. | `c767c5374` |
| 2026-08-02 | Phase 4, Steps 2–4 — refinement and scholarly margin studies | Established measure, responsive behavior, and optional empty desktop margin through local review; later retained in the Reading Missal direction. | No separate tracked commit; reviewed against `c767c5374` |
| 2026-08-02 | Phase 5, Step 1 — annotation experiment | Tested contextual notes and deliberately left the placeholder experiment uncommitted. | No tracked commit |
| 2026-08-02 | Phase 6, Step 1 — Reading Missal v1 | Made Day reading-first with dominant title and closed Settings/Notices while preserving event and text parity. | `6a68536d7` |
| 2026-08-03 | Phase 7, Step 1 — reading-first formulary page | Brought Propers into the Reading Missal visual language without merging route purposes. | `fdd88fb67` |
| 2026-08-03 | Phase 8, Step 1 — generated Mass Contents | Added shared DOM-derived Contents and completed its route integrations and tests. | `febaa92d0`, `719e975d1` |
| 2026-08-03 | Phase 9, Step 1 — Proper placement notes | Added source-bounded mechanical placement notes to supported seated Propers on Day. | `18256c51e` |
| 2026-08-03 | Phase 10, Step 1 — Roman 1955 vertical-slice assessment | At that step, recommended an exact-edition, source-bounded 1956–1960 slice and found source and precedence blockers; later external review corrected the exact-printing prerequisite. | No tracked change; review baseline `18256c51e` |
| 2026-08-03 | Phase 10, Step 2 — source acquisition | Identified the 1956 Benziger edition and institutional copies as a verified but inaccessible validation witness; later external review removed it as a universal prerequisite while preserving its witness/locality value. | No tracked change; review baseline `18256c51e` |
| 2026-08-03 | M0 — browser vision and roadmap stabilization | Established the governing destination, parallel workstreams, gates, and routing without production changes. | `bc7de4114a279ea780d5b15bdaee0a7414e07078` |
| 2026-08-03 | External-review handoff protocol | Established the immutable ignored review-package contract and major-visual-milestone gate. | `4236f21bfe5aa6f3dde76ee0b9398823373f22e3` |
| 2026-08-03 | M0 retrospective external review | Accepted the governing foundation and requested five narrow corrections: persistent action reachability, entrance-specific Compare anchors and coequal choice handling, the official-act Phase 10 model, a current execution record, and internal-versus-public milestone scope. | Handoff `20260803T155820Z-liturgy-browser-vision-retrospective`; reviewed through `4236f21bfe5aa6f3dde76ee0b9398823373f22e3` |
| 2026-08-03 | M0 external-review corrections | Resolves the five blockers without production or recension implementation; the exact SHA is recorded in the completion report and correction handoff because a commit cannot contain its own hash. | This correction commit |
| 2026-08-03 | M0 correction external acceptance | Accepted — all five blockers resolved. The governing contract is stable, and W1/W9, W2, and W7 may begin in parallel at their recorded boundaries. | Reviewed commit `aad3691ee67106f6ff2cdb639463248ff35e3594`; handoff `20260803T164600Z-liturgy-browser-vision-corrections`; review result `20260803T171758Z-liturgy-browser-vision-corrections-review-result.md` |
| 2026-08-03 | M1 — semantic parity contract external acceptance | Accepted — cycle alternatives are preserved, v1 property-presence validation is complete, the focused suite passed all 38 tests, and the deployed Day and Propers routes still load neither M1 module. The full gate remains red only at the separately approved example baseline and its authorized completion-count update. | Implementation `259573d393cd6a6bac09fc751ac1d14ec9477853`; reviewed correction `c6b8070ae76e75153448895a19a0b916c18806ea`; final micro-fix `c1a590f5854215d68d167d9040e188f41762663e`; handoffs `20260803T223346Z-liturgy-reader-state-contract` and `20260803T235342Z-liturgy-reader-state-contract-corrections`; external review dispositions *M1 liturgy reader-state contract*, *M1 reader-state corrections*, and *M1 acceptance closeout count delta* |
| 2026-08-04 | M2 candidate — responsive reader-shell prototype | Candidate pending external review. One internal noindex shell serves Day and Propers, reuses the Proper renderer and validated M1 fixtures, and tests persistent/reveal reachability, semantic Contents, coherent Study, representative mode shells, responsive sheets/rails, and print without production-route or liturgical-data integration. | This candidate commit; decision record `guidance/liturgy-reader-shell-prototype.md`; handoff `20260804T101952Z-liturgy-reader-shell-prototype` |
| 2026-08-04 | M2 candidate external-review corrections | External review accepted persistent reachability and requested three bounded corrections. The corrected candidate removes complete-state diagnostic noise, directly proves every auxiliary surface has no internal horizontal overflow including at 200% text, renames temporary Study access to Details, and gives Study mode a nonmodal pinned wide-desktop rail while retaining a reversible mobile sheet. M2 remains pending correction re-review. | This correction commit; compact correction handoff recorded in the completion report |
| 2026-08-04 | M2 — responsive reader-shell external acceptance | Accepted — the quiet persistent reader shell is the M2 direction. Complete Read states are free of diagnostic noise, all auxiliary surfaces reflow without internal horizontal scrolling, and temporary Details is distinct from wide-desktop pinned Study and mobile Study sheets. Production Day and Propers routes remain unchanged. | Candidate `68becc59b396aca830c233b88ec74991563603d1`; correction `75234e72c402f0b25a681fbe074da70d895f7274`; handoffs `20260804T101952Z-liturgy-reader-shell-prototype` and `20260804T142747Z-liturgy-reader-shell-corrections`; external review results *M2 prototype changes-requested disposition* and *M2 responsive reader-shell acceptance and closeout disposition* |
| 2026-08-04 | M3 candidate — production reader-shell foundation and Day Read integration | Candidate pending external review. The bounded noindex route extracts only the accepted persistent shell; integrates real Day Read output through production assembly, the accepted M1 adapter, shared fragment fetching, and the shared Proper renderer; preserves supported and deferred legacy state without fallback; and passes measured desktop, tablet, mobile, zoom, accessibility, print, and live-route isolation checks. | This candidate commit; handoff `20260804T154620Z-day-reader-shell-integration` |
| 2026-08-04 | M3 candidate external-review corrections | External review accepted the reusable-shell architecture and requested three bounded corrections. The correction preserves valid inactive later-mode preferences as latent Read-compatible state while active requests still defer and invalid values fail closed; clears selection state before every render attempt; restores exact assembly-owned weekday presentation; and removes raw source-hook coordinates from visible Details. M3 remains pending correction review, and live routes remain unchanged. | This correction commit; compact correction handoff `20260804T173010Z-day-reader-shell-integration-corrections` |
| 2026-08-04 | M3 — production Day Read integration external acceptance | Accepted — the production Day Read candidate reuses the existing assembly and Proper renderer behind the shared persistent shell, preserves Read-compatible legacy state, explicitly defers later-mode state, fails closed across invalid and superseded asynchronous transitions, and remains isolated from the live Day and Propers routes. Acceptance does not authorize cutover, Propers integration, later modes, public exposure, or recension work. | Candidate `45a6b76249e015f68830495ca2971e9dbc4a4e14`; correction `d0872545ccc92106cb457b448f37201381c5bb2d`; final micro-fix `c604edb8a1fffb1e5c0981798800ecb801258e7c`; handoffs `20260804T154620Z-day-reader-shell-integration` and `20260804T173010Z-day-reader-shell-integration-corrections`; external review dispositions *W3 Day reader-shell changes requested* and *W3 conditional acceptance, final micro-fix, and M3 closeout* |
| 2026-08-04 | W3 Propers Read integration candidate — second production Read entrance | Candidate pending external review. The unlinked, noindex Propers entrance uses the accepted shared shell, explicit M1 Propers state, production manifests, fragments, and Proper renderer; leaves missing identity unresolved; rejects invalid explicit state; and preserves coequal cycles and alternatives independently. This distinct W3 entrance does not reopen the accepted M3 Day integration. Public Day and Propers, the accepted Day candidate, later modes, search, public cutover, and production liturgical data remain unchanged. | Candidate `b0b1e5b63ba4a1d389b53276fa0bf9944c0ee909`; external-review handoff `20260804T212821Z-propers-reader-shell-integration` |
| 2026-08-04 | W3 Propers Read integration candidate corrections | Candidate pending external review. Browse requests translation-witness choice only when multiple identified witnesses can faithfully supply the selected formulary and translated language; source-language selection clears the private witness state. Every route attempt and Browse dismissal invalidates pending Browse loads so stale edition controls cannot replace the current form. The shared shell, M1 semantics, renderer, cycle handling, live routes, accepted Day candidate, and production data remain unchanged. | This correction commit; compact correction handoff recorded in the completion report |
| 2026-08-04 | W3 Propers Read integration external acceptance | Accepted — the W3 Propers Read integration enters the same production reader shell as the accepted Day candidate, preserves current valid formulary semantics through the M1 Propers state and production Proper renderer, leaves missing identity unresolved, fails closed on invalid state, preserves cycles and alternatives independently, requests translation witnesses only when formulary-specific translated material requires a choice, and remains isolated from the public Day and Propers routes. The initial review requested bounded Browse witness, Browse-race, tracking, and handoff corrections; the acceptance disposition confirms those blockers resolved. The reviewed evidence passed 84 focused tests, 90 public-alpha/gallery tests, and 27 Propers, 25 Day, and 18 shared-shell Chromium assertions. Shared-shell SHA-256 remained `bf1c062453f8fcfd5a68c1fe30e31aca89ea1a3c8adeef9a5525d8081ae8c707` for JavaScript and `e7195cd86ed4fc4a8455e97369702239eb22d709a13d3d8462d7759c01fe814a` for CSS. Public routes, the accepted Day candidate, M1 semantics, navigation, selectors, and production liturgical and generated data remained unchanged. The approved example baseline retained the same 23 unrelated divergences and two promised-deliverable commands; only the authorized count advanced to 18 tracked, 13 complete. Excess cycle-choice print whitespace is retained for later print refinement. | Candidate `b0b1e5b63ba4a1d389b53276fa0bf9944c0ee909`; correction `1e4587dfe04a11c18e996a16f7fbbdb54bc744a4`; handoffs `20260804T212821Z-propers-reader-shell-integration` and `20260804T225215Z-propers-reader-shell-corrections`; external-review dispositions *Propers Read candidate changes requested* and *Propers Read integration external acceptance and closeout* |
| 2026-08-05 | W3 Day Missal-mode integration candidate | Candidate pending external review. The existing unlinked Day entrance keeps Read as default and adds a continuous Missal assembled from the accepted M1 Day event stream, production Ordinary and Proper renderers, and the unchanged Ordinary seating model. Roman 1962 and postconciliar states retain distinct sequences; valid latent language and Eucharistic Prayer state survives mode changes; explicit invalid or inapplicable values and missing Proper seats fail closed; `why=1` remains deferred; and semantic location, history, races, reflow, accessibility, performance, and print have focused evidence. The public Day and Propers routes, accepted Propers candidate, M1 contract, seating engine, and production liturgical data remain isolated. | This candidate commit; external-review handoff recorded in the completion report after push |
| 2026-08-05 | W3 Day Missal-mode candidate changes requested | External review of candidate `a1221755d4fac2a6b9a009a91b99cd1da82eee9e` and handoff `20260805T145914Z-day-missal-mode-integration` passed the production Ordinary/seating architecture, edition distinctions, semantic option validity, ergonomics, isolation, and scope. Acceptance remains blocked on deterministic mode chrome for every non-ready outcome, keyboard-focus restoration after inline Eucharistic Prayer changes, and generation-safe direct-load and transition evidence. The correction remains bounded to those seams and full replacement captures; the candidate is not accepted or public. | Changes requested; correction commit and compact re-handoff pending |
| 2026-08-05 | W3 Day Missal-mode bounded corrections | Candidate pending independent correction review. One outcome-aware presentation path now commits requested Read/Missal chrome on every syntactically recognized state and neutral unchecked chrome for invalid `ordinary`; valid deferred, unresolved/territorial, and unrenderable states are distinct from explicit rejection. Inline Eucharistic Prayer changes restore focus to the rerendered checked semantic option while retaining reading location. The browser harness now proves fresh documents with unique non-semantic query nonces and document tokens, and same-document navigation with exact state plus greater committed render generation before the post-render frame boundary. All screenshots and the 21-page print were regenerated; no accepted architecture, public route, Propers surface, M1 seam, seating engine, or production data changed. | This correction commit; compact correction handoff recorded after push; acceptance remains open |
| 2026-08-05 | W3 Day Missal-mode evidence-settlement changes requested | External review of correction `ce5fce8364d24156e41c444c43673e7de31555d8` and handoff `20260805T183500Z-day-missal-mode-corrections` found the substantive product corrections sound and production isolation intact. Acceptance remains blocked only because two post-render animation frames do not prove inherited smooth scrolling and its semantic target have settled, and because both duplicate `ordinary` key orderings lack direct Chromium coverage. The micro-correction is limited to animation-frame stability proof, settled default/reduced-motion Eucharistic Prayer focus and location assertions, both duplicate-key orderings from fresh/Read/Missal paths, complete replacement evidence, and a new independent handoff. The candidate is not accepted or public. | Changes requested; evidence micro-correction and compact re-handoff pending |
| 2026-08-05 | W3 Day Missal-mode evidence-settlement micro-correction | Candidate pending independent external review. Exact document-token and committed-generation checks now precede a separate bounded animation-frame loop requiring five stable scroll, semantic-target, and focused-control frames with viewport intersection and cleared pending navigation. Settled default-motion EP I/III/IV/II and reduced-motion keyboard checks exposed and corrected one local Day-adapter issue by aligning the inline option group after semantic restoration; the shared shell and site scrolling remain unchanged. Both duplicate `ordinary` orderings are neutral and history-independent on fresh loads and transitions from Read and Missal. The complete Day screenshot and 21-page print set was regenerated; public Day/Propers, the Propers candidate, shared shell, M1 seams, seating, and production data remain isolated. | This micro-correction commit; compact correction handoff recorded after push; acceptance remains open |
| 2026-08-05 | W3 Day Missal-mode integration external acceptance | Accepted — every blocking review question is resolved and no further handoff is required. The internal Day reader reuses the production Ordinary presenter, M1 event stream, single Ordinary seating path, and Proper renderer while retaining edition-specific Roman 1962 and postconciliar structures, deterministic fail-closed state, semantic location/history/race ownership, and production isolation. The accepted handoff records 34 passing Day Chromium assertions plus the focused and regression suites, settled default/reduced-motion Eucharistic Prayer focus, neutral unchecked behavior for both duplicate `ordinary` key orderings on fresh and transitioned paths, 107 settled screenshot rows, and the 21-page print review with no console, request, or HTTP errors. Public cutover, later modes, search, source/recension expansion, and print redesign remain separate future decisions. | Candidate `a1221755d4fac2a6b9a009a91b99cd1da82eee9e`; correction `ce5fce8364d24156e41c444c43673e7de31555d8`; accepted micro-correction `86a9816c1bffdcbdd09469f5f8d005c666a8045e`; handoffs `20260805T145914Z-day-missal-mode-integration`, `20260805T183500Z-day-missal-mode-corrections`, and `20260805T201722Z-day-missal-mode-evidence-corrections` |
| 2026-08-05 | Liturgy reader visual-reset direction candidate | Candidate pending maintainer and independent visual review. Explicit maintainer direction reopens visual composition without disturbing accepted M1–M3/W3 behavior. One unlinked, noindex Day/Propers prototype compares Quiet Folio, Liturgical Instrument, and Contemporary Reader over the same semantic DOM, production adapters, renderers, seating, and shell controller. Liturgical Instrument is recommended for its ritual cue grid and continuous-action hierarchy; Folio's editorial restraint and Reader's compact chrome and Browse flow remain explicit comparison strengths. The current evidence records 52 same-run screenshots, 12 passing Chromium assertions, clean console/network/accessibility/overflow results, required responsive and enlarged states, deployed before/after comparisons, and a print smoke check. Public routes, accepted candidates, shared shell, M1 seams, seating, and production data retain exact hashes. This is a visual decision candidate, not acceptance or public cutover. | This candidate commit; compact external-review handoff recorded after the validated push |
| 2026-08-05 | Liturgy reader visual-reset direction selection | Independent review selected Liturgical Instrument as the production visual foundation and froze Quiet Folio and Contemporary Reader as comparison references. Selection closes the three-direction study but does not authorize production-integration execution or public cutover. Seven bounded visual blockers move into the separate Instrument correction candidate. | Reviewed end `0f3567dc509a2d5b42fd58a0e4c77c8f5e5dc113`; implementation `7233879350ff00c92fa2029ca04f481125daa519`; correction review remains open |
| 2026-08-06 | Liturgical Instrument correction — Work unit A | Candidate geometry correction pending the remaining Instrument finish and independent review. Read now uses one 39.75rem axis, measuring 636 px and about 75 characters at 768×1024 instead of 726 px/about 86. Missal preserves identity and the semantic cue grid while advancing the first principal text from 474.58 to 316.98 px at 1440×900, 441.77 to 324.97 px at 393×852, and 458.83 to 342.03 px at 320×852. The rebuilt preview passed all 12 Chromium assertions with no console, network, accessibility-name, or horizontal-overflow result. Shell/masthead and warning/rhythm correction remain next; accepted behavior and public routes remain unchanged. | This geometry checkpoint; canonical measurements and continuity in `build/agent-continuity/liturgy-reader-visual-plan.md` |
| 2026-08-06 | Liturgical Instrument correction — Work units B/C | Candidate finish pending Work unit D gates and independent review. The desktop card becomes a square, shadowless rail aligned immediately outside the ritual plane; the mobile dock is opaque and edge-integrated. Instrument now uses a three-stroke CSS mark and no visible meaningless progress dash, while internal semantic progress remains. Roman partial coverage becomes one exact compact status and advances held text by 197.39 px; postconciliar missing-language notices retain exact text in restrained inline pairs and advance first held text by 198.66 px at 1440×900. Mobile exchanges tighten and the 320-pixel first division wraps deliberately in two lines. The 53-capture run passed 13/13 Chromium assertions with clean console, network, HTTP, accessibility-name, duplicate-ID, and overflow results. | This finish checkpoint; full matrix/gates/handoff and independent correction review remain open |
| 2026-08-06 | Liturgical Instrument correction — Work unit D review candidate | Candidate ready for independent correction review; no acceptance or cutover claimed. The immutable handoff records 22 required full-size final states, five blocker baselines, two contact sheets, explicit route/hash/geometry/focus/semantic/error metadata, 140 focused Python passes, 13/13 visual-reset Chromium passes, 27/27 Propers browser passes, 18/18 shared-shell passes, successful locked public-alpha build/verify, Pages run `31094868150`, and byte-matched deployed assets. Day browser is 33/34 because its date-dependent first-visit test expects no notice on the current default date; the governed full gate stops at pre-existing example transcript divergence after task-owned promised-ledger examples were corrected and independently replayed 2/2. Public Day/Propers and accepted seams remain unchanged. | Implementation `62e712a1962080d1dc3c6e106651c41afbf7531b`; handoff `build/agent-handoffs/20260806T112813Z-liturgy-reader-instrument-correction/`; independent review only remaining gate |
| 2026-08-06 | Liturgical Instrument correction — independent review round 1 | Changes requested, narrowly. The reviewer confirmed the selected direction and passed six of seven original findings, including reading hierarchy, Read measure, ritual action, warnings, masthead, title wrap, and normal mobile spacing. Review retained the original shell blocker at 1024×768, where the floating card returned, and identified related mid-word action-label breaks at 200% text. Production-integration execution and public cutover remain unauthorized. | Reviewed commit `50288ddf9759f56e8a25e4907d8de25e27e25e8f`; exact disposition and bounded response in `build/agent-continuity/liturgy-reader-visual-plan.md`; narrow correction/re-review pending |
| 2026-08-06 | Liturgical Instrument correction — Round 1 shell checkpoint | Candidate correction pending successful deployed parity, immutable re-review handoff, and independent re-review. Instrument now transitions directly from the accepted 72rem ruled rail to an opaque, square, shadowless edge dock; a root-font-aware extreme state uses four whole labels in a 2×2 grid. The authoritative run records 15/15 Chromium assertions and 54 captures with exact opacity, end reserve, names, targets, overflow, focus, and normal-scale regression coverage. Focused Python is 141/141, Propers 27/27, shared shell 18/18, and Day retains only its unchanged current-date 33/34 stop. The first Pages attempt passed artifact build/verification/upload but timed out while the deployment remained externally queued; corrected deployed parity is not claimed. | Correction `ab89758e3f3ee165e0141e3605be88051450134b`; Pages run `31104342722` failed at queued-deployment timeout; continuity owns the exact evidence and stop |
| 2026-08-06 | Liturgical Instrument correction — Round 1 deployment follow-up | A second automatic Pages run for the truthful continuity checkpoint again passed checkout, locked setup, source verification, public build, Pages compatibility verification, configuration, and verified-artifact upload, then stopped only when deploy-pages polling reached its 600-second timeout. Deployed Day/Propers remain healthy and noindex but retain reviewed CSS, so corrected parity is still explicitly open. | Continuity checkpoint `c6b7f7f0a79468cfa1a503235044c92bd88c27b2`; Pages `31106008011`; another ordinary push-triggered attempt will accompany the next record |
| 2026-08-06 | Liturgical Instrument correction — Round 1 narrow re-review package | Candidate shell correction is fully measured and packaged for the three-question re-review. A third automatic Pages run again verified and uploaded the correct artifact but was canceled at the job's 15-minute ceiling during deploy polling; public prototypes remain HTTP 200/noindex with reviewed pre-correction CSS, so corrected parity is an explicit external blocker rather than a claimed pass. The handoff contains exact Round 1 correspondence, two blocker pairs, 11 original-pixel regressions, two inspected contact sheets, 15/15 browser assertions, focused sources, checks, and a runnable noindex candidate. | Correction `ab89758e3f3ee165e0141e3605be88051450134b`; checkpoint `3873bd99cb308432404378c665dbcb3246144c9e`; Pages `31107294462` cancelled; handoff `build/agent-handoffs/20260806T132759Z-liturgy-reader-instrument-correction/`; independent re-review and corrected deployed parity open |
| 2026-08-06 | Liturgical Instrument correction — Round 1 deployed re-review candidate | Pages run `31109086658` completed successfully for the immutable-handoff commit. Direct unlinked Day/Propers routes return HTTP 200/noindex and deployed CSS/JS byte-match source, resolving the earlier external polling stop. A fresh post-deployment immutable package keeps canonical continuity byte-identical and records the successful run and hashes. The candidate remains pending only the three-question independent visual re-review; production-integration execution and public cutover remain unauthorized. | Handoff commit `c388ab42dfc4f5c7d49abc71596d6bb511af5742`; final package `build/agent-handoffs/20260806T141831Z-liturgy-reader-instrument-correction/`; independent re-review only remaining gate |

For later updates, append a dated row with the workstream or unchanged
historical phase name, the evidence-backed result, and the exact commit(s).
Do not rewrite a completed row to make later sequencing look cleaner.
