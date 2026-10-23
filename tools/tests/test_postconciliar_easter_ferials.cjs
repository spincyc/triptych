'use strict';
// Fresh production structure on stdin. No duplicated resolver or source bodies.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const S=require(path.join(root,'src/web/browser/liturgy/ordinary-seating.js'));
const A=require(path.join(root,'src/web/browser/liturgy/reader-state-adapters.js'));
const C=require(path.join(root,'src/web/browser/liturgy/reader-state.js'));
const source=JSON.parse(fs.readFileSync(0,'utf8'));
const ordinary=JSON.parse(fs.readFileSync(path.join(root,'src/web/data/structure/ordinary/postconciliar.json')));
const before=JSON.stringify(source),fact='easter-4-sunday-john-10-1-10-actually-read';
const mass=source.masses.find(m=>m.key==='easter-4-monday');
assert.equal(mass.proper_source_paths.length,1);
const relation=mass.proper_source_paths[0],rid='main/easter-4-monday-gospel';
const qualified='proper-choice/postconciliar/easter-4-monday/'+rid;
assert.equal(relation.source_edition,'postconciliar');
assert.deepEqual(relation.paths.map(p=>[p.id,p.standing,p.calendar_cycles,p.choices,p.members,p.when]),[
 ['john-10-1-10','principal',{family:'sunday',in:['A','B','C']},{gospel:'john-10-1-10'},
  [{appointment:{mass:mass.key,form_id:'main',proper:'Gospel',occurrence:1},material_cycle:{family:null,cycle:'all'}}],undefined],
 ['john-10-11-18-a','optional',{family:'sunday',in:['A']},{gospel:'john-10-11-18'},
  [{appointment:{mass:mass.key,form_id:'main',proper:'Gospel',occurrence:2},material_cycle:{family:'cycles',cycle:'A'}}],{fact,is:true}]
]);
const gospels=mass.propers.filter(p=>p.name==='Gospel');
assert.equal(gospels.length,2);
assert.deepEqual(Object.keys(gospels[1].cycles),['A']);
assert.equal(gospels[1].cycles.A.citations[0].ref,'John 10:11-18');
assert.equal(gospels[0].citations[0].ref,'John 10:1-10');
let executions=0,refusals=0,adapterExecutions=0,cliCases=0;
function prepare(cycle,entrance,choice,facts,definitions=mass.proper_source_paths,propers=mass.propers){
 executions++;
 return S.prepareProperAppointments(propers.map((proper,sourceIndex)=>({proper,sourceIndex})),{
  calendar:'postconciliar',mass:mass.key,formId:'main',entrance,sourcePaths:definitions,
  calendarCycles:{sunday:cycle,weekday:'II'},choices:choice?{[rid]:choice}:{},conditionFacts:facts});
}
function selected(result){
 return S.unframedEvents(result.rows,null,result.selections).flatMap(event=>
  event.kind==='proper'?[event]:event.options.filter(option=>option.id===(event.selection||{}).option).flatMap(option=>option.rows))
  .filter(r=>r.proper.appointment_identity&&r.proper.appointment_identity.proper==='Gospel');
}
function fail(run,pattern){
 assert.throws(run,pattern);refusals++;
}
const factsCases=[{}, {[fact]:null}, {[fact]:false}, {[fact]:true},
 Object.create({[fact]:true}),Object.create({[fact]:false})];
for(const entrance of ['day','propers'])for(const cycle of ['A','B','C'])for(const facts of factsCases){
 const principal=prepare(cycle,entrance,'john-10-1-10',facts);
 assert.equal(principal.sourcePathSelections[rid].option,'john-10-1-10');
 assert.deepEqual(selected(principal).map(r=>r.proper.appointment_identity),
  [{mass:mass.key,form_id:'main',proper:'Gospel',occurrence:1}]);
 const allowed=cycle==='A'&&Object.hasOwn(facts,fact)&&facts[fact]===true;
 if(allowed){
  const alternate=prepare(cycle,entrance,'john-10-11-18-a',facts);
  assert.equal(alternate.sourcePathSelections[rid].option,'john-10-11-18-a');
  assert.deepEqual(selected(alternate).map(r=>r.proper.appointment_identity),
   [{mass:mass.key,form_id:'main',proper:'Gospel',occurrence:2}]);
  assert.equal(Object.values(alternate.materialSelections).find(p=>p.family==='cycles').cycle,'A');
 }else fail(()=>prepare(cycle,entrance,'john-10-11-18-a',facts));
 const unmade=prepare(cycle,entrance,null,facts);
 if(cycle==='A'&&(!Object.hasOwn(facts,fact)||facts[fact]!==false)){
  assert.equal(unmade.sourcePathSelections[rid].state,'required');
  assert.equal(selected(unmade).length,0);
  assert.equal(Object.keys(unmade.materialSelections).length,0);
 }else{
  // Existing unique-possible-path admission is not an authored display default.
  assert.equal(unmade.sourcePathSelections[rid].option,'john-10-1-10');
 }
 fail(()=>prepare(cycle,entrance,'john-10-1-10',{...facts,[fact]:'true'}),/boolean/);
}
for(const entrance of ['day','propers'])for(const cycle of ['A','B','C']){
 for(const bad of ['true','false',0,1,{},[],undefined]){
  fail(()=>prepare(cycle,entrance,'john-10-1-10',{[fact]:bad}),/boolean/);
  fail(()=>prepare(cycle,entrance,'john-10-11-18-a',{[fact]:bad}),/boolean/);
 }
 for(const malformed of ['wrong-occurrence','wrong-material','foreign-member','missing-guard','extra-option']){
  const definitions=structuredClone(mass.proper_source_paths),propers=structuredClone(mass.propers);
  if(malformed==='wrong-occurrence')definitions[0].paths[1].members[0].appointment.occurrence=3;
  if(malformed==='wrong-material')definitions[0].paths[1].members[0].material_cycle={family:null,cycle:'all'};
  if(malformed==='foreign-member')definitions[0].paths[1].members[0].appointment.mass='easter-4-tuesday';
  if(malformed==='missing-guard')delete propers.find(p=>p.source_path_relation).source_path_relation;
  if(malformed==='extra-option'){
   const extra=structuredClone(propers.find(p=>p.source_path_relation));
   extra.ordinary_disposition.option='unowned';extra.appointment_identity.occurrence=3;delete extra.source_path_relation;
   propers.push(extra);
  }
  fail(()=>prepare(cycle,entrance,'john-10-1-10',{},definitions,propers));
 }
}
function inputFor(cycle,entrance,framed,choice,facts){
 const request={schema:C.STATE_SCHEMA,entrance,civilDate:entrance==='day'?'2026-04-27':null,
  edition:{id:'postconciliar'},bible:{id:'douay-rheims',numbering:'vulgate'},
  languages:framed?{orations:'en',ordinary:'en'}:{orations:'en'},requestedMode:framed?'missal':'read',
  options:{ordinary:framed,legitimate:{}},coverage:[],unresolvedChoices:[],sourceHooks:[],
  properChoices:{[qualified]:choice}};
 if(entrance==='day')request.calendar={id:'postconciliar'};
 else {request.formulary={id:mass.key,type:mass.kind};if(cycle==='A')request.cycle='A';}
 return {request,structure:source,ordinary,conditionFacts:facts,
  derived:{calendar:'postconciliar',date:request.civilDate,weekday:'monday',season:'easter',
   liturgicalYear:{lectionary:{sunday:cycle,weekday:'II'},anchors:{}},
   options:[{option:null,winner:{id:mass.key,nature:'feria'},settled:true,
    readable:[{key:mass.key,state:'said'}],absent:[]}]}};
}
for(const entrance of ['day','propers'])for(const framed of [false,true])for(const cycle of ['A','B','C']){
 for(const facts of factsCases){
  const input=inputFor(cycle,entrance,framed,'john-10-1-10',facts);
  const result=entrance==='day'?A.adaptDay(input):A.adaptPropers(input);adapterExecutions++;
  assert.equal(result.sourcePathChoices.find(c=>c.id===qualified).selection.option,'john-10-1-10');
 }
 // The correct date, annual material A and an explicit alternate selection
 // together still cannot attest actual prior use.
 const unproved=inputFor('A',entrance,framed,'john-10-11-18-a',{});
 fail(()=>entrance==='day'?A.adaptDay(unproved):A.adaptPropers(unproved),/source-condition-unresolved/);
 const proved=inputFor('A',entrance,framed,'john-10-11-18-a',{[fact]:true});
 const result=entrance==='day'?A.adaptDay(proved):A.adaptPropers(proved);adapterExecutions++;
 assert.equal(result.sourcePathChoices.find(c=>c.id===qualified).selection.option,'john-10-11-18-a');
}
let staticForms=0;
for(const week of [2,3,4])for(const day of ['monday','tuesday','wednesday','thursday','friday','saturday']){
 const one=source.masses.find(m=>m.key===`easter-${week}-${day}`);
 S.validateProperSeating(ordinary,one.propers,{calendar:'postconciliar',mass:one.key,form_id:'main',full:true,
  facts:source.proper_appointment_facts||{},sourcePaths:one.proper_source_paths});staticForms++;
 const acclamation=one.propers.find(p=>p.name==='Gospel Acclamation');assert(acclamation);
 if(!['easter-2-friday','easter-3-monday'].includes(one.key)){
  assert.equal(acclamation.source,'composed');assert.equal(acclamation.text_status.state,'unavailable');
  assert.equal(acclamation.citations.length,0);assert(!acclamation.text);
 }
}
if(process.env.TRIPTYCH_EASTER_CLI_MANIFEST){
 const manifest=JSON.parse(fs.readFileSync(process.env.TRIPTYCH_EASTER_CLI_MANIFEST));
 for(const one of manifest.cases.filter(c=>c.exit===0)){
  const payload=JSON.parse(fs.readFileSync(one.path));
  const day=payload.days.find(d=>d.calendar==='postconciliar');
  const raw=day.masses.find(m=>m.key===one.mass);assert(raw);
  const request={schema:C.STATE_SCHEMA,entrance:'day',civilDate:payload.date,calendar:{id:'postconciliar'},
   edition:{id:'postconciliar'},bible:{id:'douay-rheims',numbering:'vulgate'},
   languages:{orations:'en',ordinary:'en'},requestedMode:'missal',options:{ordinary:true,legitimate:{}},
   coverage:[],unresolvedChoices:[],sourceHooks:[]};
  if(Object.keys(one.choices||{}).length)request.properChoices=one.choices;
  const derived={calendar:'postconciliar',date:payload.date,weekday:'monday',season:'easter',
   liturgicalYear:{lectionary:day.why.lectionary,anchors:{}},
   options:[{option:null,winner:{id:one.mass,nature:'feria'},settled:true,readable:[{key:one.mass,state:'said'}],absent:[]}]};
  const result=A.adaptCli({request,structure:source,ordinary,derived,payload});cliCases++;
  assert(result.events.length);
  if(one.mass===mass.key){
   assert.equal(result.sourcePathChoices.find(c=>c.id===qualified).selection.option,'john-10-1-10');
   const changed=structuredClone(payload),target=changed.days.find(d=>d.calendar==='postconciliar').masses.find(m=>m.key===mass.key);
   const at=target.propers.findIndex(p=>p.name==='Gospel'&&p.appointment_identity.occurrence===2);
   assert(at>=0);delete target.propers[at].source_path_relation;
   fail(()=>A.adaptCli({request,structure:source,ordinary,derived,payload:changed}),/order disagrees|source.*metadata/);cliCases++;
  }
 }
}
assert.equal(staticForms,18);
assert.equal(JSON.stringify(source),before,'raw source metadata must never mutate during admission');
console.log(JSON.stringify({status:'pass',executions,refusals,adapterExecutions,staticForms,cliCases}));
