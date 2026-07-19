# Postconciliar Proper Guides

This delta profile governs source-first guides to the textual variable parts of an identified postconciliar Roman-rite celebration. Follow [the universal editorial standard](../editorial.md) and [repository rules](../repository.md) first. Use [the stable proper registry](postconciliar-propers-registry.md) for permanent identities, keys, slugs, ordering, counts, owners, and occurrence grammar; use the selected edition-locale's `propers/registry/` records for adoption, dispositions, and dated occurrence results. The Missal, Lectionary, ritual books, calendar, and approved chant sources identified by the manifest control the actual target.

## Governing priorities

Apply these priorities in order:

1. **Identify the instance.** Fix the edition, language, territory, calendar, date when needed, formula key or other governing identity, source owner, cycle, form, ritual context, and branch universe before drafting.
2. **Collate the complete target.** Verify every appointed and permitted textual unit against the identified books; never combine editions, territories, cycles, calendars, or option paths into a synthetic formulary.
3. **Preserve source roles.** Keep the reusable Missal or Ritual Mass owner distinct from the cycle- or occurrence-specific leaf; keep verified text, documented history and reception, source-grounded synthesis, and editorial proposal distinct.
4. **Serve the reader's flow.** Open with the texts and synthesis. Put resolution mechanics and all work-wide edition, jurisdiction, chronology, geography, search, rights, limitation, currentness, and review apparatus in the terminal appendices.
5. **Fail closed.** Do not infer a key, slug, cycle split, edition disposition, occurrence, textual option, or local enactment. Record unresolved states in the tracked records and qualify only the claims they affect.

## Identity, registry, and ownership

Under the present provider, a publishable leaf lives at:

`src/gpt/liturgy/roman-rite/postconciliar/<edition-locale>/propers/<calendar-family>/<full-publication-slug>/`

Use `temporal` for `PC-S` leaves and `general-calendar` for `PC-R` leaves. The stable registry controls the fixed source-owner paths and reserved `PC-W` namespace. Each edition-locale owns a non-publishable `propers/registry/` directory containing:

- an index naming the governing editions, territory, records, and currentness;
- formula dispositions that adopt, qualify, or leave unresolved the stable registry targets; and
- dated occurrence records when a civil date is resolved.

An edition record may add only a directly collated, expressly documented edition delta. If an `ABC` target proves materially cycle-dependent, or another approved adaptation changes the target shape, stop publication until the edition record lists the exact replacement keys, slugs, positions, and adjusted counts. An unresolved edition expansion contributes no invented key or count.

The shared owner keeps the reusable edition-specific Missal or Ritual Mass audit, provenance, rights status, and any lawful fragment. The leaf keeps the formula composition, Lectionary and branch audit, research, generation metadata, and PDF. It references or imports exactly one canonical formulary owner and must not duplicate protected owner wording. Every external owner, shared fragment, and edition registry record that controls a build is an explicit dependency; rebuild every consumer after it changes.

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

`instance/manifest.md` is the authoritative identity and resolution record. It names the stable and edition registries, permanent parent and formula key when assigned, full slug, canonical owner, editions, language, territory, calendars, as-of date, rank, cycle, form, occurrence, ritual context, branch universe, resolved selections, and unresolved choices.

The owner's `propers/verified.md` verifies the reusable formulary, rubrics, elements, editions, locators, provenance, rights, variants, discrepancies, and collation date. The leaf's `propers/verified.md` verifies the target composition: registry identity, owner, complete ordered textual-unit inventory, Lectionary boundaries, chant layers, semantic branches, source locators, rights dispositions, resolutions, discrepancies, and collation date.

`research/scope.md` preserves the operational scholarship audit displaced from the publication: biblical and liturgical contexts, historical judgments, direct and illuminating reception, languages and corpora searched, material disagreement, negative results, rejected and unresolved leads, claim and branch limits, source roles, rights boundaries, and review performed or outstanding. It is not a diary or chain-of-thought record.

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

## Synthesis, commentary, and proposals

`The Propers: Themes and Movement` gives the source-grounded architecture of the complete target. Begin with a concise governing account and a scan-first form of no more than four primary stages. Use three to five relationship-titled units for an ordinary formula and only the extra units demanded by a complex vigil or ritual. Every inventoried unit belongs to a functional grouping or is identified as an independent, semi-continuous, or optional strand. No prose paragraph exceeds 120 words and no unstructured prose run exceeds two paragraphs.

`The Propers: Detailed Commentary` supplies the evidence and claim-local qualifications behind the synthesis. Treat every inventoried prayer, antiphon, reading, psalm, acclamation, sequence, Preface, insert, blessing, dismissal, or other variable unit in full. For every appointed Scripture passage, move from complete canonical context through direct patristic exegesis to medieval and later saintly reception, explaining the interpretive reasoning and comparing material differences or developments. Do not let liturgical synthesis substitute for passage-level exegesis, and do not use a list of authorities as depth. Organize by the strongest evidenced relationships and ritual movement rather than mechanically repeating the inventory. Each substantial claim has one fullest home.

`The Propers: Notable and Quotable` is a required compact gallery of three to five non-obvious afterlives of wording from the scriptural propers. Each entry pairs a short exact phrase from an appointed biblical text or authorized branch with a documented later use that changes its register or force: cultural, humorous, ironic, idiomatic, literary, political, institutional, visual, scientific, commercial, or another surprising reuse. Identify the proper and branch, later user or work, context and exact locus; then explain the turn in meaning. Prefer a varied gallery and include humorous, ironic, or deliberate reversal where a verified example exists.

Straight exegesis, doctrinal or devotional reception, an independently similar phrase, and a bare quotation, title, motto, artwork, or musical setting do not qualify. Those materials belong in detailed commentary or references unless the later use demonstrably redirects, contests, jokes with, secularizes, or otherwise makes unexpected work of the appointed wording. Verify the verbal link and later context in a primary source or reliable edition; describe an echo as an echo unless dependence is documented; keep protected excerpts brief. The `Notable-and-quotable audit` in `research/scope.md` records both texts and loci, relationship strength, wording check, context, translation and rights status, cultural payoff, limiting qualification, branch, and material negative results. Quote aggregators and attribution sites are leads only. Never invent a weak example to fill the gallery.

Place every original analogy, typological extension, compositional inference, or unsourced cross-element connection in the required `The Propers: Interpretive Possibilities`. This is a discovery section, not a recap. Give four to six substantial proposals. Each must join at least two precisely named appointed elements; explain the connecting mechanism and the theological, intellectual, spiritual, or pastoral fruit; identify what the ordinary element-by-element reading misses; and end with the strongest material limit, alternative, or disconfirming condition. Prefer non-obvious multi-step relations across different ritual moments, literary units, images, verbs, temporal movements, or sacramental actions. Keep optional branches distinct unless the proposal explicitly compares them as alternatives. Reject generic applications, decorative symbolism, uncontrolled numerology, and compressed restatements of the detailed commentary.

Before retaining a proposal, search the leaf's checked corpus and run a targeted precedent search for its distinctive conjunction. Record an `Interpretive-proposal audit` in `research/scope.md` naming the anchors, mechanism, nearest located precedent or analogue, search boundary, and controlling limit. Classify the novelty result as `precedent located`, `near analogue located`, or `not located in the checked corpus`. The last formula is bounded and correctable; never claim that a connection is universally unknown, unprecedented, first, or authored by the model. A daring proposal may remain when the precedent search is negative, but official correlations, independent or semi-continuous strands, authorized branches, evidence, doctrine, literal senses, and historical uncertainty still control it. Attribute no proposal to a cited authority and claim no historical compositional intent.

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
| Easter Vigil | Service of Light, repeated Word modules, Baptismal Liturgy, Eucharist; reduction rule and required Exodus; initiation and reception paths. |
| Easter Day | Second-reading alternatives, Sequence, Gospel paths, and authorized baptismal renewal. |
| Pentecost Vigil | Separate simple and extended targets; preserve each reading–psalm–collect module. |
| Pentecost Day | Sequence and every edition-appointed cycle-dependent alternative. |
| Scrutiny target | Ritual Mass owner, Year A initiation readings, proper prayers and Preface, intercessions, exorcism, and dismissal or retention. |
| Sunday replacement or weekday fallback | Same Missal owner, independently resolved Lectionary structure and every cycle-specific alternative. |
| Other Ritual Mass | Actual sacramental order and every Mass-changing ritual text; add the sacramental appendix when required. |

This table creates no key. The registries and selected books decide whether material is a target, branch, conditional Ritual Mass, or occurrence.

## Workflow and completion gate

For each new or substantially revised guide:

1. complete the manifest and edition-registry disposition;
2. collate the owner and target, including every branch and rights-safe locator;
3. study Scripture, reception, liturgical function, and material negative results;
4. classify relationships and claims;
5. draft detailed commentary before compressing the synthesis and four senses;
6. assemble the page-2 date/location sheet and terminal apparatus and refresh structured metadata; and
7. build, inspect every page and branch table, and install only the reviewed PDF.

A guide is profile-final only when its registry identity, slug, path, owner, edition disposition, and occurrence are resolved; its owner and leaf audits are complete; all authorized branches and textual units are accounted for; its claims and relationships are classified; its passage-by-passage matrix documents bounded searches of the major relevant Greek and Latin patristic and later saintly corpora, checked loci, witness roles, and negative results; its detailed commentary proves breadth and depth for every appointed passage; its notable-and-quotable section has three to five source- and locus-identified, non-obvious cultural, humorous, ironic, idiomatic, literary, political, institutional, visual, scientific, commercial, or comparable reuses of wording from the scriptural propers, with every verbal relation, contextual turn, branch, right, payoff, limit, and material negative result audited and no patristic excerpt or bare title, motto, artwork, or musical setting used as padding; its interpretive section contains four to six non-recapitulatory, multi-element proposals and its research scope records each proposal's anchors, mechanism, targeted precedent result, fruit, and strongest limit without claiming universal novelty; page 2 contains only the complete one-page date/location sheet, pages 3--4 contain the thematic movement, detailed commentary begins on page 5, and every later boundary conforms; work-wide qualifications appear only in the terminal scope appendix; rights and source records conform; every shared dependency is explicit and rebuilt; and build, metadata, log, and visual checks pass.

Do not call an edition-locale collection complete until every stable-registry target has a sourced disposition, all edition splits and conditional targets are evaluated, all weekday fallbacks are evaluated, and the replacement and local-overlay matrix is resolved. Absence in one civil year is an occurrence result, not a target disposition.

Exact-snapshot release approval authorizes only the named installed PDF hash. It does not make a guide profile-final, certify missing collation or review, or authorize a changed build. Keep any accepted limitation in the terminal scope appendix, catalog, and tracked records.

The structural schema is grounded in the Holy See's [General Instruction of the Roman Missal](https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20030317_ordinamento-messale_en.html), the approved [General Introduction to the Lectionary](https://www.liturgyoffice.org.uk/Resources/GIRM/Documents/Lectionary.pdf), the official [Roman Missal, Third Edition contents](https://www.liturgyoffice.org.uk/Missal/Information/RM3-contents.pdf), the bishops' [Missal Antiphonary](https://www.liturgyoffice.org.uk/Missal/Music/Antiphonary.pdf), official matrices for special forms, and the approved initiation rite. Exact editions, later decrees, territorial adaptations, and the competent calendar control each leaf.
