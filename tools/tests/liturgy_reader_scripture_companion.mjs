#!/usr/bin/env node
/* Citation-level named Latin Bible accompaniment; no inferred verse alignment. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createRequire } from 'node:module';
import vm from 'node:vm';
import test from 'node:test';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const CANDIDATE = resolve(process.env.TRIPTYCH_SCRIPTURE_MODULE_ROOT || ROOT);
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
const prefix = '#missal=roman-1962&type=seasonal&mass=pentecost&bible=douay-rheims&orations=la&mode=compare&compare=bible-edition';
const hash = prefix + '&peer-bible=king-james-version';
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
function runtime(moduleRoot = CANDIDATE) {
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
  vm.runInContext(readFileSync(resolve(moduleRoot,'src/web/browser/shared/browser-core.js'),'utf8'),held);
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

const companion={id:'clementine-vulgate',numbering:'vulgate'};
const latin=bibles.find(row=>row.id===companion.id);
const english=bibles.find(row=>row.id==='douay-rheims');
const companionHash='&scripture-companion=clementine-vulgate';
const noCompare=hash.replace('&mode=compare&compare=bible-edition','').replace('&peer-bible=king-james-version','');
const plain=normalize(noCompare);
const descriptor=normalize(noCompare+companionHash);
const json=node=>JSON.stringify(node);
function findCitation(predicate,calendar='roman-1962') {
  const source=read('src/web/data/structure/propers/'+calendar+'.json');
  function walk(value) {
    if (!value || typeof value!=='object') return null;
    if (!Array.isArray(value) && value.loci && predicate(value)) return value;
    for (const child of Object.values(value)) { const answer=walk(child); if(answer)return answer; }
    return null;
  }
  const answer=walk(source); assert.ok(answer,'held citation fixture'); return answer;
}
function citationProper(citation,extra={}) {return {name:'Synthetic citation owner',source:'scripture',citations:[citation],...extra};}
async function renderedCitation(citation,primary=english,extra={}) {
  const production=runtime();
  const loaded=await production.T.fetchFragments(primary,[citation],{scriptureCompanion:companion},bibles);
  return {...production,loaded,node:production.T.renderProper(citationProper(citation,extra),primary,loaded,{numbering:'vulgate'})};
}
const simple={ref:'John 1:1-2',book:'John',token:'John',loci:{vulgate:[{chapter:1,first:1,last:2}],'hebrew-unnumbered-titles':[{chapter:1,first:1,last:2}]}};

test('explicit named Latin companion is additive and round trips on both entrances without changing prayer presentation',()=>{
  assert.equal(plain.ok,true,JSON.stringify(plain.errors)); assert.equal(Object.hasOwn(plain.state,'scriptureCompanion'),false);
  assert.doesNotMatch(State.serializeLegacy(plain),/scripture-companion/);
  assert.equal(descriptor.ok,true,JSON.stringify(descriptor.errors));
  assert.deepEqual(descriptor.state.scriptureCompanion,companion);
  assert.deepEqual(normalize(State.serializeLegacy(descriptor)).state,descriptor.state);
  assert.equal(Object.hasOwn(descriptor.state,'textDisplay'),false);
  const dayContext={...context,dayReadableFormularies:[]};
  const parseDay=value=>State.normalizeLegacy(State.parseLegacy('day',value),{context:dayContext,
    defaults:{date:'2026-05-24',missal:'roman-1962',bible:'douay-rheims',orations:'la'}});
  const day=parseDay('#date=2026-05-24&missal=roman-1962&bible=douay-rheims&orations=la'+companionHash);
  assert.equal(day.ok,true,JSON.stringify(day.errors));
  assert.deepEqual(parseDay(State.serializeLegacy(day)).state,day.state);
  for (const value of ['','missing','douay-rheims']) assert.equal(normalize(noCompare+'&scripture-companion='+value).ok,false,value);
  assert.equal(normalize(noCompare+companionHash+companionHash).ok,false);
  for (const value of [null,false,[],{}, {id:'x',numbering:[]},{id:'x',numbering:'vulgate',extra:true}])
    assert.equal(State.validateReaderState({...plain.state,scriptureCompanion:value}).ok,false,JSON.stringify(value));
});

test('browse projection validates the named Latin edition and preserves its exact descriptor',()=>{
  const prepared={parsed:State.parseLegacy('propers',companionHash),missal:'roman-1962',bible:'douay-rheims',orations:'la'};
  const result=Adapters.browseState(prepared,context);
  assert.equal(result.ok,true,JSON.stringify(result.errors)); assert.deepEqual(result.state.scriptureCompanion,companion);
  for(const value of ['','douay-rheims','absent']) {
    prepared.parsed=State.parseLegacy('propers','#scripture-companion='+value);
    assert.equal(Adapters.browseState(prepared,context).ok,false,value);
  }
  prepared.parsed=State.parseLegacy('propers',companionHash+companionHash);
  assert.equal(Adapters.browseState(prepared,context).ok,false);
});

test('legacy loader stays selected-only and same-edition accompaniment makes one exact chapter request',async()=>{
  const production=runtime();
  const loaded=await production.T.fetchFragments(english,[simple]);
  assert.equal(Object.hasOwn(loaded,'companion'),false);
  assert.deepEqual(production.requests,['src/sources/bibles/douay-rheims/chapters/John/1.json']);
  const same=runtime(); const held=await same.T.fetchFragments(latin,[simple],{scriptureCompanion:companion},bibles);
  assert.deepEqual(same.requests,['src/sources/bibles/clementine-vulgate/chapters/John/1.json']);
  const node=same.T.renderProper(citationProper(simple),latin,held);
  assert.equal(classes(node,'scripture-side').length,1); assert.equal(classes(node,'verse').length,2);
  assert.equal(classes(node,'scripture-pair').length,0);
  await assert.rejects(()=>same.T.fetchFragments(english,[simple],{scriptureCompanion:{id:'douay-rheims',numbering:'vulgate'}},bibles),/not held/);
  await assert.rejects(()=>same.T.fetchFragments(english,[simple],{scriptureCompanion:{id:'clementine-vulgate',numbering:'hebrew'}},bibles),/not held/);
});

test('citation-level pairs retain each edition language numbering witness rights and source words independently',async()=>{
  const {node,loaded,T}=await renderedCitation(simple);
  const sides=classes(node,'scripture-side'); assert.equal(sides.length,2);
  assert.deepEqual(sides.map(side=>side.attrs['data-bible-edition']),[latin.id,english.id]);
  assert.deepEqual(sides.map(side=>side.attrs['data-text-language']),['la','en']);
  for(const side of sides) {
    assert.equal(side.attrs['data-bible-numbering'],'vulgate');
    assert.equal(side.attrs['data-text-rights'],'public-domain'); assert.ok(side.attrs['data-bible-witness']);
    assert.match(side.textContent,/vulgate numbering/);
  }
  assert.match(sides[0].textContent,/In principio erat Verbum/); assert.doesNotMatch(sides[0].textContent,/In the beginning was the Word/);
  assert.match(sides[1].textContent,/In the beginning was the Word/);
  assert.equal(classes(node,'proper-name').length,1);
  assert.equal(json(classes(sides[0],'citation')[0]),json(T.renderCitation(simple,latin,loaded.companion.fragments,'vulgate',{showRef:false})));
  assert.equal(json(classes(sides[1],'citation')[0]),json(T.renderCitation(simple,english,loaded.fragments,'vulgate',{showRef:false})));
});

test('real KJV Epiphany refusal remains precise beside the held Clementine citation',async()=>{
  const citation=findCitation(c=>c.ref==='Psalm 72:1-2, 7-8, 10-11, 12-13','postconciliar');
  const primary=bibles.find(row=>row.id==='king-james-version');
  const {node,requests}=await renderedCitation(citation,primary);
  const [original,selected]=classes(node,'scripture-side');
  assert.ok(classes(original,'verse').length>0); assert.equal(classes(selected,'verse').length,0);
  assert.match(selected.textContent,/English Bibles divide Psalm 72 differently/);
  assert.doesNotMatch(selected.textContent,/Deus, judicium tuum regi da/);
  assert.ok(requests.every(path=>!path.includes('king-james-version/chapters/Ps')));
});

test('a refused Latin edition never suppresses selected text; both refusals and chapter/verse gaps stay independent',async()=>{
  const refused={...simple,refused:{'clementine-vulgate':'Synthetic Latin correspondence withheld.'}};
  let result=await renderedCitation(refused);
  assert.equal(classes(classes(result.node,'scripture-side')[0],'verse').length,0);
  assert.match(classes(result.node,'scripture-side')[0].textContent,/Synthetic Latin correspondence withheld/);
  assert.ok(classes(classes(result.node,'scripture-side')[1],'verse').length>0);
  const both={...refused,refused:{...refused.refused,'douay-rheims':'Synthetic selected correspondence withheld.'}};
  result=await renderedCitation(both);
  assert.equal(classes(result.node,'verse').length,0); assert.equal(result.requests.length,0);
  assert.match(result.node.textContent,/Synthetic Latin correspondence withheld/); assert.match(result.node.textContent,/Synthetic selected correspondence withheld/);
  const production=runtime(); const selected=new Map([['John|1',{ok:true,verses:{1:'Selected first verse.'}}]]);
  const original=new Map([['John|1',{ok:false,problem:'Synthetic Latin chapter unavailable.'}]]);
  const node=production.T.renderProper(citationProper(simple),english,{fragments:selected,companion:{bible:latin,fragments:original}});
  assert.match(classes(node,'scripture-side')[0].textContent,/Synthetic Latin chapter unavailable/);
  assert.match(classes(node,'scripture-side')[1].textContent,/verse 2.*absent from this edition/);
  assert.doesNotMatch(classes(node,'scripture-side')[0].textContent,/Selected first verse/);
});

test('real psalter departures read generated edition loci and preserve each entire citation without verse zipping',async()=>{
  const source=read('src/web/data/structure/propers/postconciliar.json'); const fixtures=[];
  function walk(value) {
    if(!value||typeof value!=='object')return;
    if(value.edition_loci?.[latin.id]?.some(locus=>[115,147].includes(locus.chapter)) && !fixtures.some(c=>c.edition_loci[latin.id][0].chapter===value.edition_loci[latin.id][0].chapter))fixtures.push(value);
    for(const child of Object.values(value))walk(child);
  }
  walk(source); assert.equal(fixtures.length,2);
  for(const citation of fixtures) {
    const {node,loaded,T}=await renderedCitation(citation);
    const [original,selected]=classes(node,'scripture-side');
    assert.ok(classes(original,'verse').length>0); assert.ok(classes(selected,'verse').length>0);
    assert.equal(json(classes(original,'citation')[0]),json(T.renderCitation(citation,latin,loaded.companion.fragments,'vulgate',{showRef:false})));
    assert.equal(json(classes(selected,'citation')[0]),json(T.renderCitation(citation,english,loaded.fragments,'vulgate',{showRef:false})));
    assert.match(original.textContent,/as this edition prints it/);
  }
});

test('whole psalms cross-chapter and segmented citations preserve independent loci and fragment counts',async()=>{
  const fixtures=[findCitation(c=>c.token==='Ps'&&Object.values(c.loci).some(rows=>rows.some(l=>l.first===null&&l.last===null))),
    findCitation(c=>Object.values(c.loci).some(rows=>new Set(rows.map(l=>l.chapter)).size>1)),
    findCitation(c=>Object.values(c.loci).some(rows=>rows.length>2))];
  for(const citation of fixtures) {
    const {node,loaded,T}=await renderedCitation(citation);
    assert.equal(classes(node,'scripture-pair').length,1);
    const [a,b]=classes(node,'scripture-side');
    assert.equal(json(classes(a,'citation')[0]),json(T.renderCitation(citation,latin,loaded.companion.fragments,'vulgate',{showRef:false})));
    assert.equal(json(classes(b,'citation')[0]),json(T.renderCitation(citation,english,loaded.fragments,'vulgate',{showRef:false})));
  }
});

test('mixed composed/Scripture and cycle owners keep one heading primary event source hooks and coverage',async()=>{
  const request={...descriptor.state,textDisplay:'latin-and-selected'};
  const before=Adapters.adaptPropers({request:plain.state,structure});
  const after=Adapters.adaptPropers({request,structure});
  for(const key of ['events','coverage','unresolvedChoices','explicitAbsences','resolved'])assert.deepEqual(after[key],before[key],key);
  const proper={...citationProper(simple),source:'mixed',text:'Latin source sentinel.',translations:[{lang:'en',source_id:'synthetic-witness',rights:'public-domain',text:'English sentinel.'}]};
  const {T,loaded}=await renderedCitation(simple);
  const node=T.renderProper(proper,english,loaded,{orations:'en',textDisplay:'latin-and-selected'});
  assert.equal(classes(node,'proper-name').length,1); assert.equal(classes(node,'text-pair').length,2);
  assert.equal((node.textContent.match(/Latin source sentinel/g)||[]).length,1);
  assert.match(node.textContent,/Bible text.*not the Missal’s wording/);
  const cycling={name:'Cycle reading',citations:[],cycles:{A:{citations:[simple]},B:{citations:[{...simple,ref:'Unselected cycle sentinel'}]}}};
  const selected=T.renderProper(cycling,english,loaded,{cycle:'A'});
  assert.equal(classes(selected,'scripture-pair').length,1); assert.doesNotMatch(selected.textContent,/Unselected cycle sentinel/);
});

test('Bible Compare holds the companion fixed without changing primary citations axes or statuses',async()=>{
  const prepared=input(hash+companionHash);
  assert.deepEqual(prepared.sides.map(side=>side.result.request.scriptureCompanion),[companion,companion]);
  const divergent=structuredClone(prepared); delete divergent.sides[1].result.request.scriptureCompanion;
  assert.throws(()=>Comparison.compare(divergent),/same edition/);
  const paired=await build(hash+companionHash), single=await build(hash);
  assert.equal(paired.view.dimension,'bible-edition');
  assert.deepEqual(paired.view.units,single.view.units);
  assert.deepEqual(paired.rendered.semanticIds,single.rendered.semanticIds);
  assert.ok(classes(paired.rendered.fragment,'scripture-pair').length>0);
  const latinPaths=paired.production.requests.filter(path=>path.includes('/clementine-vulgate/'));
  assert.equal(new Set(latinPaths).size,latinPaths.length,'chapter cache deduplicates companion across primary sides');
});

test('Day recension Compare keeps the same companion across independently resolved calendars',()=>{
  const Assembly=require(modulePath('assembly-model.js'));
  const spec=read('tools/tests/fixtures/liturgy-reader-comparison/v1/day-2026-11-22.json');
  const day={comparison:spec.comparison,sides:spec.comparison.sides.map(side=>{
    const request=structuredClone(read('tools/tests/fixtures/liturgy-reader-state/v1/day-roman-1962-2026-08-02.json').requested);
    request.civilDate=spec.comparison.anchor.civilDate;request.edition={id:side.edition.id};
    request.calendar={id:side.calendar.id};request.requestedMode='read';request.scriptureCompanion=companion;
    delete request.selectedReadableFormulary;
    const derived=Assembly.derive({date:request.civilDate,
      year:read('src/web/data/structure/calendar/'+side.calendar.id+'/2026.json'),
      rubrics:read('src/web/data/structure/rubrics/'+side.calendar.id+'.json')});
    return {id:side.id,result:Adapters.adaptDay({request,derived,
      structure:read('src/web/data/structure/propers/'+side.edition.id+'.json')})};
  })};
  const view=Comparison.compare(day);assert.equal(view.entrance,'day');assert.equal(view.dimension,'recension');
  assert.deepEqual(view.sides.map(side=>side.result.request.scriptureCompanion),[companion,companion]);
  delete day.sides[1].result.request.scriptureCompanion;
  assert.throws(()=>Comparison.compare(day),/same Bible/);
});

test('translation witness Compare retains its explicit source peers while the companion stays fixed',async()=>{
  const key='commemoratione-omnium-fidelium-defunctorum';
  const caswall='edition.edward-caswall.lyra-catholica.london-1849';
  const cummiskey='edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861';
  const value='#missal=roman-1962&type=sanctoral&mass='+key+'&form=first&bible=douay-rheims&orations=en&mode=compare&compare=translation-witness&translation-witness='+caswall+'&peer-witness='+cummiskey;
  const paired=await build(value+companionHash),selected=await build(value);
  assert.equal(paired.view.dimension,'translation-witness');
  assert.deepEqual(paired.view.units,selected.view.units);
  assert.deepEqual(paired.view.sides.map(side=>side.result.request.scriptureCompanion),[companion,companion]);
  assert.deepEqual(paired.rendered.semanticIds,selected.rendered.semanticIds);
  assert.ok(classes(paired.rendered.fragment,'scripture-pair').length>0);
  assert.deepEqual(paired.view.sides.map(side=>side.result.request.languages.translationWitness),[caswall,cummiskey]);
});

test('shared URL helper preserves prayer/Compare peers and semantic place while adding or removing only companion',()=>{
  const location={href:'https://example.test/liturgy/index.html'+hash+'&text-display=latin-and-selected'};
  const paired=Actions.scriptureCompanionUrl(location,latin.id,{kind:'event',id:'compare/proper/gospel'});
  const params=new URLSearchParams(new URL(paired).hash.slice(1));
  assert.equal(params.get('scripture-companion'),latin.id); assert.equal(params.get('peer-bible'),'king-james-version');
  assert.equal(params.get('text-display'),'latin-and-selected'); assert.equal(params.get('location'),'compare/proper/gospel');
  assert.doesNotMatch(location.href,/scripture-companion/);
  assert.equal(new URLSearchParams(new URL(Actions.scriptureCompanionUrl({href:paired},null)).hash.slice(1)).has('scripture-companion'),false);
  assert.throws(()=>Actions.scriptureCompanionUrl(location,'douay-rheims'),/Invalid/);
});

test('default shared loader and Scripture DOM stay byte-identical for non-liturgy callers',{skip:!process.env.TRIPTYCH_SCRIPTURE_BASELINE_ROOT},async()=>{
  const before=runtime(resolve(process.env.TRIPTYCH_SCRIPTURE_BASELINE_ROOT)),after=runtime();
  for(const edition of bibles) {
    const old=await before.T.fetchFragments(edition,[simple]); const fresh=await after.T.fetchFragments(edition,[simple]);
    assert.equal(JSON.stringify([...fresh.fragments]),JSON.stringify([...old.fragments]),edition.id);
    assert.equal(JSON.stringify(fresh.chapters),JSON.stringify(old.chapters),edition.id);
    assert.equal(Object.hasOwn(fresh,'companion'),false);
    assert.equal(json(after.T.renderCitation(simple,edition,fresh.fragments,'vulgate')),json(before.T.renderCitation(simple,edition,old.fragments,'vulgate')),edition.id);
    assert.equal(json(after.T.renderProper(citationProper(simple),edition,fresh.fragments)),json(before.T.renderProper(citationProper(simple),edition,old.fragments)),edition.id);
  }
  assert.deepEqual(after.requests,before.requests);
});
