#!/usr/bin/env node

/* Named Latin Scripture companions over independently addressed citation fragments. */

import assert from 'node:assert/strict';
import { spawn, execFileSync } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const OVERLAY = process.env.TRIPTYCH_SCRIPTURE_MODULE_ROOT;
const BASELINE = process.env.TRIPTYCH_SCRIPTURE_BASELINE_ROOT || null;
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/reader-scripture-companion/browser'));
const DAY = '/src/web/browser/liturgy/day.html';
const PROPERS = '/src/web/browser/liturgy/index.html';

const mime = (file) => ({ '.css': 'text/css', '.html': 'text/html',
  '.js': 'text/javascript', '.json': 'application/json' })[extname(file)] || 'application/octet-stream';

function server(overlay = OVERLAY) {
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
      const body = overlay ? await readFile(resolve(overlay, relative)).catch(() => readFile(file))
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
  const paired='&scripture-companion=clementine-vulgate';
  const day='#date=2026-11-29&missal=roman-1962&bible=douay-rheims&orations=la';
  const proper='#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims&orations=la';
  let entrance='propers';
  const debug=()=>entrance==='day'?'dayReaderDebug':'propersReaderDebug';
  async function settled(){await waitFor(cdp,`window.${debug()}?.ready && document.getElementById('reader-document').getAttribute('aria-busy')==='false'`,'settled '+entrance);await evaluate(cdp,`new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))`);}
  async function visit(hash,path=PROPERS){entrance=path.includes('day')?'day':'propers';await cdp.send('Page.navigate',{url:origin+path+'?data=/src/web/data'+hash});await settled();assert.equal(await evaluate(cdp,`${debug()}.outcome`),'ready');}
  const click=async selector=>evaluate(cdp,`document.querySelector(${JSON.stringify(selector)}).click()`);
  const inventory=()=>evaluate(cdp,`({ids:[...document.querySelectorAll('#reader-document [data-semantic-event-id]')].map(n=>n.dataset.semanticEventId),contents:[...document.querySelectorAll('[data-reader-location]')].map(n=>n.dataset.readerLocation),state:${debug()}.state})`);
  for(const [path,identity]of[[DAY,day],[PROPERS,proper]]){
    await visit(identity+'&mode=read',path);const plain=await inventory();
    const selectedText=await evaluate(cdp,`[...document.querySelectorAll('#reader-document .citation')].map(n=>n.textContent)`);
    assert.equal(await evaluate(cdp,`document.querySelectorAll('#reader-document .scripture-side').length`),0);
    await visit(identity+'&mode=read'+paired,path);const pair=await inventory();
    assert.deepEqual(pair.ids,plain.ids);assert.deepEqual(pair.contents,plain.contents);assert.deepEqual(pair.state.scriptureCompanion,{id:'clementine-vulgate',numbering:'vulgate'});
    assert.equal(Object.hasOwn(pair.state,'textDisplay'),false);
    assert.deepEqual(await evaluate(cdp,`[...document.querySelectorAll('#reader-document .scripture-side[data-bible-edition="douay-rheims"] .citation')].map(n=>n.textContent)`),selectedText);
    const sides=await evaluate(cdp,`(()=>{const p=document.querySelector('#reader-document .scripture-pair');return [...p.children].map(n=>({left:n.getBoundingClientRect().left,width:n.getBoundingClientRect().width,edition:n.dataset.bibleEdition,lang:n.dataset.textLanguage,numbering:n.dataset.bibleNumbering,witness:n.dataset.bibleWitness,text:n.textContent}))})()`);
    assert.deepEqual(sides.map(s=>s.edition),['clementine-vulgate','douay-rheims']);assert.deepEqual(sides.map(s=>s.lang),['la','en']);
    assert.ok(sides.every(s=>s.width>450&&s.numbering==='vulgate'&&s.witness),JSON.stringify(sides));assert.ok(sides[1].left>sides[0].left);
    assert.equal(await evaluate(cdp,`[...document.querySelectorAll('#reader-document .proper > .composed')].every(n=>n.getBoundingClientRect().width<=636.5)`),true,'unpaired bodies retain the reading measure');
    assert.equal(await evaluate(cdp,`document.documentElement.scrollWidth>document.documentElement.clientWidth+1`),false);
    assert.equal(await evaluate(cdp,`document.querySelector('.reader-actions').getBoundingClientRect().right < document.getElementById('reader-document').getBoundingClientRect().left`),true);
  }
  assertions.push('both Read entrances preserve selected Bible words event/Contents order and named wide citation pairs');

  for(const width of[1024,768,393,320]){
    await cdp.send('Emulation.setDeviceMetricsOverride',{width,height:852,deviceScaleFactor:1,mobile:false});
    assert.equal(await evaluate(cdp,`document.documentElement.scrollWidth>document.documentElement.clientWidth+1`),false);
    assert.equal(await evaluate(cdp,`(()=>{const p=document.querySelector('#reader-document .scripture-pair');const s=[...p.children].map(n=>n.getBoundingClientRect());return s[1].top>=s[0].bottom-1})()`),true);
  }
  assertions.push('1024 768 393 and exact320 stack each citation independently without overflow');
  await cdp.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});

  for(const mode of['missal','study'])for(const [path,identity]of[[DAY,day],[PROPERS,proper]]){
    const modeKey='&mode='+mode+(mode==='study'?'&ordinary=1':'')+'&ordinary-lang=en';
    await visit(identity+modeKey,path);const plain=await inventory();
    await visit(identity+modeKey+paired+'&text-display=latin-and-selected',path);const pair=await inventory();
    assert.deepEqual(pair.ids,plain.ids);assert.deepEqual(pair.contents,plain.contents);
    assert.ok(await evaluate(cdp,`document.querySelectorAll('#reader-document .scripture-pair').length>0`));
    if(pair.state.options.ordinary)assert.ok(await evaluate(cdp,`document.querySelectorAll('#reader-document .ordinary-element > .text-pair').length>0`));
  }
  assertions.push('both Missal and Study entrances retain one semantic owner per event while prayer and Bible companions coexist');

  await visit(proper.replace('bible=douay-rheims','bible=clementine-vulgate')+'&mode=read'+paired);
  const same=await evaluate(cdp,`({pairs:document.querySelectorAll('#reader-document .scripture-pair').length,single:document.querySelectorAll('#reader-document .scripture-single').length,editions:[...document.querySelectorAll('#reader-document .scripture-side')].map(n=>n.dataset.bibleEdition)})`);
  assert.equal(same.pairs,0);assert.ok(same.single>0);assert.ok(same.editions.every(id=>id==='clementine-vulgate'));
  assertions.push('a selected Clementine Bible appears once per citation');

  const epiphany='#missal=roman-1962&type=christological&mass=epiphania-domini&bible=douay-rheims&orations=la&mode=compare&compare=bible-edition&peer-bible=king-james-version';
  await visit(epiphany+paired);
  const comparison=await evaluate(cdp,`(()=>{const n=document.querySelector('.compare-side[data-bible-edition="king-james-version"][data-bible-citations="refused"]');return {dimension:propersReaderDebug.state.comparison.dimension,companion:propersReaderDebug.state.scriptureCompanion,refusal:n?.textContent,latin:n?.querySelector('.scripture-side[data-bible-edition="clementine-vulgate"] .verse')?.textContent,status:n?.dataset.compareStatus,stacked:[...document.querySelectorAll('.compare-side .scripture-pair')].every(p=>p.children[1].getBoundingClientRect().top>=p.children[0].getBoundingClientRect().bottom-1)}})()`);
  assert.equal(comparison.dimension,'bible-edition');assert.deepEqual(comparison.companion,{id:'clementine-vulgate',numbering:'vulgate'});assert.ok(comparison.stacked);
  assert.match(comparison.refusal,/English Bibles divide Psalm 72 differently/);assert.ok(comparison.latin);assert.equal(comparison.status,'text-held');
  assertions.push('Bible Compare retains the selected KJV refusal and its primary axis while internal Latin citation pairs stack');

  const key='commemoratione-omnium-fidelium-defunctorum',caswall='edition.edward-caswall.lyra-catholica.london-1849',cummiskey='edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861';
  const witness='#missal=roman-1962&type=sanctoral&mass='+key+'&form=first&bible=douay-rheims&orations=en&mode=compare&compare=translation-witness&translation-witness='+caswall+'&peer-witness='+cummiskey;
  await visit(witness+paired+'&text-display=latin-and-selected');
  const witnesses=await evaluate(cdp,`({dimension:propersReaderDebug.state.comparison.dimension,peers:propersReaderDebug.state.comparison.sides.map(s=>s.languages.translationWitness),pairs:document.querySelectorAll('.compare-side .scripture-pair').length})`);
  assert.equal(witnesses.dimension,'translation-witness');assert.deepEqual(witnesses.peers,[caswall,cummiskey]);assert.ok(witnesses.pairs>0);
  assertions.push('same-language witness Compare keeps its explicit source peers and separate internal Bible pairs');

  await visit(proper+'&mode=read&text-display=latin-and-selected'+paired);
  await evaluate(cdp,`document.querySelectorAll('#reader-document [data-semantic-event-id]')[3].scrollIntoView()`);
  await evaluate(cdp,`new Promise(resolve=>setTimeout(resolve,500))`);
  await click('[data-reader-action="mode"]');await click('[data-reader-action="details"]');
  await waitFor(cdp,`document.querySelector('[data-reader-scripture-companion]')&&!document.querySelector('[data-reader-scripture-companion]').disabled`,'Scripture control');
  const place=await evaluate(cdp,`TriptychReaderTextSize.captureLocation(window,document.getElementById('reader-document')).id`);
  assert.ok(place,'a source event remains the captured reading position');
  await click('[data-reader-scripture-companion]');await waitFor(cdp,`propersReaderDebug.ready&&!propersReaderDebug.state?.scriptureCompanion`,'companion off');await settled();
  assert.equal(await evaluate(cdp,`propersReaderDebug.state.scriptureCompanion===undefined`),true);
  assert.equal(await evaluate(cdp,`propersReaderDebug.state.textDisplay`),'latin-and-selected');
  assert.equal(await evaluate(cdp,`new URLSearchParams(location.hash.slice(1)).get('location')`),place);
  assert.equal(await evaluate(cdp,`document.activeElement?.dataset.readerAction`),'mode');
  await click('[data-reader-action="mode"]');await click('[data-reader-action="details"]');
  await waitFor(cdp,`document.querySelector('[data-reader-scripture-companion]')&&!document.querySelector('[data-reader-scripture-companion]').disabled`,'Scripture control on');
  await click('[data-reader-scripture-companion]');await waitFor(cdp,`propersReaderDebug.ready&&propersReaderDebug.state?.scriptureCompanion?.id==='clementine-vulgate'`,'companion on');await settled();
  assert.equal(await evaluate(cdp,`propersReaderDebug.state.scriptureCompanion.id`),'clementine-vulgate');
  assertions.push('Details control toggles only the explicit companion while preserving prayer choice semantic place and focus without storage');

  await visit(proper+'&mode=read'+paired);
  await evaluate(cdp,`window.scrollTo({top:0,behavior:'instant'});new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))`);
  const image=await cdp.send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});
  await writeFile(resolve(SCRATCH,'scripture-pairs-1440.png'),Buffer.from(image.data,'base64'));
  await cdp.send('Emulation.setEmulatedMedia',{media:'print'});
  const printed=await cdp.send('Page.printToPDF',{printBackground:true,preferCSSPageSize:true});
  const pdf=resolve(SCRATCH,'advent-1-scripture-companion.pdf');await writeFile(pdf,Buffer.from(printed.data,'base64'));
  const text=execFileSync('pdftotext',['-layout',pdf,'-'],{encoding:'utf8'});await writeFile(resolve(SCRATCH,'advent-1-scripture-companion.txt'),text);
  assert.match(text,/Latin Bible companion: Clementine Vulgate/);assert.match(text,/Vulgate numbering/);assert.match(text,/Gallican psalter/);assert.match(text,/public domain/);assert.match(text,/not the Missal/);
  assert.match(text,/Douay-Rheims/);assert.match(text,/Clementine Vulgate/);assert.match(text,/Ad te/);
  assert.doesNotMatch(text,/Show Latin alongside the selected Bible|Share link/);
  await cdp.send('Emulation.setEmulatedMedia',{media:''});
  assertions.push('standalone print retains companion and selected edition identity numbering rights and Bible-wording qualification');

  const baselineInstance=BASELINE ? server(BASELINE) : null;
  const baselinePort=baselineInstance ? await listen(baselineInstance) : null;
  try{
    for(const bible of['douay-rheims','clementine-vulgate']){
      const route='/src/web/browser/scripture/track.html?data=/src/web/data#tier=landmarks&reading=1&bible='+bible;
      let before=null;
      if(baselineInstance){
        await cdp.send('Page.navigate',{url:`http://127.0.0.1:${baselinePort}`+route});
        await waitFor(cdp,`document.getElementById('reading')?.getAttribute('aria-busy')==='false'&&document.querySelector('#reading .passage')`,'baseline Scripture track');
        before=await evaluate(cdp,`document.getElementById('reading').innerHTML`);
      }
      await cdp.send('Page.navigate',{url:origin+route});
      await waitFor(cdp,`document.getElementById('reading')?.getAttribute('aria-busy')==='false'&&document.querySelector('#reading .passage')`,'candidate Scripture track');
      if(before!==null)assert.equal(await evaluate(cdp,`document.getElementById('reading').innerHTML`),before,bible);
      const text=await evaluate(cdp,`document.querySelector('#reading .passage').textContent`);
      assert.match(text,bible==='douay-rheims'?/In the beginning God created/:/In principio creavit Deus/);
      assert.equal(await evaluate(cdp,`document.querySelectorAll('.scripture-side,.scripture-pair').length`),0);
    }
  }finally{if(baselineInstance)await new Promise(done=>baselineInstance.close(done));}
  assertions.push(BASELINE?'real non-liturgy Scripture track renders identical English and Latin DOM with the default shared loader':'real non-liturgy Scripture track retains selected English and Latin text through the default shared loader');

  entrance='propers';await cdp.send('Page.navigate',{url:origin+PROPERS+'?data=/src/web/data'+proper+'&scripture-companion=douay-rheims'});
  await waitFor(cdp,`window.propersReaderDebug?.ready`,'invalid companion refusal');
  assert.notEqual(await evaluate(cdp,`propersReaderDebug.outcome`),'ready');
  assert.equal(await evaluate(cdp,`document.querySelectorAll('#reader-document .scripture-side').length`),0);
  assertions.push('explicit non-Latin companion route fails closed without substitution');

  assert.deepEqual(consoleProblems,[]);assert.deepEqual(failedRequests,[]);assert.deepEqual(httpProblems,[]);
  process.stdout.write(JSON.stringify({status:'pass',checks:assertions.length,assertions,consoleProblems,failedRequests,httpProblems})+'\n');
}catch(error){const state=cdp?await evaluate(cdp,`({hash:location.hash,day:window.dayReaderDebug,propers:window.propersReaderDebug})`).catch(()=>null):null;process.stderr.write(JSON.stringify({status:'fail',error:error.stack,state,assertions,consoleProblems,failedRequests,httpProblems})+'\n');process.exitCode=1;}
finally{if(cdp)cdp.close();const stopped=new Promise(done=>chrome.once('exit',done));chrome.kill('SIGTERM');await stopped;await new Promise(done=>instance.close(done));await rm(profile,{recursive:true,force:true,maxRetries:4,retryDelay:100});}
