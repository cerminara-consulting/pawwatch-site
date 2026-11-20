#!/usr/bin/env python3
"""
Download the Fraunces variable TTFs that scripts/make_og.py needs.

The OG image generator draws with the full variable font, so it needs the
TTF rather than the woff2 the site serves. This fetches them from the
google/fonts repository and puts them in the directory make_og.py
expects.

Usage:
    python scripts/fetch_og_fonts.py
"""
import os
import urllib.request

FONT_DIR = r"C:\Users\jmcer\AppData\Local\Temp\fonts"
BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl/fraunces"

FILES = [
    "Fraunces[SOFT,WONK,opsz,wght].ttf",
    "Fraunces-Italic[SOFT,WONK,opsz,wght].ttf",
]


def main():
    os.makedirs(FONT_DIR, exist_ok=True)
    for name in FILES:
        dest = os.path.join(FONT_DIR, name)
        if os.path.exists(dest) and os.path.getsize(dest) > 100_000:
            print(f"  {name}: already there ({os.path.getsize(dest)} bytes)")
            continue
        url = f"{BASE}/{urllib.parse.quote(name)}"
        print(f"  {name}: downloading...")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=60).read()
        if len(data) < 100_000:
            print(f"    FAIL: only {len(data)} bytes, that is not the font")
            return 1
        with open(dest, "wb") as f:
            f.write(data)
        print(f"    OK ({len(data)} bytes)")
    print(f"\nFonts are in {FONT_DIR}")
    return 0


if __name__ == "__main__":
    import urllib.parse
    raise SystemExit(main())
