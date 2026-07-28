# 1962 Roman Rite Altar-Server Training Guides

This profile governs the coordinated, print-first altar-server guides for the
1962 Roman Rite: a Low Mass child booklet, its page-matched trainer manual, and
its flash-card print companion; a Missa Cantata ceremonial guide and
cards-only print companion; and a Solemn Mass ceremonial guide and cards-only
print companion. The Low Mass learner is approximately eight to ten years old;
the sung-form learner is eight to fourteen. The series teaches received Latin
responses, pronunciation, memorization, and the complete actions of a declared
model server roster where ceremonial training is in scope.

The series belongs under
`src/<provider>/liturgy/roman-rite/1962/reference/altar-server-guides/`. Its
owner root is non-publishable; its seven independently printable leaves mirror
under `build/<provider>/` and `doc/<provider>/`. Universal evidence, rights, metadata, review, and
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
4. Make the Low Mass walkthrough and each sung-form walkthrough complete for
   its declared model roster without presenting that roster as the only lawful
   or customary arrangement.
5. Give shared Latin, pronunciation, meaning, and flash-card content one owner
   and derive every rendering from that source.
6. Keep a 1962 prescription, permitted option, ceremonial-manual convention,
   sourced local custom, and unresolved practice visibly distinct at the point
   where the learner must act.

## Series identity and form boundaries

The owner contains shared render sources and series-wide research. The Low
Mass three-publication set and the two sung-form publication pairs are:

```text
altar-server-guides/
  shared/
  research/
  01-low-mass/
  01-low-mass-trainer-manual/
  01-low-mass-flash-cards/
  02-missa-cantata/
  02-missa-cantata-cue-cards/
  03-solemn-mass/
  03-solemn-mass-cue-cards/
```

Each leaf has its own `main.tex`, `generation-metadata.tex`, and local guide
map. The Low Mass child booklet and trainer manual and the two sung-form full
guides are substantive publications and keep independent generation metadata.
A cards-only leaf is a card-face-only mechanical companion and may inherit
generation provenance only from the teaching publication named in its guide
map while displaying its own revision timestamp once.

The boundaries are strict:

- **Low Mass** means an ordinary Low Mass with the exact two-server model
  declared by the child booklet and trainer manual. The page-matched pair
  teaches the verbal responses, pronunciation, positions, movements, objects,
  and actions of that roster in continuous Mass order. Its diagrams and
  step-level labels are a declared teaching model, not a claim that the
  ordinary rubrics determine every sanctuary layout or customary assignment.
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

For a form's ceremonial route, “complete” means that, from the roster's stated
starting station before the entrance through its stated end after the
recessional, every listed server has an accounted-for response, posture,
gesture, movement, object, handoff, and waiting state at every applicable
stage. It does not mean that the guide covers every roster, parish custom,
optional solemnity, or adjacent ceremony ever used.

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

Every rendered sequence lesson, quick reference, exercise, answer item, and
response flash card must consume the same authoritative data. Do not maintain a
second editable copy for a card back or another guide. Give the page-matched
Low Mass main lane one owner, and give shared ceremonial actions one owner when
the action is genuinely identical across publications. Declare every
cross-leaf render dependency so a shared change rebuilds all affected
consumers.

## Voice, pronunciation, and memorization

Every verbal item in the teaching bank and Mass-order map identifies its actor
and mode. At minimum distinguish celebrant, deacon, subdeacon, server or
servers, schola or choir, and people; distinguish spoken, chanted, and silent
text. A printed `R.` is not by itself evidence that an altar server says the
response in all three forms. When the choir sings an item while servers perform
an action, print those as different tracks. When a sacred minister answers, do
not reassign the reply to a server. The publication named as a companion's card
key may state the form's actor and mode rule once instead of repeating a
`Voice` field on every face in the cards-only companion; any condition that
changes whether the card is used still appears on the affected card.

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

Where a printed final assessment is in scope, it requires the learner to answer
an unseen or shuffled cue accurately, without reading the reply, and to recover
after a missed cue. Pronunciation assessment records the declared tolerances
and requires a competent human listener; IPA or respelling alone cannot
certify oral performance. The Low Mass pair contains no quiz, written
exercise, or mastery record; its trainer instead conducts brief oral recall
and whole-route rehearsal. The sung-form assessments additionally test the
learner's role through a complete rehearsal or cue sequence, including branch
recognition and safe object handoffs.

## Ceremonial model, roles, and branches

The Low Mass pair declares one complete two-server model, and each sung guide
declares one complete model roster before its walkthrough. For every role state
whether it is part of the core model, an optional added role, or a role whose
work is reassigned when absent. Never let an object or action silently
disappear when an optional role is removed.

Every action in the chronological inventory records a stable action ID, Mass
stage, acting role, cue, starting and ending place, posture or gesture, carried
object, interaction or handoff, next state, applicable branch, source class,
and exact source locus. Cover standing, sitting, kneeling, bows, genuflections,
signs of the Cross, breast strikes, turns, formations, processions, bells,
books, candles, cruets, lavabo articles, communion plate, incense, boat, torches,
and every other act actually assigned to the model roster. Omit a listed object
or gesture only when the selected branch omits it, and say so there.

Each sung publication presents both a chronological walkthrough and compact
role-by-role rehearsal sheets derived from the same inventory. The Low Mass
pair presents one continuous chronological route. In every form, check that no
server is required in two places at once, no handoff lacks a giver or receiver,
and no carried object appears without preparation or disposition; in a sung
guide, also check that no role sheet contradicts the chronological route.
Clergy and choir actions appear only as needed cues and must remain visibly
distinct from server instructions.

At the affected step, label each non-core route as one of: prescribed condition,
permitted option, manual convention, sourced local custom, or unresolved
practice. State the default used by the model and show the alternate route only
far enough to rejoin it safely. “Ask the priest or master of ceremonies” may be
a prudent local direction, but it does not replace documenting the branch that
made consultation necessary.

## Flash-card contract

Each form has a parallel cards-only companion generated from the same shared
data. The Low Mass trainer manual owns its printing, actor, branch, and safety
key; each sung full guide retains that responsibility for its companion. The
teaching publications point to the paired catalog companion but do not
reproduce or embed card faces. The Low Mass flash-card companion contains
integrated verbal-response cards only. The Missa Cantata and Solemn Mass
companions retain the same applicable integrated response cards followed by
their form- and role-specific action cards.

Use one physical response card for each stable response or deliberately split
study chunk. Do not maintain separate cue-to-response and
Latin-to-pronunciation physical decks. The front gives the complete spoken cue
or complete verse used for practice. An isolated last word or ellipsis is not
a complete cue. When an appointed reading varies, print a complete,
facsimile-checked example ending on the face and identify it as an example,
not the universal proper text. The trainer may additionally practise the
complete ending from the identified Missal for the actual day. The back gives
the canonical answer. In the Low Mass companion it gives only that complete
answer in bold; pronunciation, meaning, action, exercise, and mastery material
remain in the page-matched booklets rather than on the cards. A sung companion
retains learner syllables and stress, the consistent sound line, a concise
meaning, the response or chunk ID, and any condition needed to prevent a false
response. These are renderings of the received Latin and audited editorial
learning layers; consolidation does not transfer their ownership to the card
layout.

Each physical card has a stable response/chunk or action ID. Its front and back
are generated as one audited pair from the shared data, and the flash-card
manifest identifies the companion that selects it. In the Low Mass companion,
the manifest maps each stable source ID to a printed Mass-order number. Three
header zones read `NUMBER · PRIEST / LOW MASS / STAGE` on the front and
`NUMBER · BOTH / LOW MASS / STAGE` on the back; do not add `Cue`, `Answer`, or
`Card`. A sung companion retains the rendered ID at upper left and `Cue` or
`Answer` at upper right, a compact form marker, and response-card order by the
six lesson groups rather than numerically. Its full guide's card key preserves
the speaker and form distinction so a choir or sacred-minister text is not
turned into an automatic lay-server response. Action cards identify the role,
form, cue, branch, and next action; they do not compress two incompatible local
routes into one answer.

State paper size, actual-size setting, duplex edge, page orientation, cutting
order, and whether blank backs are intentional in the governing card key. Keep
text and cut marks within safe margins. Verify front/back order and alignment
by measured overlay or an equivalent rendered check, then inspect both faces
at full size. A contact sheet alone cannot establish duplex alignment or
small-type legibility.

The Low Mass layout is eight faces on each portrait letter-size sheet, in two
columns by four rows, with each back row mirrored left-to-right for long-edge
duplex printing. Its cue and response text uses one fixed 11.5-point size and
must not shrink to fit. A response that cannot fit as one complete pair is
taught at full width in the page-matched booklets and omitted from the deck.

The sung-form trainer-print layout remains six portrait cards on each
letter-size face, in two columns by three rows, with the backs mirrored by row
for long-edge duplex printing. A sung companion may depart from six-up only
when a recorded legibility or cut-safety check shows that the actual card text
cannot fit at the profile's minimum readable size. Prefer splitting a genuinely
long response into stable sense chunks over shrinking the teaching text.

The cards-only leaf is a print companion, not a self-contained trainer. It
reproduces only the complete selected card faces: no cover, contents,
instruction, actor key, lessons, parity leaf, or terminal reference apparatus.
Its catalog link and the teaching publication's catalog pointer must tell the
reader which card key to use. The required revision and rights notice may
occupy the unused margin below the final back grid but must not add a page or
enter a cut card. Every condition needed to prevent a false individual
response or action remains on the affected face.

The companion begins with the first integrated-response front on odd physical
PDF page 1, and its mirrored back follows on even page 2. Each later sheet
front likewise falls on an odd page. In a sung-form companion, the action deck
begins on the next odd page after the complete even-length response run. Do not
add a cover, instruction, or parity leaf before the card faces. Verify physical
PDF parity after the final build; logical page numbering alone is not
sufficient. No teaching publication has an embedded card range to advertise.

## Required records and ownership

The non-publishable series owner keeps:

- `research/scope.md`: reader, three form boundaries, model horizon, language,
  pronunciation standard, jurisdiction, inclusions, exclusions, pedagogical
  progression, current-authorization boundary, rights, and alpha state;
- `research/edition-manifest.md`: exact Missal, rubrical code, official acts,
  ceremonial and chant books, pronunciation authorities, particular
  directives, manuals, and non-controlling aids actually used, with edition,
  locus, source role, access or collation state, and rights status;
- `research/response-inventory.md`: every cue and reply, stable ID, sequence,
  speaker, mode, condition, form, exact locus, checked Latin, normalization,
  meaning status, and rendered uses;
- `research/pronunciation-audit.md`: syllabification, stress, IPA, respelling,
  governing rule or checked lexical decision, variants, and unresolved source
  questions;
- `research/ceremonial-inventory.md`: the Low Mass two-server model, the two
  sung-form model rosters, and every action ID, route, handoff, source class,
  locus, option, custom, reassignment, and unresolved discrepancy;
- `research/flash-card-manifest.md`: every card ID, front/back data source,
  companion selection, ordering, duplex pairing, and either the completed
  alignment check or an explicit pre-build status;
- `research/presentation-research.md`: evaluated formats, resulting layout
  decisions, and mechanically measured legibility or layout constraints;
- `research/source-audit.md`: facsimile checks, official-source and manual
  comparisons, consequential negative results, rejected edition mixing,
  rights, and completed liturgical, Latin, pedagogical, and production checks;
  and
- `research/production-manifest.md`: the exact seven validated builds, page and
  card counts, log and PDF checks, every-page visual inspection, duplex
  verification, installed identity, and alpha state.

Each publishable leaf keeps `research/guide-map.md`, naming its form, stable
guide identity, imported data selections, model roster where applicable,
reader order, applicable lessons, drills and assessments, page-matched,
paired-guide, or card-face boundary, branches, appendices, and relationship to
the series-wide records. It must account for everything rendered without
copying the controlling inventories.

## Reader order and terminal apparatus

After a compact title, each teaching guide begins with usable guidance. A
front contents page is optional. Preparation and mastery checklists, global
qualifications, source keys, trainer policy, and publication apparatus belong
in terminal appendices. A warning or branch that changes the next action
remains beside that action.

The Low Mass child booklet begins with only the minimum actionable role,
sanctuary, and movement orientation needed to follow the route, then follows
one continuous sacristy-to-sacristy Mass-order route.
Stable stage labels, dialogue lanes, action blocks, and actual sanctuary
diagrams replace progression tables. Pronunciation and meaning appear with a
response's first occurrence; later occurrences keep the complete cue and
response without repeating those aids. Long material that does not fit a
flash-card face may use a full-width phrase ladder. The child booklet contains
no trainer-only source discussion, IPA, quiz, written exercise, or mastery
record.

The Low Mass trainer manual preserves the child's lesson order, action
identity, diagrams, and main-route page boundaries, but need not reproduce
every explanatory word. Two naturally consecutive actions or scenes may
share one page. Later identical movements may use a short explicit recall
only where cue, actor, destination, object, and finish state remain
unambiguous. The child lane is a field guide: cue, actor, observable action, finish
state, and short rehearsal check. Pronunciation meanings, source hierarchy,
manual disagreements, correction cues, preparation, and local-choice rationale
belong in the trainer layer unless a child must know them to act safely or
correctly. A narrow trainer-only rail remains on the left of every instructional
page. The trainer page must still be usable beside the matching child page
without a cross-reference search.
The child and trainer pages are monochrome letter-size publications with stable
type sizes and a typeface whose capital `I`, `J`, and `L` remain clearly
distinguishable.

Every publication-facing instructional scene uses a consistent monochrome
graphite or pencil illustration language on white rather than mixed schematic
and raster styles. Generated art contains no text, arrows, numerals, or
semantic labels; TeX owns those overlays. Altar architecture, steps, figures, carried objects, and movement
paths have distinct and consistent line treatments. Keep role labels in fixed
high-contrast capsules, identify the three levels with stable numbered
markers, and make standing and kneeling recognizable from the figure
silhouette as well as the adjacent words. Object moves and walking routes must
remain visually secondary to the final positions they explain, and crossing
paths or labels may not obscure an actor, object, level, or destination.
When one action contains materially different moments, use numbered
before/after or state-change frames rather than one composite pose. A route
frame names its cue, moving actor, carried object, stopping point, and finish
state. Do not add a figure merely to show both ends of one actor's movement.

Project-owned AI generation and revision are permitted for these instructional
scenes. Generation is a production method, not ceremonial evidence: every
actor, object, posture, route, destination, handoff, and finish state must be
controlled by the applicable publicly reachable source and canonical
inventory. Do not ask a model to resolve an open liturgical or ceremonial
question through visual plausibility. Generated output supplies no source
evidence; the checked inventories and mechanical production tests control what
may be rendered.

Each sung guide begins after its title with the minimum actionable roster and
sanctuary orientation and a direct `Choose your role` path. Standalone
role-by-role learner sheets are the main guidance. Whole-team rehearsal
follows. The complete chronology, response and pronunciation reference,
preparation and mastery checklists, card-printing controls, expanded safety
notes, and global branch rationale belong in appendices. Role sheets and the chronology
remain derived from the same inventory; reader order does not change
evidentiary priority. Put optional and local branches beside the affected
action rather than in an unconnected miscellany.

The main-body design targets are 16--18 pages for Low Mass, 20--22 pages for
Missa Cantata, and 20--24 pages for Solemn Mass. These are design controls,
not authority to omit a cue, action, handoff, or branch or to use unreadable
type. Child action text normally begins near 11.5--12 points; Latin responses
or immediate commands may be larger. Cards retain their existing fixed type
contract.

Each substantive teaching publication ends with `Scope, Edition, and
Qualifications`, references, and `Generation Metadata` as the final content
block. In the page-matched Low Mass pair these may share the final authored
page when they remain legible and in the required order. The terminal material
owns the form boundary, edition, model roster status, excluded ceremonies,
pronunciation convention, current-authorization boundary, global custom and
  manual limits, rights, and alpha state. A condition that changes what a
server says or does remains local as well.

Each cards-only companion follows the source selection and form boundary of its
named teaching publication, begins directly with the first integrated-response
front on physical page 1, and contains no independent teaching prose. Its
local guide map records the planned duplex order, final verified physical page
map, and inherited relationship.

The seven installed PDFs have one catalog home in
`library/traditional-latin-mass.md` and remain together in three form rows.
The Low Mass row gives separate, clearly labeled links for the child booklet,
trainer manual, and flash-card companion. Each sung-form row retains separate
links for its full training guide and cards-only companion. Build,
installation, cataloging, exact-snapshot release authorization, public push,
and deployment are separate operations.

## Profile gate

An alpha snapshot may be installed when source integrity, rights and lawful
distribution, safety, reproducibility and identity, mechanical validity, and
basic visual usability pass. Its first page may carry a terse status-only
`Alpha` footer. The terminal `Scope, Edition, and Qualifications` appendix
explains the alpha state and any work-wide form or use boundary once; immediate
safety instructions and conditions that change an action remain at their
points of use. Catalogs need only identify the work and available formats.
Installation and deployment remain separate operations.

Before installation or release, in addition to the universal gates:

- reconcile every rendered verbal item and card with the response inventory
  and visually collate its received Latin against the identified page image;
- reconcile every Low Mass action, object state, position, and branch with the
  declared two-server model and ceremonial inventory; verify that every
  trainer main lane is page-for-page and word-for-word identical to the child
  lane, that the trainer rail remains on the left, and that no trainer-only
  material enters the child booklet or flash cards;
- reconcile every Missa Cantata and Solemn action in both chronological and
  role views with the ceremonial inventory, including all roster states,
  objects, handoffs, omissions, and branch rejoins;
- verify that server, sacred-minister, choir, and people texts are never
  reassigned or conflated and that every spoken-or-sung label agrees with the
  selected form;
- check every syllable division, stress, IPA transcription, respelling, and
  meaning against its audit row, and inspect IPA glyph rendering and text
  extraction;
- check every applicable exercise, assessment, answer, and card pair for a
  unique stable ID and agreement with its authoritative source;
- build and inspect all seven consumers after any shared render-source change;
  reject unresolved log warnings, overfull or underfull boxes, broken links,
  missing fonts, or unstable contents;
- inspect every page for age-appropriate type size, density, navigation,
  monochrome legibility, writable space, split action units, unsafe diagram
  ambiguity, clipping, accidental blanks, and final-colophon fit;
- inspect flash-card faces at rendered full size and verify mechanically that
  the first integrated
  response front and each later sheet front are on odd physical PDF pages,
  then verify duplex edge, front/back alignment, cut safety, the Low Mass
  eight-up grid and fixed 11.5-point text, the sung-form six-up grids,
  Mass-order or lesson-group order as applicable, form markers, and the absence
  of an inserted cover or parity page; and
- state liturgical, ceremonial, Latin-pronunciation, pedagogical, and rights
  bounds accurately. Received Latin and other third-party material require a
  local rights statement and recorded distribution basis.
