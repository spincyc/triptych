/* Enhance the generated dictionary table; native details and image links are
   the complete fallback. This script owns no object, image, or source data. */
(() => {
  "use strict";

  function enhanceDictionary() {
    const table = document.querySelector(".sanctuary-table");
    if (!table || table.dataset.enhanced) return;
    const region = table.closest(".dictionary-table-region");
    const body = table.tBodies[0];
    if (!region || !body) return;

    const pairs = Array.from(body.querySelectorAll(".dictionary-row")).map(row => {
      const detailRow = row.nextElementSibling;
      const details = detailRow?.querySelector("details.dictionary-details");
      if (!detailRow?.matches(".dictionary-detail-row") || !details) return null;
      return {
        row, detailRow, details,
        figures: Array.from(details.querySelectorAll("figure[id]")),
        images: Array.from(row.querySelectorAll(".dictionary-image-toggle")),
        toggle: row.querySelector(".dictionary-row-toggle"),
        image: null,
        opener: null
      };
    });
    // Do not partially enhance malformed pairs: their native controls still work.
    if (!pairs.length || pairs.some(pair => !pair || !pair.toggle)) return;

    const search = document.querySelector("[data-dictionary-search]");
    const group = document.querySelector("[data-dictionary-group]");
    const toolbar = document.querySelector(".dictionary-toolbar");
    const count = document.getElementById("dictionary-result-count");
    const empty = body.querySelector(".dictionary-empty");
    const sortButtons = Array.from(table.querySelectorAll("[data-dictionary-sort]"));
    const scrollHint = document.querySelector(".dictionary-scroll-hint");
    const collator = new Intl.Collator("en", { sensitivity: "base", numeric: true });
    const normalize = value => value.normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "").toLocaleLowerCase("en").trim();
    let active = null;

    function sync(pair) {
      const open = pair.details.open && !pair.row.hidden;
      pair.detailRow.hidden = !open;
      pair.row.classList.toggle("is-expanded", open);
      pair.toggle.setAttribute("aria-expanded", String(open));
      for (const image of pair.images) {
        const selected = open && (!pair.image || pair.image === image.dataset.image);
        image.setAttribute("aria-expanded", String(selected));
      }
      for (const figure of pair.figures) {
        figure.hidden = open && Boolean(pair.image) && figure.id !== pair.image;
      }
    }

    function close(pair, restoreFocus = false) {
      if (!pair) return;
      pair.details.open = false;
      pair.image = null;
      if (active === pair) active = null;
      sync(pair);
      if (restoreFocus && !pair.row.hidden) {
        const opener = pair.opener || pair.toggle;
        opener.focus({ preventScroll: true });
        opener.scrollIntoView({ block: "nearest", inline: "nearest" });
      }
    }

    function open(pair, image = null, opener = null) {
      // Keep the clicked row in place when an earlier, tall panel collapses.
      const before = opener?.getBoundingClientRect().top;
      if (active && active !== pair) close(active);
      pair.image = pair.figures.some(figure => figure.id === image) ? image : null;
      pair.opener = opener || pair.toggle;
      pair.details.open = true;
      active = pair;
      sync(pair);
      if (opener && before !== undefined) {
        window.scrollBy(0, opener.getBoundingClientRect().top - before);
      }
    }

    function filter() {
      const words = normalize(search?.value || "").split(/\s+/).filter(Boolean);
      const selectedGroup = group?.value || "";
      let visible = 0;
      for (const pair of pairs) {
        const matchesGroup = !selectedGroup || selectedGroup === "all" ||
          pair.row.dataset.group === selectedGroup;
        const text = normalize(pair.row.dataset.search || pair.row.textContent);
        const show = matchesGroup && words.every(word => text.includes(word));
        if (!show && pair.details.open) close(pair);
        pair.row.hidden = !show;
        sync(pair);
        if (show) visible += 1;
      }
      if (count) count.textContent = `${visible} of ${pairs.length} entries`;
      if (empty) empty.hidden = visible !== 0;
    }

    function sort(key) {
      const rank = (pair, field) => Number(pair.row.dataset[field]) || 0;
      const byGroup = (a, b) => rank(a, "groupOrder") - rank(b, "groupOrder") ||
        rank(a, "objectOrder") - rank(b, "objectOrder");
      const byName = (a, b) => collator.compare(a.row.dataset.name, b.row.dataset.name);
      const ordered = pairs.slice().sort((a, b) => key === "name"
        ? byName(a, b) || byGroup(a, b)
        : byGroup(a, b) || byName(a, b));
      const fragment = document.createDocumentFragment();
      for (const pair of ordered) fragment.append(pair.row, pair.detailRow);
      if (empty) fragment.append(empty);
      body.append(fragment);
      for (const button of sortButtons) {
        button.closest("th").setAttribute("aria-sort",
          button.dataset.dictionarySort === key ? "ascending" : "none");
      }
    }

    function revealHash() {
      let id;
      try { id = decodeURIComponent(window.location.hash.slice(1)); }
      catch { return; }
      if (!id) return;
      const target = document.getElementById(id);
      if (!target) return;
      const pair = pairs.find(item => item.row.contains(target) || item.detailRow.contains(target));
      if (!pair) return;
      // A cited object takes precedence over a temporary filter.
      if (pair.row.hidden) {
        if (search) search.value = "";
        if (group) group.selectedIndex = 0;
        filter();
      }
      const figure = target.closest("figure[id]");
      open(pair, figure?.id || null);
      requestAnimationFrame(() => {
        target.scrollIntoView({ block: "start", inline: "nearest" });
      });
    }

    for (const pair of pairs) {
      for (const control of [pair.toggle, ...pair.images]) {
        control.setAttribute("role", "button");
        control.setAttribute("aria-controls", pair.detailRow.id);
        control.setAttribute("aria-expanded", "false");
        control.addEventListener("keydown", event => {
          if (event.key === " ") event.preventDefault();
        });
        control.addEventListener("keyup", event => {
          if (event.key === " ") {
            event.preventDefault();
            control.click();
          }
        });
        control.addEventListener("click", event => {
          // Preserve the image URL for new-tab, download and modified clicks.
          if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
          event.preventDefault();
          const image = control.dataset.image || null;
          if (pair.details.open && pair.image === image) close(pair, true);
          else open(pair, image, control);
        });
      }
      pair.details.addEventListener("toggle", () => {
        if (pair.details.open) {
          if (active !== pair) open(pair);
          else sync(pair);
        } else {
          close(pair, pair.detailRow.contains(document.activeElement));
        }
      });
      close(pair);
    }

    search?.addEventListener("input", filter);
    group?.addEventListener("change", filter);
    document.querySelector("[data-dictionary-reset]")?.addEventListener("click", () => {
      if (search) search.value = "";
      if (group) group.selectedIndex = 0;
      filter();
      search?.focus({ preventScroll: true });
    });
    for (const button of sortButtons) {
      button.disabled = false;
      button.addEventListener("click", () => sort(button.dataset.dictionarySort));
    }
    document.addEventListener("keydown", event => {
      if (event.key === "Escape" && active && !event.defaultPrevented) {
        event.preventDefault();
        close(active, true);
      }
    });
    window.addEventListener("hashchange", revealHash);
    // Following the same fragment twice does not fire hashchange.
    document.addEventListener("click", event => {
      const link = event.target.closest("a[href]");
      if (event.defaultPrevented || !link || event.button !== 0 ||
          event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      const url = new URL(link.href, window.location.href);
      if (url.origin === location.origin && url.pathname === location.pathname &&
          url.search === location.search && url.hash && url.hash === location.hash) {
        requestAnimationFrame(revealHash);
      }
    });

    function measureRegion() {
      region.style.setProperty("--dictionary-visible-width", `${Math.max(0, region.clientWidth - 2)}px`);
      if (scrollHint) scrollHint.hidden = region.scrollWidth <= region.clientWidth + 1;
    }
    if (typeof ResizeObserver !== "undefined") new ResizeObserver(measureRegion).observe(region);
    else window.addEventListener("resize", measureRegion);
    table.dataset.enhanced = "true";
    if (toolbar) toolbar.hidden = false;
    sort("group");
    filter();
    measureRegion();
    revealHash();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enhanceDictionary, { once: true });
  } else enhanceDictionary();
})();
