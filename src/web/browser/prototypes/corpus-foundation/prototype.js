(() => {
  "use strict";

  const surfaces = ["reader", "catalogue", "instrument"];
  const panels = ["none", "menu", "jump", "related"];
  const params = new URLSearchParams(window.location.search);
  const requestedSurface = params.get("surface");
  const requestedPanel = params.get("panel");
  const surface = surfaces.includes(requestedSurface) ? requestedSurface : "reader";
  const panel = panels.includes(requestedPanel) ? requestedPanel : "none";
  const surfaceNodes = [...document.querySelectorAll("[data-archetype]")];
  const surfaceButtons = [...document.querySelectorAll("[data-select-surface]")];
  const currentDomain = document.querySelector("#current-domain");
  const domainBySurface = { reader: "Publications", catalogue: "Publications", instrument: "Sources" };
  const dialogInvokers = new WeakMap();

  if (surfaces.includes(requestedSurface)) document.body.classList.add("review-isolated");

  function showSurface(name, moveFocus = false) {
    surfaceNodes.forEach((node) => {
      node.hidden = node.dataset.archetype !== name;
    });
    surfaceButtons.forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.selectSurface === name));
    });
    const domain = domainBySurface[name];
    currentDomain.textContent = domain;
    document.querySelectorAll("[data-domain]").forEach((link) => {
      if (link.dataset.domain === domain) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
    if (moveFocus) {
      document.querySelector(`[data-archetype="${name}"] h2`).focus({ preventScroll: true });
    }
  }

  function closeOpenDialog(except) {
    document.querySelectorAll("dialog[open]").forEach((dialog) => {
      if (dialog !== except) dialog.close();
    });
  }

  function openDialog(id, invoker = null) {
    const dialog = document.getElementById(id);
    if (!dialog) return;
    closeOpenDialog(dialog);
    dialogInvokers.set(dialog, invoker || document.activeElement);
    if (id === "related-dialog") {
      const visibleSurface = document.querySelector("[data-archetype]:not([hidden])");
      const context = invoker?.dataset.relatedContext || visibleSurface?.dataset.archetype || "reader";
      document.querySelectorAll("[data-related-set]").forEach((set) => {
        set.hidden = set.dataset.relatedSet !== context;
      });
    }
    if (!dialog.open) dialog.showModal();
    const focusTarget = dialog.querySelector("input, button, a[href]");
    if (focusTarget) focusTarget.focus({ preventScroll: true });
  }

  surfaceButtons.forEach((button) => {
    button.addEventListener("click", () => showSurface(button.dataset.selectSurface));
  });

  document.querySelectorAll("[data-open-dialog]").forEach((button) => {
    button.addEventListener("click", () => openDialog(button.dataset.openDialog, button));
  });

  document.querySelectorAll("[data-close-dialog]").forEach((button) => {
    button.addEventListener("click", () => button.closest("dialog").close());
  });

  document.querySelectorAll("dialog").forEach((dialog) => {
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) dialog.close();
    });
    dialog.addEventListener("close", () => {
      const savedInvoker = dialogInvokers.get(dialog);
      if (savedInvoker && savedInvoker.isConnected) savedInvoker.focus({ preventScroll: true });
      dialogInvokers.delete(dialog);
    });
  });

  const jumpInput = document.querySelector("#jump-query");
  const jumpItems = [...document.querySelectorAll("#jump-results li")];
  const jumpStatus = document.querySelector("#jump-status");
  const jumpEmpty = document.querySelector("#jump-empty");
  const catalogueInput = document.querySelector("#catalogue-filter");
  const catalogueRows = [...document.querySelectorAll("[data-catalogue-terms]")];
  const catalogueCount = document.querySelector("#catalogue-count");
  const catalogueEmpty = document.querySelector("#catalogue-empty");

  jumpInput.addEventListener("input", () => {
    const query = jumpInput.value.trim().toLocaleLowerCase();
    let count = 0;
    jumpItems.forEach((item) => {
      const visible = !query || item.dataset.searchTerms.includes(query) || item.textContent.toLocaleLowerCase().includes(query);
      item.hidden = !visible;
      if (visible) count += 1;
    });
    jumpStatus.textContent = `${count} synthetic ${count === 1 ? "destination" : "destinations"}`;
    jumpEmpty.hidden = count !== 0;
  });

  function filterCatalogue() {
    const query = catalogueInput.value.trim().toLocaleLowerCase();
    let count = 0;
    catalogueRows.forEach((row) => {
      const visible = !query || row.dataset.catalogueTerms.includes(query) || row.textContent.toLocaleLowerCase().includes(query);
      row.hidden = !visible;
      if (visible) count += 1;
    });
    catalogueCount.textContent = `${count} ${count === 1 ? "work" : "works"}`;
    catalogueEmpty.hidden = count !== 0;
  }

  catalogueInput.addEventListener("input", filterCatalogue);
  document.querySelector(".catalogue-controls").addEventListener("submit", (event) => {
    event.preventDefault();
    filterCatalogue();
    document.querySelector("#catalogue-results").scrollIntoView({ block: "start" });
  });

  showSurface(surface);
  if (panel !== "none") openDialog(`${panel}-dialog`);
})();
