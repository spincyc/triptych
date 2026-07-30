"""Tests for the cross-provider research staleness ledger."""

import contextlib
import importlib.machinery
import importlib.util
import io
import pathlib
import tempfile
import unittest

TOOL_PATH = (
    pathlib.Path(__file__).resolve().parents[2] / "tools" / "lib" / "research-staleness"
)


def load_tool():
    loader = importlib.machinery.SourceFileLoader(
        "test_research_staleness_tool", str(TOOL_PATH)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class ResearchStalenessTests(unittest.TestCase):
    def setUp(self):
        self.tool = load_tool()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.tool.ROOT = self.root
        self.tool.LEDGER = (
            self.root / "src/sources/inventories/research-staleness-v1.toml"
        )
        self.tool.LEDGER.parent.mkdir(parents=True)
        self.gpt_leaf = self.root / "src/gpt/articles/example"
        self.claude_leaf = self.root / "src/claude/articles/example"
        for leaf in (self.gpt_leaf, self.claude_leaf):
            (leaf / "research").mkdir(parents=True)
            (leaf / "main.tex").write_text("main")
            (leaf / "research/scope.md").write_text("scope v1")
        work = self.root / "src/sources/works/augustine/confessiones"
        work.mkdir(parents=True)
        (work / "work.toml").write_text("id = 'work.augustine.confessiones'\n")
        (self.gpt_leaf / "research/source-bindings.toml").write_text(
            'schema = 1\nrecord_type = "bindings"\n'
            'document = "articles/example"\n\n'
            "[[bindings]]\n"
            'source_id = "work.augustine.confessiones"\n'
            'loci = ["1.1.1"]\nrole = "textual-control"\n'
            'states = ["cataloged"]\ncontext = "test"\n'
        )

    def test_bootstrap_then_fresh(self):
        self.tool.cmd_bootstrap()
        self.assertEqual(0, self.tool.cmd_status(None))

    def test_sibling_provider_research_change_flags_both(self):
        self.tool.cmd_bootstrap()
        (self.claude_leaf / "research/scope.md").write_text("scope v2")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(1, self.tool.cmd_status(None))
            self.assertEqual(1, self.tool.cmd_explain("gpt", "articles/example"))
        self.assertEqual(1, self.tool.cmd_explain("claude", "articles/example"))
        diagnostic = output.getvalue()
        self.assertIn(
            "stale gpt articles/example "
            "[cross-provider diagnostic only; staleness grants no authority "
            "to change this provider]",
            diagnostic,
        )
        self.assertIn(
            "changed input src/claude/articles/example/research/scope.md "
            "[cross-provider diagnostic only; staleness grants no authority "
            "to change this provider]",
            diagnostic,
        )

    def test_provider_local_change_does_not_show_cross_provider_notice(self):
        self.tool.cmd_bootstrap()
        (self.gpt_leaf / "research/scope.md").write_text("scope v2")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(1, self.tool.cmd_explain("gpt", "articles/example"))
        self.assertNotIn(self.tool.CROSS_PROVIDER_NOTICE, output.getvalue())

    def test_bound_source_record_change_flags_binder_only(self):
        self.tool.cmd_bootstrap()
        (
            self.root / "src/sources/works/augustine/confessiones/work.toml"
        ).write_text("id = 'work.augustine.confessiones'\nrevised = true\n")
        self.assertEqual(1, self.tool.cmd_explain("gpt", "articles/example"))
        self.assertEqual(0, self.tool.cmd_explain("claude", "articles/example"))

    def test_rebaseline_clears_single_edition(self):
        self.tool.cmd_bootstrap()
        (self.gpt_leaf / "research/scope.md").write_text("scope v2")
        (self.claude_leaf / "research/scope.md").write_text("scope v2")
        self.tool.cmd_rebaseline("gpt", "articles/example", False)
        self.assertEqual(0, self.tool.cmd_explain("gpt", "articles/example"))
        self.assertEqual(1, self.tool.cmd_explain("claude", "articles/example"))
        self.tool.cmd_rebaseline("claude", None, False)
        self.assertEqual(0, self.tool.cmd_status(None))

    def test_new_edition_reports_unbaselined(self):
        self.tool.cmd_bootstrap()
        new_leaf = self.root / "src/claude/articles/second"
        (new_leaf / "research").mkdir(parents=True)
        (new_leaf / "main.tex").write_text("main")
        self.assertEqual(1, self.tool.cmd_status(None))

    def test_bootstrap_refuses_second_run(self):
        self.tool.cmd_bootstrap()
        with self.assertRaises(self.tool.StalenessError):
            self.tool.cmd_bootstrap()


if __name__ == "__main__":
    unittest.main()
