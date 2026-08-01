# Recensions: one rite, held in more than one state

A design study for carrying more than one state of the same rite — the Roman
Missal as it stood before the Holy Week reform of 1955, and the 1962 typical
edition as a revision applied on top of it — without holding two copies of the
eighty-seven per cent they share.

**The base is the pre-1955 book.** That is the maintainer's ruling of
2026-07-31, and it is the direction the rite actually ran: the older book is not
a variant of the newer one, and deriving an ancestor from its descendant would
invert the history the whole apparatus exists to keep straight. A third state —
the reformed Holy Week of 1956 to 1960 — then sits between them rather than
having to be squeezed alongside.

The base is chosen on that ground and on no other. It is a claim about which
book came first, not about which is better, and this document takes no position
on the second question — see `editorial.md`, "No side in what is described".

**Nothing here has been built.** It is written now, before any data moves,
because the shape is cheap to choose and expensive to change once a second
calendar exists in the tree.

## Evidence conventions

- **[verified]** — measured during this study against tracked artifacts.
- **[sourced]** — reported from an external document, cited.
- **[inferred]** — reasoned from the above. Flagged wherever it matters.

---

## 1. This is already a defect, not only a feature

The repository is **already collating a 1962 book against a pre-1955 witness and
recording the differences as errors.**

The English orations are read against the 1861 Cummiskey printing, which is a
pre-reform book. On 2026-07-31 two entries in
`roman-1962-proper-translations-v1.toml` recorded prayers as *absent from the
witness* when the witness prints them [verified]. The Easter Vigil's
postcommunion was one:

> it is printed on p. 329 as the Vespers prayer *Spiritum*, because the pre-1955
> Holy Saturday Mass **has no postcommunion**.

Nothing was wrong with the witness or the transcription. A matcher keyed on
`(mass, proper-name)` asks a pre-reform book for a slot the reform created, gets
nothing, and writes down an absence. Four further `untranslated` rows are now
flagged *untested* rather than settled, precisely because two rows with identical
wording fell the moment anyone looked [verified].

So the pivot is not a feature request that can wait. It is the missing
distinction that turns a good witness into a generator of phantom absences.

> **Rule 1.** A witness is matched against the recension it belongs to. Where the
> two differ in structure and not merely in wording, an absence in one is not
> evidence about the other.

---

## 2. The mechanics are already free; the duplication is the whole problem

`scripts/_calendars.partition` discovers calendars by walking
`src/sources/calendars/*/` and keying on the directory name [verified]. Nothing
is fixed at two. A third directory would be found by `calendar-days`,
`calendar-spine`, `calendar-rubrics`, the census, the harvest corpus and the
browser's missal control without any of them being told.

What is not free is the data. Measured against `roman-1962/propers.yaml`
[verified]:

| | count |
| --- | --- |
| masses | 460 |
| propers | 1,378 |
| Passiontide and Holy Week | 16 masses, **172 propers** |
| the four Triduum liturgies alone | 91 propers |

**A pre-1955 recension departs in roughly 12.5 per cent of the book.** Copying
1,378 propers to change 172 leaves 1,206 duplicated, and this repository's
standing rule exists because copies drift: on one day it found three disagreeing
copies of one census, an edition string written out four times, a README
restating its own table differently, and a release manifest attesting a hash that
had never matched any committed file [verified]. A second full calendar would be
the largest such copy in the tree.

> **Rule 2.** A recension is stored as its **departures from a base**, never as a
> second copy of the base.

### The text we hold was read from the newer book, and that does not have to move

Making the pre-1955 book the base raises an obvious objection: all 1,378 propers
now in the tree were transcribed from the 1962 typical edition and collated
against it, and relabelling them as though they had been read from a pre-reform
printing would be a false provenance claim — the exact defect class this
repository spends its effort catching.

The objection dissolves once **attestation is separated from residence**. A text
lives once, in the base. What witnesses attest it is a separate fact, recorded
per witness, and one text may be attested by many books — which is the ordinary
case, since the whole point is that most of the missal did not change.

So a proper in the base carries the witnesses that have actually been read for
it, and today most of them will say *1962 typical edition, collated* and nothing
else. **That is a true statement, not a false one.** It says the text stands in
the base because the rite had it before 1955, and that the only printing anyone
here has checked it against is the 1962 one.

Three consequences make this the practical shape as well as the honest one:

- **The base can be declared now, with nothing transcribed.** Populating it is
  not a precondition; it is the work.
- **Transcribing a pre-1955 witness ADDS attestation** where the text agrees and
  **creates a departure** where it does not. Neither rewrites what is there.
- **A reader can always be told what was checked.** "Attested in both printings"
  and "attested only in the 1962 printing" are different claims, and a page that
  cannot tell them apart is claiming the stronger one for free.

> **Rule 2a.** A text resides in the base. Its witnesses are recorded per
> witness, and a text attested by only one printing says so. No transcription is
> ever re-attributed to a book nobody read it from.

---

## 3. The shape is one this repository already chose once

`guidance/versification.md` §8.0 settles the projection: a set of rules rather
than a set of verses, where the default rule is identity and **writes no row**,
so the size of the projection measures how far an edition sits from the canon
rather than how large the edition is.

A recension is the same instrument pointed at a calendar. It declares its base
and records only where it departs, so the shared year has exactly one home and
the diff *is* the document — about 172 rows instead of 1,378, and no possibility
of the shared 1,206 disagreeing with itself.

The vocabulary a departure needs is wider than the projection's, because a
calendar can differ in ways a numbering cannot:

| Kind | What it says |
| --- | --- |
| `absent` | the base has this mass or proper; this recension does not |
| `added` | this recension has one the base does not |
| `replaced` | both have it and the text differs |
| `renamed` | the same formulary under another name or key |
| `moved` | the same liturgy on another day, or at another hour |
| `reslotted` | the same words in a different slot — the *Spiritum* case |
| `unrecorded` | known to differ, correspondence not established |

`reslotted` is the one this study exists to name. It is what generated the false
absences, and it is invisible to any matcher keyed on `(mass, proper-name)`
because both sides genuinely hold the words.

> **Rule 3.** A departure that cannot be established is recorded as
> `unrecorded` and resolves to nothing. It is never guessed, and it never
> silently falls back to the base.

---

## 4. Three things harder than the propers

The overlay is the easy part. These are not, and a plan that ignores them will
produce a recension that is right about words and wrong about the Mass.

**The rubrics differ, not only the texts.** The 1962 book follows the 1960
*Codex rubricarum*; a pre-1955 recension answers to the rubrics that preceded
Pius XII's reform. `rubrics.yaml` encodes precedence, and the fifteen solved
cases now genuinely enforce themselves against the browser's model — so a second
rubrics source needs its own solved cases, not a copy of the 1962 ones.

**The placements differ.** The reform moved the Easter Vigil from Saturday
morning to the night [sourced]. `calendar-days` computes placements from the
rules, so this is arithmetic and not text: a recension that overlays only
formularies would put the right words on the wrong day.

**The scope claim needs settling.** `roman-1962/propers.yaml` states in its own
conventions that *"the invariant Ordinary is out of scope; prefaces are not
recorded"* [verified]. The 1955 pivot reaches ceremonies — processions, the
blessing of fire, the order of the prophecies — more than it reaches orations.
A recension must say how far it claims to go, because a reader will otherwise
read silence as sameness.

> **Rule 4.** A recension declares its extent. Where it is silent, it is silent
> *because it has not been established*, and the page says so rather than
> serving the base as though it had been checked.

---

## 5. Naming, which is not cosmetic

"1955" names the reform, not the book, and the reform is a boundary rather than
an edition: the decree *Maxima Redemptionis* was promulgated in November 1955
and took effect in 1956 [sourced]. There are at least three states — the
pre-reform books, the 1956–1960 reformed Holy Week, and the 1962 typical edition
that carries the reform with further changes — and a two-way flag will be wrong
the first time someone asks about the middle one.

> **Rule 5.** A recension is named for the book it transcribes and dated by its
> own printing, exactly as the existing calendars are. It states which reform it
> stands before or after in prose, not in its identifier.

---

## 6. What must be true before any data moves

0. **Per-witness attestation on every proper, before anything is renamed.** This
   is Rule 2a and it comes first, because it is what lets the base be declared
   without moving a single transcription. Until a proper can say which printings
   have been read for it, declaring the pre-1955 book the base would make the
   tree assert a provenance nobody established.
1. The departure vocabulary of §3, with a validator, before the first row is
   written — the lesson `catena.md` records from the same position.
2. A check that fails when a recension's base does not exist, and when a
   departure names a mass or proper the base does not hold. A row pointing at
   nothing is the same defect as a citation that resolves wrongly.
3. `calendar-days` able to compute placements per recension, or an explicit
   statement that it cannot yet and that placements are the base's.
4. The witness question settled: `roman-1962-proper-translations-v1.toml` should
   record which recension each witness belongs to, so the matcher of Rule 1 has
   something to read. This is what makes the 1861 Cummiskey usable instead of
   misleading, and it is worth doing **before** more collation is done against
   it.

## 7. Landing it

The Triduum is both the part that is wanted and the part already producing wrong
results, and under a projection the rest of the year expresses no departure —
which is to say, no rows at all. So the first recension can be four liturgies
wide and still be correct about everything else, because it says nothing about
everything else.
