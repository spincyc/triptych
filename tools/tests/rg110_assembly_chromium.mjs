#!/usr/bin/env node

/* RG110 exact prayer groups through the production Day reader and shared renderer. */

import assert from 'node:assert/strict';
import { spawn, execFileSync } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const OVERLAY = process.env.TRIPTYCH_RG110_MODULE_ROOT;
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/rg110-assembly/browser'));
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

  const report=[];
  for(const date of ['2027-02-22','2027-01-25','2026-06-30','2060-02-22']) for(const mode of ['read','missal','study']) {
    const hash='#date='+date+'&missal=roman-1962&bible=douay-rheims&orations=la&mode='+mode+'&ordinary-lang=la';
    await cdp.send('Page.navigate',{url:origin+DAY+'?data=/src/web/data'+hash});
    await waitFor(cdp,`window.dayReaderDebug?.ready && dayReaderDebug.state?.civilDate==='${date}' && dayReaderDebug.state?.requestedMode==='${mode}' && document.getElementById('reader-document').getAttribute('aria-busy')==='false'`,'RG110 '+date+' '+mode);
    const result=await evaluate(cdp,`({outcome:dayReaderDebug.outcome,notes:document.querySelectorAll('#reader-document .inseparable-oration-note').length,groups:document.querySelectorAll('#reader-document .inseparable-oration-group').length,text:document.getElementById('reader-document').textContent,semantics:dayReaderDebug.semantic})`);
    assert.equal(result.outcome,'ready',JSON.stringify(result));assert.equal(result.notes,3);assert.equal(result.groups,3);
    assert.match(result.text,/These two prayers count as one/);
    if(date !== '2026-06-30') assert.ok(result.text.includes('Pauli') && result.text.includes('Petro')); else assert.match(result.text,/unavailable/);
    report.push({date,mode,outcome:result.outcome,notes:result.notes});
  }
  await cdp.send('Page.navigate',{url:origin+DAY+'?data=/src/web/data#date=2027-02-22&missal=roman-1962&bible=douay-rheims&orations=en&mode=read'});
  await waitFor(cdp,`window.dayReaderDebug?.ready && document.getElementById('reader-document').getAttribute('aria-busy')==='false'`,'English group');
  const english=await evaluate(cdp,`({notes:document.querySelectorAll('.inseparable-oration-note').length,text:document.getElementById('reader-document').textContent})`);
  assert.equal(english.notes,3);assert.match(english.text,/English translation unavailable/);assert.match(english.text,/Paul/);

  for (const [date,lang,peer] of [['2026-06-30','en','roman-pre-1955']]) {
    await cdp.send('Page.navigate',{url:origin+DAY+'?data=/src/web/data#date='+date+'&missal=roman-1962&bible=douay-rheims&orations='+lang+'&mode=compare&compare=recension&peer-missal='+peer+'&territory=universal&ordinary=0'});
    await waitFor(cdp,`window.dayReaderDebug?.ready && dayReaderDebug.state?.civilDate==='${date}' && dayReaderDebug.state?.requestedMode==='compare' && document.getElementById('reader-document').getAttribute('aria-busy')==='false'`,'Compare '+date);
    const compared=await evaluate(cdp,`({outcome:dayReaderDebug.outcome,notes:document.querySelectorAll('#reader-document .inseparable-oration-note').length,text:document.getElementById('reader-document').textContent})`);
    assert.equal(compared.outcome,'ready');assert.equal(compared.notes,3);if(lang==='en') assert.match(compared.text,/English translation unavailable/);assert.match(compared.text,/Paul/);
    report.push({date,mode:'compare',notes:compared.notes});
  }

  const properKeys=['conversione-s-pauli-apostoli','comm-s-petri-apostoli','cathedrae-s-petri-apostoli','comm-s-pauli-apostoli','commemoratione-s-pauli-apostoli','comm-s-petri-apostoli-2'];
  for (const key of properKeys) for (const mode of ['read','missal','study']) {
    await cdp.send('Page.navigate',{url:origin+PROPERS+'?data=/src/web/data#missal=roman-1962&type=sanctoral&mass='+key+'&bible=douay-rheims&orations=la&mode='+mode+'&ordinary-lang=la'});
    await waitFor(cdp,`window.propersReaderDebug?.ready && propersReaderDebug.state?.formulary?.id==='${key}' && propersReaderDebug.state?.requestedMode==='${mode}' && document.getElementById('reader-document').getAttribute('aria-busy')==='false'`,'raw Propers '+key+' '+mode);
    const direct=await evaluate(cdp,`({outcome:propersReaderDebug.outcome,holds:document.querySelectorAll('#reader-document .inseparable-oration-context').length,groups:document.querySelectorAll('#reader-document .inseparable-oration-group').length,text:document.getElementById('reader-document').textContent,absence:propersReaderDebug.semantic?.explicitAbsences})`);
    assert.equal(direct.outcome,'ready');assert.equal(direct.holds,3);assert.equal(direct.groups,0);
    assert.match(direct.text,/does not establish Office or votive use/);
    assert.ok(direct.absence.some(a=>a.scope==='inseparable-oration-assembly'));
    report.push({key,mode,contextHolds:direct.holds,rawBodiesOnly:true});
  }
  await cdp.send('Page.navigate',{url:origin+PROPERS+'?data=/src/web/data#missal=roman-1962&type=sanctoral&mass=commemoratione-s-pauli-apostoli&bible=douay-rheims&orations=en&mode=compare&compare=oration-language&peer-orations=la'});
  await waitFor(cdp,`window.propersReaderDebug?.ready && propersReaderDebug.state?.requestedMode==='compare' && document.getElementById('reader-document').getAttribute('aria-busy')==='false'`,'raw Propers Compare');
  const rawCompare=await evaluate(cdp,`({outcome:propersReaderDebug.outcome,holds:document.querySelectorAll('#reader-document .inseparable-oration-context').length,groups:document.querySelectorAll('#reader-document .inseparable-oration-group').length,text:document.getElementById('reader-document').textContent})`);
  assert.equal(rawCompare.outcome,'ready');assert.equal(rawCompare.holds,6);assert.equal(rawCompare.groups,0);assert.match(rawCompare.text,/does not establish Office or votive use/);
  report.push({mode:'propers-compare',contextHolds:rawCompare.holds,rawBodiesOnly:true});
  assert.deepEqual(consoleProblems,[]);assert.deepEqual(failedRequests,[]);assert.deepEqual(httpProblems,[]);
  process.stdout.write(JSON.stringify({status:'pass',report,english:{notes:english.notes,explicitHold:true},consoleProblems,failedRequests,httpProblems})+'\n');
}catch(error){const state=cdp?await evaluate(cdp,`({hash:location.hash,day:window.dayReaderDebug,propers:window.propersReaderDebug})`).catch(()=>null):null;process.stderr.write(JSON.stringify({status:'fail',error:error.stack,state,assertions,consoleProblems,failedRequests,httpProblems})+'\n');process.exitCode=1;}
finally{if(cdp)cdp.close();const stopped=new Promise(done=>chrome.once('exit',done));chrome.kill('SIGTERM');await stopped;await new Promise(done=>instance.close(done));await rm(profile,{recursive:true,force:true,maxRetries:4,retryDelay:100});}
