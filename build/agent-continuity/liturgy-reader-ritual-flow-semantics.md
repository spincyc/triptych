# Live Reader ritual-flow semantic inventory

## Governing rule

Presentation may expose and style semantic state already owned by production.
It may not infer a liturgical choice, applicability, locality, winner, source,
translation, or ritual classification from scroll position, CSS selectors, or
editorial knowledge.

## Existing ownership mapped before implementation

| Concern | Current owner | Available presentation fact |
| --- | --- | --- |
| Current semantic location | `src/web/browser/liturgy/reader-shell.js` over elements carrying `data-semantic-location` | Stable current Contents entry chosen at the shell's bounded reading threshold; passive scroll/resize events are coalesced through one animation frame. |
| Contents current row | `reader-shell.js` `setContents()` / `markCurrent()` | Exactly one generated Contents button receives `aria-current="location"`; its source element and group/label are retained in the shell's `sections` list. |
| Day Proper sequence | production assembly/adapters, then `src/web/browser/liturgy/day-reader.js` | `event.kind === "proper"`, source-owned edition slot label, rendered Proper element, and group `Appointed propers` or `Proper of the Mass`. |
| Day Ordinary divisions | production Ordinary plus seating event stream, rendered by `day-reader.js` and the shared Ordinary renderer | Source-owned section name and semantic event ID; existing Contents group is `Rites and divisions`. |
| Day Ordinary elements | production Ordinary element records and renderer output | Source-owned element record, event ID, rendered classes and text. A display label may be used only when held by the source/renderer; an internal key is not promoted as public liturgical wording. |
| Ordinary rubric | production Ordinary renderer output | Existing `.ordinary-element.is-rubric` classification is source/renderer-owned and safe for presentation hierarchy. |
| Ordinary selected option | production state and Ordinary seating | Existing `.ordinary-choice` and selected source-defined option are safe to present; no option may be selected by the orientation layer. |
| why apparatus | production assembly/rubrical result in `day-reader.js` | Existing `why=1` disclosure and source loci remain subordinate and are not recomputed. |
| Territorial branches | production assembly | Existing held branch identity and branch-specific semantic namespace remain authoritative; no geography is inferred. |
| Propers current item | production Propers events in `src/web/browser/liturgy/propers-reader.js` | Source-owned edition slot/Proper label and semantic element; no new selection is created. |
| Rail/dock | `reader-shell.js`, `reader-shell.css`, and final presentation in `reader-instrument.css` | Four-action shell, focus/modal/inert behavior, desktop rail, intermediate/mobile dock, and 200% reflow are frozen foundations. |
| Mobile identity metadata | canonical Day/Propers HTML plus route controller outcome/mode updates | Route identity and committed mode already exist; the locus must not create a second app header. |

## Safe classification policy

- **Principal/current:** a production Proper in the assembled stream, a
  production Ordinary element that is not source-classified as rubric or
  reference, or an explicitly selected source-owned option.
- **Rubric/instruction:** only renderer/source output already classified as a
  rubric.
- **Conditional/reference:** only an existing production flag, kind, selected
  state, or renderer class that positively proves the block is conditional or
  non-current. Conditional applicability is never derived from prose or IDs.
- **Source/provenance:** existing provenance, composed/source-note, coverage,
  or why apparatus classes and source loci.
- **Unknown/unclassified:** remains visible and conservatively styled until the
  production owner supplies a reliable distinction.

## Known limitation requiring conservative presentation

The existing Contents outline includes Ordinary divisions and appointed
Propers, but not every Ordinary element. A persistent unit label can therefore
be shown only where a source-owned public label is available. When no such unit
label is held, the locus will retain the current source-owned division rather
than convert an internal key into liturgical terminology.

Likewise, not every long Ordinary block is presently proved to be a
non-current reference form. RF-D may improve rubric, source-note, selected-option,
and positively classified conditional hierarchy. It must leave any uncertain
block visible and record the limitation rather than invent applicability.

## Completed source/DOM audit

The production chain is generated Proper/Ordinary data →
`reader-state-adapters.js` → `ordinary-seating.js` → Day/Propers renderer.
Ordinary seating filters only explicitly variant elements, orders Propers by
declared seats/anchors, and emits section, Ordinary-element and Proper events.
Day Read renders Proper events only. Day Missal renders the semantic stream
through `TriptychOrdinaryRenderer.renderSemanticFrame()`. Propers remains
Proper-only.

The generated Ordinary `kind` vocabulary is exactly `dialogue`, `form`,
`heading`, `prayer`, and `rubric`. The rendered `.is-rubric` class is the only
structured instruction classification. There is no structured
`instruction`, `conditional`, `reference`, or principal/subordinate field.
Ordinary elements may expose source-owned names, loci and speaker tags; absent
material uses notices; source/grant apparatus is already quieter markup.

The only structured Ordinary variants are the postconciliar Eucharistic
Prayers I–IV. Roman alternatives and conditions, Roman Prefaces, the several
postconciliar penitential acts/Creeds, and similar forms remain prose or
unresolved source choices. Therefore this phase cannot label or collapse those
forms as non-current, cannot appoint a Preface, and cannot select applicability.
It may retain the existing source-defined choice control and style positively
classified rubrics/apparatus.

Proper adapter `semanticSlot` values are exact name mappings, not general
liturgical inference. Several held names—including Lesson variants, alternative
readings/antiphons, Passion variants, Sequence, and Prayer over the People—are
deliberately unmapped. The public DOM also does not expose `semanticSlot`,
`sourceKind`, seat, condition, or provenance as presentation attributes. The
nearest preceding section heading is not a safe substitute because seated
Propers may follow a different visual section boundary. These gaps remain
unknown/unclassified.

Production semantic identity is safe and stable: Day and Propers nodes carry
`data-semantic-location`, `data-semantic-event-id`, an element ID, and a focus
target. Territorial branches namespace `data-semantic-location`; repeated raw
event IDs alone are not navigation-safe. The shell's curated Contents list is
therefore the locus authority. Group and label come directly from source-owned
Ordinary section names, edition-slot/Proper names, selected option labels, and
held territorial identities.

Representative safe anchors for the evidence harness include:

- Roman Lessons/Offertory: `ordinary-section/oblatio`, with Epistle, Gospel,
  Offertory and Secret Proper events in the same semantic stream.
- Roman Preface: `ordinary-section/praefatio`; individual emitted Prefaces are
  not proof of appointment.
- Roman Canon: `ordinary-section/canon`, including source-owned elements such as
  `canon/te-igitur` and the consecration forms.
- Roman Communion/conclusion: `ordinary-section/communio` and later seated
  Communion/Postcommunion Proper events; visual adjacency does not redefine
  the seat.
- Postconciliar Word, Gifts, Eucharistic and Communion divisions:
  `ordinary-section/liturgia-verbi`, `praeparatio-donorum`,
  `prex-eucharistica`, and `ritus-communionis`; only the explicitly selected
  Eucharistic Prayer state is current.

Postconciliar Ordinary English coverage is intentionally sparse in the held
witness, so a “deep Ordinary” state may contain source-honest incipits and
absences rather than continuous invented text. Evidence must describe that
truthfully. Roman English Ordinary coverage is the richer long-flow test.

## RF-D permitted and prohibited changes

Permitted presentation changes are limited to positively classified
`.is-rubric`, existing source/provenance note classes, existing why apparatus,
and source-defined selected-choice controls. Principal rendered prayers and
Propers remain darkest and continuous. Unknown forms remain visible at the
current hierarchy.

Prohibited changes include reading label text to infer kind, promoting internal
keys as public headings, treating every emitted Preface as appointed, choosing
among conditional forms, inferring a territorial outcome, or using nearest-DOM
section position to override production seating.
