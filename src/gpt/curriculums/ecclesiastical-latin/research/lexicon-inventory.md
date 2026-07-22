# Controlled Lexicon Inventory

## Status and boundary

This record audits the cumulative memory registry introduced for the redesigned
Ecclesiastical Latin curriculum. It is current through 2026-07-22. The
authoritative entries are in `shared/memory/lexemes.tex`; packet allocation,
recurrence, grammar-fact membership, and project prompts are in
`shared/memory/sets.tex`. This record describes those sources and does not
duplicate all 598 entries.

The registry is a controlled instructional baseline, not a frequency-ranked
claim about the whole Latin language and not a claim of any percentage of
Missal, classical, biblical, or patristic corpus coverage. Its English senses
are project glosses. Its strand labels are pedagogical allocations. No strand
label by itself asserts that the lexeme has been verified in a named author,
work, edition, or locus.

## Quantitative inventory

| Object | Count | Audit meaning |
|---|---:|---|
| Stable lexemes | 598 | Contiguous IDs L001–L598; no duplicate ID or exact citation-form entry in the registry audit |
| Trunk introductions | 550 | 25 new lexemes in each of M01–M22 |
| Poetry-branch introductions | 48 | 6 new lexemes in each of P1–P8 |
| Productive (`active`) entries | 572 | Expected in bidirectional recall and controlled composition |
| Receptive (`recognition`) entries | 26 | Expected principally in reading and analytical metalanguage |
| Grammar-memory facts | 81 | Stable IDs G001–G081 |
| Memory sets | 30 | M01–M22 and P1–P8 |
| Project prompt/model pairs | 30 | One reconstruction pair and one composition pair in each set |
| Scheduled prior-lexeme placements | 726 | Sum of R1, R2, R5, and S lists; these are sampled returns, not 726 distinct words |
| Printable sheet families | 240 | Eight stable sheet families for each of 30 sets |
| Practice/model renderings | 480 | Each sheet family appears once for fresh work and once with its project model |

Every introduced lexeme appears in five immediate modes within its packet:
complete-entry study, Latin-to-sense retrieval, sense-to-Latin retrieval,
morphology retrieval, and usage/government retrieval. Sampled lexemes then
return at R1, R2, R5, and selected stage boundaries. Any uncertain item is
carried in a personal return list even when it is not in the printed sample.

## Entry schema

Each `\DeclareMemoryLexeme` row records:

1. a stable ID;
2. complete citation form, including gender, principal parts, governed case,
   or indeclinability where applicable;
3. a concise project-created English sense;
4. inflection class or morphological facts;
5. a principal construction, government cue, or material semantic warning;
6. one or more pedagogical corpus or task strands; and
7. productive (`active`) or receptive (`recognition`) expectation.

First teaching point and later retrieval points are normalized in the memory
set registry instead of repeated in every lexical row. Material semantic
distinctions and many common complement patterns are recorded in the usage
field. A systematic word-family and collocation layer has not yet been
completed for every entry; it remains an owner-level enrichment task and must
not be represented as complete.

## Coverage design

- M01–M04 begin with ordinary animals, color, landscape, house and town,
  family, food, work, body, weather, states, and transparent actions. These
  sets support clauses such as “the fox is brown” before specialized sacred
  register.
- M05–M12 add high-frequency principal parts, passives and deponents,
  reference words, prepositions, number and comparison, non-finite governors,
  purpose/result/fear vocabulary, circumstantial connectors, commands and
  wishes, and adverbial place and time.
- M13–M18 add the Ordinary and its ministers, books, chants, vessels, oration
  verbs, lesson and Gospel persons, praise and mystery vocabulary, calendar
  and Commons terminology, Holy Week, Easter, burial, judgment, and Requiem.
- M19–M22 add biblical discourse texture, comparison particles, rhetorical and
  periodic-prose terms, witnesses and textual apparatus, argument,
  interpretation, revision, and independent exposition.
- P1–P8 add prosody, hexameter, elegiac and lyric vocabulary, Christian
  poetics, rhythmic hymnody, commentary, and verse-composition revision.

The registry deliberately mixes ordinary, classical, biblical, patristic,
liturgical, theological, canonical, rhetorical, textual, and compositional
work. This is curricular breadth, not unverified author attribution.

## Evidence and source state

The shared source label is `Project gloss; external lexical locus open (U)`.
That status is honest and deliberate: citation forms, morphology, concise
senses, and construction cues are course-created instructional synthesis based
on the grammar and lexicography references listed by the curriculum, but a
per-entry dictionary locus and corpus-token collation has not yet been recorded.
The complete registry therefore may be used for supplied packet work while
remaining visibly distinct from an edition-verified author concordance.

When an exact author occurrence is later claimed, its audit must record passage
ID, exact token or form, work, edition, locus, and verification state. In
particular, the verified Ambrose source identifier supplied during this
revision is `AMB-KRAB1857`: Ambrose, *De officiis ministrorum* I.11.38, ed.
Johann Georg Krabinger (Tübingen: H. Laupp, 1857), printed p. 44, scan p. 61,
Internet Archive item `deofficiisminis00krabgoog`. This correction replaces the
unverified candidate `AMB-CSEL32.1` for that passage. It does not automatically
attest any registry lexeme until an exact-token mapping is recorded.

## Synchronization and public renderers

- `\RenderModuleMemoryLearner{SET}` and
  `\RenderModuleMemorySolutions{SET}` render packet-local memory work from the
  same source.
- `\RenderMemoryWorkbookLearnerPacket{SET}` and
  `\RenderMemoryWorkbookSolutionPacket{SET}` render the eight collected sheet
  families.
- `\RenderCompleteMemoryLexicon` renders the complete registry as the Reading
  Lexicon in EL-REFERENCE.

The design intentionally prevents a module list, workbook sheet, answer key,
and Reading Lexicon from becoming separately maintained copies.

## Audit checks completed

- 598 declaration rows counted;
- IDs are contiguous L001–L598 and unique;
- all 598 IDs occur in at least one set allocation;
- each trunk set has exactly 25 new IDs;
- each poetry set has exactly 6 new IDs;
- 81 unique grammar-fact IDs used across the sets;
- poetry packet IDs normalized to P1–P8;
- exact duplicate citation-form rows not found by the mechanical registry
  check;
- project gloss, strand, and source-status boundary printed in the workbook
  and complete Reading Lexicon renderer.

## Outstanding lexical review

Independent Latinist review is not claimed. Before describing the lexicon as
source-audited, complete at a numerical corpus threshold, or author-attested,
the project must add per-entry dictionary loci, frequency and coverage method,
exact source-token mappings, systematic word-family and collocation data, and
recorded review of material sense and government disputes. Those future checks
may correct an entry without changing its stable ID.
