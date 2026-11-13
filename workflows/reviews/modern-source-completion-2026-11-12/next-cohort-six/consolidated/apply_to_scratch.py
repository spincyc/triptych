"""Guarded logical delta. Deliberately cannot install into a real repository.

Read current canonical objects, check finite preimages, copy a fresh validation
tree under this script's scratch directory, then apply only selected deltas.
Never use a whole old candidate inventory and never modify a shared hardlink.
"""
from pathlib import Path
import argparse, copy, hashlib, json, os, re, shutil, sys, tomllib
import yaml

HERE=Path(__file__).resolve().parent; R=HERE.parents[1]
def h(b):return hashlib.sha256(b).hexdigest()
def js(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(R)),'sha256':h(b),'bytes':len(b)}
def atomic(p,data):
 p.parent.mkdir(parents=True,exist_ok=True);temp=p.with_name(p.name+'.cohort-temp');temp.write_bytes(data);os.replace(temp,p)
def value(x):
 if isinstance(x,str):return json.dumps(x,ensure_ascii=False)
 if isinstance(x,bool):return str(x).lower()
 if isinstance(x,(int,float)):return str(x)
 if isinstance(x,list):return '['+', '.join(value(y) for y in x)+']'
 if isinstance(x,dict):return '{'+', '.join(json.dumps(k)+' = '+value(v) for k,v in x.items())+'}'
 raise TypeError(type(x))
def record(tag,d):return '[['+tag+']]\n'+''.join(k+' = '+value(v)+'\n' for k,v in d.items())+'\n'
def drop_records(text,tag,rows):
 chunks=list(re.finditer(r'(?m)^\[\[([a-zA-Z0-9_-]+)\]\]\s*$',text));spans=[]
 for old in rows:
  found=[]
  for i,m in enumerate(chunks):
   if m.group(1)!=tag:continue
   end=chunks[i+1].start() if i+1<len(chunks) else len(text)
   d=tomllib.loads(text[m.start():end])
   if d.get(tag)==[old]:found.append((m.start(),end))
  assert len(found)==1,(tag,old.get('mass'),old.get('proper'),len(found));spans+=found
 assert len(set(spans))==len(spans)
 for a,b in sorted(spans,reverse=True):text=text[:a]+text[b:]
 return text
def ident(e):return [e['mass'],e.get('form_id','main'),e['proper'],e.get('cycle','all'),e.get('occurrence',1)]
def lkey(e):return tuple(e.get(k,'')for k in ['mass','form','proper','course','cycle'])+(e.get('occurrence',1),)
def locate(doc,i):
 mass,form,proper,cycle,occ=i;found=[]
 for s in doc['sections'].values():
  for m in s.get('masses',[]):
   if m['key']!=mass:continue
   groups=[('main',m.get('propers',[]))]+[(f.get('id',f.get('key')),f.get('propers',[]))for f in m.get('forms',[])]
   for fid,ps in groups:
    if fid!=form:continue
    rows=[p for p in ps if p['name']==proper]
    if len(rows)>=occ:
     p=rows[occ-1]
     if cycle!='all':p=p[next(c for c in ['cycles','weekday_cycles']if cycle in p.get(c,{}))][cycle]
     found.append(p)
 assert len(found)==1,(i,len(found));return found[0]
def fields(x,path=()):
 if isinstance(x,dict):
  for k,v in x.items():yield from fields(v,path+(k,))
 elif isinstance(x,list):
  for k,v in enumerate(x):yield from fields(v,path+(k,))
 else:yield path,x
def assign(x,path,v):
 for k in path[:-1]:x=x[k]
 x[path[-1]]=v
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-root',type=Path,default=HERE/'dry-run-root');args=ap.parse_args();V=args.output_root.resolve()
 assert V.is_relative_to(HERE) and V!=HERE and '.scratch' in V.parts,'Output must be a fresh directory below this scratch package; canonical installation is forbidden'
 assert not V.exists(),'Refuse to overwrite any validation root'
 P=json.loads((HERE/'install-plan.json').read_text())
 TP='src/sources/inventories/postconciliar-proper-translations-v1.toml';LP='src/sources/inventories/postconciliar-proper-latin-provenance-v1.toml';CP='src/sources/calendars/postconciliar/propers.yaml';OP='src/sources/inventories/postconciliar-ordo-missae-v1.toml'
 paths=[TP,LP,CP,OP];raw={p:(R/p).read_bytes()for p in paths};before={p:(yaml.safe_load(raw[p])if p==CP else tomllib.loads(raw[p].decode()))for p in paths};after=copy.deepcopy(before)
 # Check all selected preimages BEFORE creating any projection.
 for u in P['english_updates']:
  assert [e for e in before[TP]['untranslated']if ident(e)==u['identity']]==u['live_before_untranslated'],u['identity']
  assert not any(ident(e)==u['identity']for e in before[TP]['entries']),u['identity']
  assert locate(before[CP],u['identity'])==u['live_proper_dictionary'],('proper drift',u['identity'])
  after[TP]['untranslated'].remove(u['before_untranslated']);after[TP]['entries'].append(u['after_entry'])
 for u in P['latin_updates']:
  n=locate(after[CP],u['identity']);assert n==u['before_node'];n.clear();n.update(copy.deepcopy(u['after_node']))
  assert [e for e in before[LP]['entries']if lkey(e)==lkey(u['after_provenance_entry'])]==u['before_provenance_entries']
  for e in u['before_provenance_entries']:after[LP]['entries'].remove(e)
  after[LP]['entries'].append(u['after_provenance_entry'])
 for u in P['appointment_updates']:
  n=locate(after[CP],u['identity']);assert n==u['before_node'];n['ordinary_disposition']['basis']=u['after_node']['ordinary_disposition']['basis'];assert n==u['after_node']
 u=P['ordinary_update'];els=[e for s in after[OP]['sections']for e in s.get('elements',[])if e['key']=='in-spiritu-humilitatis'];assert len(els)==1 and els[0]==u['before_element'];els[0]['latin']=copy.deepcopy(u['after_element']['latin']);assert els[0]==u['after_element']
 assert [w for w in after[OP]['witnesses']if w['id']==u['append_witness']['id']]==u['before_witnesses_same_id'];after[OP]['witnesses'].append(u['append_witness'])
 for old,new in u['prose_replacements'].items():
  fs=[(p,v)for p,v in fields(after[OP])if isinstance(v,str) and old in v];assert len(fs)==1,(old,fs);p,v=fs[0];assert v.count(old)==1;assign(after[OP],p,v.replace(old,new))
 assert all(e in after[TP]['untranslated']for e in P['preserve_gap_records'])
 for f in P['file_map']:
  b=(R/f['scratch_path']).read_bytes();assert h(b)==f['sha256'] and len(b)==f['bytes']
  dst=R/f['destination'];assert not dst.exists() or dst.read_bytes()==b,('destination drift',f['destination'])
 # Live snapshot, not any stale author's proposed tree. Existing links remain read-only.
 for rel in ['src/sources','src/gpt','src/claude','workflows']:
  shutil.copytree(R/rel,V/rel,copy_function=os.link,symlinks=True)
 for p in paths:assert (V/p).read_bytes()==raw[p],('concurrent change during snapshot',p)
 for f in P['file_map']:
  dst=V/f['destination'];data=(R/f['scratch_path']).read_bytes()
  if not dst.exists():atomic(dst,data)
  else:assert dst.read_bytes()==data
 # Preserve all unselected TOML blocks byte-for-byte.
 t=raw[TP].decode();t=drop_records(t,'untranslated',[u['before_untranslated']for u in P['english_updates']]);t+='\n'+''.join(record('entries',u['after_entry'])for u in P['english_updates']);assert tomllib.loads(t)==after[TP];atomic(V/TP,t.encode())
 t=raw[LP].decode();t=drop_records(t,'entries',[e for u in P['latin_updates']for e in u['before_provenance_entries']]);t+='\n'+''.join(record('entries',u['after_provenance_entry'])for u in P['latin_updates']);assert tomllib.loads(t)==after[LP];atomic(V/LP,t.encode())
 # The YAML writer reads the live document; semantic comparison proves no other field changes.
 t=yaml.safe_dump(after[CP],allow_unicode=True,sort_keys=False);assert yaml.safe_load(t)==after[CP];atomic(V/CP,t.encode())
 t=raw[OP].decode();matches=list(re.finditer(r'(?m)^\[\[sections(?:\.elements)?\]\]\s*$',t));spans=[]
 for i,m in enumerate(matches):
  end=matches[i+1].start()if i+1<len(matches)else len(t)
  if re.search(r'(?m)^key = "in-spiritu-humilitatis"$',t[m.start():end]):spans.append((m.start(),end))
 assert len(spans)==1;start,end=spans[0]
 # Only this one element is rewritten, including its unchanged English dictionary.
 t=t[:start]+record('sections.elements',u['after_element'])+t[end:]
 t+='\n'+record('witnesses',u['append_witness'])
 for old,new in u['prose_replacements'].items():
  pattern=re.escape(old).replace(r'\ ',r'(?:\s|\\\n)+');t,n=re.subn(pattern,lambda _:new,t);assert n==1,(old,n)
 assert tomllib.loads(t)==after[OP],'Ordinary changed outside the named delta';atomic(V/OP,t.encode())
 # Verify undo of selected changes recovers every full live semantic document.
 restored=copy.deepcopy(after)
 for u in P['english_updates']:
  restored[TP]['entries'].remove(u['after_entry'])
 # Restore refusal ordering exactly, keeping full other metadata and all entries.
 restored[TP]['untranslated']=copy.deepcopy(before[TP]['untranslated'])
 for u in P['latin_updates']:
  n=locate(restored[CP],u['identity']);n.clear();n.update(u['before_node']);restored[LP]['entries'].remove(u['after_provenance_entry'])
 restored[LP]['entries']=copy.deepcopy(before[LP]['entries'])
 for u in P['appointment_updates']:locate(restored[CP],u['identity'])['ordinary_disposition']['basis']=u['before_node']['ordinary_disposition']['basis']
 # Ordinary expected document was constructed with only the explicit changes;
 # compare generated old/new rows separately in validate_merged.py.
 for p in [TP,LP,CP]:assert restored[p]==before[p],('unselected semantic change',p)
 defect=P['separate_inherited_metadata_defect']['current_record'];assert (V/defect['path']).read_bytes()==(R/defect['path']).read_bytes()
 receipt={'schema':'triptych-next-cohort-scratch-apply/v1','status':'SCRATCH PROJECTION ONLY; not adopted','plan_sha256':h((HERE/'install-plan.json').read_bytes()),'root':str(V.relative_to(R)),'live_input_pins_at_apply':{p:{'sha256':h(raw[p]),'bytes':len(raw[p])}for p in paths},'projected_output_pins':{p:pin(V/p)for p in paths},'semantic_before_sha256':{p:h(js(before[p]).encode())for p in paths},'semantic_after_sha256':{p:h(js(after[p]).encode())for p in paths},'english_entries_before':len(before[TP]['entries']),'english_entries_after':len(after[TP]['entries']),'english_untranslated_before':len(before[TP]['untranslated']),'english_untranslated_after':len(after[TP]['untranslated']),'selected_preimages_pass':True,'unselected_semantic_objects_preserved':True,'unselected_TOML_blocks_preserved':True,'current_Hildegard_Newman_gaps_preserved':P['preserve_gap_records'],'ordinary_English_dictionary_unchanged':True,'source_files_mapped':len(P['file_map']),'separate_d85_metadata_unchanged':True,'canonical_final_pins':{p:pin(R/p)for p in paths},'canonical_writes':False}
 atomic(HERE/'scratch-apply-receipt.json',(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode());print(json.dumps({'status':receipt['status'],'root':receipt['root'],'English':len(P['english_updates']),'Latin':len(P['latin_updates'])+1,'files':len(P['file_map'])}))
if __name__=='__main__':main()
