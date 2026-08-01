# The time machine: the missal's history as a map of acts

The settled constraints for showing how the missal changed — a generated git
repository that is a research product in its own right, an interactive map, and
a printed one.

**This records rulings, not mechanism.** Research into layout algorithms,
generation and rendering is in progress and will be folded in. What is below was
settled by the maintainer and is not open for a lane to relitigate.

---

## 1. A station is an act

> Each change in the missal **must** be associated with a decree or — in the case
> of partial schism — a local edict or refusal. Each station corresponds to an
> *event*. It may be agreed in hindsight, but all changes *happened*.
> — the maintainer, 2026-07-31

A station is not an edition somebody has a scan of. It is a promulgation, a
decree, a motu proprio, an instruction, a rescript, an indult — something that
was **done**, on a date, by someone, recorded somewhere.

Three things follow, and the third was not anticipated when the rule was made.

**The graph is sourced by construction.** A node without an act is not a station,
so the map cannot contain an unsourced node. This is stronger than requiring
every edge to cite a source, because it binds the nodes too.

**A refusal is an event, and that is where a branch is born.** A local church
declining to receive a change is an act. So branches do not have to be asserted
by us on noticing a difference; they *begin* at a documented refusal or local
edict exactly as the main line begins at a promulgation. That is provenance for
the topology itself.

**It removes the OCR hazard at the root.** This corpus is optical text from old
scans, and this project measured 38 of 99 orations taken from OCR as wrong,
mostly character-level. A time-lapse over unreviewed OCR would show *the scanner*
changing its mind and present it as the liturgy changing. Under this rule it
cannot: a difference between two printings with **no act behind it is not a
change to the missal**. It is a difference between witnesses, and witnesses live
beneath the history. Compositor's variation, printing differences and OCR error
never become stations, so a reader cannot mistake one for a revision.

> **Rule 1.** No station without an act. A version nobody can cite an act for
> does not appear on the map, however many printings attest it.

A corollary that must be kept in the data: **the act is fixed and citable; what
is understood to have changed may be revised and is contested for some acts.**
Keep them separate, so a later historical judgement does not move a station.

---

## 2. Parallel stays parallel

There is no rebase and no merge for its own sake. Where two missals ran side by
side, the history shows two lines that never rejoin — the maintainer's analogy is
emacs and xemacs.

A merge commit contains one resolved tree and therefore **asserts a synthesis**.
Liturgical history frequently has coexistence *without* resolution: two uses
continuing for centuries, a feast in some calendars and not others, an indult
keeping an older form alive. Drawing a merge where no reception occurred would
not look like invention — it would look like tidy history, which is worse.

The transit metaphor already carries this distinction natively. Two lines
crossing **with** an interchange symbol means you can change trains; crossing
**without** one means you cannot. Reception is an interchange; its absence says
plainly that none occurred, and no caption has to explain it.

> **Rule 2.** A merge only where reception is documented, with the act cited.
> Where texts coexist, parallel lines and no connecting edge.

Several roots are correct where descent is genuinely disputed. One invented
common ancestor is not.

---

## 3. A map, not a slider

A slider implies a total order. A directed acyclic graph has none, and a viewer
that pretends otherwise shows one line where two traditions ran.

A transit map has no total order either — only lines and stations, with no notion
of "position 47 of 200". The topology *is* the diagram. Parallel traditions are
parallel lines; editions are stations; a suppressed use is a terminus; a
translation drawing on a Latin typical edition is an interchange.

Beck's 1933 map is the reference, and the relevant insight is that it is
**topological rather than geographic**: it distorts distance to make structure
legible. Four centuries between two stations and four years between two others
must both read.

---

## 4. Levels of specificity, derived and never curated

Both the interactive and the printed map need a high-level view and a fine-
grained one. Under Rule 1 the fine map has as many stations as there were acts,
so a high-level view must collapse some — and under Rule 1 all of those changes
happened, so a collapse must not amount to deciding that some did not.

> **Rule 3.** The level of detail is derived from a **property of the act**,
> never from a judgement of its importance.

This follows from `editorial.md`, "No side in what is described". A hand-curated
list of *the important changes* is precisely where a partisan reading enters —
invisibly, dressed as design. Deciding by hand that one reform is major and
another minor is an editorial claim wearing the costume of a zoom level.

The candidate derived property is the **juridical rank of the act**, which is a
fact about the document rather than an opinion: an apostolic constitution, a
motu proprio, a decree of a congregation, an instruction, a rescript. Whether it
is recorded consistently enough to drive a rendering is an open question and is
under research; if it is not, another derived property must be found rather than
a curated list adopted.

> **Rule 4.** A collapsed view says that acts happened which it does not show.
> An unbroken line where stations were omitted is the difference between
> simplifying and misleading.

---

## 5. Two artifacts, one generator

The interactive map and the printed map come off the **same source**, and so does
the git repository. This repository's standing rule is one derived table with no
hand-made restatement beside it; it found four separate hand-copy drifts in a
single day. A hand-drawn poster would diverge from the data the moment a station
was added, and would then be a beautiful lie.

The generated git repository is an **output**, a build artifact like the PDFs.
Regeneration rewriting its hashes is expected and is not a loss, because the
record is the source data. It is nonetheless intended to be useful to other
researchers on its own, which makes reproducibility a requirement rather than a
nicety.

> **Rule 5.** Every artifact is generated from the one source. Beauty in the
> printed map comes from the constraint system — the angle set, the spacing, the
> label rules — and not from hand-tweaking, because a tweak is a restatement and
> restatements drift.

---

## 6. What is precedented, and what is not

Researched 2026-07-31. Recorded here so the claim can be checked rather than
asserted, and so nobody has to establish it twice.

**The primitive has been used, twice, in unrelated domains.**

- Burkhard and Meier, *J.UCS* 11(4), 2005, put dated milestones in the station
  slot for hospital project-management posters, with lines as stakeholder
  audiences and an explicit left-to-right time axis. Field-evaluated: 45
  responses from 81 staff, 78 per cent agreeing it gave overview. Their stated
  limitation is one this project inherits and answers — *"the printed posters
  are static and difficult to update"* — which is exactly why Rule 5 requires the
  printed map to be generated. An automated successor exists (Stott, Rodgers,
  Burkhard, Meier and Smis, IV'05). [sourced]
- Narrative Maps (Keith Norambuena, Mitra and North, CSCW 2021) put events on
  routes for sensemaking over news corpora, and were evaluated against a timeline
  baseline. Two of their design guidelines apply directly to a chronology of
  acts: **avoid edges inferable transitively**, and **distinguish connection
  types** — a topical relation and a causal one should not share a stroke.
  [sourced]

**Nothing exists for a documentary or juridical chronology.** An exact-phrase
search for `"tube map" "canon law"` returns zero results. Legislative history is
universally drawn as a flowchart, which is the right diagram for *process* — how
a bill becomes law — and the wrong one for *descent and coexistence*. Church
history exists only as conventional timelines. Brexit Mapping, by a transit-map
scholar, keys stations to issues and lines to economic sectors, with no dates at
all: a thematic map, not a chronology. [sourced]

**The notation this project needs is unclaimed.** Burkhard and Meier have
"collective milestones" in their data model and publish no visual grammar for
them. Shahaf and others formalise an interchange as shared-station identity and
say nothing about meaningless crossings. MetroSets' central criticism of a rival
idiom is precisely that it produces *"many crossings without semantic meaning"*.
**No published metro map has a grammar separating "these lines meet" from "these
lines merely cross".** That separation is Rule 2, and it is the part of this
design with no prior art.

So the honest position, which is stronger than a claim of pure originality
because it is checkable: the application is new, one narrow precedent exists for
the station-as-event slot and is cited, and the grammar is unclaimed.

Two bounds declared rather than hidden: treaty and diplomatic history beyond
Brexit Mapping is **unverified, not negative** — the search died on rate limits —
and a snippet-referenced paper, "Metaphorical metro maps: design challenges"
(Ruhr University Bochum), could not be located in OpenAlex, arXiv or Semantic
Scholar and **may not exist as described**. [inferred]

---

## 7. The diff is the deliverable

> The missal timeline should land in a way that each commit shows a diff that
> represents what was trying to be merged. This dictates how you store and index
> each missal, such that it will show a "most minimal diff". We are trying to be
> as charitable as possible; we don't want each missal revision to look like a
> wholesale rewrite.
> — the maintainer, 2026-07-31

The repository's worth is that `git show` on a station displays what that act
changed and nothing else. A revision touching six orations that renders as a
rewrite of the book has failed, however correct its contents. So **"what does the
diff look like" is the acceptance test for every storage decision**, not a
consequence of one.

Four things decide it.

**File granularity.** One file for the missal means every act rewrites
everything. One file per addressable unit means an act touches only what it
changed. Too coarse and a one-word change shows as a page; too fine and the tree
is thousands of files, which git handles and a browsing reader does not.

**Path is liturgical identity, never page order.** A file at
`temporal/advent-1/collect` is the same object across four centuries. A file
named for a page or a line range is a different object every printing, and every
insertion above it cascades. This is precisely why the earlier corpus's
`source_lines: 50001-70000` could not produce a minimal diff: it addressed text
by where it fell in a scan.

**Deterministic serialisation.** Stable key order, stable wrapping, stable
encoding, so that regenerating an unchanged text produces no diff at all.
Nondeterminism becomes noise in every commit and drowns the signal.

**Semantic line breaks.** Prose stored as one long line diffs as one long line:
change a word and the whole prayer lights up. Broken at clause or sentence
boundaries, a changed clause shows as a changed clause. The rule must be applied
mechanically, because a hand-wrapped text will be rewrapped by the next person
and produce a phantom diff.

> **Rule 6.** Store text so that the smallest honest change produces the smallest
> diff. Not smaller than honest — where an act genuinely rewrote a book, the diff
> says so.

**A consequence that may come free.** If each text lives in its own file at a
path encoding its slot, git's own rename detection expresses the `reslotted`
departure of `recensions.md` §3 natively: the Easter Vigil postcommunion becoming
the Vespers prayer *Spiritum* renders as a rename with similarity rather than as
a deletion beside an unrelated addition. If that holds, the hardest departure
kind needs no special machinery in the viewer — git already tells the story.
[inferred, under test]

---

## 8. The second axis: the Mass as the horizontal

> A page that showed at a high level the parts of the mass that changed from one
> missal to the next … visually tracks the mass on a horizontal timeline through
> the mass and indicates between two missals which of each part of the mass
> changed and how/why.
> — the maintainer, 2026-07-31, offered as a stretch goal

**This is the transpose of the map, not a separate feature.** A change is a pair:
*(act, part of the Mass)*. The map of §3 indexes that pair by **act** — when
things happened and how traditions descend. This view indexes it by **part** —
what changed, in the order a Mass is actually said: Introit, Collect, Epistle,
Gradual, Gospel, Offertory, Secret, Preface, Canon, Communion, Postcommunion.

It also answers a question §3 left open. **What does a reader do on arriving at a
station?** They see what that act changed, laid out along the Mass. The two views
link through the act, so the *why* of any marked part is the station that changed
it, and the *how* is the diff of Rule 6.

> **Rule 7.** Both views are generated from one dataset. Neither may hold a fact
> the other cannot see.

**The hard part is that the order of the Mass is itself one of the things that
changed.** Comparing two missals means aligning two sequences that are not the
same sequence, so this is a genuine alignment problem and not a zip of two lists.
A part may be unchanged, reworded, added, removed — or **moved**, which is
`reslotted` in `recensions.md` §3, and which breaks naive alignment precisely
because both sides hold the text.

The prior art here is **not** metro maps. Textual collation has solved most of
it: an alignment table putting witnesses in rows and the text in columns with
variation marked is close to what is being described, and transposition is the
known hard case that some collation tools handle and others explicitly refuse.
Genome browsers solved the horizontal-coordinate-with-stacked-tracks problem
long ago. Both are better starting points than anything in version control.

---

## 9. What the research settled

Two lanes surveyed the field on 2026-07-31. What follows is only what changes
what gets built; the full reports are cited from their sources.

### Do not write a layout algorithm

Octilinear layout is **NP-complete** — Nöllenburg, Tech. Rep. 2005-25, by
reduction from Planar 3-SAT. The 2011 mixed-integer formulation takes **ten
hours on London** and cannot label it at all. The 2020 grid-routing
approximation (Bast, Brosi and Storandt, *CGF* 39(3)) does London in **2.7
seconds** within 7.3 per cent of optimal. [sourced]

**LOOM/`octi`** implements it — GPL-3.0, C++, actively maintained. Decisively,
it accepts a **DOT file with `pos="x,y"`** as plain Cartesian doubles, so an
abstract graph needs no geography: a generator can emit *x = date, y = tradition
lane* and let `octi` octilinearise it. One emitter, DOT, `octi`, SVG — and the
same emitter feeds the interactive version, which is Rule 5 satisfied rather
than worked around. [sourced]

**Labelling, not layout, is where automation still fails**, and the generator
must do it. Neither `octi` nor TikZ will.

### TikZ cannot do this under pdflatex

PGF's `graphdrawing` refuses to load outside LuaTeX, and ships **no octilinear
algorithm** in any case; no metro-map package exists on CTAN. TikZ is a
renderer, not a layout engine. The route that keeps the document's own
typography is the **`svg` package** with Inkscape's LaTeX text export: generated
geometry, typeset labels. [verified against this machine's TeX Live]

### Monochrome works, and the ceiling is measured

Transport for London publishes an official black-and-white Tube map — *"© TfL
April 2026"*, 1053 × 668 mm — distinguishing **22 services with no colour at
all**. The grammar is copyable: **constant band width** for every line, so
weight stays free for another dimension; the differentiation is the band's
**internal texture** plus **three grey values**; and it is paid for with
**2.4× more repeated inline naming** than the colour map. [verified from the
plate]

At ten or so traditions this is comfortable, with weight left over.

Note one convention already in a reader's vocabulary: TfL's glyph for an
out-of-station walking interchange is **two circles joined by three dots** — a
connection that is *not* a through-running of the line. That is close to Rule 2's
"contact without reception".

### Citation on the plate

Priestley's *Chart of Biography* (1765) put 2,000 dated items on a timeline and
solved the apparatus with **numbered items and a facing catalogue**. He also put
a complete **uncertainty grammar** on the plate: a full line for certainty, and
dots disposed differently for "a little before or after", "about", birth known
and death not, and — where even the century is uncertain — **no full line at
all**. That is an implementable monochrome epistemic notation, tested on 2,000
items, using only the dash channel. [sourced]

What to reject in him: he refused per-item citation as "endless" and gave a
global bibliography instead. That refusal is precisely what separates an
infographic from scholarship.

The modern complement is the ICS chronostratigraphic chart, which carries on the
plate: a notation legend, an epistemic marker defined (`~` for approximate), a
status disclaimer, the provenance of the data *with its exceptions named*, an
edition stamp, a **version-pinned URL**, and a **"To cite:" line**. For a derived
artifact that must match its interactive twin at a stated moment, the pinned URL
and edition stamp are the highest-value lines on the sheet. [sourced]

### Sizing, measured rather than estimated

TfL's black-and-white plate carries ~500 stations at ~1,400 mm² each with 2.9 mm
cap height. So: **40 nodes fit A3, 100 fit A2, 200 fit A1 with room for the
apparatus, 400–700 need A0.** Reserve 15–25 per cent for the key unless it goes
in facing text. [verified by measurement]

### Three findings that argue against parts of the metaphor

These are recorded because the design should answer them, not because they sink
it.

**Beck's rule-set is not a gold standard.** Roberts and others compared the
official octilinear Paris Métro map against a hand-drawn all-curves version:
journey planning was *faster* on the curves, effect sizes 0.48 to 1.12, and their
conclusion is that "there is no evidence to suggest that any rule-set can be
claimed to be a gold-standard". Preference and performance correlate at
effectively zero — **do not evaluate this map by asking whether people like it.**
[sourced]

**Symbol choice changes what readers believe.** Guo measured that the London map
represents about **4 per cent** of the variation in real distance, and that over
30 per cent of passengers chose a route ~15 per cent slower because the map made
it look shorter. More pointedly, the same interchange drawn as a dot versus as a
long link between platforms **changed which transfer passengers made**. Rule 2's
whole burden — that a meeting and a crossing must look different — is the same
mechanism, and it cuts both ways. [sourced]

**Storyline visualisation has no merge operator**, which is a gift. Lines run
adjacent and separate again; they never fuse. That is Rule 2's parallel case,
already published and evaluated. Conversely it offers no vocabulary for a genuine
merge, so reception needs its own mark. [sourced]

### When the industry needed branching and time together

It kept the topology and **put the time in labels, not geometry**. The Swiss
*Netzgrafik*, in service since 1982, prints arrival and departure minutes beside
stations on a topological graph, and encodes frequency in line style. TfL's
Walking Tube Map prints minutes on uniform-length edges; a 1960s San Francisco
map printed travel time at each station. **Two mature independent systems both
chose to label the edge rather than lengthen it.** [sourced]

Against that, one published diagram deliberately does the opposite: the
project-plan metro map deletes the uniform-edge-length objective because "long
edges convey meaning". Strict octilinearity and strictly time-proportional
Euclidean length **cannot both hold** — a 45° edge's x-extent is length/√2 — so
this is a choice that must be made explicitly. No diagram exists that is both.
[sourced]

### Stemmatology has the vocabulary for uncertainty, and none for refusal

The discipline standardises sigla — `O` the lost original, `ω` the archetype,
Greek minuscules for lost hyparchetypes, Latin capitals for extant witnesses —
and a solid line for descent, usually without arrowheads. Contamination is a
broken line, though dotted versus dashed is the author's choice. **The y-axis is
generation depth, not time**, explicitly. [sourced]

Three things to take:

- **The crux, †.** A centuries-old first-class sign meaning *something is
  demonstrably wrong here and I cannot account for it*. The nearest respectable
  precedent for a change whose authority cannot be established — with the caveat
  that the crux asserts corruption where our case may be neutral.
- **The Leiden Conventions.** Bracket shape encodes **who is responsible** for a
  deviation: `[…]` the material perished, `⟨…⟩` the scribe erred, `{…}` the
  editor judges, `(…)` the editor expands. Same content, different bracket,
  different agent. That architectural pattern is worth copying wholesale.
- **The soft polytomy.** Where the order of branching cannot be recovered, draw
  the branches from one point rather than inventing an order. Phylogenetics
  distinguishes *quantified but drawn* from *unquantifiable so not drawn*, which
  is exactly Rule 3's distinction.

And the negative that matters: **no convention exists for an absent or refused
relation** — not in stemmatology, not in genealogy, not in phylogenetics, where
absence of a branch is simply absence. A documented refusal-to-receive as a
first-class branch-creating event is notation this project invents. Define it in
a legend and do not claim conventionality. [sourced]

### One number, read correctly

Gallotti, Porter and Barthelemy put the cognitive limit for planning a trip at
about **8 bits**, and concluded maps "should not consist of more than 250
connection points". That counts **branch alternatives a reader must discard**,
not stations: a 500-node chain sits under it, a 250-node high-branching graph
does not. For this project it is a constraint on **branching factor**, not on how
many acts the map may carry. [sourced]
