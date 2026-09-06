"""Explicit CSRF-aware client for existing feature journeys.

The production guard is never disabled. These callers test other behavior and
submit the browser session's current token, as their rendered forms do. Security
tests use a raw Flask client, or csrf=False for deliberately missing evidence.
Explicit token values (including empty, forged and duplicate values) are retained.
"""
from flask.testing import FlaskClient
from werkzeug.datastructures import MultiDict


class CSRFClient(FlaskClient):
    def open(self, *args, csrf=True, **kwargs):
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
        return super().open(*args, **kwargs)


def csrf_client(app, **kwargs):
    return CSRFClient(app, app.response_class, **kwargs)
