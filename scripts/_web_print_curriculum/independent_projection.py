"""Canonical curriculum DSL projection for the independent semantic ledger.

This evaluator reads original source, declarations and formatter bodies. It does
not import Packet, inspect generated TeX/HTML, or use the presentation shim.
Runtime-only course APIs have typed source contracts; all visible formatter
wording comes from its canonical definitions, including short labels and notes.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re

COURSE='curriculums/ecclesiastical-latin'
CONTROL=re.compile(r'\\([A-Za-z@]+|.)',re.S)
ENVIRON=re.compile(r'\\NewEnviron\s*\{')

# These finite metrics are the writing geometry executed by the canonical
# course formatter, memory renderer and guide forms. New source dimensions
# require an explicit browser-print geometry contract.
RESPONSE_HEIGHTS=frozenset({'0.22in','0.38in','0.65in','0.7in','0.8in','0.9in',
    '1.0in','1.1in','1.15in','1.2in','1.3in','1.4in',r'1.1\baselineskip'})
ROW_HEIGHTS=frozenset({'0.5in','0.52in','0.55in','0.62in','0.65in','0.72in',
    '0.76in','0.78in','0.82in',r'2.2\baselineskip'})
GEOMETRY_ORIGINS=frozenset({'Exercise','ShortExercise','LongExercise',
    'PassageExercise','AssessmentItem','RuleLine'})


class ProjectionError(ValueError):pass


class CanonicalProjector:
    def __init__(self,root,recipe,library,math_adapter=None):
        self.root=Path(root).resolve();self.recipe=recipe;self.web=library
        self.macros={};self.environments={};self.flags={};self.counters={};self.parents={}
        self.definition_sources={}
        self.registry={'lexeme':{},'grammar':{},'set':{},'prompt':{}}
        self.sources={};self.stack=[];self.active=[];self.chunks=[];self.occurrence=0
        self.global_next=False;self.depth=0;self.math_adapter=math_adapter;self.semantic_units={}
        self.entrypoint=recipe['entrypoint'];self.active_source=self.entrypoint;self.part='Cover'
        self.runtime_contracts={};self.selection_events=[];self.field_events=[]
        self.response_geometry=[];self.geometry_origins=[];self.macro_stack=[]

    def source(self,path):
        path=Path(path).resolve()
        if not path.is_relative_to(self.root/'src') or not path.is_file():raise ProjectionError('missing or escaping source '+str(path))
        raw=path.read_text();self.sources[path]=raw
        return self.web.strip_tex_comments(raw)

    def args(self,text,pos,count,default=None):
        out=[]
        for n in range(count):
            pos=self.web.skip_gap(text,pos)
            if n==0 and default is not None:
                if text[pos:pos+1]=='[':
                    end=text.find(']',pos)
                    if end<0:raise ProjectionError('unclosed optional source argument')
                    out.append(text[pos+1:end]);pos=end+1
                else:out.append(default)
            else:
                if text[pos:pos+1]!='{':raise ProjectionError('expected source group near '+repr(text[pos:pos+80]))
                value,pos=self.web.brace_group(text,pos);out.append(value)
        return out,pos

    def substitute(self,body,args):
        body=body.replace('##','\x00PARAM\x00')
        for n,value in reversed(list(enumerate(args,1))):body=body.replace('#'+str(n),value)
        return body.replace('\x00PARAM\x00','#')

    def assign(self,name,macro,glob=False):
        self.macros[name]=macro
        self.definition_sources[name]={'path':self.active_source,'sha256':hashlib.sha256(macro[2].encode()).hexdigest()}
        if glob or self.global_next:
            for frame in self.stack:
                frame[0][name]=macro;frame[2][name]=self.definition_sources[name]
        self.global_next=False

    def boolean(self,name,value):
        self.flags[name]=value
        if self.global_next:
            for frame in self.stack:frame[1][name]=value
        self.global_next=False

    def push(self):self.stack.append((dict(self.macros),dict(self.flags),dict(self.definition_sources)))
    def pop(self):
        if not self.stack:raise ProjectionError('unbalanced source scope')
        self.macros,self.flags,self.definition_sources=self.stack.pop()

    def scalar(self,text):
        for _ in range(60):
            changed=False
            def replace(match):
                nonlocal changed
                macro=self.macros.get(match[1])
                if macro and macro[0]==0:
                    changed=True;return macro[2]
                return match.group()
            text=CONTROL.sub(replace,text)
            if not changed:return text.strip()
        raise ProjectionError('recursive source scalar')

    def definitions(self,source,source_path=None):
        for kind,definition in self.web.walk_definitions(source):
            if kind!='definition' or definition.name is None:continue
            if definition.command=='let':
                if definition.source in self.macros:self.macros[definition.name]=self.macros[definition.source]
            elif definition.macro is not None:
                if definition.command!='providecommand' or definition.name not in self.macros:self.macros[definition.name]=definition.macro
        for kind,definition in self.web.walk_definitions(source):
            if kind=='definition' and definition.name and definition.name in self.macros:
                self.definition_sources[definition.name]={'path':source_path or self.active_source,
                    'sha256':hashlib.sha256(self.macros[definition.name][2].encode()).hexdigest()}
        for found in ENVIRON.finditer(source):
            values,pos=self.args(source,found.end()-1,1);name=values[0];pos=self.web.skip_gap(source,pos);count=0
            if source[pos:pos+1]=='[':
                end=source.index(']',pos);count=int(source[pos+1:end]);pos=end+1
            values,pos=self.args(source,pos,1)
            self.environments[name]=(count,None,values[0])
        for found in re.finditer(r'\\(?:new|renew)environment\s*\{',source):
            values,pos=self.args(source,found.end()-1,1);name=values[0];pos=self.web.skip_gap(source,pos);count=0;default=None
            if source[pos:pos+1]=='[':
                end=source.index(']',pos);count=int(source[pos+1:end]);pos=self.web.skip_gap(source,end+1)
                if source[pos:pos+1]=='[':end=source.index(']',pos);default=source[pos+1:end];pos=end+1
            values,pos=self.args(source,pos,2)
            self.environments[name]=(count,default,values[0]+r'\BODY'+values[1])
        for found in re.finditer(r'\\newif\s*\\if([A-Za-z@]+)',source):self.flags.setdefault(found[1],False)
        for found in re.finditer(r'\\newcounter\s*\{([^}]+)\}(?:\[([^]]+)\])?',source):
            self.counters.setdefault(found[1],0)
            if found[2]:self.parents[found[1]]=found[2]

    def declared(self,source,name,count):
        for found in re.finditer(r'\\'+re.escape(name)+r'\s*\{',source):
            values,_=self.args(source,found.end()-1,count);yield values

    def library(self,path):
        source=self.source(path);self.definitions(source,Path(path).relative_to(self.root).as_posix())
        self.runtime_contracts[str(Path(path).relative_to(self.root))]=hashlib.sha256(source.encode()).hexdigest()

    def registry_source(self,path,source):
        filename=Path(path).name
        self.definitions(source,Path(path).relative_to(self.root).as_posix())
        forms={'lexemes.tex':('lexeme','DeclareMemoryLexeme',7,'MemoryLexemeCount'),
               'grammar-facts.tex':('grammar','DeclareMemoryGrammarFact',5,'MemoryGrammarFactCount'),
               'sets.tex':('set','DeclareMemorySet',8,'MemorySetCount')}
        if filename not in forms:return False
        kind,command,count,counter=forms[filename]
        for row in self.declared(source,command,count):
            if row[0] in self.registry[kind] and self.registry[kind][row[0]]!=row[1:]:raise ProjectionError('conflicting canonical registry '+row[0])
            self.registry[kind][row[0]]=row[1:]
        self.counters[counter]=len(self.registry[kind])
        if filename=='sets.tex':
            for row in self.declared(source,'DeclareMemoryPrompts',5):self.registry['prompt'][row[0]]=row[1:]
        return True

    def include(self,name):
        name=self.scalar(name)
        if name=='common/preamble':
            self.source(self.root/'src/common/preamble.tex');return ''
        path=self.root/'src/gpt'/name
        if not path.suffix:path=path.with_suffix('.tex')
        path=path.resolve()
        if path in self.active:raise ProjectionError('recursive canonical include '+name)
        source=self.source(path)
        if path.name=='course-format.sty':self.library(path);return ''
        if path.name in {'lexemes.tex','grammar-facts.tex','sets.tex'} and 'shared/memory/' in name:
            self.registry_source(path,source);return ''
        self.active.append(path);prior=self.active_source;self.active_source=path.relative_to(self.root).as_posix()
        try:return self.walk(source)
        finally:self.active.pop();self.active_source=prior

    def env_body(self,text,pos,name):
        depth=1
        for found in re.finditer(r'\\(begin|end)\{'+re.escape(name)+r'\}',text[pos:]):
            depth+=1 if found[1]=='begin' else -1
            if depth==0:return text[pos:pos+found.start()],pos+found.end()
        raise ProjectionError('unclosed canonical environment '+name)

    def branch(self,text,pos,truth):
        depth=1;split=None
        for found in re.finditer(r'\\(if[A-Za-z@]*|else|fi)\b',text[pos:]):
            if found[1].startswith('if'):depth+=1
            elif found[1]=='fi':
                depth-=1
                if depth==0:
                    first=text[pos:pos+split.start() if split else pos+found.start()]
                    second=text[pos+split.end():pos+found.start()] if split else ''
                    return self.walk(first if truth else second),pos+found.end()
            elif depth==1:split=found
        raise ProjectionError('unclosed canonical conditional')

    def input_path(self,name):
        name=self.scalar(name);path=self.root/'src/gpt'/name
        return path if path.suffix else path.with_suffix('.tex')

    def row(self,key,field,source):
        fields={'lexeme':'citation sense morphology usage strand expectation'.split(),
                'grammar':'title family prompt answer'.split(),'set':'title new rone rtwo rfive stage grammar'.split(),
                'prompt':'reconstruction reconstructionmodel composition compositionmodel'.split()}
        if key not in self.registry[source] or field not in fields[source]:raise ProjectionError('unknown canonical field '+key+'/'+field)
        value=self.registry[source][key][fields[source].index(field)]
        self.field_events.append({'registry':source,'id':key,'field':field,'solutions':self.flags.get('solutions',False),'memorysolutions':self.flags.get('memorysolutions',False),'source_payload_digest':hashlib.sha256(value.encode()).hexdigest()})
        return value

    def geometry(self,kind,macro,*,height,width='linewidth',lines=1,rule='hrulefill',origin=None,payload=None,canonical_origin=None):
        """Record executed source geometry independently of any renderer output."""
        ordinal=len(self.response_geometry)+1
        origin=canonical_origin or (self.geometry_origins[0] if self.geometry_origins else origin or macro)
        refs=[]
        for name in dict.fromkeys([*self.geometry_origins,macro]):
            if name in self.definition_sources:refs.append({'macro':name,**self.definition_sources[name]})
        self.response_geometry.append({'id':'response-'+str(ordinal),'kind':kind,
            'origin':origin,'macro':macro,'height':height,'width':width,'lines':lines,
            'rule':rule,'source_ref':{'path':self.active_source,
                'coordinate_space':'canonical-expansion','occurrence':ordinal},
            'source_payload_digest':hashlib.sha256((payload or ('\\'+macro)).encode()).hexdigest(),
            'definition_refs':refs})

    def named_geometry(self,name):
        # These macros are layout-only. Verify their canonical definitions;
        # then model them as one source occurrence without expanding child rules.
        shapes={
            'Blank':(r'\rule{1.3in}{0.4pt}',('inline-rule','0.4pt','1.3in',1,'0.4pt')),
            'LongBlank':(r'\rule{2.6in}{0.4pt}',('inline-rule','0.4pt','2.6in',1,'0.4pt')),
            'memory@blankcell':(r'\rule{0pt}{2.2\baselineskip}\hrulefill',
                ('blank-cell',r'2.2\baselineskip','linewidth',1,'hrulefill')),
            'memory@twolines':(r'\par\medskip\hrulefill\par\vspace{1.1\baselineskip}\hrulefill',
                ('ruled-lines',r'1.1\baselineskip','linewidth',2,'hrulefill')),
            'memory@fourlines':(r'\memory@twolines\par\vspace{1.1\baselineskip}\hrulefill\par\vspace{1.1\baselineskip}\hrulefill',
                ('ruled-lines',r'1.1\baselineskip','linewidth',4,'hrulefill')),
        }
        expected,metrics=shapes[name]
        definition=self.macros.get(name)
        if definition is None or definition[0]!=0 or re.sub(r'\s+','',definition[2])!=expected:
            raise ProjectionError('unmodelled canonical response geometry macro '+name)
        kind,height,width,lines,rule=metrics
        self.geometry(kind,name,height=height,width=width,lines=lines,rule=rule,canonical_origin=name)

    def walk(self,text):
        self.depth+=1
        if self.depth>90:raise ProjectionError('canonical projection depth exceeded')
        out=[];pos=0
        try:
            while pos<len(text):
                found=CONTROL.search(text,pos)
                if not found:out.append(text[pos:]);break
                out.append(text[pos:found.start()]);name=found[1];pos=found.end()
                if name=='[':
                    end=text.find(r'\]',pos)
                    if end<0:raise ProjectionError('unclosed canonical display math')
                    out.append(r'\['+text[pos:end]+r'\]');pos=end+len(r'\]');continue
                definition=self.web.DEFINITION_START_RE.match(text,found.start())
                if definition:
                    value=self.web.read_definition(text,definition)
                    if value is None:raise ProjectionError('unreadable executed source definition')
                    if value.command=='let':
                        if value.source not in self.macros:raise ProjectionError('unsupported source let '+str(value.source))
                        self.assign(value.name,self.macros[value.source],value.glob)
                    elif value.macro is not None:
                        if value.command!='providecommand' or value.name not in self.macros:self.assign(value.name,value.macro,value.glob)
                    elif value.name is not None and value.name in self.macros:raise ProjectionError('unmodelled executed source definition '+value.name)
                    pos=value.end;continue
                if name in {'input','include'}:
                    values,pos=self.args(text,pos,1);out.append(self.include(values[0]));continue
                if name=='InputIfFileExists':
                    values,pos=self.args(text,pos,3)
                    if self.input_path(values[0]).is_file():out.append(self.include(values[0]));out.append(self.walk(values[1]))
                    else:out.append(self.walk(values[2]))
                    continue
                if name=='NewEnviron':
                    values,pos=self.args(text,pos,1);env=values[0];pos=self.web.skip_gap(text,pos);count=0
                    if text[pos:pos+1]=='[':end=text.index(']',pos);count=int(text[pos+1:end]);pos=end+1
                    values,pos=self.args(text,pos,1);self.environments[env]=(count,None,values[0]);continue
                if name=='newif':
                    pos=self.web.skip_gap(text,pos);flag=CONTROL.match(text,pos)
                    if not flag or not flag[1].startswith('if'):raise ProjectionError('unreadable source newif')
                    self.flags[flag[1][2:]]=False;pos=flag.end();continue
                if name in {'begingroup','bgroup'}:self.push();continue
                if name in {'endgroup','egroup'}:self.pop();continue
                if name=='global':self.global_next=True;continue
                if name.endswith('true') and name[:-4] in self.flags:self.boolean(name[:-4],True);continue
                if name.endswith('false') and name[:-5] in self.flags:self.boolean(name[:-5],False);continue
                if name.startswith('if') and name[2:] in self.flags:
                    value,pos=self.branch(text,pos,self.flags[name[2:]]);out.append(value);continue
                if name in {'IfStrEq','IfSubStr'}:
                    values,pos=self.args(text,pos,4);a,b=map(self.scalar,values[:2]);truth=a==b if name=='IfStrEq' else b in a
                    out.append(self.walk(values[2] if truth else values[3]));continue
                if name=='ifdefempty':
                    values,pos=self.args(text,pos,3);out.append(self.walk(values[1] if self.scalar(values[0])=='' else values[2]));continue
                if name=='ifcsdef':
                    values,pos=self.args(text,pos,3);key=self.scalar(values[0]);truth=key in self.macros
                    out.append(self.walk(values[1] if truth else values[2]));continue
                if name=='csdef':
                    values,pos=self.args(text,pos,2);self.assign(self.scalar(values[0]),(0,None,values[1]));continue
                if name=='endinput':break
                if name in {'forcsvlist','docsvlist'}:
                    values,pos=self.args(text,pos,2 if name=='forcsvlist' else 1)
                    callback=values[0] if name=='forcsvlist' else r'\do'
                    for key in self.scalar(values[-1]).split(','):
                        if key:out.append(self.walk(callback+'{'+key+'}'))
                    continue
                if name in {'stepcounter','refstepcounter','setcounter','addtocounter'}:
                    values,pos=self.args(text,pos,2 if name in {'setcounter','addtocounter'} else 1);key=self.scalar(values[0])
                    number=int(self.scalar(values[1])) if len(values)==2 else 1
                    self.counters[key]=number if name=='setcounter' else self.counters.get(key,0)+number
                    if name in {'stepcounter','refstepcounter'}:
                        for child,parent in self.parents.items():
                            if parent==key:self.counters[child]=0
                    continue
                if name in {'arabic','roman','Roman','Alph','alph'}:
                    values,pos=self.args(text,pos,1);key=self.scalar(values[0]);number=self.counters.get(key)
                    if number is None:raise ProjectionError('unknown source counter '+key)
                    if name!='arabic':raise ProjectionError('non-Arabic reader counter needs explicit source contract')
                    out.append(str(number));continue
                if name in {'MemoryLexemeField','MemoryGrammarField','MemorySetField'}:
                    values,pos=self.args(text,pos,2);key,field=map(self.scalar,values)
                    kind='lexeme' if name=='MemoryLexemeField' else 'grammar' if name=='MemoryGrammarField' else 'prompt' if field in {'reconstruction','reconstructionmodel','composition','compositionmodel'} else 'set'
                    out.append(self.walk(self.row(key,field,kind)));continue
                if name=='memory@usesequence':
                    values,pos=self.args(text,pos,3);key,field=map(self.scalar,values[:2]);sequence=self.row(key,field,'set')
                    for item in sequence.split(','):
                        if item:out.append(self.walk(values[2]+'{'+item+'}'))
                    continue
                if name=='MemoryLexemeIDSequence':
                    for key in self.registry['lexeme']:out.append(self.walk(r'\MemorySequenceItem{'+key+'}'))
                    continue
                if name=='noalign':
                    values,pos=self.args(text,pos,1);out.append(self.walk(values[0]));continue
                if name in {'firstmemorysheettrue','firstmemorysheetfalse'}:
                    self.boolean('firstmemorysheet',name.endswith('true'));continue
                if name=='fcolorbox':
                    values,pos=self.args(text,pos,3);out.append(self.walk(values[2]));continue
                if name in {'Blank','LongBlank','memory@blankcell','memory@twolines','memory@fourlines'}:
                    self.named_geometry(name);out.append(' ');continue
                if name=='hrulefill':
                    self.geometry('inline-rule',name,height='0pt',width='fill',canonical_origin=name);out.append(' ');continue
                if name in {'hrule','removelastskip'}:
                    out.append(' ');continue
                if name=='ifdim':
                    close=text.find(r'\fi',pos)
                    if close<0:raise ProjectionError('unclosed geometry source conditional')
                    body=text[pos:close]
                    if not re.fullmatch(r'\s*\\pagetotal\s*=\s*0pt\s*\\else\s*\\clearpage\s*',body):raise ProjectionError('non-layout source ifdim conditional')
                    pos=close+len(r'\fi');continue
                if name in {'hbadness','emergencystretch'}:
                    match=re.match(r'\s*=\s*[0-9.]+(?:em|pt)?',text[pos:])
                    if not match:raise ProjectionError('unreadable source register assignment '+name)
                    pos+=match.end();continue
                if name=='begin':
                    values,pos=self.args(text,pos,1);env=values[0]
                    if env in {'enumerate','itemize','description'}:
                        pos=self.web.skip_gap(text,pos)
                        if text[pos:pos+1]=='[':
                            end=text.find(']',pos)
                            if end<0:raise ProjectionError('unclosed structural list option')
                            pos=end+1
                        out.append(r'\begin{'+env+'}');continue
                    if env in self.environments:
                        count,default,template=self.environments[env];values,pos=self.args(text,pos,count,default);body,pos=self.env_body(text,pos,env)
                        self.push();self.assign('BODY',(0,None,body))
                        self.selection_events.append({'environment':env,'arguments':values,'part':self.part,'solutions':self.flags.get('solutions',False),'source':self.active_source})
                        out.append(self.walk(self.substitute(template,values)));self.pop();continue
                    if env in {'xltabular','tabularx','tabular','longtable'}:
                        values,pos=self.args(text,pos,2 if env in {'xltabular','tabularx'} else 1)
                        columns=re.sub(r'[PpCm]\{[^{}]+\}','l',values[-1]).replace('Y','l').replace('X','l')
                        out.append(r'\begin{longtable}{'+columns+'}');continue
                    out.append(r'\begin{'+env+'}');continue
                if name=='end':
                    values,pos=self.args(text,pos,1);env=values[0]
                    out.append(r'\end{'+('longtable' if env in {'xltabular','tabularx','tabular','longtable'} else env)+'}');continue
                if name in {'part','chapter'}:
                    star=text[pos:pos+1]=='*'
                    if star:pos+=1
                    values,pos=self.args(text,pos,1)
                    if name=='part':self.part=self.scalar(values[0])
                    out.append('\\'+name+('*' if star else '')+'{'+self.walk(values[0])+'}');continue
                if name=='vspace':
                    if text[pos:pos+1]=='*':pos+=1
                    values,pos=self.args(text,pos,1)
                    cursor=self.web.skip_gap(text,pos);following=CONTROL.match(text,cursor)
                    if following and following[1] in {'hrulefill','hrule'}:
                        height=re.sub(r'\s+','',self.scalar(values[0]))
                        if height not in RESPONSE_HEIGHTS:
                            raise ProjectionError('unmodelled canonical response height '+height)
                        self.geometry('response-block',following[1],height=height,rule=following[1],
                            origin='vspace',payload=text[found.start():following.end()])
                        # Preserve the previous semantic projection byte for byte:
                        # both removed controls supplied one space apiece.
                        out.append(' '+text[pos:following.start()]+' ');pos=following.end();continue
                    out.append(' ');continue
                if name=='rule':
                    values,pos=self.args(text,pos,2);width,height=(re.sub(r'\s+','',self.scalar(value)) for value in values)
                    if width=='0pt':
                        if height not in ROW_HEIGHTS:
                            raise ProjectionError('unmodelled canonical table response height '+height)
                        self.geometry('table-row-space','rule',height=height,width=width,lines=0,rule='none',payload=text[found.start():pos],canonical_origin='rule')
                    elif width==r'\linewidth' and height=='1pt' and any(owner in self.macro_stack for owner in ('CourseTitlePage','ModuleTitlePage')):
                        # The canonical cover separator is decoration, not writing room.
                        pass
                    elif width in {'1.3in','2.6in'} and height=='0.4pt':
                        self.geometry('inline-rule','rule',height=height,width=width,rule=height,payload=text[found.start():pos],canonical_origin='rule')
                    else:raise ProjectionError('unmodelled canonical rule geometry '+width+'/'+height)
                    out.append(' ');continue
                if name in {'hypersetup','setlength','addtolength','addcontentsline','CourseUnnumberedSectionContents','markboth','markright','pagenumbering','pagestyle','thispagestyle','Needspace','needspace','hspace','fontsize'}:
                    if text[pos:pos+1]=='*':pos+=1
                    count={'setlength':2,'addtolength':2,'addcontentsline':3,'markboth':2,'fontsize':2,'rule':2}.get(name,1)
                    _,pos=self.args(text,pos,count);out.append(' ');continue
                if name in self.macros:
                    count,default,body=self.macros[name];values,pos=self.args(text,pos,count,default)
                    self.macro_stack.append(name)
                    if name in GEOMETRY_ORIGINS:self.geometry_origins.append(name)
                    try:out.append(self.walk(self.substitute(body,values)))
                    finally:
                        self.macro_stack.pop()
                        if name in GEOMETRY_ORIGINS:self.geometry_origins.pop()
                    continue
                if name in {'if','ifdefined','ifx','ifnum','else','fi','csname','endcsname','expandafter','edef','xdef','write','directlua'} or name.startswith('if'):
                    raise ProjectionError('unsupported executed source control '+name)
                out.append('\\'+name+(' ' if name[0].isalpha() else ''))
            return ''.join(out)
        finally:self.depth-=1

    def run(self):
        raw=self.source(self.root/self.entrypoint);projected=self.walk(raw)
        if self.stack:raise ProjectionError('unclosed canonical projection scope')
        head,body=self.web.split_document(projected)
        # Metadata title/subtitle are displayed in the owning cover, so the
        # semantic ledger must not invent a second metadata-only occurrence.
        body=self.web.drop_continuation_heads(body)
        if r'\TriptychRightsNotice' not in body:body+='\n\\TriptychRightsNotice\n'
        if self.math_adapter is not None:
            body,self.semantic_units=self.math_adapter(body)
        refs=[{'path':path.relative_to(self.root).as_posix(),'sha256':hashlib.sha256(raw.encode()).hexdigest()} for path,raw in sorted(self.sources.items())]
        contract={'version':'curriculum-canonical-dsl/v1','runtime_owners':self.runtime_contracts,'selection_events':self.selection_events,'field_events':self.field_events}
        digest=hashlib.sha256(json.dumps(contract,sort_keys=True).encode()).hexdigest()
        chunk={'path':self.entrypoint,'occurrence':1,'selected_line':1,'text':body,
               'projection':{'contract_id':contract['version'],'contract_digest':digest,'canonical_source_refs':refs,
                    'canonical_occurrence_id':self.recipe['id'],'source_payload_digest':hashlib.sha256(raw.encode()).hexdigest()}}
        return {'head':head,'body':body,'chunks':[chunk],'sources':self.sources,
                'selection':{'entrypoint':self.entrypoint,'role':self.recipe.get('edition','main'),'selection_digest':digest},
                'semantic_units':self.semantic_units,'projection_contract':contract,
                'response_geometry':self.response_geometry}


def project_curriculum(root,recipe,library,math_adapter=None):
    return CanonicalProjector(root,recipe,library,math_adapter).run()


def semantic_check(selection,rendered,library):
    import _web_print_semantics as semantic
    ledger=semantic.expected_units(selection,library)
    return ledger,semantic.check_units(ledger,rendered,library)
