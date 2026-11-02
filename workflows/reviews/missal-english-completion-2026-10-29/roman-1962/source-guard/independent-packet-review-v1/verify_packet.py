"""Verify exact pending packet mechanics; no rights or translation judgment."""
import argparse
import ast
from collections import Counter
from hashlib import sha256
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
from pathlib import Path
import re
import sys
import subprocess
import tempfile
import tomllib
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents
            if (parent / 'tmt.json').is_file() and (parent / 'tools/source-library').is_file())
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out', required=True, help='new reviewer-owned directory below repository .scratch')
parser.add_argument('--runtime-authority-sha256', help='permit only reviewed guard-constant activation for this exact adopted authority')
parser.add_argument('--installed-sources', action='store_true', help='verify the planned installed rows/controllers instead of freezing the preparatory sidecar bytes')
args = parser.parse_args()
assert not args.installed_sources or args.runtime_authority_sha256, 'installed sources require the exact runtime authority hash'
WORK = Path(args.out)
if not WORK.is_absolute(): WORK = ROOT / WORK
WORK = WORK.resolve()
assert WORK.is_relative_to(ROOT / '.scratch') and not WORK.exists(), 'new repository scratch output required'
WORK.mkdir(parents=True)
PACKET = HERE.parent
KEYS = ('mass', 'form', 'proper', 'course', 'cycle', 'occurrence')
TYPES = {'work', 'edition', 'artifact', 'segment', 'passage', 'corpus'}
ID = re.compile(r'^(work|edition|artifact|segment|passage|corpus)\.[a-z0-9.-]+$')
NOTICE = 'Qualified United States editorial assessment of this exact adaptation under publication policy section 1 priority 6; moderate confidence. The source record preserves the opposing originality argument. This is not holder permission or an unqualified public-domain claim. Triptych owns only its editorial carrier.'


def h(raw): return sha256(raw).hexdigest()
def canon(value): return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
def dh(value): return h(canon(value))
def read(path):
    path = ROOT / path
    assert path.resolve().is_relative_to(ROOT) and not path.is_symlink()
    return path.read_bytes()
def identifiers(value):
    if isinstance(value, str): return {value} if ID.fullmatch(value) else set()
    if isinstance(value, list): return set().union(*(identifiers(x) for x in value)) if value else set()
    if isinstance(value, dict): return set().union(*(identifiers(x) for x in value.values())) if value else set()
    return set()
def pointer(value, path):
    for part in path.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


authority = json.loads((PACKET / 'candidate-authority-v1.json').read_bytes())
declaration = json.loads((PACKET / 'declaration-v1.json').read_bytes())
assert authority['state'] == declaration['state'] == 'pending-root-adoption'
assert declaration['activation_performed'] is False and declaration['code_or_authority_mutation'] is False
assert declaration['allow_pending_receipts'] is False
assert declaration['pending_source_reviews'] == declaration['unbound_body_receipts'] == []
installation_input_deltas = []
for kind in ('inputs', 'plans', 'receipts', 'outputs'):
    for row in declaration[kind]:
        actual = read(row['path'])
        if (h(actual) != row['sha256'] and args.runtime_authority_sha256
                and row['path'] == 'scripts/_proper_finite_latin_20261029.py'):
            # An activated run may change only these three reviewed literal pins.
            # Reconstruct the exact pending bytes and compare their recorded SHA.
            lines = actual.decode().splitlines(keepends=True)
            originals = {'ADOPTION_SHA256': 'ADOPTION_SHA256 = ""\n',
                         'RECOGNITION': 'RECOGNITION = ()\n',
                         'PRIOR_ROUTES': 'PRIOR_ROUTES = {"row_sha256": [], "artifacts": [], "readings": []}\n'}
            found = {}
            for node in ast.parse(actual).body:
                if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in originals:
                    assert node.targets[0].id not in found
                    found[node.targets[0].id] = node
            assert set(found) == set(originals)
            for name, node in sorted(found.items(), key=lambda item: item[1].lineno, reverse=True):
                lines[node.lineno - 1:node.end_lineno] = [originals[name]]
            assert h(''.join(lines).encode()) == row['sha256'], 'guard logic changed beyond reviewed activation pins'
        elif (h(actual) != row['sha256'] and args.installed_sources and kind == 'inputs'
              and row['path'] == 'src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml'):
            # Preparation used this file's defaults. Installation intentionally
            # changes its rows; verify defaults now and every adopted row below.
            baseline = subprocess.check_output(['git', 'show', authority['baseline_commit'] + ':' + row['path']], cwd=ROOT)
            assert tomllib.loads(actual.decode())['defaults'] == tomllib.loads(baseline.decode())['defaults']
            installation_input_deltas.append({'path': row['path'], 'prepared_sha256': row['sha256'],
                                              'installed_sha256': h(actual)})
        else:
            assert h(actual) == row['sha256'], (kind, row['path'])

loader = SourceFileLoader('packet_mechanical_library', str(ROOT / 'tools/source-library'))
spec = spec_from_loader(loader.name, loader)
tool = module_from_spec(spec)
sys.modules[spec.name] = tool
loader.exec_module(tool)

metadata, overlays, plans, rows = {}, {}, [], []
for item in declaration['inputs']:
    if item['path'].startswith('src/sources/') and item['path'].endswith('.toml'):
        metadata[item['path']] = tomllib.loads(read(item['path']).decode())
for item in declaration['plans']:
    plan = json.loads(read(item['path']))
    plans.append(plan)
    rows.extend((item['path'], row) for row in plan.get('rows', []))
    for file in plan.get('source_files', []):
        raw = read(file['candidate_path'])
        assert h(raw) == file['sha256']
        path = file['repository_path']
        assert path not in overlays or overlays[path] == raw
        overlays[path] = raw
        if path.endswith('.toml'): metadata[path] = tomllib.loads(raw.decode())
records, locations = {}, {}
for path, row in metadata.items():
    if row.get('record_type') not in TYPES or not isinstance(row.get('id'), str): continue
    assert row['id'] not in records or locations[row['id']] == path, row['id']
    records[row['id']] = row
    locations[row['id']] = path
def future(path): return overlays[path] if path in overlays else read(path)
def closure(seeds):
    seen, todo = set(), list(seeds)
    while todo:
        rid = todo.pop()
        if rid in seen: continue
        assert rid in records, rid
        seen.add(rid)
        row = records[rid]
        record = tool.Record(Path(locations[rid]), row['record_type'], rid, row)
        edges = set(tool._dependency_ids(record)) | set(row.get('projected_from') or [])
        if row['record_type'] == 'work': edges |= set(row.get('relations') or [])
        todo.extend(edges - seen)
    return seen

defaults_path = 'src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml'
defaults = tomllib.loads(read(defaults_path).decode())['defaults']
scope_by_key = {tuple(scope['key']): scope for scope in authority['scopes']}
assert len(scope_by_key) == len(authority['scopes']) == 16
expected_keys, expected_rows, all_controllers, outside = set(), {}, set(), []
receipt_map = {row['path']: (row['sha256'], json.loads(read(row['path']))) for row in declaration['receipts']}
case_by_identity = {tuple(case['identity']): case for case in authority['case_evidence']}
pointer_count = 0
for plan_path, row in rows:
    provenance = {**defaults, **row['latin_provenance']}
    body = row['new_proper']['text']
    assert h(body.encode()) == provenance['text_sha256']
    if provenance['publication_basis'] != 'qualified-nonoriginal-adaptation':
        outside.append({'identity': row['identity'], 'body_sha256': h(body.encode()),
                        'publication_basis': provenance['publication_basis'], 'plan': plan_path})
        continue
    key = tuple(provenance[k] for k in KEYS)
    assert key not in expected_keys
    expected_keys.add(key)
    source = records[provenance['source_id']]
    assert source.get('record_type') == 'passage' and source.get('artifact_id')
    artifact = records[source['artifact_id']]
    payload = future(artifact['path'])
    assert h(payload) == artifact['sha256'] and len(payload) == artifact['byte_size']
    lines, held = payload.decode().split('\n'), []
    for first, last in source['physical_line_ranges']:
        assert type(first) is type(last) is int and 1 <= first <= last <= len(lines)
        held.extend(lines[first - 1:last])
    selected = '\n'.join(held)
    assert selected + '\n' == body
    seeds = {source['id'], artifact['id'], provenance['verification_source_id'],
             *provenance['publication_source_ids']}
    for field in ('conclusion_controllers', 'source_range_controls', 'source_record',
                  'projection_passage_record', 'pd_source_artifact_id', 'pd_source_passage_id',
                  'source_base_controller_id', 'source_base_artifact_id'):
        seeds |= identifiers(row.get(field))
    controllers = closure(seeds)
    all_controllers |= controllers
    inherited = dict(provenance, publication_status='unresolved', publication_basis='unresolved',
                     surfaces=[], note='Provenance inherited from roman-1962; target-recension attestation for roman-pre-1955 is not established.')
    expected = {'key': list(key), 'row_sha256': dh(provenance), 'inherited_row_sha256': dh(inherited),
                'body_sha256': h(body.encode()), 'artifact_payload_sha256': h(payload),
                'source_id': source['id'], 'artifact_id': artifact['id'],
                'verification_source_id': provenance['verification_source_id'],
                'publication_source_ids': provenance['publication_source_ids'],
                'projected_from': artifact['projected_from'],
                'physical_line_ranges': source['physical_line_ranges'],
                'record_sha256': {rid: dh(records[rid]) for rid in sorted(controllers)},
                'public_notice': row.get('public_notice', NOTICE)}
    assert expected == scope_by_key[key], key
    assert set(provenance['surfaces']) == {'web', 'download', 'print', 'cli', 'corpus-data', 'public-git'}
    expected_rows[key] = provenance
    case = case_by_identity[tuple(row['identity'])]
    assert case['plan'] == plan_path and case['body_sha256'] == h(body.encode())
    english = row.get('english')
    assert case['english_sha256'] == (h(english.encode()) if isinstance(english, str) else row.get('english_sha256'))
    if row.get('review_path'):
        assert case['row_review']['path'] == row['review_path']
        assert case['row_review']['sha256'] == row['review_sha256'] == h(read(row['review_path']))
    for link in case['body_bound_receipt_links']:
        digest, receipt = receipt_map[link['path']]
        assert link['sha256'] == digest
        for path in link['body_hash_pointers']:
            assert pointer(receipt, path) == case['body_sha256']
            pointer_count += 1
assert expected_keys == set(scope_by_key)
assert outside == authority['outside_qualified_scope'] and len(outside) == 1
assert len(rows) == 17 and len(case_by_identity) == 16

checks = {x['id']: x for x in declaration['controller_payload_checks']}
artifact_ids = {rid for rid in all_controllers if records[rid]['record_type'] == 'artifact'}
assert set(checks) == artifact_ids
for rid, check in checks.items():
    record = records[rid]
    assert check['record_sha256'] == dh(record)
    assert check['storage'] == record['storage']
    assert check['registered_payload_sha256'] == record['sha256']
    if record['storage'] == 'tracked':
        payload = future(record['path'])
        assert h(payload) == record['sha256'] == check['actual_payload_sha256']
        assert len(payload) == record['byte_size'] == check['actual_byte_size']
        assert check['state'] == 'actual-postimage-bytes-verified'
    else:
        assert check['state'] == 'registered-remote-metadata-pinned-no-byte-verification-claim'

if args.installed_sources:
    table = tomllib.loads(read(defaults_path).decode())
    installed_rows = [{**table['defaults'], **row} for row in table['entries']]
    for key, expected in expected_rows.items():
        found = [row for row in installed_rows if tuple(row[k] for k in KEYS) == key]
        assert found == [expected], 'installed owner row differs: ' + repr(key)
    for rid in all_controllers:
        assert tomllib.loads(read(locations[rid]).decode()) == records[rid], 'installed controller differs: ' + rid
    for rid in artifact_ids:
        record = records[rid]
        if record['storage'] == 'tracked':
            payload = read(record['path'])
            assert h(payload) == record['sha256'] and len(payload) == record['byte_size']

# Exercise exactly these scopes through the accepted runtime guard in an isolated
# synthetic adopted wrapper. This does not alter the pending authority or runtime.
sys.path.insert(0, str(ROOT / 'scripts'))
import _proper_finite_latin_20261029 as F
import _proper_qualified_latin as Q
if args.runtime_authority_sha256:
    actual_authority_raw = read(F.ADOPTION_PATH)
    actual_authority = json.loads(actual_authority_raw)
    assert h(actual_authority_raw) == args.runtime_authority_sha256 == F.ADOPTION_SHA256
    assert actual_authority['state'] == 'adopted'
    for field in ('scopes', 'case_evidence', 'prior_routes', 'outside_qualified_scope',
                  'excluded_hold_records', 'excluded_pending_targets', 'plan_pins'):
        assert actual_authority[field] == authority[field], field
    assert F.RECOGNITION == F.recognition_from_scopes(authority['scopes'])
    assert F.PRIOR_ROUTES == authority['prior_routes']
runtime_checks = 0
with tempfile.TemporaryDirectory(dir=WORK) as temporary:
    selected_root = Path(temporary)
    synthetic = dict(authority, state='adopted')
    raw = (json.dumps(synthetic, indent=2, ensure_ascii=False) + '\n').encode()
    path = selected_root / F.ADOPTION_PATH
    path.parent.mkdir(parents=True)
    path.write_bytes(raw)
    for scope in authority['scopes']:
        record = records[scope['artifact_id']]
        target = selected_root / record['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(future(record['path']))
    with patch.multiple(F, TRUSTED_ROOT=selected_root, ADOPTION_SHA256=h(raw),
                        RECOGNITION=F.recognition_from_scopes(authority['scopes']),
                        PRIOR_ROUTES=authority['prior_routes']):
        F._scopes.cache_clear()
        assert len(F._scopes()) == 16
        for key, row in expected_rows.items():
            scope = scope_by_key[key]
            source, artifact = records[scope['source_id']], records[scope['artifact_id']]
            assert Q.row_problems(row) == []
            assert Q.source_problems(row, records, effective_calendar='roman-1962') == []
            assert Q.authority_problems(selected_root, row=row) == []
            assert Q.artifact_problems(selected_root, artifact, sources=records) == []
            payload = future(artifact['path']).decode().split('\n')
            selected = '\n'.join(line for first, last in source['physical_line_ranges']
                                 for line in payload[first - 1:last])
            assert Q.reading_problems(selected_root, source, artifact, sources=records, text=selected) == []
            assert Q.row_problems(dict(row, mass='unknown-copied-owner'))
            assert Q.reading_problems(selected_root, source, artifact, sources=records, text=selected + ' added')
            runtime_checks += 7
        path.unlink()
        assert Q.authority_problems(selected_root, row=next(iter(expected_rows.values())))
    F._scopes.cache_clear()

result = {'authority_sha256': h((PACKET / 'candidate-authority-v1.json').read_bytes()),
          'declaration_sha256': h((PACKET / 'declaration-v1.json').read_bytes()),
          'scopes_rederived_exactly': len(expected_keys), 'outside_direct_public_domain': len(outside),
          'registered_controller_records': len(all_controllers),
          'artifact_payload_checks': dict(Counter(records[rid]['storage'] for rid in artifact_ids)),
          'body_pointer_links_checked': pointer_count, 'isolated_runtime_checks': runtime_checks,
          'root_or_source_activation': False, 'rights_or_English_merits_review_repeated': False,
          'actual_runtime_authority_verified': args.runtime_authority_sha256,
          'installed_sources_verified': args.installed_sources,
          'planned_installation_input_deltas': installation_input_deltas}
(WORK / 'mechanical-result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
