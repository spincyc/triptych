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
  roman-1962/
    propers.yaml        # every mass of the calendar: seasonal, marian,
  postconciliar/        # christological and sanctoral alike
    propers.yaml
```

## What an index is

An index is a planning and cross-reference spine. It answers "which propers
does this mass have, in what order, and out of which verses or text is each
one built" without opening a missal. It is not a source of record: it carries
no artifact hash, and a publication still binds the edition and artifact that
control each text through its own `research/source-bindings.toml`.

Every citation and text is an **unverified lead** until collated against the
controlling edition. Each file states this in its `verification` field and
tracks known divergences in `open_collation_items`. Fix a divergence by
collation, not by harmonizing the file into false uniformity.

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

Until a calendar's translations can move into its propers they are recorded in
`src/sources/inventories/<calendar>-proper-translations-v1.toml`, and
`check-calendar-masses` holds that sidecar to every rule above.

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
  `propers` with `forms`, each form carrying its own `name` and `propers`.
- A proper whose text varies by Lectionary cycle carries a `cycles` mapping
  keyed `A`, `B`, `C`. Where the cycles differ in kind, `source` moves inside
  each cycle; otherwise it stays on the proper.
- `notes` records a structural fact — a conditional element, an appointed
  alternative, a long and short form — in one short sentence.
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
- A proper carrying `takes_from` carries nothing else — no `source`, `text`,
  `verses`, `cycles`, `incipit` or `translations`. All of those come from the
  resolved proper, and a second copy here is the restatement the key removes.
- References may chain. A cycle, a self-reference, a missing mass and a missing
  proper are each refused by `check-calendar-masses`.
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

Counted from the files by `check-calendar-masses` and `citations check`, which
are the authority; these figures are restated here and go stale, so re-run them
before trusting the table.

| Index | Masses | Propers | Encoded passages | Placeholder-only masses | Propers in seasonal | Propers inside `forms` |
| --- | --- | --- | --- | --- | --- | --- |
| `roman-1962/propers.yaml` | 460 | 1475 | 1115 | 337 | 1141 | 97 |
| `postconciliar/propers.yaml` | 268 | 1031 | 1082 | 205 | 824 | 117 |

The proper counts include those nested inside `forms`, so a count that reads
`propers` alone lands short by the last column.

**Most of what is here is a name, not a formulary.** The placeholder-only column
is most of both indexes: those masses establish that the mass exists and where it
falls, and record nothing of what is said at it. The seasonal sections hold the
substance. Coverage is therefore wide and shallow by design, and a reader who
sees a mass listed should not infer its texts are here. The prose here states no
figure the table does not: the two disagreed for four commits, because a lane
refreshed the table and left three older totals standing beside it.

`check-calendar-masses` enforces that every mass matches a spine entry and that
no key repeats. It exits 0 on both indexes, so coverage is exact and
duplicate-free as of that run — which is a statement about the check, not a
standing property of the files.
