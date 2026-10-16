"""`references-used` holds the loci an entry names, not only its work.

Proper-study run 4d16b5e19d25dad9 (Claude, postconciliar Twenty-ninth Sunday)
derived a concise study whose References still named four loci that only the
expansive study used: Douay-Rheims Ps 145:2; Augustine, *Enarrationes in
Psalmos* 95.5 and on Ps 118 under Schin; and Aquinas's *Postilla* on Psalm 16.
The synthesis preflight passed all four, because the works were cited
elsewhere in the concise, and the cold reviewer found them by hand (SYN-001).

`SynOneTests` is that concise References over a body that cites only other
loci of the same works, and every one of the four is refused. Everything
after it is the other half, and the more important one: prose the published
corpus writes that the locus test must not refuse, because a refusal goes to a
reviser who deletes what it names. `tools/check-content-preflight` sets out
the line at the head of its locus section.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools/check-content-preflight"
LOADER = importlib.machinery.SourceFileLoader("references_loci", str(TOOL))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
PREFLIGHT = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(PREFLIGHT)

DOCUMENT = "probe"

# The four entries SYN-001 named, as the concise printed them before its
# repair, and two it kept. Only the first four carry a locus the body below
# never cites.
DOUAY = (
    "\\item The Holy Bible, Douay--Rheims version, revised by Bishop Richard "
    "Challoner (Project Gutenberg text): Gn 1:26; Ps 16:1--8; 32:15--19; "
    "95:1--13; 145:2; Is 45:1--6; Mt 22:15--21; Phil 2:15--16.")
AUGUSTINE = (
    "\\item St Augustine, \\work{Enarrationes in Psalmos} 4.8; 16.2, 8; 57.8; "
    "95.2--3, 5, 8--9; 115.13; 118, under Schin; 124.7--8; Nicene and "
    "Post-Nicene Fathers, 1st ser., vol.~8.")
AQUINAS = (
    "\\item St Thomas Aquinas, \\work{Super I epistolam ad Thessalonicenses} "
    "c.~1, lect.~1, and \\work{Postilla super Psalmos} 16 and 32 (Corpus "
    "Thomisticum text).")
JEROME = (
    "\\item St Jerome, \\work{Commentarii in Matthaeum} III, on 22:15--21 "
    "(Migne, PL 26, Paris, 1845, cols.~162--163).")
BELLARMINE = (
    "\\item St Robert Bellarmine, \\work{A Commentary on the Book of Psalms}, "
    "trans. J. O'Sullivan (1866, abridged): on Ps 32:18--19; 95:5, 10, 13.")

# A concise body that cites every other locus of those works, including the
# neighbours of each one it leaves out: Ps 16 and Ps 95:5 as Bible verses,
# Augustine at 16.8 and at three other sections of Ps 95, the *Postilla* on
# Psalm 32. Bellarmine is used and never cited by number.
BODY = """\\section*{Commentary}
The Entrance Antiphon asks to be kept ``as the apple of thy eye'' (Ps 16:6,
8). The king is not saved by a great army (Ps 32:15--16). The gods of the
gentiles are devils (Ps 95:5), and the Lord made the
heavens. St Robert Bellarmine says the gods of the nations ``are not true
gods, but demons''.

St Augustine takes the coin as the soul's image (\\work{Enarrationes in
Psalmos} 4.8), and the eye's pupil as the Church kept by God (16.2, 8). He calls
the questioners hypocrites (57.8). Christ ``possesseth regions where the
Roman empire hath never yet reached'' (95.2), and the whited wall stands for
its definition (\\work{Enarrationes in Psalmos} 95.3). ``Thou hast entered
with a present'' (95.8--9); the rod of the wicked is for a season (124.7);
the vow is exacted (115.13).

St Thomas Aquinas writes that no temporal power can bring men to the
salvation of the just (\\work{Postilla super Psalmos} 32), and that the
Thessalonians' faith shows itself in work (\\work{Super I epistolam ad
Thessalonicenses} c.~1, lect.~1). Jerome reads the tribute as owed
(\\work{Commentarii in Matthaeum} III). Cyrus is anointed (Is 45:1); man is
made to God's image (Gn 1:26). Tribute is rendered (Mt 22:15--21), and the
faithful shine as lights (Phil 2:15--16).
"""


def references(*items: str) -> str:
    return ("\\section*{References}\n\\begin{itemize}\n"
            + "\n".join(items) + "\n\\end{itemize}\n")


class Leaf:
    """A three-document leaf in a scratch tree, written edition by edition."""

    schema = 2

    def setUp(self):
        scratch = ROOT / ".scratch/references-loci"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.leaf = self.root / "src/claude" / DOCUMENT
        (self.leaf / "sections").mkdir(parents=True)
        (self.leaf / "proper-components.toml").write_text(
            f"schema = {self.schema}\n")
        for edition, entry in (("research", "main.tex"),
                               ("synthesis", "synthesis.tex"),
                               ("homily", "homily.tex")):
            (self.leaf / entry).write_text(
                f"\\input{{{DOCUMENT}/sections/{edition}}}\n")
            self.write(edition, "\\section*{Commentary}\nAugustine.\n"
                       + references("\\item St Augustine, \\work{Sermo} 90."))
        PREFLIGHT.flag_defined.cache_clear()

    def write(self, edition: str, text: str) -> None:
        (self.leaf / f"sections/{edition}.tex").write_text(text)

    def check(self, edition: str = "synthesis") -> tuple[list[str], str]:
        return PREFLIGHT.check_references_used(self.leaf, self.root, edition)


class SynOneTests(Leaf, unittest.TestCase):
    """SYN-001's four loci, each refused, and nothing else."""

    def setUp(self):
        super().setUp()
        self.write("synthesis", BODY + references(
            DOUAY, AUGUSTINE, AQUINAS, JEROME, BELLARMINE))

    def refusal(self, problems: list[str], name: str) -> str:
        found = [line for line in problems if name in line]
        self.assertEqual(len(found), 1, problems)
        return found[0]

    def test_each_of_the_four_is_refused(self):
        problems, _summary = self.check()
        douay = self.refusal(problems, "Douay")
        augustine = self.refusal(problems, "Enarrationes")
        aquinas = self.refusal(problems, "Postilla")
        self.assertIn("(145:2)", douay)
        self.assertIn("95.5", augustine)
        self.assertIn("Ps 118", augustine)
        self.assertIn("Schin", augustine)
        self.assertIn("(Ps 16)", aquinas)

    def test_only_the_four_are_refused(self):
        """Every other locus of the same works is cited, and passes."""
        problems, _summary = self.check()
        self.assertEqual(len(problems), 3, problems)
        augustine = self.refusal(problems, "Enarrationes")
        self.assertIn("(95.5, Ps 118, Schin)", augustine)
        for cited in ("4.8", "16.2", "16.8", "95.2", "95.8", "124.7"):
            with self.subTest(cited=cited):
                self.assertNotIn(cited + ",", augustine.split(":", 1)[0])

    def test_the_refusal_says_what_the_repair_is(self):
        problems, _summary = self.check()
        for line in problems:
            with self.subTest(line=line[:60]):
                self.assertIn("never cites", line)
                self.assertIn("cite each where the prose relies on it, or "
                              "take it out of the entry", line)

    def test_the_bible_verse_beside_it_is_not_augustines_section(self):
        """Ps 95:5 is cited, as Douay-Rheims; Augustine's 95.5 still is not.

        The Bible verse stands in the body in the very form a looser
        citation of the section would take, and two lines from Augustine's
        name. It is not his: nothing names him between them.
        """
        problems, _summary = self.check()
        self.assertIn("95.5", self.refusal(problems, "Enarrationes"))
        self.assertNotIn("95:5", self.refusal(problems, "Douay"))

    def test_the_repair_passes(self):
        """The concise as derive-synthesis iteration 1 left it."""
        self.write("synthesis", BODY + references(
            DOUAY.replace(" 145:2;", ""),
            AUGUSTINE.replace("95.2--3, 5, 8--9", "95.2--3, 8--9")
            .replace(" 118, under Schin;", ""),
            AQUINAS.replace("16 and 32", "32"), JEROME, BELLARMINE))
        problems, summary = self.check()
        self.assertEqual(problems, [])
        self.assertIn("every one used in the body, and the", summary)
        self.assertIn("loci held to it every one cited there", summary)

    def test_citing_them_passes_too(self):
        """A locus kept is a locus cited where the prose relies on it."""
        self.write("synthesis", BODY.replace(
            "and the Lord made the\nheavens.",
            "and the Lord made the heavens; ``Put not your trust in "
            "princes'' (Ps 145:2).").replace(
            "(95.8--9);", "(95.8--9). All nations had devils for their gods "
            "(\\work{Enarrationes in Psalmos} 95.5); the soldiers paid "
            "tribute (\\work{Enarrationes in Psalmos} 118, under Schin);"
            ).replace(
            "the just (\\work{Postilla super Psalmos} 32)",
            "the just (\\work{Postilla super Psalmos} 32), and glosses the "
            "pupil of the eye (\\work{Postilla super Psalmos} 16)")
            + references(DOUAY, AUGUSTINE, AQUINAS, JEROME, BELLARMINE))
        self.assertEqual(self.check()[0], [])

    def test_the_research_edition_is_held_the_same_way(self):
        self.write("research", BODY + references(DOUAY))
        problems, _summary = self.check("research")
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("(145:2)", problems[0])


class ScopeTests(Leaf, unittest.TestCase):
    """Where loci are judged, and where only the work still is."""

    def setUp(self):
        super().setUp()
        for edition in ("research", "synthesis", "homily"):
            self.write(edition, BODY + references(DOUAY, AUGUSTINE, AQUINAS))

    def test_the_homily_is_judged_by_work_alone(self):
        """Spoken prose names no section; its References still must be used.

        The same entries pass at the work level, and an entry the homily
        never uses is still refused.
        """
        self.assertEqual(self.check("homily")[0], [])
        self.write("homily", BODY + references(
            DOUAY, "\\item Rupert of Deutz, \\work{De divinis officiis} "
            "XII.18."))
        problems, _summary = self.check("homily")
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("cited nowhere in the body", problems[0])

    def test_the_leaf_union_is_judged_by_work_alone(self):
        """Every document's References against every document's body."""
        problems, summary = self.check("leaf")
        self.assertEqual(problems, [])
        self.assertNotIn("loci", summary)


class LegacyLeafTests(Leaf, unittest.TestCase):
    """A schema-1 leaf keeps the work-level test in every edition."""

    schema = 1

    def test_a_schema_one_concise_is_not_judged_by_locus(self):
        self.write("synthesis", BODY + references(DOUAY, AUGUSTINE, AQUINAS))
        problems, summary = self.check("synthesis")
        self.assertEqual(problems, [])
        self.assertNotIn("loci", summary)


class LegitimateUseTests(Leaf, unittest.TestCase):
    """Prose from the published corpus's own habits, which must pass."""

    def passes(self, body: str, *items: str) -> None:
        self.write("synthesis", "\\section*{Commentary}\n" + body
                   + references(*items))
        problems, _summary = self.check()
        self.assertEqual(problems, [])

    def test_a_vulgate_psalm_cited_in_hebrew_numbering(self):
        """The Lectionary numbers the psalm the Douay-Rheims does not."""
        self.passes(
            "Behold the eyes of the Lord are on them that fear him (Ps "
            "33:18--19), in the Douay--Rheims English.",
            "\\item The Holy Bible, Douay--Rheims version: Ps 32:18--19.")

    def test_a_psalm_cited_whole(self):
        self.passes(
            "Its verses repeat the ends of Pss 56 and 59, whose titles set "
            "them in David's flight in the Douay--Rheims.",
            "\\item The Holy Bible, Douay--Rheims version: Ps 56:1, 5; "
            "59:1--2.")

    def test_a_work_the_body_never_cites_by_number(self):
        """Bellarmine is used throughout and never given a locus in prose.

        Two of the published concise studies write exactly this. Nothing in
        the body says which of his loci it leans on, so none is refused.
        """
        self.passes(
            "Bellarmine reads fear joined with hope as the mark of real "
            "love, and his Judge will have no regard of persons.",
            "\\item St Robert Bellarmine, \\work{A Commentary on the Book of "
            "Psalms}: on Pss 32:18--19; 95:13; 121.")

    def test_a_single_locus_in_a_work_the_body_uses(self):
        """One place given, and the body uses the work: that is the place.

        Chrysostom's work is cited by number in the body, so the body cites
        it by locus; but the entry gives one place in it, and there is no
        other the body could be using instead. Athanasius's single psalm and
        Rupert's book and chapter are the same case without the citation.
        """
        self.passes(
            "Chrysostom says the coin bears the image of the one it is owed "
            "to (\\work{Homilies on Matthew} 70). Rupert of Deutz hears the "
            "Gradual as the Church's answer, and the Greek expositions under "
            "Athanasius's name read Sion as the Church.",
            "\\item St John Chrysostom, \\work{Homilies on Matthew} 70.1--2, "
            "Nicene and Post-Nicene Fathers, 1st ser., vol.~10.",
            "\\item Rupert of Deutz, \\work{De divinis officiis} XII.18 "
            "(Migne, PL 170, col.~326).",
            "\\item \\work{Expositiones in Psalmos} printed under the name of "
            "St Athanasius, on Ps~95 (Migne, PG 27, cols.~415--416).")

    def test_a_section_cited_in_a_looser_form_after_the_author(self):
        """`(95, 9)` two lines after "Augustine" is his, not the Bible's."""
        for form in ("(95, 9)", "(Psalm 95, section 9)", "(on Ps 95 (9))",
                     "(95, s.~9)", "(95 \\S 9)", "(95:9)", "(95.2--3, 9)"):
            with self.subTest(form=form):
                self.passes(
                    "The Communion sings Ps 95:8--9. St Augustine reads the "
                    "courts as the Church (\\work{Enarrationes in Psalmos} "
                    "95.2): ``they themselves are the house of God'' "
                    f"{form}.",
                    "\\item St Augustine, \\work{Enarrationes in Psalmos} "
                    "95.2, 9.")

    def test_dashes_and_ranges_are_one_range(self):
        for form in ("95.8--9", "95.8\u20139", "95.8-9", "95.8 -- 9"):
            with self.subTest(form=form):
                self.passes(
                    "``Thou hast entered with a present'' "
                    f"(\\work{{Enarrationes in Psalmos}} {form}), and "
                    "``he is the image'' (\\work{Enarrationes in Psalmos} "
                    "4.8).",
                    "\\item St Augustine, \\work{Enarrationes in Psalmos} "
                    "4.8; 95.9.")

    def test_a_roman_book_with_its_chapters_used_by_subject(self):
        """`Rationale VI.131, 135`: one cited, the other used by subject."""
        self.passes(
            "William Durandus hears the Introit as the judgment by which "
            "God exalts the humble, and the Gospel as Christ reproving the "
            "Pharisees (\\work{Rationale} VI.135).",
            "\\item William Durandus, \\work{Rationale divinorum officiorum} "
            "VI.131, 135 (1568 printing).")


class EntryLociTests(unittest.TestCase):
    """What is read as a locus, and what is an edition's locator."""

    def labels(self, item: str) -> list[str]:
        return [label for _family, _kind, label, _key
                in PREFLIGHT.entry_loci(item)]

    def test_a_division_list_inherits_its_head(self):
        self.assertEqual(
            self.labels("St Augustine, \\work{Enarrationes in Psalmos} "
                        "16.2, 8; 95.2--3, 5, 8--9."),
            ["16.2", "16.8", "95.2-3", "95.5", "95.8-9"])

    def test_a_verse_list_and_a_range_across_chapters(self):
        self.assertEqual(
            self.labels("Douay--Rheims: Is 45:1, 4; Mt 8:28--9:9."),
            ["45:1", "45:4", "8:28-9:9"])

    def test_chapters_in_a_bible_list(self):
        self.assertEqual(
            sorted(self.labels("Douay--Rheims: Ps 32; 75; Dan 9; Eph 1--4; "
                               "3 Kings 8:30.")),
            ["1-4", "32", "75", "8:30", "9"])

    def test_the_psalms_a_commentary_is_named_on(self):
        self.assertEqual(
            self.labels("\\work{Postilla super Psalmos} 16 and 32."),
            ["Ps 16", "Ps 32"])
        self.assertEqual(
            self.labels("\\work{Enarrationes in Psalmos} 118, under Schin."),
            ["Ps 118", "Schin"])

    def test_edition_locators_are_not_loci(self):
        for item in (
                "Nicene and Post-Nicene Fathers, 1st ser., vol.~8.",
                "Chrysostom, \\work{Homilies on Matthew} 64, NPNF I.10 "
                "(1888).",
                "Migne, PL 26, cols.~54--56; PG 13:29--32.",
                "\\work{The Greek New Testament: SBL Edition}, version~1.2.",
                "Wikisource transcription, CC BY-SA 3.0.",
                "pp.~393--394, nos.~1602--1611 (Benziger, 1962).",
                "entries for 20~September 2026.",
                "\\work{Homilies on Matthew} 71; \\work{Sermo} 90.",
                "\\work{Moralia in Iob} III.3.3--6.8."):
            with self.subTest(item=item[:40]):
                self.assertEqual(self.labels(item), [])

    def test_an_entry_with_no_locus_keeps_the_work_level_test(self):
        self.assertEqual(
            self.labels("Bl.~Ildefonso Schuster, \\work{The Sacramentary}."),
            [])


if __name__ == "__main__":
    unittest.main()
