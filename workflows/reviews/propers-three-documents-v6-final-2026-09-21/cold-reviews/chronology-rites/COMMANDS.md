# Commands and outcomes

Repository: `/home/ksh/git/worktrees/triptych/codex/propers/homily/spincyc/triptych`

All commands exited 0 unless an `rg ... || true` scan intentionally represented no matches.

## Generated artifacts and complete target preflights

For each provider (`claude`, `gpt`) and each document (`liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost`, `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a`):

```sh
tools/proper-chronology record --provider "$provider" --document "$document" --check --plain
tools/proper-chronology annotations --provider "$provider" --document "$document" --check --plain
tools/check-content-preflight --provider "$provider" --document "$document"
```

Outcome: all eight generated files current; all four full preflight sweeps passed. Transcript: `final-verification.log`.

## Direct structural audits

```sh
python3 .scratch/final-cold-chronology-rites/audit_chronology_contracts.py
python3 .scratch/final-cold-chronology-rites/audit_rite_isolation.py
```

Outcomes: 4 records / 4 comparisons / 2 Entrance inputs / 2 Isaiah dossiers / 0 problems; 4 leaves / 159 path-valued liturgical references / 0 problems.

## Corpus and source gates

```sh
tools/tpt scripture-chronology validate
tools/tpt scripture-chronology check
tools/tpt scripture-chronology coverage --plain
tools/tpt source-library validate
tools/tpt source-inventory check
git diff --check
```

Outcomes: all passed. Final counts and coverage are in `final-verification.log`.

```sh
tools/tpt source-library uses passage.united-states-conference-of-catholic-bishops.new-american-bible-revised-edition.english-usccb-web-2026-09-21.isaiah-introduction --format tsv
tools/tpt source-library uses passage.united-states-conference-of-catholic-bishops.new-american-bible-revised-edition.english-usccb-web-2026-09-21.matthew-introduction --format tsv
tools/tpt source-library uses passage.united-states-conference-of-catholic-bishops.new-american-bible-revised-edition.english-usccb-web-2026-09-21.psalms-introduction --format tsv
```

Outcome: target uses resolve to current leaf binding files with cataloged/acquired/inspected state. Transcript: `usccb-source-uses-final.log`.

## Full and focused tests

```sh
python3 -m unittest tools.tests.test_content_preflight_study -v
```

Outcome: 34 tests passed, including direction/precision, approximate-vs-exact, era-less prose, nearby-era masking, and same-date era placement. Transcript: `content-preflight-unit-final3.log`.

```sh
python3 -m unittest   tools.tests.test_chronology   tools.tests.test_chronology_derivation_lineage   tools.tests.test_content_preflight_study   tools.tests.test_proper_chronology_annotations   tools.tests.test_proper_chronology_postconciliar   tools.tests.test_proper_components   tools.tests.test_proper_components_v2   tools.tests.test_source_inventory   tools.tests.test_source_library   tools.tests.test_workflow_chronology   tools.tests.test_workflow_content_preflight -v
```

Outcome: 566 tests passed in 198.295 seconds. Transcript: `full-chronology-source-tests-final3.log`.

A preceding focused legacy/workflow run also passed 141 tests in 109.113 seconds (`legacy-workflow-tests-final.log`).

## Adversarial date probe

Loaded `tools/check-content-preflight` and applied its final era-qualified and era-less match/overlap logic to:

```text
about A.D.~50; about 140--142
about 140--142; about A.D.~50
about A.D.~140--142
about 140--142 A.D.
```

Outcome: the first two retain `about 140--142` as an era-less violation; the latter two correctly recognize the era as belonging to the same span.

## Semantic and path scans

```sh
rg -n -i 'Ordinary Time|semi-continuous'   src/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost   src/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost   --glob '!**/evaluations/**'
rg -n -i 'no identified verse' src/claude src/gpt
```

Outcome: no active matches.

Scanned both postconciliar target leaves for 1962 tree paths/calendar ids and both 1962 target leaves for postconciliar tree paths/calendar ids, excluding inert evaluation snapshots. Outcome: no matches. Transcript: `cross-tree-direct-scan-final.log`.

## Hash binding

```sh
xargs sha256sum < .scratch/final-cold-chronology-rites/subjects.txt > .scratch/final-cold-chronology-rites/HASHES.sha256
sha256sum -c .scratch/final-cold-chronology-rites/HASHES.sha256
```

Outcome: all 101 subjects verified.
