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
- Focused suite: 249 tests green, up from 231. The one V2 test that pinned the
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

### E1 Catena correction V4 — 2026-08-13

Answering the independent review at `9b1c23680c8da6b9a83bb7fb8ca689fbf9d2004c`
(**CHANGES REQUIRED**) from the exact reviewed head `f2c9bc49d`.

| Finding answered | Disposition |
| --- | --- |
| Unsupported voice — the classifier | **Corrected.** The generator counts the voice keys the corpus holds and writes them as a top-level `voices` array; the route compares the whole key. The corpus holds four source pairs — `original:grc`, `original:la`, `translation:en`, `translation:la` — projecting onto three route keys, and no Greek translation. `translation:grc`, `translation:de` and `translation:zz` all fail closed; Genesis 10 in `translation:en` keeps its true "none here". |
| Typed presentation — the nine sinks | **Corrected as one boundary**, in `catena-model.js`: text, list, record, a number as the data carries it, and a fact that may be a finite number. Absence author/work/reason/partial are typed at the read so the summary count and the listed words are one value; a scalar is no longer a translator list; a malformed language reaches no label, control value, URL or `lang`; malformed extent members state no locus; unnamed authors get no shared filter key; and the render tail sits inside the existing funnel, so a throw can no longer strand `aria-busy`, focus, the tally, the announcement or the route. |
| Package privacy | **Replaced.** A new sanitized immutable package, sealed by a rewritten sealer that reads identities from the environment, matches the account name on word boundaries, scans every file and path, and refuses to write a manifest on any hit. It refuses to seal the V3 package. The V3 package is not mutated. |
| AT-SPI overstatement | **Corrected.** Negatives are scoped to the inspected session, no command transcript is reproduced, and the claim is one status-region write rather than one spoken announcement. |
| Full-suite exactness | **Stated exactly.** No new failure identity; one pre-existing failure's detail is attributable to V4; one is environment-sensitive; the deliverable-count assertion did not move and is reported as unmoved. |
| Stranger keys | **Prose corrected**, no implementation change: `replaceState` is conditional, the canonical vocabulary is four keys but omits an empty voice, and the `?data=` evidence is real but bounded. |
| Focused-suite baseline | **Corrected** in these records: 249 is up from 231, not 179. |

Independent validation at the V4 head: focused suite **266 green**; full
discovery **1,617** tests, 14 failures, 13 errors, 11 skips against the base's
1,600/15/13/11, with **no new failure identity**; browser gate **2,290**
assertions, 1,836 pass / 226 fail / 228 skip, its assertion set, statuses and
details equal to the base object for object, run metadata excluded; promised
deliverables valid, 29 tracked; `make -k check` exit 2 with the same three
failing targets as the base. Budgets: `catena.css` unchanged at 7,629/8,000 and
2,676/2,700; `catena.js` **12,981/13,000** whole and **8,749/8,800** stripped —
both improved, no ceiling raised, paid for by the classifier simplification and
by moving pure helpers into the unbudgeted model.

Preserved owners: generator/data beyond the authorised voice-key seam, release
(now four stale Catena bindings, none re-signed), the common gate, B0/shared
shell, real-device-or-AT evidence, protected Liturgy and PDFs. E1 stays off
main and is **awaiting fresh independent review**.

### E1 Catena correction V4.1 — 2026-08-13

A micro-correction from the exact V4 head `e40720d5d`, answering only the two
review requirements V4 disclosed as unmet.

| Requirement | Disposition |
| --- | --- |
| Fail-closed presentation — neutral umbrella copy | **Corrected.** Three shared strings in `renderInvalid`: `Address not recognised` to `Address not used`; `This address names what the page does not have` to `This address cannot be used as written`; `The address could not be read; its invalid values are shown, unchanged.` to `The address is unchanged; the values not used are listed.` The component, the recovery affordance, the layout and the typed per-value reason are unchanged, so malformed and unsupported refusals stay distinguishable. One narrow regression pins the umbrella against re-diagnosing; it fails on the previous copy. |
| Package exactness — required captures | **Produced.** V4's reason, that no display was available, was incorrect: headless Chromium needs no display server. 53 captures from real built artifacts at the parent and this head, nine route states at three viewports plus forced-colors and print emulation, with before/after pairs for the two states whose copy changed. They evidence rendering only; the real-AT limitation is unchanged and unsuperseded. |
| Conditional-source omission rationale | **Recorded.** This lane consulted no external source, corpus, edition or binding, so the `sources/` class is omitted with that reason stated in the handoff inventory. |

Independent validation at the V4.1 head: focused suite **267 green** (266
inherited plus the new regression); full discovery **1,618** tests against the
base's 1,617, the 27-entry failure/error name set identical under `diff`;
browser gate **2,290** assertions whose whole report is deep-equal to the base
across 480,881 bytes including all 226 failure objects, `generatedAt` excepted;
promised deliverables valid, 29 tracked; `make -k check` exit 2 with the same
three failing targets. Budgets: `catena.css` byte-identical at 7,629/8,000 and
2,676/2,700; `catena.js` **12,970/13,000** whole and **8,734/8,800** stripped,
both smaller than V4 because the replacement copy is shorter. No ceiling raised.

The `src/web/data/` contradiction is preserved untouched for independent
adjudication; nothing under `src/web/data/` changed and the guard was not
weakened, deleted, whitelisted or expect-marked.

Preserved owners: generator/data, release (four stale Catena bindings unchanged
in count, none re-signed), the common gate, B0/shared shell, real-device-or-AT
evidence, protected Liturgy and PDFs. E1 stays off main and is **awaiting fresh
independent review**.

### E1 Catena correction V5 — 2026-08-14

Answers the fresh independent review `7f69575b982926e827974f2ed236b1c8bfd8aaad`
(**CHANGES REQUIRED** at exact candidate
`f93757854b54c19e50bdcb97ca0fed9b48d22bb7`). This lane records no acceptance
of its own work.

The review's five blocking classes are one class: malformed or unsupported
structured metadata becoming visible semantics, counts, refusals, routing
facts, bootstrap state or DOM attributes through coercion or an unchecked
collection shape. V5 answers them behind **one record boundary**, placed in
`catena-model.js` because `catena.js` had thirty gzipped bytes of margin and a
boundary bought out of thirty bytes would have been a list of one-off guards.

| Blocking class | Correction | Evidence at the head |
| --- | --- | --- |
| 1. Raw language metadata | `tongue()` gates every value reaching a DOM `lang`, a visible language label or prose — a *shape* check, not a non-emptiness check, because `lang` is machine-read. `voiceLanguage()`, narrower still, gates the voice key, because a key becomes a URL the page must accept back from itself. | Real Chromium at the base rendered `fragment-text=[object Object]`, `=42`, `=true`, `=   ` and `=not a language code`, and printed `NOT A LANGUAGE CODE — the author's own` as a language chip. At the head every attribute is a subtag and the false chip is gone. |
| 2. Malformed collection members | `records()` validates each member of every collection that feeds presentation or state: fragments, leads, blocked, refusals, absence lists, the canon and the held index. | Real Chromium at the base **replaced the whole page with `Cannot read properties of null (reading 'source')`** — every valid sibling lost, tally empty, nothing held. At the head: three fragments, both valid leads, both valid blocked rows, and no refusal manufactured from three malformed members. |
| 3. Absence findings | Rows are classified from the generator's typed `finding`, closed at four values in `scripts/_catena.py`. `not-surveyed` and unrecognised findings enter no publishing negative and no closed-claim count; a valid finding survives a malformed sibling and a malformed member of its own list. No fifth finding is invented. | Base: `4 works standing here have no English this project may publish`. Head: `2 works … ; 1 has only a partly public domain English, not yet taken; 1 has not been surveyed for English; 1 has a finding this page cannot read`. |
| 4. Numeric, verse, path, bootstrap | `whole()` is a positive safe integer, refusing `true`, `"5"`, `[5]`, `0`, negatives and fractions; extents gain an ordering check; verse keys and values and paragraph marks are typed in `chapterLines()`; addresses are composed in `chapterPath()` and `paragraphPath()` from sound text alone, and `chapterPath()` answers `null` — a broken record — where it cannot prove either a path or an emptiness. Malformed bootstrap enters the terminal funnel. | Base word chips `["1,200 words", "1,200 words", "1 words", "12.5 words"]`; head `["1,200 words"]`. Base **requested `browse/[object%20Object]001.json`**; the head makes no such request. Base bootstrap left `Loading…` standing with no `aria-busy` and nothing spoken; the head settles to `Unavailable`, `aria-busy="false"`, and says `The catena index could not be read.` |
| 5. Route completion | Seven scenarios that **begin canonical**, because every committed malformed scenario began malformed and so proved nothing about a page that had already established a route, a history and a rendered chapter. | Exact `replace`/push, final hash, status journal, tally, `aria-busy` and focus pinned for a partial arrival, for a malformed later member reached by both an action and an address, for a malformed action payload, and for a valid action after a malformed one. |

Three findings were not in the review and were found by writing its required
regressions. The replay harness stored `element.lang` as a plain JavaScript
property where the HTML DOM reflects it into the content attribute — which is
why real Chromium showed the defect while every committed test passed; the
shim now reflects it as it already reflected `id`, and `inspect()` projects
every language attribute for every scenario. `sound()` passed the string
`"not a language code"`, which the shared namer printed back as a language.
And beneath the throw the review named, `render()` had a guard that returned
*silently* when the controls could not name a book — the state a malformed
canon produces — leaving `Loading…` standing; both dead ends now reach
`startFailed`.

Nothing was weakened to pass. The one source-text assertion that changed,
`(index.voices || []).includes` to `list(index.voices).includes`, is the
stricter form of the same requirement: `|| []` let a string `voices` answer
`.includes` by substring. The adversarial absence fixture the review named is
rebuilt rather than re-asserted — not one of its rows carried a `finding` at
all, which is why it could manufacture four closed negatives from four
malformed neighbours.

Fresh results: focused Catena suite **306 tests green** (267 before; the 39 new
ones are the regressions above). Browser gate **2,290 assertions, 1,836 pass /
226 fail / 228 skip**, the whole report deep-equal to the base with the
volatile fields excluded — the comparison ignores `generatedAt`, `root`,
`durationMs` and `browser`, which is wider than the V4.1 record's wording.
Promise ledger valid at **30 tracked / 19 complete**. `catena check` valid at
1,351 fragments. Budgets: `catena.css` byte-identical at 7,629/8,000 and
2,676/2,700; `catena.js` **12,990/13,000** whole and **8,363/8,800** stripped —
the stripped figure 371 bytes *smaller* than V4.1's 8,734 because the
derivations moved to the unbudgeted model, the whole figure 20 bytes larger
because the boundary is explained where it lives. **No ceiling raised.** Four
stale Catena release bindings, unchanged in count, none re-signed; the
`catena-model.js` binding is now stale against a new digest and correctly
fails closed.

Full discovery ran **1,657 tests against the base's 1,618** — the difference is
exactly the 39 new ones — with **14 failures, 13 errors and 11 skips at both
ends** and a **27-entry FAIL/ERROR name set that `diff` reports identical**. No
literal baseline identity is claimed, because the head runs more tests; the
name set is what is compared, which is the standard `AGENTS.md` sets. The base
figures reproduce the V4.1 review's own recorded 1,618 / 14 / 13 / 11 exactly,
which is the check that this comparison environment is the review's.
`make -k check` exited **2** at the same three inherited targets the review
recorded — `check-release-bindings`, `check-tool-registry` and
`check-examples`. No record here rounds those into a green repository-wide
check.

The new regressions were also replayed against the **parent** implementation,
because a regression that passes on the code it was written to catch is not
one. With every V5 scenario present the parent's harness **dies** with an
uncaught `TypeError: Cannot read properties of null (reading 'token')` from
`catena.js:1006` — the bootstrap line — taking all 254 tests with it. With the
two bootstrap scenarios filtered out so the rest can report, **23 of the new
tests fail at the parent**, across all five blocking classes.

`catena.css`, `index.html` and every path under `src/web/data/` are
byte-identical. The production diff is `catena.js` and `catena-model.js`
alone. The `src/web/data/` contradiction is **preserved untouched** and remains
a separate owner's adjudication.

### E1 Catena correction V6 — 2026-08-14

Answers the fresh independent review `fa5b2f601565508acee2b1b236b0c69138af07a3`
(**CHANGES REQUIRED** at exact candidate
`19982ab433dd25704ed60b1ac6ddb678bc3a98f9`, evidence
`fe71d03e51bc3a89f01b9262cd3a4d9077bb0cef`, package digest
`18500400ce617365ef8322e41f011f44dc5a0a88dc39fbbcb5deb1abd78b75ea`,
re-verified byte-exact here). That review is a sibling of this line at the
reviewed parent and is not merged into it. This lane records no acceptance of
its own work.

The review's fourteen blocker classes are one distinction said fourteen ways:
V5 validated a **shape** where the contract needed a **membership**. A value
was confirmed to be an object and never asked whether it was a member of the
collection it stood in; a value was confirmed to be text and never asked
whether it was an identity this corpus had issued.

| Blocking class | Correction | Evidence at the head |
| --- | --- | --- |
| 1. Malformed members reach presentation, counts and refusals | Each collection states in `catena-model.js` what one of its members IS — the least a record must say for there to be anything to render or count. `leadRow`, `blockedRow` and `refusalNote` reject the rest before any derivation. | `mixed-collection` tallies `3 fragments held · 2 works held, not renderable yet · 2 lead entries`, where V5 pinned `3 · 3 · 3` with two blank rows standing. `empty-refusal-records` renders no refusal at all: `{}` may not claim that Scripture's verse division moves. |
| 2. Root language and identity joins | `bibleRecord` normalizes the edition manifest before `fillBibleSelect` ever sees it; `ident`, `bookToken` and `trail` state the grammars the corpus writes; `sources[key]` is read only for a string key the record owns. | The edition control reads `Douay-Rheims`, not `Douay-Rheims ([object Object])`. All 1,351 fragment ids, 73 canon paths and 7 edition ids pass the grammars unchanged, and `unsafe-identities-opened` opens six refused ids and requests none of them. |
| 3. Guessed facts where truth is unavailable | The unsupported claim is OMITTED. No `lang` is written from an unreadable language; `testamentName` is `''` where the canon states no testament. | Eight fragments intending Latin now carry no `lang` at all, where V5 wrote `lang="en"` on each and a test pinned it as survival. `malformed-testament` states nothing where V5 printed `New Testament` over Genesis. |
| 4. Order-dependent findings, and stray `partial` | Findings are read as a set: one recognized finding is the record speaking; two different ones are a record contradicting itself and the page declines rather than choosing the harsher claim. `partial` is licensed only by `partial-public-domain`. | `finding-order` and `finding-order-reversed` are byte-identical across every projection. `stray-partial` renders exactly one partial line where four stray offers sit beside findings that license none. |
| 5. Padded verse keys | Only the canonical encoding numbers a verse. | `padded-verses` renders `["1", "2"]` where `"1"`, `"01"`, `"001"`, `"0002"` and `"03"` arrive; V5 rendered verse 1 twice, each row claiming to be the verse the edition numbers 1. |
| 6. Null bootstrap, and terminal state | `bag()` at the root makes an unreadable index an empty one; the canon is checked before the address is judged; `startFailed` is a transaction that invalidates pending work, clears the tally and completes focus. | At the parent, JSON `null` throws `TypeError: Cannot read properties of null (reading 'canon')` out of `catena.js:981` and kills the whole replay process — preserved unfiltered in the package. At the head all eight unusable bootstraps render one identical terminal page. |

**The proofs were the sharper finding.** Three V5 oracles could not fail on the
defect they defended: the word-tally oracle counted a deduplicated set of class
names, the verse oracle swept the commentary while its fixture corrupted the
bible chapter, and the "nothing stale" case released its payload before
navigating. Eight oracles that expected the defects are corrected in place with
their reasons recorded rather than deleted, and the harness now projects the
rendered verses, the uncounted tally chips, the edition options and their route
values, the testament line, the absence rows' own author and work, the visible
failure paragraph, and a count of parked requests actually released.

Replaying the V6 test file against the parent with **no filter** kills the
harness and errors every `ReplayTest` class in `setUpClass`; that log ships
unfiltered, and the three-scenario filter needed for a per-class reading ships
as an exact patch beside it. Filtered, the parent runs `371` and fails `71`
with `14` errors — 85 FAIL/ERROR identities over 24 distinct classes,
decomposing as `19 + 4 + 1`: 19 of the 23 classes V6 adds, 4 of the 5
pre-existing classes whose oracles it corrected, and the model-digest pin.
The two sets do not coincide. Four V6 classes and one corrected-oracle
class do not fail there, and are named as what they are: the real-corpus
positive control, and oracles reading the production sinks for behaviour
V5 had already made correct.

Focused suite `423` at the head, exit 0, against `306` at the parent. Full
discovery `1,774` at the head against `1,657` at the parent — `14` failures,
`13` errors and `11` skips at BOTH ends, with an identical 27-entry
FAIL/ERROR identity set. The two name files are byte-identical, and that is a
derived fact rather than evidence: both source logs ship, they differ, and the
extraction script ships with them. Fresh browser gates at both ends report
`2,290` assertions — `1,836` pass, `226` fail, `228` skip — and the two
reports are deep-equal **excluding four volatile fields**: `generatedAt`,
`root`, `durationMs` and `browser`. `catena.css` and `index.html` are
byte-identical and every path under `src/web/data/` is untouched.

Budgets hold unraised: `catena.css` 7,629/8,000 whole and 2,676/2,700 stripped,
unchanged; `catena.js` 12,993/13,000 whole and 8,202/8,800 stripped, the
composition 161 bytes lighter than V5. The boundary moved further into
`catena-model.js`, which carries no ceiling; the relocation is disclosed and is
not offered as unchanged practical load.

### E1 Catena correction V7 — 2026-08-15

Answers the fresh independent review `f183ed1b0afc6f14574a3507f6eaf3102dc999fa`
(**CHANGES REQUIRED** at exact candidate
`4639b139f2179b1fca7f9cb1e4ba3ac19c9bbc46`, evidence
`ca2a8659010b3fca2ccada24f9c431796ca702b1`) with an explicit typed projection
in place of raw fragment copying.

The review's central finding is a SHAPE. `chapterFragments` copied every own
property of the shared source record and then of the fragment into one object,
and cleared afterwards the two fields it knew were dangerous — `text_path`
only when a valid composed form existed. Where the fragment's id or its file's
prefix could not be read, the record's own `text_path` survived the copy and
reached the real request sink. V7 projects instead: a record of known,
validated fields and nothing else, with `text_path` composed from the file's
own prefix and the fragment's own identity, and a carried path accepted only
where its stem is that fragment's own id — so it can address one file, the
text of the fragment that carried it.

The same reading closes the rest. Hollow fragment, absence and refusal members
make no rows, tallies or claims; an absence source is validated before it
claims a work's row; a refusal needs the closed kind and the chapter matched
against the chapter being read; a contradiction contributes no rights prose at
all; `partial` stops being coerced in the generator; and holdings, canon,
voices, the edition manifest, the paragraph layer, the verses container and
the chapter spine each distinguish a corpus read and found empty from a corpus
state that could not be established.

Oracles that had blessed those defects are corrected in place with their
reasons; the late-work guard grew from thirteen sinks to thirty-six because
the review found it omitted the final status sink. **This lane attacked its own
change three times and every pass found further defects in it** — five, then
fourteen, then eleven, each round mostly the same class one level under the
last: a container guarded and its members not, a sentinel replaced by one a
payload could still forge, an optional fetch caught one scope above the one
beside it. All are fixed with regressions, and a new guard asserts that no
exported model function throws on a hostile argument. Two confirmed findings are recorded UNFIXED:
one would move a line V6 drew and this review left standing, and one is
composed inside `loadBibles`, which is shared-shell ownership this lane does
not hold.

The evidence half is answered by machine derivation. `derive-claims.py` writes
the claim record and its rendering from one pass; `head-consistency.py` refuses
a package whose prose names a commit it may not name, calls the head a parent,
names a path the package lacks, or leaves a member unreferenced. The sealer's
two defects are fixed: `--check-only` no longer deletes the manifest it is
documented never to touch, and `--verify` now proves every archive member
against that manifest rather than checking the tree and the archive separately
and joining nothing.

`catena.css`, `index.html` and every path under `src/web/data/` are
byte-identical. The production diff is `catena.js`, `catena-model.js` and the
Catena generator alone, and `catena.js` is smaller than V6 left it in both
measures. The `src/web/data/` contradiction is **preserved untouched** and
remains a separate owner's adjudication.

### E1 Catena correction V11 — 2026-08-16

Answers the fresh independent review `f7cad8b0219de8343a0b2cce95e89558ded6946e`
on `review/catena-wave-1-e1-corrections-v10-independent` — **CHANGES
REQUIRED** at exact V10 head `ea15d16d22d7ceaed989ed9907c236f967738a03`,
which independently verified evidence
`ff49c83e4f26570bd4c07d8fc8703f94c331d92a` and ZIP SHA-256
`4c71d1c15bd1f1992bf29a1d84342f11a8b671b5b5bd6bdcc4341de091e23e2f` — with
exactly its stated next action and nothing else. Current `origin/main` is
`e7f468e842727a817631d12f0854f8249556a8ff`.

The review closed nothing it had passed: ordinary refusal consumption
before the cache and request sink, genuine absence against ordinary
refusal, the V9 request closure, the cold, present-valid and prewarmed
vectors, the primitive namespace matrix, ownership boundaries and the
existing ceilings all stand and are not reopened here.

V10 closed the exported claim boundary's SHAPES and not its MEMBERS.
`bag()` proved a record had arrived and property lookup then answered from
the prototype, so `Object.create({stated: false, trail: ''})` opened the
carried fallback as though it were this route's own absence, and an
inherited valid statement composed an address the page never derived; the
committed matrix was eight plain literals. Every semantic member is now
read once as own data through its descriptor — nothing inherited is seen,
an own accessor is never invoked, and a claim whose three-member contract
is partly written above it fails closed rather than being adjudicated. The
same reading covers the spine's own prefix, the carried path, the
fragment's id and source, the edition join and the extent members; the
wider fragment and edition contracts stay field-validated, and that limit
is stated rather than glossed.

The shared refused sentence also asserted more than most states establish.
`A text reference was supplied ... cannot be used as written` claims a
supplied reference and a written form, and V10 gave it to `null`, a record,
a list, a number, a flag, `''`, whitespace and every malformed direct
claim. The claim now carries whether a non-empty textual value was supplied
at all, and the weaker state says only `No text reference is established
for this fragment, so no text is shown.` — no holdings, file-existence,
request-failure or blame claim, and no assertion that anything was supplied
or written. The two genuinely supplied-and-refused states keep the stronger
sentence, because for them it is true.

The proof is completed where it was thin. A fourteen-case inherited and
accessor matrix pins that no such claim creates a request, reopens
fallback, composes a path, changes refusal or absence state, renders a body
or alters ownership, and asserts the planted accessors ran zero times.
Every unestablished prefix is driven to the visible and request sinks
against a planted carried body — V10's neutrality test inspected the
constant and drove nothing. The genuinely-late vector states an expected
value for all 36 guarded fields at both ends of the release instead of 13,
with a coverage test that fails if the guard widens without the proof, and
the release is pinned as the only thing permitted to move. A harness hook
pins the renderer's before-the-sink order with the refused-plus-usable-path
row the model never emits, against a control that really does fetch.

The packaged journal now reproduces ownership without the harness: each row
states sequence, address, record kind, owning step, and outcome —
completed, held, released or failed. P8 no longer executes any Python from
inside the reviewed ZIP; it runs trusted out-of-archive copies, records
each tool's trusted and shipped digest, fails hard on divergence, and
rehashes the archive after every check with an explicit pre/post equality
verdict. Provenance is read per command, so a step that dirties the tree is
recorded dirty. Log identity comes from an append-only attempt ledger, the
index is derived mechanically, the assembly writes an outer invocation log,
the gate comparison is a recorded step, and every failure path marks the
abandoned attempt non-authoritative with one reason. ZIP entries carry a
fixed DOS-epoch stamp and suffix-derived modes, so no builder offset or
umask is disclosed. The sanitizer gained convention-shaped workspace and
lane-evidence rules and rewrites local-offset timestamps to UTC so ordering
survives and the offset does not. A new handoff-inventory tool checks
`HANDOFF.md` against the protocol's ten required contents and reproduces
the review's eight-of-ten finding against the V10 package unaided.

Fresh checks: focused Catena 534 green, up from 522; catena check
1,351/1/73; full discovery 1,885 with the inherited 14/13/11 and the same
27-entry name set, none a Catena identity; browser gate 2,290 at
1,836/226/228 over 171 pages and 19 routes, identical to V10;
`make -k check` red on the same four targets at the parent and at this
head, all inherited — V10's "additional at head" label was false and is not
repeated; promise ledger valid; four stale bindings fail-closed and
unsigned. Budgets unraised: `catena.css` byte-identical, `catena.js`
12,980/13,000 whole and 7,554/8,800 stripped, the page's code smaller than
V10's. The unbudgeted model's growth is disclosed and its governance
remains the budget owner's.

All other blockers remain open and untouched, and E1 is not integrated. No
merge, re-signing, deployment or cutover is authorized.

### E1 Catena correction V10 — 2026-08-16

Answers the fresh independent review `55df5c236a1dfda12bb974efdbb9f46d0aeb3436`
(**CHANGES REQUIRED** at exact candidate
`3c5b78249193df065c4e1c2ee5a98e5989c6e582`, published review head
`4f00e04bdd1fd63702a51bfdafef256b468bef77`, evidence
`eb1ee9987425339c2b5522987bee1fb862cd7d33`) with exactly the review's stated
next action: the refused-prefix presentation closure, the exact terminal
vectors, and a protocol-correct package, and nothing else.

The review passed the V9 request-layer closure entire and proved its third
state stopped at the model: `catena.js` never read `text_refused`, sent the
refused row's empty path through the same `ABSENT` sentinel as genuine
absence, and told the reader the fragment "carries no text file" — false of
a fragment whose spine stated a reference this page declined. The page now
consumes the projection before the request sink: a refused row renders one
neutral sentence, stated once in the unbudgeted model, saying a supplied
text reference cannot be used as written — and no path, carried, cached, or
late, may answer it. Absence keeps its own sentence, the two claims are
pinned as visibly distinct, and the exported claim boundary is closed:
absence is the one shape `{stated: false, trail: ''}`, and every
contradictory direct claim — the review's `{stated: false, trail: <valid>}`
included — resolves no text and projects as refused.

The four terminal vectors are pinned to expected values, not to each other:
cold, present-valid, prewarmed, and genuinely-late each assert the whole
owned request journal — the replay now records each request's owning step
and captures `history.state`, the sink the review found uncaptured — row
identity, the standing and journalled announcements, tally, busy, hash,
history, focus, error and failure sinks; the late vector pins B's complete
terminal baseline before AND after a release pinned at exactly
zero-then-one, retaining the full 36-field guarded comparison. The focused
suite goes 519 to 522; every ceiling holds — `catena.js` 12,987/13,000
whole where the sentence's consumption is paid inside the margin — and the
unbudgeted model's growth is disclosed at +562 gzipped whole. All other
blockers remain open and untouched, and the lane returns for fresh
independent review.

### E1 Catena correction V9 — 2026-08-16

Answers the fresh independent review `611b5eed8128ad5f84f6bf73ac9f9ead5959ab7f`
(**CHANGES REQUIRED** at exact candidate
`7e4df42a21bc2be2d28ff14943f63af3e7e3a6f8`, evidence
`60122b472c3f9a09aff5f8663eb3b062c585a557`) with exactly the review's stated
next action: the composed prefix/fallback closure and a truthful final-byte
package, and nothing else.

The review passed every isolated namespace case and proved the COMPOSED rule
open: a prefix the file never stated and a prefix the file stated and the
page refused both left `textTrail` as `''`, and the carried-fallback door
opened on that one `''` — so a refused `structure/paragraphs/` prefix still
fetched the valid same-stem carried `structure/catena/text/` file and
rendered its planted body. The prefix is now a statement, `{stated, trail}`:
absence is property absence on the spine record, everything carried is a
statement, and a statement that fails validation is REFUSED — terminal, no
composed request, no carried fallback, kept on the row as `text_refused`.
Only genuine absence opens the carried door, and only for a path that
validates byte-exactly with the fragment's own stem.

The regressions pin the reviewer's exact vector cold, prewarmed and
genuinely late at the production sinks — whole journal, rendered body, rows,
announcement journal and standing `statusText`, tally, busy, hash, history,
focus, error and failure sinks — and fail nine ways at the uncorrected
parent. The package pipeline now freezes its inventory before derivation,
names derived members without sizing or hashing them, and proves its claims
against the final sealed bytes by a read-only post-seal verification from
the ZIP alone, with the retained parent run and the discarded `/tmp` run
explicitly ledgered. The focused suite goes 510 to 519; every ceiling holds
byte-identical; the unbudgeted model's growth is disclosed at +833 gzipped
whole. All other V7 blockers remain open and untouched, and the lane
returns for fresh independent review.

### E1 Catena correction V8 — 2026-08-15

Answers the fresh independent review `d9ad5ec1ae35c308a0da5ed3456fd05fdad97cbd`
(**CHANGES REQUIRED** at exact candidate
`e876b29e5797edcc6e86422daa807f4b1104ec81`, evidence
`92c88ab8c2d2b671009e8cf9f36aa5dd352f9b61`) with exactly the review's stated
first bounded commit: the byte-exact text namespace closure, and nothing else.

The review proved at `fetch` that a well-formed directory of this data root
was enough. `trail` and `leaf` state what a path looks like, not which
directory this route owns, so a `text_prefix` of `structure/paragraphs/`
composed and requested another namespace's file, a carried
`structure/paragraphs/text/<same-id>.json` passed the same-stem check and
fetched a real Sources text sharing that id, and whitespace-wrapped paths
were trimmed into validity. The model now states the namespace once —
`TEXT_HOME`, byte-exact `structure/catena/text/` — and requires it at a
directory boundary with no whitespace repair for the composed and carried
form alike, before projection completes. An address outside the owned
namespace becomes no request, no fallback, no rewritten path and no claim.

The regressions are driven at the real request sink: three adversarial replay
scenarios plant a real body at the wrong-namespace address, pin the entire
fetched journal, assert the planted words appear at no sink, and hold the
terminal state. The focused suite goes 505 to 510; all 1,356 real corpus text
paths and all 47 fixture carried paths stand unchanged; every ceiling holds
at V7's exact figures with `catena.js` and `catena.css` byte-identical. The
other V7 findings are recorded open and untouched, and the lane returns for
fresh independent review.

## Remaining program sequence

| Work | Current state | Exact dependency / stopping line |
| --- | --- | --- |
| B0/B1 shared non-liturgy implementation and harness | Authorized separately; not owned by this design branch | May use accepted A3/A4 direction and implementation findings; must stop before inventing C0/C1/D0/E0/F0 compositions and must not enter protected liturgy files. |
| C2/D1 production surface implementation | Eligible after the shell ownership boundary is clean | C0/C1/D0 are accepted; avoid branches that contend for global generator, site CSS, release binding, or shell files. |
| E1 Catena production implementation | Twelfth correction candidate (V11) awaiting fresh independent review; the disposition it answers is **CHANGES REQUIRED** at exact V10 head `ea15d16d2` (independent review `f7cad8b02` on `review/catena-wave-1-e1-corrections-v10-independent`, 2026-08-16) | That review passed the ordinary refusal path entire — the normalized refusal consumed before the cache and request sink, genuine absence kept distinct, the V9 request closure, the cold, present-valid and prewarmed vectors, the primitive namespace matrix, ownership boundaries and the existing ceilings — and found the boundary and the reader claim both wider than those cases. `fragmentRow` trusted inherited and accessor-backed `stated` and `trail`, so an object inheriting the absence shape opened the carried fallback and an inherited valid statement composed a request; the shared refused sentence asserted a supplied, written reference for malformed states that establish neither; 23 of the 36 late-guard fields were held by before/after equality alone; the packaged journal dropped the ownership the harness recorded; and the package's provenance, privacy, screenshot, complete-inventory, unique-run and read-only-P8 claims were incorrect despite exact ZIP arithmetic. Its exact next action: require own non-accessor claim members, give malformed and unestablished claims truthful presentation, add the inherited/accessor/visible/request/cache regressions, exact-pin every material late sink, and issue a privacy-safe, visually evidenced, fully inventoried package with preserved unique run and discard logs and a non-executing P8 that rehashes after verification. V11 is that correction alone; every other enumerated blocker remains open for the authorized continuation. Preserve accepted E0 and every sound V2–V10 correction. The exact Catena data seam is authorized but transfers no broader ownership; release, common-gate, B0/shared-shell, Day-reader guard, real-device/AT, protected Liturgy and PDF prerequisites remain separate. E1 stays off main. No merge, re-sign, deploy or cutover. |
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
| 2026-08-13 | E1 Catena correction V4.1 | Answered the two requirements V4 at `e40720d5d` disclosed as unmet. The shared fail-closed umbrella copy is neutral: the reference line, heading and status write no longer claim the address was unreadable, assert a holdings negative over addresses refused on grammar, or call the reader's values invalid, while the typed per-value reason is untouched and malformed and unsupported refusals stay distinguishable; one narrow regression pins it and fails on the previous copy. The missing captures were produced -- V4's stated reason, that no display was available, was incorrect, because headless Chromium needs no display server -- giving 53 images from real built artifacts at the parent and this head across nine route states, three viewports, forced-colors and print emulation, with before/after pairs for the two changed states; they evidence rendering only and do not supersede the real-AT limitation. Focused suite 267 green; full discovery 1,618 against the base's 1,617 with an identical 27-entry failure/error name set; browser gate 2,290 assertions deep-equal to the base across 480,881 bytes; `catena.css` byte-identical and `catena.js` 12,970/13,000 whole and 8,734/8,800 stripped, both smaller, no ceiling raised. The `src/web/data/` contradiction is preserved untouched for independent adjudication. | Branch `impl/catena-wave-1-e1-corrections-v4-1`; base `e40720d5d622e8b0528b8c714cc5caee0b21cee3`; head `3fb6685b2c725adca9a1e0efb43cfdd55c68c311`; package `20260813T164804Z-catena-e1-corrections-v4-1`; awaiting fresh independent review. No merge, re-signing, deployment, or outside-owner work occurred. |
| 2026-08-14 | E1 Catena correction V5 | Answered independent review `7f69575b9` (**CHANGES REQUIRED** at `f93757854`) with one record boundary rather than a list of guards, placed in `catena-model.js` because `catena.js` had thirty gzipped bytes of margin. The model now owns what a number of this corpus is, what a language code is, what the members of a collection are, and the derivations the page performed by concatenation over raw members. Real Chromium at the base rendered `lang="[object Object]"`, replaced the page with `Cannot read properties of null (reading 'source')` when one collection member was null, manufactured `4 works standing here have no English this project may publish` from rows whose findings said no such thing, printed `1 words` for a boolean and `12.5 words` for a fraction, requested `browse/[object%20Object]001.json`, and left `Loading…` standing after a malformed canon with nothing spoken; the head does none of these. Three defects the review did not name were found by writing its required regressions: the replay shim did not reflect `lang` into the content attribute, which is why the proven sink was invisible to the suite; `sound()` passed `not a language code` into visible language prose; and `render()` had a silent early return that left the page unterminated. Focused suite 306 green, up from 267; browser gate 2,290 assertions deep-equal to the base; promise ledger valid at 30 tracked / 19 complete; `catena.css`, `index.html` and all of `src/web/data/` byte-identical; `catena.js` 12,990/13,000 whole and 8,363/8,800 stripped, 371 bytes smaller stripped, no ceiling raised. The `src/web/data/` contradiction is preserved untouched. | Branch `impl/catena-wave-1-e1-corrections-v5`; parent `f93757854b54c19e50bdcb97ca0fed9b48d22bb7`; review addressed `7f69575b982926e827974f2ed236b1c8bfd8aaad`; package `20260814T123524Z-catena-e1-corrections-v5`; awaiting fresh independent review. No merge, re-signing, deployment, or outside-owner work occurred. |
| 2026-08-14 | E1 Catena correction V6 | Answered independent review `fa5b2f601` (**CHANGES REQUIRED** at `19982ab43`) by validating every semantic root, collection member, textual identity and bootstrap payload into an accepted typed representation before rendering, routing, counting or state derivation. `{}` no longer counts itself as a work this project holds and cannot name, nor refuses a boundary in Scripture's own numbering; a one-member list no longer resolves a real edition by property-key coercion; `../../../etc/passwd.json` is no longer composed or requested; an unreadable language is omitted rather than answered with `en`, and an unreadable testament rather than answered with `New Testament`; findings are read as a set, so the same records listed the other way round no longer make a different claim about a work's rights, and a self-contradicting record is declined rather than resolved to the harsher claim; a stray `partial` licenses nothing; `"01"` no longer renders verse 1 a second time; and JSON `null` no longer throws past the bootstrap's request catch — at the parent it still kills the whole replay process, which ships unfiltered. One defect the review did not name was found by writing its required regression: judged against an empty canon the page answered `Gen is not a book of this canon`, a claim about the canon drawn from a parse failure. Eight oracles that expected the defects are corrected with their reasons recorded; the harness now reads the rendered Scripture, the uncounted tally chips, the edition options and their route values, the testament line, the absence rows' own identity, the visible failure paragraph and a count of parked requests actually released. Focused suite 423 green, up from 306; full discovery 1,774 against 1,657 with 14 failures, 13 errors and 11 skips at both ends and an identical 27-entry name set; browser gate 2,290 assertions deep-equal excluding four volatile fields; promise ledger valid at 31 tracked / 19 complete AT THIS HEAD; `catena.css`, `index.html` and all of `src/web/data/` byte-identical; `catena.js` 12,993/13,000 whole and 8,202/8,800 stripped, 161 bytes lighter in composition, no ceiling raised. Every V6 test class fails at the uncorrected parent. | Branch `impl/catena-wave-1-e1-corrections-v6`; parent `19982ab433dd25704ed60b1ac6ddb678bc3a98f9`; review addressed `fa5b2f601565508acee2b1b236b0c69138af07a3`; package `20260814T182026Z-catena-e1-corrections-v6`; awaiting fresh independent review. No merge, re-signing, deployment, or outside-owner work occurred. |
| 2026-08-15 | E1 Catena correction V7 | Answered independent review `f183ed1b0` (**CHANGES REQUIRED** at `4639b139f`) by replacing raw fragment copying with an explicit typed projection. `chapterFragments` had shallow-copied every own property and cleared `text_path` only when a composed form could be built, so a fragment whose id or whose file's prefix was unreadable kept the record's own `text_path` and the page requested it; `text_path` is now composed, and a carried one is accepted only where its stem is that fragment's own validated id, which is what keeps the sample corpus working. Hollow fragment, absence and refusal members make no row, tally or claim; an absence source is validated before it claims a work's row, so a hollow source no longer renders blank and masks the valid sibling behind it; a refusal needs the closed kind and the chapter matched against the chapter being read, which stops a chapter-1 record establishing chapter 2's boundary; a contradiction contributes no rights prose, where V6 declined the finding and then printed one side's reason chosen by length; `partial` stops being coerced in `scripts/_catena.py`, where `str(row.get("partial") or "")` turned a mapping into prose; and holdings, canon, voices, the edition manifest, the paragraph layer, the verses container and the chapter spine each distinguish a corpus read and found empty from a corpus state that could not be established. Ten oracles that blessed those defects are corrected with their reasons recorded, and the late-work guard grew from thirteen sinks to thirty-six after the review found it compared the announcement journal rather than the live region a stale write could replace. This lane attacked its own change twice: the first pass found five further defects, one introduced by the correction, all fixed with regressions, and one confirmed finding is recorded unfixed rather than settled by a lane that cannot settle it. Package claims are machine-derived from one pass and a checker refuses prose that disagrees with them; the sealer no longer deletes the manifest in its read-only mode and now proves every archive member against it. `catena.css`, `index.html` and all of `src/web/data/` byte-identical; no ceiling raised, and `catena.js` smaller than V6 left it in both measures. **Every figure is derived at the sealed head and recorded in the package's own claim record rather than restated here, which is the direct answer to the five counts this review found wrong.** | Branch `impl/catena-wave-1-e1-corrections-v7`; parent `4639b139f2179b1fca7f9cb1e4ba3ac19c9bbc46`; review addressed `f183ed1b0afc6f14574a3507f6eaf3102dc999fa`; awaiting fresh independent review. No merge, re-signing, deployment, or outside-owner work occurred. |
| 2026-08-15 | E1 Catena correction V8 | Answered independent review `d9ad5ec1a` (**CHANGES REQUIRED** at `e876b29e5`) with exactly its stated first bounded commit: the byte-exact `structure/catena/text/` namespace closure at the request sink, and nothing else. `trail` and `leaf` stated what a path of this data root looks like and nothing stated which directory the route owns, so `structure/paragraphs/` composed a request, a carried same-stem `structure/paragraphs/text/<id>.json` fetched a real Sources text sharing that id, and whitespace-wrapped paths were trimmed into validity. The model now states the namespace once — `TEXT_HOME` — and `textTrail`/`textLeaf` require it byte-exactly at a directory boundary with no whitespace repair, for the composed and the carried form alike, before projection completes; `catena.js` is untouched. Three adversarial replay scenarios plant a real body at the wrong-namespace address, pin the entire fetched journal, assert the planted words reach no sink, and hold the terminal state. Focused suite 510 green, up from 505; catena check 1,351/1/73 with all 1,356 real and 47 fixture paths unchanged; browser gate 2,290 assertions with the inherited 1,836/226/228 and 117/82/27 identity; budgets unraised with `catena.js` and `catena.css` byte-identical at 12,901/13,000, 7,530/8,800, 7,629/8,000 and 2,676/2,700; the unbudgeted model's growth is disclosed at +514 gzipped whole. All other V7 findings recorded open and untouched. | Branch `impl/catena-wave-1-e1-corrections-v8`; parent `e876b29e5797edcc6e86422daa807f4b1104ec81`; review addressed `d9ad5ec1ae35c308a0da5ed3456fd05fdad97cbd`; awaiting fresh independent review. No merge, re-signing, deployment, or outside-owner work occurred. |
| 2026-08-16 | E1 Catena correction V9 | Answered independent review `611b5eed8` (**CHANGES REQUIRED** at `7e4df42a2`) with exactly its stated next action: the composed prefix/fallback closure and a truthful final-byte package, and nothing else. `textTrail` collapsed a prefix the file never stated and a prefix the file stated and the page refused into the same `''`, and `fragmentRow`'s truthy test read that `''` as leave to consult the carried `text_path`, so the reviewer's refused `structure/paragraphs/` prefix still fetched a valid same-stem carried file and rendered its planted body. The prefix is now the statement `{stated, trail}`: absence is property absence on the spine record, every carried shape is a statement, a refused statement is terminal and kept on the row as `text_refused`, and the carried door opens only on genuine absence with a byte-exact own-stem path; `catena.js` is untouched. The regressions pin the exact vector cold, prewarmed and genuinely late at the production sinks — whole journal, body, rows, announcement journal and standing `statusText`, tally, busy, hash, history, focus — and fail nine ways at the uncorrected parent; a model-level matrix classifies thirteen refused shapes beside the absent and valid states. The handoff pipeline freezes its inventory before derivation, names derived members unsized, and verifies its claims read-only against the final ZIP, with the retained parent run and the discarded `/tmp` run ledgered. Focused suite 519 green, up from 510; catena check 1,351/1/73; browser gate 2,290 with the inherited 1,836/226/228 and 117/82/27 identity, whole report identical; budgets unraised with `catena.js` and `catena.css` byte-identical at 12,901/13,000, 7,530/8,800, 7,629/8,000 and 2,676/2,700; the unbudgeted model's growth is disclosed at +833 gzipped whole. All other V7 blockers recorded open and untouched. | Branch `impl/catena-wave-1-e1-corrections-v9`; parent `7e4df42a21bc2be2d28ff14943f63af3e7e3a6f8`; review addressed `611b5eed8128ad5f84f6bf73ac9f9ead5959ab7f`; awaiting fresh independent review. No merge, re-signing, deployment, or outside-owner work occurred. |
| 2026-08-16 | E1 Catena correction V11 | Answered independent review `f7cad8b02` (**CHANGES REQUIRED** at `ea15d16d2`) with exactly its stated next action: the inherited/accessor claim closure, truthful malformed-state presentation, the complete late vector, and package/provenance/privacy correctness, and nothing else. `bag()` proved a record had arrived and property lookup then answered from the prototype, so `Object.create({stated: false, trail: ''})` opened the carried door as this route's own absence and an inherited valid statement composed an address; every semantic member is now read once as own data through its descriptor, an own accessor is never invoked, and a claim whose contract is partly written above it fails closed. The refused sentence asserted a supplied, written reference for states establishing neither, so the claim now carries whether a non-empty textual value was supplied and the weaker state says only that no text reference is established. A fourteen-case inherited and accessor matrix pins zero requests, zero fallback, zero body leak and zero accessor invocations; every unestablished prefix is driven to the visible and request sinks; the late vector states an expected value for all 36 guarded fields at both ends with a coverage test that fails if the guard widens without the proof; and a harness hook pins the renderer's before-the-sink order with the refused-plus-usable-path row the model never emits. The packaged journal gains each request's kind, owning step and outcome; P8 executes no archive code and rehashes the ZIP after every check; provenance is read per command; log identity comes from an append-only attempt ledger with mechanical index, an outer invocation log and explicit discard markers; ZIP entries carry a fixed epoch and derived modes; the sanitizer gained convention-shaped workspace and lane-evidence rules and rewrites local timestamps to UTC; a new handoff-inventory tool reproduces the review's eight-of-ten finding unaided. Focused suite 534 green, up from 522; catena check 1,351/1/73; full discovery 1,885 with the inherited 14/13/11 and the same 27-entry name set; browser gate 2,290 at 1,836/226/228, identical to V10; `make -k check` red on the same four targets at parent and head, all inherited; budgets unraised with `catena.css` byte-identical and `catena.js` 12,980/13,000 whole and 7,554/8,800 stripped; the unbudgeted model's growth disclosed. All other blockers recorded open and untouched. | Branch `impl/catena-wave-1-e1-corrections-v11`; parent `ea15d16d22d7ceaed989ed9907c236f967738a03`; review addressed `f7cad8b0219de8343a0b2cce95e89558ded6946e`; awaiting fresh independent review. No merge, re-signing, deployment, or outside-owner work occurred. |
| 2026-08-16 | E1 Catena correction V10 | Answered independent review `55df5c236` (**CHANGES REQUIRED** at `3c5b78249`, published head `4f00e04bd`) with exactly its stated next action: the refused-prefix presentation closure, the exact terminal vectors, and a protocol-correct package, and nothing else. The page now consumes `text_refused` before the request sink, so a present-invalid prefix renders one neutral model-stated sentence — a supplied text reference cannot be used as written — instead of the false `carries no text file`; genuine absence keeps its own sentence and the two claims are pinned visibly distinct with a positive control each way; absence at the exported claim boundary is the one shape `{stated: false, trail: ''}` and every contradictory direct claim projects as refused with no request, substitution, or body leak. The replay journals each request's owning step and captures `history.state`; cold, present-valid, prewarmed, and late are pinned to expected values at every material sink, the late vector pinning B's full terminal baseline before and after a release pinned at exactly zero-then-one over the retained 36-field guard. Against the uncorrected parent the V10 file yields nine failing subtest identities across seven behavioral methods while the neutrality sweep and the present-valid, genuine-absence, and late-non-vacuity controls pass. Focused suite 522 green, up from 519; catena check 1,351/1/73; full discovery 1,873 with the inherited 14/13/11 and the same 27-entry name set; browser gate 2,290 at 1,836/226/228; promise ledger 35 tracked / 19 complete; budgets unraised with `catena.css` byte-identical and `catena.js` 12,987/13,000 whole and 7,565/8,800 stripped; the unbudgeted model's growth disclosed at +562 gzipped whole. The package pipeline gains unique refusing logs, contemporaneous exact-SHA/clean/cwd provenance, a P8 transcript bound to the exact ZIP with duplicate-row checks and derived final-byte totals, a timestamp-refusing assembler, and accurate lane labels. All other blockers recorded open and untouched. | Branch `impl/catena-wave-1-e1-corrections-v10`; parent `3c5b78249193df065c4e1c2ee5a98e5989c6e582`; review addressed `55df5c236a1dfda12bb974efdbb9f46d0aeb3436`; published review head `4f00e04bdd1fd63702a51bfdafef256b468bef77`; awaiting fresh independent review. No merge, re-signing, deployment, or outside-owner work occurred. |

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
