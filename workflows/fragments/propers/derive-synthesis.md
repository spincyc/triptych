# Derive the Synthesis Companion

## Your task

The canonical edition is settled. A content evaluation has passed on it, and
its prose is now the authority for this formulary. Your job is to derive the
synthesis companion from it.

Derive, in this workflow, is a direction and not a build step. The canonical
guide is the largest edition and it was produced first; the companion is the
smallest and it is produced from what the larger one already settled. Nothing
you write here may add a claim, a witness, a locus, a count, or an evidence
state that the canonical edition does not already carry. Where the two must
differ, the companion says less — never something else.

## Why this stage exists

Both editions used to be authored together and evaluated together, and it cost
a production its whole iteration budget. Every evaluation lane read two
documents; every finding had to be repaired in two places; and a class of
defect existed that could not exist here — a claim corrected in one edition and
left standing in the other, published and wrong, because the reviser repaired
the file it was shown and not its twin. Run `e4aebcbd941b6b1a` raised that
class repeatedly, and its evaluation lanes recorded prose duplicated between
the two editions as an unowned observation at six consecutive iterations
because no criterion reached it while both were in flight at once.

Sequencing them removes the class rather than policing it. When you begin, the
canonical edition is fixed; when you finish, the companion is checked against
it once, by a stage that can see both.

## Find out what this leaf builds before you write anything

Do not assume a form. Leaves in this tree are in three states, and a rule
written from the shape of one is false of most of them: many build no
companion at all, some build one from a `synthesis.tex` that is a document in
its own right with its own `\input` list, and some from a two-line stub whose
branches live in `main.tex`.

So read, in this order: the profile in
`guidance/liturgy/roman-1962-propers.md` for whether this identity is required
to carry a companion, `proper-components.toml` for what the manifest declares
in each mode, and the leaf's own top-level `.tex` files for what is already
there. Then write what those three say is wanted.

**Where the profile requires no companion for this identity, that is your
answer.** Return `PASS`, say so in the summary, and write nothing. Inventing a
second document because the pipeline has a stage for it is the one failure
this stage can commit that no later evaluation would catch, because a
companion that should not exist still renders.

## What you write

1. `synthesis.tex` — where the leaf's established form is the stub, a two-line
   stub that defines `\TriptychSynthesisEdition` and inputs `main.tex`, and
   nothing else in it. Where the leaf's form is a standalone companion
   document, keep that form rather than converting it.
2. The `\ifdefined\TriptychSynthesisEdition` branches in `main.tex`, and the
   files under `sections/synthesis/` that those branches input.
3. `proper-components.toml` — the manifest must declare which components the
   synthesis mode carries and which the research mode carries, and no included
   component may depend on an omitted one. Declare `[[components]]` in the
   profile's reader order — the source-grounded synthesis, then `The Propers:
   Notable and Quotable`, then `The Propers: Interpretive Possibilities` —
   which `check-proper-components` requires of a revised manifest.
4. `generation-metadata.tex` — bring `\AIDocumentRevisionTimestamp` forward
   to this derivation and append an `\AIModelContribution` record for it, on
   the rules `author-proper.md` states for that file. The
   `\AIGenerationProvenance` record is unchanged: this is the same run. A
   companion derived at 19:06 under a timestamp of 17:30 was found by an
   evaluator reading mtimes, and nothing in the workflow had told the stage
   that wrote it the file existed.

You may not touch `research/scope.md`, which no stage but its writer —
`research-synthesis` in `proper`, `brief-revision` in `proper-finish` — may
change. You may not touch `propers/verified.md` or `propers/retrieved.txt`.

## What the canonical edition already says about the companion

The settled edition makes claims about the document you are deriving, and it
made them before that document existed: `format.tex`'s canonical
`\editionnote` may assert that the companion "adds nothing this edition does
not contain"; `sections/90-scope.tex` may state what the synthesis edition
names at each use of a translation; a file both editions input may carry a
locator that has to resolve in both. Under the sequence these are
**constraints the derivation must satisfy**, not descriptions of an artifact.
Read them before you write, derive so that each is true, and where one cannot
be made true of a faithful companion, say so in your summary: you may not
edit them, since they are canonical prose, and the `companion-conformance`
lane judges them next. Eight sightings across two productions found such a
sentence describing a companion nobody had yet written.

**You may not revise the canonical edition's prose.** It passed. If deriving
the companion shows you a defect in it, say so in your summary and leave it:
the synthesis evaluation that follows can raise it against the right owner.
Editing settled canonical prose here would put work beyond this stage's
evaluation and reopen what the previous stage closed.

## What the companion carries

Read `guidance/liturgy/roman-1962-propers.md` for what the profile requires of
the companion, and the canonical leaf for what there is to draw on. The
companion omits the appointed texts and the element-by-element sweep, and
carries an integrated commentary in their place. It keeps the reader order and
the page assignments the profile fixes, measured against its own build.

Two things the sequencing now makes your responsibility, because they are
decidable here and nowhere else:

- **Do not restate the canonical commentary at length.** The companion is a
  redistillation, not an abridgement, and copying or lightly compressing the
  full commentary is the failure the profile names in terms. Where a claim has
  its fullest home in the canonical edition, the companion states the
  conclusion and does not reproduce the working.
- **Do not let a claim reach the companion at a higher evidence state than the
  canonical edition gives it.** A bound the larger edition attaches to a claim
  travels with the claim. The short form is where a lead most easily stands
  flat, because the sentence that qualified it was the one cut for length.

## Result

Return a worker result. `PASS` when the companion is derived and both editions
build; `BLOCKED`, with a summary naming what stopped you, when it cannot be.

Say in your summary what the companion omits relative to the canonical
edition, and name any canonical defect you saw and left alone.
