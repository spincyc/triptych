# Per-proper witness attestation: a proposal, and an argument that the gap is on the Latin side alone

**Status: proposal. Nothing here has been accepted, and nothing here has been built.** No code, schema or data file was changed in writing it. Its subject is the sentence [`../recensions.md`](../recensions.md) §6 calls **precondition 0** and §8.4 restates as the reason residence has not been flipped: *"no proper in this repository yet records which printings have been read for it, so moving 2,312 transcriptions under a 1920 heading would assert a provenance nobody established."* The decision belongs to a human reader, and the sections are ordered so that a reader who disagrees with the reasoning can find the disagreement rather than the conclusion.

[`pre-1955-precedence-proposal.md`](pre-1955-precedence-proposal.md) and [`movable-commemoration-proposal.md`](movable-commemoration-proposal.md) landed on 1 and 2 August and are the model for an argued proposal here: each was asked to design a mechanism and each concluded that most or all of it was unnecessary. This file owes them its shape. It does not edit them and it does not edit anything else — [`../recensions.md`](../recensions.md) owns Rules 1–8, [`../web-data.md`](../web-data.md) owns the emitted layer, and `src/sources/calendars/README.md` owns the translations contract.

**The headline, stated first so it cannot be reached by accident.**

1. **Precondition 0 is met on the English side and unmet on the Latin, and the record says neither.** Every one of the 242 English readings in `roman-1962-proper-translations-v1.toml` names its printing, its page, how it was read and what the reading did — per proper, machine-readable, and now gated. Zero of the 337 Latin texts in `roman-1962/propers.yaml` name a printing in any field a tool can read. The sentence as written — *no* proper records it — was true when it was written and is false now, and the half that is now false is not the half the flip needs.
2. **The number in it has drifted.** 2,312 was the derived census on 2026-08-01 and is **2,345** at `ef1f122b5`. It is stated by hand in two places, and this repository's standing rule is one derived table and no hand-typed restatement beside it.
3. **The Latin gap is total, and the schema will not currently take a fix.** `PROPER_FIELDS` is a closed set of nine keys and none of them is a witness. What provenance exists is prose: 231 of 490 mass `notes` and 16 of 2,345 proper `notes` name the printing they were read from, and the emitted structure drops `notes` entirely, so nothing reads any of it.
4. **The smallest mechanism is not a new idiom.** The act history already keys books by `[[witnesses]]` id and already says of each which act it attests; `check-calendar-masses` already loads it. One field — `attested_in`, the acts file's own key — stated once in the header and overridden at the mass and at the proper, on the `psalm_numbering` inheritance this file already has, carries the whole of it.
5. **But per-proper attestation is not the binding constraint on the flip, and should not be built as one.** Even fully attested, flipping residence would move 2,345 propers under a 1920 heading with every one of them saying *read from the 1962 typica and no other*, which buys the reader nothing until a pre-1955 witness is read at page images — and §8.4 records why that has not happened. **The reason to build per-proper Latin attestation is the rights claim and the detector, both of which are live today.** The flip should stay deferred, for the reason §8.4 already gives and not for this one.

**The recommendation is therefore: correct the two records, register the one missing witness, build `attested_in` for the rights claim, and leave residence unflipped.**

---

## 1. The present model, exactly

Counts were measured against `ef1f122b5`, from `git show` and not from the working tree, because another lane holds uncommitted changes in `roman-1962/propers.yaml` and its section totals were already moving while this was written. Line and function references are accurate at that commit and will drift.

### 1.1 What a proper may carry

`tools/check-calendar-masses:166` enumerates it, and the enumeration is deliberate — its own comment records four defects in one day that a permissive schema hid:

    PROPER_FIELDS = frozenset(
        {"name", "source", "verses", "incipit", "text", "notes", "cycles",
         "takes_from", "psalm_numbering"}
    )

`source` is not a book. It is one of `scripture`, `composed`, `mixed` — a statement about what kind of text the proper is, not about where anyone read it. **No field in that set names a printing**, and `check_proper` (216) reports any key outside the set as an unrecognised field.

One consequence is worth stating now, because any per-proper design collides with it. `check_translations` (295) reads `proper.get("translations")` and holds it to `check_translation_list` — but `translations` is **not in `PROPER_FIELDS`**. The sidecar's own `merge` prose instructs a reader to set each proper's `translations` key from the entry's array. Performed today, that merge would raise "unrecognised field 'translations'" once per merged proper, 242 times. The rules exist and the door they are behind is bolted.

### 1.2 What the sidecar carries, which is the whole of precondition 0 for English

`src/sources/inventories/roman-1962-proper-translations-v1.toml`, 242 entries, 27 `untranslated` rows, 3 `[[sources]]`. Per entry:

| Field | Count | What it records |
| --- | ---: | --- |
| `witness` | 242 | which registered book the reading is of |
| `translations[].source_id` | 395 | the printing or artifact each text was read from, keyed `(lang, source_id)` |
| `printed_page` | 190 | where in that book |
| `ia_leaf` | 118 | which leaf of that scan |
| `collated` | 176 | *how* it was read — every value is `page-image, <date>` |
| `collation_result` | 176 | what the reading did: confirmed, corrected, recorded from the page |
| `detector` | 66 | 50 `sibling-agrees`, 16 `second-printing-agrees` |
| `disagreement` | 9 | the answer where two readings differ |

153 entries carry two `[[entries.translations]]`; 89 carry one. Every one of the 242 lands on a real Latin text in `propers.yaml` and none lands nowhere. Against the 337 distinct Latin texts the 1962 index holds, **242 have an English reading whose printing is recorded and 95 do not**.

That is not a partial answer to "which printings were read for this proper". For the English it is a complete one, at four levels of specificity, and since e2e2f2fc0 it is also self-checking: `witness_verdict` (1058) compares the two readings, `witness_problems` (1083) fails on an unrecorded divergence and on a note left behind after a correction, and the agreement half is reported as a finding.

### 1.3 What the three commits of 1–2 August actually reach

| Commit | What it added | What it reaches |
| --- | --- | --- |
| `5420ea2e7` | `attests` / `attests_kind` / `attests_basis` on every `[[sources]]` row; `source_attestation_problems` | **the book**, not the proper. Three rows in the 1962 sidecar, one in the postconciliar |
| `e2e2f2fc0` | the second 1861 transcription attached to 153 entries; the comparison derived on every run | **English propers**, 153 of them |
| `0032bd735` | a `[[witnesses]]` row for the 1861 in the act history | **the book**, again |
| `0799a1924` | `text_from`, `stands_before`, the seven kinds, the stamp | **the mass**, and it names a *calendar*, not a printing |

The first three are a genuine advance and this file is not arguing otherwise. What they have in common is that none of them touches a Latin proper. `source_attestation_problems` (733) validates a `[[sources]]` row and the sidecars hold four such rows between them; it says nothing about the 2,153 propers of `propers.yaml` that state something somebody read out of a book.

### 1.4 Where the Latin's provenance is actually written

In prose, in three places, none of them read by anything:

- **The file header.** `verification` in `roman-1962/propers.yaml` is one paragraph describing four — now five — tiers of evidence for 490 masses. It names the CMAA facsimile, the 1962 Benziger, page images at 200 and 400 dpi, and the tracked 1920 typical edition. It is accurate and it is a single string.
- **231 of 490 mass `notes`.** 230 name the CMAA facsimile, 231 give a printed page, 204 say the reading came from a text layer, 82 say page image, 28 record corroboration against the Benziger scan, 2 name the 1920.
- **16 of 2,345 proper `notes`.** All 16 are in two masses. They are the most precise provenance statements in the tree, and they are worth quoting because they show what the field would have to hold — Corpus Christi's Collect: *"Read from the 1962 CMAA facsimile page image, printed p. 375 = digital p. 456, under the heading Oratio; corroborated at 1920 lines 56332-56341, which prints the same words and the shorter conclusion Qui vivis et regnas."*

`notes` reaches no reader. The emitted proper in `src/web/data/structure/propers/*.json` carries `citations`, `cycles`, `form`, `incipit`, `name`, `source`, `taken_from`, `text`, `translations`, `untranslated` — and not `notes`. **Every Latin provenance statement in this repository is a claim nothing reads, which is the defect `check-calendar-masses`' own header says the attestation gate exists to end.**

### 1.5 The stamp, and what it names

`_calendars._stamp` (344) writes `{calendar, kind, stated, text_from, basis, also}` onto every mass of a recension, and `day.js:759` prints it: *"Text served from Missale Romanum, editio typica 1962. This recension states no text of its own here."*

`text_from` names a **calendar directory**. The comment at `_calendars.py:84` says so exactly — "MECHANICAL … the calendar that supplies every entry this file does not state". `tools/tests/test_recensions.py:131` is named `test_an_inherited_entry_says_which_printing_it_was_read_from` and asserts `stamp["text_from"] == "base"`. The name overclaims by one step, and the step it skips is the whole of this proposal: a calendar is not a printing, and today the two happen to correspond only because `roman-1962` was read out of one book.

---

## 2. The recorded claim, verified

### 2.1 Three readings of one sentence

| Reading | Verdict |
| --- | --- |
| *No proper records which printings were read for it* | **False as of 2026-08-02** for 242 propers, in English, machine-readably, at page-image precision, with a standing detector |
| *No proper records which printing its LATIN was read from* | **True**, and total: 0 of 337, with no schema field that could hold it |
| *Residence cannot be flipped until it does* | **True but not sufficient**, and §4.4 argues it is not the binding constraint |

The claim was written on 2026-08-01, before `5420ea2e7` and `e2e2f2fc0` landed. It has not been wrong for long. But it is the sentence a later session will read to decide whether the work is done, and it currently says the work is entirely undone when three quarters of the English half is finished and gated.

### 2.2 The number

`2,312` appears twice: `../recensions.md` §8.1 and §8.4, and `src/sources/calendars/roman-pre-1955/propers.yaml`'s own comment on why residence has not been flipped. It was the derived census figure at `0799a1924` on 2026-08-01 [verified: `git show 0799a1924:guidance/propers-for-agents.md` prints `| Propers | 2312 | 1031 |`]. At `ef1f122b5` the census block prints **2,345**, and the working tree at the time of writing was already past that again.

Both statements of it are hand-typed restatements of a block that `mass-propers census --write` owns and `make check-propers-census` defends. `guidance/the-shape.md` §2 names this defect and `../recensions.md` §2 records committing it in the document arguing against it. It should be replaced by a reference to the census rather than by a corrected number, which would drift again by the end of the week. **This is worth doing whether or not anything else here is accepted.**

---

## 3. The Latin side, and why it is genuinely different

### 3.1 The question may have no per-proper answer — and it does, for 337 propers

The brief that commissioned this file raised the possibility that "which printing was this Latin read from" has no per-proper answer at all. It does not hold. Every one of the 337 real Latin texts was read out of an identifiable artifact on an identifiable date, and for 16 of them the answer is written down to the page and the line. What is missing is not the answer; it is anywhere to put it.

Note also what is *not* asked. 139 propers are named `Placeholder` and were read from nothing; 53 propers carry `takes_from` and hold no text of their own; 1,811 carry a scripture citation and no Latin. A citation is still a reading of a book — the column, the marginal number and the saint's name were read off the facsimile — so the honest scope is the **2,153 propers that state something somebody read**, of which 337 carry composed Latin and the rest carry references.

### 3.2 One mass already in the tree refutes attestation at the mass

`corpus-christi` holds eleven propers. Seven scripture-bearing ones were read from the facsimile's text layer in the citation passes; four composed ones — Collect, Sequence, Secret, Postcommunion — were read from page images at 200 and 400 dpi on 2026-08-01 and corroborated against the 1920. One value for the mass would have to choose between "text layer" and "page image at 400 dpi with a second witness", and would be false about seven propers or about four. `commemoratione-omnium-fidelium-defunctorum` is the second instance of the same shape.

So the unit is the proper, and the precedent for a per-proper field that mostly inherits is already in this file: `psalm_numbering`, whose reader says it in terms — *"A proper may therefore declare its own … what it does not declare it inherits"* (`tools/mass-propers:409`). Two propers in the whole corpus made that field necessary, and it is not regretted.

### 3.3 The book every Latin word came from is not a witness

`artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf` is the artifact 230 mass notes name. The act history carries 42 `[[witnesses]]` rows across `roman-holy-week-acts-v1.toml` and the wider `latin-missal-acts-v1.toml` that extends it, and **none of them is that facsimile.** The act `editio-typica-1962` cites it by id in its own `citation` field and lists `attested_in = ['benziger-iuxta-typicam-1962']` — the corroborating scan, not the controlling one.

This is not a defect in the Holy Week slice, whose declared `extent` is four liturgies. It is a row the wider slice would need, and it is the exact finding `5420ea2e7` recorded for the English: *"The book every English word is read from is the one the act history does not carry."* The same sentence is true of the Latin today, and `check-calendar-masses` now reads that history, so the gap is one a check could see.

`edition.catholic-church.missale-romanum.vatican-typica-1962`, `…vatican-typica-1920`, `…benziger-iuxta-typicam-1962` and `…pustet-ratisbon-1862` are all registered in the source library, so no new registration is needed to name any of them; only the witness row is missing.

### 3.4 The rights claim nothing joins to the propers

`src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml` holds that the 1962 typical edition is probably protected in the United States until 2057, and that what saves the project is **17 U.S.C. 103(b)**: the new edition's copyright reaches only its own new matter, and nearly everything quoted here was inherited verbatim from typical editions long in the public domain. The record then names the material that is the 1962's own — *"the 1955 Holy Week, the 1960 Code of Rubrics, the sanctoral added after 1920, and its own front matter"* — and says that is what must not be published from this scan. It also records that a brief was wrong about this once, having asserted that no Latin is published from the facsimile when whole prayers are.

**That holding is a per-proper claim stated once in prose over 2,153 propers, with nothing joining the two.** A proper that named the earliest printing carrying its text would *be* the 103(b) claim, made where the text is, checkable. The sanctoral — the class the record names — is where recent waves have been reading hardest.

---

## 4. What flipping residence would do, operationally

### 4.1 The mechanics

1. `roman-pre-1955/propers.yaml` stops being six departure rows and becomes the full index: 490 masses, 2,345 propers, under its existing header `edition: Missale Romanum, editio typica Vaticana 1920`.
2. `roman-1962/propers.yaml` becomes the departure file, declaring `text_from: roman-pre-1955` and — because `recension_problems` (`_calendars.py:478`) refuses `text_from` without it — a `stands_before` naming an act *later* than 1962. The act history carries `celebrationis-eucharisticae-1970` in its wider slice, so the value exists; whether that is the right claim is a separate question nobody has asked.
3. The six departures invert. §9.4 measured the arithmetic already: 20 of 21 unit-level rows would be `added` in the wrong direction and are `absent` in the right one, which is the whole reason for the maintainer's ruling.
4. `mass-propers structure` writes the text into `structure/propers/roman-pre-1955.json` and leaves `roman-1962.json` carrying stamps.
5. `day.js:765` then prints, on every 1962 day, **"Text served from Missale Romanum, editio typica Vaticana 1920."**

### 4.2 What breaks

- **Step 5 is false.** No word of the served Latin was read from a 1920 book. The sentence is currently true in the other direction and would become a claim about provenance that nobody made — which is precisely the wording of the docstring at `day.js:720` explaining why the stamp was built.
- **The English does not follow.** `overlay_problems` finds a sidecar at `root / f"{path.parent.name}{OVERLAY_SUFFIX}"` (`check-calendar-masses:1161`). The sidecar is `roman-1962-proper-translations-v1.toml` and names `target = "src/sources/calendars/roman-1962/propers.yaml"`. Move the masses and the English is attached to a file that no longer holds them; the pre-1955 missal keeps serving 490 masses with `"translations": []`, which is what it does today.
- **The rights claim inverts in the dangerous direction.** The 1920 typical edition is publishable; the 1962 is probably in copyright until 2057 and is carried under 103(b). A heading reading 1920 over text read from the 1962 understates the obligation on the served Latin, and understating is the failure that matters.

### 4.3 The symmetry, which nobody has stated

**The flip would fix the English attestation and break the Latin one.** The only English this repository holds is a pre-1955 hand missal's, served under a 1962 heading because `roman-pre-1955` has no sidecar — `5420ea2e7`'s own commit message says so. Both `[[sources]]` rows now declare `attests = "si-quid-est-1634"`, an act of 1634. So the two languages point in opposite directions across the same 242 propers: the Latin is 1962 and the English is pre-1955, and each is currently filed under the other's heading in one of the two calendars.

A per-proper attestation is the only thing that can hold both at once, because it is per **witness** and not per **file**, and a proper can name two witnesses standing on either side of 1955. That is a better argument for the mechanism than the flip is.

### 4.4 Why this is not the binding constraint

Suppose attestation were complete tomorrow. Every one of the 2,153 propers would carry a value, and 2,137 of them would read *the 1962 typica, and no other book*. Flipping residence would then be honest — and it would tell a reader nothing they are not told today, because §8.4's second bound is untouched: **no pre-1955 text has been read from a page**, the only pre-1955 witnesses are OCR text layers, and this repository measured what that grade is worth at 38 corrections in 99 orations.

The flip's benefit arrives when pre-1955 readings arrive. Precondition 0 gates a step whose value is gated by something else. It should be satisfied — but on its own merits, and its own merits are §3.4 and §4.3, both of which bind now.

---

## 5. The proposal

Four changes, in increasing cost. §5.1 is required under every design and is nearly free.

### 5.1 Register the witness the Latin was actually read from

One `[[witnesses]]` row in `latin-missal-acts-v1.toml` for the CMAA facsimile of the 1962 typica: `attests = "editio-typica-1962"`, `attests_kind = "decree-printed-in-book"` (the decree *Novo rubricarum corpore* is printed at its page 2 and the act already cites it there), `read_from` as the evidence supports, `attests_basis` saying what the book is and what it is not. A second row for the 1920 witness already exists.

Without this, any per-proper field resolved against the act history would find no witness for the book 230 mass notes name, which is a check that fails on arrival.

### 5.2 `attested_in`, stated once and overridden twice

The acts inventory already uses this key, on acts, naming witness ids: `attested_in = ['missale-romanum-1920']`. Reuse it, not a fourth idiom:

```yaml
# in the file header, where verification already stands
attested_in:
- witness: missale-romanum-1962-cmaa
  read: ocr-only

# on a mass, where its notes already say this in prose
attested_in:
- witness: missale-romanum-1962-cmaa
  read: page-image
- witness: benziger-iuxta-typicam-1962
  read: ocr-only
  role: corroborating

# on a proper, where the two masses of §3.2 need it
- name: Collect
  source: composed
  text: |
    Deus, qui nobis...
  attested_in:
  - witness: missale-romanum-1962-cmaa
    read: page-image
    locus: printed p. 375 = digital p. 456
  - witness: missale-romanum-1920
    read: ocr-only
    locus: lines 56332-56341
    role: corroborating
```

`witness` resolves against `act_history()` (`check-calendar-masses:697`) — the loader this tool already imports, which resolves `extends` so the narrow and wide slices are read as one. `read` takes the act history's own three values: `page-image`, `ocr-only`, `not-read`. `page-image` is already the shared word — the sidecar writes `collated = "page-image, 2026-07-31"` and the acts file's `evidence` prose names it as the value no row there claims.

**What it does not do:** it does not carry the reading. It carries which books were opened and how, and leaves the wording to `text`. It is the Latin analogue of `witness`, `printed_page` and `collated` on a sidecar entry, and deliberately not of `translations[].text`.

**Inheritance is the whole of why this is small.** Stated once in the header, it covers the 2,137 propers whose answer is the modal one. ~82 masses override with `page-image`, ~28 add the Benziger, 2 masses and 16 propers override at the proper. This is the `psalm_numbering` shape exactly (§3.2), and it means the change is roughly **one header value, thirty to a hundred mass rows and sixteen proper rows** — not 2,153 hand-typed rows, which is the count that makes the idea look impossible.

### 5.3 What the checks must require

- `PROPER_FIELDS` gains `attested_in`; so must whatever set governs a mass and the header. The header set `REQUIRED_TOP` already requires `verification`, so a header `attested_in` is the same kind of statement one level up.
- Every `witness` names a row the act history carries, exactly as a `[[sources]]` row's `attests` must name an act it carries, and with the same message shape.
- `read` is drawn from the closed vocabulary. A value of `not-read` on a proper carrying real `text` is a contradiction and should fail.
- A proper carrying `text` that resolves to no `attested_in` at any level fails. A `Placeholder` and a `takes_from` proper are exempt: the first asserts no text and the second holds none.
- The resolution is derived, not written: one function returning the effective list for a proper, on the model of `resolve_propers` and `numbered_entries`, so that the census and any future page read the same answer.

### 5.4 What it lets the project do

| | Today | With it |
| --- | --- | --- |
| Publish decision under 103(b) | one prose holding over 2,153 propers | per proper, from the earliest witness that carries the text |
| Latin transcription detector | the CMAA/Benziger comparison ran once by hand, for 28 masses, on 2026-08-01 | derivable on every run, exactly as `witness_verdict` is for English |
| "Which printing?" on the page | `notes` is dropped from the emitted structure; nothing is shown | the same shape the witness manifest already gives the English |
| Residence flip | asserted from a header | checkable: does any witness on this proper attest an act at or before 1955? |

The second row is the one that has already paid once. `e2e2f2fc0`'s argument — that a comparison run once by hand is a fact about a day rather than a property of the data, and that making it standing immediately found a ninth divergence nobody knew about — applies verbatim to the Latin of the Commune and nothing carries it.

---

## 6. The alternatives, and why they lose

### (a) Do nothing, and leave residence unflippable

**Wins on the flip and loses on everything else, which is why it is not the recommendation.** As an answer to "should residence be flipped now", doing nothing is correct and §4.4 is the reason. `../recensions.md` §8.4 already records residence as deliberately not flipped, the recension works, and the calendar serves. Nothing is broken by waiting.

What defeats it as an answer to *this* question is that the two live costs — the unjoined 103(b) claim and the un-derived Latin comparison — are not costs of the unflipped state. They are costs of having no per-proper Latin provenance at all, and they are being paid today, on a corpus that grew by 33 propers in one day while this file was written.

### (b) Flip on the header alone, and rely on the prose

**Loses, and this is the option the whole apparatus exists to refuse.** The file-level `edition` would assert 1920 while 231 mass notes name a 1962 facsimile, and a reader — and every emitted file — would see only the first. It is the `reslotted` failure in a new place: a claim that resolves cleanly and answers wrongly, with nothing downstream able to tell.

### (c) Attest at the mass and never at the proper

**Loses on evidence already in the tree.** §3.2: `corpus-christi` and the All Souls entry each hold propers read two different ways from two different books. A mass-level value is false about seven propers or about four in the first case. It is worth noticing that mass-level would be *cheap* — 231 masses already carry the prose — and that the two counter-examples are exactly the two masses anyone has read most carefully. That is not a coincidence; it is what happens when the reading gets good enough to need the distinction.

### (d) Write a value on all 2,153 propers by hand

**Loses on the repository's own standing rule.** A value repeated 2,137 times is a hand-typed restatement of one fact, and the copies would drift the first time a mass moved. Inheritance is not a convenience here; it is what makes the field mean "this proper differs from the file's default", which is the only thing worth recording.

### (e) Derive it by parsing the `notes`

**Loses.** 231 mass notes and 16 proper notes contain the answer in English sentences of no fixed shape, written for a human. A parser over them would be a second reading of a field written for the first, and it would silently produce a default for the 259 masses whose notes say nothing. Worse, it would remove the reason to ever write the field: the parse would succeed and the record would stay prose.

Prose is where the *basis* belongs and the field is where the *fact* belongs — the same split `attests` and `attests_basis` already make on a `[[sources]]` row, and this proposal should follow it: `attested_in` for the witnesses, `notes` for the reasoning.

### (f) Give the Latin a `translations` row with `lang: la`

**Loses, narrowly, and it is the most tempting design here.** The keying is exactly right — `(lang, source_id)`, one witness speaks once per proper, two witnesses are the detector — and it would need no new comparison function at all, because `witness_verdict` already works on any language.

Three reasons it still loses. The Latin is not a translation of the Latin, and `check_translations` requires "a text to translate", so the primary text would have to become a rendering of itself. `mass-propers` ranks the manifest by coverage and sorts every list into that order, so a `la` row would enter the language selector as a witness a reader could choose. And `translations` is not in `PROPER_FIELDS` (§1.1), so the door is bolted for this design too and would have to be opened either way.

The honest part of the idea should be kept: whatever the field is called, the *keying* should be the sidecar's, one row per witness, because that is what makes a second reading attachable rather than a replacement.

### (g) Extend the sidecar to the Latin instead of touching `propers.yaml`

**Loses, but it is the runner-up and a reader may reasonably take it.** The sidecar exists precisely because another lane owns `propers.yaml`, its own header says so, and it is already gated. A `roman-1962-latin-attestation-v1.toml` beside it would land without contending for that file.

What defeats it is that the sidecar's own header names its eventual home — inside each proper — and a second sidecar would be a second thing to migrate later, keyed by `(mass, form, proper)` triples that must be kept in step with a file that gains masses weekly. The sidecar's `merge` block already warns that an entry whose mass, form, proper or incipit no longer answers the target is stale. Two of those is one too many.

---

## 7. Blast radius

**Schema and validator.** `tools/check-calendar-masses`: `PROPER_FIELDS` (166) gains a key; a new `attested_in_problems` beside `source_attestation_problems`, reading the same `act_history()` (697) and therefore adding no new dependency — `tmt.json` already declares act-history for this tool. `scripts/_calendars.py` gains the resolution function.

**Data, `latin-missal-acts-v1.toml`.** One `[[witnesses]]` row (§5.1). This file is nobody's exclusive lane at the time of writing but is read by `check-calendar-masses`, so the row lands before the check does.

**Data, `roman-1962/propers.yaml`.** One header value; on the order of 30–100 mass rows and 16 proper rows, all of them restating what the corresponding `notes` already say in prose. `postconciliar/propers.yaml` would need its own header value or the check must not require one of a calendar that declares none.

**Emitted data.** `structure/propers/*.json` gains a key per mass or proper only if the field is emitted, which §5.2 does not require and §5.4 wants eventually. Per the standing directive these are regenerated through the Make targets and no release hash is hand-edited. Note that `roman-1962.json` is **already stale** at `ef1f122b5`: its `translations` manifest lists one witness where the sidecar has held two since `e2e2f2fc0`. That is the open defect `propers-for-agents.md` records as "A stale browser structure file — Open", and it is prior to this proposal.

**Captured transcripts.** `check-calendar-masses`' `EXAMPLES` transcript is already declared stale in `scripts/replay_examples.py:207` — "2026-07-31: 459 masses over 1465 propers recorded; 462 over 1472 now" — and the live figures are 490 over 2,345. Nothing here makes it worse, and the STALE note itself should be recaptured rather than edited whenever that file is next touched.

**The 28 solved cases.** None moves. They are `calendar-rubrics` cases about which day wins, asserting `winner_row` and its neighbours; provenance is not among the fields `EXPECTATIONS` enumerates and no case asserts anything about a printing. This proposal touches no rubric, no basis and no row.

**Tests.** `tools/tests/test_recensions.py:131` should be renamed: it asserts `text_from == "base"` under the name `test_an_inherited_entry_says_which_printing_it_was_read_from`, and `text_from` names a calendar (§1.5). That is a naming correction and not a behaviour change, and it is worth making whether or not anything else here is accepted.

**Documents.** `../recensions.md` §6 item 0, §8.1 and §8.4; `src/sources/calendars/roman-pre-1955/propers.yaml`'s comment on the flip; `src/sources/calendars/README.md`'s translations section, which would gain a sibling paragraph. **None of them is edited by this file, which owns only itself.**

---

## 8. What would have to be true for this proposal to be wrong

Stated as checks a reader can run.

1. **If the 103(b) argument does not in fact turn on the printing.** §3.4 reads the rights record as making a per-proper claim about which typical edition first carried each text. If the operative distinction is coarser — whole sections rather than individual prayers — then a section-level statement would carry it and the per-proper field is over-built for that purpose. The record names "the sanctoral added after 1920", which is a set of days and not a set of propers, and that is the reading most likely to be right against this file.
2. **If the CMAA facsimile turns out to be registered somewhere the act-history loader reaches.** §3.3 rests on reading all 42 `[[witnesses]]` rows across the two slices at `ef1f122b5`. If a third slice exists, or if the row lands while this is being read, §5.1 is already done and the rest is unaffected.
3. **If `attested_in` on a proper is the wrong grain because a proper is not a unit anyone reads.** The facsimile is read by column and by page; a page holds several propers of several masses. If the natural unit of a reading is the *page*, then the honest record is a page-to-proper map and `attested_in` is a projection of it. §1.4's sixteen proper notes suggest the proper is the unit that was actually recorded, but sixteen is a small sample and they come from two masses read with unusual care.
4. **If the inheritance hides more than it saves.** §5.2's whole cost argument rests on one default covering 2,137 propers. If the true distribution is flatter — if the seasonal, Common and sanctoral passes each used a different method, so that a third of the corpus overrides — then the field is closer to a hand-typed restatement than to `psalm_numbering`, and (d) starts to look less unreasonable. **This was not measured**, because the notes are prose; measuring it is the first step of §9 and could cancel §5.2.
5. **If residence is flipped for reasons this file does not weigh.** §4.4 argues the flip buys nothing until pre-1955 text is read. If the flip has a value not measured here — a reader-facing one, or one that unblocks the pre-1955 sidecar of §4.3 — then precondition 0 becomes urgent again and the recommendation to build for the rights claim instead is merely a different order of the same work.
6. **If `translations` was left out of `PROPER_FIELDS` deliberately.** §1.1 reads it as an oversight that blocks the sidecar's own merge instruction. If it is instead a deliberate gate — translations may not land inline until the sidecar's rules are ported — then the reading is wrong, though the consequence for this proposal is unchanged: `attested_in` needs the same door opened.
7. **If the English half of precondition 0 is weaker than §1.2 makes it.** 176 of 242 entries are collated against page images; 66 rest on a detector and have never been seen on a page, which the file's own `verification` states plainly. If "records which printings were read for it" is read to mean *read on a page*, then the English half is 176 of 337 and not 242, and the claim in §2.1 should be narrowed. It would still not be zero.

---

## 9. If this is accepted, the order of work

Steps 1 and 2 change no schema and either may return an answer that cancels 4.

1. **Measure the distribution.** Read the 231 mass notes and classify each into the method it names. This is the check §8.4 asks for and it decides whether §5.2's inheritance is cheap or a fiction. It costs one reading of one file.
2. **Correct the two records that are wrong now.** `../recensions.md` §6 item 0 and §8.4, to say that per-proper attestation exists for the English and not for the Latin; and both statements of 2,312, to reference the derived census rather than restate it. Do this whether or not anything else here is accepted.
3. **Register the CMAA facsimile as a witness** (§5.1). Required under every design, independent of all of it.
4. **Adopt §5.2 and §5.3**, header first, then the masses that override, then the sixteen propers — in that order, so that the check can be turned on before the overrides land and the overrides are then written against a failing gate rather than into silence.
5. **Derive the Latin comparison** on the model of `witness_verdict`, for the 28 masses read against two scans. This is where the mechanism pays for itself, and it should not be deferred to the flip.
6. **Leave residence unflipped**, and record §4.4 as the reason beside §8.4's, so that a later session finds two reasons and not one.
