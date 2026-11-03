/* Real-browser interaction regressions for the progressively enhanced reader.
   Run: node tools/tests/publication_reader.cjs (Chromium and chromedriver).
   Generated fixtures/logs stay beneath TRIPTYCH_READER_CLIENT_EVIDENCE or .scratch. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const net = require('node:net');
const {spawn} = require('node:child_process');
const {once} = require('node:events');
const repo = path.resolve(__dirname, '../..');
const evidence = path.resolve(repo, process.env.TRIPTYCH_READER_CLIENT_EVIDENCE || '.scratch/publication-reader-client');
fs.mkdirSync(evidence, {recursive: true});
const assets = new Map(['publication-reader.js', 'catalogue-navigation.js'].map(name =>
  [name, fs.readFileSync(path.join(repo, 'src/web/browser/shared', name))]));
const body = '<section id="alpha"><h2>Alpha</h2><p>First complete section.</p><a id="body-link" href="#beta">Read Beta</a></section>' +
  '<section id="beta"><h2>Beta</h2><p>Second complete section.</p></section>' +
  '<section id="gamma"><h2>Gamma</h2><p>Third complete section.</p></section>';
function fixture(url) {
  const next = url.pathname.endsWith('other.html');
  return `<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Reader test</title>
  <style>body{margin:0;font:18px Georgia} .publication-reader__toolbar{position:sticky;top:0;z-index:5;background:white;min-height:60px;border-bottom:1px solid}
  section{height:850px;padding:20px;scroll-margin-top:90px} [data-reader-content]{padding-top:12px} button,select,input{font:inherit}
  [data-reader-toc]{padding:12px} .publication-reader__share-field{display:block} input{width:90%} a:focus{outline:3px solid blue}</style></head><body>
  <main class="publication-reader"><div class="publication-reader__toolbar"><a id="other" href="${next ? 'reader.html' : 'other.html'}">${next ? 'Return' : 'Next'}</a>
  <a id="explicit" href="reader.html#gamma">Gamma</a><a id="delayed" href="reader.html?delay=1">Delayed reader</a>
  <label class="publication-reader__document" hidden>Document<select data-reader-document-select aria-label="Document"><option value="">Choose</option><option value="other.html">Other</option><option value="https://example.invalid/escape.html">Invalid</option></select></label>
  <button type="button" data-reader-copy-link hidden>Copy section link</button><span data-reader-status role="status" aria-live="polite"></span>
  <progress data-reader-progress max="100" value="0" aria-label="Reading progress"></progress></div>
  <details data-reader-toc data-reader-contents open><summary>Contents</summary><nav aria-label="Document sections"><a data-reader-section href="#alpha">Alpha</a> <a data-reader-section href="#beta">Beta</a> <a data-reader-section href="#gamma">Gamma</a></nav></details>
  <div data-reader-content>${url.searchParams.has('opening') ? '<p style="min-height:1600px">Opening prose before the first named section, as in a homily or study introduction.</p>' : ''}${body}</div></main><iframe title="Sealed print fixture" srcdoc="<p>Print content unchanged</p>"></iframe>
  <script>window.originalBody=document.querySelector('[data-reader-content]').innerHTML;
  window.originalFrame=document.querySelector('iframe').outerHTML;
  if(new URL(location.href).searchParams.has('delay')){const c=document.querySelector('[data-reader-content]');c.style.maxHeight='100px';c.style.overflow='hidden';setTimeout(()=>{c.style.maxHeight='';c.style.overflow='';},700);}
  if(new URL(location.href).searchParams.has('blocked')){Object.defineProperty(window,'sessionStorage',{get(){throw new Error('Storage blocked')}});}</script>
  <script src="../../shared/catalogue-navigation.js"></script><script src="../../shared/publication-reader.js"></script></body></html>`;
}
const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://example.invalid');
  res.setHeader('Cache-Control', 'no-store');
  const asset = assets.get(url.pathname.split('/').pop());
  res.setHeader('Content-Type', asset ? 'text/javascript' : 'text/html');
  res.end(asset || fixture(url));
});
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
async function eventually(fn, label) {
  for (let i = 0; i < 100; i++) { if (await fn()) return; await delay(30); }
  throw new Error(label);
}
(async () => {
  server.listen(0, '127.0.0.1'); await once(server, 'listening');
  const origin = `http://127.0.0.1:${server.address().port}/project/web/gpt/`;
  const reservation = net.createServer(); reservation.listen(0, '127.0.0.1'); await once(reservation, 'listening');
  const port = reservation.address().port; await new Promise(resolve => reservation.close(resolve));
  const log = fs.openSync(path.join(evidence, 'chromedriver.log'), 'w');
  const driver = spawn(process.env.TRIPTYCH_CHROMEDRIVER || 'chromedriver', [`--port=${port}`], {stdio: ['ignore', log, log]});
  let session;
  const results = [];
  async function command(method, endpoint, value) {
    const response = await fetch(`http://127.0.0.1:${port}${endpoint}`, {method,
      headers: {'Content-Type': 'application/json'}, body: value === undefined ? undefined : JSON.stringify(value)});
    const result = (await response.json()).value;
    if (result && result.error) throw new Error(result.message);
    return result;
  }
  const execute = script => command('POST', session + '/execute/sync', {script, args: []});
  const click = selector => execute(`document.querySelector(${JSON.stringify(selector)}).click()`);
  const visit = route => command('POST', session + '/url', {url: origin + route});
  const viewport = (width, height=900) => command('POST', session + '/goog/cdp/execute', {cmd: 'Emulation.setDeviceMetricsOverride', params: {width, height, deviceScaleFactor: 1, mobile: false}});
  async function test(name, fn) { await fn(); results.push(name); process.stdout.write('PASS ' + name + '\n'); }
  try {
    await eventually(async () => { try { return !!await command('GET', '/status'); } catch (_) { return false; } }, 'chromedriver startup');
    const created = await command('POST', '/session', {capabilities: {alwaysMatch: {browserName: 'chrome',
      'goog:chromeOptions': {binary: process.env.TRIPTYCH_CHROME || '/usr/bin/chromium', args: ['--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-features=BackForwardCache']}}}});
    session = '/session/' + created.sessionId;
    await viewport(1440); await visit('reader.html?opening=1');
    await test('section state and source preservation', async () => {
      await eventually(() => execute(`return !!window.TriptychPublicationReader`), 'reader installed');
      assert.equal(await execute(`return document.querySelector('[data-reader-copy-link]').hidden`), false);
      assert.equal(await execute(`return document.querySelector('.publication-reader__document').hidden`), false);
      assert.equal(await execute(`return document.querySelector('[data-reader-content]').innerHTML===originalBody && document.querySelector('iframe').outerHTML===originalFrame`), true);
    });
    await test('copying opening prose shares the page until a named section is reached', async () => {
      assert.equal(await execute('return scrollY'), 0);
      assert.ok(await execute(`return document.getElementById('alpha').getBoundingClientRect().top>innerHeight`));
      await execute(`Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async value=>{window.copiedSection=value}}})`);
      await click('[data-reader-copy-link]');
      await eventually(() => execute('return !!window.copiedSection'), 'opening copy');
      assert.equal(await execute('return copiedSection'), origin + 'reader.html?opening=1');
      assert.equal(await execute(`return document.querySelector('[data-reader-section][aria-current="location"]')`), null);
      await execute(`document.getElementById('alpha').scrollIntoView()`);
      await eventually(() => execute(`return document.querySelector('[aria-current="location"]')?.textContent==='Alpha'`), 'first reached section');
      await click('[data-reader-copy-link]');
      assert.equal(await execute('return copiedSection'), origin + 'reader.html?opening=1#alpha');
      await execute('scrollTo(0,0)');
      await click('[data-reader-copy-link]');
      assert.equal(await execute('return copiedSection'), origin + 'reader.html?opening=1');
      assert.equal(await execute(`return document.querySelector('[data-reader-section][aria-current="location"]')`), null);
      assert.equal(await execute(`return document.querySelector('[data-reader-content]').innerHTML===originalBody && document.querySelector('iframe').outerHTML===originalFrame`), true);
    });
    await visit('reader.html');
    await test('scroll tracking leaves the URL untouched', async () => {
      await execute(`document.getElementById('beta').scrollIntoView()`);
      await eventually(() => execute(`return document.querySelector('[aria-current="location"]')?.textContent==='Beta'`), 'Beta active');
      assert.equal(await execute('return location.hash'), '');
      assert.ok(await execute(`return document.querySelector('[data-reader-progress]').value>0`));
    });
    await test('clipboard refusal provides a selectable section URL', async () => {
      await execute(`Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:()=>Promise.reject(new Error('denied'))}})`);
      await click('[data-reader-copy-link]');
      await eventually(() => execute(`return !!document.querySelector('.publication-reader__share-field input')`), 'copy fallback');
      assert.equal(await execute(`return document.querySelector('.publication-reader__share-field input').value`), origin + 'reader.html#beta');
      assert.equal(await execute(`return document.activeElement.selectionEnd-document.activeElement.selectionStart===document.activeElement.value.length`), true);
      assert.equal(await execute(`return document.querySelector('[data-reader-content]').innerHTML===originalBody`), true);
    });
    await test('copying strips auto-print and encodes literal section IDs', async () => {
      assert.equal(await execute(`return TriptychPublicationReader.sectionAddress(location.origin+'/project/web/gpt/reader.html?print=1&mode=study','a% b')`), origin + 'reader.html?mode=study#a%25%20b');
    });
    await test('successful clipboard copy reports success and closes the fallback', async () => {
      await execute(`Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async value=>{window.copiedSection=value}}})`);
      await click('[data-reader-copy-link]');
      await eventually(() => execute(`return document.querySelector('[data-reader-status]').textContent==='Section link copied.'`), 'clipboard success');
      assert.equal(await execute('return copiedSection'), origin + 'reader.html#beta');
      assert.equal(await execute(`return document.querySelector('.publication-reader__share-field').hidden`), true);
    });
    await test('document selector rejects cross-origin and unsafe schemes', async () => {
      assert.equal(await execute(`return TriptychPublicationReader.localDocument('javascript:alert(1)',location.href)`), null);
      await execute(`const s=document.querySelector('select');s.selectedIndex=2;s.dispatchEvent(new Event('change'))`);
      assert.equal(await execute('return location.pathname'), '/project/web/gpt/reader.html');
      assert.match(await execute(`return document.querySelector('[data-reader-status]').textContent`), /unavailable/);
    });
    await test('dropdown navigation and Back preserve the exact reader position', async () => {
      await execute(`scrollTo(0,1250)`); await delay(40);
      await execute(`const s=document.querySelector('select');s.selectedIndex=1;s.dispatchEvent(new Event('change'))`);
      await eventually(() => execute(`return location.pathname.endsWith('/other.html')`), 'other document');
      await command('POST', session + '/back', {});
      await eventually(() => execute(`return location.pathname.endsWith('/reader.html') && Math.abs(scrollY-1250)<3`), 'Back reader position');
    });
    await test('ordinary return navigation restores the reader position', async () => {
      await execute("dispatchEvent(new Event('wheel'));scrollTo(0,1450)"); await delay(40); await click('#other');
      await eventually(() => execute(`return location.pathname.endsWith('/other.html')`), 'other document');
      await click('#other');
      await eventually(() => execute(`return location.pathname.endsWith('/reader.html') && Math.abs(scrollY-1450)<3`), 'ordinary return reader position');
    });
    await test('an explicit fragment wins over remembered reading position', async () => {
      await click('#other'); await eventually(() => execute(`return location.pathname.endsWith('/other.html')`), 'other document');
      await click('#explicit');
      await eventually(() => execute(`return location.hash==='#gamma' && document.getElementById('gamma').getBoundingClientRect().top>=60 && document.getElementById('gamma').getBoundingClientRect().top<110`), 'Gamma fragment placement');
    });
    await test('narrow Contents closes after a native section link', async () => {
      await viewport(600); await visit('reader.html');
      assert.equal(await execute(`return document.querySelector('details').open`), false);
      await click('summary'); await click('[data-reader-section][href="#beta"]');
      await eventually(() => execute(`return location.hash==='#beta' && !document.querySelector('details').open`), 'narrow section selection');
      assert.ok(await execute(`return document.getElementById('beta').getBoundingClientRect().top>=60`));
    });
    await test('desktop Contents preference survives compact reflow', async () => {
      await viewport(1440); await delay(60); await execute(`document.querySelector('details').open=false`); await delay(40);
      await viewport(600); await delay(60); await viewport(1440); await delay(60);
      assert.equal(await execute(`return document.querySelector('details').open`), false);
    });
    await test('blocked optional storage leaves navigation usable', async () => {
      await visit('reader.html?blocked=1'); await execute('scrollTo(0,950)'); await delay(40); await click('#other');
      await eventually(() => execute(`return location.pathname.endsWith('/other.html')`), 'other document');
      await command('POST', session + '/back', {});
      await eventually(() => execute(`return location.search==='?blocked=1' && Math.abs(scrollY-950)<3`), 'history without storage');
    });
    await test('late reader height restores once available', async () => {
      await visit('other.html');
      await execute(`sessionStorage.setItem('triptych:catalogue:/project/web/gpt/reader.html?delay=1', JSON.stringify({x:0,y:1400}))`);
      await click('#delayed');
      await eventually(() => execute(`return location.search==='?delay=1' && Math.abs(scrollY-1400)<3`), 'delayed height restoration');
    });
    await test('user input cancels a pending late restoration', async () => {
      await visit('other.html');
      await execute(`sessionStorage.setItem('triptych:catalogue:/project/web/gpt/reader.html?delay=1', JSON.stringify({x:0,y:1400}))`);
      await click('#delayed'); await execute(`dispatchEvent(new Event('wheel'))`); await delay(850);
      assert.ok(await execute('return scrollY<100'));
    });
    await test('sticky toolbar clears keyboard focus without body mutation', async () => {
      await visit('reader.html');
      await execute(`const link=document.getElementById('body-link');scrollTo(0,link.getBoundingClientRect().top+scrollY-15);link.focus({preventScroll:true})`);
      assert.ok(await execute(`return document.getElementById('body-link').getBoundingClientRect().top>=document.querySelector('.publication-reader__toolbar').getBoundingClientRect().bottom+10`));
      assert.equal(await execute(`return document.querySelector('[data-reader-content]').innerHTML===originalBody && document.querySelector('iframe').outerHTML===originalFrame`), true);
    });
    fs.writeFileSync(path.join(evidence, 'results.json'), JSON.stringify({passed: results.length, cases: results}, null, 2) + '\n');
    console.log(`${results.length} reader client checks passed.`);
  } catch (error) {
    if (session) {
      try { fs.writeFileSync(path.join(evidence, 'failure.png'), Buffer.from(await command('GET', session + '/screenshot'), 'base64')); } catch (_) {}
      try { fs.writeFileSync(path.join(evidence, 'failure.json'), JSON.stringify(await execute(`return {url:location.href,y:scrollY,state:history.state,referrer:document.referrer,ready:document.readyState,navigation:performance.getEntriesByType('navigation')[0].type,storage:Object.fromEntries(Object.entries(sessionStorage)),scripts:Array.from(document.scripts,s=>s.src)}`),null,2)); } catch (_) {}
    }
    throw error;
  } finally {
    if (session) await command('DELETE', session).catch(() => {});
    const stopped = once(driver, 'exit'); driver.kill('SIGTERM'); await stopped;
    fs.closeSync(log); await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error.stack); process.exitCode = 1; });
