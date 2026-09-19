# Delta recovery of attempts to fix Claude's non-converging runs

On 19 September 2026 the maintainer asked again for recovery of work in
parallel directories that had attempted to fix Claude's looping. The
[2026-09-18 record](../claude-loop-recovery-2026-09-18/README.md) already
answers that request for the state it surveyed. This record is a delta against
it: what that survey did not mention, what has changed since, and the six
cold-review items it left unchecked. It repeats none of its classifications.

A read-only survey lane compared every clone it could find with `main` at
`0b0832a41`. It ran no fetch, checkout, stash, commit or write in any clone.
Because origin history was rewritten, ancestry was not trusted: engine-path
commits absent from `main` were matched by engine-path patch-id, full
patch-id, subject and changed-line sets, and every engine-path blob at every
ref tip, `HEAD` and stash was tested for membership in `main`'s object set.
Unreachable commits were listed to find dropped stashes. The engine paths are
`scripts/_workflow.py`, `tools/tpt`, `workflows/` and
`tools/tests/test_workflow*`.

## What the survey established

| Question | Answer | Kind |
| --- | --- | --- |
| Has anything outside this workspace changed since 2026-09-18? | No. No file, reflog entry or stash is newer in any other workspace or canonical clone. | fact |
| Has the remote moved? | No. The 103 `origin/*` refs equal the live branch list by name and sha. | fact |
| Does unmerged engine code that attempts to fix the loop exist? | No. Every engine-path commit not reachable from `main` (106 in the listed locations, 76 more beyond them, 99 unreachable) is on `main` by patch-id or content, or is superseded as the earlier record says. | fact |
| How many repositories were covered? | 111: 88 under the worktrees directory, two canonical clones and 21 found elsewhere. Which 44 the earlier survey counted is not recorded, so none can be called new to the record. | fact; the comparison is not possible |

The earlier record says a stash of `claude/tpt-execution-policy` is
byte-identical to `fb03aadbf`. The survey found twenty of its 22 files so; the
two workflow manuals differ by a few lines of draft wording, and its task brief landed
separately as `e80516bdb`. Nothing in it is absent from `main` in substance.

## Four items that existed nowhere on `main`

None is a fix for the loop, and the survey's evidence does not support calling
any of them one. They are recovered because each lived only in a disposable
workspace, and two of them bear on how Claude runs are driven. Each file below
is byte-identical to its original; none contains a private path, host or user
string, and `SHA256SUMS` records them.

| Item | Where it lived | What it is | Disposition |
| --- | --- | --- | --- |
| [`leaf-54-last-loop-run/742bda9ac-author-proper-iteration-0.patch`](leaf-54-last-loop-run/742bda9ac-author-proper-iteration-0.patch) | One unpushed commit on a workspace branch with no remote | `author-proper` iteration 0 of run `3c3fb16baa13ee6b`, the last Claude loop run: five files of the held Claude Fourteenth Sunday leaf, repairing `CON-CIT-110` and `CON-CIT-107` | **Recorded, not applied.** It is one unevaluated authoring pass on a held leaf from a run that never finished. Applying it would publish nothing and would put unreviewed prose under a leaf whose hold is recorded. It is kept as a patch so the repair is not lost with the workspace. |
| [`leaf-54-last-loop-run/run-3c3fb16baa13ee6b-blocking-findings-v1.toml.txt`](leaf-54-last-loop-run/run-3c3fb16baa13ee6b-blocking-findings-v1.toml.txt) | An uncommitted modification in the same clone | The engine-written standing-findings record of that run's `content-evaluation` iteration 0 under `proper-finish` v7: 16 blocking findings, 5 advisories, 13 observations. The earlier record's `loop-runs-summary.json` has this run's counts and not its finding texts. | **Recovered as evidence.** Kept as `.txt` so no tool reads it as a live record; `main` still carries the leaf's older schema-1 record, which is untouched. |
| [`pinned-effort-agents/`](pinned-effort-agents/) | A workspace root, outside any clone | Three Claude Code subagent definitions, `tpt-high`, `tpt-xhigh` and `tpt-max`, each pinning one reasoning effort so a driver can dispatch a stage at the level its packet declares | **Recovered, and the reason both Claude `proper-study` runs deviated.** See below. |
| [`codex-driver-validators/`](codex-driver-validators/) | An ignored `.scratch` of a Codex workspace | The Codex driver's pre-join validators for fan-out lane results and its outgoing-range audit, from a GPT run that converged. They hard-code one run id and its lane lists. | **Recovered as history**, beside the Claude driver's validator the earlier record keeps. `proper-study` has no fan-out stage, so nothing consumes them today. Kept as `.txt` for the same reason as the other. |

### The pinned-effort definitions and the host deviation

Every packet declares a reasoning effort and the operator manual says it is
workflow data, not a host choice. A Claude Code harness subagent inherits its
driver's effort unless its agent definition pins one. Both Claude
`proper-study` runs, `1e02dc05f2df9940` and `472e2eb20876b22a`, were driven
from sessions at `xhigh`, so every author stage declared `high` ran one level
above its declaration, and each run records that as its intervention 0000.

These three definitions are the driver-side answer, written on 3 September by
an earlier Claude driver and never tracked. They could not be used in either
run. The harness loads agent definitions when a session starts, from the
directory it starts in; on 19 September the driver tried to install them into
its workspace and the host's permission policy refused the write as
self-modification, which the driver did not work around. Run
`472e2eb20876b22a` records this as intervention 0001.

To use them, a person copies the three files into `.claude/agents/` of the
directory the driver session will start in, before starting it. The driver
then dispatches each stage to the definition named for the packet's `EFFORT`
line. That is a host setup step and not part of the workflow, so nothing under
`workflows/pipelines`, `fragments` or `schema` changes and no run's digest
moves.

## The six cold-review items the earlier record left unchecked

Checked against `main` at `0b0832a41`. All six belong to the legacy `proper`
and `proper-finish` workflows. Whether `proper-study` has analogous gaps was
not assessed.

| Item | Status | Locus |
| --- | --- | --- |
| 1.2 Canonical prose can move after `content-evaluation` passes | Absent. `synthesis-preflight` runs only `--edition synthesis` checks; `canonical_frozen` appears in no pipeline, fragment or tool. | `workflows/pipelines/proper-finish.json` `synthesis-preflight`; `workflows/fragments/propers/synthesis-revision.md` |
| 1.4 `web-revision` may edit the canonical leaf after acceptance | Mitigated, not repaired. `9f7674645` makes such an edit visible at `publication-gates`; the permission itself is not narrowed. | `workflows/fragments/propers/web-revision.md` |
| 2.1 The companion's own prose is judged on four criteria | Absent in the fragment; the mechanical half landed as 1.1. | `workflows/fragments/propers/synthesis-evaluation.md` |
| 2.2 The contribution colophon states counts rather than what the stage did | Absent. | `workflows/fragments/propers/author-proper.md`; `tools/check-content-preflight` |
| 2.3 Quotation bytes are not compared with the bound record | Absent. | `tools/check-content-preflight`; `workflows/fragments/propers/lanes/content-citation-integrity.md` |
| 2.4 A work-wide bound duplicated between apparatus and body | Absent. | `workflows/fragments/propers/content-evaluation.md` |

Together with the five defects the earlier record lists as still open, these
are recorded and not repaired. None has a single clear fix that leaves the
legacy pipelines' digests alone, and no legacy run is planned: new proper
guides use `proper-study`.

## What the coordinator re-checked

The survey was a delegated lane, and its report was treated as a proposal. The
coordinator confirmed independently that all eight recovered files hash to the
values the survey reported; that the patch applies cleanly to `main` and does
not reverse-apply, so its change is not there; that the standing-findings
record names run `3c3fb16baa13ee6b` at `proper-finish` v7 with 16 blocking and
5 advisory findings; that no commit on `main` has ever contained the string
`tpt-xhigh`; and that `canonical_frozen`, `quoted-text-matches-record` and
`contribution-record-sane` occur only in the cold review that proposed them
and in this record. Everything else above is the survey's finding, not
re-derived.

## What was not checked

- Agent session transcripts, and anything outside the home directory. A
  diagnosis that lives only in a transcript would be missed.
- Merges in unmerged history were excluded from patch-id matching; the blob
  test covers them only at ref tips. An engine change made in an unmerged
  merge and reverted before its tip would be missed.
- Unreachable objects other than commits.
- The `.scratch` trees of workspaces unrelated to the propers work, which were
  examined by modification time and Git state and not by content.
- The earlier record's three "superseded" judgements were checked for
  consistency with the current engine text and not re-derived.
- A relevant note with an unremarkable name and vocabulary would escape both
  the filename screen and the keyword screen.
