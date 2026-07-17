# Expositions of the Ordinary and Order of Mass

This profile governs expositions of the stable texts and ritual sequence of Mass in the 1962 and postconciliar Roman Missals. It does **not** inherit the 1962 weekly proper-guide template. An ordinary exposition is organized by the identified Order of Mass and its theological or ritual questions, not by a Sunday formulary, a ten-proper inventory, or the weekly guide's fixed pages and headings.

Under the present provider, edition-specific documents live beneath `src/gpt/liturgy/roman-rite/1962/ordinary/` or `src/gpt/liturgy/roman-rite/postconciliar/<edition-locale>/ordinary/`; cross-edition works live beneath `src/gpt/liturgy/roman-rite/comparative/`. Another provider preserves that taxonomy beneath its own provider directory.

An edition-specific exposition that functions as the stable reading preface before that edition's variable propers may use `O00` as an assembly-ordering key. In a technical table that orders the stable framework with the edition's variable propers, list `O00` before the temporal entries. This does not control reader-facing navigation or library-section ownership, which groups works by subject and use. The key does not make the Ordinary a temporal proper, change the exposition's source hierarchy or governing profile, or become part of the work's title.

## Define the object of study

Use `Ordinary` precisely. Before research, record whether the work treats:

- the sung Ordinary: Kyrie, Gloria, Credo, Sanctus, and Agnus Dei;
- the broader stable spoken and sung texts of Mass;
- the complete Order of Mass, including rubrics, gestures, roles, and variable choices; or
- a particular unit such as the Offertory, Eucharistic Prayer or Canon, Communion rite, or dismissal.

Stable does not mean invariant. Seasonal omissions, multiple forms, ritual-Mass adjustments, celebrant and assembly parts, music, and rubrical conditions may change what is used. Distinguish the stable framework from the proper of the day, options within the Order, and exceptional ritual additions.

In the publication, a compact title or identity line may name the exact Order, Missal, language, and territory because those facts identify the received object. The full textual boundary, option range, and terminology explanation belong in the terminal scope appendix rather than an opening object-and-method chapter.

## Identify editions without conflation

Every exposition names the Missal, edition, language, territory, and relevant companion books it uses. At minimum:

- a 1962 study identifies the edition of the *Missale Romanum*, its Order of Mass and rubrics, and any separate chant or ceremonial source;
- a postconciliar study identifies the Latin typical edition, the approved vernacular edition and territory when quoted, and the applicable General Instruction and companion books; and
- a comparative study gives each witness its own source trail and labels the edition governing every quotation, rubric, and translation.

Do not create a generic `traditional Mass` or `Novus Ordo` composite from several editions. Do not silently transfer vocabulary, ministerial roles, rubrical rules, translations, or pastoral options from one edition to another. Current disciplinary permissions concerning an edition are a separate canonical question from the textual and theological exposition; source and date any such claim.

## Separate ordinary, proper, and commentary

Maintain three visible layers:

1. **Received text and rite:** the exact edition-specific wording, sequence, speaker, action, and rubrical condition.
2. **Authoritative interpretation:** Scripture, liturgical books, magisterial teaching, and identified historical or theological witnesses.
3. **Editorial synthesis:** the project's proposed connections, comparisons, and implications.

When a proper supplies the context needed to explain a stable text, cite it as a proper and identify the celebration; do not absorb it into the Ordinary. Conversely, repetition across most Masses does not turn an option or locally customary practice into a universal stable text.

## Recommended working record

Keep an edition manifest, a sequence inventory, a research scope, and a source audit beside the source. For each received movement or inventory row record:

- its exact title or incipit and stable locator;
- the speaker or minister, addressee, posture or action, and audible or musical mode when the edition specifies them;
- whether it is fixed, conditionally omitted, one option among several, or locally determined;
- its principal scriptural, historical, doctrinal, and ritual questions;
- textual or rubrical differences relevant to the argument; and
- the primary and secondary sources actually used.

When a publication adopts a numbered analytical scheme not promulgated by its controlling liturgical book, identify the scheme as editorial, document any historical or catechetical antecedent actually used, and provide a reproducible mapping back to the edition. A devotional numerical correspondence may be analyzed as reception, but it must not be turned into an official taxonomy, an original compositional intention, or a claim on faith.

Sequential expositions analyze each movement at four levels: its literal ritual function; its scriptural, doctrinal, and patristic illumination; its historically supportable stratum or development; and its relation within the whole action. These are research and coverage requirements, not a reader-facing paragraph template or a requirement that every movement receive material from every source class. Do not print the same dossier headings, paragraph count, or analytical sequence for every movement and then repeat the dossier in prose. Let the received form determine the exposition: read a psalm in its literary voice and canonical setting, a hymn or creed through its own rhetoric and doctrinal progression, an oration through its address and petition, a dialogue through its speakers and assent, a procession or gesture through its spatial and ministerial action, and a consecratory or Communion passage through its distinctive sacramental grammar. A short transition, a variable proper slot, and the Canon do not require equal space or the same method merely because each appears in an inventory.

The published architecture must therefore make each movement's governing question and internal logic perceptible while keeping source classification auditable in the research record. Use the received liturgical name, standard ritual designation, or exact incipit as the primary heading for a part of the Ordinary; place an editorial or interpretive title beneath it as a subordinate heading rather than allowing the synthesis to displace the part's identity. A compact repeated header may identify received boundary, status, and Missal locus; it must not substitute for interpretation or force unlike acts into visual symmetry. Use historical detail where it changes how the received act is understood, not as a fixed quota, and keep narrow manuscript disputes in the research apparatus when they would bury the movement's theological or ritual center. Do not assign equal theological weight merely because units are equally numbered. Finish with a synthesis that returns the inventory to the unity of Word, sacrifice, sacramental presence, Communion, ecclesial participation, and mission.

A passage-level sequential exposition also gives every movement a reproducible research dossier, whether as one row or as several claim-level entries in the apparatus. Identify the received Latin or vernacular boundary by text or incipit. Do not compose or translate prayer or ritual formulas. Reproduce English prayer or ritual wording only from an exact, identified historical or approved human witness whose edition and rights status are recorded; otherwise give only a visibly third-person analytical statement of ritual function that neither closely renders the received clauses nor serves as recitation wording. Read each principal biblical locus in its own literary and canonical context, and state whether the liturgical use is direct, typological, accommodative, or allusive. Historical treatment distinguishes the earliest secure witness, a probable range, a later terminus ante quem, and retrospective attribution. Name a composer, pope, council, or other agent only when a checked source supports that role; otherwise state that no individual author is securely known. Keep the evidence matrix in the research record so broad narrative history does not substitute for passage-specific support; it need not appear as a visible dossier in the publication.

Prayers or ceremonies historically attached before or after Mass may be treated when they materially illuminate the edition, but they remain outside the received Order unless the controlling liturgical book places them within it. Give the external prescription, scope, exceptions, effective dates, and suppression history from juridically competent sources. Devotional proximity does not make an attached prayer part of the Mass, and a popular origin legend does not become history through repetition.

The document leaf also keeps the universal structured `generation-metadata.tex` record and imports it once in a terminal `Generation Metadata` section. No expository prose follows it.

Choose the published architecture to suit the scope: sequential commentary, thematic exposition, synoptic comparison, or a narrowly focused essay may each be appropriate. Comparisons should align genuinely corresponding moments and also identify additions, omissions, relocations, and changed functions; visual symmetry must not imply theological or historical equivalence.

## Reader-facing order

After the title and table of contents, begin the received movement, governing theological question, or synoptic comparison immediately. A compact sequence map may come first when it is itself a usable guide to the rite and fits without becoming another method chapter. Do not make the reader pass through a definition of `Ordinary`, source taxonomy, edition manifest, evidence key, numbering history, global ritual history, current-law survey, or review disclaimer before the exposition.

Integrate historical evidence where it changes how a movement is understood. Put a global development survey, orientation timeline, edition concordance, editorial-numbering provenance, and the law and history of adjacent pre- or post-Mass prayers in appendices unless one of them is the work's governing substantive question. The terminal apparatus contains:

1. `Scope, Edition, and Qualifications`: received boundary, edition, language, territory, options, included and excluded material, terminology, method and source classes, currentness, rights, limitations, and review state;
2. any sequence concordance, global historical timeline, numbering audit, or adjacent-prayer legal history needed by the work;
3. references; and
4. terminal `Generation Metadata`.

An exact rubric, option dependency, disputed historical attribution, cross-edition difference, or authority qualification remains beside the movement it governs. A compact immediate non-authority or present-authorization warning may remain where delaying it would create reliance risk, but it points to the appendix and is not repeated.

## Completion gate

An ordinary exposition is ready to publish only when:

- its meaning of `Ordinary` and its textual boundaries are explicit;
- its exposition begins immediately after the title and contents, while the full object definition, edition manifest, method, evidence key, global history, date range, numbering provenance, currentness, and review qualifications occur only in the terminal appendix block;
- any editorial numbering has a documented provenance, a complete edition-mapped inventory, and a non-official status statement;
- each movement receives literal, theological, historical, and whole-order analysis proportionate to its significance, with a source class used only when it actually illuminates that movement;
- reader-facing headings identify the received parts by their liturgical names, standard ritual designations, or incipits, while editorial interpretation remains visibly subordinate;
- the publication gives unlike textual and ritual genres genuinely different exegesis instead of repeating a universal dossier or paragraph template, while the research record preserves reproducible coverage;
- a passage-level study gives every movement its received textual boundary, relevant Scripture in context, calibrated historical witness or terminus, and explicit relation to the whole action in its research record, without requiring those controls to become repeated published headings;
- any English prayer or ritual wording is traceable to an exact, identified historical or approved human witness, while project-authored prose remains analysis rather than a translation or recitation substitute;
- every text and rubric is traceable to a named edition, language, and territory;
- stable texts, propers, options, customs, and exceptional ritual material remain distinct;
- adjacent pre- or post-Mass prayers are neither absorbed into the Order nor narrated from unsupported origin legends;
- cross-edition claims are based on direct comparison rather than memory or inherited labels;
- theological authority and editorial synthesis are clearly classified; and
- copyright, research-record, build, and terminal generation-metadata requirements are satisfied.
