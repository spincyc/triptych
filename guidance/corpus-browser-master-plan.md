# Triptych — World-Class Corpus Web Experience
## Master multi-agent plan and execution instructions

**Purpose:** transform the non-PDF Triptych web experience into a coherent, world-class scholarly corpus interface while preserving the PDFs as the canonical printable editions.

**Agent split**
- **Codex = product / visual / interaction design owner.**
- **Claude = production implementation / coding / test owner.**
- Codex may create disposable prototypes and test fixtures when necessary to communicate a design, but it must not become the owner of production application logic.
- Claude must implement the accepted design contract faithfully and must not casually redesign it during coding. If implementation uncovers a design conflict, record the conflict and return it for Codex disposition rather than silently changing the product.
- Both agents must persist durable knowledge, plan state, discoveries, decisions, blockers, and acceptance status in tracked repository files and commit coherent checkpoints.

This document is the **starting instruction packet**. Before doing work, each agent must inspect the repository's current tracked guidance and reconcile this plan with the live repository state.

---

# 1. Mission

Triptych should become a source like no other: not merely a library of PDFs or a collection of browser tools, but a **single navigable scholarly corpus** in which a reader can move naturally among:

- a publication;
- the source passage behind a claim;
- the work, edition, artifact, and rights state behind that passage;
- Scripture and commentary connected to it;
- a liturgical use of it;
- the historical act that changed it;
- a canon affected by it;
- independent GPT / Claude treatments of the same work, and the
  parallel-treatment relationship where two are intentionally connected;
- printable canonical PDFs;
- stable URLs that function as citations.

The central design principle is:

> **The corpus is the product. Pages are views into it.**

The current liturgical reader is the visual benchmark, not a one-off exception. Its strengths—calm reading, disciplined measure, restrained chrome, useful first viewport, source honesty, responsive reflow—must become a site-wide design language without forcing every scholarly instrument into the same layout.

PDFs remain the canonical printable editions. **Do not redesign or mutate PDF typography, pagination, or print semantics as part of this project unless an explicitly separate task says so.**

---

# 2. Non-negotiable repository rules

Before changing anything, read and obey at minimum:

1. `AGENTS.md`
2. `PROJECT-WORK.md`
3. `promised-deliverables.toml`
4. `guidance/the-shape.md`
5. `guidance/repository.md`
6. `guidance/editorial.md`
7. `guidance/external-review-handoffs.md`
8. `guidance/web-data.md`
9. `guidance/web-editions.md`
10. the profile/guidance owning the surface being touched.

For liturgy:
- `guidance/liturgy-browser-vision.md`
- `guidance/liturgy-browser-roadmap.md`
- `guidance/liturgy-reader-state.md`
- any specific liturgical profile named by `AGENTS.md`.

For Catena:
- `guidance/catena.md`
- `guidance/reading-plan-for-agents.md`
- `guidance/bibles-for-agents.md`
- `guidance/versification.md`.

For Source Library:
- `guidance/sources.md`
- relevant rights / edition guidance.

For history and law:
- `guidance/act-histories.md`
- `guidance/time-machine.md`
- applicable law/source guidance.

The current repository explicitly treats external visual/product/architectural acceptance as an evidence handoff problem. Follow `guidance/external-review-handoffs.md` exactly unless this plan explicitly tightens it.

---

# 3. Working-directory / branch discipline

Do **not** use Git worktrees.

For parallel work, use **separate full repository directories with separate branches**. One agent task owns one branch and one checkout directory at a time. Never let two agents share one working directory or one index.

Suggested names:

```text
triptych-codex-foundation/       branch: ux/foundation
triptych-codex-catena/           branch: ux/catena
triptych-codex-sources/          branch: ux/sources
triptych-codex-library/          branch: ux/library
triptych-codex-history-law/      branch: ux/history-law
triptych-codex-scripture/        branch: ux/scripture
triptych-codex-search/           branch: ux/search

triptych-claude-foundation/      branch: impl/foundation
triptych-claude-catena/          branch: impl/catena
...
```

A task may start from `main` or from a specifically named accepted foundation commit. Record the exact base SHA in the durable plan and in every handoff.

Never merge unrelated branches just to get a preview. If a composed integration preview is needed, create a dedicated integration branch and record exactly what was merged into it.

---

# 4. Durable project memory

Create or update these tracked authorities early, before substantial implementation.

Two of them already exist. A0–A4 were executed and accepted in the coordinator review of 2026-08-08, and `guidance/corpus-browser-vision.md` and `guidance/corpus-browser-roadmap.md` were written on the Codex design branch `ux/foundation`. They are brought across by the shared-foundation integration step in that review, not written a second time. §4.1 and §4.2 below state what those documents must contain, and remain the standard they are held to.

## 4.1 Site-wide product vision
Create:

```text
guidance/corpus-browser-vision.md
```

It should become the governing site-wide product / visual / interaction architecture for every non-PDF public surface.

It must define:
- corpus-wide information architecture;
- global navigation;
- visual language;
- typography;
- reading surfaces;
- data-dense research surfaces;
- search and discovery;
- source/provenance presentation;
- edition / rights presentation;
- responsive behavior;
- accessibility;
- URL/citation behavior;
- performance;
- relationship to canonical PDFs;
- anti-patterns;
- definition of world-class completion.

It must explicitly state that the more specific `liturgy-browser-vision.md` continues to govern liturgical semantics and behavior. The site-wide vision must **reuse**, not weaken, its accepted principles.

## 4.2 Execution roadmap
Create:

```text
guidance/corpus-browser-roadmap.md
```

This is the live execution ledger. Every work unit below gets:
- ID;
- owner agent;
- state;
- base commit;
- branch;
- dependencies;
- acceptance gates;
- evidence handoff;
- accepted/rejected disposition;
- follow-up findings.

## 4.3 Operational project register
Update:

```text
PROJECT-WORK.md
```

with a concise top-level corpus redesign entry and links to the two tracked authorities above. Do not duplicate the entire roadmap there.

## 4.4 Continuity record
A continuity record may live under `build/agent-continuity/...` and hold handoffs, screenshots, logs, and in-flight state. It may never be the only owner of a fact a future agent needs, and force-tracking such a file does not make it durable. Amendment D10 lists where durable truth for this project belongs; anything the continuity record knows that a future agent needs is written there too.

The continuity record must always answer:
- what is being attempted;
- what is complete;
- what is not complete;
- what was learned;
- exact current branch/SHA;
- exact next action;
- any known failed approach;
- current external-review disposition.

Never leave decisive knowledge only in chat, terminal scrollback, an ignored ZIP, or an agent's memory.

---

# 5. Research synthesis: what to borrow, what not to copy

The design should study successful scholarly/reference systems without cloning any one of them.

## Sefaria
Useful ideas:
- source text remains primary;
- linked commentary appears contextually;
- a resource/connection panel lets the reader pivot by relationship type;
- a library can expose both texts and interconnections as first-class data.

Triptych opportunity:
- go beyond generic "connections" by showing the **typed evidentiary chain**: work → edition → artifact → passage → claim/use/change.

Reference:
- https://www.sefaria.org/
- https://help.sefaria.org/hc/en-us/articles/18472472138652-Quick-Guide-Meet-the-Sefaria-Library-Resource-Panel
- https://developers.sefaria.org/docs/commentaries

## Perseus / Scaife Viewer
Useful ideas:
- work/edition/translation identity is explicit;
- stable text navigation;
- deep philological reading tools can be adjacent to text without making the base text disappear;
- corpus browsing and text searching are distinct but connected tasks.

Triptych opportunity:
- make edition identity, rights, provenance, citation loci, and source transitions even more explicit and visually coherent.

References:
- https://scaife.perseus.org/
- https://www.perseus.tufts.edu/
- https://perseus.pubpub.org/

## Digital Vatican Library / IIIF
Useful ideas:
- treat exact artifacts as first-class objects, not just "documents";
- high-resolution witnesses can be presented with durable metadata and interoperable identity;
- IIIF is worth designing toward if manuscript/image witnesses become important.

Triptych opportunity:
- do **not** prematurely implement IIIF unless actual artifact needs justify it, but keep the source-library information architecture compatible with exact-witness viewing.

References:
- https://digi.vatlib.it/
- https://iiif.io/

## Corpus Thomisticum
Useful idea:
- a corpus can be organized around scholarly addressability and cross-reference rather than magazine-like presentation.

Triptych opportunity:
- retain this rigor while dramatically improving orientation, readability, responsive behavior, and discovery.

Reference:
- https://www.corpusthomisticum.org/

## Accessibility / readable long-form references
Normative / strong implementation guidance:
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- WAI APG: https://www.w3.org/WAI/ARIA/apg/
- GOV.UK layout: https://design-system.service.gov.uk/styles/layout/

Retain the liturgical reader's existing accessibility commitments: semantic structure, keyboard operation, visible focus, reflow at 320 CSS px, 200% text enlargement, 400% zoom, forced colors, reduced motion, usable mobile targets, and no color-only semantics.

---

# 6. Target product architecture

Triptych should feel like one place with several purpose-built scholarly instruments.

## 6.1 Global corpus shell
Every non-PDF browser page **outside the protected liturgy reader** should share:
- compact Triptych identity;
- clear current-domain identity;
- global corpus search / jump;
- predictable access to the top-level corpus destinations — Publications, Sources, Scripture, Liturgy, History, Law, Commentary — with the Triptych wordmark itself acting as the Home affordance and a separate visible Home item optional;
- a persistent but quiet way to reveal related corpus objects;
- stable footer/legal/feedback treatment;
- consistent focus and responsive behavior.

The shell must remain **quiet**. Do not turn every page into a dashboard.

### The protected liturgy exception

Canonical Day and Propers are a protected surface family, and the requirement above does not reach them. On those routes, amendment D2 forbids merging site-wide Search into the reader shell, forbids a literal corpus masthead above the accepted reader, and forbids both a fifth primary reader action and a second competing modal owner. It also holds `reader-shell.js`, `reader-instrument.css`, and the canonical `liturgy/day.html` and `liturgy/index.html` source ownership closed to this project.

The corpus project may design a future low-chrome corpus exit or context affordance for liturgy, but it must enter through an already accepted seam — Details, or a quiet terminal/footer treatment — and must take its own liturgy-specific visual acceptance. The accepted first viewport remains sacred.

This exception holds while the Live Reader — Ritual Flow & Orientation deliverable is open (D18). It is the one place in this plan where the site-wide shell yields to a more specific accepted design rather than the other way round, and a lane that finds it inconvenient returns a blocker rather than an edit.

## 6.2 Home: "the corpus map"
The current homepage is a good inventory but visually functions as lists and tables. Replace the experience with an editorially calm **map of the corpus**:
- one strong statement of what Triptych is;
- immediate entrances by task, not just section;
- "Read today", "Find a text", "Trace a source", "Follow commentary", "See what changed", "Look up a canon";
- the seven existing editorial portals below or beside the task entrances, keeping their current names, order, and colour identities;
- visible corpus scale only when it is accurate and generated;
- recent/featured material only if repository truth supports a deterministic rule—no hand-curated fake freshness;
- clear distinction between browser instruments and canonical PDFs.

The seven portals are durable corpus orientation, not decoration to be discarded for the sake of a new-looking homepage. They survive unless real-data evidence proves a materially better alternative, and changing the portal table is an amendment to `guidance/repository.md` landed in the same commit. Do not silently break the generator's `README.md` preamble transform (D7).

## 6.3 Section libraries / Every Document
The section pages and `Every Document` should become a strong **catalogue and collection browser**, not HTML tables disguised as a website.

`/texts/` carries **Publications** as its compact global label in navigation. The route is not renamed and no second canonical publication home is created (D1).

Requirements:
- faceted filters;
- fast search;
- group by subject / series / section;
- strong publication title;
- concise abstract;
- provider shown as explicit metadata, alongside revision identity;
- length/revision metadata;
- obvious Read vs PDF;
- paired GPT/Claude issues presented as **parallel treatments** of one work rather than as independent random links;
- responsive list-first presentation;
- optional dense/table view for power users;
- stable URLs for filter state where useful.

Two rules govern how those pairs are named and owned.

**They are treatments, not editions.** *Independent treatment* is the human-facing label when distinguishing separately produced GPT and Claude treatments; *parallel treatment* is the relationship label when two treatments of the same work are intentionally connected. The provider is always explicit metadata, never jargon baked into the relationship name. Never call these Source Library editions unless they actually satisfy the edition model in `guidance/sources.md` (D3).

**A faceted catalogue is a discovery view, not a second ownership hierarchy.** It may reveal every relevant treatment and format, but each publication keeps exactly one owning catalogue and one canonical PDF home (D8).

## 6.4 Browser-readable publication pages
All generated "Read" versions of papers should receive a world-class long-form reader:
- controlled measure;
- meaningful heading hierarchy;
- location-aware TOC;
- footnotes/citations that are easy to inspect and return from;
- source links that open contextual detail without losing position;
- provider shown as explicit metadata, alongside revision identity;
- canonical PDF action;
- previous/next only when a real series/order exists;
- print CSS may be useful, but the PDF remains the canonical printable edition;
- side-by-side comparison of two provider treatments may be a later capability, but the architecture should allow it.

`guidance/web-editions.md` is controlling for this lane (D9). Never create a second editable copy of publication prose. Do not edit `web/<provider>/*.md` merely to achieve a UI presentation. Preserve the visible rights colophon and the revision identity, declare any material omission explicitly, and re-run the web-edition currency checks after a renderer or converter change.

## 6.5 Catena Omnia
The Catena should become a signature experience.

Wide screen:
- principal Scripture text as the anchor;
- commentary visually forms a **chronological chain** beside or immediately following the relevant extent;
- a restrained vertical chronology spine may be used;
- author/date/work/edition are easy to scan;
- commentary fragments remain distinct from mere attribution/acquisition leads;
- multilingual/original-language state is explicit;
- opening a fragment does not destroy reading position;
- connections to Source Library are one action away.

Mobile:
- one column;
- Scripture extent followed by the commentary attached to that extent;
- no two-column squeeze;
- chronological ordering remains obvious;
- disclosures preserve location.

Do not make every fragment a giant card.

## 6.6 Source Library
The Source Library should become Triptych's **evidence observatory**.

Core mental model must be visually obvious:

```text
Work
  └─ Edition
      └─ Artifact
          └─ Passage
```

Recommended experience:
- global search + faceted discovery;
- list results with enough identity to distinguish near-duplicates;
- work detail page/panel;
- edition selector/timeline;
- artifact provenance and checksum as inspectable metadata, not primary visual noise;
- passage navigator;
- rights state and distribution basis are visible and unambiguous;
- "used by" / "cited by" / "comments on" / "governs" relationships when backed by structured data;
- exact downloadable/viewable source actions only when rights permit;
- withheld passages remain visible as records with the reason.

This is not a generic document repository. The object graph is the differentiator.

## 6.7 How the Missal Changed
Preserve the "Missal Line" concept but make it feel like a serious historical instrument:
- strong horizontal/vertical timeline depending on viewport;
- stations clearly distinguish promulgated acts from weaker printed witnesses;
- selection opens a focused change narrative;
- follow-one-prayer mode should feel like tracing a lineage;
- before/after semantic units should be readable, not raw diff noise;
- broken connectors and evidentiary uncertainty are visually meaningful without relying on color alone.

## 6.8 Canon Law
Design around the actual scholar/user entrance: **the citation**.
- canonical citation box is primary;
- Code structure becomes a navigable tree/outline;
- canon text/history/acts are coherent tabs or views, if APG-compliant tabs are the right pattern;
- temporal changes read as a legal timeline;
- unavailable copyrighted words are clearly distinguished from unread or unchanged text;
- acts can be entered from either the canon or act direction;
- copied URL should remain a citation-quality deep link.

## 6.9 Story of Salvation
Turn the current plan into a genuine **reading journey**:
- three depths are an explicit progression, not merely links;
- show current/selected translation;
- scripture books/epochs give orientation;
- local reading progress is deferred from the foundation wave (D16); if it returns later it is storage-optional, never an account, and an explicit URL always wins;
- printable PDFs remain canonical;
- chapter/reading links should pivot naturally into Catena and Source Library.

## 6.10 Global cross-corpus search
This is a major differentiator and should be architected even if delivered incrementally.

One search affordance should eventually be able to return typed results:
- publication;
- work;
- edition;
- artifact;
- passage;
- Scripture citation;
- Catena commentary fragment;
- liturgical formulary;
- historical act;
- canon.

Results must **not** flatten these into one undifferentiated list.

Each result says what kind of thing it is, why it matched, and what the user can do next.

Potential shortcut:
- desktop command/jump palette;
- mobile full-screen search sheet.

Do not ship a fake "global search" that only searches page titles.

The Jump fixture in the accepted shell interaction spec is a bounded demonstration of interaction grammar, not this capability. Production Search is delivered as J0 → J1 → J2, and no route may present a title fixture as global search (D13). The search entry point also does not enter the protected liturgy reader shell; see §6.1.

---

# 7. Visual language

Codex owns the exact design system, but it should begin from these constraints.

The accepted direction is warm paper, near-black text, a restrained oxblood accent, a blue focus ring, a disciplined serif reading axis, a UI sans stack, square and quiet controls, rules rather than card walls, and restrained chrome. These are token **roles, not frozen pixels** (D5): exact type sizes — especially very large display headings — exact desktop masthead density, and exact spacing values may all move once real-data screenshots exist.

## Character
- serious but not austere;
- ecclesial without faux-medieval decoration;
- scholarly without looking like database admin software;
- contemporary without "startup SaaS" cards everywhere;
- warm and readable rather than sterile;
- restrained liturgical/source red as semantic accent, not wallpaper;
- typography carries most hierarchy.

## Typography
- optimize primary reading surfaces around ~60–72 characters per line;
- body text effectively at least 16px;
- long-form line-height around 1.5 or better;
- left aligned, not forced justification;
- Greek, Latin, Hebrew, and special symbols must have excellent fallback behavior;
- tabular numerals where dates/canons/verse references benefit;
- metadata visibly subordinate but never illegible;
- no production design may depend on a webfont, or on any particular face being installed. Use robust system/local fallback stacks unless a separately authorized font + rights + generator work unit proves a self-hosted face worth its cost (D5, D12);
- typography is not settled until it has been tested against long real titles, multilingual text, Latin, polytonic Greek where applicable, narrow screens, and Windows, Linux, and macOS fallback.

## Surfaces
Use three related surface archetypes rather than one universal layout:

1. **Reader** — papers, Scripture, liturgy, passages.
2. **Catalogue** — Home, sections, Every Document, search.
3. **Instrument** — Catena, Source Library, Missal history, Law.

They share identity, tokens, spacing logic, accessibility behavior, URL discipline, and contextual-navigation grammar. They do not share one universal layout (D4); each has purpose-built composition.

## Cards
Cards are allowed only when a bounded object genuinely benefits from containment.
Do not turn:
- every paragraph;
- every Proper;
- every commentary fragment;
- every source;
- every filter result
into floating rounded rectangles.

## Ornament
Use iconography/symbols only when they clarify domain or state. No icon library: a mark is drawn in CSS, or in inline markup the generator already accepts (D12).
Avoid decorative pseudo-manuscript texture, fake parchment, excessive crosses, illuminated initials, page-turn effects, glowing gradients, and ornamental borders that reduce scholarly credibility.

---

# 8. Full parallel execution plan

The table is intentionally segmented so independent branches can move concurrently once their small shared dependencies are sealed.

| ID | Segment | Agent | Parallel lane | Depends on | Primary output | Acceptance evidence |
|---|---|---|---|---|---|---|
| A0 | Repository/site inventory | **Codex** | Foundation | none | complete route/surface matrix; screenshots; design debt map | ZIP with route inventory + representative captures |
| A1 | Corpus UX research synthesis | **Codex** | Foundation | none | precedent analysis + Triptych-specific principles | `sources.md`, design memo, explicit recommendations |
| A2 | Site-wide product vision | **Codex** | Foundation | A0/A1 | `guidance/corpus-browser-vision.md` | tracked commit + review ZIP |
| A3 | Design tokens + three archetypes | **Codex** | Foundation | A2 | visual system prototype for Reader/Catalogue/Instrument | desktop/mobile/zoom captures |
| A4 | Shared shell interaction spec | **Codex** | Foundation | A2 | global nav/search/related-object shell prototype | keyboard/mobile/overflow evidence |
| B0 | Shared shell implementation | **Claude** | Foundation | accepted A3/A4 | shared CSS/JS/HTML primitives | tests, a11y checks, screenshots |
| B1 | Design-system regression harness | **Claude** | Foundation | A3 | viewport, zoom, forced colors, keyboard, console test harness | reproducible commands + logs |
| C0 | Homepage + section libraries design | **Codex** | Catalogue | A2/A3 | home + 2 representative section prototypes | before/after matrix |
| C1 | Every Document / catalogue design | **Codex** | Catalogue | A2/A3 | faceted catalogue + publication-edition presentation | filter/mobile/empty-state captures |
| C2 | Catalogue implementation | **Claude** | Catalogue | C0/C1 | production Home/sections/text catalogue | focused tests + production-like captures |
| D0 | Browser-readable paper design | **Codex** | Reader | A2/A3 | long-form article reader + citations/TOC/PDF action | long paper desktop/mobile evidence |
| D1 | Article reader implementation | **Claude** | Foundation (see below) | D0/B0 | reusable paper reader styling/behavior | sample corpus matrix |
| E0 | Catena signature redesign | **Codex** | Catena | A2/A3 | Scripture/commentary chain interaction + responsive states | multiple chapter/comment density states |
| E1 | Catena implementation | **Claude** | Catena | E0 | production Catena | model tests, DOM/a11y, real-data captures |
| F0 | Source Library evidence-observatory design | **Codex** | Sources | A2/A3 | work→edition→artifact→passage explorer | rights/readable/withheld/multi-edition states |
| F1 | Source Library implementation | **Claude** | Sources | F0 | production Source Library | data-parity tests + a11y + real records |
| G0 | Missal history redesign | **Codex** | History | A2/A3 | Missal Line + prayer lineage visual spec | branch/station/broken-line states |
| G1 | Missal history implementation | **Claude** | History | G0 | production history instrument | semantic + viewport regression |
| H0 | Canon-law redesign | **Codex** | Law | A2/A3 | citation-first canon/history/act UX | public-domain/withheld/unchanged states |
| H1 | Canon-law implementation | **Claude** | Law | H0 | production law instrument | deep-link + a11y + state tests |
| I0 | Story of Salvation redesign | **Codex** | Scripture | A2/A3 | 3-depth reading journey + pivots | desktop/mobile and all three depths |
| I1 | Scripture implementation | **Claude** | Scripture | I0 | production Scripture plan | translation + route tests |
| J0 | Global typed search architecture | **Codex** | Search | A2 + inventory | search UX, result taxonomy, command palette/sheet | query/result-state prototype |
| J1 | Search data feasibility / index design | **Claude** | Search | J0 | generated search index architecture with size/perf budget | index metrics + tests |
| J2 | Global search implementation | **Claude** | Search | J1/B0 | typed cross-corpus search | representative multi-domain queries |
| K0 | Cross-object relationship UX | **Codex** | Graph | E/F/G/H/I designs | contextual "related corpus" model | task walkthroughs |
| K1 | Cross-object link implementation | **Claude** | Graph | K0 + owning surfaces | source/catena/liturgy/history/law pivots | link integrity + deep-link tests |
| L0 | Mobile coherence review | **Codex** | Acceptance | C–K designs | site-wide 320/393/tablet review | screenshot/contact-sheet ZIP |
| L1 | Accessibility acceptance | **Claude** + Codex judgment | Acceptance | implemented surfaces | WCAG 2.2 AA evidence on core flows | keyboard/zoom/forced-color/SR notes |
| L2 | Performance acceptance | **Claude** | Acceptance | implemented surfaces | route budgets + measured regressions | reproducible performance logs |
| L3 | Visual cross-site acceptance | **Codex** | Acceptance | implementation complete | consistency audit against accepted visual contract | full route matrix ZIP |
| M0 | Integration / cutover | **Claude** | Integration | accepted lanes | clean integration branch/main commits | full gates + Pages verification |
| M1 | Final independent corpus review | **Codex** | Acceptance | M0 | world-class completion disposition | immutable final handoff ZIP |

### Parallelization rule

After **A2/A3/A4 are accepted**, lanes C, E, F, G, H, I, and much of J may run in parallel. They do not wait on B0.

Do not block a lane on unrelated surface implementation.

Codex design lanes can run before B0 is fully implemented if they all consume the same accepted token/archetype contract.

Claude implementation lanes should rebase/merge the accepted shared foundation before coding and should not each reinvent shared primitives.

**Implementation discovery, measured and accepted.** This rule previously said that lanes could begin only after B0 established the shared shell contract, and the dependency column made every implementation lane wait on B0. That sequencing was an assumption about the tree, and the implementation lane measured the tree instead. `guidance/corpus-browser-implementation.md` §17.1 records the measurement: every non-liturgy page loads exactly two things, `shared/browser-core.*` and the files in its own entrance directory, with no cross-entrance asset reference anywhere; and `browser-core.js` contains no header, navigation, footer, masthead, or breadcrumb construction at all. The shared shell is built at the generator seam, not in the shared browser core, so an instrument lane working inside its own entrance directory is not waiting on B0. The other stated reason for the dependency — promoting `reader-shell.js` into `shared/` so that lanes E, F, G, H, and I would be unblocked — was withdrawn by D2, because that file belongs to the liturgy deliverable; those five lanes were never blocked. The coordinator accepted this correction on 2026-08-08. It is a measurement from the implementation lane, not a product judgment, and it is superseded the moment the measurement stops holding.

**What stays single-owner.** Parallelism across entrance directories does not extend to shared or generated concerns. Each of the following is one owner's work, and no surface branch edits it casually:

- the generator and layout shell;
- shared site assets;
- the shared browser core;
- release-binding regeneration;
- global navigation;
- the common browser gates;
- the shared ledgers, `PROJECT-WORK.md` and `promised-deliverables.toml`.

`guidance/corpus-browser-implementation.md` §17.2 ranks the specific files that conflict and states the discipline for each; §17.4 states the filtered release-binding procedure. Read them before scheduling two lanes that might meet.

**D1 is a foundation lane wearing a surface lane's name.** Its diff lands in `tools/public-alpha` and the shared site stylesheet rather than under any entrance directory, so it is scheduled with the shell and foundation owner, not beside the instrument lanes, and it keeps its B0 dependency. J2 likewise keeps its B0 dependency, because a global search entry point is shell furniture.

---

# 9. Codex task protocol — visual/product agent

Every Codex task must follow this sequence.

## 9.1 Orient
1. Read required guidance.
2. Read site-wide vision/roadmap.
3. Inspect current production page and source files.
4. Record exact base SHA.
5. Update roadmap state to `in-progress`.
6. Create/update continuity record.

## 9.2 Audit before designing
For the owned surface:
- enumerate real user tasks;
- enumerate all meaningful data states;
- enumerate loading/empty/error/partial/withheld/unsupported states;
- inspect desktop, tablet, 393×852, 320-wide, 200% text, and representative zoom;
- identify what existing behavior is semantically required;
- identify what is merely current styling and may be discarded.

## 9.3 Design
Produce:
- one primary recommended direction;
- no "three themes, choose one" unless there is a real unresolved product fork;
- exact interaction behavior;
- responsive behavior;
- hierarchy/tokens;
- semantic component names;
- states and transitions;
- acceptance criteria.

Disposable prototypes are encouraged when they materially improve judgment. Keep them clearly outside production ownership.

## 9.4 Sanity check
Ask:
- Is the text/corpus object still primary?
- Does this look like a scholarly corpus, not SaaS?
- Can a new user understand where they are?
- Can an expert move faster than before?
- Is provenance more legible, not less?
- Are unavailable/uncertain states still truthful?
- Does mobile become a coherent single-column experience rather than crushed desktop?
- Is every added visual object earning its space?
- Are we using one of the three archetypes intentionally?
- Is a card being used only because it represents a bounded object?

## 9.5 Persist
Before handoff:
- update `guidance/corpus-browser-roadmap.md`;
- update the surface's owning guidance where a durable rule was learned;
- update `PROJECT-WORK.md` only if the top-level project state materially changed;
- commit the tracked knowledge **before** producing the handoff.

## 9.6 Return evidence ZIP
Use `guidance/external-review-handoffs.md`.

For visual tasks, the ZIP must contain:
- `HANDOFF.md`
- `REVIEW_REQUEST.md`
- `changes.patch`
- `checks.txt`
- `sources.md` when research informed the work
- `screenshots/`
- prototype files needed for review
- a route/state matrix
- before/after captures where applicable.

`REVIEW_REQUEST.md` must ask specific blocking questions. Never ask only "does this look good?"

---

# 10. Claude task protocol — implementation agent

Every Claude task must follow this sequence.

## 10.1 Orient
1. Read repository guidance.
2. Read accepted Codex handoff / design spec.
3. Read corpus vision/roadmap.
4. Inspect existing data models and tests.
5. Record exact base SHA.
6. Update roadmap and continuity.

## 10.2 Implement without semantic drift
- preserve source/data ownership;
- preserve stable URLs unless the accepted design explicitly changes/canonicalizes them;
- do not put data truth into CSS/DOM hacks;
- do not duplicate renderers where shared semantic objects exist;
- keep generated-data architecture additive;
- lazy-load heavy apparatus where appropriate;
- preserve rights/coverage distinctions;
- use semantic HTML first, ARIA only where needed;
- no root-relative link: GitHub Pages serves this site under `/triptych/`;
- no webfont, no icon library, no framework migration, and no asset type the generator will reject;
- preserve the HTML payload limits and the static, no-server deployment model (D12).

If the design cannot be implemented without violating a repository invariant:
1. stop that design choice;
2. record the exact conflict;
3. implement the largest safe subset if independently useful;
4. return a blocker for Codex.

Do not silently "simplify" the design.

Known browser-architecture debt — the oversized shared core, the duplicated history/law helpers, the hash routers that flood browser history, the nested `<main>` landmarks, the lost first-focus targets, the measured 320px overflow — is real debt and is paid incrementally, with path-specific commits and before-and-after gates. It is not authority for a browser-stack rewrite, and B0 does not become one (D17).

## 10.3 Test
At minimum, per affected core route:
- deterministic unit/model tests;
- browser rendering;
- console/request/HTTP error checks;
- keyboard navigation;
- focus visibility/restore;
- 393×852;
- 320 CSS px;
- 200% text;
- representative 400% zoom/reflow;
- forced colors;
- reduced motion where motion exists;
- print rules where relevant;
- direct deep-link startup;
- legacy URL fixtures if affected.

## 10.4 Persist and commit
Commit:
- implementation;
- regression tests;
- durable implementation discoveries;
- roadmap state;
- relevant guidance corrections.

Never make a "code only" commit that leaves the tracked plan lying about the state.

## 10.5 Evidence ZIP
Return a handoff ZIP under the standard protocol including:
- exact commit and base;
- focused patch;
- checks with numeric exit codes;
- relevant logs;
- screenshots;
- preview/start commands;
- known limitations;
- exact blocker questions, if any.

---

# 11. Evidence package standards for seamless browser review

The user will paste ZIP files back into ChatGPT for independent review. Optimize every handoff for that workflow.

## Required characteristics
- exactly one timestamped top-level directory in each ZIP;
- no credentials or machine-private data;
- no giant caches/build trees;
- no dependency directories;
- no irrelevant screenshots;
- no raw full build logs unless a failure depends on them;
- all paths repository-relative inside documentation;
- manifest/inventory of included artifacts;
- SHA-256 of ZIP recorded in final task response and optionally in `HANDOFF.md`;
- exact git SHA;
- exact base SHA;
- exact public/local routes;
- exact viewport names.

## Screenshot matrix
Use one comparable site-wide matrix unless a more specific owning surface requires more (D11). Every visually significant surface should normally include:

```text
<route>--default--1440x900.png
<route>--default--1024x768.png
<route>--default--768x1024.png
<route>--default--393x852.png
<route>--default--320x852.png
<route>--text-200pct--393x852.png
<route>--forced-colors--393x852.png
```

Also exercise, and capture where the behavior changes:
- 200% text enlargement;
- exact 320-CSS-pixel reflow;
- 400% zoom/reflow where meaningful;
- keyboard-only operation;
- forced colors;
- reduced motion;
- browser print, for surfaces where print is not explicitly delegated to the canonical PDF alone;
- no-JavaScript static truth;
- console/network/HTTP/accessible-name checks.

Do not create pixel-diff baselines before a real-data surface has independent visual acceptance.

Add state-specific captures rather than mechanically duplicating all sizes when the state—not viewport—is what matters.

For redesigns, include comparable:

```text
before--...
after--...
```

## Reviewer-oriented contact sheet
For any handoff with more than ~12 screenshots, generate:
- `screenshots/CONTACT-SHEET.png`
- `screenshots/INDEX.md`

The index maps filename → route → state → viewport → what the reviewer should inspect.

This dramatically reduces back-and-forth.

---

# 12. Design details by segment

## 12.1 Home and section libraries
Codex should specifically test:
- first-time visitor;
- returning reader who knows the domain but not title;
- user seeking today's Mass;
- user seeking a specific paper;
- user seeking "where did this claim come from?";
- user wanting all material on one subject;
- mobile navigation without scrolling through giant lists.

Do not simply replace tables with card grids.

Preferred direction:
- task entrances near top;
- domain collections below;
- list/table switch only if justified;
- generated metadata for scale and freshness;
- restrained editorial hierarchy.

## 12.2 Every Document
Must handle:
- paired GPT / Claude treatments of one work;
- one-model-only publication;
- PDF-only issue;
- browser-readable issue;
- synthesis issue;
- long titles;
- multiple series;
- revision dates;
- filters with zero results;
- deep-linked filter state;
- mobile.

Potential power feature:
- "Compare treatments" when two browser-readable provider treatments of one work exist.

Do not make comparison part of the first milestone unless data/reader architecture makes it straightforward.

## 12.3 Article reader
Codex should inspect representative papers:
- short essay;
- very long reference;
- citation-heavy study;
- tables;
- bilingual/Greek/Latin passages;
- headings 3+ levels deep;
- footnotes/endnotes;
- long bibliography.

The design must gracefully support the hardest paper, not only an ideal prose essay.

## 12.4 Catena
Must test:
- chapter with no held commentary;
- chapter with few fragments;
- dense chapter;
- overlapping extent;
- cross-chapter fragment;
- English-only;
- Latin/original plus translation;
- disputed attribution;
- known-but-not-acquired lead;
- unpublishable/withheld source;
- long fragment;
- many authors from similar period.

Visual distinction between:
- Scripture;
- actual held fragment;
- metadata/provenance;
- acquisition lead
must be immediate and not depend on color.

## 12.5 Source Library
Must test:
- one work / one edition;
- one work / many editions;
- same language / multiple editions;
- artifact with readable passages;
- artifact present but not distributable;
- passage withheld for rights;
- exact provenance/hash inspection;
- work used in multiple Triptych products;
- author with many works;
- search alias;
- unknown/unsettled rights.

Codex should prototype a "progressive disclosure" model so hash/legal detail is fully available but not the first thing ordinary readers confront.

Progressive disclosure has a floor (D15). It may defer hashes, extended artifact provenance, long rights and legal apparatus, and secondary technical metadata. It may never defer or erase a required licence acknowledgement at the point of use, a withheld-text reason, a typed absent / unread / unsupported / invalid state, or the distinction between availability and redistribution rights. Every renderer preserves these semantically, not only through colour or a CSS class.

## 12.6 History
Must test:
- simple linear succession;
- branch;
- missing intermediate edition;
- promulgated act;
- printed witness only;
- many changed units;
- prayer appears/disappears/reappears if corpus permits;
- mobile lineage.

## 12.7 Law
Must test:
- exact canon;
- subsection citation;
- invalid citation;
- canon never changed;
- canon changed multiple times;
- text readable;
- text withheld by rights;
- unread canon;
- act touching one canon;
- act touching an entire Book.

## 12.8 Search
Typed result taxonomy should be explicit, e.g.:

```text
PUBLICATION
SOURCE WORK
SOURCE EDITION
SOURCE PASSAGE
SCRIPTURE
COMMENTARY
MASS / FORMULARY
ACT
CANON
```

Result groups should be rankable but never semantically flattened.

Search should understand identifiers/citations especially well:
- `John 20:6-7`
- `c. 1095 §2`
- stable source IDs
- Mass keys/slugs
- known aliases/titles.

---

# 13. Cross-corpus relationship model

A signature Triptych capability should be a consistent way to answer:

> **What else in the corpus is connected to what I am reading?**

Do not implement this as a generic AI recommendation engine.

Use only structured, auditable relationships.

**Provable today.** These categories exist in the corpus and may be shown now (D14):
- explicit containment;
- passage → artifact / segment;
- Catena fragment → Scripture locus;
- Catena passage → Source Library passage;
- act descent, change, and history;
- document → catalogue page;
- Mass → propers → Scripture resolution.

**Not to be synthesised.** `translation_of`, `used_by`, `derived_from`, canon correspondences, Law → Source citations, and any generic "related" recommendation inferred from title or keyword similarity are prohibited until the corpus can prove them. A new relationship is a schema and generator work unit under the owning corpus guidance *before* it is a UI feature. An edge that resolves successfully and wrongly is the governing failure of this library; see `guidance/the-shape.md` §1.

The candidate vocabulary, from which a proven edge takes its name:
- `cites`
- `quotes`
- `comments_on`
- `translation_of`
- `edition_of`
- `artifact_of`
- `passage_of`
- `used_by`
- `governs`
- `changes`
- `supersedes`
- `compares`
- `appointed_in`
- `discussed_by_publication`

The UI may summarize these into human categories:
- Sources
- Commentary
- Liturgical uses
- Changes
- Law
- Publications

But the underlying type must remain known.

Codex designs the interaction.
Claude verifies what structured edges actually exist and implements only real ones.

---

# 14. Search/index technical direction for Claude

Do a feasibility study before committing to architecture.

The site is GitHub Pages, so global search should preferentially remain:
- static/generated;
- cacheable;
- deterministic;
- versioned with the corpus;
- no server dependency required for the core product.

Investigate:
- generated compact JSON index;
- split per entity/domain if size requires;
- pre-normalized search keys;
- citation recognizers before generic fuzzy search;
- lazy-loading result detail;
- route-specific deep links;
- language-aware normalization without destroying Greek/Latin identifiers.

Measure:
- compressed index size;
- parse time;
- main-thread cost;
- query latency;
- memory on representative mobile hardware.

Do not add a heavyweight framework/search library without measured need.

---

# 15. Accessibility gate

The site-wide redesign targets WCAG 2.2 AA across core workflows.

Required manual/mechanical evidence:
- landmarks/headings make sense with CSS disabled;
- all forms have labels;
- all interactive controls have accessible names;
- disclosure state is programmatic;
- modal/sheet focus is trapped/restored appropriately;
- no hidden content remains focusable;
- no sticky UI obscures focused elements;
- target size/spacing is practical on touch;
- no horizontal page scroll at 320 CSS px except genuinely two-dimensional content that transforms appropriately;
- 200% text and 400% zoom preserve function;
- forced colors preserve semantic boundaries;
- reduced motion respected;
- loading/status updates do not spam screen readers;
- tables retain proper semantics when tables are actually the correct structure;
- visual state is never color-only.

---

# 16. Performance gate

Preserve the accepted liturgical reader performance philosophy across the site.

Each route should have a measured baseline and budget.

Priorities:
- real useful content in first viewport;
- avoid loading source detail the reader has not requested;
- avoid shipping the entire corpus to render one page;
- lazy-load commentary fragment text only as allowed by existing Catena semantics;
- split global search/index if needed;
- minimize layout shift;
- no font strategy that creates excessive FOIT/FOUT or breaks Greek/Latin rendering;
- avoid framework migration unless clearly justified.

Record LCP/INP/CLS or reproducible lab proxies for representative routes where tooling supports it.

---

# 17. Anti-patterns — reject these even if they look polished

- generic dashboard home page;
- giant hero art that pushes corpus access below the fold;
- one card per object;
- ubiquitous rounded rectangles and shadows;
- faux parchment;
- medieval cosplay;
- decorative crosses as bullet points;
- gradient-heavy "AI" aesthetic;
- hidden navigation on desktop for the sake of minimalism;
- mobile pages that begin with huge forms;
- permanent sidebars that squeeze reading measure;
- a source page that presents hashes/rights tables before basic work identity;
- a Catena that looks like a comment thread;
- a history view that is only a raw diff;
- a law view that looks like a CRUD admin screen;
- untyped search results;
- a title fixture presented as global search;
- AI-generated "related" links not backed by corpus data;
- conflating GPT and Claude treatments into one document;
- calling a provider treatment a Source Library edition when it does not satisfy the edition model;
- a literal corpus masthead above the accepted liturgy reader;
- weakening rights/provenance detail to make the interface cleaner;
- changing canonical PDF output as collateral damage;
- silently substituting missing text from another edition/translation.

---

# 18. Sanity-check questions before every acceptance

The reviewer should be able to answer **yes** to all applicable questions:

1. Is it immediately clear what object I am looking at?
2. Is the primary text/object visually dominant?
3. Can I get to the source/provenance without losing my place?
4. Can I tell edition, translation, rights, and uncertainty apart?
5. Is the page calmer than a dashboard?
6. Does it still work as a power tool?
7. Is mobile intentionally recomposed?
8. Is 320px reflow usable?
9. Do keyboard/focus interactions behave predictably?
10. Are stable URLs still meaningful citations?
11. Are PDFs still clearly the canonical printable form?
12. Does the surface feel unmistakably part of the same Triptych system as the liturgical reader?
13. Does the surface retain a distinct composition appropriate to its task?
14. Does every visual embellishment convey information or hierarchy?
15. Are all corpus relationships shown here actually backed by repository data?
16. Could an expert use this for serious research rather than merely admire it?
17. Could a newcomer understand the next action without reading a manual?
18. Is any important truth hidden merely because it is visually inconvenient?

---

# 19. Integration and merge discipline

Parallel branches are expected.

For each accepted lane:
1. the lane's design disposition is recorded;
2. Claude implementation is green on its focused gates;
3. external review ZIP is accepted;
4. the roadmap marks the lane accepted;
5. only then is it eligible for integration.

Integration should be mechanical where possible:
- shared foundation first;
- catalogue/reader/instrument lanes next;
- cross-object links/search after owning surfaces;
- final acceptance last.

When merging reveals a conflict:
- classify it as code conflict, shared-component conflict, or product-semantic conflict;
- code conflicts may be resolved by Claude;
- shared-component visual conflicts must preserve the accepted foundation contract;
- product-semantic conflicts return to Codex for disposition.

Do not solve a product conflict by whichever branch happened to merge last.

## Commit and push authority

Codex may make and push coherent feature and integration branch checkpoints under the repository's existing direct-Codex authority. Claude may commit and push the feature branches explicitly assigned to it for this project, because the maintainer has asked for those branch handoffs.

Neither agent is authorized by this plan to merge or push `main`, or to trigger public cutover. Main integration and Pages publication remain an explicit later decision by the maintainer. Never force-push, and never rewrite shared history (D19).

---

# 20. What each agent should print when it finishes a task

Every agent response must be concise and machine-reviewable.

Print:

```text
TASK:
AGENT:
BRANCH:
BASE SHA:
HEAD SHA:
COMMITS:
TRACKED PLAN/KNOWLEDGE UPDATED:
FOCUSED CHECKS:
KNOWN FAILURES:
PUBLIC/LOCAL PREVIEW:
HANDOFF DIRECTORY:
HANDOFF ZIP:
ZIP SHA-256:
BLOCKING REVIEW QUESTIONS:
NEXT SAFE ACTION:
```

If a field is not applicable, print `None`.

Do not claim:
- deployed,
- accepted,
- complete,
- green,
unless the exact governing gate was actually satisfied.

---

# 21. The first dispatch, and its disposition

**Both dispatches below have been executed and reviewed. Do not run them again.** They are kept because the acceptance in the coordinator review of 2026-08-08 is only legible against what was asked for. A0–A4 and the Claude B0/B1 reconnaissance were all accepted, A2 with amendments D1–D20 and A3 as foundation direction rather than pixel acceptance of any production route. The dispatch that governs new work is in that review: the shared-foundation integration step, then Wave 1.

## Dispatch 1 — Codex: Foundation audit and site-wide visual/product architecture

Give Codex this file and say:

> Execute **A0–A4 only**. Do not redesign production code beyond disposable prototypes required for external visual judgment. Inspect the whole public site and all owning web source directories. Reconcile with the accepted liturgical reader foundation. Create the site-wide corpus vision and roadmap, define the three surface archetypes, define the shared shell, and return one standard external-review ZIP. Persist and commit every durable plan/discovery before packaging the handoff. Do not use Git worktrees.

Expected result:
- one committed foundation design branch;
- durable corpus vision;
- durable roadmap;
- prototype/evidence package;
- exact questions for independent review.

## Dispatch 2 — Claude: implementation feasibility, but no visual invention

Claude may begin in parallel on a separate branch with:

> Audit the current shared browser architecture and test harness for **B0/B1 feasibility only**. Do not implement a new visual direction until the A3/A4 Codex contract is accepted. Identify reusable shared CSS/JS, generator seams, test coverage, route inventory, and likely implementation risks. Persist/commit the technical discovery record and return a standard handoff ZIP.

This lets coding reconnaissance run while visual architecture is being reviewed without allowing Claude to preempt the design.

---

# 22. Definition of done for the whole corpus redesign

This project is not complete merely because every page uses the same fonts/colors.

World-class completion requires:

- the homepage clearly exposes the corpus as a connected research environment;
- every section/library surface is first-rate on desktop and mobile;
- browser-readable papers have a serious long-form reading experience;
- Catena is a signature commentary instrument;
- Source Library makes work/edition/artifact/passage relationships understandable;
- liturgical reader quality is preserved;
- Missal history communicates lineage and evidence clearly;
- Canon Law is citation-first and legally coherent;
- Story of Salvation is a genuine reading journey;
- global typed search reaches the major corpus object classes;
- structured cross-corpus pivots connect sources, commentary, liturgy, history, law, and publications;
- provenance/rights/uncertainty remain at least as truthful as before;
- PDFs remain canonical printable artifacts and are not collateral redesign targets;
- core workflows meet accessibility gates;
- route budgets/performance are measured;
- responsive behavior is intentionally designed across the site;
- all accepted behavior is regression-tested;
- every milestone has immutable evidence ZIPs suitable for independent browser review;
- durable repository guidance tells the next agent exactly why the system is shaped this way.

The desired end state is not "a prettier website."

It is a **scholarly instrument whose visual hierarchy reveals the structure of the corpus itself**.

---

# Coordinator review and execution update — 2026-08-08

This section supersedes any earlier instruction in this master plan that conflicts with it. It is the independent coordinator disposition after review of both foundation branches.

## Reviewed remote state

At review time:

- `origin/main`: `c27d6915319785686d1df6a1401a489aa9921f6f`
- Codex design branch `ux/foundation`: `3b5938a0dba88831763ec09c762ae1572007a27e`
- Claude implementation branch `impl/foundation`: `af2c9613ccda48679face4e43f59c002f93056ef`
- Both branches began from the same exact base `c27d6915319785686d1df6a1401a489aa9921f6f`.

Agents MUST fetch before starting. If `origin/main` no longer equals that SHA, do not reset, force-push, or assume the old base is current. Record the new main SHA, preserve unrelated mainline work, and perform the same integration onto current main.

## Independent disposition

| Work | Owner | Disposition | Binding note |
|---|---|---|---|
| A0 whole-site inventory | Codex | ACCEPT | Treat the route/object/ownership inventory as downstream input. Refresh counts only when release contents change materially. |
| A1 research synthesis | Codex | ACCEPT | The borrow/reject/exceed framing is useful. No framework or IIIF migration is authorized merely because it was researched. |
| A2 product / corpus architecture | Codex | ACCEPT WITH AMENDMENTS BELOW | "The corpus is the product; pages are typed views into it" is the governing product model. |
| A3 visual system + Reader/Catalogue/Instrument | Codex | ACCEPT AS FOUNDATION DIRECTION | This authorizes implementation of the shared non-liturgy foundation and further real-data prototypes. It is NOT pixel-level acceptance of any production route. Every real surface still needs screenshot review. |
| A4 shell / Jump / contextual navigation | Codex | ACCEPT WITH AMENDMENTS BELOW | Jump remains a bounded fixture until J0–J2. Related is typed navigation, never recommendation inference. |
| B0/B1 reconnaissance | Claude | ACCEPT | Claude found the actual generator seams, shared-code drift, URL constraints, rights constraints, and live WIP collisions. These findings are binding implementation input. |
| Neutral static/browser gates | Claude | ACCEPT FOR INTEGRATION | Integrate the JS/static parsing gate and generated-artifact browser gate. Known inherited failures remain findings, not excuses to rewrite unrelated areas. |
| Production shell | Claude | AUTHORIZED NEXT, NON-LITURGY FIRST | Implement only after the accepted coordinator amendments are present on the shared integration branch. |

## What this acceptance does and does not mean

This review accepts the product model and enough of the design contract to unblock real implementation and real-data design work. It deliberately does not declare the synthetic prototype itself a finished visual product. The ignored screenshot ZIP was not available through the pushed Git branch, so the next Codex handoff MUST include the external-review ZIP for direct browser review. Real routes, real titles, real source metadata, real absence/rights states, and real mobile composition are the next visual oracle.

## Binding coordinator amendments / dispositions

These decisions answer the Codex blockers and Claude C1–C16 conflicts. Record them durably in the integration branch rather than leaving them only in this handoff.

### D1 — `/texts/` public label

Accept **Publications** as the compact global label for `/texts/`.

- Do not rename the route.
- Do not create a second canonical publication home.
- The existing one-owning-catalog rule remains authoritative.
- The Publications browser may aggregate discoverability, metadata, browser-read links, and facets, but it may not create a second owning PDF catalogue.

### D2 — protected liturgy adapter

Accept the exclusive liturgy adapter. Canonical Day and Propers are a protected surface family.

Until the current Live Reader — Ritual Flow & Orientation work is independently closed or explicitly carved out:

- do NOT modify `reader-shell.js`;
- do NOT modify `reader-instrument.css`;
- do NOT modify canonical `liturgy/day.html` or `liturgy/index.html` source ownership;
- do NOT add a fifth primary reader action;
- do NOT add a second competing modal owner;
- do NOT add a literal corpus masthead above the accepted reader;
- do NOT redesign its print behavior;
- do NOT merge site-wide Search into the reader shell.

The corpus project may design a future low-chrome corpus exit/context affordance for liturgy, but it must enter through an already accepted seam such as Details or a quiet terminal/footer treatment and must receive its own liturgy-specific visual acceptance. The accepted first viewport remains sacred.

### D3 — provider terminology

Reject "parallel provider treatment" as primary public wording.

Use:

- **Independent treatment** as the human-facing label when distinguishing independently produced ChatGPT/Claude treatments.
- **Parallel treatment** as a relationship label when two treatments of the same work are intentionally connected.
- Always show the provider as explicit metadata rather than baking provider jargon into the relationship name.

Never call these Source Library editions unless they actually satisfy the edition model.

### D4 — three archetypes

Accept Reader / Catalogue / Instrument as the site-wide archetypes.

They share identity, tokens, spacing logic, accessibility behavior, URL discipline, and contextual-navigation grammar. They do not share one universal layout.

### D5 — visual tokens are roles, not frozen pixels

Accept the warm-paper / near-black / restrained-oxblood / blue-focus direction, disciplined serif reading axis, UI sans stack, square/quiet controls, rules rather than card walls, and restrained chrome.

But:

- exact type sizes, especially the synthetic prototype's very large display headings, are not frozen;
- exact desktop masthead density is not frozen;
- exact spacing values may move after real-data screenshots;
- no production design may rely on Inter actually being installed;
- use robust system/local fallback stacks unless a separately authorized font+rights+generator work unit proves a self-hosted font worth its cost;
- test long real titles, multilingual text, Latin, polytonic Greek where applicable, narrow screens, and Windows/Linux/macOS font fallback before calling typography settled.

### D6 — global navigation

Accept the information architecture, not the exact count/geometry of visible desktop links in the synthetic prototype.

Top-level corpus destinations remain:

- Publications
- Sources
- Scripture
- Liturgy
- History
- Law
- Commentary

The Triptych wordmark itself is a Home affordance; a separate visible Home item is optional and should survive only if real 1024px and 200% evidence shows the masthead still reads calmly. Lower-priority destinations may collapse to Menu earlier than the prototype if density warrants it. Do not solve density with tiny text.

### D7 — homepage and seven portals

Do not throw away the seven editorial identities merely to make the homepage look new.

Wave 1 should prototype:

- a task-oriented corpus entrance layer — read, find, trace, follow, compare/change, look up;
- the seven existing editorial portals beneath or beside it as durable corpus orientation;
- direct movement into Publications, Sources, Commentary, Liturgy, History, Law, and Scripture without turning the homepage into a dashboard.

Preserve the current seven portal names/order/color identities unless Codex demonstrates a materially better real-data alternative and explicitly proposes an amendment to `guidance/repository.md`. Do not silently break the generator's current README transform.

### D8 — one owning catalogue

A faceted Publications surface is a discovery view, not a second ownership hierarchy. It may reveal all relevant treatments and formats, but each publication still has exactly one owning catalogue and canonical PDF home.

### D9 — long-form web editions

`guidance/web-editions.md` is controlling for the publication Reader lane.

- Never create a second editable copy of publication prose.
- Do not edit `web/<provider>/*.md` merely to achieve UI presentation.
- Preserve visible rights colophon and revision identity.
- Any material omission remains explicitly declared.
- Re-run the web-edition currency checks after renderer/converter changes.

### D10 — durable project memory

For the corpus redesign, durable truth belongs primarily in:

- `guidance/corpus-browser-master-plan.md`
- `guidance/corpus-browser-vision.md`
- `guidance/corpus-browser-roadmap.md`
- `guidance/corpus-browser-implementation.md`
- relevant owning guidance for each surface
- `PROJECT-WORK.md`
- `promised-deliverables.toml`

Do not depend on a force-tracked `build/agent-continuity/*` file for facts required by future agents. `build/` may remain useful for ignored handoffs, screenshots, logs, and temporary continuity, but durable facts MUST also exist in the tracked guidance/ledger above. Do not integrate the Codex foundation continuity file as the sole owner of any fact.

### D11 — screenshot matrix

Use one comparable site-wide matrix unless a more specific owning surface requires more:

- 1440 × 900
- 1024 × 768
- 768 × 1024
- 393 × 852
- 320 × 852

Also exercise:

- 200% text enlargement;
- exact 320-CSS-pixel reflow;
- 400% zoom/reflow where meaningful;
- keyboard-only operation;
- forced colors;
- reduced motion;
- browser print for surfaces where print is not explicitly delegated only to canonical PDF;
- no-JavaScript/static truth;
- console/network/HTTP/accessible-name checks.

Do not create pixel-diff baselines before a real-data surface has independent visual acceptance.

### D12 — assets and generator constraints

Until explicitly changed and tested:

- no webfont dependency;
- no icon library;
- no framework migration;
- no root-relative links that break GitHub Pages under `/triptych/`;
- no new asset type that the generator will reject;
- preserve HTML payload limits and the static/no-server deployment model.

### D13 — Search / Jump

A4 Jump remains a bounded demonstration of interaction grammar only.

Production Search is J0 → J1 → J2:

- Codex defines typed search UX and states against real corpus objects.
- Claude benchmarks a public-only static index and proves no-leak, payload, latency, memory, multilingual, and route-state behavior.
- Claude implements only the selected measured design.

No route may pretend a title fixture is global search.

### D14 — relationships

Contextual relationships are powerful enough to become a signature Triptych feature, but only where the corpus can prove them.

Currently safe categories include explicit containment, passage→artifact/segment, Catena fragment→Scripture locus, Catena passage→Source Library passage, act descent/change/history, document→catalogue page, and Mass→propers→Scripture resolution.

Do not synthesize `translation_of`, `used_by`, `derived_from`, canon correspondences, Law→Source citations, or generic "related" recommendations from title/keyword similarity. A new relationship is a schema/generator work unit under the owning corpus guidance before it is a UI feature.

### D15 — rights, absence, and progressive disclosure

Progressive disclosure may defer:

- hashes;
- extended artifact provenance;
- long rights/legal apparatus;
- secondary technical metadata.

It may not defer or erase:

- required licence acknowledgement at point of use;
- a withheld-text reason;
- typed absence/unread/unsupported/invalid state;
- the distinction between availability and redistribution rights.

Every renderer must preserve these states semantically, not only through color or a CSS class.

### D16 — local reading progress

Defer local reading progress from the current foundation wave. If introduced later for long-form publications, it must be storage-optional and an explicit URL always wins. Do not add persistence to Day; its current no-memory behavior is intentional.

### D17 — browser architecture findings

Treat the following Claude findings as real engineering debt, not as permission for a rewrite:

- all generated surfaces pass through one layout seam;
- shared browser-core is widely adopted but oversized and unevenly used;
- history/law and Day/Propers contain localized duplicated helpers;
- several hash routers can create excessive browser-history entries;
- history currently has a missing none-claimed citation gloss;
- some generated pages have nested `<main>` landmarks;
- some generated states lose the expected first focus target/skip-link behavior;
- Source Library and Publications have measured 320px overflow in the current build;
- existing Chromium harnesses are useful and should become invoked, not discarded.

Fix these incrementally with path-specific commits and before/after gates. Do not turn B0 into a browser-stack rewrite.

### D18 — current liturgy WIP collision

The current Live Reader — Ritual Flow & Orientation task remains a separate in-progress deliverable. This corpus project does not supersede it. If the owning liturgy work finishes during this project, re-read the new main state before touching any formerly protected seam.

### D19 — commit / push authority

- Codex may make and push coherent feature/integration branch checkpoints under the repository's existing direct-Codex authority.
- Claude may commit and push its explicitly assigned feature branches for this project because the maintainer has requested these branch handoffs.
- Neither agent is authorized by this plan to merge/push to main or trigger public cutover. Main integration and Pages publication remain an explicit later decision.
- Never force-push or rewrite shared history.

### D20 — separate full checkouts

Continue using separate full repository directories for parallel lanes. Do not use worktrees for this project. Never let two agents share one working directory/index.

## Shared foundation integration — execute before the broad production fan-out

### Owner: CODEX

Create a new full checkout and branch:

```text
corpus/foundation-integration
```

Base it on current `origin/main` after fetching. At review time this is `c27d6915319785686d1df6a1401a489aa9921f6f`.

The purpose is not to merge all branch history blindly. Build one coherent accepted foundation commit series from the useful durable artifacts.

Integrate from `ux/foundation`:

- `guidance/corpus-browser-inventory.md`
- `guidance/corpus-browser-research.md`
- `guidance/corpus-browser-vision.md`
- `guidance/corpus-browser-roadmap.md`
- the synthetic foundation prototype and its focused tests
- the tracked master plan, updated to this v2 coordinator disposition
- the appropriate `PROJECT-WORK.md` / promise-ledger records

Integrate from `impl/foundation`:

- `guidance/corpus-browser-implementation.md`
- the `AGENTS.md` routing row(s), adjusted so future agents can find BOTH the design and implementation guidance
- the neutral browser/static syntax test target from Claude's `71875b7...` work
- the built-artifact corpus browser gate from Claude's `67ae7d3...` work
- the precise follow-up corrections through Claude head `af2c9613...`

Do NOT blindly integrate:

- duplicate/conflicting copies of the old master plan;
- branch-local stale `PROJECT-WORK.md` sections without manual reconciliation;
- the force-tracked `build/agent-continuity/corpus-browser-foundation.md` as a required durable owner;
- any production CSS/JS change to the protected liturgy files.

On the integration branch, update the durable records so they explicitly contain D1–D20 above and mark the reviewed foundation disposition accurately.

Suggested status language:

- A0: Accepted
- A1: Accepted
- A2: Accepted with coordinator amendments D1–D20
- A3: Accepted as foundation design direction; real production surfaces retain independent visual acceptance gates
- A4: Accepted with bounded-Jump / typed-Related / protected-liturgy amendments
- Claude reconnaissance: Accepted
- B0: Authorized in progress after this integration branch exists
- B1: Authorized in progress

Run the complete focused validation available on the integrated branch. Preserve inherited base failures as inherited findings; do not rewrite unrelated registries or stale examples to manufacture a green aggregate gate.

Push `corpus/foundation-integration`. Do not merge to main.

Return a compact integration ZIP with:

- base/head/branch;
- exact incorporated paths and source SHAs;
- conflict resolutions;
- disposition table;
- commands and numeric exit statuses;
- proof no canonical PDF changed;
- proof no protected liturgy production asset changed;
- exact next branch base for all downstream corpus work.

## Work that may continue in parallel while Codex integrates

Claude does not need to sit idle while the integration branch is being assembled.

### Owner: CLAUDE

Continue from `impl/foundation` on a new branch:

```text
impl/foundation-hardening
```

Do only work that is mechanically cherry-pickable into the eventual integration branch and does not require final surface visual decisions:

- Wire the existing real-Chromium harnesses into explicit Make targets that correctly depend on a preview build.
- Improve the new site-wide generated-artifact browser gate without pixel baselines.
- Add route/state fixtures needed to reproduce current known structural defects.
- Fix safe, non-liturgy selector/helper collisions where the change can be proven visual-neutral:
    - target-aware failure/banner plumbing;
    - History `.field` collision;
    - Publications/Texts `.detail` collision;
    - similarly scoped non-liturgy collisions discovered during the audit.
- Add tests that lock current published URL/hash compatibility before any router cleanup.
- Prepare — but do not yet land across protected liturgy files — a reusable implementation plan for shared accessibility helpers and duplicated history/law utilities.

Do NOT:

- touch `reader-shell.js`;
- touch `reader-instrument.css`;
- touch canonical Day/Propers source ownership;
- scope/fix `day-missal.css` yet if doing so enters the live liturgy owner's paths;
- implement the global shell before the integration branch records D1–D20;
- alter real visual styling of the individual corpus instruments;
- build Search;
- infer new relationships;
- edit publication prose or PDFs.

Push `impl/foundation-hardening`. Return the standard ZIP. Everything must be independently cherry-pickable by path/commit.

## Wave 1 — run Codex and Claude in parallel from the accepted integration branch

Once `corpus/foundation-integration` is pushed, all new Wave 1 work starts from its exact head.

### CODEX — real-data visual/product wave

Branch:

```text
ux/corpus-wave-1
```

Codex owns visual/product design only. Use the actual generated corpus, not synthetic titles, for the primary evidence.

Execute these design units:

| ID | Surface | Goal |
|---|---|---|
| C0/C1 | Home + Publications / Catalogue | Turn the root into a calm corpus map with task entrances plus the seven editorial portals; make Publications a serious list-first scholarly discovery surface rather than a giant table/card wall. |
| D0 | Long-form publication Reader | Apply the accepted reading quality of the liturgy work to browser-readable publications while preserving provider, revision, colophon, canonical PDF, stable anchors, and source honesty. |
| E0 | Catena Omnia | Make Scripture the anchor and commentary the chronological/typed chain. Design held fragment, attribution-only, unavailable, source link, voice/language, and narrow-screen states. This should become a signature Triptych instrument. |
| F0 | Source Library | Make Work → Edition → Artifact → Passage perceptible without forcing forensic metadata into the first glance. Design readable, withheld, unread, rights-limited, artifact, and passage-deep-link states. This should become the corpus evidence observatory. |

#### Wave 1 Codex requirements

- Start by rendering current real routes at the shared screenshot matrix.
- Design with real long titles, real multilingual/source metadata, real absences, and real provider differences.
- Reuse the foundation token roles, but adjust exact values when real evidence proves they are wrong.
- Keep primary content dominant. No dashboardification, no card-everything, no decorative ecclesiastical cosplay.
- Preserve existing URLs/hash keys and canonical PDF relationships.
- Do not modify production implementation; prototypes may be isolated/noindex.
- For each surface, record:
    - primary user jobs;
    - object being manipulated/read;
    - first viewport target;
    - information hierarchy;
    - wide/narrow composition;
    - keyboard/focus behavior;
    - absent/unsupported/withheld/error states;
    - exact contextual transitions to other corpus objects;
    - what is deliberately NOT shown first.
- Treat the foundation prototype's desktop nav geometry and display-heading sizes as hypotheses, not commandments.
- Do not visually redesign the protected canonical Day/Propers routes in this wave.

#### Required Codex evidence ZIP

This ZIP is mandatory. The next independent review will not accept a visual lane from branch source alone.

Include:

- `HANDOFF.md` first;
- exact base/head/branch;
- numbered contact sheet;
- before/after pairs for every governed route;
- 1440×900, 1024×768, 768×1024, 393×852, 320×852;
- representative 200% and 400%/reflow states;
- keyboard focus states;
- forced colors and reduced motion where behavior changes;
- open Menu/Jump/Related/Contents/filter states where applicable;
- at least one long-title stress case;
- at least one multilingual/source-heavy stress case;
- at least one withheld/unavailable/zero-result case per relevant instrument;
- browser print evidence for long-form publication Reader if the web page itself has a print treatment;
- visual review notes naming every compromise or unresolved question.

Push the branch and give the maintainer the ZIP to paste into ChatGPT for independent visual review.

### CLAUDE — shared non-liturgy production foundation

Branch:

```text
impl/corpus-wave-1
```

Base: exact head of `corpus/foundation-integration`.

Claude owns implementation and test architecture. Implement B0/B1 for non-liturgy public surfaces first, using the accepted design contract and D1–D20.

#### B0 implementation scope

- Establish the shared corpus-shell implementation at the single generator/layout seam.
- Make route/domain identity generated from one ordered source of truth.
- Implement non-liturgy masthead/navigation/Menu primitives with relative GitHub-Pages-safe URLs.
- Implement the accepted token roles in the appropriate shared CSS seam without assuming webfonts.
- Provide route-specific policy so canonical Day/Propers do not receive a visible literal corpus masthead or new modal owner.
- Preserve static/no-JS identity, core content, canonical PDF links, source/legal truth, and direct URL usefulness.
- Resolve nested landmark/skip-link issues at the lowest safe shared seam.
- Fix current 320px overflow in Sources and Publications without masking overflow globally.
- Keep all target sizes/accessibility semantics testable.
- Preserve current public paths and hash keys exactly.
- Do not promote `reader-shell.js` into the corpus shell while the liturgy Ritual Flow task owns it. Reuse ideas, not the owned file.
- Do not split/rewrite `browser-core.js` merely for aesthetics. Any extraction must be small, measured, dependency-safe, and independently testable.

#### B1 test scope

Build/invoke a site-wide browser gate that covers representative states of every non-PDF browser surface and asserts at minimum:

- no console errors/warnings that indicate a defect;
- no failed requests / HTTP failures;
- no unnamed interactive accessible nodes;
- valid single-`main` landmark structure;
- working skip link / first-focus semantics;
- no horizontal overflow at 320 CSS px;
- ≥44×44 primary interactive targets where required;
- useful behavior at 200% text and 400%/reflow;
- forced-colors and reduced-motion sanity;
- no-JS static identity/core truth;
- URL/hash compatibility;
- direct route loading on GitHub-Pages-style subpath;
- generated artifact, not merely repository source HTML.

Do not add visual pixel baselines before Codex surface acceptance.

#### Claude Wave 1 stopping line

Claude may implement the shared foundation and neutral structural fixes. Claude must NOT independently invent the final Home, Publication Reader, Catena, or Source Library composition before Codex returns the corresponding accepted D0/E0/F0/C0-C1 design evidence.

Where a surface needs styling beyond the shared foundation, create clearly bounded extension seams and stop.

#### Required Claude evidence ZIP

Include:

- `HANDOFF.md` first;
- exact base/head/branch and commit graph;
- changed-file inventory grouped by generator/shared shell/tests/surface;
- static and Chromium gate summaries with numeric exit codes;
- generated-route screenshots showing the shell only, not claiming visual acceptance of unfinished surfaces;
- 320px overflow evidence before/after where fixed;
- landmark/skip-link evidence before/after;
- URL/hash compatibility report;
- payload/build-time deltas;
- known inherited failures clearly separated from introduced failures;
- proof protected liturgy files were not changed;
- proof PDFs were byte-unmodified;
- exact dependencies still waiting on Codex C0/C1/D0/E0/F0.

Push the branch and give the maintainer the ZIP to paste into ChatGPT.

## Optional maximum-parallel design fan-out

If the maintainer launches multiple independent Codex sessions, Wave 1 may split further, but every worker MUST use a separate full checkout and branch from the same integration head:

- `ux/catalogue` — C0/C1
- `ux/reader` — D0
- `ux/catena` — E0
- `ux/sources` — F0

Do not let multiple workers edit the same durable roadmap/ledger files concurrently. Give one coordinator worker ownership of shared tracking documents; leaf workers return branch commits + ZIP evidence for that coordinator to record.

Likewise, if multiple Claude sessions are launched, safe sublanes are:

- `impl/browser-gates` — B1 only
- `impl/shell` — B0 shared non-liturgy shell only
- `impl/structural-fixes` — nested `main` / skip-link / measured overflow / selector collisions only

Again: separate full checkouts, one tracking owner, no worktrees, no shared index.

## Wave 2 — do not start production implementation yet, but keep fully parallelizable

After Wave 1 design acceptance and B0/B1 foundation acceptance:

| Design lane | Owner | Implementation lane | Owner | Dependency |
|---|---|---|---|---|
| G0 History | Codex | G1 History | Claude | accepted B0 + G0 |
| H0 Law | Codex | H1 Law | Claude | accepted B0 + H0 |
| I0 Scripture | Codex | I1 Scripture | Claude | accepted B0 + I0 |
| J0 Search UX | Codex | J1 benchmark → J2 implementation | Claude | J0 before engine choice |
| K0 typed relationships | Codex | K1 projection | Claude | accepted owning surfaces + verified schema edges |
| L0 whole-site visual coherence | Codex | L1 accessibility / mechanical closure | Claude + Codex | all surface lanes |
| M0 integration/cutover candidate | Claude on feature branch | M1 independent acceptance | Codex + ChatGPT coordinator | explicit maintainer publication authorization |

## Next review protocol

For the next browser review, provide ChatGPT:

- Codex ZIP;
- Claude ZIP;
- branch names/head SHAs if they changed after ZIP creation.

ChatGPT will review the two handoffs together, compare screenshots against implementation evidence, record accept/reject/changes-required by lane, and issue the next parallel dispatch. The maintainer should not have to manually translate one agent's findings into instructions for the other.

## Exact prompt — CODEX integration + Wave 1

> Use this entire revised master plan as governing context.
>
> You are the Codex visual/product coordinator for the Triptych corpus redesign.
>
> First execute the narrow **Shared foundation integration — CODEX** section above on `corpus/foundation-integration`. Reconcile the accepted Codex and Claude foundation artifacts path-by-path; record D1–D20 durably; do not merge to main; do not touch protected liturgy production assets; push the integration branch and produce the compact integration ZIP.
>
> Then, from the exact pushed integration head, create `ux/corpus-wave-1` and execute C0/C1, D0, E0, F0 as real-data design/prototype lanes. The target is not generic consistency: Home/Publications, long-form reading, Catena Omnia, and the Source Library must each become purpose-built world-class surfaces within one coherent corpus language.
>
> The accepted liturgy reader is the quality benchmark and protected exception. PDFs remain canonical printable editions. Preserve URLs, provenance, rights distinctions, provider identity, absence states, and static truth.
>
> Persist every important discovery, decision, rejected alternative, route/state inventory, and progress update into tracked guidance/roadmap/project records. Do not rely on chat memory or ignored build files.
>
> Return mandatory ZIP evidence exactly as specified. Push feature branches only. Do not merge or deploy main.

## Exact prompt — CLAUDE hardening + Wave 1

> Use this entire revised master plan as governing context.
>
> You are the Claude implementation/testing coordinator for the Triptych corpus redesign.
>
> Immediately continue safe parallel work on `impl/foundation-hardening` from current `impl/foundation` head `af2c9613ccda48679face4e43f59c002f93056ef`, limited to the mechanically cherry-pickable hardening tasks listed above. Do not touch protected liturgy files or invent visual product decisions.
>
> When Codex pushes `corpus/foundation-integration`, fetch it, record its exact head, and create `impl/corpus-wave-1` from that head. Execute B0/B1 for the shared non-liturgy production foundation exactly as specified above. Treat the Codex design contract and D1–D20 as binding; treat `guidance/corpus-browser-implementation.md` as the architecture/risk record; treat owning surface guidance as higher priority when more specific.
>
> Do not rewrite the browser stack, do not build Search early, do not infer missing relationship edges, do not edit publication prose, do not alter canonical PDFs, and do not enter the in-progress liturgy Ritual Flow owner's files. Preserve public URLs/hash state and GitHub Pages subpath behavior.
>
> Persist architecture discoveries, resolved hazards, measured deltas, tests, blockers, and exact dependencies into tracked guidance/roadmap/project records. Keep inherited repository failures distinct from regressions introduced by this work.
>
> Return mandatory ZIP evidence exactly as specified. Push feature branches only. Do not merge or deploy main.

---

# Change log — how sections 1–22 were reconciled with D1–D20

The coordinator review supersedes any earlier instruction in this plan that conflicts with it. Appending it was not enough on its own: sections 1–22 stated several of those superseded instructions as though they still governed, and an agent reading this document from the top would have followed them. Those sections were therefore corrected in place on 2026-08-08. This log exists so the correction can be audited. It is not an errata section, and no contradiction is left standing upstream of it.

| Location | What it said | What it says now | Required by |
|---|---|---|---|
| §1 Mission, object list | "parallel GPT / Claude treatments" | "independent GPT / Claude treatments of the same work, and the parallel-treatment relationship where two are intentionally connected" | D3 |
| §2 read list | omitted `guidance/web-editions.md` | lists it as item 9 | D9 |
| §3 branch discipline | silent on two agents in one directory | "Never let two agents share one working directory or one index." | D20 |
| §4 opening | told the reader to create the vision and roadmap | records that A0–A4 were accepted and that both documents exist on `ux/foundation`, to be integrated rather than written again | coordinator disposition, 2026-08-08 |
| §4.4 continuity record | allowed a `build/agent-continuity/...` file as the continuity authority | allows it for handoffs, screenshots, logs, and in-flight state only; durable facts also live in the tracked guidance and ledger | D10 |
| §6.1 shell requirement | "Every non-PDF browser page should share … global corpus search / jump", no exception stated | scoped to pages **outside the protected liturgy reader**, with the exception stated immediately beneath the requirement rather than 900 lines later | D2, D18 |
| §6.1 navigation list | "Home / Library / Sources / Scripture / Liturgy / History / Law / Catena" | Publications, Sources, Scripture, Liturgy, History, Law, Commentary, with the wordmark as the Home affordance | D6 |
| §6.2 homepage | "section/library discovery below" | the seven editorial portals kept by name, order, and colour, with the amendment path for changing them | D7 |
| §6.3 catalogue | "paired GPT/Claude issues treated as related editions"; "model/edition identity" | "parallel treatments of one work"; "provider shown as explicit metadata"; plus the independent-vs-parallel labels and the never-a-Source-Library-edition rule | D3 |
| §6.3 catalogue | silent on the route label and on ownership | `/texts/` labelled Publications without renaming the route; the faceted catalogue is a discovery view and each publication keeps one owning catalogue and one canonical PDF home | D1, D8 |
| §6.4 publication reader | "model/edition identity"; "side-by-side GPT/Claude comparison" | provider as explicit metadata alongside revision identity; "comparison of two provider treatments"; plus the `web-editions.md` rules | D3, D9 |
| §6.9 Story of Salvation | "progress is optional and local-only if added" | local reading progress deferred from the foundation wave; storage-optional and URL-wins if it returns later | D16 |
| §6.10 global search | silent on Jump | Jump is a bounded fixture, production Search is J0 → J1 → J2, no title fixture may pass as global search, and the entry point does not enter the liturgy reader shell | D13, D2 |
| §7 opening | no statement of the accepted visual direction or its status | the accepted direction stated as token **roles, not frozen pixels** | D5 |
| §7 Typography | silent on webfonts | no dependency on a webfont or on an installed face; fallback stacks and multilingual/cross-platform testing required before typography is settled | D5, D12 |
| §7 Surfaces | "All share tokens and shell" | enumerates what the three archetypes share, and states they do not share one universal layout | D4 |
| §7 Ornament | silent on icon libraries | "No icon library: a mark is drawn in CSS, or in inline markup the generator already accepts." | D12 |
| §8 table, *Depends on* | C2 `C0/C1/B0`, E1 `E0/B0`, F1 `F0/B0`, G1 `G0/B0`, H1 `H0/B0`, I1 `I0/B0` | B0 removed from all six | measured architecture (below) |
| §8 table, D1 row | parallel lane "Reader" | parallel lane "Foundation (see below)" | measured architecture (below) |
| §8 parallelization rule | lanes may run in parallel only after "B0 establishes the shared shell contract" | lanes do not wait on B0; the shared and generated concerns that stay single-owner are enumerated; D1 and J2 keep their B0 dependency and their reasons are given | measured architecture (below), D2 |
| §10.2 implementation | silent on asset and link constraints | no root-relative link under the `/triptych/` Pages subpath, no webfont, no icon library, no framework migration, no asset type the generator rejects, payload limits and the static/no-server model preserved | D12 |
| §10.2 implementation | silent on how far the architecture findings reach | the debt is paid incrementally with path-specific commits and before-and-after gates; B0 does not become a browser-stack rewrite | D17 |
| §11 screenshot matrix | "Suggested"; `1440x1000` and `320x800` | one normative site-wide matrix; `1440x900` and `320x852`; the further conditions to exercise; no pixel-diff baselines before a real-data surface has independent visual acceptance | D11 |
| §12.2 Every Document | "paired GPT / Claude documents"; "'Compare editions' when two browser-readable AI editions exist" | "paired GPT / Claude treatments of one work"; "'Compare treatments' when two browser-readable provider treatments of one work exist" | D3 |
| §12.5 Source Library | progressive disclosure with no stated floor | the floor stated: what may never be deferred or erased, and that it must survive semantically | D15 |
| §13 relationships | one flat list of "potential relationship types", including several the corpus cannot prove | a provable-today list, an explicit not-to-be-synthesised list, and the vocabulary demoted to candidate names for edges that are proven first | D14 |
| §17 anti-patterns | "conflating GPT and Claude editions into one document" | "…treatments…", plus three added: a title fixture presented as global search, calling a provider treatment a Source Library edition, and a literal corpus masthead above the accepted liturgy reader | D3, D13, D2 |
| §19 integration | silent on push authority | commit and push authority stated; no merge or push to `main`, no public cutover, no force-push | D19 |
| §21 first dispatch | "Run these first." | records that both dispatches were executed and disposed of, and names the dispatch that governs new work | coordinator disposition, 2026-08-08 |

## One correction is newer than the review, and is an implementation discovery

The dependency change in §8 is not a product judgment and must not be read as one. The plan's original sequencing — every implementation lane waits on B0 — was an assumption about how the tree is coupled. The implementation lane measured the tree instead and recorded the measurement at `guidance/corpus-browser-implementation.md` §17.1: no cross-entrance asset reference anywhere, and no header, navigation, footer, masthead, or breadcrumb construction in the shared browser core at all. The coordinator accepted that correction on 2026-08-08, together with the ruling that the independent instrument directories may proceed in parallel once their designs are accepted while shared and generated concerns stay single-owner. D2's withdrawal of the `reader-shell.js` promotion removed the other stated reason for the dependency.

The measurement is cited rather than copied, so it keeps one owner and cannot drift out of agreement with itself. If the tree changes, `guidance/corpus-browser-implementation.md` §17.1 is what gets re-measured, and this plan follows it.

## Three contradictions the review did not name

`guidance/web-editions.md` was missing from the §2 read list while D9 makes it controlling for a lane this plan owns. §4 instructed an agent to create two documents that already exist on the design branch. §21 told an agent to run first dispatches that had already been executed and accepted. All three are corrected above.

## What was left alone, and why

- **`Every Document` keeps its page title.** D1 accepts Publications as the compact *global label* for `/texts/` and forbids renaming the route. It does not retitle the surface, and doing so would be a product decision rather than a reconciliation.
- **J2 keeps its B0 dependency.** The measurement covers the six instrument lanes, whose work lands inside their own entrance directories. A global search entry point is shell furniture, and nothing measured says otherwise.
- **§6.6, §6.7, §6.8, and most of §12** read as design briefs rather than settled decisions and contradict no amendment. They are unchanged.
- **The definition of done in §22, the three archetypes, and the aesthetic judgments in the anti-pattern list** were accepted or untouched by the review. Changing them would be inventing product, not reconciling it.
