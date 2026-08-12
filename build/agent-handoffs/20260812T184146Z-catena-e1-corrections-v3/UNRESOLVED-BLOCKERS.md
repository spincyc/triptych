# UNRESOLVED-BLOCKERS — outside-owner ledger

Every row is **open**. This lane marks nothing here complete, repaired nothing
here, and nothing in this package should be read as evidence that any of it was
satisfied. Rows are carried forward from the V2 package's ledger and from the
2026-08-12 independent review's finding matrix, with each row's V3 status
stated explicitly.

| # | Finding | Owner | This lane | Evidence | Remaining prerequisite |
| --- | --- | --- | --- | --- | --- |
| 1 | Wrong Psalm anchor — Psalm 13/14/100 text and address projection across Vulgate, Douay and KJV | Generator / shared-renderer owner | Untouched. V3 changes no model, numbering projection, generator or Scripture data. | Review finding 1 | Owner must prove or refuse actual projection. |
| 2 | Held/acquisition truth — overlapping lead identities and omitted confidence | Generator / data owner | Untouched. The route wording the review passed is unchanged. | Review finding 3 | Owner must reconcile overlapping identities and preserve confidence. |
| 3 | Licence/attribution projection — the real CC BY-SA record is not projected, so Severian truth remains `licensed` plus edition prose | Generator / data owner | Untouched. V3 types what the spine supplies; it projects nothing new and invents no licence fact. | Review finding 4, second half | Owner projects the real licence/attribution record. |
| 4 | Release binding — exactly the changed Catena route assets are unsigned | Release owner | **Still failing closed, deliberately, and NOT repaired.** V3 changes `src/web/browser/catena/catena.js`, so its actual digest differs again; the failure identity is unchanged (same paths, same recorded hashes, `stale: 3 stale binding(s)`). `refresh-release-bindings` was not run and this lane holds no authority to run it. | `logs/release-bindings-head.log`, `checks.txt` §E | Release owner adds the deterministic Catena-data root and re-signs only a reconciled accepted tree. |
| 5 | Shared-history `lastWritten` Forward suppression | B0 / shared shell owner | Untouched. V3 adds no history behaviour; the route-owned `selfWrote` mechanism the review passed is unchanged. | Review finding 5 | Owner retains the shared-core history work. |
| 6 | Real assistive-technology session | Pre-release evidence owner | Untouched, and **not attempted**. The V2 statement of *why* it was impossible was false and is corrected in `AT-LIMITATION.md`; the conclusion is unchanged. | `AT-LIMITATION.md` | Real-device-or-AT review before release. The review recorded this as an evidence prerequisite, not a Catena code defect. |
| 7 | Genuine system forced-colors palette | Pre-release evidence owner | Untouched. V3 changes no CSS at all; `src/web/browser/catena/catena.css` is byte-identical. | Review finding 7 | Remains a disclosed limitation rather than a separately established absolute prerequisite. |
| 8 | Shared shell seams — nested `main`, skip target, global focus/arrow, target size, shared-control reflow at 200% text | B0 / shared shell owner | Untouched. The browser gate's Catena rows still fail on `single-main-element` and `primary-controls-meet-target-size`; every control named is a shared shell/navigation link, not a Catena-owned control. | `BASELINE-COMPARISON.md` §2 | Owner retains wrapper, nested-main, skip-target, global focus/arrow, target-size and shared-control reflow work. |
| 9 | Common-gate voice-sample decision | Common browser-gate owner | Untouched. | Review finding 10 | Gate owner retains its decision. |
| 10 | Shared chapter loader's session-long transport-rejection cache | B0 / shared core owner | Untouched. The route's own eviction, which the review passed, is unchanged. | Review narrative following the matrix | Owner decides. |
| 11 | `check-tool-registry` — 8 sibling-declaration findings | Tool-registry owner | Untouched and unrelated to Catena. Present identically at the reviewed head. | `logs/make-k-check-head.log` | Owner declares the missing `requires` entries. |
| 12 | `check-examples` — 30 replay divergences | Various tool owners | Untouched. The one Catena-attributable divergence is row 4 seen through `tools/public-alpha verify --preview`. | `BASELINE-COMPARISON.md` §4 | Owners re-capture; the Catena one closes when row 4 does. |

## Rows this lane's own audit added, and did not fix

| # | Observation | Why not fixed here |
| --- | --- | --- |
| 13 | `src/web/browser/catena/catena-model.js` `formatExtent` concatenates `extent` members without typing, so a malformed `extent` could still reach the extent chip. | `src/web/browser/catena/catena-model.js` is SHA-256-pinned by the focused suite and is explicitly outside this lane's boundary. V3 types the chip's other inputs and leaves this one recorded rather than reaching across the boundary. No tracked data carries a malformed extent. |
| 14 | The shared `T.languageName` fallback is `String(code).toUpperCase()`, which would render `[OBJECT OBJECT]` for an object code. | Shared `src/web/browser/shared/browser-core.js` is B0/shared-shell owned. V3 closes the Catena-side door (`sound(fragment.language)`) so no untyped code reaches it from this route. |
| 15 | The invalid page's recovery link drops unrecognized hash keys. | Recorded in `STRANGER-KEYS.md` as actual behaviour. Changing it would be a URL-contract change the review did not ask for. |
