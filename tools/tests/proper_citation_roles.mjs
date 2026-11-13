import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {createRequire} from 'node:module';
const root=path.resolve(process.argv[2]||path.join(import.meta.dirname,'../..')),require=createRequire(import.meta.url);
const data=process.argv[3]||require(path.join(root,'tools/tests/_product_data.cjs')).browserDataRoot(root);
const files=process.argv[4]||root;
const dom=require(path.join(files,'scripts/lectern/dom.js'));
globalThis.window=globalThis;globalThis.document=dom.document;globalThis.location={search:'?data=/data',hash:'',pathname:'/probe.html'};globalThis.addEventListener=()=>{};
globalThis.fetch=async url=>{const relative=new URL(String(url),'http://localhost').pathname.replace(/^\/data\//,'');const file=relative.includes('/chapters/')?path.join(root,'src/sources/bibles',relative):path.join(data,relative);const text=fs.readFileSync(file,'utf8');return{ok:true,status:200,json:async()=>JSON.parse(text),text:async()=>text};};
vm.runInThisContext(fs.readFileSync(path.join(files,'src/web/browser/shared/browser-core.js'),'utf8'));
const T=globalThis.Triptych,proper=process.argv[5]?JSON.parse(fs.readFileSync(process.argv[5])):JSON.parse(fs.readFileSync(path.join(data,'structure/propers/roman-1962.json'))).masses.find(m=>m.key==='palm-sunday').propers.find(p=>p.incipit==='Omnes collaudant nomen tuum'),snapshot=JSON.stringify(proper);
assert.deepEqual(proper.citations.map(c=>c.reading_role?.kind),['embedded-quotation','following-psalm']);
const bibles=JSON.parse(fs.readFileSync(path.join(data,'bibles.json'))).bibles,results=[];
function ordinaryCitations(node){return node.querySelectorAll('.citation').filter(n=>!n.closest('.source-citation-apparatus'));}
function sourceBodies(node){return node.querySelectorAll('.composed').map(n=>n.childNodes.slice(1).map(c=>c.textContent).join(''));}
for(const [lang,bibleId,display] of [['en','douay-rheims','selected'],['la','clementine-vulgate','selected'],['en','douay-rheims','latin-and-selected']]){
 const bible=bibles.find(b=>b.id===bibleId),fragments=await T.fetchFragments(bible,proper.citations);
 const node=T.renderProper(proper,bible,fragments,{orations:lang,textDisplay:display});
 assert.equal(ordinaryCitations(node).length,1);
 const apparatus=node.querySelector('.source-citation-apparatus');assert.ok(apparatus);assert.equal(apparatus.hasAttribute('open'),false);
 assert.ok(apparatus.querySelector('summary').textContent.includes('Matthew 21:9'));
 assert.equal(apparatus.getAttribute('data-copy'),'skip');assert.equal(apparatus.getAttribute('data-citation-source'),proper.citations[0].reading_role.source_id);
 assert.ok(ordinaryCitations(node)[0].textContent.includes(lang==='la'?'Lauda':'Praise'));
 assert.ok(node.querySelector('.unit-claim').textContent.includes('target Missal wording not established'));
 assert.ok(node.querySelector('.unit-claim').textContent.includes(bible.label || bible.id));
 assert.ok(node.querySelector('.unit-claim').textContent.includes('Doxology and antiphon repetition are not supplied'));
 assert.deepEqual(sourceBodies(node),display==='latin-and-selected'?[proper.text,proper.translations[0].text]:[lang==='la'?proper.text:proper.translations[0].text]);
 const terminal=dom.read(node).flatMap(b=>b.runs).map(r=>r.text).join('');
 const bibleQuote=apparatus.querySelector('.citation').textContent;
 assert.ok(!terminal.includes(bibleQuote));assert.ok(!terminal.includes(lang==='la'?'turbæ autem':'And the multitudes'));
 assert.ok(terminal.includes('Matthew 21:9'));assert.ok(terminal.includes('target Missal wording not established'));
 results.push({language:lang,display,visibleCitations:1,embeddedReferenceRetained:true,terminalDuplicateSuppressed:true,exactBodiesUnchanged:true});
 for(const mode of ['missing-body','missing-roles']){
  const changed=structuredClone(proper);
  if(mode==='missing-body'){changed.text=null;changed.translations=[];}else changed.citations.forEach(c=>delete c.reading_role);
  const other=T.renderProper(changed,bible,fragments,{orations:lang,textDisplay:display});
  assert.equal(other.querySelector('.source-citation-apparatus'),null);assert.equal(ordinaryCitations(other).length,2);
 }
}
assert.equal(JSON.stringify(proper),snapshot);
const controls=[['unknown-kind',r=>r.kind='hide'],['missing-source',r=>delete r.source_id],['blank-locus',r=>r.locus=' '],['extra-key',r=>r.complete=true],['wrong-schema',r=>r.schema='v2'],['not-a-psalm',r=>r.kind='following-psalm']];
const bible=bibles.find(b=>b.id==='douay-rheims'),fragments=await T.fetchFragments(bible,proper.citations);
for(const [name,mutate] of controls){const changed=structuredClone(proper);mutate(changed.citations[0].reading_role);assert.throws(()=>T.renderProper(changed,bible,fragments,{orations:'en'}),/invalid source-owned Proper citation role/,name);}
for(const kind of [undefined,'scripture','composed']){const changed=structuredClone(proper);changed.source=kind;assert.throws(()=>T.renderProper(changed,bible,fragments,{orations:'en'}),/invalid source-owned Proper citation role/);}
console.log(JSON.stringify({status:'pass',presentations:results,missingBodyAndRoleControls:6,malformedRolesRefused:9,canonicalWrites:false}));
