#!/usr/bin/env python3
"""
Apply the home page corrections from docs/site/home-corrections.md.

The corrections live in the iOS repo and name the live sentence and the
replacement for each one. This script applies them by exact string
match, and refuses to continue if a sentence is not found exactly once.

Only the sentences the corrections list are touched. Nothing else in the
file is changed.

Run with --check to see what would change without writing.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
TARGET = os.path.join(SITE, "src", "pages", "index.astro")
MOCKUP = os.path.join(SITE, "src", "components", "PhoneMockup.astro")

# Each entry: (file, old text, new text, what the correction is).
#
# The corrections table was written against the live site, which still
# said "Paw Watch". PR #1 already renamed it to "PawWatch", so the old
# text below uses the current spelling. The replacement text is the
# correction's own wording.
EDITS = [
    (
        TARGET,
        "        Built by Cerminara Consulting LLC. Free, no ads, no tracking, no\n"
        "        account required to browse the map.\n",
        "        Built by Cerminara Consulting LLC. Free, no ads, no tracking.\n",
        "1. drop \"no account required to browse the map\"",
    ),
    (
        TARGET,
        "          Color-coded pins for loose dogs, broken glass, aggressive\n"
        "          animals, and five more categories. Auto-expire after the danger\n"
        "          has passed — the map only shows what's still relevant.\n",
        "          Color-coded pins for aggressive and off-leash dogs, wildlife,\n"
        "          toxic hazards, hot pavement, and three more categories.\n"
        "          Auto-expire after the danger has passed — the map only shows\n"
        "          what's still relevant.\n",
        "2. the real hazard categories",
    ),
    (
        TARGET,
        "          Set your home once. When a new hazard appears within your\n"
        "          radius, PawWatch sends a quiet push — so you know before you\n"
        "          clip the leash.\n",
        "          Set your home once. When a new hazard appears within your\n"
        "          radius, PawWatch sends you a push, so you know before you clip\n"
        "          the leash.\n",
        "3. the push wording, and the dash removed",
    ),
    (
        TARGET,
        "        <strong>Location stays local.</strong> Your home radius is the\n"
        "        only location we store. Report coordinates are stored, but your\n"
        "        address is not.\n",
        "        <strong>You control your location.</strong> We store your home\n"
        "        point, the spot of each report you file, and the routes of walks\n"
        "        you choose to record, never the address you type. Your home and\n"
        "        your walks are visible only to you.\n",
        "4. what the app actually stores",
    ),
    (
        TARGET,
        "        <strong>Delete your account in-app.</strong> One tap in Profile,\n"
        "        your data is gone — profile, reports, walks, notification tokens.\n",
        "        <strong>Delete your account in-app.</strong> Open Account, tap\n"
        "        Delete account, and type \"delete\": your profile, photos, pets,\n"
        "        reports, walks, and notification tokens are gone.\n",
        "5. how account deletion actually works",
    ),
    (
        MOCKUP,
        "300m away · 4 min ago",
        "0.2 mi away · 4 min ago",
        "6. the mockup distance, in miles",
    ),
]


def main():
    check_only = "--check" in sys.argv
    texts = {}

    for path in (TARGET, MOCKUP):
        with open(path, encoding="utf-8") as f:
            texts[path] = f.read()

    problems = []
    for path, old, new, what in EDITS:
        count = texts[path].count(old)
        if count != 1:
            problems.append(f"{what}: found {count} matches, expected 1")
            print(f"  FAIL {what}: {count} matches, expected 1")
            continue
        if check_only:
            print(f"  would change: {what}")
            continue
        texts[path] = texts[path].replace(old, new)
        print(f"  applied: {what}")

    if problems:
        print()
        for p in problems:
            print(f"  FAIL {p}")
        return 1

    if check_only:
        print("\nNo changes written (--check).")
        return 0

    for path, text in texts.items():
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(f"  wrote {os.path.relpath(path, SITE)}")

    print("\nNote: correction 7 (\"Launching late August 2026\") is NOT applied.")
    print("The corrections file gives no replacement wording for it, only a note")
    print("to update it after launch, so it needs John's words.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
