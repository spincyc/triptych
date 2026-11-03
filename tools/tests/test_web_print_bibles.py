"""Complete Bible source fidelity and explicit edition discovery contracts."""
from __future__ import annotations

import ast
import csv
from contextlib import contextmanager
from functools import lru_cache
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SCRATCH = ROOT / '.scratch/web-print-bibles/production-tests'
sys.path.insert(0, str(ROOT / 'scripts'))
import _web_print_bibles as adapter
import _bible_editions as registry
from _psalms import addressing
EXPECTED = {
    "douay-rheims": (73, 1334, 35804),
    "douay-rheims-american-1899": (73, 1334, 35811),
    "clementine-vulgate": (73, 1334, 35809),
    "catholic-public-domain-version": (73, 1333, 35827),
    "world-english-bible-catholic": (73, 1328, 35379),
    "king-james-version": (80, 1362, 36822),
    "revised-version-1895": (80, 1362, 36836),
}


@lru_cache(maxsize=1)
def product(name):
    return adapter.render_bible(ROOT, name)


def independent_verses(parts):
    """Different parser, fed serialized markup rather than renderer records."""
    found = []
    papal = adapter.catalog.papal
    for part in parts:
        parser = papal.DocumentParser()
        parser.feed(part["html"])
        for node in papal.walk(parser.root):
            if node.tag != "span" or node.attrs.get("class") != "verse":
                continue
            children = list(node.children)
            number = children.pop(0)
            assert number.tag == "sup" and number.attrs.get("class") == "verse-number"
            body = ''.join(papal._visible(child) for child in children)
            found.append((node.attrs["data-verse-key"], papal._visible(number), ' '.join(body.split())))
    return found


class WholeBibleTests(unittest.TestCase):
    def test_all_seven_complete_editions_match_independent_raw_tsv_and_order(self):
        module = adapter.catalog._bible_typesetter()
        evidence = []
        original_open, original_bytes = Path.open, Path.read_bytes
        def safe_open(path, *args, **kwargs):
            self.assertNotEqual(path.suffix.lower(), '.pdf')
            self.assertFalse('src/web/data' in str(path), 'sparse browser data is not a whole-Bible source')
            return original_open(path, *args, **kwargs)
        def safe_bytes(path, *args, **kwargs):
            self.assertNotEqual(path.suffix.lower(), '.pdf')
            self.assertFalse('src/web/data' in str(path), 'sparse browser data is not a whole-Bible source')
            return original_bytes(path, *args, **kwargs)
        with patch.object(Path, 'open', safe_open), patch.object(Path, 'read_bytes', safe_bytes), \
                patch.object(subprocess, 'run', side_effect=AssertionError('No PDF/TeX/external tool is needed')):
            self.assertEqual(set(module.publishable(module.registry())), set(EXPECTED))
            for name, expected_counts in EXPECTED.items():
                with self.subTest(name=name):
                    rendered = product(name)
                    edition = module.Edition(name, module.entry(module.registry(), name), ROOT / 'src/sources/works')
                    printed = module.paragraphs_module().printed_marks(edition.artifacts)
                    expected_rows, expected_units, chapters = [], [], 0
                    source_stream = hashlib.sha256()
                    for book in edition.books:
                        previous = None
                        with book.path.open(encoding='utf-8', newline='') as stream:
                            for row in csv.DictReader(stream, delimiter='\t'):
                                token, chapter, verse, text = row['book'], int(row['chapter']), int(row['verse']), row['text']
                                self.assertEqual(token, book.token)
                                if chapter != previous:
                                    chapters += 1
                                    previous = chapter
                                    expected_units.append({'id': adapter.chapter_key(token, chapter),
                                                           'source': f'book:{token}#{chapter}', 'occurrence': '1'})
                                mark = '¶ ' if (token, chapter, verse) in printed else ''
                                expected_rows.append((f'{token}:{chapter}:{verse}', str(verse), ' '.join((mark + text).split())))
                                source_stream.update(f'{token}\t{chapter}\t{verse}\t{text}\n'.encode())
                    self.assertEqual((len(edition.books), chapters, len(expected_rows)), expected_counts)
                    self.assertEqual(tuple(rendered['counts'][key] for key in ('books','chapters','verses')), expected_counts)
                    self.assertEqual(rendered['expected_units'], expected_units)
                    self.assertEqual(rendered['coverage_result']['expected_units'], expected_units)
                    self.assertEqual(rendered['coverage_result']['verse_rows_sha256'], source_stream.hexdigest())
                    self.assertEqual(independent_verses(rendered['parts']), expected_rows)
                    self.assertEqual(rendered['coverage_result']['status'], 'pass')
                    self.assertEqual(rendered['context_sha256'], rendered['coverage_result']['context_sha256'])
                    self.assertGreater(rendered['coverage_result']['context_records'], rendered['counts']['chapters'])
                    self.assertTrue(all(len(part['html'].encode()) < 750_000 for part in rendered['parts']))
                    root = '\n'.join(part['html'] for part in rendered['parts'] if 'selector' in part)
                    self.assertEqual(rendered['source_id'], registry.EDITIONS[name]['source_id'])
                    owner = edition.artifacts.parent.relative_to(ROOT).as_posix() + '/'
                    for path in rendered['source_paths']:
                        if path.startswith('src/sources/'):
                            self.assertTrue(path.startswith(owner) or '/paragraph-projection-' in path)
                    self.assertIn('Verse-text edition.', root)
                    self.assertIn('extraction leaves out apparatus and some unnumbered headings', root)
                    self.assertIn('Source revision.', root)
                    self.assertIn('Source text retains its own rights.', root)
                    if name in {'king-james-version', 'revised-version-1895'}:
                        self.assertIn('United Kingdom', root)
                    for chunk in rendered['parts']:
                        if 'href' not in chunk:
                            continue
                        relative = PurePosixPath(chunk['href'])
                        self.assertFalse(relative.is_absolute())
                        self.assertNotIn('..', relative.parts)
                        route = str(PurePosixPath(rendered['root_route']).parent / relative)
                        self.assertTrue(route.startswith('print/bibles/' + name + '/'))
                        self.assertEqual(chunk['text_sha256'], adapter.sha(adapter.normalized_text(chunk['html'])))
                    evidence.append({'id': name, **rendered['counts'], 'parts': len(rendered['parts']),
                        'max_html_bytes': max(len(part['html'].encode()) for part in rendered['parts']),
                        'source_stream_sha256': source_stream.hexdigest(), 'coverage': 'exact native rows/order/text'})
        SCRATCH.mkdir(parents=True, exist_ok=True)
        (SCRATCH / 'test-evidence.json').write_text(json.dumps(evidence, indent=2) + '\n')

    def test_knox_is_refused_before_payload_access(self):
        module = adapter.catalog._bible_typesetter()
        with patch.object(module, 'Edition', side_effect=AssertionError('licensed payload access')), \
                self.assertRaisesRegex(ValueError, 'publishable is not true'):
            adapter.render_bible(ROOT, 'knox')

    def test_missing_explicit_source_root_never_falls_back_to_checkout(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            with self.assertRaisesRegex(ValueError, 'no artifact directory'):
                adapter.render_bible(Path(directory), 'douay-rheims')

    def test_products_leave_publication_shells_assets_and_fonts_to_catalogue(self):
        rendered = product('clementine-vulgate')
        self.assertEqual(rendered['assets'], [])
        self.assertEqual(rendered['fonts'], [])
        self.assertEqual(rendered['root_route'], 'print/bibles/clementine-vulgate.html')
        self.assertEqual(rendered['output_id'], 'bible:clementine-vulgate')
        self.assertTrue(all('<html' not in part['html'] for part in rendered['parts']))
        self.assertTrue(all(part['html_sha256'] == hashlib.sha256(part['html'].encode('utf-8')).hexdigest()
                            for part in rendered['parts']))
        self.assertIn('scripts/_web_print_bibles.py', rendered['source_paths'])
        self.assertTrue(all(not path.startswith('.scratch/') and not path.lower().endswith('.pdf')
                            for path in rendered['source_paths']))

    def test_native_psalm_openings_additions_verse_zero_and_escaping(self):
        book = SimpleNamespace(token='Ps', name='Psalms')
        body = adapter.chapter_html(book, 115, [(10, 'Native opening <kept> & word.')], {})
        self.assertIn('data-verse-key="Ps:115:10"', body)
        self.assertIn('>10</sup>', body)
        self.assertIn('&lt;kept&gt; &amp; word.', body)
        self.assertNotIn('data-verse-key="Ps:115:1"', body)
        body = adapter.chapter_html(book, 147, [(12, 'Native opening.')], {})
        self.assertIn('data-verse-key="Ps:147:12"', body)
        body = adapter.chapter_html(book, 3, [(0, 'Numbered title.'), (1, 'Body.')], {})
        self.assertIn('data-verse-key="Ps:3:0"', body)
        body = adapter.chapter_html(SimpleNamespace(token='EsthGr', name='Rest of Esther'), 10, [(4, 'Addition.')], {})
        self.assertIn('data-verse-key="EsthGr:10:4"', body)

    def test_missing_or_out_of_order_verses_and_chapters_fail_coverage(self):
        book = SimpleNamespace(token='Gen', name='Genesis')
        first = adapter.chapter_html(book, 1, [(1,'First.'), (2,'Second.')], {})
        second = adapter.chapter_html(book, 2, [(1,'Third.')], {})
        expected_units = [{'id':'chapter-Gen-1'}, {'id':'chapter-Gen-2'}]
        expected_rows = [('Gen:1:1','1','First.'), ('Gen:1:2','2','Second.'), ('Gen:2:1','1','Third.')]
        def chunk(html):
            return adapter.part('fixture', 'bible:fixture', 'a'*64, html, href='fixture.html')
        adapter.check_coverage(expected_units, expected_rows, [chunk(first + second)])
        mutations = {
            'missing-chapter': first,
            'out-of-order-chapters': second + first,
            'missing-verse': adapter.chapter_html(book, 1, [(1,'First.')], {}) + second,
            'out-of-order-verses': adapter.chapter_html(book, 1, [(2,'Second.'), (1,'First.')], {}) + second,
        }
        for name, html in mutations.items():
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'coverage|verse addresses'):
                adapter.check_coverage(expected_units, expected_rows, [chunk(html)])

    def test_html_bytes_are_pinned_only_after_complete_owner_coverage(self):
        body = adapter.chapter_html(SimpleNamespace(token='Gen', name='Genesis'),
                                    1, [(1, 'Élevé <kept> & word.')], {})
        chunk = adapter.part('fixture', 'bible:fixture', 'a' * 64, body,
                             href='fixture.html')
        self.assertNotIn('html_sha256', chunk)
        self.assertNotIn('text_sha256', chunk)
        expected = [('Gen:1:1', '1', 'Élevé <kept> & word.')]
        with self.assertRaisesRegex(ValueError, 'chapter coverage'):
            adapter.check_coverage([], expected, [chunk])
        self.assertNotIn('html_sha256', chunk)
        self.assertNotIn('text_sha256', chunk)
        original_html = chunk['html']
        adapter.check_coverage([{'id': 'chapter-Gen-1'}], expected, [chunk])
        self.assertEqual(chunk['html'], original_html)
        self.assertEqual(chunk['html_sha256'],
                         hashlib.sha256(original_html.encode('utf-8')).hexdigest())

    def test_complete_native_canon_contains_kjv_additions_and_rv_omissions(self):
        kjv = {key for key, _, _ in independent_verses(product('king-james-version')['parts'])}
        revised = {key for key, _, _ in independent_verses(product('revised-version-1895')['parts'])}
        self.assertIn('EsthGr:10:4', kjv)
        self.assertIn('Sus:1:1', kjv)
        self.assertIn('Bel:1:1', kjv)
        self.assertIn('Acts:8:36', revised)
        self.assertNotIn('Acts:8:37', revised)
        self.assertIn('Acts:8:38', revised)


PUBLIC = [name for name, edition in sorted(registry.EDITIONS.items(), key=lambda row: (row[1].get('rank', 999), row[0])) if edition['publishable']]


def offered(servable=None):
    """Evaluate the producer's exact typed list expression, without generation."""
    tree = ast.parse((ROOT / 'tools/index-bible').read_text())
    run = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'run_manifest')
    expression = next(node.value for node in run.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'offered' for target in node.targets))
    return eval(compile(ast.Expression(expression), '<manifest offered>', 'eval'), {
        'EDITIONS': registry.EDITIONS,
        'browser_print_offer': registry.browser_print_offer,
        'addressing': addressing,
        'servable': set(registry.EDITIONS) if servable is None else set(servable),
    })


def node(source, payload=None):
    result = subprocess.run(['node', '-e', source, json.dumps(payload)], text=True, capture_output=True, check=False, cwd=ROOT)
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


def browser_fixture():
    editions = []
    responses = {}
    for name, entry in registry.EDITIONS.items():
        edition = {'id': entry['source_id'], 'title': entry['edition'], 'language': entry['language'], 'date': '', 'passages': 0, 'readable': 0, 'file': name + '.json'}
        editions.append(edition)
        responses['fixture/source-editions/' + name + '.json'] = json.dumps({'work': {'id': 'work.test.bibles', 'title': 'The Bible', 'author': 'Source edition fixture'}, 'edition': edition, 'passages': [], 'artifacts': []})
    work = {'id': 'work.test.bibles', 'title': 'The Bible', 'author': 'Source edition fixture', 'category': 'scripture', 'directory': '', 'editions': editions}
    # editionPath requires an explicit directory; its value is source-authored.
    work['directory'] = 'source-editions/'
    responses['fixture/structure/sources/index.json'] = json.dumps({'root': '', 'works': [work], 'counted': {'works': 1}, 'facets': {}, 'advisory': ''})
    responses['fixture/bibles.json'] = json.dumps({'bibles': offered()})
    responses.update({
        'triptych/sources/index.html': (ROOT / 'src/web/browser/sources/index.html').read_text(),
        'triptych/sources/reader-model.js': (ROOT / 'src/web/browser/sources/reader-model.js').read_text(),
        'triptych/sources/sources.js': (ROOT / 'src/web/browser/sources/sources.js').read_text(),
        'triptych/sources/sources.css': (ROOT / 'src/web/browser/sources/sources.css').read_text(),
        'triptych/shared/browser-core.js': (ROOT / 'src/web/browser/shared/browser-core.js').read_text(),
        'triptych/shared/browser-core.css': (ROOT / 'src/web/browser/shared/browser-core.css').read_text(),
    })
    return responses


def drive(plan):
    SCRATCH.mkdir(parents=True, exist_ok=True)
    tree = ast.parse((ROOT / 'tools/tests/test_browser_truthfulness.py').read_text())
    harness = next(ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'HARNESS' for target in node.targets))
    harness = harness.replace('const PLAN = JSON.parse(process.argv[3]);', "const PLAN = JSON.parse(await readFile(process.argv[3], 'utf8'));")
    harness = harness.replace("join(tmpdir(), 'triptych-truthfulness-')", "join(ROOT, '.scratch/web-print-bibles/production-tests/chrome-')")
    (SCRATCH / 'harness.mjs').write_text(harness)
    (SCRATCH / 'browser-plan.json').write_text(json.dumps(plan))
    chrome = next((path for path in ('/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome-stable') if Path(path).exists()), None)
    if not chrome:
        raise unittest.SkipTest('Chromium not installed')
    result = subprocess.run(['node', str(SCRATCH / 'harness.mjs'), str(ROOT), str(SCRATCH / 'browser-plan.json'), chrome], capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


def action(expression, name=None):
    return {'do': 'eval', 'expression': expression, **({'name': name} if name else {})}


def wait(expression):
    return {'do': 'wait', 'until': expression}


class BibleDiscoveryTests(unittest.TestCase):
    def test_producer_exact_seven_public_editions_with_native_source_ids(self):
        rows = offered()
        self.assertEqual(len(rows), 7)
        self.assertEqual([row['id'] for row in rows], PUBLIC)
        for row in rows:
            self.assertEqual(row['source_id'], registry.EDITIONS[row['id']]['source_id'])
            self.assertEqual(row['print'], {'id': 'bible:' + row['id'], 'kind': 'bible', 'format': 'browser', 'href': 'print/bibles/' + row['id'] + '.html?print=1'})
        self.assertEqual(offered([PUBLIC[1]]), [rows[1]])

    def test_knox_and_unknown_never_get_a_print_offer(self):
        self.assertNotIn('knox', [row['id'] for row in offered()])
        for edition_id in ('knox', 'unknown', '', 'douay-rheims/../knox'):
            with self.subTest(edition_id=edition_id), self.assertRaises(ValueError):
                registry.browser_print_offer(edition_id)

    def test_selected_edition_join_has_no_default_or_ambiguous_fallback(self):
        result = node(r'''
const M = require(process.cwd() + '/src/web/browser/sources/reader-model.js');
const rows = JSON.parse(process.argv[1]);
const selected = rows.map(row => M.biblePrintForEdition(rows, row.source_id));
const first = rows[0];
const invalid = [null, '', 'edition.unknown', 'knox'].map(id => M.biblePrintForEdition(rows, id));
const duplicate = M.biblePrintForEdition(rows.concat([first]), first.source_id);
const bad = [
  {...first, print: null}, {...first, print: {...first.print, href:'https://outside.test/print'}},
  {...first, print: {...first.print, id:'bible:knox'}},
  {...first, print: {...first.print, format:'pdf'}},
  {...first, print: {...first.print, href:'print/bibles/knox.html?print=1'}}
].map(row => M.biblePrintForEdition([row], first.source_id));
process.stdout.write(JSON.stringify({selected,invalid,duplicate,bad}));
''', offered())
        self.assertEqual([row['id'] for row in result['selected']], PUBLIC)
        self.assertEqual(result['invalid'], [None] * 4)
        self.assertIsNone(result['duplicate'])
        self.assertEqual(result['bad'], [None] * 5)

    def test_site_path_preserves_project_prefix_and_ignores_data_override(self):
        result = node(r'''
const fs = require('node:fs'), vm = require('node:vm');
const code = fs.readFileSync('src/web/browser/shared/browser-core.js','utf8');
const results = ['', 'triptych/'].map(prefix => {
 const context = {URL,URLSearchParams, window:{location:{search:'?data=https://fixture.invalid/payload'}}, document:{currentScript:{src:'https://example.test/'+prefix+'shared/browser-core.js'},addEventListener(){}}};
 vm.runInNewContext(code, context);
 const T=context.window.Triptych;
 const rejected=['../print/x','/print/x','https://outside.test/x','print//x','print/./x','print/%2e%2e/x'].map(path=>{try{T.sitePath(path);return false;}catch(_){return true;}});
 return {href:T.sitePath('print/bibles/douay-rheims.html?print=1'),rejected};
});
process.stdout.write(JSON.stringify(results));
''')
        self.assertEqual([row['href'] for row in result], ['https://example.test/print/bibles/douay-rheims.html?print=1', 'https://example.test/triptych/print/bibles/douay-rheims.html?print=1'])
        self.assertTrue(all(all(row['rejected']) for row in result))

    def test_real_browser_all_seven_selected_editions_link_even_without_passages(self):
        acts = []
        for name in PUBLIC:
            source_id = registry.EDITIONS[name]['source_id']
            acts.extend([
                {'do': 'navigate', 'url': '/triptych/sources/index.html?data=/fixture#edition=' + source_id},
                wait("document.querySelector('[data-complete-bible-print]')"),
                action("({id:document.querySelector('[data-complete-bible-print]').dataset.completeBiblePrint, path:new URL(document.querySelector('[data-complete-bible-print]').href).pathname, query:new URL(document.querySelector('[data-complete-bible-print]').href).search, text:document.querySelector('[data-complete-bible-print]').textContent, label:document.querySelector('[data-complete-bible-print]').getAttribute('aria-label'), edition:document.querySelector('.reader-edition').textContent, empty:document.querySelector('#reader .placeholder').textContent})", name),
            ])
        for name, fragment in [('knox', '#edition=' + registry.EDITIONS['knox']['source_id']), ('finder', '')]:
            acts.extend([
                {'do': 'navigate', 'url': '/triptych/sources/index.html?data=/fixture' + fragment},
                wait("document.querySelector('#reading[aria-busy=false]') && performance.getEntriesByType('resource').some(e=>e.name.endsWith('/fixture/bibles.json')&&e.responseEnd)"),
                action("({links:document.querySelectorAll('[data-complete-bible-print]').length, hash:location.hash})", name),
            ])
        result = drive({'responses': browser_fixture(), 'acts': acts})
        (SCRATCH / 'browser-selected-editions.json').write_text(json.dumps(result, indent=2) + '\n')
        for name in PUBLIC:
            self.assertEqual(result[name]['id'], name)
            self.assertEqual(result[name]['path'], '/triptych/print/bibles/' + name + '.html')
            self.assertEqual(result[name]['query'], '?print=1')
            self.assertEqual(result[name]['text'], 'Print complete edition')
            self.assertEqual(result[name]['edition'], registry.EDITIONS[name]['edition'])
            self.assertIn('no passage', result[name]['empty'])
            self.assertIn(registry.EDITIONS[name]['label'], result[name]['label'])
        self.assertEqual(result['knox']['links'], 0)
        self.assertEqual(result['finder']['links'], 0)

    def test_delayed_offers_attach_only_to_current_selected_edition(self):
        source_a = registry.EDITIONS[PUBLIC[0]]['source_id']
        source_b = registry.EDITIONS[PUBLIC[2]]['source_id']
        result = drive({'responses': browser_fixture(), 'delays': [{'match': '/fixture/bibles.json', 'ms': 500}], 'acts': [
            {'do': 'navigate', 'url': '/triptych/sources/index.html?data=/fixture#edition=' + source_a},
            wait("document.querySelector('.reader-edition')"),
            action('location.hash=' + json.dumps('edition=' + source_b)),
            wait("document.querySelector('[data-complete-bible-print]')"),
            action("({id:document.querySelector('[data-complete-bible-print]').dataset.completeBiblePrint,count:document.querySelectorAll('[data-complete-bible-print]').length,edition:document.querySelector('.reader-edition').textContent})", 'selected'),
        ]})
        self.assertEqual(result['selected']['id'], PUBLIC[2])
        self.assertEqual(result['selected']['count'], 1)
        self.assertEqual(result['selected']['edition'], registry.EDITIONS[PUBLIC[2]]['edition'])



class BibleContextTests(unittest.TestCase):
    @contextmanager
    def fixture(self):
        directory_root = ROOT / '.scratch/web-print-bibles/context-proof'
        directory_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=directory_root) as directory:
            root = Path(directory)
            schema = root / 'src/common/document-schemas/bible-book-index.schema.json'
            schema.parent.mkdir(parents=True)
            schema.write_text('{}')
            artifacts = root / 'src/sources/works/fixture/bible/editions/native/artifacts'
            books = []
            for token, name, title, testament, rows in [
                ('Gen', 'Genesis', 'Native First Book', 'old', [(1, 1, 'First.'), (2, 1, 'Second.')]),
                ('Rev', 'Apocalypse', 'Native Last Book', 'new', [(1, 1, 'Third.')]),
            ]:
                path = artifacts / ('verse-text-' + token) / (token + '.tsv')
                path.parent.mkdir(parents=True)
                path.write_text('book\tchapter\tverse\ttext\n')
                path.with_name('artifact.toml').write_text(
                    f'id = "artifact.fixture.{token}"\nsha256 = "' + 'a' * 64 +
                    '"\ntransformation = "Canonical extraction qualification."\n')
                books.append(SimpleNamespace(token=token, name=name, title=title,
                                             testament=testament, path=path, verses=rows))
            registered = {'publishable': True, 'edition': 'Canonical edition identity',
                          'source_id': 'edition.fixture.native', 'language': 'en',
                          'numbering': 'native', 'psalter': 'native', 'psalm_titles': 'numbered'}
            edition = SimpleNamespace(id='fixture', edition=registered['edition'],
                source_id=registered['source_id'], language='en', numbering='native',
                psalter='native', psalm_titles='numbered', artifacts=artifacts, books=books,
                record={'title': 'Canonical Bible Title', 'publication': 'Canonical Publication',
                        'date': '1900', 'revision': 'Canonical revision', 'notes': 'Canonical edition qualification.'},
                rights={'status': 'public-domain', 'jurisdiction': 'Canonical jurisdiction',
                        'basis': 'Canonical rights basis.'}, load=lambda: None,
                digest=lambda: 'b' * 64)
            paragraphs = SimpleNamespace(PRINTED='printed', breaks=lambda *args: {})
            module = SimpleNamespace(registry=lambda: {'fixture': registered},
                entry=lambda registry, name: registry[name], Edition=lambda *args: edition,
                indexer=lambda: SimpleNamespace(Bible=lambda *args: None),
                paragraphs_module=lambda: paragraphs,
                TESTAMENTS={'old': 'Old Testament', 'new': 'New Testament'})
            with patch.object(adapter.catalog, '_bible_typesetter', return_value=module), \
                    patch.object(adapter, 'source_paths', return_value=set()), \
                    patch.object(adapter, 'select_book_index', return_value=root / 'book-index.tsv'), \
                    patch.object(adapter, 'check_book_index'):
                yield root, module, edition, registered

    def test_pre_pin_context_omissions_and_changes_are_refused(self):
        original_part, original_apparatus = adapter.part, adapter.apparatus
        cases = ['apparatus-omitted', 'intro-omitted', 'wrong-title', 'book-title-omitted',
                 'book-role', 'division-omitted', 'wrong-rights', 'qualification-omitted',
                 'transformation-omitted', 'project-notice-omitted', 'late-chapter-heading',
                 'wrong-link', 'wrong-language']
        for mutation in cases:
            with self.subTest(mutation=mutation), self.fixture() as (root, module, edition, registered):
                made = []
                def changed_part(identifier, output_id, source_digest, body, **kwargs):
                    if mutation == 'intro-omitted' and identifier == 'bible-introduction':
                        body = ''
                    if mutation == 'wrong-title':
                        body = body.replace('<h1>Canonical Bible Title</h1>', '<h1>Wrong Bible</h1>')
                    if mutation == 'book-title-omitted':
                        body = re.sub(r'<h3 class="bible-book">.*?</h3>\n', '', body)
                    if mutation == 'book-role':
                        body = body.replace('<h3 class="bible-book">', '<h2 class="bible-book">').replace('Book</h3>', 'Book</h2>')
                    if mutation == 'division-omitted':
                        body = re.sub(r'<h2 class="bible-division">.*?</h2>\n', '', body)
                    if mutation == 'wrong-rights':
                        body = body.replace('Canonical rights basis.', 'Wrong rights basis.')
                    if mutation == 'qualification-omitted':
                        body = body.replace('<p>Canonical edition qualification.</p>', '')
                    if mutation == 'transformation-omitted':
                        body = body.replace('<p>Canonical extraction qualification.</p>', '')
                    if mutation == 'project-notice-omitted':
                        body = re.sub(r'<p>Triptych organization and typography:.*?</p>', '', body)
                    if mutation == 'late-chapter-heading':
                        heading = re.search(r'<h4>.*?</h4>', body)
                        if heading:
                            body = body.replace(heading[0], '', 1).replace('</section>', heading[0] + '</section>', 1)
                    chunk = original_part(identifier, output_id, source_digest, body, **kwargs)
                    if mutation == 'wrong-link' and 'href' in chunk:
                        chunk['href'] = 'other-edition/chapter.html'
                    if mutation == 'wrong-language':
                        chunk['html'] = chunk['html'].replace('<section ', '<section lang="fr" ', 1)
                    made.append(chunk)
                    return chunk
                with patch.object(adapter, 'part', side_effect=changed_part), \
                        patch.object(adapter, 'apparatus', side_effect=(lambda *args: '') if mutation == 'apparatus-omitted' else original_apparatus):
                    with self.assertRaisesRegex(ValueError, 'canonical Bible context'):
                        adapter.render_bible(root, 'fixture')
                self.assertTrue(made)
                self.assertTrue(all('html_sha256' not in chunk and 'text_sha256' not in chunk for chunk in made))

    def test_canonical_language_metadata_is_not_taken_from_renderer(self):
        with self.fixture() as (root, module, edition, registered):
            edition.language = 'fr'
            with self.assertRaisesRegex(ValueError, 'canonical Bible context metadata'):
                adapter.render_bible(root, 'fixture')

    def test_context_digest_is_bound_to_selection_and_coverage_audit(self):
        with self.fixture() as (root, module, edition, registered):
            rendered = adapter.render_bible(root, 'fixture')
            expected = adapter.canonical_context(registered, edition, module,
                                                  rendered['counts'], rendered['source_digest'])
            digest = adapter.sha(adapter.canonical(expected))
            self.assertEqual(rendered['context_sha256'], digest)
            self.assertEqual(rendered['coverage_result']['context_sha256'], digest)
            self.assertEqual(rendered['coverage_result']['context_records'], len(expected['events']))
            self.assertEqual(rendered['selection_digest'], adapter.sha(adapter.canonical({
                'output_id': 'bible:fixture', 'source_digest': rendered['source_digest'],
                'expected_units': rendered['expected_units'],
                'verse_keys': ['Gen:1:1', 'Gen:2:1', 'Rev:1:1'], 'context_sha256': digest})))
            self.assertTrue(all(chunk['html_sha256'] == adapter.sha(chunk['html'])
                                and chunk['text_sha256'] == adapter.sha(adapter.normalized_text(chunk['html']))
                                for chunk in rendered['parts']))


if __name__ == '__main__':
    unittest.main()
