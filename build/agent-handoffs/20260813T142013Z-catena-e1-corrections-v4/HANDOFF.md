# Catena E1 correction V4 — immutable handoff

## Identities

| | |
| --- | --- |
| Branch | `impl/catena-wave-1-e1-corrections-v4` |
| Parent (the exact reviewed V3 head) | `f2c9bc49dd29499734193b264ba9da21304b27f1` |
| **V4 head** | `e40720d5d622e8b0528b8c714cc5caee0b21cee3` |
| Independent review answered | `9b1c23680c8da6b9a83bb7fb8ca689fbf9d2004c` — **CHANGES REQUIRED** |
| Superseded package | `20260812T184146Z-catena-e1-corrections-v3`, unchanged and unmutated |

Three commits, from the exact reviewed head. Not merged, not deployed, no
release record re-signed.

## What the review found, and what was done

### 1. The voice classifier was wrong

`index.held[].languages` is a language inventory. Support is a question about
voices. The corpus is exactly the case where they differ: Greek stands here
**only as an original**, so `grc` is in the inventory, and V3 concluded a Greek
translation was supported and rendered `Greek translation — none here` — a
claim that a Greek translation exists somewhere and merely not here. Nothing
supports it.

The generator now counts the voice keys the corpus holds, composed the way the
route composes them, and writes them into the catena index:

```json
"voices": ["original", "translation:en", "translation:la"]
```

The route compares the whole key against that array. `translation:grc` fails
closed. Genesis 10 in `translation:en` still says "none here", because that
one is true. Full derivation, the four source pairs behind the three keys, and
the reason the index is the only possible home for the answer:
`VOICE-KEY-PROJECTION.md`.

### 2. The typed-presentation boundary was incomplete

Nine sinks, closed as **one boundary** rather than nine special cases. Four
questions — text, a list, a record, a number as the data carries it, and a
fact that may lawfully be a finite number — asked once in `catena-model.js` so
the page and the model cannot answer them differently.

| sink | before | after |
| --- | --- | --- |
| absence `author`, `work` | coerced; `[object Object]`, comma-joined | typed at the read |
| absence `reason` | a malformed record became the published legal reason | withheld; valid siblings stand |
| absence `partial` | truthiness moved a work between two legal claims | typed; count and prose are one value |
| translator container | a scalar string widened into a validated-looking attribution | a scalar is not a one-item list |
| translated language | reached the voice label, the control value, the written URL and DOM `lang` | never composes a key |
| malformed author filter | one unnamed, corpus-wide, unlabelled filter key | only named authors get a switch |
| structured extents | `Genesis [object Object]:1`, `Genesis undefined:undefined`, and a false chapter crossing | the book stands alone; no locus is guessed |
| terminal cleanup | a throw in the render tail stranded `aria-busy`, focus, the tally, the announcement and the route | the tail sits inside the funnel that already existed |

Evidence that these were real: against the V3 implementation, the V4 fixture
does not merely render wrongly — it throws `TypeError: blocked is not
iterable` and kills the replay outright.

### 3. The V3 package leaked, and its sanitizer said it did not

Replaced, not amended. `PRIVACY-AUDIT.md` records what leaked, the five
reasons the V3 sealer reported zero over it, and the proof that this package's
sealer refuses to seal the V3 package.

## Why `catena-model.js` changed

The V3 lane deliberately left it byte-identical, and `HANDOFF` discipline says
to justify entering it.

- `catena.js` had **one byte** of comment-stripped margin. The typed boundary
  does not fit inside it at any comment level — measured at +87 bytes over.
- The only other unbudgeted host is `shared/browser-core.js`, which is
  **B0/shared shell and forbidden** to this lane.
- Two of the nine findings — the translated-language metadata and the
  structured extents — live inside `voiceKey` and `formatExtent`. They cannot
  be closed from the page at all.

`catena-model.js` is Catena-owned, carries no byte ceiling, and its own pin
comment says a deliberate model change is a deliberate change to that literal.
`MODEL_SHA256` is updated deliberately. A **fourth** release binding is now
stale; no release record was re-signed. `shared/browser-core.js` is
byte-identical.

**This was an explicit maintainer decision**, taken before the work, with the
`catena.js`-only alternative and the stop-and-report alternative both on the
table.

## Measurements at the V4 head

| | base `f2c9bc49` | head | ceiling |
| --- | --- | --- | --- |
| focused Catena suite | 249, OK | **266, OK** | — |
| full discovery | 1,600 / 15 F / 13 E / 11 S | **1,617 / 14 F / 13 E / 11 S** | — |
| browser gate assertions | 2,290 — 1,836 / 226 / 228 | **2,290 — 1,836 / 226 / 228** | — |
| `make -k check` | exit 2, three failing targets | exit 2, **the same three** | — |
| promised deliverables | valid | valid, 29 tracked | — |
| `catena.css` whole | 7,629 | **7,629** | 8,000 |
| `catena.css` rules only | 2,676 | **2,676** | 2,700 |
| `catena.js` whole | 12,995 | **12,981** | 13,000 |
| `catena.js` code only | 8,799 | **8,749** | 8,800 |
| stale release bindings | 3 | **4** | — |

**No ceiling was raised.** Both JavaScript measures improved on V3, paid for
by simplifying the classifier and by moving pure helpers into the unbudgeted
model.

## Comparison, stated only as far as it was measured

- **No new failure identity.** See `BASELINE-COMPARISON.md`.
- The browser gate reports are **equal object for object** — assertion set,
  every status, every detail — with run metadata (`generatedAt`, `root`)
  excluded because they differ between any two runs by design. This is one of
  the few places the word applies literally, and it is used only here.
- **One pre-existing failure's detail is attributable to V4**: a day-reader
  test that forbids every `src/web/data/` change now lists the two catena data
  paths the authorised seam writes. Same identity, same status, longer list.
- One further detail difference is environment-sensitive (an absolute path in
  a message).
- The deliverable-count assertion the V3 review watched move from `28 != 23`
  to `29 != 23` **did not move again**. It reads `29 != 23` on both sides.
- One base-only failure is a clone-path artifact and is **not** claimed as a
  V4 fix.

## Isaiah 8

Regenerating the catena structure also writes
`src/web/data/structure/catena/27-is/008.json` and adds `8` to Isaiah's
`present` list. This is **pre-existing drift, discovered and not caused** by
this lane, and that was verified rather than assumed: the unmodified generator
at `f2c9bc49` produces the same output. The committed data was stale against
its own generator. It is kept because shipping data that contradicts the
generator would be worse, and because suppressing it would mean hand-editing
generator output.

## Not done, deliberately

E1 is **not** marked accepted and **not** marked integrable. The two
deliverables the reviewer reopened remain `open`: this lane believes it meets
them, but recording that in the ledger would be certifying its own work. No
separately owned blocker was fixed, and none disappeared — see
`UNRESOLVED-BLOCKERS.md`.

## The sole next action

A fresh independent review of this head and this package. This lane does not
review its own work, does not merge, does not deploy, and does not start
another master-plan lane.
