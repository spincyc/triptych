# Visual state index — Catena E1 V5

Twenty PNGs. `before--` is the exact reviewed V4.1 head
`f93757854b54c19e50bdcb97ca0fed9b48d22bb7`; `after--` is this candidate's
implementation commit, whose build-sensitive tree is byte-identical to the
final head. Both were served from their own `make public-site` build by
`logs/probe-catena.mjs` over the DevTools Protocol in headless Chromium; no
display server was used and no image was edited.

**Every image shows fabricated adversarial data.** The fixtures are injected in
the probe's own server response path over an unmodified built site. None of
these pages shows a holding of this project, a corpus record, or any real state
of the published site. See `LIMITATIONS.md` §1.

| Image | Head | State | Address | Viewport | Media | Demonstrates |
| --- | --- | --- | --- | --- | --- | --- |
| `before--catena--malformed-language-everything-held--1440x900.png` | V4.1 base | `malformed-language-everything-held` | `#book=Gen&chapter=1&bible=douay-rheims` | 1440x900 | screen | the visible language chip: a value that is not a language code no longer names one |
| `before--catena--malformed-language-everything-held--393x852.png` | V4.1 base | `malformed-language-everything-held` | `#book=Gen&chapter=1&bible=douay-rheims` | 393x852 | screen | the visible language chip: a value that is not a language code no longer names one |
| `before--catena--mixed-collection-members--1440x900.png` | V4.1 base | `mixed-collection-members` | `#book=Gen&chapter=1&bible=douay-rheims` | 1440x900 | screen | a null member replaced the whole page with a JavaScript error; the valid siblings now stand |
| `before--catena--mixed-collection-members--393x852.png` | V4.1 base | `mixed-collection-members` | `#book=Gen&chapter=1&bible=douay-rheims` | 393x852 | screen | a null member replaced the whole page with a JavaScript error; the valid siblings now stand |
| `before--catena--typed-absence-findings--1440x900.png` | V4.1 base | `typed-absence-findings` | `#book=Gen&chapter=1&bible=douay-rheims&voice=translation:en` | 1440x900 | screen | the absence summary: a manufactured closed negative replaced by what each finding supports |
| `before--catena--typed-absence-findings--393x852.png` | V4.1 base | `typed-absence-findings` | `#book=Gen&chapter=1&bible=douay-rheims&voice=translation:en` | 393x852 | screen | the absence summary: a manufactured closed negative replaced by what each finding supports |
| `before--catena--malformed-word-tallies--1440x900.png` | V4.1 base | `malformed-word-tallies` | `#book=Gen&chapter=1&bible=douay-rheims` | 1440x900 | screen | the word-count chips: "1 words" for a boolean and "12.5 words" for a fraction are gone |
| `before--catena--malformed-word-tallies--393x852.png` | V4.1 base | `malformed-word-tallies` | `#book=Gen&chapter=1&bible=douay-rheims` | 393x852 | screen | the word-count chips: "1 words" for a boolean and "12.5 words" for a fraction are gone |
| `before--catena--malformed-canon-bootstrap--1440x900.png` | V4.1 base | `malformed-canon-bootstrap` | `(no address)` | 1440x900 | screen | the page stood at "Loading…" for ever; it now settles and says what failed |
| `before--catena--malformed-canon-bootstrap--393x852.png` | V4.1 base | `malformed-canon-bootstrap` | `(no address)` | 393x852 | screen | the page stood at "Loading…" for ever; it now settles and says what failed |
| `after--catena--malformed-language-everything-held--1440x900.png` | V5 head | `malformed-language-everything-held` | `#book=Gen&chapter=1&bible=douay-rheims` | 1440x900 | screen | the visible language chip: a value that is not a language code no longer names one |
| `after--catena--malformed-language-everything-held--393x852.png` | V5 head | `malformed-language-everything-held` | `#book=Gen&chapter=1&bible=douay-rheims` | 393x852 | screen | the visible language chip: a value that is not a language code no longer names one |
| `after--catena--mixed-collection-members--1440x900.png` | V5 head | `mixed-collection-members` | `#book=Gen&chapter=1&bible=douay-rheims` | 1440x900 | screen | a null member replaced the whole page with a JavaScript error; the valid siblings now stand |
| `after--catena--mixed-collection-members--393x852.png` | V5 head | `mixed-collection-members` | `#book=Gen&chapter=1&bible=douay-rheims` | 393x852 | screen | a null member replaced the whole page with a JavaScript error; the valid siblings now stand |
| `after--catena--typed-absence-findings--1440x900.png` | V5 head | `typed-absence-findings` | `#book=Gen&chapter=1&bible=douay-rheims&voice=translation:en` | 1440x900 | screen | the absence summary: a manufactured closed negative replaced by what each finding supports |
| `after--catena--typed-absence-findings--393x852.png` | V5 head | `typed-absence-findings` | `#book=Gen&chapter=1&bible=douay-rheims&voice=translation:en` | 393x852 | screen | the absence summary: a manufactured closed negative replaced by what each finding supports |
| `after--catena--malformed-word-tallies--1440x900.png` | V5 head | `malformed-word-tallies` | `#book=Gen&chapter=1&bible=douay-rheims` | 1440x900 | screen | the word-count chips: "1 words" for a boolean and "12.5 words" for a fraction are gone |
| `after--catena--malformed-word-tallies--393x852.png` | V5 head | `malformed-word-tallies` | `#book=Gen&chapter=1&bible=douay-rheims` | 393x852 | screen | the word-count chips: "1 words" for a boolean and "12.5 words" for a fraction are gone |
| `after--catena--malformed-canon-bootstrap--1440x900.png` | V5 head | `malformed-canon-bootstrap` | `(no address)` | 1440x900 | screen | the page stood at "Loading…" for ever; it now settles and says what failed |
| `after--catena--malformed-canon-bootstrap--393x852.png` | V5 head | `malformed-canon-bootstrap` | `(no address)` | 393x852 | screen | the page stood at "Loading…" for ever; it now settles and says what failed |

## Conditional classes and why they are or are not here

- **Print and forced-colors**: not captured. `catena.css` is byte-identical to
  V4.1 and nothing in this correction bears on those media. V4.1's accepted
  53-image matrix already covers them for the real corpus states and is neither
  superseded nor re-issued here.
- **1024×768 and 768×1024**: not captured. The five states differ in text and
  in error state, not in layout, and both captured viewports already span the
  desktop/handset divide where this page's composition changes.
- **Real corpus states**: not re-captured. Nothing about them changed, and
  V4.1's matrix is the accepted evidence for them.
- **Text-200% and scale-400%**: not captured. The shared browser gate asserts
  both across all 19 routes and 9 states, and its report is deep-equal between
  base and head.
- **Blockers 1 and 4 (`lang`, requests, `aria-busy`)**: **no image can carry
  these facts.** Their evidence is `logs/probe-base.json`,
  `logs/probe-head.json` and `PROBE-DIFFERENCE.md`, not a picture.
