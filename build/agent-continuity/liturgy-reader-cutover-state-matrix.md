# Liturgical Instrument cutover state compatibility

## Method and classifications

This matrix compares the legacy canonical controllers at the clean planning
boundary `7b7044dea7f5c35a2d32ff85f26eb5b182bf40ef` with the independently
accepted production readers after compatibility commit
`3f3949617a04ffa68a1070058d0f7bc5ac74dc93`. It combines source tracing,
state/adapter fixtures, and the current Chromium parity harnesses. The
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
| D12 | Empty first visit | local date, first rubrics row = postconciliar | local date, declared Propers default = Roman 1962 | accepted intentional difference | Roman 1962 public default expressly accepted; deterministic test fixes only date |
| D13 | Existing `why=1` | renders current calendar/rubrical explanation | production-derived subordinate branch apparatus, no self-link | exact match | direct/reload/Back/Forward, source loci, held Latin, no fabricated seat |
| D14 | Multiple territorial branches | shows all held production outcomes | shows all held branches with source headings and namespaced locations | exact match | no geography/array preference; both branches, reload, history, territorial Why |
| D15 | Remembered preferences | current Day ignores storage | accepted Day intentionally normalizes with empty remembered state | exact match | URL/default only; storage cannot override |
| D16 | Date-dependent harness result | current date may honestly carry partial coverage | same; prior test assumed notice hidden | unrelated pre-existing behavior, corrected test | freeze test browser clock at local noon 2026-08-02; product clock untouched; Day 40/40 |

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
| P10 | Cycle/alternative/translation witness | no stable current public key contract | stable `cycle`, `alternative`, `translation-witness`; aliases input-only | exact match | parse/validate/serialize/direct/reload/Back-Forward; invalid explicit fails closed |
| P11 | Remembered preferences | current route does not remember | candidate uses URL, then safe remembered missal/Bible/orations, then defaults | accepted intentional difference | accepted M1 precedence; invalid remembered value falls to declared default |

## Cross-route, publication, and navigation differences

| ID | State | Finding | Classification | Required resolution |
| --- | --- | --- | --- | --- |
| X01 | Relative assets/data | all four pages share the same directory and `../browse` default | exact match | in-place promotion, no redirect/build alias |
| X02 | Candidate indexing | retained source and built candidates carry full static noindex; no public canonical/social advertising | exact match | source/build/deployed metadata asserted before JavaScript |
| X03 | Canonical metadata | runtime titles/diagnostics are route-neutral; cutover patch owns canonical description/indexability | exact match | no visible candidate/internal wording; canonical omits robots |
| X04 | Cross-entrance/context navigation | direct destinations move from legacy footer to subordinate Details | accepted intentional difference | counterpart first; context links readable/keyboard-reachable desktop/mobile |
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
- Cutover blockers: none remain at the compatibility layer. Empty-Day default,
  `why=1`, territorial outcomes, stable Propers names, retained indexing,
  route-neutral wording, and Details navigation are resolved and evidenced.
- Unrelated pre-existing behavior: the now-determinized date-dependent Day test
  cause, ten-minute Pages cache behavior, and governed example-transcript gate.

No unexplained material difference is accepted. Public cutover execution is
still unauthorized: the compatibility bytes and regenerated exact patch require
narrow independent acceptance before a later clean execution agent may apply it.
