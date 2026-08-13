# Catena E1 — V4.1 micro-correction handoff

## 1. Task and intended outcome

Answer the two review requirements V4 explicitly disclosed as **unmet**, and
nothing else:

1. the refusal copy was not made neutral;
2. the required screenshots were not produced.

Both are now done. The intended outcome is a fresh independent review of the
exact V4.1 head and this immutable package. **Not** acceptance, integration,
merge, re-signing or deployment.

This package supersedes nothing. It names, and does not mutate,
`build/agent-handoffs/20260813T142013Z-catena-e1-corrections-v4`
(SHA-256 `1f8fce78e3e8371ada1aee7bd12ec3fda69a306f5244472f95669b87a6d75516`,
re-verified byte-exact by this lane).

## 2. Branch

`impl/catena-wave-1-e1-corrections-v4-1` — not detached.

## 3. Commits

| | |
| --- | --- |
| review addressed | `9b1c23680c8da6b9a83bb7fb8ca689fbf9d2004c` |
| base (V4 head, exact parent) | `e40720d5d622e8b0528b8c714cc5caee0b21cee3` |
| **V4.1 head** | `f93757854b54c19e50bdcb97ca0fed9b48d22bb7` |

`e40720d5d..f93757854` is exactly **two** commits: implementation
`3fb6685b2c725adca9a1e0efb43cfdd55c68c311`, then records. Every measurement in
this package was taken at the implementation commit; the records commit touches
no code, which `commits.txt` proves with the exact git commands.

## 4. Uncommitted changes in the reviewed state

**None.** `git status` is clean at the reviewed head.

## 5. Focused files changed

| File | Change |
| --- | --- |
| `src/web/browser/catena/catena.js` | three string literals in `renderInvalid` — the only production change |
| `tools/tests/test_catena_wave_1.py` | seven wording pins moved; one narrow regression added |
| `PROJECT-WORK.md` | the V4.1 record (records commit only) |
| `guidance/corpus-browser-roadmap.md` | the V4.1 section, program-sequence state and ledger row (records commit only) |

Nothing else. In particular **nothing under `src/web/data/`**, no CSS, no
`catena-model.js`, no `index.html`, no shared shell, no release record, no
generator, no PDF, no protected Liturgy surface, no common gate.

## 6. Preview and exact startup commands

    make public-site                       # -> build/public-alpha/site
    node logs/capture-catena.mjs build/public-alpha/site <out-dir> "after--"

To view by hand, serve the built site and open, with required route state:

    /catena/index.html#book=Gen&chapter=1&bible=douay-rheims                          ordinary
    /catena/index.html#book=Gen&chapter=1&bible=douay-rheims&voice=translation:grc    THE CORRECTED REFUSAL
    /catena/index.html#book=Foo&chapter=1&bible=douay-rheims                          malformed, same umbrella
    /catena/index.html#book=Gen&chapter=10&bible=douay-rheims&voice=translation:en    supported voice, empty chapter
    /catena/index.html#book=Ps&chapter=13&bible=king-james-version                    numbering refusal

The site must be served over HTTP; opened as `file://` the page reports that no
data root could be reached.

## 7. Implementation summary

The V3 review accepted the fail-closed **mechanism** and rejected its **copy**:
"address could not be read" is imprecise for a value that parsed cleanly and is
merely unsupported. Its disposition was to keep the component and the
reason-specific detail, and to make the umbrella neutral.

Three shared strings changed:

| Sink | Before | After |
| --- | --- | --- |
| reference line | `Address not recognised` | `Address not used` |
| heading | `This address names what the page does not have` | `This address cannot be used as written` |
| status write | `The address could not be read; its invalid values are shown, unchanged.` | `The address is unchanged; the values not used are listed.` |

Each old string failed one of the review's tests: unreadability was untrue of a
parsed value, "does not have" asserted a holdings negative over addresses
refused on grammar, and "invalid values" located the fault in the reader. The
typed per-value reason is untouched, so unsupported and malformed refusals
remain distinguishable. Full rationale in `REFUSAL-COPY.md`.

Screenshots were produced with the repository's own headless Chromium. V4's
stated reason — "no display was available" — was incorrect; headless Chromium
needs no display server. See `SCREENSHOT-METHOD.md`.

## 8. Known limitations

See `LIMITATIONS.md`. In short: screenshots prove rendering, not
announcement; print evidence is CSS print-media emulation, not PDF; forced
colors is browser emulation, not a system high-contrast theme; and the wider
non-neutral phrasing elsewhere on the page was deliberately left alone.

## 9. Unresolved decisions

See `REVIEW_REQUEST.md`. The load-bearing one is the `src/web/data/` test
contradiction, preserved untouched for independent adjudication
(`DATA-TEST-CONTRADICTION.md`).

## 10. Artifact inventory

| Path | What it is |
| --- | --- |
| `HANDOFF.md` | this file |
| `REVIEW_REQUEST.md` | questions needing external judgment |
| `changes.patch` | the exact diff, base..head |
| `changed-files.txt` | the two changed paths |
| `checks.txt` | every check, its exact command and numeric exit status |
| `commits.txt` | base / head / review SHAs |
| `REFUSAL-COPY.md` | before/after copy, why each was non-neutral, the regression |
| `SCREENSHOT-METHOD.md` | capability probe, method, exact commands, honest limits |
| `VISUAL-STATE-INDEX.md` | every image: head, route/state, viewport, mode, requirement |
| `BASELINE-COMPARISON.md` | base vs head, with every difference classified |
| `DATA-TEST-CONTRADICTION.md` | the `src/web/data/` conflict, preserved |
| `UNRESOLVED-BLOCKERS.md` | separately owned blockers |
| `LIMITATIONS.md` | what this package does not prove |
| `PRIVACY-AUDIT.md` | sanitization method and result |
| `EVIDENCE-INDEX.md` | what each log/artifact shows |
| `MANIFEST.sha256` | SHA-256 of every member |
| `screenshots/` | 53 PNGs + 3 capture index JSONs |
| `logs/` | test, gate, check and build logs, plus the capture, comparison and sealing tools |

**Conditional classes deliberately omitted, with reasons:**

- **`sources/`** — omitted. This lane consulted no external source, corpus,
  edition or binding; it changed three English strings and took pictures. There
  is nothing to record. (The V3 review's "conditional-source omission rationale"
  finding is answered by this sentence, which is what it asked for.)
- **PDF artifacts** — omitted; no PDF is in scope.
- **Empty directories** — none created to imply evidence exists.
