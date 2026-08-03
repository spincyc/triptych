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

Baseline date: **2026-08-03**. Repository and deployed review baseline:
`18256c51e72099b64bb1b9a6b17db9b6257e7ebf` (`Add Proper placement
notes`).

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

The public Day and Propers links named for this review were inspected in
Firefox at 1440×900, 1024×768, 768×1024, 393×852, and an exact 320×852 CSS-pixel
viewport. States included Settings closed and open, Contents closed and open,
Propers only, Ordinary enabled, Why and rubrics enabled, Roman 1962,
postconciliar, a populated Notices and unavailable-text state, and Letter
print. The locally retained Phase 4–9 reports and screenshots were reviewed as
historical evidence as well.

Measured findings:

- The closed default reflowed at every width with no horizontal page scrolling.
- At 393×852 the Roman 1962 celebration title began at 69 CSS pixels and the
  first Proper began at about 266 pixels. At 320×852 the first Proper began at
  about 278 pixels. Both first views contained real liturgical text.
- Opening Day Settings at 393×852 moved the first Proper to about 692 pixels;
  the form consumes most of the initial screen and makes common date movement
  part of a large configuration task.
- Day Contents in Propers-only output contained one item, `Beginning`; it is not
  yet useful navigation for the default mode.
- Propers Contents correctly listed its eleven rendered semantic destinations,
  but it remained a document-flow list and did not report the current unit.
- Roman 1962 and postconciliar Ordinary states had no horizontal overflow, but
  repeated unavailable-text messages became more visually prominent than the
  liturgical hierarchy. The postconciliar populated Notices state also placed a
  large availability message before the reading.
- Current Letter print was mechanically usable and removed chrome, but a Roman
  1962 Ordinary/Why state produced 34 pages containing repeated withheld-text
  and source-detail material. Print needs a mode-aware information hierarchy,
  not only print CSS hiding controls.

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
this roadmap precedes further Phase 10 implementation. Once these documents
are committed, Phase 10.2 source acquisition may proceed in parallel with W1
and W2 reader redesign. The whole visual redesign is not a prerequisite for
adding source-grounded recension coverage. Recension work must nevertheless
obey the vision's partial-coverage, fail-closed source honesty, stable identity,
and shared-rendering rules. The selected 1956 Benziger printing remains
verified but inaccessible; no calendar key or data implementation proceeds
until the required pages are acquired and inspected.

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

| Milestone | Integrated result | Required inputs |
| --- | --- | --- |
| M0 — Governing contract | Vision, roadmap, routing, baseline evidence, and no production change | This documentation task |
| M1 — Semantic parity contract | Versioned fixture schema and shared identity/event/source/coverage assertions for existing Day, Propers, and CLI | W1, W4, W9 |
| M2 — Shell prototype decision | Tested wide/intermediate/mobile/zoom/print prototypes; bounded choices resolved; no liturgical data change | W2, W8, representative W9 fixtures |
| M3 — Shared Read and Missal slice | Both entrances use shared state, semantic renderer, navigation, and Read/Missal modes for Roman 1962 and postconciliar fixtures | W1, W2, first half of W3, W8, W9 |
| M4 — Study, discovery, and coverage slice | Shared Study apparatus, compact typed coverage, Propers browse/search, source/history links | W3, W4, W5, W8, W9 |
| M5 — Compare slice | Semantic recension/translation/cycle/alternative comparison in parallel and stacked forms | W3, W4, W6, qualifying W7 fixtures, W8, W9 |
| M6 — Release-quality reader | All world-class gates pass for the advertised coverage; compatible URLs and independently usable print ship | All applicable workstreams |

Phase 10.2 may advance source acquisition after M0 and may produce internal
coverage fixtures after its own source gates. It does not depend on M2–M6. A
public 1956-recension selector depends on its complete advertised coverage and
release gates, not merely on the first reader redesign release.

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

Every production slice passes the gates it affects. “No change” to liturgical
data is proved by semantic fixture parity, not assumed from a visual diff.

### Product and semantic gates

- Day and Propers identify and render the same edition-qualified formulary and
  semantic units consistently.
- Read, Missal, Study, and Compare are each one clear action away on both
  entrances, with Read initially active and visually dominant.
- Today and real text appear immediately in a first Day visit; a valid Propers
  deep link renders immediately; a new Propers visit opens browse/search.
- Date navigation is available outside full Settings.
- Contents reports the current semantic unit and only actual destinations.
- Position and focus survive auxiliary panels, supported state changes, and
  mode transitions according to a documented rule.
- No unsupported selection falls through to another recension, locality,
  translation, cycle, alternative, formulary, or Ordinary.

### Source, data, and parity gates

- Every rendered unit and decision carries stable source/provenance and typed
  coverage data adequate for Study and tests.
- Browser, generated data, CLI, and tests agree on identity, selected branches,
  event order, text, sources, rights state, and explicit absence.
- Search results and deep links resolve the same stable formulary identities as
  the generator.
- Comparison aligns semantic units and leaves one-sided units explicit.
- Source, calendar, recension, versification, rights, and release checks owned
  by affected guidance pass.

### Responsive and visual gates

- The default 1440×900 and 393×852 first views show identity and real text.
- 1024×768 and 768×1024 use one reading column and at most one auxiliary panel.
- No horizontal page scroll or lost functionality occurs at 320 CSS pixels,
  400% zoom, or 200% text enlargement.
- Wide rails never compress the reading below its usable measure and are absent
  or empty when irrelevant.
- Mobile sheets/dialogs preserve safe areas, focused controls, and reading
  location. Compare and bilingual fragments stack by corresponding unit.
- Missing-text treatment is unmistakable but subordinate to the celebration
  and available liturgical text.

### Accessibility gates

- WCAG 2.2 AA automated checks report no applicable violations, followed by
  manual review of structure, language changes, contrast, focus order,
  focus-not-obscured, names/roles/states, status announcements, and reflow.
- Every core path is complete with keyboard alone and with touch alone.
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
- each auxiliary surface open, one at a time, with focus and scroll assertions;
- Read, Missal, Study, and Compare;
- Roman 1962 and postconciliar;
- a pre-1955 or other qualifying comparison state;
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

The Phase 10.1 proposed ordinary-Sunday vertical slice remains a useful internal
parity target only after its exact source is available. Phase 10.2's current
action is to obtain and inspect the specified pages of the 1956 Benziger
printing. Until then the state has no product key, no source registration, no
transcription, no generated data, and no selector. When it does proceed, it
uses the shared renderer and typed partial-coverage contract rather than
edition-specific UI.

## Current next action

Commit the vision, this roadmap, and the AGENTS routing as one documentation
checkpoint after all documentation and policy checks pass. No reader or
recension implementation belongs in that commit.

Immediately after that checkpoint, start two independent actions in parallel:

1. W1/W9 define the smallest shared semantic fixture and URL-state contract
   that proves one Roman 1962 and one postconciliar object identical across Day,
   Propers, generated data, and CLI, without changing presentation.
2. W7 continues Phase 10.2 by contacting the named institutional holder for the
   exact 1956 Benziger page set. It remains acquisition/research work until the
   witness and rights gates pass.

W2 may prototype the reader shell against existing fixtures at the same time.
No prototype chooses liturgical defaults or creates data to fill a review state.

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
| 2026-08-03 | Phase 10, Step 1 — Roman 1955 vertical-slice assessment | Recommended an exact-edition, source-bounded 1956–1960 slice; found source and precedence blockers. | No tracked change; review baseline `18256c51e` |
| 2026-08-03 | Phase 10, Step 2 — source acquisition | Identified the 1956 Benziger edition and institutional copies, but classified the witness verified and inaccessible; implementation remains blocked on page inspection and rights. | No tracked change; review baseline `18256c51e` |
| 2026-08-03 | M0 — browser vision and roadmap stabilization | Establishes the governing destination, parallel workstreams, gates, and routing without production changes. | The commit containing this document; record the exact SHA in the task completion report |

For later updates, append a dated row with the workstream or unchanged
historical phase name, the evidence-backed result, and the exact commit(s).
Do not rewrite a completed row to make later sequencing look cleaner.
