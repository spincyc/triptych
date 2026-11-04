"""Source-bound normalization and compact print proof invariants."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import _web_print_common as common


def descriptor():
    source='a'*64;identity='publication:fixture'
    html=(f'<section data-print-part="p" data-print-document="{identity}" data-print-source="{source}">'
          '<h2 id="heading">Source heading</h2><p id="u-1" data-print-unit="u-1">Complete source text.</p></section>')
    units=[{'id':'u-1','source':'fixture:canonical#1','occurrence':'1'}]
    return {'schema':'triptych-web-print-document/v1','id':identity,'title':'Source fixture','print_type':'flow',
            'source_digest':source,'selection_digest':'b'*64,'style_sha256':'c'*64,'expected_units':units,
            'coverage_result':{'status':'pass','output_id':identity,'source_digest':source,'selection_digest':'b'*64,'expected_units':copy.deepcopy(units)},
            'parts':[{'id':'p','href':'fixture/p.html',**common.part_statistics(html)}],
            'assets':[],'fonts':[]}


class CommonPrintTests(unittest.TestCase):
    def test_source_column_widths_have_matching_browser_classes_and_css(self):
        # The source-preserved colspan consumers expose these actual colgroup widths.
        observed = {16, 23, 24, 28, 30, 32, 35, 38, 40, 42, 56, 68, 69, 70, 86}
        self.assertLessEqual(observed, common.COLUMN_WIDTHS)
        script = (ROOT / 'src/web/browser/shared/web-print.js').read_text()
        columns = re.search(r"\.concat\(\[([0-9,]+)\]\.map\(\(n\) => 'print-column-width-'", script)
        self.assertIsNotNone(columns)
        self.assertEqual({int(n) for n in columns[1].split(',')}, common.COLUMN_WIDTHS)
        css = (ROOT / 'src/web/browser/shared/web-print.css').read_text()
        rules = re.findall(r'\[data-web-print-paper\] col\.print-column-width-(\d+)\s*\{\s*width:\s*(\d+)%;\s*\}', css)
        self.assertEqual({int(name) for name, _ in rules}, common.COLUMN_WIDTHS)
        self.assertTrue(all(name == width for name, width in rules))
        for width in observed:
            with self.subTest(width=width):
                source = f'<section><table><colgroup><col style="width: {width}%"></colgroup><tbody><tr><td colspan="2">Complete source note.</td></tr></tbody></table></section>'
                normalized = common.normalize_html(source)
                self.assertIn(f'class="print-column-width-{width}"', normalized)
                self.assertIn('colspan="2"', normalized)
                self.assertNotIn(' style=', normalized)
                self.assertEqual(common.part_statistics(source)['text_sha256'], common.part_statistics(normalized)['text_sha256'])

    def test_source_table_widths_have_matching_browser_classes_and_css(self):
        observed = {70, 74, 84, 86, 90, 94}
        self.assertLessEqual(observed, common.TABLE_WIDTHS)
        script = (ROOT / 'src/web/browser/shared/web-print.js').read_text()
        tables = re.search(r"const TABLE_CLASSES = \[([0-9,]+)\]\.map", script)
        self.assertIsNotNone(tables)
        self.assertEqual({int(n) for n in tables[1].split(',')}, common.TABLE_WIDTHS)
        css = (ROOT / 'src/web/browser/shared/web-print.css').read_text()
        rules = re.findall(r'\[data-web-print-paper\] table\.print-table-width-(\d+)\s*\{\s*width:\s*(\d+)%;\s*\}', css)
        self.assertEqual({int(name) for name, _ in rules}, common.TABLE_WIDTHS)
        self.assertTrue(all(name == width for name, width in rules))
        for width in observed:
            with self.subTest(width=width):
                source = f'<section><table style="width:{width}%;"><tbody><tr><td colspan="2">Complete source note.</td></tr></tbody></table></section>'
                normalized = common.normalize_html(source)
                self.assertIn(f'class="print-table-width-{width}"', normalized)
                self.assertIn('colspan="2"', normalized)
                self.assertEqual(common.part_statistics(source)['text_sha256'], common.part_statistics(normalized)['text_sha256'])

    def test_typed_source_styles_preserve_text_and_declared_dimensions(self):
        source=('<section><table style="width:85%;"><colgroup><col style="width: 10%"></colgroup><tbody><tr>'
                '<th style="text-align: right;">Source</th><td style="text-align: left;">same &amp; complete</td>'
                '</tr></tbody></table><p class="poetry-verse-line" style="margin:0">Arma virumque.</p>'
                '<div class="response-space" aria-label="Response space" style="min-height:0.65in"></div></section>')
        normalized,audit=common.normalize_html_with_projections(source,profile='curriculum')
        self.assertEqual(common.part_statistics(source)['text_sha256'],common.part_statistics(normalized)['text_sha256'])
        self.assertNotIn(' style=',normalized)
        for name in ['print-table-width-85','print-column-width-10','print-align-right','print-align-left','response-space-065']:
            self.assertIn(name,normalized)
        self.assertEqual(len(audit),6)
        self.assertEqual(common.normalize_html(normalized,profile='curriculum'),normalized)

    def test_unbound_visibility_styles_and_wrong_element_styles_refuse(self):
        for source in ['<p style="display:none">source</p>','<p style="text-align:left">source</p>',
                       '<table style="width:1%"></table>','<col style="width:99%">',
                       '<col style="width:33%">','<col style="width:35.5%">',
                       '<col style="width:35%;display:none">','<col style="width:calc(35%)">',
                       '<col style="width:var(--width)">','<table style="width:35%"></table>',
                       '<td style="width:35%">source</td>',
                       '<div class="response-space" style="min-height:0.1in"></div>',
                       '<p style="margin:0">untyped source</p>']:
            with self.subTest(source=source),self.assertRaises(common.ProfileError):common.normalize_html(source)

    def test_only_real_attribute_spans_are_rewritten_and_fold_state_is_typed(self):
        source='<details open class="source"><summary>Source</summary><p>complete</p></details>'
        result=common.normalize_html(source)
        self.assertEqual(result,'<details class="source"><summary>Source</summary><p>complete</p></details>')
        source='''<td title="literal style='display:none' class='example'" style="text-align: left;">source</td>'''
        result=common.normalize_html(source)
        self.assertIn('''title="literal style='display:none' class='example'"''',result)
        self.assertIn('class="print-align-left"',result)
        self.assertEqual(common.structure_sha256('<details open><p>x</p></details>'),common.structure_sha256('<details><p>x</p></details>'))

    def test_server_metadata_namespacing_and_known_grid_normalization_are_idempotent(self):
        source=('<section class="sheet low" data-side="front" data-sheet="1"><div class="grid" style="--rows:4">'
                '<article class="face" data-unit-id="LM-F01:front" data-pair-id="LM-F01"><p>Complete cue.</p></article>'
                '<div class="face blank" aria-hidden="true"></div></div></section>')
        result=common.normalize_html(source,profile='server-cards')
        self.assertIn('class="server-sheet server-low"',result)
        self.assertIn('data-print-unit="LM-F01:front"',result)
        self.assertNotIn('data-unit-id',result)
        self.assertNotIn('aria-hidden',result)
        self.assertNotIn(' style=',result)
        self.assertEqual(common.normalize_html(result,profile='server-cards'),result)
        with self.assertRaises(common.ProfileError):common.normalize_html('<p aria-hidden="true">source</p>',profile='server-guide')

    def test_part_measurements_keep_exact_nested_unit_and_id_order(self):
        source=('<section id="part-root" data-print-unit="plate-1"><h2 id="title">Plate</h2>'
                '<article id="obj-1" data-print-unit="obj-1" class="object object"><p>complete</p></article>'
                '<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mtext>Γ</mtext></mrow></math></section>')
        stats=common.part_statistics(source,selectors=['article','.object','[data-print-unit]','math'])
        self.assertEqual(stats['expected_ids'],['title','obj-1'])
        self.assertEqual(stats['units'],['plate-1','obj-1'])
        self.assertEqual(stats['counts'],{'article':1,'.object':1,'[data-print-unit]':1,'math':1})
        self.assertEqual(common.inventory(['verse-Γ-⛪']),{'count':1,'sha256':hashlib.sha256('["verse-Γ-⛪"]'.encode()).hexdigest()})

    def test_structure_does_not_repair_source_html_or_discard_raw_attributes(self):
        for source in ['<section><p>missing close</section>','<section><span/></section>',
                       '<section class="a" class="b"></section>','<section></section>lost source']:
            with self.subTest(source=source),self.assertRaises(common.StructureError):common.structure_events(source)
        implicit='<section><table><tr><td>source</td></tr></table></section>'
        explicit='<section><table><tbody><tr><td>source</td></tr></tbody></table></section>'
        self.assertNotEqual(common.structure_sha256(implicit),common.structure_sha256(explicit))
        self.assertNotEqual(common.structure_sha256('<ol start="1"><li>x</li></ol>'),common.structure_sha256('<ol start="2"><li>x</li></ol>'))

    def test_statistics_preserve_existing_structural_identities(self):
        vectors=[
            ('<section><p title="Γ &amp; ☩">Æ &amp; œ\u00a0℣</p></section>',None,
             'a0f6fa2ce01747df07209657f58489334ecf5233f0a030c49b0e8dc3056acf92'),
            ('<section>one\r\n<p id="p">two\rthree</p></section>',None,
             '37c7e1bd42daf35b8d1dac8e5d925e94f782db42f74af4088e36a4d2bbdc04bb'),
            ('<details open><summary>Title</summary><p>text</p></details>',None,
             '9bafb7edc5fc806b0eba6262193b106c2545e4a9ad193d51de33efea68ac22e6'),
            ('<section><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mi>Γ</mi>'
             '<mspace width="1em"/></mrow></math><br/></section>',None,
             'f9ec98be193489fcf1ea7741c5ec4a007211e0efb74bffb32fc6a0516d51672d'),
            ('<aside>outside</aside><section data-print-part="p"><p id="u" data-print-unit="u">'
             'Inside</p></section><footer>outside</footer>','p',
             '4aa3a4121b493b13741883b47551b1eb1a59a81f97c803326ed9b48667dd46f2'),
            ('<section data-print-unit="root"><p id="u" class="a a b" data-print-unit="u">'
             'same</p></section>',None,
             '733275eca2966639ed1103a32e55652bac8ee89d4b16902c94d813a8aac465cd'),
        ]
        for source,part,expected in vectors:
            with self.subTest(part=part,source=source):
                self.assertEqual(common.structure_sha256(source,part),expected)
                self.assertEqual(common.part_statistics(source,part)['structure_sha256'],expected)

    def test_statistics_still_reject_malformed_structure_and_duplicate_units(self):
        for source in ['<section><p>unclosed</section>','<section><span/></section>',
                       '<section class="a" class="b"></section>','<section></section>outside',
                       '<section>bad\0text</section>',
                       '<section><p id="same"></p><p id="same"></p></section>',
                       '<section data-print-unit="same"><p data-print-unit="same"></p></section>']:
            with self.subTest(source=source),self.assertRaises(common.PrintError):
                common.part_statistics(source)
        with self.assertRaises(common.StructureError):
            common.part_statistics('<section data-print-part="other"></section>','missing')

    def test_compaction_preserves_proof_without_copying_or_exposing_large_audit(self):
        class Ledger(list):
            def __deepcopy__(self,memo):raise AssertionError('large canonical ledger must not be deep-copied')
        full=descriptor();full['expected_units']=Ledger(full['expected_units'])
        full['coverage_result']['expected_units']=full['expected_units']
        full['sources']={'detailed':'audit-only'};full['parts'][0]['html']='audit-only source body'
        full['fonts']=[{'family':'Triptych Punctus Elevatus','href':'fonts/glyph.woff2','sha256':'d'*64,'unicode_range':'U+2E4E','source':'audit-only'}]
        compact=common.compact_descriptor(full,audit_sha256='e'*64)
        self.assertNotIn('sources',compact)
        self.assertNotIn('expected_units',compact)
        self.assertNotIn('html',compact['parts'][0])
        self.assertNotIn('source',compact['fonts'][0])
        self.assertEqual(compact['fonts'][0]['unicode_range'],'U+2E4E')
        self.assertEqual(compact['coverage_result']['audit_sha256'],'e'*64)
        self.assertEqual(compact['unit_inventory'],common.inventory(['u-1']))
        self.assertEqual(compact['coverage_result']['unit_inventory'],compact['unit_inventory'])
        self.assertIsInstance(full['expected_units'],Ledger)

    def test_compaction_never_invents_source_coverage_or_accepts_another_selection(self):
        for mutation in ['unverified','wrong-output','wrong-source','wrong-selection','wrong-units','missing-structure']:
            with self.subTest(mutation=mutation):
                full=descriptor()
                if mutation=='unverified':full['coverage_result']['status']='complete-mechanical-selection'
                elif mutation=='wrong-output':full['coverage_result']['output_id']='publication:other'
                elif mutation=='wrong-source':full['coverage_result']['source_digest']='0'*64
                elif mutation=='wrong-selection':full['coverage_result']['selection_digest']='0'*64
                elif mutation=='wrong-units':full['parts'][0]['units']=[]
                else:full['parts'][0].pop('structure_sha256')
                with self.assertRaises(ValueError):common.compact_descriptor(full)

    def test_a_thousand_source_parts_keep_public_transport_below_500kb(self):
        full=descriptor();units=[];parts=[]
        for index in range(1000):
            unit='unit-'+str(index);part='part-'+str(index)
            units.append({'id':unit,'source':'fixture:canonical#'+str(index),'occurrence':'1'})
            body=f'<section data-print-part="{part}"><p id="{unit}" data-print-unit="{unit}">Complete source {index}.</p></section>'
            parts.append({'id':part,'href':'parts/'+part+'.html',**common.part_statistics(body)})
        full['parts']=parts;full['expected_units']=units;full['coverage_result']['expected_units']=copy.deepcopy(units)
        compact=common.compact_descriptor(full)
        self.assertEqual(compact['unit_inventory']['count'],1000)
        self.assertLess(len(common.canonical_json(compact).encode()),500000)
        self.assertTrue(all('structure_sha256' in part for part in compact['parts']))


if __name__=='__main__':unittest.main()
