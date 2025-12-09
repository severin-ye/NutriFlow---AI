import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: false, // Disabled to prevent ref issues with camera
  // Suppress hydration warnings caused by browser extensions
  onDemandEntries: {
    maxInactiveAge: 25 * 1000,
    pagesBufferLength: 2,
  },
  experimental: {
    serverActions: {
      bodySizeLimit: '30mb', // Increase limit to 30MB for image uploads
    },
  },
};

export default nextConfig;
