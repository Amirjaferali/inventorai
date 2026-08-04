"""P4-1b-1 correction (G-P4-1B-1-AMEND-01, finding B2) — governed pytest DB isolation.

An autouse fixture points every governed test that can reach the P4-1b-1 runtime
store at a UNIQUE, pytest-managed on-disk SQLite file, so no governed test ever
writes to the shared local-development database
(`<tempdir>/inventorai_dev/inventorai_p4_1b1.sqlite`). Before and after each test
it safely closes and resets the one application-scoped store and clears
`SESSION_STORE`; the environment change is reverted by pytest's `monkeypatch`.

Bounded and honest: it introduces no production behaviour; does not globally
mock or fake the store; uses a real on-disk file (never `:memory:`); uses only
the public `store.close()`; weakens no assertion; and is order-independent.
Focused restart/durability tests continue to use a real file-backed SQLite
database under this pytest-managed temporary path.
"""
import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def _session_isolated_inventorai_db(tmp_path_factory):
    """Session-wide safety net (B2): set INVENTORAI_DB_PATH before ANY session- or
    module-scoped fixture runs, so broader-scoped fixtures that reach the runtime
    store (e.g. module-scoped `/start` fixtures set up before a function fixture)
    can never touch the shared local-development database. The per-test fixture
    below overrides this with a unique per-test path. Uses `os.environ` directly
    because a session-scoped fixture cannot use the function-scoped `monkeypatch`;
    the original value is restored on teardown."""
    path = tmp_path_factory.mktemp("inventorai_session_db") / "session_p4_1b1.sqlite"
    previous = os.environ.get("INVENTORAI_DB_PATH")
    os.environ["INVENTORAI_DB_PATH"] = str(path)
    yield
    if previous is None:
        os.environ.pop("INVENTORAI_DB_PATH", None)
    else:
        os.environ["INVENTORAI_DB_PATH"] = previous


def _close_and_reset_store():
    """Safely close the app-scoped store (public close()) and reset the runtime
    handles so the next test builds a fresh store against its own isolated DB."""
    import web.app as webapp
    store = getattr(webapp, "_STORE", None)
    if store is not None:
        try:
            store.close()
        except Exception:
            pass
    webapp._STORE = None
    webapp.SESSION_STORE.clear()


@pytest.fixture(autouse=True)
def isolated_inventorai_db(tmp_path, monkeypatch):
    # Unique, pytest-managed, on-disk database for this test — never the shared
    # local-development DB. monkeypatch reverts the env var after the test.
    monkeypatch.setenv("INVENTORAI_DB_PATH",
                       str(tmp_path / "governed_p4_1b1.sqlite"))
    _close_and_reset_store()
    yield
    _close_and_reset_store()
