# Dynamic Missal and Propers browser vision

## Status and authority

This is the governing product architecture for Triptych's dynamic Roman Missal
and Propers browser. It controls browser-visible liturgical reading, navigation,
study, comparison, responsive behavior, accessibility, performance, printing,
and sharing. It applies to the Day and Propers entrances and to their links with
How the Missal Changed and the Source Library.

This document states the destination and the invariants. The evolving execution
record is [the liturgy-browser roadmap](liturgy-browser-roadmap.md). Source,
calendar, recension, rights, and release rules remain owned by their existing
guidance. If this document and an implementation phase report differ, this
document controls future product work; the report remains evidence of what that
phase actually attempted and proved.

Reading Missal v1 is a successful baseline, not the final product. Its
phase-specific exclusions of modes, navigation rails, annotations, and new
interactions do not constrain later phases. Its successful principles do:
calm reading, a dominant celebration title, restrained controls, useful first
viewport, responsive reflow, print quality, and source honesty.

A fundamental redesign of the reader architecture is permitted. All advanced
Triptych capabilities remain equally supported and discoverable; equal access
does not mean equal visual prominence. Fast daily reading and the text itself
remain dominant.

## Product promise

**Triptych is a source-auditable, edition-aware dynamic Roman Missal. A reader
can begin with a date or a particular formulary, choose the applicable recension
and locality, read the liturgy continuously in its actual order, and inspect why
every text, placement, commemoration, omission, option, and historical change is
present.**

The defensible differentiator is not a large text catalogue by itself. It is
the joined chain from civil date and competent calendar, through sourced
precedence and formulary resolution, to semantic placement in the rite, exact
witness and rights information, and act-based history. Triptych must let a
reader move along that chain without hiding an uncertainty or substituting a
plausible text from another edition, locality, translation, cycle, or Ordinary.

## Product model

### One reader, two entrances

The two entrances answer different questions and must not collapse into one
ambiguous route.

**Day is date-first and calendar-resolved.** It answers: *What Mass or liturgy
is appointed on this date, under this recension and territorial calendar, and
why?* It may resolve competing temporal and sanctoral celebrations, precedence,
rank, commemorations, territorial and local branches, color, season and week,
Sunday and weekday cycles, readable formularies, alternatives, Ordinary and
Eucharistic Prayer options, omissions, partial coverage, rubrics, and act
history. A date is part of the identity of this entrance.

**Propers is formulary-first and calendar-independent.** It answers: *Show me
this particular Mass or formulary independently of a date.* It supports browse,
search, stable formulary links, cycles and alternatives, original texts and
translations, sources and witnesses, study, comparison, printing, and movement
to dates on which the formulary is appointed. A civil date is not required to
identify this entrance.

Both entrances render the same semantic liturgical object through one reader
architecture and visual language. Entrance context changes selection and
explanation; it must not produce a second interpretation of the same formulary,
Proper, Ordinary slot, source, or coverage fact.

### The four connected products

| Product | Primary object | Relationship to the reader |
| --- | --- | --- |
| Day | A civil date resolved under a calendar, recension, and locality | Selects the appointed liturgical object and explains the decision. |
| Propers | A stable formulary independent of a date | Finds and opens the same liturgical object directly. |
| How the Missal Changed | Acts, printed stations, branches, and changes between states | Supplies the historical reason and semantic change links used by Study and Compare. It is not replaced by a comparison pane. |
| Source Library | Works, editions, artifacts, passages, rights, and availability | Supplies the auditable evidence behind displayed text and decisions. It remains the full source record; the reader presents contextual summaries and links. |

The reader may open contextual history or source material without losing its
current place. Full research records stay in their owning products rather than
being copied into the reading DOM.

## Primary user journeys

1. **Read today's liturgy.** Open Day, see today's celebration identity and the
   beginning of its appointed texts immediately, then move through the Propers
   by ordinary vertical scrolling.
2. **Change the day or governing edition.** Use adjacent-day controls without
   opening full Settings, or open the compact chooser for a date, missal,
   territorial calendar, Bible, or language. The resolved title and content
   change without losing a sensible reading location.
3. **Read continuously as a missal.** Switch once to Missal mode and see the
   Ordinary with each Proper seated at its actual liturgical location.
4. **Understand a decision.** Switch once to Study and inspect why the
   celebration won, what was commemorated or displaced, which rubric and source
   control the result, and what remains unavailable or unresolved.
5. **Find a formulary.** Open Propers to a meaningful browse/search entry,
   search by a supported identity or citation, and receive a stable deep link.
6. **Compare corresponding units.** Switch once to Compare, choose supported
   recensions, translations, cycles, or alternatives, and compare matched
   semantic slots with their provenance and historical-change links.
7. **Cite, share, or print.** Copy a URL that reproduces the material semantic
   state, or print an independently intelligible reading with edition, date or
   formulary identity, source, and coverage context.

## Shared view modes

Mode is first-class URL state. A visible, consistently placed mode control is
present on both entrances. Read is the emphasized action; Missal, Study, and
Compare are each one clear action away and must not be hidden inside Settings.
Equal access does not require equal visual prominence.

### Read

Read is the default and is optimized for fast daily reading. It shows the
appointed Propers or other appointed texts in their actual order with minimal
application chrome. The Ordinary is off. Explanations, rubrics, source detail,
and extended apparatus are closed. Claim-local warnings remain at the claim
they limit, but routine provenance must not interrupt the reading flow.

### Missal

Missal presents one continuous celebration: the Ordinary supplies the frame
and the Propers occupy their actual semantic seats. Speaker, action, and rubric
information use a disciplined hierarchy quieter than the principal text.
Edition-specific options appear at their actual points of choice. A missing or
unlicensed Ordinary element is identified there; another edition's words are
never substituted to make the sequence appear complete.

### Study

Study exposes the calendar-resolution chain, rank and precedence,
commemorations and displaced celebrations, branch and formulary choices,
rubrics, seating and placement, provenance, source witnesses, page or locus
references, translation rights, unavailable or partial coverage, and links to
the governing acts and historical changes. The material uses one coherent
interaction model: contextual summaries lead to details, and the reader can
return to the same liturgical location and focus.

### Compare

Compare aligns semantic liturgical slots, not lines, paragraphs, or incidental
DOM positions. It may compare recensions, translations, Bible renderings,
cycles, or authorized alternatives. Each side names its edition, branch,
source, rights, and coverage state. A unit that exists on only one side remains
an explicit absence on the other; it is not shifted into a neighboring match.

Wide screens may use parallel columns when that improves correspondence.
Mobile stacks each matched unit as a pair before moving to the next unit.
Compare links material changes to How the Missal Changed and the source acts;
it does not infer a historical change from witness or OCR difference alone.

## Exact default behavior

These defaults apply unless a valid URL or preference overrides them:

1. URL state has highest precedence.
2. Valid remembered user preferences come next.
3. Repository-declared defaults govern a first visit. Existing manifest or
   policy owners determine the first-visit missal, Bible, and language; the UI
   must not invent a theological default or depend on array order that the
   repository has not declared authoritative.
4. Day opens to today in the user's civil date context unless the URL specifies
   another valid date. It does not infer a territorial calendar from
   geolocation.
5. Read is the initial mode. The Ordinary is off. Why, rubrics, and extended
   apparatus are closed.
6. Routine Notices are summarized and closed. A warning opens or remains
   inline only when concealing it would make immediate reliance unsafe.
7. Previous, Today, Next, and direct date access are available without opening
   full Settings.
8. Vertical scrolling is the ordinary web reading model. The browser does not
   imitate page turning; print and PDF are the paginated forms.
9. A valid Propers deep link renders that formulary immediately. A new Propers
   visitor receives a meaningful browse/search entry, never an unexplained
   arbitrary formulary chosen from a list.
10. No unsupported state silently falls back to another recension, locality,
    translation, cycle, alternative, formulary, or Ordinary.

Remembered preferences may include stable choices such as missal, territorial
calendar, Bible, display language, or mode. They may not override an explicit
URL, convert an unsupported state into a supported one, or turn a transient
unsafe warning into a remembered dismissal. A date or formulary link must work
correctly with storage unavailable.

## Reader architecture by viewport

These are behavioral constraints, not pixel-perfect mockups. Breakpoints follow
available space and content behavior rather than named devices.

### Wide desktop

- One dominant reading column normally holds ordinary prose to approximately
  60–72 characters per line.
- A slim, location-aware navigation rail may occupy one outer margin. A
  contextual Study/source rail may use the other.
- A rail disappears or remains visually empty when it has no relevant content;
  the page is never surrounded by a permanent dashboard.
- The navigation rail reports current location as well as destinations.
- Study material follows the liturgical unit in view and does not shift the
  reading column when opened.
- Compare may use parallel semantic columns, with synchronized correspondence
  that does not require synchronized pixel scrolling.

### Tablet and intermediate widths

- The reading surface is a single column.
- At most one auxiliary panel is open at a time.
- Navigation and Study use accessible drawers or overlays and do not
  permanently compress the text.
- Opening and closing an auxiliary panel preserves the current reading
  location and returns focus appropriately.

### Mobile

- The page has one reading column and compact access to date or browse,
  Contents, mode, and Study functions.
- Large forms and apparatus use accessible sheets or full-screen dialogs, not
  expanding blocks placed above the text.
- Controls do not obscure a focused element or the current reading location.
- Practical touch targets aim for 44–48 CSS pixels while meeting at least the
  applicable WCAG minimum and spacing rules.
- Compare stacks matching fragments vertically. Bilingual presentation also
  stacks each corresponding fragment; it never puts two complete documents
  side by side.
- Layout respects safe areas and `prefers-reduced-motion`.
- At 393×852 in the default state, the celebration identity and the beginning
  of actual liturgical content are both visible in the initial viewport.

### Bilingual and multi-witness text

Bilingual is a text presentation inside Read, Missal, Study, or Compare, not a
fifth mode. Corresponding semantic fragments remain adjacent. On a wide screen
they may form paired columns if both remain readable; at narrower widths each
source fragment is immediately followed by its translation. Labels always say
which language, edition, numbering, and witness is shown. Missing translation
does not suppress the original or borrow from a different witness.

### Print and PDF

Print removes navigation, disclosures, mode controls, buttons, and other
interactive chrome. It preserves enough context to stand alone: Day date and
resolved celebration or Propers formulary identity, missal/recension and
locality, selected text editions and languages, cycle or alternative, source
and rights acknowledgements required for use, and concise coverage warnings.
Print order follows semantic liturgical order, prevents stranded headings where
practical, and never relies on screen color alone. Print-specific pagination may
be typographic; the screen experience remains scroll-based.

## Navigation and search

### Global reader actions

Date or browse, Contents, mode, and Study are the four primary reader actions.
They use the same names and positions on Day and Propers. Settings holds
infrequent configuration, not common navigation. Share and Print are available
without entering Study.

Contents is generated from semantic liturgical units, not translated heading
strings. It is location-aware, marks the current unit, follows rerendered
branches, and does not list nonexistent or hidden material. Opening or closing
it preserves position; choosing a destination moves focus and reading location
predictably without corrupting the semantic URL.

Day provides adjacent-date movement, Today, direct date entry, and access to
every readable formulary resolved for the date. Propers provides browse and
search before a selection, previous/next only within a clearly named result or
browse order, and links from a formulary to known calendar uses without making
one date part of the formulary's identity.

### Search contract

Propers search covers, where the repository has structured evidence: title,
saint, incipit, season, formulary type, Scripture citation, civil date, and
source or witness. Results identify missal/recension, type, key, language or
text availability, and material coverage limits before selection. Search does
not merge same-named formularies across editions. A result URL is stable and a
no-result state explains the searched scope without substituting a nearby
answer.

### URL and sharing contract

URLs reproduce all state needed to identify and cite what is shown: entrance,
date or stable formulary key, missal/recension, locality or territorial
calendar, Bible and numbering where selected, text and Ordinary languages,
cycle, authorized alternative or variant, chosen readable formulary, and mode.
Compare URLs identify both sides and the comparison dimension. Temporary panel
openness and scroll pixels need not be canonical URL state, but semantic
location anchors must be stable. Existing valid Day and Propers URLs remain
resolvable through additive parsing, canonicalization, or documented redirects.

## Capability map

The shared architecture must carry these capabilities without moving advanced
work into a separate product:

| Domain | Required capability |
| --- | --- |
| Calendar | Civil-date navigation; temporal and sanctoral candidates; rank, color, season, week, Sunday and weekday cycle; competing celebrations, commemorations, transfers, omissions, all readable formularies, and decision explanations. |
| Edition | Missals and dated recensions; effective date ranges; territorial and local calendars; partial recension coverage; unsupported dates and missing material. |
| Text | Multiple Bible editions; versification and psalter distinctions; original text and translations; oration and Ordinary language; Eucharistic Prayer and other legitimate options; translation rights and availability. |
| Order | Speaker, action, rubric, semantic slot, seat, and locus; cycles and alternatives at the point of choice; continuous Ordinary with seated Propers. |
| Evidence | Source citations; physical witnesses and page references; provenance; calendar reasoning; acts and change histories; explicit uncertainty and incompleteness. |
| Discovery | Search by title, saint, incipit, season, type, citation, date, and source; stable deep links; sharing. |
| Output | Responsive reading; semantic comparison; print and PDF; parity among browser, generated data, CLI, and tests. |

Coverage may expand over time. The interaction and truthfulness requirements do
not weaken when coverage is narrow.

## Source, provenance, rights, and partial coverage

- Every displayed liturgical text and every calendar, seating, or historical
  decision retains the repository identity needed to reach its source record.
- Study distinguishes a governing source, a corroborating witness, a
  translation source, a generated inference, and an unresolved lead. A page
  reference is never presented as verified unless the corresponding witness was
  actually checked.
- Original text and translation remain separately attributable. Rights status,
  required acknowledgement, withheld text, and the reason for unavailability
  travel with the affected text.
- A concise coverage summary describes the selected recension and locality.
  Claim-local absence remains at the missing unit. Extended inventories and
  rights detail belong in Study or the Source Library.
- Partial coverage is a first-class state with an advertised supported extent.
  The reader distinguishes “not part of this rite or branch,” “not present in
  this witness,” “not yet sourced,” “not publishable here,” and “not resolved.”
- A warning must be unmistakable without becoming the largest repeated visual
  object on the page. Repeated absences may be summarized with per-unit markers
  and one accessible explanation, provided no distinct reason is lost.
- Source honesty and explicit incompleteness outrank visual smoothness. There is
  no silent cross-recension or cross-locale fallback.

## Accessibility requirements

The supported reader conforms to WCAG 2.2 Level AA across core workflows, not
only at the static page shell. The test matrix includes keyboard, touch, browser
zoom, text enlargement, forced colors, reduced motion, and representative
screen-reader use.

- Semantic headings, landmarks, lists, forms, tables, language attributes, and
  reading order must remain meaningful in every mode.
- All functions are operable by keyboard. Focus is always visible, is not
  obscured by rails, sheets, or sticky controls, and moves only in response to
  an understandable action.
- Dialogs and sheets trap focus only while modal, have an accessible name and
  close action, close with Escape where appropriate, restore focus to their
  invoker, and preserve the prior reading location.
- Disclosures use a button with a programmatically exposed expanded state and
  an associated controlled region. Enter and Space operate them.
- Text and non-text contrast meet WCAG requirements. Metadata remains readable;
  liturgical hierarchy, warnings, selection, and comparison differences are
  never communicated by color alone.
- Content reflows at 320 CSS pixels without horizontal page scrolling or loss
  of function. Genuine comparison structures may transform to stacked units;
  they do not claim a blanket two-dimensional-layout exception.
- The reader supports 200% text enlargement and 400% browser zoom without
  clipped controls, hidden content, or loss of semantic correspondence.
- Status and loading messages are announced without repeatedly interrupting
  reading. Changes of date, formulary, or mode yield an intelligible new title
  and focus outcome.

The normative accessibility basis is [WCAG 2.2](https://www.w3.org/TR/WCAG22/).
Interactive patterns follow the [WAI Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/),
including its [disclosure](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/)
and [modal dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
patterns where those widgets are used.

## Performance requirements

- Preserve the additive generated-data architecture in
  [web-data guidance](web-data.md). Do not pre-render the Cartesian product of
  missals, dates, formularies, translations, modes, and comparisons.
- A valid deep link begins resolving and rendering its requested object
  immediately. It must not render an arbitrary default formulary first.
- Read's critical path loads only what is needed to identify the selection and
  show its initial real text. Ordinary, extended Study evidence, comparison
  peers, and remote source detail load on demand and never delay the default
  reading unnecessarily.
- Changes preserve useful rendered content until replacement content is ready,
  while clearly marking busy state and refusing stale source or resolution
  claims.
- The release gate targets the current “good” Core Web Vitals thresholds at the
  75th percentile, evaluated separately for mobile and desktop: LCP at or below
  2.5 seconds, INP at or below 200 milliseconds, and CLS at or below 0.1.
  Field data is preferred when sufficient; reproducible lab tests guard changes
  before field data exists.
- Milestones set and enforce route-specific resource and main-thread budgets
  from a measured baseline. A prototype may choose the numbers; it may not ship
  without them.

The performance basis is [web.dev's Core Web Vitals guidance](https://web.dev/articles/vitals).

## Visual and interaction principles

- Liturgical text is the primary visual object. Application controls use a
  quieter vocabulary and never turn the page into a dashboard.
- The celebration or formulary title remains dominant, followed by restrained
  identity metadata and real liturgical content in the useful first viewport.
- Body text normally has an effective size of at least 16px, comfortable
  long-form line height, and a controlled measure. Running text is left aligned,
  not fully justified.
- Hierarchy arises from semantic structure, spacing, size, weight, and labels,
  not color alone. Source and rubric red is restrained and consistently means
  the same thing.
- A card grid does not wrap every Proper, Ordinary fragment, note, or source.
  Boundaries exist only where they clarify a relationship or state.
- No gratuitous animation or simulated page turn is permitted. Motion respects
  reduced-motion preferences.
- Opening and closing auxiliary material preserves scroll position. Focus
  restoration, keyboard access, and expanded state are part of the interaction,
  not later polish.

The typographic requirements are grounded in
[USWDS typography guidance](https://designsystem.digital.gov/components/typography/),
which recommends an effective 16px minimum for most body text, left alignment,
at least 1.5 line height for long text, and a long-form target near 66
characters. Responsive behavior follows the small-screen-first and bounded-line
principles in [GOV.UK layout guidance](https://design-system.service.gov.uk/styles/layout/)
and its user-task discipline in
[GOV.UK content guidance](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/plan-manage-content/identify-user-needs/).

## Non-goals and rejected anti-patterns

This vision does not select specific fonts, ornaments, icons, animation styles,
or a fashionable visual theme. Those are prototype decisions subordinate to
the invariants.

It does not add audio, social feeds, user accounts, or an offline application;
the repository contains no controlling product plan for them. It does not turn
the browser into a page-turning facsimile, replace print with screen pagination,
merge Day and Propers into an ambiguous route, or copy the full Source Library
and act history into every reading.

Rejected anti-patterns include:

- permanent dashboard chrome around a reading;
- burying common date navigation or modes inside Settings;
- a Contents list that is unaware of location or actual branch content;
- desktop rails that permanently compress the reading column or remain filled
  with irrelevant material;
- treating mobile as a narrower desktop with forms expanded above the text;
- aligning comparisons by line number or presenting two full mobile documents
  side by side;
- using a repeated large warning box for every unavailable unit;
- arbitrary first-formulary selection for a new Propers visitor;
- route-specific renderers that disagree about the same liturgical object; and
- any silent fallback across recension, locality, translation, cycle,
  alternative, formulary, Ordinary, or rights boundary.

## Product invariants

An implementation may not violate these rules:

1. Day and Propers remain distinct entrances to one shared reader.
2. Read is the calm, reading-first default; every advanced mode is one clear
   action away.
3. Text remains visually dominant, and the first useful viewport contains real
   liturgical content on representative desktop and mobile screens.
4. Semantic liturgical order and slots control rendering, navigation,
   comparison, CLI parity, and tests.
5. URL state outranks remembered preferences, which outrank repository-declared
   first-visit defaults.
6. No territorial calendar is inferred from geolocation.
7. No unsupported state silently borrows from another recension, locality,
   translation, cycle, alternative, formulary, or Ordinary.
8. Every displayed decision can reach its source and reasoning; every
   unavailable or partial result remains explicit.
9. Mobile uses single-column reading, accessible auxiliary surfaces, stacked
   correspondence, useful targets, and preserved position.
10. Screen reading scrolls vertically; print and PDF paginate.
11. Core workflows work with keyboard, touch, screen readers, zoom, text
    enlargement, forced colors, and reduced motion.
12. Browser, generated data, CLI, and tests may not disagree about identity,
    selection, order, text, source, or coverage.

## Definition of world-class completion

The product is world-class only when all of these are demonstrated against
versioned regression fixtures and real browsers:

- A first-time reader reaches today's appointed text immediately; the default
  mobile and desktop first view contains celebration identity and real text.
- A returning reader changes date, missal, locality, or mode without losing the
  relevant position or focus, and an explicit URL always wins over memory.
- Every advanced feature is discoverable within one clear interaction while
  the default page remains a reading surface rather than a dashboard.
- Day and Propers render the same liturgical object, ordering, option, source,
  and coverage state consistently.
- Every displayed decision exposes its source and reasoning; incomplete
  material is unmistakable but does not overwhelm the liturgical hierarchy.
- Compare aligns semantic liturgical units and preserves explicit one-sided
  additions, omissions, and unavailable text.
- All core workflows pass keyboard, touch, 200% text enlargement, 400% zoom,
  representative screen-reader, forced-color, and reduced-motion review.
- There is no horizontal page scroll or lost function at 320 CSS pixels.
- Print output is independently usable and retains required identity, source,
  rights, and coverage context without interactive chrome.
- URLs reproduce the semantic state needed for citation and sharing, and all
  supported legacy Day and Propers links remain valid.
- Browser, CLI, generated data, and tests agree on the same fixtures and
  semantic event sequence.
- The agreed WCAG 2.2 AA and Core Web Vitals gates pass.
- Regression fixtures cover representative Roman 1962, postconciliar,
  pre-1955, partial-recension, local-calendar, territorial-branch, cycle,
  alternative, competing-celebration, commemoration, and unavailable-text
  states. A fixture may be nonpublic where its source or coverage is not ready;
  it may not fabricate liturgical data.

## Bounded prototype decisions

The following choices are deliberately left to measured prototypes: exact
breakpoints; whether wide navigation is left or right; the visual form of the
mode control; whether an auxiliary mobile surface is a bottom sheet or
full-screen dialog in a given state; the compact representation of repeated
coverage warnings; and exact resource budgets derived from the measured
baseline. Each prototype must satisfy the defaults, accessibility behavior,
source honesty, first-viewport, URL, and parity invariants above. None may
reopen the one-reader/two-entrances model or the four modes.

## Change control

Amend this document only for a deliberate product decision that changes a
promise, mode, default, invariant, completion gate, or relationship among Day,
Propers, How the Missal Changed, and the Source Library. Record the reason,
evidence, compatibility consequence, and required roadmap migration in the
same commit. Implementation convenience, an isolated mockup, or an existing
limitation is not sufficient. Ordinary execution progress belongs only in the
roadmap.
