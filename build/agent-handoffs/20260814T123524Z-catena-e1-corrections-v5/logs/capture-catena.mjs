/* Lane-local evidence capture for the Catena E1 V4.1 correction.
 *
 * Drives the repository's own Chromium over the DevTools Protocol — the same
 * engine and the same flags `tools/tests/corpus_browser_gate.mjs` uses — against
 * a built `build/public-alpha/site` served over loopback HTTP. It adds only the
 * Catena route states the shared gate's route list does not carry (the
 * fail-closed and refusal addresses), and it lives outside the repository
 * because the shared gate is not this lane's to change.
 *
 * Usage: node capture-catena.mjs <site-root> <out-dir> <prefix>
 */
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { join, extname, normalize } from 'node:path';

const [SITE, OUT, PREFIX] = process.argv.slice(2);
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.png': 'image/png', '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2', '.txt': 'text/plain', '.xml': 'application/xml' };

const CATENA = '/catena/index.html';
const GEN1 = '#book=Gen&chapter=1&bible=douay-rheims';

/* Every address below is real repository data, verified present under
 * src/web/data/structure/catena/. Nothing is fabricated for the picture. */
const STATES = [
  ['ordinary-populated',            CATENA + GEN1],
  ['voice-original',                CATENA + GEN1 + '&voice=original'],
  ['voice-translation-en',          CATENA + GEN1 + '&voice=translation:en'],
  ['voice-translation-la',          CATENA + GEN1 + '&voice=translation:la'],
  ['unsupported-voice-grc',         CATENA + GEN1 + '&voice=translation:grc'],
  ['supported-voice-empty-chapter', CATENA + '#book=Gen&chapter=10&bible=douay-rheims&voice=translation:en'],
  ['malformed-address',             CATENA + '#book=Foo&chapter=1&bible=douay-rheims'],
  ['numbering-refusal',             CATENA + '#book=Ps&chapter=13&bible=king-james-version'],
  ['acquisition-leads',             CATENA + '#book=Ex&chapter=3&bible=douay-rheims'],
];

/* States whose SHARED umbrella copy the V4.1 correction changes. These are the
 * ones that need comparable before/after images. */
const CHANGED = new Set(['unsupported-voice-grc', 'malformed-address']);

const VIEWPORTS = [[1440, 900], [393, 852], [320, 852]];

function serve(root) {
  return new Promise((ok) => {
    const server = createServer(async (req, res) => {
      const path = normalize(decodeURIComponent(req.url.split('#')[0].split('?')[0]));
      try {
        const body = await readFile(join(root, path));
        res.writeHead(200, { 'content-type': TYPES[extname(path)] || 'application/octet-stream' });
        res.end(body);
      } catch { res.writeHead(404); res.end('not found'); }
    });
    server.listen(0, '127.0.0.1', () => ok(server));
  });
}

let nextId = 1;
function rpc(ws, pending, method, params, sessionId) {
  const id = nextId++;
  return new Promise((ok, no) => {
    pending.set(id, { ok, no });
    ws.send(JSON.stringify({ id, method, params: params || {}, sessionId }));
  });
}

async function main() {
  await mkdir(OUT, { recursive: true });
  const server = await serve(SITE);
  const base = `http://127.0.0.1:${server.address().port}`;

  const port = 9400 + (process.pid % 500);
  const chrome = spawn(CHROME, ['--headless=new', '--no-sandbox', '--disable-gpu',
    '--disable-dev-shm-usage', '--hide-scrollbars', '--force-device-scale-factor=1',
    `--remote-debugging-port=${port}`, 'about:blank'], { stdio: ['ignore', 'pipe', 'pipe'] });

  let version = null;
  for (let i = 0; i < 100 && !version; i++) {
    await new Promise((r) => setTimeout(r, 100));
    try { version = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); } catch { }
  }
  if (!version) throw new Error('Chromium did not expose a DevTools endpoint');
  console.log('browser: ' + version['Browser']);

  const ws = new WebSocket(version.webSocketDebuggerUrl);
  const pending = new Map();
  const waiters = [];
  ws.addEventListener('message', (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && pending.has(msg.id)) {
      const { ok, no } = pending.get(msg.id); pending.delete(msg.id);
      msg.error ? no(new Error(JSON.stringify(msg.error))) : ok(msg.result);
    } else { for (const w of waiters.slice()) if (w.test(msg)) { waiters.splice(waiters.indexOf(w), 1); w.ok(msg); } }
  });
  await new Promise((ok, no) => { ws.addEventListener('open', ok); ws.addEventListener('error', no); });

  const { targetId } = await rpc(ws, pending, 'Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await rpc(ws, pending, 'Target.attachToTarget', { targetId, flatten: true });
  const call = (m, p) => rpc(ws, pending, m, p, sessionId);
  await call('Page.enable'); await call('Runtime.enable');

  const index = [];
  for (const [state, route] of STATES) {
    for (const [width, height] of VIEWPORTS) {
      const modes = [['default', 'screen', []]];
      // The narrow handset carries the conditional variants, matching the
      // shared gate's own state matrix rather than inventing a new one.
      if (width === 393) modes.push(['forced-colors', 'screen', [{ name: 'forced-colors', value: 'active' }]]);
      if (width === 1440) modes.push(['print', 'print', []]);
      for (const [variant, media, features] of modes) {
        if (PREFIX === 'before--' && !(CHANGED.has(state) && variant === 'default')) continue;
        await call('Emulation.setDeviceMetricsOverride',
          { width, height, deviceScaleFactor: 1, mobile: false });
        await call('Emulation.setEmulatedMedia', { media, features });
        await call('Page.navigate', { url: base + route });
        await new Promise((r) => setTimeout(r, 1400));
        // Settle on the page's own signal: the reading region stops being busy.
        for (let i = 0; i < 40; i++) {
          const { result } = await call('Runtime.evaluate', {
            expression: `document.querySelector('#reading')?.getAttribute('aria-busy')`,
            returnByValue: true });
          if (result.value !== 'true') break;
          await new Promise((r) => setTimeout(r, 100));
        }
        const shot = await call('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
        const suffix = variant === 'default' ? '' : `--${variant}`;
        const file = `${PREFIX}catena--${state}--${width}x${height}${suffix}.png`;
        await writeFile(join(OUT, file), Buffer.from(shot.data, 'base64'));
        const { result: href } = await call('Runtime.evaluate',
          { expression: 'location.pathname + location.hash', returnByValue: true });
        index.push({ file, route, viewport: `${width}x${height}`, variant,
          media, urlAfterLoad: href.value, bytes: Buffer.from(shot.data, 'base64').length });
        console.log(file);
      }
    }
  }
  await writeFile(join(OUT, `${PREFIX || 'after--'}capture-index.json`), JSON.stringify(index, null, 2) + '\n');
  chrome.kill(); server.close();
  console.log(`captured ${index.length} image(s)`);
  process.exit(0);
}
main().catch((e) => { console.error('CAPTURE FAILED: ' + e.stack); process.exit(1); });
