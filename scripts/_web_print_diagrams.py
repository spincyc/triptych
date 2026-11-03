"""Verified immutable TikZ SVG lookup. No TeX, PDF, or renderer subprocesses."""
from __future__ import annotations
import copy
import html
import hashlib
import json
from pathlib import Path
import re

PINNED_PROJECTION_DIGEST='695b7e90bbbb37c127ccd7cd6ff3bb53977124ccdf584a0bb548da751177f8fa'

class DiagramRefused(ValueError):
    pass

def digest(data: bytes | str) -> str:
    return hashlib.sha256(data.encode() if isinstance(data,str) else data).hexdigest()

def canonical_json(value) -> bytes:
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()

def mask_comments(text: str) -> str:
    chars=list(text)
    for m in re.finditer('%[^\n]*',text):
        p=m.start()-1;slashes=0
        while p>=0 and text[p]=='\\': slashes+=1;p-=1
        if slashes%2==0:
            chars[m.start():m.end()]=' '*len(m.group())
    return ''.join(chars)

def diagram_spans(body: str) -> list[dict]:
    masked=mask_comments(body)
    tokens=re.compile(r'\\(begin|end)\s*\{\s*([^}\s]+)\s*\}')
    stack=[]; found=[]; active=None
    for m in tokens.finditer(masked):
        action,name=m.groups()
        if action=='begin':
            if name=='tikzpicture':
                if active is not None:raise DiagramRefused('nested TikZ picture')
                active={'start':m.start(),'context':list(stack)}
            stack.append(name)
        else:
            if not stack or stack[-1]!=name:
                raise DiagramRefused('unbalanced source environment: '+name)
            stack.pop()
            if name=='tikzpicture':
                assert active is not None
                active['end']=m.end();active['source_tex_sha256']=digest(body[active['start']:active['end']])
                found.append(active);active=None
    if active is not None:raise DiagramRefused('unclosed TikZ picture')
    return found

def closure(selection: dict) -> list[dict]:
    entries={row['path']:row['sha256'] for row in selection['selection']['ordered_inputs']}
    return [{'path':p,'sha256':h} for p,h in sorted(entries.items())]


def tex_group(text: str, start: int) -> tuple[str,int]:
    masked=mask_comments(text);depth=1;p=start+1
    while depth:
        if p>=len(text):raise DiagramRefused('unclosed source label')
        if masked[p] in '{}':
            j=p-1;n=0
            while j>=0 and masked[j]=='\\':n+=1;j-=1
            if n%2==0:depth+=1 if masked[p]=='{' else -1
        p+=1
    return text[start+1:p-1],p

def node_labels(tex: str) -> list[str]:
    masked=mask_comments(tex);result=[]
    for match in re.finditer(r'\\node\b',masked):
        p=match.end();square=paren=0
        while p<len(tex):
            ch=masked[p]
            if ch=='[':square+=1
            elif ch==']':square-=1
            elif ch=='(' and square==0:paren+=1
            elif ch==')' and square==0:paren-=1
            elif ch=='{' and square==0 and paren==0:
                body,p=tex_group(tex,p);result.append(body);break
            elif ch==';' and square==0 and paren==0:break
            p+=1
    return result

def selected_source_refs(selection: dict, start: int, end: int) -> list[dict]:
    result=[];cursor=0
    for chunk in selection['chunks']:
        nxt=cursor+len(chunk['text'])
        a,b=max(cursor,start),min(nxt,end)
        if a<b:
            text=chunk['text'][a-cursor:b-cursor]
            result.append({'path':chunk['path'],'occurrence':chunk['occurrence'],
                           'selected_line':chunk['selected_line']+chunk['text'][:a-cursor].count('\n'),
                           'diagram_offset':a-start,'length':b-a,'selected_fragment_sha256':digest(text)})
        cursor=nxt
    if sum(r['length'] for r in result)!=end-start:raise DiagramRefused('diagram source-chunk coverage mismatch')
    return result

def resolve(root: Path, output_id: str, selection: dict, *, asset_root: Path, expected_projection_digest: str = PINNED_PROJECTION_DIGEST) -> list[dict]:
    """Return occurrence-bound records for the exact original selected body."""
    root=Path(root).resolve();base=Path(asset_root).resolve()
    manifest=json.loads((base/'manifest.json').read_text())
    if manifest.get('schema')!='triptych-selected-diagram-assets/v1':
        raise DiagramRefused('unsupported SVG projection manifest')
    projection=manifest.get('projection_digest')
    if projection != digest(canonical_json({k:v for k,v in manifest.items() if k!='projection_digest'})):
        raise DiagramRefused('diagram manifest digest mismatch')
    if expected_projection_digest is not None and projection!=expected_projection_digest:
        raise DiagramRefused('diagram manifest disagrees with pinned projection')
    row=manifest['outputs'].get(output_id)
    spans=diagram_spans(selection['body'])
    if row is None:
        if spans:raise DiagramRefused('no verified diagram projection for '+output_id)
        return []
    declared=selection['selection']
    if declared['selection_digest'] != digest(canonical_json({k:v for k,v in declared.items() if k!='selection_digest'})):
        raise DiagramRefused('selected-source state digest mismatch')
    expected={'selection_digest':selection['selection']['selection_digest'],
              'head_sha256':digest(selection['head']),'body_sha256':digest(selection['body']),
              'source_closure':closure(selection)}
    for key,value in expected.items():
        if row[key]!=value:raise DiagramRefused('stale diagram projection '+key+': '+output_id)
    for item in expected['source_closure']:
        path=(root/item['path']).resolve()
        if not path.is_relative_to(root/'src') or not path.is_file() or digest(path.read_bytes())!=item['sha256']:
            raise DiagramRefused('diagram source closure mismatch: '+item['path'])
    units=row['diagrams']
    if len(spans)!=len(units):raise DiagramRefused('diagram occurrence count mismatch')
    for span,unit in zip(spans,units):
        for key in ['start','end','context','source_tex_sha256']:
            if span[key]!=unit[key]:raise DiagramRefused('diagram source occurrence mismatch: '+key)
        if unit['selection_digest']!=expected['selection_digest'] or unit['source_closure_digest']!=digest(canonical_json(expected['source_closure'])):
            raise DiagramRefused('diagram occurrence closure identity mismatch')
        tex=selection['body'][span['start']:span['end']]
        if unit['labels'] != node_labels(tex):raise DiagramRefused('diagram labels disagree with exact source')
        if unit['source_refs'] != selected_source_refs(selection,span['start'],span['end']):
            raise DiagramRefused('diagram source references disagree with selected chunks')
        path=(base/unit['asset']).resolve()
        if not path.is_relative_to(base/'assets') or not path.is_file():raise DiagramRefused('diagram asset unavailable')
        data=path.read_bytes()
        if digest(data)!=unit['svg_sha256'] or len(data)!=unit['bytes']:raise DiagramRefused('diagram asset hash/size mismatch')
    return [dict(u) for u in units]


SHIM=r'\newcommand{\SemanticDiagram}[1]{\par TRIPTYCHDIAGRAM#1ENDDIAGRAM\par}'+'\n'

def label_alt(unit: dict) -> str:
    """Minimal alt derived from the first actual authored node label."""
    if not unit.get('labels'):return ''
    text=unit['labels'][0]
    text=text.replace(r'\\',' ').replace(r'\&','&').replace(r'\%','%').replace(r'\_','_')
    text=re.sub(r'\\(?:textbf|textit|emph|textrm|textsf|scshape|upshape|scriptsize|footnotesize|small|normalsize)\b','',text)
    # Unknown control sequences need an explicitly supplied caller text projection.
    if re.search(r'\\[A-Za-z@]+',text):return ''
    return re.sub(r'\s+',' ',text.replace('{','').replace('}','').replace('~',' ')).strip()

def lua_string(text: str) -> str:
    eq='='
    while ']'+eq+']' in text:eq+='='
    return '['+eq+'['+text+']'+eq+']'

def lua_filter(records: list[dict], asset_url=None, alt_text=None) -> str:
    mapping=[]
    for unit in records:
        uid=unit['asset_id']
        if not re.fullmatch(r'tikz-[a-f0-9]{24}',uid):raise DiagramRefused('invalid stable SVG asset ID')
        url=asset_url(unit) if asset_url else unit['asset']
        alt=alt_text(unit) if alt_text else label_alt(unit)
        attrs={'data-semantic-diagram':uid,'data-source-asset':uid,'src':url,'alt':alt,
               'data-svg-sha256':unit['svg_sha256'],'data-source-tex-sha256':unit['source_tex_sha256'],
               'data-selection-digest':unit['selection_digest'],
               'data-source-labels-sha256':digest(canonical_json(unit['labels']))}
        img='<img '+' '.join(k+'="'+html.escape(str(v),quote=True)+'"' for k,v in attrs.items())+'>'
        figure='<figure data-semantic-asset="'+uid+'">'+img+'</figure>'
        mapping.append('  ["'+uid+'"] = '+lua_string(figure))
    table=',\n'.join(mapping)
    return """local assets = {
@ASSETS@
}
local seen = {}
local function project(block)
  local text = pandoc.utils.stringify(block.content)
  local key = text:match('^TRIPTYCHDIAGRAM(tikz%-%x+)ENDDIAGRAM$')
  if not key then
    if text:find('TRIPTYCHDIAGRAM',1,true) then error('Malformed or nonstandalone diagram sentinel') end
    return nil
  end
  if not assets[key] then error('Unbound selected diagram: '..key) end
  seen[key] = (seen[key] or 0) + 1
  if seen[key] ~= 1 then error('Duplicate selected diagram: '..key) end
  return pandoc.RawBlock('html', assets[key])
end
return {
  {Para=project, Plain=project},
  {Pandoc=function(doc)
    for key,_ in pairs(assets) do
      if seen[key] ~= 1 then error('Missing selected diagram: '..key) end
    end
    return doc
  end}
}
""".replace('@ASSETS@',table)

def project(selection: dict, records: list[dict], *, asset_url=None, alt_text=None) -> dict:
    """Replace original bound TikZ spans; retain capsule for post-flow merging.

    Call after deriving the original ledger and before flow preparation.
    Flow preparation may rebuild its shim/filter fields. Append shim/projection
    records afterward, and PREPEND diagram Lua filters before flow's container
    serializers so nested source diagrams are resolved before raw HTML output.
    Asset URLs are caller mapped, so no scratch path enters product HTML.
    """
    body=selection['body'];spans=diagram_spans(body)
    if len(spans)!=len(records):raise DiagramRefused('projection must bind every active TikZ span')
    pieces=[];cursor=0
    for span,unit in zip(spans,records):
        for key in ['start','end','source_tex_sha256']:
            if span[key]!=unit[key]:raise DiagramRefused('diagram projection span mismatch')
        pieces.extend([body[cursor:span['start']],'\n\n'+r'\SemanticDiagram{'+unit['asset_id']+'}\n\n'])
        cursor=span['end']
    pieces.append(body[cursor:]);newbody=''.join(pieces)
    result=copy.copy(selection)
    result.update(body=newbody,source=selection['head']+r'\begin{document}'+newbody+r'\end{document}',
                  canonical_body=selection.get('canonical_body',body),diagram_units=records)
    result['diagram_projection']={
       'shim_additions':SHIM if records else '',
       'lua_filters':[lua_filter(records,asset_url=asset_url,alt_text=alt_text)] if records else [],
       'projections':[{'kind':'verified-tikz-svg','asset_id':u['asset_id'],'source_tex_sha256':u['source_tex_sha256'],
                       'svg_sha256':u['svg_sha256'],'source_start':u['start'],'source_end':u['end']} for u in records]}
    return result
