# Wisdom chronology concern: bounded confirmation, 25 October 2026

**Disposition: no current defect substantiated; retain the existing source and
projection.** The inspected state is commit
`24c1b7ce1781f79937f57b66c221b0ed82e219d9` with the uncommitted GPT All Saints
research artifacts. This report is the lane's only file change. It neither
accepts the chronology corpus nor closes its 528-row independent source audit.

## Source and canonical claim

Francis Gigot, “Book of Wisdom,” *The Catholic Encyclopedia* XV (New York:
Robert Appleton Company, 1912), is registered as
`artifact.catholic-encyclopedia.volume-15.new-york-1912.newadvent-15666a-999fbc07`.
Its exact delivery is remote; its separately manifested, public-domain article
text is retained at
`src/sources/works/catholic-encyclopedia/volume-15/editions/new-york-1912/artifacts/newadvent-15666a-999fbc07-article-text/newadvent-15666a-999fbc07-article-text.txt`.
The complete retained article and both manifests were inspected, with the
material argument at line 29 and authorship/place context at lines 23–33.
This was an inspection of the retained normalized transcription, without a new
facsimile collation or live retrieval.

Line 29 identifies the persecution the writer has in view with either Ptolemy
IV Philopator's reign (221–204 B.C.) or Ptolemy VII Physicon's reign
(145–117 B.C.). It leaves the choice unsettled and permits publication after
the princes' deaths. That last clause is contrary evidence against treating
either reign's closing year as a composition terminus.

The current `composition.book-of-wisdom` unit already addresses that evidence.
`src/sources/chronology/composition.yaml:1595–1679` explains the distinction;
lines 1651–1656 and 1674–1679 encode two disputed `boundary` claims with
`direction: no-earlier-than`, endpoints 221 and 145 B.C., and complete
“in or after the time of…” statements. The reign labels remain the source's
raw wording. They do not turn the boundaries into closed composition
intervals. `src/sources/chronology/attribution-context-review.md:69–84` records
the earlier concern and its 1 October KI-015 correction, while explicitly
leaving the later independent audit outstanding. `PROJECT-WORK.md`'s KI-015
entry agrees.

No claim was narrowed or removed for missing evidence. A second source-family
search was therefore unnecessary to this bounded confirmation; no such search
is represented as completed.

## Actual All Saints publication interface

The affected appointment is the Offertory, Wisdom 3:1–3, in
`src/gpt/liturgy/roman-rite/1962/propers/temporal/f02-all-saints/`.
Its generated `research/chronology.toml:1692–1780` retains both full statements
in `date`, both `precision = "boundary"` values, and the separate raw labels,
in the audit claims and the across-all-loci publication claims.

The fresh `orientation-v2` projection yields row `row-43dce930fad06090`:

> Composition: The Book of Wisdom
>
> Disputed: In or after the time of Ptolemy IV Philopator (221-204 B.C.);
> In or after the time of Ptolemy VII Physicon (145-117 B.C.)

The generated detailed annotation at `research/chronology-annotations.tex:42`
and orientation row at line 68 both preserve this qualification visibly.
The macro has six arguments: its line-6 definition is
`\newcommand{\chronologyannotationclaim}[6]{#6}`. Argument 5 retains the raw
label for audit; argument 6 displays the qualified value. In the owner,
`scripts/_proper_chronology.py:1274–1275` renders a boundary from `claim.date`,
and lines 2058–2065 keep raw label and display value distinct. The conjectured
loss of the statement does not occur on this interface.

The plain `scripture-chronology query` diagnostic prints the raw source label.
Its JSON companion also exposes the full boundary direction, endpoint,
statement and rendered date; the proper's publication projection uses the
qualified date. A raw diagnostic label alone is insufficient evidence of a
reader-facing closed interval.

## Reproduction and checks

All commands below were run from the repository root using the pinned scratch
interpreter, shown with its repository-relative spelling. Every command exited
0. Neither currency check writes its target.

```sh
.scratch/publication-prep/venv/bin/python tools/scripture-chronology query Wis.3.1 --profile catholic-comprehensive-v1 --json
.scratch/publication-prep/venv/bin/python tools/proper-chronology annotations --document liturgy/roman-rite/1962/propers/temporal/f02-all-saints --provider gpt --presentation orientation-v2 --format text --plain
.scratch/publication-prep/venv/bin/python tools/proper-chronology record --document liturgy/roman-rite/1962/propers/temporal/f02-all-saints --provider gpt --check --plain
.scratch/publication-prep/venv/bin/python tools/proper-chronology annotations --document liturgy/roman-rite/1962/propers/temporal/f02-all-saints --provider gpt --presentation orientation-v2 --check --plain
.scratch/publication-prep/venv/bin/python -m unittest tools.tests.test_chronology.StatedBoundsTests.test_the_two_wisdom_reigns_are_two_claims tools.tests.test_proper_chronology_annotations.ReaderFacingDisplayTests.test_source_wording_after_a_subject_title_continues_the_sentence
```

The query exposes both `no-earlier-than` boundaries at 221/145 B.C.; the text
projection is quoted above; both stored artifacts are current; both existing
focused tests pass (2 tests). These checks establish the inspected source/data/
display relationship, without claiming a completed PDF or web artifact review.

| Inspected input or generated artifact | SHA-256 |
| --- | --- |
| Retained Gigot article text named above | `91d4070cb25e89df67b494b3937e5be3cbed3b3570c68884e51721a00cf9d9fc` |
| `src/sources/chronology/composition.yaml` | `a53405cc4031447b95ef0f36edda169693b1411910a6cd2b2e9ab268cffebfe1` |
| `scripts/_proper_chronology.py` | `1770866b2c46dac74b80bc95958cb0868dee65f514d711974822599adfaae108` |
| All Saints `research/chronology.toml` | `6ab0109bd1bc0e7953a23fa47f546883454948ce34f01a2b42c999633b1cccaa` |
| All Saints `research/chronology-annotations.tex` | `d396816f55517a7918ac3d74bed09420c977a11f524ec904a923668d7bbf3c51` |

The retained article digest matches its manifest. The canonical corpus, owner
code, tests and All Saints leaf were unchanged by this lane. The native
workflow's independent source-fidelity review and later rendered-artifact
reviews remain responsible for their own exact states. This same-session
confirmation does not discharge the separate corpus-wide acceptance requirement.
