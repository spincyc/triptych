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
- parallel GPT / Claude treatments;
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
9. the profile/guidance owning the surface being touched.

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

For parallel work, use **separate full repository directories with separate branches**. One agent task owns one branch and one checkout directory at a time.

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

Create or update these tracked authorities early, before substantial implementation:

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
Use a task-specific tracked continuity file if repository convention permits it, or a documented task-specific `build/agent-continuity/...` exception consistent with current project practice.

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
Every non-PDF browser page should share:
- compact Triptych identity;
- clear current-domain identity;
- global corpus search / jump;
- predictable access to Home / Library / Sources / Scripture / Liturgy / History / Law / Catena;
- a persistent but quiet way to reveal related corpus objects;
- stable footer/legal/feedback treatment;
- consistent focus and responsive behavior.

The shell must remain **quiet**. Do not turn every page into a dashboard.

## 6.2 Home: "the corpus map"
The current homepage is a good inventory but visually functions as lists and tables. Replace the experience with an editorially calm **map of the corpus**:
- one strong statement of what Triptych is;
- immediate entrances by task, not just section;
- "Read today", "Find a text", "Trace a source", "Follow commentary", "See what changed", "Look up a canon";
- section/library discovery below;
- visible corpus scale only when it is accurate and generated;
- recent/featured material only if repository truth supports a deterministic rule—no hand-curated fake freshness;
- clear distinction between browser instruments and canonical PDFs.

## 6.3 Section libraries / Every Document
The section pages and `Every Document` should become a strong **catalogue and collection browser**, not HTML tables disguised as a website.

Requirements:
- faceted filters;
- fast search;
- group by subject / series / section;
- strong publication title;
- concise abstract;
- model/edition identity;
- length/revision metadata;
- obvious Read vs PDF;
- paired GPT/Claude issues treated as related editions, not independent random links;
- responsive list-first presentation;
- optional dense/table view for power users;
- stable URLs for filter state where useful.

## 6.4 Browser-readable publication pages
All generated "Read" versions of papers should receive a world-class long-form reader:
- controlled measure;
- meaningful heading hierarchy;
- location-aware TOC;
- footnotes/citations that are easy to inspect and return from;
- source links that open contextual detail without losing position;
- model/edition identity;
- canonical PDF action;
- previous/next only when a real series/order exists;
- print CSS may be useful, but the PDF remains the canonical printable edition;
- side-by-side GPT/Claude comparison may be a later capability, but the architecture should allow it.

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
- progress is optional and local-only if added—do not require accounts;
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

---

# 7. Visual language

Codex owns the exact design system, but it should begin from these constraints.

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
- metadata visibly subordinate but never illegible.

## Surfaces
Use three related surface archetypes rather than one universal layout:

1. **Reader** — papers, Scripture, liturgy, passages.
2. **Catalogue** — Home, sections, Every Document, search.
3. **Instrument** — Catena, Source Library, Missal history, Law.

All share tokens and shell; each has purpose-built composition.

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
Use iconography/symbols only when they clarify domain or state.
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
| C2 | Catalogue implementation | **Claude** | Catalogue | C0/C1/B0 | production Home/sections/text catalogue | focused tests + production-like captures |
| D0 | Browser-readable paper design | **Codex** | Reader | A2/A3 | long-form article reader + citations/TOC/PDF action | long paper desktop/mobile evidence |
| D1 | Article reader implementation | **Claude** | Reader | D0/B0 | reusable paper reader styling/behavior | sample corpus matrix |
| E0 | Catena signature redesign | **Codex** | Catena | A2/A3 | Scripture/commentary chain interaction + responsive states | multiple chapter/comment density states |
| E1 | Catena implementation | **Claude** | Catena | E0/B0 | production Catena | model tests, DOM/a11y, real-data captures |
| F0 | Source Library evidence-observatory design | **Codex** | Sources | A2/A3 | work→edition→artifact→passage explorer | rights/readable/withheld/multi-edition states |
| F1 | Source Library implementation | **Claude** | Sources | F0/B0 | production Source Library | data-parity tests + a11y + real records |
| G0 | Missal history redesign | **Codex** | History | A2/A3 | Missal Line + prayer lineage visual spec | branch/station/broken-line states |
| G1 | Missal history implementation | **Claude** | History | G0/B0 | production history instrument | semantic + viewport regression |
| H0 | Canon-law redesign | **Codex** | Law | A2/A3 | citation-first canon/history/act UX | public-domain/withheld/unchanged states |
| H1 | Canon-law implementation | **Claude** | Law | H0/B0 | production law instrument | deep-link + a11y + state tests |
| I0 | Story of Salvation redesign | **Codex** | Scripture | A2/A3 | 3-depth reading journey + pivots | desktop/mobile and all three depths |
| I1 | Scripture implementation | **Claude** | Scripture | I0/B0 | production Scripture plan | translation + route tests |
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

After **A2/A3/A4 are accepted and B0 establishes the shared shell contract**, lanes C, D, E, F, G, H, I, and much of J may run in parallel.

Do not block a lane on unrelated surface implementation.

Codex design lanes can run before B0 is fully implemented if they all consume the same accepted token/archetype contract.

Claude implementation lanes should rebase/merge the accepted shared foundation before coding and should not each reinvent shared primitives.

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
- use semantic HTML first, ARIA only where needed.

If the design cannot be implemented without violating a repository invariant:
1. stop that design choice;
2. record the exact conflict;
3. implement the largest safe subset if independently useful;
4. return a blocker for Codex.

Do not silently "simplify" the design.

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

## Suggested screenshot matrix
Every visually significant surface should normally include:

```text
<route>--default--1440x1000.png
<route>--default--1024x768.png
<route>--default--768x1024.png
<route>--default--393x852.png
<route>--default--320x800.png
<route>--text-200pct--393x852.png
<route>--forced-colors--393x852.png
```

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
- paired GPT / Claude documents;
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
- "Compare editions" when two browser-readable AI editions exist.

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

Potential relationship types:
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
- AI-generated "related" links not backed by corpus data;
- conflating GPT and Claude editions into one document;
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

# 21. Recommended first dispatch

Run these first.

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
