'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const [structureDir, calendarDir] = process.argv.slice(2);
const browser = path.resolve(__dirname, '../../src/web/browser/liturgy');
const A = require(path.join(browser, 'reader-state-adapters.js'));
const M = require(path.join(browser, 'assembly-model.js'));
const C = require(path.join(browser, 'reader-state.js'));
const read = (root, file) => JSON.parse(fs.readFileSync(path.join(root, file)));
const calendar = 'roman-1962';
const structure = read(structureDir, 'propers/roman-1962.json');
const ordinary = read(structureDir, 'ordinary/roman-1962.json');
const rubrics = read(calendarDir, 'rubrics/roman-1962.json');
const palmGroup = 'proper-choice/roman-1962/palm-sunday/main/palm-mass-gospel';
const substitute = 'second-or-third-low-mass-gospel';
const gospelCues = ['dominus-vobiscum-ante-evangelium', 'rubrica-evangelium-proprium',
  'rubrica-post-evangelium', 'laus-tibi-christe', 'rubrica-cum-sacerdote', 'per-evangelica-dicta'];

const palms = ['2027-03-21', '2028-04-09', '2029-03-25', '2030-04-14', '2031-04-06',
  '2032-03-21', '2033-04-10', '2034-04-02', '2035-03-18', '2036-04-06'];
const dates = palms.flatMap(palm => {
  const tuesday = new Date(palm + 'T00:00:00Z');
  tuesday.setUTCDate(tuesday.getUTCDate() + 2);
  return [['palm-sunday', palm], ['holy-tuesday', tuesday.toISOString().slice(0, 10)]];
});
for (const [massKey, date] of dates) {
  const year = read(calendarDir, 'calendar/roman-1962/' + date.slice(0, 4) + '.json');
  const mass = structure.masses.find(row => row.key === massKey);
  const palm = massKey === 'palm-sunday';
  const derived = M.derive({date, year, rubrics});
  assert(derived.options.some(opt => opt.readable.some(one => one.state === 'said' && one.key === massKey)));
  for (const entrance of ['day', 'propers']) {
    for (const option of (palm ? [null, substitute] : [null])) {
      const request = {
        schema: C.STATE_SCHEMA, entrance, civilDate: entrance === 'day' ? date : null,
        edition: {id: calendar}, bible: {id: 'douay-rheims', numbering: 'vulgate'},
        languages: {orations: 'la', ordinary: 'en'}, requestedMode: 'missal',
        options: {ordinary: true, legitimate: {}}, coverage: [], unresolvedChoices: [], sourceHooks: []
      };
      if (entrance === 'day') {
        request.calendar = {id: calendar};
        request.selectedReadableFormulary = {id: massKey};
      } else {
        request.formulary = {id: massKey, type: mass.kind};
      }
      if (option) request.properChoices = {[palmGroup]: option};
      const input = {request, structure, ordinary, derived};
      const answer = entrance === 'day' ? A.adaptDay(input) : A.adaptPropers(input);
      const events = answer.events;
      let selected;
      if (palm) {
        const event = events.find(row => row.kind === 'proper-choice' && row.group === 'palm-mass-gospel');
        assert(event);
        assert.equal(event.selection.option, option || 'passion');
        assert.deepEqual(event.options.map(row => row.id), ['passion', substitute]);
        selected = event.options.find(row => row.id === event.selection.option).events[0];
        assert.equal(selected.editionSlotLabel, option ? 'Gospel (vel)' : 'Passion according to Matthew');
        const print = event.options.find(row => row.id === substitute).events[0];
        assert(print.selected.references.includes('Matthew 27:45-52'));
        assert(events.some(row => row.editionSlotLabel === 'Gospel of the Blessing of Palms'));
      } else {
        selected = events.find(row => row.editionSlotLabel === 'Passion according to Mark');
        assert(selected);
      }
      assert.equal(selected.seat.id, 'evangelium');
      const keys = events.map(row => row.id);
      const prep = ['munda-cor-meum', 'iube-domine-benedicere', 'dominus-sit-in-corde-meo']
        .map(key => 'ordinary-element/oblatio/' + key);
      assert.deepEqual(keys.filter(key => prep.includes(key)), prep);
      for (const key of gospelCues) {
        assert.equal(keys.includes('ordinary-element/oblatio/' + key), Boolean(option), key);
      }
      const readingIndex = events.findIndex(row => row === selected || row.kind === 'proper-choice' && row.group === 'palm-mass-gospel');
      assert(readingIndex > keys.indexOf(prep[2]));
      assert(readingIndex < keys.indexOf('ordinary-element/oblatio/dominus-vobiscum-ante-offertorium'));
    }
  }
}
