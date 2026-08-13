# Limitations of this lane and this package

Stated so a reviewer does not have to discover them.

## Known gaps against the review

**1. The refusal copy was not changed.** The review asked for neutral umbrella
copy or a typed unsupported reason, because *"address could not be read"* is
imprecise for a value that parsed cleanly and is merely unsupported. The
detail line does name the exact reason, and malformed and unsupported
refusals are distinguishable by detail text — but the heading and the status
line are still shared between them. Not closed. Disclosed.

**2. No screenshots, and no conditional-source omission rationale.** The
review asked for a capture of the visible refusal change. No display was
available to this session, so the refusal change is evidenced **structurally**
— replayed DOM projections, roles, labels, status writes — and not visually.
Not closed. Disclosed.

## Evidence that is structural, not real

All accessibility evidence here is structural or emulated:

- No screen-reader, speech, or braille session was completed, and no spoken
  announcement was produced or verified. What is shown is that the page
  performs **one status-region write** per render. See `AT-LIMITATION.md`, and
  read its negatives as scoped to the inspected session rather than as
  statements about the platform.
- Forced-colors evidence is **emulated**. Genuine system forced colors remains
  a disclosed limitation.
- No real-device evidence. That remains a separately owned pre-release
  prerequisite.

## Limits of the measurements

- The browser gate reports are equal **object for object** with run metadata
  excluded. That is assertion identity, status and detail — it is **not** DOM
  or pixel identity, and nothing here claims the rendered pages are visually
  identical.
- The base side of the full-suite comparison was measured in a separate clean
  clone. One failure appears there and not at head purely because of the clone
  path; it is disclosed and is **not** claimed as a fix.
- The package digest is a **transport digest** — `sha256sum` of the archive.
  It proves the archive received is the archive sent. It does **not** prove
  reproducible construction: entry timestamps are local mtimes, so re-zipping
  the same tree yields a different digest. `MANIFEST.sha256` is the content
  proof.
- Timings were measured with two full suites running concurrently, so they are
  not a clean performance baseline.

## Limits of the correction itself

- The exact voice-key projection is **counted from the tracked corpus**. It is
  correct for what is held today and regenerates automatically, but the array
  is only as good as the generator's `voice` derivation, which this lane did
  not re-verify beyond running its existing check.
- The typed boundary covers the nine sinks the review named. One further sink
  was seen and deliberately **left alone**: `renderChapter` writes verse values
  without typing them, so an object-valued verse would still render as
  `[object Object]`. It is shared with the scripture page and its data root is
  validated elsewhere, so fixing it here would have taken ownership this lane
  does not have. Named in `REVIEW_REQUEST.md`.
- `?data=fixture` now fails closed on any `voice=` key. Judged an improvement,
  not regenerated, disclosed.

## What this package does not do

It does not amend, correct, or replace the V3 package's contents. The V3
package remains exactly as sealed, with its recorded digest, as evidence of a
review that happened. This package supersedes it for the next review only.
