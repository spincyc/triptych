# Visual state index — Catena E1 V4.1

Every image below was captured from a `make public-site` artifact built at the
exact implementation head `f93757854b54c19e50bdcb97ca0fed9b48d22bb7` (the `before--` images from its parent
`e40720d5d622e8b0528b8c714cc5caee0b21cee3`), served over loopback HTTP and driven
by the repository's own headless Chromium — Chromium 151.0.7922.108, the same
engine `tools/tests/corpus_browser_gate.mjs` uses.

Routes are written as the page's own address. Every identifier is real repository
data under `src/web/data/structure/catena/`; no fixture was made for a picture.

| Image | Head | Route / state | Viewport | Browser mode | Demonstrates |
| --- | --- | --- | --- | --- | --- |
| `before--catena--unsupported-voice-grc--1440x900.png` | parent e40720d5d | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:grc` | 1440x900 | screen | BEFORE: the non-neutral umbrella copy the V3 review rejected. |
| `before--catena--unsupported-voice-grc--393x852.png` | parent e40720d5d | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:grc` | 393x852 | screen | BEFORE: the non-neutral umbrella copy the V3 review rejected. |
| `before--catena--unsupported-voice-grc--320x852.png` | parent e40720d5d | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:grc` | 320x852 | screen | BEFORE: the non-neutral umbrella copy the V3 review rejected. |
| `before--catena--malformed-address--1440x900.png` | parent e40720d5d | `/catena/index.html#book=Foo&chapter=1&bible=douay-rheims` | 1440x900 | screen | BEFORE: the non-neutral umbrella copy the V3 review rejected. |
| `before--catena--malformed-address--393x852.png` | parent e40720d5d | `/catena/index.html#book=Foo&chapter=1&bible=douay-rheims` | 393x852 | screen | BEFORE: the non-neutral umbrella copy the V3 review rejected. |
| `before--catena--malformed-address--320x852.png` | parent e40720d5d | `/catena/index.html#book=Foo&chapter=1&bible=douay-rheims` | 320x852 | screen | BEFORE: the non-neutral umbrella copy the V3 review rejected. |
| `after--catena--ordinary-populated--1440x900.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims` | 1440x900 | screen | An ordinary populated Catena chapter renders unchanged by this lane. |
| `after--catena--ordinary-populated--1440x900--print.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims` | 1440x900 | print emulation | An ordinary populated Catena chapter renders unchanged by this lane. |
| `after--catena--ordinary-populated--393x852.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims` | 393x852 | screen | An ordinary populated Catena chapter renders unchanged by this lane. |
| `after--catena--ordinary-populated--393x852--forced-colors.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims` | 393x852 | screen, `forced-colors: active` | An ordinary populated Catena chapter renders unchanged by this lane. |
| `after--catena--ordinary-populated--320x852.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims` | 320x852 | screen | An ordinary populated Catena chapter renders unchanged by this lane. |
| `after--catena--voice-original--1440x900.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=original` | 1440x900 | screen | The exact supported voice `original` projects and renders. |
| `after--catena--voice-original--1440x900--print.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=original` | 1440x900 | print emulation | The exact supported voice `original` projects and renders. |
| `after--catena--voice-original--393x852.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=original` | 393x852 | screen | The exact supported voice `original` projects and renders. |
| `after--catena--voice-original--393x852--forced-colors.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=original` | 393x852 | screen, `forced-colors: active` | The exact supported voice `original` projects and renders. |
| `after--catena--voice-original--320x852.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=original` | 320x852 | screen | The exact supported voice `original` projects and renders. |
| `after--catena--voice-translation-en--1440x900.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:en` | 1440x900 | screen | The exact supported voice `translation:en` projects and renders. |
| `after--catena--voice-translation-en--1440x900--print.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:en` | 1440x900 | print emulation | The exact supported voice `translation:en` projects and renders. |
| `after--catena--voice-translation-en--393x852.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:en` | 393x852 | screen | The exact supported voice `translation:en` projects and renders. |
| `after--catena--voice-translation-en--393x852--forced-colors.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:en` | 393x852 | screen, `forced-colors: active` | The exact supported voice `translation:en` projects and renders. |
| `after--catena--voice-translation-en--320x852.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:en` | 320x852 | screen | The exact supported voice `translation:en` projects and renders. |
| `after--catena--voice-translation-la--1440x900.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:la` | 1440x900 | screen | The exact supported voice `translation:la` projects and renders. |
| `after--catena--voice-translation-la--1440x900--print.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:la` | 1440x900 | print emulation | The exact supported voice `translation:la` projects and renders. |
| `after--catena--voice-translation-la--393x852.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:la` | 393x852 | screen | The exact supported voice `translation:la` projects and renders. |
| `after--catena--voice-translation-la--393x852--forced-colors.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:la` | 393x852 | screen, `forced-colors: active` | The exact supported voice `translation:la` projects and renders. |
| `after--catena--voice-translation-la--320x852.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:la` | 320x852 | screen | The exact supported voice `translation:la` projects and renders. |
| `after--catena--unsupported-voice-grc--1440x900.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:grc` | 1440x900 | screen | `translation:grc` fails closed: URL preserved, no chapter fetched, no holding claimed, NEUTRAL umbrella copy after the V4.1 correction. |
| `after--catena--unsupported-voice-grc--1440x900--print.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:grc` | 1440x900 | print emulation | `translation:grc` fails closed: URL preserved, no chapter fetched, no holding claimed, NEUTRAL umbrella copy after the V4.1 correction. |
| `after--catena--unsupported-voice-grc--393x852.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:grc` | 393x852 | screen | `translation:grc` fails closed: URL preserved, no chapter fetched, no holding claimed, NEUTRAL umbrella copy after the V4.1 correction. |
| `after--catena--unsupported-voice-grc--393x852--forced-colors.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:grc` | 393x852 | screen, `forced-colors: active` | `translation:grc` fails closed: URL preserved, no chapter fetched, no holding claimed, NEUTRAL umbrella copy after the V4.1 correction. |
| `after--catena--unsupported-voice-grc--320x852.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:grc` | 320x852 | screen | `translation:grc` fails closed: URL preserved, no chapter fetched, no holding claimed, NEUTRAL umbrella copy after the V4.1 correction. |
| `after--catena--supported-voice-empty-chapter--1440x900.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=10&bible=douay-rheims&voice=translation:en` | 1440x900 | screen | A valid chapter with a supported voice and no chapter material stays valid and says so without manufacturing an absence. |
| `after--catena--supported-voice-empty-chapter--1440x900--print.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=10&bible=douay-rheims&voice=translation:en` | 1440x900 | print emulation | A valid chapter with a supported voice and no chapter material stays valid and says so without manufacturing an absence. |
| `after--catena--supported-voice-empty-chapter--393x852.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=10&bible=douay-rheims&voice=translation:en` | 393x852 | screen | A valid chapter with a supported voice and no chapter material stays valid and says so without manufacturing an absence. |
| `after--catena--supported-voice-empty-chapter--393x852--forced-colors.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=10&bible=douay-rheims&voice=translation:en` | 393x852 | screen, `forced-colors: active` | A valid chapter with a supported voice and no chapter material stays valid and says so without manufacturing an absence. |
| `after--catena--supported-voice-empty-chapter--320x852.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=10&bible=douay-rheims&voice=translation:en` | 320x852 | screen | A valid chapter with a supported voice and no chapter material stays valid and says so without manufacturing an absence. |
| `after--catena--malformed-address--1440x900.png` | V4.1 f93757854 | `/catena/index.html#book=Foo&chapter=1&bible=douay-rheims` | 1440x900 | screen | An address refused on GRAMMAR shares the same neutral umbrella, with its own typed reason. |
| `after--catena--malformed-address--1440x900--print.png` | V4.1 f93757854 | `/catena/index.html#book=Foo&chapter=1&bible=douay-rheims` | 1440x900 | print emulation | An address refused on GRAMMAR shares the same neutral umbrella, with its own typed reason. |
| `after--catena--malformed-address--393x852.png` | V4.1 f93757854 | `/catena/index.html#book=Foo&chapter=1&bible=douay-rheims` | 393x852 | screen | An address refused on GRAMMAR shares the same neutral umbrella, with its own typed reason. |
| `after--catena--malformed-address--393x852--forced-colors.png` | V4.1 f93757854 | `/catena/index.html#book=Foo&chapter=1&bible=douay-rheims` | 393x852 | screen, `forced-colors: active` | An address refused on GRAMMAR shares the same neutral umbrella, with its own typed reason. |
| `after--catena--malformed-address--320x852.png` | V4.1 f93757854 | `/catena/index.html#book=Foo&chapter=1&bible=douay-rheims` | 320x852 | screen | An address refused on GRAMMAR shares the same neutral umbrella, with its own typed reason. |
| `after--catena--numbering-refusal--1440x900.png` | V4.1 f93757854 | `/catena/index.html#book=Ps&chapter=13&bible=king-james-version` | 1440x900 | screen | The numbering-boundary refusal keeps its own words and `data-state`, untouched by this lane. |
| `after--catena--numbering-refusal--1440x900--print.png` | V4.1 f93757854 | `/catena/index.html#book=Ps&chapter=13&bible=king-james-version` | 1440x900 | print emulation | The numbering-boundary refusal keeps its own words and `data-state`, untouched by this lane. |
| `after--catena--numbering-refusal--393x852.png` | V4.1 f93757854 | `/catena/index.html#book=Ps&chapter=13&bible=king-james-version` | 393x852 | screen | The numbering-boundary refusal keeps its own words and `data-state`, untouched by this lane. |
| `after--catena--numbering-refusal--393x852--forced-colors.png` | V4.1 f93757854 | `/catena/index.html#book=Ps&chapter=13&bible=king-james-version` | 393x852 | screen, `forced-colors: active` | The numbering-boundary refusal keeps its own words and `data-state`, untouched by this lane. |
| `after--catena--numbering-refusal--320x852.png` | V4.1 f93757854 | `/catena/index.html#book=Ps&chapter=13&bible=king-james-version` | 320x852 | screen | The numbering-boundary refusal keeps its own words and `data-state`, untouched by this lane. |
| `after--catena--acquisition-leads--1440x900.png` | V4.1 f93757854 | `/catena/index.html#book=Ex&chapter=3&bible=douay-rheims` | 1440x900 | screen | Acquisition/lead rows stay separate from held commentary, untouched by this lane. |
| `after--catena--acquisition-leads--1440x900--print.png` | V4.1 f93757854 | `/catena/index.html#book=Ex&chapter=3&bible=douay-rheims` | 1440x900 | print emulation | Acquisition/lead rows stay separate from held commentary, untouched by this lane. |
| `after--catena--acquisition-leads--393x852.png` | V4.1 f93757854 | `/catena/index.html#book=Ex&chapter=3&bible=douay-rheims` | 393x852 | screen | Acquisition/lead rows stay separate from held commentary, untouched by this lane. |
| `after--catena--acquisition-leads--393x852--forced-colors.png` | V4.1 f93757854 | `/catena/index.html#book=Ex&chapter=3&bible=douay-rheims` | 393x852 | screen, `forced-colors: active` | Acquisition/lead rows stay separate from held commentary, untouched by this lane. |
| `after--catena--acquisition-leads--320x852.png` | V4.1 f93757854 | `/catena/index.html#book=Ex&chapter=3&bible=douay-rheims` | 320x852 | screen | Acquisition/lead rows stay separate from held commentary, untouched by this lane. |
| `after--catena--provenance-open-fragment--1440x900--focused-region.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims`, Severian of Gabala disclosure opened | 1440x900 | screen, focused region | Displayed provenance renders typed: author, work, date, voice, extent, citation and edition. |
| `after--catena--provenance-open-fragment--393x852--focused-region.png` | V4.1 f93757854 | `/catena/index.html#book=Gen&chapter=1&bible=douay-rheims`, Severian of Gabala disclosure opened | 393x852 | screen, focused region | Displayed provenance renders typed: author, work, date, voice, extent, citation and edition. |

## Conditional classes and why they are or are not here

- **Narrow / mobile reflow** — captured, at 393x852 and 320x852, for every state.
- **Forced colors** — captured, at 393x852, via `Emulation.setEmulatedMedia`
  `forced-colors: active`. The refusal keeps a visible rule, as `ForcedColorsTest`
  asserts structurally.
- **Print** — captured, at 1440x900, via `Emulation.setEmulatedMedia` `media: print`.
  This is deterministic page emulation, not a PDF export; the repository has no
  deterministic print-to-PDF harness and none was invented.
- **before/after pairs** — produced only for the two states whose shared copy this
  lane changes (`unsupported-voice-grc`, `malformed-address`). Every other state is
  byte-untouched by the diff, so a `before--` image would be identical by
  construction and is deliberately omitted rather than padded.

