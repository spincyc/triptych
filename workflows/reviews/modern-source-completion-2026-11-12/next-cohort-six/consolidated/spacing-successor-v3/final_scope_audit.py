from pathlib import Path
import copy,hashlib,json,tomllib
import yaml
H=Path(__file__).resolve().parent;R=H.parents[3];V=H/'dry-run-final-root';P=json.loads((H/'install-plan.json').read_text());A=json.loads((H/'scratch-apply-receipt.json').read_text());checks=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def ck(k,v):assert v,k;checks.append(k)
def get(d,p):
 for k in p:d=d[k]
 return d
def replace(d,p,v):
 for k in p[:-1]:d=d[k]
 d[p[-1]]=v
def identity(e):return [e['mass'],e.get('form_id','main'),e['proper'],e.get('cycle','all'),e.get('occurrence',1)]
TP='src/sources/inventories/postconciliar-proper-translations-v1.toml';LP='src/sources/inventories/postconciliar-proper-latin-provenance-v1.toml';CP='src/sources/calendars/postconciliar/propers.yaml';OP='src/sources/inventories/postconciliar-ordo-missae-v1.toml'
old={p:(yaml.safe_load((R/p).read_text())if p==CP else tomllib.loads((R/p).read_text()))for p in [TP,LP,CP,OP]};new={p:(yaml.safe_load((V/p).read_text())if p==CP else tomllib.loads((V/p).read_text()))for p in old}
for p in old:ck('canonical byte hash unchanged '+p,sha((R/p).read_bytes())==A['live_input_pins_at_apply'][p]['sha256'])
selected=[u['identity']for u in P['english_updates']]
ck('all prior positive English records preserve content and order',new[TP]['entries'][:-10]==old[TP]['entries'])
ck('exact selected English additions',new[TP]['entries'][-10:]==[u['after_entry']for u in P['english_updates']])
ck('every unselected refusal preserves content and order',new[TP]['untranslated']==[e for e in old[TP]['untranslated']if identity(e)not in selected])
ck('all English inventory metadata unchanged',{k:v for k,v in old[TP].items()if k not in ['entries','untranslated']}=={k:v for k,v in new[TP].items()if k not in ['entries','untranslated']})
oldrows=[e for u in P['latin_updates']for e in u['before_provenance_entries']];newrows=[u['after_provenance_entry']for u in P['latin_updates']]
ck('all unselected Latin rows preserve content and order',[e for e in new[LP]['entries']if e not in newrows]==[e for e in old[LP]['entries']if e not in oldrows]);ck('exact five Latin additions',new[LP]['entries'][-5:]==newrows)
ck('all Latin inventory metadata unchanged',{k:v for k,v in old[LP].items()if k!='entries'}=={k:v for k,v in new[LP].items()if k!='entries'})
b=copy.deepcopy(old[CP]);a=copy.deepcopy(new[CP])
for u in P['latin_updates']:
 path=u['live_path'];ck('full Latin node old/new '+str(u['identity']),get(b,path)==u['before_node'] and get(a,path)==u['after_node']);replace(b,path,None);replace(a,path,None)
for u in P['appointment_updates']:
 path=u['live_path'];ck('full option node old/new '+str(u['identity']),get(b,path)==u['before_node'] and get(a,path)==u['after_node']);replace(b,path+['ordinary_disposition','basis'],None);replace(a,path+['ordinary_disposition','basis'],None)
ck('all unselected proper fields and branches unchanged',a==b)
u=P['ordinary_update'];a=copy.deepcopy(new[OP]);b=copy.deepcopy(old[OP]);path=u['live_path'];ck('complete selected Ordinary before/after dictionaries',get(b,path)==u['before_element']and get(a,path)==u['after_element']);replace(a,path+['latin'],None);replace(b,path+['latin'],None)
ck('exact one Ordinary witness appended',a['witnesses'][-1]==u['append_witness']);a['witnesses'].pop()
def restore(x):
 if isinstance(x,dict):return {k:restore(v)for k,v in x.items()}
 if isinstance(x,list):return [restore(v)for v in x]
 if isinstance(x,str):
  for oldtext,newtext in u['prose_replacements'].items():x=x.replace(newtext,oldtext)
 return x
ck('every other Ordinary field unchanged',restore(a)==b)
for f in P['file_map']:
 ck('exact source and durable projection '+f['destination'],sha((R/f['scratch_path']).read_bytes())==f['sha256']==sha((V/f['destination']).read_bytes()))
defect=P['separate_inherited_metadata_defect']['current_record'];ck('separate inherited metadata unchanged',sha((R/defect['path']).read_bytes())==defect['sha256']==sha((V/defect['path']).read_bytes()))
o={'schema':'triptych-next-cohort-final-scope-audit/v1','status':'PASS','plan_sha256':sha((H/'install-plan.json').read_bytes()),'checks':checks,'check_count':len(checks),'canonical_selected_document_bytes_unchanged':True,'unselected_field_and_row_content_order_preserved':True,'all_source_review_candidate_mappings_hash_exact':True,'no_canonical_writes':True}
(H/'final-scope-audit.json').write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'checks':len(checks),'sha256':sha((H/'final-scope-audit.json').read_bytes())}))
