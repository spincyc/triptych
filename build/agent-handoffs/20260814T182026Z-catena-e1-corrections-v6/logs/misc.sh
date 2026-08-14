#!/bin/sh
# The short read-only checks, each stated against the commit it ran at.
cd $REPO
SHA=$(git rev-parse HEAD)
PARENT=19982ab433dd25704ed60b1ac6ddb678bc3a98f9

echo "Every command below was run from the repository root at the commit named beside"
echo "it, and its numeric exit is recorded. Nothing is rounded, and nothing is"
echo "attributed to a commit that could not have produced it."
echo
echo "=== A. promise ledger — SHA $SHA, clean tree ==="
echo '$ python3 tools/tpt check-promised-deliverables'
python3 tools/tpt check-promised-deliverables 2>&1; echo "EXIT=$?"
echo
echo "=== B. catena model check — SHA $SHA ==="
echo '$ python3 scripts/_catena.py check'
python3 scripts/_catena.py check 2>&1; echo "EXIT=$?"
echo
echo "=== C. release bindings, READ-ONLY — SHA $SHA ==="
echo '$ python3 tools/tpt release-bindings status'
python3 tools/tpt release-bindings status 2>&1; echo "EXIT=$?"
echo "(no binding was re-signed; refresh-release-bindings and approve-release were not run)"
echo
echo "=== D. budgets — SHA $SHA ==="
echo '$ python3 tools/tests/../../scratch-free measurement using the test module own gz()'
python3 - <<'PY'
import sys
sys.path.insert(0, 'tools/tests')
import test_catena_wave_1 as t
for name, whole_b, strip_b, script in (('catena.css', t.CSS_BUDGET_GZ, t.CSS_RULES_BUDGET_GZ, False),
                                       ('catena.js', t.JS_BUDGET_GZ, t.JS_CODE_BUDGET_GZ, True)):
    text = t.held(t.CATENA / name)
    print(f'{name}: whole {t.gz(text)}/{whole_b}   stripped {t.gz(t.without_comments(text, script=script))}/{strip_b}')
m = t.held(t.CATENA / 'catena-model.js')
print(f'catena-model.js (NO CEILING): whole {t.gz(m)}   stripped {t.gz(t.without_comments(m, script=True))}')
PY
echo "EXIT=$?"
echo
echo "=== E. the relocation, disclosed — SHA $SHA against parent $PARENT ==="
python3 - <<'PY'
import gzip, subprocess
def gz(b):
    return len(gzip.compress(b, 9, mtime=0))
def at(sha, path):
    return subprocess.run(['git', 'show', f'{sha}:{path}'], capture_output=True).stdout
P = 'src/web/browser/catena/'
rows = []
for label, sha in (('parent', '19982ab433dd25704ed60b1ac6ddb678bc3a98f9'), ('head', 'HEAD')):
    js, md = at(sha, P + 'catena.js'), at(sha, P + 'catena-model.js')
    rows.append((label, gz(js), gz(md), gz(js + md), gz(js) + gz(md)))
    print(f'{label:7} catena.js {gz(js):>6}  catena-model.js {gz(md):>6}  '
          f'gzipped together {gz(js + md):>6}  gzipped separately and summed {gz(js) + gz(md):>6}')
p, h = rows[0], rows[1]
print(f'delta   catena.js {h[1]-p[1]:+6}  catena-model.js {h[2]-p[2]:+6}  '
      f'together {h[3]-p[3]:+6}  summed {h[4]-p[4]:+6}')
print('The model carries no ceiling by design, so formal compliance is real and is')
print('NOT the same statement as unchanged practical load. Both measures are given.')
PY
echo "EXIT=$?"
echo
echo "=== F. byte-identity against the parent $PARENT ==="
echo '$ git diff --name-only <parent>..HEAD'
git diff --name-only "$PARENT"..HEAD 2>&1
echo '$ git diff --stat <parent>..HEAD -- src/web/data src/web/browser/catena/catena.css src/web/browser/catena/index.html'
git diff --stat "$PARENT"..HEAD -- src/web/data src/web/browser/catena/catena.css src/web/browser/catena/index.html 2>&1
echo "(no output above = byte-identical)"
echo
echo "=== G. the production sources are text — SHA $SHA ==="
echo '$ file src/web/browser/catena/catena.js src/web/browser/catena/catena-model.js'
file src/web/browser/catena/catena.js src/web/browser/catena/catena-model.js
echo "EXIT=$?"
