# The refusal copy: before, after, and why

## What the review required

The V3 independent review at `9b1c23680c8da6b9a83bb7fb8ca689fbf9d2004c` carries
the requirement in one place only: the `#### Finding matrix` row keyed
**"Fail-closed presentation"** in `guidance/corpus-browser-roadmap.md`. Verbatim:

> **Mechanism passes, classifier/copy need correction.** Properly classified
> unsupported values preserve the written URL, fetch no chapter, clear stale
> content, and offer recovery. Reusing one styled error surface is acceptable,
> but "address could not be read" is imprecise for a parsed unsupported value.
> Keep the component and reason-specific detail; use neutral umbrella copy or a
> typed unsupported reason.

Two things follow, and this lane did both:

1. the **component stays** — one styled error surface is explicitly acceptable;
2. the **shared umbrella** must stop diagnosing, while the **reason-specific
   detail stays** on the value it belongs to.

## What changed

Three string literals in `src/web/browser/catena/catena.js`, inside
`renderInvalid`. Nothing else in production changed.

| Sink | Line | Before | After |
| --- | --- | --- | --- |
| reference line | 696 | `Address not recognised` | `Address not used` |
| error heading | 700 | `This address names what the page does not have` | `This address cannot be used as written` |
| status write (`aria-live`) | 717 | `The address could not be read; its invalid values are shown, unchanged.` | `The address is unchanged; the values not used are listed.` |

## Why each was non-neutral, against the review's own tests

| Before | Defect |
| --- | --- |
| `The address could not be read; ...` | **Overstates what the system knows.** Untrue of `voice=translation:grc`, which parses cleanly and is merely unsupported. This is the exact string the reviewer quoted. `its invalid values` additionally **implies blame**, labelling the reader's text invalid when the grammar accepted it. |
| `This address names what the page does not have` | **Implies an unsupported holdings fact.** It asserts a holdings negative over every fail-closed arrival — including addresses refused on *grammar* (`translation:EN`, `translation:en:extra`, a key cited twice), where nothing about holdings has been established. |
| `Address not recognised` | **Overstates what the system knows.** A parsed-but-unsupported value *was* recognised; only its support was refused. |

## Why the replacements are neutral

- They **describe the state** — the address was not used; it is unchanged; the
  values not used are listed — and assert nothing about why.
- They **do not imply blame**: no value is called invalid, and no fault is
  located in the reader.
- They **claim no holdings**: "cannot be used as written" is a statement about
  this page's use of the address, not about what the corpus has.
- They **do not overstate**: they make no claim of unreadability.
- They are **consistent with the E0 typed-state model**: the `data-state="error"`
  attribute, the component, the recovery affordance and the per-value detail rows
  are unchanged, so `error` still carries its own typed identity and the typed
  reason still distinguishes malformed from unsupported.

The reason survives exactly where the review asked it to:

    voice=translation:grc   is not a voice this corpus holds       (unsupported)
    voice=translation:EN    is not a voice — "original", or ...    (malformed)

## What was deliberately NOT changed

The page carries other phrasing that a broad editorial pass might question — the
acquisition-list heading, the "held, not renderable yet" wording, the absence
summaries, the numbering-refusal sentence, the static prose in `index.html`.
**None of it was touched.** The review asked for the fail-closed umbrella, and
this lane is a micro-correction; general wording cleanup is out of scope and
would have made the diff unreviewable. This is recorded as a reviewer question
rather than silently decided.

Layout, hierarchy, CSS, the recovery link, the focus contract, the route and the
status-write count are all unchanged.

## The regression

`TypedStateTest.test_the_shared_refusal_umbrella_stays_neutral`
(`tools/tests/test_catena_wave_1.py`) is the new pin. It reads the **umbrella
only** — reference line, heading and status writes joined — for both an
unsupported voice and a malformed address, and asserts that none of
`could not be read`, `not recognised`, `invalid`, `does not have`, `unreadable`
reappears there, while still requiring the typed per-value reason to be present.

It is a real pin, not a tautology: restoring any one of the three old strings
fails it. Demonstrated, with the old heading restored:

    AssertionError: 'does not have' unexpectedly found in
    'This address names what the page does not have Address not used
     The address is unchanged; the values not used are listed.'
     : 'does not have' diagnoses in shared copy

Seven existing assertions moved to the accepted wording, in lockstep:
`test_catena_wave_1.py` lines 1612, 1617, 2270, 2453, 2476, 2497, 3819.
