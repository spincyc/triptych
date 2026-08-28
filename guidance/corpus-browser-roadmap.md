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

### E1 Catena V16 independent final publication / evidence review — 2026-08-28

Independent review of exact V16
`cc1f2fb8625f044558c26edd358b99cd7dcc7646`, parent
`b9202882badbbbc364f1dd3d9057d2710ee47552`, V15 review
`67247ecc39a6e5f6224c64ca3ab1af163ee023b1`, evidence commit
`bfa913466c559ad410f252f4192fb3af953dd10b`, and archive
`20260827T230425Z-catena-e1-corrections-v16.zip` (2,172,189 bytes, 76
members, SHA-256
`bb473e7afbfa619182248a02fdc4db28b645792cba054e8be3cf660ff845d4fb`)
returns **SEMANTIC CHANGES REQUIRED**, **EVIDENCE CHANGES REQUIRED** and
**CHANGES REQUIRED** overall. `origin/main` remained
`2778285849f2973ea89d1cfd5b2751ed4ae58e54`; no integration is authorized.

The V15-targeted runtime correction substantially passes. No unresolved value
is published by path; the cache holds only a finished frozen null-prototype
seven-scalar content record; a later caller rebinds that value through its own
sealed row/projection/path transport completion; arbitrary and cross-owner
content is refused; application is recorded only after a confirmed write;
same-path B remains exactly B after late A; failures do not cross owners; and
all twelve production consumers, including provenance, retain actual object
identity. Focused replay is 615/615 parent and 660/660 head. The V16 file over
the parent gives 604 methods, 565 pass, 39 failing methods, 288 failure rows
and zero errors. The package's ten-closure label conflates eight runtime groups
with a provenance proof addition and observation-record correction.

Semantic closure nevertheless fails the review's explicit observation rule.
`normalizeChapter` plain-reads six raw roots, so inherited values and own
getters become fragments, sources, refusals, unfetched state, blocked rows and
leads. An exact probe produced an authoritative hostile row both from an
inherited `fragments` value and from an invoked own getter. Separately, an
inherited `then` getter observed twice across `response.json()` / async
`loadJSON()` can substitute a forged document before the otherwise-sound
own-descriptor `textPayload` finalizer runs. The exact probe finalized the
forged body after two getter calls. The source/text observation vectors are
accurate inside their fixtures, but their unqualified no-hostile-authority
claim is false.

Validation remains endpoint-stable: full discovery 1,966/2,011 with identical
14F/13E/11S over 27 rows and 22 identities, none Catena; browser gate
2,290 = 1,836/226/228 with equal sealed normalized reports; the same inherited
four `make -k check` targets; promise ledger 40/19 to 41/19; Catena
1,351/1/73; four stale unsigned release bindings. Budgets are unraised:
`catena.js` 12,958/7,724 to 12,965/7,835 under 13,000/8,800;
byte-identical CSS 7,629/2,676; uncapped model 41,077/9,536 to
44,247/10,344.

Cold V16 attempts 15/16 each report 30 divergent rows over 28 distinct command
strings and two separately declared volatile lines, with equal endpoints.
Historical V15 warm is 28/27 plus two declared volatile lines. The only new
divergent string is `tools/mass-ordinary check --out build/example-ordinary`.
The requested 32/30 totals sum values that durable and sealed prose says must
never be summed, so the underlying sets pass but the derived total has
contradictory authority.

The live/frozen/slice attempt counts are mechanically 32/31/25, and the final
32 are terminal with zero unresolved or reused ordinals. Ordinal 32's P5
unevidenced state followed by P9/P12 authority is temporally coherent. The
31-attempt member has no as-of field yet is called full, a 23-attempt
PROVENANCE table is falsely attributed to it, and the 25-attempt sibling is a
filtered slice. Complete-history closure therefore fails.

Archive identity and P8 pass exactly: 13 checks, zero problems/skips, unchanged
pre/post ZIP. The decisive authority defect does not. Authority's
`d14ce84c523c9d2ea6908acb5ca6fabf3ef5d7419954005f706e5573e50289a2`
hashes only ledger rows 1–401; all 402 rows hash
`e80d6508b88fdec0f005aa7f4a69679f0ac67dfb8cba0849290146eb2f8be184`.
P12 appends row 402 after hashing and runs no finished-mode coherence gate.
Recorded authority coherence is only a truthful P10 pending-bindings PASS.
Completeness remains COMPLETE under its naming/existence scope, but the final
outer scan is not clean: P12's last two local-offset rows were appended after
P11 and a final scan finds four substitutions/two hits.

Fresh-clone focused and parent replays reproduce their expected results. The
browser replay requires an unrecorded `make public-site` prerequisite; after
it, counts reproduce but 27 date-sensitive title details differ from the sealed
report because the date is unpinned. The authoritative attempt omitted the
required reviewer-style transcript. All current 24 structured command rows
rederive executable, but 17/39 broader prefix-prose mutations evade the finite
heuristic, and raw `ELIDED` text can satisfy the checker when prelabelled.
P10 accounting is 23 referenced / 15 executed / 30 recorded invocations / 21
shipped / 8 trusted-not-executed. Both build drivers ran, but there are two
unique drivers, three semantic run rows and only two battery rows tagged
`driver`. All 21 trusted/shipped hashes match; only the 13 actually executed
shipped tools have a real executed/trusted/shipped triad.

The ZIP privacy boundary passes; retained raw ledgers are unsanitized and the
claimed complete V15 history depends on unshipped local bytes. The authority
scanner permits an unsupported named authority assertion to hide on the same
line as aggregate or denial language, or behind a foreign-ID declaration.
Production ownership remains exactly two Catena files among seven total
changes, with data, release, common gate, shared shell, Liturgy, PDFs, CLI,
CSS, HTML and ceilings untouched.

The exact next action is one bounded V17 from exact V16: normalize every raw
chapter authority collection/member/field from own data descriptors without
invoking accessors, prevent raw text objects crossing thenable-assimilating
async boundaries, and add V16-parent-failing regressions. Preserve the accepted
publication/envelope/journal behavior. Then rebuild evidence with phase-labelled
histories, a closed immutable ledger before hashing, final post-mutation
coherence/privacy gates, hardened command and authority-language classifiers,
reconciled durable records and representative fresh-clone replay. Return for
fresh independent review; do not merge, integrate, re-sign, deploy or broaden
E1.

### E1 Catena correction V16 — 2026-08-27

Answers the fresh independent review of V15 — **SEMANTIC CHANGES REQUIRED** and
**EVIDENCE CHANGES REQUIRED**, **CHANGES REQUIRED** overall, at exact V15 head
`b9202882badbbbc364f1dd3d9057d2710ee47552` on
`impl/catena-wave-1-e1-corrections-v15`, recorded at review commit
`67247ecc39a6e5f6224c64ca3ab1af163ee023b1` on
`review/catena-wave-1-e1-corrections-v15-independent`. The V15 immutable
handoff is archived on `evidence/catena-e1-corrections-v15-handoff` at
`db5f651e4eb2d10a15d1a594a4286ac7048f612c`, and its sealed ZIP
`20260826T195656Z-catena-e1-corrections-v15.zip` is 1,400,092 bytes over 69
members with SHA-256
`711b598ab43543113ccb924234fc8ef4ddb76370ff74d24c72a549da574204ac`. Current
`origin/main` is `2778285849f2973ea89d1cfd5b2751ed4ae58e54`, and this lane is
not integrated with it. The correction is on
`impl/catena-wave-1-e1-corrections-v16`, and its handoff is archived on
`evidence/catena-e1-corrections-v16-handoff`. Neither this record nor the lane
record names its own head or its own package digest: both are members of the
tree those figures describe, so stating them here would change what they state.
They are named in the handoff and in the evidence commit.

The review closed nothing it had passed. The row-transport owner model, the
A-held/B-independent decisive behaviour and its thirty-six-field terminal
vector, the wrapper-created-authority closure, one owner's failure suppressing
no other owner's request, owner-local retry, the hostile nested `edition` and
`edition_published` accessor cases, the thirteen throwing mutations and their
downstream rerender, and every inherited V14 closure are preserved here
undiminished. **They are regressions, not V16 closures**, and this record
counts them apart; the V15 review criticised exactly that conflation.

**The semantic defect.** V15 owner-scoped pending transport correctly, but
`fragmentTexts.set(path, asked)` ran INSIDE the fulfilment handler of the
promise returned by `.then()`, before that handler returned. A promise returned
by `then` cannot settle until its handler returns, so the entry published under
that path was `Promise { <pending> }` at the instant it became reachable, and
publication also preceded the freeze. Ordinary event-loop work cannot
interleave there — which is why the behavioural tests were green — but a
synchronous reentrant operation retrieves the pending entry. The eventual
shared value was the raw parsed file, shallow-frozen at the top level and
carrying a mutable prototype, which `M.textPayload` then read at render time by
ordinary prototype-sensitive lookup: a frozen empty object could turn from
unreadable to readable between one reader and the next. And
`M.bodyAsked(row, content)` proved only that `row` occurred in `rowOwners`, so
an actual B row accepted arbitrary A content; the V15 direct test deliberately
passed `{text: "x"}` with no owned completion behind it. The body journal was
recorded before the DOM write.

**The correction.** `M.textPayload` becomes the FINALIZER, called at settlement
rather than at render: every field taken by own descriptor through `ownData` so
nothing inherited is visible and no getter is invoked, sealed into a
null-prototype, frozen, scalar-only record over the fixed key set
`M.TEXT_SCHEMA`, with `M.NO_TEXT` as the finished value for a row that resolves
no address. The page then publishes the FINAL VALUE and never a promise —
`M.textPayload(file)` runs to completion, then `fragmentTexts.set(path,
content)` — so there is no instant at which a path lookup returns unresolved or
partial work, including reentrantly. A completion ENVELOPE
(`M.textCompleted` / `M.textFailed`) carries the exact `rowTransport` owner
beside the finalized content through settlement, sealed in a `WeakSet` so a
literal of the same shape is not one; it is per-caller by construction and
never becomes the shared path-cache value. **Neither half can be supplied BY
THE DATA** — that is the exact claim, and no stronger one is made. In-realm
code holding a recorder installed through the exported `chapterWitness`
receives the page's actual row objects, and from a real row both
`M.rowTransport` and `M.textPayload` will mint valid halves in five lines; this
is not a security boundary against code already in the realm, which can write
the DOM directly, and any unqualified "cannot be supplied from outside" is
refutable by a five-line probe. `M.bodyAsked(row, completed)` now
requires that the completion be one the model sealed, that its owner be the
transport held for that very row, and that the owner's projection be the
projection that made the row — three exact-object comparisons, no path, no id,
no string — so arbitrary content beside a valid row fails closed. The new
`M.bodyApplied(row, completed, wrote)` records the body AFTER the write is
confirmed and binds owner, row, projection, path, the finalized content value
and the post-write success state; a failed or unconfirmed write leaves no entry
at all. A finished value already in the path cache is rebound to a later owner
through that owner's OWN completion, so the cached value stays owner-independent
and A's owner never crosses into B.

**Ten semantic closures, counted apart from the regressions:** no reentrant
pending path publication; finalized normalized immutable cache values only; the
mutable-prototype payload closure; the exact completion-envelope owner;
cross-owner arbitrary content rejected; body application tied to the completion
owner; post-write journal ordering; **no false applied record on a write
failure — which has two halves and is recorded with both rather than
renumbered to an eleventh, since the enumeration is fixed across the
directions, the records and the package: no journal entry for an unconfirmed
write, and containment, because a throwing body write at the V15 parent escapes
as an unhandled rejection and kills the entire replay (`Ran 35 tests, 98
errors`, every replay class down) where V16's sink contains it and the page
continues. The harness proves this without weakening the probe: an
`unhandledRejection` handler records escapes into a journal instead of being
fatal, and a global method asserts that journal empty across the whole plan —
empty at the candidate, exactly one entry at the parent**;
the provenance-specific committed `===` assertion the review found missing; and
the observation-accounting semantic correction, which adds the `getPrototypeOf`
observation caused by key enumeration and repairs the conflicting `has` versus
own-property-test terminology and the "four kinds"/"nothing else" phrasing.

**Thirteen evidence closures, counted apart:** executable command
representation; unambiguous repo variables; prefix-prose rejection;
mechanically derived tool execution; executed drivers classified correctly; a
complete nine-attempt V15 predecessor-history statement; a complete V16 attempt
history; **the example-replay figure derived mechanically and reported in its
two distinct senses — divergent ROWS and distinct COMMAND STRINGS — with the
volatile count kept apart as the static declaration it is and the cold-`build/`
precondition recorded beside the number**; compare-gate diagnostic granularity;
final completeness taken after the outer sanitize and scan; named outer logs;
direct authority bindings; and an explicit shipped-versus-local
retained-artifact privacy boundary.

**The one V15 fact this lane corrected, then corrected again, with the
experiment shown.** The V15 review found that "the authoritative logs report
**28** divergent examples plus two separately declared volatile lines, not the
durable producer claim of 30 divergences". **The finding stands.** V15's
durable prose claimed 30 while V15's own shipped transcripts —
`logs/attempt-01/make-check-parent.log` and
`logs/attempt-02/make-check-head.log`, inside
`20260826T195656Z-catena-e1-corrections-v15.zip` — each report 28 `DIFF` rows
over 27 distinct commands and each summarise `28 diverged … 2 volatile line(s)
declared`. No artifact in the V15 package supports 30, and V16 says so.
**The review's account of the difference does not survive measurement**, and
neither did V16's first attempt to write it down: V16 initially rewrote the
records to read 28 + 2, treating 30 as a sum. That decomposition is
arithmetically impossible. `volatile` is a static constant at
`scripts/replay_examples.py:734`, `sum(len(lines) for lines in
VOLATILE.values())` over the two-entry table at `:182-185`; both captures are
masked at `:405` and appear in the transcript as `ok` and `absent`, **never as
`DIFF` rows**, so they were never in the set they are supposed to be subtracted
from, and the figure counts DECLARED LINES rather than examples. **The cause is
neither arithmetic nor prose but BUILD STATE.** Measured three times
independently at exact parent `b9202882badbbbc364f1dd3d9057d2710ee47552` in a
clean checkout not under `/tmp`: `rm -rf build/example-ordinary && make
check-examples` exits 2 with **30** `DIFF` rows; run immediately again on the
now-warm tree it exits 2 with **28**. The whole delta is two captures of
`tools/mass-ordinary check --out build/example-ordinary`, which prints `3 files
would be rewritten` cold and matches its recorded `the written files are
current` afterwards, because a later capture in the same target,
`tools/mass-ordinary structure --out build/example-ordinary`, writes the very
directory the earlier captures are compared against. **In V15's shipped
transcripts both of those captures read `ok`, the signature of a warm tree**:
V15 quoted a cold figure while shipping a warm log. Neither number was wrong
about the world; the record never said which tree it was measuring. And 28 is
reachable a second way, which may be what the reviewer saw — the warm log
carries 28 rows over 27 distinct command strings and a cold run 30 over 28,
a row-versus-name conflation of the kind the same review rightly criticised in
`compare-gate.py`. **What V16 takes from this is not a number but a rule: a
count is meaningless without the state it was taken in, and this package states
both.** The battery records `build-state=COLD|WARM` at preflight, the
completeness checker names build state as the cause when a figure and a
transcript disagree, and **the V16 check pins no constant at all** — a check
that pinned 30, or 28, would be wrong in one state or the other; it refuses the
unsound SHAPE, refuses a figure the package's own transcript does not support,
and refuses a summary that disagrees with its own `DIFF` rows. The sequence —
corrected on the review's authority, measured, then corrected again — is left
standing in `PROJECT-WORK.md` and here rather than quietly reverted.

**The other V15 evidence facts corrected here.** The attempt history was
rederived mechanically across all three ledgers by `checks.py --history-table
--lane V15`, and its totals are `package_attempts 9`,
`package_authoritative 1`, `package_non_authoritative 8`, `battery_attempts 5`,
`attempts_with_no_terminal_row 1` (`parent-20260826T181908Z-01rwghhk`),
`ledger_replacements 2` and `reused_ordinals 6` — **ordinal 1 was issued three
times in one lane**. The nine are `package-20260826T180457Z-03qyvspp` (ord 3,
02-retired, discarded on a failed normalize pass), `…-04jzwm3k`, `…-058sn2j5`
and `…-067xmgxg` (ords 4–6, 02-retired, discarded at the attempt-log audit
twice and in the P4 derive once), `…-07z8rv48` (ord 7, 02-retired, sealed then
superseded at the ledger audit), `package-20260826T194118Z-033jkh3w` (ord 3,
shipped, sealed then superseded on a P8 final-verification exit 1),
`package-20260826T195048Z-04wzq5x4` (ord 4, shipped, sealed, **authoritative at
19:52:06Z and superseded one second later** when the authority-coherence gate
refused), `package-20260826T195411Z-05e1bu7n` (ord 5, shipped, discarded at the
attempt-log audit) and `package-20260826T195656Z-06v11wpe` (ord 6, shipped,
**authoritative**). Ledger digests: 01-retired 2,501 B / 5 rows `64683c0b…`;
02-retired 45,619 B / 80 rows `5b0c380c…`; shipped 61,929 B / 107 rows
`3990ff6c05a5a53d4b3a835e92259bd40f94847cfa3ce7e2de300ed66d034640`. No ledger
is a prefix of a later one and no attempt id is shared between any pair, so
these are nine distinct attempts rather than one set counted twice. Two
batteries ran green, had their figures declined and were never marked
`set-aside`, while V15's `PROVENANCE.md:296` states "This lane set no cohort
aside".

**The new checks are calibrated against the real package.** Run over the actual
V15 archive and its actual siblings the rebuilt checker reports `handoff
inventory: INCOMPLETE` with **14 problems** — the seven false-`LITERAL` rows
named by transcript path, the two unnamed outer logs, and the unsupported
example figure. Run over a corrected fixture it reports **`problems: 0` /
`COMPLETE`** with zero non-executable rows remaining. The checks turn the
shipped package's own `COMPLETE` into a correctly-explained `INCOMPLETE`,
rather than merely passing on material built to pass them.

Formerly stated as prose and retained for the detail: there were **nine** V15 package attempts
across three ledgers — eight resolved non-authoritative and one final authority,
plus five battery attempts — not five refusals and a sixth seal: one shipped
ledger of 107 rows over ordinals 01–06, and two retired-and-unshipped ledgers
(2,501 B / 5 rows and 45,619 B / 80 rows) whose five attempts were refused at
P2, P5, P5, P4 and, after sealing, at the ledger audit before P7. Ordinal 04
was sealed, briefly authoritative at P9, then superseded at P10; ordinals were
reissued three times because allocation was file-scoped and the ledger was moved
aside twice; one retired battery has no terminal row; and `PROVENANCE.md`
declares no cohort was set aside while two green retired batteries had their
figures declined. Seven of 24 `LITERAL` command rows single-quote `$WORKSPACE`
or `$REPO` and cannot expand, the parent replay overloads `$REPO`, the
classifier prefix-matches prose such as `format`, `installing` and `zipcode`,
and the handoff checker trusts the label — only 16 of 24 rows were replayable.
Two unlabelled tool-count sets are sealed in one package: `verify-final.log`
and `.tool-bytes.json` say 20 unique tools with 11 executed, while
`.assemble.log` says `executed_tools 14, executed_invocations 27,
merged_battery_invocations 6`; six "not executed" rows are synthesized with a
fabricated `at`, `phase` and `log`; and `assemble.sh` and `battery.sh` are
marked unexecuted though they drove the build. Rerunning V15's shipped
completeness checker after P11 finds the outer-sanitize and outer-scan siblings
unnamed and reports `INCOMPLETE`. In `logs/compare-gate.py`, `walk()` keys
assertions on the name alone, collapsing **2,290 assertion ROWS onto 17
diagnostic NAMES** under last-write-wins and discarding 2,273 before the
per-row diagnostics run
while calling them assertion objects — **the verdict line is nevertheless
sound**, because the final comparison is over the whole report object with all
2,290 assertion rows included minus four named volatile fields, so only the
localising diagnostics were degenerate. **That ROW-versus-NAME conflation is
the general defect, and this lane answers it generally rather than fixing the
one artifact the review named.** It occurs in four places in this evidence —
the gate (2,290 rows over 17 names) and the classifier's own prose, both found
by the review; the example replay (30 divergent rows over 28 distinct command
strings) and full discovery (27 result rows over 22 distinct identities, where
V15's "27 identities" was the row count wearing the identity count's name),
both found here — and a fifth time in the parent-discrimination figure (288
failure rows over 39 distinct methods). **Wherever this evidence quotes a
count, it now says what is being counted.** The published archive and its ten named
siblings pass the privacy scans; the discard and supersession markers, the two
retired ledgers, the lane-wide `executed-tools.jsonl` and the retained
discarded package trees lie outside every scan and preserve builder-local
offsets and raw absolute paths, so no broader all-retained-artifacts privacy
claim is accepted.

**No ceiling is raised, and the page is NOT smaller than V15 left it.**
`catena.js` moves 12,958/13,000 whole-gzip to **12,965/13,000** and 7,724/8,800
stripped to **7,835/8,800**. The whole-file ceiling had forty-two gzipped bytes
of headroom at V15 and the correction is not payable out of forty-two, so the
three sentences the page may say about a body (`TEXT_ABSENT`,
`TEXT_UNREADABLE`, `TEXT_LOST`/`TEXT_FAILED`), the presentation decision itself
(`M.bodySaying`, `M.failureSaid`) and the page's paragraph on its one
point-of-use acknowledgement channel moved to `catena-model.js`, which carries
no ceiling, and the page kept pointers. That paid for the completion envelope,
the finalized-value publication and the confirmed-write journal, and it did not
pay for all of them: the page ends seven gzipped bytes ABOVE V15 at 12,965
against 12,958, and 111 stripped bytes above at 7,835 against 7,724, with
thirty-five bytes under an unraised ceiling. Every version from V4 to V15 could
report the page smaller than its predecessor; this one cannot, and says so
rather than trimming load-bearing prose to buy the sentence. `catena.css` is
byte-identical at 7,629/8,000 and 2,676/2,700, and `index.html` is
byte-identical — its own SHA-256 is
`7779d1f19ca175fd315cd7164f5347cc3c08d68b20b3b68a9219429b02bb8fa8`, which is
the digest OF THE FILE; the release binding for it records `45c491ab…` and is
one of the four separately stale bindings, which this lane re-signs nothing to
close. **Thirty-five gzipped bytes is not enough for the next
correction of any size**, and the uncapped `catena-model.js` has reached
**44,247** whole-gzip and **10,344** stripped against 41,077 and 9,536 at V15,
digest
`64a75834abd8f9efa25ae52c76b904a3437ab96a9508ba82309211215d44c3a3`; that growth
is disclosed, not budgeted, and a governing
ceiling for the model and the combined route-model payload remains open,
separately-owned budget work.

**Two fixes identified by an adversarial review, costed, and deliberately not
made — because they cost more gzipped bytes than the unraised ceiling has.**
The cache-hit branch tests the finished value for truthiness rather than asking
`fragmentTexts.has(path)`; a sealed value is always a non-null object, so this
is safe on today's schema and is a latent trap only if the schema ever admits a
falsy sealed value — **cost to fix 37 gzipped bytes against 35 of headroom**.
And the body write assigns the class before the words; reordering so the words
land first would leave the page wholly untouched by a write that throws before
the body lands, but no such throw is reachable (`T.el`, `licence`,
`insertBefore`, `appendChild` and concatenation over `sound()`-typed strings do
not throw on real data) and **the reorder costs about 60 gzipped bytes**,
because it breaks a repeated pattern gzip was compressing. Both are disclosed,
costed and deferred, rather than paid for by raising a ceiling or trimming
load-bearing prose.

**A refused body application now leaves no journal entry at all.** V15's
`bodyAsked` witnessed every attempt including refusals, so a stale or
cross-owner application turned away still left a `body` row saying so. V16
records only confirmed applications — `M.bodyApplied` appends when the
completion is owner-valid AND `wrote === true`, and `M.bodyAsked` witnesses
nothing — so the journal no longer positively records a refusal. The negative
cases are still proved, by the boundary returning `false` in a committed direct
assertion and by the rendered page being unchanged, but the page-level journal
row V15 had is gone. Disclosed as a deliberate consequence of taking the record
AFTER the write, which is what the review required, not as an oversight.

**Further limitations recorded rather than left to be found.** The post-write
confirmation reads back `text.textContent` — the fragment's body — and does not
confirm the acknowledgement block or the `Extent —` and `Date —` apparatus
paragraphs written beside it, so "confirmed" means the fragment's words reached
the page and nothing broader; that boundary is now a pinned assertion rather
than prose, since the two write-failure modes leave different partial states —
a silent non-take still draws the apparatus, a throw draws none of it, and both
leave the acknowledgement block standing because it is written before the
words. The write runs inside a `try` (`try { said = write(); } catch (problem)
{ said = null; }`), and **the retry flag is deliberately NOT reset there**: an
earlier revision did reset it, and the reset was removed because a throw after
the body had landed would leave the body on the page, no journal entry, and an
invited second full application from the memoised completion. `asked = false`
occurs only in the transport-failure arm, because a network failure is
retryable and a failed DOM write is not; both write-failure modes therefore end
with no entry, no false success and no second attempt. The consequence
disclosed beside the decision is that a write which silently does not take
leaves the fragment showing its previous state with no way for the reader to
retry — unreachable in a real DOM, disclosed because the arm exists. And
`M.rowTransport(row)` is now
consulted unconditionally in `fragmentText`, where V15 consulted it only once
an address resolved, so a projected row that resolves NO address now produces a
transport owner (its `path` is `''`) and one `transport` witness where V15
produced neither — deliberate, because the ABSENT body is a body application
like any other and must be owned by a completion the model sealed, and
disclosed because the request journal now carries one more transport row for
such rows than V15's did.

The production diff is `catena.js` and `catena-model.js` alone. `src/web/data/`,
release-owned records, the common gate, the shared shell, Liturgy, PDFs, the
CLI, CSS and HTML are untouched; the four stale Catena release bindings remain
unsigned and correctly fail-closed and none was re-signed; and broader
projection, orphan and source-only semantics, translator coercion, malformed
absence and refusal typing, selection ordering, unreadable roots and
`bibles.json`, broader terminal and oracle proof, CLI/web duplication,
model-budget governance, the historical data seam, release bindings, the common
gate, the shared shell, device and assistive-technology work, Liturgy, PDFs and
integration remain open or separately owned.

### E1 Catena correction V15 — 2026-08-26

Answers the fresh independent review of V14 — **CHANGES REQUIRED** at exact V14
head `69f2575421ba976271c936b1abd4b39dbe8b98fd`, recorded at review commit
`0d11766ec232b2b4e46a7d1b0ada56ef22370004` on
`review/catena-wave-1-e1-corrections-v14-independent`. The V13 review that V14
answered was never published, so V14 could name no review commit; this lane
can, as every lane from V5 to V12 could. The gap is V13's alone and stays
empty. The V14 immutable handoff is archived
on `evidence/catena-e1-corrections-v14-handoff` at
`f74f8f4d4de44e21afdbef1fc4e9589a9898e986`, and its sealed ZIP is 1,366,960
bytes over 69 members with SHA-256
`414f303954d79b966f4d7f0ad6814376c0014fb73f8e2b78a0d4dc2495124bb1`. Current
`origin/main` is `e4085889fc1b3d2e6721b21166394fe5ea2dea9b`. This lane ran in a
fresh standalone clone: `workspace_mode = fresh-clone`, `worktree = false`,
`git_dir_kind = directory`.

The review closed nothing it had passed. The post-projection `unfetched`
closure, the seven-member raw authority inventory, the tally as a separate
consumer, the raw post-projection audit, the structural member matrix, the
hostile nested-source refusals, the seventeen frozen structures and the exact
null-prototype scope, the carried-path and spine-prefix closures, the fulfilled
prewarm proof, the rights, provenance and refusal DOM cases, and the whole
package protocol are preserved here undiminished. It found one decisive
semantic defect and a set of bounded proof gaps, and it found the evidence
package materially defective.

**The defect.** V14 resolved a text address THROUGH the projected row and then
handed the resolved string to a module-scope `Map` keyed on the path alone that
held the PROMISE. A second row carrying the same address did not ask: it joined
the unresolved promise it found there. Two owners became one, and the answer
the first row's request was made for was rendered under the second. Ownership
was recorded at the address decision and discarded one line later, which is
exactly why the V14 journal could name the owner of every ask while the page
had rendered the wrong body. Replayed against the exact parent, the V15 case
puts A's request in flight and B's page on screen and B's prose is `Loading…`;
after A is released B's prose is `PLANTED BODY A` — A's document, under B's row,
on B's route, in B's projection.

**The correction.** A path map may hold only a settled answer and receives the
promise from inside that promise's own settle handler, so nothing unresolved is
reachable by path. Work in flight is held against `M.rowTransport(row)` — one
frozen owner object per projected row, carrying the row, the projection that
made it and the address it asks. `M.bodyAsked(row, content)` is asked AT the
body application and records the projection, the row and the value written, so
the roster reaches the step that writes the page; a row no projection made
applies nothing, and a reported transport failure is owned as a body is. The
page's substitute record for an unreadable spine is created once per name and
reused, so walking away from an unreadable chapter and back no longer mints a
second authority over it. The decisive case parks only the FIRST ask of a shared
address and answers that address two DIFFERENT documents in turn, so B
rendering its own body and B rendering A's are distinguishable states; B settles
and renders `PLANTED BODY B` while A is held, never renders `PLANTED BODY A`,
and A's late release moves exactly one journal row against a thirty-six-field
terminal vector pinned value by value beforehand. The inverted V14 oracle is
replaced in place with its former assertions quoted beside the correction.

Two owners asking one address concurrently now make two requests where V14 made
one; that is the correction rather than a side effect, since the second request
is what B's own answer is. It costs nothing on a real route: across all 562
chapter spines under `src/web/data/structure/catena/`, holding 1,356 fragments,
no chapter has two fragments sharing a text address or an id. A settled value is
still shared by path, so a row asking afterwards makes no request at all.

**The bounded proof gaps.** The promised nested EDITION accessor case is now
asked directly and gives one coherent outcome across the edition, the printing,
the provenance line, the rights, the voices and the readable state — a proof
gap closed, not a production defect, and the record says so rather than counting
it as a closure. Observation accounting is reported by kind: **zero** value
reads that would run an own accessor, **zero** `in` tests, **three**
`getOwnPropertyDescriptor` observations per source key, **two** per stated
shared field and **one** per absent one, **one** key enumeration, and nothing
further on a second render — with `Object.hasOwn` counted under descriptors
because it is `[[GetOwnProperty]]`, which is why the per-key figure is three.
Deep immutability now survives a downstream rerender: after thirteen attempted
mutations the chapter is drawn again from the same projection and its bodies
applied again, and thirty-two rendered fields and the request journal are
unchanged while the intermediate rebuilt state is asserted to differ.

**Budgets are unraised and the page is smaller than V14 left it.** `catena.js`
moves 12,972/13,000 whole to **12,958/13,000**, and 7,546/8,800 stripped to
**7,724/8,800**. The whole-file ceiling had twenty-eight gzipped bytes of
headroom, so three paragraphs of the page's own prose moved to the uncapped
model and the page kept pointers to them — the same arithmetic V4 through V7
recorded, disclosed rather than paid for by raising a ceiling. `catena.css` is
byte-identical at 7,629/8,000 and 2,676/2,700; `index.html` is byte-identical;
the unbudgeted model moves 39,724/9,396 to 41,077/9,536 and its governance
remains budget-owner work.

The production diff is `catena.js` and `catena-model.js` alone. `src/web/data/`,
release bindings, the common gate, the shared shell, Liturgy, PDFs, the CLI,
CSS and HTML are untouched, and the four stale Catena release bindings remain
unsigned and correctly fail-closed.

### E1 Catena correction V14 — 2026-08-20

Answers the fresh independent review of V13 — **CHANGES REQUIRED** at exact
V13 head `6cc85e1a1dea317a48c0bfcfd6f774201ea3a6c3`, whose immutable handoff is
archived on `evidence/catena-e1-corrections-v13-handoff` at `fd5a1579d` and
whose sealed ZIP this lane re-verified at 1,306,976 bytes with SHA-256
`0965ca5ed6982a570427ae00e14a5bb7b38143bd36aaa90741fadd9eb93322b7` — with
exactly its stated next action and nothing else. **That review has no published
ref.** `origin` carries no `review/catena-wave-1-e1-corrections-v13-independent`
and the branch exists only in a local reviewer checkout standing at the
reviewed head with no review commit on it, so no review SHA is recorded for
V14 and the gap is stated rather than filled. Current `origin/main` is
`ac4b9d608f52e23f199c4b3149c73e5fb14c3d59`.

The review closed nothing it had passed. One chapter is normalized once and
held; `requestSnapshot` is correct for one invocation; the inherited prefix and
inherited refusal close locally; the carried path is read once; the fail-closed
contamination policy stands as a design; the six planted scenarios — carried
path, spine prefix, member and source walk, prewarmed cache, rights and
provenance, refusal — are useful and are retained here undiminished; and the
V13 package protocol is preserved rather than regressed. It found six things.

`unfetched` was the one request-critical chapter member the projection read and
did not carry, so the page read the raw record a second time for the string it
prints. Answering `undefined` while readability was decided and a forged string
afterwards replaced an accepted chapter with a manufactured unavailable state
and printed the payload's own words to the reader. At the parent the member is
asked twice and the page renders *"its record (FORGED RAW REREAD) could not be
read"* over a chapter holding a fragment, a lead, a blocked entry and a Rule 4
refusal; here it is asked once, and the walked page equals the same chapter
served with no proxy on it. The value is projected now, and seven raw members
are enumerated in the authority inventory, each walked in its own scenario,
each beside a steady control at the accepted value and a steady control at the
walked-to value.

Identity is proved rather than argued. A harness that calls the projection
beside a consumer and compares ids proves two equal strings; `chapterWitness` is
a bounded seam handed the exact object each consumer is about to read, at the
moment it reads it, with the authoritative reference recorded where the
projection is made and identity decided by a `Map` keyed on the object. The
roster grows from six consumers to ten, is checked against every consumer name
the replay produced, and the tally is recorded as a consumer of its own rather
than as the length of the rows.

A request is owned by the row that asked for it. `fragmentText(row)` resolves
the address through the row, the model records the owning row and projection at
that moment, and a row no projection made resolves no address at all. Two rows
carrying one path are two owners; two projections carrying one path stay apart;
and in the late case A's recorded ownership is unchanged before and after B
settles on the same address.

Nested sources are normalized once under one rule. `sources["1"]` as an own
getter was invoked by the voices and editions walk and declined by every
fragment row, so one projection stated two incompatible things about one
edition — at the parent, an empty provenance line under an edition whose voice
the control offers. Four hostile shapes now produce one result at every sink,
an entry whose own rights, voice, author and language are getters has each
declined alike, and the invocation counts go from one, three, three, one and
one at the parent to zero here.

The member list is tested as an inventory. `Array.isArray` is true of a proxy
over a real array and the parent asks the length twice; add, remove, reorder,
phantom and tally are pinned independently, each beside a steady control, and
one `slice` reads the length once and each index once.

The authority graph is frozen as deep as it is trusted. Seventeen structures
are asserted frozen, thirteen values are actually assigned to and every
assignment throws and every value holds, the null-prototype claim is stated at
its exact scope, and the exported row, lead and blocked builders seal what they
return. At the parent the same probe reports the leads and blocked entries
unfrozen and their values moved.

The method count is stated as what it is. This lane adds 41 methods; replayed
against the exact reviewed parent the file fails 43 ways across 29 methods —
23 semantic adversarial, 2 source-audit and roster, 1 packaged-provenance, 2
exported-builder contract and 1 candidate-hash pin — and the ten independent
semantic closures are enumerated separately. Thirteen new methods pass at both
endpoints and are recorded as coverage and control rather than closure.

Fresh checks, measured at both endpoints: focused Catena 596 green at this head
and 555 at the parent; `catena check` 1,351/1/73 at both; full discovery 1,947
here and 1,906 there — the whole difference this lane's 41 new methods — with
14/13/11 over 27 identities here and 14/14/11 over 28 there, the head's set a
strict subset of the parent's and the one extra a signal-timing PDF-review
test an earlier independent run at the same parent did not produce, recorded
flaky rather than caused; none of them Catena; `make -k check` red on the same four inherited targets at both;
browser gate 2,290 at 1,836/226/228 over 171 pages and 19 routes, identical at
both and identical to V10–V13 including its 117/82/27 breakdown; promise ledger
39 tracked / 19 complete here and 38/19 at the parent; budgets unraised with
`catena.css` and `index.html` byte-identical and `catena.js` smaller at the
whole measure and identical at the stripped one, 12,972/13,000 and 7,546/8,800
against the parent's 12,974 and 7,546, so the page's headroom improves from 26
to 28 gzipped bytes. The unbudgeted model grows 36,679 to 39,724 whole and
8,873 to 9,396 stripped; disclosed, and its governance remains the budget
owner's. `src/web/data/` has zero changes and four stale bindings stay
fail-closed and unsigned.

All other blockers remain open and untouched, and E1 is not integrated. No
merge, re-signing, deployment or cutover is authorized.

### E1 Catena correction V13 — 2026-08-17

Answers the fresh independent review `728c3e3b3d0d6e899f0da33e06a08a116375896f`
on `review/catena-wave-1-e1-corrections-v12-independent` — **CHANGES
REQUIRED** at exact V12 head `d312786dd2b23926aa88e29ea15647dfcc7e7e6e`,
which independently verified evidence
`05306fcfe221c1b0456501463e02323047635607` and ZIP SHA-256
`fa43918166b2d708c7911e3604834499260884d8433b9cd665bd7fc0ccf40890` at
1,842,342 bytes across 81 members — with exactly its stated next action and
nothing else. Current `origin/main` is
`549bf0790503bd873dd8ce6ea0a64cc34f91271d`.

The review closed nothing it had passed: `requestSnapshot` is correct for one
invocation, the inherited prefix and the inherited refusal close locally, the
carried path is read once per projection, the fail-closed contamination policy
is accepted as a design, ordinary request behaviour and the malformed and
unestablished wording are exact, the 36-field late vector and its `0 -> 1`
release pass unchanged, P8 executes no archive code and rehashes equal before
and after, the ZIP's arithmetic and CRCs are correct, and ownership boundaries
hold. It found nine things.

One raw chapter was projected three times per render, and three projections
are three observations of it. `spineUnreadable` projected to decide
readability and discarded the rows, the tally projected to keep a length, and
`renderChain` projected a third time and kept the rows that reach every sink,
so a record answering differently between them rendered and requested from an
answer nothing had approved. The chapter is now normalized once —
each of its request-critical members read into a local exactly once, the rows
frozen where they are made, the editions gathered in a single walk, and
readability decided from that same walk — into a frozen null-prototype
projection held against the raw record, which every consumer reads and none
reaches past. `catena.js` changes by two lines and gets smaller.

Identity is observable rather than argued: the projection is exported, the
count of raw chapters normalized is exported, and every model entry point that
takes a chapter is asked which projection it resolved to before it answers, so
one identity across readability, tally, render, request, cache, body and
ownership is a comparison of recorded lists. A request is bound to the
projection that produced the row carrying its address.

Six of six are non-vacuous, each at a different sink. The review found
`v12-drifting-carried-path` vacuous — it consumed its pair inside the
readability projection, which issues no request, so it passed by never
reaching a sink. Each V13 scenario walks one chapter member between
projections and plants at the address only a later projection reaches, beside
a control holding that member at the walked-to value. At the parent the walked
carried path and the walked prefix each fetch and render a deeper composed
body; the walked member list renders and fetches off members readability never
approved; the walked editions put a forged rights claim on the reader's
provenance line; the walked refusals print a Rule 4 boundary the record never
stated; and the prewarmed walk misses a warm cache to fetch a second body. The
parent asks the walked member 3, 3, 5, 8, 4 and 3 times for one render; this
head asks each once. Replayed against the uncorrected parent the file fails
twenty-seven ways across thirteen methods. One committed assertion required the
wrong answer and is corrected with its reason, and the page-level descriptor
pin moves from three to one because three was the defect the review named.

The package can now show its own ownership, and can only claim authority after
it is verified. `journal-dump.py` enumerated scenarios from a hand-maintained
list that stopped at V11, so both packaged journals were byte-identical and
carried no V12 scenario; the roster is derived from the test file now, and each
row carries its sequence, scenario, request-time route, owning projection,
path, kind, step, outcome, cache disposition and body. The terminal
`authoritative` row was written before the manifest, so a later failure could
only write sibling markers while the sealed bytes kept the claim; an in-package
row may now claim at most `sealed`, and final authority is a structured sidecar
outside the archive naming the attempt, head, ZIP basename, size, digest, P8
result and post-P8 rehash, recomputed from the archive, binding one way. The
authority gate accepted six contradictions — a second authoritative state row,
a winner later discarded, multiline and uppercase contradictory prose, a wrong
package on the authoritative line, and prose that never named the winner — and
consumed neither archive, sidecar, P8 transcript, external ledger nor sibling
markers; all six are closed and run against the V12 package it refuses it.

Provenance, inventory and privacy are closed on the same terms. Four discarded
attempts and four set-aside battery cohorts were absent from every surviving
ledger while three package members claimed them present; ordinals were reused
after a ledger restart; every summary reason was empty; ten rows named log
roots the package lacked; and one attempt's embedded timestamp postdated the
evidence commit. The ledger identity is pinned to the lane, ordinals are
monotonic and never reused, a battery may be recorded set aside rather than
forced to `complete`, chronology is checked, and the complete ledger ships
beside the package. The 10/10 inventory computed every verdict from prose and
never stat'd a sibling, which is how the package omitted its own inventory log
while scoring ten of ten; it now resolves paths, recomputes digests, discovers
siblings including its own output, and counts members, logs, journals, tools
and rows mechanically. Twelve tracked outer-log lines exposed the workspace
path, account and tool anchor because the sanitizer's walk root was the
package, and a generic temp root and a dash-flattened workspace slug survived
inside the archive because one rule required a literal substring and another
could not match a flattened path; both gaps are closed and every outer sibling
is sanitized and re-scanned before it is committed. The executed-byte claim
covered four tools of fifteen and ran at P8, proving shipped against trusted
rather than executed against shipped; every invocation now digests its exact
bytes immediately before running, and the table distinguishes shipped and
executed from shipped and not executed, external system tool and reviewer-only
helper.

Fresh checks, measured at both endpoints: focused Catena 555 green at this head
and 544 at the parent; catena check 1,351/1/73; full discovery 1,906 here and 1,895 there with the identical inherited 14/13/11 and the same 27 identities at both, none of them Catena; `make -k check` red on the same four inherited targets at both; browser gate 2,290 at 1,836/226/228 over 171 pages and 19 routes, identical at both and identical to V12; promise
ledger 38 tracked / 19 complete; budgets unraised with `catena.css`
byte-identical at 7,629/8,000 and 2,676/2,700 and `catena.js` smaller at both
measures, 12,974/13,000 and 7,546/8,800 against the parent's 12,980 and 7,554.
The unbudgeted model grows 34,367 to 36,679 whole and 8,258 to 8,873 stripped;
disclosed, and its governance remains the budget owner's. `src/web/data/` has
zero changes and four stale bindings stay fail-closed and unsigned.

All other blockers remain open and untouched, and E1 is not integrated. No
merge, re-signing, deployment or cutover is authorized.

### E1 Catena correction V12 — 2026-08-17

Answers the fresh independent review `22b9bdad5e71920a103e3ec3bcf2f79bba50cebb`
on `review/catena-wave-1-e1-corrections-v11-independent` — **CHANGES
REQUIRED** at exact V11 head `0255b84996e1dc24da3ce75ac318c4f774b7957c`,
which independently verified evidence
`0ec8cae646f0e3e60c76635b88e51439c7146796` and ZIP SHA-256
`00e93c0f539a7928281912038f135b44666aebb84af4249cb906f54238cae257` — with
exactly its stated next action and nothing else. Current `origin/main` is
`549bf0790503bd873dd8ce6ea0a64cc34f91271d`.

The review closed nothing it had passed: ordinary accessor non-invocation,
own-property projection, the refused and unestablished wording, the cold,
present-valid and prewarmed controls, the 36-field late vector and its
timing, packaged request ownership, the read-only P8 with its identity
binding and rehash, the handoff contents, the screenshots, privacy, ZIP
metadata, the byte scan, ownership boundaries and the existing ceilings all
stand and are not reopened here. It accepted the fail-closed
prototype-pollution policy as a design and found V11 applied it to some of
the ways in and not to others.

Three inputs reached the production request sink that no record's own bytes
had stated, and they are one defect: the raw record was observed more than
once and the observations were allowed to disagree. An inherited valid
spine `text_prefix` was invisible to `ownData`, so it produced the claim
that means genuine absence — the one state that reopens the carried
fallback. `ownContract` asked `Object.prototype` about three names, so
`Object.prototype.text_refused = true` sat beside an own-valid claim and
the claim still composed its request. And the carried `text_path`
descriptor was read twice, so a drifting descriptor validated one address
and handed `fetch` another.

The request-critical state is now taken once. One descriptor read per
requested name, one question to the prototype, and a null-prototype record
of frozen own data back; five named fields decide whether a request
happens, where it goes and who owns the answer, and contamination in any of
them is neither absence nor an ordinary refusal but one conservative
malformed state. An accessor is declined without being called, so the
invocation count stays zero rather than becoming one. `catena.js` is
untouched, because the row it consumes was already a trusted projection.

The proof is planted and it fires at the parent. A model matrix drives the
review's exact reproductions, ten prototype and inherited combinations and
six drifting descriptors, asserting one ask per projection and zero
accessor invocations; six replay scenarios drive the same inputs through
`T.loadJSON`, the cache and the renderer with a body planted at every
address each defect could reach and a control beside each that really does
fetch. Replayed against the uncorrected parent the file fails twelve ways
across eleven methods, and the alternating descriptor fetches and renders
the second address outright. A static pin holds the request-critical names to the
three lines that snapshot them. Two committed assertions that required the
wrong answer are corrected with their reasons; both make a closure
stricter.

The package can now say which package it is. V11 wrote `authoritative` for
both a completed battery and a sealing package attempt, so the count could
never be one, and its ledger called the superseded attempt authoritative
while calling the shipped one unresolved. The two states are separated and
their transitions defined; only a package attempt may be authoritative and
exactly one may be. A coherence check runs before publication and fails on
a second authoritative attempt, on an authoritative attempt that is not
this package or this head, on an attempt both authoritative and discarded
or superseded, on an unresolved attempt called final, and on any
disagreement between ledger, outer log and prose. Every attempt writes into
its own log root, and validation rejects an unexplained empty claimed log,
a missing one, one claimed twice, one claimed by nobody, and one outside
its attempt's root.

Fresh checks, measured at both endpoints: focused Catena 544 green at this
head and 534 at the parent; catena check 1,351/1/73; full discovery 1,895
here and 1,885 there with the identical inherited 14/13/11 at both;
`make -k check` red on the same four inherited targets at both; browser gate
2,290 at 1,836/226/228 over 171 pages and 19 routes, identical at both and
identical to V11; promise ledger 37 tracked / 19 complete; budgets unraised
with both capped files byte-identical — `catena.css` 7,629/8,000 and
2,676/2,700, `catena.js` 12,980/13,000 and 7,554/8,800. The unbudgeted model grows 32,406 to 34,367 whole and 7,973 to
8,258 stripped; disclosed, and its governance remains the budget owner's.
`src/web/data/` has zero changes and four stale bindings stay fail-closed
and unsigned.

All other blockers remain open and untouched, and E1 is not integrated. No
merge, re-signing, deployment or cutover is authorized.

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
| E1 Catena production implementation | **CHANGES REQUIRED** at exact V16 `cc1f2fb8625f044558c26edd358b99cd7dcc7646`, reviewed independently on `review/catena-wave-1-e1-corrections-v16-independent`; **SEMANTIC CHANGES REQUIRED** and **EVIDENCE CHANGES REQUIRED** are separate. Evidence is `bfa913466c559ad410f252f4192fb3af953dd10b` / ZIP `bb473e7afbfa619182248a02fdc4db28b645792cba054e8be3cf660ff845d4fb`; `origin/main` remains `2778285849f2973ea89d1cfd5b2751ed4ae58e54`, unintegrated. | Atomic finalized cache publication, exact completion-envelope ownership, cross-owner rejection/rebinding, post-write journal truth, same-path/late/failure isolation, provenance and the twelve-consumer identity roster pass. Semantic closure fails because six raw chapter roots and nested members remain prototype/accessor-sensitive, and inherited `then` assimilation can substitute fragment text before finalization. Evidence closure fails on the false 401-row ledger digest for a 402-row sibling, post-hash P12 mutation and no final coherence/clean scan, unphased 32/31/25/23 histories, omitted authoritative fresh-clone replay, date-unpinned browser replay, permissive command/authority-language scanners, qualified tool-byte claims and local-only history support. Produce one bounded V17 semantic-and-evidence correction from exact V16, preserve the accepted publication/envelope/journal work, close inherited/accessor authority and thenable substitution, rebuild truthful final-state evidence, and return for fresh independent review. No merge, integration, re-signing, deployment or unrelated E1 work. |
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
| 2026-08-28 | E1 Catena V16 independent final publication / evidence review | Returned **SEMANTIC CHANGES REQUIRED**, **EVIDENCE CHANGES REQUIRED** and **CHANGES REQUIRED** for exact `cc1f2fb8625f044558c26edd358b99cd7dcc7646`. The V15-targeted cache-publication, owner-envelope, cross-owner, journal, same-path and identity work passes, but the unqualified observation invariant does not: plain reads admit inherited/accessor chapter roots and nested values into authority, and two inherited `then` observations can substitute a text document before finalization. Validation is endpoint-stable and ownership boundaries hold. Evidence fails on the first-401/full-402 ledger hash mismatch, P12 post-hash/post-scan append, phase-overstated coherence/cleanliness, silent 32/31/25/23 attempt views, omitted authoritative fresh-clone replay, unpinned browser date, command-classifier prose escapes, authority-scanner exception smuggling, qualified tool/executed-byte claims, and dependence on local-only raw history. Exact next action is one bounded V17 from V16 closing those semantic boundaries and rebuilding final-state evidence, then fresh review. | Review branch `review/catena-wave-1-e1-corrections-v16-independent`; reviewed evidence `bfa913466c559ad410f252f4192fb3af953dd10b`; ZIP SHA-256 `bb473e7afbfa619182248a02fdc4db28b645792cba054e8be3cf660ff845d4fb`; no merge, integration, re-signing or deployment. |
| 2026-08-27 | E1 Catena correction V16 | Answered the V15 independent review (**SEMANTIC CHANGES REQUIRED** and **EVIDENCE CHANGES REQUIRED**, **CHANGES REQUIRED** overall, at exact V15 head `b9202882badbbbc364f1dd3d9057d2710ee47552`, recorded at review commit `67247ecc39a6e5f6224c64ca3ab1af163ee023b1`) with exactly its stated next action. V15 owner-scoped pending transport correctly, but `fragmentTexts.set(path, asked)` ran INSIDE the fulfilment handler of the promise returned by `.then()` — before that handler returned — so a still-pending object was briefly path-visible and publication preceded the freeze; the eventual shared value was raw shallow-frozen parsed JSON with a mutable prototype that `M.textPayload` read later by ordinary prototype-sensitive lookup, so a frozen empty object could turn from unreadable to readable between readers; and `bodyAsked(row, content)` proved only that `row` occurred in `rowOwners`, so an actual B row accepted arbitrary A content, with the body journal written before the DOM write. `M.textPayload` is now the FINALIZER called at settlement: every field taken by own descriptor through `ownData` so nothing inherited is visible and no getter is invoked, sealed into a null-prototype, frozen, scalar-only record over the fixed key set `M.TEXT_SCHEMA`, with `M.NO_TEXT` the finished value for a row that resolves no address. The page publishes the FINAL VALUE and never a promise, so no path lookup returns unresolved or partial work at any instant, including reentrantly. A `WeakSet`-sealed completion envelope (`M.textCompleted` / `M.textFailed`) carries the exact `rowTransport` owner beside the finalized content through settlement, is per-caller by construction and never becomes the shared path-cache value; `M.bodyAsked(row, completed)` requires a model-sealed completion whose owner is the transport held for that very row and whose owner's projection made the row — three exact-object comparisons, no path, id or string — so arbitrary content beside a valid row fails closed; the new `M.bodyApplied(row, completed, wrote)` records the body only after the write is confirmed and binds owner, row, projection, path, the finalized content value and the post-write success state, leaving no entry at all for a failed or unconfirmed write; and a finished cached value is rebound to a later owner through that owner's own completion, so the cached value stays owner-independent and A's owner never crosses into B. Ten semantic closures are counted apart from the preserved V15 and V14 behaviour, which is re-run as REGRESSIONS rather than restated as new work. Thirteen evidence closures rebuild the package, and the V15 evidence facts are corrected truthfully — including one this lane first corrected on the review's authority and then corrected again after measuring. **The review's finding stands:** V15's prose claimed 30 example divergences while V15's own shipped transcripts (`logs/attempt-01/make-check-parent.log`, `logs/attempt-02/make-check-head.log`) each report 28 `DIFF` rows over 27 distinct commands and `28 diverged … 2 volatile line(s) declared`, so no artifact in the V15 package supports 30. **Its diagnosis does not:** "28 plus two declared volatile lines" is arithmetically impossible, because `volatile` is a static constant at `scripts/replay_examples.py:734` over the table at `:182-185` counting DECLARED LINES for two `tools/pdf-review` captures masked at `:405` that appear as `ok` and `absent`, never as `DIFF` rows, so they were never in the set they are supposed to be subtracted from. **The cause is BUILD STATE.** Measured three times independently at the exact parent in a clean checkout not under `/tmp`: cold `build/` gives **30** rows, the same command immediately again on the warm tree gives **28**, the entire delta being two captures of `tools/mass-ordinary check --out build/example-ordinary`, whose comparison directory a later capture in the same target writes. In V15's shipped transcripts both of those captures read `ok`, the warm signature — V15 quoted a cold figure while shipping a warm log, and the record never said which tree it measured. 28 is also reachable as distinct DIFF command strings (warm 28 rows over 27, cold 30 over 28), a row-versus-name conflation of the kind the same review rightly criticised in `compare-gate.py`. **V16 takes a rule rather than a number: a count is meaningless without the state it was taken in.** The battery records `build-state=COLD|WARM` at preflight and the V16 check pins no constant — it refuses the unsound shape, a figure the package's own transcript does not support, and a summary that disagrees with its own `DIFF` rows. Also corrected: **nine** retained V15 package attempts across three ledgers, eight resolved non-authoritative and one final authority, rather than five refusals and a sixth seal; seven of 24 `LITERAL` rows unable to expand and a parent replay overloading `$REPO`; six manufactured non-execution placeholders and two unlabelled tool-count sets for one lane; a `COMPLETE` verdict that rereads as `INCOMPLETE` after P11; a compare gate whose diagnostics collapse **2,290 assertion ROWS onto 17 diagnostic NAMES** although its whole-report verdict is sound — the ROW-versus-NAME conflation this lane found in four places in its own evidence and answers generally, so that wherever this evidence quotes a count it now says what is being counted; and a privacy claim that holds for the published archive and its ten named siblings but not for retained builder-local artifacts. Focused Catena **660/660** at the candidate against **615/615** at the exact V15 parent, with **39 distinct methods failing at the parent over 288 failure ROWS and zero errors** — 30 for a semantic reason, 6 because the mechanism is ABSENT and counted apart as absence-readings rather than advertised as discriminators, 2 source-text closures and 1 hash pin — and **48** new methods against **3** removed or renamed, **11** of the new ones passing at both endpoints as coverage and controls. Full discovery **2,011** at the candidate and **1,966** at the parent, **14 failures / 13 errors / 11 skips at both**, over **27 result ROWS spanning 22 distinct identities at both, the identity sets equal**; none of the 22 is Catena's. `make -k check` exits 2 on the same four inherited targets at both endpoints — `Makefile:554` `check-web-editions-current` (101 stale-edition lines), `:598` `check-release-bindings` (4 stale), `:803` `check-tool-registry` (8 undeclared-sibling findings, genuinely run because `tmt` is installed; **a box without `tmt` shows only three red targets, which is not a change**) and `:791` `check-examples` (30, cold). The browser gate is identically red at **2,290 assertion ROWS across 17 diagnostic NAMES — 1,836 pass / 226 fail / 228 skip over 171 pages, 19 routes and 9 states**, the 226 failing rows in exactly three names (`single-main-element` 117, `primary-controls-meet-target-size` 82, `skip-link-targets-existing-element` 27) on Chromium 151.0.7922.173, and whole-report identical under the named volatile exclusions. No ceiling is raised and the page is NOT smaller than the parent: `catena.js` goes 12,958 to **12,965**/13,000 whole-gzip and 7,724 to **7,835**/8,800 stripped, seven gzipped bytes ABOVE V15 with thirty-five under an unraised ceiling, the first version since V4 that cannot report the page smaller than its predecessor and it says so; `catena.css` and `index.html` are byte-identical; the three body sentences, the presentation decision and the acknowledgement paragraph relocated to the uncapped model to pay the forty-two-byte V15 headroom are disclosed; and `catena-model.js` has reached **44,247** whole-gzip and **10,344** stripped against 41,077 and 9,536 at V15, digest `64a75834abd8f9efa25ae52c76b904a3437ab96a9508ba82309211215d44c3a3`, with thirty-five bytes of page headroom recorded as a limitation — not enough for the next correction of any size — and a governing model ceiling still open and separately owned. The post-write confirmation reads back the body alone, not the acknowledgement block or the apparatus paragraphs beside it — now a pinned assertion rather than prose, since a silent non-take still draws the apparatus, a throw draws none of it, and both leave the acknowledgement block standing because it is written before the words. `M.rowTransport` is now consulted unconditionally, so a row that resolves no address produces one more transport witness than V15's did. **A refused body application now leaves no journal entry at all**: V15's `bodyAsked` witnessed every attempt including refusals, while V16 records only confirmed applications, so the negative cases are still proved by a committed direct assertion and an unchanged page but the page-level journal row V15 had is gone — a deliberate consequence of taking the record after the write, not an oversight. **The retry flag is deliberately not reset in the write's `catch`**, because a throw after the body had landed would leave the body on the page, no entry, and an invited second application from the memoised completion; `asked = false` occurs only in the transport-failure arm, since a network failure is retryable and a failed DOM write is not, and the disclosed consequence is that a silent non-take leaves the fragment showing its previous state with no reader retry. **Two fixes were identified, costed and deliberately not made** because they exceed the unraised ceiling: testing the cache hit with `fragmentTexts.has(path)` rather than for truthiness (37 gzipped bytes against 35 of headroom, safe today because a sealed value is always a non-null object) and writing the words before the class (about 60 gzipped bytes, since the reorder breaks a repeated pattern gzip was compressing, and no throw is reachable there). And the completion envelope's two halves cannot be supplied **by the data**, which is the exact claim — in-realm code holding a recorder installed through the exported `chapterWitness` can mint valid halves from a real row in five lines, so this is not a security boundary and no unqualified impossibility is asserted. All of these are disclosed rather than left to be found. All other blockers recorded open and untouched. | Branch `impl/catena-wave-1-e1-corrections-v16`; parent `b9202882badbbbc364f1dd3d9057d2710ee47552`; review addressed `67247ecc39a6e5f6224c64ca3ab1af163ee023b1`; handoff archived on `evidence/catena-e1-corrections-v16-handoff`; awaiting fresh independent review. No merge, re-signing, deployment, or outside-owner work occurred. |
| 2026-08-26 | E1 Catena correction V15 | Answered the V14 independent review (**CHANGES REQUIRED** at `69f2575421ba976271c936b1abd4b39dbe8b98fd`, recorded at review commit `0d11766ec232b2b4e46a7d1b0ada56ef22370004`) with exactly its stated next action. V14 resolved a text address THROUGH the projected row and then handed the resolved string to a module-scope map keyed on the path alone that held the unresolved PROMISE, so a second row carrying that address did not ask — it joined the first row's request and was handed the answer that request was made for. Replayed at the exact parent, owner A is held and owner B shows `Loading…`; after A releases, B shows `PLANTED BODY A`, A's document, under B's row, on B's route, in B's projection — and the V14 test that was green over that case asserted one request for the address and B rendering A's body, so its oracle required the leak. A path map now holds only a settled answer and receives the promise from inside that promise's own settle handler; work in flight is held against `M.rowTransport(row)`, one frozen owner object per projected row carrying the row, its projection and the address it asks; `M.bodyAsked(row, content)` is asked AT the body application and records the projection, the row and the value written, so the roster reaches the step that writes the page and a row no projection made applies nothing; the substitute record for an unreadable spine is made once per name, so walking away from an unreadable chapter and back no longer mints a second authority over it; and a request released late may not displace an answer another row already has. The decisive case parks only the FIRST ask of a shared address and answers it two different documents in turn, so B rendering its own body and B rendering A's are distinguishable: B settles and renders `PLANTED BODY B` while A is held, never renders `PLANTED BODY A`, and A's late release moves exactly one journal row against a thirty-six-field terminal vector pinned value by value beforehand. The promised nested EDITION accessor case is asked directly and gives one coherent outcome across edition, printing, provenance line, rights, voices and readable state — a proof gap closed, not a production defect. Observations are reported by kind: zero value reads that would run an own accessor, zero `in` tests, three `getOwnPropertyDescriptor` observations per source key, two per stated shared field and one per absent one, one key enumeration, nothing further on a second render, with `Object.hasOwn` counted under descriptors because it is `[[GetOwnProperty]]`. After thirteen attempted mutations the chapter is drawn again from the same projection and its bodies applied again, and thirty-two rendered fields and the request journal are unchanged. Focused Catena 615 green, up from 596; fourteen methods fail at the exact parent — eleven new, plus the corrected oracle, the roster audit and the model hash pin, the last two counted apart — and eight further new methods pass at both endpoints as coverage and controls. Full discovery 1,966 at the candidate and 1,947 at the parent, 14/13/11 at both over the SAME 27 identities — **corrected in place on 2026-08-27 by the V16 lane: read 27 result ROWS over 22 distinct `module.Class.method` identities**, since two methods emit multiple `subTest` rows (`test_every_verb_shows_at_least_two_real_invocations` five, `test_shell_smoke_tests_pass` two); the substantive claim survives, the sets ARE equal, and only the label on the number was wrong. **A second precondition belongs beside the figure:** the V15 review's fresh replay reached 15 failures, the extra identity being the `pdf-review.test` tool-registry smoke test, because `tools/pdf-review:486` allows any output under `Path("/tmp").resolve()` for a non-managed worker, so **from a checkout under `/tmp` the asserted refusal never happens**; these clones are not under `/tmp`, so 14/13/11 is what they measure, and the reviewer measured something real in a place where it is true. `make -k check` exits 2 on the same four inherited targets at both, with **28** example divergences at both — **corrected in place on 2026-08-27 by the V16 lane, twice.** This row and the V15 lane record had said `30 example divergences`; the V15 review found that this lane's own shipped transcripts report 28 `DIFF` rows over 27 distinct commands and `28 diverged … 2 volatile line(s) declared`, and **it was right — no artifact in this package supports 30**, so the figure above is corrected to 28 and that correction stands. V16 first also adopted the review's explanation, rewriting this row to read 28 + 2, and **that part was wrong and is withdrawn**: `volatile` is a static constant at `scripts/replay_examples.py:734` over the table at `:182-185`, counting declared LINES for two `tools/pdf-review` captures masked at `:405` that appear as `ok` and `absent`, never as `DIFF` rows, so they were never in the set they are supposed to be subtracted from. **The cause is BUILD STATE:** measured three times independently at the exact parent in a clean checkout not under `/tmp`, a cold `build/` gives 30 and an immediately repeated warm run gives 28, the whole delta being two captures of `tools/mass-ordinary check --out build/example-ordinary`, whose comparison directory a later capture in the same target writes. Both of those captures read `ok` in this lane's shipped transcripts, the warm signature — this record quoted a cold figure while shipping a warm log, and never said which tree it measured. **`check-examples` must therefore be run exactly once per fresh clone, and no record may state the figure without stating the build state beside it.** The browser gate is byte-identical under the named volatile exclusions at **2,290 assertion ROWS across 17 diagnostic NAMES**. Budgets unraised: `catena.js` is smaller than the parent at 12,958/13,000 whole and 7,724/8,800 stripped, `catena.css` and `index.html` byte-identical, and the three paragraphs relocated to the uncapped model to pay for the correction are disclosed. All other blockers recorded open and untouched. | Branch `impl/catena-wave-1-e1-corrections-v15`; parent `69f2575421ba976271c936b1abd4b39dbe8b98fd`; review addressed `0d11766ec232b2b4e46a7d1b0ada56ef22370004`; awaiting fresh independent review. No merge, re-signing, deployment, or outside-owner work occurred. |
| 2026-08-20 | E1 Catena correction V14 | Answered the V13 independent review (**CHANGES REQUIRED** at `6cc85e1a1`) with exactly its stated next action. **That review has no published ref**: `origin` carries no `review/catena-wave-1-e1-corrections-v13-independent` and the branch exists only in a local reviewer checkout at the reviewed head with no review commit, so no review SHA is recorded and the gap is stated rather than filled. `unfetched` was the one request-critical chapter member the projection read and did not carry, so the page read the raw record a second time for the string it prints; a record answering `undefined` while readability was decided and a forged string afterwards replaced an accepted chapter with a manufactured unavailable state, taking its rows, its recorded refusal and its tally and printing the payload's own words to the reader. The value is projected now and the member is asked once, against twice at the parent. `chapterWitness` is a bounded seam handed the exact object each consumer is about to read, so identity is `===` on an object rather than equality on an id; the roster grows from six consumers to ten, is checked against every name the replay produced, and the tally is a consumer of its own rather than the length of the rows. `fragmentText(row)` resolves the address through the row and the model records the owning row and projection at that moment, so two rows carrying one path are two owners, two projections carrying one path stay apart, and a genuinely-late completion belongs to the row that started it; a row no projection made resolves no address at all. Nested `sources["1"]` as an own getter was invoked for voices and editions and declined for fragment provenance out of one projection — an empty provenance line under an edition whose voice the control offers — and every entry and shared field is own data now, with invocation counts falling from 1, 3, 3, 1 and 1 at the parent to zero. The member list is tested as an inventory: `Array.isArray` is true of a proxy over a real array and the parent asks the length twice, so add, remove, reorder, phantom and tally are pinned independently, each beside a steady control. Seventeen trusted structures are asserted frozen and thirteen values actually assigned to, every assignment throwing and every value holding; the null-prototype claim is stated at its exact scope; and the exported row, lead and blocked builders seal what they return. Focused Catena 596 green, up from 555. Replayed against the exact reviewed parent the file fails 43 ways across 29 methods — 23 semantic adversarial, 2 source-audit and roster, 1 packaged-provenance, 2 exported-builder contract and 1 candidate-hash pin — and the ten independent semantic closures are enumerated separately rather than counted off the method total; thirteen further new methods pass at both endpoints and are recorded as coverage and control. Budgets unraised with `catena.css` byte-identical and `catena.js` smaller than the parent at 12,972/13,000 whole and identical at 7,546/8,800 stripped; the unbudgeted model's growth is disclosed. All other blockers recorded open and untouched. | Branch `impl/catena-wave-1-e1-corrections-v14`; parent `6cc85e1a1dea317a48c0bfcfd6f774201ea3a6c3`; the review addressed has no published commit; awaiting fresh independent review. No merge, re-signing, deployment, or outside-owner work occurred. |
| 2026-08-17 | E1 Catena correction V13 | Answered independent review `728c3e3b3` (**CHANGES REQUIRED** at `d312786dd`) with exactly its stated next action and nothing else. V12 took each record's request-critical state once inside a projection and then ran that projection three times over one raw chapter: `spineUnreadable` projected to decide readability and threw the rows away, the tally projected to keep a length, and `renderChain` projected a third time and kept the rows that reach request, cache, body and ownership — so a record answering one way while readability was decided and another while the render was built rendered, requested, cached and attributed from an answer nothing had approved. The chapter is normalized ONCE now, each request-critical member read into a local exactly once, the rows frozen where they are made, the editions gathered in one walk and readability decided from that same walk, into a frozen null-prototype projection held against the raw record that every consumer reads and none reaches past; `catena.js` changes by two lines and gets smaller. Identity is observable rather than argued, and a request is bound to the projection that produced the row carrying its address. Six of six planted scenarios are non-vacuous, each at a different sink: at the parent the walked carried path and the walked prefix each fetch and render a deeper composed body, the walked member list renders and fetches off members readability never approved, the walked editions put a forged rights claim on the reader's provenance line, the walked refusals print a Rule 4 boundary the record never stated, and the prewarmed walk misses a warm cache to fetch a second body; the parent asks the walked member 3, 3, 5, 8, 4 and 3 times for one render and this head asks each once. Replayed against the uncorrected parent the file fails twenty-seven ways across thirteen methods; one committed assertion required the wrong answer and is corrected with its reason. On the package: the journal roster is derived from the test file rather than hand-maintained, an in-package row may claim at most `sealed` and final authority is a post-P8 sidecar bound to the ZIP's basename, size, digest and P8 result, the authority gate's six accepted contradictions are closed and it now consumes the archive, sidecar, P8 transcript, external ledger and sibling markers, ordinals are monotonic and never reused with a reason on every non-authoritative terminal state, the inventory is verified substantively rather than lexically, every outer sibling is sanitized before it is committed, and every tool invocation digests its exact bytes immediately before it runs. Measured at both endpoints: focused Catena 555 green here and 544 at the parent; catena check 1,351/1/73; full discovery 1,906 here and 1,895 there with the identical inherited 14/13/11 and the same 27 identities at both; `make -k check` red on the same four inherited targets at both; browser gate 2,290 at 1,836/226/228, identical at both; promise ledger 38 tracked / 19 complete; budgets unraised with `catena.css` byte-identical and `catena.js` smaller at both measures; the unbudgeted model's growth disclosed. All other blockers recorded open and untouched. | Branch `impl/catena-wave-1-e1-corrections-v13`; parent `d312786dd2b23926aa88e29ea15647dfcc7e7e6e`; review addressed `728c3e3b3d0d6e899f0da33e06a08a116375896f`; awaiting fresh independent review. No merge, re-signing, deployment, or outside-owner work occurred. |
| 2026-08-17 | E1 Catena correction V12 | Answered independent review `22b9bdad5` (**CHANGES REQUIRED** at `0255b8499`) with exactly its stated next action and nothing else. Three inputs reached the production request sink that no record's own bytes had stated, and they are one defect: the raw record was observed more than once and the observations were allowed to disagree. An inherited valid spine `text_prefix` was invisible to `ownData` and so produced the claim that means genuine absence, the one state that reopens the carried fallback; `ownContract` asked `Object.prototype` about three names, so an inherited refusal marker left an own-valid claim composing its request; and the carried `text_path` descriptor was read twice, so the address handed to `fetch` had passed no test. The request-critical state is now taken once — one descriptor read per requested name, one question to the prototype, a null-prototype record of frozen own data — and contamination in any of the five named fields is neither absence nor an ordinary refusal but one conservative malformed state; an accessor is declined without being called, so the invocation count stays zero rather than becoming one. `catena.js` is untouched. A model matrix drives the review's exact reproductions, ten prototype and inherited combinations and six drifting descriptors; six replay scenarios drive the same inputs through `T.loadJSON`, the cache and the renderer with a body planted at every reachable address and a control beside each that really does fetch. Replayed against the uncorrected parent the file fails twelve ways across eleven methods, and the alternating descriptor fetches and renders the second address outright. A static pin holds the request-critical names to the three lines that snapshot them, and two committed assertions that required the wrong answer are corrected with their reasons. On the package: a completed battery and a sealing package attempt were both written authoritative, so the count could never be one; the states are separated, only a package attempt may be authoritative, exactly one may be, every attempt writes into its own log root, and a coherence check run before publication fails on a second authoritative attempt, a wrong package or head, an attempt both authoritative and superseded, an unresolved attempt called final, an unexplained empty or reused or unclaimed log, and any ledger/outer-log/prose disagreement. Measured at both endpoints: focused Catena 544 green here and 534 at the parent; catena check 1,351/1/73; full discovery 1,895 here and 1,885 there with the identical inherited 14/13/11 at both; `make -k check` red on the same four inherited targets at both; browser gate 2,290 at 1,836/226/228, identical at both; promise ledger 37 tracked / 19 complete; budgets unraised with both capped files byte-identical; the unbudgeted model's growth disclosed. All other blockers recorded open and untouched. | Branch `impl/catena-wave-1-e1-corrections-v12`; parent `0255b84996e1dc24da3ce75ac318c4f774b7957c`; review addressed `22b9bdad5e71920a103e3ec3bcf2f79bba50cebb`; awaiting fresh independent review. No merge, re-signing, deployment, or outside-owner work occurred. |
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
