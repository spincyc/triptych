# Handoff, 2026-07-30

Written so the next agent starts from state rather than from scratch.
`PROJECT-WORK.md` remains the durable register; this is the session-specific
picture. The work ledger (`aiq list`) holds the task queue and is authoritative.

This file was rewritten during the second session of the day. The earlier
version described the tooling repair and the beginnings of the commentary
chain; git history has it. What follows is current.

## Nothing is committed

Twenty-eight paths are modified or new. `make check` exits 1, on purpose — see
the decisions below. Read those four before committing anything.

## The one theme

Almost everything found this session was the same bug in different clothes: a
reference that resolves **successfully and wrongly**. Not a crash, not a miss —
plausible text under a correct-looking citation. Five instances:

- `Joel 3:1-5` returned the valley of Josaphat instead of the outpoured spirit,
  and `Isaiah 9:5` the garments rolled in blood instead of the Child born to
  us. Neither appeared in any error count, because both resolved.
- Two hand-typed psalm ceilings gave Hebrew 10 and 115 the last verse of the
  Vulgate psalm hosting them, so impossible references passed the gate.
- The structure generator dropped every postconciliar cycle reading — 43% of
  citations — and looked fine.
- Mapping eBible's books by file position would have filed Ezekiel's text under
  Sirach, because it orders the deuterocanon differently from the Douay.
- The eleven mis-numbered antiphons, which resolved to real, wrong verses.

The standing lesson, now enforced in several places: **refuse rather than
guess**. A citation that cannot be resolved unambiguously carries a reason and
no text.

## Psalm numbering, settled

`scripts/_psalms.py` holds no correspondence data of its own. Every conversion,
bound and split is read from the verse-level concordance tracked with the
Challoner edition, which maps all 2528 psalm verses one to one. It is validated
on load: equal-length rows, 150 psalms per system, no gaps, no overlaps.

Conversions work in **printed** numbering, so Vulgate 115:10 is simply Hebrew
116:10. That removed `index-bible`'s `realign` flag, and the rebuilt index was
byte-identical, which is the proof the refactor changed no output.

`convert_range` rejoins pieces that abut within a chapter — the concordance
segments a psalm around its inscription and a range crossing that seam came
back as two — while a genuine division across chapters stays split.

## Bibles

| id | rights | numbering | psalter | publishable |
|---|---|---|---|---|
| douay-rheims | public-domain | vulgate | gallican | yes |
| clementine-vulgate | public-domain | vulgate | gallican | yes |
| knox | licensed | vulgate | gallican | **no** |

Knox came from `catholicbible.online`, operated by Baronius Press, the licensee
of the Westminster Diocese text — the only source whose rights chain can be
stated truthfully in an artifact record. `tools/knox-bible` retrieves it, and
every verb refuses a `--root` inside the repository. Its index and fragments
live outside the tree.

The index schema now carries `language` and `psalter`, because numbering alone
does not identify a psalter.

**Read this before adding a Latin psalter.** The 1962 Mass chants are older
than the Gallican psalter and disagree with it: the sixth Sunday after
Pentecost sings *protéctor salutárium Christi sui* where the Clementine reads
*protector salvationum*. Six divergences in two chants, verified against the
repo's own collated text. A Vulgate psalter gives confident near-misses on
chant incipits, which is worse than a miss. TASK-46 covers finding a corpus of
the sung text.

Not obtained: RNJB, NRSV, NABRE. No authorised bulk source exists for any of
them; `bible.usccb.org` blocks automated requests outright, and api.bible's
terms forbid populating a local database regardless. NRSV is also textually
wrong for this project — it fails the same citations the Douay does. NABRE is
the only English Bible whose versification matches the postconciliar citations.

## Web data

`guidance/web-data.md` is the contract. Four layers, each generated from the
one above and checked against it: canonical TSVs, per-chapter JSON fragments,
structure files with citations resolved into both numbering systems, and a
manifest naming only publishable editions.

The rule that matters: **file counts must be additive, never multiplicative**.
Adding a translation adds its fragments and changes nothing else. A future
reader will be tempted to pre-render mass-by-translation pages; the browser's
header comment argues against it at length.

Deploy assembly is TASK-49 and is specified but not built. The copy must be
driven from `bibles.json`, not from a directory listing — that is what keeps
Knox off the site.

## Reading plan

`src/sources/reading-plans/narrative-spine.yaml`: 357 readings, 12 periods,
tiers at 36 / 111 / 357 that partition rather than restate. Validated by
`tools/reading-plan` against real verse text.

Its period labels were originally Ascension's Great Adventure names, which
their terms forbid reproducing; they were replaced with the periodisation
ordinary in scholarship, and the file records that it happened. The selection
itself is independently derived from where four schemes overlap.

## The postconciliar numbering seam is not closed

This is the largest thing left, and it is bigger than it first looked.

The calendar cites in Nova Vulgata numbering; every bible in the library
follows the Vulgate division. `citation_divergences` in the postconciliar
calendar now corrects four books — Joel, Malachi, Isaiah 9 and 64, Micah 5 —
eleven citations in all, resolved by hand against the printed Douay because no
witness of the Nova Vulgata is tracked here to compile a concordance from. The
mechanism validates: an entry addressing no text fails the build, and so does
one naming a reference the calendar no longer cites.

**A further 23 citations still resolve to the wrong verses** — Exodus 22, Hosea
2 and 6, Esther 4, Wisdom 6 and 11, Sirach 3, 27 and 35, Mark 9, John 6, Acts
14 (TASK-51). Do not batch-correct them. They are three different problems: the
Sirach and Wisdom references follow the Greek the US Lectionary numbers rather
than the Nova Vulgata, and several John 6 antiphons are already
Clementine-numbered and correct while the readings beside them are not. Settle
which system each reference speaks before touching it.

Separately, **a citation naming a verse past the end of a chapter is silently
clamped rather than reported** (TASK-52). `Mark 4:41`, `1 Thessalonians 4:18`
and `Acts 7:60` are each dropped this way. They lose no text, because the
Vulgate merged those verses into their neighbours — but the mechanism is
silent. It cannot be fixed in the calendar, because the two Vulgate editions
disagree: the Douay ends 1 Thessalonians 4 at verse 17 and the Clementine at
18. It belongs in each edition's verse-aliases artifact.

## Where to pick up

Four decisions are yours and block nothing else:

- **TASK-41** — how the psalm-bound gate lands while the eleven antiphons
  stand. `make check` exits 1 until this is settled.
- **TASK-43** — are the Christmas octave days seasonal or saintly. The spine
  and the propers disagree; both are defensible.
- **TASK-48** — family membership for the new Clementine edition. Needs an
  audit date over reviewed prose, not a mechanical `refresh`.
- **TASK-49 / TASK-50** — deploy assembly, and teaching the browser to render
  reading plans as well as propers.

Then the ledger's p1 queue: TASK-17 (populate the discovery index — it is
empty, which is why the commentary corpus finds zero works), TASK-32, TASK-33's
follow-through, TASK-35, TASK-44.

## Verification

521 of 522 Python tests, 24 of 25 smoke tests, `source-library validate` clean,
`check-generation-metadata` clean. The single failure is TASK-48. Run all of
these before believing anything here:

```sh
python3 -m unittest discover -s tools/tests
for t in tests/tools/*.test; do "$t" >/dev/null || echo "FAIL $t"; done
tools/tpt source-library validate
make check
```
