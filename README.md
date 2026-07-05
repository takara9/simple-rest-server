
# Flask サーバー

- app.py
- requirements.txt
- frontend/

実装内容:
- エンドポイント: /data
- メソッド:
1. GET /data
2. POST /data
3. PUT /data
4. DELETE /data
- データ構造: id と text
- 保存先: PostgreSQL (`mydb.data`)

PostgreSQL 接続情報:
- host: `localhost`
- port: `5432`
- dbname: `mydb`
- user: `myuser`
- password: `yourpassword`

動作確認:
- app.py の構文チェックは python3 で成功しています。

実行手順:
1. cd /home/ubuntu/simple-rest-server
2. (初回のみ) Ubuntu では `sudo apt-get install -y python3.12-venv`
3. python3 -m venv .venv
4. . .venv/bin/activate
5. python -m pip install -r requirements.txt
6. PostgreSQL コンテナを起動

```bash
docker run -d \
	--name my-postgres \
	-e POSTGRES_PASSWORD=yourpassword \
	-e POSTGRES_USER=myuser \
	-e POSTGRES_DB=mydb \
	-p 5432:5432 \
	-v pgdata:/var/lib/postgresql/data \
	postgres:16
```

7. python app.py

補足:
- `error: externally-managed-environment` が出る場合、システム環境に直接 pip install せず、上記の仮想環境を使ってください。

React SPA (フロントエンド):
1. 別ターミナルで `cd /home/ubuntu/simple-rest-server/frontend`
2. `npm install`
3. `npm run dev`
4. ブラウザで `http://127.0.0.1:5173` を開く

注意:
- 5173 が使用中の場合、Vite は 5174 など別ポートへ自動切替します。`npm run dev` の出力に表示された URL を開いてください。

フロントエンドは Vite のプロキシ設定により、`/data` を Flask (`http://127.0.0.1:5000`) へ転送します。

全体の起動順:
1. ターミナルA: `cd /home/ubuntu/simple-rest-server && . .venv/bin/activate && python app.py`
2. ターミナルB: `cd /home/ubuntu/simple-rest-server/frontend && npm install && npm run dev`

リクエスト例:
1. 作成
curl -X POST http://localhost:5000/data -H "Content-Type: application/json" -d '{"id":1,"text":"hello"}'

2. 取得
curl http://localhost:5000/data

3. 更新
curl -X PUT http://localhost:5000/data -H "Content-Type: application/json" -d '{"id":1,"text":"updated"}'

4. 削除
curl -X DELETE http://localhost:5000/data -H "Content-Type: application/json" -d '{"id":1}'


