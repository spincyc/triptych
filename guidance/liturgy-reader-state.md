# Liturgy Reader State and Semantic Fixtures

## Status and scope

This is the implementation guide for the M1 candidate named in
[`liturgy-browser-roadmap.md`](liturgy-browser-roadmap.md). The governing
product contract remains [`liturgy-browser-vision.md`](liturgy-browser-vision.md).
This guide explains the shared state and regression artifacts without
repeating either document.

The DOM-free contract is
`src/web/browser/liturgy/reader-state.js`. Consumer projections are in
`src/web/browser/liturgy/reader-state-adapters.js`. Both use the existing
browser-global/CommonJS pattern. Neither production route loads them during
this candidate, so current Day and Propers behavior is unchanged while the
integration boundary is externally reviewed.

## Versioning

Reader states use `triptych-liturgy-reader-state/v1`; fixtures use
`triptych-liturgy-reader-fixture/v1`; parsed URL envelopes use
`triptych-liturgy-url-state/v1`.

The meaning of a version is frozen after acceptance. This still-unaccepted M1
candidate may be tightened in response to review before that boundary is
accepted. After acceptance, an optional field may be added to v1 only when
absence remains valid and every consumer preserves it safely. Rename a field,
narrow or broaden an identity, reinterpret a state, or make an optional field
required only in a new version. Validators reject an unknown version.

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
other future state fields are representable now, but their public URL spelling
remains provisional until the owning roadmap milestone integrates them.

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
composed text with another. The future public URL spelling of cycle selection
remains provisional.

Day Compare fixes the state's civil date and a named territorial context, then
resolves each edition side independently before comparing semantic units.
Propers Compare fixes corresponding edition-qualified formularies and rejects
a civil-date anchor.

## Legacy URL compatibility

The v1 inventory is:

| Route | Hash keys | Query keys |
| --- | --- | --- |
| Day | `date`, `missal`, `bible`, `orations`, `why`, `ordinary`, `ordinary-lang`, `rubrics`, `mass`, and manifest-declared Ordinary variant keys (currently `eucharistic-prayer`) | `data` |
| Propers | `missal`, `type`, `mass`, `bible`, `orations` | `data`, `missals` |

The contract preserves current spelling and canonical route order. Unknown
legacy pairs remain in a compatibility envelope and round-trip with both key
and value encoded. Canonical serialization spells out every current
preference-sensitive semantic value, including values equal to repository
defaults, so another reader's stored preferences cannot reinterpret a shared
URL. A variant key valid in another edition is preserved as inert and is never
applied across editions. Duplicate semantic keys and an explicit value invalid
under the selected manifests fail closed. Unknown future `cycle` or
`alternative` keys are preserved but cannot affect semantic state before their
public contract exists.

URL fields outrank valid remembered preferences, which outrank
repository-declared defaults. A throwing or absent storage adapter yields no
remembered preferences and does not fail the reader. The contract has no
storage or geolocation dependency and never infers territory. Because it is
not yet wired to the pages, current legacy behavior remains deployed exactly
as it was; the candidate tests establish the stricter integration rule rather
than silently changing public URLs.

The inventory also records current defects for later scoped integration: the
pages presently coerce some invalid explicit values, Day history navigation
does not fully restore `why` or clear an absent Ordinary variant, and the
shared self-written-hash marker can mistake a later Forward navigation for its
old event. This M1 candidate does not change those behaviors.

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

## Candidate boundary

This work is an M1 candidate pending external review. It does not accept M1,
integrate a visible mode, redesign the reader shell, add Propers search or
comparison UI, change calendar or liturgical data, or begin recension work.
