#!/usr/bin/env python3
"""
Verify the DEPLOYED preview of the PawWatch site.

This fetches each page over HTTP from the preview host and checks the
same things as verify_site.py does, but against what a visitor actually
receives rather than what was built. A page can pass the local build
check and still pick up something at the edge, so this runs against the
live URL.

Usage:
    python scripts/verify_live.py <base-url>
"""
import re
import sys
import urllib.error
import urllib.request

OWN_HOSTS = ("paw-watch.app", "www.paw-watch.app", "pawwatch-site.pages.dev")

PAGES = [
    ("/", 200),
    ("/home/", 301),
    ("/privacy-policy/", 200),
    ("/support/", 200),
    # Astro builds the 404 page as /404.html, and the site's trailing
    # slash setting turns that into a 308 to /404, which serves it.
    ("/404.html", 308),
]

failures = []
notes = []


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 Chrome"})
    # No redirect following, so the 301 is visible.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    opener = urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(req, timeout=30) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers)


def main():
    base = sys.argv[1].rstrip("/")
    if not base.startswith("http"):
        base = "https://" + base
    print(f"checking the live preview at {base}\n")

    for path, expected in PAGES:
        url = base + path
        print(f"--- {path} ---")
        status, body, headers = get(url)
        print(f"  HTTP {status} (expected {expected})")

        if status != expected:
            failures.append(f"{path}: HTTP {status}, expected {expected}")
            print(f"  FAIL status {status} != {expected}")
        else:
            print(f"  PASS status {status}")

        if status == 301:
            loc = headers.get("Location", "")
            print(f"  Location: {loc}")
            if loc.rstrip("/") in ("", "/"):
                print("  PASS redirects to the home page")
            else:
                failures.append(f"{path}: redirects to {loc}, expected /")
                print(f"  FAIL wrong redirect target")

        html = body.decode("utf-8", "replace")

        # Script tags.
        scripts = re.findall(r"<script\b", html, re.I)
        if scripts:
            failures.append(f"{path}: {len(scripts)} script tag(s)")
            print(f"  FAIL {len(scripts)} script tag(s)")
        else:
            print("  PASS zero script tags")

        # Loaded resources: every one must be same-origin.
        resource_tags = ("script", "link", "img", "iframe", "source", "video",
                         "audio", "embed", "object", "track")
        hosts = set()
        for tag in resource_tags:
            for m in re.finditer(
                r"<%s\b[^>]*?\s(?:src|href)\s*=\s*[\"'](https?://[^\"']+)[\"']" % tag,
                html, re.I):
                hosts.add(re.match(r"https?://([^/:?#]+)", m.group(1)).group(1).lower())
        for m in re.finditer(r"url\(\s*['\"]?(https?://[^'\")]+)", html, re.I):
            hosts.add(re.match(r"https?://([^/:?#]+)", m.group(1)).group(1).lower())

        external = sorted(h for h in hosts if not any(h.endswith(o) for o in OWN_HOSTS))
        if external:
            failures.append(f"{path}: loads from external host(s): {external}")
            print(f"  FAIL external resource hosts: {external}")
        else:
            print(f"  PASS no external resource hosts (hosts: {sorted(hosts) or 'none'})")

        # Google font references, anywhere.
        for bad in ("fonts.googleapis.com", "fonts.gstatic.com"):
            if bad in html:
                failures.append(f"{path}: references {bad}")
                print(f"  FAIL references {bad}")
        if "fonts.googleapis.com" not in html and "fonts.gstatic.com" not in html:
            print("  PASS no Google font references")

        # The old name.
        hits = html.count("Paw Watch")
        exempt = "privacy-policy" in path or "support" in path
        if hits and not exempt:
            failures.append(f"{path}: {hits} 'Paw Watch'")
            print(f"  FAIL 'Paw Watch' x{hits}")
        elif hits:
            notes.append(f"{path}: {hits} 'Paw Watch' in body text (exempt)")
            print(f"  NOTE {hits} 'Paw Watch' in body text (exempt)")
        else:
            print("  PASS no 'Paw Watch'")

        # Plain mailto links.
        for m in re.finditer(r'href="([^"]*mailto:[^"]*)"', html):
            if "data-cfemail" in m.group(1) or "__cf_email__" in m.group(1):
                failures.append(f"{path}: obfuscated email link")
                print("  FAIL obfuscated mailto")
        if "mailto:" in html:
            print("  PASS mailto links present and plain")

        print()

    # The 404 page has to actually be servable. Cloudflare serves it for
    # any path that does not exist, and /404 is where Astro put it.
    print("--- the 404 page itself ---")
    status, body, _ = get(base + "/404")
    print(f"  HTTP {status}")
    if status == 200:
        html = body.decode("utf-8", "replace")
        if "Paw Watch" in html:
            failures.append("/404: contains 'Paw Watch'")
            print("  FAIL contains 'Paw Watch'")
        else:
            print("  PASS served, no 'Paw Watch'")
        if re.search(r"<script\b", html, re.I):
            failures.append("/404: contains a script tag")
            print("  FAIL contains a script tag")
        else:
            print("  PASS zero script tags")
    else:
        failures.append(f"/404: HTTP {status}")
        print(f"  FAIL status {status}")

    status, _, _ = get(base + "/no-such-page-here/")
    print(f"  an unknown path returns HTTP {status}")
    if status == 404:
        print("  PASS unknown paths 404")
    else:
        failures.append(f"an unknown path returned {status}, expected 404")
        print(f"  FAIL expected 404")

    print()
    print("=" * 70)
    if notes:
        print(f"{len(notes)} note(s):")
        for n in notes:
            print(f"  NOTE  {n}")
        print()
    if failures:
        print(f"{len(failures)} FAILURE(S):")
        for f in failures:
            print(f"  FAIL  {f}")
        return 1
    print("All live checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
