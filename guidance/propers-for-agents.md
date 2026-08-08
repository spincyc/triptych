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

A rubric may appoint one text across a **span of days**. That is stated once,
in the calendar's `rubrics.yaml` under `appointed_across`, and carried by each
mass through an ordinary proper-level `takes_from`; the span never holds the
text. `check-calendar-masses`' `span_problems` joins the two.

A proper requires `name` and a `source`, unless it carries `takes_from`:

| `source` | carries | must not carry |
| --- | --- | --- |
| `scripture` | `verses` | `text` |
| `composed` | `text` | `verses` |
| `mixed` | both | — |

Optional on a proper: `incipit`, `notes`, `psalm_numbering`, `cycles`.

**The English is not in `propers.yaml`.** No proper in either calendar carries a
`translations` key; the schema allows one and nothing uses it. Translations live
in sidecar overlays merged at check time —
`src/sources/inventories/<calendar>-proper-translations-v1.toml`, found by
`OVERLAY_DIR`/`OVERLAY_SUFFIX` in `tools/check-calendar-masses` — keyed
`(lang, source_id)`, and selected by `mass-propers --witness` and `--lang`. The
rule that produced this: every validation rule had been written against a
`propers.yaml` key no calendar used, while the file the site actually serves
went unvalidated. Look in the overlay before concluding a text is missing.

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
   `tools/tpt citations encode` to encode a citation; it refuses what it cannot
   encode without guessing. It is idempotent in CONTENT and not in BYTES:
   measured on 2026-08-07, running it on a pristine tree rewrote 5,560 lines of
   `roman-1962/propers.yaml` and 2,960 of the postconciliar, because it reloads
   and re-dumps the whole document and the tracked formatting is not what its
   dumper emits. So the sanctioned way to encode a citation destroys the diff of
   whatever else you were changing. Until that is fixed, encode a new entry by
   calling `citations.parse_citation` — the same function, the same single
   derivation — and splice only the block you are editing.
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
| A verse **past the end of a chapter** | `index-bible` derives a chapter's bounds from the verses the edition prints, so it clamps rather than reports. `Mark 4:41`, `1 Thessalonians 4:18` and `Acts 7:60` were each dropped this way. | Partly closed: `Mark 4:41` and `Acts 7:60` now resolve and only `1 Thessalonians 4:18` still reports. The remedy is a `merged-verse` row in the edition's verse-aliases artifact, because the Douay and Clementine disagree here. |
| **1962 commemorations** | They existed only as prose inside a `name` string, so none could be looked up or commemorated. | Now caught: the sixty folded into feast names are dated entries of rank `Comm.`, 104 in all, and `check-calendar-masses` refuses a `comm.` anywhere but the start of a name. Their orations are still placeholders. |
| The **book's identity** retyped in a second file | `edition` sat in `propers.yaml` and again in `rubrics.yaml`, in both calendars — four hand-typed copies of two strings, with nothing comparing them. They agreed; nothing made them agree. | Now caught: the mass index owns `edition` and `edition_short`, `calendar-rubrics` reads both from it, and `_calendars.restated_identity` refuses a companion that carries either — whether or not its value matches. |
| One formulary **retyped under a second mass** | The schema could not say "this mass takes that text", so a day the Missal carries by a pointer had to be carried by a copy, and nothing compared the copies. The four resumed Sundays after the Epiphany held one set of orations twice and disagreed in five ways — `caelestis`/`coelestis`, `Caelestibus`/`Coelestibus`, `caelestibus`/`coelestibus`, one Introit citation encoded as a contiguous range against three discrete verses, and a dozen truncated incipits. The English was duplicated with it, twelve sidecar rows for four orations. | Now expressible: `takes_from` on a mass or a proper, resolved once by `_calendars.resolve_propers` for both the validator and the browser. The four Sundays now reference `epiphany-3`..`-6` and `pentecost-23` under RGMR 298. **Partly caught** — `span_problems` detects a copy where a span appoints a reference. Outside a declared span nothing does. |
| A witness's **recension** recorded only in prose | The 1962 sidecar's `caution` said its two books' rubrics, seasonal second and third orations, Holy Week and sanctoral "are not those of 1962" — a prose statement of the exact fact the recension model exists to carry, in a field no tool reads. 176 collations had been run against the 1861 under a 1962 heading. | Now caught: every `[[sources]]` row states `attests`/`attests_kind`/`attests_basis` in the act history's own vocabulary, and `source_attestation_problems` in `check-calendar-masses` refuses a row that states none, names an act the history does not carry, uses a kind no witness uses, or contradicts the history about a witness both files hold. A row naming no `source_id` — the project as its own witness — is exempt and witnesses no printing. |
| The **recension stamp** dropped between the derivation and the page | `_calendars.stamp` marks every entry of a recension with `{calendar, kind, stated, text_from, basis, also}` and the tests assert it, but `mass-propers` rebuilt each mass from a key whitelist that omitted it. `roman-pre-1955.json` held 490 masses, zero occurrences of `text_from`, and declared `edition: Missale Romanum, editio typica Vaticana 1920` over text transcribed from a 1962 printing. | Now carried: the structure pass emits `recension` where the stamp is present and omits it where it is not. **The page does not yet print it** — `src/web/browser/liturgy/day.js` still heads the Mass with `edition` alone. |
| A **stale browser structure file** | `make check` verifies that tracked `web/**/*.md` matches current sources; nothing does the same for `src/web/data/structure/propers/*.json`. Commit `8c7c7032c` landed `appointed_across` and thirteen Sequence propers without regenerating them, and the two served missals disagreed for one commit about whether the Easter octave has a Sequence. | Measured on 2026-08-07: regenerating at that day's HEAD, with the tools unchanged, rewrote 4,269 lines of `roman-pre-1955.json` that no source change of that day accounts for. The served recension had drifted that far from its own sources with nothing reporting it. **Now caught for the propers**: `mass-propers structure --check` builds every file in memory and names each tracked one the sources no longer produce, writing nothing; `make check-calendar-masses` runs it. The other six subtrees under `src/web/data/structure` were measured the same day and `calendar`, `rubrics`, `ordinary` and `readings` were current — `catena`, `paragraphs` and `act-history` were not measured and have no such verb. **Partly open** on that account. |
| A rubric appointing one text **across a span of days** | No file could say it. The Easter Sequence survived as an English sentence in a `notes` string — a free field no tool reads and no check tests — the Pentecost span was written nowhere, and eleven of the twelve days inside the two octaves rendered as a finished Mass with no Sequence in it. | Now caught: `appointed_across` in `rubrics.yaml`, read by `_calendars.spans_of`, joined to the masses by `span_problems` in `check-calendar-masses`, which fails on a day appointing no such proper, on one that prints the text instead of referencing it, and on a text out of position. Both loci were read from the controlling facsimile on 2026-08-01. |
| The **English reaching the site and not the terminal** | Translations live in a sidecar overlay, and only `mass-propers structure` merged it. `mass-propers show --lang en` and `mass-today --expanded` read the raw `propers.yaml`, where no proper carries `translations`, so both answered `no en translation recorded; showing Latin` over every one of the 332 orations whose English the same repository was publishing. A maintainer checking whether a proper still needed harvesting was told, by the tool built for that question, that it did. | Now caught: `mass-propers.carry_translations` is the one merge and both verbs call it. The reading view applies no rights filter, unlike the structure pass, because a terminal over tracked sources should show the English the site withholds as well as the English it serves; `untranslated` is printed as a decision, not as a gap. |
| A **chained `takes_from` addressed at its first hop** | `_resolve_reference` followed the chain for the TEXT and then overwrote the provenance with the mass it had just gone through, so a saint borrowing a Common that itself borrows another was addressed at the intermediate. `overlay_key` files a translation under the mass that PRINTS it, so Perpetua and Felicitas, Frances of Rome, Petronilla and Elizabeth looked up their English at a Common carrying none, found nothing, and served Latin while the terminal Common's English sat in the ledger. Text right, address wrong, nothing reporting either. | Now caught: `_resolve_reference` keeps the inner provenance where the inherited proper has one, so the address follows the text, and `mass-propers census`' `unaccounted` count fell from 5 to 0 on the strength of it. That count is the detector: a slot neither translated nor refused. |
| A **coverage census scoped past the gap it measures** | `english_coverage` excluded every scripture-bearing proper, `mixed` among them. A `mixed` proper carries the Missal's own words beside its citations — `Salus populi ego sum` above a psalm verse — and no bible renders those words, so a real gap was counted out of scope, and the rows that closed it then surfaced as `unmatched_records`, which reads as ledger rot and was its opposite. | Now caught: only `source: scripture`, whose English is wholly a bible's, is excluded. 13 postconciliar rows and 8 of the 1962's moved from "rot" into the denominator they belong in. |
| A mass block spliced by **"up to the next mass"** | The 1962 index nests masses under section headings, so the lines between the last mass of one section and the first of the next are the next section's `label:` and `masses:`. A textual edit that treats a mass as running up to the following `- key:` swallows them, and the two sections silently become one. Done on 2026-08-07 it produced 315 christological masses where there are eight, and `check-calendar-masses` passed on it: the schema is still valid, the masses are all still there, and only their filing moved. | Now caught, by accident of having a derived count: `mass-propers census --write` put `roman-1962 | christological | 315` into two documents, which is what made it visible. Nothing checks section membership directly. A block ends at the first line that is not indented into it, and a splice must stop there. |
| Two propers under **one name in one mass** | The translation overlay is keyed `(mass, form, proper name)`. `palm-sunday` prints six propers all named `Procession Antiphon`, so one ledger row answers all six and no row can answer one. A shared refusal is harmless; a shared translation would attach one antiphon's English to five others. | Open. Nothing prevents it, and the 2026-08-07 harvest left the six under a single `untranslated` row for want of a key that could tell them apart. |
| Any **stale count table** | One census of these files existed in three retyped copies, and all three disagreed; the 1962 sanctoral section read 247 in a document that called itself current and 307 in the file. | Now caught for the two documents that carry the derived block — this one and `docs/the-mass.md` — by `mass-propers census --check`, which `make check-propers-census` runs. `guidance/liturgy/propers-completion-todo.md` carried a third and was deleted on 2026-08-01 rather than corrected, its every count having drifted and nothing in it still being both unique and true. `src/sources/calendars/README.md` still carries a hand-typed table. Open. |

## Tool ownership

Never re-derive what a tool owns; that is how two artifacts come to disagree.

| Tool | Owns | Mutates |
| --- | --- | --- |
| `tools/citations` | The canonical book list, citation parsing and encoding, passage validation | yes (`encode`) |
| `tools/check-calendar-masses` | Schema, identity, `propers`/`forms` exclusivity, source-kind rules, cycle shape, the psalm-exception ledger, spine agreement. Delegates citation contents to `citations`. | no |
| `tools/calendar-spine` | The date-ordered list of celebrations and its `kind` classification, derived from the calendar-reference publications | no |
| `tools/mass-propers` | Reading one mass, with the translation overlay merged; per-proper psalm-numbering inheritance; the browser's structure files **and whether the tracked ones are current**; **the census** and the derived block both count-bearing documents carry | yes (`structure`, `census --write`); `structure --check` and `census --check` write nothing |
| `tools/index-bible` | Indexed bibles keyed by the reference strings the calendars actually make; validation of `citation_divergences` | yes |
| `scripts/_psalms.py` | The Vulgate↔Hebrew verse-level concordance and every psalm bound | — |

Invoke through `tools/tpt <tool>`. `make check` runs `check-calendar-masses` and
skips rather than fails without PyYAML.

## Harvesting the 1962 sanctoral from the facsimile

Two findings from 2026-08-08 that make this tractable, both of which cost a
session each to learn the hard way.

**Extract with `pdftotext -raw`, never `-layout`.** The facsimile is set in two
columns. `-layout` preserves the visual grid, which interleaves a day's oration
with whatever sits beside it — the text comes out shuffled between two prayers,
and reconstructing one from it is composition, not reading. `-raw` emits reading
order, so an oration arrives contiguous. Every earlier judgement that oration
extraction from this book was too dangerous to attempt was a judgement about
`-layout`.

**The day names its Common by the book's own number.** Most sanctoral days do
not print a formulary at all; they print a directive, e.g. for 8 August:

    Missa Os iusti, de Communi Confessoris non Pontificis I loco [24],
    praeter orationem sequentem:

That is a `takes_from` and a proper Collect, nothing more, and the bracketed
number is the Missal's own reference into the Commune Sanctorum. 187 such
directives carry one. Join on the NUMBER, not on the Introit incipit: `Os iusti`
heads both the Confessor-not-a-Bishop Mass and the Abbots' Mass, and `Me
exspectaverunt` heads both a Virgins' and a non-Virgins' Mass, so the incipit
alone is ambiguous where the number never is. The Commons are already complete,
so a large part of what looks like missing text is a missing pointer.

**But the Commons are complete in orations only, which the census does not say.**
Measured 2026-08-08 across all thirty: 30 Postcommunions, 29 Collects, 29 Secrets
-- and 6 Introits, 6 Gospels, 4 Lessons, 3 Graduals, 3 Alleluias, 3 Offertories,
2 Epistles, 2 Communions. `Masses holding only placeholders` reads 0 for the
common section because every one of them holds real orations, which is true and
is not the same as complete. So pointing a saint's day at its Common gives that
day its Secret and its Postcommunion and no scripture at all, which is what 8
August does now. **Filling the Commons' scripture is the unlock**: it is thirty
masses of work, not ninety-four, and it completes every day that points at them.
Citations survive this text layer well -- they are short printed references, not
prose under a drop capital -- so the objection that stopped the orations does not
apply to them.

**Why those 55 days carry a `Collect` named placeholder, and why the census reads
55 unaccounted because of it.** A day that takes a Common `praeter orationem`
has its OWN Collect. Leave the slot empty and the Common's Collect resolves
through and is printed as the day's -- for 8 August that is `Deus, qui nos beati
N. Confessoris tui`, a generic prayer with the saint's name left as `N.`,
presented as if it were St John Vianney's. Naming the placeholder `Collect`
overrides the borrowed one and blocks that. The cost is that
`mass-propers census` counts a Collect-family slot with no English, so the
1962 `unaccounted` figure went 0 -> 55. The figure is TRUE: those days' own
Collects are not transcribed at all. A zero bought by printing the wrong prayer
is the worse trade, and this was tried both ways on 2026-08-08 before choosing.

What the number does NOT settle is the day's own orations, which still have to
be read, and the drop-capital of each oration OCRs as garbage (`^\mnipotens`)
and has to be repaired from the following letters.

**A BRACKET NUMBER IS EDITION-SPECIFIC. Never carry one between books.** The
1862 Pustet prints `S. Franciscae ... Missa. Cognovi. de Comm. nec Virg. nec
Mart. [35]` where the 1962 prints `[37]` for the same Mass. Both are right about
their own book and the map above is the 1962's alone. Read as confirmation of
each other they would move Frances of Rome from the Common she takes to the one
before it. The incipit -- `Cognovi` -- is what is comparable across editions;
the number never is.

**Read the ORATIONS off the page images, not off any text layer.** Three
sessions reported the orations untranscribable, and all three were reading OCR.
The CMAA facsimile destroys them under drop capitals; the tracked 1862's own
text layer is no better, corrupting roughly one word in three -- its Casimir
Collect reads `DEus, quLinter reg&les de-licias ... virttite const&ntise
robor&sti: qusesu-mus; ut ejus intercessi6nefid6-les tui terr6na despiciant, et
ad ccel6stia`. The 1862's PAGE IMAGES are clean and legible at
`https://archive.org/download/bub_gb_E7sPAAAAIAAJ/page/n<leaf>_w1000.jpg`
(922 leaves, item `bub_gb_E7sPAAAAIAAJ`, the same public-domain printing the
library already tracks). Leaf n498 gives Frances of Rome's Collect entire and
without damage. This is the route, and it is the same one the 1861 English was
collated by at 200 and 400 dpi.

## Commands to check a claim

```sh
# Full gate. Exits 0 while the psalm-exception ledger holds; prints
# "calendar-mass excepted:" for each ledgered locus and the per-file totals.
tools/tpt check-calendar-masses
tools/tpt check-calendar-masses --calendar roman-1962

# Whether the browser is served what these sources produce now. Writes
# nothing; `mass-propers structure` is what fixes a failure. Run by
# `make check-calendar-masses` beside the validator above.
tools/tpt mass-propers structure --check

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
| roman-pre-1955 | seasonal | 6 | 6 | 6 |
| roman-1962 | seasonal | 128 | 1152 | 3 |
| roman-1962 | christological | 8 | 66 | 0 |
| roman-1962 | marian | 18 | 86 | 2 |
| roman-1962 | sanctoral | 307 | 1078 | 26 |
| roman-1962 | common | 30 | 334 | 0 |
| postconciliar | seasonal | 67 | 832 | 2 |
| postconciliar | christological | 7 | 23 | 3 |
| postconciliar | marian | 14 | 52 | 4 |
| postconciliar | sanctoral | 181 | 606 | 44 |

| Calendar | Rank | Entries | Celebrations |
| --- | --- | ---: | ---: |
| roman-pre-1955 | (no rank) | 6 | 6 |
| roman-1962 | (no rank) | 93 | 93 |
| roman-1962 | Comm. | 104 | 104 |
| roman-1962 | I | 37 | 37 |
| roman-1962 | II | 46 | 47 |
| roman-1962 | III | 211 | 211 |
| postconciliar | (no rank) | 64 | 64 |
| postconciliar | All Souls commemoration | 1 | 1 |
| postconciliar | Feast | 24 | 24 |
| postconciliar | Memorial | 69 | 69 |
| postconciliar | Optional memorial | 82 | 82 |
| postconciliar | Optional memorials | 18 | 38 |
| postconciliar | Solemnity | 11 | 11 |

| Measure | roman-pre-1955 | roman-1962 | postconciliar |
| --- | ---: | ---: | ---: |
| Masses | 6 | 491 | 269 |
| Propers | 6 | 2716 | 1513 |
| — named `Placeholder` | 6 | 31 | 55 |
| — inside a `forms` block | 0 | 147 | 140 |
| — carrying a `cycles` mapping | 0 | 0 | 253 |
| Masses holding only placeholders | 6 | 31 | 53 |
| Masses taking a formulary from another entry | 0 | 161 | 0 |
| Propers taking their text from another entry | 0 | 53 | 0 |
| Propers that are not placeholders | 0 | 2685 | 1458 |
| — of those, scripture-bearing | 0 | 2192 | 1185 |
| Encoded passages | 0 | 2598 | 1721 |
| Distinct books cited | 0 | 57 | 63 |
| Distinct slot names | 1 | 119 | 89 |

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

What the census does not cover, and what still has to be counted by reading:

- 63 of the 1962 seasonal entries carry only their scripture-bearing propers and
  a `notes` line saying so; their registry ids read `1962-T-<key>` and are
  synthetic. Three further entries carry that registry form without the note.
  Identity, rank and citations were read from an **OCR text layer** of the CMAA
  1962 facsimile, not the images. Nothing has been visually collated.
- `src/sources/calendars/README.md` still carries a hand-typed count table that
  nothing regenerates. Treat it as stale, and do not copy a figure out of it.

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

Two references cannot resolve: `4 Esdras 2:36-37` (not among the Douay-Rheims'
73 books) and `1 Thessalonians 4:18` (past the last verse this edition prints in
that chapter). `Malachi 3:19-20a` used to be a third and now resolves. Only
psalms convert between systems.

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
| A schema giving a commemoration's own three orations somewhere to live — the 104 are dated entries of rank `Comm.`, but their orations are still placeholders | 1962 `open_collation_items` |
| Which numbering system each of a further 23 non-psalm postconciliar citations speaks | postconciliar `open_collation_items` |
| Whether prefaces and the *Oratio super populum* belong in this index | postconciliar `open_collation_items` |
| The 1962 `P = 23` shortfall after Pentecost | `guidance/liturgy/calendar-computation.md` |
| Part-verse letters retained in some Lectionary citations, dropped in others | postconciliar `open_collation_items` |
| Oration conclusions rendered both as printed cue and expanded | both files' `open_collation_items` |
| A public-domain English for the 1962 Holy Week's 39 slots, which the 1861 witness cannot supply — measured 2026-08-07, not assumed | 1962 sidecar's `verification`, sixth pass; an acquisition like the Sequences below, not a collation of the book already held |
| A public-domain English for the five great Sequences, which the 1861 witness prints in Latin only | 1962 sidecar's `verification`, sixth pass; a source acquisition under `guidance/sources.md`, not a harvest. **Scoped 2026-08-07, not decided.** The obvious candidate is Caswall's *Lyra Catholica* (London, 1849), Internet Archive `lyracatholicaco00caswgoog`: it reaches four of the five — Victimae paschali, Veni Sancte Spiritus, Lauda Sion, Stabat Mater — and not the Dies irae, which is a Requiem sequence and outside its scope. Its bytes carry Google's front matter as a single contiguous head block, which is the shape the 1843 audit records as admitting the stated-deletion derivative route, unlike the 1861's page-foot stamp. What is NOT a mechanical question is which translator the project stands behind: Caswall, Neale and Aylward differ materially, and these are five of its most-read texts, so the choice is editorial and the maintainer's. Name the cost, do not pick the voice. |
| Three commemorations whose Latin the index reprints from a Common instead of referencing it, and whose English is therefore recorded twice | the three rows' own `harvest_note`; the fix is a `takes_from` and belongs to the lane owning `propers.yaml` |

Adding to an `open_collation_items` list is the correct move when you find a
divergence you cannot collate. Silently normalizing it is not.
