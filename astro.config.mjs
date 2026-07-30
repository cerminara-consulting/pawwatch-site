// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://paw-watch.app',
  output: 'static',
  build: {
    format: 'directory',
  },
  // Trailing slash is required for Cloudflare Pages static hosting
  trailingSlash: 'always',
  // Compress output for Edge delivery
  compressHTML: true,
});
