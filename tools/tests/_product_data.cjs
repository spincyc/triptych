'use strict';

// Test-only bridge to the Python product locator. Resolving a path never builds
// products; callers must prepare the committed cache or select an explicit fixture.
const { execFileSync } = require('node:child_process');
const path = require('node:path');
const roots = new Map();

function browserDataRoot(root) {
  root = path.resolve(root);
  if (!roots.has(root)) {
    const located = execFileSync(process.env.PYTHON || 'python3', [
      path.join(__dirname, '_product_data.py'), root
    ], { encoding: 'utf8', env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1' } }).trim();
    roots.set(root, path.resolve(located));
  }
  return roots.get(root);
}

function repositoryPath(root, relative) {
  root = path.resolve(root);
  const file = path.resolve(root, relative);
  const legacy = path.join(root, 'src/web/data');
  if (file !== legacy && !file.startsWith(legacy + path.sep)) return file;
  const product = path.relative(legacy, file);
  if (/^[^/]+\/chapters(?:\/|$)/.test(product)) {
    return path.join(root, 'src/sources/bibles', product);
  }
  return path.join(browserDataRoot(root), product);
}

module.exports = { browserDataRoot, repositoryPath };
