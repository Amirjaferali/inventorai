/* G1-PCC-LITERAL-SOURCE-AID-01. Presentation only: after the inventor has
 * chosen the board component in the form AND an explicit X / Y assignment, it
 * fills EMPTY board fields of the planar-clearance form. It never selects a
 * component, never answers a declaration, never overwrites a value, an
 * "I do not know yet" box or a note, and never submits anything.
 *
 * The note it places is a PROPOSAL of the inventor's own documentary text. If
 * the board, a board value or the X / Y choice changes afterwards, that note is
 * removed only while it is still exactly the text the aid placed; a note the
 * inventor has edited from it is theirs and is never erased: they get a
 * non-blocking reminder to review it instead. Nothing here verifies a note.
 */
(function () {
  "use strict";
  var box = document.querySelector("[data-pcc-aid]");
  var form = document.querySelector("[data-pcc-form]");
  if (!box || !form) return;
  var controls = box.querySelector("[data-pcc-aid-controls]");
  var apply = box.querySelector("[data-pcc-aid-apply]");
  var status = box.querySelector("[data-pcc-aid-status]");
  var board = form.querySelector("#pcc-board");
  var x = form.querySelector("#pcc-v-board_x");
  var y = form.querySelector("#pcc-v-board_y");
  var ux = form.querySelector('input[name="unknown_board_x"]');
  var uy = form.querySelector('input[name="unknown_board_y"]');
  var note = form.querySelector("#pcc-basis_board");
  var orders = box.querySelectorAll('input[name="pcc_aid_order"]');
  if (!controls || !apply || !status || !board || !x || !y || !ux || !uy || !note) return;
  controls.hidden = false;
  var placed = null;    // the exact note text the aid placed, while it is unedited
  var derived = false;  // the inventor has edited the note the aid placed

  function say(name) {
    status.textContent = status.getAttribute("data-msg-" + name);
  }

  function withdrawPlacedNote() {
    if (placed !== null && note.value === placed) {
      note.value = "";
      say("cleared");
    } else if (derived && note.value !== "") {
      say("review");
    }
    placed = null;
    derived = false;
  }

  apply.addEventListener("click", function () {
    if (board.value === "") {
      say("board");
      return;
    }
    var chosen = box.querySelector('input[name="pcc_aid_order"]:checked');
    if (!chosen) {
      say("choose");
      return;
    }
    if (x.value !== "" || y.value !== "" || ux.checked || uy.checked || note.value !== "") {
      say("occupied");
      return;
    }
    x.value = chosen.getAttribute("data-x");
    y.value = chosen.getAttribute("data-y");
    note.value = chosen.getAttribute("data-note");
    placed = note.value;
    derived = false;
    say("done");
  });
  board.addEventListener("change", withdrawPlacedNote);
  [x, y, ux, uy].forEach(function (field) {
    field.addEventListener("input", withdrawPlacedNote);
    field.addEventListener("change", withdrawPlacedNote);
  });
  Array.prototype.forEach.call(orders, function (radio) {
    radio.addEventListener("change", withdrawPlacedNote);
  });
  note.addEventListener("input", function () {
    if (placed !== null && note.value !== placed) {
      placed = null;          // edited: now the inventor's own text, never erased
      derived = true;
    }
  });
}());
