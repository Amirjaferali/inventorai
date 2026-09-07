/* Filter only the already-authorized, displayed project cards. No data service. */
(function () {
  "use strict";

  var controls = document.getElementById("project-filter");
  var list = document.getElementById("project-list");
  if (!controls || !list) return;

  var query = document.getElementById("project-filter-query");
  var domain = document.getElementById("project-filter-domain");
  var clear = document.getElementById("project-filter-clear");
  var results = document.getElementById("project-filter-results");
  var noMatch = document.getElementById("project-filter-no-match");
  if (!query || !domain || !clear || !results || !noMatch) return;

  var cards = Array.from(list.querySelectorAll(".project-card")).map(function (card) {
    var description = card.querySelector("[data-project-description]");
    var id = card.querySelector("[data-project-id]");
    var label = card.querySelector("[data-project-domain]");
    return {
      element: card,
      description: description ? description.textContent.toLowerCase() : "",
      id: id ? id.textContent.toLowerCase() : "",
      domain: label ? label.textContent.trim() : ""
    };
  });

  // Preserve the existing list order; options are the visible labels, not new metadata.
  var labels = new Set();
  cards.forEach(function (card) {
    if (card.domain && !labels.has(card.domain)) {
      labels.add(card.domain);
      var option = document.createElement("option");
      option.value = card.domain;
      option.textContent = card.domain;
      domain.appendChild(option);
    }
  });

  function applyFilters() {
    var needle = query.value.trim().toLowerCase();
    var shown = 0;
    cards.forEach(function (card) {
      var matches = (!domain.value || card.domain === domain.value) &&
        (!needle || card.description.includes(needle) || card.id.includes(needle));
      card.element.hidden = !matches;
      if (matches) shown += 1;
    });
    var count = results.dataset.countTemplate
      .replace("{shown}", String(shown)).replace("{total}", String(cards.length));
    if (results.textContent !== count) results.textContent = count;
    noMatch.hidden = shown !== 0;
  }

  query.addEventListener("input", applyFilters);
  domain.addEventListener("change", applyFilters);
  clear.addEventListener("click", function () {
    query.value = "";
    domain.value = "";
    applyFilters();
    query.focus();
  });
  window.addEventListener("pageshow", applyFilters);
  applyFilters();
  // Progressive enhancement: without this script the complete list remains usable.
  controls.hidden = false;
}());
