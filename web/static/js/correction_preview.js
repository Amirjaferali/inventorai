/* Presentation only. The server-rendered correction form owns eligibility.
 * Native disclosures keep the complete recorded text available without JS.
 */
(function () {
  "use strict";
  var select = document.getElementById("correct-target");
  if (!select || !select.form) return;
  var form = select.form;
  var preview = form.querySelector("#correction-preview");
  var status = form.querySelector("#correction-preview-status");
  if (!preview || !status) return;
  var fields = ["reference", "context", "content"];
  var outputs = fields.map(function (name) {
    return preview.querySelector("[data-preview-" + name + "]");
  });
  if (outputs.some(function (field) { return !field; })) return;

  function update(announce) {
    // Compare literal record IDs within THIS form; never interpret IDs as selectors.
    var matches = Array.from(form.querySelectorAll("[data-correction-record]"))
      .filter(function (record) {
        return record.getAttribute("data-correction-record") === select.value;
      });
    preview.hidden = true;
    status.textContent = "";
    outputs.forEach(function (field) { field.textContent = ""; });
    if (select.selectedIndex < 0 || matches.length !== 1) return;
    var inputs = fields.map(function (name) {
      return matches[0].querySelector("[data-record-" + name + "]");
    });
    if (inputs.some(function (field) { return !field; })) return;
    outputs.forEach(function (field, index) {
      field.textContent = inputs[index].textContent;
    });
    preview.hidden = false;
    if (announce) {
      status.textContent = status.getAttribute("data-message")
        .replace("{reference}", inputs[0].textContent);
    }
  }
  select.addEventListener("change", function () { update(true); });
  // Reconcile a browser-restored selection without moving focus or writing a form field.
  window.addEventListener("pageshow", function () { update(false); });
  update(false);
}());
