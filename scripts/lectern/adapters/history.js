'use strict';
/*
 * How the Missal Changed (`src/web/browser/history/`), as history.js assembles it.
 *
 * Three of the page's views: the dated book states on a year axis ("Books
 * through time"), the recorded historical lines (the act map), and the source
 * catalogue. The model `M` and the page's validators are history.js's own,
 * sliced out of the page (page-slice.js); the data is the published
 * projection, every fragment opened by the path its record names, never a
 * composed one. Literal wording reaches the terminal only through the page's
 * gates: `nativeTextBindings` before a native text is read and
 * `nativeTextValid` before it is shown, `comparisonValid` before a witness
 * comparison is shown.
 *
 * The page glue that lives in closures and cannot be sliced — the default
 * window and tradition, the window controls, the tallies, the catalogue
 * filter, the assembly of a detail panel — is repeated here as `PORT:` with
 * its history.js lines, and the page's prose as `page:` with its line. Neither
 * restates a rule the model owns.
 */
const extract = require('./page-slice.js');

module.exports = function history(realm) {
  const P = extract.history(realm);
  const M = P.M;
  const BASE = 'structure/act-history/';

  // page: history.js:2757 — record words, as the page prints them.
  const words = (value) => String(value || '').replace(/-/g, ' ');
  const plain = (value) => (value === null || value === undefined ? '' : String(value));

  /* One read per path, as the page keeps one promise per fragment. */
  const files = new Map();
  function file(relative) {
    if (!files.has(relative)) {
      const value = realm.read(BASE + relative);
      if (value === undefined) throw new Error(BASE + relative + ' could not be read');
      files.set(relative, value);
    }
    return files.get(relative);
  }

  /* catalogue.json is 10.7 MB: read once, checked once, as the page does. */
  let held = null;
  function loaded() {
    if (held) return held;
    const data = file('catalogue.json');
    // page: history.js:2559
    if (!P.catalogueValid(data)) throw new Error('The source catalogue has an unsupported or malformed record.');
    // page: history.js:2748
    if (!P.stageHistoryValid(data.stage_history)) throw new Error('The historical stage projection is missing or malformed.');
    const history = data.stage_history;
    held = {
      data,
      history,
      keys: M.stageLayout(history), // page: history.js:2758 — the keys every view prints
      overview: M.overviewModel(data),
      byStage: new Map(history.stages.map((s) => [s.id, s])),
      byTransition: new Map(history.transitions.map((t) => [t.id, t])),
      bySource: new Map(history.sources.map((s) => [s.id, s])),
      byEntry: new Map(data.entries.map((r) => [r.id, r])),
    };
    return held;
  }

  function comparisonTitle(row) { // page: history.js:2540
    return row.title || row.label || row.id.replace(/-/g, ' ');
  }

  function comparisonRouted(row) { // page: history.js:2533-2536
    return Boolean(row && /^[a-z0-9][a-z0-9-]*$/.test(row.id || '') && row.left && row.right &&
      typeof row.apparatus_caveat === 'string' && row.projection_path === 'comparisons/' + row.id + '.json');
  }

  /* ------------------------------------------------------------------------
   * Opening: what every view needs to name its choices
   * --------------------------------------------------------------------- */

  function opening() {
    const { data, history, overview } = loaded();
    const manifest = file('index.json');
    const counted = new Map();
    history.stages.forEach((s) => counted.set(s.tradition_id, (counted.get(s.tradition_id) || 0) + 1));
    return {
      default_tradition: history.default_tradition_id || null,
      traditions: history.traditions.map((t) => ({ id: t.id, label: t.label, family: t.family || '', stages: counted.get(t.id) || 0 })),
      stage_limitations: history.limitations || [],
      catalogue_limitations: data.limitations,
      // page: history.js:2576-2581
      text_sets_note: 'Configuration does not mean that a text set has been generated or verified.',
      text_sets: data.text_sets.map((set) => P.catalogueText(set.id) + ' · ' + P.catalogueText(set.adapter) + ' · ' + P.catalogueText(set.status)),
      slices: (manifest.slices || []).map((row) => ({ id: row.id, lines: row.lines, stations: row.stations, vocabulary: row.vocabulary })),
      default_slice: chosenSlice(''),
      comparisons: (data.comparisons || []).map((row) => ({
        id: row.id, title: comparisonTitle(row), kind: words(row.kind), routed: comparisonRouted(row),
        apparatus_caveat: row.apparatus_caveat || '',
      })),
      groups: overview.groups.map((g) => ({ value: 'group:' + g.id, label: g.label, records: g.entries.length })),
      entries: data.entries.length,
    };
  }

  /* ------------------------------------------------------------------------
   * Books through time
   * --------------------------------------------------------------------- */

  /* PORT: history.js:2931-2937 dateBounds. */
  function dateBounds(history, keys, tradition, leads, global) {
    const dated = history.stages.filter((s) => (s.status === 'documented' || leads) && Number.isFinite(s.start_year) &&
      (global || tradition === 'all' || s.tradition_id === tradition));
    if (!dated.length) return { start: keys.start, end: keys.end };
    const first = Math.min.apply(null, dated.map((s) => s.start_year));
    const last = Math.max.apply(null, dated.map((s) => s.end_year));
    return { start: Math.floor(first / 50) * 50, end: Math.max(Math.floor(first / 50) * 50 + 50, Math.ceil(last / 50) * 50) };
  }

  const whole = (value) => (Number.isInteger(value) ? value : null);

  /* `asked` is the reader's state ({tradition, start, end, leads, stage}); `move`
   * is one of the page's window controls. */
  function timeline(asked, move) {
    const { history, keys, byStage, byTransition } = loaded();
    asked = asked || {};
    let current = {
      tradition: asked.tradition || null, start: whole(asked.start), end: whole(asked.end),
      leads: Boolean(asked.leads), stage: asked.stage || null, transition: asked.transition || null,
    };
    // PORT: history.js:3075-3086 — the window controls, applied to the state the reader holds.
    if (move === 'tradition') current = { ...current, start: null, end: null, stage: null, transition: null };
    else if (move === 'all-years') current = { ...current, ...dateBounds(history, keys, current.tradition, current.leads, true) };
    else if (move === 'local-years') current = { ...current, ...dateBounds(history, keys, current.tradition, current.leads, false) };
    else if ((move === 'earlier' || move === 'later') && current.start !== null && current.end !== null) {
      const step = Math.max(1, Math.round((current.end - current.start) / 2)) * (move === 'earlier' ? -1 : 1);
      current = { ...current, start: current.start + step, end: current.end + step };
    } else if ((move === 'zoom-in' || move === 'zoom-out') && current.start !== null && current.end !== null) {
      const span = Math.max(10, Math.round((current.end - current.start) * (move === 'zoom-in' ? 0.5 : 2)));
      const center = (current.end + current.start) / 2;
      current = { ...current, start: Math.floor(center - span / 2), end: Math.ceil(center + span / 2) };
    }
    // PORT: history.js:2945-2950 — the tradition a reader with no other instruction arrives at.
    if (!current.tradition) {
      const selectedTransition = byTransition.get(current.transition);
      const selected = byStage.get(current.stage) || (selectedTransition && byStage.get(selectedTransition.to_stage));
      current.tradition = selected ? selected.tradition_id : history.default_tradition_id ||
        (history.traditions.find((t) => history.stages.some((s) => s.tradition_id === t.id && s.status === 'documented')) ||
          history.traditions[0]).id;
    }
    // PORT: history.js:2951-2961 — the default window, at most six centuries for one tradition.
    if (current.start === null || current.end === null) {
      const bounds = dateBounds(history, keys, current.tradition, current.leads, false);
      current.start = bounds.start; current.end = bounds.end;
      if (current.tradition !== 'all' && current.end - current.start > 600) {
        current.start = current.end - 600;
        const selected = byStage.get(current.stage);
        if (selected && Number.isFinite(selected.start_year) && selected.end_year < current.start) {
          current.start = Math.floor(selected.start_year / 50) * 50;
          current.end = Math.max(current.start + 600, Math.ceil(selected.end_year / 50) * 50);
        }
      }
    }
    // PORT: history.js:2962-2967
    if ((current.start !== null || current.end !== null) &&
        (!Number.isFinite(current.start) || !Number.isFinite(current.end) || current.end <= current.start)) {
      return { state: current, error: 'Choose an ending year later than the starting year.' }; // page: history.js:2965
    }
    // page: history.js:2968-2970 — the options the page always passes.
    const options = { start: current.start, end: current.end, includeProvisional: current.leads, width: 1600, compact: true, inlineSummary: true };
    if (current.tradition !== 'all') options.tradition = current.tradition;
    const model = M.stageLayout(history, options);

    // PORT: history.js:2976-2984 — the tally and the status sentence.
    const inScope = (s) => current.tradition === 'all' || s.tradition_id === current.tradition;
    const scopedIds = new Set(history.stages.filter(inScope).map((s) => s.id));
    const documented = history.transitions.filter((t) => t.status === 'documented' && scopedIds.has(t.to_stage));
    const substantive = documented.filter((t) => t.kind !== 'witness-succession').length;
    const tally = model.counts.documented + ' documented states · ' + substantive + ' documented revisions, branches or receptions · ' +
      (documented.length - substantive) + ' witness successions · ' + model.counts.provisional + ' provisional leads in the selected history.';
    let status = (current.start === null ? 'No dated states; see unpositioned records below. ' : 'Showing ' + current.start + '–' + current.end + ': ') +
      model.counts.visible + ' dated states; ' + model.counts.outsideWindow + ' dated states outside this window. ' +
      'Date brackets are uncertainty bounds, not lifespans.';
    if (!model.lanes.length) status = 'This tradition is not in the current stage record: ' + current.tradition;

    const card = (stage) => ({ // PORT: history.js:2911-2929 readingCard
      key: model.stageKeys[stage.id], id: stage.id, label: stage.label, date: stage.date_label + ' · ' + stage.date_kind,
      meta: stage.status + ' · Parts: ' + stage.components.map(words).join(', ') + ' · Text: ' + words(stage.text_coverage),
      scope: stage.scope, status: stage.status,
      // the changes that arrive at it, documented ones unless leads are asked for (history.js:2920-2927)
      changes: history.transitions.filter((t) => t.to_stage === stage.id && (current.leads || t.status === 'documented'))
        .map((t) => ({ id: t.id, line: model.transitionKeys[t.id] + ' · ' + words(t.kind) + ' · ' + t.summary,
          evidence: words(t.evidence_level) + ' · ' + t.status + ' · parentage ' + t.historical_parentage })),
    });
    // page: history.js:3017-3024 — a continuation outside the view says where it goes.
    const outside = (end, stage, key) => {
      const year = stage.start_year === null ? 'undated' : stage.start_year === stage.end_year
        ? String(stage.start_year) : stage.start_year + '–' + stage.end_year;
      return { end, id: stage.id, key, year, title: stage.label,
        label: (end === 'from' ? 'From ' : 'To ') + key + ' · ' + year + ' · outside this view' };
    };
    const selectedGaps = history.gaps.filter((g) => current.tradition === 'all' || g.tradition_id === current.tradition);
    return {
      state: current,
      tally,
      status,
      axis: { start: model.start, end: model.end, x0: model.axis.x0, x1: model.axis.x1, ticks: model.axis.ticks.map((t) => ({ year: t.year, x: t.x })) },
      lanes: model.lanes.map((lane) => ({
        id: lane.id, label: lane.label, scope: lane.tradition.scope, coverage_note: lane.tradition.coverage_note || '',
        count: lane.visibleCount + ' dated states in this window', // page: history.js:2996
        visible: lane.visibleCount, total: lane.totalCount,
        nodes: lane.nodes.map((node) => ({
          id: node.id, key: node.key, label: node.stage.label, date_label: node.stage.date_label, date_kind: node.stage.date_kind,
          status: node.stage.status, text_coverage: node.stage.text_coverage, start_year: node.stage.start_year, end_year: node.stage.end_year,
          x: node.x, x_start: node.xStart, x_end: node.xEnd, clipped_start: node.clippedStart, clipped_end: node.clippedEnd,
          date_lines: node.dateLines, // the model's own card lines: date label · kind, and whether bounds run past the window
          incoming: node.incoming.map((entry) => entry.key),
        })),
        // The chronological reading list: this lane's states, as the page's cards (history.js:2997-3001).
        cards: lane.nodes.map((node) => card(node.stage)),
      })),
      edges: model.edges.map((edge) => ({
        id: edge.id, key: edge.key, from: edge.from, to: edge.to, from_key: edge.fromKey, to_key: edge.toKey,
        from_outside: edge.fromOutside, to_outside: edge.toOutside, from_x: edge.fromPoint.x, to_x: edge.toPoint.x,
        style: edge.style, kind: words(edge.transition.kind), status: edge.transition.status,
        evidence: edge.transition.evidence_level, parentage: edge.transition.historical_parentage, summary: edge.transition.summary,
        outside: edge.fromOutside ? outside('from', edge.fromStage, edge.fromKey) : edge.toOutside ? outside('to', edge.toStage, edge.toKey) : null,
      })),
      unpositioned: model.unpositioned.map(card),
      provisional: model.provisional.map(card),
      none_recorded: 'None recorded in this selection.', // page: history.js:3055
      gaps: selectedGaps.map((gap) => ({ // page: history.js:3058-3064
        period: gap.period, missing: gap.missing, consequence: gap.consequence, next: 'Next source to examine: ' + gap.next_source,
      })),
      gaps_none: 'No specific gap is listed for this selection. This does not establish complete coverage.', // page: history.js:3065
      counts: model.counts,
    };
  }

  function citations(items) { // PORT: history.js:2766-2778 citation
    const { bySource } = loaded();
    return (items || []).map((e) => {
      const source = bySource.get(e.source_id);
      if (!source) return null;
      return { title: source.title, url: P.catalogueURL(source.url), locus: e.locus + ' — ' + e.claim,
        meta: words(source.kind) + ' · ' + source.status + ' · ' + source.inspection, limitations: source.limitations || '' };
    }).filter(Boolean);
  }

  function transitionView(transition) { // PORT: history.js:2805-2834 transitionContent
    const { data, keys, byStage } = loaded();
    const from = byStage.get(transition.from_stage), to = byStage.get(transition.to_stage);
    return {
      id: transition.id, key: keys.transitionKeys[transition.id],
      heading: keys.transitionKeys[transition.id] + ' · ' + words(transition.kind),
      kind: words(transition.kind), summary: transition.summary,
      meta: words(transition.evidence_level) + ' · ' + transition.status + ' · historical parentage: ' + transition.historical_parentage,
      style: M.stageStyle(transition.evidence_level, transition.status),
      from: { id: from.id, key: keys.stageKeys[from.id], label: from.date_label + ' · ' + from.label },
      to: { id: to.id, key: keys.stageKeys[to.id], label: to.date_label + ' · ' + to.label },
      changes: (transition.changes || []).map((change) => ({
        component: words(change.component),
        before: 'Before: ' + change.before, before_locus: 'Before locus: ' + change.locus_before,
        after: 'After: ' + change.after, after_locus: 'After locus: ' + change.locus_after,
        evidence: citations(change.evidence),
      })),
      no_changes: transition.changes.length ? '' : 'No component-level before/after collation is recorded for this transition.',
      limitations: transition.limitations,
      evidence: citations(transition.evidence),
      comparisons: (transition.comparison_ids || []).map((id) => (data.comparisons || []).find((c) => c.id === id)).filter(Boolean)
        .map((row) => ({ id: row.id, label: 'Read linked source-text comparison: ' + (row.label || row.title || row.id) })),
    };
  }

  function stage(id) { // PORT: history.js:2861-2908 showDetail
    const { history, keys, byStage, byEntry } = loaded();
    const s = byStage.get(id);
    if (!s) return { missing: 'This stage is not in the current record: ' + id }; // page: history.js:2862
    let native = [], routing = '';
    try {
      native = P.nativeTextBindings(s).map((binding, index) => ({
        index, label: binding === s ? 'Read available source text' : 'Read available source text: ' + binding.title,
      }));
    } catch (error) {
      routing = 'The available source text has invalid routing metadata and cannot be opened.'; // page: history.js:2878
    }
    const tradition = history.traditions.find((t) => t.id === s.tradition_id);
    return {
      id: s.id, key: keys.stageKeys[s.id], heading: keys.stageKeys[s.id] + ' · ' + s.label, label: s.label,
      tradition: tradition ? tradition.label : s.tradition_id, status: s.status,
      date: s.date_label + ' · ' + s.date_kind + ' · ' + s.status,
      bounds: s.start_year === null ? 'No year is positioned for this state.'
        : 'Date bounds: ' + s.start_year + '–' + s.end_year + '. These date this attestation; they are not a period of validity.',
      coverage: 'Text coverage: ' + words(s.text_coverage) + '. This is independent of historical evidence.',
      native, routing,
      summary: s.summary, scope: 'Scope: ' + s.scope, parts: 'Parts represented: ' + s.components.map(words).join(', '),
      witness: 'Identified witness: ' + s.witness_label, reception: 'Community reception: ' + s.reception,
      limitations: s.limitations, evidence: citations(s.evidence),
      witnesses: s.witness_ids.map((w) => {
        const row = byEntry.get(w);
        return row ? { id: w, label: row.title + ' · ' + row.date_label, act_ref: row.act_ref }
          : { id: w, label: 'Witness reference not available in this catalogue: ' + w, missing: true };
      }),
      incoming: history.transitions.filter((t) => t.to_stage === s.id).map(transitionView),
      incoming_none: 'No transition into this state has been established here. Its position in date order does not supply a parent.',
      outgoing: history.transitions.filter((t) => t.from_stage === s.id).map(transitionView),
      outgoing_none: 'No onward transition is established here. This does not establish an end to its use.',
    };
  }

  function transition(id) {
    const { byTransition } = loaded();
    const t = byTransition.get(id);
    if (!t) return { missing: 'This transition is not in the current record: ' + id }; // page: history.js:2857
    return transitionView(t);
  }

  /* ------------------------------------------------------------------------
   * Literal text, only through the page's gates
   * --------------------------------------------------------------------- */

  function native(stageId, index) { // PORT: history.js:2869-2879 and renderNativeText 2488-2525
    const { byStage } = loaded();
    const s = byStage.get(stageId);
    if (!s) return { error: 'This stage is not in the current record: ' + stageId };
    let bindings;
    try { bindings = P.nativeTextBindings(s); } catch (error) {
      return { error: 'The available source text has invalid routing metadata and cannot be opened.' }; // page: history.js:2878
    }
    const binding = bindings[index || 0];
    if (!binding) return { error: 'This state carries no source text to open.' };
    const where = binding.text_projection_path;
    let payload;
    try { payload = file(where); } catch (error) {
      return { error: BASE + where + ' could not be read: ' + String(error.message || error) }; // page: history.js:1401
    }
    if (!P.nativeTextValid(payload, s, binding)) {
      return { error: 'The source text is malformed or does not match this state’s accepted binding and extent.' }; // page: history.js:2489
    }
    const sources = new Map(payload.sources.map((x) => [x.id, x]));
    const witnesses = new Map(payload.witnesses.map((w) => [w.id, w]));
    return {
      title: payload.title,
      stage: s.label,
      extent: 'Complete declared ' + payload.scope.extent_kind + ': ' + payload.counts.units + ' source unit' +
        (payload.counts.units === 1 ? '' : 's') + '. Whole-book text coverage: ' + (payload.scope.whole_book_complete ? 'complete.' : 'partial.'),
      scope: payload.scope.description,
      excluded_heading: payload.scope.omitted_book_divisions.length ? 'Excluded book divisions:' : '',
      excluded: payload.scope.omitted_book_divisions,
      units: payload.units.map((unit) => {
        const edition = sources.get(unit.text_edition_id);
        // page: history.js:2466 — the source is named by its edition and date.
        const label = edition.title + (edition.date ? ' (' + edition.date + ')' : '');
        const witness = witnesses.get(unit.witness_id), facsimile = witness && sources.get(witness.artifact_id);
        return {
          heading: unit.source_order + ' · ' + unit.kind.replace(/-/g, ' '), unit_id: unit.unit_id,
          text: unit.text, language: unit.language, direction: unit.direction,
          source: label, url: facsimile ? P.catalogueURL(facsimile.source_url) : null, locator: unit.source_locator,
        };
      }),
      rights: Array.from(new Set(payload.units.map((u) => u.source_artifact_id))).map((artifact) => ({
        line: 'Public domain · United States. ' + sources.get(artifact).rights_basis,
        normalization: sources.get(artifact).transformation || '',
      })),
    };
  }

  function comparison(id) { // PORT: history.js:2334-2398 renderComparison
    const { data } = loaded();
    const declared = (data.comparisons || []).find((row) => row.id === id);
    if (!declared) return { error: 'This record declares no witness comparison called ' + id + '.' };
    if (!comparisonRouted(declared)) return { error: 'A configured witness comparison has invalid metadata and cannot be opened.' }; // page: history.js:2537
    let payload;
    try { payload = file(declared.projection_path); } catch (error) {
      return { error: BASE + declared.projection_path + ' could not be read: ' + String(error.message || error) };
    }
    if (!P.comparisonValid(payload, declared)) {
      return { error: 'The witness comparison is malformed or does not match its declared source members.' }; // page: history.js:2335
    }
    const side = (name) => {
      const witness = payload[name];
      const languages = Array.from(new Set(witness.members.map((m) => m.language)));
      return {
        heading: (name === 'left' ? 'Left witness: ' : 'Right witness: ') + witness.title,
        dates: 'Printed edition / target date: ' + P.catalogueText(witness.target_date) + '. Represented witness date: ' +
          P.catalogueText(witness.witness_date) + '.',
        text: witness.joined_source_text, language: languages.length === 1 ? languages[0] : '',
        count: witness.members.length === 1 ? 'One source unit; exact stored wording.'
          : witness.members.length + ' source units in their declared order, joined with one space. Source wording is unchanged.',
        members: witness.members.map((member) => [
          'Source: ' + member.source_id + ' · Edition: ' + member.text_edition_id + ' · Artifact: ' +
            P.catalogueText(member.source_artifact_id || (member.provenance && member.provenance.artifact_provenance_source_id)),
          member.printed_page ? 'Printed page: ' + member.printed_page : '',
          'Transcription: ' + P.catalogueText(member.provenance && member.provenance.status) + ' · Publication basis: ' +
            P.catalogueText(member.publication.basis),
        ].filter(Boolean)),
      };
    };
    return {
      title: comparisonTitle(declared),
      identity: payload.kind === 'parallel-liturgical-unit-comparison'
        ? 'Parallel liturgical function; different compositions. This is not a same-prayer revision comparison.'
        : 'Witnesses of the same prayer; differences do not establish an act of revision.',
      basis: payload.basis, caveat: payload.apparatus_caveat,
      left: side('left'), right: side('right'),
      diff_heading: 'Show the generated unified text diff',
      diff_legend: 'Minus marks the left witness; plus marks the right. Lines follow the generator’s mechanical clause breaks. ' +
        'These marks compare wording, spelling, and punctuation; they do not establish historical additions or deletions.',
      diff: payload.unified_diff || 'The serialized texts are identical.',
      limitations: payload.limitations,
      sources: payload.sources.filter((source) => source && typeof source === 'object')
        .map((source) => ({ title: source.title || source.id || '', url: P.catalogueURL(source.source_url) })),
    };
  }

  /* ------------------------------------------------------------------------
   * Recorded historical lines: the act map
   * --------------------------------------------------------------------- */

  /* PORT: history.js:1873-1880 chosenSlice; the page's `?slice=` is the
   * reader's own choice here. `default` is read, never row order. */
  function chosenSlice(asked) {
    if (/^[a-z0-9][a-z0-9-]*$/.test(asked || '')) return asked;
    const manifest = file('index.json');
    const slices = (manifest && manifest.slices) || [];
    const declared = (manifest && manifest.default) || '';
    if (slices.some((row) => row && row.id === declared)) return declared;
    return (slices.length && slices[0] && slices[0].id) || '';
  }

  /* Read one slice and set the page's vocabulary and kind rule for it, as
   * history.js start() does (1812-1818). */
  function sliceOf(asked) {
    const slice = chosenSlice(asked);
    if (!slice) throw new Error('structure/act-history/index.json names no slice to open');
    const spine = file(slice + '.json');
    P.readVocabulary(spine);
    const stations = spine.stations || [];
    const vocab = P.readVocabulary(spine);
    const stated = M.kindsAreStated(stations);
    P.setKindsStated(stated);
    const byId = new Map(stations.map((s) => [s.id, s]));
    const lineLabel = (id) => { // page: history.js:705-708
      const line = (spine.lines || []).find((row) => row.id === id);
      return (line && line.label) || id;
    };
    const nameOf = (station) => (station && (station.title || M.shortName(station.id))) || ''; // page: history.js:701-703
    return { slice, spine, vocab, stations, stated, byId, lineLabel, nameOf, kindOf: (s) => M.kindOf(s, stated) };
  }

  function map(asked) {
    const S = sliceOf(asked);
    const { spine, stations, byId } = S;
    const panels = stations.length ? M.panelLayout(stations, spine.lines) : [];
    const outgoing = new Map();
    panels.forEach((panel) => panel.edges.forEach((edge) => {
      if (!edge.external) return;
      if (!outgoing.has(edge.from)) outgoing.set(edge.from, []);
      outgoing.get(edge.from).push(edge);
    }));
    // PORT: history.js:1749-1805 describeLegend
    const counts = new Map();
    stations.forEach((s) => counts.set(S.kindOf(s), (counts.get(S.kindOf(s)) || 0) + 1));
    const legend = [M.PROMULGATED, M.PRINTED, M.UNSTATED].filter((kind) => counts.get(kind)).map((kind) => ({
      mark: kind, text: counts.get(kind) + ' ' + kind + (kind === M.PROMULGATED ? ' — an act stands behind it'
        : kind === M.PRINTED ? ' — a printing survives and no act has been located' : ' — this file says nothing about which'),
    }));
    const receptions = stations.reduce((n, s) => n + P.receptionsOf(s).length, 0);
    if (receptions) legend.push({ mark: 'reception', text: receptions + ' documented reception' + (receptions === 1 ? '' : 's') +
      ' — a hollow track enters a double-ring station; open it for the instrument and evidence' });
    legend.push({ mark: '', text: 'A crossing without a station marker asserts no connection. Parent links ' +
      'follow the recorded evidence; order alone does not establish textual descent.' });
    legend.push({ mark: 'stated', text: 'Wider line: an act or book states the parent link' });
    legend.push({ mark: 'attributed', text: 'Medium line: a cited scholarly attribution' });
    legend.push({ mark: 'sequence', text: 'Narrower line: recorded sequence; textual descent not established' });
    const broken = stations.filter((s) => (s.via_unrepresented || []).length).length;
    if (broken) legend.push({ mark: 'broken', text: broken + ' broken connector' + (broken === 1 ? '' : 's') +
      ' — the descent crosses an edition this record does not carry' });
    const roots = stations.filter((s) => !(s.parents || []).length).length;
    return {
      slice: S.slice, vocabulary: spine.vocabulary || '',
      heading: 'Recorded historical lines', // page: history.js:848
      note: 'Read dates downward within each line. Spacing separates recorded stations, not elapsed years. ' +
        'Separate starting points mark the limits of this record, not independent historical origins. ' +
        'An ending here does not establish suppression or extinction.', // page: history.js:850-853
      empty: stations.length ? '' : 'This slice records no stations.', // page: history.js:842
      // page: history.js:1825-1828
      tally: stations.length + ' stations on ' + (spine.lines || []).length + ' recorded lines; ' + roots +
        ' unconnected starting points in this record. This is the selected historical slice, not a comprehensive history.',
      legend,
      follow_word: P.followWord(),
      panels: panels.map((panel) => ({
        number: panel.number, line: panel.line, heading: panel.number + '. ' + panel.label, tracks: panel.tracks,
        // page: history.js:871-872
        note: panel.nodes.length + ' recorded stations · ' + panel.nodes[0].date + ' – ' + panel.nodes[panel.nodes.length - 1].date + ' · dates increase ↓',
        nodes: panel.nodes.map((node) => {
          const station = byId.get(node.id);
          const kind = S.kindOf(station);
          const moved = P.magnitude(station);
          const notes = [];
          panel.edges.filter((edge) => edge.to === node.id && edge.external).forEach((edge) => notes.push( // page: history.js:905
            (edge.reception ? 'Reception from ' : 'Parent link from ') + edge.fromTitle + ' · line ' + edge.fromPanel));
          (outgoing.get(node.id) || []).forEach((edge) => notes.push('Linked to ' + edge.toTitle + ' · line ' + edge.toPanel)); // page: history.js:912
          if (station.parent_kind === 'use-continuity' || station.parent_kind === 'line-order') {
            notes.push('Sequence in this record; textual descent is not established by this link.'); // page: history.js:918-919
          }
          if ((station.via_unrepresented || []).length) {
            notes.push('Broken link: intervening edition or act not represented here.'); // page: history.js:920-921
          }
          return {
            id: node.id, track: node.track, date: station.date, kind, title: station.title,
            // page: history.js:888-889 — "changed" only where an act stands behind it.
            count: 'Recorded units: ' + (kind === M.PROMULGATED ? (moved ? moved + ' changed' : 'nothing changed')
              : (moved ? moved + ' differ' : 'nothing differs')),
            summary: P.changeSummary(station),
            interchange: P.receptionsOf(station).length > 0,
            notes,
          };
        }),
        edges: panel.edges.map((edge) => {
          const child = byId.get(edge.to);
          return { from: edge.from, to: edge.to, external: edge.external, from_panel: edge.fromPanel, reception: edge.reception,
            evidence: child.parent_kind || 'unstated', broken: (child.via_unrepresented || []).length > 0 };
        }),
      })),
      // page: history.js:1841-1843 — with no other instruction, the last station the record reaches.
      default_station: stations.length ? stations[stations.length - 1].id : null,
      has_commonality: (spine.commonality || []).length > 0,
    };
  }

  /* page: history.js:1072-1078 value() — three states, never two. */
  function value(text, missing, withheld) {
    if (text) return { state: 'present', text };
    if (withheld) return { state: 'withheld', text: 'withheld here: ' + withheld };
    return { state: 'missing', text: missing };
  }

  function fieldRow(field, before, after, wasSide, nowSide) { // PORT: history.js:1086-1108
    const long = field === 'text' || field === 'incipit';
    const missing = long ? 'this record does not carry these words' : 'not established';
    const shown = (raw, side) => value(raw === undefined || raw === null ? '' : String(raw), missing, long ? (side || {}).withheld : '');
    return { name: P.FIELD_NAMES[field] || field, before: shown(before, wasSide), after: shown(after, nowSide) };
  }

  function standing(side) { // PORT: history.js:1181-1189
    return { incipit: value(side.incipit || '', 'this record does not carry these words', side.withheld), text: side.text || '' };
  }

  function basis(row) { // PORT: history.js:1127-1138 citations
    return (row.cited || []).filter((entry) => entry.basis || entry.note).map((entry) => ({ kind: entry.kind || 'basis', text: entry.basis || entry.note }));
  }

  function unitCard(row) { // PORT: history.js:1140-1179
    const after = row.after || {}, before = row.before || {};
    const card = {
      unit: row.unit, state: row.state, title: after.name || before.name || row.unit, kinds: P.whatHappened(row),
      where: (after.mass || before.mass || '') + ' · ' + (after.slot || before.slot || '') + ' · ' + row.unit,
      marker: row.marker || '', basis: basis(row),
    };
    if (row.state === 'changed') {
      card.fields = (row.fields || []).map((field) => fieldRow(field, before[field], after[field], before, after));
      if (!(row.fields || []).length) card.same = 'The act records a departure here and the state it leaves is the same ' +
        'in every field this record carries.';
    } else card.standing = standing(row.state === 'gone' ? before : after);
    return card;
  }

  function massCard(row) { // PORT: history.js:1191-1206
    const after = row.after || {}, before = row.before || {};
    return { title: after.title || before.title || row.mass, kinds: P.whatHappened(row), where: row.mass || '',
      fields: (row.fields || []).map((field) => fieldRow(field, before[field], after[field])), basis: basis(row) };
  }

  function receptionRows(rows, S) { // PORT: history.js:1217-1237 renderReceptions
    return rows.map((row) => ({
      from: row.from, title: 'Receives from ' + (S.nameOf(S.byId.get(row.from)) || row.from),
      facts: [['Relationship', P.RECEPTION_WORDS[row.kind] || row.kind], ['Instrument', row.instrument],
        ['Citation', row.citation], ['Basis', row.basis]].filter((entry) => entry[1]),
    }));
  }

  function station(asked, id) { // PORT: history.js:1441-1531 open, with facts 1014-1043 and renderChanges 1239-1315
    const S = sliceOf(asked);
    const s = S.byId.get(id);
    if (!s) {
      // page: history.js:1428-1431
      return { missing: 'This record carries no station with the id “' + id + '”. That is a ' +
        'statement about this record and not about the history: nothing here ' +
        'hands you a neighbouring act instead, because a neighbouring act is a ' +
        'different act.' };
    }
    const kind = S.kindOf(s);
    const facts = [
      ['Date', s.date + (s.date_precision && s.date_precision !== 'day' ? ' (' + s.date_precision + ')' : '')],
      ['Station', kind], ['Authority', s.authority], ['Instrument', s.instrument], ['Act', s.kind],
      ['Printing', s.printing], ['Line', S.lineLabel(s.line)], ['Descent', s.parent_kind],
      ['Instrument read', s.act_citation ? s.act_citation + ' — ' + (P.CITATION_WORDS[s.act_citation] || '') : null],
      ['Citation', s.citation],
      ['Effect', s.effect ? s.effect + (s.effect_established ? '' : ' (what it changed here is not established)') : null],
    ].filter((row) => row[1]).map((row) => [row[0], String(row[1])]);
    const view = { id: s.id, slice: S.slice, title: S.nameOf(s), kind, facts, summary: P.changeSummary(s) };
    let received = P.receptionsOf(s);
    // page: history.js:1045-1068 kindNote
    if (kind === M.PRINTED) view.kind_note = 'A printed station. The printing it stands on survives and no act has ' +
      'been located for it, so nothing here claims one. That is a statement ' +
      'about the evidence and not about the size of the change: the printing ' +
      'is present, the instrument is missing.';
    else if (kind === M.UNSTATED) view.kind_note = 'This file states which kind the other stations are and states nothing ' +
      'for this one, so it is left unsaid rather than assumed.';
    if ((s.via_unrepresented || []).length) { // page: history.js:1472-1476
      view.gap_note = 'The descent into this station runs through ' + s.via_unrepresented.join(', ') +
        ', which this record does not carry. The connector is drawn broken for ' +
        'that reason: the edge means “descends from”, not “immediately follows”.';
    }
    if ((s.departures || []).length) view.departures = 'Departures recorded at this act: ' + s.departures.join(', ') + '.';
    if ((s.parents || []).length > 1) { // page: history.js:1485-1493
      const names = s.parents.map((p) => S.nameOf(S.byId.get(p)) || p);
      view.parents_note = 'This station records ' + s.parents.length + ' parents. Its own changes are shown below; the parent stations are ' +
        names.slice(0, -1).join(', ') + ' and ' + names[names.length - 1] + '.';
    }
    if (s.station_path) { // page: history.js:1496-1497 — the generator names the fragment.
      let payload = null;
      try { payload = file(s.station_path); } catch (error) {
        view.change_error = 'What changed here could not be read: ' + String(error.message || error); // page: history.js:1510
      }
      if (payload) {
        if ((payload.edges || {}).receptions) received = payload.edges.receptions;
        const changes = { summary: P.changeSummary(s) + '.' };
        if (kind !== M.PROMULGATED) { // page: history.js:1251-1256
          changes.printed_caveat = 'No act has been located for this station, so nothing below was ordered ' +
            'by anybody as far as this record knows. What is shown is how this book ' +
            'differs from the one before it — a difference between printings, which ' +
            'is a far weaker thing than a change an authority made, and is not ' +
            'evidence that anyone decided it.';
        }
        const edges = payload.edges || {};
        changes.rests_on = Object.keys(P.EDGE_WORDS).filter((key) => edges[key]).map((key) => [P.EDGE_WORDS[key], String(edges[key])]);
        const groups = P.groupsIn(payload);
        changes.groups_title = 'The ' + P.plural(P.groupWord());
        changes.groups = groups.map(massCard);
        changes.units_title = 'The ' + P.plural(P.unitWord());
        changes.units = (payload.units || []).map(unitCard);
        if ((payload.unestablished || []).length) {
          changes.unestablished_note = 'The act is known to have acted on these and this record does not know ' +
            'what it left. They are removed rather than carried forward, because ' +
            'carrying them forward would assert that nothing changed.'; // page: history.js:1283-1285
          changes.unestablished = payload.unestablished.map((row) => ({ unit: row.unit, marker: row.marker }));
        }
        if (!groups.length && !(payload.units || []).length && !(payload.unestablished || []).length) {
          const totals = payload.totals || {};
          const count = totals.standing || 0;
          const heldWords = P.tallyOf(count, P.unitWord()) + (count === 1 ? ' stands after it.' : ' stand after it.');
          changes.empty = kind === M.PROMULGATED // page: history.js:1307-1314
            ? 'This act moved nothing in this slice. It keeps its station because ' +
              'an authority acted: a history keyed on diffs would have dropped it, ' +
              'and a history keyed on acts records that the authority spoke and ' +
              'this part of the book did not move. ' + heldWords
            : 'Nothing in this slice differs from what stood before. The book is ' +
              'here because it survives, and this part of it reads as the last one ' +
              'did. ' + heldWords;
        }
        view.changes = changes;
      }
    } else {
      view.change_error = 'This map file names no change set for this station, so none is shown. ' +
        'Working one out here would be a second answer to a question the ' +
        'generator already answers.'; // page: history.js:1515-1517
    }
    if (received.length) {
      view.receptions = receptionRows(received, S);
      view.reception_note = 'These links record reception between lines. They carry ancestry, not a ' +
        'copy of the received parent’s text; this station’s own changes are shown below.'; // page: history.js:1221-1222
    }
    if (s.state_path) { // page: history.js:1521-1524
      view.state_label = S.vocab.unit_named
        ? 'Read the ' + P.plural(S.vocab.unit_named) + ' as they stood after this act'
        : 'Read the recorded units as they stood after this act';
    }
    return view;
  }

  function state(asked, id) { // PORT: history.js:1317-1374 renderState
    const S = sliceOf(asked);
    const s = S.byId.get(id);
    if (!s || !s.state_path) return { error: 'This record names no recorded state for that station.' };
    let payload;
    try { payload = file(s.state_path); } catch (error) {
      return { error: BASE + s.state_path + ' could not be read: ' + String(error.message || error) };
    }
    const totals = payload.totals || {};
    return {
      title: payload.title,
      summary: P.tallyOf(totals.units || 0, P.unitWord()) + ' across ' + P.tallyOf(totals[S.vocab.group_key] || 0, P.groupWord()) +
        ', as this record holds them after ' + payload.title + '.',
      note: 'These counts describe recorded units, not complete transcriptions. ' +
        'A unit may carry only its heading or incipit; unread and withheld words ' +
        'are marked where the text would stand.',
      witnessed: payload.station_kind && payload.station_kind !== M.PROMULGATED
        ? 'This is what the surviving book prints at this point. No act stands ' +
          'behind it in this record, so it is a state witnessed and not a state ' +
          'ordered.' : '',
      groups: P.groupsIn(payload).map((mass) => ({
        title: mass.title || mass[P.groupWord()] || '',
        meta: [mass.day, mass.hour].filter(Boolean).join(' · '),
        empty: (mass.units || []).length ? '' : 'This record carries no ' + P.unitWord() + ' standing in this ' + P.groupWord() + ' at this point.',
        units: (mass.units || []).map((unit) => ({
          name: unit.name || unit.slot, slot: unit.slot, unit: unit.unit,
          incipit: value(unit.incipit || '', 'this record read the heading of this unit and not its words', unit.withheld),
          text: unit.text || '',
        })),
      })),
      unestablished_heading: (payload.unestablished || []).length ? 'Not established at this point' : '',
      unestablished: (payload.unestablished || []).map((row) => row.marker),
    };
  }

  function units(asked) { // PORT: history.js:1601-1619 loadIndex
    const S = sliceOf(asked);
    let payload;
    try { payload = file(S.slice + '/units.json'); } catch (error) {
      return { error: 'The unit index could not be read: ' + String(error.message || error) }; // page: history.js:1628
    }
    return { follow_word: P.followWord(), units: (payload.units || []).map((unit) => ({
      value: unit.unit, group: unit.mass,
      label: (unit.name || unit.slot) + ' — ' + unit.slot + (unit.standing ? '' : ' (absent by ' + unit.left_at + ')'),
    })) };
  }

  function unit(asked, id) { // PORT: history.js:1578-1585 openUnit and 1537-1576 renderUnit
    const S = sliceOf(asked);
    let index = null;
    try { index = file(S.slice + '/units.json'); } catch (error) { index = null; }
    const row = index && (index.units || []).find((one) => one.unit === id);
    // The record's own path; the page composes one only for a unit with no index row.
    const where = row && row.path ? row.path : S.slice + '/unit/' + id + '.json';
    let payload;
    try { payload = file(where); } catch (error) {
      return { error: 'That unit’s history could not be read: ' + String(error.message || error) }; // page: history.js:1588
    }
    return {
      title: payload.name || payload.unit,
      summary: (payload.name || payload.unit) + ' — ' + payload.stations.length + ' act' + (payload.stations.length === 1 ? '' : 's') +
        ' touched it. It enters this record at ' + payload.entered_at + '. ' +
        (payload.standing ? 'It still stands at the end of the line drawn here.' : 'It leaves the liturgy at ' + payload.left_at + '.'),
      stops: payload.stations.map((stop) => {
        const card = { act: stop.act, title: stop.title || stop.act, kinds: P.whatHappened(stop), state: stop.state,
          where: stop.date + ' · ' + (stop.instrument || 'instrument not carried here'), basis: basis(stop) };
        if (stop.state === 'changed') {
          card.fields = (stop.fields || []).map((field) => fieldRow(field, (stop.before || {})[field], (stop.after || {})[field], stop.before, stop.after));
        } else card.standing = standing(stop.state === 'gone' ? (stop.before || {}) : (stop.after || {}));
        return card;
      }),
    };
  }

  function junctions(asked) { // PORT: history.js:1684-1747 renderJunctions and 1655-1682 sideOfJunction
    const S = sliceOf(asked);
    const pairs = S.spine.commonality || [];
    if (!pairs.length) return { none: 'This record holds one line, so there is no pair to compare.' };
    const side = (base, line) => {
      const after = base ? M.afterBase(S.stations, base, line) : S.stations.filter((s) => s.line === line).map((s) => s.id);
      return { line: S.lineLabel(line), empty: after.length ? '' : 'Nothing below the base stands on this line in this record. An empty ' +
        'branch that is honestly empty measures what this corpus holds, not what happened.',
        stations: after.map((id) => ({ id, title: S.nameOf(S.byId.get(id)) || id, summary: S.byId.get(id) ? P.changeSummary(S.byId.get(id)) : '' })) };
    };
    const unconnected = pairs.filter((pair) => !(pair.shared_base || []).length);
    return {
      unconnected_heading: unconnected.length ? unconnected.length + ' line pairs have no shared act recorded' : '',
      unconnected_note: 'Earlier ancestry and shared wording are not established by this graph. ' +
        'These are gaps in the encoded evidence, not proof of isolation. The traditions and connections overview ' +
        'carries separate source-cited research claims and bounded text comparisons.',
      unconnected: unconnected.map((pair) => S.lineLabel(pair.a) + ' / ' + S.lineLabel(pair.b)),
      pairs: pairs.filter((pair) => (pair.shared_base || []).length).map((pair) => {
        const bases = pair.shared_base;
        const parted = pair.diverged_at || bases[bases.length - 1];
        return {
          heading: S.lineLabel(pair.a) + ' and ' + S.lineLabel(pair.b),
          base: 'The last act both lines descend from is ' + (S.nameOf(S.byId.get(parted)) || parted) +
            '. This is shared ancestry in the recorded graph. A reception does ' +
            'not copy text between lines, so a shared ancestor alone does not ' +
            'establish identical texts. The stations below show each line’s later record.',
          several: bases.length > 1 ? 'This pair has more than one best common ancestor — ' + bases.join(', ') +
            ' — which means the descent above them is itself branched. All of them are shown as bases rather than one being picked.' : '',
          sides: [side(parted, pair.a), side(parted, pair.b)],
        };
      }),
    };
  }

  /* ------------------------------------------------------------------------
   * The source catalogue
   * --------------------------------------------------------------------- */

  function entryCard(row) { // PORT: history.js:2646-2650
    return {
      id: row.id, date: row.date_label || 'Date unresolved', title: row.title, linked: Boolean(row.act_ref),
      mark: row.act_ref ? '● Recorded edition or reform' : '○ Historical book candidate',
      basis: row.chronology ? 'Date basis: ' + [row.chronology.kind, row.chronology.certainty].filter(Boolean).join(' · ') : '',
      group: (row.presentation_group ? row.presentation_group.label : row.family) + ' · ' + row.record_kind,
      statuses: 'Evidence: ' + row.evidence_status + ' · Acquisition: ' + (row.acquisition_status || 'not recorded') +
        ' · Text: ' + row.text_status + ' · Version: ' + row.substantive_status,
    };
  }

  /* PORT: history.js:2586-2621 render — the filter, the two sections, the sort. */
  function catalogue(filter) {
    const { data, overview } = loaded();
    filter = filter || {};
    const families = overview.groups.map((g) => 'group:' + g.id);
    const selectedFamily = filter.family || '';
    const search = String(filter.q || '').slice(0, 200);
    const terms = search.toLocaleLowerCase().split(/\s+/).filter(Boolean);
    const rows = data.entries.filter((row) => {
      const haystack = [row.title, row.family, row.presentation_group && row.presentation_group.label, row.date_label, row.id,
        JSON.stringify(row.source_record)].join(' ').toLocaleLowerCase();
      return (!selectedFamily || row.family === selectedFamily ||
        'group:' + (row.presentation_group ? row.presentation_group.id : 'unmapped:' + row.family) === selectedFamily) &&
        terms.every((term) => haystack.indexOf(term) !== -1);
    });
    let unknown = '';
    if (selectedFamily && families.indexOf(selectedFamily) === -1) { // page: history.js:2595-2597
      const legacy = data.entries.some((row) => row.family === selectedFamily);
      unknown = selectedFamily + (legacy ? ' (source family)' : ' (not in this catalogue)');
    }
    const group = overview.groups.find((g) => 'group:' + g.id === selectedFamily);
    const sections = [
      { title: 'Chronological books and reforms', rows: rows.filter((row) => row.chronology)
        .sort((a, b) => a.chronology.start - b.chronology.start || a.title.localeCompare(b.title)) },
      { title: 'Undated or unresolved', rows: rows.filter((row) => !row.chronology) },
    ].filter((section) => section.rows.length).map((section) => ({
      title: section.title + ' (' + section.rows.length + ')',
      note: section.title === 'Chronological books and reforms' // page: history.js:2624-2625
        ? 'Read from earlier to later recorded dates. ○ marks a historical book candidate; ● marks an edition or reform linked to a historical line. ' +
          'Date ranges retain their source qualifications. Adjacent entries do not imply descent.' : '',
      rows: section.rows.map(entryCard),
    }));
    return {
      filter: { family: selectedFamily, q: search, label: group ? group.label : unknown || 'All record groups' },
      // page: history.js:2571-2572
      tally: data.entries.length + ' source records across ' + families.length +
        ' source-defined record groups. These are navigation groups, not a census of rites and not a count of complete books.',
      status: rows.length + ' of ' + data.entries.length + ' source records shown.', // page: history.js:2613
      none: rows.length ? '' : 'No records match these filters. Clear the search or choose another tradition.', // page: history.js:2614
      sections,
    };
  }

  function endpoint(end) { // PORT: history.js:2105-2155 relationDiagram endpoints
    return {
      group: end.group, title: end.title, date: end.date, entity: end.entity,
      status: end.entity ? 'Textual reference, shown without a date axis'
        : end.record.act_ref ? 'Recorded edition or reform' : 'Historical book candidate',
      meta: end.entity ? '' : end.record.record_kind + ' · Evidence: ' + end.record.evidence_status,
    };
  }

  function record(id) { // PORT: history.js:1992-2061 catalogueRecord and 2158-2167 appendRecordRelations
    const { data, overview, byEntry } = loaded();
    const row = byEntry.get(id);
    if (!row) return { missing: 'This source record is not in the catalogue: ' + id }; // page: history.js:2666
    const facts = [
      ['Record group', row.presentation_group ? row.presentation_group.label : row.family],
      ['Family in source inventory', row.family],
      ['Language as recorded', row.source_record.language || row.source_record.languages],
    ];
    if (row.source_record.language_scope || row.source_record.inclusion_status) {
      facts.push(['Language scope', row.source_record.language_scope || row.source_record.inclusion_status]);
    }
    facts.push(['Date as recorded', row.date_label]);
    if (row.chronology) facts.push(['Date interpretation', [row.chronology.kind, row.chronology.certainty].filter(Boolean).join(' · ')]);
    else facts.push(['Chronology', 'Undated or unresolved; no year has been inferred.']);
    facts.push(['Record kind', row.record_kind], ['Evidence status', row.evidence_status], ['Source acquisition', row.acquisition_status],
      ['Text status', row.text_status], ['Substantive-version status', row.substantive_status]);
    const sources = row.sources.map((source) => ({ label: P.catalogueText(source.label || source.id || source.url), url: P.catalogueURL(source.url),
      note: 'Inspection: ' + P.catalogueText(source.inspection) }));
    row.links.forEach((link) => {
      if (link.kind !== 'source-library-edition' && row.sources.some((source) => source.url === link.url)) return;
      if (link.kind === 'source-library-edition') sources.push({ label: 'Open edition in the Source Library', url: null, note: link.edition_id || '' });
      else sources.push({ label: P.catalogueText(link.label || link.kind || link.url), url: P.catalogueURL(link.url), note: '' });
    });
    const relations = overview.relations.filter((r) => r.from.id === row.id || r.to.id === row.id).map((r) => ({
      heading: 'R' + String(r.number).padStart(2, '0') + ' · ' + P.RELATION_WORDS[r.record.kind] + ' · ' + r.record.certainty,
      label: r.record.label && r.record.label !== r.record.kind ? r.record.label : '',
      directed: r.record.directed, from: endpoint(r.from), to: endpoint(r.to),
      basis: r.record.basis, scope: 'Scope: ' + r.record.scope, limitations: r.record.limitations,
      // page: history.js:2080-2081
      boundary: 'This research relationship does not create a historical station, a Git parent, or inherited text.',
      evidence: r.record.evidence.map((e) => ({ title: e.source.title, url: P.catalogueURL(e.source.url), locus: e.locus,
        inspection: 'Source inspection: ' + e.source.inspection_status + ' · ' + P.catalogueText(e.source.inspection) })),
      comparisons: (r.record.comparison_links || []).map((link) => (data.comparisons || []).find((c) => c.id === link.id)).filter(Boolean)
        .map((c) => ({ id: c.id, label: 'Read linked text comparison: ' + (c.label || c.title || c.id) })),
      id: 'Relationship ID: ' + r.record.id,
    }));
    return {
      id: row.id, title: row.title, mark: row.act_ref ? '● Recorded edition or reform' : '○ Historical book candidate',
      facts: facts.map((f) => [f[0], P.catalogueText(f[1])]),
      separate: 'The statuses above are separate findings. A catalogue identification or a held scan does not ' +
        'establish a substantive version, a collated text, or a complete book. The original record below ' +
        'preserves the stated basis and unresolved work.', // page: history.js:2025-2027
      act_ref: row.act_ref,
      act_none: row.act_ref ? '' : 'No accepted act-history station is linked to this record.', // page: history.js:2035-2036
      relations_heading: 'Recorded research connections',
      relations_none: relations.length ? '' : 'Connections for this record have not yet been investigated or established here. This does not establish historical isolation.',
      relations,
      sources_heading: 'Sources and access',
      sources, sources_none: sources.length ? '' : 'No source access link is recorded.',
      original_heading: 'Original inventory metadata',
      origin: [row.origin.inventory, row.origin.table, row.origin.id].map(P.catalogueText).join(' · '),
      source_record: JSON.stringify(row.source_record, null, 2),
    };
  }

  return { opening, timeline, stage, transition, native, comparison, map, station, state, units, unit, junctions, catalogue, record };
};
