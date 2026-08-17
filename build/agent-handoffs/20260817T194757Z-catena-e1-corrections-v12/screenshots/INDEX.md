# Screenshots — V12 Catena request-critical-state correction

Head: `impl/catena-wave-1-e1-corrections-v12` at `d312786dd2b23926aa88e29ea15647dfcc7e7e6e`.
Parent: `0255b84996e1dc24da3ce75ac318c4f774b7957c`.
Browser: Chrome/151.0.7922.137, headless, one device-pixel per CSS pixel.

## What changed, and what these images are for

Three inputs that a hostile or broken server could hand this page reached its
request sink at the parent. None of the three is a document: a prototype, a
polluted realm and a drifting property descriptor are facts about a JavaScript
object, so none of them can be written into a corpus file and none of them was
visible to the page's own reading of the bytes it was served. At the head all
three are closed, and the reader is told only what the record established.

| scenario | the input a server could hand the page | parent (BEFORE) shows | head (AFTER) shows |
| --- | --- | --- | --- |
| `inherited-prefix` | a chapter spine with NO own `text_prefix` and a valid one on its PROTOTYPE, beside a fragment carrying a valid same-stem `text_path` | the planted body at the fragment's carried address | `No text reference is established for this fragment, so no text is shown.` |
| `inherited-refusal` | a spine with an OWN valid `text_prefix`, served while `Object.prototype.text_refused === true` | the planted body at the address that prefix composes | the same unestablished sentence |
| `drifting-path` | a fragment whose `text_path` descriptor answers one valid address on the first ask and a different plantable address on every later ask | the planted body at the SECOND address — one nothing validated | the planted body at the validated FIRST address; the second address is fetched by nothing |

The parent read an inherited prefix as the absence below it, which is the one
state that opens the carried fallback door; it asked the prototype about three
claim members and not about `text_refused`; and it read the carried descriptor
twice in one projection, so the address that passed the own-stem test and the
address handed to `fetch` were two different strings. That is the whole visible
change. `src/web/browser/catena/catena.css`, `src/web/browser/catena/catena.js`
and `src/web/browser/catena/index.html` are byte-identical between the two
commits; `src/web/browser/catena/catena-model.js` is the only page source that
differs.

## One capture class: adversarial, and what that costs

None of these three states is reachable from the tracked corpus, and none of
them can be written into a file at all. They are reached instead through the
page's own documented `?data=` parameter
(`src/web/browser/shared/browser-core.js`, `resolveDataRoot`) pointed at a
three-root fixture corpus built in the session scratchpad, with the one
contamination each scenario is about installed behind `window.fetch` before any
page script runs — the same seam, and the same three hooks (`contaminate`,
`polluteObjectPrototype`, `driftCarriedPath`), that
`tools/tests/test_catena_wave_1.py` installs behind `global.fetch`.

**No file under `src/web/data/` was read, written or altered, in either
checkout.** The capture driver's static server refuses every path that does not
resolve inside `src/web/browser/catena/`, `src/web/browser/shared/` or the
scratchpad fixture root, so the promise is enforced rather than merely intended.

Every fixture record carries the literal string
`ADVERSARIAL TEST FIXTURE — NOT REAL CORPUS DATA`, and the page renders it in
the fragment's author line, in its edition apparatus, in the translation
control and in every verse — so each of these images is self-identifying and
carries its own denial with it, detached from this file.

A body is planted at **every address each scenario could reach**, so a leak
succeeds visibly rather than merely failing to be forbidden: a BEFORE image
here shows real leaked text, not an empty box. The three bodies are named in
the images — PLANTED FALLBACK BODY, PLANTED COMPOSED BODY, PLANTED SECOND-READ
BODY — after the fixtures `V9_PLANTED_FALLBACK`, `V9_COMPOSED_DEEPER` and
`V12_PLANTED_OTHER` that pin the same three facts in the test file.

Every capture opened the fragment `<details>` disclosure and read the rendered
sentence back out of the DOM before the shutter; a mismatch against what the
image is supposed to show aborts without writing an image, so no image here can
claim a state it did not show. The text read back is recorded per image in
`screenshots/capture-metadata.json` as `rendered_text_read_from_dom`, beside
`text_requests_made` — the text addresses that page actually requested — and
`carried_descriptor_reads`, the number of times the drifting descriptor was
asked.

## Before / after result

| pair (same fixture, same viewport) | bytes identical | pixels differing / total | reading |
| --- | --- | --- | --- |
| `catena--inherited-prefix--1440x900` | no | 10068 / 1296000 (in x 838-1371, y 70-899) | Parent fetches structure/catena/text/fallback-owned.json and renders its planted body; head requests nothing and says the unestablished sentence. |
| `catena--inherited-prefix--393x852` | no | 64525 / 334836 (in x 16-376, y 218-851) | The same difference at the handset width. |
| `catena--inherited-refusal--1440x900` | no | 10217 / 1296000 (in x 838-1371, y 70-899) | Parent fetches structure/catena/text/deeper/fallback-owned.json and renders its planted body; head requests nothing and says the unestablished sentence. |
| `catena--inherited-refusal--393x852` | no | 64816 / 334836 (in x 16-376, y 218-851) | The same difference at the handset width. |
| `catena--drifting-path--1440x900` | no | 4707 / 1296000 (in x 838-1132, y 137-899) | Parent fetches structure/catena/text/other.json — the descriptor's second value, which passed no test — and renders its planted body; head fetches structure/catena/text/fallback-owned.json, the value it validated, and renders that one instead. |
| `catena--drifting-path--393x852` | no | 55397 / 334836 (in x 16-376, y 271-851) | The same difference at the handset width. |

All six pairs differ, and every difference is the fragment's text paragraph and
what its height pushes below it. Two readings of the bounding boxes are worth
stating plainly rather than leaving to be discovered:

- **At 1440x900 the boxes are nearly empty above y 750.** Per the fifty-row
  histogram in `screenshots/capture-metadata.json`
  (`pairs[].pixels_by_row_band`), every differing pixel above that line is a
  single pixel differing by one value in one channel at the fragment column's
  edge — a sub-visible compositing artifact, not content. The content
  difference is wholly inside y 750-899.
- **At 393x852 the difference runs from the paragraph to the foot of the
  image**, because the leaked body is several lines taller than the sentence
  that replaces it and everything below it reflows. Both images of each handset
  pair are scrolled so the fragment card sits the same distance below the top
  edge, so the pixels above the paragraph align and the difference below it is
  the correction rather than an offset.

Four images share a digest with another image in this directory, and
`screenshots/capture-metadata.json` lists them under `images_sharing_a_digest`.
None of them is a before/after pair. Two states that resolve identically
photograph identically: the two AFTER images of `inherited-prefix` and
`inherited-refusal` are byte-identical at each viewport because both
contaminations close the same way onto the same sentence, and
`after--catena--drifting-path` matches `before--catena--inherited-prefix`
because both render the same planted body at the same address.

## Every image

| filename | route / surface | state | viewport | corpus | checkout | what to inspect |
| --- | --- | --- | --- | --- | --- | --- |
| `screenshots/after--catena--drifting-path--1440x900.png` | Catena — `/src/web/browser/catena/index.html` | drifting-path | 1440x900 | adversarial | HEAD (V12) `d312786dd2b2` | The fragment text paragraph, and WHICH planted body is in it. Here it is the body at the validated first address; the second address is requested by nothing. |
| `screenshots/after--catena--drifting-path--393x852.png` | Catena — `/src/web/browser/catena/index.html` | drifting-path | 393x852 | adversarial | HEAD (V12) `d312786dd2b2` | The same, at the handset width. |
| `screenshots/after--catena--inherited-prefix--1440x900.png` | Catena — `/src/web/browser/catena/index.html` | inherited-prefix | 1440x900 | adversarial | HEAD (V12) `d312786dd2b2` | The unestablished sentence where V11 showed a leaked body. This is the correction. |
| `screenshots/after--catena--inherited-prefix--393x852.png` | Catena — `/src/web/browser/catena/index.html` | inherited-prefix | 393x852 | adversarial | HEAD (V12) `d312786dd2b2` | The same, at the handset width. |
| `screenshots/after--catena--inherited-refusal--1440x900.png` | Catena — `/src/web/browser/catena/index.html` | inherited-refusal | 1440x900 | adversarial | HEAD (V12) `d312786dd2b2` | The unestablished sentence where V11 composed and showed a body. This is the correction. |
| `screenshots/after--catena--inherited-refusal--393x852.png` | Catena — `/src/web/browser/catena/index.html` | inherited-refusal | 393x852 | adversarial | HEAD (V12) `d312786dd2b2` | The same, at the handset width. |
| `screenshots/before--catena--drifting-path--1440x900.png` | Catena — `/src/web/browser/catena/index.html` | drifting-path | 1440x900 | adversarial | PARENT `0255b84996e1` | The leak: the planted body of the descriptor's SECOND address, which nothing validated, rendered as an ordinary success. |
| `screenshots/before--catena--drifting-path--393x852.png` | Catena — `/src/web/browser/catena/index.html` | drifting-path | 393x852 | adversarial | PARENT `0255b84996e1` | The same, at the handset width. |
| `screenshots/before--catena--inherited-prefix--1440x900.png` | Catena — `/src/web/browser/catena/index.html` | inherited-prefix | 1440x900 | adversarial | PARENT `0255b84996e1` | The leak: an inherited prefix read as genuine absence opens the carried door, and the planted body at the carried address is fetched and rendered. |
| `screenshots/before--catena--inherited-prefix--393x852.png` | Catena — `/src/web/browser/catena/index.html` | inherited-prefix | 393x852 | adversarial | PARENT `0255b84996e1` | The same, at the handset width. |
| `screenshots/before--catena--inherited-refusal--1440x900.png` | Catena — `/src/web/browser/catena/index.html` | inherited-refusal | 1440x900 | adversarial | PARENT `0255b84996e1` | The leak: an inherited refusal marker stands beside an own-valid claim, the claim composes its request anyway, and the composed body renders. |
| `screenshots/before--catena--inherited-refusal--393x852.png` | Catena — `/src/web/browser/catena/index.html` | inherited-refusal | 393x852 | adversarial | PARENT `0255b84996e1` | The same, at the handset width. |

## Bounds — what is not here, and why

- **No real-corpus capture.** Every one of these three inputs is a fact about a
  JavaScript object rather than about a file, so none is expressible in the
  tracked corpus and no image taken from it could show any of them. The shell,
  layout and accessibility-derivative evidence for this route is unchanged from
  the V11 package: `src/web/browser/catena/catena.css`,
  `src/web/browser/catena/catena.js` and
  `src/web/browser/catena/index.html` are byte-identical across this
  correction, so a re-shot real-corpus matrix would show the same pixels twice.
- **No print capture.** The paragraph this correction changes lives inside a
  `<details>` disclosure a print stylesheet does not open by itself. Nothing
  here should be read as print evidence.
- **No no-JavaScript capture.** With scripts off the Catena route serves a
  static "About this page" block and no fragments at all, so nothing that could
  carry a text paragraph is on the page in either checkout, and an image would
  show the same thing twice.
- **The handset images do not show the page heading.** At 393x852 the fragment
  card and the page's own header cannot both be in one viewport; the card wins,
  because the card is what this correction changes. The route each image was
  taken from is recorded per image in `screenshots/capture-metadata.json`.
- **No image here is evidence about any other route.** The parent-to-head diff
  touches `src/web/browser/catena/catena-model.js`,
  `tools/tests/test_catena_wave_1.py` and project records, and nothing else.
