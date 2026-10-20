/* Attach Study evidence to the source-rendered Day Read or Missal document. */
'use strict';

(function (root) {
  function attach(row) {
    const view = root.LiturgyReaderStudyView;
    if (!view || typeof view.attach !== 'function') {
      throw new Error('Day Study needs the production Study view');
    }
    const rendered = view.attach({
      result: row.result,
      fragment: row.fragment,
      contents: row.contents,
      locationPrefix: row.prefix || ''
    });
    row.fragment = rendered.fragment;
    row.contents = rendered.contents;
    return rendered;
  }

  function bindControls(input) {
    ['read', 'missal', 'study'].forEach(function (mode) {
      root.document.querySelectorAll('[data-mode="' + mode + '"], [data-reader-action="' + mode + '"]')
        .forEach(function (button) {
          button.addEventListener('click', function () {
            if (input.runtime.mode === mode) { input.readerShell.close(); return; }
            const location = input.captureModeLocation(mode);
            input.readerShell.close({ restoreFocus: false, restoreScroll: false });
            input.onModeSwitch();
            const state = input.runtime.normalized && input.runtime.normalized.state;
            input.navigate({ mode: mode, ordinary: mode === 'study' &&
              state && state.options.ordinary ? '1' : null }, ['compare', 'peer-missal', 'territory'], {
              location: location, modeFocus: true,
              focus: button.dataset.readerAction === 'study' ? { kind: 'study-action' } : null
            });
          });
        });
    });
  }

  function syncMode(mode) {
    const action = root.document.querySelector('[data-reader-action="study"]');
    if (action) action.setAttribute('aria-current', String(mode === 'study'));
  }

  root.TriptychDayStudy = Object.freeze({ attach: attach, bindControls: bindControls, syncMode: syncMode });
}(typeof globalThis !== 'undefined' ? globalThis : this));
