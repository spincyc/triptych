# Commands and outcomes

All commands ran from the repository root and exited 0 unless a direct `rg` scan intentionally had no matches.

```sh
git status --short
git branch --show-current
git rev-parse HEAD
git rev-parse origin/main
git show -s --format=fuller b048fa37e
```

Outcome: closure files are the only tracked working-tree changes; branch is `feature/codex/propers/homily`; HEAD and the fetched `origin/main` both name `b048fa37e8e784fbcc351bce201f9e676d3d5008`.

```sh
git ls-remote origin refs/heads/main
gh run view 35691184227 --json databaseId,headSha,headBranch,event,status,conclusion,createdAt,startedAt,updatedAt,url,workflowName,jobs
```

Outcome: the live remote branch and successful Pages run both bind the exact candidate SHA.

```sh
git diff -- PROJECT-WORK.md promised-deliverables.toml \
  workflows/reviews/propers-three-documents-v6-final-2026-09-21/README.md \
  workflows/reviews/propers-three-documents-v6-final-2026-09-21/release-checks.md
```

Outcome: only the two deployment-dependent promise requirements and corresponding deliverable states close; associated prose records the observed deployment facts.

A Python audit parsed `deployment-evidence.json`, mapped entries in order to `.scratch/live-route-00` through `live-route-15`, mapped every URL to `build/public-alpha/site`, and checked existence, size, SHA-256, HTTP status, declared match, summary counts, and byte equality.

Outcome: 16 routes checked; four HTML and twelve PDF; zero errors.

A second Python audit reconciled deployed PDFs with `artifact-identities.json` and independently rehashed all sixteen installed artifacts.

Outcome: 16 identities checked; zero errors.

```sh
git diff --check
make check-promised-deliverables
python3 -m unittest tools.tests.test_proper_components \
  tools.tests.test_proper_components_v2 \
  tools.tests.test_workflow_proper_study -v
```

Outcomes: diff check passed; promise ledger valid with 40 tracked and 31 complete; 71 tests passed.

Direct `rg` scans checked the two active 1962 leaves for postconciliar path references and the two active postconciliar leaves for 1962 path references, excluding `evaluations/**`; manifest identity/calendar lines and postconciliar shared-owner paths were inspected.

Outcome: zero cross-tree paths; each leaf retains the expected calendar and same-family owner tree.
