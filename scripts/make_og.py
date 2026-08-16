#!/usr/bin/env python3
"""Regenerate pawwatch-site og-image.png \u2014 PIL + Fraunces (variable, set axis weight)."""
from PIL import Image, ImageDraw, ImageFont
import os, sys

W, H = 1200, 630

# PawWatch brand palette (from src/layouts/Layout.astro)
NAVY        = (24, 61, 98, 255)        # #183d62 page accent
CREAM       = (250, 243, 239, 255)     # #faf3ef page bg
INK         = (26, 26, 26, 255)        # body text
INK_SOFT    = (74, 85, 99, 255)        # muted
TEAL        = (74, 139, 140, 255)      # #4a8b8c accent
RULE        = (216, 207, 196, 255)     # #d8cfc4

FONT_DIR = r"C:\Users\jmcer\AppData\Local\Temp\fonts"
FRAUNCES_VAR    = os.path.join(FONT_DIR, "Fraunces[SOFT,WONK,opsz,wght].ttf")
FRAUNCES_ITALIC = os.path.join(FONT_DIR, "Fraunces-Italic[SOFT,WONK,opsz,wght].ttf")

# Variable font \u2014 set weight axis
def font_600(path, size):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_name("SemiBold")  # wght 600
    except (AttributeError, OSError, ValueError):
        pass  # fallback to default
    return f

def font_reg_italic(path, size):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_name("Italic")
    except (AttributeError, OSError, ValueError):
        pass
    return f

def font_semi_italic(path, size):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_name("SemiBold Italic")
    except (AttributeError, OSError, ValueError):
        pass
    return f

# --- canvas --------------------------------------------------------------
img = Image.new("RGBA", (W, H), CREAM)
d = ImageDraw.Draw(img)

# Top decorative rule across full width
d.rectangle([(0, 0), (W, 12)], fill=NAVY)

# Eyebrow (top, italic small caps)
f_eyebrow = font_reg_italic(FRAUNCES_ITALIC, 22)
d.text((80, 50), "PAW WATCH \u00b7 NEIGHBORHOOD PET SAFETY", font=f_eyebrow, fill=TEAL)

# H1 \u2014 measure first, then wrap to fit. Aim for max \u2248880px wide.
f_h1 = font_600(FRAUNCES_VAR, 78)
h1_lines = ["Lost pet?", "Found pet?", "Lost & found."]  # playful three-beat
y = 130
for line in h1_lines:
    bbox = d.textbbox((0, 0), line, font=f_h1)
    text_w = bbox[2] - bbox[0]
    print(f"h1 line '{line}': width={text_w}px")
    d.text((80, y), line, font=f_h1, fill=INK)
    y += 90  # ~1.15x font size for line height

# Subhead (italic, muted)
f_sub = font_reg_italic(FRAUNCES_ITALIC, 32)
sub_y = y + 12
d.text((80, sub_y), "PawWatch crowdsources sightings in your neighborhood", font=f_sub, fill=INK_SOFT)
d.text((80, sub_y + 48), "so a lost pet gets home faster.", font=f_sub, fill=INK_SOFT)

# URL footer (italic, navy)
f_url = font_600(FRAUNCES_VAR, 26)
d.text((80, sub_y + 48 + 52), "PAW-WATCH.APP", font=f_url, fill=NAVY)

# Brand mark (top-right) \u2014 navy rounded square + cream paw print
mark_size, mark_radius = 130, 28
mx, my = W - 80 - mark_size, 50
d.rounded_rectangle((mx, my, mx + mark_size, my + mark_size),
                    radius=mark_radius, fill=NAVY)
# paw emoji won't render in PIL on bare windows. Use a simple "PW" wordmark:
f_pw = font_600(FRAUNCES_VAR, 56)
bbox = d.textbbox((0, 0), "PW", font=f_pw)
pw_w, pw_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
d.text((mx + (mark_size - pw_w) // 2 - bbox[0],
        my + (mark_size - pw_h) // 2 - bbox[1] - 4),
       "PW", font=f_pw, fill=CREAM)

# Bottom rule (mirror top)
d.rectangle([(0, H - 12), (W, H)], fill=NAVY)

# --- save (script-relative path \u2014 see skill pitfall #2) ---
out = os.path.join(os.path.dirname(__file__), "..", "public", "og-image.png")
out = os.path.normpath(out)
os.makedirs(os.path.dirname(out), exist_ok=True)
img.convert("RGB").save(out, "PNG", optimize=True)
print(f"\nwrote {out}  ({os.path.getsize(out)} bytes)")
