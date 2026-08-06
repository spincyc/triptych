# Liturgical Instrument public-cutover plan handoff

## Disposition

Candidate for narrow independent planning review. No cutover execution or
public-navigation change is authorized.

Planning began from clean synchronized commit
`7b7044dea7f5c35a2d32ff85f26eb5b182bf40ef`. Architecture checkpoint
`c7124de25` records the route/state/navigation maps and selected mechanism.
Test-only commit `5e1b82b51` makes the Day first-visit assertion deterministic;
record checkpoint `2cf91dd01` carries its durable proof and the exact
task-owned promised-ledger count updates.

## Selected mechanism

A later separately authorized cutover should promote the accepted reader
DOM/load graphs behind unchanged source filenames:

- `src/web/browser/liturgy/day.html`
- `src/web/browser/liturgy/index.html`

No redirect, rename, rewrite, client forwarder, or build-only alias is used.
The accepted candidate routes and visual oracle remain deployed, unlinked, and
unchanged through the initial acceptance window.

## Important patch qualification

`PROPOSED-CUTOVER.patch` is an exact mechanical same-path promotion draft, not
an executable cutover patch. It is intentionally incomplete while the
reviewer dispositions in `CUTOVER-DECISION.md` remain open. Its header forbids
application. The later execution patch must be regenerated after those exact
decisions; this prevents accidental publication of recursive Day fallback,
provisional public state keys, indexable retained candidates, internal wording,
or lost cross-entrance navigation.

## Validation disposition

- Day browser: 34/34 after the bounded empty-URL clock fixture.
- Propers browser: 27/27.
- Shared-shell browser: 18/18.
- Governed Instrument: 19/19, no browser hygiene failures.
- Focused non-publication Python: 142/142.
- Locked-publication Python: 82/82 with Markdown 3.10.2.
- System-Python publication run: 8 errors caused solely by installed Markdown
  3.10.3 versus lock 3.10.2; the locked run is green.
- Promised ledger: 23 tracked, 17 complete.
- Tool registry: 34 tools.
- Release bindings: exact, 0 stale.
- Locked public-alpha check/build/Pages verify: pass.
- Governed full gate: exit 2 at 23 unrelated divergent and 35 known-stale
  examples among 188 replayed; two task-owned ledger examples replay 2/2.

No unrelated example transcript was recaptured or blessed.

## Product-byte isolation

Canonical source hashes, unchanged from the starting boundary:

- Day HTML: `bc5a98de6b718431f3b91e6a133bb847c2dcdf4d21fce6f45aae3ad4984de868`
- Propers HTML: `f630f4a66f3f525144336f183b1485c698030c7531ff679375b3a7aa00150c65`

The candidate/oracle hash inventory is in `logs/checks-summary.txt`.

## Deployment observation

Latest successful planning-boundary Pages run is `31127811306` for
`7b7044dea7f5c35a2d32ff85f26eb5b182bf40ef`. The exact accepted integrated
product deployment remains run `31125898045` for
`5444d89fc9b379a1babef5b2220323fe1508b2b3`. No Actions record had materialized
for the planning-only pushes when last queried; no deployment claim is made for
them.

## Integrity

`PLAN-AND-CONTINUITY.md` is byte-identical to the canonical continuity file at
seal time. `MANIFEST.sha256` is generated last and verified from this directory.
The transport ZIP is verified for integrity and exactly one top-level directory;
its SHA-256 is recorded in the outer repository continuity/closeout response.
