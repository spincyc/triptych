/* ===========================================================================
 * The reading plan, as a model — shared by the plan's front door and its tracks
 * ===========================================================================
 *
 * There are two pages in this directory and this file is neither of them:
 *
 *   index.html   the plan: what it is, its three tracks, and what it leaves out
 *   track.html   one track, read as a course: orientation, period, reading
 *
 * Both need the same answers — which tracks exist, which readings belong to
 * one, where a reading sits in its period and in its track, how a citation is
 * written out, how the plan's own prose is set. Those answers live here once.
 * Nothing below touches the DOM except the prose renderer, and nothing below
 * fetches scripture: the chapter cache, the loci and the four failure
 * renderings are the shared machinery's and are used, never re-implemented.
 *
 * TIERS ARE CUMULATIVE, AND THE DIRECTION MATTERS. `overview` is the smallest
 * set and `year` is everything; each reading is marked with the tier at which
 * it FIRST appears, and appears in no other. So a track means every reading
 * marked at its tier AND at every tier above it — overview at the narrative
 * track, overview and narrative at the year track — in `order` sequence.
 *
 * Getting this backwards inverts the plan without erroring: the reader asks for
 * the 36-reading overview and is handed the 357-reading year, or asks for the
 * year and is handed the skeleton. Both look like a working plan. Hence the
 * explicit sequence below, ranked smallest-first, and the check that the count
 * computed here matches the count the plan's own `tiers` block declares.
 * ======================================================================== */

'use strict';

window.ScripturePlan = (function () {
  const T = window.Triptych;

  const PLAN = T.params.get('plan') || 'narrative-spine';
  const PLAN_PATH = 'structure/readings/' + PLAN + '.json';

  const TIER_SEQUENCE = ['overview', 'narrative', 'year'];

  /**
   * Where a tier sits in the nesting, smallest first.
   *
   * An unrecognised tier is a data problem, not a reason to drop readings on
   * the floor: it ranks with the widest known tier, so the reading is still
   * offered at the fullest reading of the plan, and the mismatch is reported.
   */
  function tierRank(tier) {
    const rank = TIER_SEQUENCE.indexOf(tier);
    return rank < 0 ? TIER_SEQUENCE.length - 1 : rank;
  }

  /* ------------------------------------------------------------------------
   * Citations
   * --------------------------------------------------------------------- */

  /** A citation-shaped view of a reading, so the shared renderer serves it. */
  function readingCitation(reading) {
    return {
      ref: null,
      book: reading.book || null,
      token: reading.token || null,
      loci: reading.loci || {},
      unresolved: reading.unresolved || null
    };
  }

  /**
   * A reading's reference in the plan's own numbering — "Genesis 1:1-2:2".
   *
   * The display name is passed to the shared formatter so the reference reads
   * as the plan writes it rather than as the fragment path spells it: the path
   * needs "Gen", the reader wants "Genesis".
   */
  function readingReference(plan, reading) {
    const numbering = (plan && plan.numbering) || 'vulgate';
    const picked = T.lociFor(readingCitation(reading), numbering);
    if (!picked.loci) return reading.book || reading.token || '';
    return T.formatLoci(picked.loci, { book: reading.book || reading.token });
  }

  /** Distinct chapters a set of readings touches, in the plan's numbering. */
  function chapterCount(plan, readings) {
    const numbering = (plan && plan.numbering) || 'vulgate';
    return T.chaptersNeeded(readings.map(readingCitation), numbering).length;
  }

  /* ------------------------------------------------------------------------
   * Tracks
   *
   * A track is a tier read as a course: its readings in plan order, cut into
   * the twelve periods, with every position a page needs to state already
   * computed. Building one walks the whole plan, so tracks are built once and
   * held; a reader stepping through 357 readings must not pay for that on
   * every step.
   * --------------------------------------------------------------------- */

  const built = new Map();

  function planPeriods(plan) {
    return (plan && plan.periods) || [];
  }

  function tierBlock(plan, tier) {
    const tiers = (plan && plan.tiers) || {};
    return tiers[tier] || {};
  }

  function tierLabel(plan, tier) {
    const declared = tierBlock(plan, tier).label;
    if (declared) return String(declared);
    return tier ? T.titleCase(tier) : 'All';
  }

  /** The tiers this plan offers, smallest first. */
  function tiers(plan) {
    const declared = (plan && plan.tiers) || {};
    const present = new Set();
    for (const period of planPeriods(plan)) {
      for (const reading of period.readings || []) present.add(reading.tier);
    }
    const offered = TIER_SEQUENCE.filter((tier) => {
      return Object.prototype.hasOwnProperty.call(declared, tier) || present.has(tier);
    });
    return offered.length ? offered : [TIER_SEQUENCE[TIER_SEQUENCE.length - 1]];
  }

  function track(plan, tier) {
    const held = built.get(tier);
    if (held) return held;

    const wanted = tierRank(tier);
    const periods = [];
    const readings = [];

    for (const period of planPeriods(plan)) {
      const kept = (period.readings || [])
        .filter((reading) => tierRank(reading.tier) <= wanted)
        .sort((a, b) => Number(a.order) - Number(b.order));
      if (!kept.length) continue;

      const view = {
        key: String(period.key || period.label || periods.length + 1),
        label: period.label || period.key || 'Period ' + (periods.length + 1),
        summary: period.summary ? String(period.summary).trim() : '',
        index: periods.length + 1,
        readings: [],
        chapters: chapterCount(plan, kept)
      };

      for (const reading of kept) {
        const entry = {
          key: String(reading.order),
          order: Number(reading.order),
          title: reading.title || readingReference(plan, reading) ||
            String(reading.order),
          reference: readingReference(plan, reading),
          book: reading.book || reading.token || '',
          tier: reading.tier,
          note: reading.note ? String(reading.note).trim() : '',
          reading: reading,
          period: view,
          indexInPeriod: view.readings.length + 1,
          index: readings.length + 1
        };
        view.readings.push(entry);
        readings.push(entry);
      }

      periods.push(view);
    }

    // The plan's sequence is the point of it; nothing here is ever sorted by
    // title, and the periods keep the order the file gives them.
    readings.sort((a, b) => a.order - b.order);
    readings.forEach((entry, at) => { entry.index = at + 1; });
    for (const period of periods) {
      period.total = periods.length;
      period.first = period.readings[0].index;
      period.last = period.readings[period.readings.length - 1].index;
    }

    const view = {
      tier: tier,
      label: tierLabel(plan, tier),
      description: tierBlock(plan, tier).description
        ? String(tierBlock(plan, tier).description).trim() : '',
      declared: tierBlock(plan, tier).readings,
      readings: readings,
      periods: periods,
      count: readings.length,
      chapters: chapterCount(plan, readings.map((entry) => entry.reading)),
      books: new Set(readings.map((entry) => entry.reading.token ||
        entry.reading.book)).size
    };
    built.set(tier, view);
    return view;
  }

  function entryAt(view, key) {
    return view.readings.find((entry) => entry.key === String(key)) || null;
  }

  function periodAt(view, key) {
    return view.periods.find((period) => period.key === String(key)) || null;
  }

  /**
   * Check the file against itself: the cumulative count at each tier, computed
   * from the readings, against the count the `tiers` block declares. A plan
   * that disagrees with its own summary is the failure the header comment
   * exists to catch, so it is said out loud rather than logged.
   */
  function warnings(plan) {
    const problems = [];
    for (const tier of tiers(plan)) {
      const declared = tierBlock(plan, tier).readings;
      const computed = track(plan, tier).count;
      if (typeof declared === 'number' && declared !== computed) {
        problems.push(
          'the ' + tier + ' tier declares ' + declared + ' readings but holds ' + computed
        );
      }
    }
    const unknown = new Map();
    for (const period of planPeriods(plan)) {
      for (const reading of period.readings || []) {
        if (TIER_SEQUENCE.indexOf(reading.tier) >= 0) continue;
        const name = String(reading.tier);
        unknown.set(name, (unknown.get(name) || 0) + 1);
      }
    }
    for (const [name, count] of unknown) {
      problems.push(
        count + ' reading' + (count === 1 ? '' : 's') + ' marked at the ' +
        'unrecognised tier "' + name + '", shown at the fullest tier'
      );
    }
    return problems;
  }

  /* ------------------------------------------------------------------------
   * Pacing
   *
   * How long a track takes is arithmetic on its reading count and nothing
   * else. No verse total is computed here: verse counts depend on chapter
   * lengths this page has not fetched, and the plan states its own in prose.
   * --------------------------------------------------------------------- */

  function plural(count, word) {
    return count + ' ' + word + (count === 1 ? '' : 's');
  }

  function spanOfDays(days) {
    if (days < 14) return plural(days, 'day');
    if (days < 70) return plural(days, 'day') + ' — about ' +
      plural(Math.round(days / 7), 'week');
    if (days < 365) return plural(days, 'day') + ' — about ' +
      plural(Math.round(days / 30.4), 'month');
    const years = days / 365;
    const rounded = years < 1.1 ? 'about a year'
      : 'about ' + (Math.round(years * 10) / 10) + ' years';
    return plural(days, 'day') + ' — ' + rounded;
  }

  function pacing(count) {
    return [
      { pace: 'One reading a day', takes: spanOfDays(count) },
      { pace: 'Three readings a week', takes: spanOfDays(Math.ceil(count / 3) * 7) },
      { pace: 'One reading a week', takes: spanOfDays(count * 7) }
    ];
  }

  /* ------------------------------------------------------------------------
   * The plan's own prose
   *
   * `omissions`, the tier descriptions and the period summaries are written as
   * hard-wrapped paragraphs, and some paragraphs are indented by two spaces —
   * that is how the omissions account sets off the three classes of book it
   * drops entirely. Rendering it as one blob loses that structure; rendering it
   * as raw pre-formatted text loses the wrapping. So: blank lines separate
   * paragraphs, wrapped lines rejoin, and an indented paragraph is set as an
   * aside. The words themselves are never altered.
   * --------------------------------------------------------------------- */

  function prose(text, className) {
    const out = document.createDocumentFragment();
    if (!text) return out;

    const blocks = String(text).replace(/\r\n/g, '\n').trim().split(/\n[ \t]*\n/);
    for (const block of blocks) {
      const lines = block.split('\n').filter((line) => line.trim().length);
      if (!lines.length) continue;
      const indented = lines.every((line) => /^ {2,}/.test(line));
      const body = lines.map((line) => line.trim()).join(' ');
      const node = T.el(
        'p',
        (indented ? 'prose-aside' : 'prose-line') + (className ? ' ' + className : ''),
        body
      );
      out.appendChild(node);
    }
    return out;
  }

  /** The first sentence of a summary, for a contents line that must stay short. */
  function firstSentence(text) {
    const flat = String(text || '').replace(/\s+/g, ' ').trim();
    const stop = flat.search(/[.!?](\s|$)/);
    return stop < 0 ? flat : flat.slice(0, stop + 1);
  }

  /* ------------------------------------------------------------------------
   * Loading
   * --------------------------------------------------------------------- */

  async function load() {
    let file;
    try {
      file = await T.loadJSON(PLAN_PATH);
    } catch (error) {
      return {
        ok: false,
        message: 'The reading plan "' + PLAN + '" could not be loaded: ' +
          (error.message || error)
      };
    }
    if (!file || !planPeriods(file).length) {
      return {
        ok: false,
        message: 'The reading plan "' + PLAN + '" lists no periods.'
      };
    }
    built.clear();
    return { ok: true, plan: file };
  }

  /* ------------------------------------------------------------------------
   * The offline fallback
   *
   * What the pages show when they are opened straight off disk, where fetch is
   * refused. It is not the published plan and says so, and its diagnostics sit
   * in a period labelled as such, so that no real reading ever carries invented
   * data. The shared file registers the manifest and a few chapters; the plan
   * is registered here, once, for both pages.
   * --------------------------------------------------------------------- */

  T.setInlineNotice(
    'No data root could be reached at "' + T.dataRoot + '", so these pages are ' +
    'showing their built-in fallback: three readings and a diagnostics period, ' +
    'which is not a reading plan. Serve the pages over HTTP with the corpus at ' +
    'that path, or try ?data=fixture.'
  );

  T.addInlineFiles({
    'structure/readings/narrative-spine.json': {
      schema: 'triptych-reading-structure/v1',
      plan: 'Built-in fallback (not the published reading plan)',
      canon: 'catholic-73',
      numbering: 'vulgate',
      tiers: {
        overview: { label: 'Overview', readings: 5, description: 'The fallback\'s smallest set.' },
        narrative: { label: 'Narrative', readings: 6, description: 'The overview, plus one.' },
        year: { label: 'Year', readings: 7, description: 'Everything this fallback holds.' }
      },
      omissions:
        'This is the pages\' built-in fallback, not a reading plan. It holds ' +
        'three readings over the three chapters compiled into the shared ' +
        'script, plus a diagnostics period. Serve the corpus, or ?data=fixture, ' +
        'for a plan.',
      periods: [
        {
          key: 'demonstration',
          label: 'Demonstration',
          summary: 'Three readings over the chapters this fallback carries.',
          readings: [
            {
              order: 1,
              tier: 'overview',
              title: 'Creation',
              book: 'Genesis',
              token: 'Gen',
              note: 'The first lesson of the Easter Vigil.',
              loci: {
                vulgate: [{ chapter: 1, first: 1, last: 3 }],
                hebrew: [{ chapter: 1, first: 1, last: 3 }]
              },
              unresolved: null
            },
            {
              order: 2,
              tier: 'narrative',
              title: 'Lifting up the soul',
              book: 'Psalms',
              token: 'Ps',
              note: 'The Introit of the First Sunday of Advent draws on these verses.',
              loci: {
                vulgate: [{ chapter: 24, first: 1, last: 3 }],
                hebrew: [{ chapter: 25, first: 1, last: 3 }]
              },
              unresolved: null
            },
            {
              order: 3,
              tier: 'year',
              title: 'The night is passed',
              book: 'Romans',
              token: 'Rom',
              note: null,
              loci: {
                vulgate: [{ chapter: 13, first: 11, last: 12 }],
                hebrew: [{ chapter: 13, first: 11, last: 12 }]
              },
              unresolved: null
            }
          ]
        },
        {
          key: 'fallback-diagnostics',
          label: 'Fallback diagnostics (not part of any plan)',
          summary:
            'Synthetic entries, marked at the overview tier so that they appear ' +
            'at every tier. Each exercises a failure the pages must explain ' +
            'rather than swallow.',
          readings: [
            {
              order: 9001,
              tier: 'overview',
              title: 'Diagnostic: unresolved reading',
              book: 'Psalms',
              token: 'Ps',
              note: 'The reason is shown in place of the text.',
              loci: {},
              unresolved: 'Ps has no chapter 151'
            },
            {
              order: 9002,
              tier: 'overview',
              title: 'Diagnostic: missing fragment',
              book: 'Tobias',
              token: 'Tob',
              note: 'No chapter file for Tob 3 exists in this fallback.',
              loci: {
                vulgate: [{ chapter: 3, first: 1, last: 2 }],
                hebrew: [{ chapter: 3, first: 1, last: 2 }]
              },
              unresolved: null
            },
            {
              order: 9003,
              tier: 'overview',
              title: 'Diagnostic: numbering absent',
              book: 'Psalms',
              token: 'Ps',
              note: 'Hebrew-only loci, read by a vulgate-numbered edition.',
              loci: { hebrew: [{ chapter: 25, first: 1, last: 1 }] },
              unresolved: null
            },
            {
              order: 9004,
              tier: 'overview',
              title: 'Diagnostic: verses absent from the fragment',
              book: 'Genesis',
              token: 'Gen',
              note: 'Genesis 1 is present in the fallback and has no verse 300.',
              loci: {
                vulgate: [
                  { chapter: 1, first: 1, last: 3 },
                  { chapter: 1, first: 300, last: 302 }
                ],
                hebrew: [
                  { chapter: 1, first: 1, last: 3 },
                  { chapter: 1, first: 300, last: 302 }
                ]
              },
              unresolved: null
            }
          ]
        }
      ]
    }
  });

  return {
    id: PLAN,
    path: PLAN_PATH,
    TIER_SEQUENCE: TIER_SEQUENCE,
    tierRank: tierRank,
    load: load,
    tiers: tiers,
    tierLabel: tierLabel,
    tierBlock: tierBlock,
    track: track,
    entryAt: entryAt,
    periodAt: periodAt,
    warnings: warnings,
    readingCitation: readingCitation,
    readingReference: readingReference,
    chapterCount: chapterCount,
    pacing: pacing,
    plural: plural,
    prose: prose,
    firstSentence: firstSentence
  };
}());
