from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"scripts"))
import _web_print_publication as print_converter
import _web_print_semantics as coverage

ROOT=Path(__file__).resolve().parents[2]
RIGHTS=r'\newcommand{\TriptychRightsNotice}{\begin{minipage}{\linewidth}\textbf{Reuse and rights.} Exact source notice.\end{minipage}}'
RIGHTS_HTML='<p><strong>Reuse and rights.</strong> Exact source notice.</p>'

class SemanticCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.library=print_converter.load_library(ROOT)
    def ledger(self,body,head=''):
        selection={'head':RIGHTS+head,'body':body,'sources':{},'selection':{'entrypoint':'src/gpt/test/main.tex','role':'main','selection_digest':'test-source-selection'},'chunks':[{'path':'src/gpt/test/main.tex','occurrence':1,'selected_line':1,'text':body}]}
        return coverage.expected_units(selection,self.library)
    def result(self,body,html,head=''):
        return coverage.check_units(self.ledger(body,head),html+RIGHTS_HTML)
    def test_amen_is_never_length_filtered(self):
        self.assertEqual(self.result('Amen.','<p>Amen.</p>')['status'],'pass')
        self.assertEqual(self.result('Amen.','')['status'],'refused')
    def test_fragment_gate_omits_only_synthetic_publication_metadata(self):
        selection={'head':r'\newcommand{\response}[1]{\textbf{#1}}','body':r'\response{Amen.}','sources':{},'chunks':[{'path':'canonical-fragment.tex','occurrence':1,'selected_line':40,'text':r'\response{Amen.}'}],'selection':{'entrypoint':'canonical-fragment.tex','selection_digest':'selected'}}
        ledger=coverage.expected_fragment_units(selection,self.library)
        self.assertEqual(ledger['scope'],'canonical-fragment')
        self.assertEqual(coverage.check_units(ledger,'<p><strong>Amen.</strong></p>')['status'],'pass')
        self.assertEqual(coverage.check_units(ledger,'')['status'],'refused')
        with self.assertRaises(coverage.CoverageError):coverage.expected_units(selection,self.library)
    def test_samepage_fragment_keeps_every_paragraph_and_short_response(self):
        body=r'\begin{samepage}First instruction.\par Amen.\end{samepage}'
        selection={'head':'','body':body,'sources':{},'chunks':[{'path':'canonical-role-sheet.tex','occurrence':1,'selected_line':46,'text':body}],'selection':{'entrypoint':'canonical-role-sheet.tex','selection_digest':'selected'}}
        ledger=coverage.expected_fragment_units(selection,self.library)
        self.assertEqual(coverage.check_units(ledger,'<p>First instruction.</p><p>Amen.</p>')['status'],'pass')
        for fragment in ('<p>First instruction.</p>','<p>Amen.</p><p>First instruction.</p>'):
            self.assertEqual(coverage.check_units(ledger,fragment)['status'],'refused')
    def test_short_item_and_order(self):
        source=r'\begin{itemize}\item Amen.\item Deo gratias.\end{itemize}'
        self.assertEqual(self.result(source,'<ul><li>Amen.</li><li>Deo gratias.</li></ul>')['status'],'pass')
        self.assertEqual(self.result(source,'<ul><li>Deo gratias.</li><li>Amen.</li></ul>')['status'],'refused')
        self.assertEqual(self.result(source,'<ul><li>Deo gratias.</li></ul>')['status'],'refused')
    def test_short_footnote_can_move_but_cannot_disappear(self):
        source=r'Body.\footnote{Amen.}'
        html='<p>Body.<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p><div class="footnote"><ol><li id="fn:1"><p>Amen. <a class="footnote-backref" href="#fnref:1">↩</a></p></li></ol></div>'
        self.assertEqual(self.result(source,html)['status'],'pass')
        self.assertEqual(self.result(source,'<p>Body.</p>')['status'],'refused')
    def test_short_cell_and_local_order(self):
        source=r'\begin{tabular}{ll}Cue & Response\\Yes & Amen.\\\end{tabular}'
        html='<table><tr><th>Cue</th><th>Response</th></tr><tr><td>Yes</td><td>Amen.</td></tr></table>'
        self.assertEqual(self.result(source,html)['status'],'pass')
        self.assertEqual(self.result(source,html.replace('Amen.',''))['status'],'refused')
        self.assertEqual(self.result(source,html.replace('<td>Yes</td><td>Amen.</td>','<td>Amen.</td><td>Yes</td>'))['status'],'refused')
    def test_repeated_occurrences_cannot_share_one_block(self):
        self.assertEqual(self.result('Amen.\n\nAmen.','<p>Amen.</p>')['status'],'refused')
        self.assertEqual(self.result('Amen.\n\nAmen.','<p>Amen.</p><p>Amen.</p>')['status'],'pass')
    def test_paragraph_reordering(self):
        self.assertEqual(self.result('Alpha.\n\nBeta.','<p>Beta.</p><p>Alpha.</p>')['status'],'refused')
    def test_inline_ligatures_and_accents_keep_word_boundaries(self):
        body=r'p{\ae}nitentiam M\"unchener Thom\`as'
        self.assertEqual(self.result(body,'<p>pænitentiam Münchener Thomàs</p>')['status'],'pass')
        self.assertEqual(self.result(body,'<p>p nitentiam M unchener Thom as</p>')['status'],'refused')
    def test_canonical_macro_visible_body(self):
        head=r'\newcommand{\example}[2]{\textbf{#1}: #2\par}'
        self.assertEqual(self.result(r'\example{Title}{Amen.}','<p><strong>Title</strong>: Amen.</p>',head)['status'],'pass')
        self.assertEqual(self.result(r'\example{Title}{Amen.}','<p><strong>Title</strong>.</p>',head)['status'],'refused')
    def test_environment_injected_instruction_is_required(self):
        head=r'\newenvironment{lessonbox}[1]{\begin{quote}\textbf{#1}\par Required instruction.\par}{\end{quote}}'
        source=r'\begin{lessonbox}{Read}Amen.\end{lessonbox}'
        html='<blockquote><p><strong>Read</strong></p><p>Required instruction.</p><p>Amen.</p></blockquote>'
        self.assertEqual(self.result(source,html,head)['status'],'pass')
        self.assertEqual(self.result(source,html.replace('<p>Required instruction.</p>',''),head)['status'],'refused')
    def test_minipage_order_and_source_boundaries(self):
        body=r'\begin{minipage}{.48\linewidth}Latin.\end{minipage}\begin{minipage}[t]{.48\linewidth}English.\end{minipage}'
        ledger=self.ledger(body)
        self.assertEqual([unit['id'] for unit in ledger['containers']],['minipage-1','minipage-2'])
        self.assertEqual(coverage.check_units(ledger,'<section data-semantic-minipage="minipage-1"><p>Latin.</p></section><section data-semantic-minipage="minipage-2"><p>English.</p></section>'+RIGHTS_HTML)['status'],'pass')
        self.assertEqual(coverage.check_units(ledger,'<section data-semantic-minipage="minipage-2"><p>English.</p></section><section data-semantic-minipage="minipage-1"><p>Latin.</p></section>'+RIGHTS_HTML)['status'],'refused')
    def test_macro_substitution_preserves_control_token_boundaries(self):
        head=r'\newcommand{\pair}[2]{#1\enspace#2}'
        self.assertEqual(self.result(r'\pair{One}{The next}','<p>One The next</p>',head)['status'],'pass')
    def test_unexplained_extra_paragraph_is_rejected(self):
        self.assertEqual(self.result('Amen.','<p>Amen.</p><p>Invented claim.</p>')['status'],'refused')
    def test_canonical_group_definitions_restore_scope(self):
        body=r'\state.\par{\renewcommand{\state}{Inner}\state.\par}\state.'
        head=r'\newcommand{\state}{Outer}'
        self.assertEqual(self.result(body,'<p>Outer.</p><p>Inner.</p><p>Outer.</p>',head)['status'],'pass')
    def test_register_geometry_is_excluded_but_following_short_text_is_required(self):
        self.assertEqual(self.result(r'\hbadness=10000\hyphenchar\font=45\relax Amen.','<p>Amen.</p>')['status'],'pass')
        self.assertEqual(self.result(r'\hbadness=10000 Amen.','')['status'],'refused')
    def test_line_breaks_preserve_order_inside_a_paragraph(self):
        self.assertEqual(self.result(r'Alpha.\\Beta.','<p>Alpha.<br>Beta.</p>')['status'],'pass')
        self.assertEqual(self.result(r'Alpha.\\Beta.','<p>Alpha. Beta.</p>')['status'],'refused')
    def test_table_paragraphs_keep_one_complete_cell(self):
        body=r'\begin{tabular}{ll}Field & Value\\Title\par Family & Amen.\\\end{tabular}'
        html='<table><tr><th>Field</th><th>Value</th></tr><tr><td><strong>Title</strong><br>Family</td><td>Amen.</td></tr></table>'
        self.assertEqual(self.result(body,html)['status'],'pass')
        self.assertEqual(self.result(body,html.replace('Family',''))['status'],'refused')
    def test_physical_table_footers_are_not_body_rows(self):
        body=r'\begin{longtable}{l}Header\\\endhead Continued on next page\\\endfoot Final footer\\\endlastfoot Amen.\\\end{longtable}'
        self.assertEqual(self.result(body,'<table><tr><th>Header</th></tr><tr><td>Amen.</td></tr></table>')['status'],'pass')
    def test_glyph_math_cannot_disappear(self):
        self.assertEqual(self.result(r'Word \(\aleph\) and $\rightarrow$ next.','<p>Word ℵ and → next.</p>')['status'],'pass')
        self.assertEqual(self.result(r'Word $\rightarrow$ next.','<p>Word next.</p>')['status'],'refused')
    def test_external_math_group_signature_is_verified(self):
        selection={'head':RIGHTS,'body':r'\SemanticMathUnit{scheme-1}','sources':{},'chunks':[],'selection':{'entrypoint':'source.tex'},'semantic_units':{'scheme-1':{'kind':'math','source_ref':{'path':'source.tex','line':1},'source_sha256':'a'*64,'ast_digest':'b'*64,'expected_mathml_signature':[['start','mrow'],['start','mo'],['text','⌣'],['end','mo'],['end','mrow']]}}}
        ledger=coverage.expected_units(selection,self.library)
        good='<math data-semantic-unit="scheme-1"><mrow><mo>⌣</mo></mrow></math>'+RIGHTS_HTML
        self.assertEqual(coverage.check_units(ledger,good)['status'],'pass')
        self.assertEqual(coverage.check_units(ledger,good.replace('⌣',''))['status'],'refused')
    def test_controlword_delimiter_keeps_blank_line_paragraph(self):
        self.assertEqual(self.result('First \\ldots \n\nSecond.','<p>First …</p><p>Second.</p>')['status'],'pass')
    def test_comment_does_not_consume_following_empty_line(self):
        for body in ('First.%\n\nSecond.','First.%\n%comment\n \t\nSecond.'):
            self.assertEqual(self.result(body,'<p>First.</p><p>Second.</p>')['status'],'pass')
            self.assertEqual(self.result(body,'<p>First.Second.</p>')['status'],'refused')
        self.assertEqual(self.result('First.%\nSecond.','<p>First.Second.</p>')['status'],'pass')

    def test_math_minus_is_an_operator_and_cannot_disappear(self):
        body=r'Easter $-63$ days; $Y-1$.'
        self.assertEqual(self.result(body,'<p>Easter −63 days; Y−1.</p>')['status'],'pass')
        self.assertEqual(self.result(body,'<p>Easter 63 days; Y−1.</p>')['status'],'refused')
        self.assertEqual(self.result(body,'<p>Easter +63 days; Y−1.</p>')['status'],'refused')
    def test_native_math_grouping_decimal_and_case_are_material(self):
        body=r'$S=(6-2)-(27-24)=1$; $p<.05$.'
        html='<p>S=(6−2)−(27−24)=1; p&lt;.05.</p>'
        self.assertEqual(self.result(body,html)['status'],'pass')
        for bad in (html.replace('(6−2)−(27−24)','6−(2−27)−24'),html.replace('.05','05'),html.replace('S=','s=')):
            self.assertEqual(self.result(body,bad)['status'],'refused')
        self.assertEqual(self.result(r'$|$','<p>|</p>')['status'],'pass')
        self.assertEqual(self.result(r'$|$','')['status'],'refused')
        for unsupported in (r'$x^2$',r'$x_2$',r'$?$'):
            with self.assertRaises(coverage.CoverageError):self.ledger(unsupported)
        grouped=r'$S=[(6-2)-(27-24)]$'
        self.assertEqual(self.result(grouped,'<p>S=[(6−2)−(27−24)]</p>')['status'],'pass')
        self.assertEqual(self.result(grouped,'<p>S=[6−2)−(27−24)]</p>')['status'],'refused')
        self.assertEqual(self.result(r'$^{\ast}$','<p>*</p>')['status'],'pass')
        self.assertEqual(self.result(r'$^{\ast}$','')['status'],'refused')
        self.assertEqual(self.result(r'3$^\circ$','<p>3∘</p>')['status'],'pass')
        self.assertEqual(self.result(r'3$^\circ$','<p>3</p>')['status'],'refused')
    def test_discretionary_hyphen_is_not_a_word_boundary(self):
        body=r'circum\-scrip\-tively / de\-fin\-i\-tively'
        self.assertEqual(self.result(body,'<p>circum\u00adscrip\u00adtively / de\u00adfin\u00adi\u00adtively</p>')['status'],'pass')
        self.assertEqual(self.result(body,'<p>circum scrip tively / de fin i tively</p>')['status'],'refused')

    def test_vertical_space_hint_does_not_end_horizontal_paragraph(self):
        for command in ('smallskip','medskip','bigskip'):
            body='First.\\'+command+'\\noindent Second.'
            self.assertEqual(self.result(body,'<p>First.Second.</p>')['status'],'pass')
            self.assertEqual(self.result(body,'<p>First.</p><p>Second.</p>')['status'],'refused')
        self.assertEqual(self.result('First.\\medskip\n\nSecond.','<p>First.</p><p>Second.</p>')['status'],'pass')

    def test_source_longarrow_allows_only_length_reflow(self):
        body=r'One $\longrightarrow$ Two $\longrightarrow$ Three.'
        self.assertEqual(self.result(body,'<p>One → Two → Three.</p>')['status'],'pass')
        for html in ('<p>One Two → Three.</p>','<p>One ← Two → Three.</p>','<p>One → Two Three.</p>'):
            self.assertEqual(self.result(body,html)['status'],'refused')
        self.assertEqual(len(self.ledger(body)['display_adaptations']),2)

    def test_page_reference_uses_exact_canonical_heading(self):
        body=r'See p.~\pageref{hist-job}.\par\section{Job: Suffering and Hope}\label{hist-job}Amen.'
        html='<p>See <a href="#hist-job">Job: Suffering and Hope</a>.</p><h2>Job: Suffering and Hope</h2><p>Amen.</p>'
        self.assertEqual(self.result(body,html)['status'],'pass')
        self.assertEqual(self.result(body,html.replace('>Job: Suffering and Hope</a>','>Invented text</a>'))['status'],'refused')
        self.assertEqual(self.result(body,html.replace('href="#hist-job"','href="#other"'))['status'],'refused')

    def test_section_reference_and_appendix_letter_are_source_derived(self):
        body=r'See \ref{child}, Appendix~\ref{app}.\par\section{First}\subsection{Child}\label{child}Amen.\appendix\section{Sources}\label{app}Done.'
        html='<p>See <a href="#child">1.1</a>, Appendix <a href="#app">A</a>.</p><h2>First</h2><h3>Child</h3><p>Amen.</p><h2>Sources</h2><p>Done.</p>'
        self.assertEqual(self.result(body,html)['status'],'pass')
        self.assertEqual(self.result(body,html.replace('>1.1</a>','>2.1</a>'))['status'],'refused')
        self.assertEqual(self.result(body,html.replace('>A</a>','>B</a>'))['status'],'refused')
        with self.assertRaises(coverage.CoverageError):self.ledger(r'See \pageref{missing}.')
        with self.assertRaises(coverage.CoverageError):self.ledger(r'\section{A}\label{twice}\label{twice}See \ref{twice}.')

    def test_reference_targets_are_bound_to_ordered_display_occurrences(self):
        body=r'See \ref{one} and \ref{two}.\par\section{First}\label{one}Alpha.\section{Second}\label{two}Beta.'
        html='<p>See <a href="#one">1</a> and <a href="#two">2</a>.</p><h2>First</h2><p>Alpha.</p><h2>Second</h2><p>Beta.</p>'
        self.assertEqual(self.result(body,html)['status'],'pass')
        swapped=html.replace('href="#one"','href="#swap"').replace('href="#two"','href="#one"').replace('href="#swap"','href="#two"')
        self.assertEqual(self.result(body,swapped)['status'],'refused')
    def test_reference_preserves_canonical_possessive_seam_and_local_display(self):
        body=r"Appendix~\ref{a}'s rule.\par\appendix\section{Sources}\label{a}Amen."
        html='<p>Appendix <a href="#a">A</a>’s rule.</p><h2>Sources</h2><p>Amen.</p>'
        self.assertEqual(self.result(body,html)['status'],'pass')
        self.assertEqual(self.result(body,html.replace('’s',' s'))['status'],'refused')
        self.assertEqual(self.result(body,html.replace('href="#a"','href="#other"'))['status'],'refused')
        self.assertEqual(self.result(body,html.replace('>A</a>’s',">A’s</a>"))['status'],'refused')
    def test_refstepcounter_currentlabel_survives_starred_heading(self):
        body=r'See Appendix~\ref{table}.\par\appendix\section{Scope}Amen.\refstepcounter{section}\label{matrix}\section*{Matrix}Rows.\refstepcounter{section}\label{table}\section*{Initiation}Rows.'
        html='<p>See Appendix <a href="#table">C</a>.</p><h2>Scope</h2><p>Amen.</p><h2>Matrix</h2><p>Rows.</p><h2>Initiation</h2><p>Rows.</p>'
        ledger=self.ledger(body)
        self.assertEqual(ledger['references'][0]['display'],'C')
        self.assertEqual(coverage.check_units(ledger,html+RIGHTS_HTML)['status'],'pass')
        self.assertEqual(coverage.check_units(ledger,html.replace('>C</a>','>app:table</a>')+RIGHTS_HTML)['status'],'refused')
    def test_currentlabel_is_scoped_but_counters_are_global(self):
        body=r'\section{First}{\refstepcounter{section}\label{inner}}\label{outer}See \ref{inner} and \ref{outer}.'
        ledger=self.ledger(body)
        self.assertEqual([reference['display'] for reference in ledger['references']],['2','1'])
        html='<h2>First</h2><p>See <a href="#inner">2</a> and <a href="#outer">1</a>.</p>'
        self.assertEqual(coverage.check_units(ledger,html+RIGHTS_HTML)['status'],'pass')
        with self.assertRaises(coverage.CoverageError):self.ledger(r'\section*{Unnumbered}\label{no-number}See \ref{no-number}.')
    def test_locators_are_bound_to_their_own_content_units(self):
        body=r'\href{https://example.org/one}{Read}.\par\href{https://example.org/two}{Read}.'
        html='<p><a href="https://example.org/one">Read</a>.</p><p><a href="https://example.org/two">Read</a>.</p>'
        self.assertEqual(self.result(body,html)['status'],'pass')
        swapped=html.replace('/one','/swap').replace('/two','/one').replace('/swap','/two')
        self.assertEqual(self.result(body,swapped)['status'],'refused')
        self.assertEqual(self.result('Read.','<p><a href="https://example.org/one">Read</a>.</p>')['status'],'refused')
    def test_hyperref_and_url_display_binding(self):
        body=r'\hyperref[anchor]{\textbf{Exact label}}; \url{https://example.org/x\?a\=1}.\par\section{Target}\label{anchor}Amen.'
        html='<p><a href="#anchor"><strong>Exact label</strong></a>; <a href="https://example.org/x?a=1">https://example.org/x?a=1</a>.</p><h2>Target</h2><p>Amen.</p>'
        self.assertEqual(self.result(body,html)['status'],'pass')
        self.assertEqual(self.result(body,html.replace('<a href="#anchor"><strong>Exact label</strong></a>','<a href="#anchor"><strong>Exact</strong></a> label'))['status'],'refused')
    def test_output_units_expose_absolute_raw_html_host_positions(self):
        html='\n<div>\n<p>Amen.<br>Deo gratias.</p>\n<img data-semantic-diagram="drawing"></div>'
        parser=coverage.HtmlLedger();parser.feed(html[:13]);parser.feed(html[13:]);units=parser.finish()
        self.assertEqual([(unit['host_start'],unit['host_tag']) for unit in units],[(html.index('<p>'),'p'),(html.index('<p>'),'p'),(html.index('<img '),'img')])
        self.assertEqual([unit['content_start'] for unit in units],[html.index('Amen.'),html.index('Deo gratias.'),html.index('<img ')])
        self.assertEqual([unit['index'] for unit in units],[0,1,2])

    def test_uri_context_decodes_tex_before_percent_encoded_unicode(self):
        body=r'\href{https\://example.org/Moli\%C3\%A8re\?x\=1\&y\=2\#here}{Name}.'
        html='<p><a href="https://example.org/Moli%C3%A8re?x=1&amp;y=2#here">Name</a>.</p>'
        self.assertEqual(self.result(body,html)['status'],'pass')
        self.assertNotEqual(coverage.uri_identity('https://example.org/a%23b'),coverage.uri_identity('https://example.org/a#b'))
    def test_material_percentage_currency_and_section_symbols(self):
        body=r'The rate is 5\%. Pay \$3; see \S~2.'
        html='<p>The rate is 5%. Pay $3; see § 2.</p>'
        self.assertEqual(self.result(body,html)['status'],'pass')
        for symbol in ('%','$','§'):
            self.assertEqual(self.result(body,html.replace(symbol,''))['status'],'refused')
    def test_primitive_counter_labels_are_source_owned(self):
        body=r'\refstepcounter{drawing}Drawing~\thedrawing.\par\refstepcounter{drawing}Drawing~\thedrawing.'
        self.assertEqual(self.result(body,'<p>Drawing 1.</p><p>Drawing 2.</p>')['status'],'pass')
        self.assertEqual(self.result(body,'<p>Drawing 2.</p><p>Drawing 1.</p>')['status'],'refused')
    def test_counter_read_events_bind_runtime_state_and_macro_programs(self):
        import hashlib
        head=r'\newcommand{\prefix}[1]{Drawing #1 \arabic{drawing}}\newcommand{\face}[1]{\textbf{{\prefix{#1}}}\par}'
        body=r'\newcounter{drawing}\stepcounter{drawing}\face{A}\stepcounter{drawing}\face{B}'
        ledger=self.ledger(body,head);events=ledger['counter_displays']
        self.assertEqual([event['rawdisplay'] for event in events],['1','2'])
        for index,event in enumerate(events):
            self.assertEqual(event['name'],'arabic');self.assertEqual(event['counter'],'drawing');self.assertEqual(event['format'],'arabic')
            self.assertEqual([frame['name'] for frame in event['expansion']],['face','prefix'])
            self.assertEqual([frame['occurrence'] for frame in event['expansion']],[index+1,index+1])
            source=body[event['source_offset']:event['source_end']]
            self.assertEqual(source,r'\face{'+('A' if index==0 else 'B')+'}')
            self.assertEqual(event['source_tex_sha256'],hashlib.sha256(source.encode()).hexdigest())
            child=event['expansion'][-1]
            parent=event['expansion'][0]
            self.assertEqual(parent['expanded_program'][child['program_offset']:child['program_end']],r'\prefix{'+('A' if index==0 else 'B')+'}')
            self.assertEqual(child['expanded_program'][event['program_offset']:event['program_end']],r'\arabic{drawing}')
            self.assertEqual(child['arguments'],['A' if index==0 else 'B'])
        self.assertEqual(coverage.check_units(ledger,'<p>Drawing A 1</p><p>Drawing B 2</p>'+RIGHTS_HTML)['status'],'pass')
        self.assertEqual(coverage.check_units(ledger,'<p>Drawing A 2</p><p>Drawing B 1</p>'+RIGHTS_HTML)['status'],'refused')
    def test_counter_events_exclude_implicit_label_reads(self):
        head=r'\newcommand{\show}{Value \thesection\par}'
        body=r'\appendix\refstepcounter{section}\show\refstepcounter{section}\show'
        events=self.ledger(body,head)['counter_displays']
        self.assertEqual([(event['name'],event['rawdisplay']) for event in events],[('thesection','A'),('thesection','B')])
    def test_counter_macro_in_heading_argument_keeps_canonical_span(self):
        body=r'\appendix\refstepcounter{section}\section*{\titlecounter}'
        ledger=self.ledger(body,r'\newcommand{\titlecounter}{Appendix \thesection}')
        event=ledger['counter_displays'][0]
        self.assertEqual(event['source_offset'],body.index(r'\titlecounter'))
        self.assertEqual(event['source_call'],r'\titlecounter')
        self.assertEqual(event['rawdisplay'],'A')
    def test_counter_event_carries_scoped_formatter_definition(self):
        head=r'\renewcommand{\thesection}{\Alph{section}}\newcommand{\show}{Value \thesection\par}'
        body=r'\refstepcounter{section}\show'
        events=self.ledger(body,head)['counter_displays']
        self.assertEqual(len(events),1)
        self.assertEqual((events[0]['name'],events[0]['read_command'],events[0]['format'],events[0]['rawdisplay']),('thesection','Alph','Alph','A'))
    def test_direct_table_command_form(self):
        body=r'\tabularx{\linewidth}{ll}Cue & Response\\Yes & Amen.\\\endtabularx'
        html='<table><tr><th>Cue</th><th>Response</th></tr><tr><td>Yes</td><td>Amen.</td></tr></table>'
        self.assertEqual(self.result(body,html)['status'],'pass')
    def test_dossier_event_uses_actual_canonical_signature_and_all_text(self):
        head=r'\newcommand{\dossierevent}[3]{Narrated event & #1 & #2 & #3\\}'
        body=r'\begin{tabular}{llll}\dossierevent{Passage}{Place}{Date}\end{tabular}'
        html='<table><tr><td>Narrated event</td><td>Passage</td><td>Place</td><td>Date</td></tr></table>'
        self.assertEqual(self.result(body,html,head)['status'],'pass')
        self.assertEqual(self.result(body,html.replace('Narrated event',''),head)['status'],'refused')
        note=r'\newcommand{\dossierprose}[1]{\multicolumn{4}{l}{Required label: #1}\\}'
        body=r'\begin{tabular}{llll}A & B & C & D\\\dossierprose{Amen.}\end{tabular}'
        html='<table><tr><td>A</td><td>B</td><td>C</td><td>D</td></tr></table><p>Required label: Amen.</p>'
        self.assertEqual(self.result(body,html,note)['status'],'pass')
        self.assertEqual(self.result(body,html.replace('Required label: ',''),note)['status'],'refused')
    def test_custom_environment_footer_is_a_physical_definition(self):
        head=r'\newenvironment{inventory}{\begin{longtable}{l}Header\\\endhead}{\end{longtable}}'
        body=r'\begin{inventory}Continued on next page\\\endfoot Final footer\\\endlastfoot Amen.\\\end{inventory}'
        html='<table><tr><th>Header</th></tr><tr><td>Amen.</td></tr></table>'
        result=self.result(body,html,head)
        self.assertEqual(result['status'],'pass',result['failures'])
    def test_canonical_comment_offsets_and_expansion_refs(self):
        body='First.\n\n'+r'\greet{Amen.}'
        selection={'head':RIGHTS+r'\newcommand{\greet}[1]{#1}','body':body,'sources':{},'selection':{'entrypoint':'src/gpt/test/main.tex'},'chunks':[{'path':'src/gpt/test/main.tex','occurrence':1,'selected_line':1,'text':'First.\n\n'},{'path':'src/gpt/test/fragment.tex','occurrence':2,'selected_line':40,'text':r'\greet{Amen.}'}]}
        ledger=coverage.expected_units(selection,self.library)
        unit=next(unit for unit in ledger['units'] if unit['expected']=='amen')
        self.assertEqual(unit['source_ref']['path'],'src/gpt/test/fragment.tex')
        self.assertEqual(unit['source_ref']['occurrence'],2)
        self.assertEqual(unit['source_ref']['selected_line'],40)
        self.assertEqual(unit['expansion'][0]['name'],'greet')
    def test_exact_diagram_source_and_asset_binding(self):
        import hashlib,json
        body=r'\begin{tikzpicture}\node {Amen};\end{tikzpicture}'
        asset={'start':0,'end':len(body),'source_tex_sha256':hashlib.sha256(body.encode()).hexdigest(),'asset_id':'tikz-'+'b'*24,'asset':'assets/drawing.svg','svg_sha256':'a'*64,'selection_digest':'selected','source_refs':[{'path':'source.tex','occurrence':1,'selected_line':1}],'labels':['Amen']}
        selection={'head':RIGHTS,'body':body,'sources':{},'selection':{'entrypoint':'source.tex','selection_digest':'selected'},'chunks':[],'diagram_assets':[asset]}
        ledger=coverage.expected_units(selection,self.library)
        labels=hashlib.sha256(json.dumps(['Amen'],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
        image='<figure data-semantic-asset="'+asset['asset_id']+'"><img data-semantic-diagram="'+asset['asset_id']+'" data-source-asset="'+asset['asset_id']+'" src="assets/drawing.svg" data-svg-sha256="'+asset['svg_sha256']+'" data-source-tex-sha256="'+asset['source_tex_sha256']+'" data-selection-digest="selected" data-source-labels-sha256="'+labels+'"></figure>'
        self.assertEqual(coverage.check_units(ledger,image+RIGHTS_HTML)['status'],'pass')
        self.assertEqual(coverage.check_units(ledger,image.replace(asset['svg_sha256'],'c'*64)+RIGHTS_HTML)['status'],'refused')
        self.assertEqual(coverage.check_units(ledger,RIGHTS_HTML)['status'],'refused')
        self.assertEqual(coverage.check_units(ledger,image+image+RIGHTS_HTML)['status'],'refused')
        altered={**selection,'body':body.replace('Amen','Other')}
        with self.assertRaises(coverage.CoverageError):coverage.expected_units(altered,self.library)
    def test_unbound_tikz_is_not_a_word_omission_exception(self):
        with self.assertRaises(coverage.CoverageError):self.ledger(r'\begin{tikzpicture}\node{Amen};\end{tikzpicture}')

    def test_numeric_words_are_material(self):
        self.assertEqual(self.result('Code of 1917.','<p>Code of 1983.</p>')['status'],'refused')
    def test_exact_revision_is_required(self):
        body=r'\AIDocumentRevisionTimestamp{2026-11-02T17:50:42Z}\AIModelContribution{Model}{qualifiers}{runtime}'
        self.assertEqual(self.result(body,'<p><strong>Last revised (UTC):</strong> 2026-11-02T17:50:42Z</p>')['status'],'pass')
        self.assertEqual(self.result(body,'<p><strong>Last revised (UTC):</strong> 2026-11-02T17:50:43Z</p>')['status'],'refused')
    def test_unknown_macro_environment_and_control_flow_refuse(self):
        for source in (r'\Unmodelled{Amen.}',r'\begin{unmodelled}Amen.\end{unmodelled}',r'\ifnum1=1 Amen.\fi'):
            with self.assertRaises(coverage.CoverageError):self.ledger(source)
    def test_real_exact_homily_canonical_units_have_occurrence_provenance(self):
        from _print_document import publication_recipe
        output='liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost-homily'
        recipe=publication_recipe('gpt',output,root=ROOT)
        selection=print_converter.selected_source(ROOT,recipe,self.library)
        ledger=coverage.expected_units(selection,self.library)
        self.assertGreater(len(ledger['units']),35)
        self.assertTrue(all(unit.get('source_ref') for unit in ledger['units']))
        self.assertEqual(ledger['role'],'homily')

if __name__=='__main__':unittest.main()
