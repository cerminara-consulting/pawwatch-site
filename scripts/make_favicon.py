#!/usr/bin/env python3
"""Regenerate Paw Watch site favicon assets from the master logo PNG.

Source: C:\\Users\\jmcer\\pawwatch\\assets\\images\\logo-new.png
       (1024x1024 RGBA, navy/teal pin-paw-dog mark on transparent)

Per John's directive, the favicon is the master logo composited onto a
white background. Outputs:

  - public/favicon.svg        — vector, mark only on white (no padding/bleed)
  - public/favicon-32.png     — modern browser tab, 32x32
  - public/apple-touch-icon.png — iOS home screen, 180x180

The SVG mirrors the mark exactly (no extra padding) because SVG favicons
render at the size the browser picks; the PNGs include ~8% white bleed
so OS-level chrome (rounded squares, circular app icons) doesn't crop
into the mark.
"""
from PIL import Image
import os
import sys

SRC = r"C:\Users\jmcer\pawwatch\assets\images\logo-new.png"
PUBLIC = os.path.join(os.path.dirname(__file__), "..", "public")
PUBLIC = os.path.normpath(PUBLIC)

WHITE = (255, 255, 255, 255)


def load_on_white(path, target_px, bleed_pct=0.0):
    """Load `path`, composite onto a white `target_px x target_px` canvas.

    `bleed_pct` shrinks the mark to leave that fraction of padding on
    each side (0.08 = 8% inset, used for OS-chrome cropping safety).
    """
    im = Image.open(path).convert("RGBA")
    # scale so the mark's bounding box (the whole 1024x1024) fills
    # (1 - 2*bleed_pct) of the target canvas.
    fill = target_px * (1.0 - 2 * bleed_pct)
    scaled_w = int(round(fill))
    scaled = im.resize((scaled_w, scaled_w), Image.LANCZOS)

    canvas = Image.new("RGBA", (target_px, target_px), WHITE)
    offset = (target_px - scaled_w) // 2
    canvas.paste(scaled, (offset, offset), scaled)
    return canvas


def save_ico(png_im, path, size=32):
    """Save an ICO with a single 32x32 layer (modern browsers all accept PNG-in-ICO)."""
    img32 = png_im.resize((size, size), Image.LANCZOS)
    img32.save(path, format="ICO", sizes=[(size, size)])


# --- favicon.svg (vector) ---
# Embed a small rasterized copy of the mark (white background baked in,
# 256x256, ~10 KB) inside a minimal SVG. Browsers honor data-URI images
# in SVG favicons, and shipping a sub-20-KB file keeps link unfurlers
# (Discord, Twitter, Slack, iMessage) willing to actually fetch it.
mark = Image.open(SRC).convert("RGBA")
# bake transparency into white at 256x256 — small enough for any browser
# to render crisply, big enough to scale up without visible pixelation.
mark_small = mark.resize((256, 256), Image.LANCZOS)
bg = Image.new("RGBA", (256, 256), WHITE)
bg.alpha_composite(mark_small)

import io, base64
buf = io.BytesIO()
bg.convert("RGB").save(buf, format="PNG", optimize=True)
mark_b64 = base64.b64encode(buf.getvalue()).decode("ascii")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <rect width="256" height="256" fill="#FFFFFF"/>
  <image href="data:image/png;base64,{mark_b64}" width="256" height="256"/>
</svg>
'''
with open(os.path.join(PUBLIC, "favicon.svg"), "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote favicon.svg ({os.path.getsize(os.path.join(PUBLIC, 'favicon.svg'))} bytes)")

# --- favicon-32.png (modern browser tab, 32x32) ---
fav32 = load_on_white(SRC, 32, bleed_pct=0.0).convert("RGB")
fav32.save(os.path.join(PUBLIC, "favicon-32.png"), "PNG", optimize=True)
print(f"wrote favicon-32.png ({os.path.getsize(os.path.join(PUBLIC, 'favicon-32.png'))} bytes)")

# --- favicon.ico (legacy / Windows pin / some browsers) ---
# Write a multi-size ICO so browser tab (16), bookmark bar (32), and
# taskbar shortcut (48) all get a clean asset. Modern browsers prefer
# favicon-32.png / favicon.svg, but having a real ICO costs ~3 KB and
# avoids the "blank tab on IE/old Edge" footgun.
ico16 = load_on_white(SRC, 16, bleed_pct=0.0).convert("RGB")
ico32 = load_on_white(SRC, 32, bleed_pct=0.0).convert("RGB")
ico48 = load_on_white(SRC, 48, bleed_pct=0.0).convert("RGB")
ico48.save(
    os.path.join(PUBLIC, "favicon.ico"),
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48)],
    append_images=[ico16, ico32],
)
print(f"wrote favicon.ico ({os.path.getsize(os.path.join(PUBLIC, 'favicon.ico'))} bytes)")

# --- apple-touch-icon.png (iOS home screen, 180x180 with 8% bleed) ---
apple = load_on_white(SRC, 180, bleed_pct=0.08).convert("RGB")
apple.save(os.path.join(PUBLIC, "apple-touch-icon.png"), "PNG", optimize=True)
print(f"wrote apple-touch-icon.png ({os.path.getsize(os.path.join(PUBLIC, 'apple-touch-icon.png'))} bytes)")