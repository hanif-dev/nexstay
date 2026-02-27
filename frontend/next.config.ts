import type { NextConfig } from "next";

const isGithubPages = process.env.DEPLOY_TARGET === 'github';

const nextConfig: NextConfig = {
  ...(isGithubPages && {
    output: 'export',
    basePath: '/nexstay',
    assetPrefix: '/nexstay/',
  }),
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  experimental: {
    turbo: {
      ...(isGithubPages && { enabled: false }),
    },
  },
};

export default nextConfig;
