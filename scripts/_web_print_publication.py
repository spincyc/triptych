"""Complete, selected-source browser-print publications.

The canonical TeX and publication role are selected before conversion. An
independent bounded-DSL ledger proves every visible content unit; the existing
web-edition converter retains its structural audits. This generates mechanical
print content and conveys no new editorial, rights or visual review approval.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import html
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec,spec_from_loader
import json
from pathlib import Path
import re
import sys
import shutil
import tempfile
import tomllib
from _web_print_semantics import expected_units, check_units, HtmlLedger
from _web_print_flow import prepare, prepare_markdown
from _web_print_common import normalize_html


from html.parser import HTMLParser


class PartError(ValueError):pass

class Blocks(HTMLParser):
    VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self,text):
        super().__init__(convert_charrefs=False);self.text=text;self.lines=[0];self.stack=[];self.ends=[]
        for n,c in enumerate(text):
            if c=='\n':self.lines.append(n+1)
    def source_offset(self):
        row,col=self.getpos();return self.lines[row-1]+col
    def handle_starttag(self,tag,attrs):
        if tag not in self.VOID:self.stack.append(tag)
    def handle_startendtag(self,tag,attrs):
        if tag not in self.VOID:raise PartError('self-closing non-void HTML block: '+tag)
    def handle_endtag(self,tag):
        if not self.stack or self.stack.pop()!=tag:raise PartError('unbalanced HTML block: '+tag)
        if not self.stack:self.ends.append(self.text.index('>',self.source_offset())+1)
    def parts(self,limit):
        self.feed(self.text)
        if self.stack:raise PartError('unclosed HTML block')
        ends=self.ends+[len(self.text)];blocks=[];cursor=0
        for end in ends:
            if end>cursor:blocks.append(self.text[cursor:end]);cursor=end
        parts=[];current=''
        for block in blocks:
            if len(block.encode())>=limit:raise PartError('single semantic HTML block exceeds part limit')
            if len((current+block).encode())>=limit:
                parts.append(current);current=''
            current+=block
        if current.strip():parts.append(current)
        return [{'id':f'part-{i:03d}','html':part,'bytes':len(part.encode()),'html_sha256':hashlib.sha256(part.encode()).hexdigest()} for i,part in enumerate(parts,1)]

def split_parts(html,limit=600000):return Blocks(html).parts(limit)


class Refused(ValueError): pass

PANDOC_BINARY_SHA256='870b811354a230a1864dd2b50dec3b850a981926ff4659ae460aea96ab6b8d28'

def require_print_toolchain(root: Path | None = None):
    """Attest the exact official compiler bytes against the plaintext lock."""
    root=Path(root).resolve() if root is not None else Path(__file__).resolve().parents[1]
    lock_path=root/'src/common/browser-print-toolchain.toml'
    try:
        lock=tomllib.loads(lock_path.read_text())
    except (OSError,tomllib.TOMLDecodeError) as error:
        raise Refused('browser-print compiler requires its valid plaintext toolchain lock') from error
    if set(lock)!={'schema_version','record_type','pandoc'} or (type(lock.get('schema_version')) is not int or lock.get('schema_version')!=1) or lock.get('record_type')!='browser-print-toolchain':
        raise Refused('unsupported browser-print toolchain lock')
    spec=lock['pandoc']
    fields={'version','archive_url','archive_sha256','archive_bytes','binary_sha256','binary_bytes','member'}
    if not isinstance(spec,dict) or set(spec)!=fields:
        raise Refused('invalid locked Pandoc fields')
    if not all(isinstance(spec[key],str) for key in ('version','archive_url','archive_sha256','binary_sha256','member')):
        raise Refused('invalid immutable Pandoc string fields')
    if spec['version']!='3.11' or spec['binary_sha256']!=PANDOC_BINARY_SHA256:
        raise Refused('locked Pandoc is outside the audited compiler identity')
    if (not re.fullmatch(r'[a-f0-9]{64}',spec['archive_sha256']) or
        spec['archive_url']!='https://github.com/jgm/pandoc/releases/download/3.11/pandoc-3.11-linux-amd64.tar.gz' or
        spec['member']!='pandoc-3.11/bin/pandoc' or
        any(not isinstance(spec[key],int) or isinstance(spec[key],bool) or spec[key]<=0 for key in ('archive_bytes','binary_bytes'))):
        raise Refused('invalid immutable Pandoc archive/binary lock')
    executable=shutil.which('pandoc')
    if executable is None:raise Refused('the pinned print Pandoc is unavailable')
    binary=Path(executable)
    if binary.stat().st_size!=spec['binary_bytes']:
        raise Refused('print generation requires the verified official Pandoc binary, not another build with the same version')
    actual=hashlib.sha256(binary.read_bytes()).hexdigest()
    if actual!=spec['binary_sha256']:
        raise Refused('print generation requires the verified official Pandoc binary, not another build with the same version')
    return {'pandoc_version':spec['version'],'pandoc_binary_sha256':actual,
            'pandoc_binary_bytes':spec['binary_bytes'],
            'lock_path':lock_path.relative_to(root).as_posix(),
            'lock_sha256':hashlib.sha256(lock_path.read_bytes()).hexdigest()}



def load_library(root: Path, *, owner: Path | None = None):
    root=root.resolve()
    sys.path.insert(0,str(root/'scripts'))
    name='selected_web_'+hashlib.sha256((str(root)+str(owner)).encode()).hexdigest()[:12]
    loader=SourceFileLoader(name,str(owner if owner is not None else root/'tools/web-edition'))
    module=module_from_spec(spec_from_loader(name,loader))
    sys.modules[name]=module
    loader.exec_module(module)
    module.ROOT=root
    module.SRC=root/'src'
    module.SHIM=root/'scripts/web-shim.tex'
    return module


CONDITIONAL=re.compile(r'\\(?:if[A-Za-z@]*|else|fi)\b')
FLAGS={'TriptychPrintEdition':False,'TriptychSynthesisEdition':False,'TriptychHomilyEdition':False}

def select_branches(text: str, mode: str, library) -> str:
    """Balanced edition switches; choose the selected output, never research by default."""
    text=library.LEAD_COMMENT_RE.sub('',text)
    values={**FLAGS,'TriptychSynthesisEdition':mode=='synthesis','TriptychHomilyEdition':mode=='homily'}
    masked=library.mask_tex_comments(text)
    cursor=0; pieces=[]
    while True:
        start=re.search(r'\\ifdefined\s*\\([A-Za-z@]+)',masked[cursor:])
        if not start:pieces.append(text[cursor:]);break
        a,b=cursor+start.start(),cursor+start.end()
        name=start.group(1)
        if name not in values:
            raise Refused('unsupported conditional flag: '+name)
        depth=1; middle=None; ending=None
        for token in CONDITIONAL.finditer(masked,b):
            if token.group().startswith('\\if'):depth+=1
            elif token.group()=='\\fi':
                depth-=1
                if depth==0:ending=token;break
            elif token.group()=='\\else' and depth==1:middle=token
        if ending is None:raise Refused('unclosed edition conditional')
        yes=text[b:middle.start() if middle else ending.start()]
        no=text[middle.end():ending.start()] if middle else ''
        branch=select_branches(yes if values[name] else no,mode,library)
        # Preserve the established converter's inline/block seam semantics.
        if text[ending.end():].startswith('{}'):
            branch=library.BRANCH_TAIL_RE.sub('',branch.lstrip())
        else:
            if text[a-1:a]=='\n' and branch.startswith('\n'):branch=branch[1:]
            if text[ending.end():ending.end()+1]=='\n' and branch.endswith('\n'):branch=branch[:-1]
        pieces.extend((text[cursor:a],branch));cursor=ending.end()
    return ''.join(pieces)


def selected_source(root: Path, recipe: dict, library) -> dict:
    """Independently record ordered, occurrence-aware source selection first."""
    provider=recipe['provider']; mode=recipe['edition']; inputs={}; occurrences=Counter(); events=[]; stack=[]; chunks=[]
    def walk(path):
        path=path.resolve()
        if not path.is_relative_to(root/'src'/provider) and not path.is_relative_to(root/'src/common'):
            raise Refused('source escapes provider/common owner')
        if path in stack:raise Refused('input cycle')
        raw=path.read_text(); selected=select_branches(raw,mode,library)
        rel=path.relative_to(root).as_posix(); occurrences[rel]+=1
        occurrence=occurrences[rel]
        events.append({'path':rel,'occurrence':occurrence,'sha256':hashlib.sha256(raw.encode()).hexdigest(),'selected_sha256':hashlib.sha256(selected.encode()).hexdigest()})
        inputs[path]=selected;stack.append(path)
        # The common shim owns typography, rights and provenance projection.
        if path==root/'src/common/preamble.tex':stack.pop();return ''
        pieces=[]; cursor=0
        for match in library.INPUT_RE.finditer(library.mask_tex_comments(selected)):
            name=match.group(1).strip()
            if '\\' in name:raise Refused('dynamic input requires its owning adapter: '+name)
            target=library.resolve_input(name,provider)
            if target is None:raise Refused('unresolved input: '+name)
            chunks.append({'path':rel,'occurrence':occurrence,'selected_line':selected[:cursor].count('\n')+1,'text':selected[cursor:match.start()]})
            pieces.extend((selected[cursor:match.start()],walk(target)))
            cursor=match.end()
        chunks.append({'path':rel,'occurrence':occurrence,'selected_line':selected[:cursor].count('\n')+1,'text':selected[cursor:]})
        pieces.append(selected[cursor:]);stack.pop()
        return ''.join(pieces)
    entry=root/recipe['entrypoint']
    source=walk(entry)
    head,body=library.split_document(source)
    selection={'entrypoint':recipe['entrypoint'],'role':mode,'flags':{**FLAGS,'TriptychSynthesisEdition':mode=='synthesis','TriptychHomilyEdition':mode=='homily'},'ordered_inputs':events}
    selection['selection_digest']=hashlib.sha256(json.dumps(selection,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    begin=source.index(r'\begin{document}')+len(r'\begin{document}'); end=source.rindex(r'\end{document}')
    cursor=0; body_chunks=[]
    for chunk in chunks:
        next_cursor=cursor+len(chunk['text'])
        if cursor<end and next_cursor>begin:
            kept=chunk['text'][max(0,begin-cursor):min(len(chunk['text']),end-cursor)]
            body_chunks.append({**chunk,'text':kept})
        cursor=next_cursor
    if ''.join(chunk['text'] for chunk in body_chunks)!=body:raise Refused('ordered source chunk assembly mismatch')
    return {'source':source,'head':head,'body':body,'sources':inputs,'selection':selection,'chunks':body_chunks}




class PrintUnitMarkers(HTMLParser):
    """Read only existing unit identities; never infer them from visible text."""
    def __init__(self):
        super().__init__(convert_charrefs=False);self.units=[]
    def handle_starttag(self,tag,attrs):
        values=[value for name,value in attrs if name=='data-print-unit']
        if len(values)>1:raise Refused('duplicate print-unit attribute')
        if values:
            if values[0] is None or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.:-]*',values[0]):
                raise Refused('invalid print-unit identity')
            self.units.append(values[0])
    handle_startendtag=handle_starttag


def validate_internal_targets(fragment):
    """Require each generated internal hyperlink to resolve to one actual ID."""
    class Targets(HTMLParser):
        def __init__(self):
            super().__init__();self.ids=[];self.targets=[]
        def handle_starttag(self,tag,attrs):
            values=dict(attrs)
            if values.get('id') is not None:self.ids.append(values['id'])
            if tag=='a' and values.get('href','').startswith('#'):
                self.targets.append(values['href'][1:])
        handle_startendtag=handle_starttag
    parsed=Targets();parsed.feed(fragment);parsed.close();counts=Counter(parsed.ids)
    from urllib.parse import unquote
    failures=sorted({target for target in parsed.targets if counts[target]!=1 and counts[unquote(target)]!=1})
    if failures:raise Refused('internal print links lack one concrete target: '+', '.join(failures))


def print_unit_ids(fragment):
    parser=PrintUnitMarkers();parser.feed(fragment);parser.close()
    if len(parser.units)!=len(set(parser.units)):raise Refused('duplicate print-unit identity')
    return parser.units



def unit_expectations(ledger, ordered_ids):
    """Return compact source provenance in the proved DOM occurrence order."""
    records={}
    for unit in [*ledger['units'],*ledger.get('containers',[])]:
        uid=unit['id']
        if uid in records:raise Refused('canonical visible/container identity collision')
        reference=unit.get('source_ref')
        if isinstance(reference,list):reference=reference[0] if reference else None
        if not isinstance(reference,dict) or not reference.get('path'):
            raise Refused('print occurrence lacks canonical source provenance')
        source=reference['path']
        if Path(source).is_absolute():raise Refused('print provenance contains a physical workspace path')
        records[uid]={'id':uid,'source':source,'occurrence':unit.get('occurrence_id',uid),
                      'source_occurrence':reference.get('occurrence',1),
                      'source_line':reference.get('selected_line',1),
                      'coordinate_space':reference.get('coordinate_space','selected-canonical-source'),
                      'kind':unit.get('kind',unit.get('environment','container'))}
    if Counter(ordered_ids)!=Counter(records.keys()):raise Refused('ordered print identities differ from canonical occurrences')
    return [records[uid] for uid in ordered_ids]


def bind_print_units(ledger, rendered, coverage):
    """Bind independently proved source occurrences to exact legal DOM positions.

    Content-free inline markers precede the original text bytes. Atomic MathML
    and image units bind their actual host. This neither rebuilds prose from a
    second parser nor places illegal children in table/tr/MathML containers.
    Returns the bound HTML and its source-derived ordered DOM identity list.
    """
    if coverage.get('status')!='pass' or coverage.get('complete') is not True:
        raise Refused('print unit binding requires complete canonical coverage')
    source_ids=[unit['id'] for unit in ledger['units']]
    matched=coverage.get('matched_units',[])
    if Counter(item['id'] for item in matched)!=Counter(source_ids):
        raise Refused('coverage does not bind every canonical occurrence exactly once')
    existing=print_unit_ids(rendered)
    expected_containers=[container['id'] for container in ledger.get('containers',[])]
    parser=HtmlLedger();parser.feed(rendered);actual=parser.finish()
    inserts=[];ordered=[];used=set()
    safe={'p','li','td','th','dt','dd','h1','h2','h3','h4','h5','h6','figcaption'}
    for match in matched:
        index=match['output_block'];uid=match['id']
        if index in used or not 0<=index<len(actual):raise Refused('ambiguous output-block source binding')
        used.add(index);unit=actual[index];host=unit['host_tag']
        if host in {'math','img'}:
            start=unit['host_start'];end=rendered.find('>',start)
            if end<0 or not rendered.startswith('<'+host,start):raise Refused('atomic source host offset mismatch')
            token=rendered[start:end+1]
            if 'data-print-unit' in token:raise Refused('atomic source host already has a print-unit attribute')
            position=end-1 if rendered[end-1:end]=='/' else end
            inserts.append((position,' data-print-unit="'+uid+'"'))
            ordered.append((start,uid))
        elif host in safe:
            position=unit['content_start']
            if not isinstance(position,int) or position<unit['host_start'] or position>len(rendered):
                raise Refused('visible source unit has an invalid content offset')
            inserts.append((position,'<span data-print-unit="'+uid+'"></span>'))
            ordered.append((position,uid))
        else:raise Refused('source unit has no legal print marker host: '+host)
    # Include independently owned source containers at their original DOM offsets.
    class ContainerPositions(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False);self.lines=[0];self.found=[]
            self.lines.extend(index+1 for index,char in enumerate(rendered) if char=='\n')
        def handle_starttag(self,tag,attrs):
            values=dict(attrs);uid=values.get('data-semantic-minipage')
            if uid:
                self.found.append(uid)
                row,column=self.getpos();start=self.lines[row-1]+column
                existing_uid=values.get('data-print-unit')
                if existing_uid is not None and existing_uid!=uid:raise Refused('semantic container has a different print identity')
                if existing_uid is None:
                    end=rendered.find('>',start)
                    if end<0:raise Refused('semantic container opening is unclosed')
                    inserts.append((end,' data-print-unit="'+uid+'"'))
                ordered.append((start,uid))
            elif values.get('data-print-unit'):
                raise Refused('pre-existing print unit lacks its canonical container owner')
        handle_startendtag=handle_starttag
    positions=ContainerPositions();positions.feed(rendered);positions.close()
    if positions.found!=expected_containers:raise Refused('semantic containers disagree with their canonical ordered owners')
    if len({offset for offset,_ in inserts})!=len(inserts):
        raise Refused('distinct canonical units have the same insertion position')
    bound=rendered
    for offset,addition in sorted(inserts,reverse=True):bound=bound[:offset]+addition+bound[offset:]
    expected_order=[uid for _,uid in sorted(ordered)]
    if print_unit_ids(bound)!=expected_order:raise Refused('DOM print-unit order disagrees with canonical source bindings')
    verified=check_units(ledger,bound)
    if verified.get('status')!='pass' or verified.get('complete') is not True or verified.get('matched_units')!=matched:
        raise Refused('adding print identities changed complete source coverage')
    return bound,expected_order



def project_reference_displays(selection, ledger, library):
    """Resolve literal ref calls from executed canonical label/counter state.

    Pandoc counts dormant headings in macro definitions differently. Replacing
    an actual literal ref with an equivalent explicit link preserves both its
    exact target and canonical numeric display without rewriting custom links.
    """
    displays={}
    for reference in ledger.get('references',[]):
        if reference['command']!='ref':continue
        target=reference['target'];display=reference.get('display')
        if not isinstance(display,str) or not re.fullmatch(r'[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)*',display):
            raise Refused('canonical reference lacks a supported exact counter display: '+target)
        if target in displays and displays[target]!=display:raise Refused('ambiguous canonical reference display')
        displays[target]=display
    body=selection['body'];masked=library.mask_tex_comments(body);pieces=[];cursor=0;records=[]
    for match in re.finditer(r'\\ref(?![A-Za-z@])',masked):
        start=library.skip_gap(masked,match.end())
        if masked[start:start+1]!='{':continue
        target,end=library.brace_group(body,start)
        if target not in displays:continue
        replacement=r'\hyperref['+target+']{'+displays[target]+'}'
        pieces.extend((body[cursor:match.start()],replacement));cursor=end
        records.append({'kind':'canonical-reference-display','target':target,'display':displays[target],'source_offset':match.start(),'source_sha256':hashlib.sha256(body[match.start():end].encode()).hexdigest()})
    if not records:return selection
    pieces.append(body[cursor:]);newbody=''.join(pieces);result=dict(selection)
    result.update(body=newbody,source=selection['head']+r'\begin{document}'+newbody+r'\end{document}',canonical_body=selection.get('canonical_body',body),audit_body=newbody)
    result['projections']=list(selection.get('projections',[]))+records
    return result


def project_heading_aliases(selection, library):
    """Project actual scoped heading-to-heading aliases in the selected DSL.

    The independent canonical ledger is already derived. Only the three known
    sectioning primitives are modeled; definitions that defer their execution
    under an active alias refuse rather than guessing at TeX expansion state.
    """
    body=selection['body']; masked=library.mask_tex_comments(body)
    headings={'section','subsection','subsubsection'}
    mapping={name:name for name in headings}; frames=[]; pieces=[]; cursor=0; records=[]
    command=re.compile(r'\\([A-Za-z@]+)')
    def segment(start,end):
        raw=body[start:end]; scan=masked[start:end]
        pieces.append(command.sub(lambda m:'\\'+mapping[m.group(1)] if m.group(1) in mapping else m.group(),raw))
    for kind,value in library.walk_definitions(masked):
        if kind in {'open','close'}:
            segment(cursor,value); cursor=value
            if kind=='open':frames.append(dict(mapping))
            elif frames:mapping=frames.pop()
            continue
        definition=value
        segment(cursor,definition.start); cursor=definition.end
        if definition.command=='let' and definition.name in headings and definition.source in headings:
            if definition.problem:raise Refused('unsupported heading alias: '+definition.problem)
            mapping[definition.name]=mapping[definition.source]
            if definition.glob:
                for frame in frames:frame[definition.name]=mapping[definition.source]
            records.append({'kind':'scoped-heading-alias','name':definition.name,'source':definition.source,'rendered_as':mapping[definition.name],'source_offset':definition.start,'source_sha256':hashlib.sha256(body[definition.start:definition.end].encode()).hexdigest()})
            pieces.append(' ')
        else:
            if any(name!=target for name,target in mapping.items()) and any(m.group(1) in headings for m in command.finditer(masked[definition.start:definition.end])):
                raise Refused('deferred heading definition under a section alias requires an explicit adapter')
            pieces.append(body[definition.start:definition.end])
    segment(cursor,len(body))
    if not records:return selection
    if frames:raise Refused('unclosed scope in heading alias projection')
    newbody=''.join(pieces)
    result=dict(selection)
    result.update(body=newbody,source=selection['head']+r'\begin{document}'+newbody+r'\end{document}',canonical_body=selection.get('canonical_body',body),audit_body=newbody)
    result['projections']=list(selection.get('projections',[]))+records
    return result


def _diagram_helpers():
    import _web_print_diagrams as diagrams
    return diagrams


def convert_output(root: Path, provider: str, output: str, out: Path, *, asset_resolver=None, asset_url=None) -> dict:
    root=root.resolve(); out=out.resolve()
    toolchain=require_print_toolchain(root)
    if not out.is_relative_to(root/'.scratch') and not out.is_relative_to(root/'build'):
        raise Refused('print generation audit output must stay in ignored .scratch or build')
    sys.path.insert(0,str(root/'scripts'))
    from _print_document import publication_recipe
    recipe=publication_recipe(provider,output,root=root)
    leaf=root/'src'/provider/recipe['canonical']
    declaration=tomllib.loads((leaf/'web-edition.toml').read_text())
    publication_kind=tomllib.loads((leaf/'publication.toml').read_text())['kind']
    release=root/'release/publications'/provider/(output+'.json')
    if declaration.get('withdrawn') or not release.is_file() or json.loads(release.read_text()).get('status')!='alpha':
        raise Refused('selected output is held or not public')
    library=load_library(root)
    selection=selected_source(root,recipe,library)
    # Mechanical semantics only: fixed/drawn content needs a specialized owner.
    blockers=[]
    for name in ('picture',):
        if re.search(r'\\begin\s*\{'+name+r'\}',library.mask_tex_comments(selection['body'])):blockers.append(name)
    if re.search(r'\\includegraphics\b',selection['body']):blockers.append('unresolved asset inventory')
    if blockers:raise Refused('specialized adapter required: '+', '.join(blockers))
    diagrams=[];diagram_capsule={}
    if re.search(r'\\begin\s*\{tikzpicture\}',library.mask_tex_comments(selection['body'])):
        projection=_diagram_helpers()
        if asset_resolver is None:
            from _web_print_assets import generic_assets
            asset_resolver=lambda checkout,identity,selected:generic_assets(checkout,identity,selected,include_body=False)
        diagrams=asset_resolver(root,provider+'/'+output,selection)
        for unit in diagrams:
            unit['rendered_src']=asset_url(unit) if asset_url is not None else unit.get('src')
            if not isinstance(unit['rendered_src'],str) or not unit['rendered_src']:
                raise Refused('verified diagram has no public asset token')
        selection['diagram_assets']=diagrams
    ledger=expected_units(selection,library)
    if diagrams:
        selection=projection.project(selection,diagrams,asset_url=lambda unit:unit['rendered_src'])
        selection['audit_body']=selection['body']
        diagram_capsule=selection['diagram_projection']
    selection=project_reference_displays(selection,ledger,library)
    selection=project_heading_aliases(selection,library)
    selection=prepare(selection,library,expected_ledger=ledger)
    if diagrams:
        selection['shim_additions']+=diagram_capsule['shim_additions']
        selection['lua_filters']=diagram_capsule['lua_filters']+selection['lua_filters']
        selection['projections']+=diagram_capsule['projections']
        # Internal diagram tables are covered by the source-bound SVG unit.
        selection['audit_body']=selection['body']

    units=ledger['units']
    out.mkdir(parents=True,exist_ok=True)
    shim=out/'print-shim.tex'
    shim.write_text(library.SHIM.read_text()+'\n'+r'\newenvironment{properhomily}{}{}'+\
                    '\n'+r'\newenvironment{titlepage}{}{}'+\
                    '\n'+r'\newenvironment{multicols}[1]{}{}'+'\n'+r'\newcommand{\zlabel}[1]{}'+'\n'+selection['shim_additions'])
    library.SHIM=shim
    owning_audit=library.audit_output
    def capture_audit(*args,**kwargs):
        (out/'audit-body.tex').write_text(args[0])
        (out/'audit-output.md').write_text(args[1])
        failures=owning_audit(*args,**kwargs)
        (out/'owning-audit-result.json').write_text(json.dumps({'failures':failures},indent=2)+'\n')
        return failures
    def project_markdown(markdown):
        projected,records=prepare_markdown(markdown,selection,library)
        selection['projections'].extend(records)
        return projected
    context={**selection,'entrypoint':root/recipe['entrypoint'],'edition':recipe['edition'],'preserve_titlepage':True,'shim':shim,'audit_callback':capture_audit,'markdown_projection':project_markdown}
    # Owning temporary Lua/TeX files remain inside the dedicated scratch tree.
    temporary=out/'temporary'; temporary.mkdir(exist_ok=True)
    old_temp=tempfile.tempdir;tempfile.tempdir=str(temporary)
    try:markdown_path=library.convert(provider,output,out/'markdown',selected=context)
    finally:tempfile.tempdir=old_temp
    markdown=markdown_path.read_text()
    rendered=library.render_markdown(markdown,root)
    rendered=normalize_html(rendered)
    if re.search(r'\\(?:[A-Za-z@]+)',re.sub(r'<[^>]*>','',rendered)):
        raise Refused('unrendered TeX in final HTML')
    validate_internal_targets(rendered)
    coverage=check_units(ledger,rendered,library)
    if coverage['status']!='pass' or coverage.get('complete') is not True:
        (out/'coverage-refusal.json').write_text(json.dumps(coverage,indent=2)+'\n')
        raise Refused('independent selected-source coverage failed: '+str(coverage['missing_units'][:3]))
    rendered,expected_print_units=bind_print_units(ledger,rendered,coverage)
    result={'expected_print_units':expected_print_units,'print_unit_expectations':unit_expectations(ledger,expected_print_units),'schema':'triptych-print-publication/v1','toolchain':toolchain,'output_id':recipe['id'],'print_type':'proper' if publication_kind.startswith('proper') else 'flow','title':recipe.get('title') or output,'source_digest':hashlib.sha256(json.dumps(selection['selection']['ordered_inputs'],sort_keys=True).encode()).hexdigest(),'selection_digest':selection['selection']['selection_digest'],'parts':split_parts(rendered),'id':recipe['id'],'entrypoint':recipe['entrypoint'],'role':recipe['edition'],'status':'generated-mechanically-audited-unreviewed','selection':selection['selection'],'assets':[{'id':u['asset_id'],'src':u['rendered_src'],'sha256':u['svg_sha256'],'bytes':u['bytes'],'mime':'image/svg+xml','role':'diagram','source_tex_sha256':u['source_tex_sha256'],'source_inputs':u.get('source_inputs',{entry['path']:entry['sha256'] for entry in selection['selection']['ordered_inputs']})} for u in diagrams],'owning_audits':'all tools/web-edition audits retained','coverage_result':coverage,'expected_ledger':ledger,'projections':selection['projections'],'expected_units':units}
    policy_inputs=[]
    for path in (leaf/'publication.toml',leaf/'proper-components.toml',leaf/'web-edition.toml',release,root/'src/common/browser-print-toolchain.toml'):
        if path.is_file():
            policy_inputs.append({'path':path.relative_to(root).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    result['publication_binding']=policy_inputs
    result['source_digest']=hashlib.sha256(json.dumps({'ordered_source_inputs':selection['selection']['ordered_inputs'],'publication_binding':policy_inputs},sort_keys=True).encode()).hexdigest()
    offset=0
    assigned=[]
    for part in result['parts']:
        parser=HtmlLedger();parser.feed(part['html']);count=len(parser.finish())
        part['expected_print_units']=print_unit_ids(part['html'])
        part['source_unit_ids']=[unit['id'] for unit in coverage['matched_units'] if offset<=unit['output_block']<offset+count]
        assigned.extend(part['source_unit_ids']);offset+=count
    if sorted(assigned)!=sorted(unit['id'] for unit in units):
        raise Refused('balanced HTML parts lost or duplicated canonical unit bindings')
    page='<!doctype html><html lang="en"><meta charset="utf-8"><title>'+html.escape(recipe.get('title') or output)+'</title><style>body{font-family:serif;max-width:76ch;margin:2rem auto;line-height:1.45}table{border-collapse:collapse;width:100%}th,td{border:1px solid #999;padding:.35rem;vertical-align:top}thead{display:table-header-group}h1,h2,h3,h4{break-after:avoid}blockquote{margin-inline:1.5rem}img{max-width:100%}@media print{body{max-width:none;margin:0}a{color:inherit}tr{break-inside:avoid}}</style><article>'+rendered+'</article></html>'
    (out/'print.html').write_text(page)
    (out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def render_publication(root: Path, provider: str, output_id: str, *, asset_resolver=None, asset_url=None, audit_dir: Path | None = None) -> dict:
    """Return complete print content for one admitted exact publication output.

    The optional audit directory must be ignored build/scratch space. Detailed
    canonical provenance remains an authoring audit and must be compacted before
    browser-data delivery; it is never a new source or approval record.
    """
    root=Path(root).resolve()
    output=output_id.removeprefix('publication:').removeprefix(provider+'/')
    destination=audit_dir or root/'.scratch/web-print-publication'/hashlib.sha256((provider+'/'+output).encode()).hexdigest()[:16]
    return convert_output(root,provider,output,Path(destination),asset_resolver=asset_resolver,asset_url=asset_url)
