# Unknown keys in the address — exactly what happens, per path

The V3 independent review found this correction **substantively accurate** and
asked only for precision in the prose. No implementation change was required
and none was made: nothing in the V4 diff touches routing, history, or the
shared hash writer. This file restates the behaviour exactly and applies the
three corrections the review named.

## The rule

An unknown key is never validated, never rewritten, and never deliberately
preserved. It survives **exactly as long as Catena writes no route**, and is
discarded by the first canonical write. That is a consequence of when the page
writes, not a preservation feature, and it should not be described as one.

## Per path

| Arrival | Does Catena write? | What happens to an unknown key |
| --- | --- | --- |
| **Complete valid address** whose values already match the controls | No — `writeRoute` compares the four keys and returns before writing | **Survives.** The URL is left byte for byte as written |
| **Complete valid address spelled non-canonically** (e.g. `chapter=01`) | No — chapter is compared numerically, so `01` and `1` compare identical | **Survives**, and the non-canonical spelling survives with it |
| **Partial address** needing completion (a key absent, so a default is seeded) | Yes — a conditional `replaceState` of the canonical text | **Discarded** |
| **Invalid address** | No — `renderInvalid` deliberately does not call `writeRoute` | **Survives**, beside the error, with the reader's text unchanged |
| **Reader action** (a control, a step, an arrow) | Yes — a push through the shared writer | **Discarded** |

Unknown keys are not judged by the address check at all: it examines only
`book`, `chapter`, `bible` and `voice`, for multiplicity and for value. A
stranger key therefore never causes a refusal, and never prevents one.

## The three corrections the review asked for

**1. `replaceState` is conditional.** The V3 record described the completion
write as though it always used `replaceState`. It does not. The completion
path is taken only when the render answers an *arrival* **and**
`window.history.replaceState` exists; otherwise the write falls through to the
shared writer, which pushes. The distinction matters because the two differ in
whether a history entry is added.

**2. The canonical vocabulary is four keys, and may omit an empty voice.** The
V3 record described canonical output as a fixed four-key text. It is drawn
from a four-key vocabulary — `book`, `chapter`, `bible`, `voice` — but a pair
whose value is empty is skipped, by both the route's own text builder and the
shared writer. In practice this means **"Everything held" writes no `voice`
key at all**, so canonical output is commonly three keys, not four. A reviewer
comparing a written URL against a four-key template would find a false
mismatch.

**3. The shared writer does have bounded `?data=` evidence.** The V3 record
said the query string's survival across a hash write was unevidenced. That was
too strong. The shared writer assigns only `window.location.hash` and never
touches `location.search`, and there is a bounded test over the shared writer
driving `?data=fixture` through a write and asserting the search string is
still `?data=fixture` afterwards. The evidence is real but narrow: it covers
the shared writer under one query string, not every route or every parameter.

## What is deliberately not claimed

- Not that unknown keys are *preserved* — only that some paths do not write.
- Not that this behaviour is universal across the site. It is stated here for
  the Catena route and the shared writer it calls, and for nothing else.
- Not that any of it is a supported contract for callers. It is a description
  of what the code does today, pinned by the route tests, and a future
  canonicalisation decision could change it without breaking a promise.
