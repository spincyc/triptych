# The row that asked, and what that closes

## 1. The findings, and what they actually were

The V13 independent review accepted the architecture and refused six things.
Stated as the review stated them:

1. **`src/web/browser/catena/catena-model.js` reads raw `record.unfetched` during projection; later
   `src/web/browser/catena/catena.js` rereads raw `file.unfetched`; the second raw value can replace
   the accepted projected file/chapter with `null` / `NO_CHAPTER`.** Its probe
   answered `undefined` on the first read and `"FORGED RAW REREAD"` on the
   second, and observed `unreadable:false`, two reads, and the forged later
   value taken.
2. **"Same instance" is not actually proved with `===`.** The harness
   independently called `chapterProjection(file)` beside each consumer and
   compared `.id` strings.
3. **The tally is not recorded as an independent consumer.** It was collapsed
   into the rows.
4. **Request ownership is reconstructed from path strings** rather than from
   actual row identity.
5. **Nested source accessors can still produce internally contradictory
   projected semantics** — `sources["1"]` as an own getter declined for
   fragment provenance and invoked for projected voices and editions.
6. **The top-level projection is frozen; row objects may remain mutable.**

Beside them the review named two evidence defects: the member-list scenario was
not structural, and "13 parent-failing methods" was arithmetically true and
read as thirteen independent semantic closures.

The first finding is the load-bearing one and it is worth being exact about
what it costs. The chapter that reaches the second read has already been
approved: `spineUnreadable` projected it, the projection said readable, and
`chapterFile` returned the record itself. The page then reads the same raw name
again and, on a truthy answer, sets `file = null`. Every consumer after that
line resolves `NO_CHAPTER`: the rows go, the recorded refusal goes, the voice
control empties, the tally becomes "The commentary record did not load", and
the reader is shown a sentence with the payload's own string inside it. Nothing
approved any of that. The reviewed parent does exactly this when replayed
against this lane's walking case, and the sentence it prints is *"its record
(FORGED RAW REREAD) could not be read"*.

## 2. The contract

**One raw chapter member is read once, and the projection carries what it
said.** `normalizeChapter` reads `fragments`, `sources`, `refusals`,
`unfetched`, `blocked` and `leads` into locals exactly once and `text_prefix`
through the V12 snapshot, and the projection now carries `unfetched` as the
normalized value the page used to normalize for itself. `src/web/browser/catena/catena.js` reads
`M.chapterUnfetched(file)`; the raw member is not read there or anywhere else
after projection. The audit is asked of the source text as well as of the
behaviour: no `file.<member>` read, no `bag(file)`, and no property read of
`unfetched` off anything in the page.

**The member inventory is an inventory, taken once.** `Array.isArray` is true
of a proxy over a real array, so the raw `fragments` can answer "which members"
and "how many" independently. One `Array.prototype.slice.call` reads the length
once and each index once, and every question afterwards is put to the array
this file owns.

**Every nested source is normalized once, by descriptor, under one rule.** An
own accessor at a nested key or on a nested field is never invoked — not by the
voices and editions walk, not by a fragment row, not by anybody — and a key
whose value is not a plain record makes the chapter unreadable, whole, the same
way an unreadable `sources` root already did. `translators` is normalized and
frozen per edition, because it is the one shared field that is a container.

**The projection graph is frozen as deep as it is trusted**, and the rows,
leads and blocked entries are sealed where they are made rather than where
someone remembered to seal them. `fragmentRow`, `leadRow` and `blockedRow` all
freeze what they return, so an exported caller and the page hold one contract.

**A request is owned by the row that asked for it.** The page hands the model a
row; the model resolves the address through the row's own identity and records
the owning row and projection at that moment. A row no projection of this file
made resolves no address at all.

## 3. Identity is observed, not recomputed

The review's objection to V13's identity proof was precise and it is the reason
this lane did not simply assert harder. A harness that calls
`chapterProjection(file)` next to a consumer learns what the memo returns; it
does not learn what the consumer received.

`chapterWitness` installs a recorder and returns the one it replaced. Every
model entry point that answers from a projection hands the recorder the exact
object it is about to read, at the moment it reads it, and the recorder is
given no way to change what is returned; with none installed the call is one
`if` on a `null`. The **authoritative** reference is the one recorded inside
`chapterProjection`, immediately after the projection is created and memoized —
so the comparison is against the object this file made, not against the answer
to a second question. Identity is decided in the same realm by a `Map` keyed on
the object, which is `===` for object keys. The integers in the journals are
labels for that decision and not the decision.

Ten consumers are on the roster: readability, `unfetched`, tally, rows, voices,
blocked, leads, refusal, the request, and provenance. The roster is checked
against every consumer name the whole replay actually produced, so a consumer a
later lane forgets to route through the projection appears as a name the run
made and the roster does not carry.

One honesty note the roster forces. Where readability refuses the served
record, `chapterFile` substitutes the page's own `{ unfetched: <path> }`
marker, and that marker is a **different chapter with its own projection**.
Readability names the record it refused; every consumer downstream names the
marker. This lane asserts that shape rather than claiming one identity across
two.

## 4. What the shape costs

The nested-source rule is fail-closed and therefore wider than the defect: an
own accessor at a source key now makes the chapter unreadable, where V13
rendered it with an empty provenance line under an edition whose voice the
control offered. That trade is the page-wide contamination policy the V12
review accepted as a design, applied one level down. No tracked corpus record
uses an accessor.

`textAsked` refuses an address to a row no projection made, which closes
ownership and also means a **copy** of a projected row resolves nothing — the
replay harness's own `forceRow` copies, and that is exactly why the rule is
worth having.

The mutation half of the immutability probe runs for one scenario, because at
the parent an unfrozen entry really moves and a probe running everywhere would
plant its own evidence in the file it is reporting on.

## 5. Why `src/web/browser/catena/catena.js` is nearly untouched

Four statements. `sound(bag(file).unfetched)` becomes `M.chapterUnfetched(file)`
and the `file = null` line goes; `M.chapterFragments(file).length` becomes
`M.chapterTally(file)`; and `fragmentText(fragment.text_path)` becomes
`fragmentText(fragment)`, which asks the model for the address through the row.
The page is **smaller** than the parent left it at 12,972 gzipped whole against
a 13,000 ceiling, and identical at 7,546 stripped. Every semantic addition went
into the model, which carries no ceiling — and the model's growth is disclosed
rather than presented as unchanged load.

## 6. What proves it

Every claim above is asserted at a production sink in
`tools/tests/test_catena_wave_1.py` and replayed at both endpoints. See
`checks.txt` for the exact commands and figures, and the per-attempt transcript directories under `logs/` for the
transcripts. The parent replay is the load-bearing artefact: 43 failures across
29 methods at the exact reviewed head, with the read counts, the invocation
counts and the rendered sentences recorded on both sides.

## 7. What is not closed here

`LIMITATIONS.md` states every boundary; `UNRESOLVED-BLOCKERS.md` states every
finding left open with its owner. The two that bear directly on this claim:
six of the seven walked chapter members and three of the five member-structure
effects **already held at the parent** — they are pinned here as coverage with
steady controls, not claimed as closures — and the V13 review this lane answers
has no published branch or commit, so its account of the disposition cannot be
checked against the review itself.
