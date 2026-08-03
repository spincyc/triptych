/* Factual placement notes for Proper events already seated in the Ordinary. */

'use strict';

(function (root) {
  function facts(event) {
    const seat = event && event.seat;
    if (!event || event.kind !== 'proper' || event.placement !== 'seated' || !seat) {
      return null;
    }
    if ((seat.where !== 'before' && seat.where !== 'after') ||
        typeof seat.locus !== 'string' || !seat.locus.trim()) {
      return null;
    }

    const locus = seat.locus.trim();
    return {
      where: seat.where,
      locus: locus,
      text: 'Within the Ordinary, this Proper is seated ' + seat.where +
        ' its declared anchor. Seat citation: ' + locus + '.'
    };
  }

  function setOpen(button, note, properName, open) {
    note.hidden = !open;
    button.setAttribute('aria-expanded', open ? 'true' : 'false');
    button.setAttribute('aria-label',
      (open ? 'Hide' : 'Show') + ' placement note for ' + properName);
  }

  function add(options) {
    const held = options || {};
    const body = held.body;
    const event = held.event;
    const noteId = held.noteId;
    const supported = facts(event);
    if (!body || !supported || typeof noteId !== 'string' || !noteId) return null;

    const heading = body.querySelector('.proper-name');
    if (!heading || heading.querySelector('.proper-placement-toggle')) return null;

    const doc = body.ownerDocument || document;
    const properName = event.proper && event.proper.name
      ? event.proper.name : 'Proper';
    const button = doc.createElement('button');
    button.type = 'button';
    button.className = 'proper-placement-toggle';
    button.setAttribute('aria-controls', noteId);

    const note = doc.createElement('span');
    note.id = noteId;
    note.className = 'proper-placement-note';
    note.textContent = supported.text;
    note.hidden = true;
    note.setAttribute('role', 'note');

    setOpen(button, note, properName, false);
    button.addEventListener('click', () => {
      setOpen(
        button,
        note,
        properName,
        button.getAttribute('aria-expanded') !== 'true'
      );
    });
    button.addEventListener('keydown', (keyEvent) => {
      if (keyEvent.key !== 'Escape' || button.getAttribute('aria-expanded') !== 'true') {
        return;
      }
      keyEvent.preventDefault();
      setOpen(button, note, properName, false);
      button.focus({ preventScroll: true });
    });

    const subordinate = heading.querySelector('.proper-form, .proper-ref');
    heading.insertBefore(button, subordinate);
    body.insertBefore(note, heading.nextSibling);
    return { button: button, note: note, facts: supported };
  }

  root.ProperPlacementNotes = Object.freeze({ add: add, facts: facts });
}(window));
