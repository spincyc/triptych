# Reading Metaphysics: Document Specification

**Version:** 2
**Status:** Governing architecture. Binding on all authoring lanes.
**Supersedes:** version 1, at commit `92543fec1b0856b50f07eb6070734eeb3814f0a8`
**Working title of the book:** *Reading Metaphysics: What Is Being Claimed, and Why Should I Believe It?*

---

## What this document specifies

A short book, roughly fifty to eighty pages, that trains one competence:

> Given a difficult metaphysical passage, identify exactly what is being
> claimed, why the reader is supposed to believe it, where the substantive
> burden lies, what actually follows if it is granted, and what happens if it
> is denied.

The method is six questions asked in ordinary English — **Claim, Meaning,
Warrant, Burden, Consequence, Denial** — and eight standing rules. Prose is
the canonical medium. Symbolic notation appears only where it makes a named
inferential feature clearer. There is no apparatus for the reader to learn
before opening a text.

The governing test of the whole architecture:

> If the reader has to remember our names for things in order to apply the
> method to an unmarked page of Aquinas, the architecture has failed.

## Contents

| § | |
|---|---|
| 1 | Purpose, reader, and non-goals |
| 2 | The reading frame: six questions |
| 3 | Definition versus discovery |
| 4 | Warrant: why you are supposed to believe it |
| 5 | Source is not warrant |
| 6 | Revealed premises, theology, and natural reason |
| 7 | Consequence: what follows and what does not yet follow |
| 8 | Denial: what rejecting the burden costs |
| 9 | Notation: when it helps, when it hides |
| 10 | Demonstration and its limits |
| 11 | What the tradition actually held |
| 12 | Curriculum: nine lessons |
| 13 | Worked examples: the required progression |
| 14 | Exercises and solutions |
| 15 | The vertical slice |
| 16 | Author-side conventions |
| 17 | Acceptance tests and review |
| 18 | Questions deliberately deferred |
| A | Historical sources, verified |
| B | The one-page analysis sheet |

Sections 1 through 10 state the method. Section 11 governs the book's handling
of history. Sections 12 through 15 specify the curriculum, the required
examples and exercises, and the sample that must be produced and accepted
before the rest is written. Sections 16 through 18 govern authoring,
acceptance, and what remains open. The appendices are reference material.

## How to use this document

An authoring lane reads §1 and §2 first, then §16 through §18, then the
sections bearing on its assignment. No lane may introduce a vocabulary of
abbreviations, add a lesson, exceed a page budget, or symbolize an inference
that §9 does not license. Where this document is silent, ask rather than
invent.

Work order: the vertical slice (§15) is produced and accepted first. Lessons
are drafted only after it passes. No production or typesetting work begins
before the slice is accepted.

## A note on version 1

Version 1 specified a different book: a thirty-six chapter textbook teaching
the construction and audit of metaphysical demonstrations by means of a
proof-engineering apparatus. That apparatus is deleted, along with the
chapter structure built on it. What survives, translated into ordinary
English, is listed at §17.6, and version 1's verified historical research
survives at §11 and Appendix A. The reasons for the change are at §1.7.

Later agents must not restore the deleted machinery. A lane that finds itself
inventing a code of abbreviations has rediscovered version 1's mistake.

---
## 1. Purpose, reader, and non-goals

### 1.1 The competence the book produces

The book trains one competence, and its success is measured by that
competence alone:

> Given a difficult metaphysical passage, identify exactly what is being
> claimed, why the reader is supposed to believe it, where the substantive
> burden lies, what actually follows if it is granted, and what happens if it
> is denied.

A reader who finishes the book should be able to open an unfamiliar page of
serious metaphysics, with nothing but a pencil, and say in ordinary language
what the claim is, what the important words mean there, why each premise is
supposed to be accepted, which sentence is carrying the philosophical weight,
what has actually been established, and what denial would cost.

Everything in this specification exists to produce that result. Any
requirement that does not contribute to it is to be cut.

### 1.2 The problem the book solves

Serious metaphysical writing reaches a modern reader as a sea of
authoritative assertion. *Aristotle says. Augustine says. Aquinas says. Act
as act. Potency as potency. Being is said in many ways.* The prose is dense,
confident, internally cross-referential, and formed by a training the reader
never received.

The reader's difficulty is not that the vocabulary is unfamiliar. It is that
within a single paragraph the reader cannot reliably tell whether he has just
encountered:

- a definition;
- an unpacking of a technical vocabulary;
- a logical consequence of something already granted;
- a substantive claim about reality;
- a result demonstrated somewhere else;
- a theological premise held on revealed authority;
- an appeal to the standing of the author;
- or an actual demonstration.

These eight things look alike on the page. They are asserted in the same
register, in the same syntax, often in the same sentence. The reader who
cannot separate them has two bad options: accept the whole passage on the
author's credit, or reject the whole passage as verbal machinery. Both
options destroy the reader's access to whatever is actually true in the text.

The book supplies the missing discrimination. It is written for a reader who
believes there may be real root truth in metaphysics and who lacks a compact
language for locating where the genuine philosophical burden lies.

### 1.3 What the book is not

The book is primarily a personal intellectual tool. It is not, and no
authoring lane may quietly turn it into:

- a new formal science of metaphysics;
- a formalization of Thomism;
- a machine-readable metaphysical knowledge base;
- Aquinas rewritten as *Principia Mathematica*;
- a course in formal logic, modal logic, analytic metaphysics, or scholastic
  systematics;
- an encyclopedic textbook, or a thirty-six chapter curriculum;
- an exhaustive metaphysical system;
- a demonstration that Thomism is correct;
- an apparatus the reader must operate before reading a text.

The project does not aim to maximize its own scope. It aims at the smallest
thing that reliably produces the competence in §1.1.

### 1.4 The governing test

Every decision in this specification, and every decision made by an authoring
lane working from it, is subject to one test:

> **If the reader has to remember our names for things in order to apply the
> method to an unmarked page of Aquinas, the architecture has failed.**

The method must survive being forgotten. What the reader retains after the
book is closed should be six questions in ordinary English and the habit of
asking them, not a vocabulary belonging to this project.

### 1.5 The eight standing rules

The whole book rests on eight rules. They are stated here in full because
every later section elaborates one or more of them. They may be cited in this
specification, and in author-side checklists, as `S1` through `S8`. They are
never printed beside a passage as labels for the reader to decode.

- **S1 Source is not warrant.** A citation establishes that an author held a
  proposition. It does not establish that the proposition is true. (§5)
- **S2 Definition is not discovery.** An argument whose conclusion is
  guaranteed by its own definitions has unpacked a vocabulary, not found
  something out about reality. (§3)
- **S3 Prose is canonical.** Symbolic notation appears only where the text can
  name the ambiguity, inference, scope, or dependency it makes easier to see.
  (§9)
- **S4 Bound the conclusion.** Every worked argument states what has been
  established, and what has not yet been established. (§7)
- **S5 Classify the denial.** Every worked argument says which of the five
  kinds of denial rejecting its burden-bearing premise would be. (§8)
- **S6 No retrojection.** Modern pedagogical devices, including this book's
  own six questions, are never attributed to Aristotle, to Aquinas, or to the
  tradition. (§11)
- **S7 A revealed premise stays labelled.** It is never laundered into a
  result of natural reason, and it is never required to carry a metaphysical
  proof it never claimed. (§6)
- **S8 State a rival at its strongest.** A rejected position appears in the
  form its ablest defender would accept. (§8)

Eight rules and six questions are the whole of the machinery. A reader who
holds these fourteen things holds the method.

### 1.6 The reader

The book assumes an intelligent adult reader with no formal training in
scholastic philosophy or symbolic logic, capable of sustained attention to a
difficult page, and interested in the truth of the matter rather than in the
history of opinion. The reader is presumed sympathetic to the tradition and
unwilling to be managed by it.

The book does not assume the reader can read Greek or Latin. Technical terms
in those languages appear where the historical vocabulary itself matters, and
are always glossed at first use.

### 1.7 Relation to version 1

Version 1 of this specification, at commit
`92543fec1b0856b50f07eb6070734eeb3814f0a8`, described a different book: a
rigorous textbook teaching the construction, inspection, defense, refutation,
and repair of metaphysical demonstrations by means of a modern
proof-engineering apparatus. It ran to thirty-six chapters and specified
formal proof records, a fourteen-part audit of every argument, eleven
numbered conditions on demonstration, several closed vocabularies of
abbreviations, allocation ranges for identifiers, machine-readable
proposition ledgers, and automated acceptance checks.

That architecture was over-engineered for the purpose in §1.1. Its apparatus
had become the subject of study. A reader trained on it would have learned to
operate a notation rather than to read a page.

Version 2 deletes the apparatus and keeps the philosophy. What survives from
version 1, in translated form, is listed at §17.6; what was removed is listed
there also. Later agents must not restore any of it. Where an authoring lane
finds itself reinventing a code of abbreviations, it has rediscovered version
1's mistake.

Version 1's genuinely valuable work was its verified historical research.
That survives, condensed, at §11 and Appendix A.

### 1.8 Status of this specification

This document is the governing architecture. It binds every later authoring
lane. Sections §1 through §10 state the method; §11 states how the book
handles history; §12 through §15 specify the curriculum, examples, exercises,
and the sample that must be produced first; §16 through §18 govern authoring,
acceptance, and what remains open.

Where this specification is silent, an authoring lane must ask rather than
invent. Where this specification and an authoring lane's convenience
conflict, this specification governs.
## 2. The reading frame: six questions

### 2.1 The frame

The method is six questions, asked in ordinary English, of any passage that
appears to be arguing for something.

| | Question | What it asks |
|---|---|---|
| 1 | **Claim** | What exactly is being asserted? |
| 2 | **Meaning** | What do the important terms mean here? |
| 3 | **Warrant** | Why am I supposed to accept each important premise? |
| 4 | **Burden** | Which sentence is doing the real philosophical work? |
| 5 | **Consequence** | What has actually been established if I grant it? |
| 6 | **Denial** | What follows if I reject the burden-bearing premise? |

These six names are fixed for the whole book. They are ordinary words chosen
because a reader can remember them without effort and can say them to himself
while reading. No lane may rename them, and no lane may add a seventh.

The frame is the book's core operational method. Every worked passage in
every lesson is analysed under it. Every exercise trains one or more of its
questions. The vertical slice (§15) exists to show it working on a real page.

### 2.2 Claim — what exactly is being asserted

The first task is to state the claim as the author is actually making it,
neither weakened nor strengthened.

This is harder than it sounds, and it is where most misreading happens. An
author writing in a formed tradition compresses. He states a conclusion that
carries qualifications settled three books earlier. He uses a term whose
sense was fixed by a distinction he does not repeat. He asserts something
about *whatever is moved* that a modern reader will hear as a claim about
*motion in general*.

Every analysis must produce two things under this question:

1. **The claim as the author states it**, in the author's own words, quoted
   accurately, with the qualifications he attached.
2. **A plain-language reading** — a careful restatement that removes
   unnecessary school vocabulary without flattening a real distinction.

The plain-language reading is a required element, not an optional aid. It is
also the most dangerous element in the book, because a restatement that
loses a qualification has silently replaced the author's claim with a
different and usually weaker one. The rule is: a plain-language reading may
simplify the *diction* and may not simplify the *claim*. Where a technical
term cannot be replaced without loss, it is kept and glossed, and the
analysis says why it could not be replaced.

A useful discipline: after producing the plain-language reading, ask whether
the author would accept it as a statement of his position. If he would
object, the restatement is wrong, however much clearer it reads.

### 2.3 Meaning — what the important terms mean here

The second task is to fix the senses that the argument's validity depends on,
and only those.

Not every term needs defining. The analysis identifies the words that are
(a) technical, (b) doing work in the inference, or (c) ambiguous between a
technical and an ordinary sense, and it fixes those. A term that appears once
in an illustration does not need a paragraph.

Three things must be recorded where they are present:

- **Terms with a technical sense** that differs from ordinary usage, with the
  sense the author gives them. *Potency*, *act*, *accident*, *per se*,
  *substance*, *cause*, *principle*, *nature*, *necessary* all differ from
  their ordinary English cognates, sometimes drastically.
- **Distinctions the argument relies on**, stated as distinctions. The
  scholastic habit of distinguishing is not pedantry; a distinction is
  frequently the entire content of a move, and an argument can be destroyed
  by ignoring one or rescued by drawing one.
- **Terms whose sense shifts** between one occurrence and another. This is
  the single most productive diagnostic in the book. An argument that is
  valid on one reading of a term and true on another is not sound; it is
  equivocal. Where a shift is present, the analysis must show both readings
  and say which one each premise requires.

The Meaning question is answered *before* the argument is evaluated, and the
answers are not permitted to change once evaluation begins. A reader who
adjusts a definition mid-analysis to save an inference has stopped reading
and started defending.

### 2.4 Warrant — why I am supposed to accept each premise

The third task is to say, for each premise that matters, what kind of thing
is being offered in support of it. §4 specifies the eight kinds and how to
tell them apart.

Two points belong here, in the frame itself.

First, **warrant attaches to premises, not to arguments**. "This argument is
well-warranted" is not an answer. The analysis proceeds premise by premise,
and its value comes from the fact that the premises usually turn out to have
different kinds of warrant. A typical metaphysical argument mixes a
definition, an appeal to common experience, a result taken as established
earlier, and one substantive metaphysical principle. Seeing that mixture is
half the work.

Second, **the text often does not say**. Authors formed in the tradition
rarely announce that a given sentence is definitional and the next one is a
principle; the distinction was obvious to their trained readers. The analysis
must therefore make a judgement, and must say that it is making one. Where
the text genuinely underdetermines the kind of warrant, the analysis says so
and works through both readings rather than choosing silently.

### 2.5 Burden — which sentence does the real work

The fourth task is to find the **burden-bearing premise**: the smallest
proposition or transition on which the philosophical result actually turns.

The test, and the reader should learn to say it in these words:

> What is the first proposition here whose truth is not supplied merely by
> vocabulary or by a previous citation?

Working through a passage sentence by sentence, most sentences turn out to be
definitional, or to follow from what has been granted, or to be reports of
what someone held. Somewhere among them is a sentence that is none of those:
a substantive claim about reality that the argument needs and that nothing in
the argument establishes. That sentence is the burden.

Finding it is the central skill the book teaches. Its consequences are
practical: it tells the reader where to concentrate, what to read further
about, what an opponent would attack, and what the argument is actually
asking him to believe. It also frequently shortens a long dispute, because
two parties arguing about a conclusion are often disagreeing about a single
premise neither has stated.

An argument may have more than one burden-bearing premise. The analysis names
each. An argument may also have none, in which case the analysis says so
plainly: everything in it follows from the definitions, and it has established
a fact about the vocabulary. §3 governs that case, and it is not a rare one.

### 2.6 Consequence — what has been established

The fifth task is to state exactly what follows if the burden-bearing premise
is granted, and to stop there.

Two elements are required:

1. **What follows.** Stated in the weakest form that the argument actually
   supports, with its scope and its modality as the argument licenses them
   and no stronger.
2. **What is not yet established.** A short, conspicuous statement naming
   what the surrounding tradition commonly claims at this point and what this
   argument has not reached.

The second element is required and may not be omitted as obvious. Its purpose
is to hold open the gap between a conclusion and its usual destination. An
argument may validly establish that there is a first unmoved mover in a
certain ordered series without having established that it is one, that it is
simple, that it is intelligent, or that it is God. Each of those is a further
argument, and the tradition knows this perfectly well: Aquinas argues the
divine attributes in separate later questions precisely because the *viae* do
not deliver them. A reader who has not been shown the gap will import the
destination and will then be unable to say what any individual argument
accomplished.

§7 specifies this question in detail, including the recurring ways a
conclusion gets strengthened in transit.

### 2.7 Denial — what rejecting the burden costs

The sixth task is to ask what happens to a person who declines the
burden-bearing premise, and to classify the answer accurately among five
possibilities: contradiction, conflict with experience, explanatory cost,
commitment to a rival framework, or mere non-assent. §8 specifies these.

This question does more work than any other to break the appearance of a sea
of authoritative assertion, because it converts the whole argument into a
concrete alternative. It also protects the tradition from a bad defence. The
claim that denying a scholastic premise is *incoherent* is often false, and
making it where it is false discredits the cases where it is true. Frequently
the honest answer is that denial commits the reader to a developed rival
account, which then has to be examined on its own merits, or that denial
costs an explanation the reader may or may not think he needs.

### 2.8 The frame is not a pipeline

The six questions are an order of exposition, not a strict order of
discovery. In practice a reader finds the burden and only then realises which
term needs a sharper definition, or reaches the consequence and discovers the
claim was misstated. Iteration is normal and must be shown as normal.

Two constraints govern the iteration:

- The **finished analysis** is presented in the order 1 through 6, because
  that order is what makes an analysis comparable to another and legible to
  someone else.
- A revision made late may not be concealed. Where working out the
  consequence forced a change to the plain-language reading, the analysis
  presents the corrected reading and, when the correction is instructive,
  shows the mistake. The book should include at least one worked example in
  which an initial reading is revised in the course of the analysis.

### 2.9 What the frame is not

- It is not a form to be filled in. An analysis is prose, organised under six
  headings, in which the headings can be dropped without the analysis
  becoming unintelligible.
- It is not a scoring system. There is no verdict computed from the six
  answers, no grade, and no pass mark. The output is understanding, and
  understanding is judged by whether the reader can now say something true
  and specific about the passage.
- It is not a taxonomy to be completed. Where a question has no interesting
  answer for a given passage, the analysis says so in a line and moves on.
  A page of dutiful non-answers is a defect.
- It is not neutral between good and bad arguments, and it does not pretend
  to be. Applied honestly, it distinguishes them.

### 2.10 Scale of an analysis

A worked passage must be exposable on one page or one two-page spread. This
is a hard constraint on the book's design, and it is a substantive
constraint, not a typographical one: an analysis that cannot be compressed to
a spread has usually taken on too much text, and the remedy is to cut the
passage down to the sentence that matters.

Appendix B gives the one-page sheet in which an analysis is set out, and a
worked specimen of its use.
## 3. Definition versus discovery

### 3.1 The central distinction

One distinction governs the whole book:

```text
unpacking our concepts != discovering something about reality
```

Both activities are legitimate. Both are necessary. Metaphysics could not
proceed without careful conceptual work, and a tradition that has spent
centuries refining its vocabulary has usually refined it for good reasons.
The error the book exists to prevent is not the use of technical vocabulary.
It is the **transition**: the moment at which an argument stops explaining its
terms and begins telling the reader something about how things are, without
announcing that it has done so and without arguing for it.

The reader's recurring question, and it should become automatic:

> **Where does this argument stop explaining its terms and begin telling me
> something about reality?**

### 3.2 The distinction worked

Take a definition of the kind the tradition supplies:

> Potency means a capacity for an actuality not presently possessed.

From this it follows that:

> A thing with potency has a capacity for an actuality not presently
> possessed.

That inference is impeccable and it is empty. It tells us what we have decided
to mean by a word. Anyone who accepts the definition must accept the
consequence, and accepting it costs nothing, because nothing has been claimed
about any thing.

Now consider:

> The capacity invoked by change corresponds to a real principle or feature of
> the changing thing, and is not merely a description of possible future
> states.

This is a substantive claim about reality. It may be true. Much of the
tradition holds that it is true, and holds so for reasons. But it does not
follow from the definition of *potency*, and it cannot be established by
pointing out that potency is what the tradition means by the capacity in
question. It has to be argued, and an intelligent opponent can accept every
definition offered and still deny it, holding instead that talk of capacities
is a compendious way of describing what a thing will or may do under
conditions.

The distance between those two propositions is the distance the book teaches
the reader to measure. Notice what it is not: it is not the distance between a
clear claim and an obscure one. Both sentences are clear. It is the distance
between a claim about our words and a claim about the world.

### 3.3 The hostile-reader test

The operative test, applied to any argument that reaches a metaphysical
conclusion:

> **Could an intelligent opponent accept all of these definitions and still
> deny the substantive conclusion?**

- If **yes**, the argument has substantive content, and there is a
  burden-bearing premise somewhere that the opponent is denying. Find it. The
  argument is doing real work and can be evaluated.
- If **no**, the conclusion was contained in the definitions. The argument has
  established something about the vocabulary. Say so plainly, and then ask the
  further question: is the vocabulary itself the substantive claim in
  disguise? Frequently it is, and then the burden has migrated into the
  definition, which is where the analysis must go next.

The opponent in this test is *intelligent* and is not a fool. He understands
the terms, he grants the distinctions, he is not confused, and he still says
no. Constructing him honestly is a discipline in itself, and it is governed by
S8: he is given the strongest form of his position, not the form easiest to
refute.

The test also has a converse use. Where an argument's defenders claim that
denial is incoherent, the test locates whether that is so. If a competent
opponent can be constructed, denial is not incoherent, whatever else it may
be.

### 3.4 Definitions that carry claims

The hardest cases are not arguments that reason badly from honest
definitions. They are arguments whose definitions have substantive content
built into them.

A definition can smuggle a claim in at least three ways, and the book must
teach the reader to recognise each:

1. **The loaded definition.** A term is defined in a way that presupposes the
   very ontology at issue. Defining change as *the actualization of a
   potency* is not a neutral report of what change is; it embeds a specific
   account of change, and an argument that reaches an act/potency conclusion
   from it has assumed what it set out to show. The remedy is not to forbid
   the definition but to notice that accepting it is the substantive step, and
   to relocate the burden there.

2. **The reified abstraction.** A term that begins as a way of speaking about
   a thing comes to name a constituent of the thing. *A capacity* becomes *a
   principle in the subject*; *a way of being said* becomes *a mode of
   being*. The step may be right, but it is a step, and it is often taken in
   the space between two sentences. The reader must learn to ask, of any
   abstract noun in a metaphysical argument, whether the argument treats it as
   a way of describing something or as a feature of the thing described, and
   whether it has switched.

3. **The stipulated bridge.** A definition is offered that connects the
   conceptual vocabulary to the world by fiat: *by "real" we mean whatever is
   required to make change intelligible*. Anything reachable from such a
   definition is reachable trivially. The reader should be able to spot the
   pattern in which a definitional move does the work that an argument was
   promised for.

In each case the diagnosis is the same in form: the argument's real content
sits in a place the argument treats as preliminary. The analysis moves the
burden to where it actually is.

### 3.5 What the distinction does not license

The book must not teach, and no lesson may imply, that metaphysics is
verbal.

Three guards against that misreading are required in the finished work:

- **Definitions are not cheating.** Fixing a term precisely is the condition
  of arguing about anything. An argument that carefully defines its terms and
  then makes a substantive claim has done exactly what it should.
- **A conceptual result can be worth having.** Showing that two positions are
  incompatible, or that a familiar notion is incoherent, or that a
  distinction is required to state a problem, is a genuine result even though
  it is not a discovery about the furniture of the world. The book should
  include at least one case where the honest verdict is that the argument is
  conceptual and valuable.
- **The tradition often knows the difference.** Aristotle and Aquinas both
  distinguish what belongs to a thing's definition from what is demonstrated
  of it, and both have machinery for the distinction. The book presents the
  distinction as a recovery of something the tradition possessed and modern
  readers lack, not as a modern weapon against a naive tradition. S6 governs
  how that recovery is described.

### 3.6 Where this appears in the book

The distinction is installed as its own lesson (§12, Lesson 3), but it is not
confined there. Every worked example from Lesson 3 onward must make it
possible to see where definitional unpacking ends and ontological commitment
begins; this is acceptance test B (§17), and a worked example that does not
permit that judgement is defective regardless of its other merits.

The required example progression (§13) includes, adjacently, a sentence whose
truth is mostly definitional and a sentence that looks definitional but
carries a real ontological commitment. That pairing is the spine of the
lesson and may not be dropped.
## 4. Warrant: why you are supposed to believe it

### 4.1 The question

For each premise that matters, the reader asks: *why am I supposed to accept
this?* The answer is the premise's warrant.

The question is asked of premises one at a time. A metaphysical argument
almost never has a single kind of warrant throughout, and the interest of the
analysis lies in the mixture. Identifying that a passage rests on one
definition, one appeal to experience, one result carried over from an earlier
book, and one substantive principle is already most of the way to
understanding what the passage is asking of the reader.

### 4.2 The eight kinds

The book uses eight kinds of warrant, named in ordinary English. They are the
answers a text can give to *why should I believe this?*

1. **Definition** — it is true by what the terms mean. Nothing about the world
   is being asserted. See §3.
2. **Logical consequence** — it follows from propositions already accepted in
   the argument. The warrant is the inference, so the inference itself must be
   inspectable.
3. **Experience** — it rests on observation, or on something we plainly and
   commonly encounter. *That some things change* is the standing example, and
   it is a stronger premise than it looks.
4. **Prior result** — it was established earlier in the text, or elsewhere by
   an argument the author takes as available. This is a promissory warrant:
   its force is exactly the force of the argument it points to, and the reader
   must be able to find that argument or note that he cannot.
5. **Metaphysical principle** — a substantive claim about reality offered as a
   starting point. *Nothing comes from nothing.* *Whatever is moved is moved
   by another.* *A thing cannot give what it does not have.* These are not
   definitions and not observations, and they are where the philosophical
   action usually is.
6. **Hypothesis** — assumed for the sake of argument, or offered as the best
   available explanation. Legitimate, and frequently mislabelled: a conclusion
   reached by inference to the best explanation is not a demonstration, and
   §10 governs the difference.
7. **Revelation** — held on the authority of revealed teaching. Legitimate in
   its place, governed by S7 and §6, and never silently converted into any of
   the preceding kinds.
8. **Provenance only** — nothing has been offered except who said it.

### 4.3 Provenance only is a diagnosis, not a warrant

The eighth item is not a way of supporting a proposition. It is the finding
that no support has been supplied. It belongs in the list because the reader
must have somewhere to put the many sentences that arrive with a citation and
nothing else, and because giving it a name makes it visible.

When an analysis records *provenance only*, it has not refuted the
proposition. The proposition may be true, may be demonstrable, and may be
demonstrated three pages later. What the analysis has recorded is that **as
this passage stands**, the reader has been given a source and not a reason.
The proper response is to look for the argument elsewhere, and to note the
proposition as not yet established until it is found. §5 develops this.

### 4.4 Telling the kinds apart when the text does not say

Texts formed in the tradition rarely label their own premises. The following
diagnostics are what the book teaches, and they should be taught as
diagnostics that can fail rather than as an algorithm.

- **Definition or principle?** Ask whether an opponent could reject the
  proposition while still using the term in the author's sense. If he cannot,
  the proposition is definitional. If he can, it is substantive. This is the
  hostile-reader test of §3.3 applied premise by premise, and it is the single
  most useful move in the book.
- **Experience or principle?** Ask what observation would bear on it.
  *Some things change* answers immediately. *Whatever is moved is moved by
  another* does not, though it is often presented as though it did; it is a
  principle wearing the clothes of an observation.
- **Prior result or provenance only?** Ask whether the text points to an
  argument or to a person. "As was shown above" is a prior result and creates
  an obligation to check. "As the Philosopher says" is provenance, unless the
  argument is also supplied.
- **Logical consequence or hidden premise?** Ask whether the step really
  follows from what has been granted, or whether it needs something further
  that has not been stated. Suppressed premises are extremely common in
  compressed scholastic prose, and recovering them is not a hostile act; the
  author usually had one in mind and expected a trained reader to supply it.
  The analysis states the premise the argument needs and then asks what
  *its* warrant is.
- **Revelation or philosophy?** Ask whether the author himself treats the
  proposition as held by faith. Aquinas is generally explicit about this, and
  §6 governs the reading.

Where the diagnostics leave a premise genuinely undetermined, the analysis
says so and carries both readings forward. A confident misclassification is
worse than an acknowledged ambiguity.

### 4.5 Mixed and layered warrant

Two complications recur and must be taught rather than smoothed over.

**Mixed warrant.** A single sentence can carry more than one kind. *Whatever
is moved is moved by another* is presented sometimes as near-definitional,
sometimes as a principle grounded in an analysis of change, and sometimes as
supported by experience. The analysis must not choose the reading most
convenient for the argument. Where a premise's warrant is contested, the
analysis presents the candidate readings and shows what each costs: on the
definitional reading the premise is cheap but the conclusion may become
conceptual; on the substantive reading the conclusion is significant but the
premise now bears the burden.

**Layered warrant.** A prior result rests on its own argument, which has its
own premises, which have their own warrants. The reader is not obliged to
follow every chain to its end, but he is obliged to notice where a chain has
been left dangling and to record that the conclusion inherits whatever
weakness lies at the far end of it. An argument no stronger than the weakest
link it depends on has exactly that strength, and stating so is not
scepticism but accounting.

### 4.6 What the book must not do with the eight kinds

- It must not print them as labels beside every sentence of every passage.
  They are what the reader thinks with, not what the page is decorated with.
  A worked analysis may name the kind in a clause of prose.
- It must not treat the list as exhaustive of all possible support. It is a
  working list adequate to the texts the book reads. If a passage offers
  something genuinely outside it, the analysis describes what is offered in
  ordinary language rather than forcing it into a category.
- It must not rank the kinds by respectability. A definition is not a weak
  warrant; it is a warrant for a different sort of proposition. The failure
  the book targets is a mismatch between the kind of warrant offered and the
  kind of claim being made.
## 5. Source is not warrant

### 5.1 The rule

```text
SOURCE != WARRANT
```

That Aquinas wrote a proposition establishes that Aquinas held it. It does not
establish that it is true.

This is rule S1, and it is the rule that most directly addresses the reader's
original difficulty. The sea of authoritative assertion is produced by texts
in which attribution and justification are written in the same voice.
Separating them is the first thing that makes the water clear.

### 5.2 Three questions, kept apart

For any proposition in a text, three different questions can be asked, and
the book keeps them apart at all times:

- **Provenance** — who asserts it, and where. A matter of fact about texts,
  settled by citation.
- **Status** — what the proposition is doing in the argument: a definition, a
  distinction, a dialectical or probable argument, a demonstration claimed, a
  demonstration achieved, a theological conclusion, or the author's
  considered judgement. A matter of interpretation, settled by reading the
  text carefully.
- **Warrant** — why the proposition is supposed to be true. A philosophical
  question, settled, if at all, by argument.

Confusing the three produces most of the characteristic errors in reading and
in defending the tradition. A reader who takes provenance for warrant accepts
whatever is well attributed. A reader who takes status for warrant accepts
whatever is *called* a demonstration. A critic who takes provenance for
warrant thinks he has refuted a philosophy by discrediting a philosopher.

Note that status includes a distinction the book must hold firmly:
*demonstration claimed* is not *demonstration achieved*. That an author
presents an argument as a demonstration is a fact about the text; whether it
is one is a further question, and §10 gives the criteria.

### 5.3 What a citation does establish

The rule is not that citations are worthless. A citation establishes real
things, and the book must be precise about what they are:

- that the author held the proposition, or held something that has been
  interpreted as it;
- that the proposition belongs to a particular formulation of a tradition,
  which matters when the tradition is what one is trying to understand;
- that the proposition has been found worth holding by someone whose thought
  has quality and historical depth, which is a strong reason to take it
  seriously and to look for the argument;
- that a reading of a later text which contradicts it needs to explain itself;
- and, sometimes, that a proposition was uncontroversial among people who had
  thought hard about it, which is evidence, though not proof.

None of that is warrant for the proposition's truth. All of it is a reason to
do more work rather than less.

### 5.4 The name-removal test

The book's practical test for S1, and a recurring exercise (§14):

> Remove every proper name from the argument. Does it lose any of its
> philosophical force?

If the argument still stands, the names were doing scholarly work: locating a
position, crediting its author, situating a dispute. That is legitimate and
useful.

If the argument collapses, the names were doing philosophical work, and the
analysis has found either a *provenance only* premise or an argument that was
never more than an attribution.

This test is the operational form of acceptance test C (§17). It is also the
best available protection against a subtler failure, in which an argument is
carried not by any individual citation but by the accumulated weight of
citation: a passage in which every second sentence names an authority can feel
like a demonstration while containing no inference at all.

### 5.5 System-internal repetition

A second and harder case. An argument can avoid naked appeals to authority and
still fail to warrant anything, by circling inside its own vocabulary.

The naked form is easy:

```text
Aquinas says P.
Therefore P.
```

The instructive form is not:

```text
P follows from act and potency.
Why accept the relevant principle about act and potency?
Because that is what act and potency mean.
```

This pattern must be tested rather than dismissed, because it has two very
different resolutions and they look identical on the page.

- It may be that the conclusion **is** genuinely definitional. Then the
  argument has told us about the vocabulary, the analysis says so (§3), and
  the reader has learned something real and limited.
- Or it may be that a substantive claim has been **hidden inside the
  terminology**: the vocabulary was constructed to carry an ontology, and
  accepting the vocabulary is accepting the ontology. Then the burden has
  migrated into the definitions, and that is where the argument is to be
  examined.

Either resolution is respectable. What is not respectable is leaving the
question unasked, because unasked it produces the illusion of a demonstration
from nothing but a well-built terminology.

### 5.6 The burden-bearing premise

The rule and the test converge on the question the book returns to
constantly:

> **What is the first proposition here whose truth is not supplied merely by
> vocabulary or by a previous citation?**

That proposition is the burden-bearing premise. The phrase is ordinary
English and is used throughout the book as ordinary English. It is not a
label for a category; it names a thing the reader looks for.

Three outcomes are possible, and the reader must be equally comfortable with
all three:

1. There is exactly one such proposition. Usual, and the most useful result:
   the whole dispute has been localised.
2. There are several. Then the argument has several independent burdens, and
   the analysis names each, because an opponent needs to deny only one.
3. There is none. Everything in the passage is vocabulary or citation. The
   analysis says so. This outcome is not rare, and the book must include at
   least one worked case of it (§13, §14) so that the reader learns it is a
   legitimate finding rather than a failure of his own reading.

### 5.7 What this rule is not

It is not an argument against authority, tradition, or the reading of great
books. It is what makes reading them profitable.

A tradition transmits results, vocabulary, distinctions, and problems. Taking
its transmissions seriously is rational. What the rule forbids is treating
transmission as proof, which the tradition itself did not do: the medieval
practice of citing an authority and then examining objections to it exists
precisely because the citation was understood not to settle the matter.

The posture the book maintains throughout:

> A great author deserves serious attention because of the quality and
> historical depth of his thought, but philosophical claims stand or fall by
> their warrant rather than the prestige of their source.

Applied honestly, S1 increases respect for the tradition where its arguments
survive scrutiny, and increases precision where they do not. It is not a
device for winning arguments against the dead.
## 6. Revealed premises, theology, and natural reason

### 6.1 Four things to keep apart

Reading Augustine or Aquinas requires distinguishing four kinds of
proposition that appear in the same prose:

1. **A revealed premise** — held on the authority of revealed teaching, and
   presented by the author as so held.
2. **Theological reasoning from revealed premises** — valid argument whose
   starting points are revealed. The reasoning may be excellent; its
   conclusions carry the standing of their premises.
3. **A philosophical claim accessible to natural reason** — offered as
   establishable without appeal to revelation, and therefore answerable to
   argument that any competent reader can assess.
4. **Authorial judgement** — the author's considered opinion, offered as
   such: a reading of a predecessor, an assessment of how strong an argument
   is, a preference between two accounts.

The four are frequently adjacent. Aquinas will state a revealed truth, argue
from it, note that a philosopher reached something nearby by natural reason,
and add his own estimate of how far that natural argument reaches, in the
space of a single article. A reader who cannot separate the four will
misattribute the warrant of every one of them.

### 6.2 The labelling rule

Rule S7 has two halves, and both are needed:

- **A revealed premise stays labelled.** It is never laundered into a
  definition, an appeal to experience, or a metaphysical principle. An
  argument that quietly promotes a revealed premise into a naturally known
  one has misrepresented its own warrant, and the reader who accepts the
  promotion will believe a philosophical case has been made where it has not.
- **A revealed premise is never asked for a proof it never claimed.** The book
  must not demand a metaphysical demonstration of a proposition that the
  author explicitly treats as revealed. Doing so is not rigour; it is a
  category error, and it misreads the text.

### 6.3 The two symmetrical errors

The book guards against both, and must not correct one by committing the
other.

**Error one: theology in philosophical clothing.** A proposition held by faith
is presented as, or allowed to function as, a result of natural reason. The
argument then appears to establish by reason what it has taken on authority.
The remedy is to restore the label and to ask what the argument establishes
without that premise, which is frequently less, and sometimes nothing.

**Error two: philosophy defended by authority.** A proposition presented as
philosophically demonstrable is defended by appeal to ecclesial or authorial
authority when its argument is challenged. This is S1 again, in the setting
where it is most tempting. A claim advanced as available to natural reason has
accepted the standards of natural reason and cannot retreat behind authority
when those standards press.

Both errors are failures of bookkeeping rather than of piety, and the book
should present them that way.

### 6.4 Reading the tradition accurately on this point

The distinction the book teaches is not an external imposition. The tradition
draws it, deliberately and with machinery.

Aquinas distinguishes *sacra doctrina*, which proceeds from articles of faith,
from the philosophical disciplines, which proceed from principles known by
natural reason. He holds that certain propositions approached by faith can
also be reached by philosophical argument, and calls these the *praeambula
fidei*. He is explicit that this overlap is partial: some revealed truths are
not demonstrable at all, and he says so. He also treats certain claims as
demonstrable which later readers have doubted are, which is a substantive
dispute and not a scandal.

Appendix A carries the loci. What matters for the method is that the
distinction is the tradition's own, and that using it well makes Augustine
and Aquinas more intelligible rather than less. A reader who knows which
premises Aquinas took from revelation can finally see the shape of what he
thought reason could do on its own, which is the interesting question and is
invisible without the distinction.

### 6.5 Posture

The distinction must not be used to generate hostility toward authority, and
the book's tone must not suggest that a revealed premise is an embarrassment
or a concealed weakness. An author who states plainly that he holds something
by faith has been candid, and candour is what the method needs.

Nor may the distinction be used to insulate claims from examination. Where an
author presents a proposition as demonstrable, the demonstration is subject to
the whole frame, and the answer *but he was a saint* is not an answer.

The book's readers include people for whom the revealed premises are true.
Nothing in the method requires them to suspend that belief. What the method
requires is that they be able to say which of the propositions before them
they hold on that basis, because otherwise they cannot tell what their
philosophy is doing.

### 6.6 Where this appears in the book

The four-way distinction is installed in §12, Lesson 2, alongside the eight
kinds of warrant, since revelation is one of them. The required example
progression (§13) includes a theological proposition whose warrant is
revelation rather than metaphysical demonstration, and that example exists
specifically to give the reader a clean case before the mixed cases arrive.
Acceptance test C (§17) covers the second error; the first is covered by the
warrant-classification procedure in the same section.
## 7. Consequence: what follows and what does not yet follow

### 7.1 The two halves

Granting the burden-bearing premise, the reader asks what has been
established. The answer has two halves, and both are required in every worked
argument:

- **What follows** — stated in the weakest form the argument actually
  supports.
- **What does not yet follow** — a short, conspicuous statement of what the
  surrounding tradition commonly claims at this point and what this argument
  has not reached.

Rule S4 requires both. The second half is not a courtesy to opponents; it is
the element that makes the first half meaningful, because a conclusion whose
limits are unstated is indistinguishable from the whole doctrine it belongs
to.

### 7.2 Stating the conclusion at its actual strength

A conclusion has a scope, a modality, and a subject matter, and an argument
licenses particular ones. The discipline is to state the conclusion so that
every part of it is licensed:

- **Scope.** Does the argument establish something about all things of a kind,
  or about the ones under discussion, or about at least one? An argument about
  things that undergo change has not thereby said anything about things that do
  not.
- **Modality.** Does the argument establish that something *is* so, or that it
  *must* be so? The premises of a demonstration were supposed to be necessary,
  which is a demanding requirement; an argument from what happens establishes
  what happens.
- **Subject matter.** Does the argument establish something about the world, or
  about our concepts of it? §3 governs this, and it must be answered here
  rather than assumed.
- **Uniqueness.** Does the argument establish that there is such a thing, or
  that there is exactly one? These are different conclusions and the second
  almost always needs a further argument.

The plainest way to enforce this is to write the conclusion out, then attempt
to weaken each part in turn and ask whether the argument would still support
the weakened version. Whatever survives is the conclusion.

### 7.3 What is not yet established

The required statement takes this form: *the argument has reached X; the
tradition commonly proceeds from here to Y; nothing so far has established Y.*

Its purposes are three:

1. It stops the reader importing a destination. Metaphysical arguments are
   normally encountered inside systems whose conclusions the reader already
   knows, and knowing the conclusion makes every argument for it look stronger
   than it is.
2. It identifies what to read next. The gap between X and Y is a research
   question with an address.
3. It protects the argument from the discredit of overclaiming. An argument
   that genuinely establishes X is a real achievement, and presenting it as
   though it establishes Y invites the reader to dismiss it when it fails to.

The statement must be substantive. *Much remains to be said* is not a
statement of what has not been established; it is a decoration, and acceptance
test F (§17) treats it as a defect.

The standing example, and the book should use it early: an argument from
motion may establish that in a given ordered series there is a first member
that is not itself moved in the relevant respect. It has not established that
this member is unique, that it is simple, that it is intelligent, that it is
good, or that it is God. The tradition argues each of those separately, and
the honest reader who has been shown the gap can then follow those arguments
as arguments instead of as elaborations of a conclusion he has already
accepted.

### 7.4 The recurring overreaches

Conclusions get strengthened in transit, and they do it in a small number of
recognisable ways. The book should teach these as patterns to look for, in
ordinary English, without turning them into a memorised taxonomy. Seven recur
often enough to name:

1. **From is to must.** The argument shows that something is the case; the
   conclusion says it could not have been otherwise.
2. **From these to all.** The argument concerns the things under discussion;
   the conclusion is stated universally.
3. **From a concept to a thing.** The argument establishes something about
   what a term requires; the conclusion asserts that something answering to it
   exists.
4. **From at least one to exactly one.** The argument reaches a first, or a
   cause, or a principle; the conclusion reaches *the* first.
5. **From that to why.** The argument establishes that something is so; the
   conclusion claims to explain why it is so. §10 governs this, and it is the
   *quia* / *propter quid* distinction in modern dress.
6. **From a cause to this cause.** The argument establishes that there is some
   cause of the kind in question; the conclusion identifies it with a
   particular candidate.
7. **From the parts to the whole.** The argument establishes something of each
   member; the conclusion asserts it of the collection. Sometimes valid,
   frequently not, and the required example progression (§13) includes a case
   of it.

Each of these is a place to check, not a verdict. Several are sometimes
legitimate: a universal conclusion is warranted where the premises are
genuinely universal, and a move from parts to whole is warranted for some
properties. The reader's task is to notice that the move has been made and to
ask what licenses it.

### 7.5 Provisional standing

A conclusion reached under this discipline has a status the reader should be
able to state: established, established conditionally on a premise the reader
has not settled, not yet established, or established as a conceptual result
rather than a claim about reality.

The third of these is a legitimate resting place. An analysis that ends with
*this has not yet been established, and here is precisely what would be needed*
has done its work. It has converted an impression of authoritative assertion
into a specific open question, which is what the reader wanted in the first
place.

The book must not treat a negative or partial outcome as a failure of the
argument's author or of the analysis. §12 requires at least one full
reconstruction whose honest result is weaker, conditional, open, or
unsuccessful, and that lesson is where the reader learns that the method's
value does not depend on the arguments coming out well.
## 8. Denial: what rejecting the burden costs

### 8.1 The question

The sixth question asks what happens to someone who declines the
burden-bearing premise. It is the question that converts an argument from a
wall of assertion into a choice with a price, and it is where the book's
honesty is most easily tested.

Rule S5 requires every worked argument to answer it and to classify the
answer.

### 8.2 The five kinds of denial

1. **Contradiction.** Denying the premise commits the denier to a
   contradiction, or to denying something he has already granted. This is the
   strongest result and the rarest. Claiming it requires exhibiting the
   contradiction, not asserting that one lurks.
2. **Conflict with experience.** Denial requires denying something we plainly
   and commonly encounter. Strong, but weaker than contradiction: what we
   plainly encounter can be reinterpreted, and the reinterpretation must be
   examined rather than ridiculed.
3. **Explanatory cost.** Denial leaves unexplained something the premise
   explained. A real cost, and a real argument, but not a proof: a denier may
   accept the cost, may deny that the thing needs explaining, or may offer a
   different explanation.
4. **Rival framework.** Denial commits the denier to a different and developed
   metaphysical account. The dispute is then between two positions rather than
   between a position and an error, and the rival must be stated at its
   strongest before anything is concluded.
5. **Non-assent.** Denial merely declines a vocabulary or a system, with no
   contradiction, no conflict with experience, and no explanatory loss. The
   denier has not made a mistake; he has not joined a project.

### 8.3 The distinction that matters most

The book's most important work in this section is separating the first kind
from the fourth and fifth.

The tradition's defenders frequently claim that denying a scholastic premise
is incoherent. Sometimes that is exactly right, and the argument for it is one
of the strongest things in the tradition. Often it is not right, and what is
actually true is that denial commits the denier to a rival account, or that it
amounts to declining the vocabulary. Asserting incoherence where only
non-assent obtains does three kinds of damage: it misleads the reader, it
prevents the rival account from being examined, and it discredits the cases
where incoherence really is the answer.

The diagnostic is the hostile-reader test of §3.3 pushed one step further:
construct the denier explicitly. Give him a position. State what he says about
the phenomena the premise was introduced to handle. If he can be constructed
without contradiction, the denial is not a contradiction, whatever else it may
be, and the analysis says so.

### 8.4 Rivals at full strength

Rule S8: a rejected position appears in the form its ablest defender would
accept.

This is a requirement on the finished text, and a reviewer can check it. It
means that where the book says denial commits the reader to a rival account,
it must state that account accurately enough that someone who holds it would
recognise it, and must state its best reason. Where the book concludes against
it, the conclusion is reached against the strong form.

Straw men are not merely unfair; they are useless for the book's purpose. A
reader trained on weak opponents cannot interrogate a page of metaphysics,
because the objections he has learned to defeat are not the ones the page has
to survive.

### 8.5 Objection and reply

The tradition has a form for this, and the book should use it rather than
inventing one. *Objection and reply*, and the fuller *disputatio*, are
structures in which a position is stated, the strongest available objections
are set out, and each is answered. The medieval article's shape, with
objections first and the reply after the author's own determination, exists
because the objections were taken to be worth answering.

Three requirements govern the book's use of the form:

- An objection presented must be answerable in the terms in which it was
  presented. Weakening an objection in the reply is a defect.
- A **concession** is a legitimate reply. Where the objection succeeds in
  part, the book concedes that part and restates the conclusion at its reduced
  strength, which is §7's discipline arriving in a new place.
- An objection may be left standing. Where the book has no adequate reply, it
  says so. An honest unanswered objection is more useful to the reader than a
  reply that does not work.

### 8.6 What denial does not settle

Classifying a denial does not decide who is right. A denier who accepts an
explanatory cost may be making a bad trade or a good one, and the frame does
not adjudicate that. What the frame delivers is an accurate account of what is
at stake, which is what the reader needs before he can think about the
question at all.

Nor does the availability of a rival framework refute the argument. That two
coherent accounts are available means the question is open, and open questions
are the normal condition of metaphysics. The book should say so plainly, early,
so that the reader does not mistake the discovery of a coherent rival for a
defeat of the tradition.

### 8.7 Where this appears in the book

The five kinds are installed in §12, Lesson 5, together with counterexample
technique and the objection-and-reply form. From that lesson onward every
worked argument in the book carries a denial classification, and acceptance
test G (§17) checks that the classification is accurate rather than merely
present.
## 9. Notation: when it helps, when it hides

### 9.1 The reversal

Rule S3:

> **Prose is the canonical medium of metaphysical reasoning. Symbolic notation
> is used only where it makes a specific inferential feature clearer.**

This reverses the default that governed version 1 of this specification, which
required every substantial argument to be rendered formally and every
inference to be symbolized. That requirement produced pages that looked
rigorous and hid the philosophy.

The reversal is not hostility to logic. Formal logic is a precision instrument
and the book uses it. What changes is the burden of proof: notation must earn
its place on each occasion, and the argument for it must be statable.

### 9.2 What notation is licensed for

Symbolic notation is appropriate, and often the clearest available means,
where the point at issue is one of these:

1. **Quantifier scope** — whether *everything has a cause* means each thing has
   some cause or there is some cause of everything; whether *there is a first*
   is inside or outside the scope of a universal.
2. **Modal scope** — whether necessity attaches to the whole conditional or to
   its consequent, which is the classic site of fatalism arguments and of
   several bad readings of arguments for a necessary being.
3. **Contradiction** — exhibiting that a set of propositions cannot all hold,
   where the exhibition is clearer in symbols than in a paragraph.
4. **Identity** — where the argument turns on whether two descriptions pick out
   the same thing, and substitution is the operation at issue.
5. **Simple dependency** — where the structure of what depends on what is the
   content of the claim, and a diagram or a relation makes the structure
   visible.
6. **A formally invalid inference** — where displaying the form is the fastest
   honest way to show that the conclusion does not follow.
7. **Two genuinely different formal readings** — where a sentence admits more
   than one structure and the difference matters, and the point is precisely
   that the prose is ambiguous between them.

The summary rule:

> **Symbolize the logic around the metaphysics, not the metaphysics itself,
> unless the latter genuinely becomes clearer.**

### 9.3 The licensing sentence

Every displayed formula in the finished book must be accompanied, in the
surrounding prose, by a sentence that says what it makes easier to see.

This is a hard requirement and it is mechanically checkable. A reviewer
locates each formula and looks for the sentence. A formula with no such
sentence is deleted, not revised. Acceptance test D (§17) is exactly this
procedure.

The requirement has a useful side effect: it is difficult to write the
licensing sentence for notation that is doing no work, so the rule tends to
remove the offending formulas before a reviewer sees them.

### 9.4 What must not be routinely symbolized

The following are not to be encoded as predicate letters, functions, or formal
relations merely to make a page look rigorous:

act; potency; participation; essence and existence; analogy; form and matter;
causation; grounding; metaphysical dependence.

The reason is not that formalizing them is impossible. It is that the
interesting questions about each of them are questions about what the term
means and whether it picks out anything real, and a predicate letter answers
neither while appearing to have settled both. Writing `Potency(x)` does not
tell the reader whether potency is a real principle in the thing or a
description of what the thing may become, which is the entire dispute.

Where an argument genuinely turns on the *form* of a claim involving one of
these notions, notation is permitted under §9.2 and the licensing sentence
must name the feature. The prohibition is on routine encoding, not on thought.

### 9.5 Failure A: symbols that hide the question

The first pseudo-formalism failure. Consider:

```text
forall x (Change(x) -> Potency(x))
```

offered as the formalization of an argument about change and potency. The
formula is well-formed and may even be a correct rendering of a sentence in
the text. It is nonetheless a failure of analysis if the live questions are:

- what *change* means here, and whether every case the argument needs counts as
  change in that sense;
- what *potency* means here;
- whether potency is a real feature of the subject or a way of describing its
  possible future states;
- why change should license the ontological claim at all.

Every one of those questions has been packed inside a predicate letter. The
formula displays the argument's shape and conceals the whole of its content,
and a reader who accepts the formula as the analysis has been moved past the
difficulty without noticing.

The diagnostic, and it is a reviewer's procedure as well as a reader's: look
at each predicate letter and ask whether the open question is inside it. If it
is, the formula is hiding the question and the analysis belongs in prose.

### 9.6 Failure B: tautology dressed as discovery

The second failure. An argument that defines its terms so that the desired
result follows is logically immaculate and philosophically empty. Formalizing
it makes it worse, because the formal presentation supplies an appearance of
rigour precisely where the substance is missing, and a valid derivation from
definitions is the easiest thing in the world to display.

The book must therefore keep two things visibly apart:

```text
definitional consequence
```

and

```text
substantive metaphysical conclusion
```

The test is the hostile-reader question of §3.3, and it is applied to the
formal presentation as readily as to the prose: could an intelligent opponent
accept all the definitions and still deny the conclusion? If not, the
derivation is a derivation about the vocabulary, and presenting it as a result
about reality is the defect. §17 gives the reviewer's procedure.

### 9.7 Conventions, kept small

Where notation is used, the book uses ordinary first-order notation and
ordinary modal operators, introduced at first use in a line or two, with no
apparatus beyond what the example needs. Specifically:

- No formal system is presented for its own sake. There are no axioms to
  learn, no proof rules to memorise, and no derivations more than a few lines
  long.
- Notation is never required of the reader. No exercise asks the reader to
  produce a formalization except where the exercise is precisely about a scope
  ambiguity, and even there a prose answer that identifies the ambiguity
  correctly is a complete answer.
- Where a symbol and an English phrase are equally clear, the English phrase
  is used.

### 9.8 A book with few symbols is a success

Some of the best worked analyses in the finished book may contain no symbolic
notation at all, and the specification anticipates this. §13 requires that at
least three of the nine worked examples carry none, and permits the vertical
slice (§15) to carry none if its chosen passage has no genuine scope or modal
question.

An authoring lane that finds itself with a formula it cannot write a licensing
sentence for has found evidence that the analysis is not yet finished. The
formula is the symptom; the prose is the cure.
## 10. Demonstration and its limits

### 10.1 Why this section comes last

Version 1 of this specification began from demonstration: the reader was to be
trained in constructing formal proofs and then turned loose on texts. Version 2
reverses the order. Reading accurately comes first; constructing or evaluating
a complete metaphysical demonstration comes last, as the culmination.

The reason is not that demonstration is unimportant. It is that a reader who
does not yet distinguish a definition from a principle, or provenance from
warrant, cannot tell whether a demonstration has occurred, and will therefore
either accept every argument presented as one or reject the category
altogether.

Demonstration is not discarded. The reader must end the book understanding what
a successful metaphysical demonstration would look like, and able to say of a
given argument whether it is one.

### 10.2 What demonstration was supposed to be

In the tradition the book reads, a demonstration is not merely a valid
argument. It is a valid argument whose premises meet demanding further
conditions: they must be true, they must be prior to and better known than the
conclusion, they must be causes of the conclusion, and they must hold
necessarily and of the subject as such rather than incidentally. The middle
term is not a device for getting from premises to conclusion; it is supposed
to be the cause in virtue of which the conclusion holds.

§11 and Appendix A give the historical detail with citations. What matters for
the method is the shape of the requirement: **validity is the cheapest part of
a demonstration**. Everything difficult is in the premises and in the middle
term.

This yields the book's most useful negative result. An argument can be
perfectly valid, its premises can all be true, and it can still fail to be a
demonstration, because the premises are not prior, or not necessary, or not
causes. A reader who knows only validity has no way to see this and will
credit such an argument with more than it has achieved.

### 10.3 Showing that, and showing why

The tradition's distinction between demonstration *quia* and demonstration
*propter quid* is the single most useful historical instrument the book
recovers, and it must be taught precisely.

- A demonstration ***quia*** establishes **that** something is so. It may
  reason from an effect to its cause, and in that case the middle term is not
  the cause of the conclusion but something better known to us.
- A demonstration ***propter quid*** establishes **why** it is so. Its middle
  term is the cause, and the demonstration exhibits the conclusion as flowing
  from that cause.

The distinction matters for the reader for three reasons:

1. It separates two achievements that ordinary language runs together. Knowing
   that something must be the case is not knowing what makes it the case.
2. It licenses an argument to be sound and still not explanatory, which
   dissolves a common confusion about what the classical arguments for a first
   cause could have accomplished even if they succeed.
3. It is the tradition's own distinction, drawn for its own reasons, and
   Aquinas uses it explicitly about arguments the reader will encounter,
   including the argument from effect to cause where the effect takes the
   place of the definition of the cause.

The overreach named at §7.4 as *from that to why* is the failure of this
distinction in practice.

### 10.4 Demonstration is not explanation

A related distinction that the book must keep firm.

An explanation makes something intelligible to a mind. A demonstration
establishes a conclusion from premises of a certain kind. The two coincide in
the case of demonstration *propter quid*, which is why they are easy to
conflate, but they come apart in both directions:

- A demonstration *quia* establishes without explaining.
- An explanation may illuminate without establishing anything: an account may
  render a phenomenon intelligible, satisfy the mind, unify a body of
  observations, and still not show that it is true. Inference to the best
  explanation is a real form of reasoning with a real claim on us, and it is
  not demonstration. §4's sixth kind of warrant is where such reasoning
  belongs.

The practical consequence for the reader: the feeling of illumination is not
evidence of proof. A passage that suddenly makes a difficulty dissolve has
done something valuable and may have demonstrated nothing.

### 10.5 Dialectic and demonstration

The tradition also distinguishes demonstration from dialectical argument,
which proceeds from what is granted, or commonly held, or held by the wise,
rather than from necessary principles known as such.

Dialectic is not a defective demonstration. It is a different instrument, and
much of the most valuable argument in metaphysics is dialectical: examining
what is commonly held, drawing out its consequences, showing that two received
opinions conflict, clearing the ground for a principle that cannot itself be
demonstrated because it is a starting point.

The book must teach the reader to recognise dialectical argument and to value
it correctly, which means neither dismissing it as mere opinion nor crediting
it as proof. Where an author is arguing dialectically, saying so is a piece of
accurate reading, not a criticism.

### 10.6 What the reader must be able to say

By the end of the book the reader should be able to take an argument
presented as a demonstration and say which of these it is:

- a demonstration *propter quid*, establishing the conclusion through its
  cause;
- a demonstration *quia*, establishing that the conclusion holds, without
  exhibiting why;
- a valid argument from true premises that is not a demonstration, because a
  premise is not prior, not necessary, or not a cause, and to say which;
- a dialectical argument, proceeding from what is granted or commonly held;
- an inference to the best explanation;
- an argument whose conclusion follows from its own definitions (§3);
- an argument whose apparent support is provenance only (§5);
- an invalid argument.

That list is the book's exit competence in its most compressed form. Notice
that it can be applied only by someone who has already done the work of the
six questions, which is why this section is last.

### 10.7 The honest possibility

The project is not premised on metaphysical demonstrations being plentiful.

It is a possible outcome of this method, applied honestly, that a traditional
argument establishes less than is commonly claimed: that it is a demonstration
*quia* where it was presented as *propter quid*, or a dialectical argument
where it was presented as a demonstration, or a conceptual result where it was
presented as a discovery. Such a finding is acceptable and valuable, and §12
requires the book to contain at least one worked case of it.

The opposite outcome is equally possible and must be equally available. Where
an argument survives this examination, the reader has something better than
the impression of authority: he has a claim he can state precisely, a premise
he has inspected, a conclusion he knows the bounds of, and an account of what
denying it would cost. That is what it is to have understood a piece of
metaphysics, and it is the whole purpose of the book.
## 11. What the tradition actually held

### 11.1 Why the history is in this book

The book recovers a lost argumentative formation; it does not invent a system for verifying
metaphysical truth. The reader's difficulty with a page of Aquinas is largely that of a reader
never trained in the skills the page assumes, and the book must teach those skills as skills
rather than as history: grammar in the strong sense, which is working out what is actually
being said; dialectic, which is reasoning from what an opponent will grant; distinction, which
is separating two senses carried by one word; objection and reply; *disputatio*, in which a
position is held against its best attack; demonstration; *demonstratio quia* against
*demonstratio propter quid*; the middle term as the explanatory cause; and over all of these
the difference between showing *that* something is so and showing *why*.

Two rules follow, both checkable.

- **The history serves the reading skill.** A historical passage earns its place only if the
  surrounding text says what the reader can now do with a page of metaphysics that he could not
  do before; a reviewer may strike any paragraph for which that sentence is missing.
- **A survey is not the destination.** Lesson 0 (§12) orients the reader in about the space
  this section covers and no more. The reference material lives in Appendix A, which is
  author-side and is not printed as a chapter.

### 11.2 What the book must get right about Aristotle

The book's account of *apodeixis* must contain the following. Appendix A holds the quotations.

- **Scientific knowledge.** We know a thing without qualification when we know the cause on
  which the fact depends, as the cause of that fact and no other, and know the fact cannot be
  otherwise; its object is therefore necessary (*Post. An.* I.2, 71b8–16; *Nic. Eth.* VI.3,
  1139b18–22).
- **Demonstration defined.** A syllogism productive of such knowledge, whose premises must be
  true, primary, immediate, better known than the conclusion, prior to it, and causes of it
  (I.2, 71b17–72a8) — "better known" meaning better known in nature, not to us (71b29–72a5).
- **Principles.** A principle is an immediate proposition with nothing prior to it: axioms are
  common to several sciences; the theses proper to one science are hypotheses, which assert
  that a subject is, and definitions, which do not (I.2, 72a8–25). Demonstration can be
  neither circular nor endless, so not all knowledge is demonstrative (I.3, 72b5–73a20).
- **Prior knowledge.** Teaching starts from something known: in some cases that the thing is, in
  others what the term means, sometimes both (I.1, 71a11–17). The familiar threefold *an sit* /
  *quid sit* / *quia est* schema is later scholastic tradition, not this text (Appendix A).
- **Per se predication and the commensurate universal.** An attribute belongs *per se* either
  because the subject's definition contains it or because its own definition contains the
  subject, and the middle must be *per se*, not accidental (I.4, 73a34–b26); it is
  commensurately universal when it belongs to every instance essentially and as such, and
  demonstration must reach it in its primary subject (73b27–74a3).
- **The middle term is the cause.** Each of the four causes — definable form, necessitating
  antecedent, efficient, final — can be the middle term of a proof (II.11, 94a20–95a9), and a
  definition can serve as middle (II.8, 93b22–94a19).
- **Propter quid and quia.** Knowledge of the reasoned fact differs from knowledge of the fact
  when the premises are not immediate, when the better known of two reciprocals is taken as
  middle instead of the cause, when the middle is too remote, and when one science supplies
  the fact and a superior science the reason (I.13, 78a22–79a16). The planets do not twinkle
  because they are near, not the reverse (78a30–38).
- **Necessity.** Demonstrative knowledge rests on necessary premises, so there is no
  demonstration of the accidental or of chance (I.6, 74b5–75a17; I.8, 75b21–36; I.30, 88a5–17).
- **No crossing of genera.** A demonstration stays inside its subject genus, and one science
  proves another's theorem only where the sciences stand as subordinate to superior, optics to
  geometry and harmonics to arithmetic (I.7, 75a38–b20; I.13, 78b34–79a16).
- **How principles are grasped.** First premises are not reached by demonstration: the
  universal settles in the soul from perception through memory and experience, first premises
  come to be known by *epagōgē*, and *nous* grasps them (II.19, 99b18–100b17; *Nic. Eth.*
  VI.6, 1140b31–1141a8). The book must say the reading of this chapter is disputed.
- **Dialectic is not demonstration.** Dialectic argues from *endoxa*, opinions held by
  everyone, by most, or by the most reputable philosophers; its premises are neither
  necessary, primary, nor causes, and it is the path by which the principles of an inquiry are
  discussed at all (*Topics* I.1, 100a18–100b23; I.2, 101a25–37).

### 11.3 What the book must get right about Aquinas

- **The commentary is a literal exposition.** The *Expositio libri Posteriorum Analyticorum*
  follows Aristotle line by line in *lectiones*; it is not a set of independent questions (In
  PA I–II, Leonine, Rome 1882).
- **Scientia and its subject.** A science is specified by its subject under a formal account
  of that subject; the subject of metaphysics is *ens commune* (In Metaph., prooemium; Super
  Boet. De Trin. q.5 a.1, a.4).
- **Duplex est demonstratio.** Demonstration is twofold: through the cause, called *propter
  quid*, by what is prior without qualification; and through the effect, called *quia*, by
  what is prior for us. God's existence is demonstrable in the second way, and there the
  effect takes the place of the definition of the cause (ST I q.2 a.2 corp. and ad 2).
- **The middle when the essence is unavailable.** The middle of a *propter quid* demonstration
  is the *quod quid est*; where that is beyond us, what the name signifies (*quid significet
  nomen*), imposed from effects, takes its place, because the question *what it is* follows
  the question *whether it is* (ST I q.2 a.2 ad 2; In PA II lect. 1, 7, 9; Super Boet. De
  Trin. q.6 a.4 ad 2).
- **Per se nota quoad se and quoad nos.** A proposition is self-evident in itself when the
  predicate is contained in the account of the subject, and self-evident to us only if we know
  what its terms are; "God is" is self-evident in itself but not to us, which is why the
  argument from *that than which nothing greater can be thought* is refused (ST I q.2 a.1
  corp. and ad 2; SCG I cc. 10–11).
- **Analogy.** Nothing is said univocally of God and creatures; names are said analogically, by
  proportion, in a way lying between pure equivocation and simple univocity (ST I q.13 a.5),
  and in each name the perfection signified (*res significata*) is said of God more properly
  than of creatures while the mode of signifying (*modus significandi*) is not (a.3). The book
  must state the resulting difficulty: an analogical middle does not carry one and the same
  account in both premises, and so threatens a four-term fallacy — a difficulty constructed by
  the later tradition, not a theme of q.13 itself.
- **Sacra doctrina and the praeambula fidei.** Sacred doctrine proceeds from principles known
  by the light of a higher science, uses philosophers as extraneous and probable arguments,
  and treats what natural reason reaches about God as a preamble to the articles rather than
  an article of faith (ST I q.1 a.2; q.1 a.8 ad 2; q.2 a.2 ad 1; SCG I cc. 3–9).
- **Ordered series.** Infinite regress is impossible in causes ordered *per se*, where each is
  required for the effect, and is not judged impossible in causes ordered *per accidens*, as
  with a craftsman's succession of hammers or a man begotten by a man (ST I q.46 a.2 ad 7).
- **Resolutio and separatio.** Reason terminates in intellect by the way of resolution and
  proceeds from it by the way of composition, which is why metaphysics is first in dignity and
  last in learning; and metaphysics is reached by *separatio*, a negative judgment, not by
  abstraction from matter (Super Boet. De Trin. q.6 a.1; q.5 a.3).
- **The Five Ways are viae.** Aquinas's word is *viae*, and each ends in its own terminal
  phrase — a first mover moved by nothing, a first efficient cause, something necessary of
  itself, a cause of being and goodness in all things, something intelligent ordering nature
  to an end — each said to be what all men name God. Each concludes that something is, not
  what it is; the divine attributes are argued in later separate questions (ST I q.2 a.3
  corp.; qq.3–11; SCG I cc. 14–28).

### 11.4 The tradition and this book's frame

This subsection carries S6, no retrojection, into the historical material.

The six-question frame of §2 is a modern teaching aid, written to make distinctions the
tradition cared about visible to a reader not formed in it. It is inspired by the tradition; it
is not identical to it. It is answerable to the historical texts and not the reverse: where
frame and text pull apart, the text governs and the frame is corrected or bounded. Every
historical claim the book makes is a claim about a text and must be citable to that text.

Four prohibitions follow, each checkable by a reviewer with only the manuscript.

1. **No retrojection.** No chapter may write as though Aristotle or Aquinas used this book's
   frame. "Aristotle's Burden question" is a defect; "Aristotle's requirement that the middle
   term be the cause" is not.
2. **No silent equation.** A chapter placing a modern word beside a historical term must state
   the overlap and the difference, or cite §11.5.
3. **No apparatus in a historical voice.** Presenting the historical theory uses that theory's
   words: Aristotle's six conditions are "true, primary, immediate, better known, prior, and
   causes of the conclusion"; Aquinas's *duplex est demonstratio* is "demonstration through
   the cause and through the effect."
4. **No tradition without citation.** No chapter may appeal to "the tradition," "the
   schoolmen," or "classical logic" without an author, work, and locus.

### 11.5 Concordance: frame words and their antecedents

The table prevents false identification. The difference column is the working column; a
chapter quoting the overlap without the difference has misused it.

| Frame word | Historical antecedent | Overlap | Difference |
|---|---|---|---|
| Warrant | the six conditions on demonstrative premises and the kinds of principle (*Post. An.* I.2, 71b17–72a25) | both ask how a premise is known, not merely whether it is asserted | his conditions define a finished science; our eight kinds sort what an author actually offered, and two of them — revelation and provenance only — have no place in his theory of premises |
| Burden | the demand that premises be primary and immediate, and the refusal of circle and regress (*Post. An.* I.2–3) | both hunt the proposition on which everything else rests | his is a condition on a completed demonstration; ours is a diagnosis performed on a page that may be no demonstration at all |
| Consequence | the commensurate universal and the primary subject (*Post. An.* I.4, 73b27–74a3); each *via* concluding that something is, not what it is (ST I q.2 a.3) | both hold a conclusion to exactly the scope the argument earned | our conspicuous *not yet established* is a reader-side device; the tradition states the rule and leaves the bookkeeping to the science |
| Denial | objection and reply, *disputatio*, and the elenctic defence of non-contradiction (*Metaph.* Gamma 4, 1006a28ff.) | both measure a position by what refusing it costs | *disputatio* is a live exercise between two parties; our five kinds are a private classification a solitary reader applies to a text |
| *quia* / *propter quid* | *demonstratio quia*, *demonstratio propter quid* (*Post. An.* I.13, 78a22ff.; ST I q.2 a.2 corp.) | the pair is taken over from the tradition, not invented | the book uses it to grade what a passage achieved; Aristotle classifies modes of demonstration within a science, and Aquinas licenses argument from effects where the essence is unavailable |
| demonstration | *apodeixis* / *demonstratio* (*Post. An.* I.2, 71b18; ST I q.2 a.2) | both mean an argument yielding knowledge through the cause, not merely a valid inference | the historical sense carries necessity, immediacy, and a *per se* middle; a modern reader saying "demonstration" usually means only a valid argument, and the book must keep the two apart |
| principle | *archē* / *principium* (*Post. An.* I.2, 72a8) | both name a starting point not established by the argument using it | his principles are immediate and necessary; what this book calls a metaphysical principle is any substantive claim about reality offered as a starting point, contested or not |
| dialectic | reasoning from *endoxa* (*Topics* I.1, 100a18–b23) | both name argument from what will be granted rather than from causes | for Aristotle dialectic is a discipline with its own art and uses; here it names a status a proposition may have, implying nothing about what the author was practising |

Claim, Meaning, the plain-language reading, and *not yet established* have no antecedent as
frame elements, though the demand to fix what a name signifies before arguing is Aristotle's
own (*Post. An.* I.1, 71a11–17); no chapter may supply them with a historical pedigree.

### 11.6 Two things the book must not do with the history

1. **It must not treat the neo-scholastic manual tradition as identical with Aquinas.** The
   standing example is the "three degrees of abstraction," which the manuals make the principle
   dividing the speculative sciences; Aquinas distinguishes *separatio*, a distinct operation of
   the intellect, from two kinds of abstraction (Super Boet. De Trin. q.5 a.3). Where the book
   reports a manual formulation it must say so, and name the manual.
2. **It must not present a contested scholarly reading as settled.** Where Appendix A records a
   dispute — whether a demonstration from effects with a nominal definition as middle meets
   Aristotle's own conditions, whether an analogical middle can carry a syllogism, whether *Post.
   An.* II.19 describes a method or a natural process — the book says the question is open and
   names at least one position on each side.

### 11.7 Citation discipline

A historical passage is identified by author, work, canonical locus, and the edition or
translation used: Bekker page and line for Aristotle, the standard part-question-article or
book-chapter-number division for Aquinas. Chapter numbers of the *Posterior Analytics* vary
between editions, so the Bekker numbers govern. A translation is quoted as a translation, with
the translator named; no chapter may pass an English rendering off as the author's own words, or
rest an argument on a term of art without giving the original term.
## 12. Curriculum: nine lessons

Version 1 began from proof construction and treated reading as preparation. Version 2 reverses the order:
the reader learns what a passage claims, why to believe it, where the burden sits, what follows, and what
denial costs — and only in the last two lessons does he attempt or judge a demonstration. A reader who
cannot tell a definition from a metaphysical principle will build arguments in which the two are
indistinguishable and will not notice. Accurate reading is load-bearing; demonstration is what accurate
reading makes possible. The curriculum is not premised on demonstrations being plentiful, and no lesson may
require its material to succeed. That a traditional argument establishes less than commonly claimed is an
acceptable and valuable result, and Lesson 8 must contain at least one, stated as a finding.

Nine lessons, numbered 0 through 8; no lesson may be added. Each is specified with a purpose, what it
installs, its content, its worked material, its exercises, one exit test, and a page budget. Kinds of worked
example are named here and specified in `§13`; exercise types are named here and specified in `§14`.

### 12.0 Lesson 0 — What demonstration meant

**Purpose.** Afterward the reader can say what Aristotle and Aquinas were claiming when they called an
argument a demonstration, and can therefore see that a valid argument need not be one. **Installs.** No
frame question; standing rule S6 (no retrojection).

**Content.**
- Aristotle's conditions on demonstrative premises — true, primary, immediate, better known than and prior
  to the conclusion, and causes of it (*Posterior Analytics* I.2) — and that demonstration yields knowledge
  of the cause, not merely assent to a truth.
- Dialectic as argument from *endoxa*: it tests, clears ground, and defends principles that cannot
  themselves be demonstrated, and is not failed demonstration. *Disputatio* and the objection-and-reply form
  belong here, because their layout tells a trained reader which sentences are the author's own.
- *Demonstratio quia*, from effect toward cause, against *demonstratio propter quid*, from cause and showing
  why, with the middle term named in each.
- What formation the modern reader lacks: compressed argument, a distinction held across a page, a cited
  authority taken as a shared premise rather than a proof. S6 is stated here and honoured everywhere after —
  our six questions, eight kinds of warrant, and five kinds of denial are this book's devices and are never
  attributed to the tradition.
- **Worked material.** Two short exhibits, no full analyses: the valid/invalid pair from `§13`, showing that
  validity is cheap and demonstration is not; and one *quia*/*propter quid* pair on one conclusion.
- **Exercises.** Two or three, from the `§14` types for distinguishing *quia* from *propter quid* and for
  judging whether a valid inference is a demonstration. No transfer requirement yet.
- **Exit test.** Shown this lesson's valid/invalid pair, can the reader say why the valid member is still not
  a demonstration, and name the Aristotelian condition it fails? **Page budget.** 4–6 pages.

### 12.1 Lesson 1 — What is being said?

**Purpose.** Afterward the reader can restate a technical metaphysical sentence in plain language without
changing what it asserts, and can name which of its words carry a school sense. **Installs.** Frame
questions **Claim** and **Meaning**, including the plain-language reading.

**Content.**
- Separating the proposition from the sentence: subject, predicate, quantity, and every qualification present
  — *simpliciter* against *secundum quid*, *per se* against *per accidens*, absolutely against in a certain
  respect. The lesson must show one case where dropping such a qualification yields a paraphrase that is
  fluent, plausible, and a different claim.
- Which words are technical here and which ordinary. "Act", "potency", "form", "subject", "accident" and
  "being" may each be technical in one sentence and ordinary in the next, and the reader decides per
  occurrence. Reference is fixed the same way: whether "being" here means the act of existing, the totality
  of things, or the concept — and the argument may turn on which.
- What a plain-language reading may not do: strengthen or weaken the claim, add or move a quantifier, or
  silently resolve an ambiguity the author left open. An ambiguity is marked, not chosen.
- Distinction as a move: it answers an objection only if both senses can be identified independently of the
  objection. A distinction invented to absorb an objection is not an answer.
- **Worked material.** Two passages: the mostly definitional sentence from `§13`, carried only as far as
  Claim and Meaning; and one real sentence with three technical terms and one qualification, given with
  three candidate paraphrases of which two are rejected with reasons.
- **Exercises.** Five or six, from the `§14` types for plain restatement, marking technical senses, and
  preserving qualifications. At least one supplies a defective paraphrase for the reader to repair.
- **Exit test.** Does the lesson contain a solution that rejects a paraphrase which is grammatical and true,
  because it drops what the original carried, and names the word doing the work? **Page budget.** 5–7 pages.

### 12.2 Lesson 2 — Why am I supposed to believe it?

**Purpose.** Afterward the reader can go through a passage sentence by sentence and say, of each premise,
what is offered as a reason to accept it — and can recognize when nothing has been offered but a name.
**Installs.** Frame question **Warrant**; standing rules S1 (source is not warrant) and S7 (a revealed
premise stays labelled).

**Content.**
- The eight kinds of warrant applied sentence by sentence — definition, logical consequence, experience,
  prior result, metaphysical principle, hypothesis, revelation, provenance only — each introduced on a real
  sentence rather than defined in the abstract. Provenance only is a diagnosis and never a warrant, and the
  lesson must say so in those words.
- Keeping provenance, status, and warrant apart, so the reader can distinguish "Aquinas holds P", "Aquinas
  argues for P here", "Aquinas cites Aristotle for P", and "Aquinas claims to demonstrate P". The
  name-removal test: strike the author's name and ask whether any premise lost support.
- Prior result as a promissory note: a premise established elsewhere is unwarranted until located, and the
  lesson must show a case where the referenced place establishes less than the citing passage needs.
  Experience gets the same scrutiny: does "we plainly see that things change" report an observation, or
  already describe it in the vocabulary the argument will need?
- S7 in both directions. A revealed premise is labelled, never laundered into a result of natural reason, and
  never faulted for failing a proof it did not claim; conversely, a proposition offered as demonstrable by
  natural reason may not be defended by citing authority.
- **Worked material.** Two passages from `§13`: the theological proposition warranted by revelation, and the
  passage where provenance is easy to mistake for warrant. Both stop at Warrant; Burden waits for Lesson 3.
- **Exercises.** Five or six, from the `§14` types for labelling warrant by sentence, separating provenance
  from warrant, and removing author names. At least one gives two sentences that look alike and differ in
  warrant.
- **Exit test.** Given the revelation passage, can the reader say what it does establish on its own terms,
  neither dismissing it nor converting it into natural reason? **Page budget.** 6–8 pages.

### 12.3 Lesson 3 — Where is the real claim?

**Purpose.** Afterward the reader can locate, in a compressed argument, the first sentence whose truth is not
supplied by vocabulary or by a citation, and say why the sentences before it were not doing that work.
**Installs.** Frame question **Burden**; standing rule S2 (definition is not discovery).

**Content.**
- S2 and its test in the reader's own voice: could an intelligent opponent accept every definition in this
  argument and still deny its conclusion? If not, a vocabulary has been unpacked.
- The contrast the book turns on. "Potency means a capacity for an actuality not presently possessed", and
  hence "a thing with potency has such a capacity", is near enough to definitional unpacking; "the capacity
  invoked by change is a real principle in the changing thing and not merely a description of possible future
  states" is a claim about reality. The lesson must show that the second is where the argument becomes
  contestable, and must not settle whether it is true.
- The burden-bearing premise, named in that phrase and found by that question. Hidden premises are recovered
  by asking what the inference needs but does not say, stated in the author's idiom where possible and marked
  as the reader's reconstruction rather than the author's sentence.
- Nominal against real definition: the move between them is where commitments enter, because a definition
  offered as stating what something is has already asserted that there is such a nature. So definitional
  content is not always trivial — where a real definition is claimed, the essence claim is itself the burden.
  The related trap is a principle defended by appeal to what its terms mean, whose terms are defined so that
  the principle holds.
- **Worked material.** Two passages from `§13`: the sentence that looks definitional but carries an
  ontological commitment, and "whatever is moved is moved by another". The second is analyzed through Burden
  and left there; its consequences belong to Lesson 4 and its denial to Lesson 5.
- **Exercises.** Five or six, from the `§14` types for finding the first substantive ontological commitment,
  distinguishing definition from metaphysical premise, locating the burden-bearing premise, and repairing an
  argument without smuggling the conclusion into a definition. At least one is a defective argument whose
  defect is that its definitions guarantee its conclusion.
- **Exit test.** Does the lesson make the reader locate the burden in a passage the book has not marked up,
  and does its solution say why two earlier candidates are not it? **Page budget.** 7–9 pages.

### 12.4 Lesson 4 — What actually follows?

**Purpose.** Afterward the reader can state what a granted argument has established, in a sentence weak
enough to be true, and name what the tradition usually claims at that point but this argument has not
reached. **Installs.** Frame question **Consequence**, including the conspicuous "not yet established"
statement; standing rules S3 (prose is canonical) and S4 (bound the conclusion).

**Content.**
- Validity and soundness, and the consequence of S2 for inference: a valid argument from definitional
  premises yields a definitional conclusion. Validity does not upgrade the kind of claim.
- Scope, in ordinary English before any notation. "Everything moved has some mover" is not "there is
  something that moves everything moved"; "necessarily, if this is moved it has a mover" is not "if this is
  moved, it has a necessary mover". The lesson must show a real passage where the readings come apart and the
  argument needs the stronger one. The *de dicto* and *de re* labels may be mentioned once. Composition and
  division belong here: part to whole, whole to part, and the move from every member to the collection.
- Bounding, the lesson's main labour. "There is a first mover in this order of motion" is not "there is one
  God, pure act, creating from nothing". The "not yet established" statement must name the specific further
  claim commonly made here, not issue a general caution.
- S3 as a working restriction: notation appears only where the lesson states what ambiguity, inference, scope,
  or dependency it makes easier to see, and justifies each formula in a sentence. Act, potency, participation,
  essence, and causation are not symbolized as such.
- **Worked material.** Two passages from `§13`: the composition or dependence claim, and the argument with an
  illegitimate move from member to whole. Both carry an explicit "not yet established" statement, and
  "whatever is moved is moved by another" returns here for bounding only.
- **Exercises.** Five or six, from the `§14` types for weakening a conclusion to what follows, identifying what
  has not yet been established, and locating a hidden modal or quantifier shift. At least one asks the reader
  to reject a proposed bound as still too strong.
- **Exit test.** Can a reviewer find a case in which the reader's correct answer is a conclusion markedly
  weaker than the passage's own final sentence, with the gap named? **Page budget.** 6–8 pages.

### 12.5 Lesson 5 — What if I say no?

**Purpose.** Afterward the reader can say what rejecting a burden-bearing premise costs, and can tell a denial
that commits him to a contradiction from one that merely declines a vocabulary. **Installs.** Frame question
**Denial**; standing rules S5 (classify the denial) and S8 (state a rival at its strongest).

**Content.**
- The five kinds of denial — contradiction, conflict with experience, explanatory cost, rival framework,
  non-assent — each fixed on a real denial of a real premise.
- The book's central discrimination: separating rival framework and non-assent from contradiction. The lesson
  must show at least one case where a passage's rhetoric treats a denial as self-contradictory when it is
  non-assent to a vocabulary, and must say plainly that this is where traditional argument most often
  overreaches.
- Explanatory cost is a cost: leaving something unexplained is a real disadvantage and not a refutation, and
  the lesson may not let the reader convert it into one. Counterexamples are held to a matching discipline — a
  case that violates a *per se* restriction or an "in this respect" clause has not touched the claim.
- S8 in practice: a rival stated at least once at length, in the form its ablest defender would accept, such as
  a developed account on which causal powers are not real features of things, or on which dependence needs no
  first term. The reader must see a position, not an evasion. Replies are held to the same standard: one that
  restates the objection in house vocabulary and declares it answered is not a reply, and the lesson must
  contain such a pseudo-reply and name the failure. Concession is legitimate — an objection may be granted and
  the conclusion narrowed.
- **Worked material.** Three passages. The composition or dependence claim and "whatever is moved is moved by
  another" return from `§13`, now for Denial; and one fresh passage carrying a rival framework, developed at
  full strength here.
- **Exercises.** Four or five, from the `§14` types for finding the smallest denial that blocks an argument,
  classifying denial among the five kinds, and comparing a Thomistic explanation with a rival account. **The
  transfer requirement begins here:** in this lesson and each after it, at least one exercise must work on
  unannotated or lightly annotated real prose, not on a form the book has already filled out.
- **Exit test.** Does the lesson contain a premise whose denial the reader must classify as non-assent, with a
  solution saying why the denier incurs no contradiction and what he gives up? **Page budget.** 7–9 pages.

### 12.6 Lesson 6 — Demonstration and its limits

**Purpose.** Afterward the reader can say, of a valid and sound argument, whether it is a demonstration, and if
not, which condition it fails. **Installs.** No new frame question and no new standing rule; reinforces
Warrant, Consequence, S4, and S6 under historical pressure.

**Content.**
- The middle term and what it must be for a demonstration *propter quid*: a cause of the conclusion's holding,
  not merely a term that truly connects the extremes. The lesson must show a valid syllogism whose middle is a
  true but non-causal connector.
- *Quia* and *propter quid* worked on one claim, with the middle term identified in each and the direction of
  inference named. Demonstration is not the same as explanation: an argument can demonstrate *that* without
  explaining *why*, and an illuminating explanation can fall short of demonstration.
- *Per se nota quoad se* against *per se nota quoad nos*. The lesson must present a case where they come apart —
  a proposition self-evident in itself and not self-evident to us — and must not let the reader conclude that
  self-evidence is therefore whatever a reader finds obvious. What is relative to us is our access, not the
  proposition's truth.
- The ways a valid argument fails to be a demonstration: premises less known than the conclusion, a non-causal
  middle, merely probable premises, revealed premises, a conclusion that is not necessary, or an inference
  crossing from one subject matter into another. *Praeambula fidei* are treated here, and why a claim's being
  both reachable by natural reason and revealed does not make a theological argument for it a demonstration.
  "Not a demonstration" never means "worthless": dialectical argument, probable argument, and explanation each
  do work the lesson credits.
- **Worked material.** Two short exhibits: one valid argument diagnosed as not a demonstration with the failing
  condition named, and the *per se nota* case above. "Whatever is moved is moved by another" returns a third
  time, asked now whether it functions as a principle or as a conclusion.
- **Exercises.** Three or four, from the `§14` types for distinguishing *quia* from *propter quid* and for
  judging demonstration claims. At least one on unannotated or lightly annotated prose.
- **Exit test.** Given this lesson's own valid, sound, non-demonstrative argument, can the reader name the
  condition it fails without being told how many conditions there are? **Page budget.** 5–7 pages.

### 12.7 Lesson 7 — Reading real metaphysics

**Purpose.** Afterward the reader can take an unmarked page of serious metaphysics and produce the whole
six-question analysis unaided. **Installs.** No new frame question and no new standing rule; all six questions
and all eight rules are exercised together as scaffolding is withdrawn.

**Content.**
- Three or four passages of increasing difficulty. The first is worked with the book; the last is worked by the
  reader alone, with only a solution to compare against. Withdrawal must be visible: the lesson states, for
  each passage, what it supplies and what it withholds.
- One passage whose compression hides a step, reconstructed into explicit argumentative prose before any of the
  six questions is answered.
- One passage in which provenance is easy to mistake for warrant, so S1 is tested where it is hard rather than
  where it is obvious; and one from outside the Thomistic line — a rival scholastic or a contemporary treatment
  of the same problem — so the method is not tuned to a single idiom. Where the same claim is at stake, the
  reader compares burdens.
- The one-page analysis sheet of Appendix B, used from the second passage onward and unaided on the last.
- **Worked material.** Three or four real passages at the harder end of the `§13` progression, at least two
  quoted rather than reconstructed. Each ends with the plain-language reading, the burden named, the bounded
  conclusion, the "not yet established" statement, and the classified denial.
- **Exercises.** Four or five, each a full six-question analysis rather than a single-skill drill. At least two
  on unannotated prose; the last must be a passage discussed nowhere else in the book.
- **Exit test.** Is there a passage here for which the book supplies no partial analysis, only the text and a
  solution, whose solution matches the sheet the reader has been using? **Page budget.** 8–11 pages.

### 12.8 Lesson 8 — Can we demonstrate it?

**Purpose.** Afterward the reader can attempt a demonstration of a metaphysical claim, judge honestly whether
the attempt succeeded, and state the weaker result if it did not. **Installs.** No new frame question and no new
standing rule; S4, S5, S7, and S8 are held together under the pressure of building rather than reading.

**Content.**
- One or two serious metaphysical claims reconstructed from beginning to end: every premise's warrant
  classified, the middle term stated, the inference identified as *quia* or *propter quid*, the burden named,
  the conclusion bounded, the denial classified, and the strongest rival stated.
- At least one case where the honest result is weaker, conditional, open, or unsuccessful. The verdict is stated
  in a sentence, without hedging and without apology, together with what the argument does establish and what it
  does not reach. A conditional result written honestly looks like this: the conclusion holds if a named premise
  holds, that premise is a metaphysical principle, and its denial is a rival framework rather than a
  contradiction.
- Construction discipline mirroring S2: an attempt may not be rescued by adding a definition from which the
  conclusion follows, and the lesson must contain one repair refused on exactly that ground.
- Where the reader is left: the method retires into a pencil and the analysis sheet, and he keeps the six
  questions and none of our vocabulary. The lesson may not close by asserting that metaphysical demonstration is
  generally available or generally impossible — neither has been established, and saying so is the last use of S4.
- **Worked material.** Two full reconstructions: the fuller demonstration from `§13`, and one attempt that ends
  weaker or unsuccessful. Both are carried through the entire frame, and both state a rival at its strongest.
- **Exercises.** Two or three, long. One asks the reader to reconstruct and judge an argument the book has not
  analyzed; one asks him to weaken a failed argument into the strongest claim it does support. At least one on
  unannotated prose.
- **Exit test.** Does the lesson show a case where the right answer is that the demonstration fails, and does its
  solution state what the argument still establishes? **Page budget.** 8–11 pages.

### 12.9 Coverage

The nine budgets are 4–6, 5–7, 6–8, 7–9, 6–8, 7–9, 5–7, 8–11, and 8–11 pages. **They sum to 56–76 pages**,
inside the 50–80 budget of `§3`. In the table, `H` marks the primary home — the lesson responsible for
installing the item — and `r` marks required later reinforcement. Every item has exactly one home and at
least two reinforcements; a disagreement with the table is a defect in the lesson.

| | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| Claim | | H | r | r | | r | | r | r |
| Meaning | | H | r | r | r | | r | r | r |
| Warrant | | | H | r | | r | r | r | r |
| Burden | | | | H | r | r | r | r | r |
| Consequence | | | | | H | r | r | r | r |
| Denial | | | | | | H | r | r | r |
| S1 source is not warrant | | | H | r | | | r | r | r |
| S2 definition is not discovery | | r | | H | r | r | r | r | r |
| S3 prose is canonical | | | | | H | r | | r | r |
| S4 bound the conclusion | | | | | H | r | r | r | r |
| S5 classify the denial | | | | | | H | r | r | r |
| S6 no retrojection | H | | r | | | | r | r | r |
| S7 revealed premise labelled | | | H | | | r | r | | r |
| S8 rival at its strongest | | | | | | H | r | r | r |

### 12.10 What a lesson may not do

- No lesson may introduce a name, abbreviation, or code the reader must memorize in order to use the method. The
  six question words, the eight kinds of warrant, and the five kinds of denial are ordinary English and are the
  whole reader-facing vocabulary; `S1`–`S8` are author-side and must not appear in reader-facing pages.
- No lesson may require every inference to be symbolized. Notation appears only where the lesson states what it
  makes easier to see, and a lesson with no notation at all is acceptable.
- No lesson may add historical survey material beyond what Lesson 0 and Appendix A carry. Historical content
  elsewhere is admitted only where a passage cannot be read without it, in a sentence or two.
- No lesson may present a worked argument as succeeding when its own analysis does not show it succeeding, and
  none may require its examples to come out in the tradition's favour.
- From Lesson 5 onward, no lesson may end on a form the book has already filled out; the last exercise of Lessons
  5 through 8 works on real prose.

**Note on the lesson count.** The sequence and count are as proposed. Two points a reviewer may press. Lesson
6 is the shortest and the obvious candidate for merging into Lesson 0 or 8; it should stay separate, because
it is the only place where the reader judges a valid and sound argument to be a non-demonstration, and moving
it into Lesson 0 would demand the judgement before the reader can classify warrant. Lesson 4 carries three
installs and is the densest per page; splitting it would require a tenth lesson, and scope errors and
unbounded conclusions are one skill — an unbounded conclusion is usually a scope error nobody wrote down.
## 13. Worked examples: the required progression

### 13.1 What a worked example is

A worked example is a prose analysis — not a formal record — of one passage under the six headings of §2,
with the plain-language reading under Claim, each important premise assigned one of the eight kinds of §4
under Warrant, the burden-bearing premise named under Burden, the **Not yet established** note under
Consequence, and the denial classified among the five kinds under Denial. The passage stands beside it as
its author wrote it, in translation, with its locus. One to three pages each, four for Example 4, eighteen
for all nine. Every locus printed must also appear in Appendix A. No tenth example may be added without
deleting one. Each specification below fixes five things, and a reviewer checks a draft against all five:
**Exposes**, **Material**, **Frame**, **Notation**, **Outcome**.

### 13.2 Three standing rules for this section

- **No example is symbolized because it matters.** Notation appears only where the **Notation** line names
  the feature it exposes. Importance and fame are not reasons (S3, test D).
- **At least one example ends weaker than the tradition ends.** Examples 4 and 9 must each close
  conditional, bounded, or open. A book whose every example closes settled fails S4.
- **Neither side wins by construction.** Examples 3, 7, and 8 must end with the text's own discipline
  vindicated — Aquinas more careful than the reader expected. Examples 4, 6, and 9 must end with less
  established than is commonly claimed. A reviewer checks the balance across the nine outcomes.

### 13.3 How the examples relate to the lessons

§12 fixes the nine lessons; this section fixes the nine examples and their order. Each lesson must anchor at
least one, and no example may appear before the frame question that does its work has been introduced. Where
the two disagree about placement, §12 governs; about what an example must expose, this section governs.

### 13.4 Example 1 — a valid pair and an invalid pair

- **Exposes.** That an argument can run from true premises to a false conclusion with no metaphysical error
  in it at all.
- **Material.** A reconstruction, labelled as such, in the first figure of *Post. An.* I.14, 79a17–23:
  everything that changes has an unrealized capacity, this changes, so it has one; then the same first
  premise with "this has one", concluding "this changes".
- **Frame.** Consequence. Claim and Meaning stay routine, so the defect is visibly formal.
- **Notation.** Yes — a formally invalid inference: `all C are U; a is C; so a is U` against `all C are U; a
  is U; so a is C`, with one homely counterexample to the second.
- **Outcome.** The second fails whatever act and potency turn out to be. The example settles no metaphysical
  question, and says so.

### 13.5 Example 2 — a sentence whose truth is mostly definitional

- **Exposes.** That a weighty-sounding sentence can be true, useful, and empty of information about the
  world, and that saying so is not an objection to it.
- **Material.** Aristotle, *Post. An.* I.2, 71b17–25: demonstration is a syllogism productive of scientific
  knowledge. Sentence analysed: a valid syllogism from true premises may still fail to be a demonstration.
- **Frame.** Meaning and Warrant. Burden is the instructive blank: nothing substantive is asserted.
- **Notation.** None. No scope, inference, or identity is at issue; symbols would restate the definition
  rather than test it.
- **Outcome.** A standard, not a discovery (S2). Recognizing a well-made definition is not belittling it.

### 13.6 Example 3 — definitional in appearance, ontological in fact

- **Exposes.** That the sentence carrying the heaviest commitment can look like a gloss on a name.
- **Material.** Aquinas, ST I q.2 a.1 corp.: "God exists" is self-evident in itself, for God is his own
  existence; with ad 2, which refuses the step from what the name signifies to what is in *rerum natura*.
- **Frame.** Claim and Burden. Denial is routine — a rival framework, not a contradiction.
- **Notation.** Yes, on identity: what the name *God* signifies is not thereby something there is. The
  sentence reads as a gloss and is used as an existential claim.
- **Outcome.** The commitment is real and undischarged here — and Aquinas blocks the hurried inference
  himself in ad 2. The article is not Anselm's argument and must not be read as one.

### 13.7 Example 4 — "whatever is moved is moved by another"

- **Exposes.** Two readings of act and potency that share every word, and the price of each. Definitional:
  *moved* means passing from potency to act with respect to a form, *potency* means lacking that form while
  able to have it, *by another* means by something already in act with respect to it — so the premise says
  only that what comes to have a form lacked it, and that nothing gives what it has not got. Substantive:
  the potency invoked by change is a real principle in the changing thing, not a description of possible
  future states.
- **Material.** Aquinas, ST I q.2 a.3 corp. (the first way), including "to move is nothing other than to
  bring something from potency into act" and "nothing can be brought from potency to act except by some
  being in act"; with the parallel at SCG I c.13, ordered movers at n. 14.
- **Frame.** Meaning, Warrant, and Denial, all at full stretch. Claim is routine.
- **Notation.** Yes, for two features only. Quantifier order: `every M has some mover other than itself`
  against `some one thing moves every M` — the conclusion needs the second, the premise gives the first.
  Modal scope: the impossibility asserted is being in act and in potency in the same respect at once, not
  that a changing thing could not have been otherwise. Nothing else is symbolized: `all x (Change(x) ->
  Potency(x))` hides every disputed word inside itself.
- **The open question.** Whether potency is a real principle in the changing thing or a way of describing
  what the thing can become. The example may not settle this, and must say what each answer costs. As a way
  of describing possible states, the premise survives as a truth about coming-to-have but names no real
  feature demanding a real cause, and what the tradition draws from it — a real composition in every
  changing thing, an unmoved mover whose immobility is a perfection — goes unsupported here. As a real
  principle, the premise is substantive and owes its own warrant: our experience of change, plus the claim
  that bare possibility cannot account for what this thing determinately can become. The reader then owes an
  answer, at its strongest (S8), to the modern account of dispositions as modal truths or as grounded in
  microstructure.
- **Outcome.** Granted, the argument reaches something not moved in the respect at issue at the head of an
  essentially ordered series — not one such thing, not an immaterial one, not God. The identification rests
  on the closing words "and this all understand to be God", a naming; the attributes are argued separately
  at ST I qq.3–11 and SCG I cc.14–28, and **Not yet established** says so.

### 13.8 Example 5 — a dependence claim

- **Exposes.** Where an argument stops describing a distinction and starts asserting a cause.
- **Material.** Aquinas, *De ente et essentia* c. 4 (Baur ed.): in anything other than the first cause,
  essence and existence are not the same, and what does not have existence of itself has it from another.
- **Frame.** Meaning and Burden. Denial is substantive too: rejecting the real distinction is a developed
  rival framework, to be stated at strength (S8).
- **Notation.** None, and this is the book's clearest case of notation refused for a reason: rendering
  existence as a predicate letter hides the question, which is whether existence is the kind of thing a
  predicate letter can stand for.
- **Outcome.** Grant the real distinction and the dependence claim follows quickly. The distinction is the
  burden, and this passage assumes rather than argues it. **Not yet established**: that what answers to the
  first cause is one, simple, or intelligent.

### 13.9 Example 6 — an illegitimate move from member to whole

- **Exposes.** That a defence of an argument can be worse than the argument, and that a defect is charged to
  whoever committed it.
- **Material.** A reconstruction, stated as such: every member of the series of moved movers is moved by
  another, therefore the series as a whole is. Read against ST I q.46 a.2 ad 7, which distinguishes series
  ordered *per se* from *per accidens* and holds an infinite regress of the second kind not impossible.
- **Frame.** Consequence. Warrant is routine.
- **Notation.** Yes — the invalid step from `every member of S is F` to `S is F`, with a counterexample that
  settles it (each of three things is fewer than four; the three are not).
- **Outcome.** The reconstruction fails, and the failure is the reconstructor's: Aquinas's text has a
  resource the crude argument never uses. But that distinction now carries the whole weight, so the
  difficulty is relocated, not removed.

### 13.10 Example 7 — a proposition whose warrant is revelation

- **Exposes.** That "Aquinas holds P" and "Aquinas claims to demonstrate P" are different sentences, and
  that the tradition sometimes insists on the difference more strictly than its admirers do.
- **Material.** Aquinas, ST I q.46 a.2: that the world began to be is held by faith and cannot be
  demonstrated. Read with SCG I c.3 and with ST I q.2 a.2 ad 1 on the *praeambula fidei*.
- **Frame.** Warrant, and nothing else at full stretch. Denial needs care: denying a revealed premise is
  neither contradiction nor explanatory cost in the senses of §8.
- **Notation.** None. What is at issue is the standing of a proposition; no scope, identity, or inference is
  unclear.
- **Outcome.** The revealed premise stays labelled and is not made to carry a proof it never claimed (S7).
  The example may not conclude that the proposition is therefore worthless, nor adjudicate the warrant of
  revelation; it must say that this book does not.

### 13.11 Example 8 — provenance mistaken for warrant

- **Exposes.** That in a *disputatio* the quoted authority is often attached to the position the author is
  about to reject, so a reader who takes citation for warrant gets the article backwards.
- **Material.** Aquinas, ST I q.2 a.1: the *sed contra* cites John Damascene for the claim that God's
  existence is self-evident, and the *corpus* then denies that it is self-evident to us. Read with ST I q.1
  a.8 ad 2, where sacred doctrine uses philosophers as extraneous and probable arguments and Scripture as
  necessary.
- **Frame.** Warrant and Claim. Burden and Consequence are routine.
- **Notation.** None. Nothing inferential is obscure; what is obscure is what a sentence is doing in the
  form it appears in.
- **Outcome.** The citation establishes that Damascene held it, and nothing further (S1). The example must
  not suggest that Aquinas argues from authority here: he is the one distinguishing the uses of authority,
  and the confusion belongs to a reader who does not know the form.

### 13.12 Example 9 — a fuller demonstration, worked through

- **Exposes.** What it takes for an argument to be a demonstration rather than merely a valid argument, and
  how much of that a real metaphysical argument supplies.
- **Material.** Aquinas, ST I q.2 a.2 corp. and ad 2 — demonstration *quia* from effects, with what the name
  signifies serving as middle where the essence is unavailable — applied to ST I q.2 a.3 corp. and SCG I
  c.13, and tested against the six conditions on demonstrative premises (*Post. An.* I.2, 71b17–72a8) and
  the *quia* / *propter quid* distinction (*Post. An.* I.13, 78a22ff).
- **Frame.** All six. Consequence and Denial are hardest and take the most space.
- **Notation.** Yes, for one purpose: a comparison of two genuinely different formal readings of the series
  — dependence of each member on a present cause against succession of members in time.
- **Outcome.** Conditional and open, and written that way. At best this is a *demonstratio quia*: its middle
  is what the name signifies rather than the *quod quid est*, on Aquinas's own account, and whether such a
  middle yields *scire* in Aristotle's sense is genuinely disputed. The example must set out the dispute
  with named positions on both sides rather than declare a winner, and must end by stating what a reader who
  grants every premise has and has not got.
## 14. Exercises and solutions

### 14.1 Purpose

Exercises train transfer to unmarked prose. A reader who can only fill in a form the book has already
half-filled has learned nothing portable (acceptance test J). Every exercise type below must be assignable
on a passage the reader has not seen the book mark up, and the last exercise of the book must be unannotated
real prose with no scaffolding.

### 14.2 Exercise types

Sixteen named types. Each has a short name and one line stating what capability it tests. These are types
in the specification, not labels printed beside every exercise in the book. An exercise in the book need
not declare its type, and a single exercise may exercise more than one.

1. **Plain restatement** — restate a technical proposition in plain language without changing its claim.
2. **Technical word** — identify which words in a passage carry technical senses and what each means here.
3. **Warrant label** — assign each sentence one of the eight kinds of warrant of §4.
4. **First commitment** — find the first sentence that makes a substantive ontological commitment, not a
   definitional unpacking.
5. **Definition or premise** — say, for a given sentence, whether it is a definition or a metaphysical
   premise, and what would change if it were the other.
6. **Burden finder** — find the burden-bearing premise: the first proposition whose truth is not supplied
   merely by vocabulary or by a previous citation.
7. **Smallest denial** — identify the smallest denial that blocks the argument, the one that removes the
   least and suffices.
8. **Denial kind** — say which of the five kinds of denial of §8 that denial falls under, and why.
9. **Weaken** — weaken the conclusion to what actually follows from the premises granted.
10. **Not yet** — state what has not yet been established, including what the surrounding tradition
    commonly claims at this point.
11. **Quia or propter quid** — say whether the argument is a *demonstratio quia* or a *demonstratio
    propter quid*, and what would turn one into the other.
12. **Scope shift** — locate a hidden modal or quantifier shift, and say what it conceals.
13. **Reconstruct** — reconstruct a compressed passage of Aquinas into explicit argumentative prose,
    supplying the missing steps without importing conclusions.
14. **Name removal** — remove the author's name and ask whether the argument still has force; if it does
    not, say what the name was supplying (S1, acceptance test C).
15. **Rival compare** — compare an apparently Thomistic explanation with a rival account, each stated at
    its strongest (S8).
16. **Repair** — repair an argument without smuggling the conclusion into a definition (S2). The solution
    must show that the repaired premise is substantive, not a restatement of the conclusion in defined
    terms.

### 14.3 The recurring "Simon says" exercise

The recurring question of §8 — what is the first proposition whose truth is not supplied merely by
vocabulary or by a previous citation — is a standing exercise form, not a type in the list above. It must
appear in most lessons. At least one instance must use a passage where the honest answer is that there is
no such proposition: the argument is vocabulary all the way down, and the reader must say so rather than
manufacture a burden-bearing premise that is not there. A solution that invents a substantive premise
where the text offers only definitional unpacking fails S2.

### 14.4 The transfer ladder

Three levels of annotation, in ascending difficulty:

- **Annotated.** The book has already marked the structure: premises, conclusions, warrant kinds, or the
  burden-bearing premise is identified. The reader fills in what is missing or answers a question about
  what is marked.
- **Lightly annotated.** The book supplies only the passage and a question. No structure is marked.
- **Unannotated.** Real prose, no scaffolding. The reader performs the full six-question analysis
  unaided.

Per lesson, at least one exercise must be lightly annotated from Lesson 2 onward, and at least one must be
unannotated from Lesson 4 onward. The last exercise of the book is unannotated real prose with no
scaffolding. Annotated exercises may not exceed half the count in any lesson after Lesson 1.

### 14.5 Solution policy

A solution must contain three things: the answer, the reasoning that reaches it, and, where relevant, what
a competent reader might answer instead and why that answer is worse or is also defensible. A solution may
conclude that the passage is genuinely ambiguous, and when it does, it must say what the readings are and
what turns on choosing among them. A solution may not pretend to a determinacy the text does not have. A
solution that supplies a label without reasoning fails the policy, whether or not the label is correct.

For repair exercises specifically, the solution must demonstrate that the repair did not smuggle the
conclusion into a definition. It does this by showing that an opponent who accepts the repaired premise's
definition can still deny the conclusion — that is, by exhibiting the substantive gap the repair leaves
open. A repair that closes every gap by definition has rebuilt the tautology, not the argument (S2).

### 14.6 Adversarial and repair exercises

From Lesson 3 onward, each lesson must include at least one defective near-neighbour: an argument that looks
like the good one but fails. The reader is asked to say where it fails and why. The defect must be
philosophical, not a typo: a hidden scope shift, an illicit member-to-whole move, a definitional smuggling
of the conclusion, or a warrant that reduces to provenance only.

From Lesson 5 onward, each lesson must also include at least one repair exercise. The reader repairs a
defective argument. The repair must not smuggle the conclusion into a definition, and §14.5 specifies how a
solution proves it did not.

Neither the adversarial nor the repair exercises may be built so that the tradition always loses. An
adversarial exercise where the defective argument is a crude reconstruction of Aquinas must be balanced, in
the same lesson or an adjacent one, by one where the defective argument is a crude reconstruction of a
modern critic who misreads Aquinas. The book must not become a debunking manual, nor an apologetic one.

### 14.7 Counts and budget

Each lesson carries four to seven exercises, with solutions. Lesson 0 may carry fewer. The total across
nine lessons is roughly forty to fifty exercises. Exercises and solutions together consume roughly twelve
to eighteen rendered pages — no more than a quarter of the book. If the count grows beyond that, cut
annotated exercises first; the transfer ladder's upper levels are the last to go.
## 15. The vertical slice

The vertical slice proves the book works: eight to twelve rendered pages in which
one short passage of real metaphysics is read all the way through, in the
finished voice and typography of the book. It demonstrates the reading experience
and nothing else. A slice that demonstrates bookkeeping instead of an act of
reading is rejected even if every requirement below is met.

### 15.1 Standing, and relation to the curriculum

The slice is a standalone demonstration, not an excerpt from a lesson. It
exercises all six questions of the frame (§2) at once, and so draws on
competences the lessons of §12 install separately — warrant, burden, bounding,
denial — but it must be legible cold: a reader who opens the book here, having
read none of §12, must be able to follow every page. In the progression of §13 it
occupies the composition-and-dependence position, where the temptation is to move
from a claim about each member of a series to a claim about the series. It
neither replaces that item nor restates the progression; where the two disagree,
§13 governs the progression and the slice the finished presentation.

### 15.2 The passage

The slice works on Aquinas's distinction between causal series ordered *per se*
and ordered *per accidens*: ST I q.46 a.2 ad 7, the reply containing the stone
moved by the stick and the stick by the hand, the artisan with many hammers, and
the endless succession of men begetting men.

Four reasons. It is one paragraph, so all of it fits on the page and the reader
can see nothing was withheld. It is the hinge on which every regress argument in
the tradition turns, so a reader who cannot handle it cannot honestly read the
First or Second Way. Its central assertion — that an endless *per se* series is
impossible — is asserted here and argued elsewhere, so the burden-bearing premise
must be found rather than pointed at. And it sits inside an article about what is
held by faith rather than demonstrated, so questions of warrant are live.

The slice quotes; it does not reconstruct. The Latin is short and verified
verbatim in Appendix A at ST I q.46 a.2 ad 7. The author may not extend the quotation
beyond the text recorded there without verifying the extension, and may not cite
In Phys. VIII or SCG II c.38 for the ordered-series claim, which Appendix A records as
unchecked. For the place where that claim is argued rather than asserted, the
slice cites SCG I c.13 nn. 14 and 33, which Appendix A verifies.

### 15.3 Notation

The slice carries notation exactly once: two displayed lines in element 8, and
nowhere else (S3). This is not a hedge. The passage contains a genuine ambiguity of
dependency joined to a genuine question of quantifier order, and two lines expose
in a glance what a page of prose labours over. The display is preceded by a full
English gloss of its one relation symbol: `Dep(x, y)` for *the causing done by x
is derived from the causing done by y, so that x causes only because y causes*.
The quantifiers range over members of one causal series.

```text
(1)  ∀x ∃y Dep(x, y)
(2)  ∃y ∀x Dep(x, y)
```

The slice must say what both lines expose. An ambiguity: read `Dep` as bare
succession — *x was caused by y* — and (1) is what the *per accidens* concession
allows to run on forever; read it as derived causing, and (1) is what the *per se*
case is supposed to forbid. The same English words carry both readings. An order:
(1) and (2) are different propositions, the conclusion wanted here is (2), and the
passage asserts only that (1) under the second reading is impossible — without
showing that any real series of dependence satisfies (1) under that reading. That
gap is where the weight sits. Nothing else is symbolized: not cause, order, *per
se*, *per accidens*, act, potency, or existence. Numbered premises in ordinary
English are not notation.

### 15.4 The required sequence

The fifteen elements appear in this order, with the page allowance given. Each
carries a check a reviewer can perform holding only the slice.

**1. The passage in its setting (0.25 pp.).** The article's question in the exact
words of the verified text, the objection answered, and one sentence placing it in
the *Summa*. Check: the reviewer can say what Aquinas was arguing about.

**2. The wording as written (0.5 pp.).** The Latin of the reply, unmarked, with a
close English rendering beneath it; no emphasis, brackets, or numbering inside the
quotation. Check: the quotation carries none of the book's own marks.

**3. Plain-language reading (0.5 pp.).** A restatement dropping school vocabulary
the argument does not need and keeping every distinction it does, naming one term
it deliberately did not translate away and why flattening it would change the
claim. Check: restatement and Latin compare clause by clause, nothing missing.

**4. Meaning (1.0 p.).** Four things to fix first: *per se* and *per accidens* of
causes; what it is for causes to hold *the order of one cause*; *grade* in a series
of efficient causes; and the force of *inquantum* — a man begets insofar as he is a
man, not insofar as he is another man's son. Check: for each, the slice says what
would change in the argument if the term were taken otherwise.

**5. Source and provenance, kept apart from warrant (0.75 pp.).** Who is speaking,
where, and against whom — then, separately headed, that none of this is a reason to
believe anything (S1). It keeps labelled, and out of the argument in both
directions, the surrounding article's premise that the world's beginning is held
on revealed teaching (S7). Check: one sentence says the citation establishes only
that Aquinas held this, and no later element uses his name as a reason.

**6. The burden-bearing premise (1.0 p.).** Two or more candidates, decided by
argument, with the test shown on the page: could an intelligent opponent grant
everything else and still deny this? The weaker is the bare impossibility of an
endless *per se* series; the stronger, which the slice should reach, is that some
real series of dependence is *per se* ordered — that the derived causing of hand,
stick and stone holds beyond simultaneous instruments. Check: the rejected
candidate is on the page with the reason it lost; one candidate alone fails.

**7. Why the author thinks it is true (0.75 pp.).** Prose, no table, classifying the
warrant among the eight kinds and separating three things the passage does: it
illustrates by the stick and stone (experience); it relies on a prior result argued
elsewhere (SCG I c.13 nn. 14, 33); and until a reader goes there, the impossibility
is carried by provenance only — a diagnosis, not a warrant. Check: all three named.

**8. What follows if it is granted (1.0 p.).** The consequence at its exact strength,
carrying the two lines of §15.3 and the sentences saying what they expose. Check:
the reviewer can state in one sentence how the lines differ and which one the
passage supplies.

**9. Not yet established (0.5 pp.).** Conspicuous, under its own heading. It names at
least two propositions the tradition commonly reaches here and says why this
passage reaches neither: that there is a first cause of the being of things, and
that any chain we actually encounter is of the *per se* kind. Check: each is a
specific proposition a reader would otherwise have assumed the passage gave (S4).

**10. Denial, classified (0.75 pp.).** Which of the five kinds denial of the
burden-bearing premise would be. It must reach *rival framework* — the denier holds a
developed account on which every chain of dependence is like generation, each
member's causal power its own — and say why the denial is not *contradiction*: nothing
self-refuting follows from holding that no real series is *per se* ordered; merely
declining the vocabulary is *non-assent* (S5). Check: one of the five is rejected,
with reasons.

**11. The objection (0.75 pp.).** One objection against the burden-bearing premise,
not a detail, worded so its ablest defender would accept it (S8). Preferred form, a
dilemma: either *per se* ordering is narrow enough that only simultaneous instrument
chains satisfy it, and the argument reaches nothing about the existence of things,
or broad enough to cover dependence in being, and the impossibility of an endless
such series is built into the description rather than shown. A named critic is cited;
a constructed objection says so. Check: read alone, the objection reads as an argument
someone would publish, and it contradicts the burden-bearing premise.

**12. Reply, or concession (0.75 pp.).** Whichever is honest; here partly a
concession, that the passage shows what would follow if a series were *per se*
ordered in the required sense and does not show that any is. That conditional
result is the real yield and is not repaired by redefinition. Check: the reply
defeats the objection or names what it gives up; restating the claim fails.

**13. The defective near-neighbour (0.75 pp.).** A short argument in the register of a
competent expositor, differing by one locatable step: it goes from line (1) to line
(2) directly, taking "each is caused by another" to yield "there is a first,"
without the derived-causing premise that licenses it. It appears first without comment;
then the defect is located and named, and must be one that occurs in real expositions
and is reachable by inattention. Check: the two arguments lie side by side with the
differing step identifiable, and a careful author could have written it.

**14. Exercises (0.5 pp.).** Two to four; at least two on prose the slice has not
analysed. The last works on an unannotated passage, the second way at ST I q.2 a.3
corp., verified in Appendix A: *where does the ordered-series claim enter, and does the passage
tell you the series is per se ordered?* One may ask for a repair of element 13 that
does not smuggle the conclusion into a definition (S2). None may be answerable by
naming a category. Check: no exercise supplies the structure it asks for.

**15. Solutions (0.75 pp.).** Each explains why, in prose, showing the steps by which
the answer was reached, and at least one records an honest indeterminacy: two
defensible answers, the reasons for each, and what would settle it. Check: strike
the answers and the reasoning still teaches something; a solution that is a label
fails.

The allowances sum to 10.5 pages. Any redistribution must keep the total inside
the 8–12 band and may not take an element below half its allowance.

### 15.5 What the slice must not contain

- No reader-facing code, label-number, or identifier scheme, and no reference to
  one; no grid, matrix, or scoring table applied to the passage, and no ratings or
  verdict counts.
- No dependence on earlier lessons: the slice may cite §12 and §13 for context, and
  may not require that they have been read.
- No apparatus the reader must learn before reading the passage. Whatever the six
  questions need is said in the sentence that uses them.
- No notation beyond the two lines of §15.3.
- No suggestion that Aquinas used these six questions or anything resembling them
  (S6); where the slice's vocabulary is modern, it says so.
- No use of the author's name as a reason (S1), including in the solutions.

### 15.6 The acceptance gate

The slice is accepted only if the answer to this question is yes:

> Would this make an intelligent reader substantially better at interrogating an
> unannotated page of metaphysics?

Visual polish is not evidence. Typography, layout and the elegance of the Latin
setting count for nothing here. A slice that is beautifully produced and answers
no is rejected, and it is rewritten on a different passage rather than patched.

The gate is decided by transfer. A reviewer who has not read the document is given
the slice and, separately, one unmarked page of metaphysical prose it never mentions.
If that reviewer cannot produce a reading of the unmarked page identifying its claim,
its burden-bearing premise, and what it has not yet established, the answer is no.

Five findings make the answer no. Any one of them is sufficient.

1. **The structure was pre-marked.** The analysis works only because the parts were
   already italicized, numbered or labelled. Test: each added mark is argued for.
2. **The burden was assigned by authority.** The premise is announced, not found. Test:
   element 6 shows a rejected candidate and why it lost.
3. **Not yet established is decorative.** It names caution instead of propositions,
   or propositions no reader would have assumed. Test: each item is a sentence
   someone could have believed the passage proved.
4. **The objection is a straw man.** It attacks a detail, a paraphrase, or a position
   no defender holds; or the reply answers it at no cost. Test: it contradicts the
   burden-bearing premise as stated, and the reply defeats it or concedes.
5. **The near-neighbour is not near.** Its defect is one no competent author would
   commit, or it differs by more than one step. Test: one step, a plausible author.

### 15.7 If the slice runs over twelve pages

Cut in this order: the Latin quotation down to the clauses the analysis uses; the
third of the four terms in element 4; the exercises from four to two; element 5's
provenance discussion down to the source, the opponent and the rule. Overflow is never
cured by moving material into an appendix or a note read away from the point of use.

Six elements may never be cut, and never shortened below half their allowance: the
Plain-language reading; the burden-bearing premise with its rejected candidate;
Not yet established; the classified denial; the objection at full strength; and
the solutions that explain why. Length is never recovered by weakening the
objection, by trimming what has not been established, or by replacing a solution
with an answer.
## 16. Author-side conventions

This section governs the people writing the book. It exists to keep several
authoring lanes consistent, and nothing in it is a subject the reader studies.

### 16.1 The invisibility rule

Every convention in this section must be invisible to the reader. If a
convention shows up on a printed page, it is a defect and the page is
rewritten.

The test: a reviewer reads a finished spread with the specification closed.
If the reviewer can tell that a house convention was applied — because a
sentence names a rule of ours, prints an abbreviation such as `S3`, or refers
the reader to a numbering scheme — the spread fails. Worked passage titles,
exercise numbers, and ordinary citations are not conventions in this sense;
they are furniture every book has.

`S1`–`S8` may be cited in this specification and in the checklist of §16.3.
They may never appear in the book's own text, its exercises, its solutions,
or its appendices, and the reader is never asked to learn them.

### 16.2 Numbering that survives

Three numbering conventions, and no others.

- **Worked passages** are numbered sequentially within their lesson, from one.
  In prose a passage is named "the third worked passage of Lesson 4"; in
  cross-reference within the book, "Lesson 4, worked passage 3".
- **Exercises** are numbered lesson-and-item: exercise 4.2 is the second
  exercise of Lesson 4.
- **Solutions** carry the number of the exercise they answer and no number of
  their own.

Nothing else is numbered. There are no reserved number ranges, no numbering
that runs across lessons, no numbers assigned to propositions, premises,
arguments, definitions, objections, or replies, and no rules for allocating
numbers in advance of drafting. A lane that needs to refer to a premise
quotes it or describes it in words.

### 16.3 The author's checklist for a worked passage

This is the only apparatus the project keeps. It is a checklist the writer
works through before delivering a worked passage — not a form the reader
fills in, and not a template printed on the page.

1. **Claim.** Is the assertion stated as the author actually makes it, with
   its own qualifications intact? Is there a plain-language reading that
   drops school vocabulary without flattening a real distinction? Is our
   frame kept out of the author's mouth (`S6`)?
2. **Meaning.** Are the terms the argument turns on fixed before they are
   used? Have I said which senses are the author's and which are mine?
3. **Warrant.** Does every important premise have one of the eight kinds of
   warrant named for it in ordinary English? Is a citation ever standing in
   for a reason (`S1`)? Is "provenance only" presented as a diagnosis rather
   than as a warrant? Is a revealed premise labelled and left revealed
   (`S7`)?
4. **Burden.** Is the burden-bearing premise identified in a single sentence
   the reader can underline? Could an intelligent opponent accept every
   definition given and still deny the conclusion? If not, does the passage
   say the argument has unpacked a vocabulary (`S2`)?
5. **Consequence.** Does the passage state what has been established, and
   conspicuously what is not yet established at this point (`S4`)?
6. **Denial.** Is rejecting the burden classified among the five kinds
   (`S5`)? If the answer is rival framework, is the rival stated in the form
   its ablest defender would accept (`S8`)?

Then once more over the whole passage: does any notation appear, and if so
can I write the sentence saying what it makes easier to see (`S3`)? If I
cannot, the notation goes.

### 16.4 Quotation and citation discipline

A passage is identified by author, work, and the work's own internal
division — book and chapter, or part, question, and article — and by the
edition or translation quoted. The historical detail, including which
editions and translations are usable, lives in `§11` and `Appendix A`; lanes
follow those and do not restate them.

A translation is marked at first use with the translator's name, or, where a
lane has rendered the Latin itself, with a plain statement that the
translation is the book's own. Latin is printed only where a distinction
turns on it, and then with the English beside it.

A paraphrase is never presented as a quotation. Quoted words are inside
quotation marks or set as a block quotation; anything else is the book's
restatement and is introduced as one ("Aquinas's point, restated…"). A
reconstruction that compresses or reorders an author's argument says so
before it begins.

### 16.5 How prose and notation are set

Prose is the canonical medium (`S3`). A worked passage is continuous prose
under the six frame words as ordinary headings, with room for a heading to
carry two paragraphs where a question deserves them.

Notation is displayed on its own line only where `§9` licenses it, and the
licensing sentence stands in the prose beside it. Notation is never set in a
column beside the prose it comments on, and a lesson never opens or closes
on a formula.

No layout may make an analysis look like a form. No boxed fields, no ruled
grids, no label-and-blank pairs, no repeated marginal tags, no icons. The one
exception is `Appendix B`, which is deliberately a sheet the reader may copy;
its layout is fixed there and is not imitated inside a lesson.

### 16.6 What an authoring lane may not do

A lane may not:

- introduce an abbreviation, label, code, or coined term of its own, or
  rename any of the six frame words, the eight kinds of warrant, or the five
  kinds of denial;
- add, split, or renumber a lesson; the count is nine, numbered 0–8;
- exceed its page budget, or the book's, without a written amendment from
  the lead recorded in this specification;
- symbolize an inference that `§9` does not license, or symbolize a
  metaphysical relation to make a page look rigorous;
- reintroduce version 1's machinery under a new name — records of proofs,
  scored review dimensions, memorized condition lists, reader-facing token
  systems, or machine-readable structures — in any form, however renamed;
- require the reader to consult a glossary of our terms in order to finish an
  exercise.

A lane that believes one of these prohibitions blocks necessary work reports
the conflict to the lead and stops. It does not decide the question itself.
## 17. Acceptance tests and review

Every lesson is reviewed as it is drafted, and the finished book as a whole,
against the ten tests of `§17.2`. A lesson is accepted only when each test has
been run and its result recorded. No lane reviews its own lesson.

### 17.1 The pencil test

This is the master test, and it outranks every other judgement in this
section.

Hand the reader an ordinary page of Aquinas the book has never discussed, and
a pencil. If the reader cannot carry out the six-question analysis without
consulting a glossary of our terms, the architecture has failed.

How it is run. The lead selects the page by opening a volume the book does
not quote — an article of the *Summa*, a chapter of a commentary — and taking
the passage found there rather than one chosen for convenience. The lead
gives the reader the passage, a pencil, and blank paper: no specification, no
lesson text, no analysis sheet. The reader writes short answers under the six
headings and marks the sentence carrying the burden.

Who runs it, and when. The lead runs it, with a reader who has read the
drafted lessons and written none of them; where no such reader is available
the lead may read for a lesson the lead did not draft, and must say so when
recording the result. It is run at least twice — when the vertical slice is
complete, and when the last lesson is drafted — and may be run between.

What counts as failure. Any of: the reader asks what one of our words means;
the reader reaches for the specification, the slice, or `Appendix B`; the
reader names no burden-bearing premise; the answers show a heading was
misunderstood. A reader who finds the passage hard, argues with it, or answers
in a way the lead disagrees with has not failed — the test is whether the
method can be carried out unaided, not whether the reader is right.

Failure is a failure of the architecture, not of the lesson under review. The
lead reports it and amends the frame or the lessons that teach it.

### 17.2 The ten tests

**A. Personal usefulness.** *Can the method be applied with a pencil to an
ordinary page of Aquinas, without a glossary of ours?* Procedure: run the
pencil test of `§17.1`. Per lesson, additionally: the reviewer lists every
instruction the lesson gives the reader and strikes any that cannot be
carried out with the passage and a pencil alone. A lesson that asks the
reader to recall a name which is not one of the six frame words, the eight
kinds of warrant, or the five kinds of denial fails.

**B. Burden visibility.** *Can the reader see where definitional unpacking
ends and ontological commitment begins?* Procedure: in each worked passage
the reviewer underlines the one sentence the draft names as burden-bearing,
then takes each premise before it and asks whether its truth is supplied by
the meanings fixed under Meaning. Failure: no sentence is named; the named
sentence's truth does follow from the stated definitions alone, so the burden
lies later; several sentences are named without saying how the work divides
among them.

**C. Authority discipline.** *Does removing the author's name remove any
warrant?* Procedure: the reviewer strikes every proper name and citation from
the Warrant, Burden, and Consequence text of a worked passage and rereads it.
Failure: a premise is now left with no reason offered for it — unless the
draft has already labelled that premise "provenance only", which is the
diagnosis this test is meant to produce, or "revelation", which stands
labelled under `S7`.

**D. Formalism discipline.** *Does the document state what each piece of
notation makes easier to see?* Procedure: for each displayed formula in the
lesson, the reviewer locates the sentence in the surrounding prose that names
what the formula makes easier to see. Failure: no such sentence; a sentence
that names only rigour, precision, or clarity in general; a sentence naming a
feature that `§9` does not license. The remedy is deletion of the formula,
not addition of a sentence about it.

**E. Tautology discipline.** *Does a definition anywhere masquerade as a
discovery?* Procedure: run the hostile-reader check of `§17.3`, on every
worked passage and on every exercise solution that reaches a conclusion.

**F. Bounded conclusions.** *Does each worked argument say what it has not
reached?* Procedure: the reviewer finds, under Consequence, the statement of
what is not yet established, and checks that it names at least one
proposition the surrounding tradition commonly claims at that point. Failure:
the statement is missing; it is contentless ("further argument is needed");
it names something no one in the tradition claims there, which shows the
passage has not been read against its context.

**G. Honest disagreement.** *Is denial classified accurately among the five
kinds?* Procedure: the reviewer reads the Denial section, notes which kind is
asserted, and then tries to build the opposing position. If the draft says
contradiction and the reviewer can hold a consistent position that denies the
burden, the test fails. If the draft says conflict with experience and the
reviewer can deny the burden while granting everything we plainly encounter,
it fails. If the draft says rival framework, the rival must be stated as its
ablest defender would state it (`S8`); a rival described only by what it
lacks fails. Non-assent presented as contradiction is a failure in either
direction.

**H. Historical fidelity.** *Is any modern device projected backward?*
Procedure: the reviewer lists every sentence that attributes a method,
distinction, or intention to Aristotle, Aquinas, or a commentator, and checks
each against `§11` and `Appendix A`. Failure: an attribution those sections
do not support; a citation not verifiable there; any of our six headings,
eight kinds of warrant, or five kinds of denial presented as something the
author himself used or would recognize (`S6`).

**I. Scale.** *Is the book plausibly 50–80 pages?* Procedure: apply `§17.5` at
each delivery. Failure: the projection exceeds eighty pages and nothing is cut.

**J. Transfer.** *Do exercises end on real prose rather than on our
headings?* Procedure: the reviewer classifies every exercise in the lesson as
(a) set on a passage the book has already analysed, (b) set on new prose with
our headings or partial analysis supplied, or (c) set on new prose with
nothing supplied. Failure: the lesson has no exercise of kind (c); the
lesson's final exercise is of kind (a); across the book, fewer than half the
exercises are of kind (c). `§14` fixes the exercise mix; this test checks it
was kept.

### 17.3 The two pseudo-formalism checks

**Symbols that hide the question.** For each displayed formula, the reviewer
lists the questions the surrounding prose says are still open — what a term
means, whether a feature is conceptual or real, why one claim licenses
another. The reviewer then looks for those questions inside the formula. A
question that has become a predicate letter or a relation symbol has been
hidden, and the formula fails, unless the prose says plainly that the
notation sets that question aside in order to show something else, and names
what. Failure is cured by deleting the formula and arguing in prose.

**Tautology dressed as discovery.** The reviewer copies out, in a list, every
definition the passage supplies, then attempts to hold all of them at once
while denying the passage's substantive conclusion. The question in the
reader's own voice: *could an intelligent opponent accept all these
definitions and still deny the substantive conclusion?* If the opponent can,
the argument has substantive content and the check is passed. If the opponent
cannot, the passage must say so — it must state that what has been done is an
unpacking of a vocabulary, not a finding about reality. The failure is not
that an argument turned out definitional; the failure is presenting a
definitional result as a discovery.

### 17.4 Rejection protocol

1. The reviewer records, per test, one of three results: pass, defect, or
   hard fail.
2. The lead decides the outcome. A lane may not accept its own lesson, and a
   reviewer may not accept a lesson over a recorded hard fail.
3. A defect returns the lesson with the failing test named and the offending
   sentences quoted. The lane revises those sentences and resubmits.
4. A failure of test A, D, E, or H is a hard rejection, not a revision
   request. The lesson is withdrawn. Before drafting again the lane submits a
   plan — which passages, which burden-bearing premise in each, which
   notation if any — and gets the lead's approval.
5. A resubmitted lesson is reviewed against all ten tests, not only the one
   it failed.
6. Two hard rejections of the same lesson end the drafting attempt: the lead
   narrows the lesson's scope, merges it with a neighbour, or reassigns it.

### 17.5 Scale enforcement

Each lane reports the rendered page count of its lesson at delivery. The lead
keeps a running total and a projection: pages delivered, plus the budgeted
pages of lessons not yet delivered. The ceiling is eighty rendered pages for
the whole book and eight to twelve for the vertical slice.

When the projection exceeds eighty pages, the lead cuts content before
accepting another lesson, in this order:

1. worked passages beyond the minimum the required progression demands;
2. historical background in `§11` that no worked passage uses;
3. exercises above each lesson's minimum — never the final unannotated one;
4. two adjacent lessons merged into one;
5. a lesson dropped, and only by written amendment.

The remedy is always cutting content. Reducing type size, narrowing margins,
tightening leading, condensing tables, moving prose into an appendix that
still prints, or shrinking the slice below eight pages are all forbidden, and
a draft that uses one of them is returned.

A projection below fifty pages is also a defect. The remedy is more worked
passages and more exercises on real prose, never more taxonomy.

### 17.6 The reviewer's checklist

Twelve questions, each answered yes or no beside the drafted lesson. Any no
is a finding, and the reviewer names the test it belongs to.

1. Does every worked passage name one burden-bearing sentence?
2. Does every important premise have a kind of warrant named in ordinary
   English?
3. Is every citation doing provenance work only, never warrant work?
4. Does every displayed formula have its licensing sentence beside it?
5. Could an opponent grant all the definitions and still deny each
   conclusion — and if not, does the passage say so?
6. Does every worked passage state what is not yet established?
7. Is each denial classified among the five kinds, with any rival stated at
   its strongest?
8. Is every revealed premise still labelled as revealed?
9. Is every historical attribution supported by `§11` or `Appendix A`?
10. Does the lesson end on an exercise set on prose with nothing supplied?
11. Is the lesson within its page budget?
12. Is the lesson free of our abbreviations, coined labels, and form-like
    layout?
## 18. Questions deliberately deferred

These questions are open. Each is open because the evidence that would settle
it does not exist yet, and each names what would settle it. No lane may close
one of them by its own judgement; a lane that needs an answer asks the lead,
who answers by amendment when the evidence named here arrives.

### 18.1 The open questions

**Is the slice's chosen passage the right entry point?** Open because the
first passage a reader meets decides whether the frame looks usable or
fussy, and no drafted passage has yet been tried on a reader. Decided by the
slice evidence: if a reader who has read only the slice can carry out the
six questions on a fresh passage, the entry point holds; if the slice's
passage needs more historical background than eight to twelve pages can
carry, another passage replaces it.

**Are nine lessons the right count, or should some merge?** Open because the
page cost of a lesson is not known until lessons exist. Decided by the page
budget of `§17.5`: when the projection exceeds eighty pages, adjacent lessons
merge in the order that cut list gives. Nine is the ceiling on the count as
well as the plan; no lesson is added.

**How much symbolic notation does the finished book need?** Open because the
answer depends on which passages are chosen and where their inferences go
wrong. Decided by the worked examples: notation that survives test D stays.
If very few formulas survive across the whole book, `§9` shrinks to a short
warning about notation rather than a treatment of it; if a class of passages
turns out to need scope notation repeatedly, `§9` says so and gives one
model.

**Does the book address contemporary analytic metaphysics at all, or stay
with Aristotle, Aquinas, and their commentators?** Open, and deliberately
so: contemporary treatments of dependence, grounding, and modality could
sharpen a burden or could import a second vocabulary the reader must learn.
Decided by trial on the book's own material: if a contemporary discussion of
one passage already worked makes its burden easier to see without adding
vocabulary the reader must retain, it earns a place; otherwise the book stays
with the tradition and says plainly that it does.

**Does Augustine supply worked passages at all?** Open
because his genre resists the six questions differently from Aquinas's
articles. Decided by attempting one Augustinian passage under the checklist
of `§16.3`: if it yields a burden-bearing premise a reader can underline, it
stays; if the analysis becomes a commentary on rhetoric, it goes.

**Which unsuccessful demonstration is worked to the end?** The book requires
at least one case where the honest result is weaker, conditional, or
negative, but not which. Open because the candidates must be tried before one
is chosen. Decided by drafting: the case chosen is the one whose failure is
instructive about warrant rather than merely about a mistake.

**Are eight kinds of warrant enough?** Open because only real passages can
show a premise that fits none of them. Decided by the worked passages: a
premise that repeatedly resists all eight, across more than one lesson, is
evidence for an amendment to the list — made by the lead, never by a lane
coining a ninth kind in passing.

**What production format does the book take?** Not settled here. A single
printed document, a web edition, or both are all compatible with this
specification. Decided later, by the repository's own conventions for
publications and by the finished text's needs; nothing in this specification
may be shaped around a format assumption.

**Is a second volume or an extension warranted?** Open, and nothing before
completion decides it. Decided by use: after the finished book has been used
on unfamiliar passages over a real stretch of reading, either a gap in the
method shows itself or none does. Until then no lane plans for a sequel, and
no material is retained in this book on the ground that a later volume will
want it.

### 18.2 What version 2 has settled

These are closed. A later agent that wishes to reopen one asks the lead for a
written amendment; it may not decide the question in the course of drafting.

- The six-question frame — Claim, Meaning, Warrant, Burden, Consequence,
  Denial — with those names, in that order, and its two fixed sub-elements.
- Prose as the canonical medium; notation licensed case by case and never by
  default.
- The eight standing rules `S1`–`S8`, and the rule that they stay behind the
  page.
- Nine lessons, numbered 0–8.
- The ceiling of 50–80 rendered pages, and cutting content as the only
  remedy for overrun.
- The deletion of version 1's proof-engineering apparatus, and the
  prohibition on its return under any new name.

The eight kinds of warrant and five kinds of denial are settled as the
working lists; only the evidence named in `§18.1` reopens them.
## Appendix A. Historical sources, verified

### A.1 What this appendix is

This appendix is the author-side reference behind §11. It is not reader-facing pedagogy, and a
chapter may not quote it as though it were prose written for the reader. Its purpose is that a
later chapter can cite a locus without redoing the research.

Every locus below was checked against a primary text or against named secondary scholarship keyed
to that locus. Aristotle was checked in the Oxford translation of G. R. G. Mure (*Posterior
Analytics*), W. D. Ross (*Metaphysics*, *Nicomachean Ethics*), and W. A. Pickard-Cambridge
(*Topics*), consulted with the Greek lemmata and Bekker line numbers embedded in the Aquinas
commentary text at isidore.co. Aquinas was checked against the Latin at corpusthomisticum.org
(Leonine, Rome 1882 for In PA; Leonine, Rome 1888 for ST I; Leonine, Turin 1961 for SCG; Turin
1950 for In Metaph.; Decker, Leiden 1959 for Super Boet. De Trin.). Three things are kept apart
throughout and must stay apart in the book: what a text says, what the tradition took it to say,
and what modern scholarship disputes. Items that could not be verified are marked UNVERIFIED in
§A.6 and must not be silently upgraded.

### A.2 Aristotle: doctrine and locus

| Locus | Doctrine |
|---|---|
| *Post. An.* I.2, 71b8–16; *Nic. Eth.* VI.3, 1139b18–22 | *epistēmē* is knowing the cause on which the fact depends, as cause of that fact and no other, and that the fact cannot be otherwise; its object is necessary |
| *Post. An.* I.2, 71b17–72a8 | *apodeixis* is a syllogism productive of such knowledge; its premises must be true, primary, immediate, better known than the conclusion, prior to it, and causes of it |
| *Post. An.* I.2, 71b29–72a5 | "better known" is distinguished into better known in nature and better known to us; Aristotle means the former |
| *Post. An.* I.2, 72a8–25 | a principle is an immediate proposition with nothing prior; axioms (common), theses, hypotheses (asserting that a subject is), definitions (not so asserting) |
| *Post. An.* I.3, 72b5–73a20 | no circular demonstration, no infinite regress; knowledge of immediate premises is not demonstrative (72b18) |
| *Post. An.* I.1, 71a11–17 | prior knowledge is of two kinds — that the thing is; what the term means — with a combined third case ("unit") |
| *Post. An.* I.4, 73a34–b26 | two senses of *per se*: the subject's definition contains the attribute, or the attribute's definition contains the subject; anything else is accidental |
| *Post. An.* I.4, 73b27–74a3 | the commensurate universal: belonging to every instance of its subject, essentially and as such; demonstration is of the primary subject |
| *Post. An.* I.6, 74b5–75a17; 75a18–37 | demonstrative knowledge rests on necessary premises; no demonstrative knowledge of the non-essential accident |
| *Post. An.* I.7, 75a38–b20 | no passing from one genus to another; geometrical truths are not proved by arithmetic |
| *Post. An.* I.8, 75b21–36 | with commensurately universal premises the conclusion is eternal, so no attribute is demonstrated of perishable things; "for the most part" qualification at 75b32 |
| *Post. An.* I.9, 76a26–b22 | the three elements of a science: subject genus, axioms, attributes; common and proper principles |
| *Post. An.* I.10, 76b23–77a9 | hypotheses, postulates, definitions; demonstration is addressed to the discourse within the soul; without predicating one of many the middle term goes (77a5–9) |
| *Post. An.* I.13, 78a22–79a16 | *quia* against *propter quid* in four modes; planets/twinkling (78a30–38); moon/spherical (78b3–10); wall/breathing, remote cause, second figure (78b13–34); subalternation of sciences (78b34–79a16) |
| *Post. An.* I.14, 79a17–32 | the first figure is the most scientific; it is the vehicle of the mathematical sciences and yields the reasoned fact |
| *Post. An.* I.22, 77a36–78a21 | the questions proper to each science; no crossing of subject matter |
| *Post. An.* I.30, 88a5–17 | no demonstration of chance conjunctions, which are neither necessary nor general |
| *Post. An.* II.1, 89b21–90a35 | four kinds of question — that, why, whether it is, what it is — all reducing to whether there is a middle and what it is |
| *Post. An.* II.8, 93b22–94a19 | definition as middle; we cannot apprehend what a thing is without apprehending that it is (93a16–24) |
| *Post. An.* II.11, 94a20–95a9 | the four causes as four kinds of middle; efficient cause as middle at 94a36–b8, final cause at 94b8–18 |
| *Post. An.* II.16–17, 98b4–10 | deciduousness / broad-leaved / vine: reversal of middle and major in reciprocal predication (see the correction in §A.5) |
| *Post. An.* II.19, 99b18–100b17 | principles are not demonstrated: perception, memory, experience, *epagōgē*; *nous* grasps the first premise (100b5–17) |
| *Nic. Eth.* VI.6, 1140b31–1141a8 | the first principle of what is scientifically known is grasped by *nous*, not by science, art, or practical wisdom |
| *Topics* I.1, 100a18–100b23 | dialectic reasons from *endoxa* — opinions of all, of most, or of the most reputable philosophers |
| *Topics* I.2, 101a25–37 | dialectic is a process of criticism, and the path to the principles of all inquiries |
| *Metaph.* Gamma 1–2, 1003a21–b10 | one science of being qua being; the *pros hen* structure of "being," with the "healthy" analogy |
| *Metaph.* Gamma 3, 1005b15, 1005b19–20; 1006a10–11 | non-contradiction stated; presupposed by anyone who knows; not demonstrable |
| *Metaph.* Gamma 4, 1006a28–1011a5 | elenctic refutation of the one who denies non-contradiction: he must signify something definite |
| *Prior An.* I.2, 24b18–20 | the definition of *syllogismos* |

### A.3 Aquinas: doctrine and locus

Verbatim Latin quotation is available in the underlying research file for every item marked
**quotation** below; items marked **paraphrase** are summaries of the argument of the cited
passage, and a chapter that presents them as Aquinas's words is in defect.

| Locus | Doctrine | Kind |
|---|---|---|
| In PA I–II (Leonine, Rome 1882), lib. I lect. 1–44, lib. II lect. 1–20 | line-by-line literal exposition in *lectiones*, not independent questions | paraphrase |
| In PA I lect. 1 nn. 4, 6 | three acts of reason; the judicative part of logic is called analytic, "that is, resolutive," because certain judgment about effects requires resolution into first principles | quotation |
| In PA I lect. 2 nn. 4–5 | twofold pre-knowledge, *quia est* and *quid est*, of principle, subject, and property; *an est* precedes *quid est*, "for there are no definitions of non-beings" | quotation |
| In PA II lect. 1 n. 8 | "the cause is the middle in a demonstration, which makes us know; for to know is to know the cause of a thing" | quotation |
| In PA II lect. 1 n. 9 | Aquinas notes an apparent Aristotelian claim that the definition of the property is the middle, then adds his own qualification — a clear case of gloss rather than exposition | quotation |
| In PA II lect. 7 n. 9 | the middle of a *propter quid* demonstration is the *quod quid est*; what has another cause cannot be known without demonstration, yet there is no demonstration of the *quod quid est* itself | quotation |
| In PA II lect. 9 nn. 2–3 | the middle is the cause, and any of the four causes may be taken as middle | quotation |
| In Metaph., prooemium | the subject of a science is that whose causes and properties we seek; the subject of this science is *ens commune*, treated as separate from matter in being and in definition | quotation |
| Super Boet. De Trin. q.5 a.1 | three classes of speculable object by dependence on matter in being and in understanding, giving physics, mathematics, divine science | quotation |
| Super Boet. De Trin. q.5 a.3 | *separatio* (the intellect composing and dividing) for metaphysics; abstraction of form from sensible matter for mathematics; abstraction of the universal from the particular, common to all sciences | quotation |
| Super Boet. De Trin. q.5 a.4 | theology is twofold: the philosophers' theology, treating divine things as principles of the subject, and the theology handed down in Scripture, treating them as its subject | quotation |
| Super Boet. De Trin. q.6 a.1 | rational consideration terminates in intellectual by the way of resolution and proceeds from it by composition or discovery; hence *prima philosophia*, yet learned after physics, "*metaphysica quasi trans physicam*" | quotation |
| Super Boet. De Trin. q.6 a.4 ad 2 | where the effect does not equal the cause, the definition of the effect is taken as principle for demonstrating that the cause is and some of its conditions, the cause's quiddity remaining unknown | quotation |
| ST I q.1 a.2 | *sacra doctrina* proceeds from principles known by the light of a higher science, the science of God and the blessed, as optics proceeds from geometry and music from arithmetic | quotation |
| ST I q.1 a.8 ad 2 | philosophers' authorities are used as extraneous and probable arguments; canonical Scripture is used as arguing from necessity | quotation |
| ST I q.2 a.1 corp. and ad 2 | *per se notum* in itself and not to us, against in itself and to us; "God is" is self-evident in itself but not to us; the *quo maius cogitari non potest* argument yields existence only in the apprehension of the intellect | quotation |
| SCG I cc. 10–11 (esp. c.11 n. 1) | the same distinction: simply speaking God's existence is self-evident, since God is his own being, but because we cannot conceive what God is it remains unknown to us | quotation |
| ST I q.2 a.2 corp. | "*Duplex est demonstratio*": one through the cause, called *propter quid*, by what is prior simply; one through the effect, called *quia*, by what is prior for us | quotation |
| ST I q.2 a.2 ad 2 | when a cause is demonstrated through the effect, the effect must be used in place of the definition of the cause; what the name signifies, not the *quod quid est*, is taken as middle, since *quid est* follows *an est*; the names of God are imposed from effects | quotation |
| ST I q.2 a.2 ad 1 | that God is, and the like, are not articles of faith but preambles to the articles; faith presupposes natural knowledge as grace presupposes nature | quotation |
| ST I q.2 a.3 corp. | "*Deum esse quinque viis probari potest*"; the five terminal phrases, each identifying the term as what all men understand, name, call, or say is God | quotation |
| ST I qq.3–11; SCG I cc. 14–28 | the divine attributes are established in separate later questions and chapters, in SCG by the *via remotionis* (c.14: we know what God is not) | paraphrase, with c.14 title and n. 2 quoted |
| ST I q.13 a.3 | in divine names the perfection signified (*res significata*) belongs to God more properly than to creatures; the mode of signifying (*modus significandi*) does not | quotation |
| ST I q.13 a.5 | nothing is predicated univocally of God and creatures; names are said analogically, by proportion, a community "midway between pure equivocation and simple univocity" | quotation |
| ST I q.46 a.2 ad 7 | infinite regress is impossible in efficient causes ordered *per se* (stone, stick, hand); not judged impossible *per accidens* (hammers that break in succession; a man begotten by a man) | quotation |
| SCG I cc. 3, 7 | two modes of truth about God, some exceeding reason and some reachable by it; what reason naturally knows cannot be contrary to the truth of faith | quotation |
| SCG I c.13 nn. 14, 33 | ordered movers and ordered efficient causes, the same *per se* ordering used in the argument itself | paraphrase |

### A.4 Terminology

| Original | Literal sense | This book's word | Trap in the equation |
|---|---|---|---|
| *epistēmē* / *scientia* | scientific knowledge | knowledge through the cause | not modern "science"; it is knowledge of the necessary through its cause, and it names a state of the knower |
| *apodeixis* / *demonstratio* | demonstration | demonstration | not merely a valid argument; it requires necessity, immediacy, and a *per se* middle |
| *archē* / *principium* | starting point | principle | a principle is immediate and necessary for Aristotle; the book's "metaphysical principle" is any substantive starting claim, contested or not |
| *axiōma*, *thesis*, *hypothesis*, *horismos* | axiom, thesis, hypothesis, definition | the kinds of principle | *hypothesis* here asserts that a subject is; it is not the modern "working assumption" |
| *meson* / *medium demonstrationis* | middle | middle term | the middle is the cause, not merely the shared term of two premises |
| *kath' hauto* / *per se* | in itself | *per se* (left in Latin) | *per se* predication and a *per se* ordered causal series are two different uses of the phrase; never let one licence the other |
| *katholou* | universal | commensurate universal | not "universally quantified"; it requires belonging to every instance essentially and as such |
| *tou hoti* / *quia*; *tou dioti* / *propter quid* | of the fact; of the reasoned fact | showing *that*; showing *why* | the English pair invites the idea of a two-rung ladder; in the texts these are modes of demonstration, and *quia* is genuinely demonstrative |
| *endoxa* / *probabilia* | reputable opinions | what will be granted | not "probable" in any numerical sense |
| *nous* / *intellectus*; *epagōgē* / *inductio* | intuition; induction | grasp of principles; induction | *epagōgē* is not modern enumerative induction, and the relation between the two terms is itself disputed |
| *quod quid est* / *quid est* | what-it-is | the essence, or its definition | distinct from *quid significet nomen*, what the name signifies; conflating them collapses Aquinas's whole adaptation |
| *per se notum quoad se* / *quoad nos* | self-evident in itself / to us | self-evident in itself; self-evident to us | "self-evident" in modern English usually means *quoad nos*; the distinction is the refusal of the Anselmian argument |
| *res significata* / *modus significandi* | thing signified / mode of signifying | what a name names; how it names it | a distinction about divine predication, not a general test for conceptual against real content |
| *separatio* / *abstractio* | separation / abstraction | negative judgment; abstraction | *separatio* is a distinct operation of the intellect, not a higher degree of abstraction |
| *resolutio* / *compositio* | resolution / composition | from effects to causes; from causes to effects | the later labels *via iudicii* and *via inventionis* are not Aquinas's words here |
| *viae* | ways | ways | not *probationes*; "the Five Proofs" is the manuals' title, not Aquinas's |
| *praeambula fidei* | preambles to faith | preambles to faith | a preamble is demonstrable and may still be held by faith by one who cannot follow the demonstration |

### A.5 Correction notes

These are misattributions commonly made. A chapter that repeats one is in defect.

1. **The deciduousness example is not in I.13.** Deciduous character, broad leaves, vine is at
   *Post. An.* 98b4–10, in Book II (about II.16–17 in the Ross division), not at I.13. It
   illustrates the reversal of middle and major in reciprocal predication, not the *quia* /
   *propter quid* distinction of I.13. The standard I.13 examples are planets/twinkling,
   moon/spherical, and wall/breathing. Some secondary literature makes this mistake.
2. **The threefold schema of prior knowledge is not Aristotle's.** *Post. An.* I.1, 71a11–17
   gives two kinds of prior knowledge — that the thing is, and what the term means — with a
   combined third case. The *an sit* / *quid sit* / *quia est* triad is later scholastic
   tradition. Aquinas's own text at In PA I lect. 2 nn. 4–5 is likewise twofold (*quia est* and
   *quid est*) applied to three items (principle, subject, property).
3. **"Three degrees of abstraction" is the manuals', not Aquinas's.** Super Boet. De Trin. q.5
   a.3 distinguishes *separatio* from two kinds of *abstractio*; *separatio* is a different
   operation of the intellect, not a third degree of the same one.
4. **The Five Ways are *viae*.** Aquinas's word at ST I q.2 a.3 is *viae*, not *probationes* or
   *demonstrationes*, and the arguments are compressed rather than set out syllogistically. Each
   concludes that something is, under a name all men use, not what it is. The attributes are
   argued separately in qq.3–11.
5. **Aquinas does not use *subalterna* at ST I q.1 a.2.** He describes the structure — proceeding
   from principles known by the light of a higher science — without applying the technical label.
   *Praeambula fidei*, by contrast, is his own phrase at q.2 a.2 ad 1.
6. **Anselm is not named in ST I q.2 a.1.** The identification of the *quo maius cogitari non
   potest* argument as Anselm's (*Proslogion* 2–4) is standard, but the article names John
   Damascene in the *sed contra*, not Anselm.
7. **The four-term-fallacy problem for analogical middles is not Aquinas's theme.** ST I q.13
   a.5 states the doctrine of analogy; the difficulty for syllogistic middles is a construction
   of the later tradition, above all Cajetan, *De nominum analogia* (1498).
8. ***Via inventionis* and *via iudicii* are later labels.** Aquinas's words at Super Boet. De
   Trin. q.6 a.1 are *compositio* or *inventio*, and *resolutio*.
9. **Cite Bekker, not chapters.** Chapter divisions of the *Posterior Analytics* differ between
   the medieval commentary tradition and modern editions. The Aquinas commentary labels
   94a20–95a9 "Caput 11"; the Ross edition may split it across II.9–II.10 or II.10–II.11. The
   I.1/I.2 break falls at 71b8 with a one-line overlap. The Bekker numbers are unambiguous.
10. **"Better known" means better known in nature.** *Post. An.* 71b29–72a5 distinguishes the
    two senses and settles on priority in nature; reading condition (4) epistemically is a
    minority view, not the text's plain sense.

### A.6 Verification status

**Verified to a primary locus.** Every Aristotle item in §A.2 except as noted below, checked in
Mure, Ross, or Pickard-Cambridge with the Bekker numbers. Every Aquinas item in §A.3, checked
against the Latin at corpusthomisticum.org in the editions named in §A.1.

**Verified with a stated doubt.**

- *Nic. Eth.* VI.3 and VI.6: text confirmed; the exact opening line numbers (1139b18 against
  1139b19) are approximate.
- *Topics* I.1 and I.2: text confirmed in Pickard-Cambridge; the Bekker numbers come from
  standard reference works, not from line numbers in the consulted text.
- *Metaph.* Gamma 1–2: text confirmed in Ross; the Bekker numbers from standard reference.
- *Metaph.* Gamma 3–4 (1005b15, 1005b19–20, 1006a10–11): Bekker numbers taken from the Stanford
  Encyclopedia article on Aristotle on non-contradiction (Gottlieb 2023), which cites them.
- *Post. An.* II.11 and II.16–17: Bekker numbers confirmed; chapter numbers vary (correction 9).

**Resting on named secondary scholarship, not on a primary locus.**

- Demonstration as teaching and exposition rather than discovery: Barnes, "Aristotle's Theory of
  Demonstration," *Phronesis* 14 (1969): 123–152; reprinted in *Articles on Aristotle* 1 (1975),
  65–87. Both page ranges confirmed. Barnes revised the thesis in the second edition of his
  *Posterior Analytics* (Clarendon, 1993). Responses to note: Bolton (1990) on dialectic and
  peirastic, Ferejohn (1991), Detel (1993).
- The reading of *Post. An.* II.19 (*nous* and *epagōgē*): disputed. Barnes (2nd ed. 1993,
  268–275) reads it as a natural cognitive process; Smith's Stanford Encyclopedia treatment
  offers a capacity reading; Kahn (1981) and Lear (1980) differ again.
- The elenchus of *Metaph.* Gamma 4: whether it shows that non-contradiction is true or only that
  it cannot be disbelieved. Wedin (2004) for the ontological reading; Politis (2004) differs.
- The analogical middle: Cajetan, *De nominum analogia* (1498), is the locus classicus;
  Hochschild, *The Semantics of Analogy* (Notre Dame, 2010), argues that earlier readers
  misunderstood Cajetan. The Stanford Encyclopedia article "Medieval Theories of Analogy"
  surveys the dispute.
- Whether the Five Ways are complete demonstrations: Kenny, *The Five Ways* (Routledge & Kegan
  Paul, 1969), argues they fail; Wippel, *The Metaphysical Thought of Thomas Aquinas* (2000),
  gives the fullest modern account of the metaphysical foundations; Kretzmann (via the Stanford
  Encyclopedia article on Aquinas) is more sympathetic; Feser, *Five Proofs of the Existence of
  God* (Ignatius, 2017), defends them.
- Whether metaphysics can be a demonstrative science on the Aristotelian model at all, given
  that being is not a genus (*Metaph.* III.3, 998b22) and that God has no real definition
  available to us: discussed by Wippel (2000); no page-level verification.
- The manual tradition: Gredt, *Elementa philosophiae Aristotelico-Thomisticae* (Herder; 7th ed.
  1937, 13th ed. 1961), confirmed to exist, with no passage verified. The characterization of
  the manual layer in §A.5 corrections 3, 4, and 7 is a tradition-level judgment; no specific
  manual page was checked.

**UNVERIFIED. Do not upgrade these.**

- *Topics* VIII.5, 159b4ff. on peirastic: the Bekker number comes from secondary sources
  (Bolton 1990; the Stanford Encyclopedia article on Aristotle's logic) and was not checked
  against a primary text.
- Barnes, *Posterior Analytics*, 2nd ed. (Clarendon, 1993): widely cited, not directly checked.
- Aquinas, De ver. q.10 a.12; In Phys. VIII; SCG II c.38: referenced in the earlier research but
  never fetched.
- The date of the In PA (commonly placed c. 1268–1272): not verified against a scholarly source.
- Garrigou-Lagrange, Maritain, and Boyer: no specific work or doctrine verified.
- No scholarly publication was verified as making correction 3 (*separatio* against the three
  degrees of abstraction) in those terms, although the point is common in the literature.
- All page-level arguments attributed above to Kenny, Wippel, Kretzmann, Feser, Cajetan,
  Hochschild, Bolton, Ferejohn, Detel, Wedin, Politis, Kahn, and Lear: the works were confirmed
  to exist; the arguments were not checked against the printed texts.

**One tension between the two research files, left standing.** The Aristotle file attributes the
threefold *an sit* / *quid sit* / *quia est* framing to Aquinas's commentary on *Post. An.* I.1;
the Aquinas file finds the commentary's own text (In PA I lect. 2 nn. 4–5) twofold and judges it a
faithful exposition of Aristotle. A chapter treating this material must work from the Latin of
lect. 2, not from either summary.
## Appendix B. The one-page analysis sheet

### B.1 What this is

The sheet is the shape a worked analysis takes on the page: six headings, in
the order of §2, with the two required sub-elements. It is a layout convention
for the author and a habit for the reader, not a form to be filled in and not
a document the reader is expected to reproduce.

The single test of the layout is that the headings can be removed and the
analysis still read as continuous prose. If removing them leaves a page of
disconnected fragments, the analysis was written as a form and must be
rewritten.

This appendix is the one place in the book where a template may be displayed
as a template (§16.5).

### B.2 The sheet

```text
PASSAGE          author, work, locus; the text as written

CLAIM            the claim as the author states it
                 Plain-language reading: the same claim, ordinary diction

MEANING          terms carrying a technical sense
                 distinctions the argument needs
                 any term whose sense shifts between occurrences

WARRANT          premise by premise: what is offered in support
                 (definition / logical consequence / experience /
                 prior result / metaphysical principle / hypothesis /
                 revelation / provenance only)

BURDEN           the first proposition whose truth is not supplied
                 merely by vocabulary or by a previous citation

CONSEQUENCE      what follows if the burden is granted, at its actual
                 strength
                 Not yet established: what the tradition commonly
                 claims here that this argument has not reached

DENIAL           what rejecting the burden costs, and which kind:
                 contradiction / conflict with experience /
                 explanatory cost / rival framework / non-assent
```

Nothing else appears on the sheet. There is no verdict line, no score, no
identifier, and no checklist of rules satisfied.

### B.3 A worked specimen

**Passage.** A principle used throughout the tradition's causal arguments,
commonly given as *nemo dat quod non habet*: nothing gives what it does not
have.

**Claim.** Whatever a cause confers on its effect, the cause must itself
possess.

*Plain-language reading.* You cannot pass on what you have not got. A cause
cannot be the source of a feature unless that feature is somehow already in
the cause.

**Meaning.** Everything here turns on *have*. The tradition distinguishes
possessing a perfection in the same way the effect has it, possessing it in a
higher or more complete way, and possessing it in the way an instrument or an
agent possesses a power to produce it. Fire has heat as the water it heats has
heat; an architect does not have a house. Unless *have* is fixed, the principle
is either obviously false or unfalsifiable. *Give* is also technical: it means
being the source of, not transferring a quantity.

**Warrant.** As usually presented, the principle is offered as a metaphysical
principle, sometimes with an appeal to experience by way of examples. It is
often *received* by the reader as a definition, because on a sufficiently
elastic reading of *have* it cannot fail. That reading is available, and it is
the one to watch: if *have* means no more than *is able to produce*, the
principle reduces to the statement that a cause of a feature is able to cause
that feature, which is definitional and empty.

**Burden.** The burden-bearing premise is that *have* carries substantive
content, that is, that a cause must possess the perfection it confers in one of
a restricted range of determinate ways, and not merely in the sense of being
able to produce it. Everything the principle is used for depends on this, and
nothing in the vocabulary supplies it.

**Consequence.** Granting a substantive reading of *have*: a feature cannot
arise from a cause in which it has no foundation of any kind, so an account
that has a feature appearing with no source in its causes is ruled out.

*Not yet established.* The tradition standardly proceeds from here to the
conclusion that the perfections found in things pre-exist in their first cause
in a higher mode. Nothing so far has established that there is a first cause,
that the modes of possession form the hierarchy the argument needs, or that
possession in a higher mode is intelligible rather than merely asserted. Each
is a further argument.

**Denial.** A denier who holds that genuinely novel features can arise from
causes that in no sense contain them is not contradicting himself, and is not
denying anything we plainly encounter. He is committed to a rival framework, an
emergentist account on which some features are not inherited from their causes
at all, and he must then say what distinguishes cases where features are
inherited from cases where they are not. So: **rival framework**, with a real
explanatory cost attached, and not contradiction. Claiming contradiction here
would be the error §8.3 warns against.

**Notation.** None. Nothing in this analysis turns on quantifier or modal
scope; the work is all in the sense of *have*, and no predicate letter would
make that sense clearer. Compare §9.5.

### B.4 What the specimen demonstrates

Four things a reviewer should be able to see in it, and should require of
every worked analysis in the book:

1. The analysis reached a definite result and it was a limited one.
2. The burden was located in a word, not in a proposition anyone had stated.
   This is normal, and it is why the Meaning question precedes Warrant.
3. The statement of what is not yet established named the tradition's actual
   destination rather than gesturing at unfinished business.
4. The denial was classified honestly, against the interest of the argument.
