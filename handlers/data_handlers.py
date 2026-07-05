import sqlite3

from flask import jsonify


def handle_get(db_path):
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("SELECT id, text FROM data ORDER BY rowid").fetchall()

    items = [{"id": item_id, "text": text} for item_id, text in rows]
    return jsonify(items), 200


def handle_post(db_path, payload):
    item_id = payload.get("id")
    text = payload.get("text")

    if item_id is None or text is None:
        return jsonify({"error": "Both 'id' and 'text' are required."}), 400

    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                "INSERT INTO data (id, text) VALUES (?, ?)",
                (str(item_id), text),
            )
            conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Data with this id already exists."}), 409

    return jsonify({"id": str(item_id), "text": text}), 201


def handle_put(db_path, payload):
    item_id = payload.get("id")
    text = payload.get("text")

    if item_id is None or text is None:
        return jsonify({"error": "Both 'id' and 'text' are required."}), 400

    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            "UPDATE data SET text = ? WHERE id = ?",
            (text, str(item_id)),
        )
        conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Data not found."}), 404

    return jsonify({"id": str(item_id), "text": text}), 200


def handle_delete(db_path, payload):
    item_id = payload.get("id")

    if item_id is None:
        return jsonify({"error": "'id' is required."}), 400

    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT text FROM data WHERE id = ?",
            (str(item_id),),
        ).fetchone()

        if row is None:
            return jsonify({"error": "Data not found."}), 404

        conn.execute("DELETE FROM data WHERE id = ?", (str(item_id),))
        conn.commit()

    return jsonify({"id": str(item_id), "text": row[0]}), 200
