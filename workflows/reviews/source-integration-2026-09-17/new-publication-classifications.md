# Independent classification of the two new GPT research surfaces

Decision on 2026-09-17: the two sorted arrays below classify the source strata actually present in each publication's current records. **Neither row remains `unresolved`.** This is classification only, not research, authoring, PDF, workflow or release acceptance. No inventory or publication was changed. The earlier integration and font-review reports remain unchanged.

## Method and snapshot

`tools/source-inventory` defines sixteen allowed category tokens and requires unique, sorted arrays. `src/sources/inventories/README.md` defines these as the kinds of source occurring in a publication's records, independently of identity certainty, rights, evidence state and migration disposition. Consequently, an expressly recorded, identifiable lead contributes its broad family without becoming an adopted or verified authority. An access host does not itself supply a category. The existing `classification-review-v1.toml` convention records one array per exact publication identity; its neighboring rows were inspected as convention, not copied as evidence.

The exact 21 input-file hashes, both machine-checked arrays, binding counts and entrypoint-presence observations are in `new-publication-classifications-inputs.json`, SHA-256 `4be8b0c70060649b8de3d75ff822708cf026f7e534a65e84195a7cd4333d49a9`. Both arrays were checked against the tool's actual `SOURCE_CATEGORIES` set and are allowed, sorted and unique. The NO snapshot includes the rights and GIRM dependency reentry recorded in its current `scope.md`.

## TLM: Seventeenth Sunday after Pentecost

```toml
[[classifications]]
document = "liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost"
source_categories = ["finding-aid", "historical-primary", "institutional-current", "liturgical", "magisterial", "patristic", "prayer-devotional", "repository-internal", "scholastic", "scripture", "secondary"]
```

All relative evidence paths in this table belong to this TLM leaf.

| Category | Actual source and recorded role |
| --- | --- |
| `finding-aid` | `context.md` records the calendar-day and rubric computations expressly as finding aids. `scope.md` records the Catena lead map and the raw extraction/OCR locating layer, without treating them as independently checked underlying authorities. |
| `historical-primary` | The 1862 Pustet pages 341–342 are direct antecedent witnesses used for inherited-wording/rights control; the 1861 Cummiskey printing at 431–433 controls historical human English. These are identified historical primary textual witnesses, not modern accounts about those books (`source-audit.md`, `english-verification.md`, bindings). |
| `institutional-current` | The dated FSSP France and ICRSP France Ordos corroborate the 20 September 2026 occurrence, rank and associated facts. Their local institutional scope is retained (`context.md`; the two final context bindings). |
| `liturgical` | The 1962 Vatican typical Missal controls the ten elements, calendar/rubrics, Credo and Trinity Preface appointment. Earlier Missal witnesses and the Cummiskey translation have separately bounded roles (`source-audit.md`, bindings). |
| `magisterial` | `scope.md`, second-search record, identifies the Vatican audience of 8 August 2001 as the locator for Basil on Psalm 32 §8 / PG 29, 343. This category records an identified papal-audience source occurrence; its role is only a secondary locator. It does **not** claim adopted magisterial argument or independent inspection of Basil. |
| `patristic` | The actual reception readings include Augustine's Psalms, *De doctrina christiana* and *De consensu evangelistarum*; Chrysostom on Matthew 71 and Ephesians 9–11; and Jerome on Daniel 9. Their distinct texts, translation limits and bounded inspections remain explicit (`scope.md`, bindings). |
| `prayer-devotional` | `scope.md`'s exact-incipit second search records modern devotional commentary and Guéranger excerpts as encountered but unadopted leads. This is a record-occurrence category, not an additional saintly or controlling source. It is not inferred merely from the presence of Missal prayers or the proposed homily. |
| `repository-internal` | The leaf actually uses the Roman 1962 proper/rubric registries and facsimile-rights inventory, explicitly named in `review-dependencies.toml`, as well as computed occurrence findings. This is more than an incidental workflow-policy reference. |
| `scholastic` | Aquinas, *Super Ephesios* 4 lectures 1–2 and *Summa* III.79 articles 1, 2 and 6, supplies directly inspected exegesis and doctrinal illumination. Those functions are distinct from explaining the prayers' composition (`scope.md`, bindings). |
| `scripture` | The American 1899 Douay–Rheims artifacts supply Matthew 22, Ephesians 4, Daniel 9 and Psalms 32, 75, 101 and 118. Canonical study English is distinguished from liturgical adaptations (`english-verification.md`, bindings). |
| `secondary` | The second-search record explicitly includes modern devotional/blog commentary, historical-liturgical leads, and the papal audience used secondarily to locate Basil. These remain locating or unadopted material. Neither New Advent nor a modern download date alone was used to infer this category. |

**Excluded:** `canon-law` (the actual governing rubric use is liturgical; no distinct canonical-code/decree authority is adopted in this leaf's source record), `classical`, `archival-material`, `dataset-survey`, and `unresolved`. No such additional intellectual family is established by the inspected records. An Internet Archive scan is not archival-material merely because of its host. Unknown translation identity or unresolved redistribution rights do not make an otherwise identifiable patristic or liturgical family `unresolved`.

## NO: Twenty-fifth Sunday in Ordinary Time, Year A

```toml
[[classifications]]
document = "liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a"
source_categories = ["canon-law", "finding-aid", "historical-primary", "institutional-current", "liturgical", "magisterial", "patristic", "repository-internal", "scholastic", "scripture", "secondary"]
```

All relative evidence paths in this table belong to this NO leaf unless its expressly named Week 25 owner is identified.

| Category | Actual source and recorded role |
| --- | --- |
| `canon-law` | The rights reentry explicitly adopts *Postquam Summus Pontifex* 2, 3 and 40. Its canonical work record identifies a general executory decree implementing canon 838. This is a distinct ecclesiastical-law authority for the rights/competence boundary (`scope.md`, `review-dependencies.toml`); civil copyright material alone would not establish this category. |
| `finding-aid` | Calendar arithmetic, the Dicastery variation index, catalog/concordance searches, the Catena leads, and OCR locating work are recorded as bounded finding aids rather than appointment or quotation authority (`context-source-plan.md`, `scope.md`, `source-audit.md`). |
| `historical-primary` | The historical PL 76 Gregory page witness, Parma 1863 Aquinas Isaiah pages, Dessain 1857 Pauline-commentary pages and O'Sullivan's 1866 Bellarmine expression supply direct historical textual witnesses. Their identified edition layers and actual role are kept distinct from modern summaries and modern reprints (`source-audit.md`). This broad category does not authenticate an unidentified historical impression or add a historical-composition claim. |
| `institutional-current` | The 2026 USCCB national calendar and dated daily readings page control occurrence and appointment. ICEL permissions, USCCB publication guidelines, and the WIPO treaty-party record have explicit rights roles; current institutional/publisher corroboration is recorded in the Week 25 owner. The future effective date of the 2025 guidelines remains distinguished from use of their printed rights notices (`scope.md`, `context-source-plan.md`). |
| `liturgical` | U.S. Missal/Lectionary identity, the ICEL Antiphonary, the separately limited Latin 2002 reproduction, GIRM branch norms and GILM arrangement norms are actual controlling or corroborating evidence. The common formulary is inherited only through this edition's Week 25 owner (`context.md`, `source-audit.md`, current dependency audit). |
| `magisterial` | The official ecclesiastical instruction *Liturgiam authenticam* 111 and the subsequent *Postquam Summus Pontifex* decree are explicit rights/authority evidence; the official Newman calendar decree is also an identified currentness-search result. This records the authoritative ecclesiastical-document stratum without asserting new doctrinal definitions or importing unrelated source ancestors (`scope.md`, `context-source-plan.md`). |
| `patristic` | Direct, bounded reception includes Augustine 87, Psalms, *Predestination* I.41 and John 47; Chrysostom Matthew 64, Acts 35 and Philippians 3–4; Gregory 19; Irenaeus II.13.3–4; and Jerome on Isaiah 55. Their different witness and inspection limits remain intact (`source-audit.md`, bindings). |
| `repository-internal` | The explicit same-edition Week 25 owner, edition formula/occurrence registry, and applicable rights inventories are used and declared dependencies. Their institutional/rights source links are not treated as automatically sealed merely because they are mentioned in an inventory (`scope.md`, current `review-dependencies.toml`). |
| `scholastic` | Aquinas's Isaiah 55 and *Super Philippenses* 1 lectures 3–4 are independently inspected medieval exegesis supporting the actual arguments; no additional Aquinas authority is manufactured from search snippets (`source-audit.md`, bindings). |
| `scripture` | Six exact Challoner/Gutenberg book artifacts supply Isaiah, Psalms, Matthew, Philippians, Acts and John for public-domain study context. This leaf does not use the TLM leaf's American 1899 Bible identity or its appointed passages (`edition-manifest.md`, bindings). |
| `secondary` | Recorded modern commentary discussion/reposts and the modern Veronese-antecedent claim are search leads, expressly not adopted proof. The Week 25 owner also distinguishes its secondary digital Missal reproduction from an exact altar-book facsimile. No source host is classified as secondary simply by being a website (`scope.md`, Week 25 audit). |

**Excluded:** `prayer-devotional`, `classical`, `archival-material`, `dataset-survey`, and `unresolved`. The actual Missal prayers remain liturgical sources; a future homily is an output genre, not evidence that a separate devotional source family has been used. The NO record's identified commentary and repertory leads do not establish the TLM record's Guéranger/devotional stratum. Jerome's unresolved exact-delivery rights remain independent of his known patristic family. The uninspected Veronese antecedent is not promoted to manuscript/archival evidence. WIPO's treaty-party record is used as institutional rights information, not an empirical survey.

## Effect of unfinished companions

The inventory universe is discovered from each exact `main.tex`; category decisions concern its current owned source surface, not final PDF completion. At this inspection the TLM leaf has `main.tex`, `synthesis.tex`, `homily.tex` and a component manifest, while the NO leaf has only its 77-byte comment-only `main.tex` among those entrypoints. This is a presence check only, not an assessment of their completeness.

The missing NO authored companions do **not** block these category decisions or require an `unresolved` placeholder: the substantive research records already identify their actual source strata. They do block any claim that authoring or publication is complete, which this review does not make. Later authoring must trigger ordinary source-surface refresh; any genuinely new source family must also revise classification. A future category cannot be supplied now solely from an intended companion, a neighboring publication, or the other liturgical family's research.

The two assessments used separate local research records. Only the NO leaf's expressly declared same-edition shared owner was treated as inherited evidence. No TLM/NO appointments, texts, interpretations, source sufficiency judgments, or acceptance states were transferred between them.
