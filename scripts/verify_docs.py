#!/usr/bin/env python3
"""
Check that a built page says exactly what the source markdown says.

The source copy is the truth. This walks the built HTML, pulls out the
visible text, and compares it to the markdown with the markup removed.
Any word that differs is a failure.

Usage:
    python scripts/verify_docs.py [dist-directory]
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DIST = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(SITE, "dist")
DOCS = os.path.join(SITE, "src", "content-docs")

# The page file, and the built page it should match.
PAGES = {
    "privacy-policy": "privacy-policy",
    "terms": "terms",
    "support": "support",
}

failures = []
notes = []


def strip_markdown(text):
    """Turn markdown into the words a reader sees."""
    out = text
    # images
    out = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", out)
    # links -> the visible text
    out = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", out)
    # code fences
    out = re.sub(r"```.*?```", " ", out, flags=re.S)
    # inline code
    out = re.sub(r"`([^`]+)`", r"\1", out)
    # bold / italic markers
    out = re.sub(r"\*\*([^*]+)\*\*", r"\1", out)
    out = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", out)
    # headings, list bullets, blockquote markers
    out = re.sub(r"^#{1,6}\s+", "", out, flags=re.M)
    out = re.sub(r"^\s*[-*+]\s+", "", out, flags=re.M)
    out = re.sub(r"^\s*\d+\.\s+", "", out, flags=re.M)
    out = re.sub(r"^\s*>\s?", "", out, flags=re.M)
    # table pipes
    out = re.sub(r"^\|.*$", " ", out, flags=re.M)
    return out


def html_to_text(page_html):
    """Pull the visible text out of a built page.

    Block level tags become a space, because they separate words.
    Inline tags become nothing, because they do not: <strong>Email:</strong>
    reads as "Email:", and turning the tag into a space would read as
    "Email :".
    """
    body = page_html
    # Drop the parts that are not the page content.
    body = re.sub(r"<script.*?</script>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<style.*?</style>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<head.*?</head>", " ", body, flags=re.S | re.I)

    # Block level tags separate words.
    block = (r"p|div|section|article|header|footer|main|nav|aside|"
             r"h1|h2|h3|h4|h5|h6|ul|ol|li|dl|dt|dd|table|tr|td|th|"
             r"thead|tbody|blockquote|hr|br|figure|figcaption|address|pre")
    body = re.sub(rf"</?({block})(\s[^>]*)?>", " ", body, flags=re.I)

    # Everything else is inline and does not separate words.
    body = re.sub(r"<[^>]+>", "", body)
    body = html.unescape(body)
    return body


def words(text):
    """The words of a text, normalised for comparison."""
    return re.sub(r"\s+", " ", text).strip()


def main():
    for page, doc in PAGES.items():
        built = os.path.join(DIST, page, "index.html")
        source = os.path.join(DOCS, f"{doc}.md")

        if not os.path.exists(built):
            failures.append(f"{page}: no built page at {built}")
            print(f"  FAIL {page}: not built")
            continue
        if not os.path.exists(source):
            failures.append(f"{page}: no source copy at {source}")
            print(f"  FAIL {page}: no source copy")
            continue

        page_html = open(built, encoding="utf-8").read()
        md = open(source, encoding="utf-8").read()

        # The page's own content area only, so the shared header and
        # footer do not pollute the comparison.
        m = re.search(r"<section[^>]*>(.*?)</section>", page_html, re.S)
        if m:
            content_html = m.group(1)
        else:
            content_html = page_html
            notes.append(f"{page}: no <section> found, compared the whole page")

        got = words(html_to_text(content_html))
        want = words(strip_markdown(md))

        print(f"=== {page} ===")
        print(f"  built words: {len(got.split())}")
        print(f"  source words: {len(want.split())}")

        if got == want:
            print("  PASS the page says exactly what the source says")
        else:
            got_w = got.split()
            want_w = want.split()
            first_diff = None
            for i in range(max(len(got_w), len(want_w))):
                g = got_w[i] if i < len(got_w) else "<missing>"
                w = want_w[i] if i < len(want_w) else "<extra>"
                if g != w:
                    first_diff = (i, g, w)
                    break
            if first_diff:
                i, g, w = first_diff
                print(f"  FAIL text differs at word {i}")
                print(f"       built:  {got_w[max(0,i-6):i+8]}")
                print(f"       source: {want_w[max(0,i-6):i+8]}")
            failures.append(f"{page}: built text does not match the source copy")
        print()

    print("--- summary ---")
    if failures:
        for f in failures:
            print(f"  FAIL {f}")
        return 1
    print("  PASS every page matches its source copy word for word")
    return 0


if __name__ == "__main__":
    sys.exit(main())
