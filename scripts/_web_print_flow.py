"""Source-backed semantic projections for the current flow-print DSL.

These projections remove dimension assignments and physical
continuation furniture, preserve the actual aleph witness glyph, preserve all
novena prayer/status fields while retaining typed language lanes, and preserve
canonical title display paragraphs. Unknown syntax is refused rather than absorbed
by a blanket command/environment whitelist.
"""
from __future__ import annotations
from collections import Counter
import copy
import hashlib
import html
import json
import re
import unicodedata

class FlowFixError(ValueError):pass

_LENGTH_REGISTERS={'itemsep','parsep','columnsep'}
_DIMENSION=re.compile(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:pt|em|ex|in|cm|mm|bp|pc|dd|cc|sp)\Z')
_SETLENGTH=re.compile(r'\\setlength(?![A-Za-z@])')


def _hash(text):return hashlib.sha256(text.encode()).hexdigest()


def drop_length_assignments(text,library):
    """Only known length-register assignments with literal dimensions are inert."""
    pieces=[];cursor=0;projections=[]
    for match in _SETLENGTH.finditer(library.mask_tex_comments(text)):
        if match.start()<cursor:continue
        register,index=library.brace_group(text,match.end())
        register=register.strip()
        name=register.removeprefix('\\')
        if register!='\\'+name or name not in _LENGTH_REGISTERS:continue
        value,end=library.brace_group(text,index)
        if not _DIMENSION.fullmatch(value.strip()):
            raise FlowFixError('unsupported '+name+' dimension assignment: '+value)
        pieces.extend((text[cursor:match.start()],'{}'))
        projections.append({'kind':'length-assignment','register':name,'value':value.strip(),'source_offset':match.start(),'source_sha256':_hash(text[match.start():end])})
        cursor=end
    pieces.append(text[cursor:])
    return ''.join(pieces),projections


def preserve_aleph(text):
    """The actual Codex Sinaiticus siglum, never a deleted unknown math command."""
    pattern=re.compile(r'\\\(\s*\\aleph\s*\\\)')
    projections=[]
    def replace(match):
        projections.append({'kind':'witness-siglum','source_offset':match.start(),'source':match.group(),'rendered':'ℵ'})
        return 'ℵ'
    return pattern.sub(replace,text),projections


def _control_word_gap(text,cursor):
    """TeX ignores delimiter space, but a blank line remains a paragraph."""
    first_endline=None
    while cursor<len(text):
        if text[cursor] in ' \t\r':cursor+=1;continue
        if text[cursor]=='%':
            end=text.find('\n',cursor)
            cursor=len(text) if end<0 else end+1
            continue
        if text[cursor]=='\n':
            if first_endline is not None:return first_endline
            first_endline=cursor;cursor+=1;continue
        break
    return cursor


def preserve_glyph_aliases(text,head,library):
    r"""Project exact zero-argument accent/ligature aliases before Pandoc.

Pandoc expands the owner's aeacute but retains its control-word delimiter
space, splitting qu\aeacute sumus into two visible words. TeX consumes that
delimiter. Only canonical aliases with the exact accent/ligature grammar are
handled; unknown content macros remain untouched and subject to refusal.
"""
    macros,_=library.command_definitions(library.strip_tex_comments(head))
    ligatures={'ae':'æ','AE':'Æ','oe':'œ','OE':'Œ'}
    aliases={}
    for name,(count,default,body) in macros.items():
        if count or default is not None:continue
        match=re.fullmatch(r"\s*\\'\s*\{\s*\\(ae|AE|oe|OE)\s*\}\s*",library.strip_tex_comments(body))
        if match:aliases[name]=(unicodedata.normalize('NFC',ligatures[match.group(1)]+'\u0301'),_hash(body))
    if not aliases:return text,[]
    definitions=[]
    for kind,definition in library.walk_definitions(library.mask_tex_comments(text)):
        if kind!='definition':continue
        if definition.name in aliases:
            raise FlowFixError('scoped glyph-alias reassignment requires an explicit adapter: '+definition.name)
        definitions.append((definition.start,definition.end))
    pattern=re.compile(r'\\('+'|'.join(re.escape(name) for name in sorted(aliases,key=len,reverse=True))+r')(?![A-Za-z@])')
    pieces=[];cursor=0;records=[]
    for match in pattern.finditer(library.mask_tex_comments(text)):
        if match.start()<cursor:continue
        if any(start<=match.start()<end for start,end in definitions):continue
        glyph,digest=aliases[match.group(1)]
        end=_control_word_gap(text,match.end())
        pieces.extend((text[cursor:match.start()],glyph));cursor=end
        records.append({'kind':'canonical-glyph-alias','macro':match.group(1),'source_offset':match.start(),'source_definition_sha256':digest,'rendered':glyph})
    pieces.append(text[cursor:])
    return ''.join(pieces),records


def preserve_known_separator(text,head,library,context):
    """Preserve known literal separator glyphs, including inside definitions."""
    glyphs={'textperiodcentered':'·','textbar':'|','space':' '}
    macros,_=library.command_definitions(library.strip_tex_comments(head))
    conflicts=set(glyphs)&set(macros)
    if conflicts:raise FlowFixError('source separator redefinition requires an explicit glyph adapter: '+', '.join(sorted(conflicts)))
    for kind,definition in library.walk_definitions(library.mask_tex_comments(text)):
        if kind=='definition' and definition.name in glyphs:
            raise FlowFixError('source separator reassignment requires an explicit glyph adapter: '+definition.name)
    records=[]
    pattern=re.compile(r'\\(textperiodcentered|textbar|space)(?![A-Za-z@])'+library.CONTROL_WORD_SPACE+r'(?:\{\})?')
    def replace(match):
        glyph=glyphs[match.group(1)]
        records.append({'kind':'canonical-separator-glyph','macro':match.group(1),'context':context,'source_offset':match.start(),'source_sha256':_hash(match.group()),'rendered':glyph})
        return glyph
    return pattern.sub(replace,text),records


def guard_literal_brackets(text,library,context):
    """A literal paragraph-opening bracket is content, never a par option."""
    pieces=[];cursor=0;records=[]
    for match in re.finditer(r'\\par(?![A-Za-z@])',library.mask_tex_comments(text)):
        next_token=library.skip_gap(text,match.end())
        if text[next_token:next_token+1]!='[':continue
        pieces.extend((text[cursor:match.end()],'{}'));cursor=match.end()
        records.append({'kind':'literal-paragraph-bracket-guard','context':context,'source_offset':match.start()})
    pieces.append(text[cursor:])
    return ''.join(pieces),records


def canonical_openings(ledger,library):
    """Explicit print-only opening oracle derived before conversion.

Canonical ledger units already type layout arguments and preserve explicit
source paragraph/display-line boundaries. The old lexical heuristic can see
``em`` in vspace{0.08em} before it sees the actual lowercase display line.
No converted text or failure list contributes an allowed opening here.
"""
    if not ledger or 'units' not in ledger:return None
    openings=set()
    for unit in ledger['units']:
        if unit.get('kind') in {'metadata-title','metadata-subtitle'}:continue
        word=library.WORD_RE.search(unit.get('expected',''))
        if word:openings.add(word.group().casefold())
    return sorted(openings)


def drop_longtable_footers(text,library):
    """Physical longtable foot/last-foot definitions are not body rows.

The source parser identifies their role by TeX's actual endfoot/endlastfoot
markers. It never matches a prose phrase such as 'continued' in a real row.
"""
    pieces=[];cursor=0;projections=[]
    for match in re.finditer(r'\\begin\s*\{longtable\}',library.mask_tex_comments(text)):
        if match.start()<cursor:continue
        _,start=library.brace_group(text,match.end())
        end_match=re.search(r'\\end\s*\{longtable\}',library.mask_tex_comments(text[start:]))
        if not end_match:raise FlowFixError('unclosed longtable')
        stop=start+end_match.start();region=text[start:stop]
        markers=list(re.finditer(r'\\(?:endfirsthead|endhead|endfoot|endlastfoot)(?![A-Za-z@])',library.mask_tex_comments(region)))
        last_head=0;remove=[]
        for token in markers:
            name=token.group()[1:]
            if name in ('endfirsthead','endhead'):last_head=token.end()
            elif name in ('endfoot','endlastfoot'):
                remove.append((last_head,token.end(),name));last_head=token.end()
        for a,b,name in reversed(remove):
            projections.append({'kind':'longtable-physical-footer','role':name,'source_offset':start+a,'source_sha256':_hash(region[a:b])})
            region=region[:a]+'\n'+region[b:]
        pieces.extend((text[cursor:start],region));cursor=stop
    pieces.append(text[cursor:])
    return ''.join(pieces),projections


def _stack_minipages(body,library):
    """Preserve every word/argument of the owning prayer macro, in lane order."""
    begin=re.compile(r'\\begin\s*\{minipage\}')
    pieces=[];cursor=0;count=0
    for match in begin.finditer(library.mask_tex_comments(body)):
        index=library.skip_gap(body,match.end())
        if body[index:index+1]=='[':
            end=body.find(']',index)
            if end<0 or body[index+1:end].strip()!='t':raise FlowFixError('unsupported prayer minipage alignment')
            index=library.skip_gap(body,end+1)
        width,end=library.brace_group(body,index)
        if width.strip()!=r'0.48\linewidth':raise FlowFixError('unsupported prayer minipage width')
        pieces.extend((body[cursor:match.start()],r'\begin{quote}'))
        cursor=end;count+=1
    pieces.append(body[cursor:]);result=''.join(pieces)
    endings=len(re.findall(r'\\end\s*\{minipage\}',result))
    if count!=2 or endings!=2:raise FlowFixError('prayer adapter requires exactly two complete language lanes')
    result=re.sub(r'\\end\s*\{minipage\}',lambda _:r'\end{quote}',result)
    result=re.sub(r'\\hfill(?![A-Za-z@])','\n',result)
    return result


def prayer_shim(selection,library):
    """Use canonical prayer wrappers verbatim, preserving typed language lanes.

The reader shim flattens bilingualprayer. This print projection preserves the
owner's actual minipages. No prayer/status prose is maintained in this module.
"""
    macros,_=library.command_definitions(library.strip_tex_comments(selection['head']))
    additions=[];projections=[]
    base_known=library.defined_names(library.SHIM.read_text())
    known=library.defined_names(library.SHIM.read_text()+library.local_definitions(selection['head']))
    for name in ('bilingualprayer','carmellatinprayer'):
        macro=macros.get(name)
        if macro is None:continue
        if macro[0]!=4 or macro[1] is not None:raise FlowFixError('unsupported '+name+' signature')
        body=macro[2]
        if Counter(re.findall(r'#([1-4])',body))!=Counter({'1':1,'2':1,'3':1,'4':1}):
            raise FlowFixError(name+' field mapping changed; explicit reconciliation required')
        # Validate the current two-lane structure without altering its text.
        _stack_minipages(body,library)
        failures=library.undefined_uses({selection.get('entrypoint_path','canonical-prayer-macro'):body},known)
        if failures:raise FlowFixError('\n'.join(failures))
        command='renewcommand' if name in base_known else 'newcommand'
        additions.append('\n\\'+command+'{\\'+name+'}[4]{'+body+'}\n')
        projections.append({'kind':'paired-prayer-lanes','macro':name,'source_definition_sha256':_hash(body),'fields':[1,2,3,4],'lanes':2})
    return ''.join(additions),projections


def table_environment_shim(selection,library):
    """Retain the selected owner's complete timeline header definition.

The shared reader shim has a different accounttimeline vocabulary from the
Claude institutional-history owner. Its canonical opening/closing program is
derived here, including literal header words; no header prose is copied into
this adapter and no expected source cell is relaxed.
"""
    source=library.strip_tex_comments(selection['head'])
    pattern=re.compile(r'\\((?:new|renew)environment)\*?\s*\{\s*accounttimeline\s*\}')
    definition=None
    for match in pattern.finditer(source):
        if definition is not None and match.group(1)=='newenvironment':
            raise FlowFixError('duplicate canonical accounttimeline definition')
        cursor=library.skip_gap(source,match.end())
        if source[cursor:cursor+1]=='[':
            end=source.find(']',cursor)
            if end<0 or source[cursor+1:end].strip()!='0':
                raise FlowFixError('unsupported accounttimeline environment signature')
            cursor=library.skip_gap(source,end+1)
        opening,cursor=library.brace_group(source,cursor)
        closing,cursor=library.brace_group(source,cursor)
        definition=(opening,closing)
    if definition is None:return '',[]
    opening,closing=definition
    known=library.defined_names(library.SHIM.read_text()+library.local_definitions(selection['head']))
    failures=library.undefined_uses({'canonical-accounttimeline':opening+'\n'+closing},known)
    if failures:raise FlowFixError('\n'.join(failures))
    addition='\n'+r'\renewenvironment{accounttimeline}{'+opening+'}{'+closing+'}\n'
    return addition,[{'kind':'canonical-table-environment','environment':'accounttimeline','source_opening_sha256':_hash(opening),'source_closing_sha256':_hash(closing),'argument_count':0}]


def normative_environment_shim(selection,library):
    """Guard canonical environment-final ignorespaces before literal numbers.

The empty group has no visible content. Definitions and labels are derived
from canonical owners; the adapter never maintains a second wording.
"""
    source=library.strip_tex_comments(selection['head'])
    additions=[];records=[]
    for name,count in (('normtext',1),('workingrendering',0)):
        pattern=re.compile(r'\\(?:new|renew)environment\*?\s*\{\s*'+name+r'\s*\}')
        definitions=list(pattern.finditer(source))
        if not definitions:continue
        if len(definitions)!=1:raise FlowFixError('multiple canonical '+name+' definitions require reconciliation')
        match=definitions[0];cursor=library.skip_gap(source,match.end())
        observed=0
        if source[cursor:cursor+1]=='[':
            end=source.find(']',cursor)
            if end<0 or not source[cursor+1:end].strip().isdigit():raise FlowFixError('unsupported '+name+' signature')
            observed=int(source[cursor+1:end].strip());cursor=library.skip_gap(source,end+1)
        if observed!=count:raise FlowFixError('unsupported '+name+' signature')
        opening,cursor=library.brace_group(source,cursor);closing,cursor=library.brace_group(source,cursor)
        if r'\par' not in opening:raise FlowFixError(name+' no longer establishes the expected source paragraph')
        ending=re.search(r'\\ignorespaces\s*\Z',opening)
        if ending is None:
            if re.search(r'\\ignorespaces\{\}\s*\Z',opening):continue
            raise FlowFixError(name+' ending changed; explicit reconciliation required')
        guarded=opening[:ending.start()]+r'\ignorespaces{}'+opening[ending.end():]
        command='renewenvironment' if name in library.defined_names(library.SHIM.read_text()) else 'newenvironment'
        signature='['+str(count)+']' if count else ''
        additions.append('\n\\'+command+'{'+name+'}'+signature+'{'+guarded+'}{'+closing+'}\n')
        records.append({'kind':'canonical-environment-numeric-guard','environment':name,'source_opening_sha256':_hash(opening),'projected_opening_sha256':_hash(guarded),'source_closing_sha256':_hash(closing),'argument_count':count})
    return ''.join(additions),records


def inline_form_lines(body,selection,library):
    """Preserve the bounded two-label inline write-in form, not a rule-as-hr.

The independent inventory comes from the original selected source line before
conversion. Other rule uses retain their existing layout gates.
"""
    canonical=selection.get('canonical_body',selection['body'])
    pattern=re.compile(r'(?P<label1>[ \t]*[A-Za-z][A-Za-z \t]*:[ \t]*)\\rule\s*\{(?P<width1>[^{}]+)\}\s*\{(?P<height1>[^{}]+)\}(?P<gap>[ \t]*\\hfill[ \t]*)(?P<label2>[A-Za-z][A-Za-z \t]*:[ \t]*)\\rule\s*\{(?P<width2>[^{}]+)\}\s*\{(?P<height2>[^{}]+)\}[ \t]*\Z')
    widths={r'0.20\linewidth':'20',r'0.28\linewidth':'28'}
    rows=[];records=[];offset=0
    for line in canonical.splitlines(keepends=True):
        raw=line.rstrip('\r\n');match=pattern.fullmatch(library.mask_tex_comments(raw))
        if not match:offset+=len(line);continue
        uid='form-line-'+_hash(str(offset)+'\0'+raw)[:24]
        fields=[]
        for index in (1,2):
            width=match.group('width'+str(index)).strip();height=match.group('height'+str(index)).strip()
            if width not in widths or height!='0.4pt':raise FlowFixError('unsupported inline form field dimensions')
            fields.append({'id':uid+'-'+str(index),'row':uid,'role':'write-in-line','width':width,'thickness':height,'width_class':widths[width],'label':match.group('label'+str(index)).strip().removesuffix(':')})
        gap={'id':uid+'-gap','row':uid,'role':'fill-gap'}
        expected=[fields[0],gap,fields[1]]
        projected=match.group('label1')+r'\SemanticFillLine{'+fields[0]['id']+'} '+r'\SemanticFillLine{'+gap['id']+'} '+match.group('label2')+r'\SemanticFillLine{'+fields[1]['id']+'}'
        # Source line identity prevents a matching width elsewhere being selected.
        occurrences=[m.start() for m in re.finditer(re.escape(raw),body)]
        if len(occurrences)!=1:raise FlowFixError('canonical inline form row occurrence is ambiguous or changed')
        body=body[:occurrences[0]]+projected+body[occurrences[0]+len(raw):]
        rows.append({'id':uid,'fields':expected})
        source_ref={'coordinate_space':'canonical-selected-body','line':canonical[:offset].count('\n')+1}
        chunk_offset=0
        for chunk in selection.get('chunks',[]):
            if chunk_offset<=offset<chunk_offset+len(chunk['text']):
                source_ref={'path':chunk['path'],'occurrence':chunk['occurrence'],'selected_line':chunk['selected_line']+chunk['text'][:offset-chunk_offset].count('\n')};break
            chunk_offset+=len(chunk['text'])
        records.append({'kind':'typed-inline-write-in-form','source_offset':offset,'source_ref':source_ref,'source_sha256':_hash(raw),'source':raw,'fields':expected})
        offset+=len(line)
    if not rows:return body,'',[],[],[]
    if 'TRIPTYCHFILL' in canonical or r'\SemanticFillLine' in canonical:raise FlowFixError('reserved inline form marker occurs in canonical source')
    mapping={}
    for row in rows:
        for field in row['fields']:
            attrs={'class':'print-fill-gap' if field['role']=='fill-gap' else 'print-fill-line print-fill-line-'+field['width_class'],'data-print-type':field['role'],'data-semantic-form-line':field['id']}
            if field['role']=='write-in-line':attrs.update({'data-source-width':field['width'],'data-source-thickness':field['thickness']})
            mapping[field['id']]='<span '+' '.join(name+'="'+html.escape(value,quote=True).replace('\\','&#92;')+'"' for name,value in attrs.items())+'></span>'
    row_for={field['id']:row['id'] for row in rows for field in row['fields']}
    lua='local fields = {'+','.join('['+json.dumps(key)+']='+json.dumps(value) for key,value in mapping.items())+'}\n'
    lua+='local row_for = {'+','.join('['+json.dumps(key)+']='+json.dumps(value) for key,value in row_for.items())+'}\n'
    lua+='local rows = {'+','.join('['+json.dumps(row['id'])+']={'+','.join(json.dumps(field['id']) for field in row['fields'])+'}' for row in rows)+'}\n'
    lua+=r'''
local seen, row_seen = {}, {}
return {
  {Str=function(inline)
    local id=inline.text:match('^TRIPTYCHFILL([%w%-]+)ENDFILL$')
    if not id then
      if inline.text:find('TRIPTYCHFILL',1,true) then error('malformed inline form marker') end
      return nil
    end
    if not fields[id] then error('unbound inline form marker') end
    seen[id]=(seen[id] or 0)+1
    if seen[id]~=1 then error('duplicate inline form marker') end
    return pandoc.RawInline('html',fields[id])
  end},
  {Para=function(block)
    local found, owner = {}, nil
    block:walk({RawInline=function(inline)
      if inline.format~='html' then return nil end
      local id=inline.text:match('data%-semantic%-form%-line="([^"]+)"')
      if not id then return nil end
      if not row_for[id] then error('unbound inline form HTML') end
      if owner and owner~=row_for[id] then error('merged inline form rows') end
      owner=row_for[id];found[#found+1]=id
    end})
    if not owner then return nil end
    if #found~=#rows[owner] then error('split inline form paragraph') end
    for i,id in ipairs(rows[owner]) do
      if found[i]~=id then error('inline form fields changed order') end
    end
    row_seen[owner]=(row_seen[owner] or 0)+1
    local inside=pandoc.write(pandoc.Pandoc({block}),'html5',pandoc.WriterOptions{wrap_text='none'})
    inside=inside:gsub('^<p>','<p class="print-form-field-row">',1)
    return pandoc.RawBlock('html',inside)
  end},
  {Pandoc=function(document)
    for id,_ in pairs(fields) do if seen[id]~=1 then error('missing inline form field') end end
    for id,_ in pairs(rows) do if row_seen[id]~=1 then error('missing inline form paragraph') end end
  end},
}
'''
    return body,r'\newcommand{\SemanticFillLine}[1]{ TRIPTYCHFILL#1ENDFILL }'+'\n',[lua],records,rows


def check_form_lines(rows,fragment):
    """Independently require every source blank, dimension, order and row."""
    if not rows:return
    from html.parser import HTMLParser
    expected={field['id']:field for row in rows for field in row['fields']}
    class Audit(HTMLParser):
        def __init__(self):super().__init__();self.observed=[];self.row=0;self.active=None
        def handle_starttag(self,tag,attrs):
            values=dict(attrs)
            if tag=='p' and 'print-form-field-row' in values.get('class','').split():self.row+=1;self.active=self.row
            uid=values.get('data-semantic-form-line')
            if uid is None:return
            if tag!='span' or uid not in expected or self.active is None:raise FlowFixError('unbound or noninline source form field')
            field=expected[uid];classes=values.get('class','').split()
            if values.get('data-print-type')!=field['role']:raise FlowFixError('source form field role changed')
            if field['role']=='write-in-line':
                if set(classes)!={'print-fill-line','print-fill-line-'+field['width_class']} or values.get('data-source-width')!=field['width'] or values.get('data-source-thickness')!=field['thickness']:raise FlowFixError('source form field dimensions changed')
            elif classes!=['print-fill-gap']:raise FlowFixError('source form gap role changed')
            self.observed.append((uid,self.active))
        def handle_endtag(self,tag):
            if tag=='p':self.active=None
    audit=Audit();audit.feed(fragment)
    required=[field['id'] for row in rows for field in row['fields']]
    if [uid for uid,_ in audit.observed]!=required or audit.row!=len(rows):raise FlowFixError('source form fields missing, duplicated or reordered')
    for index,row in enumerate(rows,1):
        if any(number!=index for uid,number in audit.observed if uid in {field['id'] for field in row['fields']}):raise FlowFixError('source form fields no longer share their canonical paragraph')


def counter_display_projection(body,selection,ledger,library):
    """Replay only canonical macro paths containing executed counter reads.

The independent interpreter supplies actual call bytes, source programs,
arguments, nested offsets and raw counter values. The renderer never infers
letters from expected prose or assigns a manual publication sequence.
"""
    events=ledger.get('counter_displays',[])
    if not events:return body,[]
    canonical=selection.get('canonical_body',selection['body'])
    digest=selection.get('selection',{}).get('selection_digest')
    if digest!=ledger.get('selection_digest'):raise FlowFixError('counter events belong to another source selection')
    roots={};all_ids=set()
    def node(frame):
        program=frame.get('expanded_program');definition=frame.get('definition');args=frame.get('arguments')
        if not isinstance(program,str) or not isinstance(definition,str) or not isinstance(args,list):raise FlowFixError('counter frame lacks its canonical program')
        if _hash(program)!=frame.get('expanded_program_sha256') or _hash(definition)!=frame.get('definition_digest'):raise FlowFixError('counter frame program hash mismatch')
        if [_hash(arg) for arg in args]!=frame.get('argument_digests'):raise FlowFixError('counter frame argument hash mismatch')
        pieces=[]
        for token in re.findall(r'\\[A-Za-z@]+|\\.|##|#[1-9]|[^\\#]+|#',definition,re.S):
            if token=='##':part='#'
            elif re.fullmatch(r'#[1-9]',token):
                index=int(token[1])-1
                if index>=len(args):raise FlowFixError('unbound counter frame parameter')
                part=args[index]
            else:part=token
            if pieces and re.search(r'\\[A-Za-z@]+$',pieces[-1]) and re.match(r'[A-Za-z@]',part):pieces.append('{}')
            pieces.append(part)
        if ''.join(pieces)!=program:raise FlowFixError('counter frame argument replay mismatch')
        return {'program':program,'children':{},'reads':{}}
    for event in events:
        event_id=event.get('id')
        if not event_id or event_id in all_ids:raise FlowFixError('duplicate/unbound counter event identity')
        all_ids.add(event_id)
        start,end=event.get('source_offset'),event.get('source_end');call=event.get('source_call')
        if not isinstance(start,int) or not isinstance(end,int) or not 0<=start<end<=len(canonical) or canonical[start:end]!=call or _hash(call)!=event.get('source_tex_sha256'):
            raise FlowFixError('counter event canonical source call mismatch')
        value=event.get('rawdisplay')
        if not isinstance(value,str) or not re.fullmatch(r'(?:[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)*)?',value):raise FlowFixError('unsupported literal counter display')
        if event.get('selection_digest')!=digest:raise FlowFixError('counter event selection digest mismatch')
        key=(start,end);trace=event.get('expansion',[])
        if key not in roots:roots[key]={'call':call,'events':[],'node':None,'direct':None}
        root=roots[key];root['events'].append(event)
        if not trace:
            if root['node'] is not None or root['direct'] not in (None,value):raise FlowFixError('conflicting direct counter reads')
            root['direct']=value;continue
        owner=next((i for i,frame in enumerate(trace) if frame.get('source_offset') is not None),None)
        if owner is None:raise FlowFixError('counter expansion lacks a source-bound root')
        trace=trace[owner:]
        first=trace[0]
        if first.get('source_offset')!=start or first.get('source_end')!=end or first.get('source_call')!=call:raise FlowFixError('counter expansion root span mismatch')
        if root['node'] is None:root['node']=node(first)
        current=root['node']
        for frame in trace[1:]:
            a,b=frame.get('program_offset'),frame.get('program_end')
            if not isinstance(a,int) or not isinstance(b,int) or not 0<=a<b<=len(current['program']):raise FlowFixError('counter child span is not bound to its parent program')
            key2=(a,b)
            if key2 not in current['children']:current['children'][key2]=node(frame)
            child=current['children'][key2]
            if child['program']!=frame['expanded_program']:raise FlowFixError('conflicting counter expansion programs')
            current=child
        a,b=event.get('program_offset'),event.get('program_end')
        if not isinstance(a,int) or not isinstance(b,int) or not 0<=a<b<=len(current['program']):raise FlowFixError('counter read span is not bound to its canonical program')
        token=current['program'][a:b]
        if not re.fullmatch(r'\\(?:the[A-Za-z@]+|arabic|alph|Alph|roman|Roman)(?:\s*\{[^{}]+\})?\s*',token):raise FlowFixError('counter read is not a recognized source token')
        if (a,b) in current['reads'] and current['reads'][(a,b)]!=value:raise FlowFixError('one source counter read has conflicting values')
        current['reads'][(a,b)]=value
    def replay(current):
        replacements=[(a,b,value) for (a,b),value in current['reads'].items()]
        replacements.extend((a,b,replay(child)) for (a,b),child in current['children'].items())
        replacements.sort()
        previous=0;pieces=[]
        for a,b,value in replacements:
            if a<previous:raise FlowFixError('overlapping counter expansion/read spans')
            pieces.extend((current['program'][previous:a],value));previous=b
        pieces.append(current['program'][previous:]);return ''.join(pieces)
    definition_spans=[(definition.start,definition.end) for kind,definition in library.walk_definitions(library.mask_tex_comments(body)) if kind=='definition']
    by_call={}
    for span,root in sorted(roots.items()):by_call.setdefault(root['call'],[]).append((span,root))
    replacements=[];records=[]
    for call,items in by_call.items():
        observed=[];cursor=0
        while True:
            start=body.find(call,cursor)
            if start<0:break
            end=start+len(call);cursor=end
            if any(a<=start<b for a,b in definition_spans):continue
            if call[-1:].isalpha() and body[end:end+1].isalpha():continue
            observed.append((start,end))
        if len(observed)!=len(items):raise FlowFixError('canonical counter call occurrence mismatch after upstream source projections')
        for (a,b),((source_start,source_end),root) in zip(observed,items):
            rendered=replay(root['node']) if root['node'] is not None else root['direct']
            replacements.append((a,b,rendered))
            records.append({'kind':'canonical-executed-counter-display','source_offset':source_start,'source_end':source_end,'source_call_sha256':_hash(call),'projected_source_sha256':_hash(rendered),'event_ids':[event['id'] for event in root['events']],'displays':[{'name':event['name'],'counter':event['counter'],'format':event['format'],'rawdisplay':event['rawdisplay']} for event in root['events']]})
    replacements.sort();pieces=[];cursor=0
    for a,b,value in replacements:
        if a<cursor:raise FlowFixError('overlapping selected source counter calls')
        pieces.extend((body[cursor:a],value));cursor=b
    pieces.append(body[cursor:]);return ''.join(pieces),records

def canonical_content_macros(selection,library):
    """Restore selected source macro semantics where the reader shim differs.

Every program is taken from the selected canonical definition. Only explicit
layout controls that Pandoc swallows with a following group are removed from
the group label; text, fields and paragraph boundaries remain untouched.
"""
    canonical,_=library.command_definitions(library.strip_tex_comments(selection['head']))
    base,_=library.command_definitions(library.SHIM.read_text())
    additions=[];records=[]
    for name,count in (('virtuegrouplabel',1),('sacramentSummaryStart',3),('sacramentSummaryEnd',0)):
        if name not in canonical:continue
        arity,default,program=canonical[name]
        if arity!=count or default is not None:raise FlowFixError('unsupported canonical '+name+' signature')
        projected=program
        if name=='virtuegrouplabel':
            if program.count('#1')!=1:raise FlowFixError('virtuegrouplabel field mapping changed')
            projected=re.sub(r'\\(?:medskip|smallskip|noindent)(?![A-Za-z@])',' ',program)
        command='renewcommand' if name in base else 'newcommand'
        additions.append('\n\\'+command+'{\\'+name+'}'+('['+str(count)+']' if count else '')+'{'+projected+'}\n')
        records.append({'kind':'canonical-content-macro','macro':name,'argument_count':count,'source_definition_sha256':_hash(program),'projected_definition_sha256':_hash(projected)})
    # A source providecommand must not be defeated by an unrelated shim name.
    # This bounded current-corpus conflict is a two-cell row, not a term style.
    body=selection.get('canonical_body',selection['body'])
    defs=[d for kind,d in library.walk_definitions(library.mask_tex_comments(body)) if kind=='definition' and d.name=='term']
    if defs and 'term' in base and 'term' not in canonical:
        if len(defs)!=1:raise FlowFixError('multiple body term definitions require a scoped adapter')
        definition=defs[0];macro=definition.macro
        if definition.command!='providecommand' or macro is None or macro[:2]!=(2,None):raise FlowFixError('unsupported source/shim term conflict')
        if re.search(r'\\term(?![A-Za-z@])',library.mask_tex_comments(body[:definition.start])):raise FlowFixError('source term uses precede its canonical row definition')
        program=macro[2]
        if program.count('#1')!=1 or program.count('#2')!=1 or '&' not in program or r'\\' not in program:raise FlowFixError('canonical term row program changed')
        spacing=re.search(r'\\addlinespace\s*\[([^\]]+)\]\s*\Z',program)
        projected=program
        if spacing:
            if not _DIMENSION.fullmatch(spacing.group(1).strip()):raise FlowFixError('unsupported canonical row spacing')
            projected=program[:spacing.start()]
        additions.append('\n'+r'\renewcommand{\term}[2]{'+projected+'}\n')
        records.append({'kind':'canonical-signature-conflict','macro':'term','shim_argument_count':base['term'][0],'canonical_argument_count':2,'source_definition_sha256':_hash(program),'projected_definition_sha256':_hash(projected),'source_offset':definition.start})
    return ''.join(additions),records


def minipage_lua_filter(containers,note_bindings=None):
    """Preserve each complete Pandoc minipage as a source-bound typed block.

IDs are assigned top-down before block conversion. Local notes require an
independent canonical binding, and the owning audit counts their exact IDs.
"""
    for i,record in enumerate(containers,1):
        if record.get('id')!='minipage-'+str(i) or not record.get('source_ref'):
            raise FlowFixError('unbound canonical minipage expectation')
    note_bindings={} if note_bindings is None else note_bindings
    for key,ids in note_bindings.items():
        if key not in {c['id'] for c in containers} or any(not re.fullmatch(r'unit-\d{6}',value) for value in ids):
            raise FlowFixError('unbound canonical minipage note expectation')
    lua_bindings='{'+','.join('['+json.dumps(key)+']={'+','.join(json.dumps(value) for value in ids)+'}' for key,ids in note_bindings.items())+'}'
    return r'''
local count = 0
local expected = @EXPECTED@
local note_bindings = @NOTE_BINDINGS@
local function minipage(block)
  return block.classes:includes('minipage')
end
return {
  {
    traverse = 'topdown',
    Div = function(block)
      if not minipage(block) then return nil end
      count = count + 1
      block.attributes['data-print-unit'] = 'minipage-' .. count
      return block
    end,
  },
  {
    Div = function(block)
      if not minipage(block) then return nil end
      local notes = 0
      block:walk({Note = function() notes = notes + 1 end})
      local key = block.attributes['data-print-unit']
      local bindings = note_bindings[key] or {}
      if notes ~= #bindings then error('minipage notes require the owning raw-HTML note audit: canonical note count mismatch') end
      local inside = pandoc.write(pandoc.Pandoc(block.content), 'html5',
        pandoc.WriterOptions{identifier_prefix=key .. '-', wrap_text='none'})
      if notes > 0 then
        inside = inside:gsub('class="footnotes footnotes%-end%-of%-document"', 'class="footnote print-local-notes"')
        inside = inside:gsub('class="footnote%-back"', 'class="footnote-backref"')
        local observed = 0
        local escaped_key = key:gsub('([^%w])', '%%%1')
        inside = inside:gsub('(<li id="' .. escaped_key .. '%-fn(%d+)")', function(opening, index)
          local binding = bindings[tonumber(index)]
          if not binding then error('unexpected minipage note identity') end
          observed = observed + 1
          return opening .. ' data-semantic-note="' .. binding .. '"'
        end)
        if observed ~= #bindings then error('minipage HTML note binding shortfall') end
      end
      return pandoc.RawBlock('html', '<section class="print-flow-block" data-print-type="minipage" data-print-unit="' .. key .. '" data-semantic-minipage="' .. key .. '">\n' .. inside .. '</section>')
    end,
  },
  {
    -- Python Markdown cannot nest a raw HTML block inside its Markdown
    -- blockquote/list writer without manufacturing an invalid p wrapper.
    -- Preserve the enclosing original AST container as semantic HTML too.
    -- This changes no text, list item, quotation, or table structure.
    BlockQuote = function(block)
      local found = false
      block:walk({RawBlock = function(raw)
        if raw.format == 'html' and raw.text:find('data%-semantic%-minipage=') then found = true end
      end})
      if not found then return nil end
      local notes = 0
      block:walk({Note = function() notes = notes + 1 end})
      if notes ~= 0 then error('minipage enclosing block notes require the owning raw-HTML note audit') end
      return pandoc.RawBlock('html', pandoc.write(pandoc.Pandoc({block}), 'html5',
        pandoc.WriterOptions{wrap_text='none'}))
    end,
    BulletList = function(block)
      local found = false
      block:walk({RawBlock = function(raw)
        if raw.format == 'html' and raw.text:find('data%-semantic%-minipage=') then found = true end
      end})
      if not found then return nil end
      return pandoc.RawBlock('html', pandoc.write(pandoc.Pandoc({block}), 'html5',
        pandoc.WriterOptions{wrap_text='none'}))
    end,
    OrderedList = function(block)
      local found = false
      block:walk({RawBlock = function(raw)
        if raw.format == 'html' and raw.text:find('data%-semantic%-minipage=') then found = true end
      end})
      if not found then return nil end
      return pandoc.RawBlock('html', pandoc.write(pandoc.Pandoc({block}), 'html5',
        pandoc.WriterOptions{wrap_text='none'}))
    end,
    DefinitionList = function(block)
      local found = false
      block:walk({RawBlock = function(raw)
        if raw.format == 'html' and raw.text:find('data%-semantic%-minipage=') then found = true end
      end})
      if not found then return nil end
      return pandoc.RawBlock('html', pandoc.write(pandoc.Pandoc({block}), 'html5',
        pandoc.WriterOptions{wrap_text='none'}))
    end,
    Table = function(block)
      local found = false
      block:walk({RawBlock = function(raw)
        if raw.format == 'html' and raw.text:find('data%-semantic%-minipage=') then found = true end
      end})
      if not found then return nil end
      return pandoc.RawBlock('html', pandoc.write(pandoc.Pandoc({block}), 'html5',
        pandoc.WriterOptions{wrap_text='none'}))
    end,
  },
  {
    Pandoc = function(document)
      document:walk({Div = function(block)
        error('unsupported remaining flow Div: ' .. table.concat(block.classes, ','))
      end})
      if count ~= expected then
        error('canonical minipage count mismatch: expected ' .. expected .. ', observed ' .. count)
      end
      io.stderr:write('triptych-minipages: ' .. count .. '\n')
    end,
  },
}
'''.replace('@EXPECTED@',str(len(containers))).replace('@NOTE_BINDINGS@',lua_bindings)


def prepare(selection,library,expected_ledger=None):
    """Return a prepared copy; preserve canonical body/chunks for the independent ledger."""
    result=copy.copy(selection);body=selection['body'];head=selection['head'];projections=list(selection.get('projections',[]))
    if expected_ledger is None:
        from _web_print_semantics import expected_units
        expected_ledger=expected_units(selection,library)
    body,form_shim,form_filters,records,form_rows=inline_form_lines(body,selection,library);projections.extend(records)
    body,records=counter_display_projection(body,selection,expected_ledger,library);projections.extend(records)
    body,records=preserve_glyph_aliases(body,selection['head'],library);projections.extend(records)
    for function in (drop_length_assignments,preserve_aleph,drop_longtable_footers):
        body,records=function(body,library) if function is not preserve_aleph else function(body)
        projections.extend(records)
    head,records=preserve_known_separator(head,selection['head'],library,'head');projections.extend(records)
    body,records=preserve_known_separator(body,selection['head'],library,'body');projections.extend(records)
    head,records=guard_literal_brackets(head,library,'head');projections.extend(records)
    body,records=guard_literal_brackets(body,library,'body');projections.extend(records)
    addition,records=prayer_shim(selection,library);projections.extend(records)
    table_addition,records=table_environment_shim(selection,library);projections.extend(records)
    normative_addition,records=normative_environment_shim(selection,library);projections.extend(records)
    content_addition,records=canonical_content_macros(selection,library);projections.extend(records)
    addition=selection.get('shim_additions','')+addition+table_addition+normative_addition+content_addition+form_shim
    addition,records=preserve_known_separator(addition,selection['head'],library,'derived-shim');projections.extend(records)
    addition,records=guard_literal_brackets(addition,library,'derived-shim');projections.extend(records)
    if expected_ledger is None:
        from _web_print_semantics import expected_units
        expected_ledger=expected_units(selection,library)
    containers=expected_ledger.get('containers',[])
    bindings={container['id']:[] for container in containers}
    for index,unit in enumerate(expected_ledger.get('units',[])):
        if unit.get('lane')!='notes':continue
        owners=[c for c in containers if c.get('unit_start',0)<=index<c.get('unit_end',0)]
        if owners:
            owner=min(owners,key=lambda c:c['unit_end']-c['unit_start'])
            bindings[owner['id']].append(unit['id'])
    filters=list(selection.get('lua_filters',[]))+form_filters+([minipage_lua_filter(containers,bindings)] if containers else [])
    projections.extend({'kind':'typed-flow-block',**container} for container in containers)
    audit_source=selection.get('audit_body',selection.get('canonical_body',selection['body']))
    result.update(head=head,body=body,source=head+r'\begin{document}'+body+r'\end{document}',canonical_body=selection.get('canonical_body',selection['body']),audit_body=drop_longtable_footers(audit_source,library)[0],projections=projections,shim_additions=addition,lua_filters=filters,expected_containers=containers,expected_form_lines=form_rows,raw_html_notes=[value for ids in bindings.values() for value in ids],source_openings=canonical_openings(expected_ledger,library))
    return result


def prepare_markdown(markdown,selection,library):
    """Project literal Markdown glyphs and source-bound URNs for the site parser.

Empty span formatting is removed only from already-empty padding cells.
No words, notes, links, or cell content are omitted or synthesized.
"""
    body=selection.get('canonical_body',selection['body']);records=[]
    check_form_lines(selection.get('expected_form_lines',[]),markdown)
    count=markdown.count(r'\<')
    if count:
        markdown=markdown.replace(r'\<','&lt;')
        records.append({'kind':'markdown-literal-angle-entity','count':count})
    source=selection.get('head','')+'\n'+body
    urns=set()
    for match in re.finditer(r'\\url(?![A-Za-z@])',library.mask_tex_comments(source)):
        value,_=library.brace_group(source,match.end())
        if value.startswith('urn:') and not re.search(r'[\s<>"\\]',value):urns.add(value)
    for uri in sorted(urns):
        pattern='<'+uri+'>';count=markdown.count(pattern)
        if count:
            markdown=markdown.replace(pattern,'<a href="'+html.escape(uri,quote=True)+'">'+html.escape(uri)+'</a>')
            records.append({'kind':'canonical-urn-link','target':uri,'occurrences':count})
    if re.search(r'\\multicolumn\s*\{\s*[2-9]\d*\s*\}',body):
        pattern=re.compile(r'(?P<opening><(?P<cell>t[dh])\b[^>]*>)\s*(?:<(?P<face>strong|em)>\s*</(?P=face)>\s*)+(?P<ending></(?P=cell)>)')
        markdown,count=pattern.subn(lambda match:match.group('opening')+match.group('ending'),markdown)
        if count:records.append({'kind':'empty-span-padding-format','cells':count})
    return markdown,records
