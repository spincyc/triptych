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

  return {
    touchesChapter: touchesChapter,
    fragmentsOnChapter: fragmentsOnChapter,
    formatExtent: formatExtent,
    spansChapters: spansChapters
  };
}));
