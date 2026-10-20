#!/usr/bin/env node
/* Optional source-served Chromium proof: native hints reuse responses; split validation stays authoritative. */
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(process.env.TRIPTYCH_STARTUP_ROOT || resolve(import.meta.dirname, '../..'));
const OVERLAY = process.env.TRIPTYCH_STARTUP_OVERLAY;
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH || resolve(ROOT, '.scratch/reader-proper-startup'));
const sleep = ms => new Promise(done => setTimeout(done, ms));
const counts = new Map();
let corrupt = false;
const server = createServer(async (request, response) => {
  try {
    let relative = decodeURIComponent(new URL(request.url, 'http://localhost').pathname).replace(/^\/+/, '');
    counts.set('/'+relative, (counts.get('/'+relative) || 0)+1);
    if (relative === 'favicon.ico') { response.writeHead(204); response.end(); return; }
    if (/^src\/web\/data\/[^/]+\/chapters\//.test(relative)) {
      relative = relative.replace(/^src\/web\/data\//, 'src/sources/bibles/');
    }
    const file = resolve(ROOT, relative);
    if (!file.startsWith(ROOT+sep)) throw new Error('outside repository');
    let body;
    if (OVERLAY) {
      try { body = await readFile(resolve(OVERLAY, relative)); } catch { /* unchanged source */ }
    }
    body ??= await readFile(file);
    if (corrupt && relative.includes('/propers/mass/roman-1962/')) {
      const value = JSON.parse(body.toString());
      value.generation = '0'.repeat(64);
      body = Buffer.from(JSON.stringify(value));
    }
    const type = ({'.js':'text/javascript','.html':'text/html','.css':'text/css','.json':'application/json'})[extname(file)] || 'application/octet-stream';
    response.writeHead(200, {'content-type':type,'cache-control':'max-age=600'});
    response.end(body);
  } catch { response.writeHead(404, {'cache-control':'no-store'}); response.end(); }
});
async function listen(instance) {
  await new Promise((done,reject) => { instance.once('error',reject); instance.listen(0,'127.0.0.1',done); });
  return instance.address().port;
}
const port = await listen(server);
const probe = createServer();
const driverPort = await listen(probe);
await new Promise(done => probe.close(done));
await mkdir(SCRATCH,{recursive:true});
const profile = await mkdtemp(resolve(SCRATCH,'chromium-'));
const driver = spawn(process.env.TRIPTYCH_CHROMEDRIVER || '/usr/bin/chromedriver', [`--port=${driverPort}`], {stdio:'ignore'});
let sid;
async function request(method,path,data) {
  const response = await fetch(`http://127.0.0.1:${driverPort}${path}`,{
    method,headers:{'content-type':'application/json'},...(data ? {body:JSON.stringify(data)} : {})});
  const result = await response.json();
  if (!response.ok || result.value?.error) throw new Error(JSON.stringify(result));
  return result.value;
}
const wd = (path,data,method='POST') => request(method,`/session/${sid}${path}`,data);
const js = script => wd('/execute/sync',{script,args:[]});
const cdp = (cmd,params={}) => wd('/goog/cdp/execute',{cmd,params});
const DAY = 'date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&mode=read&ordinary=0';
const PROPERS = 'missal=roman-1962&type=sanctoral&mass=commemoratione-omnium-fidelium-defunctorum&form=first&bible=douay-rheims&orations=en&translation-witness=edition.edward-caswall.lyra-catholica.london-1849';
async function navigate(page,hash) {
  await wd('/url',{url:'about:blank'});
  await cdp('Network.clearBrowserCache');
  counts.clear();
  await wd('/url',{url:`http://127.0.0.1:${port}/src/web/browser/liturgy/${page}?data=/src/web/data#${hash}`});
  for (let attempt=0;attempt<600;attempt++) {
    const result = await js(`const d=window.dayReaderDebug||window.propersReaderDebug;
      return {ready:d?.ready,outcome:d?.outcome,title:document.querySelector('h1')?.innerText,
      hints:[...document.querySelectorAll('link[rel="preload"][as="fetch"]')].map(e=>e.href)};`);
    if (result.ready) return result;
    await sleep(50);
  }
  throw new Error('reader did not settle: '+page);
}
let checks = 0;
try {
  for (let i=0;i<120;i++) {
    try { await request('GET','/status'); break; } catch { await sleep(50); }
  }
  sid = (await request('POST','/session',{capabilities:{alwaysMatch:{browserName:'chrome',
    'goog:chromeOptions':{binary:process.env.TRIPTYCH_CHROME||'/usr/bin/chromium',args:[
      '--headless=new','--no-sandbox','--disable-dev-shm-usage',`--user-data-dir=${profile}`]}}}})).sessionId;
  await wd('/timeouts',{pageLoad:60000,script:30000});
  await cdp('Network.enable');
  for (const [page,hash,total,title] of [
    ['day.html',DAY,7,'Tenth Sunday after Pentecost'],['day-reader.html',DAY,7,'Tenth Sunday after Pentecost'],
    ['index.html',PROPERS,5,'In Commemoratione Omnium Fidelium Defunctorum'],
    ['propers-reader.html',PROPERS,5,'In Commemoratione Omnium Fidelium Defunctorum']]) {
    const result = await navigate(page,hash);
    assert.equal(result.title,title);
    assert.equal(result.hints.length,total);
    for (const url of result.hints) assert.equal(counts.get(new URL(url).pathname),1,url+' must transfer once');
    assert.equal(counts.has('/src/web/data/structure/propers/roman-1962.json'),false,
      'a valid bounded Read link retains its selected-Mass path');
    assert.equal(counts.has('/src/web/data/structure/ordinary/roman-1962.json'),false,
      'Read does not warm Ordinary text');
    checks++;
  }
  for (const [page,hash] of [
    ['day.html',DAY.replace('mode=read','mode=study')],['day.html',DAY+'&missal=postconciliar'],
    ['day.html',DAY.replace('2026-08-02','2026-02-30')],
    ['index.html',PROPERS.replace('mass=commemoratione-omnium-fidelium-defunctorum','mass=..%2Fsecret')]]) {
    assert.equal((await navigate(page,hash)).hints.length,0);
    checks++;
  }
  corrupt = true;
  const fallback = await navigate('index.html',PROPERS);
  assert.equal(fallback.title,'In Commemoratione Omnium Fidelium Defunctorum');
  assert.equal(fallback.outcome,'ready');
  assert.equal(counts.get('/src/web/data/structure/propers/roman-1962.json'),1,
    'a hinted Mass with a bad generation must use the validated monolith fallback');
  checks++;
  process.stdout.write(JSON.stringify({status:'pass',checks})+'\n');
} finally {
  if (sid) await request('DELETE',`/session/${sid}`).catch(()=>{});
  driver.kill('SIGTERM');
  await new Promise(done => driver.once('exit',done));
  await new Promise(done => server.close(done));
  await rm(profile,{recursive:true,force:true,maxRetries:5,retryDelay:100});
}
