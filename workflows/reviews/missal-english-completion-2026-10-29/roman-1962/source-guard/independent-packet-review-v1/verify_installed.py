"""Bounded actual-source followthrough after root-authorized installation."""
import argparse
import ast
from hashlib import sha256
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
from pathlib import Path
import subprocess
import sys
import tomllib
import types
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents
            if (parent / 'tmt.json').is_file() and (parent / 'tools/source-library').is_file())
VERIFY = HERE / 'verify_packet.py'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out', required=True, help='new reviewer-owned directory below repository .scratch')
OUT = parser.parse_args().out
AUTHORITY_SHA = '920299972ab84575183de8c84adcd3f7418bdc46304fbe1d6a4435fad1103ee3'
GUARD_SHA = '34c7ea2520f0917108495ea333323c33e4eb3b6993aba2e10c91fc49385dfb40'

# Execute the retained verifier's exact data reconstruction and pin checks.
# Its isolated positive fixture loop is unnecessary here: actual sources follow.
tree = ast.parse(VERIFY.read_bytes())
prefix = []
for node in tree.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'runtime_checks' for t in node.targets):
        break
    prefix.append(node)
argv = sys.argv
try:
    sys.argv = [str(VERIFY), '--out', OUT, '--runtime-authority-sha256', AUTHORITY_SHA, '--installed-sources']
    state = {'__name__': 'installed_finite_review', '__file__': str(VERIFY)}
    exec(compile(ast.Module(body=prefix, type_ignores=[]), str(VERIFY), 'exec'), state)
finally:
    sys.argv = argv
work = state['WORK']
F, Q = state['F'], state['Q']
assert sha256((ROOT / 'scripts/_proper_finite_latin_20261029.py').read_bytes()).hexdigest() == GUARD_SHA
assert sha256((ROOT / F.ADOPTION_PATH).read_bytes()).hexdigest() == AUTHORITY_SHA
for field in ('root_rights_judgment', 'independent_packet_mechanics_review', 'preserved_exact_pending_proposal'):
    binding = json.loads((ROOT / F.ADOPTION_PATH).read_bytes())[field]
    assert sha256((ROOT / binding['path']).read_bytes()).hexdigest() == binding['sha256']

actual = {}
for rid in state['all_controllers']:
    path = ROOT / state['locations'][rid]
    assert path.is_file() and not path.is_symlink(), str(path)
    record = tomllib.loads(path.read_text())
    assert record == state['records'][rid], 'installed controller differs: ' + rid
    actual[rid] = record
for rid in state['artifact_ids']:
    record = actual[rid]
    if record['storage'] == 'tracked':
        payload = (ROOT / record['path']).read_bytes()
        assert sha256(payload).hexdigest() == record['sha256'] and len(payload) == record['byte_size']

import _proper_latin as L
ledger = tomllib.loads((ROOT / 'src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml').read_text())
rows = {tuple({**ledger['defaults'], **r}[k] for k in state['KEYS']): {**ledger['defaults'], **r}
        for r in ledger['entries']}
document = L._calendars.load_document(ROOT / 'src/sources/calendars', 'roman-1962')
bodies = {tuple(key.as_dict()[k] for k in state['KEYS']): text
          for key, text, status in L.body_owners(document) if status == 'present'}
loader = SourceFileLoader('installed_finite_reader', str(ROOT / 'tools/source-reader'))
spec = spec_from_loader(loader.name, loader)
reader = module_from_spec(spec)
sys.modules[spec.name] = reader
loader.exec_module(reader)
library = types.SimpleNamespace(root=ROOT, records={rid: types.SimpleNamespace(data=record)
                                                   for rid, record in actual.items()})
F._scopes.cache_clear()
assert len(F._scopes()) == 16
scope_cases = 0
negative_cases = 0
inherited_cases = 0
for key, expected in state['expected_rows'].items():
    row = rows[key]
    assert row == expected
    scope = state['scope_by_key'][key]
    text = bodies[key]
    assert sha256(text.encode()).hexdigest() == scope['body_sha256']
    assert Q.row_problems(row) == []
    assert L._row_problems('actual finite review', row) == []
    assert Q.source_problems(row, actual, effective_calendar='roman-1962') == []
    assert Q.authority_problems(ROOT, row=row) == []
    assert L._source_record_problems('actual finite review', row, actual,
        authority_root=ROOT, effective_calendar='roman-1962') == []
    source, artifact = actual[scope['source_id']], actual[scope['artifact_id']]
    assert Q.artifact_problems(ROOT, artifact, sources=actual) == []
    reading = reader.reading_of(library, source)
    assert reading['readable'] and sha256((reading['text'] + '\n').encode()).hexdigest() == scope['body_sha256']
    decision = L.decision_for(L.LatinKey(*key), text, {L.LatinKey(*key): row})
    assert decision.permits(L.SURFACES)
    assert not L.decision_for(L.LatinKey(*key), text + ' added', {L.LatinKey(*key): row}).permits(L.SURFACES)
    assert Q.row_problems(dict(row, mass='unknown-copied-owner'))
    assert Q.row_problems(dict(row, surfaces=['web']))
    assert Q.reading_problems(ROOT, source, artifact, sources=actual, text=reading['text'] + ' added')
    inherited = dict(row, publication_status='unresolved', publication_basis='unresolved', surfaces=[],
                     note='Provenance inherited from roman-1962; target-recension attestation for roman-pre-1955 is not established.')
    assert Q.inherited_row_exact(inherited)
    assert Q.row_problems(inherited)
    assert Q.source_problems(inherited, actual, effective_calendar='roman-pre-1955') == []
    assert not L.decision_for(L.LatinKey(*key), text, {L.LatinKey(*key): inherited}).permits(L.SURFACES)
    assert Q.source_problems(row, actual, effective_calendar='roman-pre-1955')
    assert Q.source_problems(row, actual, effective_calendar='postconciliar')
    inherited_cases += 1
    copied = dict(artifact, id='artifact.unknown.copy', rights_basis='Original editorial carrier')
    copied.pop('notes', None)
    passage = dict(source, id='passage.unknown.copy', artifact_id=copied['id'])
    forged = types.SimpleNamespace(root=ROOT, records={**library.records,
        copied['id']: types.SimpleNamespace(data=copied)})
    refused = reader.reading_of(forged, passage)
    assert not refused['readable'] and 'text' not in refused
    wrapper = 'Wrapper.\n' + text + 'Suffix.\n'
    copied['sha256'] = sha256(wrapper.encode()).hexdigest()
    passage.update(artifact_sha256=copied['sha256'], physical_line_ranges=[[2, 1 + len(text.removesuffix('\n').split('\n'))]])
    with patch.object(reader, '_payload_lines', return_value=wrapper.split('\n')):
        refused = reader.reading_of(forged, passage)
    assert not refused['readable'] and 'text' not in refused
    scope_cases += 1
    negative_cases += 6

# Preserve the actual older two routes, using their existing records and bodies.
wanted = set(Q.CONTROLLER_SHA256) | set(Q.PARENT_FIELDS) | {s['verification_source_id'] for s in Q.SCOPES}
old_sources = {}
for author, name in {(rid.split('.')[1], rid.split('.')[2]) for rid in wanted}:
    for path in (ROOT / 'src/sources/works' / author / name).rglob('*.toml'):
        record = tomllib.loads(path.read_text())
        if record.get('id') in wanted: old_sources[record['id']] = record
assert set(old_sources) == wanted
legacy_cases = 0
for scope in Q.SCOPES:
    key = tuple(scope['key'])
    row = rows[key]
    assert Q.row_problems(row) == Q.source_problems(row, old_sources) == []
    assert Q.authority_problems(ROOT, row=row) == []
    inherited = dict(row, publication_status='unresolved', publication_basis='unresolved', surfaces=[],
                     note='Provenance inherited from roman-1962; target-recension attestation for roman-pre-1955 is not established.')
    assert Q.inherited_row_exact(inherited)
    assert Q.source_problems(inherited, old_sources, effective_calendar='roman-pre-1955') == []
    artifact, source = old_sources[scope['artifact_id']], old_sources[scope['source_id']]
    assert Q.artifact_problems(ROOT, artifact, sources=old_sources) == []
    assert Q.reading_problems(ROOT, source, artifact, sources=old_sources, text=bodies[key].removesuffix('\n')) == []
    colliding = dict(state['authority']['scopes'][0], body_sha256=row['text_sha256'],
                     artifact_payload_sha256=artifact['sha256'])
    with patch.object(F, '_scopes', return_value=(colliding,)):
        assert Q.row_problems(row) == Q.source_problems(row, old_sources) == []
        assert Q.authority_problems(ROOT, row=row) == []
        assert Q.inherited_row_exact(inherited)
        assert Q.artifact_problems(ROOT, artifact, sources=old_sources) == []
        assert Q.reading_problems(ROOT, source, artifact, sources=old_sources,
                                  text=bodies[key].removesuffix('\n')) == []
    legacy_cases += 1
F._scopes.cache_clear()
assert sha256((ROOT / 'scripts/_proper_finite_latin_20261029.py').read_bytes()).hexdigest() == GUARD_SHA
assert sha256((ROOT / F.ADOPTION_PATH).read_bytes()).hexdigest() == AUTHORITY_SHA
result = {'actual_guard_sha256': GUARD_SHA, 'actual_authority_sha256': AUTHORITY_SHA,
          'installed_exact_scopes': 16, 'installed_controller_records': len(actual),
          'new_scope_cases_checked': scope_cases, 'negative_cases_checked': negative_cases,
          'inherited_resets_checked': inherited_cases,
          'legacy_routes_checked': legacy_cases, 'forced_legacy_collision_routes_checked': legacy_cases,
          'root_bindings_checked': 3, 'canonical_source_or_code_mutations': False}
(work / 'installed-runtime-result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
