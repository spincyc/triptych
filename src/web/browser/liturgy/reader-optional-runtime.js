/* Load the unchanged Ordinary presenter only for validated state that uses it. */
'use strict';

(function (root) {
  const doc = root.document;
  const source = new URL('day.js', doc.currentScript.src).href;
  let pending = null;

  function loadOrdinary() {
    if (root.TriptychOrdinaryRenderer) return Promise.resolve(root.TriptychOrdinaryRenderer);
    if (pending) return pending;
    pending = new Promise(function (resolve, reject) {
      const script = doc.createElement('script');
      script.src = source;
      script.onload = function () {
        if (root.TriptychOrdinaryRenderer) resolve(root.TriptychOrdinaryRenderer);
        else { pending = null; script.remove(); reject(new Error('The Ordinary presenter did not initialize')); }
      };
      script.onerror = function () {
        pending = null;
        script.remove();
        reject(new Error('The Ordinary presenter could not be loaded'));
      };
      doc.head.appendChild(script);
    });
    return pending;
  }

  function forState(state) {
    return state.options.ordinary ? loadOrdinary() : Promise.resolve(null);
  }

  root.TriptychReaderOptionalRuntime = Object.freeze({ loadOrdinary: loadOrdinary, forState: forState });
}(window));
