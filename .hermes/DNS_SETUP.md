# paw-watch.app — DNS & Cloudflare setup reference

**Status as of 2026-08-16.** This doc describes the live state
of paw-watch.app after the zone was created in Cloudflare and
Apex + www records were added. Use this when troubleshooting a
regression or onboarding a new machine.

---

## Current state

| Component | Status |
|---|---|
| Registrar | GoDaddy (where the domain was bought) |
| DNS hosting | **Cloudflare** (zone `paw-watch.app` lives there now) |
| Nameservers (parent `.app` registry) | `karina.ns.cloudflare.com`, `pete.ns.cloudflare.com` |
| Site hosting | Cloudflare Pages project `pawwatch-site` |
| Live URL | `https://paw-watch.app/` (after Pages custom-domain add) |
| Fallback URL | `https://pawwatch-site.pages.dev/` (live now) |
| Mailboxes (`privacy@`, `support@`) | Google Workspace, MX records present in Cloudflare |

## Apex DNS records in Cloudflare

| Type | Name | Value | Proxy |
|---|---|---|---|
| A | `@` | `76.223.105.230` | DNS only (grey cloud) |
| A | `@` | `13.248.243.5` | DNS only (grey cloud) |
| CNAME | `www` | `pawwatch-site.pages.dev` | DNS only |
| MX | `@` | `aspmx.l.google.com` (priority 1) | n/a |
| MX | `@` | `alt1.aspmx.l.google.com` (priority 5) | n/a |
| MX | `@` | `alt2.aspmx.l.google.com` (priority 5) | n/a |
| MX | `@` | `alt3.aspmx.l.google.com` (priority 10) | n/a |
| MX | `@` | `alt4.aspmx.l.google.com` (priority 10) | n/a |
| TXT | `@` | `v=spf1 include:_spf.google.com ~all` | n/a |
| TXT | `@` | `google-site-verification=-xdDU-32kk4U0cnvpPNhkTxrjrXYRmpFv0WnbTVb2L4` | n/a |

**Important**: apex A records are **DNS only** (grey cloud), not
proxied. Cloudflare Pages uses CNAME-style custom-hostname
verification and the apex A records point at Cloudflare's
reverse-proxy fleet (`76.223.105.230` / `13.248.243.5`) which
are NOT going through Cloudflare's proxy. Going through the
orange proxy on these specific IPs would break Pages routing.

## The transition history (so future-us doesn't repeat it)

1. **Initial state** — Domain was bought at GoDaddy, hosted on
   `pawwatch-site.pages.dev` as a Cloudflare Pages project.
   Apex pointed at GoDaddy parking IPs.
2. **First attempt** — Added A records (GoDaddy + Pages IP) and
   CNAME (www → pages.dev) at GoDaddy. Tried the Cloudflare
   "Add custom domain" wizard in Pages — wizard refused because
   the parent `.app` registry was still pointing at GoDaddy
   nameservers, so Cloudflare wasn't authoritative for the zone.
3. **Pivot to Cloudflare DNS** — Switched nameservers at GoDaddy
   to `karina.ns.cloudflare.com` + `pete.ns.cloudflare.com`.
   Parent `.app` registry propagated.
4. **Zone created** — Added `paw-watch.app` to Cloudflare
   account. Cloudflare assigned the karina/pete nameservers and
   the zone became authoritative.
5. **Records needed** — Cloudflare's auto-import found nothing
   (records were at GoDaddy, not transferable). Manually added
   A + CNAME + MX + TXT records to the Cloudflare zone.

## Outstanding (next steps)

- The Pages custom-domain wizard should now accept `paw-watch.app`
  because Cloudflare is authoritative for the zone. This adds
  `paw-watch.app` as a custom hostname on the Pages project,
  which auto-issues an SSL certificate within ~60 seconds.
- Mailbox DNS records live in Cloudflare now (not GoDaddy). If
  mailboxes break later, check Cloudflare DNS records page, not
  GoDaddy.

## Pitfalls learned

1. **CNAME-only setup is gone** — Cloudflare's Pages wizard no
   longer accepts CNAME-only apex setups without zone ownership.
   DNS at Cloudflare is required.
2. **Records don't transfer on NS switch** — GoDaddy records
   vanish when nameservers leave; you have to re-add them in
   the new DNS host.
3. **Apex A records to Pages IPs should be DNS-only, not
   proxied**. The IPs `76.223.105.230` / `13.248.243.5` are
   Cloudflare's CNAME-flattening fleet, not the proxy fleet.
   Proxying them would route through a different system.
4. **Use the nameservers Cloudflare assigns to YOU**, not arbitrary
   Cloudflare nameservers. The karina/pete pair above is unique to
   this zone; another zone has different assigned nameservers.

## Files & links

- Live site: https://paw-watch.app/ (apex)
- Alt: https://www.paw-watch.app/
- Cloudflare project: Workers & Pages → pawwatch-site
- Domain registrar: godaddy.com, account john@cerminaraconsulting.com
