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

### E1 Catena production independent review — 2026-08-10

This is a cold review of the production candidate, not an implementation or
integration pass. The exact reviewed head is
`efd7559a93310442753383bfeec80529f4693288`; its declared focused base is
`f6c3b75b5e37da9b6da9c6966ef5270abd4ed76e`. The current-main comparison is
`9b9ff74a77d1bcd7d454d2a7fc448b8a6c8f1fd4`, with merge base
`b87dfc744ec86ec54bb6f5d39154df85f36dc8e4`. The branch is 12 commits ahead
of and 27 commits behind that current main, but E1 itself is the three-commit,
seven-path range `f6c3b75b5..efd7559a9`.

The reviewed transport is
`20260809T030856Z-catena-wave-1-implementation/` and its sibling ZIP. The ZIP
has SHA-256
`e906ffcf4a056e00ba4596059d0eef6255fedd320f2fb1ecf96e43f3c29c72c8`.
Independent inspection found one safe archive root and 35 of 35 byte-identical
members between the directory and ZIP. `changes.patch` is byte-identical to
the focused Git diff, 97,910 bytes, SHA-256
`0fbd209ffb43f48b358a39a84de2522f4e6730dd05aaaa858b68f29deedede52`.
The transport is nevertheless protocol-incomplete: it has neither of the
required core files `REVIEW_REQUEST.md` and `checks.txt`, and no `sources.md`
despite the source, rights, and data-architecture questions in scope. It also
supplies no separate manifest file or ZIP digest, and its own screenshot index
says the captures are not visual acceptance. The independent hashes above
qualify the bytes inspected; they do not manufacture the missing protocol
evidence.

#### Validation

All commands below ran in a fresh full checkout at the exact candidate, not a
worktree or synthetic merge.

| Check | Exact result | Classification |
| --- | --- | --- |
| `git diff --check f6c3b75b5..efd7559a9` | exit 0 | Focused E1 patch is mechanically clean. |
| `test_catena_wave_1.py` | 36 passed | Green, but several assertions bless weaker or synthetic states identified below. |
| `test_catena.py` | 52 passed | No regression detected by the existing Catena model/generator suite. |
| `test_browser_url_contract.py` | 46 passed | Published key vocabulary is retained; invalid values and history restoration are not covered. |
| `test_browser_static.py` | 6 passed | Landmark count passes on the candidate's inherited shell base. |
| `test_browser_collisions.py` | 11 passed | No new selector collision detected. |
| `test_corpus_browser_gate.py` | 17 passed, 1 slow live-browser case skipped by its opt-in contract | Gate structure passes. |
| `tools/tpt check-promised-deliverables` | exit 0; 24 tracked, 18 complete | Candidate ledger is valid but contains no E1 implementation promise. |
| `make check-catena` | exit 0; 1,351 fragments, one held book, 73-book canon | Current generated data is internally valid under its present checks. |
| `make check-release-bindings` | exit 0; zero stale | The listed bindings match the candidate tree; the Catena-data binding gap below remains. |
| `make public-site` | exit 0 | Exact candidate artifact built. |
| `public-alpha verify --deployment-target github-pages` | exit 0 | Exact built artifact verifies under the current verifier. |
| Live Chromium artifact gate | exit 1; 2,290 assertions: 1,953 passed, 109 failed, 228 skipped | Exactly reproduces the candidate handoff. Failures are 82 target-size and 27 skip-link/modal findings inherited from the shell/protected routes; no E1 delta from its recorded baseline. |
| `make check` | exit 2 at `check-tool-registry` | Eight undeclared sibling-tool dependencies, unchanged between candidate and main. |
| `make -k check` | exit 2 on candidate and current main | Same two failing targets at both endpoints: the eight registry findings and `check-examples` with 201 captures, 192 replayed, 29 divergent, 35 known stale, 6 never run, and 3 unrunnable. Only the expected ledger count text differs: candidate 24/18, main 27/19. No E1-specific failure identity was found. |

The fresh Chromium run also generated and independently inspected the Catena
default at 1440x900, 1024x768, 768x1024, 393x852, 320x852, 200-percent text,
the gate's nominal 400-percent scale, forced colors, and reduced motion. The
candidate package's contact sheet and representative original images were
inspected for Genesis 1 ordinary/long/multiple-type content, Genesis 2
cross-chapter extent, Genesis 42 sparse content, Exodus 3 acquisition-only,
Psalm refusal and paragraph-data absence, open-fragment provenance, and its
claimed translation-unavailable state. The latter actually depicts Genesis 1
with 14 held English fragments, not the real Genesis 10 selected-voice-empty
state. Several narrow captures never scroll to the state named by the file;
the 320px open-fragment and default files are byte-identical.

A separate real-CDP no-JavaScript rendering at 393x852 showed permanent
`Loading...`, three disabled loading selects, a disabled `Everything held`
select, `aria-busy="true"`, and `Loading the chapter...`. A seven-page browser
print was generated; page one still prints the chapter/commentary control
disclosure. No admissible held-but-unrenderable row exists in the 561 current
spines. No real assistive-technology session was supplied or performed, so it
is not claimed.

#### Required findings

1. **Critical — the Scripture anchor can cite the wrong Psalm.** Catena spines
   are Vulgate-numbered, but `catena.js` passes their chapter integer unchanged
   to a selected Hebrew-numbered Bible. Vulgate Psalm 14 is therefore displayed
   beside KJV Psalm 14 even though the tracked concordance maps it to Hebrew
   Psalm 15. The refusal generator is also keyed from the Hebrew number as if it
   were canonical. This violates Catena Rules 3 and 4 and E0's central Scripture
   anchor. The smallest correction is one generator/shared-renderer-owned,
   tested Vulgate-to-selected-edition projection that either resolves the exact
   chapter or visibly refuses; no same-number fallback. Re-review must exercise
   Psalm 13, 14, and 100 across Vulgate, Douay, and KJV and compare actual verse
   text and addresses.

2. **High — E1 breaks the chronological chain it claims to preserve.** The
   generator correctly orders held fragments by text date, but
   `catena.js:675-731` then coalesces every work by author. Genesis 1 becomes
   Augustine 401, Augustine 417, Severian 401 under one Augustine heading
   labelled 401. The smallest correction is to preserve fragment chronology
   and coalesce only a contiguous, semantically identical run, never a later
   work across another author/date. Re-review needs a real 401 Augustine / 401
   Severian / 417 Augustine assertion and rendered chain.

3. **High — acquisition and held truth are contradicted on real chapters.**
   The generator emits L1 leads without reconciling held works and strips the
   confidence that the Catena guidance assigns to the acquisition list. Exact
   author/title overlaps occur in 89 rows across 46 chapters; Genesis 1 lists
   six held works again as "not yet acquired." E1 then says no text of any lead
   is held. The smallest correction is source/generator-owned identity
   reconciliation (or an explicitly truthful partial-acquisition state),
   preservation of applicable confidence, and copy that asserts no more than
   the data proves. Re-review needs a corpus-wide invariant plus Genesis 1 and
   Genesis 42 rendered evidence.

4. **High — licensed source obligations disappear at the point of use.** Six
   Severian/PTA fragments are held under CC BY-SA 4.0 with recorded Voicu,
   von Stockhausen, BBAW, attribution, and ShareAlike terms. The generated
   Catena source record reduces that to `rights: "licensed"`, and E1 prints
   only that word. The smallest correction is to project and render the actual
   licence identifier/link and required attribution in the nearest useful
   source apparatus reachable from each licensed excerpt. Re-review must trace
   one real Severian passage from Artifact and Edition records through the
   generated payload to the rendered acknowledgement.

5. **High — cited state does not fail closed.** Invalid `book`, `chapter`, or
   `bible` hashes silently select a default on cold load; invalid hash changes
   may leave stale content. The E1 `voice` fix preserves valid held and absent
   voices, but malformed values can render a blank "none here" option and
   broken prose. Shared history also suppresses Forward after Back because its
   last-written hash remains stale. The smallest correction is typed validation
   that retains and visibly identifies every invalid cited value with recovery,
   plus deterministic Back/Forward state restoration. Re-review needs cold and
   hashchange tests for every key, malformed voice, and Back/Forward sequences.

6. **High — no-JavaScript and print remain false loading/interactive states.**
   With scripts disabled the built route never owns useful Catena content or an
   honest Catena browse entry; E1's new test expressly blesses the permanent
   loading state. On a slow narrow load the initially open controls also close
   only after three awaited requests, creating avoidable shift. Browser print
   retains the interactive controls. The smallest correction is a useful static
   chapter/browse entry or explicit no-JavaScript recovery, synchronous narrow
   enhancement before the first await, and scoped print rules that hide
   interaction chrome while identifying browser print as non-canonical.
   Re-review needs real no-script desktop/mobile captures, throttled startup
   evidence, and an inspected print PDF.

7. **High — forced colors collapses a protected epistemic distinction.** Every
   paragraph reserves a transparent 2px border; forced-colors mode materializes
   it as `CanvasText`, so an ordinary or no-paragraph-data passage receives the
   same black rule as a projected boundary. The smallest correction is a
   `Canvas` base border and `CanvasText` only for `.projected`, with focused
   normal/forced-color comparisons of projected, printed, and absent paragraph
   data.

8. **High — several reader-facing counts and states are false.** A selected
   empty voice can headline "Nothing held here" while 71 original-language
   fragments are held; partial-public-domain absences are counted under "no
   English this project may publish"; paragraph headings count breaks rather
   than paragraphs; a single hidden author can leave zero visible fragments
   with no filter control to restore him; and an expected Catena-spine 404 is
   treated as genuine emptiness. Correct each claim from the typed state rather
   than from a filtered count, distinguish integrity errors from absence, and
   test the real Genesis 10, Genesis 42, and paragraph fixtures. The footer's
   E1-introduced statement that everything begins closed must also agree with
   the open chapter and first author.

9. **High — release approval does not bind the public Catena corpus.** The
   release source inventory binds Catena HTML/CSS/JavaScript, but not the
   published `src/web/data/structure/catena/**` spines/payloads or a deterministic
   approved root over them. Artifact/current-source byte equality is not an
   approval binding. Add a release-owned deterministic Catena-data root or exact
   file bindings and prove a fragment or attribution change moves the approved
   snapshot.

10. **High ownership/integration prerequisite — the composed production shell
    remains narrower and less accessible than accepted E0.** E1 did not edit
    shared shell assets or core, but it did edit the common artifact gate and
    both global release records; those supporting changes require their owners'
    disposition and the release records must be regenerated, not transplanted.
    The inherited 60rem wrapper compresses E0's 74rem wide instrument, truncates
    the selected Bible label, and leaves the published skip link targeting a
    non-focusable wrapper. Arrow shortcuts also fire from links and summaries
    and can detach focus during rerender. These are B0/shared-owner corrections,
    not permission for E1 to broaden further. Re-review must use the integrated
    shell at 1440, 1025, 1024, keyboard skip, arrow-on-interactive, and
    post-render focus states.

11. **Medium — the evidence and performance waiver are incomplete.** The
    handoff omits required core and applicable source records, 1024/768 focused state
    captures, real Genesis 10 absence, meaningful 400-percent reflow, keyboard,
    reduced-motion, no-JavaScript, print, and assistive-technology evidence.
    Its CSS and JavaScript gzip-9 sizes, 8,287 and 13,229 bytes, exceed the
    recorded 8,000/13,000 ceilings; the candidate changed tests to 8,600/13,400
    without an accepted waiver. Meet the original ceilings or record an explicit
    owner-approved replacement, then provide one protocol-complete immutable
    package for the corrected exact head.

#### What passes and what remains out of scope

The production work is recognizably faithful to E0's design direction:
Scripture is first and adjacent to commentary at wide size; narrow layouts use
one reading order; held fragments, leads, refusals, absence notices, paragraph
qualification, and cross-chapter extent remain separately structured; first
author/open-fragment lazy loading and the Source Library passage link work; the
local reduced-motion rules are sound; 320px default has no measured document
overflow; and the route looks like Triptych without importing protected
Liturgy styling.

The route-owned portion of the focused E1 diff changes no protected Liturgy
file, PDF, publication prose, Catena model, generated data, generator, shared
browser core, Search, relationships, or canonical route. Its supporting
shared-gate edit only adds `voice` to the existing Catena hash sample, and the
two derived release edits do not authorize E1 to own those global surfaces. A
synthetic held-unrenderable unit fixture may test defensive rendering only if
it remains explicitly synthetic; it is not real-data acceptance evidence. The
misleading `position: static` comments that call the Scripture column "pinned"
or "never scrolls away" should be corrected, but sticky behavior was not part
of accepted E0 and is not demanded here.

#### Integration risk and disposition

**Disposition: CHANGES REQUIRED.** The candidate has substantive product,
data-integrity, rights, URL, resilience, and accessibility defects; this is not
an `ACCEPT WITH BOUNDED INTEGRATION CONDITIONS` case. It remains off main. This
review does not merge, deploy, cut over, or begin fixes.

The Catena HTML/CSS/JavaScript, focused test, and single-fixture gate patch apply
mechanically to current main, but that does not make the result acceptable.
The full branch must never be merged wholesale: nine pre-E1 shell-plumbing
commits alter the Makefile, layout, generator, guidance, and shared tests under
a separate owner. The full candidate/main overlap is the older
`guidance/corpus-browser-implementation.md` plus both derived release records.
Keep current-main guidance. Regenerate `release/public-alpha.json` and
`release/rights/public-alpha-2026-07-15.md` from the corrected reconciled tree;
never choose either conflicting side verbatim. Consume shell/generator work
only under its own B0 and source-data gates, then rerun failure-set comparisons
and review the exact reconciled artifact.

**One E1 next action:** dispatch one new bounded Claude route-owner correction
agent from current main, use `efd7559a93310442753383bfeec80529f4693288` only
as the reviewed reference for reconstructing the route-owned Catena patch,
explicitly exclude the common gate, release records, Catena source/generator,
and B0 paths pending their separately authorized owners, and produce the route
patch and prerequisite contract for a protocol-complete reconciled handoff and
fresh independent review.

### E1 Catena correction independent review — 2026-08-11

This is the required cold review of that bounded correction, not a fix,
integration, release, or deployment pass. The exact reviewed identity is:

- branch `impl/catena-wave-1-e1-corrections`;
- current-main base and merge base
  `9b9ff74a77d1bcd7d454d2a7fc448b8a6c8f1fd4`;
- route/test commit `67191afd1d6281006e5cb947596452481c0d9692`;
- packaged head `dfc636665df26563138ff893bd2a9f9afc7d80c0`;
- prior review `254c4446ff693e3015364e005624d62fbdf8e35b`;
  and
- immutable package `20260811T134130Z-catena-e1-corrections/` and sibling ZIP,
  whose independently verified ZIP SHA-256 is
  `8013074d9a77ae54208399207e10d58aaacb7e1b6efab6e820bbeaaa9fd83b05`.

The live remote branch and `origin/main` still resolved to those exact heads
during review. The two-commit base-to-head range changes exactly eight paths:
the three Catena route assets, the new focused Catena test, and the four
durable authority records. `catena-model.js`, the generator, generated Catena
data, common gate, shared browser core, layout, site CSS, release records,
protected Liturgy, and PDFs are byte-unchanged. The review itself changes only
the four authority records named by the review protocol.

#### Package and validation

The package directory and ZIP are mechanically sound: one archive root, 35
regular files, 34 manifest-covered payload files, exact directory/archive
agreement, a byte-identical base-to-head patch, and the required ZIP digest.
That integrity does not make the handoff protocol-complete. The screenshot
index names `67191afd1` rather than the packaged head, cites an absent capture
script and absent stderr log, and includes machine-private absolute paths and
loopback ports despite the handoff's contrary claim. The index and route-state
matrix call the 17-page print PDF eight pages. They also say print has no
navigation even though footer navigation and ten loopback annotations remain.
No before/after pairs, focused 1024/768 captures, meaningful 400-percent
artifact, real assistive-technology session, full-system-palette forced-colors
capture, or throttled-startup evidence is supplied. These are evidence defects,
not permission to alter the immutable pair; a replacement must be a new package.

Independent commands ran in fresh full checkouts at the exact revisions:

| Check | Exact result | Review classification |
| --- | --- | --- |
| `git diff --check 9b9ff74a7..dfc636665` | exit 0 | Mechanically clean. |
| `test_catena_wave_1.py` | 99 passed | Green but incomplete; it does not cover the adversarial URL, load-race, blocked/empty, print-identity, and real-payload cases below. |
| `test_catena.py` | 52 passed | Existing Catena model/generator behavior unchanged. |
| `test_browser_url_contract.py` | 47 passed | Common key vocabulary remains intact; it does not close the Catena-local parser defects. |
| `test_browser_static.py` | 5 passed | Static checks pass while the inherited published nested-`main` defect remains explicitly allowed. |
| `test_browser_collisions.py` | 11 passed | No selector collision regression. |
| `test_corpus_browser_gate.py` | 17 passed, 1 intentional live-browser skip | Gate unit contract passes. |
| `scripts/_catena.py check` | exit 0; 1,351 fragments, one held book, 73-book canon | Current generated corpus is internally valid under its present schema. |
| `tools/tpt check-promised-deliverables` at packaged head | exit 0; 28 tracked, 19 complete | The correction promise is valid but incomplete. |
| `make -k check` at packaged head | exit 2; three failing targets | `check-release-bindings` finds the three stale Catena route bindings; `check-tool-registry` finds eight inherited sibling dependencies; `check-examples` reports 201 captured, 192 replayed, 30 divergent, 35 known stale, 6 never run, 3 unrunnable, and 2 volatile lines. The handoff's statement that head has the same two failing targets as base is false. |
| Browser artifact gate, base and head | each exit 1; 2,290 assertions: 1,836 passed, 226 failed, 228 skipped | Failure identity/status sets are identical: 117 nested-main, 82 target-size, and 27 skip-link failures. Catena's 121 identity/status tuples are identical; 15 complete Catena assertion objects and five failure details differ, so the package's unqualified byte-identical-row claim is false. |

Whole-file gzip-9 measurement independently reproduces CSS at 7,026 of the
original 8,000-byte ceiling and JavaScript at 12,946 of the original
13,000-byte ceiling. The rejected candidate measured 8,287 and 13,229; no
approved ceiling was raised. The correction therefore passes the original
budget requirement, with only 54 JavaScript bytes of whole-file headroom.

#### Visual and behavioral review

Original package assets, their contact sheet, every one of the 17 print pages,
and independent real-Chromium states were inspected. Genesis 1 retains a clear
Scripture-first wide hierarchy and the corrected Augustine 401 / Severian 401 /
Augustine 417 order. Genesis 42 is calm and sparse; Genesis 10 truthfully says
71 fragments are held while none is in the selected English voice. The valid
voice deep link, ordinary no-JavaScript desktop/mobile state, route-local
Gen 1 -> Gen 2 -> Back -> Forward sequence, 320-pixel reflow, and 200-percent
text reflow all work. The forced-colors CSS correctly reserves `Canvas` for the
base paragraph edge and `CanvasText` for projected boundaries, although the
package proves only media-query/computed-style emulation, not a real system
palette or assistive-technology experience.

Print is blocking. The selected Douay-Rheims Scripture edition disappears when
the controls are hidden; the printed footer still speaks of opening closed
fragments and retains navigation; page three is almost blank under an orphaned
author heading; and the package's 8-page/no-navigation claims contradict the
17-page artifact. The normal closed Bible label is also visibly clipped in the
integrated 60rem shell, an inherited B0 prerequisite rather than authority for
Catena to edit the shared wrapper.

#### Original finding matrix

| Finding | Correction-review result | Smallest remaining correction / evidence |
| --- | --- | --- |
| 1. Wrong Psalm anchor | **Open, outside owner.** The route still loads the same-numbered selected-Bible chapter under a projection refusal; no actual verse/address projection test exists. | Generator/shared-renderer projection that resolves or refuses Psalm 13, 14, and 100 across Vulgate, Douay, and KJV, with actual text and addresses. |
| 2. Chronological chain | **Corrected.** The route preserves generator order and coalesces only contiguous equal author/date runs; rendered Genesis 1 proves the 401/401/417 seam. | Retain the real ordered identity assertion, strengthened to prove every fragment ID exactly once rather than counts alone. |
| 3. Held/acquisition truth | **Changes required.** The generator-owned 89-row/46-chapter overlap and stripped confidence remain. Route copy calls projected rows "works" and "printed as recorded" although the projection omits confidence and does not establish distinct works. | Route calls them unreconciled lead entries and discloses that confidence is omitted; generator owner later reconciles identity and preserves confidence. Pin exact row identity/order, not only counts. |
| 4. Licensed obligations | **Changes required.** Real Severian data still reaches the route only as `licensed`. The new renderer invents a second lazy-payload acknowledgement channel and suppresses a supplied `rights_basis` whenever any acknowledgement is truthy; malformed values can hide valid rights data. | One generator-owned licence projection; route validates nonempty typed fields and renders every supplied obligation without browser-side precedence or suppression. Re-review one real Severian excerpt through artifact, payload, screen, and print. |
| 5. Cited state/history | **Changes required.** The local Back/Forward sequence passes and the shared `lastWritten` bug remains properly outside the lane. Route parsing still accepts duplicate recognized keys and malformed `translation:en:extra`, whitespace, or arbitrary suffixes; an identical invalid URL has history-dependent validation/recovery; mixed invalid hashchange leaves stale controls; recovery loses focus; transport failures can leave URL/render disagreement; and stale rejected requests can erase newer valid or invalid state. | Validate the complete multimap and a closed whole-voice grammar; make invalid interpretation independent of prior controls; synchronize sound controls and focus; discard stale errors before mutation; keep URL/render agreement across failures. Test cold/hashchange for every key, duplicates, races, bootstrap failure, recovery, reload, Back, and Forward in the real page. |
| 6. No-JavaScript and print | **Changes required.** Static no-JavaScript truth passes at desktop and 393 pixels, but no no-JavaScript 320 proof or throttled startup exists. Print loses Scripture-edition identity, retains interaction prose/navigation and loopback annotations, and paginates poorly. | Preserve a print-visible typed state and Scripture edition, remove interactive-only prose and navigation/annotations, repair pagination, and supply accurate inspected PDF plus no-JavaScript 320 and throttled-startup evidence. |
| 7. Forced colors | **Implementation correction passes; evidence remains incomplete.** The paragraph-border distinction is sound, but only emulation/computed styles are shown and no focused-element or full system-palette capture exists. Normal focus also overrides the accepted strong-blue role with a thinner violet route rule. | Retain the Canvas/CanvasText distinction, stop overriding shared focus semantics, and supply focused real forced-colors and reduced-motion evidence under the governing protocol. |
| 8. False counts/states | **Changes required.** Genesis 10 and Genesis 42 counts are truthful, but a synthetic blocked record simultaneously renders "Nothing held here", "No commentary ... held", and "Held, and not renderable yet" because tally/chain count fragments while blocked rows render separately. Integrity and invalid states can also label a selected voice "none here". | Derive tally, empty, blocked, integrity, and voice-option claims from one typed state; assert exact state-to-node association and reject contradictory empty/blocked output. |
| 9. Release binding | **Open, outside owner.** Exactly three route bindings are stale and Catena data still lacks a release-owned root. | Release owner adds deterministic data binding, proves content changes move it, and re-signs the reconciled accepted route. |
| 10. Shared shell/integration | **Boundary preserved; prerequisite open.** No shared or protected file changed. The inherited 60rem wrapper, nested `main`, skip target, arrow/focus, target-size, and shared-history defects remain. | B0/shared owner corrects and independently verifies its seams; common-gate owner separately decides the voice sample. |
| 11. Evidence and budgets | **Budget pass; handoff changes required.** The 8,000/13,000 whole-file ceilings are met without waiver. Mechanical archive integrity passes, but the false head/page/gate/no-navigation claims, private data, absent capture files, and missing governed evidence make the package protocol-incomplete. | Keep the immutable pair unchanged. Produce a new timestamped sanitized package with reproducible capture commands, accurate claims, before/after pairs, the complete focused matrix, real AT/forced-colors where required, a new manifest, and a new ZIP digest. |

Additional route-local robustness findings reinforce, rather than broaden, the
matrix: index/manifest bootstrap failures leave permanent Loading labels;
asynchronous fragment completion/failure is not announced; detailed per-work
translation-absence reasons are hidden in a closed disclosure despite the
non-deferrable absence contract; the primary Scripture locus is absent from
heading navigation; and invalid-address recovery removes the focused link
without restoring focus. These all remain within the new Catena route/test
correction boundary or are explicitly assigned to the existing shared owner.

#### Disposition, blockers, and next action

**Disposition: CHANGES REQUIRED.** The correction is not accepted for bounded
integration. It remains off main; this review performs no merge, release
re-signing, deployment, cutover, or follow-on implementation.

Remaining blockers are the route/test defects in findings 3-8 and 11; the
generator/data prerequisites in findings 1, 3, and 4; the release prerequisite
in finding 9; the common-gate and B0/shared-shell prerequisites in finding 10
and the shared half of finding 5; and a new protocol-complete exact-head package
followed by fresh independent review. Passing chronology, no-JavaScript truth,
reflow, route-local history, forced-colors CSS, package mechanics, and budgets
must not be regressed.

**One E1 next action:** dispatch one new bounded Catena correction lane from
current main. It may edit only the three Catena route assets, the focused
Catena test, and the four durable authority records needed to record its state;
it must fix the route/test and handoff defects above, create a new immutable
sanitized package, and return for fresh independent review. It must not edit or
dispatch the generator/data, release, common-gate, B0/shared-shell, protected
Liturgy, or PDF prerequisites and must not merge, re-sign, deploy, or cut over.

## Remaining program sequence

| Work | Current state | Exact dependency / stopping line |
| --- | --- | --- |
| B0/B1 shared non-liturgy implementation and harness | Authorized separately; not owned by this design branch | May use accepted A3/A4 direction and implementation findings; must stop before inventing C0/C1/D0/E0/F0 compositions and must not enter protected liturgy files. |
| C2/D1 production surface implementation | Eligible after the shell ownership boundary is clean | C0/C1/D0 are accepted; avoid branches that contend for global generator, site CSS, release binding, or shell files. |
| E1 Catena production implementation | **Changes required** at correction head `dfc636665` | Preserve accepted E0 and the passing bounded corrections. A new Catena-only correction lane must repair the route/test and handoff defects recorded above, leave every generator/data, release, common-gate, B0/shared-shell, protected Liturgy, and PDF prerequisite with its owner, and return a new protocol-complete exact-head handoff for fresh independent review. |
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
| 2026-08-10 | E1 Catena production independent review | **CHANGES REQUIRED.** E0's direction and E1's narrow product boundary survive, but exact real-data review found blocking Scripture projection, chronology, acquisition/held truth, licensed attribution, cited-state, no-JavaScript/print, forced-colors, state-counting, release-binding, shared-owner prerequisite, and evidence defects. The review changed no implementation and performed no merge, deployment, cutover, or follow-on work. | Reviewed head `efd7559a93310442753383bfeec80529f4693288` against main `9b9ff74a77d1bcd7d454d2a7fc448b8a6c8f1fd4`; package `20260809T030856Z-catena-wave-1-implementation.zip`; independently measured ZIP SHA-256 `e906ffcf4a056e00ba4596059d0eef6255fedd320f2fb1ecf96e43f3c29c72c8`. |
| 2026-08-11 | E1 Catena bounded correction | Reconstructed the route-owned patch from current main inside the three Catena assets and one focused test; recorded the outside-owner seams and produced an immutable exact-head package. | Route `67191afd1`; packaged head `dfc636665`; branch `impl/catena-wave-1-e1-corrections`; package `20260811T134130Z-catena-e1-corrections.zip`. |
| 2026-08-11 | E1 Catena correction independent review | **CHANGES REQUIRED.** Chronology, ordinary no-JavaScript truth, reflow, route-local Back/Forward, forced-colors CSS, archive mechanics, and original budgets pass. Route-owned URL, async-state, blocked/empty, leads, licence, print, accessibility, and handoff defects remain; all outside-owner prerequisites remain explicit. No implementation, merge, release re-signing, deployment, cutover, or follow-on work occurred. | Reviewed head `dfc636665df26563138ff893bd2a9f9afc7d80c0` against main `9b9ff74a77d1bcd7d454d2a7fc448b8a6c8f1fd4`; ZIP SHA-256 `8013074d9a77ae54208399207e10d58aaacb7e1b6efab6e820bbeaaa9fd83b05`. |

## Next Codex tasks

No implementation or integration task is authorized by this review. After this
review-disposition record is committed and pushed on its dedicated independent-
review branch and its exact SHA is reported, stop. The sole E1 follow-up is the
new bounded Catena correction lane specified above. This disposition does not
authorize merging the candidate or review branch, pushing `main`, re-signing a
release, deployment, public cutover, protected Liturgy edits, canonical PDF
changes, or work in any separately owned prerequisite.

Append later findings and dispositions. Do not rewrite earlier rows to make the
sequence appear cleaner.
