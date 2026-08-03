/* Consumer projections for the shared liturgy reader-state contract.
 *
 * These adapters do not resolve a calendar, fetch a source, render a DOM, or
 * format a terminal. They project the existing MassAssembly result, generated
 * Proper/Ordinary structures, and mass-today JSON into one compact semantic
 * shape. OrdinarySeating remains the sole seating and event-order engine.
 */

'use strict';

(function (root, factory) {
  let api;
  if (typeof module === 'object' && module && module.exports) {
    api = factory(require('./reader-state.js'), require('./ordinary-seating.js'));
    module.exports = api;
  } else {
    api = factory(root.LiturgyReaderState, root.OrdinarySeating);
    root.LiturgyReaderStateAdapters = api;
  }
}(typeof globalThis !== 'undefined' ? globalThis : this, function (Contract, Seating) {
  if (!Contract || !Seating) throw new Error('reader-state adapters require contract and seating');

  function pad(value) {
    return String(value + 1).padStart(3, '0');
  }

  function properEventId(editionId, formularyId, index) {
    return 'proper/' + editionId + '/' + formularyId + '/' + pad(index);
  }

  const SEMANTIC_SLOTS = Object.freeze({
    'Introit': 'entrance-antiphon',
    'Entrance Antiphon': 'entrance-antiphon',
    'Collect': 'collect',
    'Epistle': 'reading-1',
    'First Reading': 'reading-1',
    'Gradual': 'gradual',
    'Responsorial Psalm': 'responsorial-psalm',
    'Second Reading': 'reading-2',
    'Alleluia': 'gospel-acclamation',
    'Tract': 'gospel-acclamation',
    'Gospel Acclamation': 'gospel-acclamation',
    'Gospel': 'gospel',
    'Offertory': 'offertory-chant',
    'Secret': 'prayer-over-offerings',
    'Prayer over the Offerings': 'prayer-over-offerings',
    'Communion': 'communion-antiphon',
    'Communion Antiphon': 'communion-antiphon',
    'Postcommunion': 'prayer-after-communion',
    'Prayer after Communion': 'prayer-after-communion'
  });

  function semanticSlot(proper) {
    const id = proper && SEMANTIC_SLOTS[proper.name];
    return id ? { state: 'mapped', identity: { id: id } } : {
      state: 'edition-local-unmapped',
      reason: 'generated Proper data has no cross-edition semantic slot identity'
    };
  }

  function properIndex(mass) {
    const held = new Map();
    (mass.propers || []).forEach(function (proper, index) { held.set(proper, index); });
    return held;
  }

  function cycleKeys(proper) {
    return Object.keys((proper && proper.cycles) || {}).sort().filter(function (key) {
      const row = proper.cycles[key] || {};
      return Boolean((row.citations || []).length || row.text);
    });
  }

  function dayCycle(proper, lectionary) {
    if (!lectionary) return null;
    const keys = cycleKeys(proper);
    if (keys.indexOf(lectionary.sunday) >= 0) return lectionary.sunday;
    if (keys.indexOf(lectionary.weekday) >= 0) return lectionary.weekday;
    return null;
  }

  function materialForCycle(proper, request, structure, cycle) {
    const cycleRows = cycle ? [cycle] : [];
    const citations = (proper.citations || []).slice();
    let cycleText = null;
    for (const key of cycleRows) {
      const row = (proper.cycles || {})[key] || {};
      for (const citation of row.citations || []) citations.push(citation);
      if (row.text) cycleText = row.text;
    }
    const references = citations.map(function (one) { return one.ref; }).filter(Boolean);
    if (references.length) {
      const unresolved = citations.filter(function (one) { return one.unresolved; }).map(function (one) {
        return { reference: one.ref, reason: one.unresolved };
      });
      return {
        kind: 'scripture',
        bible: request.bible && request.bible.id || null,
        numbering: request.bible && request.bible.numbering || null,
        cycle: cycle,
        cycles: cycleRows,
        references: references,
        availability: unresolved.length ? 'unavailable' : 'held',
        rights: null,
        unresolved: unresolved
      };
    }
    if (proper.text || cycleText) {
      const wanted = request.languages && request.languages.orations || 'la';
      if (wanted === 'la') {
        return {
          kind: 'composed', language: 'la', cycle: cycle,
          cycles: cycleRows, sourceId: null, rights: null, missing: false,
          availability: 'held', text: cycleText || proper.text
        };
      }
      const translations = (proper.translations || []).filter(function (one) {
        return one && one.lang === wanted && one.text;
      });
      const witness = request.languages && request.languages.translationWitness || null;
      const translation = witness
        ? translations.find(function (one) {
            return (one.source_id || one.source || null) === witness;
          })
        : (translations.length === 1 ? translations[0] : null);
      if (translation) {
        return {
          kind: 'composed', language: wanted, cycle: cycle, cycles: cycleRows,
          sourceId: translation.source_id || translation.source || null,
          rights: translation.rights || null, missing: false,
          availability: 'held', text: translation.text
        };
      }
      if (translations.length > 1 && !witness) {
        const witnessIds = translations.map(function (one) {
          return one.source_id || one.source || null;
        });
        if (witnessIds.some(function (id) { return !id; })) {
          return {
            kind: 'composed', language: wanted, cycle: cycle, cycles: cycleRows,
            sourceId: null, rights: null, missing: true, availability: 'unavailable',
            reason: 'translation-witness-identity-missing'
          };
        }
        return {
          kind: 'composed', language: wanted, cycle: cycle, cycles: cycleRows,
          sourceId: null, rights: null, missing: false, availability: 'choice-required',
          unresolvedWitnesses: witnessIds.slice().sort()
        };
      }
      return {
        kind: 'composed', language: wanted, cycle: cycle, cycles: cycleRows,
        sourceId: null, rights: null, missing: true, availability: 'unavailable',
        reason: 'translation-missing'
      };
    }
    if (proper.incipit) {
      return {
        kind: 'incipit-only', language: 'la', cycle: cycle, cycles: cycleRows,
        rights: null, availability: 'held'
      };
    }
    return {
      kind: 'absent', rights: null, availability: 'absent',
      reason: proper.name === 'Placeholder' ? 'not-transcribed' : 'semantic-absence'
    };
  }

  function selectedMaterial(proper, request, structure, cycleMode) {
    const keys = cycleKeys(proper);
    if (cycleMode === 'day') {
      return materialForCycle(proper, request, structure, dayCycle(proper, request.lectionary));
    }
    const explicitCycle = hasOwn(request, 'cycle') && request.cycle !== null;
    if (explicitCycle) {
      if (keys.length && keys.indexOf(request.cycle) < 0) {
        throw new Error('explicit cycle is not held for this Proper');
      }
      return materialForCycle(proper, request, structure, keys.length ? request.cycle : null);
    }
    if (keys.length === 0) return materialForCycle(proper, request, structure, null);
    if (keys.length === 1) return materialForCycle(proper, request, structure, keys[0]);
    return {
      kind: 'cycle-alternatives',
      cycle: null,
      availability: 'choice-required',
      rights: null,
      alternatives: keys.map(function (cycle) {
        return {
          id: cycle,
          cycle: cycle,
          material: materialForCycle(proper, request, structure, cycle),
          sourceHooks: []
        };
      })
    };
  }

  function sourceHooks(proper, selected, editionId, formularyId, index) {
    const hooks = [{
      kind: 'proper-structure',
      id: editionId + '/' + formularyId + '/' + pad(index)
    }];
    if (selected && selected.sourceId) hooks.push({ kind: 'translation', id: selected.sourceId });
    const taken = proper.taken_from;
    if (taken) {
      hooks.push({
        kind: 'taken-from',
        id: [taken.mass, taken.proper, taken.form, taken.citation].filter(Boolean).join('|')
      });
    }
    return hooks;
  }

  function projectProper(proper, index, mass, request, structure, cycleMode, seat) {
    const selected = selectedMaterial(proper, request, structure, cycleMode);
    if (selected.kind === 'cycle-alternatives') {
      selected.alternatives.forEach(function (alternative) {
        alternative.sourceHooks = sourceHooks(
          proper, alternative.material, request.edition.id, mass.key, index
        ).concat([{
          kind: 'proper-cycle',
          id: request.edition.id + '/' + mass.key + '/' + pad(index) + '/' + alternative.cycle
        }]);
      });
    }
    return {
      id: properEventId(request.edition.id, mass.key, index),
      kind: 'proper',
      semanticSlot: semanticSlot(proper),
      editionSlotLabel: proper.name || null,
      form: proper.form || null,
      sourceKind: proper.source || null,
      selected: selected,
      seat: seat || null,
      sourceHooks: sourceHooks(proper, selected, request.edition.id, mass.key, index)
    };
  }

  function ordinaryTranslation(element, ordinary, language, witness) {
    const candidates = (element.translations || []).filter(function (one) {
      return one && one.lang === language && one.text;
    });
    const found = witness ? candidates.find(function (one) {
      return (one.source_id || one.source || null) === witness;
    }) : (candidates.length === 1 ? candidates[0] : null);
    if (found) {
      return {
        kind: 'ordinary-text',
        language: language,
        sourceId: found.source_id || null,
        rights: found.rights || null,
        absenceKey: null,
        availability: 'held',
        text: found.text
      };
    }
    if (!witness && candidates.length > 1) {
      const ids = candidates.map(function (one) {
        return one.source_id || one.source || null;
      });
      if (ids.every(Boolean)) {
        return {
          kind: 'ordinary-text', language: language, sourceId: null, rights: null, absenceKey: null,
          availability: 'choice-required', text: null,
          unresolvedWitnesses: ids.slice().sort()
        };
      }
    }
    const row = (ordinary.languages || []).find(function (one) { return one.lang === language; });
    return {
      kind: 'ordinary-text', language: language,
      sourceId: null,
      rights: null,
      absenceKey: row && element.absent && element.absent[row.absent] || 'language-not-held',
      availability: 'unavailable',
      text: null
    };
  }

  function seatedEvents(mass, request, structure, ordinary, cycleMode) {
    if (!ordinary) {
      return (mass.propers || []).map(function (proper, index) {
        return { proper: proper, index: index };
      }).filter(function (row) {
        return row.proper.name !== 'Placeholder';
      }).map(function (row) {
        return projectProper(row.proper, row.index, mass, request, structure, cycleMode, null);
      });
    }
    const variant = request.options && request.options.legitimate || {};
    const group = Seating.variantGroupOf(ordinary);
    const wanted = group && variant[group.group] || null;
    if (wanted && !(group.options || []).some(function (one) { return one.id === wanted; })) {
      throw new Error('explicit Ordinary option is not held by this edition');
    }
    const shown = Seating.shownElements(ordinary, wanted);
    const placed = Seating.seatPropers(
      mass.propers || [], Seating.seats(ordinary, shown),
      function (proper) { return proper && proper.name === 'Placeholder'; }
    );
    const indexes = properIndex(mass);
    return Seating.massEvents(shown, placed).map(function (event) {
      if (event.kind === 'begin_section') {
        return {
          id: 'ordinary-section/' + event.section.key,
          kind: 'ordinary-section',
          sourceHooks: [{
            kind: 'ordinary-structure', id: request.edition.id + '/' + event.section.key
          }]
        };
      }
      if (event.kind === 'ordinary_element') {
        const selected = ordinaryTranslation(
          event.element, ordinary,
          request.languages && request.languages.ordinary || 'en',
          request.languages && request.languages.ordinaryWitness || null
        );
        return {
          id: 'ordinary-element/' + event.element.key,
          kind: 'ordinary-element',
          speaker: event.element.speaker || null,
          action: event.element.kind === 'rubric',
          locus: event.element.locus || null,
          selected: selected,
          sourceHooks: [{
            kind: 'ordinary-structure',
            id: request.edition.id + '/' + event.element.key
          }].concat(selected.sourceId ? [{ kind: 'translation', id: selected.sourceId }] : [])
        };
      }
      return projectProper(
        event.proper,
        indexes.get(event.proper),
        mass,
        request,
        structure,
        cycleMode,
        event.seat ? {
          id: event.seat.key,
          anchor: event.seat.anchor,
          where: event.seat.where,
          locus: event.seat.locus,
          placement: event.placement
        } : { id: null, placement: event.placement }
      );
    });
  }

  function coverageFor(mass, request, ordinary, events) {
    const rows = [];
    const propers = mass.propers || [];
    const placeholders = propers.filter(function (one) { return one.name === 'Placeholder'; });
    if (placeholders.length) {
      rows.push(Contract.coverage(
        'supported', 'formulary:' + mass.key, 'partial',
        [{ kind: 'text-not-held', count: placeholders.length, repositoryTerm: 'Placeholder' }]
      ));
    } else {
      rows.push(Contract.coverage('supported', 'formulary:' + mass.key, 'complete', []));
    }
    const selections = selectedRows(events);
    const missingTranslations = selections.filter(function (row) {
      return row.selected.missing;
    });
    if (missingTranslations.length) {
      rows.push(Contract.coverage(
        'unavailable', 'proper-translation:' + request.languages.orations, null,
        [{ kind: 'translation-missing', count: missingTranslations.length }]
      ));
    }
    const unresolvedCitations = selections.filter(function (row) {
      return (row.selected.unresolved || []).length;
    });
    if (unresolvedCitations.length) {
      rows.push(Contract.coverage(
        'unavailable', 'proper-scripture-text', null,
        [{ kind: 'unresolved-citation', count: unresolvedCitations.length }]
      ));
    }
    if (request.options && request.options.ordinary) {
      if (!ordinary) {
        rows.push(Contract.coverage(
          'unsupported', 'ordinary:' + request.edition.id, null,
          [{ kind: 'ordinary-missing' }]
        ));
      } else {
        const language = request.languages && request.languages.ordinary || 'en';
        const declared = (ordinary.languages || []).find(function (one) { return one.lang === language; });
        if (!declared || declared.held === 0) {
          rows.push(Contract.coverage(
            'unavailable', 'ordinary:' + request.edition.id + ':' + language, null,
            [{ kind: 'language-missing', absenceKey: declared && declared.absent || 'language-not-held' }]
          ));
        } else {
          const incomplete = declared.held < declared.elements;
          rows.push(Contract.coverage(
            'supported', 'ordinary:' + request.edition.id + ':' + language,
            incomplete ? 'partial' : 'complete',
            incomplete ? [{ kind: 'language-missing', absenceKey: declared.absent }] : []
          ));
        }
      }
    }
    return rows;
  }

  function branchFor(derived, request) {
    const branches = derived.options || [];
    const territory = territoryId(request);
    if (branches.length === 1 && (branches[0].option === null || branches[0].option === territory)) {
      return branches[0];
    }
    if (territory === null) throw new Error('territorial Day branch must be explicit');
    const found = branches.find(function (one) { return one.option === territory; });
    if (!found) throw new Error('requested territorial Day branch is not held');
    return found;
  }

  function hasOwn(value, key) {
    return Object.prototype.hasOwnProperty.call(value || {}, key);
  }

  function territoryId(request) {
    const territory = request.calendar && hasOwn(request.calendar, 'territory')
      ? request.calendar.territory : null;
    return territory && territory.id || null;
  }

  function readableFor(branch, request) {
    const rows = branch.readable || [];
    if (request.selectedReadableFormulary) {
      const exact = rows.find(function (one) {
        return one.key === request.selectedReadableFormulary.id;
      });
      if (!exact) throw new Error('requested readable formulary is not held on this Day branch');
      return exact;
    }
    const said = rows.filter(function (one) { return one.state === 'said'; });
    if (said.length === 1) return said[0];
    if (said.length > 1 || branch.choice) return null;
    return null;
  }

  function branchChoices(branch) {
    const out = [];
    if (branch.choice && (branch.choice.among || []).length > 1) {
      out.push(Contract.unresolvedChoice(
        'calendar-precedence',
        branch.choice.what || 'the calendar source leaves the celebrations coequal',
        branch.choice.among.map(function (one) { return { id: one.id, identity: { id: one.id } }; }),
        branch.choice.locus ? [{ kind: 'locus', id: branch.choice.locus }] : []
      ));
    }
    for (const choice of branch.massChoices || []) {
      if ((choice.among || []).length < 2) continue;
      if (choice.preferred) {
        const held = choice.among.some(function (one) {
          return one.id === choice.preferred || one.key === choice.preferred;
        });
        if (!held) throw new Error('source-preferred formulary is not among the authorized options');
        continue;
      }
      out.push(Contract.unresolvedChoice(
        choice.id || 'authorized-formulary-choice',
        choice.openBecause || choice.what || 'the source authorizes coequal options',
        choice.among.map(function (one) { return {
          id: one.key || one.id,
          identity: { id: one.key || one.id }
        }; }),
        choice.locus ? [{ kind: 'locus', id: choice.locus }] : []
      ));
    }
    return out;
  }

  function translationChoices(events) {
    return selectedRows(events).filter(function (row) {
      return row.selected.availability === 'choice-required' &&
        (row.selected.unresolvedWitnesses || []).length > 1;
    }).map(function (row) {
      const event = row.event;
      return Contract.unresolvedChoice(
        'translation-witness:' + event.id + (row.cycle ? ':' + row.cycle : ''),
        'more than one held witness supplies the requested translation language',
        row.selected.unresolvedWitnesses.map(function (id) {
          return {
            id: id,
            identity: { id: id },
            sourceHooks: [{ kind: 'translation', id: id }]
          };
        }),
        row.sourceHooks
      );
    });
  }

  function selectedRows(events) {
    const rows = [];
    (events || []).forEach(function (event) {
      if (event.kind !== 'proper' || !event.selected) return;
      if (event.selected.kind !== 'cycle-alternatives') {
        rows.push({
          event: event, selected: event.selected, cycle: null,
          sourceHooks: event.sourceHooks || []
        });
        return;
      }
      event.selected.alternatives.forEach(function (alternative) {
        rows.push({
          event: event, selected: alternative.material, cycle: alternative.cycle,
          sourceHooks: alternative.sourceHooks || []
        });
      });
    });
    return rows;
  }

  function explicitAbsencesFor(branch, lectionary) {
    return (branch.absent || []).map(function (one) {
      return {
        kind: 'explicit-semantic-absence', scope: 'calendar-result',
        repositoryTerm: 'absent', value: one
      };
    }).concat(lectionary ? [] : [{
      kind: 'explicit-semantic-absence',
      scope: 'lectionary-cycle',
      repositoryTerm: 'semantic-absence',
      reason: 'not-applicable-to-edition'
    }]);
  }

  function adaptDay(input) {
    const request = input.request;
    const checked = Contract.validateReaderState(request);
    if (!checked.ok || request.entrance !== 'day') throw new Error('invalid Day reader state');
    const derived = input.derived;
    if (!derived || derived.date !== request.civilDate || derived.calendar !== request.calendar.id) {
      throw new Error('Day adapter requires the matching existing MassAssembly result');
    }
    const branch = branchFor(derived, request);
    const choices = branchChoices(branch);
    const readable = readableFor(branch, request);
    if (!readable && choices.length) {
      return {
        entrance: 'day',
        request: request,
        calendarResult: {
          calendar: derived.calendar, date: derived.date, territory: branch.option,
          winner: branch.winner && branch.winner.id || null, settled: branch.settled
        },
        resolved: null,
        events: [],
        coverage: [Contract.coverage(
          'absent', 'resolved-formulary', null,
          [{ kind: 'semantic-absence', repositoryTerm: 'unresolved' }]
        )],
        unresolvedChoices: choices
      };
    }
    if (!readable) throw new Error('Day branch has no deterministic or explicitly selected formulary');
    const mass = (input.structure.masses || []).find(function (one) { return one.key === readable.key; });
    if (!mass) throw new Error('resolved Day formulary is absent from the selected edition structure');
    const lectionary = derived.liturgicalYear && derived.liturgicalYear.lectionary || null;
    const adaptedRequest = Object.assign({}, request, { lectionary: lectionary });
    const ordinary = request.options && request.options.ordinary ? (input.ordinary || null) : null;
    const events = seatedEvents(mass, adaptedRequest, input.structure, ordinary, 'day');
    return {
      entrance: 'day',
      request: request,
      calendarResult: {
        calendar: derived.calendar,
        date: derived.date,
        territory: branch.option,
        winner: branch.winner && branch.winner.id || null,
        selectedBranch: branch.option,
        settled: branch.settled,
        season: derived.season || null,
        week: derived.week || null,
        lectionary: lectionary
      },
      resolved: { edition: request.edition.id, formulary: mass.key, standing: readable.state },
      events: events,
      coverage: coverageFor(mass, request, ordinary, events),
      explicitAbsences: explicitAbsencesFor(branch, lectionary),
      unresolvedChoices: choices.concat(translationChoices(events))
    };
  }

  function adaptPropers(input) {
    const request = input.request;
    const checked = Contract.validateReaderState(request);
    if (!checked.ok || request.entrance !== 'propers') throw new Error('invalid Propers reader state');
    if (input.structure.calendar !== request.edition.id) {
      throw new Error('Propers structure does not match requested edition');
    }
    const mass = (input.structure.masses || []).find(function (one) {
      return one.key === request.formulary.id;
    });
    if (!mass) throw new Error('requested Propers formulary is not held');
    if (request.formulary.type && request.formulary.type !== (mass.kind || null)) {
      throw new Error('requested Propers formulary type does not match the held object');
    }
    if (hasOwn(request, 'alternative')) {
      throw new Error('explicit Propers alternative has no held stable generated identity');
    }
    const heldCycles = new Set();
    (mass.propers || []).forEach(function (proper) {
      cycleKeys(proper).forEach(function (cycle) { heldCycles.add(cycle); });
    });
    if (hasOwn(request, 'cycle') && request.cycle !== null && !heldCycles.has(request.cycle)) {
      throw new Error('explicit cycle is not held by this Propers formulary');
    }
    const events = seatedEvents(mass, request, input.structure, null, 'propers');
    return {
      entrance: 'propers',
      request: request,
      calendarResult: null,
      resolved: { edition: request.edition.id, formulary: mass.key, type: mass.kind || null },
      events: events,
      coverage: coverageFor(mass, request, null, events),
      explicitAbsences: [{
        kind: 'explicit-semantic-absence',
        scope: 'civil-date-and-calendar-result',
        repositoryTerm: 'semantic-absence',
        reason: 'propers-entrance-is-date-independent'
      }],
      unresolvedChoices: (request.unresolvedChoices || []).concat(translationChoices(events))
    };
  }

  function sameJson(left, right) {
    return JSON.stringify(left) === JSON.stringify(right);
  }

  function cliMaterial(proper, request, generatedProper) {
    const cycle = generatedProper ? dayCycle(generatedProper, request.lectionary) : null;
    const references = (proper.verses || []).map(function (one) { return one.ref; }).filter(Boolean);
    if (references.length) {
      const generated = selectedMaterial(generatedProper, request, { numbering: null }, 'day');
      if (generated.kind !== 'scripture' || !sameJson(references, generated.references)) {
        throw new Error('mass-today scripture references disagree with generated structure');
      }
      const unresolved = (proper.verses || []).filter(function (one) {
        return !one.text;
      }).map(function (one) {
        return { reference: one.ref, reason: one.note || 'text-not-held' };
      });
      return {
        kind: 'scripture', bible: request.bible && request.bible.id || null,
        numbering: request.bible && request.bible.numbering || null,
        cycle: cycle, cycles: cycle ? [cycle] : [],
        availability: unresolved.length ? 'unavailable' : 'held', rights: null,
        references: references,
        unresolved: unresolved
      };
    }
    if (proper.text) {
      const language = request.languages && request.languages.orations || 'la';
      if (language !== 'la') {
        throw new Error('mass-today payload does not expose a selected non-Latin oration witness');
      }
      const generatedText = cycle && generatedProper.cycles && generatedProper.cycles[cycle] &&
        generatedProper.cycles[cycle].text || generatedProper.text;
      if (proper.text !== generatedText) {
        throw new Error('mass-today composed text disagrees with generated structure');
      }
      return {
        kind: 'composed', language: 'la', cycle: cycle, cycles: cycle ? [cycle] : [],
        sourceId: null, rights: null, missing: false, availability: 'held', text: proper.text
      };
    }
    return { kind: 'absent', rights: null, availability: 'absent', reason: 'semantic-absence' };
  }

  function adaptCli(input) {
    const request = input.request;
    const checked = Contract.validateReaderState(request);
    if (!checked.ok || request.entrance !== 'day') throw new Error('invalid Day reader state');
    if (!input.derived || input.derived.date !== request.civilDate ||
        input.derived.calendar !== request.calendar.id) {
      throw new Error('CLI adapter requires the matching existing MassAssembly result');
    }
    const branch = branchFor(input.derived, request);
    const payload = input.payload;
    if (payload.date !== request.civilDate) {
      throw new Error('mass-today payload date does not match the requested Day state');
    }
    const day = (payload.days || []).find(function (one) {
      return one.calendar === request.calendar.id;
    });
    if (!day) throw new Error('mass-today payload does not carry the requested calendar');
    if (!payload.scripture || payload.scripture.id !== (request.bible && request.bible.id)) {
      throw new Error('mass-today payload Bible does not match the requested Day state');
    }
    const territory = territoryId(request);
    if (territory !== null) {
      throw new Error('mass-today parity cannot represent a territorial branch');
    }
    const wanted = request.selectedReadableFormulary && request.selectedReadableFormulary.id;
    const candidates = (day.masses || []).filter(function (one) {
      return wanted ? one.key === wanted : one.standing === 'said';
    });
    if (candidates.length !== 1) throw new Error('mass-today payload has no unique requested formulary');
    const mass = candidates[0];
    if (!mass.bible || mass.bible.id !== request.bible.id) {
      throw new Error('mass-today formulary Bible does not match the request');
    }
    const generatedMass = input.structure && (input.structure.masses || []).find(function (one) {
      return one.key === mass.key;
    });
    if (!generatedMass) throw new Error('mass-today parity requires the matching generated formulary');
    const generatedRows = (generatedMass.propers || []).map(function (proper, index) {
      return { proper: proper, sourceIndex: index };
    }).filter(function (row) { return row.proper.name !== 'Placeholder'; });
    if (generatedRows.length !== (mass.propers || []).length) {
      throw new Error('mass-today held Proper count disagrees with generated structure');
    }
    const lectionary = input.derived && input.derived.liturgicalYear &&
      input.derived.liturgicalYear.lectionary || null;
    const payloadLectionary = day.why && hasOwn(day.why, 'lectionary')
      ? day.why.lectionary : null;
    if (!sameJson(payloadLectionary, lectionary)) {
      throw new Error('mass-today lectionary result disagrees with calendar assembly');
    }
    const adaptedRequest = Object.assign({}, request, { lectionary: lectionary });
    function cliProper(proper, cliIndex, seat) {
      const generatedRow = generatedRows[cliIndex] || {};
      const generatedProper = generatedRow.proper || null;
      const sourceIndex = generatedRow.sourceIndex;
      if (!generatedProper || generatedProper.name !== proper.name ||
          (generatedProper.form || null) !== (proper.form || null) ||
          (generatedProper.source || null) !== (proper.source || null) ||
          !sameJson(generatedProper.taken_from || null, proper.taken_from || null)) {
        throw new Error('mass-today Proper order disagrees with generated structure');
      }
      const selected = cliMaterial(proper, adaptedRequest, generatedProper);
      return {
        id: properEventId(request.edition.id, mass.key, sourceIndex),
        kind: 'proper',
        semanticSlot: semanticSlot(generatedProper),
        editionSlotLabel: proper.name || null,
        form: proper.form || null,
        sourceKind: proper.source || null,
        selected: selected,
        seat: seat || null,
        sourceHooks: sourceHooks(
          proper, selected, request.edition.id, mass.key, sourceIndex
        )
      };
    }
    let events;
    if (request.options && request.options.ordinary && day.ordinary && !day.ordinary.refused) {
      const ordinary = day.ordinary;
      const group = Seating.variantGroupOf(ordinary);
      const variants = request.options.legitimate || {};
      const wantedVariant = group && variants[group.group] || null;
      const shown = Seating.shownElements(ordinary, wantedVariant);
      const placed = Seating.seatPropers(mass.propers || [], Seating.seats(ordinary, shown));
      const indexes = properIndex(mass);
      events = Seating.massEvents(shown, placed).map(function (event) {
        if (event.kind === 'begin_section') {
          return {
            id: 'ordinary-section/' + event.section.key,
            kind: 'ordinary-section',
            sourceHooks: [{
              kind: 'ordinary-structure', id: request.edition.id + '/' + event.section.key
            }]
          };
        }
        if (event.kind === 'ordinary_element') {
          const selected = ordinaryTranslation(
            event.element, ordinary, request.languages && request.languages.ordinary || 'en',
            request.languages && request.languages.ordinaryWitness || null
          );
          return {
            id: 'ordinary-element/' + event.element.key,
            kind: 'ordinary-element',
            speaker: event.element.speaker || null,
            action: event.element.kind === 'rubric',
            locus: event.element.locus || null,
            selected: selected,
            sourceHooks: [{
              kind: 'ordinary-structure',
              id: request.edition.id + '/' + event.element.key
            }].concat(selected.sourceId ? [{ kind: 'translation', id: selected.sourceId }] : [])
          };
        }
        return cliProper(event.proper, indexes.get(event.proper), event.seat ? {
          id: event.seat.key,
          anchor: event.seat.anchor,
          where: event.seat.where,
          locus: event.seat.locus,
          placement: event.placement
        } : { id: null, placement: event.placement });
      });
    } else {
      events = (mass.propers || []).map(function (proper, index) {
        return cliProper(proper, index, null);
      });
    }
    return {
      entrance: 'day',
      request: request,
      calendarResult: {
        calendar: day.calendar, date: payload.date, territory: branch.option,
        winner: branch.winner && branch.winner.id || null,
        selectedBranch: branch.option, settled: day.settled, season: day.season || null,
        week: day.week || null,
        lectionary: lectionary
      },
      resolved: { edition: request.edition.id, formulary: mass.key, standing: mass.standing },
      events: events,
      coverage: coverageFor(
        generatedMass, request,
        request.options && request.options.ordinary && day.ordinary && !day.ordinary.refused
          ? day.ordinary : null,
        events
      ),
      explicitAbsences: explicitAbsencesFor(branch, lectionary),
      unresolvedChoices: branchChoices(branch).concat(translationChoices(events))
    };
  }

  function validationContext(input) {
    const context = { missals: {}, bibles: {} };
    for (const bible of (input.bibles && input.bibles.bibles) || []) {
      context.bibles[bible.id] = { numbering: bible.numbering || null };
    }
    const dayCalendars = new Set(
      ((input.rubricsIndex && input.rubricsIndex.calendars) || []).map(function (one) {
        return one.calendar;
      })
    );
    const properEntries = ((input.properIndex && input.properIndex.missals) || []).filter(
      function (entry) {
        return input.entrance !== 'day' || dayCalendars.has(entry.id);
      }
    );
    for (const entry of properEntries) {
      const structure = input.structures && input.structures[entry.id];
      if (!structure) continue;
      const types = {};
      for (const mass of structure.masses || []) {
        const type = mass.kind || 'other';
        if (!types[type]) types[type] = [];
        types[type].push(mass.key);
      }
      const languages = ['la'];
      for (const translation of structure.translations || []) {
        if (translation.lang && languages.indexOf(translation.lang) < 0) languages.push(translation.lang);
      }
      context.missals[entry.id] = {
        calendar: structure.calendar || entry.id,
        types: types,
        orationLanguages: languages,
        ordinaryLanguages: [],
        variantGroups: {}
      };
    }
    for (const row of (input.ordinaryIndex && input.ordinaryIndex.calendars) || []) {
      if (!context.missals[row.calendar]) continue;
      const ordinary = input.ordinaries && input.ordinaries[row.calendar];
      if (!ordinary) continue;
      context.missals[row.calendar].ordinaryLanguages = (ordinary.languages || []).map(function (one) {
        return one.lang;
      });
      for (const group of ordinary.variants || []) {
        context.missals[row.calendar].variantGroups[group.group] = (group.options || []).map(function (one) {
          return one.id;
        });
      }
    }
    if (input.derived) {
      const branches = input.derived.options || [];
      const branch = input.territory === undefined
        ? (branches.length === 1 ? branches[0] : null)
        : branches.find(function (one) { return one.option === input.territory; });
      context.dayReadableFormularies = branch
        ? (branch.readable || []).map(function (one) { return { id: one.key, state: one.state }; })
        : [];
    }
    return context;
  }

  return Object.freeze({
    properEventId: properEventId,
    validationContext: validationContext,
    adaptDay: adaptDay,
    adaptPropers: adaptPropers,
    adaptCli: adaptCli
  });
}));
