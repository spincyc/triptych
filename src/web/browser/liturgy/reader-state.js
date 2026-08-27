/* ===========================================================================
 * Shared semantic state for the liturgy readers
 * ===========================================================================
 *
 * This module is a contract, not a page. It has no DOM, storage, network,
 * calendar, or rendering dependency. Day and Propers adapters give it already
 * resolved repository data; it validates identity, coverage, choices, Compare
 * anchors, and legacy URL state without deriving a second liturgical answer.
 *
 * Both production readers load this contract. Their controllers remain
 * responsible for rendering and navigation, while this module supplies the
 * shared fail-closed state and canonical URL vocabulary they enforce.
 * ======================================================================== */

'use strict';

(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  else root.LiturgyReaderState = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  const STATE_SCHEMA = 'triptych-liturgy-reader-state/v1';
  const FIXTURE_SCHEMA = 'triptych-liturgy-reader-fixture/v1';
  const URL_SCHEMA = 'triptych-liturgy-url-state/v1';
  const ENTRANCES = Object.freeze(['day', 'propers']);
  const MODES = Object.freeze(['read', 'missal', 'study', 'compare']);
  const DEFAULT_BIBLE_ID = 'douay-rheims';
  const STATE_FIELDS = Object.freeze([
    'schema', 'entrance', 'civilDate', 'edition', 'calendar', 'formulary', 'browse',
    'bible', 'languages', 'selectedReadableFormulary', 'requestedMode', 'options',
    'apparatus', 'form', 'cycle', 'alternative', 'semanticLocation', 'sourceHooks',
    'coverage', 'unresolvedChoices', 'explicitAbsences', 'comparison'
  ]);

  const COVERAGE_STATES = Object.freeze(['supported', 'unsupported', 'unavailable', 'absent']);
  const COVERAGE_COMPLETENESS = Object.freeze(['complete', 'partial']);
  const COVERAGE_REASONS = Object.freeze([
    'partial-recension',
    'unsupported-date',
    'unsupported-object',
    'text-not-held',
    'text-withheld',
    'ordinary-missing',
    'translation-missing',
    'language-missing',
    'unresolved-citation',
    'semantic-absence'
  ]);
  const COVERAGE_REASON_STATES = Object.freeze({
    supported: Object.freeze([
      'partial-recension', 'text-not-held', 'text-withheld', 'translation-missing',
      'language-missing', 'unresolved-citation'
    ]),
    unsupported: Object.freeze(['unsupported-date', 'unsupported-object', 'ordinary-missing']),
    unavailable: Object.freeze([
      'text-not-held', 'text-withheld', 'translation-missing',
      'language-missing', 'unresolved-citation'
    ]),
    absent: Object.freeze(['semantic-absence'])
  });

  const DAY_KEYS = Object.freeze([
    'date', 'missal', 'bible', 'orations', 'why', 'ordinary',
    'ordinary-lang', 'rubrics', 'mass', 'form', 'translation-witness', 'mode', 'location'
  ]);
  const PROPERS_KEYS = Object.freeze([
    'missal', 'type', 'mass', 'bible', 'orations',
    'form', 'cycle', 'alternative', 'translation-witness', 'mode', 'location'
  ]);
  const URL_INVENTORY = Object.freeze({
    day: Object.freeze({
      hash: Object.freeze(DAY_KEYS.concat(['eucharistic-prayer'])),
      dynamicHash: Object.freeze(['eucharistic-prayer']),
      query: Object.freeze(['data'])
    }),
    propers: Object.freeze({
      hash: PROPERS_KEYS,
      query: Object.freeze(['data', 'missals'])
    })
  });
  const CANONICAL_ROUTES = Object.freeze({
    day: Object.freeze({ canonical: 'day.html', legacy: Object.freeze(['day-reader.html']) }),
    propers: Object.freeze({ canonical: 'index.html', legacy: Object.freeze(['propers-reader.html']) })
  });

  function has(object, key) {
    return Object.prototype.hasOwnProperty.call(object || {}, key);
  }

  function object(value) {
    return value && typeof value === 'object' && !Array.isArray(value);
  }

  function nonempty(value) {
    return typeof value === 'string' && value.length > 0;
  }

  function strictDate(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value || '')) return false;
    const stamp = Date.parse(value + 'T00:00:00Z');
    return !Number.isNaN(stamp) && new Date(stamp).toISOString().slice(0, 10) === value;
  }

  /** Replace only a known retained reader basename; preserve its directory. */
  function canonicalRoute(entrance, pathname) {
    if (ENTRANCES.indexOf(entrance) < 0) throw new Error('entrance must be day or propers');
    const route = CANONICAL_ROUTES[entrance];
    const path = String(pathname || '');
    const slash = path.lastIndexOf('/');
    const directory = slash >= 0 ? path.slice(0, slash + 1) : '';
    const basename = slash >= 0 ? path.slice(slash + 1) : path;
    if (basename === route.canonical || route.legacy.indexOf(basename) >= 0) {
      return directory + route.canonical;
    }
    return path;
  }

  function issue(code, path, message, source) {
    return { code: code, path: path, message: message, source: source || null };
  }

  function assertIdentity(errors, value, path) {
    if (!object(value) || !nonempty(value.id)) {
      errors.push(issue('required-identity', path, path + ' must carry a stable id'));
    }
    if (object(value) && (has(value, 'label') || has(value, 'name'))) {
      errors.push(issue(
        'display-label-is-not-identity', path,
        path + ' may not encode a translated display label as identity'
      ));
    }
  }

  function validateSourceHook(value, path) {
    if (!object(value) || !nonempty(value.kind) || !nonempty(value.id)) {
      return [issue(
        'source-hook', path,
        'source and provenance hooks need stable kind and id fields'
      )];
    }
    return [];
  }

  function validateSourceHooks(value, path, required) {
    if (!Array.isArray(value)) {
      return required || value !== undefined
        ? [issue('source-hooks-array', path, 'source hooks must be an array')]
        : [];
    }
    const errors = [];
    value.forEach(function (hook, index) {
      errors.push.apply(errors, validateSourceHook(hook, path + '[' + index + ']'));
    });
    return errors;
  }

  function validateExplicitAbsence(value, path) {
    const at = path || 'explicitAbsence';
    const errors = [];
    if (!object(value) || value.kind !== 'explicit-semantic-absence') {
      return [issue(
        'explicit-absence-kind', at,
        'an explicit absence must use the explicit-semantic-absence discriminant'
      )];
    }
    if (!nonempty(value.scope)) {
      errors.push(issue('explicit-absence-scope', at + '.scope', 'explicit absence needs a scope'));
    }
    if (!nonempty(value.repositoryTerm)) {
      errors.push(issue(
        'explicit-absence-term', at + '.repositoryTerm',
        'explicit absence must retain the repository-owned absence term'
      ));
    }
    if (!nonempty(value.reason) && !nonempty(value.value)) {
      errors.push(issue(
        'explicit-absence-reason', at,
        'explicit absence must retain a stable reason or source value'
      ));
    }
    return errors;
  }

  function validateSemanticSlot(value, path) {
    const at = path || 'semanticSlot';
    if (!object(value) || (value.state !== 'mapped' && value.state !== 'edition-local-unmapped')) {
      return [issue(
        'semantic-slot-state', at,
        'semantic slot must be mapped or explicitly edition-local and unmapped'
      )];
    }
    const errors = [];
    if (value.state === 'mapped') {
      assertIdentity(errors, value.identity, at + '.identity');
    } else if (!nonempty(value.reason)) {
      errors.push(issue(
        'semantic-slot-unmapped-reason', at + '.reason',
        'an unmapped edition-local slot must state why it has no cross-edition identity'
      ));
    }
    if (has(value, 'label') || has(value, 'name')) {
      errors.push(issue(
        'semantic-slot-label', at,
        'translated or display labels may not be semantic slot identity'
      ));
    }
    return errors;
  }

  function validateSelectedMaterial(value, path) {
    const at = path || 'selected';
    const errors = [];
    if (!object(value) || !nonempty(value.kind)) {
      return [issue('selected-material', at, 'selected material needs a typed kind')];
    }
    if (['held', 'unavailable', 'absent', 'choice-required'].indexOf(value.availability) < 0) {
      errors.push(issue(
        'selected-availability', at + '.availability',
        'selected material needs typed availability'
      ));
    }
    if (!has(value, 'rights')) {
      errors.push(issue(
        'selected-rights', at + '.rights',
        'selected material must assert rights identity or explicit null'
      ));
    } else if (value.rights !== null && !nonempty(value.rights)) {
      errors.push(issue('selected-rights-id', at + '.rights', 'rights identity must be stable'));
    }
    if (value.kind === 'cycle-alternatives') {
      if (value.availability !== 'choice-required' || value.cycle !== null) {
        errors.push(issue(
          'selected-cycle-choice', at,
          'cycle alternatives must remain an unselected choice-required result'
        ));
      }
      if (has(value, 'selected') || has(value, 'default')) {
        errors.push(issue(
          'selected-cycle-order-default', at,
          'cycle alternatives may not carry an incidental selection or default'
        ));
      }
      if (!Array.isArray(value.alternatives) || value.alternatives.length < 2) {
        errors.push(issue(
          'selected-cycle-alternatives', at + '.alternatives',
          'multiple held cycles require at least two structured alternatives'
        ));
      } else {
        const ids = [];
        value.alternatives.forEach(function (alternative, index) {
          const alternativePath = at + '.alternatives[' + index + ']';
          if (!object(alternative) || !nonempty(alternative.id) ||
              !nonempty(alternative.cycle) || alternative.id !== alternative.cycle) {
            errors.push(issue(
              'selected-cycle-alternative-id', alternativePath,
              'each cycle alternative needs one matching stable id and cycle code'
            ));
          } else ids.push(alternative.id);
          if (object(alternative) &&
              (has(alternative, 'selected') || has(alternative, 'default'))) {
            errors.push(issue(
              'selected-cycle-alternative-default', alternativePath,
              'a cycle alternative may not carry an incidental selection or default'
            ));
          }
          if (!object(alternative) || !object(alternative.material) ||
              alternative.material.kind === 'cycle-alternatives') {
            errors.push(issue(
              'selected-cycle-alternative-material', alternativePath + '.material',
              'each cycle alternative must retain one concrete selected material result'
            ));
          } else {
            errors.push.apply(
              errors,
              validateSelectedMaterial(alternative.material, alternativePath + '.material')
            );
            if (alternative.material.cycle !== alternative.cycle) {
              errors.push(issue(
                'selected-cycle-alternative-cycle', alternativePath + '.material.cycle',
                'the concrete material must retain its alternative cycle code'
              ));
            }
          }
          if (object(alternative)) {
            errors.push.apply(errors, validateSourceHooks(
              alternative.sourceHooks, alternativePath + '.sourceHooks', true
            ));
          }
        });
        if (new Set(ids).size !== ids.length) {
          errors.push(issue(
            'selected-cycle-alternative-duplicate', at + '.alternatives',
            'cycle alternative ids must be unique'
          ));
        }
      }
    } else if (value.kind === 'scripture') {
      if (!nonempty(value.bible)) {
        errors.push(issue('selected-bible', at + '.bible', 'scripture selection needs a Bible id'));
      }
      if (!Array.isArray(value.references) || !value.references.length ||
          value.references.some(function (one) { return !nonempty(one); })) {
        errors.push(issue(
          'selected-references', at + '.references',
          'scripture selection needs stable references'
        ));
      }
    } else if (value.kind === 'composed') {
      if (!nonempty(value.language) || typeof value.missing !== 'boolean') {
        errors.push(issue(
          'selected-composed', at,
          'composed selection needs a language and explicit missing flag'
        ));
      }
      if (value.availability === 'choice-required' &&
          (!Array.isArray(value.unresolvedWitnesses) || value.unresolvedWitnesses.length < 2)) {
        errors.push(issue(
          'selected-witness-choice', at + '.unresolvedWitnesses',
          'choice-required translation needs at least two stable witnesses'
        ));
      }
    } else if (value.kind === 'incipit-only') {
      if (!nonempty(value.language)) {
        errors.push(issue('selected-incipit-language', at + '.language', 'incipit needs a language'));
      }
    } else if (value.kind === 'absent') {
      if (!nonempty(value.reason) || value.availability !== 'absent') {
        errors.push(issue('selected-absence', at, 'absent material needs an absence reason'));
      }
    } else if (value.kind === 'ordinary-text') {
      if (!nonempty(value.language)) {
        errors.push(issue('selected-ordinary-language', at + '.language', 'Ordinary text needs a language'));
      }
      if (value.availability === 'choice-required' &&
          (!Array.isArray(value.unresolvedWitnesses) || value.unresolvedWitnesses.length < 2)) {
        errors.push(issue(
          'selected-ordinary-witness-choice', at + '.unresolvedWitnesses',
          'choice-required Ordinary text needs at least two stable witnesses'
        ));
      }
    } else {
      errors.push(issue('selected-kind', at + '.kind', 'unknown selected material kind'));
    }
    return errors;
  }

  function validateCoverage(value, path) {
    const errors = [];
    const at = path || 'coverage';
    if (!object(value)) return [issue('coverage-object', at, at + ' must be an object')];
    if (COVERAGE_STATES.indexOf(value.state) < 0) {
      errors.push(issue('coverage-state', at + '.state', 'unknown coverage state'));
    }
    if (!nonempty(value.scope)) {
      errors.push(issue('coverage-scope', at + '.scope', 'coverage must name its scope'));
    }
    if (value.state === 'supported') {
      if (COVERAGE_COMPLETENESS.indexOf(value.completeness) < 0) {
        errors.push(issue(
          'coverage-completeness', at + '.completeness',
          'supported coverage must be complete or partial'
        ));
      }
    } else if (has(value, 'completeness')) {
      errors.push(issue(
        'coverage-completeness-state', at + '.completeness',
        'only supported coverage has a completeness measure'
      ));
    }
    if (!Array.isArray(value.reasons)) {
      errors.push(issue('coverage-reasons', at + '.reasons', 'coverage reasons must be an array'));
    } else {
      value.reasons.forEach(function (reason, index) {
        if (!object(reason) || COVERAGE_REASONS.indexOf(reason.kind) < 0) {
          errors.push(issue(
            'coverage-reason', at + '.reasons[' + index + ']',
            'coverage reason must use the closed repository-facing vocabulary'
          ));
        }
      });
      if ((value.state !== 'supported' || value.completeness === 'partial') &&
          value.reasons.length === 0) {
        errors.push(issue(
          'coverage-reason-required', at + '.reasons',
          'partial, unsupported, unavailable, and absent coverage must state why'
        ));
      }
      const reasonKinds = value.reasons.map(function (one) { return one && one.kind; });
      if (value.state === 'supported' && value.completeness === 'complete' && reasonKinds.length) {
        errors.push(issue(
          'coverage-complete-reasons', at + '.reasons',
          'complete supported coverage may not carry an incompleteness reason'
        ));
      }
      const allowed = COVERAGE_REASON_STATES[value.state] || [];
      if (reasonKinds.some(function (kind) { return allowed.indexOf(kind) < 0; })) {
        errors.push(issue(
          'coverage-reason-state', at + '.reasons',
          'coverage reasons must agree with the coverage state'
        ));
      }
    }
    return errors;
  }

  function coverage(state, scope, completeness, reasons, details) {
    const value = Object.assign({
      state: state,
      scope: scope,
      reasons: reasons || []
    }, details || {});
    if (completeness) value.completeness = completeness;
    const errors = validateCoverage(value);
    if (errors.length) throw new Error(errors.map((one) => one.message).join('; '));
    return value;
  }

  function validateUnresolvedChoice(value, path) {
    const errors = [];
    const at = path || 'unresolvedChoice';
    if (!object(value) || value.kind !== 'unresolved-authorized-choice') {
      return [issue('choice-kind', at, 'choice must be an unresolved authorized choice')];
    }
    if (!nonempty(value.id)) errors.push(issue('choice-id', at + '.id', 'choice needs an id'));
    if (!nonempty(value.reason)) {
      errors.push(issue('choice-reason', at + '.reason', 'open choice must state why it is open'));
    }
    if (!Array.isArray(value.options) || value.options.length < 2) {
      errors.push(issue('choice-options', at + '.options', 'open choice needs at least two options'));
    } else {
      const ids = [];
      value.options.forEach(function (option, index) {
        const optionPath = at + '.options[' + index + ']';
        if (!object(option) || !nonempty(option.id)) {
          errors.push(issue('choice-option-id', optionPath, 'choice option needs a stable id'));
        } else ids.push(option.id);
        if (object(option)) {
          assertIdentity(errors, option.identity, optionPath + '.identity');
          errors.push.apply(errors, validateSourceHooks(
            option.sourceHooks, optionPath + '.sourceHooks', true
          ));
        }
        if (object(option) && (has(option, 'default') || has(option, 'selected'))) {
          errors.push(issue(
            'choice-order-default', optionPath,
            'a coequal unresolved option may not carry an incidental default or selection'
          ));
        }
      });
      if (new Set(ids).size !== ids.length) {
        errors.push(issue('choice-option-duplicate', at + '.options', 'choice option ids must be unique'));
      }
    }
    if (has(value, 'selected') || has(value, 'default')) {
      errors.push(issue(
        'choice-selected', at,
        'an unresolved choice may not be selected by array, manifest, DOM, or source order'
      ));
    }
    errors.push.apply(errors, validateSourceHooks(value.sourceHooks, at + '.sourceHooks', true));
    return errors;
  }

  function unresolvedChoice(id, reason, options, hooks) {
    const value = {
      kind: 'unresolved-authorized-choice',
      id: id,
      reason: reason,
      options: (options || []).map(function (one) {
        return Object.assign({}, one, {
          identity: one.identity || null,
          sourceHooks: one.sourceHooks || []
        });
      }),
      sourceHooks: hooks || []
    };
    const errors = validateUnresolvedChoice(value);
    if (errors.length) throw new Error(errors.map((one) => one.message).join('; '));
    return value;
  }

  /* Resolve only an explicit answer or a source-declared deterministic one.
   * There is deliberately no options[0] path in this function. */
  function resolveAuthorizedChoice(value, requestedId, deterministicId) {
    const errors = validateUnresolvedChoice(value);
    if (errors.length) return { ok: false, errors: errors };
    const requestedWasSupplied = arguments.length >= 2 && requestedId !== undefined && requestedId !== null;
    const deterministicWasSupplied = arguments.length >= 3 &&
      deterministicId !== undefined && deterministicId !== null;
    const wanted = requestedWasSupplied ? requestedId : (deterministicWasSupplied ? deterministicId : null);
    if (!requestedWasSupplied && !deterministicWasSupplied) {
      return { ok: true, unresolved: value, selected: null };
    }
    const found = value.options.find(function (one) { return one.id === wanted; });
    if (!found) {
      return {
        ok: false,
        errors: [issue('choice-option-invalid', 'choice', 'the requested authorized option is not held')]
      };
    }
    return { ok: true, unresolved: null, selected: found };
  }

  function validateComparison(value, entrance, path) {
    const errors = [];
    const at = path || 'comparison';
    if (!object(value)) return [issue('comparison-object', at, 'comparison must be an object')];
    if (ENTRANCES.indexOf(entrance) < 0) {
      return [issue('comparison-entrance', at, 'comparison entrance must be day or propers')];
    }
    if (!nonempty(value.dimension)) {
      errors.push(issue('comparison-dimension', at + '.dimension', 'comparison needs a dimension'));
    }
    if (!Array.isArray(value.sides) || value.sides.length < 2) {
      errors.push(issue('comparison-sides', at + '.sides', 'comparison needs at least two sides'));
    } else {
      const sideIds = [];
      value.sides.forEach(function (side, index) {
        const sidePath = at + '.sides[' + index + ']';
        if (!object(side) || !nonempty(side.id)) {
          errors.push(issue(
            'comparison-side-id', sidePath + '.id',
            'each comparison side needs a stable id'
          ));
        } else sideIds.push(side.id);
        assertIdentity(errors, side && side.edition, sidePath + '.edition');
        if (entrance === 'day') {
          assertIdentity(errors, side && side.calendar, sidePath + '.calendar');
        } else {
          assertIdentity(errors, side && side.formulary, sidePath + '.formulary');
        }
      });
      if (new Set(sideIds).size !== sideIds.length) {
        errors.push(issue(
          'comparison-side-id-duplicate', at + '.sides',
          'comparison side ids must be unique'
        ));
      }
    }
    const anchor = value.anchor;
    if (!object(anchor)) {
      errors.push(issue('comparison-anchor', at + '.anchor', 'comparison needs an anchor'));
    } else if (entrance === 'day') {
      if (!strictDate(anchor.civilDate)) {
        errors.push(issue('day-compare-date', at + '.anchor.civilDate', 'Day Compare fixes a civil date'));
      }
      if (!nonempty(anchor.territorialContext)) {
        errors.push(issue(
          'day-compare-territory', at + '.anchor.territorialContext',
          'Day Compare fixes an explicitly selected territorial context'
        ));
      }
    } else {
      if (!nonempty(anchor.correspondingFormulary)) {
        errors.push(issue(
          'propers-compare-formulary', at + '.anchor.correspondingFormulary',
          'Propers Compare fixes a corresponding formulary identity'
        ));
      }
      if (has(anchor, 'civilDate')) {
        errors.push(issue(
          'propers-compare-date', at + '.anchor.civilDate',
          'Propers Compare is independent of a civil date'
        ));
      }
    }
    return errors;
  }

  function validateReaderState(value) {
    const errors = [];
    if (!object(value)) return { ok: false, errors: [issue('state-object', '', 'state must be an object')] };
    Object.keys(value).forEach(function (key) {
      if (STATE_FIELDS.indexOf(key) < 0) {
        errors.push(issue(
          'state-field', key,
          'unknown v1 reader-state fields are not an extension mechanism'
        ));
      }
    });
    if (value.schema !== STATE_SCHEMA) {
      errors.push(issue('state-schema', 'schema', 'reader state must use ' + STATE_SCHEMA));
    }
    if (ENTRANCES.indexOf(value.entrance) < 0) {
      errors.push(issue('entrance', 'entrance', 'entrance must be explicit: day or propers'));
      return { ok: false, errors: errors };
    }
    assertIdentity(errors, value.edition, 'edition');
    if (has(value, 'requestedMode') && value.requestedMode !== null &&
        MODES.indexOf(value.requestedMode) < 0) {
      errors.push(issue('mode', 'requestedMode', 'unknown reader mode'));
    }
    if (has(value, 'bible')) assertIdentity(errors, value.bible, 'bible');
    if (object(value.bible) && has(value.bible, 'numbering') &&
        value.bible.numbering !== null && !nonempty(value.bible.numbering)) {
      errors.push(issue(
        'bible-numbering', 'bible.numbering',
        'Bible numbering must be a stable code or explicit null'
      ));
    }
    if (has(value, 'languages') && !object(value.languages)) {
      errors.push(issue('languages-object', 'languages', 'language selections must be an object'));
    } else if (object(value.languages)) {
      const languageKeys = [
        'original', 'translation', 'translationWitness', 'orations',
        'ordinary', 'ordinaryWitness'
      ];
      Object.keys(value.languages).forEach(function (key) {
        if (languageKeys.indexOf(key) < 0) {
          errors.push(issue(
            'language-field', 'languages.' + key,
            'unknown language or witness selection field'
          ));
        }
        if (!nonempty(value.languages[key])) {
          errors.push(issue(
            'language-selection', 'languages.' + key,
            'language and witness selections must be stable nonempty codes'
          ));
        }
      });
    }
    if (has(value, 'options') && !object(value.options)) {
      errors.push(issue('options-object', 'options', 'legitimate options must be an object'));
    } else if (object(value.options)) {
      if (has(value.options, 'ordinary') && typeof value.options.ordinary !== 'boolean') {
        errors.push(issue('ordinary-option', 'options.ordinary', 'Ordinary selection must be boolean'));
      }
      if (has(value.options, 'legitimate') && !object(value.options.legitimate)) {
        errors.push(issue(
          'legitimate-options-object', 'options.legitimate',
          'edition-qualified legitimate options must be keyed data'
        ));
      } else if (object(value.options.legitimate)) {
        Object.keys(value.options.legitimate).forEach(function (key) {
          if (!nonempty(key) || !nonempty(value.options.legitimate[key])) {
            errors.push(issue(
              'legitimate-option-id', 'options.legitimate.' + key,
              'legitimate option groups and selections need stable ids'
            ));
          }
        });
      }
    }
    if (has(value, 'cycle') && value.cycle !== null && !nonempty(value.cycle)) {
      errors.push(issue('cycle-id', 'cycle', 'cycle must be a stable code or explicit null'));
    }
    if (has(value, 'form') && !nonempty(value.form)) {
      errors.push(issue('form-id', 'form', 'form must be a stable nonempty id when supplied'));
    }
    if (has(value, 'alternative') && value.alternative !== null) {
      assertIdentity(errors, value.alternative, 'alternative');
    } else if (has(value, 'alternative')) {
      errors.push(issue(
        'alternative-identity', 'alternative',
        'an explicitly present alternative must carry a stable identity'
      ));
    }
    if (has(value, 'selectedReadableFormulary')) {
      assertIdentity(errors, value.selectedReadableFormulary, 'selectedReadableFormulary');
    }
    if (has(value, 'semanticLocation') &&
        (!object(value.semanticLocation) || !nonempty(value.semanticLocation.eventId))) {
      errors.push(issue(
        'semantic-location', 'semanticLocation',
        'semantic location must name a stable event id'
      ));
    }
    if (has(value, 'apparatus')) {
      if (!object(value.apparatus)) {
        errors.push(issue('apparatus-object', 'apparatus', 'apparatus must be an object'));
      } else {
        Object.keys(value.apparatus).forEach(function (key) {
          if (key !== 'why' && key !== 'rubrics') {
            errors.push(issue(
              'apparatus-field', 'apparatus.' + key,
              'unknown v1 apparatus field'
            ));
          } else if (typeof value.apparatus[key] !== 'boolean') {
            errors.push(issue(
              'apparatus-boolean', 'apparatus.' + key,
              'apparatus disclosure selections must be booleans'
            ));
          }
        });
      }
    }
    if (has(value, 'sourceHooks')) {
      errors.push.apply(errors, validateSourceHooks(value.sourceHooks, 'sourceHooks', true));
    }
    if (value.entrance === 'day') {
      if (!strictDate(value.civilDate)) {
        errors.push(issue('day-date', 'civilDate', 'Day state requires a real civil date'));
      }
      assertIdentity(errors, value.calendar, 'calendar');
      if (object(value.calendar) && has(value.calendar, 'territory') &&
          value.calendar.territory !== null) {
        assertIdentity(errors, value.calendar.territory, 'calendar.territory');
      }
      if (object(value.calendar) && has(value.calendar, 'locality') &&
          value.calendar.locality !== null) {
        assertIdentity(errors, value.calendar.locality, 'calendar.locality');
      }
      if (has(value, 'browse')) {
        errors.push(issue('day-browse', 'browse', 'Day state is date-resolved, not a browse entry'));
      }
      if (has(value, 'formulary')) {
        errors.push(issue(
          'day-formulary', 'formulary',
          'Day may select only a resolved readable formulary, not a Propers formulary identity'
        ));
      }
    } else {
      if (has(value, 'civilDate') && value.civilDate !== null) {
        errors.push(issue('propers-date', 'civilDate', 'Propers state is calendar-independent'));
      }
      if (has(value, 'browse') &&
          (!object(value.browse) || value.browse.kind !== 'browse-entry')) {
        errors.push(issue(
          'propers-browse', 'browse',
          'Propers browse state must be the explicit browse-entry sentinel'
        ));
      }
      if (has(value, 'browse') && has(value, 'formulary')) {
        errors.push(issue(
          'propers-entry-exclusive', 'browse',
          'Propers browse and formulary entries are mutually exclusive'
        ));
      }
      if (has(value, 'calendar')) {
        errors.push(issue(
          'propers-calendar', 'calendar',
          'Propers state is independent of a calendar result'
        ));
      }
      if (has(value, 'selectedReadableFormulary')) {
        errors.push(issue(
          'propers-readable-formulary', 'selectedReadableFormulary',
          'a selected readable Day formulary is not Propers entrance state'
        ));
      }
      if (!has(value, 'browse') && (!object(value.formulary) || !nonempty(value.formulary.id))) {
        errors.push(issue(
          'propers-formulary', 'formulary',
          'Propers requires an edition-qualified formulary or an explicit browse entry'
        ));
      } else if (!has(value, 'browse')) {
        assertIdentity(errors, value.formulary, 'formulary');
        if (has(value.formulary, 'type') && !nonempty(value.formulary.type)) {
          errors.push(issue(
            'formulary-type', 'formulary.type',
            'formulary type must be a stable code when supplied'
          ));
        }
      }
    }
    if (has(value, 'coverage') && !Array.isArray(value.coverage)) {
      errors.push(issue('coverage-array', 'coverage', 'coverage must be an array'));
    } else {
      (value.coverage || []).forEach(function (one, index) {
        errors.push.apply(errors, validateCoverage(one, 'coverage[' + index + ']'));
      });
    }
    if (has(value, 'unresolvedChoices') && !Array.isArray(value.unresolvedChoices)) {
      errors.push(issue(
        'unresolved-choices-array', 'unresolvedChoices',
        'unresolved choices must be an array'
      ));
    } else {
      (value.unresolvedChoices || []).forEach(function (one, index) {
        errors.push.apply(errors, validateUnresolvedChoice(one, 'unresolvedChoices[' + index + ']'));
      });
    }
    if (has(value, 'explicitAbsences') && !Array.isArray(value.explicitAbsences)) {
      errors.push(issue(
        'explicit-absences-array', 'explicitAbsences',
        'explicit absences must be a typed array'
      ));
    } else {
      (value.explicitAbsences || []).forEach(function (one, index) {
        errors.push.apply(
          errors, validateExplicitAbsence(one, 'explicitAbsences[' + index + ']')
        );
      });
    }
    if (has(value, 'comparison') && value.comparison !== null) {
      errors.push.apply(errors, validateComparison(value.comparison, value.entrance));
      if (value.entrance === 'day' && object(value.comparison.anchor) &&
          value.comparison.anchor.civilDate !== value.civilDate) {
        errors.push(issue(
          'day-compare-state-date', 'comparison.anchor.civilDate',
          'Day Compare anchor must equal the reader state civil date'
        ));
      }
    }
    if (value.requestedMode === 'compare' &&
        (!has(value, 'comparison') || value.comparison === null)) {
      errors.push(issue(
        'compare-mode-state', 'comparison',
        'Compare mode requires a valid comparison request'
      ));
    }
    if (has(value, 'comparison') && value.comparison !== null &&
        value.requestedMode !== 'compare') {
      errors.push(issue(
        'comparison-mode-state', 'requestedMode',
        'a comparison request requires Compare mode'
      ));
    }
    return { ok: errors.length === 0, errors: errors };
  }

  function parseLegacy(entrance, rawHash, options) {
    if (ENTRANCES.indexOf(entrance) < 0) throw new Error('entrance must be day or propers');
    const opts = options || {};
    const base = entrance === 'day' ? DAY_KEYS : PROPERS_KEYS;
    const variants = entrance === 'day' ? (opts.variantKeys || []) : [];
    if (!Array.isArray(variants) || variants.some(function (key) {
      return !nonempty(key) || DAY_KEYS.indexOf(key) >= 0;
    }) || new Set(variants).size !== variants.length) {
      throw new Error('variant keys must be unique nonempty keys disjoint from Day legacy keys');
    }
    const known = new Set(base.concat(variants));
    const params = new URLSearchParams(String(rawHash || '').replace(/^#/, ''));
    const recognized = {};
    const present = [];
    const unknown = [];
    const duplicates = [];
    for (const pair of params.entries()) {
      const key = pair[0];
      const value = pair[1];
      if (!known.has(key)) {
        unknown.push({ key: key, value: value });
      } else if (has(recognized, key)) {
        duplicates.push({ key: key, value: value });
      } else {
        recognized[key] = value;
        present.push(key);
      }
    }
    return {
      schema: URL_SCHEMA,
      entrance: entrance,
      recognized: recognized,
      present: present,
      unknown: unknown,
      duplicates: duplicates,
      variantKeys: variants.slice()
    };
  }

  function safeRemembered(storage, entrance) {
    if (!storage || typeof storage.getItem !== 'function') return {};
    try {
      const raw = storage.getItem('triptych:liturgy:' + entrance);
      const value = raw ? JSON.parse(raw) : {};
      return object(value) ? value : {};
    } catch (error) {
      return {};
    }
  }

  function sourceValue(parsed, remembered, defaults, key) {
    if (has(parsed.recognized, key)) {
      return { value: parsed.recognized[key], source: 'url', explicit: true };
    }
    if (has(remembered, key)) {
      return { value: remembered[key], source: 'remembered', explicit: false };
    }
    if (has(defaults, key)) {
      return { value: defaults[key], source: 'repository-default', explicit: false };
    }
    return { value: null, source: 'absent', explicit: false };
  }

  function valuesOf(rows) {
    return Array.isArray(rows) ? rows : [];
  }

  function knownId(table, id) {
    return object(table) && has(table, id);
  }

  /** Repository preference first, then stable identity order; never manifest order. */
  function defaultBibleId(rows, preferred) {
    const held = valuesOf(rows).filter(function (row) {
      return object(row) && nonempty(row.id);
    }).map(function (row) { return row.id; });
    const declared = preferred || DEFAULT_BIBLE_ID;
    if (held.indexOf(declared) >= 0) return declared;
    return held.slice().sort()[0] || null;
  }

  function normalizeLegacy(parsed, options) {
    const opts = options || {};
    const context = opts.context || {};
    const remembered = opts.remembered || {};
    const defaults = opts.defaults || {};
    const errors = [];
    const sources = {};

    if (!object(parsed) || parsed.schema !== URL_SCHEMA || ENTRANCES.indexOf(parsed.entrance) < 0) {
      return { ok: false, errors: [issue('url-state', '', 'invalid parsed URL state')] };
    }
    for (const duplicate of parsed.duplicates || []) {
      errors.push(issue(
        'duplicate-explicit-key', duplicate.key,
        'a semantic URL key may not occur more than once', 'url'
      ));
    }

    function choose(key) {
      let choice = sourceValue(parsed, remembered, defaults, key);
      sources[key] = choice.source;
      return choice;
    }

    function validOrDefault(key, valid, required) {
      let choice = choose(key);
      if (choice.value !== null && choice.value !== '' && valid(choice.value)) return choice.value;
      if (choice.explicit) {
        errors.push(issue(
          'invalid-explicit-value', key,
          'explicit ' + key + ' is invalid for the selected semantic context', 'url'
        ));
        return null;
      }
      if (choice.source === 'remembered') {
        choice = has(defaults, key)
          ? { value: defaults[key], source: 'repository-default', explicit: false }
          : { value: null, source: 'absent', explicit: false };
        sources[key] = choice.source;
        if (choice.value !== null && choice.value !== '' && valid(choice.value)) return choice.value;
      }
      if (required) errors.push(issue('required-url-value', key, key + ' has no valid declared default'));
      return null;
    }

    const missal = validOrDefault('missal', function (id) {
      return knownId(context.missals, id);
    }, true);
    const missalContext = missal && context.missals[missal] || {};
    const bible = validOrDefault('bible', function (id) {
      return knownId(context.bibles, id);
    }, true);
    const orations = validOrDefault('orations', function (lang) {
      return valuesOf(missalContext.orationLanguages).indexOf(lang) >= 0;
    }, true);

    const state = {
      schema: STATE_SCHEMA,
      entrance: parsed.entrance,
      edition: missal ? { id: missal } : null,
      bible: bible ? {
        id: bible,
        numbering: context.bibles[bible] && context.bibles[bible].numbering || null
      } : null,
      languages: { orations: orations },
      requestedMode: null,
      coverage: [],
      unresolvedChoices: [],
      sourceHooks: []
    };

    const legacy = {
      sources: sources,
      unknown: (parsed.unknown || []).slice(),
      inert: [],
      variants: {}
    };
    const mode = validOrDefault('mode', function (value) {
      return MODES.indexOf(value) >= 0;
    }, false);
    const location = validOrDefault('location', nonempty, false);
    if (location !== null) state.semanticLocation = { eventId: location };

    if (parsed.entrance === 'day') {
      state.civilDate = validOrDefault('date', strictDate, true);
      state.calendar = missal ? { id: missalContext.calendar || missal } : null;
      const ordinaryLanguage = validOrDefault('ordinary-lang', function (lang) {
        return valuesOf(missalContext.ordinaryLanguages).indexOf(lang) >= 0;
      }, false);
      if (ordinaryLanguage !== null) state.languages.ordinary = ordinaryLanguage;
      const why = validOrDefault('why', function (value) {
        return value === '0' || value === '1';
      }, false);
      const ordinary = validOrDefault('ordinary', function (value) {
        return value === '0' || value === '1';
      }, false);
      const rubrics = validOrDefault('rubrics', function (value) {
        return value === '0' || value === '1';
      }, false);
      state.apparatus = { why: why === '1', rubrics: rubrics !== '0' };
      const legacyMode = ordinary === '1' ? 'missal' : 'read';
      if (mode !== null && (mode === 'read' || mode === 'missal') &&
          has(parsed.recognized, 'ordinary') && mode !== legacyMode) {
        errors.push(issue(
          'conflicting-explicit-mode', 'mode',
          'explicit mode and legacy ordinary state select different reader modes', 'url'
        ));
      }
      state.requestedMode = mode === null ? legacyMode : mode;
      state.options = {
        ordinary: mode === 'read' ? false : (mode === 'missal' ? true : ordinary === '1'),
        legitimate: {}
      };
      const dayRows = valuesOf(context.dayReadableFormularies);
      const mass = validOrDefault('mass', function (id) {
        return dayRows.some(function (one) { return one.id === id; });
      }, false);
      if (mass) state.selectedReadableFormulary = { id: mass };
      const form = validOrDefault('form', function (id) {
        return mass && valuesOf((missalContext.formsByMass || {})[mass]).indexOf(id) >= 0;
      }, false);
      if (form !== null) state.form = form;
      const translationWitness = validOrDefault('translation-witness', nonempty, false);
      if (translationWitness !== null) {
        state.languages.translationWitness = translationWitness;
      }

      const groups = missalContext.variantGroups || {};
      for (const key of parsed.variantKeys || []) {
        if (!has(parsed.recognized, key)) continue;
        const raw = parsed.recognized[key];
        if (!has(groups, key)) {
          legacy.inert.push({ key: key, value: raw, reason: 'not-applicable-to-selected-edition' });
          continue;
        }
        if (valuesOf(groups[key]).indexOf(raw) < 0) {
          errors.push(issue(
            'invalid-explicit-variant', key,
            'explicit option is not held by the selected edition', 'url'
          ));
          continue;
        }
        state.options.legitimate[key] = raw;
        legacy.variants[key] = raw;
      }
    } else {
      const types = missalContext.types || {};
      const type = validOrDefault('type', function (id) { return has(types, id); }, true);
      const mass = validOrDefault('mass', function (id) {
        return type && valuesOf(types[type]).indexOf(id) >= 0;
      }, true);
      state.formulary = mass ? { id: mass, type: type } : null;
      state.civilDate = null;
      const form = validOrDefault('form', function (id) {
        return mass && valuesOf((missalContext.formsByMass || {})[mass]).indexOf(id) >= 0;
      }, false);
      const cycle = validOrDefault('cycle', nonempty, false);
      const alternative = validOrDefault('alternative', nonempty, false);
      const translationWitness = validOrDefault('translation-witness', nonempty, false);
      if (form !== null) state.form = form;
      if (cycle !== null) state.cycle = cycle;
      if (alternative !== null) state.alternative = { id: alternative };
      if (translationWitness !== null) {
        state.languages.translationWitness = translationWitness;
      }
      state.requestedMode = mode === null ? 'read' : mode;
    }

    const validated = validateReaderState(state);
    errors.push.apply(errors, validated.errors);
    return { ok: errors.length === 0, state: state, legacy: legacy, errors: errors };
  }

  function encodePair(key, value) {
    return encodeURIComponent(key) + '=' + encodeURIComponent(value);
  }

  function serializeLegacy(normalized) {
    if (!normalized || !normalized.ok) throw new Error('only validated URL state can be serialized');
    const state = normalized.state;
    const pairs = [];
    if (state.entrance === 'day') {
      pairs.push(['date', state.civilDate]);
      pairs.push(['missal', state.edition.id]);
      pairs.push(['bible', state.bible.id]);
      pairs.push(['orations', state.languages.orations]);
      pairs.push(['mode', state.requestedMode || (state.options.ordinary ? 'missal' : 'read')]);
      if (state.requestedMode && ['read', 'missal'].indexOf(state.requestedMode) < 0) {
        pairs.push(['ordinary', state.options.ordinary ? '1' : '0']);
      }
      if (state.semanticLocation) pairs.push(['location', state.semanticLocation.eventId]);
      pairs.push(['why', state.apparatus.why ? '1' : '0']);
      if (state.languages.ordinary) pairs.push(['ordinary-lang', state.languages.ordinary]);
      pairs.push(['rubrics', state.apparatus.rubrics ? '1' : '0']);
      if (state.selectedReadableFormulary) pairs.push(['mass', state.selectedReadableFormulary.id]);
      if (state.form) pairs.push(['form', state.form]);
      if (state.languages.translationWitness) {
        pairs.push(['translation-witness', state.languages.translationWitness]);
      }
      Object.keys(normalized.legacy.variants || {}).sort().forEach(function (key) {
        pairs.push([key, normalized.legacy.variants[key]]);
      });
      for (const row of normalized.legacy.inert || []) pairs.push([row.key, row.value]);
    } else {
      pairs.push(['missal', state.edition.id]);
      if (state.formulary) {
        pairs.push(['type', state.formulary.type]);
        pairs.push(['mass', state.formulary.id]);
      }
      pairs.push(['bible', state.bible.id]);
      pairs.push(['orations', state.languages.orations]);
      pairs.push(['mode', state.requestedMode || 'read']);
      if (state.semanticLocation) pairs.push(['location', state.semanticLocation.eventId]);
      if (state.form) pairs.push(['form', state.form]);
      if (has(state, 'cycle') && state.cycle !== null) pairs.push(['cycle', state.cycle]);
      if (state.alternative) pairs.push(['alternative', state.alternative.id]);
      if (state.languages.translationWitness) {
        pairs.push(['translation-witness', state.languages.translationWitness]);
      }
    }
    for (const row of normalized.legacy.unknown || []) pairs.push([row.key, row.value]);
    return '#' + pairs.filter(function (one) {
      return one[1] !== null && one[1] !== undefined;
    }).map(function (one) { return encodePair(one[0], one[1]); }).join('&');
  }

  function validateFixture(value) {
    const errors = [];
    if (!object(value) || value.schema !== FIXTURE_SCHEMA) {
      return { ok: false, errors: [issue('fixture-schema', 'schema', 'fixture must use ' + FIXTURE_SCHEMA)] };
    }
    if (!nonempty(value.id)) errors.push(issue('fixture-id', 'id', 'fixture needs a stable id'));
    if (value.visibility !== 'public-data' && value.visibility !== 'synthetic-non-public') {
      errors.push(issue('fixture-visibility', 'visibility', 'fixture visibility must be explicit'));
    }
    if (value.visibility === 'synthetic-non-public') {
      const mark = value.synthetic;
      if (!object(mark) || mark.contractOnly !== true || mark.liturgicalText !== false ||
          mark.historicalClaims !== false) {
        errors.push(issue(
          'synthetic-boundary', 'synthetic',
          'synthetic fixtures must be contract-only and disclaim text and historical claims'
        ));
      }
      if (!object(value.basis) || value.basis.kind !== 'synthetic-contract' ||
          value.basis.nonPublic !== true) {
        errors.push(issue(
          'synthetic-basis', 'basis',
          'synthetic fixtures need an explicit non-public synthetic-contract basis'
        ));
      }
    } else if (value.visibility === 'public-data') {
      if (has(value, 'synthetic') || !object(value.basis) ||
          value.basis.kind !== 'tracked-production-data' ||
          !Array.isArray(value.basis.paths) || value.basis.paths.length < 1 ||
          value.basis.paths.some(function (one) { return !nonempty(one); })) {
        errors.push(issue(
          'public-fixture-basis', 'basis',
          'public-data fixtures must name tracked production basis paths and cannot be synthetic'
        ));
      }
    }
    const state = validateReaderState(value.requested);
    errors.push.apply(errors, state.errors.map(function (one) {
      return issue(one.code, 'requested.' + one.path, one.message, one.source);
    }));
    if (!object(value.expected)) {
      errors.push(issue('fixture-expected', 'expected', 'fixture needs semantic assertions'));
    } else {
      const expected = value.expected;
      if (!has(expected, 'resolved') ||
          (expected.resolved !== null && !object(expected.resolved))) {
        errors.push(issue(
          'fixture-resolved', 'expected.resolved',
          'fixture must assert a resolved identity or explicit null'
        ));
      } else if (object(expected.resolved)) {
        if (value.requested.comparison && value.requested.entrance === 'propers') {
          if (!nonempty(expected.resolved.correspondence) ||
              expected.resolved.dateIndependent !== true) {
            errors.push(issue(
              'fixture-propers-comparison-result', 'expected.resolved',
              'Propers comparison must assert correspondence and date independence'
            ));
          }
        } else if (value.requested.comparison && value.requested.entrance === 'day') {
          if (!nonempty(expected.resolved.dimension) ||
              !Array.isArray(expected.resolved.sides) || expected.resolved.sides.length < 2) {
            errors.push(issue(
              'fixture-day-comparison-result', 'expected.resolved',
              'Day comparison must assert its dimension and independently resolved sides'
            ));
          } else {
            const requestedComparison = value.requested.comparison;
            if (expected.resolved.dimension !== requestedComparison.dimension ||
                expected.resolved.sides.length !== requestedComparison.sides.length) {
              errors.push(issue(
                'fixture-day-comparison-shape', 'expected.resolved',
                'Day comparison results must match the requested dimension and side count'
              ));
            }
            requestedComparison.sides.forEach(function (requestedSide, index) {
              const resultSide = expected.resolved.sides[index];
              if (!object(resultSide) || resultSide.id !== requestedSide.id ||
                  resultSide.edition !== requestedSide.edition.id ||
                  resultSide.calendar !== requestedSide.calendar.id ||
                  !nonempty(resultSide.calendarResult) || !nonempty(resultSide.formulary)) {
                errors.push(issue(
                  'fixture-day-comparison-side', 'expected.resolved.sides[' + index + ']',
                  'each result side must bind to its requested side and assert calendar and formulary results'
                ));
              }
            });
          }
        } else if (!nonempty(expected.resolved.edition) ||
                   !nonempty(expected.resolved.formulary)) {
          errors.push(issue(
            'fixture-resolved-identity', 'expected.resolved',
            'resolved fixture result needs edition and formulary identities'
          ));
        }
      }
      if (!has(expected, 'calendarResult') ||
          (expected.calendarResult !== null && !object(expected.calendarResult))) {
        errors.push(issue(
          'fixture-calendar-result', 'expected.calendarResult',
          'fixture must assert a calendar result or explicit date-independent null'
        ));
      } else if (value.requested.entrance === 'propers' && expected.calendarResult !== null) {
        errors.push(issue(
          'fixture-propers-calendar-result', 'expected.calendarResult',
          'Propers fixtures must assert explicit date-independent null'
        ));
      } else if (value.requested.entrance === 'day' && object(expected.calendarResult)) {
        if (!strictDate(expected.calendarResult.date) ||
            expected.calendarResult.date !== value.requested.civilDate) {
          errors.push(issue(
            'fixture-day-calendar-date', 'expected.calendarResult.date',
            'Day fixture calendar result must match the fixed civil date'
          ));
        }
        if (value.requested.comparison) {
          const anchor = value.requested.comparison.anchor;
          if (expected.calendarResult.territorialContext !== anchor.territorialContext ||
              expected.calendarResult.resolveEachSideIndependently !== true ||
              expected.calendarResult.showCalendarDifferencesFirst !== true) {
            errors.push(issue(
              'fixture-day-comparison-calendar', 'expected.calendarResult',
              'Day comparison calendar assertions must bind the fixed context and independent resolution'
            ));
          }
        }
      }
      if (!Array.isArray(expected.events)) {
        errors.push(issue('fixture-events', 'expected.events', 'fixture events must be an array'));
      } else {
        const ids = [];
        expected.events.forEach(function (event, index) {
          const at = 'expected.events[' + index + ']';
          if (!object(event) || !nonempty(event.id) || !nonempty(event.kind)) {
            errors.push(issue('fixture-event', at, 'semantic event needs a stable id and kind'));
          } else ids.push(event.id);
          if (object(event) && event.kind === 'proper') {
            errors.push.apply(errors, validateSemanticSlot(event.semanticSlot, at + '.semanticSlot'));
            if (!nonempty(event.editionSlotLabel)) {
              errors.push(issue(
                'fixture-edition-slot-label', at + '.editionSlotLabel',
                'a Proper event retains its edition-local label outside identity'
              ));
            }
          }
          if (object(event) && has(event, 'seat') && event.seat !== null) {
            if (!object(event.seat) || !nonempty(event.seat.id) ||
                !nonempty(event.seat.placement) ||
                ['seated', 'unseated'].indexOf(event.seat.placement) < 0) {
              errors.push(issue(
                'fixture-event-seat', at + '.seat',
                'event seat must carry a stable id and seated or unseated placement'
              ));
            }
          }
          if (object(event) && (event.kind === 'proper' || event.kind === 'ordinary-element') &&
              !object(event.selected)) {
            errors.push(issue(
              'fixture-event-selected', at + '.selected',
              'semantic event must assert selected material and availability'
            ));
          } else if (object(event) && object(event.selected)) {
            errors.push.apply(
              errors, validateSelectedMaterial(event.selected, at + '.selected')
            );
          }
          if (object(event)) errors.push.apply(
            errors, validateSourceHooks(event.sourceHooks, at + '.sourceHooks', true)
          );
        });
        if (new Set(ids).size !== ids.length) {
          errors.push(issue('fixture-event-ids', 'expected.events', 'semantic event ids must be unique'));
        }
      }
      if (!Array.isArray(expected.coverage)) {
        errors.push(issue('fixture-coverage', 'expected.coverage', 'fixture coverage must be an array'));
      } else {
        expected.coverage.forEach(function (one, index) {
          errors.push.apply(errors, validateCoverage(one, 'expected.coverage[' + index + ']'));
        });
      }
      if (!Array.isArray(expected.explicitAbsences)) {
        errors.push(issue(
          'fixture-absences', 'expected.explicitAbsences',
          'fixture explicit absences must be an array'
        ));
      } else expected.explicitAbsences.forEach(function (one, index) {
        errors.push.apply(
          errors, validateExplicitAbsence(one, 'expected.explicitAbsences[' + index + ']')
        );
      });
      if (!Array.isArray(expected.unresolvedChoices)) {
        errors.push(issue(
          'fixture-unresolved-choices', 'expected.unresolvedChoices',
          'fixture unresolved choices must be an array'
        ));
      } else {
        expected.unresolvedChoices.forEach(function (one, index) {
          errors.push.apply(
            errors, validateUnresolvedChoice(one, 'expected.unresolvedChoices[' + index + ']')
          );
        });
      }
      if (expected.url !== null && (!object(expected.url) ||
          !nonempty(expected.url.legacy) || !nonempty(expected.url.canonical) ||
          expected.url.legacy.charAt(0) !== '#' || expected.url.canonical.charAt(0) !== '#')) {
        errors.push(issue(
          'fixture-url', 'expected.url',
          'fixture URL assertion must carry legacy and canonical hash strings or explicit null'
        ));
      }
      if (!/^[0-9a-f]{64}$/.test(expected.semanticHash || '')) {
        errors.push(issue(
          'fixture-semantic-hash', 'expected.semanticHash',
          'fixture must carry a SHA-256 hash of its canonical semantic projection'
        ));
      }
    }
    return { ok: errors.length === 0, errors: errors };
  }

  return Object.freeze({
    STATE_SCHEMA: STATE_SCHEMA,
    FIXTURE_SCHEMA: FIXTURE_SCHEMA,
    URL_SCHEMA: URL_SCHEMA,
    ENTRANCES: ENTRANCES,
    MODES: MODES,
    DEFAULT_BIBLE_ID: DEFAULT_BIBLE_ID,
    STATE_FIELDS: STATE_FIELDS,
    COVERAGE_STATES: COVERAGE_STATES,
    COVERAGE_COMPLETENESS: COVERAGE_COMPLETENESS,
    COVERAGE_REASONS: COVERAGE_REASONS,
    URL_INVENTORY: URL_INVENTORY,
    CANONICAL_ROUTES: CANONICAL_ROUTES,
    strictDate: strictDate,
    canonicalRoute: canonicalRoute,
    coverage: coverage,
    unresolvedChoice: unresolvedChoice,
    resolveAuthorizedChoice: resolveAuthorizedChoice,
    validateCoverage: validateCoverage,
    validateExplicitAbsence: validateExplicitAbsence,
    validateSemanticSlot: validateSemanticSlot,
    validateSelectedMaterial: validateSelectedMaterial,
    validateUnresolvedChoice: validateUnresolvedChoice,
    validateComparison: validateComparison,
    validateReaderState: validateReaderState,
    parseLegacy: parseLegacy,
    safeRemembered: safeRemembered,
    defaultBibleId: defaultBibleId,
    normalizeLegacy: normalizeLegacy,
    serializeLegacy: serializeLegacy,
    validateFixture: validateFixture
  });
}));
