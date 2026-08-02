# Pre-1955 precedence: a proposal, and an argument that most of it is unnecessary

**Status: proposal. Nothing here has been accepted, and nothing here has been built.** No code, schema or data file was changed in writing it. [`../recensions.md`](../recensions.md) §9.7 says the change it sketches "should be argued before it is written"; this file is that argument, and it reaches a different conclusion from the sketch. The decision belongs to a human reader, and the sections are ordered so that a reader who disagrees with the reasoning can find the disagreement rather than the conclusion.

It concerns one question only: **what would have to change in this repository before `src/sources/calendars/roman-pre-1955/` could carry a `rubrics.yaml` and be offered in the missal selector.** It does not propose a pre-1955 `rubrics.yaml`, it does not decide any day, and it is not an authority for what was celebrated anywhere. [`calendar-computation.md`](calendar-computation.md) owns the arithmetic, [`../web-data.md`](../web-data.md) owns the emitted layer, and [`../recensions.md`](../recensions.md) owns Rules 1–8. Where this file disagrees with §9.7 of that document it says so in terms, and it does not edit it.

**The headline, stated first so it cannot be reached by accident.** The extension §9.7 sketches — "an ordered criteria list as a second kind of precedence" — is, as sketched, **provably unnecessary**: a list of criteria taken in order over per-day attributes is a total preorder, and every total preorder is already expressible as numbered rows. If that were the whole of the pre-1955 rule, flattening would be honest and the schema would need nothing. It is not the whole of the rule, and the part that resists is **not** criterion (e), which is the reason §9.7 gives and which cannot bite in this layer at all. It is the pairwise guard in criterion (a), read with Titulus III, which admits a three-way cycle that no row numbering can reproduce. Whether that cycle is *reachable* in the calendar this repository actually serves is an empirical question that no one here has answered, and it is answerable by reading a book already located, already public domain, and already on the wanted list. **The recommendation is therefore to defer the schema change and do that reading first.**

---

## 1. The present model, exactly

Four files, in the order a rule travels through them. Line numbers are given so that the description can be checked rather than believed; they are accurate at the commit this file was written on and will drift.

### 1.1 The source

`src/sources/calendars/<calendar>/rubrics.yaml`, beside the `propers.yaml` mass index it classifies. Two exist: `roman-1962` and `postconciliar`. `roman-pre-1955` has a `propers.yaml` and no `rubrics.yaml`, which is why the selector does not offer it.

`precedence` is a mapping carrying `stated`, `locus`, and `rows`: a list of `{row, class, label}` entries, numbered from 1, in which **a lower number wins**. The 1962 file carries twenty-eight rows under RG 91; the postconciliar file carries thirteen under the Table of Liturgical Days. The 1962 file's own gloss records why the numbers are learned as numbers and not merely as an order — later rubrics of the 1960 code cite them as addresses.

`bases` is a list of the reasons a day carries the row it carries. Each basis has an `id`, a `label`, a `why`, a `locus`, usually a `row`, and optionally `class`, `nature`, `commemoration`, `optional`, `competes`, `de_tempore`, `constitutes_the_day`. `assignment` is an ordered list of predicate rules mapping each mass in the index to exactly one basis — first match wins, and an unmatched mass is a hard failure rather than a silent default.

Three further mechanisms are worth distinguishing, because they are easy to run together:

- **`assignment`** maps a mass that exists in the index to a basis, and therefore to a row.
- **`implied`** constitutes a liturgical day the index carries no formulary for — a feria, an octave day — so that it can compete at all.
- **`appointed_across`** states that one text is appointed over a span of days. It is **not** part of precedence and is not read by `calendar-rubrics` at all: it is absent from both `REQUIRED_TOP` and `EMITTED` in that tool, and is read instead by `_calendars.spans_of` (`scripts/_calendars.py:585-614`) and checked by `span_problems` in `check-calendar-masses`. It landed in `rubrics.yaml` because that is the file that states rules once per calendar, not because it bears on ranking. Nothing in this proposal touches it.

### 1.2 The validator

`tools/calendar-rubrics`. Two functions carry the whole of the present model's shape:

| Function | Lines | What it actually enforces |
| --- | ---: | --- |
| `check_precedence` | 326–340 | `precedence.stated` is truthy, with the message *"this file exists to state it"*; `precedence.locus` is non-empty; the `row` values of `rows` equal `1..N` in order; every row carries a `label`. |
| `check_bases` | 343–374 | Every basis has a unique `id`, a `why` and a `label`. A basis with `row: null` must declare `competes: false` (or `nature: commemoration`). A basis with a row must name **a row the table has**, and must carry a `locus`. |

Two details matter to anything built on top of them, and neither is obvious from the description:

- **`check_precedence` does not require a non-empty table.** `rows = table.get("rows") or []` and the comparison against `range(1, len(rows) + 1)` both succeed on an empty list. A source with `rows: []` passes `check_precedence`; it fails later, in `check_bases`, because every competing basis names a row the table does not have. The guard against a table-less source is in the second function, not the first.
- **`check_bases` reads `document["precedence"]["rows"]` unguarded** (line 345), so a source omitting the key entirely raises `KeyError` out of the reader rather than returning a problem. `REQUIRED_TOP` (165–181) requires `precedence`, not `precedence.rows`.

`build` (889–925) runs the checks per calendar and hands `document_for` (585–616) the emitted copy, in which basis ids are resolved to positions. `run_check` (948 onward) additionally verifies that the written `src/web/data/structure/rubrics/*.json` is what the source would write now, and then replays every solved case against the browser's model under node. A missing model, a missing `node`, and **a set of sources yielding no solved case at all** are hard failures with no opt-out (984–1008): "a gate that cannot run is not a gate that passed."

### 1.3 The derivation

`src/web/browser/liturgy/assembly-model.js`, which owns the derivation and is the only implementation of it in the repository. The relevant parts:

- `competes` (505–507): a candidate competes if its basis does not declare `competes: false` **and `one.row != null`**. A row is what standing consists of.
- `rank` (509–593). Overrides run first (534–557) and defeat candidates the row numbers alone would have made winners: `yields_to` matches another candidate's `basis.nature`, `over_key_matches` a mass key regex, both anchored on `override.key`, which is **a mass key and not a basis id**. Then the comparison:

      let best = standing[0];
      for (const one of standing) if (one.row < best.row) best = one;
      const tied = standing.filter((one) => one.row === best.row);

  A tie among bases all marked `optional` becomes a choice for the celebrant; any other tie is a gap, and the derivation stops and says which rule would settle it.
- `placeWord` (595–597) prints "row" for `roman-1962` and "place" for everything else — the vocabulary is already per-calendar.
- The row is read in six further places: the loser ordering for commemorations (788–791, `row == null` sorts last), `classOfRow` (655–662) as the fallback when a basis states no `class`, the commemoration ceilings (814, 867–869), `rowLabel`, and the emitted result (1173–1175 for each candidate, 1207–1209 for the winner). `day.js:473` prints the winner's place, guarded by `branch.winner.row != null`.

### 1.4 What holds it together

Twenty-eight solved cases — sixteen in `roman-1962`, twelve in `postconciliar` — are replayed against that model on every `calendar-rubrics check`. **Twenty-six of the twenty-eight assert `winner_row`.** A case may assert only fields the tool enumerates in `EXPECTATIONS` (711–735), so a misspelled field is an error rather than a field nobody checks, and every run reports which fields no case asserts.

---

## 2. The pre-1955 rule, exactly

### 2.1 The text was reached, and this file quotes it

`src/sources/inventories/pre-1955-rubrics-sources-v1.toml` records the rule at *Acta Apostolicae Sedis* 3 (1911) 641–642, in `AAS-03-1911-ocr.pdf`, sha256 `590a78b6…f7c`, 3 418 093 bytes, fetched from vatican.va. **Writing this file, that PDF was fetched again from the same URL; the bytes are 3 418 093 and the sha256 is `590a78b670da67f013ea6fc0b62bb7ed347dc89a9267fbb7ddc0380f1e872f7c`, identical to the recorded digest.** The Latin below is `pdftotext` output from those bytes, at the recorded position. It is a 1911 Holy See publication, `public-domain-us-pre-1931`, and the inventory records `may_publish_text = "yes"` — which, as that record observes, is a stronger rights position than the 1960 code governing the calendar beside it holds.

Two cautions on the transcription. It is an OCR text layer, and the same volume's OCR elsewhere shows the usual damage (`eStumque` for *eorumque* in the Titulus III heading, `Duplici I autì II classis` in IV.2). The passages quoted below are clean, but a `rubrics.yaml` built on them should be read against page images, exactly as `guidance/recensions.md` §8 requires of the pre-1955 orations, where 38 of 99 OCR readings were wrong.

### 2.2 Titulus II, *De Festorum praestantia*

> 1. *Ut recte dignoscatur quale ex pluribus Officiis sit praestantius et proinde sive in occurrentia, sive in concurrentia, sive in ordine repositionis aut translationis praeferendum, sequentes praestantiae characteres considerandi sunt:*
>
> *a) Ritus altior, nisi occurrat Dominica, vel Feria, vel Octava privilegiata, vel etiam quaelibet dies Octava iuxta Rubricas.*
> *b) Ratio Primarii aut Secundarii.*
> *c) Dignitas Personalis, hoc ordine servato: Festa Domini, B. Mariae Virginis, Angelorum, S. Ioannis Baptistae, S. Ioseph, SS. Apostolorum et Evangelistarum.*
> *d) Sollemnitas externa, scilicet si Festum sit feriatum, aut celebretur cum Octava.*
>
> 2. *In occurrentia, et in ordine repositionis aut translationis, alius quoque character considerandus est, nempe:*
>
> *e) Proprietas Festorum. Dicitur Festum alicuius loci proprium, si agatur de Titulo Ecclesiae, de loci Patrono etiam secundario, de Sancto … cuius habetur corpus vel aliqua insignis et authentica reliquia, vel de Sancto, qui cum Ecclesia, vel loco, vel personarum coetu specialem habeat rationem. Igitur Festum quodvis istiusmodi proprium, ceteris paribus, praefertur Festo Universalis Ecclesiae. Excipiuntur tamen Dominicae, Feriae, Octavae et Vigiliae privilegiatae, nec non Festa primaria Duplicia I classis Universalis Ecclesiae, quae uniuscuiusque loci propria considerantur et sunt. Festum autem Universalis Ecclesiae, cuiusvis ritus, quia est praeceptivum, ceteris paribus, praeferri debet Festis aliquibus locis ex mero Indulto S. Sedis concessis, quae tamen propria, sensu quo supra, dici nequeunt.*

The inventory's summary of this is accurate. Two things the full text adds are load-bearing below, and neither is in the summary:

- **(e) is an *additional* character in occurrence and translation, not a character *withdrawn* from concurrence.** n. 2's construction is *alius quoque character considerandus est*. The effect is what the inventory records — four characters in concurrence, five in occurrence and translation — but the direction matters when one asks what a schema must express: the questions do not carry different orderings of the same criteria, they carry different-length prefixes of one list.
- **(e) ranks a feast proper *to a place* above a feast of the universal Church, and a universal feast above an indulted one.** Its whole subject matter is the particular calendar: title of the church, patron of the place, a saint whose body or notable relic is held, a saint with a special relation to the church, place or community.

### 2.3 What Titulus II does not decide, and where the rest is

Criterion (a) does not resolve the cases it excepts. Its guard — *nisi occurrat Dominica, vel Feria, vel Octava privilegiata, vel etiam quaelibet dies Octava* — sets the rite comparison aside without saying who then wins. That answer is in the following titles, in the same publishable pages:

- **Titulus III**, *De Festorum occurrentia accidentali eorumque translatione*, nn. 1–6: major Sundays of the first class always keep the Office; Sundays of the second class yield only to *Duplicia I classis*; minor Sundays always keep the Office *nisi occurrat Festum quodcumque Domini, aut aliquod Duplex I vel II classis, aut dies Octava Festorum Domini*; *Duplicia I et II classis* impeded are transferred to the nearest following free day; *Duplicia maiora* and *Duplicia minora Doctorum* are no longer transferred but commemorated; 2 November excludes any transfer.
- **Titulus IV**, *De Festorum occurrentia perpetua eorumque repositione*, nn. 1–4: perpetual impediment and reposition, with major Sundays excluding perpetual assignment of any feast whatever.
- **Titulus V**, *De concurrentia Festorum*, nn. 1–3 — Vespers only.
- **Titulus VI**, *De Commemorationibus*, whose n. 3 prints an **ordered list of eleven classes** for the order of commemorations. That list is flat, printed, and numbered, and would go into the existing `commemoration.order` block unchanged. It is worth noticing that the same title that resists flattening for precedence flattens without argument for commemoration.

So the pre-1955 occurrence rule is not one text but three read together — Titulus II for the general characters, Titulus III and IV for the cases Titulus II excepts. The books of the period do not ask their users to do that: as the inventory's located rows record, the Breviaries print a **`Tabella occurrentiae`** and a **`Tabella concurrentiae`** — two grids, one per question, with *notanda*. The 1960 code replaced all of it with one numbered table and the phrase *sublatis quibuslibet aliis titulis vel normis*.

**That contrast is the real subject of this proposal.** The 1911 rule's own books express it as a matrix of pairs. The 1960 code's book expresses it as a linear list. `rubrics.yaml` models the second.

---

## 3. Where it does not fit — and where it does

### 3.1 Criterion (e) is not the obstacle, for two independent reasons

`guidance/recensions.md` §9.7 states the failure this way: "A row number is one order for all questions. Criterion (e) makes the same two days rank differently in occurrence than in concurrence, so no single number can carry the pre-1955 answer." The premise is true of the rule. **It is inert against this layer, twice over.**

**First: this layer never asks the concurrence question.** Concurrence disposes of Vespers. `roman-1962/rubrics.yaml` carries it under `precedence.concurrence` with `decides_the_mass: false` and the gloss "Concurrence is the meeting of one evening's Vespers, not of two days. It never decides which Mass is said the next morning", and lists it again in `not_decided_here`: "Concurrence, which disposes of Vespers and never of the next morning's Mass (RG 103-105)." The postconciliar source says the same of NUALC 61: "It is stated for the Office and has no Mass analogue." Nothing in `assembly-model.js` computes a Vespers. A pre-1955 source would declare the same thing about Titulus V and be as true as its two siblings. The remaining questions this layer *does* decide — occurrence, and transfer/reposition — take **the same five characters in the same order**, by n. 2's own words. One order suffices for everything asked.

**Second: (e) has no values to distinguish in the calendar this repository serves.** Its subject is the feast proper to a place, against the feast of the universal Church, against the indulted feast. This repository decides no particular calendar: `roman-1962/rubrics.yaml`'s `not_decided_here` opens with "Which calendar binds the celebrant (RGMR 274-284), and every particular, diocesan, religious, patronal, titular and dedication feast that calendar carries. Rows 12, 13, 19, 20 and 23 of the table are therefore **always empty here**." `roman-pre-1955/propers.yaml` is a departure record over `roman-1962` and inherits that scope. In a universal-calendar-only slice, every competitor is *Festum Universalis Ecclesiae*: criterion (e) takes one value across the whole field, and a criterion with one value orders nothing.

Either reason alone disposes of the argument. **§9.7's stated reason for the schema change does not hold against the tool as it exists, and this file's first recommendation is that the sentence be corrected whether or not anything else here is accepted.**

### 3.2 The sketched extension would not fix what does break

§9.7 proposes admitting "an ordered criteria list as a second kind of precedence". Consider what that buys. If each criterion is a function of one day's own attributes, and the criteria are taken in order until one separates two days, the result is **lexicographic order on a tuple** — which is a total preorder. Every total preorder over a finite set of bases can be written as row numbers: enumerate the distinct tuples the calendar actually exhibits, sort them lexicographically, number them `1..N`, and give each basis the number of its tuple. `check_precedence` requires exactly `1..N` in order and would accept the result; `check_bases` would accept each basis naming one; `assembly-model.js` would compare them correctly with the fold it already has.

**A criteria list, evaluated as a tuple comparison, is therefore expressible in today's schema with no change whatever.** As a second kind of precedence it is not a second kind of anything: it is the same order, written in a form that has to be compiled back into rows before it can be compared. The only thing it adds is provenance — the file would show *why* row 14 sits above row 15 — and provenance can be had far more cheaply (§4.3).

### 3.3 What does break: the guard in (a), and a cycle

The criteria are not pure functions of one day. Criterion (a) carries a **pairwise guard**: the higher rite prevails *unless the other party is a Sunday, a feria, a privileged octave or any octave day*. In that case the rite comparison is set aside and Titulus III decides. A guarded comparison is a property of a pair, not of a day, and a relation defined pairwise need not be transitive.

It is not. Three sentences of the rule, taken together:

| Pair | Winner | Authority |
| --- | --- | --- |
| A feast of the Lord at *Duplex minus* vs a minor Sunday | the feast | Tit. III n. 2: the Sunday keeps the Office *nisi occurrat Festum quodcumque Domini* — any feast of the Lord, no rite qualification |
| A minor Sunday vs a *Duplex maius* of a saint | the Sunday | Tit. III n. 5: on minor Sundays likewise the Office is of the Sunday, *nisi … Festum quodcumque Domini, aut quodvis Duplex I vel II classis, aut dies Octava Festorum Domini* — and a *Duplex maius* of a saint is none of those |
| A *Duplex maius* of a saint vs a feast of the Lord at *Duplex minus* | the *Duplex maius* | Tit. II (a): *ritus altior*, and the guard does not apply, since neither party is a Sunday, feria or octave |

Write `r(X)` for a row number. The three facts require `r(DuplexMinus Domini) < r(Dominica minor)`, `r(Dominica minor) < r(Duplex maius sancti)`, and `r(Duplex maius sancti) < r(DuplexMinus Domini)`. Adding them gives a contradiction. **No assignment of row numbers to those three bases satisfies all three pairs**, and this holds however finely the bases are subdivided — giving feasts of the Lord their own bases, which is the obvious repair, is already assumed in the statement.

Note what this costs, because it is worse than it first looks. The cycle does not need three candidates on one date to do damage. **A flattened table gets at least one of those three *pairs* wrong, and every one of those pairs is an ordinary two-candidate day.** The wrong answer would be delivered by a file that validates, resolves, and cannot be told from a right one downstream — which is the failure Rule 8 exists to prevent, committed in the file written to prevent it.

Note also that a *fold* over an intransitive relation is order-dependent: `for (const one of standing) if (one.row < best.row) best = one` returns whichever element the iteration order favours. A comparison built on such a relation cannot be a running minimum; it must compute the undefeated set and refuse when that set is empty or larger than one.

### 3.4 The honest state of the cycle: unverified reachability

**The cycle is a property of the rule text. Whether it is reachable in the calendar this repository serves is unknown, and nobody here has checked.** It requires a feast *of the Lord* at *Duplex minus* rite (or lower) in the served calendar. In the pre-1955 universal calendar, feasts of the Lord tend to be high rite — the Circumcision, the Holy Name, the Epiphany, the Finding and the Exaltation of the Cross, the Transfiguration, the Sacred Heart, the Precious Blood, Christ the King — while the lower-rite feasts of the Lord (the Holy Lance and Nails, the Holy Shroud, the Prayer in the Garden) are largely *pro aliquibus locis*, and this repository decides no particular calendar. **It is entirely possible that the triple is vacuous over the days this layer would ever rank.** It is equally possible that the same construction recurs through the *feria* and *octave day* limbs of the guard, which have not been worked through here at all.

That question is answerable, and answering it is cheaper than any code proposed below. It is already on the record as a want: `pre-1955-kalendarium-read-as-data`, priority 3 in the sourcing inventory — "A pre-1955 general calendar, read from a pre-1955 book, as a list of days with their grades and their octaves and vigils." With it, and with the `Tabella occurrentiae` read from page images of `breviarium-romanum-1922-mame` or `breviarium-romanum-1927-pustet` — both located, both `public-domain-us-pre-1931`, both `may_publish_text = "yes"` — the question becomes arithmetic: **compute whether the grid the books print is a linear order.** If it is, flatten. If it is not, the exceptions the grid records *are* the specification of the extension.

One warning belongs here, because it is the cheapest way to waste the reading: the inventory records that **the grids do not survive OCR** and must be read from page images — "any lane that takes the grid from the text layer will be transcribing noise, and the noise will look like data."

---

## 4. The proposal

Three designs, in increasing cost. The recommendation is §4.3 and then §4.1, with §4.2 held in reserve.

### 4.1 Preferred if the reading permits: rows, plus pairwise exceptions targeted at a basis

The repository already has a pairwise-exception mechanism, invented for exactly this problem: `overrides`, whose first entry is `all-souls-yields-to-a-sunday` — a row-8 day defeated by a row-15 one, because RG 91's own row says *quae tamen locum cedit dominicae occurrenti*. That is a table getting a pair wrong and a named rule fixing it.

Every carve-out in Titulus III and IV has that shape. So: order the rows by rite (with Sundays, ferias, octaves and vigils placed where Titulus III puts them), and express each carve-out as one override citing one numbered rubric. In the worked triple, rows ordered `Duplex maius sancti` above `Dominica minor` above `Duplex minus Domini` satisfy two pairs, and one override — *a minor Sunday yields to any feast of the Lord*, Tit. III n. 2 — satisfies the third.

One change is needed, and it is small: **`overrides` must be able to target a basis, not only a mass key.** `rank` today finds its target with `contest.find((one) => one.key === override.key)`, so "minor Sundays yield to any feast of the Lord" would need one override per Sunday in the calendar. Adding an optional `basis:` beside `key:` — with `check_bases` requiring that it name a declared basis, exactly as it requires a row to name a declared row — makes the rule statable once. `yields_to` already matches on `basis.nature` and needs nothing.

Why this is preferable: it adds one field and no second comparison; the rules stay legible one-to-one against the numbered rubrics they come from; the two served calendars are untouched; and where the overrides cannot express a case, the model already fails closed — an override cycle defeats every candidate, `standing.length` is zero, and the day is reported unsettled instead of decided.

Its honest weakness is that a table so built has **row numbers no book prints**. §4.3 is the answer to that, and is required whether or not §4.1 is adopted.

### 4.2 If the reading forbids §4.1: a pairwise comparator, not a criteria list

If the grid turns out to be genuinely irreducible — many exceptions, or exceptions whose conditions are not expressible as "basis X yields to nature Y" — then the extension is warranted, and it is **not** the one §9.7 sketches. It is a pairwise comparator.

Concretely, in the source:

```yaml
precedence:
  stated: true
  kind: criteria            # new; absent means `rows`, so both served files are unchanged
  locus: AAS 3 (1911) 641-642, Titulus II, De Festorum praestantia
  decides: [occurrence, translation]     # and NOT concurrence
  criteria:
  - order: 1
    id: ritus-altior
    values: [duplex-i-classis, duplex-ii-classis, duplex-maius, duplex-minus,
             semiduplex, simplex]        # best first; the ordinal is the value
    unless_other_is: [sunday, feria, privileged-octave, octave-day]
    then: defer              # this criterion abstains for that pair
    locus: AAS 3 (1911) 641, Tit. II n. 1 a
  - order: 5
    id: proprietas-festorum
    applies_in: [occurrence, translation]
    inert_here: true
    inert_because: >-
      its values distinguish the feast proper to a place from the feast of the
      universal Church, and this file decides no particular calendar.
```

and in each competing basis a `characters:` mapping giving one declared value per criterion, in place of `row:`.

What `check_precedence` must then require: exactly one of `rows` and `criteria`; `order` running `1..N`; a `label`, a `locus` and a non-empty ordered `values` list per criterion; `applies_in` drawn from a closed vocabulary `{occurrence, concurrence, translation}`; a `decides` list, with a criterion that applies only to questions the file does not decide required to say so (`inert_here` with `inert_because`, on the model of `stated_only` in `overrides` and `open_because` in `mass_choices` — this repository's existing idiom for a rule recorded and deliberately not applied). Its current tolerance of `rows: []` and its unguarded read of `precedence.rows` in `check_bases` both have to be closed, or a criteria source will crash the reader rather than fail the check.

What `check_bases` must then require: for a criteria source, every competing basis carries a complete `characters` block — exactly the declared criterion ids, each with a value drawn from that criterion's `values`. That is the precise analogue of today's "names a row the table has", and it must be complete rather than partial, because a missing character is a silent tie. A basis carrying both `row` and `characters` is an error. `row: null` ⇒ `competes: false` survives unchanged as `characters: null` ⇒ `competes: false`.

What the winner comparison becomes. `competes` (505–507) tests `one.row != null`; it becomes `one.row != null || one.characters != null`. `rank` (562–564) stops folding:

      // rows: beats(a,b) === a.row < b.row.  criteria: take the criteria in
      // order, skipping any that defers for this pair or does not apply to the
      // question asked, until one separates them.
      const undefeated = standing.filter((one) =>
        !standing.some((other) => other !== one && beats(rubrics, other, one)));
      if (undefeated.length !== 1) -> unsettled, naming the cycle or the tie

For a rows calendar `beats` is `a.row < b.row` and `undefeated` is exactly today's answer, so the two served calendars derive identically. The other six row-readers need a `placeOf`/`placeLabel` abstraction: the loser sort (788–791) needs a total order, and a comparator that may cycle cannot supply one — the honest fallback is to sort by the first criterion alone and say so. `class` must come from the basis's own `class` field rather than `classOfRow`, which a criteria calendar cannot answer.

Tool-side, `EXPECTATIONS` gains a key so a pre-1955 solved case can assert a winner's standing (`winner_characters`, say) where a 1962 case asserts `winner_row`.

**This is the design the evidence would support if the reading goes the other way, and I am not confident it is complete.** The parts I am least sure of: whether `then: defer` is the right semantics for (a)'s guard, or whether the guard should instead be modelled as a rule *promoting* Titulus III into the comparison; how the disposition of the loser (translate, repose, commemorate, omit) is keyed, since the pre-1955 disposition depends on the *pair* — a *Duplex I classis* is transferred, a *Duplex maius* is commemorated — where the existing `impediment` and `commemoration` blocks key on the loser alone; and whether the *feria* and *octave day* limbs of the guard generate cycles of their own.

### 4.3 Required in either case: a derived table must declare itself derived

The 1962 rows are transcribed: RG 91 prints them, numbered, and later rubrics cite the numbers as addresses. The postconciliar places are likewise printed. **A pre-1955 table would be neither.** Its ordering would be this repository's reading of Titulus II with Titulus III and IV, and its numbers would exist nowhere in any book. `check_bases` requires each row-carrying basis to name a `locus`, and today that requirement is satisfied by a citation; a derived table would satisfy it with a citation to the criteria the row was *derived from*, which is a materially weaker claim wearing the same field name.

So: `precedence` should be able to say which it is — `transcribed: true` for a printed table, or `derived_from_criteria:` naming the criteria and the loci they were read at, plus, if §4.1 is adopted, a `criteria:` block recorded **for the record and not applied**, including the criteria that are inert and why. This costs one field and one check, it is independent of everything else here, and it is what makes a flattened table honest rather than merely convenient. Without it, a reader of `roman-pre-1955.json` cannot tell a row that the Holy See numbered from a row this repository numbered — and that is the distinction the whole of §9.7 was reaching for.

---

## 5. The alternatives, and why they lose

### (a) Flatten the five criteria into synthetic row numbers

**This is the alternative that has to be taken most seriously, because on the evidence assembled here it may well win, and §3.2 shows that a straight criteria list would be nothing else.**

The occurrence/concurrence asymmetry of criterion (e) **survives flattening**, in the strict sense that it never arises: this layer does not decide concurrence, and (e) has one value across the calendar it does serve (§3.1). If that were the only obstacle, flattening would be honest and this proposal should be rejected in full — which, as the brief that commissioned it observed, would be the most valuable outcome available. The record should say so plainly: **the reason §9.7 gives for the extension does not survive contact with the tool.**

What defeats *naive* flattening is not (e) but §3.3: the guard in (a) admits a three-way cycle, and a linear table must decide at least one ordinary two-candidate pair wrongly, silently, in the file written to prevent exactly that. What defeats *disciplined* flattening is nothing yet — because §4.1 is disciplined flattening, with the pairwise exceptions written down as overrides citing Titulus III, and §4.3 making the derivation visible. That is the recommendation.

So the verdict on (a) is conditional and should not be rounded off: **flattening loses if it is done by numbering the criteria tuples and calling the result a table; it wins if the carve-outs are written as pairwise exceptions and the table declares itself derived — and whether even that suffices depends on a reading nobody has done.**

### (b) A separate comparison path per recension

Lose, and the reasons are already written down elsewhere in this repository. `calendar-rubrics` states as one of the three things it refuses: "It does not check the derivation in a second implementation… A Python re-implementation would drift from the page it is meant to hold." `web-data.md` says the derivation "lives in `src/web/browser/liturgy/assembly-model.js` and exists once". A second comparison path is that defect with a different justification: two ways to resolve a day, in the layer whose whole job is deciding which day wins, with nothing comparing them. It is also unnecessary — §4.2's comparator is one function whose rows branch is the present behaviour exactly, which is a strictly better way to get the same expressiveness. The one honest version of (b) is that the *pre-1955 rule* is a different rule and deserves its own **source**; it already gets one. The derivation is not the rule.

### (c) Leave the calendar unoffered permanently

Lose, but it is the option to fall back to if the reading in §3.4 is not done, and it is not shameful. Rule 6 says "a recension is offered to a reader only where it can be served", which is a condition and not a prohibition; Rule 8 says the schema is extended *before* the source is written, which presumes the extension eventually happens. Permanence would have to rest on a claim nobody has established — that the rule cannot be stated in any schema — and the evidence points the other way: the books of the period stated it, in two printed grids, and the inventory has located two public-domain witnesses to those grids. **Leaving it unoffered while the grid is unread is the correct present state and is exactly what Rule 6 already produces.** Leaving it unoffered after reading the grid, without a reason from the grid, would be Rule 6 used as an excuse rather than a rule.

There is also a cost to (c) worth stating, because §9.7 does not: the pre-1955 calendar already serves 490 masses and resolves 316 of the 365 days of 2026 through this repository's tooling, and its propers and year files are already written to `src/web/data`. The only thing standing between it and the selector is `structure/rubrics/index.json`, which lists what has rules. This is not a recension awaiting acquisition; it is one awaiting a decision about a comparison.

---

## 6. Blast radius

**Schema and validator.** `tools/calendar-rubrics`: `check_precedence` and `check_bases` under §4.2 or §4.3; a new field admitted in `overrides` under §4.1. `EXPECTATIONS` gains a key only under §4.2. The captured example transcripts in `EXAMPLES` carry live counts — "roman-1962: 460 masses classified over 28 bases and 28 rows", "solved cases: 28 of 28 verified", "asserting 6 of 19 fields the model returns" — and `tools/tests/test_example_replay.py` replays them, so **a third calendar, or a nineteenth expectation, makes those transcripts stale and they must be recaptured, not edited.**

**The browser.** `assembly-model.js`: `competes` (505), `rank` (509–593), the loser sort (788–791), `classOfRow` (655), the ceilings (814, 867–869), the emitted candidate and winner rows (1173–1175, 1207–1209). `day.js:473` already guards on `winner.row != null` and would need the criteria vocabulary in `placeWord`'s neighbourhood. **Under §4.1 none of this changes at all** beyond the override target.

**Can the browser's model change without breaking the two served calendars?** Yes, on one condition: the rows branch must be the present code path and not a re-expression of it. `beats(a, b) === a.row < b.row` folded to the undefeated set returns exactly what the running minimum returns whenever the relation is a total order, which it is for both served calendars, so the twenty-eight solved cases are the proof and not merely a hope. If the rewrite instead re-derives rows through a general comparator, the two calendars are at risk and the risk is invisible — the cases would still pass while the reasoning changed underneath them.

**The 28 solved cases.** None needs a new assertion. Twenty-six of the twenty-eight assert `winner_row`, which continues to mean what it means for a rows calendar; the other two assert other fields. What is required is **new cases for pre-1955** — `run_check` treats a source exercising no case as a hard failure, and by the two existing sources' standard that means twelve to sixteen. They can be written today: `src/web/data/structure/calendar/roman-pre-1955/` and `structure/propers/roman-pre-1955.json` already exist, so the year files a case needs are in place. Each case must be worked from a book and not from the model.

**Tracked data.** `src/web/data/structure/rubrics/index.json`, `roman-1962.json` and `postconciliar.json` are tracked; a `roman-pre-1955.json` joins them and the index gains a row, which is what puts the missal in the selector. Per the standing directive, these are regenerated through the Make targets and the release hashes are never hand-edited.

**Tests that would have to move, and one that would not.** `tools/tests/test_recensions.py` asserts `test_it_ships_no_rubrics_source_so_the_selector_cannot_offer_it` — that `roman-pre-1955/rubrics.yaml` does not exist — and `test_the_headline_stays_honest_while_no_rubrics_source_ships`, which ties `rubrics_sources_this_record_makes_writable` in the sourcing inventory to that file's existence. Both are working as designed: they are the tripwires that make landing a pre-1955 source a deliberate act, and both must be rewritten in the same commit that lands it, along with the inventory count moving 0 → 1. `tools/tests/test_calendar_rubrics.py::test_every_basis_names_a_row_the_table_carries_or_declines_to_compete` iterates a **hard-coded** `("roman-1962", "postconciliar")`; a third calendar joins the emitted layer without joining that test, which is worth fixing whichever design is chosen.

**Documents.** `guidance/recensions.md` §9.7 and Rule 8's illustration; `guidance/web-data.md`'s rubrics-layer section, which currently describes bases as assigning "each mass to a row"; `src/sources/calendars/README.md`; and `src/sources/inventories/pre-1955-rubrics-sources-v1.toml`, whose finding `the-rule-is-criteria-not-rows` states the (e) reasoning this file disputes. **None of them is edited by this file, which owns only itself.**

---

## 7. What would have to be true for this proposal to be wrong

Stated as checks a reader can run, not as hedges.

1. **If this layer does decide, or comes to decide, concurrence.** The whole of §3.1's first reason rests on `decides_the_mass: false` and on `not_decided_here`. An Office layer — Vespers, first and second — would make Titulus V live, criterion (e) would then genuinely apply to one question and not the other, and §9.7's reasoning would become correct as written. Nothing in this file argues that the Office should not be built; it argues about what the Mass layer needs today.
2. **If this layer comes to decide a particular calendar.** Then criterion (e) acquires values, proper and indulted feasts enter the field, and its ranking becomes live in occurrence and translation. Even then it would apply to every question this layer asks and would not by itself require a second kind of precedence — but §3.1's second reason would fall, and a flattened table would have to carry (e) explicitly.
3. **If the cycle in §3.3 is a misreading.** The three sentences were read from an OCR text layer, and the argument turns on *Festum quodcumque Domini* in Titulus III n. 2 covering feasts of the Lord at any rite, including *Duplex minus*. If the printed page reads otherwise, or if a *notandum* in the Breviary tables restricts it, the cycle dissolves and §4.1 collapses into plain flattening — which would be a better outcome, not a worse one.
4. **If the `Tabella occurrentiae` is a linear order.** Then the tradition's own answer is a table, the 1960 code merely renumbered it, and §4.1's overrides may not even be needed. This is the single most informative thing anyone could learn about this question and it costs one reading of one public-domain book.
5. **If the cycle is real and reachable in the served calendar.** Then §4.1 is insufficient wherever the overrides run out, §4.2 is required, and the parts of §4.2 flagged as uncertain — loser disposition keyed on the pair, the semantics of the guard — become the hard part rather than the comparison.
6. **If the exceptions turn out to be many rather than few.** §4.1 rests on the carve-outs being a short list of citable sentences. A table needing forty overrides is a matrix pretending to be a list, and the pretence would be worse than §4.2's honesty.
7. **If a pre-1955 `rubrics.yaml` cannot be sourced to the standard the other two meet.** Both existing sources transcribe from a collated in-repository publication with an evidence class per rule. No such publication exists for the pre-1955 rubrics. That is a real gap, it is not addressed anywhere above, and it may be the binding constraint long after the schema question is settled.

---

## 8. If this is accepted, the order of work

Nothing in 1–2 changes any file under `src/`, and either may return an answer that cancels 3–5.

1. Read the `Tabella occurrentiae` and its *notanda* **from page images** of `breviarium-romanum-1922-mame` or `breviarium-romanum-1927-pustet`, and record whether it is a linear order. Not from the OCR text layer.
2. Obtain `pre-1955-kalendarium-read-as-data` and determine whether the §3.3 triple, and any sibling triple through the feria and octave limbs, is reachable in the universal calendar this repository serves.
3. Correct `guidance/recensions.md` §9.7 and the inventory finding `the-rule-is-criteria-not-rows` to the reason the evidence supports, whatever that turns out to be. Do this whether or not any code follows; the present reason is stated with more confidence than it can carry.
4. Adopt §4.3 — the derived-table declaration — since it is required under every design and is independent of the reading.
5. Then, and only then, §4.1 or §4.2, with the pre-1955 solved cases worked from a book first and the model run against them second.
