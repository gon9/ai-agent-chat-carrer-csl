FROM python:3.12-slim

WORKDIR /app

# 必要なパッケージをインストール
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uv

# ソースコードをコピー
COPY requirements.txt .

# 依存関係をインストール
RUN uv pip install --system -r requirements.txt

# ソースコードをコピー
COPY . .

# 環境変数を設定
ENV PYTHONUNBUFFERED=1

# ポートを公開
EXPOSE 8000

# アプリケーションを実行
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
