from pathlib import Path
import re
import copy
import subprocess
import tempfile
import unittest
import sys,shutil
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"scripts"))
import _web_print_publication as print_converter
import _web_print_flow as flow_fixes

ROOT=Path(__file__).resolve().parents[2]
PANDOC=Path(shutil.which('pandoc') or 'pandoc')
SCRATCH=ROOT/'.scratch/web-print-converter/flow-fixes'

class FlowFixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library=print_converter.load_library(ROOT)
        SCRATCH.mkdir(parents=True,exist_ok=True)

    def minipages(self,text,count):
        containers=[{'id':'minipage-'+str(i),'source_ref':{'path':'source.tex','selected_line':i}} for i in range(1,count+1)]
        with tempfile.NamedTemporaryFile('w',suffix='.lua',dir=SCRATCH) as helper:
            helper.write(flow_fixes.minipage_lua_filter(containers));helper.flush()
            return subprocess.run([str(PANDOC),'-f','latex','-t','markdown','--lua-filter='+helper.name],input='\\begin{document}'+text+'\\end{document}',text=True,capture_output=True)

    def test_length_register_assignment_removed_not_following_words(self):
        result,records=flow_fixes.drop_length_assignments(r'\setlength{\itemsep}{0.15em}7 witnesses.\setlength{\parsep}{0pt}',self.library)
        self.assertEqual(result,'{}7 witnesses.{}')
        self.assertEqual([r['register'] for r in records],['itemsep','parsep'])

    def test_content_in_dimension_refused(self):
        with self.assertRaises(flow_fixes.FlowFixError):
            flow_fixes.drop_length_assignments(r'\setlength{\itemsep}{\UnknownText{Amen.}}',self.library)

    def test_unknown_register_is_not_whitelisted(self):
        source=r'\setlength{\NovelRegister}{2em}Words.'
        result,records=flow_fixes.drop_length_assignments(source,self.library)
        self.assertEqual(source,result);self.assertFalse(records)
        self.assertTrue(self.library.undefined_uses({Path('source.tex'):result},set()))

    def test_aleph_witness_siglum_preserved(self):
        result,records=flow_fixes.preserve_aleph(r'Codex Sinaiticus (\(\aleph\)).')
        self.assertEqual(result,'Codex Sinaiticus (ℵ).');self.assertEqual(len(records),1)
        self.assertEqual(flow_fixes.preserve_aleph(r'\UnknownMath')[0],r'\UnknownMath')

    def test_canonical_accent_alias_consumes_control_word_space(self):
        head=r"\newcommand{\aeacute}{\'{\ae}}"
        body=r'Largíre nobis, qu\aeacute sumus, Dómine.'
        projected,records=flow_fixes.preserve_glyph_aliases(body,head,self.library)
        self.assertEqual(projected,'Largíre nobis, quǽsumus, Dómine.')
        self.assertEqual(records[0]['macro'],'aeacute')
        run=subprocess.run([str(PANDOC),'-f','latex','-t','html5','--wrap=none'],input='\\begin{document}'+projected+'\\end{document}',text=True,capture_output=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('quǽsumus',run.stdout);self.assertNotIn('quǽ sumus',run.stdout)

    def test_glyph_alias_preserves_explicit_space_and_paragraph_boundary(self):
        head=r"\newcommand{\aeacute}{\'{\ae}}"
        self.assertEqual(flow_fixes.preserve_glyph_aliases(r'qu\aeacute{} sumus',head,self.library)[0],'quǽ{} sumus')
        self.assertEqual(flow_fixes.preserve_glyph_aliases('qu\\aeacute\n\nNext.',head,self.library)[0],'quǽ\n\nNext.')
        self.assertEqual(flow_fixes.preserve_glyph_aliases('qu\\aeacute% comment\nsumus',head,self.library)[0],'quǽsumus')

    def test_glyph_alias_does_not_rewrite_definitions_or_guess_reassignment(self):
        head=r"\newcommand{\aeacute}{\'{\ae}}"
        definition=r'\newcommand{\alias}{qu\aeacute sumus}'
        self.assertEqual(flow_fixes.preserve_glyph_aliases(definition,head,self.library)[0],definition)
        with self.assertRaises(flow_fixes.FlowFixError):
            flow_fixes.preserve_glyph_aliases(r'\renewcommand{\aeacute}{X}qu\aeacute sumus',head,self.library)

    def test_canonical_timeline_headers_are_not_replaced_by_shared_words(self):
        opening=r'\begin{longtable}{llll}\textbf{Date} & \textbf{Act or event} & \textbf{Witness used} & \textbf{Status}\\\endhead'
        closing=r'\end{longtable}'
        head=r'\newenvironment{accounttimeline}{'+opening+'}{'+closing+'}'
        addition,records=flow_fixes.table_environment_shim({'head':head},self.library)
        self.assertIn(opening,addition);self.assertIn(closing,addition)
        self.assertNotIn('Event or act',addition);self.assertNotIn('Witness or edition',addition)
        run=subprocess.run([str(PANDOC),'-f','latex','-t','html5','--wrap=none'],input=self.library.SHIM.read_text()+addition+'\\begin{document}\\begin{accounttimeline}2026 & An act & A witness & Secure\\\\\\end{accounttimeline}\\end{document}',text=True,capture_output=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('Act or event',run.stdout);self.assertIn('Witness used',run.stdout)
        self.assertNotIn('Event or act',run.stdout)
        self.assertEqual(records[0]['environment'],'accounttimeline')

    def test_separator_inside_canonical_macro_definition_is_rendered(self):
        head=r'\newcommand{\appointedrubric}[2]{\par\textbf{Rubric as printed:} #1\textperiodcentered{} #2\par}'
        projected,records=flow_fixes.preserve_known_separator(head,head,self.library,'head')
        self.assertIn('·',projected);self.assertEqual(len(records),1)
        source=projected+r'\begin{document}\appointedrubric{Credo.}{Printed direction.}\end{document}'
        run=subprocess.run([str(PANDOC),'-f','latex','-t','html5','--wrap=none'],input=source,text=True,capture_output=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('Credo.· Printed direction.',run.stdout)

    def test_separator_projection_preserves_control_word_spacing(self):
        source='Miscel\\textperiodcentered lania; a\\textperiodcentered{} b.\\textperiodcentered\n\nNext.'
        projected,_=flow_fixes.preserve_known_separator(source,'',self.library,'body')
        self.assertEqual(projected,'Miscel·lania; a· b.·\n\nNext.')
        with self.assertRaises(flow_fixes.FlowFixError):
            flow_fixes.preserve_known_separator(r'\textperiodcentered',r'\newcommand{\textperiodcentered}{X}',self.library,'body')

    def test_normative_environment_keeps_first_numeric_token(self):
        opening=r'\begin{studyframe}\small\textbf{Locus:} #1\par\vspace{0.15em}\itshape\ignorespaces'
        head=r'\newenvironment{normtext}[1]{'+opening+r'}{\end{studyframe}}'
        addition,records=flow_fixes.normative_environment_shim({'head':head},self.library)
        self.assertIn(r'\ignorespaces{}',addition)
        source=self.library.SHIM.read_text()+addition+r'\begin{document}\begin{normtext}{Law}1. Tempus ecclesiasticum.\end{normtext}\end{document}'
        run=subprocess.run([str(PANDOC),'-f','latex','-t','html5','--wrap=none'],input=source,text=True,capture_output=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('1. Tempus ecclesiasticum.',run.stdout)
        self.assertEqual(records[0]['environment'],'normtext')

    def test_literal_responsum_label_cannot_be_par_option(self):
        body='Virgo fertur apparuisse.\\par\n[Responsum:] Simulacra collocari poterunt.'
        projected,records=flow_fixes.guard_literal_brackets(body,self.library,'body')
        self.assertIn(r'\par{}',projected);self.assertEqual(len(records),1)
        run=subprocess.run([str(PANDOC),'-f','latex','-t','html5','--wrap=none'],input=r'\begin{document}'+projected+r'\end{document}',text=True,capture_output=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('[Responsum:]',run.stdout)
        self.assertEqual(run.stdout.count('<p>'),2)

    def test_bracket_guard_does_not_rewrite_heading_or_numeric_layout_option(self):
        source=r'\paragraph{Heading}[More]\nopagebreak[4]\par{}[Already guarded]'
        projected,records=flow_fixes.guard_literal_brackets(source,self.library,'body')
        self.assertEqual(projected,source);self.assertFalse(records)

    def test_canonical_openings_do_not_read_layout_dimensions(self):
        source=r'\par}\vspace{0.08em}{\Large\itshape of the Latin Bible\par}'
        self.assertIn('em',self.library.source_openings(source))
        ledger={'units':[{'kind':'paragraph','expected':'of the latin bible'}]}
        self.assertEqual(flow_fixes.canonical_openings(ledger,self.library),['of'])

    def test_opening_oracle_never_uses_converted_output_or_metadata(self):
        ledger={'units':[{'kind':'metadata-subtitle','expected':'invented opening'},{'kind':'paragraph','expected':'canonical words'}]}
        self.assertEqual(flow_fixes.canonical_openings(ledger,self.library),['canonical'])
        self.assertIsNone(flow_fixes.canonical_openings({'containers':[]},self.library))

    def test_prepare_keeps_source_cover_paragraph_boundaries(self):
        source=r'\begin{titlepage}{\Large First\par}\vspace{0.08em}{\Large second\par}\end{titlepage}'
        selection={'head':'','body':source}
        result=flow_fixes.prepare(selection,self.library,expected_ledger={'containers':[]})
        self.assertEqual(result['body'],source)

    def test_longtable_footers_are_not_body_rows(self):
        source=r'\begin{longtable}{ll}First & Head\\\endfirsthead Repeat & Head\\\endhead Footer & Here\\\endfoot Last & Footer\\\endlastfoot Body & Amen.\\\end{longtable}'
        result,records=flow_fixes.drop_longtable_footers(source,self.library)
        self.assertNotIn('Footer',result);self.assertNotIn('Last',result)
        self.assertIn('Body & Amen.',result);self.assertIn('First & Head',result)
        self.assertEqual(len(records),2)

    def test_prepare_preserves_supplied_diagram_audit_projection(self):
        source=r'Canonical diagram contains internal table cells.'
        audit=r'\begin{longtable}{l}Head\\\endhead Physical footer\\\endfoot VERIFIED_SVG_UNIT\\\end{longtable}'
        selection={'head':'','body':source,'canonical_body':source,'audit_body':audit,'projections':[{'kind':'verified-svg'}],'shim_additions':'% verified SVG shim\n','lua_filters':['-- verified SVG filter']}
        result=flow_fixes.prepare(selection,self.library,expected_ledger={'containers':[]})
        self.assertEqual(result['canonical_body'],source)
        self.assertIn('VERIFIED_SVG_UNIT',result['audit_body'])
        self.assertNotIn('internal table cells',result['audit_body'])
        self.assertNotIn('Physical footer',result['audit_body'])
        self.assertEqual(result['projections'][0],{'kind':'verified-svg'})
        self.assertTrue(result['shim_additions'].startswith('% verified SVG shim'))
        self.assertEqual(result['lua_filters'],['-- verified SVG filter'])

    def test_real_body_continued_word_not_removed(self):
        source=r'\begin{longtable}{l}Heading\\\endhead A continued tradition.\\\end{longtable}'
        result,_=flow_fixes.drop_longtable_footers(source,self.library)
        self.assertIn('continued tradition',result)

    def test_empty_style_padding_removed_without_cell_words(self):
        source={'body':r'\multicolumn{5}{l}{Group}'}
        text='<table><td><strong></strong></td><td><strong>Amen.</strong></td></table>'
        result,records=flow_fixes.prepare_markdown(text,source,self.library)
        self.assertIn('<td></td>',result);self.assertIn('<strong>Amen.</strong>',result)
        self.assertEqual(records[0]['cells'],1)
        self.assertEqual(flow_fixes.prepare_markdown(text,{'body':'ordinary table'},self.library)[0],text)

    def test_typed_minipage_groups_preserve_all_short_words_and_order(self):
        run=self.minipages(r'\begin{minipage}{0.48\linewidth}Latin: Amen.\end{minipage}\begin{minipage}{0.48\linewidth}English: So be it.\end{minipage}',2)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertNotIn(':::',run.stdout)
        self.assertIn('data-semantic-minipage="minipage-1"',run.stdout);self.assertIn('data-semantic-minipage="minipage-2"',run.stdout)
        self.assertLess(run.stdout.index('Latin: Amen.'),run.stdout.index('English: So be it.'))
        self.assertIn('triptych-minipages: 2',run.stderr)

    def test_nested_minipage_ids_follow_source_preorder(self):
        run=self.minipages(r'\begin{minipage}{\linewidth}Outer.\begin{minipage}{\linewidth}Inner.\end{minipage}\end{minipage}',2)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertLess(run.stdout.index('data-print-unit="minipage-1"'),run.stdout.index('data-print-unit="minipage-2"'))

    def test_enclosing_quotation_is_semantic_html_not_p_around_section(self):
        run=self.minipages(r'\begin{quote}Frame.\begin{minipage}{\linewidth}Amen.\end{minipage}\end{quote}',1)
        self.assertEqual(run.returncode,0,run.stderr)
        html=self.library.render_markdown(run.stdout,ROOT)
        self.assertIn('<blockquote>',html)
        self.assertNotRegex(html,r'<p>\s*<section')
        self.assertIn('Amen.',html)

    def test_extra_or_missing_group_fails_expected_count(self):
        run=self.minipages(r'\begin{minipage}{\linewidth}Amen.\end{minipage}',2)
        self.assertNotEqual(run.returncode,0);self.assertIn('count mismatch',run.stderr)

    def test_unknown_environment_not_silently_flattened(self):
        run=self.minipages(r'\begin{UnknownFlow}Amen.\end{UnknownFlow}',0)
        self.assertNotEqual(run.returncode,0);self.assertIn('unsupported remaining flow Div',run.stderr)

    def test_minipage_notes_require_owning_note_audit(self):
        run=self.minipages(r'\begin{minipage}{\linewidth}Amen.\footnote{Brief note.}\end{minipage}',1)
        self.assertNotEqual(run.returncode,0);self.assertIn('owning raw-HTML note audit',run.stderr)


    def test_textbar_is_source_glyph_inside_prose_and_macro(self):
        head=r'\newcommand{\witness}[1]{#1\textbar{} Psalm.}'
        result,records=flow_fixes.preserve_known_separator(head,head,self.library,'head')
        self.assertIn('#1| Psalm.',result)
        self.assertEqual(records[0]['macro'],'textbar')
        run=subprocess.run([str(PANDOC),'-f','latex','-t','markdown'],input=result+r'\begin{document}\witness{First.}\end{document}',text=True,capture_output=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('|',self.library.render_markdown(run.stdout,ROOT))

    def test_working_rendering_initial_number_is_retained(self):
        head=r'\newenvironment{workingrendering}{\par\small\textbf{Project translation.}\ \ignorespaces}{\par}'
        addition,records=flow_fixes.normative_environment_shim({'head':head},self.library)
        run=subprocess.run([str(PANDOC),'-f','latex','-t','html5','--wrap=none'],input=addition+r'\begin{document}\begin{workingrendering}3) When the year begins.\end{workingrendering}\end{document}',text=True,capture_output=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('3) When',run.stdout)
        self.assertEqual(records[0]['argument_count'],0)

    def test_canonical_virtue_label_is_not_layout_argument(self):
        head=r'\newcommand{\virtuegrouplabel}[1]{\Needspace{5\baselineskip}\par\medskip\noindent{\normalsize\bfseries #1}\par\smallskip}'
        addition,records=flow_fixes.canonical_content_macros({'head':head,'body':''},self.library)
        run=subprocess.run([str(PANDOC),'-f','latex','-t','html5','--wrap=none'],input=self.library.SHIM.read_text()+addition+r'\begin{document}\virtuegrouplabel{Unequal debts: religion, piety, and observance}\end{document}',text=True,capture_output=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('<strong>Unequal debts: religion, piety, and observance</strong>',run.stdout)
        self.assertEqual(records[0]['macro'],'virtuegrouplabel')

    def test_source_summary_retains_runtime_kicker(self):
        head=(ROOT/'src/gpt/theology/sacraments/summary-preamble.tex').read_text()
        addition,records=flow_fixes.canonical_content_macros({'head':head,'body':''},self.library)
        source=self.library.SHIM.read_text()+addition+r'\begin{document}\renewcommand{\sacramentSummaryKicker}{Sacramental Appendix---}\sacramentSummaryStart{Matrimony}{One flesh}{A covenant}\sacramentSummaryEnd\end{document}'
        run=subprocess.run([str(PANDOC),'-f','latex','-t','html5','--wrap=none'],input=source,text=True,capture_output=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('Sacramental Appendix',run.stdout);self.assertIn('Matrimony at a Glance',run.stdout)
        self.assertIn('One flesh',run.stdout);self.assertIn('A covenant',run.stdout)

    def test_source_two_argument_term_keeps_two_table_cells(self):
        body=r'\providecommand{\term}[2]{\textbf{#1} & #2\\\addlinespace[0.12em]}\begin{tabular}{ll}Term&Meaning\\\term{Act}{Perfection.}\end{tabular}'
        addition,records=flow_fixes.canonical_content_macros({'head':'','body':body},self.library)
        run=subprocess.run([str(PANDOC),'-f','latex','-t','html5','--wrap=none'],input=self.library.SHIM.read_text()+addition+r'\begin{document}'+body+r'\end{document}',text=True,capture_output=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertRegex(run.stdout,r'<td[^>]*><strong>Act</strong></td>\s*<td[^>]*>Perfection\.</td>')
        self.assertEqual(records[0]['canonical_argument_count'],2)
        self.assertEqual(run.stdout.count('<tr'),2)

    def test_early_source_term_use_refuses_signature_override(self):
        body=r'\term{Early}\providecommand{\term}[2]{#1&#2\\}'
        with self.assertRaises(flow_fixes.FlowFixError):flow_fixes.canonical_content_macros({'head':'','body':body},self.library)

    def test_markdown_less_than_has_literal_glyph_without_backslash(self):
        result,records=flow_fixes.prepare_markdown(r'*p*\<.05',{'body':'$p<.05$'},self.library)
        rendered=self.library.render_markdown(result,ROOT)
        self.assertIn('&lt;.05',rendered);self.assertNotIn('\\',rendered)
        self.assertEqual(records[0]['kind'],'markdown-literal-angle-entity')

    def test_source_urn_autolink_is_real_bound_link(self):
        uri='urn:cts:greekLit:tlg0526.tlg001.perseus-grc2:6.16'
        result,records=flow_fixes.prepare_markdown('<'+uri+'>',{'body':r'\url{'+uri+'}'},self.library)
        rendered=self.library.render_markdown(result,ROOT)
        self.assertIn('href="'+uri+'"',rendered);self.assertIn('>'+uri+'</a>',rendered)
        self.assertEqual(records[0]['occurrences'],1)
        untouched,_=flow_fixes.prepare_markdown('<urn:unbound>',{'body':''},self.library)
        self.assertEqual(untouched,'<urn:unbound>')

    def test_bound_local_minipage_note_preserves_body_and_identity(self):
        containers=[{'id':'minipage-1','source_ref':{'path':'source.tex','selected_line':1}}]
        with tempfile.NamedTemporaryFile('w',suffix='.lua',dir=SCRATCH) as helper:
            helper.write(flow_fixes.minipage_lua_filter(containers,{'minipage-1':['unit-000002']}));helper.flush()
            run=subprocess.run([str(PANDOC),'-f','latex','-t','markdown','--lua-filter='+helper.name],input=r'\begin{document}\begin{minipage}{\linewidth}Amen.\footnote{Brief note.}\end{minipage}\end{document}',text=True,capture_output=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('data-semantic-note="unit-000002"',run.stdout)
        self.assertIn('Brief note.',run.stdout);self.assertIn('class="footnote print-local-notes"',run.stdout)
        self.assertIn('class="footnote-backref"',run.stdout)
        self.assertIn('href="#minipage-1-fn1"',run.stdout)


    def test_caption_numbers_follow_canonical_executed_counter_calls(self):
        from _web_print_semantics import Ledger
        head=r'\newcounter{sketchfigure}\newcommand{\sketchcaption}[1]{\refstepcounter{sketchfigure}\textbf{Drawing \thesketchfigure.} #1\par}'
        body=r'\newcounter{sketchfigure}\sketchcaption{The first ark.}\sketchcaption{The second ark.}'
        selection={'head':head,'body':body};ledger=Ledger(selection,self.library).run(fragment=True)
        result,records=flow_fixes.counter_display_projection(body,selection,ledger,self.library)
        self.assertIn('Drawing 1.',result);self.assertIn('Drawing 2.',result)
        self.assertIn('The first ark.',result);self.assertIn('The second ark.',result)
        self.assertEqual([r['displays'][0]['rawdisplay'] for r in records],['1','2'])

    def test_source_explicit_word_space_survives_macro_projection(self):
        source=r'\renewcommand{\Prefix}{Appendix D:\space}\Prefix Baptism'
        projected,records=flow_fixes.preserve_known_separator(source,'',self.library,'body')
        self.assertIn('Appendix D: ',projected)
        self.assertEqual(records[0]['macro'],'space')


    def test_local_note_short_content_omission_fails_independent_gate(self):
        from _web_print_semantics import Ledger,check_units
        source=r'\begin{minipage}{\linewidth}Amen.\footnote{A short note.}\end{minipage}'
        selection={'head':'','body':source}
        ledger=Ledger(selection,self.library).run(fragment=True)
        prepared=flow_fixes.prepare(selection,self.library,expected_ledger=ledger)
        with tempfile.NamedTemporaryFile('w',suffix='.lua',dir=SCRATCH) as helper:
            helper.write(prepared['lua_filters'][0]);helper.flush()
            run=subprocess.run([str(PANDOC),'-f','latex','-t','markdown','--lua-filter='+helper.name],input=r'\begin{document}'+prepared['body']+r'\end{document}',text=True,capture_output=True)
        self.assertEqual(run.returncode,0,run.stderr)
        rendered=self.library.render_markdown(run.stdout,ROOT)
        self.assertEqual(check_units(ledger,rendered,self.library)['status'],'pass')
        failed=check_units(ledger,rendered.replace('A short note.',''),self.library)
        self.assertEqual(failed['status'],'refused')
        self.assertTrue(any(row['kind']=='note' for row in failed['failures']))


    def test_executed_counter_replay_preserves_nested_source_program_and_args(self):
        from _web_print_semantics import Ledger
        head=r'\newcommand{\prefix}{Appendix \thesection:\space}\newcommand{\face}[1]{\textbf{\prefix#1}\par}'
        body=r'\appendix\refstepcounter{section}\face{Baptism}\refstepcounter{section}\face{Matrimony}'
        selection={'head':head,'body':body};ledger=Ledger(selection,self.library).run(fragment=True)
        result,records=flow_fixes.counter_display_projection(body,selection,ledger,self.library)
        self.assertIn('Appendix A:',result);self.assertIn('Appendix B:',result)
        self.assertIn('Baptism',result);self.assertIn('Matrimony',result)
        self.assertEqual(len(records),2)
        self.assertEqual([r['displays'][0]['rawdisplay'] for r in records],['A','B'])

    def test_duplicate_literal_counter_call_occurrences_keep_executed_order(self):
        from _web_print_semantics import Ledger
        head=r'\newcommand{\show}{Value \thesection\par}'
        body=r'\appendix\refstepcounter{section}\show\refstepcounter{section}\show'
        selection={'head':head,'body':body};ledger=Ledger(selection,self.library).run(fragment=True)
        result,records=flow_fixes.counter_display_projection(body,selection,ledger,self.library)
        self.assertLess(result.index('Value A'),result.index('Value B'))
        self.assertEqual(len(records),2)

    def test_counter_replay_binds_multiple_reads_and_direct_primitive(self):
        from _web_print_semantics import Ledger
        head=r'\newcommand{\show}{\arabic{thing} / \Roman{thing}\par}'
        body=r'\newcounter{thing}\stepcounter{thing}\show Direct \arabic{thing}.'
        selection={'head':head,'body':body};ledger=Ledger(selection,self.library).run(fragment=True)
        result,records=flow_fixes.counter_display_projection(body,selection,ledger,self.library)
        self.assertIn('1 / I',result);self.assertIn('Direct 1.',result)
        self.assertEqual(sum(len(r['event_ids']) for r in records),3)

    def test_counter_replay_refuses_changed_program_call_or_missing_occurrence(self):
        from _web_print_semantics import Ledger
        head=r'\newcommand{\show}{Value \thesection\par}'
        body=r'\appendix\refstepcounter{section}\show'
        selection={'head':head,'body':body};ledger=Ledger(selection,self.library).run(fragment=True)
        mutated=copy.deepcopy(ledger);mutated['counter_displays'][0]['expansion'][0]['expanded_program']='Invented words.'
        with self.assertRaises(flow_fixes.FlowFixError):flow_fixes.counter_display_projection(body,selection,mutated,self.library)
        with self.assertRaises(flow_fixes.FlowFixError):flow_fixes.counter_display_projection(body.replace(r'\show',''),selection,ledger,self.library)
        mutated=copy.deepcopy(ledger);mutated['counter_displays'][0]['source_call']=r'\other'
        with self.assertRaises(flow_fixes.FlowFixError):flow_fixes.counter_display_projection(body,selection,mutated,self.library)


    def render_inline_form(self,source):
        from _web_print_semantics import Ledger
        selection={'head':'','body':source};ledger=Ledger(selection,self.library).run(fragment=True)
        prepared=flow_fixes.prepare(selection,self.library,expected_ledger=ledger)
        with tempfile.NamedTemporaryFile('w',suffix='.lua',dir=SCRATCH) as helper:
            helper.write(prepared['lua_filters'][0]);helper.flush()
            run=subprocess.run([str(PANDOC),'-f','latex','-t','markdown','--lua-filter='+helper.name],input=prepared['shim_additions']+r'\begin{document}'+prepared['body']+r'\end{document}',text=True,capture_output=True)
        self.assertEqual(run.returncode,0,run.stderr)
        rendered=self.library.render_markdown(run.stdout,ROOT)
        return prepared,ledger,rendered

    def test_inline_checker_date_retains_source_widths_and_one_paragraph(self):
        from _web_print_semantics import check_units
        source=r'Checker: \rule{0.28\linewidth}{0.4pt}\hfill Date: \rule{0.20\linewidth}{0.4pt}'
        prepared,ledger,rendered=self.render_inline_form(source)
        self.assertEqual(rendered.count('<p'),1);self.assertNotIn('<hr',rendered)
        self.assertIn('data-source-width="0.28&#92;linewidth"',rendered)
        self.assertIn('data-source-width="0.20&#92;linewidth"',rendered)
        self.assertEqual(rendered.count('data-source-thickness="0.4pt"'),2)
        self.assertIn('print-fill-line-28',rendered);self.assertIn('print-fill-line-20',rendered)
        self.assertLess(rendered.index('Checker:'),rendered.index('Date:'))
        flow_fixes.check_form_lines(prepared['expected_form_lines'],rendered)
        self.assertEqual(check_units(ledger,rendered,self.library)['status'],'pass')

    def test_inline_form_field_omission_or_dimension_mutation_refuses(self):
        source=r'Checker: \rule{0.28\linewidth}{0.4pt}\hfill Date: \rule{0.20\linewidth}{0.4pt}'
        prepared,_,rendered=self.render_inline_form(source)
        lost=re.sub(r'<span class="print-fill-line print-fill-line-20"[^>]*></span>','',rendered)
        with self.assertRaises(flow_fixes.FlowFixError):flow_fixes.check_form_lines(prepared['expected_form_lines'],lost)
        with self.assertRaises(flow_fixes.FlowFixError):flow_fixes.check_form_lines(prepared['expected_form_lines'],rendered.replace('0.28&#92;linewidth','0.20&#92;linewidth'))

    def test_unknown_inline_form_metrics_refuse_other_rules_keep_existing_gates(self):
        bad=r'Checker: \rule{0.29\linewidth}{0.4pt}\hfill Date: \rule{0.20\linewidth}{0.4pt}'
        with self.assertRaises(flow_fixes.FlowFixError):flow_fixes.inline_form_lines(bad,{'body':bad},self.library)
        other=r'\rule{\linewidth}{0.35pt}'
        result=flow_fixes.inline_form_lines(other,{'body':other},self.library)
        self.assertEqual(result[0],other);self.assertFalse(result[4])

    def test_inline_form_source_row_binding_refuses_changed_label(self):
        source=r'Checker: \rule{0.28\linewidth}{0.4pt}\hfill Date: \rule{0.20\linewidth}{0.4pt}'
        with self.assertRaises(flow_fixes.FlowFixError):flow_fixes.inline_form_lines(source.replace('Date:','Day:'),{'body':source},self.library)

if __name__=='__main__':unittest.main()
