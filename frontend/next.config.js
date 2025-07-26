/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://backend:8000/api/:path*', // Docker Compose内でのバックエンドサービス名
      },
    ];
  },
};

module.exports = nextConfig;
