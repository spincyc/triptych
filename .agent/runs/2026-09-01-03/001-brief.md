---
protocol: relay-v1
run: 2026-09-01-03
turn: 001
role: planner
agent: gpt-5.6-sol
branch: feature/catena-omnia/co-03-scale-benchmark
base: 09437907472581df4a8969010bd494249a3539a5
---

## Objective

Execute Catena Omnia CO-03 as a real, reproducible scale benchmark against released Catena E1 behavior. Measure whether the current static-first generator/data/browser architecture remains adequate as the corpus grows across the whole canon and inside very deep chapters. Produce benchmark tooling and a durable evidence-backed decision that directly constrains CO-04 acquisition hardening.

The outcome must be measurable forward progress, not another conceptual architecture review: synthetic/public-safe fixtures exercising the real Catena schema and renderer, repeatable commands, machine-readable measurements, and an explicit architecture disposition based on observed scaling behavior.

## Scope boundary

You own only `feature/catena-omnia/co-03-scale-benchmark` and the relay artifacts for run `2026-09-01-03`.

Start from exact released main `09437907472581df4a8969010bd494249a3539a5`, where Catena E1 is merged, release-bound, and live. This benchmark deliberately runs in parallel with a separate B0/B1 convergence/integration lane. Do not depend on that lane landing first and do not edit shared shell/foundation files merely to make the benchmark easier.

You may add or modify benchmark/test tooling, synthetic fixture-generation support, and a concise durable benchmark report/record. Synthetic fixture output must live under an existing ignored/build/test-fixture location and must never enter production `src/web/data` as if it were real corpus evidence. You may make only the smallest non-production seam necessary to run production Catena code against fixture data; do not change accepted Catena product semantics.

Do not acquire real commentary, alter Source Library records, edit protected Liturgy, start Search/relationships/advanced views, change release bindings, merge/deploy/sign, or implement a new chunking architecture in this lane. If the benchmark proves architecture change is needed, record the measured requirement and stop; that implementation belongs to the next lane.

## Acceptance criteria

1. **Re-derive the real baseline.** From the exact checked-out tree, derive current Catena fragment/book/canon counts and current route/data sizes. Do not copy historical `1,351 / 1 / 73` numbers without reproducing them.

2. **Use the real schema and real production model.** Fixtures must flow through the same Catena structure/fragment shapes, canonical locus rules, voice/translation states, natural extents, refusals/absence semantics, and browser model used by production. Do not create a toy benchmark whose data bypasses the generator/model contracts being measured.

3. **Build three composite fixture families, not dozens of micro-fixtures.** Each fixture should exercise multiple orthogonal dimensions at once:
   - `wide-canon`: shallow commentary distributed across many books and chapters, sufficient to expose whole-canon index/manifest scaling;
   - `deep-chapter`: the same chapter at approximately 10, 100, 500, and 1,000 held fragments, with varied authors, works, dates, extents, and voices;
   - `mixed-truth`: held originals/translations, translation absence, blocked/lead/refusal states, cross-chapter natural extents, projection refusal/unsupported cases, and at least one malformed case that must fail safely.
   Synthetic text must be obviously fixture text and public-safe. It must never look like historical commentary in production output.

4. **Measure generator scale.** For each relevant fixture point record wall-clock time, peak memory using a portable mechanism available on the host, generated file count, uncompressed bytes, gzip-9 bytes, and any superlinear growth. Avoid relying on `/usr/bin/time`; use Python/Node timing/resource APIs or another repository-portable approach.

5. **Measure browser/transport scale in real Chromium.** Using the built fixture artifact and the repository's existing dependency-free CDP conventions, measure at minimum:
   - initial HTML/CSS/JS bytes;
   - data requests and bytes before Scripture is visible;
   - requests and bytes before first held commentary is visible/openable;
   - per-chapter manifest bytes compressed/uncompressed;
   - fragment-text requests for representative reading patterns;
   - main-thread/render elapsed time for 10/100/500/1,000-fragment chains;
   - browser memory or a stable CDP proxy before and after the deep-chain run;
   - cold versus repeated-load behavior/cache evidence;
   - URL/hash/history selection behavior at deep scale;
   - browser find behavior across lazy commentary if currently supported, or an explicit measured limitation if not.

6. **Accessibility/truth under stress is sampled, not postponed.** On at least the 1,000-fragment and mixed-truth fixture, prove one coherent keyboard path, useful heading/landmark structure, no document-level overflow at 320 CSS px, and truthful no-JavaScript/failure behavior. Do not turn this into a full visual-acceptance matrix; the purpose is to catch scale-caused architectural breakage, not redo E0/E1 design review.

7. **No fake completeness.** The wide-canon fixture must include empty/unsolved chapters as well as solved ones, and the benchmark must prove that scale machinery does not turn absence into an implied corpus claim. Synthetic coverage counts must be labelled as fixture measurements only.

8. **Produce reproducible tooling.** Add one canonical command (or a small documented pair) that regenerates/runs the benchmark from a clean checkout without manual fixture editing. The command must cleanly separate production source from generated benchmark artifacts and leave the worktree clean after ordinary use.

9. **Produce machine-readable and human-readable results.** Commit a compact JSON/CSV measurement artifact only if repository guidance permits tracked benchmark evidence; otherwise commit the harness and a durable Markdown report containing the measurements and identify the ignored generated result path. The report must include slopes/knee points, not just raw terminal output.

10. **Make one explicit CO-03 disposition.** End with exactly one primary decision:
   - `CURRENT_SCHEME_ADEQUATE_FOR_NEXT_ACQUISITION_WAVE`;
   - `BOUNDED_MANIFEST_PARTITIONING_NEEDED`;
   - `FRAGMENT_METADATA_TEXT_SPLIT_NEEDED`;
   - `SEARCH_INDEX_MUST_BE_SEPARATE_LAZY_ARTIFACT`;
   - `OTHER_MEASURED_ARCHITECTURE_CHANGE_NEEDED`.
   Multiple secondary observations are allowed, but one decision must govern CO-04. State the first observed bottleneck and the scale at which it appears.

11. **Do not optimize speculatively.** No framework migration, server assumption, service worker, new public chunking layout, or production data rewrite belongs in this lane. If current architecture remains adequate through the tested envelope, say so and move on to acquisition rather than polishing the benchmark.

12. **Stop at pushed benchmark evidence.** Commit/push the tooling and durable report, return exact work SHA(s), commands, baseline and fixture metrics, Chromium version, disposition, and the smallest next CO-04 action. Do not self-integrate.

## Verification

Read `AGENTS.md` and `tmt.json` first and use existing tools before inventing new scripts. At minimum, preserve and run:

```text
python3 scripts/_catena.py check
PYTHONDONTWRITEBYTECODE=1 python -m unittest tools.tests.test_catena
make check-browser-static
make public-preview
git diff --check
```

Run the new benchmark command from a clean state at least twice enough to demonstrate reproducibility of structural counts and stable order-of-magnitude timings. Run focused tests for fixture isolation and failure safety. Use real Chromium; a skip-only browser benchmark is `blocked`, not complete.

After benchmark generation/execution, prove production Catena source and production generated data remain unchanged from the branch base unless the brief explicitly permitted a non-production harness seam. `git status --short` must be clean before result preparation except for the result file itself.

## Context

Read current main versions of:

- `AGENTS.md`
- `guidance/catena.md`
- `guidance/corpus-browser-vision.md`
- `guidance/corpus-browser-roadmap.md`
- `guidance/web-data.md`
- `guidance/sources.md`
- `guidance/versification.md`
- `PROJECT-WORK.md`
- `tmt.json`
- `scripts/_catena.py`
- `tools/tests/test_catena.py`
- current Catena browser/model/route files under `src/web/browser/catena/`

The recovered long-horizon Catena Omnia roadmap exists at exact donor commit `639b9a6fc84b9a169948b951b59972acae24b0a2` as `guidance/catena-omnia-roadmap.md`; its CO-03 direction is restated fully in this brief, so you do not need another relay run's context. You may inspect that ordinary repository file at the exact commit if useful, but do not read other `.agent/runs/` directories.

Product invariants to preserve while benchmarking:

- Scripture is the anchor;
- only held L3 text renders as commentary text;
- canonical locus identity precedes display projection, and projection refusals stay refusals;
- fragment natural extent is the stored truth;
- chronology/attribution/voice/edition/rights remain distinct;
- static-first and lazy text transport are preferred until measurements prove otherwise;
- synthetic fixtures are test data, never corpus claims.

The purpose of CO-03 is to prevent two opposite mistakes: scaling the architecture before there is evidence it needs scaling, or multiplying commentary acquisition on an architecture whose first real deep chapter will collapse.

## When blocked

Follow relay-v1 preflight and blocked-channel rules exactly. Do not improvise around a dirty checkout, wrong repository/branch, stale brief, failed fetch/push, rebase/merge state, protocol mismatch, or unavailable real Chromium.

If production code cannot be exercised against isolated fixture data without changing accepted semantics, report `partial` with the exact missing seam and the smallest proposed seam; do not quietly benchmark a toy substitute. If real Chromium cannot be driven, report `blocked` with the missing capability. If timings are noisy, report distributions/ranges and structural measurements rather than fabricating precision.
