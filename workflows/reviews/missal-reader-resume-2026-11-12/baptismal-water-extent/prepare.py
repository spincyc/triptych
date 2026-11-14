#!/usr/bin/env python3
"""Prepare exact source-adopted water splices into scratch postimages only.

The actual typed Root source adoption and all three independent source reviews
are byte-pinned and checked. No application implementation or --apply option
exists. Root installs separately from exact fresh maps in its own window;
source_epoch admission and consumer gates remain separate.
"""
from pathlib import Path
import argparse
import copy
import difflib
import hashlib
import json
import re
import tomllib
import yaml

HERE=Path(__file__).resolve().parent
MANIFEST_SHA='0b67bd8d762597780057f9c3b568ddf89d052f4186601dfa97191007b989e9f0'
TRANSITION_SHA='52e55bb4479f1fe74f85a3ea9fc2a16366725fa44cb0456505d1cd5fc03214a2'
ROOT_ADOPTION_SHA256='e5247c34f6f5ef9aa200533b3e106aa0f7617723885f7a259fb6c8215b93a087'
REVIEW_CONTROLS=[('source-review.json', '.scratch/roman-sources/baptismal-water-independent-review/review.json', '0abbcd83ca64cd2b861026bf76cbbb0b06a333fcaf2ba269749e41a95d0377fc'), ('v4-review.json', '.scratch/roman-sources/baptismal-water-independent-review/v4-delta/review.json', '1889c1b391ea9337e7cf8b1634bff8d911c213a48d241a44ac1e7d7aaac6d527'), ('v5-review.json', '.scratch/roman-sources/baptismal-water-independent-review/v5-delta/review.json', '3910848d967e765856dded9d8d5e243324ae2ea6a308f3ded5f5a55fe2e6de3e')]
PROPER='src/sources/calendars/roman-1962/propers.yaml'
LATIN='src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml'
ENGLISH='src/sources/inventories/roman-1962-proper-translations-v1.toml'
TARGET=['easter-vigil','main','Blessing of the Baptismal Water','all',1]
LATIN_KEY=['easter-vigil','','Blessing of the Baptismal Water','','',1]
canon=lambda d:json.dumps(d,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
sha=lambda d:hashlib.sha256(d if isinstance(d,bytes) else canon(d)).hexdigest()
jb=lambda d:(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()

def require(test,message):
    if not test:raise ValueError(message)

def safe_path(root,path):
    p=Path(path)
    require(not p.is_absolute() and '..' not in p.parts,'Unsafe relative path')
    result=root/p
    for parent in [result,*result.parents]:
        if parent==root.parent:break
        require(not parent.is_symlink(),'Symlink in controlled path: '+str(parent))
    return result

def val(d):
    if isinstance(d,bool):return str(d).lower()
    if isinstance(d,int):return str(d)
    if isinstance(d,list):return '['+', '.join(val(x) for x in d)+']'
    require(isinstance(d,str),'Unsupported approved TOML value')
    return json.dumps(d,ensure_ascii=False)

def la_key(row):return [row.get(k) for k in ['mass','form','proper','course','cycle','occurrence']]
def en_key(row):return [row.get(k) for k in ['mass','form_id','proper','cycle','occurrence']]

def proper(doc):
    found=[p for s in doc['sections'].values() if isinstance(s,dict) for m in s.get('masses',[]) if m.get('key')==TARGET[0] for p in m.get('propers',[]) if p.get('name')==TARGET[2]]
    require(len(found)==1,'Proper identity is not unique')
    return found[0]

def one_row(doc,key,keyfn):
    found=[r for r in doc['entries'] if keyfn(r)==key]
    require(len(found)==1,'Ledger identity is not unique')
    return found[0]

def row_block(text,before,key,keyfn):
    starts=list(re.finditer(r'(?m)^\[\[?[^].\n]+\]\]?\s*\n',text));found=[]
    for i,m in enumerate(starts):
        if m.group().strip()!='[[entries]]':continue
        end=starts[i+1].start() if i+1<len(starts) else len(text)
        block=text[m.start():end];row=tomllib.loads(block)['entries'][0]
        if keyfn(row)==key:found.append((m.start(),end,block,row))
    require(len(found)==1,'Raw ledger identity is not unique')
    start,end,block,row=found[0]
    require(row==before,'Exact ledger dictionary preimage changed')
    return start,end,block

def mapping(node,key):
    require(isinstance(node,yaml.MappingNode),'Expected YAML mapping')
    found=[v for k,v in node.value if k.value==key]
    require(len(found)==1,'YAML mapping key is not unique: '+key)
    return found[0]

def proper_yaml_node(tree):
    found=[]
    for _,section in mapping(tree,'sections').value:
        if not isinstance(section,yaml.MappingNode):continue
        masses=[v for k,v in section.value if k.value=='masses']
        if not masses:continue
        for mass in masses[0].value:
            if mapping(mass,'key').value!=TARGET[0]:continue
            for p in mapping(mass,'propers').value:
                if mapping(p,'name').value==TARGET[2]:found.append(p)
    require(len(found)==1,'YAML proper node identity is not unique')
    return found[0]

def pair(a,b):return dict(before=a,after=b,before_sha256=sha(a),after_sha256=sha(b))

def adoption_controls(manifest,change):
    path=HERE/'evidence/root-source-adoption.json'
    raw=path.read_bytes();require(sha(raw)==ROOT_ADOPTION_SHA256,'Actual Root source-adoption bytes changed')
    adoption=json.loads(raw)
    require(adoption.get('schema')=='triptych-root-baptismal-water-source-adoption/v1' and adoption.get('status')=='accepted','Not the typed accepted Root water source adoption')
    require(adoption.get('target')==TARGET and adoption.get('latin_key')==LATIN_KEY,'Root adoption target mismatch')
    require(adoption['manifest']['sha256']==MANIFEST_SHA and adoption['transition']['sha256']==TRANSITION_SHA,'Root adoption candidate pins mismatch')
    require(adoption['source_files']==manifest['source_files'],'Root adoption source-six scope mismatch')
    require(adoption['owner_splices']==change['owner_splices'],'Root adoption exact owner objects differ')
    note=manifest['existing_source_metadata_change']
    require(adoption['existing_source_note']==dict(path=note['canonical_path'],before_sha256=note['before_raw_sha256'],after_sha256=note['after_raw_sha256']),'Root adoption verification-note scope mismatch')
    expected=[dict(path=source,sha256=digest) for _,source,digest in REVIEW_CONTROLS]
    require(adoption['independent_reviews']==expected,'Root adoption review set mismatch')
    for local,source,digest in REVIEW_CONTROLS:
        review_raw=(HERE/'evidence'/local).read_bytes();require(sha(review_raw)==digest,'Independent review bytes changed: '+source)
        review=json.loads(review_raw)
        verdict=review.get('verdict',review.get('status',''))
        require(isinstance(verdict,str) and verdict.startswith('PASS'),'Independent review is not a passing record')
        require(not review.get('blockers') and not review.get('blocking_errors') and not review.get('failures'),'Independent review contains blockers')
    return dict(root_source_adoption_sha256=ROOT_ADOPTION_SHA256,independent_reviews=expected,state='source-adopted-preparation-only')

def prepare(root,inputs):
    manifest_path=HERE/'candidate-manifest.json'
    require(sha(manifest_path.read_bytes())==MANIFEST_SHA,'Candidate manifest changed')
    manifest=json.loads(manifest_path.read_bytes())
    traw=(HERE/'positive-transition-proposal.json').read_bytes()
    require(sha(traw)==TRANSITION_SHA,'Transition declaration changed')
    change=json.loads(traw);before_decl=change['before'];after_decl=change['after']
    adopted=adoption_controls(manifest,change)
    require(change['target']==TARGET and change['latin_key']==LATIN_KEY,'Unapproved target identity')
    require(before_decl['english_binding']['dictionary']['translations']==after_decl['english_binding']['dictionary']['translations'],'English body/translation descriptors changed')
    before={};after={};read_controls={}
    def read(path):
        resolved=inputs.get(path)
        if resolved:
            p,digest=resolved;raw=p.read_bytes();require(sha(raw)==digest,'Input read-map pin changed: '+path)
        else:p=safe_path(root,path);raw=p.read_bytes()
        read_controls[path]=raw
        return raw
    for path in [PROPER,LATIN,ENGLISH]:before[path]=read(path)
    doc=yaml.safe_load(before[PROPER]);expected_doc=copy.deepcopy(doc)
    require(proper(doc)==before_decl['proper']['dictionary'],'Exact proper dictionary preimage changed')
    p1=after_decl['proper']['dictionary'];p0=before_decl['proper']['dictionary']
    require({k for k in set(p0)|set(p1) if p0.get(k)!=p1.get(k)}=={'text','notes'},'Undeclared proper field change')
    require(p1['text'].startswith(p0['text']),'Old Latin prefix changed')
    require(sha(p1['text'].encode())=='82487ee719c8b1b7dbcf33dcf7f855373edf43ddbc79fd1d4345dddd377d2864','Proposed Latin body changed')
    text=before[PROPER].decode();node=proper_yaml_node(yaml.compose(text));edits=[]
    for key in ['text','notes']:
        scalar=mapping(node,key)
        require(isinstance(scalar,yaml.ScalarNode),'Proper field is not scalar')
        raw=text[scalar.start_mark.index:scalar.end_mark.index]
        require(scalar.style in ['|','>'] and raw.endswith('\n'),'Unsupported YAML scalar formatting')
        if key=='text':replacement='|\n'+''.join('          '+line for line in p1[key].splitlines(keepends=True))
        else:replacement=json.dumps(p1[key],ensure_ascii=False)+'\n'
        edits.append((scalar.start_mark.index,scalar.end_mark.index,replacement))
    for start,end,replacement in sorted(edits,reverse=True):text=text[:start]+replacement+text[end:]
    after[PROPER]=text.encode();expected_proper=proper(expected_doc);expected_proper.clear();expected_proper.update(copy.deepcopy(p1))
    require(yaml.safe_load(after[PROPER])==expected_doc,'Undeclared calendar value changed')
    ldoc=tomllib.loads(before[LATIN].decode());lexpected=copy.deepcopy(ldoc)
    l0=before_decl['latin_proof_raw']['dictionary'];l1=after_decl['latin_proof_raw']['dictionary']
    require(one_row(ldoc,LATIN_KEY,la_key)==l0,'Latin row preimage changed')
    for field in ['publication_status','publication_basis','surfaces','provenance_status','relationship','provenance_authority','provenance_confidence']:
        require(l0[field]==l1[field],'Latin permission/grade changed')
    s,e,lb0=row_block(before[LATIN].decode(),l0,LATIN_KEY,la_key)
    lb1='[[entries]]\n'+'\n'.join(k+' = '+val(v) for k,v in l1.items())+'\n\n'
    after[LATIN]=(before[LATIN].decode()[:s]+lb1+before[LATIN].decode()[e:]).encode()
    lr=one_row(lexpected,LATIN_KEY,la_key);lr.clear();lr.update(copy.deepcopy(l1))
    require(tomllib.loads(after[LATIN].decode())==lexpected,'Undeclared Latin ledger value changed')
    edoc=tomllib.loads(before[ENGLISH].decode());eexpected=copy.deepcopy(edoc)
    e0=before_decl['english_binding']['dictionary'];e1=after_decl['english_binding']['dictionary']
    require({k for k in set(e0)|set(e1) if e0.get(k)!=e1.get(k)}=={'witness_note'},'English changes exceed witness_note')
    require(one_row(edoc,TARGET,en_key)==e0,'English row preimage changed')
    s,e,eb0=row_block(before[ENGLISH].decode(),e0,TARGET,en_key)
    matches=list(re.finditer(r'(?m)^witness_note = .*\n',eb0));require(len(matches)==1,'English note field not unique')
    m=matches[0];eb1=eb0[:m.start()]+'witness_note = '+val(e1['witness_note'])+'\n'+eb0[m.end():]
    require(tomllib.loads(eb1)['entries'][0]==e1,'Undeclared English row change')
    after[ENGLISH]=(before[ENGLISH].decode()[:s]+eb1+before[ENGLISH].decode()[e:]).encode()
    er=one_row(eexpected,TARGET,en_key);er.clear();er.update(copy.deepcopy(e1))
    require(tomllib.loads(after[ENGLISH].decode())==eexpected,'Undeclared English ledger value changed')
    metadata=manifest['existing_source_metadata_change'];path=metadata['canonical_path']
    before[path]=read(path);require(sha(before[path])==metadata['before_raw_sha256'],'Verification passage raw preimage changed')
    after[path]=safe_path(HERE,metadata['prepared_path']).read_bytes()
    require(sha(after[path])==metadata['after_raw_sha256'],'Verification passage postimage changed')
    old=tomllib.loads(before[path].decode());new=tomllib.loads(after[path].decode())
    require(old==metadata['before_dictionary'] and new==metadata['after_dictionary'],'Verification passage dictionary mismatch')
    require({k for k in set(old)|set(new) if old.get(k)!=new.get(k)}=={'notes'},'Verification passage change exceeds notes')
    preserved=[]
    for entry in manifest['preserved_source_controls']:
        raw=read(entry['path']);require(sha(raw)==entry['sha256'],'Preserved source drift: '+entry['path'])
        preserved.append(dict(path=entry['path'],sha256=sha(raw)))
    for entry in manifest['source_files']:
        path=entry['canonical_path'];require(path not in before,'Repeated destination')
        require(path not in inputs and not safe_path(root,path).exists(),'New source destination already exists: '+path)
        before[path]=None;after[path]=safe_path(HERE,entry['prepared_path']).read_bytes()
        require(sha(after[path])==entry['sha256'] and len(after[path])==entry['byte_size'],'New source bytes changed: '+path)
    require(len(after)==10,'Expected six new files and four existing owners')
    defaults=ldoc['defaults']
    row=dict(target=TARGET,latin_key=LATIN_KEY,proper=pair(p0,p1),latin_proof_raw_dictionary=pair(l0,l1),latin_proof_default_resolved=pair({**defaults,**l0},{**defaults,**l1}),english_binding=pair(e0,e1),latin_raw_toml_row=dict(before_sha256=sha(lb0.encode()),after_sha256=sha(lb1.encode())),english_raw_toml_row=dict(before_sha256=sha(eb0.encode()),after_sha256=sha(eb1.encode())),latin_body=pair(p0['text'],p1['text']),english_body_sha256=sha(e0['translations'][0]['text'].encode()))
    # Body hashes are raw UTF-8, unlike the full dictionary hashes above.
    row['latin_body']['before_sha256']=sha(p0['text'].encode());row['latin_body']['after_sha256']=sha(p1['text'].encode())
    readmap=dict(schema='triptych-baptismal-water-source-adopted-read-map/v1',authority='Source-adopted preparation only; Root owns exact fresh installation and source_epoch transition.',source_adoption=adopted,candidate_manifest_sha256=MANIFEST_SHA,transition_sha256=TRANSITION_SHA,driver_sha256=sha(Path(__file__).read_bytes()),hash_serialization="Dictionary SHA256 uses ensure_ascii=False, sort_keys=True, separators=(',',':'); body/file/row hashes use exact UTF-8 bytes.",rows=[row],files=[dict(canonical_path=p,postimage_path='postimages/'+p,before_sha256=sha(before[p]) if before[p] is not None else None,after_sha256=sha(after[p]),byte_size=len(after[p])) for p in sorted(after)],preserved_files=preserved,invariants=dict(exact_old_latin_prefix=True,english_body_payload_rights_locators_unchanged=True,english_binding_note_only=True,verification_passage_note_only=True,ordinary_frames_unchanged=True,all_unrelated_owner_values_and_bytes_preserved=True,source_six_bytes_match_v1=True,no_other_holy_week_or_native_ending_changes=True))
    patch=''.join(''.join(difflib.unified_diff((before[p] or b'').decode().splitlines(True),after[p].decode().splitlines(True),fromfile='a/'+p if before[p] is not None else '/dev/null',tofile='b/'+p)) for p in sorted(after))
    return before,after,readmap,patch,read_controls

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True,help='Fresh repository scratch directory for postimages/read-map')
    ap.add_argument('--read-map',type=Path,help='Optional prior staged map: files[].canonical_path/postimage_path/after_sha256; reads only')
    args=ap.parse_args();root=args.root.resolve();out=args.out.resolve()
    require('.scratch' in out.relative_to(root).parts,'Output must be inside root scratch')
    require(not out.exists(),'Output directory must be fresh')
    inputs={}
    if args.read_map:
        mp=args.read_map.resolve();record=json.loads(mp.read_bytes())
        for row in record['files']:
            key=row['canonical_path'];require(key not in inputs,'Duplicate input map identity')
            inputs[key]=(safe_path(mp.parent,row['postimage_path']),row['after_sha256'])
    before,after,readmap,patch,controls=prepare(root,inputs)
    serialized=jb(readmap);digest=sha(serialized)
    # A read-only map must still describe one stable set of exact input bytes.
    for path,raw in controls.items():
        p=inputs[path][0] if path in inputs else safe_path(root,path)
        require(p.read_bytes()==raw,'Input changed during preparation: '+path)
    for path,raw in before.items():
        if raw is None:require(not safe_path(root,path).exists(),'New source appeared during preparation: '+path)
    for p,raw in after.items():
        dest=out/'postimages'/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
    (out/'read-map.json').write_bytes(serialized);(out/'source-owner.patch').write_text(patch)
    receipt=dict(status='source-adopted-prepared-only',read_map_sha256=digest,root_source_adoption_sha256=ROOT_ADOPTION_SHA256,files=len(after),root_writes=0)
    (out/'receipt.json').write_bytes(jb(receipt));print(json.dumps(receipt))

if __name__=='__main__':main()
