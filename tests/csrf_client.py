"""Explicit CSRF-aware client for existing feature journeys.

The production guard is never disabled. These callers test other behavior and
submit the browser session's current token, as their rendered forms do. Security
tests use a raw Flask client, or csrf=False for deliberately missing evidence.
Explicit token values (including empty, forged and duplicate values) are retained.

UQTR-01 Step 2B (answer-form binding). A rendered answer form on
``/session/<sid>`` carries the current answer token AND a signed
``answer_target`` bound to that token. For posts to exactly that route this
client supplies what the rendered form would, and nothing more:

* ``answer_target`` is added only when absent, and only for the token the live
  entry currently holds (minted by the app's own render functions for the
  current form context) — or, for a token that is no longer current, the exact
  target this client already sent with that token (the same retained browser
  form resubmitted). A forged, foreign or never-rendered token gets no target.
* ``answer_token`` is added only for the five non-answer actions, which never
  carried one before this binding; an answered post without a token keeps its
  deliberate absence.

Stale-form, swap and tamper tests pass ``answer_binding=False`` (or explicit
values) and parse the real rendered forms.
"""
import re

from flask.testing import FlaskClient
from werkzeug.datastructures import MultiDict

_ANSWER_ROUTE = re.compile(r"^/session/([^/?#]+)/?$")
_NON_ANSWER_ACTIONS = frozenset({
    "unknown", "deferred", "provisional_assumption", "specialist_requested",
    "evidence_requested"})


class CSRFClient(FlaskClient):
    def open(self, *args, csrf=True, answer_binding=True, **kwargs):
        method = kwargs.get("method", "GET").upper()
        if csrf and method not in ("GET", "HEAD", "OPTIONS"):
            data = kwargs.get("data")
            if "json" not in kwargs and (data is None or isinstance(data, (dict, MultiDict))):
                data = MultiDict(data or {})
                if "csrf_token" not in data:
                    with self.session_transaction() as session:
                        auth = session.get("auth")
                        token = auth.get("csrf") if isinstance(auth, dict) else session.get("csrf")
                    if not token:
                        # A real form GET obtains anonymous evidence. Existing
                        # authenticated tokens need no extra GET/session touch,
                        # especially during storage-failure injection.
                        super().open("/", method="GET")
                        with self.session_transaction() as session:
                            auth = session.get("auth")
                            token = auth.get("csrf") if isinstance(auth, dict) else session.get("csrf")
                    if token:
                        data["csrf_token"] = token
                kwargs["data"] = data
        if answer_binding and method == "POST" and args and isinstance(args[0], str):
            match = _ANSWER_ROUTE.match(args[0])
            data = kwargs.get("data")
            if match and "json" not in kwargs and (
                    data is None or isinstance(data, (dict, MultiDict))):
                data = MultiDict(data or {})
                self._bind_answer_form(match.group(1), data)
                kwargs["data"] = data
        return super().open(*args, **kwargs)

    def _bind_answer_form(self, sid, data):
        if "criticality_action" in data or "answer_target" in data:
            return
        import web.app as webapp
        entry = webapp.SESSION_STORE.get(sid)
        action = (data.get("action") or "answered").strip().lower()
        if "answer_token" not in data:
            if action not in _NON_ANSWER_ACTIONS or entry is None:
                return
            data["answer_token"] = webapp._answer_token_for(sid, entry)
        token = data.get("answer_token")
        sent = self.__dict__.setdefault("_uqtr_sent_targets", {})
        if entry is not None and token and token == entry.get("answer_token"):
            state = entry["state"]
            target = webapp._issue_answer_target(
                sid, token, webapp._answer_target_from(
                    webapp._resolve_question_context(
                        state, entry.get("last_result")),
                    state, bool(entry.get("criticality_correction"))))
            sent[(sid, token)] = target
        else:
            target = sent.get((sid, token))
        if target:
            data["answer_target"] = target


def csrf_client(app, **kwargs):
    return CSRFClient(app, app.response_class, **kwargs)
