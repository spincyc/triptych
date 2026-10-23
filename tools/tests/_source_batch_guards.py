"""Frozen source-batch partitions and strict historical test-input replay.

This is accounting over a reviewable fixture, never a publication permission or
source-reading oracle. Live body/provenance/rights tests keep using live inputs.
The fixture is a candidate input pin until its separately recorded review closes.
"""
from __future__ import annotations
import copy,hashlib,json,tomllib
from functools import lru_cache
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
YAML_PATH='src/sources/calendars/roman-1962/propers.yaml'
LATIN_PATH='src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml'
def canonical(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(value):return hashlib.sha256(value.encode()if isinstance(value,str)else value).hexdigest()
def require(condition,label):
 if not condition:raise AssertionError('frozen source batch: '+label)
def _bound_manifest_rows(data):
 """Verify the exact bound bytes on every consumption, including warm calls."""
 manifest_path=Path(data['source_input_manifest_path'])
 require(not manifest_path.is_absolute()and '..'not in manifest_path.parts,'manifest must be repository relative')
 try: manifest_raw=(ROOT/manifest_path).read_bytes()
 except OSError as error: raise AssertionError('frozen source batch: source input manifest missing')from error
 require(digest(manifest_raw)==data['source_input_manifest_sha256'],'exact source input manifest bytes')
 manifest=json.loads(manifest_raw)
 return manifest if isinstance(manifest,list)else manifest['files']
@lru_cache(maxsize=1)
def fixture():
 data=json.loads((ROOT/'tools/tests/fixtures/missal-source-batch-20261023.json').read_text())
 require(data['schema']=='triptych-test-source-batch/v1','fixture schema')
 acceptance=data['acceptance']
 require(acceptance['status']=='accepted','source input acceptance is pending')
 relative=Path(acceptance['receipt_path'])
 require(not relative.is_absolute()and '..'not in relative.parts,'receipt must be repository relative')
 try: raw=(ROOT/relative).read_bytes()
 except OSError as error: raise AssertionError('frozen source batch: acceptance receipt missing')from error
 require(digest(raw)==acceptance['receipt_sha256'],'exact acceptance receipt bytes')
 receipt=json.loads(raw)
 require(receipt['status']=='accepted'and receipt['scope']=='missal-source-batch','accepted receipt scope')
 require(receipt['source_input_manifest_sha256']==data['source_input_manifest_sha256'],'acceptance bound to exact source input manifest')
 rows=_bound_manifest_rows(data)
 source_pins={r['path']:r['post_sha256']for r in rows}
 require(len(source_pins)==len(rows),'duplicate source manifest path')
 for relative,want in source_pins.items():
  path=Path(relative)
  require(not path.is_absolute()and '..'not in path.parts,'source manifest path must be repository relative')
  try: current=(ROOT/path).read_bytes()
  except OSError as error: raise AssertionError('frozen source batch: accepted source input missing '+relative)from error
  require(digest(current)==want,'entire accepted source input '+relative)
 for relative,spec in data['files'].items():
  require(source_pins.get(relative)==spec['after_sha256'],'every replay input belongs to accepted input manifest '+relative)
 return data
def key_string(key):return canonical(key.as_dict())
def historical_bytes(relative,current=None):
 """Check the entire frozen current file before reversing explicit raw slices."""
 raw=(ROOT/relative).read_bytes()if current is None else current.encode()if isinstance(current,str)else current
 spec=fixture()['files'].get(relative)
 if spec is None:return raw
 live=(ROOT/relative).read_bytes()
 require(digest(live)==spec['after_sha256'],relative+' entire live bytes')
 require(digest(raw)==spec['after_sha256'],relative+' entire current bytes')
 lines=raw.splitlines(keepends=True);end=0
 for h in spec['hunks']:
  start,stop=h['after_lines'];require(0<=start<=stop<=len(lines)and start>=end,relative+' replacement bounds');end=stop
  require(digest(b''.join(lines[start:stop]))==h['after_slice_sha256'],relative+' exact current slice')
 result=list(lines)
 for h in reversed(spec['hunks']):
  start,stop=h['after_lines'];result[start:stop]=[h['before_utf8'].encode()]
 result=b''.join(result)
 require(digest(result)==spec['before_sha256'],relative+' entire historical bytes')
 return result
def historical_text(relative,current=None):return historical_bytes(relative,current).decode()
def historical_document(document):
 require(digest((ROOT/YAML_PATH).read_bytes())==fixture()['files'][YAML_PATH]['after_sha256'],'entire live document input')
 require(digest(canonical(document))==fixture()['current_roman_document_sha256'],'entire current parsed document before historical replay')
 return yaml.load(historical_bytes(YAML_PATH),Loader=yaml.CSafeLoader)
def assert_current_latin(records,calendar='roman-1962'):
 expected=fixture()['latin_current_rows'][calendar]
 actual={key_string(k):digest(canonical(v))for k,v in records.items()}
 require(set(actual)==set(expected),'exact current Latin owner set '+calendar)
 for key in expected:require(actual[key]==expected[key],'current Latin row '+key)
def historical_latin_records(records,calendar='roman-1962'):
 assert_current_latin(records,calendar)
 base=fixture()['latin_baseline_rows']['roman-1962'if calendar=='roman-pre-1955'else calendar]
 return {k:r for k,r in records.items()if key_string(k)in base}
def assert_permitted_owners(permitted):
 actual={(calendar,key_string(k))for calendar,k,row in permitted}
 expected={('roman-1962',key)for key in fixture()['latin_permitted_keys']}
 require(actual==expected,'exact independently frozen permitted owner identities')
def projection_specs():
 specs=copy.deepcopy(fixture()['new_projection_specs'])
 for row in specs.values():
  for field in ('publication_source_ids','projected_from'):row[field]=set(row[field])
 return specs
def add_projection_specs(specs):
 additions=projection_specs()
 require(set(specs).isdisjoint(additions),'new projection editions cannot override historical literal edition oracles')
 specs.update(additions)
def assert_current_projection_source_files():
 """Preserve every historical projection file plus explicit accepted deltas."""
 data=fixture();expected=dict(data['projection_baseline_source_files'])
 prefix='src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/'
 for row in _bound_manifest_rows(data):
  if row['path'].startswith(prefix):expected[row['path']]=row['post_sha256']
 actual={str(p.relative_to(ROOT)):digest(p.read_bytes())for p in (ROOT/prefix).rglob('*')if p.is_file()}
 require(set(actual)==set(expected),'exact entire current project-projection source-file identities')
 for path,want in expected.items():require(actual[path]==want,'exact current project-projection source file '+path)
def projection_artifact_specs():
 specs=copy.deepcopy(fixture()['new_projection_artifact_specs'])
 for row in specs.values():
  for field in ('publication_source_ids','projected_from'):row[field]=set(row[field])
 return specs
def assert_supplemented_owners(rows):
 actual={key_string(k):ids for k,ids in rows}
 require(len(actual)==len(rows)and actual==fixture()['latin_current_supplements'],'exact supplemented owner/witness pairs')
def assert_live_baseline_bodies(document):
 from _proper_latin import body_owners
 require(digest(canonical(document))==fixture()['current_roman_document_sha256'],'whole current calendar before body partition')
 actual={key_string(k):{'state':s,'body_sha256':digest(b)if b is not None else None}for k,b,s in body_owners(document)}
 require(actual==fixture()['latin_current_bodies'],'all current Latin body identities/states/hashes')
def assert_current_english_entries(entries):
 require({canonical(k):digest(canonical(v))for k,v in entries.items()}==fixture()['roman_current_english_positive'],'exact complete current English dictionary partition')
def historical_english_entries(entries):
 assert_current_english_entries(entries)
 keys=fixture()['english_219_keys']
 selected={k:v for k,v in entries.items()if canonical(k)in keys}
 require({canonical(k):digest(canonical(v))for k,v in selected.items()}==keys,'historical219 English dictionaries')
 return selected

def assert_current_english_coverage(row,calendar):
 expected=fixture()['english_coverage'][calendar]
 require(all(row[k]==v for k,v in expected.items()),'exact declared English identity accounting '+calendar)

def historical_english_coverage(calendar):
 """Check an old coverage claim against its exact source/positive cohort."""
 import runpy
 propers=runpy.run_path(str(ROOT/'tools/mass-propers'))
 document=yaml.load(historical_bytes(YAML_PATH),Loader=yaml.CSafeLoader)
 ledger=tomllib.loads(historical_text('src/sources/inventories/roman-1962-proper-translations-v1.toml'))
 all_targets={canonical(propers['translation_record_identity'](r,document))for table in ('entries','untranslated')for r in ledger[table]}
 require(len(all_targets)==len(ledger['entries'])+len(ledger['untranslated']),'historical English owner categories disjoint')
 positives=set(fixture()['english_219_keys']);require(positives<=all_targets,'historical positive cohort belongs to original target universe')
 excluded=set()
 if calendar=='roman-pre-1955':
  child=tomllib.loads(historical_text('src/sources/inventories/roman-pre-1955-proper-translations-v1.toml'))
  excluded={canonical(propers['translation_record_identity'](r))for r in child['inherited_inapplicable']}
  require(len(excluded)==len(child['inherited_inapplicable']),'historical child suppressions distinct')
  require(excluded<=all_targets,'historical child suppressions belong to parent universe')
 else:require(calendar=='roman-1962','historical English calendar scope')
 targets=all_targets-excluded;available=positives-excluded
 return {'slots':len(targets),'with_english':len(available),'ledgered_untranslated':len(targets-available),'inherited_inapplicable_records':len(excluded)}
def historical_english_source_files():
 """Validate the complete current namespace partition, return old audit hashes.

 The returned historical hashes are never installed as source bytes. In
 particular, an accepted later source-identity qualification stays current.
 """
 data=fixture();expected=dict(data['english_baseline_source_files'])
 prefixes=tuple('src/sources/works/'+n+'/'for n in ('francis-xavier-lasance','eugene-cummiskey','edward-caswall'))
 for row in _bound_manifest_rows(data):
  if row['path'].startswith(prefixes):expected[row['path']]=row['post_sha256']
 actual={}
 for name in ('francis-xavier-lasance','eugene-cummiskey','edward-caswall'):
  for path in (ROOT/'src/sources/works'/name).rglob('*'):
   if path.is_file():actual[str(path.relative_to(ROOT))]=digest(path.read_bytes())
 require(set(actual)==set(expected),'exact entire current English source-file identities')
 for path,want in expected.items():require(actual[path]==want,'exact current English source file '+path)
 historical=data['english_historical_source_files']
 require(set(historical)<=set(actual),'missing original historical English source file')
 return dict(historical)

def historical_english_absence(key):
 rows=fixture()['english_historical_absence_scope']['rows']
 identity=canonical(key)
 require(identity in rows,'unfrozen historical English absence '+identity)
 return copy.deepcopy(rows[identity])

def explicit_cross_supplement(key,extra):
 return canonical([key_string(key),extra])in fixture()['cross_supplement_specs']
def assert_explicit_cross_supplement(key,ids,extra,primary,supplement):
 spec=fixture()['cross_supplement_specs'][canonical([key_string(key),extra])]
 require(ids==spec['publication_source_ids'],'exact cross-printing source array')
 require((primary['id'],primary['edition_id'],supplement['id'],supplement['edition_id'])==(spec['primary_artifact_id'],spec['primary_edition_id'],spec['supplement_artifact_id'],spec['supplement_edition_id']),'exact cross-printing owner/artifact/edition pair')
