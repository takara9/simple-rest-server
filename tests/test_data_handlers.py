from flask import Flask
import psycopg2

from handlers.data_handlers import handle_delete, handle_get, handle_post, handle_put


class FakeCursor:
    def __init__(self, *, rows=None, row=None, rowcount=0):
        self.rows = rows or []
        self.row = row
        self.rowcount = rowcount
        self.executed = []

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchall(self):
        return self.rows

    def fetchone(self):
        return self.row

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor
        self.committed = False

    def cursor(self):
        return self._cursor

    def commit(self):
        self.committed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def make_connect(fake_connection):
    def _connect(**_kwargs):
        return fake_connection

    return _connect


def test_handle_get_returns_items(monkeypatch):
    fake_cursor = FakeCursor(rows=[("1", "hello"), ("2", "world")])
    fake_connection = FakeConnection(fake_cursor)
    monkeypatch.setattr(
        "handlers.data_handlers.psycopg2.connect",
        make_connect(fake_connection),
    )

    app = Flask(__name__)
    with app.app_context():
        response, status = handle_get({})

    assert status == 200
    assert response.get_json() == [
        {"id": "1", "text": "hello"},
        {"id": "2", "text": "world"},
    ]


def test_handle_post_missing_fields_returns_400():
    app = Flask(__name__)
    with app.app_context():
        response, status = handle_post({}, {"id": "1"})

    assert status == 400
    assert response.get_json()["error"] == "Both 'id' and 'text' are required."


def test_handle_post_duplicate_returns_409(monkeypatch):
    def raise_integrity_error(**_kwargs):
        raise psycopg2.IntegrityError()

    monkeypatch.setattr("handlers.data_handlers.psycopg2.connect", raise_integrity_error)

    app = Flask(__name__)
    with app.app_context():
        response, status = handle_post({}, {"id": "1", "text": "hello"})

    assert status == 409
    assert response.get_json()["error"] == "Data with this id already exists."


def test_handle_put_not_found_returns_404(monkeypatch):
    fake_cursor = FakeCursor(rowcount=0)
    fake_connection = FakeConnection(fake_cursor)
    monkeypatch.setattr(
        "handlers.data_handlers.psycopg2.connect",
        make_connect(fake_connection),
    )

    app = Flask(__name__)
    with app.app_context():
        response, status = handle_put({}, {"id": "1", "text": "updated"})

    assert status == 404
    assert response.get_json()["error"] == "Data not found."


def test_handle_delete_success_returns_deleted_data(monkeypatch):
    fake_cursor = FakeCursor(row=("hello",))
    fake_connection = FakeConnection(fake_cursor)
    monkeypatch.setattr(
        "handlers.data_handlers.psycopg2.connect",
        make_connect(fake_connection),
    )

    app = Flask(__name__)
    with app.app_context():
        response, status = handle_delete({}, {"id": "1"})

    assert status == 200
    assert response.get_json() == {"id": "1", "text": "hello"}
