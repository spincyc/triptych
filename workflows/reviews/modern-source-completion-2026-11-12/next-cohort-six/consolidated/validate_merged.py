from pathlib import Path
import copy,csv,hashlib,importlib.machinery,importlib.util,json,os,sys,tomllib
H=Path(__file__).resolve().parent;R=H.parents[1];V=H/'dry-run-final-root'
os.environ['TRIPTYCH_SOURCE_LIBRARY_CACHE']='0';os.environ['TRIPTYCH_LIBRARY_CACHE']='0';os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.path.insert(0,str(R/'scripts'))
import _proper_latin as latin,_calendars as cal,_missal_coverage as coverage
def load(name,p):
 l=importlib.machinery.SourceFileLoader(name,str(p));s=importlib.util.spec_from_loader(name,l);m=importlib.util.module_from_spec(s);sys.modules[name]=m;l.exec_module(m);return m
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(R)),'sha256':sha(b),'bytes':len(b)}
P=json.loads((H/'install-plan.json').read_text());checks=[]
def ck(name,truth):assert truth,name;checks.append(name)
def source_body(lib,pid,body):
 p=lib.records[pid].data;a=lib.records[p['artifact_id']].data;raw=(V/a['path']).read_bytes();ck('payload '+pid,sha(raw)==a['sha256']==p['artifact_sha256'])
 if 'text'in p:ck('passage text '+pid,p['text']==body)
 elif raw.decode().removesuffix('\n')==body:ck('complete plain text '+pid,True)
 else:
  lines=raw.decode().splitlines(); spans=p['physical_line_ranges'];ck('one TSV row '+pid,len(spans)==1 and spans[0][0]==spans[0][1]);row=list(csv.DictReader([lines[0],lines[spans[0][0]-1]],delimiter='\t'))[0]
  vals=[json.loads(v) if k.endswith('_json')else v for k,v in row.items() if k in ['english','english_json','text','latin']];ck('TSV body '+pid,body in vals)
 return {'passage_id':pid,'artifact_id':a['id'],'artifact_sha256':a['sha256'],'payload':pin(V/a['path']),'body_sha256':sha(body.encode()),'rights_status':a['rights_status'],'physical_line_ranges':p.get('physical_line_ranges')}
sl=load('next_cohort_source_library',R/'tools/source-library');lib=sl.load_library(V);ck('complete source graph including owning works and loci',not lib.errors)
print('Full source graph passed:',len(lib.records),'records',flush=True)
for f in P['file_map']:ck('mapped destination '+f['destination'],sha((V/f['destination']).read_bytes())==f['sha256'])
data_root=V/'src/sources/calendars';doc=cal.load_document(data_root,'postconciliar',effective=False);records,errors=latin.publication_records(data_root,'postconciliar');ck('actual publication records',not errors);owners=list(latin.text_owners(doc));latchecks=[]
for u in P['latin_updates']:
 key=latin.LatinKey.from_mapping(u['after_provenance_entry']);matches=[(k,b)for k,b in owners if k==key];ck('exact owner '+str(u['identity']),len(matches)==1 and matches[0][1]==u['after_node']['text']);body=matches[0][1];decision=latin.decision_for(key,body,records);ck('six surfaces '+str(u['identity']),decision.permits(latin.SURFACES));projection=decision.projection(latin.SURFACES);grade=coverage.latin_evidence(projection)['relationship'];ck('target grade '+str(u['identity']),grade==('exact-target'if u['group']=='semen'else 'unresolved'))
 mass=cal.mass_index(doc)[key.mass];public=latin.sanitize_mass(mass,records,latin.SURFACES);ps=public['propers'];n=[x for x in ps if x['name']==key.proper][key.occurrence-1]
 if key.course:n=n[key.course][key.cycle]
 ck('published body retained '+str(u['identity']),n['text']==body and n['latin']['withheld'] is False)
 latchecks.append({'identity':u['identity'],'actual_owner':key.as_dict(),'body_sha256':sha(body.encode()),'coverage_relationship':grade,'decision':projection,'source_binding':source_body(lib,u['after_provenance_entry']['source_id'],body)})
mp=load('next_cohort_mass_propers',R/'tools/mass-propers');overlay,untranslated,stale,witnesses=mp.translation_overlay('postconciliar',data_root);english=[]
easter=json.loads((R/P['candidate_pins']['easter-three']['path']).read_text());temporal=json.loads((R/P['candidate_pins']['pentecost-two']['path']).read_text());saints=json.loads((R/P['candidate_pins']['all-saints']['path']).read_text())
for u in P['english_updates']:
 i=tuple(u['identity']);e=u['after_entry'];body=u['after_english_body'];ck('overlay '+str(i),i in overlay and overlay[i]['translations']==e['translations']);ck('no terminal former gap '+str(i),not any(mp.untranslated_record_identity(x)==i for xs in untranslated.values()for x in xs))
 mp.validate_study_translation_binding(e,'postconciliar',data_root,H/'install-plan.json');mp.validate_translation_publication_binding(e,data_root,H/'install-plan.json')
 if e.get('publication_passage_id'):pid=e['publication_passage_id']
 elif e.get('study_english_passage_id'):pid=e['study_english_passage_id']
 elif u['group']=='all-saints':pid=saints['english_publication_binding']['passage_id']
 elif u['group']=='easter-three':pid=next(proof['english_passage_id']for proof,update in zip(easter['source_proofs'],easter['english_updates'])if update['identity']==u['identity'])
 elif u['group']=='pentecost-two':pid=next(c['study_publication_passage_id']for c in temporal['changes']if c['identity']==u['identity'])
 else:raise AssertionError(('unmapped English source',i))
 binding=source_body(lib,pid,body)
 mass=cal.mass_index(doc)[i[0]];public=latin.sanitize_mass(mass,records,latin.SURFACES);formname=''
 if i[1]=='main':propers=public['propers']
 else:
  f=next(f for f in public['forms']if f['id']==i[1]);propers=f['propers'];formname=f.get('name','')
 p=copy.deepcopy([p for p in propers if p['name']==i[2]][i[4]-1])
 if i[3]!='all':p=copy.deepcopy(p[next(c for c in ['cycles','weekday_cycles']if i[3]in p.get(c,{}))][i[3]])
 local_stale=[];carried=mp.carry_translations('postconciliar',(i[0],formname,i[2]),p,overlay,local_stale,identity=i,witnesses=witnesses);ck('no stale selected English '+str(i),not local_stale)
 selected=[]
 for name,fn in [('mass-propers.select_texts',mp.select_texts),('_calendars.texts_of',cal.texts_of)]:
  out=fn(carried,'en');ck('actual '+name+' body '+str(i),len(out)==1 and out[0][0]==body);note=mp.public_witness_caution(e['witness_note']);ck('actual '+name+' qualification '+str(i),bool(note) and note in out[0][2]);selected.append({'consumer':name,'body_sha256':sha(out[0][0].encode()),'attribution':out[0][1],'note':out[0][2]})
 english.append({'identity':u['identity'],'body_sha256':sha(body.encode()),'source_binding':binding,'consumers':selected,'selected_stale':local_stale})
ordinary=load('next_cohort_mass_ordinary',R/'tools/mass-ordinary');op='src/sources/inventories/postconciliar-ordo-missae-v1.toml';arts=ordinary.artifact_records(V/'src/sources');built=ordinary.calendar_structure(V/'src/sources',V/op,arts);old=ordinary.calendar_structure(R/'src/sources',R/op,arts)
def rows(b):return {e['key']:e for s in b['sections']for e in s['elements']}
oldrows=rows(old);newrows=rows(built);changed=[k for k in oldrows if oldrows[k]!=newrows[k]];ck('only named Ordinary projection changes',changed==['praeparatio-donorum/in-spiritu-humilitatis'])
inv=tomllib.loads((V/op).read_text());entry=next(e for s in inv['sections']for e in s.get('elements',[])if e['key']=='in-spiritu-humilitatis');w=ordinary.witness_table(inv,arts,'cohort');r=ordinary.restricted_witness_table(inv,arts,'cohort');la=ordinary.side_text(entry,'la',w,r,arts,entry['key'],'cohort');en=ordinary.side_text(entry,'en',w,r,arts,entry['key'],'cohort')
ck('Ordinary exact quoted2008 word grade',la['target_wording']=='word-exact' and la['coverage_relationship']=='exact-target');ck('Ordinary fullLatin',la['text']==P['ordinary_update']['new_latin_body']);ck('Ordinary Latin hash',sha(la['text'].encode())==P['ordinary_update']['new_latin_body_sha256']);ck('Ordinary English body unchanged',sha(en['text'].encode())==P['ordinary_update']['english_unchanged']['body_sha256']);ck('Ordinary English dictionary unchanged',entry['english']==P['ordinary_update']['before_element']['english'])
key=changed[0];ck('Ordinary all other English fields unchanged',[x for x in oldrows[key]['translations']if x['lang']=='en']==[x for x in newrows[key]['translations']if x['lang']=='en'])
receipt={'schema':'triptych-next-cohort-merged-validation/v1','status':'PASS; scratch merged projection only; no canonical adoption','plan':pin(H/'install-plan.json'),'apply_receipt':pin(H/'scratch-apply-receipt.json'),'full_source_graph':{'errors':lib.errors,'records':len(lib.records),'bindings':len(lib.bindings),'owning_work_locus_validation':'full graph'},'publication_records_errors':errors,'english':english,'proper_latin':latchecks,'ordinary':{'changed_elements':changed,'before_Latin_body':P['ordinary_update']['prior_latin_body'],'after_Latin':la,'unchanged_English':en,'before_element':P['ordinary_update']['before_element'],'after_element':entry},'check_count':len(checks),'checks':checks,'canonical_writes':False,'limitations':['No fresh visual source re-review; accepts the exact pinned independent source reviews.','No new source rights or target-edition finding; all grades preserve approved finite scope.','Root must repeat live-preimage check and final integrated source-epoch/public browser checks at actual adoption.','Inherited d85 metadata defect remains a separately owned unchanged record.']}
(H/'merged-validation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':receipt['status'],'checks':len(checks),'English':len(english),'Latin':len(latchecks)+1,'receipt':pin(H/'merged-validation.json')},indent=2))
