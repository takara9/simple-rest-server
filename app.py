import os

import psycopg2

from flask import Flask, jsonify, request
from handlers import handle_delete, handle_get, handle_post, handle_put

app = Flask(__name__)
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "mydb"),
    "user": os.getenv("DB_USER", "myuser"),
    "password": os.getenv("DB_PASSWORD", "yourpassword"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
}


def init_db():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(
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
        "GET": lambda: handle_get(DB_CONFIG),
        "POST": lambda payload: handle_post(DB_CONFIG, payload),
        "PUT": lambda payload: handle_put(DB_CONFIG, payload),
        "DELETE": lambda payload: handle_delete(DB_CONFIG, payload),
    }

    if request.method == "GET":
        return method_handlers["GET"]()

    payload = request.get_json(silent=True) or {}

    if request.method in method_handlers:
        return method_handlers[request.method](payload)

    return jsonify({"error": "Method not allowed."}), 405


init_db()


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
