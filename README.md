# Paw Watch — Web

Static site for **paw-watch.app**. Hosts the App Store-required pages
(privacy policy, support) and a landing page for human visitors.

Built with [Astro](https://astro.build) — no JS framework, no CMS, free
to host on Cloudflare Pages.

## Run it locally

```bash
npm install --no-audit --no-fund
npm run dev          # http://localhost:4321
npm run build        # → dist/
npm run preview      # serve dist/ locally
```

## Pages

- `/` — Landing page (hero + features + about)
- `/privacy-policy/` — Privacy Policy (App Store requirement)
- `/support/` — Support FAQ + contact info
- `/404.html` — Custom 404

## Deploy

Cloudflare Pages, connected to GitHub. Custom domain `paw-watch.app`
once DNS is pointed at the Pages project.

## Maintainer

Paw Watch is published by Cerminara Consulting LLC.
See `../pawwatch` for the iOS app repo.
