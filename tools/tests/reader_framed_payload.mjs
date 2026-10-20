/* Exact source, semantic, coverage and Ordinary parity for bounded 1962 framed payloads. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import {resolve} from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const root=resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname,'../..'));
const modules=resolve(process.env.TRIPTYCH_FRAMED_PAYLOAD_MODULE_ROOT || root,'src/web/browser/liturgy');
const json=p=>JSON.parse(fs.readFileSync(root+'/src/web/data/'+p));
const State=require(root+'/src/web/browser/liturgy/reader-state.js');
const A=require(root+'/src/web/browser/liturgy/reader-state-adapters.js');
const Model=require(root+'/src/web/browser/liturgy/assembly-model.js');
const Payload=require(modules+'/reader-proper-payload.js');
globalThis.LiturgyReaderProperPayload=Payload;
const Day=require(modules+'/day-read-payload.js');
const Props=require(modules+'/propers-read-payload.js');
const full=json('structure/propers/roman-1962.json'),index=json('structure/propers/index.json');
const ordinary=json('structure/ordinary/roman-1962.json'),ordinaryIndex=json('structure/ordinary/index.json');
const rubrics=json('structure/rubrics/roman-1962.json'),rubricsIndex=json('structure/rubrics/index.json'),year=json('structure/calendar/roman-1962/2026.json'),bibles=json('bibles.json');
const catalog=json('structure/propers/catalog/roman-1962.json');
const mono='structure/propers/roman-1962.json',catalogPath='structure/propers/catalog/roman-1962.json';
const envelopes=new Map(full.masses.map(m=>[m.key,json('structure/propers/mass/roman-1962/'+m.key+'.json')]));
function loader(requests,corrupt=null){return async p=>{requests.push(p);if(p===mono)return full;if(p===catalogPath)return catalog;if(p.startsWith('structure/propers/mass/roman-1962/')){let e=envelopes.get(p.split('/').at(-1).replace('.json',''));if(corrupt)e=corrupt(structuredClone(e));return e;}throw Error('unexpected '+p)}}
function context(entrance,structure,derived){return A.validationContext({entrance,bibles,rubricsIndex,properIndex:index,ordinaryIndex,structures:{'roman-1962':structure},ordinaries:{'roman-1962':ordinary},derived})}
function normalize(entrance,parsed,structure,derived){const n=State.normalizeLegacy(parsed,{context:context(entrance,structure,derived),defaults:{date:derived?.date,missal:'roman-1962',bible:'douay-rheims',orations:'la','ordinary-lang':'en'}});assert.equal(n.ok,true,JSON.stringify(n.errors));return n}
function propersParsed(mass,extra={}) {
 return State.parseLegacy('propers','#'+new URLSearchParams({missal:'roman-1962',type:mass.kind,
  mass:mass.key,bible:'douay-rheims',orations:'la',mode:'missal','ordinary-lang':'la',...extra}));
}
function dayInput(date,extra={}) {
 const parsed=State.parseLegacy('day','#'+new URLSearchParams({date,missal:'roman-1962',
  bible:'douay-rheims',orations:'la',mode:'missal',ordinary:'1','ordinary-lang':'la',...extra}));
 return {parsed,missal:'roman-1962',mode:parsed.recognized.mode,needsOrdinary:parsed.recognized.ordinary==='1',
  derived:Model.derive({date,rubrics,year}),index};
}

test('every eligible Propers Mass has exact full-context and seated-result parity',async(t)=>{
 let masses=0,states=0;
 assert.ok(Payload.framedMass(full.masses.find(m=>m.key==='pentecost'),propersParsed(full.masses.find(m=>m.key==='pentecost'))));
 for(const mass of full.masses){
  const parsed=propersParsed(mass);if(!Payload.framedMass(mass,parsed))continue;masses++;
  const requests=[],split=await Props.load({parsed,calendar:'roman-1962',index,load:loader(requests),monolith:mono});
  assert.ok(!requests.includes(mono),mass.key);assert.deepEqual(context('propers',split),context('propers',full));
  for(const lang of ['la','en'])for(const bible of ['douay-rheims','clementine-vulgate']){
   const p=propersParsed(mass,{'ordinary-lang':lang,bible});
   const a=normalize('propers',p,full),b=normalize('propers',p,split);assert.deepEqual(a,b);
   const x=A.adaptPropers({request:a.state,structure:full,ordinary}),y=A.adaptPropers({request:b.state,structure:split,ordinary});
   assert.deepEqual(y,x,mass.key);assert.deepEqual(y.unresolvedChoices,[]);assert.deepEqual(y.ordinaryUnresolved,[]);states++;
  }
 }
 t.diagnostic(`${masses} complete Mass payloads; ${states} exact language/Bible states`);
});

test('every eligible 2026 Day has exact Missal and Study Ordinary parity',async(t)=>{
 let dates=0,states=0;assert.equal(Day.eligibleKey(dayInput('2026-08-02')),'pentecost-10');
 for(let i=0;i<365;i++){
  const date=new Date(Date.UTC(2026,0,1+i)).toISOString().slice(0,10),input=dayInput(date);
  const key=Day.eligibleKey(input),mass=full.masses.find(m=>m.key===key);
  if(!key||!Payload.framedMass(mass,input.parsed))continue;dates++;
  const requests=[],split=await Day.loadStructure({...input,load:loader(requests)});
  assert.ok(!requests.includes(mono),date);assert.deepEqual(context('day',split,input.derived),context('day',full,input.derived));
  for(const mode of ['missal','study'])for(const lang of ['la','en'])for(const bible of ['douay-rheims','clementine-vulgate']){
   const p=dayInput(date,{mode,'ordinary-lang':lang,bible}).parsed;
   const a=normalize('day',p,full,input.derived),b=normalize('day',p,split,input.derived);assert.deepEqual(a,b);
   const x=A.adaptDay({request:a.state,derived:input.derived,structure:full,ordinary});
   const y=A.adaptDay({request:b.state,derived:input.derived,structure:split,ordinary});
   assert.deepEqual(y,x,date);assert.deepEqual(y.unresolvedChoices,[]);assert.deepEqual(y.ordinaryUnresolved,[]);states++;
  }
 }
 t.diagnostic(`${dates} settled dates; ${states} exact Missal/Study language/Bible states`);
});

test('commemorations, cross-Mass text, choices and exceptional frames retain full source',async()=>{
 for(const [date,extra] of [['2026-07-02',{}],['2026-12-25',{}],['2026-08-02',{mass:'pentecost-10'}],
  ['2026-08-02',{mode:'study',ordinary:'0'}],['2026-08-02',{mode:'compare'}],['2026-08-02',{orations:'en'}]]){
  const requests=[],selected=await Day.loadStructure({...dayInput(date,extra),load:loader(requests)});
  assert.equal(selected,full,date);assert.equal(requests.at(-1),mono);
 }
 for(const key of ['commune-doctorum-pontificis','commemoratione-omnium-fidelium-defunctorum',
  's-hilarii-episcopi-confessoris-ecclesiae-doctoris','good-friday','mass-of-the-lords-supper']){
  const mass=full.masses.find(m=>m.key===key),requests=[];
  assert.ok(mass,key);
  const selected=await Props.load({parsed:propersParsed(mass),calendar:'roman-1962',index,load:loader(requests),monolith:mono});
  assert.equal(selected,full,key);assert.equal(requests.at(-1),mono);
  const normalized=normalize('propers',propersParsed(mass),selected);
  A.adaptPropers({request:normalized.state,structure:selected,ordinary});
 }
 const mass=full.masses.find(m=>m.key==='pentecost'),requests=[];
 assert.equal(await Props.load({parsed:propersParsed(mass,{orations:'en'}),calendar:'roman-1962',index,load:loader(requests),monolith:mono}),full);
 assert.deepEqual(requests,[mono], 'known language boundary does not request unused split files');
 const english=normalize('propers',propersParsed(mass,{orations:'en'}),full);
 A.adaptPropers({request:english.state,structure:full,ordinary});
});

test('a wrong generation or descriptor cannot become a framed source claim',async()=>{
 for(const mutation of [e=>({...e,generation:'0'.repeat(64)}),e=>({...e,mass:{...e.mass,name:'wrong identity'}})]){
  const requests=[];assert.equal(await Day.loadStructure({...dayInput('2026-08-02'),load:loader(requests,mutation)}),full);
  assert.equal(requests.at(-1),mono);
  const mass=full.masses.find(m=>m.key==='pentecost'),propersRequests=[];
  assert.equal(await Props.load({parsed:propersParsed(mass),calendar:'roman-1962',index,load:loader(propersRequests,mutation),monolith:mono}),full);
  assert.equal(propersRequests.at(-1),mono);
 }
});


test('an older shared helper without framed capability keeps the full-source path',async()=>{
 const current=globalThis.LiturgyReaderProperPayload;
 globalThis.LiturgyReaderProperPayload={load:Payload.load};
 try {
  const requests=[];
  assert.equal(await Day.loadStructure({...dayInput('2026-08-02'),load:loader(requests)}),full);
  assert.deepEqual(requests,[mono]);
  const mass=full.masses.find(m=>m.key==='pentecost'),propersRequests=[];
  assert.equal(await Props.load({parsed:propersParsed(mass),calendar:'roman-1962',index,load:loader(propersRequests),monolith:mono}),full);
  assert.deepEqual(propersRequests,[mono]);
 } finally { globalThis.LiturgyReaderProperPayload=current; }
});
