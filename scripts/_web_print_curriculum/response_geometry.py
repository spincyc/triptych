"""Finite, source-owned writing-room contracts, separate from prose coverage."""
from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
import hashlib
import html
import json
import re

HEIGHTS = {'0.22in':'022','0.38in':'038','0.65in':'065','0.7in':'070','0.8in':'080',
           '0.9in':'090','1.0in':'100','1.1in':'110','1.15in':'115','1.2in':'120','1.3in':'130','1.4in':'140'}
STRUTS = {'0.5in':'050','0.52in':'052','0.55in':'055','0.62in':'062','0.65in':'065',
          '0.72in':'072','0.76in':'076','0.78in':'078','0.82in':'082'}
FIELDS = ('kind','origin','height','width','lines','rule','macro')


class GeometryError(ValueError):pass


def signature(origin, height=None):
    """Renderer contract; the independent walker supplies separate expectations."""
    if origin in {'Blank','LongBlank'}:
        width='1.3in' if origin=='Blank' else '2.6in'
        return dict(kind='inline-rule',origin=origin,height='0.4pt',width=width,lines=1,rule='0.4pt',macro=origin)
    if origin=='memory@blankcell':
        return dict(kind='blank-cell',origin=origin,height=r'2.2\baselineskip',width='linewidth',lines=1,rule='hrulefill',macro=origin)
    if origin in {'memory@twolines','memory@fourlines'}:
        return dict(kind='ruled-lines',origin=origin,height=r'1.1\baselineskip',width='linewidth',lines=2 if origin.endswith('twolines') else 4,rule='hrulefill',macro=origin)
    if origin=='hrulefill':
        return dict(kind='inline-rule',origin=origin,height='0pt',width='fill',lines=1,rule='hrulefill',macro=origin)
    if origin=='rule':
        if height not in STRUTS:raise GeometryError('unknown canonical table response strut: '+str(height))
        return dict(kind='table-row-space',origin=origin,height=height,width='0pt',lines=0,rule='none',macro='rule')
    if origin not in {'Exercise','ShortExercise','LongExercise','PassageExercise','AssessmentItem','RuleLine','vspace'}:
        raise GeometryError('unknown canonical response origin: '+origin)
    if height not in HEIGHTS and not (origin=='vspace' and height==r'1.1\baselineskip'):
        raise GeometryError('unknown canonical response height: '+str(height))
    rule='hrule' if origin=='RuleLine' else 'hrulefill'
    return dict(kind='response-block',origin=origin,height=height,width='linewidth',lines=1,rule=rule,macro=rule)


def variant(event):
    kind=event['kind'];origin=event['origin']
    if kind=='blank-cell':return 'response-cell'
    if kind=='ruled-lines':return 'response-lines-'+str(event['lines'])
    if kind=='table-row-space':return 'response-strut-'+STRUTS[event['height']]
    if kind=='response-block':
        return 'response-block-baseline110' if event['height']==r'1.1\baselineskip' else 'response-block-'+HEIGHTS[event['height']]
    return {'Blank':'response-blank-short','LongBlank':'response-blank-long','hrulefill':'response-rule'}[origin]


def render(event, number):
    name=variant(event)
    attrs=' class="response-space '+name+'" data-response-id="response-'+str(number)+'" data-response-origin="'+html.escape(event['origin'],quote=True)+'" aria-label="Response space"'
    children='<span class="response-ruled-line"></span>'*event['lines'] if event['kind']=='ruled-lines' else ''
    return '<span'+attrs+'>'+children+'</span>'


class GeometryHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.events=[];self.root=None;self.depth=0;self.line_children=0
    def handle_starttag(self,tag,attrs):
        values=dict(attrs);classes=values.get('class','').split()
        if 'response-space' in classes:
            if self.root is not None or tag!='span':raise GeometryError('nested or non-span response geometry')
            allowed={'class','data-response-id','data-response-origin','aria-label'}
            if len(attrs)!=len(allowed) or set(values)!=allowed or values.get('aria-label')!='Response space':
                raise GeometryError('unexpected response geometry attributes')
            origin=values.get('data-response-origin');name=[c for c in classes if c!='response-space']
            if len(name)!=1:raise GeometryError('response geometry requires one exact finite variant')
            value=name[0];height=None
            if value.startswith('response-strut-'):
                height=next((metric for metric,code in STRUTS.items() if value=='response-strut-'+code),None)
            elif value.startswith('response-block-'):
                height=r'1.1\baselineskip' if value=='response-block-baseline110' else next((metric for metric,code in HEIGHTS.items() if value=='response-block-'+code),None)
            event=signature(origin,height)
            if variant(event)!=value:raise GeometryError('response variant disagrees with canonical metrics')
            event['id']=values.get('data-response-id')
            if not re.fullmatch(r'response-[1-9][0-9]*',event['id'] or ''):raise GeometryError('response geometry lacks occurrence identity')
            self.root=event;self.depth=1;self.line_children=0
        elif self.root is not None:
            if tag!='span' or len(attrs)!=1 or set(values)!={'class'} or classes!=['response-ruled-line'] or self.root['kind']!='ruled-lines' or self.depth!=1:
                raise GeometryError('unknown response geometry child')
            self.depth+=1;self.line_children+=1
        elif any(name.startswith('response-') for name in classes):
            raise GeometryError('orphan response geometry class')
    def handle_endtag(self,tag):
        if self.root is None:return
        if tag!='span':raise GeometryError('response geometry must remain inside its span host')
        self.depth-=1
        if self.depth==0:
            expected=self.root['lines'] if self.root['kind']=='ruled-lines' else 0
            if self.line_children!=expected:raise GeometryError('response ruled-line count differs from source')
            self.events.append(self.root);self.root=None
    def handle_data(self,value):
        if self.root is not None and value:raise GeometryError('response geometry contains unowned visible text')

    def handle_comment(self,value):
        if self.root is not None:raise GeometryError('response geometry must not contain comments')


def check(expected, rendered):
    parser=GeometryHTML();parser.feed(rendered);parser.close()
    if parser.root is not None:raise GeometryError('unclosed response geometry')
    wanted=[{key:event[key] for key in ('id',*FIELDS)} for event in expected]
    if parser.events!=wanted:
        mismatch=next((i for i,pair in enumerate(zip(wanted,parser.events)) if pair[0]!=pair[1]),min(len(wanted),len(parser.events)))
        raise GeometryError('canonical response geometry missing, changed, repeated or reordered at occurrence '+str(mismatch+1))
    return {'status':'pass','complete':True,'unit_count':len(wanted),
            'kinds':dict(Counter(event['kind'] for event in wanted)),
            'variants':dict(Counter(variant(event) for event in wanted)),
            'expected_digest':hashlib.sha256(json.dumps(expected,sort_keys=True).encode()).hexdigest()}
