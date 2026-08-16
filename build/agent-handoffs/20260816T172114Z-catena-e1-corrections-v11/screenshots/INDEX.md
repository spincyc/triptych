# Screenshots — V11 Catena missing-text correction

Head: `impl/catena-wave-1-e1-corrections-v11` at `3b93f74f032e74de9a50c1e2f1b35aa5b567f8d8`.
Parent: `ea15d16d22d7ceaed989ed9907c236f967738a03`.
Browser: Chrome/151.0.7922.137, headless, one device-pixel per CSS pixel.

## What changed, and what these images are for

The Catena route tells a reader why a fragment shows no text. Before V11 it had
two sentences; at V11 it has three.

| sentence | when |
| --- | --- |
| `This fragment carries no text file, so nothing of it can be shown.` | ABSENT — the chapter file states no text location and the fragment carries none |
| `A text reference was supplied for this fragment, but it cannot be used as written, so no text is shown.` | REFUSED — a non-empty written reference this page declines |
| `No text reference is established for this fragment, so no text is shown.` | UNESTABLISHED — **new at V11**; the member is present but is not a written textual value |

At the parent, an unestablished spine rendered the REFUSED sentence, asserting
two facts — that a reference *was supplied* and that it was unusable *as
written* — that its own state had not established. That is the whole visible
change. `src/web/browser/catena/catena.css` is byte-identical between the two commits and `src/web/browser/catena/catena.js`
differs by one line (`M.TEXT_REFUSED` becomes `fragment.text_note`).

## Two capture classes, kept apart

**real-corpus.** The built public artifact (`make public-site`), driven by the
repository's own gate, `tools/tests/corpus_browser_gate.mjs`, over its nine
governing states. Every fragment in the tracked corpus is present-valid, so no
missing-text sentence can appear in these images. They are the shell, layout
and accessibility-derivative evidence, and the evidence that the correction
disturbed none of it.

**adversarial.** The four fragment text-states are unreachable from the tracked
corpus. They are reached instead through the page's own documented `?data=`
parameter (`src/web/browser/shared/browser-core.js`, `resolveDataRoot`) pointed at a four-chapter
fixture corpus built in the session scratchpad. **No file under
`src/web/data/` was read, written or altered, in either checkout.** Each
fixture fragment renders the literal string
`ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA` in its author line and again
in its edition apparatus, so every one of these images is self-identifying.

Every adversarial capture opened the fragment `<details>` disclosure and read
the rendered sentence back out of the DOM before the shutter; a mismatch
against the expected sentence aborts without writing an image, so no image here
can claim a state it did not show. The text read back is recorded per image in
`screenshots/capture-metadata.json` as `rendered_text_read_from_dom`.

## Before / after result

| pair (same fixture, same viewport) | bytes identical | pixels differing / total | reading |
| --- | --- | --- | --- |
| `catena--fragment-absent--1440x900` | YES | 0 / 1296000 | Unchanged by design. The parent already rendered `ABSENT` here and so does the head; the two PNGs are byte-identical. |
| `catena--fragment-absent--393x852` | YES | 0 / 334836 | Unchanged by design. The parent already rendered `ABSENT` here and so does the head; the two PNGs are byte-identical. |
| `catena--fragment-present-valid--1440x900` | YES | 0 / 1296000 | Unchanged by design. The parent already rendered `BODY-TEXT` here and so does the head; the two PNGs are byte-identical. |
| `catena--fragment-present-valid--393x852` | YES | 0 / 334836 | Unchanged by design. The parent already rendered `BODY-TEXT` here and so does the head; the two PNGs are byte-identical. |
| `catena--fragment-refused--1440x900` | YES | 0 / 1296000 | Unchanged by design. The parent already rendered `REFUSED` here and so does the head; the two PNGs are byte-identical. |
| `catena--fragment-refused--393x852` | YES | 0 / 334836 | Unchanged by design. The parent already rendered `REFUSED` here and so does the head; the two PNGs are byte-identical. |
| `catena--fragment-unestablished--1440x900` | no | 11392 / 1296000 (in x 830-1436, y 121-899) | Parent renders `REFUSED`, head renders `UNESTABLISHED`. This is the correction. |
| `catena--fragment-unestablished--393x852` | no | 13639 / 334836 (in x 16-376, y 686-851) | Parent renders `REFUSED`, head renders `UNESTABLISHED`. This is the correction. |

Three of the four states are **byte-identical** before and after. That is not a
failure to capture a difference: it is the evidence that V11 changed only the
state the review found wrong and left the two the parent already got right, plus
the present-valid path, exactly as they were. The two unestablished pairs are
the only ones that differ, and they differ because the sentence differs; the
content below it reflows, which is why the differing region is larger than the
sentence itself.

## Every image

| filename | route / surface | state | viewport | corpus | checkout | what to inspect |
| --- | --- | --- | --- | --- | --- | --- |
| `screenshots/after--catena--fragment-absent--1440x900.png` | Catena — `/src/web/browser/catena/index.html` | fragment-absent | 1440x900 | adversarial | HEAD (V11) `3b93f74f032e` | That the absence sentence is unchanged from the parent. |
| `screenshots/after--catena--fragment-absent--393x852.png` | Catena — `/src/web/browser/catena/index.html` | fragment-absent | 393x852 | adversarial | HEAD (V11) `3b93f74f032e` | That the absence sentence is unchanged from the parent. |
| `screenshots/after--catena--fragment-present-valid--1440x900.png` | Catena — `/src/web/browser/catena/index.html` | fragment-present-valid | 1440x900 | adversarial | HEAD (V11) `3b93f74f032e` | That a valid text still renders and no sentence intrudes. |
| `screenshots/after--catena--fragment-present-valid--393x852.png` | Catena — `/src/web/browser/catena/index.html` | fragment-present-valid | 393x852 | adversarial | HEAD (V11) `3b93f74f032e` | That a valid text still renders and no sentence intrudes. |
| `screenshots/after--catena--fragment-refused--1440x900.png` | Catena — `/src/web/browser/catena/index.html` | fragment-refused | 1440x900 | adversarial | HEAD (V11) `3b93f74f032e` | That the refusal sentence the parent already got right is untouched — this is the control for the correction. |
| `screenshots/after--catena--fragment-refused--393x852.png` | Catena — `/src/web/browser/catena/index.html` | fragment-refused | 393x852 | adversarial | HEAD (V11) `3b93f74f032e` | That the refusal sentence the parent already got right is untouched — this is the control for the correction. |
| `screenshots/after--catena--fragment-unestablished--1440x900.png` | Catena — `/src/web/browser/catena/index.html` | fragment-unestablished | 1440x900 | adversarial | HEAD (V11) `3b93f74f032e` | The one sentence this correction changes. Compare the before-- and after-- images of the same viewport. |
| `screenshots/after--catena--fragment-unestablished--393x852.png` | Catena — `/src/web/browser/catena/index.html` | fragment-unestablished | 393x852 | adversarial | HEAD (V11) `3b93f74f032e` | The one sentence this correction changes. Compare the before-- and after-- images of the same viewport. |
| `screenshots/before--catena--fragment-absent--1440x900.png` | Catena — `/src/web/browser/catena/index.html` | fragment-absent | 1440x900 | adversarial | PARENT (V10) `ea15d16d22d7` | That the absence sentence is unchanged from the parent. |
| `screenshots/before--catena--fragment-absent--393x852.png` | Catena — `/src/web/browser/catena/index.html` | fragment-absent | 393x852 | adversarial | PARENT (V10) `ea15d16d22d7` | That the absence sentence is unchanged from the parent. |
| `screenshots/before--catena--fragment-present-valid--1440x900.png` | Catena — `/src/web/browser/catena/index.html` | fragment-present-valid | 1440x900 | adversarial | PARENT (V10) `ea15d16d22d7` | That a valid text still renders and no sentence intrudes. |
| `screenshots/before--catena--fragment-present-valid--393x852.png` | Catena — `/src/web/browser/catena/index.html` | fragment-present-valid | 393x852 | adversarial | PARENT (V10) `ea15d16d22d7` | That a valid text still renders and no sentence intrudes. |
| `screenshots/before--catena--fragment-refused--1440x900.png` | Catena — `/src/web/browser/catena/index.html` | fragment-refused | 1440x900 | adversarial | PARENT (V10) `ea15d16d22d7` | That the refusal sentence the parent already got right is untouched — this is the control for the correction. |
| `screenshots/before--catena--fragment-refused--393x852.png` | Catena — `/src/web/browser/catena/index.html` | fragment-refused | 393x852 | adversarial | PARENT (V10) `ea15d16d22d7` | That the refusal sentence the parent already got right is untouched — this is the control for the correction. |
| `screenshots/before--catena--fragment-unestablished--1440x900.png` | Catena — `/src/web/browser/catena/index.html` | fragment-unestablished | 1440x900 | adversarial | PARENT (V10) `ea15d16d22d7` | The one sentence this correction changes. Compare the before-- and after-- images of the same viewport. |
| `screenshots/before--catena--fragment-unestablished--393x852.png` | Catena — `/src/web/browser/catena/index.html` | fragment-unestablished | 393x852 | adversarial | PARENT (V10) `ea15d16d22d7` | The one sentence this correction changes. Compare the before-- and after-- images of the same viewport. |
| `screenshots/catena-index--desktop-1440x900--1440x900.png` | Catena — `/catena/index.html` | desktop-1440x900 | 1440x900 | real-corpus | HEAD (V11) `3b93f74f032e` | The changed route over the whole governing viewport and emulation matrix, on the real tracked corpus. Every tracked fragment is present-valid, so no missing-text sentence can appear here; these images are the shell and layout evidence, and the evidence that the correction disturbed neither. |
| `screenshots/catena-index--handset-393x852--393x852.png` | Catena — `/catena/index.html` | handset-393x852 | 393x852 | real-corpus | HEAD (V11) `3b93f74f032e` | The changed route over the whole governing viewport and emulation matrix, on the real tracked corpus. Every tracked fragment is present-valid, so no missing-text sentence can appear here; these images are the shell and layout evidence, and the evidence that the correction disturbed neither. |
| `screenshots/catena-index--handset-393x852-forced-colors--393x852.png` | Catena — `/catena/index.html` | handset-393x852-forced-colors | 393x852 | real-corpus | HEAD (V11) `3b93f74f032e` | The changed route over the whole governing viewport and emulation matrix, on the real tracked corpus. Every tracked fragment is present-valid, so no missing-text sentence can appear here; these images are the shell and layout evidence, and the evidence that the correction disturbed neither. |
| `screenshots/catena-index--handset-393x852-reduced-motion--393x852.png` | Catena — `/catena/index.html` | handset-393x852-reduced-motion | 393x852 | real-corpus | HEAD (V11) `3b93f74f032e` | The changed route over the whole governing viewport and emulation matrix, on the real tracked corpus. Every tracked fragment is present-valid, so no missing-text sentence can appear here; these images are the shell and layout evidence, and the evidence that the correction disturbed neither. |
| `screenshots/catena-index--handset-393x852-scale-400--393x852.png` | Catena — `/catena/index.html` | handset-393x852-scale-400 | 393x852 | real-corpus | HEAD (V11) `3b93f74f032e` | The changed route over the whole governing viewport and emulation matrix, on the real tracked corpus. Every tracked fragment is present-valid, so no missing-text sentence can appear here; these images are the shell and layout evidence, and the evidence that the correction disturbed neither. |
| `screenshots/catena-index--handset-393x852-text-200--393x852.png` | Catena — `/catena/index.html` | handset-393x852-text-200 | 393x852 | real-corpus | HEAD (V11) `3b93f74f032e` | The changed route over the whole governing viewport and emulation matrix, on the real tracked corpus. Every tracked fragment is present-valid, so no missing-text sentence can appear here; these images are the shell and layout evidence, and the evidence that the correction disturbed neither. |
| `screenshots/catena-index--laptop-1024x768--1024x768.png` | Catena — `/catena/index.html` | laptop-1024x768 | 1024x768 | real-corpus | HEAD (V11) `3b93f74f032e` | The changed route over the whole governing viewport and emulation matrix, on the real tracked corpus. Every tracked fragment is present-valid, so no missing-text sentence can appear here; these images are the shell and layout evidence, and the evidence that the correction disturbed neither. |
| `screenshots/catena-index--narrow-320x852--320x852.png` | Catena — `/catena/index.html` | narrow-320x852 | 320x852 | real-corpus | HEAD (V11) `3b93f74f032e` | The changed route over the whole governing viewport and emulation matrix, on the real tracked corpus. Every tracked fragment is present-valid, so no missing-text sentence can appear here; these images are the shell and layout evidence, and the evidence that the correction disturbed neither. |
| `screenshots/catena-index--tablet-768x1024--768x1024.png` | Catena — `/catena/index.html` | tablet-768x1024 | 768x1024 | real-corpus | HEAD (V11) `3b93f74f032e` | The changed route over the whole governing viewport and emulation matrix, on the real tracked corpus. Every tracked fragment is present-valid, so no missing-text sentence can appear here; these images are the shell and layout evidence, and the evidence that the correction disturbed neither. |
| `screenshots/index--desktop-1440x900--1440x900.png` | Home — `/index.html` | desktop-1440x900 | 1440x900 | real-corpus | HEAD (V11) `3b93f74f032e` | Home shell, unchanged by this correction. |
| `screenshots/index--handset-393x852--393x852.png` | Home — `/index.html` | handset-393x852 | 393x852 | real-corpus | HEAD (V11) `3b93f74f032e` | Home shell, unchanged by this correction. |
| `screenshots/index--narrow-320x852--320x852.png` | Home — `/index.html` | narrow-320x852 | 320x852 | real-corpus | HEAD (V11) `3b93f74f032e` | Home shell, unchanged by this correction. |
| `screenshots/liturgy-day-reader--desktop-1440x900--1440x900.png` | Reader — `/liturgy/day-reader.html` | desktop-1440x900 | 1440x900 | real-corpus | HEAD (V11) `3b93f74f032e` | Reader shell, unchanged by this correction. |
| `screenshots/sources-index--desktop-1440x900--1440x900.png` | Sources — `/sources/index.html` | desktop-1440x900 | 1440x900 | real-corpus | HEAD (V11) `3b93f74f032e` | Source Library shell, unchanged by this correction. |
| `screenshots/texts-index--desktop-1440x900--1440x900.png` | Publications — `/texts/index.html` | desktop-1440x900 | 1440x900 | real-corpus | HEAD (V11) `3b93f74f032e` | Publications catalogue shell, unchanged by this correction. |

## Bounds — what is not here, and why

- **No print capture.** The changed sentence lives inside a `<details>`
  disclosure that a print stylesheet does not open by itself, and the roadmap's
  print item is a check rather than a required image for a copy correction.
  Nothing here should be read as print evidence.
- **No no-JavaScript capture.** With scripts off the Catena route serves a
  static "About this page" block and no fragments at all — verified in the built
  `src/web/browser/catena/index.html` — so nothing that could carry a missing-text sentence is
  on the page in either checkout, and an image would show the same thing twice.
  The gate's `no-script-static-truth` phase covers that route as a check.
- **No corrected-Sources or changed-Browse-control capture.** The parent-to-head
  diff touches `src/web/browser/catena/catena-model.js`,
  `src/web/browser/catena/catena.js` and `tools/tests/test_catena_wave_1.py`
  and nothing else. There is no corrected Sources page and no changed Browse
  control in this correction to photograph. The Sources, Publications, Reader
  and Home wide-default images in the table above are shell evidence that they are untouched,
  not correction evidence about them.
- **The gate reports pre-existing failures** on these routes (two `<main>`
  elements introduced by the release layout wrapping, and undersized navigation
  targets at the handset width). They are present on every route captured,
  including ones this correction does not touch, and they are not caused by it.
  They belong to the checks lane, not to this directory.
