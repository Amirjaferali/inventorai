/* G1-PCC-LITERAL-SOURCE-AID-01. Presentation only: it fills EMPTY fields of the
 * planar-clearance form after the inventor explicitly picks an assignment. It
 * never selects a component, never answers a declaration, never overwrites a
 * value, an "I do not know yet" box or a note, and never submits anything. The
 * server re-checks every saved value and note.
 */
(function () {
  "use strict";
  var box = document.querySelector("[data-pcc-aid]");
  var form = document.querySelector("[data-pcc-form]");
  if (!box || !form) return;
  var controls = box.querySelector("[data-pcc-aid-controls]");
  var apply = box.querySelector("[data-pcc-aid-apply]");
  var status = box.querySelector("[data-pcc-aid-status]");
  var x = form.querySelector("#pcc-v-board_x");
  var y = form.querySelector("#pcc-v-board_y");
  var ux = form.querySelector('input[name="unknown_board_x"]');
  var uy = form.querySelector('input[name="unknown_board_y"]');
  var note = form.querySelector("#pcc-basis_board");
  if (!controls || !apply || !status || !x || !y || !ux || !uy || !note) return;
  controls.hidden = false;

  apply.addEventListener("click", function () {
    var chosen = box.querySelector('input[name="pcc_aid_order"]:checked');
    if (!chosen) {
      status.textContent = status.getAttribute("data-msg-choose");
      return;
    }
    if (x.value !== "" || y.value !== "" || ux.checked || uy.checked || note.value !== "") {
      status.textContent = status.getAttribute("data-msg-occupied");
      return;
    }
    x.value = chosen.getAttribute("data-x");
    y.value = chosen.getAttribute("data-y");
    note.value = chosen.getAttribute("data-note");
    status.textContent = status.getAttribute("data-msg-done");
  });
}());
