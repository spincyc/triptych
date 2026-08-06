# Liturgical Instrument cutover state compatibility

## Method and classifications

This matrix compares the current canonical controllers at
`7b7044dea7f5c35a2d32ff85f26eb5b182bf40ef` with the independently accepted
Day/Propers production-reader candidates. It combines source tracing, existing
state/adapter unit fixtures, and the current Chromium parity harnesses. The
machine-readable companion is
`liturgy-reader-cutover-state-matrix.json`.

Classifications mean:

- **exact match** — same valid identity/text/state meaning or same required
  route behavior;
- **accepted intentional difference** — already required by accepted
  fail-closed, Browse, shell, focus, or visual architecture;
- **cutover blocker** — requires an explicit plan disposition or bounded
  compatibility implementation before execution;
- **unrelated pre-existing behavior** — known behavior outside the cutover
  diff, retained honestly.

## Day

| ID | State | Current canonical | Accepted candidate | Classification | Proof / required execution assertion |
| --- | --- | --- | --- | --- | --- |
| D01 | Governing Roman deep link, 2026-08-05 | parses date/missal/Bible and renders resolved Proper | strict parser resolves same identity and Proper | exact match | canonical and candidate identity/text/citations/order; direct load and reload |
| D02 | Another date, Roman 2026-08-02 Read | Roman Propers-only | same Roman Read semantic projection | exact match | existing candidate/current parity and semantic fixture |
| D03 | Postconciliar 2026-11-29 Read | postconciliar Propers-only | same identity, cycle, Proper order/text | exact match | both-edition parity fixture |
| D04 | Bible/orations selection | hash selects held editions/languages | same public keys and held values | exact match | state round-trip plus rendered text/citation parity |
| D05 | Roman/postconciliar Missal | `ordinary=1` seats production Ordinary/Propers | same public flag, renderer, seating, events | exact match | both-edition Ordinary/Proper text and seat parity |
| D06 | Reload/direct link | hash reproduces selection | hash reproduces validated selection | exact match | browser reload/direct navigation |
| D07 | Back/Forward Read↔Missal | hash rerender with coarse focus | `pushState`, committed render, semantic location | accepted intentional difference | accepted state/focus/race ownership must remain stronger |
| D08 | Malformed/unsupported explicit state | often falls back or retains current value | rejects explicit invalid state and exposes no stale semantic selection | accepted intentional difference | fail-closed is frozen; never weaken for legacy smoothness |
| D09 | Partial/incomplete coverage | explicit notices/text | same source facts with compact hierarchy | accepted intentional difference | exact absence reasons/text; accepted warning presentation |
| D10 | Date/Contents/Mode/Details open/close | native flow disclosures | modal surfaces, inert background, Escape and focus return | accepted intentional difference | accepted shell behavior and URL unchanged while modal |
| D11 | Scroll/semantic restoration | limited DOM focus behavior | stable semantic event capture/restoration | accepted intentional difference | mode and history transitions retain equivalent semantic location |
| D12 | Empty first visit | local date, first rubrics row = postconciliar | local date, declared Propers default = Roman 1962 | cutover blocker | independent review must accept one public default; test clock fixes only the date |
| D13 | Existing `why=1` | renders current calendar/rubrical explanation | retains key but defers and links `day.html` | cutover blocker | must integrate compatibility or expressly narrow; no post-cutover self-link |
| D14 | Multiple territorial branches | current route retains its production resolution UI | fails closed and links current `day.html` | cutover blocker | no geography/array inference and no recursive canonical link |
| D15 | Remembered preferences | current Day ignores storage | accepted Day intentionally normalizes with empty remembered state | exact match | URL/default only; storage cannot override |
| D16 | Date-dependent harness result | current date may honestly carry partial coverage | same; prior test assumed notice hidden | unrelated pre-existing behavior, corrected test | freeze test browser clock at local noon 2026-08-02; product clock untouched; expect 34/34 |

## Propers

| ID | State | Current canonical | Accepted candidate | Classification | Proof / required execution assertion |
| --- | --- | --- | --- | --- | --- |
| P01 | Governing Roman seasonal deep link | renders Advent 1 | same production Proper identity/text | exact match | candidate/current text parity and state fixture |
| P02 | Supported Roman sanctoral | renders explicitly named mass key | same edition-qualified formulary | exact match | derive exact key from structure; no nearby fallback |
| P03 | Empty first visit | selects first type/formulary by order | opens Browse and selects no liturgical text | accepted intentional difference | vision forbids arbitrary first-formulary choice |
| P04 | Missal/Bible/orations | five public hash keys | same five public keys; URL beats remembered values | exact match | explicit deep link and storage precedence fixture |
| P05 | Browse selector | nested canonical production selector | same production Browse & edition model in modal surface | accepted intentional difference | selector option identity/order preserved; shell interaction accepted |
| P06 | Reload/direct link | hash reproduces selection | strict hash reproduces selection | exact match | direct navigation and reload |
| P07 | Back/Forward | hashchange rerender | coalesced popstate/hashchange with winning render | accepted intentional difference | identity and state restored without duplicate render |
| P08 | Malformed/unsupported explicit state | may retain/fall back | fail closed without selecting by order | accepted intentional difference | frozen fail-closed behavior |
| P09 | Modal open/close | native disclosure | modal/inert/Escape/focus restoration | accepted intentional difference | URL intact and four actions named/reachable |
| P10 | Cycle/alternative/translation witness | no stable current public key contract | candidate writes `_candidate-*` keys reachable from production data | cutover blocker | stable public names or explicitly gated states required before cutover |
| P11 | Remembered preferences | current route does not remember | candidate uses URL, then safe remembered missal/Bible/orations, then defaults | accepted intentional difference | accepted M1 precedence; invalid remembered value falls to declared default |

## Cross-route, publication, and navigation differences

| ID | State | Finding | Classification | Required resolution |
| --- | --- | --- | --- | --- |
| X01 | Relative assets/data | all four pages share the same directory and `../browse` default | exact match | in-place promotion, no redirect/build alias |
| X02 | Candidate indexing | deployed candidate raw HTML is currently `index, follow`; runtime noindex is ineffective because layout already supplies robots | cutover blocker | source-declare repository noindex on retained candidates and suppress public OG/canonical advertising |
| X03 | Canonical metadata | candidate source/runtime titles and diagnostics say internal/candidate; canonical titles are public | cutover blocker | route-neutral runtime wording plus canonical public title/description/indexing |
| X04 | Cross-entrance/context navigation | canonical footers have direct exits; Instrument hides generated chrome and has Home only | cutover blocker | independently approve quiet counterpart/context access or expressly accept removal |
| X05 | Service worker | none exists | exact match | introduce none |
| X06 | Static cache | unversioned files and Pages `max-age=600` affect forward and rollback deployments | unrelated pre-existing behavior | compatible mixed-cache bytes; bypassed and post-expiry verification |
| X07 | Full repository gate | unrelated stored example transcript divergence stops `make check` | unrelated pre-existing behavior | record exact exit; do not recapture/bless or call full gate green |

## Difference disposition summary

- Exact matches: valid core Day and Propers deep links, relative data/assets,
  source identities, Proper/Ordinary text and order, Bible/oration selection,
  reload/direct links, Day storage independence, and no service worker.
- Accepted intentional differences: strict explicit-invalid failure, Propers
  Browse first visit, modal/focus/location/race behavior, remembered Propers
  precedence, and accepted warning/composition hierarchy.
- Cutover blockers requiring independent disposition: empty-Day edition
  default, `why=1`, territorial fallback, public option-key spellings, retained
  candidate indexing/metadata, canonical candidate wording, and direct
  cross-entrance/context navigation.
- Unrelated pre-existing behavior: the now-determinized date-dependent Day test
  cause, ten-minute Pages cache behavior, and governed example-transcript gate.

No unexplained material difference is accepted. The selected same-path
mechanism is executable only after all cutover blockers receive recorded
dispositions and the proposed patch is regenerated to match them exactly.
