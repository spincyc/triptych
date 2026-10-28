import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
const root=path.resolve(process.argv[2]||path.join(import.meta.dirname,'../..'));
const require=createRequire(import.meta.url);
const M=require(root+'/src/web/browser/liturgy/assembly-model.js');
const A=require(root+'/src/web/browser/liturgy/reader-state-adapters.js');
const S=require(root+'/src/web/browser/liturgy/ordinary-seating.js');
const load=relative=>JSON.parse(fs.readFileSync(root+'/'+relative,'utf8'));
const structure=load('src/web/data/structure/propers/roman-1962.json');
const rubrics=load('src/web/data/structure/rubrics/roman-1962.json');
const ordinary=load('src/web/data/structure/ordinary/roman-1962.json');
const fixture=load('tools/tests/fixtures/liturgy-reader-state/v1/day-roman-1962-2026-08-02.json');
const yearFor=date=>load('src/web/data/structure/calendar/roman-1962/'+date.slice(0,4)+'.json');
const clone=value=>JSON.parse(JSON.stringify(value));
const derive=date=>M.derive({date,year:yearFor(date),rubrics});
function requestFor(date,mode='read',language='la') {
 const request=clone(fixture.requested);delete request.selectedReadableFormulary;
 request.civilDate=date;request.requestedMode=mode;request.options.ordinary=mode==='missal';
 request.languages.orations=language;return request;
}
function adapt(date,mode='read',language='la',source=structure) {
 return A.adaptDay({request:requestFor(date,mode,language),derived:derive(date),structure:source,ordinary:mode==='missal'?ordinary:null});
}
function prayers(result) {return result.events.filter(e=>e.kind==='proper'&&e.orationGroups);}
function flat(result) {return prayers(result).flatMap(e=>e.orationGroups.flatMap(g=>g.members));}
function raw(member) {const hook=member.sourceHooks.find(h=>h.kind==='proper-structure').id.split('/');return structure.masses.find(m=>m.key===hook[1]).propers[Number(hook[2])-1];}
let checks=0;
for (const mode of ['read','missal']) for(const language of ['la','en']) {
 const result=adapt('2026-03-17',mode,language);
 assert.equal(prayers(result).length,3);assert.equal(flat(result).length,3);
 for(const event of prayers(result)) {const group=event.orationGroups[0];assert.equal(group.kind,'commemoration');assert.equal(group.conclusion_group,2);assert.equal(group.count,1);assert.equal(group.members[0].of_name,'S. Patricii Episcopi et Confessoris');assert.ok(['source-wording','unresolved'].includes(group.execution.state));}
 for(const member of flat(result)) if(language==='la')assert.equal(member.selected.text,raw(member).text);
 assert.equal(result.explicitAbsences.some(a=>a.reason==='intermediate-conclusion-spans-unbound'),false);checks++;
}
for(const date of ['2026-01-19','2026-03-04','2026-03-27','2026-10-21']) {
 const result=adapt(date);assert.equal(prayers(result).length,3);
 assert.ok(prayers(result).every(e=>e.orationGroups.length===2&&e.orationGroups.every(g=>g.conclusion_group===2)));
 assert.equal(result.explicitAbsences.filter(a=>a.reason==='intermediate-conclusion-spans-unbound').length,3);
 for(const member of flat(result))assert.equal(member.selected.text,raw(member).text);checks++;
}
const advent=derive('2026-12-03').options[0];
assert.equal(advent.orations.low_mass[1].source_key,'advent-1');
assert.equal(advent.readable.find(r=>r.key==='advent-1').state,'commemorated');
assert.ok(flat(adapt('2026-12-03')).every(member=>member.id.includes('/advent-1/')));checks++;
for(const date of ['2027-01-25','2027-02-22','2060-02-22','2026-06-30']) {
 const result=adapt(date);const groups=prayers(result).flatMap(e=>e.orationGroups).filter(g=>g.kind==='inseparable');
 assert.equal(groups.length,3);assert.ok(groups.every(g=>g.members.length===2&&g.count===1));
 for(const member of groups.flatMap(g=>g.members))assert.equal(member.selected.text,raw(member).text||null);checks++;
}
// A subordinate's conditional appointment uses the existing source fact domain.
for(const [date,key] of [['2025-05-11','ss-philippi-iacobi-apostolorum'],['2030-04-13','s-hermenegildi-martyris']]) {
 const result=adapt(date),members=flat(result).filter(member=>member.id.includes('/'+key+'/'));
 assert.equal(members.length,3);assert.ok(members.some(member=>member.sourceHooks.some(h=>h.kind==='proper-appointment')));
 for(const member of members)assert.equal(member.selected.text,raw(member).text||null);checks++;
}
const conditionalDay=derive('2025-05-11'),conditionalBranch=conditionalDay.options[0];
const conditionalMain=structure.masses.find(m=>m.key===conditionalBranch.orations.low_mass[0].source_key);
const conditionalContext={active:true,calendar:'roman-1962',mainKey:conditionalMain.key,date:conditionalDay.date,
 execution:conditionalBranch.oration_execution,series:conditionalBranch.orations.low_mass,season:null,
 facts:structure.proper_appointment_facts,owners:structure.masses.map(m=>({key:m.key,rows:m.propers.map((proper,sourceIndex)=>({proper,sourceIndex}))}))};
assert.throws(()=>S.orationPlan(conditionalMain.propers,conditionalContext),e=>e.code==='oration-source-slot-unbound');
assert.throws(()=>S.orationPlan(conditionalMain.propers,{...conditionalContext,facts:{}}),e=>e.code==='oration-source-context-unbound');checks++;
// Missing source, missing slot, duplicated slot and unsupported context refuse with typed reasons.
for(const mutation of [
 s=>s.masses.splice(s.masses.findIndex(m=>m.key==='s-patricii-episcopi-confessoris'),1),
 s=>{const m=s.masses.find(m=>m.key==='s-patricii-episcopi-confessoris');m.propers=m.propers.filter(p=>p.name!=='Secret');},
 s=>{const m=s.masses.find(m=>m.key==='s-patricii-episcopi-confessoris');m.propers.push(clone(m.propers.find(p=>p.name==='Collect')));},
 s=>{const m=s.masses.find(m=>m.key==='lent-4-tuesday');m.propers=m.propers.filter(p=>p.name!=='Collect');}
]) {const source=clone(structure);mutation(source);assert.throws(()=>adapt('2026-03-17','read','la',source),e=>typeof e.code==='string'&&e.context.scope==='oration-assembly');checks++;}
const context={active:true,calendar:'roman-1962',mainKey:'main',execution:derive('2026-03-17').options[0].oration_execution,
 series:[{position:1,source_key:'main'},{position:2,source_key:'feria',of:'feria',of_name:'Feria'}],
 owners:[{key:'main',rows:[]},{key:'feria',rows:[{proper:{name:'Collect',text:'FIRST',form_id:'main'},sourceIndex:0},{proper:{name:'Oratio',text:'LATER',form_id:'main'},sourceIndex:2},{proper:{name:'Secret',text:'S',form_id:'main'},sourceIndex:4},{proper:{name:'Postcommunion',text:'P',form_id:'main'},sourceIndex:6}]}]};
const rows=['Collect','First Lesson','Oratio','Epistle','Secret','Postcommunion'].map((name,sourceIndex)=>({proper:{name},sourceIndex}));
// The admitted form's actual source sequence determines the final pre-Epistle seat.
for(const [key,form,index] of [['lent-1-ember-wednesday','main',4],['lent-1-ember-saturday','longer',16],['lent-1-ember-saturday','shorter',29]]) {
 const held=structure.masses.find(m=>m.key===key).propers.map((proper,sourceIndex)=>({proper,sourceIndex})).filter(row=>row.proper.form_id===form);
 const result=S.orationPlan(held,{...context,mainKey:key,series:[{position:1,source_key:key},context.series[1]]});
 assert.equal(result[0].sourceIndex,index);assert.equal(result[0].groups[0].members[0].proper.text,'FIRST');checks++;
}
const plan=S.orationPlan(rows,context);assert.equal(plan[0].sourceIndex,2);assert.equal(plan[0].groups[0].members[0].proper.text,'FIRST');assert.equal(plan[0].groups[0].placement_locus,'RGMR 442-443');checks++;
assert.throws(()=>S.orationPlan(rows,{...context,calendar:'roman-pre-1955'}),e=>e.code==='unsupported-oration-context');
assert.deepEqual(S.orationPlan(rows,{...context,active:false}),[]);checks++;
assert.ok(adapt('2026-03-17').explicitAbsences.some(a=>a.reason==='source-name-placeholder-unbound'));checks++;
// A modern transfer reference inherited by a pre1955 year is not new authority.
const legacyYear=load('src/web/data/structure/calendar/roman-pre-1955/2021.json');
const legacyRubrics=load('src/web/data/structure/rubrics/roman-pre-1955.json');
const legacy=M.derive({date:'2021-05-15',year:legacyYear,rubrics:legacyRubrics});
assert.equal(legacy.options.length,1);assert.equal(legacy.options[0].oration_execution,undefined);checks++;
if(process.argv[3]) {
 const payload=JSON.parse(fs.readFileSync(process.argv[3]));const date=payload.date;
 const request=requestFor(date,'missal',process.argv[4]||'la');const derived=derive(date);
 const browser=A.adaptDay({request,derived,structure,ordinary});
 const cli=A.adaptCli({request,derived,structure,payload});
 assert.deepEqual(cli.events,browser.events);assert.deepEqual(cli.explicitAbsences,browser.explicitAbsences);
 const cliGroups=payload.days[0].masses.find(m=>m.key===cli.resolved.formulary).expanded_events.filter(e=>e.oration_groups);
 assert.equal(cliGroups.length,prayers(browser).length);
 for(const event of cliGroups) {const expected=prayers(browser).find(e=>e.id===event.id);assert.deepEqual(event.oration_groups.map(g=>g.members.map(m=>m.id)),expected.orationGroups.map(g=>g.members.map(m=>m.id)));}
 const bad=clone(payload);const owner=bad.days[0].masses.find(m=>m.standing==='commemorated');
 if(owner){const row=owner.propers.find(p=>p.name==='Collect');if(request.languages.orations==='en')row.language_selection.texts[0].text='DRIFT';else row.text='DRIFT';assert.throws(()=>A.adaptCli({request,derived,structure,payload:bad}),/disagrees|drifted|no exact/);}checks++;
}
process.stdout.write(JSON.stringify({checks,sourceContract:Boolean(rubrics.orations.execution)}));
