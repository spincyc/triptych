Triptych — World-Class Corpus Web Experience
Master multi-agent plan and execution instructions

Purpose: transform the non-PDF Triptych web experience into a coherent, world-class scholarly corpus interface while preserving the PDFs as the canonical printable editions.

Agent split

    Codex = product / visual / interaction design owner.

    Claude = production implementation / coding / test owner.

    Codex may create disposable prototypes and test fixtures when necessary to communicate a design, but it must not become the owner of production application logic.

    Claude must implement the accepted design contract faithfully and must not casually redesign it during coding. If implementation uncovers a design conflict, record the conflict and return it for Codex disposition rather than silently changing the product.

    Both agents must persist durable knowledge, plan state, discoveries, decisions, blockers, and acceptance status in tracked repository files and commit coherent checkpoints.

This document is the starting instruction packet. Before doing work, each agent must inspect the repository's current tracked guidance and reconcile this plan with the live repository state.
1. Mission

Triptych should become a source like no other: not merely a library of PDFs or a collection of browser tools, but a single navigable scholarly corpus in which a reader can move naturally among:

    a publication;

    the source passage behind a claim;

    the work, edition, artifact, and rights state behind that passage;

    Scripture and commentary connected to it;

    a liturgical use of it;

    the historical act that changed it;

    a canon affected by it;

    parallel GPT / Claude treatments;

    printable canonical PDFs;

    stable URLs that function as citations.

The central design principle is:

    The corpus is the product. Pages are views into it.

The current liturgical reader is the visual benchmark, not a one-off exception. Its strengths—calm reading, disciplined measure, restrained chrome, useful first viewport, source honesty, responsive reflow—must become a site-wide design language without forcing every scholarly instrument into the same layout.

PDFs remain the canonical printable editions. Do not redesign or mutate PDF typography, pagination, or print semantics as part of this project unless an explicitly separate task says so.
2. Non-negotiable repository rules

Before changing anything, read and obey at minimum:

    AGENTS.md

    PROJECT-WORK.md

    promised-deliverables.toml

    guidance/the-shape.md

    guidance/repository.md

    guidance/editorial.md

    guidance/external-review-handoffs.md

    guidance/web-data.md

    the profile/guidance owning the surface being touched.

For liturgy:

    guidance/liturgy-browser-vision.md

    guidance/liturgy-browser-roadmap.md

    guidance/liturgy-reader-state.md

    any specific liturgical profile named by AGENTS.md.

For Catena:

    guidance/catena.md

    guidance/reading-plan-for-agents.md

    guidance/bibles-for-agents.md

    guidance/versification.md.

For Source Library:

    guidance/sources.md

    relevant rights / edition guidance.

For history and law:

    guidance/act-histories.md

    guidance/time-machine.md

    applicable law/source guidance.

The current repository explicitly treats external visual/product/architectural acceptance as an evidence handoff problem. Follow guidance/external-review-handoffs.md exactly unless this plan explicitly tightens it.
3. Working-directory / branch discipline

Do not use Git worktrees.

For parallel work, use separate full repository directories with separate branches. One agent task owns one branch and one checkout directory at a time.

Suggested names:

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

A task may start from main or from a specifically named accepted foundation commit. Record the exact base SHA in the durable plan and in every handoff.

Never merge unrelated branches just to get a preview. If a composed integration preview is needed, create a dedicated integration branch and record exactly what was merged into it.
4. Durable project memory

Create or update these tracked authorities early, before substantial implementation:
4.1 Site-wide product vision

Create:

guidance/corpus-browser-vision.md

It should become the governing site-wide product / visual / interaction architecture for every non-PDF public surface.

It must define:

    corpus-wide information architecture;

    global navigation;

    visual language;

    typography;

    reading surfaces;

    data-dense research surfaces;

    search and discovery;

    source/provenance presentation;

    edition / rights presentation;

    responsive behavior;

    accessibility;

    URL/citation behavior;

    performance;

    relationship to canonical PDFs;

    anti-patterns;

    definition of world-class completion.

It must explicitly state that the more specific liturgy-browser-vision.md continues to govern liturgical semantics and behavior. The site-wide vision must reuse, not weaken, its accepted principles.
4.2 Execution roadmap

Create:

guidance/corpus-browser-roadmap.md

This is the live execution ledger. Every work unit below gets:

    ID;

    owner agent;

    state;

    base commit;

    branch;

    dependencies;

    acceptance gates;

    evidence handoff;

    accepted/rejected disposition;

    follow-up findings.

4.3 Operational project register

Update:

PROJECT-WORK.md

with a concise top-level corpus redesign entry and links to the two tracked authorities above. Do not duplicate the entire roadmap there.
4.4 Continuity record

Use a task-specific tracked continuity file if repository convention permits it, or a documented task-specific build/agent-continuity/... exception consistent with current project practice.

The continuity record must always answer:

    what is being attempted;

    what is complete;

    what is not complete;

    what was learned;

    exact current branch/SHA;

    exact next action;

    any known failed approach;

    current external-review disposition.

Never leave decisive knowledge only in chat, terminal scrollback, an ignored ZIP, or an agent's memory.
5. Research synthesis: what to borrow, what not to copy

The design should study successful scholarly/reference systems without cloning any one of them.
Sefaria

Useful ideas:

    source text remains primary;

    linked commentary appears contextually;

    a resource/connection panel lets the reader pivot by relationship type;

    a library can expose both texts and interconnections as first-class data.

Triptych opportunity:

    go beyond generic "connections" by showing the typed evidentiary chain: work → edition → artifact → passage → claim/use/change.

Reference:

    https://www.sefaria.org/

    https://help.sefaria.org/hc/en-us/articles/18472472138652-Quick-Guide-Meet-the-Sefaria-Library-Resource-Panel

    https://developers.sefaria.org/docs/commentaries

Perseus / Scaife Viewer

Useful ideas:

    work/edition/translation identity is explicit;

    stable text navigation;

    deep philological reading tools can be adjacent to text without making the base text disappear;

    corpus browsing and text searching are distinct but connected tasks.

Triptych opportunity:

    make edition identity, rights, provenance, citation loci, and source transitions even more explicit and visually coherent.

References:

    https://scaife.perseus.org/

    https://www.perseus.tufts.edu/

    https://perseus.pubpub.org/

Digital Vatican Library / IIIF

Useful ideas:

    treat exact artifacts as first-class objects, not just "documents";

    high-resolution witnesses can be presented with durable metadata and interoperable identity;

    IIIF is worth designing toward if manuscript/image witnesses become important.

Triptych opportunity:

    do not prematurely implement IIIF unless actual artifact needs justify it, but keep the source-library information architecture compatible with exact-witness viewing.

References:

    https://digi.vatlib.it/

    https://iiif.io/

Corpus Thomisticum

Useful idea:

    a corpus can be organized around scholarly addressability and cross-reference rather than magazine-like presentation.

Triptych opportunity:

    retain this rigor while dramatically improving orientation, readability, responsive behavior, and discovery.

Reference:

    https://www.corpusthomisticum.org/

Accessibility / readable long-form references

Normative / strong implementation guidance:

    WCAG 2.2: https://www.w3.org/TR/WCAG22/

    WAI APG: https://www.w3.org/WAI/ARIA/apg/

    GOV.UK layout: https://design-system.service.gov.uk/styles/layout/

Retain the liturgical reader's existing accessibility commitments: semantic structure, keyboard operation, visible focus, reflow at 320 CSS px, 200% text enlargement, 400% zoom, forced colors, reduced motion, usable mobile targets, and no color-only semantics.
6. Target product architecture

Triptych should feel like one place with several purpose-built scholarly instruments.
6.1 Global corpus shell

Every non-PDF browser page should share:

    compact Triptych identity;

    clear current-domain identity;

    global corpus search / jump;

    predictable access to Home / Library / Sources / Scripture / Liturgy / History / Law / Catena;

    a persistent but quiet way to reveal related corpus objects;

    stable footer/legal/feedback treatment;

    consistent focus and responsive behavior.

The shell must remain quiet. Do not turn every page into a dashboard.
6.2 Home: "the corpus map"

The current homepage is a good inventory but visually functions as lists and tables. Replace the experience with an editorially calm map of the corpus:

    one strong statement of what Triptych is;

    immediate entrances by task, not just section;

    "Read today", "Find a text", "Trace a source", "Follow commentary", "See what changed", "Look up a canon";

    section/library discovery below;

    visible corpus scale only when it is accurate and generated;

    recent/featured material only if repository truth supports a deterministic rule—no hand-curated fake freshness;

    clear distinction between browser instruments and canonical PDFs.

6.3 Section libraries / Every Document

The section pages and Every Document should become a strong catalogue and collection browser, not HTML tables disguised as a website.

Requirements:

    faceted filters;

    fast search;

    group by subject / series / section;

    strong publication title;

    concise abstract;

    model/edition identity;

    length/revision metadata;

    obvious Read vs PDF;

    paired GPT/Claude issues treated as related editions, not independent random links;

    responsive list-first presentation;

    optional dense/table view for power users;

    stable URLs for filter state where useful.

6.4 Browser-readable publication pages

All generated "Read" versions of papers should receive a world-class long-form reader:

    controlled measure;

    meaningful heading hierarchy;

    location-aware TOC;

    footnotes/citations that are easy to inspect and return from;

    source links that open contextual detail without losing position;

    model/edition identity;

    canonical PDF action;

    previous/next only when a real series/order exists;

    print CSS may be useful, but the PDF remains the canonical printable edition;

    side-by-side GPT/Claude comparison may be a later capability, but the architecture should allow it.

6.5 Catena Omnia

The Catena should become a signature experience.

Wide screen:

    principal Scripture text as the anchor;

    commentary visually forms a chronological chain beside or immediately following the relevant extent;

    a restrained vertical chronology spine may be used;

    author/date/work/edition are easy to scan;

    commentary fragments remain distinct from mere attribution/acquisition leads;

    multilingual/original-language state is explicit;

    opening a fragment does not destroy reading position;

    connections to Source Library are one action away.

Mobile:

    one column;

    Scripture extent followed by the commentary attached to that extent;

    no two-column squeeze;

    chronological ordering remains obvious;

    disclosures preserve location.

Do not make every fragment a giant card.
6.6 Source Library

The Source Library should become Triptych's evidence observatory.

Core mental model must be visually obvious:

Work
  └─ Edition
      └─ Artifact
          └─ Passage

Recommended experience:

    global search + faceted discovery;

    list results with enough identity to distinguish near-duplicates;

    work detail page/panel;

    edition selector/timeline;

    artifact provenance and checksum as inspectable metadata, not primary visual noise;

    passage navigator;

    rights state and distribution basis are visible and unambiguous;

    "used by" / "cited by" / "comments on" / "governs" relationships when backed by structured data;

    exact downloadable/viewable source actions only when rights permit;

    withheld passages remain visible as records with the reason.

This is not a generic document repository. The object graph is the differentiator.
6.7 How the Missal Changed

Preserve the "Missal Line" concept but make it feel like a serious historical instrument:

    strong horizontal/vertical timeline depending on viewport;

    stations clearly distinguish promulgated acts from weaker printed witnesses;

    selection opens a focused change narrative;

    follow-one-prayer mode should feel like tracing a lineage;

    before/after semantic units should be readable, not raw diff noise;

    broken connectors and evidentiary uncertainty are visually meaningful without relying on color alone.

6.8 Canon Law

Design around the actual scholar/user entrance: the citation.

    canonical citation box is primary;

    Code structure becomes a navigable tree/outline;

    canon text/history/acts are coherent tabs or views, if APG-compliant tabs are the right pattern;

    temporal changes read as a legal timeline;

    unavailable copyrighted words are clearly distinguished from unread or unchanged text;

    acts can be entered from either the canon or act direction;

    copied URL should remain a citation-quality deep link.

6.9 Story of Salvation

Turn the current plan into a genuine reading journey:

    three depths are an explicit progression, not merely links;

    show current/selected translation;

    scripture books/epochs give orientation;

    progress is optional and local-only if added—do not require accounts;

    printable PDFs remain canonical;

    chapter/reading links should pivot naturally into Catena and Source Library.

6.10 Global cross-corpus search

This is a major differentiator and should be architected even if delivered incrementally.

One search affordance should eventually be able to return typed results:

    publication;

    work;

    edition;

    artifact;

    passage;

    Scripture citation;

    Catena commentary fragment;

    liturgical formulary;

    historical act;

    canon.

Results must not flatten these into one undifferentiated list.

Each result says what kind of thing it is, why it matched, and what the user can do next.

Potential shortcut:

    desktop command/jump palette;

    mobile full-screen search sheet.

Do not ship a fake "global search" that only searches page titles.
7. Visual language

Codex owns the exact design system, but it should begin from these constraints.
Character

    serious but not austere;

    ecclesial without faux-medieval decoration;

    scholarly without looking like database admin software;

    contemporary without "startup SaaS" cards everywhere;

    warm and readable rather than sterile;

    restrained liturgical/source red as semantic accent, not wallpaper;

    typography carries most hierarchy.

Typography

    optimize primary reading surfaces around ~60–72 characters per line;

    body text effectively at least 16px;

    long-form line-height around 1.5 or better;

    left aligned, not forced justification;

    Greek, Latin, Hebrew, and special symbols must have excellent fallback behavior;

    tabular numerals where dates/canons/verse references benefit;

    metadata visibly subordinate but never illegible.

Surfaces

Use three related surface archetypes rather than one universal layout:

    Reader — papers, Scripture, liturgy, passages.

    Catalogue — Home, sections, Every Document, search.

    Instrument — Catena, Source Library, Missal history, Law.

All share tokens and shell; each has purpose-built composition.
Cards

Cards are allowed only when a bounded object genuinely benefits from containment.
Do not turn:

    every paragraph;

    every Proper;

    every commentary fragment;

    every source;

    every filter result
    into floating rounded rectangles.

Ornament

Use iconography/symbols only when they clarify domain or state.
Avoid decorative pseudo-manuscript texture, fake parchment, excessive crosses, illuminated initials, page-turn effects, glowing gradients, and ornamental borders that reduce scholarly credibility.
8. Full parallel execution plan

The table is intentionally segmented so independent branches can move concurrently once their small shared dependencies are sealed.
ID	Segment	Agent	Parallel lane	Depends on	Primary output	Acceptance evidence
A0	Repository/site inventory	Codex	Foundation	none	complete route/surface matrix; screenshots; design debt map	ZIP with route inventory + representative captures
A1	Corpus UX research synthesis	Codex	Foundation	none	precedent analysis + Triptych-specific principles	sources.md, design memo, explicit recommendations
A2	Site-wide product vision	Codex	Foundation	A0/A1	guidance/corpus-browser-vision.md	tracked commit + review ZIP
A3	Design tokens + three archetypes	Codex	Foundation	A2	visual system prototype for Reader/Catalogue/Instrument	desktop/mobile/zoom captures
A4	Shared shell interaction spec	Codex	Foundation	A2	global nav/search/related-object shell prototype	keyboard/mobile/overflow evidence
B0	Shared shell implementation	Claude	Foundation	accepted A3/A4	shared CSS/JS/HTML primitives	tests, a11y checks, screenshots
B1	Design-system regression harness	Claude	Foundation	A3	viewport, zoom, forced colors, keyboard, console test harness	reproducible commands + logs
C0	Homepage + section libraries design	Codex	Catalogue	A2/A3	home + 2 representative section prototypes	before/after matrix
C1	Every Document / catalogue design	Codex	Catalogue	A2/A3	faceted catalogue + publication-edition presentation	filter/mobile/empty-state captures
C2	Catalogue implementation	Claude	Catalogue	C0/C1/B0	production Home/sections/text catalogue	focused tests + production-like captures
D0	Browser-readable paper design	Codex	Reader	A2/A3	long-form article reader + citations/TOC/PDF action	long paper desktop/mobile evidence
D1	Article reader implementation	Claude	Reader	D0/B0	reusable paper reader styling/behavior	sample corpus matrix
E0	Catena signature redesign	Codex	Catena	A2/A3	Scripture/commentary chain interaction + responsive states	multiple chapter/comment density states
E1	Catena implementation	Claude	Catena	E0/B0	production Catena	model tests, DOM/a11y, real-data captures
F0	Source Library evidence-observatory design	Codex	Sources	A2/A3	work→edition→artifact→passage explorer	rights/readable/withheld/multi-edition states
F1	Source Library implementation	Claude	Sources	F0/B0	production Source Library	data-parity tests + a11y + real records
G0	Missal history redesign	Codex	History	A2/A3	Missal Line + prayer lineage visual spec	branch/station/broken-line states
G1	Missal history implementation	Claude	History	G0/B0	production history instrument	semantic + viewport regression
H0	Canon-law redesign	Codex	Law	A2/A3	citation-first canon/history/act UX	public-domain/withheld/unchanged states
H1	Canon-law implementation	Claude	Law	H0/B0	production law instrument	deep-link + a11y + state tests
I0	Story of Salvation redesign	Codex	Scripture	A2/A3	3-depth reading journey + pivots	desktop/mobile and all three depths
I1	Scripture implementation	Claude	Scripture	I0/B0	production Scripture plan	translation + route tests
J0	Global typed search architecture	Codex	Search	A2 + inventory	search UX, result taxonomy, command palette/sheet	query/result-state prototype
J1	Search data feasibility / index design	Claude	Search	J0	generated search index architecture with size/perf budget	index metrics + tests
J2	Global search implementation	Claude	Search	J1/B0	typed cross-corpus search	representative multi-domain queries
K0	Cross-object relationship UX	Codex	Graph	E/F/G/H/I designs	contextual "related corpus" model	task walkthroughs
K1	Cross-object link implementation	Claude	Graph	K0 + owning surfaces	source/catena/liturgy/history/law pivots	link integrity + deep-link tests
L0	Mobile coherence review	Codex	Acceptance	C–K designs	site-wide 320/393/tablet review	screenshot/contact-sheet ZIP
L1	Accessibility acceptance	Claude + Codex judgment	Acceptance	implemented surfaces	WCAG 2.2 AA evidence on core flows	keyboard/zoom/forced-color/SR notes
L2	Performance acceptance	Claude	Acceptance	implemented surfaces	route budgets + measured regressions	reproducible performance logs
L3	Visual cross-site acceptance	Codex	Acceptance	implementation complete	consistency audit against accepted visual contract	full route matrix ZIP
M0	Integration / cutover	Claude	Integration	accepted lanes	clean integration branch/main commits	full gates + Pages verification
M1	Final independent corpus review	Codex	Acceptance	M0	world-class completion disposition	immutable final handoff ZIP
Parallelization rule

After A2/A3/A4 are accepted and B0 establishes the shared shell contract, lanes C, D, E, F, G, H, I, and much of J may run in parallel.

Do not block a lane on unrelated surface implementation.

Codex design lanes can run before B0 is fully implemented if they all consume the same accepted token/archetype contract.

Claude implementation lanes should rebase/merge the accepted shared foundation before coding and should not each reinvent shared primitives.
9. Codex task protocol — visual/product agent

Every Codex task must follow this sequence.
9.1 Orient

    Read required guidance.

    Read site-wide vision/roadmap.

    Inspect current production page and source files.

    Record exact base SHA.

    Update roadmap state to in-progress.

    Create/update continuity record.

9.2 Audit before designing

For the owned surface:

    enumerate real user tasks;

    enumerate all meaningful data states;

    enumerate loading/empty/error/partial/withheld/unsupported states;

    inspect desktop, tablet, 393×852, 320-wide, 200% text, and representative zoom;

    identify what existing behavior is semantically required;

    identify what is merely current styling and may be discarded.

9.3 Design

Produce:

    one primary recommended direction;

    no "three themes, choose one" unless there is a real unresolved product fork;

    exact interaction behavior;

    responsive behavior;

    hierarchy/tokens;

    semantic component names;

    states and transitions;

    acceptance criteria.

Disposable prototypes are encouraged when they materially improve judgment. Keep them clearly outside production ownership.
9.4 Sanity check

Ask:

    Is the text/corpus object still primary?

    Does this look like a scholarly corpus, not SaaS?

    Can a new user understand where they are?

    Can an expert move faster than before?

    Is provenance more legible, not less?

    Are unavailable/uncertain states still truthful?

    Does mobile become a coherent single-column experience rather than crushed desktop?

    Is every added visual object earning its space?

    Are we using one of the three archetypes intentionally?

    Is a card being used only because it represents a bounded object?

9.5 Persist

Before handoff:

    update guidance/corpus-browser-roadmap.md;

    update the surface's owning guidance where a durable rule was learned;

    update PROJECT-WORK.md only if the top-level project state materially changed;

    commit the tracked knowledge before producing the handoff.

9.6 Return evidence ZIP

Use guidance/external-review-handoffs.md.

For visual tasks, the ZIP must contain:

    HANDOFF.md

    REVIEW_REQUEST.md

    changes.patch

    checks.txt

    sources.md when research informed the work

    screenshots/

    prototype files needed for review

    a route/state matrix

    before/after captures where applicable.

REVIEW_REQUEST.md must ask specific blocking questions. Never ask only "does this look good?"
10. Claude task protocol — implementation agent

Every Claude task must follow this sequence.
10.1 Orient

    Read repository guidance.

    Read accepted Codex handoff / design spec.

    Read corpus vision/roadmap.

    Inspect existing data models and tests.

    Record exact base SHA.

    Update roadmap and continuity.

10.2 Implement without semantic drift

    preserve source/data ownership;

    preserve stable URLs unless the accepted design explicitly changes/canonicalizes them;

    do not put data truth into CSS/DOM hacks;

    do not duplicate renderers where shared semantic objects exist;

    keep generated-data architecture additive;

    lazy-load heavy apparatus where appropriate;

    preserve rights/coverage distinctions;

    use semantic HTML first, ARIA only where needed.

If the design cannot be implemented without violating a repository invariant:

    stop that design choice;

    record the exact conflict;

    implement the largest safe subset if independently useful;

    return a blocker for Codex.

Do not silently "simplify" the design.
10.3 Test

At minimum, per affected core route:

    deterministic unit/model tests;

    browser rendering;

    console/request/HTTP error checks;

    keyboard navigation;

    focus visibility/restore;

    393×852;

    320 CSS px;

    200% text;

    representative 400% zoom/reflow;

    forced colors;

    reduced motion where motion exists;

    print rules where relevant;

    direct deep-link startup;

    legacy URL fixtures if affected.

10.4 Persist and commit

Commit:

    implementation;

    regression tests;

    durable implementation discoveries;

    roadmap state;

    relevant guidance corrections.

Never make a "code only" commit that leaves the tracked plan lying about the state.
10.5 Evidence ZIP

Return a handoff ZIP under the standard protocol including:

    exact commit and base;

    focused patch;

    checks with numeric exit codes;

    relevant logs;

    screenshots;

    preview/start commands;

    known limitations;

    exact blocker questions, if any.

11. Evidence package standards for seamless browser review

The user will paste ZIP files back into ChatGPT for independent review. Optimize every handoff for that workflow.
Required characteristics

    exactly one timestamped top-level directory in each ZIP;

    no credentials or machine-private data;

    no giant caches/build trees;

    no dependency directories;

    no irrelevant screenshots;

    no raw full build logs unless a failure depends on them;

    all paths repository-relative inside documentation;

    manifest/inventory of included artifacts;

    SHA-256 of ZIP recorded in final task response and optionally in HANDOFF.md;

    exact git SHA;

    exact base SHA;

    exact public/local routes;

    exact viewport names.

Suggested screenshot matrix

Every visually significant surface should normally include:

<route>--default--1440x1000.png
<route>--default--1024x768.png
<route>--default--768x1024.png
<route>--default--393x852.png
<route>--default--320x800.png
<route>--text-200pct--393x852.png
<route>--forced-colors--393x852.png

Add state-specific captures rather than mechanically duplicating all sizes when the state—not viewport—is what matters.

For redesigns, include comparable:

before--...
after--...

Reviewer-oriented contact sheet

For any handoff with more than ~12 screenshots, generate:

    screenshots/CONTACT-SHEET.png

    screenshots/INDEX.md

The index maps filename → route → state → viewport → what the reviewer should inspect.

This dramatically reduces back-and-forth.
12. Design details by segment
12.1 Home and section libraries

Codex should specifically test:

    first-time visitor;

    returning reader who knows the domain but not title;

    user seeking today's Mass;

    user seeking a specific paper;

    user seeking "where did this claim come from?";

    user wanting all material on one subject;

    mobile navigation without scrolling through giant lists.

Do not simply replace tables with card grids.

Preferred direction:

    task entrances near top;

    domain collections below;

    list/table switch only if justified;

    generated metadata for scale and freshness;

    restrained editorial hierarchy.

12.2 Every Document

Must handle:

    paired GPT / Claude documents;

    one-model-only publication;

    PDF-only issue;

    browser-readable issue;

    synthesis issue;

    long titles;

    multiple series;

    revision dates;

    filters with zero results;

    deep-linked filter state;

    mobile.

Potential power feature:

    "Compare editions" when two browser-readable AI editions exist.

Do not make comparison part of the first milestone unless data/reader architecture makes it straightforward.
12.3 Article reader

Codex should inspect representative papers:

    short essay;

    very long reference;

    citation-heavy study;

    tables;

    bilingual/Greek/Latin passages;

    headings 3+ levels deep;

    footnotes/endnotes;

    long bibliography.

The design must gracefully support the hardest paper, not only an ideal prose essay.
12.4 Catena

Must test:

    chapter with no held commentary;

    chapter with few fragments;

    dense chapter;

    overlapping extent;

    cross-chapter fragment;

    English-only;

    Latin/original plus translation;

    disputed attribution;

    known-but-not-acquired lead;

    unpublishable/withheld source;

    long fragment;

    many authors from similar period.

Visual distinction between:

    Scripture;

    actual held fragment;

    metadata/provenance;

    acquisition lead
    must be immediate and not depend on color.

12.5 Source Library

Must test:

    one work / one edition;

    one work / many editions;

    same language / multiple editions;

    artifact with readable passages;

    artifact present but not distributable;

    passage withheld for rights;

    exact provenance/hash inspection;

    work used in multiple Triptych products;

    author with many works;

    search alias;

    unknown/unsettled rights.

Codex should prototype a "progressive disclosure" model so hash/legal detail is fully available but not the first thing ordinary readers confront.
12.6 History

Must test:

    simple linear succession;

    branch;

    missing intermediate edition;

    promulgated act;

    printed witness only;

    many changed units;

    prayer appears/disappears/reappears if corpus permits;

    mobile lineage.

12.7 Law

Must test:

    exact canon;

    subsection citation;

    invalid citation;

    canon never changed;

    canon changed multiple times;

    text readable;

    text withheld by rights;

    unread canon;

    act touching one canon;

    act touching an entire Book.

12.8 Search

Typed result taxonomy should be explicit, e.g.:

PUBLICATION
SOURCE WORK
SOURCE EDITION
SOURCE PASSAGE
SCRIPTURE
COMMENTARY
MASS / FORMULARY
ACT
CANON

Result groups should be rankable but never semantically flattened.

Search should understand identifiers/citations especially well:

    John 20:6-7

    c. 1095 §2

    stable source IDs

    Mass keys/slugs

    known aliases/titles.

13. Cross-corpus relationship model

A signature Triptych capability should be a consistent way to answer:

    What else in the corpus is connected to what I am reading?

Do not implement this as a generic AI recommendation engine.

Use only structured, auditable relationships.

Potential relationship types:

    cites

    quotes

    comments_on

    translation_of

    edition_of

    artifact_of

    passage_of

    used_by

    governs

    changes

    supersedes

    compares

    appointed_in

    discussed_by_publication

The UI may summarize these into human categories:

    Sources

    Commentary

    Liturgical uses

    Changes

    Law

    Publications

But the underlying type must remain known.

Codex designs the interaction.
Claude verifies what structured edges actually exist and implements only real ones.
14. Search/index technical direction for Claude

Do a feasibility study before committing to architecture.

The site is GitHub Pages, so global search should preferentially remain:

    static/generated;

    cacheable;

    deterministic;

    versioned with the corpus;

    no server dependency required for the core product.

Investigate:

    generated compact JSON index;

    split per entity/domain if size requires;

    pre-normalized search keys;

    citation recognizers before generic fuzzy search;

    lazy-loading result detail;

    route-specific deep links;

    language-aware normalization without destroying Greek/Latin identifiers.

Measure:

    compressed index size;

    parse time;

    main-thread cost;

    query latency;

    memory on representative mobile hardware.

Do not add a heavyweight framework/search library without measured need.
15. Accessibility gate

The site-wide redesign targets WCAG 2.2 AA across core workflows.

Required manual/mechanical evidence:

    landmarks/headings make sense with CSS disabled;

    all forms have labels;

    all interactive controls have accessible names;

    disclosure state is programmatic;

    modal/sheet focus is trapped/restored appropriately;

    no hidden content remains focusable;

    no sticky UI obscures focused elements;

    target size/spacing is practical on touch;

    no horizontal page scroll at 320 CSS px except genuinely two-dimensional content that transforms appropriately;

    200% text and 400% zoom preserve function;

    forced colors preserve semantic boundaries;

    reduced motion respected;

    loading/status updates do not spam screen readers;

    tables retain proper semantics when tables are actually the correct structure;

    visual state is never color-only.

16. Performance gate

Preserve the accepted liturgical reader performance philosophy across the site.

Each route should have a measured baseline and budget.

Priorities:

    real useful content in first viewport;

    avoid loading source detail the reader has not requested;

    avoid shipping the entire corpus to render one page;

    lazy-load commentary fragment text only as allowed by existing Catena semantics;

    split global search/index if needed;

    minimize layout shift;

    no font strategy that creates excessive FOIT/FOUT or breaks Greek/Latin rendering;

    avoid framework migration unless clearly justified.

Record LCP/INP/CLS or reproducible lab proxies for representative routes where tooling supports it.
17. Anti-patterns — reject these even if they look polished

    generic dashboard home page;

    giant hero art that pushes corpus access below the fold;

    one card per object;

    ubiquitous rounded rectangles and shadows;

    faux parchment;

    medieval cosplay;

    decorative crosses as bullet points;

    gradient-heavy "AI" aesthetic;

    hidden navigation on desktop for the sake of minimalism;

    mobile pages that begin with huge forms;

    permanent sidebars that squeeze reading measure;

    a source page that presents hashes/rights tables before basic work identity;

    a Catena that looks like a comment thread;

    a history view that is only a raw diff;

    a law view that looks like a CRUD admin screen;

    untyped search results;

    AI-generated "related" links not backed by corpus data;

    conflating GPT and Claude editions into one document;

    weakening rights/provenance detail to make the interface cleaner;

    changing canonical PDF output as collateral damage;

    silently substituting missing text from another edition/translation.

18. Sanity-check questions before every acceptance

The reviewer should be able to answer yes to all applicable questions:

    Is it immediately clear what object I am looking at?

    Is the primary text/object visually dominant?

    Can I get to the source/provenance without losing my place?

    Can I tell edition, translation, rights, and uncertainty apart?

    Is the page calmer than a dashboard?

    Does it still work as a power tool?

    Is mobile intentionally recomposed?

    Is 320px reflow usable?

    Do keyboard/focus interactions behave predictably?

    Are stable URLs still meaningful citations?

    Are PDFs still clearly the canonical printable form?

    Does the surface feel unmistakably part of the same Triptych system as the liturgical reader?

    Does the surface retain a distinct composition appropriate to its task?

    Does every visual embellishment convey information or hierarchy?

    Are all corpus relationships shown here actually backed by repository data?

    Could an expert use this for serious research rather than merely admire it?

    Could a newcomer understand the next action without reading a manual?

    Is any important truth hidden merely because it is visually inconvenient?

19. Integration and merge discipline

Parallel branches are expected.

For each accepted lane:

    the lane's design disposition is recorded;

    Claude implementation is green on its focused gates;

    external review ZIP is accepted;

    the roadmap marks the lane accepted;

    only then is it eligible for integration.

Integration should be mechanical where possible:

    shared foundation first;

    catalogue/reader/instrument lanes next;

    cross-object links/search after owning surfaces;

    final acceptance last.

When merging reveals a conflict:

    classify it as code conflict, shared-component conflict, or product-semantic conflict;

    code conflicts may be resolved by Claude;

    shared-component visual conflicts must preserve the accepted foundation contract;

    product-semantic conflicts return to Codex for disposition.

Do not solve a product conflict by whichever branch happened to merge last.
20. What each agent should print when it finishes a task

Every agent response must be concise and machine-reviewable.

Print:

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

If a field is not applicable, print None.

Do not claim:

    deployed,

    accepted,

    complete,

    green,
    unless the exact governing gate was actually satisfied.

21. Recommended first dispatch

Run these first.
Dispatch 1 — Codex: Foundation audit and site-wide visual/product architecture

Give Codex this file and say:

    Execute A0–A4 only. Do not redesign production code beyond disposable prototypes required for external visual judgment. Inspect the whole public site and all owning web source directories. Reconcile with the accepted liturgical reader foundation. Create the site-wide corpus vision and roadmap, define the three surface archetypes, define the shared shell, and return one standard external-review ZIP. Persist and commit every durable plan/discovery before packaging the handoff. Do not use Git worktrees.

Expected result:

    one committed foundation design branch;

    durable corpus vision;

    durable roadmap;

    prototype/evidence package;

    exact questions for independent review.

Dispatch 2 — Claude: implementation feasibility, but no visual invention

Claude may begin in parallel on a separate branch with:

    Audit the current shared browser architecture and test harness for B0/B1 feasibility only. Do not implement a new visual direction until the A3/A4 Codex contract is accepted. Identify reusable shared CSS/JS, generator seams, test coverage, route inventory, and likely implementation risks. Persist/commit the technical discovery record and return a standard handoff ZIP.

This lets coding reconnaissance run while visual architecture is being reviewed without allowing Claude to preempt the design.
22. Definition of done for the whole corpus redesign

This project is not complete merely because every page uses the same fonts/colors.

World-class completion requires:

    the homepage clearly exposes the corpus as a connected research environment;

    every section/library surface is first-rate on desktop and mobile;

    browser-readable papers have a serious long-form reading experience;

    Catena is a signature commentary instrument;

    Source Library makes work/edition/artifact/passage relationships understandable;

    liturgical reader quality is preserved;

    Missal history communicates lineage and evidence clearly;

    Canon Law is citation-first and legally coherent;

    Story of Salvation is a genuine reading journey;

    global typed search reaches the major corpus object classes;

    structured cross-corpus pivots connect sources, commentary, liturgy, history, law, and publications;

    provenance/rights/uncertainty remain at least as truthful as before;

    PDFs remain canonical printable artifacts and are not collateral redesign targets;

    core workflows meet accessibility gates;

    route budgets/performance are measured;

    responsive behavior is intentionally designed across the site;

    all accepted behavior is regression-tested;

    every milestone has immutable evidence ZIPs suitable for independent browser review;

    durable repository guidance tells the next agent exactly why the system is shaped this way.

The desired end state is not "a prettier website."

It is a scholarly instrument whose visual hierarchy reveals the structure of the corpus itself.
Coordinator review and execution update — 2026-08-08

This section supersedes any earlier instruction in this master plan that conflicts with it. It is the independent coordinator disposition after review of both foundation branches.
Reviewed remote state

At review time:

    origin/main: c27d6915319785686d1df6a1401a489aa9921f6f

    Codex design branch ux/foundation: 3b5938a0dba88831763ec09c762ae1572007a27e

    Claude implementation branch impl/foundation: af2c9613ccda48679face4e43f59c002f93056ef

    Both branches began from the same exact base c27d6915319785686d1df6a1401a489aa9921f6f.

Agents MUST fetch before starting. If origin/main no longer equals that SHA, do not reset, force-push, or assume the old base is current. Record the new main SHA, preserve unrelated mainline work, and perform the same integration onto current main.
Independent disposition
Work	Owner	Disposition	Binding note
A0 whole-site inventory	Codex	ACCEPT	Treat the route/object/ownership inventory as downstream input. Refresh counts only when release contents change materially.
A1 research synthesis	Codex	ACCEPT	The borrow/reject/exceed framing is useful. No framework or IIIF migration is authorized merely because it was researched.
A2 product / corpus architecture	Codex	ACCEPT WITH AMENDMENTS BELOW	“The corpus is the product; pages are typed views into it” is the governing product model.
A3 visual system + Reader/Catalogue/Instrument	Codex	ACCEPT AS FOUNDATION DIRECTION	This authorizes implementation of the shared non-liturgy foundation and further real-data prototypes. It is NOT pixel-level acceptance of any production route. Every real surface still needs screenshot review.
A4 shell / Jump / contextual navigation	Codex	ACCEPT WITH AMENDMENTS BELOW	Jump remains a bounded fixture until J0–J2. Related is typed navigation, never recommendation inference.
B0/B1 reconnaissance	Claude	ACCEPT	Claude found the actual generator seams, shared-code drift, URL constraints, rights constraints, and live WIP collisions. These findings are binding implementation input.
Neutral static/browser gates	Claude	ACCEPT FOR INTEGRATION	Integrate the JS/static parsing gate and generated-artifact browser gate. Known inherited failures remain findings, not excuses to rewrite unrelated areas.
Production shell	Claude	AUTHORIZED NEXT, NON-LITURGY FIRST	Implement only after the accepted coordinator amendments are present on the shared integration branch.
What this acceptance does and does not mean

This review accepts the product model and enough of the design contract to unblock real implementation and real-data design work. It deliberately does not declare the synthetic prototype itself a finished visual product. The ignored screenshot ZIP was not available through the pushed Git branch, so the next Codex handoff MUST include the external-review ZIP for direct browser review. Real routes, real titles, real source metadata, real absence/rights states, and real mobile composition are the next visual oracle.
Binding coordinator amendments / dispositions

These decisions answer the Codex blockers and Claude C1–C16 conflicts. Record them durably in the integration branch rather than leaving them only in this handoff.
D1 — /texts/ public label

Accept Publications as the compact global label for /texts/.

    Do not rename the route.

    Do not create a second canonical publication home.

    The existing one-owning-catalog rule remains authoritative.

    The Publications browser may aggregate discoverability, metadata, browser-read links, and facets, but it may not create a second owning PDF catalogue.

D2 — protected liturgy adapter

Accept the exclusive liturgy adapter. Canonical Day and Propers are a protected surface family.

Until the current Live Reader — Ritual Flow & Orientation work is independently closed or explicitly carved out:

    do NOT modify reader-shell.js;

    do NOT modify reader-instrument.css;

    do NOT modify canonical liturgy/day.html or liturgy/index.html source ownership;

    do NOT add a fifth primary reader action;

    do NOT add a second competing modal owner;

    do NOT add a literal corpus masthead above the accepted reader;

    do NOT redesign its print behavior;

    do NOT merge site-wide Search into the reader shell.

The corpus project may design a future low-chrome corpus exit/context affordance for liturgy, but it must enter through an already accepted seam such as Details or a quiet terminal/footer treatment and must receive its own liturgy-specific visual acceptance. The accepted first viewport remains sacred.
D3 — provider terminology

Reject “parallel provider treatment” as primary public wording.

Use:

    Independent treatment as the human-facing label when distinguishing independently produced ChatGPT/Claude treatments.

    Parallel treatment as a relationship label when two treatments of the same work are intentionally connected.

    Always show the provider as explicit metadata rather than baking provider jargon into the relationship name.

Never call these Source Library editions unless they actually satisfy the edition model.
D4 — three archetypes

Accept Reader / Catalogue / Instrument as the site-wide archetypes.

They share identity, tokens, spacing logic, accessibility behavior, URL discipline, and contextual-navigation grammar. They do not share one universal layout.
D5 — visual tokens are roles, not frozen pixels

Accept the warm-paper / near-black / restrained-oxblood / blue-focus direction, disciplined serif reading axis, UI sans stack, square/quiet controls, rules rather than card walls, and restrained chrome.

But:

    exact type sizes, especially the synthetic prototype's very large display headings, are not frozen;

    exact desktop masthead density is not frozen;

    exact spacing values may move after real-data screenshots;

    no production design may rely on Inter actually being installed;

    use robust system/local fallback stacks unless a separately authorized font+rights+generator work unit proves a self-hosted font worth its cost;

    test long real titles, multilingual text, Latin, polytonic Greek where applicable, narrow screens, and Windows/Linux/macOS font fallback before calling typography settled.

D6 — global navigation

Accept the information architecture, not the exact count/geometry of visible desktop links in the synthetic prototype.

Top-level corpus destinations remain:

    Publications

    Sources

    Scripture

    Liturgy

    History

    Law

    Commentary

The Triptych wordmark itself is a Home affordance; a separate visible Home item is optional and should survive only if real 1024px and 200% evidence shows the masthead still reads calmly. Lower-priority destinations may collapse to Menu earlier than the prototype if density warrants it. Do not solve density with tiny text.
D7 — homepage and seven portals

Do not throw away the seven editorial identities merely to make the homepage look new.

Wave 1 should prototype:

    a task-oriented corpus entrance layer — read, find, trace, follow, compare/change, look up;

    the seven existing editorial portals beneath or beside it as durable corpus orientation;

    direct movement into Publications, Sources, Commentary, Liturgy, History, Law, and Scripture without turning the homepage into a dashboard.

Preserve the current seven portal names/order/color identities unless Codex demonstrates a materially better real-data alternative and explicitly proposes an amendment to guidance/repository.md. Do not silently break the generator's current README transform.
D8 — one owning catalogue

A faceted Publications surface is a discovery view, not a second ownership hierarchy. It may reveal all relevant treatments and formats, but each publication still has exactly one owning catalogue and canonical PDF home.
D9 — long-form web editions

guidance/web-editions.md is controlling for the publication Reader lane.

    Never create a second editable copy of publication prose.

    Do not edit web/<provider>/*.md merely to achieve UI presentation.

    Preserve visible rights colophon and revision identity.

    Any material omission remains explicitly declared.

    Re-run the web-edition currency checks after renderer/converter changes.

D10 — durable project memory

For the corpus redesign, durable truth belongs primarily in:

    guidance/corpus-browser-master-plan.md

    guidance/corpus-browser-vision.md

    guidance/corpus-browser-roadmap.md

    guidance/corpus-browser-implementation.md

    relevant owning guidance for each surface

    PROJECT-WORK.md

    promised-deliverables.toml

Do not depend on a force-tracked build/agent-continuity/* file for facts required by future agents. build/ may remain useful for ignored handoffs, screenshots, logs, and temporary continuity, but durable facts MUST also exist in the tracked guidance/ledger above. Do not integrate the Codex foundation continuity file as the sole owner of any fact.
D11 — screenshot matrix

Use one comparable site-wide matrix unless a more specific owning surface requires more:

    1440 × 900

    1024 × 768

    768 × 1024

    393 × 852

    320 × 852

Also exercise:

    200% text enlargement;

    exact 320-CSS-pixel reflow;

    400% zoom/reflow where meaningful;

    keyboard-only operation;

    forced colors;

    reduced motion;

    browser print for surfaces where print is not explicitly delegated only to canonical PDF;

    no-JavaScript/static truth;

    console/network/HTTP/accessible-name checks.

Do not create pixel-diff baselines before a real-data surface has independent visual acceptance.
D12 — assets and generator constraints

Until explicitly changed and tested:

    no webfont dependency;

    no icon library;

    no framework migration;

    no root-relative links that break GitHub Pages under /triptych/;

    no new asset type that the generator will reject;

    preserve HTML payload limits and the static/no-server deployment model.

D13 — Search / Jump

A4 Jump remains a bounded demonstration of interaction grammar only.

Production Search is J0 → J1 → J2:

    Codex defines typed search UX and states against real corpus objects.

    Claude benchmarks a public-only static index and proves no-leak, payload, latency, memory, multilingual, and route-state behavior.

    Claude implements only the selected measured design.

No route may pretend a title fixture is global search.
D14 — relationships

Contextual relationships are powerful enough to become a signature Triptych feature, but only where the corpus can prove them.

Currently safe categories include explicit containment, passage→artifact/segment, Catena fragment→Scripture locus, Catena passage→Source Library passage, act descent/change/history, document→catalogue page, and Mass→propers→Scripture resolution.

Do not synthesize translation_of, used_by, derived_from, canon correspondences, Law→Source citations, or generic “related” recommendations from title/keyword similarity. A new relationship is a schema/generator work unit under the owning corpus guidance before it is a UI feature.
D15 — rights, absence, and progressive disclosure

Progressive disclosure may defer:

    hashes;

    extended artifact provenance;

    long rights/legal apparatus;

    secondary technical metadata.

It may not defer or erase:

    required licence acknowledgement at point of use;

    a withheld-text reason;

    typed absence/unread/unsupported/invalid state;

    the distinction between availability and redistribution rights.

Every renderer must preserve these states semantically, not only through color or a CSS class.
D16 — local reading progress

Defer local reading progress from the current foundation wave. If introduced later for long-form publications, it must be storage-optional and an explicit URL always wins. Do not add persistence to Day; its current no-memory behavior is intentional.
D17 — browser architecture findings

Treat the following Claude findings as real engineering debt, not as permission for a rewrite:

    all generated surfaces pass through one layout seam;

    shared browser-core is widely adopted but oversized and unevenly used;

    history/law and Day/Propers contain localized duplicated helpers;

    several hash routers can create excessive browser-history entries;

    history currently has a missing none-claimed citation gloss;

    some generated pages have nested <main> landmarks;

    some generated states lose the expected first focus target/skip-link behavior;

    Source Library and Publications have measured 320px overflow in the current build;

    existing Chromium harnesses are useful and should become invoked, not discarded.

Fix these incrementally with path-specific commits and before/after gates. Do not turn B0 into a browser-stack rewrite.
D18 — current liturgy WIP collision

The current Live Reader — Ritual Flow & Orientation task remains a separate in-progress deliverable. This corpus project does not supersede it. If the owning liturgy work finishes during this project, re-read the new main state before touching any formerly protected seam.
D19 — commit / push authority

    Codex may make and push coherent feature/integration branch checkpoints under the repository's existing direct-Codex authority.

    Claude may commit and push its explicitly assigned feature branches for this project because the maintainer has requested these branch handoffs.

    Neither agent is authorized by this plan to merge/push to main or trigger public cutover. Main integration and Pages publication remain an explicit later decision.

    Never force-push or rewrite shared history.

D20 — separate full checkouts

Continue using separate full repository directories for parallel lanes. Do not use worktrees for this project. Never let two agents share one working directory/index.
Shared foundation integration — execute before the broad production fan-out
Owner: CODEX

Create a new full checkout and branch:

corpus/foundation-integration

Base it on current origin/main after fetching. At review time this is c27d6915319785686d1df6a1401a489aa9921f6f.

The purpose is not to merge all branch history blindly. Build one coherent accepted foundation commit series from the useful durable artifacts.

Integrate from ux/foundation:

    guidance/corpus-browser-inventory.md

    guidance/corpus-browser-research.md

    guidance/corpus-browser-vision.md

    guidance/corpus-browser-roadmap.md

    the synthetic foundation prototype and its focused tests

    the tracked master plan, updated to this v2 coordinator disposition

    the appropriate PROJECT-WORK.md / promise-ledger records

Integrate from impl/foundation:

    guidance/corpus-browser-implementation.md

    the AGENTS.md routing row(s), adjusted so future agents can find BOTH the design and implementation guidance

    the neutral browser/static syntax test target from Claude's 71875b7... work

    the built-artifact corpus browser gate from Claude's 67ae7d3... work

    the precise follow-up corrections through Claude head af2c9613...

Do NOT blindly integrate:

    duplicate/conflicting copies of the old master plan;

    branch-local stale PROJECT-WORK.md sections without manual reconciliation;

    the force-tracked build/agent-continuity/corpus-browser-foundation.md as a required durable owner;

    any production CSS/JS change to the protected liturgy files.

On the integration branch, update the durable records so they explicitly contain D1–D20 above and mark the reviewed foundation disposition accurately.

Suggested status language:

    A0: Accepted

    A1: Accepted

    A2: Accepted with coordinator amendments D1–D20

    A3: Accepted as foundation design direction; real production surfaces retain independent visual acceptance gates

    A4: Accepted with bounded-Jump / typed-Related / protected-liturgy amendments

    Claude reconnaissance: Accepted

    B0: Authorized in progress after this integration branch exists

    B1: Authorized in progress

Run the complete focused validation available on the integrated branch. Preserve inherited base failures as inherited findings; do not rewrite unrelated registries or stale examples to manufacture a green aggregate gate.

Push corpus/foundation-integration. Do not merge to main.

Return a compact integration ZIP with:

    base/head/branch;

    exact incorporated paths and source SHAs;

    conflict resolutions;

    disposition table;

    commands and numeric exit statuses;

    proof no canonical PDF changed;

    proof no protected liturgy production asset changed;

    exact next branch base for all downstream corpus work.

Work that may continue in parallel while Codex integrates

Claude does not need to sit idle while the integration branch is being assembled.
Owner: CLAUDE

Continue from impl/foundation on a new branch:

impl/foundation-hardening

Do only work that is mechanically cherry-pickable into the eventual integration branch and does not require final surface visual decisions:

    Wire the existing real-Chromium harnesses into explicit Make targets that correctly depend on a preview build.

    Improve the new site-wide generated-artifact browser gate without pixel baselines.

    Add route/state fixtures needed to reproduce current known structural defects.

    Fix safe, non-liturgy selector/helper collisions where the change can be proven visual-neutral:

        target-aware failure/banner plumbing;

        History .field collision;

        Publications/Texts .detail collision;

        similarly scoped non-liturgy collisions discovered during the audit.

    Add tests that lock current published URL/hash compatibility before any router cleanup.

    Prepare — but do not yet land across protected liturgy files — a reusable implementation plan for shared accessibility helpers and duplicated history/law utilities.

Do NOT:

    touch reader-shell.js;

    touch reader-instrument.css;

    touch canonical Day/Propers source ownership;

    scope/fix day-missal.css yet if doing so enters the live liturgy owner's paths;

    implement the global shell before the integration branch records D1–D20;

    alter real visual styling of the individual corpus instruments;

    build Search;

    infer new relationships;

    edit publication prose or PDFs.

Push impl/foundation-hardening. Return the standard ZIP. Everything must be independently cherry-pickable by path/commit.
Wave 1 — run Codex and Claude in parallel from the accepted integration branch

Once corpus/foundation-integration is pushed, all new Wave 1 work starts from its exact head.
CODEX — real-data visual/product wave

Branch:

ux/corpus-wave-1

Codex owns visual/product design only. Use the actual generated corpus, not synthetic titles, for the primary evidence.

Execute these design units:
ID	Surface	Goal
C0/C1	Home + Publications / Catalogue	Turn the root into a calm corpus map with task entrances plus the seven editorial portals; make Publications a serious list-first scholarly discovery surface rather than a giant table/card wall.
D0	Long-form publication Reader	Apply the accepted reading quality of the liturgy work to browser-readable publications while preserving provider, revision, colophon, canonical PDF, stable anchors, and source honesty.
E0	Catena Omnia	Make Scripture the anchor and commentary the chronological/typed chain. Design held fragment, attribution-only, unavailable, source link, voice/language, and narrow-screen states. This should become a signature Triptych instrument.
F0	Source Library	Make Work → Edition → Artifact → Passage perceptible without forcing forensic metadata into the first glance. Design readable, withheld, unread, rights-limited, artifact, and passage-deep-link states. This should become the corpus evidence observatory.
Wave 1 Codex requirements

    Start by rendering current real routes at the shared screenshot matrix.

    Design with real long titles, real multilingual/source metadata, real absences, and real provider differences.

    Reuse the foundation token roles, but adjust exact values when real evidence proves they are wrong.

    Keep primary content dominant. No dashboardification, no card-everything, no decorative ecclesiastical cosplay.

    Preserve existing URLs/hash keys and canonical PDF relationships.

    Do not modify production implementation; prototypes may be isolated/noindex.

    For each surface, record:

        primary user jobs;

        object being manipulated/read;

        first viewport target;

        information hierarchy;

        wide/narrow composition;

        keyboard/focus behavior;

        absent/unsupported/withheld/error states;

        exact contextual transitions to other corpus objects;

        what is deliberately NOT shown first.

    Treat the foundation prototype's desktop nav geometry and display-heading sizes as hypotheses, not commandments.

    Do not visually redesign the protected canonical Day/Propers routes in this wave.

Required Codex evidence ZIP

This ZIP is mandatory. The next independent review will not accept a visual lane from branch source alone.

Include:

    HANDOFF.md first;

    exact base/head/branch;

    numbered contact sheet;

    before/after pairs for every governed route;

    1440×900, 1024×768, 768×1024, 393×852, 320×852;

    representative 200% and 400%/reflow states;

    keyboard focus states;

    forced colors and reduced motion where behavior changes;

    open Menu/Jump/Related/Contents/filter states where applicable;

    at least one long-title stress case;

    at least one multilingual/source-heavy stress case;

    at least one withheld/unavailable/zero-result case per relevant instrument;

    browser print evidence for long-form publication Reader if the web page itself has a print treatment;

    visual review notes naming every compromise or unresolved question.

Push the branch and give the maintainer the ZIP to paste into ChatGPT for independent visual review.
CLAUDE — shared non-liturgy production foundation

Branch:

impl/corpus-wave-1

Base: exact head of corpus/foundation-integration.

Claude owns implementation and test architecture. Implement B0/B1 for non-liturgy public surfaces first, using the accepted design contract and D1–D20.
B0 implementation scope

    Establish the shared corpus-shell implementation at the single generator/layout seam.

    Make route/domain identity generated from one ordered source of truth.

    Implement non-liturgy masthead/navigation/Menu primitives with relative GitHub-Pages-safe URLs.

    Implement the accepted token roles in the appropriate shared CSS seam without assuming webfonts.

    Provide route-specific policy so canonical Day/Propers do not receive a visible literal corpus masthead or new modal owner.

    Preserve static/no-JS identity, core content, canonical PDF links, source/legal truth, and direct URL usefulness.

    Resolve nested landmark/skip-link issues at the lowest safe shared seam.

    Fix current 320px overflow in Sources and Publications without masking overflow globally.

    Keep all target sizes/accessibility semantics testable.

    Preserve current public paths and hash keys exactly.

    Do not promote reader-shell.js into the corpus shell while the liturgy Ritual Flow task owns it. Reuse ideas, not the owned file.

    Do not split/rewrite browser-core.js merely for aesthetics. Any extraction must be small, measured, dependency-safe, and independently testable.

B1 test scope

Build/invoke a site-wide browser gate that covers representative states of every non-PDF browser surface and asserts at minimum:

    no console errors/warnings that indicate a defect;

    no failed requests / HTTP failures;

    no unnamed interactive accessible nodes;

    valid single-main landmark structure;

    working skip link / first-focus semantics;

    no horizontal overflow at 320 CSS px;

    ≥44×44 primary interactive targets where required;

    useful behavior at 200% text and 400%/reflow;

    forced-colors and reduced-motion sanity;

    no-JS static identity/core truth;

    URL/hash compatibility;

    direct route loading on GitHub-Pages-style subpath;

    generated artifact, not merely repository source HTML.

Do not add visual pixel baselines before Codex surface acceptance.
Claude Wave 1 stopping line

Claude may implement the shared foundation and neutral structural fixes. Claude must NOT independently invent the final Home, Publication Reader, Catena, or Source Library composition before Codex returns the corresponding accepted D0/E0/F0/C0-C1 design evidence.

Where a surface needs styling beyond the shared foundation, create clearly bounded extension seams and stop.
Required Claude evidence ZIP

Include:

    HANDOFF.md first;

    exact base/head/branch and commit graph;

    changed-file inventory grouped by generator/shared shell/tests/surface;

    static and Chromium gate summaries with numeric exit codes;

    generated-route screenshots showing the shell only, not claiming visual acceptance of unfinished surfaces;

    320px overflow evidence before/after where fixed;

    landmark/skip-link evidence before/after;

    URL/hash compatibility report;

    payload/build-time deltas;

    known inherited failures clearly separated from introduced failures;

    proof protected liturgy files were not changed;

    proof PDFs were byte-unmodified;

    exact dependencies still waiting on Codex C0/C1/D0/E0/F0.

Push the branch and give the maintainer the ZIP to paste into ChatGPT.
Optional maximum-parallel design fan-out

If the maintainer launches multiple independent Codex sessions, Wave 1 may split further, but every worker MUST use a separate full checkout and branch from the same integration head:

    ux/catalogue — C0/C1

    ux/reader — D0

    ux/catena — E0

    ux/sources — F0

Do not let multiple workers edit the same durable roadmap/ledger files concurrently. Give one coordinator worker ownership of shared tracking documents; leaf workers return branch commits + ZIP evidence for that coordinator to record.

Likewise, if multiple Claude sessions are launched, safe sublanes are:

    impl/browser-gates — B1 only

    impl/shell — B0 shared non-liturgy shell only

    impl/structural-fixes — nested main / skip-link / measured overflow / selector collisions only

Again: separate full checkouts, one tracking owner, no worktrees, no shared index.
Wave 2 — do not start production implementation yet, but keep fully parallelizable

After Wave 1 design acceptance and B0/B1 foundation acceptance:
Design lane	Owner	Implementation lane	Owner	Dependency
G0 History	Codex	G1 History	Claude	accepted B0 + G0
H0 Law	Codex	H1 Law	Claude	accepted B0 + H0
I0 Scripture	Codex	I1 Scripture	Claude	accepted B0 + I0
J0 Search UX	Codex	J1 benchmark → J2 implementation	Claude	J0 before engine choice
K0 typed relationships	Codex	K1 projection	Claude	accepted owning surfaces + verified schema edges
L0 whole-site visual coherence	Codex	L1 accessibility / mechanical closure	Claude + Codex	all surface lanes
M0 integration/cutover candidate	Claude on feature branch	M1 independent acceptance	Codex + ChatGPT coordinator	explicit maintainer publication authorization
Next review protocol

For the next browser review, provide ChatGPT:

    Codex ZIP;

    Claude ZIP;

    branch names/head SHAs if they changed after ZIP creation.

ChatGPT will review the two handoffs together, compare screenshots against implementation evidence, record accept/reject/changes-required by lane, and issue the next parallel dispatch. The maintainer should not have to manually translate one agent's findings into instructions for the other.
Exact prompt — CODEX integration + Wave 1

Use this entire revised master plan as governing context.

You are the Codex visual/product coordinator for the Triptych corpus redesign.

First execute the narrow Shared foundation integration — CODEX section above on corpus/foundation-integration. Reconcile the accepted Codex and Claude foundation artifacts path-by-path; record D1–D20 durably; do not merge to main; do not touch protected liturgy production assets; push the integration branch and produce the compact integration ZIP.

Then, from the exact pushed integration head, create ux/corpus-wave-1 and execute C0/C1, D0, E0, F0 as real-data design/prototype lanes. The target is not generic consistency: Home/Publications, long-form reading, Catena Omnia, and the Source Library must each become purpose-built world-class surfaces within one coherent corpus language.

The accepted liturgy reader is the quality benchmark and protected exception. PDFs remain canonical printable editions. Preserve URLs, provenance, rights distinctions, provider identity, absence states, and static truth.

Persist every important discovery, decision, rejected alternative, route/state inventory, and progress update into tracked guidance/roadmap/project records. Do not rely on chat memory or ignored build files.

Return mandatory ZIP evidence exactly as specified. Push feature branches only. Do not merge or deploy main.
Exact prompt — CLAUDE hardening + Wave 1

Use this entire revised master plan as governing context.

You are the Claude implementation/testing coordinator for the Triptych corpus redesign.

Immediately continue safe parallel work on impl/foundation-hardening from current impl/foundation head af2c9613ccda48679face4e43f59c002f93056ef, limited to the mechanically cherry-pickable hardening tasks listed above. Do not touch protected liturgy files or invent visual product decisions.

When Codex pushes corpus/foundation-integration, fetch it, record its exact head, and create impl/corpus-wave-1 from that head. Execute B0/B1 for the shared non-liturgy production foundation exactly as specified above. Treat the Codex design contract and D1–D20 as binding; treat guidance/corpus-browser-implementation.md as the architecture/risk record; treat owning surface guidance as higher priority when more specific.

Do not rewrite the browser stack, do not build Search early, do not infer missing relationship edges, do not edit publication prose, do not alter canonical PDFs, and do not enter the in-progress liturgy Ritual Flow owner's files. Preserve public URLs/hash state and GitHub Pages subpath behavior.

Persist architecture discoveries, resolved hazards, measured deltas, tests, blockers, and exact dependencies into tracked guidance/roadmap/project records. Keep inherited repository failures distinct from regressions introduced by this work.

Return mandatory ZIP evidence exactly as specified. Push feature branches only. Do not merge or deploy main.

---

## 2026-08-08 dispatch disposition

> **Dispatch-only precedence boundary.** For the task dispatched on
> 2026-08-08, the task-specific repository-root `./directions` superseded only
> this plan's precursor instruction to create and push a
> `corpus/foundation-integration` branch before beginning Wave 1.

The dispatched work instead used these exact execution facts:

- base: `origin/main` at `c27d6915319785686d1df6a1401a489aa9921f6f`;
- working branch: `ux/corpus-wave-1`;
- selective foundation input: `origin/ux/foundation` at
  `3b5938a0dba88831763ec09c762ae1572007a27e`;
- selective implementation input: `origin/impl/foundation` at
  `af2c9613ccda48679face4e43f59c002f93056ef`.

This disposition makes no claim that the precursor integration branch existed
or that either input branch was merged wholesale. All D1-D20 dispositions and
all other v2 content remain preserved and governing except for that one
superseded branch-sequencing precursor.

### Wave 1 source-schema clarification

The plan's compact `Work → Edition → Artifact/Segment → Passage` language is a
reader-orientation shorthand, not a licence to invent structural containment.
The repository schema owns the precise relation: Work owns Edition; Artifact,
Segment, and Passage are edition-owned siblings; and a Passage separately
identifies its controlling Artifact, directly or through a Segment. A Segment
may resolve to an Artifact owned under another Work. Wave 1 evidence and later
implementation must show that controller relation explicitly where the public
projection carries it, and must record a generator gap rather than infer it
where the projection does not.

The plan's requested `unread` Source stress state is likewise a category to
verify, not permission to relabel inspected material. All 2,751 current Passage
records are inspected. The dispatched Wave therefore uses honest
`text-not-readable-here`, external-only, rights-withheld, unsupported, and
invalid states where the public projection proves them, and defers a true
unread state until repository-owned data can supply one.
