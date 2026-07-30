# Calendar Mass Indexes

Normalized YAML indexes of Roman-rite mass formularies and their ordered
propers, one directory per calendar and one file per deterministic series.
`guidance/sources.md` owns the contract; this file records what is here and how
to read it.

```text
src/sources/calendars/
  roman-1962/
    sundays.yaml        # 52 temporal Sundays plus the three Triduum identities
  postconciliar/
    sundays.yaml        # PC-S01-PC-S60 plus the three PC-T Triduum identities
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
  registry: "39"               # quoted registry id; never a bare number
  season: advent
  propers:
    - name: Introit
      incipit: Ad te levavi
      source: scripture        # scripture | composed | mixed
      verses: ["Psalm 24:1-3", "Psalm 24:4"]
    - name: Collect
      incipit: Excita, quaesumus
      source: composed
      text: |
        Excita, quaesumus, Domine, potentiam tuam, et veni...
```

- `source: scripture` carries `verses`, the full ordered set of citations that
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
tools/check-calendar-masses                      # every index
tools/check-calendar-masses --calendar roman-1962
tools/check-calendar-masses --json
```

The validator checks the schema header, entry identity and uniqueness, the
`propers`/`forms` exclusivity, the source-kind rules above, and the cycle
shape. It runs inside `make check` and needs PyYAML
(`requirements-tools.txt`).
