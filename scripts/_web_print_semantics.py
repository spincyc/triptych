"""Independent visible-text ledger for the selected corpus's bounded TeX DSL.

Reads canonical macro/environment definitions, not converted Markdown or the web
shim. Unknown executed constructs refuse. Layout arguments are explicitly typed;
short text, inline accents, notes and table cells are never size-filtered.
"""
from __future__ import annotations
from collections import Counter
from bisect import bisect_right
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import tomllib
import unicodedata
from urllib.parse import unquote,quote,urlsplit,urlunsplit

class CoverageError(ValueError): pass

WORD = re.compile(r"[^\W_]+(?:['’][^\W_]+)*|[→⟶±×÷=<>≤≥≠∈∉⊂⊆∞·⋅°∘∗%$£€§¶+−–—|\-]", re.UNICODE)
COMMAND = re.compile(r"\\([A-Za-z@]+|.)", re.S)
ENVDEF = re.compile(r"\\((?:new|renew)environment|newtcolorbox)\*?\s*\{")
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
BLOCKS = {'p','li','dt','dd','th','td','h1','h2','h3','h4','h5','h6','figcaption','math'}
FORMAT = {'textbf','textit','texttt','textsc','textnormal','textrm','textsf','emph','underline','textsuperscript','textsubscript','mbox','fbox','hbox','IeC','nouppercase'}
LAYOUT0 = set('begingroup endgroup bgroup egroup removelastskip noindent indent nobreak allowbreak protect relax ignorespaces strut phantomsection tiny scriptsize footnotesize small normalsize large Large LARGE huge Huge itshape bfseries scshape rmfamily sffamily ttfamily upshape mdseries normalfont selectfont raggedright raggedleft centering RaggedRight Centering sloppy clearpage newpage pagebreak thispagestyleempty appendix tableofcontents toprule midrule bottomrule hline endhead endfirsthead endfoot endlastfoot arraybackslash makeatletter makeatother sectionguard raggedcolumns theendnotes leavevmode AIDisplayDocumentRevisionTimestamp'.split())
SPACES = set('space enspace thinspace negthinspace quad qquad hfill'.split())
LAYOUT_ARGS = {'setlength':2,'addtolength':2,'setcounter':2,'addtocounter':2,'fontsize':2,'vspace':1,'hspace':1,'Needspace':1,'needspace':1,'rule':2,'enlargethispage':1,'thispagestyle':1,'pagestyle':1,'pagenumbering':1,'label':1,'zlabel':1,'addcontentsline':3,'addtocontents':2,'geometry':1,'hypersetup':1,'color':1,'phantom':1,'hphantom':1,'vphantom':1,'markright':1,'markboth':2,'pdfbookmark':2,'sectionmark':1,'subsectionmark':1,'linespread':1,'runninghead':1,'addvspace':1}
ENV_LAYOUT = {'document','center','flushleft','flushright','quote','quotation','verse','abstract','titlepage','landscape','table','figure','samepage'}
TABLES = {'longtable':1,'tabular':1,'tabularx':2,'tabular*':2,'array':1}
GLYPHS = {'ae':'æ','AE':'Æ','oe':'œ','OE':'Œ','ss':'ß','o':'ø','O':'Ø','l':'ł','L':'Ł','aa':'å','AA':'Å','i':'ı','j':'ȷ','S':'§','P':'¶','dag':'†','ddag':'‡','textendash':'–','textemdash':'—','textquotesingle':"'",'textquotedblleft':'“','textquotedblright':'”','textperiodcentered':'·','textbullet':'•','textdegree':'°','textordmasculine':'º','textordfeminine':'ª','guillemotleft':'«','guillemotright':'»','textbackslash':'\\','textbar':'|','textasciitilde':'~','copyright':'©','slash':'/','ldots':'…','dots':'…','LaTeX':'LaTeX','TeX':'TeX','textexclamdown':'¡','textquestiondown':'¿','Theta':'Θ','Lambda':'Λ','alpha':'α','aleph':'ℵ','pm':'±','cdot':'⋅','rightarrow':'→','longrightarrow':'→','circ':'∘','ast':'∗','leq':'≤'}
ACCENTS = {"'":'\u0301','`':'\u0300','"':'\u0308','^':'\u0302','~':'\u0303','=':'\u0304','.':'\u0307','u':'\u0306','v':'\u030c','H':'\u030b','c':'\u0327','k':'\u0328','r':'\u030a','b':'\u0331','d':'\u0323'}


def normalized(value: str) -> str:
    value=unicodedata.normalize('NFKC',value).replace('\u00ad','').replace('---','—').replace('--','–').replace('’',"'").replace('‘',"'").replace('`',"'")
    return ' '.join(word.casefold() for word in WORD.findall(value))


def math_identity(value):
    """Keep mathematical case, grouping and decimal punctuation; ignore spacing."""
    return ''.join(unicodedata.normalize('NFKC',value).split())


def uri_identity(value,tex=False):
    r"""Compare an actual URI, preserving encoded reserved delimiters.

    TeX URI arguments escape punctuation before percent-encoded UTF-8 bytes
    are read. Decode those control symbols first; otherwise \%C3\%A8 is
    incorrectly decoded as two broken Unicode sequences around backslashes.
    """
    if tex:
        value=re.sub(r'\\([^A-Za-z@])',lambda match:match.group(1),value)
        if '\\' in value:raise CoverageError('unsupported control word in canonical URI '+value)
    # Encode literal Unicode/space uniformly, but never collapse an encoded
    # path delimiter (%23/%2F) into a fragment/slash with a different meaning.
    value=quote(value,safe=":/?#[]@!$&'()*+,;=%-._~")
    value=re.sub(r'%[a-fA-F0-9]{2}',lambda match:match.group().upper(),value)
    return value

def _replace(template,args):
    # Substitute token lists once. Text concatenation must not invent a new
    # control word (\enspace#2 -> \enspaceThe) or replace a parameter carried
    # inside an argument. Doubled parameters belong to a nested definition.
    pieces=[]
    for token in re.findall(r'\\[A-Za-z@]+|\\.|##|#[1-9]|[^\\#]+|#',template,re.S):
        if token=='##':part='#'
        elif re.fullmatch(r'#[1-9]',token):
            index=int(token[1])-1
            if index>=len(args):raise CoverageError('unbound canonical macro parameter '+token)
            part=args[index]
        else:part=token
        if pieces and re.search(r'\\[A-Za-z@]+$',pieces[-1]) and re.match(r'[A-Za-z@]',part):pieces.append('{}')
        pieces.append(part)
    return ''.join(pieces)


def _environments(text,library):
    environments={}
    for match in ENVDEF.finditer(library.strip_tex_comments(text)):
        source=library.strip_tex_comments(text)
        name,cursor=library.brace_group(source,match.end()-1)
        count=0;default=None;cursor=library.skip_gap(source,cursor)
        if source[cursor:cursor+1]=='[':
            close=source.find(']',cursor)
            if close<0:raise CoverageError('unclosed environment signature: '+name)
            count=int(source[cursor+1:close]);cursor=library.skip_gap(source,close+1)
            if source[cursor:cursor+1]=='[':
                close=source.find(']',cursor);default=source[cursor+1:close];cursor=close+1
        opening,cursor=library.brace_group(source,cursor)
        if match.group(1)=='newtcolorbox':
            # tcolorbox's sole visible option is title. Execution hooks must be
            # reconciled explicitly rather than silently treated as geometry.
            if re.search(r'(?:before|after)\s+(?:upper|lower)\s*=',opening):raise CoverageError('content hook in tcolorbox '+name)
            title=re.search(r'(?:^|,)\s*title\s*=\s*',opening)
            label=''
            if title:
                gap=library.skip_gap(opening,title.end())
                label=library.brace_group(opening,gap)[0] if opening[gap:gap+1]=='{' else opening[gap:].split(',',1)[0]
            opening=('\\par '+label+'\\par ') if label else '\\par '
            closing='\\par '
        else:closing,cursor=library.brace_group(source,cursor)
        environments[name]=(count,default,opening,closing)
    return environments


class Ledger:
    def __init__(self,selection,library):
        self.library=library;self.selection=selection
        common=[]
        for path,source in selection.get('sources',{}).items():
            if str(path).endswith('/common/preamble.tex'):common.append(source)
        definition_source='\n'.join(common)+'\n'+selection.get('head','')
        self.macros,_=library.command_definitions(library.strip_tex_comments(definition_source))
        self.environments=_environments(definition_source,library)
        self.macro_digest=hashlib.sha256(json.dumps(self.macros,sort_keys=True).encode()).hexdigest()
        self.counters={};self.layout_omissions=[];self.units=[];self.links=[];self.buffer=[];self.buffer_refs=[];self.buffer_expansions=[];self.buffer_states=[];self.buffer_math=[];self.buffer_links=[];self.macro_occurrences=Counter();self.kind='paragraph';self.lane='body'
        self.labels={};self.references=[];self.last_heading=None;self.current_reference=None;self.appendix=False;self.display_adaptations=[];self.counter_displays=[];self.counter_eval_depth=0
        self.table_stack=[];self.table_number=0;self.environment_stack=[];self.item_depth=0
        self.notes=0;self.note_stack=[];self.revision=None;self.rights=False;self.expansions=[];self.limit=0;self.boundaries=[];self.minipages=0
        self.scope_stack=[];self.semantic_units=selection.get('semantic_units',{});self.diagram_assets=selection.get('diagram_assets',[]);self.diagram_by_start={};self.diagram_seen=[]
        self.origin={'path':selection.get('selection',{}).get('entrypoint','<selected-source>'),'occurrence':1,'selected_line':1}
        self.offsets=[];self.offset_starts=[];self.origin_cache={};cursor=0
        for chunk in selection.get('chunks',[]):
            self.offset_starts.append(cursor);self.offsets.append((cursor,cursor+len(chunk['text']),chunk,[i for i,char in enumerate(chunk['text']) if char=='\n']));cursor+=len(chunk['text'])
        self._origin_offset=None
        self.body=selection['body']
        self.head=definition_source
        previous_end=0
        for asset in self.diagram_assets:
            start,end=asset.get('start'),asset.get('end')
            if not isinstance(start,int) or not isinstance(end,int) or not previous_end<=start<end<=len(self.body):raise CoverageError('invalid/overlapping canonical diagram span')
            raw=self.body[start:end]
            if hashlib.sha256(raw.encode()).hexdigest()!=asset.get('source_tex_sha256'):raise CoverageError('diagram canonical source-span hash mismatch')
            tokens=list(re.finditer(r'\\(begin|end)\s*\{\s*([^}\s]+)\s*\}',self.library.mask_tex_comments(raw)))
            if not tokens or tokens[0].group(1)!='begin' or tokens[0].group(2)!='tikzpicture' or tokens[-1].group(1)!='end' or tokens[-1].group(2)!='tikzpicture':raise CoverageError('diagram span is not one complete TikZ environment')
            stack=[]
            for token in tokens:
                action,name=token.groups()
                if action=='begin':stack.append(name)
                elif not stack or stack.pop()!=name:raise CoverageError('unbalanced canonical diagram environment')
            if stack or tokens[0].start()!=0 or tokens[-1].end()!=len(raw):raise CoverageError('diagram span has unbound content')
            if not asset.get('asset_id') or not re.fullmatch(r'[a-f0-9]{64}',asset.get('svg_sha256','')) or not asset.get('source_refs'):raise CoverageError('incomplete canonical diagram asset identity')
            if asset.get('selection_digest')!=selection.get('selection',{}).get('selection_digest'):raise CoverageError('diagram belongs to another selected source graph')
            self.diagram_by_start[start]=asset;previous_end=end
        self.source_origin=self.origin

    def origin_at(self,offset):
        if offset is None:return self.origin
        index=bisect_right(self.offset_starts,offset)-1
        if index<0:return self.origin
        start,end,chunk,newlines=self.offsets[index]
        if not start<=offset<end:return self.origin
        line=bisect_right(newlines,offset-start-1)
        key=(index,line)
        if key not in self.origin_cache:
            reference={'path':chunk['path'],'occurrence':chunk['occurrence'],'selected_line':chunk['selected_line']+line}
            if chunk.get('projection'):reference.update(projection=chunk['projection'],coordinate_space='semantic-projection')
            self.origin_cache[key]=reference
        return self.origin_cache[key]

    def append(self,text,offset=None):
        if text.strip():
            reference=self.origin_at(offset)
            if not self.buffer:self.source_origin=reference
            if not self.buffer_refs or self.buffer_refs[-1]!=reference:self.buffer_refs.append(reference)
            for expansion in self.expansions:
                public={key:value for key,value in expansion.items() if not key.startswith('_')}
                if public not in self.buffer_expansions:self.buffer_expansions.append(public)
            if not self.buffer_states or self.buffer_states[-1]!=self.macro_digest:self.buffer_states.append(self.macro_digest)
        self.buffer.append(text)

    def flush(self,kind=None,cell_end=False):
        if self.table_stack and not cell_end:
            if self.buffer and not self.buffer[-1].endswith(' '):self.buffer.append(' ')
            return
        text=''.join(self.buffer);self.buffer=[]
        references,expansions,states,math_literals,locators=self.buffer_refs,self.buffer_expansions,self.buffer_states,self.buffer_math,self.buffer_links
        self.buffer_refs=[];self.buffer_expansions=[];self.buffer_states=[];self.buffer_math=[];self.buffer_links=[]
        value=normalized(text)
        if not value and not math_literals:
            if locators:raise CoverageError('canonical hyperlink has no visible containing content unit')
            return
        active=self.table_stack[-1] if self.table_stack else None
        unit_kind=kind or ('table-cell' if active else self.kind)
        index=len(self.units)+1
        record={'id':f'unit-{index:06d}','occurrence_id':f'unit-{index:06d}','kind':unit_kind,'lane':self.lane,'source_ref':dict(self.source_origin),'source_refs':references,'macro_states':states,'expected':value,'text_digest':hashlib.sha256(value.encode()).hexdigest(),'macro_state_digest':self.macro_digest,'counter_state_digest':hashlib.sha256(json.dumps(self.counters,sort_keys=True).encode()).hexdigest()}
        if active:record.update(table=active['id'],row=active['row'],column=active['column'])
        if expansions:record['expansion']=expansions
        if math_literals:record['math_literals']=math_literals
        if locators:
            for locator in locators:locator['unit_id']=record['id']
            record['locators']=locators
        self.units.append(record)
        if not active:self.kind='paragraph'

    def arguments(self,text,cursor,count,default=None):
        args=[]
        for index in range(count):
            cursor=self.library.skip_gap(text,cursor)
            if index==0 and default is not None:
                if text[cursor:cursor+1]=='[':
                    end=text.find(']',cursor)
                    if end<0:raise CoverageError('unclosed optional argument')
                    args.append(text[cursor+1:end]);cursor=end+1
                else:args.append(default)
            else:
                try:arg,cursor=self.library.brace_group(text,cursor)
                except Exception as error:raise CoverageError('unsupported unbraced argument near '+text[cursor:cursor+60]) from error
                args.append(arg)
        return args,cursor

    def atom(self,text,cursor):
        cursor=self.library.skip_gap(text,cursor)
        if text[cursor:cursor+1]=='{':return self.library.brace_group(text,cursor)
        match=COMMAND.match(text,cursor)
        if match:return match.group(),match.end()
        if cursor<len(text):return text[cursor],cursor+1
        raise CoverageError('missing accent argument')

    def inline(self,text):
        state=(self.buffer,self.kind,self.source_origin,self.buffer_refs,self.buffer_expansions,self.buffer_states,self.buffer_math,self.buffer_links)
        self.buffer=[];self.buffer_refs=[];self.buffer_expansions=[];self.buffer_states=[];self.buffer_math=[];self.buffer_links=[];self.kind='inline'
        self.parse(text,base=None)
        result=''.join(self.buffer);self.buffer,self.kind,self.source_origin,self.buffer_refs,self.buffer_expansions,self.buffer_states,self.buffer_math,self.buffer_links=state
        return result

    def locator(self,target,display,offset,kind='locator',reference_id=None):
        record={'kind':kind,'target':target,'expected_target':uri_identity(target,tex=True),'expected_display':normalized(display),'source_ref':self.origin_at(offset)}
        if reference_id:record['reference_id']=reference_id
        self.links.append(record);self.buffer_links.append(record)

    def linked_display(self,text,target,offset,depth,kind='locator'):
        units_before=len(self.units);prefix=''.join(self.buffer)
        self.parse_child(text,offset,depth)
        if len(self.units)!=units_before or not ''.join(self.buffer).startswith(prefix):raise CoverageError('block-spanning canonical hyperlink requires a typed adapter')
        self.locator(target,''.join(self.buffer)[len(prefix):],offset,kind)

    def push_scope(self,tag):
        self.scope_stack.append((tag,dict(self.macros),dict(self.environments),self.current_reference))

    def pop_scope(self,tag):
        if not self.scope_stack or self.scope_stack[-1][0]!=tag:raise CoverageError('unbalanced canonical scope '+tag)
        _,self.macros,self.environments,self.current_reference=self.scope_stack.pop()
        self.macro_digest=hashlib.sha256(json.dumps(self.macros,sort_keys=True).encode()).hexdigest()

    def _definition(self,text,cursor):
        match=self.library.DEFINITION_START_RE.match(text,cursor)
        if not match:return None
        definition=self.library.read_definition(text,match)
        if definition is None:raise CoverageError('unreadable executed definition')
        if definition.command=='environment':
            self.environments.update(_environments(text[definition.start:definition.end],self.library))
        elif definition.name:
            if definition.problem:
                self.macros[definition.name]=('refuse',None,definition.problem)
            elif definition.command=='let':
                if definition.source in self.macros:self.macros[definition.name]=self.macros[definition.source]
                elif definition.source in LAYOUT0:self.macros[definition.name]=(0,None,'')
                elif definition.source in LAYOUT_ARGS:self.macros[definition.name]=(LAYOUT_ARGS[definition.source],None,'')
                elif definition.source in {'section','subsection','subsubsection','paragraph','subparagraph','chapter','part'}:self.macros[definition.name]=(1,None,'\\'+definition.source+'{#1}')
                else:raise CoverageError('unsupported let target '+str(definition.source))
            elif definition.macro is not None:
                if definition.command not in {'newcommand','providecommand'} or definition.name not in self.macros:self.macros[definition.name]=definition.macro
        if definition.glob and definition.name and definition.name in self.macros:
            for _,saved_macros,_,_ in self.scope_stack:saved_macros[definition.name]=self.macros[definition.name]
        self.macro_digest=hashlib.sha256(json.dumps(self.macros,sort_keys=True).encode()).hexdigest()
        return definition.end

    def footer_definitions(self,text,cursor,base):
        if not self.table_stack or not self.table_stack[-1].get('pending_footer_scan'):return cursor
        depth=0;markers=[];closed=False
        for token in re.finditer(r'\\(?:begin|end)\s*\{([^{}]+)\}|\\(endfoot|endlastfoot)(?![A-Za-z@])',self.library.mask_tex_comments(text[cursor:])):
            if token.group(2):
                if depth==0:markers.append(token)
            elif token.group().startswith('\\begin'):depth+=1
            elif depth:depth-=1
            else:closed=True;break
        if markers:
            end=cursor+markers[-1].end()
            self.layout_omissions.append({'role':'physical-longtable-footer-definitions','source_ref':self.origin_at(None if base is None else base+cursor),'source_sha256':hashlib.sha256(text[cursor:end].encode()).hexdigest()})
            self.table_stack[-1]['pending_footer_scan']=False
            return end
        if closed:self.table_stack[-1]['pending_footer_scan']=False
        return cursor

    def counter_text(self,name,style='arabic'):
        number=self.counters.get(name,0)
        if style=='arabic':return str(number)
        if style in {'alph','Alph'}:
            if not 0<=number<=26:raise CoverageError('alphabetic counter out of range '+name)
            value='' if number==0 else chr(ord('a')+number-1)
            return value.upper() if style=='Alph' else value
        if number<0 or number>3999:raise CoverageError('Roman counter out of range '+name)
        result=''
        for value,label in ((1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')):
            while number>=value:result+=label;number-=value
        return result.lower() if style=='roman' else result

    def counter_reference(self,name):
        if 'the'+name in self.macros:
            self.counter_eval_depth+=1
            try:return self.inline('\\the'+name)
            finally:self.counter_eval_depth-=1
        levels=('section','subsection','subsubsection','paragraph','subparagraph')
        if name in levels:
            components=[self.counter_text('section','Alph' if self.appendix else 'arabic')]
            components.extend(self.counter_text(component) for component in levels[1:levels.index(name)+1])
            return '.'.join(components)
        return self.counter_text(name,'Roman' if name=='part' else 'arabic')

    def macro_frame(self,name,macro,args,offset,end,program_offset,program_end):
        self.macro_occurrences[name]+=1
        frame={'name':name,'occurrence':self.macro_occurrences[name],'occurrence_id':f'macro-{name}-{self.macro_occurrences[name]:06d}','call_source_ref':dict(self.origin_at(offset)),'source_offset':offset,'source_end':end,'program_offset':program_offset,'program_end':program_end,'argument_digests':[hashlib.sha256(arg.encode()).hexdigest() for arg in args],'definition_digest':hashlib.sha256(macro[2].encode()).hexdigest(),'_arguments':list(args),'_definition':macro[2],'_parameters':macro[0],'_default':macro[1]}
        if offset is not None and end is not None:
            frame['_source_call']=self.body[offset:end];frame['source_tex_sha256']=hashlib.sha256(frame['_source_call'].encode()).hexdigest()
        return frame

    def counter_display(self,command,counter,style,value,offset,end,program_offset,program_end):
        if self.counter_eval_depth:return
        trace=[]
        for frame in self.expansions:
            record={key:value for key,value in frame.items() if not key.startswith('_')}
            for private,public in (('_arguments','arguments'),('_definition','definition'),('_parameters','parameters'),('_default','default'),('_source_call','source_call')):
                if private in frame:record[public]=frame[private]
            if '_definition' in frame:
                record['expanded_program']=_replace(frame['_definition'],frame['_arguments'])
                record['expanded_program_sha256']=hashlib.sha256(record['expanded_program'].encode()).hexdigest()
            trace.append(record)
        owner=next((frame for frame in trace if frame.get('source_offset') is not None),None)
        source_offset=owner['source_offset'] if owner else offset
        source_end=owner['source_end'] if owner else end
        name=next((frame['name'] for frame in reversed(trace) if frame['name']=='the'+counter),command)
        event={'id':f'counter-display-{len(self.counter_displays)+1:06d}','name':name,'read_command':command,'counter':counter,'format':style,'rawdisplay':value,'source_offset':source_offset,'source_end':source_end,'source_ref':owner['call_source_ref'] if owner else self.origin_at(offset),'read_source_ref':self.origin_at(offset),'read_source_offset':offset,'program_offset':program_offset,'program_end':program_end,'expansion':trace,'counter_state':dict(self.counters),'counter_state_digest':hashlib.sha256(json.dumps(self.counters,sort_keys=True).encode()).hexdigest(),'macro_state_digest':self.macro_digest,'appendix':self.appendix,'selection_digest':self.selection.get('selection',{}).get('selection_digest')}
        if source_offset is not None and source_end is not None:
            event['source_call']=self.body[source_offset:source_end];event['source_tex_sha256']=hashlib.sha256(event['source_call'].encode()).hexdigest()
        self.counter_displays.append(event)

    def parse_child(self,text,offset,depth,*,source_base=None,program_base=None):
        original_origin=self.origin
        self.origin=self.origin_at(offset)
        self.parse(text,source_base,depth,program_base=program_base)
        self.origin=original_origin

    def parse(self,text,base=0,depth=0,program_base=0):
        if depth>48:raise CoverageError('content macro expansion depth exceeded')
        self.limit+=len(text)
        if self.limit>40_000_000:raise CoverageError('content macro expansion size exceeded')
        cursor=0
        while cursor<len(text):
            cursor=self.footer_definitions(text,cursor,base)
            if cursor>=len(text):break
            offset=None if base is None else base+cursor
            if offset in self.diagram_by_start:
                asset=self.diagram_by_start[offset];self.flush();index=len(self.units)+1
                self.units.append({'id':f'unit-{index:06d}','occurrence_id':asset['asset_id'],'kind':'diagram','lane':self.lane,'source_ref':asset['source_refs'],'expected':'','macro_state_digest':self.macro_digest,'asset':asset['asset'],'rendered_src':asset.get('rendered_src',asset['asset']),'svg_sha256':asset['svg_sha256'],'source_tex_sha256':asset['source_tex_sha256'],'selection_digest':asset['selection_digest'],'source_labels_digest':hashlib.sha256(json.dumps(asset.get('labels',[]),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()})
                self.diagram_seen.append(asset['asset_id']);cursor+=asset['end']-asset['start'];continue
            ch=text[cursor]
            if ch=='%':
                end=text.find('\n',cursor)
                if end<0:cursor=len(text)
                else:
                    cursor=end+1
                    # A comment consumes its own line ending, but a following
                    # physically empty line is still TeX's paragraph token.
                    blank=re.match(r'[ \t]*\n',text[cursor:])
                    if blank:self.flush();cursor+=blank.end()
                continue
            if ch=='\\':
                command_start=cursor
                definition_end=self._definition(text,cursor)
                if definition_end is not None:cursor=definition_end;continue
                match=COMMAND.match(text,cursor)
                if not match:raise CoverageError('invalid control sequence')
                name=match.group(1);cursor=match.end()
                if name.isalpha() or '@' in name:
                    # TeX consumes the delimiter whitespace of a control word.
                    delimiter=re.match(r'\s*',text[cursor:]).group()
                    paragraph=re.search(r'\n[ \t]*\n',delimiter)
                    cursor+=paragraph.start() if paragraph else len(delimiter)
                starred=text[cursor:cursor+1]=='*' and name in {'section','subsection','subsubsection','paragraph','subparagraph','chapter','part','vspace','hspace','Needspace','needspace'}
                if starred:cursor+=1
                if name=='\\':
                    self.flush(cell_end=bool(self.table_stack))
                    if self.table_stack:self.table_stack[-1]['row']+=1;self.table_stack[-1]['column']=0
                    if text[cursor:cursor+1]=='*':cursor+=1
                    if text[cursor:cursor+1]=='[':
                        close=text.find(']',cursor)
                        if close<0:raise CoverageError('unclosed row-spacing option')
                        cursor=close+1
                    continue
                if name in {'%','&','#','$','_','{','}'}:self.append(name,offset);continue
                if name in {' ','\n','\t',',',';',':'}:self.append(' ',offset);continue
                if name in {'-','!','@'}:continue
                if name in ACCENTS:
                    value,cursor=self.atom(text,cursor);visible=self.inline(value)
                    if len(visible)!=1:raise CoverageError('non-glyph accent argument '+repr(value))
                    self.append(unicodedata.normalize('NFC',visible+ACCENTS[name]),offset);continue
                if name in GLYPHS:
                    if name=='longrightarrow':self.display_adaptations.append({'role':'arrow-length-reflow','command':name,'display':'→','source_ref':self.origin_at(offset)})
                    self.append(GLYPHS[name],offset);continue
                if name in FORMAT:
                    argument_start=self.library.skip_gap(text,cursor)+1
                    args,cursor=self.arguments(text,cursor,1);self.parse_child(args[0],offset,depth+1,source_base=None if base is None else base+argument_start,program_base=None if program_base is None else program_base+argument_start);continue
                if name in SPACES:self.append(' ',offset);continue
                if name in {'par','vfill'}:self.flush();continue
                # LaTeX's vertical-space hints use \vadjust in horizontal mode;
                # they do not terminate the current paragraph.
                if name in {'smallskip','medskip','bigskip'}:continue
                if name in {'newline','linebreak'}:self.flush();continue
                if name in {'Urlmuskip','parindent','parskip','hbadness','vbadness','hyphenchar','emergencystretch','clubpenalty','widowpenalty','displaywidowpenalty','brokenpenalty','hyphenpenalty','exhyphenpenalty','arraystretch','tabcolsep','LTpre','LTpost'}:
                    register=re.match(r'(?:\\font\s*)?=?\s*-?[0-9.]+(?:\s*(?:pt|em|ex|mm|cm|in|bp|sp|mu))?(?:\s+(?:plus|minus)\s+-?[0-9.]+(?:pt|em|ex|mm|cm|in|bp|sp|mu))?',text[cursor:])
                    if not register:raise CoverageError('unsupported layout register assignment '+name)
                    cursor+=register.end();continue
                if name=='hrule':
                    rule=re.match(r'(?:\s*(?:height|width|depth)\s*-?[0-9.]+(?:pt|em|ex|mm|cm|in|bp|sp))*',text[cursor:])
                    cursor+=rule.end();continue
                if name in {'vskip','hskip','kern'}:
                    register=re.match(r'=?\s*-?[0-9.]+(?:pt|em|ex|mm|cm|in|bp|sp|mu)(?:\s+(?:plus|minus)\s+-?[0-9.]+(?:pt|em|ex|mm|cm|in|bp|sp|mu))?',text[cursor:])
                    if not register:raise CoverageError('unsupported literal layout skip '+name)
                    cursor+=register.end();continue
                if name=='noalign':
                    args,cursor=self.arguments(text,cursor,1);self.parse_child(args[0],offset,depth+1);continue
                if name=='endhead':
                    if self.table_stack:self.table_stack[-1]['pending_footer_scan']=True
                    cursor=self.footer_definitions(text,cursor,base)
                    continue
                if name in {'endfoot','endlastfoot'}:raise CoverageError('unscoped physical table footer definition')
                if name=='endfirsthead':
                    continuation=re.search(r'\\endhead(?![A-Za-z@])',text[cursor:])
                    if continuation is None:raise CoverageError('continuation table header has no endhead')
                    cursor+=continuation.end()
                    if self.table_stack:self.table_stack[-1]['pending_footer_scan']=True
                    cursor=self.footer_definitions(text,cursor,base);continue
                if name in {'begingroup','bgroup'}:self.push_scope('explicit');continue
                if name in {'endgroup','egroup'}:self.pop_scope('explicit');continue
                if name=='appendix':
                    self.appendix=True
                    for counter in ('section','subsection','subsubsection','paragraph','subparagraph'):self.counters[counter]=0
                    self.last_heading=None;continue
                if name in {'label','zlabel'}:
                    args,cursor=self.arguments(text,cursor,1)
                    self.labels.setdefault(args[0],[]).append({'source_ref':self.origin_at(offset),'heading':self.last_heading,'reference':self.current_reference})
                    continue
                if name in LAYOUT0:continue
                if name in {'refstepcounter','stepcounter','newcounter','setcounter','addtocounter'}:
                    args,cursor=self.arguments(text,cursor,2 if name in {'setcounter','addtocounter'} else 1)
                    key=args[0]
                    if name=='newcounter':
                        self.counters.setdefault(key,0)
                        if text[cursor:cursor+1]=='[':cursor=text.index(']',cursor)+1
                    elif name in {'refstepcounter','stepcounter'}:
                        self.counters[key]=self.counters.get(key,0)+1
                        if name=='refstepcounter':self.current_reference={'number':self.counter_reference(key),'counter':key,'source_ref':self.origin_at(offset)}
                    else:
                        if not re.fullmatch(r'-?[0-9]+',args[1].strip()):raise CoverageError('nonliteral counter assignment '+key)
                        self.counters[key]=(0 if name=='setcounter' else self.counters.get(key,0))+int(args[1])
                    continue
                if name in {'arabic','alph','Alph','roman','Roman'}:
                    args,cursor=self.arguments(text,cursor,1);value=self.counter_text(args[0],name)
                    self.counter_display(name,args[0],name,value,offset,None if base is None else base+cursor,None if program_base is None else program_base+command_start,None if program_base is None else program_base+cursor);self.append(value,offset);continue
                if name.startswith('the') and name[3:] in self.counters and name not in self.macros:
                    value=self.counter_reference(name[3:]);self.counter_display(name,name[3:],'counter-reference',value,offset,None if base is None else base+cursor,None if program_base is None else program_base+command_start,None if program_base is None else program_base+cursor);self.append(value,offset);continue
                if name in LAYOUT_ARGS:
                    _,cursor=self.arguments(text,cursor,LAYOUT_ARGS[name]);continue
                if name in {'textcolor','colorbox'}:
                    args,cursor=self.arguments(text,cursor,2);self.parse_child(args[1],offset,depth+1);continue
                if name in {'texorpdfstring'}:
                    args,cursor=self.arguments(text,cursor,2);self.parse_child(args[0],offset,depth+1);continue
                if name in {'section','subsection','subsubsection','paragraph','subparagraph','chapter','part'}:
                    if text[cursor:cursor+1]=='[':cursor=text.index(']',cursor)+1
                    argument_start=self.library.skip_gap(text,cursor)+1
                    args,cursor=self.arguments(text,cursor,1);self.flush()
                    levels=('part','chapter','section','subsection','subsubsection','paragraph','subparagraph');level=levels.index(name)
                    if not starred:
                        self.counters[name]=self.counters.get(name,0)+1
                        for subordinate in levels[level+1:]:self.counters[subordinate]=0
                    number=self.counter_reference(name) if not starred else None
                    if not starred:self.current_reference={'number':number,'counter':name,'source_ref':self.origin_at(offset)}
                    self.kind='heading';self.parse_child(args[0],offset,depth+1,source_base=None if base is None else base+argument_start,program_base=None if program_base is None else program_base+argument_start);self.flush('heading')
                    if not self.units or self.units[-1]['kind']!='heading':raise CoverageError('empty canonical heading')
                    self.last_heading={'unit_id':self.units[-1]['id'],'number':number,'command':name,'starred':bool(starred)}
                    continue
                if name in {'footnote','endnote'}:
                    if text[cursor:cursor+1]=='[':cursor=text.index(']',cursor)+1
                    args,cursor=self.arguments(text,cursor,1)
                    old=(self.buffer,self.kind,self.lane,self.table_stack,self.source_origin,self.buffer_refs,self.buffer_expansions,self.buffer_states,self.buffer_math,self.buffer_links)
                    self.buffer=[];self.buffer_refs=[];self.buffer_expansions=[];self.buffer_states=[];self.buffer_math=[];self.buffer_links=[];self.kind='note';self.notes+=1;self.lane='notes';self.table_stack=[]
                    self.parse_child(args[0],offset,depth+1);self.flush('note')
                    self.buffer,self.kind,self.lane,self.table_stack,self.source_origin,self.buffer_refs,self.buffer_expansions,self.buffer_states,self.buffer_math,self.buffer_links=old;continue
                if name in {'url','nolinkurl','href','sourceurl','path'}:
                    args,cursor=self.arguments(text,cursor,2 if name in {'href','sourceurl'} else 1)
                    if len(args)==2:self.linked_display(args[1],args[0],offset,depth+1)
                    else:
                        visible=re.sub(r'\\([^A-Za-z@])',lambda match:match.group(1),args[0]);self.append(visible,offset)
                        if name=='url':self.locator(args[0],visible,offset)
                    continue
                if name in {'ref','pageref','hyperref'}:
                    if name=='hyperref':
                        if text[cursor:cursor+1]!='[':raise CoverageError('unsupported hyperref syntax')
                        end=text.index(']',cursor);target=text[cursor+1:end];cursor=end+1
                        args,cursor=self.arguments(text,cursor,1);self.linked_display(args[0],'#'+target,offset,depth+1,'reference')
                    else:
                        args,cursor=self.arguments(text,cursor,1);target=args[0]
                        marker=f'semanticreference{len(self.references)+1:06d}token'
                        reference={'id':marker,'command':name,'target':target,'source_ref':self.origin_at(offset)}
                        if name=='pageref':
                            # A print page abbreviation belongs to the physical
                            # page number, replaced by the canonical heading.
                            visible=''.join(self.buffer)
                            prefix=re.search(r'(?<![\w\\])pp?\.\s*$',visible)
                            if prefix:
                                reference['print_abbreviation']=visible[prefix.start():]
                                self.buffer=[visible[:prefix.start()]]
                        self.references.append(reference)
                        self.append(marker,offset)
                        self.locator('#'+target,marker,offset,'reference',marker)
                    continue
                if name in {'(','['}:
                    closing='\\'+(')' if name=='(' else ']');end=text.find(closing,cursor)
                    if end<0:raise CoverageError('unclosed TeX math delimiter')
                    self.parse_math(text[cursor:end],offset,depth+1);cursor=end+len(closing);continue
                if name in {'chronologyannotation','chronologyorientationrow'}:
                    args,cursor=self.arguments(text,cursor,1 if name=='chronologyannotation' else 2)
                    call='\\'+name+''.join('{'+arg+'}' for arg in args)
                    projected,_=self.library.expand_chronology_annotations(call,self.head+'\n'+self.body)
                    original_origin=self.origin;self.origin=self.origin_at(offset)
                    self.expansions.append({'name':name,'arguments':args,'definition_source_digest':hashlib.sha256((self.head+'\n'+self.body).encode()).hexdigest()})
                    self.parse(projected,None,depth+1);self.expansions.pop();self.origin=original_origin;continue
                if name=='multicolumn':
                    args,cursor=self.arguments(text,cursor,3);self.parse_child(args[2],offset,depth+1);continue
                if name=='multirow':raise CoverageError('multirow requires an explicit semantic row contract')
                if name in {'cmidrule','cline'}:
                    if text[cursor:cursor+1]=='(':cursor=text.index(')',cursor)+1
                    _,cursor=self.arguments(text,cursor,1);continue
                if name in {'addlinespace','nopagebreak'}:
                    if text[cursor:cursor+1]=='[':cursor=text.index(']',cursor)+1
                    continue
                if name=='item':
                    self.flush();self.kind='list-item'
                    if text[cursor:cursor+1]=='[':
                        close=text.index(']',cursor);self.parse_child(text[cursor+1:close],offset,depth+1);self.flush('term');cursor=close+1;self.kind='list-item'
                    continue
                if name=='bibitem':
                    self.flush();self.kind='list-item'
                    if text[cursor:cursor+1]=='[':cursor=text.index(']',cursor)+1
                    _,cursor=self.arguments(text,cursor,1);continue
                if name in TABLES:
                    args,cursor=self.arguments(text,cursor,TABLES[name]);self.parse('\\begin{'+name+'}'+''.join('{'+arg+'}' for arg in args),None,depth+1);continue
                if name.startswith('end') and name[3:] in TABLES:self.parse('\\end{'+name[3:]+'}',None,depth+1);continue
                if name in {'begin','end'}:
                    args,cursor=self.arguments(text,cursor,1);environment=args[0]
                    if name=='begin':
                        self.push_scope('environment:'+environment)
                        if environment in TABLES:
                            if self.table_stack:raise CoverageError('nested table requires an explicit semantic cell contract')
                            _,cursor=self.arguments(text,cursor,TABLES[environment]);self.flush();self.table_number+=1;self.table_stack.append({'id':f'table-{self.table_number}','row':0,'column':0});self.environment_stack.append((environment,''));continue
                        if environment in {'itemize','enumerate','description'}:
                            if text[cursor:cursor+1]=='[':cursor=text.index(']',cursor)+1
                            self.flush();self.item_depth+=1;self.environment_stack.append((environment,''));continue
                        if environment in ENV_LAYOUT:
                            self.flush();self.environment_stack.append((environment,''));continue
                        if environment=='multicols':
                            _,cursor=self.arguments(text,cursor,1);self.flush();self.environment_stack.append((environment,''));continue
                        if environment=='minipage':
                            if text[cursor:cursor+1]=='[':cursor=text.index(']',cursor)+1
                            args,cursor=self.arguments(text,cursor,1);self.flush();self.minipages+=1
                            self.boundaries.append({'id':f'minipage-{self.minipages}','environment':'minipage','source_ref':self.origin_at(offset),'unit_start':len(self.units),'layout_width':args[0]})
                            self.environment_stack.append((environment,''));continue
                        if environment in {'tikzpicture','picture'}:raise CoverageError('specialized semantic asset/layout adapter required: '+environment)
                        if environment not in self.environments:raise CoverageError('unknown executed environment '+environment)
                        count,default,opening,closing=self.environments[environment]
                        args,cursor=self.arguments(text,cursor,count,default);self.environment_stack.append((environment,_replace(closing,args)))
                        original_origin=self.origin;self.origin=self.origin_at(offset);self.parse(_replace(opening,args),None,depth+1);self.origin=original_origin;continue
                    self.flush(cell_end=environment in TABLES)
                    if environment in self.environments and environment not in TABLES and environment not in ENV_LAYOUT:
                        owners=[i for i,(name,_) in enumerate(self.environment_stack) if name==environment]
                        if not owners:raise CoverageError('unbalanced source environment '+environment)
                        closing=self.environment_stack[owners[-1]][1]
                        if closing:self.parse(closing,None,depth+1)
                        if not self.environment_stack or self.environment_stack[-1][0]!=environment:raise CoverageError('environment closing leaves unmatched child '+environment)
                        self.environment_stack.pop()
                    else:
                        if not self.environment_stack or self.environment_stack[-1][0]!=environment:raise CoverageError('unbalanced source environment '+environment)
                        self.environment_stack.pop()
                        if environment=='minipage':
                            boundary=next(record for record in reversed(self.boundaries) if 'unit_end' not in record)
                            boundary['unit_end']=len(self.units)
                        if environment in TABLES:
                            if not self.table_stack:raise CoverageError('table scope lost')
                            self.table_stack.pop()
                        elif environment in {'itemize','enumerate','description'}:self.item_depth-=1
                    self.pop_scope('environment:'+environment)
                    continue
                if name in {'propertitle','weektitle','pcweektitle'}:
                    count=4 if name=='propertitle' else 3
                    args,cursor=self.arguments(text,cursor,count);self.flush()
                    for arg in args:
                        self.kind='title';self.parse_child(arg,offset,depth+1);self.flush('title')
                    continue
                if name in {'dossierprose','dossierevent'} and self.macros.get(name,(None,))[0]==1:
                    args,cursor=self.arguments(text,cursor,1);self.flush(cell_end=True)
                    saved_table=self.table_stack;self.table_stack=[];self.kind='table-note'
                    # The shared one-argument full-width note is linearized
                    # below its table. Expand the entire owning definition:
                    # a same-named three-argument event is an ordinary row,
                    # and injected labels in either definition remain content.
                    macro=self.macros[name];original_origin=self.origin;self.origin=self.origin_at(offset)
                    self.expansions.append(self.macro_frame(name,macro,args,offset,None if base is None else base+cursor,None if program_base is None else program_base+command_start,None if program_base is None else program_base+cursor))
                    self.parse(_replace(macro[2],args),None,depth+1);self.flush('table-note')
                    self.expansions.pop();self.origin=original_origin;self.table_stack=saved_table;continue
                if name=='AIDocumentRevisionTimestamp':
                    args,cursor=self.arguments(text,cursor,1);self.revision=args[0]
                    self.flush();self.append('Last revised (UTC): '+args[0],offset);self.flush('revision');continue
                if name in {'AIModelContribution','AIModelContributionRepeat','AIGenerationProvenance','AIInheritedGenerationMetadata'}:
                    _,cursor=self.arguments(text,cursor,{'AIGenerationProvenance':6,'AIInheritedGenerationMetadata':1}.get(name,3));continue
                if name=='SemanticMathUnit':
                    args,cursor=self.arguments(text,cursor,1);key=args[0]
                    if key not in self.semantic_units:raise CoverageError('undeclared semantic math unit '+key)
                    unit=self.semantic_units[key]
                    if unit.get('kind')!='math' or not unit.get('source_sha256') or not unit.get('ast_digest') or not unit.get('expected_mathml_signature'):raise CoverageError('incomplete canonical math contract '+key)
                    self.flush();index=len(self.units)+1
                    self.units.append({'id':f'unit-{index:06d}','occurrence_id':key,'kind':'math','lane':self.lane,'source_ref':unit['source_ref'],'source_sha256':unit['source_sha256'],'ast_digest':unit['ast_digest'],'expected_mathml_signature':unit['expected_mathml_signature'],'expected':'','macro_state_digest':self.macro_digest})
                    continue
                if name=='TriptychRightsNotice':self.rights_notice(offset,depth);continue
                if name in {'setlist','fancyhead','fancyfoot','fancyhf'}:
                    if text[cursor:cursor+1]=='[':cursor=text.index(']',cursor)+1
                    _,cursor=self.arguments(text,cursor,1);continue
                if name in {'titleformat','titlespacing'}:
                    if text[cursor:cursor+1]=='*':cursor+=1
                    _,cursor=self.arguments(text,cursor,5 if name=='titleformat' else 4)
                    if text[cursor:cursor+1]=='[':cursor=text.index(']',cursor)+1
                    continue
                if name in {'if','ifdefined','ifx','ifnum','else','fi','csname','endcsname','expandafter','edef','xdef','directlua','write','input','include'}:raise CoverageError('unsupported executed TeX control flow \\'+name)
                if name in self.macros:
                    macro=self.macros[name]
                    if macro[0]=='refuse':raise CoverageError('unmodelled macro '+name+': '+str(macro[2]))
                    args,cursor=self.arguments(text,cursor,macro[0],macro[1]);original_origin=self.origin;self.origin=self.origin_at(offset);self.expansions.append(self.macro_frame(name,macro,args,offset,None if base is None else base+cursor,None if program_base is None else program_base+command_start,None if program_base is None else program_base+cursor))
                    self.parse(_replace(macro[2],args),None,depth+1);self.expansions.pop();self.origin=original_origin;continue
                raise CoverageError('unknown executed command \\'+name)
            if ch=='{':
                group,end=self.library.brace_group(text,cursor);self.push_scope('brace');argument_start=cursor+1
                self.parse_child(group,offset,depth+1,source_base=None if base is None else base+argument_start,program_base=None if program_base is None else program_base+argument_start);self.pop_scope('brace');cursor=end;continue
            if ch=='}':raise CoverageError('unbalanced closing source brace')
            if ch=='&' and self.table_stack:self.flush(cell_end=True);self.table_stack[-1]['column']+=1;cursor+=1;continue
            if ch=='~':self.append(' ',offset);cursor+=1;continue
            if ch=='$':
                end=text.find('$',cursor+1)
                if end<0:raise CoverageError('unclosed math')
                math=text[cursor+1:end]
                self.parse_math(math,offset,depth+1);cursor=end+1;continue
            if ch=='\n':
                if re.match(r'\n\s*\n',text[cursor:]):
                    self.flush();cursor+=len(re.match(r'\n\s*\n',text[cursor:]).group());continue
                self.append(' ',offset);cursor+=1;continue
            self.append(ch,offset);cursor+=1

    def parse_math(self,text,offset,depth):
        # Current static-flow math consists of literal text and this explicit
        # glyph set. Schemes/fractions need an independently typed MathML AST.
        source_text=text
        names=COMMAND.findall(text)
        allowed={'Theta','Lambda','alpha','aleph','pm','cdot','rightarrow','longrightarrow','circ','ast','leq'}
        if any(name not in allowed for name in names):raise CoverageError('unsupported semantic math glyph/control: '+repr(names))
        for name in names:
            if name=='longrightarrow':self.display_adaptations.append({'role':'arrow-length-reflow','command':name,'display':'→','source_ref':self.origin_at(offset)})
        # Only the corpus's degree and asterisk markers flatten superscripts.
        # Other powers/subscripts need a typed MathML AST rather than losing
        # their grouping or silently becoming ordinary adjacent characters.
        def superscript_marker(match):
            name=next(group for group in match.groups() if group)
            if name=='ast':
                self.display_adaptations.append({'role':'asterisk-marker-shape-reflow','command':'ast','display':'*','source_ref':self.origin_at(offset)})
                return '*'
            return '\\circ'
        text=re.sub(r'\^(?:\{\\(circ|ast)\}|\\(circ|ast))',superscript_marker,text)
        if '^' in text or '_' in text:raise CoverageError('native math power/subscript requires a typed MathML contract')
        projected=COMMAND.sub(lambda match:GLYPHS[match.group(1)],text)
        if '{' in projected or '}' in projected:raise CoverageError('unmodelled native math grouping')
        projected=projected.replace('-','−')
        literal_chars=set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+=<>.,()[]|−*')
        literal_chars.update(GLYPHS[name] for name in allowed)
        if any(not (char.isspace() or char in literal_chars) for char in projected) or (not normalized(projected) and projected.strip()!='*'):raise CoverageError('unsupported native math literal')
        self.buffer_math.append({'expected':math_identity(projected),'source_ref':self.origin_at(offset),'source_sha256':hashlib.sha256(source_text.encode()).hexdigest()})
        self.append(projected,offset)

    def rights_notice(self,offset,depth):
        if self.rights:return
        self.rights=True
        macro=self.macros.get('TriptychRightsNotice')
        if macro is None:raise CoverageError('canonical rights notice definition missing')
        body=macro[2]
        start=body.find(r'\textbf{Reuse and rights.}')
        end=body.find(r'\end{minipage}',start)
        if start<0 or end<0:raise CoverageError('canonical rights notice shape changed')
        self.flush();self.kind='rights';self.parse(body[start:end],None,depth+1);self.flush('rights')

    def run(self,fragment=False):
        if not fragment:
            try:title,subtitle=self.library.pdf_metadata(self.head)
            except Exception:title,subtitle='', ''
            for field,value in (('metadata-title',title),('metadata-subtitle',subtitle)):
                if value:
                    self.kind=field;self.parse(value,None);self.flush(field)
        self.parse(self.body)
        self.flush()
        if self.environment_stack or self.scope_stack:raise CoverageError('unclosed source environments/scopes')
        if self.diagram_seen!=[asset['asset_id'] for asset in self.diagram_assets]:raise CoverageError('canonical diagram occurrences were not all executed in order')
        if not fragment and not self.rights:self.rights_notice(None,0)
        self.resolve_references()
        navigation_allowed=r'\tableofcontents' in self.body
        entrypoint=self.selection.get('selection',{}).get('entrypoint')
        if entrypoint:
            declaration=self.library.ROOT/entrypoint
            record=declaration.parent/'web-edition.toml'
            if record.is_file():navigation_allowed=navigation_allowed or tomllib.loads(record.read_text()).get('contents',False)
        contract={'scope':'canonical-fragment' if fragment else 'canonical-publication','navigation_allowed':bool(navigation_allowed),'entrypoint':self.selection.get('selection',{}).get('entrypoint'),'role':self.selection.get('selection',{}).get('role'),'selection_digest':self.selection.get('selection',{}).get('selection_digest'),'macro_state_digest':self.macro_digest,'units':self.units,'links':self.links,'containers':self.boundaries,'layout_omissions':self.layout_omissions,'references':self.references,'display_adaptations':self.display_adaptations,'counter_displays':self.counter_displays}
        contract['ledger_digest']=hashlib.sha256(json.dumps(contract,sort_keys=True).encode()).hexdigest()
        return contract

    def resolve_references(self):
        by_id={unit['id']:unit for unit in self.units}
        for reference in self.references:
            labels=self.labels.get(reference['target'],[])
            if len(labels)!=1:raise CoverageError('reference requires one canonical label: '+reference['target'])
            label=labels[0];heading=label['heading'];unit=by_id[heading['unit_id']] if heading else None
            if reference['command']=='pageref':
                if unit is None:raise CoverageError('page reference requires a canonical heading label: '+reference['target'])
                value=unit['expected']
            else:
                if not label['reference']:raise CoverageError('reference label has no canonical currentlabel: '+reference['target'])
                reference['display']=label['reference']['number'];reference['counter']=label['reference']['counter'];reference['counter_source_ref']=label['reference']['source_ref']
                value=normalized(reference['display'])
            if 'semanticreference' in value:raise CoverageError('reference target heading contains an unresolved reference')
            reference.update(expected=value,label_source_ref=label['source_ref'])
            if unit:reference.update(heading_unit_id=unit['id'],heading_source_ref=unit['source_ref'])
            occurrences=0
            for owner in self.units:
                if reference['id'] not in owner['expected']:continue
                occurrences+=owner['expected'].count(reference['id'])
                owner['expected']=owner['expected'].replace(reference['id'],value)
                owner['text_digest']=hashlib.sha256(owner['expected'].encode()).hexdigest()
                owner.setdefault('references',[]).append(reference)
                for locator in owner.get('locators',[]):
                    if locator.get('reference_id')==reference['id']:locator['expected_display']=value
            if occurrences!=1:raise CoverageError('reference occurrence is missing or repeated: '+reference['id'])


class HtmlLedger(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.stack=[];self.units=[];self.links=[];self.hidden=0;self.frames=[];self.note_depth=0;self.navigation_depth=0;self.cell_frame=None;self.math=None;self.containers=[];self.container_stack=[];self.active_link=None;self.source_length=0;self.line_starts=[0]
    def feed(self,data):
        self.line_starts.extend(self.source_length+index+1 for index,char in enumerate(data) if char=='\n')
        self.source_length+=len(data);super().feed(data)
    def host_position(self):
        line,column=self.getpos()
        return self.line_starts[line-1]+column
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);parent_note=self.note_depth
        if self.math is not None and tag!='math':
            if tag not in {'mrow','mi','mn','mo','mtext','mfrac','msub','msup','msubsup','munder','mover','munderover'}:raise CoverageError('unsupported output MathML tag '+tag)
            self.math['signature'].append(['start',tag])
        if attrs.get('data-semantic-minipage'):
            record={'id':attrs['data-semantic-minipage'],'tag':tag,'unit_start':len(self.units)};self.containers.append(record);self.container_stack.append(record)
        hidden=self.hidden or attrs.get('id','').startswith('fnref:') or 'footnote-backref' in attrs.get('class','').split() or 'footnote-ref' in attrs.get('class','').split()
        if tag=='img':
            if not attrs.get('data-semantic-diagram'):raise CoverageError('output image has no canonical semantic binding')
            if self.frames and self.frames[-1]['text']:self._flush_frame(self.frames[-1])
            self.units.append({'kind':'diagram','lane':'notes' if parent_note else 'body','text':'','index':len(self.units),'host_start':self.host_position(),'content_start':self.host_position(),'host_tag':tag,'asset_id':attrs.get('data-semantic-diagram'),'source_asset':attrs.get('data-source-asset'),'src':attrs.get('src'),'svg_sha256':attrs.get('data-svg-sha256'),'source_tex_sha256':attrs.get('data-source-tex-sha256'),'selection_digest':attrs.get('data-selection-digest'),'source_labels_digest':attrs.get('data-source-labels-sha256')})
        if tag=='a' and not hidden and attrs.get('href'):
            if self.active_link is not None:raise CoverageError('nested output hyperlink')
            if not self.frames:raise CoverageError('output hyperlink has no containing content block')
            target=uri_identity(attrs['href']);self.links.append(target)
            self.active_link={'target':target,'text':[],'frame':self.frames[-1]}
        note=parent_note or attrs.get('id','').startswith('fn:') or 'footnote' in attrs.get('class','').split()
        navigation=self.navigation_depth or 'toc' in attrs.get('class','').split() or attrs.get('role')=='doc-toc'
        if tag not in VOID:self.stack.append((tag,self.hidden,self.note_depth,self.navigation_depth))
        self.hidden=int(bool(hidden));self.note_depth=int(bool(note));self.navigation_depth=int(bool(navigation))
        if tag=='br' and self.frames and not self.hidden:
            if self.cell_frame is not None:self.cell_frame['text'].append(' ')
            else:self._flush_frame(self.frames[-1])
        if tag in BLOCKS and self.cell_frame is not None and tag not in {'td','th'}:
            if tag=='math':raise CoverageError('typed math inside a table cell requires a cell semantic contract')
            self.cell_frame['text'].append(' ');return
        if tag in BLOCKS:
            if tag=='math':
                if self.math is not None:raise CoverageError('nested semantic math unit')
                self.math={'id':attrs.get('data-semantic-unit'),'signature':[]}
                if not self.math['id']:raise CoverageError('output math lacks canonical semantic unit identity')
            if self.frames and self.frames[-1]['text'] and tag in {'p','li','dt','dd','td','th','h1','h2','h3','h4','h5','h6','math'}:self._flush_frame(self.frames[-1])
            self.frames.append({'tag':tag,'host_start':self.host_position(),'content_start':None,'host_tag':tag,'text':[],'locators':[],'lane':'notes' if note else ('navigation' if navigation else 'body')})
            if tag in {'td','th'}:self.cell_frame=self.frames[-1]
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID:self.handle_endtag(tag)
    def handle_data(self,data):
        if not self.hidden and self.frames:
            if self.math is not None and data.strip():self.math['signature'].append(['text',' '.join(data.split())])
            if self.frames[-1]['content_start'] is None:self.frames[-1]['content_start']=self.host_position()
            self.frames[-1]['text'].append(data)
            if self.active_link is not None:self.active_link['text'].append(data)
    def _flush_frame(self,frame):
        if self.active_link is not None and self.active_link['frame'] is frame:raise CoverageError('output hyperlink crosses content block boundary')
        raw_text=''.join(frame['text']);text=normalized(raw_text);locators=frame['locators'];content_start=frame['content_start'] if frame['content_start'] is not None else frame['host_start'];frame['text']=[];frame['locators']=[];frame['content_start']=None
        if frame['tag']=='math':
            self.units.append({'kind':'math','lane':frame['lane'],'text':text,'index':len(self.units),'host_start':frame['host_start'],'content_start':frame['host_start'],'host_tag':frame['host_tag'],'semantic_unit':self.math['id'],'signature':self.math['signature']});self.math=None;return
        if text or raw_text.strip()=='*':self.units.append({'kind':frame['tag'],'lane':frame['lane'],'text':text,'raw_text':raw_text,'locators':locators,'host_start':frame['host_start'],'content_start':content_start,'host_tag':frame['host_tag'],'index':len(self.units)})
        elif locators:raise CoverageError('output hyperlink has no visible containing content unit')
    def handle_endtag(self,tag):
        if tag=='a' and self.active_link is not None:
            capture=self.active_link;self.active_link=None
            capture['frame']['locators'].append({'target':capture['target'],'display':normalized(''.join(capture['text']))})
        if self.math is not None and tag!='math':self.math['signature'].append(['end',tag])
        if self.container_stack and self.container_stack[-1]['tag']==tag:
            self.container_stack[-1]['unit_end']=len(self.units);self.container_stack.pop()
        if tag in BLOCKS and self.cell_frame is not None and tag not in {'td','th'}:
            self.cell_frame['text'].append(' ')
        elif tag in BLOCKS:
            if not self.frames or self.frames[-1]['tag']!=tag:raise CoverageError('unbalanced output content block '+tag)
            self._flush_frame(self.frames.pop())
            if tag in {'td','th'}:self.cell_frame=None
        if tag not in VOID:
            if not self.stack or self.stack[-1][0]!=tag:raise CoverageError('unbalanced output HTML '+tag)
            _,self.hidden,self.note_depth,self.navigation_depth=self.stack.pop()
    def finish(self):
        if self.stack or self.frames or self.active_link:raise CoverageError('unclosed output HTML')
        return self.units


def expected_units(selection,library):
    """Return an occurrence-aware canonical ledger, or refuse unknown source."""
    return Ledger(selection,library).run()


def expected_fragment_units(selection,library):
    """Audit one source-owned fragment, without synthetic publication colophon.

    This checks only the supplied canonical selected fragment. Its caller must
    independently select/cover every fragment and check publication metadata,
    rights, diagrams and document structure at the publication boundary.
    """
    return Ledger(selection,library).run(fragment=True)


def check_units(ledger,rendered,library=None):
    parser=HtmlLedger();parser.feed(rendered);actual=parser.finish()
    failures=[];matched=[]
    for lane in ('body','notes'):
        expected=[unit for unit in ledger['units'] if unit['lane']==lane]
        candidates=[unit for unit in actual if unit['lane']==lane]
        cursor=0
        for unit in expected:
            compatible={'table-cell':{'td','th'},'heading':{'h1','h2','h3','h4','h5','h6'},'term':{'dt'},'table-note':{'p','td','th'},'title':{'p','h1','h2','h3'},'metadata-title':{'h1'},'metadata-subtitle':{'p'},'math':{'math'},'diagram':{'diagram'}}.get(unit['kind'],{'p','li','dd','dt','td','th','figcaption','math'})
            found=None
            for index in range(cursor,len(candidates)):
                candidate=candidates[index]
                if candidate['kind'] not in compatible:continue
                value=unit['expected']
                if unit['kind']=='diagram':
                    same=(candidate['kind']=='diagram' and candidate['asset_id']==unit['occurrence_id'] and candidate['source_asset']==unit['occurrence_id'] and candidate['src']==unit['rendered_src'] and all(candidate.get(key)==unit.get(key) for key in ('svg_sha256','source_tex_sha256','selection_digest','source_labels_digest')))
                elif unit['kind']=='math':same=(candidate['kind']=='math' and candidate.get('semantic_unit')==unit['occurrence_id'] and candidate.get('signature')==unit['expected_mathml_signature'])
                else:
                    same=value==candidate['text']
                    if same and unit.get('math_literals'):
                        math_cursor=0;visible=math_identity(candidate['raw_text'])
                        for literal in unit['math_literals']:
                            position=visible.find(literal['expected'],math_cursor)
                            if position<0:same=False;break
                            math_cursor=position+len(literal['expected'])
                    if same:
                        source_locators=[(link['expected_target'],link['expected_display']) for link in unit.get('locators',[])]
                        output_locators=[(link['target'],link['display']) for link in candidate.get('locators',[])]
                        same=source_locators==output_locators
                if same:found=index;break
            if found is None:
                failures.append({'id':unit['id'],'kind':unit['kind'],'source_ref':unit['source_ref'],'expected':unit['expected'],'reason':'missing, changed, repeated or reordered content block'})
            else:
                matched.append({'id':unit['id'],'output_block':candidates[found]['index']});cursor=found+1
    used={match['output_block'] for match in matched}
    header_signatures={(unit['expected'],tuple((link['expected_target'],link['expected_display']) for link in unit.get('locators',[]))) for unit in ledger['units'] if unit['kind']=='table-cell' and unit.get('row')==0}
    heading_texts={unit['expected'] for unit in ledger['units'] if unit['kind'] in {'heading','title','metadata-title'}}
    for unit in actual:
        if unit['index'] in used:continue
        if unit['kind']=='th' and (unit['text'],tuple((link['target'],link['display']) for link in unit.get('locators',[]))) in header_signatures:continue
        if unit['lane']=='navigation' and ledger.get('navigation_allowed') and unit['text'] in heading_texts:continue
        failures.append({'kind':'unexpected-output-block','output_block':unit['index'],'output_kind':unit['kind'],'text':unit['text'],'reason':'output block has no canonical content or explicitly generated navigation/header owner'})
    expected_containers=[container['id'] for container in ledger.get('containers',[])]
    actual_containers=[container['id'] for container in parser.containers]
    if expected_containers!=actual_containers:failures.append({'kind':'minipage-containers','expected':expected_containers,'found':actual_containers})
    expected_links=Counter(uri_identity(link['target'],tex=True) for link in ledger['links'])
    actual_links=Counter(parser.links)
    for target,count in expected_links.items():
        if actual_links[target]<count:failures.append({'kind':'locator','target':target,'expected':count,'found':actual_links[target]})
    return {'status':'refused' if failures else 'pass','complete':not failures,'unit_count':len(ledger['units']),'matched_units':matched,'failures':failures,'missing_units':failures,'macro_state_digest':ledger['macro_state_digest'],'ledger_digest':ledger['ledger_digest'],'selection_scope':ledger.get('scope','canonical-publication'),'scope':'Canonical bounded-DSL macro and environment expansion; all short/long visible blocks; ordered source occurrences and local table cells; independently ordered footnotes; ordered per-containing-unit locator targets and display text; source-local native math signatures. Owning converter structure audits remain required.'}
