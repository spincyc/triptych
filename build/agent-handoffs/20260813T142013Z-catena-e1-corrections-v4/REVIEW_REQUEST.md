# Review request — Catena E1 correction V4

Review **`e40720d5d622e8b0528b8c714cc5caee0b21cee3`** on
`impl/catena-wave-1-e1-corrections-v4`, against parent
`f2c9bc49dd29499734193b264ba9da21304b27f1`, answering review
`9b1c23680c8da6b9a83bb7fb8ca689fbf9d2004c`.

Read `HANDOFF.md` first. Everything below is either a question this lane
cannot answer about itself, or a place where it made a judgment a reviewer
should test.

## Questions this lane cannot answer for itself

### 1. Is three route keys the right vocabulary, or should the index publish four source pairs?

The review states the vocabulary as four `(voice, language)` **source pairs**:
`original:grc`, `original:la`, `translation:en`, `translation:la`. The route's
own `voiceKey` collapses every original to bare `original`, so the corpus
projects onto **three route keys**. This lane published the three, because
those are the strings a URL can actually carry and the strings the route
compares.

The consequence is that `original:grc` is **not** an accepted URL value — it
never was, and the closed grammar refuses it as self-contradictory. If the
review intended the index to publish the four pairs, or intended
`original:grc` to become addressable, this is wrong and is the place to say
so. Both statements are recorded in `VOICE-KEY-PROJECTION.md` so either can be
checked.

### 2. A test forbids the `src/web/data/` change the review authorised

`test_candidate_does_not_leak_fixture_or_discovery_records` asserts that a
candidate branch changes **nothing** under `src/web/data/`. The review
explicitly authorised exactly one such change — the voice-key index seam. Both
cannot hold.

The test already failed at the base for unrelated propers reasons, so this is
not a new failure; V4 lengthens its list by two entries. This lane did not
touch the test, because it belongs to the liturgy day-reader lane. **A
reviewer should decide** whether that test needs an exemption for the
authorised seam, or whether the seam should have been carried differently.

### 3. Is failing closed under `?data=fixture` acceptable?

The sample corpus predates the voice axis: no `sources`, no `voice` field, no
`voices` array. Under V4 a `voice=` key therefore fails closed there, where
previously it rendered `English translation — none here`.

This lane judged that an improvement — the old behaviour was the same
invented-holding claim, about a corpus with no voice axis at all — and did not
regenerate the fixture, because that is generator/data work beyond the
authorised seam. **If the fixture should instead be regenerated, that is a
separate authorisation.**

### 4. Is Isaiah 8 acceptable to carry?

Regenerating restored a chapter file and a `present` entry that were missing
from committed data. Verified pre-existing: the unmodified generator at
`f2c9bc49` produces the same output. Kept rather than reverted, on the
reasoning in `HANDOFF.md`. A reviewer may prefer it split into its own lane.

### 5. Are the reopened deliverables this lane's to close?

The reviewer set `unsupported-voice-distinguished-from-shape` and
`displayed-provenance-typed` to `open`. This lane believes both criteria are
now met and **left them open anyway**, because marking them `pass` would be
self-certification. If the ledger is meant to record implementation state
rather than review state, they should be flipped and this lane got it wrong.

## Where to press hardest

- **`catena-model.js`.** The V3 lane kept it byte-identical; this lane changed
  it on an explicit maintainer decision, for the byte and ownership reasons in
  `HANDOFF.md`. `MODEL_SHA256` is updated and a fourth release binding is
  stale. If the model should have stayed frozen, the typed boundary does not
  fit anywhere this lane is allowed to put it, and that is the finding.
- **The refusal copy.** The review asked for neutral umbrella copy or a typed
  unsupported reason, because *"address could not be read"* is imprecise for a
  parsed-but-unsupported value. **This lane did not change that copy.** The
  detail line does name the exact reason (`voice=translation:grc is not a
  voice this corpus holds`), and the malformed and unsupported refusals are
  distinguishable by their detail text — but the heading and the status line
  are still shared. This is a **known gap against the review**, disclosed
  rather than quietly closed.
- **Missing captures.** The review asked for a screenshot of the visible
  refusal change and a conditional-source omission rationale. **Neither is
  included**: no display was available to this session (see
  `AT-LIMITATION.md`). The refusal change is evidenced structurally, by
  replayed DOM projections, not visually. This is a **second known gap**.
- **The new regressions themselves.** Seventeen tests were added. They were
  checked against the V3 implementation and fail there — one of them
  catastrophically. A test that passes both ways would prove nothing, so
  please confirm the negative control rather than trusting this note.
- **Whether one boundary is really one boundary.** The claim is that four
  questions in the model cover nine sinks. Look for a tenth sink that should
  have been covered and was not — `renderChapter`'s verse values are one this
  lane saw and deliberately left alone, because they are shared with the
  scripture page.

## What this lane did not touch

`src/web/browser/shared/browser-core.js`, `src/web/browser/catena/catena.css`,
`src/web/browser/catena/index.html`, release records, the common gate,
protected Liturgy, PDFs, and every generator/data surface beyond the
authorised voice-key seam. Verified in `checks.txt`.

## Reproducing

Every command, with its exit status, is in `checks.txt`. The sealer is
`logs/sanitize-and-seal.py`; running it against this package with
`--check-only` should report zero hits, and running it against the V3 package
should refuse to seal.
