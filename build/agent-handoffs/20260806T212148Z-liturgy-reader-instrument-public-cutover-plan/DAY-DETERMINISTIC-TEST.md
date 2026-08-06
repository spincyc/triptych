# Deterministic Day first-visit gate

## Finding

The disclosed 33/34 Day-browser result was caused exactly by wall-clock drift,
not by product behavior. The first-visit assertion opened an empty URL and
expected no partial-coverage notice. On 2026-08-06 the production default date
correctly produced a partial Roman-1962 coverage notice, so only that assertion
failed; all browser hygiene counters remained zero.

## Bounded correction

Commit `5e1b82b51` changes only
`tools/tests/day_reader_integration_browser.mjs`. Immediately before the
first-visit navigation, the harness installs a Chrome DevTools Protocol
`Page.addScriptToEvaluateOnNewDocument` clock fixture whose local civil time is
noon on 2026-08-02. The test still opens an empty URL, still exercises the
production default-date path, and now additionally asserts the exact committed
`civilDate` value `2026-08-02`. The fixture is removed in `finally`.

The assertion was not deleted or broadened, and no Day HTML, CSS, JavaScript,
calendar data, default-date rule, URL behavior, candidate route, canonical
route, or visual-oracle byte changed.

## Validation

Before correction:

- `node tools/tests/day_reader_integration_browser.mjs` — exit 1, 33/34; only
  `first-visit default follows the Propers declared default` failed because the
  coverage notice was visible on the wall-clock date.

After correction:

- `node --check tools/tests/day_reader_integration_browser.mjs` — exit 0.
- `node tools/tests/day_reader_integration_browser.mjs` — exit 0, 34/34;
  console errors 0, failed requests 0, HTTP errors 0, unnamed controls 0,
  duplicate IDs 0, horizontal-overflow failures 0.
- `python3 -m unittest -v tools.tests.test_day_missal_integration` — exit 0.

This is a task-owned deterministic test correction, not a product change and
not authorization to execute public cutover.
