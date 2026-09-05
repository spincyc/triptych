"""The house-voice screen, and the prose it must never touch.

Every string in `TheDefectIsRefused` was reported by a max-effort evaluation
lane over one real leaf, in one of three iterations of one production run.
Every string in `LegitimateProseSurvives` is prose from the same corpus that
the same lanes read and deliberately left alone, or that a draft of this screen
wrongly refused. The second class is the important one, and it is here for the
reason the Latin body screen beside it gives: a refused leaf costs one rewrite,
and a wrongly refused sentence costs evidence, because the worker acting on the
refusal deletes the clause.

`RelativeClausesAreNotSubjects` is the second class at its sharpest. Every
sentence in it is a real published sentence that the first version of this
screen refused, because it tested one word either side of the work's name
instead of testing whether the name began a clause at all. What it therefore
refused was denominators, the extent of a search, and the 17 U.S.C.
\u00a7103(b) rights basis under which the Latin of two leaves is printed.
Those strings are tests now and not a list of accepted line numbers, because a
line number stops testing anything the moment the leaf is edited.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from _house_voice import exempt, house_voice, prose, unscreened  # noqa: E402

SPECIMEN = (ROOT / "src/claude/liturgy/roman-rite/1962/propers/temporal"
            / "54-fourteenth-after-pentecost")


def refused(text: str) -> list[str]:
    """What the screen saw, if anything, over one snippet."""
    return [saw for _line, saw, _quotation in house_voice(text)]


class TheDefectIsRefused(unittest.TestCase):
    """Each case is a locus a lane reported over a real leaf."""

    def test_retrieval_mechanics_printed_for_the_reader(self):
        # "Leave retrieval mechanics, checksums, query detail, discarded
        # leads, and operational audit in those records." Whether a file's
        # bytes matched a registered digest changes the truth of no claim.
        for text in (
                "His chapter stands in a rights-restricted facsimile, read "
                "on a rendered page image, hash-verified and retained "
                "nowhere.",
                "Schuster's \\work{The Sacramentary} vol.~III, pp.~136--138, "
                "was read on page images of the registered artifact, hashed "
                "and matched before reading.",
                "this Collect was read at printed p.~425 of the registered "
                "1861 scan, whose bytes were hash-matched before a page was "
                "opened",
                "His definitions are \\textbf{verbatim} the pair Aquinas "
                "attributes to the Gloss, from two separately retrieved and "
                "separately hashed artifacts."):
            with self.subTest(text=text[:40]):
                self.assertIn("retrieval mechanics stand in the body",
                              refused(text))

    def test_a_rule_reads_across_the_line_end_it_is_written_over(self):
        """The defect is a sentence, and a sentence is not a line.

        A line-at-a-time reader found about half of these, which is worse
        than useless: it reports a habit as a handful of stragglers.
        """
        self.assertIn(
            "retrieval mechanics stand in the body",
            refused("At the hinge stands Augustine's reading of "
                    "\\latin{primum}, carried in Latin by a\nsecond and "
                    "separately hashed thirteenth-century witness."))
        self.assertIn(
            "the count is labelled instead of stated",
            refused("\\latin{Salvatio} as a noun occurs \\textbf{once} in "
                    "the forty-five orations of the fifteen collated\n"
                    "formularies, and it is here --- a count over those "
                    "records and not over the\n\\work{Missale Romanum}."))

    def test_the_work_possesses_the_finding(self):
        for text in (
                "\\textbf{He reads the Secret's \\latin{tuae propitiatio "
                "potestatis} as the appeasing of the divine omnipotence}, "
                "where Gu\u00e9ranger and this guide's collation arrive "
                "independently.",
                "\\textbf{Gu\u00e9ranger construes \\latin{propitiatio "
                "potestatis} the same way}, independently agreeing with this "
                "guide's own collation."):
            with self.subTest(text=text[:40]):
                self.assertIn("the work possesses the finding", refused(text))

    def test_the_work_is_the_subject_of_its_own_clause(self):
        """The work opening a clause, with a finite verb after it.

        Both of these begin a main clause -- one after a coordinating
        conjunction, one after a full stop -- which is what makes the work the
        subject of a sentence rather than of a relative clause hanging off a
        source. `RelativeClausesAreNotSubjects` holds the other side.
        """
        for text in (
                "Neither is an official liturgical translation, and this "
                "guide has composed, translated, adapted and paraphrased "
                "nothing.",
                "It is a study companion, not an altar book or a hand "
                "missal. The project has translated nothing.",
                "They say so in the margin and print ``Pseudo-Chrys.'' The "
                "guide names the source that way and does not credit "
                "Chrysostom."):
            with self.subTest(text=text[:40]):
                self.assertIn("the work is the subject", refused(text))

    def test_the_production_pipeline_is_named_to_the_reader(self):
        for text in (
                "\\latin{regnum Dei} occurs in \\textbf{this formulary "
                "alone}, at exactly three loci, independently reproduced in "
                "a second provider's collation.",
                "\\textbf{The section number is XXXIII; an earlier form of "
                "this leaf printed Book II sect.~LXIX.}"):
            with self.subTest(text=text[:40]):
                self.assertIn("the production pipeline is named",
                              refused(text))

    def test_the_source_library_is_the_subject(self):
        self.assertIn(
            "the source library is the subject",
            refused("The \\work{Liber Comitis} pairs these two lessons at "
                    "these two extents, so the pairing is old; but the "
                    "library's sole registered treatment of Gal.\\ 5:16--24 "
                    "is Anthony of Padua's sermon."))

    def test_the_guides_own_apparatus_is_the_subject(self):
        for text in (
                "Hilary allegorises them, Jerome and Augustine forbid it "
                "--- and page~1's allegorical row prints that division under "
                "the names that hold it.",
                "both of which this repository tracks as public-domain "
                "text; the terminal appendix states the basis and its bounds "
                "in full.",
                "The paper is an unremarkable local one and the writer is "
                "unnamed: the entry's value is the neatness of the "
                "redirection, not the standing of its author."):
            with self.subTest(text=text[:40]):
                self.assertIn("the guide's own apparatus is the subject",
                              refused(text))

    def test_a_meta_label_on_the_guides_own_count(self):
        for text in (
                "three carry \\latin{semper} in an oration and \\textbf{this "
                "is the only one that carries it twice} --- a statement "
                "about fifteen collated formularies and not about the "
                "Missal.",
                "``Temporal'' against ``spiritual'' is a judgment and not a "
                "measurement."):
            with self.subTest(text=text[:40]):
                self.assertIn("the count is labelled instead of stated",
                              refused(text))

    def test_the_discipline_is_narrated_instead_of_kept(self):
        # `guidance/editorial.md` names each of these forms outright: "Prose
        # that says a difference was retained rather than silently
        # harmonised, that a negative result is bounded and correctable ...
        # is narrating compliance where it should simply be compliant."
        for text in (
                "Chrysostom and Theodoret do not raise the question at all. "
                "This guide reports the difference and adopts no "
                "harmonisation.",
                "The difference from Augustine is retained instead of being "
                "silently harmonized.",
                "Schuster reads something very slightly different, and the "
                "two readings are printed above rather than harmonised.",
                "the textual history is reported without harmonization",
                "The Communion's one addition is an address to the "
                "communicant and not a legal exclusion. Both negatives are "
                "bounded to the appointed elements.",
                "The absences are bounded to pp.~136--138 and correctable "
                "by anyone who reads the volume's introduction.",
                "The alphabetic acrostic can now be stated --- as documented "
                "reception."):
            with self.subTest(text=text[:40]):
                self.assertIn("the discipline is narrated instead of kept",
                              refused(text))

    def test_the_evidence_class_is_disclaimed_after_the_claim(self):
        for text in (
                "Rabanus compiles rather than composes, and is cited for the "
                "compilation and its arrangement and never as a vote.",
                "It is reported as the exposition printed under Bede's name "
                "and never as Bede.",
                "so it stands as his reading of the verse and never as the "
                "verse's sense"):
            with self.subTest(text=text[:40]):
                self.assertIn(
                    "the evidence class is disclaimed after the claim",
                    refused(text))

    def test_a_run_in_label_that_counts_the_guides_own_bounds(self):
        # The profile: "A heading, a run-in label, or a table column that
        # prints the discipline -- a retained control, a caveat field, a note
        # that a difference was not harmonised -- is the defect."
        for text in ("\\textbf{Four bounds travel with it.} The search was "
                     "run over two optical layers.",
                     "\\textbf{Three qualifications travel with all of it.}"):
            with self.subTest(text=text[:40]):
                self.assertIn("a run-in label prints the discipline",
                              refused(text))


class RelativeClausesAreNotSubjects(unittest.TestCase):
    """The subject of a relative clause is not the subject of the sentence.

    Every string here is published prose that the first version of this screen
    refused, and every one of them carries something a worker acting on that
    refusal would have deleted. `guidance/editorial.md` is explicit that this
    screen "reports a sentence to rewrite, never a sentence to delete" and
    that "every difference, negative result, bound and attribution stands
    after the repair"; a rule that points at the clause carrying the bound is
    pointing at exactly the words that may not go.
    """

    def test_the_denominator_of_a_bounded_negative_result(self):
        """The sentence subject is `No Collect, Secret or Postcommunion`.

        Delete the clause the old rule pointed at and the sentence becomes a
        false universal about the Missale Romanum instead of a bounded,
        correctable statement about fifteen collated formularies.
        """
        self.assertEqual([], refused(
            "\\textbf{The silence about temporal goods is a fact about the "
            "genre.} No Collect,\nSecret or Postcommunion of any of the "
            "fifteen 1962 identities this repository\nhas collated --- "
            "forty-five orations --- asks for food, drink or clothing."))

    def test_the_rights_basis_for_printing_the_latin(self):
        """17 U.S.C. \u00a7103(b), in a relative clause, in two leaves.

        The subject is the appointed text; the clause is why it may be
        printed at all. A screen that refuses this is asking a worker to
        delete the ground of the publication's own lawfulness.
        """
        for text in (
                "All ten appointed elements of this formulary are printed in "
                "the Pustet Missal of Ratisbon, 1862, which this repository "
                "tracks as public-domain text.",
                "five of them are already in print in the Pustet Missal of "
                "Ratisbon of 1862, which this repository tracks as "
                "public-domain text.",
                "the same form is printed in the Pustet Missal of Ratisbon, "
                "1862, which this repository tracks as public-domain text "
                "--- which shows the recasting is old."):
            with self.subTest(text=text[:40]):
                self.assertEqual([], refused(text))

    def test_the_extent_actually_searched(self):
        """The subject is the preacher, or the passage, or the formulary."""
        for text in (
                "And the one medieval preacher the library registers on this "
                "Epistle expounds it beside a different Gospel.",
                "the one Bellarmine passage this repository registers falls "
                "at Ps.~33 vv.~2--3, reaching no appointed verse of any "
                "element",
                "And across the fifteen 1962 formularies this repository has "
                "facsimile-collated, \\latin{regnum Dei} occurs in this "
                "formulary alone."):
            with self.subTest(text=text[:40]):
                self.assertEqual([], refused(text))

    def test_a_cross_reference_is_not_a_subject(self):
        """Naming the appendix inside a sentence is not making it the subject.

        The lane that read these reported the sentence whose subject IS the
        apparatus and left these standing.
        """
        for text in (
                "Two limits belong here rather than in the terminal "
                "appendix, because they change what this section claims.",
                "The tension the page-2 dossier reports --- an Asaph title "
                "on a psalm that mourns the temple --- is old.",
                "together they are the warrant for what this guide says"):
            with self.subTest(text=text[:40]):
                self.assertEqual([], refused(text))


class TopicIsNotForm(unittest.TestCase):
    """Five rules fired on subject matter, in a corpus that has that matter.

    The module claims of itself that every rule fires on a form and never on a
    topic. These five did not, and each of them refuses a plain sentence this
    library could print on any page. They are deleted or re-formed; the
    sentences stay here so that re-adding one has to face them.
    """

    def test_the_digest_is_a_book_this_library_cites(self):
        for text in ("The \\work{Digest} of Justinian treats the same "
                     "question at 1.3.2.",
                     "Cassiodorus digests the psalm into three parts.",
                     "Book V of Isidore's \\work{Etymologies} is a "
                     "compressed digest of late Roman jurisprudence."):
            with self.subTest(text=text[:40]):
                self.assertEqual([], refused(text))

    def test_a_leaf_is_a_leaf_of_a_tree_and_of_a_codex(self):
        for text in ("The fig tree bore no leaf, and the Lord cursed it.",
                     "No leaf of the Ottobonianus carries the rubric."):
            with self.subTest(text=text[:40]):
                self.assertEqual([], refused(text))

    def test_an_earlier_form_belongs_to_the_antiphon_too(self):
        self.assertEqual([], refused(
            "An earlier form of this antiphon stands in the Ottobonianus "
            "margin."))

    def test_a_revision_is_what_happened_to_the_missal_in_1568(self):
        for text in ("The revision of 1568 removed the sequence.",
                     "Wilson holds its ``Gelasian'' portions to be a "
                     "revision based on the Gregorian type.",
                     "Mercy is not a revision forced upon God."):
            with self.subTest(text=text[:40]):
                self.assertEqual([], refused(text))

    def test_a_page_of_a_source_has_a_possessive_too(self):
        self.assertEqual([], refused(
            "Read at page~174's running head in the Pustet printing, which "
            "carries the further halved number."))


class LegitimateProseSurvives(unittest.TestCase):
    """Every case is prose the lanes read and left standing.

    Several are prose an earlier draft of this screen refused. A rule that
    fired on any of them would have a worker delete a denominator, a bounded
    negative, or a fact about a source.
    """

    def test_a_denominator_stated_in_an_oblique_case(self):
        # The dangerous false positive, and the reason the screen asks
        # whether the work's name begins a clause. "Of the fifteen
        # formularies collated in this repository" is the denominator of the
        # count in the same sentence; a worker told it was a defect deletes
        # the denominator.
        for text in (
                "Of the fifteen formularies collated in this repository, "
                "three carry \\latin{semper} in an oration.",
                "neither a registered artifact of this repository, the "
                "registered excerpt covering only cols.~1--40",
                "Theodoret is reporting about the Hebrew, and no Hebrew "
                "psalter stands behind this guide.",
                "the clause-for-clause correspondence recorded for this "
                "leaf",
                "no Psalterium Romanum witness was collated for this leaf"):
            with self.subTest(text=text[:40]):
                self.assertEqual([], refused(text))

    def test_the_work_in_the_object_position(self):
        """The subject test is a subject test, not a word search."""
        self.assertEqual(
            [], refused("The reading \\latin{undecim} controls this "
                        "publication."))

    def test_a_bounded_negative_result(self):
        # The profile requires these and the lanes protected them by name:
        # the subject is a source, or the extent actually searched.
        for text in (
                "None of the three orations stands in the Veronense on a "
                "search of two uncorrected optical layers.",
                "The \\work{Breviarium Romanum} itself was not opened.",
                "Gu\u00e9ranger's judgment rests on Tommasi's Antiphonary "
                "and ``the ancient liturgists,'' neither consulted.",
                "Antiphon texts are routinely shortened for chant, so both "
                "changes may be conventional rather than expressive, and "
                "that count was not run.",
                "Two of the three 1962 assignments in the rotation were "
                "verified against collated text."):
            with self.subTest(text=text[:40]):
                self.assertEqual([], refused(text))

    def test_a_claim_local_evidence_state_or_source_status(self):
        for text in (
                "Schuster's \\work{The Sacramentary} vol.~III, pp.~136--138, "
                "was read on page images of the registered artifact.",
                "the one Bellarmine passage falls at Ps.~33 vv.~2--3, and is "
                "in an abridged Victorian English translation rather than "
                "the Latin",
                "his sentences were not verified, so nothing is printed as "
                "his words"):
            with self.subTest(text=text[:40]):
                self.assertEqual([], refused(text))

    def test_a_source_that_harmonises_or_an_english_that_flattens(self):
        # The rule is about the guide's own restraint. A Father who
        # harmonises two Gospels, an English that flattens a Latin
        # distinction, and a book of harmonising material are facts about
        # those texts.
        for text in (
                "\\work{De consensu evangelistarum} II.66 harmonises the "
                "triumphal entry and moves straight to the cleansing.",
                "the reception stands in Book~IV --- his sweep of Mark-only "
                "material --- and not in the harmonising Books II--III",
                "the 1861 English flattens \\latin{a fidelibus tuis} into "
                "``thy faithful''",
                "These witnesses deepen rather than flatten the petition.",
                "The complete psalm refuses that flattening."):
            with self.subTest(text=text[:40]):
                self.assertEqual([], refused(text))

    def test_things_that_travel_with_other_things(self):
        self.assertEqual(
            [], refused("The Fifteenth Sunday's Communion is \\latin{Panis "
                        "quem ego dedero} --- which travels with the "
                        "Offertory \\latin{Immittet Angelus} at both its "
                        "occurrences."))

    def test_a_library_that_is_a_real_library(self):
        """A gallery entry cites the Library of Congress. It is not ours."""
        self.assertEqual(
            [], refused("\\work{Norwich Bulletin} (Conn.), 22 June 1912, "
                        "p.~6. Read in the Library of Congress Chronicling "
                        "America page text."))

    def test_a_statement_about_a_printed_page(self):
        for text in (
                "the superscript reference letters stand before the section "
                "numbers and not as part of them",
                "The convergence is about the psalm and not about the chant, "
                "which stops at v.~1.",
                "it remains a historical translation, not a syntactic "
                "control for the Latin"):
            with self.subTest(text=text[:40]):
                self.assertEqual([], refused(text))

    def test_a_bold_lead_in_naming_the_appointed_bounds(self):
        """Only a count of the guide's own bounds is a discipline label."""
        self.assertEqual(
            [], refused("\\textbf{the second of the two standing inside the "
                        "appointed bounds} --- and a third independent "
                        "Father setting the same limit."))

    def test_a_comment_is_not_reader_facing(self):
        self.assertEqual(
            [], refused("% An earlier form of this leaf printed sect.~LXIX;\n"
                        "% this guide's collation is recorded in the audit.\n"
                        "Wilson prints the Postcommunion at sect.~LXVIII."))

    def test_a_comment_after_a_line_break_is_still_a_comment(self):
        """`\\\\%` is a comment; `\\%` is a printed percent sign.

        A one-character lookbehind reads the second backslash of a LaTeX line
        break as an escape and screens the comment after it as prose.
        """
        self.assertEqual(
            [], refused("Wilson prints the Postcommunion at sect.~LXVIII. "
                        "\\\\% this guide's collation is in the audit\n"
                        "and the Secret at sect.~LXVII."))
        self.assertIn(
            "the work possesses the finding",
            refused("Ninety-five \\% of the orations are older, and this "
                    "guide's collation says so."))


class MaskingDoesNotManufactureMatches(unittest.TestCase):
    """What is cut out must not read as a space between its neighbours.

    Every rule's literal spaces are whitespace-tolerant, because the defect
    crosses line ends constantly. When a cut region was spaces too, the words
    on either side of it joined, and the screen reported phrases that are in
    no file.
    """

    def test_a_dropped_path_does_not_join_the_words_around_it(self):
        text = ("It follows the \\texttt{research/scope.md} workflow of "
                "Augustine.")
        words = " ".join(prose(exempt(text)[0]).split())
        self.assertNotIn("the workflow", words)
        self.assertIn("It follows the", words)

    def test_a_rule_does_not_reach_across_a_dropped_argument(self):
        self.assertEqual(
            [], refused("The two readings are printed above rather than "
                        "\\texttt{research/harmonise.md} harmonised copies "
                        "of one another."))

    def test_a_rule_does_not_reach_across_an_exempt_section(self):
        self.assertEqual(
            [], refused("The count runs over those records and not\n"
                        "\\section*{References}\n"
                        "over the Missale Romanum, which is a different "
                        "book.\n"))


class ProtectedRegionsAreNotRead(unittest.TestCase):
    """Four regions the guidance requires to carry exactly this register."""

    def test_the_terminal_appendix_and_the_references(self):
        for heading in ("Appendix: Scope and Qualifications", "References"):
            with self.subTest(section=heading):
                self.assertEqual([], refused(
                    f"\\section*{{{heading}}}\n"
                    "This guide has composed, translated, adapted and "
                    "paraphrased nothing, and every negative in this guide "
                    "is bounded to the corpora named. The scan's bytes were "
                    "hash-matched to the registered digest before a page was "
                    "opened."))

    def test_a_heading_without_its_star_still_heads_a_section(self):
        """One published leaf writes `\\section{Appendix: ...}`.

        A pattern that required the star screened that leaf's whole terminal
        appendix, which is the one region of a leaf that is required to read
        like this.
        """
        self.assertEqual([], refused(
            "\\section{Appendix: Scope and Qualifications}\n"
            "This guide has composed, translated, adapted and paraphrased "
            "nothing."))

    def test_a_leaf_local_alias_still_heads_a_section(self):
        """Six of the twenty published propers alias an environment.

        A leaf is free to alias `\\section*` too, and a screen that only knew
        the built-in name would read the appendix it defines as body prose.
        """
        self.assertEqual([], refused(
            "\\apxhead{Appendix: Scope and Qualifications}\n"
            "This guide has composed, translated, adapted and paraphrased "
            "nothing."))

    def test_a_protected_name_inside_a_sentence_heads_nothing(self):
        """Or one bold cross-reference silences the rest of the file."""
        for text in (
                "The \\textbf{References} list is long. This guide has "
                "composed, translated, adapted and paraphrased nothing.",
                "\\textbf{References} are given below, and this guide has "
                "composed, translated, adapted and paraphrased nothing."):
            with self.subTest(text=text[:40]):
                self.assertIn("the work is the subject", refused(text))

    def test_a_subsection_does_not_end_the_terminal_appendix(self):
        """The appendix runs to the end of the file, sub-headings and all."""
        self.assertEqual([], refused(
            "\\section*{Appendix: Scope and Qualifications}\n"
            "This appendix carries the work-wide bounds.\n\n"
            "\\subsection*{Search limits}\n"
            "This guide has composed, translated, adapted and paraphrased "
            "nothing, and every negative is bounded to the corpora named."))

    def test_the_page_two_sheet_carries_the_modern_critical_horizon(self):
        self.assertEqual([], refused(
            "\\section*{Scriptural Date and Location}\n"
            "The terminal appendix states the basis; this guide prints the "
            "traditional ascription beside the modern critical date."))

    def test_the_exploratory_notice_and_the_strongest_limit_field(self):
        text = (
            "\\section*{The Propers: Interpretive Possibilities}\n"
            "\\begin{studybox}{What this section is}\n"
            "Everything below is exploratory editorial and AI proposal, and "
            "this guide claims no historical intent for any of it.\n"
            "\\end{studybox}\n"
            "\\begin{proposal}{P1. Goods are ordered}\n"
            "\\pfield{Mechanism}{The formulary states one choice in two "
            "grammatical registers.}\n"
            "\\pfield{Controlling limit}{His wording is not quoted here, the "
            "passage standing in a column this guide may not quote until a "
            "page image is read.}\n"
            "\\end{proposal}\n")
        self.assertEqual([], refused(text))

    def test_the_limit_field_under_every_name_the_profile_allows(self):
        """"the strongest material limit, alternative, or disconfirming
        condition" -- three names, one field.

        `tools/check-content-preflight` accepts all three as the profile's
        fifth field. Reading only `limit` here left this screen refusing the
        very field that check requires, in the one place the guidance says
        the register belongs.
        """
        for heading in ("Strongest limit", "Controlling limit", "Limit",
                        "Strongest alternative", "Disconfirming condition"):
            with self.subTest(heading=heading):
                self.assertEqual([], refused(
                    "\\section*{The Propers: Interpretive Possibilities}\n"
                    "\\begin{proposal}{P1. Goods are ordered}\n"
                    "\\pfield{Mechanism}{One choice, two registers.}\n"
                    f"\\pfield{{{heading}}}{{No leaf for it exists here, and "
                    "this guide's collation reaches no further.}}\n"
                    "\\end{proposal}\n"))

    def test_a_field_of_the_authors_own_devising_is_not_the_carve_out(self):
        """The carve-out is the profile's field, not any field.

        A lane put it exactly this way: the substituted heading "is a field
        of the author's own devising, not the profile's mandated
        controlling-limit field, which the proposal carries separately, so it
        is not inside the carve-out."
        """
        text = (
            "\\section*{The Propers: Interpretive Possibilities}\n"
            "\\begin{proposal}{P4. The hope-formula lies past the cut}\n"
            "\\pfield{The control the corpus supplies}{Across the "
            "twenty-one collated text records, \\latin{gustate} stands in "
            "the Eighth and the Fourteenth only --- a count over those "
            "collated records and not over the Missal.}\n"
            "\\pfield{Controlling limit}{The antiphons' extents are "
            "inherited chant tradition.}\n"
            "\\end{proposal}\n")
        self.assertIn("the count is labelled instead of stated", refused(text))


class WhatWasNotReadIsSaidOutright(unittest.TestCase):
    """A cut region is a non-answer, and a non-answer has to be reported.

    Six of the twelve leaves that carry a manifest write their interpretive
    section with no `\\pfield`, and nothing else marks where the protected
    exploratory notice ends and the proposals begin. The section is therefore
    cut whole -- and if that were silent, dropping the field markup would be a
    legal way to take half a leaf's discovery prose out of the reach of this
    screen and of `proposal-fields` at once.
    """

    UNMARKED = ("\\section*{The Propers: Interpretive Possibilities}\n"
                "Everything below is exploratory editorial proposal.\n\n"
                "\\textbf{P1.} This guide has composed nothing, and the "
                "difference is retained rather than silently harmonised.\n")

    def test_an_unmarked_interpretive_section_is_not_screened(self):
        self.assertEqual([], refused(self.UNMARKED))

    def test_and_the_screen_says_so(self):
        self.assertEqual([(1, "The Propers: Interpretive Possibilities")],
                         unscreened(self.UNMARKED))

    def test_a_marked_one_is_screened_and_reported_as_read(self):
        marked = self.UNMARKED.replace(
            "\\textbf{P1.}",
            "\\begin{proposal}{P1}\n\\pfield{Mechanism}{One choice.}\n"
            "\\end{proposal}\n\\textbf{P1.}")
        self.assertEqual([], unscreened(marked))
        self.assertIn("the work is the subject", refused(marked))


class TheQuotationIsTheFilesOwnWords(unittest.TestCase):
    """What the refusal hands a worker has to exist in the file.

    The quotation used to be cut out of the *masked* text at fifty characters
    either side of the match, so it began mid-word, ended mid-word, and had
    spaces where the markup had been. A worker cannot search for a string like
    that, and a reviser handed one has to guess which words the screen meant.
    """

    SENTENCE = ("The \\work{Liber Comitis} pairs these two lessons at these "
                "two extents, so the pairing is old; but the library's sole "
                "registered treatment of Gal.\\ 5:16--24 is Anthony of "
                "Padua's sermon.")

    def test_the_quotation_occurs_in_the_source(self):
        for _line, _saw, quotation in house_voice(self.SENTENCE):
            self.assertIn(quotation, " ".join(self.SENTENCE.split()))

    def test_it_reaches_the_sentence_and_keeps_the_markup(self):
        quotations = [q for _line, _saw, q in house_voice(self.SENTENCE)]
        self.assertEqual(len(quotations), 1)
        self.assertTrue(quotations[0].startswith("The \\work{Liber Comitis}"),
                        quotations[0])
        self.assertTrue(quotations[0].endswith("sermon."), quotations[0])

    def test_it_contains_the_words_the_rule_saw(self):
        """A long quotation is trimmed around the match, not from its end."""
        long_one = ("Augustine reads it one way and Jerome another, and "
                    "the tradition after them is divided in the same terms "
                    "for eight centuries together, which is the whole of "
                    "what can be said from the witnesses reached here about "
                    "how the two readings stood beside one another in the "
                    "Latin west, and the point is worth making at length. "
                    "The library's sole registered treatment of Gal.\\ "
                    "5:16--24 is Anthony's sermon.")
        for _line, _saw, quotation in house_voice(long_one):
            self.assertIn("library's", quotation)


@unittest.skipUnless(SPECIMEN.is_dir(), "the specimen leaf is not in the tree")
class TheSpecimenLeaf(unittest.TestCase):
    """The live leaf the three evaluation iterations were spent on.

    Its earlier iterations' loci are repaired and the last iteration's are
    not, so it carries both classes at once. The numbers below are the
    screen's measured signal on real prose; they are asserted so that a
    change to a rule has to say what it cost.
    """

    # The loci the final iteration's lanes reported, as (file, line range).
    # Twenty-two, which is what the run terminated BLOCKED holding.
    REPORTED = (
        ("sections/30-commentary.tex", 393, 398),
        ("sections/30-commentary.tex", 428, 433),
        ("sections/30-commentary.tex", 709, 714),
        ("sections/30-commentary.tex", 1006, 1011),
        ("sections/30-commentary.tex", 1913, 1919),
        ("sections/30-commentary.tex", 450, 456),
        ("sections/30-commentary.tex", 1174, 1181),
        ("sections/30-commentary.tex", 1859, 1864),
        ("sections/30-commentary.tex", 1987, 1992),
        ("sections/30-commentary.tex", 1993, 1999),
        ("sections/30-commentary.tex", 2029, 2034),
        ("sections/30-commentary.tex", 2044, 2050),
        ("sections/35-source-grounded-synthesis.tex", 42, 47),
        ("sections/35-source-grounded-synthesis.tex", 22, 29),
        ("sections/35-source-grounded-synthesis.tex", 224, 231),
        ("sections/35-source-grounded-synthesis.tex", 384, 391),
        ("sections/35-source-grounded-synthesis.tex", 398, 402),
        ("sections/35-source-grounded-synthesis.tex", 440, 449),
        ("sections/35-source-grounded-synthesis.tex", 489, 493),
        ("sections/40-notable.tex", 113, 119),
        ("sections/40-notable.tex", 197, 203),
        ("sections/50-interpretive.tex", 158, 168),
    )
    # The one locus reported in both editions of the same sentence. It is one
    # defect and two repairs, so the recall count treats it as one.
    ALSO = ("sections/synthesis/20-integrated-commentary.tex", 111, 116)

    @classmethod
    def setUpClass(cls):
        cls.found = []
        for path in sorted(SPECIMEN.glob("sections/**/*.tex")):
            where = path.relative_to(SPECIMEN).as_posix()
            source = path.read_text(encoding="utf-8")
            for line, saw, quotation in house_voice(source):
                cls.found.append((where, line, saw, quotation))

    def covered(self) -> set[tuple[str, int, int]]:
        return {locus for locus in self.REPORTED
                if any(locus[0] == where and locus[1] <= line <= locus[2]
                       for where, line, _saw, _quotation in self.found)}

    def test_it_finds_seventeen_of_the_twenty_two_loci_the_lanes_found(self):
        """Recall, measured, with every miss named and priced.

        Three of the five were bought deliberately, and what they bought is
        `RelativeClausesAreNotSubjects` and `TopicIsNotForm`:

        - 30-commentary 1174--1181 is "the one Bellarmine passage this
          repository registers falls at Ps. 33" -- the same shape as the
          denominator at 35-source-grounded-synthesis 418, which is not a
          lane locus and must never be refused. No rule can separate them, so
          both go.
        - 30-commentary 1993--1999 was carried by `no leaf`, which also
          refuses "The fig tree bore no leaf".
        - 40-notable 113--119 is "It is the gallery's only Epistle entry",
          where the apparatus is a predicate and not a subject.

        The other two were never found: "The \\work{Breviarium Romanum} itself
        was not opened; this is a within-one-book control" needs a rule on
        `control` as a methodological noun, and the corpus uses the same word
        for a control the Latin supplies and a control in prayer; the last is
        a paragraph whose defect is that a count of the guide's own is its
        subject, with no word in it that is not ordinary English.
        """
        missing = sorted(set(self.REPORTED) - self.covered())
        self.assertEqual(len(self.covered()), 17, f"not found: {missing}")
        self.assertEqual(
            missing,
            [("sections/30-commentary.tex", 1174, 1181),
             ("sections/30-commentary.tex", 1987, 1992),
             ("sections/30-commentary.tex", 1993, 1999),
             ("sections/35-source-grounded-synthesis.tex", 384, 391),
             ("sections/40-notable.tex", 113, 119)])

    def test_the_second_edition_of_a_reported_sentence_is_found_too(self):
        """One sentence, two files, and both have to be repaired."""
        where, first, last = self.ALSO
        self.assertTrue(
            any(w == where and first <= line <= last
                for w, line, _saw, _quotation in self.found))

    def test_everything_it_reports_is_a_sentence_a_lane_named(self):
        """Precision, measured, and the one extra held by its words.

        Twenty loci, nineteen of them inside a range a lane reported. The
        twentieth is the full-edition twin of a sentence the lanes DID report,
        at 35-source-grounded-synthesis 491 and in the synthesis companion:
        the same clause stands a third time in the detailed commentary and the
        lane's location list did not reach it. It is held here by the words it
        contains rather than by its line, because a line number stops testing
        anything the moment the leaf is edited.
        """
        loci = self.REPORTED + (self.ALSO,)
        extra = [(where, line, saw, quotation)
                 for where, line, saw, quotation in self.found
                 if not any(where == f and a <= line <= b for f, a, b in loci)]
        self.assertEqual(len(self.found), 20)
        self.assertEqual(len(extra), 1, extra)
        self.assertIn("The library's sole registered treatment",
                      extra[0][3])

    def test_every_quotation_is_a_string_from_the_leaf(self):
        """The refusal a reviser acts on names words that are in the file."""
        collapsed = {}
        for path in sorted(SPECIMEN.glob("sections/**/*.tex")):
            collapsed[path.relative_to(SPECIMEN).as_posix()] = " ".join(
                path.read_text(encoding="utf-8").split())
        for where, line, _saw, quotation in self.found:
            with self.subTest(locus=f"{where}:{line}"):
                self.assertIn(quotation, collapsed[where])


if __name__ == "__main__":
    unittest.main()
