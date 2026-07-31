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
translation names its `source_id`; a licensed one also carries the `notice` its
licensor requires. Languages may not repeat within a proper.

```yaml
translations:
- lang: en
  rights: licensed
  source_id: work.icel.roman-missal-2011
  notice: 'Excerpts from the English translation of The Roman Missal (c) 2010, ICEL.'
  text: |
    Stir up thy power, O Lord, and come...
```

A translation is someone's expression and is not relicensed by inclusion; see
`THIRD_PARTY.md`.

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
