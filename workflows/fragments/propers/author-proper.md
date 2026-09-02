# Author or Revise Canonical Proper Leaf

## Your task

Author or revise the canonical proper leaf. The canonical leaf owns the
prose, research, and audit records. The synthesis artifact is mechanically
derived from it.

Where the packet's CARRIED_FINDINGS header is not empty, read it before you
begin. It holds blocking findings a content evaluation raised against the leaf
— `repair_target: "authoring"` — that no authoring stage has yet seen, because
the run went first to whichever owner the routing put ahead of you: the brief
you are about to work from was corrected, and these were not. They describe
the document you are re-authoring and they are still true of it. Address each
one and say in your summary what you did with it. This is not optional
context; before it existed the author re-authored blind and the next
evaluation spent five lanes finding the same defects again.

Work from the research brief the `research-synthesis` stage wrote to
`research/scope.md`, and not from any prose a controller composed for you.
`research/scope.md` is immutable input owned by `research-synthesis`. Read
it; do not edit, overwrite, append to, or regenerate it. Anything authoring
learns belongs in the files this stage owns, listed below.

## Steps

1. Create or update `main.tex` with the full research sequence:
   - Page 1: Propers map and four senses (Literal, Allegorical, Moral,
     Anagogical)
   - Page 2: Scriptural Date and Location (exactly one physical page,
     forced boundaries)
   - The Propers: Themes and Movement (begins page 3, exactly two complete
     pages, both substantively filled)
   - The Propers: Detailed Commentary (begins page 5)
   - The Propers: Notable and Quotable (3-5 non-obvious cultural/literary
     reuses: exactly the entries the brief's `Notable-and-quotable audit`
     covers)
   - The Propers: Interpretive Possibilities (4-6 exploratory proposals:
     exactly the ones the brief's `Interpretive-proposal audit` covers)
   - Sacramental Appendix (when required)
   - Appendix: Scope and Qualifications
   - References
   - Generation Metadata
2. Create or update `synthesis.tex` as a 2-line stub that defines
   `\TriptychSynthesisEdition` and inputs `main.tex`.
3. Create or update `proper-components.toml` with the component manifest.
4. Create or update `format.tex` with leaf-local LaTeX macros.
5. Create or update `generation-metadata.tex`. It carries three kinds of
   declaration and `check-generation-metadata` requires all of them:
   - `\AIDocumentRevisionTimestamp{...}` first, once.
   - `\AIGenerationProvenance{workflow_id}{workflow_version}{workflow_digest}{run_id}{seed_commit}{install_commit}`
     second, once. Read the first four straight off this packet's own header
     and copy them exactly:
     - `workflow_id` and `workflow_version` are the two halves of the header's
       `WORKFLOW:` line — a header reading `WORKFLOW: proper v9` gives
       `{proper}{9}`. Read the number from your own packet; do not carry over
       the one in this example.
     - `workflow_digest` is the header's `WORKFLOW_DIGEST:` value in full, all
       64 hex characters.
     - `run_id` is the header's `RUN_ID:` value.
     - `seed_commit` is the header's `COMMIT:` value — the commit this run was
       pinned to when it was seeded, which is not necessarily HEAD now, so take
       it from the header and never from `git`.
     - `install_commit` is `unknown`. It states the commit where the produced
       artifact entered the tree, and that commit does not exist yet while you
       are writing this file; whoever installs the publication records it, and
       inventing one now would be a claim nobody could check.
     Write the word `unknown` for any field you genuinely cannot read, and for
     that field only. Do not guess a digest, a run id, or a commit, and do not
     copy any of these six values out of the leaf's existing record or out of
     the prose of an `\AIModelContribution` — that prose was written by an
     earlier pass and states an earlier run. This packet's header is the only
     source for them. `content-preflight` holds the five run fields of the
     record against the run producing this leaf and fails the stage on any
     one of them that does not match, so a value carried over from the
     leaf's previous record is caught rather than published.
   - `\AIModelContribution{model}{qualifiers}{runtime}` records after it, one
     per model contribution.
   None of this renders: the macro typesets nothing, so the record leaves the
   built PDF byte-identical, and the gate refuses any digest, run id or commit
   from it that reaches the rendered page.
6. Create or update `web-edition.toml` with web edition eligibility.
7. Create or update `propers/verified.md` and `propers/retrieved.txt`.
8. Leave `research/scope.md` exactly as you found it. Authoring adds no
   audit record to it: the profile keeps operational audit in that record and
   has the Scope and Qualifications appendix point at it rather than repeat
   it. Publish only what the brief's audits cover. If an audit is missing, if
   it covers entries you cannot publish, or if the gallery or the proposals
   you would publish differ from the audited ones, block rather than publish
   an unaudited entry or amend the audit yourself.
9. Print every biblical date through the chronology macros, and print no
   other. `guidance/scripture-chronology.md` §14 forbids this guide to infer,
   research, harmonize or recall a biblical date; the corpus's answer for this
   formulary is in `src/{provider}/{proper}/research/chronology.toml` and
   restated in the brief's `Scriptural chronology audit`, and those are the
   only dates that may reach the page.

   Define two macros in `format.tex` and use them on page 2:

   ```latex
   % \chronology{subject}{relation}{label} -- one assertion of the corpus.
   % Typesets the label; the first two arguments are the corpus's own ids and
   % render nothing.
   \newcommand{\chronology}[3]{#3}
   % \chronodate{element-keys}{content} -- one dossier row's Date cell.
   % Typesets the content; the keys render nothing.
   \newcommand{\chronodate}[2]{#2}
   ```

   - `subject` and `relation` are copied from the record, exactly. `label` is
     the record's `label` — the source's own words — and never its `date`,
     which is the normalized form and is not for the page.
   - `element-keys` is the comma-separated list of appointed elements the row
     covers, in the manifest's spelling: `\chronodate{gospel,communion}{...}`
     for a row that carries both.
   - **Every appointed Scripture gets a cell**, including the ones the corpus
     dates nowhere. Where the status is `undated-in-tradition` or
     `research-pending`, or the element carries no assertion, the cell states
     that absence in the guide's own voice — a fact about the sources, in the
     register the house voice requires — and carries no figure at all.
   - **A Date cell may hold no figure outside a `\chronology` claim.** Not a
     year, not a reign, not a range, not an Anno Mundi number, whatever
     source you met it in. A well-formed year reads exactly like a right one,
     which is why this is the one place in the guide where a fact may not be
     stated without naming the assertion behind it.

   `content-preflight` runs `chronology-record-current` and
   `chronology-claims-supported` over what you write: a claim the corpus does
   not make at that element's own verses, a figure with no claim behind it,
   an appointed Scripture with no cell, or a record that has drifted from the
   corpus all fail the gate to `content-revision` with the defect named. A
   date you remember is not evidence, and a date a commentary prints is that
   commentary's reception, reported as such and never as the date of the
   passage.
10. Ensure the brief synthesis markers
   (`triptych:brief-synthesis:start`, `:end`, `:next`) are placed correctly
   for the two-page gate.
11. Follow `guidance/editorial.md` for evidence states, attribution,
    metadata, review, publication standards, and the house voice below.
12. Follow `guidance/liturgy/roman-1962-propers.md`, the profile that governs
    this genre: the fixed reader order, the five claim classes, the reception
    sweep, the gallery and proposal contracts, the terminal apparatus, and
    this genre's deltas against the house voice.
13. Follow `guidance/repository.md` for source ownership, target paths, and
    build rules.

## House voice

Two rules in `guidance/editorial.md` govern every reader-facing word you
write, and `guidance/liturgy/roman-1962-propers.md` states the deltas for a
proper guide. They are the difference between a guide that has finished its
research and a guide that keeps telling the reader it did one.

**State the finding, not the process that produced it.** Lead with the claim.
State the interpretation directly and let the evidence carry it. Integrate
evidence into the sentence that needs it. Remove self-explanation of method,
and remove any sentence whose main work is to justify that an interpretation
may be offered rather than to offer it: an editorial principle, the restraint
exercised, why one emphasis was preferred, what governs the section, why
caution is called for. Do not write "It is important to distinguish", "The
guiding principle here is", "Methodologically, this section", "We have chosen
to emphasize", or "This interpretation should be approached cautiously
because". Where the evidence genuinely limits a claim, qualify that claim,
briefly, beside it — and keep the qualification a qualification instead of
letting it become the section's organizing voice. Method, search bounds,
corpora checked, evidence classes, and negative results already have their
homes: the audit records the profile names, and the terminal `Appendix: Scope
and Qualifications`. The body is not one of them.

**Speak from within the tradition.** The governing voice is Catholic,
affirmative, tradition-inhabiting, source-disciplined, and historically
responsible. Present Scripture, liturgy, doctrine, patristic reception,
typology, and saintly interpretation in the theological grammar they use,
attributed to the witness who taught them: "The Fathers read", "Augustine
identifies", "the liturgy presents", "the Church receives", "the typology
joins". Not "later Christians believed", "a devotional reading
might see", "the Fathers understandably interpreted", "although tradition
claimed", "the Church came to read this as", "from a modern perspective".
Do not translate an inherited interpretation into secularized distance, do not
treat modern skepticism as the neutral default, and do not apologise for
typology, doctrine, sacramental interpretation, or saintly reception merely
because they are theological. Modern criticism is not the authority that
validates or invalidates a theological reading.

Neither rule suppresses evidence, and neither is ever satisfied by deleting
something:

- the modern critical horizon belongs in the page-2 explanatory row, where the
  profile requires it, and it may qualify authorship, dating, textual history,
  setting, and manuscript evidence;
- genuine disagreement between sources is stated and attributed to the sources
  that hold it, never harmonised into a consensus that does not exist;
- the secular, ironic, political, and hostile afterlives in `The Propers:
  Notable and Quotable` are the point of that gallery, and belong there;
- the terminal appendix, `References`, and the exploratory notice and
  `Strongest limit` of `The Propers: Interpretive Possibilities` are
  qualification by design, and the declarative rule does not reach them.

When a sentence is doubtful, look at its grammatical subject. If the subject is
a source, a text, a witness, or a fact — Augustine's lemma, the missal's
rubric, the psalm's modern critical date — the sentence is doing the guide's
work. If the subject is the guide, the reading, or an evidence class — "this
guide does not press", "the reading is documented reception rather than", "the
negative result is bounded and correctable" — it is narrating the process, and
the reader came for the finding.

## A restatement inherits the evidence state of what it restates

The guide says the same things at several lengths. A claim worked out at
length in `The Propers: Detailed Commentary` comes back compressed in `The
Propers: Themes and Movement`, in the two-page brief synthesis, in the
four-senses table on page 1, in a `Notable and Quotable` entry, and in an
`Interpretive Possibilities` proposal. Length is the only thing that changes.
A claim is not better evidenced for being said briefly: if it is an
unverified lead in the commentary it is a lead in every short form of it; if
a witness reaches the guide through a catena, an anthology, or an OCR
transcription and the commentary says so, the short form says so too; if a
negative result is bounded — one corpus, one language, a literal-string
sweep — the short form states the negative at the extent actually searched
and never promotes it into plain absence. The qualifications the brief
attaches to a claim travel with the claim into every place it appears, at
whatever length, and an exploratory proposal is labeled one wherever it is
restated.

Compression is where this fails, and it fails invisibly: each section reads
well on its own, and only the pair shows the drop, so a reader who meets the
short form alone is told something the evidence does not support. Where a
short form has no room for the qualification, it has no room for the claim
either. Say less, or say it as the lead it is.

This rule and the house voice above pull in one direction and are easy to
read as pulling apart. What travels with a claim is the qualification, and it
travels in the register the house voice requires: a fact about the material,
whose subject is a source, a text, a witness, or a bound. "Ambrose's surviving
commentaries do not treat the verse" carries the bound and is the guide's
work. "The negative result is bounded and correctable" narrates the sweep
instead, and belongs to `research/scope.md`. Neither rule is ever satisfied by
dropping the qualification, and neither licenses restating the audit in the
guide's own voice.

## Pagination constraints

- Page 1: propers map + four senses, no work-wide apparatus
- Page 2: Scriptural Date and Location only, exactly one physical page
- Themes and Movement: pages 3-4, exactly two complete readable pages
- Detailed Commentary: begins page 5
- Brief synthesis: must occupy exactly two physical pages (N and N+1)

## Result

Return a worker result with `disposition: "PASS"`, the artifact path
(pointing to `main.tex`), and a summary of what was authored or revised.

If `research/scope.md` is insufficient, contradictory, missing evidence you
need, or otherwise unsuitable to author from safely, do not repair it and do
not author around it. Return `disposition: "BLOCKED"`, naming in the summary
exactly what the brief lacks. The run stops there, and the deficiency is on
the record where the workflow can act on it; a brief quietly patched by the
author would leave no such record.

Needing evidence the brief does not carry is that insufficiency, and it is
the case most easily misread as something else. It is not a gap for this
stage to fill. Retrieving evidence is out of scope for authoring, whatever
the source and however easy the retrieval looks: no fetch, no download, no
reaching past the brief into a catalog, a library, or an edition the brief
did not put in your hands, and nothing recalled from model memory to stand
in for a date, a place, a genre, a locus, or an attribution. Ease is not
permission. A source one command away is as far out of scope as one nobody
holds, because evidence gathered here is evidence no research lane swept, no
coverage audit saw, and no rights check cleared.

The brief states, section by section, whether it supplies that section's
evidence. Where it says a section's evidence is not there, that is not a gap
for you to close either: write the section to the bound the brief records,
because the extent of what was actually searched is itself something the
guide is meant to carry — carried as a fact about the sources, in the
register the house voice requires, and never in the audit's own words.
Where you need what the brief neither carries nor bounds, block, naming the
section and the evidence it wanted. That block costs one stage; authoring
around it costs a full research round, and a guide resting on evidence no
stage audited costs more than either.
