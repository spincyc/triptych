'use strict';
// In-memory production structure is mandatory on stdin. No OLM body fixture.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const S=require(path.join(root,'src/web/browser/liturgy/ordinary-seating.js'));
const A=require(path.join(root,'src/web/browser/liturgy/reader-state-adapters.js'));
const C=require(path.join(root,'src/web/browser/liturgy/reader-state.js'));
const source=JSON.parse(fs.readFileSync(0,'utf8'));
const ordinary=JSON.parse(fs.readFileSync(path.join(root,'src/web/data/structure/ordinary/postconciliar.json')));
const before=JSON.stringify(source),preserved=new Set(['easter-6-wednesday','easter-6-saturday','easter-7-tuesday']);
const days=['monday','tuesday','wednesday','thursday','friday','saturday'];
let staticForms=0,adapterExecutions=0,heldAcclamationChecks=0,cliCases=0;
function properEvents(result){
 return result.events.flatMap(event=>event.kind==='proper'?[event]:
  event.kind==='proper-choice'?event.options.filter(o=>o.id===event.selection.option).flatMap(o=>o.events):[]);
}
function build(mass,cycle,entrance,framed,date='2027-05-10'){
 const request={schema:C.STATE_SCHEMA,entrance,civilDate:entrance==='day'?date:null,
  edition:{id:'postconciliar'},bible:{id:'douay-rheims',numbering:'vulgate'},
  languages:framed?{orations:'en',ordinary:'en'}:{orations:'en'},
  requestedMode:framed?'missal':'read',options:{ordinary:framed,legitimate:{}},
  coverage:[],unresolvedChoices:[],sourceHooks:[]};
 if(entrance==='day')request.calendar={id:'postconciliar'};
 else request.formulary={id:mass.key,type:mass.kind};
 // This is a projection/admission fixture, not evidence of regional transfer,
 // actual preceding-Sunday use, or which service occurred.
 const derived={calendar:'postconciliar',date,weekday:days.find(d=>mass.key.endsWith(d)),season:'easter',
  liturgicalYear:{lectionary:{sunday:cycle,weekday:'II'},anchors:{}},
  options:[{option:null,winner:{id:mass.key,nature:'feria'},settled:true,
   readable:[{key:mass.key,state:'said'}],absent:[]}]};
 return {request,derived,structure:source,ordinary};
}
for(const week of [5,6,7])for(const day of days){
 const mass=source.masses.find(m=>m.key===`easter-${week}-${day}`);assert(mass);
 S.validateProperSeating(ordinary,mass.propers,{calendar:'postconciliar',mass:mass.key,form_id:'main',full:true,
  facts:source.proper_appointment_facts||{},sourcePaths:mass.proper_source_paths});staticForms++;
 for(const cycle of ['A','B','C'])for(const entrance of ['day','propers'])for(const framed of [false,true]){
  const input=build(mass,cycle,entrance,framed);
  const result=entrance==='day'?A.adaptDay(input):A.adaptPropers(input);adapterExecutions++;
  const events=properEvents(result);
  assert.equal(events.length,mass.propers.length);
  assert.deepEqual(events.map(e=>e.editionSlotLabel),mass.propers.map(p=>p.name));
  const acclamation=events.find(e=>e.editionSlotLabel==='Gospel Acclamation');assert(acclamation);
  if(!preserved.has(mass.key)){
   heldAcclamationChecks++;
   assert.equal(acclamation.sourceKind,'composed');
   assert.equal(acclamation.selected.availability,'unavailable');
   assert(!acclamation.selected.text);
   const raw=mass.propers.find(p=>p.name==='Gospel Acclamation');
   assert.equal(raw.citations.length,0);assert(!raw.text);
   assert.equal(raw.text_status.state,'unavailable');
  }else assert.equal(acclamation.sourceKind,'scripture');
 }
}
if(process.env.TRIPTYCH_EASTER_V_VII_CLI_MANIFEST){
 const manifest=JSON.parse(fs.readFileSync(process.env.TRIPTYCH_EASTER_V_VII_CLI_MANIFEST));
 for(const one of manifest.cases.filter(c=>c.exit===0)){
  const payload=JSON.parse(fs.readFileSync(one.path));
  const day=payload.days.find(d=>d.calendar==='postconciliar');
  const raw=day.masses.find(m=>m.key===one.mass);assert(raw);
  const mass=source.masses.find(m=>m.key===one.mass);assert(mass);
  for(const framed of [false,true]){
   const input=build(mass,day.why.lectionary.sunday,'day',framed,payload.date);
   input.derived.liturgicalYear.lectionary=day.why.lectionary;
   // Match the actual CLI's selected readable standing, including optional
   // memorial days. This bridge check is not an independent occurrence witness.
   assert.equal(raw.selected,true);
   input.request.selectedReadableFormulary={id:one.mass};
   input.derived.options[0].readable[0].state=raw.standing;
   if(Object.keys(one.choices||{}).length)input.request.properChoices=one.choices;
   const browser=A.adaptDay(input);
   const cli=A.adaptCli({...input,payload});cliCases++;
   // Admission, identities and availability match. CLI carries actual fetched
   // Bible text whereas browser state carries addresses, so do not equate bodies.
   const shape=result=>properEvents(result).map(e=>({
    id:e.id,role:e.editionSlotLabel,source:e.sourceKind,semanticSlot:e.semanticSlot,
    unavailable:e.selected.availability==='unavailable',seat:e.seat}));
   assert.deepEqual(shape(cli),shape(browser));
  }
 }
}
assert.equal(JSON.stringify(source),before);
console.log(JSON.stringify({status:'pass',staticForms,adapterExecutions,heldAcclamationChecks,cliCases}));
