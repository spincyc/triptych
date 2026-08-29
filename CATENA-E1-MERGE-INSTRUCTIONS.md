# Triptych — Merge Confirmed Catena E1 Integration to Main

## Agent

**Use a fresh Claude CLI agent.**

This is the final Catena E1 merge lane.

The integration candidate has completed convergence review, independent integration review, one bounded correction pass, and confirmation review.

Confirmation disposition:

`CONFIRMED — CATENA E1 INTEGRATION READY TO MERGE`

Do not reopen Catena hardening.
Do not start V17.
Do not modify the confirmed integration candidate.
Do not broaden scope into release, shared-shell, Liturgy, PDF, evidence-tooling, or other backlog lanes.
Do not deploy.
Do not re-sign release-owned records.

Your task is to merge the exact confirmed Catena candidate into the exact current main, resolve only the known record conflicts, run a minimal post-merge validation, push `main`, verify the remote, report, and stop.

---

## 1. Exact identities

Confirmed Catena candidate:

`b832cdc5bc01391cea67c01437318d25e0c7c315`

Branch:

`integration/catena-e1`

Confirmation review:

- branch: `review/catena-e1-integration-confirmation`
- durable review commit: `7dfd944494a8d9355264579156214f16d3722a9f`
- disposition: `CONFIRMED — CATENA E1 INTEGRATION READY TO MERGE`

Original integration review:

`c3698563e3b45e35a672db37616e39ef27eb3d08`

Convergence review:

`f1a5bbad763b847ded8799748223898de6ad4de9`

Current main, independently verified before these instructions were published:

`004615faf506eb4083d484d41b18ee1c61f0aa7f`

The confirmed merge-tree review found exactly two textual conflicts between current main and the candidate:

- `PROJECT-WORK.md`
- `promised-deliverables.toml`

No production, source, test, data, configuration, shared-shell, Liturgy, or PDF conflict was found.

---

## 2. Start in a fresh clone

**Do not use a git worktree.**

Create a fresh clone in a separate directory.

```bash
git clone <repo-url> triptych-catena-e1-merge
cd triptych-catena-e1-merge
git fetch --all --prune
```

Verify exact refs:

```bash
git rev-parse origin/main
git rev-parse origin/integration/catena-e1
git rev-parse origin/review/catena-e1-integration-confirmation
```

Require before proceeding:

```text
origin/main = 004615faf506eb4083d484d41b18ee1c61f0aa7f
origin/integration/catena-e1 = b832cdc5bc01391cea67c01437318d25e0c7c315
```

The confirmation-review branch may now have an additional instruction-file commit above `7dfd9444...`; that is expected. The durable confirmation decision remains commit `7dfd944494a8d9355264579156214f16d3722a9f`.

If `origin/main` has moved beyond `004615faf506eb4083d484d41b18ee1c61f0aa7f`, **do not blindly merge**. Stop and report the new SHA and a read-only merge-tree comparison. These instructions authorize the exact verified main above.

---

## 3. Check out exact current main

```bash
git switch --detach 004615faf506eb4083d484d41b18ee1c61f0aa7f
git switch -c merge/catena-e1-into-main
```

Verify clean state:

```bash
git status --short
git rev-parse HEAD
```

Require an empty working tree and exact main SHA.

---

## 4. Reconfirm the merge shape read-only

Before performing the merge, run:

```bash
BASE=$(git merge-base 004615faf506eb4083d484d41b18ee1c61f0aa7f b832cdc5bc01391cea67c01437318d25e0c7c315)
git merge-tree "$BASE" 004615faf506eb4083d484d41b18ee1c61f0aa7f b832cdc5bc01391cea67c01437318d25e0c7c315
```

Confirm the only conflicts are:

- `PROJECT-WORK.md`
- `promised-deliverables.toml`

If any production/source/test/data/config file now conflicts, stop. That is outside the confirmed merge authorization.

---

## 5. Begin a non-committing merge

Merge the exact confirmed candidate:

```bash
git merge --no-ff --no-commit b832cdc5bc01391cea67c01437318d25e0c7c315
```

Do not resolve by taking one side wholesale.

Verify conflict list:

```bash
git diff --name-only --diff-filter=U
```

It must contain exactly:

```text
PROJECT-WORK.md
promised-deliverables.toml
```

If anything else is conflicted, stop and report.

---

## 6. Resolve `PROJECT-WORK.md`

This is an append-only/current-state record conflict.

Preserve both lanes' valid records:

- all current-main Missal remediation / post-base work;
- all confirmed Catena E1 integration and bounded-correction records;
- the confirmation review result;
- truthful current statuses.

Do not delete one side's records simply to resolve the hunk.

Do not duplicate identical records.

Add only the smallest merge-time record needed to state that the confirmed Catena E1 integration is being landed, if repository convention requires it.

After resolution, there must be no conflict markers.

---

## 7. Resolve `promised-deliverables.toml` carefully

The confirmation reviewer rehearsed this conflict and identified an important TOML structural detail:

- the shared `[[deliverables]]` header sits above the conflict hunk;
- the array terminator for the first entry sits below it;
- blind concatenation produces invalid TOML.

Resolve by preserving both complete deliverable entries as valid independent TOML records.

For multiple entries, each must have its own proper:

```toml
[[deliverables]]
```

header and all arrays/fields must close before the next entry begins.

Preserve:

- current-main deliverables, including Missal remediation state;
- Catena E1 deliverable/integration state;
- all unrelated current-main entries.

Do not duplicate a deliverable ID.

Do not accidentally nest one deliverable inside another.

After resolution, validate TOML structurally before proceeding.

---

## 8. Record final Catena integration status truthfully

The confirmed candidate was intentionally recorded as a candidate before merge.

During this merge, update only the minimal durable state required by repository convention to reflect the confirmed merge decision.

Use the existing schema/conventions found in current main.

The record should establish, as applicable under the repository's existing vocabulary:

- candidate reviewed: `b832cdc5bc01391cea67c01437318d25e0c7c315`;
- confirmation review: `7dfd944494a8d9355264579156214f16d3722a9f`;
- confirmation disposition: `CONFIRMED — CATENA E1 INTEGRATION READY TO MERGE`;
- E1 Catena integration landed in this merge;
- hardening backlog remains backlog;
- evidence-tooling backlog remains backlog;
- separately owned blockers remain open.

Do **not** mark unrelated Wave 1 work, release bindings, shared shell, Liturgy, PDFs, or other blockers complete.

Do not invent a new status vocabulary if the repository already defines one.

---

## 9. Stage only the resolved merge

After resolving the two conflicts and minimal merge-time status records:

```bash
git add PROJECT-WORK.md promised-deliverables.toml
```

If another durable record must legitimately change to record the merge under existing repository convention, inspect and justify it explicitly before staging.

Do not edit Catena production/test/data bytes during conflict resolution.

---

## 10. Verify Catena production bytes survived the merge unchanged

The merge must preserve the exact confirmed candidate versions of Catena production/source/test assets because current main had no overlapping changes in those paths.

At minimum compare the merged index against candidate blobs for the confirmed integration-owned paths, excluding the two intentionally reconciled record files.

Use commands such as:

```bash
git diff --cached b832cdc5bc01391cea67c01437318d25e0c7c315 -- \
  src/web/browser/catena \
  scripts/_catena.py \
  src/web/data/structure/catena \
  tools/tests/test_catena.py \
  tools/tests/test_catena_production.py \
  tools/tests/catena_recovery_focus_gate.mjs
```

Expected result for those integration-owned production/test/data paths:

**no semantic/content delta from the confirmed candidate**, except any path whose generated bytes are demonstrably affected by current-main source state and explicitly authorized by the merge. The confirmation rehearsal found none.

If a production/test blob differs unexpectedly, stop before commit.

---

## 11. Validate repository records before commit

Run the repository's normal promised-deliverable/work-register validation.

At minimum:

```bash
tools/tpt check-promised-deliverables
```

Also run the exact repository ledger test used by the confirmed candidate if distinct.

Require:

- valid TOML;
- no duplicate deliverable IDs;
- work-register marker valid;
- no new record failures caused by merge resolution.

---

## 12. Minimal Catena post-merge smoke

Do **not** restart full adversarial hardening.

Run only the confirmed minimal merge smoke.

### Corpus / generator

```bash
python3 scripts/_catena.py check
```

Expected production structure:

```text
fragments = 1351
books = 1
canon = 73
```

### Focused Catena

Run the repository's exact confirmed command for `tools/tests/test_catena.py`.

Expected:

```text
56/56
```

### Curated production suite

Run the repository's exact confirmed command for `tools/tests/test_catena_production.py`, with real Chromium available so the focus gate executes rather than silently skipping.

Expected:

```text
394/394
```

### Static browser checks

Run the same confirmed static Catena browser checks used by the candidate.

Expected:

```text
5/5
```

### Catena Chromium route smoke

Run the confirmed Catena route-only browser command against the merged tree.

Expected status universe remains:

```text
121 identities
95 pass
14 inherited fail
12 skip
```

No new identity/status change is allowed.

The 14 inherited failures are separately owned shared-shell baseline and are not merge blockers.

---

## 13. Do not run another broad acceptance loop

Do not rerun V13–V16 evidence packages.

Do not add hostile getter/thenable/prototype tests.

Do not fix:

- hardening backlog;
- evidence-tooling backlog;
- release bindings;
- common shared-shell failures;
- Liturgy;
- PDFs;
- model/combined-budget governance;
- historical data seam;
- other separately owned work.

This is a merge, not another acceptance project.

---

## 14. Check merge result before commit

Run:

```bash
git status
git diff --check
git diff --cached --stat
git diff --cached
```

Verify:

- no conflict markers;
- TOML valid;
- no accidental unrelated paths;
- only mechanical record reconciliation beyond the already-confirmed candidate;
- all minimal smoke checks pass.

---

## 15. Commit the merge

Create the merge commit with a clear message, for example:

```text
Merge Catena E1 integration
```

The commit message should mention:

- confirmed candidate `b832cdc5bc01391cea67c01437318d25e0c7c315`;
- confirmation review `7dfd944494a8d9355264579156214f16d3722a9f`;
- only two record conflicts resolved;
- minimal post-merge validation passed.

Do not squash the integration candidate into an unrelated commit.

Preserve merge ancestry.

---

## 16. Verify merge ancestry

After commit, record the merge SHA and verify:

```bash
git merge-base --is-ancestor b832cdc5bc01391cea67c01437318d25e0c7c315 HEAD
git merge-base --is-ancestor 004615faf506eb4083d484d41b18ee1c61f0aa7f HEAD
```

Both must succeed.

Inspect:

```bash
git log --graph --oneline --decorate -20
```

---

## 17. Push the merge to `main`

Only after all checks pass, push the merge commit to main without force:

```bash
git push origin HEAD:main
```

No force push.

No deployment.

No release signing.

---

## 18. Verify remote main

After push:

```bash
git fetch origin
git rev-parse HEAD
git rev-parse origin/main
```

Require local merge HEAD == `origin/main`.

Also verify the confirmed candidate is now an ancestor of remote main:

```bash
git merge-base --is-ancestor b832cdc5bc01391cea67c01437318d25e0c7c315 origin/main
```

Require success.

---

## 19. Final post-push sanity check

Do not rerun the whole suite after push unless the push changed bytes unexpectedly.

At minimum verify:

- remote main SHA;
- clean working tree;
- candidate ancestry;
- merge commit parents;
- no release/deployment operation occurred.

If repository policy requires one final lightweight ledger command after push, run it read-only.

---

## 20. Stop-condition report

Return:

- merge branch/workspace;
- starting main SHA `004615faf506eb4083d484d41b18ee1c61f0aa7f`;
- confirmed candidate SHA `b832cdc5bc01391cea67c01437318d25e0c7c315`;
- confirmation review SHA `7dfd944494a8d9355264579156214f16d3722a9f`;
- merge commit SHA;
- merge parents;
- conflict count;
- exact conflict paths;
- `PROJECT-WORK.md` resolution summary;
- `promised-deliverables.toml` resolution summary;
- TOML validation result;
- work-register/promised-deliverables validation result;
- confirmation candidate production-byte preservation result;
- `python3 scripts/_catena.py check` result;
- focused Catena result;
- curated production result;
- static browser result;
- Chromium Catena route result;
- new route identity/status count;
- `git diff --check` result;
- unexpected changed-path count;
- hardening backlog preserved;
- evidence-tooling backlog preserved;
- separately owned blockers preserved;
- push-to-main result;
- exact remote main SHA after push;
- candidate-is-ancestor-of-main result;
- clean working tree result;
- confirmation no force push;
- confirmation no deploy;
- confirmation no release re-signing.

Then stop.

The Catena E1 integration task is complete once the confirmed candidate has been merged and pushed to `main` with the two record conflicts resolved and the minimal post-merge smoke passing.

Do not begin the next backlog lane in this agent session.
