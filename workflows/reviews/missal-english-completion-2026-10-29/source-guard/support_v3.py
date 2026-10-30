"""Immutable Git access and historical replay for the bounded source successor."""
from __future__ import annotations
import copy
import tomllib
import difflib
from hashlib import sha256
import json
from pathlib import PurePosixPath
import posixpath
import re
import subprocess

ORIGINAL='2e030b564f4413b735ddbea3061082ebe981b11a'
ANCHOR='6a1fe6e3361fec6d1f011a0ae03a0e47d12fa6cf'
ANCHOR_FIXTURE_SHA='2337ecf91cba462e994bb8630531290a6f5629d6e6914873099d9c77a46e09d4'
HELPER='tools/tests/_source_batch_guards.py'
HELPER_SHA='f60498c9c9f28f72d69d729b1d086044fa3877803327bb4e16d779c479ad55b1'
FIXTURE='tools/tests/fixtures/missal-source-batch-20261023.json'
MANIFEST='tools/tests/fixtures/missal-source-batch-20261023-inputs.json'
HISTORICAL_FIELDS=('schema','baseline_revision','baseline_roman_document_sha256',
 'latin_baseline_rows','latin_baseline_bodies','latin_baseline_present_keys',
 'latin_baseline_supplemented_keys','projection_baseline_source_files','english_219_keys',
 'english_baseline_source_files','english_historical_source_files','english_historical_absence_scope')

def digest(raw):return sha256(raw.encode() if isinstance(raw,str) else raw).hexdigest()
def canonical(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def require(value,message):
 if not value:raise AssertionError('next source parent: '+message)
def relative(value):
 require(isinstance(value,str) and bool(value),'path string required')
 path=PurePosixPath(value)
 require(not path.is_absolute() and '..' not in path.parts and path.as_posix()==value,'canonical repository-relative path required')
 return value
def sha_pin(value):
 require(isinstance(value,str) and bool(re.fullmatch('[0-9a-f]{64}',value)),'explicit SHA256 required')
 return value

class GitObjects:
 def __init__(self,repo):self.repo=repo;self.trees={}
 def kind(self,revision):
  return subprocess.check_output(['git','cat-file','-t',revision],cwd=self.repo,text=True).strip()
 def tree(self,revision):
  if revision not in self.trees:
   raw=subprocess.check_output(['git','ls-tree','-r','-z',revision],cwd=self.repo)
   parsed={}
   for item in raw.split(b'\0'):
    if not item:continue
    metadata,name=item.split(b'\t',1)
    mode,kind,oid=metadata.decode().split()
    parsed[name.decode()]={'mode':mode,'kind':kind,'oid':oid}
   self.trees[revision]=parsed
  return self.trees[revision]
 def raw(self,revision,path):
  return subprocess.check_output(['git','show',revision+':'+relative(path)],cwd=self.repo)
 def blob(self,revision,path):
  path=relative(path);seen=set()
  while True:
   require(path not in seen,'Git source symlink cycle')
   seen.add(path);entry=self.tree(revision).get(path)
   require(entry is not None and entry['kind']=='blob','parent input must exist as a Git blob: '+path)
   raw=self.raw(revision,path)
   if entry['mode']!='120000':return raw
   target=raw.decode()
   require(not PurePosixPath(target).is_absolute(),'external source symlink cannot be bound by immutable Git')
   path=relative(posixpath.normpath(str(PurePosixPath(path).parent/target)))
 def verify_rows(self,revision,rows):
  """Stream ordinary source blobs; use immutable internal links for symlinks."""
  process=subprocess.Popen(['git','cat-file','--batch'],cwd=self.repo,
                           stdin=subprocess.PIPE,stdout=subprocess.PIPE)
  try:
   for row in rows:
    path=relative(row['path']);want=sha_pin(row['post_sha256'])
    entry=self.tree(revision).get(path)
    require(entry is not None and entry['kind']=='blob','every accepted parent input must be published in Git: '+path)
    if entry['mode']=='120000':raw=self.blob(revision,path)
    else:
     process.stdin.write((entry['oid']+'\n').encode());process.stdin.flush()
     header=process.stdout.readline().decode().rstrip().split()
     require(len(header)==3 and header[1]=='blob','invalid Git batch blob')
     raw=process.stdout.read(int(header[2]));require(process.stdout.read(1)==b'\n','Git blob framing')
    require(digest(raw)==want,'entire immutable parent input: '+path)
  finally:
   process.stdin.close();process.stdout.close();require(process.wait()==0,'Git batch failed')

def reverse(current,spec):
 require(digest(current)==spec['after_sha256'],'entire parent replay after bytes')
 lines=current.splitlines(keepends=True);end=0
 for hunk in spec['hunks']:
  start,stop=hunk['after_lines']
  require(type(start) is int and type(stop) is int and 0<=start<=stop<=len(lines) and start>=end,'ordered inverse bounds')
  require(digest(b''.join(lines[start:stop]))==hunk['after_slice_sha256'],'entire inverse after slice')
  end=stop
 for hunk in reversed(spec['hunks']):
  start,stop=hunk['after_lines'];lines[start:stop]=[hunk['before_utf8'].encode()]
 result=b''.join(lines)
 require(digest(result)==spec['before_sha256'],'entire original inverse before bytes')
 return result

def replay_spec(before,after):
 old=before.decode().splitlines(keepends=True);new=after.decode().splitlines(keepends=True)
 hunks=[]
 for operation,i,j,k,l in difflib.SequenceMatcher(a=old,b=new).get_opcodes():
  if operation!='equal':hunks.append({'after_lines':[k,l],'after_slice_sha256':digest(''.join(new[k:l])),'before_utf8':''.join(old[i:j])})
 spec={'before_sha256':digest(before),'after_sha256':digest(after),'hunks':hunks}
 require(reverse(after,spec)==before,'new inverse must preserve original bytes')
 return spec



def ledger(raw,key):
    table=tomllib.loads(raw.decode());result={}
    for entry in table['entries']:
        row={**table.get('defaults',{}),**entry};identity=canonical(key.from_mapping(row).as_dict())
        require(identity not in result,'duplicate Latin owner');result[identity]=row
    return result


def hashrows(rows):return {key:digest(canonical(row)) for key,row in rows.items()}


def english_ledger(raw,doc,owner):
    table=tomllib.loads(raw.decode());maps={}
    for field in ('entries','untranslated'):
        rows={canonical(owner['translation_record_identity'](row,doc)):row for row in table[field]}
        require(len(rows)==len(table[field]),'duplicate/overlapping English owner')
        maps[field]=rows
    require(not set(maps['entries'])&set(maps['untranslated']),'English partitions overlap')
    aux={k:v for k,v in table.items() if k not in ('entries','untranslated')}
    return maps['entries'],maps['untranslated'],aux


def projection_oracles(source,prior,parsed,newkeys,changed):
    """Only active permitted prayer proofs create prayer oracles; preserve history."""
    indexes={}
    def artifact(identifier):
        _,author,work,edition,name=identifier.split('.')
        namespace=(author,work)
        if namespace not in indexes:
            found={}
            for path in (source/'src/sources/works'/author/work/'editions').glob('*/artifacts/*/artifact.toml'):
                row=tomllib.loads(path.read_text());require(row['id'] not in found,'duplicate artifact ID')
                found[row['id']]=row
            indexes[namespace]=found
        return indexes[namespace][identifier]
    editions,artifacts,cross={},{},{}
    for key in newkeys+changed:
        row=parsed[key]
        if row['publication_status']!='permitted':continue
        ids=row['publication_source_ids'];projection=artifact(ids[0])
        require(ids[0].startswith('artifact.triptych.roman-1962-latin-proper-editorial-projection.'),'permitted proof needs exact project projection')
        item={'artifact_id':ids[0],'publication_source_ids':[ids[1]],'projected_from':sorted(projection['projected_from'])}
        if ids[0] in artifacts:
            old=artifacts[ids[0]];require(old['projected_from']==item['projected_from'],'projection witnesses changed')
            item['publication_source_ids']=sorted(set(old['publication_source_ids'])|set(item['publication_source_ids']))
        artifacts[ids[0]]=item;edition=ids[0].split('.')[3]
        ed=editions.setdefault(edition,copy.deepcopy(item))
        if edition in prior['new_projection_specs']:ed['artifact_id']=prior['new_projection_specs'][edition]['artifact_id']
        for field in ('publication_source_ids','projected_from'):ed[field]=sorted(set(ed[field])|set(item[field]))
        primary=artifact(ids[1])
        for extra in ids[2:]:
            supplement=artifact(extra)
            if primary['edition_id']!=supplement['edition_id']:
                cross[canonical([key,extra])]={'publication_source_ids':ids,'primary_artifact_id':primary['id'],
                    'primary_edition_id':primary['edition_id'],'supplement_artifact_id':supplement['id'],'supplement_edition_id':supplement['edition_id']}
    active=set(editions)
    for edition,item in prior['new_projection_specs'].items():
        if edition not in editions:editions[edition]=copy.deepcopy(item)
        else:
            require(editions[edition]['artifact_id']==item['artifact_id'],'historical edition representative changed')
            for field in ('publication_source_ids','projected_from'):editions[edition][field]=sorted(set(editions[edition][field])|set(item[field]))
    for old,current in ((prior['new_projection_artifact_specs'],artifacts),(prior['cross_supplement_specs'],cross)):
        for identity,item in old.items():
            require(identity not in current or canonical(item)==canonical(current[identity]),'historical artifact/cross witness oracle changed')
            current[identity]=copy.deepcopy(item)
    return editions,artifacts,cross,active


def direct_pd_oracles(source, pins, parsed, bodies, texts, validated, decide,
                      key_class, surfaces, declaration):
    """Bind exactly the adopted direct-source class, separately from projections."""
    require(declaration.get('schema') == 'triptych-exact-direct-pd-latin-proof-declaration/v1'
            and declaration.get('calendar') == 'roman-1962', 'exact direct-PD declaration type')
    require(declaration.get('required_surfaces') == sorted(surfaces), 'direct-PD surface scope')
    rows = declaration.get('records')
    require(isinstance(rows, list) and len(rows) == 25, 'exact25 direct-PD records')
    expected = {canonical(row['key']): row for row in rows}
    require(len(expected) == 25, 'distinct direct-PD target tuples')
    prefix = 'artifact.triptych.roman-1962-latin-proper-editorial-projection.'
    actual = {key: row for key, row in parsed.items()
              if row['publication_status'] == 'permitted'
              and not (row.get('publication_source_ids')
                       and row['publication_source_ids'][0].startswith(prefix))}
    require(set(actual) == set(expected), 'complete exact direct-PD partition; no missing or extra target')
    artifacts = declaration.get('primary_artifacts')
    require(isinstance(artifacts, list) and len(artifacts) == 3, 'exact3 direct-PD artifacts')
    artifact_ids = {artifact['id'] for artifact in artifacts}
    require(len(artifact_ids) == 3 and artifact_ids == {
        row['record']['publication_source_ids'][0] for row in rows
    }, 'direct-PD primary artifact partition')
    for artifact in artifacts:
        path, payload = relative(artifact['path']), relative(artifact['payload_path'])
        for dependency, expected_sha in ((path, artifact['sha256']),
                                         (payload, artifact['payload_sha256'])):
            require(pins.get(dependency) == expected_sha
                    and digest((source / dependency).read_bytes()) == expected_sha,
                    'exact declared direct-PD artifact input ' + dependency)
        metadata = tomllib.loads((source / path).read_text())
        require(canonical(metadata) == canonical(artifact['record'])
                and metadata['id'] == artifact['id']
                and metadata['rights_status'] == 'public-domain'
                and metadata['path'] == payload
                and metadata['sha256'] == artifact['payload_sha256']
                and metadata['byte_size'] == artifact['payload_bytes']
                == (source / payload).stat().st_size, 'entire direct-PD artifact record and payload')
    result = {}
    for key, expected_row in expected.items():
        record = actual[key]
        require(canonical(record) == canonical(expected_row['record']),
                'entire exact direct-PD proof dictionary ' + key)
        require(record['publication_basis'] == 'public-domain'
                and set(record['surfaces']) == set(surfaces), 'direct-PD basis and surfaces ' + key)
        text = texts.get(key)
        require(isinstance(text, str) and bool(text.strip())
                and bodies.get(key) == {'state': 'present', 'body_sha256': expected_row['body_sha256']}
                and digest(text) == expected_row['body_sha256'], 'entire direct-PD body ' + key)
        identity = key_class(**expected_row['key'])
        require(canonical(validated.get(identity)) == canonical(record),
                'actual validated production proof record ' + key)
        decision = decide(identity, text, validated)
        require(decision.permits(surfaces) and not decision.reason,
                'actual production decision permits direct-PD body ' + key)
        require(canonical(decision.projection(surfaces)) == canonical(expected_row['production_decision']),
                'entire actual production decision projection ' + key)
        result[key] = copy.deepcopy(expected_row)
    return result
