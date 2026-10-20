#!/usr/bin/env node

/* Exact source reading alternatives through the production Propers adapter and renderer. */

import assert from 'node:assert/strict';
import { spawn, execFileSync } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const OVERLAY = process.env.TRIPTYCH_LATIN_MODULE_ROOT;
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/reader-latin-accompaniment/browser'));
const DAY = '/src/web/browser/liturgy/day.html';
const PROPERS = '/src/web/browser/liturgy/index.html';

const mime = (file) => ({ '.css': 'text/css', '.html': 'text/html',
  '.js': 'text/javascript', '.json': 'application/json' })[extname(file)] || 'application/octet-stream';

function server() {
  return createServer(async (request, response) => {
    try {
      let relative = decodeURIComponent(new URL(request.url, 'http://localhost').pathname)
        .replace(/^\/+/, '');
      if (relative === 'favicon.ico') { response.writeHead(204); response.end(); return; }
      if (/^src\/web\/data\/[^/]+\/chapters\//.test(relative)) {
        relative = relative.replace(/^src\/web\/data\//, 'src/sources/bibles/');
      }
      const file = resolve(ROOT, relative || 'README.md');
      if (!file.startsWith(ROOT + sep)) throw new Error('outside repository');
      response.writeHead(200, { 'content-type': mime(file), 'cache-control': 'no-store' });
      const body = OVERLAY ? await readFile(resolve(OVERLAY, relative)).catch(() => readFile(file))
        : await readFile(file);
      response.end(body);
    } catch (_error) { response.writeHead(404); response.end('not found'); }
  });
}

async function listen(instance) {
  await new Promise((done, reject) => {
    instance.once('error', reject);
    instance.listen(0, '127.0.0.1', done);
  });
  return instance.address().port;
}

async function freePort() {
  const instance = server();
  const port = await listen(instance);
  await new Promise((done) => instance.close(done));
  return port;
}

async function waitJson(url) {
  for (let attempt = 0; attempt < 120; attempt += 1) {
    try { const reply = await fetch(url); if (reply.ok) return reply.json(); }
    catch (_error) { /* Chromium is starting. */ }
    await new Promise((done) => setTimeout(done, 50));
  }
  throw new Error('Chromium debugging endpoint did not start');
}

class CDP {
  constructor(url) {
    this.socket = new WebSocket(url);
    this.next = 0;
    this.pending = new Map();
    this.events = new Map();
  }
  on(name, callback) {
    this.events.set(name, [...(this.events.get(name) || []), callback]);
  }
  async ready() {
    await new Promise((done, reject) => {
      this.socket.addEventListener('open', done, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (!message.id) {
        for (const callback of this.events.get(message.method) || []) callback(message.params);
        return;
      }
      const pending = this.pending.get(message.id);
      if (!pending) return;
      this.pending.delete(message.id);
      clearTimeout(pending.timer);
      if (message.error) pending.reject(new Error(message.error.message));
      else pending.resolve(message.result);
    });
  }
  send(method, params = {}) {
    const id = ++this.next;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id); reject(new Error('CDP timeout: ' + method));
      }, 30000);
      this.pending.set(id, { resolve, reject, timer });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }
  close() { this.socket.close(); }
}

async function evaluate(cdp, expression) {
  const reply = await cdp.send('Runtime.evaluate', {
    expression, awaitPromise: true, returnByValue: true, userGesture: true
  });
  if (reply.exceptionDetails) throw new Error(
    reply.exceptionDetails.exception?.description || reply.exceptionDetails.text);
  return reply.result.value;
}

async function waitFor(cdp, expression, label) {
  for (let attempt = 0; attempt < 240; attempt += 1) {
    if (await evaluate(cdp, `Boolean(${expression})`)) return;
    await new Promise((done) => setTimeout(done, 50));
  }
  throw new Error('Timed out waiting for ' + label);
}

async function key(cdp, name) {
  const codes = { Enter: 13, Escape: 27, ' ': 32 };
  for (const type of ['keyDown', 'keyUp']) await cdp.send('Input.dispatchKeyEvent', {
    type, key: name, code: name === ' ' ? 'Space' : name,
    windowsVirtualKeyCode: codes[name], nativeVirtualKeyCode: codes[name],
    ...(type === 'keyDown' && name !== 'Escape' ? { text: name === 'Enter' ? '\r' : name } : {})
  });
}

const instance = server();
const port = await listen(instance);
const debugPort = await freePort();
await mkdir(SCRATCH, { recursive: true });
const profile = await mkdtemp(resolve(SCRATCH, 'chromium-'));
const chrome = spawn(CHROME, ['--headless=new','--disable-gpu','--no-sandbox','--disable-dev-shm-usage',
  `--remote-debugging-port=${debugPort}`,`--user-data-dir=${profile}`,'about:blank'], {stdio:'ignore'});
let cdp;
const assertions=[], consoleProblems=[], failedRequests=[], httpProblems=[];
try {
  const pages=await waitJson(`http://127.0.0.1:${debugPort}/json`);
  cdp=new CDP(pages.find(page=>page.type==='page').webSocketDebuggerUrl); await cdp.ready();
  cdp.on('Runtime.exceptionThrown',({exceptionDetails})=>consoleProblems.push(exceptionDetails?.exception?.description||exceptionDetails?.text));
  cdp.on('Runtime.consoleAPICalled',({type,args})=>{if(type==='error'||type==='warning')consoleProblems.push(args.map(one=>one.value||one.description||'').join(' '));});
  cdp.on('Network.loadingFailed',({canceled,errorText})=>{if(!canceled)failedRequests.push(errorText);});
  cdp.on('Network.responseReceived',({response})=>{if(response?.status>=400)httpProblems.push({status:response.status,url:response.url});});
  await Promise.all([cdp.send('Page.enable'),cdp.send('Runtime.enable'),cdp.send('Network.enable')]);
  await cdp.send('Page.addScriptToEvaluateOnNewDocument',{source:`Storage.prototype.getItem=function(){throw new Error('storage unavailable')};Storage.prototype.setItem=function(){throw new Error('storage unavailable')};`});
  await cdp.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
  const origin=`http://127.0.0.1:${port}`;
  const paired='&text-display=latin-and-selected';
  const day='#date=2026-05-24&missal=roman-1962&bible=douay-rheims&orations=en';
  const proper='#missal=roman-1962&type=seasonal&mass=pentecost&bible=douay-rheims&orations=en';
  let entrance='propers';
  const debug=()=>entrance==='day'?'dayReaderDebug':'propersReaderDebug';
  async function settled(){await waitFor(cdp,`window.${debug()}?.ready && document.getElementById('reader-document').getAttribute('aria-busy')==='false'`,'settled '+entrance);await evaluate(cdp,`new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))`);}
  async function visit(hash,path=PROPERS){entrance=path.includes('day')?'day':'propers';await cdp.send('Page.navigate',{url:origin+path+'?data=/src/web/data'+hash});await settled();assert.equal(await evaluate(cdp,`${debug()}.outcome`),'ready');}
  const click=async selector=>evaluate(cdp,`document.querySelector(${JSON.stringify(selector)}).click()`);
  const inventory=()=>evaluate(cdp,`({ids:[...document.querySelectorAll('#reader-document [data-semantic-event-id]')].map(n=>n.dataset.semanticEventId),contents:[...document.querySelectorAll('[data-reader-location]')].map(n=>n.dataset.readerLocation),state:${debug()}.state})`);
  for(const [path,identity]of[[DAY,day],[PROPERS,proper]]){
    await visit(identity+'&mode=read',path);const plain=await inventory();
    assert.equal(await evaluate(cdp,`document.querySelectorAll('#reader-document .text-pair').length`),0);
    await visit(identity+'&mode=read'+paired,path);const pair=await inventory();
    assert.deepEqual(pair.ids,plain.ids);assert.deepEqual(pair.contents,plain.contents);assert.equal(pair.state.textDisplay,'latin-and-selected');
    const collect=await evaluate(cdp,`(()=>{const n=[...document.querySelectorAll('#reader-document .proper')].find(n=>n.querySelector(':scope > .proper-name')?.textContent.startsWith('Collect'));return {languages:[...n.querySelectorAll('.text-side')].map(s=>s.dataset.textLanguage),widths:[...n.querySelectorAll('.text-side')].map(s=>s.getBoundingClientRect().width),sources:[...n.querySelectorAll('.text-side')].map(s=>s.dataset.textSourceId),relationship:[...n.querySelectorAll('.text-side')].map(s=>s.dataset.textRelationship),sideways:[...n.querySelectorAll('.text-side')].map(s=>s.getBoundingClientRect().left)}})()`);
    assert.deepEqual(collect.languages,['la','en']);assert.ok(collect.widths.every(n=>n>450),JSON.stringify(collect));assert.ok(collect.sideways[1]>collect.sideways[0]);assert.ok(collect.sources.every(Boolean));assert.deepEqual(collect.relationship,['exact-target','historical-antecedent']);
    const lesson=await evaluate(cdp,`(()=>{const n=[...document.querySelectorAll('#reader-document .proper')].find(n=>n.querySelector(':scope > .proper-name')?.textContent.startsWith('Lesson'));return [...n.querySelectorAll('.text-side')].map(s=>({text:s.textContent,bodies:s.querySelectorAll('.composed').length}))})()`);
    assert.equal(lesson[0].bodies,1);assert.equal(lesson[1].bodies,0);assert.match(lesson[1].text,/English translation unavailable/);
    assert.equal(await evaluate(cdp,`document.documentElement.scrollWidth>document.documentElement.clientWidth+1`),false);
    assert.equal(await evaluate(cdp,`document.querySelector('.reader-actions').getBoundingClientRect().right < document.getElementById('reader-document').getBoundingClientRect().left`),true);
  }
  assertions.push('both Read entrances retain event and Contents order while showing wide held pairs and precise English gaps');

  for(const width of[1024,768,393,320]){
    await cdp.send('Emulation.setDeviceMetricsOverride',{width,height:852,deviceScaleFactor:1,mobile:false});
    assert.equal(await evaluate(cdp,`document.documentElement.scrollWidth>document.documentElement.clientWidth+1`),false);
    assert.equal(await evaluate(cdp,`(()=>{const p=document.querySelector('#reader-document .text-pair');const s=[...p.children].map(n=>n.getBoundingClientRect());return s[1].top>=s[0].bottom-1})()`),true);
  }
  assertions.push('1024 768 393 and exact 320 widths stack owner-level fragments without page overflow');

  await visit(proper+'&mode=read'+paired);
  await evaluate(cdp,`(()=>{const node=document.querySelector('[data-semantic-event-id="proper/roman-1962/pentecost/005"]');node.scrollIntoView();})()`);
  await evaluate(cdp,`new Promise(resolve=>setTimeout(resolve,500))`);
  await click('[data-reader-action="mode"]'); await click('[data-reader-action="details"]');
  await waitFor(cdp,`document.querySelector('[data-reader-text-display]')&&!document.querySelector('[data-reader-text-display]').disabled`,'presentation control');
  assert.equal(await evaluate(cdp,`document.querySelector('[data-reader-text-display]').checked`),true);
  const locationBefore = await evaluate(cdp,`TriptychReaderTextSize.captureLocation(window,document.getElementById('reader-document')).id`);
  assert.ok(locationBefore);
  await click('[data-reader-text-display]');
  await waitFor(cdp,`window.propersReaderDebug?.ready&&propersReaderDebug.state?.textDisplay==='selected'`,'presentation switch');await settled();
  assert.equal(await evaluate(cdp,`document.querySelectorAll('#reader-document .text-pair').length`),0);
  assert.equal(await evaluate(cdp,`document.activeElement.dataset.readerAction`),'mode');
  assert.equal(await evaluate(cdp,`new URLSearchParams(location.hash.slice(1)).get('location')`),locationBefore);
  await click('[data-reader-action="mode"]'); await click('[data-reader-action="details"]');
  await click('[data-reader-text-display]');await waitFor(cdp,`propersReaderDebug.ready&&propersReaderDebug.state?.textDisplay==='latin-and-selected'`,'paired again');await settled();
  await key(cdp,'Escape');
  assertions.push('shared guarded control changes canonical display state while preserving focus and semantic place without storage');

  for(const [path,identity]of[[DAY,day],[PROPERS,proper]]){
    await visit(identity+'&mode=missal&ordinary-lang=en',path);const prior=await inventory();
    await visit(identity+'&mode=missal&ordinary-lang=en'+paired,path);
    const inv=await inventory();assert.equal(new Set(inv.ids).size,inv.ids.length);assert.deepEqual(inv.ids,prior.ids);assert.deepEqual(inv.contents,prior.contents);
    const turns=await evaluate(cdp,`(()=>{const n=document.querySelector('[data-semantic-event-id="ordinary-element/oblatio/sursum-corda"]');return {owners:n.querySelectorAll('.ordinary-element').length,sides:[...n.querySelectorAll('.text-side')].map(s=>({turns:s.querySelectorAll('.ordinary-turn').length,cues:s.querySelectorAll('.ordinary-turn-cue').length,source:s.dataset.textSourceId,lang:s.dataset.textLanguage}))}})()`);
    assert.equal(turns.owners,0);assert.deepEqual(turns.sides.map(s=>s.lang),['la','en']);assert.deepEqual(turns.sides.map(s=>s.turns),[6,6]);assert.deepEqual(turns.sides.map(s=>s.cues),[6,6]);assert.ok(turns.sides.every(s=>s.source));
    assert.equal(await evaluate(cdp,`document.documentElement.scrollWidth>document.documentElement.clientWidth+1`),false);
  }
  await cdp.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
  assert.equal(await evaluate(cdp,`[...document.querySelectorAll('.text-side .composed > .speaker-tag.is-opening-cue')].every(n=>{const a=n.getBoundingClientRect(),b=n.closest('.text-side').getBoundingClientRect();return a.left>=b.left-1&&a.right<=b.right+1})`),true);
  assertions.push('both Missal entrances keep one event and Contents entry per source owner with separately sourced Ordinary turns');

  await visit(day+'&mode=study&ordinary=1&ordinary-lang=en'+paired,DAY);
  assert.ok(await evaluate(cdp,`document.querySelectorAll('.study-event .text-pair,.text-pair').length>0`));
  assert.ok(await evaluate(cdp,`document.querySelectorAll('.study-facts').length>0`));
  assertions.push('Study with Ordinary retains both held language bodies and source apparatus');

  const compare='#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims&orations=en&mode=compare&compare=oration-language&peer-orations=la';
  await visit(compare+paired);
  const comparison=await evaluate(cdp,`({state:propersReaderDebug.state, sides:[...document.querySelectorAll('[data-semantic-event-id="compare/proper/collect"] > .compare-pair > .compare-side')].map(n=>({status:n.dataset.compareStatus,pairs:n.querySelectorAll('.text-pair').length,latin:n.querySelectorAll('[data-text-language="la"] .composed').length,missing:n.querySelector('.unit-absence')?.textContent}))})`);
  assert.equal(comparison.state.comparison.dimension,'oration-language');assert.deepEqual(comparison.state.comparison.sides.map(s=>s.languages.orations),['en','la']);
  assert.equal(comparison.sides[0].status,'text-unavailable');assert.equal(comparison.sides[0].pairs,1);assert.equal(comparison.sides[0].latin,1);assert.match(comparison.sides[0].missing,/English translation unavailable/);assert.equal(comparison.sides[1].pairs,0);
  assertions.push('Compare retains its selected language axis and unavailable primary status while held Latin remains visible; selected Latin is not duplicated');

  await cdp.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
  assert.equal(await evaluate(cdp,`(()=>{const s=[...document.querySelector('.text-pair').children].map(n=>n.getBoundingClientRect());return s[1].top>=s[0].bottom-1})()`),true);
  assertions.push('language pairs inside Compare cells remain stacked at wide widths');

  await visit(proper+'&mode=read'+paired);
  await cdp.send('Emulation.setEmulatedMedia',{media:'print'});
  const pdf=await cdp.send('Page.printToPDF',{printBackground:true,preferCSSPageSize:true});const pdfPath=resolve(SCRATCH,'pentecost-latin-accompaniment.pdf');await writeFile(pdfPath,Buffer.from(pdf.data,'base64'));
  const text=execFileSync('/usr/bin/pdftotext',[pdfPath,'-'],{encoding:'utf8'});await writeFile(resolve(SCRATCH,'pentecost-latin-accompaniment.txt'),text);
  assert.match(text,/Pentecost/);assert.match(text,/Latin alongside translated prayers/);assert.match(text,/English translation unavailable/);assert.match(text,/historical antecedent/);assert.match(text,/Latin source/);assert.match(text,/Cummiskey/);assert.doesNotMatch(text,/Show Latin alongside|Share link/);
  await cdp.send('Emulation.setEmulatedMedia',{media:'screen'});
  const screenshot=await cdp.send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await writeFile(resolve(SCRATCH,'paired-read-1440.png'),Buffer.from(screenshot.data,'base64'));
  assertions.push('print preserves both language bodies independent source qualifications and gaps while hiding the presentation control');

  await cdp.send('Page.navigate',{url:origin+PROPERS+'?data=/src/web/data'+proper+'&text-display=bad'});await settled();assert.equal(await evaluate(cdp,'propersReaderDebug.outcome'),'invalid');assert.equal(await evaluate(cdp,'document.querySelectorAll(".text-pair").length'),0);
  assert.deepEqual(consoleProblems,[]);assert.deepEqual(failedRequests,[]);assert.deepEqual(httpProblems,[]);
  process.stdout.write(JSON.stringify({status:'pass',checks:assertions.length,assertions,consoleProblems,failedRequests,httpProblems})+'\n');
}catch(error){const state=cdp?await evaluate(cdp,`({hash:location.hash,day:window.dayReaderDebug,propers:window.propersReaderDebug})`).catch(()=>null):null;process.stderr.write(JSON.stringify({status:'fail',error:error.stack,state,assertions,consoleProblems,failedRequests,httpProblems})+'\n');process.exitCode=1;}
finally{if(cdp)cdp.close();const stopped=new Promise(done=>chrome.once('exit',done));chrome.kill('SIGTERM');await stopped;await new Promise(done=>instance.close(done));await rm(profile,{recursive:true,force:true,maxRetries:4,retryDelay:100});}
