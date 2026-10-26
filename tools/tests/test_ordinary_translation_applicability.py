"""The CLI withholds a held day-only witness until its formulary is known."""
from pathlib import Path
import importlib.util
import json
import os
import sys
import unittest

ROOT = Path(os.environ.get('TRIPTYCH_REVIEW_ROOT', Path(__file__).resolve().parents[2]))
CODE = Path(os.environ.get('TRIPTYCH_ORDINARY_MODULE_ROOT', ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))
from _tooling import Style
spec = importlib.util.spec_from_file_location('scoped_ordinary_text', CODE / 'scripts/_ordinary_text.py')
text = importlib.util.module_from_spec(spec)
spec.loader.exec_module(text)

class OrdinaryTranslationApplicability(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ordinary = json.loads(Path(os.environ.get('TRIPTYCH_ORDINARY_DATA', ROOT /
            'src/web/data/structure/ordinary/roman-1962.json')).read_text())
        cls.head = next(e for s in ordinary['sections'] for e in s['elements']
                        if e['key'] == 'canon/communicantes-pascha')
        cls.words = next(t['text'] for t in cls.head['translations'] if t['lang'] == 'en')

    def render(self, context=None, element=None):
        return ' '.join(' '.join(text.element_lines(element or self.head, 'en',
            Style('unicode', False), context=context)).split())

    def test_default_unknown_and_vigil_cannot_execute_the_day_body(self):
        for context in (None, {}, {'calendar': 'roman-1962', 'formulary': 'unknown'},
                        {'calendar': 'roman-1962', 'formulary': 'easter-vigil'}):
            with self.subTest(context=context):
                self.assertNotIn(self.words, self.render(context))
                self.assertIn('applicability', self.render(context))

    def test_appointed_easter_day_retains_literal_words(self):
        self.assertIn(self.words, self.render({'calendar': 'roman-1962', 'formulary': 'easter-sunday'}))

    def test_guard_applies_before_heading_text_is_printed(self):
        heading = dict(self.head, kind='heading')
        self.assertNotIn(self.words, self.render(element=heading))
        self.assertIn(self.words, self.render({'calendar': 'roman-1962', 'formulary': 'easter-sunday'}, heading))

if __name__ == '__main__':
    unittest.main()
