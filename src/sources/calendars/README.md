# Calendar Mass Indexes

Normalized YAML indexes of Roman-rite mass formularies and their ordered
propers, one directory per calendar and one `propers.yaml` in each. That file's
`sections` map is the single canonical mass list, labeled by kind
(`christological`, `marian`, `sanctoral`, `seasonal`). There is no other copy: a
top-level `masses` key duplicates the list and `check-calendar-masses` rejects
it.
`guidance/sources.md` owns the contract; this file records what is here and how
to read it.

```text
src/sources/calendars/
  recensions.json      # capability catalog; never a calendar index
  roman-1962/
    propers.yaml        # every mass of the calendar: seasonal, marian,
  postconciliar/        # christological and sanctoral alike
    propers.yaml
```

## Recension capability catalog

`recensions.json` is the single identity and capability catalog for the Roman
book states and language/territory expressions named by tracked evidence. It is
JSON so the YAML-only calendar discovery cannot turn an unsupported row into a
calendar selector. `check-calendar-masses` validates the catalog, every cited
source record, and the one-to-one mapping between its `calendar` fields and the
actual `propers.yaml` indexes.

Capability `data_availability` describes target-attested repository data, not
mechanical fallback from a neighboring recension. `publication_availability`
is a separate rights/surface claim; held or partially collated data can remain
unavailable for publication, but absent target data cannot claim a publishable
surface. `collation` distinguishes direct collation,
mixed evidence, a finding aid, and an unestablished claim. Detailed and
derivable coverage stays in each row's capability-keyed `coverage_ref`; every
available or partial capability names a record whose schema covers that domain,
and its availability claim cannot exceed the record. Counts are not copied into
the catalog. An `interval-gap` has no `calendar`, and every unavailable
capability must be named by an activation requirement.

## What an index is

An index is a planning and cross-reference spine. It answers "which propers
does this mass have, in what order, and out of which verses or text is each
one built" without opening a missal. It is not a source of record: it carries
no artifact hash, and a publication still binds the edition and artifact that
control each text through its own `research/source-bindings.toml`.

The index alone is not evidence for a citation or text. Each file's
`verification` header and individual rows state the applicable evidence grade,
and a publication binds the source artifact separately. Treat no row as more
verified than those records say. Known divergences remain in
`open_collation_items`; fix one by collation, not by harmonizing the file into
false uniformity.

## Translations

A proper that carries `text` may carry `translations`, a list of renderings in
other languages. Each entry needs `lang`, `text`, and a `rights` basis of
`public-domain`, `licensed`, or `project-created`. A public-domain or licensed
translation names its `source_id`, and that id must resolve to a record in the
source library; a licensed one also carries the `notice` its licensor requires.

**A proper may hold two translations in the same language, and should.** What
may not repeat is the pair `(lang, source_id)` — one witness speaking twice in
one proper is a copied row, not a second reading. Two witnesses are the reason
a translation control is worth offering at all, and their disagreement is this
corpus's only detector for a bad transcription: the two independent readings of
the 1861 Cummiskey missal here disagree at 45 of 153 shared orations, and all
38 errors the site was serving sat inside those 45. A translation that names no
`source_id` — only a `project-created` one may — has nothing to tell it from
another in its language, so a language holds at most one of those.

```yaml
translations:
- lang: en
  rights: public-domain
  source_id: edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861
  text: |
    Exert, we beseech thee, O Lord, thy power, and come...
- lang: en
  rights: public-domain
  source_id: artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.temporal-orations-en
  text: |
    Stir up thy power, we beseech thee, O Lord, and come...
```

Which one a page shows is not left to list order. `mass-propers structure`
writes a per-calendar witness manifest beside the masses, ordered by coverage,
and sorts every translation list into that order; see `guidance/web-data.md`.

A translation is someone's expression and is not relicensed by inclusion; see
`THIRD_PARTY.md`.

An overlay entry collated visually from an exact page-image artifact records
all three of these fields together:

```toml
artifact_id = "artifact.example.exact-facsimile"
passage_id = "passage.example.collect"
ia_leaf_range = [912, 913]
```

`ia_leaf_range` is a zero-based, inclusive Internet Archive BookReader range;
the legacy `ia_leaf` field, when retained, equals its first member. The passage
must be dated and verified, name the same exact artifact and hash, and cover the
corresponding one-based artifact pages (leaf + 1). `printed_page` gives the
visible printed page or full inclusive range and must agree with the passage's
locus. The calendar checker resolves all of this against the source library;
an impressive-looking but stale or partial passage ID is not provenance.

The page-image artifact proves what was read and where. It does not silently
become the translation's publication basis. `source_id` continues to identify
the translation witness, and that witness's `[[sources]].artifact_id` names the
independent rights artifact. Thus a remote whole-book PDF whose mixed contents
remain unresolved can control a visual passage while a separately tracked,
bounded public-domain derivative supplies the publication basis.

Until a calendar's translations can move into its propers they are recorded in
`src/sources/inventories/<calendar>-proper-translations-v1.toml`, and
`check-calendar-masses` holds that sidecar to every rule above.

An unavailable translation may still have an exact official witness. Record it
without its wording: `witness_artifact_id` and `witness_passage_id` identify the
registered artifact and verified passage, while `verified_on_page`,
`verified_artifact_page`, `verified_printed_page`, `verified_heading`, and
`verified_url` retain the locator. The checker requires the passage to be
inspected, verified, dated, controlled by the named artifact, to cover the
recorded artifact page, and to pin the artifact hash. These audit fields never
enter the public propers structure; its unavailable projection is limited to
the canonical target, language, and state.

Use `no-exemplar` only when no exact exemplar is known. If an exact body is
known but cannot be published on the named surfaces, use `rights-withheld` and
name the registered source that establishes the restriction. Do not assign a
single `rights` basis to a mixed-rightsholder body. The Palm Sunday Simple
Entrance Antiphon is the live case: the official artifact interleaves ICEL text
with a Revised Grail Psalm span, so ICEL's permission cannot describe the whole
proper.

A rejected detector is not an exemplar. The six typed Gospel Acclamation gaps
at Nativity Vigil and Day, Pentecost Vigil and Day, Easter 3 Year C, and
Ordinary Time 15 Year A record the liturgies.net candidates only by detector ID
and quarantine hash. The ICEL Antiphonary contains no Gospel Acclamations, and
the likely Lectionary/CCD ownership plus a USCCB comparison supplies neither an
exact redistributable witness nor permission. They remain `no-exemplar`, with
no ICEL rights or witness metadata.

## Latin provenance and publication

The Latin `text` in this index is a transcription lead. Its presence does not
establish either where the exact words were read or permission to publish
them. Those are separate per-text decisions in:

```text
src/sources/inventories/<calendar>-proper-latin-provenance-v1.toml
```

Each direct text node is keyed by `mass`, `form`, `proper`, reading `course`
and `cycle`, plus a one-based `occurrence`. The occurrence is load-bearing:
repeated names are legitimate. Palm Sunday, for example, has seven target
occurrences named Procession Antiphon: six direct source-owned bodies and one
Scripture-owned occurrence. The Latin-provenance ledger therefore has six
direct-body rows, while the translation overlay counts all seven targets; their
occurrence ordinals must not be copied across those two ledgers. Each Latin row carries the SHA-256 of the exact Unicode
string, so a changed text cannot keep an earlier decision by name alone.
A source-appointed composed proper whose wording was never held also carries
no `text`. It carries `text_status` with state `unavailable`, scope
`proper-body`, and either a registered `witness-gap` reason or a
`no-exemplar` reason with no `source_id`. This is a structural appointment, not
a former text body: it owns no Latin provenance row or hash. Creating either
would fabricate an identity for wording the repository never possessed.

When a rights review removes a body from the current YAML, the state is
different. Its row retains that former hash and whatever evidence was actually
established, if any, with `body_status = "removed"`. Unresolved provenance
stays unresolved; quarantine never upgrades a search lead into a transcription
source. The matching proper carries no `text`; it carries the same unavailable
`proper-body` status but with a registered `rights-withheld` reason. That
reason's `source_id` identifies rights/search context only. It does not assert
that the removed bytes were read from, or are exact to, that source. This
rights-withheld pairing is checked bidirectionally. The hash remains an audit
identity, not a store from which a consumer may recover or reconstruct the
wording.

`provenance_status` identifies the transcription witness, source date,
locator, relationship, transformations, verification witness, evidence,
authority, and confidence. `publication_status`, `publication_basis`, and
`surfaces` independently say whether the words may be emitted to `web`,
`download`, `print`, `cli`, the tracked `corpus-data`, or `public-git`. Both
tracked surfaces must be affirmative while the wording remains in this public
repository. A witness may be
fully identified while publication remains unresolved; naming a Holy See
edition never supplies a Vatican permission or a public-domain conclusion.

The defaults are fixed to unresolved. An affirmative public-domain row needs
an exact per-text collation against a registered witness. A permission or
licensed row needs its distinct rights authority, evidence, retrieval date,
conditioned notice, and the exact surfaces covered. `publication_source_ids`
and `publication_locator` bind that rights basis to registered evidence
independently of the transcription and verification witnesses. Missing records, orphan
records, stale hashes, ambiguous occurrences, and incomplete grants fail
closed in generated browser/download/print data and in CLI output.

Most source YAML remains tracked while the per-text collation is completed;
an explicitly quarantined `body_status = "removed"` row is the exception and
has no corresponding YAML wording. Filtering projections does not retract
other words from the current Git tree or any removed wording from its history;
the unresolved `corpus-data` and `public-git` exposure is a separate
maintainer/counsel disposition, not a permission this schema infers.

## Entry shape

Each file is a mapping with an identifying header and a `sections` map. Each
section carries its `kind`, a display `label`, and a `masses` list: dated
masses in civil date order within their kind, seasonal masses in
liturgical-year order.

```yaml
- key: advent-1                # kebab-case identity, stable within the file
  name: First Sunday of Advent # the edition's catalog name
  registry: '39'               # quoted registry id; never a bare number
  season: advent
  propers:
  - name: Introit
    incipit: Ad te levavi
    source: scripture          # scripture | composed | mixed
    verses:
    - book: Psalms             # canonical Catholic-canon name
      ranges:
      - begin: {chapter: 24, verse: 1}
        end: {chapter: 24, verse: 3}
      ref: Psalm 24:1-3        # the edition's printed string, a side field
  - name: Collect
    incipit: Excita, quaesumus
    source: composed
    text: |
      Excita, quaesumus, Domine, potentiam tuam, et veni...
```

### Recension departure shape

A recension index stores only its departures from `text_from`; it does not copy
the inherited calendar. Its `stands_before` header is a nonempty, unique list
of act ids, and every id must resolve through the Latin Missal acts inventory.
The list states the explicit historical boundaries of the whole recension, not the source
of its inherited text.

Every departure has a required `departure` and `basis`. The primary claim and
each mapping under `also` may carry an optional `act`, also resolved against the
acts inventory:

```yaml
text_from: roman-1962
stands_before:
- de-rubricis-simpliciorem-1955
- maxima-redemptionis-1955

- key: example
  departure: replaced
  act: maxima-redemptionis-1955
  basis: The source record establishes this difference at that station.
  also:
  - departure: unrecorded
    act: editio-typica-1962
    basis: The later station inventories the difference but no causal act was found.
```

`act` names the act-history station or attribution record. It is not always a
causal claim: an `unrecorded` row may be inventoried at the first later witness
while explicitly stating that no promulgating act was found. Leaving `act`
unset is required when no honest station has been established; consumers must
not infer one from the base calendar or from `stands_before`.

## Citations are machine-primary

A passage is structured data, not a string to re-parse. `book` is the canonical
canon name, so `Ecclesiasticus` and `Sirach` both resolve to `Sirach`. `ranges`
holds one or more contiguous extents, and a citation that selects several
stretches of a chapter becomes several ranges:

```yaml
- book: Psalms
  ranges:
  - begin: {chapter: 22, verse: 8}
    end: {chapter: 22, verse: 9}
  - begin: {chapter: 22, verse: 17}
    end: {chapter: 22, verse: 20}
  ref: Psalm 22:8-9, 17-20
```

- A range may cross a chapter boundary, as the Passions do:
  `begin: {chapter: 18, verse: 1}`, `end: {chapter: 19, verse: 42}`.
- A chant sung entire is cited by chapter, with no `verse` on either edge.
- `part` records a printed part-verse letter: `{chapter: 4, verse: 10, part: b}`.
- One-chapter books resolve into chapter 1, so `Philemon 9-10` encodes as
  chapter 1, verses 9 to 10.
- `ref` preserves what the edition actually prints and is never authoritative;
  the ranges are.

`tools/tpt citations encode` derives this form from a printed citation and is
idempotent, so re-running it on an encoded index changes nothing. It refuses a
citation it cannot encode without guessing rather than writing a wrong range.

- `source: scripture` carries `verses`, the full ordered set of passages that
  construct the text, and no `text`.
- `source: composed` carries the full Latin `text` and no `verses`.
- `source: mixed` carries both: the scriptural constituents and the full text.
- A celebration with several Mass formularies — the Nativity's four Masses, the
  Vigil and Day Masses of Epiphany, Ascension, and Pentecost — replaces
  `propers` with `forms`, each form carrying its own `id`, `name`, and
  `propers`, and optionally its own `ordinary_frame`. The source-authored `id`
  is a nonempty lowercase kebab-case string and is unique within the mass. It is
  stable identity for sidecars and consumers; the printed `name` remains the
  display label. `main` is reserved for the implicit sole formulary of a mass
  without `forms`, so it cannot be an `id` when a mass has multiple forms.
- A proper whose text varies by Lectionary cycle carries a `cycles` mapping
  keyed `A`, `B`, `C`. Where the cycles differ in kind, `source` moves inside
  each cycle; otherwise it stays on the proper.
- A proper whose text varies by the **weekday** cycle carries a
  `weekday_cycles` mapping keyed `'I'` and `'II'`, quoted, with the same inner
  contract as `cycles`: each key holds `verses`, `text`, or both under the
  proper's `source`, or carries a `source` of its own where the cycles differ in
  kind; the mapping excludes top-level `verses` and `text`.

  ```yaml
  - name: First Reading
    source: scripture
    weekday_cycles:
      'I': {verses: [...]}
      'II': {verses: [...]}
  ```

  **`A`/`B`/`C` and `I`/`II` are two different cycles and must never be poured
  into one key.** The Sunday course runs on three years and the ferial course of
  Ordinary Time on two, and neither ever determines the other;
  `guidance/liturgy/calendar-computation.md` owns that arithmetic and is the
  only place it is stated. What the schema owes it is two keys: a numeral
  written as a letter, or a letter as a numeral, is a year of readings served on
  the wrong day. `check-calendar-masses` refuses both of them on one
  proper — one slot reads on one course. It also refuses `weekday_cycles` in any
  calendar but `postconciliar`, which is the only one with a two-year course at
  all, and on any mass whose `season` is not `ordinary-time`, because the
  General Introduction confines the two-year course to the ferias of Ordinary
  Time; a `I`/`II` numeral outside it is a category error, not a fact.

  Known limitation, stated here so no later wave discovers it by landing on it:
  the translation overlay is keyed `(mass, form_id, proper name, cycle,
  occurrence)` and cannot see
  inside `weekday_cycles` any more than it can inside `cycles`. That is harmless
  while these propers are pure scripture, whose English is a bible's; the moment
  an English text is recorded for a cycle-varying slot, one row would answer
  both cycles and attach one year's words to the other's reading.
- `notes` records a structural fact — a conditional element, an appointed
  alternative, a long and short form — in one short sentence.
- `ordinary_disposition` records the exact source row's non-cumulative
  relationship to the normal Ordinary frame. It has one of two closed shapes:

  ```yaml
  ordinary_disposition:
    kind: alternative
    group: gospel-form
    option: shorter-form
    basis: The source prints this as the shorter alternative to the principal Gospel.
  ```

  ```yaml
  ordinary_disposition:
    kind: unplaced
    group: blessing-before-mass
    region: before-frame
    basis: The source prints this blessing before the Mass begins.
  ```

  `group` and, for an alternative, `option` are stable lowercase kebab-case
  identifiers. `basis` is always a nonempty source-grounded statement.
  `region` is exactly `before-frame` or `after-frame`; it does not license an
  unknown row in the middle of the Mass. Every member of an alternative,
  including its principal member, carries the field. Each effective formulary
  must retain at least two distinct options for the group and every member must
  carry the same basis. One option may intentionally cover several consecutive
  rows as a bundle only when those rows belong to the same semantic Ordinary
  seat. Each group and each multi-row option is one contiguous source-order
  run. Source order selects nothing, and names do not cause rows to be inferred
  into a group. The union of `before-frame` rows is an exact prefix of the
  formulary and the union of `after-frame` rows is an exact suffix. Resolution
  validates the groups again, so removing an option or leaving an orphan
  annotation fails instead of silently changing the appointment.
- `takes_from` says where a text is printed instead of printing it again. See
  the next section.

## A mass may say where its text is printed

The books do this constantly. A fourth-class feria takes the preceding Sunday's
Mass (RGMR 299). A Sunday after the Epiphany resumed after Pentecost takes the
Twenty-third Sunday's chants over its own orations, Epistle and Gospel (RGMR
298). A third-class saint takes a whole Mass from the *Commune Sanctorum* and
supplies only a Collect. Until `takes_from` existed the only way to carry such a
day was to retype the text beside itself, and the copies drift: the four resumed
Sundays after the Epiphany held the same orations twice and the two copies had
already disagreed at `caelestis` against `coelestis`, at `Caelestibus` against
`Coelestibus`, and over whether one citation was a contiguous range or three
discrete verses.

`takes_from` is a mapping. On a mass it takes `mass`, optionally `form`,
`citation` and `note`; on a proper it also takes `proper`, defaulting to the
referring proper's own name. `mass` names a key in **the same file** — a
reference never crosses calendars, because the two books print different prayers
under the same names. `citation` records the edition's own printed pointer, which
is the evidence that the reference is the book's and not the reader's.
The narrow same-mass exception is a proper in one form naming a directly printed
proper in a **different** sibling form. A mass-level self-reference, a same-form
proper reference, and a sibling target that is itself only a reference remain
cycles and are refused.

```yaml
- key: resumed-epiphany-5
  name: Fifth Sunday after the Epiphany, resumed after Pentecost
  registry: 48R
  season: after-pentecost
  takes_from: {mass: epiphany-5, citation: RGMR 298}
  propers:                       # replacements, matched on `name`
  - name: Introit
    takes_from: {mass: pentecost-23, citation: RGMR 298}
```

- A mass carrying `takes_from` starts from the referenced formulary, then
  applies its own `propers` as replacements matched on `name`. That is what a
  third-class saint is: the Mass of the Common, with the Collect of the saint.
  A local proper the referenced formulary does not print is appended rather than
  dropped.
- A mass carrying `takes_from` may not also carry `forms`; a reference into a
  mass that *is* printed in forms must name which form.
- One narrow mass-level absence may accompany `takes_from`: `text_status` with
  `state: unavailable` and `scope: proper-collect`. It means the referenced
  formulary supplies every held proper except its Collect, because the dated
  mass's own proper Collect is unavailable. The resolver therefore omits only
  the inherited Collect and retains every other borrowed proper with its
  provenance. Such a mass carries neither `forms` nor a local Collect; other
  `text_status` scopes cannot accompany `takes_from`.
- A proper carrying `takes_from` carries no wording of its own — no `source`,
  `text`, `verses`, `cycles`, `weekday_cycles`, `incipit` or `translations`.
  All of those come from the resolved proper, and a second copy here is the
  restatement the key removes. It may carry `ordinary_disposition`, because
  that is structure of this appointment rather than a copy of the target's
  wording; the resolver preserves it on the resolved row.
- References may chain. A cycle, a mass-level self-reference, a same-form proper
  self-reference, a missing mass and a missing proper are each refused by
  `check-calendar-masses`; the explicit different-sibling exception above is the
  only same-mass reference.
- The resolution is `resolve_propers` in `scripts/_calendars.py`, read by the
  validator and by `mass-propers` alike, so the reference the gate accepts and
  the reference the site resolves cannot come apart. Nothing is ever copied into
  the file; correcting the Common corrects every mass that takes it.
- `mass-propers` looks a borrowed proper's `translations` up under the mass that
  **prints** it, so an English oration is recorded once and served at every mass
  the Missal appoints it on.
- The census counts what each file *carries*, so a mass that takes a formulary
  lowers the proper count. Its two `taking` rows count what the calendar
  *appoints* from elsewhere. Neither shape is a placeholder.

## A Common direction is not resolved text

`common_from` records a source-witnessed Common direction for exactly the named
Missal slots when the Common formulary is not held as resolvable text. It is
deliberately separate from `takes_from`: the latter borrows an existing
formulary, while the former preserves only a witnessed structural appointment.
Consumers must expose the direction and must not turn it into words.

```yaml
common_from:
  scope: missal-antiphons
  source_id: artifact.catholic-church.missale-romanum.2010-english-icel-antiphonary.antiphonary-pdf
  locus: artifact page 112, printed page 104
  options:
  - mass: commune-martyrum
    selection: "<printed Common subheading>"
text_status:
  state: unavailable
  scope: missal-formulary
  reasons:
  - kind: no-exemplar
```

`options` are coequal where more than one is printed; list order selects
nothing. Each `mass` must exist in this file's `kind: common` section.
`selection`, when present, records the printed subdivision label but does not
claim that the subdivision has been modeled as a form. `source_id` and `locus`
identify the registered structural witness. A mass carrying `common_from`
never carries `forms`. The currently admitted `missal-antiphons` scope is exact:
the registered ICEL Antiphonary can attest the Common direction for the Entrance
and Communion Antiphons, but carries no orations and resolves none of the words.
It therefore cannot account for the Collect, Prayer over the Offerings, or Prayer
after Communion.

`text_status` keeps the missing words separate from the verified direction.
Its `state`, `scope`, reason keys, and source ids are closed and checked.
`proper-collect` belongs only to the exact `takes_from` case above, where it
suppresses the borrowed Common's Collect. `missal-formulary` accounts for the
whole Missal formulary when target wording is unavailable; it does not include
Lectionary options. It is required on a text-free Common destination and on a
text-free dated `common_from` mass. With `state: unavailable` it otherwise stands
alone. A non-Common Mass may instead use `state: partial` beside exactly one of
real `propers` or `forms`; `common_from` may accompany the flat `propers` case
because its narrow antiphon direction resolves no text, while `takes_from` may
not. The independent status, not the Antiphonary pointer, accounts for every
missing word. The reason kinds reuse the Ordinary
inventory's `witness-gap`, `rights-withheld`, and `no-exemplar` vocabulary.
`witness-gap` and `rights-withheld` name the registered source that establishes
the gap; `no-exemplar` names the absence of an exact copy and therefore omits
`source_id`.

At proper level, `scope: proper-body` preserves an exact source-owned composed
slot while recording why its body is unavailable. A `witness-gap` or
`no-exemplar` proper-body was never held and therefore has no Latin provenance
row. A `rights-withheld` proper-body is a quarantine owner and must have the
matching `body_status = "removed"` row with the former body's exact hash. The
reason, not the shared unavailable state, distinguishes those two cases.

```yaml
- key: target-formulary-not-held
  name: Target formulary not held
  registry: 'example'
  season: example
  text_status:
    state: unavailable
    scope: missal-formulary
    reasons:
    - kind: witness-gap
      source_id: artifact.example.restricted-target-edition
```

A proper named `Placeholder` is never an alternate representation of this
state. It invents a composed slot the Missal does not own and is rejected by
`check-calendar-masses`; use the mass-level typed absence instead.

## An exceptional rite may not take the normal Ordinary frame

Omitting `ordinary_frame` means that the normal full Ordinary applies. The
field may live on the mass or on an individual member of `forms`; a selected
form's explicit frame overrides the mass-level frame, and otherwise the mass
field (or the implicit full default) applies. Record it only where the source
establishes an exception:

```yaml
ordinary_frame:
  applicability: none
  basis: The source identifies this service as a liturgical action, not a Mass.
```

`applicability: none` means there is no Mass frame to borrow, as on Good
Friday. `applicability: unavailable` means the rite includes a Mass but the
repository has not modeled a frame that can seat it honestly, as when a Vigil,
its specialized Mass boundary, and a following Hour remain one bundled entry.
Both explicit states require a nonempty source-grounded `basis`; consumers fail
closed and suppress the generic Ordinary. Do not mark a Mass `none` merely
because blessings, processions, extra lessons, or another exceptional Proper
structure surround or enter it.

## A rubric may appoint one text across a span of days

The Missal appoints a text on a range of days as readily as on one. Under the
Sequence at Easter it prints *Sequentia dicitur usque ad sabbatum in albis
inclusive*, and under the Sequence at Pentecost *Et dicitur cotidie usque ad
sequens sabbatum inclusive*: twelve further Masses, one appointment each.

`takes_from` already carries such a text without copying it, one proper at a
time. What no file could say was that the twelve days are **one** appointment,
and the cost of not saying it was not documentary. The Easter span survived as
an English sentence in a `notes` string — a free field no tool reads and no
check tests — the Pentecost span was written nowhere at all, and eleven of the
twelve days rendered as a finished Mass with no Sequence in it.

So the span is stated once, in the calendar's `rubrics.yaml`, under a top-level
`appointed_across` list, and the masses reference the text as they reference
any other:

```yaml
appointed_across:
- id: victimae-paschali-laudes-within-the-octave-of-easter
  label: the Sequence Victimae paschali laudes, at every Mass of the octave of Easter
  prints: {mass: easter-sunday, proper: Sequence}   # where the text is written, once
  keys: [easter-monday, easter-tuesday, ...]        # the masses it is appointed on
  before: Gospel                                    # where it stands in each
  stated: true                                      # the rubric was read from a witness
  locus: Proprium de tempore, Dominica Resurrectionis, ... printed p. 330
  latin: Sequentia dicitur usque ad sabbatum in albis inclusive.
  note: ...
```

- The span **never carries the text**. Each mass in `keys` takes it with an
  ordinary proper-level `takes_from`, placed where the Missal prints it, and
  `resolve_propers` swaps it in position. Correcting the one printing corrects
  every day the rubric appoints it on.
- The reference stays bare — `takes_from: {mass: easter-sunday}` — and carries
  no `citation`. The printed pointer is the span's `locus`, written once;
  thirteen copies of it beside thirteen references would be the restatement
  `takes_from` exists to remove.
- `stated` and `locus` are two fields so that a day list this repository is
  confident of can be told from a printed rubric it has never seen.
  `stated: false` with `locus: null` is that sentence, and it is enforced: a
  `stated: false` row may carry neither a locus nor the rubric's Latin, because
  a quotation with no locus is a quotation from nowhere.
- `scripts/_calendars.py` holds the reader, `spans_of`, so the gate and any
  renderer read one derivation rather than two.
- `check-calendar-masses span_problems` joins the halves and reports four
  things nothing reported before: a mass in `keys` that appoints no proper of
  that name, a mass that **prints** the text instead of referencing it, a text
  that does not stand immediately before the slot `before` names, and a span
  whose authority and evidence disagree. A mass printed in `forms` is held to
  the rule in **each** form: the Ember Saturday of the Pentecost octave prints
  a longer and a shorter Mass, and a Sequence supplied to only one of them is
  missing from whichever Mass is actually said.

Propers stand in the order the edition appoints them, not in a fixed template,
so Tracts, Sequences, palm-rite antiphons, the Improperia, the Exsultet, the
prophecies, and the litanies appear only where they are actually appointed. The
invariant Ordinary is out of scope, and prefaces are not recorded.

## Citation conventions

The two calendars cite differently, and each file declares its own rule:

| | `roman-1962` | `postconciliar` |
| --- | --- | --- |
| Psalms in chants and orations | Vulgate numbering, as printed | the Missal's own printed numbering |
| Psalms in readings | Vulgate numbering | Lectionary (modern/Hebrew) numbering |
| Latin orthography | `j` retained, no accents | `i` for `j`, no accents |

A postconciliar entry can therefore cite Psalm 26 for its entrance antiphon
and Psalm 27 for its responsorial psalm. That is the books' own inconsistency,
not the file's.

### Numbering divergences outside the psalter

The psalter converts between numberings through a tracked verse-level
concordance, and `scripts/_psalms.py` owns it. Nothing else can: the
postconciliar Lectionary cites the Nova Vulgata, no witness of that
versification is tracked here, and every bible in this library follows the
Vulgate division. Where the two divide a book differently — Joel, Malachi, and
single chapters of Isaiah and Micah — the reference does not fail. It resolves,
to different words. `Joel 3:1-5` returned the valley of Josaphat instead of the
outpoured spirit, in Latin and English alike, and appeared in no error count.

A calendar therefore records the correspondence itself, per citation, in a
top-level `citation_divergences` list beside `open_collation_items`:

```yaml
citation_divergences:
- book: Isaiah
  chapters: [9, 64]            # omit where the chapter counts themselves differ
  divergence: the Vulgate opens chapter 9 one verse earlier...
  numbering:
    hebrew: resolved           # see below; every other numbering must be ruled on
  citations:
    "Isaiah 9:5": "Isaiah 9:6"          # the Child born to us, not the spoils
    "Isaiah 2:1-5": "Isaiah 2:1-5"      # stated even where nothing moves
```

The left side is the citation as this calendar prints it; the right side is the
reference addressing the same text in Vulgate numbering, parsed by
`tools/tpt citations`, so the two cannot drift apart. A correspondence that
holds unchanged is written out rather than omitted: inside a divergent locus,
silence is not evidence that anyone checked.

Every resolution is written in Vulgate numbering, because that is the text each
was read out of. Not every indexed edition is in that numbering, and the answer
is not the same for every book: the English Bibles keep the Vulgate's division
in the prophets, where only the Hebrew differs, but follow the Greek through the
New Testament and the deuterocanon, where a Lectionary citation already stands
where it belongs. `numbering` therefore rules, per locus, on every other
numbering an indexed edition is in — one of `resolved` (that numbering divides
the book as the Vulgate does, so the resolution corrects it too), `as-cited`
(it divides the book as this calendar cites it, so the citation is left exactly
as it stands), or `unrecorded` (neither is established, or this file's citations
for the book do not all speak one system, so the citation refuses there). There
is no default: whichever it were would be applied silently to the books nobody
had thought about yet, and the two live answers are opposites.

`tools/tpt index-bible` validates the list against the citations actually made
before it indexes anything, and fails the build on a resolution for a reference
no longer cited, one landing in another book, one addressing no text in an
edition holding that book and using the resolution, a declared chapter nothing
reaches, or a numbering left unruled. A citation reaching a divergent locus with
no correspondence recorded is refused: left out of every index and reported
unresolved. That is deliberate. A missing passage is a question; a plausible
wrong one is an answer, and this defect is what answering wrongly looks like.

These entries resolve text. They do not settle the collation question of which
numbering the file should print, which stays an `open_collation_items` entry.

## Validating

```sh
tools/tpt check-calendar-masses                       # every index
tools/tpt check-calendar-masses --calendar roman-1962
tools/tpt citations check --root src/sources/calendars # citation contents only
tools/tpt citations parse "Baruch 3:9-15, 32-4:4"  # encode one citation
```

`check-calendar-masses` checks the schema header, entry identity and
uniqueness, the `propers`/`forms` exclusivity, the source-kind rules above, and
the cycle shape, then delegates citation contents to `tools/tpt citations`, which
owns the canon. Both run inside `make check` and need PyYAML
(`requirements-tools.txt`); `make check` skips rather than fails without it.

## Current contents

<!-- census:begin — derived; edit nothing between these markers -->

| Calendar | Section | Masses | Propers | Masses holding only placeholders |
| --- | --- | ---: | ---: | ---: |
| roman-pre-1955 | seasonal | 6 | 0 | 0 |
| roman-pre-1955 | marian | 1 | 0 | 0 |
| roman-pre-1955 | sanctoral | 1 | 0 | 0 |
| roman-1962 | seasonal | 128 | 1352 | 0 |
| roman-1962 | christological | 8 | 96 | 0 |
| roman-1962 | marian | 18 | 124 | 0 |
| roman-1962 | sanctoral | 307 | 1509 | 0 |
| roman-1962 | common | 30 | 358 | 0 |
| postconciliar | seasonal | 390 | 2116 | 0 |
| postconciliar | christological | 7 | 69 | 0 |
| postconciliar | marian | 14 | 52 | 0 |
| postconciliar | sanctoral | 201 | 760 | 0 |
| postconciliar | common | 7 | 0 | 0 |

| Calendar | Rank | Entries | Celebrations |
| --- | --- | ---: | ---: |
| roman-pre-1955 | (no rank) | 6 | 6 |
| roman-pre-1955 | I | 1 | 1 |
| roman-pre-1955 | II | 1 | 1 |
| roman-1962 | (no rank) | 93 | 93 |
| roman-1962 | Comm. | 104 | 104 |
| roman-1962 | I | 37 | 37 |
| roman-1962 | II | 46 | 47 |
| roman-1962 | III | 211 | 211 |
| postconciliar | (no rank) | 394 | 394 |
| postconciliar | All Souls commemoration | 1 | 1 |
| postconciliar | Feast | 24 | 24 |
| postconciliar | Memorial | 69 | 69 |
| postconciliar | Optional memorial | 120 | 120 |
| postconciliar | Solemnity | 11 | 11 |

| Measure | roman-pre-1955 | roman-1962 | postconciliar |
| --- | ---: | ---: | ---: |
| Masses | 8 | 491 | 619 |
| Propers | 0 | 3439 | 2997 |
| — named `Placeholder` | 0 | 0 | 0 |
| — inside a `forms` block | 0 | 182 | 188 |
| — carrying a `cycles` mapping | 0 | 0 | 258 |
| — carrying a `weekday_cycles` mapping | 0 | 0 | 409 |
| Masses holding only placeholders | 0 | 0 | 0 |
| Masses taking a formulary from another entry | 0 | 164 | 0 |
| Propers taking their text from another entry | 0 | 70 | 49 |
| Propers that are not placeholders | 0 | 3439 | 2997 |
| — of those, scripture-bearing | 0 | 2192 | 2635 |
| Encoded passages | 0 | 2598 | 3590 |
| Distinct books cited | 0 | 57 | 73 |
| Distinct slot names | 0 | 120 | 92 |

Counted from `src/sources/calendars/*/propers.yaml` and written here by
`tools/mass-propers census --write`, which is the only thing that writes the
block above; `make check-propers-census` refuses a copy that has drifted. What
each row counts, because two honest counts of “propers” differ by hundreds
when they key differently: a **mass** is one entry under `sections[*].masses`.
A **proper** is one entry in a mass's `propers`, or in the `propers` of one of
its `forms`; a proper carrying `cycles` counts once, not three times.
Placeholders are **inside** the proper and mass totals, and are also given
their own rows. A mass **holds only placeholders** when every proper it holds,
those inside `forms` included, is named `Placeholder` — keying on the mass's
own `propers` alone undercounts, because it misses the masses whose
placeholders sit inside a `forms` block. **Scripture-bearing** means a
`source` of `scripture` or `mixed`, or a `cycles` entry that is. **Encoded
passages** and **distinct books** are `tools/citations check`'s own counts,
one passage per encoded citation entry and books counted distinct within a
file. **Distinct slot names** counts distinct proper `name` values, with
`Placeholder` among them. The two **taking** rows count the entries that name
where their text is printed instead of printing it — a feria taking the
preceding Sunday, a saint taking a Mass of the Common. Such an entry holds few
propers or none, so it lowers the proper count while raising what the calendar
can actually show: every row above counts what a file **carries**, and these
two count what it **appoints** from elsewhere. Neither is a placeholder.

The rank rows count **entries**, and a calendar's rank rows sum to its
`Masses` above. `(no rank)` is a row and not an omission: the temporal cycle
prints no rank at all, so unranked entries are a large group in both indexes,
and a table that dropped them would invite the ranks it does show to be read
as the whole book. **Celebrations** counts what those entries name. One entry
can print more than one celebration — a pair of optional memorials falling on
the same day, or the Greater Litanies kept with Saint Mark — and the index
records the join only in the entry's `name`, joined with `;`, so that is where
it is read from; the plural rank word marks some such entries and not others,
and it never says how many. Where the two columns differ the index is keeping
more celebrations than it holds entries: reading the entry count as a count of
celebrations understates the calendar, and folding the celebrations into the
entry count would break the sum against `Masses`, so both are given and
neither replaces the other. A **rank** is reproduced exactly as the file
prints it. `Optional memorial` and `Optional memorials` are two rows because
they are two different words in the index, and the two Missals' rank
vocabularies are not one scale — no row of this table is comparable across
calendars, which is why rank is tabulated down the page and not across it.
This table answers what an index is scoped to; it does not answer which
entries are Sundays, because no entry states that and it is not derived here.

<!-- census:end -->
