# Recovered attempts to fix Claude's non-converging workflow runs

On 18 September 2026 the maintainer asked for recovery of work in parallel
directories that had attempted to fix Claude's looping: the September Claude
runs of the `proper` and `proper-finish` workflows that cycled through
evaluation and revision without reaching acceptance. A read-only survey
compared every local clone and every related remote branch with `origin/main`.
It covered 44 local repositories, their stashes, dirty trees, untracked files and `.scratch`
notes, and 15 engine-touching remote branches. Origin history has been
rewritten since some of those clones were made, so ancestry was not trusted:
commits were matched by engine-path patch-id, full patch-id and subject, and
unmatched items were checked against the current engine and guidance text.

## What was already fixed on `main`

The v25 advisory ratchet, where lanes re-filed their own advisories as blocking
because an advisory reached no stage, was closed on `main` by `3be1a1f9e`
(advisories travel with the repair) and `fba3974a9` (an advisory outlives the
reviser the route chose). `555a7465e` records the analysis. No unmerged code
fix for that loop exists in any surveyed location.

| Item surveyed | Status |
| --- | --- |
| `origin/claude/tpt-*`, `origin/codex/tpt-seed-idempotency`, a stash of `claude/tpt-execution-policy` | On `main` (patch-id matches; stash files byte-identical to `fb03aadbf`) |
| `b55ea6c18`, owner change is not a repeat | On `main` as `9e2938a55` |
| `ca4278eeb` and its copies `80b0c4032`, `2f04927c3` (`PREVIOUS_FINDINGS` header; refusal of a reused finding id) | Superseded by the opposite design in `6b601e3e0`, `6235d4a3f`, `5e148caf2`: ids are handles and the budget reads `finding_dispositions` |
| `46fbd0072` (one id, one defect; 200 dpi review rasters) | Superseded: the resolution change is `2ed8f4214`; the id rule by `6b601e3e0` |
| `af5abc2ae` / `d31fedd43` (reconciling two budget rewrites) | Superseded by `5e148caf2` |
| Driver notes, lane-brief template and draft diagnosis | Superseded by `HANDOFF-proper-55-blocked.md`, `HANDOFF-proper-56-convergence.md` and `555a7465e`; retained here as history |

## What existed only in a disposable workspace

The `claude/propers/tlm/merge` workspace had no remote branch. Its ignored
`.scratch/tpt/` held the only copies of three records, now preserved here
verbatim except that one private checkout path is replaced by a placeholder
in three files. `ORIGINAL-SHA256SUMS` records the unredacted originals.

- [`proper-finish-cold-review-2026-09-10/`](proper-finish-cold-review-2026-09-10/FINDINGS.md):
  an 18-finding cold review of `proper-finish`, requested by the maintainer on
  10 September, and its authorized sequence. Items 1.1, 1.3, 2.6 and 2.7 later
  landed in `9f7674645`. The survey verified 1.5, 2.5, 3.1, 3.2, 3.4, 4.1 and
  4.2 absent from `main`; 1.2, 1.4 and 2.1–2.4 were not rechecked.
- [`driver-handoff-2026-09-11/`](driver-handoff-2026-09-11/HANDOFF.md): the
  Claude driver's handoff for leaves 54–56. Its 4b, 4c and 4e are on `main`
  (`9f7674645`, `fba3974a9`).
- `driver-handoff-2026-09-11/validate-lanes.py.txt`: that driver's pre-join
  validator for fan-out lane results, kept as text because it hard-codes
  `proper-finish.json` and one checkout. `_workflow.py` refers to "the
  pre-advance validator", but no validator is tracked.

`loop-runs-summary.json` is a derived per-result summary of the eleven Claude
run directories that were the primary evidence of the loop. It lists each
stage, iteration, disposition and finding-severity count, with the retained
result and state hashes. The run directories themselves are ignored build
state of up to 1.6 GB each and are not preserved.

## Still open

The maintainer then authorized engine changes wherever both the defect and
its fix are clear. Two were repaired in the same session:

- Cold review 4.1 is fixed in `scripts/_workflow.py`. A finding now travels as
  a forwarded finding whenever its own route leads to the stage the winning
  route chose, so a mixed `derivation`/`seam` round hands the reviser both
  kinds to account for. `tools/tests/test_workflow_shared_reviser.py` fails
  5 of its 6 cases without the change. No `proper-study` route shares a
  reviser, and both live `proper-study` runs replayed byte-identically after
  it.
- The `_check_review_scope` docstring no longer cites a pre-advance validator
  as if one were tracked.

Five of the six below remain open; cold review 4.1 is repaired, as the row
naming it says. The rest are recorded, not repaired. They belong to the legacy `proper` and
`proper-finish` workflows. The `proper-study` successor routes each review's
findings to one owner per repair target and carries upstream routes from
every review. Items 4.2 and 4d would change shared fragments that a live
`proper-study` run is bound to by digest. The others lack a single clear fix.

| Id | Open defect | Proposed remedy in the source record |
| --- | --- | --- |
| Cold review 4.1 (repaired, above) | In `proper-finish`, `synthesis-evaluation` routes both `derivation` and `seam` to `synthesis-revision`, but the engine forwards only the findings naming the winning route. Seam findings arrive only as carried findings, so they are never reported `not-repaired` and never charge the repeat budget. This is the same budget blindness as the v25 ratchet. | Forward every finding whose route resolves to the chosen transition (about four lines in `_workflow.py`) |
| Cold review 4.2 | Two lanes' partitions can produce findings that cannot both be satisfied, so the run oscillates silently | One `result-format.md` paragraph on contradictory findings |
| Handoff 4a | The "seam" defect class (a clause true in the canonical edition and false in the companion) was carried only by driver memory | Encode the class in a gate or fragment |
| Handoff 4d | An evaluator can mark a defect `accepted` against explicit guidance, for example a rights-only final page | Require accepted findings to cite the guidance checked; give lane fragments the guidance loci their criteria touch |
| Handoff 4f | A canonical defect found after `content-evaluation` passes has no repair owner in `proper-finish` | Structural; re-seeding was the only route |
| Handoff §7 | Visual and web evaluation lanes cannot see finding ids from earlier rounds | Narrow `PREVIOUS_FINDINGS`-style context for those stages |

The Claude `proper-study` production for the Seventeenth Sunday after
Pentecost, driven the same day, records its own cycles in its leaf's
`research/production-review.md`. It tests whether the successor workflow
converges for Claude.
