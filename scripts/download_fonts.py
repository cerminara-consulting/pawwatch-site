#!/usr/bin/env python3
"""
Download the Fraunces and Inter woff2 files the site uses, so the site
can serve them itself instead of asking Google for them.

Both families are SIL Open Font License. The license text is downloaded
alongside the fonts, because the OFL requires the license to ship with
the fonts.

Fraunces and Inter are variable fonts: Google's CSS points every weight
of a style at ONE file, so one file per (family, style, subset) covers
all the weights in use. The site uses Fraunces normal and italic, and
Inter normal.

Two subsets per style: latin for the page text, latin-ext so accented
characters in names and addresses render in the right typeface instead
of falling back to a system font.

This uses urllib rather than curl because curl's -o misbehaves writing
into this directory on this Windows host.

Usage:
    python scripts/download_fonts.py
"""
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
FONT_DIR = os.path.join(SITE, "public", "fonts")
LICENSE_DIR = os.path.join(FONT_DIR, "licenses")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

GS = "https://fonts.gstatic.com/s"
GH = "https://raw.githubusercontent.com/google/fonts/main/ofl"

# (local name, url)
FILES = [
    ("fraunces-latin.woff2",
     f"{GS}/fraunces/v38/6NU78FyLNQOQZAnv9bYEvDiIdE9Ea92uemAk_WBq8U_9v0c2Wa0KxC9TeA.woff2"),
    ("fraunces-latin-ext.woff2",
     f"{GS}/fraunces/v38/6NU78FyLNQOQZAnv9bYEvDiIdE9Ea92uemAk_WBq8U_9v0c2Wa0KxCFTeO-U.woff2"),
    ("fraunces-italic-latin.woff2",
     f"{GS}/fraunces/v38/6NU58FyLNQOQZAnv9ZwNjucMHVn85Ni7emAe9lKqZTnbB-gzTK0K1ChjeveQ.woff2"),
    ("fraunces-italic-latin-ext.woff2",
     f"{GS}/fraunces/v38/6NU58FyLNQOQZAnv9ZwNjucMHVn85Ni7emAe9lKqZTnbB-gzTK0K1ChjdPeQ_5Y.woff2"),
    ("inter-latin.woff2",
     f"{GS}/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2"),
    ("inter-latin-ext.woff2",
     f"{GS}/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa25L7SUc.woff2"),
]

WOFF2_SIG = b"wOF2"


def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    with open(dest, "wb") as f:
        f.write(data)
    return data


def main():
    os.makedirs(LICENSE_DIR, exist_ok=True)

    print("== downloading font files ==")
    for name, url in FILES:
        dest = os.path.join(FONT_DIR, name)
        try:
            data = fetch(url, dest)
        except Exception as e:
            print(f"FAIL: {name}: {e}")
            return 1
        ok = data[:4] == WOFF2_SIG
        print(f"  {name:<32} {len(data):>7} bytes  sig={data[:4]!r}"
              f"  {'OK' if ok else 'NOT A WOFF2'}")
        if not ok:
            print(f"FAIL: {name} is not a woff2 file.")
            return 1

    print()
    print("== downloading the SIL Open Font License text ==")
    for fam in ("fraunces", "inter"):
        dest = os.path.join(LICENSE_DIR, f"{fam}-OFL.txt")
        try:
            data = fetch(f"{GH}/{fam}/OFL.txt", dest)
        except Exception as e:
            print(f"FAIL: {fam}-OFL.txt: {e}")
            return 1
        head = data[:2000].decode("utf-8", "replace")
        # The OFL text starts with a copyright line for the font project,
        # so the licence name appears a few lines in, not on line 1.
        ok = "SIL Open Font License" in head
        print(f"  {fam}-OFL.txt {'OK' if ok else 'UNEXPECTED'} ({len(data)} bytes)")
        if not ok:
            print(f"FAIL: {fam}-OFL.txt does not look like the OFL.")
            print(head[:300])
            return 1

    print()
    print("== done ==")
    total = 0
    for name, _ in FILES:
        p = os.path.join(FONT_DIR, name)
        total += os.path.getsize(p)
        print(f"  {name:<34} {os.path.getsize(p):>7}")
    print(f"  {'TOTAL':<34} {total:>7} bytes ({total/1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
