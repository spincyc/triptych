"""Source mutations must break the appropriate reference contract without PDFs."""
from pathlib import Path
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
from _document_schema import SchemaError, _normalise
from document_schema_checks.reference import ANGEL_ARTICLES, SACRAMENTS, check


class ReferenceFixture(unittest.TestCase):
    def setUp(self):
        scratch = REPO / ".scratch" / "schema-ref-checks"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def put(self, leaf, name, text):
        target = self.root / "src/gpt" / leaf / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def record(self, kind, leaf, roles=()):
        return {"id": f"gpt/{leaf}", "provider": "gpt", "leaf": leaf,
                "source_dir": f"src/gpt/{leaf}", "kind": kind,
                "entrypoint": "main.tex", "structure": [
                    {"role": role, "source": source} for role, source in roles]}

    def novena(self, companion=False):
        owner = "devotions/novenas/00-example"
        leaf = owner + ("-daily-prayer" if companion else "")
        imports = []
        for number in range(1, 10):
            prayer = f"prayers/day-{number:02d}-collect.tex"
            self.put(owner, prayer, f"\\bilingualprayer{{Day {number}}}{{Witness}}{{Latin {number}}}{{English {number}}}\n")
            day = f"days/{number:02d}-example.tex"
            self.put(owner, day, f"\\section{{Day {number}: title}}\nA meditation.\n\\input{{{owner}/{prayer}}}\n")
            imports.append((f"\\recitationday{{{number}}}{{Title}}\n\\input{{{owner}/{prayer}}}\n") if companion else f"\\input{{{owner}/{day}}}\n")
        self.put(leaf, "main.tex", "\\begin{document}\n" + "".join(imports) + "\\end{document}\n")
        inventory = "| Prayer | Latin | English | Use |\n|---|---|---|---|\n"
        inventory += "".join(f"| Day {n}, Collect | Witness {n} | Human translation {n} | Day {n} |\n" for n in range(1, 10))
        self.put(owner, "research/prayer-inventory.md", inventory)
        record = self.record("novena-companion" if companion else "novena", leaf)
        record["structure"] = [{"role": "prayer-inventory", "data": f"src/gpt/{owner}/research/prayer-inventory.md"}]
        return record

    def sacraments(self, companion=False):
        owner = "theology/sacraments"
        leaf = owner + ("-at-a-glance" if companion else "")
        imports = []
        roles = []
        for role, source in (("sacrament-matrix", "fragments/full-matrix.tex"), ("sacrament-lexicon", "fragments/lexicon.tex")):
            self.put(owner, source, "Canonical retrieval content.\n")
            imports.append(f"\\input{{{owner}/{source}}}\n")
            roles.append({"role": role, "data": f"src/gpt/{owner}/{source}"})
        for number, name in enumerate(SACRAMENTS):
            treatment = f"sections/{number:02d}-{name}.tex"
            self.put(owner, treatment, f"\\section{{{name}}}\nSacramental treatment.\n")
            if not companion:
                imports.append(f"\\input{{{owner}/{treatment}}}\n")
            summary = f"summaries/{name}.tex"
            self.put(owner, summary, f"\\sacramentSummaryStart{{{name}}}{{Identity}}{{Theological content}}\n")
            imports.append(f"\\input{{{owner}/{summary}}}\n")
        table = "\\begin{tabularx}{\\linewidth}{XXXXX}\n"
        table += "".join(f"Tradition & Catholic Church {n} & Infant & Adult & Evidence \\\\\n" for n in range(24))
        table += "\\end{tabularx}\n"
        initiation = "sections/14-churches-initiation.tex"
        self.put(owner, initiation, table)
        imports.append(f"\\input{{{owner}/{initiation}}}\n")
        self.put(leaf, "main.tex", "\\begin{document}\n" + "".join(imports) + "\\end{document}\n")
        record = self.record("sacraments-summary" if companion else "sacraments", leaf)
        record["structure"] = roles + [{"role": "sacrament-summaries", "data": f"src/gpt/{owner}/summaries/*.tex"}, {"role": "initiation-table", "data": f"src/gpt/{owner}/{initiation}"}]
        return record

    def angelology(self):
        leaf = "theology/angelology"
        inventory = "| key | question | article | determination | grade | body |\n|---|---|---|---|---|---|\n"
        census = []
        body = []
        for question, maximum in ANGEL_ARTICLES.items():
            body.append(f"\\label{{sec:q{question}}}\nThe question is treated.\n")
            census.append(f"\\subsection{{Question {question}}}\n\\begin{{longtable}}{{lll}}\n")
            for article in range(1, maximum + 1):
                inventory += f"| I-{question}-{article} | {question} | {article} | Determination | Thomist position | sec:q{question} |\n"
                census.append(f"\\textbf{{{article}.}} Question & Determination & Grade \\\\\n")
            census.append("\\end{longtable}\n")
        self.put(leaf, "research/question-inventory.md", inventory)
        self.put(leaf, "sections/treatise.tex", "".join(body))
        roman = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV")
        self.put(leaf, "sections/15-celestial-hierarchy.tex", "".join(f"\\subsection{{{n}: Chapter}}\nExposition.\n" for n in roman))
        self.put(leaf, "appendices/02-article-census.tex", "".join(census))
        self.put(leaf, "main.tex", "\\begin{document}\n" + "".join(f"\\input{{{leaf}/{p}}}\n" for p in ("sections/treatise.tex", "sections/15-celestial-hierarchy.tex", "appendices/02-article-census.tex")) + "\\end{document}\n")
        return self.record("angelology", leaf, (("question-inventory", "research/question-inventory.md"),))

    def path(self, record, name):
        return self.root / record["source_dir"] / name

    def test_novena_exact_nine_day_and_prayer_map(self):
        record = self.novena()
        self.assertEqual([], check(self.root, record))
        main = self.path(record, "main.tex")
        main.write_text(main.read_text().replace("days/09-example.tex", "days/08-example.tex"))
        errors = check(self.root, record)
        self.assertTrue(any("nine day imports" in e and "duplicate=[8]" in e for e in errors), errors)

    def test_novena_missing_inventory_day_is_not_hidden_by_prose(self):
        record = self.novena()
        inventory = self.path(record, "research/prayer-inventory.md")
        inventory.write_text(inventory.read_text().replace("| Day 9, Collect | Witness 9 | Human translation 9 | Day 9 |", "Narrative mentions Day 9."))
        self.assertTrue(any("prayer-inventory day map" in e for e in check(self.root, record)))

    def test_novena_wrong_day_prayer_and_duplicate_vocal_text(self):
        record = self.novena()
        day = self.path(record, "days/09-example.tex")
        day.write_text(day.read_text().replace("day-09-collect", "day-08-collect"))
        self.assertTrue(any("day 9:" in e for e in check(self.root, record)))
        self.path(record, "prayers/day-09-collect.tex").write_text(self.path(record, "prayers/day-08-collect.tex").read_text())
        self.assertTrue(any("repeat the same" in e for e in check(self.root, record)))

    def test_companion_imports_canonical_prayers(self):
        record = self.novena(companion=True)
        self.assertEqual([], check(self.root, record))
        main = self.path(record, "main.tex")
        main.write_text(main.read_text().replace("\\recitationday{9}", "\\recitationday{8}"))
        self.assertTrue(any("companion recitation days" in e for e in check(self.root, record)))

    def test_comments_cannot_replace_a_mandatory_import(self):
        record = self.novena()
        main = self.path(record, "main.tex")
        main.write_text(main.read_text().replace("\\input{devotions/novenas/00-example/days/09", "%\\input{devotions/novenas/00-example/days/09"))
        self.assertTrue(any("nine day imports" in e for e in check(self.root, record)))

    def test_unused_macro_cannot_replace_a_mandatory_import(self):
        record = self.novena()
        main = self.path(record, "main.tex")
        edge = "\\input{devotions/novenas/00-example/days/09-example.tex}"
        main.write_text(main.read_text().replace(edge, "\\newcommand{\\unused}{" + edge + "}"))
        self.assertTrue(any("nine day imports" in e for e in check(self.root, record)))

    def test_sacraments_seven_and_twenty_four_distinct_churches(self):
        record = self.sacraments()
        self.assertEqual([], check(self.root, record))
        table = self.path(record, "sections/14-churches-initiation.tex")
        table.write_text(table.read_text().replace("Catholic Church 23", "Catholic Church 22"))
        self.assertTrue(any("24 distinct Church rows" in e for e in check(self.root, record)))

    def test_sacramental_companion_rejects_independent_prose(self):
        record = self.sacraments(companion=True)
        self.assertEqual([], check(self.root, record))
        main = self.path(record, "main.tex")
        main.write_text(main.read_text().replace("\\end{document}", "Independent theological claim.\n\\end{document}"))
        self.assertIn("sacramental companion contains independent prose outside canonical imports", check(self.root, record))

    def test_missing_sacramental_summary_and_matrix_import(self):
        record = self.sacraments(companion=True)
        main = self.path(record, "main.tex")
        main.write_text(main.read_text().replace("\\input{theology/sacraments/summaries/baptism.tex}", "").replace("\\input{theology/sacraments/fragments/full-matrix.tex}", ""))
        errors = check(self.root, record)
        self.assertTrue(any("baptism.tex must be imported" in e for e in errors), errors)
        self.assertTrue(any("full-matrix.tex must be imported" in e for e in errors), errors)

    def test_angel_inventory_and_reader_census_agree(self):
        record = self.angelology()
        self.assertEqual([], check(self.root, record))
        census = self.path(record, "appendices/02-article-census.tex")
        census.write_text(census.read_text().replace("\\textbf{5.} Question & Determination & Grade \\\\", "", 1))
        self.assertIn("article census does not project the question inventory exactly once per article", check(self.root, record))

    def test_angel_missing_final_article_and_duplicate_identity(self):
        record = self.angelology()
        inventory = self.path(record, "research/question-inventory.md")
        inventory.write_text(inventory.read_text().replace("| I-114-5 | 114 | 5 |", "| I-114-4 | 114 | 4 |"))
        errors = check(self.root, record)
        self.assertTrue(any("duplicates a stable key" in e for e in errors), errors)
        self.assertTrue(any("missing mandatory Summa articles: I 114.5" in e for e in errors), errors)

    def test_inventory_cross_reference_must_resolve(self):
        record = self.angelology()
        inventory = self.path(record, "research/question-inventory.md")
        inventory.write_text(inventory.read_text().replace("sec:q50", "sec:invented"))
        self.assertTrue(any("body label does not resolve: sec:invented" in e for e in check(self.root, record)))

    def test_hierarchy_missing_chapter_fails(self):
        record = self.angelology()
        hierarchy = self.path(record, "sections/15-celestial-hierarchy.tex")
        hierarchy.write_text(hierarchy.read_text().replace("\\subsection{XV: Chapter}", ""))
        self.assertTrue(any("chapters 1–15 once in order" in e for e in check(self.root, record)))

    def test_virtue_stable_keys_and_projection_names(self):
        leaf = "theology/virtues"
        inventory = "| Sort | Stable key | Preferred term and source term | Class and provenance | Formal object; characteristic act | Exact primary loci | Opposition |\n|---|---|---|---|---|---|---|\n| 01.010 | TV-FAITH | Faith (fides) | Theological | First truth; assent | Exact locus | Unbelief |\n"
        self.put(leaf, "research/virtue-inventory.md", inventory)
        census = "\\begin{longtable}{lllll}\nPrincipal & Unbelief & Faith & Inapplicable & Contrary \\\\\n\\end{longtable}\n"
        self.put(leaf, "sections/95-synoptic-table.tex", census)
        self.put(leaf, "main.tex", "\\input{sections/95-synoptic-table}")
        record = self.record("virtues", leaf, (("virtue-inventory", "research/virtue-inventory.md"),))
        self.assertEqual([], check(self.root, record))
        self.put(leaf, "sections/95-synoptic-table.tex", census.replace("& Faith &", "& Invented virtue &"))
        self.assertTrue(any("stable key TV-FAITH" in e for e in check(self.root, record)))
        self.put(leaf, "research/virtue-inventory.md", inventory + inventory.splitlines()[-1] + "\n")
        self.assertIn("virtue inventory duplicates a stable key or sort key", check(self.root, record))

    def test_marian_four_treatments_and_synopses(self):
        leaf = "theology/mariology/marian-dogmas"
        names = ("divine-motherhood", "perpetual-virginity", "immaculate-conception", "assumption")
        imports = []
        for number, name in enumerate(names):
            source = f"sections/{number:02d}-{name}.tex"
            self.put(leaf, source, "Source-grounded dogmatic exposition.")
            imports.append(f"\\input{{{source}}}\n")
        self.put(leaf, "sections/95-synopses.tex", "".join("\\subsection{" + name.replace("-", " ") + "}\nDefined object and its authority.\n" for name in names))
        imports.append("\\input{sections/95-synopses}\n")
        self.put(leaf, "main.tex", "".join(imports))
        record = self.record("marian-dogma", leaf)
        self.assertEqual([], check(self.root, record))
        self.put(leaf, "sections/95-synopses.tex", "\\subsection{Divine motherhood}\nOnly one synopsis.")
        self.assertTrue(any("four dogma synopses" in e for e in check(self.root, record)))

    def test_apparition_legacy_status_is_not_forced_into_modern_taxonomy(self):
        leaf = "theology/mariology/champion"
        self.put(leaf, "main.tex", "Event history and exact competent judgment.")
        dossier = "## Event dossier\n- **Stable identity:** One event.\n- **Jurisdiction:** Competent diocese.\n- **Authority / act:** Bishop, named act, date and locus.\n- **Exact object judged:** Bounded event.\n- **Current controlling status:** Historical formula preserved.\n"
        self.put(leaf, "research/corpus-status.md", dossier)
        record = self.record("marian-apparition", leaf, (("corpus-status", "research/corpus-status.md"),))
        self.assertEqual([], check(self.root, record))
        self.put(leaf, "research/corpus-status.md", dossier.replace("- **Exact object judged:** Bounded event.\n", ""))
        self.assertIn("apparition event dossier lacks object judged", check(self.root, record))

    def test_unknown_manifest_fields_are_refused(self):
        with self.assertRaisesRegex(SchemaError, "unknown fields: invented"):
            _normalise(self.root, {"invented": "accepted?"}, None)


if __name__ == "__main__":
    unittest.main()
