"""Create immutable prose-spacing successors; never mutate predecessor bytes."""
from pathlib import Path
import copy, hashlib, json, re, tomllib
H=Path(__file__).resolve().parent; B=H.parents[1]; R=H.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p.relative_to(R)),'sha256':sha(b),'bytes':len(b)}
def output(p,d):
 assert not p.exists(),('Immutable successor already exists',p)
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def compact(s):return re.sub(r'\s','',s)
original_plan=pin(B/'install-plan.json');assert original_plan['sha256']=='c9646fcf3baa770bebeb244a699599307af06180f93b27a9331ed783cc544280'
old=json.loads((B/'install-plan.json').read_text());new=copy.deepcopy(old)

# Technical identifiers, actual paths/URLs and hash strings are indivisible.
# Only the remaining prose receives inserted spaces; no letter/punctuation is changed.
PROTECTED=re.compile(r'\b\d{1,3}(?:,\d{3})+\b|\b\d+:\d+(?:[-–]\d+)?\b|\bUTF8\b|https?://[^\s<>"\']+|(?:work|edition|artifact|passage|segment)\.[A-Za-z0-9][A-Za-z0-9._-]*|(?:\.?[A-Za-z0-9_-]+/)+[A-Za-z0-9_.-]+\.(?:json|toml|yaml|md|py|pdf|png|jpg|txt|tsv)|\b[0-9a-f]{8,64}\b|\b(?:SHA256|SHA-256|UTF-8|CC-BY-4\.0)\b')
def normalize(s):
 # Delimit a source carrier label from a short hash before protecting the hash.
 s=re.sub(r'\b(PDF|artifact)(?=[0-9a-f]{8}\b)',r'\1 ',s)
 chunks=[];end=0
 def plain(x):
  x=re.sub(r'([A-Za-z])(?=\d)',r'\1 ',x)
  x=re.sub(r'(\d)(?=[A-Za-z])',r'\1 ',x)
  x=re.sub(r'([a-z])(?=[A-Z])',r'\1 ',x)
  x=re.sub(r'([,;])(?=[A-Za-z0-9])',r'\1 ',x)
  x=re.sub(r'(?<!\d):(?=[A-Za-z0-9])',': ',x)
  x=re.sub(r'\.(?=[A-Z])','. ',x)
  x=re.sub(r'\b(p|pp|n|nn)\.(?=\d)',r'\1. ',x)
  x=re.sub(r'\.(?=(?:18|19|20)\d\d\b)','. ',x)
  for a,b in [('wholebody','whole body'),('fullbody','full body'),('wholebook','whole book'),('bodyonly','body only'),('allcycle','all cycle'),('sourcebased','source based'),('wordexact','word exact')]:
   x=re.sub(r'\b'+a+r'\b',b,x)
  x=re.sub(r'\b(Book)(?=[IVX]+\b)',r'\1 ',x)
  x=re.sub(r'\b(section)(?=[ivxl]+\b)',r'\1 ',x)
  x=re.sub(r'\b(printed)(?=\[)',r'\1 ',x)
  return x
 for m in PROTECTED.finditer(s):chunks += [plain(s[end:m.start()]),m.group()];end=m.end()
 chunks.append(plain(s[end:]));out=''.join(chunks)
 assert compact(out)==compact(s),('Nonspacing transformation',s,out)
 return out
def at(obj,path):
 for k in path:obj=obj[k]
 return obj
def setat(obj,path,v):
 for k in path[:-1]:obj=obj[k]
 obj[path[-1]]=v
plan_deltas=[]
def change(path):
 oldval=at(new,path);assert isinstance(oldval,str);after=normalize(oldval)
 if oldval!=after:
  assert compact(oldval)==compact(after)
  plan_deltas.append({'path':path,'before':oldval,'after':after,'non_whitespace_characters_unchanged':True});setat(new,path,after)
def fields(base,allowed):
 obj=at(new,base)
 for k,v in obj.items():
  if k not in allowed:continue
  if isinstance(v,str):change(base+[k])
  elif isinstance(v,list):
   for i,item in enumerate(v):
    if isinstance(item,str):change(base+[k,i])

for i,u in enumerate(new['english_updates']):
 fields(['english_updates',i,'after_entry'],{'witness_note','divergence','ancient_witness'})
for i,u in enumerate(new['latin_updates']):
 fields(['latin_updates',i,'after_node'],{'notes'})
 fields(['latin_updates',i,'after_provenance_entry'],{'locator','verification_locator','transformations','provenance_evidence','provenance_authority','publication_locator','publication_evidence','note'})
for i,u in enumerate(new['appointment_updates']):change(['appointment_updates',i,'after_node','ordinary_disposition','basis'])
fields(['ordinary_update','after_element','latin'],{'note','reading_note','collation_finding'})
fields(['ordinary_update','append_witness'],{'label','caution'})
for k in new['source_grade_limits']:change(['source_grade_limits',k])
change(['scope'])

source_deltas=[];source_manifest=[]
SOURCE_PROSE={'title','description','composed_basis','notes','context','rights_basis','transformation','provenance'}
for i,f in enumerate(new['file_map']):
 src=R/f['scratch_path'];assert sha(src.read_bytes())==f['sha256'] and src.stat().st_size==f['bytes']
 if not f['destination'].startswith('src/'):continue
 if not f['destination'].endswith('.toml'):
  source_manifest.append({'destination':f['destination'],'successor':pin(src),'predecessor':pin(src),'status':'unchanged-payload'})
  continue
 text=src.read_text();record=tomllib.loads(text);updated=copy.deepcopy(record);deltas=[]
 for key,value in record.items():
  if key not in SOURCE_PROSE or not isinstance(value,str):continue
  after=normalize(value)
  if after==value:continue
  assert compact(value)==compact(after)
  pattern=re.compile(r'(?m)^'+re.escape(key)+r'\s*=\s*("(?:[^"\\]|\\.)*")[ \t]*$')
  matches=list(pattern.finditer(text));assert len(matches)==1,(src,key,'non-simple TOML field')
  m=matches[0];assert tomllib.loads(key+' = '+m.group(1))[key]==value
  text=text[:m.start(1)]+json.dumps(after,ensure_ascii=False)+text[m.end(1):]
  updated[key]=after;deltas.append({'path':[key],'before':value,'after':after,'non_whitespace_characters_unchanged':True})
 assert tomllib.loads(text)==updated
 if deltas:
  dst=H/'files'/f['destination'];assert not dst.exists();dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(text)
  predecessor=pin(src);successor=pin(dst);source_deltas.append({'destination':f['destination'],'record_id':record['id'],'record_type':record['record_type'],'predecessor':predecessor,'successor':successor,'fields':deltas})
  f['scratch_path']=successor['path'];f['sha256']=successor['sha256'];f['bytes']=successor['bytes'];f['spacing_predecessor']=predecessor
  source_manifest.append({'destination':f['destination'],'successor':successor,'predecessor':predecessor,'status':'prose-spacing-only'})
 else:source_manifest.append({'destination':f['destination'],'successor':pin(src),'predecessor':pin(src),'status':'unchanged-metadata'})

# Mechanical invariants are independent of whether every optional prose token was spaced.
for a,b in zip(old['english_updates'],new['english_updates']):
 for k in a:
  if k!='after_entry':assert a[k]==b[k],('English protected field',k)
 for k in a['after_entry']:
  if k not in {'witness_note','divergence','ancient_witness'}:assert a['after_entry'][k]==b['after_entry'][k],('English protected field',k)
for a,b in zip(old['latin_updates'],new['latin_updates']):
 assert a['target_grade']==b['target_grade'];assert a['before_node']==b['before_node'];assert a['before_provenance_entries']==b['before_provenance_entries'];assert a['after_node']['text']==b['after_node']['text']
assert old['ordinary_update']['before_element']==new['ordinary_update']['before_element']
assert old['ordinary_update']['after_element']['english']==new['ordinary_update']['after_element']['english']
assert old['ordinary_update']['english_unchanged']==new['ordinary_update']['english_unchanged']
assert old['candidate_pins']==new['candidate_pins'] and old['preserve_gap_records']==new['preserve_gap_records']
assert old['separate_inherited_metadata_defect']==new['separate_inherited_metadata_defect']
report={'schema':'triptych-next-cohort-spacing-delta/v1','status':'author proof; independent review pending','predecessor_plan':original_plan,'allowed_change':'Insert whitespace only in explicit descriptive fields; administrative scratch mapping/hash/size updates identify new metadata bytes. No lexical, body, rights, grade, prior-state, source-ID, locus, URL or path alteration.','proposed_dictionary_deltas':plan_deltas,'source_metadata_deltas':source_deltas,'counts':{'proposed_string_fields':len(plan_deltas),'metadata_files':len(source_deltas),'metadata_string_fields':sum(len(x['fields'])for x in source_deltas),'source_files':len(source_manifest)},'protected_scope':['All old/before/live dictionaries and all original_admitted_entry dictionaries unchanged.','All prayer texts, source quotations/ancient_reading, body and TSV payload bytes unchanged.','In spiritu existing English dictionary, scalar hash, and artifact hash unchanged.','Every source ID/path/URL/locus and stored source/body hash unchanged.','Every per-row target_grade and formal relationship/collation/rights/publication-status field unchanged. Descriptive source_grade_limits prose spacing is explicitly listed.','Original final plan, candidates, source/fidelity and installation reviews, manifests and their pins unchanged.','Only the after-prose and actual new metadata-file mappings differ; original accepted receipts are not represented as reviews of successor metadata bytes.','Inherited d85 metadata record remains outside this change.'],'body_hashes':[{'identity':u['identity'],'English':u['after_english_body_sha256']}for u in new['english_updates']]+[{'identity':u['identity'],'Latin':u['after_provenance_entry']['text_sha256']}for u in new['latin_updates']]+[{'identity':new['ordinary_update']['identity'],'Latin':new['ordinary_update']['new_latin_body_sha256'],'unchanged_English':new['ordinary_update']['english_unchanged']['body_sha256']}],'original_review_candidate_file_pins':[f for f in old['file_map']if not f['destination'].startswith('src/')],'canonical_writes':False}
output(H/'metadata-delta.json',report);output(H/'source-manifest-successor.json',source_manifest)
new['spacing_successor']={'predecessor_plan':original_plan,'metadata_delta':pin(H/'metadata-delta.json'),'source_manifest_successor':pin(H/'source-manifest-successor.json'),'review_status':'independent exact metadata delta review pending','original_receipts':'All original accepted candidate/source/review bytes remain immutable and bound. They establish underlying body/source merit; successor whitespace metadata has its own explicit review.'}
output(H/'install-plan.json',new)
merit=json.loads((B/'root-merit-inputs.json').read_text());merit['install_plan']=pin(H/'install-plan.json')
for m,u in zip(merit['english'],new['english_updates']):m['after']=u['after_entry'];m['grade']=new['source_grade_limits'][u['group']]
merit['latin']=new['latin_updates'];merit['ordinary']=new['ordinary_update'];merit['neutral_option_basis_updates']=new['appointment_updates'];merit['file_map']=new['file_map'];merit['spacing_successor']=new['spacing_successor']
output(H/'root-merit-inputs.json',merit)
# Reuse exactly the reviewed logical-delta mechanism, changing only scratch depth.
for name in ['apply_to_scratch.py','validate_merged.py','final_scope_audit.py']:
 src=B/name;text=src.read_text();text=text.replace('R=HERE.parents[1]','R=HERE.parents[3]').replace('R=H.parents[1]','R=H.parents[3]')
 dst=H/name;assert not dst.exists();dst.write_text(text)
assert pin(B/'install-plan.json')==original_plan
print(json.dumps({'plan':pin(H/'install-plan.json'),'merit':pin(H/'root-merit-inputs.json'),'delta':pin(H/'metadata-delta.json'),'source_manifest':pin(H/'source-manifest-successor.json'),'counts':report['counts']},indent=2))
