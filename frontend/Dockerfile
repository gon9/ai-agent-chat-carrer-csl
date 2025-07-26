FROM node:20-slim

WORKDIR /app

# 必要なファイルをコピー
COPY package*.json ./

# 依存関係をインストール
RUN npm install

# ソースコードをコピー
COPY . .

# ポートを公開
EXPOSE 3000

# 開発サーバーを起動
# ホストマシンからアクセスできるように設定
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0"]
