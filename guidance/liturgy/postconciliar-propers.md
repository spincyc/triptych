# Postconciliar Proper Guides

This delta profile governs source-first guides to the textual variable parts of an identified postconciliar Roman-rite celebration. Follow [the universal editorial standard](../editorial.md) and [repository rules](../repository.md) first. Use [the stable proper registry](postconciliar-propers-registry.md) for permanent identities, keys, slugs, ordering, counts, owners, and occurrence grammar; use the selected edition-locale's `propers/registry/` records for adoption, dispositions, and dated occurrence results; use [calendar computation](calendar-computation.md) for every cycle letter, weekday numeral, Ordinary Time week number, and movable date. The Missal, Lectionary, ritual books, calendar, and approved chant sources identified by the manifest control the actual target.

## Governing priorities

Apply these priorities in order:

1. **Identify the instance.** Fix the edition, language, territory, calendar, date when needed, formula key or other governing identity, source owner, cycle, form, ritual context, and branch universe before drafting.
2. **Collate the complete target.** Verify every appointed and permitted textual unit against the identified books; never combine editions, territories, cycles, calendars, or option paths into a synthetic formulary.
3. **Preserve source roles.** Keep the reusable Missal or Ritual Mass owner distinct from the cycle- or occurrence-specific leaf; keep verified text, documented history and reception, source-grounded synthesis, and editorial proposal distinct.
4. **Serve the reader's flow.** Open with the texts and synthesis. Put resolution mechanics and all work-wide edition, jurisdiction, chronology, geography, search, rights, limitation, currentness, and review apparatus in the terminal appendices.
5. **Fail closed.** Do not infer a key, slug, cycle split, edition disposition, occurrence, textual option, or local enactment. Record unresolved states in the tracked records and qualify only the claims they affect.

## Identity, registry, and ownership

**This collection is closed.** The maintainer bounded it at the set already
published on 2026-07-25; the registry's identities stay complete and permanent,
but an identity with no guide is the normal state and not a target. See
[the production plan](propers-production-plan.md) for the boundary and for how
to derive what each provider has actually published.

Under a provider branch, a publishable leaf lives at:

`src/<provider>/liturgy/roman-rite/postconciliar/<edition-locale>/propers/<calendar-family>/<full-publication-slug>/`

Use `temporal` for `PC-S` and `PC-T` leaves and `general-calendar` for `PC-R` leaves. The stable registry controls the fixed source-owner paths, the `PC-T03` Easter Vigil alias, and reserved `PC-W` namespace. Each edition-locale owns a non-publishable `propers/registry/` directory containing:

- an index naming the governing editions, territory, records, and currentness;
- formula dispositions that adopt, qualify, or leave unresolved the stable registry targets; and
- dated occurrence records when a civil date is resolved.

An edition record may add only a directly collated, expressly documented edition delta. If an `ABC` target proves materially cycle-dependent, or another approved adaptation changes the target shape, stop publication until the edition record lists the exact replacement keys, slugs, positions, and adjusted counts. An unresolved edition expansion contributes no invented key or count.

The shared owner keeps the reusable edition-specific Missal or Ritual Mass audit, provenance, rights status, and any lawful fragment. The leaf keeps the formula composition, Lectionary and branch audit, research, generation metadata, and PDF. It references or imports exactly one canonical formulary owner, names that owner in the manifest and in its own audit, and never becomes a second owner: it must not duplicate protected owner wording, and it must not restate the owner's edition evidence, locators, checksums, variation audit, element boundaries, or analytic summaries in its own words. The stable registry fixes the owner path for every parent and makes the Ordinary Time owner computable from the parent number; create the owner before the leaf that consumes it, and let all three cycle leaves under one parent share it.

Every external owner, shared fragment, and edition registry record that controls a build is an explicit dependency; rebuild and re-review every consumer after it changes. Declare each edge in the Makefile beside the collection's existing shared edges, following the established `SACRAMENT_SHARED` and `POSTCONCILIAR_US_FORMAT` pattern: collection-wide shared material is declared once against the collection's build PDFs, while a per-parent or per-week formulary owner is declared as a prerequisite of each consuming leaf's PDF target. An undeclared owner is a build defect even where the leaf reads correctly.

### Commons recovery evidence

`src/sources/inventories/postconciliar-sanctoral-commons-v1.toml` is the
durable recovery of Common directions already present on dated calendar
records. It is an inventory, not a resolver input: no row creates a
`takes_from` or `common_from` edge, chooses among alternatives, or establishes
the target Missal's formulary body. An *Ordo lectionum Missae* heading governs
the reading provision only. A direction recovered from the ICEL Antiphonary
governs antiphons only, because that excerpt carries no orations and is not a
ritual edition. A historical antecedent flagged as wrong-edition evidence
never becomes evidence for the target postconciliar Missal.

Keep one row per singular dated Mass key, including same-date celebrations as
separate rows. Preserve the exact heading, artifact and printed-page locator,
entry number, alternatives, and sub-selection stated by the owning evidence;
do not derive a Common from the saint's title. Refresh the inventory whenever
those calendar notes or directions change, and leave every row fail-closed
until a source with authority for the exact target-Missal relation has been
read. The inventory is deliberately absent from public projections.

## Required tracked records

Every publishable leaf contains:

```text
<full-publication-slug>/
  main.tex
  generation-metadata.tex
  instance/
    manifest.md
  propers/
    verified.md
  research/
    scope.md
```

Each shared owner named by the registry is a non-publishable source directory:

```text
<owner>/
  propers/
    verified.md
```

Add a focused finding aid beside it only where the evidence rules require one. An owner has no `main.tex`, `generation-metadata.tex`, `web-edition.toml`, PDF mirror, or catalog entry, and no reader-facing apparatus; it is a source of record, not a publication.

`instance/manifest.md` is the authoritative identity and resolution record. It names the stable and edition registries, permanent parent and formula key when assigned, full slug, canonical owner, editions, language, territory, calendars, as-of date, rank, cycle, form, occurrence, ritual context, branch universe, resolved selections, and unresolved choices.

The owner's `propers/verified.md` verifies the reusable formulary, rubrics, elements, editions, locators, provenance, rights, variants, discrepancies, and collation date. The leaf's `propers/verified.md` verifies the target composition: registry identity, owner, complete ordered textual-unit inventory, Lectionary boundaries, chant layers, semantic branches, source locators, rights dispositions, resolutions, discrepancies, and collation date.

`research/scope.md` preserves the operational scholarship audit displaced from the publication: biblical and liturgical contexts, historical judgments, direct and illuminating reception, languages and corpora searched, material disagreement, negative results, material rejected and unresolved leads, claim and branch limits, source roles, rights boundaries, and review performed or outstanding. It is not a diary or chain-of-thought record.

## Published text and English

### Component architecture

The component architecture here supersedes the older two-leaf packaging
language below while existing pilots are migrated. New and substantially
revised guides use one canonical leaf and provider-neutral
`proper-components.toml`. The bare ID produces the complete research PDF and
sole full HTML edition. A mechanical `-synthesis` PDF companion uses the same
source and owns no prose, audit record, or web declaration.

The manifest assigns stable lowercase kebab-case keys to every textual unit
and records ordered components, mode membership, dependencies, element
bindings, and component-scoped references. Each synthesis relation joins at
least two element keys and declares controlled evidence classes. No component
included in one mode may depend on a component omitted from that mode.

The research edition contains the existing pages 1 and 2; every lawfully
reproducible appointed text; `Each Proper in Full` with the bounded reception
sweep; exactly two pages of `The Propers: Themes and Movement`; unbounded
`Source-Grounded Synthesis Across the Propers`; unbounded `Interpretive
Possibilities Across the Propers`; notable quotations; and
terminal apparatus. The synthesis companion retains pages 1 and 2, brief
synthesis, the complete source-grounded synthesis, the complete exploratory
synthesis, notable quotations, and terminal apparatus. It omits both the
appointed-text component and the per-element sweep. It remains subject to the
copyright limits below.

Because rights prevent this canonical edition from reproducing every
controlling appointed text in full, its catalog label is `Research PDF`;
the companion is `Synthesis PDF`. `Full PDF` is reserved for a canonical
edition whose texts are actually complete.

Mark the brief synthesis with
`triptych:brief-synthesis:start`,
`triptych:brief-synthesis:end`, and
`triptych:brief-synthesis:next`. After the build settles,
`tools/tpt check-proper-components --aux` must find those markers on pages N,
N+1, and N+2. Page breaks without that validation do not meet the exact
two-page requirement.

The rights position for these installed PDFs is narrower than it is for the
site's live display. The ICEL English of the Roman Missal is under copyright;
ICEL's standing permission is limited to a qualifying no-fee noncommercial
Internet site and expressly grants no license for another form of publication.
It therefore is not reproduced in these PDFs. Lectionary text is controlled
separately by CCD and is not reproduced either. Nor is any Bible translation
under copyright — the Knox, Jerusalem and New Jerusalem, RSV and NRSV, NABRE,
and the Grail psalms are all excluded.
A guide may cite a locus, describe what a text says, and quote the short
phrase an argument actually turns on; it may not stand in for the book.

Within that bound:

- Scriptural pericopes and antiphons are given in the Douay–Rheims
  (Challoner), which is public domain. Because the reader will hear a
  different translation at Mass, every leaf carries a standing notice —
  in the terminal scope appendix and again where scripture first appears
  — stating plainly that the English printed is a public-domain study
  translation and is **not** the text proclaimed in the celebration, and
  naming the Lectionary as the controlling English.
- Orations get their Latin incipit from the *editio typica* and a
  description of what the prayer asks. Do not supply a rendering of the
  project's own, and do not paraphrase the ICEL text closely enough to
  reconstruct it.

Do not copy a live-page acknowledgement into the PDF and infer that it expands
the permission. For a future qualifying web display of excerpts, ICEL currently
prescribes `Excerpts from the English translation of The Roman Missal © 2010,
International Commission on English in the Liturgy Corporation. All rights
reserved.` That notice is necessary where applicable but does not clear a PDF,
a public data bundle, USCCB-specific material, or CCD/Lectionary text.

Where this leaves an element without English, say so in that element's
own place rather than in a general disclaimer. An honest gap is a
finding; a quiet substitution is a defect.

## Research and claim discipline

Read every selected passage in its complete literary context. Distinguish composition, first audience, and narrated event; preserve traditional attribution, modern judgment, disagreement, and uncertainty without silent harmonization. Seek direct patristic or saintly exegesis before later doctrinal or liturgical illumination, and record material negative results rather than inventing a witness.

Maintain a passage-by-passage reception matrix in `research/scope.md` for every reading, psalm, scriptural acclamation, and book-identified antiphon or adaptation in every authorized branch. Consolidate repeated passages while naming all uses. Each row records direct ancient exegesis checked; medieval, Doctoral, or later saintly reception checked; works, loci, languages, and corpora searched; the role of every retained witness; and material negative results. Search direct commentaries, homilies, and psalm expositions first; then major relevant Greek and Latin Fathers; then medieval Doctors and later canonized exegetes or spiritual writers; and only then illuminating doctrinal or liturgical reuse. Use a catena as a lead map only and verify the underlying work and locus.

Breadth requires a documented search for every appointed passage across the major reasonably accessible patristic and saintly corpora relevant to it. Depth requires the commentary to explain and, where useful, compare the witnesses' arguments rather than stack names or isolated sayings. Retain a direct checked witness wherever one is found and multiple voices where they materially differ, converge by distinct reasoning, or show development. If no direct witness is located, identify the corpora checked and label any broader reuse as illuminating rather than direct. Never claim universal exhaustiveness; define the bounded search so later omissions remain correctable.

Classify every cross-element relation before drafting:

- `officially correlated`;
- `responsorial`;
- `acclamatory`;
- `semi-continuous`;
- `seasonal or ritual`;
- `textual observation`;
- `documented reception`;
- `source-grounded synthesis`; or
- `editorial or AI proposal`.

The General Introduction to the Lectionary controls these classifications. In Ordinary Time, the Old Testament reading is normally correlated with the Gospel while the apostolic and Gospel courses remain semi-continuous; do not impose a whole-formulary thematic design. Shared orations and antiphons likewise are not historically designed for one cycle's readings without direct evidence.

Use these controlled branch statuses in the tracked records: `required`, `appointed alternative`, `conditional`, `permitted`, `ritual substitution`, `locally selected`, `omitted`, and `not applicable`. Do not collapse omission into inapplicability or narrate mutually exclusive alternatives as one enactment.

## Reader-facing order

Use this macro-order:

1. compact title block naming only the celebration and the formula, cycle, or form needed to identify the object;
2. unheaded two-column textual-variable-parts inventory in actual liturgical order;
3. unheaded four-senses table;
4. physical page 2 alone: `Scriptural Date and Location`;
5. exactly two pages of `The Propers: Themes and Movement`;
6. unbounded `The Propers: Detailed Commentary`;
7. required `The Propers: Notable and Quotable`;
8. required `The Propers: Interpretive Possibilities`, with one global editorial or AI disclosure;
9. any required `Sacramental Appendix`;
10. fresh-page `Appendix: Liturgical Resolution`;
11. `Appendix: Scope and Qualifications`;
12. `References`; and
13. terminal imported `Generation Metadata`.

For an ordinary Sunday or solemnity, the title, complete inventory, and four-senses table occupy page 1. The date/location sheet begins and ends at forced page boundaries and is the only content on physical page 2. `Themes and Movement` begins on page 3 and fills exactly two substantive, readable pages without a repeated heading or continuation label. `Detailed Commentary` begins on page 5 and has no upper limit. Do not use padding, artificial whitespace, omitted material, or hidden qualifications to meet a page boundary; use compact but readable tabular design only where the complete page-2 inventory requires it.

The page-2 sheet is the sole exception to terminal historical apparatus. It carries passage-specific composition and narrated-event orientation, not edition verification, jurisdiction, rights, source status, search method, currentness, review state, or other global qualification. Liturgical resolution and scope remain terminal before `References`. Keep only a claim-local qualification beside the claim it changes.

## Page-one inventory and four senses

The textual inventory has exactly two conceptual columns:

| Column | Content |
| --- | --- |
| `Textual unit` | One text-bearing variable unit in its actual ritual position. |
| `Text / citation` | Minimal prayer or antiphon identifier, exact biblical citation and boundary, and ordinary-language labels for all closed alternatives of that unit. |

Use one row per actual unit, not per branch. Group rows with visible phase labels appropriate to the form and omit empty phases. Keep semantic branch IDs and authority in the resolution appendix and tracked records. Include every appointed unit and every concretely documented local selection; keep an unresolved open selection class in the records unless it materially identifies or limits the guide.

Inspect, as applicable, entrance rites and chants; Collect; readings; Responsorial Psalm; Sequence; acclamation; Gospel; concretely appointed or selected Preparation chant; Prayer over the Offerings; proper, narrowly appointed, or concretely selected Preface; proper Eucharistic Prayer insert; Communion antiphon or selected chant; Prayer after Communion; and distinctive concluding text. Special vigils and rituals follow their actual repeated or substituted units.

The following unheaded table has columns `Sense` and `Synthesis` and exactly four rows: `Literal`, `Allegorical`, `Moral`, and `Anagogical`. Ground every row in the appointed texts or documented reception, preserve branch limits and relationship classifications, and exclude original proposals.

## Page-two scriptural date and location

`Scriptural Date and Location` inventories every distinct directly appointed biblical passage and book-identified scriptural adaptation: readings, psalms, scriptural acclamations, and scriptural Missal or ritual texts. Label `Cf.` and equivalent wording as adaptation or allusion; exclude loose echoes in composed orations. Order dossiers by Catholic canonical book order and then chapter and verse. Consolidate repeated passages while naming every unit and branch. Use these conceptual columns:

| `Textual unit / alternative` | `Citation` | `Location` | `Date` |
| --- | --- | --- | --- |

For each dossier, distinguish inherited attribution from historical judgment and state, as evidence permits, authorship, composition date and place, first audience, horizon, and salvation-historical setting. Add a separate `Narrated event` row when event and composition differ. Keep writer, audience, and event locations distinct. The sheet contains orientation, not copyrighted biblical text. Keep source-role disputes and operational research detail in `research/scope.md`, and keep global edition, branch, jurisdiction, rights, search, currentness, and review qualifications in the terminal scope appendix. The complete sheet always occupies exactly one physical page; if it does not fit legibly, redesign its dossiers or table rather than spill, omit evidence, or introduce unrelated apparatus.

Present each passage as a compact two-tier dossier, following the established temporal-propers hierarchy rather than a flat run of unrelated rows. The first tier is a concise four-field summary in `Textual unit / alternative`, `Citation`, `Location`, and `Date`; when composition and narrated event differ, place an italic `Narrated event` row immediately beneath that summary and bound it with partial rules. The second tier is one full-width explanatory row, normally about `0.92\linewidth`, that distinguishes inherited attribution from historical judgment and records audience, life-setting, uncertainty, and claim-local source anchors. Separate complete dossiers with full rules only. As a default starting point, use top-aligned ragged-right columns near `0.14`, `0.18`, `0.35`, and `0.16` of the line width, `\footnotesize`, `\LTpre` near `0.15em`, zero `\LTpost`, and `\arraystretch` near `1.02`; change those measurements only as needed to keep the single page legible and complete.

## Synthesis, commentary, and proposals

`The Propers: Themes and Movement` gives the source-grounded architecture of the complete target. Begin with a concise governing account and a scan-first form of no more than four primary stages. Use three to five relationship-titled units for an ordinary formula and only the extra units demanded by a complex vigil or ritual. Every inventoried unit belongs to a functional grouping or is identified as an independent, semi-continuous, or optional strand. No prose paragraph exceeds 120 words and no unstructured prose run exceeds two paragraphs.

`The Propers: Detailed Commentary` supplies the evidence and claim-local qualifications behind the synthesis. Treat every inventoried prayer, antiphon, reading, psalm, acclamation, sequence, Preface, insert, blessing, dismissal, or other variable unit in full. For every appointed Scripture passage, move from complete canonical context through direct patristic exegesis to medieval and later saintly reception, explaining the interpretive reasoning and comparing material differences or developments. Do not let liturgical synthesis substitute for passage-level exegesis, and do not use a list of authorities as depth. Organize by the strongest evidenced relationships and ritual movement rather than mechanically repeating the inventory. Each substantial claim has one fullest home.

**`The Propers: Notable and Quotable` and `The Propers: Interpretive
Possibilities` are governed by [the 1962 proper-guide profile](roman-1962-propers.md),
"Themes, commentary, and exploration",** which owns both contracts for every
proper guide in either collection: what qualifies as an afterlife and what does
not, the `Notable-and-quotable audit`, the four-to-six proposal shape, the
targeted precedent search, the `Interpretive-proposal audit`, and the three
novelty classifications. The two profiles carried that text verbatim until
2026-08-01, when the copies were found identical and one owner was named.

Four deltas apply here, all of them consequences of the postconciliar rite's
option branches:

- A gallery entry may draw its phrase from an appointed biblical text **or an
  authorized branch**, and it identifies the branch as well as the proper.
- The `Notable-and-quotable audit` records the **branch** alongside the other
  fields that entry names.
- A proposal keeps **optional branches distinct** unless it explicitly compares
  them as alternatives.
- A surviving proposal is controlled additionally by **official correlations,
  independent or semi-continuous strands, and authorized branches**. Attribute no
  proposal to a cited authority and claim no historical compositional intent.

## Terminal appendices

### Appendix: Liturgical Resolution

Give the reader only the identity and resolution needed to interpret the textual record:

- celebration, rank, season, color, parent and formula key or other governing identity, form, and occurrence;
- governing edition-locale, calendar, territory, owner, Lectionary locator, and other controlling books;
- production coverage, actual Sunday cycle, independent weekday cycle when applicable, and source-owner relationship; and
- treated branches and any selection established by the evidence.

When reader-relevant branches exist, use:

| Branch ID | Authority and trigger | Status | Units affected | Resolution |
| --- | --- | --- | --- | --- |

Use one stable semantic branch ID unchanged in the appendix, manifest, and leaf audit. A branch never creates a formula key unless the stable or edition registry expressly does so. Model dependent Preface and Eucharistic Prayer selections as coupled branches under the governing rubric.

### Appendix: Scope and Qualifications

Consolidate the work-wide edition and formulary scope, branch universe, governing calendar and jurisdiction, chronological and geographic bounds, source and verification scope, search method, rights and use limits, currentness, unresolved global questions, and review state. Point to the manifest, leaf and owner audits, edition registry records, and research scope instead of reproducing them. `References` contains only sources actually used and does not repeat this apparatus.

## Form-specific modules

Use the target's actual order:

| Target | Required delta |
| --- | --- |
| Ordinary Sunday or solemnity | Actual Introductory Rites, Liturgy of the Word, Liturgy of the Eucharist, Communion, and any distinctive conclusion. |
| Palm Sunday | Separate Entrance commemoration and Mass; procession, solemn, and simple entrances; cycle Gospel; Passion lengths; admitted pre-Gospel reduction. |
| Evening Mass of the Lord's Supper | Introductory Rites, Liturgy of the Word, washing of feet where carried out, Liturgy of the Eucharist, transfer of the Most Blessed Sacrament, and the prescribed conclusion. |
| Celebration of the Lord's Passion | Liturgy of the Word, Solemn Intercessions, Adoration of the Holy Cross, and Holy Communion; preserve every appointed option and branch. |
| Easter Vigil | Service of Light, repeated Word modules, Baptismal Liturgy, Eucharist; reduction rule and required Exodus; initiation and reception paths. This is the `PC-T03` identity resolved through the existing `PC-S17-*-VIGIL` targets, never a duplicate leaf. |
| Easter Day | Second-reading alternatives, Sequence, Gospel paths, and authorized baptismal renewal. |
| Pentecost Vigil | Separate simple and extended targets; preserve each reading–psalm–collect module. |
| Pentecost Day | Sequence and every edition-appointed cycle-dependent alternative. |
| Scrutiny target | Ritual Mass owner, Year A initiation readings, proper prayers and Preface, intercessions, exorcism, and dismissal or retention. |
| Sunday replacement or weekday fallback | Same Missal owner, independently resolved Lectionary structure and every cycle-specific alternative. |
| Other Ritual Mass | Actual sacramental order and every Mass-changing ritual text; add the sacramental appendix when required. |

This table creates no key. The registries and selected books decide whether material is a target, branch, conditional Ritual Mass, or occurrence.

## Workflow and completion gate

For each new or substantially revised guide:

1. confirm or create the registry-fixed shared owner, then complete the manifest and edition-registry disposition;
2. collate the owner and target, including every branch and rights-safe locator, and declare the owner's build edge;
3. study Scripture, reception, liturgical function, and material negative results;
4. classify relationships and claims;
5. draft detailed commentary before compressing the synthesis and four senses;
6. assemble the page-2 date/location sheet and terminal apparatus and refresh structured metadata; and
7. build, inspect every page and branch table, and install only the reviewed PDF.

A guide is profile-final only when its registry identity, slug, path, owner, edition disposition, and occurrence are resolved; its shared owner exists at the registry-fixed path, alone carries the formulary evidence, and is declared as an explicit build edge, while the leaf restates none of it; its cycle letter and any weekday numeral were resolved independently under [calendar computation](calendar-computation.md) and confirmed against a dated official witness; its owner and leaf audits are complete; all authorized branches and textual units are accounted for; its claims and relationships are classified; its passage-by-passage matrix documents bounded searches of the major relevant Greek and Latin patristic and later saintly corpora, checked loci, witness roles, and negative results; its detailed commentary proves breadth and depth for every appointed passage; its notable-and-quotable section has three to five source- and locus-identified, non-obvious cultural, humorous, ironic, idiomatic, literary, political, institutional, visual, scientific, commercial, or comparable reuses of wording from the scriptural propers, with every verbal relation, contextual turn, branch, right, payoff, limit, and material negative result audited and no patristic excerpt or bare title, motto, artwork, or musical setting used as padding; its interpretive section contains four to six non-recapitulatory, multi-element proposals and its research scope records each proposal's anchors, mechanism, targeted precedent result, fruit, and strongest limit without claiming universal novelty; page 2 contains only the complete one-page date/location sheet, pages 3--4 contain the thematic movement, detailed commentary begins on page 5, and every later boundary conforms; work-wide qualifications appear only in the terminal scope appendix; rights and source records conform; every shared dependency is explicit and rebuilt; and build, metadata, log, and visual checks pass.

Do not call an edition-locale collection complete until every stable-registry target has a sourced disposition, all edition splits and conditional targets are evaluated, all weekday fallbacks are evaluated, and the replacement and local-overlay matrix is resolved. Absence in one civil year is an occurrence result, not a target disposition.

Exact-snapshot release approval authorizes only the named installed PDF hash. It does not make a guide profile-final, certify missing collation or review, or authorize a changed build. Keep any accepted limitation in the terminal scope appendix, catalog, and tracked records.

The structural schema is grounded in the Holy See's [General Instruction of the Roman Missal](https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20030317_ordinamento-messale_en.html), the approved [General Introduction to the Lectionary](https://www.liturgyoffice.org.uk/Resources/GIRM/Documents/Lectionary.pdf), the official [Roman Missal, Third Edition contents](https://www.liturgyoffice.org.uk/Missal/Information/RM3-contents.pdf), the bishops' [Missal Antiphonary](https://www.liturgyoffice.org.uk/Missal/Music/Antiphonary.pdf), official matrices for special forms, and the approved initiation rite. Exact editions, later decrees, territorial adaptations, and the competent calendar control each leaf.
