/* InventorAI — Draft Level 2: Same-Device Unsubmitted-Text Recovery (Local Draft Recovery).
 *
 * Governed by G-DRAFT-L2-LOCAL-CONTINUITY-CONTRACT-01 (merged PR #371) and
 * implemented under G-DRAFT-L2-LOCAL-CONTINUITY-IMPLEMENTATION-01.
 *
 * A single, first-party, framework-free script. It stores a LITERAL LOCAL COPY of
 * text the user typed, in this browser's localStorage only, so the user can
 * EXPLICITLY recover unfinished text on the SAME browser/device after refresh,
 * tab/browser closure, crash, power/battery loss, temporary offline, or an
 * intentional pause. It is local-only, same-device, explicit-recovery.
 *
 * It NEVER: submits or accepts an answer; creates an AssertionRecord; runs
 * deterministic evaluation; closes a gap; changes maturity/gaps/outputs; advances
 * progression; creates a session; claims ownership; claims server/account/other-
 * device/permanent persistence; sends any network request to save a draft;
 * silently overwrites newer visible text; or inserts untrusted HTML.
 *
 * Fail-closed: any storage error leaves the app fully usable at truthful Level 0
 * and never blocks normal form submission. With JavaScript disabled, none of this
 * runs and the server-rendered forms behave exactly as before (Level 0).
 */
(function () {
  "use strict";

  var KEY_PREFIX = "inventorai:draft:v1:";
  var SCHEMA = 1;
  var TTL_MS = 7 * 24 * 60 * 60 * 1000; // 7 days (contract-fixed for this increment)
  // Bounded per-draft size cap, measured in CHARACTERS of the serialized record
  // (String.length = UTF-16 code units, NOT bytes) — a generous local limit that
  // prevents an unbounded write; oversized input is not stored (truthful fail).
  var MAX_DRAFT_CHARS = 64 * 1024;
  var DEBOUNCE_MS = 800;

  // Bilingual, truthful strings. Never claim account/server/other-device/permanent.
  var STR = {
    savedLocal: { en: "Draft saved on this device", ar: "تم حفظ المسودة على هذا الجهاز" },
    saving: { en: "Saving locally…", ar: "جارٍ الحفظ محليًا…" },
    saveFail: { en: "Could not save a draft on this device", ar: "تعذّر حفظ مسودة على هذا الجهاز" },
    found: { en: "Unsent text was found on this device.", ar: "تم العثور على نص غير مرسل محفوظ على هذا الجهاز." },
    restore: { en: "Restore", ar: "استعادة" },
    discard: { en: "Discard", ar: "حذف" },
    restored: { en: "Draft restored", ar: "تمت استعادة المسودة" },
    discarded: { en: "Draft discarded", ar: "تم حذف المسودة" },
    newerElsewhere: {
      en: "A newer draft was saved in another tab on this device.",
      ar: "تم حفظ مسودة أحدث في علامة تبويب أخرى على هذا الجهاز."
    }
  };

  function lang() {
    var l = (document.documentElement.getAttribute("lang") || "en").toLowerCase();
    return l.indexOf("ar") === 0 ? "ar" : "en";
  }
  function t(entry) { return entry[lang()] || entry.en; }

  // --- storage helpers (all fail-closed; never throw to callers) -------------
  function hasStorage() {
    try {
      var k = "__inventorai_probe__";
      window.localStorage.setItem(k, "1");
      window.localStorage.removeItem(k);
      return true;
    } catch (e) { return false; }
  }
  function keyFor(el) {
    return KEY_PREFIX +
      (el.getAttribute("data-draft-scope") || "") + ":" +
      (el.getAttribute("data-draft-field") || "") + ":" +
      (el.getAttribute("data-draft-context") || "") + ":" +
      (el.getAttribute("data-draft-context-version") || "");
  }
  function readDraft(key, el) {
    var raw;
    try { raw = window.localStorage.getItem(key); } catch (e) { return null; }
    if (!raw) return null;
    var obj;
    try { obj = JSON.parse(raw); } catch (e) { safeRemove(key); return null; } // corrupted -> ignore + purge
    if (!obj || obj.v !== SCHEMA || typeof obj.text !== "string" ||
        typeof obj.ts !== "number") { safeRemove(key); return null; }
    if ((Date.now() - obj.ts) > TTL_MS) { safeRemove(key); return null; }   // expired -> ignore + purge
    // Defence in depth: stored context must match the current surface context.
    if (obj.scope !== el.getAttribute("data-draft-scope") ||
        obj.field !== el.getAttribute("data-draft-field") ||
        obj.context !== el.getAttribute("data-draft-context") ||
        obj.ctxver !== el.getAttribute("data-draft-context-version")) {
      return null;   // mismatched project/field/question/version -> never restore
    }
    return obj;
  }
  function writeDraft(key, el, text) {
    var payload = {
      v: SCHEMA, text: text, ts: Date.now(),
      scope: el.getAttribute("data-draft-scope"),
      field: el.getAttribute("data-draft-field"),
      context: el.getAttribute("data-draft-context"),
      ctxver: el.getAttribute("data-draft-context-version")
    };
    var s = JSON.stringify(payload);
    if (s.length > MAX_DRAFT_CHARS) return false; // oversized -> not stored (truthful fail)
    try { window.localStorage.setItem(key, s); return true; } catch (e) { return false; }
  }
  function safeRemove(key) { try { window.localStorage.removeItem(key); } catch (e) {} }

  // Remove every draft of a given field for a scope (used on confirmed accept).
  function removeFieldDrafts(scope, field) {
    try {
      var pfx = KEY_PREFIX + scope + ":" + field + ":";
      var doomed = [];
      for (var i = 0; i < window.localStorage.length; i++) {
        var k = window.localStorage.key(i);
        if (k && k.indexOf(pfx) === 0) doomed.push(k);
      }
      doomed.forEach(safeRemove);
    } catch (e) {}
  }

  // --- status region (aria-live polite; textContent only) --------------------
  function statusEl(el) {
    var id = "draft-status-" + (el.id || el.getAttribute("data-draft-field") || "x");
    var s = document.getElementById(id);
    if (!s) {
      s = document.createElement("span");
      s.id = id;
      s.className = "draft-status";
      s.setAttribute("aria-live", "polite");
      s.setAttribute("role", "status");
      s.style.cssText = "display:block;font-size:12px;color:#557;margin-top:4px;min-height:1em";
      el.parentNode.insertBefore(s, el.nextSibling);
    }
    return s;
  }
  function setStatus(el, msg) { statusEl(el).textContent = msg; }

  // --- explicit, non-silent recovery prompt (no innerHTML) -------------------
  function offerRecovery(el, key, draft) {
    if (document.getElementById("draft-recovery-" + (el.id || key))) return;
    var box = document.createElement("div");
    box.id = "draft-recovery-" + (el.id || key);
    box.className = "draft-recovery";
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", t(STR.found));
    box.style.cssText = "background:#fff8e1;border:1px solid #e6d28a;border-radius:4px;" +
      "padding:8px 12px;margin:6px 0;font-size:13px;color:#5b4a12";
    var msg = document.createElement("span");
    msg.textContent = t(STR.found) + " ";
    var restore = document.createElement("button");
    restore.type = "button";
    restore.className = "draft-restore";
    restore.textContent = t(STR.restore);
    restore.style.cssText = "margin:0 6px;padding:3px 10px;cursor:pointer";
    var discard = document.createElement("button");
    discard.type = "button";
    discard.className = "draft-discard";
    discard.textContent = t(STR.discard);
    discard.style.cssText = "margin:0;padding:3px 10px;cursor:pointer";
    restore.addEventListener("click", function () {
      el.value = draft.text;           // value API only; never innerHTML
      el.focus();
      setStatus(el, t(STR.restored));
      box.parentNode.removeChild(box); // keep the draft until submit/discard
    });
    discard.addEventListener("click", function () {
      safeRemove(key);
      setStatus(el, t(STR.discarded));
      box.parentNode.removeChild(box);
      el.focus();
    });
    box.appendChild(msg);
    box.appendChild(restore);
    box.appendChild(discard);
    el.parentNode.insertBefore(box, el);
  }

  // --- low-emphasis cross-tab awareness notice (no overwrite, no delete) ------
  function showAwareness(el) {
    var id = "draft-awareness-" + (el.id || el.getAttribute("data-draft-field") || "x");
    if (document.getElementById(id)) return;
    var note = document.createElement("div");
    note.id = id;
    note.className = "draft-awareness";
    note.setAttribute("role", "status");
    note.setAttribute("aria-live", "polite");
    note.style.cssText = "background:#eef3fb;border:1px solid #cdd8ea;border-radius:4px;" +
      "padding:6px 10px;margin:6px 0;font-size:12px;color:#3a4a63";
    note.textContent = t(STR.newerElsewhere);
    el.parentNode.insertBefore(note, el);
  }

  // --- per-field wiring -------------------------------------------------------
  function wire(el) {
    var key = keyFor(el);

    // Recovery: offer ONLY when the field is empty (or only whitespace) so newer
    // visible text is never silently overwritten.
    var draft = readDraft(key, el);
    if (draft && draft.text && !(el.value || "").trim()) {
      offerRecovery(el, key, draft);
    }

    var timer = null;
    var userEdited = false; // whether the user actually typed in THIS tab

    // Save is used by the interruption flush (pagehide / tab hidden) and the
    // debounced input path. It only WRITES non-empty text — it NEVER deletes a
    // stored draft merely because the visible field is empty (B2/B3): an
    // untouched empty field or an empty sibling tab must not remove a draft.
    function save() {
      var val = el.value != null ? el.value : "";
      if (!val.trim()) return;                            // never delete on empty
      var ok = writeDraft(key, el, val);
      setStatus(el, ok ? t(STR.savedLocal) : t(STR.saveFail));
    }

    el.addEventListener("input", function () {
      userEdited = true;
      var val = el.value != null ? el.value : "";
      if (timer) window.clearTimeout(timer);
      if (!val.trim()) {
        // The user intentionally cleared the field IN THIS TAB after editing it:
        // remove only THIS field's matching draft (never an unrelated draft).
        safeRemove(key);
        setStatus(el, "");
        return;
      }
      setStatus(el, t(STR.saving));
      timer = window.setTimeout(save, DEBOUNCE_MS);
    });

    // Interruption flush (pagehide / tab hidden). beforeunload is intentionally
    // NOT the primary path. Flush only SAVES (never deletes).
    window.addEventListener("pagehide", save);
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "hidden") save();
    });

    // Cross-tab storage events (another tab wrote/removed this key). Never
    // overwrite visible text and never delete the stored draft here.
    window.addEventListener("storage", function (ev) {
      if (ev.key !== key) return;
      if (ev.newValue == null) return;                   // another tab removed it; leave our view alone
      if ((el.value || "").trim()) {
        showAwareness(el);                               // non-empty field -> low-emphasis notice only
      } else if (!document.getElementById("draft-recovery-" + (el.id || key))) {
        var d2 = readDraft(key, el);
        if (d2 && d2.text) offerRecovery(el, key, d2);   // empty field -> offer the newer draft
      }
    });
  }

  function init() {
    if (!hasStorage()) return; // fail closed to Level 0; forms remain fully usable

    // Confirmed-acceptance cleanup signals (server-provided, truthful, one-shot).
    // These fire ONLY on the render immediately after a successful acceptance —
    // NOT on a generic session render, a bookmark, a history entry, or another
    // tab — so an unrelated unsent draft is never deleted (B1).
    var sig = document.getElementById("draft-signals");
    if (sig) {
      var scope = sig.getAttribute("data-draft-scope") || "";
      // Seed idea accepted by THIS start (one-shot) -> clear the matching seed draft.
      if (sig.getAttribute("data-seed-accepted") === "1") {
        removeFieldDrafts("__seed__", "idea");
      }
      // Answer accepted on THIS session (one-shot) -> clear its answer/correction drafts.
      if (sig.getAttribute("data-answer-accepted") === "1" && scope) {
        removeFieldDrafts(scope, "answer");
        removeFieldDrafts(scope, "correction");
      }
    }

    var fields = document.querySelectorAll("textarea[data-draft-field]");
    for (var i = 0; i < fields.length; i++) wire(fields[i]);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
