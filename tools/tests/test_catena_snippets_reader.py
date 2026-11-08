"""Exact reviewed snippets remain bound to their full natural source fragment."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import subprocess
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / 'src/web/browser/catena/catena-model.js'
NODE = shutil.which('node')
SCRATCH = ROOT / '.scratch/lane-snippet-browser'
TEXT = '  Context before.\n\nExact 😀 words <script>not markup</script>.\n\nContext after.  '
EXCERPT = 'Exact 😀 words <script>not markup</script>.'
START = TEXT.index(EXCERPT)
END = START + len(EXCERPT.encode('utf-16-le')) // 2
EXTENT = {'token': 'Gen', 'first_chapter': 1, 'first_verse': 3,
          'last_chapter': 1, 'last_verse': 4}
SNIPPET = {'id': 'verses-3-4', 'start': START, 'end': END, 'extent': EXTENT,
           'locator': 'Synthetic section 2', 'basis': 'Synthetic evidence; not a source claim.'}
PAYLOAD = {'text': TEXT, 'snippets': [SNIPPET], 'basis': 'Synthetic natural extent.',
           'acknowledgement': 'Synthetic required credit.'}


@unittest.skipUnless(NODE, 'Node is required')
class SnippetModelTest(unittest.TestCase):
    def probe(self, payload=PAYLOAD, expression=''):
        code = '''const M=require(process.argv[1]), raw=JSON.parse(process.argv[2]);
const body=M.textPayload(raw);
''' + (expression or '''process.stdout.write(JSON.stringify({saying:M.bodySaying(body),
snippets:M.matchingSnippets(body,'Gen',1,'3')}));''')
        done = subprocess.run([NODE, '-e', code, str(MODEL), json.dumps(payload)],
                              check=True, text=True, capture_output=True)
        return json.loads(done.stdout)

    def test_exact_utf16_slice_and_untrimmed_parent_survive(self):
        result = self.probe()
        self.assertEqual(result['saying'], {'missing': False, 'said': TEXT})
        self.assertEqual(result['snippets'], [{**SNIPPET, 'text': EXCERPT}])

    def test_overlap_matches_whole_excerpt_and_never_clips_its_extent(self):
        result = self.probe(expression='''process.stdout.write(JSON.stringify(
['','2','3','4','4-5','5','4-3'].map(verses=>M.matchingSnippets(body,'Gen',1,verses))));''')
        self.assertEqual([len(rows) for rows in result], [1, 0, 1, 1, 1, 0, 0])
        self.assertTrue(all(row['extent'] == EXTENT for rows in result for row in rows))

    def test_cross_chapter_extent_uses_both_canonical_boundaries(self):
        payload = copy.deepcopy(PAYLOAD)
        payload['snippets'][0]['extent'].update(last_chapter=2, last_verse=2)
        result = self.probe(payload, '''process.stdout.write(JSON.stringify(
[[1,'2'],[1,'3'],[2,'2'],[2,'3']].map(([ch,verses])=>M.matchingSnippets(body,'Gen',ch,verses).length)));''')
        self.assertEqual(result, [0, 1, 1, 0])

    def test_absent_empty_and_nonmatching_metadata_keep_the_full_fragment(self):
        for snippets in (None, [], [{**SNIPPET, 'extent': {**EXTENT, 'token': 'Phil'}}]):
            payload = copy.deepcopy(PAYLOAD)
            if snippets is None:
                del payload['snippets']
            else:
                payload['snippets'] = snippets
            result = self.probe(payload)
            self.assertEqual(result['snippets'], [])
            self.assertEqual(result['saying'], {'missing': False, 'said': TEXT})

    def test_bad_offsets_ranges_and_duplicate_rows_refuse_atomically(self):
        changes = [{'start': -1}, {'start': True}, {'start': str(START)}, {'end': START},
                   {'start': START + 1}, {'end': END - 1},
                   {'end': 10000}, {'start': START + 7}, {'end': START + 7},
                   {'extent': {**EXTENT, 'first_verse': 0}},
                   {'extent': {**EXTENT, 'last_verse': 2}}, {'id': '../wrong'},
                   {'basis': ''}, {'locator': []}]
        payloads = [{**PAYLOAD, 'snippets': [{**SNIPPET, **change}]} for change in changes]
        payloads.extend([{**PAYLOAD, 'snippets': [SNIPPET, SNIPPET]},
                         {**PAYLOAD, 'snippets': None}, {**PAYLOAD, 'snippets': {}}])
        for payload in payloads:
            with self.subTest(snippets=payload['snippets']):
                result = self.probe(payload)
                self.assertTrue(result['saying']['missing'])
                self.assertIn('snippets', result['saying']['said'])
                self.assertEqual(result['snippets'], [])

    def test_overlapping_or_reversed_offsets_and_unpaired_surrogates_refuse(self):
        for rows in ([SNIPPET, {**SNIPPET, 'id': 'second', 'start': END - 2}],
                     [SNIPPET, {**SNIPPET, 'id': 'before', 'start': 0, 'end': 3}]):
            self.assertTrue(self.probe({**PAYLOAD, 'snippets': rows})['saying']['missing'])
        self.assertTrue(self.probe({**PAYLOAD, 'text': TEXT + '\ud800'})['saying']['missing'])

    def test_untrusted_metadata_is_not_read_again_after_finalization(self):
        result = self.probe(expression='''const selected=M.matchingSnippets(body,'Gen',1,'3');
raw.text='changed';raw.snippets[0].extent.first_verse=31;raw.snippets[0].start=0;
process.stdout.write(JSON.stringify({same:M.matchingSnippets(body,'Gen',1,'3'),
frozen:Object.isFrozen(selected)&&Object.isFrozen(selected[0])&&Object.isFrozen(selected[0].extent),
raw:M.matchingSnippets(raw,'Gen',1,'3')}));''')
        self.assertEqual(result['same'][0]['text'], EXCERPT)
        self.assertTrue(result['frozen'])
        self.assertEqual(result['raw'], [])

    def test_optional_source_identity_is_frozen_and_not_inferred(self):
        record = {'edition_id': 'edition.synthetic.work.1900',
                  'artifact_id': 'artifact.synthetic.work.1900.text-ab123456',
                  'artifact_sha256': 'a' * 64, 'physical_line_ranges': [[3, 9]]}
        result = self.probe({**PAYLOAD, 'source_record': record}, '''const source=M.sourceRecord(body);
process.stdout.write(JSON.stringify({source,frozen:Object.isFrozen(source)&&
Object.isFrozen(source.physical_line_ranges[0])}));''')
        self.assertEqual(result['source'], record)
        self.assertTrue(result['frozen'])
        self.assertIsNone(self.probe(expression='process.stdout.write(JSON.stringify(M.sourceRecord(body)));'))


@unittest.skipUnless(NODE and shutil.which('chromium'), 'Chromium and Node are required')
class SnippetBrowserTest(unittest.TestCase):
    def test_late_body_uses_the_new_focus_without_reusing_old_excerpts(self):
        from . import _cdp_drive as cdp
        from .test_catena_passage_readers import SPINE
        spine = copy.deepcopy(SPINE)
        spine['fragments'] = [spine['fragments'][1]]
        spine['fragments'][0]['extent'].update(first_verse=1, last_verse=9)
        identifier = spine['fragments'][0]['id']
        path = 'src/web/data/structure/catena/text/' + identifier + '.json'
        route = '/src/web/browser/catena/index.html?data=/src/web/data#book=Gen&chapter=1&bible=douay-rheims&verses=3'
        opened = "document.querySelector('.author-body').open=true;document.querySelector('.fragment-body').open=true"
        plan = {'responses': {'src/web/data/structure/catena/01-gen/001.json': json.dumps(spine),
                              path: json.dumps(PAYLOAD)},
                'delays': [{'match': path, 'ms': 500}], 'acts': [
            {'do': 'navigate', 'url': route},
            cdp.wait("document.querySelector('#reading[aria-busy=false] .fragment-body')"),
            cdp.act(opened),
            cdp.wait("document.querySelector('.fragment-text').textContent==='Loading…'"),
            cdp.act("document.querySelector('#verse-input').value='8';document.querySelector('#passage-focus').requestSubmit()"),
            cdp.wait("location.hash.includes('verses=8') && document.querySelector('#reading[aria-busy=false] .fragment-body')"),
            cdp.act(opened),
            cdp.wait("document.querySelector('.fragment-text').textContent.includes('Context after.')"),
            cdp.act("({text:document.querySelector('.fragment-text').textContent,excerpts:document.querySelectorAll('.snippet-text').length,context:document.querySelectorAll('.fragment-context').length})", 'fresh')
        ]}
        SCRATCH.mkdir(parents=True, exist_ok=True)
        harness = cdp.HARNESS.replace("join(tmpdir(), 'triptych-truthfulness-')",
                                     "join(ROOT, '.scratch/lane-snippet-browser/chrome-')")
        with patch.object(cdp, 'SCRATCH', SCRATCH), patch.object(cdp, 'HARNESS', harness):
            result = cdp.drive(plan)
        self.assertEqual(result['fresh'], {'text': TEXT, 'excerpts': 0, 'context': 0})

    def test_excerpts_context_keyboard_history_and_print_use_the_same_exact_text(self):
        from . import _cdp_drive as cdp
        from .test_catena_passage_readers import SPINE
        spine = copy.deepcopy(SPINE)
        spine['fragments'] = [spine['fragments'][1]]
        spine['fragments'][0]['extent'].update(first_verse=1, last_verse=9)
        spine['fragments'][0]['acknowledgement'] = PAYLOAD['acknowledgement']
        identifier = spine['fragments'][0]['id']
        responses = {
            'src/web/data/structure/catena/01-gen/001.json': json.dumps(spine),
            'src/web/data/structure/catena/text/' + identifier + '.json': json.dumps(PAYLOAD)}
        route = '/src/web/browser/catena/index.html?data=/src/web/data#book=Gen&chapter=1&bible=douay-rheims&verses=3'
        opened = "document.querySelector('.author-body').open=true;document.querySelector('.fragment-body').open=true"
        snapshot = """({excerpt:document.querySelector('.snippet-text')?.textContent,
context:document.querySelector('.fragment-context > .fragment-text')?.textContent,
contextOpen:document.querySelector('.fragment-context')?.open,
label:document.querySelector('.fragment-context > summary')?.textContent,
credit:document.querySelector('.fragment-acknowledgement')?.textContent,
script:!!document.querySelector('.fragment-body script')})"""
        plan = {'responses': responses, 'acts': [
            {'do': 'navigate', 'url': route},
            cdp.wait("document.querySelector('#reading[aria-busy=false] .fragment-body')"),
            cdp.act("document.querySelectorAll('.fragment-snippets').length", 'lazy'),
            cdp.act(opened), cdp.wait("document.querySelector('.fragment-context')"),
            cdp.act(snapshot, 'excerpt'), cdp.act("document.querySelector('.fragment-context > summary').focus()"),
            {'do': 'key', 'key': 'Enter', 'code': 'Enter', 'virtualKeyCode': 13, 'text': '\r'},
            cdp.wait("document.querySelector('.fragment-context').open"), cdp.act(snapshot, 'full'),
            {'do': 'media', 'media': 'print'},
            cdp.act("getComputedStyle(document.querySelector('.fragment-snippets')).display", 'printSnippets'),
            {'do': 'media', 'media': ''},
            cdp.act("document.querySelector('#verse-input').value='8';document.querySelector('#passage-focus').requestSubmit()"),
            cdp.wait("location.hash.includes('verses=8') && document.querySelector('#reading[aria-busy=false] .fragment-body')"),
            cdp.act(opened), cdp.wait("document.querySelector('.fragment-text').textContent.includes('Context after.')"),
            cdp.act("({text:document.querySelector('.fragment-text').textContent,snippets:document.querySelectorAll('.snippet-text').length})", 'fallback'),
            cdp.act('history.back()'), cdp.wait("location.hash.includes('verses=3') && document.querySelector('#reading[aria-busy=false] .fragment-body')"),
            cdp.act(opened), cdp.wait("document.querySelector('.fragment-context')"), cdp.act(snapshot, 'back')
        ]}
        SCRATCH.mkdir(parents=True, exist_ok=True)
        harness = cdp.HARNESS.replace("join(tmpdir(), 'triptych-truthfulness-')",
                                     "join(ROOT, '.scratch/lane-snippet-browser/chrome-')")
        with patch.object(cdp, 'SCRATCH', SCRATCH), patch.object(cdp, 'HARNESS', harness):
            result = cdp.drive(plan)
        self.assertEqual(result['lazy'], 0)
        for key in ('excerpt', 'full', 'back'):
            self.assertEqual(result[key]['excerpt'], EXCERPT)
            self.assertEqual(result[key]['context'], TEXT)
            self.assertIn('Genesis 1:1-9', result[key]['label'])
            self.assertIn(PAYLOAD['acknowledgement'], result[key]['credit'])
            self.assertFalse(result[key]['script'])
        self.assertFalse(result['excerpt']['contextOpen'])
        self.assertTrue(result['full']['contextOpen'])
        self.assertEqual(result['printSnippets'], 'none')
        self.assertEqual(result['fallback'], {'text': TEXT, 'snippets': 0})


if __name__ == '__main__':
    unittest.main()
