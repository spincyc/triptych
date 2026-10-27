"""Two adopted name/span inferences; never an ordinary translation or resolver."""
from pathlib import Path
import csv,hashlib,json,re,tomllib,unicodedata
METHOD='roman-1962-finite-name-two-20261026'
AUTHORITY='workflows/reviews/reader-completion-2026-10-26/finite-name-two-authority.json'
AUTHORITY_SHA='d76fd673914273e464b9e837d31826dd5aafcad4dbee1ae207f284383191713d'
ADOPTION='workflows/reviews/reader-completion-2026-10-26/finite-name-two-root-adoption.json'
ADOPTION_SHA='b4c1dcf2a7f5b27bda5f8e2fe298cd178a576553af97c1d36e025243a1512ae2'
TARGETS={('s-patricii-episcopi-confessoris','main','Postcommunion','all',1),('s-antonii-abbatis','main','Collect','all',1)}
SOURCE='edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945'
PUBLIC_FIELDS={'schema','method_id','target','accepted_date','calendar','required_role','terminal_common','source_id','source_aliases','source_label','template','name_controller','canonical_latin_sha256','canonical_proof_sha256','canonical_proof_owner','common_latin_sha256','common_proof_sha256','named_normative_latin_sha256','conclusion','applicability_rule','inference','record_sha256','offset_units','recipient_source_relation'}
def sha(v):return hashlib.sha256(v.encode()if isinstance(v,str)else v).hexdigest()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def need(v,message):
    if not v:raise ValueError('finite name execution: '+message)
def words(v):return re.findall('[a-z]+',''.join(c for c in unicodedata.normalize('NFKD',v.casefold().replace('æ','ae').replace('œ','oe'))if not unicodedata.combining(c)))
def u16(v,p):return len(v[:p].encode('utf-16-le'))//2
def span(v,p,literal):
    need(set(p)=={'literal','codepoint_range','full_source_sha256'},'unknown span field')
    a,b=p['codepoint_range'];need(type(a)is int and type(b)is int and 0<=a<b<=len(v),'invalid codepoint span');need(v[a:b]==literal==p['literal']and sha(v)==p['full_source_sha256'],'whole controller or literal span changed')
    return {'start':u16(v,a),'end':u16(v,b)}
def public_projection(r):
    text=r['template_text'];name=r['name_controller'];cue=r['conclusion'];a,b=r['placeholder']['codepoint_range'];na,nb=name['span']['codepoint_range'];ending=cue['literal_english_cue']
    return dict(schema='triptych-finite-name-execution-source/v1',offset_units='utf16',method_id=METHOD,target=r['target'],accepted_date=r['date'],calendar='roman-1962',required_role=r['required_role'],recipient_source_relation=r['recipient_source_relation'],terminal_common=r['terminal_common'],source_id=r['source_id'],source_aliases=r['source_aliases'],source_label=r['source_label'],template=dict(text=text,sha256=r['template_sha256'],placeholder=dict(start=u16(text,a),end=u16(text,b)),publication_passage_id=r['template_binding']['publication_passage_id'],binding_sha256=r['template_binding_sha256']),name_controller=dict(text=name['text'],sha256=name['sha256'],name_span=dict(start=u16(name['text'],na),end=u16(name['text'],nb)),publication_passage_id=name['publication_passage_id'],kind=name['kind']),canonical_latin_sha256=r['canonical_latin_sha256'],canonical_proof_sha256=r['canonical_proof_sha256'],canonical_proof_owner=r['canonical_proof_owner'],common_latin_sha256=r['common_latin_sha256'],common_proof_sha256=r['common_proof_sha256'],named_normative_latin_sha256=r['normative_named_controller']['whole_named_latin_sha256'],conclusion=dict(state='separately-proved-source-prefix',family=cue['family'],literal_english_cue=ending,cue_span=dict(start=u16(text,len(text)-len(ending)),end=u16(text,len(text))),table_sha256=cue['formula_controller']['sha256'],table_publication_passage_id=cue['formula_controller']['transcription_passage_id'],named_target_prefix_sha256=sha(cue['actual_named_target_cue']),named_target_prefix_tokens=len(cue['actual_named_target_cue_tokens'])),applicability_rule=dict(id='RG108;RG111a',controller_sha256=sha(canonical(r['mass_use_controller']))),inference=dict(root_adoption_sha256=r['approval_sha256'],source_review_sha256=r['independent_review_sha256'],source_facts_sha256=r['source_facts_sha256'],historically_named_English=False,ordinary_admissions=0),record_sha256=sha(canonical(r)))
def authority(repository):
    root=Path(repository);raw=(root/AUTHORITY).read_bytes();need(sha(raw)==AUTHORITY_SHA,'method authority changed; reviewed successor required');v=json.loads(raw)
    need(v['method_id']==METHOD and len(v['records'])==2 and {tuple(r['target'])for r in v['records']}==TARGETS,'exact two method targets required');a=(root/ADOPTION).read_bytes();need(sha(a)==ADOPTION_SHA,'coordinator adoption changed');return {tuple(r['target']):r for r in v['records']},json.loads(a)
def validate_public(v,repository):
    need(isinstance(v,dict)and set(v)==PUBLIC_FIELDS,'unknown/missing public field or private carrier');rows,_=authority(repository);key=tuple(v['target']);need(key in TARGETS and sha(canonical(v))==rows[key]['public_sha256'],'public source, proof, conclusion or scope changed')
    template=v['template'];name=v['name_controller'];need(sha(template['text'])==template['sha256']and sha(name['text'])==name['sha256'],'whole public controller changed')
    for text,p,literal in [(template['text'],template['placeholder'],'N.'),(name['text'],name['name_span'],'Patrick'if key[0].startswith('s-patricii')else'Anthony')]:
        a,b=p['start'],p['end'];raw=text.encode('utf-16-le');need(type(a)is int and type(b)is int and 0<=a<b<=len(raw)//2,'invalid UTF16 range')
        try:value=raw[2*a:2*b].decode('utf-16-le')
        except UnicodeDecodeError as error:raise ValueError('finite name execution: surrogate split')from error
        need(value==literal,'literal source interval differs')
    return v

def validate_native(r,targets,entries,proofs,repository,owner=None,calendar_root=None):
    rows,adoption=authority(repository);key=tuple(r['target']);need(key in TARGETS and sha(canonical(r))==rows[key]['record_sha256'],'unadopted/changed complete native record');grant=next(x for x in adoption['exact_contexts']if tuple(x['recipient'])==key)
    need(r['schema']=='triptych-finite-name-execution-record/v1'and r['method_id']==METHOD and r['calendar']=='roman-1962'and r['source_id']==SOURCE,'wrong method/source/calendar');template=r['template_text'];name=r['name_controller'];span(template,r['placeholder'],'N.');span(name['text'],name['span'],grant['English_name_span']['literal'])
    need(template.count('N.')==1 and sha(template)==grant['source_template_sha256']and sha(name['text'])==grant['English_name_controller_sha256'],'not exact singular whole template/name controller');need(r['date']==grant['date']and r['required_role']==grant['required_execution_role'],'different dated source role');target=targets[key];common_key=tuple(r['terminal_common']);common=targets[common_key]
    need(isinstance(target.get('text'),str)and isinstance(common.get('text'),str),'current canonical body missing');need(sha(target['text'])==r['canonical_latin_sha256']==grant['canonical_Latin_sha256']and sha(common['text'])==r['common_latin_sha256'],'current whole canonical recipient/Common differs');need(target.get('taken_from')==r['recipient_source_relation'],'actual recipient/Common source relation changed');named=r['normative_named_controller'];need(named['whole_named_latin_sha256']==grant['named_normative_Latin_sha256']and named['actual_name_span']==grant['actual_Latin_name_span'],'named normative controller changed')
    if key[0].startswith('s-patricii'):need(r['canonical_proof_owner']==common_key[0]and r['canonical_latin_sha256']!=named['whole_named_latin_sha256']and re.search(r'\bN\.',target['text'])and target['taken_from']['mass']==common_key[0],'Patrick canonical N/Common proof must remain distinct from named Patricio')
    else:need(r['canonical_proof_owner']==key[0]and r['canonical_latin_sha256']==named['whole_named_latin_sha256'],'Anthony own named canonical controller changed')
    for field,pkey in [('canonical_proof',(r['canonical_proof_owner'],key[2])),('common_proof',(common_key[0],key[2]))]:need(proofs[pkey]==r[field]and sha(canonical(r[field]))==r[field+'_sha256'],'complete current proof differs')
    binding=r['template_binding'];need(entries[common_key]==binding and sha(canonical(binding))==r['template_binding_sha256']and binding['translations'][0]['text']==template,'whole template positive binding changed')
    if owner is not None:
        _,_,_,witnesses=owner.translation_overlay('roman-1962',calendar_root);owner.validate_translation_payload(binding,Path('name_execution_sources'),witnesses);owner.validate_translation_publication_binding(binding,calendar_root,Path('name_execution_sources'),witnesses)
    if name['existing_binding']:
        k=tuple(name['existing_binding'][x]for x in ['mass','form_id','proper','cycle','occurrence']);need(entries[k]==name['existing_binding']and name['existing_binding']['translations'][0]['text']==name['text'],'literal own-Collect controller changed')
        if owner is not None:owner.validate_translation_publication_binding(name['existing_binding'],calendar_root,Path('name_execution_sources'),witnesses)
    else:
        artifact=name['new_publication']['artifact'];raw=(Path(repository)/artifact['path']).read_bytes();need(sha(raw)==artifact['sha256']and len(raw)==artifact['byte_size']and artifact['derived_from']==binding['artifact_id']and artifact['rights_status']=='public-domain','heading publication changed');data=list(csv.DictReader(raw.decode().splitlines(),delimiter='\t'));need(len(data)==1 and data[0]['controller_id']=='anthony-january17-heading'and json.loads(data[0]['english_json'])==name['text'],'whole literal heading row changed')
        for kind in ['verification','publication']:
            pub=name['new_publication'];actual=tomllib.loads((Path(repository)/pub[kind+'_path']).read_text());need(actual==pub[kind+'_record'],'complete heading verification/publication controller changed')
        verify=name['new_publication']['verification_record'];published=name['new_publication']['publication_record'];need(verify['artifact_id']==binding['artifact_id']and verify['artifact_sha256']=='6cf3c3d01b853bc4a35c1cc9b0a4e54a0489a5ccf5d9a742bb681ac10608ce70'and verify['artifact_page_ranges']==[[867,867]]and published['artifact_id']==artifact['id']and published['artifact_sha256']==artifact['sha256']and published['physical_line_ranges']==[[2,2]],'heading physical/source-row join differs')
    cue=r['conclusion'];control=cue['formula_controller'];raw=(Path(repository)/control['path']).read_bytes();need(sha(raw)==control['sha256'],'same-book conclusion controller changed');table=json.loads(raw);ordinary=next(x for x in table['formulas']if x['key']=='through-our-lord');actual=words(cue['actual_named_target_cue']);need(actual==cue['actual_named_target_cue_tokens']==words(ordinary['full_latin'])[:len(actual)]and len(actual)==(5 if key[0].startswith('s-patricii')else 14),'independent named-target conclusion prefix differs');need(cue['family']=='through-our-lord'and cue['source_latin_cue']=='Per Dominum.'and cue['literal_english_cue']==ordinary['short_english']=='Through our Lord.'and template.endswith(ordinary['short_english']),'English ending cannot change or expand')
    return validate_public(public_projection(r),repository)

def load_name_sources(calendar_root,calendar,owner):
    if calendar!='roman-1962':return {}
    root=Path(calendar_root);repository=root.resolve().parents[2];path=root.parent/'inventories/roman-1962-proper-translations-v1.toml';ledger=tomllib.loads(path.read_text())
    if 'name_execution_sources'not in ledger:return {}
    rows=ledger['name_execution_sources'];need(isinstance(rows,list)and len(rows)==2,'exact two name source rows required');document=owner.load_calendar(root,calendar);targets={}
    for _,mass in owner.masses_of(document):
        if mass['key']not in {k[0]for k in TARGETS}|{'commune-abbatum','commune-confessoris-pontificis-1'}:continue
        seen={}
        for form,proper,taken in owner.appointed_propers(document,mass):
            form_id=owner.form_id_for_label(mass,form);label=(form_id,proper['name']);seen[label]=seen.get(label,0)+1;targets[(mass['key'],form_id,proper['name'],'all',seen[label])]={'text':proper.get('text'),'taken_from':taken or None}
    entries={owner.translation_record_identity(r,document):r for r in ledger['entries']};raw_proofs=tomllib.loads((root.parent/'inventories/roman-1962-proper-latin-provenance-v1.toml').read_text())['entries'];proofs={(r['mass'],r['proper']):r for r in raw_proofs if r['occurrence']==1 and not r['form']and not r['cycle']};result={}
    for row in rows:
        need(set(row)=={'target','method_id','record_json'}and row['method_id']==METHOD,'unknown name sidecar field/method');key=tuple(row['target']);record=json.loads(row['record_json']);need(key==tuple(record['target'])and key not in result,'repeated/wrong name target');result[key]=validate_native(record,targets,entries,proofs,repository,owner,root)
    need(set(result)==TARGETS,'incomplete name source set');return result
