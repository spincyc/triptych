# Expositions of the Ordinary and Order of Mass

This profile governs expositions of the stable texts and ritual sequence of Mass in the 1962 and postconciliar Roman Missals. It does **not** inherit the 1962 weekly proper-guide template. An ordinary exposition is organized by the identified Order of Mass and its theological or ritual questions, not by a Sunday formulary, a ten-proper inventory, or the weekly guide's fixed pages and headings.

Under the present provider, edition-specific documents live beneath `src/gpt/liturgy/roman-rite/1962/ordinary/` or `src/gpt/liturgy/roman-rite/postconciliar/<edition-locale>/ordinary/`; cross-edition works live beneath `src/gpt/liturgy/roman-rite/comparative/`. Another provider preserves that taxonomy beneath its own provider directory.

## Define the object of study

Use `Ordinary` precisely. At the start of every project, state whether it treats:

- the sung Ordinary: Kyrie, Gloria, Credo, Sanctus, and Agnus Dei;
- the broader stable spoken and sung texts of Mass;
- the complete Order of Mass, including rubrics, gestures, roles, and variable choices; or
- a particular unit such as the Offertory, Eucharistic Prayer or Canon, Communion rite, or dismissal.

Stable does not mean invariant. Seasonal omissions, multiple forms, ritual-Mass adjustments, celebrant and assembly parts, music, and rubrical conditions may change what is used. Distinguish the stable framework from the proper of the day, options within the Order, and exceptional ritual additions.

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

Keep an edition manifest and a sequence inventory beside the source. For each unit record:

- its exact title or incipit and stable locator;
- the speaker or minister, addressee, posture or action, and audible or musical mode when the edition specifies them;
- whether it is fixed, conditionally omitted, one option among several, or locally determined;
- its principal scriptural, historical, doctrinal, and ritual questions;
- textual or rubrical differences relevant to the argument; and
- the primary and secondary sources actually used.

The document leaf also keeps the universal structured `generation-metadata.tex` record and imports it once at the placement selected for the exposition; it does not copy a proper guide's terminal-section convention unless that placement suits the work.

Choose the published architecture to suit the scope: sequential commentary, thematic exposition, synoptic comparison, or a narrowly focused essay may each be appropriate. Comparisons should align genuinely corresponding moments and also identify additions, omissions, relocations, and changed functions; visual symmetry must not imply theological or historical equivalence.

## Completion gate

An ordinary exposition is ready to publish only when:

- its meaning of `Ordinary` and its textual boundaries are explicit;
- every text and rubric is traceable to a named edition, language, and territory;
- stable texts, propers, options, customs, and exceptional ritual material remain distinct;
- cross-edition claims are based on direct comparison rather than memory or inherited labels;
- theological authority and editorial synthesis are clearly classified; and
- copyright, research-record, build, and generation-metadata requirements are satisfied.
