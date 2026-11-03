"""Strict source-owned metrical schemes for the eight curriculum poetry packets.

Only the finite scansion language actually present in the canonical owners is
accepted. Source ASTs/signatures are derived before the render pass. MathML
preserves every symbol, labelled underbrace and their exact sequence/grouping.
"""
from __future__ import annotations
import hashlib
import html
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

from .core import Packet,CurriculumError
from . import prose_coverage


class ScansionError(CurriculumError): pass


SYMBOLS={'smile':'⌣','times':'×','mid':'∣','Vert':'‖','parallel':'∥'}
COMMAND=re.compile(r'\\([A-Za-z@]+|.)',re.S)
MATHML_TAGS={'mrow','mo','mtext','munder'}


def canonical_json(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))


class ScansionParser:
    def __init__(self,source):self.source=source;self.pos=0
    def gap(self):
        while self.pos<len(self.source) and self.source[self.pos].isspace():self.pos+=1
    def group(self):
        self.gap()
        if self.source[self.pos:self.pos+1]!='{':raise ScansionError('scansion requires braced argument')
        start=self.pos+1;depth=1;self.pos+=1
        while self.pos<len(self.source):
            ch=self.source[self.pos]
            if ch=='\\':self.pos+=2;continue
            if ch=='{':depth+=1
            elif ch=='}':
                depth-=1
                if depth==0:
                    value=self.source[start:self.pos];self.pos+=1;return value
            self.pos+=1
        raise ScansionError('unclosed scansion group')
    def text(self,source):
        # Text-mode mathematical labels may contain the source's explicit
        # $...$ metrical symbols; no arbitrary text command is ignored.
        children=[];cursor=0
        for found in re.finditer(r'\$([^$]*)\$',source,re.S):
            if '\\' in source[cursor:found.start()]:raise ScansionError('unsupported scansion text control')
            plain=' '.join(source[cursor:found.start()].split()).replace('---','—').replace('--','–')
            if plain:children.append({'kind':'text','value':plain})
            children.append(ScansionParser(found[1]).parse())
            cursor=found.end()
        rest=source[cursor:]
        if '$' in rest or '\\' in rest:raise ScansionError('unsupported or unclosed scansion text control')
        plain=' '.join(rest.split()).replace('---','—').replace('--','–')
        if plain:children.append({'kind':'text','value':plain})
        return {'kind':'row','children':children}
    def parse(self):
        children=[]
        while self.pos<len(self.source):
            self.gap()
            if self.pos>=len(self.source):break
            ch=self.source[self.pos]
            if ch=='\\':
                found=COMMAND.match(self.source,self.pos)
                if found is None:raise ScansionError('unreadable scansion control')
                name=found[1];self.pos=found.end()
                if name in SYMBOLS:children.append({'kind':'symbol','value':SYMBOLS[name]})
                elif name in {',',';',':',' ','!'}:
                    # Pure spacing has no metrical or verbal payload. It remains
                    # in the AST binding without inventing a content token.
                    children.append({'kind':'spacing','source':name})
                elif name=='text':children.append(self.text(self.group()))
                elif name=='underbrace':
                    body=ScansionParser(self.group()).parse();self.gap()
                    if self.source[self.pos:self.pos+1]!='_':raise ScansionError('labelled underbrace requires its source label')
                    self.pos+=1
                    label_source=self.group()
                    label_parser=ScansionParser(label_source)
                    label=label_parser.parse()
                    children.append({'kind':'underbrace','body':body,'label':label})
                else:raise ScansionError('unsupported scansion control: \\'+name)
            elif ch in '.,|':
                children.append({'kind':'symbol','value':ch});self.pos+=1
            elif ch=='{':children.append(ScansionParser(self.group()).parse())
            else:raise ScansionError('unsupported scansion token: '+repr(ch))
        return {'kind':'row','children':children}


def ast_signature(ast):
    kind=ast['kind']
    if kind=='spacing':return []
    if kind in {'symbol','text'}:
        tag='mo' if kind=='symbol' else 'mtext'
        return [['start',tag],['text',ast['value']],['end',tag]]
    if kind=='row':
        return [['start','mrow']]+[record for child in ast['children'] for record in ast_signature(child)]+[['end','mrow']]
    if kind=='underbrace':
        return ([['start','munder'],['start','munder']]+ast_signature(ast['body'])
                +[['start','mo'],['text','⏟'],['end','mo'],['end','munder']]
                +ast_signature(ast['label'])+[['end','munder']])
    raise ScansionError('unknown AST node: '+kind)


def render_ast(ast):
    kind=ast['kind']
    if kind=='spacing':return ''
    if kind in {'symbol','text'}:
        tag='mo' if kind=='symbol' else 'mtext'
        return '<'+tag+'>'+html.escape(ast['value'])+'</'+tag+'>'
    if kind=='row':return '<mrow>'+''.join(render_ast(child) for child in ast['children'])+'</mrow>'
    if kind=='underbrace':
        return '<munder><munder>'+render_ast(ast['body'])+'<mo>⏟</mo></munder>'+render_ast(ast['label'])+'</munder>'
    raise ScansionError('unknown AST node: '+kind)


def mathml_signature(markup):
    try:element=ET.fromstring(markup)
    except ET.ParseError as error:raise ScansionError('malformed rendered MathML') from error
    if element.tag.split('}')[-1]!='math':raise ScansionError('math unit lacks math root')
    result=[]
    def visit(node):
        tag=node.tag.split('}')[-1]
        if tag not in MATHML_TAGS:raise ScansionError('unsupported rendered MathML tag: '+tag)
        if node.attrib:raise ScansionError('unexpected semantic MathML attribute')
        result.append(['start',tag])
        if node.text:
            if tag in {'mo','mtext'}:result.append(['text',node.text])
            elif node.text.strip():raise ScansionError('untyped MathML text')
        for child in node:
            visit(child)
            if child.tail and child.tail.strip():raise ScansionError('untyped MathML tail')
        result.append(['end',tag])
    for child in element:visit(child)
    return result


def verify_math_units(rendered,units):
    actual=[]
    for found in re.finditer(r'<math\b[^>]*>.*?</math>',rendered,re.S):
        try:element=ET.fromstring(found.group())
        except ET.ParseError as error:raise ScansionError('malformed math output') from error
        ident=element.attrib.get('data-semantic-unit')
        if ident not in units:raise ScansionError('unplanned semantic math output')
        signature=mathml_signature(found.group())
        if signature!=units[ident]['expected_mathml_signature']:raise ScansionError('source scansion symbol/group signature changed')
        actual.append(ident)
    if actual!=list(units):raise ScansionError('source scansion occurrence order or count changed')
    return {'status':'pass','complete':True,'unit_count':len(units),'ordered_ids':actual}


class WindowHTML(HTMLParser):
    def __init__(self,print_units=()):
        super().__init__(convert_charrefs=True);self.depth=0;self.active=None;self.line=None;self.windows=[]
        self.print_units=set(print_units);self.marker=False;self.seen_markers=set()
    def handle_starttag(self,tag,attrs):
        if self.marker:raise ScansionError('received-text print marker must be empty')
        raw_attrs=attrs
        attrs=dict(attrs)
        if tag not in {'br','hr','img','input','meta','link'}:self.depth+=1
        if tag=='div' and 'data-poetry-window' in attrs:
            if self.active is not None:raise ScansionError('nested received-text windows')
            self.active={'occurrence':int(attrs['data-poetry-window']),'name':attrs['data-poetry-window-name'],'lines':[],'depth':self.depth}
        elif self.active:
            if tag=='span':
                identity=attrs.get('data-print-unit')
                if self.line is None or len(raw_attrs)!=1 or set(attrs)!={'data-print-unit'} or identity not in self.print_units or identity in self.seen_markers:
                    raise ScansionError('received-text print marker lacks an exact canonical identity')
                self.marker=True;self.seen_markers.add(identity)
                return
            if tag not in {'p','em'}:raise ScansionError('unmodelled received-text window markup: '+tag)
            if tag=='p':
                if self.line is not None:raise ScansionError('nested received-text verse lines')
                expected=str(len(self.active['lines'])+1)
                if attrs.get('data-poetry-line')!=expected:raise ScansionError('received-text line ID or order changed')
                self.line=[]
    def handle_data(self,value):
        if self.marker and value:raise ScansionError('received-text print marker must be empty')
        if self.line is not None:self.line.append(value)
        elif self.active and value.strip():raise ScansionError('unassigned text inside received-text window')
    def handle_endtag(self,tag):
        if self.marker:
            if tag!='span':raise ScansionError('received-text print marker must close explicitly')
            self.marker=False;self.depth-=1
            return
        if self.active and tag=='p':
            if self.line is None:raise ScansionError('unbalanced received-text verse line')
            self.active['lines'].append(' '.join(''.join(self.line).split()));self.line=None
        if self.active and tag=='div' and self.depth==self.active['depth']:
            record=dict(self.active);record.pop('depth');self.windows.append(record);self.active=None
        if tag not in {'br','hr','img','input','meta','link'}:self.depth-=1

    def handle_startendtag(self,tag,attrs):
        if self.active and tag=='span':raise ScansionError('received-text print marker must close explicitly')
        self.handle_starttag(tag,attrs)
        if tag not in {'br','hr','img','input','meta','link'}:self.handle_endtag(tag)

    def handle_comment(self,value):
        if self.marker:raise ScansionError('received-text print marker must be empty')

    def handle_decl(self,value):
        if self.marker:raise ScansionError('received-text print marker must be empty')

    def handle_pi(self,value):
        if self.marker:raise ScansionError('received-text print marker must be empty')


def verify_windows(rendered,windows,print_units=()):
    parser=WindowHTML(print_units);parser.feed(rendered)
    if parser.active or parser.line is not None or parser.marker:raise ScansionError('unclosed received-text window')
    expected=[{'occurrence':n,'name':row['name'],'lines':row['lines']} for n,row in enumerate(windows,1)]
    if parser.windows!=expected:raise ScansionError('received-text window words, lineation, grouping or order changed')
    return {'status':'pass','complete':True,'occurrences':len(windows),'line_count':sum(len(row['lines']) for row in windows)}


class PoetryPacket(Packet):
    def __init__(self,root,recipe):
        self.semantic_units={};self.math_by_source={};self.math_seen=[];self.math_checks=[]
        self.window_definitions={};self.expected_windows=[];self.window_seen=[];self.window_checks=[]
        super().__init__(root,recipe)
        if '/04-advanced/poetry/' not in recipe['entrypoint']:
            raise ScansionError('poetry adapter requires an exact poetry packet entrypoint')

    def independent_plan(self):
        super().independent_plan()
        window_path=self.root/'src/gpt/curriculums/ecclesiastical-latin/shared/content/poetry-advanced/source-windows.tex'
        window_source=self.read(window_path)
        for kind,definition in self.web.walk_definitions(window_source):
            if kind!='definition' or not definition.name or not definition.name.startswith('Poetry'):continue
            if definition.macro is None or definition.macro[:2]!=(0,None):raise ScansionError('source window API must be a zero-argument canonical text macro')
            source=definition.macro[2].strip()
            found=re.match(r'\\Latin\s*\{',source)
            if not found:raise ScansionError('source window must declare its Latin text')
            payload,end=self.web.brace_group(source,found.end()-1)
            if source[end:].strip():raise ScansionError('unmodelled source-window tail')
            lines=[' '.join(value.split()) for value in re.split(r'\\\\(?:\[[^\]]*\])?',payload)]
            if not lines or any(not line or '\\' in line for line in lines):raise ScansionError('unmodelled source-window line or control')
            self.window_definitions[definition.name]={'source':window_path.relative_to(self.root).as_posix(),
                'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'source_tex':source,'lines':lines,
                'source_line':window_source[:definition.start].count('\n')+1}
        for row in self.expected_units:
            active=prose_coverage.project_unit(row['source_tex'],row['solutions'],row['part'],self.web)
            pattern=r'\\('+'|'.join(map(re.escape,self.window_definitions))+r')\b'
            for found in re.finditer(pattern,active):
                self.expected_windows.append({'name':found[1],'part':row['part'],'solutions':row['solutions'],
                    'call_source':row['source'],'source_ref':{'path':row['source'],'occurrence':row['occurrence_id'],'selected_line':row['selected_line']},
                    **self.window_definitions[found[1]]})
            for found in re.finditer(r'\\\[(.*?)\\\]',row['source_tex'],re.S):
                raw=found.group();ast=ScansionParser(found[1]).parse()
                digest=hashlib.sha256(raw.encode()).hexdigest()
                ident='poetry-scansion-'+digest[:20]
                if ident in self.semantic_units:raise ScansionError('duplicate scansion source occurrence requires an explicit occurrence key')
                source=(self.root/row['source']).read_text()
                start=source.find(raw)
                if start<0:raise ScansionError('scansion display not found in exact canonical owner')
                unit={'kind':'math','id':ident,'source_ref':{'path':row['source'],'occurrence':row['occurrence_id'],'selected_line':source[:start].count('\n')+1},
                      'source_sha256':digest,'ast_digest':hashlib.sha256(canonical_json(ast).encode()).hexdigest(),
                      'expected_mathml_signature':ast_signature(ast),'ast':ast,'source_tex':raw}
                self.semantic_units[ident]=unit;self.math_by_source[raw]=ident

    def custom_command(self,name,text,pos,depth):
        if name in self.window_definitions:
            index=len(self.window_seen)
            if index>=len(self.expected_windows):raise ScansionError('unplanned received-text window occurrence')
            expected=self.expected_windows[index]
            source=self.active_inputs[-1].relative_to(self.root).as_posix()
            if (name,self.part,self.solutions,source)!=(expected['name'],expected['part'],expected['solutions'],expected['call_source']):
                raise ScansionError('received-text window selection or source occurrence order differs')
            self.window_seen.append(name)
            return ' TRIPTYCHPOETRYWINDOW'+str(index+1)+' ',pos
        if name!='[':return super().custom_command(name,text,pos,depth)
        closing=text.find(r'\]',pos)
        if closing<0:raise ScansionError('unclosed source display math')
        raw=r'\['+text[pos:closing]+r'\]'
        if raw not in self.math_by_source:raise ScansionError('unplanned active scansion display')
        ident=self.math_by_source[raw];self.math_seen.append(ident)
        return '\\par TRIPTYCHPOETRYMATH'+ident.replace('-','X')+'\\par ',closing+2

    def validate_selection(self):
        super().validate_selection()
        if self.math_seen!=list(self.semantic_units):raise ScansionError('canonical math source occurrence order differs')
        if self.window_seen!=[row['name'] for row in self.expected_windows]:raise ScansionError('canonical received-text window occurrences differ')

    def postprocess_html(self,rendered):
        rendered=super().postprocess_html(rendered)
        for index,window in enumerate(self.expected_windows,1):
            marker='TRIPTYCHPOETRYWINDOW'+str(index)
            if rendered.count(marker)!=1:raise ScansionError('received-text window lost or duplicated')
            lines=''.join('<p class="poetry-verse-line" data-poetry-line="'+str(n)+'" style="margin:0"><em>'+html.escape(line)+'</em></p>'
                          for n,line in enumerate(window['lines'],1))
            unit='<div class="poetry-source-window" data-poetry-window="'+str(index)+'" data-poetry-window-name="'+window['name']+'">'+lines+'</div>'
            paragraph=r'<p>\s*'+re.escape(marker)+r'\s*</p>'
            if len(re.findall(paragraph,rendered))!=1:raise ScansionError('source-window paragraph boundary changed')
            rendered=re.sub(paragraph,unit,rendered)
            self.window_checks.append({'occurrence':index,'name':window['name'],'line_count':len(window['lines']),'status':'pass'})
        for ident,unit in self.semantic_units.items():
            marker='TRIPTYCHPOETRYMATH'+ident.replace('-','X')
            math='<math xmlns="http://www.w3.org/1998/Math/MathML" display="block" data-semantic-unit="'+ident+'">'+render_ast(unit['ast'])+'</math>'
            actual=mathml_signature(math)
            if actual!=unit['expected_mathml_signature']:raise ScansionError('rendered scansion tokens or grouping differ from canonical AST')
            pattern=r'<p>\s*'+re.escape(marker)+r'\s*</p>'
            if len(re.findall(pattern,rendered))!=1:raise ScansionError('metrical display was lost, duplicated or merged')
            rendered=re.sub(pattern,'<p class="poetry-scansion">'+math+'</p>',rendered)
            self.math_checks.append({'id':ident,'status':'pass','signature':actual})
        return rendered

    def semantic_projection(self,body):
        for ident in self.semantic_units:
            marker='TRIPTYCHPOETRYMATH'+ident.replace('-','X')
            body=body.replace(marker,r'\SemanticMathUnit{'+ident+'}')
        for index,window in enumerate(self.expected_windows,1):
            body=body.replace('TRIPTYCHPOETRYWINDOW'+str(index),window['source_tex'])
        return body

    def canonical_semantic_projection(self,body):
        """Project only raw canonical displays for the independent source gate.

        This receives the source planner's text, never rendered markers or
        HTML. A display not present in the independently selected canonical
        math inventory refuses rather than becoming an empty content block.
        """
        selected=[]
        def replace(found):
            raw=found.group()
            ident=self.math_by_source.get(raw)
            if ident is None:raise ScansionError('independent source planner encountered an unplanned math display')
            # Bind exact source bytes and parsed grouping again at this edge.
            unit=self.semantic_units[ident]
            if hashlib.sha256(raw.encode()).hexdigest()!=unit['source_sha256']:
                raise ScansionError('independent scansion source bytes differ')
            selected.append(ident)
            return r'\SemanticMathUnit{'+ident+'}'
        projected=re.sub(r'\\\[.*?\\\]',replace,body,flags=re.S)
        if selected!=list(self.semantic_units):raise ScansionError('independent canonical math display order or count differs')
        return projected,self.semantic_units

    def render(self):
        result=super().render()
        result['semantic_units']=self.semantic_units
        result['math_coverage']=verify_math_units(result['html'],self.semantic_units)
        result['source_windows']={'occurrences':self.expected_windows,'coverage':verify_windows(result['html'],self.expected_windows,result['expected_print_units']),'checks':self.window_checks}
        result['semantic_projection']=self.semantic_projection(result['tex'])
        return result


def render_packet(root,recipe):
    return PoetryPacket(Path(root),recipe).render()
