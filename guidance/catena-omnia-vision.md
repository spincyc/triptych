# Catena Omnia — complete product vision

## Status, authority, and relationship to existing guidance

This document records the complete long-horizon product vision for **Catena
Omnia**, Triptych's Scripture-and-commentary instrument. It is intentionally
ambitious. It describes the destination that incremental corpus, source,
interface, and relationship work should converge toward without pretending that
the present corpus already realizes it.

This document is Catena-specific product guidance. It does **not** silently
supersede the authorities that already own adjacent concerns:

- `guidance/corpus-browser-master-plan.md` owns program boundaries, sequencing,
  protected-surface rules, and integration authority;
- `guidance/corpus-browser-vision.md` owns the shared non-PDF product and visual
  language;
- `guidance/corpus-browser-roadmap.md` owns the accepted corpus-browser work-unit
  state;
- `guidance/corpus-browser-implementation.md` owns the current implementation
  seams, defects, and hardening sequence;
- `guidance/catena.md` owns Catena's fragment, locus, chronology, rights, and
  rendering semantics;
- `guidance/liturgy-browser-vision.md` owns the protected Day and Propers reader;
- source-library, versification, chronology, Bible, rights, release, and
  publication guidance retain their existing authority.

Where this vision conflicts with one of those more specific or already accepted
authorities, the existing authority wins until an explicit amendment reconciles
the conflict. This file is therefore a durable north star and a constraint on
future Catena work, not a back door around accepted review or ownership.

The recovered baseline for this vision is `main`
`09437907472581df4a8969010bd494249a3539a5`, where Catena E1 is merged and
release-bound. The accepted E0 composition and E1 behavior are treated as
closed product work, not as a prototype waiting to be redesigned. The E1 merge
validation recorded 1,351 fragments, one solved commentary book, and a 73-entry
canonical Bible inventory. Those figures are historical evidence, not constants;
future work must rederive live counts from the corpus instead of copying them
from this paragraph.

## Mission

**At any exact place in Scripture, a reader should be able to encounter the
biblical text as text, then walk the historical chain of commentary that
Triptych actually holds on that place — oldest voice forward — and move from
any claim to the exact work, edition, witness, rights state, and source evidence
that makes it publishable.**

The goal is not merely to aggregate quotations. The goal is to make the
tradition surrounding Scripture navigable without flattening the differences
between Scripture, commentary, attribution, translation, edition, witness,
rights, chronology, uncertainty, and later synthesis.

Catena Omnia should become the place where Triptych's underlying corpus model is
most immediately understandable to a reader. Versification is no longer an
invisible technical concern when Augustine, Chrysostom, Aquinas, a Vulgate,
and a modern Bible use different numbering. Source identity is no longer an
internal metadata problem when the exact words on screen came from a particular
edition. Rights are no longer footer boilerplate when one translation can be
shown and another cannot. Chronology is no longer a bibliography sort when a
pseudonymous or disputed text would otherwise be put in the wrong century.

Catena should make those distinctions useful rather than burdensome.

## What “Omnia” means

`Omnia` is a horizon, not a completeness claim.

It means:

> every commentary fragment that Triptych actually holds, can lawfully publish,
> can anchor to Scripture, and can present without lying about identity or
> uncertainty, across the whole canonical corpus.

It does **not** mean:

- every commentary ever written;
- every Father, Doctor, theologian, exegete, or school;
- every surviving language or translation;
- every fragment named by the acquisition index;
- every plausible relationship suggested by an AI model;
- every verse having commentary;
- every historical judgment being settled;
- every gap being silently filled.

A sparse chapter is truthful. An empty chapter is truthful. A chapter for which
Triptych knows of twenty relevant works but holds none is truthful when it says
exactly that. Omnia is achieved by increasing the amount of truth the corpus can
show, never by decreasing the visibility of what it does not hold.

## The larger Triptych thesis

Triptych's corpus-browser thesis is that **the corpus is the product; pages are
typed views into it**. Catena is the clearest demonstration of that idea.

The long-horizon corpus graph is not a generic knowledge graph and must never
become one. It is a set of explicit, typed, repository-owned relationships among
objects Triptych can actually identify:

```text
Scripture locus
  -> Scripture edition / projected display locus
  -> held commentary fragment
       -> commentator / attributed author
       -> commentary work
       -> source edition
       -> controlling artifact or segment
       -> rights / review / verification state

Scripture locus
  -> liturgical reading or formulary binding, where structured evidence exists
  -> historical act or change, where structured evidence exists
  -> publication treatment, where a publication explicitly binds the locus
  -> related law or other corpus object, only where a typed owner records it
```

Catena owns the Scripture-to-commentary view. It should connect cleanly to the
other views without swallowing them. Full source records belong in Sources.
Full liturgical decision chains belong in Liturgy. Full historical change
records belong in History. Canon law belongs in Law. Publications retain their
own reading surfaces. Catena links to those objects when the relationship is
known; it does not reproduce their products inside itself.

The result should feel like moving through one corpus, not being bounced among
unrelated microsites.

## The reader promise

A reader entering Catena at a stable Scripture address should be able to answer,
without guesswork:

1. **Where am I?** The biblical book, chapter, verse or range, and selected
   Bible/numbering are clear.
2. **What does Scripture say here?** The biblical text is visually primary and
   readable at a disciplined measure.
3. **What commentary does Triptych actually possess here?** Held fragments are
   presented as text; leads are not.
4. **Whose words are these?** Author, attribution status, work, text date or
   chronological basis, language/voice, and natural extent are visible.
5. **Which edition supplied these exact words?** The source edition and
   controlling evidence are reachable without turning the reading view into a
   bibliographic database.
6. **May these words be displayed and reused?** Required rights acknowledgements
   and withholding states are explicit at the point they govern.
7. **How certain is this placement?** Projection refusals, uncertain paragraph
   boundaries, disputed attribution, partial extent, and unsupported state stay
   visible as their own kinds of fact.
8. **What else in Triptych is structurally connected to this place?** Proven
   Scripture, Source, Liturgy, History, Law, and Publication transitions are
   available when the corpus actually contains the edge.
9. **Can I cite and return to this exact state?** Material semantic state has a
   stable URL and visible human locator.

No one of these answers should require the reader to understand the repository.
The repository remains available for audit, but the product should express its
truths in ordinary scholarly language first.

## The ten invariants

### 1. Scripture is the anchor

Catena begins with Scripture, not with a commentator, search result, dashboard,
or explanation of the product. The current E0/E1 decision is correct: the
current Scripture locus is the fact, and the page identity is quieter context.

Commentary may be extensive. It may visually occupy more total page length than
the chapter. It must never make Scripture feel like a metadata sidebar attached
to a commentary database.

### 2. Held text and research lead are different ontological states

The three-layer distinction from `guidance/catena.md` remains fundamental:

- **L1 attribution / acquisition lead:** Triptych has evidence that a work may
  comment on this place.
- **L2 holding:** Triptych possesses a specific work/edition/artifact under a
  known rights state.
- **L3 fragment:** Triptych possesses the actual words of a commentary fragment
  and can bind them to a canonical Scripture extent.

The default Catena chain renders L3. L1 and blocked L2 information may be useful,
but must remain visually and semantically incapable of impersonating L3.

### 3. Canonical identity precedes display numbering

A commentary fragment binds to a canonical Scripture extent. The selected Bible
is a projection of that identity, not the storage key for it. Where the
projection refuses, Catena refuses. It never substitutes “same visible number”
for a mapping the corpus cannot establish.

This principle must survive full-canon expansion, deuterocanonical books,
Psalter differences, alternate chapter boundaries, and any later Bible edition.

### 4. Store the natural extent; derive views

A fragment is stored at the extent the commentary actually addresses. Chapter,
verse, liturgical-reading, search-result, author, work, and thematic views are
derived from that one statement. A fragment spanning a chapter boundary remains
one fragment and appears under every chapter it touches at its full extent.

No future performance optimization may create a second hand-maintained truth
about fragment placement.

### 5. Chronology is a historical claim

The chain is chronological because chronology helps a reader see reception
unfold. The date used must describe the text as honestly as the corpus can:
composition/text date where established; an explicit basis where only another
date is available; deterministic ordering for ties and unknowns; pseudonymous
works placed by the text's actual historical horizon rather than a claimed
apostolic identity.

Chronology uncertainty is data, not an inconvenience to hide for a cleaner
sort.

### 6. Exact words require edition identity

An author does not own an abstract block of English prose. The exact words on
screen came from an edition, transcription, or translation. That identity must
be reachable from the fragment and must govern language, rights, provenance,
and review status.

A work title may be human-friendly. A source link may be progressively
disclosed. Neither may erase the exact edition behind the displayed words.

### 7. Rights are part of product truth

Rights attach to editions and translations, not to the age of an author.
Catena must continue to distinguish:

- readable and redistributable;
- held but withheld;
- original-language public-domain text with no lawful translation;
- partial lawful translation;
- external-only access;
- unknown or unresolved rights.

Required acknowledgement stays adjacent to the words it governs. A blocked
translation does not cause the page to borrow an unrelated translation or hide
the original.

### 8. Uncertainty has types

Unavailable, withheld, unacquired, unread, unsupported, invalid, projection
refusal, missing translation, uncertain paragraph boundary, disputed
attribution, and transport error are different states. They must not collapse
into one grey “Unavailable” treatment.

The current solid-versus-dashed visual grammar is valuable precisely because it
maps epistemic state into form rather than merely into color.

### 9. Relationships must be owned

A relationship shown by Catena must come from structured repository evidence.
A title match, shared keyword, same saint, same feast, nearby date, likely
allusion, or model suggestion is not a corpus edge.

AI may propose edges for review. It may not publish them as established
relationships until an owning schema and validation process accept them.

### 10. AI never becomes an invisible authority layer

AI is useful for discovery, transcription assistance, candidate alignment,
translation drafts, source comparison, QA, and synthesis. None of those may
silently turn into historical commentary.

If Catena later offers AI-generated synthesis — for example “compare these
Fathers,” “trace this doctrine,” or “summarize the reception of this verse” — it
must be a **separate derived treatment** that:

- identifies itself as synthesis;
- cites the exact fragments it used;
- never appears in the historical chain as though it were another commentator;
- never fills a gap by inventing what an unavailable work might say;
- preserves contrary, minority, uncertain, and untranslated evidence rather
  than smoothing it into consensus;
- can be omitted entirely without changing the underlying corpus view.

The source chain remains the authority-bearing substrate.

## Information architecture

### Public naming

The compact global navigation label remains **Commentary**. The product/page
name may remain **Catena Omnia**. This pairing solves two problems at once:
ordinary visitors can understand the destination, while the page can retain the
traditional genre name.

The page should continue to explain the term *catena* below first-useful content
rather than consuming the first viewport with a definition.

### Primary route

`/catena/` remains the durable entrance. State should be additive and
shareable. At minimum, a stable URL should identify the Scripture locus and
selected Scripture edition. Commentary voice/language belongs in URL state when
it materially changes what the page displays. Temporary disclosure openness,
scroll pixels, and incidental UI state do not need canonical URLs.

Future citation work may add a stable fragment anchor and copy-citation action,
but must preserve existing valid URLs.

### Entrances into Catena

Catena should eventually support four clean entrances:

1. **Direct Scripture address** — book/chapter/verse or stable locus.
2. **Scripture browser transition** — “Commentary on this place.”
3. **Liturgy transition** — from a reading whose exact Scripture binding is
   known, without adding Catena as permanent Liturgy chrome.
4. **Typed corpus search** — an exact citation, author, work, or fragment result
   lands at a stable Catena state.

A fifth entrance may come from a publication or historical object when it owns
an explicit Scripture relationship. “Related content” based on similarity is
not an entrance contract.

## Composition and visual identity

Catena belongs to Triptych's **Instrument** archetype but contains a substantial
Reader plane. Its visual success depends on keeping those roles distinct.

### Wide composition

The accepted E0/E1 composition is the baseline:

- Scripture forms the anchored left reading plane;
- the commentary chain occupies the adjacent principal apparatus plane;
- neither column is pinned merely to imitate a desktop application;
- commentary text receives a real reading measure;
- apparatus and controls do not squeeze Scripture into an annotation gutter.

The exact breakpoint and track sizes are not a new eternal pixel contract.
Future shared-shell changes must recapture real evidence and prove that
commentary does not visually overpower Scripture near the split threshold.

### Narrow composition

Below the content-driven split, Catena has one reading order. The Scripture
locus and its projection truth form the first reading unit: when the selected
projection carries a boundary refusal, that refusal precedes the affected
Scripture, as the accepted E1 behavior already renders it; otherwise Scripture
text comes first. Commentary follows. Acquisition leads, blocked material, and
extended apparatus remain later or under deliberate disclosure. There is no
side-by-side mobile mode, horizontal card rail, or squeezed miniature Scripture
column.

### Typography

The visual system should continue to communicate semantic kind before a reader
parses labels:

- Scripture: sustained-reading serif;
- actual commentary text: sustained-reading serif;
- commentator/work identity: restrained mixed serif/sans hierarchy;
- dates, loci, language, extent, review state, and interface labels: UI sans;
- literal identifiers: identifier role only when the machine/scholarly ID is
  materially useful.

No ornamental historical display face is required to make patristic material
feel serious. If Triptych later adopts a self-hosted reading typeface, Catena
inherits it through the separately authorized site typography work rather than
creating a Catena-only font dependency.

### Color and line grammar

Commentary's restrained violet identity may remain a section orientation cue.
It must not become a purple page theme. Near-black text, warm paper-neutral
surfaces, quiet rules, strong focus, and section ink remain dominant.

The current grammar should be preserved unless a later independent review
proves a better one:

- **solid rule / reading serif:** held commentary text;
- **dashed rule / sans:** lead, blocked, or refusal state;
- **strong notice treatment:** an actual refusal/error that changes what a
  reader may safely infer;
- **hairlines rather than cards:** continuity of a chain rather than a stack of
  unrelated widgets.

Forced-colors behavior must preserve these distinctions without depending on
violet, opacity, or background tint.

### Ornament

Do not solve “Catholic,” “patristic,” or “ancient” by adding parchment texture,
illuminated initials, ornamental manuscripts, portraits of every Father,
heraldic crests, faux marginalia, or ecclesiastical clip art.

Ecclesial credibility comes from accurate text, attribution, authority,
chronology, edition, rights, and source evidence. The interface should feel
beautiful because it is calm, proportioned, literate, and exact.

## The full feature horizon

### 1. Whole-canon reach

The 73-entry canonical inventory is the eventual navigation space. Catena must
be able to open every canonical book and chapter even when the honest result is
“no held commentary.”

Expansion should optimize two dimensions separately:

- **breadth:** more books and chapters with at least one held, publishable
  fragment;
- **depth:** more commentators, periods, languages, and works on already solved
  loci.

Neither metric alone equals quality. Ten thousand fragments in Genesis do not
make a whole-Bible Catena; one fragment per book does not make a useful one.

### 2. Original-language and translated voices

The current distinction between Scripture translation and **commentary voice**
should become a major strength.

Where the corpus supports it, a reader should be able to choose:

- the author's own language;
- one or more lawful translations;
- clearly labelled translation-of-translation cases;
- an explicit “translation unavailable” state without losing the original.

Voice is not a generic language filter. “Latin” can mean a Latin Father writing
Latin or a later Latin translation of Greek. The model must preserve that
difference.

### 3. Exact fragment citation

Every publishable fragment should eventually have a stable human citation and a
stable public anchor sufficient to return to:

- Scripture extent;
- commentator/work;
- edition;
- fragment locus;
- displayed voice;
- current public revision/as-of identity where required.

A copy-citation action should produce scholarly useful text, not merely a URL.
The URL remains the return path; the source identity remains the citation truth.

### 4. Source drill-down without losing place

A reader should be able to inspect the source path behind a fragment and return
to the same Catena location. The first disclosure should answer ordinary human
questions — edition, witness, rights, review state — and link into the Source
Library for the full record.

Digests, storage paths, retrieval machinery, and extended legal basis remain
progressive apparatus. They are available to an auditor without being the
first thing a reader sees.

### 5. Scripture-to-Catena continuity

The future Scripture product and Catena should feel like two views of the same
locus, not separate applications. A Scripture chapter with held commentary may
expose a quiet, typed transition into Catena. Catena should expose a reciprocal
route back to the plain Scripture reader.

The transition preserves the exact canonical locus and selected Bible when the
target supports it.

### 6. Liturgy-to-Catena continuity

A liturgical reading is one of the most natural entrances into the historical
commentary tradition. Once the Liturgy owner exposes an accepted context seam,
Study or Details may offer a quiet transition to commentary on the exact
Scripture binding.

This must **not**:

- add a fifth permanent primary action to Day/Propers;
- place a Catena column beside the liturgical reading;
- introduce the non-Liturgy global masthead into the protected reader;
- infer a biblical locus from visible translated prose when a structured
  binding is absent;
- lose the user's liturgical reading position when they return.

### 7. Typed search

Global Search should eventually recognize:

- canonical Bible citations;
- commentator names and aliases;
- commentary work titles;
- exact Source objects;
- fragment text where rights permit indexing it;
- language/voice;
- period/date;
- explicit relationship targets.

Exact recognizers precede lexical search. Ambiguity stays visible. Search is an
object router, not an AI answer box.

Within Catena, lightweight filtering may help a reader narrow a large chain by
held structured dimensions such as author, period, work, or voice. Filters must
not change the default truth that the chronological chain contains every
applicable held fragment.

### 8. Comparative apparatus

A later Catena may support deliberate comparison without becoming a pane farm.
Useful comparisons include:

- original commentary text and one translation;
- two translations of the same fragment;
- one commentator across a bounded Scripture range;
- two known recensions/editions of the same work where the source model owns the
  relationship;
- reception by historical period.

Comparison aligns exact identified objects. It never aligns “similar sounding”
passages by model judgment and never creates a fake synoptic relationship from
proximity alone.

### 9. Tradition threads

Triptych may eventually expose curated or generated **tradition threads** such
as a doctrine, typology, image, or recurring interpretation across Scripture.
This is one of the project's highest-potential advanced features, but it is also
one of the easiest places to corrupt the source model.

A thread is therefore a derived view over explicit reviewed edges. Every step
must identify the Scripture locus and fragment supporting it. A thread can say
“these sources are connected by this reviewed theme”; it cannot retroactively
turn the theme into the fragment's own explicit subject unless the source says
so.

AI can help propose and summarize threads. Human- or rule-reviewed structured
relationships must own publication.

### 10. Historical reception views

Once enough dated material exists, Catena can expose secondary views such as:

- earliest held witness on a locus;
- patristic / medieval / scholastic / early-modern / modern slices;
- author or school trajectories;
- disputed or changing attribution histories;
- translation history of a commentary work.

These are views over the same fragments, not alternate stores of fragment truth.

### 11. Acquisition transparency

Readers should be able to distinguish “the tradition is silent” from “Triptych
has not acquired it.” Catena should therefore retain an honest, quieter view of
known acquisition leads and blocked works.

Internally, acquisition planning should have richer coverage analytics:

- canonical breadth by book/chapter;
- held fragment depth;
- author/work diversity;
- chronological diversity;
- original-language versus translation coverage;
- rights-blocked opportunities;
- unresolved locus/attribution work;
- source verification state.

Public counts may be shown only when generated from the same release artifact
and labelled by object type. Internal planning metrics must never become public
claims accidentally.

### 12. Static-first scaling

Catena should remain compatible with Triptych's static deployment model.
Scaling from a one-book solved corpus toward whole-canon depth must be achieved
through generated, public-only indexes, bounded manifests, lazy fragment text,
cacheable immutable or revision-bound artifacts, and measured request/payload
budgets — not by assuming a server will appear later.

The current behavior of fetching fragment text when opened is directionally
right. Whole-corpus scale must benchmark:

- cold route payload;
- per-chapter manifest size;
- fragment request count;
- cache hit behavior;
- large-chain render cost;
- memory on mobile;
- search-index size;
- full-corpus generation time;
- GitHub Pages artifact size and request behavior.

Performance must be measured with real corpus growth before choosing a new
chunking scheme.

### 13. Offline and durable reading as a possible later layer

Because the corpus is static-first, a later release may support stronger
cache/offline behavior for previously visited Scripture and commentary. This is
a possible enhancement, not a current requirement. It must not create hidden
stale authority or cause an old cached fragment to appear current after a
rights or attribution correction.

Any service-worker or offline proposal therefore requires explicit revision,
cache invalidation, privacy, and release review.

### 14. Print and export

Browser print remains a non-canonical fallback. It should produce an
independently intelligible chapter/commentary reading with:

- Scripture locus and edition;
- commentary voice;
- author/work/date/extent;
- required rights acknowledgement;
- source identity sufficient to follow up;
- explicit absence/refusal qualification where needed.

Interactive controls disappear. Canonical Triptych PDFs remain the authoritative
print editions where one exists. Catena must not quietly become a second PDF
typesetting system.

Structured export may later be useful for research, but rights and public-only
filtering must govern it independently of what a browser can technically fetch.

## Acquisition philosophy

The interface will not make Catena Omnia great if the corpus remains shallow.
Acquisition is therefore a first-class product workstream, not a content chore
that begins after UI completion.

The acquisition program should prefer sources that maximize **truthful reusable
coverage**, not prestige in the abstract. Factors include:

1. redistributable rights;
2. stable obtainable witness;
3. clear work and edition identity;
4. Scripture extent that can be established without invention;
5. original-language value;
6. translation availability;
7. chronological and author diversity;
8. canonical breadth;
9. connection to commonly encountered liturgical Scripture;
10. marginal cost of verification and maintenance.

A modern copyrighted translation may be excellent scholarship and still be a
poor acquisition target for a public static corpus. A less fashionable public-
domain edition may create more reader value because Triptych can actually show
and audit it.

Acquisition must never lower the fragment acceptance bar merely to increase
counts.

## Editorial and theological posture

Catena is a Catholic project presenting the received commentary tradition in a
source-auditable way. Its interface should not constantly interrupt historical
commentary with a modern skeptical narrator, nor should it silently rewrite
historical authors into present-day theological language.

The page's job is first to **present what the source says and what Triptych can
prove about the source**. Later editorial synthesis may explain reception,
dispute, development, or ecclesial status, but it must be visibly distinct from
the historical voice.

Likewise, source honesty is not secularization. Recording a disputed
attribution, uncertain date, or unavailable translation is how the project
protects the tradition from false precision.

## Accessibility and resilience are design, not cleanup

World-class Catena means a keyboard, screen-reader, zoom, forced-colors, narrow-
screen, low-motion, and no-JavaScript user encounters the same epistemic truth
as a wide-screen mouse user.

Required properties include:

- exactly one meaningful `main` landmark in the built artifact;
- useful heading navigation with the current Scripture locus exposed;
- no document-level overflow at 320 CSS pixels;
- practical primary targets and visible unobscured focus;
- disclosure semantics that announce open/closed state;
- focus return after modal surfaces;
- one coherent narrow-screen reading order;
- no distinction encoded by color alone;
- failure states that replace false “Loading…” claims;
- no-JavaScript content that tells the truth about what is unavailable without
  scripts;
- reduced-motion behavior where any motion exists;
- print that remains intelligible without screen color.

A future feature is not complete when it looks correct in the default desktop
screenshot.

## Performance and payload doctrine

The first useful content is Scripture, not controls, analytics, source hashes,
or a search application boot sequence.

Catena should preserve:

- minimal route shell;
- generated data split by the reader's actual question;
- lazy fragment text;
- no framework dependency merely to manage state already handled by small
  route-owned code;
- no icon library;
- no external font dependency;
- no server dependency;
- no speculative prefetch of every commentary text in a chapter;
- no full-corpus search index on pages that do not use Search.

When the corpus grows enough to invalidate a current assumption, benchmark the
real failure first, then change the architecture.

## Success criteria

Catena Omnia is succeeding when all of the following move upward together:

### Corpus breadth

- more canonical books with held commentary;
- more solved chapters;
- more exact natural extents;
- fewer ambiguous/unresolved fragment placements.

### Corpus depth

- more authors and works per relevant locus;
- broader chronological representation;
- more original-language holdings;
- more lawful translations;
- more source editions with complete evidence.

### Epistemic integrity

- zero displayed L1 leads masquerading as L3 text;
- zero silent versification fallback;
- zero fragment text without edition identity;
- zero rights leakage;
- zero inferred relationship rendered as established;
- typed absences/refusals remain distinguishable;
- chronology and attribution uncertainty stay visible.

### Reader quality

- Scripture remains the immediate anchor;
- long commentary is comfortable to read;
- exact source inspection is close but not intrusive;
- mobile is one coherent reading order;
- keyboard and screen-reader workflows are complete;
- stable URLs reproduce material semantic state.

### System quality

- static build/deploy remains tractable;
- generated data and release bindings are deterministic;
- Catena regressions are caught by model, production, artifact, and browser
  gates;
- shared-shell changes prove no Catena product regression;
- source growth does not require hand-maintained duplicate placement tables.

No single headline count substitutes for these dimensions.

## Explicit non-goals

Catena Omnia is not:

- a chatbot answering Bible questions;
- a generated homily engine;
- a generic semantic-search portal;
- a crowdsourced annotation wall;
- a facsimile manuscript viewer by default;
- a social network for notes;
- an infinite dashboard of panes;
- a substitute for the Source Library;
- a substitute for the Liturgy reader;
- a reproduction of Aquinas's *Catena Aurea*;
- a claim that all historical commentary agrees;
- a claim that an acquisition lead is a text;
- a mechanism for hiding unavailable evidence behind a polished synthesis.

Features in those neighboring categories require their own product case and
must not be smuggled into Catena because the data is nearby.

## Governance and change discipline

### Closed E0/E1 product contract

The accepted Catena composition and E1 model/transport/voice/refusal behavior are
closed unless a new work unit explicitly reopens one of them with evidence.
Routine corpus expansion should not redesign the page.

### Shared foundation

Shared shell, token, accessibility, and plumbing changes may reach Catena only
through the owning foundation lane. Any such change must prove that the Catena
route preserves:

- Scripture-first hierarchy;
- held/lead/refusal distinctions;
- URL state;
- fragment fetch behavior;
- source/rights truth;
- keyboard recovery and focus visibility;
- narrow reading order;
- no horizontal overflow.

### Protected Liturgy

Catena has no authority to alter protected Day/Propers files. A future
Liturgy-to-Catena transition requires an explicit Liturgy-owned seam or
carve-out. The relationship being valuable does not grant ownership of the
surface that exposes it.

### Release

Changing a published Catena or shared source does not authorize release-binding
refresh, deployment, merge, or acceptance. Those remain distinct authorities.

## Cold review of this vision

### Method

The vision was reread as if written by another team, against the current
accepted Catena design, the corpus-browser architecture, the protected Liturgy
contract, the Source identity model, static-host constraints, and the known
B0/B1 foundation state. The review looked specifically for ambition that would
silently weaken existing truth or ownership rules.

### Disposition

**ACCEPT WITH BINDING CONDITIONS — conditions incorporated into the text above.**

The vision is ambitious enough to justify a long-running program and is
coherent with Triptych's existing architecture. The strongest parts are the
Scripture anchor, the L1/L2/L3 boundary, the use of Catena as a concrete consumer
of versification/source/rights machinery, and the decision to make cross-product
navigation typed rather than recommendation-driven.

The cold review found the following risks and required the stated corrections.
They are already reflected in the final text.

| Severity | Finding | Required correction incorporated |
| --- | --- | --- |
| Major | “Omnia” could be read as a completeness claim and pressure the corpus to hide gaps. | Define Omnia as the whole-corpus horizon over held publishable fragments; require explicit gap states and generated coverage truth. |
| Major | An ambitious commentary product could visually demote Scripture once chains become large. | Keep Scripture as the first-useful-content anchor; preserve the split only while real evidence shows the commentary plane does not overpower it. |
| Major | Cross-corpus integration could devolve into model-inferred “related” links. | Permit only structured repository-owned edges; AI may propose but not publish relationships. |
| Major | AI synthesis could become visually indistinguishable from historical commentary. | Make synthesis a separate derived treatment that cites fragments and is never inserted into the chronological chain. |
| Major | Whole-canon growth could overwhelm the current static transport model. | Require a scale benchmark before chunking changes and preserve static-first, lazy, public-only artifacts. |
| Major | Liturgy integration could violate the protected four-action reader and become a second apparatus pane. | Require a Liturgy-owned Study/Details seam; forbid a fifth action, new masthead, or Catena pane in the protected reader. |
| Major | Acquisition could become a prestige-driven book-collection exercise disconnected from publishable reader value. | Make rights, stable witness, exact locus, breadth/depth, and verification cost first-class acquisition criteria. |
| Moderate | Chronological sorting can falsely imply precise composition dates or orthodox historical order. | Treat chronology as a stated historical claim with explicit basis, pseudonymous handling, ties, and unknowns. |
| Moderate | “Language filter” language can conflate original voice and later translation. | Preserve commentary voice as a first-class axis distinct from bare language code and Scripture translation. |
| Moderate | Advanced comparison and thematic views could create duplicate stores of placement truth. | Require all alternate views to derive from the one natural-extent fragment record and reviewed edges. |
| Moderate | Source transparency could overload the reading view with hashes and legal metadata. | Keep human source/rights identity immediate and extended technical apparatus progressively disclosed. |
| Moderate | Accessibility and performance could be postponed until the corpus is larger. | Make them continuous acceptance properties for every growth wave, not a final cleanup phase. |
| Minor | Traditional visual styling might seem like the obvious way to signal patristic seriousness. | Explicitly reject faux manuscript ornament as a substitute for source credibility; retain restrained editorial design. |

### What the cold review deliberately did not change

It did **not** reopen the accepted E0/E1 visual composition, replace the wide
Scripture/chain relationship, invent a framework, propose a webfont, redesign
protected Liturgy, merge Search into Catena, or turn the page into a general
research dashboard. Those would be new product decisions, not completion of
this vision.

## Independent cold disposition, 2026-08-30

An independent review at exact branch head
`407dfad76061460e1b3f5e3ad65ea41c73c5f746` returns
**ACCEPT_WITH_CORRECTIONS** for this vision. The correction is the narrow-order
sentence above: the accepted E1 renderer places a projection-boundary refusal
before the affected Scripture, so a blanket promise that every refusal followed
Scripture contradicted the closed product behavior this document says it
preserves. This is a guidance correction only; no Catena production source,
generated data, release record, or accepted E0/E1 behavior changed.

With that correction, the vision:

- treats Omnia as a whole-corpus horizon over held, publishable, exactly anchored
  commentary rather than as a completeness claim;
- keeps canonical Scripture identity, natural commentary extent, exact edition,
  rights, voice, chronology, and L1/L2/L3 state distinct;
- permits only typed, repository-owned relationships and keeps the protected
  Liturgy surface behind its own owner and seam;
- makes any AI synthesis a late, optional, separately labelled derived treatment
  over cited fragments, never another voice in the historical chain.

## Final north star

The mature Catena Omnia should feel simple on first contact and almost
bottomless on inspection.

A reader opens a biblical place. Scripture is there. The historical voices that
Triptych truly holds follow in time. Every voice has a name, work, extent,
language, date basis, edition, rights state, and path back to evidence. Gaps are
named. Refusals are named. The reader can move outward into the rest of Triptych
only along relationships the corpus can prove.

The ambition is not to make the interface appear omniscient.

The ambition is to make an enormous body of Catholic scriptural reception
**legible, connected, beautiful, and auditable without ever pretending to know
more than the sources establish.**
