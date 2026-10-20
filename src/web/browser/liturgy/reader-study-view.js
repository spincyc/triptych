/* Contextual Study apparatus over one already resolved reader result.
 * It reports selected facts and source identities. It does not resolve a
 * calendar, choose text, quote a held body, or infer a historical change.
 */
'use strict';

(function (root, factory) {
  const api = factory(root);
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  else root.LiturgyReaderStudyView = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function (root) {
  const SCHEMA = 'triptych-liturgy-reader-study-view/v1';

  function fail(message) { throw new Error('reader Study view: ' + message); }
  function nonempty(value) { return typeof value === 'string' && Boolean(value.trim()); }

  function selectedFacts(selected) {
    if (!selected || typeof selected !== 'object' || Array.isArray(selected)) return null;
    const facts = {};
    ['kind', 'availability', 'language', 'sourceId', 'rights', 'reason',
      'unavailableState', 'bible', 'numbering', 'cycle', 'cycleDimension',
      'extent', 'relation', 'collation'].forEach(function (key) {
      if (nonempty(selected[key])) facts[key] = selected[key];
    });
    if (Array.isArray(selected.references)) {
      facts.references = selected.references.filter(nonempty);
    }
    // Text and alternative bodies are intentionally absent from Study's
    // evidence model, including when an unavailable row improperly carries it.
    return facts;
  }

  function seatFacts(seat) {
    if (!seat || typeof seat !== 'object' || Array.isArray(seat)) return null;
    const facts = {};
    ['id', 'placement', 'anchor', 'where', 'region', 'basis'].forEach(function (key) {
      if (nonempty(seat[key])) facts[key] = seat[key];
    });
    return facts;
  }

  function sourceFacts(hooks) {
    if (!Array.isArray(hooks)) return [];
    return hooks.filter(function (one) {
      return one && nonempty(one.kind) && nonempty(one.id);
    }).map(function (one) { return { kind: one.kind, id: one.id }; });
  }

  function coverageFacts(rows) {
    return rows.map(function (row) {
      if (!row || !nonempty(row.state) || !nonempty(row.scope)) {
        fail('coverage needs a typed state and scope');
      }
      return {
        state: row.state, scope: row.scope,
        completeness: nonempty(row.completeness) ? row.completeness : null,
        reasons: (row.reasons || []).map(function (reason) {
          return {
            kind: reason && nonempty(reason.kind) ? reason.kind : 'unclassified',
            basis: reason && nonempty(reason.basis) ? reason.basis : null,
            applicability: reason && nonempty(reason.applicability)
              ? reason.applicability : null
          };
        })
      };
    });
  }

  function project(result) {
    if (!result || ['day', 'propers'].indexOf(result.entrance) < 0 ||
        !result.request || !result.request.edition ||
        !Array.isArray(result.events) || !Array.isArray(result.coverage) ||
        !Array.isArray(result.unresolvedChoices)) {
      fail('a resolved reader adapter result is required');
    }
    if (result.entrance === 'day' && !result.calendarResult) {
      fail('Day Study needs its calendar result');
    }
    if (result.entrance === 'propers' && result.calendarResult !== null) {
      fail('Propers Study is date-independent');
    }
    const ids = new Set();
    const events = result.events.map(function (event) {
      if (!event || !nonempty(event.id) || !nonempty(event.kind) || ids.has(event.id)) {
        fail('events need distinct stable identities');
      }
      ids.add(event.id);
      return {
        id: event.id, location: event.id, kind: event.kind,
        label: event.editionSlotLabel || event.name || event.id,
        semanticSlot: event.semanticSlot && event.semanticSlot.state === 'mapped'
          ? event.semanticSlot.identity.id : null,
        seat: seatFacts(event.seat), selected: selectedFacts(event.selected),
        sourceHooks: sourceFacts(event.sourceHooks)
      };
    });
    const calendar = result.entrance === 'day' ? {
      calendar: result.calendarResult.calendar,
      date: result.calendarResult.date,
      territory: result.calendarResult.territory || 'universal',
      winner: result.calendarResult.winner || null,
      selectedBranch: result.calendarResult.selectedBranch || null,
      settled: result.calendarResult.settled,
      season: result.calendarResult.season || null,
      week: result.calendarResult.week || null,
      lectionary: result.calendarResult.lectionary || null
    } : null;
    return {
      schema: SCHEMA, entrance: result.entrance,
      edition: result.request.edition.id,
      resolved: result.resolved && {
        formulary: result.resolved.formulary || null,
        form: result.resolved.form || null,
        standing: result.resolved.standing || null,
        type: result.resolved.type || null
      },
      calendar: calendar, coverage: coverageFacts(result.coverage),
      unresolvedChoices: result.unresolvedChoices.map(function (choice) {
        return {
          id: choice.id,
          reason: choice.reason || null,
          options: (choice.options || []).map(function (one) { return one.id; }),
          sourceHooks: sourceFacts(choice.sourceHooks)
        };
      }),
      events: events
    };
  }

  // Attach to the same source-rendered fragment used by Read or Missal. Study may
  // describe a held event, but it must never manufacture or replace its text.
  function attach(input) {
    const T = root.Triptych;
    if (!T || typeof T.el !== 'function' || !root.document ||
        typeof root.document.createDocumentFragment !== 'function') {
      fail('a browser DOM and production element helper are required');
    }
    const study = project(input && input.result);
    const fragment = input && input.fragment;
    const contents = input && input.contents;
    const prefix = input && input.locationPrefix || '';
    if (!fragment || fragment.nodeType !== 11 || typeof fragment.contains !== 'function' ||
        !Array.isArray(contents) ||
        typeof prefix !== 'string') {
      fail('a source-rendered DocumentFragment, Contents, and location prefix are required');
    }
    const byId = new Map();
    contents.forEach(function (row) {
      if (!row || !nonempty(row.id) || !row.element || byId.has(row.id)) {
        fail('source Contents need distinct identities and elements');
      }
      if (!fragment.contains(row.element)) {
        fail('source Contents elements must belong to the supplied reading');
      }
      byId.set(row.id, row.element);
    });
    // Ordinary elements need not be separate Contents destinations. Attach to
    // every rendered source event while keeping the source navigation intact.
    Array.from(fragment.querySelectorAll('[data-semantic-event-id]')).forEach(function (host) {
      const id = host.dataset.semanticLocation;
      if (!nonempty(id) || byId.has(id) && byId.get(id) !== host) {
        fail('source event DOM needs distinct semantic locations');
      }
      byId.set(id, host);
    });
    // A source placeholder can lack a Read node; its coverage remains in the
    // overview, while only rendered source events receive inline notes.
    const attached = study.events.map(function (event) {
      return { event: event, host: byId.get(prefix + event.id) };
    }).filter(function (row) { return Boolean(row.host); });
    attached.forEach(function (row) {
      if (!row.host.dataset || row.host.dataset.semanticEventId !== row.event.id ||
          row.host.dataset.semanticLocation !== prefix + row.event.id) {
        fail('source Contents and event DOM identities disagree');
      }
    });

    function section(parent, title, className) {
      const node = T.el('section', className);
      node.appendChild(T.el('h2', null, title));
      parent.appendChild(node);
      return node;
    }

    function fact(list, label, value) {
      if (value === null || value === undefined || value === '') return;
      list.appendChild(T.el('dt', null, label));
      list.appendChild(T.el('dd', null, String(value)));
    }

    const overview = T.el('div', 'study-overview');
    const intro = section(overview, 'Study this selection', 'study-intro');
    intro.appendChild(T.el('p', null,
      'The reading below retains its source text. This apparatus reports selected calendar, coverage, placement, and source identities.'));
    const identity = T.el('dl', 'study-facts');
    fact(identity, 'Edition', study.edition);
    fact(identity, 'Formulary', study.resolved && study.resolved.formulary);
    fact(identity, 'Form', study.resolved && study.resolved.form);
    fact(identity, 'Standing', study.resolved && study.resolved.standing);
    intro.appendChild(identity);
    if (study.calendar) {
      const node = section(overview, 'Calendar result', 'study-calendar');
      const facts = T.el('dl', 'study-facts');
      fact(facts, 'Civil date', study.calendar.date);
      fact(facts, 'Calendar', study.calendar.calendar);
      fact(facts, 'Territorial branch', study.calendar.territory);
      fact(facts, 'Winner', study.calendar.winner);
      fact(facts, 'Selected branch', study.calendar.selectedBranch);
      fact(facts, 'Settled', study.calendar.settled === true ? 'Yes' :
        (study.calendar.settled === false ? 'No' : null));
      fact(facts, 'Season', study.calendar.season);
      fact(facts, 'Week', study.calendar.week);
      if (study.calendar.lectionary) {
        fact(facts, 'Sunday cycle', study.calendar.lectionary.sunday);
        fact(facts, 'Weekday cycle', study.calendar.lectionary.weekday);
      }
      node.appendChild(facts);
    } else {
      intro.appendChild(T.el('p', 'study-date-absence',
        'Propers is date-independent; no calendar result is assigned here.'));
    }

    if (study.coverage.length) {
      const node = section(overview, 'Coverage', 'study-coverage');
      study.coverage.forEach(function (row) {
        const item = T.el('div', 'study-coverage-row');
        const facts = T.el('dl', 'study-facts');
        fact(facts, 'Scope', row.scope);
        fact(facts, 'State', row.state);
        fact(facts, 'Completeness', row.completeness);
        row.reasons.forEach(function (reason) {
          fact(facts, 'Reason', reason.kind);
          fact(facts, 'Source basis', reason.basis);
          fact(facts, 'Applicability', reason.applicability);
        });
        item.appendChild(facts);
        node.appendChild(item);
      });
    }

    if (study.unresolvedChoices.length) {
      const node = section(overview, 'Unresolved choices', 'study-choices');
      study.unresolvedChoices.forEach(function (choice) {
        const item = T.el('div', 'study-choice');
        const facts = T.el('dl', 'study-facts');
        fact(facts, 'Choice', choice.id);
        fact(facts, 'Reason', choice.reason);
        fact(facts, 'Source options', choice.options.join('; '));
        choice.sourceHooks.forEach(function (hook) {
          fact(facts, 'Source record', hook.kind + ': ' + hook.id);
        });
        item.appendChild(facts);
        node.appendChild(item);
      });
    }

    attached.forEach(function (row) {
      const event = row.event;
      const host = row.host;
      const node = T.el('aside', 'study-event');
      node.dataset.studyEventId = event.id;
      node.appendChild(T.el('h3', null, 'Study notes for ' + event.label));
      const facts = T.el('dl', 'study-facts');
      fact(facts, 'Event', event.id);
      fact(facts, 'Kind', event.kind);
      fact(facts, 'Functional slot', event.semanticSlot);
      if (event.seat) {
        fact(facts, 'Seat', event.seat.id);
        fact(facts, 'Placement', event.seat.placement);
        fact(facts, 'Seat region', event.seat.region);
        fact(facts, 'Seat basis', event.seat.basis);
      }
      if (event.selected) {
        fact(facts, 'Selected material', event.selected.kind);
        fact(facts, 'Availability', event.selected.availability);
        fact(facts, 'Language', event.selected.language);
        fact(facts, 'Witness', event.selected.sourceId);
        fact(facts, 'Rights', event.selected.rights);
        fact(facts, 'Availability reason', event.selected.reason);
        fact(facts, 'Unavailable state', event.selected.unavailableState);
        fact(facts, 'Bible', event.selected.bible);
        fact(facts, 'Numbering', event.selected.numbering);
        fact(facts, 'Cycle', event.selected.cycle);
        fact(facts, 'Citations', event.selected.references &&
          event.selected.references.join('; '));
        fact(facts, 'Witness relation', event.selected.relation);
        fact(facts, 'Collation', event.selected.collation);
      }
      event.sourceHooks.forEach(function (hook) {
        fact(facts, 'Source record', hook.kind + ': ' + hook.id);
      });
      node.appendChild(facts);
      // Ordinary divisions are heading events. Keep their apparatus adjacent
      // so a heading never contains an aside or another heading.
      if (/^H[1-6]$/.test(host.tagName || '')) host.after(node);
      else host.appendChild(node);
    });
    fragment.insertBefore(overview, fragment.firstChild);
    return {
      fragment: fragment, contents: contents,
      semanticIds: contents.map(function (one) { return one.id; })
    };
  }

  return Object.freeze({
    SCHEMA: SCHEMA, project: project, attach: attach
  });
}));
