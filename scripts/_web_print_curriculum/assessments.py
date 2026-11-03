"""Source-selected assessment companions with independent semantic coverage.

Canonical prose remains in the course owners. This adapter models their public
assessment selectors and refuses incomplete or unmodelled output.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

from . import core, independent_projection

Packet, CurriculumError, COURSE = core.Packet, core.CurriculumError, core.COURSE
FORM_ID=re.compile(r'[FCMA]-[ABC]\Z')


class Assessment(Packet):
    def __init__(self,root,recipe):
        self.assessment_selection=[]
        self.assessment_id=None
        self.assessment_number=0
        self.assessments=[]
        self.expected_assessments=[]
        self.assessment_groups=[]
        self.assessment_response_dimensions={}
        super().__init__(Path(root),recipe,allow_companion=True)
        if '/05-stage-assessments/' not in str(self.entry):
            raise CurriculumError('assessment adapter requires an assessment companion')

    def metadata(self):
        source=self.read(self.entry)
        return {d.name:d.macro[2] for kind,d in self.web.walk_definitions(source)
                if kind=='definition' and d.name and d.macro and d.macro[0]==0}

    def independent_plan(self):
        fields=self.metadata()
        identifiers=fields.get('AssessmentSelection','').split(',')
        if not identifiers or any(not FORM_ID.fullmatch(key) for key in identifiers):
            raise CurriculumError('assessment selection must name explicit stable form IDs')
        if len(set(identifiers))!=len(identifiers):
            raise CurriculumError('duplicate assessment form ID')
        self.selection_contract={name:fields.get(name,'') for name in ('CompanionID','AssessmentSelection','ReviewSourceSet','ReviewReaderSet')}
        self.selection_contract['modes']=['learner','solutions']
        self.macros['ModuleID']=(0,None,fields['CompanionID'])
        self.macros['ModuleTitle']=(0,None,fields['CompanionTitle'])
        source_path=self.root/'src/gpt'/COURSE/'shared/assessments/all.tex'
        source=self.read(source_path)
        discovered=set()
        groups=[]
        pos=0
        pattern=re.compile(r'\\begin\{assessmentgroup\}')
        while (found:=pattern.search(source,pos)):
            group_args,start=self.args(source,found.end(),2)
            group_body,pos=self.environment(source,start,'assessmentgroup')
            group_ids=group_args[0].split(',')
            for group_id in group_ids:
                if group_id in discovered:raise CurriculumError('duplicate source assessment ID '+group_id)
                discovered.add(group_id)
            if not set(group_ids).intersection(identifiers):continue
            forms=[]
            form_pos=0
            form_pattern=re.compile(r'\\begin\{assessment\}')
            while (form:=form_pattern.search(group_body,form_pos)):
                args,start=self.args(group_body,form.end(),4)
                body,form_pos=self.environment(group_body,start,'assessment')
                if args[0] not in identifiers:continue
                items=[]
                for ordinal,item in enumerate(re.finditer(r'\\AssessmentItem\b',body),1):
                    cursor=self.web.skip_gap(body,item.end())
                    if body[cursor:cursor+1]=='[':
                        cursor=body.index(']',cursor)+1
                    payloads,_=self.args(body,cursor,2)
                    items.append((args[0]+'.'+str(ordinal),payloads))
                forms.append({'id':args[0],'args':args,'body':body,'items':items,
                    'source_body_sha256':hashlib.sha256(body.encode()).hexdigest()})
            groups.append({'ids':group_ids,'title':group_args[1],'forms':forms})
        if set(identifiers)-discovered:
            raise CurriculumError('unknown assessment IDs: '+repr(sorted(set(identifiers)-discovered)))
        selected_forms=[form['id'] for group in groups for form in group['forms']]
        if len(selected_forms)!=len(set(selected_forms)) or set(selected_forms)!=set(identifiers):
            raise CurriculumError('selected assessment IDs lack exactly one canonical form')
        for mode,part in ((False,'Review Forms'),(True,'Answers and Models')):
            for group in groups:
                for form in group['forms']:
                    self.expected_assessments.append({'id':form['id'],'solutions':mode,'part':part,
                        'source_body_sha256':form['source_body_sha256']})
                    for stable,payloads in form['items']:
                        self.expected_items.append({'id':stable,'payloads':payloads,'solutions':mode,'part':part,
                            'source':source_path.relative_to(self.root).as_posix(),
                            'occurrence_id':part+':assessment:'+stable+('::solutions' if mode else '::learner')})
        for kind,keys in (('reviewsourceunit',fields.get('ReviewSourceSet','').split(',')),
                          ('courseunit',fields.get('ReviewReaderSet','').split(','))):
            selected={key for key in keys if key}
            if not selected:continue
            found_ids=set()
            reader_root=self.root/'src/gpt'/COURSE/'shared/content/readers'
            for file in ('ordinary-latin.tex','authentic-prose.tex','poetry-trunk.tex'):
                path=reader_root/file;raw=self.read(path);pos=0
                pattern=re.compile(r'\\begin\{'+kind+r'\}')
                while (found:=pattern.search(raw,pos)):
                    args,start=self.args(raw,found.end(),1)
                    body,pos=self.environment(raw,start,kind)
                    if args[0] not in selected:continue
                    found_ids.add(args[0])
                    self.expected_units.append({'id':args[0],'solutions':False,'part':'Included Latin',
                        'source':path.relative_to(self.root).as_posix(),'source_body_sha256':hashlib.sha256(body.encode()).hexdigest(),
                        'source_tex':body,'selected_line':raw[:found.start()].count('\n')+1,
                        'occurrence_id':'Included Latin:'+kind+':'+args[0]})
            if selected-found_ids:
                raise CurriculumError('unknown included Latin selection: '+repr(sorted(selected-found_ids)))

    def custom_command(self,name,text,pos,depth):
        if name=='SelectAssessments':
            args,pos=self.args(text,pos,1)
            value=self.scalar(args[0])
            selected=value.split(',')
            if any(not FORM_ID.fullmatch(key) for key in selected):
                raise CurriculumError('unmodelled assessment selector '+value)
            self.assessment_selection=selected
            return '',pos
        if name=='ifdefempty':
            args,pos=self.args(text,pos,3)
            value=self.scalar(args[0])
            if '\\' in value:raise CurriculumError('unresolved empty-test value '+value)
            return self.eval(args[1] if not value else args[2],depth+1),pos
        if name=='AssessmentItem':
            if self.assessment_id is None:raise CurriculumError('assessment item outside selected form')
            cursor=self.web.skip_gap(text,pos)
            height='0.65in'
            if text[cursor:cursor+1]=='[':
                end=text.index(']',cursor)
                height=text[cursor+1:end].strip();cursor=end+1
            if not re.fullmatch(r'(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)(?:in|em|ex|pt)',height):
                raise CurriculumError('unmodelled assessment response dimension '+height)
            args,pos=self.args(text,cursor,2)
            self.assessment_number+=1
            stable=self.assessment_id+'.'+str(self.assessment_number)
            self.items.append({'id':stable,'solutions':self.solutions,'part':self.part,
                'source':self.active_inputs[-1].relative_to(self.root).as_posix(),
                'payloads':args,'prompt':args[0],'answer':args[1]})
            ordinal=str(len(self.items))
            prompt=(' TRIPTYCHCURRICULUMPROMPTSTART'+ordinal+' '+self.eval(args[0],depth+1)
                    +' TRIPTYCHCURRICULUMPROMPTEND'+ordinal+' ')
            if self.solutions:
                answer=('\\par\\textbf{Answer / model:} TRIPTYCHCURRICULUMANSWERSTART'+ordinal+' '
                        +self.eval(args[1],depth+1)+' TRIPTYCHCURRICULUMANSWEREND'+ordinal+' ')
            else:
                marker=self.response('AssessmentItem',height).strip()
                self.assessment_response_dimensions[marker]=height
                answer='\\par '+marker+'\\par '
            return ('\\item \\begin{minipage}[t]{\\linewidth}\\textit{Item ID: '+stable+'}\\par '
                    +prompt+answer+'\\end{minipage}\n'),pos
        return None

    def postprocess_html(self,rendered):
        return rendered

    def custom_environment(self,name,text,pos,depth):
        if name=='assessmentgroup':
            args,pos=self.args(text,pos,2)
            body,pos=self.environment(text,pos,name)
            if not set(args[0].split(',')).intersection(self.assessment_selection):return '',pos
            self.assessment_groups.append({'ids':args[0],'title':args[1],'solutions':self.solutions})
            return '\\subsection{'+self.eval(args[1],depth+1)+'}\n'+self.eval(body,depth+1),pos
        if name=='assessment':
            args,pos=self.args(text,pos,4)
            body,pos=self.environment(text,pos,name)
            if args[0] not in self.assessment_selection:return '',pos
            self.assessments.append({'id':args[0],'solutions':self.solutions,'part':self.part,
                'source_body_sha256':hashlib.sha256(body.encode()).hexdigest()})
            old_id,old_number=self.assessment_id,self.assessment_number
            self.assessment_id=args[0];self.assessment_number=0
            try:
                content=self.eval(body,depth+1)
            finally:
                self.assessment_id,self.assessment_number=old_id,old_number
            return ('\\subsubsection*{'+self.eval(args[1],depth+1)+'}\n'
                '\\textbf{Review form ID:} '+args[0]+'\\par\n'
                '\\textbf{Focus:} '+self.eval(args[2],depth+1)+'\\par\n'
                '\\textbf{Use:} '+self.eval(args[3],depth+1)+'\\par\n'
                '\\begin{enumerate}\n'+content+'\\end{enumerate}\n'),pos
        return None

    def validate_selection(self):
        if self.assessments!=self.expected_assessments:
            raise CurriculumError('independent assessment form order/mode coverage failed')
        for actual,expected,keys in (
            (self.selected_units,self.expected_units,('id','solutions','part','source','source_body_sha256')),
            (self.items,self.expected_items,('id','solutions','part','source','payloads')),
        ):
            if [{key:row[key] for key in keys} for row in actual]!=[{key:row[key] for key in keys} for row in expected]:
                raise CurriculumError('independent assessment source occurrence/payload coverage failed')
        if self.registry_occurrences:
            raise CurriculumError('unexpected registry lookup in assessment selection')

    def canonical_projection(self,projector):
        """Read the independent source path; isolated tests may supply fixtures."""
        return projector.project_curriculum(self.root,self.recipe,self.web)

    def independent_semantic_ledger(self):
        selection=self.canonical_projection(independent_projection)
        for path,raw in selection['sources'].items():
            relative=path.relative_to(self.root).as_posix()
            if relative in self.sources and self.sources[relative]!=hashlib.sha256(raw.encode()).hexdigest():
                raise CurriculumError('canonical source changed between assessment renderer and independent planner: '+relative)
        import _web_print_semantics as semantic
        ledger=semantic.expected_units(selection,self.web)
        self._assessment_semantic_selection=selection
        return selection,ledger,semantic

    def render(self):
        result=super().render()
        result['print_type']='curriculum-assessment'
        result['assessment_forms']=self.assessments
        result['expected_assessment_forms']=self.expected_assessments
        for marker in sorted(self.assessment_response_dimensions,key=len,reverse=True):
            result['tex']=result['tex'].replace(marker,'')
        result['checks']['source_response_heights']=dict(self.assessment_response_dimensions)
        selection=self._assessment_semantic_selection
        ledger=result['semantic_ledger'];coverage=result['coverage_result']
        if not coverage.get('complete') or coverage.get('status')!='pass':
            raise CurriculumError('independent assessment semantic coverage refused: '+json.dumps(coverage['failures'][:8],ensure_ascii=False))
        result['coverage_result']=coverage
        result['expected_source_occurrences']=result['expected_units']
        result['expected_units']=ledger['units']
        result['semantic_ledger']=ledger
        result['projection_contract']=selection['projection_contract']
        result['canonical_projection']=selection['body']
        result['declared_selection_digest']=result['selection_digest']
        result['selection_digest']=selection['selection']['selection_digest']
        for part in result['parts']:
            part['source_unit_ids']=[row['id'] for row in ledger['units']]
        return result


def render_assessment(root,recipe):
    return Assessment(Path(root),recipe).render()
