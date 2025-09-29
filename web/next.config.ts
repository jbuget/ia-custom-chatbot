import type { NextConfig } from "next";
import path from 'path';

/* cf. https://nextjs.org/docs/app/api-reference/config/next-config-js */
const nextConfig: NextConfig = {
  turbopack: {
    root: path.join(__dirname, '..'),
  },
};

export default nextConfig;
