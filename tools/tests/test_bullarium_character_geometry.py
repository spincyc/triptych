"""Character patches preserve source identity, indivisible units and raw chunks."""
from __future__ import annotations

import copy
import gzip
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _bullarium_character_geometry as engine
import _bullarium_geometry as words


class CharacterGeometryTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/bullarium_reconstruction/character_geometry/engine/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temp.name)
        self.out = self.root / ".scratch/result"
        self.recipe_path = self.root / "recipe.json"
        self.fixture()

    def tearDown(self):
        self.temp.cleanup()

    def fixture(self, source_space=" "):
        values = ["Títle ", "M.scientia" + source_space, "Right & more", "Later"]
        self.raw = (values[0] + "\r\n" + values[1] + "\r\n" + values[2] + "\r\n\r\n" + values[3]).encode()
        self.raw_path = self.root / "cache/raw.txt"
        self.xml_path = self.root / "cache/djvu.xml"
        self.native_path = self.root / "cache/native.xml"
        self.gz_path = self.root / "cache/native.gz"
        self.scan_path = self.root / "cache/scandata.xml"
        self.raw_path.parent.mkdir()
        self.raw_path.write_bytes(self.raw)
        xml = '<DjVuXML><BODY>'
        for leaf, vv in [(1, values[:3]), (2, values[3:])]:
            xml += f'<OBJECT width="400" height="300" usemap="fixture_{leaf:04}.djvu" data="/private/local/image.djvu">'
            for index, value in enumerate(vv):
                xml += f'<LINE><WORD coords="20,{30+index*40},390,{10+index*40}">{escape(value)}</WORD></LINE>'
            xml += '</OBJECT>'
        self.xml_path.write_text(xml + '</BODY></DjVuXML>')
        native = '<?xml version="1.0" encoding="UTF-8"?><document pagesCount="3">'
        native_pages = [[['WRAPPER_UNCLEARED_XYZ']], [list(values[0]), ['M', '.', 's', 'ci', 'e', 'n', 't', 'i', 'a', ' '], list(values[2])], [list(values[3])]]
        for pi, page in enumerate(native_pages):
            width, height = (500, 600) if pi == 0 else (400, 300)
            native += f'<page width="{width}" height="{height}" resolution="400" originalCoords="true">'
            for li, groups in enumerate(page):
                native += '<block><text><par><line>'
                x = 20
                for ci, value in enumerate(groups):
                    if pi == 1 and li == 1 and ci == 2:
                        x = 100
                    native += f'<charParams l="{x}" t="{10+li*40}" r="{x+len(value)*5}" b="{30+li*40}" charConfidence="100">{escape(value)}</charParams>'
                    x += len(value) * 5
                native += '</line></par></text></block>'
            native += '</page>'
        self.native_path.write_text(native + '</document>')
        self.gz_path.write_bytes(gzip.compress(self.native_path.read_bytes(), mtime=0))
        scan = '<book><pageData>'
        for leaf in range(3):
            scan += f'<page leafNum="{leaf}"><addToAccessFormats>{"false" if leaf==0 else "true"}</addToAccessFormats><pageType>Normal</pageType><cropBox><w>400</w><h>300</h></cropBox></page>'
        self.scan_path.write_text(scan + '</pageData></book>')
        pins = {k: self.pin(p) for k, p in zip(engine.SOURCES,
                [self.raw_path, self.xml_path, self.gz_path, self.native_path, self.scan_path])}
        page = words.source_pages(self.root, {k:v for k,v in pins['source_txt'].items() if k!='sha1'},
                                  {k:v for k,v in pins['source_xml'].items() if k!='sha1'}, [1])['pages'][0]
        b = self.native_path.read_bytes()
        start = b.index(b'<page width="400"')
        end = b.index(b'</page>', start) + len(b'</page>')
        text = ''.join(values[:3])
        spec = {'leaf':1, 'object_ordinal_1':1, 'native_page_ordinal_1':2,
                'source_byte_range_0':page['source_byte_range_0'], 'source_lf_range_1':page['source_lf_range_1'],
                'native_page_byte_range_0':[start,end],
                'nonwhite_fingerprint':{'sha256':self.sha(''.join(text.split()).encode()),'codepoints':len(''.join(text.split()))},
                'word_pins':[], 'split_words':[], 'components':[], 'before':'', 'replacement_sha256':'0'*64}
        self.recipe = {'schema':engine.SCHEMA, **pins, 'excluded_scan_leaves':[0], 'changed_pages':[spec], 'expected_output':{}}
        self.write_recipe()
        prepared = engine.prepare(self.root, self.recipe_path)['pages'][0]
        self.page = prepared['page']
        self.chars = [c for c in prepared['native_chars'] if c['native_line_page_1']==2]
        self.margin = [c['native_char_global_1'] for c in self.chars if c['bbox'][2] <= 30]
        self.body = [c['native_char_global_1'] for c in self.chars if c['bbox'][0] >= 100]
        spec['word_pins'] = [{k:v for k,v in w.items() if k in engine.WORD_FIELDS | {'source_attrs'}} for w in self.page['words']]
        spec['split_words'] = [{'source_word_global_1':2, 'native_chars':self.chars,
                                'whitespace_policy':'exact' if source_space==' ' else 'unicode-whitespace-only'}]
        def component(kind, number, value, role, ids=None):
            c={'kind':kind,'source_word_global_1':number,'value':value,'role':role,'flags':['synthetic-reviewed-role'],'after':'\n'}
            if ids is not None:c['native_char_global_ids_1']=ids
            return c
        byid={c['native_char_global_1']:c for c in self.chars}
        spec['components']=[component('word',1,values[0],'header'),component('word',3,values[2],'body-right'),
                            component('native-chars',2,''.join(byid[n]['value'] for n in self.body),'body-left',self.body),
                            component('native-chars',2,''.join(byid[n]['value'] for n in self.margin),'margin-left',self.margin)]
        self.expected()

    @staticmethod
    def sha(value):
        return hashlib.sha256(value).hexdigest()

    def pin(self, path):
        value=path.read_bytes()
        return {'path':path.relative_to(self.root).as_posix(),'sha256':self.sha(value),'byte_size':len(value),
                'sha1':hashlib.sha1(value).hexdigest()}

    def write_recipe(self):
        self.recipe_path.write_bytes(words._json_bytes(self.recipe))

    def expected(self):
        spec=self.recipe['changed_pages'][0]
        payload=(spec['before']+''.join(c['value']+c['after'] for c in spec['components'])).encode()
        spec['replacement_sha256']=self.sha(payload)
        a,z=spec['source_byte_range_0']
        self.hybrid=self.raw[:a]+payload+self.raw[z:]
        self.recipe['expected_output']={'sha256':self.sha(self.hybrid),'byte_size':len(self.hybrid)}
        self.write_recipe()

    def build(self):
        self.write_recipe()
        return engine.build(self.root,self.recipe_path,self.out)

    def test_deterministic_build_check_exact_unchanged_bytes_and_compact_maps(self):
        info=self.build()
        self.assertEqual(engine.check(self.root,self.recipe_path,self.out),info)
        second=self.root/'.scratch/second'
        engine.build(self.root,self.recipe_path,second)
        for p in self.out.iterdir():self.assertEqual(p.read_bytes(),(second/p.name).read_bytes())
        self.assertEqual((self.out/'hybrid.txt').read_bytes(),self.hybrid)
        self.assertTrue((self.out/'hybrid.txt').read_bytes().endswith(b'\r\nLater'))
        maps=[json.loads(line) for line in gzip.decompress((self.out/'component-map.jsonl.gz').read_bytes()).splitlines()]
        self.assertEqual([c['role'] for c in maps],['header','body-right','body-left','margin-left'])
        self.assertEqual(maps[1]['value'],'Right & more')
        chars=[c for row in maps for c in row['native_chars']]
        self.assertEqual(len(chars),len({c['native_char_global_1'] for c in chars}))
        self.assertIn('ci',[c['value'] for c in chars])
        self.assertEqual(info['split_WORDs'],1)
        self.assertEqual(info['changed_components'],4)
        self.assertEqual([p['leaf'] for p in info['excluded_upstream_pages']],[0])
        for p in self.out.iterdir():
            data=gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes()
            self.assertNotIn(b'/private/local',data)
            self.assertNotIn(b'cache/',data)
            self.assertNotIn(b'WRAPPER_UNCLEARED_XYZ',data)

    def test_multicodepoint_charParams_is_indivisible(self):
        body=self.recipe['changed_pages'][0]['components'][2]
        ci=next(c for c in self.chars if c['value']=='ci')
        body['native_char_global_ids_1'].remove(ci['native_char_global_1'])
        body['value']=body['value'].replace('ci','c')
        self.expected()
        with self.assertRaisesRegex(ValueError,'mutated exact source characters'):self.build()

    def test_pages_can_preserve_whole_WORDs_without_nominating_characters(self):
        s=self.recipe['changed_pages'][0];s['split_words']=[]
        s['components']=[{'kind':'word','source_word_global_1':w['source_word_global_1'],'value':w['value'],
                          'role':'uncertain','flags':['unreviewed-original-order'],'after':'\n'} for w in self.page['words']]
        self.expected();info=self.build()
        self.assertEqual(info['split_WORDs'],0)
        self.assertEqual(info['changed_components'],3)

    def test_wrong_leaf_native_ordinal_and_page_fingerprint_are_refused(self):
        original=copy.deepcopy(self.recipe)
        for key,value in [('leaf',2),('native_page_ordinal_1',3),('nonwhite_fingerprint',{'sha256':'0'*64,'codepoints':10})]:
            with self.subTest(key=key):
                self.recipe=copy.deepcopy(original);self.recipe['changed_pages'][0][key]=value
                with self.assertRaises(ValueError):self.build()
                self.assertFalse(self.out.exists())

    def test_wrong_native_XML_byte_range_and_bbox_are_refused(self):
        original=copy.deepcopy(self.recipe)
        for field,value in [('bbox',[0,0,1,1]),('source_xml_byte_range_0',[0,20]),('value','changed')]:
            with self.subTest(field=field):
                self.recipe=copy.deepcopy(original);self.recipe['changed_pages'][0]['split_words'][0]['native_chars'][0][field]=value
                with self.assertRaisesRegex(ValueError,'character value/bbox/byte pin mismatch'):self.build()

    def test_dropped_duplicated_and_mutated_native_components_are_refused(self):
        original=copy.deepcopy(self.recipe)
        for action in ['drop','duplicate','mutate']:
            with self.subTest(action=action):
                self.recipe=copy.deepcopy(original);c=self.recipe['changed_pages'][0]['components']
                if action=='drop':c.pop()
                elif action=='duplicate':c.append(copy.deepcopy(c[-1]))
                else:c[-1]['value']='replacement'
                self.expected()
                with self.assertRaises(ValueError):self.build()

    def test_whole_WORD_coverage_and_exact_value_are_required(self):
        original=copy.deepcopy(self.recipe)
        for action in ['drop-pin','duplicate-word','mutate-word','whole-plus-split']:
            with self.subTest(action=action):
                self.recipe=copy.deepcopy(original);s=self.recipe['changed_pages'][0]
                if action=='drop-pin':s['word_pins'].pop()
                elif action=='duplicate-word':s['components'].append(copy.deepcopy(s['components'][0]))
                elif action=='mutate-word':s['components'][0]['value']='Different'
                else:s['components'].append({**s['components'][0],'source_word_global_1':2,'value':'M.scientia '})
                self.expected()
                with self.assertRaises(ValueError):self.build()

    def test_full_binding_must_match_source_position_not_only_declared_text(self):
        split=self.recipe['changed_pages'][0]['split_words'][0]
        split['native_chars']=[{**c,'native_char_global_1':c['native_char_global_1']-1} for c in split['native_chars']]
        with self.assertRaisesRegex(ValueError,'position-aligned|pin mismatch'):self.build()

    def test_source_ordinal_types_cannot_alias_integers(self):
        original=copy.deepcopy(self.recipe)
        for field in ['split','WORD-pin','char-pin']:
            with self.subTest(field=field):
                self.recipe=copy.deepcopy(original);s=self.recipe['changed_pages'][0]
                if field=='split':s['split_words'][0]['source_word_global_1']=2.0
                elif field=='WORD-pin':s['word_pins'][0]['source_word_global_1']=True
                else:s['split_words'][0]['native_chars'][0]['bbox'][0]=float(s['split_words'][0]['native_chars'][0]['bbox'][0])
                with self.assertRaises(ValueError):self.build()

    def test_explicit_whitespace_only_normalization_and_exact_mode(self):
        # Rebuild a fresh isolated fixture with native one-space/source two-space tails.
        self.temp.cleanup();scratch=ROOT/'.scratch/bullarium_reconstruction/character_geometry/engine/tests'
        self.temp=tempfile.TemporaryDirectory(dir=scratch);self.root=Path(self.temp.name)
        self.out=self.root/'.scratch/result';self.recipe_path=self.root/'recipe.json';self.fixture('  ')
        self.assertEqual(self.build()['split_WORDs'],1)
        self.out=self.root/'.scratch/exact-failure'
        self.recipe['changed_pages'][0]['split_words'][0]['whitespace_policy']='exact'
        with self.assertRaisesRegex(ValueError,'original WORD whitespace'):self.build()

    def test_unhashed_changed_sources_and_wrong_gzip_decoding_are_refused(self):
        original=copy.deepcopy(self.recipe)
        for action in ['unhashed','changed-txt','changed-native','wrong-gzip']:
            with self.subTest(action=action):
                self.recipe=copy.deepcopy(original)
                raw,native,gz=self.raw_path.read_bytes(),self.native_path.read_bytes(),self.gz_path.read_bytes()
                if action=='unhashed':self.recipe['source_abbyy_xml'].pop('sha256')
                elif action=='changed-txt':self.raw_path.write_bytes(raw+b'x')
                elif action=='changed-native':self.native_path.write_bytes(native+b'x')
                else:
                    self.gz_path.write_bytes(gzip.compress(b'<different/>',mtime=0));self.recipe['source_abbyy_gz']=self.pin(self.gz_path)
                with self.assertRaises(ValueError):self.build()
                self.raw_path.write_bytes(raw);self.native_path.write_bytes(native);self.gz_path.write_bytes(gz)

    def test_native_characters_require_explicit_line_ownership(self):
        b=self.native_path.read_bytes().replace(b'<line>',b'').replace(b'</line>',b'')
        self.native_path.write_bytes(b);self.gz_path.write_bytes(gzip.compress(b,mtime=0))
        self.recipe['source_abbyy_xml']=self.pin(self.native_path);self.recipe['source_abbyy_gz']=self.pin(self.gz_path)
        with self.assertRaisesRegex(ValueError,'unique line/page'):self.build()

    def test_native_XML_entities_and_external_sources_are_refused(self):
        b=self.native_path.read_bytes().replace(b'<document',b'<!DOCTYPE document [<!ENTITY extra "x">]><document',1)
        self.native_path.write_bytes(b);self.gz_path.write_bytes(gzip.compress(b,mtime=0))
        self.recipe['source_abbyy_xml']=self.pin(self.native_path);self.recipe['source_abbyy_gz']=self.pin(self.gz_path)
        with self.assertRaisesRegex(ValueError,'DOCTYPE/entities'):self.build()

    def test_scandata_access_identity_and_full_native_page_fingerprint(self):
        original=self.scan_path.read_bytes()
        self.scan_path.write_bytes(original.replace(b'<addToAccessFormats>false',b'<addToAccessFormats>true',1))
        self.recipe['source_scandata']=self.pin(self.scan_path)
        self.recipe['excluded_scan_leaves']=[]
        with self.assertRaisesRegex(ValueError,'DjVu leaf sequence'):self.build()
        self.scan_path.write_bytes(original);self.recipe['source_scandata']=self.pin(self.scan_path)
        self.recipe['excluded_scan_leaves']=[0]
        # Change a character on the unchanged final page, repinning both native inputs.
        b=self.native_path.read_bytes().replace(b'>L</charParams>',b'>X</charParams>')
        self.native_path.write_bytes(b);self.gz_path.write_bytes(gzip.compress(b,mtime=0))
        self.recipe['source_abbyy_xml']=self.pin(self.native_path);self.recipe['source_abbyy_gz']=self.pin(self.gz_path)
        with self.assertRaisesRegex(ValueError,'page nonwhite fingerprint'):self.build()

    def test_excluded_leaf_assertion_and_excluded_page_patch_are_refused(self):
        self.recipe['excluded_scan_leaves']=[]
        with self.assertRaisesRegex(ValueError,'excluded scan leaves'):self.build()
        self.recipe['excluded_scan_leaves']=[0]
        self.recipe['changed_pages'][0]['leaf']=0
        self.recipe['changed_pages'][0]['native_page_ordinal_1']=1
        with self.assertRaisesRegex(ValueError,'changed leaf absent'):self.build()

    def test_existing_differing_products_are_not_overwritten(self):
        self.build()
        p=self.out/'hybrid.txt';p.write_bytes(b'Existing owner bytes.\n')
        with self.assertRaisesRegex(ValueError,'refusing to overwrite'):self.build()
        self.assertEqual(p.read_bytes(),b'Existing owner bytes.\n')

    def test_tampered_products_and_expected_hashes_are_refused(self):
        self.build()
        for name in ['hybrid.txt','byte-map.json','page-map.json','component-map.jsonl.gz','validation.json']:
            with self.subTest(name=name):
                p=self.out/name;b=p.read_bytes();p.write_bytes(b+b'X')
                with self.assertRaisesRegex(ValueError,'product mismatch'):engine.check(self.root,self.recipe_path,self.out)
                p.write_bytes(b)
        self.recipe['expected_output']['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'expected whole output'):self.build()

    def test_raw_page_span_and_expected_replacement_hash_are_pinned(self):
        original=copy.deepcopy(self.recipe)
        for field,value in [('source_byte_range_0',[1,20]),('source_lf_range_1',[1,9]),('replacement_sha256','0'*64)]:
            with self.subTest(field=field):
                self.recipe=copy.deepcopy(original);self.recipe['changed_pages'][0][field]=value
                with self.assertRaises(ValueError):self.build()

    def test_runtime_input_map_does_not_enter_maps_and_unknown_fields_reject(self):
        mapping={}
        for name in engine.SOURCES:
            pin=self.recipe[name];mapping[pin['sha256']]=pin.pop('path')
        self.write_recipe()
        engine.build(self.root,self.recipe_path,self.out,mapping)
        self.assertEqual(engine.check(self.root,self.recipe_path,self.out,mapping)['split_WORDs'],1)
        self.recipe['changed_pages'][0]['object_attrs']={'data':'/private/host/path'}
        self.write_recipe()
        with self.assertRaisesRegex(ValueError,'unsupported fields'):engine.build(self.root,self.recipe_path,self.root/'.scratch/refused',mapping)

    def test_nonwhitespace_insertion_and_canonical_output_are_refused(self):
        self.recipe['changed_pages'][0]['before']='invented'
        with self.assertRaisesRegex(ValueError,'only whitespace'):self.build()
        self.recipe['changed_pages'][0]['before']=''
        self.write_recipe()
        with self.assertRaisesRegex(ValueError,'repository .scratch'):engine.build(self.root,self.recipe_path,self.root/'src/sources/forbidden')


if __name__ == '__main__':
    unittest.main()
