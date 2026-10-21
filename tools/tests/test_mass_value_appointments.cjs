'use strict';
const assert=require('node:assert/strict');const path=require('node:path');const fs=require('node:fs');
const root=path.resolve(__dirname,'../..');const S=require(path.join(root,'src/web/browser/liturgy/ordinary-seating.js'));
const A=require(path.join(root,'src/web/browser/liturgy/reader-state-adapters.js'));const C=require(path.join(root,'src/web/browser/liturgy/reader-state.js'));
const copy=(one)=>JSON.parse(JSON.stringify(one));const checks=[];function test(name,fn){fn();checks.push(name);}
const edition='roman-1962',common='contract-common',key='contract-widow',group='contract-reading',factid='contract-subject';
const coord=(proper)=>({mass:common,form_id:'main',proper,occurrence:1});
const propers=['Lesson','Lesson (alternative)'].map((name,index)=>({name,form:null,form_id:'main',source:'composed',text:'Contract-only body.',citations:[],cycles:{},translations:[],taken_from:null,
 appointment_identity:coord(name),ordinary_disposition:{kind:'alternative',group,option:index?'pro-vidua':'principal',basis:'Contract-only source basis.',anchor:coord('Lesson'),seat:'reading-1',when:{fact:factid,in:index?['widow']:['general','widow']}}}));
const fact={edition,values:['general','widow'],mass_values:{[key]:{value:'widow',basis:'Contract-only exact source heading and referral.'}},basis:'Contract-only source subject fact.'};
const structure={calendar:edition,proper_appointment_facts:{[factid]:fact},masses:[{key:common,kind:'common',propers:copy(propers)},{key,kind:'feast',propers:copy(propers)}]};
const choice=(mass)=>'proper-choice/'+edition+'/'+mass+'/main/'+group;
function context(mass,choices){return{calendar:edition,entrance:'propers',mass,facts:structure.proper_appointment_facts,choices:choices||{}};}
function request(mass,option,entrance='propers'){
 const result={schema:C.STATE_SCHEMA,entrance,civilDate:entrance==='day'?'2026-10-20':null,edition:{id:edition},bible:{id:'douay-rheims',numbering:'vulgate'},languages:{orations:'la'},requestedMode:'read',options:{ordinary:false,legitimate:{}},coverage:[],unresolvedChoices:[],sourceHooks:[]};
 if(entrance==='propers')result.formulary={id:mass,type:mass===common?'common':'feast'};else result.calendar={id:edition};
 if(option)result.properChoices={[choice(mass)]:option};return result;
}
function derived(mass){return{calendar:edition,date:'2026-10-20',weekday:'tuesday',season:'lent',liturgicalYear:{lectionary:null,anchors:{}},options:[{option:null,winner:{id:mass,nature:'feast'},settled:true,readable:[{key:mass,state:'said'}],absent:[]}]};}
function event(result){return result.events.find((one)=>one.kind==='proper-choice'&&one.group===group);}
test('a positive exact source Mass binding leaves both principal and widow readings optional',()=>{
 const prepared=S.prepareProperAppointments(propers,context(key));assert.deepEqual(prepared.selections['main/'+group],{state:'required',option:null});
 assert.equal(prepared.rows.length,2);for(const option of ['principal','pro-vidua'])assert.equal(S.prepareProperAppointments(propers,context(key,{['main/'+group]:option})).selections['main/'+group].option,option);
});
test('an unbound Common remains unknown and cannot establish widow eligibility by explicit selection',()=>{
 assert.equal(S.prepareProperAppointments(propers,context(common)).selections['main/'+group].state,'required');
 assert.throws(()=>S.prepareProperAppointments(propers,context(common,{['main/'+group]:'pro-vidua'})),/unknown source Mass eligibility/);
 assert.equal(S.prepareProperAppointments(propers,context(common,{['main/'+group]:'principal'})).selections['main/'+group].option,'principal');
 assert.throws(()=>S.prepareProperAppointments(propers,context('contract-not-widow-by-label',{['main/'+group]:'pro-vidua'})),/unknown source Mass eligibility/);
});
test('source Mass bindings use the validated object on Day and Propers without a date or URL fact',()=>{
 for(const entrance of ['day','propers']){
  const pending=entrance==='day'?A.adaptDay({request:request(key,null,entrance),derived:derived(key),structure}):A.adaptPropers({request:request(key),structure});
  assert.equal(event(pending).selection.state,'required');assert.equal(event(pending).options.length,2);
  for(const option of ['principal','pro-vidua']){
   const input={request:request(key,option,entrance),derived:derived(key),structure};const result=entrance==='day'?A.adaptDay(input):A.adaptPropers(input);assert.equal(event(result).selection.option,option);
  }
 }
 assert.throws(()=>A.adaptPropers({request:request(common,'pro-vidua'),structure}),/unknown source Mass eligibility/);
 assert.equal(event(A.adaptPropers({request:request(common,'principal'),structure})).selection.option,'principal');
});
test('selector and per-binding evidence have exact closed shapes and unknown is never a default',()=>{
 for(const mutate of [f=>{f.season_values={lent:'widow'};},f=>{delete f.mass_values;},f=>{f.mass_values[key]='widow';},f=>{f.mass_values[key].basis='';},f=>{f.mass_values[key].extra=true;},f=>{f.mass_values[key].value='unknown-value';},f=>{f.mass_values[key]=null;}]){
  const broken=copy(fact);mutate(broken);assert.throws(()=>S.prepareProperAppointments(propers,{...context(key),facts:{[factid]:broken}}),/fact is unheld, malformed/);
 }
 assert.throws(()=>S.prepareProperAppointments(propers,context({key})),/validated source Mass key/);
 const trap=copy(fact);trap.mass_values.undefined={value:'widow',basis:'Contract-only literal key, not an absent default.'};
 assert.throws(()=>S.prepareProperAppointments(propers,{...context(undefined,{['main/'+group]:'pro-vidua'}),facts:{[factid]:trap}}),/unknown source Mass eligibility/);
});
function payload(req){return{date:req.civilDate,scripture:{id:req.bible.id},days:[{calendar:edition,selected_territory:null,settled:true,why:{lectionary:null},masses:[{key,standing:'said',bible:{id:req.bible.id},selected_form:'main',proper_appointment_facts:copy(structure.proper_appointment_facts),propers:copy(propers)}]}]};}
test('CLI parity retains every mass selector binding value, basis and closed field',()=>{
 const req=request(key,'pro-vidua','day');const input={request:req,derived:derived(key),structure,payload:payload(req)};
 assert.equal(event(A.adaptCli(input)).selection.option,'pro-vidua');
 for(const mutate of [f=>{f.mass_values[key].basis='Changed source heading proof.';},f=>{f.mass_values[key].value='general';},f=>{delete f.mass_values[key];},f=>{f.mass_values[key].extra='unheld';},f=>{f.season_values={lent:'widow'};}]){
  const changed=copy(input.payload);mutate(changed.days[0].masses[0].proper_appointment_facts[factid]);assert.throws(()=>A.adaptCli({...input,payload:changed}),/appointment facts disagree/);
 }
});
test('CLI fact identity preserves object, array and primitive types at every closed mapping level',()=>{
 const req=request(key,'pro-vidua','day');const input={request:req,derived:derived(key),structure,payload:payload(req)};
 const pairs=(value)=>Object.keys(value).sort().map((name)=>[name,value[name]]);
 for(const level of ['binding','selector','fact','map']){
  const changed=copy(input.payload);const mass=changed.days[0].masses[0];const facts=mass.proper_appointment_facts;
  if(level==='binding')facts[factid].mass_values[key]=pairs(facts[factid].mass_values[key]);
  if(level==='selector')facts[factid].mass_values=pairs(facts[factid].mass_values);
  if(level==='fact')facts[factid]=pairs(facts[factid]);
  if(level==='map')mass.proper_appointment_facts=pairs(facts);
  assert.throws(()=>A.adaptCli({...input,payload:changed}),/appointment facts disagree/);
 }
 const explicit=copy(input.payload);explicit.days[0].masses[0].proper_appointment_facts[factid].mass_values[key].extra=undefined;
 assert.throws(()=>A.adaptCli({...input,payload:explicit}),/appointment facts disagree/);
});
test('unbound prototype-named Masses and inherited binding maps cannot establish source eligibility',()=>{
 for(const missing of ['constructor','__proto__']){
  const supplied=context(missing);assert.equal(S.prepareProperAppointments(propers,supplied).selections['main/'+group].state,'required');
  assert.equal(S.prepareProperAppointments(propers,{...supplied,choices:{['main/'+group]:'principal'}}).selections['main/'+group].option,'principal');
  assert.throws(()=>S.prepareProperAppointments(propers,{...supplied,choices:{['main/'+group]:'pro-vidua'}}),/unknown source Mass eligibility/);
 }
 const inherited=copy(fact);inherited.mass_values=Object.create({[key]:copy(fact.mass_values[key])});inherited.mass_values['contract-other']={value:'widow',basis:'Contract-only other positive key.'};
 const supplied={...context(key),facts:{[factid]:inherited}};
 assert.throws(()=>S.prepareProperAppointments(propers,{...supplied,choices:{['main/'+group]:'pro-vidua'}}),/unknown source Mass eligibility/);
 assert.equal(S.prepareProperAppointments(propers,{...supplied,choices:{['main/'+group]:'principal'}}).selections['main/'+group].option,'principal');
 const unowned=Object.create({[factid]:copy(fact)});assert.throws(()=>S.prepareProperAppointments(propers,{...context(key),facts:unowned}),/fact is unheld/);
});
test('static source gate validates both source candidates without choosing a reading',()=>{
 // Use the held frame vocabulary rather than making a new Lesson policy.
 const ordinary=JSON.parse(fs.readFileSync(path.join(root,'src/web/data/structure/ordinary/roman-1962.json')));
 const result=S.validateProperSeating(ordinary,propers,{calendar:edition,mass:key,form_id:'main',full:true,facts:structure.proper_appointment_facts});
 assert.equal(result.candidates,2);assert.equal(result.choice_groups,1);
});
process.stdout.write(JSON.stringify({status:'pass',groups:checks.length,checks})+'\n');
