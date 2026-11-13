from pathlib import Path
import hashlib,json,sys
H=Path(__file__).resolve().parent;B=H.parents[1];R=H.parents[3]
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p.relative_to(R)),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def read(p):return json.loads(Path(p).read_text())
P=read(H/'install-plan.json');D=read(H/'metadata-delta.json');V=read(H/'merged-validation.json');S=read(H/'final-scope-audit.json');old=read(B/'handoff-manifest.json')
review=R/sys.argv[1];reviewpin=pin(review)
assert V['check_count']==239 and V['plan']['sha256']==pin(H/'install-plan.json')['sha256'];assert S['check_count']==128 and S['plan_sha256']==pin(H/'install-plan.json')['sha256']
WF='workflows/reviews/modern-source-completion-2026-11-12/next-cohort-six';DEST=WF+'/consolidated/spacing-successor-v3'
maps={f['destination']:dict(f)for f in old['durable_file_map']}
# Preserve original consolidated evidence; use successor metadata at source destinations.
for f in P['file_map']:maps[f['destination']]=dict(f)
def add(src,dst,role):
 p=pin(src);record={'scratch_path':p['path'],'destination':dst,'sha256':p['sha256'],'bytes':p['bytes'],'role':role}
 if dst in maps:assert maps[dst]['sha256']==p['sha256']
 maps[dst]=record
for m in D['source_metadata_deltas']:
 add(R/m['predecessor']['path'],DEST+'/predecessor-source-records/'+m['destination'],'immutable-predecessor-metadata-evidence')
names=['install-plan.json','root-merit-inputs.json','metadata-delta.json','source-manifest-successor.json','README.md','apply_to_scratch.py','prepare.py','validate_merged.py','scratch-apply-receipt.json','merged-validation.json','final_scope_audit.py','final-scope-audit.json','freeze_handoff.py']
for name in names:add(H/name,DEST+'/'+name,'consolidated-spacing-plan-or-validation')
add(review,DEST+'/independent-metadata-review.json','independent-exact-metadata-delta-review')
def review_evidence(x):
 if isinstance(x,dict):
  p=x.get('path')
  if isinstance(p,str) and p.startswith('.scratch/modern-next-cohort-spacing-review/') and (R/p).is_file():
   if x.get('sha256'):assert pin(R/p)['sha256']==x['sha256']
   if R/p!=review:
    rel=Path(p).relative_to('.scratch/modern-next-cohort-spacing-review');add(R/p,DEST+'/independent-review-evidence/'+str(rel),'independent-review-support')
  for v in x.values():review_evidence(v)
 elif isinstance(x,list):
  for v in x:review_evidence(v)
review_evidence(read(review))
for f in maps.values():
 p=R/f['scratch_path'];assert pin(p)['sha256']==f['sha256'] and p.stat().st_size==f['bytes']
out={'schema':'triptych-next-cohort-spacing-handoff/v1','status':'Final spacing successor; independent metadata review retained separately; NO INSTALL','scope':P['counts'],'predecessor_handoff':pin(B/'handoff-manifest.json'),'predecessor_plan':pin(B/'install-plan.json'),'final_plan':pin(H/'install-plan.json'),'root_merit_inputs':pin(H/'root-merit-inputs.json'),'exact_metadata_delta':pin(H/'metadata-delta.json'),'source_manifest_successor':pin(H/'source-manifest-successor.json'),'independent_metadata_review':reviewpin,'merged_validation':pin(H/'merged-validation.json'),'final_scope_audit':pin(H/'final-scope-audit.json'),'scratch_projection':str((H/'dry-run-final-root').relative_to(R)),'source_file_count':61,'metadata_successor_file_count':45,'proposed_prose_fields':63,'source_metadata_prose_fields':83,'durable_file_map_count':len(maps),'durable_file_map':list(maps.values()),'original_evidence_rule':'All original candidate/body/source-review receipts and source manifests remain byte-exact. The45 predecessor TOML records are additionally mapped to separate workflow evidence paths. Their source destinations map to final successor metadata; no old receipt is represented as a review of the new metadata bytes.','invariants':'Prayer/body/TSV bytes, source quotations, prior/live and already-admitted English dictionaries, In spiritu English, source IDs/paths/URLs/loci, stored body/source hashes, formal grades and per-row target grades are unchanged. Explanatory grade prose spacing is explicitly listed in the delta. All edits insert whitespace only.','canonical_writes':False,'remaining_owner_actions':['Root reads the independent exact metadata delta receipt and final plan, then issues its actual bounded adoption receipt.','Root applies only the finite live-preimage-guarded changes; supplied executable remains scratch-only.','Root retains all mapped original and successor evidence together; the inherited d85 metadata defect remains separate.','Root performs the final integrated source-epoch/browser validation following authorized adoption.'],'superseded_spacing_drafts':[pin(H.parent/'install-plan.json'),pin(H.parent/'v2/install-plan.json')],'runtime_code_pins_at_handoff':[pin(R/p)for p in ['tools/source-library','tools/mass-propers','tools/mass-ordinary','scripts/_proper_latin.py','scripts/_calendars.py','scripts/_missal_coverage.py']]}
dest=H/'handoff-manifest.json';assert not dest.exists(),'Immutable handoff already exists';dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'handoff':pin(dest),'maps':len(maps),'plan':out['final_plan'],'merit':out['root_merit_inputs'],'review':reviewpin},indent=2))
