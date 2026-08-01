# Propers: working rules for agents

Operating rules for the calendar mass indexes under `src/sources/calendars/`.
Terse by design. For the subject matter itself, read [`docs/the-mass.md`](../docs/the-mass.md).

Authority order: `guidance/sources.md` owns the source contract;
`guidance/liturgy/calendar-computation.md` owns every calendar arithmetic rule;
`src/sources/calendars/README.md` owns the schema; this file owns nothing — it
points at the owners and states what breaks.

## What you are looking at

```text
src/sources/calendars/roman-1962/propers.yaml
src/sources/calendars/postconciliar/propers.yaml
```

Two calendars, one file each, one schema (`triptych-calendar-masses/v1`).
An index is a **planning and cross-reference spine, not a source of record**. It
carries no artifact hash. Every citation and text in it is an **unverified lead**
until collated against the controlling edition. Do not cite one as evidence.

## Data model

Header keys, all required: `schema`, `calendar`, `edition`, `series`, `ordering`,
`registry`, `orthography`, `citation_convention`, `verification`. Plus
`psalm_numbering` (`vulgate` or `hebrew`), and optionally `conventions`,
`open_collation_items`, `citation_divergences`, `psalm_numbering_exceptions`.

`sections` is the **single canonical mass list**. A top-level `masses` key is
rejected. Each section carries `kind` ∈ {`seasonal`, `christological`, `marian`,
`sanctoral`, `common`}, a `label`, and `masses`.

`common` is the *Commune Sanctorum*: formularies no day owns, reached only by
`takes_from`. A mass in a `common` section carries **neither** `season` nor
`date` — it is placed by use, not by the year — and every mass in every other
section still carries exactly one of the two.

A mass requires `key`, `name`, `registry`. `registry` is always a **quoted
string** — `'39'`, never `39`. It may carry `date`, `rank`, `season`, `kind`,
`notes`; an entry carrying `date` must **also** carry a valid `kind` and the
edition's printed `rank`. It carries **either** `propers` **or** `forms`, never
both — `exactly one of propers, forms or takes_from is required` — unless it
carries `takes_from`, which may stand alone or beside `propers` but never beside
`forms`.

`takes_from` says where a text is printed instead of printing it again, and is
the only sanctioned way to carry a mass that takes another's formulary. On a
mass: `mass` (a key in the **same file**), optional `form`, `citation`, `note`.
On a proper, also `proper`, defaulting to its own name; a proper carrying it
carries nothing else. A mass's own `propers` replace the borrowed ones by
`name`. `src/sources/calendars/README.md` owns the full rule.

A proper requires `name` and a `source`, unless it carries `takes_from`:

| `source` | carries | must not carry |
| --- | --- | --- |
| `scripture` | `verses` | `text` |
| `composed` | `text` | `verses` |
| `mixed` | both | — |

Optional on a proper: `incipit`, `notes`, `translations`, `psalm_numbering`,
`cycles`.

`cycles` is keyed `A`/`B`/`C` and excludes top-level `verses` and `text`. Where
cycles differ in kind, `source` moves inside each cycle; otherwise it stays on
the proper. Postconciliar only — a 1962 proper must never carry one.

`forms` is a list, each with `name` and `propers`. Used for the Nativity's four
Masses, the Vigil/Day pairs of Epiphany, Ascension and Pentecost, and the 1962
Ember Saturdays' longer and shorter forms.

A citation is structured data:

```yaml
- book: Psalms          # canonical Catholic-canon name; Ecclesiasticus -> Sirach
  ranges:
  - begin: {chapter: 22, verse: 8}
    end: {chapter: 22, verse: 9}
  - begin: {chapter: 22, verse: 17}
    end: {chapter: 22, verse: 20}
  ref: Psalm 22:8-9, 17-20   # the edition's printed string; NEVER authoritative
```

`ranges` is canonical. `ref` is a side field. Read the ranges.

A placeholder mass holds exactly one proper, named `Placeholder`, `source:
composed`, text `This entry is a placeholder pending formula migration and
source verification.` Nothing is partial — there is no half-filled tier.

## Invariants

1. **Never edit these files by hand where a tool owns the transform.** Run
   `tools/tpt citations encode` to encode a citation; it is idempotent and
   refuses what it cannot encode without guessing.
2. **Never harmonize a divergence.** Two calendars citing the same text
   differently is the books' own inconsistency. Fix by collation, or record it
   in `open_collation_items`. Making the file uniform destroys evidence.
3. **Never invent an oration.** A day whose orations were not read carries only
   its scripture-bearing propers and says so in `notes`. Absent is correct;
   plausible-but-fabricated is not.
4. **Never import a cycle letter across calendars.** No `A`/`B`/`C` or `I`/`II`
   in a 1962 record; no postconciliar week number, season boundary, or Ordinary
   Time term projected onto 1962, or the reverse.
5. **Never compute an occurrence and publish it as a witness.** Computation is a
   finding aid. Territorial transfers (Epiphany, Ascension, Corpus Christi) are
   not computable at all. Fail closed on disagreement with a dated official
   witness; `guidance/liturgy/calendar-computation.md` is authoritative and no
   other file may restate its rules.
6. **Spine and propers must agree.** Every celebration `calendar-spine` derives
   must have a mass filed under the kind the spine assigns it.
   `check-calendar-masses` enforces this.
7. **`registry` stays quoted and unique within a file.** Both files are
   duplicate-free; keep them so.
8. **Anything added inherits the file's `verification` marking.** New entries are
   unverified model-generated leads unless actually collated.

## What fails silently

These are the ways this data has gone wrong without anything reporting it.
Assume more of the same kind exist.

| Failure | Why it is silent | Status |
| --- | --- | --- |
| A citation resolving to the **wrong words** across a book-division divergence | It resolves. `Joel 3:1-5` returned the valley of Josaphat, not the outpoured spirit, and appeared in no error count. | Now caught: `citation_divergences` is validated by `index-bible`, which refuses an unrecorded citation reaching a divergent locus. |
| A psalm verse **beyond the end of its psalm** under the file's declared numbering | The bounds check once held ceilings for six psalms only, so `Psalm 118:137` passed although Hebrew 118 ends at 29. | Now caught: every psalm is bounded from the tracked verse-level concordance. Eleven loci remain, ledgered. |
| A celebration in the **spine and in no section** | The two artifacts had different histories and nothing compared them. Three Christmas octave days sat in the gap. | Now caught: `spine_problems` in `check-calendar-masses`. |
| A verse **past the end of a chapter** | `index-bible` derives a chapter's bounds from the verses the edition prints, so it clamps rather than reports. `Mark 4:41`, `1 Thessalonians 4:18`, `Acts 7:60` are each dropped this way. | Open. The remedy is a `merged-verse` row in the edition's verse-aliases artifact, because the Douay and Clementine disagree here. |
| **1962 commemorations** | They existed only as prose inside a `name` string, so none could be looked up or commemorated. | Now caught: the sixty folded into feast names are dated entries of rank `Comm.`, 104 in all, and `check-calendar-masses` refuses a `comm.` anywhere but the start of a name. Their orations are still placeholders. |
| The **book's identity** retyped in a second file | `edition` sat in `propers.yaml` and again in `rubrics.yaml`, in both calendars — four hand-typed copies of two strings, with nothing comparing them. They agreed; nothing made them agree. | Now caught: the mass index owns `edition` and `edition_short`, `calendar-rubrics` reads both from it, and `_calendars.restated_identity` refuses a companion that carries either — whether or not its value matches. |
| One formulary **retyped under a second mass** | The schema could not say "this mass takes that text", so a day the Missal carries by a pointer had to be carried by a copy, and nothing compared the copies. The four resumed Sundays after the Epiphany held one set of orations twice and disagreed in five ways — `caelestis`/`coelestis`, `Caelestibus`/`Coelestibus`, `caelestibus`/`coelestibus`, one Introit citation encoded as a contiguous range against three discrete verses, and a dozen truncated incipits. The English was duplicated with it, twelve sidecar rows for four orations. | Now expressible: `takes_from` on a mass or a proper, resolved once by `_calendars.resolve_propers` for both the validator and the browser. The four Sundays now reference `epiphany-3`..`-6` and `pentecost-23` under RGMR 298. **Not yet caught** — nothing detects a formulary retyped where a reference would do. |
| Any **stale count table** | One census of these files existed in three retyped copies, and all three disagreed; the 1962 sanctoral section read 247 in a document that called itself current and 307 in the file. | Now caught for the two documents that carry the derived block — this one and `docs/the-mass.md` — by `mass-propers census --check`, which `make check-propers-census` runs. `src/sources/calendars/README.md` and `guidance/liturgy/propers-completion-todo.md` still carry hand-typed tables. Open. |

## Tool ownership

Never re-derive what a tool owns; that is how two artifacts come to disagree.

| Tool | Owns | Mutates |
| --- | --- | --- |
| `tools/citations` | The canonical book list, citation parsing and encoding, passage validation | yes (`encode`) |
| `tools/check-calendar-masses` | Schema, identity, `propers`/`forms` exclusivity, source-kind rules, cycle shape, the psalm-exception ledger, spine agreement. Delegates citation contents to `citations`. | no |
| `tools/calendar-spine` | The date-ordered list of celebrations and its `kind` classification, derived from the calendar-reference publications | no |
| `tools/mass-propers` | Reading one mass; per-proper psalm-numbering inheritance; the browser's structure files; **the census** and the derived block both count-bearing documents carry | yes (`structure`, `census --write`) |
| `tools/index-bible` | Indexed bibles keyed by the reference strings the calendars actually make; validation of `citation_divergences` | yes |
| `scripts/_psalms.py` | The Vulgate↔Hebrew verse-level concordance and every psalm bound | — |

Invoke through `tools/tpt <tool>`. `make check` runs `check-calendar-masses` and
skips rather than fails without PyYAML.

## Commands to check a claim

```sh
# Full gate. Exits 0 while the psalm-exception ledger holds; prints
# "calendar-mass excepted:" for each ledgered locus and the per-file totals.
tools/tpt check-calendar-masses
tools/tpt check-calendar-masses --calendar roman-1962

# Citation contents only. Exits 1 today: it reads the file-level
# psalm_numbering and not the per-proper one, so the eleven still report.
tools/tpt citations check --root src/sources/calendars

# Encode one printed citation without touching a file.
tools/tpt citations parse "Baruch 3:9-15, 32-4:4"

# Read a mass, with scripture resolved and psalm numbers converted.
tools/tpt mass-propers show --calendar roman-1962 --mass advent-1 --bible douay-rheims
tools/tpt mass-propers list --calendar postconciliar

# The spine, and its December filing.
tools/tpt calendar-spine derive --calendar roman-1962
```

Counting. Never count by hand and never retype a count. One verb owns the
census, and the block under [Current numbers](#current-numbers) is its output:

    # Print the derived block; writes nothing.
    tools/tpt mass-propers census

    # Rewrite the block in every document that carries it.
    tools/tpt mass-propers census --write

    # Fail, naming each stale document, without writing. `make
    # check-propers-census` runs this.
    tools/tpt mass-propers census --check

## Current numbers

Everything between the markers below is written by
`tools/tpt mass-propers census --write` and by nothing else. Do not edit it, and
do not restate any of it in prose here or anywhere: that restatement is exactly
how one census came to exist in three copies that disagreed. `docs/the-mass.md`
carries the identical block.

<!-- census:begin — derived; edit nothing between these markers -->

| Calendar | Section | Masses | Propers | Masses holding only placeholders |
| --- | --- | ---: | ---: | ---: |
| roman-1962 | seasonal | 128 | 1121 | 5 |
| roman-1962 | christological | 8 | 10 | 8 |
| roman-1962 | marian | 17 | 17 | 17 |
| roman-1962 | sanctoral | 307 | 309 | 306 |
| roman-1962 | common | 2 | 15 | 0 |
| postconciliar | seasonal | 66 | 824 | 3 |
| postconciliar | christological | 7 | 7 | 7 |
| postconciliar | marian | 14 | 15 | 14 |
| postconciliar | sanctoral | 181 | 185 | 181 |

| Measure | roman-1962 | postconciliar |
| --- | ---: | ---: |
| Masses | 462 | 268 |
| Propers | 1472 | 1031 |
| — named `Placeholder` | 338 | 210 |
| — inside a `forms` block | 97 | 117 |
| — carrying a `cycles` mapping | 0 | 252 |
| Masses holding only placeholders | 336 | 205 |
| Masses taking a formulary from another entry | 6 | 0 |
| Propers taking their text from another entry | 20 | 0 |
| Propers that are not placeholders | 1134 | 821 |
| — of those, scripture-bearing | 904 | 548 |
| Encoded passages | 1095 | 1082 |
| Distinct books cited | 48 | 61 |
| Distinct slot names | 90 | 86 |

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

<!-- census:end -->

What the census does not cover, and what still has to be counted by reading:

- 63 of the 1962 seasonal entries carry only their scripture-bearing propers and
  a `notes` line saying so; their registry ids read `1962-T-<key>` and are
  synthetic. Three further entries carry that registry form without the note.
  Identity, rank and citations were read from an **OCR text layer** of the CMAA
  1962 facsimile, not the images. Nothing has been visually collated.
- `src/sources/calendars/README.md` and
  `guidance/liturgy/propers-completion-todo.md` still carry hand-typed count
  tables that nothing regenerates. Treat both as stale, and do not copy a figure
  out of either.

## The psalm-numbering situation

Read this before touching any psalm citation in `postconciliar/propers.yaml`.

The calendar declares `psalm_numbering: hebrew`. Its recovered
`citation_convention` says *Lectionary readings and antiphons preserve the
numbering in the controlling missal* — so an antiphon reproduces the Missal's
printed number (Vulgate across most of the psalter) while a responsorial psalm or
acclamation takes the Lectionary's. `ot-23` shows both in one Mass: Entrance
Antiphon `Psalm 118:137, 124`, Year C Gospel Acclamation `Psalm 119:135`. Same
psalm.

Eleven antiphons carried the Vulgate number inside the Hebrew-declaring file and
so addressed verses that do not exist. State as of 2026-07-31:

- **Data:** all eleven now carry `psalm_numbering: vulgate` on the proper.
  `tools/mass-propers.numbered_entries` implements the inheritance — a proper
  inherits its calendar's numbering unless it declares its own, and its cycles may
  differ again.
- **Validation:** not yet caught up. `tools/citations.check` still reads only the
  document-level key, so all eleven still report, and `check-calendar-masses`
  still sets them aside through the `psalm_numbering_exceptions` ledger. Net
  effect: `check-calendar-masses` exits 0, `citations check` exits 1.
- **The ledger is self-cleaning in both directions.** A psalm-bound problem at an
  *unlisted* locus still fails. A listed locus that has *stopped* breaching also
  fails, with `delete the entry`. So an entry cannot outlive its defect, and you
  cannot slip a new one in behind the known ones.
- **Owner:** TASK-32 — measure each antiphon against its incipit and decide per
  slot whether the number moves or the declaration does. When it lands the ledger
  empties and goes. Do not pre-empt it by renumbering.

The eleven: `ascension`/Vigil Mass, `ot-6`, `ot-8`, `ot-9`, `ot-22`, `ot-23`,
`ot-26`, `ot-29`, `ot-31`, `ot-33`, `christ-the-king`.

Two references cannot resolve for upstream reasons: `4 Esdras 2:36-37` (not among
the Douay-Rheims' 73 books) and `Malachi 3:19-20a` (Hebrew numbering where the
Vulgate prints Malachi 4:1-6). Only psalms convert between systems.

## Octave-day classification

Within an octave the edition's own punctuation decides, and `calendar-spine`
implements it:

- **colon** → the day's own principal celebration; classify that.
  `Second day within the octave: S. Stephani Protomartyris` → `sanctoral`.
- **semicolon** → a mere commemoration; cut the clause away.
  `Fifth day within the octave; comm. S. Thomae Episcopi et Martyris` → `seasonal`.

So 1962 12-26/27/28 are `sanctoral` and 12-29/30/31 are `seasonal`, and the spine
and the propers now agree. The three seasonal ones are placeholders: the shared
formulary those days actually use is still absent from the file, along with
*D. N. Iesu Christi Regis* and *Sanctissimi Nominis Iesu*. All three are movable
or shared, so nothing in the fixed-date spine reports them missing.

## Open items — name them, do not decide them

| Item | Recorded in |
| --- | --- |
| Twelve of the thirteen 1962 Commons, and the sanctoral pointers into them | 1962 `open_collation_items` |
| Whether the eleven antiphons move their number or keep the per-slot declaration | TASK-32; `psalm_numbering_exceptions` |
| Whether `ascension`, `corpus-christi`, `sacred-heart`, `chrism-mass` belong under `seasonal` or `christological` | 1962 `open_collation_items` |
| A registry scheme for 1962 ferias | 1962 `open_collation_items` |
| A schema for 1962 commemorations | `guidance/liturgy/propers-completion-todo.md` |
| Which numbering system each of a further 23 non-psalm postconciliar citations speaks | postconciliar `open_collation_items` |
| Whether prefaces and the *Oratio super populum* belong in this index | postconciliar `open_collation_items` |
| The 1962 `P = 23` shortfall after Pentecost | `guidance/liturgy/calendar-computation.md` |
| Part-verse letters retained in some Lectionary citations, dropped in others | postconciliar `open_collation_items` |
| Oration conclusions rendered both as printed cue and expanded | both files' `open_collation_items` |

Adding to an `open_collation_items` list is the correct move when you find a
divergence you cannot collate. Silently normalizing it is not.
