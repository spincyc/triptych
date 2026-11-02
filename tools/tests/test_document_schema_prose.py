from pathlib import Path
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
from document_schema_checks.prose import check, editorial_requirements


class ProseChecks(unittest.TestCase):
    def setUp(self):
        scratch = REPO / ".scratch/schema-ref-checks"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def put(self, record, source, text):
        target = self.root / record["source_dir"] / source
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def record(self, kind="article-faith"):
        leaf = {"article-faith": "articles/faith/example", "article-canon-law": "articles/canon-law/example", "biography": "biographies/example", "history-account": "history/example/01-study", "history-parish": "history/catholic-parish-histories/01-example"}[kind]
        record = {"kind": kind, "provider": "gpt", "leaf": leaf, "id": f"gpt/{leaf}", "source_dir": f"src/gpt/{leaf}", "entrypoint": "main.tex", "structure": []}
        for role in ("scope", "source-audit"):
            self.role(record, role, f"research/{role}.md", "An actual research record.\n")
        self.put(record, "main.tex", "\\begin{document}\nAn argument can unfold without an opening thesis label.\n\\end{document}")
        return record

    def role(self, record, role, source, text):
        record["structure"].append({"role": role, "source": source})
        return self.put(record, source, text)

    def test_article_has_no_forced_thesis_or_section_order(self):
        record = self.record()
        self.assertEqual([], check(self.root, record))

    def test_biography_requires_distinct_substantive_ledgers(self):
        record = self.record("biography")
        self.role(record, "chronology", "research/chronology.md", "# Chronology\n")
        errors = check(self.root, record)
        self.assertIn("chronology: record contains no substantive content", errors)
        self.assertIn("missing required tradition-audit record", errors)
        self.role(record, "tradition-audit", "research/tradition-audit.md", "The earliest located witness and its limit.\n")
        self.put(record, "research/chronology.md", "A securely dated event and competing chronology.\n")
        self.assertEqual([], check(self.root, record))

    def test_biography_stable_keys_cannot_repeat(self):
        record = self.record("biography")
        self.role(record, "chronology", "research/chronology.md", "| Key | Event | Source |\n|---|---|---|\n| life-a | Event one | Witness one |\n| life-a | Event two | Witness two |\n")
        self.role(record, "tradition-audit", "research/tradition-audit.md", "Earliest witness and later reception.\n")
        self.assertIn("chronology: duplicate stable ledger key", check(self.root, record))

    def test_history_does_not_require_orientation_timeline(self):
        record = self.record("history-account")
        self.role(record, "evidence-map", "research/evidence-map.md", "The principal interpretive claim has an exact witness.\n")
        self.assertEqual([], check(self.root, record))

    def test_canon_law_needs_actual_legal_scope_block(self):
        record = self.record("article-canon-law")
        text = "\\section{Legal Scope and Currentness}\nThe 1983 CIC governs the Latin Church. Amendments checked as of 2026-07-25.\n"
        self.role(record, "scope-appendix", "sections/scope.tex", text)
        self.put(record, "main.tex", "\\begin{document}\nArgument.\n\\input{sections/scope}\n\\end{document}")
        self.assertEqual([], check(self.root, record))
        self.put(record, "sections/scope.tex", text.replace("Legal Scope and Currentness", "An argument"))
        self.assertTrue(any("Legal Scope and Currentness block" in e for e in check(self.root, record)))

    def test_canon_law_constant_appendix_can_be_defined_in_an_import(self):
        record = self.record("article-canon-law")
        self.put(record, "sections/argument.tex", "An argument.\n\\newcommand{\\legalappendix}{\\subsection{Legal Scope and Currentness}\nCIC governs the Latin Church. Amendments checked 2026-07-25.}\n")
        self.put(record, "main.tex", "\\begin{document}\n\\input{sections/argument}\n\\appendix\n\\legalappendix\n\\end{document}")
        self.assertEqual([], check(self.root, record))

    def test_parish_list_requires_a_source_import_and_resolved_refs(self):
        record = self.record("history-parish")
        self.role(record, "evidence-map", "research/evidence-map.md", "Officeholder and service date are witnessed.\n")
        self.role(record, "scope-appendix", "sections/scope.tex", "\\section{Historical coordinates}\nCorpus bounds.\n")
        self.role(record, "pastor-succession", "sections/historical-pastors.tex", "\\begin{longtable}{llll}\n1920 & Person & Pastor & Witness \\\\\n\\end{longtable}\n\\ref{missing-person}\n")
        self.role(record, "references", "sections/references.tex", "\\section{References}\nExact witnesses.\n")
        self.put(record, "main.tex", "\\begin{document}\nNarrative.\n\\input{sections/scope}\n\\input{sections/historical-pastors}\n\\input{sections/references}\n\\end{document}")
        self.assertIn("pastor-succession reference does not resolve: missing-person", check(self.root, record))
        self.put(record, "sections/historical-pastors.tex", "\\begin{longtable}{llll}\n1920 & Person & Pastor & Witness \\\\\n\\end{longtable}\n")
        self.assertEqual([], check(self.root, record))
        main = self.root / record["source_dir"] / "main.tex"
        main.write_text(main.read_text().replace("\\input{sections/historical-pastors}", ""))
        self.assertIn("pastor-succession list must be imported exactly once", check(self.root, record))

    def test_editorial_requirements_are_reported_separately(self):
        record = self.record()
        record["profile_definition"] = {"requirements": ["Assess source fidelity and fairness."]}
        self.assertEqual([], check(self.root, record))
        self.assertEqual(["Assess source fidelity and fairness."], editorial_requirements(record))


if __name__ == "__main__":
    unittest.main()
