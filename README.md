# AI Agent Chat Career Counselor

LangGraphを使用したキャリアカウンセリングAIチャットアプリケーション

## 概要

このプロジェクトは、FastAPIとLangGraphを使用して構築されたキャリアカウンセリングAIチャットアプリケーションです。ユーザーはAIキャリアカウンセラーとチャットを行い、キャリアに関するアドバイスを受けることができます。

## 技術スタック

- Python 3.12
- FastAPI
- LangGraph
- LangChain
- OpenAI API (gpt-4o)
- uvicorn

## セットアップ

### 前提条件

- Python 3.12
- uv（パッケージマネージャー）

### インストール

```bash
# バックエンドディレクトリに移動
cd backend

# 仮想環境を作成
uv venv -p 3.12

# 仮想環境をアクティベート
source .venv/bin/activate

# 依存関係をインストール
uv pip install fastapi uvicorn langchain langchain-core langchain-community langchain-openai langgraph pydantic-settings
```

### 環境変数の設定

`.env.example`ファイルを`.env`にコピーし、必要な環境変数を設定します：

```bash
cp .env.example .env
```

`.env`ファイルを編集して、OpenAI APIキーを設定します：

```
OPENAI_API_KEY=your_openai_api_key_here
```

### アプリケーションの実行

```bash
python run.py
```

アプリケーションは`http://localhost:8000`で実行されます。
API ドキュメントは`http://localhost:8000/api/v1/docs`で確認できます。

## API エンドポイント

### ヘルスチェック

```
GET /api/v1/health
```

**レスポンス例：**

```json
{
  "status": "ok"
}
```

### 新しい会話の作成

```
POST /api/v1/chat/conversations
```

**レスポンス例：**

```json
{
  "id": "f3f8e270-e66b-4c5f-b81d-2fb4a45df269",
  "messages": [],
  "metadata": null,
  "created_at": "2025-07-13T20:59:57.599271",
  "updated_at": "2025-07-13T20:59:57.599274"
}
```

### メッセージの送信

```
POST /api/v1/chat/send
```

**リクエスト例：**

```json
{
  "message": "キャリアについて相談したいです",
  "conversation_id": "f3f8e270-e66b-4c5f-b81d-2fb4a45df269"
}
```

**レスポンス例：**

```json
{
  "message": "職場環境も重要な要素です。どのような企業文化や働き方があなたに合っていると思いますか？",
  "conversation_id": "f3f8e270-e66b-4c5f-b81d-2fb4a45df269",
  "metadata": {
    "history": [
      {
        "role": "user",
        "content": "キャリアについて相談したいです"
      }
    ]
  }
}
```

### 会話の取得

```
GET /api/v1/chat/conversations/{conversation_id}
```

**レスポンス例：**

```json
{
  "id": "f3f8e270-e66b-4c5f-b81d-2fb4a45df269",
  "messages": [
    {
      "id": "8a8eb1d1-8429-44c2-a16c-ef953a22dd63",
      "role": "user",
      "content": "キャリアについて相談したいです",
      "timestamp": "2025-07-13T21:00:07.708799"
    },
    {
      "id": "cf24157e-64d1-4253-bfbb-6d5d26f25ad2",
      "role": "assistant",
      "content": "職場環境も重要な要素です。どのような企業文化や働き方があなたに合っていると思いますか？",
      "timestamp": "2025-07-13T21:00:07.712741"
    }
  ],
  "metadata": null,
  "created_at": "2025-07-13T20:59:57.599271",
  "updated_at": "2025-07-13T21:00:07.712741"
}
```

### 会話のメッセージ取得

```
GET /api/v1/chat/conversations/{conversation_id}/messages
```

**レスポンス例：**

```json
[
  {
    "id": "8a8eb1d1-8429-44c2-a16c-ef953a22dd63",
    "role": "user",
    "content": "キャリアについて相談したいです",
    "timestamp": "2025-07-13T21:00:07.708799"
  },
  {
    "id": "cf24157e-64d1-4253-bfbb-6d5d26f25ad2",
    "role": "assistant",
    "content": "職場環境も重要な要素です。どのような企業文化や働き方があなたに合っていると思いますか？",
    "timestamp": "2025-07-13T21:00:07.712741"
  }
]
```

## プロジェクト構造

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── chat.py
│   │       │   └── health.py
│   │       └── router.py
│   ├── core/
│   │   └── config.py
│   ├── models/
│   ├── schemas/
│   │   ├── chat.py
│   │   └── health.py
│   ├── services/
│   │   ├── agent.py
│   │   └── conversation.py
│   └── main.py
├── .env
├── .env.example
└── run.py
```
