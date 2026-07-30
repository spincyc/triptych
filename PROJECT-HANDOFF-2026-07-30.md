# Handoff, 2026-07-30

Written at the end of a long session so the next agent starts from state rather
than from scratch. `PROJECT-WORK.md` remains the durable register; this is the
session-specific picture. The work ledger (`aiq list`) holds the task queue.

## What this session was

It began as a code review of `tools/tpt` and became a repair of the tooling
layer beneath it, then the beginnings of the commentary research chain.

## The tool layer

`tools/tpt` is the launcher. Implementations are executable scripts at
`tools/<id>`, which is what `tmt` requires; `scripts/` holds shared library
code (`_tooling.py`, `_psalms.py`) and tool data (`web-shim.tex`), because a
bare unregistered file in `tools/` fails the registry gate. Python tests live
in `tools/tests/`; every registered tool must have a shell smoke test at
`tests/tools/<id>.test`, and `tools/tests/test_tool_registry.py` enforces that
plus registry drift, hardcoded paths, and `usage` accuracy.

Launcher controls are dash-prefixed — `--list`, `--info`, `--path`, `--check` —
so a registry id can never shadow one.

Things repaired that are worth not re-breaking:

- The Makefile used two-word variables (`tools/tpt <id>`) as prerequisites and
  as `sha256sum` arguments. Make read them as two prerequisites and silently
  dropped the PDF rules; `make pdf` planned zero builds. Prerequisite and hash
  sites must name `tools/<id>`, not the launcher invocation.
- Sixteen tools computed the repo root one level too high after a directory
  move. `check-proper-components` printed `valid: 0` and exited 0 — a green
  gate over nothing.
- The mass list was stored twice. `sections` is now the single canonical
  container and a top-level `masses` key is a hard error.

## Psalm numbering

The two missals number the psalter differently: the Advent chant *Ad te levavi*
is Psalm 24 in the 1962 books and Psalm 25 in the postconciliar. Resolving one
against the other returns a different psalm under a correct-looking reference.

`scripts/_psalms.py` converts chapters, points and ranges, rebasing verses
across the psalms that divide (Hebrew 116:10 is Vulgate 115:1, not 115:10). It
raises rather than guesses where a split needs a verse. Each calendar declares
`psalm_numbering`; `commentary-work-index` normalises everything to Vulgate
before keying, which healed 27 false merges and 20 false splits.

**Open and important:** the postconciliar file declares `hebrew` at file level,
but its own recovered `citation_convention` says antiphons keep the Missal's
printed Vulgate number while responsorial psalms use the Lectionary's. Eleven
references are confirmed Vulgate-numbered inside that Hebrew-declared file and
fail to resolve. The declaration may need to be per-slot. See the TODO.

## The commentary chain

    propers.yaml -> commentary-work-index build-corpus -> 1307 passages
    harvest plan/record/promote -> passage-commentary-index.yaml
    harvest propers -> one collated acquisition list

`tools/harvest` never calls a model. `plan` emits a worklist, `record` ingests
one run with its model identity and date, `promote` and `propers` collate.
Confidence is agreement across runs — appearances over runs — so the tool stays
deterministic and the nondeterminism is visible and dated in the ledger.

Rules the maintainer set, now enforced:

- A query covers at most one chapter. `Isaiah 63:16-64:7` becomes two loci,
  never one. `plan --by-chapter` gives 491 loci against 1300 verse ranges.
- Work identity is author plus any known title, so aliases collapse. The
  machinery is in; **the alias data is not populated**, which is why Aquinas
  still appears twice in the current collation as *Postilla super Psalmos* and
  *In Psalmos Davidis Expositio*. Those are one work.
- `death_year` is required and must be at or before 1900, so the cutoff is
  checkable rather than living in a prompt.

Three real harvest runs are recorded for the 1962 Advent I propers, seven
passages. Augustine's *Enarrationes*, Cassiodorus, Theodoret and Gregory the
Great each appear in all three; the variance is in the tail. `harvest-ledger.yaml`
is untracked so far — decide whether it belongs in the repository.

## Bibles

`src/sources/bibles/<id>/index.yaml` carries `rights`, `publishable` and
`numbering`. Douay-Rheims is indexed and resolves 438 of 438 roman-1962
references and 937 of 950 postconciliar. It was built from the repository's
already-tracked Challoner edition, not a fresh download, so book names come
from its own modern-name column.

Knox and NJB are approved by the maintainer but **not obtained**: Baronius's own
site carries no scripture text, and the one host that does returned 500 on every
chapter URL tried. They need a real file or a licensed feed. `--bible-root`
lets a licensed index live outside the repository so it is never published.

## Propers

Only the seasonal sections have real propers: 122 of 596 masses. The other 474
carry a single placeholder. `guidance/liturgy/propers-completion-todo.md` holds
the coverage tables, the scope decision, five known defects and the cost.

## Where to pick up

The work ledger is authoritative; at the time of writing the priority ones are
the postconciliar per-slot numbering, the psalter verse-count derivation that
would have caught those eleven references at the gate, the spine-coverage check,
and populating the alias metadata so the collation stops splitting works.

## Verification

`make check` rc=0, `tmt check` ok, 23 of 23 smoke tests pass, and the Python
suite runs with `python3 -m unittest discover -s tools/tests`. Run all four
before believing anything here.
