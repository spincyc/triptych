/* ===========================================================================
 * The plan's front door — what it is, its three tracks, and what it omits
 * ===========================================================================
 *
 * This page reads no scripture and fetches no chapter. It exists because
 * choosing a depth is a different act from reading at one, and because the
 * plan's account of its own omissions needs somewhere it is the subject rather
 * than an aside beneath a passage.
 *
 * A track is entered at ./track.html, which is where every reading lives.
 * Links from here carry the query string forward, so ?data= and ?plan= survive
 * the crossing.
 *
 * The page also honours the addresses the earlier single-page reader published:
 * a hash naming a reading or a tier is forwarded to the track page unchanged,
 * so nothing anyone bookmarked stops working.
 * ======================================================================== */

'use strict';

(function () {
  const T = window.Triptych;
  const P = window.ScripturePlan;

  const content = document.getElementById('reading');
  const lede = document.getElementById('plan-lede');

  const SEARCH = window.location.search;

  function trackHref(hash) {
    return 'track.html' + SEARCH + (hash || '');
  }

  /* ------------------------------------------------------------------------
   * The addresses the single-page reader used
   *
   * It answered at this file with #tier=…&reading=…&bible=…. Those links are in
   * the wild; they now name a place on the track page, and are forwarded there
   * rather than quietly landing on a page that ignores them. `replace` keeps
   * the dead address out of the reader's history.
   * --------------------------------------------------------------------- */

  const arriving = T.readHash();
  if (arriving.get('reading') || arriving.get('tier') || arriving.get('period')) {
    window.location.replace(trackHref(window.location.hash));
    return;
  }

  /* ------------------------------------------------------------------------
   * Rendering
   * --------------------------------------------------------------------- */

  function figures(view) {
    return [
      P.plural(view.count, 'reading'),
      P.plural(view.chapters, 'chapter'),
      P.plural(view.books, 'book')
    ].join(' · ');
  }

  function link(text, href, className) {
    const anchor = T.el('a', className || null, text);
    anchor.href = href;
    return anchor;
  }

  function trackCard(plan, view, index, total) {
    const card = T.el('article', 'track-card');

    const title = T.el('h3', 'track-card-title');
    title.appendChild(link(
      'The ' + view.label + ' track',
      trackHref('#tier=' + encodeURIComponent(view.tier)),
      'track-card-link'
    ));
    card.appendChild(title);

    card.appendChild(T.el('p', 'track-card-rank',
      'Depth ' + index + ' of ' + total));
    card.appendChild(T.el('p', 'figures', figures(view)));

    const daily = P.pacing(view.count)[0];
    card.appendChild(T.el('p', 'track-card-pace',
      'At a reading a day: ' + daily.takes + '.'));

    if (view.description) card.appendChild(P.prose(view.description));

    const go = T.el('p', 'track-card-go');
    go.appendChild(link(
      'Open the track',
      trackHref('#tier=' + encodeURIComponent(view.tier)),
      'begin-link'
    ));
    if (view.readings.length) {
      go.appendChild(document.createTextNode(' '));
      go.appendChild(link(
        'Begin at reading 1',
        trackHref('#tier=' + encodeURIComponent(view.tier) +
          '&reading=' + encodeURIComponent(view.readings[0].key)),
        'track-card-begin'
      ));
    }
    card.appendChild(go);

    return card;
  }

  function nestingTable(views) {
    const table = T.el('table', 'nesting');
    const caption = T.el('caption', 'nesting-caption',
      'Each track contains the one above it entire. The figures are counts of ' +
      'readings, of the distinct chapters they touch, and of the books those ' +
      'chapters are in.');
    table.appendChild(caption);

    const head = T.el('thead');
    const headRow = T.el('tr');
    for (const label of ['Track', 'Readings', 'New at this depth', 'Chapters', 'Books']) {
      const cell = T.el('th', null, label);
      cell.setAttribute('scope', 'col');
      headRow.appendChild(cell);
    }
    head.appendChild(headRow);
    table.appendChild(head);

    const body = T.el('tbody');
    let previous = 0;
    for (const view of views) {
      const row = T.el('tr');
      const name = T.el('th', null, view.label);
      name.setAttribute('scope', 'row');
      row.appendChild(name);
      row.appendChild(T.el('td', null, String(view.count)));
      row.appendChild(T.el('td', null, String(view.count - previous)));
      row.appendChild(T.el('td', null, String(view.chapters)));
      row.appendChild(T.el('td', null, String(view.books)));
      body.appendChild(row);
      previous = view.count;
    }
    table.appendChild(body);
    return table;
  }

  function periodTable(plan, views) {
    const table = T.el('table', 'nesting');
    const caption = T.el('caption', 'nesting-caption',
      'The twelve periods are the same twelve at every depth. Only how closely ' +
      'each is read changes.');
    table.appendChild(caption);

    const head = T.el('thead');
    const headRow = T.el('tr');
    const first = T.el('th', null, 'Period');
    first.setAttribute('scope', 'col');
    headRow.appendChild(first);
    for (const view of views) {
      const cell = T.el('th', null, view.label);
      cell.setAttribute('scope', 'col');
      headRow.appendChild(cell);
    }
    head.appendChild(headRow);
    table.appendChild(head);

    const widest = views[views.length - 1];
    const body = T.el('tbody');
    for (const period of widest.periods) {
      const row = T.el('tr');
      const name = T.el('th', null, period.label);
      name.setAttribute('scope', 'row');
      row.appendChild(name);
      for (const view of views) {
        const held = P.periodAt(view, period.key);
        row.appendChild(T.el('td', null, held ? String(held.readings.length) : '—'));
      }
      body.appendChild(row);
    }

    const totals = T.el('tr', 'nesting-total');
    const label = T.el('th', null, 'All periods');
    label.setAttribute('scope', 'row');
    totals.appendChild(label);
    for (const view of views) totals.appendChild(T.el('td', null, String(view.count)));
    body.appendChild(totals);

    table.appendChild(body);
    return table;
  }

  function section(id, title) {
    const node = T.el('section', 'plan-block');
    const heading = T.el('h2', 'plan-title', title);
    heading.id = id;
    node.appendChild(heading);
    node.setAttribute('aria-labelledby', id);
    return node;
  }

  function render(plan) {
    const views = P.tiers(plan).map((tier) => P.track(plan, tier));
    T.clear(content);

    lede.textContent = plan.plan
      ? String(plan.plan)
      : 'An abridged reading of the story of salvation, at three depths.';

    const tracks = section('tracks', 'Three tracks, one story');
    tracks.appendChild(T.el('p', 'plan-lead',
      'The tracks nest. Every reading is marked with the depth at which it ' +
      'first appears and appears at no other, so a track is read by taking ' +
      'every reading at its own depth and at every depth above it, in order. ' +
      'The shorter tracks are not summaries of the longer ones: they are the ' +
      'same story told with fewer sittings.'));

    const deck = T.el('div', 'track-deck');
    views.forEach((view, at) => {
      deck.appendChild(trackCard(plan, view, at + 1, views.length));
    });
    tracks.appendChild(deck);
    tracks.appendChild(nestingTable(views));
    content.appendChild(tracks);

    const periods = section('periods', 'The twelve periods');
    periods.appendChild(T.el('p', 'plan-lead',
      'The periods are the spine of the story, and every track walks all ' +
      'twelve. A period is where a reader should start: it is the unit at ' +
      'which the plan explains itself.'));
    periods.appendChild(periodTable(plan, views));
    content.appendChild(periods);

    if (plan.omissions) {
      const cost = section('omissions', 'What this plan does not read');
      cost.appendChild(T.el('p', 'plan-lead',
        'This account belongs at the front and not in a footnote. An ' +
        'abridgement is defined by what it drops, and a reader owed the story ' +
        'in order is also owed the bill for it.'));
      cost.appendChild(P.prose(plan.omissions));
      content.appendChild(cost);
    }

    if (plan.precedents) {
      const from = section('precedents', 'Where the selection comes from');
      from.appendChild(P.prose(plan.precedents));
      content.appendChild(from);
    }

    const text = section('text', 'Text and numbering');
    const facts = T.el('dl', 'facts');
    const rows = [
      ['Canon', T.titleCase(String(plan.canon || 'unstated'))],
      ['References', T.titleCase(String(plan.numbering || 'unstated')) + ' numbering'],
      ['Readings', String(views[views.length - 1].count) + ' in all, over ' +
        views[views.length - 1].periods.length + ' periods']
    ];
    for (const [term, value] of rows) {
      facts.appendChild(T.el('dt', null, term));
      facts.appendChild(T.el('dd', null, value));
    }
    text.appendChild(facts);
    text.appendChild(T.el('p', 'plan-lead',
      'A track offers every translation the corpus carries, and states the ' +
      'reference again in that edition\'s own numbering wherever the two ' +
      'differ — the psalter is numbered one way in the Vulgate tradition and ' +
      'another in the Hebrew, and a reader who notices the disagreement is ' +
      'owed the reason rather than left to doubt one of them.'));
    content.appendChild(text);

    content.setAttribute('aria-busy', 'false');
    document.title = 'The Story of Salvation — Triptych';
    T.statusLine(
      'The reading plan, in ' + views.length + ' tracks: ' +
      views.map((view) => view.label + ', ' + view.count).join('; ') + '.'
    );
  }

  async function start() {
    // The manifest is not needed to describe the plan, but loading it is what
    // decides whether a data root can be reached at all; without it a page
    // opened off disk would report a missing plan rather than a missing corpus.
    await T.loadBibles();

    const loaded = await P.load();
    if (!loaded.ok) {
      T.fail(loaded.message);
      return;
    }

    const problems = P.warnings(loaded.plan);
    if (problems.length) {
      T.showBanner(
        'The reading plan "' + P.id + '" does not agree with itself: ' +
        problems.join('; ') + '.'
      );
    }

    render(loaded.plan);
  }

  start();
}());
