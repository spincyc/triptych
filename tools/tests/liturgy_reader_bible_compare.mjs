#!/usr/bin/env node
/* Explicit public Bible editions over one unchanged source formulary. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createRequire } from 'node:module';
import vm from 'node:vm';
import test from 'node:test';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const CANDIDATE = resolve(process.env.TRIPTYCH_BIBLE_COMPARE_MODULE_ROOT || ROOT);
const require = createRequire(import.meta.url);
const modulePath = name => resolve(CANDIDATE, 'src/web/browser/liturgy', name);
const State = require(modulePath('reader-state.js'));
const Adapters = require(modulePath('reader-state-adapters.js'));
const Comparison = require(modulePath('reader-comparison.js'));
const PropersCompare = require(modulePath('propers-compare.js'));
const View = require(modulePath('reader-compare-view.js'));
const Actions = require(modulePath('reader-share-print.js'));
const read = path => JSON.parse(readFileSync(resolve(ROOT, path), 'utf8'));
const bibles = read('src/web/data/bibles.json').bibles;
const structure = read('src/web/data/structure/propers/roman-1962.json');
const context = Adapters.validationContext({ entrance:'propers', bibles:{ bibles },
  properIndex:read('src/web/data/structure/propers/index.json'), ordinaryIndex:{ calendars:[] },
  structures:{ 'roman-1962':structure } });
const prefix = '#missal=roman-1962&type=seasonal&mass=advent-1&bible=douay-rheims&orations=la&mode=compare&compare=bible-edition';
const fixture = JSON.parse(readFileSync(resolve(CANDIDATE, 'tools/tests/fixtures/liturgy-reader-comparison/v1/propers-roman-1962-bible-editions.json'), 'utf8'));
const hash = fixture.positive.hash;
assert.equal(hash, prefix + '&peer-bible=king-james-version');
const normalize = value => State.normalizeLegacy(State.parseLegacy('propers', value), {
  context, defaults:{ missal:'roman-1962', bible:'douay-rheims', orations:'la' }
});
function input(value = hash) {
  const normalized = normalize(value);
  assert.equal(normalized.ok, true, JSON.stringify(normalized.errors));
  const state = normalized.state;
  return { state, comparison:state.comparison, bibles,
    sides:state.comparison.sides.map(descriptor => ({ id:descriptor.id, structure,
      result:Adapters.adaptPropers({ request:PropersCompare.sideRequest(state, descriptor), structure }) })) };
}
class Element {
  constructor(tag, text = '') {
    this.tagName=tag; this.nodeType=tag==='#text'?3:1; this.nodeValue=tag==='#text'?text:null;
    this._text=tag==='#text'?'':text; this.children=[]; this.className=''; this.attrs={}; this.dataset={};
    this.lang=''; this.hidden=false; this.style={};
    this.classList={ add:(...names)=>{this.className+=' '+names.join(' ');}, remove:()=>{}, toggle:()=>{} };
  }
  appendChild(node) { this.children.push(node); return node; }
  append(...nodes) { nodes.forEach(node=>this.appendChild(node)); }
  replaceChildren(...nodes) { this.children=[]; this._text=''; this.append(...nodes); }
  setAttribute(key,value) { this.attrs[key]=String(value); }
  getAttribute(key) { return this.attrs[key]??null; }
  addEventListener() {}
  querySelectorAll() { return []; }
  get lastChild() { return this.children.at(-1)||null; }
  get textContent() { return this.nodeValue??this._text+this.children.map(node=>node.textContent).join(''); }
  set textContent(value) { this._text=String(value); this.children=[]; }
}
function runtime() {
  const document={ createElement:tag=>new Element(tag), createTextNode:text=>new Element('#text',text),
    createDocumentFragment:()=>new Element('#fragment'), getElementById:()=>null, addEventListener(){},
    body:{ classList:{toggle(){}} } };
  const requests=[];
  const window={ document, location:{search:'?data=/src/web/data'}, addEventListener(){} };
  async function fetch(url) {
    let path=String(url).replace(/^\/+/, '');
    if (/^src\/web\/data\/[^/]+\/chapters\//.test(path)) path=path.replace(/^src\/web\/data\//,'src/sources/bibles/');
    requests.push(path);
    try { const value=read(path); return {ok:true,status:200,text:async()=>JSON.stringify(value)}; }
    catch(_error) { return {ok:false,status:404,json:async()=>null}; }
  }
  const held=vm.createContext({window,document,URLSearchParams,URL,console,fetch,Map,Set});
  vm.runInContext(readFileSync(resolve(CANDIDATE,'src/web/browser/shared/browser-core.js'),'utf8'),held);
  return {T:window.Triptych,document,requests};
}
const classes=(node,name)=>[...(node.className.split(/\s+/).includes(name)?[node]:[]),...node.children.flatMap(child=>classes(child,name))];
async function build(value = hash) {
  const prepared=input(value), production=runtime();
  globalThis.document=production.document; globalThis.Triptych=production.T;
  const result=await PropersCompare.build({ state:prepared.state, structure, bibles,
    Adapters, Comparison, View, T:production.T, isCurrent:()=>true });
  return {...result,production,prepared};
}

test('explicit published Bible peers retain identities numbering and canonical storage-free URL state',()=>{
  const normalized=normalize(hash);
  assert.equal(normalized.ok,true,JSON.stringify(normalized.errors));
  assert.deepEqual(normalized.state.comparison.sides.map(side=>side.bible), fixture.positive.bibles);
  assert.equal(normalized.state.civilDate,null);
  const canonical=State.serializeLegacy(normalized);
  assert.deepEqual(normalize(canonical).state,normalized.state);
  assert.equal(State.serializeLegacy(normalize(canonical)),canonical);
});

test('missing equal unknown duplicate wrong-entrance and mixed-axis Bible peers refuse',()=>{
  for(const value of [prefix,hash.replace('&bible=douay-rheims',''),
    hash.replace('peer-bible=king-james-version','peer-bible=douay-rheims'),
    hash.replace('peer-bible=king-james-version','peer-bible=nab-revised'),
    hash+'&peer-bible=clementine-vulgate',hash+'&peer-cycle=A',hash+'&peer-orations=en',
    hash+'&peer-alternative=longer',hash+'&peer-witness=other',hash.replace('mode=compare','mode=read')])
    assert.equal(normalize(value).ok,false,value);
  const day=State.normalizeLegacy(State.parseLegacy('day','#date=2026-08-02&missal=roman-1962&bible=douay-rheims&orations=la&mode=compare&compare=recension&peer-missal=postconciliar&territory=universal&peer-bible=king-james-version'),{context,defaults:{date:'2026-08-02',missal:'roman-1962',bible:'douay-rheims',orations:'la'}});
  assert.equal(day.ok,false);
});

test('raw state and compare API reject mismatched primary Bible or numbering and absent public manifest',()=>{
  const prepared=input();
  const wrong=structuredClone(prepared.state); wrong.comparison.sides[0].bible.id='clementine-vulgate';
  assert.equal(State.validateReaderState(wrong).ok,false);
  const numbering=input(); numbering.comparison.sides[1].bible.numbering='vulgate';
  assert.throws(()=>Comparison.compare(numbering),/Bible|numbering/);
  const missing=input(); delete missing.bibles;
  assert.throws(()=>Comparison.compare(missing),/published Bible/);
  const duplicate=input(); duplicate.bibles=bibles.concat([bibles[0]]);
  assert.throws(()=>Comparison.compare(duplicate),/published Bible/);
});

test('Bible side requests preserve every non-Bible axis and never mutate original state',()=>{
  const state=normalize(hash).state;
  Object.assign(state,{form:'day',cycle:'A',alternative:{id:'source-option'},textDisplay:'latin-and-selected'});
  state.languages={orations:'en',translationWitness:'fixed-witness',ordinary:'la'};
  state.options={ordinary:false,legitimate:{creed:'nicene'}};
  const before=JSON.stringify(state), request=PropersCompare.sideRequest(state,{
    ...state.comparison.sides[1],languages:{orations:'la'},cycle:'B',alternative:{id:'wrong-option'}});
  for(const key of ['edition','formulary','form','cycle','alternative','textDisplay','languages','options']) assert.deepEqual(request[key],state[key],key);
  assert.deepEqual(request.bible,{id:'king-james-version',numbering:'hebrew'});
  assert.equal(Object.hasOwn(request,'comparison'),false); assert.equal(JSON.stringify(state),before);
});

test('same source membership aligns every Pentecost occurrence including unmapped Lesson and Sequence',()=>{
  const prepared=input(hash.replace('mass=advent-1','mass=pentecost'));
  const view=Comparison.compare(prepared);
  assert.equal(view.units.length,10); assert.equal(view.calendarResults,null);
  assert.ok(view.units.every(unit=>unit.relation==='same-source-event'));
  for(const ordinal of [3,5]) {
    const unit=view.units.find(unit=>unit.sourceCoordinate.ordinal===ordinal);
    assert.equal(unit.semanticSlot,null);
    assert.equal(unit.sides[0].event.id,unit.sides[1].event.id);
    assert.equal(unit.sourceCoordinate.properStructureId,`roman-1962/pentecost/00${ordinal}`);
  }
});

test('duplicate wrong-owner wrong-form wrong-label and wrong-coordinate source evidence refuse',()=>{
  for(const mutate of [
    p=>p.sides[1].result.events.push(structuredClone(p.sides[1].result.events[0])),
    p=>{p.sides[1].result.events[0].sourceHooks.push({...p.sides[1].result.events[0].sourceHooks[0]});},
    p=>{p.sides[1].result.events[0].sourceHooks[0].id='roman-1962/pentecost/001';},
    p=>{p.sides[1].result.events[0].id='proper/roman-1962/advent-1/999';},
    p=>{p.sides[1].result.events[0].editionSlotLabel='Not its source role';},
    p=>{p.sides[1].result.resolved.form='another-form';},
    p=>{p.sides[1].structure=structuredClone(structure);}
  ]) { const prepared=input(); mutate(prepared); assert.throws(()=>Comparison.compare(prepared)); }
});

test('all non-Bible side selections and strict recension dimension remain guarded',()=>{
  for(const mutate of [
    p=>{p.sides[1].result.request.edition.id='postconciliar';},
    p=>{p.sides[1].result.request.form='other';},p=>{p.sides[1].result.request.cycle='A';},
    p=>{p.sides[1].result.request.languages.orations='en';},
    p=>{p.sides[1].result.request.languages.translationWitness='other';},
    p=>{p.sides[1].result.request.textDisplay='latin-and-selected';},
    p=>{p.sides[1].result.request.options.legitimate={creed:'nicene'};},
    p=>{p.sides[1].result.request.alternative={id:'other'};}
  ]) { const prepared=input(); mutate(prepared); assert.throws(()=>Comparison.compare(prepared)); }
  const recension=input(); recension.comparison.dimension='recension';
  assert.throws(()=>Comparison.compare(recension),/Propers comparison/);
  const Assembly = require(modulePath('assembly-model.js'));
  const spec = read('tools/tests/fixtures/liturgy-reader-comparison/v1/day-2026-11-22.json');
  const day = {comparison:spec.comparison,sides:spec.comparison.sides.map(side=>{
    const request = structuredClone(read('tools/tests/fixtures/liturgy-reader-state/v1/day-roman-1962-2026-08-02.json').requested);
    request.civilDate=spec.comparison.anchor.civilDate; request.edition={id:side.edition.id};
    request.calendar={id:side.calendar.id}; request.requestedMode='read'; delete request.selectedReadableFormulary;
    const derived=Assembly.derive({date:request.civilDate,
      year:read('src/web/data/structure/calendar/'+side.calendar.id+'/2026.json'),
      rubrics:read('src/web/data/structure/rubrics/'+side.calendar.id+'.json')});
    return {id:side.id,result:Adapters.adaptDay({request,derived,
      structure:read('src/web/data/structure/propers/'+side.edition.id+'.json')})};
  })};
  assert.equal(Comparison.compare(day).entrance,'day');
  day.sides[1].result.request.bible={id:'king-james-version',numbering:'hebrew'};
  assert.throws(()=>Comparison.compare(day),/same Bible/);
});

test('two Bible fragment maps render independent words and precise Psalm numbering context',async()=>{
  const built=await build();
  const text=built.rendered.fragment.textContent;
  assert.match(text,/Douay-Rheims/); assert.match(text,/King James/);
  assert.match(text,/vulgate numbering/); assert.match(text,/hebrew numbering, psalm titles unnumbered/);
  assert.match(text,/Bible reconstruction/); assert.match(text,/To thee|Unto thee/i); assert.match(text,/Psalm[s]? 25|Ps 25/);
  assert.ok(built.production.requests.some(path=>path.includes('/douay-rheims/chapters/')));
  assert.ok(built.production.requests.some(path=>path.includes('/king-james-version/chapters/')));
  assert.equal(built.rendered.semanticIds.length,10);
  assert.ok(built.rendered.semanticIds.every(id=>id.startsWith('compare/source/proper/roman-1962/advent-1/')));
});

test('real Epiphany Psalm72 refusal stays on the selected English side without a Douay fallback',async()=>{
  const built=await build(fixture.negative.hash);
  const offertory=built.view.units.find(unit=>unit.sourceCoordinate.ordinal===7);
  assert.equal(offertory.sides[0].bibleCitations[0].state,'resolved');
  assert.equal(offertory.sides[1].bibleCitations[0].state,'refused');
  assert.deepEqual(offertory.sides[1].bibleCitations[0], {reference:fixture.negative.reference, state:fixture.negative.state, reason:fixture.negative.reason});
  const unit=classes(built.rendered.fragment,'compare-unit').find(node=>node.dataset.semanticLocation.endsWith('/007'));
  const columns=classes(unit,'compare-side');
  assert.match(columns[1].textContent,/Psalm 72.*no verse-for-verse correspondence/);
  assert.equal(classes(columns[1],'passage').length,0);
  assert.ok(classes(columns[0],'passage').length>0);
  assert.equal(columns[1].dataset.bibleCitations,'refused');
});

test('compare view refuses absent or malformed Bible citation evidence',async()=>{
  const built=await build(), wrong=structuredClone(built.view);
  delete wrong.units[0].sides[1].bibleCitations;
  assert.throws(()=>View.project(wrong),/per-citation resolution/);
  wrong.units[0].sides[1].bibleCitations=[{reference:'Psalm24',state:'resolved',reason:'silently guessed'}];
  assert.throws(()=>View.project(wrong),/per-citation resolution/);
});

test('full same-source locations preserve the original Proper on entering and leaving Compare',()=>{
  const prepared=input(); const result=prepared.sides[0].result;
  const location={kind:'event',id:result.events[5].id};
  const compared=PropersCompare.compareLocation(location,result,'bible-edition');
  assert.deepEqual(compared,{kind:'event',id:'compare/source/'+location.id});
  assert.deepEqual(PropersCompare.fromCompareLocation(compared,result),location);
});

test('sharing names the actual peer Bible and carries no liturgical text',()=>{
  const state=normalize(hash).state;
  const title=Actions.shareTitle('propers',{querySelector:()=>({textContent:'First Sunday of Advent'})},state);
  assert.match(title,/Compare bible-edition with king-james-version/);
  assert.doesNotMatch(title,/with roman-1962|Unto thee/);
  const canonical=Actions.canonicalUrl('propers',{href:'https://example.test/liturgy/propers-reader.html'+hash},State);
  assert.match(canonical,/index\.html#/); assert.match(canonical,/peer-bible=king-james-version/);
});
