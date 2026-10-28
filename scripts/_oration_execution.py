"""Finite literal-source partitions for six dated Roman1962 RG110 contexts.

This is a separate source/execution mapping. It never creates an ordinary
translation, changes an absence, expands a cue, or supplies a companion text.
"""
from __future__ import annotations
import hashlib,json,re,tomllib,unicodedata
from pathlib import Path

METHOD_ID='roman-1962-rg110-six-source-execution-20261026'
AUTHORITY_PATH='workflows/reviews/reader-completion-2026-10-26/oration-execution-six-authority.json'
AUTHORITY_SHA256='9ad680a26652ed2e8c9982a04884e517ab7bdbee8b17131bb1d524c1c256580d'
SOURCE_SCHEMA='triptych-oration-execution-source-record/v1'
PUBLIC_SCHEMA='triptych-oration-execution-source/v1'
HOSTS={'commemoratione-s-pauli-apostoli':('comm-s-petri-apostoli-2','06-30','edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945'),'cathedrae-s-petri-apostoli':('comm-s-pauli-apostoli','02-22','edition.gaspar-lefebvre.daily-missal-with-vespers.saint-andre-lohmann-1925')}
TARGETS={(host,'main',slot,'all',1)for host in HOSTS for slot in ('Collect','Secret','Postcommunion')}
PUBLIC_FIELDS={'schema','method_id','record_sha256','target','lang','source_id','source_label','source_aliases','source_text','source_sha256','offset_units','ranges','target_latin_sha256','target_proof_sha256','fixed_date','companion','provenance','scope','rule'}
def sha(value):return hashlib.sha256(value.encode()if isinstance(value,str)else value).hexdigest()
def canonical(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def require(condition,message):
    if not condition:raise ValueError('oration execution source: '+message)
def words(value):
    value=value.casefold().replace('æ','ae').replace('œ','oe')
    return re.findall('[a-z]+|[0-9]+',''.join(c for c in unicodedata.normalize('NFKD',value)if not unicodedata.combining(c)))
def utf16(text,position):return len(text[:position].encode('utf-16-le'))//2
def validate_partition(text,parts,cue):
    require(isinstance(text,str)and text and isinstance(parts,list)and len(parts)==3,'three source parts required')
    require([p.get('kind')for p in parts]==['petition','separator','printed-conclusion-cue'],'cue is source text, never a rubric or an empty formula')
    cursor=0
    for part in parts:
        require(set(part)=={'kind','start','end','utf8_start','utf8_end'},'unknown source range field')
        a,b=part['start'],part['end'];require(type(a)is int and type(b)is int and a==cursor and a<=b<=len(text),'source codepoint partition gap, overlap or bound')
        require(part['utf8_start']==len(text[:a].encode())and part['utf8_end']==len(text[:b].encode()),'UTF8 and Unicode codepoint bounds disagree')
        cursor=b
    require(cursor==len(text)and parts[0]['end']>0,'whole source suffix lost or petition empty')
    require(text[parts[1]['start']:parts[1]['end']].isspace(),'separator must preserve exact source whitespace')
    require(isinstance(cue,str)and cue and text[parts[2]['start']:parts[2]['end']]==cue,'actual printed source cue required')
    require(''.join(text[p['start']:p['end']]for p in parts)==text,'source reconstruction differs')

def public_projection(record):
    binding=record['source_binding'];text=binding['translations'][0]['text'];comp=record['companion'];ce=comp['english_binding']['translations'][0]
    return {'schema':PUBLIC_SCHEMA,'method_id':METHOD_ID,'record_sha256':sha(canonical(record)),'target':record['target'],'lang':'en','source_id':record['source_id'],'source_label':record['source_label'],'source_aliases':record['source_aliases'],'source_text':text,'source_sha256':sha(text),'offset_units':'utf16','ranges':[{'kind':p['kind'],'start':utf16(text,p['start']),'end':utf16(text,p['end'])}for p in record['english_parts']],'target_latin_sha256':record['target_latin_sha256'],'target_proof_sha256':record['target_proof_sha256'],'fixed_date':record['relation']['month_day'],'companion':{'target':comp['target'],'latin_sha256':comp['latin_sha256'],'proof_sha256':comp['proof_sha256'],'source_id':ce['source_id'],'source_text':ce['text'],'source_sha256':comp['english_sha256'],'cue_state':comp['cue_state'],'cue':comp['cue'],'family':comp['family'],'unbound_name':bool(re.search(r'\bN\.',ce['text']))},'provenance':{'kind':'historical-source-execution','publication_passage_id':binding['publication_passage_id'],'companion_publication_passage_id':comp['english_binding']['publication_passage_id']},'scope':'dated-mass-of-office','rule':'RG110'}

def authority(repository):
    path=Path(repository)/AUTHORITY_PATH;raw=path.read_bytes()
    require(sha(raw)==AUTHORITY_SHA256,'finite durable authority changed; a successor needs independent review')
    value=json.loads(raw);require(value['schema']=='triptych-finite-oration-execution-authority/v1'and value['id']==METHOD_ID,'wrong authority schema or method')
    rows=value['records'];require(len(rows)==6 and {tuple(r['target'])for r in rows}==TARGETS,'authority must close exactly six targets')
    return {tuple(r['target']):r for r in rows}

def validate_public(value,repository):
    require(isinstance(value,dict)and set(value)==PUBLIC_FIELDS,'unknown/missing public field or private carrier')
    require(value['schema']==PUBLIC_SCHEMA and value['method_id']==METHOD_ID and value['lang']=='en','unknown public execution source schema, method or language')
    key=tuple(value['target']);expected=authority(repository)
    require(key in expected and sha(canonical(value))==expected[key]['public_sha256'],'public source/body/part/proof differs from finite source authority')
    text=value['source_text'];require(sha(text)==value['source_sha256'],'public source hash differs')
    require(value['offset_units']=='utf16','browser offsets must state UTF16')
    raw=text.encode('utf-16-le');cursor=0
    for part in value['ranges']:
        require(set(part)=={'kind','start','end'}and type(part['start'])is int and type(part['end'])is int,'unknown public range field')
        require(part['start']==cursor and cursor<=part['end']<=len(raw)//2,'public source range gap/overlap/bound')
        try:raw[part['start']*2:part['end']*2].decode('utf-16-le')
        except UnicodeDecodeError as error:raise ValueError('oration execution source: surrogate boundary split')from error
        cursor=part['end']
    require(cursor==len(raw)//2,'public full source suffix lost')
    return value

def load_sources(calendar_root,calendar,owner):
    if calendar!='roman-1962':return {}
    calendar_root=Path(calendar_root);repository=calendar_root.resolve().parents[2]
    path=calendar_root.parent/'inventories/roman-1962-proper-translations-v1.toml'
    ledger=tomllib.loads(path.read_text())
    if 'execution_sources' not in ledger:return {}
    rows=ledger['execution_sources']
    require(isinstance(rows,list),'execution source section must be an array')
    expected=authority(repository);require(len(rows)==6,'execution source section must contain exactly six finite rows')
    document=owner.load_calendar(calendar_root,calendar);masses={m['key']:m for _,m in owner.masses_of(document)}
    _,_,_,witnesses=owner.translation_overlay(calendar,calendar_root)
    records,_=owner._source_library_records(calendar_root)
    proofs=tomllib.loads((calendar_root.parent/'inventories/roman-1962-proper-latin-provenance-v1.toml').read_text())['entries']
    positive={owner.translation_record_identity(r,document):r for r in ledger['entries']}
    result={}
    def target_body(key):
        matches=[p for p in masses[key[0]]['propers']if p['name']==key[2]]
        require(len(matches)==1,'target proper/occurrence is not unique')
        matches_proof=[p for p in proofs if p['mass']==key[0]and p['proper']==key[2]and p['occurrence']==key[4]]
        require(len(matches_proof)==1,'complete target proof is not unique')
        return matches[0]['text'],matches_proof[0]
    for raw in rows:
        require(set(raw)=={'target','method_id','record_json'},'unknown execution-source sidecar field')
        key=tuple(raw['target']);require(key in TARGETS and key not in result and raw['method_id']==METHOD_ID,'unlisted/repeated source target or method')
        record=json.loads(raw['record_json'])
        require(record['target']==raw['target']and sha(canonical(record))==expected[key]['record_sha256'],'complete source record differs from immutable method authority')
        host,slot=key[0],key[2];companion,date,source=HOSTS[host]
        require(record['schema']==SOURCE_SCHEMA and record['lang']=='en'and record['source_id']==source and record['method_id']==METHOD_ID,'source identity/language/schema differs')
        binding=record['source_binding'];require(owner.translation_record_identity(binding,document)==key,'full source binding target differs')
        owner.validate_translation_payload(binding,path,witnesses);owner.validate_translation_publication_binding(binding,calendar_root,path,witnesses)
        english=binding['translations'][0]['text'];latin=record['historical_latin']
        validate_partition(english,record['english_parts'],record['source_english_cue']);validate_partition(latin,record['latin_parts'],record['source_latin_cue'])
        require(sha(latin)==record['historical_latin_sha256'],'full historical Latin changed')
        body,proof=target_body(key)
        require(body==record['target_latin']and sha(body)==record['target_latin_sha256']and proof==record['target_proof']and sha(canonical(proof))==record['target_proof_sha256'],'full current host target or proof changed')
        source_petition=words(latin[:record['latin_parts'][0]['end']]);target=words(body)
        require(len(source_petition)==len(target),'complete petition length differs')
        diffs=[(i,s,t)for i,(s,t)in enumerate(zip(source_petition,target))if s!=t]
        if host=='commemoratione-s-pauli-apostoli'and slot=='Collect':
            require(diffs==[(14,'natalitia','natalicia')],'only exact natalitia/natalicia at global14')
            change=record['petition_comparison']['differences'][0];parse=change['parse']
            require((parse['case'],parse['number'],parse['gender'])==('accusative','plural','neuter')and'colimus'in parse['context'],'particular neuter accusative plural context required')
            for identifier in change['source_passage_ids']:require(identifier in records,'lexical source not installed')
        elif host=='cathedrae-s-petri-apostoli'and slot=='Collect':require(diffs==[(9,'coelestis','caelestis')],'only exact separately recorded spelling at global9')
        else:require(not diffs,'unlisted petition word difference')
        context=records.get(record['source_context_passage_id'])
        require(context and context['artifact_id']==binding['artifact_id']and context['artifact_sha256']==records[binding['artifact_id']]['sha256']and context['artifact_page_ranges']==[[min(record['source_context_pages']),max(record['source_context_pages'])]]and'inspected'in context['states']and'verified'in context['states'],'own-appointment/referral source context differs')
        comp=record['companion'];ckey=(companion,key[1],slot,key[3],key[4]);cb,cp=target_body(ckey)
        require(tuple(comp['target'])==ckey and cb==comp['latin']and sha(cb)==comp['latin_sha256']and cp==comp['proof']and sha(canonical(cp))==comp['proof_sha256'],'complete current companion target/proof changed')
        require(positive[ckey]==comp['english_binding']and sha(canonical(positive[ckey]))==comp['english_binding_sha256'],'companion literal English source binding changed')
        owner.validate_translation_publication_binding(positive[ckey],calendar_root,path,witnesses)
        ce=positive[ckey]['translations'][0]['text'];require(sha(ce)==comp['english_sha256'],'companion English changed')
        require(comp['cue_state']in {'printed','not-printed'}and((comp['cue_state']=='printed'and comp['cue']and ce.endswith(comp['cue']))or(comp['cue_state']=='not-printed'and comp['cue']=='')),'English cue must be literally printed or explicitly not printed')
        require(comp['family']==('addressed-to-son'if host=='commemoratione-s-pauli-apostoli'and slot=='Collect'else'through-our-lord'),'companion conclusion family cannot come from host')
        relation=record['relation'];require(relation['host']==host and relation['companion']==companion and relation['slot']==slot and relation['month_day']==date and relation['scope']=='dated-mass-of-office'and relation['rule']=='RG110'and relation['conclusion_provider']=='separately-verified-companion-only','unlisted execution relation')
        result[key]=validate_public(public_projection(record),repository)
    require(set(result)==TARGETS,'finite source partition incomplete')
    return result
