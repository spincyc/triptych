# Triptych corpus browser vision

## Status, authority, and scope

This is the candidate governing product, visual, and interaction architecture
for every non-PDF public Triptych surface. It is an A2-A4 design contract under
[`corpus-browser-roadmap.md`](corpus-browser-roadmap.md), based on the exact
A0/A1 records in
[`corpus-browser-inventory.md`](corpus-browser-inventory.md) and
[`corpus-browser-research.md`](corpus-browser-research.md). It remains pending
independent review and grants no production implementation or cutover authority.

The more specific
[`liturgy-browser-vision.md`](liturgy-browser-vision.md) continues to govern
liturgical identity, selection, modes, source behavior, URL state, and reader
semantics. This vision reuses its accepted calm reading, disciplined measure,
restrained chrome, useful first viewport, source honesty, responsive reflow,
and accessibility principles. It does not weaken or casually replace the
Liturgical Instrument. Canonical Day and Propers retain their exclusive shell
and exactly four actions until a separate accepted integration design says
otherwise.

PDFs remain the canonical printable editions. This vision neither redesigns
their typography nor makes browser print a substitute for them.

## Product promise

**The corpus is the product. Pages are typed views into it.** A reader should
be able to identify the object in view, read or inspect it without irrelevant
chrome, follow every supported relationship to its source or corpus context,
and preserve a citation-quality address. Visual polish may subordinate detail;
it may never blur work, edition, artifact, segment, passage, provider, rights,
availability, jurisdiction, recension, or uncertainty.

Triptych is not a magazine, document dump, dashboard, or set of unrelated
microsites. It is one source-first corpus with three compatible surface
archetypes:

1. **Reader** — sustained text such as a publication, Scripture chapter,
   source passage, or liturgical reading.
2. **Catalogue** — discovery and selection such as Home, the seven portals,
   Publications, and future typed search.
3. **Instrument** — data-dense research such as Commentary, Sources, History,
   Law, and the Liturgical Instrument.

These share tokens, identity language, accessibility behavior, and a typed
relationship vocabulary. They do not share one universal page composition.
Hybrid routes may combine archetypes only when each part retains a clear task
and reading order.

## Corpus information architecture

### Public places

The candidate compact global vocabulary is:

| Label | Current destination | Role |
| --- | --- | --- |
| Home | `/` | corpus map and task entrances |
| Publications | `/texts/` | all browser-readable and canonical-PDF treatments |
| Sources | `/sources/` | Work → Edition → Artifact/Segment → Passage evidence |
| Scripture | `/scripture/` | editions, numbering, reading plans, and passages |
| Liturgy | `/liturgy/` | protected Day and Propers Liturgical Instrument |
| History | `/history/` | acts, stations, versions, and changes |
| Law | `/law/` | code-qualified canons and act history |
| Commentary | `/catena/` | passage-linked voices and support state |

This candidate changes labels, not destinations. It uses **Publications** for
the current Every Document destination because the existing repository treats
Home as the Library and does not publish `/library/`. Independent review must
decide whether this clearer compact label should supersede the present
Home-is-the-library convention. Until acceptance, production continues to use
its current vocabulary and routes.

The seven editorial portals remain **Faith, Scripture, Liturgy, History,
Formation, Mary, and Law**. They organize publications; they are not another
global application hierarchy. Existing public titles remain intact, including
Mary, Curricula, and Postconciliar Roman Rite.

### Task entrances

Home should orient by honest tasks before exposing the full catalogue:

- Read a publication.
- Find a text or canonical PDF.
- Trace a source passage and its exact witness.
- Follow Scripture and commentary.
- See a liturgical or historical change.
- Look up a canon in its governing code.

Counts may appear only when generated from the same release artifact and
labeled with the counted object type. “Recent” and “featured” require a
deterministic repository-owned rule; otherwise omit them.

### Object and provider identity

Source identity has four visible levels: **Work**, **Edition**, **Artifact**
(with Segment where required), and **Passage**. Human citation, stable internal
ID, external alias, and rendered URL are related but distinct. Exact words must
name an edition; immutable research citations additionally need revision or
as-of identity.

Provider publications are not bibliographic Source Editions. GPT and Claude
outputs remain independent provider-qualified treatments even when a catalogue
groups them under one work. Product titles stay primary; provider identity is
a compact qualifying line or column. Exact model/runtime metadata belongs in
the research or provenance record, not ordinary reader chrome.

## Global corpus shell

### Desktop

The non-liturgy shell is a static, full-width masthead within a 74rem maximum
content axis. It contains one Triptych home link, the current domain, visible
global navigation, and a **Jump** action. It is separated from content by a
single rule. It has no hero illustration, ornamental crest, shadow, rounded
floating bar, or permanently open side panel.

The current domain is expressed in text and `aria-current`, never color alone.
The shell is deliberately not sticky in the foundation: a persistent global
bar would compete with route-owned sticky instruments and the accepted liturgy
reader. A later production implementation may propose persistence only with
measured collision and reading evidence.

### Narrow layouts

Below 52rem the global link row becomes one **Menu** button. It opens one native
modal dialog containing the same links in document order. Jump and Menu remain
44px or larger. No hamburger glyph is the only accessible name.

Every surface has one open overlay owner. Opening Menu, Jump, or Related closes
the previous overlay; Escape closes; focus returns to the invoker; background
content is inert while a modal is open; and reopening does not unexpectedly
move the underlying reading position. At 320 CSS pixels and 200% text, the
shell wraps or recomposes without horizontal page overflow.

### Liturgy adapter

Canonical Day and Propers do not receive the literal global masthead, a fifth
action, a second modal owner, or additional sticky chrome. Their accepted
reader masthead and four-action shell remain the public identity/navigation
adapter. Cross-corpus access belongs in their existing Details/footer seams or
a later separately reviewed integration. The foundation prototype therefore
does not import or alter production liturgy assets.

### Footer

The shared footer is quiet and linear: About, Contributing, Licence,
Third-party material, and Feedback. It does not duplicate the full global
navigation or present corpus statistics without a generated source.

## Visual language

Triptych should feel editorial, exact, and contemporary: warm paper-neutral
surfaces, near-black text, one restrained oxblood accent, strong blue focus,
hairline rules, square controls, and typography that distinguishes sustained
reading from interface metadata without ornamental historicism.

### Foundation tokens

The candidate token roles are:

```css
:root {
  --tp-font-text: Charter, "Bitstream Charter", "Iowan Old Style",
    Baskerville, Georgia, serif;
  --tp-font-ui: Inter, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, "Segoe UI", sans-serif;
  --tp-font-mono: ui-monospace, "SFMono-Regular", Consolas, monospace;

  --tp-canvas: #f4f1ea;
  --tp-surface: #faf8f2;
  --tp-surface-raised: #fffefa;
  --tp-text: #1d211f;
  --tp-text-muted: #555e59;
  --tp-text-subtle: #656d68;
  --tp-rule-subtle: #cfd3ce;
  --tp-rule-strong: #858d88;
  --tp-accent: #8f292b;
  --tp-accent-tint: #efe3e1;
  --tp-link: #8f292b;
  --tp-link-hover: #6f2831;
  --tp-focus: #1f5d8b;
  --tp-positive: #356b4c;
  --tp-caution: #835c13;
  --tp-negative: #9a2f32;

  --tp-space-1: .25rem;
  --tp-space-2: .5rem;
  --tp-space-3: .75rem;
  --tp-space-4: 1rem;
  --tp-space-6: 1.5rem;
  --tp-space-8: 2rem;
  --tp-space-12: 3rem;
  --tp-space-16: 4rem;
  --tp-space-24: 6rem;
  --tp-target: 2.75rem;
  --tp-reader: 46rem;
  --tp-liturgy-read: 39.75rem;
  --tp-instrument: 56rem;
  --tp-catalogue: 68rem;
  --tp-shell: 74rem;
}
```

The prototype uses local system stacks and no font network request. A later
implementation may evaluate self-hosted fonts only with licensing, full Latin
and polytonic/multilingual coverage, payload, fallback, and layout-shift
evidence. Portal colors may orient locally but never override the global
accent, reduce contrast, or carry meaning alone.

### Composition rules

- Use open composition and rules, not a card around every object.
- Use square corners. Reserve shadows for modal separation when a border is
  insufficient.
- Keep body text at a comfortable 60–72-character measure. Reader prose is
  normally no wider than 46rem/66ch; liturgy retains its protected 39.75rem
  Read axis.
- Use tabular numerals for counts, dates, loci, and identifiers.
- Keep headings sentence case and labels concrete. Interface text uses the UI
  stack; primary long-form text uses the text stack; machine identifiers use
  mono only when the literal identifier matters.
- Separate identity, status, and action. Do not encode unavailable, withheld,
  partial, unsupported, or uncertain as one generic disabled appearance.

Breakpoints are content-driven reference points, not device classes: 72rem for
wide catalogue/instrument breathing room, 52rem for global-shell reflow, 30rem
for dense-row recomposition, and an 18rem minimum supported viewport. Layouts
must still work between them.

## Reader archetype

The Reader makes the work and current locus immediately evident, then gets out
of the way.

1. Breadcrumb or compact corpus/domain context.
2. Work title and concise provider/edition/revision qualification.
3. Primary actions: canonical PDF when available, Contents, and Source details.
4. Optional in-page contents that does not permanently squeeze the text.
5. One primary text column with stable heading/paragraph/footnote anchors.
6. Source notes and qualifications adjacent to the claim they support.
7. Typed Related objects after the reading or in one deliberate surface.

Contents reflects actual headings. A browser-readable treatment never hides
its canonical PDF, and a PDF-only treatment remains discoverable with an
explicit availability state rather than a dead Reader. Citation copy should
use a stable public URL and visible human locator; it must not imply that a
current mutable page hash is immutable.

## Catalogue archetype

The Catalogue is list-first. Its default is a ruled, information-dense row or
group—not a tile wall.

1. Task-oriented title and one-sentence scope.
2. Search/filter controls proportionate to the corpus; applied filters remain
   visible and removable.
3. Honest count named by object type.
4. Grouped work rows with product title, collection, provider-qualified
   treatments, browser/PDF availability, and material status.
5. Useful zero state that repeats the active constraint and offers a concrete
   recovery action.

Provider treatments may be visually grouped but never merged into one edition.
On narrow screens, column labels become inline terms in a coherent row. The
first useful result remains near the first viewport; filters do not consume a
screen before the catalogue begins.

## Instrument archetype

The Instrument couples one exact object, one primary interpretive plane, and
one auditable evidence plane.

1. Object selector or stable cited locus.
2. Human-readable identity with edition, jurisdiction, date, or recension as
   applicable.
3. Primary text, comparison, or timeline plane.
4. Evidence/context surface holding source hierarchy, rights, availability,
   derivation, uncertainty, and technical identity.
5. Explicit partial, withheld, unread, unsupported, and invalid states.
6. Typed transitions to real related objects.

Wide layouts may place a compact contextual rail beside the primary plane only
when it does not move or narrow that plane. Narrow layouts have one reading
order; secondary material becomes in-flow disclosure or one modal surface, not
squeezed side-by-side panes. Digests prove byte identity only; they never stand
in for authority, verification, correctness, or reuse permission.

## Jump and future corpus search

A4 names the immediate shell action **Jump**, because the foundation has no
production corpus index. Jump may resolve a small, explicit, static destination
set and demonstrate typed result anatomy. It must be visibly labelled as a
synthetic fixture in the review prototype.

Production **Search** requires J0/J1/J2. It must:

- recognize exact public route, object ID, conventional citation, and known
  alias before lexical matching;
- group results by type and show why each matched;
- preserve Work/Edition/Artifact/Passage/provider distinctions;
- expose ambiguity and invalid input instead of nearest-object substitution;
- index public material only and prove that withheld text and private metadata
  do not leak through terms, snippets, counts, or facets;
- support stable, shareable search state without a server rewrite;
- remain useful without JavaScript through browse routes and direct URLs;
- meet measured payload, initialization, query-latency, memory, keyboard,
  mobile, multilingual, and accessibility budgets.

Pagefind is a feasibility hypothesis, not a decision. No hosted dependency,
AI answer layer, personalization, analytics, or crawler-only extraction is
accepted by this foundation.

## Contextual relationships

Related is a typed object router, not a recommendation feed. Every displayed
edge must name its relation and derive from repository-owned structured data,
for example:

- **cites passage** / **is cited by publication**;
- **uses in liturgy**;
- **comments on Scripture passage**;
- **changes act or formulary**;
- **governs canon**;
- **parallel provider treatment**;
- **is artifact/edition of work**.

Unsupported or merely plausible relationships are omitted, not inferred from
keywords. Ordering must be deterministic. A future relationship projection
needs source IDs, edge type, direction, derivation, revision, public state, and
tests against private/withheld leakage.

## Source, rights, and availability presentation

Immediate identity answers: What is this? Which edition or treatment? What
portion? Can I read it? One deliberate Details action exposes authority,
artifact, rights basis, acquisition/retrieval, derivation, revision, digest,
and known limitations.

Rights and availability are separate. Public access is not redistribution
permission. Withheld, unread, absent, partial, external-only, and unsupported
remain distinct textual states. Uncertainty names what is uncertain and why.
No state depends on red/green or an icon alone.

IIIF identities may later be typed external aliases for actual witnesses, but
Triptych does not treat an external Manifest or Canvas as its own Artifact and
does not implement a viewer without a concrete witness, rights disposition,
and accessibility/performance need.

## Responsive and accessible behavior

Every production surface must pass semantic landmarks, heading order, native
control semantics, keyboard operation, visible focus, focus restoration,
logical reading order, status announcement, touch targets, contrast, and
non-color state checks. Navigation uses links and a disclosure/modal pattern,
not an application `menubar`.

Required evidence includes 320 CSS pixels, 200% text enlargement,
representative 400% zoom, keyboard-only use, 44px primary targets, forced
colors, reduced motion, no-JavaScript core truth, browser print, and at least
one real mobile/assistive-technology review before release. Motion is optional,
short, and never required to understand state. Print suppresses interactive
chrome and points readers to—not away from—the canonical PDF.

## URL and citation behavior

Published paths, route-owned query keys, and meaningful fragments are citation
assets. A future migration must inventory existing public forms and provide
additive parsing/canonicalization or an explicit compatibility mechanism before
changing them. GitHub Pages provides no request-time rewrite or state-specific
metadata; designs may not assume either.

Each addressable object needs a canonical public route and an object/locus
identifier within that route. Invalid cited objects fail closed with the bad
value visible and a recovery path. They never silently select object zero, the
previous object, a nearest verse, or a default edition.

The prototype's `surface` and `panel` query keys are review controls only. They
are not proposed production URLs or data contracts.

## Performance and static architecture

The no-JavaScript page owns identity, primary content or honest browse entry,
canonical PDF action, essential source qualification, and legal links.
JavaScript progressively enhances navigation, filtering, relationship panels,
and search. Public projections are generated, versioned, deterministic,
additive, public-only, and lazy by route. A page must not load the whole corpus
to show one object.

Production gates measure compressed bytes, requests, cold/warm initialization,
main-thread work, p50/p95 interaction, memory, layout shift, image decoding,
and narrow-network behavior. Exact budgets are set from J1/L0 baselines, not
invented in A2. Large images need derivatives and dimensions; the current
sanctuary-gallery originals are not the pattern for future catalogue delivery.

## Relationship to canonical PDFs

The browser is the navigable, responsive corpus view. The installed reviewed
PDF is the canonical printable edition. Reader and Catalogue surfaces expose
the PDF whenever one exists, name PDF-only availability honestly, and never
silently regenerate or alter canonical pagination. Browser print is a useful
fallback and research aid, not the canonical edition.

## Rejected foundation approaches

| ID | Rejected approach | Reason and consequence |
| --- | --- | --- |
| RA-01 | One universal page layout | Reader, Catalogue, and Instrument have different primary tasks; share language and shell, not geometry. |
| RA-02 | Dashboard or giant-hero Home | Delays useful corpus entrances and fabricates product activity; Home becomes a calm task/corpus map. |
| RA-03 | Card grid as default | Hides edition/status comparison and scales poorly; use ruled lists and selective feature composition. |
| RA-04 | Permanent sidebars everywhere | Squeezes text and fails narrow reflow; context is deliberate and archetype-specific. |
| RA-05 | Faux medieval or ecclesial ornament | Credibility comes from authority and evidence, not parchment, crests, decorative crosses, or institutional imitation. |
| RA-06 | Literal global shell on liturgy | Creates duplicate identity, a fifth action, and competing modal/sticky owners; retain a protected adapter. |
| RA-07 | Calling a title fixture global search | Misstates capability; A4 uses Jump and J1 must earn Search through typed corpus benchmarks. |
| RA-08 | Flattening Work/Edition/Artifact/Passage | Destroys citation and rights truth; retain explicit object levels. |
| RA-09 | Merging GPT and Claude outputs | Provider-qualified treatments are independent; grouping never erases provenance. |
| RA-10 | Digest-first Source UI | Hashes prove bytes, not authority or rights; human identity and availability come first. |
| RA-11 | Generic Related recommendations | Untyped similarity is unauditable; display only deterministic structured edges. |
| RA-12 | Framework or IIIF migration in foundation | No measured problem requires either; preserve static architecture and design toward typed external identities. |

## Blocking review questions

1. Does **Publications** become the compact label for `/texts/`, superseding the
   current convention that Home itself is the Library, or should another label
   preserve that mental model?
2. Is the protected liturgy adapter correct: no literal global masthead and no
   change to its four-action exclusive shell under B0/B1?
3. Is **parallel provider treatment** the correct public term, avoiding the
   misleading suggestion that GPT/Claude outputs are bibliographic editions?
4. Are the three archetypes, token system, static masthead, Jump boundary,
   typed Related contract, and responsive compositions accepted for production
   implementation, rejected, or returned with specific changes?

## World-class completion

The corpus experience is complete only when every public route is assigned an
archetype and owning object model; every supported object has truthful identity,
availability, source, and citation behavior; cross-corpus relationships are
typed and auditable; global discovery works across public corpus types without
leakage; canonical PDFs remain obvious; all current paths have a compatibility
disposition; and the complete release passes deterministic generation,
route/state/browser/accessibility/performance/visual checks plus independent
product, source, rights, and release review.

Visual coherence alone is not completion. Neither is an accepted prototype.
A0-A4 become an implementation contract only through an explicit independent
disposition recorded in the roadmap and promise ledger; production work then
proceeds through B0-M1 with its own evidence and release authority.

## Change control

Amend this document only for a deliberate site-wide product or visual decision.
Put surface-specific semantics in the owning guidance and execution progress in
the roadmap. Record material rejected approaches and compatibility consequences
here rather than leaving them in chat.
