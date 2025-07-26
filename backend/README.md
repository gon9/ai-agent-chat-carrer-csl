# キャリアカウンセラーAIアシスタント バックエンド

FastAPIとLangGraphを使用したキャリアカウンセラーAIアシスタントのバックエンド実装です。Python 3.12とuvを使用した最新の開発環境で構築されています。

## 機能

- FastAPIによるRESTful API
- LangGraphを使用したマルチエージェントシステム
- キャリアカウンセラーとITスキル専門家の連携
- OpenAI GPT-4oモデルを活用した高度な対話
- 会話履歴の保存と取得機能

## プロジェクト構成

```
backend/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/
│   │   │   └── health.py
│   │   └── router.py
│   ├── core/
│   │   └── config.py
│   ├── models/
│   ├── schemas/
│   │   └── health.py
│   ├── services/
│   │   └── agent.py
│   └── main.py
├── .env
├── .env.example
├── pyproject.toml
├── README.md
├── run.py
└── visualize_graph.py
```

## 環境構築

### 前提条件

- Python 3.12以上
- uv (Python パッケージマネージャー)

### セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/ai-agent-chat-carrer-csl.git
cd ai-agent-chat-carrer-csl/backend

# 仮想環境を作成
uv venv

# 仮想環境を有効化
source .venv/bin/activate

# 依存関係をインストール
uv pip install -e .

# .envファイルを設定
cp .env.example .env
# .envファイルを編集してOpenAI APIキーを設定
```

## 実行方法

```bash
# 仮想環境を有効化（まだ有効化していない場合）
source .venv/bin/activate

# サーバーを起動
python run.py
```

## エージェントグラフの可視化

```bash
python visualize_graph.py
```

このコマンドを実行すると、`agent_graph.png`というファイルが生成され、以下のようなエージェントの構造が可視化されます：

- キャリアカウンセラー（エントリーポイント）
- ITスキル専門家（専門的な技術相談が必要な場合）
- レスポンス生成（最終的な回答を生成）
- 終了ノード

## Dockerでの実行

このプロジェクトはDockerでも実行できます。以下は`Dockerfile`の例です：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 必要なパッケージをインストール
RUN pip install --no-cache-dir uv

# ソースコードをコピー
COPY . .

# 依存関係をインストール
RUN uv pip install -e .

# 環境変数を設定
ENV PYTHONUNBUFFERED=1

# ポートを公開
EXPOSE 8000

# アプリケーションを実行
CMD ["python", "run.py"]
```

Dockerイメージをビルドして実行するには：

```bash
# イメージをビルド
docker build -t carrer-csl-backend .

# コンテナを実行
docker run -p 8000:8000 -e OPENAI_API_KEY=your_api_key_here carrer-csl-backend
```
