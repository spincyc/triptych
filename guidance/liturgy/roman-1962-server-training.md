# 1962 Roman Rite Altar-Server Training Guides

This profile governs the coordinated, print-first altar-server guides for the
1962 Roman Rite: a Low Mass response trainer, a Missa Cantata ceremonial guide,
a Solemn Mass ceremonial guide, and one cards-only print companion for each
full guide. The intended learner is eight to fourteen years old. The series
teaches received Latin responses,
pronunciation, memorization, and, in the two sung-form guides, the complete
actions of a declared model server roster.

The series belongs under
`src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/`. Its owner root
is non-publishable; its six independently printable leaves mirror under
`build/gpt/` and `doc/gpt/`. Universal evidence, rights, metadata, review, and
publication rules remain in `guidance/editorial.md`; ownership, paths, shared
dependencies, catalogs, and installation remain governed by
`guidance/repository.md`.

These guides are training aids. They are not liturgical books, parish
directives, certificates of competence, or evidence of present authorization
to celebrate or serve according to the 1962 books.

## Governing priorities

1. Reproduce the selected 1962 text, sequence, speaker, and ceremonial form
   before simplifying its presentation for a young learner.
2. Teach an observable skill in short, cumulative units: hear or identify the
   cue, give the right response, pronounce it intelligibly, and, where in
   scope, perform the assigned action.
3. Distinguish what a server says from what the celebrant, sacred ministers,
   schola or choir, and people say or sing.
4. Make each sung-form walkthrough complete for its declared model roster
   without presenting that roster as the only lawful or customary arrangement.
5. Give shared Latin, pronunciation, meaning, and flash-card content one owner
   and derive every rendering from that source.
6. Keep a 1962 prescription, permitted option, ceremonial-manual convention,
   sourced local custom, and unresolved practice visibly distinct at the point
   where the learner must act.

## Series identity and form boundaries

The owner contains shared render sources and series-wide research. The three
canonical full guides and their three print companions are:

```text
altar-server-guides/
  shared/
  research/
  01-low-mass/
  01-low-mass-cue-cards/
  02-missa-cantata/
  02-missa-cantata-cue-cards/
  03-solemn-mass/
  03-solemn-mass-cue-cards/
```

Each leaf has its own `main.tex`, `generation-metadata.tex`, and local guide
map. The three full guides are substantive publications and keep independent
generation metadata. A cards-only leaf is a card-face-only mechanical
companion and may inherit generation provenance only from its matching full
guide while displaying its own revision timestamp once.

The boundaries are strict:

- **Low Mass** is a verbal response and pronunciation trainer. It gives the
  celebrant's verbal cue and the server's reply in Mass order, but contains no
  directions for posture, gestures, movement, position, bells, books, vessels,
  vesture, or other ceremonial acts. A short ritual label may locate a verbal
  cue, but it must not become an action instruction.
- **Missa Cantata** means a non-Solemn sung Mass with one celebrant, a schola or
  choir, and the exact server roster declared by the guide. It accounts for
  every response and every ceremonial action of that roster, including any
  selected incense branch, while never assigning the functions of deacon or
  subdeacon to a server.
- **Solemn Mass** means a non-pontifical Solemn Mass with celebrant, deacon,
  subdeacon, schola or choir, and the exact server roster declared by the
  guide. It accounts for every server action and the sacred ministers' actions
  only to the extent needed as cues, coordination points, or handoffs.

Do not use the ambiguous label “High Mass” as the formal identity of either
sung guide. Do not collapse Missa Cantata into Solemn Mass or infer that a
practice proper to one belongs to the other.

“Complete” means that, from the roster's stated starting station before the
entrance through its stated end after the recessional, every listed server has
an accounted-for response, posture, gesture, movement, object, handoff, and
waiting state at every applicable stage. It does not mean that the guide covers
every roster, parish custom, optional solemnity, or adjacent ceremony ever
used.

## Controlling object, horizon, and exclusions

The controlling liturgical object is the Order of Mass and rubrical system of
the identified 1962 typical edition of the *Missale Romanum*. Record the exact
witnesses used for the *Ordo Missae*, *Ritus servandus*, General Rubrics, and
the 1960 rubrical code incorporated into that edition. Identify every official
instruction, decree, ceremonial book, chant book, or particular directive used
to establish a form, response, role, or option.

The core model is an ordinary, non-pontifical celebration under the 1962 books.
Requiem Masses, Holy Week, ritual Masses, the nuptial ceremony, Mass before the
Blessed Sacrament exposed, pontifical functions, the Asperges, processions,
Benediction, Communion outside Mass, and prayers or devotions before or after
Mass are excluded unless a separately titled and sourced appendix deliberately
adds one of them. An appendix must state exactly which core steps it replaces,
omits, or supplements; proximity to Mass does not make an adjacent rite part of
the Order.

Do not import pre-1962 or post-1962 text or ceremonial as the 1962 norm. In
particular, do not insert a second *Confiteor* before Communion merely because a
manual, local practice, or older customary sequence contains it. Do not count
the Leonine prayers as part of Mass. Dialogue-Mass participation by the people,
chant-degree choices, vernacular permissions, and current permissions to use
the 1962 books are separate questions and enter only when deliberately sourced,
dated, and labeled.

The guide must not imply that the ordinary rubrics determine a local sacristy
layout, number of steps, sanctuary dimensions, traffic pattern, or customary
assignment that they do not in fact determine.

## Source hierarchy and ceremonial claims

Apply the following hierarchy without treating every source as if it had the
same authority:

1. A checked page-image witness of the identified 1962 *Missale Romanum*
   controls the received Mass text, printed sequence, and the rubrics it
   contains.
2. Official acts and liturgical books in force at the chosen 1962 horizon
   control the matters they actually regulate, including distinctions among
   Low, sung, and Solemn execution and among spoken and sung roles.
3. Applicable particular law or an identified competent local directive
   controls only its own jurisdiction, place, community, and date.
4. Named, edition-appropriate ceremonial manuals may resolve or document
   practical details left unstated by higher sources. Record the manual's
   edition and scope; a manual convention is not silently promoted into a
   universal rubric.
5. Historical scholarship and later training materials may explain or compare
   practice but do not control the 1962 action. A current community's sheet or
   video can document its local custom only when that is the stated purpose.
6. OCR, searchable transcriptions, aggregations, and unattributed server cards
   are finding aids until checked against their underlying witness.

Where official sources are silent and reliable manuals disagree, preserve the
disagreement, choose and name one model for the teaching sequence, and mark the
alternative. Do not create a hybrid route by silently selecting the easiest
detail from several manuals. Source a local custom from an actual local or
community authority; frequency, memory, or online repetition does not establish
its status.

Pronunciation has its own evidence trail. Name the ecclesiastical Latin
pronunciation standard taught, the sources used to establish it, and the
territorial or historical bounds of those sources. Do not describe a common
Italianate realization, a chant realization, or a house accent as the only
possible ecclesiastical pronunciation unless the evidence establishes that
claim.

## Shared response and learning-data contract

The series owner keeps one render-capable source for each reusable datum. At a
minimum, every response entry has a stable ID and records:

- its Mass-order location and condition;
- the cue, cue speaker, response, and response speaker;
- exact source Latin and locus;
- any displayed normalization, syllable division, and stress;
- phonemic or phonetic IPA, identified as such;
- the young-server-readable respelling and the rule set behind it;
- a concise meaning or gloss and its authorship or witness status; and
- form, role, spoken-or-sung mode, omission, option, and local-custom status.

Keep the facsimile-checked Latin distinct from pedagogically marked Latin.
Adding stress, expanding a ligature, changing *i/j*, dividing syllables, or
altering punctuation is a declared normalization, not a silent correction of
the Missal. IPA, respelling, memory cues, and project-written meanings are
editorial teaching layers and may not be presented as received liturgical text.
A short project gloss must be labeled as meaning and must not function as an
English ritual response; a full English ritual rendering requires an exact
identified human witness and recorded rights status.

The sequence lesson, quick reference, exercises, answer material, and response
flash cards must consume the same authoritative data. Do not maintain a second
editable copy for a card back or another guide. Give shared ceremonial actions
one owner as well when the action is genuinely identical across the two sung
forms. Declare every cross-leaf render dependency so a shared change rebuilds
all affected consumers.

## Voice, pronunciation, and memorization

Every verbal item in the teaching bank and Mass-order map identifies its actor
and mode. At minimum distinguish celebrant, deacon, subdeacon, server or
servers, schola or choir, and people; distinguish spoken, chanted, and silent
text. A printed `R.` is not by itself evidence that an altar server says the
response in all three forms. When the choir sings an item while servers perform
an action, print those as different tracks. When a sacred minister answers, do
not reassign the reply to a server. A paired full guide may state the form's
actor and mode rule once in its card key instead of repeating a `Voice` field
on every face in the cards-only companion; any condition that changes whether
the card is used still appears on the affected card.

Give a compact pronunciation key before first use, then keep every local entry
consistent with it. Syllable breaks and primary stress must agree with the
recorded rule; IPA must use one declared transcription convention; and the
English-like respelling must map consistently to that IPA without claiming
technical authority. Mark consequential elision, assimilation, doubled
consonants, or alternative realizations rather than hiding them. Keep speech
training distinct from chant rhythm and melody unless a checked chant source is
expressly in scope.

Teach responses in short ordered groups, moving from recognition to cued recall
and then delayed, cumulative recall. Each unit gives the learner a checkable
target, an immediate correction method, and a next decision. Use meaning and
word-pattern associations to support memory without inventing an etymology,
doctrinal symbolism, or historical origin. Page completion and confidence are
not mastery evidence.

The final assessment for a response set requires the learner to answer an
unseen or shuffled cue accurately, without reading the reply, and to recover
after a missed cue. Pronunciation assessment records the declared tolerances and
requires a competent human listener; IPA or respelling alone cannot certify
oral performance. The sung-form assessments additionally test the learner's
role through a complete rehearsal or cue sequence, including branch recognition
and safe object handoffs.

## Ceremonial model, roles, and branches

Each sung guide declares one complete model roster before its walkthrough. For
every role state whether it is part of the core model, an optional added role,
or a role whose work is reassigned when absent. Never let an object or action
silently disappear when an optional role is removed.

Every action in the chronological inventory records a stable action ID, Mass
stage, acting role, cue, starting and ending place, posture or gesture, carried
object, interaction or handoff, next state, applicable branch, source class,
and exact source locus. Cover standing, sitting, kneeling, bows, genuflections,
signs of the Cross, breast strikes, turns, formations, processions, bells,
books, candles, cruets, lavabo articles, communion plate, incense, boat, torches,
and every other act actually assigned to the model roster. Omit a listed object
or gesture only when the selected branch omits it, and say so there.

The publication presents both a chronological walkthrough and compact
role-by-role rehearsal sheets derived from the same inventory. Check that no
server is required in two places at once, no handoff lacks a giver or receiver,
no carried object appears without preparation or disposition, and no role sheet
contradicts the chronological route. Clergy and choir actions appear only as
needed cues and must remain visibly distinct from server instructions.

At the affected step, label each non-core route as one of: prescribed condition,
permitted option, manual convention, sourced local custom, or unresolved
practice. State the default used by the model and show the alternate route only
far enough to rejoin it safely. “Ask the priest or master of ceremonies” may be
a prudent local direction, but it does not replace documenting the branch that
made consultation necessary.

## Flash-card contract

Each full guide has a parallel cards-only companion generated from the same
shared data. The full guide owns the printing, actor and form, branch, and
safety key and points to its paired catalog companion; it does not reproduce
or embed card faces. The Low Mass companion contains integrated verbal-response
cards only. The Missa Cantata and Solemn Mass companions contain the same
applicable integrated response cards followed by their form- and role-specific
action cards.

Use one physical response card for each stable response or deliberately split
study chunk. Do not maintain separate cue-to-response and
Latin-to-pronunciation physical decks. The front gives the complete spoken cue
or complete verse used for practice. An isolated last word or ellipsis is not
a complete cue. When an appointed reading varies, print a complete,
facsimile-checked example ending on the face and identify it as an example,
not the universal proper text. The trainer may additionally practise the
complete ending from the identified Missal for the actual day. The back gives
the canonical answer, learner syllables and stress, the consistent sound line,
a concise meaning, the response or chunk ID, and any condition needed to
prevent a false response. These are renderings of the received Latin and
audited editorial learning layers; consolidation does not transfer their
ownership to the card layout.

Each physical card has a stable response/chunk or action ID. Its front and back
are generated as one audited pair from the shared data, and the flash-card
manifest identifies the companion that selects it. Put the rendered ID at
upper left and `Cue` or `Answer` at upper right; do not add the generic word
`Card`, a repeated recall slogan, or a repeated `Voice` field. Add a compact
form marker to the rendered ID so cut cards from Low Mass, Missa Cantata, and
Solemn Mass cannot be silently mixed while the underlying stable ID remains
unchanged. Order response cards by the six lesson groups, not numerically. The
full guide's card key preserves the speaker and form distinction so a choir or
sacred-minister text is not turned into an automatic lay-server response.
Action cards identify the role, form, cue, branch, and next action; they do not
compress two incompatible local routes into one answer.

State paper size, actual-size setting, duplex edge, page orientation, cutting
order, and whether blank backs are intentional in the full guide's card key.
Keep text and cut marks within safe margins. Verify front/back order and
alignment by measured overlay or an equivalent rendered check, then inspect
both faces at full size. A contact sheet alone cannot establish duplex
alignment or small-type legibility.

The standard trainer-print layout is six portrait cards on each letter-size
face, in two columns by three rows, with the backs mirrored by row for
long-edge duplex printing. A companion may depart from six-up only when a
recorded legibility or cut-safety check shows that the actual card text cannot
fit at the profile's minimum readable size. Prefer splitting a genuinely long
response into stable sense chunks over shrinking the teaching text.

The cards-only leaf is a print companion, not a self-contained trainer. It
reproduces only the complete selected card faces: no cover, contents,
instruction, actor key, lessons, parity leaf, or terminal reference apparatus.
Its catalog link and the full guide's catalog pointer must tell the reader to
use the matching full guide's card key. The required revision and rights notice may
occupy the unused margin below the final back grid but must not add a page or
enter a cut card. Every condition needed to prevent a false individual
response or action remains on the affected face.

The companion begins with the first integrated-response front on odd physical
PDF page 1, and its mirrored back follows on even page 2. Each later sheet
front likewise falls on an odd page. In a sung-form companion, the action deck
begins on the next odd page after the complete even-length response run. Do not
add a cover, instruction, or parity leaf before the card faces. Verify physical
PDF parity after the final build; logical page numbering alone is not
sufficient. The full guide has no embedded card range to advertise.

## Required records and ownership

The non-publishable series owner keeps:

- `research/scope.md`: reader, three form boundaries, model horizon, language,
  pronunciation standard, jurisdiction, inclusions, exclusions, pedagogical
  progression, current-authorization boundary, rights, and review state;
- `research/edition-manifest.md`: exact Missal, rubrical code, official acts,
  ceremonial and chant books, pronunciation authorities, particular
  directives, manuals, and non-controlling aids actually used, with edition,
  locus, source role, access or collation state, and rights status;
- `research/response-inventory.md`: every cue and reply, stable ID, sequence,
  speaker, mode, condition, form, exact locus, checked Latin, normalization,
  meaning status, and rendered uses;
- `research/pronunciation-audit.md`: syllabification, stress, IPA, respelling,
  governing rule or checked lexical decision, variants, completed oral or
  specialist checks, and unresolved items;
- `research/ceremonial-inventory.md`: the two model rosters and every action ID,
  route, handoff, source class, locus, option, custom, reassignment, and
  unresolved discrepancy;
- `research/flash-card-manifest.md`: every card ID, front/back data source,
  companion selection, ordering, duplex pairing, and either the completed
  alignment check or an explicit pre-build status;
- `research/source-audit.md`: facsimile checks, official-source and manual
  comparisons, consequential negative results, rejected edition mixing,
  rights, and completed liturgical, Latin, pedagogical, and production review;
  and
- `research/production-manifest.md`: the exact six reviewed builds, page and
  card counts, log and PDF checks, every-page review, duplex verification,
  installed identity, and outstanding release state.

Each publishable leaf keeps `research/guide-map.md`, naming its form, stable
guide identity, imported data selections, model roster where applicable,
reader order, lessons, drills, assessments, paired-guide or card-face boundary,
branches, appendices, and relationship to the series-wide records. It must
account for everything rendered without copying the controlling inventories.

## Reader order and terminal apparatus

After a compact title and contents, every full guide begins with a one-page
trainer start sheet. It tells the trainer which publication to print, what the
server should learn first, how to run a short practice, and where an assigned
role or lesson begins. Labels such as “For the Trainer,” “For the Server,” and
“MC / Trainer Reference” keep instructions, learner text, and technical audit
material visibly distinct. The main learning route must not require a trainer or server
to decode an inventory table before beginning practice.

The Low Mass guide begins with the compact pronunciation key and teaches the
responses in short, easy-to-hard lessons. It then consolidates those learned
answers in Mass order, followed by cumulative drills, mastery, quick reference,
and a linked cards-only companion. The lesson order may differ from Mass order
when that reduces the server's first memory burden, provided the later
Mass-order route is complete and derived from the same response data. It does
not acquire ceremonial material through an introduction, diagram, quiz, or
card.

Each sung guide begins with its model roster, today's local-route choices, and
a short scene map. Standalone role-by-role learner sheets come before the full
chronological inventory so a server can first find and rehearse one assigned
job. The complete chronological walkthrough follows as MC/trainer reference, then
cumulative rehearsal and mastery checks, verbal-response practice, quick
reference, and a linked cards-only companion. Role sheets and the chronology
remain derived from the same inventory; reader order does not change
evidentiary priority. Put optional and local branches beside the affected
action rather than in an unconnected miscellany.

Each full guide ends with `Scope, Edition, and Qualifications`, references, and
`Generation Metadata` as the final content block. The terminal appendix owns
the form boundary, edition, model roster status, excluded ceremonies,
pronunciation convention, current-authorization boundary, global custom and
manual limits, rights, and review state. A condition that changes what a server
says or does remains local as well.

Each cards-only companion follows the source selection and form boundary of its
matching full guide, begins directly with the first integrated-response front
on physical page 1, and contains no independent teaching prose. Its local guide
map records the planned duplex order, final verified physical page map, and
inherited relationship.

The six installed PDFs have one catalog home in
`library/traditional-latin-mass.md` and remain together in three form rows.
Each form row gives separate, clearly labeled links for the full training guide
and its cards-only companion. Build, installation, cataloging, exact-snapshot
release authorization, public push, and deployment are separate operations.

## Profile gate

Before installation or release, in addition to the universal gates:

- reconcile every rendered verbal item and card with the response inventory
  and visually collate its received Latin against the identified page image;
- prove that the Low Mass source, contents, extracted text, and cards contain no
  gesture or ceremonial instruction;
- reconcile every Missa Cantata and Solemn action in both chronological and
  role views with the ceremonial inventory, including all roster states,
  objects, handoffs, omissions, and branch rejoins;
- verify that server, sacred-minister, choir, and people texts are never
  reassigned or conflated and that every spoken-or-sung label agrees with the
  selected form;
- check every syllable division, stress, IPA transcription, respelling, and
  meaning against its audit row, and inspect IPA glyph rendering and text
  extraction;
- check every exercise, assessment, answer, and card pair for a unique stable
  ID and agreement with its authoritative source;
- build and inspect all six consumers after any shared render-source change;
  reject unresolved log warnings, overfull or underfull boxes, broken links,
  missing fonts, or unstable contents;
- inspect every page for age-appropriate type size, density, navigation,
  monochrome legibility, writable space, split action units, unsafe diagram
  ambiguity, clipping, accidental blanks, and final-colophon fit;
- inspect flash-card faces at full size and verify that the first integrated
  response front and each later sheet front are on odd physical PDF pages,
  then verify duplex edge, front/back alignment, cut safety, lesson-group
  order, form markers, and the absence of an inserted cover or parity page; and
- state liturgical, ceremonial, Latin-pronunciation, pedagogical, rights, and
  independent-review status accurately. Received Latin and other third-party
  material require a local rights statement and recorded distribution basis;
  technical completion or installation does not clear a release gate or grant
  ecclesiastical approval.
