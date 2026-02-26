import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  basePath: '/nexstay',
  assetPrefix: '/nexstay/',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
