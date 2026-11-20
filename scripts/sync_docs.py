#!/usr/bin/env python3
"""
Sync the site pages from the copy in the iOS repo.

The page copy lives in the private repo cerminara-consulting/pawwatch-ios,
folder docs/site/. This script fetches those files with `gh api` and
writes the processed versions into src/content-docs/, which the Astro
pages import.

READ ONLY against pawwatch-ios. This script only ever issues GET
requests. It never pushes, never opens a pull request, never writes to
that repo.

Three transforms are applied, and only these three:
  1. HTML comments are removed. They are notes for John, not page copy.
  2. [PUBLISH DATE] becomes today's date, in the ISO form the current
     pages use.
  3. Bare email addresses become mailto links, and the bare policy URLs
     become links. The visible words are not changed.

Everything else is word for word.

Usage:
    python scripts/sync_docs.py            # fetch and write
    python scripts/sync_docs.py --check    # verify the committed files
                                           # match a fresh fetch, write nothing
"""
import base64
import datetime
import json
import os
import re
import subprocess
import sys

REPO = "cerminara-consulting/pawwatch-ios"
REF = "637ad33"
SOURCE_DIR = "docs/site"

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
OUT_DIR = os.path.join(SITE, "src", "content-docs")

# The pages, and the file each one comes from.
PAGES = {
    "privacy-policy": "privacy-policy.md",
    "terms": "terms.md",
    "support": "support.md",
}

# Bare URLs in the copy that should be links. The visible text stays
# exactly as written; only the href is added.
URLS = {
    "apple.com/legal/internet-services/itunes/dev/stdeula/":
        "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/",
    "apple.com/legal/privacy":
        "https://www.apple.com/legal/privacy/",
    "openai.com/policies/privacy-policy":
        "https://openai.com/policies/privacy-policy",
    "resend.com/legal/privacy-policy":
        "https://resend.com/legal/privacy-policy",
    "supabase.com/privacy":
        "https://supabase.com/privacy",
    # Our own policy page.
    "paw-watch.app/privacy-policy/":
        "/privacy-policy/",
}


def gh_get(path, ref):
    """Fetch a file from the iOS repo. Read only."""
    out = subprocess.run(
        ["gh", "api", f"repos/{REPO}/contents/{path}?ref={ref}"],
        capture_output=True, text=True, check=True).stdout
    data = json.loads(out)
    return base64.b64decode(data["content"]).decode("utf-8")


def strip_comments(md):
    """Remove HTML comments. They are notes for John."""
    return re.sub(r"<!--.*?-->", "", md, flags=re.S)


def set_publish_date(md, date_str):
    """Replace the [PUBLISH DATE] placeholder."""
    if "[PUBLISH DATE]" not in md:
        return md
    return md.replace("[PUBLISH DATE]", date_str)


def linkify_emails(md):
    """Turn bare email addresses into mailto links.

    The visible text is unchanged, only the link is added. An address
    that is already part of a link is left alone.
    """
    pattern = re.compile(
        r"(?<![\w/.\-])([A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,})(?![/\w])")
    return pattern.sub(r"[\1](mailto:\1)", md)


def linkify_urls(md):
    """Turn the bare policy URLs into links, longest first."""
    for bare in sorted(URLS, key=len, reverse=True):
        href = URLS[bare]
        # The URL must not be followed by more URL characters, so
        # "supabase.com/privacy." links the URL and leaves the full stop
        # outside the link.
        pattern = re.compile(re.escape(bare) + r"(?![\w/\-])")
        md = pattern.sub(f"[{bare}]({href})", md)
    return md


# A line that ends a sentence. If a line ends with one of these, it is
# the end of the sentence, not the start of a new row.
SENTENCE_END = (".", "?", "!", ":", ";")


def hard_break_rows(md):
    """
    Keep the rows of a multi-line block on separate lines.

    Markdown treats a plain newline inside a paragraph as a soft break,
    and renders it as a space. So a block written one row per line comes
    out as one run-on line. The copy writes the mailing address that
    way, so it would render as "Cerminara Consulting LLC Attn: PawWatch
    PO Box 23 Studley, VA 23162-9997 United States" on one line, which
    is worse than the page it replaces.

    Two trailing spaces make a markdown hard break, and Astro renders
    that as a <br>. So a row gets a hard break when the row after it
    starts a new row rather than continuing the sentence.

    A row continues a sentence when the next line starts with a lower
    case letter or a continuation mark, which is what a paragraph of
    prose that has been wrapped by hand looks like. The copy does not
    wrap its prose, but this keeps the rule safe if it ever does.

    List items and headings are left alone.
    """
    blocks = re.split(r"(\n\s*\n)", md)
    out = []
    for i, block in enumerate(blocks):
        # Even indices are content, odd indices are the separators.
        if i % 2 == 1 or not block.strip():
            out.append(block)
            continue

        lines = block.split("\n")
        if len(lines) < 2:
            out.append(block)
            continue

        # Skip lists, headings, tables and code. A bold label such as
        # "**Mailing address**" is not a list item: it starts with "**",
        # not "* ", so it is not skipped.
        first = lines[0].lstrip()
        is_list = (re.match(r"^[-*+]\s", first)
                   or re.match(r"^\d+\.\s", first))
        if (is_list or first.startswith(("#", "|", "```", ">"))):
            out.append(block)
            continue

        for idx in range(len(lines) - 1):
            line = lines[idx]
            nxt = lines[idx + 1].strip()
            if not line.strip() or not nxt:
                continue
            stripped = line.rstrip()
            # Already a hard break, or the end of a sentence.
            if stripped.endswith("  ") or stripped.endswith(SENTENCE_END):
                continue
            # The next line continues the sentence.
            if nxt[0].islower() or nxt[0] in ",;)]}\"'":
                continue
            lines[idx] = stripped + "  "

        out.append("\n".join(lines))
    return "".join(out)


def process(md, date_str):
    out = strip_comments(md)
    out = set_publish_date(out, date_str)
    out = linkify_emails(out)
    out = linkify_urls(out)
    out = hard_break_rows(out)
    # Collapse the blank lines the comment removal leaves behind, and
    # make sure the file ends with exactly one newline.
    out = re.sub(r"\n{3,}", "\n\n", out)
    out = out.strip() + "\n"
    return out


def main():
    check_only = "--check" in sys.argv
    date_str = datetime.date.today().isoformat()

    print(f"source: {REPO}@{REF} {SOURCE_DIR}")
    print(f"publish date: {date_str}")
    print()

    os.makedirs(OUT_DIR, exist_ok=True)
    problems = []

    for page, filename in PAGES.items():
        raw = gh_get(f"{SOURCE_DIR}/{filename}", REF)
        processed = process(raw, date_str)
        dest = os.path.join(OUT_DIR, f"{page}.md")

        if check_only:
            if not os.path.exists(dest):
                problems.append(f"{page}.md is missing")
                print(f"  {filename:<22} MISSING")
                continue
            current = open(dest, encoding="utf-8").read()
            if current != processed:
                problems.append(f"{page}.md is out of date")
                print(f"  {filename:<22} OUT OF DATE")
            else:
                print(f"  {filename:<22} up to date")
            continue

        with open(dest, "w", encoding="utf-8", newline="\n") as f:
            f.write(processed)
        print(f"  {filename:<22} -> src/content-docs/{page}.md "
              f"({len(processed)} bytes)")

    if check_only:
        if problems:
            print()
            for p in problems:
                print(f"  FAIL {p}")
            return 1
        print("\nAll page copy is in sync with the source.")
        return 0

    print("\nWritten. Now build and check:")
    print("  npm run build")
    print("  python scripts/verify_docs.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
