import assert from 'node:assert/strict';import fs from 'node:fs';import path from 'node:path';import {createRequire} from 'node:module';import vm from 'node:vm';
const root=path.resolve(process.argv[2] || path.join(import.meta.dirname, '../..'));const require=createRequire(import.meta.url);const A=require(root+'/src/web/browser/liturgy/reader-state-adapters.js'),M=require(root+'/src/web/browser/liturgy/assembly-model.js');const load=p=>JSON.parse(fs.readFileSync(root+'/'+p));const structure=load('src/web/data/structure/propers/roman-1962.json'),rubrics=load('src/web/data/structure/rubrics/roman-1962.json'),ordinary=load('src/web/data/structure/ordinary/roman-1962.json'),fixture=load('tools/tests/fixtures/liturgy-reader-state/v1/day-roman-1962-2026-08-02.json');const clone=v=>structuredClone(v);let checks=0,negative=0;
const requestFor=(date,mode='read',lang='en',witness=null)=>{const q=clone(fixture.requested);delete q.selectedReadableFormulary;q.civilDate=date;q.requestedMode=mode;q.options.ordinary=mode==='missal';q.languages.orations=lang;if(witness)q.languages.translationWitness=witness;else delete q.languages.translationWitness;return q;};
const derive=date=>M.derive({date,year:load('src/web/data/structure/calendar/roman-1962/'+date.slice(0,4)+'.json'),rubrics});
const adapt=(date,mode='read',lang='en',witness=null,s=structure)=>A.adaptDay({request:requestFor(date,mode,lang,witness),derived:derive(date),structure:s,ordinary:mode==='missal'?ordinary:null});
const bounded=result=>result.events.flatMap(e=>(e.orationGroups||[]).flatMap(g=>g.members)).filter(e=>e.executionSource);
for(const date of ['2026-06-30','2027-02-22','2028-02-22','2060-02-22'])for(const mode of ['read','missal']){
 const result=adapt(date,mode),sources=bounded(result);assert.equal(sources.length,3);assert.equal(result.executionSourceCoverage.petitions,3);assert.equal(result.executionSourceCoverage.whole_body_translations_added,0);assert.equal(result.executionSourceCoverage.complete_English_claim,false);
 for(const row of sources){assert.equal(row.selected.missing,true);assert.equal(row.selected.availability,'unavailable');assert.equal(row.selected.sourceId,null);assert.equal(row.selected.text,null);assert.equal(row.executionSource.source.source_text,structure.masses.find(m=>m.key===row.executionSource.source.target[0]).propers.find(p=>p.name===row.executionSource.source.target[2]).execution_sources[0].source_text);}
 assert.equal(result.executionSourceCoverage.unresolved,date.slice(5)==='02-22'?2:0);checks++;
}
for(const date of ['2026-02-22','2030-06-30','2026-06-29','2027-02-23','2027-01-25']){assert.equal(bounded(adapt(date)).length,0);negative++;}
assert.equal(bounded(adapt('2026-06-30','read','la')).length,0);negative++;
const withoutExecution=clone(structure);for(const mass of withoutExecution.masses)for(const proper of mass.propers)delete proper.execution_sources;
for(const date of ['2026-06-30','2027-02-22','2060-02-22']){
 const wholeBodyRows=result=>result.coverage.filter(row=>row.scope==='proper-translation:en');
 assert.deepEqual(wholeBodyRows(adapt(date)),wholeBodyRows(adapt(date,'read','en',null,withoutExecution)));checks++;
}
const lasance=structure.masses.find(m=>m.key==='commemoratione-s-pauli-apostoli').propers.find(p=>p.execution_sources).execution_sources[0].source_id;
const cummiskey=structure.masses.find(m=>m.key==='comm-s-petri-apostoli-2').propers[0].translations.find(t=>t.lang==='en').source_id;
assert.equal(bounded(adapt('2026-06-30','read','en',cummiskey)).length,0);negative++;
const explicit=bounded(adapt('2026-06-30','read','en',lasance));assert.equal(explicit.length,3);assert.ok(explicit.every(e=>e.executionSource.unresolved.includes('companion-English-unavailable-in-selected-witness')));checks++;
const sourceKey='commemoratione-s-pauli-apostoli';
const mutations=[
 s=>{s.masses.find(m=>m.key===sourceKey).propers.find(p=>p.execution_sources).execution_sources.push(clone(s.masses.find(m=>m.key===sourceKey).propers.find(p=>p.execution_sources).execution_sources[0]));},
 ...['source_text','source_id','source_sha256','target_latin_sha256','target_proof_sha256','method_id','lang','fixed_date','record_sha256','scope'].map(k=>s=>{s.masses.find(m=>m.key===sourceKey).propers.find(p=>p.execution_sources).execution_sources[0][k]='CORRUPTED';}),
 s=>{s.masses.find(m=>m.key===sourceKey).propers.find(p=>p.execution_sources).execution_sources[0].private_locator='PRIVATE';},
 s=>{s.masses.find(m=>m.key===sourceKey).propers.find(p=>p.execution_sources).execution_sources[0].ranges[0].end--;},
 ...['cue','family','proof_sha256','source_text'].map(k=>s=>{s.masses.find(m=>m.key===sourceKey).propers.find(p=>p.execution_sources).execution_sources[0].companion[k]='CORRUPTED';}),
 s=>{s.masses.find(m=>m.key===sourceKey).propers.find(p=>p.execution_sources).text+=' CHANGED';},
 s=>{s.masses.find(m=>m.key==='comm-s-petri-apostoli-2').propers[0].text+=' CHANGED';},
 s=>{s.masses.find(m=>m.key==='comm-s-petri-apostoli-2').propers[0].translations[0].text+=' CHANGED';}
];
for(const mutation of mutations){const s=clone(structure);mutation(s);assert.throws(()=>adapt('2026-06-30','read','en',null,s));negative++;}
// A missing finite source remains a whole-body English hold; it never borrows another source.
const missing=clone(structure);delete missing.masses.find(m=>m.key===sourceKey).propers.find(p=>p.execution_sources).execution_sources;assert.equal(bounded(adapt('2026-06-30','read','en',null,missing)).length,2);negative++;
// Actual shared renderer and native DOM adapter preserve the literal witness, without placing its cue in the petition.
const dom=require(root+'/scripts/lectern/dom.js');globalThis.document=dom.document;globalThis.window=globalThis;globalThis.location={search:'',hash:'',pathname:'/'};globalThis.history={replaceState(){},pushState(){}};globalThis.addEventListener=()=>{};vm.runInThisContext(fs.readFileSync(root+'/src/web/browser/shared/browser-core.js','utf8'));
for(const date of ['2026-06-30','2027-02-22','2060-02-22']){
 const result=adapt(date);for(const event of result.events.filter(e=>e.orationGroups)){
  const hook=event.sourceHooks.find(h=>h.kind==='proper-structure').id.split('/');const proper=structure.masses.find(m=>m.key===hook[1]).propers[Number(hook[2])-1];
  const node=Triptych.renderProper(proper,{},null,{orations:'en',eventId:event.id,structure,orationGroups:event.orationGroups,executionSource:event.executionSource||null});
  const rows=bounded({events:[event]});for(const row of rows){const source=row.executionSource.source;const petition=source.source_text.slice(0,source.ranges[0].end);assert.ok(node.textContent.includes(petition));assert.ok(node.textContent.includes('Historical witness ending: '+source.source_text.slice(source.ranges[2].start)));assert.ok(node.textContent.includes(source.source_text));}
  assert.ok(node.querySelector('.execution-source-apparatus').hasAttribute('data-copy'));assert.ok(dom.read(node).some(b=>b.runs.some(r=>r.text.includes('Historical witness ending:'))));checks++;
 }
}
// Study preserves the source/execution distinction, public proof hooks and separate coverage.
const Study=require(root+'/src/web/browser/liturgy/reader-study-view.js');
for(const date of ['2026-06-30','2027-02-22','2060-02-22']){
 const result=adapt(date,'missal'),facts=Study.project(result);
 assert.equal(facts.executionCoverage.petitions,3);assert.equal(facts.executionCoverage.whole_body_translations_added,0);assert.equal(facts.executionCoverage.complete_English_claim,false);
 const members=facts.events.flatMap(e=>(e.orationGroups||[]).flatMap(g=>g.members)).filter(e=>e.executionFacts);assert.equal(members.length,3);
 for(const member of members){assert.equal(member.executionFacts.disposition,'petition-only');assert.equal(member.selected.availability,'unavailable');assert.ok(member.sourceHooks.some(h=>h.id===member.executionFacts.publicationPassage));assert.ok(member.sourceHooks.some(h=>h.id===member.executionFacts.companionPublicationPassage));assert.equal('source_text'in member.executionFacts,false);}
 const fragment=document.createDocumentFragment();for(const event of result.events){const host=Triptych.el('section');host.dataset.semanticEventId=event.id;host.dataset.semanticLocation=event.id;fragment.appendChild(host);}
 Study.attach({result,fragment,contents:[]});assert.ok(fragment.textContent.includes('Execution-scoped historical petitions'));assert.ok(fragment.textContent.includes('Selected execution witness'));assert.ok(fragment.textContent.includes('Petition publication passage'));assert.ok(fragment.textContent.includes(members[0].executionFacts.publicationPassage));checks++;
 const changed=clone(result);changed.executionSourceCoverage.private_field='PRIVATE';assert.throws(()=>Study.project(changed),/closed execution coverage/);negative++;
 const principal=changed.events.find(e=>e.executionSource)||changed.events.find(e=>e.orationGroups).orationGroups[0].members[0];delete changed.executionSourceCoverage.private_field;principal.executionSource.private_field='PRIVATE';assert.throws(()=>Study.project(changed),/closed execution source/);negative++;
}
const choices=Triptych.executionWitnesses(adapt('2027-02-22'),[],'en');assert.equal(choices.length,1);assert.equal(choices[0].execution_sources,3);assert.equal(choices[0].whole_body_translations_added,0);checks++;
// Reach the range validator with a synthetic source-authority fixture, without widening production authority.
const instrumented=fs.readFileSync(root+'/src/web/browser/liturgy/reader-state-adapters.js','utf8').replace('    properEventId: properEventId,','    testSha: executionSha, testPins: EXECUTION_PUBLIC_PINS, testValidate: validateExecutionSource, properEventId: properEventId,');
const moduleFixture={exports:{}};vm.runInNewContext(instrumented,{module:moduleFixture,require:name=>require(path.resolve(root+'/src/web/browser/liturgy',name)),globalThis:{}});
const privateApi=moduleFixture.exports;assert.equal(privateApi.testSha('abc'),'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad');checks++;
const hostProper=structure.masses.find(m=>m.key===sourceKey).propers.find(p=>p.execution_sources),toy=clone(hostProper.execution_sources[0]);
toy.source_text='😀'+toy.source_text;toy.source_sha256=privateApi.testSha(toy.source_text);toy.ranges.forEach((range,index)=>{range.start+=index?2:0;range.end+=2;});toy.ranges[0].end=1;toy.ranges[1].start=1;
// Canonicalization includes nested keys; obtain it from a JSON source-only test closure.
function canonical(value){return Array.isArray(value)?'['+value.map(canonical).join(',')+']':value&&typeof value==='object'?'{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+canonical(value[k])).join(',')+'}':JSON.stringify(value);}
privateApi.testPins[JSON.stringify(toy.target)]=privateApi.testSha(canonical(toy));
const companionProper=structure.masses.find(m=>m.key===toy.companion.target[0]).propers.find(p=>p.name===toy.target[2]);
const group={kind:'inseparable',count:1,slot:toy.target[2],members:[{key:toy.target[0],proper:hostProper},{key:toy.companion.target[0],proper:companionProper}]};
assert.throws(()=>privateApi.testValidate(toy,hostProper,group,requestFor('2026-06-30'),structure),/source characters/);negative++;
if(process.argv[3]){
 const payload=JSON.parse(fs.readFileSync(process.argv[3],'utf8')),date=payload.date,language=process.argv[4]||'en';
 const request=requestFor(date,'missal',language),derived=derive(date);
 const browser=A.adaptDay({request,derived,structure,ordinary}),cli=A.adaptCli({request,derived,structure,payload});
 assert.deepEqual(cli.events,browser.events);assert.deepEqual(cli.executionSourceCoverage,browser.executionSourceCoverage);assert.deepEqual(cli.explicitAbsences,browser.explicitAbsences);checks++;
}
process.stdout.write(JSON.stringify({positive_checks:checks,rejected_controls:negative,source_contexts:6,whole_body_admissions:0})+'\n');
