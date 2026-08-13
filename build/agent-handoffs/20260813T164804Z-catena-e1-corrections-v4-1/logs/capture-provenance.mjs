/* Lane-local provenance capture: opens a real fragment so the full recorded
 * apparatus — author, work, date, extent, edition and rights basis — renders.
 * Severian of Gabala is the corpus's licensed source, so it is the state that
 * exercises the rights line. Real data; nothing is fabricated for the picture. */
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { join, extname, normalize } from 'node:path';

const [SITE, OUT] = process.argv.slice(2);
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.png': 'image/png', '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2', '.txt': 'text/plain', '.xml': 'application/xml' };

const serve = (root) => new Promise((ok) => {
  const s = createServer(async (req, res) => {
    const p = normalize(decodeURIComponent(req.url.split('#')[0].split('?')[0]));
    try {
      const b = await readFile(join(root, p));
      res.writeHead(200, { 'content-type': TYPES[extname(p)] || 'application/octet-stream' });
      res.end(b);
    } catch { res.writeHead(404); res.end('nope'); }
  });
  s.listen(0, '127.0.0.1', () => ok(s));
});

let nextId = 1;
async function main() {
  await mkdir(OUT, { recursive: true });
  const server = await serve(SITE);
  const base = `http://127.0.0.1:${server.address().port}`;
  const port = 9700 + (process.pid % 200);
  const chrome = spawn(CHROME, ['--headless=new', '--no-sandbox', '--disable-gpu',
    '--disable-dev-shm-usage', '--hide-scrollbars', '--force-device-scale-factor=1',
    `--remote-debugging-port=${port}`, 'about:blank'], { stdio: ['ignore', 'pipe', 'pipe'] });

  let version = null;
  for (let i = 0; i < 100 && !version; i++) {
    await new Promise((r) => setTimeout(r, 100));
    try { version = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); } catch { }
  }
  const ws = new WebSocket(version.webSocketDebuggerUrl);
  const pending = new Map();
  ws.addEventListener('message', (e) => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) {
      const { ok, no } = pending.get(m.id); pending.delete(m.id);
      m.error ? no(new Error(JSON.stringify(m.error))) : ok(m.result);
    }
  });
  await new Promise((ok, no) => { ws.addEventListener('open', ok); ws.addEventListener('error', no); });
  const { targetId } = await rpcT('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await rpcT('Target.attachToTarget', { targetId, flatten: true });
  function rpcT(method, params, sid) {
    const id = nextId++;
    return new Promise((ok, no) => { pending.set(id, { ok, no });
      ws.send(JSON.stringify({ id, method, params: params || {}, sessionId: sid })); });
  }
  const call = (m, p) => rpcT(m, p, sessionId);
  await call('Page.enable'); await call('Runtime.enable');

  const index = [];
  for (const [w, h] of [[1440, 900], [393, 852]]) {
    await call('Emulation.setDeviceMetricsOverride',
      { width: w, height: h, deviceScaleFactor: 1, mobile: false });
    await call('Page.navigate',
      { url: base + '/catena/index.html#book=Gen&chapter=1&bible=douay-rheims' });
    await new Promise((r) => setTimeout(r, 2000));
    // Open the licensed Severian fragment by its recorded author name, and
    // bring it into view. No data is altered; only disclosure state changes.
    const { result } = await call('Runtime.evaluate', {
      expression: `(() => {
        const authors = [...document.querySelectorAll('#reading details.author-body')]
          .filter((d) => /Severian/.test(d.querySelector('summary')?.textContent || ''));
        authors.forEach((d) => { d.open = true; });
        if (!authors.length) return 'no Severian author disclosure found';
        // Only THIS author's first fragment, so the apparatus stays on screen.
        const frags = [...authors[0].querySelectorAll('details.fragment-body')];
        if (frags.length) frags[0].open = true;
        const target = authors[0];
        const r = target.getBoundingClientRect();
        return JSON.stringify({ text: target.textContent.replace(/\\s+/g, ' ').slice(0, 200),
          x: Math.max(0, r.x + window.scrollX - 12), y: Math.max(0, r.y + window.scrollY - 12),
          width: Math.min(r.width + 24, 2000), height: Math.min(r.height + 24, 2400) });
      })()`, returnByValue: true });
    await new Promise((r) => setTimeout(r, 900));
    let clip = null;
    try { const d = JSON.parse(result.value); clip = { x: d.x, y: d.y, width: d.width, height: d.height, scale: 1 }; } catch { }
    const shot = await call('Page.captureScreenshot', clip ? { format: 'png', clip, captureBeyondViewport: true } : { format: 'png' });
    const file = `after--catena--provenance-open-fragment--${w}x${h}--focused-region.png`;
    await writeFile(join(OUT, file), Buffer.from(shot.data, 'base64'));
    index.push({ file, viewport: `${w}x${h}`, opened: result.value });
    console.log(file + '  |  ' + result.value);
  }
  await writeFile(join(OUT, 'after--provenance-index.json'), JSON.stringify(index, null, 2) + '\n');
  chrome.kill(); server.close(); process.exit(0);
}
main().catch((e) => { console.error('CAPTURE FAILED: ' + e.stack); process.exit(1); });
