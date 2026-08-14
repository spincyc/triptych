# How the captures were made, and how each pair is classified

## The instrument

`logs/probe-catena.mjs` starts its own static server over a built site, injects
the adversarial fixtures **in the response path** (the built artifact on disk is
never modified), drives headless Chromium over the DevTools Protocol, reads the
live DOM and the resource log, and captures PNGs. It was run twice with
identical fixtures: once over the parent `19982ab433dd25704ed60b1ac6ddb678bc3a98f9`
with prefix `before--`, once over this head with prefix `after--`.

The fixtures are the same objects the regression suite uses; they were extracted
mechanically from `tools/tests/test_catena_wave_1.py` and the extraction is kept
as `logs/fixtures-source.json` so a reviewer can check that the pictures and the
tests are of the same data.

## Every pair is audited by digest AND by pixel, before anything is described

`logs/pair-audit.py` classifies each `before--`/`after--` pair three ways:

- **(a) byte-identical** — the two files have the same SHA-256. Exits non-zero.
- **(b) byte-different but visually equivalent** — every differing pixel is
  within a tolerance in every channel, i.e. encoder noise. Exits non-zero.
- **(c) pixels differ** — with the count, the percentage, and the **bounding box
  of the change**, so a description can be checked against the region it claims.

Both (a) and (b) fail the audit, because both mean a claimed visual difference
is not one. The audit is also a hard gate inside `logs/sanitize-and-seal.py`:
sealing fails if a byte-identical pair is described anywhere in the package as
showing a difference.

**Result for this package**: 16 pairs audited, **0 byte-identical, 0 visually
equivalent, 16 genuinely different**, exit 0. The full table with digests, pixel
counts and bounding boxes is `logs/pair-audit.txt`, and `logs/pair-audit.json`
is the machine-readable form.

This is the direct answer to the V5 review's finding that five of ten claimed
pairs were byte-identical while four separate documents described each as
showing a visible change.

## What was captured, and what was deliberately not

A screenshot is offered **only** where the correction is visible in a raster.
Three states are not captured at all, and saying so is part of the evidence:

| Not captured | Because the finding is |
| --- | --- |
| `unsafe-textual-identity` | *which URL was requested*. A request is not in the picture; `logs/probe-parent.json` and `logs/probe-head.json` carry the resource logs. |
| `late-stale-work` | `hash`, `aria-busy`, focus and the tally after a late completion. The page a reader sees is Genesis 2 either way. |
| `bible-language-forms-voice` | additional `lang` attributes over a state already captured. A `lang` attribute is invisible. |

One further capture was **produced, audited, and then deleted**:
`bible-language-forms` at 393x852. The audit returned byte-identical; opening
the image showed why, and it is a fact about the page rather than about the
tool. At `max-width: 64rem` the page folds the controls disclosure shut on load,
so `#bible-select` — the element carrying the whole finding — is not rendered at
that viewport. Rather than ship a picture that frames none of its claim, the
viewport was removed from that state's matrix; the probe records
`capturedViewports: ["1440x900"]` for it.

Three states (`finding-order`, `finding-order-reversed`, `stray-partial`) were
**re-framed rather than deleted**. Captured to the viewport they were
byte-identical, because the absence disclosure sits below the fold and the whole
correction was off-screen. They are now captured beyond the viewport, so the
image contains the region it is offered for.

## Every image denies its own authenticity

Each PNG carries an `iTXt` chunk, keyword `Comment`:

    ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA | state=<name> | fabricated=true

All 30 were verified present. It is metadata rather than paint: burning a banner
into the pixels would alter the very rendering the picture is evidence of. The
chunk text is deterministic — no label, no path, no timestamp — so it cannot
manufacture a difference between the two runs.

`screenshots/before--probe-index.json` and `screenshots/after--probe-index.json`
carry the same banner at their root and on every entry, with each file's
`sha256`, `bytes` and `frame`. Neither index asserts a difference on its own
authority: each entry records
`differenceEstablishedBy: "pair-audit.py over a before--/after-- pair"`.
