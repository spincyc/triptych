"""Replay only immutable baseline proof; current unrelated source writes are irrelevant."""
import argparse
import ast
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents
            if (parent / 'tmt.json').is_file() and (parent / 'tools/source-library').is_file())
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out', required=True, help='new reviewer-owned directory below repository .scratch')
args = parser.parse_args()
WORK = Path(args.out)
if not WORK.is_absolute(): WORK = ROOT / WORK
WORK = WORK.resolve()
assert WORK.is_relative_to(ROOT / '.scratch') and not WORK.exists(), 'new repository scratch output required'
WORK.mkdir(parents=True)
PACKET = HERE.parent
SUBJECT = PACKET / 'prepare_activation.py'
raw = SUBJECT.read_bytes()
assert sha256(raw).hexdigest() == '53eb75950f8bf58d48cbbc09e4f555638c65f7189881333b32dcf915d051e6c1'
namespace = {'__name__': 'immutable_prior_replay', '__file__': str(SUBJECT)}
exec(compile(raw, str(SUBJECT), 'exec'), namespace)
# Preserve exact archived compiler bytes while adapting its historical entrypoint.
namespace['ROOT'] = ROOT
namespace['OWN'] = WORK
tree = ast.parse(raw)
main = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'main')
block = next(node for node in main.body if isinstance(node, ast.Try))
statements = []
for node in block.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'authority' for t in node.targets):
        continue
    if isinstance(node, ast.Expr) and 'candidate-authority.json' in ast.unparse(node):
        continue
    statements.append(node)
authority = json.loads((PACKET / 'candidate-authority-v1.json').read_bytes())
out = WORK / 'immutable-baseline-replay'
out.mkdir()
namespace.update(out=out, scopes=authority['scopes'],
                 body_hashes={s['body_sha256'] for s in authority['scopes']},
                 payload_hashes={s['artifact_payload_sha256'] for s in authority['scopes']},
                 artifact_ids={s['artifact_id'] for s in authority['scopes']},
                 source_ids={s['source_id'] for s in authority['scopes']})
namespace['marker'] = lambda value: isinstance(value, str) and (
    namespace['METHOD'] in value or namespace['AUTHORITY'] in value)
namespace['artifact_matches'] = lambda artifact: {
    'identity': artifact.get('id') in namespace['artifact_ids'],
    'payload': artifact.get('sha256') in namespace['payload_hashes'],
    'marker': any(namespace['marker'](artifact.get(field)) for field in ('rights_basis', 'notes'))}
namespace['tool'] = namespace['load_tool']('source-library')
namespace['reader'] = namespace['load_tool']('source-reader')
snapshot = namespace['GitSnapshot'](authority['baseline_commit'])
namespace['snap'] = snapshot
try:
    exec(compile(ast.Module(body=statements, type_ignores=[]), str(SUBJECT), 'exec'), namespace)
finally:
    snapshot.close()
expected = (PACKET / 'prior-route-proof-v1.json').read_bytes()
actual = (out / 'prior-route-proof.json').read_bytes()
assert actual == expected, 'immutable baseline proof did not reproduce byte-exactly'
result = {'compiler_sha256': sha256(raw).hexdigest(),
          'expected_proof_sha256': sha256(expected).hexdigest(),
          'replayed_proof_sha256': sha256(actual).hexdigest(),
          'byte_exact': True, 'baseline_commit': authority['baseline_commit'],
          'current_metadata_consumed': False,
          'scope_or_source_mutations': False}
(WORK / 'immutable-prior-replay-result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
