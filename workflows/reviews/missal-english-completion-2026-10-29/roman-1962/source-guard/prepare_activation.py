#!/usr/bin/env python3
"""Prepare pending finite-authority metadata; never install, adopt, or activate."""
from __future__ import annotations
import argparse
from collections import OrderedDict
from hashlib import sha256
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tomllib
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
OWN = ROOT / '.scratch/roman-english-completion-20261029/finite-guard'
BASE = '6aeb96a392a61e216310c3bf71834863afb229f8'
AUTHORITY = 'workflows/reviews/missal-english-completion-2026-10-29/roman-1962/finite-latin-authority-v1.json'
METHOD = 'english-completion-20261029-finite-latin-v1'
KEYS = ('mass','form','proper','course','cycle','occurrence')
BASIS = 'qualified-nonoriginal-adaptation'
TYPES = {'work','edition','artifact','segment','passage','corpus'}
IDENTIFIER = re.compile(r'^(work|edition|artifact|segment|passage|corpus)\.[a-z0-9.-]+$')
NOTICE = ('Qualified United States editorial assessment of this exact adaptation under publication policy section 1 priority 6; moderate confidence. The source record preserves the opposing originality argument. This is not holder permission or an unqualified public-domain claim. Triptych owns only its editorial carrier.')


def h(value): return sha256(value).hexdigest()
def canonical(value): return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',',':')).encode()
def dh(value): return h(canonical(value))
def rel(path): return Path(path).resolve().relative_to(ROOT).as_posix()
def safe_path(value):
    p = PurePosixPath(value)
    if p.is_absolute() or any(x in {'','.','..'} for x in p.parts): raise ValueError('noncanonical path: '+str(value))
    return p.as_posix()
def read_local(value):
    p=ROOT/safe_path(value)
    if p.is_symlink() or not p.resolve().is_relative_to(ROOT): raise ValueError('path escapes repository: '+value)
    return p.read_bytes()
def load_tool(name):
    loader=SourceFileLoader('activation_'+name.replace('-','_'),str(ROOT/'tools'/name)); spec=spec_from_loader(loader.name,loader)
    module=module_from_spec(spec);sys.modules[spec.name]=module;loader.exec_module(module);return module


class GitSnapshot:
    def __init__(self, revision):
        self.revision=subprocess.check_output(['git','rev-parse','--verify',revision+'^{commit}'],cwd=ROOT,text=True).strip()
        raw=subprocess.check_output(['git','ls-tree','-r','-l','-z',self.revision,'src/sources','workflows/reviews/missal-reader-completion-2026-10-26'],cwd=ROOT)
        self.tree={}
        for item in raw.split(b'\0'):
            if not item: continue
            head,path=item.split(b'\t',1);mode,kind,oid,size=head.split()
            self.tree[path.decode()]={'mode':mode.decode(),'oid':oid.decode(),'size':int(size)}
        self.proc=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        self.cache=OrderedDict();self.cache_size=0;self.bytes_read=0;self.blobs_read=0
    def close(self):
        self.proc.stdin.close();self.proc.wait()
    def read(self,path):
        path=safe_path(path)
        if path in self.cache: self.cache.move_to_end(path);return self.cache[path]
        meta=self.tree[path]
        if meta['mode'] not in {'100644','100755'}: raise ValueError('unsupported immutable input mode: '+path)
        self.proc.stdin.write((meta['oid']+'\n').encode());self.proc.stdin.flush()
        header=self.proc.stdout.readline().split()
        if len(header)!=3 or header[0].decode()!=meta['oid'] or header[1]!=b'blob': raise ValueError('git blob protocol failed: '+path)
        size=int(header[2]);data=self.proc.stdout.read(size)
        if len(data)!=size or self.proc.stdout.read(1)!=b'\n': raise ValueError('short immutable blob: '+path)
        self.bytes_read+=size;self.blobs_read+=1
        if size<=32*1024*1024:
            self.cache[path]=data;self.cache_size+=size
            while self.cache_size>128*1024*1024:
                _,old=self.cache.popitem(last=False);self.cache_size-=len(old)
        return data
    def record_files(self):
        return [p for p in sorted(self.tree) if p.endswith('.toml') and (p.startswith('src/sources/works/') or p.startswith('src/sources/corpora/'))]


def add_record(records,locations,path,data):
    rid=data.get('id')
    if data.get('record_type') not in TYPES or not isinstance(rid,str): return
    if rid in records: raise ValueError('duplicate source identity at '+locations[rid]+' and '+path+': '+rid)
    records[rid]=data;locations[rid]=path


def dependencies(tool, records, rid):
    record=records[rid]
    owned=tool.Record(Path(rid),record['record_type'],rid,record)
    result=set(tool._dependency_ids(owned))
    result.update(record.get('projected_from') or [])
    if record.get('record_type')=='work': result.update(record.get('relations') or [])
    return result


def closure(tool,records,seeds):
    seen=set();todo=list(seeds)
    while todo:
        rid=todo.pop()
        if rid in seen: continue
        if rid not in records: raise ValueError('missing controller: '+rid)
        seen.add(rid);todo.extend(dependencies(tool,records,rid)-seen)
    return seen


def identifiers(value):
    if isinstance(value,str): return {value} if IDENTIFIER.fullmatch(value) else set()
    if isinstance(value,list): return set().union(*(identifiers(x) for x in value)) if value else set()
    if isinstance(value,dict): return set().union(*(identifiers(x) for x in value.values())) if value else set()
    return set()


def artifact_for(records,passage):
    if passage.get('segment_id'): return records[records[passage['segment_id']]['artifact_id']]
    return records[passage['artifact_id']]


def selected_text(passage,artifact,payload):
    if isinstance(passage.get('text'),str) and passage['text'].strip(): return passage['text']
    ranges=passage.get('physical_line_ranges')
    if not ranges or not artifact.get('media_type','').startswith('text/plain'): return None
    lines=payload.decode('utf-8').split('\n');selected=[]
    for first,last in ranges:
        if isinstance(first,bool) or not isinstance(first,int) or not 1<=first<=last<=len(lines): raise ValueError('invalid physical range')
        selected.extend(lines[first-1:last])
    return '\n'.join(selected)


def controller_payload(records,artifact,read):
    path=artifact.get('path')
    if artifact.get('storage')!='tracked' or not path: raise ValueError('expected tracked controller '+artifact['id'])
    payload=read(path)
    if h(payload)!=artifact.get('sha256') or len(payload)!=artifact.get('byte_size'): raise ValueError('controller payload mismatch '+artifact['id'])
    return payload


def library(tool,root,records,locations):
    lib=tool.Library(root,root/'src/sources',[])
    for rid,data in records.items():
        path=root/locations[rid]
        common=tool._validate_common_record(lib,path,data)
        if common is None: continue
        record=tool.Record(path,*common,data);lib.records[rid]=record
        tool._validate_strings(lib,record);tool._validate_record_path(lib,record)
    for check in (tool._validate_relationships,tool._validate_cycles,tool._validate_work_dates,tool._validate_loci): check(lib)
    if lib.errors: raise ValueError('source graph refused: '+json.dumps(lib.errors[:8]))
    return lib


def write_bounded_baseline(tool,snapshot,records,locations,seeds,root):
    wanted=closure(tool,records,seeds)
    for rid in wanted:
        p=root/locations[rid];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(snapshot.read(locations[rid]))
        record=records[rid]
        if record.get('record_type')=='artifact' and record.get('storage')=='tracked':
            data=controller_payload(records,record,snapshot.read);p=root/record['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    lib=library(tool,root,{k:records[k] for k in wanted},{k:locations[k] for k in wanted})
    for check in (tool._validate_artifacts,tool._validate_support_artifact_references,tool._validate_passage_locators,tool._validate_artifact_licenses): check(lib)
    if lib.errors: raise ValueError('baseline collision closure refused: '+json.dumps(lib.errors[:8]))
    return sorted(wanted)


def pointer_hashes(value,target,pointer=''):
    hits=[]
    if isinstance(value,dict):
        for key,item in value.items(): hits+=pointer_hashes(item,target,pointer+'/'+str(key).replace('~','~0').replace('/','~1'))
    elif isinstance(value,list):
        for i,item in enumerate(value): hits+=pointer_hashes(item,target,pointer+'/'+str(i))
    elif value==target: hits.append(pointer)
    return hits


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--plan',action='append',required=True)
    ap.add_argument('--receipt',action='append',default=[])
    ap.add_argument('--baseline-ref',default=BASE)
    ap.add_argument('--allow-pending-receipts',action='store_true')
    ap.add_argument('--pending-target',action='append',default=[])
    ap.add_argument('--out',required=True)
    compiler_start_sha256=h(Path(__file__).read_bytes())
    args=ap.parse_args();out=ROOT/safe_path(args.out)
    if not out.resolve().is_relative_to(OWN): raise ValueError('output must remain under owned finite-guard scratch')
    out.mkdir(parents=True,exist_ok=False)
    tool=load_tool('source-library');reader=load_tool('source-reader')
    current={};locations={};local_pins={};initial_manifest_pins={};manifest_map={}
    for code in ['tools/source-library','tools/source-reader','scripts/_proper_latin.py','scripts/_proper_qualified_latin.py','scripts/_proper_finite_latin_20261029.py']:local_pins[code]=h(read_local(code))
    for p in sorted((ROOT/'src/sources').rglob('*.toml')):
        if p.is_symlink(): raise ValueError('source metadata symlink')
        data=p.read_bytes();parsed=tomllib.loads(data.decode());relative=p.relative_to(ROOT).as_posix();initial_manifest_pins[relative]=h(data);manifest_map[relative]=parsed
    current_metadata_snapshot={'selection':'Every recursive *.toml regular nonsymlink file below src/sources, keyed by repository-relative POSIX path; values are exact file-byte SHA256; map serialized as sorted compact ensure_ascii=False UTF8 JSON.','file_count':len(initial_manifest_pins),'canonical_path_sha256_map_sha256':dh(initial_manifest_pins)}
    initial_records={};initial_locations={}
    for path,parsed in sorted(manifest_map.items()):add_record(initial_records,initial_locations,path,parsed)
    overlays={};plans=[];rows=[];holds=[];receipts=[];plan_review_conditions={}
    for value in args.plan:
        data=read_local(value);plan=json.loads(data);plans.append({'path':value,'sha256':h(data),'state':plan.get('state',plan.get('status'))})
        plan_review_conditions[value]={key:plan[key]for key in ('final_source_assembly_review_state',)if key in plan}
        for file in plan.get('source_files',[]):
            path=safe_path(file['repository_path']);candidate=file['candidate_path'];payload=read_local(candidate)
            if h(payload)!=file['sha256']: raise ValueError('plan file pin failed: '+candidate)
            if path in overlays and overlays[path]['sha256']!=h(payload): raise ValueError('plan postimages conflict: '+path)
            overlays[path]={'candidate_path':candidate,'sha256':h(payload)};local_pins[candidate]=h(payload)
            if path.endswith('.toml'):
                parsed=tomllib.loads(payload.decode());manifest_map[path]=parsed
        for row in plan.get('rows',[]): rows.append((value,row))
        holds.append({'plan':value,'pointer':'/holds','canonical_sha256':dh(plan.get('holds')),'count':len(plan.get('holds') or [])})
    for path,parsed in sorted(manifest_map.items()):
        rid=parsed.get('id')
        if parsed.get('record_type') in TYPES and isinstance(rid,str):
            if rid in current:raise ValueError('merged tree duplicates source id at '+locations[rid]+' and '+path+': '+rid)
            current[rid]=parsed;locations[rid]=path
    def future_read(path):
        if path in overlays:
            payload=read_local(overlays[path]['candidate_path'])
            if h(payload)!=overlays[path]['sha256']:raise ValueError('planned postimage changed: '+path)
            return payload
        payload=read_local(path)
        if path in initial_manifest_pins and h(payload)!=initial_manifest_pins[path]:raise ValueError('used controller metadata changed: '+path)
        local_pins[path]=h(payload);return payload
    for value in args.receipt:
        data=read_local(value);receipts.append({'path':value,'sha256':h(data),'value':json.loads(data)});local_pins[value]=h(data)
    defaults_path='src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml';defaults_bytes=read_local(defaults_path);local_pins[defaults_path]=h(defaults_bytes);defaults=tomllib.loads(defaults_bytes.decode())['defaults']
    scopes=[];case_links=[];outside=[];seen=set();controller_payload_checks={}
    for plan_path,row in rows:
        provenance={**defaults,**row['latin_provenance']};identity=[provenance[k] for k in KEYS]
        if tuple(identity) in seen: raise ValueError('duplicate target in plans: '+repr(identity))
        seen.add(tuple(identity));body=row['new_proper']['text'];body_sha=h(body.encode())
        if body_sha!=provenance['text_sha256']: raise ValueError('plan target body hash failed')
        if provenance['publication_basis']!=BASIS:
            outside.append({'identity':row['identity'],'body_sha256':body_sha,'publication_basis':provenance['publication_basis'],'plan':plan_path});continue
        source=current[provenance['source_id']];artifact=artifact_for(current,source)
        payload=controller_payload(current,artifact,future_read);selected=selected_text(source,artifact,payload)
        if selected is None or h((selected+'\n').encode())!=body_sha: raise ValueError('selected projection does not equal complete target: '+repr(identity))
        if source.get('artifact_id')!=artifact['id'] or not source.get('physical_line_ranges'): raise ValueError('finite source requires direct physical-line passage')
        seeds={source['id'],artifact['id'],provenance['verification_source_id']}|set(provenance['publication_source_ids'])
        for field in ('conclusion_controllers','source_range_controls','source_record','projection_passage_record','pd_source_artifact_id','pd_source_passage_id','source_base_controller_id','source_base_artifact_id'):seeds.update(identifiers(row.get(field)))
        bound=closure(tool,current,seeds)
        inherited=dict(provenance,publication_status='unresolved',publication_basis='unresolved',surfaces=[],note='Provenance inherited from roman-1962; target-recension attestation for roman-pre-1955 is not established.')
        scope={'key':identity,'row_sha256':dh(provenance),'inherited_row_sha256':dh(inherited),'body_sha256':body_sha,'artifact_payload_sha256':h(payload),'source_id':source['id'],'artifact_id':artifact['id'],'verification_source_id':provenance['verification_source_id'],'publication_source_ids':provenance['publication_source_ids'],'projected_from':artifact['projected_from'],'physical_line_ranges':source['physical_line_ranges'],'record_sha256':{rid:dh(current[rid])for rid in sorted(bound)},'public_notice':row.get('public_notice',NOTICE)}
        scopes.append(scope)
        for rid in bound:
            path=locations[rid]
            raw_record=future_read(path)
            if tomllib.loads(raw_record.decode())!=current[rid]:raise ValueError('merged controller differs from actual postimage: '+rid)
            if path not in overlays: local_pins[path]=h(raw_record)
            controller=current[rid]
            if controller.get('record_type')=='artifact' and rid not in controller_payload_checks:
                check={'id':rid,'record_sha256':dh(controller),'storage':controller.get('storage'),'registered_payload_sha256':controller.get('sha256'),'registered_byte_size':controller.get('byte_size')}
                if controller.get('storage')=='tracked':
                    actual=controller_payload(current,controller,future_read)
                    check.update(state='actual-postimage-bytes-verified',path=controller['path'],actual_payload_sha256=h(actual),actual_byte_size=len(actual))
                else:check['state']='registered-remote-metadata-pinned-no-byte-verification-claim'
                controller_payload_checks[rid]=check
        english=row.get('english');links={'identity':row['identity'],'body_sha256':body_sha,'english_sha256':h(english.encode())if isinstance(english,str)else row.get('english_sha256'),'plan':plan_path,'row_review':None,'plan_review_conditions':plan_review_conditions[plan_path],'body_bound_receipt_links':[]}
        if row.get('review_path'):
            try:
                data=read_local(row['review_path'])
            except FileNotFoundError:
                if not args.allow_pending_receipts:raise
                data=None
            if data is None:
                links['row_review']={'path':row['review_path'],'expected_sha256':row.get('review_sha256'),'state':'pending-unavailable'}
            else:
                if h(data)!=row.get('review_sha256'):raise ValueError('source review pin failed')
                local_pins[row['review_path']]=h(data);links['row_review']={'path':row['review_path'],'sha256':h(data),'state':'exact-file-pinned-not-role-or-merits-judged'}
        for receipt in receipts:
            pointers=pointer_hashes(receipt['value'],body_sha)
            if pointers:links['body_bound_receipt_links'].append({'path':receipt['path'],'sha256':receipt['sha256'],'body_hash_pointers':pointers})
        case_links.append(links)
    scopes.sort(key=lambda x:x['key']);body_hashes={x['body_sha256']for x in scopes};payload_hashes={x['artifact_payload_sha256']for x in scopes}
    source_ids={x['source_id']for x in scopes};artifact_ids={x['artifact_id']for x in scopes}
    marker=lambda value:isinstance(value,str)and(METHOD in value or AUTHORITY in value)
    def artifact_matches(artifact):
        return {'identity':artifact.get('id')in artifact_ids,'payload':artifact.get('sha256')in payload_hashes,'marker':any(marker(artifact.get(field))for field in ('rights_basis','notes'))}
    snap=GitSnapshot(args.baseline_ref)
    try:
        baseline={};base_paths={}
        for path in snap.record_files():add_record(baseline,base_paths,path,tomllib.loads(snap.read(path).decode()))
        base_root=out/'baseline-validation-root';base_root.mkdir()
        lib=library(tool,base_root,baseline,base_paths)
        # The exact initial legacy authority is needed only by its old reader route.
        import _proper_qualified_latin as Q
        for path in (Q.ADOPTION_PATH,Q.RIGHTS_PATH):
            p=base_root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(snap.read(path))
        for scope in Q.SCOPES:
            artifact=baseline[scope['artifact_id']];p=base_root/artifact['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(controller_payload(baseline,artifact,snap.read))
        prior_rows=[];prior_artifacts=[];prior_readings=[];collision_proofs=[];validated=set();captured_ids=set();readable_by_artifact={};read_counts={'passages':0,'readable':0,'body_collisions':0,'payload_collisions':0,'artifact_classifier_captures':0,'passage_identity_collisions':0};lines_cache={}
        def baseline_lines(library_,artifact):
            rid=artifact['id']
            if rid not in lines_cache:lines_cache[rid]=controller_payload(baseline,artifact,snap.read).decode('utf-8').split('\n')
            return lines_cache[rid]
        def validate(seeds):
            ids=write_bounded_baseline(tool,snap,baseline,base_paths,seeds,base_root);validated.update(ids);return ids
        for artifact in (r for r in baseline.values()if r.get('record_type')=='artifact'):
            matches=artifact_matches(artifact)
            if not any(matches.values()):continue
            if artifact.get('storage')!='tracked' or artifact.get('rights_status')not in reader.DISTRIBUTABLE_RIGHTS:raise ValueError('baseline artifact classifier capture needs an independently validated supported prior carrier: '+artifact['id'])
            ids=validate({artifact['id']});controller_payload(baseline,artifact,snap.read)
            prior_artifacts.append({'artifact_record_sha256':dh(artifact),'payload_sha256':artifact['sha256']});captured_ids.add(artifact['id']);read_counts['payload_collisions']+=int(matches['payload']);read_counts['artifact_classifier_captures']+=1
            collision_proofs.append({'kind':'artifact','id':artifact['id'],'classifier_matches':matches,'manifest_path':base_paths[artifact['id']],'manifest_git_oid':snap.tree[base_paths[artifact['id']]]['oid'],'payload_path':artifact['path'],'payload_git_oid':snap.tree[artifact['path']]['oid'],'validated_record_ids':ids})
        with patch.object(reader,'_payload_lines',side_effect=baseline_lines):
            passages=sorted((r for r in baseline.values()if r.get('record_type')=='passage'),key=lambda r:(r.get('artifact_id',''),r['id']))
            for passage in passages:
                read_counts['passages']+=1;result=reader.reading_of(lib,passage)
                if not result.get('readable'):continue
                read_counts['readable']+=1;digest=h((result['text']+'\n').encode());artifact=artifact_for(baseline,passage)
                readable_by_artifact.setdefault(artifact['id'],[]).append((passage,digest))
                if digest not in body_hashes and passage['id']not in source_ids:continue
                artifact=artifact_for(baseline,passage);captured_ids.add(artifact['id']);ids=validate({passage['id']});controller_payload(baseline,artifact,snap.read)
                prior_artifacts.append({'artifact_record_sha256':dh(artifact),'payload_sha256':artifact['sha256']});prior_readings.append({'artifact_record_sha256':dh(artifact),'passage_record_sha256':dh(passage),'body_sha256':digest});read_counts['body_collisions']+=int(digest in body_hashes);read_counts['passage_identity_collisions']+=int(passage['id']in source_ids)
                collision_proofs.append({'kind':'reading','id':passage['id'],'body_sha256':digest,'manifest_path':base_paths[passage['id']],'manifest_git_oid':snap.tree[base_paths[passage['id']]]['oid'],'artifact_id':artifact['id'],'artifact_manifest_git_oid':snap.tree[base_paths[artifact['id']]]['oid'],'payload_git_oid':snap.tree[artifact['path']]['oid'],'validated_record_ids':ids})
        # Capturing a prior carrier changes every reading on it, not only the matching body.
        for artifact_id in sorted(captured_ids):
            artifact=baseline[artifact_id]
            for passage,digest in readable_by_artifact.get(artifact_id,[]):
                ids=validate({passage['id']})
                prior_readings.append({'artifact_record_sha256':dh(artifact),'passage_record_sha256':dh(passage),'body_sha256':digest})
                collision_proofs.append({'kind':'captured-carrier-readable-closure','id':passage['id'],'body_sha256':digest,'artifact_id':artifact_id,'manifest_git_oid':snap.tree[base_paths[passage['id']]]['oid'],'validated_record_ids':ids})
        # Check every direct calendar ledger against the complete row classifier.
        import _proper_latin as L
        import yaml
        signatures={'keys':{tuple(x['key'])for x in scopes},'source_ids':{x['source_id']for x in scopes},'artifact_ids':{x['artifact_id']for x in scopes}}
        row_scan={'direct_sidecars':{},'classifier_matches':[],'target_override_rows':0,'target_override_matches':[]}
        def row_matches(row):
            return {'key':tuple(row.get(k)for k in KEYS)in signatures['keys'],'body':row.get('text_sha256')in body_hashes,'source':row.get('source_id')in signatures['source_ids'],'carrier':bool(set(row.get('publication_source_ids')or [])&signatures['artifact_ids']),'marker':any(marker(row.get(field))for field in ('publication_authority','publication_evidence','note'))}
        for row_path in sorted(p for p in snap.tree if p.endswith('-proper-latin-provenance-v1.toml')):
            table=tomllib.loads(snap.read(row_path).decode());calendar=table['calendar'];row_scan['direct_sidecars'][calendar]=len(table.get('entries',[]))
            for raw in table.get('entries',[]):
                row={**table['defaults'],**raw};matches=row_matches(row)
                if not any(matches.values()):continue
                row_scan['classifier_matches'].append({'calendar':calendar,'key':[row.get(k)for k in KEYS],'row_sha256':dh(row),'matches':matches,'publication_status':row.get('publication_status'),'prior_admitted_route':row.get('publication_status')=='permitted'})
                if row.get('publication_status')!='permitted':continue
                seeds={row['source_id'],row['verification_source_id'],*row['publication_source_ids']};ids=validate(seeds)
                trouble=L._row_problems('baseline prior route',row)+L._source_record_problems('baseline prior route',row,baseline,authority_root=base_root,effective_calendar=calendar)
                if trouble:raise ValueError('prior row source qualification refused: '+json.dumps(trouble))
                calendar_path='src/sources/calendars/'+calendar+'/propers.yaml'
                text_nodes=dict(L.text_owners(yaml.safe_load(snap.read(calendar_path))))
                key=L.LatinKey.from_mapping(row)
                if key not in text_nodes or h(text_nodes[key].encode())!=row['text_sha256']:raise ValueError('baseline prior row actual Latin mismatch')
                prior_rows.append(dh(row))
                inherited=None
                if calendar=='roman-1962':
                    inherited=dict(row,publication_status='unresolved',publication_basis='unresolved',surfaces=[],note='Provenance inherited from roman-1962; target-recension attestation for roman-pre-1955 is not established.');prior_rows.append(dh(inherited))
                collision_proofs.append({'kind':'row','calendar':calendar,'key':[row[k]for k in KEYS],'row_sha256':dh(row),'inherited_row_sha256':dh(inherited)if inherited else None,'sidecar_git_oid':snap.tree[row_path]['oid'],'calendar_git_oid':snap.tree[calendar_path]['oid'],'validated_record_ids':ids})
        for override_path in sorted(p for p in snap.tree if p.endswith('-proper-target-overrides-v1.toml')):
            table=tomllib.loads(snap.read(override_path).decode())
            for entry in table.get('entries',[]):
                row=entry['provenance'];row_scan['target_override_rows']+=1;matches=row_matches(row)
                if any(matches.values()):row_scan['target_override_matches'].append({'path':override_path,'key':[row.get(k)for k in KEYS],'matches':matches})
        if row_scan['target_override_matches']:raise ValueError('prior target-override collision needs its owning effective-context proof; refusing an inferred exemption')
        unique=lambda xs:sorted({canonical(x).decode():x for x in xs}.values(),key=lambda x:canonical(x))
        routes={'row_sha256':sorted(set(prior_rows)),'artifacts':unique(prior_artifacts),'readings':unique(prior_readings)}
        authority={'schema':'triptych-finite-latin-authority/v1','method_id':METHOD,'state':'pending-root-adoption','authority_boundary':'Proposed exact scope only. This compiler performs no rights judgment, adoption, installation or code activation.','baseline_commit':snap.revision,'prior_routes':routes,'scopes':scopes,'case_evidence':case_links,'outside_qualified_scope':outside,'excluded_hold_records':holds,'excluded_pending_targets':[json.loads(x)for x in args.pending_target],'plan_pins':plans}
        (out/'candidate-authority.json').write_text(json.dumps(authority,indent=2,ensure_ascii=False)+'\n')
        proof={'schema':'triptych-finite-prior-route-proof/v1','state':'pending-root-review','baseline_commit':snap.revision,'baseline_source_records':len(baseline),'baseline_structural_validation':'source-library common/string/path/relationship/cycle/work-date/locus checks; not a whole-5.7GB payload-validation claim','prior_collision_validation':'Each collision closure additionally passes actual immutable payload hashes, source-library artifact/support/passage/license validators and the owning baseline reader or per-body Latin source checks.','baseline_reading_scan':read_counts,'baseline_row_classifier_scan':row_scan,'captured_carrier_count':len(captured_ids),'captured_carrier_readings_closed':sum(len(readable_by_artifact.get(aid,[]))for aid in captured_ids),'prior_route_counts':{k:len(v)for k,v in routes.items()},'collision_proofs':collision_proofs,'validated_collision_records':{rid:dh(baseline[rid])for rid in sorted(validated)},'snapshot_io':{'blobs':snap.blobs_read,'bytes':snap.bytes_read},'no_empty_prior_routes_inference':'Rows, full carrier hashes and every readable selected passage were scanned separately; an empty result is measured, never inferred from the Latin ledger alone.'}
        (out/'prior-route-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
    finally:snap.close()
    current_diagnosis={'schema':'triptych-current-finite-route-diagnosis/v1','state':'diagnostic-only-no-exemptions','metadata_snapshot':current_metadata_snapshot,'automatic_prior_route_additions':False,'alias_candidates':[]}
    try:
        current_lib=library(tool,ROOT,initial_records,initial_locations)
        current_diagnosis['structural_graph']='validated-current-metadata-snapshot'
    except ValueError as error:
        current_diagnosis['structural_graph']='unsettled-refused'
        current_diagnosis['graph_error']=str(error)
        current_lib=tool.Library(ROOT,ROOT/'src/sources',[])
        current_lib.records={rid:tool.Record(ROOT/initial_locations[rid],data['record_type'],rid,data)for rid,data in initial_records.items()}
    current_lines_cache={};current_readings={};current_captured=set()
    def current_bytes(path):
        payload=read_local(path)
        if path in initial_manifest_pins and h(payload)!=initial_manifest_pins[path]:raise ValueError('current diagnostic metadata drift: '+path)
        local_pins[path]=h(payload);return payload
    def current_lines(library_,artifact):
        rid=artifact['id']
        if rid not in current_lines_cache:current_lines_cache[rid]=controller_payload(initial_records,artifact,current_bytes).decode('utf-8').split('\n')
        return current_lines_cache[rid]
    current_counts={'passages':0,'readable':0,'body_collisions':0,'payload_collisions':0,'artifact_classifier_captures':0,'passage_identity_collisions':0}
    for artifact in (r for r in initial_records.values()if r.get('record_type')=='artifact'):
        matches=artifact_matches(artifact)
        if any(matches.values()):
            current_captured.add(artifact['id']);current_counts['payload_collisions']+=int(matches['payload']);current_counts['artifact_classifier_captures']+=1
            check={'kind':'artifact','id':artifact['id'],'classifier_matches':matches,'artifact_record_sha256':dh(artifact),'registered_payload_sha256':artifact.get('sha256'),'root_proof_required':True}
            if artifact.get('storage')=='tracked':check['actual_payload_sha256']=h(controller_payload(initial_records,artifact,current_bytes))
            current_diagnosis['alias_candidates'].append(check)
    with patch.object(reader,'_payload_lines',side_effect=current_lines):
        for passage in sorted((r for r in initial_records.values()if r.get('record_type')=='passage'),key=lambda r:(r.get('artifact_id',''),r['id'])):
            current_counts['passages']+=1;result=reader.reading_of(current_lib,passage)
            if not result.get('readable'):continue
            current_counts['readable']+=1;digest=h((result['text']+'\n').encode());artifact=artifact_for(initial_records,passage)
            current_readings.setdefault(artifact['id'],[]).append((passage,digest))
            if digest not in body_hashes and passage['id']not in source_ids:continue
            controller_payload(initial_records,artifact,current_bytes);current_captured.add(artifact['id']);current_counts['body_collisions']+=int(digest in body_hashes);current_counts['passage_identity_collisions']+=int(passage['id']in source_ids)
            current_diagnosis['alias_candidates'].append({'kind':'reading','id':passage['id'],'passage_record_sha256':dh(passage),'body_sha256':digest,'artifact_id':artifact['id'],'artifact_record_sha256':dh(artifact),'root_proof_required':True})
    current_diagnosis['captured_carrier_readable_closure']=[{'artifact_id':aid,'passage_id':p['id'],'artifact_record_sha256':dh(initial_records[aid]),'passage_record_sha256':dh(p),'body_sha256':digest}for aid in sorted(current_captured)for p,digest in current_readings.get(aid,[])]
    current_diagnosis['scan']=current_counts
    current_diagnosis['exemption_boundary']='Current aliases, if any, are only leads. Root must separately bind independently accepted source evidence before any prior-route pin; a current rights token or a readable result supplies no automatic exemption.'
    (out/'current-route-diagnosis.json').write_text(json.dumps(current_diagnosis,indent=2)+'\n')
    for path,expected in local_pins.items():
        if h(read_local(path))!=expected:raise ValueError('used source input changed during preparation: '+path)
    for one in plans:
        if h(read_local(one['path']))!=one['sha256']:raise ValueError('plan changed during preparation')
    final_metadata_paths=sorted((ROOT/'src/sources').rglob('*.toml'))
    if {p.relative_to(ROOT).as_posix()for p in final_metadata_paths}!=set(initial_manifest_pins):raise ValueError('current diagnostic metadata inventory changed during preparation')
    for p in final_metadata_paths:
        if p.is_symlink()or not p.resolve().is_relative_to(ROOT)or h(p.read_bytes())!=initial_manifest_pins[p.relative_to(ROOT).as_posix()]:raise ValueError('current diagnostic metadata snapshot changed during preparation: '+p.relative_to(ROOT).as_posix())
    if h(Path(__file__).read_bytes())!=compiler_start_sha256:raise ValueError('compiler source changed during preparation')
    declaration={'schema':'triptych-finite-activation-preparation/v1','state':'pending-root-adoption','compiler_sha256':compiler_start_sha256,'current_metadata_snapshot':current_metadata_snapshot,'current_metadata_final_inventory_and_content_recheck':True,'inputs':[{'path':p,'sha256':v}for p,v in sorted(local_pins.items())],'plans':plans,'receipts':[{'path':x['path'],'sha256':x['sha256']}for x in receipts],'controller_payload_checks':[controller_payload_checks[rid]for rid in sorted(controller_payload_checks)],'outputs':[{'path':rel(p),'sha256':h(p.read_bytes())}for p in sorted(out.glob('*.json'))],'qualified_scopes':len(scopes),'outside_qualified_scope':len(outside),'prior_routes':{k:len(v)for k,v in routes.items()},'activation_performed':False,'code_or_authority_mutation':False,'allow_pending_receipts':args.allow_pending_receipts,'pending_source_reviews':[x['identity']for x in case_links if x['row_review'] is None or x['row_review'].get('state')=='pending-unavailable' or 'pending' in x['plan_review_conditions'].get('final_source_assembly_review_state','').lower()],'unbound_body_receipts':[x['identity']for x in case_links if not x['body_bound_receipt_links']],'receipt_binding_boundary':'Exact body-hash pointer links only. Neither file names, generic row review pins nor matching hashes infer a receipt role, completed source review, rights recommendation, or adoption.'}
    (out/'declaration.json').write_text(json.dumps(declaration,indent=2)+'\n')
    print(json.dumps({'state':declaration['state'],'qualified_scopes':len(scopes),'prior_routes':declaration['prior_routes'],'out':rel(out)}))

if __name__=='__main__':
    try:main()
    except Exception as error:
        print('prepare_activation refused: '+str(error),file=sys.stderr);raise SystemExit(1)
