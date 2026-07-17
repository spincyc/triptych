# Virtues Reference Work

This profile governs the comprehensive philosophical and theological reference at `src/gpt/theology/virtues/`. The work studies virtue as habit, the theological and cardinal orders, the intellectual virtues, the virtues annexed to the cardinal virtues, and the principal related states distinguished by Aristotle, Augustine, and Thomas Aquinas. It is a theological reference work, not a discursive article, a catechism, a catalogue of personality traits, or an instrument for diagnosing another person's character. Its publication mirrors to `build/gpt/theology/virtues.pdf` and `doc/gpt/theology/virtues.pdf`.

## Comprehensive claim and controlling inventory

“All virtues” is meaningful only relative to a declared corpus and classification rule. The controlling corpus is Aristotle's securely attributed ethical works, principally the *Nicomachean Ethics*; Augustine's systematic treatments of faith, hope, charity, ordered love, and named Christian virtues; and Aquinas's *Summa theologiae* I--II, questions 49--70, II--II, questions 1--170, and III, question 85 on penance as a virtue, with III, question 90 controlling its virtue--sacrament boundary and context-conditioned divisions. Other authentic works may clarify a disputed classification, but a late handbook, modern list, or name resemblance cannot add an item by itself.

The document keeps `research/virtue-inventory.md` as its controlling census. Every candidate is recorded as one of:

- a principal theological, cardinal, moral, or intellectual virtue;
- a subjective species or potential part that the controlling source expressly treats as a virtue;
- a qualified or cognate state that a source distinguishes from virtue in the strict sense;
- an integral condition, act, gift, fruit, beatitude, counsel, passion, relation, or state of life that must not be counted as a coordinate virtue; or
- a rejected duplicate, translation variant, doubtful attribution, or unsupported modern addition.

The inventory records a stable key and sort key, Greek or Latin term where material, preferred English name, classification, formal object and act, exact primary loci, provenance status, opposition structure, appendix treatment, and unresolved qualification. Narrative prose may explain but may not silently enlarge the census.

## Taxonomic and sorting contract

The publication order is reproducible and must be stated near the beginning:

1. theological virtues, in the order of generation---faith, hope, charity---while identifying charity as first in perfection;
2. a dedicated cardinal overview that explicitly names prudence, justice, fortitude, and temperance, explains why they are four, defines integral, subjective, and potential parts, and distinguishes determinate habits from general conditions, overflow, and modes;
3. the four cardinal families in the received order prudence, justice, fortitude, temperance;
4. within each family, the principal virtue, nested integral conditions, subjective species, and potential or annexed virtues, with source-defined classification controlling before mere question order;
5. strict moral virtues that have secure provenance but no non-editorial position in the governing Thomistic parts-lists, ordered by a stated residual rule;
6. the remaining intellectual virtues, ordered from first principles through demonstrated knowledge to wisdom, then productive art, with prudence cross-referenced rather than duplicated; and
7. qualified Aristotelian or Christian states and the explicit exclusion ledger.

This is an order of exposition, not a claim that every later item is less excellent. Keep distinct the order of generation, order of perfection, logical dependence, and authorial exposition. A synonymous English rendering does not create another virtue, and a virtue appearing under two taxonomic aspects receives one controlling dossier and one appendix row. A species named only under a term used widely or analogically does not add a row unless the source establishes a distinct univocal habit; the inventory must record the reduction rather than silently omit the name. A publication-row count must be identified as a count of treated taxonomic entries, not a claim that principal roots, genera, subjective species, potential parts, and nested specifications are coordinate habits.

## Definition and dossier contract

The general account distinguishes power, act, disposition, habit, virtue, passion, gift, and grace. It explains acquired and infused virtues, the role of prudence and charity in connection among virtues, and the sense in which virtue makes both its possessor and characteristic act good. The Aristotelian mean is a rational measure relative to the agent and circumstances, not arithmetic mediocrity, moral compromise, or permission to perform an intrinsically wrongful kind of act.

Every counted virtue receives, directly or through a clearly identified parent dossier, these visible fields:

- `Class and provenance`---principal, species, annexed, intellectual, or qualified status and exact source loci;
- `Formal object`---the good, truth, relation, passion, or action that specifies the habit;
- `Characteristic act`---what the perfected power reliably does;
- `Defect-side opposition` and `Excess-side opposition`---only in the sense warranted by the source; and
- `Boundary`---a nearby act, passion, gift, counterfeit, or similarly named state that must not be confused with the virtue.

Definitions are source-grounded syntheses, not invented quotations. Material differences between Aristotle's natural teleology, Augustine's ordering by the love of God, and Aquinas's acquired and infused orders remain visible.

## Defect, excess, and terminology discipline

The two-flank schema applies strictly to moral matters whose action or passion admits too little and too much under the rule of reason. It does not apply univocally to every virtue:

- theological virtues have no intrinsic excess in their divine object;
- intellectual virtues are measured principally by truth, not by a quantitative mean of passion;
- justice has an objective mean of equality, so loss and gain in the parties are not two vices in the agent; and
- virginity, continence, friendship, shame, heroic virtue, gifts, fruits, and similar cases retain the classification supplied by their sources.

The terminal table keeps `Defect-side opposition`, `Virtue`, and `Excess-side opposition` in that left-to-right order. It must distinguish at least: a genuine mean flank; a named contrary that is not quantitative; an objective justice outcome; a counterfeit or corruption; a source-recognized but unnamed flank; the absence of one dedicated vice for a broad matter; and a genuinely non-applicable comparison. Do not use one dash or one residual code for all of those conclusions. The table also exposes each entry's taxonomic status and parent so that principal virtues, species, potential parts, and nested specifications do not appear coordinate.

Where a source supplies named extremes or contraries, preserve the source-grounded noun even when its English form is privative: `imprudence`, `disobedience`, `ingratitude`, and `irreligion` may not be suppressed merely to make labels lexically unrelated to their virtues. The ban applies to analytic fillers such as “too little courage” and “too much courage,” not to historical nomenclature. Source accuracy also overrides global word uniqueness: the same vice may stand in distinct formal relations, and a source's alternate terms may be retained together when choosing only one would distort the account. Preserve source-language terms, translation choices, and editorial qualifiers in `research/terminology-audit.md`. When Aristotle leaves a state unnamed, say so; do not invent a technical noun, manufacture symmetry, turn a medical condition or demographic trait into a moral vice, or attribute project-created language to an ancient or medieval authority.

## Required records and source hierarchy

The leaf keeps and imports one `generation-metadata.tex` record and keeps:

- `research/scope.md`, defining question, reader, thesis, corpus, comprehensive rule, authority classes, sorting method, rights boundary, limitations, and review state;
- `research/source-audit.md`, mapping governing definitions, classifications, and opposition claims to exact primary loci and recording translation status;
- `research/virtue-inventory.md`, the controlling census and exclusion ledger; and
- `research/terminology-audit.md`, recording every preferred vice label, source term, translation choice, unnamed extreme, collision avoided, and editorial descriptor.

Prefer the original Greek or Latin text and stable critical witnesses where practicable, then identified public-domain or otherwise lawfully cited human translations. The *Summa*'s own organization is evidence for Aquinas's classifications; a search result or modern virtue chart is not. Keep quotations short, identify the translation actually used, and record the independent rights status of external texts and online editions.

## Publication architecture

The work:

- begins with a title page, structured generation metadata, limitation, and table of contents;
- states the scope, corpus, definition of completeness, relation types, taxonomic levels, and complete sorting algorithm before the virtue dossiers;
- supplies the philosophical grammar of habit, mean, prudence, acquired and infused virtue, and ordered love;
- presents the theological virtues, then a dedicated section named **The Four Cardinal Virtues**, then each cardinal family;
- defines integral, subjective, and potential parts before using those classifications, and visibly states the parent and level of every strict appendix entry;
- places securely attested moral virtues outside the named parts-lists in a separately governed residual section rather than inventing a theological or cardinal-family parent;
- presents the remaining intellectual virtues and then qualified states after the strict moral order;
- explains gifts, fruits, beatitudes, passions, friendship, continence, shame, martyrdom, and heroic virtue sufficiently to prevent category errors;
- includes formation and self-examination principles without diagnosing persons or reducing virtue to a score; and
- ends with exact references and a landscape appendix containing every counted virtue in the same canonical order as the controlling inventory, with the defect and excess columns on either side of the virtue and reader-facing status, parent, and relation fields.

## Completion gate

The virtues reference is ready to install only when:

- every comprehensive claim agrees with the controlling inventory and every candidate is counted, nested, qualified, or excluded with a stated reason;
- definitions identify formal objects and characteristic acts rather than offering circular synonyms;
- Aristotle's mean is not extended to theological or intellectual virtue, justice, or qualified states without express warrant;
- every named defect or excess is traceable as a source term, checked translation, or visibly editorial descriptor;
- every named contrary supplied by the controlling source is represented even when its English form is privative, and every missing flank is identified as unnamed, undedicated, counterfeit, outcome, or non-applicable rather than collapsed into an unexplained dash;
- theological, cardinal, intellectual, acquired, infused, annexed, and qualified classifications remain distinct;
- the cardinal overview, each appendix parent, and each taxonomic status agree with the inventory's hierarchy;
- order of exposition, generation, logical dependence, and excellence are not conflated;
- source, translation, quotation, and rights boundaries are recorded;
- independent philosophical or theological review is claimed only when actually recorded; and
- universal metadata validation, settled multi-pass build, clean-log inspection, every-page visual review, PDF structure checks, installed/build comparison, catalog integration, supporting records, and release-policy accounting are complete.
