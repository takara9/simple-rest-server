import psycopg2

from flask import jsonify


def handle_get(db_config):
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, text FROM data ORDER BY id")
            rows = cur.fetchall()

    items = [{"id": item_id, "text": text} for item_id, text in rows]
    return jsonify(items), 200


def handle_post(db_config, payload):
    item_id = payload.get("id")
    text = payload.get("text")

    if item_id is None or text is None:
        return jsonify({"error": "Both 'id' and 'text' are required."}), 400

    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO data (id, text) VALUES (%s, %s)",
                    (str(item_id), text),
                )
            conn.commit()
    except psycopg2.IntegrityError:
        return jsonify({"error": "Data with this id already exists."}), 409

    return jsonify({"id": str(item_id), "text": text}), 201


def handle_put(db_config, payload):
    item_id = payload.get("id")
    text = payload.get("text")

    if item_id is None or text is None:
        return jsonify({"error": "Both 'id' and 'text' are required."}), 400

    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE data SET text = %s WHERE id = %s",
                (text, str(item_id)),
            )
            updated_count = cur.rowcount
        conn.commit()

    if updated_count == 0:
        return jsonify({"error": "Data not found."}), 404

    return jsonify({"id": str(item_id), "text": text}), 200


def handle_delete(db_config, payload):
    item_id = payload.get("id")

    if item_id is None:
        return jsonify({"error": "'id' is required."}), 400

    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT text FROM data WHERE id = %s",
                (str(item_id),),
            )
            row = cur.fetchone()

            if row is None:
                return jsonify({"error": "Data not found."}), 404

            cur.execute("DELETE FROM data WHERE id = %s", (str(item_id),))
        conn.commit()

    return jsonify({"id": str(item_id), "text": row[0]}), 200
