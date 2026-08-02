# Registering a movable commemoration: a proposal, and an argument that no schema change is needed

**Status: proposal. Nothing here has been accepted, and nothing here has been built.** No code, schema or data file was changed in writing it. Its subject is the two rulings that `src/sources/calendars/roman-1962/propers.yaml` records in its own `open_collation_items` as blocking the *Commemoratio septem Dolorum B. Mariae Virg.* of the Friday after Passion Sunday, and with it the fifth and last of the 1962 Sequences, *Stabat Mater dolorosa*. The decision belongs to a human reader, and the sections are ordered so that a reader who disagrees with the reasoning can find the disagreement rather than the conclusion.

[`pre-1955-precedence-proposal.md`](pre-1955-precedence-proposal.md) landed today and is the model for an argued proposal in this repository: it reached the conclusion that the extension it was asked to design was unnecessary, and said so first. This file reaches the same kind of conclusion by a different route, and owes that file its shape. It does not edit it, and it does not edit anything else.

It concerns one question only: **what must be settled before the Friday after Passion Sunday can carry an entry in the 1962 mass index.** It does not decide precedence, it does not transcribe a formulary, and it is not an authority for what is celebrated anywhere. [`calendar-computation.md`](calendar-computation.md) owns the arithmetic and [`../web-data.md`](../web-data.md) owns the emitted layer.

**The headline, stated first so it cannot be reached by accident.** Neither open question needs a schema change, and one of them is already answered inside `roman-1962/rubrics.yaml` by a worked case nobody connected to it.

1. **The registry scheme exists and has sixty-six members.** `check-calendar-masses` requires *exactly one* of `season` and `date`, and asks for a `rank` **only of a dated entry**. A movable day is therefore an ordinary undated entry with a `1962-T-<key>` id, which is what `rogation-mass`, `chrism-mass` and every feria in the file already are. The premise in the index's own note — that the commemoration model "is dated" — is true of the *sixty* commemorations unfolded from feast names and is not true of the schema.
2. **Whether a `Comm.` carrying its own printed Mass files as a commemoration or as a mass is a false alternative, and the file has already refused it once.** `mass_choices: carmel-on-a-saturday` records the Commemoration of Our Lady of Mount Carmel — a `Comm.` entry whose reason for existing is that "the Missal prints a full formulary for this commemoration, and the rubric at the day permits it to be said as the Mass." It stayed a commemoration; the permission became a `mass_choices` row. The Friday is the second instance of that shape, not a new case.
3. **The cheap route the brief proposed — the September feast plus a `takes_from` — fails, and it fails twice.** The two Masses are *not* the same text: read on the controlling facsimile today, the Collect differs in its whole middle clause, the chant after the Lesson is a Tract on the Friday and an Alleluia with three conditional substitutes in September, and the Sequence's last word differs. And even had they been identical, `takes_from` names a key in the same file, so the referring mass is still a mass with a `key` and a `registry` — the mechanism cannot dodge a registry question, only reduce how much text is copied.
4. **But the Stabat Mater can land today, by a route the brief did not consider.** The Missal prints the Sequence *twice, in full*, and the second printing is at 15 September, on an entry that already exists, is already dated, already carries a spine registry id, and carries no Sequence. Transcribing it there needs no ruling, no scheme and no reference.

**The recommendation is therefore: land the Sequence at 15 September now, and land the Friday as an undated `1962-T-` entry filed `calendar-commemoration` with a `mass_choices` row for the permitted festive Masses.** The total cost is three data edits and one line of `tools/calendar-days`. No schema field, no validator function and no browser code changes.

---

## 1. The present model, exactly

Line and function references are accurate at the commit this file was written on and will drift. Every count below was recomputed from the file itself while writing.

### 1.1 What a registry id actually is

`registry` is one of three fields `check-calendar-masses` requires of every mass (`ENTRY_REQUIRED = ("key", "name", "registry")`, line 130). The only thing checked *about* it is that it is a quoted string (456–458). There is no vocabulary, no pattern and no uniqueness check on it.

Ids come from two places and are of five shapes. The 490 masses of `roman-1962/propers.yaml` divide:

| Shape | Count | Where the id comes from |
| --- | ---: | --- |
| `01`–`52`, `46R`–`49R`, `T01`–`T03` | 59 | printed identities owned by [`roman-1962-propers.md`](roman-1962-propers.md) |
| `1962-<MM-DD>` | 275 | derived by `tools/calendar-spine`, one per civil date |
| `1962-T-<key>` | 66 | synthetic; the file's own scheme for a temporal day the registry does not number |
| `1962-<MM-DD>-comm` | 60 | synthetic; the commemorations unfolded from feast names on 2026-07-31 |
| `1962-C-<key>` | 30 | synthetic; the Commune Sanctorum |

`calendar-spine` derives its ids in one line — `entry["registry"] = f"{PREFIX[calendar]}-{entry['date']}"` (line 283) — over entries parsed from `50-sanctorale-jan-jun.tex` and `60-sanctorale-jul-dec.tex` alone (`SOURCES`, lines 89–99). **A movable day is unreachable by that derivation not because it is movable but because the spine reads only the two sanctorale sections.** The reconciliation in `check-calendar-masses` (`check_spine`, 780–820) runs one way: every spine id must be filed under a mass of the matching kind, and an index id the spine does not carry is not an error. That is what lets the other 215 synthetic ids exist at all.

### 1.2 The commemoration model, restated accurately

The index's note says "each of the 104 entries of rank `Comm.` carries a civil date and a `1962-<date>-comm` registry id". **The first half is true and the second is not.** Of the 104:

- **60** are the entries unfolded from joint names on 2026-07-31 and carry `1962-<MM-DD>-comm`.
- **44** are the commemorations the calendar reference inscribes outright. The spine already carries them as its entry for that date, so they carry a plain `1962-<MM-DD>` id and are indistinguishable in shape from a feast.

The distinction matters, because it shows the id has never encoded commemoration-ness. Rank does. The `-comm` suffix exists to disambiguate a *second* entry on a date the spine already owns, and nothing else.

### 1.3 What the schema requires of an undated entry

`check_entry` (434–478) is the whole of it:

- `key`, `name`, `registry` required; key lowercase kebab-case.
- `check_name` refuses a name folding `comm.` in after position 0 — an entry that *is* a commemoration may name itself so from its first character.
- A mass of the Commune carries neither a season nor a date; **every other mass carries exactly one of the two** (469–470).
- `check_date`, `kind` from `("christological", "marian", "sanctoral", "seasonal")`, and a printed `rank` are required **only inside `if has_date:`** (473–477).

So an undated, season-bearing entry needs no rank and no kind check. `rogation-mass` is exactly that today: `season: paschaltide`, registry `1962-T-rogation-mass`, **no `rank` field at all**, propers carrying an Introit through a Communion and a `notes` string recording that its chants are conditional by season.

### 1.4 How an undated mass is placed and ranked

Two files, neither of them schema.

- **`tools/calendar-days`** puts a key on a date arithmetically. The Passion-week ferias are one loop (`for step, name in enumerate(WEEKDAYS, start=1): year.put(passion + timedelta(days=step), f"passion-{name}", ...)`), the Chrism Mass one line, the Rogation Mass four. Placing a new movable key is one further `year.put`.
- **`tools/calendar-rubrics`** maps every mass to exactly one basis through `assignment`, first match wins, over `PREDICATE_FIELDS = ("keys", "key_matches", "dated", "kind", "rank", "season")` (212). `matches` (377–388) compares `dated` as a boolean derived from `bool(mass.get("date"))`. **A mass matching no rule is a hard failure** (412), and a rule matching nothing is also a failure (417) — so a rule cannot be written in advance of the mass it is for.

Three bases already carry `row: null`:

| Basis | `commemoration` | `competes` | What it says |
| --- | --- | --- | --- |
| `calendar-commemoration` | `ordinary` | (default) | an entry the calendar inscribes as a commemoration; it occupies no row, so it can never take the day and can only ever be commemorated |
| `additional-mass` | `none` | `false` | a further Mass appointed on a day whose identity is settled elsewhere; not a competitor |
| `alternative-formulary` | `none` | `false` | a formulary printed for a slot another day occupies |

`assembly-model.js` reads `row == null` with `commemoration != 'none'` into `standingAside` (526) and thence into the commemoration pass; `additional-mass` is *offered and not ranked*, which the `maundy-thursday` solved case asserts in terms.

### 1.5 The one rule in `assignment` that blocks the Friday

`- {basis: calendar-commemoration, dated: true, rank: Comm.}`

That is the only obstacle in the whole apparatus, and it is a **data line in `rubrics.yaml`**, not a schema. `season` is already a predicate field; so is `keys`. Widening it, or adding a sibling rule above it, is an ordinary edit of the kind that file takes every week.

---

## 2. The two open questions, precisely, and what each costs

### 2.1 "A registry scheme for a movable commemoration"

**Precisely:** what string goes in `registry` for a celebration the spine cannot derive, given that `1962-<date>-comm` presupposes a date.

**Cost to answer:** zero, if the answer is `1962-T-<key>`. That scheme is already in the file 66 times, is already declared synthetic in the file's own notes, and is already recorded there as an open collation item in its own right ("their registry ids read `1962-T-<key>` and are synthetic … settle a scheme at collation"). Adopting it for a 67th entry does not enlarge the open item; refusing to, and inventing a sixth shape, does.

The one thing it costs is a **name**: `T` was chosen for the *temporal* days, and the Seven Sorrows is printed in the Proprium Sanctorum. §5.4 argues that this is a cost worth paying and not a reason to invent a scheme.

### 2.2 "Whether a `Comm.` carrying its own printed Mass files as a commemoration or as a mass"

**Precisely:** which of the three `row: null` bases in §1.4 `assignment` should map the entry to, since a mass gets exactly one.

**Cost to answer:** zero, because the file answered it on 16 July and the answer is *commemoration*. `mass_choices: carmel-on-a-saturday` exists because the Commemoration of Our Lady of Mount Carmel — `comm-beatae-mariae-virginis-monte-carmelo`, registry `1962-07-16`, rank `Comm.` — carries a full printed formulary that the day's own rubric permits to be said as the Mass. It was not reclassified as a mass. It stayed a `Comm.` assigned to `calendar-commemoration`, and the permission was written where permissions go.

**The two rubrics are the same shape.** At 16 July: *Si Commemoratio B. Mariae Virg. de Monte Carmelo venerit in sabbato, Missa dici potest aut de sancta Maria in sabbato, aut propria de Commemoratione.* At the Friday, printed p. 499 and read today: *Hodie, ubi peculiaria pietatis exercitia in honorem beatae Mariae Virg. Matris dolorosae peraguntur, permittuntur duae Missae festivae de septem Doloribus beatae Mariae Virginis.* Both say: this is a commemoration, and here is when its own Mass may be said instead.

There is one real difference and §4.3 does not hide it. Carmel's condition is a weekday, which `mass_choices.when` can state. The Friday's condition is *ubi … peraguntur* — where the devotions are actually held — which is a local fact this repository decides nothing about, exactly as it decides no particular calendar. That is a limit on what `when` can carry, not a reason to file the day differently.

---

## 3. The cheap route, tested against the book

The brief's hypothesis was that the 15 September feast could carry the text and the Friday reach it by `takes_from`, so that the registry question need not be answered at all. **It does not hold, and the book is the reason.**

### 3.1 The witness

The controlling artifact is `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`, whose record pins sha256 `648fdb8f…3518a` at 82 815 941 bytes. A copy already present under untracked `build/` was hashed before any reading was taken from it and **matched the pinned digest exactly**, which is the route `roman-1962-seasonal-citation-collation-v1.toml` establishes for this edition. The printed-to-digital offset the `appointed_across` rows record, `pdf_page = printed_page + 81`, was checked at both loci and holds: printed 499–501 are digital 580–582, printed 656–658 are digital 737–739.

**These readings are from the embedded text layer, not from page images.** By this repository's own standard that makes them uncollated, and §8 says what would overturn them. They are quoted here because the differences below are gross — whole clauses and whole propers — and survive any plausible OCR damage. A word-level claim would not be safe on this evidence and none is made.

### 3.2 What the two settings actually print

Friday after Passion Sunday, printed pp. 499–501, marginal nn. 2358–2371. Fifteen September, printed pp. 656–658, marginal nn. 3615–3631.

| Slot | Friday after Passion Sunday | 15 September | Same? |
| --- | --- | --- | --- |
| Heading | *Feria VI post dominicam I Passionis / Septem Dolorum beatae Mariae Virginis / **Commemoratio*** — no class printed | *Die 15 septembris / SEPTEM DOLORUM BEATAE MARIAE VIRGINIS / **II classis*** | no |
| Rubric at head | two festive Masses permitted where devotions are held | — | no |
| Introit | *Stabant iuxta Crucem* (Io. 19, 25) + *Ibid.*, 26-27 | identical | **yes** |
| **Collect** | *Deus, in cuius passione… ut, qui **transfixionem eius et passionem venerando recolimus, gloriosis meritis et precibus omnium Sanctorum Cruci fideliter astantium intercedentibus**, passionis tuae effectum…* | *…ut, qui **dolores eius venerando recolimus**, passionis tuae effectum…* | **no** |
| Second oration | *Et fit commemoratio feriae*: **Cordibus nostris** | *Et fit commemoratio S. Nicomedis*: **Adesto, Domine** | no |
| Votive Collect | — | *In Missis votivis*: **Interveniat pro nobis** | no |
| Lesson | Iudith 13, 22 et 23-25 | identical | **yes** |
| Gradual | *Dolorosa et lacrimabilis* | identical but for punctuation | **yes** |
| **After the Gradual** | a **Tract** only, *Stabat sancta Maria* + V. Thren. 1, 12, unconditional | an **Alleluia**, *Stabat sancta Maria*, **without** the Thren. verse; plus three printed conditions — added in votive Masses, replaced after Septuagesima by the Tract, and in Paschaltide the Gradual dropped for a further Alleluia carrying the Thren. verse | **no** |
| **Sequence** | *Stabat Mater dolorosa*, unconditional, ending *Paradisi gloria. **Amen.*** | *Stabat Mater dolorosa*, marked ***(in Missis votivis omittenda)***, ending *Paradisi gloria. Amen. **Alleluia.*** | **no** |
| Gospel | Io. 19, 25-27 | identical, **followed by *Credo*** | near |
| Offertory | *Recordare, Virgo Mater Dei* (Ierem. 18, 20) | identical | **yes** |
| Secret | *Offerimus tibi preces et hostias* | identical | **yes** |
| Second Secret | feria: **Praesta nobis, misericors Deus** | *Pro S. Nicomede*: **Suscipe, Domine, munera** | no |
| Preface | *de B. Maria Virg. Et te in Transfixione* | identical | **yes** |
| Communion | *Felices sensus* | identical | **yes** |
| Postcommunion | *Sacrificia, quae sumpsimus* | identical | **yes** |
| Third oration | feria: **Sumpti sacrificii** | *Pro S. Nicomede*: **Purificent nos** | no |

### 3.3 What follows

Seven of the day's own propers are word-for-word identical and four are not. **The four that are not are the four that matter most to this question:**

- **The Collect is the text a commemoration consists of.** The commemoration of the Seven Sorrows *is* those three orations said inside another Mass, and the Collect is the one that differs. A reference asserting the two days share a formulary would be asserting sameness in precisely the slot where the book prints two prayers.
- **The chant between the Lesson and the Sequence differs in kind.** The Friday is in Passiontide and has a Tract and no Alleluia; September has an Alleluia and three seasonal conditions. `_apply_overrides` in `scripts/_calendars.py` (705–722) matches replacements on `name` and **appends** anything unmatched. It has no way to *remove* a proper the referenced formulary carries. A Friday taking from September could not suppress September's Alleluia, and would render a Passiontide Mass with an Alleluia in it.
- **The Sequence's last word differs**, and September's carries a rubric — *in Missis votivis omittenda* — that the Friday's does not.

Neither setting refers to the other. Each prints the whole Mass, and the Missal prints the Friday first. A `takes_from` in either direction would state a derivation the book does not.

**And the mechanism would not have paid for itself anyway.** `takes_from` names a key in the same file; the referring entry still needs `key`, `name` and `registry`. Reaching for it does not avoid the registry question — it only shortens the entry.

### 3.4 The cheap route that *does* work, and what it does not do

The Missal prints the Stabat Mater twice, whole, at nn. 2364 and 3624. The second printing is on a day this repository already carries: `septem-dolorum-beatae-mariae-virginis`, registry `1962-09-15`, rank II, kind marian, holding a Lesson, a Gospel and an Offertory recovered in the 2026-08-01 citation pass and no Sequence.

**So the fifth Sequence can land at 15 September today, with no ruling, no scheme and no reference** — as a transcription onto an existing entry, in the same act as its Introit, Collect, Gradual, Alleluia, Tract, Secret, Communion and Postcommunion, off page images at printed pp. 656–658. That is strictly cheaper than anything else in this file and it should be done first.

It is also **not the whole task.** It leaves the Friday exactly where `rubrics.yaml` `unsettled` says it is — "A Friday after Passion Sunday shows the feria alone, with no commemoration of the Seven Sorrows beside it" — and it leaves the *Friday's* Stabat Mater, which is a different printing with a different ending, unrecorded. §4 is about that day, and it is cheap too.

---

## 4. The proposal

Four changes. None is a schema change; none touches `tools/check-calendar-masses`, `tools/calendar-rubrics` or `src/web/browser/liturgy/assembly-model.js`.

### 4.1 The entry: undated, season-bearing, `1962-T-`

In `propers.yaml`, one mass in the **marian** section:

```yaml
- key: comm-septem-dolorum-beatae-mariae-virginis
  name: Comm. Septem Dolorum Beatae Mariae Virginis
  registry: '1962-T-septem-dolorum'
  season: passiontide
  kind: marian          # inherited from the section; not checked on an undated entry
  # no `rank`: check_entry asks for a printed rank only of a dated entry, and
  # the Missal prints no class here, only the word Commemoratio.
  propers: [...]        # the whole formulary of printed pp. 499-501
```

Why marian and not seasonal. The four entries the index files seasonal against their kind — `ascension`, `corpus-christi`, `sacred-heart`, `chrism-mass` — are filed there because *the Missal prints them in the Proprium de Tempore*, and the index's own note says which section should hold them is open. **The Friday is the mirror case and it resolves the other way:** the Missal prints it in the Proprium Sanctorum, between the March and April feasts, and its title is a title of Our Lady. Book-position and kind agree, and marian is the section where they agree. Filing it seasonal would import the open question of those four for no gain. The schema permits either: `check_entry` validates `kind` only inside `if has_date:`.

The precedent for the *shape* is `rogation-mass`, which is undated, seasonal-by-`season`, rankless, `1962-T-`-registered, carries eight propers, and records its conditional chants in a `notes` string. The Friday needs less than that: its chants are unconditional.

### 4.2 Placement: one line of `tools/calendar-days`

Beside the loop that already places `passion-monday` through `passion-saturday`:

```python
year.put(passion + timedelta(days=5), "comm-septem-dolorum-beatae-mariae-virginis",
         "Friday after Passion Sunday")
```

This is the same idiom as `year.put(easter - timedelta(days=3), "chrism-mass", "Easter -3")`. It is code, and it is the only code in this proposal. The date is not in dispute: [`calendar-computation.md`](calendar-computation.md) owns the anchor, the calendar reference's own Temporale table prints the position as "Friday after Passion Sunday", and Passion Sunday is Easter − 14.

### 4.3 Classification: widen one `assignment` rule, and add one `mass_choices` row

In `rubrics.yaml`, `- {basis: calendar-commemoration, dated: true, rank: Comm.}` becomes two rules, the new one first:

```yaml
- {basis: calendar-commemoration, keys: [comm-septem-dolorum-beatae-mariae-virginis],
   note: 'the one commemoration the calendar inscribes on a movable day...'}
- {basis: calendar-commemoration, dated: true, rank: Comm.}
```

A `keys:` rule is preferred to relaxing `dated: true`, for the reason `calendar-rubrics` reports an unmatched mass as a hard failure: a named key cannot silently sweep in a future undated entry that meant something else, and if a second movable commemoration is ever found the rule that admits it should be written then, with its own note. Dropping `dated: true` outright would be the wider and less honest edit.

Then, in `mass_choices`, a second row on the model of `carmel-on-a-saturday`: `what` naming the Mass of the feria against the proper Mass of the Commemoration, `locus` the Missal's own rubric at printed p. 499, `latin` the *Hodie, ubi peculiaria pietatis exercitia* sentence quoted as printed, `among` the two options with `takes: office_mass` and `takes: mass`, and — the part that must not be faked — **`when: null` with `open_because` saying that the condition is whether the devotions are in fact held locally, which this repository does not decide and cannot compute.** `carmel-on-a-saturday` already sets `default: null` and explains it; this row extends that honesty from the *preference* to the *condition*.

**What this filing buys and what it costs.** It buys the everyday fact: every year, on that Friday, the browser shows the Seven Sorrows commemorated at the feria's Mass, with its three orations, which is what the calendar reference inscribes (`comm.`) and what the rubrics deliver through `standingAside` and `orationsFrom`. It costs the festive-Mass permission any *computed* expression — the page will name both options and say the choice turns on a local fact. That is the right trade, because the commemoration binds always and the permission binds *ubi … peraguntur*.

### 4.4 Delete nothing silently, and clear the notes

Three prose records assert the blockage this proposal removes, and all three must move in the same change: the two `open_collation_items` in `propers.yaml` (the one recording the missing entry, and the Sequences item saying the fifth "is blocked on an entry and not on a text"); the `known_absences` entry, **if** the interim in §8.2 was taken; and the `unsettled` row in `rubrics.yaml` headed "whether a movable commemoration can be written at all under the model that landed on 2026-07-31". The four-formularies item shrinks to three, then to two once the Nativity-octave Mass lands. A record of a gap that is no longer a gap is as false as an unrecorded one — the `known_absences` block says so itself.

---

## 5. The alternatives, and why they lose

### 5.1 A synthetic date

Give the Friday a `date`, chosen so nothing collides — 03-00, or a date the sanctorale leaves empty.

**Loses, and it is the worst option here.** `date` is not decoration: `calendar-days` places dated masses by date, `check_date` validates it against `DAYS_IN_MONTH`, `calendar-rubrics` derives its `dated` predicate from it, and `check_spine` reads dates to reconcile against the spine. A date the Missal does not print would put a *computable* falsehood into the field the whole placement layer trusts, and the falsehood would resolve cleanly. That is the defect `guidance/the-shape.md` names and the one this repository has refused twice in this very file — once when it declined to land 148 machine-recovered Common pointers because a pointer with the right Common and the wrong saint "would resolve cleanly and look right", and once when it left 14, 21 and 22 May unresolved rather than answer by preference a question the books answer nowhere.

It also fails on its own terms. The day *has* no date; that is its defining property. A schema whose answer to "this has no date" is "invent one" has not modelled the day, it has hidden it.

### 5.2 An Easter-relative key in the registry id — `1962-E-35`, `1962-E+(-35)`

Encode the offset: Passion Sunday is Easter − 14, so the Friday is Easter − 9.

**Loses, on three counts.**

- **It duplicates a derivation that already exists once.** [`calendar-computation.md`](calendar-computation.md) owns the movable anchors and `tools/calendar-days` computes them. Putting the offset in an identifier makes a second statement of the same arithmetic, in a field nothing parses, that can drift from the first. This repository's standing rule is one derived table and no hand-typed restatement beside it.
- **It is wrong for most of what it would have to cover.** Sixty-six `1962-T-` entries are movable, and their offsets are not all constant: the Sundays after Pentecost vary in number, the resumed Epiphany Sundays are conditional, and `mass-of-the-first-sunday-after-epiphany` is fixed by a Sunday rule and not by Easter at all. A scheme that works for one of sixty-seven and fails for the rest is not a scheme.
- **It buys nothing.** Nothing reads a registry id programmatically. `check-calendar-masses` checks only that it is a string.

The honest version of this idea is not an id but a field, and it already exists elsewhere: `saturday_office.forms` in `rubrics.yaml` carries `from_anchor: {anchor: easter, offset_days: 0}` and `to_anchor: {anchor: trinity, offset_days: 0}`. If a movable day's arithmetic ever needs stating in data rather than in `calendar-days`, that vocabulary is where it should be stated, in the rubrics file, in the block that already has it. Not in the id.

### 5.3 Not registering movable commemorations at all

Leave the Friday out, land the Sequence at 15 September (§3.4), and declare the absence in `known_absences`.

**Loses, but it is the correct interim and it is not shameful.** It is honest, it is cheap, and it gets the fifth Sequence. The `known_absences` block exists for exactly this and is currently `[]` with a comment saying it "is the only place a movable absence can be declared: the spine derives fixed dates, so nothing below it reports one." That the Seven Sorrows is *not* declared there today, while `unsettled` and two `open_collation_items` describe it in prose, is a small inconsistency this proposal notes and does not fix.

What defeats it as a *permanent* answer is that the cost of the alternative turned out to be three data edits and one line. Permanence would have to rest on a claim nobody has established — that the schema cannot hold the day — and §1.3 shows the schema holds it already. Leaving a day out because nobody has checked whether it fits is right; leaving it out after checking is the check used as an excuse.

### 5.4 A sixth registry shape for movable commemorations — `1962-M-<key>`

Mint a prefix that says what the day is, since `T` says *temporal* and this day is printed in the sanctorale.

**Loses, narrowly, and this is the closest call in the file.** The objection is real: `1962-T-septem-dolorum` misdescribes where the Missal prints the Mass.

Three reasons it still loses. First, `T` already misdescribes several of its sixty-six members — `chrism-mass` is a ritual Mass, `rogation-mass` is *in Litaniis maioribus et minoribus* and is placed on a civil date three times in four — so the prefix has never meant "printed in the Proprium de Tempore"; it has meant "movable, and the registry numbers it not". That is exactly true of the Friday. Second, `roman-1962-propers.md` already reserves a letter for a non-Sunday non-temporal identity — `M`, "a ritual, votive, or other non-Sunday guide" — and **enumerates no `M` identity**, exactly as it enumerates no `F`. The index's note about Christ the King records the settled practice for that situation: prefer the shape the file already uses over a letter nothing fixes. Third, a sixth shape enlarges the open collation item rather than leaving it where it is, and this proposal's whole claim is that it changes nothing that has to be settled later.

If a reader disagrees, the disagreement is cheap: the id is a string nothing parses, and changing it later is a one-line edit in one file. **This is the point in the proposal least worth arguing about, and it is recorded as a preference rather than as a finding.**

### 5.5 Filing the entry `additional-mass` instead of `calendar-commemoration`

Treat the printed formulary as the primary fact, as `chrism-mass` and `rogation-mass` are treated.

**Loses, but it is the runner-up and a reader may reasonably take it.** `additional-mass` carries `commemoration: none`, so `assembly-model.js` would refuse the Seven Sorrows a place among the day's commemorations (757–763: "a day of this kind is never commemorated") and the Friday would show the feria's Mass alone with a further Mass offered beside it. That inverts the book: the commemoration is what happens every year everywhere, and the festive Masses are what happens where devotions are held.

The Chrism Mass is not a counter-example. It is a second Mass of a day whose identity is settled and which is *never* commemorated in the Thursday's Mass; there is no commemoration to lose. Here there is.

---

## 6. How this relates to `appointed_across` and to `reslotted`

Both landed recently, both say "this text belongs here too" without copying, and **neither is the mechanism this day needs.** Saying so is the point of this section; a third idiom would be worth arguing for only if one of these two nearly fit, and neither does.

- **`appointed_across`** (`rubrics.yaml`, two rows; read by `_calendars.spans_of`, checked by `span_problems`) states that *one* text is appointed over a *span of days*: the Sequence *Victimae paschali laudes* through the octave of Easter, *Veni Sancte Spiritus* through the octave of Pentecost. Its `prints` names one mass and one proper, and its `keys` names the masses that take it. **The Seven Sorrows is not a span.** It is one text printed twice, on two days five months apart, in two settings that differ (§3.2) — the opposite configuration. Writing it as a span would assert both a sameness the book denies and a contiguity it does not have.
  It is worth noticing what `appointed_across` did *not* need: it did not need the twelve octave days to stop being twelve entries. It stated the appointment once, beside the days, in the rubrics file. §4.3 does the same thing with the festive-Mass permission — states it once, in `mass_choices`, beside the day — and that parallel is the reason `mass_choices` is the right home rather than a note on the entry.
- **`reslotted`** is one of seven closed `DEPARTURE_KINDS` in `scripts/_calendars.py` (107–116), "the same words in a different slot", and it belongs to the **recension** machinery: a departure is a statement by one calendar *about a base calendar's* entry, and `roman-pre-1955` uses it eight times. There is one calendar here and no base. `reslotted` cannot be borrowed across that boundary without making `roman-1962` a recension of itself.

What the two do jointly establish is a **precedence about placement**: when this repository has needed to say that a text stands in more than one place, it has said so in `rubrics.yaml` — the file that states rules once per calendar — and left `propers.yaml` holding formularies. §4 keeps to that. The entry holds the Mass; the rubrics file holds the classification and the permission.

---

## 7. Blast radius

**Schema.** None. `check-calendar-masses` and `calendar-rubrics` are unchanged, and no field is added anywhere. This is the claim most worth attacking, and §8.4 says what would break it.

**Data, `propers.yaml`.** One new mass in the marian section — the 491st, and the 18th marian. Its formulary is fourteen propers plus three orations of the feria's commemoration; §8.1 governs how they are read. Separately, and independently landable, the 15 September entry gains its Introit, Collect, Gradual, Alleluia, Tract, Sequence, Secret, Communion and Postcommunion. Four notes edited per §4.4.

**Data, `rubrics.yaml`.** One `assignment` rule added above an existing one; one `mass_choices` row added; one `unsettled` row deleted; `known_absences` unchanged (or one row deleted, if §8.2 was taken).

**Code.** One `year.put` in `tools/calendar-days`, in the Passion-week block.

**Emitted data.** `src/web/data/structure/propers/roman-1962.json` gains a mass; `structure/rubrics/roman-1962.json` gains a basis position for it and a `mass_choices` row; every emitted year file under `structure/calendar/roman-1962/` gains one key on one date — **101 year files**, by the count the Rogation note records. Per the standing directive these are regenerated through the Make targets and no release hash is ever hand-edited.

**Captured transcripts.** `calendar-rubrics` `EXAMPLES` carries live counts — "roman-1962: 460 masses classified over 28 bases and 28 rows" — and `tools/tests/test_example_replay.py` replays them. A 491st mass moves that number. **The transcripts must be recaptured, not edited.** `calendar-spine`'s own examples are untouched: the spine is unchanged, since it derives nothing here.

**Solved cases.** None of the 28 breaks. `calendar-rubrics run_check` treats a source exercising no case as a hard failure only per *source*, and `roman-1962` has sixteen. But a new classification with no case is a rule nobody checks, and by the standard of `chrism-mass` — which has one, `maundy-thursday`, asserting it is offered and never ranked — **this day should get one**, worked from the book: a Friday after Passion Sunday in a named year, expecting `passion-friday` as winner at row 22 with the Seven Sorrows admitted as an ordinary commemoration, and the `mass_choices` row present.

**Counts that move in prose.** The index header's "104 entries of rank `Comm.`" stays 104 — the new entry carries no rank — but the sentence about it is wrong today for the reason §1.2 gives and should be corrected whether or not anything else here is accepted. The five-Sequences item goes to five of five.

---

## 8. What would have to be true for this proposal to be wrong

Stated as checks a reader can run.

1. **If the page images disagree with the text layer.** Everything in §3.2 is from `pdftotext` over a digest-matched artifact, and this repository's own rule is that no OCR text layer may supply a reading. The differences claimed are whole clauses and whole propers, which OCR does not invent — but **the two formularies must be read at 200 dpi or better before either is transcribed**, and if the Collects turn out to be the same prayer, §3.3's first and strongest argument falls. It would not resurrect `takes_from`, because the chants and the Sequence ending would still differ and `_apply_overrides` still cannot remove a proper; but the proposal would then be resting on a narrower base than it claims.
2. **If `known_absences` cannot in fact hold a movable match.** `check_absences` (552–563) requires `what`, `match`, `effect` and `locus`, and checks only that each is truthy. The block's comment says it is "the only place a movable absence can be declared", but nothing in the tool demonstrates a movable `match` is expressible, and no row has ever been written. §5.3's interim depends on it. This is unverified and it is the one factual gap in this file.
3. **If the Friday's identity is not what the calendar reference says.** `40-temporale.tex` line 25 prints "Seven Sorrows of the Blessed Virgin Mary & Friday after Passion Sunday & comm. & Seasonal commemoration printed in the calendar." The whole of §4.3 rests on `comm.` there. If a witness shows the 1962 books rank the day otherwise — and the Missal itself prints no class at the formulary, only the word *Commemoratio* — the classification changes and §5.5 may become right.
4. **If `kind` is checked on an undated entry by anything downstream.** §4.1 puts a marian mass in the file without a `date`, which `check_entry` permits because it validates `kind` only inside `if has_date:`. No emitter in `assembly-model.js` was traced for an assumption that a marian mass is dated. **This was not checked and should be**, by adding the entry and running the gates before anything is written about it.
5. **If a `Comm.`-natured entry carrying a full formulary renders wrongly.** All 104 existing commemorations are placeholders; none carries a real Mass. This entry would be the first. `orationsFrom` (881–905) builds the commemoration's orations from the candidate, and nothing traced suggests it would show more than the orations — but nothing traced proves it either, and a page that printed a whole second Mass where three prayers belong would be a rendering defect of the class `guidance/the-shape.md` names.
6. **If a second movable commemoration exists.** §4.3 uses a `keys:` rule on the ground that there is exactly one. The reference's Temporale table lists no other `comm.`, and the Minor Litanies and the Office of Our Lady on Saturday are not commemorations. If another is found, the rule generalises — but the generalisation should be written then, against that day, and not now.
7. **If the two permitted festive Masses are more than a permission.** §4.3 treats *permittuntur duae Missae festivae* as conditioned on a local fact. If a rubric elsewhere in the 1960 code makes those Masses obligatory somewhere this repository does serve, `mass_choices` with `when: null` understates them, and `additional-mass` — §5.5 — becomes the better filing after all.

---

## 9. If this is accepted, the order of work

Steps 1 and 2 are independent of every ruling and either could be done today.

1. **Read printed pp. 656–658 at page images and transcribe the 15 September Mass whole, Sequence included.** This lands the fifth and last 1962 Sequence, needs no decision from anything above, and is the single highest-value act available. The entry already exists.
2. **Correct the two prose claims that are wrong now**: the index's "each of the 104 entries of rank `Comm.` carries a civil date and a `1962-<date>-comm` registry id" (§1.2), and the `unsettled` row's premise that the model's datedness is what blocks the day (§1.3). Do this whether or not anything else here is accepted.
3. **Read printed pp. 499–501 at page images** and settle §8.1 — whether the Collects, the chants and the Sequence ending differ as §3.2 has them from the text layer.
4. **Adopt §4.1 through §4.3** and land the Friday, in one change, with the notes of §4.4 cleared in the same commit.
5. **Write the solved case** (§7) from a book and not from the model, and recapture the `calendar-rubrics` transcripts rather than editing them.
