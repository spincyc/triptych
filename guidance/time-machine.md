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
