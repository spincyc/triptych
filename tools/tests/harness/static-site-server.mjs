/* Shared static server for browser harnesses: one tree, one mount path.
 *
 * The mount path is the deployment-base seam. GitHub Pages serves the same
 * artifact at "/" under a custom domain and at "/<repo>" as a project site,
 * so a harness that can serve one tree at either mount can prove the
 * artifact is deployment-location independent. `serveTree` mimics the two
 * GitHub Pages behaviours the site depends on: a directory URL serves its
 * index.html, and a miss serves the artifact's root 404.html with a 404
 * status while the browser keeps the missed URL as the document base.
 */

import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

export function mime(path) {
  return ({
    '.css': 'text/css; charset=utf-8', '.html': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8',
    '.png': 'image/png', '.svg': 'image/svg+xml', '.pdf': 'application/pdf',
    '.txt': 'text/plain; charset=utf-8'
  })[extname(path)] || 'application/octet-stream';
}

export async function listen(server) {
  await new Promise((accept, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', accept);
  });
  return server.address().port;
}

export async function freePort() {
  const server = createServer();
  const port = await listen(server);
  await new Promise((accept) => server.close(accept));
  return port;
}

export function mountFromEnv() {
  const mount = process.env.TRIPTYCH_TEST_MOUNT || '';
  if (mount && (!mount.startsWith('/') || mount.endsWith('/'))) {
    throw new Error(
      "TRIPTYCH_TEST_MOUNT must be empty or start with '/' and not end with one: " + mount
    );
  }
  return mount;
}

export function serveTree({ root, mountPath = '' }) {
  const treeRoot = resolve(root);
  const server = createServer(async (request, response) => {
    const url = new URL(request.url, 'http://127.0.0.1');
    const pathname = decodeURIComponent(url.pathname);
    const miss = async (status) => {
      try {
        const body = await readFile(resolve(treeRoot, '404.html'));
        response.writeHead(status, { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' });
        response.end(body);
      } catch (_error) {
        response.writeHead(status, { 'content-type': 'text/plain; charset=utf-8' });
        response.end('not found');
      }
    };
    if (pathname === '/favicon.ico') {
      response.writeHead(204, { 'cache-control': 'no-store' });
      response.end();
      return;
    }
    if (mountPath && pathname !== mountPath && !pathname.startsWith(mountPath + '/')) {
      await miss(404);
      return;
    }
    let relative = pathname === mountPath ? '' : pathname.slice(mountPath.length).replace(/^\/+/, '');
    if (!relative || relative.endsWith('/')) relative += 'index.html';
    try {
      const file = resolve(treeRoot, relative);
      if (file !== treeRoot && !file.startsWith(treeRoot + sep)) throw new Error('outside root');
      const body = await readFile(file);
      response.writeHead(200, {
        'content-type': mime(file), 'cache-control': 'no-store',
        'x-robots-tag': 'noindex, nofollow'
      });
      response.end(body);
    } catch (error) {
      if (error && error.code === 'EISDIR') {
        // GitHub Pages answers a bare directory URL with a redirect to the
        // trailing-slash form, whose index.html then resolves.
        response.writeHead(301, { location: pathname + '/' + url.search });
        response.end();
        return;
      }
      await miss(404);
    }
  });
  return server;
}
