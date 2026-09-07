/* A1 presentation only: native form submission, no network or storage API.
 * Only a server acceptance signal may say "saved". A pending request never does.
 */
(function () {
  "use strict";
  var copy = document.getElementById("journey-submit-feedback");
  if (!copy) return;
  var resetters = [];
  document.querySelectorAll("main form[method='POST']").forEach(function (form) {
    var status = document.createElement("p");
    status.setAttribute("role", "status");
    status.setAttribute("aria-live", "polite");
    status.className = "journey-note";
    form.appendChild(status);
    var timer;
    function reset() {
      window.clearTimeout(timer);
      form.removeAttribute("aria-busy");
      status.textContent = "";
    }
    resetters.push(reset);
    form.addEventListener("submit", function (event) {
      if (event.defaultPrevented) return;
      reset();
      form.setAttribute("aria-busy", "true");
      status.textContent = copy.getAttribute("data-sending");
      timer = window.setTimeout(function () {
        status.textContent = copy.getAttribute("data-waiting");
      }, 15000);
      // Do not disable a submitter or change its name/value, intercept submission,
      // retry automatically, clear text, or claim persistence from elapsed time.
    });
  });
  window.addEventListener("pageshow", function () {
    resetters.forEach(function (reset) { reset(); });
  });
  document.querySelectorAll("a[data-primary-action][href^='#']").forEach(function (link) {
    link.addEventListener("click", function () {
      var target = document.getElementById(link.getAttribute("href").slice(1));
      if (!target) return;
      if (target.tagName === "DETAILS") {
        target.open = true;
        target.querySelector("summary").focus();
      } else {
        target.focus();
      }
    });
  });
}());
