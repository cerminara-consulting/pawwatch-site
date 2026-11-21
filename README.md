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
- `/terms/` — Terms of Use (App Store requirement)
- `/support/` — Support FAQ + contact info
- `/404.html` — Custom 404

`/home/` used to be the landing page and now redirects to `/`. The rule
is in `public/_redirects`.

## Where the page copy comes from

The privacy policy, terms and support copy lives in the **iOS repo**, not
here, in `docs/site/`. `scripts/sync_docs.py` fetches it with `gh api`
(read only — it never writes to that repo) and writes it into
`src/content-docs/`. The Astro pages import those files and render them
at build time, so the site ships plain HTML with no script.

Three transforms are applied, and only these three:

1. HTML comments are removed. They are notes for John, not page copy.
2. `[PUBLISH DATE]` becomes today's date.
3. Bare email addresses and bare policy URLs become links. The visible
   words are not changed.

Everything else is word for word. `scripts/verify_docs.py` proves it: it
compares the built page's text against the source and fails on the first
word that differs.

To pick up a change in the copy:

```bash
python scripts/sync_docs.py    # fetch and write
npm run build
python scripts/verify_site.py  # checks the build against the copy
```

`scripts/sync_docs.py --check` verifies the committed copy still matches
the source without writing anything.

The home page corrections are applied the same way, by
`scripts/apply_home_corrections.py`. It matches each sentence exactly
and refuses to continue if a sentence is not found exactly once.

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
