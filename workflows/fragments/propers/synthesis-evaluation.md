# Synthesis Companion Evaluation

## Your task

You are a fresh evaluator. The canonical edition is settled and has already
passed its own content evaluation; the synthesis companion has just been
derived from it. You evaluate **the companion, against the canonical edition
it was derived from**.

That comparison is the whole of your job, and it is why this stage exists
separately. Do not re-evaluate the canonical edition. Do not raise a defect
that is equally true of the canonical prose — that document passed, and
reopening it here spends a budget that was closed. If the companion is faithful
to a canonical edition that is itself wrong, the companion is not what is
wrong; record it as an observation and let it reach a person.

## What each document is

- `main.tex` builds the canonical guide. It is the largest edition and the
  authority for this formulary.
- `synthesis.tex` is a two-line stub defining `\TriptychSynthesisEdition` and
  inputting `main.tex`. The `\ifdefined` branches in `main.tex` and the files
  under `sections/synthesis/` decide what the companion carries.

Follow the inputs both ways before you read anything, and name in every
finding the file the defect is in and the line or sentence within it.

## Evaluation criteria

Your stage owns four, and the lane fragment that follows tells you which are
yours:

1. **Derivation fidelity**: Does the companion assert anything the canonical
   edition does not? A claim, witness, locus, date, attribution or count
   present in the companion and absent from the canonical edition is a defect
   of derivation, whatever its merits.
2. **Evidence state carried down**: Where the canonical edition bounds a
   claim — a lead not yet checked, a reading held on one printing, a
   translation named — does the companion carry that bound? The short form is
   where a qualification is most easily cut for length, leaving the claim
   standing flat in the edition nobody compared.
3. **Redistillation, not abridgement**: Is the companion a cross-proper
   argument in its own right, or the canonical commentary copied and lightly
   compressed? Substantial verbatim reuse is the specific failure the profile
   names, and this is the stage that can see it, because it is the only stage
   that reads both documents with the larger one already fixed.
4. **Companion conformance**: Does the companion's own build match the reader
   order and page assignments the profile fixes, and is every count it states
   true of its own shorter text? A count true of the full commentary is
   routinely false of the abridged one that inherited the sentence.

## Repair ownership

Every **blocking** finding carries `repair_target`, and your packet's
`REPAIR_TARGETS` header names the values this run admits. In the ordinary case
that is `derivation` alone: the canonical edition and the brief are both
settled, and what you are judging is the derivation. Where the header names
more, the shared rules for choosing an owner apply.

A defect that is equally true of the canonical edition is not a derivation
defect and must not be routed as one. Where the header admits no owner who may
write the canonical leaf, such a defect is an `escalation` or an observation,
not a blocking finding — see the shared fragment above for both shapes.

## Result

Return an evaluator result. `PASS` with no blocking findings, or
`CHANGES_REQUIRED` with them, or `BLOCKED` where a finding cannot be resolved
by revision.

Record under `observations` anything real your criteria do not reach —
including a canonical defect the companion faithfully inherited.

Finding IDs must use the `SYN-` prefix and be stable across iterations.
