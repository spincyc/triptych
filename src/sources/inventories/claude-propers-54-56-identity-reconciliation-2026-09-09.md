# Claude propers 54–56 source identity reconciliation — 2026-09-09

This is the bounded source-identity reconciliation performed while integrating the
Claude Fourteenth, Fifteenth and Sixteenth Sundays after Pentecost
(`feature/claude/propers/tlm/54`, `/55`, `/56`) onto `main` at `d3ceb2937`, which
already carried the GPT productions of the same three identities and
[their reconciliation](propers-54-56-identity-reconciliation-2026-09-06.md). It
changes evidence metadata and review pins only; it revises no publication prose,
records no new research sweep, retrieval or collation, and accepts no publication.
The governing rules are [source identity, immutable artifacts and consumer
review](../../../guidance/sources.md).

Each branch's research registered its sources independently of the GPT
production that reached `main` first, so the same bytes or the same identity
were sometimes registered twice. The rule applied throughout: the record `main`
already held is canonical, the branch's duplicate is withdrawn, and every
consumer binding that named the withdrawn record is rebound and re-pinned with a
dated `Metadata review` note in its `context`. An old identifier in a research
brief is not evidence that different bytes were consulted.

## Sixteenth Sunday (`feature/claude/propers/tlm/56`)

### Duplicate identities withdrawn

| Withdrawn (branch) | Canonical (`main`) | Ground |
| --- | --- | --- |
| `artifact.thomas-aquinas.super-psalmos.latin-corpusthomisticum-web-2026-09-05.cps31-html-e2d50b43`, declared a second time under `editions/latin-corpusthomisticum-web-2026-09-05/` with its own `edition.toml` | the same ids under `editions/2026-09-05-latin-corpusthomisticum-web-2026-09-05/` | same edition id, artifact id, URL, SHA-256 `e2d50b43…`, byte size and restricted disposition; `main`'s directory also holds the five other responses the GPT production registered |
| `artifact.cyril-of-alexandria.commentary-on-luke.english-payne-smith-oxford-1859.tertullian-sermons-99-109-html` | `artifact.cyril-of-alexandria.commentary-on-luke.english-payne-smith-pearse-web-2026-09-05.cyril-on-luke-10-sermons-99-109-f545b082` | byte-identical Tertullian Project delivery, SHA-256 `f545b082…`, 121 616 bytes; `main` registers that dated web delivery as its own edition state, and the 1859 printing keeps only the sermons 110-123 delivery it held before |
| `artifact.ildefonso-schuster.the-sacramentary.burns-oates-washbourne-english-1927.ia-djvu-ocr-volume-3-4d8c8988` | `artifact.ildefonso-schuster.the-sacramentary.burns-oates-washbourne-english-1927.ia-volume-3-ocr-4d8c8988` | byte-identical Internet Archive OCR, SHA-256 `4d8c8988…`, 1 149 699 bytes; the canonical record is the one the 2026-09-06 reconciliation already chose |
| `work.roger-pearse.early-church-fathers-additional-texts`, its edition `tertullian-org-web-2026-09-05` and artifact `index-html-98196cf3` | `work.roger-pearse.early-church-fathers-additional-texts-index`, edition `english-web-2026-09-05`, artifact `fathers-index-html-98196cf3` | byte-identical index page, SHA-256 `98196cf3…`; the branch registered it only to enumerate the Cyril files and no publication binds it |

Both providers' Sixteenth Sunday productions registered `work.william-shakespeare.sonnets`,
`work.friedrich-nietzsche.menschliches-allzumenschliches` and
`work.elizabeth-barrett-browning.sonnets-from-the-portuguese` under the same work
ids with different editions. The work records are merged: the branch's
composition dates and bases (which `main` had recorded as unknown) and fuller
titles are kept, and `main`'s alternate titles are retained as aliases. The
editions and artifacts of both productions stand unchanged under the merged
works.

### Bindings re-pinned

Twelve bindings moved fingerprint with no change to their loci, roles or
evidence states, each carrying a `Metadata review 2026-09-09` note:

- `src/claude/…/56-sixteenth-after-pentecost/research/source-bindings.toml`
  bindings 53 (Cyril, rebound), 58 (Aquinas cps31, duplicate withdrawn),
  63 (Schuster, rebound), 70 and 71 (Guéranger volume XI, whose edition and
  work records `main` had corrected to the 1909 imprint), 97 (Barrett
  Browning), 120 and 121 (Nietzsche) — the last three because of the merged
  work records.
- `src/gpt/…/56-sixteenth-after-pentecost/research/source-bindings.toml`
  bindings 36 and 54 (Shakespeare), 37 (Nietzsche) and 38 (Barrett Browning),
  because of the merged work records.

### Inventories

The Claude publication inventory gained the Sixteenth Sunday leaf and its
classification review resolves it to the same strata as the Fourteenth: finding
aid, historical primary, institutional current, liturgical, magisterial,
patristic, prayer-devotional, scholastic, scripture and secondary, derived from
the works its bindings name. The GPT inventory's pinned hash of its own
Sixteenth Sunday binding file follows the re-pins above. The family ledger is
refreshed against the changed canonical catalog with every review unit still
pending, as the 2026-09-06 refresh left it. `tools/source-library validate`,
both inventory checks, `source-inventory classify` and `make check-sources`
pass on the integrated tree.

## Fourteenth Sunday (`feature/claude/propers/tlm/54`)

No duplicate bytes: the branch's New Advent responses differ from the GPT
production's by the page furniture that host changes between deliveries, so
each stays its own artifact. Two records were registered under ids `main`
already held, and `main`'s wording is kept verbatim in both cases, because
each was already pinned by an integrated leaf:

| Branch record | Disposition |
| --- | --- |
| `work.augustine.de-sermone-domini-in-monte` | `main`'s record (GPT Fourteenth Sunday registration, with its unknown-composition basis) stands; the branch's edition `english-npnf-new-advent-web-2026-09-05` and its Book II response join it unchanged |
| `edition.augustine.enarrationes-in-psalmos.english-npnf-new-advent-web-2026-09-05` | `main`'s record (Claude Sixteenth Sunday registration of the same dated web state) stands; the branch's four psalm responses (33, 83, 94, 117 in the Vulgate numbering) join it unchanged |

Five bindings in
`src/claude/…/54-fourteenth-after-pentecost/research/source-bindings.toml`
(38 to 42) moved fingerprint through those two ancestors and are re-pinned
with a `Metadata review 2026-09-09` note; their loci, roles and evidence
states are unchanged. The Claude publication inventory follows the revised
leaf, the family ledger is refreshed, and the same checks pass.
