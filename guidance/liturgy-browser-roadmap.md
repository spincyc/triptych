# Dynamic Missal and Propers browser roadmap

## Status

This is the evolving execution record for the product governed by
[the liturgy-browser vision](liturgy-browser-vision.md). It records the current
baseline, gaps, parallel workstreams, dependencies, acceptance gates, and
progress. Update it when evidence or implementation changes. Do not weaken a
vision invariant here.

This roadmap does not authorize liturgical data, source acquisition,
publication, deployment, or release on its own. Each workstream remains subject
to the guidance that owns its data and artifacts.

## Completion plan, 2026-10-19

This section is the current recovery and execution plan. It supersedes the
older sections' descriptions of the **current** baseline and next action;
their dated implementation and acceptance records remain historical evidence.
The [vision](liturgy-browser-vision.md) still owns the product contract. The
maintainer requested this plan's persistence on `feature/missal-reader`;
recording it does not mark its implementation milestones accepted.

### Current priority: complete annual minimum reader, 2026-10-20

The maintainer explicitly puts correctness and completeness of Propers and
Commons first: one full TLM year and one full Novus Ordo year for **each**
Sunday cycle A, B and C. This supersedes the previous next-action ordering.
The minimum reader uses the existing Day/Propers reading path and source model.

| Audit | Inclusive dates | Scope |
| --- | --- | --- |
| Roman 1962 TLM | 2026-01-01–2026-12-31 | 365 civil dates |
| Novus Ordo A | 2025-11-30–2026-11-28 | 364 dates, weekday cycle II where applicable |
| Novus Ordo B | 2026-11-29–2027-11-27 | 364 dates, weekday cycle I where applicable |
| Novus Ordo C | 2027-11-28–2028-12-02 | 371 dates, weekday cycle II where applicable |

The durable [annual structural gate](../tools/tests/test_complete_missal_year.py)
uses these four intervals: 1,464 date/calendar coordinates, 2,928 English/Latin
states and 5,856 JSON/text renderings. The full run remains opt-in and has not
been run for this scope. Its structural checks do not establish correct
appointments, literal wording or complete text availability.

The Novus Ordo intervals are complete liturgical years, including their own
Advent, derived through the existing calendar owner under
[calendar computation](liturgy/calendar-computation.md). Preserve territorial
transfer branches and source-owned choices; do not invent precedence or a
local calendar. Audit every date, appointed formulary, Common referral,
commemoration, form, reading cycle and alternative. Repair source/data and basic
reading failures before adding capabilities. Track appointment correctness,
exact wording, available language/witness and publication separately; a typed
gap or successful structural dump does not establish complete liturgical text.

Startup optimization, further print/visual refinements, advanced modes,
pre-1955 expansion and final review-package work are subsequent features.
Their completed checkpoints and dormant proposals remain historical evidence.
No speech synthesis, WAV/audio capture, Orca/service setup or audio test
pipeline is required or planned. Existing browser semantic, keyboard, DOM and
AX checks remain relevant to the basic reader; unrelated feature acceptance
matrices do not hold up this annual content-first implementation.

### Recovered baseline and acceptance boundaries

Recovery baseline: `c6da24eda429337fe13d59420a3c489a98a16e66`, inspected on
2026-10-19. The canonical public entrances are
[Day](https://mystago.gy/liturgy/day.html) and
[Propers](https://mystago.gy/liturgy/index.html). The repository's older Pages
hostname redirects to `mystago.gy`. The latest successful Pages run at recovery,
[38988789355](https://github.com/spincyc/triptych/actions/runs/38988789355),
names that commit; the served `day-reader.js` also matched the tracked file
byte for byte. These are recovery observations, not acceptance of a new reader.

- Preserve the accepted Liturgical Instrument foundation and canonical URLs.
  Day enables Read and Missal. Propers enables Read. Study and Compare are
  disabled, as is Propers Missal. A visible mode description is not delivered
  functionality; source owners are `day.html` and `index.html` under
  `src/web/browser/liturgy/`.
- The separately accepted August public cutover was a narrower release than
  the full four-mode M6 destination. Older wording that M6 would be the first
  public redesigned reader release describes the original sequencing, not
  today's deployment. Full M6 completion remains outstanding.
- The August 28 Complete Missal remediation received independent AI cold
  review and verified deployment. Its completion included typed unresolved
  and unavailable dispositions; it did not assert possession of every text.
  [The work register](../PROJECT-WORK.md) and
  [promise ledger](../promised-deliverables.toml) own that disposition and
  supersede the August 20/27 rows' then-current review status.
- The separate `liturgy-reader-live-ritual-flow-2026-08-07` deliverable still
  has six open requirements. October's KI-052 also records it as planned.
  Reuse that deliverable for orientation and long-reading work; do not mark it
  complete from the old implementation checkpoint or duplicate its promises.
- October repaired nested main landmarks, arrival Browse focus trapping,
  leaking Day CSS, and incompatible Ordinary options surviving a missal
  switch. Reproduce before reopening them. The old example-replay failure is
  also superseded by October's recorded zero-divergence result.
- KI-046 retains 77 enhanced control-target findings across the whole corpus.
  Treat them as a design baseline to investigate by affected surface, not as
  77 Liturgy defects or an established WCAG AA failure. Ritual-flow acceptance
  also needs a fresh disposition of the historical mobile-overlap measurement.
- Some pre-rewrite commit IDs in historical continuity are absent from the
  recovered history. Reachable milestones include `6603fd0947ec9cb34bafaf64765974dd5b53ad2c`
  (canonical promotion), `ab9eb9388d182b0013baa0f708ec4ee6e8a5abd5`
  (ritual-orientation checkpoint), and `3e35f3b1f22bdf9afc26f8557aee5e86fa965028`
  (takeover record). Do not apply old scratch patches or replay old cutover
  instructions against the current reader.

### Content and translation inventory

The following are measured or source-recorded facts at the recovery commit.
The units are deliberately named: distinct source identities, modeled elements,
and reused occurrences are different denominators. None is a whole-Missal
completion percentage.

| Family | Represented Proper scope | English non-scriptural identities | Latin Proper bodies | Ordinary coverage and qualification |
| --- | --- | --- | --- | --- |
| Roman 1962 | 491 Mass records; 3,443 direct Proper records; 5,060 resolved occurrences | 112 of 1,197 canonical identities translated; 1,085 typed untranslated | 1,377 available resolved occurrences; 209 unavailable | English 189 and Latin 112 of 189 modeled elements; all held wording is an 1861 antecedent uncollated against the 1962 target |
| Postconciliar 2008 | 619 Mass records; 2,998 Proper records; seven Commons have identities without formularies | 113 of 330 canonical identities: 70 project translations, 40 Cummiskey antecedents, three Caswall sequences; 217 untranslated | No resident/published full bodies; the source census records 322 incipit-only and four absent non-scriptural slots | No English; 20 Latin antecedent elements of 59 modeled, five target-collated and 15 uncollated |
| Pre-1955, nominal 1920 | Eight departure rows, no independent Proper wording; 489 projected Mass records through inheritance | 99 of 1,149 canonical identities, principally inherited dispositions | No target-qualified published Proper bodies | English 195 and Latin 112 of 195 modeled elements; uncollated 1861 antecedents |

The seven public Bible editions are Douay-Rheims (Challoner), Douay-Rheims
(American 1899), Clementine Vulgate, Catholic Public Domain Version, World
English Bible Catholic Edition, King James with Apocrypha, and Revised Version
with Apocrypha. Six are English and one Latin. They supply Bible renderings,
not seven complete liturgical translations.

The 1962 projection delegates 3,474 occurrences to Scripture and the
postconciliar projection 2,647. Citation expansion does not establish the exact
Missal or Lectionary incipit, part-verse, antiphon adaptation, response,
acclamation, or ending. Existing gaps include 4 Esdras references, the declared
postconciliar Ordinary Time 24 Saturday cycle-II Psalm 56:13–14 refusal, and
edition-dependent correspondence gaps in Sirach, Psalms, Daniel, and Esther.
The 2026 calendar report finds some Mass on all 365 dates in each family;
that does not prove precedence, complete wording, or Missal-mode rendering.

Evidence owners:

- [Public Bible manifest](../src/web/data/bibles.json) and the generated
  [1962](../src/web/data/structure/propers/roman-1962.json),
  [postconciliar](../src/web/data/structure/propers/postconciliar.json), and
  [pre-1955](../src/web/data/structure/propers/roman-pre-1955.json) structures.
- [1962 translation inventory](../src/sources/inventories/roman-1962-proper-translations-v1.toml)
  and [postconciliar translation inventory](../src/sources/inventories/postconciliar-proper-translations-v1.toml).
  The latter records the 70 project-created translations as unreviewed study
  English. Review does not convert them into approved liturgical translations.
- [1962 Ordinary inventory](../src/sources/inventories/roman-1962-ordo-missae-v1.toml),
  [postconciliar Ordinary inventory](../src/sources/inventories/postconciliar-ordo-missae-v1.toml),
  and [pre-1955 inheritance](../src/sources/calendars/roman-pre-1955/propers.yaml).
- [Completeness report implementation](../tools/complete-missal):
  `expected_celebrations` and `expected_text_slots` have no target-book
  expectation model. `--check` validates the report while 13 of 15 dimension
  cells per family remain unresolved: 39 cells, not 39 missing texts.

### Recovery findings and remaining design gaps

The first two findings below describe the recovered baseline. C1 implements
their accounting and label corrections; real-browser acceptance remains open.

| Finding | Evidence and consequence |
| --- | --- |
| Availability counters mix units | `orationLanguagesOf()` in `src/web/browser/shared/browser-core.js` counts translation rows against top-level occurrences and omits nested cycle accounting. The 1962 label 234 of 1,441 counts 234 records covering only 207 occurrences, with repeated witnesses/aliases; those occurrences derive from 112 canonical translated identities. |
| Latin availability is overstated | `orationLanguageLabel()` says “Latin, as printed” and assumes source-language completeness even where postconciliar full Proper bodies are absent. Availability and target-edition fidelity need independent assertions. |
| Cue loss | `spoken()` in `src/web/browser/liturgy/day.js` suppresses an `all` opening cue but still removes the leading source P./R. The postconciliar preface dialogue and Pax Domini lose their initial priest attribution. |
| Duplicate and inconsistent cues | Structured 1962 Confiteor turns receive a gutter P plus source P.; server turns receive S plus source R. An event-specific rule in `reader-instrument.css` hides the generated response glyph only for postconciliar Orate fratres. |
| Sparse structured dialogue | Of 301 held 1962 Ordinary translations, ten across five elements have turns and none has an explicit dialogue role. Of 20 held postconciliar translations, only Orate fratres has turns. Most exchanges remain inline prose with word labels. |
| Flattened prose, poetry, and actions | Shared passage/composed renderers use single paragraphs. They do not consume the Bible paragraph layer or checked stanza structure. A Pentecost Alleluia's embedded genuflection rubric remains mixed into principal text. File hard wraps cannot safely supply poetic lineation. |
| Sustained-reading hierarchy | Live 1962 Missal reading interleaves small headings, source page loci, and inline response labels with short exchanges. The pending ritual-flow work owns the current-place indicator and Contents behavior. |
| Unclear daily choices | On postconciliar 2026-10-19, three legitimate options appear as inline radios, repeated choice headings, and unexpanded rubric codes. Preserve explicit choice while making its presentation understandable and touch-friendly. |
| Advanced product unfinished | Study, Compare, Propers Missal, comprehensive search, and paired bilingual presentation still need their governed implementations and acceptance. Existing internal fixtures do not prove public coverage. |

Live Chromium inspection covered Roman 1962 Read at 393×852, Roman 1962
Missal at 1440×1000, postconciliar Read at 393×852, and the postconciliar
choice state at 1440×1000. The 1962 mobile first view already contains the
celebration and real text. Postconciliar Advent I exposed Bible citation
expansion including a Psalm superscription in its Entrance Antiphon. These are
diagnostic observations; the temporary captures were not retained as an
immutable acceptance package. Reproduce them for any release review.

### Ordered implementation milestones

The C-series below refines the existing W1–W9 workstreams. It does not replace
M1–M6 or broaden any historical acceptance. C1 is **complete** on the feature branch: every
requirement passes under the maintainer decisions below, and the pre-1955
recension is enumerated from its accepted witness. C2, C3, C4, C5 and C6 are
**in progress**; C6 release acceptance remains open.

Maintainer decisions, 2026-10-19:

- **1920 witness.** The files circulating as the "1920 typical edition" are
  public domain for their 1920 content and may be pulled and used. They are the
  registered Bonn 2004 *reimpressio* of a conformed 28th edition of about
  1954, now accepted as the witness of the pre-1955 recension, with the 1922
  Mame conformed printing as control. An exact Vatican 1920 impression is no
  longer a C1 blocker. Text first published in 1931 or later inside that
  printing is outside the decision (`guidance/missals.md` §5), so post-1922
  additions are inventoried in separate slices.
- **2008.** Acquiring complete 2008 body or index evidence is deferred. The
  2008 whole-book universe stays an explicit unresolved boundary and does not
  hold up later milestones.
- **Performance.** Load-time optimization is deferred to the end, once
  presentation and sources are in place, so the project does not chase
  performance changes the entire time. Payload and timing are measured and
  recorded at checkpoints, but budget failures do not block C1–C5; C6 owns
  them. This supersedes treating the 2.5 s LCP budget as a per-milestone gate.

| Milestone | Deliverable | Exit evidence and dependency |
| --- | --- | --- |
| C1 — Truthful coverage | One typed coverage report and an expected-target inventory; corrected language/witness controls and notices | Every expected target is classified; canonical identities, occurrences, and witness alternatives have separate counts; browser, generated data, CLI, and tests agree. W1/W4/W7/W9. |
| C2 — Representative Mass pattern | One fully audited representative Mass per principal missal, using the common text/turn model, source links, language selection, reading layout, and print | Each promised unit is checked; missing or restricted units remain explicit and prevent a claim of textual completeness. No unrelated text substitution. Depends on C1; W1/W3/W4/W7. |
| C3 — Corpus completion | Expand the pattern through the expected daily formularies, Commons, commemorations, Ordinary, prefaces, cycles, alternatives, and exceptional rites | Exact target and language denominators; source and publication checks; zero unexplained gaps in each completed slice. Begin 1962 completion while postconciliar acquisition and review run alongside it. Depends on C1/C2; W7. |
| C4 — Reading design and navigation | Consistent dialogue/glyph presentation, paragraph/stanza/action layouts, bilingual pairing, source-aware hierarchy, current-place Contents, date movement, and clear choices | Fresh real-browser and print evidence; source text/event parity; all six existing ritual-flow requirements independently dispositioned. Prototype alongside C1; integrate after C2. W2/W3/W8/W9. |
| C5 — Complete shared capabilities | Propers Missal, Study, semantic Compare, meaningful formulary search, contextual history/source navigation, sharing, and preferences | Both entrances meet their separate identity/URL contracts; modes operate over the same semantic units; compare retains one-sided absences and independently resolved calendar differences. Depends on stable C1/C2/C4 seams; W3/W5/W6. |
| C6 — Accepted release | Advertised coverage and all implemented modes pass the vision's acceptance gates | Full content/semantic/browser/print/URL evidence, independent review disposition, exact artifact and deployment verification. A reliable daily Read/Missal slice may be accepted within its named boundary; full M6 requires C5 and the complete product contract. |

#### C1: one coverage vocabulary and a defensible denominator

Inventory expected targets from the identified books rather than from the
records already held. Include celebrations, Commons, commemorations, proper
prefaces, Ordinary options, Mass forms, cycles, and rites outside an ordinary
Mass frame. Record date range, recension, territory, language, and source for
each advertised slice. The existing typed absences remain distinct: genuinely
inapplicable, absent in this witness, not sourced, not publishable, and unresolved.

Track exact target wording, historical antecedent, study translation, and Bible
reconstruction separately from availability and rights. Count a target once
even if multiple witnesses or aliases supply it. Expose witness selection and
Mass-specific coverage without implying that a whole language is complete.
All selectors, notices, discovery results, and audit tools consume this report.
The report may establish a complete inventory with known gaps; textual
completion requires those gaps to be filled for the claimed scope.

Implementation and bounded source checkpoint, 2026-10-19: the independent
[expected-target inventory](../src/sources/inventories/missal-expected-targets-v1.toml)
contains 2,850 identities in 36 bounded source slices and 57 explicit
boundaries, including sixty appointments/referrals established directly from
the official 2008 supplement. These heterogeneous identities do not form a
whole-book text-slot denominator. The accompanying
[source review](../src/sources/inventories/missal-expected-targets-review-2026-10-19.md)
records source extent, target correspondence and retrieval limits. In
particular, Saint Anastasia's Christmas commemoration is expected from the
1962 source calendar but lacks a represented Mass entry. Whole-book enumeration
remains open for every family. The accessible 2002 book's named structural
queues are inventoried at their declared granularity; they do not establish
exact 2008 correspondence. Completion requires authenticated 1920 Vatican
evidence, readable full 1962 witness evidence, an authenticated complete 2008
body/index or documented correspondence for each bounded slice, and the
selected US 2011 edition's structural dispositions. The source review records
the exact retrieval boundaries.

The versioned shared report drives generated
Proper/Ordinary data, CLI accounting, and Day/Propers controls, discovery and
selected-Mass notices. Partial witnesses remain selectable with explicit gaps;
mixed components and nested cycles retain separate accounting. Independent
review fixes passed 279 regression tests (six existing skips), all nineteen
affected captured examples, source checks, and strict public-data admission.
The historical three-calendar, 365-date gate passed all 4,380 JSON/text renderings; final source-snapshot
coverage checks pass 53 tests. Corrected real-browser fixtures now exercise
alias deduplication and genuinely partial witnesses; their offline/static
regression checks pass, with live browser runs still skipped or blocked.
Browser, responsive and print acceptance require an execution environment
that permits the local listener and Chromium system calls refused here.
The [work register](../PROJECT-WORK.md) records the validation results,
unchanged source-only baseline failures, publication checkpoints, and payload
cost. This checkpoint does not close C1.

Retry, 2026-10-19: the maintainer requested fresh parallel source and browser
work after removing the execution restrictions. The complete registered 1962
PDF now downloads with its expected hash, and Chromium runs the reader harness.
Exact-target source enumeration, independent responsive/print review and payload
measurements are active. The earlier inaccessible Isidore 3453 candidate was
inspected and is a 2004 reprint, not an authenticated 1920 Vatican impression.
The acceptance criteria above remain unchanged.

The second retry's inventory checkpoint enumerates every section of the
registered 1962 facsimile and assigns every artifact page to a section slice or
an extent boundary. It joins twenty 2002 appointments to the official 2008
variation list and adds the selected U.S. 2011 General Index headings. An
independent page-image review then confirmed the 1962 formulary and Preface
enumeration, corrected nine kinds, and retired those two whole-book boundaries.
The inventory now holds 10,683 targets in 72 slices with 91 boundaries; the
[source review](../src/sources/inventories/missal-expected-targets-review-2026-10-19.md)
owns the extents and dispositions. All three whole-book universes stay
unresolved. 1962 still has unenumerated text-slot and other dimensions. 2008
needs an authenticated complete body or index, and 1920 an authenticated
Vatican impression; a bounded search found neither, and the
[acquisition audit](../src/sources/inventories/missal-acquisition-audit-v1.toml)
records the hosts reached and the hosts still unsearched.

Real-browser acceptance of the C1 surfaces is recorded in the
[work register](../PROJECT-WORK.md); C1-attributable defects were fixed with
regressions. These findings belong to C4 and the ritual-flow deliverable:

| Finding | Owner surface |
| --- | --- |
| At 400% zoom, a Contents jump leaves the chosen unit under the fixed action bar | `reader-instrument.css` scroll padding/margin; ritual-flow `contents-live-map` |
| Coverage notice and absence notes are about 12 px, below the 16 px body norm | `reader-instrument.css` notice styles |
| Closed selects truncate trailing coverage figures, including the witness count | Browse and Date selector presentation |
| Latin headings and option labels carry no `lang="la"` | shared renderer and reader identity blocks |
| Pre-1955 days without a formulary show "Selection unavailable" | `day-reader.js` selection resolution |
| A postconciliar unit says "No English or Latin body is held here" beside restricted siblings | absence wording for `untranslated` units |

Throttled-mobile cold LCP still fails the 2.5 s budget, as it did before C1
(Day 1962 12.21 s against 11.89 s). Under the 2026-10-19 decision above this is
C6 work. These are the recorded options, all requiring reader changes. In roman-1962 gzip terms, a lazily fetched coverage sidecar plus
removing the pre-C1 `forms[].propers` copy saves about 233 KB. Deriving unit
target and occurrence identities from position saves about 75 KB. Computing
per-Mass coverage in the browser saves about 66 KB. Per-Mass structure files,
which `web-data.md` already names as the next candidate, are the largest
option.

#### C2: the reusable representative-Mass pattern

Each reviewed slice carries the following evidence in its existing source and
test owners, rather than another hand-maintained copy of the liturgical text:

1. **Identity and appointment:** edition, calendar/territory, date or stable
   formulary, cycle, form, authorized alternatives, Ordinary options, and
   governing source. Preserve genuinely coequal choices until explicitly made.
2. **Expected sequence:** every appointed semantic unit and seat, including
   commemorations and exceptional before/after material. Preserve event IDs
   and legacy URLs; version any identity change under the state contract.
3. **Text and witness:** target-language wording, translation, exact loci,
   rights/distribution basis, collation status, and typed absences. Whole-book
   possession does not establish a checked passage.
4. **Internal text structure:** edition-owned paragraphs, checked stanzas,
   speaker/role turns, printed markers, and inline actions. Every derivative
   must retain an auditable relationship to immutable witness text.
5. **Presentation:** Read and Missal, chosen language/witness, paired bilingual
   units, source access, clear incomplete states, and independent print context.
6. **Interaction and evidence:** selection, Contents, deep-scroll location,
   focus restoration, sharing, copy behavior, real accessibility output, and
   browser/generated-data/CLI parity.

Existing 1962 Pentecost X on 2026-08-02 and postconciliar Advent I on
2026-11-29 are useful reproducible baseline fixtures, not assertions that
either is textually complete. Select the first completion exemplars only after
C1 establishes attainable, source-checked coverage. A postconciliar exemplar
with unavailable exact text may prove the renderer's partial-state behavior
but cannot pass the complete-text gate.

##### C2 exemplars and execution plan, 2026-10-19

A read-only audit ran real Chromium against the source-served readers at
`d3c36e8ea`. Its per-unit tables were transient; this section records the
decisions and the gap register they produced.

**Exemplars.** All three principal missals use Pentecost Sunday, civil date
**2026-05-24**. That one formulary exercises a Sequence, the Pentecost
genuflection, proper Ordinary variables, form and source alternatives, and a
Sunday cycle. The three sides resolve the date independently, which also gives
C5 its first Day Compare fixture.

| Missal | Exemplar | Gate it can reach | Measured at selection |
| --- | --- | --- | --- |
| Roman 1962 | `pentecost` (printed pp. 356–358) | complete text, after bounded C3 work | 10 units: 6 Bible reconstructions, 5 bodies; Latin 5/5 collated word-exact projections; English 1/5; Preface, Communicantes and Hanc igitur not modelled |
| Postconciliar | `pentecost`, form `day`, Year A | partial-state behaviour only | 16 units: 11 Bible, 5 bodies; Latin 0/5; English 2/5 (study Collect, antecedent Sequence); Missal frame withheld for lack of a Sequence slot |
| Pre-1955 | `pentecost` | after the Bonn-witness inventory | inherited from 1962, uncollated |

Alternates: 1962 Saturday of Our Lady III, the highest attainable text;
postconciliar Corpus Christi; pre-1955 Vigil of Pentecost, a probable
structural departure. 1962 Pentecost X and postconciliar Advent I stay
regression baselines. Low Sunday 1962 (2026-04-12) and Lent III Year A
(2026-03-08) cover long Gospels.

**Decisions taken from existing guidance, 2026-10-19:**

- A collated projection that is word-exact under the 2026-09-03 rule in
  [propers-for-agents](propers-for-agents.md) is the target's wording and
  counts as `exact-target`. That rule makes agreement of words, never of
  strings, the test.
- A Read-mode Contents jump writes `location` to the URL, as Missal mode
  already does. The [vision](liturgy-browser-vision.md) requires stable
  semantic location anchors.
- The postconciliar Vigil-or-Day offering needs a cited source rule (G8). It is
  research, not preference.
- The pre-1955 exemplar is chosen after its witness inventory is read.

**Gap register.** C2 owns wrong or unexplained claims, C3 missing text, and C4
truthful but not yet usable presentation.

| ID | Finding | Owner | Milestone |
| --- | --- | --- | --- |
| G1 | Coverage never receives the Latin provenance relation: `tools/mass-propers` omits it and `_missal_coverage.unit` reads `latin.rights` where data carry `latin.publication.basis`, so every report says "0 exact-target" | `tools/mass-propers`, `scripts/_missal_coverage.py` | C2 |
| G2 | Caswall English is `unresolved` in 1962 and pre-1955 but `historical-antecedent` postconciliar | 1962 translation inventory | C2 |
| G3 | Four 1962 oration absences say "rights restricted" although Cummiskey 1861 is public domain; the blocker is a missing passage binding | 1962 translation sidecar; absence wording | C2 retype; C3 binding |
| G4 | Exemplar expected-target rows are unjoined and text-slot targets are unclassified | expected-target inventory, `expectations()` | C2 |
| G5 | Ordinary variables are not appointed: Missal mode prints all eleven 1962 Prefaces, and the common Communicantes and Hanc igitur stand silently in Pentecost's proper seats; the postconciliar Preface and paschal dismissal are unmodelled; pre-1955 seasonal orations render on a first-class day | calendar appointments, Preface rules, Ordinary inventories, `tools/mass-ordinary`, `ordinary-seating.js` | C2 model; C3 texts |
| G6 | 1962 English Missal mode shows postcommunion elements its inventory types `not-in-the-1962-ordo` | `roman-1962-ordo-missae-v1.toml` exclusions | C2 |
| G7 | The postconciliar Ordinary inventory has no Sequence slot, so the Missal frame is withheld on Pentecost, Easter, Corpus Christi and Our Lady of Sorrows | postconciliar Ordinary inventory, seating | C2 |
| G8 | Postconciliar 2026-05-24 offers Vigil and Day with no default and loses the celebration from the first view | postconciliar rubrics, assembly, calendar | C2 rule; C4 presentation |
| G9 | No unit-level marker says a Bible reconstruction is not the Missal's wording | shared renderer | C2 |
| G10 | Choosing an unavailable English hides the held Latin | shared renderer | C2; C4 pairing |
| G11 | Pre-1955 Day surfaces and print omit the inherited-and-uncollated caveat | `day.js` notice and print | C2 |
| G12 | `no-exemplar` units lose their typed reason ("No English or Latin body is held here") | shared absence wording | C2 |
| G13 | Details says no formulary outcome was selected after an explicit `form=day` | `day.js` Details | C2 |
| G14 | Sequence stanzas flatten, the genuflection rubric sits in principal text, and copy loses ℣ but gains labels | inline-action and stanza data contract (C2); rendering and copy (C4) | C2/C4 |
| G15–G16 | Repeated "Not shown" notes, untagged Latin headings, small form radios, a witness chooser offering a witness with no body for the unit | C4 surfaces | C4 |
| G17 | Read-mode Contents jumps write no `location` | reader state | C2 |
| G18–G20 | Missal pericope incipits and refrains; 1962 Ordinary collation; the basis of the postconciliar study Collect | calendar and fragment data; Ordinary inventory; translation review | C3. G19 slice, 2026-10-19: the 99 exercised 1861 Latin elements were collated against the 1962 Ordo on page images. 85, plus the second Sanctus, are exact-target; 12 record variants or abbreviated bodies; 2 stay uncollated. The 1962 Ordinary has 104 collated Latin rows, 92 exact-target. |
| G21 | Approved postconciliar English and Lectionary English are restricted, and no 2002/2008 Latin body is held | publication policy; participation-aid review due to begin by 2026-11-15 | C3, rights-blocked |
| G22 | Pre-1955 needs witness loci, per-proper attestation, the Kalendarium and precedence | pre-1955 inventory | dependency |

**Ordered work.** Each step regenerates through its owning tool and adds its
regression before the next begins:

1. truthful accounting (G1–G3), implemented 2026-10-19:
   - coverage reads Latin provenance and publication records;
   - a collated `editorial-projection-exact-to-target` body is `exact-target`,
     so roman-1962 reports 1,377 exact-target uses (1,068 targets);
   - inherited Latin is never `exact-target`;
   - Caswall English is `historical-antecedent` in all three families;
   - 339 English absences whose only blocker is a missing passage binding are
     retyped `no-exemplar` and reported `not-sourced`.
   Follow-ups:
   - a more precise binding-pending absence kind;
   - typing the postconciliar `no-exemplar` rows that are really ICEL rights
     matters (G21) as restricted;
   - giving the Cummiskey and Lasance rows the same evidenced antecedent
     relation as Caswall;
2. the expected-target join (G4): the formulary level was implemented on
   2026-10-19:
   - 488 1962 and 463 pre-1955 form rows are joined, and none is
     not-represented.
   - The field `form_id` had three meanings. Its parent-reference use became
     `parent_id`, and its source-local formulary keys became
     `source_form_key`, so `form_id` now means only a held-Mass form join.
   - Four OCR-missed inventory rows were added after image checks.
   - The first text-slot join, 2026-10-20: all thirteen 1962 Pentecost slots
     now join their held Proper role or printed Ordinary appointment through
     the independently inventoried parent form. A missing Lesson or a changed
     Preface option is reported as `not-represented`; other unjoined slots stay
     unresolved. The whole-book text-slot join remains a follow-up;
3. the appointment and sequence model (G5–G8), implemented 2026-10-19:
   - The Preface, Communicantes, Hanc igitur and postconciliar dismissal are
     `[[appointments]]` in the Ordinary inventories, and formularies record
     their printed direction as `ordinary_appointments`.
   - Resolution takes the formulary's direction, then a stated span, then a
     sourced default. Otherwise a typed stand-in is shown, never the common
     form.
   - 1962 and pre-1955 Pentecost seat exactly the Holy Spirit Preface, with
     typed proper Communicantes and Hanc igitur absences (RGMR 482/493/501;
     Canon nn. 1093–1099; Bonn pp. 336–337).
   - The 1962 frame excludes the second-Postcommunion regime and Et famulos
     (Ordo nn. 1113–1139).
   - Pre-1955 seasonal orations are not said outside their rubrical windows.
   - The postconciliar frame seats the Sequence (IGMR 64).
   - On a solemnity's own date the Day takes its Day form; the Vigil is for the
     evening before (Missal 2002 p. 265; NUALC 11).
   Follow-ups:
   - Preface directions were then recorded from the sources on 2026-10-19:
     - 176 1962 formulary directions from the expected-target rows, plus the
       RGMR 482–499 de Tempore spans and the common default. 1962 days in 2026
       showing the stand-in fell from 337 to 0.
     - A recension no longer inherits its base's directions. Pre-1955 applies
       its own Bonn-attested `attested_appointments` (161 masses).
     - The pre-1955 rule that brings in a commemorated feast's or an octave's
       Preface (Bonn tit. VIII) needs a commemoration model, so 206 pre-1955
       days still show the typed stand-in.
     - The 1962 Cena Domini proper Communicantes and Hanc igitur need an
       Ordinary option.
     - Postconciliar Preface appointments are not yet recorded.
   - Placing a vigil on the preceding civil date needs `calendar-days` support.
   - The postconciliar proper Communicantes for Eucharistic Prayer I is not
     modelled.
   - Whether the pre-1955 frame carries the 1861 book's *Et famulos* is
     undecided;
4. claim-local truth in both entrances (G9–G13, G17), implemented 2026-10-19.
   Both entrances state each unit's claim from its coverage record:
   - a Bible-reconstructed unit carries one quiet "Bible reconstruction ·
     Missal wording not established" line, on screen and in print;
   - a missing translation leaves the held Latin visible beside its typed
     absence, and every absence names one of the five typed reasons;
   - pre-1955 Day shows the Propers recension caveat in its notice, Details
     and print;
   - Details reports an explicit formulary or form and only what remains open;
   - Read and Missal Contents jumps record `location` by replacing the history
     entry, as Propers does (neither Day mode had written it).
   Ordinary element absences received reader labels in the 2026-10-20 C4 pass.
   The `mass-propers` reading view now states the same typed reasons, held
   equal to the browser's table by test. Published inventory slices omit
   `source_refs`, which name repository records including restricted
   editions';
5. the internal-structure data contract (G14), handing rendering to C4;
6. exemplar evidence: harness states, a CLI/structure/browser event-order
   parity test, the viewport and print matrix, and an external-review handoff.

Checkpoint, 2026-10-20: the 1962 Pentecost inventory's ten Proper and three
Ordinary-variable slots are now explicitly joined and represented. A removed
Lesson and a wrong Preface appointment fail separately. Day and Propers select
the same ten Proper roles in the same order; Day adds their ritual seats. Fresh
source-served Chromium runs passed 55 Day and 49 Propers assertion groups with
no console or request failures. Captures at 1440, 393 and 320 CSS pixels have
no horizontal overflow. The Latin Day Missal print is 25 pages; English Read
is ten pages in both entrances. A follow-up print correction removes the
final-page tinted frame bleed in both entrances without changing those page
counts or the 25-page Latin Day Missal print. Extensive translation notes
still dominate the English print, an open C4 presentation finding. Full CLI/structure/browser
event-order parity, the complete viewport and print matrix, and independent
acceptance remain open; this checkpoint does not close C2 or C3.

Continuation, 2026-10-20: source-inventoried, unique parent-form and Proper-role
joins now classify more of the 1962 target universe. Of 6,285 inventoried text
slots, the served structure reports 3,182 represented, 178 not represented,
and 2,925 unresolved. Another 229 roles absent from their raw Mass rows resolve
through an appointed Common. The remaining 178 effective Sanctoral role gaps
are printed in the source but lack a role in the calendar model. The published
inventory also carries one earlier missing Christmas commemoration, so its
all-kind `not-represented` count is 179. These joins
establish structural placement, not word agreement or translation coverage.
Three image-checked Scripture appointments (St Francis Xavier's Alleluia and
St Lucy's Alleluia and Communion) and seven Common oration joins account for
the ten newly represented roles. The St Stanislaus C 2 page mark resolves one
Common option inherited by the pre-1955 model; six such selections remain
unresolved in each recension.
A focused Pentecost parity check now compares all 179 generated Missal events
with browser semantic and DOM order, and thirteen ordered CLI landmarks with
the same browser sequence. The CLI still has no machine-readable expanded
event stream for full event-ID parity. This is additional C2 evidence, not
independent acceptance. The follow-up CLI projection now exposes ordered,
text-free expanded event IDs. A source-served browser probe matches all 179
1962 Pentecost and 181 pre-1955 Pentecost event IDs and kinds against Day and
Propers, plus 71 postconciliar Day events. Date-free postconciliar Propers
retains its two typed unresolved Ordinary appointments. This closes the
exemplar event-order check; word-exact seating and independent C2 acceptance
remain open.

A second 2026-10-20 Sanctoral citation pass added twelve source-checked roles.
The effective Roman 1962 text-slot states are now 3,194 represented, 166 not
represented and 2,925 unresolved; across 7,990 target kinds they are 4,017,
167 and 3,806 respectively. Each added Gospel or chant uses the existing
Bible-reconstruction claim; no exact Missal wording is asserted. Eight
candidate chant joins were held because the printed words differ from the
whole Bible verse, and the St Gabriel Gospel's printed Luke 2:26–38 locator
contradicts its Annunciation body, so its role remains open pending a source
correction. The 1962 Adjutorium row now has source-bound priest and answer
turns, restoring its printed ℣/℟ dialogue cue; sixteen other Ordinary
elements still need glyph review.
The next print-only C4 pass moves an orphaned Collect translation credit beside
its witness account in both entrances. Same-source Chromium PDFs retain seven
English Read pages and identical extracted text; checked Latin layouts also
retain their page count and text. Longer mode-aware note composition remains
open.
St Lucy's Communion is the next bounded C3 word-exact repair: a target passage,
public-domain 1922 Mame witness and editorial projection now bind the 1962
Latin antiphon with `quasi`, while Psalm 118:161–162 remains a citation rather
than a substitute body. This brings Roman 1962 exact-target Latin Proper
availability to 1,074 of 1,203 represented composed targets. The text CLI now
labels Bible reconstructions beside citation expansions, and distinguishes
Bible text shown alongside a held Missal body. A form-qualified, text-free
Propers search index and a two-side functional-slot Compare core pass focused
tests; search controls, Compare mode, and independent C5 acceptance remain
open.

The next bounded C3 repair collates the St Thomas Apostle Introit against the
1962 typica and public-domain 1922 Mame printing. Its complete antiphon,
Psalm verse and Gloria Patri cue are exact-target Latin, raising the count to
1,075 of 1,204 represented composed targets. English has a typed no-exemplar
gap. The printed `honorati` differs from the Bible's `honorificati`; proposed
St Anthony Offertory and St Michael Introit Bible joins were likewise held
when their antiphon wording did not match. Whole-family text coverage remains
unresolved.
Their later page collation found the exact Missal chants in the public-domain
1922 Mame printing and the controlling 1962 pages. Both are now represented
as mixed source-bound Latin bodies with text-free English gaps, while their
Bible citations remain structural. Effective 1962 target states are 4,020
represented, 164 not represented and 3,806 unresolved. The whole-family
text denominator is still unresolved.

An exemplar passes C2 when:

- every expected text slot is joined and classified;
- every seat is the appointed text with its witness, relationship, locus and
  basis, or a typed absence in the appointed place, with no common or
  neighbouring substitute;
- coverage, Details, notices, `complete-missal` and Propers agree;
- Day and Propers render the same units;
- language and witness switches preserve location and never substitute;
- print carries identity, witness, coverage and recension caveats; and
- the console is clean.

1962 reaches the complete-text gate only after C3 supplies its chant,
pericope-incipit, English and Ordinary-variable texts. Postconciliar is
accepted only as a partial-state exemplar.

Bounded acceptance audit, 2026-10-20 (source snapshot `60b69ee46`):

| Pentecost exemplar | Checks already established | Acceptance still required |
| --- | --- | --- |
| 1962, main form | Thirteen inventoried text slots joined and represented; ten Proper Latin bodies exact-target; English available for nine Proper roles with the Lesson a typed witness gap; appointed Holy Spirit Preface, proper Communicantes and Hanc igitur; recorded 179-event CLI/structure/Day/Propers parity | Whole-form extent remains unresolved. Preserve the English Lesson and Communicantes variant gaps, the Preface's conditional words, and source-local Ordinary qualifications in the final language/witness, responsive and print review. |
| Pre-1955, main form | Accepted Bonn witness identities are inventoried; source-owned Pentecost appointments and recorded 181-event CLI/structure/Day/Propers parity | Its thirteen inventoried text slots remain unresolved: zero represented, zero not-represented. The inherited 1962 Proper bodies have no pre-1955 target attestation. Join and collate the bounded witness slots; acquiring an exact Vatican 1920 impression is not a prerequisite. |
| Postconciliar, Day form | Recorded 71-event CLI/structure/Day parity, the entrance-antiphon choice and explicit Day form; date-free Propers retains the two unresolved Gloria/Creed appointments | No bounded Pentecost text-slot report is joined. Establish that scoped source accounting and retain Bible reconstruction, study translation, unavailable Latin and approved-English limits. Acceptance is for a partial-state exemplar. |

The owning checks are `tools/tests/test_ordinary_appointments.py`,
`test_complete_missal_report.py`, `test_proper_text_structure.py` and
`test_ordinary_held_prefaces.py`, with the recorded live parity contract in
`test_missal_exemplar_parity.py`. Structural equality is not wording collation.
The later Ordinary source checkpoint has 120 held Latin occurrences, 118
collated and 97 word-exact; nine Prefaces remain explicitly partial and two
source-only rows uncollated. These are represented Ordinary occurrences, not a
whole-book denominator. C2 and C3 remain in progress until the applicable
acceptance matrix is dispositioned; no independent human acceptance is claimed.
F01 source changes must be regenerated and checked before this snapshot's
results are applied to the merged inputs. Repeat the annual gate when its
consumed calendar, CLI or model inputs change.

#### C3: source and translation completion lanes

- **1962:** recover remaining Latin and historical English against exact target
  slots; collate the 1861 Ordinary's inherited wording and target differences;
  supply exact sung Propers; resolve Common-set selections. Include Holy Week,
  Christmas/All Souls forms, commemorations, and exceptional frames explicitly.
- **Postconciliar:** complete assignments and versification, model actual
  liturgical fragments separately from Bible expansion, review project study
  translations, and acquire/collate target Latin. Approved English requires an
  exact exemplar and a permitted publication route. The existing
  [publication policy](liturgical-text-publication-policy.md) owns that decision;
  a live daily-readings feed is not an arbitrary-date downloadable Lectionary.
- **Pre-1955:** retain honest partial access while joining and collating the
  accepted Bonn witness and historical calendar, with the 1922 Mame conformed
  printing as control. Do not relabel either as the 1920 Vatican impression or
  treat inherited 1962 wording as independent evidence of its ancestor. The
  completed C1 identity inventory does not establish wording agreement.

The existing [participation-aid review record](../src/sources/inventories/day-reader-participation-aid-review-v1.toml)
requires review to begin by **2026-11-15** and complete before **2026-11-29**.
Refresh its evidence before a proposed affected release; this plan records the
existing dependency and supplies no new rights clearance.

##### 1962 Pentecost complete-text plan, 2026-10-19

A read-only lane checked every unit of the 1962 C2 exemplar on page images. The
witnesses are the registered 1962 facsimile (artifact pp. 373, 385–386,
437–439), the 1922 Mame, the 1862 Pustet, Cummiskey 1861 and Lasance.
Public-domain witnesses exist for nearly every unit:

| Unit | What is missing | Route |
| --- | --- | --- |
| Introit, Offertory, Communion | Missal Latin; today a Bible reconstruction | 1962 nn. 1310, 1316, 1318, collated with Mame and Pustet as for the Saturday-BVM chants; `source: mixed`; Lasance English (Cummiskey drops alleluias in the Introit and Communion) |
| Collect, Secret, Postcommunion | English only | Cummiskey 1861 binding, with Lasance as the second reading (G3) |
| Lesson, Gospel | Missal wording ("discipuli"; "Dixit Iesus discipulis suis") and headings | `source: mixed` with the Missal's printed text, collated with Mame and Pustet; Gospel English from Cummiskey or Lasance; Lesson English a typed witness gap |
| Alleluia, Sequence | Inline genuflection and ten strophes | The G14 inline-action and stanza contract |
| Preface | The common opening is hidden, Latin is uncollated, and *hodierna die* is conditional | A span-level join to the common opening; collation of 1861, 1962 and Mame |
| Proper Hanc igitur | Whole body | Mame and Pustet Latin, Lasance English; an Ordinary element needs a non-Cummiskey source |
| Proper Communicantes | Whole body | Head from Mame and Pustet; the continuation clause is blocked (below) |
| Ordinary dialogues | Collation of the 1861 rows against the 1962 Ordo (G19) and per-turn rows (C4) | Element-level collation status |

Rules settled from existing guidance:

- The Missal's own reading text uses the existing `source: mixed` shape:
  scriptural constituents plus the printed full text. No new field is needed.
- A historical English that drops an alleluia or omits a word is a variant
  under the 2026-09-03 rule. It is not bound as the antecedent, and the unit
  carries a typed witness gap naming the loci.

Maintainer decision, 2026-10-19: the 1962 Communicantes continuation's "sed et
beati Ioseph, eiusdem Virginis Sponsi" (decree of 13 November 1962) has no
public-domain witness. It is published as a short phrase. The implementation
records that basis once, citing 37 CFR 202.1(a) (words and short phrases), in
`src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`, where
item 5 was previously "not adjudicated". The decision reaches only that clause;
it is not a general basis for 1962 matter. It applies to the proper and the
common Communicantes alike.

Found along the way:

- `roman-1962/propers.yaml` carries 154 duplicated `notes` keys whose first,
  provenance-bearing value the parser silently drops. Fixing them, and making
  `check-calendar-masses` refuse duplicate keys, is the first implementation
  step.
- The Saturday-BVM provenance rows name Mame as the publication source while
  their evidence text names Pustet.

The ordered implementation is: the duplicate-key fix; G3 English; the chants;
the readings; G14; the Preface; the Hanc igitur; the Communicantes; the G19
slice; then regeneration and the C2 acceptance checks.

Progress, 2026-10-19. All text moved by script, collated word for word and
checked on page images:

- **Duplicate keys.** The 154 duplicated `notes` keys are merged, and
  `check-calendar-masses` refuses duplicate keys in every calendar file.
- **Latin.** The Introit, Lesson, Gospel, Offertory and Communion carry the
  Missal's own Latin as `source: mixed`. The publication witness is the 1862
  Pustet, from its now-tracked leaves, with Mame as the second witness.
  Pentecost Latin is 10/10 exact-target.
- **English.** Cummiskey binds the Collect, Secret and Postcommunion, and
  Lasance the Introit, Gospel, Offertory and Communion. The Lesson is a typed
  gap.
  A 2026-10-20 page-image audit also checked the complete Acts 2:1–11 Lesson
  in [Pace/Wynne 1916, p. 608](https://archive.org/download/TheMassEveryDayOfTheYear/page/n613_w1400.jpg)
  and [a B. Herder 1926 missal, p. 381](https://archive.org/download/missal0000vari/page/n448_w1400.jpg). Both omit “disciples” in
  verse 1, as Cummiskey, Lasance and Lefebvre do; none can supply the recorded
  1962 Latin's English counterpart under the word-agreement rule. [Cabrol
  1921](https://catalog.hathitrust.org/Record/100567132) is catalogued full-view
  but its page image was inaccessible here, so that
  candidate remains unverified and the `witness-gap` stays explicit.
- **Antecedent typing.** Cummiskey and Lasance rows declare the evidenced
  antecedent relation.
- **Saturday-BVM rows** now name Mame as their publication witness.
- **Missal mode** seats the whole Holy Spirit Preface: its opening is joined
  at the 1861 asterisk, and *hodierna die* is marked conditional. It also
  seats the proper Hanc igitur (Mame and Pustet Latin, Lasance English) and the
  proper Communicantes head with the shared 1962 continuation, under the
  recorded short-phrase basis. The common Communicantes carries the same
  continuation. The English of the head and of the continuation are typed
  variant gaps.

- **Alleluia English** is bound from Lasance (printed p. 599), and its
  genuflection is a typed rubric.
- **G14 is implemented.** `text_structure` records hash-pinned stanza and
  inline-action offsets, checked on page images; the Sequence is tied to 1862
  Pustet witness lines. Both entrances and print render strophes and rubrics.
- **Copy** keeps ℣ and drops hidden labels.
- **Mixed units** label their Bible passages "Bible text · edition · not the
  Missal's wording".
- **G19 slice.** The exercised Ordinary is collated against the 1962 Ordo (see
  the gap register).

Remaining: the C2 acceptance checks for the exemplar.

Follow-ups:

- Structure for the other Sequences (Victimae paschali, Lauda Sion, Stabat
  Mater, Dies irae), each checked on page images.
- 102 more projection rows share the Mame/Pustet naming contradiction. The St
  Luke row rests on a weak text-layer reading.
- Six merged notes cite two loci.
- The other four proper Communicantes heads remain.
- The other seven asterisk Prefaces need the opening join.
- A Cena Domini option is still needed.

#### C4: dialogue, typography, and usability contract

The versicle/response work completes the existing distinction between speaker
and dialogue role. A priest may respond and a server may initiate. Do not
derive ℣/℟ from priest/server identity, a Bible verse number, or an unreviewed
string substitution. Preserve protections for abbreviations such as B. V. M.
and Post Communion labels.

- Show **one visible cue per verified turn**. Separate a printed source marker
  from the spoken body in a reviewed presentation derivative. Remove the
  Orate-fratres-only CSS exception once the common representation handles it.
- Place each spoken turn on its own row. Align its cue with the first text
  baseline in a narrow hanging column; continuation lines align under words.
  Group short exchanges without repeated heading or source-locus interruptions.
- Give ℣/℟ one deliberate font, fallback, and readable scale across Ordinary
  and Propers. Preserve speaker identity where it adds information. Use red
  consistently and supplement color with structure and labels.
- Expose one understandable accessible cue with correct language tagging;
  decorative glyphs do not produce duplicate announcements. Test actual
  browser accessibility and selected/copied text, since CSS-generated cues and
  fake-DOM source-parity tests cannot prove those behaviors.
- Use canonical Bible paragraph breaks where available. Supply checked stanza
  boundaries for Sequences and distinct inline-action/rubric structure. Source
  file hard wraps are not poetic lineation. Start with a long Gospel, one
  Sequence, and the Pentecost genuflection rubric.
- Preserve the Instrument's calm ground, dominant celebration, bounded serif
  reading measure, quiet controls, and useful first viewport. Subordinate
  routine provenance and page loci to Details while retaining qualifications
  needed to understand the displayed text.
- Pair bilingual text by corresponding fragment: readable columns on wide
  screens and adjacent stacked fragments on narrow screens. Missing translation
  leaves the original visible with its precise absence.
- Keep Previous/Today/Next and direct date access reachable without full
  configuration. Present authorized celebration choices as distinct touchable
  rows with short explanations; do not choose one by incidental ordering.
- Complete source-owned current-place orientation and Contents centering;
  preserve focus and semantic location through auxiliary surfaces and state
  changes. Provide practical text enlargement, share, and print controls.
  Remember valid preferences below explicit URL state; infer no territory.
- Print the same semantic sequence with independent identity, source, and
  coverage context. Keep cues with their text, avoid stranded headings, and let
  long readings and Sequences paginate instead of imposing blanket no-break
  treatment on an entire Proper.

Repair the demonstrated opening-cue loss first. Then prove one visible cue on
Confiteor, Suscipiat, and postconciliar Orate fratres before extending checked
turns through Introibo/Judica, Sursum corda, Pax, and dismissal. Preserve
language-local turn boundaries, source text, and event order throughout.

Progress, 2026-10-19: the opening-cue loss is repaired. Ordinary turns may
declare a generator-validated `printed_marker`, so each verified turn of the
Confiteor, Suscipiat and Orate fratres shows one visible cue; the
Orate-fratres CSS exception is removed. The [work register](../PROJECT-WORK.md)
records the evidence. The next extension is recorded below.

Step 2, 2026-10-19:

- **Turn rows.** Introibo/Judica, the Preface dialogue, the Pax and the
  dismissal are held as reviewed child rows of the 1861 artifacts, one per
  printed turn, under new derived artifact identities. The originals stay
  unchanged, as `guidance/sources.md` requires. Each language partitions the
  rows with speaker and `printed_marker`.
- **Roles.** A ℣/℟ role stands only where the 1962 typica prints the mark at
  that turn (nn. 1015, 1080–1081, 1118, 1131–1132). The Judica verses, printed
  S./M., carry speakers only. A partition that declares a role must state its
  basis.
- **Postconciliar.** The Latin antecedent Preface dialogue takes its roles from
  the 2002 Praefationes; the Pax (n. 127) has speakers only. Both are split the
  same way. The Orate fratres roles, which had no printed basis, are reviewed
  under the same rule.
- **Headings.** Reviewed incipit markers keep P./R. out of element headings.

Remaining at that checkpoint:

- twenty opaque dialogue blocks;
- ℣/℟ typography;
- the postconciliar dismissal, which has no sourced text.

Further source-fragment work on 2026-10-20 completes the explicit twenty-block
1962 mixed-speaker scope: Adjutorium was already divided, and the remaining
nineteen now partition 38 language-local parent cells into 97 source fragments.
Ten immutable 1861 derivative artifacts preserve the exact parent words;
independent 1962 page evidence controls dialogue roles. The three English Kyrie
translations are explicit nonspoken source glosses with their own note semantics;
Latin retains its three acclamations. No turn-index pairing is implied. The
196-element order, event identities, rights, coverage and target qualifications
remain. Source-only Postcommunion gains no target placement. Pre-1955 stays
outside this slice. Postconciliar doxology now has checked speaker spans;
Pater noster retains its source-only Amen and an explicit extent qualification,
with target turn mapping still unresolved. The integrated browser probe passes
36 checks, including real native copy and AX trees. Representative AT, literal
desktop 400% zoom, complete print composition and independent acceptance remain
open; this bounded result is not all-Ordinary completion.

On 2026-10-20, Ordinary absence rows gained short source-owned reader labels.
The Day preamble and silent elements now show those labels with the existing
typed state, while the internal keys remain in generated data. This closes the
key-only wording portion of G15; repeated absence notices and other G15
presentation work remain open. A print-only C4 pass lets long Proper witness
accounts paginate, keeping headings and short prayers together; 1962 Pentecost
English Read fell from ten to seven pages in both entrances with the extracted
text unchanged. Long notes still need mode-aware print composition.

The G16 translation-witness chooser now stands beside its first Proper and
names its Mass-wide scope. It retains all source-supported partial witnesses
with their coverage counts, and a focused Pentecost Chromium regression
confirms that selecting Caswall leaves the Introit's English gap explicit
while holding its Sequence in both entrances. The control no longer suggests
that every offered witness supplies the Introit.

The first C5 core-preference slice now shares missal, Bible and oration-language
choices across Day and Propers. An explicit URL still wins; a malformed or
unavailable stored value falls back to a valid repository default, and only a
successful Date or Browse Apply saves a new preference. The older Propers
record remains readable for migration. Date, territory, Mass, form and witness
choices are never remembered. Dedicated source-served Chromium checks passed
11/11, with the existing Day and Propers suites passing 55/55 and 49/49.
Propers Missal, Study, Compare, search and independent C5 acceptance remain
open.

Further feature-branch work on 2026-10-20 adds a source-seated Propers Missal
view. Its semantic event list combines the selected Proper appointments with
the selected Ordinary, including source-authored exceptional frames and explicit
date-unknown applicability. Read and Missal share semantic locations, with
Ordinary language and option choices carried in the URL. The 1962 Pentecost
fixture has 179 events, comprising 163 Ordinary events, six divisions and ten
Propers. A source-served Chromium run passed 56 Propers assertions. Independent
source-served QA passed nine responsive, keyboard, mode, URL and print checks,
including a same-document deep-link repair. This is a C5 implementation slice,
not acceptance of the whole mode set or public release.

The same checkpoint adds a form-qualified, public-safe Proper search index and
a two-side semantic Compare core. Their browser controls remain open. A bounded
form-slot report now gives source-inventoried expectations without treating
them as whole-book totals: the 1962 Pentecost Day slice has 13 expected and 13
represented appointments, while its whole-form extent and all 39 whole-family
completeness cells remain unresolved. A source-printed 1962 final `Deo gratias`
response now has its English and Latin dialogue role. Neither the structural
slot joins nor Bible reconstructions assert word-exact Missal wording.

The next source-served C5 checkpoint exposes the form-qualified search in
both Propers entrances and loads its index only on a query. Day Compare
resolves both calendar outcomes independently for an explicit date and shared
territory; Propers Compare holds one date-independent formulary and Bible while
adapting two oration languages. Paired functional slots distinguish a missing
event from unavailable text, and mode/location links round-trip. Chromium
passed 10/10 Day Compare and 63/63 Propers Read/Missal/Search/Compare checks
after the latest source regeneration. All seven registered built-preview
browser harnesses pass. Study, independent visual acceptance,
and the full C5 scope remain open.

The Study continuation keeps Read source text and semantic event IDs in place
and attaches calendar, coverage, source and availability context. Day's
source-served Study probe passed 10/10; Propers Read/Missal/Search/Compare/
Study passed 66/66. Day `mode=study&ordinary=0` is live, while explicit
`ordinary=1` still reports a deferred state. All seven registered built-preview
browser harnesses pass after integration; independent C5 acceptance remains
open.
Independent private-preview QA found and corrected three print fragmentations,
a 400% Day Compare Contents landing and a modal focus-wrap gap. The refreshed
visual harness passes 30/30 against the verified preview. Day Study print is
ten pages, Propers Study eight and Day Compare twelve; further C4 composition
and the complete C5 acceptance matrix remain open.

The committed `eb8ac428b` preview's C6 lab sample measured 12.5–12.9 s
narrow cold LCP on Slow 4G and 4× CPU, against the 2.5 s target; warm narrow
and desktop cold samples passed. The 1962 Proper structure is about 1.23 MB
gzipped and dominates transfer. The selected-Mass change at `f671358ba`
generates one catalog and 491 exact Mass files. Eligible settled 1962 Read
links on both entrances fetch only the catalog and selected Mass; other modes,
unresolved choices, cross-Mass references, and invalid split data use the
monolith. Generation and public-preview gates prove all 491 Masses reproduce
the source structure and pass the same public-data rights scan. Seven built
Chromium harnesses and the verified private preview pass.

The same two-run lab profile now records 7.68–7.74 s cold mobile Day LCP
and 7.01–7.02 s Propers LCP, with transfer 319 KB and 269 KB respectively;
the prior samples transferred 1.49 MB and 1.43 MB. Day uses the same resolved
Mass with its safe derived-choice URL, without explicit `mass=`. Cold desktop
LCP is 0.69–0.75 s. These are local samples, not field percentiles, and the
mobile 2.5 s gate still fails. Further startup and request work, independent
C5 acceptance, full print/accessibility review, and release verification
remain open. No production deployment has been made.

The following C5 checkpoint adds shared Mode-radio keyboard behavior and
secondary Share/Print actions on both entrances. One selected radio is in the
Tab order; Arrow, Home/End, Enter and Space use controller-owned choices.
Share sends the canonical reader URL and identity title with the comparison's
actual peer edition or language. It sends no liturgical text and offers local
copy when native sharing is unavailable. Print invokes the browser dialog and
omits these controls. Eighteen real Chromium keyboard checks and all seven
built browser tests pass; this remains an internal C5 slice.

Safe 1962 Read catalog loading now overlaps existing manifest/rubric requests,
and the selected Mass loads concurrently with its validated catalog. The same
two-run Slow-4G/4×-CPU lab profile records cold mobile LCP at 7.34–7.35 s for
Day and 6.36–6.37 s for Propers, with about 325 KB and 274 KB transferred.
Cold desktop samples are 0.60–0.70 s. The 2.5 s mobile gate still fails; these
local samples establish neither field p75 nor independent release acceptance.

The following C5 usability slice exposes Study directly in the fourth dock
position on both entrances. Details moves into Mode while retaining source,
Share and Print access. Direct Study preserves semantic place and returns
focus to its command; secondary Details returns to the visible Mode invoker.
A native 100–200% text-size control preserves place/focus, stores only valid
display preferences, works without storage, and leaves print independently
sized. Integrated focused Chromium probes pass eighteen keyboard checks,
twelve direct-Study checks, three enlargement cases and four Share/Print
cases, including reduced-motion surface transfer and clean diagnostics.

Compact Study facts and paired Compare print columns retain source/coverage
context, unavailable-side protection and a complete final pair. Checked page
counts are now 7/9/7/6 for Day Study, Day Compare, Propers Study and Propers
Compare, formerly 10/12/8/9. Extracted content parity and representative page
rasters were checked. Full C4 print composition, the broader C5 modes and
independent acceptance remain open.

Retained-oracle dependency correction, 2026-10-20: extracting Day mode
bindings into the existing `day-study.js` helper required that helper before
`day-reader.js` in `reader-visual-reset-day.html`. The old dock, labels, DOM
composition and visual CSS are preserved. Guarded Study-marker updates also
permit a shell without the new Study dock command. The protected HTML hash
now records this one-script dependency repair; the 30-check visual suite
passes. This records a changed dependency baseline, not external re-acceptance
of the earlier prototype.

Retained-oracle source-choice dependency exception, 2026-10-20: the maintainer
authorized one `source-choice-controls.js` include immediately before
`reader-shell.js` in each retained Day and Propers oracle. The dedicated helper
owns the existing native source choice controls and restores the unchanged
18 KiB shell cap. The prior Day Study and current Propers events dependencies
remain. Hash guards remove only this new include and, where already specified,
the earlier Day Study include before comparing the unchanged original hashes.
Every other oracle byte and all earlier frozen packages remain preserved.
This dependency repair and its source/DOM checks do not confer browser, visual
or independent C7 acceptance; the combined r4 revision requires separate review.

The next internal C5 slice supersedes the explicit Day Study Ordinary defer:
`mode=study&ordinary=1` now uses the existing full Missal renderer, attaching
the same source/coverage facts to its semantic events. Seven full-order
fixtures preserve text, order, branches, choices, absences and coverage;
mode changes preserve semantic place and map to the nearest Proper in Read.
The expanded Day Study Chromium probe passes 25 checks, including explicit
missing-resource refusal.

Propers Compare also supports explicitly selected held lectionary cycles
within one formulary. The Transfiguration A/B/C Gospel fixture holds edition,
form, Bible and languages fixed. Its text remains a Bible reconstruction,
without exact-Missal-wording or civil-year-applicability claims. Eight contract
checks and eight Chromium checks cover coequal selection, invalid or equal
peers, source boundaries and state cleanup. Compare print now keeps a source
credit with the preceding text tail while long readings still paginate.
These are internal capabilities; remaining comparison axes, the full print
matrix and independent C5 acceptance remain open.

The following C6 startup slice adds bounded response hints immediately after
the shared browser core on the four modern entrances. Explicit eligible 1962
Read links use the core's existing data-root policy; normal loaders still own
generation, identity, rights and fallback validation. Ordinary presentation
code loads only for validated state that requests it, including Day Study with
the Ordinary. Shared requests, explicit failure/retry and render-serial guards
preserve selection ownership; retained eager visual oracles remain supported.
Focused Chromium probes pass nine hint checks and eleven Ordinary-loading
checks with no unexpected diagnostics. Deferring the code can add a request
after validation on the first Missal visit. Timing evidence must describe that
tradeoff and the exact transport/artifact separately from semantic parity.

Two cold HTTP/2 samples per entrance on the frozen C9 baseline and combined
startup candidate use 562.5 ms latency, 1.47456 Mbps down and 4× CPU. Day LCP
changes from 5.328/5.360 to 4.600/4.668 s; Propers from 4.552/4.368 to
4.000/3.880 s. Transfer is 330,659 → 303,215 bytes and 280,651 → 253,210 bytes.
The earlier 7.34/6.36 s samples used HTTP/1.1. State, text and semantic hashes
agree; diagnostics are clean. One first Day Missal switch costs 9.322 rather
than 8.650 s, with 29,252 code bytes deferred to that action. The chosen All
Souls/Caswall Propers baseline refuses Missal, so it yields no valid switch
timing comparison. Field p75 remains unmeasured and the 2.5 s cold mobile
target still fails.

The following internal C5 slice compares the Presentation Gospel's source-held
longer Luke 2:22–40 and shorter Luke 2:22–32 options by their explicit IDs. Other
axes remain fixed; source choices are retained and no date applicability is
inferred. Eight Node checks and six Chromium checks cover selection, invalid
peers, place/focus, narrow pairing and print. The All Souls/Caswall Missal
refusal found in timing is corrected by passing the already loaded Ordinary
to its Proper-witness probe. Five Node and four Chromium checks preserve the
held Sequence, per-Proper witness gaps and independent Ordinary language.

The next C6 payload slice extends the existing exact Mass projection to
conservative 1962 Missal and Day Study-with-Ordinary states with explicit Latin
orations. Cross-Mass dependencies, commemorations, choices/forms, exceptional
frames and other languages keep full-source loading. Five durable test groups
cover 2,044 exact state/result comparisons; forty Chromium groups preserve
text, semantic events, source/coverage, controls and races. Existing Read
requests/results match across 365 dates and 491 Masses. Gzip6 Proper bodies
become 41,404 bytes for the Tenth Sunday or 51,149 for Pentecost instead of
1,225,510; an eligible Read→Missal transition reuses already held Proper data.
The complete Ordinary stays separate. No new latency, field percentile or
independent release acceptance follows from these byte measurements.

Latin accompaniment candidate: the optional `text-display=latin-and-selected`
presentation pairs held prayer and Missal bodies at the existing Proper/cycle/
Ordinary-element boundary on both entrances. It preserves primary selection,
source absences, and semantic event order. Selected Latin appears once; Compare
retains its existing axis and stacks internal language pairs. Scripture remains
one selected Bible unless the separate companion selection below is requested.
No stanza/turn correspondence is inferred. Source-owned subfragment alignment
and independent C4 acceptance remain open.

Latin Bible companion candidate: optional `scripture-companion=clementine-vulgate`
adds independently addressed Latin and primary selected Bible text at each
citation in both entrances and all modes. Each side retains its language,
edition witness, numbering, rights, reconstruction qualification and precise
refusal. Primary semantic selection and all Compare axes stay fixed; one selected
Latin edition appears once. This supplies citation-level bilingual presentation
using the existing held text and loci. It establishes no finer verse/stanza/turn
correspondence and no exact Missal wording from a Bible reconstruction.

The same shared-capability checkpoint adds explicit Propers translation-witness
and Bible-edition comparison. Both sides retain exact source-occurrence IDs,
form membership and unique hooks; All Souls Sequence can pair despite lacking a
cross-edition functional slot. Partial Caswall/Cummiskey gaps remain one-sided,
and Bible cells separately record coordinate refusals with their precise reason.
Independent numbering conversion, source qualifications and unchanged primary
Compare axes are covered by the combined 63-check Node run and four feature
browser wrappers. Cross-edition comparisons retain their strict slot guard.

Bounded print composition keeps source directions/headings with their next short
Ordinary text, and short paired bodies with their own source accounts. Long
Scripture/stanzas remain free to paginate. Repeated beforeprint, afterprint and
reader rerendering preserve event IDs and restore the original screen DOM.
Current-input ordered PDF text is preserved; final frozen all-page review remains
pending. The cumulative declared script/style gzip6 increase against
`aa39475c5` is 9,252 bytes for Day and 10,645 for Propers, with 29 direct resources
each. These measurements do not establish latency or independent acceptance.

Further source work on 2026-10-20 adds three independently identified Mame
1922 Latin prayer bodies to existing English-only elements, preserving the
196-element frame and source-specific Cummiskey absence findings. Overall
Latin availability becomes 120 held / 76 missing; English remains 186 / 10.
The optional additive inventory join requires a source-owned exact turn
partition and basis for every spoken side, so Latin cannot inherit an English
actor. Munda's priest attribution is limited to the express Low Mass reuse;
Per evangelica retains independent Latin Priest and English priest-with-
assistants assignments. Its separately checked English one-turn partition
exposes the source All cue without changing words or adding a dialogue role.

Eleven bounded Latin collation findings cover the Common Preface, Trinity,
eight other held Prefaces and the common Hanc igitur. Only Common and Hanc gain
new word-agreement findings. The nine partial Prefaces keep their literal cues,
variants and unassembled opening/conclusion limits, without a whole-row
target-wording grade. No new Trinity opening event is added. The source-only
Gloria heading and unplaced pre-Postcommunion greeting remain uncollated.
These are source-qualified implementation slices; complete corpus wording,
source-owned finer bilingual alignment and independent C2–C6 acceptance remain
open.

The next frozen HTTP/2 lab run measures eligible first Missal transitions at
1.94 s for Day and 1.92 s for Propers, compared with 9.35 s and 9.29 s before
exact-Mass reuse. Final transitions transfer no additional Proper body. On the
same 562.5 ms latency, 1.47456 Mbps down and 4× CPU mobile profile, cold Read LCP
remains 4.644/4.664 s for Day and 3.916/4.116 s for Propers. The 2.5 s release
target and field p75 remain open.

A separate two-year early-loading pilot records 3.488–3.532 s Day LCP, with
1.144–1.176 s gains across four adjacent pairs. All samples fail the unchanged
3.0 s pilot integration limit. It remains outside the branch; the proposed
101-year expansion is held. Helper completion near 1.89 s and authenticated
sidecar admission near 2.77 s identify the remaining network path. Exact Mass
and chapter hints have one body each, but Bible metadata has two. Text, state,
semantic events and URL parity pass with clean diagnostics; these findings do
not turn the failed value test into acceptance.

The following bounded startup candidate loads shared Compare/Study presentation
APIs through the existing validated-state optional loader. Read and open Mode
request neither; Compare and Study await only their own modules. Per-resource
requests, initialization validation, retry and stale-render guards preserve
the current mode, place and invoking-control focus. The main controllers and
eager visual oracles stay byte-identical. Ten Node contracts and 23 Chromium
groups pass on the scratch candidate. Direct script/style gzip6 sums become
192,881 bytes for Day and 160,850 for Propers, saving 12,079 and 12,098 bytes
respectively, with 26 initial resources. Integrated preview/integrity checks,
all seven full browser tests and 205 focused tests pass (one separate browser
opt-in skipped). After correcting the caller's locked-dependency PATH, the
full repository check passes 250 example replays with zero divergence or
tracked writes. Latency remains pending; byte savings alone do not establish
a performance result.

A twelve-sample HTTP/2 follow-up holds this checkpoint constant across the
committed build, original early-loading pilot and two-HTML priority revision.
Day LCP medians are 4.582 / 3.442 / 4.092 s on August 2 and
4.600 / 3.452 / 4.100 s on the independent September 5 fixture. Native Low
body priorities are honored, but delay core/controller completion by about
one second; the second Bible-metadata request then determines readiness.
The revision fails both unchanged value conditions and stays off branch.
Text/state/events/URL and response identities match; diagnostics are clean
and all experiment processes close. The original pilot also remains outside
the 3.0 s integration limit, so its 101-year expansion stays held. Removing
the duplicate Bible wait alone cannot meet either the original integration
limit or the 2.5 s release target. Future work must address the measured
serial data path or competing transfers rather than repeat priority guesses.

A subsequent initial-HTML scratch prototype combines the canonical resource
owner, private Day startup policy and authenticated two-year dispatcher in
3,986 gzip6 bytes, with 280 bytes of complete CSP/authentication metadata.
Its final generation passes 2,770 actual-kernel topology/fault checks,
14,452 facade comparisons, 66 build-boundary checks and 43 browser groups.
The narrow Bible handoff preserves independent parsing and normal admission.
The derived head exception applies only to the two Day pages; authored inline
scripts remain refused and stricter header CSP retains external fallback.

Its eight cold HTTP/2 samples nevertheless fail: baseline/inline LCP medians
are 4.574/9.726 s on 2026-08-02 and 4.586/9.710 s on 2027-09-05. Directed data
finishes by 2.52 s, but the fifteen normal scripts are discovered serially
and the controller finishes near 9.58 s. There is no Proper-monolith fallback
or duplicate body. Exact reader parity and all 108 response identities pass,
with no diagnostics or foreign browsers at sample boundaries; run, analysis
and teardown pass. An excluded first baseline preserves its process-census
harness failure and the bounded parsing repair. The candidate stays outside
the branch, with both performance thresholds and the 101-year hold intact.
[Chromium's scanner source](https://chromium.googlesource.com/chromium/src.git/+/c5542734590fdc1427ddf14171904c7a7ea13b0d/third_party/blink/renderer/core/html/parser/html_preload_scanner.cc)
supports a CSP-meta discovery explanation when its experimental preloading
feature is disabled; that installed-browser causal attribution is not yet
isolated. One scratch revision will derive native preloads for exactly the
existing Day body scripts, preserving execution order, attributes and
priorities. Runtime/kernel/table bytes remain fixed; complete HTML growth,
browser behavior and measured value require fresh evidence.

The derived-preload revision passes 58 static checks and 44 browser groups;
all fifteen scripts retain one response and their original execution order.
Complete Day HTML grows by 93 gzip bytes, its alias by 92. The subsequent eight
cold samples restore concurrent script discovery and measure LCP medians
3.054/3.072 s against 4.600/4.594 s. All gains exceed 1.5 s, but every candidate
still fails the unchanged 3.0 s integration and 2.5 s release limits. Table
responses near 2.27 s precede directed data near 2.96–2.99 s; core/catalog
completion competes on the same path. Exact reader and script/data reuse
checks pass, with late icon-event coverage explicitly qualified. Preflight,
probe, analysis and teardown pass. The revision remains outside the branch.
A bounded lossless catalog/private-presentation prototype must first prove
its complete net byte reduction and source/API contracts; it has no measured
value or 101-year rollout authorization.

The lossless catalog/private-presentation prototype now has fresh paired
source/generation evidence with the separately committed Text Size fix on both
sides. Both actual-kernel proofs pass (5,540 checks total), and four complete
45-route ledgers save 18,574–18,577 gzip6 bytes within the unchanged kernel
and authentication caps. All 84 browser groups pass, including ten inspected
Retry focus images, fourteen native completion records and the previously
failing 200% text-size control. An earlier 39/84 supplemental-harness setup
failure and its exact four-tree comparison repair remain separately preserved;
complete five-tree admission and the full assertion matrix remain intact.

Its eight cold HTTP/2 samples nevertheless fail the unchanged value gate.
Against committed runtime `a29df844d`, baseline/candidate LCP medians are
4.590/3.032 s on August 2 and 4.596/3.030 s on September 5. All four gains exceed
1.5 s, but all four candidates miss 3.0 s by 16–48 ms and the 2.5 s release
budget by 516–548 ms. Exact reader and response/reuse checks pass; diagnostics
and foreign-browser boundaries are clean. Preflight, probe, analysis and
closure exit 0 with all experiment resources closed. The prototype stays
outside the branch, the full-span expansion remains held, and the thresholds
are unchanged. This C6 failure does not block final C1–C5 review of the verified
committed reader, including fresh artifact-bound visual, zoom and print checks.
The measured candidate has 46 bodies over 45 unique routes because the icon is
fetched twice (229 extra gzip bytes). The staged route-ledger net remains
separate from complete measured transfer; there is no paired timing proof of
R2 icon multiplicity. Required data, script and Bible bodies remain unique.

The first committed-artifact review subsequently identifies a real desktop
Compare/rail collision on both entrances. The eight native 400% cases pass,
but their 48 inspected images expose the 100% baseline problem; the 88-image
matrix confirms six affected wide Compare frames. A screen-only wide-layout
rule reserves the existing rail and limits Compare to available viewport
space, preserving its 70rem cap where it fits. Paired-language and narrow
layouts retain their existing rules. The focused browser test reproduces seven
rendered-text collisions before correction and passes afterward; all 33 full
visual assertions, default registry checks, preview build and integrity checks
pass. These captures remain diagnostic, with final source-frozen screen/print
review and independent acceptance still required.

Native Chromium browser zoom is now verified for one Day Read smoke on the
existing C29 artifact: the API reports 400% within conversion precision,
physical window/pixel dimensions remain fixed, CSS width quarters and DPR
quadruples without emulation or CSS scaling. Contents and Mode pass after
observed smooth-scroll settlement; four images are inspected and diagnostics
and handles are clear. Two prior harness failures remain recorded. The
[registered native-zoom test](../tools/tests/test_reader_native_zoom.py)
preserves the eight-case entrance/mode matrix with an explicit artifact-bound
opt-in; two default tests pass and the expensive browser test is skipped.
Fresh final-artifact execution and every-image review remain pending, along
with representative assistive technology, manual touch and independent WCAG
and product disposition.

The final ritual-flow evidence audit preserves the planned 88 images and adds
44 existing named representatives absent from that plan: sustained Roman and
postconciliar reading, Why and territorial views, typed partial/Browse states,
and current Contents geometry through deep, narrow and enlarged-text states.
Historical captures have different consumed inputs. The registered visual test
helper exposes the same source-owned fixtures and capture/measurement functions
for a selective artifact-bound adapter, with its default CLI behavior retained.
Eleven offline adapter checks pass; no final images or acceptance follow from
this preparation. Current-row centering or proved boundary clamping, focus,
inertness, source parity and every-image inspection remain required.

#### Print attachment correction and startup experiment boundary, 2026-10-20

The narrow print repair uses the actual Letter content width during native
`beforeprint`, scopes measured Compare keeps to a short responsorial Psalm,
and attaches Study evidence to its selected language's tail and source credit.
The preceding companion language may paginate independently; a whole paired
Ordinary element is not kept together. The rejected broad keep candidate's
173 Study pages and 37 nonfinal pages ending above 400 points remain a failed
result. The narrower three-PDF proof has 143/9/4 pages, all 156 individually
inspected, with passing attachment and 400-point pagination checks. Ordered
semantic DOM and text-character multiset parity hold, while column extraction
order and page counts can change. Both rerender/late-`afterprint` orders restore
the exact screen DOM. Seven registered browser groups now include real PDF
regressions; the final frozen eight-PDF review remains required.

For the next source-owned plain-JSON startup experiment, the complete inline
kernel's experimental ceiling is **4,500 gzip6 bytes**. The reviewed 4,333-byte
kernel still fails the historical 4,000-byte ceiling by 333 bytes; no earlier
experiment is relabelled as passing. One source-owner reuse investigation
reduced the kernel from 4,382 to 4,333 bytes; further legacy annual-sidecar
machinery is excluded. The extra 333 bytes cost about 1.8 ms at the lab's
nominal bandwidth, against a frozen-input composed reduction of about 13 KB.
Those byte estimates justify testing this bounded architecture, not a latency
claim. Actual composed HTML, payload, runtime, and response multiplicity must
all be charged again after current source and accessibility changes.

The complete authentication ceiling remains 300 gzip6 bytes; the pilot's
plain-JSON payload ceiling remains 128 KiB. Initial Read savings must remain at
least 18,000 gzip6 bytes after a 512-byte reserve. The 3.0-second / 1.0-second
gain integration gate and 2.5-second release budget are unchanged. The naive
101-year inline envelope exceeds the pilot bound, so full-span generation is
held for an explicit source-owned size/architecture decision and passing pilot
value evidence. Exact canonical data-root identity gates speculative warming;
different custom roots skip these optional hints and retain normal loading.
Publication copy eligibility and actual artifact fragment bytes must agree
through the canonical owner before any generated experiment can be accepted.

### Verification and completion gates

The integrated 2026-10-20 source checkpoint passes 80 focused source tests,
the stable Ordinary shell contract, 44 Chromium dialogue groups (38 actual
AX-tree and native-copy records each), all seven full browser tests, 217
static tests, source/publication checks, preview integrity, and the final full
`make check` replay (250 examples, zero divergence or tracked writes). The
prior three-calendar, 365-date annual module passed 4,380 matrix renders plus six language sentinels. Its
broader worktree-freeze wrapper remains failed because two example-count
constants were edited during the run; an independent full-blob audit confirms
unchanged consumed CLI/source/data inputs and executable AST. This is a
qualified historical annual result, not a pass of that broader wrapper or of
the current four-interval annual gate. Final print,
performance and independent acceptance remain open.

Recovery checks actually run on the baseline:

| Command or check | Result and limit |
| --- | --- |
| `python3 tools/complete-missal --check` | Passed report validation; 39 completeness dimension cells remain unresolved. |
| `python3 tools/mass-propers census --json` | Produced the source-identity census used above. |
| `python3 tools/mass-propers structure --check` | Four tracked generated files current. |
| `python3 tools/mass-ordinary coverage --json` and `python3 tools/mass-ordinary check` | Coverage measured; generated files current. |
| `python3 tools/check-calendar-masses check` | Passed with the declared Psalm 56:14 exception. |
| `python3 tools/calendar-days coverage --first 2026 --last 2026 --json` | All 365 dates reach some Mass in each family; no text-completeness claim. |
| `python3 -m unittest tools.tests.test_day_missal_switch tools.tests.test_liturgy_reader_state tools.tests.test_day_missal_integration` | 95 tests passed. |
| Focused Ordinary renderer checks | Three existing semantic/rendering tests passed; an additional harness probe reproduced the two initial priest-cue losses. |
| Live Chromium diagnostic views and deployed script comparison | Observations and byte match recorded above; no complete browser, accessibility, or print acceptance claimed. |

Implementation gates extend these existing tools and fixtures rather than
creating a second liturgical resolver. Run affected source, rights, generated
data, and seating checks; the opt-in 5,856-render four-interval year matrix; Sunday A/B/C
and weekday I/II selections; Holy Week; multiple-Mass days; commemorations;
territorial choices; long/short alternatives; and every distinct absence.
The current four-interval year matrix has not been run. The earlier 4,380-render
results above belong to the superseded interval/calendar matrix.

Its existing opt-in invocation is:

```sh
TRIPTYCH_COMPLETE_MISSAL_YEAR=1 \
  python3 -m unittest tools.tests.test_complete_missal_year
```

The UI matrix includes both entrances, every delivered mode, deep-scroll
navigation and each auxiliary surface, at 1440×900, 1024×768, 768×1024,
393×852, and exact 320 CSS pixels; 200% text and 400% zoom; keyboard, touch,
representative screen readers, forced colors, and reduced motion. Assert
identity, unit order, text/source status, focus, location, URL, overflow, and
console/network outcomes. Exercise actual copy and accessible-name behavior
for crossed speaker/role turns and duplicate-marker regressions. Inspect every
page of representative short, long, bilingual, partial, and comparison print.

Use the vision's WCAG 2.2 AA and measured performance budgets. A current-state
audit or a passing static test is not independent visual acceptance. Prepare
fresh evidence under the [external-review protocol](external-review-handoffs.md)
for the implementation milestones that require it; record blocker dispositions
in this roadmap and reconcile the existing deliverables. Verify exact outgoing
objects, release bindings, artifacts, and the deployed revision at release.

### Execution order and next action

C1's coverage vocabulary and denominators are implemented within their
inventoried bounds. The next acceptance checkpoint is **the audited
representative-Mass pattern for each principal missal**, including full
event-ID parity, source and absence review, and browser/print evidence. Expand
C3 and C4 in tested slices while C5 uses those same text, turn and coverage
contracts. C6 accepts only a named, independently reviewed scope. Additional
recension expansion must not delay repair of the daily reader's current claims.
The planning deliverable does not close ritual-flow, corpus, or full-product
requirements. Resume through this section and the current source tree, not
the historical takeover commands below.

## Historical deployed baseline, 2026-08-03

Baseline date: **2026-08-03**. The unchanged production-browser and deployed
review baseline is `18256c51e72099b64bb1b9a6b17db9b6257e7ebf` (`Add Proper
placement notes`). The governing documents were committed at `bc7de4114`, the
external-review protocol at `4236f21bf`, and this execution record includes the
subsequent five-blocker correction disposition recorded in the progress ledger.

The current product has two public routes:

- `liturgy/day.html` resolves a civil date through generated calendar and
  rubrics data, then renders one or more readable formularies either directly
  or seated in a generated Ordinary.
- `liturgy/index.html` selects a missal, type, and formulary and renders its
  ordered Propers independently of a date.

The pages use generated manifests and structures for Bibles, calendars,
rubrics, Propers, and Ordinaries. `assembly-model.js` supplies shared calendar
resolution; `ordinary-seating.js` supplies shared seats and semantic Mass
events to browser and CLI paths; `browser-core.js` supplies shared text and
Proper rendering. The pages share the Reading Missal stylesheet and generated
Contents module, but retain separate HTML shells and orchestration scripts.

At this baseline:

- Day discovers public missals from the rubrics manifest, currently
  postconciliar and Roman 1962. The Propers manifest also exposes the
  calendar-independent `roman-pre-1955` formulary projection.
- A first Day visit uses today, the first repository-provided rubrics-manifest
  entry, the first Bible-manifest entry, Latin orations, Read-like
  Propers-only output, and visible-rubric state if the Ordinary is later
  enabled. A first Propers visit uses the manifest default and then the first
  available type and Mass. Neither route remembers preferences.
- URL hashes already carry most selection state, and a valid Propers deep link
  renders immediately. Existing hash semantics are a compatibility asset.
- Settings, Notices, and Contents are native, initially closed document-flow
  disclosures above the reading. Date navigation is inside Settings.
- Contents is generated from the rendered DOM. On Day with the Ordinary off it
  contains only `Beginning`; with the Ordinary on it lists Ordinary divisions
  and seated Propers. It does not track the current location.
- Day can render a complete semantic Mass event stream, display calendar
  resolution and source details, and add source-backed mechanical placement
  notes to seated Propers. These scholarly features do not yet share one
  interaction model and are not present consistently on Propers.
- Print removes interactive chrome and paginates the rendered reading, but it
  prints whatever apparatus and repeated unavailability material is present in
  the reading DOM rather than composing a deliberate print edition by mode.

This description is evidence, not a default contract. The intended defaults
are those in the vision.

## Deployed review, 2026-08-03

The retained Phase 4–9 reports, measurements, screenshots, and print artifacts
support review at 1440×900, 1024×768, 768×1024, and 393×852 across Settings,
Notices, Contents, Propers-only, Ordinary, Why, Roman 1962, postconciliar, and
print states. The retrospective external-review package contains no matching
320-pixel capture or measurement report and no artifact supporting the former
34-page current-print claim. Those exact figures are not treated as retained
baseline evidence; 320-pixel reflow remains a future acceptance gate.

Evidence-backed findings:

- The closed default reflowed at every width with no horizontal page scrolling.
- At 393×852 the Roman 1962 first view contained the celebration identity and
  real liturgical content.
- Opening Day Settings at 393×852 made the form consume most of the initial
  screen and turned common date movement into part of a large configuration
  task.
- Day Contents in Propers-only output contained one item, `Beginning`; it is not
  yet useful navigation for the default mode.
- Propers Contents correctly listed its eleven rendered semantic destinations,
  but it remained a document-flow list and did not report the current unit.
- Roman 1962 and postconciliar Ordinary states had no horizontal overflow, but
  repeated unavailable-text messages became more visually prominent than the
  liturgical hierarchy. The postconciliar populated Notices state also placed a
  large availability message before the reading.
- Retained Letter print was mechanically usable and removed chrome, but the
  screen DOM's repeated withheld-text and source-detail material still needs a
  mode-aware print hierarchy, not only print CSS hiding controls.

## Critical assessment

### Strengths that must not regress

- The celebration or formulary title is the dominant page identity.
- The default page is calm and text-led, with restrained controls and useful
  first view on desktop and mobile.
- The reading measure, line height, continuous vertical flow, responsive
  reflow, and current print legibility provide a strong foundation.
- Day derives calendar decisions from generated source-backed structures and
  preserves competing celebrations, dispositions, cycles, choices, and
  unresolved states.
- Shared event traversal and seating already give browser and CLI a semantic
  parity boundary.
- Propers and Day already share Proper rendering, Reading Missal vocabulary,
  and stable URL-driven selection.
- Missing, withheld, and unsupported text is explicit rather than silently
  replaced.
- Existing tests protect event order, rendered text, URL behavior, focus on
  Contents jumps, print hiding, duplicate IDs, console cleanliness, and
  horizontal overflow across representative widths.

### Problems the redesign must solve

Reading Missal v1 is a successful baseline, not the final product. Settings,
Notices, and Contents are currently document-flow disclosures rather than a
mature reader shell. Common date navigation should not remain buried in
Settings. Contents must become location-aware and responsive.

The current scholarly apparatus lacks one coherent interaction model. Calendar
resolution, source preambles, rubrical details, placement notes, availability
notices, How the Missal Changed, and the Source Library are separate surfaces
with different placement and discovery. The existing empty desktop scholarly
margin is useful space for a contextual Study rail, but only when the selected
unit has relevant material.

Large and repeated unavailable-text messages should not overwhelm the
liturgical hierarchy. They must remain explicit, source-specific, and
accessible while using summary-plus-claim-local markers where repetition adds
no new fact. Source honesty and explicit incompleteness outrank visual
smoothness.

Day and Propers must share components and modes without losing their distinct
purposes. Today they share lower-level helpers and styling but not one reader
state, shell, navigation model, apparatus model, or complete semantic rendering
pipeline. Advanced features must be discoverable without making the default
page resemble a dashboard.

Mobile is not a reduced desktop layout. It requires accessible sheets or
dialogs, stacked comparison and bilingual fragments, useful touch targets,
safe-area handling, and preserved reading position. Desktop side margins are
not a reason to compress mobile text or expand long forms above it.

No silent cross-recension or cross-locale fallback is acceptable. A route that
cannot satisfy the requested edition, locality, translation, cycle, alternative,
or Ordinary must refuse or mark partial coverage rather than choose a smoother
neighbor.

## Capability and coverage matrix

`Present` means a current public path carries the capability. `Partial` means
the data or behavior exists but coverage, consistency, or reader access is
incomplete. `Gap` means the shared reader does not yet provide it.

| Capability | Baseline | Required destination |
| --- | --- | --- |
| Civil-date navigation | Present inside Day Settings and keyboard/date controls | Primary Day action outside full Settings; remembered preference never replaces explicit date. |
| Temporal and sanctoral resolution | Present for public rubrics calendars | Preserve candidates, precedence, dispositions, omissions, and uncertainty in shared Study. |
| Dated recensions and effective ranges | Partial: recension projection exists; Day and Propers expose different sets | Edition-aware selection with explicit effective and coverage bounds in both entrances. |
| Territorial and local calendars | Partial in calendar structures and resolved branches; public coverage is narrow | Explicit user selection, no geolocation inference, stable URL state, and branch fixtures. |
| Rank, color, season, week, and cycle | Present in generated resolution; presentation varies | Shared identity summary and contextual Study details. |
| Competing celebrations and commemorations | Present in Day resolution; subordinate texts remain incomplete in some cases | Complete source-backed disposition and text ownership, or explicit partial status. |
| All readable formularies for a day | Present through the dynamic formulary selector | Primary, understandable access with each selection linkable and no hidden arbitrary choice. |
| Multiple Bible editions | Present | Shared selection and source/numbering labels in all modes. |
| Versification and psalter distinctions | Partial but source-modeled, with explicit refusal paths | Expose relevant distinction in Study and preserve identical browser/CLI resolution. |
| Original and translated Proper text | Present with uneven coverage | Bilingual fragment pairing, witness selection, rights, and per-unit availability. |
| Oration language and rights | Present with partial translations | Shared language/witness control and concise coverage summary without invented translations. |
| Ordinary language and variants | Present for generated inventories; many words are withheld or untranscribed | Honest edition-specific Missal rendering, point-of-choice options, and compact repeated-absence treatment. |
| Speaker, action, rubric, seat, and locus | Partial in Ordinary events and Day placement notes | One semantic hierarchy and Study apparatus across both entrances. |
| Source citations, witnesses, and pages | Partial across reading, preamble, and Source Library | Contextual source summaries with stable Source Library links and verified-locus status. |
| Calendar-decision explanations | Present on Day when Why is enabled | Study mode with a coherent disclosure and focus model. |
| Act and change histories | Present as a separate generated product | Contextual semantic links from Study and Compare; no duplicated history graph. |
| Recension comparison | Gap in the liturgy reader | Semantic-slot comparison with explicit additions, omissions, alternatives, sources, and act links. |
| Partial and unsupported coverage | Present but visually repetitive and not uniformly classified | First-class coverage states, concise summary, claim-local reason, and fail-closed selection. |
| Propers browse and search | Gap: nested selects and arbitrary initial formulary | Meaningful browse/search by structured fields, stable result URLs, and scoped no-result states. |
| Stable deep links | Present for current hash keys | Versioned, canonical semantic state with backward-compatible parsing. |
| Sharing | Partial: browser URL can be copied | Explicit share action, canonical URL, stable semantic anchors, and readable unfurl/title metadata. |
| Print and PDF | Present mechanically | Mode-aware, independently usable composition with required identity, rights, source, and coverage context. |
| Browser/generated-data/CLI/test parity | Strong partial foundation through assembly, seating, and event tests | One fixture contract covering identity, semantic events, text, source, options, and failure states. |

## Architectural gaps between Day and Propers

| Boundary | Current gap | Required boundary |
| --- | --- | --- |
| Reader state | Separate orchestration and different defaults | One validated semantic state model with entrance-specific required fields and URL serialization. |
| Object identity | Day begins with a resolved branch; Propers begins with nested list selection | One edition-qualified formulary identity, with optional date-resolution context. |
| Event rendering | Day can traverse a seated Mass; Propers renders an unseated Proper list | Shared semantic event/component renderer capable of direct Propers and continuous Missal views. |
| Shell | Repeated HTML disclosures and page-specific control grids | Shared responsive shell for primary actions, panels, focus, scroll restoration, status, and safe areas. |
| Modes | Feature toggles and page-specific apparatus | Explicit Read, Missal, Study, and Compare state with shared transitions. |
| Navigation | DOM-generated static buttons; default Day has only Beginning | Semantic, location-aware Contents generated from the object actually rendered. |
| Apparatus | Margins, preambles, details, notices, and placement notes are separate idioms | One contextual Study model linking decision, placement, provenance, rights, and history. |
| Discovery | Day date selector; Propers select cascade | Distinct date navigation and formulary browse/search feeding the same reader. |
| Coverage | Several free-form unavailable messages | Typed coverage result shared by rendering, search, URL validation, CLI, and tests. |
| Comparison | No shared comparator | Semantic-slot correspondence derived before visual layout. |

## Parallel workstreams

These workstreams proceed concurrently where their dependencies permit. They
are not new historical phase numbers.

### W1 — Shared reader and rendering foundation

- Define the edition-qualified liturgical object, entrance context, semantic
  event/slot contract, coverage result, and source hooks.
- Extract shared state validation, URL serialization, rendering components,
  status handling, and event traversal without changing liturgical resolution.
- Prove that current Day, Propers, and `mass-today --expanded` fixtures produce
  the same identity, order, text, variants, provenance keys, and absences.
- Encode entrance-specific Compare anchors and an explicit unresolved-choice
  result that cannot collapse to manifest or array order.
- Preserve additive generated data and lazy loading.

Dependencies: vision committed; existing assembly, seating, browser-core, and
generated schemas. W1 is the principal dependency for modes and comparison,
but shell prototypes may use adapters before extraction is complete.

### W2 — Responsive reader shell and navigation

- Prototype the four primary actions and quiet mode control at wide,
  intermediate, mobile, zoomed, and print widths.
- Move common Day navigation out of full Settings.
- Implement location-aware semantic Contents, optional wide navigation and
  Study rails, single-panel intermediate behavior, and mobile sheets/dialogs.
- Keep Date or Browse, Contents, Mode, and Details reliably revealable from a
  deeply scrolled semantic location without permanent dashboard chrome,
  reading-surface compression, or an obscured focused element.
- Preserve reading location and focus through open, close, rerender, route, and
  mode changes.

Dependencies: vision and representative fixtures. Can prototype in parallel
with W1; production integration depends on shared state and semantic locations.

### W3 — Read, Missal, Study, and Compare modes

- Make mode explicit, URL-addressable, and shared by Day and Propers.
- Retain Read's first-viewport and calm-reading baseline.
- Generalize continuous Ordinary seating for the shared Missal renderer.
- Consolidate decision, placement, source, rights, and coverage material in
  Study without duplicating source records.
- Build comparison from semantic correspondence before building parallel or
  stacked layouts.

Dependencies: W1 event/state contract; W2 shell interaction contract. Read and
Missal can stabilize before the full Study and Compare apparatus.

### W4 — Source and calendar apparatus

- Define contextual summaries and stable links for calendar reasons, rubrics,
  seats, witnesses, pages/loci, rights, availability, acts, and change history.
- Type absence and partial-coverage reasons instead of relying on repeated
  presentation strings.
- Keep unsafe reliance warnings visible while making repeated routine gaps
  compact and accessible.
- Confirm every exposed fact is carried by current generated data or add a
  source-owned schema change under the appropriate guidance.

Dependencies: W1 source and coverage hooks. Can inventory data gaps and design
the Study information model in parallel with W2.

### W5 — Propers browse and search

- Build a generated, additive search index over structured title, saint,
  incipit, season, type, citation, calendar use/date, and source identities.
- Give a new visitor a useful browse/search entry; preserve immediate rendering
  for valid deep links.
- Keep same-named edition objects distinct and expose coverage before opening.
- Link a formulary to supported Day occurrences without making one date its
  identity.

Dependencies: W1 identity and URL contract. Search-index work and prototype
research can proceed in parallel with shell work.

### W6 — Semantic comparison and historical-change integration

- Define correspondence keys for Ordinary divisions/elements, Proper slots,
  cycles, alternatives, and exceptional units.
- Define Day comparison around a fixed civil date and explicitly selected
  territorial context, with each recension resolving independently and
  calendar-result differences shown before semantic-unit correspondence.
- Define Propers comparison around corresponding edition-qualified formularies
  independently of a date; known calendar uses remain contextual links.
- Distinguish absence, unavailable text, differently seated material, and a
  genuine act-backed change.
- Link corresponding changes to How the Missal Changed and their source acts.
- Test parallel desktop and paired-stack mobile/bilingual presentations.

Dependencies: W1 semantic contract, W3 mode mechanics, W4 source/act hooks, and
at least two source-honest comparison fixtures. It must not wait for every
recension to be complete.

### W7 — Recension and territorial coverage

- Expand source-grounded formularies, dated recensions, effective ranges,
  territorial/local calendars, solved cases, and explicit partial boundaries.
- Maintain per-witness attestation, rights, calendar, Ordinary, browser, CLI,
  and test parity.
- Add no public selector whose label overstates its supported extent.
- Supply representative coverage fixtures to every other workstream.

Dependencies: source acquisition and the owning calendar/recension guidance,
not completion of the visual redesign.

**Historical Phase 10 placement.** Existing Phase 10 work on the Pius XII/1956
recension belongs in W7. Documentation stabilization through the vision and
this roadmap precedes further Phase 10 implementation; M0 and this correction
complete that documentation prerequisite once externally accepted. The
universal source model is:

```text
verified pre-1955 base text and structures
  + the official 1955 decree
  + applicable subsequent official decrees and authentic responses
  = a source-grounded 1956–1960 recension state
```

The Sacred Congregation of Rites' [*De rubricis ad simpliciorem formam
redigendis*](https://www.vatican.va/archive/aas/documents/AAS-47-1955-ocr.pdf),
23 March 1955, AAS 47 (1955), pp. 218–224, directs use of the liturgical books
as they then existed, applies its enumerated changes, leaves matters not
expressly named unchanged, takes effect 1 January 1956, and forbids publishers
to innovate meanwhile. [*Rubricarum
instructum*](https://www.vatican.va/content/john-xxiii/la/motu_proprio/documents/hf_j-xxiii_motu-proprio_19600725_rubricarum-instructum.html),
AAS 52 (1960), pp. 593–595, makes the new code obligatory on 1 January 1961 and
ends the 1955 decree's force that day.

After the official acts and inherited base material for a narrow slice are
verified, W7 may build an internal, typed-partial-coverage vertical slice in
parallel with W1 and W2. The verified but inaccessible 1956 Benziger printing
remains a valuable validation witness for publisher arrangement and American
or local supplements; it is not a universal implementation prerequisite. The
whole visual redesign is likewise not a prerequisite. Recension work must obey
the vision's partial-coverage, fail-closed source honesty, stable identity, and
shared-rendering rules, and the state remains absent from the ordinary public
selector until advertised coverage, Ordinary extent, locality, rights, and
tests are honest.

### W8 — Accessibility, performance, and print

- Establish automated and manual accessibility baselines for both entrances
  and all mode transitions.
- Measure route data, parse/render cost, LCP candidates, interaction latency,
  and layout shifts; set budgets before production shell integration.
- Build mode-aware print composition and independently usable PDF review.
- Exercise reduced motion, forced colors, safe areas, zoom, text enlargement,
  screen readers, keyboard, touch, and slow-device/network conditions.

Dependencies: begins with baseline measurement immediately; every workstream
must meet its gates continuously rather than defer them to release.

### W9 — Migration, regression, and release verification

- Preserve and test legacy Day and Propers hashes while introducing canonical
  shared state.
- Maintain versioned fixtures, screenshot baselines, semantic parity hashes,
  console/network checks, and release bindings.
- Prepare and record the external-review package required for each major visual
  milestone before acceptance.
- Verify public-preview and public-site artifacts, links, source bindings,
  rights, and exact deployed SHA before release.
- Stage rollouts so a new shell or mode can be disabled without changing
  liturgical data or invalidating links.

Dependencies: continuous. A release checkpoint integrates completed slices
from the other workstreams; it does not wait for unrelated coverage expansion.

## Integration milestones and dependencies

Milestones are cross-workstream checkpoints, not sequential development lanes
and not replacements for historical phases.

M1–M5 are internal integration milestones. They may be privately previewed and
externally reviewed, but they are not public releases and may not advertise an
incomplete mode set. The existing public reader and every currently supported
function remain intact while those milestones develop behind fixtures or a
reversible preview boundary. M6 is the first public reader release governed by
the complete four-mode product contract and all world-class gates.

| Milestone | Integrated result | Required inputs |
| --- | --- | --- |
| M0 — Governing contract | Vision, roadmap, routing, baseline evidence, correction disposition, and no production change | `bc7de4114`, `4236f21bf`, retrospective review, this correction commit, and its external acceptance |
| M1 — Semantic parity contract | Versioned fixture schema and shared identity/event/source/coverage assertions for existing Day, Propers, and CLI | W1, W4, W9 |
| M2 — Shell prototype decision | Tested wide/intermediate/mobile/zoom/print prototypes; bounded choices resolved; no liturgical data change | W2, W8, representative W9 fixtures |
| M3 — Shared Read and Missal slice | Both entrances use shared state, semantic renderer, navigation, and Read/Missal modes for Roman 1962 and postconciliar fixtures | W1, W2, first half of W3, W8, W9 |
| M4 — Study, discovery, and coverage slice | Shared Study apparatus, compact typed coverage, Propers browse/search, source/history links | W3, W4, W5, W8, W9 |
| M5 — Compare slice | Semantic recension/translation/cycle/alternative comparison in parallel and stacked forms | W3, W4, W6, qualifying W7 fixtures, W8, W9 |
| M6 — Release-quality reader | All world-class gates pass for the advertised coverage; compatible URLs and independently usable print ship | All applicable workstreams |

Phase 10 may advance official-act collation, inherited-base verification, and
exact-printing validation after the corrected M0 contract is externally
accepted. It may produce a narrow internal typed-partial-coverage fixture after
its own source gates and does not depend on M2–M6. A public 1956–1960 recension
selector depends on its complete advertised coverage and release gates, not on
an inaccessible printing alone or merely on the first reader redesign release.

## External-review handoff gate

Before M2, or any M3–M6 checkpoint containing browser-visible change, is marked
accepted, create and externally review the unique package required by the
[external-review handoff protocol](external-review-handoffs.md). Its screenshot
set follows this roadmap's required routes, states, and viewports; its review
request identifies the precise blocking acceptance judgments. Record the
handoff basename, reviewer disposition, and resolution of every blocker in the
progress ledger or owning tracked acceptance record. Creating the package alone
does not satisfy the gate.

## Acceptance gates

Every implementation slice passes the gates for the capabilities it affects.
M1–M5 remain internal and do not fail merely because a later mode is not yet
integrated; they preserve every current public function and do not advertise
the incomplete product. M6 passes the complete product contract and all gates
before public release. “No change” to liturgical data is proved by semantic
fixture parity, not assumed from a visual diff.

### Product and semantic gates

- Day and Propers identify and render the same edition-qualified formulary and
  semantic units consistently.
- Read, Missal, Study, and Compare are each one clear action away on both
  entrances, with Read initially active and visually dominant.
- At every semantic reading location, Date or Browse, Contents, Mode, and Study
  are reachable without returning to the document beginning or losing that
  location.
- Today and real text appear immediately in a first Day visit; a valid Propers
  deep link renders immediately; a new Propers visit opens browse/search.
- Date navigation is available outside full Settings.
- Contents reports the current semantic unit and only actual destinations.
- Position and focus survive auxiliary panels, supported state changes, and
  mode transitions according to a documented rule.
- No unsupported selection falls through to another recension, locality,
  translation, cycle, alternative, formulary, or Ordinary.
- No coequal unresolved authorized option is selected by manifest or array
  order; the choice appears at its semantic point.

### Source, data, and parity gates

- Every rendered unit and decision carries stable source/provenance and typed
  coverage data adequate for Study and tests.
- Browser, generated data, CLI, and tests agree on identity, selected branches,
  event order, text, sources, rights state, and explicit absence.
- Search results and deep links resolve the same stable formulary identities as
  the generator.
- Day comparison holds date and territorial context fixed, resolves each
  recension independently, exposes calendar-result differences first, and then
  aligns semantic units. Propers comparison aligns corresponding
  edition-qualified formularies without introducing a date. Both leave
  one-sided units explicit.
- Source, calendar, recension, versification, rights, and release checks owned
  by affected guidance pass.

### Responsive and visual gates

- The default 1440×900 and 393×852 first views show identity and real text.
- 1024×768 and 768×1024 use one reading column and at most one auxiliary panel.
- No horizontal page scroll or lost functionality occurs at 320 CSS pixels,
  400% zoom, or 200% text enlargement.
- Wide rails never compress the reading below its usable measure and are absent
  or empty when irrelevant.
- Deep-scroll access to the four primary actions is reliably revealable without
  permanent dashboard chrome, reading-surface compression, or covered focused
  content at every supported width.
- Mobile sheets/dialogs preserve safe areas, focused controls, and reading
  location. Compare and bilingual fragments stack by corresponding unit.
- Missing-text treatment is unmistakable but subordinate to the celebration
  and available liturgical text.

### Accessibility gates

- WCAG 2.2 AA automated checks report no applicable violations, followed by
  manual review of structure, language changes, contrast, focus order,
  focus-not-obscured, names/roles/states, status announcements, and reflow.
- Every core path is complete with keyboard alone and with touch alone.
- Keyboard, touch, and screen-reader runs prove that the four primary actions
  can be revealed and dismissed from a deeply scrolled location with focus and
  semantic location preserved.
- Disclosures, sheets, and dialogs follow the applicable WAI pattern, including
  expanded state, Escape behavior, focus containment where modal, and focus
  restoration.
- Representative screen-reader runs cover Day selection, Propers search,
  Contents navigation, every mode, options, coverage warnings, comparison, and
  print access.
- Forced colors and reduced motion retain meaning and operation.

### Performance gates

- Field data, when sufficient, meets the current good Core Web Vitals at the
  75th percentile separately for mobile and desktop: LCP ≤2.5 s, INP ≤200 ms,
  CLS ≤0.1.
- Reproducible lab tests enforce the same direction before field data exists,
  including throttled mobile and warm/cold-cache deep links.
- Route-specific transfer, request-count, main-thread, and rendered-DOM budgets
  are recorded at M2 and enforced thereafter.
- Read does not fetch the Ordinary, comparison peers, or full Study/source
  records until needed. Valid deep links do not incur an arbitrary-formulary
  render first.

### Print, URL, and release gates

- Print hides all interactive chrome and preserves independent edition, date or
  formulary, locality, language, cycle/alternative, source, rights, and coverage
  context.
- Print review includes text extraction and visual inspection of every page for
  representative short, long, bilingual, partial, and comparison cases.
- Canonical URLs reproduce semantic state in a storage-free session. Legacy
  URLs pass compatibility fixtures and canonicalization changes no selection.
- Public-preview and public-site builds, link/fragment verification, release
  bindings, console/network review, and exact deployed-SHA verification pass.

## Visual-regression strategy

The visual suite is fixture-driven. It never changes production data merely to
manufacture a screenshot state. A state absent from public data uses a lawful,
explicit test fixture that exercises the same renderer and declares that it is
not public coverage.

Every release candidate captures at least:

- 1440×900, 1024×768, 768×1024, 393×852, and exact 320 CSS-pixel reflow;
- Day and Propers with the reader shell closed;
- each route deeply scrolled, with the four primary actions revealed and
  dismissed while asserting semantic location, focus, and unobscured content;
- each auxiliary surface open, one at a time, with focus and scroll assertions;
- Read, Missal, Study, and Compare;
- Roman 1962 and postconciliar;
- a pre-1955 or other qualifying comparison state;
- a Day comparison whose recensions resolve the fixed date to different
  celebrations, a date-independent Propers comparison of corresponding
  formularies, and a coequal unresolved option that requires user choice;
- Ordinary off and on; Why/rubrics closed and open;
- bilingual paired and stacked text;
- populated routine Notice, immediate-reliance warning, partial recension,
  unsupported date, unavailable translation, missing Ordinary, competing
  celebration, commemoration, cycle, alternative, local calendar, and
  territorial branch;
- light/dark only if both are actually supported, plus forced colors and reduced
  motion regardless; and
- screen and print/PDF output.

Pixel diffs protect composition and regressions but do not approve correctness.
Each fixture also asserts title, semantic unit IDs and order, accessible names
and states, focus target, scroll position rule, URL, overflow, console/network
errors, and source/coverage identity. Reviewers inspect the first viewport and
every printed page rather than accepting a contact sheet alone.

## URL and compatibility migration

1. Inventory every current Day and Propers hash key and add it to permanent
   compatibility fixtures before changing parsing.
2. Define one shared semantic state schema with entrance-specific requirements.
   Keep route identity explicit; do not make a missing date distinguish Day from
   Propers by accident.
3. Parse legacy hashes into that state, validate against generated manifests,
   and serialize one canonical URL. Invalid requested values produce an
   explicit unsupported state, not a default substitution.
4. Introduce additive keys for mode, locality, semantic location, comparison
   dimension and sides, and any newly linkable option. Do not reuse an old key
   with changed meaning.
5. Keep old links working through parsing or a documented redirect for at least
   the supported life of the published corpus. Preserve unrecognized keys while
   a compatible older client may own them only when doing so is safe.
6. Test URL precedence over remembered preferences and storage-free behavior.
7. Update share metadata and canonical links only after semantic-state fixtures
   pass on the deployed artifact.

The exact spelling of new keys and whether canonical state remains in the hash
or moves partly to query/path is an M1 prototype decision. Compatibility,
explicit entrance identity, and reproducibility are not open decisions.

## Print and sharing strategy

Print is generated from the same semantic object and selected mode, with a
print-specific composition layer. Read print emphasizes appointed text; Missal
print preserves the continuous order; Study print includes only explicitly
selected apparatus or a concise appendix; Compare print preserves paired
semantic units and clear edition headings. Interactive open/closed state alone
must not accidentally determine whether essential print context exists.

The Share action copies a canonical semantic URL and provides a descriptive
title naming the celebration or formulary and edition. Day shares include the
date and locality; Propers shares do not invent a date. Compare shares name the
dimension and both sides. Sharing never embeds unpublished text or bypasses a
rights restriction.

## Data and rendering parity

One fixture record must be sufficient to ask all consumers the same questions:

| Assertion | Browser | Generated data | CLI | Tests |
| --- | --- | --- | --- | --- |
| Object and edition identity | Visible title/meta and URL | Stable keys/manifests | Named result | Exact equality |
| Calendar result and branch | Day Study | Calendar/rubrics result | `mass-today` | Solved case |
| Semantic event and seat order | Read/Missal/Contents | Proper/Ordinary structures | Expanded event stream | Ordered IDs/hash |
| Text, language, cycle, alternative | Rendered fragment | Source fragment and selection | Printed/structured output | Exact text/selection |
| Source, witness, locus, rights | Study/link/print context | Source identities and coverage | Structured detail | Join and refusal assertions |
| Missing or unsupported material | Typed summary and claim marker | Typed coverage result | Explicit refusal | No-fallback assertion |

Presentation-only adapters may differ. No consumer may re-derive a liturgical
choice, reparse translated labels to find a slot, or manufacture a source fact.

## Coverage and recension expansion

Coverage work is incremental and may ship independently when its advertised
boundary is complete and honest. Each increment names the exact dated book or
act state, locality, calendar span, supported formularies, Ordinary extent,
translations, rights, and unresolved material. Public discovery must not imply
more.

Representative regression coverage eventually includes Roman 1962,
postconciliar, pre-1955, the source-grounded 1956–1960 middle state when
available, territorial/local overlays, cycles, alternatives, commemorations,
competing celebrations, resumed Sundays, partial recensions, unsupported dates,
and exceptional rites that do not fit an ordinary Mass frame.

The Phase 10.1 ordinary-Sunday vertical slice remains a useful internal parity
target after the official acts and the inherited pre-1955 base text and
structures required for that slice are verified. Applicable later official
decrees and authentic responses must also be collated. The slice may then use
an internal stable identity, source registration, and typed partial-coverage
boundary without claiming a complete printed edition. It uses the shared
renderer rather than edition-specific UI.

Inspection of the selected 1956 Benziger printing proceeds in parallel as
validation of arrangement, local supplements, Ordinary loci, and witness-level
text. It remains necessary for claims about that printing and any American or
local coverage, but not for universal changes already established by the
official acts and inherited base. No ordinary public selector appears until the
advertised calendar span, formularies, Ordinary extent, locality, rights, and
tests are complete and explicit.

## Historical next-action record, through 2026-08-27

The [2026-10-19 completion plan](#completion-plan-2026-10-19) owns current
recovery and execution order. The following record preserves the historical
cutover and phase dispositions; its then-current next actions, old object IDs,
and example-replay status must not be treated as today's instructions.

The Liturgical Instrument visual reset, responsive correction, production
integration, compatibility closure, cutover gate repair, and same-path public
cutover are independently accepted and complete. Canonical
`liturgy/day.html` and `liturgy/index.html` now serve the accepted production
readers without redirecting. Exact cutover commit
`9b5f21c0ca26bf02af03d207ddd2617021e16fb3` owns qualifying successful Pages
run `31175722949`, 936/936 immediate live assertions, and 216/216 ordinary-
cache assertions after 613 seconds. The immutable execution handoff was
introduced at commit `1d60b49bcf2a46e5ee43d6326af3e13a43265b72`, with verified
ZIP SHA-256
`06752126a3a3235a342f54ec08811faaf4fc2622924008c4362dda519624c410`.

On 2026-08-27 the seven formerly tracked Liturgical Instrument review packages
were removed from the current tree as whole packages. Their protected PNG/PDF
evidence could not remain, and leaving partial packages or refreshing their
manifests would contradict the immutable ignored-handoff contract. The packages
therefore have no current-tree directories or manifests. Their historical
locations are:

- `20260806T112813Z-liturgy-reader-instrument-correction` at
  `50288ddf9759f56e8a25e4907d8de25e27e25e8f`;
- `20260806T132759Z-liturgy-reader-instrument-correction` at
  `c388ab42dfc4f5c7d49abc71596d6bb511af5742`;
- `20260806T141831Z-liturgy-reader-instrument-correction` at
  `4daf7d8a1e1c509edb81a738cc71223170bbbd2d`;
- `20260806T183040Z-liturgy-reader-instrument-production-integration` at
  `8c6e1270f692ca4136f2f6a60002bacd3af0440c`;
- `20260807T052836Z-liturgy-reader-public-cutover-compatibility` at
  `e69d91ffff5823dc2970f867f1be8c9eb5b6363b`;
- `20260807T105259Z-liturgy-reader-public-cutover-gate-repair` at
  `a996a82a68163dd5f7a2af24ae63f100244d6bc0`; and
- `20260807T115341Z-liturgy-reader-instrument-public-cutover-execution` at
  `1d60b49bcf2a46e5ee43d6326af3e13a43265b72`.

Those commits preserve the historical record, including the protected objects;
this disclosure is not a current distribution clearance or a decision to
rewrite published history.

Public navigation was not redesigned. Retained `day-reader.html`,
`propers-reader.html`, and both visual-reset oracle routes remain intact and
nonindexable as rollback and regression surfaces; their cleanup is deferred and
unauthorized. No automatic reader phase follows this closeout. Any future
production reader work begins from the live canonical pages under separate
planning and authorization. The governed full repository check remains
non-green only at the unrelated stored-example transcript replay; no transcript
was recaptured or blessed. The canonical acceptance and execution record is
`build/agent-continuity/liturgy-reader-visual-plan.md`.

1. M1's W1/W9 shared semantic fixture and URL-state contract is accepted at
   correction `c6b8070ae76e75153448895a19a0b916c18806ea` plus final micro-fix
   `c1a590f5854215d68d167d9040e188f41762663e`. The Round 1 acceptance supplies
   the separate bounded production-integration scope; any further W1/W9 slice
   still requires separate authority.
2. W2 and M2 are **accepted** at corrected implementation
   `75234e72c402f0b25a681fbe074da70d895f7274`. The quiet persistent shell is
   the direction for Date or Browse, Contents, Mode, and Details. Complete Read
   states omit diagnostic noise; every auxiliary surface reflows without
   internal horizontal scrolling; temporary Details is distinct from pinned
   nonmodal wide-desktop Study and reversible tablet/mobile Study sheets. The
   internal noindex prototype remains evidence, including its non-preferred
   scroll-reveal variant. The measured decision record is
   [the reader-shell prototype record](liturgy-reader-shell-prototype.md).
   W3 now has one reversible, unlinked Day Read-mode integration candidate at
   `liturgy/day-reader.html`. The reusable shell owns interaction only; the Day
   adapter crosses the accepted M1 boundary and reuses production assembly,
   fragment fetching, and Proper rendering. Supported legacy state retains its
   meaning, later-mode state is handed intact to the unchanged live route, and
   invalid explicit state fails closed. It does not replace or alter the live
   Day route. External review accepted the architecture and requested bounded
   legacy-state, transition-clearing, weekday, and human-facing Details
   corrections. Those corrections are represented in the compact handoff
   `20260804T173010Z-day-reader-shell-integration-corrections`. M3 is accepted
   after final micro-fix `c604edb8a1fffb1e5c0981798800ecb801258e7c` made the
   existing render serial authoritative across delayed success and failure
   paths. Deterministic Chromium races prove that a superseded valid or failed
   request cannot replace a newer valid or invalid result, including during
   Back navigation. Live Day and Propers remain unchanged; Propers integration,
   later modes, public navigation and cutover, and recension work remain
   outside that accepted Day slice. A second W3 entrance now enters the same
   shell at `liturgy/propers-reader.html`: it
   selects a formulary without a civil date, crosses the accepted M1 Propers
   adapter, and reuses the production Proper renderer. Its Browse, cycle and
   alternative, transition, responsive, accessibility, and print evidence is
   externally accepted after the bounded correction at
   `1e4587dfe04a11c18e996a16f7fbbdb54bc744a4`. It does not reopen the accepted
   Day slice or start public cutover, later modes, search, or recension work.
   The distinct **Day Missal-mode integration** is now accepted at
   `86a9816c1bffdcbdd09469f5f8d005c666a8045e`. It extends only the existing
   unlinked Day candidate: `ordinary=1` renders the production Ordinary through
   the production renderer and M1 assembly/seating event stream, while
   `ordinary=0` retains Read and valid latent Ordinary preferences. Settled
   Chromium evidence proves deterministic outcome chrome, semantic location,
   inline Eucharistic Prayer focus, render ownership, and neutral duplicate-key
   rejection without changing the accepted M3 record, accepted Propers Read
   entrance, or any public route. Study, Compare, Propers Missal mode, search,
   cutover, and recension coverage remain later boundaries.
3. W7 verifies the pre-1955 base and official acts for the narrow Phase 10
   slice, while exact-printing acquisition continues in parallel as validation
   rather than a universal prerequisite.

No prototype chooses liturgical defaults or creates data to fill a review
state. M1–M5 remain internal; M6 is the first public redesigned reader release.

## Progress ledger

Historical phase names and numbering are preserved. Rows that produced no
tracked commit say so rather than borrowing a neighboring SHA.

| Date | Historical work | Result | Commit reference |
| --- | --- | --- | --- |
| 2026-08-02 | Phase 4, Step 1 — continuous missal presentation | Added the continuous reading surface and retained rendered text parity. | `c767c5374` |
| 2026-08-02 | Phase 4, Steps 2–4 — refinement and scholarly margin studies | Established measure, responsive behavior, and optional empty desktop margin through local review; later retained in the Reading Missal direction. | No separate tracked commit; reviewed against `c767c5374` |
| 2026-08-02 | Phase 5, Step 1 — annotation experiment | Tested contextual notes and deliberately left the placeholder experiment uncommitted. | No tracked commit |
| 2026-08-02 | Phase 6, Step 1 — Reading Missal v1 | Made Day reading-first with dominant title and closed Settings/Notices while preserving event and text parity. | `6a68536d7` |
| 2026-08-03 | Phase 7, Step 1 — reading-first formulary page | Brought Propers into the Reading Missal visual language without merging route purposes. | `fdd88fb67` |
| 2026-08-03 | Phase 8, Step 1 — generated Mass Contents | Added shared DOM-derived Contents and completed its route integrations and tests. | `febaa92d0`, `719e975d1` |
| 2026-08-03 | Phase 9, Step 1 — Proper placement notes | Added source-bounded mechanical placement notes to supported seated Propers on Day. | `18256c51e` |
| 2026-08-03 | Phase 10, Step 1 — Roman 1955 vertical-slice assessment | At that step, recommended an exact-edition, source-bounded 1956–1960 slice and found source and precedence blockers; later external review corrected the exact-printing prerequisite. | No tracked change; review baseline `18256c51e` |
| 2026-08-03 | Phase 10, Step 2 — source acquisition | Identified the 1956 Benziger edition and institutional copies as a verified but inaccessible validation witness; later external review removed it as a universal prerequisite while preserving its witness/locality value. | No tracked change; review baseline `18256c51e` |
| 2026-08-03 | M0 — browser vision and roadmap stabilization | Established the governing destination, parallel workstreams, gates, and routing without production changes. | `bc7de4114a279ea780d5b15bdaee0a7414e07078` |
| 2026-08-03 | External-review handoff protocol | Established the immutable ignored review-package contract and major-visual-milestone gate. | `4236f21bfe5aa6f3dde76ee0b9398823373f22e3` |
| 2026-08-03 | M0 retrospective external review | Accepted the governing foundation and requested five narrow corrections: persistent action reachability, entrance-specific Compare anchors and coequal choice handling, the official-act Phase 10 model, a current execution record, and internal-versus-public milestone scope. | Handoff `20260803T155820Z-liturgy-browser-vision-retrospective`; reviewed through `4236f21bfe5aa6f3dde76ee0b9398823373f22e3` |
| 2026-08-03 | M0 external-review corrections | Resolves the five blockers without production or recension implementation; the exact SHA is recorded in the completion report and correction handoff because a commit cannot contain its own hash. | This correction commit |
| 2026-08-03 | M0 correction external acceptance | Accepted — all five blockers resolved. The governing contract is stable, and W1/W9, W2, and W7 may begin in parallel at their recorded boundaries. | Reviewed commit `aad3691ee67106f6ff2cdb639463248ff35e3594`; handoff `20260803T164600Z-liturgy-browser-vision-corrections`; review result `20260803T171758Z-liturgy-browser-vision-corrections-review-result.md` |
| 2026-08-03 | M1 — semantic parity contract external acceptance | Accepted — cycle alternatives are preserved, v1 property-presence validation is complete, the focused suite passed all 38 tests, and the deployed Day and Propers routes still load neither M1 module. The full gate remains red only at the separately approved example baseline and its authorized completion-count update. | Implementation `259573d393cd6a6bac09fc751ac1d14ec9477853`; reviewed correction `c6b8070ae76e75153448895a19a0b916c18806ea`; final micro-fix `c1a590f5854215d68d167d9040e188f41762663e`; handoffs `20260803T223346Z-liturgy-reader-state-contract` and `20260803T235342Z-liturgy-reader-state-contract-corrections`; external review dispositions *M1 liturgy reader-state contract*, *M1 reader-state corrections*, and *M1 acceptance closeout count delta* |
| 2026-08-04 | M2 candidate — responsive reader-shell prototype | Candidate pending external review. One internal noindex shell serves Day and Propers, reuses the Proper renderer and validated M1 fixtures, and tests persistent/reveal reachability, semantic Contents, coherent Study, representative mode shells, responsive sheets/rails, and print without production-route or liturgical-data integration. | This candidate commit; decision record `guidance/liturgy-reader-shell-prototype.md`; handoff `20260804T101952Z-liturgy-reader-shell-prototype` |
| 2026-08-04 | M2 candidate external-review corrections | External review accepted persistent reachability and requested three bounded corrections. The corrected candidate removes complete-state diagnostic noise, directly proves every auxiliary surface has no internal horizontal overflow including at 200% text, renames temporary Study access to Details, and gives Study mode a nonmodal pinned wide-desktop rail while retaining a reversible mobile sheet. M2 remains pending correction re-review. | This correction commit; compact correction handoff recorded in the completion report |
| 2026-08-04 | M2 — responsive reader-shell external acceptance | Accepted — the quiet persistent reader shell is the M2 direction. Complete Read states are free of diagnostic noise, all auxiliary surfaces reflow without internal horizontal scrolling, and temporary Details is distinct from wide-desktop pinned Study and mobile Study sheets. Production Day and Propers routes remain unchanged. | Candidate `68becc59b396aca830c233b88ec74991563603d1`; correction `75234e72c402f0b25a681fbe074da70d895f7274`; handoffs `20260804T101952Z-liturgy-reader-shell-prototype` and `20260804T142747Z-liturgy-reader-shell-corrections`; external review results *M2 prototype changes-requested disposition* and *M2 responsive reader-shell acceptance and closeout disposition* |
| 2026-08-04 | M3 candidate — production reader-shell foundation and Day Read integration | Candidate pending external review. The bounded noindex route extracts only the accepted persistent shell; integrates real Day Read output through production assembly, the accepted M1 adapter, shared fragment fetching, and the shared Proper renderer; preserves supported and deferred legacy state without fallback; and passes measured desktop, tablet, mobile, zoom, accessibility, print, and live-route isolation checks. | This candidate commit; handoff `20260804T154620Z-day-reader-shell-integration` |
| 2026-08-04 | M3 candidate external-review corrections | External review accepted the reusable-shell architecture and requested three bounded corrections. The correction preserves valid inactive later-mode preferences as latent Read-compatible state while active requests still defer and invalid values fail closed; clears selection state before every render attempt; restores exact assembly-owned weekday presentation; and removes raw source-hook coordinates from visible Details. M3 remains pending correction review, and live routes remain unchanged. | This correction commit; compact correction handoff `20260804T173010Z-day-reader-shell-integration-corrections` |
| 2026-08-04 | M3 — production Day Read integration external acceptance | Accepted — the production Day Read candidate reuses the existing assembly and Proper renderer behind the shared persistent shell, preserves Read-compatible legacy state, explicitly defers later-mode state, fails closed across invalid and superseded asynchronous transitions, and remains isolated from the live Day and Propers routes. Acceptance does not authorize cutover, Propers integration, later modes, public exposure, or recension work. | Candidate `45a6b76249e015f68830495ca2971e9dbc4a4e14`; correction `d0872545ccc92106cb457b448f37201381c5bb2d`; final micro-fix `c604edb8a1fffb1e5c0981798800ecb801258e7c`; handoffs `20260804T154620Z-day-reader-shell-integration` and `20260804T173010Z-day-reader-shell-integration-corrections`; external review dispositions *W3 Day reader-shell changes requested* and *W3 conditional acceptance, final micro-fix, and M3 closeout* |
| 2026-08-04 | W3 Propers Read integration candidate — second production Read entrance | Candidate pending external review. The unlinked, noindex Propers entrance uses the accepted shared shell, explicit M1 Propers state, production manifests, fragments, and Proper renderer; leaves missing identity unresolved; rejects invalid explicit state; and preserves coequal cycles and alternatives independently. This distinct W3 entrance does not reopen the accepted M3 Day integration. Public Day and Propers, the accepted Day candidate, later modes, search, public cutover, and production liturgical data remain unchanged. | Candidate `b0b1e5b63ba4a1d389b53276fa0bf9944c0ee909`; external-review handoff `20260804T212821Z-propers-reader-shell-integration` |
| 2026-08-04 | W3 Propers Read integration candidate corrections | Candidate pending external review. Browse requests translation-witness choice only when multiple identified witnesses can faithfully supply the selected formulary and translated language; source-language selection clears the private witness state. Every route attempt and Browse dismissal invalidates pending Browse loads so stale edition controls cannot replace the current form. The shared shell, M1 semantics, renderer, cycle handling, live routes, accepted Day candidate, and production data remain unchanged. | This correction commit; compact correction handoff recorded in the completion report |
| 2026-08-04 | W3 Propers Read integration external acceptance | Accepted — the W3 Propers Read integration enters the same production reader shell as the accepted Day candidate, preserves current valid formulary semantics through the M1 Propers state and production Proper renderer, leaves missing identity unresolved, fails closed on invalid state, preserves cycles and alternatives independently, requests translation witnesses only when formulary-specific translated material requires a choice, and remains isolated from the public Day and Propers routes. The initial review requested bounded Browse witness, Browse-race, tracking, and handoff corrections; the acceptance disposition confirms those blockers resolved. The reviewed evidence passed 84 focused tests, 90 public-alpha/gallery tests, and 27 Propers, 25 Day, and 18 shared-shell Chromium assertions. Shared-shell SHA-256 remained `bf1c062453f8fcfd5a68c1fe30e31aca89ea1a3c8adeef9a5525d8081ae8c707` for JavaScript and `e7195cd86ed4fc4a8455e97369702239eb22d709a13d3d8462d7759c01fe814a` for CSS. Public routes, the accepted Day candidate, M1 semantics, navigation, selectors, and production liturgical and generated data remained unchanged. The approved example baseline retained the same 23 unrelated divergences and two promised-deliverable commands; only the authorized count advanced to 18 tracked, 13 complete. Excess cycle-choice print whitespace is retained for later print refinement. | Candidate `b0b1e5b63ba4a1d389b53276fa0bf9944c0ee909`; correction `1e4587dfe04a11c18e996a16f7fbbdb54bc744a4`; handoffs `20260804T212821Z-propers-reader-shell-integration` and `20260804T225215Z-propers-reader-shell-corrections`; external-review dispositions *Propers Read candidate changes requested* and *Propers Read integration external acceptance and closeout* |
| 2026-08-05 | W3 Day Missal-mode integration candidate | Candidate pending external review. The existing unlinked Day entrance keeps Read as default and adds a continuous Missal assembled from the accepted M1 Day event stream, production Ordinary and Proper renderers, and the unchanged Ordinary seating model. Roman 1962 and postconciliar states retain distinct sequences; valid latent language and Eucharistic Prayer state survives mode changes; explicit invalid or inapplicable values and missing Proper seats fail closed; `why=1` remains deferred; and semantic location, history, races, reflow, accessibility, performance, and print have focused evidence. The public Day and Propers routes, accepted Propers candidate, M1 contract, seating engine, and production liturgical data remain isolated. | This candidate commit; external-review handoff recorded in the completion report after push |
| 2026-08-05 | W3 Day Missal-mode candidate changes requested | External review of candidate `a1221755d4fac2a6b9a009a91b99cd1da82eee9e` and handoff `20260805T145914Z-day-missal-mode-integration` passed the production Ordinary/seating architecture, edition distinctions, semantic option validity, ergonomics, isolation, and scope. Acceptance remains blocked on deterministic mode chrome for every non-ready outcome, keyboard-focus restoration after inline Eucharistic Prayer changes, and generation-safe direct-load and transition evidence. The correction remains bounded to those seams and full replacement captures; the candidate is not accepted or public. | Changes requested; correction commit and compact re-handoff pending |
| 2026-08-05 | W3 Day Missal-mode bounded corrections | Candidate pending independent correction review. One outcome-aware presentation path now commits requested Read/Missal chrome on every syntactically recognized state and neutral unchecked chrome for invalid `ordinary`; valid deferred, unresolved/territorial, and unrenderable states are distinct from explicit rejection. Inline Eucharistic Prayer changes restore focus to the rerendered checked semantic option while retaining reading location. The browser harness now proves fresh documents with unique non-semantic query nonces and document tokens, and same-document navigation with exact state plus greater committed render generation before the post-render frame boundary. All screenshots and the 21-page print were regenerated; no accepted architecture, public route, Propers surface, M1 seam, seating engine, or production data changed. | This correction commit; compact correction handoff recorded after push; acceptance remains open |
| 2026-08-05 | W3 Day Missal-mode evidence-settlement changes requested | External review of correction `ce5fce8364d24156e41c444c43673e7de31555d8` and handoff `20260805T183500Z-day-missal-mode-corrections` found the substantive product corrections sound and production isolation intact. Acceptance remains blocked only because two post-render animation frames do not prove inherited smooth scrolling and its semantic target have settled, and because both duplicate `ordinary` key orderings lack direct Chromium coverage. The micro-correction is limited to animation-frame stability proof, settled default/reduced-motion Eucharistic Prayer focus and location assertions, both duplicate-key orderings from fresh/Read/Missal paths, complete replacement evidence, and a new independent handoff. The candidate is not accepted or public. | Changes requested; evidence micro-correction and compact re-handoff pending |
| 2026-08-05 | W3 Day Missal-mode evidence-settlement micro-correction | Candidate pending independent external review. Exact document-token and committed-generation checks now precede a separate bounded animation-frame loop requiring five stable scroll, semantic-target, and focused-control frames with viewport intersection and cleared pending navigation. Settled default-motion EP I/III/IV/II and reduced-motion keyboard checks exposed and corrected one local Day-adapter issue by aligning the inline option group after semantic restoration; the shared shell and site scrolling remain unchanged. Both duplicate `ordinary` orderings are neutral and history-independent on fresh loads and transitions from Read and Missal. The complete Day screenshot and 21-page print set was regenerated; public Day/Propers, the Propers candidate, shared shell, M1 seams, seating, and production data remain isolated. | This micro-correction commit; compact correction handoff recorded after push; acceptance remains open |
| 2026-08-05 | W3 Day Missal-mode integration external acceptance | Accepted — every blocking review question is resolved and no further handoff is required. The internal Day reader reuses the production Ordinary presenter, M1 event stream, single Ordinary seating path, and Proper renderer while retaining edition-specific Roman 1962 and postconciliar structures, deterministic fail-closed state, semantic location/history/race ownership, and production isolation. The accepted handoff records 34 passing Day Chromium assertions plus the focused and regression suites, settled default/reduced-motion Eucharistic Prayer focus, neutral unchecked behavior for both duplicate `ordinary` key orderings on fresh and transitioned paths, 107 settled screenshot rows, and the 21-page print review with no console, request, or HTTP errors. Public cutover, later modes, search, source/recension expansion, and print redesign remain separate future decisions. | Candidate `a1221755d4fac2a6b9a009a91b99cd1da82eee9e`; correction `ce5fce8364d24156e41c444c43673e7de31555d8`; accepted micro-correction `86a9816c1bffdcbdd09469f5f8d005c666a8045e`; handoffs `20260805T145914Z-day-missal-mode-integration`, `20260805T183500Z-day-missal-mode-corrections`, and `20260805T201722Z-day-missal-mode-evidence-corrections` |
| 2026-08-05 | Liturgy reader visual-reset direction candidate | Candidate pending maintainer and independent visual review. Explicit maintainer direction reopens visual composition without disturbing accepted M1–M3/W3 behavior. One unlinked, noindex Day/Propers prototype compares Quiet Folio, Liturgical Instrument, and Contemporary Reader over the same semantic DOM, production adapters, renderers, seating, and shell controller. Liturgical Instrument is recommended for its ritual cue grid and continuous-action hierarchy; Folio's editorial restraint and Reader's compact chrome and Browse flow remain explicit comparison strengths. The current evidence records 52 same-run screenshots, 12 passing Chromium assertions, clean console/network/accessibility/overflow results, required responsive and enlarged states, deployed before/after comparisons, and a print smoke check. Public routes, accepted candidates, shared shell, M1 seams, seating, and production data retain exact hashes. This is a visual decision candidate, not acceptance or public cutover. | This candidate commit; compact external-review handoff recorded after the validated push |
| 2026-08-05 | Liturgy reader visual-reset direction selection | Independent review selected Liturgical Instrument as the production visual foundation and froze Quiet Folio and Contemporary Reader as comparison references. Selection closes the three-direction study but does not authorize production-integration execution or public cutover. Seven bounded visual blockers move into the separate Instrument correction candidate. | Reviewed end `0f3567dc509a2d5b42fd58a0e4c77c8f5e5dc113`; implementation `7233879350ff00c92fa2029ca04f481125daa519`; correction review remains open |
| 2026-08-06 | Liturgical Instrument correction — Work unit A | Candidate geometry correction pending the remaining Instrument finish and independent review. Read now uses one 39.75rem axis, measuring 636 px and about 75 characters at 768×1024 instead of 726 px/about 86. Missal preserves identity and the semantic cue grid while advancing the first principal text from 474.58 to 316.98 px at 1440×900, 441.77 to 324.97 px at 393×852, and 458.83 to 342.03 px at 320×852. The rebuilt preview passed all 12 Chromium assertions with no console, network, accessibility-name, or horizontal-overflow result. Shell/masthead and warning/rhythm correction remain next; accepted behavior and public routes remain unchanged. | This geometry checkpoint; canonical measurements and continuity in `build/agent-continuity/liturgy-reader-visual-plan.md` |
| 2026-08-06 | Liturgical Instrument correction — Work units B/C | Candidate finish pending Work unit D gates and independent review. The desktop card becomes a square, shadowless rail aligned immediately outside the ritual plane; the mobile dock is opaque and edge-integrated. Instrument now uses a three-stroke CSS mark and no visible meaningless progress dash, while internal semantic progress remains. Roman partial coverage becomes one exact compact status and advances held text by 197.39 px; postconciliar missing-language notices retain exact text in restrained inline pairs and advance first held text by 198.66 px at 1440×900. Mobile exchanges tighten and the 320-pixel first division wraps deliberately in two lines. The 53-capture run passed 13/13 Chromium assertions with clean console, network, HTTP, accessibility-name, duplicate-ID, and overflow results. | This finish checkpoint; full matrix/gates/handoff and independent correction review remain open |
| 2026-08-06 | Liturgical Instrument correction — Work unit D review candidate | Candidate ready for independent correction review; no acceptance or cutover claimed. The immutable handoff records 22 required full-size final states, five blocker baselines, two contact sheets, explicit route/hash/geometry/focus/semantic/error metadata, 140 focused Python passes, 13/13 visual-reset Chromium passes, 27/27 Propers browser passes, 18/18 shared-shell passes, successful locked public-alpha build/verify, Pages run `31094868150`, and byte-matched deployed assets. Day browser is 33/34 because its date-dependent first-visit test expects no notice on the current default date; the governed full gate stops at pre-existing example transcript divergence after task-owned promised-ledger examples were corrected and independently replayed 2/2. Public Day/Propers and accepted seams remain unchanged. | Implementation `62e712a1962080d1dc3c6e106651c41afbf7531b`; handoff `build/agent-handoffs/20260806T112813Z-liturgy-reader-instrument-correction/`; independent review only remaining gate |
| 2026-08-06 | Liturgical Instrument correction — independent review round 1 | Changes requested, narrowly. The reviewer confirmed the selected direction and passed six of seven original findings, including reading hierarchy, Read measure, ritual action, warnings, masthead, title wrap, and normal mobile spacing. Review retained the original shell blocker at 1024×768, where the floating card returned, and identified related mid-word action-label breaks at 200% text. Production-integration execution and public cutover remain unauthorized. | Reviewed commit `50288ddf9759f56e8a25e4907d8de25e27e25e8f`; exact disposition and bounded response in `build/agent-continuity/liturgy-reader-visual-plan.md`; narrow correction/re-review pending |
| 2026-08-06 | Liturgical Instrument correction — Round 1 shell checkpoint | Candidate correction pending successful deployed parity, immutable re-review handoff, and independent re-review. Instrument now transitions directly from the accepted 72rem ruled rail to an opaque, square, shadowless edge dock; a root-font-aware extreme state uses four whole labels in a 2×2 grid. The authoritative run records 15/15 Chromium assertions and 54 captures with exact opacity, end reserve, names, targets, overflow, focus, and normal-scale regression coverage. Focused Python is 141/141, Propers 27/27, shared shell 18/18, and Day retains only its unchanged current-date 33/34 stop. The first Pages attempt passed artifact build/verification/upload but timed out while the deployment remained externally queued; corrected deployed parity is not claimed. | Correction `ab89758e3f3ee165e0141e3605be88051450134b`; Pages run `31104342722` failed at queued-deployment timeout; continuity owns the exact evidence and stop |
| 2026-08-06 | Liturgical Instrument correction — Round 1 deployment follow-up | A second automatic Pages run for the truthful continuity checkpoint again passed checkout, locked setup, source verification, public build, Pages compatibility verification, configuration, and verified-artifact upload, then stopped only when deploy-pages polling reached its 600-second timeout. Deployed Day/Propers remain healthy and noindex but retain reviewed CSS, so corrected parity is still explicitly open. | Continuity checkpoint `c6b7f7f0a79468cfa1a503235044c92bd88c27b2`; Pages `31106008011`; another ordinary push-triggered attempt will accompany the next record |
| 2026-08-06 | Liturgical Instrument correction — Round 1 narrow re-review package | Candidate shell correction is fully measured and packaged for the three-question re-review. A third automatic Pages run again verified and uploaded the correct artifact but was canceled at the job's 15-minute ceiling during deploy polling; public prototypes remain HTTP 200/noindex with reviewed pre-correction CSS, so corrected parity is an explicit external blocker rather than a claimed pass. The handoff contains exact Round 1 correspondence, two blocker pairs, 11 original-pixel regressions, two inspected contact sheets, 15/15 browser assertions, focused sources, checks, and a runnable noindex candidate. | Correction `ab89758e3f3ee165e0141e3605be88051450134b`; checkpoint `3873bd99cb308432404378c665dbcb3246144c9e`; Pages `31107294462` cancelled; handoff `build/agent-handoffs/20260806T132759Z-liturgy-reader-instrument-correction/`; independent re-review and corrected deployed parity open |
| 2026-08-06 | Liturgical Instrument correction — Round 1 deployed re-review candidate | Pages run `31109086658` completed successfully for the immutable-handoff commit. Direct unlinked Day/Propers routes return HTTP 200/noindex and deployed CSS/JS byte-match source, resolving the earlier external polling stop. A fresh post-deployment immutable package keeps canonical continuity byte-identical and records the successful run and hashes. The candidate remains pending only the three-question independent visual re-review; production-integration execution and public cutover remain unauthorized. | Handoff commit `c388ab42dfc4f5c7d49abc71596d6bb511af5742`; final package `build/agent-handoffs/20260806T141831Z-liturgy-reader-instrument-correction/`; independent re-review only remaining gate |
| 2026-08-06 | Liturgical Instrument correction — independent Round 1 acceptance | Accepted. The reviewer independently tested the immutable ZIP, verified all 109 manifest entries and source/candidate CSS parity, inspected the blocker sheets and 11 original-pixel captures, and passed all three bounded questions: continuous shell integration across 1440/1024/768/393/320, whole usable labels at 200%, and no regression to accepted geometry or behavior. Liturgical Instrument is the accepted production visual foundation and production-integration execution may begin through the smallest shared presentation seam. Public navigation and cutover remain unauthorized. Pages run `31110517661` for post-deployment evidence commit `4daf7d8a1e1c509edb81a738cc71223170bbbd2d` failed at deploy polling and is not treated as successful; deployed parity remains owned by successful run `31109086658` for `c388ab42dfc4f5c7d49abc71596d6bb511af5742`. | Correction `ab89758e3f3ee165e0141e3605be88051450134b`; accepted deployed handoff `c388ab42dfc4f5c7d49abc71596d6bb511af5742`; reviewed package `build/agent-handoffs/20260806T141831Z-liturgy-reader-instrument-correction/`; production integration next, independent integration review before cutover |
| 2026-08-06 | Liturgical Instrument acceptance-record deployment settlement | Acceptance/tracking commit `1608f0ee0ee61df956247072a91647147548c5ad` changes no product or public route. Pages run `31113461987` passed checkout, locked setup, source verification, public build, Pages compatibility verification, configuration, and verified-artifact upload, then failed after deploy-pages polled `deployment_in_progress` for 600 seconds. Direct Day/Propers Instrument routes remain HTTP 200 with the complete noindex policy; deployed CSS `850e1acacb6f487a5c2f3118388b3fce7b96f9db667e783ba35cdef7d9918b48` and JavaScript `eb1c1dd5c0c9c7076b74f2187627dc56e39963429212c0a51872df0ea98a9679` byte-match source. The failed run is not a successful deployment and does not supersede accepted successful parity run `31109086658`. | Acceptance `1608f0ee0ee61df956247072a91647147548c5ad`; Pages `31113461987` failed at deployment polling; production hook inventory remains next |
| 2026-08-06 | Liturgical Instrument production integration acceptance and durable closeout | Accepted. Independent review passed all six production-integration questions with no product, visual, evidence, harness, deployment, source-ownership, accessibility, or isolation correction. Exact production commit `5444d89fc9b379a1babef5b2220323fe1508b2b3` owns successful Pages run `31125898045` and direct deployed/source parity. The sole process finding—an ignored local review package—is closed by the path-authorized archival commit, which pushes the byte-identical reviewed directory and ZIP with 216/216 manifest entries, one top-level directory, and ZIP SHA-256 `ebf0361309ac33b4580cbb535e4bbd3eabd144756e6c078aa140e716c748f05f`. The Day date-dependent 33/34 result and unrelated example-transcript full-gate stop remain honestly disclosed. Separate cutover planning may begin after closeout; public navigation and cutover execution remain unauthorized. | Implementation `3cd46072b164ff39b00639bb67ad6b8943a255dc`; deployed state `5444d89fc9b379a1babef5b2220323fe1508b2b3`; archival commit `8c6e1270f692ca4136f2f6a60002bacd3af0440c`; exact review and response in canonical continuity |
| 2026-08-06 | Liturgical Instrument public-cutover planning kickoff | In progress from clean synchronized boundary `7b7044dea7f5c35a2d32ff85f26eb5b182bf40ef`. Planning will map the canonical and accepted-candidate route/state/loading contracts, select one same-URL reversible mechanism, classify all differences, repair only the known clock-dependent Day test if safely proved, and prepare an unapplied patch, exact rollback/gates, and immutable review handoff. Initial inspection identifies static candidate indexing, legacy Day fallback/self-link, first-visit default, provisional Propers option-key, and lost direct cross-entrance navigation questions that must be resolved explicitly. No canonical page, public navigation, candidate, oracle, or cutover byte is changed or authorized by this phase. | Deliverable `liturgy-reader-instrument-public-cutover-plan-2026-08-06`; canonical continuity owns exact progress and stopping point |
| 2026-08-06 | Liturgical Instrument public-cutover plan review candidate | Candidate for narrow independent planning review; no cutover or navigation authorization claimed. The route/load/publication map selects same-path source promotion behind unchanged `day.html` and `index.html`, rejects redirects/renames/build aliases, inventories every owned navigation link, classifies URL/state differences in Markdown and JSON, and defines ordinary-revert rollback plus exact local/oracle/Pages/cache gates. Day's only 33/34 failure was proved clock-dependent and now passes 34/34 through an empty-URL test-only clock fixture. The proposed mechanical patch is tracked but unapplied; review must resolve the empty-Day default, deferred Day reasoning/territorial behavior, stable Propers option keys, candidate/canonical metadata and wording, and direct cross-entrance/context access before execution. Canonical pages, navigation, candidates, and oracle remain byte-identical to the starting boundary. | Planning `c7124de25`; deterministic test `5e1b82b51`; record checkpoint `2cf91dd01`; handoff `build/agent-handoffs/20260806T212148Z-liturgy-reader-instrument-public-cutover-plan/`; independent plan review is the only next phase |
| 2026-08-06 | Liturgical Instrument public-cutover plan review and compatibility closure | Plan direction accepted; compatibility closure in progress. Independent review accepted same-path source promotion, rollback, static-hosting, deterministic-Day, canonical-route, and visual-oracle architecture, then bound the remaining public contract: Roman 1962 empty-Day default; preserved source-derived `why=1`; every held territorial branch without inference or a new public locality key; stable Propers `cycle`, `alternative`, and `translation-witness`; source-static retained-candidate noindex; route-neutral wording; and Details-based counterpart/context links. Candidate/shared implementation and evidence are authorized, but the reviewed patch remains deliberately unapplied and must be regenerated and narrowly re-reviewed. Production integration and its durable handoff remain accepted complete. Canonical Day/Propers HTML and public navigation remain byte-unchanged; canonical promotion, public navigation changes, cutover execution, and candidate/oracle cleanup remain unauthorized. The governed full gate remains honestly non-green at unrelated stored example-transcript divergence. | Exact review and bounded response are in canonical continuity; compatibility implementation, evidence, regenerated patch, immutable handoff, checkpoint commit, Pages result, and narrow re-review are pending |
| 2026-08-07 | Liturgical Instrument public-cutover compatibility implementation | Candidate/shared compatibility is implemented and deployed for narrow review without touching canonical Day/Propers or public navigation. Commit `3f3949617a04ffa68a1070058d0f7bc5ac74dc93` preserves source-derived `why=1`, every held territorial branch, stable public Propers option keys with legacy input-only aliases, static candidate noindex, route-neutral visible wording, and Details-based related/context navigation. Pages run `31148986910` succeeded for that exact commit with direct HTTP and deployed/build/source parity. Day passes 40/40, Propers 32/32, shared shell 18/18, and visual assertions 24/24 over 113 captures; literal document reload now covers ordinary and territorial Why, and the evidence includes a mobile view of the second held branch. The obsolete draft patch is not executable and will be replaced from the exact evidence baseline. Canonical promotion, public navigation, cutover execution, and candidate/oracle cleanup remain unauthorized pending narrow review. | Compatibility `3f3949617a04ffa68a1070058d0f7bc5ac74dc93`; Pages `31148986910`; regenerated patch and immutable compatibility handoff next |
| 2026-08-07 | Liturgical Instrument public-cutover compatibility review candidate | Ready for the seven-question narrow independent review. Evidence baseline `998648c341691c0807b0c209f93fbae16d641d48` adds literal reload proof and a mobile view of the second held territorial branch without changing product bytes; Pages run `31150296458` succeeded. The regenerated normal-context future patch passes `git apply --check`, proposes only canonical entry points plus exact release/test/tracking ownership, and leaves compatibility code, candidates, shared seams, navigation, and oracle untouched. The immutable package contains the verbatim review/response, 13 original-pixel compatibility states, full browser results, locked validation, hashes, source snapshots, and rollback/gates. Canonical sources remain at their reviewed legacy hashes. Cutover and navigation remain unauthorized pending review. | Compatibility handoff `build/agent-handoffs/20260807T052836Z-liturgy-reader-public-cutover-compatibility/`; independent review only next |
| 2026-08-07 | Liturgical Instrument public-cutover execution candidate | The independently authorized same-path execution replaces only canonical `day.html` and `index.html` source markup/load graphs with the accepted compatibility-closed readers, retains the filenames and hash/query contract, updates exact publication bindings, and re-owns the governed canonical-route tests. No redirect, public-navigation change, candidate/oracle cleanup, renderer/state/data refactor, or visual redesign is included. Retained candidate and oracle routes remain noindex. Deployment and independent cutover acceptance remain separate gates, with ordinary revert as the immediate rollback. | This bounded cutover commit; exact Pages run, deployed parity, cache-window verification, and review disposition remain to be appended |
| 2026-08-07 | Liturgical Instrument final public-cutover acceptance | Accepted and complete. Canonical Day and Propers serve the accepted Instrument at their unchanged filenames with no redirect; all nine independent review dispositions pass. Exact cutover `9b5f21c0ca26bf02af03d207ddd2617021e16fb3` owns successful Pages run `31175722949`, deployed-byte parity, 936/936 immediate assertions, and 216/216 post-window assertions without mixed generation. Public navigation is unchanged. Retained candidate and oracle routes remain intact and nonindexable; cleanup is deferred and unauthorized. The unrelated stored-example full-gate replay remains honestly non-green and was not blessed. | Execution handoff `build/agent-handoffs/20260807T115341Z-liturgy-reader-instrument-public-cutover-execution/`; ZIP SHA-256 `06752126a3a3235a342f54ec08811faaf4fc2622924008c4362dda519624c410`; final acceptance in canonical continuity |
| 2026-08-07 | Live Reader — Ritual Flow & Orientation kickoff | In progress as a distinct production refinement phase after the accepted cutover. RF-A maps and captures live sustained-reading states and classifies only source-owned semantics; RF-B adds a quiet persistent ritual locus; RF-C makes Contents open on its accessible current place; RF-D restores visual hierarchy between principal action and proved rubric/reference/provenance material; RF-E tunes deep desktop/mobile rhythm while protecting the accepted first viewport and 636-pixel portrait Read measure. No liturgical applicability is inferred. Migration, navigation, candidate/oracle cleanup, search, Study/Compare, print, source, translation, and recension scope remain closed. | Start `1bca6a0ee862fce5873d6b0c2d92389e78ca018b`; deliverable `liturgy-reader-live-ritual-flow-2026-08-07`; canonical continuity and RF-A evidence own the next checkpoint |
| 2026-08-20 | Missal-mode seating — printed order, qualified variants, and the moved freeze | **Not externally re-accepted; recorded so the change is not silent.** Two defects kept 243 of 491 Masses out of Missal mode. First, a 2026-08-08 scripture wave had appended propers above the orations in 49 formularies, so the seating walk broke at the Collect; the printed order was restored from the CMAA facsimile (Commune unius Martyris I, marginal nos. 4193-4203) and is now enforced by `order_problems` in check-calendar-masses with a self-cleaning `proper_order_exceptions` ledger for the eleven rites that genuinely leave the frame. Second, 95 of the remaining 105 refused on propers the reader had already placed: a slot may now declare `qualified` and claim `<name> (<qualifier>)`, on Ritus servandus V, 2 / VII, 7 / XI, 1, and the Gradual slot gains `Sequence` and `Greater Alleluia` on RS VI, 1 and the Proprium rubric at Sabbato in albis. Refusals fell 243 -> 105 -> 17. **The acceptance freeze in `tools/tests/test_day_missal_integration.py` moved for the second time**, for the same reason it moved on 2026-08-08: completing the propers and commons necessarily rewrites `src/sources/calendars` and `src/web/data`, which that guard pins, and this change also edits `ordinary-seating.js`, which it hashes. What is NOT claimed: nobody has re-accepted the readers against the data or the seating engine as they now stand, and the Missal-mode fail-closed guard in `day-reader.js` is untouched -- admitting riding propers and rendering `before`/`after` through the legacy stated aside remain proposed and unlanded, needing this ledger's own process. | `b24a3e3fd`, `0893e5e8a`, `5d6c92627` |
| 2026-08-20 | Missal mode — a day of several Masses is seated as one | **Diagnosed and measured; fix written and deliberately NOT applied.** A day that prints several Masses carries them as `forms`, and `mass-propers structure` flattens that block into one `propers` array whose entries keep only a `form` label — a mass carrying forms has no `forms` key in the served file at all. `seatPropers` therefore reads three Masses as one, and the second Introit sends the walk backwards at the first slot it reaches, so the second and third Masses lose their seats and the reader refuses the day. Christmas Day and All Souls are the 1962 cases; the postconciliar Pentecost is another. Measured: seating each form on its own closes 2 of the 1962's 17 remaining refusals and 6 of the postconciliar's 30, 8 masses across both editions. A patch is written at `.scratch/lanes/forms-seating-defect/ordinary-seating.patch` and is additive — `formsOf` and `propersOfForm` helpers, a subsequence and never a reordering, and a caller that names no form gets byte-identical behaviour. **Two reasons it is not landed.** It is inert alone: which of several Masses a reader is at is not deterministic from the data, so a caller must name the form, and that is a reader decision this ledger owns. And it edits `ordinary-seating.js`, which the acceptance freeze hashes and which this branch has already moved twice; a third move for a change that would observably do nothing is not a trade this lane may make. | proposal and measurement in the lane directory; no commit |
| 2026-08-27 | Missal mode — stable Mass forms supersede the unlanded flattening patch | **The 2026-08-20 diagnosis is historical and its patch must not be applied.** Generated Masses with authored alternatives now carry an ordered `forms[]` manifest whose stable `forms[].id` values partition the legacy flat Proper sequence, and every nested Proper carries its matching `form_id`. The shared reader adapter requires that exact partition, refuses an implicit default when several forms exist, and preserves each selected form's original flat source offsets. This closes the old data-shape blocker without label inference or the lane's obsolete display-label patch; remaining alternative and exceptional-frame seating is tracked separately. | Current generated Propers structures, `properFormSelection`, and form-parity tests; no historical row rewritten |
| 2026-08-27 | Postconciliar Ordinary boundary recovery and browser evidence refresh | **Implemented, not externally re-accepted.** The Rite of Peace is now two elements at nn. 127 and 128; n. 127 carries only an explicitly uncollated 1861 antecedent because the target evidence does not establish the full response at that locus, and optional n. 128 remains text-free. Eucharistic Prayer I is represented by twelve option-bound children around the already-common n. 91 acclamation and n. 98 doxology; nine carry labelled antecedents, while Communicantes, Qui pridie and Supplices remain empty at their proved divergences. The generated postconciliar structure is 59 elements with 20 Latin antecedents, and no production browser JavaScript changed. The Day Chromium harness now resolves EP I to Te igitur, counts all twelve selected children, and passed that keyboard focus/location assertion plus 39 other source-only assertions. Its sole 40/41 failure was the concurrent source-only Proper scratch fixture saying the January 15 Mass lacked its own oration slot; it did not touch this Ordinary sequence. This row records refreshed acceptance evidence, not a new external blessing. | Working-tree recovery; `mass-ordinary check --calendar postconciliar` current; focused Ordinary/source tests 17/17; Day source-only Chromium 40/41 with the EP-I assertion green |
| 2026-10-19 | Daily reader recovery and completion planning | Recovered baseline `c6da24eda429337fe13d59420a3c489a98a16e66`; reconciled accepted cutover/remediation with unfinished ritual-flow and modes; recorded scoped translation inventories, coverage-counter defects, cue/paragraph defects, the C1–C6 execution plan, representative-Mass pattern, and acceptance gates. Planning only; implementation remains open. | This planning change; promise `missal-reader-completion-plan-2026-10-19`; recovery commands and evidence owners in the current completion-plan section |

For later updates, append a dated row with the workstream or unchanged
historical phase name, the evidence-backed result, and the exact commit(s).
Do not rewrite a completed row to make later sequencing look cleaner.
