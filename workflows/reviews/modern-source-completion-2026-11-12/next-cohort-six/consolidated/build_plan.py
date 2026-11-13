from pathlib import Path
import copy, hashlib, json, re, sys, tomllib
import yaml

R=Path(__file__).resolve().parents[2]; O=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
 p=R/p; b=p.read_bytes(); return {'path':str(p.relative_to(R)), 'sha256':sha(b), 'bytes':len(b)}
def load(p): return json.loads((R/p).read_text())
def put(name,d): (O/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
P={
 'semen':('.scratch/modern-partition-ordinarytime/semen-install-proposal/proposal-v2.json','5ddffab68daf6703cd0782145c7fc63f58e52b2da2728e2d9b6171e0d8ed2efc'),
 'in-spiritu':('.scratch/modern-official2008-latin/in-spiritu/candidate.json','4e4325c656bad4426575f11e3a98efaf0392ad602926879b605669e968fa0c91'),
 'ot21':('.scratch/modern-partition-ordinarytime/plenum-full-proposal-v2/installation-proposal-v3.json','c249aaf635ed0cef4e1a599544e024d749462b24c118445422e09436052c887e'),
 'all-saints':('.scratch/modern-partition-nonseasonal/all-saints-installation-v2/installation.json','ddfe5005181a193af80536ca4306e46f00ae7576ac45b68cdb5b28e9ac44b222'),
 'easter-three':('.scratch/modern-partition-easter/three-install-proposal/proposal-v3.json','a735dd958bf401c666d331c3b43988403750eb39ccbbdb574a2c00be06f45ee6'),
 'pentecost-two':('.scratch/modern-study-qualification-addendum/temporal-proposal-v3.json','f15964221edd40b97a9c684048aeaf42ce13085b0f40c326354c3392a1a55235'),
}
Q='.scratch/modern-sources/next-cohort-review-queue.md'
assert pin(Q)['sha256']=='8561ad3d553aa2f31920af12c7f9de328e68fd815fe8d1c71dc9c51aba9c3285'
for p,h in P.values(): assert pin(p)['sha256']==h,(p,pin(p))
D={k:load(p) for k,(p,h) in P.items()}
TP='src/sources/inventories/postconciliar-proper-translations-v1.toml'
LP='src/sources/inventories/postconciliar-proper-latin-provenance-v1.toml'
CP='src/sources/calendars/postconciliar/propers.yaml'
OP='src/sources/inventories/postconciliar-ordo-missae-v1.toml'
live={TP:tomllib.loads((R/TP).read_text()),LP:tomllib.loads((R/LP).read_text()),CP:yaml.safe_load((R/CP).read_text()),OP:tomllib.loads((R/OP).read_text())}
def ident(e): return [e['mass'],e.get('form_id','main'),e['proper'],e.get('cycle','all'),e.get('occurrence',1)]
def node_path(doc,i):
 mass,form,proper,cycle,occ=i; found=[]
 for sn,s in doc['sections'].items():
  for mi,m in enumerate(s.get('masses',[])):
   if m['key']!=mass:continue
   groups=[('main',m.get('propers',[]),['sections',sn,'masses',mi,'propers'])]
   groups += [(f.get('id',f.get('key')),f.get('propers',[]),['sections',sn,'masses',mi,'forms',fi,'propers']) for fi,f in enumerate(m.get('forms',[]))]
   for fid,ps,base in groups:
    if fid!=form:continue
    matches=[(pi,p) for pi,p in enumerate(ps) if p['name']==proper]
    if len(matches)<occ:continue
    pi,p=matches[occ-1]; path=base+[pi]
    if cycle!='all':
     course=next(c for c in ['cycles','weekday_cycles'] if cycle in p.get(c,{}));path += [course,cycle]
    found.append(path)
 assert len(found)==1,(i,found)
 return found[0]
def get(doc,path):
 for k in path:doc=doc[k]
 return doc
def lkey(e):return tuple(e.get(k,'') for k in ['mass','form','proper','course','cycle'])+(e.get('occurrence',1),)
english=[]; latin=[]
for u in D['semen']['english_updates']:english.append({'group':'semen',**copy.deepcopy(u)})
english.append({'group':'ot21','identity':D['ot21']['identity'],**copy.deepcopy(D['ot21']['english_update'])})
a=D['all-saints'];english.append({'group':'all-saints','identity':a['scope'],'before_untranslated':a['prior_english_untranslated'],'after_entry':a['proposed_english_entry']})
english += [{'group':'easter-three',**copy.deepcopy(u)} for u in D['easter-three']['english_updates']]
english += [{'group':'pentecost-two','identity':u['identity'],'before_untranslated':u['before'],'after_entry':u['after'],'original_admitted_entry':u['original_admitted_entry']} for u in D['pentecost-two']['changes'] if u['identity'][0:2]==['pentecost','extended-vigil']]
assert len(english)==10
for u in english:
 matches=[x for x in live[TP]['untranslated'] if ident(x)==u['identity']]
 assert matches==[u['before_untranslated']],u['identity']
 assert not any(ident(x)==u['identity'] for x in live[TP]['entries']),u['identity']
 u['live_before_entries']=[];u['live_before_untranslated']=matches;u['after_english_body']=u['after_entry']['translations'][0]['text'];u['after_english_body_sha256']=sha(u['after_english_body'].encode())
 u['live_proper_path']=node_path(live[CP],u['identity']);u['live_proper_dictionary']=copy.deepcopy(get(live[CP],u['live_proper_path']))
for u in D['semen']['latin_updates']:latin.append({'group':'semen',**copy.deepcopy(u)})
latin.append({'group':'ot21','identity':D['ot21']['identity'],**copy.deepcopy(D['ot21']['latin_update'])})
latin.append({'group':'all-saints','identity':a['scope'],'before_node':a['prior_proper'],'after_node':a['proposed_proper'],'before_provenance_entries':([] if a['prior_latin_provenance_entry'] is None else [a['prior_latin_provenance_entry']]),'after_provenance_entry':a['proposed_latin_provenance_entry']})
for u in latin:
 p=node_path(live[CP],u['identity']);assert get(live[CP],p)==u['before_node'],u['identity'];u['live_path']=p
 matches=[x for x in live[LP]['entries'] if lkey(x)==lkey(u['after_provenance_entry'])];assert matches==u['before_provenance_entries'],(u['identity'],matches)
 assert sha(u['after_node']['text'].encode())==u['after_provenance_entry']['text_sha256']
 u['target_grade']='exact governing OLM1981 body, not Missal2008' if u['group']=='semen' else 'historical source expression; modern2008 target unresolved'
appointments=copy.deepcopy(D['easter-three']['appointment_updates'])
for u in appointments:
 u['live_path']=node_path(live[CP],u['identity']);assert get(live[CP],u['live_path'])==u['before_node']
 b=copy.deepcopy(u['before_node']);b['ordinary_disposition']['basis']=u['after_node']['ordinary_disposition']['basis'];assert b==u['after_node']
c=D['in-spiritu'];els=[(si,ei,e) for si,s in enumerate(live[OP]['sections']) for ei,e in enumerate(s.get('elements',[])) if e['key']=='in-spiritu-humilitatis'];assert len(els)==1
si,ei,e=els[0];assert e==c['before_element'];assert e['english']==c['after_element']['english']
ws=[w for w in live[OP]['witnesses'] if w['id']==c['new_witness']['id']];assert not ws,'Witness appeared; rebase finite merge explicitly'
ordinary={'identity':'praeparatio-donorum/in-spiritu-humilitatis','live_path':['sections',si,'elements',ei],'before_element':copy.deepcopy(e),'after_element':copy.deepcopy(c['after_element']),'before_witnesses_same_id':ws,'append_witness':c['new_witness'],'prose_replacements':c['prose_replacements'],'prior_latin_body':c['prior_latin_body'],'prior_latin_body_sha256':c['prior_latin_body_sha256'],'new_latin_body':"In spiritu humilitatis, et in animo contrito suscipiamur a te Domine: et sic fiat sacrificium nostrum in conspectu tuo hodie, ut placeat tibi, Domine Deus.",'new_latin_body_sha256':c['new_latin_body_sha256'],'english_unchanged':c['english_unchanged'],'target_grade':'word-exact to complete official2022 quotation expressly citing Missal2008 p515; prayer words only'}
maps={};WF='workflows/reviews/modern-source-completion-2026-11-12/next-cohort-six'
def add(src,dst,group,role,expected=None):
 p=pin(src)
 if expected:assert p['sha256']==expected,(src,p['sha256'],expected)
 assert not dst.startswith('.scratch/') and '..' not in Path(dst).parts
 m={'scratch_path':p['path'],'destination':dst,'sha256':p['sha256'],'bytes':p['bytes'],'group':group,'role':role,'live_destination':pin(dst) if (R/dst).is_file() else None}
 if m['live_destination']:assert m['live_destination']['sha256']==p['sha256'],('conflicting existing destination',dst)
 if dst in maps:assert maps[dst]['sha256']==p['sha256'];return
 maps[dst]=m
def manifest(group,base,items):
 for x in items:
  if isinstance(x,str):x={'path':x}
  add(str(Path(base)/x['path']),x['path'],group,'source-record-or-payload',x.get('sha256'))
manifest('semen','.scratch/modern-partition-ordinarytime/semen-install-proposal/files',load('.scratch/modern-partition-ordinarytime/semen-install-proposal/new-source-files-manifest.json'))
manifest('ot21','.scratch/modern-partition-ordinarytime/plenum-full-proposal-v2/files',load('.scratch/modern-partition-ordinarytime/plenum-full-proposal-v2/new-source-files-manifest.json'))
manifest('all-saints','.scratch/modern-partition-nonseasonal/all-saints-installation-v2/package',a['new_source_files'])
manifest('in-spiritu','.scratch/modern-official2008-latin/in-spiritu/proposed',[x for x in load('.scratch/modern-official2008-latin/in-spiritu/manifest.json') if x['path']!=OP])
for x in load('.scratch/modern-partition-easter/three-install-proposal/files-manifest.json'):
 if x['path'].endswith('-source-review.json'):
  name=Path(x['path']).name.removesuffix('-source-review.json');src=f'.scratch/modern-new-orations-review/{name}/review.json'
 else:src=str(Path('.scratch/modern-partition-easter/three-install-proposal/files')/x['path'])
 add(src,x['path'],'easter-three','source-review' if x['path'].endswith('-source-review.json') else 'source-record-or-admission',x['sha256'])
manifest('pentecost-two','.scratch/modern-partition-temporal/install-proposal-v2/files',[x for x in D['pentecost-two']['files'] if 'pentecost-extended' in x['path']])
assert len([x for x in maps.values() if x['group']=='pentecost-two'])==10
for g,(p,h) in P.items():add(p,f'{WF}/{g}/final-proposal.json',g,'final-reviewed-proposal',h)
reviews=[
 ('semen','.scratch/modern-new-acclamations-review/review.json','source-review.json','c49c1aed1affe1a728c3be023f2dce339966e916fee2d2cbbecae702ffeacd0e'),
 ('semen','.scratch/modern-new-acclamations-review/semen-install-addendum.json','install-review.json','570e19e354e5b6dad3c4de106576c99c14d0fd7d3b97c7de3d20947948a4fd5c'),
 ('in-spiritu','.scratch/modern-in-spiritu-review/review.json','independent-review.json','5768c83e5cee91917894d5fff377525bc61036ae777fc5ae40cb58853642e4ae'),
 ('ot21','.scratch/modern-new-orations-review/ot21/review.json','petition-review.json',None),
 ('ot21','.scratch/modern-new-orations-review/ot21-complete/review.json','complete-review.json','32b0e0dfedfd435d5d70313b33439e3a2568f24f7c9bb0e656c1826e1f8dcd71'),
 ('all-saints','.scratch/modern-new-antiphons-review/receipt.json','source-review.json','bd94d75113edc325a1f907837269046b9de7e622f48d082cce61f047deca51f2'),
 ('all-saints','.scratch/modern-new-antiphons-review/all-saints-installation/receipt.json','install-review.json','83d9ef0581fc42e3332cc8ccb2c12b23f31b56aae308f713b8a2b544c55b3d4e'),
 ('easter-three','.scratch/modern-new-orations-review/easter-install/review.json','install-review.json','1e1ed83bb3b7074af6073271b0d34893aafe55071ba9eab49664dedb8fb23b1c'),
 ('pentecost-two','.scratch/modern-temporal-collects-review/review.json','scoped-install-review.json','424a147b1e7f75dc02f74185f3e7b6befade0c2bdf707c432f720c06676ae875'),
 ('shared','.scratch/modern-study-qualification-addendum/review.json','qualification-addendum.json','a2131d7c0459893555406e07828b72ef64ecccb2b5133d2b7b93d000262a5d27'),
]
for g,p,n,h in reviews:add(p,f'{WF}/{g}/{n}',g,'independent-review',h)
extras=[
 ('semen','.scratch/modern-partition-ordinarytime/semen-candidates.json','original-two-source-candidates.json'),
 ('semen','.scratch/modern-partition-lent-holyweek/candidate-package.json','lent-source-candidates-original.json'),
 ('semen','.scratch/modern-partition-lent-holyweek/candidate-package-v2.json','lent-source-candidates-v2.json'),
 ('semen','.scratch/modern-partition-ordinarytime/semen-install-proposal/proposal.json','rejected-runtime-key-predecessor.json'),
 ('semen','.scratch/modern-partition-ordinarytime/semen-install-proposal/new-source-files-manifest.json','source-manifest.json'),
 ('semen','.scratch/modern-partition-ordinarytime/semen-install-proposal/runtime-validation-v2.json','author-runtime-validation.json'),
 ('in-spiritu','.scratch/modern-official2008-latin/in-spiritu/manifest.json','source-manifest-with-unadopted-old-inventory-pin.json'),
 ('ot21','.scratch/modern-partition-ordinarytime/plenum-full-proposal-v2/candidate.json','full-body-candidate.json'),
 ('ot21','.scratch/modern-partition-ordinarytime/plenum-full-proposal-v2/new-source-files-manifest.json','source-manifest.json'),
 ('ot21','.scratch/modern-partition-ordinarytime/plenum-candidate.json','petition-candidate.json'),
 ('ot21','.scratch/modern-new-orations-review/ot21-complete/inherited-formula-metadata-defect.json','separate-inherited-metadata-defect.json'),
 ('all-saints','.scratch/modern-partition-nonseasonal/all-saints-study-candidate.json','source-candidate.json'),
 ('all-saints','.scratch/modern-partition-nonseasonal/all-saints-input-preimage.json','original-preimage.json'),
 ('all-saints','.scratch/modern-partition-nonseasonal/all-saints-installation/installation.json','pre-note-proposal.json'),
 ('easter-three',D['easter-three']['candidate_packet_path'],'source-candidates.json'),
 ('easter-three','.scratch/modern-partition-easter/three-install-proposal/files-manifest.json','source-manifest.json'),
 ('easter-three','.scratch/modern-partition-easter/three-install-proposal/proposal-v2.json','pre-note-proposal.json'),
 ('pentecost-two','.scratch/modern-partition-temporal/install-proposal-v2/proposal.json','pre-note-four-row-proposal.json'),
 ('pentecost-two','.scratch/modern-temporal-collects-review/note-successor-review.json','independent-note-review.json'),
 ('pentecost-two','.scratch/modern-temporal-collects-review/verification.json','scoped-independent-verification.json'),
 ('shared','.scratch/modern-study-qualification-addendum/python-consumers-review.json','python-consumers-review.json'),
 ('shared','.scratch/modern-study-qualification-addendum/browser-review.json','browser-review.json'),
 ('shared','.scratch/modern-study-qualification-addendum/browser-actual-320.json','browser-actual-320.json'),
]
for g,p,n in extras:add(p,f'{WF}/{g}/{n}',g,'candidate-or-manifest')
defect='src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945/artifacts/english-completion-20261029-postconciliar-opening2-lasance-conclusion217-d85c36fb/artifact.toml'
plan={'schema':'triptych-modern-next-cohort-logical-install-plan/v1','status':'SCRATCH ONLY; NO INSTALL; Root merits review and adoption pending','scope':'Queue sections1–6 only; ten proper English uses plus six Latin selections including Ordinary. Temporal other two proposals excluded. No source authority or target grade expanded.','queue':pin(Q),'counts':{'proper_english_uses':10,'proper_latin_selections':5,'ordinary_latin_selections':1,'neutral_appointment_basis_updates':2},'canonical_documents':{p:pin(p) for p in live},'candidate_pins':{g:pin(p) for g,(p,h) in P.items()},'english_updates':english,'latin_updates':latin,'appointment_updates':appointments,'ordinary_update':ordinary,'file_map':list(maps.values()),'excluded_temporal_changes':[x['identity'] for x in D['pentecost-two']['changes'] if x['identity'][0]!='pentecost'],'preserve_gap_records':[copy.deepcopy(x) for x in live[TP]['untranslated'] if x['mass'] in ['saint-hildegard-bingen-virgin-doctor-church','saint-john-henry-newman-priest-doctor']],'separate_inherited_metadata_defect':{'current_record':pin(defect),'action':'UNCHANGED; Root owns any truthful digitizer-notice successor separately. This plan carries no metadata correction and no new payload permission.'},'preservation_contract':['All existing positive English entries and unselected refusal dictionaries remain semantically and textually unchanged.','All unselected proper nodes and fields remain semantically unchanged; two Easter option nodes differ only in identical neutral basis.','All unselected Latin sidecar rows remain unchanged. No default, Psalm/Bible, appointment choice or all-cycle alias body is added.','Every Ordinary element except In spiritu remains exactly unchanged; its current English source dictionary/body remains unchanged. Only named Latin dictionary, absent witness append and two source-prose corrections change.','Do not copy any proposed whole inventory snapshot. Recompute finite delta against live selected preimages; stop on mismatch.','Candidates/reviews remain byte-exact. Scratch path strings in frozen archival evidence are resolved by this explicit durable path map, not silently rewritten.','Source evidence beyond mapped metadata/payloads retains its existing acquisition/rights disposition; no PDF/image or protected target carrier is installed.'],'source_grade_limits':{'semen':'Exact full governing OLM1981, independently old fullbody; historical Bute human English; no approved2011.','in-spiritu':'Exact named2008 prayer word sequence proven by full official2022 quote plus independent1862 wholebody; no wider Ordo claim.','ot21':'Qualified complete historical assembly plus new study English; printed2002 fidelity and2008 target unresolved.','all-saints':'Complete1922 historical Latin plus new study English; secondary2002 comparison,2008 unresolved.','easter-three':'Qualified study English only; ancient complete source expressions and separate formulas as declared; no Latin/2008 upgrade.','pentecost-two':'Two receiving uses of unchanged existing study English; official2008 referral/incipits plus secondary wholebody; no complete2008 Latin, branch/default or conclusion expansion.'}}
put('install-plan.json',plan)
put('root-merit-inputs.json',{'schema':'triptych-next-cohort-root-merit-inputs/v1','status':'Review inputs only; no new merits authority asserted','install_plan':pin(str((O/'install-plan.json').relative_to(R))),'english':[{'group':u['group'],'identity':u['identity'],'before':u['live_before_untranslated'],'after':u['after_entry'],'full_english':u['after_english_body'],'body_sha256':u['after_english_body_sha256'],'latin_before':u['live_proper_dictionary'],'grade':plan['source_grade_limits'][u['group']]} for u in english],'latin':latin,'ordinary':ordinary,'neutral_option_basis_updates':appointments,'file_map':list(maps.values()),'excluded_changes':plan['excluded_temporal_changes'],'separate_metadata_defect':plan['separate_inherited_metadata_defect'],'merits_questions':['Accept only each recorded finite full-expression basis and target grade; do not infer modern edition authority from historical availability.','Preserve each approved-English refusal in durable exact proposal and consolidated evidence despite availability of a separate historical/study English route.','Do the live selected preimages and all output qualification checks still match at actual adoption?','Adopt source files and durable independent reviews together; no installed source graph may point only to disposable evidence.']})
print(json.dumps({'plan':pin(str((O/'install-plan.json').relative_to(R))),'file_maps':len(maps),'source_paths':sum(x['destination'].startswith('src/') for x in maps.values()),'root_merit':pin(str((O/'root-merit-inputs.json').relative_to(R)))},indent=2))
