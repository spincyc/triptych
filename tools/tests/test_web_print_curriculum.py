from pathlib import Path
import re
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from _web_print_curriculum.core import CurriculumError, Packet, render_packet
from _print_document import select

M01 = 'publication:gpt/curriculums/ecclesiastical-latin/01-foundations/01-form-case-and-agreement'
M20 = 'publication:gpt/curriculums/ecclesiastical-latin/04-advanced/20-allusion-rhetoric-and-periodic-prose'


class CurriculumTableReceiptTests(unittest.TestCase):
    def setUp(self):
        self.packet=Packet(ROOT,select(M01,root=ROOT))

    def receipt(self, stderr, code=0):
        return self.packet.table_span_receipt(subprocess.CompletedProcess([],code,'',stderr))

    def test_empty_and_nonempty_typed_receipts(self):
        self.assertEqual(self.receipt('triptych-table-spans: \n'),{})
        self.assertEqual(self.receipt('triptych-table-spans: 2 4 2\n'),{2:2,4:1})

    def test_missing_duplicate_warning_and_nonzero_receipts_refuse(self):
        for stderr,code in [('',0),('triptych-table-spans:\n',0),
                ('triptych-table-spans: \ntriptych-table-spans: \n',0),
                ('triptych-table-spans: \n[WARNING] Arbitrary warning\n',0),
                ('triptych-table-spans: \n',1),('triptych-table-spans: 1\n',0)]:
            with self.subTest(stderr=stderr,code=code),self.assertRaises(CurriculumError):
                self.receipt(stderr,code)

    def test_final_span_inventory_must_match_even_when_empty(self):
        fragment='<table><tr><td colspan="2">Complete note</td></tr></table>'
        self.packet.validate_table_spans({2:1},fragment)
        for expected,rendered in [({},fragment),({2:1},fragment.replace(' colspan="2"','')),
                                  ({4:1},fragment)]:
            with self.subTest(expected=expected),self.assertRaisesRegex(CurriculumError,'spans changed'):
                self.packet.validate_table_spans(expected,rendered)


class CurriculumPacketPrintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipe=select(M01,root=ROOT)
        cls.product=render_packet(ROOT,cls.recipe)

    def test_exact_six_parts_in_order_and_no_extra_teaching(self):
        headings=[re.sub(r'<[^>]+>','',value) for value in re.findall(r'<h2[^>]*>(.*?)</h2>',self.product['html'])]
        self.assertEqual(headings,[
            'Teaching','Memory Work','Reading and Composition','Cumulative Practice','Answers and Models','Scope and Sources'])
        self.assertIn('Unit 1: From English Grammar to Latin Forms',self.product['html'])
        self.assertIn('Unit 2: Case, Number, Gender, and Agreement',self.product['html'])
        self.assertNotIn('Unit 3:',self.product['html'])

    def test_all_variants_and_exact_answer_order(self):
        sheets=self.product['selections']['worksheets']
        for mode in (False,True):
            selected=[row for row in sheets if row['solutions']==mode]
            self.assertEqual([row['variant'] for row in selected],list('ABCDABCD'))
            self.assertEqual([row['id'] for row in selected],['I.'+str(i) for i in range(1,9)])
        self.assertEqual(self.product['checks']['learner_items'],48)
        self.assertEqual(self.product['checks']['answer_items'],48)
        self.assertTrue(self.product['checks']['canonical_occurrence_order_payloads_match'])

    def test_semantic_tables_and_payloads(self):
        self.assertEqual(self.product['checks']['source_html_table_count'],11)
        self.assertEqual(self.product['checks']['lost_table_cell_openings'],[])
        self.assertNotIn('class="tabularx"',self.product['html'])
        self.assertIn('EL-I.1 EL-I.2',self.product['html'])

    def test_span_validation_follows_final_packet_normalization(self):
        original=Packet.normalize_profile
        def inject(packet,rendered):
            return re.sub(r'<td\b', '<td colspan="2"', original(packet,rendered), count=1)
        with patch.object(Packet,'normalize_profile',inject),self.assertRaisesRegex(CurriculumError,'spans changed'):
            render_packet(ROOT,self.recipe)

    def test_memory_fields_answers_rights_and_revision_retained(self):
        for text in ('vulpes, vulpis f.','Lemma and printed form','Reconstruction prompt.','Composition prompt.',
                     'Reuse and rights.','2026-08-27T22:42:04Z'):
            self.assertIn(text,self.product['html'])
        self.assertNotIn('AIModelContribution',self.product['html'])
        self.assertNotIn('AIGenerationProvenance',self.product['html'])

    def test_independent_provenance_and_selection_digest(self):
        self.assertEqual(len(self.product['expected_units']),10)
        self.assertEqual(len(self.product['expected_items']),96)
        for row in self.product['expected_units']:
            self.assertTrue(row['source'].startswith('src/gpt/curriculums/'))
            self.assertEqual(len(row['source_body_sha256']),64)
            self.assertIn(row['id'],row['occurrence_id'])
        self.assertEqual(len(self.product['selection_digest']),64)
        self.assertLess(len(self.product['parts'][0]['html'].encode()),750000)
        self.assertTrue(self.product['coverage_result']['complete'])
        self.assertEqual(self.product['coverage_result']['failures'],[])
        self.assertEqual(self.product['literal_coverage']['status'],'pass')
        self.assertEqual(self.product['literal_coverage']['missing_units'],[])
        self.assertGreater(self.product['literal_coverage']['kinds']['short-literal-unit'],0)
        self.assertNotIn('TRIPTYCHCURRICULUM',self.product['html'])

    def test_unknown_selected_macro_fails(self):
        packet=Packet(ROOT,self.recipe)
        original=packet.read
        def read(path):
            text=original(path)
            if str(path).endswith('/content/volume1/all.tex'):
                text=text.replace(r'\chapter{Unit 1:',r'\UndeclaredContent{Never lose this}\chapter{Unit 1:',1)
            return text
        with patch.object(packet,'read',side_effect=read),self.assertRaisesRegex(CurriculumError,'unknown macro'):
            packet.render()

    def test_unsupported_active_conditional_fails(self):
        packet=Packet(ROOT,self.recipe)
        with self.assertRaisesRegex(CurriculumError,'unsupported active conditional'):
            packet.eval(r'\ifunknownconditional active words\else other words\fi')

    def test_companion_not_silently_treated_as_packet(self):
        recipe=dict(self.recipe,edition='synthesis')
        with self.assertRaisesRegex(CurriculumError,'canonical GPT curriculum packets'):
            render_packet(ROOT,recipe)

    def test_advanced_packet_selected_content_and_answers(self):
        result=render_packet(ROOT,select(M20,root=ROOT))
        self.assertEqual(result['checks']['learner_items'],39)
        self.assertEqual(result['checks']['answer_items'],39)
        self.assertEqual(result['checks']['lost_table_cell_openings'],[])
        self.assertTrue(result['checks']['canonical_occurrence_order_payloads_match'])
        self.assertEqual(result['literal_coverage']['missing_units'],[])

    def mutated_product(self, fixture, drop):
        original_read=Path.read_text
        original_run=subprocess.run
        web=Packet(ROOT,self.recipe).web
        def read(path,*args,**kwargs):
            text=original_read(path,*args,**kwargs)
            if fixture=='item' and str(path).endswith('/shared/exercises/volume1/all.tex'):
                found=re.search(r'\\Exercise\s*\{',text)
                _,end=web.brace_group(text,found.end()-1)
                _,end=web.brace_group(text,web.skip_gap(text,end))
                return text[:found.start()]+r'\Exercise{Zed.}{Yup.}'+text[end:]
            if fixture=='registry' and str(path).endswith('/shared/memory/lexemes.tex'):
                return text.replace('{fox}','{Zed.}',1)
            if fixture in {'short-prose','unknown-environment'} and str(path).endswith('/shared/content/volume1/all.tex'):
                inserted=('Zed.\n\n'+r'\footnote{Yup.}'+'\n\n' if fixture=='short-prose' else
                          r'\begin{unmodelledinstructions}Keep this instruction.\end{unmodelledinstructions}')
                return text.replace(r'\begin{courseunit}{I.1}',r'\begin{courseunit}{I.1}'+'\n'+inserted,1)
            return text
        def run(*args,**kwargs):
            result=original_run(*args,**kwargs)
            if Path(args[0][0]).name=='pandoc':
                result.stdout=result.stdout.replace(drop,'')
            return result
        with patch.object(Path,'read_text',read),patch('_web_print_curriculum.core.subprocess.run',side_effect=run):
            return render_packet(ROOT,self.recipe)

    def test_short_prompt_drop_is_refused(self):
        with self.assertRaisesRegex(CurriculumError,'prompt/answer payload shortfall'):
            self.mutated_product('item','Zed.')

    def test_short_answer_drop_is_refused(self):
        with self.assertRaisesRegex(CurriculumError,'prompt/answer payload shortfall'):
            self.mutated_product('item','Yup.')

    def test_short_registry_drop_is_refused(self):
        with self.assertRaisesRegex(CurriculumError,'table cell payload lost|registry payload shortfall'):
            self.mutated_product('registry','Zed.')

    def test_unknown_environment_cannot_hide_instructions(self):
        with self.assertRaisesRegex(CurriculumError,'unknown environment unmodelledinstructions'):
            self.mutated_product('unknown-environment','Keep this instruction.')

    def test_short_paragraph_drop_marks_coverage_refused(self):
        with self.assertRaisesRegex(CurriculumError,'complete curriculum semantic') as failed:
            self.mutated_product('short-prose','Zed.')
        self.assertTrue(any(row.get('expected')=='zed' for row in failed.exception.coverage['failures']))

    def test_short_note_drop_marks_coverage_refused(self):
        with self.assertRaisesRegex(ValueError,'complete curriculum semantic|output hyperlink has no visible containing content unit') as failed:
            self.mutated_product('short-prose','Yup.')
        if hasattr(failed.exception,'coverage'):
            self.assertTrue(any(row.get('kind')=='note' and row.get('expected')=='yup' for row in failed.exception.coverage['failures']))

    def test_invented_output_instruction_is_refused(self):
        original=Packet.pandoc_html
        def invent(packet,*args):
            result=original(packet,*args);result.stdout+='<p>An invented instruction.</p>';return result
        with patch.object(Packet,'pandoc_html',invent),self.assertRaisesRegex(CurriculumError,'complete curriculum semantic') as failed:
            render_packet(ROOT,self.recipe)
        self.assertTrue(any(row['kind']=='unexpected-output-block' for row in failed.exception.coverage['failures']))

    def test_reordered_cover_blocks_are_refused(self):
        original=Packet.pandoc_html
        def reorder(packet,*args):
            result=original(packet,*args)
            first='<p><strong>Ecclesiastical Latin</strong></p>'
            second='<p><strong>EL-M01: Form, Case, and Agreement</strong></p>'
            result.stdout=result.stdout.replace(first,'COVERBLOCKSWAP',1).replace(second,first,1).replace('COVERBLOCKSWAP',second,1)
            return result
        with patch.object(Packet,'pandoc_html',reorder),self.assertRaisesRegex(CurriculumError,'complete curriculum semantic'):
            render_packet(ROOT,self.recipe)

    def test_supplemental_formulary_selections_remain_exact(self):
        specs=[('03-missal-reading/18-holy-week-requiem-and-complete-mass',
                ['MR62-FORM-ADV1','MR62-FORM-PENT','MR62-FORM-XII-PENT','MR62-FORM-XXIII-PENT']),
               ('04-advanced/21-collation-and-controlled-imitation',['MR62-FORM-XII-PENT']),
               ('04-advanced/22-guided-composition-and-independent-research',['MR62-FORM-XXIII-PENT'])]
        for leaf,wanted in specs:
            result=render_packet(ROOT,select('publication:gpt/curriculums/ecclesiastical-latin/'+leaf,root=ROOT))
            self.assertTrue(result['coverage_result']['complete'])
            self.assertEqual(result['selections']['contract']['supplemental_review_sources'],wanted)
            for mode in (False,True):
                actual=[row['id'] for row in result['selections']['units'] if row['solutions']==mode and row['id'].startswith('MR62-')]
                self.assertEqual(actual,wanted)

    def test_inline_arrow_glyph_deletion_is_refused(self):
        original=Packet.postprocess_html
        def drop(packet,rendered):
            return original(packet,rendered).replace('<mo>→</mo>','<mo></mo>',1)
        identity='publication:gpt/curriculums/ecclesiastical-latin/01-foundations/02-noun-systems'
        with patch.object(Packet,'postprocess_html',drop),self.assertRaisesRegex(CurriculumError,'complete curriculum semantic'):
            render_packet(ROOT,select(identity,root=ROOT))

    def test_public_metadata_excludes_full_source_ledgers(self):
        from _web_print_curriculum import compact_product_metadata
        import json
        metadata=compact_product_metadata(self.product)
        self.assertLess(len(json.dumps(metadata).encode()),4000)
        self.assertNotIn('expected_units',metadata)
        self.assertNotIn('semantic_ledger',metadata)
        self.assertEqual(metadata['coverage_result']['unit_count'],self.product['coverage_result']['unit_count'])
        self.assertNotIn('html',metadata['parts'][0])

    def test_verified_official_renderer_and_no_inline_styles(self):
        from _web_print_curriculum.core import OFFICIAL_PANDOC_SHA256
        self.assertEqual(self.product['render_toolchain']['sha256'],OFFICIAL_PANDOC_SHA256)
        self.assertTrue(self.product['html_profile']['input_styles'])
        self.assertNotRegex(self.product['html'],r'\sstyle\s*=|<style\b')
        for part in self.product['parts']:
            self.assertNotRegex(part['html'],r'\sstyle\s*=|<style\b')

    def test_unknown_inline_style_is_refused_before_admission(self):
        original=Packet.postprocess_html
        def inject(packet,rendered):
            return original(packet,rendered).replace('<p>','<p style="display:none">',1)
        with patch.object(Packet,'postprocess_html',inject),self.assertRaisesRegex(ValueError,'untyped.*print style'):
            render_packet(ROOT,self.recipe)


"""Companion tests to merge into the production curriculum test module."""
from pathlib import Path
import hashlib
import re
import sys
import unittest
from unittest.mock import patch

COMPANION_TEST_ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(COMPANION_TEST_ROOT/'scripts'))
from _print_document import select as select_companion_recipe
from _web_print_curriculum.companions import (
    Companion as CurriculumCompanion,
    CurriculumError as CurriculumCompanionError,
    render_companion as render_curriculum_companion,
)
from _web_print_curriculum.core import OFFICIAL_PANDOC_SHA256 as COMPANION_OFFICIAL_PANDOC_SHA256


def companion_recipe(name):return select_companion_recipe('publication:gpt/curriculums/ecclesiastical-latin/'+name,root=COMPANION_TEST_ROOT)


class CurriculumCompanionTests(unittest.TestCase):
    def test_span_validation_follows_final_companion_normalization(self):
        original=CurriculumCompanion.normalize_profile
        def drop(companion,rendered):
            return re.sub(r' colspan="[2-9][0-9]*"','',original(companion,rendered),count=1)
        with patch.object(CurriculumCompanion,'normalize_profile',drop),self.assertRaisesRegex(CurriculumError,'spans changed'):
            render_curriculum_companion(COMPANION_TEST_ROOT,companion_recipe('00-reference-grammar'))

    @classmethod
    def setUpClass(cls):
        cls.guide=render_curriculum_companion(COMPANION_TEST_ROOT,companion_recipe('00-course-guide'))
        cls.reference=render_curriculum_companion(COMPANION_TEST_ROOT,companion_recipe('00-reference-grammar'))
        cls.memory=render_curriculum_companion(COMPANION_TEST_ROOT,companion_recipe('00-memory-workbook'))

    def test_complete_guide_source_and_forms(self):
        result=self.guide
        self.assertTrue(result['coverage_result']['complete'])
        self.assertEqual(result['checks']['guide_forms'],24)
        self.assertEqual(result['checks']['tables'],47)
        self.assertEqual(result['checks']['lost_table_openings'],[])

    def test_complete_reference_all_lexemes_and_fields(self):
        result=self.reference
        self.assertTrue(result['coverage_result']['complete'])
        self.assertEqual(result['checks']['registry_field_occurrences'],598*6)
        self.assertIn('L001',result['rendered'])
        self.assertIn('L598',result['rendered'])
        self.assertNotIn('TRIPTYCHSPANCELL',result['rendered'])

    def test_complete_workbook_all_sets_sheets_fields_and_modes(self):
        result=self.memory
        self.assertTrue(result['coverage_result']['complete'])
        self.assertEqual(result['checks']['workbook_packet_views'],60)
        self.assertEqual(result['checks']['workbook_sheet_views'],480)
        self.assertEqual(result['checks']['registry_field_occurrences'],19928)
        self.assertEqual(result['checks']['tables'],363)
        self.assertIn('M01-S',result['rendered'])
        self.assertIn('P8-COMP',result['rendered'])
        self.assertNotEqual(result['selection_digest'],result['selector_digest'])

    def test_parts_preserve_all_content_and_order(self):
        for result in (self.guide,self.reference,self.memory):
            self.assertEqual(''.join(part['html'] for part in result['parts']),result['rendered'])
            self.assertTrue(all(len(part['html'].encode())<750000 for part in result['parts']))
            self.assertNotRegex(result['rendered'],r'\sstyle\s*=')
            self.assertEqual(result['render_toolchain']['sha256'],COMPANION_OFFICIAL_PANDOC_SHA256)
            self.assertEqual(result['print_binding']['output_sha256'],hashlib.sha256(result['rendered'].encode()).hexdigest())
            self.assertEqual(result['html_profile']['output_sha256'],result['print_binding']['input_sha256'])
            for part in result['parts']:
                self.assertEqual(part['sha256'],hashlib.sha256(part['html'].encode()).hexdigest())
                self.assertEqual(part['bytes'],len(part['html'].encode()))

    def test_canonical_revision_rights_without_internal_contributors(self):
        for result in (self.guide,self.reference,self.memory):
            self.assertIn('Last revised (UTC):',result['rendered'])
            self.assertIn('Reuse and rights.',result['rendered'])
            self.assertNotIn('AIModelContribution',result['rendered'])
            self.assertNotIn('AIGenerationProvenance',result['rendered'])

    def test_short_table_cell_deletion_is_refused(self):
        original=CurriculumCompanion.postprocess_html
        def drop(converter,text):
            text=original(converter,text)
            return re.sub(r'(<t[dh][^>]*>)Date(</t[dh]>)',r'\1\2',text,count=1)
        with patch.object(CurriculumCompanion,'postprocess_html',drop),self.assertRaises(CurriculumCompanionError):
            render_curriculum_companion(COMPANION_TEST_ROOT,companion_recipe('00-course-guide'))

    def test_known_macro_instruction_drop_is_refused(self):
        original=CurriculumCompanion.custom_command
        def drop(converter,name,text,pos,depth):
            if name=='StudyLoop':return '',pos
            return original(converter,name,text,pos,depth)
        with patch.object(CurriculumCompanion,'custom_command',drop),self.assertRaisesRegex(CurriculumCompanionError,'semantic source coverage failed'):
            render_curriculum_companion(COMPANION_TEST_ROOT,companion_recipe('00-course-guide'))

    def test_reordered_complete_paragraphs_are_refused(self):
        original=CurriculumCompanion.postprocess_html
        def reorder(converter,text):
            text=original(converter,text)
            found=list(re.finditer(r'<p\b[^>]*>.*?</p>',text,re.S))
            a,b=found[:2]
            return text[:a.start()]+b.group()+text[a.end():b.start()]+a.group()+text[b.end():]
        with patch.object(CurriculumCompanion,'postprocess_html',reorder),self.assertRaisesRegex(CurriculumCompanionError,'semantic source coverage failed'):
            render_curriculum_companion(COMPANION_TEST_ROOT,companion_recipe('00-course-guide'))

    def test_duplicate_known_paragraph_is_refused(self):
        original=CurriculumCompanion.postprocess_html
        def duplicate(converter,text):
            text=original(converter,text);first=re.search(r'<p\b[^>]*>.*?</p>',text,re.S)
            return text[:first.end()]+first.group()+text[first.end():]
        with patch.object(CurriculumCompanion,'postprocess_html',duplicate),self.assertRaisesRegex(CurriculumCompanionError,'semantic source coverage failed'):
            render_curriculum_companion(COMPANION_TEST_ROOT,companion_recipe('00-course-guide'))

    def test_lost_minipage_boundary_is_refused(self):
        original=CurriculumCompanion.postprocess_html
        def drop(converter,text):return re.sub(r' data-semantic-minipage="[^"]+"','',original(converter,text),count=1)
        with patch.object(CurriculumCompanion,'postprocess_html',drop),self.assertRaisesRegex(CurriculumCompanionError,'semantic source coverage failed'):
            render_curriculum_companion(COMPANION_TEST_ROOT,companion_recipe('00-course-guide'))

    def test_unknown_environment_cannot_hide_instruction(self):
        original=CurriculumCompanion.read
        def inject(converter,path):
            text=original(converter,path)
            if str(path).endswith('/content/00-using-the-course.tex'):
                text += r'\begin{unmodelledinstructions}Read every word.\end{unmodelledinstructions}'
            return text
        with patch.object(CurriculumCompanion,'read',inject),self.assertRaisesRegex(CurriculumCompanionError,'unknown environment'):
            render_curriculum_companion(COMPANION_TEST_ROOT,companion_recipe('00-course-guide'))

    def test_identity_cannot_name_another_companions_source(self):
        value=companion_recipe('00-course-guide');value['id']=companion_recipe('00-reference-grammar')['id']
        with self.assertRaisesRegex(CurriculumCompanionError,'identity and canonical entrypoint disagree'):
            render_curriculum_companion(COMPANION_TEST_ROOT,value)

    def test_arbitrary_style_is_refused(self):
        original=CurriculumCompanion.postprocess_html
        def inject(converter,text):return original(converter,text)+'<p style="color: red">Unexpected styling.</p>'
        with patch.object(CurriculumCompanion,'postprocess_html',inject),self.assertRaisesRegex(CurriculumCompanionError,'untyped companion HTML style'):
            render_curriculum_companion(COMPANION_TEST_ROOT,companion_recipe('00-course-guide'))

    def test_wrong_pandoc_binary_is_refused(self):
        with patch('_web_print_curriculum.core.shutil.which',return_value=sys.executable),self.assertRaisesRegex(CurriculumCompanionError,'verified official Pandoc binary'):
            render_curriculum_companion(COMPANION_TEST_ROOT,companion_recipe('00-course-guide'))



from pathlib import Path
import hashlib
import re
import subprocess
import unittest
from unittest.mock import patch

from _web_print_curriculum import assessments as assessment_print_module
from _web_print_curriculum.assessments import (
    Assessment as AssessmentPrintAdapter,
    CurriculumError as AssessmentPrintError,
    render_assessment as render_assessment_print,
)
from _print_document import select

# This fragment is merged into tools/tests/test_web_print_curriculum.py.
ASSESSMENT_ROOT = Path(__file__).resolve().parents[2]
ASSESSMENT_PREFIX='publication:gpt/curriculums/ecclesiastical-latin/05-stage-assessments/'
ASSESSMENT_NAMES=('01-foundations','02-core-grammar','03-missal-reading','04-advanced')


class CurriculumAssessmentPrintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipes={name:select(ASSESSMENT_PREFIX+name,root=ASSESSMENT_ROOT) for name in ASSESSMENT_NAMES}
        cls.products={name:render_assessment_print(ASSESSMENT_ROOT,recipe) for name,recipe in cls.recipes.items()}

    def test_all_four_have_complete_source_coverage(self):
        for name,product in self.products.items():
            with self.subTest(name=name):
                self.assertEqual(product['coverage_result']['status'],'pass')
                self.assertTrue(product['coverage_result']['complete'])
                self.assertEqual(product['coverage_result']['failures'],[])
                self.assertEqual(len(product['expected_units']),product['coverage_result']['unit_count'])
                self.assertLess(max(len(part['html'].encode()) for part in product['parts']),750000)
                self.assertEqual(product['render_toolchain']['sha256'],'870b811354a230a1864dd2b50dec3b850a981926ff4659ae460aea96ab6b8d28')
                self.assertNotRegex(''.join(part['html'] for part in product['parts']),r'\bstyle\s*=')

    def test_exact_selected_forms_and_source_item_namespaces(self):
        for name,ids,count in zip(ASSESSMENT_NAMES,(('F-A','F-B'),('C-A','C-B'),('M-A','M-B','M-C'),('A-A','A-B')),(82,76,72,36)):
            product=self.products[name]
            for mode in (False,True):
                self.assertEqual([row['id'] for row in product['assessment_forms'] if row['solutions']==mode],list(ids))
            self.assertEqual(len(product['expected_items']),count)
            self.assertTrue(all(row['id'].split('.')[0] in ids for row in product['expected_items']))

    def test_included_latin_is_exact_and_not_whole_course(self):
        self.assertEqual(self.products[ASSESSMENT_NAMES[0]]['expected_source_occurrences'],[])
        self.assertEqual(self.products[ASSESSMENT_NAMES[1]]['expected_source_occurrences'],[])
        self.assertEqual([row['id'] for row in self.products[ASSESSMENT_NAMES[2]]['expected_source_occurrences']],
            ['MR62-FORM-ADV1','MR62-FORM-PENT','MR62-FORM-XII-PENT','MR62-FORM-XXIII-PENT'])
        self.assertEqual([row['id'] for row in self.products[ASSESSMENT_NAMES[3]]['expected_source_occurrences']],
            ['MR62-FORM-XII-PENT','MR62-FORM-XXIII-PENT','M19','M20','M21','M22'])

    def test_protocol_rubric_and_comparison_sources_preserved(self):
        value=self.products['04-advanced']['html']
        for words in ('Advanced composition points to inspect','Course-built transcription and collation sets',
                      'A2, course-built comparison reading.','B2, course-built comparison reading.',
                      'Borrowed language','Reuse and rights.'):
            self.assertIn(words.casefold(),value.casefold())

    def test_source_response_dimensions_and_prefix_markers(self):
        body=self.products['01-foundations']['parts'][0]['html']
        first_ten=re.search(r'Item ID: F-A\.10(.*?)</li>',body,re.S).group(1)
        self.assertIn('class="response-space response-block-065"',first_ten)
        self.assertNotIn('</span>0',first_ten)
        self.assertIn('class="response-space response-block-100"',body)
        self.assertNotRegex(body,r'\bstyle\s*=')
        self.assertNotIn('TRIPTYCH',body)

    def test_source_keep_together_containers_preserved(self):
        for product in self.products.values():
            source=[row['id'] for row in product['semantic_ledger']['containers']]
            actual=re.findall(r'data-semantic-minipage="([^"]+)"',product['parts'][0]['html'])
            self.assertEqual(actual,source)
            self.assertEqual(len(actual),len(product['expected_items']))

    def mutate_output(self,change):
        original=subprocess.run
        def run(*args,**kwargs):
            result=original(*args,**kwargs)
            if Path(args[0][0]).name=='pandoc' and '-f' in args[0]:result.stdout=change(result.stdout)
            return result
        with patch.object(assessment_print_module.core.subprocess,'run',side_effect=run):
            return render_assessment_print(ASSESSMENT_ROOT,self.recipes['01-foundations'])

    def test_short_prompt_drop_refused(self):
        with self.assertRaisesRegex(AssessmentPrintError,'prompt/answer payload shortfall'):
            self.mutate_output(lambda html:html.replace('<em>sanctarum</em>','',1))

    def test_answer_tail_drop_refused(self):
        with self.assertRaisesRegex(AssessmentPrintError,'prompt/answer payload shortfall'):
            self.mutate_output(lambda html:html.replace('they were coming.','',1))

    def test_template_protocol_paragraph_drop_refused(self):
        with self.assertRaisesRegex(AssessmentPrintError,'semantic.*coverage.*(?:refused|failed)'):
            self.mutate_output(lambda html:re.sub(r'<p>Each companion offers parallel forms.*?</p>','',html,count=1,flags=re.S))

    def test_reordered_items_refused(self):
        def move(html):
            rows=list(re.finditer(r'<li>.*?</li>',html,re.S))
            a,b=rows[:2]
            return html[:a.start()]+b.group()+html[a.end():b.start()]+a.group()+html[b.end():]
        with self.assertRaisesRegex(AssessmentPrintError,'semantic.*coverage.*(?:refused|failed)'):
            self.mutate_output(move)

    def test_unowned_output_prose_refused(self):
        with self.assertRaisesRegex(AssessmentPrintError,'semantic.*coverage.*(?:refused|failed)'):
            self.mutate_output(lambda html:html+'<p>Unowned invented prose.</p>')

    def test_unknown_environment_instruction_refused(self):
        original=AssessmentPrintAdapter.read
        def read(instance,path):
            value=original(instance,path)
            if str(path).endswith('/shared/assessments/protocol.tex'):
                value+='\n'+r'\begin{hiddeninstructions}Keep this.\end{hiddeninstructions}'+'\n'
            return value
        with patch.object(AssessmentPrintAdapter,'read',read),self.assertRaisesRegex(AssessmentPrintError,'unknown environment'):
            render_assessment_print(ASSESSMENT_ROOT,self.recipes['01-foundations'])

    def test_short_template_note_drop_refused(self):
        suffix='\n\nMicro.\\footnote{Amen.}\n\n'
        original_read=AssessmentPrintAdapter.read
        original_run=subprocess.run
        def read(instance,path):
            value=original_read(instance,path)
            if str(path).endswith('/shared/assessments/protocol.tex'):
                raw=Path(path).read_text()+suffix
                instance.sources[Path(path).resolve().relative_to(instance.root).as_posix()]=hashlib.sha256(raw.encode()).hexdigest()
                return instance.web.strip_tex_comments(raw)
            return value
        def project(instance,module):
            source=module.CanonicalProjector(instance.root,instance.recipe,instance.web)
            original=source.source
            def fixture(path):
                value=original(path)
                if str(path).endswith('/shared/assessments/protocol.tex'):
                    source.sources[Path(path).resolve()]+=suffix
                    value+=suffix
                return value
            source.source=fixture
            return source.run()
        def run(*args,**kwargs):
            value=original_run(*args,**kwargs)
            if Path(args[0][0]).name=='pandoc' and '-f' in args[0]:value.stdout=value.stdout.replace('Amen.','')
            return value
        with patch.object(AssessmentPrintAdapter,'read',read),patch.object(AssessmentPrintAdapter,'canonical_projection',project),patch.object(assessment_print_module.core.subprocess,'run',side_effect=run),self.assertRaisesRegex(ValueError,'semantic.*coverage.*(?:refused|failed)|output hyperlink has no visible containing content unit'):
            render_assessment_print(ASSESSMENT_ROOT,self.recipes['01-foundations'])


from collections import Counter as PoetryCounter
from pathlib import Path as PoetryPath
import re as poetry_re
import unittest as poetry_unittest

from _web_print_curriculum.poetry import (
    PoetryPacket as ProductionPoetryPacket,
    CurriculumError as ProductionPoetryCurriculumError,
    ScansionError as ProductionPoetryScansionError,
    ScansionParser as ProductionPoetryScansionParser,
    ast_signature as poetry_ast_signature,
    render_ast as poetry_render_ast,
    render_packet as poetry_render_packet,
    verify_math_units as poetry_verify_math_units,
    verify_windows as poetry_verify_windows,
)
import _web_print_semantics as poetry_semantic_coverage

POETRY_TEST_ROOT=next(parent for parent in PoetryPath(__file__).resolve().parents
                      if (parent/'tmt.json').is_file() and (parent/'src/common/preamble.tex').is_file())
from _print_document import select as poetry_select


def poetry_source_schemes():
    source=(POETRY_TEST_ROOT/'src/gpt/curriculums/ecclesiastical-latin/shared/content/poetry-advanced/all.tex').read_text()
    return [found[1] for found in poetry_re.finditer(r'\\\[(.*?)\\\]',source,poetry_re.S)]


class CurriculumScansionProductionTests(poetry_unittest.TestCase):
    def test_all_three_canonical_schemes_have_exact_signatures(self):
        schemes=poetry_source_schemes();self.assertEqual(len(schemes),3)
        for source in schemes:
            ast=ProductionPoetryScansionParser(source).parse()
            math='<math display="block" data-semantic-unit="test">'+poetry_render_ast(ast)+'</math>'
            expected={'test':{'expected_mathml_signature':poetry_ast_signature(ast)}}
            self.assertEqual(poetry_verify_math_units(math,expected)['status'],'pass')

    def test_senarius_all_short_long_anceps_and_bar_tokens(self):
        signature=poetry_ast_signature(ProductionPoetryScansionParser(poetry_source_schemes()[0]).parse())
        tokens=PoetryCounter(row[1] for row in signature if row[0]=='text')
        self.assertEqual(tokens,PoetryCounter({'⌣':6,'–':5,'∣':3,'‖':2,'×':1,'.':1}))

    def test_hexameter_nested_text_math_retains_every_quantity(self):
        signature=poetry_ast_signature(ProductionPoetryScansionParser(poetry_source_schemes()[1]).parse())
        text=''.join(row[1] for row in signature if row[0]=='text')
        self.assertEqual(text.count('–'),8)
        self.assertEqual(text.count('⌣'),6)
        self.assertEqual(text.count('|'),5)
        self.assertEqual(text.count('×'),1)

    def test_choriamb_labels_and_underbrace_grouping_are_complete(self):
        signature=poetry_ast_signature(ProductionPoetryScansionParser(poetry_source_schemes()[2]).parse())
        labels=[row[1] for row in signature if row[0]=='text' and row[1].startswith(('opening','choriamb'))]
        self.assertEqual(labels,['opening base','choriamb 1','choriamb 2','choriamb 3'])
        self.assertEqual(signature.count(['start','munder']),8)

    def test_unknown_math_controls_refuse_before_render(self):
        with self.assertRaisesRegex(ProductionPoetryScansionError,'unsupported scansion control'):
            ProductionPoetryScansionParser(r'\smile\secretmeaning{kept instruction}').parse()


class CurriculumPoetryProductionPacketTests(poetry_unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.products={}
        for entry in sorted((POETRY_TEST_ROOT/'src/gpt/curriculums/ecclesiastical-latin/04-advanced/poetry').glob('*/main.tex')):
            identity='publication:gpt/'+entry.parent.relative_to(POETRY_TEST_ROOT/'src/gpt').as_posix()
            cls.products[entry.parent.name]=poetry_render_packet(POETRY_TEST_ROOT,poetry_select(identity,root=POETRY_TEST_ROOT))

    def test_all_eight_exact_selected_packet_outputs_render(self):
        self.assertEqual(len(self.products),8)
        for leaf,product in self.products.items():
            with self.subTest(leaf=leaf):
                self.assertEqual(product['math_coverage']['status'],'pass')
                self.assertTrue(product['coverage_result']['complete'])
                self.assertEqual(product['coverage_result']['failures'],[])
                self.assertEqual(product['source_windows']['coverage']['status'],'pass')
                self.assertEqual(product['checks']['prompt_answer_payload_shortfalls'],[])
                self.assertEqual(product['checks']['registry_payload_shortfalls'],[])
                self.assertNotIn('TRIPTYCHPOETRY',product['html'])
                self.assertEqual(product['render_toolchain']['sha256'],'870b811354a230a1864dd2b50dec3b850a981926ff4659ae460aea96ab6b8d28')
                for part in product['parts']:
                    self.assertNotRegex(part['html'],r'\sstyle\s*=')
                if product['source_windows']['occurrences']:
                    self.assertIn('class="poetry-verse-line"',product['html'])
                for mode in (False,True):
                    self.assertEqual([row['variant'] for row in product['selections']['worksheets'] if row['solutions']==mode],list('ABCD'))

    def test_math_symbol_drop_refuses(self):
        product=self.products['01-textual-prosody']
        damaged=product['html'].replace('<mo>⌣</mo>','',1)
        with self.assertRaisesRegex(ProductionPoetryScansionError,'signature changed'):
            poetry_verify_math_units(damaged,product['semantic_units'])

    def test_independent_raw_source_math_change_or_drop_refuses(self):
        identity='publication:gpt/curriculums/ecclesiastical-latin/04-advanced/poetry/01-textual-prosody'
        packet=ProductionPoetryPacket(POETRY_TEST_ROOT,poetry_select(identity,root=POETRY_TEST_ROOT));packet.independent_plan()
        source=next(iter(packet.semantic_units.values()))['source_tex']
        projection,units=packet.canonical_semantic_projection(source)
        self.assertIn(r'\SemanticMathUnit{',projection)
        self.assertEqual(len(units),1)
        with self.assertRaisesRegex(ProductionPoetryScansionError,'unplanned math display'):
            packet.canonical_semantic_projection(source.replace(r'\smile',r'\times',1))
        with self.assertRaisesRegex(ProductionPoetryScansionError,'order or count differs'):
            packet.canonical_semantic_projection('')

    def test_complete_source_gate_refuses_reordered_cover_paragraphs(self):
        class Reordered(ProductionPoetryPacket):
            def postprocess_html(self,rendered):
                rendered=super().postprocess_html(rendered)
                return poetry_re.sub(r'(<p>.*?</p>)(\s*)(<p>.*?</p>)',r'\3\2\1',rendered,count=1,flags=poetry_re.S)
        identity='publication:gpt/curriculums/ecclesiastical-latin/04-advanced/poetry/01-textual-prosody'
        with self.assertRaisesRegex(ProductionPoetryCurriculumError,'complete curriculum semantic source coverage failed'):
            Reordered(POETRY_TEST_ROOT,poetry_select(identity,root=POETRY_TEST_ROOT)).render()

    def test_math_group_label_reordering_refuses(self):
        product=self.products['04-lyric-meters']
        damaged=product['html'].replace('choriamb 1','choriamb TEMP').replace('choriamb 2','choriamb 1').replace('choriamb TEMP','choriamb 2')
        with self.assertRaisesRegex(ProductionPoetryScansionError,'signature changed'):
            poetry_verify_math_units(damaged,product['semantic_units'])

    def test_unknown_mathml_group_refuses(self):
        product=self.products['01-textual-prosody']
        damaged=product['html'].replace('<mo>⌣</mo>','<annotation>⌣</annotation>',1)
        with self.assertRaisesRegex(ProductionPoetryScansionError,'unsupported rendered MathML tag'):
            poetry_verify_math_units(damaged,product['semantic_units'])

    def test_short_received_window_amen_drop_refuses(self):
        product=self.products['06-rhythmic-hymnody-and-sequences']
        damaged=product['html'].replace('gaudium. Amen. Alleluia.','gaudium. Alleluia.',1)
        self.assertNotEqual(damaged,product['html'])
        with self.assertRaisesRegex(ProductionPoetryScansionError,'words, lineation, grouping or order changed'):
            poetry_verify_windows(damaged,product['source_windows']['occurrences'],product['expected_print_units'])

    def test_source_window_line_order_cannot_change(self):
        product=self.products['02-hexameter']
        lines=product['source_windows']['occurrences'][0]['lines']
        damaged=product['html'].replace(lines[0],'WINDOWTEMP').replace(lines[1],lines[0]).replace('WINDOWTEMP',lines[1])
        with self.assertRaisesRegex(ProductionPoetryScansionError,'words, lineation, grouping or order changed'):
            poetry_verify_windows(damaged,product['source_windows']['occurrences'],product['expected_print_units'])

    def test_received_window_print_markers_must_be_empty_and_closed(self):
        product=self.products['01-textual-prosody'];start=product['html'].index('data-poetry-window="1"')
        marker=poetry_re.search(r'<span data-print-unit="[^"]+"></span>',product['html'][start:]).group()
        variants=[marker.replace('></span>','>Invented.</span>'),
                  marker.replace('></span>','><em></em></span>'),
                  marker.replace('></span>','><!--comment--></span>'),
                  marker.replace('></span>','/>')]
        for replacement in variants:
            with self.subTest(replacement=replacement),self.assertRaisesRegex(ProductionPoetryScansionError,'print marker must be empty|print marker must close explicitly'):
                poetry_verify_windows(product['html'].replace(marker,replacement,1),product['source_windows']['occurrences'],product['expected_print_units'])

    def test_received_window_print_marker_requires_its_source_identity(self):
        product=self.products['01-textual-prosody'];start=product['html'].index('data-poetry-window="1"')
        marker=poetry_re.search(r'<span data-print-unit="[^"]+"></span>',product['html'][start:]).group()
        damaged=product['html'].replace(marker,'<span data-print-unit="unowned-marker"></span>',1)
        with self.assertRaisesRegex(ProductionPoetryScansionError,'exact canonical identity'):
            poetry_verify_windows(damaged,product['source_windows']['occurrences'],product['expected_print_units'])

    def test_semantic_ledger_compares_math_subtree_not_word_count(self):
        product=self.products['01-textual-prosody'];ident=next(iter(product['semantic_units']));unit=product['semantic_units'][ident]
        ledger={'units':[{'id':'math-1','occurrence_id':ident,'kind':'math','lane':'body','source_ref':unit['source_ref'],
                         'expected':'','expected_mathml_signature':unit['expected_mathml_signature']}],
                'links':[],'containers':[],'macro_state_digest':'test','ledger_digest':'test','navigation_allowed':False}
        math='<math display="block" data-semantic-unit="'+ident+'">'+poetry_render_ast(unit['ast'])+'</math>'
        self.assertTrue(poetry_semantic_coverage.check_units(ledger,math)['complete'])
        damaged=math.replace('<mo>⌣</mo>','',1)
        self.assertFalse(poetry_semantic_coverage.check_units(ledger,damaged)['complete'])



class CurriculumPublicationPrintApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from _web_print_curriculum import render_publication
        cls.product=render_publication(ROOT,'gpt',M01)

    def test_exact_namespace_and_curriculum_subtype(self):
        from _web_print_curriculum import render_publication
        self.assertEqual(self.product['output_id'],M01)
        self.assertEqual(self.product['print_type'],'curriculum')
        self.assertEqual(self.product['subtype'],'curriculum-packet')
        relative=M01.removeprefix('publication:gpt/')
        again=render_publication(ROOT,'gpt',relative)
        self.assertEqual(again['source_digest'],self.product['source_digest'])
        self.assertEqual(again['selection_digest'],self.product['selection_digest'])

    def test_canonical_product_has_no_workspace_paths(self):
        import json
        self.assertNotIn(str(ROOT),json.dumps(self.product))
        self.assertTrue(all(not Path(path).is_absolute() for path in self.product['source_paths']))
        self.assertTrue(self.product['coverage_result']['complete'])

    def test_every_print_unit_identity_reaches_the_final_dom(self):
        from html.parser import HTMLParser
        class Units(HTMLParser):
            def __init__(self):super().__init__();self.identifiers=[]
            def handle_starttag(self,tag,attrs):
                for name,value in attrs:
                    if name=='data-print-unit':self.identifiers.append(value)
        parser=Units()
        for part in self.product['parts']:parser.feed(part['html'])
        self.assertEqual(parser.identifiers,self.product['expected_print_units'])
        self.assertEqual(len(parser.identifiers),len(set(parser.identifiers)))
        self.assertGreaterEqual(len(parser.identifiers),self.product['coverage_result']['unit_count'])

    def test_dispatch_refuses_non_curriculum_owner(self):
        from _web_print_curriculum import render_publication
        with patch('_print_document.publication_recipe',return_value={'canonical':'articles/other'}):
            with self.assertRaisesRegex(CurriculumError,'outside the canonical curriculum owner'):
                render_publication(ROOT,'gpt','articles/other')


class CurriculumResponseGeometryTests(unittest.TestCase):
    def fixtures(self):
        records=[]
        def add(kind,origin,height,width,lines,rule,macro):
            records.append(dict(id='response-'+str(len(records)+1),kind=kind,origin=origin,height=height,width=width,lines=lines,rule=rule,macro=macro))
        add('inline-rule','Blank','0.4pt','1.3in',1,'0.4pt','Blank')
        add('inline-rule','LongBlank','0.4pt','2.6in',1,'0.4pt','LongBlank')
        add('inline-rule','hrulefill','0pt','fill',1,'hrulefill','hrulefill')
        add('blank-cell','memory@blankcell',r'2.2\baselineskip','linewidth',1,'hrulefill','memory@blankcell')
        add('ruled-lines','memory@twolines',r'1.1\baselineskip','linewidth',2,'hrulefill','memory@twolines')
        add('ruled-lines','memory@fourlines',r'1.1\baselineskip','linewidth',4,'hrulefill','memory@fourlines')
        for origin,height in [('ShortExercise','0.22in'),('Exercise','0.38in'),('Exercise','0.7in'),('LongExercise','0.9in'),('PassageExercise','1.15in'),('AssessmentItem','0.65in'),('AssessmentItem','0.8in'),('AssessmentItem','1.0in'),('AssessmentItem','1.1in'),('AssessmentItem','1.2in'),('AssessmentItem','1.3in'),('AssessmentItem','1.4in'),('RuleLine','0.22in'),('vspace',r'1.1\baselineskip')]:
            primitive='hrule' if origin=='RuleLine' else 'hrulefill'
            add('response-block',origin,height,'linewidth',1,primitive,primitive)
        for height in ['0.5in','0.52in','0.55in','0.62in','0.65in','0.72in','0.76in','0.78in','0.82in']:
            add('table-row-space','rule',height,'0pt',0,'none','rule')
        return records

    def test_all_canonical_variants_preserve_exact_source_signatures(self):
        from _web_print_curriculum.response_geometry import render,check
        events=self.fixtures();fragment=''.join(render(event,n) for n,event in enumerate(events,1))
        self.assertTrue(check(events,fragment)['complete'])
        self.assertEqual(check(events,fragment)['unit_count'],len(events))

    def test_every_variant_omission_is_refused(self):
        from _web_print_curriculum.response_geometry import render,check,GeometryError
        events=self.fixtures();parts=[render(event,n) for n,event in enumerate(events,1)]
        for n in range(len(parts)):
            with self.subTest(event=events[n]),self.assertRaises(GeometryError):check(events,''.join(parts[:n]+parts[n+1:]))

    def test_every_unknown_or_changed_variant_is_refused(self):
        from _web_print_curriculum.response_geometry import render,check,GeometryError,variant
        for n,event in enumerate(self.fixtures(),1):
            expected=[dict(event,id='response-1')];fragment=render(event,1)
            with self.subTest(event=event),self.assertRaises(GeometryError):check(expected,fragment.replace(variant(event),'response-unmodelled',1))
        event=self.fixtures()[7];expected=[dict(event,id='response-1')]
        with self.assertRaises(GeometryError):check(expected,render(event,1).replace('response-block-038','response-block-070'))

    def test_multiline_rule_omission_is_refused(self):
        from _web_print_curriculum.response_geometry import render,check,GeometryError
        for event in self.fixtures()[4:6]:
            expected=[dict(event,id='response-1')]
            with self.subTest(event=event),self.assertRaisesRegex(GeometryError,'ruled-line count'):
                check(expected,render(event,1).replace('<span class="response-ruled-line"></span>','',1))

    def test_orphan_response_classes_are_refused(self):
        from _web_print_curriculum.response_geometry import check,GeometryError
        for name in ['response-blank-short','response-ruled-line','response-block-038']:
            with self.subTest(name=name),self.assertRaisesRegex(GeometryError,'orphan'):check([],'<span class="'+name+'"></span>')

    def test_unknown_source_metrics_are_refused(self):
        from _web_print_curriculum.response_geometry import signature,GeometryError
        for origin,height in [('Exercise','9in'),('rule','0.66in'),('AssessmentItem','20pt')]:
            with self.subTest(origin=origin),self.assertRaises(GeometryError):signature(origin,height)

    def test_response_visibility_or_metric_attributes_are_refused(self):
        from _web_print_curriculum.response_geometry import render,check,GeometryError
        event=self.fixtures()[4];expected=[dict(event,id='response-1')];fragment=render(event,1)
        for attribute in [' style="display:none"',' hidden',' aria-hidden="true"',' style="width:0"']:
            with self.subTest(attribute=attribute),self.assertRaises(GeometryError):
                check(expected,fragment.replace('<span','<span'+attribute,1))
        with self.assertRaises(GeometryError):
            check(expected,fragment.replace('class="response-ruled-line"','class="response-ruled-line" style="display:none"',1))

    def test_final_parts_have_geometry_proof_and_uniform_byte_pins(self):
        import hashlib
        from _web_print_curriculum import render_publication
        from _web_print_curriculum.response_geometry import check
        product=render_publication(ROOT,'gpt',M01)
        self.assertEqual(check(product['expected_response_geometry'],''.join(part['html'] for part in product['parts'])),product['response_geometry_coverage'])
        self.assertGreater(product['response_geometry_coverage']['unit_count'],0)
        for part in product['parts']:self.assertEqual(part['html_sha256'],hashlib.sha256(part['html'].encode()).hexdigest())


if __name__=='__main__':
    unittest.main()
