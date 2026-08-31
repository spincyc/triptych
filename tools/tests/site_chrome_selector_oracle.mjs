#!/usr/bin/env node

/* Real Chromium as the semantic oracle for one question: can this CSS selector
 * reach an element the published layout owns?
 *
 * WHY THIS EXISTS. The question used to be answered in Python, by a hand-written
 * model of CSS selector semantics inside `tools/tests/test_browser_collisions.py`.
 * A second independent cold review reproduced two classes of unsoundness in it,
 * and both were unsoundness for VALID CSS rather than for anything exotic:
 *
 *   - an unknown pseudo-class was treated as satisfiable, which is conservative
 *     in a positive position and the exact opposite inside `:not()`, so
 *     `a:not(:hover)` and `.site-header:not(:focus-within)` — which really do
 *     match site chrome in ordinary states — were read as unable to;
 *   - route scope was inferred by scanning the selector TEXT for a class name
 *     the layout does not own, so `a[href$=".html"]` was read as scoped by
 *     `.html`, `body:has(.plan-page, .site-header) .site-footer a` as scoped
 *     when its `.site-header` alternative makes it global, and
 *     `:is(:not(.plan-page), .plan-page) a` — a tautology — as scoped at all.
 *
 * Neither is fixable by adding cases. A selector engine is what answers the
 * question, and Chromium already ships one. So this harness stops deciding CSS
 * truth and starts asking: it builds the site's real shell for a named set of
 * route states, and for every selector arm asks the browser's own
 * `querySelectorAll` whether the elements it selects include one the layout owns.
 *
 * WHAT IT IS NOT. It is not a CSS engine, a cascade model, or a claim about
 * specificity, `@media` conditions, or which rule wins. Reach is the hazard: a
 * rule that CAN match the masthead reaches every page carrying the file, whether
 * or not it also wins. Nothing here measures appearance.
 *
 * THE PROTOCOL. Line-delimited JSON in on stdin, line-delimited JSON out on
 * stdout, so one Chromium session answers every question a test module has and
 * the browser is started once rather than once per selector:
 *
 *   {"op":"init","states":[{"name":"…","html":"…"}]}   the shells, rendered by
 *                                                     the caller from the
 *                                                     build's own wrapper
 *   {"op":"arms","arms":["a:not(:hover)", …]}          classify and evaluate
 *   {"op":"verify","arms":[…],"states":[…]}            the independent check
 *   {"op":"report"}                                    bounds and measurements
 *   {"op":"quit"}
 *
 * `arms` walks every state once per BATCH, so a caller that asks for everything
 * it needs in one request pays for one walk. `report` returns the batch count,
 * the navigation count and the elapsed milliseconds, so the runtime and the
 * batching are measured facts in the caller's own report rather than a claim.
 *
 * THE THREE ANSWERS, AND FAILING CLOSED. Every arm comes back as one of:
 *
 *   - `reach`: a state name mapped to the descriptor of a chrome element the
 *     selector selects there, or null. Chromium decided it.
 *   - `refusal`: a stated reason the browser could not be asked — the selector
 *     is invalid or unsupported HERE, in the version that ships this gate; or it
 *     names `:visited`, whose truth Chromium deliberately withholds from script
 *     and which therefore cannot be established either way; or it forces a user
 *     state in more than one compound, which the walk below does not establish.
 *     A refusal is reported to the caller as unsafe. It is never silence.
 *   - `origin`: a pseudo-element arm's originating element selector.
 *     `document.querySelectorAll('*::before')` does not throw in Chromium — it
 *     returns NOTHING, which is the most dangerous answer available, so a
 *     pseudo-element arm is judged by the element the pseudo-element belongs to.
 *     That over-approximates deliberately: reaching an element's `::before` is
 *     reaching that element's rendering, and the origin selector matches at
 *     least everywhere the pseudo-element rule applies. The `verify` op reads
 *     the pseudo-element's own computed style to show the over-approximation is
 *     one, in the direction claimed.
 *
 * THE STATE MATRIX. A quiescent document does not answer every question either:
 * `a:hover` matches nothing until something is hovered, and reading that as safe
 * would be a false negative of exactly the kind this harness exists to remove.
 * So each state is walked under real user state — the pointer over each chrome
 * element that contains no other, a press held there, keyboard focus on each
 * focusable chrome element, and the document's own fragment target — and an arm
 * is reached if ANY of those sub-states reaches it. The union is monotone: a
 * sub-state can only ADD reach, never withdraw it, which is why the quiescent
 * pass alone already reports `a:not(:hover)`.
 *
 * The walk forces ONE user state at a time, plus whatever a press carries with
 * it — a press on a link focuses it, so `.site-header:hover a:focus` is reached
 * by accident. It never holds focus on one chrome element while the pointer
 * rests on a different one, and a real reader reaches that state with a Tab and
 * a mouse move: an independent rereview observed real Chromium matching
 * `a:focus ~ .site-footer:hover` and `.skip-link:focus ~ .site-footer:hover a`
 * against layout-owned elements while this walk reported no reach at all. So an
 * arm whose Chromium serialization names a forced user state in two or more
 * DISTINCT compounds is REFUSED, with the reason stated, rather than reported
 * safe. That is the fail-closed answer for a shape the walk cannot establish;
 * widening the walk to co-force states is a larger change and is not what this
 * does.
 *
 * What the matrix does not force is written down rather than assumed.
 * `:disabled`, `:checked`, `:open`, `:placeholder-shown` and the rest of the
 * form and element states cannot become true for any element in the layout's
 * chrome, because the layout emits no form control, no `<details>`, no
 * `<dialog>` and nothing editable. That is not asserted here — it is MEASURED
 * per state and returned as `interactive` by the `init` op, and the caller
 * asserts it empty for every state, so the layout gaining one fails the gate
 * instead of quietly ending the reasoning.
 */

import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdtemp, access } from 'node:fs/promises';
import { constants } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import process from 'node:process';

const CHROME_CANDIDATES = [
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
  '/usr/bin/google-chrome-stable',
  '/usr/bin/google-chrome'
];
const EXIT_NO_BROWSER = 3;

/* The layout's own landmark. Everything outside it is the site's chrome and
 * everything inside it is the page's own content, which is what an instrument
 * stylesheet is for. The landmark itself counts as chrome: a rule that restyles
 * `<main>` restyles it on every route the file reaches. */
const LANDMARK_ID = 'main-content';

/* One viewport, wide enough that the masthead and footer lay out as they do on a
 * desktop and every chrome element has a box the pointer can be moved onto. No
 * assertion here depends on a width; the responsive matrix belongs to
 * corpus_browser_gate.mjs, which measures pages rather than selectors. */
const VIEWPORT = { width: 1280, height: 900 };

/* The user states the matrix forces, by the mechanism that forces each. Written
 * here because the list IS the bound: an arm whose safety depends on a state
 * outside it is not a safe arm this harness has established, and an arm needing
 * two of them at once, on two different chrome elements, is refused rather than
 * reported safe. */
const FORCED_STATES = ['hover', 'active', 'focus', 'focus-visible', 'focus-within', 'target'];

/* Pseudo-classes whose truth Chromium will not report to script. `:visited` is
 * withheld by design — history sniffing — so a rule keyed on it can be neither
 * confirmed nor refuted here, and an arm naming it is refused rather than passed.
 */
const UNESTABLISHABLE = /:visited\b/i;

/* Which arms need the state matrix walked for them. Lexical, over both the arm
 * as written and Chromium's own serialization of it, and deliberately generous:
 * a false positive here explores states an arm does not need, which costs time
 * and cannot change an answer. A false NEGATIVE would matter, which is why the
 * test is `contains` rather than anything cleverer — an escaped `\:hover` inside
 * a class name is matched too, and that is the harmless direction. */
const DYNAMIC = /:(hover|active|focus|focus-visible|focus-within|target)\b/i;

/* The compounds of a selector, split at TOP-LEVEL whitespace and combinators
 * only: a combinator inside `:has(…)` or `:is(…)` belongs to that compound
 * rather than standing beside it. Lexical, like `DYNAMIC`, and applied to
 * Chromium's serialization rather than to the authored text. An escape that
 * hides a separator can only split one compound into two, which is the direction
 * that refuses rather than the direction that passes. */
function topLevelCompounds(selector) {
  const compounds = [];
  let current = '';
  let depth = 0;
  let quote = '';
  for (const character of selector) {
    if (quote) {
      current += character;
      if (character === quote) quote = '';
      continue;
    }
    if (character === '"' || character === "'") {
      quote = character;
      current += character;
      continue;
    }
    if (character === '(' || character === '[') depth += 1;
    else if (character === ')' || character === ']') depth -= 1;
    if (depth <= 0 && /[\s>+~,]/.test(character)) {
      if (current) compounds.push(current);
      current = '';
      continue;
    }
    current += character;
  }
  if (current) compounds.push(current);
  return compounds;
}

/* The compounds of one arm that force a user state. Two or more of them is the
 * shape the walk cannot establish, because the walk holds one user state at a
 * time; see the header comment for the observed witness. */
function statefulCompounds(selector) {
  return topLevelCompounds(selector).filter((compound) => DYNAMIC.test(compound));
}

/* A trailing pseudo-element, on the browser's own serialization of the selector.
 * `::part(name)` and `::slotted(sel)` take an argument, hence the optional
 * group. Applied to `cssRules[0].selectorText`, never to the authored text, so
 * the shape being matched is one Chromium produced. */
const PSEUDO_ELEMENT_TAIL = /::[-A-Za-z0-9_\\]+(\([^()]*\))?$/;

/* The pseudo-elements `getComputedStyle` will resolve, used only by the `verify`
 * op to show that judging a pseudo-element arm by its origin over-approximates
 * rather than under-approximates. Not a claim that CSS has only these. */
const PROBED_PSEUDO_ELEMENTS = [
  '::before', '::after', '::marker', '::first-line', '::first-letter',
  '::placeholder', '::selection', '::backdrop', '::file-selector-button'
];

/* The sentinel the independent check reads. `outline-color` because it does not
 * inherit — an inherited property would report a descendant's reach as its
 * ancestor's — and `!important` because the check is about whether the rule
 * REACHES the element, not about whether it would win a cascade it never has to
 * enter. */
const SENTINEL_PROPERTY = 'outline-color';
const SENTINEL_VALUE = 'rgb(1, 2, 3)';

class CDP {
  constructor(url) {
    this.socket = new WebSocket(url);
    this.next = 0;
    this.pending = new Map();
    this.events = new Map();
  }

  async ready() {
    await new Promise((accept, reject) => {
      this.socket.addEventListener('open', accept, { once: true });
      this.socket.addEventListener('error', reject, { once: true });
    });
    this.socket.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (message.id) {
        const pending = this.pending.get(message.id);
        if (!pending) return;
        this.pending.delete(message.id);
        clearTimeout(pending.timer);
        if (message.error) pending.reject(new Error(message.error.message));
        else pending.accept(message.result);
        return;
      }
      (this.events.get(message.method) || []).forEach((listener) => listener(message.params || {}));
    });
  }

  on(name, listener) {
    if (!this.events.has(name)) this.events.set(name, []);
    this.events.get(name).push(listener);
  }

  send(method, params = {}) {
    const id = ++this.next;
    return new Promise((accept, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error('CDP command timed out: ' + method));
      }, 30000);
      this.pending.set(id, { accept, reject, timer });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }

  close() {
    this.socket.close();
  }
}

async function exists(path) {
  try {
    await access(path, constants.R_OK);
    return true;
  } catch (_error) {
    return false;
  }
}

async function waitForJson(url, attempts = 300) {
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return await response.json();
    } catch (_error) {
      // Chromium's debugging endpoint is not ready yet.
    }
    await new Promise((accept) => setTimeout(accept, 50));
  }
  throw new Error('Chromium debugging endpoint did not become ready: ' + url);
}

/* --------------------------------------------------------------- page-side code
 *
 * Everything below runs in the page. It answers three things and infers nothing:
 * which elements are chrome, whether Chromium accepts a selector, and which
 * elements a selector selects. */

const INSTALL = `((landmarkId) => {
  const main = document.getElementById(landmarkId);
  if (!main) return { error: 'the shell carries no #' + landmarkId + ' landmark' };
  /* Captured BEFORE the probe stylesheet is appended, so the probe is never
   * mistaken for part of the layout. */
  const chrome = [...document.querySelectorAll('*')].filter(
    (node) => node === main || !main.contains(node)
  );
  const describe = (node) => {
    const value = (node.getAttribute && node.getAttribute('class') || '').trim();
    return node.tagName.toLowerCase() +
      (node.id ? '#' + node.id : '') +
      (value ? '.' + value.split(/\\s+/).join('.') : '');
  };
  const probe = document.createElement('style');
  document.head.appendChild(probe);
  const sentinel = document.createElement('style');
  document.head.appendChild(sentinel);
  const chromeSet = new Set(chrome);
  /* A chrome element that contains no other chrome element. Moving the pointer
   * onto one of these puts every chrome ancestor of it into :hover too, so the
   * set of leaves is the set of pointer positions the matrix needs. */
  const leaves = chrome.filter(
    (node) => !chrome.some((other) => other !== node && node.contains(other))
  );
  const box = (node) => {
    const rect = node.getBoundingClientRect();
    return { width: rect.width, height: rect.height, x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };
  };
  /* Positions and focus stops are carried as INDEXES into the chrome list, not
   * as descriptors. The layout's navigation and footer links are anchors with
   * neither id nor class, so several of them describe identically and a walk
   * keyed on the description would visit the first one five times and the other
   * four never. */
  const at = (node) => chrome.indexOf(node);
  window.__oracle = {
    main, chrome, chromeSet, describe, probe, sentinel,
    reach(arm) {
      let selected;
      try {
        selected = document.querySelectorAll(arm);
      } catch (error) {
        return { rejected: (error && error.name) || 'error' };
      }
      for (const node of selected) if (chromeSet.has(node)) return describe(node);
      return null;
    },
    reachAll(arms) { return arms.map((arm) => this.reach(arm)); },
    /* Chromium's own parser is the judge of whether a selector is a selector,
     * and its own serialization is what the pseudo-element question is asked
     * about. A declaration is attached because a rule with none may be dropped. */
    classify(arm) {
      this.probe.textContent = '';
      let accepted = false;
      let serialized = null;
      let detail = null;
      try {
        this.probe.textContent = arm + ' { --oracle-probe: 1; }';
        const rules = this.probe.sheet.cssRules;
        accepted = rules.length === 1 && rules[0].type === CSSRule.STYLE_RULE;
        if (rules.length !== 1) detail = 'parsed as ' + rules.length + ' rules';
        else if (!accepted) detail = 'parsed as a non-style rule';
        else serialized = rules[0].selectorText;
      } catch (error) {
        detail = (error && error.message) || 'threw';
      }
      this.probe.textContent = '';
      return { accepted, serialized, detail };
    },
    /* The independent observation: not "which elements does this selector
     * select" but "which elements does a rule written with it actually reach",
     * read out of the style engine through a non-inherited property. */
    sentinelReach(arm, property, value, pseudos) {
      this.sentinel.textContent = '';
      try {
        this.sentinel.textContent = arm + ' { ' + property + ': ' + value + ' !important; }';
      } catch (error) {
        this.sentinel.textContent = '';
        return { rejected: (error && error.message) || 'threw' };
      }
      if (this.sentinel.sheet.cssRules.length !== 1) {
        this.sentinel.textContent = '';
        return { rejected: 'the browser kept no rule for it' };
      }
      const element = [];
      const pseudo = {};
      for (const node of this.chrome) {
        if (getComputedStyle(node).getPropertyValue(property) === value) element.push(this.describe(node));
        for (const one of pseudos) {
          if (getComputedStyle(node, one).getPropertyValue(property) === value) {
            (pseudo[one] = pseudo[one] || []).push(this.describe(node));
          }
        }
      }
      this.sentinel.textContent = '';
      return { element, pseudo };
    },
    hoverTargets: leaves.map((node) => ({ index: at(node), descriptor: describe(node), ...box(node) })),
    focusables: chrome
      .filter((node) => node.matches('a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'))
      .map((node) => ({ index: at(node), descriptor: describe(node) })),
    identifiers: chrome.filter((node) => node.id).map((node) => node.id),
    /* Measured, not assumed. The form and element states the matrix does not
     * force cannot become true for an element that is not one of these. */
    interactive: chrome
      .filter((node) => node.matches(
        'input, select, textarea, button, option, optgroup, fieldset, details, ' +
        'dialog, summary, label, output, progress, meter, [contenteditable], [popover]'
      ))
      .map(describe)
  };
  return {
    chromeCount: chrome.length,
    descriptors: chrome.map(describe),
    hoverTargets: window.__oracle.hoverTargets,
    focusables: window.__oracle.focusables,
    identifiers: window.__oracle.identifiers,
    interactive: window.__oracle.interactive
  };
})(${JSON.stringify(LANDMARK_ID)})`;

/* ------------------------------------------------------------------ the harness */

class Oracle {
  constructor(cdp, base) {
    this.cdp = cdp;
    this.base = base;
    this.states = [];
    this.dynamicStates = null;
    this.arms = new Map();
    this.walks = [];
    this.batches = 0;
    this.navigations = 0;
    this.evaluations = 0;
    this.startedAt = Date.now();
    this.installedAt = null;
    this.current = null;
  }

  async evaluate(expression) {
    this.evaluations += 1;
    const result = await this.cdp.send('Runtime.evaluate', {
      expression, awaitPromise: true, returnByValue: true
    });
    if (result.exceptionDetails) {
      throw new Error(
        result.exceptionDetails.exception?.description || result.exceptionDetails.text
      );
    }
    return result.result.value;
  }

  async open(index) {
    const state = this.states[index];
    this.navigations += 1;
    await this.cdp.send('Page.navigate', { url: `${this.base}/state/${index}.html` });
    /* The shells are served from memory by this process and carry no script that
     * runs, so one readiness poll is the whole wait. */
    for (let attempt = 0; attempt < 200; attempt += 1) {
      const ready = await this.evaluate('document.readyState === "complete"');
      if (ready) break;
      await new Promise((accept) => setTimeout(accept, 10));
    }
    const installed = await this.evaluate(INSTALL);
    if (installed && installed.error) {
      throw new Error(`${state.name}: ${installed.error}`);
    }
    this.current = index;
    return installed;
  }

  async init(states, dynamicStates) {
    this.states = states.map((state) => ({ name: state.name, html: state.html }));
    this.dynamicStates = dynamicStates && dynamicStates.length
      ? dynamicStates
      : null;
    const model = {};
    for (let index = 0; index < this.states.length; index += 1) {
      model[this.states[index].name] = await this.open(index);
    }
    this.installedAt = Date.now();
    return { states: model };
  }

  /* One classification per arm for the whole run: whether Chromium accepts it,
   * how Chromium writes it, whether it names a pseudo-element and what that
   * pseudo-element belongs to, and whether it needs the state matrix. */
  async classify(arms) {
    const fresh = arms.filter((arm) => !this.arms.has(arm));
    if (!fresh.length) return fresh;
    const classified = await this.evaluate(
      `${JSON.stringify(fresh)}.map((arm) => window.__oracle.classify(arm))`
    );
    for (let index = 0; index < fresh.length; index += 1) {
      const arm = fresh[index];
      const { accepted, serialized, detail } = classified[index];
      const record = {
        accepted, serialized, judged: arm, origin: null, refusal: null, walked: false,
        dynamic: DYNAMIC.test(arm) || DYNAMIC.test(serialized || ''), reach: {}
      };
      if (!accepted) {
        record.refusal =
          'Chromium does not accept it as a selector' + (detail ? ` (${detail})` : '');
      } else if (UNESTABLISHABLE.test(serialized)) {
        record.refusal =
          'it names a pseudo-class whose truth Chromium withholds from script, so ' +
          'neither reach nor safety can be established here';
      } else if (statefulCompounds(serialized).length > 1) {
        const stateful = statefulCompounds(serialized);
        record.refusal =
          `it forces a user state in ${stateful.length} distinct compounds ` +
          `(${stateful.join(', ')}), and this walk holds one user state at a time — ` +
          'a reader who tabs to one chrome element and then moves the pointer onto ' +
          'another is in a state the walk never visits, so the arm can be neither ' +
          'reached nor established safe here';
      } else {
        const tail = serialized.match(PSEUDO_ELEMENT_TAIL);
        if (tail) {
          const origin = serialized.slice(0, tail.index).trim() || '*';
          const check = await this.evaluate(
            `window.__oracle.classify(${JSON.stringify(origin)})`
          );
          if (!check.accepted) {
            record.refusal =
              `it names the pseudo-element \`${tail[0]}\`, and the element it would ` +
              `belong to (\`${origin}\`) is not itself a selector Chromium accepts`;
          } else {
            record.origin = origin;
            record.judged = origin;
            record.dynamic = record.dynamic || DYNAMIC.test(origin);
          }
        }
      }
      this.arms.set(arm, record);
    }
    return fresh;
  }

  async hover(target) {
    await this.cdp.send('Input.dispatchMouseEvent', {
      type: 'mouseMoved', x: target.x, y: target.y, button: 'none', clickCount: 0
    });
  }

  async press(target, type) {
    await this.cdp.send('Input.dispatchMouseEvent', {
      type, x: target.x, y: target.y, button: 'left', clickCount: 1
    });
  }

  /* One walk of one state, over one list of arms. `record` is called with the
   * name of the sub-state that reached an arm, and only the FIRST reach is kept:
   * the question is whether a route with no instrument marker can be reached at
   * all, and one witness answers it. */
  async walk(stateIndex, batch, dynamicBatch) {
    const state = this.states[stateIndex];
    const installed = await this.open(stateIndex);
    /* The sub-state walk is bounded to the states the caller names: the shells
     * whose reach actually decides the verdict, plus one representative page
     * that carries the chrome the others do not. Every state still gets the
     * quiescent pass, which is where static reach is recorded; a dynamic arm's
     * reach OUTSIDE the walked states is simply not observed, and the report
     * says which states were walked rather than leaving it implicit. */
    const walkDynamic = this.dynamicStates === null
      || this.dynamicStates.includes(state.name);
    const note = (arms, results, substate) => {
      for (let index = 0; index < arms.length; index += 1) {
        const record = this.arms.get(arms[index]);
        if (!record || record.refusal) continue;
        /* One witness answers the question, so a state that has already been
         * reached is not re-recorded and the sub-state that first reached it is
         * the one kept. */
        if (record.reach[state.name]) continue;
        const result = results[index];
        if (result && result.rejected) {
          record.refusal = `Chromium rejected it while matching: ${result.rejected}`;
          continue;
        }
        record.reach[state.name] = result === null ? null : { substate, element: result };
      }
    };
    const judged = (arms) => arms.map((arm) => this.arms.get(arm).judged);
    const evaluateAll = async (arms) => {
      if (!arms.length) return [];
      return this.evaluate(`window.__oracle.reachAll(${JSON.stringify(judged(arms))})`);
    };

    note(batch, await evaluateAll(batch), 'quiescent');
    if (!dynamicBatch.length || !walkDynamic) {
      return { state: state.name, substates: ['quiescent'], walkedDynamic: walkDynamic && dynamicBatch.length > 0 };
    }

    const substates = ['quiescent'];
    const unreachable = [];
    for (const target of installed.hoverTargets) {
      const label = `${target.descriptor}[${target.index}]`;
      if (target.width <= 0 || target.height <= 0) {
        unreachable.push(`${label}: no box to move the pointer onto`);
        continue;
      }
      await this.hover(target);
      const landed = await this.evaluate(
        `window.__oracle.chrome[${target.index}].matches(':hover')`
      );
      if (!landed) unreachable.push(`${label}: the pointer did not land on it`);
      note(dynamicBatch, await evaluateAll(dynamicBatch), `hover:${label}`);
      await this.press(target, 'mousePressed');
      note(dynamicBatch, await evaluateAll(dynamicBatch), `active:${label}`);
      await this.press(target, 'mouseReleased');
      substates.push(`hover:${label}`, `active:${label}`);
    }
    await this.hover({ x: 0, y: 0 });

    /* `:focus-visible` is a claim about HOW focus arrived. One real Tab sets the
     * keyboard modality for the rest of the walk, after which a focus() call is
     * focus-visible focus — asserted rather than assumed by returning what the
     * page reports for each element. */
    for (const type of ['keyDown', 'keyUp']) {
      await this.cdp.send('Input.dispatchKeyEvent', {
        type, key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9, nativeVirtualKeyCode: 9, text: ''
      });
    }
    const focusStates = [];
    for (const stop of installed.focusables) {
      const label = `${stop.descriptor}[${stop.index}]`;
      const held = await this.evaluate(`(() => {
        const node = window.__oracle.chrome[${stop.index}];
        node.focus();
        return { focus: node.matches(':focus'), visible: node.matches(':focus-visible') };
      })()`);
      note(dynamicBatch, await evaluateAll(dynamicBatch), `focus:${label}`);
      substates.push(`focus:${label}`);
      focusStates.push({ stop: label, ...(held || {}) });
    }
    await this.evaluate('document.activeElement && document.activeElement.blur()');

    for (const identifier of installed.identifiers) {
      await this.evaluate(`location.hash = ${JSON.stringify('#' + identifier)}`);
      note(dynamicBatch, await evaluateAll(dynamicBatch), `target:#${identifier}`);
      substates.push(`target:#${identifier}`);
    }
    await this.evaluate(`history.replaceState(null, '', location.pathname)`);

    return { state: state.name, substates, unhovered: unreachable, focusStates };
  }

  async ask(arms) {
    await this.classify(arms);
    /* An arm the `verify` op classified but never walked is not an arm with no
     * reach; it is an arm nothing has asked about yet. The flag is what keeps the
     * two apart, so asking after verifying cannot return an empty reach map as
     * though it were an answer. */
    const pending = arms.filter((arm) => {
      const record = this.arms.get(arm);
      return !record.refusal && !record.walked;
    });
    if (pending.length) {
      this.batches += 1;
      const dynamic = pending.filter((arm) => this.arms.get(arm).dynamic);
      for (let index = 0; index < this.states.length; index += 1) {
        this.walks.push({ batch: this.batches, ...(await this.walk(index, pending, dynamic)) });
      }
      for (const arm of pending) this.arms.get(arm).walked = true;
    }
    const answer = {};
    for (const arm of arms) {
      const record = this.arms.get(arm);
      answer[arm] = {
        accepted: record.accepted,
        serialized: record.serialized,
        origin: record.origin,
        judged: record.judged,
        dynamic: record.dynamic,
        refusal: record.refusal,
        reach: record.reach
      };
    }
    return { arms: answer, batches: this.batches, walks: this.walks };
  }

  /* The independent check. Two things are asked that the answer above does not
   * rest on: the style engine's own reach for the arm as written, read through a
   * non-inherited property; and the same reading with every user state forced on
   * every chrome node through the protocol DevTools uses, which is a different
   * mechanism from the real pointer and keyboard the walk above uses. */
  async verify(arms, stateNames) {
    const wanted = stateNames && stateNames.length
      ? stateNames
      : this.states.map((state) => state.name);
    await this.classify(arms);
    const rows = [];
    for (const name of wanted) {
      const index = this.states.findIndex((state) => state.name === name);
      if (index < 0) throw new Error(`no such state: ${name}`);
      await this.open(index);
      const { root } = await this.cdp.send('DOM.getDocument', { depth: -1 });
      const { nodeIds } = await this.cdp.send('DOM.querySelectorAll', {
        nodeId: root.nodeId, selector: '*'
      });
      for (const forced of [false, true]) {
        for (const nodeId of nodeIds) {
          await this.cdp.send('CSS.forcePseudoState', {
            nodeId, forcedPseudoClasses: forced ? FORCED_STATES : []
          });
        }
        for (const arm of arms) {
          const record = this.arms.get(arm) || { judged: arm, origin: null, refusal: null };
          const selectorApi = await this.evaluate(
            `window.__oracle.reach(${JSON.stringify(record.judged)})`
          );
          const sentinel = await this.evaluate(
            `window.__oracle.sentinelReach(${JSON.stringify(arm)}, ` +
            `${JSON.stringify(SENTINEL_PROPERTY)}, ${JSON.stringify(SENTINEL_VALUE)}, ` +
            `${JSON.stringify(PROBED_PSEUDO_ELEMENTS)})`
          );
          rows.push({
            state: name, arm, forced, judged: record.judged, origin: record.origin,
            selectorApi, sentinel
          });
        }
      }
      for (const nodeId of nodeIds) {
        await this.cdp.send('CSS.forcePseudoState', { nodeId, forcedPseudoClasses: [] });
      }
    }
    return { verification: rows };
  }

  report(chromeVersion) {
    return {
      chrome: chromeVersion,
      landmark: LANDMARK_ID,
      viewport: VIEWPORT,
      forcedStates: FORCED_STATES,
      probedPseudoElements: PROBED_PSEUDO_ELEMENTS,
      sentinel: { property: SENTINEL_PROPERTY, value: SENTINEL_VALUE },
      states: this.states.map((state) => state.name),
      dynamicStatesWalked: this.dynamicStates
        ? this.dynamicStates.slice()
        : this.states.map((state) => state.name),
      browserSessions: 1,
      batches: this.batches,
      navigations: this.navigations,
      evaluations: this.evaluations,
      arms: this.arms.size,
      startupMs: this.installedAt ? this.installedAt - this.startedAt : null,
      elapsedMs: Date.now() - this.startedAt
    };
  }
}

async function readRequests(onRequest) {
  let buffer = '';
  for await (const chunk of process.stdin) {
    buffer += chunk.toString();
    let newline = buffer.indexOf('\n');
    while (newline >= 0) {
      const line = buffer.slice(0, newline).trim();
      buffer = buffer.slice(newline + 1);
      if (line) {
        const done = await onRequest(JSON.parse(line));
        if (done) return;
      }
      newline = buffer.indexOf('\n');
    }
  }
}

async function main() {
  const binary = process.env.TRIPTYCH_CHROME
    || (await Promise.all(CHROME_CANDIDATES.map(exists)))
      .map((present, index) => (present ? CHROME_CANDIDATES[index] : null))
      .find(Boolean)
    || null;
  if (!binary || !(await exists(binary))) {
    process.stderr.write(
      'site_chrome_selector_oracle: no Chromium binary is available.\n' +
      'Set TRIPTYCH_CHROME to a Chromium or Chrome executable, for example\n' +
      '  TRIPTYCH_CHROME=/usr/bin/chromium\n' +
      `Tried: ${process.env.TRIPTYCH_CHROME || CHROME_CANDIDATES.join(', ')}\n` +
      'This harness reports nothing rather than reporting a selector proof it did ' +
      'not observe.\n'
    );
    process.exitCode = EXIT_NO_BROWSER;
    return;
  }

  /* The shells are served rather than assigned into the document, because a
   * served document is the one a reader receives: relative references resolve,
   * `location` is a real URL, and the fragment target state is reachable. Every
   * subresource answers 200 with nothing, so the page's own stylesheets and
   * scripts are present in the DOM exactly as the build emits them while
   * contributing no declaration and running no code — this harness measures which
   * selectors can reach the chrome, not which of them would win. */
  let states = [];
  const server = createServer((request, response) => {
    const match = /^\/state\/(\d+)\.html$/.exec(new URL(request.url, 'http://127.0.0.1').pathname);
    if (match && states[Number(match[1])]) {
      const body = Buffer.from(states[Number(match[1])].html, 'utf8');
      response.writeHead(200, {
        'content-type': 'text/html; charset=utf-8',
        'content-length': body.length,
        'cache-control': 'no-store'
      });
      response.end(body);
      return;
    }
    response.writeHead(200, { 'content-length': 0, 'cache-control': 'no-store' });
    response.end();
  });
  await new Promise((accept, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', accept);
  });
  const base = `http://127.0.0.1:${server.address().port}`;

  const profile = await mkdtemp(join(tmpdir(), 'triptych-selector-oracle-'));
  const debugPort = await new Promise((accept) => {
    const probe = createServer();
    probe.listen(0, '127.0.0.1', () => {
      const { port } = probe.address();
      probe.close(() => accept(port));
    });
  });
  const chrome = spawn(binary, [
    '--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu',
    '--disable-extensions', '--disable-component-extensions-with-background-pages',
    '--disable-background-networking', '--disable-component-update',
    '--disable-domain-reliability', '--disable-client-side-phishing-detection',
    '--disable-sync', '--no-pings', '--no-service-autorun', '--metrics-recording-only',
    '--password-store=basic', '--use-mock-keychain', '--mute-audio',
    '--disable-features=Translate,MediaRouter,OptimizationHints,InterestFeedContentSuggestions,CalculateNativeWinOcclusion,PushMessaging',
    `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', 'about:blank'
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  let chromeStderr = '';
  chrome.stderr.on('data', (chunk) => { chromeStderr += chunk.toString(); });

  let cdp = null;
  const write = (value) => process.stdout.write(JSON.stringify(value) + '\n');
  try {
    const version = await waitForJson(`http://127.0.0.1:${debugPort}/json/version`);
    const created = await (await fetch(
      `http://127.0.0.1:${debugPort}/json/new?${encodeURIComponent('about:blank')}`,
      { method: 'PUT' }
    )).json();
    cdp = new CDP(created.webSocketDebuggerUrl);
    await cdp.ready();
    for (const domain of ['Page', 'Runtime', 'DOM', 'CSS']) await cdp.send(`${domain}.enable`);
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: VIEWPORT.width, height: VIEWPORT.height, deviceScaleFactor: 1, mobile: false,
      screenWidth: VIEWPORT.width, screenHeight: VIEWPORT.height
    });
    await cdp.send('Page.bringToFront');
    /* The walk presses the pointer on chrome elements, and most of them are
     * links. Following one would replace the document under the walk, so the
     * default action is refused in the capture phase — the state the press
     * creates is what is wanted, never its consequence. */
    await cdp.send('Page.addScriptToEvaluateOnNewDocument', {
      source:
        "document.addEventListener('click', (event) => event.preventDefault(), true);\n" +
        "document.addEventListener('auxclick', (event) => event.preventDefault(), true);\n" +
        "document.addEventListener('submit', (event) => event.preventDefault(), true);\n"
    });

    const oracle = new Oracle(cdp, base);
    await readRequests(async (request) => {
      try {
        if (request.op === 'init') {
          states = request.states || [];
          write({ ok: true, ...(await oracle.init(states, request.dynamicStates)) });
          return false;
        }
        if (request.op === 'arms') {
          write({ ok: true, ...(await oracle.ask(request.arms || [])) });
          return false;
        }
        if (request.op === 'verify') {
          write({ ok: true, ...(await oracle.verify(request.arms || [], request.states || [])) });
          return false;
        }
        if (request.op === 'report') {
          write({ ok: true, report: oracle.report(version.Browser || 'unknown') });
          return false;
        }
        if (request.op === 'quit') {
          write({ ok: true });
          return true;
        }
        write({ ok: false, error: `unknown op: ${request.op}` });
        return false;
      } catch (error) {
        write({
          ok: false,
          error: (error && (error.stack || error.message)) || String(error),
          chromeStderr: chromeStderr.slice(-2000)
        });
        return false;
      }
    });
  } catch (error) {
    write({
      ok: false,
      error: (error && (error.stack || error.message)) || String(error),
      chromeStderr: chromeStderr.slice(-2000)
    });
    process.exitCode = 1;
  } finally {
    if (cdp) cdp.close();
    chrome.kill('SIGTERM');
    await new Promise((accept) => server.close(accept));
  }
}

await main();
