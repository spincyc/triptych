#!/usr/bin/env node
/* Validated mode dependencies, independently controlled at the script boundary. */
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import vm from 'node:vm';
import test from 'node:test';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const MODULE_ROOT = resolve(process.env.TRIPTYCH_OPTIONAL_RUNTIME_MODULE_ROOT || ROOT);
function source(file) {
  const candidate = resolve(MODULE_ROOT, file);
  return readFileSync(existsSync(candidate) ? candidate : resolve(ROOT, file), 'utf8');
}
const LITURGY = 'src/web/browser/liturgy/';
const identities = {
  'day.js': ['TriptychOrdinaryRenderer', 'render'],
  'reader-comparison.js': ['LiturgyReaderComparison', 'compare'],
  'reader-compare-view.js': ['LiturgyReaderCompareView', 'render'],
  'reader-study-view.js': ['LiturgyReaderStudyView', 'attach']
};
function harness(globals = {}) {
  const scripts = [];
  const document = {
    currentScript: {src:'https://example.test/nested/liturgy/reader-optional-runtime.js'},
    createElement(tag) {
      assert.equal(tag, 'script');
      return {removed:false,remove(){this.removed=true;}};
    },
    head: {appendChild(script){scripts.push(script);}}
  };
  const context = vm.createContext({document,URL,Promise,Map,...globals});
  context.window = context;
  vm.runInContext(source(LITURGY+'reader-optional-runtime.js'), context);
  const fileOf = script => new URL(script.src).pathname.split('/').at(-1);
  function requested() { return scripts.map(fileOf); }
  function latest(file) { return scripts.findLast(script=>fileOf(script)===file&&!script.removed); }
  function finish(file, api) {
    const script = latest(file); assert.ok(script, 'a request must exist for '+file);
    const [name,method] = identities[file];
    context[name] = api || {[method](){}};
    script.onload();
  }
  return {context,scripts,requested,latest,finish,runtime:context.TriptychReaderOptionalRuntime};
}
const state = (mode,ordinary=false) => ({requestedMode:mode,options:{ordinary}});
async function stillPending(promise) {
  let complete = false; promise.then(()=>{complete=true;},()=>{complete=true;});
  await Promise.resolve(); await Promise.resolve();
  assert.equal(complete,false);
}

test('validated Read and Missal do not fetch shared mode code; Ordinary remains state-owned',async()=>{
  const held = harness();
  assert.equal(await held.runtime.forState(state('read')),null);
  assert.deepEqual(held.requested(),[]);
  const missal = held.runtime.forState(state('missal',true));
  assert.deepEqual(held.requested(),['day.js']);
  held.finish('day.js'); assert.equal(await missal,held.context.TriptychOrdinaryRenderer);
  assert.equal(await held.runtime.forState(state('read')),null);
  assert.deepEqual(held.requested(),['day.js']);
});

test('direct validated Compare awaits exactly its two shared modules without changing state',async()=>{
  const held=harness(), request=state('compare'), before=JSON.stringify(request);
  const direct=held.runtime.forState(request);
  assert.deepEqual(held.requested(),['reader-comparison.js','reader-compare-view.js']);
  for(const script of held.scripts) assert.ok(script.src.startsWith('https://example.test/nested/liturgy/'));
  held.finish('reader-compare-view.js'); await stillPending(direct);
  held.finish('reader-comparison.js'); assert.equal(await direct,null);
  assert.equal(JSON.stringify(request),before);
});

test('direct validated Study loads only apparatus without Compare or Ordinary',async()=>{
  const held=harness(), direct=held.runtime.forState(state('study'));
  assert.deepEqual(held.requested(),['reader-study-view.js']);
  await stillPending(direct); held.finish('reader-study-view.js');
  assert.equal(await direct,null);
});

test('Study and Ordinary start independently and readiness awaits both',async()=>{
  const held=harness(), direct=held.runtime.forState(state('study',true));
  assert.deepEqual(held.requested(),['day.js','reader-study-view.js']);
  held.finish('reader-study-view.js'); await stillPending(direct);
  held.finish('day.js'); assert.equal(await direct,held.context.TriptychOrdinaryRenderer);
  const reverse=harness(), other=reverse.runtime.forState(state('study',true));
  reverse.finish('day.js'); await stillPending(other);
  reverse.finish('reader-study-view.js'); await other;
});

test('concurrent mode requests deduplicate and completed modules reuse; Read does not wait for Compare',async()=>{
  const held=harness();
  const first=held.runtime.forState(state('compare'));
  const second=held.runtime.forState(state('compare'));
  assert.equal(await held.runtime.forState(state('read')),null);
  assert.deepEqual(held.requested(),['reader-comparison.js','reader-compare-view.js']);
  held.finish('reader-comparison.js'); held.finish('reader-compare-view.js');
  await Promise.all([first,second]); await held.runtime.forState(state('compare'));
  assert.equal(held.scripts.length,2);
});

test('mode network failure removes the failed script and permits retry while retaining the successful peer',async()=>{
  const held=harness(), first=held.runtime.forState(state('compare'));
  const rejected=assert.rejects(first,/reader-comparison\.js could not be loaded/);
  held.finish('reader-compare-view.js');
  const failed=held.latest('reader-comparison.js'); failed.onerror(); await rejected;
  assert.equal(failed.removed,true);
  const retried=held.runtime.forState(state('compare'));
  assert.deepEqual(held.requested(),['reader-comparison.js','reader-compare-view.js','reader-comparison.js']);
  held.finish('reader-comparison.js'); await retried;
});

test('missing or malformed mode initialization rejects precisely and retries; Ordinary errors still retry',async()=>{
  for(const value of [undefined,{attach:true}]) {
    const held=harness(), first=held.runtime.forState(state('study'));
    const rejected=assert.rejects(first,/reader-study-view\.js did not initialize/);
    if(value) held.context.LiturgyReaderStudyView=value;
    const failed=held.latest('reader-study-view.js'); failed.onload(); await rejected;
    assert.equal(failed.removed,true);
    const second=held.runtime.forState(state('study')); held.finish('reader-study-view.js'); await second;
  }
  const held=harness(), ordinary=held.runtime.loadOrdinary();
  const ordinaryRejected=assert.rejects(ordinary,/Ordinary presenter could not be loaded/);
  held.latest('day.js').onerror(); await ordinaryRejected;
  const retry=held.runtime.loadOrdinary(); held.finish('day.js'); await retry;
  assert.equal(held.requested().filter(file=>file==='day.js').length,2);
});

test('existing eager globals satisfy all modes and retain the Ordinary API without requests',async()=>{
  const globals=Object.fromEntries(Object.values(identities).map(([name,method])=>[name,{[method](){}}]));
  const held=harness(globals);
  assert.equal(await held.runtime.loadOrdinary(),globals.TriptychOrdinaryRenderer);
  await held.runtime.forState(state('compare')); await held.runtime.forState(state('study',true));
  assert.deepEqual(held.requested(),[]);
});

test('Day Compare can initialize before shared modules and build using their later-loaded APIs',async()=>{
  const held=harness();
  vm.runInContext(source(LITURGY+'day-compare.js'),held.context);
  const day=held.context.TriptychDayCompare;
  await assert.rejects(day.build({}),/semantic and view modules/);
  const ready=held.runtime.forState(state('compare'));
  let compared=null, presented=null;
  const view={schema:'synthetic-view'}, rendered={semanticIds:['compare/proper/gospel']};
  held.finish('reader-comparison.js',{compare(input){compared=input;return view;}});
  held.finish('reader-compare-view.js',{render(input){presented=input;return rendered;}});
  await ready;
  const derived={options:[{option:null}]};
  const request={...state('compare'),edition:{id:'primary'},calendar:{id:'primary'},bible:{id:'fixed'},
    comparison:{dimension:'recension',anchor:{civilDate:'2026-11-22',territorialContext:'universal'},
      sides:[{id:'primary',edition:{id:'primary'},calendar:{id:'primary'}},
        {id:'peer',edition:{id:'peer'},calendar:{id:'peer'}}]}};
  const built=await day.build({state:request,derived,isCurrent:()=>true,
    load:async()=>({}),Model:{derive:()=>derived},
    structures:{primary:{masses:[{key:'held'}]},peer:{masses:[{key:'held'}]}},
    Adapters:{adaptDay({request}){return {request,resolved:{edition:request.edition.id,formulary:'held'}};}},
    bibles:[{id:'fixed'}],missals:[],T:{citationsOf:()=>[],fetchFragments:async()=>({fragments:new Map()})}});
  assert.equal(built.view,view); assert.equal(built.rendered,rendered);
  assert.equal(compared.sides.length,2); assert.equal(presented.sides.length,2);
});

test('modern shells keep eager controls and shared styles while mode modules remain loader-owned',()=>{
  const optional=source(LITURGY+'reader-optional-runtime.js');
  for(const file of ['day.html','day-reader.html','index.html','propers-reader.html']) {
    const page=source(LITURGY+file);
    for(const module of ['reader-comparison','reader-compare-view','reader-study-view']) {
      assert.ok(!page.includes('<script src="'+module+'.js"></script>'),file+' '+module);
      assert.ok(optional.includes(module+'.js'));
    }
    const day=file.startsWith('day');
    for(const module of [day?'day-compare':'propers-compare',day?'day-study':'propers-study','reader-state','reader-state-adapters'])
      assert.ok(page.includes('<script src="'+module+'.js"></script>'));
    assert.ok(page.includes('reader-compare-view.css')); assert.ok(page.includes('reader-study-view.css'));
  }
  for(const file of ['reader-visual-reset-day.html','reader-visual-reset-propers.html']) {
    const oracle=source(LITURGY+file);
    assert.ok(oracle.includes('<script src="day.js"></script>'));
    assert.ok(!oracle.includes('<script src="reader-optional-runtime.js"></script>'));
  }
});
