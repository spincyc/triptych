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

  function link(text, href, className) {
    const anchor = T.el('a', className || null, text);
    anchor.href = href;
    return anchor;
  }

  // One table rather than three cards and a table beside them. The figures
  // were already tabular; the prose around them repeated what the columns
  // say, so the columns are what remain.
  function trackTable(views) {
    const table = T.el('table', 'nesting tracks');
    const caption = T.el('caption', 'nesting-caption',
      'Each track contains the one above it entire.');
    table.appendChild(caption);

    const head = T.el('thead');
    const headRow = T.el('tr');
    for (const label of
      ['Track', 'Readings', 'New here', 'Chapters', 'Books', 'A reading a day']) {
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
      const name = T.el('th', 'track-name');
      name.setAttribute('scope', 'row');
      name.appendChild(link(
        view.label,
        trackHref('#tier=' + encodeURIComponent(view.tier)),
        'track-link'
      ));
      row.appendChild(name);
      row.appendChild(T.el('td', null, String(view.count)));
      row.appendChild(T.el('td', null, String(view.count - previous)));
      row.appendChild(T.el('td', null, String(view.chapters)));
      row.appendChild(T.el('td', null, String(view.books)));
      row.appendChild(T.el('td', null, P.pacing(view.count)[0].takes));
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
      'The shorter tracks are not summaries of the longer ones: they are the ' +
      'same story told with fewer sittings.'));
    tracks.appendChild(trackTable(views));
    content.appendChild(tracks);

    const periods = section('periods', 'The twelve periods');
    periods.appendChild(T.el('p', 'plan-lead',
      'Every track walks all twelve.'));
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
      'The Story of Salvation, in ' + views.length + ' tracks: ' +
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
