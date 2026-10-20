#!/usr/bin/env node

/* Source-served native clipboard and accessibility checks for divided Ordinary rows. */
import assert from 'node:assert/strict';
import { spawn, spawnSync } from 'node:child_process';
import { createServer } from 'node:http';
import { access, mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const OVERLAY = process.env.TRIPTYCH_DIALOGUE_OVERLAY ? resolve(process.env.TRIPTYCH_DIALOGUE_OVERLAY) : null;
const CHROME = process.env.TRIPTYCH_CHROME || '/usr/bin/chromium';
const SCRATCH = resolve(process.env.TRIPTYCH_BROWSER_SCRATCH || resolve(ROOT, '.scratch/reader-dialogue'));
const KEYS = ['praeparatio/deus-tu-conversus', 'praeparatio/ostende-nobis',
  'praeparatio/domine-exaudi', 'praeparatio/dominus-vobiscum',
  'praeparatio/misereatur-tui', 'praeparatio/misereatur-vestri', 'praeparatio/indulgentiam',
  'praeparatio/kyrie-eleison', 'praeparatio/christe-eleison', 'praeparatio/kyrie-eleison-repetitio',
  'praeparatio/dominus-vobiscum-post-gloriam', 'oblatio/dominus-vobiscum-ante-evangelium',
  'oblatio/dominus-vobiscum-ante-offertorium', 'conclusio/dominus-vobiscum-ante-postcommunionem',
  'canon/per-omnia-saecula', 'communio/pater-noster', 'communio/per-omnia-saecula-post-libera-nos',
  'conclusio/requiescant-in-pace', 'conclusio/initium-sancti-evangelii'];
const GOSPEL_PRAYERS = ['oblatio/munda-cor-meum', 'oblatio/dominus-sit-in-corde-meo',
  'oblatio/per-evangelica-dicta'];
const MAME = 'edition.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam';
const CUMMISKEY = 'edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861';
const KYRIE = KEYS.filter(key => /(?:kyrie|christe)-eleison/.test(key));
const clean = value => value.replace(/\s+/g, ' ').trim();
const eventSelector = key => `[data-semantic-event-id="ordinary-element/${key}"]`;
const assertions = [], failures = [], consoleProblems = [], failedRequests = [], httpProblems = [];
const clipboard = [], accessibility = [], pdfs = [];

async function source(path) {
  if (OVERLAY) {
    const file = resolve(OVERLAY, path);
    if (file.startsWith(OVERLAY + sep)) {
      try { await access(file); return readFile(file); } catch (_error) { /* sparse overlay */ }
    }
  }
  const file = resolve(ROOT, path);
  if (!file.startsWith(ROOT + sep)) throw new Error('outside root');
  return readFile(file);
}
function server() {
  return createServer(async (request, response) => {
    try {
      let path = decodeURIComponent(new URL(request.url, 'http://localhost').pathname).replace(/^\/+/, '');
      if (path === 'favicon.ico') { response.writeHead(204); response.end(); return; }
      if (/^src\/web\/data\/[^/]+\/chapters\//.test(path)) path = path.replace(/^src\/web\/data\//, 'src/sources/bibles/');
      const mime = ({'.css':'text/css', '.html':'text/html', '.js':'text/javascript', '.json':'application/json'})[extname(path)] || 'application/octet-stream';
      const body = await source(path);
      response.writeHead(200, {'content-type':mime, 'cache-control':'no-store'}); response.end(body);
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

async function waitJson(url) {
  for (let i = 0; i < 120; i += 1) {
    try { const response = await fetch(url); if (response.ok) return response.json(); }
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
  }
  async ready() {
    await new Promise((done, reject) => {
      this.socket.addEventListener('open', done, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (!message.id) return;
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
      const timer = setTimeout(() => reject(new Error('CDP timeout: ' + method)), 30000);
      this.pending.set(id, { resolve, reject, timer });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }
  close() { this.socket.close(); }
}

async function evaluate(cdp, expression) {
  const result = await cdp.send('Runtime.evaluate', {
    expression, awaitPromise: true, returnByValue: true, userGesture: true
  });
  if (result.exceptionDetails) throw new Error(
    result.exceptionDetails.exception?.description || result.exceptionDetails.text
  );
  return result.result.value;
}

async function waitFor(cdp, expression, label) {
  for (let i = 0; i < 240; i += 1) {
    if (await evaluate(cdp, `Boolean(${expression})`)) return;
    await new Promise((done) => setTimeout(done, 50));
  }
  throw new Error('Timed out waiting for ' + label);
}


async function check(name, run) {
  try { await run(); assertions.push({name,status:'pass'}); }
  catch (error) { assertions.push({name,status:'fail'}); failures.push({name,error:String(error.stack || error)}); }
}
async function viewport(cdp, width, height = 852, scale = 1) {
  await cdp.send('Emulation.setDeviceMetricsOverride', {width,height,deviceScaleFactor:1,
    mobile:width < 768,screenWidth:width,screenHeight:height});
  await cdp.send('Emulation.setPageScaleFactor', {pageScaleFactor:scale});
}
function route(entrance, lang, {requiem=false,rubrics=true,location=null,textDisplay=null} = {}) {
  const params = new URLSearchParams({missal:'roman-1962', bible:'douay-rheims', orations:'la',
    mode:'missal','ordinary-lang':lang,
    mass:requiem ? 'commemoratione-omnium-fidelium-defunctorum' : entrance === 'day' ? 'pentecost-10':'pentecost'});
  if (entrance === 'day') {
    params.set('date',requiem ? '2026-11-02':'2026-08-02');
    params.set('ordinary','1');params.set('rubrics',rubrics ? '1':'0');
  }
  else params.set('type',requiem ? 'sanctoral':'seasonal');
  if (requiem) params.set('form','first');
  if (location) params.set('location',location);
  if (textDisplay) params.set('text-display',textDisplay);
  return '/src/web/browser/liturgy/' + (entrance === 'day' ? 'day.html':'index.html') + '?data=/src/web/data#' + params;
}
async function visit(cdp, base, entrance, lang, options={}) {
  const destination=route(entrance,lang,options);
  const requested=new URLSearchParams(destination.split('#')[1]);
  await cdp.send('Page.navigate',{url:base+destination});
  await waitFor(cdp, `window.${entrance}ReaderReady === true && window.${entrance}ReaderDebug?.state &&
    window.${entrance}ReaderDebug?.state.requestedMode === 'missal' &&
    window.${entrance}ReaderDebug.state.languages.ordinary === ${JSON.stringify(lang)} &&
    (window.${entrance}ReaderDebug.state.textDisplay || 'selected') === ${JSON.stringify(options.textDisplay || 'selected')} &&
    ${entrance === 'day' ? `window.dayReaderDebug.state.apparatus?.rubrics === ${requested.get('rubrics') === '1'}` : 'true'} &&
    ${entrance === 'day'
      ? `window.dayReaderDebug.state.civilDate === ${JSON.stringify(requested.get('date'))} &&
         window.dayReaderDebug.state.selectedReadableFormulary?.id === ${JSON.stringify(requested.get('mass'))}`
      : `window.propersReaderDebug.state.formulary?.id === ${JSON.stringify(requested.get('mass'))}`} &&
    (window.${entrance}ReaderDebug.state.form || null) === ${JSON.stringify(requested.get('form'))} &&
    document.getElementById('reader-document').getAttribute('aria-busy') === 'false' &&
    document.querySelector('#reader-document [data-semantic-event-id]')`, entrance+' '+lang+' ready');
  return evaluate(cdp, `({outcome:${entrance}ReaderDebug.outcome,error:${entrance}ReaderDebug.error,
    events:${entrance}ReaderDebug.semantic?.events?.map(row=>row.id) || null,hash:location.hash})`);
}
const data = JSON.parse(await source('src/web/data/structure/ordinary/roman-1962.json'));
const elements = new Map(data.sections.flatMap(section=>section.elements.map(element=>[element.key,element])));
const turns = (key,lang) => {
  const held = elements.get(key)?.translations.find(row=>row.lang===lang);
  assert.ok(held?.turns?.length,key+' '+lang+' source turns');
  assert.equal(held.turns.map(row=>row.text).join('\n'),held.text,key+' exact generated source-row stream');
  return held.turns;
};
function cue(turn) {
  const speaker = {priest:'Priest',server:'Server',all:'All'}[turn.speaker];
  const role = {versicle:'Versicle',response:'Response'}[turn.dialogue_role];
  return {label: role && speaker ? role+' — '+speaker : role || speaker,
    glyph: {versicle:'℣',response:'℟'}[turn.dialogue_role] || {priest:'P',server:'S',all:'All'}[turn.speaker]};
}
function words(turn) {
  return turn.printed_marker ? turn.text.slice(turn.printed_marker.length+1) : turn.text;
}
async function observedRows(cdp,key) {
  return evaluate(cdp, `(() => {
    const event=document.querySelector(${JSON.stringify(eventSelector(key))});
    if (!event) return null;
    return [...event.querySelectorAll('.ordinary-turn')].map((row,index)=>{
      row.dataset.dialogueProbe=String(index);
      const text=row.querySelector('.ordinary-turn-text'), cue=row.querySelector('.ordinary-turn-cue');
      return {text:text?.textContent,lang:text?.lang,speaker:row.dataset.speaker||null,
        dialogueRole:row.dataset.dialogueRole||null,marker:row.dataset.printedMarker||null,
        action:row.dataset.action||null,gloss:row.dataset.gloss||null,role:row.getAttribute('role'),
        name:row.getAttribute('aria-label'),labels:[...row.querySelectorAll('.speaker-tag .visually-hidden')].map(node=>node.textContent),
        glyphs:[...row.querySelectorAll('.cue-mark')].map(node=>getComputedStyle(node,'::before').content.replace(/^"|"$/g,'')),
        decorative:[...row.querySelectorAll('.cue-mark')].map(node=>node.getAttribute('aria-hidden')),
        cueLanguage:cue?.lang||null,italic:getComputedStyle(text).fontStyle,
        destinations:row.matches('[data-semantic-event-id],[data-semantic-location],[data-reader-location]') ||
          Boolean(row.querySelector('[data-semantic-event-id],[data-semantic-location],[data-reader-location],button,a')),
        visible:getComputedStyle(row).display !== 'none',
        overflow:row.scrollWidth > row.clientWidth+1 || text.scrollWidth > text.clientWidth+1};
    });
  })()`);
}
async function verifyRows(cdp,entrance,lang) {
  let count=0;
  for (const key of KEYS) {
    const rows=await observedRows(cdp,key);
    if (key==='conclusio/requiescant-in-pace' && !rows) continue;
    assert.ok(rows,key+' rendered');
    const expected=turns(key,lang);
    assert.equal(rows.length,expected.length,key+' row count');
    rows.forEach((row,index)=>{
      const turn=expected[index], where=entrance+' '+lang+' '+key+' '+index;
      assert.equal(row.text,words(turn),where+' exact body');
      assert.equal(row.lang,lang,where+' body language');
      assert.equal(row.speaker,turn.speaker||null,where+' source speaker');
      assert.equal(row.dialogueRole,turn.dialogue_role||null,where+' target role');
      assert.equal(row.marker,turn.printed_marker||null,where+' source marker separated');
      assert.equal((row.marker ? row.marker+' ':'')+row.text,turn.text,where+' source marker reconstructed');
      assert.equal(row.destinations,false,where+' no turn destination');
      assert.equal(row.overflow,false,where+' row reflows');
      if (turn.gloss) {
        assert.deepEqual([row.labels,row.glyphs,row.decorative],[[],[],[]],where+' no gloss cue');
        assert.deepEqual([row.gloss,row.role,row.name,row.action],['true','note','Source translation',null]);
        assert.equal(row.italic,'italic',where+' italic source note');
        assert.equal(row.visible,true,where+' visible source note');
      } else {
        const expectedCue=cue(turn);
        assert.deepEqual(row.labels,[expectedCue.label],where+' one understandable label');
        assert.deepEqual(row.glyphs,[expectedCue.glyph],where+' one visible cue');
        assert.deepEqual(row.decorative,['true'],where+' decorative glyph');
        assert.equal(row.cueLanguage,'en',where+' label language');
      }
      count++;
    });
  }
  const semantic=await evaluate(cdp, `(() => ({ids:[...document.querySelectorAll('#reader-document [data-semantic-event-id]')].map(node=>node.dataset.semanticEventId),
    glosses:document.querySelectorAll('[data-gloss="true"]').length,
    qualification:document.querySelector('#reader-document').innerText,
    crossed:[...document.querySelectorAll('${eventSelector('praeparatio/misereatur-tui')} .ordinary-turn')].map(row=>[row.dataset.speaker,row.dataset.dialogueRole||null])}))()`);
  assert.equal(new Set(semantic.ids).size,semantic.ids.length,'unique semantic event identities');
  assert.deepEqual(semantic.crossed,[['server',null],['priest',null]],'crossed Misereatur retains server then priest without target roles');
  assert.equal(semantic.glosses,lang==='en'?3:0,'language-local gloss count');
  assert.ok(clean(semantic.qualification).includes(clean(data.advisory)),'exact source/target advisory remains visible');
  for (const witness of data.translations) {
    assert.ok(clean(semantic.qualification).includes(clean(witness.label)),'source witness label remains visible');
    if (witness.caution) assert.ok(clean(semantic.qualification).includes(clean(witness.caution)),'exact witness qualification remains visible');
  }
  for (const key of KYRIE) assert.ok(turns(key,lang).every(turn=>!turn.dialogue_role),'Kyrie gains no target role');
  const pater=turns('communio/pater-noster',lang);
  assert.equal(pater.at(-1).speaker,'priest');assert.equal(pater.at(-1).dialogue_role,null,'priest Amen remains unmarked');
  assert.equal(turns('oblatio/dominus-vobiscum-ante-evangelium',lang)[2].dialogue_role,null,'Gospel announcement stays unmarked');
  assert.equal(turns('conclusio/initium-sancti-evangelii',lang)[2].dialogue_role,null,'Last Gospel cross is not a versicle');
  const sourceOnly=elements.get('conclusio/dominus-vobiscum-ante-postcommunionem').translations.find(row=>row.lang===lang);
  assert.equal(sourceOnly.collation,'uncollated');
  assert.equal(sourceOnly.target_wording,undefined,'source-only Postcommunion gains no target wording');
  assert.ok(sourceOnly.turns.every(turn=>!turn.dialogue_role),'source-only Postcommunion gains no target dialogue role');
  return {count,ids:semantic.ids};
}
async function axRows(cdp,key,lang=null) {
  const {nodes}=await cdp.send('Accessibility.getFullAXTree');
  const byId=new Map(nodes.map(node=>[node.nodeId,node]));
  const {root}=await cdp.send('DOM.getDocument',{depth:0});
  const rows=await observedRows(cdp,key), result=[];
  for (let index=0;index<rows.length;index++) {
    if (lang && rows[index].lang!==lang) continue;
    const {nodeId}=await cdp.send('DOM.querySelector',{nodeId:root.nodeId,
      selector:eventSelector(key)+` [data-dialogue-probe="${index}"]`});
    const {node}=await cdp.send('DOM.describeNode',{nodeId});
    const start=nodes.find(one=>one.backendDOMNodeId===node.backendNodeId);
    assert.ok(start,key+' '+index+' exposed AX node');
    const text=[];
    (function walk(one){
      if (!one.ignored && one.role?.value==='StaticText') {text.push(one.name?.value||'');return;}
      for(const id of one.childIds||[]) if(byId.has(id)) walk(byId.get(id));
    })(start);
    result.push({role:start.role?.value,name:start.name?.value,text});
  }
  return result;
}
async function verifyAX(cdp,entrance,lang,keys=[...KYRIE,'praeparatio/misereatur-tui','praeparatio/misereatur-vestri','communio/pater-noster']) {
  for(const key of keys) {
    const actual=await axRows(cdp,key,lang),expected=turns(key,lang);
    assert.equal(actual.length,expected.length,key+' '+lang+' exact AX row count');
    actual.forEach((row,index)=>{
      const turn=expected[index];
      assert.deepEqual(row.text,turn.gloss?[turn.text]:[cue(turn).label,words(turn)],key+' AX label plus exact body');
      if(turn.gloss) assert.deepEqual([row.role,row.name],['note','Source translation'],key+' named note with body');
      assert.doesNotMatch(row.text.join(' '),/[℣℟]/,key+' decorative glyph is silent');
    });
    accessibility.push({entrance,lang,key,rows:actual});
  }
}
async function verifyCopy(cdp,entrance,lang,keys=[...KYRIE,'praeparatio/misereatur-tui']) {
  await cdp.send('Page.bringToFront');
  await cdp.send('Emulation.setFocusEmulationEnabled',{enabled:true});
  for(const key of keys) {
    const copied=await evaluate(cdp, `(async()=>{
      const event=document.querySelector(${JSON.stringify(eventSelector(key))});
      event.scrollIntoView({block:'center',behavior:'instant'});event.focus({preventScroll:true});
      const rows=event.querySelectorAll('.ordinary-turn'), selection=getSelection();
      selection.removeAllRanges();const range=document.createRange();
      range.selectNodeContents(event.querySelector('.ordinary-dialogue[lang="${lang}"]'));selection.addRange(range);
      const selected=selection.toString(),ok=document.execCommand('copy');
      await new Promise(done=>setTimeout(done,50));
      const text=await navigator.clipboard.readText();selection.removeAllRanges();
      return {ok,selected,text};
    })()`);
    clipboard.push({entrance,lang,key,...copied});
    const expected=turns(key,lang).map(turn=>turn.gloss?turn.text:cue(turn).label+' '+words(turn));
    assert.equal(copied.ok,true,key+' native copy succeeds');
    assert.equal(clean(copied.text),expected.join(' '),key+' copied cue/body and gloss exactly once');
    assert.deepEqual(copied.text.split(/\n\s*\n/).map(clean),expected,key+' preserves exact copied row boundaries');
    assert.equal(copied.text,copied.selected,key+' native clipboard preserves actual selection');
    assert.doesNotMatch(copied.text,/(?:^|\n)\s*[PR]\.\s/,key+' no duplicate source marker');
  }
}
async function verifyGospelPrayers(cdp,entrance,paired) {
  const witness=data.translations.find(row=>row.source_id===MAME);
  assert.equal(witness?.held,3,'exact additional Latin witness extent');
  assert.match(witness.caution,/priest cue is limited.*without deacon and subdeacon/);
  assert.match(witness.caution,/solemn-Mass occurrence belongs to the deacon/);
  const page=await evaluate(cdp,`document.querySelector('#reader-document').innerText`);
  assert.ok(clean(page).includes(clean(witness.label)),'Mame witness visibly identified');
  assert.ok(clean(page).includes(clean(witness.caution)),'Munda actor qualification remains visible');
  for (const key of GOSPEL_PRAYERS) {
    const element=elements.get(key),latin=element.translations.find(row=>row.lang==='la');
    const english=element.translations.find(row=>row.lang==='en');
    assert.equal(latin.source_id,MAME,key+' independent Latin source');
    assert.equal(english.source_id,CUMMISKEY,key+' original English source');
    assert.equal(latin.target_wording,'word-exact',key+' bounded collation');
    assert.ok(latin.note.includes('Cummiskey 1861 prints this existing block in English only'),key+' source-specific absence retained');
    const expected=turns(key,'la');assert.equal(expected.length,1,key+' one Latin priest turn');
    assert.deepEqual([expected[0].speaker,expected[0].dialogue_role,expected[0].printed_marker],['priest',null,null]);
    const rows=await observedRows(cdp,key),actual=rows.filter(row=>row.lang==='la');
    assert.equal(actual.length,1,key+' exact rendered Latin extent');
    const row=actual[0];
    assert.equal(row.text,latin.text,key+' exact source body');
    assert.deepEqual([row.speaker,row.dialogueRole,row.marker],['priest',null,null],key+' source actor without inferred role or marker');
    assert.deepEqual([row.labels,row.glyphs,row.decorative],[['Priest'],['P'],['true']],key+' one priest cue');
    assert.equal(row.cueLanguage,'en');assert.equal(row.visible,true);assert.equal(row.overflow,false);
    const facts=await evaluate(cdp,`(() => {
      const event=document.querySelector(${JSON.stringify(eventSelector(key))});
      const semantic=${entrance}ReaderDebug.semantic.events.find(row=>row.id===${JSON.stringify('ordinary-element/'+key)});
      return {source:semantic?.selected?.sourceId,
        headings:[...event.querySelectorAll('.proper-name,.ordinary-head')].map(node=>node.textContent.trim()),
        sides:[...event.querySelectorAll('.text-pair > .text-side')].map(side=>({
          lang:side.dataset.textLanguage,source:side.dataset.textSourceId,rights:side.dataset.textRights,
          label:side.querySelector('.text-side-label')?.textContent,
          credit:side.querySelector(':scope > .composed-note')?.textContent}))};
    })()`);
    assert.ok(!facts.headings.includes('All'),key+' no inherited All heading');
    if (paired) {
      assert.deepEqual(facts.sides.map(side=>[side.lang,side.source,side.rights]),[['la',MAME,'public-domain'],['en',CUMMISKEY,'public-domain']],key+' independently attributed language sides');
      assert.ok(facts.sides[0].credit.includes(witness.label),key+' Latin source credit');
    } else {
      assert.equal(facts.source,MAME,key+' selected Latin semantic source');
      assert.deepEqual(rows.map(row=>row.lang),['la'],key+' selected Latin only');
    }
    if (key==='oblatio/per-evangelica-dicta') {
      assert.equal(element.speaker,'all','Cummiskey base actor remains all');
      assert.equal(english.turns.length,1,'one source-supported English turn');
      assert.deepEqual([english.turns[0].speaker,english.turns[0].dialogue_role,english.turns[0].printed_marker],['all',null,null]);
      assert.doesNotMatch(latin.text,/Amen/,'no added Per evangelica Amen');
      if (paired) {
        assert.deepEqual(rows.map(one=>[one.lang,one.speaker,one.labels,one.glyphs]),[
          ['la','priest',['Priest'],['P']],['en','all',['All'],['All']]],'Latin Priest and English All remain independent');
        assert.equal(rows[1].text,english.text,'exact unchanged English body');
        assert.equal(rows[1].dialogueRole,null);assert.equal(rows[1].marker,null);
      }
    }
  }
  const layout=await reflow(cdp);assert.equal(layout.page,true);assert.equal(layout.rows,true);
}
async function capture(cdp,name) {
  await evaluate(cdp,`document.querySelector('${eventSelector('praeparatio/kyrie-eleison')}').scrollIntoView({block:'center',behavior:'instant'})`);
  const image=await cdp.send('Page.captureScreenshot',{format:'png'});
  await writeFile(resolve(SCRATCH,name+'.png'),Buffer.from(image.data,'base64'));
}
async function reflow(cdp) {
  return evaluate(cdp, `(() => ({page:document.documentElement.scrollWidth<=innerWidth+1,
    rows:[...document.querySelectorAll('.ordinary-turn')].filter(row=>row.getClientRects().length)
      .every(row=>row.scrollWidth<=row.clientWidth+1 && row.querySelector('.ordinary-turn-text').scrollWidth<=row.querySelector('.ordinary-turn-text').clientWidth+1),
    glosses:[...document.querySelectorAll('[data-gloss]')].map(row=>({visible:getComputedStyle(row).display!=='none',
      italic:getComputedStyle(row.querySelector('.ordinary-turn-text')).fontStyle}))}))()`);
}

const instance=server();const port=await listen(instance);const base=`http://127.0.0.1:${port}`;
const reserve=server();const debugPort=await listen(reserve);await new Promise(done=>reserve.close(done));
await mkdir(SCRATCH,{recursive:true});const profile=await mkdtemp(resolve(SCRATCH,'chromium-'));
const chrome=spawn(CHROME,['--headless=new','--disable-gpu','--no-sandbox','--disable-dev-shm-usage',
  '--disable-background-networking','--disable-sync','--no-first-run',
  `--remote-debugging-port=${debugPort}`,`--user-data-dir=${profile}`,'about:blank'],{stdio:'ignore'});
let cdp;
try {
  const targets=await waitJson(`http://127.0.0.1:${debugPort}/json`);
  cdp=new CDP(targets.find(row=>row.type==='page').webSocketDebuggerUrl);await cdp.ready();
  cdp.socket.addEventListener('message',event=>{
    const message=JSON.parse(event.data),p=message.params||{};
    if(message.method==='Runtime.consoleAPICalled' && p.type==='error') consoleProblems.push(p.args.map(row=>row.value||row.description||'').join(' '));
    if(message.method==='Runtime.exceptionThrown') consoleProblems.push(p.exceptionDetails.exception?.description||p.exceptionDetails.text);
    if(message.method==='Network.loadingFailed') failedRequests.push({error:p.errorText,canceled:Boolean(p.canceled)});
    if(message.method==='Network.responseReceived' && p.response.status>=400) httpProblems.push({status:p.response.status,path:new URL(p.response.url).pathname});
  });
  await Promise.all([cdp.send('Page.enable'),cdp.send('Runtime.enable'),cdp.send('Network.enable'),cdp.send('Accessibility.enable')]);
  await cdp.send('Browser.grantPermissions',{origin:base,permissions:['clipboardReadWrite','clipboardSanitizedWrite']});
  await cdp.send('Emulation.setFocusEmulationEnabled',{enabled:true});
  for(const entrance of ['day','propers']) for(const lang of ['en','la']) {
    for(const width of [1440,393,320]) {
      await viewport(cdp,width,width===1440?900:852);
      await check(`${entrance}-${lang}-${width}-source-turns`,async()=>{
        const loaded=await visit(cdp,base,entrance,lang);
        assert.ok(['ready','unresolved'].includes(loaded.outcome),JSON.stringify(loaded));
        const actual=await verifyRows(cdp,entrance,lang);
        if(loaded.events) assert.deepEqual(actual.ids,loaded.events,'DOM preserves the semantic event stream');
        if(entrance==='day') assert.equal(actual.ids.length,178,'Pentecost X retains its 178 semantic events');
        if(lang==='en' && width!==1440) await capture(cdp,`${entrance}-${width}-kyrie`);
      });
      if(width===393) {
        await check(`${entrance}-${lang}-real-accessibility-tree`,()=>verifyAX(cdp,entrance,lang));
        await check(`${entrance}-${lang}-native-copy`,()=>verifyCopy(cdp,entrance,lang));
        await check(`${entrance}-${lang}-print`,async()=>{
          try {
            await cdp.send('Emulation.setEmulatedMedia',{media:'print'});
            const layout=await reflow(cdp);assert.equal(layout.rows,true,'printed rows reflow');
            assert.deepEqual(layout.glosses,lang==='en'?Array(3).fill({visible:true,italic:'italic'}):[]);
            if(lang==='en') {
              const printed=await cdp.send('Page.printToPDF',{printBackground:true,preferCSSPageSize:true,displayHeaderFooter:false});
              const path=resolve(SCRATCH,`${entrance}-dialogue.pdf`);await writeFile(path,Buffer.from(printed.data,'base64'));
              const extracted=spawnSync('pdftotext',['-layout',path,'-'],{encoding:'utf8'});
              assert.equal(extracted.status,0,extracted.stderr);
              const text=clean(extracted.stdout);
              assert.equal(text.split('Lord, have mercy upon us.').length-1,2,'two exact Lord glosses in PDF');
              assert.equal(text.split('Christ, have mercy upon us.').length-1,1,'one exact Christ gloss in PDF');
              const pages=extracted.stdout.split('\f');
              for(const gloss of ['Lord, have mercy upon us.','Christ, have mercy upon us.']) {
                for(const page of pages.filter(page=>clean(page).includes(gloss)))
                  assert.match(page,/Kyrie eleison|Christe eleison/,'gloss page retains an acclamation');
              }
              pdfs.push({entrance,pages:pages.filter(page=>page.trim()).length,glosses:3});
              await writeFile(resolve(SCRATCH,`${entrance}-dialogue-pdf.txt`),extracted.stdout);
            }
          } finally {await cdp.send('Emulation.setEmulatedMedia',{media:'screen'});}
        });
      }
    }
    await check(`${entrance}-${lang}-requiem-condition`,async()=>{
      await visit(cdp,base,entrance,lang,{requiem:true});
      const actual=await observedRows(cdp,'conclusio/requiescant-in-pace');
      assert.ok(actual,'source-supported All Souls renders Requiescant');
      assert.deepEqual(actual.map(row=>[row.labels,row.glyphs]),[
        [['Versicle — Priest'],['℣']],[['Response — Server'],['℟']]]);
      assert.deepEqual(actual.map(row=>(row.marker?row.marker+' ':'')+row.text),turns('conclusio/requiescant-in-pace',lang).map(row=>row.text));
    });
  }
  for(const entrance of ['day','propers']) {
    for(const paired of [false,true]) for(const width of [1440,393]) {
      await check(`${entrance}-gospel-prayers-${paired?'paired':'latin'}-${width}`,async()=>{
        await viewport(cdp,width,width===1440?900:852);
        await visit(cdp,base,entrance,paired?'en':'la',{
          textDisplay:paired?'latin-and-selected':null,rubrics:width===1440});
        await verifyGospelPrayers(cdp,entrance,paired);
        if(width===393) {
          await verifyAX(cdp,entrance,'la',GOSPEL_PRAYERS);
          await verifyCopy(cdp,entrance,'la',GOSPEL_PRAYERS);
          if(paired) {
            await verifyAX(cdp,entrance,'en',['oblatio/per-evangelica-dicta']);
            await verifyCopy(cdp,entrance,'en',['oblatio/per-evangelica-dicta']);
          }
        }
      });
    }
    await viewport(cdp,393,852);
    await check(`${entrance}-semantic-location-and-focus`,async()=>{
      await visit(cdp,base,entrance,'en');
      const event='ordinary-element/praeparatio/kyrie-eleison';
      const key=entrance==='day'?'ordinary-section/praeparatio':event;
      await evaluate(cdp,`document.querySelector('[data-reader-action="contents"]').click()`);
      const target=await evaluate(cdp,`Boolean(document.querySelector('[data-reader-contents] [data-reader-location="${key}"]'))`);
      assert.equal(target,true,'existing parent Contents destination remains available');
      await evaluate(cdp,`document.querySelector('[data-reader-contents] [data-reader-location="${key}"]').click()`);
      const jumped=await evaluate(cdp,`({focus:document.activeElement.dataset.semanticEventId,
        location:new URLSearchParams(location.hash.slice(1)).get('location')})`);
      assert.equal(jumped.focus,key,'Contents restores semantic focus');
      assert.equal(jumped.location,key,'Contents writes semantic location');
      const loaded=await visit(cdp,base,entrance,'en',{location:event});
      assert.equal(new URLSearchParams(loaded.hash.slice(1)).get('location'),event);
      await waitFor(cdp,`(()=>{const row=document.querySelector('[data-semantic-event-id="${event}"]');
        return row.getBoundingClientRect().bottom>0 && row.getBoundingClientRect().top<innerHeight;})()`,'deep-linked Kyrie parent is visible');
      assert.equal(await evaluate(cdp,`document.querySelectorAll('[data-gloss] [data-reader-location], [data-gloss][data-semantic-location]').length`),0);
    });
    await check(`${entrance}-${entrance==='day'?'rubrics-hidden':'source-notes'}-200-percent-text`,async()=>{
      await visit(cdp,base,entrance,'en',{rubrics:false});
      await evaluate(cdp,`document.documentElement.style.fontSize='200%'`);
      const actual=await reflow(cdp);assert.equal(actual.page,true);assert.equal(actual.rows,true);
      assert.deepEqual(actual.glosses,Array(3).fill({visible:true,italic:'italic'}));
      await verifyCopy(cdp,entrance,'en');
      await capture(cdp,`${entrance}-200-percent-kyrie`);
      await evaluate(cdp,`document.documentElement.style.fontSize=''`);
    });
    await check(`${entrance}-400-percent-equivalent-reflow`,async()=>{
      // The 320×225 CSS viewport is equivalent to 1280×900 at 400% browser
      // zoom. Pinch magnification would shrink the visual viewport again and
      // would exercise a different case, so keep visual scale at one.
      await viewport(cdp,320,225,1);await visit(cdp,base,entrance,'en');
      const actual=await reflow(cdp);assert.equal(actual.page,true);assert.equal(actual.rows,true);
      assert.deepEqual(actual.glosses,Array(3).fill({visible:true,italic:'italic'}));
      const reachable=await evaluate(cdp,`(()=>{
        const rows=[...document.querySelectorAll('${eventSelector('praeparatio/kyrie-eleison')} .ordinary-turn')];
        return rows.every(row=>{row.scrollIntoView({block:'center',behavior:'instant'});
          const box=row.getBoundingClientRect(),top=document.querySelector('.reader-masthead').getBoundingClientRect().bottom,
            bottom=document.querySelector('.reader-actions').getBoundingClientRect().top;
          return box.top>=top-1 && box.bottom<=bottom+1;});
      })()`);
      assert.equal(reachable,true,'each short spoken row and gloss can be read between fixed controls');
      await capture(cdp,`${entrance}-400-percent-equivalent-kyrie`);
      await viewport(cdp,393,852,1);
    });
    await check(`${entrance}-forced-colors-cues-and-notes`,async()=>{
      await cdp.send('Emulation.setEmulatedMedia',{features:[{name:'forced-colors',value:'active'}]});
      try {
        assert.equal(await evaluate(cdp,`matchMedia('(forced-colors: active)').matches`),true);
        await verifyRows(cdp,entrance,'en');
        await capture(cdp,`${entrance}-forced-colors-kyrie`);
        const actual=await reflow(cdp);assert.equal(actual.page,true);assert.equal(actual.rows,true);
      } finally {await cdp.send('Emulation.setEmulatedMedia',{features:[]});}
    });
  }
} catch(error) {failures.push({name:'harness',error:String(error.stack||error)});}
finally {
  if(cdp) {await cdp.send('Browser.resetPermissions',{}).catch(()=>{});cdp.close();}
  const exited=new Promise(done=>chrome.once('exit',done));chrome.kill('SIGTERM');
  await Promise.race([exited,new Promise(done=>setTimeout(done,2000))]);
  await new Promise(done=>instance.close(done));await rm(profile,{recursive:true,force:true,maxRetries:5,retryDelay:100});
}
const report={status:failures.length||consoleProblems.length||failedRequests.length||httpProblems.length?'fail':'pass',
  checks:assertions.length,assertions,failures,consoleProblems,failedRequests,httpProblems,expectedHttpProblems:[],
  clipboard,accessibility,pdfs,acceptance:{realAccessibilityTree:accessibility.length===38,nativeClipboard:clipboard.length===38,
    screenReader:false,manualPrintReview:false,literalBrowserZoom:false,
    reason:'Real AX, native copy, CSS viewport equivalence and automated PDF checks were run; assistive technology, literal desktop zoom and complete human print review were not run.'}};
await writeFile(resolve(SCRATCH,'dialogue-evidence.json'),JSON.stringify(report,null,2)+'\n');
process.stdout.write(JSON.stringify(report)+'\n');if(report.status!=='pass') process.exitCode=1;
