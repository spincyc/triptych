"""Render the source-selected Guide, Reference, and Memory Workbook.

Every public result passes independent canonical-source semantic coverage.
"""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import tempfile
import tomllib

from .core import COURSE, CurriculumError, Packet, RESPONSE
from .independent_projection import project_curriculum
from _web_print_semantics import CoverageError, HtmlLedger, check_units, expected_units

COMPANIONS={'00-course-guide','00-reference-grammar','00-memory-workbook'}
SHEET_NAMES=('MemoryNewStudySheet','MemoryLatinToEnglishSheet','MemoryEnglishToLatinSheet',
             'MemoryMorphologySheet','MemoryUsageSheet','MemoryGrammarSheet',
             'MemoryReconstructionSheet','MemoryCompositionSheet')



class Companion(Packet):
    def __init__(self,root,recipe):
        self.render_calls=[];self.sheet_calls=[];self.field_calls=[];self.form_calls=[]
        self.first_memory_sheet=True
        self.lexicon_calls=0
        super().__init__(Path(root),recipe,allow_companion=True)
        self.companion=self.entry.parent.name
        if self.companion not in COMPANIONS:
            raise CurriculumError('not a selected course-wide companion')
        identity='publication:gpt/'+self.entry.parent.relative_to(self.root/'src/gpt').as_posix()
        if recipe.get('id')!=identity:
            raise CurriculumError('companion identity and canonical entrypoint disagree')
        for name in ('lexemes.tex','grammar-facts.tex','sets.tex'):
            self.definitions(self.read(self.root/'src/gpt'/COURSE/'shared/memory'/name))
        self.counts={'MemoryLexemeCount':len(self.lexemes),'MemoryGrammarFactCount':len(self.grammar),'MemorySetCount':len(self.sets)}

    def independent_plan(self):
        source=self.read(self.entry)
        definitions={d.name:d.macro[2] for kind,d in self.web.walk_definitions(source)
                     if kind=='definition' and d.name and d.macro and d.macro[0]==0}
        self.selection_contract={'entrypoint':self.recipe['entrypoint'],'companion_id':definitions['CompanionID'],
            'companion':self.companion,'registry_counts':self.counts}
        self.expected_render_calls=[];self.expected_sheet_calls=[];self.expected_field_calls=[]
        self.expected_form_calls=[]
        if self.companion=='00-course-guide':
            path=self.root/'src/gpt'/COURSE/'shared/content/practice-forms.tex'
            self.expected_form_calls=list(self.calls(self.read(path),'FormPage',2))
        elif self.companion=='00-reference-grammar':
            for ident in self.lexemes:
                for field in ('citation','sense','morphology','usage','strand','expectation'):
                    self.expected_field_calls.append(('lexemes.tex',ident,field,False))
        else:
            path=self.root/'src/gpt'/COURSE/'shared/content/memory-workbook/all.tex'
            source=self.read(path)
            names='RenderMemoryWorkbookLearnerPacket|RenderMemoryWorkbookSolutionPacket'
            for found in re.finditer(r'\\('+names+r')\s*\{',source):
                key,_=self.web.brace_group(source,found.end()-1)
                if key not in self.sets:raise CurriculumError('unknown workbook set '+key)
                mode=found[1]=='RenderMemoryWorkbookSolutionPacket'
                self.expected_render_calls.append((found[1],key))
                self.expected_field_calls.append(('sets.tex',key,'title',mode))
                definition=self.macros[found[1]][2]
                sheet_names=re.findall(r'\\(Memory[A-Za-z]+Sheet)\{#1\}',definition)
                if tuple(sheet_names)!=SHEET_NAMES:
                    raise CurriculumError('canonical eight-sheet contract changed')
                for name in sheet_names:
                    self.expected_sheet_calls.append((name,key,mode))
                    self.expected_field_calls.extend(self.expected_sheet_fields(name,key,mode))
            keys=['M'+str(i).zfill(2) for i in range(1,23)]+['P'+str(i) for i in range(1,9)]
            if self.expected_render_calls != [('RenderMemoryWorkbookLearnerPacket',key) for key in keys]+[('RenderMemoryWorkbookSolutionPacket',key) for key in keys]:
                raise CurriculumError('canonical workbook does not select all 30 learner then all 30 solution packets')
            self.selection_contract['workbook_calls']=self.expected_render_calls

    def expected_sheet_fields(self,name,key,mode):
        fields='title new rone rtwo rfive stage grammar'.split()
        def sequence(label):return [ident for ident in self.sets[key][fields.index(label)].split(',') if ident]
        def lexeme(ident,names):return [('lexemes.tex',ident,field,mode) for field in names]
        result=[]
        if name=='MemoryNewStudySheet':
            for ident in sequence('new'):result+=lexeme(ident,('citation','sense','morphology','usage','expectation','strand'))
        elif name=='MemoryLatinToEnglishSheet':
            for label in ('new','rone','rtwo','rfive','stage'):
                for ident in sequence(label):result+=lexeme(ident,('citation','sense') if mode else ('citation',))
        elif name=='MemoryEnglishToLatinSheet':
            for label in ('new','rfive','stage'):
                for ident in sequence(label):result+=lexeme(ident,('sense','citation') if mode else ('sense',))
        elif name=='MemoryMorphologySheet':
            for label in ('new','rtwo'):
                for ident in sequence(label):result+=lexeme(ident,('citation','morphology') if mode else ('citation',))
        elif name=='MemoryUsageSheet':
            for label in ('new','rone'):
                for ident in sequence(label):result+=lexeme(ident,('citation','usage') if mode else ('citation',))
        elif name=='MemoryGrammarSheet':
            for ident in sequence('grammar'):
                result += [('grammar-facts.tex',ident,field,mode) for field in (('title','family','prompt','answer') if mode else ('title','family','prompt'))]
        elif name=='MemoryReconstructionSheet':
            result += [('sets.tex',key,field,mode) for field in (('reconstruction','reconstructionmodel') if mode else ('reconstruction',))]
        elif name=='MemoryCompositionSheet':
            result += [('sets.tex',key,field,mode) for field in (('composition','compositionmodel') if mode else ('composition',))]
        else:raise CurriculumError('unmodelled workbook sheet '+name)
        return result

    def macro_expansion(self,name,text,pos,depth):
        call=self.web.macro_call(text,pos,self.macros[name])
        if call is None:raise CurriculumError('unreadable companion macro '+name)
        expanded,end=call
        return self.eval(expanded,depth+1),end

    def custom_command(self,name,text,pos,depth):
        if name=='removelastskip':
            return '',pos
        if name in {'input','include'}:
            args,end=self.args(text,pos,1);value=self.scalar(args[0])
            if value.removesuffix('.tex')==COURSE+'/shared/memory/renderers':
                self.read(self.root/'src/gpt'/COURSE/'shared/memory/renderers.tex')
                return '',end
        if name=='arabic':
            args,end=self.args(text,pos,1)
            if args[0] not in self.counts:raise CurriculumError('unknown visible registry counter '+args[0])
            return str(self.counts[args[0]]),end
        if name in {'firstmemorysheettrue','firstmemorysheetfalse'}:
            self.first_memory_sheet=name.endswith('true');return '',pos
        if name=='iffirstmemorysheet':
            return self.conditional(text,pos,self.first_memory_sheet)
        if name in {'RenderMemoryWorkbookLearnerPacket','RenderMemoryWorkbookSolutionPacket'}:
            args,_=self.args(text,pos,1);self.render_calls.append((name,self.scalar(args[0])))
            return self.macro_expansion(name,text,pos,depth)
        if name in SHEET_NAMES:
            args,_=self.args(text,pos,1);self.sheet_calls.append((name,self.scalar(args[0]),self.memorysolutions))
            return self.macro_expansion(name,text,pos,depth)
        if name=='RenderCompleteMemoryLexicon':
            self.lexicon_calls+=1;return self.macro_expansion(name,text,pos,depth)
        if name=='MemoryLexemeIDSequence':
            return self.eval(''.join(r'\MemorySequenceItem{'+ident+'}' for ident in self.lexemes),depth+1),pos
        if name=='noalign':
            args,end=self.args(text,pos,1);value=args[0].strip()
            match=re.match(r'\\gdef\\MemorySequenceItem##1\s*\{',value)
            if not match:raise CurriculumError('unmodelled noalign assignment')
            body,last=self.web.brace_group(value,match.end()-1)
            if value[last:].strip():raise CurriculumError('trailing source in sequence assignment')
            self.macros['MemorySequenceItem']=(1,None,body.replace('##','#'))
            return '',end
        if name in {'MemoryLexemeField','MemoryGrammarField','MemorySetField'}:
            args,end=self.args(text,pos,2);key,field=map(self.scalar,args)
            if name=='MemoryLexemeField':table,fields,file=self.lexemes,'citation sense morphology usage strand expectation'.split(),'lexemes.tex'
            elif name=='MemoryGrammarField':table,fields,file=self.grammar,'title family prompt answer'.split(),'grammar-facts.tex'
            elif field in {'reconstruction','reconstructionmodel','composition','compositionmodel'}:table,fields,file=self.prompts,'reconstruction reconstructionmodel composition compositionmodel'.split(),'sets.tex'
            else:table,fields,file=self.sets,'title new rone rtwo rfive stage grammar'.split(),'sets.tex'
            if key not in table or field not in fields:raise CurriculumError('unknown companion registry field '+key+'/'+field)
            self.field_calls.append((file,key,field,self.memorysolutions))
            return self.eval(table[key][fields.index(field)],depth+1),end
        if name=='FormPage':
            args,_=self.args(text,pos,2);self.form_calls.append(args)
            call=self.web.macro_call(text,pos,self.macros[name])
            if call is None:raise CurriculumError('unreadable canonical FormPage')
            expanded,end=call
            geometry=r'\ifdim\pagetotal=0pt\else\clearpage\fi'
            if geometry not in expanded:raise CurriculumError('FormPage geometry branch changed')
            return self.eval(expanded.replace(geometry,''),depth+1),end
        if name=='RuleLine':
            return '\\par '+self.response('RuleLine','0.22in')+'\\par ',pos
        return None

    def validate_selection(self):
        if self.render_calls != self.expected_render_calls:raise CurriculumError('workbook packet selection/order differs from canonical source')
        if self.sheet_calls != self.expected_sheet_calls:raise CurriculumError('workbook sheet selection/order differs from canonical source')
        if self.field_calls != self.expected_field_calls:raise CurriculumError('companion registry field occurrence order differs from canonical source')
        if self.form_calls != self.expected_form_calls:raise CurriculumError('Guide form source fields/order differ')
        if self.lexicon_calls != (1 if self.companion=='00-reference-grammar' else 0):raise CurriculumError('complete lexicon must render exactly once in its Reference')

    def make_parts(self,rendered):
        # All candidate boundaries are semantic top-level chapters/Parts. Check
        # each fragment's structure; never cut through a table or list to fit.
        pieces=re.split(r'(?=<h[23](?:\s|>))',rendered)
        parts=[];pending=''
        for piece in pieces:
            if not piece:continue
            candidate=pending+piece
            try:
                parser=HtmlLedger();parser.feed(candidate);parser.finish()
            except CoverageError:
                pending=candidate;continue
            if len(candidate.encode())>=750000:raise CurriculumError('one complete semantic companion section exceeds 750 KB')
            payload=candidate.encode()
            parts.append({'id':'part-'+str(len(parts)+1),'html':candidate,'bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest(),'html_sha256':hashlib.sha256(payload).hexdigest()});pending=''
        if pending:raise CurriculumError('unbalanced terminal companion fragment')
        if ''.join(part['html'] for part in parts)!=rendered:raise CurriculumError('semantic part splitting changed content/order')
        return parts

    def postprocess_html(self,rendered):
        number=0
        def identify(match):
            nonlocal number
            number+=1
            return match.group(0)[:-1]+' data-semantic-minipage="minipage-'+str(number)+'">'
        return re.sub(r'<div\b[^>]*\bclass="[^"]*\bminipage\b[^"]*"[^>]*>',identify,rendered)

    def render_content(self):
        body,shim=self.flatten()
        source=self.read(self.entry)
        title,subtitle=self.web.pdf_metadata(source.split(r'\begin{document}',1)[0])
        title=' '.join(self.scalar(title).split());subtitle=' '.join(self.scalar(subtitle).split())
        if '\\' in title+subtitle:raise CurriculumError('unmodelled companion title metadata')
        pandoc=self.pandoc_executable()
        scratch=self.root/'.scratch/web-print-curriculum'
        scratch.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='conversion-',dir=scratch) as folder:
            table_filter=Path(folder)/'tables.lua';table_filter.write_text(self.web.TABLE_FILTER)
            run=subprocess.run([pandoc,'-f','latex','-t','html5','--wrap=none','--shift-heading-level-by=1','--lua-filter='+str(table_filter)],
                input=shim+'\n\\begin{document}\n'+body+'\n\\end{document}\n',text=True,capture_output=True)
        if run.returncode or run.stderr.strip():raise CurriculumError('Pandoc refused companion: '+run.stderr)
        rendered=self.render_responses(run.stdout)
        rendered=self.postprocess_html(rendered)
        try:rendered=self.normalize_profile(rendered)
        except ValueError as error:raise CurriculumError('untyped companion HTML style: '+str(error)) from error
        if re.search(r'\\[A-Za-z]+',rendered):raise CurriculumError('unconverted companion control sequence')
        tables=self.web.table_count(body,shim)
        if tables!=len(re.findall(r'<table(?:\s|>)',rendered)):raise CurriculumError('companion source/HTML table count differs')
        lost=self.web.lost_cell_openings(self.strip_response_markers(body),rendered,shim)
        if lost:raise CurriculumError('companion source table cell opening lost: '+repr(lost))
        for required in ('Reuse and rights.','Last revised (UTC):'):
            if required not in rendered:raise CurriculumError('companion required notice missing: '+required)
        if any(name in rendered for name in ('AIModelContribution','AIGenerationProvenance','AIDocumentRevisionTimestamp')):
            raise CurriculumError('companion internal metadata escaped')
        content=rendered
        parts=[]
        return {'output_id':self.recipe['id'].removeprefix('publication:'),'print_type':tomllib.loads((self.entry.parent/'publication.toml').read_text())['kind'],
            'title':title,'subtitle':subtitle,'tex':body,'rendered':content,'parts':parts,'assets':[],
            'source_paths':self.sources,'source_digest':hashlib.sha256(json.dumps(self.sources,sort_keys=True).encode()).hexdigest(),
            'render_toolchain':self.pandoc_info,'html_profile':self.html_profile_info,
            'selection_digest':hashlib.sha256(json.dumps(self.selection_contract,sort_keys=True).encode()).hexdigest(),
            'selection':self.selection_contract,'checks':{'canonical_selection_and_field_order':'pass','tables':tables,'lost_table_openings':lost,
                'workbook_packet_views':len(self.render_calls),'workbook_sheet_views':len(self.sheet_calls),'registry_field_occurrences':len(self.field_calls),
                'guide_forms':len(self.form_calls),'parts':0,'max_part_bytes':0},
            'status':'generated-unreviewed'}

    def render(self):
        # The independent projector reads the original owner graph before the
        # renderer runs; it is never given converted TeX or output HTML.
        selection=project_curriculum(self.root,self.recipe,self.web)
        expected=expected_units(selection,self.web)
        result=self.render_content()
        coverage=check_units(expected,result['rendered'],self.web)
        if not coverage.get('complete'):
            error=CurriculumError('complete companion semantic source coverage failed')
            error.coverage=coverage
            raise error
        if any(Path(path).read_text()!=raw for path,raw in selection['sources'].items()):
            raise CurriculumError('canonical source changed during companion conversion')
        result['rendered']=self.bind_units(expected,result['rendered'],coverage)
        coverage=check_units(expected,result['rendered'],self.web)
        if not coverage.get('complete'):
            error=CurriculumError('bound companion semantic source coverage failed')
            error.coverage=coverage
            raise error
        result['print_binding']=self.print_binding_info
        result['expected_print_units']=self.expected_print_units
        from .response_geometry import check as check_geometry
        result['response_geometry_coverage']=check_geometry(selection['response_geometry'],result['rendered'])
        result['expected_response_geometry']=selection['response_geometry']
        result['parts']=self.make_parts(result['rendered'])
        result['checks']['parts']=len(result['parts'])
        result['checks']['max_part_bytes']=max(len(part['html'].encode()) for part in result['parts'])
        result['selector_digest']=result['selection_digest']
        result['selection_digest']=selection['selection']['selection_digest']
        result['projection_contract_id']=selection['projection_contract']['version']
        from _web_print_publication import unit_expectations
        result['print_unit_expectations']=unit_expectations(expected,self.expected_print_units)
        result['semantic_ledger']=expected
        result['expected_units']=expected['units'];result['coverage_result']=coverage
        result['html']='<!doctype html><html lang="en"><head><meta charset="utf-8"><title>'+html.escape(result['title'])+'</title></head><body>'+result['rendered']+'</body></html>\n'
        return result


def render_companion(root,recipe):return Companion(root,recipe).render()

