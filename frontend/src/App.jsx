import React, { useEffect, useState } from "react";

const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");
const dataEndpoint = apiBaseUrl ? `${apiBaseUrl}/data` : "/data";

function App() {
  const [items, setItems] = useState([]);
  const [formId, setFormId] = useState("");
  const [formText, setFormText] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function requestJson(url, options = {}) {
    const response = await fetch(url, options);
    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.error || "Request failed");
    }

    return data;
  }

  async function loadItems() {
    setLoading(true);
    setError("");
    try {
      const data = await requestJson(dataEndpoint);
      setItems(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadItems();
  }, []);

  async function handleCreate(event) {
    event.preventDefault();
    setMessage("");
    setError("");

    try {
      await requestJson(dataEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: formId, text: formText }),
      });

      setMessage("作成しました");
      setFormId("");
      setFormText("");
      await loadItems();
    } catch (e) {
      setError(e.message);
    }
  }

  async function handleUpdate(itemId, newText) {
    setMessage("");
    setError("");

    try {
      await requestJson(dataEndpoint, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: itemId, text: newText }),
      });

      setMessage(`id=${itemId} を更新しました`);
      await loadItems();
    } catch (e) {
      setError(e.message);
    }
  }

  async function handleDelete(itemId) {
    setMessage("");
    setError("");

    try {
      await requestJson(dataEndpoint, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: itemId }),
      });

      setMessage(`id=${itemId} を削除しました`);
      await loadItems();
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <main className="page">
      <section className="panel">
        <h1>Data Manager SPA</h1>
        <p>/data API をブラウザから操作できます。</p>

        <form className="form" onSubmit={handleCreate}>
          <label>
            id
            <input
              value={formId}
              onChange={(e) => setFormId(e.target.value)}
              placeholder="例: 1"
              required
            />
          </label>

          <label>
            text
            <input
              value={formText}
              onChange={(e) => setFormText(e.target.value)}
              placeholder="例: hello"
              required
            />
          </label>

          <button type="submit">新規作成 (POST)</button>
        </form>

        {message && <p className="ok">{message}</p>}
        {error && <p className="ng">{error}</p>}
      </section>

      <section className="panel">
        <h2>一覧 (GET)</h2>
        {loading ? <p>読み込み中...</p> : null}
        {!loading && items.length === 0 ? <p>データがありません。</p> : null}

        <ul className="list">
          {items.map((item) => (
            <DataRow
              key={item.id}
              item={item}
              onUpdate={handleUpdate}
              onDelete={handleDelete}
            />
          ))}
        </ul>
      </section>
    </main>
  );
}

function DataRow({ item, onUpdate, onDelete }) {
  const [editText, setEditText] = useState(item.text);

  useEffect(() => {
    setEditText(item.text);
  }, [item.text]);

  return (
    <li className="item">
      <div className="meta">
        <strong>id:</strong> {item.id}
      </div>
      <input
        value={editText}
        onChange={(e) => setEditText(e.target.value)}
        aria-label={`text-${item.id}`}
      />
      <div className="actions">
        <button onClick={() => onUpdate(item.id, editText)}>更新 (PUT)</button>
        <button className="danger" onClick={() => onDelete(item.id)}>
          削除 (DELETE)
        </button>
      </div>
    </li>
  );
}

export default App;
