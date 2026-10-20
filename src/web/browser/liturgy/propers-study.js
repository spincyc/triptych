/* Propers Study keeps the source-rendered Read text and adds local apparatus. */
'use strict';

(function (root, factory) {
  const api = factory(root);
  if (typeof module === 'object' && module && module.exports) module.exports = api;
  else root.TriptychPropersStudy = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function (root) {
  function attach(input) {
    const View = root.LiturgyReaderStudyView;
    if (!View || typeof View.attach !== 'function') {
      throw new Error('Propers Study needs the shared source-adjacent apparatus');
    }
    if (!input || !input.result || input.result.entrance !== 'propers' ||
        input.result.calendarResult !== null) {
      throw new Error('Propers Study needs one date-independent adapter result');
    }
    return View.attach({ result: input.result, fragment: input.fragment,
      contents: input.contents, locationPrefix: '' });
  }

  function bindControls(input) {
    const button = root.document.querySelector('[data-mode="study"]');
    if (!button) return;
    button.addEventListener('click', function () {
      const current = input.runtime.normalized && input.runtime.normalized.state;
      if (!current || current.requestedMode === 'study') {
        input.readerShell.close();
        return;
      }
      const captured = input.readerShell.captureSemanticLocation();
      const location = current.requestedMode === 'compare'
        ? input.Compare.fromCompareLocation(captured, input.runtime.result)
        : input.ProperEvents.nearestProperLocation(captured, input.runtime.result);
      input.readerShell.close({ restoreFocus: false });
      input.navigate({ mode: 'study' }, ['compare', 'peer-orations'],
        { location: location, focus: 'mode' });
    });
  }

  return Object.freeze({ attach: attach, bindControls: bindControls });
}));
