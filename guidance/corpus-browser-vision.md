# Triptych corpus browser vision

## Status, authority, and scope

This is the accepted governing product, visual, and interaction architecture
for Triptych's non-PDF public surfaces. The A2 product architecture is accepted
with the coordinator amendments D1–D20 in
[corpus-browser-master-plan.md](corpus-browser-master-plan.md). The A3
Reader/Catalogue/Instrument system and A4 shell, Jump, and contextual-navigation
work are accepted as foundation direction. That acceptance authorizes
non-liturgy foundation implementation and real-data design; it does not freeze
the synthetic prototype's pixels or accept any production route visually.

Independent review of Wave 1 at exact head `e42b928...` accepted C0 Home, C1
Publications, D0 Reader, and E0 Catena as design contracts and required bounded
corrections to F0 Sources and the shared non-Liturgy shell. Independent review
of correction head `ecbd93a0575c4b890cc814af7cd20d01f5af7beb` then recorded
**F0 Source Library — ACCEPT** and **Shared non-Liturgy shell — ACCEPT**,
closing those design-review gates. Accessibility and resilience remain
accepted production requirements with production proof outstanding; browser
print remains accepted only as a non-canonical fallback. A prototype, passing
local gate, branch push, or coherent appearance does not authorize production
cutover.

This document owns the active site-wide product and visual rules. The master
plan owns the coordinator disposition and program boundaries; the
[corpus-browser-roadmap.md](corpus-browser-roadmap.md) owns execution state,
evidence, next actions, and review disposition; and
[corpus-browser-implementation.md](corpus-browser-implementation.md) owns
generator seams, technical risks, and implementation sequencing. Surface
semantics remain with their more specific guidance.

The more specific
[liturgy-browser-vision.md](liturgy-browser-vision.md) continues to govern
liturgical identity, selection, modes, source behavior, URL state, and reader
semantics. This vision reuses its accepted calm reading, disciplined measure,
restrained chrome, useful first viewport, source honesty, responsive reflow,
and accessibility principles. It does not weaken or casually replace the
Liturgical Instrument.

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
microsites. It is one source-first corpus with three accepted surface
archetypes:

1. **Reader** — sustained text such as a publication, Scripture chapter,
   source passage, or liturgical reading.
2. **Catalogue** — discovery and selection such as Home, the seven portals,
   Publications, and future typed search.
3. **Instrument** — data-dense research such as Commentary, Sources, History,
   Law, and the Liturgical Instrument.

These archetypes share semantic tokens, identity language, accessibility
behavior, URL discipline, and typed contextual-navigation grammar. They do not
share one universal composition. A hybrid route may combine archetypes only
when each part retains a clear task and reading order.

## Corpus information architecture

### Public places

The accepted compact global vocabulary is:

| Label | Current destination | Role |
| --- | --- | --- |
| Publications | /texts/ | all browser-readable and canonical-PDF treatments |
| Sources | /sources/ | Work → Edition ownership with Passage → Artifact/Segment evidence |
| Scripture | /scripture/ | editions, numbering, reading plans, and passages |
| Liturgy | /liturgy/ | protected Day and Propers Liturgical Instrument |
| History | /history/ | acts, stations, versions, and changes |
| Law | /law/ | code-qualified canons and act history |
| Commentary | /catena/ | passage-linked voices and support state |

**Publications** is the accepted public label for /texts/. The route does not
change, and the Publications browser is a discovery view rather than a second
canonical catalogue. Each publication keeps exactly one owning catalogue and
one canonical PDF home.

The Triptych wordmark is a Home affordance. A separate visible Home navigation
item is optional and survives only if real 1024-pixel and 200%-text evidence
shows that the masthead remains calm. The accepted information architecture
does not freeze the number or geometry of visible desktop links; lower-priority
destinations may enter Menu earlier than the foundation prototype did.

The seven editorial portals remain, in order and with their established muted
color identities: **Faith** in white, **Scripture** in gold, **Liturgy** in red,
**History** in green, **Formation** in violet, **Mary** in rose, and **Law** in
black. They organize publications and provide durable corpus orientation; they
are not another global application hierarchy. A material change to their
names, order, or color identities requires an explicit amendment to
[repository.md](repository.md), not a silent homepage redesign.

### Task entrances

Home should orient by honest tasks while retaining the seven portals:

- read a publication;
- find a text or canonical PDF;
- trace a source passage and its exact witness;
- follow Scripture and commentary;
- compare or follow a liturgical or historical change;
- look up a canon in its governing code.

These entrances are a calm orientation layer, not dashboard widgets. Counts
may appear only when generated from the same release artifact and labelled with
the counted object type. Recent and featured material require a deterministic
repository-owned rule; otherwise they are omitted.

### Object and provider identity

Source identity has five distinct record types: **Work**, **Edition**,
**Artifact**, **Segment**, and **Passage**. Work owns Edition; Artifact, Segment,
and Passage are edition-owned siblings, while a Passage is controlled by an
Artifact directly or through a Segment. Human citation, stable internal ID,
external alias, and rendered URL are related but distinct. Exact words must
name an edition; immutable research citations additionally need revision or
as-of identity.

Provider publications are not bibliographic Source Editions. GPT and Claude
outputs remain independent provider-qualified treatments even when a catalogue
groups them under one work:

- **Independent treatment** is the human-facing label when distinguishing the
  independently produced treatments.
- **Parallel treatment** is the relationship label when two treatments of the
  same work are intentionally connected.
- Provider remains explicit metadata rather than being hidden in either label.

Exact model and runtime metadata belongs in the research or provenance record,
not ordinary reader chrome.

## Global corpus shell

### Non-liturgy desktop shell

The non-liturgy shell is a static, restrained masthead with one Triptych Home
link, current-domain identity, access to the accepted top-level destinations,
and a **Jump** action. One quiet rule separates it from content. It has no hero
illustration, ornamental crest, shadowed floating bar, or permanently open side
panel.

The current domain is expressed in text and aria-current, never color alone.
The foundation does not require a sticky global bar: persistence would compete
with route-owned instruments and must earn acceptance through real collision,
reading, and first-viewport evidence.

The exact maximum width, spacing, heading scale, and number of simultaneously
visible links are real-data decisions, not frozen prototype pixels. Density is
resolved by composition and Menu, never tiny text.

### Narrow shell and overlay ownership

At the content-driven point where the global link row no longer reads calmly,
it becomes one **Menu** button exposing the same destinations in document
order. Menu and Jump retain usable touch targets and visible text names; a
hamburger glyph is not the only accessible name.

Every surface has one open overlay owner. Opening Menu, Jump, Related, or a
route-owned auxiliary surface closes the previous overlay. Escape closes it,
focus returns to the invoker, background content is inert during a modal, and
opening or closing a surface does not unexpectedly move the underlying reading
position. At 320 CSS pixels and 200% text, the shell recomposes without
horizontal page overflow.

### Protected liturgy adapter

Canonical Day and Propers remain a protected surface family. They do not
receive the literal global masthead, a fifth primary action, a second competing
modal owner, additional sticky chrome, a print redesign, or site-wide Search
inside the reader shell. Their accepted masthead and exactly four actions
remain the public identity and navigation adapter: Date/Browse, Contents, Mode,
and Details.

Future low-chrome corpus context may use an accepted seam such as Details or a
quiet terminal/footer treatment only after separate liturgy-specific design
and visual acceptance. The accepted first viewport remains protected. The
concurrent Live Reader — Ritual Flow & Orientation work is a separate
deliverable; this corpus program neither supersedes it nor treats its
work-in-progress state as a visual oracle.

### Footer

The shared non-liturgy footer is quiet and linear: About, Contributing,
Licence, Third-party material, and Feedback. It does not duplicate the full
global navigation or present corpus statistics without a generated source.

## Semantic visual system

Triptych should feel editorial, exact, and contemporary: warm paper-neutral
surfaces, near-black text, one restrained oxblood accent, strong blue focus,
hairline rules, square quiet controls, and typography that distinguishes
sustained reading from interface metadata without ornamental historicism.

The accepted contract is a set of semantic roles, not frozen color values,
font sizes, spacing values, breakpoints, or masthead geometry:

| Family | Required roles |
| --- | --- |
| Surface | canvas, primary surface, raised surface |
| Text | primary, muted, subtle |
| Rules | subtle separator, strong boundary |
| Action | accent, accent tint, link, hover/active |
| Accessibility | focus |
| State | positive, caution, negative |
| Typography | sustained text, interface, literal identifier |
| Space | compact through major section rhythm |
| Measure | Reader, protected liturgy Read, Instrument, Catalogue, shell |
| Interaction | minimum practical control target and safe-area offsets |

Implementations may calibrate exact values after real-route screenshots, but
must preserve the role distinctions. Portal colors may orient their own
catalogues but never replace the global accent, reduce contrast, or carry
meaning alone.

Use robust system and locally available fallback stacks. There is no accepted
webfont dependency or assumption that Inter is installed. A self-hosted font
requires a separately authorized work unit covering licensing, generator
support, payload, layout shift, and full Latin, multilingual, and polytonic
Greek coverage where applicable.

### Composition rules

- Use open composition and rules, not a card around every object.
- Use square or nearly square controls. Reserve shadows for modal separation
  when a border is insufficient.
- Keep sustained text at a comfortable reading measure; test rather than freeze
  the foundation prototype's exact width.
- Preserve the accepted 39.75rem liturgy Read axis unless its owning guidance
  deliberately changes it.
- Use tabular numerals for counts, dates, loci, and identifiers.
- Keep headings sentence case and labels concrete.
- Use the interface type role for controls and metadata, the sustained-text
  role for primary prose, and the identifier role only when the literal
  machine or scholarly identifier matters.
- Separate identity, status, and action. Unavailable, withheld, partial,
  unsupported, unread, and uncertain never collapse into one disabled style.

Breakpoints are discovered from content rather than assigned to device names.
The foundation prototype's breakpoints are starting hypotheses. Real routes
must prove where navigation, dense rows, contextual rails, and text measures
recompose.

## Reader archetype

The Reader makes the work and current locus immediately evident, then gets out
of the way:

1. breadcrumb or compact corpus/domain context;
2. work title and concise provider, edition, and revision qualification;
3. primary actions: canonical PDF when available, Contents, and Source details;
4. optional in-page Contents that does not permanently squeeze the text;
5. one primary text column with stable heading, paragraph, and footnote
   anchors;
6. source notes and qualifications adjacent to the claim they support;
7. typed contextual objects after the reading or in one deliberate surface.

Contents reflects actual headings. A browser-readable treatment never hides
its canonical PDF, and a PDF-only treatment remains discoverable with an
explicit availability state rather than a dead Reader. Citation copy uses a
stable public URL and visible human locator; it does not imply that a current
mutable page hash is an immutable research citation.

The publication Reader is a renderer over the authoritative publication
source. [web-editions.md](web-editions.md) controls this lane: never create a
second editable prose copy or edit a generated web edition merely to obtain a
presentation effect; preserve visible revision identity, rights colophon, and
declared omissions; and re-run currency checks after renderer changes.

## Catalogue archetype

The Catalogue is list-first. Its default is a ruled, information-dense row or
group, not a tile wall:

1. task-oriented title and one-sentence scope;
2. search or filter controls proportionate to the corpus, with applied
   constraints visible and removable;
3. honest count named by object type;
4. grouped work rows with product title, collection, explicit provider,
   Independent treatment labels, browser/PDF availability, and material state;
5. useful zero state that repeats the active constraint and offers a concrete
   recovery action.

Independent treatments may be visually grouped but never merged into one
edition. A Parallel treatment link appears only when structured data records
that relationship. On narrow screens, column labels become inline terms in a
coherent row. Filters must not consume the first screen before results begin.

Publications remains a generated discovery view. It may expose metadata,
browser-read links, canonical PDFs, and facets without creating a second owning
catalogue or moving a publication's canonical home.

## Instrument archetype

The Instrument couples one exact object, one primary interpretive plane, and
one auditable evidence plane:

1. object selector or stable cited locus;
2. human-readable identity with edition, jurisdiction, date, or recension as
   applicable;
3. primary text, comparison, or timeline plane;
4. evidence/context surface holding source hierarchy, rights, availability,
   derivation, uncertainty, and technical identity;
5. explicit partial, withheld, unread, unsupported, and invalid states;
6. typed transitions to proven related objects.

Wide layouts may place a compact contextual rail beside the primary plane only
when it does not move or materially narrow that plane. Narrow layouts have one
reading order; secondary material becomes in-flow disclosure or one modal
surface, not squeezed side-by-side panes. Digests prove byte identity only;
they never stand in for authority, verification, correctness, or reuse
permission.

## Wave 1 real-route contract

Wave 1 applies the accepted foundation to actual data. Each surface has a
first-useful-content target and an explicit first-glance exclusion:

| Unit and surface | Primary job and object | First useful content | Deliberately not shown first |
| --- | --- | --- | --- |
| C0 Home | orient within the corpus and choose a task or editorial portal | clear corpus identity, task entrances, and the beginning of the seven-portal orientation | dashboard metrics, giant hero, fabricated recent activity, or a card wall |
| C1 Publications | find and distinguish a work, treatment, and available format | useful generated results plus the active constraint and honest object count | a full-screen filter form, duplicate owning hierarchy, or provider-conflated edition |
| D0 publication Reader | identify and read one provider-qualified publication | title, provider/revision identity, canonical PDF/source actions, and the opening substantive prose | permanent sidebars, extended technical provenance, or decorative masthead display |
| E0 Commentary | read Scripture and follow the held commentary attached to its exact extent | cited Scripture locus and text followed by the first applicable chronological or typed commentary link | global controls before Scripture, squeezed desktop columns on narrow screens, or implied commentary text |
| F0 Sources | find or inspect a Work, Edition, Artifact/Segment, or Passage | human identity, material availability, and either the first result or selected evidence object | hashes, retrieval detail, long legal apparatus, or unproved cross-corpus connections |

For every unit, wide evidence must show that context does not displace the
primary plane. Narrow evidence must show one coherent reading order, a useful
first viewport, and no page overflow. Keyboard evidence must cover entry,
operation, dismissal, and focus return. Invalid, empty, partial, unsupported,
withheld, unread, external-only, and zero-result states must remain explicit
where the underlying model supports them.

Contextual transitions are links between named corpus objects, not vague
recommendations. Every transition must preserve the current route's reading
position where practical and land at a stable address with enough visible
identity to confirm the destination.

## Jump and future corpus search

The immediate shared-shell action remains **Jump**. It may resolve a small,
explicit, static destination set and demonstrate interaction grammar. It may
not be called global corpus search or imply coverage beyond its fixture.

Production **Search** remains J0 → J1 → J2:

- Codex defines typed search jobs, result taxonomy, and exact, ambiguous,
  invalid, and empty states using real public corpus objects.
- Claude benchmarks a public-only static index for payload, latency, memory,
  multilingual behavior, route state, and rights leakage.
- Implementation follows only after that measured design is selected.

Production Search must recognize exact public routes, object IDs, conventional
citations, and known aliases before lexical matching; group results by type and
say why each matched; preserve Work/Edition/Artifact/Segment/Passage/provider
distinctions; expose ambiguity instead of substituting a nearest object; index
public material only; provide stable shareable state within static-hosting
constraints; and leave useful browse routes and direct URLs when JavaScript is
unavailable.

No hosted dependency, AI answer layer, personalization, analytics, crawler-only
extraction, or unmeasured search engine is accepted by this foundation.

## Contextual relationships

Contextual navigation displays only relationships proven by current
repository-owned structured data. Presently safe categories include:

- explicit containment;
- Passage → controlling Artifact or Segment;
- Catena fragment → Scripture locus;
- Catena passage → Source Library passage;
- act descent, act change, and unit history;
- document → owning catalogue page;
- Mass → propers → resolved Scripture loci.

Do not synthesize translation_of, used_by, derived_from, canon
correspondences, Law → Source citations, or generic related recommendations
from titles, keywords, prose, or domain proximity. Data-missing relationships
are recorded as future schema or generator opportunities under the owning
guidance, not fabricated as interface links.

Every displayed edge names its relation and direction, has deterministic
ordering, and remains traceable to its source identifier and public revision.
A new relationship type is first a schema and generator work unit with
no-private/no-withheld-leakage tests; only then may it become a UI feature.

## Source, rights, absence, and progressive disclosure

The first view answers: What is this? Which edition or treatment? What portion?
Can I read it? The following may be deferred to one deliberate Details action:

- hashes;
- extended artifact provenance;
- long rights or legal apparatus;
- secondary technical metadata.

The following may not be deferred, weakened, or conveyed only by color:

- required licence acknowledgement at the point of use;
- a withheld-text reason;
- typed absent, unread, unsupported, partial, external-only, and invalid state;
- the distinction between availability and redistribution rights.

Public access is not redistribution permission. Withheld prose is not sent to
the client merely because the interface can name its record. Uncertainty names
what is uncertain and why. A digest proves bytes, not authority or rights.

IIIF identities may later be typed external aliases for actual witnesses, but
Triptych does not treat an external Manifest or Canvas as its own Artifact and
does not implement a viewer without a concrete witness, rights disposition,
and accessibility and performance need.

## Responsive, accessible, no-JavaScript, and print behavior

Every production surface must pass semantic landmarks, heading order, native
control semantics, keyboard operation, visible focus, focus restoration,
logical reading order, concise status announcement, practical touch targets,
contrast, and non-color state checks. Navigation uses links and
disclosure/dialog behavior rather than an application menubar.

The comparable site-wide evidence matrix is:

- 1440 × 900;
- 1024 × 768;
- 768 × 1024;
- 393 × 852;
- 320 × 852.

Also exercise 200% text enlargement, exact 320-CSS-pixel reflow, meaningful
400% zoom/reflow, keyboard-only operation, forced colors, reduced motion,
browser print where print is not delegated solely to the canonical PDF,
no-JavaScript/static truth, console and network health, HTTP state, and
accessible names. Real routes additionally need at least one real-device or
assistive-technology review before release.

Do not create pixel-diff baselines before a real-data surface has independent
visual acceptance. Motion is optional, short, and never required to understand
state. Print suppresses interactive chrome and points readers to, not away
from, the canonical PDF.

## URL and citation behavior

Published paths, route-owned query keys, and meaningful fragments are citation
assets. The accepted label Publications does not rename /texts/. A future
migration must inventory existing public forms and provide additive parsing,
canonicalization, or an explicit compatibility mechanism before changing them.
GitHub Pages provides no request-time rewrite or state-specific metadata.

Each addressable object needs a canonical public route and an object or locus
identifier within that route. Invalid cited objects fail closed with the bad
value visible and a recovery path. They never silently select object zero, the
previous object, a nearest verse, or a default edition.

Local reading progress is deferred from the current foundation and Wave 1. If
introduced later for long-form publications, it must be optional, work with
storage unavailable, and yield to an explicit URL. Day's no-memory behavior is
intentional and remains unchanged.

## Static architecture and performance

The no-JavaScript page owns identity, primary content or an honest browse
entry, canonical PDF action, essential source qualification, and legal links.
JavaScript progressively enhances navigation, filtering, relationship panels,
and later Search. Public projections are generated, versioned, deterministic,
additive, public-only, and lazy by route. A page must not load the whole corpus
to show one object.

The implementation remains static and incrementally improved. The shared
layout seam, browser-core drift, duplicate helpers, hash-history defects,
nested landmarks, focus defects, and measured narrow overflow are engineering
debt, not permission for a framework or browser-stack rewrite.

Until separately changed and tested:

- no webfont dependency;
- no icon library;
- no framework migration;
- no root-relative link that breaks custom-domain-root or `/triptych/`
  project-path portability;
- no new asset type outside the generator allowlist;
- no violation of the HTML payload ceiling or static/no-server deployment
  model.

Production gates measure compressed bytes, requests, cold and warm
initialization, main-thread work, p50/p95 interaction, memory, layout shift,
image decoding, and narrow-network behavior. Exact budgets come from measured
real-route baselines rather than invented foundation numbers. Large images need
appropriate derivatives and dimensions.

## Relationship to canonical PDFs

The browser is the navigable, responsive corpus view. The installed reviewed
PDF is the canonical printable edition. Reader and Catalogue surfaces expose
the PDF whenever one exists, name PDF-only availability honestly, and never
silently regenerate or alter canonical pagination. Browser print is a useful
fallback and research aid, not the canonical edition.

## Rejected directions

| ID | Rejected direction | Binding consequence |
| --- | --- | --- |
| RA-01 | One universal page layout | Reader, Catalogue, and Instrument share language and behavior, not geometry. |
| RA-02 | Dashboard or giant-hero Home | Home begins with calm task and corpus orientation plus the seven portals. |
| RA-03 | Card grid as the default | Use ruled lists and selective composition that preserve comparison and status. |
| RA-04 | Permanent sidebars everywhere | Context is deliberate and reflows into one narrow-screen reading order. |
| RA-05 | Faux medieval or ecclesial ornament | Credibility comes from authority and evidence, not parchment, crests, decorative crosses, or institutional imitation. |
| RA-06 | Literal global shell on Liturgy | Preserve the protected four-action adapter and first viewport. |
| RA-07 | Calling a bounded title fixture Search | It remains Jump until J0–J2 prove real typed corpus coverage. |
| RA-08 | Flattening Work/Edition/Artifact/Segment/Passage | Preserve explicit object identity for citation and rights truth. |
| RA-09 | Merging provider outputs or calling them Source Editions | Show Independent treatments with explicit provider metadata; use Parallel treatment only for a proven relationship. |
| RA-10 | Digest-first Source interface | Human identity and material availability precede hashes and technical provenance. |
| RA-11 | Generic related recommendations | Display only deterministic structured relationships. |
| RA-12 | Framework or IIIF migration as foundation work | Preserve the static architecture and add a viewer only for a justified witness. |
| RA-13 | Freezing prototype typography, spacing, masthead density, or breakpoints | Semantic roles are accepted; exact pixels must be proved with real content. |
| RA-14 | Hiding rights or absence to simplify the interface | Required acknowledgement and typed absence remain immediate. |
| RA-15 | Treating missing relationship data as design permission | Record the opportunity; do not fabricate the edge. |

## Operational boundary

This design contract does not authorize a broad architecture rewrite, changes
to the protected liturgy family, integration to main, or public cutover.
Feature and integration branch checkpoints may be committed and pushed within
the authority recorded in the master plan, but main integration and Pages
publication remain later explicit decisions. Parallel lanes use separate full
checkouts and never share a working directory or index.

## Wave 1 correction acceptance record

C0, C1, D0, and E0 are accepted and were not reopened by the correction
checkpoint. Independent review of the corrected F0 and shared shell answered:

1. **Sources:** Does the interface express Work → Edition ownership while
   keeping Artifact, Segment, and Passage as edition-owned siblings, with the
   Passage's controlling Artifact identified directly or through Segment?
2. **One-Passage state:** When the selected Edition has one Passage, are the
   selector and exact `Passage 1 of 1` retained while impossible Previous and
   Next actions are omitted?
3. **Wide shell:** Does each wide surface show exactly one current-location
   signal and a meaningful bounded Browse control rather than a duplicated
   domain label plus generic Menu?
4. **Compact shell:** At 393px and 320px, do the domain label, Menu, and bounded
   Jump remain visible, named, operable, and free of clipping or overflow?
5. **Preservation:** Are the four accepted compositions, protected Liturgy,
   PDFs, routes and hashes, real-data boundary, and epistemic states unchanged?

Independent review recorded accepted dispositions for F0 and the shared shell
in the roadmap and operational ledgers. The accepted answers preserve the
exact contracts above; they do not accept production implementation or
authorize integration, deployment, or cutover.

## World-class completion

The corpus experience is complete only when every public route is assigned an
archetype and owning object model; every supported object has truthful
identity, availability, source, and citation behavior; cross-corpus
relationships are typed and auditable; global discovery works across public
corpus types without leakage; canonical PDFs remain obvious; all current paths
have a compatibility disposition; and the release passes deterministic
generation, route/state/browser/accessibility/performance/visual checks plus
independent product, source, rights, and release review.

Visual coherence alone is not completion. Neither is an accepted foundation
prototype. Real production surfaces retain independent visual acceptance gates,
and integration or deployment has its own authorization and evidence.

## Change control

Amend this document only for a deliberate site-wide product or visual decision
or an accepted real-route design contract. Put surface-specific semantics in
the owning guidance, observed route facts in the corpus inventory, technical
architecture in the implementation guidance, and execution progress,
limitations, evidence, next actions, and review disposition in the roadmap.
Record material rejected directions and their compatibility consequences here
rather than leaving them in chat or temporary continuity.
