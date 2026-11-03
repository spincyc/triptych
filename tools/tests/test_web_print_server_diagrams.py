"""Source-only discovery and explicit selected server-diagram authoring."""
from __future__ import annotations

import base64
import contextlib
import io
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import _web_print_server_diagrams as diagrams


class ServerDiagramAuthoringTests(unittest.TestCase):
    def test_inventory_reads_canonical_sources_without_subprocesses(self):
        with patch.object(diagrams.subprocess, 'run', side_effect=AssertionError('native discovery')):
            result = diagrams.inventory(ROOT)
        self.assertEqual(result['asset_count'], 39)
        self.assertEqual(result['active_macro_count'], 24)
        self.assertEqual({v: sum(e['variant'] == v for e in result['entries'].values())
                          for v in diagrams.VARIANTS}, {'child': 15, 'trainer': 15, 'sung': 9})
        self.assertIn('LMSceneCruetService',
                      result['entries']['child:LMSceneCruets']['definition_closure'])
        self.assertEqual(result['entries']['trainer:LMSceneLastGospel']['definition_closure']
                         ['LMSceneXUnit']['definition_tex'],
                         r'\newcommand{\LMSceneXUnit}{0.55cm}')
        self.assertEqual(result['entries']['child:LMSceneLastGospel']['definition_closure']
                         ['LMSceneXUnit']['definition_tex'],
                         r'\newcommand{\LMSceneXUnit}{0.75cm}')

    def test_list_and_inventory_cli_do_not_run_tools_or_write_assets(self):
        for command in ('list', 'inventory'):
            with self.subTest(command=command), contextlib.redirect_stdout(io.StringIO()) as out:
                with patch.object(diagrams.subprocess, 'run', side_effect=AssertionError('native CLI')):
                    self.assertEqual(diagrams.main(['--root', str(ROOT), command]), 0)
                self.assertIn('child:LMSceneStart', out.getvalue())

    def test_selected_wrapper_preserves_imports_switches_and_layout_state(self):
        with patch.object(diagrams.subprocess, 'run', side_effect=AssertionError('native wrapper')):
            trainer = diagrams.selected_wrapper(ROOT, 'trainer', 'LMSceneMissalMove')
            child = diagrams.selected_wrapper(ROOT, 'child', 'LMSceneMissalMove')
            sung = diagrams.selected_wrapper(ROOT, 'sung', 'MCAblutionsDiagram')
        self.assertIn(r'\def\pgfsysdriver{pgfsys-dvisvgm.def}', trainer)
        self.assertIn(r'\input{common/preamble}', trainer)
        self.assertIn(r'\TrainerManualGuidetrue', trainer)
        self.assertIn(r'\begin{minipage}{0.745\textwidth}', trainer)
        self.assertIn(r'\ChildBookletGuidetrue', child)
        self.assertIn(r'\begin{minipage}{\textwidth}', child)
        self.assertIn(r'\begin{deepstudy}', sung)
        self.assertIn('/shared/low-mass-diagrams}', trainer)
        self.assertIn('/shared/sung-mass-diagrams}', sung)
        self.assertNotIn(r'\newcommand{\LMScene', trainer)

    def test_unknown_macro_variant_and_injection_refuse_before_native_execution(self):
        for variant, macro in (('child', 'UnknownScene'), ('sung', 'LMSceneStart'),
                               ('unknown', 'LMSceneStart'), ('child', r'LMSceneStart}\input{bad')):
            with self.subTest(variant=variant, macro=macro):
                with patch.object(diagrams, '_native_tools', side_effect=AssertionError('native refusal')):
                    with self.assertRaises(diagrams.ServerDiagramError):
                        diagrams.render(ROOT, variant, macro, ROOT / '.scratch' / 'unused-render')
                    with self.assertRaises(diagrams.ServerDiagramError):
                        diagrams.selected_wrapper(ROOT, variant, macro)

    def test_unsafe_output_refuses_before_native_execution(self):
        for out in (ROOT, ROOT.parent / 'escaped-render', ROOT / 'src', ROOT / '.git' / 'render'):
            with self.subTest(out=out):
                with patch.object(diagrams, '_native_tools', side_effect=AssertionError('unsafe native render')):
                    with self.assertRaises(diagrams.ServerDiagramError):
                        diagrams.render(ROOT, 'child', 'LMSceneStart', out)
        self.assertEqual(diagrams.output_directory(ROOT, Path('.scratch/test-render')),
                         ROOT / '.scratch/test-render')
        self.assertEqual(diagrams.output_directory(ROOT, Path('build/server-diagram-render')),
                         ROOT / 'build/server-diagram-render')

    def test_output_symlink_escape_refuses_before_native_execution(self):
        scratch = ROOT / '.scratch'
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch, prefix='server-diagram-test-') as name:
            out = Path(name)
            (out / 'assets').symlink_to(ROOT / 'src', target_is_directory=True)
            with patch.object(diagrams, '_native_tools', side_effect=AssertionError('escaped native render')):
                with self.assertRaises(diagrams.ServerDiagramError):
                    diagrams.render(ROOT, 'child', 'LMSceneStart', out)

    def test_cli_requires_explicit_root_and_render_output(self):
        for args in (['list'], ['--root', str(ROOT), 'render',
                                '--variant', 'child', '--macro', 'LMSceneStart']):
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    diagrams.main(args)
                self.assertEqual(error.exception.code, 2)

    def test_font_fallback_and_box_diagnostics_refuse(self):
        for log in ('LaTeX Font Warning: Font shape unavailable.\n\n',
                    'Underfull \\hbox (badness 10000)\n',
                    'Missing character: There is no glyph in font.\n'):
            with self.subTest(log=log), self.assertRaises(diagrams.ServerDiagramError):
                diagrams._render_warnings(log)
        known = ('Package pgf Warning: Your graphic driver pgfsys-dvisvgm.def does not support fa\n'
                 'dings. This warning is given only once on input line 31.\n\n')
        self.assertEqual(diagrams._render_warnings(known), [known.strip()])

    @unittest.skipUnless(os.environ.get('TRIPTYCH_SERVER_DIAGRAM_TEST_OUT'),
                         'native authoring needs an explicit disposable test output')
    def test_optional_native_selected_render_and_original_png_identity(self):
        """Opt-in only; supplied expected hash can bind a reviewed immutable SVG."""
        for name in ('latex', 'dvisvgm', 'extractbb', 'dvitype', 'kpsewhich'):
            if not shutil.which(name):
                self.skipTest(f'missing selected-authoring runtime: {name}')
        out = Path(os.environ['TRIPTYCH_SERVER_DIAGRAM_TEST_OUT'])
        receipt = diagrams.render(ROOT, 'child', 'LMSceneMissalMove', out)
        target = diagrams.output_directory(ROOT, out) / receipt['asset']
        self.assertEqual(receipt['svg_sha256'], diagrams.sha(target.read_bytes()))
        expected = os.environ.get('TRIPTYCH_SERVER_DIAGRAM_EXPECTED_SHA256')
        if expected:
            self.assertEqual(receipt['svg_sha256'], expected)
        self.assertEqual(receipt['dvi_pages'], 1)
        self.assertEqual(receipt['pdf_files_generated'], [])
        self.assertNotEqual(receipt['repository_dependencies'], {})
        self.assertTrue(any(p.endswith('.pfb') for p in receipt['toolchain_dependencies']))
        elements = ET.parse(target).getroot().iter(f'{{{diagrams.SVG_NS}}}image')
        actual = [diagrams.sha(base64.b64decode(e.get(f'{{{diagrams.XLINK_NS}}}href').split(',', 1)[1]))
                  for e in elements]
        self.assertEqual(actual, [a['sha256'] for a in receipt['embedded_artwork']])
        self.assertTrue(all(diagrams.sha((ROOT / a['source']).read_bytes()) == a['sha256']
                            for a in receipt['embedded_artwork']))


if __name__ == '__main__':
    unittest.main()
