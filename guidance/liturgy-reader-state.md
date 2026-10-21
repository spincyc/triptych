# Liturgy Reader State and Semantic Fixtures

## Status and scope

This is the implementation guide for the accepted M1 contract named in
[`liturgy-browser-roadmap.md`](liturgy-browser-roadmap.md). The governing
product contract remains [`liturgy-browser-vision.md`](liturgy-browser-vision.md).
This guide explains the shared state and regression artifacts without
repeating either document.

The DOM-free contract is
`src/web/browser/liturgy/reader-state.js`. Consumer projections are in
`src/web/browser/liturgy/reader-state-adapters.js`. Both use the existing
browser-global/CommonJS pattern. The canonical Day and Propers routes load both
modules before their entrance-specific reader controller; the retained legacy
route names canonicalize to those same public entrances.

## Versioning

Reader states use `triptych-liturgy-reader-state/v1`; fixtures use
`triptych-liturgy-reader-fixture/v1`; parsed URL envelopes use
`triptych-liturgy-url-state/v1`.

The meaning of v1 is frozen at the accepted snapshot
`c1a590f5854215d68d167d9040e188f41762663e`. An optional field may be added to
v1 only when absence remains valid and every consumer preserves it safely.
Rename a field, narrow or broaden an identity, reinterpret a state, or make an
optional field required only in a new version. Validators reject an unknown
version.

## Reader-state boundary

Every state names `entrance` explicitly. It is never inferred from a missing
date.

- `day` requires a real civil date, a stable edition identity, and a stable
  calendar identity. Optional territory and locality are stable nested
  identities, never labels. Readable formulary, Bible and numbering,
  language selections, Ordinary options, cycle, alternative, semantic
  location, apparatus hooks, coverage, choices, and comparison are conditional
  fields. It may not carry the Propers `formulary` or `browse` fields.
- `propers` requires a stable edition identity and an edition-qualified
  formulary identity. A future unselected landing state uses the explicit
  `browse: {"kind": "browse-entry"}` sentinel instead; `formulary` and
  `browse` are mutually exclusive. Civil date may be stated only as explicit
  `null` to record date independence. Calendar and selected-readable-Day fields
  are forbidden. Known calendar uses never become part of formulary identity.

Optional cycle codes are strings; an alternative is a stable identity;
original, translation, oration, and Ordinary language/witness selections use
the contract's closed language-field names; and legitimate option groups map a
stable group ID to a stable option ID. Invalid shapes fail validation rather
than surviving as arbitrary extension data.

The v1 top-level field vocabulary is closed in code. Unknown fields fail; v1
has no implicit extension data. `apparatus`, when present, is an object whose
only fields are optional Boolean `why` and `rubrics` selections. Every
conditional field is validated by property presence, so `false`, an empty
string, an array, or a wrong object cannot bypass validation. `null` is not a
generic absence spelling. Its documented state-level meanings are: a Propers
`civilDate` asserts calendar independence; `requestedMode: null` states that no
mode was requested; `cycle: null` states that no cycle was selected; and
`comparison: null` states that no comparison was requested. Bible numbering
may be `null` when an edition declares no separate numbering identity, and Day
territory or locality may be `null` for the universal or non-local branch.
Other inapplicable fields are omitted.

`requestedMode`, when present, is `null` or one of `read`, `missal`, `study`,
and `compare`. A non-null comparison requires Compare mode, and Compare mode
requires a valid non-null comparison. Comparison anchors remain entrance
specific as described below.

Stable IDs carry identity. Edition names, celebration titles, translated
headings, control labels, DOM IDs, CSS classes, notice prose, and current
disclosure state do not. `requestedMode`, semantic location, comparison, and
other future state fields are representable now. The integrated public URL
spellings are `mode` for `requestedMode` and `location` for an exact semantic
event ID. `compare` names an implemented comparison dimension; its explicit
peer keys remain entrance-specific.

The adapters accept resolved data; they do not fetch it. Day receives the
existing `MassAssembly.derive()` result. Proper and Ordinary data remain the
generated structures. `OrdinarySeating` remains the only seating and event
order implementation. The CLI adapter consumes `mass-today --expanded` JSON
and joins it to those same stable structures; it never parses terminal
headings. This keeps calendar resolution, browser presentation, and terminal
formatting outside the contract.

## Semantic results

An event ID is a source coordinate, not a heading scrape:

- an Ordinary section is `ordinary-section/<section.key>`;
- an Ordinary element is `ordinary-element/<element.key>`;
- a Proper is `proper/<edition-id>/<formulary-id>/<three-digit-source-ordinal>`.

The Proper ordinal is stable within a generated-data revision and across
Read/Missal projections because placeholders retain their source positions. It
is not a permanent citation if a lawful source correction inserts or reorders a
Proper. The semantic hash makes that revision visible; adding durable
source-owned per-Proper IDs would require an explicit contract-version decision
rather than silently changing existing coordinates.

The Proper coordinate identifies an occurrence. `semanticSlot` is a typed
cross-edition alignment identity from the adapter's closed vocabulary;
`editionSlotLabel` retains the generated Proper `name` only as an edition-local
label. A role without a defensible alignment is explicitly
`edition-local-unmapped`, never slugged into identity from its label. Form,
source kind, selected cycle, selected references or composed-language witness,
seat, rights, and provenance hooks remain separate assertions. Future semantic
comparison aligns the stable slot identity and its structured context, not the
edition-local event ID, label, or line number.

Fixture `semanticHash` is SHA-256 over the ordered event IDs joined by a single
line feed, with no trailing line feed. It detects order or identity drift while
excluding text, labels, formatting, generated timestamps, and DOM structure.
Exact selected text remains owned by existing source and browser/CLI tests;
fixtures assert its stable citation, language, witness, rights, and provenance
identity instead of copying Mass text.

## Coverage, absence, and choice

Coverage rows are scoped and discriminated:

- `supported` is `complete` or `partial`;
- `unsupported` names an unsupported date, object, or missing Ordinary;
- `unavailable` names text not held or withheld, a missing translation or
  language, or an unresolved citation;
- `absent` records explicit semantic absence.

Reasons retain repository-owned terms such as `Placeholder`, `unresolved`, and
Ordinary `absenceKey` values. Availability completeness does not assert that a
source claim has been independently verified. A correctly absent unit is not
silently treated as incomplete coverage.

An open coequal choice is `unresolved-authorized-choice`. It preserves a
reason, at least two uniquely identified options, and source hooks. It may not
carry a selected or default option. The resolver accepts only an explicit
answer or a separately supplied deterministic source result; it has no first
array, manifest, DOM, or incidental-source-order path. Multiple translation
witnesses likewise remain unresolved unless the request identifies a witness.

Cycle-bearing material on the calendar-independent Propers entrance follows
the same rule. An explicitly requested held cycle selects only that cycle; an
invalid explicit cycle fails closed; and a single held cycle is deterministic.
When two or more cycles remain held with no request, selected semantic material
is a `cycle-alternatives` result with `choice-required` availability. Each
alternative retains its own stable cycle identity, citations or composed
material, rights, availability, and source hooks. Stable-key sorting may make
the representation canonical, but may never choose an alternative. The adapter
neither concatenates mutually exclusive readings nor overwrites one cycle's
composed text with another. The Propers URL uses the stable `cycle` key for an
explicit cycle and the stable `alternative` key for another explicitly named
alternative. The shared contract validates their nonempty identities; whether
the selected production formulary holds them remains adapter-owned and fails
closed when it does not.

The optional `properChoices` map names complete source group identities
(`proper-choice/<edition>/<mass>/<form>/<group>`) and their option IDs. Both
entrances serialize it as sorted JSON in `proper-choices`. The Propers scalar
`alternative` remains compatible for one group; declaring the same group in
both forms refuses. Adapters reject stale groups, options not held by their
source group and incompatible cycle selections. A valid source option may
still carry a typed body or translation gap; selecting it does not make its
words held.

Native controls accumulate independent group selections and preserve their
semantic focus. Date, edition, type, Mass or form changes clear stale choices;
presentation changes retain them. The map selects groups already supplied by
the generated source data. It creates no appointments, inferred applicability
or allowed-path relation between source-correlated groups.

The producer's exact `appointment_identity` is distinct from terminal wording
provenance. The calendar schema owns anchored groups, optional source-qualified
`seat: reading-1`, applicability facts and explicit inherited-group replacements.
Shared Seating validates these before either framed or unframed execution.
Day consumes the existing derived owner season and exact selected source Mass
identity. Calendar-independent Propers may qualify a seasonal view by an
explicit held option, never by inventing a date. An explicit choice cannot
attest unknown subject eligibility; an option covering the whole unknown
subject domain remains selectable without asserting that fact.
Source-use facts additionally require the shared owner's exact positive
canonical winner, candidate and selected said-readable tuple. Borrowed-winner
context does not establish usage for a different selected commemoration.
Propers and incomplete canonical context leave source use unknown; source
choices and URL state cannot supply that fact.
Unsupported inherited-recension applicability remains a text-free
`appointment_applicability` marker and refuses execution; it is not a
proper-body witness gap. See the
[calendar schema](../src/sources/calendars/README.md#source-owned-applicability-and-exact-choice-anchors).

Mixed owned text follows the composed-text witness/absence selector. Its
optional `selected.scriptureComponents` carries only Bible ID, numbering and
references; it does not replace a missing whole chant body. Pure Scripture
continues through its existing Bible reconstruction selector.

A source-owned `proper_source_paths` relation may additionally constrain
several groups to one held reading set. Its qualified `properChoices` identity
selects a path ID; the source path supplies the exact compatible sibling tuple.
Conflicting sibling choices refuse. Native path controls, CLI choices, Share
and Print use the same state map and source admission owner. The calendar's
cycle remains distinct from each admitted material cycle, including a held
Year A set authorized on a Year B or C calendar day. Missing actual-use facts
remain unresolved even after an explicit path selection. No URL or choice
attests an evening celebration, an Ascension arrangement or previous reading
use. See the [source contract](../src/sources/calendars/README.md#correlated-source-paths).

Day Compare fixes the state's civil date and a named territorial context, then
resolves each edition side independently before comparing semantic units.
Propers Compare fixes corresponding edition-qualified formularies and rejects
a civil-date anchor.

The integrated Propers comparison dimensions are `oration-language`,
`lectionary-cycle`, `reading-alternative`, `translation-witness`, and
`bible-edition`. A cycle comparison names both
held cycles explicitly. A reading-alternative comparison uses full source
option identities from one held choice group, such as
`proper-choice/postconciliar/presentation-lord/main/gospel/longer`. It selects
that option without discarding the other source evidence or resolving another
choice group. Each comparison holds the other semantic selections fixed;
equal, missing, unknown, cross-group, or mixed-dimension peers refuse. Bible
expansions retain their reconstruction qualifications and establish no civil
date applicability. A translation-witness comparison explicitly names the primary
`translation-witness` and `peer-witness` in the same selected language; aliases
of one canonical witness cannot form two sides. Partial witnesses are the union
of held selected-unit coverage, and each missing witness body stays unavailable.
This axis uses `same-source-event` correspondence only within one identical held
structure object and edition/formulary/form revision. Every event must match its
unique `proper-structure` hook and exact source owner; duplicate, mismatched or
missing coordinates refuse comparison. Units carry a `sourceCoordinate` and
`compare/source/<Proper-event-id>` location, including units without a proved
cross-edition semantic slot. Display labels and input array order never define
correspondence. Other comparison axes retain their mapped functional-slot guard;
this source-coordinate rule grants no cross-edition equivalence.

A Bible-edition comparison explicitly names both `bible` and `peer-bible` from
the currently publishable Bible manifest. The peers must be distinct and keep
the manifest's own numbering. Edition, source formulary/form, Proper language,
translation witness, cycle, reading alternative, legitimate options, and
`textDisplay` stay fixed. Each side fetches and renders its own fragments through
the existing citation/locus conversion. It uses the same checked source-coordinate
rule as witness comparison; a label, an array position, or a cross-edition slot
never substitutes for source membership.

Each Bible cell carries `bibleCitations` evidence: citation reference, coordinate
resolution `resolved` or `refused`, and the precise refusal reason. Resolved
coordinates do not guarantee complete fragments: the existing renderer retains
chapter-load failures and missing-verse notices. This evidence describes the selected
Bible independently of the adapter's structural Proper availability. A mixed
Proper may retain held composed text while a cited Bible passage refuses; a
held passage in the other Bible cannot supply a replacement. Empty citation
lists mean that the source unit is not scriptural. Existing Bible reconstruction
and numbering qualifications remain visible, including in print. These renderings
establish neither exact Missal wording nor approved Lectionary wording, date
applicability, a new source correspondence, or new publication rights.

Day's recension comparison remains independently resolved
for its explicit date and territorial context.

## Legacy URL compatibility

The v1 inventory is:

| Route | Hash keys | Query keys |
| --- | --- | --- |
| Day | `date`, `missal`, `bible`, `orations`, `why`, `ordinary`, `ordinary-lang`, `rubrics`, `mass`, `form`, `translation-witness`, `mode`, `location`, `text-display`, `scripture-companion`, `compare`, `peer-missal`, `territory`, `proper-choices`, and manifest-declared Ordinary variant keys | `data` |
| Propers | `missal`, `type`, `mass`, `bible`, `orations`, `form`, `cycle`, `alternative`, `translation-witness`, `mode`, `location`, `text-display`, `scripture-companion`, `ordinary-lang`, `compare`, `peer-orations`, `peer-cycle`, `peer-alternative`, `peer-witness`, `peer-bible`, `proper-choices` | `data`, `missals` |

The contract preserves current spelling and canonical route order. Unknown
legacy pairs remain in a compatibility envelope and round-trip with both key
and value encoded. Canonical serialization spells out every current
preference-sensitive semantic value, including values equal to repository
defaults, so another reader's stored preferences cannot reinterpret a shared
URL. A variant key valid in another edition is preserved as inert and is never
applied across editions. Duplicate semantic keys and an explicit value invalid
under the selected manifests fail closed. Day and Propers
`translation-witness` values, and Propers `cycle` and `alternative` values, use
stable nonempty public identities. Their canonical order follows the five base
Propers keys, and serialization never uses implementation-scoped aliases.
Production adapters retain ownership of whether the selected formulary actually
holds the named choice or witness.

`form` is valid only beside an exact selected `mass` and names a
source-authored form ID held by that Mass. The internal single-form `main`
sentinel is omitted from public state and an explicit `form=main` refuses. A
multi-form Mass without `form` remains choice-required; a form without a Mass,
or an invalid form, fails closed without substituting or concatenating text.
`mode` uses the closed reader-mode vocabulary. `location` names an exact
semantic event and is restored only inside the selected result.

URL fields outrank valid remembered preferences, which outrank
repository-declared defaults. A throwing or absent storage adapter yields no
remembered preferences and does not fail the reader. The contract has no
storage or geolocation dependency and never infers territory. Both canonical
pages apply the contract now: invalid explicit semantic values refuse, route
aliases canonicalize without dropping the query string, and history state
retains the semantic location needed to restore navigation.

## Adding a fixture

Fixtures live only under
`tools/tests/fixtures/liturgy-reader-state/<version>/`; never place one below
`src/web/data`. To add one:

1. Choose a lawful tracked state and name its
   `tracked-production-data` basis paths, or mark it `synthetic-non-public`
   with a `synthetic-contract`, `nonPublic: true` basis plus
   `contractOnly: true`, `liturgicalText: false`, and
   `historicalClaims: false`.
2. Name the entrance and every requested identity explicitly.
3. Derive the expected result through the existing assembly, generated
   structure, and seating code. Keep edition labels outside identity and do not
   copy full Mass text.
4. Assert resolved identity, calendar result or explicit date independence,
   semantic event order and slot identity, selection availability, Bible or
   translation witness, rights, source hooks, seats where applicable, coverage,
   typed absences, choices, and legacy/canonical URL state where one exists.
5. Compute the semantic hash from ordered event IDs and run
   `tools/tests/test_liturgy_reader_state.py`.

Synthetic catalogs exercise the same validator as tracked data. Tests prove
their sentinel identities occur nowhere in generated public data and that the
release map contains the contract modules but no fixture path.

## Accepted M1 boundary

External review accepted the cycle-alternative and v1 property-presence model
after correction `c6b8070ae76e75153448895a19a0b916c18806ea` and final micro-fix
`c1a590f5854215d68d167d9040e188f41762663e`; the focused suite passed all 38
tests. That acceptance was the historical M1 boundary. The canonical Day and
Propers routes have since integrated the contract, adapters, visible reader
modes, and semantic-location restoration. Comparison UI remains outside this
contract; calendar, source, and recension changes still require their own
evidence and review.


## Latin accompaniment presentation

The optional v1 `textDisplay` field and additive `text-display` hash key accept
`selected` and `latin-and-selected`. Absence preserves the existing selected
language presentation and legacy canonical URL. An explicitly requested value
round-trips in both entrances; invalid or duplicated values fail closed. It is
not a remembered preference or a fifth mode. Comparison holds it fixed.

“Show Latin alongside translated prayers” pairs held composed and Missal bodies
within their existing Proper, selected cycle, or Ordinary element. A selected
Latin component appears once. Each side keeps its witness, rights, relationship,
checked internal structure and precise absence. The normalized primary selection
and event/Contents order are unchanged. Scripture remains the selected Bible
edition unless the separate companion selection below is requested. Source and
translation stanza/turn arrays are never zipped; source-owned alignment below an
element needs its own evidence.


## Latin Bible companion presentation

The optional v1 `scriptureCompanion: {id, numbering}` descriptor and additive
`scripture-companion=<Bible ID>` hash key name one held Latin Bible alongside
the primary selected Bible. Absence preserves the existing state, canonical URL,
requests and liturgical DOM. Explicit empty, unknown, non-Latin or duplicate URL selections
fail closed. This is separate from prayer `textDisplay`, is not remembered, and
stays fixed across every Compare axis. The primary Bible selection, event,
source hooks, coverage, semantic location and Contents order remain unchanged.

“Show Latin alongside the selected Bible” explicitly selects
`scripture-companion=clementine-vulgate`, the current publishable Latin edition.
Each citation pairs that edition with the selected Bible, identifying language,
edition witness, numbering, psalter and public rights state. A primary selection
of the same edition appears once. Each side independently reads the generated
`loci`, `edition_loci` and `refused` through the existing loader and renderer.
A refused or missing side does not suppress or borrow the other edition's text.
Bible reconstruction and exact-Missal-wording qualifications remain visible.

The citation is the common semantic fragment. Its loci, verses and paragraphs
retain their edition's order; there is no array zipping or runtime numbering
conversion. Finer verse, stanza or turn correspondence needs an exact
source-owned mapping or an explicit inexact/refused outcome. This presentation
does not claim such alignment or repair gaps in the held text.
