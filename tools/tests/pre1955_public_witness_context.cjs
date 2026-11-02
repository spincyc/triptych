// Pure function-level DOM controls. No browser, owner tool, or output generator.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const repo = path.resolve(__dirname, '../..');
const script = fs.readFileSync(path.join(repo, 'src/web/browser/shared/browser-core.js'), 'utf8');
function extract(name, next) {
  const start = script.indexOf('  function ' + name + '(');
  const end = script.indexOf(next, start);
  assert(start >= 0 && end > start);
  return script.slice(start, end);
}
class Node {
  constructor(tag, className, text) { this.tagName = tag; this.className = className; this.textContent = text || ''; this.children = []; this.attributes = {}; }
  appendChild(child) { this.children.push(child); }
  setAttribute(key, value) { this.attributes[key] = value; }
}
const sandbox = {
  SOURCE_LANGUAGE:'la',
  el:(tag, className, text) => new Node(tag, className, text),
  composedBody:(text) => new Node('div','composed',text),
  composedLabel:(text) => new Node('span','composed-label',text),
  languageName:(lang) => ({la:'Latin', en:'English'}[lang] || lang),
  absenceClause:(owner, lang) => ({lang,availability:'not-sourced',text:lang+' unavailable'}),
  coverageWitnessIdentity:(owner, lang, row) => row.source_id,
  coverageWitnessMatches:(owner, lang, wanted, row) => wanted === row.source_id,
};
vm.createContext(sandbox);
vm.runInContext(extract('properBodyUnavailable', '  /* ------------------------------------------------------------------------\n   * Claim-local truth') +
  extract('renderSingleOrationState', '  /** One labelled language side'), sandbox);
const context = {scope:'witness-state-only',label:'Bonn 2004 reimpressio of a conformed edition of about 1954',civil_date_authority:false};
const owner = {source:'composed',text:'Fixture Latin.',latin:{withheld:false,target_context:context,publication:{status:'permitted',basis:'public-domain'},provenance:{status:'collated',relationship:'editorial-projection-exact-to-target'}},translations:[{lang:'en',text:'Fixture English.',source_id:'passage.fixture.english'}]};
const render = (one, held) => {
  const container = new Node('section');
  sandbox.renderSingleOrationState(container, one, held || {orations:'la'}, null, null);
  return container;
};
const notes = (node) => node.children.filter(child => child.className === 'composed-note unit-witness-context');
let count = 0;
let shown = render(owner);
assert.equal(notes(shown).length,1);
assert.equal(notes(shown)[0].lang,'en');
assert.equal(notes(shown)[0].attributes['data-target-witness-context'],context.scope);
assert.match(notes(shown)[0].textContent,/no date-specific pre-1955 attribution/); count++;
shown = render(owner,{orations:'en'});
assert.equal(shown.children[0].textContent,'Fixture English.');
assert.equal(notes(shown).length,0); count++;
const noEnglish = structuredClone(owner); noEnglish.translations=[];
shown = render(noEnglish,{orations:'en'});
assert.equal(shown.children[0].textContent,'Fixture Latin.');
assert.equal(shown.children[0].attributes['data-unit-original'],'la');
assert.equal(notes(shown).length,1); count++;
shown = render(noEnglish,{orations:'en',separateOriginal:true});
assert.equal(notes(shown).length,0); count++;
const held = structuredClone(owner); held.text=null; held.latin.withheld=true;
assert.equal(notes(render(held)).length,0); count++;
const otherScope = structuredClone(owner); otherScope.latin.target_context.scope='generic-recension';
assert.equal(notes(render(otherScope)).length,0); count++;
const civilAuthority = structuredClone(owner); civilAuthority.latin.target_context.civil_date_authority=true;
assert.equal(notes(render(civilAuthority)).length,0); count++;
const plain = structuredClone(owner); delete plain.latin.target_context;
assert.equal(notes(render(plain)).length,0); count++;
for (const mutation of [
  one => { one.latin.target_context.artifact_id = 'artifact.fixture.private'; },
  one => { one.latin.target_context.extra = true; },
  one => { one.latin.target_context.label = ''; },
  one => { one.latin.target_context.civil_date_authority = 0; },
  one => { one.latin.provenance.status = 'identified'; },
  one => { one.latin.publication.status = 'withheld'; },
]) {
  const one = structuredClone(owner); mutation(one);
  assert.equal(notes(render(one)).length, 0); count++;
}
console.log(JSON.stringify({status:'pass',pure_ui_controls:count,scope:'Exact sealed render/selection function bytes; minimal DOM fixture; no generator or print-layout acceptance'}));
