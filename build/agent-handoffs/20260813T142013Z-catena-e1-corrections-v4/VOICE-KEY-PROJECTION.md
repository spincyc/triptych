# The exact voice-key projection

## The defect, stated exactly

V3 answered *"is this voice supported?"* with *"does any held book carry this
language?"*, reading `index.held[].languages`. Those are different questions,
and the corpus is a case where they differ.

Greek stands in this corpus **only as an original**. `grc` is therefore in the
language inventory, and V3 concluded from that inventory that
`voice=translation:grc` named something the corpus holds. It does not. The
page then rendered `Greek translation — none here`, which is a claim about
holdings — it says a Greek translation exists somewhere and merely not on this
chapter. Nothing in the corpus supports it.

The inference V3 made was:

    Greek exists somewhere in the holdings
    therefore translation:grc is supported

That is false. A language inventory cannot tell an original from a
translation, which is precisely the distinction the voice axis exists to make.

## Three questions that are not one question

| Question | Answered from | Failing it means |
| --- | --- | --- |
| Is the key **well formed**? | the closed URL grammar | malformed address |
| Is the key **supported**? | the exact voice keys the corpus holds | unsupported voice — fails closed |
| Is it **held on this chapter**? | the chapter spine, after it loads | a true "none here" |

V3 collapsed the second into a language test. V4 answers it exactly, and the
third is untouched and still works.

## What the corpus actually holds

Counted over every tracked chapter spine, the `(voice, language)` **source
pairs** are exactly four:

| source pair | source entries |
| --- | --- |
| `original` + `la` | 210 |
| `original` + `grc` | 3 |
| `translation` + `en` | 13 |
| `translation` + `la` | 1 |

**There is no `translation` + `grc`. There are zero Greek translations.**

The route composes a selectable key from a source with `voiceKey`, which
collapses every original to the bare key `original` — a reader asking for the
author's own language asks one question, not one per language. Projecting the
four pairs through it gives exactly three keys:

| route voice key | source entries behind it |
| --- | --- |
| `original` | 213 |
| `translation:en` | 13 |
| `translation:la` | 1 |

Both statements are recorded because the review states the vocabulary as four
source pairs and the implementation works in three route keys. They are the
same fact seen through `voiceKey`, and a reviewer can check either.

## Where the truth now lives

`scripts/_catena.py` accumulates the projected key of every fragment row as it
writes the structure, and emits the sorted set as a top-level `voices` array
of the catena index:

```json
"voices": ["original", "translation:en", "translation:la"]
```

The generator already carried `voice` on every row — it derives it from the
work record and the edition record together and refuses a fragment whose two
independent signals disagree — so this publishes an existing derivation rather
than inventing one. It is **counted, not declared**: no list of keys is
hard-coded anywhere, and a corpus that acquires a Greek translation tomorrow
gets `translation:grc` in this array from the next generation, with no code
change.

The route reads it where it already reads the index:

```js
} else if (!(index.voices || []).includes(voice)) {
  flag('voice', voice, 'is not a voice this corpus holds');
}
```

The whole key is compared against whole keys. No language is extracted, and no
holding is inferred from one.

## Why the index, and not somewhere else

The address is judged in `hashProblems`, which runs on arrival when exactly
three files have been fetched: the catena index, the bibles manifest and the
paragraph index. The chapter spine — the only other place exact voices exist —
is fetched later, by the render, and is chapter-scoped in any case. A test
pins the first-load fetch list, so no new request may be added.

That leaves the catena index as the only place a corpus-wide exact answer can
come from. The V3 independent review anticipated this and authorised it
explicitly: the V4 lane is *"explicitly authorized to add the exact Catena
voice-key projection"*, and the review lists the voice-key index seam as the
one generator/data seam this lane may enter. No other generator or data
ownership was taken; see `UNRESOLVED-BLOCKERS.md`.

## Behaviour, before and after

| address | V3 | V4 |
| --- | --- | --- |
| `voice=original` | honoured | honoured |
| `voice=translation:en` | honoured | honoured |
| `voice=translation:la` | honoured | honoured |
| `voice=translation:grc` | **rendered `Greek translation — none here`** | **fails closed**, names no holding |
| `voice=translation:de` | fails closed | fails closed |
| `voice=translation:zz` | fails closed | fails closed |
| `voice=translation:EN` | malformed | malformed |
| `voice=translation:` | malformed | malformed |
| `voice=translation:en:extra` | malformed | malformed |
| Genesis 10 + `translation:en` | `English translation — none here` | **unchanged** — still `English translation — none here` |

The last row is the control the review named, and it is the point of the
exercise: `translation:en` is supported corpus-wide and absent from Genesis
10, so "none here" is a true statement about a chapter. That behaviour is
preserved exactly. Only the false version of it was removed.

## One deliberate consequence, disclosed

The sample corpus reachable at `?data=fixture` predates the voice axis: its
chapter files carry no `sources` map and **no `voice` field at all**, and its
index carries no `voices` array. Under V4 a `voice=` key therefore fails
closed there.

This is a behaviour change, and it is the correct one. Previously that corpus
answered `voice=translation:en` with `English translation — none here` — the
same invented-holding claim, made about a corpus that has no voice axis to
hold anything on. Failing closed says the sample corpus does not support the
voice axis, which is true. The fixture is not regenerated by this lane; that
would be generator/data work beyond the authorised seam.
