# PawWatch — Web

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

`/home/` used to be the landing page and now redirects to `/`. The rule
is in `public/_redirects`.

## Fonts

Fraunces and Inter are served by this site, not by Google's Fonts API,
so a visitor's browser never contacts Google and no visitor's IP address
is sent to them. Both are SIL Open Font License; the licence text is at
`/fonts/licenses/`.

`scripts/download_fonts.py` re-downloads the font files.
`scripts/fetch_og_fonts.py` fetches the TTFs that `scripts/make_og.py`
draws the social share image with.

## Checks

- `scripts/verify_site.py` — checks the built site in `dist/`
- `scripts/verify_live.py <url>` — checks a deployed host over HTTP
- `scripts/deploy-preview.sh` — builds, checks, then deploys to the
  preview branch. It does not touch production.

## Deploy

Cloudflare Pages, connected to GitHub. Custom domain `paw-watch.app`
once DNS is pointed at the Pages project.

A push to `main` deploys to production. Everything else gets a preview
link.

## Maintainer

PawWatch is published by Cerminara Consulting LLC.
See `../pawwatch` for the iOS app repo.
