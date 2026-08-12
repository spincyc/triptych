# LIMITATIONS — what this package does not establish

## 1. No real assistive-technology evidence

Unchanged from V2, and still **not met**. The V2 package's stated reason was
factually wrong and is corrected in `AT-LIMITATION.md`: an AT-SPI bus launcher
does exist and the bus was running. What is genuinely absent is a display, a
screen reader, a speech channel and a braille stack, so no AT session was
possible and none is claimed. Correcting the reason does not soften the
conclusion. The real-device-or-AT review remains a pre-release evidence
prerequisite owned outside this lane.

## 2. Stranger-key discard is proven by reading, not by test

`STRANGER-KEYS.md` §3 lists exactly which cases have tests and which do not.
Only the value-identical preservation case is pinned. The discard cases —
partial completion, reader action, the recovery link, and the `replaceState`
rewrite of a restored history entry — are read from the code and are labelled
as such. This lane deliberately added no test for them, because each would pin
URL behaviour the review did not ask to change. See `REVIEW_REQUEST.md` for the
question this raises.

## 3. The byte ceilings are one and five bytes clear, and cost prose

`src/web/browser/catena/catena.js` measures 12,995 of 13,000 whole-file and 8,799 of 8,800
comment-stripped, gzip-9 with `mtime=0`. Both ceilings are unraised and both
were paid for by deletion, not waiver. But the comment-stripped ceiling in
particular left no room for the explanatory prose this file's house style
otherwise carries, so:

- the new unsupported-voice branch carries **no comment**, where the three
  address checks beside it each carry one;
- `joinNames` was rewritten to `pop` rather than `slice`, which means it now
  **consumes the list it is given**. Both call sites hand it a freshly mapped
  array, so it is safe today; the two non-mutating forms measured were larger
  than the original and did not fit. Because a comment did not fit either, the
  precondition is pinned by a test —
  `FrozenContractTest.test_the_name_joiner_is_only_ever_handed_a_fresh_list`.

This is disclosed rather than presented as a style choice. A reviewer may
reasonably judge that a waiver for a slightly larger ceiling would buy back
clearer source; this lane had no authority to raise a ceiling and did not.

## 4. `translators` accepts a lone string as one name

The typed container rule is `[].concat(fragment.translators).filter(sound)`.
Objects, numbers, booleans, `null`, blank strings and array-like non-arrays all
yield no translator fact. A **bare string** — `"translators": "Eustathius Afer"`
rather than `["Eustathius Afer"]` — is treated as a one-item list and renders.

That is a deliberate widening of a case that previously **threw**, and it is
the reason the fix also removes the page-kill described in `HANDOFF.md` §7.2.
It is not a coercion: the value is real recorded text, presented under the
correct label. The stricter form (`Array.isArray`) was measured and did not fit
inside the unraised ceilings. Flagged for judgement in `REVIEW_REQUEST.md`.

## 5. The supported set is a language axis, not a voice axis

`index.held[].languages` records the languages the corpus holds fragments in,
regardless of voice. Its corpus-wide union is `en`, `grc`, `la`. The real voice
population is `original` (213), `translation:en` (13), `translation:la` (1) —
there is no Greek *translation* anywhere.

So `voice=translation:grc` is **accepted** as supported, and then correctly
reports that this chapter holds none. That claim is true — the corpus does hold
Greek, and holds no Greek translation — but it is a weaker check than a true
voice-axis check would be. A voice-axis set cannot be used here: the only true
voice enumeration, `M.chapterVoices(file)`, is derived from the chapter spine,
which is not fetched until after address validation, and reaching for it would
add a request that the pinned six-request first load forbids. The honest claim
this check supports is "a language this corpus holds commentary in", and the
refusal note says exactly that: *is not a voice this corpus holds*.

## 6. No capture set

This package carries no screenshots, PDFs or accessibility-tree captures. The
four corrections are a URL-validation branch, a rendering-type discipline and
two prose corrections; no new visual state was introduced, and every behavioural
claim here is pinned by the focused suite instead. The V2 package's capture set
remains the visual evidence of record for the states it covers, and remains
accurate for them, because `src/web/browser/catena/catena.css` and `src/web/browser/catena/index.html` are byte-identical at
this head.

## 7. Fixture-driven provenance evidence

The tracked corpus types every provenance field it carries, and no tracked
payload is malformed. The coercion the review found can therefore only be shown
against a **labelled synthetic fixture**, `UNTYPED_PROVENANCE_FIXTURE`. Nothing
in this package asserts the corpus contains malformed provenance; the fixture
exists to prove the renderer's discipline, not to describe the data.

## 8. What this package does not touch, and does not establish

The deliberately unsigned Catena release binding still fails closed and was not
repaired — see `UNRESOLVED-BLOCKERS.md`. No generator, generated data, release
record, common browser gate, B0/shared shell, protected Liturgy path or PDF was
changed. The pre-existing `check-tool-registry` and `check-examples` failures
are inherited and unrelated. Nothing here is acceptance, integration, merge,
re-signing or deployment, and this package is not acceptance by itself.
