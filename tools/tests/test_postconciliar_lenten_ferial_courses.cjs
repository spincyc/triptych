'use strict';
// stdin: fresh canonical reading owners; no generated fixture or source words.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../..');
const S = require(path.join(root, 'src/web/browser/liturgy/ordinary-seating.js'));
const source = JSON.parse(fs.readFileSync(0, 'utf8'));
const ordinary = JSON.parse(fs.readFileSync(path.join(root, 'src/web/data/structure/ordinary/postconciliar.json')));
const before = JSON.stringify(source);
const fact = 'lent-5-sunday-john-8-1-11-actually-read';
let executions = 0, negatives = 0, staticForms = 0;
function prepare(mass, cycle, entrance, choices={}, facts={}, definitions=mass.proper_source_paths, propers=mass.propers) {
  executions++;
  return S.prepareProperAppointments(propers.map((proper, sourceIndex) => ({proper, sourceIndex})), {
    calendar:'postconciliar', mass:mass.key, formId:'main', entrance,
    sourcePaths:definitions, calendarCycles:{sunday:cycle, weekday:'II'}, choices, conditionFacts:facts
  });
}
function selected(result) {
  return S.unframedEvents(result.rows, null, result.selections).flatMap(event =>
    event.kind === 'proper' ? [event] :
      event.options.filter(option => option.id === (event.selection||{}).option).flatMap(option => option.rows));
}
for (const mass of source.masses) {
  S.validateProperSeating(ordinary, mass.propers, {calendar:'postconciliar', mass:mass.key,
    form_id:'main', full:true, facts:{}, sourcePaths:mass.proper_source_paths});
  staticForms++;
  const relation=mass.proper_source_paths[0], rid='main/'+relation.id;
  const optional=relation.paths.find(p=>p.id.startsWith('course-'));
  for(const entrance of ['day','propers']) for(const cycle of ['A','B','C']) {
    const undecided=prepare(mass,cycle,entrance);
    assert.equal(undecided.sourcePathSelections[rid].state,'required');
    assert.equal(selected(undecided).length,0);
    for(const p of relation.paths) {
      if(!p.calendar_cycles.in.includes(cycle)) continue;
      const facts=p.when ? {[p.when.fact]:p.when.is} : {};
      const result=prepare(mass,cycle,entrance,{[rid]:p.id},facts);
      assert.equal(selected(result).length,p.members.length);
      assert.equal(result.sourcePathSelections[rid].option,p.id);
      if(p===optional) {
        assert.equal(selected(result).length,4);
        const names=selected(result).map(row=>row.proper.name);
        assert.deepEqual(new Set(names),new Set(['First Reading','Responsorial Psalm','Verse Before the Gospel','Gospel']));
        const verse=selected(result).find(row=>row.proper.name==='Verse Before the Gospel').proper;
        assert.equal(verse.source,'composed');
        assert.equal(verse.text_status.state,'unavailable');
        assert.equal(verse.text_status.scope,'proper-body');
        for(const field of ['text','verses','incipit','translations']) assert.equal(verse[field],undefined);
      }
      if(p.when) {
        assert.throws(()=>prepare(mass,cycle,entrance,{[rid]:p.id},{}));
        negatives++;
      }
    }
    const oldGospel=relation.paths.find(p=>p.standing==='principal').choices.gospel;
    assert.throws(()=>prepare(mass,cycle,entrance,{[rid]:optional.id,'main/gospel':oldGospel}));
    negatives++;
    if(mass.key==='lent-5-monday') {
      for(const actual of [null,false,true]) {
        const result=prepare(mass,cycle,entrance,{[rid]:optional.id},{[fact]:actual});
        assert.equal(selected(result).length,4);
        assert.equal(selected(result).find(r=>r.proper.name==='Gospel').proper.verses[0].ref,'John 11:1-45');
      }
      const unresolved=prepare(mass,cycle,entrance,{}, {[fact]:null});
      assert.equal(unresolved.sourcePathSelections[rid].state,'required');
    }
  }
  for(const mutation of ['incomplete-option','foreign-member','foreign-relation','wrong-material','missing-guard']) {
    const definitions=structuredClone(mass.proper_source_paths), rows=structuredClone(mass.propers);
    const p=definitions[0].paths.find(p=>p.id.startsWith('course-'));
    if(mutation==='incomplete-option') p.members.pop();
    if(mutation==='foreign-member') p.members[0].appointment.mass='lent-3';
    if(mutation==='foreign-relation') definitions[0].source_edition='roman-1962';
    if(mutation==='wrong-material') p.members[0].material_cycle={family:'cycles',cycle:'A'};
    if(mutation==='missing-guard') delete rows.find(r=>r.name==='First Reading').source_path_relation;
    assert.throws(()=>prepare(mass,'B','day',{[rid]:optional.id},{},definitions,rows), mutation);
    negatives++;
  }
}
const tuesday=source.masses.find(mass=>mass.key==='lent-5-tuesday');
const tuesdayRelation=tuesday.proper_source_paths[0];
assert.equal(tuesdayRelation.paths.find(p=>p.standing==='principal').members.length,4);
const tuesdayVerses=tuesday.propers.filter(p=>p.name==='Verse Before the Gospel');
assert.equal(tuesdayVerses.length,2);
assert(tuesdayVerses.every(p=>p.source==='composed' && p.text_status.state==='unavailable'));

assert.equal(executions,560);assert.equal(negatives,202);assert.equal(staticForms,18);
const coreExecutions=executions;
let additionalControls=0;
for(const mass of source.masses){
  const relation=mass.proper_source_paths[0],rid='main/'+relation.id;
  const optional=relation.paths.find(p=>p.id.startsWith('course-'));
  assert.throws(()=>prepare(mass,'B','day',{'main/gospel':optional.choices.gospel}),/complete selected source path/);
  additionalControls++;
  assert.throws(()=>prepare(mass,'B','day',{'main/first-reading':optional.choices['first-reading']}),/complete selected source path/);
  additionalControls++;
  assert.throws(()=>prepare(mass,'D','day',{[rid]:optional.id}));additionalControls++;
  assert.throws(()=>S.unframedEvents(mass.propers,()=>true),/must be prepared/);additionalControls++;
  const malformed=structuredClone(mass.propers);
  malformed.find(p=>p.name==='Verse Before the Gospel'&&p.source==='composed').appointment_identity.occurrence=99;
  assert.throws(()=>S.validateProperSeating(ordinary,malformed,{calendar:'postconciliar',mass:mass.key,
    form_id:'main',full:true,sourcePaths:mass.proper_source_paths}),/appointment|member|guard|missing/);additionalControls++;
  const extra=structuredClone(mass.propers);
  const forged=structuredClone(extra.find(p=>p.name==='First Reading'));
  forged.ordinary_disposition.option='unowned-test-option';
  forged.appointment_identity.occurrence=99;delete forged.source_path_relation;extra.push(forged);
  assert.throws(()=>prepare(mass,'B','day',{[rid]:optional.id},{},mass.proper_source_paths,extra),/raw extent|membership|guard/);
  additionalControls++;
}
const monday=source.masses.find(m=>m.key==='lent-5-monday');
const mondayId='main/lent-5-monday-reading-course';
for(const entrance of ['day','propers']){
  for(const native of monday.proper_source_paths[0].paths.filter(p=>p.when)){
    assert.throws(()=>prepare(monday,'C',entrance,{[mondayId]:native.id},{[fact]:!native.when.is}),/inapplicable/);
    additionalControls++;
  }
  for(const stale of ['john-8-1-11-ab','john-8-1-11-c','john-8-12-20-c']){
    // A Gospel-only selector cannot silently pick Daniel or infer prior use.
    assert.throws(()=>prepare(monday,'C',entrance,{'main/lent-5-monday-gospel':stale},{[fact]:true}),/unknown|held|unused/);
    assert.throws(()=>prepare(monday,'C',entrance,{[mondayId]:stale},{[fact]:true}),/not held/);
    additionalControls+=2;
  }
  for(const facts of [{},{[fact]:null},Object.create({[fact]:true})]){
    for(const option of ['john-8-12-20-c-longer','john-8-12-20-c-shorter']){
      assert.throws(()=>prepare(monday,'C',entrance,{[mondayId]:option},facts),/source-condition-unresolved/);
      additionalControls++;
    }
    const optional=prepare(monday,'C',entrance,{[mondayId]:'course-250'},facts);
    assert.equal(selected(optional).length,4);
    assert.equal(selected(optional).find(r=>r.proper.name==='Gospel').proper.verses[0].ref,'John 11:1-45');
  }
  for(const bad of ['true','false',1,0,{},[],undefined]){
    assert.throws(()=>prepare(monday,'C',entrance,{[mondayId]:'course-250'},{[fact]:bad}),/boolean/);
    additionalControls++;
  }
}
// Source-local truth table, both Daniel forms, both entrances. Choosing an
// option, even on the right date or through an inherited value, cannot attest.
let conditionExecutions=0, conditionNegatives=0;
const factsCases=[{}, {[fact]:null}, {[fact]:false}, {[fact]:true},
  Object.create({[fact]:true}), Object.create({[fact]:false})];
for(const entrance of ['day','propers']) for(const cycle of ['A','B','C']) {
  for(const facts of factsCases) for(const daniel of ['longer','shorter']) {
    const primary=(cycle==='C'?'john-8-1-11-c-':'john-8-1-11-ab-')+daniel;
    const result=prepare(monday,cycle,entrance,{[mondayId]:primary},facts);
    conditionExecutions++;
    assert.equal(result.sourcePathSelections[mondayId].option,primary);
    assert.deepEqual(selected(result).map(r=>r.proper.name),
      [daniel==='longer'?'First Reading':'First Reading (shorter form)',
       'Responsorial Psalm','Verse Before the Gospel','Gospel']);
    assert.equal(selected(result).at(-1).proper.verses[0].ref,'John 8:1-11');
    const alternate={[mondayId]:'john-8-12-20-c-'+daniel};
    if(cycle==='C' && Object.hasOwn(facts,fact) && facts[fact]===true) {
      const optional=prepare(monday,cycle,entrance,alternate,facts);
      assert.equal(selected(optional).length,4);
      assert.equal(selected(optional).at(-1).proper.verses[0].ref,'John 8:12-20');
    } else {
      assert.throws(()=>prepare(monday,cycle,entrance,alternate,facts));
      conditionNegatives++;
    }
    conditionExecutions++;
    // Neither complete course can borrow even one role from the other.
    for(const choices of [
      {[mondayId]:primary,'main/gospel':'course-250'},
      {[mondayId]:'course-250','main/first-reading':daniel},
      {[mondayId]:primary,'main/first-reading':daniel==='longer'?'shorter':'longer'}
    ]) {
      assert.throws(()=>prepare(monday,cycle,entrance,choices,facts),/mix incompatible/);
      conditionExecutions++;conditionNegatives++;
    }
  }
}
assert.equal(conditionExecutions,360);
assert.equal(conditionNegatives,284);
assert.equal(JSON.stringify(source),before,'admission must preserve original raw source metadata');
console.log(JSON.stringify({status:'pass',staticForms,executions:coreExecutions,negativeControls:negatives,
  additionalControls,additionalExecutions:executions-coreExecutions,conditionExecutions,conditionNegatives,
  scope:'18 coupled ferial courses; 19 composed unavailable owners; explicit n252 gap; stale Gospel-only selectors fail closed'}));
