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
string** — `'01'`, never `01`. It may carry `date`, `rank`, `season`, `kind`,
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
`name`. A proper in one form may name a directly printed proper in a different
sibling form of the same mass; mass-level and same-form self-references remain
cycles. `src/sources/calendars/README.md` owns the full rule.

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

Optional on a proper: `incipit`, `notes`, `psalm_numbering`, `cycles`,
`weekday_cycles`.

**The English is not in `propers.yaml`.** No proper in either calendar carries a
`translations` key; the schema allows one and nothing uses it. Translations live
in sidecar overlays merged at check time —
`src/sources/inventories/<calendar>-proper-translations-v1.toml`, found by
`OVERLAY_DIR`/`OVERLAY_SUFFIX` in `tools/check-calendar-masses` — keyed
`(lang, source_id)`, and selected by `mass-propers --witness` and `--lang`. The
rule that produced this: every validation rule had been written against a
`propers.yaml` key no calendar used, while the file the site actually serves
went unvalidated. Look in the overlay before concluding a text is missing.

An exact exemplar can be held as **text-free witness metadata** while its body
remains unavailable. Such an `[[untranslated]]` row uses the exact canonical
target, a typed reason, `witness_artifact_id`, `witness_passage_id`, and the
verified date and page locator; the calendar checker resolves the passage,
artifact, page range, date, and hash. The browser structure receives only the
target, language, and unavailable or rights-restricted state. It never receives
the witness ids, locator, rights analysis, quarantine hash, or protected words.

Palm Sunday's Simple Entrance Antiphon is the controlling mixed-rights case.
The official ICEL Antiphonary, artifact page 44 and printed p. 36, interleaves
ICEL spans with its Revised Grail Psalm 23:9-10 span. The exact exemplar is held;
`no-exemplar` is false. The whole body is `rights-withheld` on every current
surface because no one basis reaches both rightsholders and the current model
cannot publish spans independently. Do not attach ICEL's `permission` token to
the whole row or substitute a selected Bible and call the result the approved
English.

The same source boundary runs the other direction for Gospel Acclamations. The
official ICEL Antiphonary contains none. Nativity Vigil and Day, Pentecost Vigil
and Day, Easter 3 Year C, and Ordinary Time 15 Year A therefore remain exact
`no-exemplar` rows: their rejected liturgies.net payloads are only hash-bound
source candidates for Lectionary/CCD text, and a USCCB comparison is not a
redistribution grant. Never inherit ICEL permission merely because an
unofficial page labels one of these rows “Roman Missal / ICEL Music.”

`cycles` is keyed `A`/`B`/`C` and excludes top-level `verses` and `text`. Where
cycles differ in kind, `source` moves inside each cycle; otherwise it stays on
the proper. Postconciliar only — a 1962 proper must never carry one.

`weekday_cycles` is the Lectionary's **other** cycle, keyed `'I'`/`'II'` and
quoted, with the same inner contract. The two are not one scale and must never
be poured into one key: `check-calendar-masses` refuses a letter under
`weekday_cycles`, a numeral under `cycles`, both keys on one proper, the key in
any calendar but the postconciliar, and the key on a proper whose mass is not
`ordinary-time` — the General Introduction confines I/II to the Ordinary Time
ferial course, and a numeral outside it is a category error, not a fact.
`src/sources/calendars/README.md` owns the shape;
`guidance/liturgy/calendar-computation.md` owns which cycle a year is in.

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

Never encode a missing formulary as a composed proper named `Placeholder`.
That boilerplate is repository apparatus, not a source-owned Proper slot. A
whole Mass whose Missal wording is unavailable carries a mass-level
`text_status` with `state: unavailable`, `scope: missal-formulary`, and one or
more typed `witness-gap`, `rights-withheld`, or `no-exemplar` reasons; it carries
no `propers` or `forms`. This applies to dated and seasonal masses as well as
text-free Commons. A non-Common Mass with some genuine target wording may use
`state: partial` beside exactly one of `propers` or `forms`; the typed status
accounts for the rest without inventing content.

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
| A psalm verse **beyond the end of its psalm** under the file's declared numbering | The bounds check once held ceilings for six psalms only, so `Psalm 118:137` passed although Hebrew 118 ends at 29. | Now caught: every psalm is bounded from the tracked verse-level concordance. Three loci remain ledgered across four owning slots. |
| A celebration in the **spine and in no section** | The two artifacts had different histories and nothing compared them. Three Christmas octave days sat in the gap. | Now caught: `spine_problems` in `check-calendar-masses`. |
| A verse **past the end of a chapter** | `index-bible` derives a chapter's bounds from the verses the edition prints, so it clamps rather than reports. `Mark 4:41`, `1 Thessalonians 4:18` and `Acts 7:60` were each dropped this way. | Partly closed: `Mark 4:41` and `Acts 7:60` now resolve and only `1 Thessalonians 4:18` still reports. The remedy is a `merged-verse` row in the edition's verse-aliases artifact, because the Douay and Clementine disagree here. |
| **1962 commemorations** | They existed only as prose inside a `name` string, so none could be looked up or commemorated. | Now caught: the sixty folded into feast names are dated entries of rank `Comm.`, 104 in all, and `check-calendar-masses` refuses a `comm.` anywhere but the start of a name. Their three appointed oration identities are typed text-free witness gaps, not placeholders or invented bodies. |
| The **book's identity** retyped in a second file | `edition` sat in `propers.yaml` and again in `rubrics.yaml`, in both calendars — four hand-typed copies of two strings, with nothing comparing them. They agreed; nothing made them agree. | Now caught: the mass index owns `edition` and `edition_short`, `calendar-rubrics` reads both from it, and `_calendars.restated_identity` refuses a companion that carries either — whether or not its value matches. |
| One formulary **retyped under a second mass** | The schema could not say "this mass takes that text", so a day the Missal carries by a pointer had to be carried by a copy, and nothing compared the copies. The four resumed Sundays after the Epiphany held one set of orations twice and disagreed in five ways — `caelestis`/`coelestis`, `Caelestibus`/`Coelestibus`, `caelestibus`/`coelestibus`, one Introit citation encoded as a contiguous range against three discrete verses, and a dozen truncated incipits. The English was duplicated with it, twelve sidecar rows for four orations. | Now expressible: `takes_from` on a mass or a proper, resolved once by `_calendars.resolve_propers` for both the validator and the browser. The four Sundays now reference `epiphany-3`..`-6` and `pentecost-23` under RGMR 298. **Partly caught** — `span_problems` detects a copy where a span appoints a reference. Outside a declared span nothing does. |
| A witness's **recension** recorded only in prose | The 1962 sidecar's `caution` said its two books' rubrics, seasonal second and third orations, Holy Week and sanctoral "are not those of 1962" — a prose statement of the exact fact the recension model exists to carry, in a field no tool reads. 176 collations had been run against the 1861 under a 1962 heading. | Now caught: every `[[sources]]` row states `attests`/`attests_kind`/`attests_basis` in the act history's own vocabulary, and `source_attestation_problems` in `check-calendar-masses` refuses a row that states none, names an act the history does not carry, uses a kind no witness uses, or contradicts the history about a witness both files hold. A row naming no `source_id` — the project as its own witness — is exempt and witnesses no printing. |
| The **recension stamp** dropped between the derivation and the page | `_calendars.stamp` marks every entry of a recension with `{calendar, kind, stated, text_from, basis, act?, also[{kind, basis, act?}]}` and the tests assert it, but `mass-propers` rebuilt each mass from a key whitelist that omitted it. `roman-pre-1955.json` held 490 masses, zero occurrences of `text_from`, and declared `edition: Missale Romanum, editio typica Vaticana 1920` over text transcribed from a 1962 printing. | Now carried and rendered: the structure pass emits `recension` where the stamp is present, carries the aggregate `stands_before` boundary, and both readers expose the boundary and any row-level act-history station. An `unrecorded` station is not restated as a proved causal act. |
| A **stale browser structure file** | `make check` verifies that tracked `web/**/*.md` matches current sources; nothing does the same for `src/web/data/structure/propers/*.json`. Commit `8c7c7032c` landed `appointed_across` and thirteen Sequence propers without regenerating them, and the two served missals disagreed for one commit about whether the Easter octave has a Sequence. | Measured on 2026-08-07: regenerating at that day's HEAD, with the tools unchanged, rewrote 4,269 lines of `roman-pre-1955.json` that no source change of that day accounts for. The served recension had drifted that far from its own sources with nothing reporting it. **Now caught for the propers**: `mass-propers structure --check` builds every file in memory and names each tracked one the sources no longer produce, writing nothing; `make check-calendar-masses` runs it. The other six subtrees under `src/web/data/structure` were measured the same day and `calendar`, `rubrics`, `ordinary` and `readings` were current — `catena`, `paragraphs` and `act-history` were not measured and have no such verb. **Partly open** on that account. |
| A rubric appointing one text **across a span of days** | No file could say it. The Easter Sequence survived as an English sentence in a `notes` string — a free field no tool reads and no check tests — the Pentecost span was written nowhere, and eleven of the twelve days inside the two octaves rendered as a finished Mass with no Sequence in it. | Now caught: `appointed_across` in `rubrics.yaml`, read by `_calendars.spans_of`, joined to the masses by `span_problems` in `check-calendar-masses`, which fails on a day appointing no such proper, on one that prints the text instead of referencing it, and on a text out of position. Both loci were read from the controlling facsimile on 2026-08-01. |
| The **English reaching the site and not the terminal** | Translations live in a sidecar overlay, and only `mass-propers structure` merged it. `mass-propers show --lang en` and `mass-today --expanded` read the raw `propers.yaml`, where no proper carries `translations`, so both answered `no en translation recorded; showing Latin` over every one of the 332 orations whose English the same repository was publishing. A maintainer checking whether a proper still needed harvesting was told, by the tool built for that question, that it did. | Now caught: `mass-propers.carry_translations` is the one merge and both verbs call it. The reading view applies no rights filter, unlike the structure pass, because a terminal over tracked sources should show the English the site withholds as well as the English it serves; `untranslated` is printed as a decision, not as a gap. |
| A **chained `takes_from` addressed at its first hop** | `_resolve_reference` followed the chain for the TEXT and then overwrote the provenance with the mass it had just gone through, so a saint borrowing a Common that itself borrows another was addressed at the intermediate. `overlay_key` files a translation under the mass that PRINTS it, so Perpetua and Felicitas, Frances of Rome, Petronilla and Elizabeth looked up their English at a Common carrying none, found nothing, and served Latin while the terminal Common's English sat in the ledger. Text right, address wrong, nothing reporting either. | Now caught: `_resolve_reference` keeps the inner provenance where the inherited proper has one, so the address follows the text, and `mass-propers census`' `unaccounted` count fell from 5 to 0 on the strength of it. That count is the detector: a slot neither translated nor refused. |
| A **coverage census scoped past the gap it measures** | `english_coverage` excluded every scripture-bearing proper, `mixed` among them. A `mixed` proper carries the Missal's own words beside its citations — `Salus populi ego sum` above a psalm verse — and no bible renders those words, so a real gap was counted out of scope, and the rows that closed it then surfaced as `unmatched_records`, which reads as ledger rot and was its opposite. | Now caught: only `source: scripture`, whose English is wholly a bible's, is excluded. 13 postconciliar rows and 8 of the 1962's moved from "rot" into the denominator they belong in. |
| A mass block spliced by **"up to the next mass"** | The 1962 index nests masses under section headings, so the lines between the last mass of one section and the first of the next are the next section's `label:` and `masses:`. A textual edit that treats a mass as running up to the following `- key:` swallows them, and the two sections silently become one. Done on 2026-08-07 it produced 315 christological masses where there are eight, and `check-calendar-masses` passed on it: the schema is still valid, the masses are all still there, and only their filing moved. | Now caught, by accident of having a derived count: `mass-propers census --write` put `roman-1962 | christological | 315` into two documents, which is what made it visible. Nothing checks section membership directly. A block ends at the first line that is not indented into it, and a splice must stop there. |
| Two propers under **one name in one mass** | Palm Sunday has seven targets named `Procession Antiphon`: six direct source-owned bodies and one Scripture-owned occurrence. An overlay key omitting occurrence would attach one antiphon's English to the others. | Now caught: translation identities are `(mass, form_id, proper name, cycle, occurrence)`. The 2026-08-27 page-image collation attaches Cummiskey English only to occurrences 1–3; occurrence 4 remains Scripture-owned and occurrences 5–7 retain exact no-witness dispositions. The Latin-provenance ledger counts only its six direct bodies, so its occurrence ordinals are not translation ordinals. |
| Propers stored **out of the order the edition prints them** | The schema stays valid and census counts move correctly unless order is checked explicitly. The 2026-08-08 scripture wave appended newly transcribed propers **above** the pre-existing orations, so 49 Commons, sanctoral and marian formularies stood Introit..Communion, Collect, Secret, Postcommunion. The browser's seating walks the propers in file order and by contract never reorders, so the Collect broke the walk and it and everything after it lost their seat: **243 masses — very nearly half the 1962 index — refused the Day reader's Missal mode** and 219 dated days of 2026 with them (the denominator is the census's own and is deliberately not retyped here), while Read mode printed the orations after the Communion without saying anything. | Data corrected and now enforced: the 1962 typical edition prints Introit, Oratio, Epistle, Gradual, Alleluia, Tract, Gospel, Offertory, Secreta, Communion, Postcommunio — read on the CMAA facsimile of the controlling edition, Commune unius Martyris I at marginal nos. 4193–4203 and S. Martini at 4073–4075 — and the 49 lists were restored by moving whole blocks. `order_problems` in `check-calendar-masses` validates each formulary, requires every temporary `proper_order_exceptions` row to remain necessary, and compares qualified names by their canonical proper family. Legitimate variants such as `Collect (in plurali)`, `Secret (Altera secreta)`, `Sequence`, and `Greater Alleluia` are therefore handled without turning their qualifiers into an escape from ordering. |
| A guard that **disables the only way out** | `setDateSurfaceEnabled` was rewritten on 2026-08-08 so the navigating controls stopped following its `enabled` argument and followed `Boolean(runtime.missals && runtime.missals.length)` instead. The intent was right — a failed outcome must not disable the date box, the missal select, Apply and Today, which are the only controls able to reach another day. The execution tied them to manifest state, so any paint before `loadManifests()` fills `runtime.missals` freezes the whole surface, which is what the maintainer reported hours later. | Open, and the first move is to revert to `enabled` for every control before re-attempting the fix. The safer shape is to leave the controls live always and let the click handlers refuse, so no state a renderer can be in disables the escape. |
| A tracked file **written where the source library forbids it** | `source-library validate` rejects any file under `src/sources` outside its own schema list — this file says so — and a research survey was written to `src/sources/inventories` anyway. Nothing local caught it: `make check-calendar-masses` and the census both pass, because neither validates that tree. GitHub Pages did, at `check-deployment-sources`, and refused to publish. | Now removed. The lesson is placement, not validation: a finding belongs in guidance or a document, and only a record matching a source-library schema belongs under `src/sources`. |
| Any **stale count table** | One census of these files existed in three retyped copies, and all three disagreed; the 1962 sanctoral section read 247 in a document that called itself current and 307 in the file. | Now caught for all three documents carrying the identical derived block — this one, `docs/the-mass.md`, and `src/sources/calendars/README.md` — by `mass-propers census --check`, which `make check-propers-census` runs. |

## Tool ownership

Never re-derive what a tool owns; that is how two artifacts come to disagree.

| Tool | Owns | Mutates |
| --- | --- | --- |
| `tools/citations` | The canonical book list, citation parsing and encoding, passage validation | yes (`encode`) |
| `tools/check-calendar-masses` | Schema, identity, `propers`/`forms` exclusivity, source-kind rules, cycle shape, the psalm-exception ledger, spine agreement. Delegates citation contents to `citations`. | no |
| `tools/calendar-spine` | The date-ordered list of celebrations and its `kind` classification, derived from the calendar-reference publications | no |
| `tools/mass-propers` | Reading one mass, with the translation overlay merged; per-proper psalm-numbering inheritance; the browser's structure files **and whether the tracked ones are current**; **the census** and every document's identical derived block | yes (`structure`, `census --write`); `structure --check` and `census --check` write nothing |
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

**The Commons are structurally populated; that is not a body-completeness claim.**
The current Common section carries 30 Masses and 358 direct proper nodes: 214
scripture or mixed appointments, 111 composed nodes, and 33 proper references.
It carries zero literal Latin bodies. The composed appointments are typed
unavailable or resolve to such a node, and six targets expose mutually exclusive
oration options through `common_sets`. Counts of nodes or resolved occurrences
therefore establish appointment structure, not textual availability or collation.

**Why those 55 days carry a text-free `Collect`, while the census reads zero
unaccounted.** A day that takes a Common `praeter orationem`
has its OWN Collect. Leave the slot empty and the Common's Collect resolves
through and is printed as the day's -- for 8 August that is `Deus, qui nos beati
N. Confessoris tui`, a generic prayer with the saint's name left as `N.`,
presented as if it were St John Vianney's. A typed unavailable proper-body node
named `Collect` overrides the borrowed one and blocks that false substitution.
Its exact English `untranslated` identity makes the absence accounted, so zero
`unaccounted` means complete disposition, not complete text. Those days' own
Collect bodies remain unavailable.

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

## What a public-domain printing can and cannot supply

Sixteen agents read the 1862 page images on 2026-08-08 and settled the ceiling
this project has been circling for a week.

**1962: 66 of the 80 missing Collects were read and landed.** The rest are not a
reading failure. A pre-1931 printing cannot contain a saint canonised after it,
and each of these was confirmed by opening the leaf where the day would be, not
by failing to grep: John Vianney (1925, leaf 597 shows 8 August as Ss. Cyriaci,
Largi et Smaragdi), John Eudes (1925), Peter Canisius (1925), Laurence of
Brindisi (1881), Claret (1950), Gregory Barbarigo (1960), Albert the Great,
Ephraem. Others need no Collect at all -- Evaristus, the Lateran Dedication and
Cornelius & Cyprian take their whole Mass from a Common and print no proper
oration, so the right entry there is the pointer alone.

**Postconciliar: 31 of 53 now have a located public-domain historical source,
22 have none, and 0 remain undecided as acquisition questions.** Target-edition
collation is a separate gate and remains open for all 31. The negatives are one
fact wearing many names -- Fatima, Guadalupe, Kolbe, Teresa of Calcutta, Padre
Pio, Faustina, Paul VI, John XXIII, John Paul II, Juan Diego, Mother of the
Church: every one canonised or inserted after 1931.

The two former undecideds are **Bede and Rita of Cascia**. The exact
public-domain witness is
`artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.ia-scan-pdf-9873693a`,
a Tours Mame 1922 `editio quarta juxta typicam Vaticanam`, not an authenticated
Vatican 1920 impression. Bede is in its universal sanctoral at PDF
artifact pages 715-716, printed pages 601-602: the Common-of-Doctors pointer and
proper Collect, Secret and Postcommunion. Rita is absent only from the bounded
universal-sanctoral sequence, whose printed page 598 ends 20 May and page 599
begins 25 May; the same book's `Missae pro aliquibus locis` appendix carries her
complete 22 May Mass at PDF artifact pages 1109-1111, printed appendix pages
[79]-[81]. Reading only the universal sanctoral would therefore report a false
whole-book absence. Passage records carry all four visual bounds. Neither
historical formulary has been compared with the restricted 2002 target edition,
so neither result licenses filling the postconciliar prayer slots.

**What 31 located antecedents does NOT mean.** The agents established a
public-domain historical source locus for each: 29 supply at least one proper
oration, while Blaise and Eusebius print a Common pointer and no proper oration.
They did NOT establish that the 2002 Missal's oration is any historical text --
the MR 2002 is in copyright and not held here, so the per-oration match stays an
editorial determination. Denis, Clement and Catherine were flagged as likely
revisions.

**Reading the 1862: leaf = printed page + 85**, derived independently by six
lanes and constant through the main body. It breaks in the appendices, where the
OCR text order does not track physical leaves; there, read one page, note its
printed folio, and step by folio. Two traps the sanctoral sets: its *Festa
Januarii* opens at 11 January, so 22 December to 10 January sits in the
Temporale (Telesphorus, 5 January, is at leaf 116, some 350 leaves from where a
date-ordered guess puts him); and the Proprium de Sanctis begins at 29 November
and ends at 26 November, so late-November feasts are split across both ends.

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

# Citation contents only. Exits 0 while reporting the three ledgered loci at
# their four owning slots; an unledgered breach or stale ledger row still fails.
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
| roman-pre-1955 | seasonal | 6 | 0 | 0 |
| roman-pre-1955 | marian | 1 | 0 | 0 |
| roman-pre-1955 | sanctoral | 1 | 0 | 0 |
| roman-1962 | seasonal | 128 | 1352 | 0 |
| roman-1962 | christological | 8 | 96 | 0 |
| roman-1962 | marian | 18 | 124 | 0 |
| roman-1962 | sanctoral | 307 | 1511 | 0 |
| roman-1962 | common | 30 | 358 | 0 |
| postconciliar | seasonal | 390 | 2116 | 0 |
| postconciliar | christological | 7 | 69 | 0 |
| postconciliar | marian | 14 | 52 | 0 |
| postconciliar | sanctoral | 201 | 761 | 0 |
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
| Propers | 0 | 3441 | 2998 |
| — named `Placeholder` | 0 | 0 | 0 |
| — inside a `forms` block | 0 | 182 | 188 |
| — carrying a `cycles` mapping | 0 | 0 | 258 |
| — carrying a `weekday_cycles` mapping | 0 | 0 | 409 |
| Masses holding only placeholders | 0 | 0 | 0 |
| Masses taking a formulary from another entry | 0 | 164 | 0 |
| Propers taking their text from another entry | 0 | 70 | 49 |
| Propers that are not placeholders | 0 | 3441 | 2998 |
| — of those, scripture-bearing | 0 | 2194 | 2635 |
| Encoded passages | 0 | 2600 | 3590 |
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

What the census does not cover, and what still has to be counted by reading:

- The 63-entry temporal expansion retains a `notes` line marking its
  transcription boundary. Where exact wording remains unheld, each
  source-established Collect, Secret and Postcommunion is an explicit composed
  Proper whose `text_status.state` is `unavailable` and whose reason is
  `witness-gap`. Its registry ids read `1962-T-<key>` and are synthetic; three
  further entries carry that registry form without the note. Identity, rank and
  citations were read from an **OCR text layer** of the CMAA 1962 facsimile, not
  the images. Nothing has been visually collated.
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

Eleven antiphons once carried the Vulgate number inside the Hebrew-declaring
file and therefore addressed verses that did not exist under the inherited
numbering. Their propers now declare their numbering; all their shifted loci
have self-cleaned from the exception ledger, while the out-of-bound
`Psalm 28:11` endpoint remains. Three unresolved loci remain across four owning
slots: that antiphon endpoint and two responsorial-psalm endpoints.

- **Data:** the former eleven antiphons carry `psalm_numbering: vulgate` on the
  proper. Their Vulgate-to-Hebrew shifts no longer breach; `Psalm 28:11` still
  exceeds the tracked Vulgate bound.
  `tools/mass-propers.numbered_entries` implements the inheritance — a proper
  inherits its calendar's numbering unless it declares its own, and its cycles may
  differ again.
- **Validation:** `tools/citations.check` and `check-calendar-masses` both honor
  the per-proper declaration. Each reports the three ledgered loci at their four
  owning slots without failing.
- **The ledger is self-cleaning in both directions.** A psalm-bound problem at an
  *unlisted* locus still fails. A listed locus that has *stopped* breaching also
  fails, with `delete the entry`. So an entry cannot outlive its defect, and you
  cannot slip a new one in behind the known ones.
- **Remaining decisions:** `Psalm 28:11` requires checking the Communion
  Antiphon's printed text and verse bound. `Psalm 56:14` and `Psalm 150:6` are
  responsorial endpoints and require checking the Ordo's numbering rather than
  treating them as antiphon renumberings.

The three loci are `Psalm 28:11` at `christ-the-king`, `Psalm 56:14` at
`ot-24-saturday` cycle II, and `Psalm 150:6` at both `ot-23-thursday` cycle I
and `ot-33-wednesday` cycle II.

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
and the propers now agree. The fifth day owns the shared formulary: the Day Mass
chants and orations with the Dawn Mass's Titus 3:4-7 and Luke 2:15-20 readings.
The sixth and seventh days reference that resolved hybrid. None of the three is
a placeholder.

## The corpus targets, and what each still owes

The maintainer's brief at `guidance/liturgical-corpus-brief-2026-08-21.md` asks
for three missal states to be measured and completed. Its sections 7 to 9 are
the target list; this section is where they live, because this file owns the
data they describe. Read the counts from `mass-propers census`, never from here.

**1962.** This is the most populated state, not an independently complete one.
The 1862 Pustet printing and the 1861 Cummiskey English are public-domain
witnesses, while use of the CMAA facsimile of the controlling edition is bounded
by the 103(b) analysis at
`src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`.
The derived census measures represented rows and translation dispositions; it
does not establish a complete expected-slot universe, full target-edition
collation, or per-text provenance. Open Latin, English, Common, Ordinary, Holy
Week, and calendar questions remain in the owning inventories and lists below.

**Postconciliar.** This is an index and a collection of bounded text routes, not
a complete transcription of the 2002 Missal. The restricted target-edition
artifact is not a publication source. The calendar carries extensive Lectionary
assignments as facts about what is appointed, but the current census does not
prove that the target universe is exhaustively modelled or collated. Stored
Latin bodies mix independently witnessed antecedents with rows whose exact
target-edition relation remains unrepresented. ICEL's standing permission is
recorded, but the current clonable/downloadable route publishes no ICEL payload
on that basis. The seven edition-identified Common identities carry typed
unavailable/rights dispositions rather than target-edition formularies. Counts
of represented masses, propers, translations, or non-placeholder rows must not
be reported as textual, provenance, rights, or whole-book completeness.

**Pre-1955.** A structural-only RECENSION and not a corpus:
`roman-pre-1955` holds only stated structural departure rows. Known-different
formularies whose target wording is not held use typed whole-Mass unavailable
status, not pseudo-Proper placeholders, and every unstated formulary is
mechanically inherited from `roman-1962` without target-recension collation.
The file holds no independently transcribed target Proper wording. The inherited
mass count is therefore an assembly result, not evidence that the pre-1955
Missal agrees with 1962 or that either book is complete. Where the Triduum has
been examined, 20 of 38 modelled units do not survive the reform. The known
distance to 1962 was made by four acts: the `stands_before` list names both
explicit 1955 boundaries, while optional row-level `act` values preserve the
act-history station or attribution for each established departure claim;
`guidance/recensions.md` and the coverage header own the precise boundaries and
apportionment.

## Open items — name them, do not decide them

| Item | Recorded in |
| --- | --- |
| Seven sanctoral pointers whose printed evidence does not yet choose among the typed Common-set candidates | 1962 `open_collation_items` and `finding_aid_coverage[*].unresolved_common_set_selections` |
| The unresolved bound or numbering of `Psalm 28:11`, `Psalm 56:14`, and `Psalm 150:6` across their four owning slots | postconciliar `psalm_numbering_exceptions` |
| Whether `ascension`, `corpus-christi`, `sacred-heart`, `chrism-mass` belong under `seasonal` or `christological` | 1962 `open_collation_items` |
| A registry scheme for 1962 ferias | 1962 `open_collation_items` |
| Exact bodies for the 104 commemorations' three appointed text-free oration identities | 1962 `open_collation_items` and translation sidecar |
| Which numbering system each of a further 23 non-psalm postconciliar citations speaks | postconciliar `open_collation_items` |
| Whether prefaces and the *Oratio super populum* belong in this index | postconciliar `open_collation_items` |
| The 1962 `P = 23` shortfall after Pentecost | `guidance/liturgy/calendar-computation.md` |
| Part-verse letters retained in some Lectionary citations, dropped in others | postconciliar `open_collation_items` |
| Oration conclusions rendered both as printed cue and expanded | both files' `open_collation_items` |
| A public-domain English for the 1962 Holy Week's remaining 36 slots. The 2026-08-27 page-image collation recovered three Palm Sunday procession antiphons from the 1861 witness; its other negative Holy Week results remain measured, not assumed. | 1962 translation sidecar's `verification`, sixth pass and 2026-08-27 correction; further work is a source acquisition or an exact per-text collation, not a cross-recension inference |
| Three commemorations whose Latin the index reprints from a Common instead of referencing it, and whose English is therefore recorded twice | the three rows' own `harvest_note`; the fix is a `takes_from` and belongs to the lane owning `propers.yaml` |

Adding to an `open_collation_items` list is the correct move when you find a
divergence you cannot collate. Silently normalizing it is not.

The former Sequence-acquisition item is closed. The registered London first
printing of Edward Caswall's *Lyra Catholica* (James Burns, 1849; Internet
Archive `LyraCatholica1849`) contains all five Sequence translations, including
the *Dies irae* at printed pp. 241–244, leaves n278–n281. The previously cited
item `lyracatholicaco00caswgoog` is a New York 1851 reprint, not the London
1849 edition. Their Google matter was also formerly reversed here: the London
text layer has 311 page-foot stamp occurrences and no Google front block; the
New York text layer has a contiguous head block and no page-foot stamps. The
active 1962 overlay records Caswall as the through-line across all five and the
Irons *Dies irae* as an alternative voice, not as coverage of a Caswall gap.
