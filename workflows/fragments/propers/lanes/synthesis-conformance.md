# Lane: Companion Conformance

## Your lane

You own criterion **4 (Companion conformance)** of the shared criteria above,
and nothing else. The derivation-fidelity lane owns criteria 1 to 3; do not
report on them, and do not judge the work as a whole.

Read the companion's own build against the profile in
`guidance/liturgy/roman-1962-propers.md`, and answer only:

- Does the companion's reader order and page assignment match what the profile
  fixes for it, measured on the companion's own build and not the canonical
  one?
- Is every count the companion states true of the companion's own text?

## Counts are yours, and the abridgement is where they break

A count the companion states about its own material is a fact it asserts, and
it is checked against what is there. This lane exists for it because the
abridgement is exactly where a true sentence becomes false: the companion
inherits a sentence written for the full commentary — `four witnesses`, `three
ways`, `read here and nowhere else` — and then carries three of the four, or
two of the three, because the fourth was cut for length. The sentence is
unchanged and now untrue.

So count what the *companion* prints, never what the canonical edition prints
under the same heading. When a sentence announces a number — witnesses,
manuscripts, elements, features, senses, proposals, occurrences, departures,
divisions — count what follows it in the companion and check the two agree.
Do the same for a total against its rows, a `both` against a list of three, an
`only` against a second instance elsewhere in the companion.

Say in `required_result` which half you believe is wrong, the number or the
list, and on what. A reviser cannot tell from the finding alone whether a
witness was cut or was never there.

## Not yours: whether the companion says more than the canonical edition

Whether the companion asserts something the canonical edition does not, and
whether it reuses canonical prose verbatim, are criteria 1 and 3 and belong to
the derivation-fidelity lane. Your interest in the companion's content is its
internal arithmetic and its rendered order, not its faithfulness. Leave
faithfulness there.

## Not yours: the canonical edition's pagination

The canonical edition passed its own evaluation, including its reader order.
Measure the companion. Where the profile's requirement is met by the canonical
build and missed by the companion's, that is a finding; where both miss it, the
canonical edition's evaluation is what should have caught it, and this is an
observation rather than a blocking finding against the derivation.

## Result

Return an evaluator result for this lane. `PASS` when the criterion is met,
`CHANGES_REQUIRED` with blocking findings when it is not, `BLOCKED` when a
finding cannot be resolved by revision.

Record under `observations` anything real your criteria do not reach.

Finding IDs must use the `SYN-CON-` prefix and be stable across iterations.
