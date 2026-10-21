'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../..'),mod=path.join(root,'src/web/browser/liturgy');
const S=require(path.join(mod,'ordinary-seating.js')),A=require(path.join(mod,'reader-state-adapters.js')),C=require(path.join(mod,'reader-state.js')),Model=require(path.join(mod,'assembly-model.js'));
const year=JSON.parse(fs.readFileSync(path.join(root,'src/web/data/structure/calendar/roman-1962/2026.json'))),rubrics=JSON.parse(fs.readFileSync(path.join(root,'src/web/data/structure/rubrics/roman-1962.json')));
const copy=(one)=>JSON.parse(JSON.stringify(one));const checks=[];function test(name,run){run();checks.push(name);}
const borrowed=['2026-12-01','2026-12-05','2026-12-09','2026-12-10','2026-12-12','2026-12-14','2026-12-15','2026-12-17','2026-12-22','2026-12-23'];
const own=['2026-11-29','2026-12-06','2026-12-13','2026-12-20'];
const unused=['2026-11-30','2026-12-02','2026-12-03','2026-12-04','2026-12-07','2026-12-08','2026-12-11','2026-12-21','2026-12-24'];
const factid='contract-advent-use',edition='roman-1962';
const fact={edition,values:['chant-present','chant-omitted'],usage_values:{'own-sunday':'chant-present','borrowed-feria':'chant-omitted'},basis:'Contract-only test; actual four source clauses are owned separately.'};
function owner(date){const derived=Model.derive({date,year,rubrics});const branch=derived.options[0];const readable=branch.readable.find((one)=>one.state==='said');return{derived,branch,readable};}
function mass(key){return{key,kind:'temporal',propers:['Gradual','Alleluia'].map((name)=>({name,form:null,form_id:'main',source:'composed',text:'Contract-only body '+name,citations:[],cycles:{},translations:[],taken_from:null,
 ...(name==='Alleluia'?{appointment_identity:{mass:key,form_id:'main',proper:name,occurrence:1},ordinary_disposition:{kind:'conditional',group:'contract-alleluia',basis:'Contract-only Advent conditional.',when:{fact:factid,in:['chant-present']}}}:{})}))};}
function evidence(input,m){return{calendar:input.derived.calendar,entrance:'day',branch:input.branch,readable:input.readable,mass:m,formId:'main'};}
function prepared(input,m,extra={}){return S.prepareProperAppointments(m.propers,{calendar:edition,entrance:'day',mass:m.key,date:input.derived.date,season:input.derived.season,facts:{[factid]:fact},usageContext:evidence(input,m),...extra});}
function req(date,m){return{schema:C.STATE_SCHEMA,entrance:'day',civilDate:date,edition:{id:edition},calendar:{id:edition},bible:{id:'douay-rheims',numbering:'vulgate'},languages:{orations:'la'},requestedMode:'read',options:{ordinary:false,legitimate:{}},coverage:[],unresolvedChoices:[],sourceHooks:[]};}
function structure(m){return{calendar:edition,proper_appointment_facts:{[factid]:fact},masses:[m]};}
let borrowedCases=0,ownCases=0;
test('the ten actual borrowed and four own Sunday canonical tuples control only the annotated chant',()=>{
 for(const date of borrowed.concat(own)){
  const input=owner(date),m=mass(input.readable.key),before=JSON.stringify(m),isBorrowed=borrowed.includes(date),expected=isBorrowed?'borrowed-feria':'own-sunday';
  assert.equal(S.projectProperUsage(evidence(input,m)),expected);const selected=prepared(input,m);assert.equal(selected.usage,expected);
  assert.equal(selected.rows.length,isBorrowed?1:2);assert.equal(selected.rows[0].proper.name,'Gradual');assert.equal(selected.inactive.length,isBorrowed?1:0);assert.equal(selected.unresolved.length,0);
  const result=A.adaptDay({request:req(date,m),derived:input.derived,structure:structure(m)});assert.equal(result.properAppointmentUsage,expected);assert.equal(result.events.length,isBorrowed?1:2);
  assert.equal(JSON.stringify(m),before);if(isBorrowed)borrowedCases++;else ownCases++;
 }
});
test('nine advertised unused formulas cannot inherit the winner context',()=>{
 for(const date of unused){const input=owner(date);assert(!['sunday','feria'].includes(input.branch.winner.nature));for(const offered of year.ferial_formulary[date]||[]){const m=mass(offered.key);assert.equal(S.projectProperUsage(evidence(input,m)),null);assert.equal(prepared(input,m).usage,null);}}
});
test('Ember Masses and separately selected commemorations never inherit borrowed Sunday use',()=>{
 for(const date of ['2026-12-16','2026-12-18','2026-12-19']){const input=owner(date);assert.equal(S.projectProperUsage(evidence(input,mass(input.readable.key))),null);}
 for(const date of ['2026-12-05','2026-12-10']){const input=owner(date);const comm=input.branch.readable.find((one)=>one.state==='commemorated');assert(comm);assert.equal(S.projectProperUsage({...evidence(input,mass(comm.key)),readable:comm}),null);}
});
test('borrowed provenance cannot suppress a post-Pentecost chant without a source disposition',()=>{
 const input=owner('2026-08-03'),m=mass(input.readable.key);assert.equal(S.projectProperUsage(evidence(input,m)),'borrowed-feria');
 delete m.propers[1].ordinary_disposition;delete m.propers[1].appointment_identity;
 const before=JSON.stringify(m);const held=prepared(input,m);assert.equal(held.rows.length,2);assert(!Object.prototype.hasOwnProperty.call(held,'usage'));assert.equal(JSON.stringify(m),before);
});
test('missing and partial owner tuples stay unknown without a new default or usage attestation',()=>{
 const input=owner(own[0]),m=mass(input.readable.key),original=evidence(input,m);
 const mutations=[e=>{delete e.branch.winner;},e=>{delete e.branch.candidates;},e=>{delete e.branch.readable;},e=>{delete e.branch.winner.formulary;},e=>{e.branch.settled=false;},e=>{e.branch.candidates.find(c=>c.id===e.branch.winner.id).rule=null;},e=>{e.readable.id='wrong-id';},e=>{e.readable.state='displaced';},e=>{e.mass.key='wrong-mass';},e=>{e.formId='wrong-form';},e=>{e.mass.forms=[{id:'other'}];},e=>{e.entrance='propers';},e=>{e.branch=Object.create(e.branch);},e=>{e.readable=Object.create(e.readable);},e=>{e.mass=Object.create(e.mass);},e=>{const candidate=e.branch.candidates.find(c=>c.id===e.branch.winner.id);candidate.rule=Object.create(candidate.rule);}];
 for(const mutate of mutations){const changed=copy(original);mutate(changed);assert.equal(S.projectProperUsage(changed),null);assert.equal(prepared(input,m,{usageContext:changed}).usage,null);}
 for(const date of [own[0],borrowed[0]]){
  const actual=owner(date),source=mass(actual.readable.key),positive=evidence(actual,source),expected=own.includes(date)?'own-sunday':'borrowed-feria';
  const mutations=[
   e=>e.branch.readable.push({state:'said'}),
   e=>e.branch.readable.push(Object.create({state:'said'})),
   e=>e.branch.readable.push({id:e.readable.id}),
   e=>e.branch.readable.push(Object.create(e.readable)),
   e=>e.branch.readable.push({...e.readable,state:'commemorated'}),
   e=>{e.branch.readable=e.branch.readable.map(r=>r.id===e.readable.id?{...r,state:'commemorated'}:r);},
   e=>e.branch.candidates.push({id:e.branch.winner.id}),
   e=>e.branch.candidates.push(Object.create(e.branch.candidates.find(c=>c.id===e.branch.winner.id))),
   e=>e.branch.candidates.push(copy(e.branch.candidates.find(c=>c.id===e.branch.winner.id))),
   e=>{e.mass.forms=[{id:'main'},Object.create({id:'main'})];},
   e=>{e.mass.forms=[{id:'main'},{id:'main'}];},
   e=>{e.mass.forms=[Object.create({id:'main'})];},
   e=>{e.branch.winner=Object.create(e.branch.winner);}
  ];
  for(const mutate of mutations){const changed=copy(positive);mutate(changed);assert.equal(S.projectProperUsage(changed),null);const unresolved=prepared(actual,source,{usageContext:changed});assert.equal(unresolved.usage,null);assert.equal(unresolved.inactive.length,0);assert.equal(unresolved.unresolved.length,1);}
  const unrelated=copy(positive);unrelated.branch.readable.push({state:'commemorated',id:'unrelated',key:'unrelated'});unrelated.branch.candidates.push({id:'unrelated'});unrelated.mass.forms=[{id:'main'},{id:'unrelated'}];assert.equal(S.projectProperUsage(unrelated),expected);
 }
 assert.equal(prepared(input,m,{usageContext:undefined,usage:'own-sunday'}).usage,null);
 const inherited=Object.assign(Object.create({usageContext:original}),{calendar:edition,entrance:'day',mass:m.key,date:input.derived.date,season:input.derived.season,facts:{[factid]:fact}});
 assert.equal(S.prepareProperAppointments(m.propers,inherited).usage,null);
 assert.equal(prepared(input,m,{usageContext:{...original,calendar:'wrong-edition'}}).usage,null);
 const request=req(own[0],m);request.usage='own-sunday';assert.throws(()=>A.adaptDay({request,derived:input.derived,structure:structure(m)}),/invalid Day/);
});
test('Propers remains date-free and unknown; restricted nonseason choices cannot establish actual use',()=>{
 const input=owner(own[0]),m=mass(input.readable.key),request=req(own[0],m);request.entrance='propers';request.civilDate=null;request.formulary={id:m.key,type:m.kind};delete request.calendar;
 const result=A.adaptPropers({request,structure:structure(m)});assert.equal(result.properAppointmentUsage,null);assert.equal(result.events.length,1);assert(result.unresolvedChoices.length);
 const rows=['Alleluia','Alleluia (alternative)'].map((name,i)=>({name,form_id:'main',source:'composed',text:'Contract-only alternative.',appointment_identity:{mass:m.key,form_id:'main',proper:name,occurrence:1},ordinary_disposition:{kind:'alternative',group:'contract-choice',option:i?'present':'principal',basis:'Contract-only choice.',anchor:{mass:m.key,form_id:'main',proper:'Alleluia',occurrence:1},when:{fact:factid,in:i?['chant-present']:['chant-present','chant-omitted']}}}));
 assert.throws(()=>S.prepareProperAppointments(rows,{calendar:edition,entrance:'propers',mass:m.key,facts:{[factid]:fact},choices:{'main/contract-choice':'present'}}),/unknown source use applicability/);
 assert.equal(S.prepareProperAppointments(rows,{calendar:edition,entrance:'propers',mass:m.key,facts:{[factid]:fact},choices:{'main/contract-choice':'principal'}}).selections['main/contract-choice'].option,'principal');
});
test('usage selector maps are closed, mutually exclusive and edition bound',()=>{
 const input=owner(own[0]),m=mass(input.readable.key);
 for(const mutate of [f=>{f.season_values={advent:'chant-present'};},f=>{f.usage_values.extra='chant-present';},f=>{delete f.usage_values['own-sunday'];},f=>{f.usage_values['borrowed-feria']=null;},f=>{f.usage_values['own-sunday']='unheld';},f=>{f.edition='roman-pre-1955';}]){const broken=copy(fact);mutate(broken);assert.throws(()=>prepared(input,m,{facts:{[factid]:broken}}),/fact is unheld|usage selector/);}
});
test('CLI derives usage independently from original Day owner and rejects mismatched or missing derived metadata',()=>{
 const date=borrowed[0],input=owner(date),m=mass(input.readable.key),request=req(date,m);
 const payload={date,scripture:{id:request.bible.id},days:[{calendar:edition,selected_territory:null,settled:true,why:{lectionary:null},masses:[{key:m.key,standing:'said',bible:{id:request.bible.id},selected_form:'main',proper_appointment_facts:{[factid]:copy(fact)},proper_appointment_usage:'borrowed-feria',propers:copy(m.propers)}]}]};
 const value={request,derived:input.derived,structure:structure(m),payload};assert.equal(A.adaptCli(value).properAppointmentUsage,'borrowed-feria');
 for(const usage of ['own-sunday',null,undefined]){const changed=copy(payload);if(usage===undefined)delete changed.days[0].masses[0].proper_appointment_usage;else changed.days[0].masses[0].proper_appointment_usage=usage;assert.throws(()=>A.adaptCli({...value,payload:changed}),/usage context disagrees/);}
 const derived=copy(input.derived);delete derived.options[0].candidates;assert.throws(()=>A.adaptCli({...value,derived}),/usage context disagrees/);
 const changed=copy(payload);changed.days[0].masses[0].proper_appointment_facts[factid].usage_values['borrowed-feria']='chant-present';assert.throws(()=>A.adaptCli({...value,payload:changed}),/appointment facts disagree/);
});
process.stdout.write(JSON.stringify({status:'pass',groups:checks.length,borrowedCases,ownCases,unusedCases:unused.length,checks})+'\n');
