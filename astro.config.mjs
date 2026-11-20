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
  markdown: {
    // The page copy in src/content-docs/ is the source of truth, word
    // for word. Smartypants would rewrite the straight quotes in it
    // into curly quotes, so the page would not match the source. It
    // stays off.
    smartypants: false,
  },
});
