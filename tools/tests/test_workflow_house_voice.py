#!/usr/bin/env python3
"""The guide states its findings, and speaks from inside the tradition.

Two faults recur in the generated propers. The prose explains the editorial
process that produced a conclusion instead of giving the conclusion, and it
holds inherited Christian interpretation at arm's length as though a secular
vantage were the neutral one. `guidance/editorial.md` now owns both rules and
`guidance/liturgy/roman-1962-propers.md` states this genre's deltas; these
tests hold that where it has to hold, in the deterministic bytes the workers
are handed.

The workflow was causing the second fault, not merely failing to catch it.
`content-evaluation` asked whether disagreement was "preserved rather than
silently harmonized", and an evaluator reading a finished PDF can only verify
non-silence if the prose says so — so the cheapest way to pass was to write
"the difference from Augustine is retained instead of being silently
harmonized", which is exactly the defect. That criterion now asks whether the
disagreement is present and attributed. Four more causes of the same shape are
fixed with it, and the tests below name each one.

What this suite proves, and what it does not. It proves that the guidance
states both rules, that the fragments carry them, that the compiled packets
deliver them to the workers, that the repair routes are what they claim, and
that the illustrative examples below are labelled correctly on both sides:
prose that reads as a defect, and prose that must survive because a rule
deleting a required modern dating, a documented disagreement, or the Joyce
and Keynes afterlives would be worse than the fault it replaced.

It does not prove that any particular guide is free of the fault, and the
phrase list here is illustrative rather than a detector. It cannot be one.
The exemptions the rules state are section-scoped — the same sentence is a
defect in `Detailed Commentary` and required in `Appendix: Scope and
Qualifications` — and a sentence carries no section; and the fault is not
always a sentence, the plainest instance in the corpus being a table column
header. Enforcement is criteria 11 and 12 read by an evaluator that can see
which section it is reading, and the deterministic bytes that carry those
criteria to it are what is tested here.
"""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _workflow import (  # noqa: E402
    CHANGES_REQUIRED,
    FANOUT,
    HOST_MAX,
    SINGLE,
    STRICT_UNION,
)
from test_workflow_brief_ownership import propers_fragments  # noqa: E402
from test_workflow_research_fanout import (  # noqa: E402
    CONTENT_LANES,
    FRAGMENTS,
    RESEARCH_LANES,
    VISUAL_LANES,
    assert_lane_owns_its_findings,
    workflow_json,
)
from test_workflow_repair_routing import (  # noqa: E402
    AUTHORING,
    RESEARCH,
    RoutingCase,
    blocking,
)

GUIDANCE = ROOT / "guidance"
EDITORIAL = GUIDANCE / "editorial.md"
PROFILE = GUIDANCE / "liturgy" / "roman-1962-propers.md"

# The house voice changed the fragments a run is bound to, so it needed a
# version bump. It was 8 before and 9 after on the branch this suite was
# written on; merged onto the production line it lands at 12, over version
# 11's twenty-four-stage lifecycle.
HOUSE_VOICE_VERSION = 12

# The lanes that own the two new criteria. No lane was added for them: a voice
# defect is judged by whoever already reads the prose it appears in.
VOICE_LANE = "reception-sweep"
DECLARATIVE_LANE = "profile-conformance"


def flat(text: str) -> str:
    return " ".join(text.split())


def sentences(text: str) -> list[str]:
    """Reconstruct hard-wrapped Markdown into sentences."""
    return [part for part in re.split(r"(?<=[.;:?])\s+", flat(text)) if part]


# ---------------------------------------------------------------------------
# The illustrative phrase list, and what it is not
# ---------------------------------------------------------------------------
#
# Both faults share one sentence template:
#
#     <the tradition's reading>, not <what a modern critic would deny>
#     — and the guide <states / keeps / does not press> it.
#
# The discriminator is grammatical. A defective clause's subject is the guide,
# the reading, or an evidence class. A legitimate clause's subject is a source,
# a text, a witness, or a fact. Every pattern below is anchored on a defective
# subject or on an unmistakable piece of process vocabulary; none is anchored
# on the mere presence of a qualification, because qualification is what the
# profile requires.
#
# The list classifies the labelled examples below. It is not a detector over
# the corpus and must not be presented as one, for two reasons that no amount
# of further pattern-writing removes:
#
#   1. The exemptions the rules state are section-scoped, and a sentence
#      carries no section. `This guide does not settle the year of the
#      Passion` is a defect in `Detailed Commentary` and is exactly what
#      `Appendix: Scope and Qualifications` exists to say. The same string
#      has opposite verdicts, so no function of the string alone is right.
#      SECTION_EXEMPT_BUT_MATCHING below holds real corpus sentences that
#      prove it, and a test asserts that the list still matches them.
#   2. Not every defect is a sentence. The `{Control retained}` column at
#      `src/gpt/.../46-sixth-after-pentecost/main.tex:109` is a table column
#      header inside `The Propers: Themes and Movement`, and a sentence
#      matcher cannot see a column.
#   3. A phrase list is evaded by rewording: `a guide which` for `a guide
#      that`, `documented medieval reception` for the four adjectives listed
#      above, `X is reported here` for `this guide reports X`. Adding
#      patterns chases that forever, costs a false positive each time, and
#      buys nothing the evaluator reading the criteria does not already do
#      better. Do not answer a missed example by extending the list.
#
# Enforcement therefore lives where the review found it already working: in
# criteria 11 and 12 and the lanes that own them, read by an evaluator that
# can see which section it is reading. These tests prove the deterministic
# half of that — the guidance states the rules, the fragments carry them, the
# packets deliver them, and the examples are labelled correctly.

SELF_NARRATION = re.compile(r"""
    \b(this|the\ present|our)\ (guide|commentary|treatment|exposition
        |analysis|section|study|sheet)\b
        [^.;:]{0,80}?\b(reports?|does\ not|do\ not|declines?|refrains?
        |adopts\ no|makes\ no|asserts\ no|supplies|will\ not|treats
        |has\ not\ resolved)\b
  | \bthe\ analysis\ above\b
  | \ba\ guide\ that\b
  | \bthe\ comparison\ therefore\ asks\b
  | \bit\ is\ (important|worth)\ (to\ )?(distinguish|note|remember|stress
        |stating|saying|recording)\b
  | \bthe\ guiding\ principle\b
  | \bmethodologically\b
  | \bwe\ (have\ chosen|choose)\ to\b
  | \bshould\ be\ approached\ (cautiously|with\ caution)\b
  | \bbounded\ negative\b
  | \bbounded\ and\ correctable\b
  | \bsilently\ harmoni[sz]\w*\b
  | \bis\ offered\ as\ (source-grounded|documented)\b
  | \b(is|are)\ documented\ (allegorical\ |typological\ |later\ |patristic\ )?
        reception,\ not\b
  | \bnot\ a\ replacement\ for\ the\b
  | \b(does\ not\ prove|without\ claiming|not\ proof\ of|not\ evidence\ for)\b
        [^.;:]{0,60}?\b(compiler|compilers|redactor|compilation)\b
""", re.IGNORECASE | re.VERBOSE)

TRADITION_DISTANCE = re.compile(r"""
    \blater\ christians\ (believed|thought|held|came\ to)\b
  | \ba\ devotional\ reading\ might\b
  | \bthe\ fathers\ understandably\b
  | \balthough\ (later\ )?tradition\ (claimed|held|maintained|believed)\b
  | \bfrom\ a\ modern\ perspective\b
  | \bthe\ church\ came\ to\ read\b
""", re.IGNORECASE | re.VERBOSE)


def phrase_list_matches(text: str) -> list[str]:
    """Sentences the illustrative phrase list matches.

    A match is evidence about the sentence's grammar, not a verdict: whether
    a matched sentence is a defect depends on the section it stands in, which
    this function cannot see. See the header comment above.
    """
    return [s for s in sentences(text)
            if SELF_NARRATION.search(s) or TRADITION_DISTANCE.search(s)]


# --- Negative controls: real prose from the generated corpus, plus the exact
# --- forms the brief names. Every one of these must be caught.

METHOD_NARRATION_DEFECTS = [
    # src/claude/.../49-ninth-after-pentecost/sections/30-commentary.tex:239
    "The analysis above rests on the printed Latin, its punctuation, and "
    "its juxtaposition, and is offered as source-grounded synthesis rather "
    "than documented reception.",
    # .../53-thirteenth-after-pentecost/sections/30-commentary.tex:314
    "This guide reports that as the Glossa's apparatus and not as its own "
    "finding, because no Psalterium Romanum witness was collated for this "
    "leaf.",
    # .../49-ninth-after-pentecost/sections/30-commentary.tex:293
    "This guide reports the difference and adopts no harmonisation.",
    # .../48-eighth-after-pentecost/sections/30-commentary.tex:612
    "This guide reports the divergence and does not adjudicate the Greek "
    "text.",
    # .../51-eleventh-after-pentecost/sections/30-commentary.tex:210
    "This guide does not assert a line of descent from Cassiodorus's "
    "psalter to the Introit.",
    # .../49-ninth-after-pentecost/sections/30-commentary.tex:119
    "This guide does not supply a rendering of its own.",
    # .../53-thirteenth-after-pentecost/sections/30-commentary.tex:1500
    "A bounded negative. The prayer is not in the Verona collection.",
    # .../52-twelfth-after-pentecost/sections/30-commentary.tex:152
    "Augustine, for all nine sections of his exposition, never mentions the "
    "other psalm - a bounded negative verified against the full Latin of "
    "both expositions.",
    # src/gpt/.../54-fourteenth-after-pentecost/sections/30-commentary.tex:40
    "The difference from Augustine is retained instead of being silently "
    "harmonized.",
    # src/gpt/.../43-third-after-pentecost/main.tex:258
    "Neither witness is expanded or silently harmonized.",
    # src/gpt/.../50-tenth-after-pentecost/sections/
    #     33-comparative-reception.tex:6
    "The comparison therefore asks three questions at every stage: what the "
    "source text says in its own literary setting, what a later reader "
    "adds, and what the 1962 sequence permits.",
    # .../48-eighth-after-pentecost/sections/30-commentary.tex:685
    "It is worth stating plainly what this section has not resolved, "
    "because a guide that manufactured a consensus here would misrepresent "
    "its sources.",
    # src/claude/.../53-thirteenth-after-pentecost/sections/
    #     10-date-location.tex:16, the closing clause of the Ps. 73 dossier.
    #     Page 2 is reader-facing prose, and until this repair criterion 12
    #     did not reach it, so this defect had no criterion able to see it.
    "Witnesses since antiquity have resolved the tension as prophecy or as a "
    "later Asaphite's voice; this sheet reports it unresolved.",
    # The forms the governing brief names directly.
    "It is important to distinguish the literal sense from the allegorical "
    "here.",
    "The guiding principle here is restraint.",
    "Methodologically, this section proceeds from context to reception.",
    "We have chosen to emphasize the Collect.",
    "This interpretation should be approached cautiously because the "
    "evidence is thin.",
]

SECULAR_FRAMING_DEFECTS = [
    # src/gpt/.../45-fifth-after-pentecost/main.tex:218
    "This is documented allegorical reception, not a replacement for the "
    "royal psalm's literal and historical horizon.",
    # src/gpt/.../54-.../sections/35-source-grounded-synthesis.tex:29
    "This theological movement does not prove a compiler's symbolic plan.",
    # src/gpt/.../54-.../sections/synthesis/20-integrated-commentary.tex:106
    "This relation joins desire, command, sacrifice, reception, and hope "
    "without claiming a recoverable compiler's intention.",
    # src/gpt/.../50-.../sections/synthesis/10-themes-and-movement.tex:91
    "His correspondence is documented later reception, not proof of Roman "
    "compiler intent.",
    # The forms the governing brief names directly.
    "Later Christians believed the psalm spoke of the Church.",
    "A devotional reading might see Christ in the Samaritan.",
    "The Fathers understandably interpreted the verse typologically.",
    "Although tradition claimed Mosaic authorship, the text is later.",
    "From a modern perspective this is problematic.",
    "The Church came to read this as a figure of baptism.",
]

# --- Positive controls. Category (a)-(d) of the governing brief's "do not
# --- erase legitimate historical evidence", every sentence taken from the
# --- generated corpus. A rule that flags any of these has destroyed the
# --- qualifications the profile requires, and is worse than the fault.

CLAIM_LOCAL_QUALIFICATIONS = [                                     # (a)
    "Augustine's lemma is not the chant's.",
    "An eleventh-century anonymous treatise transmitted among Augustine's "
    "works and printed under Auctor incertus.",
    "No public-domain English exists at this sermon - the standard modern "
    "translation is in copyright - so it is quoted here in Latin only.",
    "Cyril of Alexandria's surviving sermon on this pericope reads it "
    "morally and never identifies the Samaritan with Christ.",
    "The forty Homiliae in Evangelia contain no homily on Lk. 10:23-37.",
    "The Douay renders the Clementine, 'and judge me in thy strength,' so "
    "it cannot be quoted for the missal's verb.",
]

HISTORICAL_CRITICAL_DATING = [                                     # (b)
    "Ancient tradition identifies Luke, the Antiochene physician and "
    "Pauline companion; modern Catholic orientation commonly places the "
    "Gospel's final composition about AD 80-90, outside Palestine, for a "
    "substantially Gentile Christian audience.",
    "Pauline authorship is traditional and the mainstream modern judgment "
    "alike. Who the Galatians were is not settled: the NABRE holds them "
    "most likely among the descendants of Celts.",
    "Ancient tradition identifies St. Matthew, former tax collector and "
    "apostle. Modern scholarship usually dates the canonical Greek Gospel "
    "after AD 70, often c. 80-90, with Antioch in Syria plausible but "
    "unproved.",
    "Catholic tradition receives Moses as the Pentateuch's principal "
    "inspired author. The 1906 Pontifical Biblical Commission allows "
    "pre-Mosaic sources, secretarial aid, inspired additions, and later "
    "linguistic updating while maintaining substantial Mosaic authenticity.",
    # src/claude/.../53-thirteenth-after-pentecost/sections/
    #     10-date-location.tex:16, with its closing clause removed. The
    #     dossier ends `this sheet reports it unresolved`, whose subject is
    #     the sheet's own conduct, so by this commit's own discriminator that
    #     clause is the defect and cannot be a positive control. The fact and
    #     the witnesses who differ say the same thing declaratively, and the
    #     discarded clause is now a negative control below.
    "Asaph is David's chief musician, so the bare title suggests a "
    "Davidic-era horizon - yet the psalm mourns a sanctuary already "
    "destroyed, and witnesses since antiquity have resolved the tension as "
    "prophecy or as a later Asaphite's voice.",
]

DOCUMENTED_DISAGREEMENT = [                                        # (c)
    "Whether the steward's act is left uncensured (Ambrose) or expressly "
    "excluded from imitation (Augustine) is a real disagreement between two "
    "Doctors.",
    "Jerome has nothing on vv. 1, 19, 20, 22 or 23.",
    "Theodoret answers Moses, explicitly: the law was laid down with angels "
    "serving and Moses ministering at its enactment, for him he called "
    "mediator.",
    "Augustine reads the psalm as the cry of the pilgrim Church, while "
    "Cassiodorus refers it to the Babylonian destruction.",
]

CULTURAL_AFTERLIFE = [                                             # (d)
    "A congregation's sung plea that God arise and defend his own cause "
    "becomes the juridical opening of an excommunication process, a human "
    "tribunal speaking the psalm in God's stead, and its target answers.",
    "The plea becomes a processional ensign carried at autos-da-fe, the "
    "sword of the sentence on one side of the cross and the olive of "
    "reconciliation on the other.",
    "Joyce lets the manna of every taste run as liturgical soundtrack to "
    "profane appetite.",
    "The pericope becomes an experimental protocol, and the experiment "
    "re-enacts it.",
    "Keynes proposes an economic forecast and strategy, not an exegesis of "
    "the lilies.",
    "The Gospel image becomes both a name for post-scarcity leisure and an "
    "ironic measure of an economic order still serving what it knows is not "
    "the final good.",
]

REQUIRED_NOTICES = [
    # Mandated by the profile: the exploratory notice and the strongest limit.
    "These proposals are exploratory editorial or AI proposals, not sourced "
    "historical intent or attributed teaching.",
    "Strongest limit: no patristic witness connects the two verses directly.",
    # The declarative ideal the governing brief itself writes out.
    "The Introit establishes exile as the formulary's opening condition.",
    "The Collect turns that condition into petition.",
    "The Fathers read the manna as a figure of the Eucharist.",
    # Reconnaissance flagged this as a false positive for a naive probe on
    # "the tradition heard as": the sentence reports what a body of witnesses
    # did, and its main subject is the returning leper, not the guide.
    "The one who comes back is named by a word the tradition heard as "
    "keeper.",
]

TERMINAL_APPARATUS = [                                             # (e)
    # src/claude/.../52-twelfth-after-pentecost/sections/90-scope.tex:104.
    # That file has exactly one heading, `\section*{Appendix: Scope and
    # Qualifications}` at line 2, so line 104 is inside the appendix that
    # editorial.md, the profile, criterion 12 and the profile-conformance
    # lane all exempt by name. It was first labelled a body defect; it is
    # the appendix doing its job, and bounding the negatives is required of
    # it. (The gpt tree's file of the same name is 38 lines and has no line
    # 104; the sentence is the claude tree's.)
    "No exhaustive search of Syriac originals, chant manuscripts, "
    "untranslated homiliaries, subscription databases or current specialist "
    "monographs is claimed, and none of these negatives is offered as a "
    "claim about literature outside the corpora named.",
]

LEGITIMATE = (CLAIM_LOCAL_QUALIFICATIONS + HISTORICAL_CRITICAL_DATING
              + DOCUMENTED_DISAGREEMENT + CULTURAL_AFTERLIFE
              + REQUIRED_NOTICES + TERMINAL_APPARATUS)

# --- The section-blindness demonstration. Real corpus sentences that the
# --- phrase list matches and that are legitimate where they stand, because
# --- they stand in a section the rules exempt by name. Grammar cannot tell
# --- these from the identical sentence in `Detailed Commentary`, where each
# --- would be a defect, so these are the standing proof that the list
# --- classifies labelled examples and does not detect defects in a corpus.
SECTION_EXEMPT_BUT_MATCHING = [
    # src/claude/.../51-eleventh-after-pentecost/sections/90-scope.tex,
    # inside `Appendix: Scope and Qualifications`. Declining to settle
    # authorship is precisely what a scope appendix is for.
    "This guide does not settle the authorship or date of any psalm, the "
    "date or place of Mark's composition, the compilation history of "
    "Proverbs, or the year of the events Mark narrates.",
    # src/claude/.../49-ninth-after-pentecost/sections/90-scope.tex, same
    # section.
    "This guide does not settle the year of the Passion, the date or place "
    "of Luke's or John's composition, or the historical authorship of any "
    "psalm.",
    # src/claude/.../51-eleventh-after-pentecost/sections/99-references.tex,
    # inside `References`, where a source-local note on what a search
    # established is exactly the right home for the audit's phrasing.
    "Also searched entire for the Collect, with the bounded negative result "
    "recorded in research/scope.md.",
    # src/claude/.../52-twelfth-after-pentecost/sections/99-references.tex,
    # same section.
    "De principiis I.1.2, with the bounded negative at Book IV;",
]


# ---------------------------------------------------------------------------
# Proof 12's matcher: no stage may direct method into the body
# ---------------------------------------------------------------------------

BODY_TARGET = re.compile(
    r"(reader-facing (prose|body|text)|\bin the body\b|\bin the prose\b"
    r"|\bthe commentary\b|\bin `?main\.tex`?|Detailed Commentary"
    r"|Themes and Movement|\bon page 1\b|\bon page 2\b)", re.IGNORECASE)
METHOD_TOPIC = re.compile(
    r"(methodolog\w+|\bmethod\b|editorial (principle|policy|choice|decision"
    r"|process|reasoning)|guiding principle|research process"
    r"|interpretive policy|why caution|the caution|search bounds"
    r"|workflow boundar\w+)", re.IGNORECASE)
DIRECTIVE = re.compile(
    r"\b(explain|narrate|describe|state|set out|record|justify|include|add"
    r"|give|report)\w*\b", re.IGNORECASE)
# A sentence that sends the material somewhere else is not directing it here.
ELSEWHERE = re.compile(
    r"(research/scope\.md|`notes`|audit record|terminal (apparatus|appendix)"
    r"|Scope and Qualifications|belongs? in|out of scope|not for the reader"
    r"|References)", re.IGNORECASE)
FORBIDS = re.compile(
    r"(\bdo(es)? not\b|\bnever\b|\bno\b|\bnor\b|\bremove\b|\bavoid\b"
    r"|\bmust not\b|\bmay not\b|\bwithout\b|\bunless\b|\bforbid\w*\b"
    r"|\brather than\b|\binstead of\b|\bout of\b)", re.IGNORECASE)


def method_in_body_directives(text: str) -> list[str]:
    """Sentences telling a worker to narrate method in reader-facing prose.

    A question is excluded. An evaluator criterion asks whether the prose
    narrates its method, in the same vocabulary a directive to narrate it
    would use, and the two are told apart by mood rather than by wording.
    """
    found = []
    for sentence in sentences(text):
        if sentence.rstrip().endswith("?"):
            continue
        if not (BODY_TARGET.search(sentence) and METHOD_TOPIC.search(sentence)
                and DIRECTIVE.search(sentence)):
            continue
        if ELSEWHERE.search(sentence) or FORBIDS.search(sentence):
            continue
        found.append(sentence)
    return found


METHOD_IN_BODY_EVASIONS = [
    "Explain in the detailed commentary the editorial principle that "
    "governed which witnesses were included.",
    "State in the body why caution is necessary before presenting the "
    "typology.",
    "In reader-facing prose, narrate the research process that produced the "
    "reception matrix.",
    "The commentary should describe the methodology that governs this "
    "treatment.",
    "On page 2, set out the guiding principle behind the chronology.",
]


# ---------------------------------------------------------------------------
# 1-2, 11. The author packet carries both rules
# ---------------------------------------------------------------------------

class PacketCase(RoutingCase):
    """Compiles the real packets a worker is handed."""

    def compiled_packets(self) -> dict[str, str]:
        run_id, _ = self.advance_to("research")
        workflow = self.engine.load_workflow("proper")
        state = self.engine.load_state(run_id)
        packets = {}
        for stage in workflow["stages"]:
            compiled = self.engine._compile_stage_packets(
                workflow, stage, state, self.engine.run_dir(run_id), [])
            packets[stage["id"]] = compiled["bytes"].decode("utf-8")
            for lane in compiled.get("lanes", []):
                packets[f"{stage['id']}/{lane['lane']}"] = \
                    lane["bytes"].decode("utf-8")
        return packets


class AuthorPacketTests(PacketCase):
    """Proof 1, 2 and 11, on the deterministic bytes."""

    def setUp(self):
        super().setUp()
        self.packets = self.compiled_packets()
        self.author = flat(self.packets["author-proper"])

    def test_the_author_packet_states_the_declarative_rule(self):
        """Proof 1."""
        self.assertIn("State the finding, not the process that produced it",
                      self.author)
        self.assertIn("Lead with the claim", self.author)
        self.assertRegex(self.author, re.compile(
            r"remove any sentence whose main work is to justify that an "
            r"interpretation may be offered rather than to offer it",
            re.IGNORECASE))
        for banned in ("It is important to distinguish",
                       "The guiding principle here",
                       "Methodologically",
                       "We have chosen to emphasize",
                       "should be approached cautiously"):
            with self.subTest(form=banned):
                self.assertIn(banned.lower(), self.author.lower(),
                              "the author is shown the form to avoid")

    def test_the_author_packet_states_the_interpretive_voice_rule(self):
        """Proof 2."""
        self.assertIn("Speak from within the tradition", self.author)
        self.assertIn("Catholic", self.packets["author-proper"])
        self.assertRegex(self.author, re.compile(
            r"theological grammar they use, attributed to the witness who "
            r"taught them", re.IGNORECASE))
        for preferred in ("The Fathers\nread", "Augustine identifies",
                          "the liturgy presents", "the Church receives"):
            with self.subTest(form=preferred):
                self.assertIn(flat(preferred), self.author)
        for distanced in ("later Christians believed",
                          "a devotional reading might see",
                          "the Fathers understandably interpreted",
                          "although tradition claimed",
                          "the Church came to read this as"):
            with self.subTest(form=distanced):
                self.assertIn(distanced.lower(), self.author.lower())

    def test_the_author_packet_names_the_profile_that_owns_the_deltas(self):
        """The fragment never named its own profile before this change."""
        self.assertIn("guidance/liturgy/roman-1962-propers.md", self.author)
        self.assertIn("guidance/editorial.md", self.author)

    def test_method_is_directed_away_from_the_body(self):
        """Proof 11."""
        self.assertRegex(self.author, re.compile(
            r"Method, search bounds, corpora checked, evidence classes, and "
            r"negative results already have their homes", re.IGNORECASE))
        self.assertIn("Appendix:\nScope and Qualifications".replace("\n", " "),
                      self.author)
        self.assertIn("The body is not one of them.", self.author)

    def test_the_declarative_rule_is_not_a_licence_to_delete(self):
        """Proofs 7-9, in the author's own bytes."""
        self.assertIn("Neither rule suppresses evidence", self.author)
        self.assertIn("modern critical horizon belongs in the page-2 "
                      "explanatory row", self.author)
        self.assertIn("genuine disagreement between sources is stated and "
                      "attributed", self.author)
        self.assertIn("Notable and Quotable` are the point of that gallery",
                      self.author)

    def test_the_grammatical_discriminator_reaches_the_worker(self):
        """The rule is teachable only if the test for it is in the packet."""
        self.assertIn("look at its grammatical subject", self.author)
        self.assertIn("a source, a text, a witness, or a fact", self.author)
        self.assertIn("the guide, the reading, or an evidence class",
                      self.author)


# ---------------------------------------------------------------------------
# 3. Content revision repairs both defects, and deletes nothing
# ---------------------------------------------------------------------------

class ContentRevisionTests(PacketCase):
    """Proof 3."""

    def setUp(self):
        super().setUp()
        self.revision = flat(self.compiled_packets()["content-revision"])

    def test_revision_can_repair_both_defects(self):
        for defect in ("Excessive methodological narration",
                       "editorial self-justification",
                       "secular skeptical framing",
                       "unnecessary distancing from patristic interpretation",
                       "modern-critical framing that has taken over the "
                       "theological reading"):
            with self.subTest(defect=defect):
                self.assertIn(defect, self.revision)
        self.assertIn("all editorial defects", self.revision)

    def test_revision_repairs_by_rewriting_and_never_by_deleting(self):
        self.assertIn(
            "repaired by rewriting the sentence, never by deleting what the "
            "sentence was about", self.revision)
        for preserved in ("the claim-local qualification that keeps a claim "
                          "accurate",
                          "the required modern chronology",
                          "the documented disagreement",
                          "the documented cultural afterlife"):
            with self.subTest(preserved=preserved):
                self.assertIn(preserved, self.revision)

    def test_a_finding_that_would_cost_evidence_is_blocked(self):
        self.assertIn(
            "If the only way to satisfy a finding is to drop evidence, it is "
            "a research finding wrongly routed here", self.revision)
        self.assertIn("return `BLOCKED`", self.revision)

    def test_revision_inherits_the_house_voice_from_the_author_fragment(self):
        """The packet appends `author-proper.md`, so both rules are present."""
        self.assertIn("State the finding, not the process that produced it",
                      self.revision)
        self.assertIn("Speak from within the tradition", self.revision)


# ---------------------------------------------------------------------------
# 4. Content evaluation checks both defects, and the criterion that caused one
# ---------------------------------------------------------------------------

class ContentEvaluationTests(PacketCase):
    """Proof 4, and the root cause the criterion itself was."""

    def setUp(self):
        super().setUp()
        self.packets = self.compiled_packets()
        self.shared = flat(self.packets["content-evaluation"])

    def test_both_defects_are_numbered_criteria(self):
        """Proof 4."""
        self.assertIn("11. **Interpretive voice**",
                      self.packets["content-evaluation"])
        self.assertIn("12. **Declarative discipline**",
                      self.packets["content-evaluation"])
        self.assertIn("has secular skepticism become the narrator's default "
                      "stance", self.shared)
        self.assertIn("how the editors reasoned", self.shared)
        self.assertIn("what methodology governs the section", self.shared)

    def test_a_recurring_habit_is_the_defect_not_a_local_qualification(self):
        self.assertIn("A few necessary claim-local qualifications are not a "
                      "defect; the defect is a recurring rhetorical habit",
                      self.shared)

    def test_the_qualification_sections_are_exempt(self):
        """The appendix is qualification by design; the body is not.

        The mandated limit field is exempted by role rather than by label,
        because the corpus writes it as `Strongest limit`, as `Limit`, and
        as inline bold prose depending on the leaf.
        """
        for exempt in ("Appendix: Scope and Qualifications", "References",
                       "the exploratory notice", "the novelty "
                       "classification", "controlling-limit field"):
            with self.subTest(section=exempt):
                self.assertIn(exempt, self.shared)
        self.assertIn("Out of scope, as qualification by design", self.shared)

    def test_criterion_twelve_reaches_every_reader_facing_section(self):
        """The holes the review found: page 2, the gallery, and the body of
        Interpretive Possibilities were outside every content criterion."""
        for section in ("Scriptural Date and Location",
                        "The Propers: Notable and Quotable",
                        "the proposals of `The Propers: Interpretive "
                        "Possibilities`"):
            with self.subTest(section=section):
                self.assertIn(section, self.shared)
        self.assertIn("Every reader-facing section is in scope", self.shared)

    def test_criterion_twelve_reaches_a_defect_that_is_not_a_sentence(self):
        """The `{Control retained}` column and the `Rights and limit` block
        are the fault written as a column and as a field."""
        self.assertIn("a run-in label, a standing per-entry field, or a "
                      "table column", self.shared)
        self.assertIn("`Control` or `Rights and limit` block", self.shared)

    def test_criterion_twelve_spares_the_content_those_sections_must_carry(
            self):
        """Widening scope must not make required material a finding."""
        self.assertIn("and none of those is ever a finding", self.shared)
        self.assertIn("the modern critical horizon", self.shared)
        self.assertIn("later user or work, exact locus, and turn in meaning",
                      self.shared)

    def test_criterion_six_no_longer_rewards_the_defect(self):
        """The root cause: an evaluator could only verify non-silence if the
        prose announced it, so the criterion paid for the announcement."""
        self.assertNotIn("preserved rather than silently harmonized",
                         self.shared)
        self.assertIn("is the disagreement present in the prose and "
                      "attributed to the sources that hold it", self.shared)
        self.assertIn("Never judge whether the guide announces that it "
                      "preserved anything", self.shared)
        self.assertIn("it is a criterion 12 defect", self.shared)

    def test_the_lane_echo_of_criterion_six_is_fixed_too(self):
        """The same sentence lived in the lane that owns the criterion."""
        lane = flat(self.packets[f"content-evaluation/{VOICE_LANE}"])
        self.assertNotIn("preserved rather than silently harmonized into one "
                         "settled reading", lane)
        self.assertIn("Judge what the text contains, and never whether the "
                      "guide announces that it preserved anything", lane)

    def test_modern_criticism_is_not_the_governing_frame(self):
        """Proof 10."""
        self.assertIn("modern criticism treated as the authority that "
                      "validates or invalidates a theological reading",
                      self.shared)
        author = flat(self.packets["author-proper"])
        self.assertIn("Modern criticism is not the authority that validates "
                      "or invalidates a theological reading", author)

    def test_the_evaluator_may_not_flag_the_required_evidence(self):
        """Proofs 7-9, in the evaluator's own bytes."""
        for permitted in ("Accurate modern dating", "a genuine authorship "
                          "dispute", "factual source criticism",
                          "historically documented disagreement",
                          "the secular afterlives"):
            with self.subTest(permitted=permitted):
                self.assertIn(permitted, self.shared)
        self.assertIn("a finding that would delete one is wrong",
                      self.shared.lower())


# ---------------------------------------------------------------------------
# 5-6. Repair routing, deterministically
# ---------------------------------------------------------------------------

class VoiceRepairRoutingTests(RoutingCase):
    """Proofs 5 and 6, driven through the real engine."""

    def test_the_fragments_assign_voice_defects_to_authoring(self):
        """Proof 5, in the guidance the evaluator is given."""
        text = flat((FRAGMENTS / "propers" / "content-evaluation.md")
                    .read_text(encoding="utf-8"))
        self.assertIn("A criterion 11 or 12 finding is `authoring`", text)
        self.assertIn("rewriting the prose is the whole repair", text)

    def test_the_tie_breaker_does_not_swallow_a_voice_finding(self):
        """Without this the ambiguity rule sends every voice finding through
        a research or brief re-entry, which is the expensive wrong loop.

        The tie-breaker was "prefer `research`" when this was written.
        Version 10's third owner replaced it with an explicit earliest-owner
        ordering, which can still swallow a voice finding, so the carve-out
        is asserted against the ordering that exists rather than the wording
        that used to express it.
        """
        text = flat((FRAGMENTS / "propers" / "content-evaluation.md")
                    .read_text(encoding="utf-8"))
        self.assertIn("name the earliest owner whose correction is actually "
                      "necessary", text)
        self.assertIn("That tie-breaker does not reach criteria 11 and 12",
                      text)
        self.assertIn("`brief` is not a third answer for those two criteria",
                      text)

    def test_a_voice_finding_routes_to_content_revision(self):
        """Proof 5, through the engine that actually decides."""
        route = self.route_for({
            VOICE_LANE: [blocking("CON-REC-011", AUTHORING,
                                  "secular skeptical framing governs the "
                                  "commentary on the Gradual")],
            DECLARATIVE_LANE: [blocking("CON-PRO-012", AUTHORING,
                                        "the section narrates its method "
                                        "instead of stating the finding")],
        })
        self.assertEqual(route["next"], "content-revision")
        self.assertEqual(route["transition"],
                         {"from": "content-evaluation",
                          "to": "content-revision",
                          "disposition": CHANGES_REQUIRED})
        forwarded = self.forwarded(route["packet"])
        self.assertEqual(sorted(f["id"] for f in forwarded),
                         ["CON-PRO-012", "CON-REC-011"])

    def test_a_missing_catholic_foundation_routes_to_research(self):
        """Proof 6: the one voice defect the author cannot repair."""
        text = flat((FRAGMENTS / "propers" / "content-evaluation.md")
                    .read_text(encoding="utf-8"))
        self.assertIn("a passage for which the evidence supplies no Catholic "
                      "reception at all", text)
        self.assertIn("the finding is `research`", text)

        route = self.route_for({
            VOICE_LANE: [blocking("CON-REC-011", RESEARCH,
                                  "the brief carries no Catholic reception "
                                  "for the Offertory at all")],
        })
        self.assertEqual(route["next"], RESEARCH)
        self.assertEqual(route["transition"]["to"], RESEARCH)

    def test_the_owning_lane_states_the_discriminator_itself(self):
        """A lane worker never reads the other lane's fragment."""
        lane = flat((FRAGMENTS / "propers" / "lanes"
                     / f"content-{VOICE_LANE}.md").read_text(encoding="utf-8"))
        self.assertIn("the finding is `research`; otherwise it is `authoring`",
                      lane)
        other = flat((FRAGMENTS / "propers" / "lanes"
                      / f"content-{DECLARATIVE_LANE}.md")
                     .read_text(encoding="utf-8"))
        self.assertIn("A criterion 12 finding is `authoring`", other)


# ---------------------------------------------------------------------------
# The labelled examples are labelled correctly, and the list knows its limits
# ---------------------------------------------------------------------------

class IllustrativeExampleTests(unittest.TestCase):
    """The phrase list classifies the labelled examples correctly.

    This is a claim about the examples, not about the corpus. What must not
    happen is a required qualification being labelled a defect, because a
    rule that deleted a modern dating, a documented disagreement, or the
    Joyce and Keynes afterlives would be worse than the fault it replaced.
    """

    def test_the_rule_catches_methodological_narration(self):
        for text in METHOD_NARRATION_DEFECTS:
            with self.subTest(defect=text[:60]):
                self.assertTrue(phrase_list_matches(text),
                                f"the rule lets this through: {text!r}")

    def test_the_rule_catches_secular_framing(self):
        for text in SECULAR_FRAMING_DEFECTS:
            with self.subTest(defect=text[:60]):
                self.assertTrue(phrase_list_matches(text),
                                f"the rule lets this through: {text!r}")

    def test_claim_local_qualification_survives(self):
        """Proof 7's neighbour: the profile requires these beside the claim."""
        for text in CLAIM_LOCAL_QUALIFICATIONS:
            with self.subTest(allowed=text[:60]):
                self.assertEqual(
                    phrase_list_matches(text), [],
                    f"a required claim-local qualification is flagged: "
                    f"{text!r}")

    def test_historical_critical_dating_survives(self):
        """Proof 7: the profile requires the modern horizon on page 2."""
        for text in HISTORICAL_CRITICAL_DATING:
            with self.subTest(allowed=text[:60]):
                self.assertEqual(
                    phrase_list_matches(text), [],
                    f"a required modern dating is flagged: {text!r}")

    def test_documented_disagreement_survives(self):
        """Proof 8."""
        for text in DOCUMENTED_DISAGREEMENT:
            with self.subTest(allowed=text[:60]):
                self.assertEqual(
                    phrase_list_matches(text), [],
                    f"a documented disagreement is flagged: {text!r}")

    def test_cultural_afterlife_survives(self):
        """Proof 9: Joyce, Keynes, the Inquisition standard, Leo X's bull."""
        for text in CULTURAL_AFTERLIFE:
            with self.subTest(allowed=text[:60]):
                self.assertEqual(
                    phrase_list_matches(text), [],
                    f"a documented cultural afterlife is flagged: {text!r}")

    def test_the_required_notices_survive(self):
        for text in REQUIRED_NOTICES:
            with self.subTest(allowed=text[:60]):
                self.assertEqual(
                    phrase_list_matches(text), [],
                    f"a profile-mandated notice is flagged: {text!r}")

    def test_the_terminal_apparatus_survives(self):
        """The appendix and References are qualification by design."""
        for text in TERMINAL_APPARATUS:
            with self.subTest(allowed=text[:60]):
                self.assertEqual(
                    phrase_list_matches(text), [],
                    f"the terminal apparatus is flagged: {text!r}")

    def test_every_labelled_example_is_classified_correctly(self):
        """Both control sets together: every labelled defect matched, no
        labelled legitimate sentence matched."""
        defects = METHOD_NARRATION_DEFECTS + SECULAR_FRAMING_DEFECTS
        self.assertEqual(
            [t for t in defects if not phrase_list_matches(t)], [])
        self.assertEqual(
            [t for t in LEGITIMATE if phrase_list_matches(t)], [])
        self.assertGreaterEqual(len(defects), 28)
        self.assertGreaterEqual(len(LEGITIMATE), 21)

    def test_the_phrase_list_is_section_blind_and_says_so(self):
        """The list matches legitimate prose in the exempt sections.

        This test asserts the limitation rather than papering over it. Each
        sentence below is required of the section it stands in and would be
        a defect in the substantive body, so grammar cannot decide it and
        the phrase list is not the enforcement. Criteria 11 and 12 are, read
        by an evaluator that can see the section.
        """
        for text in SECTION_EXEMPT_BUT_MATCHING:
            with self.subTest(exempt=text[:60]):
                self.assertTrue(
                    phrase_list_matches(text),
                    f"this example no longer demonstrates section-blindness, "
                    f"so it should be retired or moved: {text!r}")

    def test_the_module_does_not_claim_the_list_detects_defects(self):
        """The suite must not narrate a discipline it does not have."""
        source = Path(__file__).read_text(encoding="utf-8")
        self.assertIn("It is not a detector over", source)
        self.assertIn("a sentence matcher cannot see a column", source)
        self.assertIn("illustrative", __doc__)


# ---------------------------------------------------------------------------
# 12. No stage tells the author to narrate method in the body
# ---------------------------------------------------------------------------

class NoMethodInTheBodyTests(PacketCase):
    """Proof 12, over every fragment and every compiled packet.

    The sweeps below find nothing, and a sweep that finds nothing proves
    nothing until it is shown to be capable of finding something. Exactly
    one fragment sentence reaches the BODY_TARGET / METHOD_TOPIC / DIRECTIVE
    gate — criterion 12's own question — and the question rule excludes it.
    The inoculation tests therefore spike each fragment and each packet with
    a directive that must be caught, so a green sweep is a fact about the
    fragments rather than about the gate.
    """

    def test_the_rule_catches_the_directive_it_forbids(self):
        for text in METHOD_IN_BODY_EVASIONS:
            with self.subTest(evasion=text[:60]):
                self.assertTrue(method_in_body_directives(text),
                                f"the rule lets this through: {text!r}")

    def reaches_the_gate(self, sentence: str) -> bool:
        return bool(BODY_TARGET.search(sentence)
                    and METHOD_TOPIC.search(sentence)
                    and DIRECTIVE.search(sentence))

    def test_the_rule_permits_a_directive_that_sends_method_away(self):
        """Each case must reach the gate before a guard can clear it.

        The gate is asserted first because a case that never reaches it
        exercises no guard and proves nothing about one. ELSEWHERE and
        FORBIDS are the guards; the question rule is checked separately.
        """
        cleared_by_elsewhere = [
            "State the editorial reasoning behind each inclusion in "
            "research/scope.md, and give the detailed commentary the "
            "conclusion it reached.",
            "Record the search bounds that govern the commentary in the "
            "terminal appendix.",
        ]
        cleared_by_forbids = [
            "Never explain the guiding principle in the detailed commentary.",
            "Do not narrate the research process in reader-facing prose.",
        ]
        for text, guard in ([(x, ELSEWHERE) for x in cleared_by_elsewhere]
                            + [(x, FORBIDS) for x in cleared_by_forbids]):
            with self.subTest(allowed=text[:60]):
                self.assertTrue(
                    any(self.reaches_the_gate(s) for s in sentences(text)),
                    f"this case never reaches the gate, so it tests no "
                    f"guard: {text!r}")
                self.assertTrue(
                    any(guard.search(s) for s in sentences(text)),
                    f"the intended guard does not fire on {text!r}")
                self.assertEqual(method_in_body_directives(text), [],
                                 f"the rule wrongly flags: {text!r}")

    def test_a_criterion_asking_the_question_is_not_a_directive(self):
        """The one fragment sentence that reaches the gate is criterion 12's
        own question, and mood is what tells it from an instruction."""
        question = ("Does the reader-facing prose state its findings, or "
                    "does it repeatedly narrate what methodology governs "
                    "the section?")
        self.assertTrue(self.reaches_the_gate(question))
        self.assertEqual(method_in_body_directives(question), [])

    def test_no_fragment_directs_method_into_the_body(self):
        for name, text in propers_fragments().items():
            with self.subTest(fragment=name):
                self.assertEqual(
                    method_in_body_directives(text), [],
                    f"{name} tells a worker to narrate method in "
                    f"reader-facing prose")

    def test_no_emitted_packet_directs_method_into_the_body(self):
        for stage, text in self.compiled_packets().items():
            with self.subTest(stage=stage):
                self.assertEqual(
                    method_in_body_directives(text), [],
                    f"the {stage} packet directs method into the body")

    def test_the_fragment_sweep_would_catch_a_directive_if_one_appeared(self):
        """Inoculation: the green sweep above is about the fragments."""
        spike = ("\n\nThe fragment ends here. Explain in the detailed "
                 "commentary the editorial principle that governed which "
                 "witnesses were included.\n")
        for name, text in propers_fragments().items():
            with self.subTest(fragment=name):
                found = method_in_body_directives(text + spike)
                self.assertTrue(
                    found,
                    f"the sweep over {name} cannot see a directive that is "
                    f"actually there, so its silence proves nothing")
                self.assertIn("editorial principle that governed",
                              " ".join(found))

    def test_the_packet_sweep_would_catch_a_directive_if_one_appeared(self):
        """Inoculation, for the compiled packets."""
        spike = ("\n\nThe packet ends here. In reader-facing prose, "
                 "narrate the research process that produced the reception "
                 "matrix.\n")
        for stage, text in self.compiled_packets().items():
            with self.subTest(stage=stage):
                found = method_in_body_directives(text + spike)
                self.assertTrue(
                    found,
                    f"the sweep over the {stage} packet cannot see a "
                    f"directive that is actually there")
                self.assertIn("narrate the research process",
                              " ".join(found))


# ---------------------------------------------------------------------------
# The causes, not only the symptoms
# ---------------------------------------------------------------------------

class RootCauseTests(unittest.TestCase):
    """Five workflow instructions produced the prose they were blamed for."""

    def fragment(self, *parts: str) -> str:
        return flat((FRAGMENTS.joinpath("propers", *parts))
                    .read_text(encoding="utf-8"))

    def test_bounded_and_correctable_is_named_as_audit_language(self):
        """R3: the phrase was correct for `notes` and leaked into the PDF.

        "a bounded negative" reached reader-facing prose in seven places
        across three leaves, because the research fragment asked for the
        quality without ever naming where the wording belonged.
        """
        text = self.fragment("research.md")
        self.assertIn("keep every negative result bounded and correctable",
                      text)
        self.assertIn("belongs to the `notes` field of the findings you "
                      "return, which is an audit record", text)
        self.assertIn('A guide that prints "a bounded negative" has put the '
                      "audit in the body", text)

    def test_the_limiting_qualification_is_the_audits_not_the_gallerys(self):
        """R4: both providers printed it as a reader-facing block."""
        text = self.fragment("lanes", "research-cultural-afterlife.md")
        self.assertIn("That list is the audit's, and the audit is not the "
                      "gallery", text)
        self.assertIn("do not become a rights-and-limit block printed under "
                      "each entry", text)

    def test_a_forbidden_claim_is_satisfied_by_silence(self):
        """R5: the profile forbade inventing compilation intent and never
        said where to record that the guide was not inventing it, so the
        disclaimer went into the prose instead."""
        text = flat(PROFILE.read_text(encoding="utf-8"))
        self.assertIn("These are constraints on what may be asserted, and "
                      "they are satisfied by not asserting it", text)
        self.assertIn("it does not tell the reader that its observation does "
                      "not prove a compiler's intention", text)

    def test_the_no_side_rule_is_bounded_to_what_it_governs(self):
        """R6: written about recensions and reforms, it read as a general
        neutral-observer stance and produced distance from the tradition."""
        text = flat(EDITORIAL.read_text(encoding="utf-8"))
        self.assertIn("This is a constraint on the writing, not a reticence "
                      "about the facts", text)
        self.assertIn("What the rule constrains is comparison: between rites, "
                      "recensions, editions, uses, and reforms", text)
        self.assertIn("It is not a posture of neutrality toward the Catholic "
                      "reading of Scripture", text)

    def test_the_synthesis_brief_keeps_its_register_to_itself(self):
        """The brief is an audit record; the author inherits conclusions."""
        text = self.fragment("research-synthesis.md")
        self.assertIn("The author inherits the conclusions and not the "
                      "register", text)


# ---------------------------------------------------------------------------
# Guidance ownership: one authority, and fragments that point at it
# ---------------------------------------------------------------------------

class GuidanceOwnershipTests(unittest.TestCase):
    """The rules are publication requirements, not workflow tactics."""

    @classmethod
    def setUpClass(cls):
        cls.editorial = flat(EDITORIAL.read_text(encoding="utf-8"))
        cls.profile = flat(PROFILE.read_text(encoding="utf-8"))

    def test_editorial_owns_the_declarative_rule(self):
        self.assertIn("## State the finding, not the process that produced it",
                      EDITORIAL.read_text(encoding="utf-8"))
        self.assertIn("It does not narrate the editorial principles behind "
                      "those conclusions", self.editorial)
        self.assertIn("A constraint on what may be asserted is satisfied by "
                      "not asserting it, never by disclaiming it in the "
                      "reader's hearing", self.editorial)

    def test_editorial_owns_the_interpretive_voice_rule(self):
        self.assertIn("## Speaking from within the tradition",
                      EDITORIAL.read_text(encoding="utf-8"))
        self.assertIn("are presented from within the Catholic tradition that "
                      "produced them, not from a stance outside it",
                      self.editorial)
        self.assertIn("Modern skepticism is not the neutral default",
                      self.editorial)

    def test_the_rule_does_not_weaken_research(self):
        """Part III of the governing brief: qualify internally, state plainly.

        The failure mode of a declarative-prose rule is that a writer reaches
        it by researching less and asserting more.
        """
        self.assertIn("The desired movement is research thoroughly, qualify "
                      "internally, and then state the resulting conclusion "
                      "directly", self.editorial)
        self.assertIn("It is never research less and assert more",
                      self.editorial)

    def test_editorial_keeps_the_three_carve_outs(self):
        """Proofs 7-9 in the authority that owns them."""
        for carve_out in ("**Historical-critical fact.**",
                          "**Genuine disagreement.**",
                          "**Cultural afterlife.**"):
            with self.subTest(carve_out=carve_out):
                self.assertIn(carve_out, self.editorial)
        self.assertIn("What it may not become is the hermeneutical judge of "
                      "Catholic theological interpretation", self.editorial)
        self.assertIn("It is documented rather than purged for being secular",
                      self.editorial)

    def test_editorial_states_the_grammatical_discriminator(self):
        self.assertIn("A qualifying sentence is legitimate when its subject "
                      "is a source, a text, a witness, or a fact",
                      self.editorial)
        self.assertIn("The same sentence is the defect when its subject is "
                      "the guide, the reading, or an evidence class",
                      self.editorial)

    def test_the_profile_points_at_the_owner_and_states_only_deltas(self):
        """One owner, a bold pointer, deltas only - the house pattern."""
        self.assertIn("**The house voice is owned by "
                      "[`guidance/editorial.md`](../editorial.md)",
                      self.profile)
        self.assertIn("Both govern every reader-facing word of a proper "
                      "guide, and both are revised there and not here",
                      self.profile)
        self.assertIn("Four deltas apply to this genre", self.profile)

    def test_the_profile_does_not_restate_the_universal_rule(self):
        """A long parallel formulation in two files is two rules tomorrow."""
        self.assertNotIn("Do not make apology, suspicion, modern correction, "
                         "or distance from inherited typology the organizing "
                         "voice", self.profile)
        self.assertNotIn("## Speaking from within the tradition", self.profile)
        self.assertNotIn("State the finding, not the process that produced "
                         "it.**", self.profile.replace(
                             '"State the finding, not the process that '
                             'produced it".', ""))

    def test_the_profile_exempts_the_sections_that_qualify_by_design(self):
        self.assertIn("are qualification by design, and the declarative rule "
                      "does not reach them", self.profile)
        self.assertIn("What it reaches is their register leaking into the "
                      "body", self.profile)

    def test_the_profile_delta_reaches_every_reader_facing_section(self):
        """The delta named five sections, so page 2, the gallery and the
        exploratory proposals were told the rules did not apply to them
        while criterion 12 was widened to judge them."""
        for section in ("Scriptural Date and Location",
                        "The Propers: Notable and Quotable",
                        "the proposals of `The Propers: Interpretive "
                        "Possibilities`"):
            with self.subTest(section=section):
                self.assertIn(section, self.profile)
        self.assertIn("Both rules reach every reader-facing word",
                      self.profile)
        self.assertIn("never reach that required content", self.profile)

    def test_the_profile_does_not_require_the_limits_to_be_signposted(self):
        """The surviving incentive: a signpost scan could only recover the
        principal limits if the limits were printed as signposts, which is
        the fault, and is what produced the `Control retained` column."""
        self.assertNotIn("decisive evidence, and principal limits",
                         self.profile)
        self.assertIn("Do not make the limits recoverable by scan",
                      self.profile)
        self.assertIn("a table column that prints the discipline",
                      self.profile)
        self.assertIn("a requirement that a scan surface the limits is how "
                      "a guide is driven to write one", self.profile)

    def test_the_profile_gate_can_reject_a_violation(self):
        self.assertIn("the reader-facing body states its findings rather than "
                      "the editorial process behind them and speaks from "
                      "within the Catholic tradition", self.profile)

    def test_the_profile_keeps_the_secular_gallery(self):
        self.assertIn("A secular, ironic, political, or hostile afterlife is "
                      "the point of an entry there and is never removed for "
                      "being secular", self.profile)


# ---------------------------------------------------------------------------
# Regression: a house-style correction, not a workflow redesign
# ---------------------------------------------------------------------------

class PreservedTopologyTests(unittest.TestCase):
    """Nothing in the accepted topology moved."""

    @classmethod
    def setUpClass(cls):
        cls.workflow = workflow_json()
        cls.stages = {s["id"]: s for s in cls.workflow["stages"]}

    def test_no_lane_was_added_for_the_new_criteria(self):
        """Criterion 11 and 12 went to lanes that already read the prose."""
        for stage_id, lanes in (("research", RESEARCH_LANES),
                                ("content-evaluation", CONTENT_LANES),
                                ("visual-evaluation", VISUAL_LANES)):
            with self.subTest(stage=stage_id):
                execution = self.stages[stage_id]["execution"]
                self.assertEqual(execution["mode"], FANOUT)
                self.assertEqual(execution["parallelism"], HOST_MAX)
                self.assertEqual(execution["join"], STRICT_UNION)
                self.assertEqual([l["id"] for l in execution["lanes"]], lanes)
        self.assertEqual(len(RESEARCH_LANES), 7)
        self.assertEqual(len(CONTENT_LANES), 5)

    def test_the_lanes_still_own_disjoint_finding_spaces(self):
        for lane in CONTENT_LANES:
            with self.subTest(lane=lane):
                assert_lane_owns_its_findings(self, f"content-{lane}")

    def test_the_single_owner_stages_are_unchanged(self):
        for stage_id in ("research-synthesis", "author-proper",
                         "content-revision", "source-audit"):
            with self.subTest(stage=stage_id):
                self.assertEqual(self.stages[stage_id]["execution"],
                                 {"mode": SINGLE})
        self.assertEqual(self.stages["research"]["next"], "research-synthesis")
        self.assertEqual(self.stages["content-revision"]["revision_target"],
                         "author-proper")

    def test_the_repair_routes_are_untouched(self):
        """The house voice added no route.

        Written when there were two routes; the third, `brief` to
        `research-synthesis`, is version 10's and predates the merge that
        brought the house voice onto this line. What this still guards is
        that criteria 11 and 12 introduced no route of their own, so the
        list is asserted whole rather than by length.
        """
        self.assertEqual(
            self.stages["content-evaluation"]["repair_routes"],
            [{"repair_target": "research", "transition": "research"},
             {"repair_target": "brief",
              "transition": "research-synthesis"},
             {"repair_target": "authoring",
              "transition": "content-revision"}])

    def test_the_result_schema_needed_no_new_value(self):
        """The house voice needed no repair target of its own.

        Every value below is routed, and none of them was added for
        criteria 11 and 12: `research` and `authoring` are the two the voice
        rules use, and `brief` came with version 10's third owner. A voice
        finding is `authoring` unless the evidence carries no Catholic
        reception at all, in which case it is `research`; `brief` never wins
        one, because the held-but-not-carried case is a criterion 3 defect.
        """
        schema = json.loads(
            (ROOT / "workflows" / "schema" / "content-evaluation-result.json")
            .read_text(encoding="utf-8"))
        self.assertEqual(schema["finding_enums"]["repair_target"],
                         ["research", "brief", "authoring"])
        self.assertEqual(schema["blocking_finding_fields"], ["repair_target"])

    def test_the_workflow_version_is_past_the_house_voice_bump(self):
        """Changed fragment bytes must stop a run bound to the old ones."""
        version = self.workflow["version"]
        self.assertIsInstance(version, int)
        self.assertGreaterEqual(
            version, HOUSE_VOICE_VERSION,
            "the author and evaluation fragments changed, so the bound "
            "source digest changed; a run seeded before that must be told to "
            "seed again")

    def test_the_manuals_state_the_version_the_pipeline_declares(self):
        version = self.workflow["version"]
        for manual in ("OPERATOR.md", "ARCHITECTURE.md"):
            with self.subTest(manual=manual):
                text = (ROOT / "workflows" / manual).read_text(
                    encoding="utf-8")
                stated = re.search(
                    r"`proper` workflow is at version (\d+)", text)
                self.assertIsNotNone(
                    stated, f"{manual} must state the workflow version")
                self.assertEqual(int(stated.group(1)), version)


if __name__ == "__main__":
    unittest.main()
