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
- Is every statement either edition makes about the other true of the
  companion as derived?

## Statements about the other edition are yours

The canonical edition was settled before the companion existed, and it
already says things about the companion: `format.tex`'s canonical
`\editionnote` may claim the companion "adds nothing this edition does not
contain", `sections/90-scope.tex` may say what the synthesis edition names at
each use of a translation, and a file both editions input may carry a
cross-reference or locator that has to resolve in both. Read each such
sentence against the companion's build and report it where it is false.

**That class now has an owner, and it is not `derivation`.** Where the
companion cannot be made to satisfy the sentence without the shared file
changing — because the profile forbids the companion the apparatus the sentence
names, so nothing inside `sections/synthesis/` can make the pointer resolve —
raise the finding with:

```json
"repair_target": "seam"
```

A `seam` finding licenses the reviser to wrap that one clause in an
`\ifdefined\TriptychSynthesisEdition` branch, leaving the canonical rendering
byte-identical, so the companion's reader gets a sentence true of the edition
in hand. Say in `required_result` which clause, in which file, and what the
companion's branch should say.

Keep `derivation` for what the companion itself got wrong: a claim it
misstates, a locus it dropped, prose it lifted. The test is not how serious the
defect is but which file has to change to clear it. Getting this wrong in
either direction wastes a round — a `seam` defect sent to `derivation` reaches
a reviser forbidden to repair it, and a `derivation` defect sent to `seam`
invites an edit to canonical prose that nothing evaluated.

This class was sighted eight times across two productions and owned by nobody,
because it is a claim about an artifact no canonical lane could see. Run
`da04e65ca4ec963b` raised twenty-four dangling locators in one round and the
reviser reported every one of them unrepaired, correctly.

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
