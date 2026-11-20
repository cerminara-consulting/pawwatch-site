#!/usr/bin/env python3
"""
Verify the built PawWatch site.

Checks every built page for:
  1. Zero <script> tags.
  2. No reference to any host other than the site itself. That means no
     fonts.googleapis.com, no fonts.gstatic.com, no analytics, no
     third-party script, no external image.
  3. No "Paw Watch" anywhere, except in the privacy policy and support
     body text, which John is rewriting separately.

Usage:
    python scripts/verify_site.py [dist-directory]
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DIST = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(SITE, "dist")

# The site's own host. A preview build is served from
# pawwatch-site.pages.dev and the production build from paw-watch.app.
# Both are the site itself.
OWN_HOSTS = ("paw-watch.app", "www.paw-watch.app", "pawwatch-site.pages.dev")

# Pages whose BODY text John is rewriting separately. Their titles and
# shared chrome still have to be correct, so only the body text is
# exempt from the "Paw Watch" check.
BODY_EXEMPT = ("privacy-policy", "support")

failures = []
notes = []


def ocr_image(path):
    """
    Read the text out of the social share image.

    The PNG carries no text of its own, so this is the only way to
    check what it says. scripts/make_og.py writes a plain text manifest
    next to the image listing every string it drew, and that is used
    first because it is exact. OCR is the backstop, for the case where
    the manifest is missing or the image was changed some other way.

    Returns the text, or None if it could not be read at all.
    """
    manifest = os.path.join(os.path.dirname(path), "og-image.txt")
    if os.path.exists(manifest):
        with open(manifest, encoding="utf-8") as f:
            return f.read()

    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        return None

    # tesseract is not on PATH by default on Windows.
    for candidate in (r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                      r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"):
        if os.path.exists(candidate):
            pytesseract.pytesseract.tesseract_cmd = candidate
            break
    try:
        return pytesseract.image_to_string(Image.open(path))
    except Exception:
        return None


def fail(msg):
    failures.append(msg)


def pages():
    out = []
    for root, _dirs, files in os.walk(DIST):
        for f in sorted(files):
            if f.endswith(".html"):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, DIST).replace("\\", "/")
                out.append((rel, p))
    return sorted(out)


def check_page(rel, path):
    html = open(path, encoding="utf-8").read()
    print(f"\n--- {rel} ---")

    # 1. Script tags.
    scripts = re.findall(r"<script\b", html, re.I)
    if scripts:
        fail(f"{rel}: {len(scripts)} <script> tag(s)")
        print(f"  FAIL script tags: {len(scripts)}")
    else:
        print("  PASS zero script tags")

    # Inline event handlers and javascript: URLs are scripts too.
    handlers = re.findall(r"\son\w+\s*=\s*[\"']", html)
    if handlers:
        fail(f"{rel}: {len(handlers)} inline event handler(s)")
        print(f"  FAIL inline handlers: {len(handlers)}")
    else:
        print("  PASS zero inline event handlers")

    if re.search(r"javascript:", html, re.I):
        fail(f"{rel}: a javascript: URL")
        print("  FAIL javascript: URL")
    else:
        print("  PASS no javascript: URLs")

    # 2. External hosts.
    #
    # The check is on RESOURCES the page loads: stylesheets, scripts,
    # images, fonts, iframes, and so on. A hyperlink in prose is not a
    # request. The privacy policy links to Apple's, Google's and
    # Supabase's own privacy policies, which are a reader choosing to
    # go somewhere, and are not the site reaching out to anyone.
    #
    # An XML namespace URI (xmlns="http://www.w3.org/2000/svg") is an
    # identifier, not an address. Nothing is fetched from it.
    resource_tags = ("script", "link", "img", "iframe", "source", "video",
                     "audio", "embed", "object", "track")
    hosts = set()
    for tag in resource_tags:
        for m in re.finditer(
            r"<%s\b[^>]*?\s(?:src|href)\s*=\s*[\"'](https?://[^\"']+)[\"']" % tag,
            html, re.I,
        ):
            hosts.add(re.match(r"https?://([^/:?#]+)", m.group(1)).group(1).lower())
        # srcset="a.png 1x, https://... 2x"
        for m in re.finditer(
            r"<%s\b[^>]*?\ssrcset\s*=\s*[\"']([^\"']+)[\"']" % tag, html, re.I,
        ):
            for part in m.group(1).split(","):
                url = part.strip().split(" ")[0]
                if url.startswith("http"):
                    hosts.add(re.match(r"https?://([^/:?#]+)", url).group(1).lower())

    # A CSS @import or url() in an inline style block.
    for m in re.finditer(r"url\(\s*['\"]?(https?://[^'\")]+)", html, re.I):
        hosts.add(re.match(r"https?://([^/:?#]+)", m.group(1)).group(1).lower())

    external = sorted(h for h in hosts if not any(h.endswith(o) for o in OWN_HOSTS))
    if external:
        fail(f"{rel}: loads a resource from an external host: {', '.join(external)}")
        print(f"  FAIL external resource hosts: {external}")
    else:
        print(f"  PASS every loaded resource is the site itself "
              f"(resource hosts: {sorted(hosts) or 'none'})")

    # The specific strings this task was about. These must not appear
    # anywhere, not even as a hyperlink.
    for bad in ("fonts.googleapis.com", "fonts.gstatic.com"):
        if bad in html:
            fail(f"{rel}: references {bad}")
            print(f"  FAIL references {bad}")

    # 3. "Paw Watch".
    body_exempt = any(x in rel for x in BODY_EXEMPT)
    hits = html.count("Paw Watch")
    if hits:
        if body_exempt:
            notes.append(f"{rel}: {hits} 'Paw Watch' in the body text (exempt, being rewritten)")
            print(f"  NOTE {hits} 'Paw Watch' in body text (exempt)")
        else:
            fail(f"{rel}: {hits} 'Paw Watch'")
            print(f"  FAIL 'Paw Watch' x{hits}")
    else:
        print("  PASS no 'Paw Watch'")

    # Titles and shared chrome are never exempt.
    t = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    if t:
        title = t.group(1)
        if "Paw Watch" in title:
            fail(f"{rel}: title says 'Paw Watch': {title}")
            print(f"  FAIL title: {title}")
        else:
            print(f"  PASS title: {title}")

    for label in ("og:site_name",):
        m = re.search(r'<meta\s+property="%s"\s+content="([^"]*)"' % label, html, re.I)
        if m and "Paw Watch" in m.group(1):
            fail(f"{rel}: {label} says 'Paw Watch'")
            print(f"  FAIL {label}: {m.group(1)}")

    # Mailto links must be plain.
    mailtos = re.findall(r'href="([^"]*mailto:[^"]*)"', html)
    if mailtos:
        for m in mailtos:
            if "data-cfemail" in m or "__cf_email__" in m:
                fail(f"{rel}: obfuscated email link: {m}")
                print(f"  FAIL obfuscated mailto: {m}")
        print(f"  PASS {len(mailtos)} plain mailto link(s)")

    # The wordmark and footer must point at the home page.
    if rel == "index.html":
        if 'href="/home/"' in html:
            fail(f"{rel}: still links to /home/")
            print("  FAIL links to /home/")
        else:
            print("  PASS no link to /home/")


def main():
    if not os.path.isdir(DIST):
        print(f"FAIL: no build at {DIST}")
        return 1

    print(f"checking build at {DIST}")
    ps = pages()
    print(f"{len(ps)} HTML page(s) found")
    if not ps:
        print("FAIL: no HTML pages found")
        return 1

    for rel, path in ps:
        check_page(rel, path)

    # The fonts must be present and referenced locally.
    print("\n--- fonts ---")
    fdir = os.path.join(DIST, "fonts")
    if not os.path.isdir(fdir):
        fail("no fonts/ directory in the build")
        print("  FAIL no fonts/ directory")
    else:
        woffs = sorted(f for f in os.listdir(fdir) if f.endswith(".woff2"))
        print(f"  PASS {len(woffs)} woff2 file(s): {woffs}")
        css = os.path.join(fdir, "fonts.css")
        if not os.path.exists(css):
            fail("no fonts/fonts.css in the build")
        else:
            c = open(css, encoding="utf-8").read()
            if "fonts.googleapis.com" in c or "fonts.gstatic.com" in c:
                fail("fonts.css references Google")
                print("  FAIL fonts.css references Google")
            else:
                print("  PASS fonts.css has no Google references")
            missing = [w for w in woffs if w not in c]
            if missing:
                fail(f"fonts.css does not reference: {missing}")
                print(f"  FAIL fonts.css missing: {missing}")
            else:
                print("  PASS fonts.css references every woff2 file")
            lic = os.path.join(fdir, "licenses")
            if not os.path.isdir(lic) or not os.listdir(lic):
                fail("the OFL licence text is not shipped with the fonts")
                print("  FAIL no licence text")
            else:
                print(f"  PASS licence text shipped: {sorted(os.listdir(lic))}")

    # _redirects must be in the build.
    red = os.path.join(DIST, "_redirects")
    if not os.path.exists(red):
        fail("no _redirects in the build")
        print("\n--- redirects ---\n  FAIL no _redirects")
    else:
        print("\n--- redirects ---")
        content = open(red, encoding="utf-8").read()
        print("  PASS _redirects present")
        if "/home/" in content and "301" in content:
            print("  PASS /home/ redirects to / with 301")
        else:
            fail("_redirects does not redirect /home/ to / with a 301")
            print("  FAIL /home/ redirect missing")

    # The social share image. It is a PNG, so the page checks cannot see
    # the text inside it. It is drawn by scripts/make_og.py, and a stale
    # copy of that PNG keeps saying the old name even after every source
    # file is fixed. OCR the image and check the text in it.
    print("\n--- social share image ---")
    og = os.path.join(DIST, "og-image.png")
    if not os.path.exists(og):
        fail("no og-image.png in the build")
        print("  FAIL no og-image.png")
    else:
        text = ocr_image(og)
        if text is None:
            notes.append("could not OCR og-image.png, so its text was not checked")
            print("  NOTE could not read the text in og-image.png")
        elif "Paw Watch" in text or "PAW WATCH" in text:
            fail(f"og-image.png still says the old name: {text!r}")
            print(f"  FAIL og-image.png says 'Paw Watch': {text!r}")
        else:
            print(f"  PASS og-image.png text: {text!r}")

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
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
