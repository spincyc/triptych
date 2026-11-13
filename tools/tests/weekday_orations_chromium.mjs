#!/usr/bin/env node
import { repositoryPath } from './_product_data.cjs';

/* Source-served, real-browser checks for the explicit weekday prayer selection. */

import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';
import process from 'node:process';

const ROOT = resolve(import.meta.dirname, '../..');
const DATA = '/src/web/data';
const DAY = '/src/web/browser/liturgy/day.html';
const PROPERS = '/src/web/browser/liturgy/index.html';
const PREFERENCES_KEY = 'triptych:liturgy:preferences:v1';
const LEGACY_KEY = 'triptych:liturgy:propers';
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH ||
  resolve(ROOT, '.scratch/reader-audit/browser'));

function mime(file) {
  return ({
    '.css': 'text/css; charset=utf-8', '.html': 'text/html; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8', '.json': 'application/json'
  })[extname(file)] || 'application/octet-stream';
}

function server() {
  return createServer(async (request, response) => {
    try {
      let relative = decodeURIComponent(new URL(request.url, 'http://localhost').pathname)
        .replace(/^\/+/, '');
      if (relative === 'favicon.ico') {
        response.writeHead(204); response.end(); return;
      }
      if (/^src\/web\/data\/[^/]+\/chapters\//.test(relative)) {
        relative = relative.replace(/^src\/web\/data\//, 'src/sources/bibles/');
      }
      const file = resolve(ROOT, relative || 'README.md');
      if (!file.startsWith(ROOT + sep)) throw new Error('outside root');
      const body = await readFile(repositoryPath(ROOT, file));
      response.writeHead(200, { 'content-type': mime(file), 'cache-control': 'no-store' });
      response.end(body);
    } catch (_error) {
      response.writeHead(404); response.end('not found');
    }
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
  for (let index = 0; index < 120; index += 1) {
    try {
      const reply = await fetch(url);
      if (reply.ok) return await reply.json();
    } catch (_error) { /* Chromium is starting. */ }
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
  on(name, handler) {
    this.events.set(name, [...(this.events.get(name) || []), handler]);
  }
  async ready() {
    await new Promise((done, reject) => {
      this.socket.addEventListener('open', done, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (!message.id) {
        for (const handler of this.events.get(message.method) || []) handler(message.params);
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
        this.pending.delete(id);
        reject(new Error('CDP timeout: ' + method));
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
  if (reply.exceptionDetails) {
    throw new Error(reply.exceptionDetails.exception?.description || reply.exceptionDetails.text);
  }
  return reply.result.value;
}

async function waitFor(cdp, expression, label) {
  for (let index = 0; index < 240; index += 1) {
    if (await evaluate(cdp, `Boolean(${expression})`)) return;
    await new Promise((done) => setTimeout(done, 50));
  }
  const state = await evaluate(cdp, '({outcome:window.dayReaderDebug?.outcome,error:window.dayReaderDebug?.error,hash:location.hash})');
  throw new Error('Timed out waiting for ' + label + ': ' + JSON.stringify(state));
}

let sequence = 0;
async function visit(cdp, base, path, hash = '') {
  const url = `${base}${path}?data=${DATA}&pref-test=${++sequence}${hash}`;
  await cdp.send('Page.navigate', { url });
  const ready = path === DAY ? 'window.dayReaderReady === true' :
    'window.propersReaderReady === true';
  await waitFor(cdp, `performance.getEntriesByType('navigation')[0]?.name === ${JSON.stringify(url)} && ${ready}`,
    path + ' readiness');
  return evaluate(cdp, path === DAY ? 'dayReaderDebug' : 'propersReaderDebug');
}

const instance = server();
const port = await listen(instance);
const debugPort = await freePort();
await mkdir(SCRATCH, { recursive: true });
const profile = await mkdtemp(resolve(SCRATCH, 'chromium-'));
const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage',
  `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`, 'about:blank'
], { stdio: 'ignore' });
let cdp;
let checks = 0;
const consoleProblems = [];
const failedRequests = [];
const httpProblems = [];
try {
  const pages = await waitJson(`http://127.0.0.1:${debugPort}/json`);
  cdp = new CDP(pages.find((row) => row.type === 'page').webSocketDebuggerUrl);
  await cdp.ready();
  cdp.on('Runtime.exceptionThrown', ({ exceptionDetails }) => {
    consoleProblems.push(exceptionDetails?.exception?.description ||
      exceptionDetails?.text || 'uncaught JavaScript exception');
  });
  cdp.on('Runtime.consoleAPICalled', ({ type, args }) => {
    if (type === 'error') consoleProblems.push(args.map((arg) => arg.value ||
      arg.description || '').join(' '));
  });
  cdp.on('Network.loadingFailed', ({ canceled, errorText }) => {
    if (!canceled) failedRequests.push(errorText || 'network request failed');
  });
  cdp.on('Network.responseReceived', ({ response }) => {
    if (response?.status >= 400) httpProblems.push(response.status + ' ' + response.url);
  });
  await Promise.all([
    cdp.send('Page.enable'), cdp.send('Runtime.enable'), cdp.send('Network.enable')
  ]);
  const base = `http://127.0.0.1:${port}`;
  const values = {date:'2026-01-12',missal:'postconciliar',bible:'douay-rheims',orations:'en'};
  const route = (patch={}) => '#' + new URLSearchParams({...values,...patch});
  const properEvents = () => evaluate(cdp, 'dayReaderDebug.semantic.events.filter(row=>row.kind === "proper")');
  let row = await visit(cdp, base, DAY, route());
  assert.equal(row.state.orationMass, undefined);
  const original = await properEvents();
  assert.equal(original.length, 4);
  assert.equal(await evaluate(cdp, 'document.querySelector("[name=oration-mass]").value'), '');
  assert.equal(await evaluate(cdp, 'new URLSearchParams(location.hash.slice(1)).has("oration-mass")'), false);
  assert.deepEqual(await evaluate(cdp, 'Array.from(document.querySelector("[name=oration-mass]").options).slice(1).map(row=>row.value)'),
    Array.from({length:32}, (_,index) => 'ot-' + (index+2)));
  checks++;

  await evaluate(cdp, `(() => {const select=document.querySelector('[name=oration-mass]');
    select.value='ot-2';select.dispatchEvent(new Event('change',{bubbles:true}));select.form.requestSubmit();})()`);
  await waitFor(cdp, 'dayReaderDebug.ready && dayReaderDebug.state?.orationMass === "ot-2"', 'selected prayers');
  let selected = await properEvents();
  assert.equal(selected.length, 7);
  assert.deepEqual(selected.filter(event=>event.id.includes('/ot-1-monday/')), original);
  const prayers = selected.filter(event=>event.id.includes('/ot-2/'));
  assert.deepEqual(prayers.map(event=>event.editionSlotLabel), ['Collect','Prayer over the Offerings','Prayer after Communion']);
  assert.ok(prayers.every(event=>event.sourceHooks.some(hook=>hook.id.startsWith('postconciliar/ot-2/'))));
  assert.ok(await evaluate(cdp, 'document.querySelector(".weekday-oration-choice").textContent.includes("Prayers from")'));
  assert.equal(await evaluate(cdp, 'new URLSearchParams(location.hash.slice(1)).get("oration-mass")'), 'ot-2');
  const english = prayers.filter(event=>event.selected?.text);
  assert.ok(english.length > 0, 'selected English prayer body is held');
  for (const prayer of english) assert.ok(await evaluate(cdp,
    `document.querySelector('[data-semantic-event-id="${prayer.id}"]').textContent.includes(${JSON.stringify(prayer.selected.text.slice(0,60))})`));
  checks++;

  await cdp.send('Page.reload');
  await waitFor(cdp, 'window.dayReaderReady && dayReaderDebug.state?.orationMass === "ot-2"', 'reload');
  assert.deepEqual(await properEvents(), selected);
  checks++;

  row = await visit(cdp, base, DAY, route({'oration-mass':'ot-2',mode:'missal'}));
  assert.ok(row.semantic.events.some(event=>event.kind === 'ordinary-element'));
  assert.deepEqual((await properEvents()).map(event=>event.id), selected.map(event=>event.id));
  checks++;

  row = await visit(cdp, base, DAY, route({'oration-mass':'ot-2',orations:'la'}));
  assert.ok((await properEvents()).filter(event=>event.id.includes('/ot-2/')).every(event=>event.selected.missing));
  assert.ok(await evaluate(cdp, 'document.querySelector("#reader-document").textContent.includes("unavailable")'));
  for (const width of [393,320]) {
    await cdp.send('Emulation.setDeviceMetricsOverride', {width,height:844,deviceScaleFactor:1,mobile:false});
    assert.ok(await evaluate(cdp, 'document.documentElement.scrollWidth <= innerWidth'), 'no narrow viewport overflow');
  }
  await writeFile(resolve(SCRATCH, 'weekday-320.png'), Buffer.from((await cdp.send('Page.captureScreenshot')).data, 'base64'));
  checks++;

  await evaluate(cdp, `document.querySelector('#reader-orations').value='en';
    document.querySelector('#date-form').requestSubmit()`);
  await waitFor(cdp, 'dayReaderDebug.ready && dayReaderDebug.state?.languages.orations === "en"', 'language change');
  assert.equal(await evaluate(cdp, 'dayReaderDebug.state.orationMass'), 'ot-2');
  checks++;

  await evaluate(cdp, `document.querySelector('#reader-date').value='2026-01-13';
    document.querySelector('#date-form').requestSubmit()`);
  await waitFor(cdp, 'dayReaderDebug.ready && dayReaderDebug.state?.civilDate === "2026-01-13"', 'date change');
  assert.equal(await evaluate(cdp, 'dayReaderDebug.state.orationMass'), undefined);
  assert.equal(await evaluate(cdp, 'new URLSearchParams(location.hash.slice(1)).has("oration-mass")'), false);
  checks++;

  await visit(cdp, base, DAY, route({'oration-mass':'ot-2'}));
  await evaluate(cdp, `document.querySelector('#reader-missal').value='roman-1962';
    document.querySelector('#date-form').requestSubmit()`);
  await waitFor(cdp, 'dayReaderDebug.ready && dayReaderDebug.state?.edition.id === "roman-1962"', 'calendar change');
  assert.equal(await evaluate(cdp, 'dayReaderDebug.state.orationMass'), undefined);
  assert.equal(await evaluate(cdp, 'new URLSearchParams(location.hash.slice(1)).has("oration-mass")'), false);
  checks++;

  const qualifications = await evaluate(cdp, `(() => {
    const owner={name:'Collect',source:'composed',text:'Latine.',notes:'Historical witness; target wording remains uncollated.',
      latin:{withheld:false,publication:{status:'permitted',basis:'public-domain'},
        provenance:{status:'collated',relationship:'exact-transcription',source_date:'1879',source_id:'fixture'}}};
    return [{orations:'la'},{orations:'en'},{orations:'en',textDisplay:'latin-and-selected'}].map(options=>{
      const node=Triptych.renderProper(owner,{id:'douay-rheims'}, {}, options);
      return {qualifications:node.querySelectorAll('.latin-source-qualification').length,
        credits:node.querySelectorAll('.latin-source-credit').length,text:node.textContent};
    });
  })()`);
  assert.ok(qualifications.every(row=>row.qualifications === 1 && row.credits === 1 &&
    row.text.includes('target wording remains uncollated') && row.text.includes('1879')));
  checks++;

  row = await visit(cdp, base, DAY, route({date:'2026-06-04'}));
  await evaluate(cdp, `(() => {const select=document.querySelector('[name=oration-mass]');
    select.value='ot-2';select.dispatchEvent(new Event('change',{bubbles:true}));select.form.requestSubmit();})()`);
  await waitFor(cdp, 'dayReaderDebug.ready && dayReaderDebug.state?.orationMass === "ot-2"', 'territorial prayers');
  row = await evaluate(cdp, 'dayReaderDebug');
  assert.equal(row.state.orationTerritory, 'corpus-christi-transferred-to-sunday');
  assert.ok(!row.error?.length, JSON.stringify(row.error));
  assert.deepEqual(await evaluate(cdp, 'Array.from(document.querySelectorAll(".candidate-failure")).map(row=>row.textContent)'), []);
  assert.equal(await evaluate(cdp, 'document.querySelectorAll(".weekday-oration-choice").length'), 1);
  checks++;

  for (const patch of [ {'oration-mass':'ot-1'}, {'oration-mass':'ot-2',date:'2026-01-18'},
    {'oration-mass':'ot-2',missal:'roman-1962'}, {'oration-mass':'ot-2',mode:'compare','peer-missal':'roman-1962'} ]) {
    row = await visit(cdp, base, DAY, route(patch));
    assert.notEqual(row.outcome, 'ready', 'inapplicable explicit selection is refused');
    assert.ok(row.error?.length, JSON.stringify(row));
  }
  checks++;

  const dedicationRoute = '#' + new URLSearchParams({date:'2026-11-09',missal:'roman-1962',
    bible:'douay-rheims',orations:'la'});
  row = await visit(cdp, base, DAY, dedicationRoute);
  assert.ok(row.semantic, JSON.stringify({outcome:row.outcome,error:row.error}));
  const dedicationOriginal = await properEvents();
  assert.equal(await evaluate(cdp, 'document.querySelector("[name=dedication-location]").value'), '');
  await evaluate(cdp, `(() => {const select=document.querySelector('[name=dedication-location]');
    select.value='in-dedicated-church';select.dispatchEvent(new Event('change',{bubbles:true}));select.form.requestSubmit();})()`);
  assert.deepEqual(await properEvents(), dedicationOriginal, 'a location option alone is no attestation');
  await evaluate(cdp, `(() => {const checkbox=document.querySelector('[name=confirm-dedication-location]');
    checkbox.click();checkbox.form.requestSubmit();})()`);
  await waitFor(cdp, 'dayReaderDebug.ready && dayReaderDebug.semantic?.events.some(row=>row.id.includes("/commune-dedicationis-ecclesiae/"))', 'confirmed inside location');
  const inside = await properEvents();
  const insideSecret = inside.filter(event=>event.id.includes('/commune-dedicationis-ecclesiae/'));
  assert.equal(insideSecret.length, 1);
  assert.ok(insideSecret[0].editionSlotLabel.includes('In ecclesia ipsa dedicata'));
  assert.deepEqual(inside.filter(event=>!event.id.includes('/commune-dedicationis-ecclesiae/')), dedicationOriginal);
  await writeFile(resolve(SCRATCH, 'dedication-320.png'), Buffer.from((await cdp.send('Page.captureScreenshot')).data, 'base64'));
  assert.equal(await evaluate(cdp, 'Array.from(new URLSearchParams(location.hash.slice(1)).keys()).some(key=>key.startsWith("dedication"))'), false);
  checks++;

  for (const language of ['en','la']) {
    await evaluate(cdp, `document.querySelector('#reader-orations').value=${JSON.stringify(language)};
      document.querySelector('#date-form').requestSubmit()`);
    await waitFor(cdp, `dayReaderDebug.ready && dayReaderDebug.state?.languages.orations === ${JSON.stringify(language)}`, 'dedication language change');
    assert.equal(await evaluate(cdp, 'document.querySelector("[name=dedication-location]").value'), 'in-dedicated-church');
    assert.equal((await properEvents()).filter(event=>event.id.includes('/commune-dedicationis-ecclesiae/')).length, 1);
  }
  checks++;

  await evaluate(cdp, `(() => {const select=document.querySelector('[name=dedication-location]');
    document.querySelector('.dedication-location-choice summary').click();
    select.value='outside-dedicated-church';select.dispatchEvent(new Event('change',{bubbles:true}));
    document.querySelector('[name=confirm-dedication-location]').click();select.form.requestSubmit();})()`);
  await waitFor(cdp, 'dayReaderDebug.ready && document.querySelector(".dedication-location-choice .candidate-choice-locus")?.textContent.startsWith("Outside")', 'confirmed outside location');
  const outside = await properEvents();
  const outsideSecret = outside.filter(event=>event.id.includes('/commune-dedicationis-ecclesiae/'));
  assert.equal(outsideSecret.length, 1);
  assert.notEqual(outsideSecret[0].id, insideSecret[0].id);
  assert.deepEqual(outside.filter(event=>!event.id.includes('/commune-dedicationis-ecclesiae/')), dedicationOriginal);
  checks++;

  await cdp.send('Page.reload');
  await waitFor(cdp, 'window.dayReaderReady && document.querySelector("[name=dedication-location]")?.value === ""', 'location reconfirmation after reload');
  assert.deepEqual(await properEvents(), dedicationOriginal);
  await visit(cdp, base, DAY, dedicationRoute + '&dedication-location=outside-dedicated-church');
  assert.equal(await evaluate(cdp, 'document.querySelector("[name=dedication-location]").value'), '');
  assert.deepEqual(await properEvents(), dedicationOriginal, 'a URL does not attest the actual venue');
  checks++;

  const structure = JSON.parse(await readFile(repositoryPath(ROOT, 'src/web/data/structure/propers/postconciliar.json'), 'utf8'));
  const supper = structure.masses.find(mass=>mass.key === 'mass-of-the-lords-supper');
  const hymns = supper.propers.filter(proper=>['Hymn at the Transfer of the Blessed Sacrament',
    'Chant at the Place of Reposition'].includes(proper.name));
  assert.equal(hymns.length, 2);
  for (const display of [{orations:'la'},{orations:'en','text-display':'latin-and-selected'}]) {
    row = await visit(cdp, base, PROPERS, '#' + new URLSearchParams({missal:'postconciliar',
      type:'seasonal',mass:supper.key,bible:'douay-rheims',...display}));
    assert.equal(row.outcome, 'ready');
    for (const hymn of hymns) {
      const proof = await evaluate(cdp, `(() => {
        const note=Array.from(document.querySelectorAll('.latin-source-qualification'))
          .find(node=>node.textContent === ${JSON.stringify(hymn.latin.note)});
        return {visible:Boolean(note?.getClientRects().length && !note.closest('details:not([open])')),
          body:note?.parentElement.textContent.includes(${JSON.stringify(hymn.text.slice(0,24))}),
          credits:note?.parentElement.querySelectorAll('.latin-source-credit').length};
      })()`);
      assert.deepEqual(proof, {visible:true,body:true,credits:1});
    }
  }
  checks++;

  for (const hymn of hymns) {
    const fallback = {...hymn, translations:[]};
    const proof = await evaluate(cdp, `(() => {
      const node=Triptych.renderProper(${JSON.stringify(fallback)}, {id:'douay-rheims'}, {}, {orations:'en'});
      return {qualification:node.querySelector('.latin-source-qualification')?.textContent,
        original:node.querySelector('[data-unit-original="la"]')?.textContent,
        absence:node.querySelectorAll('[data-unit-absence]').length};
    })()`);
    assert.equal(proof.qualification, hymn.latin.note);
    assert.ok(proof.original.includes(hymn.text.slice(0,24)));
    assert.ok(proof.absence > 0);
  }
  checks++;

  const roman = JSON.parse(await readFile(repositoryPath(ROOT, 'src/web/data/structure/propers/roman-1962.json'), 'utf8'));
  const sourcePrayer = (mass,name) => roman.masses.find(row=>row.key === mass).propers.find(row=>row.name === name);
  const literal = (proper,language) => language === 'la' ? proper.text : proper.translations.find(row=>row.lang === 'en').text;
  const endingRoute = (date,language,display='selected',mass=null) => '#' + new URLSearchParams({date,missal:'roman-1962',bible:'douay-rheims',orations:language,'text-display':display,...(mass?{mass}:{})});
  for (const language of ['en','la']) {
    await visit(cdp, base, DAY, endingRoute('2026-12-06',language));
    const secret = sourcePrayer('advent-2','Secret'), index = roman.masses.find(row=>row.key==='advent-2').propers.indexOf(secret)+1;
    const proof = await evaluate(cdp, `(() => {
      const section=document.querySelector('[data-semantic-event-id="proper/roman-1962/advent-2/${String(index).padStart(3,'0')}"]');
      return {body:section.querySelector('.conclusion-execution [data-speaker="priest"]')?.textContent,
        responses:section.querySelectorAll('.conclusion-response').length,
        quotation:section.querySelector('.conclusion-source-quotation .composed')?.textContent};
    })()`);
    assert.ok(proof.body?.endsWith(secret.conclusion_execution[0].languages[language].full_conclusion));
    assert.equal(proof.responses,1);assert.equal(proof.quotation,literal(secret,language));
  }
  checks++;

  for (const language of ['en','la']) {
    row = await visit(cdp, base, DAY, endingRoute('2026-12-06',language) + '&mode=missal&ordinary=1&ordinary-lang=' + language);
    assert.ok(row.semantic.events.some(event=>event.kind==='ordinary-element'));
    const secret=(await properEvents()).find(event=>event.editionSlotLabel==='Secret');
    const expected=sourcePrayer('advent-2','Secret').conclusion_execution[0].languages[language].full_conclusion;
    assert.ok(await evaluate(cdp, `document.querySelector('[data-semantic-event-id="${secret.id}"] .conclusion-execution [data-speaker="priest"]').textContent.endsWith(${JSON.stringify(expected)})`));
    assert.equal(await evaluate(cdp, `document.querySelector('[data-semantic-event-id="${secret.id}"]').querySelectorAll('.conclusion-response').length`),1);
  }
  checks++;

  row = await visit(cdp, base, DAY, endingRoute('2026-03-27','en'));
  assert.equal(row.outcome,'unresolved');
  assert.deepEqual(await evaluate(cdp, `Array.from(document.querySelectorAll('.calendar-formulary-choice input')).map(node=>({id:node.value,checked:node.checked}))`), [
    {id:'passion-friday',checked:false},
    {id:'comm-septem-dolorum-beatae-mariae-virginis',checked:false}
  ]);
  row = await visit(cdp, base, DAY, endingRoute('2026-03-27','en','selected','s-ioannis-damasceni-confessoris-ecclesiae-doctoris'));
  assert.equal(row.outcome,'unresolved');
  assert.equal(await evaluate(cdp, 'document.querySelectorAll("[data-semantic-event-id], .calendar-formulary-choice input:checked").length'),0);
  checks++;

  for (const [language,display] of [['en','selected'],['la','selected'],['en','latin-and-selected']]) {
    row = await visit(cdp, base, DAY, endingRoute('2026-03-27',language,display,'passion-friday'));
    assert.ok(row.semantic, JSON.stringify({language,display,outcome:row.outcome,error:row.error}));
    const post = (await properEvents()).find(event=>event.editionSlotLabel==='Postcommunion');
    const proof = await evaluate(cdp, `(() => {
      const section=document.querySelector('[data-semantic-event-id="${post.id}"]');
      return {members:Array.from(section.querySelectorAll('.commemorated-oration .conclusion-execution')).map(node=>({
        language:node.lang,role:node.dataset.conclusionRole,text:node.querySelector('[data-speaker="priest"]').textContent,
        responses:node.querySelectorAll('.conclusion-response').length})),
        unresolved:section.querySelectorAll('.oration-execution-absence').length};
    })()`);
    const languages=display==='latin-and-selected'?['la','en']:[language];
    for(const lang of languages){
      const members=proof.members.filter(row=>row.language===lang);
      assert.deepEqual(members.map(row=>row.role),['petition','conclusion-provider']);
      assert.deepEqual(members.map(row=>row.responses),[0,1]);
      const first=sourcePrayer('s-ioannis-damasceni-confessoris-ecclesiae-doctoris','Postcommunion');
      const last=sourcePrayer('comm-septem-dolorum-beatae-mariae-virginis','Postcommunion');
      assert.ok(members[0].text.endsWith(literal(first,lang).slice(0,first.conclusion_execution[0].languages[lang].cue_start)));
      assert.ok(members[1].text.endsWith(last.conclusion_execution[0].languages[lang].full_conclusion));
    }
    assert.equal(proof.unresolved,0);
    if(display==='latin-and-selected') {
      await evaluate(cdp, `document.querySelector('[data-semantic-event-id="${post.id}"] .conclusion-execution').scrollIntoView({behavior:'instant',block:'start'})`);
      await evaluate(cdp, 'new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
      await writeFile(resolve(SCRATCH, 'conclusions-320.png'), Buffer.from((await cdp.send('Page.captureScreenshot')).data,'base64'));
    }
  }
  checks++;

  for(const language of ['en','la']){
    await visit(cdp,base,DAY,endingRoute('2026-01-19',language));
    const post=(await properEvents()).find(event=>event.editionSlotLabel==='Postcommunion');
    const proof=await evaluate(cdp,`(() => {const section=document.querySelector('[data-semantic-event-id="${post.id}"]');
      return {executed:section.querySelectorAll('.commemorated-oration .conclusion-execution').length,
        held:section.querySelectorAll('.oration-execution-absence').length};})()`);
    assert.equal(proof.executed,0);assert.ok(proof.held>0);
  }
  checks++;

  assert.deepEqual({consoleProblems,failedRequests,httpProblems}, {consoleProblems:[],failedRequests:[],httpProblems:[]});
  process.stdout.write(JSON.stringify({status:'pass',checks,consoleProblems,failedRequests,httpProblems})+'\n');
} finally {
  if (cdp) cdp.close();
  chrome.kill('SIGTERM');
  await new Promise((done) => chrome.once('exit', done));
  await new Promise((done) => instance.close(done));
  await rm(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 100 });
}
