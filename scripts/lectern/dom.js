'use strict';
/*
 * Just enough of a document for the shared renderers to build their nodes, and
 * a reader that turns what they built back into blocks of styled runs.
 *
 * The browser's renderers (`browser-core.js` renderProper and its helpers) own
 * every sentence a page says about a text: its absences, its witness, its
 * claim. Running them against this document lets the terminal print those
 * sentences rather than a second copy of them. Nothing is laid out here; the
 * class names the renderer chose travel with each run, and the terminal styles
 * by them.
 */

class Node {
  constructor(type) {
    this.nodeType = type;
    this.childNodes = [];
    this.parentNode = null;
  }
  get firstChild() { return this.childNodes[0] || null; }
  get lastChild() { return this.childNodes[this.childNodes.length - 1] || null; }
  get children() { return this.childNodes.filter((one) => one.nodeType === 1); }
  get textContent() { return this.childNodes.map((one) => one.textContent).join(''); }
  set textContent(value) {
    this.childNodes.forEach((one) => { one.parentNode = null; });
    this.childNodes = [];
    if (value !== null && value !== undefined && value !== '') this.appendChild(new Text(String(value)));
  }
  appendChild(child) {
    if (child.nodeType === 11) {
      const moved = child.childNodes.slice();
      child.childNodes = [];
      moved.forEach((one) => this.appendChild(one));
      return child;
    }
    if (child.parentNode) child.parentNode.removeChild(child);
    child.parentNode = this;
    this.childNodes.push(child);
    return child;
  }
  append(...items) {
    items.forEach((item) => this.appendChild(typeof item === 'string' ? new Text(item) : item));
  }
  prepend(...items) {
    const nodes = items.map((item) => (typeof item === 'string' ? new Text(item) : item));
    nodes.reverse().forEach((node) => this.insertBefore(node, this.firstChild));
  }
  insertBefore(child, before) {
    if (!before) return this.appendChild(child);
    if (child.nodeType === 11) {
      child.childNodes.slice().forEach((one) => this.insertBefore(one, before));
      child.childNodes = [];
      return child;
    }
    if (child.parentNode) child.parentNode.removeChild(child);
    const at = this.childNodes.indexOf(before);
    child.parentNode = this;
    this.childNodes.splice(at < 0 ? this.childNodes.length : at, 0, child);
    return child;
  }
  removeChild(child) {
    const at = this.childNodes.indexOf(child);
    if (at >= 0) this.childNodes.splice(at, 1);
    child.parentNode = null;
    return child;
  }
  remove() { if (this.parentNode) this.parentNode.removeChild(this); }
  after(...items) {
    if (!this.parentNode) return;
    const parent = this.parentNode;
    const next = parent.childNodes[parent.childNodes.indexOf(this) + 1] || null;
    items.forEach((item) => parent.insertBefore(typeof item === 'string' ? new Text(item) : item, next));
  }
  before(...items) {
    if (!this.parentNode) return;
    items.forEach((item) => this.parentNode.insertBefore(typeof item === 'string' ? new Text(item) : item, this));
  }
  contains(other) {
    for (let node = other; node; node = node.parentNode) if (node === this) return true;
    return false;
  }
  querySelectorAll(selector) {
    const direct = /^:scope\s*>\s*(.+)$/.exec(selector.trim());
    if (direct) return this.children.filter((one) => one.matches(direct[1]));
    const found = [];
    const walk = (node) => node.children.forEach((one) => {
      if (one.matches(selector)) found.push(one);
      walk(one);
    });
    walk(this);
    return found;
  }
  querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
  addEventListener() {}
  removeEventListener() {}
}

class Text extends Node {
  constructor(value) { super(3); this.nodeValue = value; }
  get textContent() { return this.nodeValue; }
  set textContent(value) { this.nodeValue = String(value); }
}

class Fragment extends Node {
  constructor() { super(11); }
}

class ClassList {
  constructor(element) { this.element = element; }
  get names() { return this.element.className.split(/\s+/).filter(Boolean); }
  add(...names) { this.element.className = Array.from(new Set(this.names.concat(names))).join(' '); }
  remove(...names) { this.element.className = this.names.filter((one) => !names.includes(one)).join(' '); }
  contains(name) { return this.names.includes(name); }
  toggle(name, force) {
    const on = force === undefined ? !this.contains(name) : force;
    if (on) this.add(name); else this.remove(name);
    return on;
  }
}

class Element extends Node {
  constructor(tag) {
    super(1);
    this.tagName = String(tag).toUpperCase();
    this.localName = String(tag).toLowerCase();
    this.className = '';
    this.attributes = {};
    const dataName = (key) => 'data-' + String(key).replace(/[A-Z]/g, (letter) => '-' + letter.toLowerCase());
    this.dataset = new Proxy({}, {
      set: (data, key, value) => {
        data[key] = String(value);
        this.attributes[dataName(key)] = String(value);
        return true;
      },
      deleteProperty: (data, key) => {
        delete data[key];
        delete this.attributes[dataName(key)];
        return true;
      },
    });
    this.style = {};
    this.classList = new ClassList(this);
  }
  setAttribute(name, value) {
    this.attributes[name] = String(value);
    if (name === 'class') this.className = String(value);
    if (name.startsWith('data-')) {
      this.dataset[name.slice(5).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase())] = value;
    }
  }
  getAttribute(name) { return Object.prototype.hasOwnProperty.call(this.attributes, name) ? this.attributes[name] : null; }
  hasAttribute(name) { return Object.prototype.hasOwnProperty.call(this.attributes, name); }
  removeAttribute(name) {
    delete this.attributes[name];
    if (name.startsWith('data-')) {
      delete this.dataset[name.slice(5).replace(/-([a-z])/g, (_, letter) => letter.toUpperCase())];
    }
  }
  get hidden() { return this.hasAttribute('hidden'); }
  set hidden(value) { this.toggleAttribute('hidden', Boolean(value)); }
  toggleAttribute(name, force) {
    const on = force === undefined ? !this.hasAttribute(name) : force;
    if (on) this.attributes[name] = ''; else delete this.attributes[name];
    return on;
  }
  matches(selector) {
    return selector.split(',').some((one) => simple(this, one.trim()));
  }
  closest(selector) {
    for (let node = this; node && node.nodeType === 1; node = node.parentNode) {
      if (node.matches(selector)) return node;
    }
    return null;
  }
  focus() {}
  scrollIntoView() {}
}

/* Tag, .class, tag.class and [attribute] selectors: what the renderers ask. */
function simple(element, selector) {
  const match = /^([a-z0-9]*)((?:\.[\w-]+)*)((?:\[[\w-]+\])*)$/i.exec(selector);
  if (!match) return false;
  if (match[1] && element.localName !== match[1].toLowerCase()) return false;
  const classes = match[2].split('.').filter(Boolean);
  if (!classes.every((name) => element.classList.contains(name))) return false;
  const attributes = (match[3].match(/[\w-]+/g) || []);
  return attributes.every((name) => element.hasAttribute(name));
}

const document = {
  createElement: (tag) => new Element(tag),
  createTextNode: (value) => new Text(String(value)),
  createDocumentFragment: () => new Fragment(),
  getElementById: () => null,
  querySelector: () => null,
  querySelectorAll: () => [],
  addEventListener() {},
  getSelection: () => null,
  body: new Element('body'),
  documentElement: new Element('html'),
};

/*
 * The reader. A block is a paragraph-like node: a heading, a paragraph, a list
 * item. Its runs are text with the class names and tags of every node above
 * them inside the block, which is all a terminal needs to set them. Generated
 * cue text and the verse marker's margin are preserved as visible runs. A node the
 * page hides from sight (`visually-hidden`, or `hidden`) is not read: it is
 * there for a screen reader, and a terminal reader sees what the page shows.
 */
const BLOCKS = new Set(['P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'LI', 'DT', 'DD', 'BLOCKQUOTE',
  'FIGCAPTION', 'SUMMARY', 'PRE', 'TR', 'CAPTION', 'LEGEND']);

function read(root) {
  const blocks = [];
  let current = null;
  function open(node, trail) {
    current = { tag: node.tagName.toLowerCase(), classes: trail.classes.slice(), lang: trail.lang, runs: [] };
    blocks.push(current);
  }
  function walk(node, trail) {
    if (node.nodeType === 3) {
      if (!node.nodeValue) return;
      if (!current) current = { tag: 'p', classes: trail.classes.slice(), lang: trail.lang, runs: [] }, blocks.push(current);
      current.runs.push({ text: node.nodeValue, tags: trail.tags.slice(), classes: trail.classes.slice(), lang: trail.lang });
      return;
    }
    if (node.nodeType === 1) {
      const names = node.classList.names;
      if (names.includes('visually-hidden') || node.hasAttribute('hidden')) return;
      const inner = {
        tags: trail.tags.concat(node.localName),
        classes: trail.classes.concat(names),
        lang: node.lang || trail.lang,
      };
      if (node.dataset && node.dataset.cycle) inner.classes.push('cycle-' + node.dataset.cycle);
      // The browser closes routine translation research by default. The
      // terminal's Study asks the same owner for an explicitly open disclosure.
      if (node.tagName === 'DETAILS' && names.includes('translation-apparatus') &&
          !node.hasAttribute('open')) {
        inner.classes.push('translation-apparatus-closed');
        const summary = node.children.find((child) => child.tagName === 'SUMMARY');
        if (summary) walk(summary, inner);
        current = null;
        return;
      }
      if (BLOCKS.has(node.tagName)) {
        const saved = current;
        open(node, inner);
        node.childNodes.forEach((child) => walk(child, inner));
        current = null;
        void saved;
        return;
      }
      // Ordinary cues are printed by the browser's ::before from data-cue.
      // Preserve that explicit renderer output, including its column gap;
      // otherwise every structured turn reaches the terminal without a cue.
      if (names.includes('cue-mark') && node.hasAttribute('data-cue')) {
        if (!current) open(node, inner);
        current.runs.push({ text: node.getAttribute('data-cue') + ' ',
          tags: inner.tags.slice(), classes: inner.classes.slice(), lang: inner.lang });
      }
      if (node.tagName === 'BR') {
        if (current) current.runs.push({ text: '\n', tags: inner.tags, classes: inner.classes, lang: inner.lang });
        return;
      }
      // A container that is not itself a block ends the block before it and after it.
      const container = ['SECTION', 'DIV', 'ARTICLE', 'UL', 'OL', 'DL', 'TABLE', 'TBODY', 'DETAILS', 'NAV', 'ASIDE', 'HEADER', 'FOOTER'].includes(node.tagName);
      if (container) current = null;
      node.childNodes.forEach((child) => walk(child, inner));
      // The browser sets a margin between a superscript verse number and the
      // words. A terminal has no CSS margin; keep that gap outside the numbered
      // run so a verse-per-line consumer does not see a second verse marker.
      if ((names.includes('verse-num') || names.includes('ordinary-locus')) && current) {
        const verse = names.includes('verse-num');
        current.runs.push({ text: verse ? ' ' : '  ', tags: trail.tags.slice(),
          classes: trail.classes.concat(verse ? 'verse-gap' : 'ordinary-locus-gap'), lang: inner.lang });
      }
      if (container) current = null;
      return;
    }
    if (node.nodeType === 11) node.childNodes.forEach((child) => walk(child, trail));
  }
  walk(root, { tags: [], classes: [], lang: '' });
  return blocks.filter((block) => block.runs.some((run) => run.text.trim()));
}

module.exports = { document, Element, Text, Fragment, read };
