# Roman 1962 Seasonal Primers

This profile governs primers for the liturgical seasons of the 1962 Roman
Rite: works that prepare a reader to keep a season and accompany the reader
through it. A primer gives the season's meaning, its history, what its
Sundays and proper days show, the Fathers' and the Scriptures' teaching on
it, and the practice of prayer, penance and the sacraments it calls for. It
does not govern the proper guides of the season's Masses
(`guidance/liturgy/roman-1962-propers.md`), calendar inventories
(`guidance/liturgy/roman-calendar-references.md`), assembly questions
(`guidance/liturgy/roman-1962-assembly.md`) or discursive articles
(`guidance/articles.md`). Universal evidence, voice, rights and metadata rules
remain in `guidance/editorial.md`; paths and build rules in
`guidance/repository.md`.

The maintainer asked for the series on 2026-11-18, with Advent first and Lent
to follow in 2027 at a larger scale. A primer is study and spiritual reading,
not a liturgical book, a directory of law, or a substitute for a confessor or
spiritual director.

## Collection identity

- A leaf is `src/<provider>/liturgy/roman-rite/1962/seasons/<season>`, where
  `<season>` is the season's English name in lower case (`advent`, `lent`).
  The season is the one the 1962 books name; a primer that spans more than one
  (Lent with Passiontide, say) says so in its scope and title.
- The kind is `seasonal-primer-1962`. Its catalog home is
  `library/traditional-latin-mass.md`, section "Seasonal Primers", one row per
  season in liturgical-year order and with no two-digit ID cell (that pattern
  belongs to the Proper of Time). The Sunday Propers Calendar may cue a primer
  without owning it: the Advent primer, whose season opens that table, is cued
  by one italic line above the table, carrying a
  `triptych-publication-reference` marker, and a ◇ note after the † and §
  notes
  ([reader list presentation](roman-1962-propers.md#reader-list-presentation)).
  The cue for a later season is decided when that primer is added.
- A leaf is on the `liturgy-reference-v1`
  [document type](../document-schemas.md#document-types): its `[document]`
  table declares the title lines, the body and apparatus section lists, and
  its options (endnotes where the primer uses notes).
- Identify the work by the 1962 books and their rubrics (1960 *Codex
  Rubricarum*), the universal calendar, and any named territorial layer.

## Governing priorities

1. Let the liturgy, Scripture and the Fathers carry the work. A major witness
   is expounded at identified loci, not listed.
2. Keep law, custom and counsel apart at every practical claim.
3. Own the season, not its formularies.
4. Give the reader something to do each day of the season.
5. Put work-wide scope, editions, law and as-of date in the terminal appendix.

## Boundary with the proper guides

The proper guides own each formulary: its texts, components, senses,
chronology and homily. For each Sunday and proper day a primer gives the
station, the governing text or two at incipit length (a collect may be quoted
whole), the day's place in the season's movement, and a patristic reading of
it. It prints no complete proper and no component inventory, and it does not
link a proper guide that is not yet published. Where another catalog's work
serves the season (the Four Last Things essays for Advent), the primer names
it and does not restate it.

## Law, custom and counsel

Every statement about fasting, abstinence, precept or closed times names its
body of law, territory and date, and keeps three things apart:

| Kind | Example | How it is written |
| --- | --- | --- |
| Law | the 1917 Code's fast days; the 1983 Code's penitential days | stated with canon, territory and as-of date; the 1962-horizon law and the law now are never merged |
| Custom | St Martin's Lent; the Rorate Mass at dawn | attributed to its documented time and place |
| Counsel | a graded rule of life | labelled as the primer's own proposal, with a word on prudence and direction |

A historical fast is not presented as a present obligation, and a present
freedom is not presented as the tradition's whole teaching.

## Witnesses and texts

- The Fathers and Doctors speak at length in identified human translations;
  Latin may stand with a gloss labelled as the project's. English Scripture
  comes from a registered public-domain witness.
- Every text offered for prayer reproduces an identified received witness
  (`guidance/editorial.md`, "Rights, quotation, and received prayer"); where
  no public-domain English exists, the Latin stands alone.
- A devotion's origin is stated as documented, once, without inflating its
  antiquity or debunking it.
- Quotations are checked against held bytes in the source library; whole
  public-domain texts a primer relies on are acquired there under
  `guidance/sources.md`.

## Reader-facing order

Title, a short note on how to keep the book, contents, then three parts and
the apparatus:

1. **The season**: its name and meaning, its history, its shape.
2. **The Sundays and days**: one section per Sunday and proper day or group
   of days, in liturgical order.
3. **Keeping the season**: the Fathers' teaching on its spiritual work;
   prayer; fasting and almsgiving; a graded rule of life; preparation for
   confession; a short close.

Appendices: a daily reading table keyed to the season's weeks and days (dated
where the 1962 books date them), with the Office's Scripture lesson or a stated
course and one patristic reading with locus; prayers of the season; `Scope,
Method, and Qualifications`; references. The daily table is computed from the
books, not from one civil year, so it serves every year the season's length
allows; a worked year may be named in the scope appendix.

## Required records

Each leaf keeps `research/scope.md` (plan and boundary),
`research/source-audit.md` (claim-to-source matrix and quotation checks),
`research/source-bindings.toml`, and the record of its cold review.

## Profile gate

Every quotation resolves to a held witness at an exact locus; every prayer
text to a received witness; every law statement to a body of law, territory
and date; every counsel is labelled; the per-Sunday sections stay inside the
boundary above; and a cold review has checked attribution and voice against
`guidance/editorial.md`.
