'use strict';
// Exact source tuples are exercised from the canonical producer projection.
// A scratch projection can be supplied while the source owner's patch awaits
// integration. No fixture here invents a reading, source condition or course.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');
const S = require(path.join(root, 'src/web/browser/liturgy/ordinary-seating.js'));
const A = require(path.join(root, 'src/web/browser/liturgy/reader-state-adapters.js'));
const C = require(path.join(root, 'src/web/browser/liturgy/reader-state.js'));
const structurePath = process.env.TRIPTYCH_SOURCE_PATH_STRUCTURE || path.join(root, 'src/web/data/structure/propers/postconciliar.json');
const structure = JSON.parse(fs.readFileSync(structurePath));
const ordinary = JSON.parse(fs.readFileSync(path.join(root, 'src/web/data/structure/ordinary/postconciliar.json')));
const copy = (one) => JSON.parse(JSON.stringify(one));
const sameCoordinate = (left, right) => left && right && ['mass','form_id','proper','occurrence'].every((key) => left[key] === right[key]);
const relationMasses = structure.masses.filter((mass) => (mass.proper_source_paths || []).length);
assert(relationMasses.length >= 9, 'the exact authored nine Masses must be projected');
assert.equal(relationMasses.reduce((count,mass) => count+mass.proper_source_paths.length,0),10);
const before = JSON.stringify(structure); const checks = []; let executions=0;
function test(name, run) { run(); checks.push(name); }
function rowsFor(mass, form) {
 return mass.propers.map((proper,sourceIndex) => ({proper,sourceIndex})).filter((row) => row.proper.form_id === form);
}
function scoped(relation){return relation.form_id+'/'+relation.id;}
function qualified(mass, relation){return 'proper-choice/'+structure.calendar+'/'+mass.key+'/'+scoped(relation);}
function context(mass, relation, cycle, option){
 return {calendar:structure.calendar,mass:mass.key,formId:relation.form_id,entrance:'day',sourcePaths:mass.proper_source_paths,
  calendarCycles:{sunday:cycle,weekday:'II'},choices:option?{[scoped(relation)]:option}:{}};
}
function inputs(mass,relation,cycle,selected,framed,entrance){
 const request={schema:C.STATE_SCHEMA,entrance,civilDate:entrance==='day'?'2026-10-20':null,edition:{id:structure.calendar},
  bible:{id:'douay-rheims',numbering:'vulgate'},languages:framed?{orations:'la',ordinary:'en'}:{orations:'la'},
  requestedMode:framed?'missal':'read',options:{ordinary:framed,legitimate:{}},coverage:[],unresolvedChoices:[],sourceHooks:[],
  properChoices:{[qualified(mass,relation)]:selected.id}};
 if(entrance==='day')request.calendar={id:structure.calendar};else{request.formulary={id:mass.key,type:mass.kind};request.cycle=cycle;}
 if((mass.forms||[]).length>1){request.form=relation.form_id;if(entrance==='day')request.selectedReadableFormulary={id:mass.key};}
 const derived={calendar:structure.calendar,date:request.civilDate,weekday:'sunday',season:'lent',liturgicalYear:{lectionary:{sunday:cycle,weekday:'II'},anchors:{}},
  options:[{option:null,winner:{id:mass.key,nature:'sunday'},settled:true,readable:[{key:mass.key,state:'said'}],absent:[]}]};
 const conditionFacts=selected.when?{[selected.when.fact]:selected.when.is}:{};
 return{request,structure,ordinary,derived,conditionFacts};
}
function allEvents(events){return events.flatMap((event)=>event.kind==='proper-choice'?event.options.flatMap((option)=>allEvents(option.events)):[event]);}
test('all actual source paths retain exact material, original ordinals and calendar course in both entrances and frames',()=>{
 for(const mass of relationMasses)for(const relation of mass.proper_source_paths)for(const selected of relation.paths)for(const cycle of selected.calendar_cycles.in)for(const framed of [false,true])for(const entrance of ['day','propers']){
  const input=inputs(mass,relation,cycle,selected,framed,entrance);
  const result=entrance==='day'?A.adaptDay(input):A.adaptPropers(input);
  if(entrance==='day')assert.equal(result.calendarResult.lectionary.sunday,cycle);else assert.equal(result.calendarResult,null);
  const control=result.sourcePathChoices.find((one)=>one.id===qualified(mass,relation));assert(control);assert.equal(control.selection.option,selected.id);
  for(const member of selected.members){
   const sourceIndex=mass.propers.findIndex((proper)=>sameCoordinate(proper.appointment_identity,member.appointment));assert(sourceIndex>=0);
   const event=allEvents(result.events).find((one)=>one.id==='proper/'+structure.calendar+'/'+mass.key+'/'+String(sourceIndex+1).padStart(3,'0'));
   assert(event,'selected member must remain a distinct source event');assert.equal(event.selected.cycle,member.material_cycle.cycle==='all'?null:member.material_cycle.cycle);
   if(framed&&(!mass.ordinary_frame||mass.ordinary_frame.applicability==='full'))assert(event.seat,'selected member must occupy its existing seat');
  }
  assert(!result.events.some((event)=>event.kind==='proper-choice'&&control.ownedChoiceIds.includes(event.id)));
  executions++;
 }
});
const lent=relationMasses.find((mass)=>mass.key==='lent-3');const lentRel=lent.proper_source_paths[0];
const optional=lentRel.paths.find((one)=>one.id==='optional-material-a-gospel-longer');
const base=()=>context(lent,lentRel,'B',optional.id);const lentRows=rowsFor(lent,'main');
test('multiple paths stay required, source standing/order never appoint a celebration',()=>{
 const unselected=S.prepareProperAppointments(lentRows,context(lent,lentRel,'B'));
 assert.equal(unselected.sourcePathSelections[scoped(lentRel)].state,'required');assert.equal(unselected.sourcePathUnresolved.length,1);
 assert.equal(Object.keys(unselected.materialSelections).length,0);
 assert(!unselected.rows.some((row)=>row.proper.source_path_relation));
});
test('tuples cannot mix coupled roles or select a role without the complete declared path',()=>{
 const mixed=base();mixed.choices['main/gospel']='shorter';assert.throws(()=>S.prepareProperAppointments(lentRows,mixed),/mix incompatible/);
 const partial=context(lent,lentRel,'B');partial.choices['main/gospel']='longer';assert.throws(()=>S.prepareProperAppointments(lentRows,partial),/complete selected source path/);
 const wrong=base();wrong.calendarCycles.sunday='A';assert.throws(()=>S.prepareProperAppointments(lentRows,wrong),/inapplicable/);
 const stale=base();stale.choices[scoped(lentRel)]='stale';assert.throws(()=>S.prepareProperAppointments(lentRows,stale),/not held/);
});
test('exact members refuse duplicate coordinates, wrong owners, missing appointments and forged guards',()=>{
 for(const mutate of [
  (rel)=>rel.paths[0].members.push(copy(rel.paths[0].members[0])),
  (rel)=>{rel.paths[0].members[0].appointment.mass='wrong-owner';},
  (rel)=>{rel.paths[0].members[0].appointment.occurrence=999;},
  (rel)=>{rel.paths[0].members[0].material_cycle.cycle='D';}
 ]){const relation=copy(lentRel);mutate(relation);assert.throws(()=>S.prepareProperAppointments(lentRows,{...base(),sourcePaths:[relation]}),/duplicate|foreign|missing|not held/);}
 const rows=copy(lentRows);rows.find((row)=>row.proper.source_path_relation).proper.source_path_relation='wrong-relation';
 assert.throws(()=>S.prepareProperAppointments(rows,base()),/guard|membership/);
 const forged=copy(lentRows);forged.find((row)=>row.proper.source_path_relation).proper.name='Gospel';
 assert.throws(()=>S.prepareProperAppointments(forged,base()),/appointment/);
});
test('a relation owns the complete actual-group extent, including unselected alternatives',()=>{
 const rows=copy(lentRows);const extra=copy(rows.find((row)=>row.proper.ordinary_disposition&&row.proper.ordinary_disposition.group==='gospel'));
 extra.sourceIndex=999;extra.proper.ordinary_disposition.option='forged-extra';extra.proper.appointment_identity.occurrence=999;delete extra.proper.source_path_relation;rows.push(extra);
 assert.throws(()=>S.prepareProperAppointments(rows,base()),/complete raw extent/);
});
test('all inactive source cycles and body states validate before path selection',()=>{
 const malformed=copy(lentRows);malformed.find((row)=>row.proper.source_path_relation).proper.cycles.D={citations:[{ref:'unheld'}]};
 assert.throws(()=>S.prepareProperAppointments(malformed,base()),/unsupported Lectionary/);
 const both=copy(lentRows);both.find((row)=>row.proper.source_path_relation).proper.weekday_cycles={I:{citations:[{ref:'unheld'}]}};
 assert.throws(()=>S.prepareProperAppointments(both,base()),/both Sunday and weekday/);
 const broken=copy(structure);const brokenMass=broken.masses.find((mass)=>mass.key==='lent-3');
 const inactive=brokenMass.propers.find((proper)=>proper.source_path_relation&&proper.ordinary_disposition&&proper.ordinary_disposition.option==='shorter');
 inactive.cycles[Object.keys(inactive.cycles)[0]].text_status={state:'unavailable',scope:'wrong-body'};
 const input=inputs(brokenMass,lentRel,'B',optional,false,'day');input.structure=broken;
 assert.throws(()=>A.adaptDay(input),/body|text_status|scope/);
});
test('unknown actual-use facts are applicability obligations, never a date, URL or body inference',()=>{
 const mass=relationMasses.find((one)=>one.key==='easter-6');const relation=mass.proper_source_paths[0];const selected=relation.paths.find((one)=>one.when);
 const supplied=context(mass,relation,selected.calendar_cycles.in[0],selected.id);const rows=rowsFor(mass,relation.form_id);
 assert.throws(()=>S.prepareProperAppointments(rows,supplied),/source-condition-unresolved/);
 assert.throws(()=>S.prepareProperAppointments(rows,{...supplied,conditionFacts:{[selected.when.fact]:null}}),/source-condition-unresolved/);
 assert.throws(()=>S.prepareProperAppointments(rows,{...supplied,conditionFacts:{[selected.when.fact]:!selected.when.is}}),/inapplicable/);
 assert.throws(()=>S.prepareProperAppointments(rows,{...supplied,conditionFacts:{[selected.when.fact]:'true'}}),/boolean/);
 assert(S.prepareProperAppointments(rows,{...supplied,conditionFacts:{[selected.when.fact]:selected.when.is}}).sourcePathSelections[scoped(relation)].state==='selected');
 for(const malformed of [null,false,0,'',[]]){
  assert.throws(()=>S.prepareProperAppointments(rows,{...supplied,conditionFacts:malformed}),/boolean/);
  const badInput=inputs(mass,relation,selected.calendar_cycles.in[0],selected,false,'day');badInput.conditionFacts=malformed;
  assert.throws(()=>A.adaptDay(badInput),/boolean/);
  assert.throws(()=>S.prepareProperAppointments(rows,{...supplied,calendarCycles:malformed}),/calendar cycle/);
  assert.throws(()=>S.prepareProperAppointments(rows,{...supplied,sourcePaths:malformed}),/relation list|relation membership/);
 }
 const propers={...supplied,entrance:'propers',calendarCycles:{}};assert.throws(()=>S.prepareProperAppointments(rows,propers),/source-condition-unresolved/);
 const unselected=context(mass,relation,selected.calendar_cycles.in[0]);const result=S.prepareProperAppointments(rows,unselected);
 assert(result.sourcePathUnresolved.length);assert.equal(result.unresolved.length,0);
});
test('condition facts require own properties even for prototype-named or inherited valid identifiers',()=>{
 const owner='contract-owner',rel='contract-condition',coordinate=(proper)=>({mass:owner,form_id:'main',proper,occurrence:1});
 const rows=['Gospel','Gospel (optional)'].map((name)=>({name,form_id:'main',source:'composed',text:'Contract-only body.',appointment_identity:coordinate(name),source_path_relation:rel}));
 function supplied(fact,conditionFacts){return{calendar:structure.calendar,mass:owner,formId:'main',entrance:'day',calendarCycles:{sunday:'B'},conditionFacts,
  sourcePaths:[{id:rel,form_id:'main',source_edition:structure.calendar,basis:'Contract-only source condition proof.',paths:[
   {id:'principal',standing:'principal',calendar_cycles:{family:'sunday',in:['B']},choices:{},members:[{appointment:coordinate('Gospel'),material_cycle:{family:null,cycle:'all'}}]},
   {id:'optional',standing:'optional',calendar_cycles:{family:'sunday',in:['B']},choices:{},members:[{appointment:coordinate('Gospel (optional)'),material_cycle:{family:null,cycle:'all'}}],when:{fact,is:true}}
  ]}]};}
 for(const fact of ['constructor','technical-actual-use']){
  for(const facts of [{},Object.create(null),Object.create({[fact]:true}),Object.create({[fact]:false})]){
   const context=supplied(fact,facts),result=S.prepareProperAppointments(rows,context);
   assert.equal(result.sourcePathSelections['main/'+rel].state,'required');assert.equal(result.sourcePathAvailability['main/'+rel].optional.state,'unresolved');assert.equal(Object.keys(result.materialSelections).length,0);
   assert.throws(()=>S.prepareProperAppointments(rows,{...context,choices:{['main/'+rel]:'optional'}}),/source-condition-unresolved/);
  }
  const ownFalse=S.prepareProperAppointments(rows,supplied(fact,{[fact]:false}));assert.equal(ownFalse.sourcePathSelections['main/'+rel].option,'principal');
  const known=S.prepareProperAppointments(rows,{...supplied(fact,{[fact]:true}),choices:{['main/'+rel]:'optional'}});assert.equal(known.sourcePathSelections['main/'+rel].option,'optional');
 }
 assert.throws(()=>S.prepareProperAppointments(rows,supplied('__proto__',{})),/source-owned boolean fact/);
});
test('pure-path foreign and raw unprepared rows refuse before placeholder predicates',()=>{
 assert.throws(()=>S.unframedEvents(lentRows,()=>true),/must be prepared/);
 const pure=copy(lentRows.find((row)=>row.proper.source_path_relation&&!row.proper.ordinary_disposition));assert(pure);
 pure.proper.appointment_applicability={state:'unresolved',reason:'foreign-source-applicability',source_edition:structure.calendar,target_edition:'roman-pre-1955',basis:'Exact inherited source relation remains unsupported in target edition.'};
 for(const predicate of [null,()=>true])assert.throws(()=>S.unframedEvents([pure],predicate),/foreign-source|unsupported.*applicability/);
 const foreign=copy(lentRel);foreign.source_edition='foreign-edition';assert.throws(()=>S.prepareProperAppointments(lentRows,{...base(),sourcePaths:[foreign]}),/foreign-source/);
});
test('two Easter Day relations remain independent and Holy Family Gospel keeps its own source options',()=>{
 const easter=relationMasses.find((mass)=>mass.key==='easter-sunday');assert.equal(easter.proper_source_paths.length,2);
 const request=inputs(easter,easter.proper_source_paths[0],'B',easter.proper_source_paths[0].paths[0],false,'propers');
 const result=A.adaptPropers(request);assert.equal(result.sourcePathChoices.length,2);assert(result.sourcePathChoices.some((one)=>one.selection.state==='required'));
 const holy=relationMasses.find((mass)=>mass.key==='holy-family');const rel=holy.proper_source_paths[0];const input=inputs(holy,rel,'B',rel.paths.find((one)=>one.id==='common'),false,'day');
 const chosen=A.adaptDay(input);assert(chosen.events.some((event)=>event.kind==='proper-choice'&&event.group==='gospel'));
});
let cliCases=0;
test('CLI raw guard presence is checked unconditionally before any source projection',()=>{
 // Minimal public transport fixture; these are contract-only words and owner
 // coordinates, not a Missal source or a calendar appointment claim.
 const calendar='source-guard-contract';const key='contract';const date='2026-10-20';
 const proper={name:'Collect',form:null,form_id:'main',source:'composed',text:'Contract-only body.',citations:[],cycles:{},translations:[],taken_from:null};
 const model={calendar,masses:[{key,kind:'contract',propers:[copy(proper)]}]};
 const request={schema:C.STATE_SCHEMA,entrance:'day',civilDate:date,edition:{id:calendar},calendar:{id:calendar},
  bible:{id:'douay-rheims',numbering:'vulgate'},languages:{orations:'la'},requestedMode:'read',options:{ordinary:false,legitimate:{}},coverage:[],unresolvedChoices:[],sourceHooks:[]};
 const derived={calendar,date,weekday:'tuesday',liturgicalYear:{lectionary:null,anchors:{}},options:[{option:null,winner:{id:key,nature:'feast'},settled:true,readable:[{key,state:'said'}],absent:[]}]};
 const payload={date,scripture:{id:'douay-rheims'},days:[{calendar,selected_territory:null,settled:true,why:{lectionary:null},masses:[{key,standing:'said',selected_form:'main',bible:{id:'douay-rheims'},propers:[copy(proper)]}]}]};
 const input={request,derived,structure:model,payload};assert.equal(A.adaptCli(input).events.length,1);
 for(const malformed of [null,false,'']){
  const changed=copy(payload);changed.days[0].masses[0].propers[0].source_path_relation=malformed;
  assert.throws(()=>A.adaptCli({...input,payload:changed}),/order disagrees|source.*metadata/);cliCases++;
 }
});
if(process.env.TRIPTYCH_SOURCE_PATH_CLI_PAYLOAD){
 test('actual CLI preserves exact raw guard presence before filtering and exact admitted material metadata',()=>{
  const payload=JSON.parse(fs.readFileSync(process.env.TRIPTYCH_SOURCE_PATH_CLI_PAYLOAD));
  const day=payload.days.find((one)=>one.calendar===structure.calendar);
  const mass=relationMasses.find((one)=>one.key==='lent-3');const relation=mass.proper_source_paths[0];
  const projected=day.masses.find((one)=>one.key===mass.key);const selected=relation.paths.find((one)=>one.id===projected.source_path_selections[scoped(relation)].option);
  const input=inputs(mass,relation,day.why.lectionary.sunday,selected,true,'day');
  input.request.civilDate=payload.date;input.request.languages={orations:'en',ordinary:'en'};
  input.derived.date=payload.date;input.derived.liturgicalYear.lectionary=day.why.lectionary;input.payload=payload;
  const result=A.adaptCli(input);assert.equal(result.sourcePathChoices[0].selection.option,selected.id);
  const unowned=projected.propers.findIndex((proper)=>!Object.prototype.hasOwnProperty.call(proper,'source_path_relation'));assert(unowned>=0);
  for(const malformed of [null,false,'']){
   const changed=copy(payload);changed.days.find((one)=>one.calendar===structure.calendar).masses.find((one)=>one.key===mass.key).propers[unowned].source_path_relation=malformed;
   assert.throws(()=>A.adaptCli({...input,payload:changed}),/order disagrees|source.*metadata/);cliCases++;
  }
  const inactive=projected.propers.findIndex((proper,index)=>proper.source_path_relation&&!Object.prototype.hasOwnProperty.call(projected.material_selections,String(index)));assert(inactive>=0);
  const stripped=copy(payload);delete stripped.days.find((one)=>one.calendar===structure.calendar).masses.find((one)=>one.key===mass.key).propers[inactive].source_path_relation;
  assert.throws(()=>A.adaptCli({...input,payload:stripped}),/order disagrees|source.*metadata/);cliCases++;
  const forged=copy(payload);const forgedMass=forged.days.find((one)=>one.calendar===structure.calendar).masses.find((one)=>one.key===mass.key);
  const first=Object.keys(forgedMass.material_selections)[0];forgedMass.material_selections[first].cycle='C';
  assert.throws(()=>A.adaptCli({...input,payload:forged}),/material_selections.*disagrees/);cliCases++;
 });
}
assert.equal(JSON.stringify(structure),before,'raw source words/courses/provenance must remain unchanged');
process.stdout.write(JSON.stringify({status:'pass',groups:checks.length,executions,cliCases,checks})+'\n');
