#!/usr/bin/env node
/* Owner-level prayer language pairs; synthetic words never assert liturgical coverage. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createRequire } from 'node:module';
import vm from 'node:vm';
import test from 'node:test';

const ROOT = resolve(process.env.TRIPTYCH_REVIEW_ROOT || resolve(import.meta.dirname, '../..'));
const CANDIDATE = resolve(process.env.TRIPTYCH_LATIN_MODULE_ROOT || ROOT);
const BASELINE = process.env.TRIPTYCH_LATIN_BASELINE_ROOT;
const require = createRequire(import.meta.url);
const modulePath = (name) => resolve(CANDIDATE, 'src/web/browser/liturgy', name);
const State = require(modulePath('reader-state.js'));
const Adapters = require(modulePath('reader-state-adapters.js'));
const Compare = require(modulePath('reader-comparison.js'));
const Actions = require(modulePath('reader-share-print.js'));
const read = (name) => JSON.parse(readFileSync(resolve(ROOT, name), 'utf8'));

class Element {
  constructor(tag, text = '') {
    this.tagName = tag; this.nodeType = tag === '#text' ? 3 : 1;
    this.nodeValue = tag === '#text' ? text : null;
    this._text = tag === '#text' ? '' : text; this.children = [];
    this.className = ''; this.attrs = {}; this.lang = ''; this.hidden = false; this.style = {};
    this.classList = { add: (...names) => { this.className += ' ' + names.join(' '); },
      remove: (...names) => { this.className = this.className.split(' ').filter(one => !names.includes(one)).join(' '); }, toggle() {} };
  }
  appendChild(child) { this.children.push(child); return child; }
  append(...children) { children.forEach(child => this.appendChild(child)); }
  setAttribute(key, value) { this.attrs[key] = String(value); }
  getAttribute(key) { return this.attrs[key] ?? null; }
  addEventListener() {}
  querySelectorAll() { return []; }
  get lastChild() { return this.children.at(-1) || null; }
  get textContent() { return this.nodeValue ?? this._text + this.children.map(one => one.textContent).join(''); }
  set textContent(value) { this._text = String(value); this.children = []; }
  toJSON() { return { tag: this.tagName, text: this.nodeValue ?? this._text, class: this.className,
    attrs: this.attrs, lang: this.lang, hidden: this.hidden, children: this.children }; }
}
function runtime(root) {
  const document = { createElement: tag => new Element(tag), createTextNode: text => new Element('#text', text),
    createDocumentFragment: () => new Element('#fragment'), getElementById: () => null,
    addEventListener() {}, body: { classList: { toggle() {} } } };
  const window = { document, location: { search: '' }, addEventListener() {},
    OrdinarySeating: require(resolve(root, 'src/web/browser/liturgy/ordinary-seating.js')),
    LiturgyReaderStateAdapters: Adapters };
  const context = vm.createContext({ window, document, URLSearchParams, URL, console });
  for (const name of ['src/web/browser/shared/browser-core.js', 'src/web/browser/liturgy/day.js']) {
    vm.runInContext(readFileSync(resolve(root,name),'utf8'), context, { filename: name });
  }
  return { T: window.Triptych, Ordinary: window.TriptychOrdinaryRenderer };
}
const production = runtime(CANDIDATE);
const classes = (root, name) => {
  const out = [];
  function visit(node) { if (node.className.split(/\s+/).includes(name)) out.push(node); node.children.forEach(visit); }
  visit(root); return out;
};
const sides = node => classes(node,'text-side');
const json = node => JSON.stringify(node);
const bible = { id: 'douay-rheims', label: 'Douay-Rheims', language: 'en', numbering: 'vulgate' };
function owner(overrides = {}) { return { name: 'Collect', source: 'composed', text: 'Latin sentinel.',
  translations: [{ lang:'en', source_id:'witness-english', rights:'public-domain', text:'English sentinel.' }],
  latin: { withheld:false, publication:{basis:'public-domain'}, provenance:{source_id:'passage-latin',source_date:'Synthetic Latin witness'} },
  ...overrides }; }
const render = (proper, options = {}) => production.T.renderProper(proper,bible,new Map(), {orations:'en',textDisplay:'latin-and-selected',...options});
const structure = read('src/web/data/structure/propers/roman-1962.json');
const ordinary = read('src/web/data/structure/ordinary/roman-1962.json');
const context = Adapters.validationContext({ entrance:'propers', bibles:read('src/web/data/bibles.json'),
  properIndex:read('src/web/data/structure/propers/index.json'), ordinaryIndex:{calendars:[]},
  structures:{'roman-1962':structure} });
const identity = '#missal=roman-1962&type=seasonal&mass=pentecost&bible=douay-rheims&orations=en';
const normalize = hash => State.normalizeLegacy(State.parseLegacy('propers',hash), {context,
  defaults:{missal:'roman-1962',bible:'douay-rheims',orations:'la'}});

test('optional display preserves old hashes and validates explicit values and duplicate keys', () => {
  const old = normalize(identity);
  assert.equal(old.ok,true,JSON.stringify(old.errors)); assert.equal(Object.hasOwn(old.state,'textDisplay'),false);
  assert.doesNotMatch(State.serializeLegacy(old),/text-display/);
  for (const value of ['selected','latin-and-selected']) {
    const normalized=normalize(identity+'&text-display='+value);
    assert.equal(normalized.ok,true,JSON.stringify(normalized.errors));
    assert.equal(normalized.state.textDisplay,value);
    assert.deepEqual(normalize(State.serializeLegacy(normalized)).state,normalized.state);
  }
  for (const value of ['', 'parallel', '1']) assert.equal(normalize(identity+'&text-display='+value).ok,false);
  assert.equal(normalize(identity+'&text-display=selected&text-display=latin-and-selected').ok,false);
  for (const value of [null,{},[],false]) assert.equal(State.validateReaderState({...old.state,textDisplay:value}).ok,false);
});

test('browse projection preserves display state and rejects malformed values without a selected Mass', () => {
  const prepared={parsed:State.parseLegacy('propers','#text-display=latin-and-selected'),missal:'roman-1962',bible:'douay-rheims',orations:'en'};
  const result=Adapters.browseState(prepared,context);
  assert.equal(result.ok,true,JSON.stringify(result.errors)); assert.equal(result.state.textDisplay,'latin-and-selected');
  prepared.parsed=State.parseLegacy('propers','#text-display=bad');
  assert.equal(Adapters.browseState(prepared,context).ok,false);
});

test('paired held bodies keep separate language source and rights metadata; Latin selection appears once', () => {
  const p=owner(); const before=JSON.stringify(p); const node=render(p); const [latin,english]=sides(node);
  assert.equal(sides(node).length,2); assert.equal(latin.attrs['data-text-language'],'la');
  assert.equal(english.attrs['data-text-language'],'en');
  assert.equal(latin.attrs['data-text-source-id'],'passage-latin');
  assert.equal(english.attrs['data-text-source-id'],'witness-english');
  assert.equal(latin.attrs['data-text-rights'],'public-domain'); assert.equal(english.attrs['data-text-rights'],'public-domain');
  assert.match(latin.textContent,/Latin sentinel/); assert.doesNotMatch(latin.textContent,/English sentinel/);
  assert.match(english.textContent,/English sentinel/); assert.doesNotMatch(english.textContent,/Latin sentinel/);
  assert.equal((node.textContent.match(/Latin sentinel/g)||[]).length,1);
  assert.equal(classes(render(p,{orations:'la'}),'text-pair').length,0);
  assert.equal(JSON.stringify(p),before);
});

test('missing restricted and selected-witness gaps preserve held Latin without borrowing English', () => {
  for (const p of [owner({translations:[]}),owner({translations:[],unavailable_translations:[{lang:'en',state:'rights-restricted'}]}),owner()]) {
    const node=render(p,{translationWitness:p.translations.length?'other-witness':null});
    assert.match(sides(node)[0].textContent,/Latin sentinel/);
    assert.doesNotMatch(sides(node)[1].textContent,/English sentinel|Latin sentinel/);
    assert.match(sides(node)[1].textContent,/unavailable|selected witness/);
  }
});

test('a missing Latin body never suppresses held English and both missing sides stay explicit', () => {
  const p=owner({text:null,latin:{withheld:true,state:'rights-restricted'}});
  const node=render(p);
  assert.match(sides(node)[0].textContent,/Latin text unavailable.*not publishable/);
  assert.match(sides(node)[1].textContent,/English sentinel/);
  assert.equal(classes(node,'composed').length,1);
  const empty=render(owner({text:null,translations:[],latin:{withheld:true,state:'rights-restricted'},untranslated:[{lang:'en',state:'unavailable'}]}));
  assert.equal(classes(empty,'composed').length,0); assert.equal(classes(empty,'unit-absence').length,2);
});

test('multiple English witnesses remain unresolved while the Latin side remains readable', () => {
  const node=render(owner({translations:[{lang:'en',source_id:'w1',rights:'public-domain',text:'First choice.'},{lang:'en',source_id:'w2',rights:'public-domain',text:'Second choice.'}]}));
  assert.match(sides(node)[0].textContent,/Latin sentinel/);
  assert.match(sides(node)[1].textContent,/Choose a witness/);
  assert.doesNotMatch(node.textContent,/First choice|Second choice/);
});

test('held Pentecost Sequence preserves each language’s checked stanza count without inferred alignment', () => {
  const sequence=structure.masses.find(m=>m.key==='pentecost').propers.find(p=>p.name==='Sequence');
  const node=render(sequence);
  assert.deepEqual(sides(node).map(side=>classes(side,'stanza').length),[11,10]);
  assert.equal(classes(node,'text-pair').length,1);
});

test('selected cycles stay isolated, including their language absences', () => {
  const p=owner({text:null,translations:[],cycles:{A:{text:'Cycle A Latin.',translations:[{lang:'en',source_id:'a',rights:'public-domain',text:'Cycle A English.'}]},B:{text:'Cycle B Latin.',translations:[],untranslated:[{lang:'en',state:'unavailable'}]}}});
  const node=render(p,{cycle:'B'});
  assert.match(node.textContent,/Cycle B Latin/); assert.doesNotMatch(node.textContent,/Cycle A/);
  assert.match(node.textContent,/English translation unavailable for this cycle/);
});

test('Ordinary pairs preserve one semantic owner and independent turn/gloss structure', () => {
  const file={languages:[{lang:'la',absent:'latin'},{lang:'en',absent:'english'}],translations:[{source_id:'w',label:'Synthetic witness'}],absences:[]};
  const element={key:'synthetic',kind:'dialogue',name:'Synthetic exchange',translations:[
    {lang:'la',source_id:'w',rights:'public-domain',text:'Latin turn.',turns:[{key:'one',speaker:'priest',text:'Latin turn.'}]},
    {lang:'en',source_id:'w',rights:'public-domain',text:'English turn.\nEnglish gloss.',turns:[{key:'one',speaker:'priest',text:'English turn.'},{key:'gloss',gloss:true,text:'English gloss.'}]}]};
  production.Ordinary.configure({ordinaryLang:'en',textDisplay:'latin-and-selected',why:false});
  const node=production.Ordinary.renderElement(element,file);
  assert.equal(classes(node,'ordinary-element').length,1);
  assert.equal(classes(node,'proper-name').length,1);
  assert.deepEqual(sides(node).map(side=>classes(side,'ordinary-turn').length),[1,2]);
  assert.deepEqual(sides(node).map(side=>classes(side,'ordinary-turn-cue').length),[1,1]);
  assert.match(sides(node)[1].textContent,/English gloss/);
  production.Ordinary.configure({ordinaryLang:'la',textDisplay:'latin-and-selected'});
  assert.equal(classes(production.Ordinary.renderElement(element,file),'text-pair').length,0);
});

test('Ordinary missing languages and coequal witnesses do not borrow or choose by array order', () => {
  const file={languages:[{lang:'en',absent:'english'},{lang:'la',absent:'latin'}],translations:[],absences:[{key:'no-latin',kind:'untranscribed',label:'Latin has not been sourced'}]};
  const element={kind:'prayer',name:'Synthetic prayer',absent:{latin:'no-latin'},translations:[{lang:'en',source_id:'w1',rights:'public-domain',text:'First English.'},{lang:'en',source_id:'w2',rights:'public-domain',text:'Second English.'}]};
  production.Ordinary.configure({ordinaryLang:'en',textDisplay:'latin-and-selected'});
  const node=production.Ordinary.renderElement(element,file);
  assert.match(sides(node)[0].textContent,/Latin has not been sourced/);
  assert.match(sides(node)[1].textContent,/no witness was selected/);
  assert.doesNotMatch(node.textContent,/First English|Second English/);
});

test('text-free sharing preserves explicit display and semantic location without altering comparison peers', () => {
  const location={href:'https://example.test/liturgy/index.html'+identity+'&mode=compare&compare=oration-language&peer-orations=la'};
  const url=Actions.textDisplayUrl(location,'latin-and-selected',{kind:'event',id:'compare/proper/collect'});
  const params=new URL(url).hash;
  assert.match(params,/text-display=latin-and-selected/); assert.match(params,/peer-orations=la/);
  assert.match(params,/location=compare%2Fproper%2Fcollect/); assert.doesNotMatch(location.href,/text-display/);
  assert.throws(()=>Actions.textDisplayUrl(location,'bad'),/Invalid/);
});

test('primary semantic identity selection order and coverage stay unchanged by accompaniment', () => {
  const plain=normalize(identity).state; const paired={...plain,textDisplay:'latin-and-selected'};
  const a=Adapters.adaptPropers({request:plain,structure}); const b=Adapters.adaptPropers({request:paired,structure});
  for (const key of ['events','coverage','unresolvedChoices','explicitAbsences','resolved']) assert.deepEqual(b[key],a[key],key);
});

test('Day normalization round trips the same optional presentation without a territorial inference', () => {
  const dayContext={...context,dayReadableFormularies:[]};
  const normalizeDay=hash=>State.normalizeLegacy(State.parseLegacy('day',hash),{context:dayContext,
    defaults:{date:'2026-05-24',missal:'roman-1962',bible:'douay-rheims',orations:'en'}});
  const state=normalizeDay('#date=2026-05-24&missal=roman-1962&bible=douay-rheims&orations=en&text-display=latin-and-selected');
  assert.equal(state.ok,true,JSON.stringify(state.errors));
  assert.equal(state.state.textDisplay,'latin-and-selected');
  assert.equal(state.state.calendar.territory,undefined);
  assert.deepEqual(normalizeDay(State.serializeLegacy(state)).state,state.state);
});

test('comparison axes hold accompaniment fixed across independently adapted sides', () => {
  const left=normalize(identity.replace('pentecost','advent-1')).state;
  const right={...left,languages:{orations:'la'},textDisplay:'latin-and-selected'};
  const comparison={dimension:'oration-language',anchor:{correspondingFormulary:'advent-1'},sides:[
    {id:'en',edition:left.edition,formulary:left.formulary,languages:left.languages},
    {id:'la',edition:right.edition,formulary:right.formulary,languages:right.languages}]};
  const adapted=state=>Adapters.adaptPropers({request:state,structure});
  assert.throws(()=>Compare.compare({comparison,sides:[{id:'en',result:adapted(left)},{id:'la',result:adapted(right)}]}),/same edition/);
  const view=Compare.compare({comparison,sides:[{id:'en',result:adapted({...left,textDisplay:right.textDisplay})},{id:'la',result:adapted(right)}]});
  assert.equal(view.dimension,'oration-language');
  assert.deepEqual(view.sides.map(side=>side.result.request.textDisplay),['latin-and-selected','latin-and-selected']);
  assert.equal(Compare.compare({comparison,sides:[{id:'en',result:adapted(left)},
    {id:'la',result:adapted({...right,textDisplay:'selected'})}]}).dimension,'oration-language');
});

test('shared Scripture rendering is unchanged for every public Bible language and failure disposition', {skip:!BASELINE}, () => {
  const baseline=runtime(resolve(BASELINE));
  for (const edition of read('src/web/data/bibles.json').bibles) for (const fragment of [
    {ok:true,verses:{1:'First source verse.',2:'Second source verse.'}},
    {ok:true,verses:{1:'First source verse.'}}, {ok:false,problem:'Synthetic unavailable chapter'}]) {
    const locus={chapter:1,first:1,last:2};
    assert.equal(json(production.T.renderLocus(locus,fragment,edition.language)),
      json(baseline.T.renderLocus(locus,fragment,edition.language)),edition.id);
  }
});

test('default Proper and Ordinary DOM remains identical to the prerequisite baseline', {skip:!BASELINE}, () => {
  const baseline=runtime(resolve(BASELINE)); let count=0;
  for (const mass of structure.masses.filter(m=>['pentecost','advent-1','s-luciae-virginis-et-martyris'].includes(m.key))) {
    for (const proper of mass.propers) for (const lang of ['la','en']) {
      const options={orations:lang};
      assert.equal(json(production.T.renderProper(proper,bible,new Map(),options)),json(baseline.T.renderProper(proper,bible,new Map(),options)),mass.key+'/'+proper.name+'/'+lang); count++;
    }
  }
  for (const lang of ['la','en']) {
    production.Ordinary.configure({ordinaryLang:lang,textDisplay:'selected',why:false});
    baseline.Ordinary.configure({ordinaryLang:lang,why:false});
    for (const element of ordinary.sections.flatMap(s=>s.elements)) {
      assert.equal(json(production.Ordinary.renderElement(element,ordinary)),json(baseline.Ordinary.renderElement(element,ordinary)),element.key+'/'+lang); count++;
    }
  }
  assert.ok(count>400);
});
