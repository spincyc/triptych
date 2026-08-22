# Metaphysical Demonstration Textbook - Document Specification

> **Status: frozen architectural contract.** This file is the binding
> specification for the metaphysical-demonstration project, produced by the
> architecture lane. It binds every later lane — chapter authoring, exercise
> authoring, LaTeX production, and review — which implement against it and do
> not renegotiate it in passing.
> Canonical repository-relative path: `metaphysical-demonstration/DOCUMENT-SPEC.md`.
> A later agent who finds this specification inadequate, ambiguous, or wrong
> **escalates for an amendment** to the coordinator and halts the affected work;
> deviating locally, or silently interpreting around a gap, is a defect.

## Contents

- [1. Mission and Audience](#1-mission-and-audience)
- [2. What This Project Means by "Metaphysical Demonstration"](#2-what-this-project-means-by-metaphysical-demonstration)
- [3. Glossary of Methodological Terms](#3-glossary-of-methodological-terms)
- [4. The Canonical Proof Object](#4-the-canonical-proof-object)
- [5. Formal Logic and Metaphysical Semantics: The Three-Layer Representation](#5-formal-logic-and-metaphysical-semantics-the-three-layer-representation)
- [6. The Proof-Audit Rubric](#6-the-proof-audit-rubric)
- [7. Error Taxonomy for Metaphysical Demonstrations](#7-error-taxonomy-for-metaphysical-demonstrations)
- [8. Curriculum and Table of Contents](#8-curriculum-and-table-of-contents)
- [9. The Exercise System](#9-the-exercise-system)
- [10. The Proposition and Dependency Ledger](#10-the-proposition-and-dependency-ledger)
- [11. Margin Annotation Grammar](#11-margin-annotation-grammar)
- [12. Visual and Production Requirements (Specification Only)](#12-visual-and-production-requirements-specification-only)
- [13. Source and Authority Policy](#13-source-and-authority-policy)
- [14. Declared Framework and Neutrality Policy](#14-declared-framework-and-neutrality-policy)
- [15. The First Vertical Slice](#15-the-first-vertical-slice)
- [16. Acceptance Criteria for Later Lanes](#16-acceptance-criteria-for-later-lanes)
- [17. Questions Deliberately Deferred](#17-questions-deliberately-deferred)
- [Appendix A. Architectural Exemplars](#appendix-a-architectural-exemplars)


## 1. Mission and Audience

### 1.1 What the eventual document is

The document specified here is a textbook-style lesson teaching a reader to
perform five operations on a metaphysical demonstration: **construct** one,
**inspect** one, **defend** one, **refute** one, **repair** one. Every chapter,
example, and exercise builds one of those five capacities; material that builds
none of them does not belong in the book.

Its organizing content is the chain it never lets blur:

```text
formal validity != soundness != philosophical warrant
    != metaphysical demonstration != metaphysical explanation
```

The first four are rungs (`RG-VALID`, `RG-SOUND`, `RG-WARRANTED`,
`RG-THAT`/`RG-WHY`); the fifth is `PRI-GND`, a relation between facts and not an
argument at all.

The book is not a survey of metaphysical positions, not an apologetics tract,
not a history of philosophy, and not a logic text with metaphysical examples
attached. Doctrine appears only as material to be audited.

### 1.2 Competence assumed on entry

Later authors MUST assume all of the following and MUST NOT teach any of it.
Each item is stated so a reviewer can write a diagnostic question for it.

1. **Logic.** Reads and writes a natural-deduction derivation in first-order
   logic with identity, naming the rule at each line; treats soundness and
   completeness as distinct properties; reads a countermodel.
2. **Scope discrimination.** Distinguishes a quantifier scope error
   (`∀x∃y Rxy` vs `∃y∀x Rxy`) from a modal scope error (`SCP-CMP`, `□(A → B)`,
   vs `SCP-DIV`, `A → □B`), and can say why they are not the same mistake.
3. **Modal logic at reading level.** Knows what a Kripke frame is, that `S5` and
   `T` differ, and reads `□`/`◇` without gloss.
4. **Mathematical proof.** Follows induction, reductio, proof by cases, and a
   uniqueness argument; sees when existence is proved without construction.
5. **Philosophy.** States, unaided and without caricature, the core claim of
   nominalism, of Humean regularity theory, and of physicalism; knows the
   analytic/synthetic distinction and that it is contested.
6. **Theology.** Knows that natural and revealed theology differ in premise
   source; names the classical divine attributes (simplicity, immutability,
   unity, omniscience, omnipotence, goodness) and treats each as a distinct
   claim, not a package.

**Not assumed**, and therefore introduced under a `TM-###`, `DF-###`, `DS-###`,
or `PR-###` before first use: act and potency; hylomorphism; the
essence/existence distinction; analogical predication; `DK-REAL`/`DK-VIRT`/
`DK-NOM`; `SER-ACC` versus `SER-ESS`; the grounding literature; scholastic
Latin; any reading of Aristotle or Aquinas; sequent or tableau notation; set
theory beyond the naive; any religious commitment. An author needing a
competence absent from the six items above MUST introduce it under an id or
escalate per §1.5 — never assume it silently.

### 1.3 Exit profile

A graduate can do the following unaided. This list is the target the exercise
system and the audit rubric serve: every exercise cites at least one item, and
every rubric axis is exercised by at least one item.

1. Cast an argument found in the wild into a `PF-###`, filling every `MUST`
   field, and name the fields the source left implicit.
2. Mark all fourteen audit axes with a stated reason each, and *compute* the
   verdict by the §6.3 rules rather than choosing it.
3. Assign a closed-list warrant token to every premise, and detect a `W-AUTH` or
   `W-REV` premise dressed as `W-SELF`.
4. Apply the MD5 paraphrase test and decide whether a conclusion is `REAL` or
   only `CONCEPTUAL`.
5. Apply the necessity test order (`NEC-LOG`, `NEC-CON`, `NEC-NOM`, `NEC-MET`)
   and catch conceptual necessity recorded as metaphysical necessity.
6. Detect an unlicensed change of `NEC-*` kind, `SCP-*` scope, or `PRI-*`
   relation, and state the `BR-###` that would license it.
7. Apply the MD11b reversal detector and grade `RG-THAT` where the middle is
   `EFFECT-SIGN`.
8. Produce a minimal `denial-set` and give, at its strongest, a named standing
   opponent's own reason for rejecting each member.
9. Weaken an overstrong conclusion to exactly what is licensed, writing both
   `established` and a non-empty `not-established`.
10. Exhibit a minimal repair and state what survives, or show why no repair
    preserves a `REAL` conclusion.
11. Detect a substantive premise hidden in a definition and promote it to a
    `PR-###` carrying its own warrant.
12. State the dependency edges a multi-step result consumes, and spot a forward
    reference or a cycle by inspection.

### 1.4 Register and structural model

An upper-level mathematics or logic text with restrained scholastic character.
Binding consequences:

1. Numbered environments carry the content. Definitions, propositions, lemmas,
   corollaries, demonstrations, objections, replies, specimens, and exercises
   are environments with ids, not paragraphs with topic sentences.
2. Every paragraph states a claim, defines a term, marks a distinction, supplies
   a warrant, applies a rule, raises an objection, replies, or instructs.
   *Reviewer test:* delete it; if nothing on that list is lost, it was filler and
   MUST be cut.
3. No rhetorical questions, no exhortation, no anticipatory summary ("we shall
   see that…"), no peroration. Second person is reserved for exercise
   instructions.
4. Scholastic character means the *apparatus* — objection and reply, named
   distinctions, explicit `QUA-SIMP`/`QUA-SEC` qualification — not the costume.
   Prohibited: faux-medieval ornament; a decorative *sed contra* where the
   objection and reply environments already run; untranslated Latin; a Latin
   term without a `TM-###` and an English gloss at first occurrence.
5. Historical material lives in `scholion` and in classified citations. No
   `steps` line ever depends on one.

### 1.5 Status of this specification

1. This document is the binding contract for every later lane. Where it and a
   later agent's editorial judgment conflict, it governs.
2. Chapter drafts, LaTeX documentation, and review reports cite it as
   `DOCUMENT-SPEC §n.m`, an enumerated rule as `DOCUMENT-SPEC §n.m (k)`, never
   by quoting spec prose without a locator.
3. **No local deviation.** An agent judging the spec wrong, blocking, or
   internally inconsistent MUST stop and file a spec-amendment request naming
   (a) the section, (b) the defect, (c) proposed replacement text, (d) what is
   blocked. Work resumes on the amended spec. A chapter that departs from the
   spec is defective regardless of its quality.
4. **Silence.** Where the spec is silent, an agent MAY decide locally only if
   the decision touches none of: the closed vocabularies, the identifier scheme,
   the audit axes and verdict rules, the layer rules, or the eight house rules.
   Any such decision MUST be recorded with its rationale and surfaced for
   ratification. Closed vocabularies are never extended locally.
5. Amendment is the only route by which this spec changes. A later agent's
   working notes do not amend it.
6. **Reference resolution (binding).** (a) Every section reference in this
   specification denotes a section *of this specification*, written `§n.m` or
   `DOCUMENT-SPEC §n.m`. (b) A reference written against the frozen spine's
   numbering is a defect and is rewritten using the resolution table below.
   (c) A submission citing a locator that does not resolve is rejected under
   §16.7 as a mechanical defect.

| Spine | This spec | Spine | This spec |
|---|---|---|---|
| §1.1 | §2.2 | §3.1 | §6.2 |
| §1.2 | §2.1.1 | §3.2 | §6.3 |
| §1.3 | §2.5 | §4.1, §4.2, §4.3, §4.4 | §3.9 |
| §2.2 | §4.2 | §5 | §11 |
| §2.3 | §4.3 | §6 | §10 |
| §2.4 | §2.1.2 | §7 | §5 |
| §2.5 | §4.1 and §10.1 | §8 | §17 |

7. **Illustrative identifiers.** An identifier appearing inside a schematic
   example, worked instance, or machine-readable sketch in this specification —
   §4.6, §9.9, §10.4, §11.7, §12.4–§12.5, §14.2 — is illustrative: it allocates
   nothing, binds no band, and is exempt from `LC-22` and from the
   forward-reference rules. Appendix A and §7.6 are not illustrative in this
   sense: they allocate in the `9##` band reserved by §7.4, and every rule
   binding a live id binds theirs.

### 1.6 Non-goals of the finished book

The book will not:

1. survey metaphysical positions, or present a position it does not audit;
2. narrate the history of philosophy, or make "what Aquinas held" a chapter
   objective;
3. defend a full cosmological argument at length, or treat natural theology as
   the destination rather than as late material on which the method is
   exercised;
4. let "proof of God" name a sequence of distinct claims, or deliver an
   attribute as a corollary of reaching a non-derivative principle (house
   rule 6);
5. present a revealed premise as a conclusion of natural reason, or admit a
   `W-REV` premise into an object of `kind: DEMONSTRATION` (house rule 4);
6. let a citation occupy a warrant slot (house rule 3);
7. settle every dispute it raises: `V-OPEN` is a legitimate terminal verdict;
8. persuade or produce assent: no axis may be marked down for the absence of
   persuasiveness;
9. teach formal logic, model theory, or mathematical technique for its own sake;
10. weaken nominalism, Humeanism, physicalism, modal fictionalism, grounding
    deflationism, or any analytic objection to make the working framework look
    stronger (house rule 7).

### 1.7 The eight house rules

These eight are the closed referent of every "house rule N" citation in this
specification, and of the phrase "the eight house rules" in §1.5(4) and §16.5.
Each names the axis or verdict that enforces it and the condition that detects
its breach.

1. Never blur the five-term chain of §1.1 — formal validity, soundness,
   philosophical warrant, metaphysical demonstration, metaphysical explanation —
   and never call an argument an explanation. *Axis* `DEM`; *detector* `UA-1`.
2. Never let a formally valid derivation count, by itself, as a metaphysical
   demonstration. *Verdict* `V-VALID-ONLY`; *detector* `UA-2`.
3. Never let a citation or an author's authority occupy a warrant slot: `W-AUTH`
   exists to be detected, never used. *Axis* `PRV`; *detector* `UA-3`.
4. Never admit a premise held on revelation into any proof object, and never
   present one as a conclusion of natural reason: `W-REV` likewise. *Axis*
   `PRV`; *detector* `UA-4`.
5. Never let a substantive disputed premise hide inside a definition, a term
   sense, or a distinction — promote underivable content to a `PR-###` carrying
   its own warrant. *Check* `LC-08`; *detector* `UA-5`.
6. Never let a phrase, a name, or a title collapse a plurality of distinct
   results into one — every attribute is a separate `PF-###` with an explicit
   `depends-on` edge. *Error class* `ER-604`; *detector* `UA-6`.
7. Never state a named rival below its own strongest published form.
   *Condition* MD9, *error class* `ER-705`; *detector* `UA-7`.
8. Never present a modern proof-engineering token as the historical theory's
   own concept, or project the apparatus backward onto Aristotle or Aquinas.
   The audit axes, proof-object schema, warrant tokens, rung ladder, error
   taxonomy, and all other apparatus of this specification are a pedagogical
   superstructure built over the tradition (§2.8), not the tradition itself.
   Historical claims are `CC-TEXT` under §13.2. *Detector* `UA-11`.

The numbering is normative: no later agent may renumber a rule, add a ninth,
or drop one.


## 2. What This Project Means by "Metaphysical Demonstration"

### 2.1 The governing definition

Binding, and not paraphrasable by any later agent:

> `A` is a metaphysical demonstration of `C` iff MD1–MD10; additionally `RG-WHY` iff MD11.

#### 2.1.1 The eleven conditions, verbatim and binding

This specification is self-contained: every condition, token, and test it binds
later agents to is printed in it, and no later agent is required to consult any
other document.

1. **MD1 Declared consequence.** Every step names its licensing rule and the
   lines it consumes, from a calculus named in `logic` (default: first-order
   logic with identity; modal systems named, e.g. `S5`, `T`). *Detector:* an
   unlabelled step. "Obviously follows" is not a logic.
2. **MD2 Sense fixity.** Every non-logical term occurring in two or more lines
   carries one `TM-###.n` sense selector at every occurrence, or is declared
   `PRD-ANA` with the shared ratio stated. *Detector:* substitute the declared
   sense everywhere; if a premise goes false or a step fails, MD2 fails.
3. **MD3 Existential discipline.** No term denotes by occupying subject position.
   Universals read `∀x(Fx → Gx)` with no existential import; any step needing
   `∃x Fx` cites a premise or prior `PR-###` asserting it. Definite descriptions
   are Russellian: "*the* first cause" may not be written until a uniqueness
   lemma is proved and cited. Constants enter only by existential instantiation
   citing that proposition's id. *Detector:* delete every nonemptiness premise;
   if the argument still purports to prove something exists, MD3 fails.
4. **MD4 Declared warrant.** Every premise carries exactly one token from §2.1.2.
5. **MD5 Real import.** `C` has `import: REAL`, and so does at least one
   load-bearing premise. *Paraphrase detector:* rewrite every metaphysical term
   in `C` as a claim about our concepts ("our concept of change requires…"). If
   the same premises support the rewrite with the same force, only a conceptual
   truth is established and MD5 fails.
6. **MD6 Modal integrity.** `C` carries no necessity kind stronger than the
   weakest link. Every change of `NEC-*` kind or `SCP-*` scope cites a bridge
   `BR-###` that carries its own warrant token and whose antecedent is discharged
   inside `A`. *Detector:* a conclusion token appearing in no premise and
   licensed by no cited `BR-###`.
7. **MD7 Non-circularity.** No premise's warrant presupposes `C`, or any id whose
   ledger record lists `C` in `depends-on`. The `depends-on` graph plus warrant
   edges is acyclic.
8. **MD8 Commensurate conclusion.** `established` restates `C` at exactly the
   licensed strength — same modality, scope, and subject, no wider and no
   narrower — and `not-established` names at least one nearby stronger claim not
   reached. `NONE` is inadmissible there.
9. **MD9 Dialectical exposure.** `denial-set` gives a minimal set of premises,
   definitions, or distinctions whose joint rejection blocks `C`; each member is
   load-bearing (removing it breaks a step); and for each, the text names a
   standing position that rejects it — nominalist, Humean, physicalist, grounding
   deflationist, modal fictionalist, or another named — with that position's own
   reason at its strongest. Giving a named opponent a weaker reason than that
   opponent's literature gives is `DIA` = `FAIL`, not a stylistic choice.
10. **MD10 Named middle.** `middle` names the term through which `C` is reached;
    `middle-kind` ∈ `FORMAL`, `MATERIAL`, `EFFICIENT`, `FINAL`,
    `PROPER-ATTRIBUTE`, `EFFECT-SIGN`. The middle belongs to the subject, and the
    attribute to the middle, *per se* — not by accidental co-occurrence.
11. **MD11 Grounding middle (`RG-WHY` only).** (a) The priority of `middle` to
    `C` is `PRI-GND`, declared. (b) *Reversal detector:* "`S` is `P` because `M`"
    is assertible and "`M` because `S` is `P`" is not; if both read equally well,
    `M` is a sign and the rung is `RG-THAT`. (c) The author exhibits a **stripped
    variant** — a valid derivation of the same `C` not routing through `M`, plus
    a statement of what it leaves unexplained — or shows that every valid route
    to `C` passes through `M`.

*Micro-example.* "This wall is illuminated; nothing illuminates it but the lamp;
therefore the lamp is on" is `RG-THAT` (`middle-kind: EFFECT-SIGN`). "The lamp is
on and the wall lies in its beam; therefore the wall is illuminated" is `RG-WHY`
(`middle-kind: EFFICIENT`, `PRI-GND`). Both are valid; only the second answers
*why*.

**Reading guide.** The table fixes how each condition is read at the point of use
and what the reader asks to test it. It is an aid, not a source: where the guide
and §2.1.1 differ, §2.1.1 governs.

| Cond. | Reader's operative question | Violation that usually escapes notice |
|---|---|---|
| MD1 | Which rule, consuming which lines? | A step licensed by a rhetorical connective in `L1-PROSE` and never rewritten in `L2-NUM`. |
| MD2 | Does one sense selector survive every occurrence? | A term drifting between a broad and a narrow sense across a chapter boundary, each use locally innocent. |
| MD3 | Which premise buys the existence claim? | "The" attached to a term before its uniqueness lemma; a `∀` premise silently read with import. |
| MD4 | Which of the nine §2.1.2 tokens, exactly one? | A premise whose warrant is stated as "standard" or "granted by all parties". |
| MD5 | Does the conceptual paraphrase carry the same force? | A conclusion true of our concepts, printed `import: REAL` because its vocabulary sounds ontological. |
| MD6 | For each step, is the modality of `to` no stronger, under the §10.3 force/kind/scope order, than the weakest modality among all lines in that step's `from`; and is `claim`'s modality no stronger than the weakest among the load-bearing premises (a premise is load-bearing iff deleting it makes some step fail)? | An unbridged `NEC-CON` → `NEC-MET` upgrade performed by the word "must". |
| MD7 | Does any premise's warrant presuppose `C`? | Circularity through a *definition* cited by a premise, not through the premise itself. |
| MD8 | Do `established` and `claim` say the same thing? | `not-established` filled with a claim nobody would make, in place of the nearby stronger one. |
| MD9 | What minimal denial blocks `C`, and who denies it? | A `denial-set` member attributed to a named opponent in a form that opponent's literature does not hold. |
| MD10 | Through what term is `C` reached? | A middle that co-occurs with the attribute rather than belonging to the subject *per se*. |
| MD11 | Does the "because" run one way only? | A `PRI-ONT` dependence recorded as `PRI-GND` because the two co-vary. |

**MD6 is a lower bound, never a membership test.** The presence of a token on any
premise not in the conclusion step's `from` set licenses nothing: a `NEC-MET`
premise idling elsewhere in the object does not entitle `claim` to `NEC-MET`.
Wherever §4.3, §4.8, §6.2's `MOD` row, `ER-301`, and `UA-9` are worded as
presence tests, that wording is superseded and read as this weakest-link test.

A proof object satisfying MD1–MD10 is a metaphysical demonstration whatever any
reader's reaction to it; failing one, it is not one, and no accumulation of the
others compensates.

#### 2.1.2 The closed warrant list

`W-SELF` (evident on analysis of its terms, analysis printed) · `W-DEM`
(established earlier; cites the `PR-###`) · `W-DEF` (unpacks a cited `DF-###`,
adds no substantive content) · `W-IND` (generalization from experience, inductive
base named) · `W-EMP` (particular empirical datum, source cited) · `W-HYP`
(assumed for reductio or conditional proof; MUST be discharged) · `W-POST`
(framework posit, accepted here, not proved here) · `W-REV` (accepted on
revelation) · `W-AUTH` (asserted by an authority).

`W-REV` and `W-AUTH` exist **to be detected, never used**. A proof object with a
`W-REV` premise is not a metaphysical demonstration at any rung: it is a
theological argument and MUST be labelled one. `W-AUTH` is never a warrant
anywhere; a canonical author's statement may occupy only `scholion` or a
classified citation. Both trigger `PRV` = `FAIL` in a proof object of any kind,
not only in a `DEMONSTRATION`.

The list is closed at nine. No section may add a token, rename one, or regloss
one; an author who needs a tenth files a spec amendment under §1.5(3).

### 2.2 The ladder of strictly increasing commitment

Each rung adds commitments to the one below and retains all of them.

| Rung | Asserts | Does **not** yet license | One-line diagnostic |
|---|---|---|---|
| `RG-VALID` | the shape is truth-preserving in the declared `logic` | any claim that a premise is true, that terms are univocal, or that anything exists | Every step names a rule that licenses it — and nothing else has been checked. |
| `RG-SOUND` | additionally, every premise is in fact true | any claim that the truth is *known* or citable | None: soundness is a fact about the world, so **the book never assigns this rung**. It stays on the ladder to name what warrant aims at and to block "warranted, therefore true". |
| `RG-WARRANTED` | MD1–MD4 with every warrant undefeated: each premise carries a printed, surviving reason | that anything *real* has been established, or that the conclusion is about the world rather than our concepts | Delete every premise whose warrant is `W-DEF`, `W-HYP`, `W-AUTH`, or `W-REV`; does a defended premise remain for every step? |
| `RG-THAT` | MD1–MD10: a real conclusion, modally commensurate, non-circular, dialectically exposed, reached through a named middle | any claim to have said *why* `C` holds, or to have exhibited the ground of `C` | Apply the MD5 paraphrase detector and the MD8 restatement; if `C` survives as a claim about things and `established` matches it, the rung is reached. |
| `RG-WHY` | MD1–MD11: the middle is prior to `C` by `PRI-GND`, with a stripped variant exhibited | that the *explanation* has been proved; the proof exhibits a grounding relation, it is not one | Run the reversal detector: if "`M` because `S` is `P`" reads as well as "`S` is `P` because `M`", the rung is `RG-THAT`. |

The fifth term of the governing chain, **metaphysical explanation**, sits off the
ladder: it is the relation `PRI-GND` between facts, assertible with no argument
present. An `RG-WHY` proof exhibits an explanation; it is not one. No section may
call an argument an explanation, or treat a bare grounding claim as an argument.

### 2.3 The gaps are real: five miniature cases

Each case clears the rung named and fails the next.

1. **`RG-VALID`, not `RG-SOUND`.** *p1:* whatever has parts was assembled. *p2:*
   this crystal has parts. *∴* it was assembled. `LOG: OK`; `p1` is false.
2. **`RG-SOUND`, not `RG-WARRANTED`.** *p1* (`warrant: W-AUTH`): every agent acts
   for an end. *p2:* this is an agent. *∴* it acts for an end. Suppose `p1` true:
   sound, and still failing MD4. `WAR: FAIL`, `PRV: FAIL`. Truth without a
   printable warrant is invisible to every audit the book runs.
3. **`RG-WARRANTED`, not `RG-THAT`.** From `DF-101` ("a potency is a capacity not
   now actualized") and `DF-102` ("to actualize is to bring a potency to act"),
   both premises `W-DEF`: "whatever is in potency is not actualized by itself".
   Warrants undefeated, shape valid — but the MD5 paraphrase ("our concept of
   potency requires…") is supported with identical force. `import: CONCEPTUAL`;
   verdict `V-VALID-ONLY`.
4. **`RG-THAT`, not `RG-WHY`.** *p1:* this ice is melting. *p2:* nothing here
   melts ice but a heat source. *∴* a heat source is present.
   `middle-kind: EFFECT-SIGN`. The reversal detector passes both ways, so the
   middle is a sign. `EXP: N/A`, rung `RG-THAT`, complete of its species.
5. **`RG-WHY` versus explanation.** "This substance's being conductive is
   grounded in its being metallic," asserted alone, is a `PRI-GND` claim on no
   rung whatever: it has no `steps`, hence not even `RG-VALID`. Explanation is
   cheap to assert and expensive to demonstrate; the ladder measures the
   latter only.

Case 3 carries house rule 2: nothing in the passage from a valid derivation to a
warranted one crosses from concepts to things. Only MD5 does that.

### 2.4 Demonstration *that* and demonstration *why*

The book's target is `RG-WHY`; a proof object claiming it prints MD11's three
sub-conditions in full, stripped variant included.

`RG-THAT` is nonetheless a **completed result**, not a failed `RG-WHY`, and MUST
NOT be graded as one (`EXP` is `N/A`, never `FLAG`, when `rung: RG-THAT`). It is
the accepted **`RG-THAT` stopping case** in exactly these cases, extensible
only by addition:

- the subject is knowable only through its effects, so no `PRI-GND` middle is
  available to us even if one obtains (`middle-kind: EFFECT-SIGN`);
- the middle is a `PROPER-ATTRIBUTE` convertible with the subject, where the
  reversal detector is expected to pass both ways;
- Stage A and Stage B specimens, whose pedagogical point is structural.

**The stopping case is never self-certifying.** Every `kind: DEMONSTRATION` carrying
`rung: RG-THAT` MUST state, as the first clause of its mandatory `OV-EXPL` entry
in `not-established`, which of the three cases applies — or, where none does,
that a grounding middle may exist and is not exhibited here, naming the candidate
ground (a `TM-###`, a `PR-###`, or a described relation) and the chapter.section
or `NOT-IN-BOOK` where it would be treated. An `RG-THAT` demonstration whose
`middle-kind` is neither `EFFECT-SIGN` nor `PROPER-ATTRIBUTE` and which makes no
such statement is `DEM: FAIL` routed to `V-REPAIR`. This is the only `DEM` test
that fires on an *under*-claim rather than an over-claim; it exists because `EXP`
is mandatorily `N/A` at `RG-THAT` and can therefore detect nothing there. The
word *terminus* is reserved in this specification to the Stage F non-derivative
principle (§8.10) and is never used of an `RG-THAT` stopping point.

A claimed `RG-WHY` with an achieved `RG-THAT` is `DEM: FAIL` routed to
`V-REPAIR`; the repair is reclassification plus withdrawal of every explanatory
phrase in the prose.

### 2.5 What the project refuses to build into the definition

The definition excludes: reader certainty; opponent assent; uncontested premises;
premises self-evident to everyone; an independently established framework;
uniqueness or minimality of the proof; symbolization; univocity; machine-checking;
persuasiveness; elegance; brevity; novelty; endorsement by any canonical author;
that no objection remain open.

Each is a fact about audiences, about rival proofs, or about presentation; the
definition quantifies over the argument and the world only. Admitting any would
make one proof object change rung when its reader changed. §7.1(3)'s
negative-closure list is a subset of this one, which governs.

**The binding consequence.** A demonstration can satisfy MD1–MD11 and persuade no
one. Persuasion is therefore never evidence of demonstrative success, and failure
to persuade is never a defect in the proof. No axis may be marked `FLAG` or
`FAIL` for the absence of anything on this list, and no verdict may cite one.

*Reviewer detector.* Grep audit tables, `replies`, and margin callouts for
`compelling|convincing|undeniable|no one can (deny|doubt)|any rational (agent|person) must|everyone (must )?(admits?|grants?)|self-evident to all`. Each hit is a defect
unless inside a quoted opponent position or a reported `OB-###`. Symmetrically,
weakening `established` because an opponent remains unconvinced is an `SCO`
defect in the other direction.

### 2.6 The reflexive problem

The book uses metaphysical vocabulary to teach the evaluation of metaphysical
arguments. What keeps this non-circular is a strict separation of two registers,
enforced by where a term may appear in a `PF-###`:

- **Framework-neutral machinery** — the axis tokens, rungs, warrant tokens,
  identifier scheme, layer tokens, ledger checks, and the record schema itself.
  Test of neutrality, and it is a real test: applying the machinery to any proof
  object entails no `PR-###` with `import: REAL`. Machinery classifies and
  detects; it never asserts about things. Machinery vocabulary appears in
  `audit`, in margin callouts, and in `not-established`; it may **not** appear in
  `premises` or `steps` without first being minted as a `TM-###`/`DF-###` and
  given a warrant token like any other content.
- **Framework-dependent commitment** — act and potency, essence, substance, real
  distinction (`DK-REAL`), grounding (`PRI-GND`), real necessity (`NEC-MET`),
  essentially ordered series (`SER-ESS`). Every one enters the object language as
  an id with `framework` set and, where posited rather than proved,
  `warrant: W-POST`.

Three tokens straddle the boundary: `PRI-GND`, `NEC-MET`, `DK-VIRT`. Each is
neutral as a *classification slot* (any position can be asked which slot it
takes) and framework-dependent as an *assertion* (that this pair does stand in
`PRI-GND`). Where the book relies on the assertion it prints an `OB-###` from the
position rejecting the slot itself — grounding deflationism, modal
conventionalism — with a reply that may concede.

*Detector.* A term occurring in a printed audit row or margin callout and also in
`premises` without a `TM-###` id in `lexicon` is a register violation
(`FRM: FAIL`). The marking policy proper — including demonstration *within* a
framework versus one that *establishes part of* it — belongs to §14 and is not
duplicated here.

### 2.7 Controlled vocabulary: no competing sense of "demonstration"

No later agent may introduce a second sense of the words below. The list is
closed; a licensed use must satisfy the stated condition, and every other use is
a defect.

| Word | Licensed use only | Never |
|---|---|---|
| demonstration / demonstrate | (i) `kind: DEMONSTRATION`; (ii) the glosses "metaphysical demonstration *that*/*why*" naming `RG-THAT`/`RG-WHY`; (iii) the definiendum of §2.1 | as a synonym for argument, derivation, case, or presentation |
| proof | a `PF-###` proof object, or the fixed compounds "proof object", "proof-audit", "proof grammar" | "proof of God", "proof that God exists", or any phrase naming a *sequence* of claims (house rule 6) |
| prove / proves / proven / proved | inside the fixed compound nouns already listed for *proof*, and inside a quoted `CC-TEXT` passage or an objection stated in an opponent's voice | as a verb whose subject is a `PF-###`, a `PR-###`, a chapter, or the book |
| establishes | content appearing verbatim in `established`, in a sentence naming the object's id and printing its achieved rung (§6.2.1), and only where that object's computed verdict is `V-PASS`, `V-PARTIAL`, or `V-OPEN`; where the verdict is `V-OPEN` or the object's `framework` is not `NEUTRAL`, the sentence additionally carries the §16.4(2) conditionality clause | of anything in `not-established`; of a `W-POST` premise; of any object whose verdict is `V-FATAL`, `V-REPAIR`, or `V-VALID-ONLY` |
| shows | subject is a table, figure, or an id-bearing proof object, and a rung token appears in the same sentence | of a bare `PRI-GND` claim, or as a hedge meaning "suggests" |
| entails | on a `steps` line naming the rule that licenses it, or inside a stated countermodel | of a whole argument |
| implies | — | never licensed anywhere |
| explains / explanation | of a `PRI-GND` relation between facts, and of the `middle` of an object whose *achieved* rung is `RG-WHY` | of an argument, a chapter, a theory, or an account |
| warrants / warranted | of a premise carrying a §2.1.2 token, or of the rung `RG-WARRANTED` with that token printed in the same sentence | of a conclusion, or of a `PR-###` |

For the three verdicts excluded from "establishes", the licensed sentence is,
respectively: `V-FATAL` — "nothing is established, at any rung"; `V-REPAIR` —
"nothing is established until the exhibited repair is made"; `V-VALID-ONLY` — "a
conceptual result is established and no claim about things is". A
`V-VALID-ONLY` object's `conceptual-result` may be spoken of as established only
with the qualifier "conceptually". The fixed phrases "establishes part of the
framework" and "establishing part of it", required by the §14.3 framework-role
vocabulary, are licensed uses of "establish" and are not adjudicated against this
table.

Licensed weaker verbs, short of a rung: *argues*, *supports*, *renders
plausible*, *is consistent with*, *motivates*. Licensed inside `steps`: *yields*,
*licenses*. An author needing a new sense mints a `TM-###` with numbered senses
and never overloads a reserved word.

*Enforcement.* A reviewer runs, over every authored file:

```
grep -nEi '\b(demonstrat|proofs?|prove[nsd]?|establish|shows?|entail|impl(y|ies|ied)|explain|explanation|warrant)' <files>
```

and adjudicates each hit against the table. Two further greps are mandatory:
`grep -nEi 'proof of (god|the)'` (house rule 6 — each hit must resolve to one
`PF-###` with an explicit `depends-on` edge), and the same reserved-word grep
restricted to files containing `W-REV` or `W-AUTH` (house rules 3 and 4). A hit
surviving adjudication is `PRV: FAIL` or `DEM: FAIL` by which word was abused.

### 2.8 The Historical Theory of Demonstration: Reconstruction and Heritage

#### 2.8.1 Why this section exists

The definition of metaphysical demonstration in §2.1, the audit rubric in §6,
the error taxonomy in §7, and the entire proof-object schema of §4 are modern
pedagogical apparatus. They are not the historical theory of demonstration.
This section reconstructs the historical theory accurately, so that later
agents can present it without retrojecting our apparatus onto it, and
explicitly labels the relationship between the two.

The distinction this section enforces is:

```text
historical theory of demonstration (Aristotle, Aquinas, the tradition)
    != modern proof-engineering apparatus (this specification)
```

The apparatus is built over the tradition. It is inspired by it, designed to
teach its distinctions, and answerable to it. It is not identical to it. House
rule 8 (§1.7) enforces this distinction throughout the book.

#### 2.8.2 Aristotle's apodeixis

The following reconstruction is binding for all `CC-TEXT` claims about
Aristotle. Every doctrine is stated with its Bekker locus; the dossier at
`.scratch/historical/aristotle-dossier.md` provides citation-level detail,
verbatim quotation, and scholarly dispute notes. A later agent presenting
any of these doctrines in the book cites the locus per §13.3.

1. **Epistēmē and its object.** We possess unqualified scientific knowledge
   (ἐπιστήμη, *epistēmē*) of a thing when we know the cause on which the fact
   depends, as the cause of that fact and of no other, and further that the
   fact cannot be otherwise. The object of scientific knowledge is necessary.
   (Post. An. I.2, 71b8–16; Nic. Eth. VI.3, 1139b18–22.)

2. **Apodeixis defined.** Demonstration (ἀπόδειξις, *apodeixis*) is a
   syllogism productive of scientific knowledge. Its premises must be: (1)
   true, (2) primary/first, (3) immediate, (4) better known than the
   conclusion, (5) prior to the conclusion, (6) causes of the conclusion.
   (Post. An. I.2, 71b17–72a8.)

3. **Principles (ἀρχαί).** A basic truth is an immediate proposition — one
   with no other prior to it. Theses include axioms (common to multiple
   sciences), hypotheses (asserting existence or non-existence of a subject),
   and definitions. Demonstration cannot be circular and cannot regress
   infinitely. Not all knowledge is demonstrative; knowledge of immediate
   premises is independent of demonstration. (Post. An. I.2–3, 72a8–73a20;
   I.10, 76b23–77a9.)

4. **Praecognita.** All instruction proceeds from pre-existent knowledge. The
   text distinguishes two kinds with a combined third case: (1) admission of
   the fact (ὅτι ἔστι, *hoti esti*), (2) comprehension of the meaning (τί
   τὸ λεγόμενόν ἐστι), (3) sometimes both. The later scholastic threefold
   framing (*an sit* / *quid sit* / *quia est*) is tradition, not the
   Aristotelian text. (Post. An. I.1, 71a11–17.)

5. **Per se predication and the commensurate universal.** Essential (*per
   se*, καθ' αὑτό) attributes belong to their subject either because the
   subject's definition contains the attribute or because the attribute's
   definition contains the subject. A commensurately universal (καθόλου)
   attribute belongs to every instance of its subject, and to every instance
   essentially and as such. The middle term must be *per se*, not accidental.
   (Post. An. I.4, 73a21–74a3; I.6, 74b5–75a17.)

6. **The middle term as cause.** The middle term (μέσον, *meson*) is the
   cause (αἰτία, *aitia*). The four causes — formal, material (necessitating),
   efficient, final — can each serve as the middle. Definition can serve as
   the middle: when we know the fact we seek the reason, and the reason is the
   middle, which is a definition. (Post. An. II.11, 94a20–95a9; II.8,
   93b22–94a19.)

7. **Propter quid vs quia (τοῦ διότι vs τοῦ ὅτι).** Knowledge of the reasoned
   fact (*propter quid*) differs from knowledge of the fact (*quia*). The
   distinction arises: (1) when the premises are not immediate; (2) when the
   premises are immediate but the better known of two reciprocals is taken as
   middle instead of the cause; (3) when the middle falls outside major and
   minor; (4) across different sciences (subalternation). Standard examples:
   the planets are near because they do not twinkle (*quia* — they do not
   twinkle because they are near, not vice versa); the moon is spherical
   because it waxes in a certain manner (*quia* — reversal gives *propter
   quid*). The first figure (Barbara) is the most scientific. (Post. An. I.13,
   78a22–79a16; I.14, 79a17–32.)

8. **Necessity of premises.** Demonstrative knowledge rests on necessary
   basic truths. There is no demonstration of the accidental or of chance.
   Demonstration is of what holds always or for the most part. (Post. An.
   I.6, 74b5–75a17; I.8, 75b21–36; I.30, 88a5–17.)

9. **No crossing of genera.** Demonstration stays within one science's
   subject genus. The theorem of one science cannot be demonstrated by
   another unless the sciences are related as subordinate to superior
   (subalternation: optics/geometry, harmonics/arithmetic). (Post. An. I.7,
   75a38–75b20; I.9, 76a26–76b22; I.13, 78b34–79a16.)

10. **How principles are grasped.** The basic premises are not known by
    demonstration. Nous (νοῦς) grasps the first principles; induction
    (ἐπαγωγή, *epagōgē*) is the process by which the universal comes to be in
    the soul from perception of particulars. (Post. An. II.19, 99b18–100b17;
    Nic. Eth. VI.6, 1140b31–1141a8.)

11. **Dialectic and demonstration.** Dialectical reasoning reasons from
    endoxa (ἔνδοξα, reputable opinions). Dialectic is not demonstration
    because its premises are not necessary, primary, or causes. Dialectic
    is useful for discussing the ultimate bases of principles. (Topics I.1,
    100a18–100b23; I.2, 101a25ff.)

12. **Aristotle's own practice.** The Analytics model of finished science
    does not describe Aristotle's own investigative treatises, which proceed
    by dialectical inquiry and aporia. Barnes (1969) argued that demonstration
    is for teaching and exposition, not discovery. This is disputed. (Barnes,
    "Aristotle's Theory of Demonstration," *Phronesis* 14, 1969, 123–152.)

13. **Metaphysics as a science.** There is a science of being qua being (ὂν
    ᾗ ὄν). The many senses of "being" are related to one central point (πρὸς
    ἕν, *pros hen*), not by mere ambiguity. The principle of
    non-contradiction is not demonstrable but defensible by elenchus. (Metaph.
    Gamma 1–4, 1003a21–1011a5.)

14. **The four questions.** The kinds of question are four: (1) whether the
    connection is a fact (*hoti*), (2) what is the reason (*dioti*), (3)
    whether a thing exists (*ei esti*), (4) what is the nature (*ti esti*).
    The middle is the cause. We cannot know what a thing is without knowing
    that it is. (Post. An. II.1, 89b21–90a35.)

#### 2.8.3 Aquinas's adaptations

The following reconstruction is binding for all `CC-TEXT` claims about
Aquinas. The dossier at `.scratch/historical/aquinas-dossier.md` provides
citation-level detail.

1. **Reception of the Posterior Analytics.** The *Expositio libri
   Posteriorum* is Aquinas's line-by-line commentary on the *Posterior
   Analytics*. It follows Aristotle closely, dividing into lectiones that
   track the Aristotelian chapters. (In PA, lib. I–II; Leonine ed., Romae
   1882.)

2. **Scientia and its subject.** A science (*scientia*) is specified by its
   subject (*subiectum*), determined by its formal ratio. Metaphysics is a
   *scientia* whose subject is *ens commune* (being in common). (In Metaph.
   prooem.; Super Boet. De Trin. q.5 a.1, a.4.)

3. **Duplex est demonstratio.** There are two kinds of demonstration:
   *propter quid* (through the cause, *per causam*) and *quia* (through the
   effect, *per effectum*). God's existence is demonstrable *quia*, from
   effects. When the cause is demonstrated through the effect, the effect
   takes the place of the definition of the cause (*effectus loco
   definitionis causae*). (ST I q.2 a.2 corp. and ad 2.)

4. **Medium demonstrationis.** The middle of a demonstration *propter quid*
   is the cause, which is the *quod quid est* (the essence). When the *quid
   est* is unavailable — as with God — the *quid significet nomen* (the
   meaning of the name, imposed from effects) takes its place. (In PA II
   lect. 1, 7, 9; ST I q.2 a.2 ad 2; Super Boet. De Trin. q.6 a.4 ad 2.)

5. **Praecognita.** Before a conclusion can be demonstrated, certain things
   must be pre-known: the principle, the subject, and the passion. Of each,
   there is *quia est* (that it is) and *quid est* (what it is). The *quia est*
   precedes the *quid est*: non-beings have no definitions. (In PA I lect. 2;
   ST I q.2 a.2 ad 2.)

6. **Per se nota.** A proposition is *per se nota* (self-evident) in two ways:
   *quoad se* (in itself) and *quoad nos* (to us). "God exists" is *per se
   nota quoad se* but not *quoad nos*, because we do not know what God is.
   This doctrine is deployed against Anselm. (ST I q.2 a.1 corp. and ad 2;
   SCG I cc. 10–11.)

7. **Analogy.** Nothing is predicated univocally of God and creatures. Names
   are said *analogice* (*secundum proportionem*). The *res significata* (the
   perfection signified) is properly said of God; the *modus significandi*
   (the mode of signifying) belongs to creatures. The analogical middle
   problem: if terms are neither univocal nor purely equivocal, a syllogism
   using such a term risks the four-term fallacy (*quaternio terminorum*).
   This problem is not explicitly thematized by Aquinas but is a construction
   of the later tradition (Cajetan, *De nominum analogia*, 1498). (ST I q.13
   a.3, a.5.)

8. **Sacra doctrina and praeambula fidei.** Sacred doctrine is a *scientia*
   that proceeds from principles known by a higher science (the science of God
   and the blessed). Philosophical authorities are used as "extraneous and
   probable arguments" (*quasi extraneis argumentis*). What is demonstrable
   by natural reason about God is a *praeambulum ad articulos*, not an article
   of faith. (ST I q.1 a.2; q.1 a.8 ad 2; q.2 a.2 ad 1; SCG I cc. 3–9.)

9. **Per se vs per accidens causal series.** In efficient causes it is
   impossible to proceed to infinity *per se* (essentially ordered: each
   cause essentially required for the effect). But *per accidens* (accidentally
   ordered: a member's causing does not require the prior member's concurrent
   causing) infinite regress is not impossible. (ST I q.46 a.2 ad 7.)

10. **Resolutio and compositio.** The two orders of inquiry: *via
    inventionis*/*compositio* (from causes to effects) and *via
    iudicii*/*resolutio* (from effects to causes). Metaphysics uses
    *separatio* (negative judgment, e.g., "God is not a body"), not
    *abstractio*, because its objects are separate from matter in being. The
    later manual tradition conflates *separatio* with a "third degree of
    abstraction" — this is a manual-layer reading, not the text's formulation.
    (Super Boet. De Trin. q.5 a.3; q.6 a.1.)

11. **The Five Ways.** Aquinas calls them *viae* (ways), not *probationes*
    (proofs) or *demonstrationes*. Each concludes to a terminal phrase
    identifying what "all name God" — *an sit* (that something is), not *quid
    sit* (what it is). The divine attributes (simplicity, perfection,
    goodness, etc.) are established in separate questions (ST I qq.3–11),
    not as corollaries of the Ways. In SCG I, after the demonstration of God's
    existence (c.13), Aquinas proceeds through the *via remotionis* (c.14) to
    establish attributes one by one. (ST I q.2 a.3 corp.; ST I qq.3–11; SCG I
    cc.14–28.)

12. **The later scholastic manual tradition.** The Neo-scholastic manuals
    (Gredt, Garrigou-Lagrange, Maritain, etc.) systematized the doctrine of
    demonstration in a formalized way that differs from the original texts: (a)
    the manuals standardize "three degrees of abstraction" where Aquinas
    distinguishes *separatio* from *abstractio*; (b) the manuals present the
    Five Ways as "proofs" in formal syllogistic dress where Aquinas presents
    them as *viae* in compressed form; (c) the manuals systematize analogy
    following Cajetan's technical distinctions where Aquinas's own treatment
    is less formalized.

13. **Modern scholarly disputes.** A careful author must not paper over: (a)
    whether Aquinas's *quia* demonstration of God satisfies Aristotle's own
    conditions on *apodeixis* (Kenny, *The Five Ways*, 1969; Wippel, *The
    Metaphysical Thought of Thomas Aquinas*, 2000; Feser, *Five Proofs*,
    2017); (b) whether analogical middles can carry syllogistic weight
    (Cajetan; Hochschild, *The Semantics of Analogy*, 2010); (c) whether
    metaphysics can be a demonstrative science on the Aristotelian model at
    all (being is not a genus); (d) whether the Ways are complete
    demonstrations or *viae* that initiate a larger inquiry completed through
    the *via remotionis* and separate attribute-demonstrations.

#### 2.8.4 The Heritage Declaration

**Binding on every later agent.** The modern proof-engineering apparatus of
this specification — the warrant ladder (§2.2), the eleven MD conditions
(§2.1.1), the nine warrant tokens (§2.1.2), the fourteen audit axes (§6.2),
the six verdicts (§6.3), the proof-object schema (§4), the error taxonomy
(§7), the margin annotation grammar (§11), the dependency ledger (§10), and
the exercise system (§9) — is a **pedagogical superstructure** built over the
historical theory of demonstration reconstructed in §2.8.2 and §2.8.3.

The relationship between the apparatus and the tradition is one of
**pedagogical inheritance, not historical identity**:

1. The apparatus is **inspired by** the tradition. The rung ladder answers
   to Aristotle's distinction between valid syllogism, knowledge of the
   fact, and knowledge of the reasoned fact. The middle-term requirement
   (MD10) answers to Aristotle's doctrine that the middle is the cause. The
   *quia*/*propter quid* distinction answers to the `RG-THAT`/`RG-WHY`
   distinction. The warrant tokens answer to the tradition's concern for how
   premises are known.

2. The apparatus is **not identical to** the tradition. Aristotle's
   *apodeixis* is a syllogism producing *epistēmē*; our proof object is a
   record schema producing an audit verdict. Aristotle's six conditions on
   premises are not our eleven MD conditions. Aquinas's *duplex est
   demonstratio* is not our rung ladder. The audit axes have no historical
   antecedent. The error taxonomy is modern. The margin annotation grammar is
   modern.

3. The apparatus is **answerable to** the tradition. Where a modern token
   maps to a historical concept, the mapping is partial and the disanalogy is
   stated (§2.8.5). No later agent may present a modern token as the "real
   meaning" of a historical concept, or project the apparatus backward onto
   Aristotle or Aquinas as though they had been doing proof auditing all
   along.

4. **Historical claims are `CC-TEXT`.** Every claim about what Aristotle or
   Aquinas held, said, or meant is a textual/historical claim under §13.2,
   carrying a full locus per §13.3, and occupying a `scholion` or historical
   prose — never a warrant slot, a premise, or a definition. The
   reconstruction in §2.8.2–§2.8.3 is the binding summary; the dossiers
   provide the citation-level detail.

#### 2.8.5 Concordance: modern apparatus and historical theory

The following table maps modern tokens to their historical antecedents. Each
entry states the overlap and the disanalogy. The table is **not** an
identification; it is a concordance with stated limits.

| Modern token | Historical antecedent | Overlap | Disanalogy |
|---|---|---|---|
| `RG-VALID` | valid syllogism (Aristotle, *Prior An.*) | both name truth-preservation of shape | Aristotle's syllogistic is term logic; our `logic` field names any calculus |
| `RG-THAT` | *demonstratio quia* (Aristotle, *Post. An.* I.13; Aquinas, ST I q.2 a.2) | both proceed from effects to the fact of the cause | our rung is a pedagogical grade on a ladder; Aristotle's *quia* is one mode among several, not a "rung" |
| `RG-WHY` | *demonstratio propter quid* (Aristotle, *Post. An.* I.13; Aquinas, ST I q.2 a.2) | both require the cause as middle, showing why | our MD11 grounding test is a modern reconstruction; Aristotle's *propter quid* requires the middle to be the cause and prior *simpliciter* |
| `middle` / `middle-kind` | μέσον / *medium demonstrationis* (Aristotle, *Post. An.* II.11; Aquinas, In PA II) | both name the term through which the conclusion is reached | our `middle-kind` taxonomy (`FORMAL`, `MATERIAL`, `EFFICIENT`, `FINAL`, `PROPER-ATTRIBUTE`, `EFFECT-SIGN`) is a modern classification; Aristotle's four causes as middles do not map one-to-one |
| `W-SELF` | *per se notum quoad se* (Aquinas, ST I q.2 a.1) | both name self-evidence from analysis of terms | our warrant system is a nine-token classification; Aquinas's *per se notum* is a two-way distinction (*quoad se* / *quoad nos*) |
| `W-DEM` | demonstrated premise (Aristotle, *Post. An.* I.2) | both name a premise established by prior demonstration | our `W-DEM` cites a `PR-###` id; Aristotle's demonstrative premise is established by a prior demonstration in the same science |
| `W-POST` | hypothesis (Aristotle, *Post. An.* I.2, 72a19); *positio* (Aquinas) | both name a premise assumed, not proved, within a science | our `W-POST` marks framework posits with a rival register; Aristotle's hypothesis asserts existence of the subject genus |
| `W-REV` | — | no historical antecedent in the demonstrative theory | our token exists to detect revealed premises, a concern arising from *sacra doctrina*'s separation from philosophy (Aquinas, ST I q.1 a.2, q.2 a.2 ad 1), not from the demonstrative theory itself |
| `W-AUTH` | — | no historical antecedent | our token exists to detect appeal-to-authority, a concern of the `PRV` axis, not of the demonstrative theory |
| `MD2` (sense fixity) | — | no direct antecedent | Aristotle requires *per se* predication, not sense selectors; the concern with equivocation is traditional but the mechanism is modern |
| `MD3` (existential discipline) | — | no direct antecedent | Aristotle's hypotheses assert existence; our Russellian descriptions and existential-import declarations are modern logic |
| `MD5` (real import) | *res significata* / *modus significandi* (Aquinas, ST I q.13 a.3) | partial: both distinguish the thing signified from the mode | our MD5 paraphrase test is a modern test for conceptual vs. real import; Aquinas's distinction concerns analogical predication of God |
| `MD6` (modal integrity) | necessity of premises (Aristotle, *Post. An.* I.6) | both require that the conclusion's necessity be earned | our weakest-link test and bridge system are modern; Aristotle requires necessary premises but has no bridge rules |
| `MD9` (dialectical exposure) | endoxa (Aristotle, *Topics* I.1) | partial: both name the opponent's position | our `denial-set` is a proof-object field; Aristotle's endoxa are premises for dialectical reasoning, not a field of a demonstration |
| `MD10` (named middle) | middle term as cause (Aristotle, *Post. An.* II.11) | both require the middle to be *per se*, not accidental | our `middle-kind` taxonomy is modern; Aristotle's four causes as middles are not classified into our six kinds |
| `MD11` (grounding middle) | *propter quid* through the cause (Aristotle, *Post. An.* I.13) | both require showing why through the cause | our `PRI-GND` and stripped-variant test are modern; Aristotle's requirement is that the middle be the cause and prior *simpliciter* |
| `PRI-GND` | — | no direct antecedent in the demonstrative theory | grounding is a contemporary metaphysical relation; Aristotle's causation is not identical to modern grounding |
| `SER-ESS` / `SER-ACC` | *per se* / *per accidens* causal series (Aquinas, ST I q.46 a.2 ad 7) | both distinguish essentially from accidentally ordered series | our concurrency test is a modern reconstruction; Aquinas's distinction is stated in the *ad 7* without a formal test |
| `DK-REAL` / `DK-VIRT` / `DK-NOM` | real distinction / virtual distinction / distinction of reason (scholastic tradition) | both classify distinctions by ontological status | our three-valued scheme with a binding test order is a modern reconstruction; the tradition's distinctions are not formally tri-valued in the same way |
| `PRD-ANA` | *analogia* / *secundum proportionem* (Aquinas, ST I q.13 a.5) | both name analogical predication with a stated ratio | our `PRD-ANA` is a proof-object field; Aquinas's analogy concerns divine names, not a general predication mode |
| `SCP-CMP` / `SCP-DIV` | — | no direct antecedent | the composite/divided distinction is medieval (*de dicto* / *de re*) but our scope tokens are modern modal logic |
| Fourteen audit axes | — | no historical antecedent | the audit rubric is a modern pedagogical instrument; Aristotle's demonstrative theory has no "axes" |
| Six verdicts | — | no historical antecedent | the verdict system is a modern classification of argument outcomes |
| Error taxonomy (§7) | — | no historical antecedent | the error taxonomy is a modern diagnostic instrument; the tradition's fallacy lists (Aristotle, *Sophistical Refutations*) are not our `ER-###` classes |

**How to use this table.** A chapter author presenting the historical theory
(Chapter 0, §8.2a) cites the historical antecedent by its own name and locus,
not by the modern token. A chapter author using the modern apparatus cites it
by its own token, not as "what Aristotle called..." The concordance table
exists so that both authors know the relationship and its limits.

#### 2.8.6 What this section forbids

1. **No retrojection.** No later agent may present a modern token as the
   historical theory's own concept, or write as though Aristotle or Aquinas
   had been using the audit rubric, the proof-object schema, or the error
   taxonomy. "Aristotle's MD10" is a defect; "Aristotle's requirement that the
   middle term be the cause" is not.

2. **No silent equation.** The §3.2 Latin forms table maps *demonstratio quia*
   to `RG-THAT` and *demonstratio propter quid* to `RG-WHY`. This mapping is a
   concordance, not an identity. The historical terms name a distinction
   within Aristotle's theory of demonstration; the rung tokens name grades on
   a modern pedagogical ladder. A later agent writing "Aquinas's
   *demonstratio quia* is our `RG-THAT`" MUST add "in the sense that..." and
   state the overlap, or cite §2.8.5.

3. **No apparatus in historical voice.** When presenting the historical
   theory (Chapter 0, §8.2a; scholions; `CC-TEXT` passages), the apparatus
   tokens do not appear. Aristotle's six conditions are not "MD1–MD6"; they
   are "true, primary, immediate, better known, prior, and causes of the
   conclusion." Aquinas's *duplex est demonstratio* is not "the
   `RG-THAT`/`RG-WHY` distinction"; it is "demonstration through the cause and
   demonstration through the effect."

4. **No tradition without citation.** Every claim about what the tradition
   held is a `CC-TEXT` claim under §13.2. The reconstruction in §2.8.2–§2.8.3
   is the binding summary; where it differs from a later agent's reading, the
   later agent files an amendment under §1.5(3).


## 3. Glossary of Methodological Terms

### 3.1 Status of this glossary

**G-R1 (single home).** A term is load-bearing if an audit mark, verdict,
ledger check, or step of any `PF-###` turns on which sense is meant. Every such
term is defined here **exactly once**; no later section may redefine, extend, or
narrow an entry. *Detection:* grep the term outside §3; a second gloss attached
("by X we mean…") breaks the rule.

**G-R2 (status is mandatory).** Every entry ends with `Status:` valued
`NEUTRAL` or `AT`, reusing the spec's `framework` vocabulary (§4.2).
`NEUTRAL` = framework-neutral machinery a nominalist, Humean, physicalist, or
grounding deflationist can use to audit their own arguments while conceding
nothing. `AT` = a framework-dependent metaphysical commitment
(Aristotelian-Thomistic unless another framework is named); every `AT` entry
**MUST** name a live tradition that rejects or reconstrues it, or carry an
explicit *(inherits N)* or *(contrast term of N)* pointer to a numbered entry
that names one; and an `AT` term in a `premises` subrecord forces
`framework: AT` plus `contested: true` unless that premise is independently
demonstrated.

**G-R3 (no smuggling).** No entry makes a substantive metaphysical thesis true
by definition. A term with both a schematic and a loaded use gets **two numbered
entries**, cited by number at every point of use: pairs 6/7, 10/11, 13/14,
29/30, 37/38.

**G-R4 (loaded dependency).** A `NEUTRAL` entry whose conditions quantify over
`AT` notions carries a `Loaded dependency:` line. It remains neutral machinery;
the line is a pointer for the `FRM` axis.

### 3.2 Latin forms (closed list)

Glossed once; thereafter the **canonical form** is the only permitted printing.
A retired Latin form may reappear only inside a quotation or a `scholion`.

| Latin | English gloss | Canonical form |
|---|---|---|
| *per se* | in virtue of what the thing is / not incidentally | *per se* (italic Latin; retained) |
| *per accidens* | incidentally, by co-occurrence | *per accidens* (italic Latin; retained) |
| *demonstratio quia* | demonstration *that* (historical) | historical antecedent of `RG-THAT`; concordance at §2.8.5, not an identity |
| *demonstratio propter quid* | demonstration *why* (historical) | historical antecedent of `RG-WHY`; concordance at §2.8.5, not an identity |
| *simpliciter* | without qualification | `QUA-SIMP` |
| *secundum quid* | in a stated respect | `QUA-SEC` |
| *ratio* | the account answering "what is it?" | "account" |
| *esse* | the act of existing | "act of existing" |
| *ens* | a being | "a being" |
| *actus purus* | pure act | "pure act" |

Only *per se* and *per accidens* survive as Latin: English "essential" and
"accidental" collide with entries 20–21 and 25–26.

### 3.3 Argument status

**1. validity.** The conclusion cannot be false with all premises true, under
the calculus named in `logic`. A property of *shape*. *Confused with:* soundness
(2); warrant (3); demonstration (4). *Test:* uniformly reinterpret every
non-logical term; if a countermodel appears, invalid. *Status:* `NEUTRAL`.

**2. soundness.** Validity plus the actual truth of every premise. A property of
the world, not of a text. *Confused with:* validity (1); `V-PASS`. *Test:* no
audit certifies it; ask which premise could still be false with every axis at
`OK`, and answering "none" is itself the error. *Status:* `NEUTRAL`.

**3. warrant.** The stated, defeasible entitlement to assert a premise, drawn
from the closed list of nine printed at §2.1.2. Warrant attaches to premises;
validity to inferences; rungs to whole proofs. *Confused with:* truth;
persuasiveness; provenance (a citation is never a warrant). *Test:* name the
§2.1.2 token, then name what would defeat it; if nothing could, the token is
probably wrong. *Status:* `NEUTRAL`.

**4. demonstration.** An argument satisfying MD1–MD10 (§2.1.1); `RG-WHY` if
also MD11. *Confused with:* a valid derivation (1); a persuasive argument; an
explanation (5). *Test:* run the ladder — a formally impeccable derivation with
no `REAL` import is `RG-VALID` and `V-VALID-ONLY`, never a demonstration.
*Status:* `NEUTRAL`. *Loaded dependency:* MD5 presupposes the real/conceptual
distinction is available and MD10 that a middle can belong *per se*; a Carnapian
or deflationist contests both while accepting MD1–MD4.

**5. metaphysical explanation.** The worldly relation `PRI-GND`: `B` obtains in
virtue of `A`. Not an argument, not a rung. *Confused with:* demonstration (4) —
the fifth term of the governing chain; `PRI-CAU`; a good reason to believe.
*Test:* its relata are facts and it has no premises; if it has premises it is an
argument. *Status:* `AT`. *Rejected/reconstrued by:* grounding deflationists
("in virtue of" names no distinctive relation) and Humean/pragmatic accounts of
explanation (answer-relative to interests, not worldly).

**6. middle term (schematic).** The term through which `subject` is joined to
`attribute`; the `middle` field. *Confused with:* the minor premise; any
convenient intermediate step. *Test:* delete the term from every line; if some
line survives intact, that term was not the middle. *Status:* `NEUTRAL`.

**7. middle-kind.** Classification of a middle as `FORMAL`, `MATERIAL`,
`EFFICIENT`, `FINAL`, `PROPER-ATTRIBUTE`, or `EFFECT-SIGN`. *Confused with:*
entry 6, which is neutral. *Status:* `AT`, the classification presupposing that
grounds come in these sorts. *Rejected by:* physicalists and Humeans, who admit
only `EFFICIENT` and `EFFECT-SIGN`, and by most naturalism, which denies
`FINAL`.

**8. explanatory ground.** Synonym for the relatum `A` of `PRI-GND` (5); the
canonical printing is "ground". Never used for a premise. *Test:* if replacing
"ground" with "premise" leaves the sentence true, the word was misused.
*Status:* `AT` (inherits entry 5).

### 3.4 Statements, definitions, distinctions

**9. premise.** A statement offered in support of `claim`, carrying exactly one
warrant token plus `modality`, `modal-scope`, `import`. *Confused with:*
principle (10, 11); definition (13). *Test:* it can be denied without changing
the subject of discussion. *Status:* `NEUTRAL`.

**10. principle (schematic).** A premise not demonstrated in this book and used
by more than one proof; ledger `kind: PRINCIPLE`. *Confused with:* entry 11;
axiom-like principle (12). *Test:* bibliographic — two or more `consumed-by`
entries, `established-by` empty. *Status:* `NEUTRAL`.

**11. principle (constitutive).** An intrinsic co-constituent of a being — act
and potency, matter and form — not a proposition at all. *Confused with:* entry
10; part; cause. *Test:* can it be asserted or denied? If yes it is entry 10.
*Status:* `AT`. *Rejected by:* trope and bundle theorists, mereological
nominalists, ontic structural realists.

**12. axiom-like principle.** A principle warranted `W-SELF`: evident on
analysis of its terms, analysis printed. *Confused with:* an obvious truth; an
unsupported assertion. *Test:* the analysis must exhibit the predicate in the
subject's account; "everyone accepts it" is not an analysis and yields
`WAR` = `FAIL`. *Status:* `NEUTRAL`.

**13. nominal definition.** A stipulation fixing which sense of a word is live
(`DF-###` over a `TM-###.n`). Adds no content; not false, only useless or
equivocal. *Confused with:* 14; premise (9). *Test:* `LC-08` — if it entails
anything not derivable from the sense plus prior ids it is a hidden premise and
MUST become a `PR-###` (house rule 5). *Status:* `NEUTRAL`.

**14. real definition.** A statement of what a thing is, through its intrinsic
principles or genus and difference; truth-apt and demonstrable — and therefore
**never a `DF-###`**. `DF-###` is reserved for nominal definitions (13). A real
definition is a substantive proposition recorded as a `PR-###` carrying its own
warrant token, `import`, `modality`, non-empty `objections`, and denial-set
membership; premises consume it by `W-DEM` or `W-POST`, never by `W-DEF`. A
statement of what a thing is entered as a `DF-###` is `WAR` = `FAIL` and
`ER-106`, and being a real rather than a nominal definition is never a defence
against `LC-08` or `UA-5`. *Confused with:* entry 13; essence (20). *Test:*
could it be false while the word keeps exactly its current use? Yes → real, and
it takes a `PR-###`; no → nominal, and it takes a `DF-###`. *Status:* `AT`.
*Rejected by:* nominalists and Quinean holists, for whom all definition is
stipulative or conventional; conceptual-role semantics.

**15. distinction; `DK-NOM`.** A claim that two accounts are not
interchangeable. `DK-NOM`: two names, one account, no entailment differs. The
traditional triple *conceptual / virtual / real* maps exactly onto
`DK-NOM` / `DK-VIRT` / `DK-REAL`; "conceptual distinction" and "distinction of
reason" are **retired** in favour of `DK-NOM`, and no fourth grade may be
minted. *Confused with:* a difference of emphasis. *Test:* the `DK-*` order at
§3.9. *Status:* `NEUTRAL`.

**16. `DK-VIRT` (virtual distinction).** Defined at §3.9. *Confused with:*
`DK-NOM` (dismissed as mere words) and `DK-REAL` (overclaimed as two things).
*Test:* §3.9 — produce the divergent entailment or downgrade. *Status:* `AT`.
*Rejected by:* Quinean and Carnapian critics who treat the middle option as
ontologically idle.

**17. `DK-REAL` (real distinction).** Defined at §3.9. *Confused with:* a
distinction we draw in thought. *Test:* §3.9; a conceptual difference alone
yields `ONT` = `FAIL`. *Status:* `AT`. *Rejected by:* monists, bundle theorists,
Humeans about the essence/existence and substance/accident cases specifically.

### 3.5 Predication and the categories

**18. univocal (`PRD-UNI`) / equivocal (`PRD-EQV`).** One account across
occurrences / two unrelated accounts. *Confused with:* each other by
inattention, and both with entry 19. *Test:* substitute one account at every
occurrence (MD2). *Status:* `NEUTRAL`.

**19. analogical (`PRD-ANA`).** The same account does not apply to both
analogates, yet a ratio relating the accounts can be stated. *Confused with:*
`PRD-EQV` (when the ratio is not stated, it *is* `PRD-EQV`) and metaphor.
*Test:* state the ratio in one sentence, or downgrade. *Status:* `AT`.
*Rejected by:* the Scotist tradition of the univocity of being, and by
contemporary semanticists who admit only univocity, ambiguity, and metaphor.

**20. essence.** What a thing is, prior to and distinct from whether it is.
*Confused with:* the meaning of a word (13); a cluster of necessary properties.
*Test:* if your only evidence is what competent speakers would say, you have a
nominal definition. *Status:* `AT`. *Rejected by:* nominalists, modal
conventionalists (necessities as artefacts of our conventions), Quinean
anti-essentialists.

**21. accident.** A determination inhering in a substance and not constituting
what it is. *Confused with:* a contingent property; a *per accidens* connection
(26). *Test:* removal leaves the same thing numerically the same. *Status:*
`AT`. *Rejected by:* bundle and trope theorists, for whom there is no substrate
to inhere in.

**22. substance.** That which exists in itself and is the subject of accidents.
*Confused with:* stuff; matter; an ordinary count-noun object.
*Test:* does the candidate exist *in* something else as in a subject? *Status:*
`AT`. *Rejected by:* bundle theorists, ontic structural realists, process
metaphysicians, and Humeans who admit only distinct co-located qualities.

**23. act.** A determination actually possessed; that by which something is or
is such rather than merely able to be. *Confused with:* action; activity;
occurrence at a time; existence tout court. *Test:* ask what it excludes — act
excludes the corresponding potency, not rest or silence. *Status:* `AT`.
*Rejected by:* physicalists who replace the act/potency pair with occurrent
categorical states plus laws.

**24. potency.** A real capacity of an existing subject to be otherwise;
neither a mere logical possibility nor nothing. *Confused with:* `POS-LOG`,
`POS-CON`, an unrealized future. *Test:* it is located in a namable subject
("*this* water's capacity to boil"). *Status:* `AT`. *Rejected by:* neo-Humean
categoricalists (powers reduce to laws plus categorical bases); *reconstrued*,
not rejected, by contemporary dispositionalism — a partial ally the book MUST
NOT overstate.

**25. *per se*.** Holding in virtue of what the subject is, and so not
eliminable by adding information about circumstances. *Confused with:*
"necessarily"; "always"; "non-accidentally" in the loose sense. *Test:* the
predicate appears in the account of the subject, or the subject in the account
of the predicate. *Status:* `AT` (inherits 20). *Rejected by:* Quinean
anti-essentialism.

**26. *per accidens*.** Holding by co-occurrence, however invariable.
*Confused with:* rare, unimportant, or coincidental in the colloquial sense — an
exceptionless regularity is still *per accidens*. *Test:* a true universal
generalization with no account linking the terms. *Status:* `AT` (contrast term
of 25).

### 3.6 Modality, scope, and their defects

**27. modal force.** Informal name for the spine field `modality`. **Canonical
form: `modality`.** "Modal force" MAY appear in running prose, never as a field
name or table header. *Status:* `NEUTRAL`.

**28. necessity (kinds).** `NEC-LOG`, `NEC-CON`, `NEC-NOM`, `NEC-MET`,
`NEC-HYP`; tests and binding test order at §3.9. *Confused with:* one
another — the genre's signature failure. *Status:*
`NEC-LOG`, `NEC-CON`, `NEC-NOM`, `NEC-HYP` `NEUTRAL`; **`NEC-MET` is `AT`** —
denied by modal conventionalists, Humeans about modality, and modal
fictionalists, who allow nothing beyond logical, conceptual, and nomological
necessity.

**29. contingency (modal).** `CONT`: true and possibly false. *Confused with:*
entry 30; caused; temporary. *Test:* §3.9 — exhibit the possibility at the
recorded grade. *Status:* `NEUTRAL`.

**30. contingent being (categorial).** A being whose essence does not include
its act of existing. *Confused with:* entry 29 — the slide from "possibly false"
to "does not contain its own existing" is a substantive step needing a cited
`BR-###`. *Status:* `AT`. *Rejected by:* anyone denying the essence/existence
`DK-REAL` (entry 17), including most contemporary analytic metaphysics.

**31. scope (three senses).** (a) *syntactic scope* — the argument of a
quantifier or operator; (b) *modal scope* — `SCP-CMP` versus `SCP-DIV`; (c)
*conclusion scope* — the `SCO` axis, whether `claim` exceeds `established`.
**Canonical rule:** bare "scope" always means (c); (a) and (b) are always
written out or given as tokens. *Status:* `NEUTRAL`.

**32. existential import.** Whether a form asserts that its subject class is
non-empty. *Confused with:* truth; the `IMPORT` margin token; the `import`
field. *Test:* MD3 — delete every nonemptiness premise and see what still
purports to exist. *Status:* `NEUTRAL`.

**33. quantifier shift.** Inferring `∃y∀x Rxy` from `∀x∃y Rxy` (or the modal
analogue). *Confused with:* a harmless reordering. *Test:* one countermodel:
everyone has a mother, no one is everyone's mother. *Status:* `NEUTRAL`.

**34. totalization.** Inferring a property of a collection or of the whole
domain from that property's holding of each member. *Confused with:* a valid
universal generalization. *Test:* does the conclusion quantify over a new object
(the totality) not in the premises? *Status:* `NEUTRAL`.

**35. modal collapse.** A structure entailing that everything actual is
necessary, or that all necessity is `NEC-LOG`. *Confused with:* a strong
conclusion. *Test:* derive `p → □p` for arbitrary `p` from the argument's own
resources. *Status:* `NEUTRAL`.

**36. qualification.** Adding a stated respect (`QUA-SEC`) or removing one
(`QUA-SIMP`). *Confused with:* hedging; weakening (`SCO` repair). *Test:* §3.9.
*Status:* `NEUTRAL`.

### 3.7 Dependence, priority, series

**37. dependence (schematic).** `PRI-ONT` (§3.9): necessarily `B` only if `A`,
and not conversely. *Confused with:* entry 38;
temporal succession; correlation. *Test:* a modal test only; it licenses no
claim about what accounts for what. *Status:* `NEUTRAL`.

**38. dependence (grounding).** `PRI-GND`: `B` obtains in virtue of `A`.
Strictly stronger than 37; `PRI-ONT` does **not** entail it. *Test*, three
steps, every one discharged in print: **(1)** `PRI-ONT` holds first —
necessarily `B` only if `A`, and not conversely; failing this the token is not
`PRI-GND`. **(2)** An **asymmetry witness** is exhibited: a case in which `A`
obtains and the `B`-fact does not, or a third fact grounded in `A` and not in
`B`. An appeal to `PRI-GND`'s stipulated asymmetry is not a witness. **(3)**
"`B` because `A`" is assertible and "`A` because `B`" is not, with the reason
the converse fails stated in terms of the account of `A` or of `B`, never in
terms of how the sentences read. **Default, binding:** if step 2 or step 3 is not
discharged in print, the recorded token is `PRI-ONT`, not `PRI-GND`; and where
the token is the priority of a middle to its `claim`, MD11(a) is unsatisfied and
the rung is `RG-THAT` whatever is claimed. Recording `PRI-GND` with a step
undischarged is `DEP` = `FAIL`, and at a middle additionally `EXP` = `FAIL`.
*Status:* `AT` (inherits 5).

**39. priority (kinds).** `PRI-TMP`, `PRI-CAU`, `PRI-ONT`, `PRI-GND`, `PRI-DEF`,
`PRI-EPI`, plus `SIM-NAT`, with tests at §3.9. *Confused with:* one another;
every swap needs a cited `BR-###`. *Status:* `PRI-TMP`, `PRI-DEF`, `PRI-EPI`,
`PRI-ONT` are `NEUTRAL`; `PRI-CAU` and `PRI-GND` are `AT` — Humeans reconstrue
causal priority as regularity or counterfactual covariation with no productive
relation, and grounding deflationists reject `PRI-GND` outright.

**40. `SER-ESS` / `SER-ACC`.** Essentially versus accidentally ordered series,
defined at §3.9. *Confused with:* infinite versus finite; simultaneous versus
successive. *Test:* the concurrency test at §3.9. *Status:* `AT` — presupposes
derivative causal power (entry 39's `PRI-CAU`), which Humeans deny; a
physicalist may accept the concurrency test while denying that any actual series
is `SER-ESS`.

### 3.8 Defect, burden, and repair

**41. begging the question.** A premise whose *warrant* presupposes `claim`, or
any id listing `claim` in `depends-on` (MD7). *Confused with:* a premise an
opponent happens to reject; a premise as strong as the conclusion. *Test:*
trace warrant edges, not sentence resemblance. *Status:* `NEUTRAL`.

**42. dialectical burden.** What `denial-set` records: a minimal set of
premises, definitions, or distinctions whose joint rejection blocks `claim`,
each independently holdable and matched to a named position stated at its
strongest (MD9). *Confused with:* a list of complaints; rhetorical burden of
proof. *Test:* remove a member — if nothing breaks, `DIA` = `FAIL`. *Status:*
`NEUTRAL`.

**43. objection (`OB-###`).** A stated reason to reject a specific premise,
inference, distinction, or the scope of `claim`, attributed to a position and
given that position's own best reason. *Confused with:* a rhetorical foil.
*Test:* would a competent holder of the position sign it? *Status:* `NEUTRAL`.

**44. reply (`RP-###`).** The answer to exactly one `OB-###`, sharing its
number. A reply MAY concede. **Canonical form: "reply"; "response" is retired**
and MUST NOT appear as an environment name, field name, or heading. *Test:*
1:1 with objections; an unanswered `OB-###` routes to `V-PARTIAL`. *Status:*
`NEUTRAL`.

**45. bridge lemma (`BR-###`).** A licensing rule for a change of necessity
kind, modal scope, or priority kind, carrying its own warrant token, antecedent
discharged inside the proof (MD6). *Confused with:* a rule of the calculus; a
plausible transition. *Test:* a conclusion token appearing in no premise — name
the `BR-###` or read `MOD`/`DEP` = `FAIL`. *Status:* `NEUTRAL` as machinery; an
*individual* bridge is usually `AT` and MUST declare its own `framework`.

**46. lemma / corollary.** Ledger `kind` values: a proposition established in
order to be consumed by a named later proof / a proposition following from an
established one with no new substantive premise. *Confused with:* rank or
importance. *Test:* a corollary whose derivation adds a substantive premise is a
`PROPOSITION`, not a corollary. *Status:* `NEUTRAL`.

**47. repair.** A minimal alteration — weakening `established`, adding a
declared premise, supplying a `BR-###`, splitting an equivocal term, or
reclassifying `rung` — after which some `REAL` conclusion survives (`V-REPAIR`).
*Confused with:* rebuttal; substitution of a different argument. *Test:*
minimality (each addition shown necessary), and `survives` prints what now
stands. *Status:* `NEUTRAL`.

**48. terminus.** The non-derivative principle reached at the end of Stage E, of
which Stage F predicates attributes one at a time (§8.10). The word is reserved
to this use. *Confused with:* the `RG-THAT` stopping case (49). *Test:* the item
is the `subject` of a `PR-4##` and carries a `dossier` line. *Status:*
`NEUTRAL`.

**49. `RG-THAT` stopping case.** The declared reason a demonstration stops at
`RG-THAT`: `middle-kind: EFFECT-SIGN`; a `PROPER-ATTRIBUTE` middle convertible
with the subject; a Stage A or B structural specimen; or none of the three, in
which case the candidate ground is named (§2.4). *Confused with:* failure to
reach `RG-WHY` — `RG-THAT` is a completed species, never graded as a failed
`RG-WHY`. *Test:* the case is stated as the first clause of the mandatory
`OV-EXPL` entry in `not-established`. *Status:* `NEUTRAL`.

**50. stripped variant.** The `COND` field of §4.2 discharging MD11(c): a valid
derivation of the same `claim` not routing through `middle`, plus one sentence
naming what it leaves unexplained — or, where no such derivation exists, the
printed exclusion argument §4.2 licenses in its place. *Confused with:* a second
demonstration with its own conclusions. *Test:* the variant derives `claim` with
`middle` deleted from every line. *Status:* `NEUTRAL`.

**51. claimed rung / achieved rung.** The rung a proof object declares in
`rung`, and the rung §6.2.1 computes from its fourteen marks. *Confused with:*
one another — the divergence is exactly what the `DEM` axis detects. *Test:*
claimed above achieved is `DEM` = `FAIL`, routed to `V-REPAIR` (§2.2, §6.2.1).
*Status:* `NEUTRAL`.

**52. load-bearing premise.** A premise whose deletion breaks some step of the
object. *Confused with:* a premise that is merely contested, or merely carries
`import: REAL`. *Test:* delete each premise in turn and re-run `steps`; those
whose deletion breaks a step are the load-bearing ones (MD9, `UA-9`(a)).
*Status:* `NEUTRAL`.

### 3.9 Deciding tests, verbatim and binding

**Necessity and possibility.**

| Token | Kind | Deciding test |
|---|---|---|
| `NEC-LOG` | logical | true under every uniform reinterpretation of the non-logical vocabulary |
| `NEC-CON` | conceptual / analytic | derivable from cited `DF-###`/`DS-###` plus logic alone; carries **no** real import without a cited `BR-###` |
| `NEC-NOM` | nomological | false at some world differing from ours only in laws; warrant is `W-EMP` or `W-IND` |
| `NEC-MET` | real / metaphysical | the denial describes no genuine possibility even where conceptually coherent; the text names the grounding nature and the possibility space surveyed |
| `NEC-HYP` | hypothetical | the operator scopes a conditional whose antecedent is itself contingent |
| `ACT` · `CONT` · `IMPOSS` | actual · contingent · impossible | asserted as fact · true and possibly false · no world verifies it |
| `POS-LOG` · `POS-CON` · `POS-NOM` · `POS-MET` | possibility, mirroring the above | for `POS-MET` the possibility must be exhibited, not merely not-yet-refuted |

**Test order, binding:** `NEC-LOG`, then `NEC-CON`, then `NEC-NOM`, then
`NEC-MET`. A claim recorded `NEC-MET` that passes the `NEC-CON` test is
misrecorded — conceptual necessity in metaphysical dress is the signature failure
of the genre. Conceivability licenses `POS-CON` only; `POS-MET` requires a cited
conceivability-possibility bridge tagged `W-POST`. `NEC-NOM` never upgrades to
`NEC-MET` without a named, audited `BR-###`. "Necessary being" is not an operator
and MUST be cashed out *de re* with explicit scope.

**Modal scope.** `SCP-CMP` — composite sense, necessity of the consequence,
`□(A → B)`. `SCP-DIV` — divided sense, necessity of the consequent, `A → □B`.
Every modal line in `L3-SKEL` prints its scope token. *Worked defect:* from
"necessarily, whatever is moved is moved by another" (`SCP-CMP`) and "this is
moved" (`ACT`), the licensed conclusion is "this is moved by another" (`ACT`),
not "necessarily, this is moved by another" (`SCP-DIV`). Recording the premise
as `NEC-MET` in the divided sense is `MOD` = `FAIL`.

**Priority and dependence.**

| Token | Relation | Deciding test |
|---|---|---|
| `PRI-TMP` | temporal | settled by dates alone; entails no other priority whatever |
| `PRI-CAU` | causal | `A`'s acting accounts for `B`'s being or coming to be; may be simultaneous; direction fixed by which removal removes which |
| `PRI-ONT` | existential dependence | necessarily `B` exists only if `A` does, and not conversely; a modal test, not an explanatory one |
| `PRI-GND` | grounding | `B` obtains *in virtue of* `A`; irreflexive, asymmetric, transitive by stipulation; strictly stronger than `PRI-ONT`; recorded only by the three-step test at entry 38 |
| `PRI-DEF` | definitional | `A`'s definiens occurs in `B`'s and not conversely; carries no real import |
| `PRI-EPI` | order of knowing | `A` is recognizable without `B`; **evidence for no other priority** |
| `SIM-NAT` | natural simultaneity | each entails the other and neither account is prior; blocks the inference "simultaneous, therefore neither depends" |

`PRI-ONT` does **not** entail `PRI-GND`: necessary co-existents may depend on one
another existentially with grounding in neither direction. Any swap of one
`PRI-*` token for another cites a `BR-###`.

**Series.** `SER-ACC` (accidentally ordered: a member's causing does not require
the prior member's concurrent causing) versus `SER-ESS` (essentially ordered: it
does; power derivative here and now). Any argument turning on the impossibility
of infinite regress MUST declare which and apply the concurrency test: does
removing a non-terminal member remove the effect *simultaneously*?

**Distinction kind**, three-valued because a two-valued scheme forces every
author to overclaim or underclaim: `DK-REAL` (separable at least in principle, or
really distinct principles of one thing) · `DK-VIRT` (inseparable even in
principle, yet the thing itself grounds two non-synonymous true accounts with
different entailments) · `DK-NOM` (two names, one account, no entailment
differs). Test order: attempt separation; failing that, produce an entailment
true of one account and false of the other; failing that, `DK-NOM`.

**Predication:** `PRD-UNI`, `PRD-EQV`, `PRD-ANA`. Test for `PRD-ANA`: the same
account does not apply to both analogates, yet a ratio relating the accounts can
be stated. If the ratio cannot be stated, the use is `PRD-EQV` and the argument
equivocates.

**Qualification:** `QUA-SIMP` (unqualified) and `QUA-SEC` (asserted in a stated
respect, which MUST be printed). Inferring `QUA-SIMP` from `QUA-SEC` requires a
licensing premise with its own warrant.


## 4. The Canonical Proof Object

### 4.1 Status, print order, and reference syntax

The proof object `PF-###` is the only anatomy in which this book presents an
argument it takes seriously. It is a *record*, not a layout: one record drives
`L1-PROSE`, `L2-NUM`, `L3-SKEL` (§5), the audit table (§6), the ledger entry
(§10), and every exercise citing the argument. A field appearing in one layer
and vanishing from another breaks the contract.

**Print order is fixed and never varied**: `id` · `name` · `kind` · `provenance` ·
`reconstruction-note` · `rung` · `logic` · `claim` · `subject` · `attribute` · `import` · `modality` · `domain` ·
`lexicon` · `premises` · `steps` · `middle` · `middle-kind` · `stripped-variant`
· `series-kind` · `commitments` · `depends-on` · `established` ·
`not-established` · `denial-set` · `objections` · `replies` · `framework` ·
`framework-role` · `layers` · `fidelity` · `audit` · `scholion`. No two fields
may be merged into one printed run, and no field may be replaced by a
cross-reference to another proof object. A field whose content is genuinely
empty prints its key with the token `EMPTY`, except where this section forbids
emptiness.

**Where the record is printed.** The record is not set as a keyed block in the
book. The print order governs four artefacts only: the ledger and proof-object
source files; the schematic blocks inside this specification; `T4` solution
answers (§9.7); and the back-matter blank audit form. On a book page each field
surfaces only as §4.2's `L1-PROSE` and `L2/L3` columns specify, together with the
audit table and the margin callouts. `EMPTY` is a source-file token and is never
set in type.

**Reference syntax (binding on the exercise and solution sections).** A dotted
suffix on a `PF-###` id is read mechanically by its first character: bare digits
name an inference step (`PF-007.3`, §4.2); `p` plus digits names a premise
(`PF-007.p2`); `c` plus digits names a commitment row (`PF-007.c1`); `n` plus
digits names a `not-established` entry (`PF-007.n2`); anything else is a field
name (`PF-007.established`). Objections and replies are cited by their own
`OB-###` / `RP-###` ids, never through the proof object. Solutions cite the same
slot the exercise cited; a solution that answers at a coarser grain than the
exercise asked ("the argument fails somewhere in the middle") is a defect.

### 4.2 Field table

**Requiredness legend, two codes.** `MUST` = required on every proof object of
every kind at every stage: `id`, `name`, `kind`, `rung`, `logic`, `claim`,
`subject`, `attribute`, `import`, `modality`, `lexicon`, `premises`, `steps`,
`depends-on`, `established`, `not-established`, `framework`, `layers`,
`audit`. `MUST-C` = required from Stage C
onward for `kind: DEMONSTRATION` and `kind: DIALECTICAL`: `domain`, `middle`,
`middle-kind`, `commitments`, `denial-set`, `objections`, `replies` — and `framework-role`, which is additionally gated by
its own row (`COND` on `framework ≠ NEUTRAL`, §14 N8). `COND` = required exactly
under the stated trigger; `MAY` = optional. All four codes require the *key*,
not a non-empty value, except where a row or §4.5 forbids emptiness. A
`SPECIMEN` object's `depends-on` is required precisely so that the reader can
see which established results a defective argument helps itself to; `EMPTY` is a
legitimate value there, silence is not. Requiredness of `established` and
`not-established` is not the same thing as requiredness of §4.5's seven-line
dimension survey, which keeps its own narrower trigger. `L2/L3` gives the schematic rendering;
where the two layers differ the cell says so.

| Field | Req | MUST contain | MUST NOT contain | `L1-PROSE` | `L2/L3` |
|---|---|---|---|---|---|
| `id` | MUST | `PF-###`, allocated once, never reused | a status word ("Lemma") baked into the number | in the environment header | header of both layers |
| `name` | MUST | ≤ 6 words, unique on `name-normalized` | a claim, a verdict, or a hedge | header, after the id | header |
| `kind` | MUST | `DEMONSTRATION`, `DIALECTICAL`, or `SPECIMEN`, as §4.2.1 defines them | more than one token | header word ("Demonstration") | header |
| `provenance` | COND — iff `kind: SPECIMEN` | one of `SPC-HIST`, `SPC-COMP`, `SPC-CONS` as §8.8.1 defines them | more than one token; an attribution standing in place of the token | in the specimen header | header |
| `reconstruction-note` | COND — iff `provenance: SPC-HIST` | the two sentences §8.8.2 R2 requires: where the reconstruction supplies material the source leaves implicit, and whether the source would accept it | an evaluation of the source or of its author | beneath the specimen header | header |
| `rung` | MUST | one §2.2 token | explanatory language when `RG-THAT` | header, in brackets | header of `L2-NUM` |
| `logic` | MUST | named system, modal system named if modal lines occur | "informal", "obvious" | one clause in the opening sentence | header of `L3-SKEL` |
| `claim` | MUST | exactly one canonical sentence, immutable once `ACTIVE` | "therefore", scare quotes, or a second sentence | stated once, in italic, before the argument | line `C` in `L2-NUM`; the last line of `L3-SKEL` |
| `subject` | MUST | the term `claim` predicates of, with its `TM-###.n` selector | a description whose uniqueness is unproved (MD3) | inline in `claim` | printed beside `claim` in `L2-NUM` |
| `attribute` | MUST | the predicated term, with its selector | an analogical term with no declared ratio | inline in `claim` | as for `subject` |
| `import` | MUST | `REAL`, `CONCEPTUAL`, `LINGUISTIC`, or `MIXED`; `MIXED` only when `commitments` carries at least one row with `import: REAL` and at least one with `CONCEPTUAL` or `LINGUISTIC`, and the object prints one sentence beneath `established`, first in the order §4.5 fixes, naming exactly which part of `claim` is the real part | `REAL` when every premise is `W-DEF` or `W-HYP` | one clause after `claim` | header of `L2-NUM` |
| `modality` | MUST | one necessity/possibility/`ACT`/`CONT`/`IMPOSS` token plus one `SCP-*` token | an ordinary-language modal ("must") standing alone | inline, with the token in parentheses | `L2-NUM` prints both tokens on the conclusion line; `L3-SKEL` prints scope on every modal line |
| `domain` | MUST-C | each quantifier's range, plus an existential-import declaration per quantified premise | a domain fixed only by example | one sentence before the premises | a labelled preamble line in both layers |
| `lexicon` | MUST | three labelled runs — `lexicon.terms` (`TM-###.n`), `lexicon.definitions` (`DF-###`), `lexicon.distinctions` (`DS-###`) | a technical term with no id; a `DF-###` asserting substantive content (`LC-08`) | each id expanded at first use with a `DEF` or `DIST` callout | listed as a preamble block |
| `premises` | MUST | ordered subrecords (§4.3) | an unwarranted premise; a principle used but unlisted | full sentences, in subrecord order | numbered `p1…pn` in `L2-NUM`; symbolized in `L3-SKEL` |
| `steps` | MUST | ordered subrecords (§4.3) | "it follows that" with no rule | prose may compress steps but may not add one | every step printed in both layers, with its rule name |
| `middle` | MUST-C | the term through which `claim` is reached, with its selector; `EMPTY` in a `DIALECTICAL` object (§4.2.1) | the conclusion restated | named explicitly in one sentence, with a `WHY` callout | printed as a labelled line of `L2-NUM` |
| `middle-kind` | MUST-C | one of the six MD10 tokens; `EMPTY` in a `DIALECTICAL` object | two tokens, or `EFFECT-SIGN` beside `rung: RG-WHY` | inline with `middle` | as above |
| `stripped-variant` | COND — iff `rung: RG-WHY` | a valid derivation of the same `claim` not routing through `middle`, plus one sentence naming what it leaves unexplained; or, where no valid derivation of `claim` avoiding `middle` exists, a printed exclusion argument that (i) is recorded as its own `PR-###` with its own warrant token, (ii) names the class of routes it excludes and the property of `claim` that excludes them, and (iii) does not rest on `PRI-DEF` or on `middle` occurring in the definition of `subject` (MD11c) | a second demonstration with its own conclusions; an alternative discharge failing any of (i)–(iii), which is `EXP` = `FAIL` routed to `V-REPAIR` by reclassification to `rung: RG-THAT` | a short indented paragraph after the demonstration | a two- or three-line skeleton in `L3-SKEL` |
| `series-kind` | COND — iff any step turns on the impossibility, finitude, or termination of a regress | `SER-ACC` or `SER-ESS`, plus the concurrency test applied to this series | an appeal to "infinite regress" with no token | one sentence with the test result | a labelled line beside the step that uses it |
| `commitments` | MUST-C | commitment rows (§4.4) | a quantifier ranging over anything absent from the rows | a paragraph headed by the `IMPORT` callout | a table beside `L2-NUM`; not symbolized |
| `depends-on` | MUST | every `TM`, `DF`, `DS`, `PR` id consumed; may be `EMPTY`; a bridge is listed by its companion `PR-###` and never by its `BR-###` alias (§10.2a) | an id used in `steps` but unlisted (`LC-21`); any entry matching `^BR-` (`LC-12`) | a `USES` callout at each point of consumption | a preamble list plus edges in the dependency graph |
| `established` | MUST | §4.5 | a word absent from `claim` and `lexicon` | printed verbatim in a set-off block after the last step | printed verbatim, identically, in `L2-NUM` |
| `not-established` | MUST | §4.5; ≥ 1 entry; `NONE` inadmissible | a rebuttal of the stronger claim; an assurance that it holds elsewhere | a bulleted list, each item with a `SCOPE` callout | the same list, unabbreviated |
| `denial-set` | MUST-C | MD9: a minimal load-bearing set, each member with a named standing position and that position's strongest reason | a position given a reason weaker than its own literature gives | one paragraph, each member with an `OBJ` callout | listed by `pid` or id |
| `objections` | MUST-C | `OB-###` ids; ≥ 1 when `import: REAL` or `framework ≠ NEUTRAL` | an objection authored weaker than its best published form | each objection in full, in its own environment | listed by id |
| `replies` | MUST-C | `RP-###`, one per objection, same number; a reply MAY concede | a reply that silently amends `claim` | as above | listed by id |
| `framework` | MUST | `NEUTRAL`, `AT`, or another named framework | an unnamed framework where `W-POST` premises occur | one clause before the premises | header of `L2-NUM` |
| `framework-role` | COND — iff `framework ≠ NEUTRAL` | exactly one of `FR-NEUTRAL` (uses no `FS-INTERNAL` premise, sense, definition, or distinction), `FR-INTERNAL` (proved within the framework; `established` conditional, with §14's conditionality note printed beneath it), `FR-CONSTITUTIVE` (establishes part of the framework; every premise `FS-NEUTRAL` or `FS-EARNED`) | `FR-NEUTRAL` beside any `W-POST` premise or any `FS-INTERNAL` element; any token without the `FR-` prefix | one clause beside `framework` | header |
| `layers` | MUST | which of `L1-PROSE`, `L2-NUM`, `L3-SKEL` appear | `L3-SKEL` without `L2-NUM` | not printed as such | header |
| `fidelity` | COND — iff `L3-SKEL` is printed | one sentence naming what the symbolization drops | a defence of the symbolization | a footnote or a `RISK` callout | printed under `L3-SKEL` |
| `audit` | MUST | all fourteen axis marks in §6.2 order, plus one verdict token | a verdict chosen rather than computed | not printed in prose | a table beside the argument |
| `scholion` | MAY | a textual or historical note | anything cited by a `steps` line as warrant | a small-type note | not printed |

**Exercise hooks**, once rather than per row: `rung` (grade the rung) · `claim`
(WEAKEN THE CONCLUSION) · `subject`, `attribute` (wider-or-narrower subject) ·
`import` (conceptual versus real) · `modality` (hidden modal shift) · `domain`
(existential import) · `lexicon.definitions` (hidden premise) · `middle` (which
term explains) · `not-established` (scope) · `denial-set` (burden location) ·
`fidelity` (rival formalization) · `audit` (AUDIT, in full). `SPECIMEN` objects
are the stock of REFUTE and LOCATE THE FAILURE stems; `scholion` carries none.
Fields are cited by the §4.1 dotted grammar; §9 governs stem construction.

Two closures bind this table. (1) The `FS-*` and `FR-*` families are closed and
owned by §14. The values `INTERNAL`, `CONSTITUTIVE`, `INDEPENDENT` and the
lowercase word "neutral" are retired; each is a compile error under `AC-P20`.
(2) An object recorded `MIXED` is treated as `REAL` for MD5 and for `UA-2` — the
paraphrase test runs on the real part and the paraphrase is printed — and `MIXED`
never by itself satisfies MD5. An object recorded `MIXED` whose `commitments`
carries no `REAL` row has `import: CONCEPTUAL`, and recording it `MIXED` is
`ONT` = `FAIL`.

#### 4.2.1 The three kinds

`kind` fixes what the book does with the object. Each prohibition below is bound
to content, not to the token chosen, so that retyping an object never lifts one.

**`DEMONSTRATION`** — an argument the book asserts on its own authority. It is
the only kind eligible to appear in a `PR-###`'s `established-by`, or to be
consumed by a `steps` line, a `USES` callout, or a `depends-on` edge.

**`DIALECTICAL`** — an argument printed to exhibit a position the book neither
asserts nor rejects: an argument constitutive of a framework the book does not
itself assert, a reductio of a rival, an argument run on an opponent's own
commitments. It is hard-capped at `rung: RG-VALID`; it carries every `MUST-C`
field and the full fourteen-row audit; it MUST print one sentence naming whose
premises it argues from; and it MUST NOT appear in any `established-by` or in any
`DEMONSTRATION`'s `depends-on`. Its `middle`, `middle-kind`, and
`stripped-variant` are `EMPTY`, and its `established` states only that the
considerations adduced support the claim.

**`SPECIMEN`** — an argument printed in order to be rejected. Every `SPECIMEN`
carries at least one axis at `FAIL` and at least one `ER-###`.

Two consequences bind.

(a) An argument that is correct but establishes no real claim is
`kind: DEMONSTRATION` at `rung: RG-VALID` with verdict `V-VALID-ONLY`, never a
`SPECIMEN`; and an object typed `SPECIMEN` whose audit carries no `FAIL` is
`DEM` = `FAIL`.

(b) `W-REV` and `W-AUTH` premises are prohibited in every proof object of every
kind, the single exception being a `SPECIMEN` whose declared target error class
is `ER-702` or `ER-703`. `PRV` = `FAIL` is therefore not scoped to
`kind: DEMONSTRATION`, and relabelling `kind` is never a remedy.

### 4.3 Premise and step subrecords

**Premise.** `{ pid, text, warrant, modality, modal-scope, import,
framework-status, contested, source, discharged-at }`. `pid` is `p1, p2, …`.
`source` is the `PR-###` id when the premise is a previously established
principle, lemma, or corollary — this is how *principles* are distinguished from
locally asserted premises — and `LOCAL` otherwise; a premise with
`warrant: W-DEM` and `source: LOCAL` is a contradiction and is `WAR` = `FAIL`.
`framework-status` takes exactly one `FS-*` token from §14. A premise with
`warrant: W-DEF` MUST carry `import: CONCEPTUAL` or `LINGUISTIC`,
`modality: NEC-CON`, and `framework-status: FS-NEUTRAL`; it MUST cite exactly one
`DF-###` in `depends-on`; and it MUST NOT be the premise discharging MD5's
requirement that at least one load-bearing premise carry `import: REAL`. A
`W-DEF` premise recorded `REAL` or `MIXED`, or carrying any necessity token other
than `NEC-CON`, is `ONT` = `FAIL` and `ER-106`; the repair promotes the content to
a `PR-###`, and the premise's warrant becomes `W-DEM`, `W-SELF`, or `W-POST`.
`discharged-at` is `COND` — required exactly when `warrant: W-HYP` — and names
the step discharging the hypothesis; an undischarged `W-HYP` premise is
`LOG` = `FAIL`. `contested` MUST be `true` for every premise in `denial-set`, and
a premise marked `contested: true` MUST appear in `denial-set` or in some
`OB-###`.

**Step.** `{ k, from, rule, to, modality, modal-scope, bridge }`. `from` lists
the `pid`s and earlier `k`s consumed; `rule` names a rule of the declared
`logic`; `to` is the resulting line. `bridge` is `COND` — required exactly when
`modality` or `modal-scope` on `to` is stronger, under the §10.3 orders, than
the weakest such token among all lines in `from` (identity with the token of
some one line in `from` does not discharge it), or when the step swaps one
`PRI-*` token for another — and names the `BR-###` licensing the change. A step
that changes a modal or priority token with `bridge: EMPTY` is `MOD` = `FAIL` or
`DEP` = `FAIL`.

### 4.4 The commitment rows

`commitments` is a table, one row per commitment, with columns
`cid · commitment-kind · statement · import · licensed-by · tag · paraphrase`.

`commitment-kind` is one of four: `EXISTS` (something of a named kind or a named
individual exists), `REALLY-DISTINCT` (two items are distinct in the thing and
not merely in our accounts of it), `REALLY-DEPENDS` (one item depends on another
in the thing), `RANGES-OVER` (a quantifier ranges over a kind without asserting
that the kind is occupied). Every kind, relation, and individual quantified over
or named in `claim`, `premises`, or `steps` appears in exactly one row.

The field forces one sentence the author would otherwise not write: **if `claim`
is true, what exists, what is really distinct, and what really depends on what.**

1. `import` on each row is `REAL`, `CONCEPTUAL`, or `LINGUISTIC`. A row whose
   content is only that we use two words, or draw two concepts, is
   `LINGUISTIC` or `CONCEPTUAL` and may not be written with the vocabulary of
   things.
2. `tag` carries the `DK-*` token for every `REALLY-DISTINCT` row and the
   `PRI-*` token for every `REALLY-DEPENDS` row. `DK-NOM` in a
   `REALLY-DISTINCT` row is a contradiction and is `ONT` = `FAIL`.
3. `paraphrase` is `COND` — required on every row with `import: REAL` — and
   prints the MD5 rewrite of that commitment ("our concept of *F* requires…")
   plus one sentence saying why the cited premises do not support the rewrite
   with equal force. A `REAL` row whose paraphrase is supported equally well is
   `ONT` = `FAIL`.
4. `licensed-by` names the `pid`, step, or prior id that incurs the commitment.
   A commitment licensed by nothing is a commitment smuggled in by the prose.
5. **Import coherence.** A `PF-###` whose `claim` carries `import` `REAL` or
   `MIXED` MUST contain at least one commitment row with `import: REAL`; and a
   row of kind `EXISTS`, `REALLY-DISTINCT`, or `REALLY-DEPENDS` may not carry
   `import` `CONCEPTUAL` or `LINGUISTIC`. Either is `ONT` = `FAIL`. Only
   `RANGES-OVER` rows may be non-`REAL`.
6. **Licensed-by on a `REAL` row must name something warranted.** Every row with
   `import: REAL` MUST cite a premise `pid` of this object, or a `PR-###`
   carrying its own warrant token. A `TM-###`, `DF-###`, or `DS-###` id in
   `licensed-by` on a `REAL` row is `ONT` = `FAIL`: naming a distinction is never
   asserting one. That a pair stands in `DK-REAL` or `DK-VIRT` is a substantive
   proposition needing its own `PR-###`, and `denial-set` membership where
   load-bearing.
7. **Claim-level paraphrase.** Every `PF-###` with `import` `REAL` or `MIXED`
   prints, once, beneath `established`, in the order §4.5 fixes, the MD5 rewrite of
   `claim`
   itself, followed by one sentence naming the `pid` or `cid` that fails to
   support the rewrite with equal force. The `ONT` audit row cites it by locus
   rather than restating it; an `ONT` mark of `OK` with no such printed rewrite
   is rejected in review.

### 4.5 The anti-overreach pair

`established` and `not-established` are both mandatory in every proof object at
every stage, including reduced ones (§4.8). **They may never be merged, printed
as a single paragraph, or elided.** Their separation is what makes house rules 2
and 6 checkable on the page.

**`established` — the conclusion actually established.** A verbatim restatement
of `claim` bounded by the premises: same subject, same attribute, same sense
selectors, and exactly the modality and modal scope licensed by the weakest link.
Mechanical constraints: (i) every non-logical word in `established` occurs in
`claim` or in `lexicon`; (ii) `established` contains no inferential connective
("therefore", "hence"), no hedge ("arguably", "in some sense"), and no
explanatory connective ("because", "in virtue of") unless `rung: RG-WHY`, in
which case exactly one such connective may appear and it must name `middle`;
(iii) if `established` differs from `claim` in any respect other than
typography, `claim` was overstated, and the object is at least `V-REPAIR` with
the repair being the substitution of `established` for `claim` under a new id.

**Order beneath `established` (binding).** `established` prints as a set-off
block after the last step. Where more than one of the following is owed, they
print immediately beneath it in this order and no other: (1) the `MIXED`
real-part sentence (§4.2, `import` row); (2) the claim-level MD5 rewrite (§4.4
(7)); (3) the conditionality note (§14 N11); (4) the inherited-verdict sentence
(§6.5 (4)). No other material intervenes.

**`not-established` — stronger conclusions not yet established.** An explicit
enumeration of the nearby stronger claims a competent reader might wrongly take
the argument to have delivered. Each entry is
`{ nid, statement, overreach-kind, missing-bridge, where-treated }`.
`overreach-kind` is one of seven, each mapping to the axis that would record the
mistake: `OV-MOD` (modality strengthened; `MOD`), `OV-SCOPE` (subject or
quantifier widened; `SCO`), `OV-IMPORT` (a conceptual result read as a real one;
`ONT`), `OV-UNIQ` (from "some" or "a" to "the"; `EXI`), `OV-EXPL` (from *that* to
*why*; `EXP`), `OV-IDENT` (the item reached identified with a familiar item under
another name; `ONT`), `OV-TOTAL` (from every member to the collection; `SCO`).

`missing-bridge` holds ids only: one or more `ACTIVE` `BR-###` or `PR-###` ids;
or an unproved `PR-###` with empty `established-by`, visibly a stub; or the
token `NO-BRIDGE-KNOWN`. Free prose there is `SCO` = `FAIL`, as is naming a
bridge that exists as no id. `where-treated` holds `NOT-IN-BOOK` or the `PR-###`
id at which the stronger claim is established, whose record must then list, for
each id in this entry's `missing-bridge`, that id — or, for a `BR-###`, its
companion `PR-###` (§10.2a) — in its own `depends-on`; a bare
chapter.section reference is `SCO` = `FAIL`. An entry stating the object's
framework role, rather than a claim not reached, is `SCO` = `FAIL` and does not
count toward non-emptiness. The entries mandated by §5, rule (iv), §5.4, and
§5.5(e)(3) are written in this same five-key grammar as `OV-IMPORT` entries
whose `statement` names the stronger claim the symbolization invites — that the
term is univocal across its occurrences, that validity here has been
machine-checked, that the formula says what `claim` says — with `missing-bridge`
`NO-BRIDGE-KNOWN` and `where-treated` `NOT-IN-BOOK`; each satisfies the
`OV-IMPORT` line of the dimension survey and counts toward non-emptiness.

Entries name bridges missing *from the book*, not from the argument; they never
trigger verdict rule 5, which concerns a bridge the argument itself needs and
does not cite. An entry is required for every strengthening dimension the
argument plausibly invites, not one token entry to satisfy the count.

**Dimension survey, mandatory.** In every `PF-###` with `kind: DEMONSTRATION` and
`import` `REAL` or `MIXED`, from Stage C onward, `not-established` prints exactly
seven labelled lines, one per `overreach-kind` token, in the fixed order `OV-MOD`,
`OV-SCOPE`, `OV-IMPORT`, `OV-UNIQ`, `OV-EXPL`, `OV-IDENT`, `OV-TOTAL`. Each line
carries either one `n#` entry in the five-key grammar above, or the token
`CLOSED` plus one reason of at most fifteen words naming the feature of `claim`,
`subject`, or `domain` that leaves that dimension with no nearby stronger claim.
A missing line, a bare `CLOSED`, or a `CLOSED` reason that remains true and apt
when transplanted to another proof object with a different `claim` (the
transplant test, §11.6) is `SCO` = `FAIL` and `ER-605`. `OV-EXPL` may never read
`CLOSED` in an `RG-THAT` object, which by construction has not shown why.

Emptiness is inadmissible: the field never prints `NONE` and never prints
`EMPTY`. In objects to which the mandatory survey does not apply, and where the
author judges that no nearby stronger claim exists, the field prints `EXHAUSTED`
followed by a survey naming all seven `overreach-kind` dimensions and stating,
for each, why it is closed. `EXHAUSTED` is admissible only when
`kind ≠ DEMONSTRATION` and `import ∈ {CONCEPTUAL, LINGUISTIC}`; its appearance
anywhere else is `SCO` = `FAIL`.

### 4.6 Worked skeletal instance

An exemplar, deliberately small; a chapter instance carries fuller premise
analyses and the full fourteen-row audit table. Its ids are illustrative and
allocated in no band.

- `id` `PF-007` · `name` No self-caused coming-to-be · `kind` `DEMONSTRATION` ·
  `rung` `RG-WHY` · `logic` first-order logic with identity, modal lines in `T`
- `claim` For every *x*, *x* is not the total efficient cause of *x*'s own
  coming to be.
- `subject` *x* (`TM-019.1`, individual that comes to be) · `attribute` total
  efficient cause of its own coming to be (`TM-012.2`)
- `import` `REAL` · `modality` `NEC-MET`, `SCP-CMP`
- `domain` *x* ranges over individuals that come to be; the universal premises
  carry no existential import; nothing is asserted to come to be.
- `lexicon.terms` `TM-012.2`, `TM-019.1` · `lexicon.definitions` `DF-004` (total
  efficient cause of *E*: that whose acting suffices for *E*) ·
  `lexicon.distinctions` `DS-003` (`PRI-CAU` versus `PRI-TMP`, tag `DK-REAL`)
- `premises`
  - `p1` A total efficient cause of *E* acts in producing *E*. — `W-DEF`
    (`DF-004`) · `NEC-CON` · `SCP-CMP` · `CONCEPTUAL` · `FS-NEUTRAL` · not
    contested · `source: LOCAL`
  - `p2` Nothing acts at a point at which it does not yet exist. — `W-SELF`,
    analysis printed at the line · `NEC-MET` · `SCP-CMP` · `REAL` · `FS-NEUTRAL` ·
    `contested: true` · `source: LOCAL`
  - `p3` Nothing exists prior in the order of causal priority (`PRI-CAU`) to its
    own coming to be. — `W-SELF` · `NEC-MET` · `SCP-CMP` · `REAL` · `FS-NEUTRAL` ·
    `contested: true` · `source: LOCAL`
  - `p0` Suppose some *a* is the total efficient cause of *a*'s own coming to
    be. — `W-HYP` · `discharged-at: 4`
- `steps` 1. `p0`, `p1`; ∀-elim, MP; *a* acts in producing *a*'s coming to be. ·
  2. 1, `p2`; MP; *a* exists prior in `PRI-CAU` to *a*'s coming to be (`NEC-MET`;
  `bridge: BR-003`, licensing the `NEC-CON` → `NEC-MET` move on line 1;
  companion proposition `PR-031`). · 3. 2, `p3`; ⊥. ·
  4. ¬-intro discharging `p0`, then ∀-intro; `claim`.
- `middle` the agent's being in act at the point of its acting · `middle-kind`
  `EFFICIENT` · priority of `middle` to `claim`: `PRI-GND`
- `stripped-variant` Stipulating that "coming to be" excludes self-production
  reaches the same `claim` in one valid line and leaves unexplained why the
  stipulation is not arbitrary; the present route explains it through `p2`.
- `commitments` `c1` `RANGES-OVER` individuals that come to be — `REAL`,
  licensed by `p3`, no existence asserted; paraphrase "our concept of coming to
  be has whatever instances we classify under it" — not supported equally, since
  `p3` governs what such individuals can stand in, not how we sort them.
  `c2` `REALLY-DEPENDS` an acting
  presupposes the agent's actuality — `REAL`, tag `PRI-CAU`, licensed by `p2`;
  paraphrase "our concept of acting includes an actual agent" — not supported
  equally, since `p2` is denied by anyone holding that causal talk records mere
  succession — a claim about the world, not the concept.
  `c3` `REALLY-DISTINCT` causal priority from temporal priority — `REAL`, tag
  `DK-REAL`, licensed by `PR-024` (that the two priorities are `DK-REAL`;
  `DS-003` names the distinction and licenses nothing); paraphrase "we keep the
  causal and temporal accounts apart" — not supported equally, since `p3`
  requires the ordering to obtain in the thing.
- `depends-on` `TM-012.2`, `TM-019.1`, `DF-004`, `DS-003`, `PR-024`, `PR-031`
  (`BR-003`'s companion; a bridge is never listed in `depends-on` by its alias)
- `established` For every *x*, *x* is not the total efficient cause of *x*'s own
  coming to be, and this because acting presupposes the agent's actuality
  (`NEC-MET`, `SCP-CMP`). MD5 rewrite of `claim`: "our concept of coming to be
  excludes self-production"; `p2` fails to support it with equal force, being a
  claim about what an agent must be in order to act.
- `not-established` (seven lines, fixed order)
  - `OV-MOD` `CLOSED` — `claim` already carries `NEC-MET`, the strongest
    necessity kind the book assigns.
  - `OV-SCOPE` `n1` Everything that comes to be has a cause. —
    `missing-bridge` `PR-044` (stub, `established-by` empty) ·
    `where-treated` `NOT-IN-BOOK`
  - `OV-IMPORT` `n2` Nothing is self-sustaining in existence. —
    `missing-bridge` `NO-BRIDGE-KNOWN` · `where-treated` `NOT-IN-BOOK`
  - `OV-UNIQ` `CLOSED` — `claim` names no individual and contains no definite
    description.
  - `OV-EXPL` `CLOSED` — `rung` is `RG-WHY`; the grounding middle is exhibited
    and declared `PRI-GND`.
  - `OV-IDENT` `CLOSED` — `claim` identifies nothing; it denies a relation of
    each *x* to itself.
  - `OV-TOTAL` `n3` There is a first uncaused cause. — `missing-bridge` `PR-044`,
    `PR-061` (`SER-ESS` regress), `PR-063` (uniqueness) · `where-treated`
    `PR-090`, whose record lists all three in `depends-on`
- `denial-set` `{p2}` — the Humean about causal powers denies it at full
  strength: causation is not a productive relation, so requiring the agent to be
  in act when it acts presupposes the metaphysics of powers she rejects on
  independent grounds
- `objections` `OB-018` (the *causa sui* tradition meant aseity, not efficient
  self-production) · `replies` `RP-018` (conceded; `n2` records that this proof
  says nothing about aseity)
- `framework` `NEUTRAL` · `framework-role` `FR-NEUTRAL` · `layers` all three
- `fidelity` The skeleton renders "acts" as one predicate letter, dropping the
  `QUA-SEC` respect-qualification and the `PRI-CAU` ordering. — `RISK` callout on
  step 2.
- `audit` all fourteen axes `OK` except `FID` `FLAG` (paired with that callout) —
  verdict `V-PASS`

### 4.7 Forbidden to leave implicit

For each item: the omission, and the symptom a reviewer sees on the page without
consulting the record.

1. **The middle term.** Symptom: no `WHY` callout anywhere in the demonstration,
   and no sentence of the form "through *M*".
2. **The warrant of every premise.** Symptom: a numbered premise line in
   `L2-NUM` with no warrant token printed after it.
3. **The modality and scope of every premise and conclusion.** Symptom: an
   English modal ("must", "cannot") in `claim` or `established` with no token
   beside it.
4. **Every nonemptiness premise.** Symptom: `established` asserts that something
   exists while no premise line carries `∃`.
5. **Every change of necessity kind, modal scope, or priority kind.** Symptom: a
   token on a step's `to` that appears on none of its `from` lines and no
   `MODAL` callout beside it.
6. **The sense selected for an analogical term.** Symptom: a term declared
   `PRD-ANA` in `lexicon` appearing in the argument without a `TM-###.n` suffix,
   or rendered as a bare predicate letter with no `RISK` callout.
7. **`established`, printed separately from `claim`.** Symptom: the demonstration
   ends at its last step with no set-off restatement block.
8. **`not-established`, with a named missing bridge per entry.** Symptom: a
   bulleted list of stronger claims with no `BR-###` or `PR-###` stub attached,
   or a list absent entirely.
9. **`denial-set`, with a named position and its strongest reason.** Symptom: an
   objection paragraph that names no school, or names one and gives it a reason
   no member of that school has published.
10. **`commitments`, with `import` per row.** Symptom: the demonstration
    quantifies over an entity type that appears in no `IMPORT` callout.
11. **`depends-on`.** Symptom: a proposition used in a step whose id appears in
    no `USES` callout on the page.
12. **`series-kind` where a regress is at work.** Symptom: the words "infinite
    regress" on the page with no `SER-ACC` or `SER-ESS` token within the same
    environment.
13. **`framework` and `framework-role`.** Symptom: a `W-POST` premise on the
    page and no sentence saying whether the result holds inside the framework or
    helps establish it.
14. **`fidelity` wherever `L3-SKEL` is printed.** Symptom: a symbolic derivation
    with no sentence under it beginning "The symbolization drops…".
15. **The stripped variant or exclusion argument, wherever `rung: RG-WHY`.**
    Symptom: an `RG-WHY` object with no second numbered derivation on the page.
16. **The claim-level MD5 rewrite, wherever `import` is `REAL` or `MIXED`.**
    Symptom: an `ONT` row marked `OK` with no printed rewrite to cite.

### 4.8 The reduced object and the threshold

A **reduced object**, `PF-###/min`, is licensed for small items — the one-step
inferences of Stage A and B exercises, invalid near-neighbours, illustrative
fragments. It prints exactly ten fields, in this order: `id`, `name`, `kind`,
`rung`, `logic`, `claim`, `premises` (text and `warrant` only), `steps`,
`established`, `not-established`, plus a four-row axis probe (`SEM`, `LOG`,
`MOD`, `SCO`), labelled a probe and carrying no verdict token; a reduced
`SPECIMEN` still names its `ER-###`. `established` and `not-established` are the
ninth and tenth fields and are never the fields a reduction drops. Nothing else
is printed and nothing may be added selectively; an item needing any eleventh
field is a full object. A reduced specimen is written `PF-###/S/min`: §7.4's
`/S` precedes `/min`, and any line selector follows both (`PF-214/S/min.2`).

**Threshold, mechanical.** The reduced form is licensed if and only if all nine
conditions hold. Failing any one, the full object is mandatory; no editorial
judgement enters.

1. `kind ≠ DEMONSTRATION`.
2. `rung: RG-VALID`. Claiming any higher rung forfeits the reduced form.
3. `steps` count ≤ 2.
4. `premises` count ≤ 3.
5. Every premise's `warrant` ∈ {`W-SELF`, `W-DEF`, `W-DEM`, `W-HYP`}.
6. `import` ∈ {`CONCEPTUAL`, `LINGUISTIC`}.
7. The conclusion's necessity and `SCP-*` tokens are no stronger, under the
   §10.3 orders, than the weakest such tokens among all premises, and no step
   changes either. Identity with the tokens of some one premise is not
   sufficient.
8. The item introduces no new `TM-###` sense, `DF-###`, or `DS-###`, and no
   commitment row would carry `import: REAL`.
9. The item is `established-by` for no `PR-###` and appears in no other object's
   `depends-on`.

Condition 9 is checked at production time, not at authoring time: if a later
chapter comes to consume a reduced item, it is promoted to a full object under
the same id before the citation is printed. A reduced object whose `MOD` probe
row is anything but `OK` is likewise promoted, under the same id, before it is
printed. The anti-overreach pair survives reduction unchanged — a one-step
invalid near-neighbour still prints what it established, often nothing, and what
a reader might wrongly infer — and `EXHAUSTED` is admissible here, conditions 1
and 6 being exactly its admissibility conditions.

### 4.9 Decisions taken where the spine is silent

Flagged for cross-section checking: the dotted reference grammar of §4.1; the
three labelled runs of `lexicon`; `source` and `discharged-at` on the premise
subrecord; the step subrecord keys `{k, from, rule, to, modality, modal-scope,
bridge}`; the `commitment-kind` set {`EXISTS`, `REALLY-DISTINCT`,
`REALLY-DEPENDS`, `RANGES-OVER`} with the `paraphrase` column; the
`overreach-kind` set and its mandatory seven-line survey; the conditional fields
`stripped-variant` and `series-kind`; the `MUST` / `MUST-C` split of §4.2 and the
`kind` bindings of §4.2.1; the tokens `EMPTY`, `LOCAL`, `NO-BRIDGE-KNOWN`,
`NOT-IN-BOOK`, `CLOSED`, `EXHAUSTED`; the reduced object `PF-###/min` and its
composition with `/S`; the conditional fields `provenance` and
`reconstruction-note`, adopted verbatim from §8.8.1 and §8.8.2 R2; and the
broadening of the `W-REV`/`W-AUTH` prohibition from `kind: DEMONSTRATION` (spine
§2.4) to every kind (§4.2.1 (b)).
`framework-role` and its `FR-*` values are owned by §14, not decided here.


## 5. Formal Logic and Metaphysical Semantics: The Three-Layer Representation

The layer tokens `L1-PROSE`, `L2-NUM`, `L3-SKEL` are fixed. This section owns the
printing rules, cited elsewhere as §5(i)–(vi): **(i)** from Stage C onward all
three layers are printed for every `PF-###` with `kind: DEMONSTRATION`, and
Stages A and B MAY omit `L1-PROSE`; **(ii)** `L3-SKEL` is never printed without
`L2-NUM` beside it; **(iii)** every `L3-SKEL` carries its `fidelity` sentence
naming what the symbolization drops, and the `FID` row records the
back-translation; **(iv)** any `PRD-ANA` term rendered as a single predicate
letter requires a `RISK` callout and an entry in `not-established`; **(v)** where
`L1-PROSE` and `L2-NUM` diverge, `L2-NUM` governs and the divergence is printed
as a `RISK` note; **(vi)** the margin note beside a symbolized disputed premise
is `RISK` or `OBJ`, never `INF`.

**Structural decision (spine-silent, flagged).** `L3-SKEL` names *one* printed
layer with *two* components: the **logical skeleton** (`L3-SKEL/logic`, a
derivation in the calculus named in `logic`) and the **dependency skeleton**
(`L3-SKEL/dep`, a typed graph over ledger ids). Rule (i) requires the layer from
Stage C onward; that requirement is discharged by `L3-SKEL/dep` plus either
`L3-SKEL/logic` or a non-symbolization notice (§5.4). Nothing here licenses
omitting the layer.

### 5.1 Capacity, incapacity, entitlement

| Layer | Establishes | Entitles the reader, from that layer alone, to conclude |
|---|---|---|
| `L1-PROSE` | what the claim is about, which sense is intended, why the question arises | **only that a question has been posed under fixed senses.** Not validity, not truth, not rung. |
| `L2-NUM` | premise-by-premise responsibility; warrant, modality, scope, middle per line; what an opponent must deny | that the conclusion follows *given the declared readings and cited rules*, when the printed audit shows `LOG` = `OK`; and what the `denial-set` costs. Never soundness, never import. |
| `L3-SKEL/logic` | validity of the shape in the declared calculus; quantifier and modal scope; divergence from a near-neighbour shape; presence of cycles | that the shape is or is not valid **in that calculus under that symbolization**. Maximum achievable rung from this component alone is `RG-VALID`; the matching verdict is `V-VALID-ONLY`. |
| `L3-SKEL/dep` | what the proof consumes, and whether the consumption graph is acyclic and free of forward reference | the results of `LC-01` and `LC-02` and nothing else. An edge drawn from `depends-on` is a fact about proof order, not a fact about the world; only a `PRI-*`-labelled edge asserts real dependence, and it asserts it on the warrant of its `PR-###`, not on the warrant of being drawn. |

Binding consequences.

1. No `PR-###` may carry an `established-by` naming a `PF-###` that prints only
   `L1-PROSE`. Prose is never the establishing layer.
2. `L2-NUM` is the only layer at which an argument's demonstrative status can be
   assessed — whether MD1–MD10 hold is read off the numbered form, since only
   there does every premise carry its warrant, modality, scope, and import and
   every step its rule. A skeleton may therefore never be cited in place of a
   numbered line: a cross-reference of the form "see the derivation" without a
   `PF-###.k` is a `LOG` defect. Being a demonstration is a property of the
   argument, fixed by §2.1 and by the computed achieved rung; no layer confers
   it and no layer withdraws it, and a proof object does not change rung when a
   layer is added or omitted.
3. Where the symbolization and the canonical `claim` diverge, the
   ordinary-language `claim` governs and is unchanged (§5.5, flag
   `claim-divergence`). Where narrative prose and `L2-NUM` diverge, `L2-NUM`
   governs (rule (v)). These two canonicity rules do not conflict: `claim` is
   an `L2-NUM` field written in ordinary language.

### 5.2 The prohibition: formalization exhibits structure, it does not confer warrant

Stated as rules with detectors. Violations route to the axis named.

- **R5.2.1 Warrant invariance.** Symbolizing a premise changes no field of its
  subrecord. If the `warrant`, `import`, `modality`, `modal-scope`, or
  `contested` value differs between the `L2-NUM` premise and its skeleton
  counterpart, the difference is a defect, not a discovery. *Detector:* compare
  the two; any change attributable to symbolization is `FID` = `FAIL`, and
  `PRV` = `FAIL` if the changed field is `warrant`.
- **R5.2.2 No unaccompanied skeleton.** Rule (ii). *Typographic consequence:*
  `L2-NUM` and `L3-SKEL` are set as one indivisible block that
  never breaks across a spread; the skeleton is set at a narrower measure,
  indented under the numbered form, ruled off above, and carries no
  theorem-style header of its own.
- **R5.2.3 Symbols never outrank prose.** No proof is titled, indexed,
  cross-referenced, summarized in a running head, or listed in the table of
  contents by its formula. No skeleton is set in display size larger than the
  numbered form.
- **R5.2.4 Total glossing.** Every predicate letter, individual constant,
  function symbol, and relation symbol has a glossary line mapping it to a
  `TM-###.n` sense selector or a cited `DF-###`. *Detector:* a legend line
  reading "let `Fx` = *x* changes" with no sense selector is `SEM` = `FAIL`.
- **R5.2.5 Callout discipline.** `INF` attaches only to a line justified by a
  rule application; a premise line never takes `INF`. The margin note beside a
  symbolized disputed premise is `RISK` or `OBJ` (rule (vi)).
- **R5.2.6 Rider.** Any skeleton whose argument contains a premise with
  `contested: true` prints the validity-only rider of §5.5(a) directly beneath
  the derivation. The rider is a required element of the printed `L3-SKEL`
  block, not a commentary on it: a skeleton printed without it where the trigger
  fires is an incomplete layer, and the mark is `FID` = `FAIL`, routed to
  `V-REPAIR` whose repair is printing the rider. `DIA` = `FAIL` applies
  additionally when the contested premise is absent from `denial-set`.
  *Reviewer test:* count the printed `L3-SKEL` blocks whose proof has any
  premise with `contested: true` or `warrant` ∈ {`W-POST`, `W-IND`, `W-HYP`},
  and grep the chapter for the literal string "Validity is not warrant"; the two
  counts must be equal.
- **R5.2.7 Cross-section constraint (flagged for the exercise lane).** A
  `FORMALIZE` exercise MUST carry a second part demanding the `fidelity`
  sentence for the symbolization the reader produced. A `FORMALIZE` item scored
  solely on the well-formedness of its output is defective.

### 5.3 Test R: is `L3-SKEL/logic` required, optional, or harmful?

Run in order; the first clause that fires decides.

- **R-0 Precondition.** A term declared `PRD-ANA` occurs in two premises under
  different analogates and the inference's validity turns on both occurrences.
  → **HARMFUL as a single letter.** Either split into two predicates plus an
  explicit ratio premise carrying its own warrant, or take the R-4 exit. Never
  print the collapsed version silently; flag `analogy-collapse` if printed at
  all.
- **R-1 Discrimination triggers.** `L3-SKEL/logic` is **REQUIRED** if any holds:
  (i) a near-neighbour shape exists that a competent reader could confuse with
  this one (`P → Q, Q ⊢ P` beside `P → Q, P ⊢ Q`); (ii) the argument contains a
  quantifier alternation; (iii) it contains a modal operator whose scope admits
  both `SCP-CMP` and `SCP-DIV` readings; (iv) it contains a nested conditional,
  reductio, or discharged `W-HYP`; (v) it is consumed by two or more later
  `PF-###`.
- **R-2 Shortfall measurement.** It decides nothing and issues no print
  instruction. List the load-bearing items — every `DS-###` in `lexicon`, every
  `PRI-*` token, every `DK-*` tag, every `QUA-SEC` respect, every degree or
  *per se* ordering, every second-order quantification — and record which of
  them have no representation in the declared calculus. That record is the
  **shortfall list**.
- **R-3 Required-partial.** If any R-1 trigger fired, `L3-SKEL/logic` is
  **REQUIRED** even when the shortfall list is non-empty: print the derivation,
  mark each affected line `[not-FOL]`, name every shortfall item in `fidelity`,
  and raise flag (d).
- **R-4 Exit.** If no R-1 trigger fired and the shortfall list is non-empty,
  `L3-SKEL/logic` is **HARMFUL**: omit the derivation and print the §5.4 notice.
- **R-5 Default.** If no R-1 trigger fired and the shortfall list is empty,
  `L3-SKEL/logic` is **OPTIONAL**; print it if it shortens the audit.

*Worked application.* "Being is said in many ways." R-0 fires on `being`; R-1
fires on nothing; R-2 finds that writing `Bx` makes being a first-order property
with a determinate extension, which is exactly what the claim denies. R-4: take
the exit. A shortfall list containing a `PRI-*` token is the normal case for
Stage C–F demonstrations, since no `PRI-*` relation is representable in the
default calculus; R-3 and R-4 therefore govern most of the book.

### 5.4 The non-symbolization notice

A dedicated environment, named by §12; its content is fixed here. Four required
fields, in order: **attempted** — the calculus tried; **resists** — the
exact feature that blocks it, named from the R-2 list; **would require** — what
the calculus would have to add; **substitute discipline** — the rule names cited
line by line at `L2-NUM`, plus the dependency skeleton, which remain mandatory.

Two anti-abuse rules. A notice never raises the rung and never excuses an
unlabelled step: MD1 still binds at `L2-NUM`. Every proof carrying a notice
prints in `not-established`, as an `OV-IMPORT` entry in the five-key grammar of
§4.5, that validity here is checked by hand under named rules and has not been
machine-checkable.

### 5.5 Skeleton flags

Five flags. Not record fields: printed annotations whose audit consequences land
on existing axes. Surfacing uses only the closed margin set of §11, two inline
markers minted here — `[approx]` and `[not-FOL]`, both grayscale-legible words,
not glyphs — and dedicated environments.

| Flag | Exact trigger | Surface | Audit consequence |
|---|---|---|---|
| (a) `disputed-premise` | `LOG` = `OK` and some premise has `contested: true`, or `warrant` ∈ {`W-POST`, `W-IND`, `W-HYP`} | margin `RISK` (or `OBJ` if an `OB-###` exists) on the premise line, **plus** the validity-only rider beneath the derivation, printed verbatim in whichever of two fixed forms applies: (i) where the premise stands in `denial-set` — "Valid in ⟨calculus⟩. Validity is not warrant: ⟨pid⟩ carries ⟨token⟩ and stands in `denial-set`."; (ii) where it does not — "Valid in ⟨calculus⟩. Validity is not warrant: ⟨pid⟩ carries ⟨token⟩ and is not established here; see ⟨OB-###⟩ or `not-established`." | `LOG` `OK`; `WAR` `FLAG` minimum. **Ceiling**, restating §6.3 verdict rule 4 and no more: only where a load-bearing premise carries `W-POST` and the book does not undertake to settle it may the verdict not exceed `V-OPEN`. A contested premise warranted `W-SELF`, `W-DEF`, `W-IND`, `W-EMP`, or `W-DEM` imposes no ceiling; it routes to §6.3 rule 5 where a disjunct of that rule obtains — a named bridge missing, or an `OB-###` standing with no `RP-###` — and otherwise leaves the verdict free |
| (b) `analogy-collapse` | a `PRD-ANA` term is rendered as one predicate letter (rule (iv)) | margin `RISK`; glossary line prints the ratio; mandatory `not-established` entry, `OV-IMPORT` in the five-key grammar of §4.5 | `SEM` `FLAG`, `FID` `FLAG`; `SEM` `FAIL` if no ratio is stated |
| (c) `ambiguity-suppressed` | the `L1-PROSE` sentence admits two regimentations that are not logically equivalent, and the skeleton adopts one | **Rival Regimentations** environment: both symbolizations, the adopted one named, and the ground of adoption — which must be a cited `TM-###.n` or `DF-###`, never "charity" or "the natural reading" | `SEM` `FLAG`; `SEM` `FAIL` if the adopted reading is the one validity needs and the rejected one is the more natural |
| (d) `not-first-orderable` | an R-2 item is load-bearing and unrepresentable | partial case: inline `[not-FOL]` on the line plus `IMPORT` or `MODAL` callout; total case: the §5.4 notice | `FID` `FLAG`. Binding: this flag licenses **neither** "not derivable in FOL, therefore not a principle" **nor** "derivable in FOL, therefore metaphysically established" |
| (e) `claim-divergence` | back-translation test fails (§5.6) | remedy environment, three parts, order fixed below | `FID` `FAIL` if unremedied; `FID` `FLAG` if retained as declared approximation; never `FID` `OK` |

**Required remedy for (e).** (1) *State the divergence*: print the
back-translated sentence beside the canonical `claim` and name the differing
element — modality, scope, respect, priority kind, or analogate. (2) *Declare
canonicity*: the ordinary-language `claim` governs; the symbolization does not
amend it; `claim` is not rewritten and mints no new id. (3) *Repair or
approximate*: either reprint a corrected symbolization, noting that the first
attempt is superseded, or retain it marked `[approx]` with the exact shortfall
in one `fidelity` sentence and an `OV-IMPORT` entry in `not-established`, written
in the five-key grammar of §4.5. An approximation
whose shortfall is described as "some loss of nuance" fails: the shortfall names
a token or a distinction.

*Worked (e).* Claim: "Whatever is in potency is reduced to act by something
already in act." Symbolized `∀x(Px → ∃y(Ay ∧ Ryx))`. Back-translation: "for
every potential *x* there is an actual *y* standing in *R* to *x*." Divergence:
the `QUA-SEC` respect is gone — *y* must be in act *with respect to the same
perfection* — and `R`'s `PRI-CAU` character is gone. Repair the first:
`∀x∀f(Pot(x,f) → ∃y(Act(y,f) ∧ Red(y,x,f)))`. The second is irreparable in
first-order logic; retain `[approx]` with `fidelity`: "`Red` is written as a bare
relation; that it is causal and not merely concomitant is asserted at `L2-NUM`
and carried by its `PR-###`, not by the symbolism."

### 5.6 Formal apparatus

**Back-translation test**, referenced above and by axis `FID`: read each symbol
by rule `R5.2.4` (§5.2), render the formula mechanically into English, and
ask whether the author asserts *that sentence* with the same modality, scope, and
import. If not, flag (e).

| Apparatus | Used where | Distinction it buys | Cost, which MUST be stated once in front matter |
|---|---|---|---|
| Classical first-order logic with identity | default `logic` (MD1) | validity of shape; quantifier alternation; identity claims | predicate letters are univocal by construction, so FOL cannot represent `PRD-ANA`, tense, degree, *per se* predication, or any `PRI-*` relation, which is why `fidelity` is mandatory. |
| Negative free logic with an explicit existence predicate `E!` | any proof whose `claim` has `import: REAL` and whose subject term's instantiation is at issue; required wherever MD3 bites | separates "the first cause is uncaused" from "a first cause exists"; makes every existential step cite its nonemptiness premise | `∀xφ ⊢ φ(a)` fails without `E!a`, so classically trained readers must be warned; and negative free logic decides that atomic predications of non-denoting terms are false — a commitment a Meinongian rejects. Where a step turns on that decision, record it as a `PR-###` with `W-POST` and place it in `denial-set`. |
| Modal system **T** (K + `□A → A`) | default modal calculus | factive necessity, `SCP-CMP`/`SCP-DIV` scope (§3.9) | T cannot express iterated modal claims usefully, so any proof about the modal status of a modal status must escalate — and thereby declare. |
| Variable-domain quantified modal logic; Barcan and Converse Barcan **invalid** by default | all quantified modal proofs | blocks the silent slide from "possibly something is *F*" to "something is possibly *F*" | instantiation across `□` needs explicit existence premises; proofs are longer. Either formula requires a cited `BR-###`. |
| Parthood as a defined relation `P(x,y)` with axioms cited as `PR-###` | composition and mereological proofs | keeps transitivity, supplementation, extensionality, and unrestricted fusion as separately warranted claims | verbosity; no off-the-shelf CEM theorems. Deliberate: CEM would otherwise import composition-as-identity for free. |
| Grounding operator `A ≺ B`, non-truth-functional | only in proofs that declare it | writes `PRI-GND` inside a derivation | its structural rules are *stipulated* (§3.9), and stipulated structural rules are substantive: transitivity of grounding is contested. Each structural rule actually used is cited as its own `PR-###` with `W-POST`. |

#### 5.6.1 Closed apparatus; no free rules

1. **Closure.** `logic` may name only an apparatus listed in the §5.6 table, a
   documented restriction of one, or a stated combination of them. Naming any
   other system, operator, axiom schema, or rule requires a spec amendment
   (§1.5(3)) and is never an authorial decision.
2. **No free rules.** Every inference rule, axiom schema, structural rule, or
   primitive operator used at `L3-SKEL/logic` or cited in a `steps` line's
   `rule` slot that is not a rule of classical first-order logic with identity
   MUST be recorded as its own `PR-###` carrying a warrant token — `W-POST`
   unless separately demonstrated by a cited `PF-###` — listed in the consuming
   proof's `depends-on`, and placed in `denial-set` wherever the derivation
   fails without it.
3. **Declaration.** Such a proof prints beneath the derivation the
   calculus-commitment line fixed immediately below for modal escalation: rule
   name, the rule in symbols and in English, its `PR-###`, and confirmation of
   `denial-set` membership, with a `MODAL` or `IMPORT` callout on the first line
   that uses it.
4. **Detector and sanction.** Strike from the declared calculus every rule not
   belonging to classical first-order logic with identity and re-run the
   derivation; any step that now fails was carried by a premise disguised as a
   rule. A rule used without the record required by (2) is `WAR` = `FAIL` and
   `PRV` = `FAIL`, routed to `V-REPAIR` whose repair is demotion of the rule to
   a premise.

This clause governs the reading of §13.1's sentence listing "a rule of the
declared calculus" among the things that settle a question in this book: a rule
settles a question only if it belongs to classical first-order logic with
identity or carries the record required by (2), and in the second case what
settles the question is that `PR-###` and its warrant.

**Escalation above T.** Any proof whose `logic` names a system stronger than T
prints a **modal-commitment line** immediately beneath the derivation: system
name, characteristic axiom in symbols and in English, the `PR-###` recording it
as `W-POST`, and confirmation that it appears in `denial-set`, with a `MODAL`
callout on the first line that uses it. Silence is not assent-by-default; an
unflagged escalation is `MOD` = `FAIL`.

| System | Characteristic axiom | Commits the author to |
|---|---|---|
| S4 | `□A → □□A` | modal status is itself non-contingent |
| B | `A → □◇A` | actuality is accessible from every world it can reach |
| S5 | `◇A → □◇A` | one possibility space, invariant across worlds — the axiom on which modal arguments for a necessary being turn, and therefore never a background convenience |

Also binding: "necessary being" is cashed out *de re* with explicit scope
(§3.9), so `∃x□E!x` and `□∃xE!x` are always distinct skeletons; printing one
where the prose supports the other is flag (c) and, if validity depends on the
choice, `SEM` = `FAIL`.

### 5.7 The dependency skeleton

`L3-SKEL/dep` is a typed directed graph, not an illustration of the derivation.

**Nodes.** Ledger ids only — `PR-###`, `DF-###`, `DS-###`, `BR-###`, `PF-###`,
`OB-###` — each printing its id and, for `PR-###`, its `rung` or `status`. A node
whose record carries `warrant: W-POST` is drawn in a visibly distinct node
shape, so that framework dependence is legible without reading labels.

**Edges, four kinds, never merged into one arrow style.** Each is
shape-distinguished and grayscale-legible; no meaning is carried by color.

| Edge | Drawn from → to | Source | Asserts |
|---|---|---|---|
| `uses` | consumed id → consumer | `depends-on` | proof order only |
| `bridges` | licensing `BR-###` → the step it licenses | MD6 | a change of `NEC-*` kind, `SCP-*` scope, or `PRI-*` token |
| `priority` | prior → posterior, labelled with its `PRI-*` token | the proof's content | a real relation, warranted by its own `PR-###` |
| `denies` | `OB-###` → the premise or step targeted | `objections` | a dialectical attack, not a dependence |

*Detector:* a diagram whose legend offers one arrow type while its caption speaks
of dependence in two senses conflates proof order with ontological priority; that
is `DEP` = `FAIL`.

**When each artifact appears.** `L3-SKEL/logic`: by Test R. `L3-SKEL/dep`:
required for every `PF-###` from Stage C onward; required as a cumulative graph
at the close of every chapter that establishes two or more `PR-###`; required for
every Stage E chain and every Stage F bridge, where its function is to make House
Rule 6 visible — each attribute reached by its own edge from its own `PF-###`,
never a single node labelled with a compound conclusion. In Stages A and B a
dependency skeleton MAY be replaced by the line "consumes: none" when
`depends-on` is empty and no `PRI-*` claim is made.


## 6. The Proof-Audit Rubric

### 6.1 Standing of the fourteen axes

The rubric is fourteen axes in the fixed order of §6.2, four marks (`OK`,
`FLAG`, `FAIL`, `N/A`), and six verdict tokens. No section may add a fifteenth
axis, rename one, or mint a verdict.

Homes for the required layers: semantics → `SEM`; consequence → `LOG`; warrant →
`WAR`; import → `ONT`, with `EXI` owning the existence sub-case; modality →
`MOD`; explanation → `EXP`; dependence → `DEP`; scope → `SCO`; dialectical
burden → `DIA`; demonstrative grade → `DEM`. Two distinctions are deliberately
not axes: *per se* commensuration is a sub-test of `SCO`, and the *that* / *why*
distinction is carried by `rung` and adjudicated by `DEM`, nowhere else. `EXI`, `FRM`, `FID`, `PRV` are
axes because each owns a failure no other axis detects — an undeclared import
assumption, an unmarked framework premise, a lossy symbolization, and a citation
in a warrant slot each survive a flawless derivation from true premises.

### 6.2 The rubric table

Verdicts are computed for the whole proof object (§6.5), never per axis; the last
column bounds which verdicts a failure on this axis can reach.

| Axis | Core question | Auditor inspects | Failure signature | Verdicts reachable on `FAIL` |
|---|---|---|---|---|
| `SEM` | Is every term's sense fixed, or its analogy declared with a stated ratio? | `lexicon` against the `TM-###.n` selector at every occurrence in `premises` and `steps` | One word, selector `.1` at `p1` and `.2` at `p3`; or `PRD-ANA` with no ratio printed | `V-REPAIR`; `V-FATAL` when no single sense leaves every premise true |
| `LOG` | Does each step follow by the rule it names in the declared calculus? | Each `steps` line `{from, rule, to}` against `logic` | An unlabelled step; a rule that does not license its transition; "hence" doing the work | `V-REPAIR`; `V-FATAL` when the premise restoring validity is `claim` |
| `EXI` | Is every existence claim earned? | `domain`, each quantifier's import declaration, each constant's entry point, each definite description | A universal read with import; "the first cause" before its uniqueness lemma; a constant with no cited existential instantiation | `V-REPAIR`; `V-FATAL` when the only nonemptiness premise available is `claim` |
| `WAR` | What warrants each substantive premise? | Each premise's `warrant` token; the printed analysis for `W-SELF`; the inductive base for `W-IND`; for `W-DEF`, the cited `DF-###` itself — derive its `statement` from its `TM-###.n` sense plus prior ids, and confirm the premise's `import` is `CONCEPTUAL` or `LINGUISTIC` and its `modality` is `NEC-CON`; for `W-DEM`, the cited record's `rung`, `import`, and `audit-verdict` | A premise with no token; `W-SELF` with no analysis; a warrant stated and then defeated in `replies`; a `W-DEF` premise whose cited definition carries content underivable from its sense (`LC-08`, `ER-106`) or which is recorded `REAL`/`MIXED` or at a necessity kind other than `NEC-CON`; a `W-DEM` premise whose cited record has `rung: RG-VALID`, `import` other than `REAL` or `MIXED`, or `audit-verdict` in {`V-VALID-ONLY`, `V-FATAL`, `V-REPAIR`} while the consuming premise subrecord records `import: REAL` | `V-REPAIR`; `V-OPEN` when the repair reclassifies the premise `W-POST`; `V-FATAL` when no admissible warrant exists |
| `MOD` | Has necessity kind or modal scope shifted without a licence? | `modality` and `modal-scope` on `claim` and each premise; each `NEC-*`/`POS-*`/`SCP-*` change against its cited `BR-###` | The weakest-link test of §2.1 (MD6) fails: a step whose `to` carries a modality or scope stronger than the weakest among all lines in its `from`, or a `claim` stronger than the weakest load-bearing premise, with no cited `BR-###` whose antecedent is discharged inside the object; `SCP-CMP` premises yielding a `SCP-DIV` conclusion; `NEC-MET` on a claim passing the `NEC-CON` test | `V-REPAIR`; `V-FATAL` only when the correctly weakened claim is trivial (§6.4) |
| `ONT` | Is a real claim being made where a real claim is needed? | `import` on `claim` and premises; `commitments` and their `DK-*` tags; the MD5 paraphrase rewrite. `import: MIXED` is handled per §4.2 — MD5 runs on the real component, and `MIXED` alone never satisfies it | The concept-talk paraphrase is carried by the same premises with the same force; a `DK-NOM` distinction doing `DK-REAL` work | `V-REPAIR`; `V-FATAL`. Never `V-VALID-ONLY`, which requires no `FAIL`: a conceptual residue after an `ONT` failure prints in `survives` |
| `EXP` | Does the middle ground the conclusion, or merely accompany it? | `middle`, `middle-kind`, the middle's `PRI-*` token, the reversal test, the stripped variant. The default discharge of MD11(c) is the printed stripped variant; the only alternative is the bounded exclusion argument of §4.2, and an unbounded assertion that every route passes through `middle` discharges nothing | Both directions of "…because…" read equally well; no stripped variant and no argument that every route passes through the middle | `V-REPAIR` (reclassify `RG-THAT`, withdraw explanatory language) in every case in which `claim` survives reclassification, including where `claim` predicates a grounding relation of its subject: a demonstration that `A` grounds `B`, reached through an `EFFECT-SIGN` or `PROPER-ATTRIBUTE` middle, is a complete `RG-THAT` result whose `OV-EXPL` entry then reads "why `B` is grounded in `A`". `V-FATAL` only where the sole content of `claim` is that `middle` grounds the subject's having the attribute, so that withdrawing the grounding assertion leaves nothing predicated |
| `DEP` | Is the dependency ordering the one asserted, and acyclic? | Each `PRI-*` token against its deciding test; `depends-on` plus warrant edges; the `SER-ACC`/`SER-ESS` declaration and concurrency test | `PRI-TMP` or `PRI-EPI` taken as evidence of `PRI-CAU`; `PRI-ONT` read as `PRI-GND`; a regress argument declaring no series kind | `V-REPAIR`; `V-FATAL` when the only break in a cycle assumes `claim` |
| `SCO` | Is the conclusion exactly as strong as the premises license? | `claim` against `established`; `subject` and `attribute` against what the steps deliver; `not-established` | `established` restates `claim` with a widened subject; `not-established` empty, `NONE`, or listing only claims nobody would assert | `V-REPAIR` always, weakening being always available; `V-FATAL` only when the weakened claim is trivial |
| `DIA` | What minimally must an opponent deny, and is that opponent's reason at full strength? | `denial-set` for minimality (remove each member; a step must break); the named standing position and the reason attributed to it | A member whose removal breaks nothing; an opponent named with a reason weaker than that opponent's own literature gives | `V-REPAIR`; `V-FATAL` when the minimal `denial-set` is genuinely empty, `claim` being then deniable by nothing |
| `DEM` | Is the achieved rung the claimed rung? | `rung` against the other thirteen results of this sweep | `rung` unstated; explanatory prose over an `RG-THAT` proof; `RG-WHY` claimed with `EXP` not `OK` | `V-REPAIR` (reclassify, withdraw explanatory language) |
| `FRM` | Is the argument inside a framework or establishing part of one, and does it say which? | `framework`; `framework-status` on each premise; the sentence declaring internal versus establishing | A `W-POST` premise with `framework: NEUTRAL`; no sentence placing the result on one side of that line | `V-REPAIR`, ordinarily `V-OPEN` on recomputation |
| `FID` | Does the symbolization say what the author asserts? | `L3-SKEL` back-translated and compared with `L1-PROSE` and `L2-NUM`; the `fidelity` sentence | Back-translation yields a claim the author would refuse; `fidelity` absent; a `PRD-ANA` term as one predicate letter with no `RISK` callout | `V-REPAIR` (amend or withdraw the symbolization) |
| `PRV` | Does any citation or revealed premise occupy a warrant slot? | Every `warrant` token for `W-REV`/`W-AUTH`; every `scholion`; every citation in `premises` | A canonical author's name where a warrant belongs; a `W-REV` premise inside `kind: DEMONSTRATION` | `V-REPAIR` when that premise is removable or replaceable by another §2.1.2 warrant; `V-FATAL` when load-bearing and irreplaceable |

**`W-DEM` admissibility.** A `W-DEM` premise may not be recorded at an
`import`, `modality`, or `modal-scope` stronger than the cited record's own
(`WAR` = `FAIL` and `SCO` = `FAIL`). Citing a `V-VALID-ONLY`, `V-REPAIR`, or
`V-FATAL` record as `W-DEM` for a premise used with `import: REAL` is
`WAR` = `FAIL`, repairable only by demoting the premise to `W-POST` or
re-warranting it; citing a `V-OPEN` record is admissible but inherits the
openness (§6.5). House rule 5 is audited on the page at `WAR`, not only at build
time by `LC-08`: an auditor who marks `WAR` without opening every cited `DF-###`
has not run the axis.

**Mark admissibility, binding.** `LOG`, `DEM`, `PRV` are binary — `OK` or `FAIL`,
never `FLAG`: a step is licensed or not, a rung achieved or not, a warrant slot
occupied by a citation or not. Every other axis admits `FLAG` for a real, stated
limitation. `N/A` appears only in two cases, `EXP` at `rung: RG-THAT` and `FID` with no
`L3-SKEL`; no other cell may read `N/A`.

#### 6.2.1 Computing the achieved rung

The achieved rung is computed by the audit and never chosen by the author. It is
printed on the verdict line beside the claimed `rung` (§6.6). No new
proof-object field is minted for it; it is a function of the fourteen marks,
taken as an ordered first-match ladder:

1. `RG-VALID` iff `LOG` and `SEM` are not `FAIL`. If this clause fails, **no
   rung is achieved**, and the verdict line prints none.
2. `RG-WARRANTED` iff additionally `WAR`, `PRV`, `EXI`, `FRM` are not `FAIL`.
3. `RG-THAT` iff additionally `MOD`, `ONT`, `DEP`, `SCO`, `DIA`, `FID` are not
   `FAIL` and `import` is `REAL` or `MIXED`.
4. `RG-WHY` iff additionally `EXP` is `OK`.
5. `RG-SOUND` is never computed: no audit certifies that a premise is true.

A `FLAG` on any axis lowers no rung, a `FLAG` being a stated limitation and not
a defect; and a `W-POST` premise is an undefeated warrant for MD4 and blocks no
rung, its cost being carried by the verdict (§6.3 rule 4) and by the §14.4
conditionality note, not by demotion.

`DEM` = `FAIL` iff the claimed `rung` exceeds the achieved rung, or `rung` is
unstated. The ledger key `rung` takes the **achieved** rung, and every sentence
licensed by §2.7 to use "establishes" or "shows" prints the achieved rung, never
the claimed one.

### 6.3 Verdict definitions

Each verdict has a necessary-and-sufficient condition, stated below as it
applies *at its position* in the first-match order.

**Ceilings and riders do not compute.** No flag, rider, note, or ceiling stated
in any other section alters a computed verdict; the six rules and their printed
inputs (§6.6) are the whole computation. The following are additional
**disjuncts of the named rules**, part of the computation rather than overrides
of it.

- Rule 4 (`V-OPEN`) also fires with no axis at `FAIL` when any axis carries a
  `FLAG` arising from a `class-status: CONTESTED` error class (§7.8), or an
  `FR-INTERNAL` object consumes a posit still marked `POSITED` (§14.3).
- Rule 5 (`V-PARTIAL`) also fires with no axis at `FAIL` when any `RP-###`
  carries `disposition: RD-OPEN` (§14.7), or a premise carries `warrant` in
  {`W-IND`, `W-HYP`} and stands in `denial-set`.

The words "ceiling" and "may not exceed", wherever they appear in §5.5, §7.8,
§14.4, or §14.7, name these disjuncts and confer no independent authority.
Because a pass may therefore stand over a live denial-set, the verdict line of
any `V-PASS` whose proof triggered §5.5 flag (a) appends the fixed clause
"(denial-set live: ⟨pid list⟩)".

**`V-FATAL` (fatal defect).** Necessary and sufficient: at least one axis is
`FAIL`, and no admissible repair (§6.4) preserves the intended conclusion. Prints
`errors`, `why-no-repair`, `survives`. *Micro-example.* A proof whose premise
"every causal series has a first member" is warranted `W-DEM` citing a
proposition whose ledger record lists this proof's own `claim` in `depends-on`.
`WAR` and `DEP` fail; every premise strong enough to restore the step asserts
`claim`; `survives: NONE`. An author may not escape the `V-FATAL` branch of `EXP` by
raising `rung` to `RG-WHY`: the rung is fixed by MD11 applied to `middle`, never
by the vocabulary of `claim`.

**`V-REPAIR` (repairable defect).** Necessary and sufficient: at least one axis
is `FAIL`, and the auditor exhibits a specific admissible conclusion-preserving
repair. Prints `errors`, `repair`, `survives`. *Micro-example.* From "necessarily,
whatever is moved is moved by another" (`SCP-CMP`) and "this is moved" (`ACT`),
the text concludes "necessarily, this is moved by another" (`SCP-DIV`). `MOD`
fails; the repair restates `established` at `ACT`.

**`V-VALID-ONLY` (valid but not demonstrative).** Necessary and sufficient: no
axis is `FAIL`, and either `import` is `CONCEPTUAL` or `LINGUISTIC`, or `ONT` or
`EXI` carries a `FLAG` leaving no real claim standing. Prints
`conceptual-result`. *Micro-example.* "Nothing is both F and not-F in the same
respect at the same time; this is F in respect R at t; ∴ this is not not-F in
respect R at t." Impeccable, `import: CONCEPTUAL`; `conceptual-result` records
that a constraint on consistent description has been established and no feature
of the thing has. This verdict enforces house rule 2.

**`V-OPEN`.** Necessary and sufficient: no axis is `FAIL`, a load-bearing premise
carries `W-POST`, and the book does not undertake to settle it. Prints the
premise and the live positions on each side. *Micro-example.* A dependence
argument load-bearing on a restricted principle of sufficient reason marked
`W-POST`, with the reason on each side printed at full strength.

**`V-PARTIAL` (correct but incomplete).** Necessary and sufficient: no axis is
`FAIL`, everything asserted is licensed, and either a named bridge to a *further*
claim is missing or an `OB-###` stands with no `RP-###`. Prints `missing` as a
`PR-###` stub. *Micro-example.* A proof reaching a non-derivative member of an
essentially ordered series records in `not-established` that nothing is shown
about that member's simplicity, and prints
`missing: PR-### (bridge from non-derivative actualizer to simplicity)`.
Incompleteness is an announced gap to a claim *not* made. If the
stronger claim is asserted while the bridge is missing, `SCO` fails and the
verdict is `V-REPAIR` or `V-FATAL`, never `V-PARTIAL`.

**`V-PASS`.** Necessary and sufficient: no axis is `FAIL` and none of rules 3–5
matches. *Micro-example.* A bounded demonstration that a thing acquiring a
feature it previously lacked is composite of a persisting subject and that
feature: `middle` = the subject's persistence (`middle-kind: FORMAL`,
`PRI-GND`), `import: REAL`, `denial-set` = {the persistence premise}, opponent a
named bundle theorist with his own reason at full strength.

**Binding print rule.** A pass at `RG-THAT` is complete of its own species and
is graded neither up nor down; the achieved rung printed beside the verdict
(§6.6) stops a reader taking `V-PASS` for "and it has been shown why". No
seventh verdict is needed: a claimed `RG-WHY` with `EXP` not `OK` fails `DEM`
and lands at `V-REPAIR`.

### 6.4 Repairable versus fatal

The criterion is the existence of a repair, not its cost. A repair requiring a
new chapter and three new lemmas is still a repair; a one-word fix that empties
the conclusion is not.

**Admissible repair.** A repair `r` is a finite edit to `premises`, `steps`,
`lexicon`, `middle`, `modality`, `established`, `not-established`, `rung`, or
`kind`. It is admissible iff:

1. every premise of the repaired object carries a §2.1.2 warrant token other than
   `W-REV` and `W-AUTH`;
2. no added premise has a warrant presupposing `claim`, or presupposing any id
   whose ledger record lists `claim` in `depends-on`;
3. the repaired object has no axis at `FAIL`;
4. `established` after repair has `import: REAL`.

**Conclusion preservation.** `r` preserves the intended conclusion iff the
repaired `established` predicates the same `attribute` of the same `subject` as
`claim`, at no stronger modality and no wider scope, and is non-trivial.

**Non-trivial.** The repaired `established` is non-trivial iff (a) it is not
derivable from `lexicon` plus logic alone, (b) its `denial-set` is non-empty and
at least one member is rejected by a named standing position, and (c) it is not
an instance of a logical truth.

**Decision.** `FAIL` present and some admissible conclusion-preserving repair
exists → `V-REPAIR`, and the audit exhibits one such repair, not merely asserts
that one exists. `FAIL` present and none exists → `V-FATAL`, and
`why-no-repair` names which of conditions 1–4 or (a)–(c) every candidate repair
violates. Missing bridges are repairs, not fatalities: the repair is the
`PR-###` stub plus a scoped-down `established`. Only two fatal patterns stand:
(i) every sufficient premise asserts `claim`; (ii) every scoping-down that
removes the defect lands on a claim failing (a)–(c).

### 6.5 Aggregation

The overall verdict is a function of the fourteen marks together with the
printed rule inputs of §6.6 and the inherited verdicts of the `depends-on`
closure, computed in the first-match order of §6.3. It is **not** a majority, **not** a score, **not** an average, and
there is no partial credit and no weighting. Thirteen `OK` marks and one `FAIL`
is `V-REPAIR` or `V-FATAL`. Any number of `FLAG` marks is compatible with
`V-PASS` unless a rule 3–5 condition is met.

Precedence, exact and binding:

1. `V-FATAL` — an unrepairable defect moots every downstream question.
2. `V-REPAIR` — any `FAIL` bars every no-`FAIL` verdict below.
3. `V-VALID-ONLY` — no real conclusion, so nothing to be open or partial about.
4. `V-OPEN` — an unsettled load-bearing posit outranks a missing bridge, and one
   proof can carry both.
5. `V-PARTIAL` — the weakest qualification.
6. `V-PASS` — residual, and only residual.

**Verdict inheritance, binding.**

1. Compute the object's own verdict from its fourteen marks by the six rules.
2. Take the worse of that verdict and the worst `audit-verdict` carried by any
   `PR-###` in the object's transitive `depends-on` closure, ordered by the
   precedence list above.
3. The inherited verdict is the **printed** verdict, and the verdict line names
   its source: `V-OPEN, inherited from PR-338`.
4. A `W-DEM` premise citing a record whose verdict is `V-OPEN` or `V-PARTIAL`
   requires one explicit sentence beneath `established`, last in the order §4.5
   fixes, naming that record and its verdict.

Verdicts are computed, not chosen: a `V-PASS` over a printed `FAIL` is an
arithmetic error, rejected by recomputation (§6.9 rule 5).

### 6.6 Rendered form

The audit table is a four-column table:

| Column | Content | Constraint |
|---|---|---|
| Axis | Token plus full axis name | All fourteen rows, §6.2 order, no reordering, no omission |
| Mark | `OK` / `FLAG` / `FAIL` / `N/A` | Never blank; `N/A` only in the two licensed cases |
| Locus | The field or line the mark is about: `p2`, `PF-014.3`, `claim`, `middle`, `not-established` | Mandatory for every `FLAG` and `FAIL`; for `OK` see §6.9 rule 2 |
| Finding | One sentence, ≤ 25 words | Must name an id or token; may not restate the axis question |

Beneath the table and above the verdict line stands the fifth mandatory element
of the rendered form, the four columns being the first four: **Rule inputs**,
always present, exactly four lines, each answered by ids or by the literal word
`none`. These are the data rules 3–5 discriminate on.

1. `import` of `claim`, plus whether any `ONT`/`EXI` `FLAG` leaves a real claim
   standing.
2. Load-bearing premises carrying `warrant: W-POST`, by `pid`, each marked
   "settled by `PF-###`" or "unsettled".
3. Missing named bridges, as `PR-###` stubs.
4. `OB-###` ids with no matching `RP-###`.

Beneath them, one **verdict line**: the verdict token and the achieved rung
(§6.2.1), then the extra fields required for that verdict. Every object of
`kind: DEMONSTRATION` prints an achieved rung whatever its verdict —
`V-OPEN at RG-THAT`, `V-PARTIAL at RG-WHY`, `V-REPAIR at RG-VALID` are all
well-formed lines. Only `SPECIMEN` and `DIALECTICAL` objects, and a `V-FATAL`
where no rung is achieved, print a verdict line with no rung. The verdict line
is never separated from its table by a page or column break.

Placement. The table is the last element of the proof object, printed after
`replies` so that `DIA` and `WAR` rows may cite `OB-###`/`RP-###` ids, on the
same spread as the proof's final layer. For `kind: SPECIMEN` it precedes the
defect discussion and the repaired form, the table *being* the localization. For
an audit set as an exercise, no table is printed with the proof; the completed
table appears in the matching `SO-##.##`. Every `FLAG` and `FAIL` row is paired
with a margin callout on the offending line (§11).

### 6.7 Application protocol

The sweep runs in five gates. Gate order is *run* order; the printed table is
always in axis order, whatever order its cells were filled in.

| Gate | Axes | Why here |
|---|---|---|
| 1 Sense | `SEM`, `FID` | Nothing downstream is well defined until each term has one sense and the symbolization is known to mean what the prose means. |
| 2 Structure | `LOG`, `EXI`, `MOD` | Consequence, import, and modal scope are checkable once senses are fixed, before any premise is evaluated for truth. |
| 3 Support | `WAR`, `PRV`, `FRM` | What each premise rests on, and whether that is a citation, a revelation, or a framework posit. |
| 4 Import and order | `ONT`, `DEP` | Whether a real claim is made, and whether the asserted ordering is the one the deciding tests deliver. |
| 5 Result | `SCO`, `DIA`, `EXP`, `DEM` | What was established, what an opponent must deny, whether the middle grounds — and last the rung, a function of the other thirteen marks (§6.2.1). |

**No early stop.** All five gates are completed after a `FAIL`, because failures
mask each other: an equivocation at `SEM` makes an argument look valid, and only
once the sense is fixed does `LOG` show four terms; an overstrong `claim` stays
invisible at `SCO` while `EXI` still grants the unearned existence claim that
appears to reach it. An audit stopped at the first `FAIL` under-reports and is
rejected in review.

**Provisional repairs.** On a failure the auditor records the mark, writes the
minimal provisional repair as `r1`, `r2`, …, and continues the sweep against the
repaired object; each downstream `Finding` names the repair it presupposes
("under `r1`"). Both the original `FAIL` and the downstream marks stand. With no
provisional repair available at gate 1 or 2, the auditor completes the remaining
gates against the strongest available reading and records in `why-no-repair`
which readings were tried.

### 6.8 Weaning schedule

Stage letters are the curriculum section's, which owns chapter numbering; these
gates attach to stage boundaries, not to chapter numbers.

| Stage | Audit form | Who fills it |
|---|---|---|
| A — proof grammar | **Axis probe**: a 3–5 row table drawn from `SEM`, `LOG`, `EXI`, `MOD`, `SCO`, labelled as a probe, with the axes not printed simply absent. No verdict token: a verdict requires a complete sweep. A reduced object (§4.8) prints its licensed four-row axis probe and no verdict token, in keeping with this row. | Author, fully worked |
| B — meaning and distinction | Axis probe extended with `ONT`, `DEP`, `WAR`, `FRM`. Still no verdict token, and a reduced object (§4.8) prints its licensed four-row probe and no verdict token, as in Stage A. | Author, fully worked |
| C — first metaphysical demonstrations | Full fourteen-row table with verdict line, on every `kind: DEMONSTRATION`. The rubric is printed entire at the opening of Stage C and each `FLAG`/`FAIL` row gets a prose paragraph. | Author, fully worked |
| D — adversarial examples | Full table with the `Finding` column blank for 4–6 rows in at least half the specimens; `SO-##.##` supplies the full table and the verdict computation. | Reader, scaffolded |
| E — larger dependency chains | One anchor demonstration per chapter carries a full worked audit; every other prints marks, rule inputs, and verdict line only, findings withheld to solutions. AUDIT is the default exercise verb. | Reader, mostly unaided |
| F — from first principle to further attributes | Full fourteen-row table with verdict line printed **in the main text** for every `PF-4##` with `kind: DEMONSTRATION`, in axis order, with the Axis, Mark, Locus and rule-input elements complete and the Finding column printed blank; findings are supplied in the matching `SO-##.##`. Marks, loci, verdict, and the verdict's extra fields are authored by `LN-1` and are byte-identical to the ledger record's `audit-axes` and `audit-verdict`; `LN-2` supplies Finding cells only and may not alter a mark, a locus, or a verdict. | Marks: `LN-1`. Findings: reader, unaided |

A Stage F chapter printing a verdict line with no table, or a solution whose
marks differ from the ledger record, is rejected as an intellectual failure.

**Reprint gate.** The rubric — axes, marks, verdict rules, precedence — is
reprinted in full at the opening of Stage C and again at the opening of Stage D,
and **not** reprinted from Stage E onward. From Stage E the only standing copy is
the one-page reference card in the back matter, cross-referenced by id.

### 6.9 Anti-checklist mechanisms

Six mechanisms make a table filled in by pattern, rather than by inspection,
detectable in a submitted draft.

1. **Transplant test.** Paste any `Finding` cell under a different proof's
   audit. If it still reads as true and apposite it is generic and the row is
   rejected: every `Finding` must be falsified by moving it.
2. **Costed `OK`.** At least four `OK` rows per full audit carry an inspection
   note naming a specific id or printed artifact — e.g. "`SEM` `OK`: `TM-007.2`
   selected at `p1`, `p3`, step `.4`" — of which at least two come from {`WAR`,
   `ONT`, `EXP`, `DIA`} and at least one from {`SEM`, `LOG`, `EXI`, `MOD`,
   `FID`}. Regardless of its mark, the `WAR` row of every full audit names each
   premise by `pid` with its warrant token, and the `ONT` row cites by locus the
   printed MD5 rewrite of `claim`. An audit in which every `OK` row is bare, or
   in which every costed row falls in the second set, is rejected.
3. **Discriminating power.** Every `V-PASS` in Stages C–F carries a one-line
   audit of a near-neighbour variant — one premise weakened, one modality
   strengthened, one quantifier moved — naming the axis the variant fails. A
   rubric that cannot fail the near neighbour has not been applied.
4. **Banned strings.** These may not appear in a `Finding` cell: "no issues",
   "looks fine", "satisfied", "as required", "the argument is rigorous", "OK as
   written", "nothing to note". A reviewer greps.
5. **Recomputation.** The reviewer re-runs the six verdict rules against the
   printed marks *and the printed rule inputs*. A verdict inconsistent with
   either is a draft rejection, not an editorial note; so is a rule-input line
   contradicted by the object's `premises`, `objections`, or `not-established`
   fields.
6. **Locus coverage.** Every `FLAG` and `FAIL` row names a locus and has a paired
   margin callout on that line. A `FAIL` with locus "the argument" or with no
   callout is rejected.

A chapter draft with three or more full audits carrying no `FLAG` and no `FAIL`
anywhere is returned to the author: either the specimens are too easy for the
stage, or the rubric was filled in rather than run.


## 7. Error Taxonomy for Metaphysical Demonstrations

### 7.1 What the taxonomy is, and what may never enter it

An `ER-###` record names a **diagnosis**, never a verdict. Verdicts are computed
by §6.3 from axis marks; an `ER-###` id is the required content of the `errors`
field of a `V-REPAIR` or `V-FATAL` audit, and is inadmissible anywhere else as a
substitute for that computation. A chapter that writes "this commits ER-303" and
stops has not audited anything.

Three closure rules bind every later author.

1. **Single-axis rule.** Every `ER-###` record names exactly one §6.2
   axis. Families group errors by phenomenon, not by axis; several families
   therefore contain classes whose home axis lies outside the family's usual
   range, and the record's `axis` field, not the family, decides which row of the
   audit table fires.
2. **No prose errors.** An auditor who finds a defect with no class MUST mint a
   new `ER-###` in the owning family's band, with the complete §7.3 block, before
   reporting it. Reporting an unclassed defect in running prose is itself a
   defect.
3. **Negative closure (§2.5).** No `ER-###` may be minted, and no existing
   class may be stretched, to cover: unpersuasiveness, inelegance, length, the
   absence of symbolization, the absence of opponent assent, contestedness of a
   premise as such, the presence of an unanswered objection, or the absence of an
   endorsement by a canonical author. Any proposed class whose detector reduces to
   one of these is rejected at review.

### 7.2 Families, bands, and the `ER-###` record

The spine's identifier prefixes are closed, so families cannot take prefixes of
their own. **Decision:** a family is a reserved hundred-band inside `ER-###`, and
carries a vocabulary token of the form `EF-XXX` (not an identifier: it does not
match `^[A-Z]{2}-[0-9]`). Bands are never reallocated; a retired class leaves a
hole.

| Family token | Band | Family | Home axes | Characteristic failure |
|---|---|---|---|---|
| `EF-SEM` | `ER-1##` | semantic and terminological | `SEM`, `WAR`, `FID` | the words do not hold still |
| `EF-LOG` | `ER-2##` | formal | `LOG`, `EXI` | the step is not licensed |
| `EF-MOD` | `ER-3##` | modal | `MOD` | the strength is not earned |
| `EF-ONT` | `ER-4##` | ontological | `ONT` | a concept is doing an entity's work |
| `EF-EXP` | `ER-5##` | explanatory and dependence | `EXP`, `DEP` | the order of dependence is wrong or unshown |
| `EF-SCO` | `ER-6##` | scope and strength | `SCO`, `DEM` | more is claimed than reached |
| `EF-DIA` | `ER-7##` | dialectical and provenance | `DIA`, `WAR`, `FRM`, `PRV` | the burden is misplaced or the warrant is borrowed |

Record fields, all mandatory: `id` · `name` (≤ 5 words, unique) · `family` ·
`axis` (exactly one §6.2 token) · `class-status` (§7.8) · `detector` (one
sentence, mechanical) · `specimen` · `locus` · `licenses` · `repair` ·
`survives` · `default-verdict` · `positions` (required iff `class-status` is
`CONTESTED` or `HYBRID`).

### 7.3 The mandatory five-part block

Every first presentation of a class, in a chapter or in the class register,
prints these five parts in this order, under these headings, with nothing
interposed. A block missing any part is rejected; a block reordering them is
rejected.

**1. Specimen.** A defective proof object with `kind: SPECIMEN`, numbered and
suffixed as §7.4 fixes, printed in at least `L2-NUM`. For a class whose
`class-status` is `CONTESTED` (§7.8), the part-1 object is instead
`kind: DIALECTICAL`, carries the class's axis at `FLAG` rather than `FAIL`, and
takes neither the `/S` suffix nor the `Defective` marker: a contested move is
not a defect, and §4.2.1 requires every `SPECIMEN` to carry at least one `FAIL`.

*Plausibility is enforced, not exhorted.* A specimen MUST satisfy all of:

- (a) **Invisible in prose.** For every class outside `EF-LOG`, the defect MUST
  NOT be detectable from `L1-PROSE` alone; locating it must require consulting
  `lexicon`, `modality`, `modal-scope`, `commitments`, a `PRI-*` token, a warrant
  token, or `established`. *Reviewer test:* hand a competent reader only the
  prose; if that reader names the defect, the specimen is replaced.
- (b) **Otherwise clean.** Every axis other than the class's own axis is `OK` or
  carries a stated `FLAG`; in particular `LOG` is `OK` for every specimen outside
  `EF-LOG`. A specimen that fails three axes teaches nothing about any of them.
- (c) **Warranted premises.** Every premise carries a §2.1.2 token other than
  `W-AUTH` and `W-REV`, except in `ER-702` and `ER-703`, whose subject matter is
  those tokens.
- (d) **Minimum structure.** At least three numbered lines, so that the defect
  has a location that is not the whole argument.
- (e) **No caricature.** If the specimen is attributed to a named position, it
  MUST be at least as strong as that position's own best statement, cited in
  `scholion`; otherwise it is attributed to no one. A specimen that violates this
  makes the book itself an instance of `ER-705`.

Preferred sourcing, in order: a faithful compression of an argument actually
advanced in the literature (cited in `scholion`, never in a warrant slot); a
near-neighbour of a demonstration the book has already validated, altered at one
token; a construction of the author's own.

**2. Locus.** Exact localization, printed as an ordered triple

> `⟨proof-object field · identifier or line · offending token⟩`

for example `⟨premises.p1 · PF-951/S.p1 · PRI-TMP where PRI-CAU is required⟩`. The
first offending line MUST be named even when the defect propagates. The phrases
"somewhere in the argument", "the argument as a whole", and "the general
approach" are forbidden. The single exception: `ER-307`, `ER-506`, and `ER-701`
are properties of a graph, and their locus is the cycle itself, printed as an
ordered list of ids with the edge that closes it named last.

**3. Licenses.** What false thing the argument would license if the defect stood.
This part MUST be a sentence the author is prepared to reject, exhibited by one
of two devices, and by no third:

- the **parallel-form device**: a second specimen of identical structure whose
  conclusion is plainly false, showing the pattern proves too much; or
- the **contradiction device**: a derivation from the offending line to a claim
  that contradicts a cited `PR-###` already established in the book.

Writing that the argument is "unwarranted", "hasty", or "not fully established"
does not discharge this part. The test is: could a reader who accepted the defect
now derive something the book denies, and is that thing printed?

**4. Repair.** Either a minimal repair or the token `NO-REPAIR`. Repair kinds are
a closed list; a repair names exactly one, or names two and explains why one does
not suffice:

`FIX-QUALIFY` (add a time, respect, or `QUA-SEC` index) · `FIX-SPLIT-SENSE`
(mint a further `TM-###.n` and re-run MD2) · `FIX-BRIDGE` (cite or prove a
`BR-###` or interposed `PR-###`) · `FIX-PROMOTE` (move content out of a `DF-###`
into a `PR-###` carrying its own warrant) · `FIX-WEAKEN` (lower `modality`,
`modal-scope`, `import`, or `rung`) · `FIX-RESTRICT` (narrow `subject` or
`domain`) · `FIX-REROUTE` (replace `middle` and redo `steps`) · `FIX-DISCHARGE`
(discharge a `W-HYP`) · `FIX-DECLARE` (add the missing `commitments`,
`framework`, or `denial-set` entry).

*Minimality is checkable:* delete any component of the proposed repair and the
same axis returns to `FAIL`. A repair that also repairs a second axis is not
minimal and MUST be split.

`NO-REPAIR` MUST state which of exactly two grounds applies, in the words of
§6.3 rule 1: the only available repair assumes `claim`, or every available repair
leaves `survives: NONE`. "No repair is obvious" is not a ground. A third ground
is available only to a class whose `class-status` is `CONTESTED`: the move is
contested rather than defective and there is nothing to repair (§7.8 (1)).

**5. Survives.** One sentence in the indicative, at the repaired argument's
actual strength, carrying its `modality`, `modal-scope`, and `import` tokens,
followed by the entries added to `not-established`. The mandated pattern:

> **What now stands:** ⟨sentence + tokens⟩. **What does not stand:** ⟨the
> original `claim`, quoted, and any nearby claim the reader would otherwise
> assume was carried along⟩.

The survivor is printed even when it is trivial, conceptual, or `NONE`; a repair
section that ends without this pair is itself a defect. When the survivor is
weaker than the original — the usual case — the book says so in that sentence and
does not soften it in surrounding prose.

The block closes with a two-line audit stub: the firing axis with its mark, and
the §6.3 verdict, both computed by the rubric rather than asserted.

### 7.4 Marking incorrect examples

Two mechanisms, both mandatory, because either alone fails under excerpting.

**Mechanism 1 — the specimen suffix (identifier-level).** *Decision:* no band is
reserved for specimens. Every `kind: SPECIMEN` proof object takes its number from
its own stage band, under the curriculum section's allocation, and carries the
mandatory suffix `/S` — `PF-214/S`. The suffix is part of the identifier, not a
printing convention: it is reproduced wherever the id is printed or cited, in the
environment header, the running head, the index, an exercise stem, a solution, a
margin callout, a dependency diagram, and every cross-reference, and it precedes
any line selector (`PF-214/S.p2`, `PF-214/S.3`). The id is therefore
self-marking: an occurrence of `/S` in any excerpt is on its face a reference to
a defective argument. Any citation of a `/S` id in a `warrant`, `depends-on`,
`established-by`, or `source` field is `PRV` = `FAIL` and a hard build error. A
repaired specimen never keeps its number: it is re-entered as a fresh unsuffixed
`PF-###` in the ordinary allocation, and only that record may be cited as
establishing anything.

**Mechanism 2 — the `Specimen` environment (typographic).** Named here as the
required environment; its LaTeX realization belongs to the production section,
subject to these requirements:

1. The environment's opening line carries, before any content, the word
   **Defective** followed by the id and the `ER-###` classes it instantiates.
2. A full-height rule runs the outer edge of the block, continuing across page
   breaks.
3. Every numbered line inside the environment is prefixed with a repeated
   marker glyph, so that a single quoted line still carries the mark.
4. Any page containing specimen material carries a running head naming it.
5. No meaning is carried by color alone; the block MUST read as defective in
   grayscale and in plain-text extraction of the PDF.
6. Specimen content never enters the ledger as a `PR-###`, never appears in the
   index of propositions, and is excluded from any "summary of results" apparatus.
7. The offending line carries a margin callout from §11 — the family's callout
   token per §7.9; where §7.9 gives a family two tokens the author takes the one
   §11.3 admits for this object, and where §11.3 forbids `WHY` (any object at
   `rung: RG-THAT`) the token is `USES` — naming the `ER-###` id. *Decision (flagged):* naming an
   identifier in a callout is an id reference, permitted like `OBJ`'s and
   `USES`'s, and is not the "citation" that §11 forbids.

The `9##` band is reserved to this specification's exemplar appendix and
allocates no book id of any class.

### 7.5 The classes

`class-status` values are defined in §7.8. `axis` is the single §6.2 axis whose
row the class causes to fire.

#### `EF-SEM` — semantic and terminological (`ER-1##`)

| Id | Name | Axis | Status | Detector |
|---|---|---|---|---|
| `ER-101` | Equivocation | `SEM` | `FLAW` | one `TM-###` bears two sense selectors across lines with no `PRD-ANA` declaration; the MD2 substitution test breaks a step under either uniform reading |
| `ER-102` | Sense drift | `SEM` | `FLAW` | the selector is declared at first use and silently widened later; the sense at the last use entails more than the sense at the first |
| `ER-103` | Analogy flattened | `SEM` | `FLAW` | a term satisfying the `PRD-ANA` test is used with one account across both analogates, or rendered as a single predicate letter with no `RISK` callout and no `not-established` entry |
| `ER-104` | Ratio switched | `SEM` | `HYBRID` | the ratio stated for analogates ⟨a,b⟩ licenses a step taken over ⟨b,c⟩, for which no ratio is stated |
| `ER-105` | Suppressed relativization | `SEM` | `FLAW` | a `QUA-SEC` premise is consumed as `QUA-SIMP`, or a predicate the argument needs held fixed carries no time, respect, or aspect index |
| `ER-106` | Premise concealed in a definition | `WAR` | `FLAW` | `LC-08`: the `DF-###` asserts content not derivable from its `TM-###.n` sense plus prior ids, and deleting that clause breaks a step |
| `ER-107` | Fidelity drift | `FID` | `FLAW` | back-translating `L3-SKEL` into prose yields a claim the author would not assert, or the `fidelity` sentence is absent or false |

#### `EF-LOG` — formal (`ER-2##`)

| Id | Name | Axis | Status | Detector |
|---|---|---|---|---|
| `ER-201` | Affirming the consequent | `LOG` | `FLAW` | a step from `A → B, B` to `A`, or from `A → B, ¬A` to `¬B`; the named rule does not license it in the declared `logic` |
| `ER-202` | Illicit quantifier shift | `LOG` | `FLAW` | `∀x∃y Rxy` consumed as `∃y∀x Rxy`, or a constant introduced by existential instantiation reused outside its scope |
| `ER-203` | Composition | `LOG` | `FLAW` | a predicate proved of each part or member is asserted of the whole or the collection with no distributive-to-collective lemma cited (`BR-007`) |
| `ER-204` | Division | `LOG` | `FLAW` | the mirror: a predicate of the whole or collection asserted of a part or member with no lemma |
| `ER-205` | Existential-import error | `EXI` | `FLAW` | MD3: `∀x(Fx → Gx)` is made to yield `∃x Gx`, or a definite description is written before its uniqueness lemma is proved and cited |
| `ER-206` | Undischarged hypothesis | `LOG` | `FLAW` | a `W-HYP` premise lies in the dependency set of `established` with no discharge line in `steps` |
| `ER-207` | Unlicensed step | `LOG` | `FLAW` | residual class: a `steps` line names no rule, or names a rule absent from the declared calculus |

#### `EF-MOD` — modal (`ER-3##`)

| Id | Name | Axis | Status | Detector |
|---|---|---|---|---|
| `ER-301` | Modal strengthening | `MOD` | `FLAW` | MD6: `claim` carries a necessity kind or modal scope stronger than the weakest among the load-bearing premises, the §10.3 order fixing rank, with no cited `BR-###` whose antecedent is discharged inside the object |
| `ER-302` | Composite/divided conflation | `MOD` | `FLAW` | an `SCP-CMP` premise is consumed as `SCP-DIV` or conversely; or an `L3-SKEL` modal line prints no scope token |
| `ER-303` | Conceptual necessity read as real | `MOD` | `FLAW` | the record says `NEC-MET` but the `NEC-CON` test succeeds earlier in the binding test order, and the MD5 paraphrase survives |
| `ER-304` | Regularity promoted | `MOD` | `HYBRID` | a `NEC-NOM` premise warranted `W-IND` or `W-EMP` yields a `NEC-MET` conclusion with no `BR-002` |
| `ER-305` | Conceivability taken for possibility | `MOD` | `HYBRID` | `POS-MET` asserted on a conceivability report with no `BR-001`; the possibility is not exhibited, only not yet refuted |
| `ER-306` | Epistemic modality read as alethic | `MOD` | `FLAW` | replace "must"/"cannot be otherwise"/"may for all we know" with "the evidence settles that"; if the step still runs, the recorded `NEC-*`/`POS-*` token is wrong |
| `ER-307` | Modal collapse | `MOD` | `CONTESTED` | the premises jointly entail `NEC-MET` for a proposition the same object records `CONT`; locus is the entailment chain |
| `ER-308` | Hypothetical necessity absolutized | `MOD` | `FLAW` | a `NEC-HYP` operator is detached from an antecedent that is itself `CONT` |

#### `EF-ONT` — ontological (`ER-4##`)

| Id | Name | Axis | Status | Detector |
|---|---|---|---|---|
| `ER-401` | Conceptual result paraded as real | `ONT` | `FLAW` | `import: REAL` although the MD5 paraphrase is supported by the same premises with the same force |
| `ER-402` | Distinction of reason reified | `ONT` | `HYBRID` | `DK-REAL` asserted with neither separability nor a divergent entailment exhibited, the §3.9 test order having been skipped |
| `ER-403` | Real distinction collapsed | `ONT` | `HYBRID` | `DK-NOM` asserted although a divergent entailment is available and unaddressed |
| `ER-404` | Definitional priority read as ontological | `ONT` | `FLAW` | `PRI-DEF` is what the text establishes; `PRI-ONT` or `PRI-GND` is what a later step consumes; no `BR-###` |
| `ER-405` | Silent commitment | `ONT` | `FLAW` | a quantifier ranges over, or a constant names, a kind absent from `commitments`, or present with no licensing id or `DK-*` tag |

#### `EF-EXP` — explanatory and dependence (`ER-5##`)

| Id | Name | Axis | Status | Detector |
|---|---|---|---|---|
| `ER-501` | Temporal priority read as causal or ontological | `DEP` | `FLAW` | `PRI-TMP` is what the premise supports; `PRI-CAU`, `PRI-ONT`, or `PRI-GND` is what the step consumes; no `BR-###` |
| `ER-502` | Causal priority made chronological | `DEP` | `HYBRID` | `PRI-CAU` is asserted to require temporal precedence, excluding simultaneous causation without argument (`BR-006` uncited) |
| `ER-503` | Series equivocation | `DEP` | `HYBRID` | an argument turns on the impossibility of regress but declares neither `SER-ACC` nor `SER-ESS`, or declares one and applies the other's test; the concurrency test is not run |
| `ER-504` | Sign taken for ground | `EXP` | `FLAW` | `rung: RG-WHY` or `PRI-GND` asserted although the MD11b reversal reads equally well in both directions, or no stripped variant is exhibited |
| `ER-505` | Illicit totalization | `EXP` | `CONTESTED` | an explanandum is predicated of the sum or series as a subject distinct from its members, with no lemma constituting the totality a subject |
| `ER-506` | Circular explanatory dependence | `DEP` | `HYBRID` | `LC-02`: a cycle in `depends-on` plus warrant edges; locus is the cycle |
| `ER-507` | Regress fatigue | `EXP` | `HYBRID` | a terminus is inferred from a regress being non-traversable, unsatisfying, or infinite, with no `SER-ESS` premise and no concurrency test |
| `ER-508` | Missing bridge lemma | `DEP` | `FLAW` | a step consumes a proposition present neither in `premises` nor in `depends-on`; if the gap is modal or a `PRI-*` swap, the class is `ER-301`, `ER-304`, or `ER-501`, not this one |
| `ER-509` | Order of knowing read as order of being | `DEP` | `FLAW` | `PRI-EPI` is established and `PRI-ONT` or `PRI-GND` consumed; §3.9 makes `PRI-EPI` evidence for no other priority |
| `ER-510` | Simultaneity taken to exclude dependence | `DEP` | `FLAW` | contemporaneity or `SIM-NAT` is used to deny `PRI-CAU` or `PRI-GND` between the simultaneous items |
| `ER-511` | Vacuous middle | `EXP` | `FLAW` | `middle` is definitionally equivalent to `attribute`; deleting the middle leaves the step valid and the explanation unchanged |

#### `EF-SCO` — scope and strength (`ER-6##`)

| Id | Name | Axis | Status | Detector |
|---|---|---|---|---|
| `ER-601` | Overstrong conclusion | `SCO` | `FLAW` | `claim` exceeds `established` in modality, modal scope, or subject |
| `ER-602` | Subject creep | `SCO` | `FLAW` | the attribute is proved of a subject wider or narrower than `subject` names; per se commensuration fails |
| `ER-603` | Rung inflation | `DEM` | `FLAW` | achieved rung below claimed rung, or `rung` unstated and explanatory language used |
| `ER-604` | Nominal identification | `SCO` | `FLAW` | a proper name or theological title is attached to a demonstrated subject with no bridge proposition and no dependency edge; house rule 6 |
| `ER-605` | Suppressed `not-established` | `SCO` | `FLAW` | `not-established` is empty, `NONE`, or lists only claims no reader would have attributed to the argument |

#### `EF-DIA` — dialectical and provenance (`ER-7##`)

| Id | Name | Axis | Status | Detector |
|---|---|---|---|---|
| `ER-701` | Petitio principii | `WAR` | `FLAW` | MD7: a premise's warrant chain reaches `claim`, or an id whose record lists `claim` in `depends-on`; locus is the chain. Entailment of a premise by the conclusion is not this defect; only warrant-dependence is |
| `ER-702` | Authority in the warrant slot | `PRV` | `FLAW` | `LC-09`: `W-AUTH` on a premise in any proof object — §4.2.1 (b) scopes the prohibition to every `kind`, the single exception being a `SPECIMEN` whose declared target class is `ER-702` or `ER-703` — or a citation standing where a warrant token belongs; house rule 3 |
| `ER-703` | Revealed premise naturalized | `PRV` | `FLAW` | `LC-09`: a `W-REV` premise in an object labelled a metaphysical demonstration at any rung; house rule 4 |
| `ER-704` | Framework posit unmarked | `FRM` | `FLAW` | a `W-POST` premise printed under `framework: NEUTRAL`, or the text does not say whether the result holds inside the framework or establishes part of it |
| `ER-705` | Straw opponent | `DIA` | `FLAW` | MD9: the reason attributed to a named position is weaker than that position's own best published statement; house rule 7 |
| `ER-706` | Denial-set defect | `DIA` | `FLAW` | `denial-set` empty, non-minimal, or containing a member whose removal breaks no step, or containing a member no standing position actually holds |
| `ER-707` | Plausibility taken for warrant | `WAR` | `FLAW` | a `W-SELF` premise whose printed analysis appeals to obviousness, wide acceptance, long tradition, or inability to imagine otherwise, rather than to the analysis of its terms |
| `ER-708` | Claim revised under objection | `DIA` | `FLAW` | `claim` differs between its statement and the `RP-###` that defends it, with no new `PF-###` and no `superseded-by` |

### 7.6 Two worked blocks

`PF-951/S` and `PF-952/S` are specification-local illustrations, distinct from
the exemplars of the appendix; neither is a book id, and no chapter may cite
either. Later authors match this level of specificity or the block is rejected.

#### `ER-501`, temporal priority read as causal or ontological

**1. Specimen** — `PF-951/S`, `kind: SPECIMEN`, `logic`: FOL with identity.
`claim`: "The universe's existing at the first moment of time has no cause."
p1 Every cause is prior to its effect. `[W-SELF, PRI-TMP, NEC-MET, SCP-CMP]`
p2 Nothing is temporally prior to the first moment of time.
`[W-DEM, PR-TBD-first-moment-unpreceded]`
p3 The universe exists at the first moment of time. `[W-EMP]`
`steps`: 1 from p1, p3 (universal instantiation); 2 from 1, p2 (modus tollens).
`LOG` is `OK`; the prose is unremarkable.

**2. Locus** — `⟨premises.p1 · PF-951/S.p1 · PRI-TMP asserted where PRI-CAU is
what the argument consumes at PF-951/S.2⟩`. The warrant `W-SELF` is defensible
for the `PRI-CAU` reading and indefensible for the `PRI-TMP` reading; the premise
is stated so that the two are not distinguished.

**3. Licenses** — parallel-form device: from the same premise, "a hand resting in
sand is not causing the depression, since hand and depression are simultaneous"
follows by identical steps. The book denies that conclusion at
`PR-TBD-simultaneous-causation-possible`, so the pattern proves too much.

**4. Repair** — `FIX-BRIDGE` with `FIX-QUALIFY`. Replace p1 with "Every cause is
causally prior (`PRI-CAU`) to its effect", warrant `W-SELF`, and cite `BR-006`,
which denies the entailment `PRI-CAU → PRI-TMP`. Minimality: dropping `BR-006`
returns `DEP` to `FAIL`, since p2 is then irrelevant to the step.

**5. Survives** — **What now stands:** nothing temporally prior to the first
moment causes the universe to exist at that moment (`ACT`, `SCP-DIV`, `import:
REAL`). **What does not stand:** "the universe's existing at the first moment has
no cause"; and nothing here bears on whether a simultaneous or non-temporal cause
sustains it, which enters `not-established`.

*Audit stub:* `DEP` = `FAIL`; verdict `V-REPAIR`, `errors: [ER-501]`.

#### `ER-106`, premise concealed in a definition

**1. Specimen** — `PF-952/S`, `kind: SPECIMEN`. `lexicon` declares
`DF-TBD-contingent-being`: "A *contingent being* is a being whose existence is
explained by something other than itself." p1 Every contingent being's existence
is explained by another `[W-DEF]`. p2 Some being is contingent `[W-EMP]`.
`claim`: "Some being's
existence is explained by another." Every step is licensed; every premise carries
a warrant; the definition reads like standard vocabulary.

**2. Locus** — `⟨lexicon · DF-TBD-contingent-being · the clause "whose existence
is explained by something other than itself"⟩`, consumed at `PF-952/S.p1`.
`LC-08` fires: the
`TM-TBD-contingent.1` sense of *contingent* is "exists and possibly does not"
(`POS-MET`); explicability is not derivable from that sense plus prior ids.

**3. Licenses** — contradiction device: with `DF-TBD-contingent-being` in force,
the thesis that some existing thing is a brute fact is refuted by lexicon alone,
contradicting the book's record of that thesis as a standing position under
`PR-TBD-brute-fact`. A substantive principle of sufficient reason would be
established by stipulation.

**4. Repair** — `FIX-PROMOTE`. Restore `DF-TBD-contingent-being` to the
`TM-TBD-contingent.1` sense. Mint `PR-TBD-contingents-explained`, "Every being
that exists and possibly does not has its existence explained by another",
`warrant: W-POST`, `framework: AT`, `contested: true`,
entered in `denial-set`. Minimality: leaving the clause in the definition and
merely adding a footnote returns `WAR` to `FAIL`, since `W-DEF` still stands on a
non-definitional claim.

**5. Survives** — **What now stands:** every being that exists and possibly does
not is contingent (`NEC-CON`, `SCP-CMP`, `import: CONCEPTUAL`); and,
conditionally on `PR-TBD-contingents-explained`, the original claim. **What does
not stand:** "some being's existence is explained by another" as an
unconditional result of natural reason; it now depends on a declared framework
posit.

*Audit stub:* `WAR` = `FAIL`; verdict `V-REPAIR`, `errors: [ER-106]`. After
repair the object's verdict is `V-OPEN`, not `V-PASS`, because
`PR-TBD-contingents-explained` is load-bearing and the book does not settle it.

Placeholders in draft blocks take the `<PREFIX>-TBD-<slug>` form fixed by §10.1 (3) and
never a digit-bearing improvisation; `LC-16` rejects any that survive into a
reviewed draft.

### 7.7 Bridges invoked by repairs

Repairs above cite `BR-###` rules. This section allocates the seven the taxonomy
requires; the modality section may add, but may not renumber. Each carries its own
warrant token and is audited like any premise.

| Id | Licenses | Warrant | Condition |
|---|---|---|---|
| `BR-001` | `POS-CON` → `POS-MET` | `W-POST` | modal-rationalist bridge; contested, must be marked |
| `BR-002` | `NEC-NOM` → `NEC-MET` | `W-POST` | via a stated essentialist account of the kind in question |
| `BR-003` | `NEC-CON` → `NEC-MET` | `W-DEM` | requires a cited nonemptiness `PR-###` supplying real instantiation |
| `BR-004` | `SCP-CMP` → `SCP-DIV` | `W-DEM` | licensed only when the antecedent carries necessity of the same kind |
| `BR-005` | `PRI-ONT` → `PRI-GND` | `W-POST` | requires an exhibited asymmetry witness; §3.9 denies the entailment |
| `BR-006` | blocks `PRI-CAU` → `PRI-TMP` | `W-SELF` | admits simultaneous causation |
| `BR-007` | distributive → collective predication | `W-DEM` | requires a lemma proving the predicate collective for the specified collection |

### 7.8 Error versus disagreement

Labelling an opponent fallacious instead of answering him is the characteristic
vice of this genre, and the taxonomy is the instrument most likely to produce it.
Every class therefore carries one `class-status`:

- **`FLAW`** — a mistake by the argument's own declared standards. Any competent
  party, including a rival, concedes it once the locus is shown, because the
  defect is a mismatch between what the record declares and what the steps
  consume. May be called a fallacy or an error in prose.
- **`CONTESTED`** — a move that a named standing position accepts and another
  rejects, where the disagreement is about a premise, not an inference. May
  **never** be called a fallacy, an error, a confusion, or a mistake. The book's
  own rejection of it is an argument the book must make, at length, elsewhere.
- **`HYBRID`** — the move is a `FLAW` when made without applying the deciding
  test the spine supplies, and `CONTESTED` once the test has been applied and the
  verdict of the test is what the parties dispute. Every `HYBRID` block MUST
  print both halves and say which is at issue in the specimen.

Binding consequences.

1. **Mark routing.** A `FLAW` produces axis `FAIL`. A `CONTESTED` move produces
   axis `FLAG`, with the required margin callout, and routes to verdict `V-OPEN`
   under §6.3 rule 4 — never to `V-REPAIR`, since there is nothing to repair. A
   `CONTESTED` move produces `FAIL` in exactly one circumstance: the proof
   object's own declared `framework` rejects it, which is internal inconsistency.
2. **`positions` is mandatory** for `CONTESTED` and `HYBRID`. It names at least
   one standing position that accepts the move and one that rejects it, each with
   that position's own strongest reason. A `positions` field that gives the
   opposed side a reason weaker than its literature gives makes the book an
   instance of `ER-705`, and the reviewer marks `DIA` = `FAIL` on the chapter.
3. **The word "fallacy"** is reserved to `FLAW` classes. Its appearance beside a
   `CONTESTED` or `HYBRID` id is a copy-editing defect with an audit consequence.
4. **Axis binarity.** A class whose `axis` is `LOG`, `DEM`, or `PRV` MUST take
   `class-status: FLAW`. Those three axes are binary under §6.2 — a step is
   licensed by the declared calculus or it is not, the achieved rung reaches the
   claimed rung or it does not, a warrant slot holds a warrant token or a
   citation — and no standing position disputes the reading rather than a
   premise. A `CONTESTED` or `HYBRID` proposal on one of them is misfiled: the
   disagreement belongs to the axis its disputed premise loads.
5. **Reviewer test.** Take any `CONTESTED` class and ask whether a competent
   holder of the rival position, reading the block, would say "that is not what I
   claim" or "that is what I claim, and here is why". Only the second is
   acceptable. If the first, the block is rewritten.

`CONTESTED` at present: `ER-307`, `ER-505`. `HYBRID`: `ER-104`, `ER-304`,
`ER-305`, `ER-402`, `ER-403`, `ER-502`, `ER-503`, `ER-506`, `ER-507`. All others
are `FLAW`.

### 7.9 Cross-reference discipline

**Family to detection.** Each family is detected by the rubric rows below; a
chapter claiming a defect of a family whose rows are all `OK` has misclassified
it, and the mismatch is itself reviewable.

| Family | Detected by axes | Margin callout on the offending line | Ledger checks | Typical verdict |
|---|---|---|---|---|
| `EF-SEM` | `SEM`, `FID`, `WAR` | `DEF`, `RISK` | `LC-08`, `LC-11` | `V-REPAIR` |
| `EF-LOG` | `LOG`, `EXI` | `INF`, `IMPORT` | — | `V-REPAIR`, `V-FATAL` |
| `EF-MOD` | `MOD` | `MODAL` | `LC-05` | `V-REPAIR` |
| `EF-ONT` | `ONT` | `IMPORT`, `DIST` | — | `V-VALID-ONLY`, `V-REPAIR` |
| `EF-EXP` | `EXP`, `DEP` | `WHY`, `USES` | `LC-02`, `LC-10` | `V-PARTIAL`, `V-REPAIR` |
| `EF-SCO` | `SCO`, `DEM` | `SCOPE` | `LC-05` | `V-REPAIR` |
| `EF-DIA` | `DIA`, `WAR`, `FRM`, `PRV` | `OBJ`, `RISK` | `LC-06`, `LC-09` | `V-OPEN`, `V-FATAL` |

**Citation rules.**

1. Every `FAIL` or `FLAG` in a printed audit table names at least one `ER-###`
   in the verdict's `errors` field. A `FAIL` with no class is inadmissible: it
   means either the class is missing from the taxonomy, in which case mint it, or
   the mark is wrong.
2. Every `ER-###` names exactly one axis; conversely, every axis has at least one
   class. The mapping above is total on both sides, and a reviewer checks it.
3. Exercises cite the `/S` specimen id and the axis token they exercise;
   diagnosis exercises MUST NOT cite the `ER-###` in the prompt, since that gives
   the answer. The `SO-##.##` solution cites the `ER-###`, the locus triple, the
   repair kind, and the surviving conclusion — the last three parts of §7.3 in
   full, not a gesture at them.
4. A class may be cited in prose only where the five-part block, or a
   cross-reference to it, is on the same page or the facing page.
5. Where two classes both fire, the block names both, and states which is prior:
   the class whose repair, applied alone, removes the other.


## 8. Curriculum and Table of Contents (Part 1: Stages A-C)

### 8.1 Progression principle

The book installs, in order: (i) the apparatus, (ii) competence at *auditing*
an argument the reader already knows how to grade, (iii) competence at
*constructing* one under the canonical schema, and only then (iv) the
metaphysical vocabulary. Stage A runs on material where the reader's
independent verdict is already secure — arithmetic, elementary number theory,
propositional and first-order logic — so that a disagreement between reader
and audit table diagnoses the reader's grip on the apparatus, not a
philosophical disagreement.

**Rule 8.1.1 (binding).** No proof object in Chapters 1–17 may carry a `claim`
whose `subject` or `attribute` is God, a first cause, a necessary being, a
pure act, an unmoved mover, or any divine attribute; no `PF-###` in these
chapters, including a `kind: SPECIMEN`, may be drawn from a natural-theology
argument. *Detector:* grep the Stage A–C source for those terms outside a
`scholion`.

**Rule 8.1.2.** A reader who meets the apparatus first inside a famous proof
for God learns five specific wrong habits that later stages cannot dislodge:

1. **Motivated auditing.** The reader arrives with a verdict, so axis marks
   become post-hoc justifications of a prior commitment in either direction, and
   `DIA` degenerates into apologetics or debunking.
2. **Framework blindness.** *Act*, *potency*, *essence*, and *per se* order
   arrive pre-loaded inside the argument, so `framework: AT` premises read as
   `NEUTRAL` machinery. Stage B blocks this by giving each term its own warrant
   token before any argument consumes it.
3. **Verdict inflation.** With stakes high, `V-VALID-ONLY` and `V-OPEN` feel
   like verdicts against the reader, and the reader reaches for `V-PASS`. Stage
   A therefore produces flawless derivations terminating at `RG-VALID`, so
   `V-VALID-ONLY` is first met where nobody has a stake.
4. **Chain collapse.** "The proof of God" is met as one object, and the habit of
   demanding a separate `PF-###` with an explicit `depends-on` edge per bridge
   is never acquired (house rule 6).
5. **Objection as attack.** An objection is read as aimed at the conclusion
   rather than as the denial of a specific `pid` in `denial-set`, so the reader
   cannot construct one.

### 8.2 Identifier ranges owned by Stages A-C

Every band is **closed at its stated ceiling**, and no stage may allocate above
its ceiling under any circumstance. Stages A–C own 001–199 in every class; every
id from 200 upward belongs to the Stage D–F bands; 500–899 is the coordinator
reserve; 900–999 is the specification appendix reserve. A stage that exhausts a
band stops and files an amendment (§1.5(3)) requesting an allocation from the
coordinator reserve; it never takes the next number.

| Class | Stage A | Stage B | Stage C | Ceiling (closed) |
|---|---|---|---|---|
| `TM-###` | 001–029 | 030–079 | 080–119 | `TM-119` |
| `DF-###` | 001–019 | 020–059 | 060–089 | `DF-089` |
| `DS-###` | 001–009 | 010–039 | 040–059 | `DS-059` |
| `PR-###` | 001–029 | 030–079 | 080–139 | `PR-139` |
| `PF-###` | 001–059 | 060–119 | 120–199 | `PF-199` |
| `OB-###` / `RP-###` | 001–019 | 020–059 | 060–119 | `OB-119` |

Stage D–F floors are fixed at 200 in every class, and the unallocated ranges
below 200 (`TM-120`–`TM-199`, `DF-090`–`DF-199`, and their analogues) are Stage
A–C headroom released only by amendment. Chapter 17 fills `PF-199` and `OB-119`
exactly, so its allocation is frozen at those ceilings and cannot absorb an
overflow from any earlier chapter.

Bridges are not allocated by the curriculum. Every `BR-###` is owned, numbered,
and defined by the error-taxonomy section's bridge table (§7.7). A chapter
installs a bridge by citing its existing id; a chapter needing a bridge that
table does not carry files an amendment against it and, until granted, takes the
stub-plus-`V-PARTIAL` route (§6.3, rule 5). No chapter mints a `BR-###`.

`EX-##.##` and `SO-##.##` are chapter-keyed and collide only if chapter
numbers do. Within a stage, ids are allocated in order of introduction, and a
stage may close leaving gaps; gaps are never backfilled by a later stage.

A chapter may name a token before the chapter that installs it only in a line of
the form "deferred to Chapter *n*", and may never require its application before
then.

**Error-class citation.** This section allocates no `ER-###` number and names
none. `ER-###` ids are allocated solely by the error-taxonomy section, in its
family hundred-bands: `EF-SEM` = `ER-1##`, `EF-LOG` = `ER-2##`, `EF-MOD` =
`ER-3##`, `EF-ONT` = `ER-4##`, `EF-EXP` = `ER-5##`, `EF-SCO` = `ER-6##`,
`EF-DIA` = `ER-7##`. A family's home axes are plural, so the number does not
encode the axis; the axis is read from the class record's `axis` key and from
nowhere else. Chapter rows below cite error classes by canonical name and family
token only.

### 8.2a Chapter 0 — The Historical Theory of Demonstration

**Chapter 0. The Historical Theory of Demonstration.** Presents the
reconstructed historical theory (§2.8) as the foundation the modern apparatus
is built over. **Exempt from the proof-object apparatus:** no `PF-###`, no audit
tables, no margin callouts, no exercises, no ledger records. All claims are
`CC-TEXT` with full loci per §13.3. The chapter presents: (1) Aristotle's
*apodeixis* — *epistēmē*, the six conditions on demonstrative premises,
principles (*archai*), *per se* predication and the commensurate universal,
the middle term as cause, *propter quid* vs *quia*, necessity of premises, no
crossing of genera, *nous* and induction, dialectic vs demonstration; (2)
Aquinas's adaptations — *duplex est demonstratio*, *medium demonstrationis*
and the *quid significet nomen* substitution, *praecognita* and the *an
est*/*quid est* order, *per se nota* *quoad se*/*quoad nos*, analogy and the
analogical middle problem, *sacra doctrina* and *praeambula fidei*, *per
se*/*per accidens* causal series, *resolutio*/*compositio* and *separatio*,
the *viae* as "ways" not "proofs", the divine attributes as separate
demonstrations; (3) the later scholastic manual tradition and where it differs
from the texts (three degrees of abstraction vs *separatio*, formalization of
the Ways, Cajetan's analogy system); (4) modern scholarly disputes (whether
quia demonstration satisfies Aristotle's conditions, whether analogical
middles carry syllogistic weight, whether metaphysics is a demonstrative
science on the Aristotelian model, Thomistic vs analytic readings of the
Ways). The chapter closes with the Heritage Declaration (§2.8.4) and the
concordance table (§2.8.5), explicitly labeling the modern apparatus as a
pedagogical superstructure built over the tradition, not the tradition itself.
No ledger allocation. No identifier band. Rule 8.1.1 does not govern this
chapter: it is not a proof-object chapter, and its references to God, a first
cause, or divine attributes are historical claims under `CC-TEXT`, never
premises or conclusions. *Exit:* the reader can state what the historical
theory of demonstration was, distinguish it from the modern apparatus the book
uses, and say why the distinction matters.

### 8.3 Stage A - Proof grammar (Chapters 1-6)

Framework for the whole stage is `NEUTRAL`; `import` is `CONCEPTUAL` or
`LINGUISTIC` throughout. Per §5, `L1-PROSE` may be omitted; `L2-NUM` and
`L3-SKEL` are printed for every specimen.

**Chapter 1. The Proof Object and the Audit.** Installs the apparatus itself.
The reader learns to read and write a `PF-###` record field by field, to run
the fourteen axes in order, and to compute — not choose — a verdict by the
first matching rule. Both proofs of the worked pair carry `import: CONCEPTUAL`
and therefore compute to `V-VALID-ONLY` by verdict rule 3 (§6.3), stated plainly
here and re-motivated at Chapter 6; neither is ever marked `V-PASS`. One worked
pair carries the chapter: a correct proof that
the sum of two even integers is even, and a second proof of the same claim
padded with an unused premise, so `denial-set` minimality and `depends-on`
bookkeeping arrive before any defect does. *Ledger:* `TM-001`–`TM-004`
(*follows*, *premise*, *rule*, *middle*), `DF-001`–`DF-003`, `PR-001`–`PR-003`
(arithmetic principles used as demonstration fodder), `PF-001`–`PF-004`.
*Errors:* none exercised; defects are named but not yet diagnosed. *Drills:*
all fourteen axes read aloud; `LOG`, `WAR`, `DEP`, `SCO` marked. *Exit:* the
reader can transcribe an unstructured prose argument into a complete `L2-NUM`
record with every `MUST` field filled, and can state which axis would detect
each omitted field.

**Chapter 2. Valid Schemas and Their Near Neighbours.** Installs the reflex of
checking a step against a named rule rather than against plausibility. Modus
ponens, modus tollens, hypothetical and disjunctive syllogism, constructive
dilemma; then the near neighbours printed beside the schema each imitates —
affirming the consequent, denying the antecedent, the converse error, the
illicit conversion of a universal — each given a countermodel, not a verdict.
*Ledger:* `TM-005`–`TM-009`, `DF-004`–`DF-007`, `PR-004`–`PR-008`,
`PF-005`–`PF-011` (valid) and `PF-012/S`–`PF-018/S` (invalid, `kind:
SPECIMEN`, each carrying the mandatory `/S` suffix of §7.4). *Errors:* affirming the
consequent, denying the antecedent, illicit conversion (`EF-LOG`); begging
the question in its purely formal form (`EF-DIA`). *Drills:* `LOG` to `FAIL`
with a cited countermodel; `DEP` cycle detection by hand. *Exit:* given any
one-step inference the reader can name the licensing rule or produce a
countermodel, and can say which of `LOG` and `WAR` a given complaint belongs
to.

**Chapter 3. Quantifiers, Scope, and Existential Import.** Installs MD3. It
separates three things ordinary language fuses: the order of nested
quantifiers, the existential commitment of a universal, and the licence to
write a definite description. The shift pair is drilled where the answer is
known (every integer has a larger integer / some integer is larger than every
integer); the uniqueness lemma on *the* least element of a possibly empty set.
*Ledger:* `TM-010`–`TM-015`, `DF-008`–`DF-011`, `DS-001`–`DS-002`,
`PR-009`–`PR-014`, `PF-019`–`PF-030`. *Errors:* illicit quantifier shift,
existential-import mistake, premature definite description (`EF-LOG`); illicit
totalization (`EF-EXP`). *Drills:* `EXI` as a
standalone axis; `LOG`; `SCO`. *Exit:* the reader can write the `domain` field
for any quantified argument, including a per-premise existential-import
declaration, and can apply the MD3 deletion detector.

**Chapter 4. Modal Scope and Kinds of Necessity.** Installs §3.9 while the
examples are still mathematical, so `NEC-LOG`, `NEC-CON`, and `SCP-CMP`/`SCP-DIV`
are met before anything is at stake. The composite/divided defect of §3.9 is run
on a modal toy and then on an arithmetic conditional.
`NEC-MET` and `NEC-NOM` are named and deferred to Chapter 12; the binding test
order is stated and practised in the two applicable cases only. *Ledger:*
`TM-016`–`TM-022`, `DF-012`–`DF-016`, `DS-003`–`DS-004`, `PR-015`–`PR-021`,
`PF-031`–`PF-042`; installs `BR-004` (`SCP-CMP` → `SCP-DIV`) by citation from
§7.7. *Errors:* composite/divided conflation, modal strengthening, modal
collapse (`EF-MOD`). *Drills:* `MOD`; `SCO`; `FID` on a symbolization that
erases a scope.
*Exit:* the reader can annotate every line of a modal derivation with its
`NEC-*`/`POS-*` token and its `SCP-*` token, and can name the `BR-###` that
any change of either would require.

**Chapter 5. Enthymemes and Hidden Assumptions.** Installs premise
archaeology. Given a valid-sounding argument, the reader produces the
*weakest* premise that completes it, distinguishes that from the strongest
premise the author probably believed, and discharges `W-HYP` assumptions.
`denial-set` construction is first taught here as a skill: minimality testing
by removal. *Ledger:* `TM-023`–`TM-026`, `DF-017`–`DF-019`, `DS-005`–`DS-006`,
`PR-022`–`PR-026`, `PF-043`–`PF-052`. *Errors:* missing bridge lemma
(`EF-EXP`); undischarged hypothesis (`EF-LOG`); plausibility taken for warrant
(`EF-DIA`); premise concealed in a definition, in its formal presentation
(`EF-SEM`, cross-referenced to
`LC-08`). *Drills:* `WAR`; `DIA` minimality; `LOG`. *Exit:* the reader can
produce a minimal `denial-set` for any Stage A specimen and demonstrate
minimality by showing that removing each member breaks a named step.

**Chapter 6. The Ceiling of Formal Method.** Installs house rule 2 before it
can be resisted. A flawless, fully audited derivation is graded `V-VALID-ONLY`
because `import` is `CONCEPTUAL`; the MD5 paraphrase detector then runs in
full for the first time, on a conclusion that sounds ontological but survives
paraphrase into a claim about concepts. The chapter states what `L3-SKEL`
provably cannot establish (§5) and requires a `fidelity` sentence from the
reader. *Ledger:* `TM-027`–`TM-029`, `DS-007`–`DS-009`, `PR-027`–`PR-029`,
`PF-053`–`PF-059`. *Errors:* conceptual result paraded as real (`EF-ONT`);
fidelity drift, analogy flattened by symbolization (`EF-SEM`). *Drills:* `ONT`;
`FID`; `DEM` (claimed rung above
achieved rung); verdict computation to `V-VALID-ONLY`. *Exit:* the reader can
run the MD5 paraphrase detector unaided and can state, for a given proof
object, the highest rung its premises could possibly support.

### 8.4 Stage B - Meaning and distinction (Chapters 7-12)

Stage B is where framework-dependent vocabulary enters. It enters at two
declared crossings, each marked in the text and mechanically detectable.

**Crossing 1 — real import.** The first premise anywhere in the book with
`import: REAL` appears in Chapter 8. It is marked with an `IMPORT` callout,
the MD5 paraphrase test is printed in full beside it, and the `ONT` row of the
audit carries a note. *Rule:* no `PF-###` numbered below `PF-060` may print
`import: REAL`; a reviewer greps for it.

**Crossing 2 — framework commitment.** The first premise anywhere in the book
with `framework: AT` and `warrant: W-POST` appears in Chapter 10. It is marked
with an `OBJ` callout naming a standing position that rejects it, and from
that point the book prints a persistent **Framework Notice** environment at
the head of every chapter whose demonstrations consume an `AT` posit. *Rule:*
no `PF-###` numbered below `PF-090` may print `framework: AT` or a `W-POST`
premise, and every proof object using a framework posit MUST carry
`framework-role` per §4.2 and print the framework-conditionality note
immediately below `established`. That declaration is never written into
`not-established`, whose entries are confined to nearby stronger claims
carrying an `overreach-kind` token; an entry stating the framework role of the
object is `SCO` = `FAIL` and does not count toward the field's non-emptiness.

**Chapter 7. Terms, Senses, and the Lexicon.** Installs the `TM`/`DF`/`DS`
split and house rule 5. The reader assigns a `TM-###.n` sense selector at
every occurrence, tests candidate definitions against `LC-08`, and separates
`PRD-UNI`, `PRD-EQV`, and `PRD-ANA` by the ratio test. Analogy enters as a
semantic fact requiring a stated ratio, never as a licence. *Ledger:*
`TM-030`–`TM-041`, `DF-020`–`DF-030`, `DS-010`–`DS-014`, `PR-030`–`PR-036`,
`PF-060`–`PF-070`. *Errors:* equivocation, sense drift, premise concealed in a
definition, analogy flattened (`EF-SEM`). *Drills:* `SEM`; `PRV` (a citation
offered as a definition's warrant);
`FID`. *Exit:* the reader can apply the MD2 substitution detector and can
promote a defective `DF-###` to a `PR-###` with the correct warrant token.

**Chapter 8. Identity, Non-Contradiction, and Qualification.** Installs `QUA-
SIMP`/`QUA-SEC` and the same-time/same-respect qualifications as explicit
printed fields rather than as understood provisos. The principle of non-
contradiction is stated twice and given two ledger records: a semantic form
(`import: CONCEPTUAL`, `NEC-LOG`, `framework: NEUTRAL`) and an ontological
form (`import: REAL`, `NEC-MET`, `framework: NEUTRAL`, `warrant: W-SELF` with
the analysis printed). Crossing 1 occurs at the second. Identity is treated
with Leibniz's law and its intensional failure cases. *Ledger:*
`TM-042`–`TM-050`, `DF-031`–`DF-038`, `DS-015`–`DS-020`, `PR-037`–`PR-046`
(`PR-039` semantic PNC, `PR-040` ontological PNC),
`PF-071`–`PF-080`. *Errors:* suppressed relativization — dropping a `QUA-SEC`
respect, inferring `QUA-SIMP` from `QUA-SEC` — and substitution into an opaque
context (`EF-SEM`); conceptual result paraded as real (`EF-ONT`). *Drills:*
`ONT`; `SEM`; `MOD`; `WAR` on `W-SELF`. *Exit:* the reader can state any
contradiction claim with its time index and respect printed, and can say which
of the two PNC records a given argument consumes.

**Chapter 9. Predication and Its Modes.** Installs the `subject`/`attribute`
discipline and the *per se* / *per accidens* distinction that MD10 relies on.
Modes: essential and accidental predication, denominative predication,
predication of a whole versus of a part, and predicating of a kind versus
quantifying over its members. Still `framework: NEUTRAL` — the chapter
concerns what predication does, not yet what natures are. *Ledger:*
`TM-051`–`TM-060`, `DF-039`–`DF-046`, `DS-021`–`DS-026`, `PR-047`–`PR-055`,
`PF-081`–`PF-089`. *Errors:* composition, division, part-to-whole transfer
(`EF-LOG`); illicit totalization, accidental co-occurrence taken for a *per se*
middle (`EF-EXP`). *Drills:* `SCO` (attribute proved of
a wider subject than `subject` names); `ONT`; `EXP`. *Exit:* the reader can
fill `subject`, `attribute`, `middle`, and `middle-kind` for any argument and
justify the `middle-kind` choice.

**Chapter 10. Essence and Accident.** Crossing 2. The essence/accident
apparatus enters explicitly as a framework posit — the first `W-POST` premise,
`framework: AT` — with the strongest nominalist and class-nominalist
objections recorded as `OB-###` and replies that may concede. The reader is
shown what changes when the posit is accepted and what the same argument looks
like with it withdrawn. *Ledger:* `TM-061`–`TM-069`, `DF-047`–`DF-053`,
`DS-027`–`DS-031`, `PR-056`–`PR-064` (`PR-056` the essence posit, `kind:
FRAMEWORK-POSIT`), `OB-020`–`OB-034`, `PF-090`–`PF-099`. *Errors:* framework
posit unmarked, straw opponent (`EF-DIA`);
distinction of reason reified (`EF-ONT`). *Drills:* `FRM`; `DIA`;
verdict computation to `V-OPEN`. *Exit:* the reader can classify any premise
as neutral, internal to a declared framework, or establishing part of one, and
can state the live positions on each side of a `V-OPEN` verdict.

**Chapter 11. Conceptual, Virtual, and Real Distinction.** Installs `DK-REAL`,
`DK-VIRT`, `DK-NOM` and the binding test order of §3.9. It prevents the book's
central failure mode — treating a distinction the mind draws as a distinction
in the thing — and the reverse error, collapsing a real distinction because
separation is not observable. *Ledger:* `TM-070`–`TM-076`, `DF-054`–`DF-058`,
`DS-032`–`DS-038`, `PR-065`–`PR-072`, `OB-035`–`OB-045`, `PF-100`–`PF-109`.
*Errors:* distinction of reason reified, real distinction collapsed,
`DK-VIRT` overclaimed as `DK-REAL` (`EF-ONT`). *Drills:* `ONT`;
`DIA`; `SCO`. *Exit:* the reader can run the three-step test on any asserted
distinction and produce the entailment pair that separates `DK-VIRT` from `DK-
NOM`.

**Chapter 12. Possibility, Actuality, and Real Modality.** Completes §3.9:
`NEC-NOM` and `NEC-MET` are now discharged from Chapter 4's deferral, the
binding test order is run in full, and the conceivability–possibility bridge
is installed as `BR-001` carrying `W-POST` — never as a free inference.
`POS-MET` must be exhibited, not merely undefeated. *Ledger:*
`TM-077`–`TM-079`, `DF-059`, `DS-039`, `PR-073`–`PR-079`,
`OB-046`–`OB-059`, `PF-110`–`PF-119`; installs by citation `BR-001`
(conceivability, `W-POST`), `BR-002` (nomological-to-metaphysical, `W-POST`),
and `BR-003` (`NEC-CON` → `NEC-MET`, `W-DEM`). *Errors:* regularity promoted,
conceivability taken for possibility, modal collapse, conceptual necessity read
as real (`EF-MOD`). *Drills:* `MOD`; `ONT`; `DIA` against a
Humean and a modal-fictionalist opponent at full strength. *Exit:* the reader
can assign a necessity kind by running the four tests in order and can name
the `BR-###` required by any upgrade.

### 8.5 Stage C - First metaphysical demonstrations (Chapters 13-17)

From Chapter 13 all three layers are printed for every `kind: DEMONSTRATION`
(§5), and every such object carries all `MUST` fields. **Containment
rule:** every Stage C demonstration has at most seven `steps` lines, at most
five premises, and a `depends-on` list confined to Stages A–C, so that a
reader can audit it completely in one sitting; a demonstration exceeding these
bounds is deferred to Stage E. Each chapter presents exactly one central
`DEMONSTRATION` plus its defective near neighbours as `SPECIMEN` objects.

**Chapter 13. Change and the Persisting Subject.** First full canonical proof
object. Central demonstration: whatever changes has something that persists
through the change and something that does not. It is chosen as the smallest
claim in the book carrying genuine `import: REAL` with a genuine `denial-set`,
and because the Eleatic and Humean denials are both statable at full strength.
*Ledger:* `TM-080`–`TM-088`, `DF-060`–`DF-066`, `DS-040`–`DS-044`,
`PR-080`–`PR-090`, `PF-120`–`PF-134`, `OB-060`–`OB-072`. *Errors:* temporal
succession taken for change, replacement described as alteration (`EF-SEM`);
conceptual result paraded as real (`EF-ONT`).
*Drills:* all fourteen axes; `EXP` and `DEM` marked for the first time on a
real claim. *Exit:* the reader can produce a complete `PF-###` record for a
supplied prose argument and defend every field.

**Chapter 14. Act and Potency.** Central demonstration: potency is neither
actuality nor nothing — a real capacity distinct from both the actual state
and mere logical possibility. Drills `DK-VIRT` and the `NEC-MET`/`NEC-CON`
boundary on one object. `middle-kind: FORMAL`. *Ledger:* `TM-089`–`TM-096`,
`DF-067`–`DF-072`, `DS-045`–`DS-049`, `PR-091`–`PR-102`,
`PF-135`–`PF-148`, `OB-073`–`OB-085`. *Errors:* potency reified as a hidden
actuality, silent commitment (`EF-ONT`); possibility (`POS-LOG`) substituted
for real potency, modal collapse (`EF-MOD`). *Drills:* `ONT`; `MOD`; `EXP`;
`FRM`. *Exit:*
the reader can distinguish, for a given capacity claim, whether `POS-LOG`,
`POS-NOM`, `POS-MET`, or a real potency is being asserted, and which premise
carries the difference.

**Chapter 15. Dependence Without Time.** Installs §3.9's priority tokens.
Central demonstration:
a dependence relation can hold between simultaneous relata, so temporal
priority is neither necessary nor sufficient for causal or ontological
priority. Every `PRI-*` token gets its deciding test, drilled where temporal
intuition points the wrong way; `SIM-NAT` blocks the inference from
simultaneity to independence. *Ledger:* `TM-097`–`TM-105`, `DF-073`–`DF-078`,
`DS-050`–`DS-053`, `PR-103`–`PR-115`,
`PF-149`–`PF-163`, `OB-086`–`OB-098`; installs by citation `BR-005`
(`PRI-ONT` → `PRI-GND`) and `BR-006` (blocking `PRI-CAU` → `PRI-TMP`).
*Errors:* temporal priority read as causal or ontological, causal priority made
chronological, `PRI-ONT` taken to entail `PRI-GND`, order of knowing read as
order of being, circular explanatory dependence (`EF-EXP`). *Drills:* `DEP`;
`EXP`; `MOD`. *Exit:* the reader can assign a `PRI-*` token by its deciding
test and name the `BR-###` required to swap it for another.

**Chapter 16. Composition and the Composite.** Central demonstration: a
composite whose parts are really distinct depends on something other than any
one of its parts for its being composed. Runs composition and division against
the `DK-REAL`/`DK-VIRT` machinery of Chapter 11 and the part/whole predication
of Chapter 9. Aggregate, structured-whole, and mereological-nihilist readings
each appear at full strength as rival positions in `denial-set`. *Ledger:*
`TM-106`–`TM-113`, `DF-079`–`DF-085`, `DS-054`–`DS-057`, `PR-116`–`PR-128`,
`PF-164`–`PF-180`, `OB-099`–`OB-110`. *Errors:* composition, division, invalid
transfer from members to whole (`EF-LOG`); illicit totalization (`EF-EXP`);
overstrong conclusion (`EF-SCO`).
*Drills:* `ONT`; `SCO`; `DIA` against a mereological nihilist and a structure-
only theorist. *Exit:* the reader can state, for any whole/part argument,
which direction of transfer is being attempted and what licenses it.

**Chapter 17. Ordered Series and the Explanatory Middle.** Stage C
consolidation. Installs `SER-ACC`/`SER-ESS` with the concurrency test and
closes the stage on the `RG-THAT`/`RG-WHY` boundary: one conclusion reached
twice, through an `EFFECT-SIGN` middle and through a grounding middle, with
the MD11(b) reversal detector printed for both routes — two full sentences
each, and for the grounding route the stated reason its converse fails. The
`EFFECT-SIGN` route is printed as the grounding route's `stripped-variant`: a
valid derivation of the same `claim` not routing through the grounding middle,
in `L2-NUM` with its rule names, plus one sentence naming what it leaves
unexplained. The `EFFECT-SIGN` object itself carries no `stripped-variant`
field, that field being conditional on `rung: RG-WHY`, and instead prints its
`OV-EXPL` entry naming the grounding middle it does not take. The chapter
states this asymmetry explicitly. This chapter prints the book's first
`RG-WHY` object and installs the MD11 apparatus. The
chapter reaches no conclusion about whether any actual series is essentially
ordered — Stage E's burden — and says so in `not-established`. The stage's
first multi-proof dependency diagram is printed here, covering
`PF-120`–`PF-199`. *Ledger:* `TM-114`–`TM-119`, `DF-086`–`DF-089`,
`DS-058`–`DS-059`, `PR-129`–`PR-139`, `PF-181`–`PF-199`,
`OB-111`–`OB-119`; installs by citation `BR-007` (distributive → collective
predication). *Errors:* series equivocation — `SER-ACC` and `SER-ESS`
conflated, or a regress argument run without declaring the series kind — and
sign taken for ground (`EF-EXP`); overstrong conclusion, stronger than the
series argument licenses (`EF-SCO`). *Drills:* `EXP`; `DEM`; `DEP`; `SCO`;
full verdict computation
across all six rules. *Exit:* the reader can grade a supplied demonstration's
achieved rung against its claimed rung, exhibit a stripped variant, and write
a `not-established` entry that a hostile reviewer cannot call dishonest.

### 8.6 Handoff

Stage D begins at **Chapter 18**. Chapter numbering continues without gap; the
Stage D–F lane owns Chapters 18 and upward, and allocates ledger ids from the
fixed Stage D–F floor of 200 in every class, never from the unallocated
headroom below the Stage A–C ceilings of §8.2.


## 8. Curriculum and Table of Contents (Part 2: Stages D-F)

### 8.7 Identifier ranges owned by Stages D–F

Stage C ends at Chapter 17 (§8.5). Stage D is Chapters 18–22, Stage E 23–28,
Stage F 29–35, and the closing chapter is 36. Chapter numbers below are resolved,
not placeholders; exercises and solutions take the spine forms `EX-##.##` /
`SO-##.##` with that number in the first field (`EX-18.07` … `EX-36.##`).

| Class | Stage D | Stage E | Stage F |
|---|---|---|---|
| `TM-###`, `DF-###`, `DS-###` | 200–249 | 300–349 | 400–449 |
| `PR-###` | 200–249 | 300–399 | 400–499 |
| `PF-###` | 200–299 | 300–399 | 400–499 |
| `OB-###` / `RP-###` | 200–299 | 300–399 | 400–499 |

1. Stages A–C own every id below 200; 500–899 is the coordinator reserve and
   900–999 the specification appendix reserve (§8.2, §7.4). Allocation within a
   band is strictly in order of introduction, preserving the
   sort-equals-introduction invariant (§10.1(1)).
2. Stages D–F mint **no** `ER-###` and **no** `BR-###`; they cite classes and
   bridges owned by the error-taxonomy and modality sections. A chapter needing
   an uncatalogued bridge may not invent one: it files a `PR-###` stub in its
   own band, takes `V-PARTIAL`, and stops.
3. Every specimen is a `PF-###` in the Stage D band; each of its premises that
   survives audit becomes a `PR-###`, since an unrecorded premise cannot be
   cited later. Stage D mints no `kind: DEMONSTRATION` at `rung: RG-WHY` — its
   objects are specimens — so any Stage D chapter claiming a first is in error.
4. **Cite before minting.** Before minting any `TM-###`, `DF-###`, or `DS-###`, a
   Stage D–F chapter searches the register of `ACTIVE` records for one covering
   the notion and cites it. A new lexical id is legal **only** where no `ACTIVE`
   record covers the notion. Where the new record stands in any relation of
   strength, restriction, disambiguation, or variance to an existing one, the
   chapter records the §10.3 `relations` edge on both records (`LC-14`).
   Re-minting an existing notion under a new name is a hard error of this
   section, surfaced by `LC-13`; and no sign-off may discharge `LC-13` by
   asserting independence for a distinction Stages A–C already installed.

---

### 8.8 Stage D — Adversarial diagnosis (Chapters 18–22)

#### 8.8.1 Specimen admission (D1–D7, all binding)

The proof-object field **`provenance`** (§4.1 print order, §4.2 field table),
required on every `kind: SPECIMEN` proof object, is one of `SPC-HIST` (real,
attributed published argument), `SPC-COMP` (composite of positions actually
held, unattributed), `SPC-CONS` (constructed). Absence is a defect.

1. **D1 Deception threshold.** At most **two** axes `FAIL`, exactly one being
   the *lesson axis*; a second `FAIL` must be a consequence of the first and the
   audit must say so. Three or more failing axes is a caricature: inadmissible.
2. **D2 Shape integrity.** `LOG` = `OK`, unless invalidity is the lesson, in
   which case the bad step differs from a valid rule by exactly one quantifier,
   one modal operator, or one occurrence of one term.
3. **D3 Live premises.** Every premise is `OK` on `WAR` or is defended in print
   by a named standing position. No premise that no competent philosopher holds.
4. **D4 No telegraphing.** First presentation carries no marker words
   ("obviously", "surely"), no scare quotes on the equivocal term, and **no
   margin callouts**; callouts appear only in the audit pass printed after it.
5. **D5 Non-trivial remainder.** Across Stage D at least half the specimens have
   a non-`NONE` `survives`. A stage where everything collapses teaches rejection,
   not diagnosis.
6. **D6 Anti-manufacture.** An author **MUST NOT** weaken an argument to make it
   a specimen, and may not present a manufactured weak argument as a hard case.
   If reconstruction at maximum strength removes the defect, the specimen is
   withdrawn and reclassified `DEMONSTRATION` or `DIALECTICAL`. *Detector:* the
   audit's `errors` entry points at a step the strongest reconstruction lacks.
7. **D7 Symmetry.** For every two specimens whose `framework` is a rival to the
   book's, at least one with `framework: AT` is audited. *Detector:* count
   `framework` fields in the Stage D band.

#### 8.8.2 Real published arguments (permitted, under R1–R6)

1. **R1** `SPC-HIST` requires edition and section in `scholion`. A citation never
   occupies a warrant slot (`PRV` = `FAIL`).
2. **R2 Strongest reconstruction first.** Before any audit mark or verdict, the
   chapter prints an `L2-NUM` reconstruction certified as the strongest version
   the source's text supports. The proof-object field
   **`reconstruction-note`** (§4.1 print order, §4.2 field table), required on
   `SPC-HIST`: one sentence naming every place the reconstruction supplies
   material the source leaves implicit, one stating whether the source would
   accept it.
3. **R3 Charity closure.** If a repair is licensed by the source's own stated
   commitments, the *repaired* argument is what the book attributes to the
   source; the defect is reported as one of a common presentation, not of the
   author.
4. **R4** Contemporary authors may be specimens only for work published in a form
   intended as final. Lectures, interviews, correspondence: inadmissible.
5. **R5** An `SPC-COMP` is labelled a composite and never introduced with "as X
   argues".
6. **R6 Argument, not author.** *Detector:* any sentence in a Stage D audit whose
   grammatical subject is an author's name and whose predicate is evaluative.

#### 8.8.3 Chapters

**Chapter 18 — Reading an argument you suspect is wrong.**
*Purpose.* Installs the diagnostic order: reconstruct at maximum strength, fix
the lexicon, run the fourteen axes in §6.2 order, compute the verdict, only then
repair. Its thesis is that a reader who reaches for the defect first reliably
mislocates it.
*Introduces.* `TM-200`–`TM-204`; `DS-200` (defect of an argument vs. of a
presentation); `PF-200/S` (`SPC-CONS` exemplar).
*Errors.* None as targets; the procedure itself is the object.
*Rubric.* All fourteen axes, in order, on one specimen.
*Exit.* On an unseen specimen the reader's fourteen-row audit matches the
solution on ≥ 12 rows and the verdict exactly (`EX-18.07`).

**Chapter 19 — Specimens that fail on sense.**
*Purpose.* Drills what a formal check cannot see: a sense selector shifting
silently between lines, an analogical term carried as univocal, a substantive
claim smuggled into a `DF-###`. Every specimen here is formally impeccable.
*Introduces.* `PR-200`–`PR-204`; `DS-201` (`PRD-ANA` with stated ratio vs.
`PRD-EQV`); `PF-201/S`–`PF-204/S`.
*Errors.* Equivocation; hidden change in a technical term; analogy read as
univocity; disputed premise hidden in a definition; conceptual distinction taken
as real.
*Rubric.* `SEM`, `ONT`, `FID`, with `LOG` = `OK` throughout.
*Exit.* Reader names the shifted `TM-###.n` and its line in three of four unseen
specimens, and repairs one by promoting a definition to a warranted `PR-###`
(`EX-19.09`).

**Chapter 20 — Specimens that fail on modality and scope.**
*Purpose.* Drills illicit strengthening: composite read as divided, conceptual
necessity dressed as `NEC-MET`, regularity promoted without a bridge,
conceivability read as `POS-MET`, conclusions wider than the premises license.
*Introduces.* `PR-205`–`PR-209`; `DF-200` (bridge premise, generic form);
`PF-205/S`–`PF-209/S`.
*Errors.* Modal strengthening; conceptual vs. real necessity; modal
composition/division; empirical regularity promoted to necessity; overstrong
conclusion; modal collapse.
*Rubric.* `MOD`, `SCO`, `DEM`; the `NEC-LOG`→`NEC-CON`→`NEC-NOM`→`NEC-MET` test
order run by hand.
*Exit.* Reader rewrites an overstrong conclusion as the exact `established`
sentence licensed and supplies a `not-established` entry a solution reviewer
accepts as neither empty nor dishonest (`EX-20.11`).

**Chapter 21 — Specimens that fail on dependence and existential import.**
*Purpose.* Drills failures peculiar to causal and quantificational metaphysics:
temporal succession read as causal or grounding priority, an accidental series
treated as essential, an existential conclusion with no nonemptiness premise, a
definite description before its uniqueness lemma, member-to-collection
totalization.
*Introduces.* `PR-210`–`PR-216`; `PF-210/S`–`PF-216/S`. Mints no `DS-###`: the
`SER-ACC`/`SER-ESS` distinction and its concurrency test are Stage C property
(`DS-058`–`DS-059`, Chapter 17) and are cited, not re-minted (§8.7(4)).
*Errors.* `PRI-TMP` read as `PRI-CAU`/`PRI-GND`; accidental vs. essential series;
existential-import mistakes; illicit quantifier shift; composition/division;
illicit totalization; circular explanatory dependence.
*Rubric.* `DEP`, `EXI`, `ONT`.
*Exit.* Reader applies the concurrency test to an unseen regress argument,
declares `SER-ACC` or `SER-ESS` with a reason, and states which the argument
needs (`EX-21.08`).

**Chapter 22 — Repair, remainder, and the audit of a real argument.**
*Purpose.* Turns diagnosis into salvage: `V-FATAL` versus `V-REPAIR`, minimal
repairs, an exact statement of what survives. Closes with one full `SPC-HIST`
treatment under R1–R6 — reconstruction, `reconstruction-note`, audit, repair, and
a statement of what the source is and is not thereby committed to.
*Introduces.* `PR-217`–`PR-224`; `PF-217/S`–`PF-220/S` (`SPC-HIST`);
`OB-200`–`OB-210` with matched replies.
*Errors.* Missing bridge lemma; begging the question; affirming the consequent in
metaphysical dress; transfer from members to whole.
*Rubric.* Verdict rules 1–6; `WAR`, `DIA`, `PRV`.
*Exit.* Reader exhibits a repair plus `survives` for an unseen `V-REPAIR`
specimen and writes `why-no-repair` for an unseen `V-FATAL` one (`EX-22.12`).

---

### 8.9 Stage E — Multi-step demonstrations (Chapters 23–28)

**E1 Closure.** No Stage E chapter may consume a `PR-###` that is not already
`status: ACTIVE`, with non-empty `established-by` and an earlier `introduced-at`.
`LC-01` detects violation. There is no exception for propositions "everyone
grants".
**E2 The three legal moves.** When a step needs something undemonstrated the
chapter may only (a) demonstrate it in place as a lemma with its own `PF-###` and
full audit; (b) file a `PR-###` stub in `missing`, weaken the conclusion, take
`V-PARTIAL`; or (c) admit it as `W-POST`, set `framework: AT`, take `V-OPEN`.
Asserting it, citing an authority, or absorbing it into a `DF-###` are defects.
**E3 Edges printed.** Each chapter opens with incoming edges listed by id and
closes with a `consumed-by` reconciliation (`LC-04`).
**E4 No fusion.** A chain is a graph over ids, never one long numbered argument;
each link keeps its own `established` and `not-established`.
**E5 No definite article.** Until a uniqueness lemma exists the book writes "a
non-derivative actualizer", never "the" (MD3).

**Chapter 23 — Change, act, and potency.**
*Purpose.* The book's first multi-step demonstration: change requires a subject
in potency actualized by something already in act, act/potency carried as
`DK-VIRT` and argued, not assumed. Here a `middle-kind` is first defended.
*Introduces.* `TM-300`–`TM-306`; `DS-300`; `PR-300`–`PR-308`; `PF-300`–`PF-302`.
*Errors.* Conceptual distinction treated as real; middle that accompanies rather
than grounds.
*Rubric.* `ONT`, `EXP`, `DEP`; the first `RG-WHY` claim inside a multi-step
chain, and the first whose `middle` and its `PRI-GND` priority are argued rather
than displayed. The apparatus itself — reversal detector, asymmetry witness,
stripped-variant standard — is installed at Chapter 17, which prints the book's
first `RG-WHY` object; this chapter consumes it and does not re-teach it.
*Exit.* Reader reconstructs `PF-300`'s `depends-on` graph from the printed proofs
and names the one premise whose denial blocks all three (`EX-23.10`).

**Chapter 24 — Composition and composite dependence.**
*Purpose.* Demonstrates that a composite depends on its principles of composition
and on whatever unites them, distinguishing that dependence (`PRI-ONT` or
`PRI-GND`, argued) from mereological truism, temporal assembly, `PRI-DEF`.
*Introduces.* `PR-309`–`PR-317`; `PF-303`–`PF-305`. Cites the Stage C
composition distinctions (`DS-054`–`DS-057`, Chapter 16); mints `DS-301`
(composition vs. aggregation) **only** if aggregation is not covered there, with
a `RESTRICTS` edge to the Stage C record and its inverse (§8.7(4)).
*Errors.* Transfer from members to whole; illicit totalization; definitional
priority mistaken for real dependence.
*Rubric.* `DEP`, `ONT`, `SCO`.
*Exit.* For an unseen composite the reader names the `PRI-*` token the argument
requires and the test that would settle it (`EX-24.09`).

**Chapter 25 — Essentially ordered causality.**
*Purpose.* Establishes `SER-ESS`/`SER-ACC` as a demonstrated result, not a
stipulation, and demonstrates what an essentially ordered series requires here
and now. The regress premise is a premise, with its own warrant and its own
strongest objection, never an obvious truth.
*Introduces.* `PR-318`–`PR-327`; `PF-306`–`PF-309`; `OB-300`–`OB-306`.
*Errors.* Causal dependence confused with chronological succession; accidental
vs. essential series; begging the question in the regress premise.
*Rubric.* `DEP`, `DIA`, `WAR`; concurrency test applied formally.
*Exit.* Reader constructs the strongest objection to the no-infinite-`SER-ESS`
premise and answers it without strengthening the original claim (`EX-25.07`).

**Chapter 26 — Contingency and dependence.**
*Purpose.* Separates four routinely fused claims: that a thing might not have
existed, depends on something, has its explanation outside it, is caused. Each is
demonstrated or refused separately, modal kind declared on every line.
*Introduces.* `PR-328`–`PR-337`; `DS-302` (`CONT` vs. `PRI-ONT`), carrying
`DISAMBIGUATES` edges to the Stage B modality distinctions and the Stage C
`PRI-*` records it refines; `PF-310`–`PF-313`.
*Errors.* Modal strengthening; illicit totalization ("each member is contingent,
therefore the totality is"); conceptual necessity read as real.
*Rubric.* `MOD`, `SCO`, `EXI`, `DIA`; Humean and modal-fictionalist denials at
full strength.
*Exit.* Reader shows why the totality inference fails, states the premise that
would license it, and marks that premise's warrant honestly (`EX-26.11`).

**Chapter 27 — Essence and existence.**
*Purpose.* Treats the real distinction as a contested `PR-###`, not a background
assumption: demonstration given, `DK-*` tag argued, strongest deflationary and
Fregean objections stated, verdict recorded honestly even if `V-OPEN`.
*Introduces.* `TM-307`–`TM-311`; `DS-303`, carrying a `RESTRICTS` edge to the
Stage C `DK-REAL`/`DK-VIRT`/`DK-NOM` record it refines, and its inverse;
`PR-338`–`PR-347`; `PF-314`–`PF-317`; `OB-307`–`OB-315`.
*Errors.* Abstraction treated as a real distinction; existential-import mistakes;
disputed premise hidden in a definition.
*Rubric.* `ONT`, `EXI`, `FRM`, `DIA`; `DK-REAL`/`DK-VIRT`/`DK-NOM` test order.
*Exit.* Reader states which `DK-*` tag each of three rival positions assigns and
what each must give up (`EX-27.08`).

**Chapter 28 — A non-derivative principle, and the audit of the whole graph.**
*Purpose.* Assembles the prior chapters into the book's central result — at least
one non-derivative actualizing or explanatory principle, stated at exactly the
strength the chain licenses — then audits the graph itself and prints the
`not-established` list Stage F must bridge.
*Introduces.* `PR-348`–`PR-360`; `PF-318`–`PF-320`; `OB-316`–`OB-325`.
*Errors.* Conclusion stronger than the demonstrated result; circular explanatory
dependence; missing bridge lemma.
*Rubric.* All fourteen on the terminal proof, plus the eleven spine checks
`LC-01`–`LC-11` (§10.5) on the accumulated ledger.
*Exit.* From the printed `not-established` fields alone the reader recites the
full list of what has not been shown, and finds three defects planted in a
supplied ledger fragment (`EX-28.12`).

---

### 8.10 Stage F — From a first principle to further attributes (Chapters 29–35)

A reviewer rejects the stage outright if any of F1–F7 is violated once.

1. **F1 One attribute, one demonstration.** Each attribute gets its own `PF-4##`,
   its own `PR-4##`, and its own complete fourteen-axis audit. Compound
   attributes split: "simple" is at minimum three demonstrations (matter/form,
   essence/existence, subject/accident), each with its own id. Reaching a
   non-derivative actualizer establishes **none** of simplicity, unity,
   immateriality, intellect, goodness, or omnipotence. The `claim` and
   `established` of every `PF-4##` predicate **exactly one** attribute term of
   the terminus; conjunction, disjunction, and enumeration of attributes in
   `claim`, `established`, `subject`, or `attribute` are inadmissible, as is a
   single attribute term whose sense is stated as a conjunction or which a
   competent reader would unpack into two. *Detector:* an "and", an "or", or a
   comma-list joining predicates in `claim` or `established`, and any attribute
   term whose `TM-###.n` sense contains a conjunction. A chapter needing two
   attributes files two `PF-4##`, two `PR-4##`, two bridge tables, and two
   audits; the second may cite the first by `W-DEM`.
2. **F2 Printed bridge table.** Immediately before its own `L2-NUM`, each
   `PF-4##` prints four columns: *incoming `PR-###`* | *additional premises with
   warrant token, modality, framework status* | *`BR-###` licensing any change of
   necessity kind, modal scope, or `PRI-*` token* | *resulting `PR-4##`*. One
   table per attribute demonstration; a merged or chapter-level bridge table is
   inadmissible, and the fourth column holds exactly one `PR-4##`. Every
   additional premise in the second column MUST appear verbatim as a `pid` in
   that same object's `premises`, and every `pid` in that `premises` list which
   is not a `W-DEM` citation of a first-column incoming `PR-###` MUST appear in
   the second column; a premise present in one and absent from the other is
   `DEP` = `FAIL`. *Detector:* set-compare the second column against `premises`
   for each `PF-4##`. Each additional premise is warranted independently of the
   terminus result. A premise whose only support is that the terminus would
   otherwise fail to match a traditional description is circular: `WAR` and
   `DEP` = `FAIL`, verdict `V-FATAL`.
3. **F3 Honest stopping.** Where the bridge is genuinely contested or the book
   judges the demonstration incomplete, the chapter records `V-OPEN` or
   `V-PARTIAL`, names the live positions on each side, writes `established` as
   the conditional actually shown, and **stops**. It does not then assert the
   attribute in weaker prose, in a summary, or in a later chapter.
4. **F4 The terminus dossier.** **New closing apparatus, spine silent: the
   `dossier`** — not a proof-object field, but a list reprinted at the close of
   every Stage F chapter, of the records licensed to predicate an attribute of
   the terminus. *Line format:* each line prints the
   `PR-4##`, its `established` verbatim, its `audit-verdict`, and the single
   attribute term it licenses; **only that term** is licensed, and no synonym, no
   cognate, no traditional equivalent. *Admission:* a record enters the dossier
   only if (a) its `audit-verdict` is `V-PASS`; (b) its `established` is
   categorical — containing no conditional and no "if", "provided that",
   "assuming", or "within `<framework>`" operator, its proof containing no
   `W-HYP` premise whose discharge is not itself a demonstrated `PR-###`; and
   (c) every id in its transitive `depends-on` closure is itself `V-PASS` with a
   categorical `established`. Conditional, hypothetical, and framework-relative
   results are printed with their chapter and listed in closing-apparatus item F,
   never in the dossier. **No predicate may be applied to the terminus anywhere
   in the book unless it matches a dossier line.** *Detector:* list every
   sentence in the book whose grammatical subject, object, or appositive denotes
   the terminus, and for each list every predication made of it in any form —
   predicate adjective, predicate nominative, appositive noun phrase, relative
   clause, participial phrase, prepositional modifier, possessed noun, and every
   finite verb other than the copula. Each must match, in its attribute term, a
   dossier line; an unmatched predication is `SCO` = `FAIL` plus `ER-604`.
   *Single exception:* a theological remark block (§13.4), structurally outside
   the proof object and outside the dossier, in which every predication of the
   terminus carries the sentence-initial prefix "On revelation," or "As a datum
   of faith,", is accompanied in the same block by the dossier line stating what
   was in fact demonstrated, and never recurs outside that block. A prefixed
   predicate reappearing outside its block is `PRV` = `FAIL`.
5. **F5 Naming prohibition.** The phrase **"proof of God" is forbidden** as the
   name of anything, as is any singular "the proof", "the argument", or "the Five
   Ways" naming a plurality of distinct results. Instead the book names each
   result by id and short name ("`PR-401`, non-derivative actuality") and the
   collection "the attribute series" or "the demonstrations of Stage F". A
   traditional label may appear only in a `scholion`, as a terminological claim.
   The form "we have proved that God is X" is forbidden; the licensed form names
   the id, the attribute, and the achieved rung: "`PR-4##` establishes, at
   `<achieved rung>`, that a non-derivative actualizer is X." Where that object's
   verdict is `V-OPEN` or `V-PARTIAL`, or any load-bearing premise carries
   `W-POST`, the §16.4(2) conditionality clause is appended **in the same
   sentence** and is not deferred to a note. A Stage F sentence using
   "establishes" with no printed achieved rung is `DEM` = `FAIL`; the same
   sentence omitting a triggered conditionality clause is `FRM` = `FAIL`. A
   reviewer greps every Stage F chapter for "establishes" and checks both.
6. **F6 Identification is not a conclusion.** An **identification claim** is any
   proposition asserting identity, co-reference, title-sharing, or "is what `X`
   calls" between the terminus, or any dossier subject, and a deity, divine name,
   or object of worship of any religious tradition. The prohibition is by
   content, not by token: an identification claim is inadmissible in `claim`,
   `premises`, `steps`, `depends-on`, `established`, or `denial-set` of any proof
   object at any rung, under **every** warrant token including `W-POST`, `W-HYP`,
   `W-SELF`, and `W-DEM`. It may exist in the ledger only with
   `kind: DISPUTED-PREMISE`, `terminal: true`, and empty `consumed-by`, and may
   never appear in the Framework Declaration's posit table.
   *Prose rule.* The tokens "God", "divine", "divinity", "deity", and any proper
   divine name of a tradition are forbidden in body prose, in chapter and section
   titles, in `claim`, `established`, `not-established`, in margin callouts, and
   in exercise and solution text — everywhere outside Chapter 35, a quoted
   `CC-TEXT` passage, a `scholion`, and a theological remark block.
   *Detector:* `grep -nEiw 'god|gods|divine|divinity|deity'` over every authored
   file; each surviving hit is `SCO` = `FAIL` plus `ER-604`, and a hit inside a
   proof object is `PRV` = `FAIL`, verdict `V-FATAL`. Chapter 35 prints these two
   rules as rules of the book and itself demonstrates nothing about co-reference.
7. **F7 Denial sets are never thin.** Every Stage F `denial-set` names a standing
   contemporary position with its own strongest reason. A chapter whose only
   named opponent is historical is incomplete.

**Chapter 29 — The bridge discipline.**
*Purpose.* States F1–F7 with worked micro-examples and shows by counter-example
how one unbridged step turns an audited chain into an overclaim. Introduces the
dossier, initialized with the Stage E result alone.
*Introduces.* `TM-400`–`TM-404`; `DF-400` (bridge table); `PR-400`; `PF-400/S`
(deliberately unbridged `SPC-CONS`).
*Errors.* Missing bridge lemma; overstrong conclusion; circular warrant.
*Rubric.* `SCO`, `DEP`, `WAR`, `DEM`.
*Exit.* Given an attribute claim and its incoming `PR-###` the reader writes the
bridge table and names at least one additional premise required (`EX-29.06`).

**Chapter 30 — Absence of passive potency.**
*Purpose.* The exemplar bridge, worked in full, from the Stage E terminus to the
claim that a non-derivative actualizer has no unactualized passive potency. Every
additional premise is separately warranted and separately objected to.
*Introduces.* `PR-401`–`PR-406`; `PF-401`–`PF-403`; `OB-400`–`OB-406`.
*Errors.* Modal strengthening; equivocation on "potency".
*Rubric.* All fourteen; `MOD` and `SEM` emphasized.
*Exit.* Reader states which premise a Humean and a grounding deflationist
respectively deny and why each denial is reasonable on its own terms
(`EX-30.08`).

**Chapter 31 — Non-composition: three separate demonstrations.**
*Purpose.* Absence of matter/form, essence/existence, and subject/accident
composition as three distinct results with three distinct dependency edges, and
why establishing one establishes none of the others. Where the essence/existence
bridge depends on Chapter 27's contested result, the dependence is printed and the
verdict inherits it.
*Introduces.* `PR-407`–`PR-418`; `PF-404`–`PF-409`; `OB-407`–`OB-418`.
*Errors.* Composition/division; conceptual distinction treated as real; silent
inheritance of a contested premise.
*Rubric.* `ONT`, `DEP`, `FRM`, `SCO`.
*Exit.* Reader shows the three results logically independent by exhibiting, for
each, a position granting the other two and denying it (`EX-31.09`).

**Chapter 32 — Uniqueness, and the licensing of the definite article.**
*Purpose.* Demonstrates, or fails to demonstrate, at most one terminus. Only on
this chapter's strength may later text write "the" non-derivative actualizer; if
the argument takes `V-OPEN` the indefinite article stands for the rest of the
book, and the chapter says so.
*Introduces.* `PR-419`–`PR-426`; `PF-410`–`PF-412`; `OB-419`–`OB-425`.
*Errors.* Existential-import mistakes; definite description before its uniqueness
lemma; illicit totalization.
*Rubric.* `EXI`, `SCO`, `DIA`.
*Exit.* Reader finds every unlicensed definite description in a supplied draft
passage (`EX-32.05`).

**Chapter 33 — Immateriality and intellect: two bridges, unequal in strength.**
*Purpose.* Two separate demonstrations with two separate audits, and the book's
principal exercise in honest stopping. The judgement that the immateriality
bridge is stronger than the intellect bridge is stated as a judgement with
reasons, and the weaker result is left at `V-OPEN` or `V-PARTIAL`, not asserted.
*Introduces.* `PR-427`–`PR-440`; `PF-413`–`PF-417`; `OB-426`–`OB-440`.
*Errors.* Analogy read as univocity ("intellect", "knows"); modal strengthening;
overstrong conclusion.
*Rubric.* `SEM`, `EXP`, `SCO`, `DEM`, `FRM`; verdict rules 4 and 5.
*Exit.* Reader writes the `not-established` field for the intellect demonstration
and states what a completed bridge would have to supply (`EX-33.10`).

**Chapter 34 — Goodness and power.**
*Purpose.* Demonstrates what can be demonstrated of goodness and power and marks
what cannot. The transcendental convertibility premise is carried as `W-POST`
with `framework: AT` and audited as such; "omnipotence" in any maximal sense is
listed in `not-established` unless a bridge is exhibited that survives audit.
*Introduces.* `PR-441`–`PR-454`; `PF-418`–`PF-422`; `OB-441`–`OB-454`.
*Errors.* Equivocation on "good"; empirical regularity promoted to necessity;
modal collapse; overstrong conclusion.
*Rubric.* `SEM`, `FRM`, `MOD`, `SCO`, `DIA`.
*Exit.* From the printed dossier the reader sorts attributes into established,
conditional on a `W-POST` premise, and open (`EX-34.07`).

**Chapter 35 — The identification question.**
*Purpose.* States, and does not answer by demonstration, whether the terminus is
the God of any revealed religion. It separates three claims: (i) the attributes
demonstrated of the terminus, by dossier id; (ii) the descriptions a given
tradition predicates of God, cited as theological data; (iii) that (i) and (ii)
are co-referential. Only (i) is demonstrated; (ii) is `W-REV` and never a premise
in a `DEMONSTRATION`; (iii) is neither demonstrated nor refuted here, and the
chapter names precisely what a demonstration of (iii) would require and why this
book does not supply it.
*Introduces.* `PR-455`–`PR-462`, each with explicit `warrant` and `framework`,
none with `kind: PROPOSITION` and `warrant: W-REV`; `PF-423/S`, a specimen in
which
a `W-REV` premise is disguised as natural reason.
*Errors.* Revealed premise presented as a conclusion of natural reason; authority
citation in a warrant slot; equivocation between a tradition-specific and a
demonstrated sense of a divine name.
*Rubric.* `PRV`, `FRM`, `SEM`, `SCO`; `LC-09`.
*Exit.* Reader classifies ten supplied sentences into the six source-policy
categories with at most one error (`EX-35.10`).

---

### 8.11 Chapter 36 — Working unaided, and the closing apparatus

**Scaffold-removal schedule (binding).** Audit-table scaffolding by stage is
fixed by §6.8 and is neither restated nor varied here. In addition: in Stage F at
least one chapter prints a demonstration with `not-established` and `denial-set`
withheld. Chapter 36 prints no scaffolds at all.

*Purpose.* Removes the book. The reader is given (1) an unseen argument in
`L1-PROSE` only, with no ledger and no lexicon, and must produce the full
`PF-###` record, all three layers, the fourteen-row audit, the verdict, a repair
if any, and a `survives` sentence; (2) a construction task — supply a bridge for
one attribute the book left `V-OPEN`, with bridge table and an honest verdict on
the reader's own work, concluding that no bridge is available being a permitted
answer; (3) a hygiene task — run the eleven spine checks `LC-01`–`LC-11`
(§10.5) by hand over a fragment holding three planted defects of different
classes; (4) a project brief — take an argument of the reader's own choosing to a
complete audited proof object.
*Introduces.* No ids. Consuming without minting is the point.
*Errors.* Reader's choice; the solutions enumerate the class of each planted
defect.
*Rubric.* All fourteen axes unprompted, plus the eleven spine checks
`LC-01`–`LC-11` (§10.5); `LC-12`–`LC-22` are tool-run under `UA-10`.
*Exit.* The reader's proof object for task (4) satisfies MD1–MD10 with non-empty,
non-trivial `not-established` and `denial-set`. The solutions supply a reviewer's
checklist, not an answer.

**Closing apparatus (required).**

| Item | Content |
|---|---|
| A. Ledger appendix | Every `ACTIVE` record, all spine keys, sorted by id, `consumed-by` populated |
| B. Blank audit form | One reproducible page: fourteen axes in §6.2 order, mark column, verdict box, `errors`/`repair`/`survives` lines |
| C. Error index | Every `ER-###` under the single axis it violates |
| D. Bridge index | Every `BR-###` used, with the chapter discharging its antecedent |
| E. The dossier | Final state, each line with `PR-###` and `audit-verdict` |
| F. What this book did not establish | Every `not-established` entry from Stages E and F, reprinted verbatim with its source id; and every conditional, hypothetical, or framework-relative Stage F result that F4(b) excludes from the terminus dossier, printed with its chapter and its `PR-4##` |

Item F is the book's final instrument: a reader who can state exactly what was
not shown has learned the discipline the book teaches.


## 9. The Exercise System

Exercises are the only place where the reader operates the machinery. An
exercise set completable by reading is a production defect and blocks the
chapter (§9.6). Rules here are cited by decimal address (`§9.6.3`); §10.1 stays
closed. Exercises are `EX-##.##`, solutions `SO-##.##` with the same number.

### 9.1 The exercise record

Every item carries this header, printed above the item body in the exercise
block. Field names are binding.

| Field | Content |
|---|---|
| `id` | `EX-##.##`, chapter.item |
| `tier` | one tier token (§9.4) |
| `verb` | exactly one primary verb (§9.2); `verb-secondary` optional, at most one |
| `target` | the `PF-###`, `PR-###`, `OB-###`, `TM-###.n`, `DF-###`, or `DS-###` operated on; or `INLINE` when the specimen is printed inside the item |
| `axes` | the §6.2 axis tokens the item drills, most drilled first; or `BLIND` (§9.1.2) |
| `product` | what the reader hands in, named in §4.2 field names and §10.1 id classes |

**9.1.1 Reference rule.** Every item cites a `PF-###`/`PR-###` in `target` or an
axis token in `axes`. From `T2-LOCALIZATION` up, `product` is stated in §4.2
field names — "the corrected `established` and `not-established`", "a `BR-###`
with its antecedent discharged" — never "explain" or "discuss". A `product` that
cannot be diffed against a supplied answer invalidates the item.

**9.1.2 Blinding.** Naming the axis gives away a localization item. `axes: BLIND`
is permitted only when `target` names an id (keeping 9.1.1 satisfied); the axis
list then lives in `SO-##.##`. Forbidden at `T1-RECOGNITION`.

**9.1.3 Forward-reference ban.** An item may use only ids, tokens, and machinery
introduced at or before its own chapter. This is `LC-01` applied to exercises.
*Reviewer's procedure:* grep every `target` and every id named in the solution
against §8.2's allocation table for the citing chapter's stage; an id outside
that stage's range, or in a later chapter's run, rejects the item.

**9.1.4 Taxonomy binding.** Any item or solution asserting a defect names the
`ER-###` and the single §6.2 axis that class violates. That axis MUST appear in
the item's `axes` list (or, under `BLIND`, in the solution's); a mismatch is a
mechanical check failure, not a judgement call.

**9.1.5 Specimens inside exercises; the sense of "demonstration".** Overriding
the specimen-marking requirements of §12.5: a specimen printed inside an
`EX-##.##` block — `target: INLINE`, or a proof object reprinted with the item —
prints in the `SPECIMEN` environment with all four marking channels intact, but
(a) its header suppresses the `ER-###` list and reads `DEFECTIVE — EX-##.##
specimen`, and (b) it prints **no closing verdict line**; verdict token and
`ER-###` list move verbatim into `SO-##.##`. An exercise block printing an
`ER-###` id, a `V-*` token, an audit mark, a locus triple, or a `FIX-*` token
anywhere in the item is rejected: the reviewer greps the exercise file for
exactly the strings `AC-P15a`'s detector names, and any hit outside a `product`
description rejects the item. This section states no string list of its own.

In a stem, a `product`, or a solution, **"demonstration" carries only the §2.1
sense**. An item whose graded product is a populated record that reaches no rung
MUST name its product "a complete `PF-###`" and MUST NOT use the word.

### 9.2 The verb vocabulary (closed: thirteen)

| Verb | Required product | Wrong when |
|---|---|---|
| CLASSIFY | given a statement or proof object and one named closed family (`defensible / false / ambiguous / insufficiently-specified`, or `NEC-*`, `PRI-*`, `DK-*`, `PRD-*`, `SCP-*`, `RG-*`, `W-*`, `V-*`): the token, the §3.9 deciding test applied in one sentence, and the rival token tested and rejected | the token is right but no deciding test is applied; the test cited is not the one §3.9 assigns; **the specimen carries no printed feature that positively supports the rival token, or `SO-##.##` cannot name the feature a competent wrong answerer would have relied on** |
| LOCATE THE FAILURE | the exact `PF-###.k` line or §4.2 field, one axis token marked `FAIL`, the `ER-###`, one sentence of why | the defect is described but not located to a line or field; several axes are named without showing each fails independently |
| FIND THE HIDDEN PREMISE | the suppressed proposition as a full premise subrecord (§4.3), the step it repairs, and whether it is `contested` | the supplied premise is entailed by the printed premises (redundant, not hidden), or it entails `claim` on its own |
| MINIMIZE | the reduced premise set, each deletion justified by "no step consumes it"; which survivor carries `import: REAL`; the resulting `denial-set` | a load-bearing premise is deleted; a deletion is justified by the premise being doubtful rather than unused |
| QUALIFY | the proposition rewritten with a printed `QUA-SEC` respect, a narrowed `domain`, or a weaker `NEC-*`/`SCP-*` token, plus what the qualified form no longer licenses | the qualification makes the proposition analytic (`W-DEF`), or leaves it too vague for any deciding test |
| WEAKEN THE CONCLUSION | rewritten `established` at exactly the licensed strength, plus a new `not-established` entry naming the abandoned claim | the weakened claim is still unlicensed; `not-established` is unchanged |
| PROVIDE THE MISSING BRIDGE | a `BR-###` stub: antecedent, consequent, its own §2.1.2 warrant token, and where in the argument the antecedent is discharged | the bridge is dressed as a definition, or carries `W-DEF` while adding substantive content (`LC-08`) |
| FORMALIZE | `L3-SKEL` from `L2-NUM` in the declared `logic`, every modal line carrying its `SCP-*` token, plus the `fidelity` sentence | a `PRD-ANA` term becomes one predicate letter with no `RISK` callout and no `not-established` entry; `fidelity` omitted |
| DE-FORMALIZE | prose back-translation of `L3-SKEL`, the `FID` mark, and whether the author would assert the back-translated claim | the back-translation restores content the symbols do not carry |
| REFUTE | an `OB-###` at maximum strength: target id, exact denial, a named standing position holding it, and that position's own reason as its literature gives it | the objection attacks a claim the argument does not make; the named position is given a reason weaker than its strongest (MD9, `DIA` = `FAIL`) |
| DEFEND | given a bare claim, a complete `PF-###` with every `MUST` and `MUST-C` field of §4.2 populated, whose fourteen-axis audit carries no `FAIL`, whose achieved rung is `RG-THAT` or higher, and whose `import` is `REAL` or `MIXED`; given a proof plus an `OB-###`, an `RP-###` leaving `claim` byte-identical that rebuts, distinguishes, or concedes with a restated `established` | `claim` is silently reworded; the reply answers a weaker objection than the one given; **the object is formally complete but computes `V-VALID-ONLY`, or its `import` is `CONCEPTUAL` or `LINGUISTIC` — a filled record is not thereby a demonstration** |
| REPAIR | the minimal edit with changed fields printed in full, the resulting verdict, and `survives`; **or** the exhibited failure of repair, with `why-no-repair` and `survives` (§9.8) | the repair adds a premise entailing `claim`; a smaller edit suffices |
| AUDIT | all fourteen §6.2 axes in rubric order marked `OK`/`FLAG`/`FAIL`/`N/A`, one verdict by §6.3's first-match rule, and that verdict's required extra fields | fewer than fourteen rows; a chosen rather than computed verdict; `N/A` outside `EXP` at `RG-THAT` and `FID` without `L3-SKEL` |

**Additions to the brief's eleven.** `CLASSIFY`, because a token-assignment
drill routed through AUDIT would make the whole rubric a prerequisite for a
five-second exercise; `MINIMIZE`, because stripping unused premises and naming
the premise carrying the real burden is one operation on `denial-set`. No
further verb: "compare two rival formalizations" is DE-FORMALIZE twice on `FID`,
"construct an objection" is REFUTE.

### 9.3 Exercise types

| # | Type | Verb | Axes drilled | Floor tier |
|---|---|---|---|---|
| 1 | classify a statement defensible / false / ambiguous / insufficiently-specified | CLASSIFY | `SEM`, `SCO` | T1 |
| 2 | identify which term changes meaning between two lines | LOCATE THE FAILURE | `SEM` | T1 |
| 3 | locate an invalid inference | LOCATE THE FAILURE | `LOG` | T1 |
| 4 | decide whether an argument is valid but unsound | CLASSIFY (`RG-VALID` vs `RG-SOUND`) | `LOG`, `WAR` | T2 |
| 5 | decide `PRI-TMP` vs `PRI-CAU` vs `PRI-ONT` vs `PRI-GND` | CLASSIFY | `DEP` | T2 |
| 6 | identify a hidden modal shift | LOCATE THE FAILURE + CLASSIFY | `MOD` | T2 |
| 7 | find the hidden premise | FIND THE HIDDEN PREMISE | `WAR`, `EXI` | T2 |
| 8 | strip unnecessary premises | MINIMIZE | `DEP`, `DIA` | T2 |
| 9 | determine which premise carries the real metaphysical burden | MINIMIZE | `DIA`, `ONT` | T2 |
| 10 | formalize a numbered argument | FORMALIZE | `LOG`, `FID` | T2 |
| 11 | repair a false universal proposition | QUALIFY | `SCO`, `MOD`, `EXI` | T3 |
| 12 | supply the missing bridge proposition | PROVIDE THE MISSING BRIDGE | `MOD`, `DEP` | T3 |
| 13 | weaken an overstrong conclusion | WEAKEN THE CONCLUSION | `SCO` | T3 |
| 14 | construct an objection at full strength | REFUTE | `DIA`, `FRM` | T3 |
| 15 | answer an objection without changing the claim | DEFEND (reply) | `DIA`, `SCO` | T3 |
| 16 | compare two rival formalizations | DE-FORMALIZE ×2 | `FID`, `SEM` | T3 |
| 17 | full fourteen-axis audit of a supplied specimen | AUDIT | all | T3 |
| 18 | reclassify claimed versus achieved rung | AUDIT (`DEM` focus) | `DEM`, `EXP` | T3 |
| 19 | repair a defective demonstration, or show it irreparable | REPAIR | varies; declared in `SO` | T4 |
| 20 | produce a complete demonstration under §4.2 reaching `RG-THAT` or higher | DEFEND (construct) | all | T4 |
| 21 | place a proposition in the ledger: `depends-on`, `consumed-by`, the `LC-##` catching its misuse | AUDIT + CLASSIFY | `DEP`, `SCO` | T5 |
| 22 | show that an attribute bridge is *not* licensed by the prior result | REFUTE + WEAKEN THE CONCLUSION | `SCO`, `DEP`, `DEM` | T5 |
| 23 | the complete mandatory callout set for a supplied `L2-NUM` object: every §11.3 MUST-trigger fired on the correct line, each note's required content and citation duty met inside the word budget | AUDIT | `SEM`, `DEP`, `SCO` | T3 |
| 24 | the grounding middle and stripped variant that would lift a supplied `RG-THAT` demonstration to `RG-WHY`, or a showing that no grounding middle is available, with the `RG-THAT` stopping case that applies (§2.4) | DEFEND | `EXP`, `DEM`, `DEP` | T4 |

At least one type-23 item appears in every stage from Stage C onward; at least
one type-24 item in each of Stages E and F.

A chapter MAY invent an item that fits no row only by declaring its verb, axes,
and product under §9.1; it MAY NOT invent a verb.

**9.3.1 Axis coverage.** Each of the fourteen §6.2 axes is the **primary drilled
axis** — first token in `axes` — of ≥ 3 items across the book and of ≥ 1 item in
every stage from Stage C onward. An axis appearing merely as one row of a
completed audit table counts toward neither floor. `PRV` requires ≥ 2 dedicated
items: one specimen carrying a `W-AUTH` premise dressed as `W-SELF`, one
carrying a `W-REV` premise inside a proof object, both graded on the reader
producing the corrected warrant token and the resulting verdict. *Reviewer's
procedure:* tally the fourteen rows from the `axes` fields, reading the
solution's list for `BLIND` items; any row below floor rejects.

### 9.4 Difficulty tiers

| Tier | Reader operation | Graded product |
|---|---|---|
| `T1-RECOGNITION` | assign a token from a closed family, or point at a line | one token or line number, plus the deciding test in one sentence |
| `T2-LOCALIZATION` | localize and name a defect, or supply one missing component | a complete localization triple — the locus form ⟨field · id or line · offending token⟩, the axis mark, the `ER-###`, and one sentence of why, all four supplied by the reader; or one premise subrecord |
| `T3-INTERVENTION` | modify an existing argument | rewritten §4.2 fields, or a new `OB-###`, `RP-###`, or `BR-###` |
| `T4-CONSTRUCTION` | produce a whole proof object, or a full audit plus repair | a complete `PF-###`, or fourteen axis rows plus verdict plus repair |
| `T5-ARCHITECTURE` | operate across two or more proof objects and the ledger | a dependency subgraph, its edge list, and the governing `LC-##` |

### 9.5 Composition and stage binding

Per chapter: **10 ≤ items ≤ 24**.

1. `T1-RECOGNITION` ≥ 1 and ≤ 30% of items in any chapter whose stage admits
   T1; exactly 0 in any chapter whose stage does not.
2. `T2-LOCALIZATION` ≥ 20% of items in any chapter whose stage admits T2; where
   the stage does not admit T2, that floor transfers to `T3-INTERVENTION`.
3. T3 + T4 + T5 ≥ 40% of items, and ≥ 4 items absolutely.
4. **Construction minimum:** ≥ 2 items (Stages A–B) or ≥ 3 (Stages C–F) whose
   graded product is a new or modified proof object or component, of which ≥ 1
   is `T4-CONSTRUCTION` from Stage B onward. See §9.6.5.
5. **Functional families**, the acceptance term used elsewhere in this
   specification. *Diagnose* = CLASSIFY, LOCATE THE FAILURE, AUDIT,
   DE-FORMALIZE. *Adjust* = QUALIFY, WEAKEN THE CONCLUSION, MINIMIZE, REPAIR,
   PROVIDE THE MISSING BRIDGE, FIND THE HIDDEN PREMISE. *Construct* = DEFEND,
   REFUTE, FORMALIZE. Every chapter carries ≥ 1 item from each family, and ≥ 2
   from *construct* from Stage C onward; no primary verb carries more than 40%
   of a chapter's items.

| Stage | Tiers admitted | Additional requirement |
|---|---|---|
| A — proof grammar | T1–T3 (T4 permitted) | ≥ 2 items at T3; T5 forbidden |
| B — meaning and distinction | T1–T4 | ≥ 1 T4; ≥ 2 CLASSIFY items over `DK-*`/`PRD-*`/`QUA-*` |
| C — first metaphysical demonstrations | T1–T5 | ≥ 1 T4 producing a `PF-###` with every MUST field |
| D — adversarial | T2–T5, T1 ≤ 10% | ≥ 2 `IRREPARABLE` items (§9.8); ≥ 1 T4 REPAIR |
| E — dependency chains | T2–T5 | ≥ 1 T5; ≥ 1 item that must detect a forward reference |
| F — attribute bridges | T3–T5 | ≥ 2 T5, of which ≥ 1 is type 22 |

Where a numbered rule above and this stage table conflict, the stage table
governs.

**9.5.1 Ceiling rule.** No chapter introduces a tier more than one above the
highest used in the preceding chapter. Tiers, once introduced, stay admissible.

### 9.6 The anti-rote rule

An item violating any of 9.6.1–9.6.7 is rejected. Rejection is mechanical: the
reviewer performs the stated procedure and records the result.


**9.6.1 Restatement test.** Search the whole book as it stands at that point —
the chapter body, every earlier chapter, the glossary, the class register, the
back-matter reference card, every printed audit table, every margin callout,
every figure and table cell — for the item's answer. If any contiguous span of
≤ 3 sentences, **or any single table row, callout, locus triple, or environment
header**, quoted with names, ids, and line numbers substituted, would be scored
correct, the item is invalid. This voids "state the definition of", "which axis
detects", "list the fourteen".

**9.6.2 Production floor.** At `T2-LOCALIZATION` and above the reader must
produce or modify at least one of: a proposition, a premise subrecord, an
inference step, an `OB-###`, an `RP-###`, a `BR-###`, a rewritten `established`
or `not-established`, a completed set of fourteen axis rows, or a **complete
localization triple** — the locus form ⟨field · id or line · offending token⟩,
the axis mark, the `ER-###`, and one sentence of why, all four supplied by the
reader. A response of tokens without the locus triple and the why-sentence is
`T1-RECOGNITION` and may not be labelled higher, however many tokens it
contains.

**9.6.3 Novel-material rule.** At `T3-INTERVENTION` and above the target must be
material not printed in the chapter body: a fresh specimen, an argument from an
opponent's literature, or a **perturbed variant** of a worked example. A
perturbed variant is admissible only when the perturbation is printed and is
**answer-changing**: at least one graded component of the correct response — the
failing axis, the `ER-###`, the verdict token, the repair kind, the surviving
conclusion, or the answer mode — differs from the worked example's, and
`SO-##.##` states in one sentence which changed and why. A perturbation confined
to names, line order, premise numbering, or any token no step consumes is not
answer-changing, and the item is invalid at T3+. *Reviewer's procedure:* set the
body's printed answer beside the solution and diff the graded components; an
empty diff rejects the item.

**9.6.4 Shortest-answer diff.** The reviewer writes the shortest response that
would score correct. If it contains no new proposition, no token assignment
requiring a §3.9 deciding test, and no modified §4.2 field, the item is rote.
Reject.

**9.6.5 Ship gate.** A chapter whose exercise set fails §9.5 rule 4 **MUST NOT
ship**: production returns it unbuilt. A chapter in which more than one
third of the items are answerable by a single token, or by tokens alone with no
locus, no produced artifact, and no deciding test written out, fails likewise,
whatever its tier labels say. *Reviewer's procedure:* take §9.6.4's shortest
scoring response for each item and tally those containing no sentence.

**9.6.6 Verb honesty.** The printed verb must match the expected product. An item
labelled REPAIR whose answer is "this inference is invalid" is mislabelled LOCATE
THE FAILURE; one labelled AUDIT whose answer is fewer than fourteen rows is
mislabelled.

**9.6.7 Specimen freshness.** No `EX-##.##` takes as `target` any proof object,
proposition, or objection whose five-part error block (§7.3), locus triple,
completed audit table, or verdict line is printed anywhere in the book. Exercise
specimens are freshly minted ids whose five-part block appears only in the
matching `SO-##.##`; the ids are allocated by the chapter-authoring lane on
request through the amendment route of §1.5(3), never by the exercise or
solution (§9.7.3). *Reviewer's procedure:* grep the accepted book text and the
class register for each item's `target`; any printed diagnosis of it rejects the
item.

### 9.7 Solution policy

All solutions are collected in one back-matter part, ordered by id. Chapters
print exercises only; no answer, hint, or partial answer appears in one.

| Tier | Solution form |
|---|---|
| T1 | the token plus one sentence of deciding test; ≤ 3 sentences total |
| T2 | line or field, axis mark, `ER-###`, one paragraph |
| T3 | the modified artifact printed in full, plus what changed and why |
| T4 | a complete proof object with all `MUST` and `MUST-C` fields, headed by its `SO-##.##` id (§9.7.3), or a fourteen-row audit table, plus verdict and its required extra fields |
| T5 | the dependency subgraph, its edge list, and the governing `LC-##` |

**9.7.1 Rubric echo (mandatory, T2 and above).** Every such solution ends with a
line of the form

```text
audit-delta: MOD FAIL -> OK; SCO FLAG -> OK    verdict: V-REPAIR -> V-PASS at RG-THAT
```

naming every axis whose mark changes and the verdict before and after. `V-PASS`
is always printed with the achieved rung after it; a bare `V-PASS`, or a missing
`audit-delta` line, is incomplete and blocks the chapter.

**9.7.2 Answer mode.** Every solution declares exactly one of `SETTLED`,
`PLURAL`, `IRREPARABLE`. The mode is solution-side and is **never** printed in
the exercise; printing it reveals the answer.

- `SETTLED` — one correct answer. The solution names the nearest wrong answer and
  the deciding test it fails.
- `PLURAL` — the question genuinely admits rivals. The solution MUST print, in
  order: (a) the reference answer, marked `PLURAL`; (b) an **acceptance-test**,
  a checkable statement of the conditions any rival must meet, written so a
  reader grades an answer the author never saw; (c) one worked rival that passes
  it; (d) one plausible response that fails it, with the clause it fails. A
  `PLURAL` solution lacking (b) and (d) is incomplete: "answers may vary" is not
  a solution.
- `IRREPARABLE` — §9.8.

**9.7.3 Solutions mint no identifiers.** No `EX-##.##` or `SO-##.##` ever
allocates a `PF-###`, `PR-###`, `TM-###`, `DF-###`, `DS-###`, `OB-###`,
`RP-###`, `ER-###`, or `BR-###`. A solution that must print a complete proof
object heads it with its own solution id and addresses its parts by that id —
`SO-14.09` for the object, `SO-14.09.p1` for a premise, `SO-14.09.3` for a step —
using the dotted-suffix syntax of §4.1. Such an object is not a ledger record,
appears in no register, and may not be cited as establishing anything. The
`product` phrase "a complete `PF-###`" names the shape of what the reader hands
in, not an allocation.

**9.7.4 Prohibitions.** A solution may not cite a canonical author in a warrant
slot (`PRV` = `FAIL`); may not depend on material later than its exercise's
chapter (§9.1.3); and may not reword an exercise's `claim`.

### 9.8 Exercises that cannot be repaired

**9.8.1 Uniform phrasing.** *Every* REPAIR item is phrased identically: "Repair
`PF-###`, or show, by exhibiting one weakening of `established` and one added
premise, that no repair preserves a `REAL` conclusion, and state what survives."
No item hints which it is; "if it can be repaired" is a tell and is rejected.
This wording is licensed and is not varied. The specimen printed with a REPAIR
item carries no verdict token, since `V-REPAIR` versus `V-FATAL` is the answer
(§9.1.5). "Demonstration" and "demonstrate" appear in no exercise stem except in
naming an object with `kind: DEMONSTRATION`.

**9.8.2 The `IRREPARABLE` answer.** The solution supplies verdict `V-FATAL` with
`why-no-repair` and `survives`, and states which case holds: `survives: NONE`,
or a `CONCEPTUAL`/`LINGUISTIC` residue recorded as `V-VALID-ONLY` on the
residual argument. Irreparability asserted without the two failed attempts the
stem demands is incomplete, since §6.3 rule 2 prefers `V-REPAIR` whenever a
repair exists.

**9.8.3 Quota, two-sided.** Across the book, `IRREPARABLE` solutions are ≥ 20%
and ≤ 40% of all REPAIR-verb items. Every Stage D chapter carries ≥ 2; every
Stage C, E, and F chapter carries ≥ 1. Neither lesson — every proof salvageable,
or metaphysical argument futile — may be taught by the distribution.

**9.8.4 False negatives are graded too.** For a repairable item, the
acceptance-test states the repair a reader answering "irreparable" missed, so the
wrong answer is diagnosable rather than merely marked.

### 9.9 Worked micro-examples

Each is sited in a chapter whose stage owns every id and token it uses.

```text
EX-04.07  tier: T2-LOCALIZATION  verb: LOCATE THE FAILURE   [Chapter 4, Stage A]
target: PF-031/S  axes: BLIND
product: the PF-031/S.k line, one axis token with its mark, the ER-###, one sentence.

SO-04.07  answer-mode: SETTLED
Line PF-031/S.3. MOD = FAIL, ER-302. Premise p1 carries NEC-CON with SCP-CMP;
line 3 asserts the conclusion under SCP-DIV, and BR-004 (which would license the
shift) is not cited and its antecedent is undischarged. Nearest wrong answer:
"LOG = FAIL" - the shape is valid on the composite reading, so the defect is
modal scope, not consequence.
audit-delta: MOD FAIL -> OK   verdict: V-REPAIR -> V-VALID-ONLY at RG-VALID
(line 3 weakened to ACT; import is CONCEPTUAL throughout Stage A, so V-PASS is
unavailable and conceptual-result is the required extra field)
```

```text
EX-12.11  tier: T3-INTERVENTION  verb: QUALIFY   [Chapter 12, Stage B]
target: PR-074 ("Whatever begins to exist has a cause.")  axes: SCO, EXI, WAR
product: the rewritten proposition with its QUA-SEC respect or narrowed domain,
its NEC-* token, and what the qualified form no longer licenses.

SO-12.11  answer-mode: PLURAL
Acceptance-test. A rival passes iff (i) its deciding test for the recorded NEC-*
token is stated and survives one counter-instance the reader supplies; (ii) it
still licenses PF-112.4, which consumes it; (iii) it does not entail the claim of
PF-112 by itself - a qualification that does has become ER-106, premise concealed
in a definition (axis WAR), not a repair.
Reference answer, one passing rival, and one failing response follow.
audit-delta: SCO FAIL -> OK; EXI FLAG -> OK   verdict: V-REPAIR -> V-PARTIAL
```

### 9.10 Decisions taken where the spine is silent

Tier tokens (`T1-RECOGNITION` … `T5-ARCHITECTURE`), the answer-mode tokens
(`SETTLED`, `PLURAL`, `IRREPARABLE`), the exercise-record field names, the
`audit-delta` format, the three functional families (§9.5 rule 5), and the two
added verbs (`CLASSIFY`, `MINIMIZE`) are decided here. No new identifier prefix
is introduced; §10.1 remains closed and every cross-reference is by existing id.


## 10. The Proposition and Dependency Ledger

The ledger is a single source file holding one record per `TM-###`, `DF-###`,
`DS-###`, and `PR-###`. It is normative, not documentary: the book draws
proposition text, headers, and cross-references *from* it, and no author retypes
a proposition into prose — the production lane pulls the string by id.

### 10.1 Identifier allocation

The prefix set and semantics are fixed by §4.1 and are not restated here.
Allocation rules:

1. **Width.** Three digits, zero-padded, `001`–`999` per class, so ASCII sort
   equals order of introduction within a band (clause 2). A class approaching
   `999` is an architectural failure requiring review, not a widened field.
2. **Bands and serialization.** Bands are reserved per stage and per chapter by
   §8.2 and §8.7, per vertical slice by §15.3, and per specification appendix by
   §8.2 and §7.4, and those reservations bind. Within its own band an author allocates
   strictly ascending at the moment a record is committed. A band may close
   leaving gaps, never backfilled by a later stage. No author allocates outside
   the band of the unit being written; a duplicate allocation is a hard error
   (`LC-22`).
3. **Drafting placeholders.** Prose in progress may cite `<PREFIX>-TBD-<slug>`
   for any id class — `PR-TBD-<slug>`, `DF-TBD-<slug>`, `TM-TBD-<slug>` — none of
   which is an identifier (each fails `^[A-Z]{2}-[0-9]`); `LC-16` rejects any
   placeholder surviving into a reviewed draft.
4. **No reuse, no renumbering.** Once a record has appeared in any pushed draft,
   its id is permanently bound to its `statement`. Withdrawal sets `status:
   RETIRED`, replacement sets `SUPERSEDED` and `superseded-by`; neither frees
   the number, and renumbering to close gaps is prohibited outright.
5. **Status is not a prefix.** A lemma promoted to a theorem keeps its `PR-###`
   and changes `kind`; printed cross-references never go stale.

### 10.2 Record schema

The key list is closed: exactly the keys below, of which `relations` is the one
added key, declared in §10.3. Two spine key *values* are widened here, and the
widening is declared rather than silent: `introduced-at` takes
chapter.section.seq rather than chapter.section, and each `strength-history`
entry carries a fourth element, `asserted-import`. `LC-01`, `LC-05`, and `LC-22`
depend on both. Requiredness codes: **M** every record · **M-P**
propositional kinds (`PRINCIPLE`, `LEMMA`, `PROPOSITION`, `COROLLARY`,
`DISPUTED-PREMISE`, `FRAMEWORK-POSIT`, `HYPOTHESIS`), `N/A` on `TERM` and
`DEFINITION`, and `N/A` on `DISTINCTION` except where a row requires it ·
**C** conditional, condition stated · **D** derived, written by tooling, never
hand-edited · **O** optional.

| Key | Type | Req | Validation rule |
|---|---|---|---|
| `id` | id string | M | matches its class pattern; unique; prefix agrees with `kind` (`TERM`→`TM`, `DEFINITION`→`DF`, `DISTINCTION`→`DS`, all others→`PR`) |
| `kind` | enum (10) | M | one of the ten kinds named above; changing `kind` on an `ACTIVE` record is permitted and logged, except that no record moves into a kind whose `established-by` may be empty (`PRINCIPLE`, `DISPUTED-PREMISE`, `FRAMEWORK-POSIT`, `HYPOTHESIS`) from one whose may not (`LEMMA`, `PROPOSITION`, `COROLLARY`) — that direction requires a new id and a supersession pair. Changing `statement` is never permitted |
| `name` | text, ≤ 6 words | M | unique; no modal or scope word (`necessary`, `every`, `possible`) — the name labels, it does not assert |
| `name-normalized` | text | D | `name` case-folded, articles stripped, whitespace collapsed; unique among `ACTIVE` records (`LC-06`) |
| `statement` | text | M | §10.3. With `established-by` non-empty, byte-identical after whitespace collapse to the `established` field of at least one proof named there; matching only a named proof's `claim` is a hard error (`LC-19`) — the ledger records what was established, never what was claimed. For `kind: TERM`, a numbered sense list, one line `TM-###.n: <sentence>` per sense, each satisfying §10.3 and applicable to cases by a competent adherent of every framework in the rival register (§14.5) without first accepting any proposition of this book. A sense line entailing a non-trivial claim about what exists, about what depends on what, or about what any thing must be is a proposition in a sense line's clothing and MUST be split into a neutral sense line plus a `PR-###` carrying its own warrant, `objections`, and audit (`LC-18`). A `TERM` whose `framework` is not `NEUTRAL` MUST name a standing position construing the term otherwise |
| `status` | `ACTIVE`\|`SUPERSEDED`\|`RETIRED` | M | `SUPERSEDED` iff `superseded-by` non-empty; `RETIRED` requires `consumed-by` empty |
| `rung` | `RG-*` | M-P for `LEMMA`, `PROPOSITION`, `COROLLARY` | the achieved rung of at least one proof in `established-by`, never the claimed rung |
| `import` | `REAL`\|`CONCEPTUAL`\|`LINGUISTIC`\|`MIXED` | M | `REAL` requires a named proof carrying `import: REAL`, or `warrant` ∈ {`W-SELF`, `W-IND`, `W-EMP`, `W-POST`} |
| `modality` | one `NEC-*`/`POS-*`/`ACT`/`CONT`/`IMPOSS` | M-P | matches any modal word in `statement`, or `statement` carries none; a modal word with no matching token is a hard error |
| `modal-scope` | `SCP-CMP`\|`SCP-DIV`\|`N/A` | C: required iff `modality` is `NEC-*`, `POS-*`, or `IMPOSS` | `N/A` only when the record asserts no operator |
| `warrant` | one closed warrant token | M-P, and required on `DISTINCTION` | `W-DEM` requires non-empty `established-by`; `W-HYP` requires `kind: HYPOTHESIS`; `W-REV` or `W-AUTH` on a record of **any** kind is a hard error (`LC-09`) — a datum accepted on revelation is not a record of this ledger at all. On `DISTINCTION` the licensed values are exactly `W-DEM`, citing the `PR-###` that establishes the distinction, and `W-POST`, which then forces `framework ≠ NEUTRAL` by the rule below |
| `framework` | `NEUTRAL`\|`AT`\|named | M | any record with `warrant: W-POST` must not be `NEUTRAL` |
| `introduced-at` | chapter.section.seq | M | all three integers, `seq` the printed order of the record within its section; locations compare as the numeric triple, chapter first, never lexically; strictly earlier than every `consumed-by` location, equality being a forward reference within a section and a hard error (`LC-01`) |
| `established-by` | list of `PF-###` | M-P | may be empty only for `PRINCIPLE`, `DISPUTED-PREMISE`, `FRAMEWORK-POSIT`, `HYPOTHESIS`; plural permitted (rival demonstrations); every `PF-###` named MUST carry an `audit-verdict` in {`V-PASS`, `V-VALID-ONLY`, `V-OPEN`, `V-PARTIAL`}, never `V-REPAIR` or `V-FATAL` — a repaired argument is published as a distinct `PF-###` with its own audit, only that id being nameable (`LC-19`) |
| `depends-on` | id list | M | every entry exists, is `ACTIVE`, and has an `introduced-at` strictly earlier under the triple ordering; may be empty; a bridge is cited by its companion `PR-###` and never as a bare `BR-###` (§10.2a) |
| `consumed-by` | list of `{id, location}` | D | exact inverse of every other record's `depends-on` (`LC-04`) |
| `lexicon` | list of `TM-###.n`, `DF-###`, `DS-###` | M | every technical term in `statement` appears here with a sense selector (`LC-11`) |
| `denial-set` | id list | M-P when `import: REAL` | non-empty; each member load-bearing and naming a standing position that rejects it |
| `objections` | list of `OB-###` | M-P | ≥ 1 when `import: REAL` or `framework ≠ NEUTRAL`; ≥ 1 always for `DISPUTED-PREMISE` and `FRAMEWORK-POSIT` |
| `replies` | list of `RP-###` | M-P | 1:1 with `objections` by number; a reply may concede |
| `audit-axes` | map, 14 axis tokens → `OK`\|`FLAG`\|`FAIL`\|`N/A` | M-P | all fourteen keys present, copied from the `established-by` proof, worst mark per axis across rival proofs |
| `audit-verdict` | `V-*` | M-P | the verdict §6.3's first-match rules compute from `audit-axes`; a hand-entered verdict disagreeing with the computation is a hard error |
| `strength-history` | ordered list `{location, asserted-modality, asserted-scope, asserted-import}` | D | one entry per `consumed-by` entry, same order. The three asserted values are read from the consuming proof's premise subrecord for this record — the `modality`, `modal-scope`, and `import` keys of the `premises` entry whose `source` equals this `id` — or, where the record is consumed with no premise subrecord, from the `to` line of the first `steps` entry citing it, `asserted-import` then being the consuming proof's `import`, a step carrying no import key. No other source is admissible; a hand-written entry is a hard error |
| `terminal` | boolean | M | `true` only where nothing is intended to consume the record; `true` with `consumed-by` non-empty is a warning |
| `supersedes` / `superseded-by` | id or empty | M | exact inverses; at most one each way |
| `relations` | list of `{kind, target}` | C: §10.3 | inverse recorded on the target |

Brief-to-key map, so no later agent invents a synonym: *first point of
introduction* = `introduced-at`; *later propositions that consume it* =
`consumed-by`; *terms whose definitions it depends on* = `lexicon`; *modal
strength* = `modality` + `modal-scope`; *logical / conceptual / empirical / real
necessity* = `NEC-LOG` / `NEC-CON` / `NEC-NOM` / `NEC-MET`, read with `import`;
*proof-audit status* = `audit-axes` + `audit-verdict`.

### 10.2a Bridges in the ledger

Every `BR-###` used anywhere in the book MUST have a companion ledger record
whose `statement` is the bridge as one conditional proposition satisfying S1–S8,
with `kind: PRINCIPLE` where the bridge's warrant is `W-SELF` or `W-DEM` and
`kind: FRAMEWORK-POSIT` where it is `W-POST`. The companion carries `warrant`,
`framework`, `import`, `modality`, `modal-scope`, `established-by`,
`denial-set`, `objections` (≥ 1), `audit-axes`, and `audit-verdict` like any
other propositional record, plus the discharge sites at which the bridge's
antecedent is discharged.

The `BR-###` label is an alias for that `PR-###`, and it is the companion
`PR-###`, never the bare `BR-###`, that appears in any `depends-on`; an entry
matching `^BR-` is itself a hard error (`LC-12`). A companion carrying
`warrant: W-POST` is a framework posit for all purposes of the Framework
Declaration's posit table (§14.1 N1(2)) and counts as a load-bearing `W-POST`
premise for verdict rule 4, `V-OPEN` (§6.3), in every proof whose `depends-on`
closure contains it.

*Worked instance.* `BR-002` (`NEC-NOM` → `NEC-MET`, `W-POST`, §7.7) is aliased
to companion `PR-011`, `kind: FRAMEWORK-POSIT`. A proof consuming the bridge
lists `PR-011` in `depends-on`, prints `BR-002` at the licensing step and in the
bridge index, and cannot reach `V-PASS` while `PR-011` stands at `W-POST`.

### 10.3 The `statement` field, and how a variant claim is handled

`statement` is the strictest field in the project. Rules **S1–S8** are all
hard errors.

- **S1 One sentence.** Exactly one declarative sentence, one terminal period, no
  semicolon, no em-dash aside, no parentheses, no footnote mark, no citation, no
  cross-reference other than `TM-###.n` sense selectors.
- **S2 No hedging.** A closed stop-list is rejected on match: *arguably,
  plausibly, roughly, more or less, in some sense, broadly speaking, presumably,
  apparently, it seems that, one might say, at least in some cases, so to speak,
  basically*. There is no editorial override; a claim that needs a hedge is a
  `DISPUTED-PREMISE` stated flatly, the doubt carried by `warrant`,
  `objections`, and `audit-verdict`.
- **S3 No escape clauses.** A restrictive clause narrowing subject, respect, or
  domain is required wherever it applies and is part of the claim (*"in the
  respect in which it is in act"*). *Detector:* delete the clause; if
  truth-conditions are unchanged it was an escape clause, and it is forbidden.
- **S4 Explicit quantification.** Every subject carries a determiner: *every*,
  *some*, *this*, *no*. A bare plural subject is rejected.
- **S5 Declared modality.** Any modal word in the sentence must correspond to the
  `modality` and `modal-scope` tokens, and the operator's scope must be readable
  from word order alone.
- **S6 Lexical closure.** Every technical term is listed in `lexicon` with a
  sense selector.
- **S7 Verbatim citation.** Wherever the statement appears — body, exercise,
  solution, audit table, register, diagram label — the string is byte-identical
  after whitespace collapse, case unfolded. Authors cite by id; the production
  lane substitutes.
- **S8 Immutability.** Once `ACTIVE`, only whitespace and typographic-quote
  normalization is editable in place; any change of wording, quantifier,
  modality, scope, subject, attribute, or import mints a **new id**.

**The variant mechanism.** A later chapter wanting a different claim — wider
subject, stronger necessity kind, divided rather than composite sense, dropped
qualification — does not edit `PR-014`. It mints `PR-097` and records a
`relations` entry on both:

| Relation on new record | Inverse on old | Meaning |
|---|---|---|
| `STRENGTHENS` | `WEAKENS` | same subject, higher modal force, wider scope, or dropped qualification |
| `RESTRICTS` | `GENERALIZES` | narrower subject or domain |
| `DISAMBIGUATES` | `DISAMBIGUATED-BY` | one sense selector replaced by another |
| `VARIANT-OF` | `VARIANT-OF` | rewording claimed to be equivalent; must state the equivalence argument's id |
| `CONTRARY-TO` | `CONTRARY-TO` | the two cannot both hold |

A `STRENGTHENS` edge is not a licence: `PR-097` carries its own `warrant`,
`established-by`, and `audit-axes`, and where it is reached from `PR-014` by a
modal, scope, or import move, the companion of the licensing bridge appears in
its `depends-on`. The old record stays `ACTIVE` while still consumed, becoming
`SUPERSEDED` only when the earlier claim is withdrawn.

`relations` is the one key added beyond those §10.2 inherits, and no other key
is renamed, dropped, or retyped by any later lane: supersession cannot express
two live claims standing in a strength relation, which is exactly the
configuration silent strengthening produces.

**Modal strength order**, needed by `LC-05` and left undefined by §3.9, decided
here: force ranks `NEC-*` ≻ `ACT` ≻ `CONT` ≻ `POS-*`, `IMPOSS` read as necessity
of the negation; scope ranks `SCP-DIV` ≻ `SCP-CMP`; necessity kinds rank
`NEC-LOG` ≻ `NEC-MET` ≻ `NEC-NOM` ≻ `NEC-HYP`, with `NEC-CON` above `NEC-HYP`
and incomparable to `NEC-MET` and `NEC-NOM`; import ranks `REAL` ≻ `MIXED` ≻
`CONCEPTUAL` ≻ `LINGUISTIC`. Any upward or incomparable move requires a cited
`BR-###`, an upward import move exactly as a modal move does; a downward move
requires none but is still recorded in `strength-history`. Possibility kinds rank
`POS-NOM` ≻ `POS-MET` ≻ `POS-CON` ≻ `POS-LOG`: the narrower the possibility
space, the stronger the claim. An upward move requires a cited `BR-###` —
`BR-001` for `POS-CON` → `POS-MET` — and a downward move requires none, which is
why the `POS-NOM` → `POS-MET` step of §15.2 needs no bridge. These orders govern
`strength-history` comparisons (`LC-05`) and the step-level `bridge` condition of
§4.3 on `modality` and `modal-scope`. The import order is compared across uses of
one record; it is never the comparison between a proof's premises and its
conclusion, where MD5 and §4.4 (5) govern.

### 10.4 Machine-readable sketch

Non-normative where it differs from §10.2; §10.2 governs.

```yaml
id: PR-014
kind: PROPOSITION            # one of the ten kinds
name: Moved by another
name-normalized: moved by another          # derived
statement: "Every thing that is moved TM-003.2 is moved by another."
status: ACTIVE
rung: RG-WHY
import: REAL
modality: NEC-MET
modal-scope: SCP-CMP
warrant: W-DEM
framework: AT
introduced-at: "7.3.2"       # chapter.section.seq; compared as a numeric triple
established-by: [PF-021]
depends-on: [DF-006, DS-004, PR-009, PR-011]   # PR-011 = companion of BR-002
consumed-by:                 # derived; exact inverse of depends-on
  - {id: PR-031, location: "9.1.1"}
lexicon: [TM-003.2, TM-011.1, DF-006, DS-004]
denial-set: [PR-009, DS-004]
objections: [OB-018]
replies: [RP-018]
audit-axes: {SEM: OK, LOG: OK, EXI: OK, WAR: OK, MOD: FLAG, ONT: OK,
             EXP: OK, DEP: OK, SCO: OK, DIA: OK, DEM: OK, FRM: FLAG,
             FID: OK, PRV: OK}
audit-verdict: V-OPEN
strength-history:            # derived; one entry per consumed-by entry
  - {location: "9.1.1", asserted-modality: NEC-MET, asserted-scope: SCP-CMP,
     asserted-import: REAL}
terminal: false
supersedes: null
superseded-by: null
relations:
  - {kind: GENERALIZES, target: PR-097}
```

### 10.5 Checks

`LC-01`–`LC-11` keep the ids and the failures named below and are neither
renumbered nor redefined by any later lane; the table adds severity and the data
each inspects. `LC-12`–`LC-22` are added by this section.

| Id | Failure caught | Data inspected | Severity |
|---|---|---|---|
| `LC-01` | forward reference to an unproved proposition | `depends-on` × target `introduced-at`, `established-by`, `status`; locations compare as numeric triples, ties in chapter.section resolved by `seq` | hard error |
| `LC-02` | dependency cycle, including a warrant presupposing its own conclusion | transitive closure of `depends-on` ∪ warrant edges | hard error |
| `LC-03` | orphan: a proposition proved and never used | `status`, `consumed-by`, `terminal` | warning; sign-off records why it is kept or `terminal: true` |
| `LC-04` | dependency graph internally inconsistent | `depends-on` vs `consumed-by` across all records | hard error (both are derived-consistent) |
| `LC-05` | silent strengthening; a proposition consumed with stronger modal force than it was established with | each `strength-history` entry vs the record's own `modality`, `modal-scope`, and `import`, under §10.3's order, and the citing site's `depends-on` for the companion of a `BR-###` | hard error |
| `LC-06` | two different propositions under one verbal label | `name-normalized` across `ACTIVE` records | hard error |
| `LC-07` | live reference to a withdrawn or replaced record | every id reference × target `status` | hard error |
| `LC-08` | a disputed premise hidden inside a definition, a distinction, or a term | a `DEFINITION`, `DISTINCTION`, or `TERM` record whose `statement` asserts content not derivable from its declared sense plus prior `ACTIVE` ids | hard error. Cleared by one of exactly two ledger edits, never a sign-off: the underivable clause moves into a new `PR-###` carrying its own warrant token, `import`, `objections`, and `denial-set` membership in every consuming proof, the consuming premises' warrant changing from `W-DEF`; or a derivation is recorded in the record as a `steps` list printing the sense line, each prior id consumed, and the rule at each line. Prose asserting that a derivation exists does not clear it |
| `LC-09` | revelation or authority used as warrant for a proposition | `kind` and `warrant` on every ledger record, and the `warrant` of every premise subrecord in every printed `PF-###` | hard error |
| `LC-10` | an explanatory claim with no grounding middle | `rung: RG-WHY` × `established-by` proof's `middle`, `middle-kind`, priority token | hard error |
| `LC-11` | an undeclared or unselected technical term | `statement` tokens × `lexicon` | hard error |
| `LC-12` | a Stage F attribute demonstration consuming a bridge or disputed premise with no warrant record, or citing a bridge by its alias | for every record whose `introduced-at` chapter maps to Stage F, each `depends-on` entry must resolve to a record with non-empty `warrant`, non-empty `objections`, and a present `audit-verdict`; and, at any stage, any `depends-on` entry matching `^BR-`, a bridge being cited by its companion `PR-###` (§10.2a) | hard error |
| `LC-13` | an unnoticed near-variant of an existing claim | pairwise normalized-token similarity of `ACTIVE` `statement`s above threshold, where neither record names the other in `relations` | warning; sign-off records a `relations` edge or asserts independence |
| `LC-14` | a relation asserted in one direction only | each `relations` entry × the inverse table in §10.3, and `supersedes`/`superseded-by` | hard error |
| `LC-15` | a malformed proposition string | `statement` against S1–S7, `S7` checked across every printed occurrence of the string | hard error, sub-coded `LC-15a`–`LC-15g` by rule |
| `LC-16` | an unresolved placeholder or dangling id | every `*-TBD-*` occurrence, and every id reference with no record | hard error |
| `LC-17` | a proposition asserted with no proof and no declared status as unproved | `kind` × `established-by`: `LEMMA`, `PROPOSITION`, `COROLLARY` with `established-by` empty; `DISPUTED-PREMISE`/`FRAMEWORK-POSIT` with it non-empty | hard error |
| `LC-18` | a framework-laden term sense recorded as neutral machinery | each `TM-###.n` sense line, its framework-status classification, `framework`, `objections`. *Detector:* a sense line only a reader already committed to the declared framework would grant, recorded neutral; or one whose adoption makes a premise in a consuming proof analytic where the ordinary sense leaves it disputed | hard error; cleared only by splitting the sense into a neutral sense line plus a `PR-###` with its own warrant and objections |
| `LC-19` | a proposition recorded at its proof's claimed rather than its established strength, or established by a failed proof | `statement` against each named proof's `established`; `established-by` against each named proof's `audit-verdict` | hard error |
| `LC-20` | an undemonstrated real-import proposition laundered as a principle or posit | records with `kind: PRINCIPLE` or `FRAMEWORK-POSIT`, `import: REAL`, and an `introduced-at` chapter in Stage D, E, or F | hard error; the legal responses are to demonstrate in place, to file a stub and take `V-PARTIAL`, or to carry `W-POST` and take `V-OPEN`. Such a record MUST carry ≥ 1 objection and appear in the `denial-set` of every proof consuming it |
| `LC-21` | an id used inside a proof but unlisted | every id in a `PF-###`'s printed `premises`, `steps`, `lexicon`, or dependency line against that proof's `depends-on`, and against the `depends-on` of every record naming that proof in `established-by`, which must be a superset of it | hard error |
| `LC-22` | an id allocated twice, or allocated outside the band its `introduced-at` unit owns | every `id` against every other record's `id`, and against the band §10.1(2) assigns to its unit | hard error |

No check enforcing a house rule may be a warning: `LC-08`, `LC-09`, `LC-10`, and
`LC-18` are hard errors with no sign-off route. `LC-08` compares a definition
with its sense and `LC-18` audits the sense; neither substitutes for the other,
and §3.1's G-R2 — an `AT` entry names a live tradition rejecting or reconstruing
it — binds every `TM-###` record, not only the numbered glossary entries. The
detector for §4.2's *an id used in `steps` but unlisted* is `LC-21`, not
`LC-04`, which compares derived ledger fields and cannot see a proof's printed
lines.

A hard error blocks the build; there is no override flag. A warning blocks the
build until an editorial sign-off record naming the check id, the record id, and
the reason is present in the ledger source; sign-offs are reviewed as content,
not as configuration.

### 10.6 Ledger and printed book

**At point of use.** The environment header carries kind, id, and name ("Lemma
PR-014 · Moved by another"); the dependency bar, `USES` callouts, and diagrams
follow §12.7. `SCOPE`, `MODAL`, and `OBJ` callouts fire wherever the
corresponding axis carries a `FLAG` or `FAIL`. Each chapter opens with a
*propositions in force* strip: id, short name, and one-line modality for every
record it consumes but does not establish.

**In back matter.** A *Register of Propositions*, sorted by id, columns: id,
name, kind, status, `rung`, `modality` + `modal-scope`, `import`, `framework`,
`introduced-at`, page, `audit-verdict`; a reverse index from `consumed-by`; one
dependency diagram per stage. `SUPERSEDED` and `RETIRED` records stay in the
register with their `supersedes`/`superseded-by`/`relations` links printed: a
reader must be able to see that a claim was replaced and by what.

**Source only.** `name-normalized`, `strength-history`, `consumed-by` locations,
`lexicon` (surfacing instead as glossary entries), per-axis `audit-axes` marks
in the ledger copy (the fourteen-row table prints with its `PF-###`, never
twice), and sign-off records.

### 10.7 Not built here

No ledger file, schema, validator, linter, build hook, or diagram generator is
produced in this lane. The production lane implements `LC-01`–`LC-22` against
§10.2 and the orders in §10.3, and owns only the serialization format and the
`LC-13` threshold. It may not weaken a severity, add an override for a hard
error, or alter a key name.


## 11. Margin Annotation Grammar

### 11.1 The closed set and the disposition of the candidates

The callout vocabulary is exactly ten tokens, closed here:

`DEF` · `DIST` · `INF` · `IMPORT` · `MODAL` · `WHY` · `RISK` · `OBJ` · `SCOPE` ·
`USES`

No later agent may add a token, subdivide one, or use one of these spellings for
a second purpose. Seven of the brief's candidates are kept unchanged: `DEF`,
`DIST`, `MODAL`, `WHY`, `RISK`, `OBJ`, `SCOPE`. `DEF` is not merged into `USES`,
since selecting *which sense* of a term is live at a line is what no other token
does; `WHY` is the sole page-level marker of the `EXP` axis and of the
`RG-THAT` / `RG-WHY` boundary. Three are renamed; nothing dropped or merged.

| Candidate | Becomes | Reason |
|---|---|---|
| `LOGIC` | `INF` | The note names the rule applied at one step. `LOGIC` invited general commentary about logic — the commonest way a margin becomes a second textbook. |
| `META` | `IMPORT`, absorbing existential-import flags | `META` licenses stamping anything metaphysical-sounding. `IMPORT` forces the author to name the commitment incurred — what a nominalist or Humean would query — and matches the `import` field and the `ONT`/`EXI` axes. |
| `DEP` | `USES` | `DEP` already names audit axis `DEP`, and one spelling may not carry two meanings. `USES` reads as what the line does: consume a prior id. |

### 11.2 Kinds

Every token belongs to exactly one **kind**, drawn from this fixed four-member
set. The kind, not merely the token, must be recognizable at a glance and in
grayscale.

| Kind | Members | Reader is being told | Marker (shape, never hue) |
|---|---|---|---|
| `K-EXPL` explanation | `DEF`, `DIST`, `INF`, `WHY` | what is happening in the reasoning here | hairline rule, text-side edge; token small caps, regular; no glyph |
| `K-WARN` warning | `MODAL`, `IMPORT`, `RISK`, `SCOPE` | where this argument can go wrong or is easily overread | heavy solid rule; token small caps, bold; glyph `!` |
| `K-DEP` dependency | `USES` | this line is borrowing something already established | dotted rule; token small caps, letterspaced; glyph `→` |
| `K-ACT` reader action | `OBJ` | act here — this is the point you would deny, defend, or attack | double rule; token small caps, regular; glyph `?` |

`OBJ` is the sole `K-ACT` member by design: it alone puts the reader under an
obligation rather than describing the text, and it is the hook the exercise verbs
`REFUTE`, `DEFEND`, and `FIND THE HIDDEN PREMISE` attach to. It is not empty in
practice: `OBJ` fires once per `denial-set` member (§11.3), and `denial-set` is
never empty.

Rule weight, rule pattern, token weight, and glyph are four independent
non-chromatic channels. The mechanism — rule weights, small-caps face, glyph
metrics, margin geometry, placement — is implemented by the production section
(§12.3), whose note-styling condition AC-P09 is amended to permit exactly these
four kind markers and no others: no kind is ever marked by color, and any three
of the four channels surviving degradation identifies the kind.

### 11.3 Triggers, contents, and frequency

Triggers are mechanical conditions on the proof object's fields, so that two
authors annotating the same `PF-###` fire the same tokens on the same lines.
"MUST fire" means omission is a defect detectable by the coverage test (§11.6);
"MAY fire" means the author judges, subject to the density budget.

| Token | Kind | Trigger | Frequency (binding) |
|---|---|---|---|
| `DEF` | `K-EXPL` | MAY fire at a `TM-###`'s first occurrence in this `PF-###`. MUST fire at any line whose sense selector for a term differs from that term's previous occurrence in this `PF-###`. | ≤ 2 per proof object at every stage |
| `DIST` | `K-EXPL` | MUST fire at the first line consuming each `DS-###` listed in `lexicon` — i.e. the first line that would go false or ambiguous if the distinction were collapsed. | 0–2 per proof object |
| `INF` | `K-EXPL` | MUST fire at a `steps` line whose `rule` is a quantifier rule (UI, UG, EI, EG), a modal rule, or a reductio / conditional-proof discharge; or where a near-neighbour rule would yield the same `to` from the same `from` (converse and inverse traps). MUST NOT fire on modus ponens, modus tollens, conjunction, or simplification unless one of those conditions holds. | ≤ 2 per proof object |
| `IMPORT` | `K-WARN` | MUST fire at the first line incurring an ontological or existential commitment — a `commitments` entry with `import: REAL` — capped at three an opponent is likeliest to refuse. | 1–3 per demonstration |
| `MODAL` | `K-WARN` | MUST fire at every line where the necessity kind (`NEC-*`/`POS-*`/`ACT`/`CONT`/`IMPOSS`) or `SCP-*` scope of the running claim differs from the preceding line, and at every line citing a `BR-###`. Never discretionary. | 0–3 per demonstration; exactly one per licensed bridge |
| `WHY` | `K-EXPL` | MUST fire, exactly once, at the step whose `from` includes the premise predicating `middle` of `subject` and whose `to` predicates `attribute`. MUST NOT fire in a `PF-###` with `rung: RG-THAT`. | exactly 1 per `RG-WHY`; 0 otherwise |
| `RISK` | `K-WARN` | MUST fire where a `PRD-ANA` term is rendered as one predicate letter in `L3-SKEL`; where `L1-PROSE` and `L2-NUM` diverge; and beside a symbolized `denial-set` premise the symbolization makes look settled. MAY fire where an ordinary-language sense broader than the selected `TM-###.n` would make the premise more plausible. | 0–2 per demonstration; ≤ 4 in a specimen's audit pass |
| `OBJ` | `K-ACT` | MUST fire at the line stating each member of `denial-set`, one note per member. | = size of `denial-set` |
| `SCOPE` | `K-WARN` | MUST fire, exactly once, at the line stating `established`, and at any surrounding line whose ordinary reading would assert an entry of `not-established`. | 1–2 per proof object |
| `USES` | `K-DEP` | MUST fire at each premise carrying warrant `W-DEM`, and at each line consuming an id listed in `depends-on`; one note per distinct id, not per occurrence. | one per distinct id in `depends-on`, no upper bound; if this exceeds the ceilings, §11.4(7) applies |

**The frequency column binds.** Where it and the density budget of §11.4 differ,
the lower number governs — unless the excess consists solely of MUST-fired notes,
in which case §11.4(7) applies. No frequency here is stated per page; the
per-page cap lives in §11.4(2) alone.

Contents. The word budget is **20 words, one sentence**, counting neither the
leading token, nor bare ids, nor rule names, nor the bracketed audit tag of
§11.7.

| Token | MUST contain | MUST NOT contain | Citation duty |
|---|---|---|---|
| `DEF` | the sense now in force, in the author's words | a new stipulation, a defence of the definition | MUST cite one `TM-###.n` or `DF-###` |
| `DIST` | the two sides, named | an argument that the distinction is real | MUST cite one `DS-###` and print its `DK-*` |
| `INF` | the rule name **and the specific item it is applied to** — which premise, which quantifier, which occurrence of which term; where the trigger is a near-neighbour trap, also the near-neighbour rule that would *not* license this `to` from this `from` | commentary on logic in general, a validity claim about the whole proof | MUST NOT cite record ids in ordinary text; inside a `SPECIMEN`'s audit pass MAY carry exactly one `ER-###` (§11.7); MAY cite step ids `PF-###.k` |
| `IMPORT` | the commitment, named as an entity, kind, or relation | the bare word "metaphysical"; a defence of the commitment | MAY cite one `DK-*` or licensing `PR-###` |
| `MODAL` | both tokens, before and after | a defence of the change; the word "obviously" | MUST cite the `BR-###` when one licenses the change |
| `WHY` | the middle term **and the relatum it grounds**, in the form "`M` grounds *attribute* of *subject*" | a restatement of the conclusion; a second reason | MAY print `PRI-GND`; MUST NOT cite `PF-###` |
| `RISK` | the hazard, named by the word or phrase that carries it | its resolution; reassurance | MAY cite one `ER-###` or `TM-###.n`; sole token permitted to print `W-REV` or `W-AUTH`, and only in a `SPECIMEN` or beside a printed `PRV` row |
| `OBJ` | what is denied, in the opponent's terms | the reply; an evaluation of the objection | MUST cite one `OB-###` |
| `SCOPE` | what is *not* thereby established | a stronger claim asserted as reachable | MAY cite the `PR-###` or `PF-###` whose `not-established` it echoes |
| `USES` | the role the borrowed item plays here | a summary of the borrowed item's content or its proof | MUST cite exactly one id |

At most two ids in any callout. Verdict tokens (`V-*`) and rung tokens (`RG-*`)
never appear in the margin: they are computed properties of the whole object and
belong to the audit table.

### 11.4 Density budget, precedence, and bloat

1. At most **one** callout per numbered line.
2. Hard maximum **5** notes per page; **median 3** across any chapter. A page
   with 6 is a defect however well each note reads.
3. Per proof object: discretionary (MAY-fired) callouts ≤ ⌊n/3⌋, *n* being the
   number of numbered lines (premises plus steps); hard ceiling 12 notes per
   `PF-###`, mandatory ones included.
4. **Precedence** when two triggers fire on one line: a callout required by a
   printed `FLAG` or `FAIL` row outranks all; then `MODAL`, `OBJ`, `WHY`,
   `SCOPE`, `RISK`, `IMPORT`, `USES`, `DIST`, `DEF`, `INF`.
5. **Migration.** A displaced trigger moves to the nearest line on which the same
   item is still in play, and the note prints the id of its trigger line (`p2`,
   `PF-###.k`). A note fired by a **MAY**-trigger MAY be dropped on displacement.
   **A note fired by a MUST-trigger may never be dropped, whatever its kind** —
   this covers `WHY`, `DIST`, the sense-change case of `DEF`, and `INF`'s
   mandatory cases as much as every warning, dependency, and action note. If a
   mandatory note cannot be placed within two lines of its trigger, the page is
   over-annotated and the remedy is clause 7, never suppression.
6. A callout that merely restates its line is a defect, not a redundancy.
7. **Budget conflict.** Where the mandatory notes of §11.3 exceed the per-page
   cap (clause 2) or the per-object ceiling (clause 3), the conflict is a
   spec-level escalation, filed by the production lane against the authoring lane
   under §1.5(3). **The production lane may not resolve it:** it may not relocate
   a note to a footnote, the body, a facing page, or a following page; may not
   merge, shorten, reorder, or drop one; and may not re-anchor one more than two
   lines from its trigger. The authoring lane resolves it, by splitting the proof
   object into two objects with their own ids or by reducing the numbered lines
   that share a page — never by suppressing a mandatory note, and never by
   removing an entry from `commitments`, `depends-on`, or `denial-set` to shed a
   trigger. Until it is resolved the unit is not accepted.

### 11.5 The margin is not a second textbook

**Governing rule.** The margin annotates reasoning that is complete without it.
Concretely, and each clause is separately checkable:

- **No new content.** Every content word in a callout, after striking the token,
  cited ids, rule names, and audit tag, is traceable to the annotated line, to
  the proof object's printed fields, or to the cited record.
- **No argument.** A callout may not contain the connectives *because*,
  *therefore*, *since*, *hence*, *for*, *so*, *it follows*, or *which shows*
  joining two claims. A callout asserts at most one thing about the line.
- **Not load-bearing.** No `steps` line, no `premises` entry, no exercise, and no
  cross-reference may cite a callout. `cleveref` MUST NOT resolve to margin
  material. Callouts are unnumbered.
- **Deletion test (binding).** Delete every callout on the page. If any premise,
  inference, term sense, dependency, or claim is now missing from the argument,
  the spec has been violated and the missing item is moved into the main text: a
  reader who ignores the margins entirely loses no part of any proof.

### 11.6 Reviewer tests

Five procedures, all runnable by a reviewer with the page and the proof object in
hand.

- **Deletion test** — §11.5. Detects load-bearing margins.
- **Overlap test** — strike the token, cited ids, and audit tag from a callout;
  strike rule names too, but only for tokens other than `INF`, whose rule name
  plus applied item *is* its required content (§11.3). If every remaining content
  word appears in the annotated line, the note restates and MUST be deleted.
  `WHY` is exempt: its required content is on the annotated line by construction,
  and it is governed by the transplant test instead. *Restatement, deleted:* line reads
  "Whatever is moved is moved by another"; note reads `IMPORT!` *Whatever is
  moved is moved by something else*. *Admissible:* `IMPORT!` *Quantifies over
  movers as really distinct from the moved* `DK-REAL`.
- **Transplant test (binding)** — move each callout, unchanged, to any other
  numbered line in the same chapter firing the same token. If it remains true and
  apt there, it is generic and MUST be rewritten. A callout survives only if the
  transplant makes it false, inapplicable, or mis-cited — only, that is, if it
  names something proper to its own line: a specific term sense with its English
  gloss; a named standing position and the claim it asserts instead; a named
  entity, kind, or relation drawn verbatim from `commitments`; a named
  non-consequence drawn verbatim from `not-established`; a named rule with the
  specific premise, quantifier, or term it is applied to; or a specifically
  identified hazard word.
  *Banned strings, which a reviewer greps:* "supplies a premise", "used here",
  "as above", "see above", "an ontological commitment", "a metaphysical
  commitment", "denies this premise", "an objection arises", "a hazard",
  "ambiguity" unqualified by the ambiguous term, "sense" unaccompanied by that
  sense's gloss, "a stronger conclusion", "not established here" unaccompanied by
  the named non-consequence, "a rule is applied", "this step follows".
  *No duplicates:* two callouts anywhere in one chapter whose content words are
  identical after striking ids are **both** defects.
- **Page-budget audit** — count notes per page across the chapter. Any page > 5,
  or a chapter median > 3, is margin bloat.
- **Coverage test** (the dual defect, margin starvation) — walk the §11.3 trigger
  column row by row against the audited object; each MUST-fire condition below
  has its note, or the object fails:
  1. `DEF` — each line whose sense selector differs from that term's previous
     occurrence in this `PF-###`.
  2. `DIST` — each `DS-###` listed in `lexicon`, on its first consuming line.
  3. `INF` — each quantifier, modal, or discharge step, and each near-neighbour
     trap.
  4. `IMPORT` — each `commitments` entry with `import: REAL`, selected under
     the cap of three, at the line incurring it.
  5. `MODAL` — each necessity-kind or `SCP-*` change, and each `BR-###`
     citation.
  6. `WHY` — exactly one per `RG-WHY` object; none in an `RG-THAT`.
  7. `RISK` — each `PRD-ANA` term rendered as one predicate letter, each
     `L1-PROSE`/`L2-NUM` divergence, each symbolized `denial-set` premise the
     symbolization makes look settled.
  8. `OBJ` — each `denial-set` member.
  9. `SCOPE` — `established`, and each line whose ordinary reading would assert
     an entry of `not-established`.
  10. `USES` — each distinct id in `depends-on`, and each `W-DEM` premise.
  11. Each `FLAG` and each `FAIL` row in the printed audit table, on its
      offending line, tagged per §11.7.
  A miss on any row is a defect of the same severity as bloat.

### 11.7 Interaction with the audit rubric and the error taxonomy

- **Audit linkage.** Every `FLAG` or `FAIL` mark in a printed audit table has a
  callout on the offending line, and that callout MUST end with the axis token
  and mark in square brackets: `[MOD FLAG]`, `[SEM FAIL]`, `[PRV FAIL]`. Nothing
  else goes inside the brackets. The tag does not count toward the 20-word
  budget. Conversely, **no axis tag may appear in a margin without a
  corresponding row in a printed audit table** — no orphan flags.
- **Deferred audits.** Where the audit is set as an exercise and the table prints
  only in the matching `SO-##.##` (§6.6), the linkage moves with the table. The
  body-side margin beside the proof carries its mandatory callouts but **no axis
  tag**, no table yet being printed. The solution MUST then print, for every
  `FLAG` and every `FAIL` row in its table, the callout text and the line id it
  attaches to, in the form the margin would have carried, tagged with the axis
  and mark — `PF-014.3` · `IMPORT!` *Quantifies over movers as really distinct
  from the moved* `[ONT FLAG]`. The coverage test runs against the solution's
  table and that list, not against the body-side margin. A deferred audit whose
  solution prints marks with no matching callout list is rejected.
- **Axis coverage.** The token-to-axis map is fixed here, is total, and is used
  unchanged by §6.2 and §7.9: `DEF`→`SEM`; `DIST`→`ONT`; `INF`→`LOG`;
  `IMPORT`→`ONT`,`EXI`; `MODAL`→`MOD`; `WHY`→`EXP`,`DEM`;
  `RISK`→`SEM`,`FID`,`PRV`; `OBJ`→`DIA`,`WAR`,`FRM`; `SCOPE`→`SCO`;
  `USES`→`DEP`. A callout may only carry an audit tag naming an axis in its own
  map row.
- **Error taxonomy.** In ordinary text `RISK` is the only token that may cite an
  `ER-###`, and only where the hazard on that line instances the class. Inside a
  `SPECIMEN`'s audit pass the family callout token assigned by the
  family-to-callout map of §7.9 may **also** carry exactly one `ER-###` — `INF`
  or `IMPORT` for `EF-LOG`, `MODAL` for `EF-MOD`, `SCOPE` for `EF-SCO`, listed
  here illustrative of §7.9's family-to-callout table rather than as the
  complete map — so that the defect is marked by the token whose axis fires. No callout carries two
  `ER-###`. The citation marks the defect *location*; diagnosis, repair, and
  surviving conclusion live in the main text, never in the margin.
- **Citation format.** Ids appear bare, uppercase, unbracketed: `PR-014`,
  `TM-012.2`, `PF-009.4`. No *cf.*, no *see*, no page or chapter numbers, no
  italic titles, no parentheses.

*Worked pair.* Line: "Whatever is in motion is put in motion by another
(`NEC-MET`, `SCP-CMP`); this is in motion (`ACT`); so this is put in motion by
another." Admissible: `MODAL!` *Consequence necessary, consequent not; conclusion
holds only as* `ACT` `[MOD OK]`. Inadmissible: `MODAL!` *This move is safe
because the premise is necessary in the composite sense* — a connective joining
two claims, and a defence of the move: missed by the overlap test, caught by the
no-argument clause.

### 11.8 Accessibility, restated locally

Callout meaning MUST survive grayscale printing and photocopying, and MUST NOT be
carried by color alone or by color as its only reliable channel. The token
spelling is always printed; kind is carried by the four channels of §11.2, with
which any color the production section uses is redundant. A page rendered at 100%
black must be fully legible and fully disambiguated.

### 11.9 Local decisions, spine silent

- **`SPECIMEN` objects** (plausible-but-defective arguments). A specimen's first
  presentation carries **no margin callouts of any kind, in any stage** (§8.8.1,
  D4): the margin never discloses the defect before the reader has diagnosed it.
  Callouts — including the `RISK` note naming the `ER-###`, and the family token
  of §11.7 — appear only in the audit pass printed after it, and there the
  specimen is annotated exactly like a demonstration, under every rule of this
  section. The coverage test runs against the audit pass, never against the first
  presentation.
- **Exercise blocks print no callouts** — not because the margin is optional
  there, but because the annotation is withheld from the reader: the annotation
  grammar is itself drilled by the exercise types requiring the reader to supply
  or criticise a callout set. Solutions that print callouts obey this section in
  full.


## 12. Visual and Production Requirements (Specification Only)

§12.1–§12.9 and §12.11–§12.12 are **frozen acceptance conditions**: a reviewer
checks each against a built PDF and passes or rejects. §12.10 is a
**recommendation**: the production agent MAY substitute any package, font, or class
named there if the substitution and its reason are recorded in the build report and
the acceptance conditions still pass. The agent may not revise an acceptance
condition, only report one as unmeetable and stop.

### 12.1 Governing visual principle: reserved emphasis

The design has exactly **one** loud element. Every text-block environment —
propositions, lemmas, corollaries, definitions, distinctions, demonstrations,
objections, replies, audit tables — is set by typographic means only: small-caps
headers, hanging indents, light rules, size and leading changes. **No box, frame,
tint, or rule of weight ≥ 1 pt may be used for any of them.** Boxing and banding
are reserved without exception for the `SPECIMEN` environment (§12.5): a design in
which several environments are boxed cannot make the defective one unmistakable.

*Detector:* open any twenty consecutive pages containing no `SPECIMEN`. Any framed
or tinted region rejects the build. No ornament may appear that carries none of the
semantic loads named here. Drop caps are prohibited outright.

### 12.2 Trim, text block, and measure

**AC-P01 — Measure.** Running body prose MUST set at a mean of **62–72 characters
per line including spaces**, target 66, measured over ≥ 300 full prose lines drawn
from ≥ 5 chapters. Below 62 the frequent inline notation forces bad breaks; above
72 the return sweep degrades on a page also scanned laterally into a dense note
column. The band, not the point size, is the requirement.

**AC-P02 — Identifier integrity.** No identifier, token, or sense selector may
break across a line. *Detector:* search the text layer for a line ending in a
fragment matching `[A-Z]{2}-` or in a truncated token.

**AC-P03 — Trim.** One trim size for the whole book, declared in the build report,
with every page's MediaBox equal to it and no bleed elements. Recommended:
**178 × 254 mm (7 × 10 in)** — a stock print-on-demand size taking a 40 mm+ note
column without dropping the measure below 62 cpl.

**AC-P04 — Asymmetric geometry.** The text block sits toward the spine; the note
column occupies the outer margin and swaps side between recto and verso.
Recommended allocation, summing to the 178 mm trim: inner margin 24 mm, text block
92 mm, text-to-note gutter 6 mm, note column 42 mm, outer margin 14 mm. Vertical:
22 mm head, 200 mm text height, 32 mm foot. The folio sits in the outer foot so a
photocopied excerpt retains its locator.

**AC-P05 — Vertical justification.** The body sets `\raggedbottom`; facing pages
MUST agree in final baseline position to within two lines. `\flushbottom` is
prohibited: with anchored margin notes it buys spread alignment with stretched
interline space, corrupting the grouping of numbered demonstration lines.

### 12.3 The note column and the density budget

**AC-P06 — Worst-case capacity.** The column is sized from the annotation
grammar's worst case: five 20-word notes plus their token labels MUST set in one
page's note column with zero collisions and no note displaced more than two lines
from its anchor's baseline. At 42 mm, 8.5 pt on 11 pt, a 20-word note runs about
four lines and that worst case fills roughly half the column. A narrower column
fails this test before it fails legibility.

**AC-P07 — Over-budget detection.** The class MUST count notes per shipped page and
warn above five; the build gate treats the warning as an error (B08).

**AC-P08 — Outer placement.** Every note sets in the outer margin on both recto and
verso, with strict page-side detection; no note may reach the wrong side or the
wrong page.

**AC-P09 — Token label.** Each note opens with its annotation token in small caps
on its own line, then the note text at note size. The token is emitted by a macro,
never typed literally (AC-P20). Notes take no tint and no color. Each note carries
on its text-side edge the kind marker the margin section (§11.2) assigns —
hairline solid rule for `K-EXPL` explanation notes, heavy solid rule for `K-WARN`
warnings, dotted rule for `K-DEP` dependency notes, double rule for `K-ACT` action
notes — together with the token weight that section specifies (regular, bold,
letterspaced, regular) and its trailing kind glyph (none, `!`, `→`, `?`).

**AC-P09a — Kind separation.** The four kind treatments MUST remain mutually
distinguishable at 1-bit threshold with the note text unread; B08 verifies this on
ten sampled pages each carrying at least three kinds. §12.1's prohibition on rules
of weight ≥ 1 pt governs text-block environments only and does not reach the note
column's kind rules, whose weight contrast is one of the four channels carrying
kind.

### 12.4 Environment inventory

Each row MUST exist as a distinct environment with the stated header form and break
behavior. The printed number is always the ledger identifier (AC-P14).

| Environment | Header form | Break behavior |
|---|---|---|
| `definition` | `Definition DF-007 (Short Name).` | breakable; header never the last line of a page |
| `term` | `Term TM-012 — senses .1, .2.` | unbreakable if ≤ 12 lines |
| `distinction` | `Distinction DS-004 (Short Name) [DK-VIRT].` | breakable; the `DK-*` tag prints in the header |
| `principle`/`proposition`/`lemma`/`corollary` | `Lemma PR-014 (Short Name).` — one environment, kind word drawn from the ledger `kind` field | breakable; ≥ 2 lines each side |
| `demonstration` | `Demonstration PF-023 of PR-014.`, closed by a right-aligned tombstone | breakable; tombstone never alone on a page |
| `objection`/`reply` | `Objection OB-031.` / `Reply RP-031.` | a reply begins on the same page as, or the page facing, its objection |
| `specimen` | §12.5 | §12.5 |
| `audit` | one environment taking its form as a mandatory argument (`AC-P11`): *full* — fourteen rows, rule-input block, verdict line; *probe* — header *Axis probe*, only the named axis rows, no verdict line | AC-P11; the probe form unbreakable if ≤ 6 rows |
| `exercise`/`exerciseblock` | a six-field header block above the item body, fixed order: the id (`EX-03.07`) flush left, then `tier`, `verb`, `target`, `axes`, `product`, each on its own line at note size with the field name in small caps; `axes` prints the literal token `BLIND` when the record carries it, and the class MUST raise a compile error if any axis token is emitted for a `BLIND` item | an item is unbreakable if ≤ 8 lines; the header block never splits from the first line of its body |
| `solution` | `SO-03.07` | AC-P17 |
| `scholion` | `Scholion.` at note size, indented both sides | breakable; never carries an inference |
| `theologicalremark` | the literal formula `Theological remark (not a result of natural reason).` | after `not-established`, outside the proof object; compile error if nested in `demonstration`, `objection`, `reply`, `audit`, or `scholion`; set off distinguishably from `scholion` in grayscale; excluded by construction from every generated `established` line, `dossier`, and register; the class warns if a `steps` line, `USES` callout, or `depends-on` entry cites a line inside it |
| `nosymbolization` | `Non-symbolization notice.` then the four fields of §5.4, each labelled in small caps | unbreakable if ≤ 12 lines; never separated from the `L2-NUM` it governs |
| `rivalregimentation` | `Rival regimentations.`; both symbolizations in a two-row aligned display, the adopted one labelled with its cited ground (§5.5c) | unbreakable; both rows always on one page |
| `validityrider` | no header word; a hairline rule above, then the rider sentence at note size beneath the derivation (§5.5a) | unbreakable; never separated from the derivation it qualifies |
| `modalcommitment` | `Modal commitment.` then the object's `modality` and `SCP-*` tokens and every change of either with its licensing `BR-###` | unbreakable; sits with the layer whose lines it records |
| `frameworkdeclaration` (+ posit table) | `Framework Declaration.`, six numbered clauses, then the numbered posit table of §14.1, reprinted as an appendix | front matter, begins recto; a clause never splits from its number; the posit table repeats its header row on break |
| `frameworknotice` | `Framework notice.` at the head of every chapter whose demonstrations consume an `AT` posit | unbreakable; prints below the chapter head, above the `propositionsinforce` strip |
| `conditionalitynote` | no header word; body text set beneath `established`, third in the order §4.5 fixes, in the fixed form of §14.4, **never** in the margin | unbreakable; no page break between `established` and the note |
| `rivalregister` | `Rival register.`, keyed by position name, columns per §14.5; printed once in back matter | breakable at row boundaries; header row repeats |
| `bridgetable` | `Bridge table.` with the four columns of §8.10 F2 | prints before its chapter's proof; breakable with repeating header |
| `dossier` | `Terminus dossier — PR-4## established of the terminus.` (§8.10 F4) | reprinted at the close of every Stage F chapter; breakable at row boundaries; header repeats |
| `propositionsinforce` | `Propositions in force.` strip at each chapter opening: id, short name, one-line modality, page (§10.6) | breakable at row boundaries only |
| `usesbar` | one rule-delimited line immediately below an environment header: `Uses: DF-002, PR-004 (p. 58).`, or `Uses: none.` | never omitted; never breaks; never separated from its header |
| `reducedproof` | `Proof PF-032/min (Short Name).`; exactly the ten fields of §4.8 in that order, closed by an `audit` in its probe form | unbreakable if ≤ 15 lines |
| `errorblock` | `Error class ER-204 (Short Name).`, then the five parts under the fixed headings *Specimen*, *Locus*, *Licenses*, *Repair*, *Survives* (§7.3), closed by the two-line audit stub | breaks only between parts; no heading is the last line of a page; the audit stub never stands alone on a page |

**Revelation formulas.** No environment other than `theologicalremark` and
`scholion` may print a sentence beginning "On revelation," or "As a datum of
faith,". The class warns on either string elsewhere, and the build gate treats the
warning as an error (B04).

**AC-P10 — Demonstration layout.** `L2-NUM` sets as three aligned columns: step id
(`PF-023.4`) in a fixed-width hanging indent; step content in the measure;
justification (`from`, `rule`) right-aligned at the text-block edge in small caps at
note size. Columns align down the whole demonstration; a wrapped step keeps its
justification on its first line; no page break separates a step from its
justification.

**AC-P11 — Audit table: two forms.** Two audit forms exist, and the environment
takes the form as a mandatory argument.

1. **Full audit.** All fourteen axis rows in axis order (§6.2), `OK` rows included,
   then the rule-input block — the extra fields the matched verdict rule requires
   (§6.3) — then the verdict line: the token in small caps preceded by *Verdict*,
   with the rung where applicable.
2. **Axis probe.** Used in Stages A and B and by every reduced object. Only the
   axes named in the probe print; the header reads *Axis probe*; omitted axes are
   simply absent, not marked `N/A`; **no verdict line is printed**.

The class MUST raise a compile error on (a) a full audit with fewer than fourteen
rows, (b) a probe carrying a verdict token, (c) a probe used in Stage C or later
otherwise than as the closing probe of a `reducedproof`, which §4.8 licenses at
every stage. B16 checks all three. Either form sets in the measure; if it breaks, the header row
repeats and the caption reads *continued*. Any `FLAG` or `FAIL` row MUST be paired
with a margin callout on the offending line; the class SHOULD warn when a table
carries a non-`OK` mark and the enclosing proof object carries no callout.

### 12.5 The `SPECIMEN` environment

A specimen defect mistaken for the book's own doctrine is this design's worst
failure. The environment carries **four independent channels**, and its acceptance
conditions state how many survive each degradation.

1. **Band** — a 6 mm diagonally hatched band (45° rules, ~1.5 mm pitch) in the outer
   margin, running the full height the environment occupies on every page it
   occupies. Hatching, not tint: it survives 1-bit thresholding.
2. **Word** — `DEFECTIVE` in spaced small caps in the header, repeated in the outer
   foot of every such page as `SPECIMEN PF-025/S — DEFECTIVE`.
3. **Typeface shift** — specimen body in a visibly different family at the same
   optical size, so the block reads as quoted, not authorial.
4. **Tint** — 10 % flat gray behind the body. Redundant accelerant only; it may
   never be counted toward a survival condition.

**AC-P12 — Survival conditions.**

| Degradation | Condition |
|---|---|
| Two-page opening, in color, at arm's length, unread | Channels 1 and 3 identify the block as not-the-book's-voice without reading a word |
| Grayscale print at 600 dpi | All four channels present, body legible, tint no darker than 12 % |
| 1-bit threshold photocopy of **any single page** carrying specimen material | **≥ 2** channels survive on that page — necessarily 1 and 2, tint dropping out and family shift softening; hence the per-page `DEFECTIVE` foot |
| Excerpt handed to a reader who has not seen the book | The reader states within five seconds that the material is presented as erroneous. Failure rejects the build regardless of every other condition |

**AC-P13 — Break behavior and verdict adjacency.**

1. A `specimen` MUST NOT begin within the last four lines of a page; shorter than
   0.75 text height, it MUST NOT break at all.
2. When it breaks, the continuation prints `Specimen PF-025/S, continued —
   DEFECTIVE`, and band and foot continue.
3. **No page break may fall between the specimen's last line and its closing
   verdict line** (verdict token plus `ER-###` list). The verdict is inside the
   environment, so no page can end with unlabelled defective reasoning.
4. A specimen MUST NOT be the last material on a recto whose verso begins a new
   topic: the diagnosis or repair begins before the page turn, or the specimen moves.
5. No `PR-###` may be established inside a `specimen`, and nothing inside one may be
   labelled as an establishing location. A specimen is indexed only in the Register
   of Specimens (AC-P30); a specimen locator in the Index of Propositions and Proof
   Objects is a build failure.

### 12.6 Numbering, cross-reference, and ledger alignment

**AC-P14 — No independent counters.** Every numbered item's printed number **is**
its ledger identifier. The class MUST NOT auto-increment a counter for any id class
of §4.1 and §10.1. Each environment takes its id as a mandatory argument, sets its
label to exactly that id, and MUST raise a compile error on disagreement. Chapter
and section numbers are the only autonomous counters. The rule follows from the
status-is-a-field decision of §4.1 and §10.1: a lemma promoted to a proposition
keeps `PR-014`, and the header word is drawn from the ledger `kind` field rather
than encoded twice.

**AC-P15 — Exercise field consistency.** In `EX-##.##` the first field MUST equal
the chapter counter zero-padded to two digits; a mismatch is a compile error.
Chapter numbers are capped at 99.

**AC-P15a — No answer leakage from an exercise.** No exercise environment may
print an `ER-###`, an answer-mode token (`SETTLED`, `PLURAL`, `IRREPARABLE`), an
axis token for a `BLIND` item, a verdict token, or any audit mark. *Detector:* grep
the text layer of every exercise block for `ER-`, `V-`, `FIX-`, the three
answer-mode tokens, and the three audit marks `OK`, `FLAG`, `FAIL`; and, in a
`BLIND` item only, for the fourteen axis tokens. Any hit outside a `product`
field's description is a build failure (B16). This list is the single governing
one: §9.1.5 cites it and states no list of its own.

**AC-P16 — Reference form.** Every cross-reference prints kind plus id (`Lemma
PR-014`, `Exercise EX-03.07`, `Specimen PF-025/S`); references crossing a chapter
boundary add a page number. Prose anaphora is prohibited: the text layer MUST
contain zero occurrences of *the argument above*, *as shown earlier*, *the previous
proposition*, *the foregoing*, *see above*, *see below*.

**AC-P17 — Solution separation.** A solution MUST NOT fall on the same page or the
facing page as its exercise; solutions collect in back matter. Each exercise block
ends with one pointer line naming the solution range and its page; individual
exercises carry no page pointer.

### 12.7 Dependency edges in print

A printed proof object shows its dependency edges in three places and only these:

1. **Dependency bar** — the `usesbar` environment (§12.4): ids only, ascending, no
   summaries, never omitted, so its absence is detectable by inspection.
2. **`USES` margin callouts** at each consuming line, per the annotation grammar.
3. **Chapter-end dependency diagram** (AC-P18), backward edges only; the
   `consumed-by` direction is a forward reference and appears only in the ledger
   appendix.

**AC-P18 — Dependency diagrams.** A DAG, top-to-bottom, node label = identifier over
short name. Edge kinds are distinguished by **line pattern and arrowhead shape
only**: solid = `depends-on`; dashed = a bridge `BR-###`, labelled with its id;
dotted = an edge into a `SPECIMEN`. Content MUST be generated from ledger data, not
hand-drawn; the gate verifies that every drawn edge exists in `depends-on` and
every in-scope entry is drawn. A diagram exceeding the measure sets landscape on
its own page rather than shrinking below 7 pt labels.

**AC-P19 — Inference trees.** Every inference line carries its rule name as a right
label; an unlabelled line is a defect, not a layout choice. A tree overflowing the
measure MUST be decomposed into named subtrees, each with its own conclusion, never
scaled. Overflow into the note column is fatal.

### 12.8 Notation, tokens, and mathematics

**AC-P20 — Every closed-vocabulary token is a macro.** Every token belonging to
any family declared closed anywhere in this specification — wherever declared, and
including a family added by later amendment — MUST be emitted by a macro that
validates the token against that family's closed list and errors on an unknown one.
Literal token strings in source are prohibited. This makes a misspelled token a
compile error rather than a silent divergence from the specification, makes
coverage checkable, and needs no edit when a family is added.

**AC-P21 — Symbol registry.** Every mathematical or metaphysical symbol is
introduced by a semantic macro and recorded in the Index of Notation with symbol,
reading, and location of introduction. Raw glyphs for registered operators are
prohibited in source.

**AC-P22 — Long equations.** Displays break before a binary relation or operator,
repeating it at the head of the continuation; no display is scaled to fit. Global
equation numbering is suppressed: a display that is a proof step takes the step id
(`PF-023.4`) as its right-aligned tag; one that is not a step is unnumbered and
MUST NOT be referred to.

**AC-P23 — Fonts.** The family MUST supply true small caps (not slanted or scaled),
oldstyle and lining figures, and a matching OpenType math font covering every
symbol used. Acceptance: zero missing-glyph and zero substitution warnings.

### 12.9 Color, grayscale, and print quality

**AC-P24 — No meaning by color alone.** Absolute. Every semantic distinction is
carried by shape, position, weight, pattern, or a printed word; color is redundant
wherever it appears. *Detector:* rebuild with all color forced to black; if any
distinction a reader must make is no longer makeable, the design is rejected. The
two builds MUST have identical pagination.

**AC-P25 — Ink budget.** At most two non-black inks in the whole book, only in
dependency diagrams and inference trees. The hue pair MUST stay distinguishable
under simulated deuteranopia, protanopia, and tritanopia, and MUST differ by
≥ 30 L\* so it separates in grayscale. Body text and all rules are 100 % K.

**AC-P26 — Print quality.** PDF/X-4 or PDF/X-1a; all fonts embedded and subset; all
text 100 % K, never four-color black; no transparency in the print stream; no raster
below 600 dpi at placed size; no bleed elements, so trimming variance cannot clip a
band or folio; every MediaBox equal to the declared trim.

**AC-P27 — Widows, orphans, headers.** Club, widow, and display-widow penalties set
to prohibit single lines at a page boundary; no environment header is the last line
of a page. Any occurrence in the built PDF is an error, not a warning.

**AC-P28 — Reading order.** The document declares its language; extracting the text
layer of any page yields the body in reading order, each margin note emitted
adjacent to its anchoring paragraph rather than interleaved mid-sentence.
Structural tagging is a SHOULD; correct extraction order is a MUST.

### 12.10 Recommended toolchain (revisable with a stated reason)

**Engine: LuaLaTeX** — OpenType fonts with real small caps and oldstyle figures via
`fontspec`/`unicode-math`, and because per-page note counting (AC-P07), token
validation (AC-P20), and the ledger cross-check (B05) are written in Lua rather
than in expansion-only TeX.

**Base class: `memoir`, over KOMA-Script.** The decisive reasons are AC-P04 and
AC-P08: `memoir` states this asymmetric five-zone geometry and strict recto/verso
detection directly (`\setlrmarginsandblock`, `\setmarginnotes`, `\sidepar`,
`\strictpagecheck`/`\checkoddpage`) and supplies multiple independent indexes
(AC-P30) natively, whereas KOMA-Script's `typearea` derives margins from a DIV
canon, so this geometry means disabling the mechanism its quality rests on and
rebuilding the note apparatus anyway. Choose KOMA-Script only if
`scrlayer-scrpage`'s head/foot machinery comes to matter more — and say so.

Recommended packages, each revisable: `amsmath` + `mathtools` (AC-P22); `amsthm`
with its numbering hook replaced so ids come from arguments (AC-P14);
`unicode-math` with a Libertinus or STIX Two Serif/Math pairing (AC-P23);
`marginnote` for non-floating notes, which work inside theorem-like environments
and floats where `\marginpar` fails; `tcolorbox` breakable for the specimen band,
tint, and continuation header — and for nothing else, per §12.1; `booktabs` with
`tabularray` or `longtable` for repeating header rows (AC-P11); `bussproofs` for
inference trees; TikZ for ledger-generated diagrams; `cleveref` configured to print
kind-plus-id (AC-P16); `biblatex` with `biber`; `microtype`.

Two integration risks the build report MUST address: `marginnote` does not float,
so collision avoidance is the class's responsibility (AC-P06, AC-P09a); and
`tcolorbox` breakable interacts poorly with notes anchored inside it, so
specimen-internal callouts may need raising to the enclosing page context.

### 12.11 Apparatus

**AC-P29 — Bibliography.** Author–year for modern secondary literature. Classical
and scholastic primary sources cite by canonical locus (Bekker number, *Summa*
part–question–article), never by page of a printing; the edition or translation is
named separately, and every non-English primary source names a translation. No citation may occupy a warrant slot in any proof object; a citation
appears only in a `scholion`, a `theologicalremark`, or a classified citation form.

**AC-P30 — Indexes and registers.** Five: Index of Terms (by `TM-###` with sense
selector); Index of Propositions and Proof Objects (by identifier, establishing
location in bold); Index of Names; Index of Notation (AC-P21); Register of
Specimens (each specimen's id, the `ER-###` classes it instantiates, and its page).
Acceptance: every `ACTIVE` record of kind `TERM` appears in the Index of Terms;
every `ACTIVE` `PR-###` and every `PF-###` with `kind: DEMONSTRATION` or
`DIALECTICAL` appears in the Index of Propositions and Proof Objects, checked
mechanically against the ledger for propositions and against the chapter sources
for proof objects; no `PF-###` with `kind: SPECIMEN` appears in that index at all.

**AC-P31 — Glossary.** Generated from exactly the families AC-P20 validates
against, so that a family added by amendment is covered without editing this
condition. One entry per token: the token, its one-sentence meaning, and the
location of its governing definition. Every token of every such family appears
exactly once; a token used in the body but absent from the glossary, or present
twice, is a build failure.

### 12.12 Build verification gate

The production agent MUST run all of the following and record each outcome in a
build report accompanying the PDF. A PDF submitted without a complete build report
is rejected unread.

| Id | Check | Pass condition |
|---|---|---|
| B01 | LuaLaTeX ×3 plus `biber` | Zero errors; zero undefined references or citations; zero multiply-defined labels |
| B02 | Overfull boxes | Zero above 0.5 pt in the text block; **any** intrusion into the note column is fatal |
| B03 | Unresolved markers | Zero `??` and zero placeholder strings in the text layer |
| B04 | Phrase grep (AC-P16, §12.4) | Zero hits on the prohibited anaphora list; zero sentences opening "On revelation," or "As a datum of faith," outside `theologicalremark` and `scholion` |
| B05 | Ledger cross-check | Every printed id exists in the ledger with matching kind and name; every `ACTIVE` record is printed; `LC-01`–`LC-22` clean, or every exception listed with a reason |
| B06 | Grayscale build diff (AC-P24) | Identical pagination; no distinction lost |
| B07 | Specimen degradation (AC-P12) | 1-bit render of every page carrying specimen material shows ≥ 2 channels; the five-second reader test passes |
| B08 | Margin density and kind separation (AC-P07, AC-P09a) | Zero pages above five notes; zero collisions; median ≤ 3 across the book; on ten sampled pages carrying ≥ 3 kinds, the four kind treatments separate at 1-bit threshold with the text unread |
| B09 | Widow/orphan/header scan (AC-P27) | Zero occurrences |
| B10 | Break-rule scan (AC-P13, AC-P10, AC-P17) | Zero verdict separations; zero split step/justification pairs; zero solution adjacent to its exercise |
| B11 | Fonts and geometry (AC-P23, AC-P26, AC-P03) | All fonts embedded and subset; zero substitution warnings; every MediaBox equals the declared trim |
| B12 | Measure sample (AC-P01) | Mean characters per line in 62–72 over ≥ 300 sampled prose lines |
| B13 | Diagram/ledger agreement (AC-P18) | Every drawn edge exists in `depends-on`; every in-scope edge is drawn |
| B14 | Token validation (AC-P20) | Zero literal token strings in source; zero suppressed unknown-token errors |
| B15 | Reading order (AC-P28) | Text extraction of ten random pages yields body prose uninterrupted by note text |
| B16 | Audit form and exercise leakage (AC-P11, AC-P15a) | Zero full audits with fewer than fourteen rows; zero probes carrying a verdict token; zero probes in Stage C or later other than a `reducedproof`'s closing probe; zero exercise-block hits on `ER-`, `V-`, `FIX-`, an answer-mode token, an audit mark, or — in a `BLIND` item — an axis token |

B07 is the only check requiring a human. It is not optional, and may not be run by
the agent that designed the specimen environment.


## 13. Source and Authority Policy

**Governing rule.** A citation never warrants a premise. §2.1.2 closes the
warrant list, and `W-AUTH` is on it only so that the audit can detect it; axis
`PRV` is `FAIL` whenever a citation occupies a warrant slot. Everything below
makes that rule checkable sentence by sentence.

### 13.1 Bodies of material and the role each plays

| Body | Role it plays | Role it never plays |
|---|---|---|
| Aristotle | Demonstrative apparatus (middle term, *per se* predication, `PRI-*` order, `SER-ESS`); `TM-###` senses; origin of reconstructed `PF-###` | Warrant. No `BR-###`, `DF-###`, or premise is licensed by "Aristotle argues so" |
| Aquinas | The same, plus standing formulations of most Stage C–F `PF-###` and of *videtur quod* objections | Warrant; nor arbiter of whether a reconstruction succeeds — the audit table is |
| Classical / scholastic vocabulary | The primary `TM-###` lexicon: act, potency, essence, *esse*, per se / per accidens, analogy, `DK-*`, `QUA-*` | A supply of premises. Entering the lexicon commits the book to a *sense*, never to a proposition (`LC-08`) |
| Contemporary formal logic | Calculi named in `logic`, rules cited by `steps`, `L3-SKEL` notation; owns `LOG` and `EXI` | Metaphysical content: `NEC-LOG` and `NEC-CON` results carry no real import without a cited `BR-###` (§3.9) |
| Contemporary analytic metaphysics | Sharpened distinctions (`PRI-GND` against `PRI-ONT`), rival `L3-SKEL` regimentations, and — required by MD9 — each named opponent's strongest reason | Warrant, or neutral referee. An analytic objection is `OB-###` material with its own `RP-###`, not an automatic defeater |

No body is a court of appeal. A question is settled only by a rule of the
declared calculus, a §2.1.2 warrant that survives audit, or a prior `PR-###`
cited by id.

**Historical reconstruction.** The reconstructed historical theory of
demonstration — Aristotle's *apodeixis* and Aquinas's adaptations — is binding
on every `CC-TEXT` claim about what either author held, said, or meant. The
reconstruction lives at §2.8.2 (Aristotle) and §2.8.3 (Aquinas), with
concordance tables at §2.8.5 mapping modern apparatus tokens to their
historical antecedents and stating the disanalogy. The Heritage Declaration
(§2.8.4) labels the modern proof-engineering apparatus as a pedagogical
superstructure built over the tradition, not the tradition itself. House rule
8 (§1.7) and `UA-11` (§16.3) enforce the distinction. A later agent presenting
the historical theory cites the historical terms by their own names and loci,
not by modern apparatus tokens; a later agent using the modern apparatus cites
it by its own tokens, not as "what Aristotle called..."

### 13.2 The six claim classes

Token family `CC-*` (closed). Every asserting sentence belongs to exactly one
class. The **printed marker** lets a reader classify a sentence at sight without
consulting a ledger; it is content, not typography: the production section may
style it, never remove it.

| Token | Class | Printed marker | Must cite | The citation establishes | It conspicuously does **not** establish | May occupy |
|---|---|---|---|---|---|---|
| `CC-TEXT` | textual / historical — "Aquinas says X" | Names the author, carries a §13.3 locus, and stands in a `scholion`, a footnote, or a passage explicitly marked as historical | Full locus per §13.3 | That the author wrote those words there, in that edition and translation | That X is true; that the author held X as his settled view (itself a further historical claim); that anyone should accept X | `scholion`; historical prose; never `premises`, `steps`, `DF-###`, `DS-###`, or `commitments` |
| `CC-TERM` | terminological — "X is traditionally called Y" | The phrase "traditionally called", "in the scholastic vocabulary", or "we retain the term", plus the `TM-###.n` id | One locus establishing the usage, or a standard lexicon entry | That the label is in use with that sense in that tradition | That anything answers to the term; that the distinction it names is `DK-REAL` rather than `DK-VIRT` or `DK-NOM` | `lexicon`; `TM-###` records; `DEF`/`DIST` callouts |
| `CC-LOG` | logical | The line names its rule and the lines it consumes (MD1) | The calculus named in `logic` | That the step is licensed under that calculus and reading | Truth of any premise; that the symbolization preserves the claim (axis `FID`) | `steps`; `L3-SKEL` |
| `CC-META` | metaphysical premise | The premise line prints its `warrant`, `modality`, `modal-scope`, and `import` tokens (§4.3) | Nothing external; it must carry a §2.1.2 warrant other than `W-REV` or `W-AUTH` | — | — | `premises`; `PR-###` with `kind: PRINCIPLE`, `DISPUTED-PREMISE`, or `FRAMEWORK-POSIT` |
| `CC-DEM` | demonstrated conclusion | Asserted only by `PR-###` id, with a `USES` callout, never above that record's `established` | Its `established-by` `PF-###` and audit verdict | That the claim holds at the recorded rung, modality, and scope | Anything in that record's `not-established`; anything at `RG-VALID` or `V-VALID-ONLY` about the real world | `established`; later `depends-on` chains |
| `CC-REV` | theological datum accepted on revelation | The block opens with the literal sentence-initial formula **"Theological remark (not a result of natural reason)."** and every claim inside is prefixed "On revelation," or "As a datum of faith," | The doctrinal locus (scriptural reference, conciliar or magisterial document with section number) | That the datum is so held, and where | That it is demonstrable; that it follows from anything in the book; that any philosophical result reaches it | `scholion`; theological remark blocks only (§13.4) |

**Distinctions are claims.** A `DS-###` whose distinction-kind tag is `DK-REAL`
or `DK-VIRT` asserts something about things and is therefore a
metaphysical-premise sentence, not a terminological or textual one. It MUST be
carried by a `PR-###` stating the distinction in one sentence with its own
warrant, `modality`, `modal-scope`, and `import`, and that `PR-###` MUST appear
in the `DS-###` record's `depends-on`. The separability test or
divergent-entailment exhibition that §3.9 requires of a distinction MUST be that
`PR-###`'s printed warrant analysis or its `established-by` proof, and MUST NOT
be a textual sentence, a quotation, or a locus. A `DK-REAL` or `DK-VIRT`
distinction lacking that `PR-###` is `PRV` = `FAIL` and `ONT` = `FAIL`, and no
proof object may list it in `lexicon` or `commitments`. *Reviewer test:* strike
every canonical or contemporary author's name, quotation, and locus from the
passage introducing a `DS-###`; if the required test order is no longer
exhibited, the distinction was carried by authority.

**Gloss fidelity.** Where a terminological sentence glosses the term it names,
the gloss MUST be the cited `TM-###.n` sense line verbatim, or a strict
abbreviation adding no clause and no entailment; any relative clause,
apposition, parenthesis, or qualifier present in the gloss but absent from the
sense line is a metaphysical assertion and MUST be removed from the gloss and
carried by a `PR-###` with its own warrant, `modality`, and `import`. *Reviewer
test:* delete from the printed gloss every clause absent from the cited sense
line; if any claim is lost, the terminological sentence was carrying
metaphysical content — `PRV` = `FAIL` and `SEM` = `FAIL`. The same rule governs
a terminological sentence introducing a `DS-###`, whose gloss may name the two
sides and print the distinction-kind tag and nothing further.

**Warrant mapping.** `CC-TEXT` and `CC-TERM` supply *no* warrant token whatever;
`CC-LOG` licenses steps, never premises; `CC-META` alone may carry `W-SELF`,
`W-IND`, `W-EMP`, `W-POST`, or `W-HYP`; `CC-DEM` alone `W-DEM`; `CC-REV` carries
`W-REV`, which excludes it from every `kind: DEMONSTRATION` object.

### 13.3 Edition and translation discipline for `CC-TEXT`

A passage is identified by all five of: (i) author; (ii) work, canonical short
title; (iii) canonical internal locus, never a page of a modern printing —
Bekker number for Aristotle; part, question, article, and *corpus* or *ad n.*
for the *Summa theologiae*; book, chapter, paragraph for *Summa contra
Gentiles*; book, lectio, Marietti paragraph for the commentaries; (iv) the
edition relied on (Leonine, Marietti, Bekker/OCT, named critical edition);
(v) the translation and its translator, or "tr. mine". Every textual sentence
anywhere in the book carries all five parts — worked examples, specimen objects,
exercises, solutions, and incidental parenthetical asides included; brevity is
not an exemption.

Two further rules. **(a)** Where the argument turns on a term, the original-
language term is printed once in parentheses at first use (*esse*, *ἐνέργεια*),
and a material divergence between translations of it is recorded as a `RISK`
callout, not silently resolved. **(b)** *A textual claim is a historical claim.*
"Aquinas holds that whatever is moved is moved by another" is a claim about
Aquinas, warranted by loci and defeasible by other loci; it is never a reason to
accept that whatever is moved is moved by another. Where the book asserts both,
they are two sentences of two classes, and the `CC-META` one carries its own
warrant token.

### 13.4 `CC-REV`: the absolute prohibition

**Prohibition.** A proposition accepted on revelation may never appear as a
conclusion of natural reason, inside such a conclusion, as a premise of a
`kind: DEMONSTRATION` object, as the antecedent discharged by a `BR-###`, or as
the tacit ground of a `W-SELF` claim's "analysis". `LC-09` catches the ledger
form; axis `PRV` catches the printed form; the verdict is `V-FATAL` unless the
premise passes the faith-independence test below **and** carries `W-SELF` with
its analysis printed, `W-DEM` citing an `established-by` proof, `W-IND` with its
inductive base named, or `W-EMP` with its source cited — in which case it was
never `CC-REV` in that use and is rewritten as `CC-META`. `W-POST` and `W-DEF`
are never sufficient re-warrants, neither supplying any reason for the premise's
content; a doctrinal premise offered as `W-POST` is `PRV` = `FAIL`, not
`V-OPEN`.

**Faith-independence test (content-based, binding).** Strike from the author's
stated evidence every proposition believed only because a tradition teaches it,
and read what remains. If no stated reason remains for asserting this sentence
in this form and at this strength, the item's warrant is `W-REV` whatever token
is printed, and the verdict is `PRV` = `FAIL` regardless of the printed token.
The test runs on premises, bridges, definitions, and term senses alike, and
marker-driven excision alone does not discharge it: an undeclared revealed
premise carries no marker to excise.

**Where such data may appear at all.** (1) A theological remark block, placed
after `not-established` and structurally *outside* the proof object, relating an
established philosophical result to a theological one by contrast, restriction,
non-identity, or shortfall; it may never add to `established`, and the audit is
computed as if it were absent. (2) A `scholion`. (3) Chapter framing prose posing
a question, provided no later line cites it. (4) An `OB-###` labelled a
theological objection, with a likewise labelled `RP-###`; such a pair never
counts toward MD9's `denial-set`, which is philosophical.

**Reviewer test (excision test).** Delete every theological remark block, every
`scholion`, and every sentence carrying the `CC-REV` marker; then delete every
proposition whose warrant chain passes through one. Re-run the proof object. If
any `steps` line has lost an input, any premise has lost its warrant, or
`established` has narrowed, the demonstration was using revelation: `PRV` =
`FAIL`.

**The failure mode to be hunted.** A revealed premise entering a *bridge step*,
where it is least visible. Worked instance: a regress argument excluding an
infinite series by asserting that the world began to exist. That proposition is
`CC-REV`. That Aquinas denies its demonstrability — Aquinas, *Summa theologiae*
I q. 46 a. 2 corp. (Leonine; tr. mine) — is a `CC-TEXT` claim and settles
nothing. The repair is not to cite him: declare the series `SER-ESS`, so that the
concurrency test of §3.9 blocks the regress with no temporal premise, and record
in `not-established` that no `SER-ACC` regress has been excluded. A demonstration
not repairable this way is a theological argument and is labelled one
(§2.1.2).

### 13.5 The appeal-to-canonical-author rule

**Trigger (binding).** The deletion test applies to every passage appealing to a
source, author, school, tradition, consensus, received view, or long acceptance,
whether or not a proper name occurs; absence of a proper name aggravates the
defect rather than excusing it, leaving nothing to strike.

**Deletion test.** Strike the author's name, the school or tradition invoked,
the quotation, and the locus; read what remains. If any premise now lacks a
warrant, any step lacks a rule, any `DF-###` or `TM-###.n` lacks a sense, any
`DS-###` lacks its required exhibition, any objection loses its force, or any
`RP-###` loses its answer, the citation was doing argumentative work: `PRV` =
`FAIL`. If what remains is unchanged as an argument, the citation is a
legitimate `CC-TEXT` scholion. `UA-3`, the acceptance checklist's citation veto
(§16.3), is read against this six-item loss list and the trigger above, not
against the presence of a proper name.

**Remedy, one of exactly two.** (a) *Reconstruct and audit*: enter the argument
the author gives as a `PF-###` with premises, warrants, and a full fourteen-axis
audit, and let the result stand on that audit — the citation surviving only as
`scholion`. (b) *Drop the claim*. A third option — retaining it hedged ("as the
tradition maintains") — is prohibited; hedged authority is still authority.
Formulations treated as `PRV` `FAIL` markers on sight, anywhere but a
`scholion`: "as Aristotle shows", "the Angelic Doctor establishes", "the
tradition has always recognized", "it is a commonplace of scholastic metaphysics
that". These are examples, not an exhaustive list: any construction offering
acceptance, antiquity, or consensus in place of a warrant is `PRV` = `FAIL` on
sight. The rule reaches contemporary authors identically — "Kripke showed that"
is `W-AUTH` exactly as "Aquinas showed that" is.

**Replies are arguments.** Every claim asserted inside an `RP-###` that is not
already an `ACTIVE` id cited by id MUST print a warrant token, `modality`,
`modal-scope`, and `import` exactly as a premise subrecord does (§4.3), or the
reply's disposition MUST be `RD-OPEN`. A reply whose operative content is a
textual sentence is `PRV` = `FAIL` and its disposition is corrected to
`RD-OPEN`. Where the answer the book wants is one a canonical author gives,
remedy (a) applies: the answer is reconstructed as a `PF-###` with premises,
warrants, and a full audit, the citation surviving only as `scholion`.

**Mandatory grep**, run over every authored file and not only over files
containing `W-REV` or `W-AUTH`:

```
grep -nEi '\b(traditionally|the tradition|commonplace|widely (held|accepted)|generally (agreed|accepted)|no one (denies|disputes)|everyone (accepts|grants)|received view|it is agreed|long recognized|has always|is well known)'
```

plus one grep per surname in the bibliography. Each hit is adjudicated against
the §13.2 table and its disposition recorded; an unadjudicated hit blocks
acceptance.

### 13.6 Honesty rules

1. **Cite only what was used.** Every bibliography entry is cited at a specific
   locus; none appears for standing or completeness. A spot-check of any entry
   must find its locus.
2. **Invent nothing.** No fabricated quotation, locus, attribution, doctrine,
   edition, translator, historical event, or scholarly consensus. A quotation is
   printed only if its wording was checked against a named edition or
   translation; otherwise the book paraphrases and marks it as a paraphrase. An
   unverifiable locus means the claim is dropped, not approximated.
3. **Preserve material disagreement.** Where competent scholarship divides on
   what an author held, or on a translation that matters to the argument, the
   division is stated with at least one locus per side and left unresolved unless
   the book argues for one side. Harmonizing rival readings into a single smooth
   "the tradition holds" is a defect. An MD9 opponent position must be traceable
   to a cited proponent's own statement of the reason; a reason with no proponent
   behind it is presumptively below its strongest form (`DIA` = `FAIL`).

   **Constructed objections.** The adherent-source requirement is a floor on how
   weakly a named position may be stated, never a ceiling on what may be
   objected. Where the minimal `denial-set` includes a premise no standing
   position has addressed in print, the author MUST retain it and supply an
   author-constructed objection, marked in the `OB-###` as constructed and
   carrying one sentence naming the position-type that would reject it and why
   nothing in the cited literature reaches it; it is stated at the strongest form
   the author can produce and is subject to the anti-straw-man tests like any
   other. Absence of a published proponent is never a ground for omitting a
   `denial-set` member, never a ground for `DIA` = `FAIL`, and never a ground for
   `ER-706`, whose clause about a member no standing position holds is read as
   excluding only members no one *could* hold. *Reviewer test:* remove each
   `denial-set` member and each non-member load-bearing premise in turn; if a
   premise outside the set breaks a step, the set is not minimal-and-complete,
   and a `denial-set` of wholly citable members with an uncited load-bearing
   premise standing outside it is itself `DIA` = `FAIL`.
4. **Two-part apparatus.** The bibliography divides into *Sources* (works quoted
   or located, per §13.3) and *Positions engaged* (literature supporting the MD9
   opponent statements). Both take the same locus discipline; neither warrants.

### 13.7 Decisions taken where the spine is silent

The margin set is closed at ten tokens, so the six classes are **not** margin
callouts: `CC-*` is an inline family with the printed markers of §13.2, and the
only margin tokens marking a provenance hazard are `RISK` (per the `RISK`→`PRV`
mapping of §11) and `OBJ`. The `scholion` field is fixed as the sole
proof-object field admitting `CC-TEXT` or `CC-REV` content (§13.8). The
theological remark block is a new printed environment, named and styled by the
production section subject to §13.4's placement rule.

### 13.8 Bounds on textual passages

1. **One channel.** The only printed home for textual material outside a
   footnote's bibliographic apparatus is the `scholion` environment — what
   §13.2's "historical prose" and "passage explicitly marked as historical"
   name, and which no `steps` line may cite. Footnotes carry loci, editions,
   translators, and variant readings only, never a reported argument.
2. **No inference.** A textual passage may report what an author wrote, where,
   and how the book's own reconstruction differs. It may contain no inference
   marker joining two of its own sentences, and no premise-conclusion
   presentation of the source's reasoning.
3. **Cap and route.** A textual passage may not exceed 120 words. Where a
   source's own argument must be shown, it is entered as a reconstructed
   `PF-###` with a full audit and referred to by id.
4. **Excision.** The excision test of §13.4 is extended to delete every textual
   passage as well. If any claim the chapter relies on is then unsupported, or
   the chapter's persuasive weight visibly shifts, `PRV` = `FAIL`.


## 14. Declared Framework and Neutrality Policy

Neutrality here is not refusal to hold positions and not equal airtime. It is
one discipline: **every place the book's own metaphysics is doing work is visible
from the page, in a token a reviewer can check.** The book may argue for
Aristotelian-Thomistic conclusions as hard as it likes; it may never let `AT`
vocabulary act as a silent premise, nor let declaring a framework substitute for
warrant.

This section fixes `framework-status` values (`FS-*`), adds a `PF-###` field
`framework-role` (`FR-*`), an `OB-###` field `target` (`RJ-*`), and an `RP-###`
field `disposition` (`RD-*`). No margin token, identifier prefix, warrant token,
axis, or verdict is minted; §11 (margin set), §10.1 (identifiers), §2.1.2
(warrants), §6.2 (axes), and §6.3 (verdicts) remain closed.

### 14.1 The declaration

**N1.** The book prints a **Framework Declaration** in front matter before
Chapter 1 and reprints its posit table as an appendix: a table plus six numbered
clauses, never a discursive preface. It MUST contain, checkable item by item:

1. The framework's name and the exact token used in the `framework` field
   (`AT`), plus the name of every other framework token the book will use.
2. A closed, numbered table of the framework's **posits**: every `PR-###` whose
   ledger `kind` is `FRAMEWORK-POSIT`, with `statement`, `modality`,
   `modal-scope`, `import`, `introduced-at`, `consumed-by`. Closed means no
   proof object may carry a `W-POST` premise absent from this table; detection
   is a reviewer scan of every `W-POST` premise against it.
3. For each posit, its disposition in this book: `POSITED` (`warrant: W-POST`,
   never argued for here) or `ARGUED` (cites the `PF-###` that undertakes to
   establish it; see N8). Both are permitted. Silence is not.
4. For each posit, which named rivals reject it, pointing into the rival
   register (§14.5). A posit no named rival rejects MUST say so.
5. **The anti-warrant clause, in the book's own voice.** Declaring a framework
   confers no warrant on anything in it. `W-POST` records *that* the framework
   accepts a premise; it discharges MD4 while contributing nothing to premise
   truth. A reader who rejects the posits may read every `FR-INTERNAL` result as
   a conditional and lose nothing the book claims to have shown.
6. A statement either naming at least one rival framework in which some named
   demonstration of the book could be reconstructed, or stating that no such
   reconstruction is known to the author.

These six items are cited as N1(1)–N1(6).

**N2.** The Declaration contains no argument and no sentence of it may function
as a premise.

**N3.** Citing it in a `steps` line or `warrant` field is `PRV` = `FAIL`.

### 14.2 Marking framework-dependent premises

**N4.** `framework-status` (§4.3) takes exactly one of three values.

| Value | Holds when | Warrant it may carry |
|---|---|---|
| `FS-NEUTRAL` | a competent adherent of every rival in the register would grant the sentence *under the declared sense selector*, whether or not on the book's grounds | `W-SELF`, `W-DEF`, `W-IND`, `W-EMP`, `W-DEM` from `FS-NEUTRAL` ancestry |
| `FS-EARNED` | framework-laden content the book has established from `FS-NEUTRAL` premises | `W-DEM` only, citing an `FR-CONSTITUTIVE` `PF-###` |
| `FS-INTERNAL` | only a reader already committed to the declared framework would grant it | `W-POST`, or `W-DEM` from a chain containing one |

**N5. Posit-deletion test (binding detector).** Delete (a) every `W-POST`
premise; (b) every id whose `depends-on` closure contains one; (c) every
`TM-###.n` sense line, `DF-###`, and `DS-###` classified `FS-INTERNAL`, together
with every premise whose `warrant` is `W-DEF` on a deleted definition and every
`commitments` row licensed by a deleted id. Where a deleted sense line has an
`FS-NEUTRAL` sibling sense of the same term, re-run the argument on that sibling
under MD2. If `claim` no longer follows, or follows only in a weaker modality,
scope, or import, a load-bearing element is `FS-INTERNAL` whatever the records
say, and a record saying otherwise is `FRM` = `FAIL`. Deletion by warrant token
alone is not the test: a posit carrying no warrant token because it was entered
as vocabulary is exactly the case this detector exists to reach.

**N6. Marking mechanism, three places, no exceptions.** (a) *Proof object:*
`framework-status` on every premise subrecord; `contested: true` on every
`FS-INTERNAL` premise; `framework: AT`. (b) *Ledger:* `kind: FRAMEWORK-POSIT`,
`warrant: W-POST`, `framework: AT`, and a non-empty `objections` list. (c)
*Margin:* each `FS-INTERNAL` premise carries, at first occurrence in a chapter,
an `OBJ` callout citing the `OB-###` recording the strongest rival rejection of
it; a line incurring the ontological commitment separately carries `IMPORT`; if
both fall on one line `OBJ` wins (§11 caps callouts at one per line). An
`FS-INTERNAL` premise with no `OBJ` callout in its chapter is `FRM` = `FAIL`.

**N7. Posits may not hide in definitions.** A `DF-###` only a committed reader
would grant is a posit in a definition's clothes. *Worked micro-example.*
`DF-###` "change is the actualization of a potency by something already actual"
is inadmissible as a definition: it embeds three `AT` posits. Admissible split —
`TM-012` *change*, sense `.1`: a thing's bearing a property at `t₂` that it
lacked at `t₁` (`FS-NEUTRAL`); `PR-057` "every change is the actualization of a
potency" (`kind: FRAMEWORK-POSIT`, `warrant: W-POST`, `import: REAL`, `FS-INTERNAL`,
Humean and physicalist rejections registered). Any proof consuming `PR-057` is
thereby `FR-INTERNAL` unless `PR-057` is `ARGUED`. *Detection:* `LC-08` for the
definitional form, `LC-18` for the sense form — a `TM-###.n` sense line only a
committed reader would grant — and N5(c) as the test that runs on the page when
neither check has been run.

### 14.3 Within the system versus establishing the system

**N8.** Every `PF-###` carries `framework-role`, required whenever `framework ≠
NEUTRAL`, printed in the proof header:

| Token | Meaning | Binding constraint |
|---|---|---|
| `FR-NEUTRAL` | uses no `FS-INTERNAL` premise | asserting it with an `FS-INTERNAL` premise present is `FRM` = `FAIL` |
| `FR-INTERNAL` | a demonstration **within** the system | `established` MUST be conditional (N10); MUST NOT be described as supporting, confirming, vindicating, or motivating the framework |
| `FR-CONSTITUTIVE` | a demonstration intended to **establish part of** the system: `claim` is itself a framework posit or entails one | **every** premise MUST be `FS-NEUTRAL` or `FS-EARNED`. One `FS-INTERNAL` premise makes the role `FR-INTERNAL`, full stop |

The `FR-NEUTRAL` / `FR-INTERNAL` / `FR-CONSTITUTIVE` set is closed and owned by
this section; the proof-object section (§4.2) adopts it verbatim and mints no
token of its own.

**N9. The non-promotion rule.** An `FR-INTERNAL` demonstration may never be
presented as establishing any part of the framework — not partially, not
inductively, not by cumulative-case language. Doing so is `FRM` = `FAIL`,
routed to `V-REPAIR`; the repair is reclassification plus deletion of the
confirmatory language. *Reviewer test:* an `FR-INTERNAL` proof whose `claim` or
`established` mentions a Declaration posit is presumptively in violation, and
the author must show the mention is a use, not a support.

**N10. Discharge.** A posit moves from `POSITED` to `ARGUED` only by a cited
`FR-CONSTITUTIVE` proof with verdict `V-PASS` or `V-PARTIAL`. Consumers then
record the premise `FS-EARNED` with `warrant: W-DEM`. Until then every consumer
is `FR-INTERNAL`, and the rubric returns `V-OPEN`: an `FR-INTERNAL` object
consuming a posit still marked `POSITED` is an additional disjunct of verdict
rule 4, stated in §6.3. A discharge resting on a merely `V-PARTIAL`
`FR-CONSTITUTIVE` proof carries that verdict to every consumer through the
inheritance rule of §6.5, and does not remove the conditionality note of N11.

### 14.4 Internal validity versus external acceptance

**N11.** Every `FR-INTERNAL` proof prints, immediately below `established`, a
**conditionality note** in this fixed form:

> Established within `AT`, on posits `PR-057`, `PR-061`. A reader who rejects
> `PR-057` — see `OB-023`, the Humean rejection at its strongest — incurs no
> commitment to this conclusion. Nothing in this demonstration bears on the
> truth of `PR-057`.

Slots: framework token; every `FS-INTERNAL` premise by id; for each, one named
rival with its `OB-###`; the closing disclaimer. A missing or truncated note is
`FRM` = `FAIL`. The note is body text, never margin: it states the standing of a
result and so is argument, not annotation.

**N12.** Internal validity is never evidence of external acceptability. Arguing
from the coherence, fruitfulness, or elegance of `AT` to the truth of a posit is
admissible only as an explicit `FR-CONSTITUTIVE` `PF-###` with `kind:
DIALECTICAL`, `rung: RG-VALID` at most, carrying an `OB-###` for the
underdetermination objection.

### 14.5 Rivals: the register and the rejection-target requirement

**N13.** The book maintains a **rival register**, printed once and keyed by
position name (positions are named, objections are numbered; no prefix is
minted). Minimum entries: nominalism, Humeanism about causation and necessity,
physicalism, contemporary modal theories (at least modal fictionalism and one
realist competitor), and standard analytic objections (grounding deflationism
and ontological deflation at minimum). Fields: position name; the commitment it
denies, by
`PR-###`/`DF-###`/`DS-###`/`TM-###.n`, the last where the target is `RJ-DEF` or
`RJ-SENSE`; its own positive alternative account; at least one source in which
an *adherent* defends it; the `OB-###` ids that carry it.

**N14. Rejection target.** Every `OB-###` attributed to a named position carries
`target`, exactly one token, plus the id it attaches to:

| Token | The rival | Attaches to | Axis | Responsive reply must |
|---|---|---|---|---|
| `RJ-PREM` | denies a premise | `pid` / `PR-###` | `WAR` | give warrant for that premise, or concede |
| `RJ-INF` | grants premises, denies a step | `PF-###.k` | `LOG` | exhibit the rule application, or repair the step |
| `RJ-SENSE` | grants the sentence under another sense | `TM-###.n` | `SEM` | show the argument runs on one sense throughout |
| `RJ-IMPORT` | grants the sentence, denies `import: REAL` | premise or `claim` | `ONT` | pass the MD5 paraphrase test explicitly |
| `RJ-MODAL` | grants the sentence at a weaker `NEC-*` or other `SCP-*` | premise | `MOD` | cite the `BR-###`, or lower the recorded modality |
| `RJ-SCOPE` | grants all, denies `established` reaches `claim` | `claim` | `SCO` | narrow `established`, or license the width |
| `RJ-GROUND` | grants `RG-THAT`, denies the middle grounds | `middle` | `EXP` | supply the reversal test and stripped variant, or drop to `RG-THAT` |
| `RJ-DEF` | grants the argument under the declared sense, but denies that the declared sense is the one at issue, or holds that the sense builds the disputed thesis in | `TM-###.n` / `DF-###` / `DS-###` | `WAR` | derive the sense's contested content as a `PR-###` with its own warrant, or concede that the result is `FS-INTERNAL` and reclassify `framework-role` |

`RJ-SENSE` covers only the charge of equivocation between two senses of one
term. Where the complaint is that a single stable sense was stipulated so as to
make a disputed premise analytic, the target is `RJ-DEF`, and recording such an
objection as `RJ-SENSE` is misclassification: `DIA` = `FAIL` under N15. Against
`RJ-DEF`, showing that the argument runs on one sense throughout is
non-responsive.

**N15.** Misclassifying the target is a defect, not a presentation choice:
`DIA` = `FAIL`, as is a reply addressing a target other than the one recorded
(**non-responsive**). *Worked pair.*
The Humean objection to "whatever comes to be has a cause" is `RJ-MODAL` on the
premise (the regularity is granted; `NEC-MET` is denied, `NEC-NOM` at most
allowed) — answering it by re-deriving the conclusion validly is non-responsive.
The quantifier-shift objection to "each thing has a cause, therefore something
causes each thing" is `RJ-INF` — answering it by defending the premise's truth
is equally non-responsive. Two rivals, two defects, one root: the book did not
say what was being rejected.

### 14.6 Anti-straw-man standard and enforcement

**N16. Adherent-assent standard.** A rival is admissibly stated only if a
competent contemporary adherent, reading it cold, would sign it as their own
view without asking for charity. Not "would recognise", not "would concede is
close": **would sign**.

**N17. Reviewer tests for violation.** Any one failing is `DIA` = `FAIL`.

1. *Adherent-source test.* The register entry cites a source in which an
   adherent defends the position. A rival sourced only to its critics fails
   automatically.
2. *Reason test.* The statement gives the rival's own reason, not merely its
   denial. "The nominalist simply denies universals" fails.
3. *Strongest-form test.* The reviewer attempts, from the cited literature, a
   stronger version of the rival's reason. If one exists and the `RP-###` does
   not address it, the statement fails.
4. *Disowned-consequence test.* If the reply's first move attributes to the rival
   a consequence adherents explicitly disown, it fails.
5. *Reciprocity test.* The book's own posits must be stated so that a rival
   would accept the statement as accurate. The standard is symmetric.

**N18. Screening heuristic, not itself a defect.** A rival stated in materially
fewer words than the reply answering it triggers mandatory test 3.

### 14.7 Open objections as a permitted and sometimes required outcome

**N19.** Every `RP-###` carries `disposition`: `RD-ANSWERED` (the objection is
shown to fail, with the argument given) · `RD-COSTED` (granted as a real cost;
`claim` stands with `not-established` enlarged or `modality` lowered) ·
`RD-CONCEDED` (the objection succeeds against the proof as stated; audit routes
to `V-REPAIR` or `V-FATAL`) · `RD-OPEN` (the book has no answer it will defend;
the objection stands).

**N20.** `RD-OPEN` is permitted anywhere and **required** whenever N17.3 yields
a version of the rival the book cannot answer. Answering a weakened version
instead is the gravest dialectical defect available to this book: `DIA` =
`FAIL`, and the manufactured win is deleted, not repaired. An `RD-OPEN` reply
still exists (§4.2 requires 1:1) and states what would have to be shown to close
it, naming the missing `PR-###` stub. An `RP-###` carrying `RD-OPEN` is an
additional disjunct of verdict rule 5, stated in §6.3, so the rubric returns
`V-PARTIAL` — or `V-OPEN`, rule 4 matching first, when the contested item is a
`W-POST` premise.

**N21. Chapter-level review trigger.** A chapter in which every disposition is
`RD-ANSWERED` is not thereby defective, but its reviewer MUST run N17.3 against
every `OB-###` in it before signing off. Manufacturing concessions for the
appearance of balance is a reciprocity failure in the other direction.

### 14.8 Exit standard

The reader must finish better able to say where disagreement actually lies — a
property of the printed text, tested rather than asserted.

**N22. Locus test (reviewer, per Part).** Using only printed text and no
knowledge of their own, the reviewer fills in, for each rival named in the Part:
*position · the exact id rejected (`PR-###`, `DF-###`, `DS-###`, `TM-###.n`,
`PF-###.k`) ·
`RJ-*` token · the rival's own reason, quoted · `RD-*` disposition*. Any cell
needing reviewer-supplied knowledge fails the Part. A rival named anywhere with
no complete row anywhere is name-dropping: `FRM` = `FAIL`.

**N23. Signature test.** Take any three consecutive pages of framework-laden
argument and ask which sentences a competent nominalist would sign. If the pages
furnish no way to answer — no `framework-status` marks, no `OBJ` callout, no
conditionality note in scope — `FRM` = `FLAG` at minimum.

**N24. Reader-side test (constraint on the exercise system).** Each Part MUST
contain at least one exercise whose solution is an id plus an `RJ-*` token, the
solution explaining why the neighbouring targets are wrong. The exercise section
owns the verb and difficulty ladder; this is a coverage floor, not a format.


## 15. The First Vertical Slice

### 15.1 Subject matter, and why this one

The slice is built on **one designated particular and one modal predicate**: an
unbroken drinking glass, `a`, and the predicate *can shatter*.

The choice is argued, not assumed:

1. **Genuinely metaphysical, not a disguised logic exercise.** "This glass can
   shatter" is uncontested; everything at issue lives in the declared fields — is
   the possibility `POS-CON`, `POS-NOM`, or `POS-MET`; is `import` `LINGUISTIC`
   or `REAL`; is the modality predicated `SCP-DIV` of the glass or only `SCP-CMP`
   of a conditional. Lewisian counterpart-theoretic Humeanism, best-system law
   theory, and modal quasi-realism deny the answers this slice gives, each for
   its own reason: the dispute is live, locatable, not about the sentence.
2. **Bounded.** The subject is one particular, so no universal quantifier can
   quietly widen; the conclusion reaches `POS-NOM`, so the interesting slide from
   conceivability to real possibility sits one line beyond the demonstration,
   where the reader can see it refused.
3. **Carries the book's later machinery in embryo** — potency, the divided sense,
   the nomological/metaphysical boundary, the sign/ground contrast — at a scale
   where the reader holds the whole proof object in view.
4. **Not an argument for the existence of God**, and `not-established` (15.2)
   blocks every route out of it toward one.

The slice is organized around **two near-neighbour pairs**, one of form (valid /
invalid, M1–M2) and one of metaphysical modality (correct / defective, M5 vs M8).
This parallel is the slice's pedagogical spine and MUST be visible in its section
ordering.

### 15.2 The bounded claim, and the stronger claims it does not reach

`PR-501` — `claim`, one sentence, immutable once `ACTIVE`:

> This glass, while unbroken, can shatter.

with `subject: this glass (a)` · `attribute: can shatter` · `import: REAL` ·
`modality: POS-NOM` · `modal-scope: SCP-DIV` · `rung: RG-THAT` ·
`middle: differential outcome of matched treatment` · `middle-kind: EFFECT-SIGN`.
`framework` is **computed, not chosen**, by §14.2 N4: `AT` if any premise of
`PF-503` is `FS-INTERNAL`, `NEUTRAL` only if every premise is `FS-NEUTRAL` under
the every-rival-would-grant-it test.

The same eight-word sentence recorded with `import: LINGUISTIC` and
`modality: POS-CON` is a **different proposition** with a different id: the slice
says so in one sentence, and thereby why ids attach to records, not sentences.

`not-established` — printed in full, each with the discipline that blocks it:

| Stronger nearby claim | Blocked by |
|---|---|
| The possibility is grounded in an intrinsic potency of `a` rather than in `a` together with the laws and its surroundings. | No premise supplies a grounding claim, and nothing isolates `a` from its circumstances; axis `ONT`. |
| `a` contains a potency `DK-REAL`-distinct from its actual constitution. | No separation or entailment test is run; at most `DK-VIRT` is in evidence. |
| Act and potency are the composing principles of every changeable thing. | `subject` is one particular; `SCO`. |
| Whatever is in potency is reduced to act only by something already in act. | Not a consequent of anything above. |
| *Why* `a` can shatter. | `rung: RG-THAT`; the middle is a sign. |

**The modal ordering, binding on every element of the slice.** Nomological
possibility entails metaphysical possibility: whatever the actual laws permit is
metaphysically possible. `POS-MET` is therefore *weaker* than `POS-NOM`, not
stronger; no bridge from `POS-NOM` to `POS-MET` exists or is needed, and no
element of this slice — row, callout, audit, exercise, or solution — may present
that move as a strengthening or its absence as a defect. The slice's designated
modal defect runs the other way, `POS-CON` → `POS-MET` (M8), where a bridge is
required and absent.

### 15.3 Identifier allocation, and two decisions the spine leaves open

The slice is **chapter `00`**, permanently reserved; no curriculum chapter may
later claim `EX-00.##` / `SO-00.##`. Every ledger id in the slice is drawn from
**500–519 in its class**, inside the coordinator reserve of §8.6(1), which no
curriculum stage may allocate. If the slice is later absorbed into a chapter, its
content is re-entered under fresh ids from that chapter's band and every `5##`
record is set to `status: SUPERSEDED` with `superseded-by` naming the new id; a
`5##` id is never promoted into a curriculum band. The slice's ids lying outside
the Stage A–C bands, the numeric crossing rules keyed on `PF-060` (`import:
REAL`) and `PF-090` (`framework: AT`, `W-POST`) do not govern it; the slice
states its `import` and `framework` explicitly instead, and still prints the MD5
test and the `OBJ` callout those crossings require.

| Id | Kind | Role |
|---|---|---|
| `PF-501` | `DEMONSTRATION` | valid near-neighbour (`RG-VALID`) |
| `PF-502/S` | `SPECIMEN` | invalid near-neighbour |
| `PF-503` | `DEMONSTRATION` | the bounded demonstration of `PR-501` |
| `PF-504` | `DEMONSTRATION` | the `RG-WHY` contrast, ≤ 4 lines |
| `PF-505/S` | `SPECIMEN` | the plausible but incorrect variant |
| `PF-506` | `DEMONSTRATION` | the repaired form |
| `PF-507/S` | `SPECIMEN` | the perturbed variant printed inside `EX-00.10` |
| `PR-502` | `FRAMEWORK-POSIT` | the bridge posit exposed by the repair, `W-POST`, `framework: AT` |

**Decision (spine silent):** items occurring only inside a `kind: SPECIMEN` proof
object — its definitions and premises — are **not** allocated `DF-###` / `PR-###`
ledger ids. They are addressed as `PF-505/S.d1`, `PF-505/S.p4` (premise-local `pid`
per §4.3), unambiguous against numeric step references `PF-505/S.4`: the ledger
must not carry content the book rejects, and `LC-03`/`LC-09` would misfire on
it.

**Decision (spine silent):** the slice cites error classes by **name and axis**
and MUST NOT invent an `ER-###` number; the production agent substitutes the
number the taxonomy assigns. The slice requires exactly three named classes: *affirming the consequent* (`LOG`), *conceivability taken for
possibility* (`MOD`), *conclusion stronger than the demonstrated result* (`SCO`).

### 15.4 Required contents

Each row is mandatory; the acceptance condition is what a reviewer checks, and a
row whose condition fails is a slice failure, graded by 15.8.

| # | Element | Acceptance condition |
|---|---|---|
| M1 | One trivial valid argument, `PF-501` (`kind: DEMONSTRATION`, `rung: RG-VALID`): "if `a` is struck with force `f`, `a` shatters; `a` is struck with force `f`; so `a` shatters." | Printed at `L2-NUM` and `L3-SKEL` (`P → Q, P ⊢ Q`); every step names its rule; `logic` declared. Same subject matter as M3; an unrelated toy example fails. The verdict is whatever §6.3 first-match computes. |
| M2 | One nearly identical invalid argument, `PF-502/S`: same first premise, "`a` shatters", so "`a` was struck with force `f`". | Differs from `PF-501` by one line; a countermodel (thermal shock) is exhibited, not merely a fallacy named; `LOG` = `FAIL`; `kind: SPECIMEN`. |
| M3 | The bounded demonstration, `PF-503`, all `MUST` fields of §4.2 populated. | Passes MD1–MD10; `rung: RG-THAT` claimed and achieved; MD5 paraphrase detector run **in print**, the conceptual rewrite shown failing. |
| M4 | `L1-PROSE` of `PF-503`. | Fixes which sense of "can" is live and why the question arises; no "so"/"hence"/"must" presented as licensing anything (§5, rule (i)). |
| M5 | `L2-NUM` of `PF-503`: ≥ 5 and ≤ 9 numbered lines. | Every premise carries `warrant`, `modality`, `modal-scope`, `import`, `framework-status`, `contested`. The composite-to-divided transition is either **licensed** — a cited line naming the licensing `BR-###`, that bridge's licensing condition discharged inside `PF-503` and the discharge printed on the same page — or **disclaimed**: if the move is instead an ordinary distribution of the possibility operator over a composite conditional plus a cited possibility premise, the line says so in one clause and cites no bridge, and the `MODAL` anchor of 15.5 moves to the line fixing the necessity kind. Neither cited nor disclaimed fails. |
| M5b | `PF-504`, the `RG-WHY` contrast: `a` shattered *because* a crack propagated under tension (`middle-kind: EFFICIENT`, `PRI-GND`), with its stripped variant (the breakage alarm sounded — `EFFECT-SIGN`, `RG-THAT`). | Prints `rung`, `middle`, `middle-kind`, the middle's `PRI-*` token, `stripped-variant`, `established`, `not-established`, and what the stripped route leaves unexplained; reversal detector printed with both readings; makes visible why `PF-503` is `RG-THAT`. Graded by G11b. |
| M6 | `L3-SKEL` of `PF-503` plus its one-sentence `fidelity`. | Never printed without `L2-NUM` beside it; possibility operators carry their kind subscript; `fidelity` names at least that the calculus has no resource for the `POS-CON`/`POS-MET` distinction or for any `PRI-*` token. |
| M7 | Margin callouts. | All ten §11 tokens appear ≥ 1 time, anchored per 15.5; ≤ 5 per page, median 3; every `FLAG`/`FAIL` row in M14 has a callout on its line; the §11.6 deletion test passes. |
| M8 | The incorrect variant, `PF-505/S`: `PF-503` plus one further line applying the printed definition `DF-501` — *can* = conceivable without contradiction, the `TM-501.2` (`POS-CON`) sense — to license "so this glass can shatter" read at `TM-501.4` (`POS-MET`), `SCP-DIV`, and thence "so there is in this glass a real potency to shattering." | **Formally valid** — `LOG` = `OK`: the extra line is a substitution instance of a definition printed and accepted earlier, so a reader who has read M3 must be able to accept it. The slide `POS-CON` → `POS-MET` requires the conceivability–possibility bridge (`W-POST`) and cites none. |
| M9 | Localization. | Names exactly one line (`PF-505/S.7`), the definition and the premise line applying it (`PF-505/S.d1` / `PF-505/S.p6`), one field — the `TM-501.n` sense selector both carry — one primary axis (`MOD`), one error class (15.3), one consequent axis (`SCO`). Excision test: correcting that selector alone removes the defect and changes nothing else. |
| M10 | Repair, `PF-506`, in **two routes**: (A) minimal — restore the `TM-501.2` selector, so the line concludes at `POS-CON` only, and drop the real-potency line, leaving `PF-503`'s `established` standing; (B) retain the `POS-MET` reading and the potency line by promoting the conceivability–possibility bridge to `PR-502`, `W-POST`, `framework: AT`, on which §6.3 rule 4 computes `V-OPEN`. | The surviving conclusion printed verbatim under each route. Route A's `claim` is strictly weaker than `PF-505/S`'s (G9). Route B is not the recommended route; the text says which dispute it relocates rather than settles. |
| M11 | Exercises, per 15.6. | 10 ≤ items ≤ 24; ≥ 4 verbs from the closed thirteen of §9.2; all three functional families of 15.6 — diagnose, adjust, construct; ≥ 3 tier tokens of §9.4; ≥ 3 items on material printed nowhere in the slice body. |
| M12 | End-of-slice solutions `SO-00.##`. | Collected at the end, numbered identically to their exercises; concise for diagnostic items, full proof objects for construction items; each cites ≥ 1 axis token, declares one answer mode (§9.7.2), and from `T2-LOCALIZATION` up carries the §9.7.1 `audit-delta` line; alternates named where a defensible alternative exists. |
| M13 | ≥ 1 dependency diagram over `PF-503` and `PF-505/S`. | Two distinguishable edge types (`depends-on`, warrant); shows what the numbered form does not — the absent `BR-###` as a gap, `PR-502` as a leaf with no incoming edge; legible in grayscale; no meaning by colour alone. |
| M14 | ≥ 3 completed audit tables: `PF-503`, `PF-505/S`, `PF-504`. | Fourteen rows each, §6.2 order, every row marked; verdicts computed by §6.3 first-match, never chosen. **No verdict is mandated for `PF-503`:** it is whatever the first-match rules compute from the marks, and if the premise named under G8 is `FS-INTERNAL` and load-bearing, rule 4 fires and the printed verdict is `V-OPEN` with that premise and the live positions on each side. `V-PASS` is not a target, no premise's `warrant` or `framework-status` may be chosen so as to reach it, and a `V-OPEN` slice is a passing slice. `PF-505/S` carries a `FAIL` at `MOD` by construction (M9) and prints its computed verdict's extra fields; `PF-504`'s table is graded by G11b. |
| S1 | Lexicon block: `TM-501` *can* (senses `.1` epistemic, `.2` `POS-CON`, `.3` `POS-NOM`, `.4` `POS-MET`), `TM-502` *shatter*, `DF-501` (glossing `TM-501.2`), `DS-501` (`DK-REAL` / `DK-VIRT` / `DK-NOM`). | Every technical term in any printed `claim` has a `TM` id and a sense selector at each occurrence (`LC-11`). |
| S2 | `OB-501`–`OB-503` with `RP-501`–`RP-503`. | ≥ 1 objection is the counterpart-theoretic Humean at full strength; ≥ 1 reply concedes. |
| S3 | Ledger extract for `PR-501`, `PR-502`, `TM-501`. | All §10.2 keys present; `strength-history` shows the `POS-NOM` entry and, for `PF-505/S`, the `POS-CON` → `POS-MET` entry that `LC-05` catches. |

### 15.5 Margin token anchors

All ten tokens of §11, at minimum:

| Token | Anchor |
|---|---|
| `DEF` | the line of `PF-503` where `TM-501.3` is selected |
| `DIST` | `DS-501` where `DK-VIRT` is distinguished from `DK-REAL` |
| `INF` | the `L3-SKEL` line of `PF-502/S` where the shape diverges |
| `IMPORT` | the `W-EMP` premise asserting `a`'s existence |
| `MODAL` | the composite-to-divided line of `PF-503` under M5(a), or the line at which the necessity kind is fixed under M5(b); and again on `PF-505/S.7` (`POS-CON` → `POS-MET`) |
| `WHY` | the grounding middle of `PF-504` |
| `RISK` | the `L3-SKEL` line where a kind-subscripted operator is not an operator of the declared calculus |
| `OBJ` | the premise `OB-501` targets |
| `SCOPE` | the last line of `PF-503`, naming what is not thereby established |
| `USES` | the `PF-506` line consuming `PR-502` |

### 15.6 Exercises

Ten items, `EX-00.01`–`EX-00.10`, each printed with the full §9.1 header. Verbs
are the closed thirteen of §9.2 and **no verb may be invented for the slice**;
tiers are the tokens of §9.4; `product` narrows the §9.2 product for the verb.

| Id | `tier` | `verb` | `target` | `axes` | `product` |
|---|---|---|---|---|---|
| `EX-00.01` | `T2-LOCALIZATION` | LOCATE THE FAILURE | `PF-505/S`, `L2-NUM` reprinted without commentary | `BLIND` | the `PF-505/S.k` line, the §4.2 field, one axis marked `FAIL`, the `ER-###`, one sentence |
| `EX-00.02` | `T4-CONSTRUCTION` | AUDIT | `INLINE`: a four-line `RG-WHY` candidate, printed as a stated perturbation of `PF-504` | all fourteen | fourteen rows in §6.2 order, the computed verdict, its extra fields |
| `EX-00.03` | `T2-LOCALIZATION` | DE-FORMALIZE | one `L3-SKEL` line of `PF-503` | `FID`, `SEM` | the back-translation, the `FID` mark, and whether the author would assert it |
| `EX-00.04` | `T3-INTERVENTION` | WEAKEN THE CONCLUSION | `INLINE`: unseen argument concluding "every material thing can be destroyed" | `SCO` | `established` rewritten at the licensed strength, plus the new `not-established` entry |
| `EX-00.05` | `T2-LOCALIZATION` | FIND THE HIDDEN PREMISE | `INLINE`: unseen argument on an undeclared `SCP-CMP`/`SCP-DIV` equivocation | `WAR`, `MOD` | the premise subrecord (§4.3), the step it repairs, whether it is `contested` |
| `EX-00.06` | `T3-INTERVENTION` | PROVIDE THE MISSING BRIDGE | `INLINE`: a perturbed `PF-505/S`, its conceivability premise on another predicate | `MOD`, `DEP` | the `BR-###` licensing `POS-CON` → `POS-MET`: antecedent, consequent, §2.1.2 warrant token, discharge point, and the position that denies it |
| `EX-00.07` | `T3-INTERVENTION` | REFUTE | `PR-501` | `DIA`, `FRM` | an `OB-###` at full strength in ≤ 4 lines, with the named position's own reason, plus the `denial-set` member it would add |
| `EX-00.08` | `T1-RECOGNITION` | CLASSIFY | `TM-501`, four printed uses of *can* | `SEM`, `MOD` | per use: the sense token `.1`–`.4`, the §3.9 deciding test in one sentence, the rival sense rejected |
| `EX-00.09` | `T2-LOCALIZATION` | MINIMIZE | `PF-503`, its premise set | `DEP`, `DIA`, `ONT` | the reduced premise set, each deletion justified by "no step consumes it", the survivor carrying `import: REAL`, the resulting `denial-set` |
| `EX-00.10` | `T4-CONSTRUCTION` | REPAIR | `PF-507/S`, printed in the item | `BLIND` | asked in the uniform §9.8.1 wording — "Repair `PF-507/S`, or show, by exhibiting one weakening of `established` and one added premise, that no repair preserves a `REAL` conclusion, and state what survives" — answered by the minimal edit with changed fields in full, the verdict, `survives` |

Functional families exercised, the three the slice recognizes: **diagnose** (01,
02, 03, 08), **adjust** (04, 05, 06, 09, 10), **construct** (07). Every T3+ item
targets material not printed in the slice body (§9.6.3).

### 15.7 Page budget

Target **13.75 rendered pages**; budget rejection is G13 and nothing else.

| Element | Pages | Element | Pages |
|---|---|---|---|
| Frame and reading map | 0.25 | S2 objections / replies | 0.75 |
| M1 + M2 pair | 0.75 | M14a audit table `PF-503` | 0.75 |
| S1 lexicon, claim, domain | 1.00 | M8 variant `PF-505/S` | 0.75 |
| M4 `L1-PROSE` | 0.50 | M9 localization + M14b | 1.00 |
| M5 `L2-NUM` | 1.25 | M10 repair, routes A and B | 0.75 |
| M5b `PF-504` + M14c its table | 0.75 | M11 exercises | 1.75 |
| M6 `L3-SKEL` + `fidelity` | 0.75 | M12 solutions | 2.00 |
| M13 dependency diagram | 0.50 | S3 ledger extract | 0.25 |

### 15.8 The acceptance gate

Gates are run in order. **G1–G12, including G1b, G5b, and G11b, are
intellectual; G13–G14 are typographic.** Each is a failure condition with the
test the reviewer runs.

| Gate | Fails when | Reviewer test |
|---|---|---|
| **G1** merely valid | `PF-503` establishes only a conceptual or linguistic truth. | Run the MD5 paraphrase detector on `PR-501`. If the premises support "our concept of glass requires that it can shatter" with equal force, or if `PF-503`'s computed verdict is `V-VALID-ONLY`, reject. |
| **G1b** derivation unchecked | The derivations are taken on the strength of the slice's own marks. | Re-derive every numbered line of `PF-503` and of both repair routes against the rule it names in the declared `logic`, without consulting the submitted audit. Any step the named rule does not license, any modal line whose scope or necessity-kind token changes with no `BR-###` cited, and any cited `BR-###` whose licensing condition is not discharged inside the same object, rejects the slice. |
| **G2** obvious error | `PF-505/S` would deceive nobody. | (i) `PF-505/S` must be formally valid — `LOG` = `FAIL` rejects; (ii) its defective line must be licensed by a definition already printed and accepted earlier; (iii) its conclusion must be one the book's own framework wants true. Failing any, reject. |
| **G3** gesturing localization | M9 names a region rather than a point. | Excision test: replace exactly the named item; the defect must disappear and no other line change. Reject if M9 names two primary axes, or uses "somewhere", "equivocates", "trades on", or "conflates" without a line number and field name. |
| **G4** decorative margin | A callout adds no token the line already carries. | For each callout: does it introduce an id, a rule name, an axis-relevant hazard, or a named non-consequence absent from its line? If not, reject. Then the §11.6 deletion test; then check every `FLAG`/`FAIL` row has its callout. |
| **G5** recall exercises | An item is answerable by copying the slice. | Search the body for each solution's operative sentence; if present verbatim or near-verbatim, reject that item. Fewer than three items resting on material printed nowhere in the body rejects M11 entire. |
| **G5b** wrong solutions | A printed solution is wrong, or cites what does not exist. | Before reading the solutions, work all ten items independently and record an answer for each. Every printed solution must match on the operative point — the line and field named, the axis marked, the `BR-###` id and warrant token cited, the weakened `established` — or must name the divergence as a stated defensible alternate with its discriminating consideration. An unmatched, unnamed divergence rejects the slice; a solution citing an id that exists in no closed table and no `ACTIVE` record is an automatic rejection. |
| **G6** mechanical audit | A table is filled to look complete. | Before reading the submitted tables, derive all fourteen marks for `PF-503` and `PF-505/S` independently from the §6.2 failure conditions, then compare row by row. Any divergence rejects the slice, whether the submitted mark is too kind or too harsh; an `OK` the reviewer cannot confirm counts as a divergence. `PF-503`'s table must further carry ≥ 3 non-`OK` rows, of which ≥ 2 are `FLAG` with a stated one-clause reason; fourteen `OK` rows reject on sight. `PF-505/S`'s `FAIL` rows must be exactly those M9 names — a surplus `FAIL` is a smear, a missing one is a miss. |
| **G7** overstrong conclusion | `established` exceeds what the weakest link licenses. | Identify the weakest premise's `modality`, `modal-scope`, `import`; `established` may carry none stronger. `not-established` holds ≥ 3 entries, ≥ 1 the claim a reader would have expected to be proved. `NONE` rejects. |
| **G8** unmarked framework premise | A premise a named standing position rejects is recorded `FS-NEUTRAL` or left blank. | Name the premise a Lewisian Humean rejects. It MUST carry `framework-status: FS-INTERNAL`; `warrant: W-POST`, or `W-DEM` from a chain containing one; `contested: true`; membership in `denial-set`; an `OBJ` callout citing the `OB-5##` recording the rejection; and a computed verdict reflecting §6.3 rule 4. A premise recorded `FS-NEUTRAL` while a named standing position rejects it is `FRM` = `FAIL` and rejects the slice. `PF-503` must also state whether its result stands inside a framework or establishes part of one. |
| **G9** cosmetic repair | The repair preserves the conclusion it should have weakened. | Route A must be strictly weaker than `PF-505/S`'s claim on modality, scope, subject breadth, or import. Test: describe a situation verifying `PF-506`(A) and falsifying `PF-505/S`. If none exists, reject. Route B presented as costless — without naming the posit, its warrant token, and its deniers — also rejects. |
| **G10** straw opponent | An objection is stated below its strongest form. | Compare `OB-501` to a one-sentence statement a competent Humean would sign. If it requires the opponent to deny an evident datum, or omits the best-system account of laws, reject (`DIA` = `FAIL`). |
| **G11** grammar untested | The slice does not exercise the machinery it exists to test. | All ten margin tokens present; all three audit tables complete; ≥ 1 diagram; the three-layer set `L1-PROSE` / `L2-NUM` / `L3-SKEL` printed for `PF-503`; `L3-SKEL` never alone. |
| **G11b** unexhibited why | The `RG-WHY` contrast is asserted rather than exhibited. | `PF-504` prints `rung`, `middle`, `middle-kind`, the middle's `PRI-*` token with an exhibited asymmetry witness, and a full audit whose `EXP` row is `OK` with a locus naming the middle. The reversal detector is printed as two complete sentences, the reason the converse fails stated in terms of the account of the middle, not of how the sentences read. The stripped variant is a valid derivation of `PF-504`'s own claim not routing through the middle, printed in `L2-NUM` with every rule named, followed by one sentence naming what it leaves unexplained; and deleting the middle from every line makes at least one line underivable. Failing any part rejects. |
| **G12** provenance | An authority or a revealed premise carries weight. | No `W-AUTH` or `W-REV` in any `DEMONSTRATION`; a canonical author appears only in `scholion` or a classified citation; no `scholion` is cited by a `steps` line. |
| **G13** budget | Total outside 12.0–15.0 pages, or an element over allocation by > 0.25. | Count rendered pages. |
| **G14** production | Colour-only meaning, grayscale-illegible callout, broken cross-reference, widow or orphan in a numbered proof, or a `L3-SKEL` derivation broken across a page turn from its `L2-NUM`. | Inspect the PDF in grayscale. |

### 15.9 Rejection rule

If **any of G1–G12** fails, the slice is **rejected as a whole and rebuilt, not
patched**. The reviewer classifies the failure as exactly one of two kinds, and
the disposition follows from the classification:

1. **Execution failure** — the mandated subject matter admits a compliant slice
   and this one was built badly. The lane re-derives every required element from
   scratch on the same subject matter; a patched-in-place resubmission is
   rejected without review.
2. **Subject-matter failure** — no compliant slice can be built on that subject
   matter: a variant nobody would believe, an audit table with nothing to say, a
   repair with nothing to weaken. The reviewer files an amendment against
   15.1–15.6 proposing replacement subject matter and the consequent rewrites;
   only the architecture lane may amend them.

A lane may not change the subject matter, the bounded claim, the id allocation,
or any acceptance condition on its own authority. An amendment proposing to
weaken a gate rather than to change the subject matter is out of order and
returned unread. Resubmission re-argues the subject matter under 15.1 and re-runs
all seventeen gates.

Failures of **G13–G14 alone** are recorded as a defect list and fixed in place,
the intellectual gates not re-run. Typographic excellence is evidence on none of
G1–G12 and may not be cited in mitigation of them.


## 16. Acceptance Criteria for Later Lanes

A lane's work is **accepted** only when every condition below that applies to it
is met. Conditions are stated so that a reviewer can mark each one met or not
met by inspection, without judgment of taste. Where a condition names a
detection method, that method is the reviewer's procedure; a reviewer who
rejects must cite the condition id and the locus.

**New identifier families declared here.** `LN-#` names a *process lane* and
`AM-###` a *spec amendment*. Neither is book content, so neither extends the
closed identifier scheme of §10.1; no `LN-#` or `AM-###` id ever appears in a
printed page, a proof object field, or a ledger record.

### 16.1 Lane inventory

| Id | Lane | Deliverable | Exclusive resource boundary | Entry precondition |
|---|---|---|---|---|
| `LN-1` | Chapter authoring | Chapter prose for its assigned chapters, plus every `PF-###`, `OB-###`, `RP-###`, `TM-###`, `DF-###`, `DS-###`, and `PR-###` those chapters introduce, each with a complete ledger record (§10); `ER-###` and `BR-###` are consumed here, never minted (§7) | The source files of its assigned chapters and the ledger records it originates. MUST NOT edit another chapter, any `EX-##.##`/`SO-##.##`, any LaTeX class or style file, or a ledger record it did not originate | Spec frozen at a named version; every chapter in the coordinator-issued chapter-level `depends-on` list is `ACCEPTED`, so every consumed id exists and is `ACTIVE` |
| `LN-2` | Exercise and solution authoring | `EX-##.##` and `SO-##.##` pairs for its assigned chapters | Exercise and solution files. MUST NOT alter chapter prose, mint a `PR-###`, or change any `claim`; a needed proposition is requested from `LN-1` by amendment or escalation | The chapter is `ACCEPTED`; every id the exercises cite is `ACTIVE` |
| `LN-3` | LaTeX design and production | Document class, environments, margin apparatus, dependency-diagram and inference-tree macros, build configuration, and a rendered PDF | `.cls`/`.sty`/template/build files. MUST NOT edit a word of prose, a `claim`, a `not-established` entry, a callout's text, or an audit table cell — including to fix a bad line break | The §12 production requirements are frozen; at least the vertical slice's content is `ACCEPTED` |
| `LN-4` | Ledger tooling | Machine-readable ledger and executable implementations of `LC-01`–`LC-22`, each emitting record ids and a pass/fail line | Ledger data and check code. MUST NOT edit book content, and MUST NOT silence a check by relaxing it | §10 schema frozen. May run against fixtures before any chapter exists |
| `LN-5` | Editorial review | An acceptance or rejection notice (§16.7) per submission | Review notices only. Holds **no** content resource: a reviewer never repairs the work under review, and a reviewer who edits a deliverable has thereby disqualified the review | The submitting lane declares completion and attaches its own §16.3 self-check with every item marked |

Lanes are serial where a precondition binds and parallel otherwise. Two lanes
never hold the same file. A need that crosses a boundary is an escalation
(§16.5), never a quiet edit.

### 16.2 Per-lane acceptance criteria

**`LN-1` chapter authoring.** Accepted iff: (1) every `PF-###` with
`kind: DEMONSTRATION` prints all `MUST` fields of §4.2, and `not-established`
and `denial-set` are non-empty; (2) every printed audit table has all fourteen
§6.2 rows in order, and the verdict equals what the §6.3 rules compute from
those marks — a reviewer recomputes from the marks and any divergence is a
rejection; (3) every premise carries exactly one §2.1.2 token; (4) every
`FLAG` or `FAIL` mark has a margin callout on the offending line, and the five
reviewer tests of §11.6 — deletion, overlap, transplant, page-budget, and
coverage, the last run as a row-by-row walk of the trigger column — all pass
over one sampled proof object per chapter and over any object the reviewer
spot-checks; a chapter in which a sampled callout fails the transplant test,
or in which any MUST-trigger is unfired, is rejected; (5) from Stage C onward
all three layers print, `L3-SKEL` never appears without `L2-NUM`, and each
`L3-SKEL` carries its `fidelity` sentence; (6) every technical term occurs
with a sense selector and appears in `lexicon`; (7) `LC-01`–`LC-22` report
clean when run over the accumulated ledger — every `ACCEPTED` chapter's
records plus the submitted delta — never over the delta alone, and a check
that cannot resolve a referenced id reports a hard error rather than skipping
it; (8) every §1.3 exit-profile item the chapter's assignment names is
exercised by some worked instance in the chapter; (9) the chapter's assignment
carries an explicit coordinator-issued chapter-level `depends-on` list, and
the chapter cites no id whose introducing chapter is absent from that list or
later than its own.

**`LN-2` exercise and solution authoring.** Accepted iff: (1) every `EX-##.##`
cites the `PF-###`, `PR-###`, or axis token it exercises; (2) every item
survives the anti-rote rules §9.6.1–§9.6.7, each applied by its own stated
procedure with the result recorded per item: the reviewer performs the
restatement search, the shortest-answer diff, the specimen-freshness grep, and
the verb-honesty check, and records pass or fail for each item by id.
Producing a bare token or a bare axis mark is not evidence that an item is
non-recall; (3) `SO-##.##` exists for every `EX-##.##` with the identical
number; (4) each solution cites the audit axes it turns on; (5) where more
than one answer is defensible, the solution says so and states the
discriminating consideration, rather than presenting one answer as the answer;
(6) no solution introduces a proposition not `ACTIVE` at that point in the
book; (7) the chapter's composition satisfies every rule of §9.5 and its stage
row, counted by the reviewer from the printed `tier` fields, including verb
spread and functional-family coverage; (8) every solution at `T2` and above
ends with an `audit-delta` line; (9) every solution declares exactly one
answer mode, and every `PLURAL` solution prints its parts (a)–(d), the
acceptance-test and the failing response included; (10) the chapter's
`IRREPARABLE` count meets the per-stage floor of §9.8.3 and the book-level
running total is reported with the submission; (11) no exercise block prints
an `ER-###`, a verdict token, an audit mark, or a locus triple, and no
solution mints an identifier of any class.

**`LN-3` LaTeX design and production.** Accepted iff: (1) every environment
named in §12 exists and renders; (2) every §11 margin token is distinguishable
in grayscale and by shape or label, never by color alone — the reviewer's test
is a grayscale print of any three pages; (3) all fourteen audit rows fit and
render without overflow; (4) cross-references resolve to ids, and a reference
to a `SUPERSEDED` or `RETIRED` id fails the build rather than rendering; (5)
margin density holds at median 3 and maximum 5 notes per page across a sampled
chapter; (6) a byte-level diff of the prose sources before and after the
production pass is empty.

**`LN-4` ledger tooling.** Accepted iff: (1) each of `LC-01`–`LC-22` is
implemented and, run against a deliberately corrupted fixture exhibiting
exactly that fault, reports it and names the offending ids; (2) each of
`LC-01`–`LC-22` run against a clean fixture reports nothing; (3) `LC-05` fires
on a `strength-history` entry above the record's own `modality` or
`modal-scope` with no new id and no cited `BR-###`; (4) no check is satisfied
by absence of data — a record missing a required key is a failure, not a skip;
(5) the tool exits non-zero on any check failure; (6) each of `LC-12`–`LC-22`
is implemented at the severity §10.5 assigns it, `LC-15` sub-coded by rule,
with a corrupted fixture supplied for each — including a revealed premise
entered under a non-`PROPOSITION` `kind`, a bridge premise resolving to no
warranted companion record, a proposition recorded at its proof's claimed
rather than its established strength, and a proposition with empty
`established-by`. A check implemented at a lower severity than assigned, or
reported as skipped, is a rejection, not a note.

**`LN-5` editorial review.** Accepted iff every notice cites, for each
finding, the condition id or axis token and the locus; and iff the notice
contains no rewritten text of the deliverable.

### 16.3 Universal acceptance checklist

Applies to every lane and every submission. Each item is a **veto**: one
unmet item is a rejection under §16.7, regardless of the rest. The submitting
lane marks all twelve before submission; the reviewer re-derives them
independently.

| Id | Condition | Reviewer's detection method |
|---|---|---|
| `UA-1` | The warrant ladder is preserved; no passage treats two rungs as one, and no argument is called an explanation | Grep the deliverable for "proves", "demonstrates", "explains", "shows". For each hit, read off the `rung` of the object it describes. A word above the recorded rung, or "explanation" applied to an argument rather than to `PRI-GND`, is the failure |
| `UA-2` | No formal derivation is treated, by itself, as a metaphysical demonstration | For every object whose `import` is `CONCEPTUAL` or `LINGUISTIC`, confirm the verdict is `V-VALID-ONLY` and that no later line consumes its conclusion as a real claim. Then apply the MD5 paraphrase test to every `import: REAL` object: rewrite `C` as a claim about our concepts; if the same premises support the rewrite with the same force, `UA-2` fails |
| `UA-3` | No citation substitutes for an argument | The §13.5 deletion test on every passage containing a canonical or contemporary author's proper name: strike name, quotation, locus; if any premise loses its warrant, any step its rule, any `DF-###` its sense, or any objection its force, `UA-3` fails |
| `UA-4` | No revealed premise stands inside a conclusion of natural reason | The §13.4 excision test: delete every theological remark block, every `scholion`, every `CC-REV` sentence, and every proposition whose warrant chain passes through one; re-run the object. A lost step input, a lost warrant, or a narrowed `established` is the failure. Then, because marker-driven excision cannot see an *undeclared* revealed premise, apply the §13.4 faith-independence test to every premise, bridge, definition, and term sense whose content a religious tradition teaches, whatever warrant token is printed: strike from the author's stated evidence every proposition believed only because a tradition teaches it, and ask whether any stated reason remains. `LC-09` catches the ledger form |
| `UA-5` | No substantive disputed premise hides inside a definition | For every `DF-###`, attempt to derive its `statement` from its `TM-###.n` sense plus prior ids alone. Underivable residue is a hidden premise and must have been promoted to a `PR-###` with its own §2.1.2 warrant. `LC-08` is the mechanical form |
| `UA-6` | No attribute conclusion is reached without an explicit bridge | For every attribute claim (simplicity, unity, immateriality, intellect, goodness, omnipotence, and every other), confirm a separate `PF-###` exists, that its `depends-on` names the prior result, and that the prior result's `not-established` still lists the attribute. An attribute delivered as a corollary of reaching a non-derivative principle is the failure |
| `UA-7` | No rival position is straw-manned | For each `denial-set` member and each `OB-###`, confirm the named opponent's reason is traceable to a cited proponent's own statement (§13.6 (3)). A reason with no proponent behind it, or weaker than that literature's, is `DIA` = `FAIL` |
| `UA-8` | No proposition is consumed before it is established | `LC-01`–`LC-22` over the accumulated ledger, never over the delta alone — the one set in which a forward reference cannot appear — plus a manual pass: for each `USES` callout and each `depends-on` entry, confirm the cited record is `ACTIVE`, `established-by` is non-empty, and its `introduced-at` precedes the citing locus |
| `UA-9` | No conclusion is stronger than its premises license | Three sub-tests, each vetoing independently. **(a) Weakest link:** identify the load-bearing premises by deleting each in turn and seeing whether some step fails; compare `established`'s necessity kind and modal scope against the weakest value among *those* premises under the §10.3 orders. A value above that lower bound with no `BR-###` cited on the step that raises it, and whose antecedent is discharged inside the object, is the failure; the token's presence on a non-load-bearing premise is never a defence. **(b) Delivered subject:** read the `to` line of the final step and compare its subject and quantifier with `subject` and `domain`; a mismatch is the failure whether or not `established` agrees with the `subject` field. **(c) Survey completeness:** `not-established` prints all seven `overreach-kind` lines, each an entry or a `CLOSED` with its reason; a missing line, or a `CLOSED` reason surviving the transplant test, is the failure. `UA-9` is met only when all three sub-tests are met, and a reviewer marking it met MUST record which premise supplied the lower bound in (a) |
| `UA-10` | Every ledger check reports clean over the accumulated ledger | Run the tool over every `ACCEPTED` chapter's records plus the submitted delta and read its exit code; `LC-01`–`LC-22` must all report clean. For any check the tooling lane has not yet implemented, run it by hand and record the result and the check id in the notice. A check reported as skipped is an unmet `UA-10` |
| `UA-11` | No modern apparatus token is presented as the historical theory's own concept (house rule 8) | Grep the deliverable for apparatus tokens (`RG-*`, `MD*`, `W-*`, audit-axis tokens, `ER-*`) appearing in `CC-TEXT` passages, `scholion` environments, or Chapter 0 historical prose. Each hit is a retrojection: the historical theory is cited by its own terms and loci, not by modern tokens. A passage presenting Aristotle's six conditions as "MD1–MD6" or Aquinas's *duplex est demonstratio* as "the `RG-THAT`/`RG-WHY` distinction" is the failure |
| `UA-12` | The concordance between modern apparatus and historical theory is complete and honest | For every modern token mapping to a historical antecedent (§2.8.5), the disanalogy is stated where the mapping is used. A mapping presented as an identity ("Aquinas's *demonstratio quia* is our `RG-THAT`") with no disanalogy stated or cited is the failure |

### 16.4 What later agents may and may not claim

**Permitted frames, by situation.** Each is the licensed wording; a lane may
vary the syntax but not the force.

1. *Complete demonstration* — verdict `V-PASS`, `rung: RG-WHY` or `RG-THAT`,
   `framework: NEUTRAL`. Permitted: "`PR-###` establishes `<established>`, at
   achieved rung `RG-WHY`/`RG-THAT`" (per §2.7, naming the object's id and printing
   its achieved rung; no conditionality clause attaches, the verdict being
   `V-PASS` and the framework `NEUTRAL`); for `RG-THAT`, "establishes *that*, not
   *why*", with the explanatory claim printed in `not-established`. Forbidden:
   calling an `RG-THAT` result an explanation.
2. *Complete within the declared framework* — verdict `V-PASS` or `V-OPEN` with
   `framework ≠ NEUTRAL`, or a load-bearing `W-POST` premise. Required frame:
   "Within `<framework>`, `PR-###` follows; the argument does not establish
   `<framework>`, and `<premise>` is a `W-POST` posit that `<named position>`
   rejects for `<its own reason>`." Omitting either half is `FRM` = `FAIL`.
3. *Weaker conclusion than intended* — `V-PARTIAL` or `V-REPAIR` on `SCO`.
   Required: state the weakened `established` in full, and name in
   `not-established` the intended stronger claim that was not reached. Forbidden:
   "essentially establishes", "amounts to", "in effect shows", "for practical
   purposes".
4. *Failure* — `V-FATAL`. Required: name the `ER-###`, the defect's exact
   location, `why-no-repair`, and `survives` (which may be `NONE`). Forbidden:
   presenting a failed argument as suggestive, promising, or "pointing toward" a
   conclusion; a failed demonstration supports nothing.

**Prohibited concealment phrases.** "It can be shown that", "obviously", "it
follows immediately", "clearly", "it is evident that", "as is well known",
"needless to say", "of course", "trivially" are **prohibited wherever they stand
in place of an inference the reader is entitled to see** — that is, wherever the
step they cover is not (a) an application of a named rule in a printed `L2-NUM`
or `L3-SKEL` line, or (b) a citation of an `ACTIVE` id. *Reviewer's method:*
grep for each phrase; for every hit, demand the rule name or the id. Absent
either, delete the phrase and check whether an unwritten inference is now
visible; if so, reject. The same words are permitted inside a quoted `CC-TEXT`
passage and inside an objection stated in an opponent's voice.

**Never claimed at all:** that a demonstration compels assent, refutes a
tradition, settles a dispute the book has not audited, or is the only or best
proof of its conclusion. Those all stand on the "Deliberately not required"
list, and no axis may be marked `FLAG` or `FAIL` for their absence.

### 16.5 Escalation

Where the spec is **silent**, an agent may decide locally only under §1.5(4) —
the decision touching none of the closed vocabularies, the identifier scheme,
the audit axes or verdict rules, the layer rules, or the eight house rules — and
MUST record the decision and its rationale for ratification. In every other
case, and in every case where the spec is **ambiguous** (two readings yield
different deliverables) or **wrong** (the rule as written forces a defect), the
agent **stops work on the affected unit** and files an amendment request.

An amendment request `AM-###` contains, in order: (a) requesting lane and
submission; (b) the spec locator in `DOCUMENT-SPEC §n.m (k)` form; (c) the
defect class — `SILENT`, `AMBIGUOUS`, or `WRONG`; (d) the competing readings, or
the defect the current rule forces, with the concrete instance that provoked it;
(e) proposed replacement text, quotable verbatim into the spec; (f) what is
blocked and what work continues meanwhile.

Prohibited while an `AM-###` is open: implementing either reading "provisionally";
leaving a `TODO`, a placeholder id, or a hedged sentence in the deliverable;
submitting the affected unit for review. Unaffected units continue. An agent
that improvises past a silence in a governed area has produced a defective
deliverable however good the improvisation.

### 16.6 Change control on this specification

1. Only the architecture lane amends `DOCUMENT-SPEC.md`. No later lane edits it,
   and no lane's working notes, README, or code comment amends it by implication.
2. An amendment lands as an edit to the spec text itself, carrying its `AM-###`
   and a one-line statement of **what it supersedes**: the exact prior sentence,
   rule, table row, or token, marked superseded or removed. Leaving the old
   wording in place beside the new is prohibited.
3. Closed vocabularies (`RG-*`, `W-*`, the fourteen axes, the six verdicts,
   `NEC-*`/`POS-*`, `PRI-*`, `DK-*`, `PRD-*`, `QUA-*`, `CC-*`, the ten margin
   tokens, the §10.1 prefixes) change only by amendment, and an amendment that
   adds or removes a token MUST state the migration for every already-accepted
   use.
4. The spec carries a version stamp, incremented by each amendment. Every
   submission names the version it was written against. When an amendment
   changes a rule that already-accepted work relied on, the amendment names each
   affected unit and whether it is re-opened; silence means not re-opened.
5. Ratified local decisions under §1.5(4) are folded into the spec by amendment
   at the next opportunity, so that the spec remains the single source of truth.

### 16.7 Rejection protocol

A review returns exactly one of: **ACCEPT**, **REVISE**, or **REJECT**.

- **REVISE** is available only for *mechanical* defects: a missing field, a
  malformed id, a broken cross-reference, a fourteenth row omitted from a table,
  a callout over the word limit, a build error. The intellectual content is
  correct and the fix does not change any `claim`, `established`,
  `not-established`, verdict, or audit mark.
- **REJECT** is mandatory for *intellectual* failures: any unmet `UA-1`–`UA-12`;
  a verdict that does not follow from the marks; an audit mark that is wrong on
  its own axis definition; a `denial-set` member below its strongest form; a
  concealment phrase covering an unwritten inference; a claim outside §16.4's
  permitted frames; a boundary violation under §16.1; an exercise set failing
  any of `LN-2` criteria (2) or (7)–(11); a margin callout that fails the
  transplant test or contains a banned string; an unfired MUST-trigger; a Stage
  F chapter printing a verdict line with no audit table. These are not revision
  requests. The unit is returned unaccepted, and the lane re-does it — a lane
  that patches the sentence a reviewer quoted, without re-deriving the object,
  has not answered the rejection.

A rejection notice contains: submission id and spec version; per finding, the
condition id or axis token, the exact locus, a one-sentence statement of the
defect, and the detection method applied; the disposition (`REJECT`); and
nothing else. The reviewer supplies no replacement text, no suggested premise,
and no rewritten conclusion — supplying them makes the reviewer a co-author of
the object and disqualifies the next review. Where the reviewer believes the
spec itself caused the defect, the reviewer files an `AM-###` instead of
rejecting.

Two consecutive rejections of the same unit on the same condition escalate to
the architecture lane as a suspected spec defect rather than a third attempt.


## 17. Questions Deliberately Deferred

### 17.1 The test a deferral must pass

A question may appear in §17.2 only if all five conditions hold. An item failing
any one is a hole in this specification wearing the costume of a decision, and
MUST be moved to the section that owns it.

1. **Startability.** A chapter author can draft Stages A through C, and the
   production lane can build the vertical slice to its §15.8 gate, without the
   answer.
2. **No retroactive edit.** Every admissible answer leaves every id, `claim`
   wording, premise warrant, `modality`, `depends-on` edge, axis mark, and
   verdict untouched. If some answer would re-mint an id or move an audit
   result, the question is architectural, not late-stage.
3. **Named owner and named gate.** A later lane owns it and a stated event
   forces it. "Later" is not a gate.
4. **Bounded on arrival.** A rule already in force constrains the answer space,
   so a bad answer is detectable when proposed, not discovered in rendering.
5. **No frozen condition contradicted.** No admissible answer may fail an
   acceptance condition already fixed by the production conditions `AC-P##`
   (§12), the vertical-slice gate (§15.8, §15.9), or the acceptance criteria
   (§16.2, §16.3). A question one of whose admissible answers would breach such a
   condition is not a deferral but a conflict between sections; it is escalated
   under §16.5 and MUST NOT be listed in §17.2. A narrowed remainder that every
   admissible answer leaves conforming may be listed.

**Reviewer procedure.** Delete any row of §17.2 and ask whether the §15 slice can
still be authored and built. If yes, the deferral is honest; if no, this
specification is incomplete and that row is the evidence. Then negate each row's
answer space and check it against condition 5. The list is nine rows; a longer
one would be the same evidence. A lane proposing to defer anything not listed
below files a spec-amendment request under §1.5 — deferral is never a local
decision.

### 17.2 Deferred questions

| # | Question | Owner | Safe because | Settled by |
|---|---|---|---|---|
| D1 | Typeface selection: text, math, and the grade carrying the margin tokens | Production | §12 constrains faces by function — measure in characters, grayscale separation of grades, coverage of `□ ◇ ∀ ∃ → ⊢ ≠ ·` — never by name; any conforming face substitutes without altering a word of text | First vertical-slice build; frozen thereafter |
| D2 | Final trim size and margin geometry within the §12 measure and outer-margin ranges | Production | No proof-object field, id, or axis mark is a function of page dimensions, and nothing is paginated before the first build | First vertical-slice build — §15.7 counts rendered pages, so it cannot be measured earlier |
| D3 | Implementation language, serialization, and invocation of the ledger tooling | Tooling | §10.2 fixes the record keys and their value vocabularies and §10.5 the semantics of `LC-01`–`LC-22`; at small scale authors write conforming records and reviewers run the checks by hand | The earlier of: 40 `ACTIVE` ledger records, or acceptance of the first Stage C chapter |
| D4 | Typographic treatment and head-note wording of the four indexes `AC-P30` mandates: run-in versus indented setting, sense-selector and locator styling, head-note wording | Production | `AC-P30` fixes which four indexes ship, that entries are generated from `lexicon`, `name-normalized`, and identifier fields rather than hand-compiled, and that coverage is checked mechanically against the ledger; presentation is a function of no record, so no treatment can alter, add, or lose an entry | First-edition page freeze. Inadmissible under any treatment: dropping an index, hand-compiling an entry, or erasing the establishing/specimen locator distinction |
| D5 | Reference layout and punctuation — field order within an entry, delimiters, and the style file emitting them — inside the six `CC-*` citation classes §13.2 fixes and the author–year / canonical-locus split `AC-P29` fixes | Production, under §13.2 and `AC-P29` | Class membership, the printed class marker, canonical locus for classical and scholastic primaries, author–year for modern secondary literature, and the separately named edition are fixed above the style layer; punctuation cannot erase any of them | First build carrying a citation from each of the six classes. Inadmissible under any style: rendering the six classes indistinguishably, substituting a printing's page for a canonical locus, or dropping the named edition or translation |
| D6 | Whether the back-matter solutions part is bound in this volume or issued as a separately bound back-matter fascicle of the same edition, same ids, same order | Editorial with production | §9.7 fixes one collected solutions part ordered by id and forbids any answer, hint, or partial answer in a chapter; `AC-P17` forbids a solution on the page or facing page of its exercise. Collection and non-adjacency hold under either binding, and each exercise block's single pointer line names the solution range either way | First-edition page freeze. Inadmissible under either binding: a solution printed in a chapter, or a per-exercise page pointer |
| D7 | How far past the minimum the first edition carries Stage F, and whether post-curriculum material ships as appendix or second volume | Curriculum with editorial | Ids are allocated globally and never reused or renumbered (§4.1, §10.1), so appending or withholding an attribute chapter mints new ids only and disturbs no prior `claim`, edge, or verdict | First-edition content freeze |
| D8 | Translation and localization | Editorial; no lane in this programme | Out of scope for the first edition; no English text depends on it | Not settled unless commissioned. Binding then: ids and every closed vocabulary (`RG-*`, `W-*`, `NEC-*`, `PRI-*`, `DK-*`, `SCP-*`, `PRD-*`, the margin and verdict tokens) are proper names of the apparatus and are never translated |
| D9 | Whether any `L3-SKEL` derivation is additionally machine-checked, and in which assistant | Tooling | Machine-checking is on the "deliberately not required" list of §2.5; adding it changes no field of any existing object | Not settled unless commissioned. Binding then: a check confirms `LOG` and nothing else — it never raises a rung above `RG-VALID`, never touches `FID`, `WAR`, or `ONT`, and its absence is never a `FLAG` |

### 17.3 Settled elsewhere, and therefore not open

These invite reopening and are closed. A lane that reopens one has departed from
the specification, not exercised judgment (§1.5).

| Looks deferrable | Settled in |
|---|---|
| What "demonstration" means: MD1–MD11, the rung ladder, and that `RG-THAT` is a complete species, not a failed `RG-WHY` | §2.1.1 for MD1–MD11; ladder at §2.2 |
| The eight house rules, their numbering, and the axis, check, or detector enforcing each | §1.7 |
| The historical theory of demonstration (Aristotle's *apodeixis*, Aquinas's adaptations), the Heritage Declaration, and the concordance between modern apparatus and historical theory | §2.8 |
| The closed warrant list of nine, and that `W-REV` and `W-AUTH` exist to be detected and never used | §2.1.2, enforced by §13.2 and §13.4 |
| The necessity, modal-scope, priority, distinction, predication, and qualification token families and their binding test orders | §3.9, used as fields in §4.2 and §4.3 |
| Which proof-object fields are `MUST`, and what may never be left implicit | §4.2 field table; §4.7 |
| The identifier scheme: closed prefixes, global allocation, no reuse or renumbering, immutable `claim`, supersession by new id | §4.1 reference syntax; §10.1 allocation |
| The fourteen audit axes, the four marks, and the six verdicts computed first-match rather than chosen | §6.1, §6.2, §6.3 |
| The anti-rote rule: every exercise cites the `PF-###`, `PR-###`, or axis it exercises, and reproducing an approved argument is not an exercise | §9.6 |
| The Stage F bridge discipline: every attribute a separate `PF-###` with explicit `depends-on`, none a corollary of reaching a non-derivative principle | §8.10 |
| The incorrect-example marking mechanism: `kind: SPECIMEN`, its pedagogical format, and that no specimen is ever cited as `W-DEM` | §7.4; environment at §12.5 |
| The closed margin token set, its per-token content rules, and the delete-the-margin reviewer test | §11.1, §11.3, §11.6 |
| The three layers, what each cannot establish, and that `L3-SKEL` never prints without `L2-NUM` | §5(i)–(vi); capacities at §5.1 |
| The ledger record keys and the semantics of `LC-01`–`LC-22`; only their implementation is deferred, at D3 | §10.2, §10.5 |
| Framework marking, and the difference between proving a result inside a framework and establishing part of it | §14.2, §14.3 |
| The vertical-slice acceptance gate, including what makes an attractive prototype rejectable | §15.8, §15.9; lane criteria at §16.2 |


## Appendix A. Architectural Exemplars

Five miniatures, each illustrating a spec requirement. None is chapter content;
no later agent may lift one into the book as written.

**Conventions, binding on this appendix only.**

1. Exemplar ids come from the reserved appendix band `TM-901+`, `DF-901+`,
   `DS-901+`, `PR-901+`, `PF-901+`, `OB-901+`, `BR-901+`. No chapter and no other
   section allocates in the 900 band — §7.4 reserves it against every book id of
   every class, and the error-taxonomy section's worked specimens stand clear of
   the appendix run at `PF-951/S` and `PF-952/S` — and this appendix allocates no
   id outside it. Nothing here is a live ledger record.
2. `ER-###` numbers cited here are the **live ids** assigned by the
   error-taxonomy section in its family hundred-bands (§7.2, §7.5), not
   placeholders drawn from an axis band. An exemplar cites a class by id,
   canonical name, and the single axis the taxonomy records for it (§7.1(1));
   where the two disagree, the taxonomy governs and the citation here is the
   defect.
3. **Incorrect-specimen marking is a pointer, not a variant.** The mechanism is
   fixed by §7.4 and §12.5 and is neither restated nor varied here. Three
   consequences bind the exemplars below. (a) The single marker word is
   `DEFECTIVE`, printed in the environment header with the id and the `ER-###`
   list and repeated in the outer foot of every page the environment occupies;
   "INCORRECT AS STATED" and "Incorrect" are retired. (b) There is **no
   undisclosed-specimen exemption**: a specimen posed as a find-the-defect
   exercise withholds its `ER-###` list and its audit table, never its marker
   word, band, or foot. (c) Every specimen id prints its mandatory `/S` suffix,
   which precedes any line selector: `PF-902/S.2`.
4. `kind` follows §4.2.1 and is not softened here. `kind: SPECIMEN` means an
   argument printed **in order to be rejected**, carrying at least one axis at
   `FAIL` and at least one `ER-###`. A correct argument that is nonetheless no
   demonstration is `kind: DEMONSTRATION` at `rung: RG-VALID`, verdict
   `V-VALID-ONLY`: Exemplar A is that case, and typing it `SPECIMEN` would be
   `DEM` = `FAIL` by §4.2.1(a).

### A.1 Exemplar A — Valid logical skeleton, in three layers

Illustrates: §5 layer machinery; house rule 2; verdict `V-VALID-ONLY`.

`PF-901` · `kind: DEMONSTRATION` · `rung: RG-VALID` · `logic: first-order logic
with identity` · `import: CONCEPTUAL` · `framework: NEUTRAL` ·
`layers: L1-PROSE, L2-NUM, L3-SKEL`. `kind` records what the book does with the
object — asserts it — not the rung it reaches; §4.8 condition 1 denies it the
reduced form, and no `MUST-C` field is owed at Stage A.

**`L1-PROSE`.** Any number divisible by four is even. Twelve is divisible by
four. So twelve is even.

**`L2-NUM`.** Every line carries warrant, modality, scope, and import; every step
names `from` and `rule`.

| Line | Content | `warrant` or `from`, `rule` | Tokens |
|---|---|---|---|
| p1 | For every *n*, if *n* is divisible by 4 then *n* is even | `W-DEM` (`PR-901`) | `NEC-CON`, `SCP-CMP`, `CONCEPTUAL` |
| p2 | 12 is divisible by 4 | `W-DEM` (`PR-902`) | `NEC-CON`, `SCP-CMP`, `CONCEPTUAL` |
| .1 | If 12 is divisible by 4 then 12 is even | p1; universal instantiation | — |
| .2 | 12 is even | .1, p2; modus ponens | `NEC-CON`, `SCP-CMP`, `CONCEPTUAL` |

**`L3-SKEL`.** `∀n(Dn → En)`; `D(12)`; `⊢ E(12)` by UI then MP. `domain`: the
integers; the `∀` premise declared **without** existential import; the constant
`12` licensed by `PR-902`, not by occupying subject position (MD3). `fidelity`:
`D` and `E` are uninterpreted, so `L3-SKEL` shows only that the shape transmits
truth, never that either predicate applies to anything.

**What this does and does not establish.** MD1 holds; `LOG` = `OK`; that is the
whole of it. MD5 fails: paraphrase the conclusion as a claim about our concepts
and the same premises support it with the same force, so no `REAL` import is
incurred. Achieved rung `RG-VALID`; verdict `V-VALID-ONLY` with
`conceptual-result` printed. `PF-901` is therefore no metaphysical demonstration
at any rung, and is not certified sound — `RG-SOUND` is a property of the world,
which no audit reaches. Validity is a property of the shape alone.

### A.2 Exemplar B — Invalid near-neighbour, and how to localize

Illustrates: the localization discipline that Stage A and Stage D authors imitate.

`Specimen PF-902/S · ER-201 — DEFECTIVE` · `kind: SPECIMEN` · `rung: RG-VALID`
(claimed) · `import: CONCEPTUAL`.

| Line | Content | Rule cited |
|---|---|---|
| p1 | For every *n*, if *n* is divisible by 4 then *n* is even | `W-DEM` (`PR-901`) |
| p2 | 6 is even | `W-DEM` (`PR-903`) |
| .1 | If 6 is divisible by 4 then 6 is even | from p1, UI |
| .2 | 6 is divisible by 4 | from .1, p2, "modus ponens" |

**Correct localization** (the five obligatory elements, in this order):

1. **Line or field.** `PF-902/S.2`.
2. **Axis and mark.** `LOG` = `FAIL`. Exactly one axis; the other thirteen are
   assessed independently, and none fails.
3. **Error class.** `ER-201`, affirming the consequent, axis `LOG`, family
   `EF-LOG`.
4. **Countermodel.** Domain `{6}`; `D` false of 6, `E` true of 6. Then p1 is
   vacuously true, p2 true, `.2` false. The rule named at `.2` does not license
   its `to` from its `from`: modus ponens consumes the antecedent, `.2` the
   consequent.
5. **Consequence.** Nothing is established, at any rung.

`audit`: `LOG` = `FAIL`; `FID` = `N/A`, no `L3-SKEL` printed; no other axis
fails. `verdict`: `V-FATAL` by §6.3 rule 1, second disjunct — the only edits
reaching `claim` are asserting `D(6)` or adding `E(6) → D(6)`, each of which
assumes `claim`. Fields: `errors: ER-201`; `why-no-repair` as stated;
`survives: NONE`.

**Vague localization, for contrast — a defect, not a style.** *"It confuses a
conditional with its converse, and so is unsound and its conclusion
unwarranted."* No line, no axis (*unsound* is a rung word), no `ER-###`, no
countermodel; the complaint-words hide that only `LOG` fails. Any diagnosis
missing one of the five elements is rejected.

### A.3 Exemplar C — Modal defect: conditional necessity to necessary consequent

Illustrates: §3.9 test order and scope tokens, MD6, `BR-###` discipline.

`Specimen PF-903/S · ER-302, ER-303 — DEFECTIVE` · `kind: SPECIMEN`.

| Line | Content | Tokens |
|---|---|---|
| p1 | Necessarily, if *a* is a composite then *a* has parts | `NEC-CON`, `SCP-CMP`, `W-DEF` on `DF-901` |
| p2 | *a* is a composite | `ACT`, `W-EMP` |
| .1 | *a* necessarily has parts | `NEC-MET`, `SCP-DIV`, from p1, p2, "modus ponens" |

It is tempting because the consequent is one a competent metaphysician believes
*de re*: that belief, not the inference, is doing the work.

**Two defects, two error classes, one axis.** The single-axis rule (§7.1(1))
attaches one axis per *class*, not one per defect; both classes below are
`EF-MOD` and both fire `MOD`, so one `FAIL` row carries two `ER-###` ids.

| Defect at `PF-903/S.1` | Class | Axis |
|---|---|---|
| `SCP-CMP` premise read in `SCP-DIV` at the conclusion | `ER-302`, composite/divided conflation | `MOD` = `FAIL` |
| `NEC-CON` premise yields a `NEC-MET` conclusion | `ER-303`, conceptual necessity read as real | `MOD` = `FAIL` |

Margin, in the audit pass (§11.9), on `PF-903/S.1`: `MODAL!` *`NEC-CON`
`SCP-CMP` in, `NEC-MET` `SCP-DIV` out; no bridge cited* `[MOD FAIL]`.

**Repair (minimal).** Delete the modal operator from `.1`. Nothing else changes.

**What survives.** (i) *a* has parts — `ACT`, `import: REAL`, warrant inherited
from p2. (ii) In every world in which *a* is a composite, *a* has parts —
`NEC-CON`, `SCP-CMP`, `import: CONCEPTUAL`, carrying no real import without a
cited bridge (§3.9). **Not** surviving: that *a* has parts in every world in
which *a* exists. That needs two further things, neither free — a premise that
*a* is composite essentially, and a cited `BR-901` licensing `NEC-CON` →
`NEC-MET`, itself `W-POST`. `verdict: V-REPAIR`; `errors: ER-302, ER-303`;
`survives` = (i) and (ii). The surviving `REAL` claim is about *a* alone and is
`ACT` — the strength the premises paid for.

### A.4 Exemplar D — Metaphysical ambiguity: a semantic failure, not a logical one

Illustrates: MD2 substitution detector, `TM`/`DF` split, house rule 5, `SEM`
versus `DEP` routing.

**Proposition.** *Whatever a thing depends on is prior to it.* The term
`TM-902` *prior* is the pivot.

| Sense | Reading (§3.9) | Value | Test that settles it |
|---|---|---|---|
| `TM-902.1` | `PRI-TMP` | **False** | The shape of the bronze depends on the bronze's arrangement at the very same instant: `SIM-NAT`, nothing earlier. |
| `TM-902.2` | `PRI-ONT` | **True**, but `NEC-CON`, `CONCEPTUAL` | Derivable from `DF-902` (*depends*) plus logic alone; unpacks the definition, adds nothing real. |
| `TM-902.3` | `PRI-GND` | **Not established** | `PRI-ONT` does not entail `PRI-GND` (§3.9): necessary co-existents may depend existentially with grounding in neither direction. |

One word, three readings, three values — and every derivation containing the
proposition stays formally impeccable, since one uniform predicate letter for
*prior* preserves validity in all three cases. `LOG` = `OK`; the failure is
`SEM` = `FAIL`. A reviewer who reaches for `LOG` here has misrouted.

**What the author must do.**

1. `TM-902` is entered with numbered senses and **every** occurrence carries its
   selector (MD2). Two selectors across two lines with no declared `PRD-ANA` is
   `SEM` = `FAIL`.
2. Run the MD2 substitution detector: `.1` everywhere makes the proposition
   false; `.2` everywhere costs the conclusion its real import. Either fails MD2.
3. **No `DF-###` may stipulate the sense that makes the disputed reading true.**
   Writing `DF-903` "*prior* means: that in virtue of which the dependent
   obtains" imports the grounding claim into a definition. `LC-08` fires, and the
   content is promoted to `PR-904` with its own warrant, `contested: true`, and
   its own `denial-set` membership. House rule 5, mechanically.
4. An author claiming one account spans all three senses is making a `PRD-ANA`
   claim and MUST state the ratio; unstated ratio means `PRD-EQV`, and the
   argument equivocates.
5. Margin, where the selector changes: `DEF` *prior at `TM-902.2`: what the
   dependent cannot exist without*. The sense is given in the author's own words;
   a note reading only *sense `TM-902.2`* names nothing proper to its line and is
   deleted by the transplant test (§11.6). **No axis tag is printed**: a tag is
   admissible only beside a printed audit-table row (§11.7), and an orphan
   `[SEM FLAG]` beside running prose is itself the defect.

**Routing rule.** *Sliding* between senses of one term takes `ER-102`, sense
drift, axis `SEM`. *Asserting* a `PRI-*` token on the wrong test — calling a
dependence `PRI-TMP` on the strength of a grounding intuition — takes `ER-501`,
temporal priority read as causal or ontological, axis `DEP` (family `EF-EXP`).

### A.5 Exemplar E — A bounded metaphysical demonstration, end to end

Illustrates: the canonical proof object with every `MUST` field populated, one
filled audit table, one margin column. Deliberately `RG-THAT`, deliberately
small.

**`PF-905` record.**

| Field | Value |
|---|---|
| `id` / `name` | `PF-905` / Change requires a persistent constituent |
| `kind` / `rung` / `logic` | `DEMONSTRATION` / `RG-THAT` / first-order logic with identity, modal lines in `T` |
| `claim` | In every change, some constituent of the subject is numerically the same before and after, and some feature of it is not. |
| `subject` / `attribute` | changes (`TM-903.1`) / having both a persisting and a non-persisting constituent |
| `import` / `modality` | `REAL` / `NEC-MET`, `SCP-CMP` |
| `domain` | changes, their subjects' constituents, each change's two termini; **no existential import on any premise** |
| `lexicon` | terms `TM-903.1` *change*, `TM-904.1` *constituent*; distinctions `DS-901` persisting constituent / non-persisting feature, `DK-VIRT` |
| `premises` / `steps` | p1 – p3 and .1 – .7, below |
| `middle` / `middle-kind` | numerical sameness of the subject across the change / `FORMAL` |
| `commitments` | c1 – c2, below |
| `depends-on` | `TM-903.1`, `TM-904.1`, `DS-901`, `PR-905`, `PR-906` — every `lexicon` id, plus both borrowed propositions. `PR-907`, the posit p3 states, is **not** an edge: `LC-01` requires a strictly earlier `introduced-at`, and a posit first stated here is a record *of this location* |
| `established` | exactly `claim`, no wider and no narrower; MD5 rewrite of `claim`: *Our concept of change requires describing each changing subject twice over, by a recurring constituent and a non-recurring feature.* `p3` fails to support it with equal force, asserting sameness of a constituent in the thing, not merely in the concept. Then the §14 N11 conditionality note: *Established within `AT`, on posit `PR-907` (premise p3). A reader who rejects `PR-907` — `OB-902`, the perdurantist rejection at its strongest — incurs no commitment to this conclusion. Nothing here bears on the truth of `PR-907`.* |
| `not-established` | n1 – n3 plus four CLOSED lines, below |
| `denial-set` | {p1, p3}, each load-bearing by removal test |
| `objections` / `replies` | `OB-901`, `OB-902` / `RP-901`, `RP-902` (`RP-902` concedes conditionally) |
| `framework` / `framework-role` | `AT`, p3 only / `FR-INTERNAL` |
| `layers` / `audit` | `L1-PROSE`, `L2-NUM`, `L3-SKEL` / below |
| `fidelity` | *constituent* becomes one predicate letter, before/after two time arguments; `DS-901`'s `DK-VIRT` status is dropped, the declared calculus being unable to carry it |

**`commitments` (§4.4).**

| `cid` | `commitment-kind` | `statement` | `import` | `licensed-by` | `tag` | `paraphrase` |
|---|---|---|---|---|---|---|
| c1 | `RANGES-OVER` | changes as a kind, and the two termini of each as times; no change is asserted to occur | `CONCEPTUAL` | p1 | — | — |
| c2 | `REALLY-DISTINCT` | in one changing subject, a constituent that persists and a feature that does not, distinct in the thing | `REAL` | .6 | `DK-VIRT` | *Our concept of change requires describing the subject twice over.* Not equally supported: p3 asserts sameness of a constituent **in the thing**, and the perdurantist grants the concept while denying that sameness |

**`not-established` (§4.5), five keys each.**

| `nid` | `statement` | `overreach-kind` | `missing-bridge` | `where-treated` |
|---|---|---|---|---|
| — | `CLOSED` — `claim` already carries `NEC-MET`; no stronger necessity kind is licensed here | `OV-MOD` | — | — |
| n1 | that any change occurs | `OV-SCOPE` | `PR-908` (stub, `W-EMP`) | `NOT-IN-BOOK` |
| — | `CLOSED` — `claim` is `REAL`; the conceptual paraphrase fails, so no conceptual result is misread | `OV-IMPORT` | — | — |
| — | `CLOSED` — `claim` says some constituent; it does not establish the unique persisting constituent | `OV-UNIQ` | — | — |
| n3 | that the persisting constituent is *why* change is possible — the `PRI-GND` claim that would lift the rung to `RG-WHY`. Terminus declaration (§2.4): `middle-kind` is `FORMAL`, neither `EFFECT-SIGN` nor `PROPER-ATTRIBUTE`, so the object declares that a grounding middle may exist, is not exhibited here, and has as candidate ground the persisting constituent taken as bearer of act | `OV-EXPL` | `NO-BRIDGE-KNOWN` | `NOT-IN-BOOK` |
| n2 | that the persister is matter, or a substance, rather than any constituent whatever | `OV-IDENT` | `BR-902` | `NOT-IN-BOOK` |
| — | `CLOSED` — `claim` concerns each change individually, not all changes as a totality | `OV-TOTAL` | — | — |

**Premises and steps (`L2-NUM`), with the margin column.**

| Line | Content | Premise tokens / `from`, `rule` | Margin |
|---|---|---|---|
| p1 | In any change, the subject that is F beforehand is numerically the same as the subject that is not-F afterwards | `W-SELF` (analysis printed), `NEC-MET`, `SCP-CMP`, `REAL`, `FS-NEUTRAL`, `contested: true` | `OBJ?` *Hume: the persisting subject is supplied by habit, not observed* `OB-901` |
| p2 | If a thing is F at t1 and not-F at t2, something belonging to it at t1 does not belong to it at t2 | `W-DEM` (`PR-905`), `NEC-LOG`, `SCP-CMP`, `CONCEPTUAL`, `FS-NEUTRAL`, `contested: false` | `USES→` *`PR-905` supplies the difference principle discharged at .4* |
| p3 | Numerical sameness of a subject across t1 and t2 requires some constituent numerically the same at both | `W-POST` (`PR-907`), `NEC-MET`, `SCP-CMP`, `REAL`, `FS-INTERNAL`, `contested: true` | `OBJ?` *Perdurantist: persistence is counterpart-linked temporal parts, none shared* `OB-902` `[WAR FLAG]` |
| .1 | Instances of p1, p2, p3, `PR-906` at an arbitrary change *c*, subject *a*, termini t1, t2 | p1, p2, p3, `PR-906`; universal instantiation | `DIST` *`DS-901`: what persists across *c* against what does not; `DK-VIRT`* — trigger line `p3` |
| .2 | *a* at t1 = *a* at t2 | .1; conjunction elimination | `INF` *universal instantiation on p1 – p3 and `PR-906` at *c*; existential instantiation would not license naming *a** — trigger line `.1` |
| .3 | Some constituent of *a* is numerically the same at t1 and t2 | .2, .1(p3); modus ponens | `USES→` *`TM-904.1` fixes what recurs here as a constituent, not a stage* |
| .4 | Something belonging to *a* at t1 does not belong to it at t2 | .1, .1(p2); conjunction elimination, then modus ponens | `USES→` *`TM-903.1` fixes t1 and t2 as *c*'s own termini, not arbitrary instants* |
| .5 | That item is a constituent of *a* at t1 and not at t2 | .4, .1(`PR-906`); modus ponens | `USES→` *`PR-906` licenses reading what belongs as a constituent* |
| .6 | Some constituent of *a* is the same at t1 and t2, and some feature of it is not | .3, .5; conjunction introduction | `IMPORT!` *commits to a persisting constituent and a non-persisting feature, distinct in the thing* `DK-VIRT` |
| .7 | In every change, some constituent of the subject is numerically the same before and after, and some feature of it is not | .6; universal generalization on *c* | `INF` *universal generalization on *c*, free in no premise; existential generalization would not license the universal* |

Two further notes fall off the numbered lines: `SCOPE!` *not thereby matter,
substance, or accident* on the `established` block, and `RISK!` *`DK-VIRT` status
of `DS-901` unrepresentable in `T`* `[FID FLAG]` beside the `L3-SKEL` line
symbolizing *constituent*.

Twelve mandatory notes fire in all (§11.6 coverage rows 2, 3, 4, 8, 10, 11): two
`OBJ`, one per `denial-set` member; four `USES`, one per `depends-on` id other
than `DS-901`, whose `DIST` note cites it and names both sides, a second note on
that distinction being a §11.6 duplicate; one `DIST`; two `INF`; one `IMPORT`;
one `SCOPE`; one `RISK`. Two migrations, neither a drop, §11.4(5) forbidding the
dropping of a MUST-fired note: `DIST`, outranked by `OBJ` at trigger line p3,
moves to .1 and prints that id; `INF`, outranked at .1, moves to .2 and prints
its own. Twelve is the §11.4(3) ceiling exactly, so the object runs three pages
at five notes a page, and one further `denial-set` member or consumed id would
force the §11.4(7) escalation, which the authoring lane resolves. Coverage holds:
both `FLAG` rows are annotated on their own lines, both `denial-set` members
carry an `OBJ`, and no `WHY` appears — correctly, given `rung: RG-THAT`.

**Why `RG-THAT`.** Reversal detector (MD11b): *"there is a persister because the
subject is numerically the same"* and *"the subject is numerically the same
because there is a persister"* read equally well, so the middle is a sign, not a
ground. `EXP` is `N/A`, the unshown explanatory claim stands at n3 with its
terminus declaration, and the object is complete of its species, not a failed
`RG-WHY`.

**Filled audit table.**

| Axis | Mark | Note |
|---|---|---|
| `SEM` | `OK` | one selector per term throughout; no `PRD-ANA` needed |
| `LOG` | `OK` | every step names a rule licensed in the calculus |
| `EXI` | `OK` | no existence claim: `domain` declares every universal without import, and n1 records that no change is asserted to occur |
| `WAR` | `FLAG` | p3 is `W-POST` (`PR-907`): accepted here, not proved here |
| `MOD` | `OK` | `SCP-CMP` throughout; no necessity-kind change; no axiom beyond `T`'s reflexivity; no `BR-###` needed |
| `ONT` | `OK` | MD5 paraphrase fails at c2: "our concept of change requires a persister" is weaker than p1 |
| `EXP` | `N/A` | licensed only because `rung: RG-THAT` |
| `DEP` | `OK` | `depends-on` acyclic; each `PRI-*` token asserted on its own test |
| `SCO` | `OK` | `established` = `claim`; n1 – n3 name three distinct overreach dimensions; four further dimensions CLOSED |
| `DIA` | `OK` | two-member `denial-set`, minimal by removal; both opponents at strength |
| `DEM` | `OK` | achieved rung equals claimed rung, and the `RG-THAT` terminus is declared at n3 |
| `FRM` | `OK` | `FR-INTERNAL`; p3 `FS-INTERNAL`; conditionality note printed under `established` |
| `FID` | `FLAG` | `fidelity` printed; the symbolization erases `DS-901`'s `DK-VIRT` status, which the declared calculus cannot represent |
| `PRV` | `OK` | no citation in a warrant slot; no `W-REV` or `W-AUTH` |

**Verdict, computed.** No axis at `FAIL`, so §6.3 rules 1 and 2 do not fire. Rule
3 does not fire: `import` is `REAL`, and the `WAR` and `FID` flags are stated
limitations leaving the universal claim standing. Rule 4 fires on two independent
disjuncts: p3 is load-bearing, carries `W-POST`, and is unsettled here; and §14
N10 makes an `FR-INTERNAL` object consuming a posit still `POSITED` a case of the
same rule. **`V-OPEN`, achieved rung `RG-THAT`**, the extra field naming p3 and
the live positions on each side — endurantist substrate theories against
perdurantist and stage-theoretic accounts. Rule 5 is never reached: a reviewer
checks the ordering, not the label.

