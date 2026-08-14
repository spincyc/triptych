# The typed presentation boundary — what V5 changed, and where

The V4.1 review found five blocking classes. They are one class, stated five
ways: **malformed or unsupported structured metadata must never become visible
semantics, counts, refusals, routing facts, bootstrap state or DOM attributes
through coercion or an unchecked collection shape.** V5 answers it once.

## Why the correction is in the model and not in the page

`catena.js` had **thirty gzipped bytes** of whole-file margin at the reviewed
head. A record boundary bought out of thirty bytes would have been a list of
one-off guards at each sink — which is the shape the review's own instruction
warns against, and the shape that produced these defects in the first place,
each sink having been fixed alone as it was found.

`catena-model.js` carries no ceiling. That is stated in the file itself and it
is why V4 moved `voiceKey` and `formatExtent` there. V5 continues that: the
model now owns the questions, and the page asks them.

The result is a page that is **smaller**: 8,734 → 8,363 stripped gzipped
bytes, 371 fewer. The whole-file figure rose 20 bytes, from 12,970 to 12,990,
because the boundary is explained where it lives. Both ceilings are unraised.

## The questions the model now owns

| Question | Answer | Refuses |
| --- | --- | --- |
| Is this text? | `sound` (V3) | a record, a list, a number, a flag, blank, whitespace |
| Is this a container? | `list` (V3) | a scalar pretending to be a one-item list |
| Is this a record? | `bag` (V3) | a list, a string |
| Did a number arrive? | `count` (V4) | `"1"`, `[1]` |
| **Is this a number this corpus counts by?** | **`whole` (V5)** | `0`, negatives, fractions, `1e21`, `"5"`, `[5]`, `true` |
| **Is this a language code?** | **`tongue` (V5)** | everything `sound` refuses, plus sound text that is not a subtag |
| **Is this a language code a VOICE KEY may carry?** | **`voiceLanguage` (V5)** | everything `tongue` refuses, plus anything outside the published route grammar |
| **Which members of this list are records?** | **`records` (V5)** | scalars, nulls, nested lists |

`tongue` and `voiceLanguage` are deliberately two questions. A `lang`
attribute may legitimately carry `en-GB`; a voice key may not, because the key
becomes a URL and the published route grammar is two or three lowercase
letters. Composed wider, the page issues a link it then refuses on the way back
in — the self-refusing address V4 fixed for records alone. One grammar, one
place: `hashProblems` now asks `M.voiceLanguage` too, so the route's own
validation and the key's composition cannot come to hold two opinions.

## The derivations that moved

Each of these was performed in the page by concatenation or truthiness over
raw record members. Each is now a named derivation with a typed answer.

| Derivation | What it decides | The defect it closes |
| --- | --- | --- |
| `canonBook` / `canonBooks` / `bookOf` | which members of the canon are books | a `null` member threw during startup, outside every funnel |
| `chapterPath` | a chapter spine's address — **or `''` for a real emptiness, or `null` for a record that cannot prove either** | `[object Object]` composed into a fetched URL; and "Nothing held here" inferred from an unreadable `present` list |
| `paragraphPath` | the paragraph layer's address, or none | the same coercion in the edition layer |
| `chapterLines` | the verses of a chapter, their words, and the marks that open them | `Number()` taking `" 3 "`, `"3.0"` and `"1e3"` for verses; raw values printed as Scripture; any truthy value opening a paragraph while counting as neither kind |
| `absenceRows` / `absenceCount` / `absenceSummary` | what each typed finding licenses the page to say | `not-surveyed` spoken as a publishing negative |

`chapterPath`'s three-valued answer is the load-bearing one. **"Nothing held
here" is a claim about the corpus.** A record this page cannot read establishes
no such claim, so a malformed `present` list or a malformed `path` reaches the
broken-record notice rather than the emptiness — because an absence inferred
from a parse failure is exactly the manufactured negative this boundary exists
to refuse.

## The absence findings, and why no taxonomy was invented

`scripts/_catena.py` closes `finding` at four values so that a fifth has to be
argued for rather than typed. Its own comment says they say different things:

```
# `none-published` is a fact about the world, `in-copyright` is a
# fact about the law, `partial-public-domain` is an offer this project has not
# taken, and `not-surveyed` is an admission.
```

The page read none of them. It classified a row by whether a `partial` string
happened to be attached, so everything that was not a partial became *no
English this project may publish* — including `not-surveyed`, whose entire
content is that nobody has looked. That is a closed claim about publishing
rights manufactured out of an admission of ignorance.

V5 maps the generator's four findings to what each licenses, adds no fifth,
and gives a finding it cannot read a clause that claims nothing:

| finding | the page may say |
| --- | --- |
| `none-published` | no English this project may publish |
| `in-copyright` | no English this project may publish |
| `partial-public-domain` | only a partly public domain English, not yet taken |
| `not-surveyed` | **has not been surveyed for English** |
| anything else | **has a finding this page cannot read** |

The last row is not a fifth finding. It is the page declining to speak for a
record it cannot read, and a row holding it enters no count.

## Three defects the review did not name

Found by writing the regressions the review required.

1. **The harness could not see the sink the review proved.** The replay shim
   stored `element.lang` as a plain JavaScript property. The HTML DOM reflects
   it into the content attribute, stringifying whatever it is given — which is
   why real Chromium showed `lang="[object Object]"` while every committed test
   passed. The shim now reflects `lang` exactly as it already reflected `id`,
   and `inspect()` projects every language attribute under the reading region
   for **every** scenario, so the cross-scenario coercion sweep covers DOM
   attributes and not only text.
2. **Sound text is not a language.** `sound()` passed the string
   `"not a language code"`, and the shared namer printed it straight back,
   uppercased, as a language chip. Non-emptiness was never the right question
   for a language; shape is.
3. **A silent return is not a terminal state.** Beneath the throw the review
   named, `render()` had a guard that returned quietly when the controls could
   not name a book — precisely the state a malformed canon produces. Reached
   that way it left `Loading…` standing with nothing said: the same dead end as
   the throw, invisible for the same reason. Both now reach `startFailed`.

## What was not weakened

One source-text assertion changed. `test_the_supported_set_is_read_from_the_index_not_from_the_key`
pinned the literal `!(index.voices || []).includes(voice)`; it now pins
`!list(index.voices).includes(voice)` and additionally asserts the old form is
absent. This is the **stricter** form of the same requirement: `|| []` let a
string `voices` answer `.includes` by substring, so `translation:e` passed
against a corpus holding only `translation:en`.

`MALFORMED_ABSENCES` was rebuilt rather than re-asserted. Not one of its rows
carried a `finding` at all, which is why it could manufacture four closed
negatives from four malformed neighbours — the review named this fixture
specifically. Its rows now put a real typed finding beside malformed siblings
and malformed findings beside sound ones, so the two questions are separable.
No assertion was relaxed to accommodate output; the fixture was corrected to
ask the question the review said it was failing to ask.

`MODEL_SHA256` was updated, deliberately, because `catena-model.js` changed
deliberately. That makes one release binding stale, unsigned, and correctly
fail-closed. It was not re-signed.
