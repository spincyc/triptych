# Production review

## Post-acceptance revision answering every standing finding, 2026-10-01

This recovery completed the interrupted revision in this leaf, preserving the
repairs already present and checking them against their witnesses. The
publication retains its component schema 1 and its two existing editions,
the full study and synthesis companion. There is no homily to rebuild. This
is a post-acceptance revision, not a new `proper-finish` run: the original
run's metadata and historical counts remain, with dated resolutions added
to its standing findings. The contributing agent is recorded as GPT-6 in OpenAI Codex, with the
requested effort high. Runtime reasoning effort, model revision, sampling
configuration and client metadata are explicitly unexposed.

### Findings and dispositions

`OBS-01` through `OBS-07` below identify the seven unnumbered observations
in their original file order. These are local references, not invented
identifiers from the original evaluation. Every accepted finding,
observation and escalation in `evaluations/blocking-findings-v1.toml` now
has a dated resolution.

| Finding | Checked against | Disposition | What changed or why retained |
| --- | --- | --- | --- |
| SYN-CON-009 | The registered Holy See AAS 52 scan, printed pp. 599 and 709; both References and synthesis unit 6 | declined | The entry identifies both instruments and both printed pages. Its warning about two different provisions numbered 18 is intelligible in either edition; no pointer promises an omitted discussion. Both pages were re-read, and the whole scan's registered digest re-matched. |
| OBS-01 | The controlling 1962 Missal, printed p. 397, and the full commentary's spelling comparison | repaired | `sections/synthesis/20-integrated-commentary.tex` explicitly names the **u** of *Aduléscens*. The interrupted repair removes the ambiguous referent of “that vowel”. |
| OBS-02 | The original contribution's own enumeration, 10 + 8 + 6 + 4 + 2 | repaired | `generation-metadata.tex` now states thirty clauses in five files. Later guards remain attributed to their later repair rounds. |
| OBS-03 | Synthesis unit 6 and the scope appendix's Pustet qualification | declined | The small overlap supplies the same necessary provenance qualification where each claim appears. The Sunday cross-refers its Gospel; the Venice 1570 and 1604 witnesses supply the printed pericope. The observation itself judged the overlap legitimate. |
| OBS-04 | Synthesis unit 4 and source-grounded synthesis C2 | declined | The shared *portate / portabit / qui portabant* sentence stem names the subject of C2's pointer. The fourth unit supplies the argument. No second developed argument is duplicated. |
| OBS-05 | The historical contributions and both settled `.aux` files | repaired | `generation-metadata.tex` repairs the thirty-clauses/five-files arithmetic, the mangled class-sweep sentence, and the adjacent iteration-1 page claim. The brief synthesis is on pp. 3–4, with the next component on p. 5. |
| OBS-06 | Augustine, *Enarratio in Ps.* 85 §§1–6, in the bound augustinus.it text; its digest re-matched | repaired | The interrupted repair in synthesis unit 3 places §5 immediately after *omni tempore … Unus homo usque in finem saeculi extenditur*, preserving §2 for *Inclinat aurem*. The themes section already cites 85.5. |
| OBS-07 | All five proposal fields and the current profile's requirement | declined | “What the element-by-element reading misses” names a manner of reading, not a component promised in the companion. The five fields retain their required substantive role and pass `proposal-fields`. |
| CON-CIT-003 | The controlling Missal, printed p. 397, and the corrected Cummiskey Secret and Postcommunion passage records | repaired | The source-library owner corrected the Secret's number to 1589 and the Postcommunion's number to 1591 and incipit to *Mentes nostras et corpora possideat*. This leaf re-read the page and corrected records, repinned both fingerprints in `research/source-bindings.toml`, and recorded completion in `research/scope.md` and `propers/verified.md`. English payloads did not change. |
| CON-PRO-003 | Commit `b27036f9b856bd8f662f51b6e6128bd90a5ed633` and the current profile | already repaired | The 2026-09-11 guidance repair reconciled the audit fields: anchors, mechanism, nearest located precedent or analogue, search boundary, controlling limit. The printed proposal carries Fruit; this leaf's research audit owes no new Fruit field. |

The full-leaf revision also completed these straightforward research-record
repairs from the interrupted work:

- The opening scope's Missal extent is pp. 396–397, confirmed on PDF leaves
  477–478. The next Sunday begins on printed p. 397; p. 398 is not part of
  this formulary.
- The remaining Wilson count in scope §10.1 and the Old Gelasian image
  binding now say five witnesses. Wilson 1894 p. 230 and his introduction
  distinguish Rheinau and St Gall (`R. S.`), Gerbert, Pamelius and Menard.
  The second Collect carries three sigla, `R. S. / Gerb. 175.`. The narrower
  quoted passage about “four witnesses” elsewhere concerns a different
  exegetical audit and is unchanged.
- The Hadrianum image binding distinguishes its one word-order departure
  from 1962 (*tueantur semper*) from the Old Gelasian's second departure,
  *possideat, Domine, quaesumus*. Wilson 1915 p. 174 and Wilson 1894 p. 230
  were read as images. The main discussion's two-departure account was
  already repaired in commit `43e354b12`.
- Scope §12 now quotes the Fourteenth Sunday's actual statement,
  “repository derivative and not a facsimile collation”, rather than the
  earlier inaccurate quotation; the adjacent historical caveat remains
  attributed to that sibling's record.
- The current chronology generator regenerated the annotations. The
  Gospel's A.D. 27 and Communion's A.D. 28 are visibly marked “derived”,
  matching their corpus basis and Maas's A.U.C. ranges. The Maas binding
  context now explains that relationship. All seven printed Date cells
  were read against their explanatory prose; none contradicts it. The
  generated record remains current with 18 assertions. The broader fresh
  chronology audit tracked as KI-017 remains a separate coordinator-owned
  item; this revision does not claim to have completed it.

The source-library corrections changed the Secret fingerprint to
`sha256:7e563c0e653497f5aadac16cd2865b7981b9611c32e49ae5f66e2e401e28dc52`
and Postcommunion fingerprint to
`sha256:2a9fbf5a8b81bcfe57d6e02640f6a8541e4840ea33c39d0b4c96bbe4f559cf64`.
The original passage verification dates remain the dates of the English
wording check; the binding contexts separately date this metadata repair.

### Layout repairs

The initial rebuild exposed an underfull paragraph at the metadata input:
the shared timestamp macro ends a line before the contribution commands,
which print no text. A local `\begingroup` / `\raggedright` / `\par` /
`\endgroup` around the metadata input in `main.tex` makes that paragraph
ragged right. No warning threshold was changed. Both editions still have
their original page counts, 36 and 24. The brief-synthesis markers remain
start 3, end 4, next 5 in both editions.

All 60 pages were inspected on contact sheets. The changed dossier and
commentary pages and both terminal pages were also inspected at full size.
The generated Date cells fit on p. 2; the two synthesis prose repairs fit on
pp. 5–6. No clipping or overlap was found. The full edition's sparse final
page already existed in the baseline and still carries the final References
entries, timestamp and rights statement.

### Artifacts

Paths are relative to the repository root. Nothing was installed under
`pdf/` or `web/` by this revision lane.

| Output | Pages | SHA-256 | Bytes |
| --- | ---: | --- | ---: |
| `build/claude/liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost.pdf` | 36 | `c2b94955797178dfe6df237c775db8d66e9b2354358a709bad7d46817229b309` | 608032 |
| `build/claude/liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost-synthesis.pdf` | 24 | `343320a491eb0664b489cbf97e4fccd1b9aba067d2a84a4f0a0abbec4e2b9a1f` | 540814 |
| `build/web/claude/liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost.md` | — | `6dacd0fa198e21faa9e99040058fbb5a2e631163cabd7ac9e7db5b9a158c1d37` | 169965 |

The revision timestamp is `2026-10-01T22:26:08Z`. Because this remains a
schema-1 leaf, the artifact table records the revision's receipts; the
schema-2 `proper-study snapshot` and `snapshot-web` operations do not apply.

### Checks run

- Both normal `make doc` recipes completed, including their PDF anchor,
  component-manifest and generation-metadata gates. Their settled logs
  contain no overfull or underfull box, warning, undefined reference or
  rerun request. These editions declare no contents links or bookmarks;
  their anchor checks report zero of each.
- All 35 checks in the recovery gate sweep pass. For **each** edition,
  `check-content-preflight` ran `references-used`, `identifiers-resolve`,
  `bindings-valid`, `restricted-not-reproduced`, `relation-coverage`,
  `unquoted-not-quoted`, `structural-meta-labels`, `house-voice`,
  `chronology-record-current`, `chronology-annotations-current`,
  `chronology-claims-supported`, `proposal-fields` and
  `provenance-matches-run`; `check-proper-components` ran both content and
  artifacts phases. The other five were `proper-chronology record
  --check`, `proper-chronology annotations --check`, `source-library
  validate`, `check-web-edition` and `check-generation-metadata`.
- `provenance-matches-run` checked the preserved original `proper-finish`
  v6 identity, run `05f2d2fd7c2cf8b3`, workflow digest
  `4dd807084e8cde3d6482395745b07bd6e837678332417fcd12f50f68160fd768`,
  seed `57bae9ebf82a2ce312660050fde1050ff89b224b`. It is not a claim that
  this recovery created a new workflow run.
- Web generation used a scratch virtual environment with the repository's
  two pins, Markdown 3.10.3 and PyYAML 6.0.3. `check-web-edition` passes.
- `pdfinfo` reads both PDFs, confirms their titles and subjects, Letter
  dimensions and page counts. `pdffonts` reports every font embedded,
  subsetted and carrying a Unicode mapping. `pdftotext -layout` succeeds;
  comparison with the retained baseline shows only the two derived-date
  labels, the two synthesis prose repairs and the revised timestamp with
  its paragraph spacing.
- `tools/tpt pdf-review` rendered all 60 pages. The command rejects scratch
  output with `pdf-review: --output must remain under this checkout's
  build/ tree or a /tmp subdirectory`, so its output is in the leaf's own
  `build/claude/liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost-review/`.

The schema-2 command was probed once and correctly refused this legacy
leaf: `proper-study: proper-study requires component schema 2; use legacy
proper for schema 1`. The equivalent legacy component checks above passed.
An initial contribution qualifier also failed validation with
`qualifier 'reasoning effort: high' must use key=value or 'unexposed:
component'`; it was corrected to a valid key-value qualifier before the
final builds. The audit-only follow-up correctly records that qualifier as
`requested-effort=high`, with runtime reasoning effort explicitly unexposed.
Both PDFs and the web edition were regenerated after that metadata-only
correction and are byte-identical to the artifact receipts above; generation
metadata and web-edition checks pass. No failure remains in the final gate
sweep.

Ephemeral evidence is under `.scratch/recovery-leaf-claude55/`: exact
commands and outputs in `checks.json`, build and web logs, PDF metadata,
font inventories and extracted-text diffs. Retained witness images from
the interrupted revision are under `.scratch/rev-claude-55/` and were read
without modification. The Missal scan re-matches
`648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a`;
the Augustine text re-matches
`3909c029b75092eb11f8c353b295b24c5fb3bcf8d7ba52f196040914b7a6692b`;
the AAS scan fetched for this review re-matches
`c734079d1a9393f09595bd95dd5900ad30e9c5a2bc6939a8bfd84e048f414702`.

At this handoff the artifacts are ready for independent content and
visual/web review. This authoring record does not itself assert independent
acceptance; the coordinator records the subsequent verdict and installation.
