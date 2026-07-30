# Calendar Mass Indexes

Normalized YAML indexes of Roman-rite mass formularies and their ordered
propers, one directory per calendar and one file per deterministic series.
For sanctoral propers, each calendar now uses one `propers.yaml` with
separate, labeled sections (`marian`, `christological`, and `saintly`).
`guidance/sources.md` owns the contract; this file records what is here and how
to read it.

```text
src/sources/calendars/
  roman-1962/
    propers.yaml        # consolidated sanctoral propers (marian/christological/saintly)
  postconciliar/
    propers.yaml        # consolidated sanctoral propers (marian/christological/saintly)
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

## Entry shape

Each file is a mapping with an identifying header and a `masses` list in the
series' declared order.

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

| Index | Masses | Propers | Encoded passages |
| --- | --- | --- | --- |
| `roman-1962/propers.yaml` | 59 | 636 | 548 |
| `postconciliar/propers.yaml` | 63 | 821 | 1082 |

The 1962 index covers the 59-item seasonal spine, the four resumed Epiphany
Sundays, and `T01`-`T03`. The postconciliar index covers `PC-S01`-`PC-S60` and
`PC-T01`-`PC-T03`, with the Nativity, Epiphany, Ascension, and Pentecost
carrying `forms`. Registry coverage in both is exact and duplicate-free.
