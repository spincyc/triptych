"""Shared source-bound browser print normalization, measurements and transport.

These helpers measure source-owned parts and validate an existing independent
coverage proof. They never grant editorial approval or manufacture coverage PASS.
Normalize source styles first, project final route hrefs, then compute part pins.
"""
from __future__ import annotations

from collections import Counter
import copy
from decimal import Decimal
import hashlib
import html
from html.parser import HTMLParser
import json
import re


class PrintError(ValueError):
    """A source print product is incomplete, unsupported or inconsistent."""


VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class StructureError(PrintError):pass

class Events(HTMLParser):
    def __init__(self, fragment, part_id=None):
        super().__init__(convert_charrefs=True)
        self.part_id=part_id
        self.events=[];self.stack=[];self.roots=0;self.active=False
        if '\0' in fragment:raise StructureError('NUL is not valid source markup')
        self.feed(fragment.replace('\r\n','\n').replace('\r','\n'))
        self.close()
        if self.stack or self.roots!=1:raise StructureError('part structure is unclosed, missing or ambiguous')

    def handle_starttag(self, tag, attrs):
        if not self.active:
            if self.part_id is not None and dict(attrs).get('data-print-part')!=self.part_id:return
            self.roots+=1
            if self.roots!=1:raise StructureError('multiple selected part roots')
            self.active=True
        elif any(name=='data-print-part' for name,_ in attrs):
            raise StructureError('nested print parts')
        names=[name for name,_ in attrs]
        if len(names)!=len(set(names)):raise StructureError('duplicate source attribute')
        if any(not name.isascii() for name in names):raise StructureError('non-ASCII attribute name')
        attrs=[[name,value if value is not None else ''] for name,value in attrs if not (tag=='details' and name=='open')]
        self.events.append(['start',tag,sorted(attrs,key=lambda pair:pair[0])])
        self.stack.append(tag)
        if tag in VOID:self.handle_endtag(tag)

    def handle_startendtag(self, tag, attrs):
        if not self.active and self.part_id is not None and dict(attrs).get('data-print-part')!=self.part_id:return
        foreign=tag=='math' or 'math' in self.stack
        if tag not in VOID and not foreign:raise StructureError('self-closing nonvoid HTML changes the native tree')
        self.handle_starttag(tag,attrs)
        if tag not in VOID:self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if not self.active:
            if self.part_id is None:raise StructureError('closing element outside the selected part')
            return
        if not self.stack or self.stack[-1]!=tag:raise StructureError('unbalanced source element')
        self.events.append(['end',tag]);self.stack.pop()
        if not self.stack:self.active=False

    def handle_data(self, value):
        if not self.active and self.part_id is None and value.strip():raise StructureError('content outside the selected part')

def structure_events(fragment, part_id=None):
    return Events(fragment,part_id).events

def structure_sha256(fragment, part_id=None):
    data=json.dumps(structure_events(fragment,part_id),ensure_ascii=False,separators=(',',':'))
    return hashlib.sha256(data.encode()).hexdigest()

def canonical_json(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':'))

def inventory(values):
    if not isinstance(values,list) or not all(isinstance(value,str) for value in values):
        raise ValueError('inventory must be an ordered string array')
    if len(set(values))!=len(values):
        raise ValueError('canonical inventory contains duplicate identities')
    return {'count':len(values),'sha256':hashlib.sha256(canonical_json(values).encode()).hexdigest()}

def compact_descriptor(descriptor, *, audit_sha256=None):
    """Return public shape only after checking the full independent owner proof.

    Caller persists the original complete ledger and coverage checks in ignored
    build audit. This is transport compaction, not generation of source proof.
    """
    # The independent ledger can exceed 100 MB. Borrow it read-only; copying it
    # before projecting would defeat the bounded public transport's memory use.
    d=descriptor
    proof=d['coverage_result']
    expected=d['expected_units']
    if (proof.get('status')!='pass' or proof.get('output_id')!=d['id'] or
        proof.get('source_digest')!=d['source_digest'] or proof.get('selection_digest')!=d['selection_digest'] or
        proof.get('expected_units')!=expected):
        raise ValueError('independent exact-output source coverage has not passed')
    units=[unit['id'] for unit in expected]
    if not units or not all(unit.get('source') and unit.get('occurrence') for unit in expected):
        raise ValueError('canonical source units are incomplete')
    if [unit for part in d['parts'] for unit in part['units']]!=units:
        raise ValueError('parts differ from independent ordered source selection')
    public_keys={'schema','id','title','edition','revision','language','print_type','page_format','availability',
                 'source_digest','selection_digest','style_sha256'}
    public={key:copy.deepcopy(value) for key,value in d.items() if key in public_keys}
    public['unit_inventory']=inventory(units)
    public['coverage_result']={key:proof[key] for key in ['status','output_id','source_digest','selection_digest']}
    public['coverage_result']['unit_inventory']=copy.deepcopy(public['unit_inventory'])
    digest=audit_sha256 or proof.get('audit_sha256')
    if digest:
        if len(digest)!=64 or any(char not in '0123456789abcdef' for char in digest):
            raise ValueError('audit identity is invalid')
        public['coverage_result']['audit_sha256']=digest
    public['parts']=[]
    for part in d['parts']:
        if not isinstance(part.get('structure_sha256'),str) or len(part['structure_sha256'])!=64:
            raise ValueError('part structure must be pinned after typed normalization and routing')
        item={key:copy.deepcopy(value) for key,value in part.items() if key in {'id','href','selector','text_sha256','structure_sha256','counts'}}
        item['expected_ids']=inventory(part['expected_ids'])
        item['units']=inventory(part['units'])
        public['parts'].append(item)
    public['assets']=[{key:value for key,value in asset.items() if key in {'id','href','sha256','mime','role'}} for asset in d.get('assets',[])]
    public['fonts']=[{key:value for key,value in font.items() if key in {'family','href','sha256','weight','style','unicode_range'}} for font in d.get('fonts',[])]
    return public


def sha256(value):
    """Return the SHA256 of UTF8 text or the provided exact bytes."""
    return hashlib.sha256(value.encode() if isinstance(value,str) else value).hexdigest()


def normalize_text(value):
    r"""Match JavaScript /\s+/gu normalization exactly, including source FEFF."""
    return re.sub(r"[\t\n\v\f\r \u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff]+"," ",value).strip(" ")


class _Statistics(Events):
    def __init__(self,fragment,part_id=None):
        self.text=[]
        super().__init__(fragment,part_id)
    def handle_data(self,value):
        if self.active:self.text.append(value)
        else:super().handle_data(value)


def part_statistics(fragment,part_id=None,selectors=None):
    """Measure one strict source part without repairing its HTML tree.

    IDs exclude the part root; units include it. Both retain exact DOM preorder.
    Counts concern descendants only and can be narrowed to supplied selectors.
    These measurements are not an independent canonical-source coverage proof.
    """
    parsed=_Statistics(fragment,part_id)
    nodes=[(event[1],dict(event[2])) for event in parsed.events if event[0]=='start']
    descendants=nodes[1:]
    ids=[attrs['id'] for _,attrs in descendants if attrs.get('id')]
    units=[attrs['data-print-unit'] for _,attrs in nodes if 'data-print-unit' in attrs]
    if len(set(ids))!=len(ids) or len(set(units))!=len(units):
        raise PrintError('part repeats a semantic identity or source unit')
    measured=Counter(tag for tag,_ in descendants)
    measured.update('.'+name for _,attrs in descendants for name in set(attrs.get('class','').split()))
    if selectors is None:
        counts=dict(sorted(measured.items()))
    else:
        counts={}
        for selector in selectors:
            if not re.fullmatch(r'(?:[a-z][a-z0-9-]*|\.[a-z][a-z0-9-]*|\[data-print-[a-z-]+\])',selector):
                raise PrintError('unsupported semantic count selector')
            if selector.startswith('[data-print-'):
                key=selector[1:-1];counts[selector]=sum(key in attrs for _,attrs in descendants)
            else:counts[selector]=measured.get(selector,0)
    return {'text_sha256':sha256(normalize_text(''.join(parsed.text))),
            'structure_sha256':structure_sha256(fragment,part_id),
            'expected_ids':ids,'units':units,'counts':counts}


class ProfileError(PrintError):
    """Source formatting is outside the finite reviewed print vocabulary."""


HEIGHTS={Decimal('0.65'):'065',Decimal('0.8'):'080',Decimal('0.9'):'090',Decimal('1.0'):'100',Decimal('1.1'):'110',Decimal('1.2'):'120',Decimal('1.3'):'130',Decimal('1.4'):'140'}
TABLE_WIDTHS=frozenset({83,85,87,92,93,95,96})
COLUMN_WIDTHS=frozenset({7,8,9,10,11,12,13,14,15,17,18,19,20,21,25,26,27,31,34})
_SERVER_CLASSES=frozenset('action branch continuation diagram guide-part minipage paired-lanes response scene titlepage trainer-layout trainer-rail center description role smallcaps uri samepage unnumbered align-left sheet low sung grid face blank answer apparatus face-header sheet-notice sheet-duplex action-body dense face-footer field field-label learner meaning sound source-size-6 source-size-8 source-size-9 source-size-10 source-size-11 small tiny'.split())


def _attribute_spans(raw):
    """Locate real source attributes without matching text inside quoted values."""
    tag=re.match(r'<\s*[^\s/>]+',raw)
    if tag is None:raise ProfileError('malformed source start tag')
    pos=tag.end();result=[]
    while pos<len(raw):
        begin=pos
        while pos<len(raw) and raw[pos].isspace():pos+=1
        if raw[pos:] in {'>','/>'}:return result
        name=re.match(r'[^\s/>=]+',raw[pos:])
        if name is None:raise ProfileError('malformed source attribute')
        key=name.group().lower();pos+=len(name.group());name_end=pos
        while pos<len(raw) and raw[pos].isspace():pos+=1
        if pos<len(raw) and raw[pos]=='=':
            pos+=1
            while pos<len(raw) and raw[pos].isspace():pos+=1
            if pos>=len(raw):raise ProfileError('source attribute has no value')
            quote=raw[pos]
            if quote in {'"',"'"}:
                pos+=1;end=raw.find(quote,pos)
                if end<0:raise ProfileError('unclosed source attribute')
                pos=end+1
            else:
                value=re.match(r'[^\s>]+',raw[pos:])
                if value is None:raise ProfileError('source attribute has no value')
                pos+=len(value.group())
        else:pos=name_end
        result.append((key,begin,pos))
    raise ProfileError('unclosed source start tag')


def _rewrite_attributes(raw,attrs,replacements,removals):
    spans=_attribute_spans(raw)
    if [name for name,_,_ in spans]!=[name for name,_ in attrs]:
        raise ProfileError('ambiguous source attribute syntax')
    pieces=[];cursor=0;used=set()
    for name,begin,end in spans:
        pieces.append(raw[cursor:begin]);cursor=end
        if name in removals:continue
        if name in replacements:
            pieces.append(' '+name+'="'+html.escape(replacements[name],quote=True)+'"');used.add(name)
        else:pieces.append(raw[begin:end])
    tail=raw[cursor:]
    additions=''.join(' '+name+'="'+html.escape(value,quote=True)+'"' for name,value in replacements.items() if name not in used and name not in removals)
    if additions:
        marker='/>' if tail.endswith('/>') else '>'
        tail=tail[:-len(marker)]+additions+marker
    return ''.join(pieces)+tail


class _Normalize(HTMLParser):
    def __init__(self,profile):
        super().__init__(convert_charrefs=False)
        self.profile=profile;self.output=[];self.projections=[];self.stack=[]

    def start(self,tag,attrs):
        names=[key for key,_ in attrs]
        if len(names)!=len(set(names)):raise ProfileError('duplicate source attribute')
        values=dict(attrs);classes=values.get('class','').split();extra=[]
        replacements={};removals=set();style=values.get('style')
        if 'style' in values:
            if style is None:raise ProfileError('empty source style')
            style=style.strip()
            alignment=re.fullmatch(r'text-align:\s*(left|center|right)\s*;?',style)
            width=re.fullmatch(r'width:\s*([0-9]+)%\s*;?',style)
            height=re.fullmatch(r'min-height:\s*([0-9]+(?:\.[0-9]+)?)in\s*;?',style)
            if width and tag=='table' and int(width[1]) in TABLE_WIDTHS:extra=['print-table-width-'+str(int(width[1]))]
            elif width and tag=='col' and int(width[1]) in COLUMN_WIDTHS:extra=['print-column-width-'+str(int(width[1]))]
            elif alignment and tag in {'td','th'}:extra=['print-align-'+alignment[1]]
            elif re.fullmatch(r'margin:\s*0\s*;?',style) and tag=='p' and 'poetry-verse-line' in classes:pass
            elif height and tag in {'span','div'} and 'response-space' in classes:
                key=Decimal(height[1])
                if key not in HEIGHTS:raise ProfileError('undeclared response-space height')
                extra=['response-space-'+HEIGHTS[key]]
            elif self.profile in {'server-guide','server-cards'} and tag=='div' and classes==['grid'] and style in {'--rows:3','--rows:4'}:pass
            else:raise ProfileError('untyped source print style on '+tag+': '+style)
            removals.add('style');self.projections.append({'tag':tag,'style':style,'typed_classes':extra})
        if tag=='details' and 'open' in values:
            removals.add('open');self.projections.append({'tag':tag,'state':'open','normalization':'print-all-content'})
        if self.profile in {'server-guide','server-cards'}:
            mapped=[]
            for name in classes:
                if name in {'print-align-left','print-align-center','print-align-right'} or name in {'print-table-width-'+str(n) for n in TABLE_WIDTHS} or name in {'print-column-width-'+str(n) for n in COLUMN_WIDTHS}:
                    mapped.append(name);continue
                plain=name.removeprefix('server-')
                if plain not in _SERVER_CLASSES:raise ProfileError('untyped server source class '+name)
                mapped.append('server-'+plain)
            classes=mapped
            if 'data-unit-id' in values:
                unit=values['data-unit-id']
                if not unit or ('data-print-unit' in values and values['data-print-unit']!=unit):raise ProfileError('ambiguous source unit identity')
                replacements['data-print-unit']=unit;removals.add('data-unit-id')
                if 'id' not in values:replacements['id']=unit
            if 'aria-hidden' in values:
                if tag!='div' or classes!=['server-face','server-blank'] or values['aria-hidden']!='true':raise ProfileError('hidden semantic server source')
                removals.add('aria-hidden')
            if tag=='img' and 'data-print-asset' not in values:
                asset=next((parent.get('data-diagram-id') for name,parent in reversed(self.stack) if name=='figure' and parent.get('data-diagram-id')),None)
                if asset:replacements['data-print-asset']=asset
        if tag=='img' and values.get('data-source-asset'):
            asset=values['data-source-asset']
            if values.get('data-print-asset',asset)!=asset:raise ProfileError('ambiguous source illustration identity')
            replacements['data-print-asset']=asset
        for name in extra:
            if name not in classes:classes.append(name)
        if classes!=values.get('class','').split():replacements['class']=' '.join(classes)
        raw=self.get_starttag_text()
        self.output.append(_rewrite_attributes(raw,attrs,replacements,removals) if replacements or removals else raw)
        if tag not in VOID:self.stack.append((tag,values))

    def handle_starttag(self,tag,attrs):self.start(tag,attrs)
    def handle_startendtag(self,tag,attrs):
        self.start(tag,attrs)
        if tag not in VOID:self.stack.pop()
    def handle_endtag(self,tag):
        self.output.append('</'+tag+'>')
        if self.stack and self.stack[-1][0]==tag:self.stack.pop()
    def handle_data(self,value):self.output.append(value)
    def handle_entityref(self,value):self.output.append('&'+value+';')
    def handle_charref(self,value):self.output.append('&#'+value+';')
    def handle_comment(self,value):self.output.append('<!--'+value+'-->')
    def handle_decl(self,value):raise ProfileError('unexpected declaration in a source part')
    def handle_pi(self,value):raise ProfileError('unexpected processing instruction in a source part')


def normalize_html_with_projections(fragment,profile='flow'):
    """Return typed source HTML and its finite presentation projection audit."""
    parser=_Normalize(profile);parser.feed(fragment);parser.close()
    return ''.join(parser.output),parser.projections


def normalize_html(fragment,profile='flow'):
    """Normalize only finite source styles and print-neutral details fold state.

    Does not select content, rewrite links, infer canonical units or grant PASS.
    Structural measurement afterwards deliberately refuses native-tree repairs.
    """
    return normalize_html_with_projections(fragment,profile)[0]
