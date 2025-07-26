FROM python:3.12-slim

WORKDIR /app

# 必要なパッケージをインストール
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uv

# プロジェクト定義ファイルをコピー
COPY pyproject.toml uv.lock ./

# pyproject.tomlとuv.lockから正確な依存関係をインストール
RUN uv pip install --system .

# ソースコードをコピー
COPY . .

# 環境変数を設定
ENV PYTHONUNBUFFERED=1

# ポートを公開
EXPOSE 8000

# アプリケーションを実行
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
