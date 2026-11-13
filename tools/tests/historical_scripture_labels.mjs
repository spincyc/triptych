import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {createRequire} from 'node:module';
const root=path.resolve(process.argv[2] || path.join(import.meta.dirname,'../..'));
const require=createRequire(import.meta.url);
const {browserDataRoot}=require(path.join(root,'tools/tests/_product_data.cjs'));
const data=process.argv[3] || browserDataRoot(root);
const core=process.argv[4] || path.join(root,'src/web/browser/shared/browser-core.js');
const canonical=JSON.parse(fs.readFileSync(path.join(data,'structure/propers/postconciliar.json'))).masses
 .filter(m=>['christmas-december-30','christmas-december-31'].includes(m.key))
 .map(m=>({mass:m.key,proper:m.propers.find(p=>p.name==='Entrance Antiphon'&&p.form_id==='main')}));
assert.equal(canonical.length,2);
// 2026-11-13: the historical Lasance English for these two antiphons stayed in a
// private validation snapshot only; the reviewed canonical rows remain
// rights-withheld (workflows/reviews/modern-source-completion-2026-11-12/
// next-cohort-six/shared/qualification-addendum.json, "temporal" group,
// unrelated_experimental_rows_restored_only_in_private_snapshot). No held
// scripture-sourced English body exists, so the presentation and grade controls
// run on explicitly synthetic, never-published words over the real carriers.
const SYNTHETIC='synthetic.test-only.historical-scripture-witness';
function historicalSynthetic({mass,proper}){
 const held=structuredClone(proper),label='Synthetic historical English witness (test only, not published)';
 held.translations=[{lang:'en',rights:'public-domain',source_id:SYNTHETIC,source_label:label,
  caution:'Synthetic caution sentinel for '+mass+'.',text:'Synthetic historical scriptural sentinel for '+mass+'.'}];
 held.untranslated=[];held.unavailable_translations=[];
 held.languages=held.languages.map(r=>r.lang==='en'?{available:true,held:true,lang:'en',reason:null,status:'full-text'}:r);
 held.coverage.languages=held.coverage.languages.map(r=>r.lang!=='en'?r:{availability:'available',collation:'unresolved',lang:'en',
  publication_basis:'public-domain',relationship:'historical-antecedent',witnesses:[{aliases:[],collation:'unresolved',id:SYNTHETIC,
  label,publication_basis:'public-domain',relationship:'historical-antecedent',source_id:SYNTHETIC}]});
 return {mass,proper:held};
}
const source=process.argv[5] ? JSON.parse(fs.readFileSync(process.argv[5])) : canonical.map(historicalSynthetic);
assert.equal(source.length,2);
const dom=require(path.join(root,'scripts/lectern/dom.js'));
globalThis.window=globalThis;globalThis.document=dom.document;globalThis.location={search:'?data=/data',hash:'',pathname:'/probe.html'};
globalThis.addEventListener=()=>{};
globalThis.fetch=async url=>{
 const relative=new URL(String(url),'http://localhost').pathname.replace(/^\/data\//,'');
 const file=relative.includes('/chapters/')?path.join(root,'src/sources/bibles',relative):path.join(data,relative);
 const text=fs.readFileSync(file,'utf8');return {ok:true,status:200,json:async()=>JSON.parse(text),text:async()=>text};
};
vm.runInThisContext(fs.readFileSync(core,'utf8'),{filename:core});
const T=globalThis.Triptych,bible=JSON.parse(fs.readFileSync(path.join(data,'bibles.json'))).bibles.find(b=>b.id==='douay-rheims');
const clone=value=>structuredClone(value),reports=[],withheld=[];
for(const {mass,proper} of canonical){
 const coverage=proper.coverage.languages.find(r=>r.lang==='en');
 assert.equal(coverage.publication_basis,'restricted',mass);assert.equal(coverage.availability,'not-publishable',mass);
 assert.ok(!(proper.translations||[]).some(t=>t.lang==='en'),mass);
 const fragments=await T.fetchFragments(bible,proper.citations);
 for(const textDisplay of ['selected','latin-and-selected']){
  const node=T.renderProper(proper,bible,fragments,{orations:'en',textDisplay});
  assert.equal(node.querySelector('.composed'),null,mass);
  assert.ok(!node.textContent.includes('Historical scriptural text'),mass);
 }
 withheld.push(mass);
}
for(const {mass,proper} of source){
 assert.equal(proper.source,'scripture');assert.equal(proper.text,null);
 const english=proper.translations.find(t=>t.lang==='en'),coverage=proper.coverage.languages.find(r=>r.lang==='en');
 assert.equal(coverage.relationship,'historical-antecedent');assert.equal(coverage.publication_basis,'public-domain');
 assert.equal(proper.coverage.languages.find(r=>r.lang==='la').relationship,'bible-reconstruction');
 assert.equal(proper.coverage.scripture_component.relationship,'bible-reconstruction');
 const snapshot=JSON.stringify(proper),fragments=await T.fetchFragments(bible,proper.citations);
 for(const textDisplay of ['selected','latin-and-selected']){
  const node=T.renderProper(proper,bible,fragments,{orations:'en',textDisplay});
  const body=node.querySelector('.composed'),label=body.querySelector('.composed-label').textContent;
  assert.equal(label,'Historical scriptural text · English');
  assert.equal(body.childNodes.slice(1).map(n=>n.textContent).join(''),english.text);
  assert.ok(node.textContent.includes(english.source_label));assert.ok(node.textContent.includes(english.caution));
  assert.ok(!node.textContent.includes('Composed text — not scripture'));
  assert.equal(node.querySelector('.unit-claim').getAttribute('data-unit-claim'),'bible-reconstruction');
  assert.ok(node.querySelector('.citation').textContent.trim());
  assert.notEqual(node.querySelector('.citation').textContent,english.text);
  const blocks=dom.read(node),runs=blocks.flatMap(b=>b.runs);
  assert.ok(runs.some(r=>r.classes.includes('composed-label')&&r.text===label));
  assert.ok(runs.some(r=>r.classes.includes('translation-qualification')));
  const study=dom.read(T.translationCredits(T.orationFor(proper,'en'),{expanded:true}));
  assert.ok(study.flatMap(b=>b.runs).some(r=>r.text===english.caution));
  if(textDisplay==='latin-and-selected'){
   const sides=node.querySelectorAll('.text-side');
   const en=sides.find(n=>n.getAttribute('data-text-language')==='en');
   const la=sides.find(n=>n.getAttribute('data-text-language')==='la');
   assert.equal(en.getAttribute('data-text-relationship'),'historical-antecedent');
   assert.equal(en.getAttribute('data-text-rights'),'public-domain');
   assert.equal(la.getAttribute('data-text-relationship'),'bible-reconstruction');
   assert.equal(la.querySelector('.composed'),null);
  }
  reports.push({mass,textDisplay,label,sourceGrade:coverage.relationship,bibleSeparate:true,bodyUnchanged:true,creditsUnchanged:true,terminalRuns:true});
 }
 assert.equal(JSON.stringify(proper),snapshot);
 const latin=T.renderProper(proper,bible,fragments,{orations:'la'});
 assert.equal(latin.querySelector('.composed'),null);
 assert.equal(latin.querySelector('.unit-claim').getAttribute('data-unit-claim'),'bible-reconstruction');
}
const original=source[0].proper,fragment=await T.fetchFragments(bible,original.citations);
const controls=[
 ['exact-target',p=>{const r=p.coverage.languages.find(r=>r.lang==='en');r.relationship='exact-target';r.witnesses[0].relationship='exact-target';},'Scriptural text'],
 ['study-translation',p=>p.coverage.languages.find(r=>r.lang==='en').witnesses[0].relationship='study-translation','Scriptural text'],
 ['missing-coverage',p=>delete p.coverage,'Scriptural text'],
 ['unknown-witness',p=>p.translations[0].source_id='unclassified-witness','Scriptural text'],
 ['unnamed-witness',p=>delete p.translations[0].source_id,'Scriptural text'],
 ['witness-alias',p=>{const w=p.coverage.languages.find(r=>r.lang==='en').witnesses[0];w.aliases=[w.id];w.id='canonical-alias';delete w.source_id;},'Historical scriptural text'],
 ['mixed',p=>p.source='mixed','Missal text'],
 ['composed',p=>p.source='composed','Composed text — not scripture']
];
for(const [name,mutate,label] of controls){const proper=clone(original);mutate(proper);const node=T.renderProper(proper,bible,fragment,{orations:'en'});assert.equal(node.querySelector('.composed-label').textContent,label+' · English',name);}
console.log(JSON.stringify({status:'pass',presentations:reports,latinNoBody:2,gradeControls:controls.map(r=>r[0]),canonicalWithheld:withheld,canonicalWrites:false}));
