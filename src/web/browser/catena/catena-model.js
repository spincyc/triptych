/* ===========================================================================
 * The catena, as a model — the chapter view, derived, and derived only here
 * ===========================================================================
 *
 * THE ONE THING THIS FILE OWNS: which fragments stand under a chapter.
 *
 * `guidance/catena.md` Rule 5 stores a fragment at its natural extent — the
 * range the commentator actually addressed — and derives the chapter view.
 * Rule 6 then says a fragment whose extent crosses a chapter boundary appears
 * under every chapter it touches, once, at its full extent, and is never split
 * there, because splitting would attribute to one chapter words written about
 * another.
 *
 * Both are questions a reader asks, so both are answered here, at read time,
 * from the per-book file. NOTHING KEYED BY CHAPTER IS WRITTEN TO DISK. That is
 * not an optimisation, it is the point: a stored chapter table and a stored
 * extent are two representations of one fact, and this repository has already
 * been bitten by the pair disagreeing — `passage-commentary-index.yaml` answers
 * the same question at two granularities today and the answers differ.
 *
 * `catena check` runs THIS FILE under node against the solved cases in
 * `src/sources/commentary/fragment-loci.yaml`, exactly as `calendar-rubrics
 * check` runs the liturgy assembly model. So there is one derivation, and a
 * check that would fail if a second one were written beside it.
 *
 * It loads both as a browser global and as a node module, because the harness
 * needs the second and the page needs the first.
 * ======================================================================== */

'use strict';

(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.CatenaModel = api;
}(typeof self !== 'undefined' ? self : this, function () {

  /**
   * Does this extent touch this chapter?
   *
   * Inclusive at both ends and stated over chapters alone. A fragment on
   * Genesis 1:1-2:2 touches chapter 1 and chapter 2; one on Genesis 1:3-1:5
   * touches chapter 1 only. The verses do not enter: a fragment that reaches
   * into a chapter at all is about that chapter, and asking whether it reaches
   * "enough" of it would be a judgment no data here supports.
   */
  function touchesChapter(extent, chapter) {
    if (!extent) return false;
    const first = Number(extent.first_chapter);
    const last = Number(extent.last_chapter);
    if (!Number.isFinite(first) || !Number.isFinite(last)) return false;
    return first <= chapter && chapter <= last;
  }

  /** Every fragment standing under one chapter, in the order it was given. */
  function fragmentsOnChapter(fragments, chapter) {
    const wanted = Number(chapter);
    return (fragments || []).filter(function (fragment) {
      return touchesChapter(fragment.extent, wanted);
    });
  }

  /**
   * "Genesis 1:1-2:2", "Genesis 1:4-5", "Genesis 1:4" — the full extent, always.
   *
   * Rule 6 again, on the label this time. A fragment shown under Genesis 2 must
   * still say it runs from 1:1, or the reader is told Augustine wrote about
   * chapter 2 when he wrote across the seam.
   */
  function formatExtent(extent, bookName) {
    if (!extent) return bookName || '';
    const book = bookName || extent.token || '';
    const first = extent.first_chapter + ':' + extent.first_verse;
    if (extent.first_chapter !== extent.last_chapter) {
      return book + ' ' + first + '-' + extent.last_chapter + ':' + extent.last_verse;
    }
    if (extent.first_verse === extent.last_verse) return book + ' ' + first;
    return book + ' ' + first + '-' + extent.last_verse;
  }

  /** Does this fragment cross a chapter boundary? The page says so when it does. */
  function spansChapters(extent) {
    return !!extent && Number(extent.last_chapter) > Number(extent.first_chapter);
  }

  /**
   * A chapter file's fragments, each rejoined to what it shares with its edition.
   *
   * The spine writes the author, the work, the date, the language, the printing,
   * the translators and the rights ONCE per distinct set of them, under
   * `sources`, and gives every fragment the key of its set. Written per fragment
   * they cost more than everything else in the file put together — on Genesis 1,
   * 107 copies of ten fields — and every copy was a chance for two of them to
   * disagree about one edition.
   *
   * The join happens here and at read time, which is where `browser-core.js`
   * says joins belong. `text_path` is composed the same way, from the file's own
   * one statement of where fragment texts live, so the page never carries a
   * directory layout the generator can change underneath it.
   */
  function chapterFragments(file) {
    if (!file) return [];
    const sources = file.sources || {};
    const prefix = file.text_prefix || '';
    return (file.fragments || []).map(function (fragment) {
      const shared = sources[fragment.source] || {};
      const joined = {};
      for (const name in shared) if (Object.hasOwn(shared, name)) joined[name] = shared[name];
      for (const name in fragment) if (Object.hasOwn(fragment, name)) joined[name] = fragment[name];
      if (fragment.id) joined.text_path = prefix + fragment.id + '.json';
      return joined;
    });
  }

  /* ------------------------------------------------------------------------
   * Whose words these are — the axis the commentary control runs along
   *
   * NOT `la / grc / en`. A father may be held in his own Greek, in an ancient
   * Latin version of that Greek, and in a Victorian English of it, and those
   * are three different claims about one page of words. On a language axis the
   * middle one is invisible: it prints "Latin", indistinguishably from Ambrose
   * writing Latin himself, and a reader who asked for the original would be
   * handed a translation with nothing on the page to say so.
   *
   * So the generator derives `voice` per edition — `original` where the
   * edition is in a language the work was written in, `translation` otherwise —
   * from the work record and the edition record together, and refuses to emit a
   * fragment whose two independent signals for it disagree. This file only
   * counts what arrived.
   *
   * The key a selection carries is `original`, or `translation:` and the
   * language, because "English" and "Latin" are different offers and a reader
   * choosing between them is choosing between two translations.
   * --------------------------------------------------------------------- */

  const ORIGINAL = 'original';
  const TRANSLATION = 'translation';

  /** The selectable key for one edition's voice, or '' where it has none. */
  function voiceKey(source) {
    const voice = (source && source.voice) || '';
    if (voice === ORIGINAL) return ORIGINAL;
    if (voice === TRANSLATION) return TRANSLATION + ':' + ((source && source.language) || '');
    return '';
  }

  /**
   * Every voice this chapter actually holds, counted rather than assumed.
   *
   * Read off `sources`, which the spine writes with exactly one entry per
   * edition standing under this chapter — so an offer appears here only when
   * something is behind it, and a chapter held in one voice offers one.
   * Originals first, then translations by language, so the control reads
   * outward from the author.
   */
  function chapterVoices(file) {
    const sources = (file && file.sources) || {};
    const found = new Map();
    for (const key in sources) {
      if (!Object.hasOwn(sources, key)) continue;
      const source = sources[key];
      const wanted = voiceKey(source);
      if (!wanted || found.has(wanted)) continue;
      found.set(wanted, {
        key: wanted,
        voice: source.voice,
        // Named for a translation and deliberately blank for an original. The
        // reader asking for the author's own language is asking one question,
        // not one per language: a chapter holding Ambrose's Latin beside
        // Severian's Greek holds both authors' own words, and offering them
        // separately would put the reader back on the axis this replaced.
        language: source.voice === TRANSLATION ? source.language || '' : ''
      });
    }
    return Array.from(found.values()).sort(function (a, b) {
      if (a.voice !== b.voice) return a.voice === ORIGINAL ? -1 : 1;
      return a.language < b.language ? -1 : a.language > b.language ? 1 : 0;
    });
  }

  /**
   * A selection key read back as the voice it names.
   *
   * Composed by `voiceKey` and taken apart only here, so a page that has to
   * NAME a selection the chapter does not hold — which it must, rather than
   * silently widening — never parses the key a second way.
   */
  function parseVoiceKey(wanted) {
    const key = String(wanted || '');
    if (!key) return null;
    if (key === ORIGINAL) return { key: key, voice: ORIGINAL, language: '' };
    const cut = key.indexOf(':');
    if (cut < 0) return null;
    return {
      key: key,
      voice: key.slice(0, cut),
      language: key.slice(cut + 1)
    };
  }

  /**
   * Does this fragment answer that selection?
   *
   * An empty selection is every fragment. A fragment whose voice could not be
   * derived answers no selection at all rather than the nearest one: it is
   * refused by the generator's check before it reaches here, and if one ever
   * arrives it must not be served as though someone had established whose
   * words it carries.
   */
  function matchesVoice(fragment, wanted) {
    if (!wanted) return true;
    return voiceKey(fragment) === wanted;
  }

  return {
    touchesChapter: touchesChapter,
    fragmentsOnChapter: fragmentsOnChapter,
    chapterFragments: chapterFragments,
    formatExtent: formatExtent,
    spansChapters: spansChapters,
    chapterVoices: chapterVoices,
    matchesVoice: matchesVoice,
    voiceKey: voiceKey,
    parseVoiceKey: parseVoiceKey,
    ORIGINAL: ORIGINAL,
    TRANSLATION: TRANSLATION
  };
}));
