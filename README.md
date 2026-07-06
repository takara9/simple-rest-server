
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

バックエンド環境変数:
- `DB_HOST` (default: `localhost`)
- `DB_PORT` (default: `5432`)
- `DB_NAME` (default: `mydb`)
- `DB_USER` (default: `myuser`)
- `DB_PASSWORD` (default: `yourpassword`)
- `CORS_ALLOWED_ORIGINS` (default: `*`, カンマ区切り)

CORS 設定例（S3 Website からのアクセス許可）:
- `CORS_ALLOWED_ORIGINS=http://takara-450041988467-ap-northeast-1-an.s3-website-ap-northeast-1.amazonaws.com`

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

バックエンドを Docker コンテナで実行する手順:
1. PostgreSQL コンテナを起動（上記コマンド）
2. バックエンドイメージをビルド

```bash
docker build --network=host -t simple-rest-backend:latest .
```

3. バックエンドコンテナを起動

```bash
docker run --rm -p 5000:5000 \
	--add-host=host.docker.internal:host-gateway \
	-e DB_HOST=host.docker.internal \
	-e DB_PORT=5432 \
	-e DB_NAME=mydb \
	-e DB_USER=myuser \
	-e DB_PASSWORD=yourpassword \
	--name simple-rest-backend \
	simple-rest-backend:latest
```

ビルド時の注意:
- `Temporary failure in name resolution` が出る場合、上記の `--network=host` 付きビルドを使ってください。

フロントエンドを Docker コンテナで実行する手順:
1. フロントエンドイメージをビルド

```bash
docker build --network=host -t simple-rest-frontend:latest ./frontend
```

2. フロントエンドコンテナを起動

```bash
docker run --rm -p 5173:5173 \
	--add-host=host.docker.internal:host-gateway \
	-e VITE_API_PROXY_TARGET=http://host.docker.internal:5000 \
	--name simple-rest-frontend \
	simple-rest-frontend:latest
```

3. ブラウザで `http://127.0.0.1:5173` を開く

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

docker compose での起動方法:
1. プロジェクトルートに移動

```bash
cd /home/ubuntu/simple-rest-server
```

2. 3サービス（postgres / backend / frontend）を起動

```bash
docker compose up -d
```

イメージを GHCR から最新化して起動する場合:

```bash
docker compose pull
docker compose up -d --force-recreate
```

3. 起動状態を確認

```bash
docker compose ps
```

4. ブラウザで以下を開く
- フロントエンド: `http://127.0.0.1:5173`
- バックエンド API: `http://127.0.0.1:5000/data`

5. 停止する場合

```bash
docker compose down
```

S3 配信向けに API アドレスを変更してビルドする方法:
1. `frontend/src/App.jsx` は `VITE_API_BASE_URL` を読む実装になっています。
2. 以下のように API のベース URL を指定してビルドします（末尾に `/data` は付けない）。

```bash
cd /home/ubuntu/simple-rest-server/frontend
VITE_API_BASE_URL=https://si-bf2f33478ce845f1aa3f7920f62e7fd7.ecs.ap-northeast-1.on.aws npm run build
```

3. 生成された `frontend/dist` を S3 へアップロードしてください。



## メモ

```
sg-0de78feec0d792957

database-1.czy22iewajnl.ap-northeast-1.rds.amazonaws.com

curl -X POST https://si-bf2f33478ce845f1aa3f7920f62e7fd7.ecs.ap-northeast-1.on.aws/data -H "Content-Type: application/json" -d '{"id":1,"text":"hello"}'
curl https://si-bf2f33478ce845f1aa3f7920f62e7fd7.ecs.ap-northeast-1.on.aws/data
curl -X DELETE https://si-bf2f33478ce845f1aa3f7920f62e7fd7.ecs.ap-northeast-1.on.aws/data -H "Content-Type: application/json" -d '{"id":1}'
curl -X DELETE https://si-bf2f33478ce845f1aa3f7920f62e7fd7.ecs.ap-northeast-1.on.aws/data -H "Content-Type: application/json" -d '{"id":2}'
```
