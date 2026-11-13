"""Bounded Sources discovery and selected canonical reading stay complete."""
from __future__ import annotations

import importlib.machinery
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
loader = importlib.machinery.SourceFileLoader('discovery_reader_test', str(ROOT / 'tools/source-reader'))
spec = importlib.util.spec_from_loader(loader.name, loader)
reader = importlib.util.module_from_spec(spec)
sys.modules[loader.name] = reader
loader.exec_module(reader)


def fixture(size=300):
    works = []
    for at in range(size):
        works.append(dict(id=f'work.{at:04}', title=f'Title {at:04}', author='Author', category='book',
                          alternate_titles=['late alias'] if at == size - 1 else [], directory=f'editions/test/{at}/',
                          editions=[dict(id=f'edition.{at:04}', title=f'Title {at:04}', language='en',
                            date='1900', year=1900, file='1900-first.json', passages=1, readable=0,
                            rights=['restricted'])]))
    return dict(schema=reader.SCHEMA, works=works, root='structure/sources/', texts='structure/sources/text/',
                facets={}, counted=dict(works=size, editions=size, passages=size, readable=0))


def node(script, data):
    done = subprocess.run(['/usr/bin/node', '-e', script, str(ROOT)], input=json.dumps(data),
                          text=True, capture_output=True, check=True, timeout=30)
    return json.loads(done.stdout)


class DiscoveryTests(unittest.TestCase):
    def test_compact_metadata_preserves_titles_aliases_and_exact_routes(self):
        built = fixture()
        expanded = reader.expand_spine(reader.compact_spine(built))
        self.assertEqual(expanded['works'], built['works'])
        self.assertNotIn('works', reader.compact_spine(built))

    def test_shards_load_only_as_needed_and_failed_shard_is_retryable(self):
        files = reader.discovery_files(fixture())
        result = node(r"""
const fs = require('fs'), root = process.argv[1];
const M = require(root + '/src/web/browser/sources/reader-model.js');
const files = JSON.parse(fs.readFileSync(0, 'utf8'));
const calls = []; let fail = true;
const source = M.discovery(JSON.parse(files['index.json']), async (path) => {
  calls.push(path);
  if (fail && path.endsWith('0001.json')) { fail = false; throw Error('offline'); }
  return JSON.parse(files[path.replace('structure/sources/', '')]);
});
(async () => {
  await source.ensure(40);
  const first = { calls: calls.length, loaded: source.file.works.length, total: source.total };
  await source.ensure(80);
  let refused = false;
  try { await source.ensure(160); } catch (error) { refused = true; }
  await source.all();
  const matches = M.narrow(source.file.works, Object.assign(M.blank(), {find:'late alias'}));
  process.stdout.write(JSON.stringify({first, refused, calls: calls.length,
    all: source.file.works.length, alias: matches[0].work.id}));
})();
""", files)
        self.assertEqual(result, dict(first=dict(calls=1, loaded=128, total=300), refused=True,
                                      calls=4, all=300, alias='work.0299'))

    def test_adapter_first_page_is_bounded_and_global_search_reaches_last_shard(self):
        files = reader.discovery_files(fixture())
        result = node(r"""
const fs = require('fs'), root = process.argv[1];
const files = JSON.parse(fs.readFileSync(0, 'utf8')); const calls = [];
globalThis.ReaderModel = require(root + '/src/web/browser/sources/reader-model.js');
globalThis.Triptych = {languageName:(s)=>s, loadJSON: async (path)=>{
  calls.push(path); return JSON.parse(files[path.replace('structure/sources/', '')]);
}};
const adapter = require(root + '/scripts/lectern/adapters/sources.js')({script:()=>{}});
(async () => {
  const opening = await adapter.opening(); const opened = calls.length;
  const first = await adapter.find({}); const initial = calls.length;
  const next = await adapter.find({}, 1); const second = calls.length;
  const last = await adapter.find({find:'late alias'});
  const followed = await adapter.follow('edition.0299', '');
  process.stdout.write(JSON.stringify({opened, initial, second, total: opening.counted.works,
    summaries: opening.works.length, first: first.rows.length, next: next.rows[0][0],
    pages: first.pages, last: last.workRows[0][1].id, followed}));
})();
""", files)
        self.assertEqual(result, dict(opened=1, initial=2, second=2, total=300, summaries=0,
                                      first=40, next=40, pages=8, last='work.0299',
                                      followed=dict(work=299, edition=0, at=0)))


class FakeIndex:
    def __init__(self):
        self.rows = {}
        self.reads = []
    def add(self, kind, ident, relative, **values):
        self.rows[ident] = (relative, dict(id=ident, record_type=kind, **values))
    def record(self, ident):
        self.reads.append(ident)
        return self.rows[ident][1]
    def record_kind(self, ident):
        return self.rows[ident][1]['record_type']
    def record_path(self, ident):
        return self.rows[ident][0]
    def record_id_for_path(self, path):
        return next(ident for ident, row in self.rows.items() if row[0] == path)
    def paths(self, prefix='', suffix=None):
        return tuple(row[0] for row in self.rows.values() if row[0].startswith(prefix) and
                     (suffix is None or row[0].endswith(suffix)))
    def records(self, kind=None):
        raise AssertionError('selected reading enumerated the whole corpus')


class SelectedReadingTests(unittest.TestCase):
    def test_external_controller_stays_lazy_and_withheld_body_is_refused(self):
        from _reader_source_products import resolve
        index = FakeIndex()
        base = 'src/sources/works/test/reading/'
        edition = base + 'editions/first/'
        index.add('work', 'work.test', base + 'work.toml', title='The Work')
        index.add('edition', 'edition.test', edition + 'edition.toml', work_id='work.test',
                  title='First Edition', language='en', date='1900')
        foreign = 'src/sources/works/other/container/editions/first/'
        index.add('artifact', 'artifact.foreign', foreign + 'artifacts/text/artifact.toml',
                  edition_id='edition.foreign', rights_status='public-domain', storage='tracked',
                  rights_basis='Published 1900.', artifact_type='transcribed-text', media_type='text/plain')
        index.add('passage', 'passage.test', edition + 'passages/one.toml', edition_id='edition.test',
                  artifact_id='artifact.foreign', locus='1', text='Actual reading.')
        index.add('work', 'work.unrelated', 'src/sources/works/unrelated/work/work.toml', title='Unrelated')
        route = 'structure/sources/editions/test/reading/1900-first.json'
        detail = json.loads(resolve(route, ROOT, index))
        self.assertEqual(detail['edition']['id'], 'edition.test')
        self.assertFalse(detail['artifacts'][0]['edition_owned'])
        self.assertEqual(json.loads(resolve('structure/sources/text/passage.test.json', ROOT, index))['text'],
                         'Actual reading.')
        self.assertNotIn('work.unrelated', index.reads)
        index.rows['artifact.foreign'][1]['rights_status'] = 'restricted'
        detail = json.loads(resolve(route, ROOT, index))
        self.assertFalse(detail['passages'][0]['readable'])
        self.assertNotIn('text_path', detail['passages'][0])
        with self.assertRaisesRegex(ValueError, 'not readable'):
            resolve('structure/sources/text/passage.test.json', ROOT, index)


class TerminalPagingTests(unittest.IsolatedAsyncioTestCase):
    async def test_page_delivery_is_bounded_and_late_search_cannot_replace_it(self):
        from unittest.mock import patch
        from textual.widgets import OptionList
        from lectern.app import TriptychApp
        from lectern.surfaces.sources import Sources
        files = reader.discovery_files(fixture())
        data = node(r"""
const fs=require('fs'), root=process.argv[1], files=JSON.parse(fs.readFileSync(0,'utf8'));
globalThis.ReaderModel=require(root+'/src/web/browser/sources/reader-model.js');
globalThis.Triptych={languageName:s=>s,loadJSON:async path=>JSON.parse(files[path.replace('structure/sources/','')])};
const adapter=require(root+'/scripts/lectern/adapters/sources.js')({script:()=>{}});
(async()=>process.stdout.write(JSON.stringify({opening:await adapter.opening(),
 first:await adapter.find({}), second:await adapter.find({},1)})))();
""", files)
        asked = []
        with patch.object(Sources, 'start', lambda owner: None), patch.object(Sources, 'find',
                lambda owner, token, state, page=0: asked.append(page)):
            app = TriptychApp(start='sources')
            async with app.run_test(size=(140, 42)) as pilot:
                await pilot.pause()
                owner = app.current()
                owner.opened_with(data['opening'])
                owner.listed(data['first'])
                listing = owner.query_one('#sources-list', OptionList)
                self.assertEqual(listing.option_count, 81)
                self.assertEqual(listing.get_option_at_index(80).id, 'page-next')
                owner.refind(1)
                self.assertEqual(asked[-1], 1)
                token = owner._find_token
                owner.found_for(token - 1, data['first'])
                owner.found_for(token, data['second'])
                self.assertEqual(owner._finder_page, 1)
                self.assertEqual(listing.option_count, 82)
                self.assertEqual(listing.get_option_at_index(1).id, 'w-40')
                owner.found_for(token - 1, data['first'])
                self.assertEqual(owner._finder_page, 1)


if __name__ == '__main__':
    unittest.main()
