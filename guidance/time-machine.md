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
