# Triptych corpus browser roadmap

## Status and authority

This is the detailed execution record for the non-PDF corpus experience
governed by [`corpus-browser-vision.md`](corpus-browser-vision.md).
`PROJECT-WORK.md` and `promised-deliverables.toml` remain the fail-closed
operational authorities for what is promised and complete. This roadmap records
the work-unit detail, evidence gates, and review dispositions they link to; it
does not grant production implementation, integration, publication, or
acceptance authority by itself.

The more specific [`liturgy-browser-vision.md`](liturgy-browser-vision.md)
continues to govern liturgical identity, semantics, state, navigation, and
reader behavior. Canonical Day and Propers are a protected surface family in
this wave. No corpus work may add a literal global masthead, fifth primary
action, second modal owner, Search integration, print redesign, or a competing
visual direction there.

PDFs remain the canonical printable editions. Wave 1 owns visual/product design
and isolated real-data prototypes; it does not own production application logic
or publication prose.

## Exact branch, base, and imported provenance

The A0-A4 foundation began from exact `origin/main` commit
`c27d6915319785686d1df6a1401a489aa9921f6f` on `ux/foundation`. The foundation
roadmap and A4 prototype record were selectively taken from
`ac37b6ffa6022dbab551385d91a12e277bb816cb`; the reviewed Codex foundation head
is `3b5938a0dba88831763ec09c762ae1572007a27e`. Accepted implementation and
architecture findings were inspected at Claude head
`af2c9613ccda48679face4e43f59c002f93056ef`. These SHAs identify reference
inputs; no foundation commit was merged as ancestry.

The current task-specific dispatch supersedes the v2 plan's integration-first
sequence for this Codex wave. `ux/corpus-wave-1` starts directly from exact
current `origin/main` commit
`c27d6915319785686d1df6a1401a489aa9921f6f` and carries forward only accepted
foundation knowledge and required artifacts path by path. The proposed
`corpus/foundation-integration` precursor was **not executed for this dispatch**.
That is a sequencing override, not a claim that the precursor was completed,
rejected, blocked, merged, or waived.

The reviewed Wave 1 head is
`e42b9287485a5a6d18ad8a528ab0f0f3f0024ff9`. The bounded correction branch
`ux/corpus-wave-1-review-fixes` starts from that exact commit. Feature-branch
checkpoints may be committed and pushed. Nothing in this roadmap authorizes a
merge or push to `main`, Pages deployment, public cutover, production behavior,
history rewriting, or force-push.

## State and disposition vocabulary

- **Planned**: sequenced but not authorized or started.
- **In progress**: authorized work has begun but has not produced a complete
  review candidate.
- **Candidate**: the committed tracked design and complete evidence package
  await independent disposition.
- **Accepted**, **changes required**, or **rejected**: an independent reviewer
  recorded the lane-specific decision and conditions in tracked authorities.
- **Complete**: every promised requirement and required independent disposition
  passed. A prototype, local check, commit, push, screenshot set, or ZIP cannot
  create this state by itself.

`Blocked` names an actual external dependency. It is not a synonym for pending,
difficult, unstarted, or awaiting ordinary review.

## Reviewed A0-A4 foundation disposition

The independent coordinator review accepted the product model and enough of
the design contract to authorize real-data Wave 1 work. It did not accept the
synthetic prototype as pixel-level production design; every real surface keeps
its own screenshot and external-acceptance gate.

| ID | Deliverable | Owner | State / disposition | Base / branch | Binding follow-up |
| --- | --- | --- | --- | --- | --- |
| A0 | [Repository and public-site inventory](corpus-browser-inventory.md) | Codex | **Accepted** | `c27d691` / `ux/foundation` | Use the route/object/ownership inventory; refresh counts only when release contents materially change. |
| A1 | [Scholarly corpus UX research](corpus-browser-research.md) | Codex | **Accepted** | `c27d691` / `ux/foundation` | Retain borrow/reject/exceed reasoning; research did not authorize a framework or IIIF migration. |
| A2 | Site-wide product and corpus architecture | Codex | **Accepted with coordinator amendments D1-D20** | `c27d691` / `ux/foundation` | “The corpus is the product; pages are typed views into it” governs Wave 1. |
| A3 | Tokens and Reader/Catalogue/Instrument archetypes | Codex | **Accepted as foundation direction only** | `c27d691` / `ux/foundation` | Token roles and archetypes may guide real-data design; exact pixels, heading sizes, masthead density, spacing, and font results are not frozen. |
| A4 | Shared navigation, Jump, Related, and shell interaction | Codex | **Accepted with amendments** | `c27d691` / `ux/foundation` | Jump remains bounded until J0-J2; Related is typed navigation, never recommendations; the protected liturgy adapter remains exclusive. |
| B0/B1 reconnaissance | Claude | **Accepted as implementation input** | `c27d691` / `impl/foundation` | Generator seams, static-host constraints, structural defects, URL compatibility, and existing browser harnesses are binding findings, not permission for a rewrite. |

## Binding coordinator decisions D1-D20

1. **Publications:** `/texts/` keeps its route and uses **Publications** as its
   compact public label. It is a discovery view, not a second owning catalogue.
2. **Protected liturgy:** do not modify canonical Day/Propers ownership,
   `reader-shell.js`, or `reader-instrument.css` while the separate Live Reader
   task owns those seams.
3. **Provider terminology:** use **Independent treatment** for a visible
   provider-qualified work and **Parallel treatment** only as a relationship
   label. Provider remains explicit metadata. A provider output is not a Source
   Library edition unless it satisfies that model.
4. **Archetypes:** Reader, Catalogue, and Instrument share identity, token
   roles, spacing logic, accessibility, URL discipline, and contextual
   navigation—not one universal layout.
5. **Visual roles:** retain warm paper, near-black text, restrained oxblood,
   strong blue focus, serif reading, UI sans fallbacks, square controls, quiet
   rules, restrained chrome, and content dominance. Exact values remain subject
   to real-data evidence; no production design may assume Inter is installed.
6. **Global navigation:** the durable destinations are Publications, Sources,
   Scripture, Liturgy, History, Law, and Commentary. The wordmark links Home;
   a separate Home item survives only if 1024-pixel and 200% evidence stays calm.
7. **Home:** preserve Faith, Scripture, Liturgy, History, Formation, Mary, and
   Law in their current order and identity unless a separately recorded
   repository-guidance amendment proves a better real-data alternative.
8. **One owning catalogue:** facets may aggregate treatments and formats but
   may not create another publication ownership hierarchy or PDF home.
9. **Web editions:** `web-editions.md` controls D0. Do not create or edit a
   second prose copy for presentation; preserve revision, colophon, omissions,
   and canonical PDF relationships.
10. **Durable memory:** decisive facts belong in tracked corpus guidance,
    owning surface guidance, `PROJECT-WORK.md`, and the promise ledger—not only
    chat, ignored handoffs, or `build/agent-continuity/`.
11. **Evidence:** use 1440x900, 1024x768, 768x1024, 393x852, and 320x852 plus
    200% text, exact 320 CSS-pixel reflow, representative 400% zoom/reflow,
    keyboard, forced colors, reduced motion, browser print where applicable,
    no-JavaScript truth, and console/network/HTTP/accessible-name checks. Do not
    create pixel baselines before a real-data surface is independently accepted.
12. **Static constraints:** no webfont or icon-library dependency, framework
    migration, root-relative link that breaks `/triptych/`, rejected asset
    type, server dependency, or unmeasured payload expansion.
13. **Search:** A4 Jump is only an explicit fixture. Production Search remains
    J0-J2; no page may present fixture title matching as global search.
14. **Relationships:** show only repository-owned structured edges. Never infer
    a connection from title, keyword, or intellectual plausibility.
15. **Rights and absence:** progressive disclosure may defer hashes, extended
    provenance, long legal apparatus, and secondary technical metadata. It may
    not hide required licence acknowledgement, withholding reason, typed
    absence/unread/unsupported/invalid state, or the difference between access
    and redistribution rights.
16. **Local progress:** defer it. If later proposed for publications it must be
    storage-optional and explicit URL state must win; Day retains no memory.
17. **Architecture debt:** repair shared/generator problems incrementally with
    path-specific proof. Do not turn B0 or any design lane into a browser-stack
    rewrite.
18. **Concurrent liturgy:** the Live Reader — Ritual Flow & Orientation promise
    remains separate and in progress. Re-read its eventual mainline result
    before entering any formerly protected seam.
19. **Git authority:** coherent feature-branch commits and pushes are allowed;
    main integration, deployment, force-push, and history rewriting are not.
20. **Checkout discipline:** parallel lanes use separate full checkouts and
    branches, never worktrees or a shared index.

## Wave 1 real-data design register

Independent review of `ux/corpus-wave-1` at exact head `e42b928...` produced a
split disposition. The review package was
`20260809T000346Z-corpus-wave-1-design-review.zip`; its manifest was
independently verified. The accepted rows do not make F0 or the shared shell
accepted.

| ID | Surface and bounded output | Independent disposition | Binding follow-up |
| --- | --- | --- | --- |
| C0 | **Home / corpus entry.** Task entrances plus seven editorial portals. | **Accepted.** | Preserve the accepted composition. Do not force every task above the fold at 200% text; preserve semantic order and reflow. |
| C1 | **Publications `/texts/`.** List-first discovery, facets, independent treatments, format availability, and zero state. | **Accepted.** | Preserve the composition and one-owning-catalogue rule. Redundant rule/spacing cleanup is optional implementation polish. |
| D0 | **Publication Reader.** One reading plane, provider and revision identity, Contents, rights, stable loci, and canonical PDF. | **Accepted.** | Preserve typography and interaction. Production must make identity and PDF truth static, retain hash/focus/table semantics, and treat browser print only as fallback. |
| E0 | **Catena Omnia.** Scripture anchor plus chronological and typed commentary chain. | **Accepted.** | Production may proceed independently without editing shared shell owners or protected Liturgy; preserve every held, lead, absence, refusal, and error state. |
| F0 | **Source Library.** Work -> Edition ownership with edition-owned sibling Artifact, Segment, and Passage records and a separate Passage controller relation. | **Changes required.** | Correct the false linear lede/hierarchy and one-passage navigation; production F1 remains blocked until the correction receives independent acceptance. |
| Shared shell | **Non-Liturgy shell.** Current domain, durable browse access, bounded Jump, responsive identity. | **Changes required.** | Use one wide current-location signal and a bounded wide Browse control; retain compact domain, Menu, and Jump. Final cutover remains blocked pending acceptance. |
| Accessibility and resilience | Production requirement. | **Accepted as a requirement; production proof outstanding.** | Production must prove one `main`, 320px no-overflow, focus/dialog behavior, forced colors, reduced motion, hash/history, `/triptych/` links, no-JS truth, and static PDF access. |
| Browser print | Non-canonical fallback. | **Accepted only as a non-canonical fallback.** | Hide interactive chrome and preserve obvious canonical-PDF access; do not reproduce the typeset PDF. |

### Review-fix checkpoint

The correction branch may change only the isolated design layer, focused tests,
and durable authorities needed to:

- make the Source lede and labels express the exact sibling/controller model;
- omit or unequivocally disable Previous and Next when an Edition has one
  Passage;
- remove duplicated wide current-domain identity;
- present one meaningful wide Browse control while retaining compact Menu and
  bounded Jump; and
- optionally remove Source-only redundant filter/result spacing when already
  touching that layout.

It may not redesign C0, C1, D0, or E0, implement production behavior, enter
protected Liturgy, change a PDF, route, hash contract, public build mapping, or
deployment state. Its fresh evidence must cover wide shell states on all five
surfaces, compact Home and Instrument states at 393px and 320px, corrected
Sources wide and narrow, the one-Passage state in normal and forced colors, and
keyboard focus on the wide Browse control.

The new ZIP is evidence transport, not acceptance. At this checkpoint F0 and
the shared shell remained **changes required** until an independent reviewer
accepted the corrected states and that disposition was recorded here and in
the fail-closed authorities.

### Final correction disposition

Independent review of packaged head
`ecbd93a0575c4b890cc814af7cd20d01f5af7beb` and the fresh immutable package
`20260809T021953Z-corpus-wave-1-review-fixes.zip` (SHA-256
`d5fde51b14f143db05f762178896284d7768c0b2a11fc222fc2b32da63e22062`)
recorded both required dispositions:

- **F0 Source Library — ACCEPT.** The corrected design distinguishes
  Work/Edition ownership from the Artifact/Segment relation controlling
  Passage text. Its reviewed one-Passage state retains the selector, exact
  `Passage 1 of 1`, rights, provenance, and inspection-scope truth while
  omitting impossible Previous and Next actions.
- **Shared non-Liturgy shell — ACCEPT.** Wide surfaces show exactly one
  current-location signal, no duplicate wide domain identity, and Browse as a
  bounded destination control distinct from Jump. Compact surfaces preserve
  domain identity, Menu, Jump, target sizing, and no document-level overflow
  at 393 and 320 CSS pixels.

These dispositions preserve C0, C1, D0, and E0 and the protected Liturgy, PDF,
production-route, and hash boundaries. They close only the F0 and shared-shell
design-review gates; the disposable overlay remains design evidence rather
than production application logic.

The following findings are non-blocking only for design acceptance and retain
their distinct downstream classifications:

- the inherited nested-`main` defect remains a production blocker;
- Reader table-cell reflow and full no-JavaScript behavior remain production
  obligations;
- implementation and hardening must add comprehensive Menu/Browse destination
  activation tests;
- the prototype stylesheet used 8,171 of its 8,192-byte gzip-9 ceiling and
  supplies neither meaningful extension headroom nor a production CSS budget;
  and
- the stale Fortescue Artifact note remains with its proper source-data
  authority owner and is not corrected by this disposition.

## Structured-data limits and blocked follow-ups

Safe current relationship categories are explicit containment,
passage-to-artifact/segment, Catena fragment-to-Scripture locus, Catena
passage-to-Source Library passage, act descent/change/history,
document-to-owning-catalogue page, and Mass-to-propers-to-Scripture resolution.
Even these appear only where the actual record exposes the edge.

The following are **blocked on separate repository-owned schema, generator,
and verification work**, not blockers to producing honest Wave 1 designs:

- `translation_of`, `used_by`, `derived_from`, inferred canon
  correspondences, Law-to-Source citations, and generic Related edges;
- a corpus-wide typed relationship projection with direction, derivation,
  revision, and public/no-leak guarantees;
- a true global Search index and recognizers for citations, aliases, IDs, and
  multilingual text (J0-J2);
- side-by-side provider comparison until both browser-readable treatments and
  stable alignment semantics are proven;
- IIIF viewing until a concrete witness, rights disposition, and measured
  accessibility/performance need exist;
- an honest unread passage or commentary-fragment fixture: all 2,751 current
  passages are inspected, so unread remains a future schema/data state and must
  not be fabricated for design evidence;
- disputed-attribution and held-unrenderable Catena presentation until a lawful
  structured record exists; the current generated Catena has no admissible
  instance of either state;
- local reading progress, generated freshness/featured claims, or corpus counts
  without deterministic release-owned inputs.

Designs may show an explicit unsupported/absent state or record a future corpus
opportunity. They must not simulate the missing relationship, search result,
comparison, text, or metadata in the UI.

### E1 Catena corrections and their independent review — 2026-08-11

E1 Catena production implementation was dispatched independently from main
`9b9ff74a77d1bcd7d454d2a7fc448b8a6c8f1fd4`. Its history, which this tree did
not previously record, is: an independent production review
(`254c4446ff693e3015364e005624d62fbdf8e35b`, branch
`ux/catena-wave-1-e1-review`) found **CHANGES REQUIRED** at candidate head
`efd7559a93310442753383bfeec80529f4693288` with eleven findings; a first
bounded correction lane (route/test commit
`67191afd1d6281006e5cb947596452481c0d9692`, packaged head
`dfc636665df26563138ff893bd2a9f9afc7d80c0`, branch
`impl/catena-wave-1-e1-corrections`, immutable package
`20260811T134130Z-catena-e1-corrections` and its ZIP, SHA-256
`8013074d9a77ae54208399207e10d58aaacb7e1b6efab6e820bbeaaa9fd83b05`) met the
original budgets and corrected the chronological chain, ordinary
no-JavaScript truth, narrow and 200-percent reflow, route-local
Back/Forward, and the forced-colors paragraph-border rule; and a fresh
independent correction review
(`8f8f424ec5ccd5300dcee997a529f79fc23a8959`, branch
`ux/catena-wave-1-e1-correction-review`) again found **CHANGES REQUIRED** at
`dfc636665`, because the route-owned halves of findings 3, 4, 5, 6, 8 and 11
remained open, the accepted forced-colors correction carried a route focus
rule that overrode the accepted shared role, five route-local robustness
findings stood, and the first package was protocol-incomplete.

This second bounded correction lane answers that review from current main.

- Base and merge base: `9b9ff74a77d1bcd7d454d2a7fc448b8a6c8f1fd4`, unmoved
  through the lane. Branch `impl/catena-wave-1-e1-corrections-v2`. The first
  lane's route/test commit `67191afd1` was carried forward by cherry-pick and
  the remaining route-owned defects were corrected in `981959b4f78209401ba00bfbdcc430e23e09c8bb`.
  The candidate head is the durable-record commit carrying this subsection;
  its exact SHA is recorded in the handoff package and this lane's report,
  which is how package and head identity stay non-circular.
- Exclusive file boundary, unchanged: `src/web/browser/catena/catena.js`,
  `catena.css`, `index.html`, and `tools/tests/test_catena_wave_1.py`, plus
  these four durable authority records. `catena-model.js` is byte-identical
  to main (SHA-256 `f1ea94f9…ccf57b`, pinned by the focused suite), and the
  base-to-head range changes no other tracked path.
- Route defects corrected: the URL grammar validates the raw multimap, so a
  recognized key cited twice is refused even when the citations agree, an
  undecodable percent-value fails, `voice` is a closed whole-key grammar
  (corrected in V3 below, which distinguishes a supported voice from a
  merely well-formed one), and a chapter is
  ranged against the book the address resolves to rather than a leftover
  control; one seeding runs for every arrival, so an identical invalid address
  renders one page whether it was pasted, reloaded, or reached by hashchange,
  Back or Forward, with no stale controls, options or step buttons beneath it;
  a rebuild that swallows the focused element hands focus to the reading
  region, including on the failure arm, and each state speaks once;
  asynchronous completions prove route ownership before they may repaint,
  error, recount, announce or write history, rejected loads are evicted so the
  retry the copy promises is real, a failed bootstrap says so instead of
  leaving a permanent Loading label, and the route's own pushing write is
  remembered by identity so its echo cannot revert a reader who has moved on;
  tally, empty, blocked, integrity and voice-option claims derive from one
  typed state, so held-but-unrenderable material is never summarized as
  nothing held and no absence label is manufactured during an integrity
  failure, an invalid route, a failed load, or beside a blocked row whose
  voice the record does not state; acquisition rows are unreconciled lead
  entries whose omitted confidence is disclosed and which assert no distinct
  work, possession or renderability; every supplied valid rights fact renders
  through one point-of-use acknowledgement channel without browser-side
  precedence, and a malformed value is withheld rather than coerced into a
  fact or a guessed legal status; print carries the selected Scripture edition
  and voice, drops navigation, loopback annotations and interaction-only
  prose, and keeps headings with their content; the route's focus-outline
  overrides are gone in normal and forced-colors modes; the Scripture locus is
  a heading; and per-work translation-absence reasons are no longer deferred
  behind a closed disclosure.
- Validation at the candidate head: focused suite 179 tests OK, grown from 99
  and covering the adversarial URL, load-race, blocked/empty, print-identity
  and real-payload cases the review named, an exactly-once identity assertion
  over every rendered commentary fragment, and a regression test for each
  finding of this lane's own internal adversarial audit; `test_catena` 52,
  `test_browser_url_contract` 47, `test_browser_static` 5,
  `test_browser_collisions` 11, `test_corpus_browser_gate` 18 with its one
  intentional live-browser skip, and `make check-browser-harnesses` 6, all
  matching the pristine-main baseline; `scripts/_catena.py check` exit 0 with
  1,351 fragments, one held book and a 73-book canon; whole-file gzip-9
  budgets 7,629 of 8,000 bytes for CSS and 12,996 of 13,000 for JavaScript,
  the original ceilings, unraised; `make -k check` exit 2 with three failing
  targets against the baseline's two — `check-tool-registry` and
  `check-examples` are inherited, and both new reds are the one unsigned
  binding condition seen twice, since `check-release-bindings` finds exactly
  the three changed Catena route assets stale and `check-examples`' single new
  divergence is `tools/public-alpha verify --preview` failing on those same
  three hashes; browser artifact gate exit 1 with 2,290 assertions, 1,836
  passed, 226 failed and 228 skipped, its failure classes 117 nested-`main`,
  82 target-size and 27 skip-link, exactly the pristine-main baseline.
- Baseline comparison, in precise terms: the base and head
  `(route, state, name, status)` identity/status tuple sets are identical and
  no assertion changed status in either direction. The complete assertion
  objects are **not** byte-identical: of the 121 Catena rows on each side, 106
  objects match byte for byte and 15 differ in their `detail` text alone,
  reporting the renamed controls and lower target-size offender counts; of all
  2,290 assertions exactly those 15 objects differ, and no non-Catena row
  changed.
- Outside-owner prerequisites remain untouched and open: the Psalm
  Vulgate-to-edition projection, acquisition-lead reconciliation with its
  stripped confidence, and the real licence/attribution projection belong to
  the generator and data owner; the deterministic Catena-data release root and
  the three route re-signatures belong to the release owner, and
  `check-release-bindings` is meant to stay fail-closed until that owner acts;
  the `voice` deep-link sample disposition belongs to the common-gate owner;
  and the wrapper width, nested `main`, skip target, global focus and arrow
  behavior, target size, and the shared-history `lastWritten` Forward
  suppression belong to the B0/shared-shell owner. This lane also records two
  findings of its own audit for other owners: the shared chapter loader caches
  a transport rejection for the session, and every browser page nests
  `main#reading` inside `main#main-content`.
- Environment limits stated rather than papered over: no real
  assistive-technology session was possible in this lane's headless
  environment, so the accessibility-tree and keyboard-sequence artifacts are
  labelled supplements and the requirement is recorded as unmet; forced-colors
  evidence is browser emulation, labelled as such, not a system palette.
- Immutable handoff: `20260811T212656Z-catena-e1-corrections-v2` and its sibling ZIP under
  `build/agent-handoffs/`, whose ZIP SHA-256 is recorded in the package's
  transport digest and this lane's report. The first package remains unchanged
  as historical evidence.
- Status: **awaiting fresh independent review** of the exact candidate head and
  its package. This lane accepts nothing, integrates nothing, merges nothing,
  re-signs nothing, and deploys nothing.

### E1 Catena correction V3 — 2026-08-12

The independent review of correction V2 (`4c30d86f7118d69eb27d12dc9b63568e531918eb`, branch
`review/catena-wave-1-e1-corrections-v2-independent`) dispositioned the
reviewed head `17f031b37840d8320c664a128d72b502108fe075` **CHANGES REQUIRED**. It
passed the V2 URL, history, race, focus, print, lead and rights corrections,
the package mechanics and the unraised budgets, and named exactly four things
for this lane: two route defects and two inaccurate statements. Every other
finding stays with the owner the review assigned it to, and none is answered
here.

- Implementation defect 1 — **unsupported voice** (findings 5 and 8). A
  well-formed `voice=translation:zz` satisfied the two-or-three-lowercase
  grammar and was then carried into the page as `none in ZZ translation`,
  converting an unsupported voice into a claim about corpus holdings. Shape
  and support are now separate questions: the closed supported-language set
  is read from `index.held[].languages`, Catena-owned runtime truth the route
  already holds before any voice is resolved, and a well-formed voice naming a
  language the corpus holds nothing in fails closed through the existing
  invalid-address state, exactly as an unpublished `bible` does. Three states
  now exist where two did — malformed shape, supported voice, and supported
  shape without a supported language. A voice the CHAPTER merely lacks is
  untouched and still says so.
- Implementation defect 2 — **untyped displayed provenance** (finding 4). Every
  provenance value this route displays now passes one typed gate before it can
  become words. The review named `edition`, `edition_published` and a
  `translators` item; the audit for this correction found the same door open on
  `locator`, `review`, `author`, `work`, `date`, `language`, the author heading,
  the author-filter label and the refusal note, and one worse case: a
  `translators` value carrying a `length` and no `join` threw out of an
  asynchronous render, so the chapter kept `aria-busy` for ever. Each translator
  entry is judged alone, so a broken one is dropped while its valid siblings
  stand, and no scalar fact is lost because a neighbour is malformed.
- Evidence correction 1 — **stranger keys**. The V2 handoff claimed without
  qualification that a stranger's key is "neither honoured nor disturbed". The
  precise behaviour is: unrecognized hash keys are judged by nothing — the
  validator reads only `book`, `chapter`, `bible` and `voice` — and they
  survive exactly as long as the route writes nothing, which is an address that
  already parses to the rendered state, and an invalid or duplicate-key address
  left as written. Every write the route makes replaces the whole fragment with
  those four keys alone, so an unrecognized key is discarded when a partial or
  otherwise non-identical arrival is completed in place, when a reader action
  pushes an entry, and in the recovery link the invalid page offers.
  Preservation is a consequence of not writing, not a preservation rule. Only
  the value-identical case is proven by test; the discard cases are read from
  the code and are labelled as such. No URL contract changed to suit the prose.
- Evidence correction 2 — **AT-SPI**. The V2 `AT-LIMITATION.md` said no AT-SPI
  bus launcher exists. That is false: `at-spi2-core` provides
  `/usr/lib/at-spi-bus-launcher`, installed before the V2 capture. The accurate
  limitation is that the review environment provided no usable display, AT bus
  session or AT client stack — no screen-reader, speech or braille session was
  available — and therefore no successful real-assistive-technology evidence
  was produced. The existing emulated and structural artifacts remain labelled
  supplements, and no real-AT validation is claimed. The V2 package is left
  byte-identical; the correction is carried in the V3 package, not by editing
  a sealed one.
- Exclusive file boundary: `src/web/browser/catena/catena.js` and
  `tools/tests/test_catena_wave_1.py`, plus these durable records. `catena.css`
  and `index.html` are byte-identical to the reviewed head, `catena-model.js`
  is byte-identical to main, and no generator, generated data, release record,
  common gate, B0/shared shell, protected Liturgy or PDF path is touched.
- Budgets unraised and paid for by deletion, not waiver: `catena.css` is
  unchanged at 7,629/8,000 and 2,676/2,700; `catena.js` is 12,995/13,000 whole
  and 8,799/8,800 with comments stripped. The corrections were funded by
  removing a provably dead voice lookup repeated four times, folding six
  per-field guards into one typed gate, and tightening three expressions. The
  code-only ceiling now stands one byte clear, and the prose the house style
  would ordinarily carry could not be afforded — one precondition is pinned by
  test instead of by comment, and that is recorded as a limitation.
- Focused suite: 249 tests green, up from 179. The one V2 test that pinned the
  defect — a `translation:de` deep link rendering "German translation — none
  here" — is retargeted to `translation:grc`, a language the corpus really
  holds, and the unsupported case is now pinned as a refusal.
- Immutable handoff: `20260812T184146Z-catena-e1-corrections-v3` under
  `build/agent-handoffs/`, for the exact V3 head. The V2 package and its ZIP
  are unchanged.
- Status: **awaiting fresh independent review** of the exact V3 head and its
  package. This lane accepts nothing, integrates nothing, merges nothing,
  re-signs nothing, and deploys nothing. Every outside-owner prerequisite the
  review left open remains open.

## Remaining program sequence

| Work | Current state | Exact dependency / stopping line |
| --- | --- | --- |
| B0/B1 shared non-liturgy implementation and harness | Authorized separately; not owned by this design branch | May use accepted A3/A4 direction and implementation findings; must stop before inventing C0/C1/D0/E0/F0 compositions and must not enter protected liturgy files. |
| C2/D1 production surface implementation | Eligible after the shell ownership boundary is clean | C0/C1/D0 are accepted; avoid branches that contend for global generator, site CSS, release binding, or shell files. |
| E1 Catena production implementation | Third correction candidate awaiting fresh independent review | Review `4c30d86f7` (CHANGES REQUIRED at `17f031b37`) is answered by `impl/catena-wave-1-e1-corrections-v3`, which corrects unsupported-voice handling, untyped displayed provenance, and the two inaccurate handoff statements and nothing else; preserve accepted E0 and every V2 correction the review passed; every generator/data, release, common-gate, B0/shared-shell, pre-release real-device-or-AT evidence, emulation-only forced-colors limitation, protected Liturgy, and PDF prerequisite stays with its owner; no merge, re-sign, deploy, or cutover. |
| F1 Sources production implementation | Eligible only for separate owner-authorized dispatch | The F0 design-review dependency is satisfied; no production implementation is started or authorized by this disposition. |
| Final shared-shell cutover | **Blocked** | The shell design-review dependency is satisfied; cutover still requires a clean implementation-foundation checkpoint and explicit cutover authority. |
| G0/H0/I0/J0 and implementation partners | Planned Wave 2 | Do not begin merely because Wave 1 prototypes exist; follow owning guidance and exact accepted dependencies. |
| K0/K1 typed relationships | Planned | Requires accepted owning surfaces and verified structured edges; schema gaps above remain explicit. |
| L0/L1 visual and accessibility acceptance | Planned | Requires implemented representative surfaces and complete real-data matrices. Automated checks cannot supply independent visual judgment. |
| M0/M1 integration, cutover, and final acceptance | Planned | Requires accepted lanes and explicit maintainer publication authority. This branch may not merge or deploy main. |

## Progress ledger

| Date | Work | Evidence-backed result | Commit or handoff |
| --- | --- | --- | --- |
| 2026-08-08 | A0-A4 foundation | Inventory, research, corpus architecture, three archetypes, isolated synthetic prototype, Menu, bounded Jump, typed Related, responsive behavior, and browser gates were produced from `c27d691`; the coordinator accepted A0/A1, accepted A2/A4 with D1-D20 amendments, and accepted A3 as direction only. | Source roadmap/prototype commit `ac37b6f`; reviewed Codex head `3b5938a`; Claude findings head `af2c961`. |
| 2026-08-08 | Direct Wave 1 dispatch | Created `ux/corpus-wave-1` directly from current `origin/main` `c27d691`; did not execute or merge the proposed foundation-integration precursor; authorized C0, C1, D0, E0, and F0 real-data visual/product work. | Base `c27d6915319785686d1df6a1401a489aa9921f6f`; branch `ux/corpus-wave-1`; external acceptance open. |
| 2026-08-09 | Wave 1 Candidate checkpoint | Completed the isolated real-route prototype and 83-case matrix over all five surfaces. The exact browser report records 1,979 assertions, 1,917 passes, 62 disclosed inherited findings, and zero gating failures; 83 main captures and every page of the 236-page print were inspected. Protected Liturgy, PDFs, prose, production browser sources, release bindings, and deployment remain unchanged. | `build/agent-handoffs/20260809T000346Z-corpus-wave-1-design-review/`; exact branch head and ZIP digest are recorded in the handoff; external acceptance remains open. |
| 2026-08-08 | Independent Wave 1 review | Accepted C0 Home, C1 Publications, D0 Reader, and E0 Catena; required changes to F0 and the shared non-Liturgy shell; accepted accessibility/resilience as a production requirement and browser print only as a non-canonical fallback. | Reviewed head `e42b9287485a5a6d18ad8a528ab0f0f3f0024ff9`; verified package `20260809T000346Z-corpus-wave-1-design-review.zip`. |
| 2026-08-08 | Review-fix dispatch | Authorized `ux/corpus-wave-1-review-fixes` from exact reviewed head for bounded F0, shell, evidence, and authority corrections only. | F0 and shell remain changes required pending a fresh independent disposition; no production/main/deploy authority. |
| 2026-08-09 | Review-fix implementation and test checkpoint | Completed the bounded F0 and shared-shell prototype corrections without reopening C0, C1, D0, or E0. The full capture run covered 85 real-route cases and 2,296 assertions with zero gating failures. Its 64 disclosed non-gating findings comprise 52 inherited nested-`main` findings, eight before-state useful-content findings, two before-only narrow-overflow findings, and two inherited Reader no-JavaScript overlay limitations. Protected Liturgy production and canonical PDF paths have zero reviewed-base-to-head changes. | Authority reconciliation `3bfb9df10e1bd4b8d4d2b56aeb430c897f67700a`; design/test head `c66c143643ff75a6cd54afdbe1fcd6eac0aca1b6`. F0 and shell remain changes required until independent acceptance. The earlier correction package `20260809T014145Z-corpus-wave-1-review-fixes` is superseded for protocol defects; a fresh immutable package follows this tracking repair. |
| 2026-08-09 | Final F0 and shared-shell design review | Independent review recorded **F0 Source Library — ACCEPT** and **Shared non-Liturgy shell — ACCEPT**, preserving C0/C1/D0/E0 and protected Liturgy/PDF/routes/hashes while carrying the disclosed production and data obligations forward. | Reviewed and packaged head `ecbd93a0575c4b890cc814af7cd20d01f5af7beb`; package `20260809T021953Z-corpus-wave-1-review-fixes.zip`; SHA-256 `d5fde51b14f143db05f762178896284d7768c0b2a11fc222fc2b32da63e22062`. |
| 2026-08-11 | E1 Catena correction pass 2 | Answered correction review `8f8f424ec` (**CHANGES REQUIRED** at `dfc636665`) from unmoved main `9b9ff74a7`: carried route/test commit `67191afd1` forward and corrected the remaining route-owned URL-grammar, history-independence, recovery-focus, asynchronous-transaction, blocked/empty, lead, licence, print, focus-override, heading, and absence-disclosure defects inside the four-path boundary. Focused suite 179 tests; budgets 7,629/8,000 and 12,996/13,000 unraised; gate 2,290 assertions with the pristine-main failure identity/status set unchanged, 15 Catena `detail` texts differing and no row changing status; `check-release-bindings` deliberately fail-closed on the three changed route assets. | Branch `impl/catena-wave-1-e1-corrections-v2`; route/test commit `981959b4f78209401ba00bfbdcc430e23e09c8bb`; packaged head and package `20260811T212656Z-catena-e1-corrections-v2` recorded in the handoff; awaiting fresh independent review. |
| 2026-08-12 | E1 Catena correction V3 | Answered independent review `4c30d86f7` (**CHANGES REQUIRED** at `17f031b37`) with the smallest bounded correction: a well-formed but unsupported voice now fails closed against the corpus's own held-language set instead of rendering `none in ZZ translation`, and every displayed provenance value passes one typed gate, which also removes a `translators` shape that threw out of an asynchronous render and left the region `aria-busy`. The unqualified stranger-key claim and the false AT-SPI-launcher claim are corrected in these records and in a new package. Focused suite 249 tests green; budgets unraised at 7,629/8,000 and 12,995/13,000, paid for by deletion; `catena.css`, `index.html` and `catena-model.js` byte-identical; `check-release-bindings` still deliberately fail-closed on the Catena route assets, unrepaired. | Branch `impl/catena-wave-1-e1-corrections-v3`; base `17f031b37840d8320c664a128d72b502108fe075`; package `20260812T184146Z-catena-e1-corrections-v3`; awaiting fresh independent review. No merge, re-signing, deployment, or outside-owner work occurred. |

## Next Codex tasks

No further Codex design or implementation task is authorized by this
acceptance. After this acceptance/continuity-only update is committed and
pushed and its resulting HEAD SHA is reported, stop. Production implementation
remains owned by the appropriate Claude lanes under separate authority. This
acceptance does not authorize merging the disposable prototype, merging or
pushing `main`, deployment, public cutover, protected Liturgy edits, or
canonical PDF changes.

Append later findings and dispositions. Do not rewrite earlier rows to make the
sequence appear cleaner.
