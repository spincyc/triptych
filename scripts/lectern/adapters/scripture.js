'use strict';
/*
 * The Story of Salvation, as `src/web/browser/scripture/plan.js` (the front
 * door) and `track.js` (one track) assemble it.
 *
 * Every value below is a return of `plan-model.js` (`ScripturePlan`) or
 * `browser-core.js` (`Triptych`), called in the order the pages call them,
 * except the sentences marked `page:` -- prose that lives in the page code and
 * is repeated here with its line. Tracks are the model's (`P.tiers`,
 * `P.track`): nothing here counts readings per tier, nests tiers, or sorts.
 *
 * Two departures from the page, both in its favour, and both said where made:
 *
 *  - The verse text is rendered from the reading AS PUBLISHED, not from
 *    `P.readingCitation(reading)`, which copies only book, token, loci and
 *    unresolved and so drops the edition's own `edition_loci` and `refused`
 *    (plan-model.js:57-65 against guidance/web-data.md "Loci"). The same
 *    `T.renderCitation` then sees what the generator recorded for the edition:
 *    reading 255 under the CPDV is its recorded refusal, not Esther 10:4-15:14
 *    of a Septuagint-arranged text presented as the reading.
 *  - "in the " + label doubles the article for "The Story" and "The Full
 *    Account" (track.js:480, 566, 755; `updateChrome`). `theTrack` says it once.
 *
 * A period is handed to the reader by its place among the plan's periods
 * (`n`, 1-based, in the fullest track), never by its `key`: the keys are an
 * opaque scheme the plan must not display (guidance/reading-plan-for-agents.md
 * "Rights rules"), so they do not cross into the terminal at all.
 */
module.exports = function scripture(realm) {
  realm.script('shared/browser-core.js');
  realm.script('scripture/plan-model.js');
  const T = globalThis.Triptych;
  const P = globalThis.ScripturePlan;

  let started = null;
  function start() { // track.js:782
    if (!started) {
      started = (async () => {
        // The manifest first, as the page loads it: it is what decides whether
        // a data root can be reached at all (plan.js:227).
        const manifest = await T.loadBibles();
        if (!manifest.ok) throw new Error(manifest.message);
        const loaded = await P.load();
        if (!loaded.ok) throw new Error(loaded.message);
        // The built-in fallback is a demonstration, never the plan
        // (plan-model.js:340): a reader that cannot read the data fails.
        if (T.isInline()) {
          throw new Error('The published plan could not be read, and its built-in fallback is not a reading plan.');
        }
        return { bibles: manifest.bibles, plan: loaded.plan };
      })();
      started.catch(() => { started = null; });
    }
    return started;
  }

  function views(plan) {
    return P.tiers(plan).map((tier) => P.track(plan, tier));
  }

  /* A period's place among the plan's periods: its index in the fullest track. */
  function placeOf(plan, period) {
    const all = views(plan);
    const held = P.periodAt(all[all.length - 1], period.key);
    return held ? held.index : null;
  }

  /* "in the Landmarks track", "in The Story track": the article once. */
  function theTrack(view) {
    return (/^the\s/i.test(view.label) ? '' : 'the ') + view.label + ' track';
  }

  function prose(text, className) {
    return text ? realm.dom.read(P.prose(text, className)) : [];
  }

  function bibleRow(one) {
    return {
      id: one.id, label: one.label, edition: one.edition || '', language: one.language || '',
      languageName: one.language ? T.languageName(one.language) : '',
      numbering: one.numbering || '', psalter: one.psalter || '',
      // page: browser-core.js:505 (fillBibleSelect) -- "label (language)"
      choice: one.language ? one.label + ' (' + one.language + ')' : one.label,
      meta: T.bibleMeta(one),
    };
  }

  /* --- the front door --------------------------------------------------- */

  async function opening() {
    const { bibles, plan } = await start();
    const all = views(plan);
    const widest = all[all.length - 1];
    const problems = P.warnings(plan);
    const books = new Map();
    for (const entry of widest.readings) {
      const token = entry.reading.token;
      if (token && !books.has(token)) books.set(token, { token: token, name: entry.book || token });
    }
    return {
      title: plan.plan ? String(plan.plan) : '',
      // page: track.js:807
      warning: problems.length
        ? 'The reading plan "' + P.id + '" does not agree with itself: ' + problems.join('; ') + '.'
        : '',
      tracks: all.map((view, at) => ({
        tier: view.tier, label: view.label, count: view.count,
        newHere: view.count - (at ? all[at - 1].count : 0), // plan.js:95
        chapters: view.chapters, books: view.books,
        pacing: P.pacing(view.count),
      })),
      periods: widest.periods.map((period) => ({
        n: period.index,
        label: period.label,
        counts: all.map((view) => {
          const held = P.periodAt(view, period.key);
          return held ? held.readings.length : null;
        }),
      })),
      omissions: prose(plan.omissions),
      // page: plan.js:194-212, "Text and numbering"
      text: {
        rows: [
          ['Canon', T.titleCase(String(plan.canon || 'unstated'))],
          ['References', T.titleCase(String(plan.numbering || 'unstated')) + ' numbering'],
          ['Readings', String(widest.count) + ' in all, over ' + widest.periods.length + ' periods'],
        ],
        lead: 'A track offers every translation the corpus carries, and states the ' +
          'reference again in that edition\'s own numbering wherever the two ' +
          'differ — the psalter is numbered one way in the Vulgate tradition and ' +
          'another in the Hebrew, and a reader who notices the disagreement is ' +
          'owed the reason rather than left to doubt one of them.',
      },
      bibles: bibles.map(bibleRow),
      books: Array.from(books.values()),
    };
  }

  /* --- one track --------------------------------------------------------- */

  function figuresLine(view) { // page: track.js:270
    return [P.plural(view.count, 'reading'), P.plural(view.chapters, 'chapter'),
      P.plural(view.books, 'book')].join(' · ');
  }

  function nestingLine(plan, view) { // page: track.js:278-295
    const all = views(plan);
    const at = all.findIndex((held) => held.tier === view.tier);
    const wider = all.slice(at + 1);
    if (!wider.length) {
      return 'This is the fullest of the plan\'s tracks: nothing the plan holds ' +
        'is kept back from it. The plan itself is still an abridgement, and ' +
        'what follows is its own account of what it does not read at any depth.';
    }
    const said = wider.map((held) => theTrack(held).toLowerCase() + ' reads ' + held.count +
      ', ' + (held.count - view.count) + ' more than this one');
    return 'This track holds ' + view.count + ' of the plan\'s ' +
      all[all.length - 1].count + ' readings: ' + said.join(', and ') +
      '. Beyond that, the plan itself is an abridgement, and what follows is ' +
      'its own account of what it does not read at any depth.';
  }

  function badge(plan, view, entry) { // track.js:420
    if (P.tierRank(entry.tier) >= P.tierRank(view.tier)) return null;
    return { label: P.tierLabel(plan, entry.tier), tier: entry.tier,
      // page: track.js:424, the article said once
      title: 'First appears at ' + theTrack({ label: P.tierLabel(plan, entry.tier) }) };
  }

  async function track(tier) {
    const { plan } = await start();
    if (P.tiers(plan).indexOf(tier) < 0) throw new Error('This plan has no “' + tier + '” track.');
    const view = P.track(plan, tier);
    const first = view.readings[0] || null;
    return {
      tier: view.tier, label: view.label, count: view.count,
      chapters: view.chapters, books: view.books,
      rank: P.tierRank(view.tier),
      heading: view.label + ' track', // track.js:243
      lede: view.description ? P.firstSentence(view.description) : // track.js:614
        P.plural(view.count, 'reading') + ' in ' + view.periods.length + ' periods.',
      figures: figuresLine(view),
      description: prose(view.description),
      begin: first ? { order: first.order, said: 'Begin at reading 1 — ' + first.title } : null, // track.js:367
      pacing: P.pacing(view.count),
      nesting: nestingLine(plan, view),
      periods: view.periods.map((period) => ({
        n: placeOf(plan, period),
        index: period.index, total: period.total, label: period.label,
        count: period.readings.length, first: period.first, last: period.last,
        chapters: period.chapters,
        // page: track.js:338-343
        contents: ['Period ' + period.index + ' of ' + period.total,
          P.plural(period.readings.length, 'reading') + ' (' + period.first + '–' + period.last +
            ' of ' + view.count + ')',
          P.plural(period.chapters, 'chapter')].join(' · '),
        // page: track.js:476-482
        meta: ['Period ' + period.index + ' of ' + period.total,
          P.plural(period.readings.length, 'reading') + ' — ' + period.first + '–' + period.last +
            ' of ' + view.count + ' in ' + theTrack(view),
          P.plural(period.chapters, 'chapter')].join(' · '),
        line: P.firstSentence(period.summary),
        summary: prose(period.summary, 'period-summary'),
        badged: period.readings.some((entry) => badge(plan, view, entry)),
      })),
      readings: view.readings.map((entry) => ({
        order: entry.order, index: entry.index, n: placeOf(plan, entry.period),
        indexInPeriod: entry.indexInPeriod, title: entry.title, reference: entry.reference,
        book: entry.book, tier: entry.tier, badge: badge(plan, view, entry), note: entry.note || '',
      })),
    };
  }

  /* --- one reading -------------------------------------------------------- */

  function neighbour(view, other, entry, side) { // track.js:524-542
    if (!other) {
      return { side, none: side === 'Before' ? 'This is where the track begins.' : 'This is where the track ends.' };
    }
    return {
      side, order: other.order, title: other.title, reference: other.reference,
      crossing: other.period.key !== entry.period.key
        ? (side === 'Before' ? 'Last of ' : 'First of ') + other.period.label : '',
    };
  }

  async function reading(tier, key, bibleId) {
    const { bibles, plan } = await start();
    if (P.tiers(plan).indexOf(tier) < 0) throw new Error('This plan has no “' + tier + '” track.');
    const view = P.track(plan, tier);
    const entry = P.entryAt(view, key);
    if (!entry) throw new Error('Reading ' + key + ' is not in ' + theTrack(view) + '.');
    const bible = bibles.find((one) => one.id === bibleId);
    if (!bible) throw new Error('bibles.json offers no edition “' + bibleId + '”.');

    // The reading as published: lociFor then sees edition_loci and refused.
    const citation = Object.assign({}, entry.reading);
    const held = await T.fetchFragments(bible, [citation]);
    const block = T.renderCitation(citation, bible, held.fragments, plan.numbering || null,
      { book: entry.book, showRef: false }); // track.js:580
    return {
      order: entry.order, index: entry.index, count: view.count,
      n: placeOf(plan, entry.period), indexInPeriod: entry.indexInPeriod,
      period: entry.period.label, periodCount: entry.period.readings.length,
      title: entry.title, reference: entry.reference, book: entry.book, note: entry.note || '',
      badge: badge(plan, view, entry),
      // page: track.js:563-567, the article said once
      position: [
        'Reading ' + entry.indexInPeriod + ' of ' + entry.period.readings.length + ' in ' + entry.period.label,
        entry.index + ' of ' + view.count + ' in ' + theTrack(view)],
      bible: bibleRow(bible),
      blocks: realm.dom.read(block),
      // The chapters the plan's own references name, for the commentary held on
      // them: the model's own list, in the plan's numbering.
      chapters: T.chaptersNeeded([P.readingCitation(entry.reading)], plan.numbering || null)
        .map((one) => ({ token: one.book, chapter: Number(one.chapter) })),
      before: neighbour(view, view.readings[entry.index - 2], entry, 'Before'),
      after: neighbour(view, view.readings[entry.index], entry, 'After'),
    };
  }

  /*
   * Changing track keeps the reader's place (track.js:712-760): a reading the
   * new track holds stays; one it does not lands on the nearest reading before
   * it, and the page says so.
   */
  async function land(tier, key) {
    const { plan } = await start();
    if (P.tiers(plan).indexOf(tier) < 0) throw new Error('This plan has no “' + tier + '” track.');
    const view = P.track(plan, tier);
    if (P.entryAt(view, key)) return { order: Number(key), notice: '' };
    const wanted = Number(key);
    let nearest = null;
    if (Number.isFinite(wanted)) {
      for (const entry of view.readings) if (entry.order <= wanted) nearest = entry;
    }
    if (!nearest) return { order: view.readings.length ? view.readings[0].order : null, notice: '' };
    return {
      order: nearest.order,
      // page: track.js:755-757
      notice: 'That reading is not in ' + theTrack(view) + ', which is the smaller selection. ' +
        'This is the nearest reading before it.',
    };
  }

  /*
   * The readings whose own references name a chapter: in this track, and else
   * in the fullest, each with the track it first appears at. Read off the
   * model's chapter list for each reading, in the plan's numbering.
   */
  async function at(tier, token, chapter) {
    const { plan } = await start();
    const all = views(plan);
    const touches = (entry) => T.chaptersNeeded([P.readingCitation(entry.reading)], plan.numbering || null)
      .some((one) => one.book === token && Number(one.chapter) === Number(chapter));
    const row = (entry) => ({ order: entry.order, title: entry.title, reference: entry.reference,
      tier: entry.tier, tierLabel: P.tierLabel(plan, entry.tier) });
    const here = all.find((view) => view.tier === tier);
    return {
      here: here ? here.readings.filter(touches).map(row) : [],
      anywhere: all[all.length - 1].readings.filter(touches).map(row),
    };
  }

  return { opening, track, reading, land, at };
};
