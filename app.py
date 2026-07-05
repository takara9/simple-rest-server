import sqlite3

from flask import Flask, jsonify, request
from handlers import handle_delete, handle_get, handle_post, handle_put

app = Flask(__name__)
DB_PATH = "data.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS data (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL
            )
            """
        )
        conn.commit()


@app.route("/data", methods=["GET", "POST", "PUT", "DELETE"])
def data_api():
    method_handlers = {
        "GET": lambda: handle_get(DB_PATH),
        "POST": lambda payload: handle_post(DB_PATH, payload),
        "PUT": lambda payload: handle_put(DB_PATH, payload),
        "DELETE": lambda payload: handle_delete(DB_PATH, payload),
    }

    if request.method == "GET":
        return method_handlers["GET"]()

    payload = request.get_json(silent=True) or {}

    if request.method in method_handlers:
        return method_handlers[request.method](payload)

    return jsonify({"error": "Method not allowed."}), 405


init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
