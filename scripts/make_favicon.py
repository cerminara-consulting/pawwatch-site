#!/usr/bin/env python3
"""Regenerate Paw Watch site favicon assets from the master logo PNG.

Source: C:\\Users\\jmcer\\pawwatch\\assets\\images\\logo-new.png
       (1024x1024 RGBA, navy/teal pin-paw-dog mark on transparent,
        generous internal whitespace around the subject)

Per John's directive, the favicon is the master logo composited onto a
rounded-corner white card. Outputs:

  - public/favicon.svg        — vector, mark on white rounded card
  - public/favicon-32.png     — modern browser tab, 32x32
  - public/favicon.ico        — legacy / Windows, 16/32/48 multi-size
  - public/apple-touch-icon.png — iOS home screen, 180x180

The radius (18% of edge length) is chosen to match the site's brand
vocabulary — .wordmark-img and .card both use border-radius: 8px on
~44px elements, which is ~18%. At apple-touch-icon size that lands
close to iOS's own squircle mask; the 8% white bleed is still applied
so iOS's re-masking doesn't crop into the mark.
"""
from PIL import Image, ImageDraw
import os
import io
import base64

SRC = r"C:\Users\jmcer\pawwatch\assets\images\logo-new.png"
PUBLIC = os.path.join(os.path.dirname(__file__), "..", "public")
PUBLIC = os.path.normpath(PUBLIC)

WHITE = (255, 255, 255, 255)
CORNER_RADIUS_PCT = 0.12  # ~22px on 180, ~4px on 32 — reads as a rounded square, not a squircle


def load_on_white_rounded(path, target_px, bleed_pct=0.0, radius_pct=CORNER_RADIUS_PCT):
    """Load `path`, place it on a rounded-corner white `target_px x target_px`
    canvas with transparent corners outside the rounded rect.

    `bleed_pct` shrinks the mark to leave that fraction of padding on
    each side (e.g. 0.08 = 8% inset, used for iOS app-icon masking).
    `radius_pct` is the corner radius as a fraction of edge length.
    """
    im = Image.open(path).convert("RGBA")
    fill = int(round(target_px * (1.0 - 2 * bleed_pct)))
    scaled = im.resize((fill, fill), Image.LANCZOS)

    # Transparent canvas, paint a rounded white card onto it, then
    # composite the mark on top. Anything outside the rounded rect
    # stays transparent, so browser-tab backgrounds show through the
    # rounded corners.
    canvas = Image.new("RGBA", (target_px, target_px), (0, 0, 0, 0))
    radius = int(round(target_px * radius_pct))
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle(
        [(0, 0), (target_px - 1, target_px - 1)],
        radius=radius,
        fill=WHITE,
    )
    offset = (target_px - fill) // 2
    canvas.paste(scaled, (offset, offset), scaled)  # mask=scaled preserves RGBA alpha
    return canvas


def save_ico(path_out, sizes=(16, 32, 48)):
    """Save a multi-size ICO with one PNG-encoded frame per requested size.

    PIL's ICO writer silently drops appended frames when the base frame's
    declared `sizes` don't match every appended frame's pixel dimensions.
    Rather than fight that, build the ICO binary directly: an ICONDIR
    header + one ICONDIRENTRY per size + the PNG bytes for each frame
    concatenated. PNG-encoded ICO entries use width/height byte 0 to mean
    "256 or larger" — standard ICO encoding, supported by every modern
    browser, Windows, and macOS since 2007.
    """
    import struct

    # Build each frame as a rounded white card with the mark composited on top.
    frames = []
    for sz in sizes:
        frame = load_on_white_rounded(SRC, sz, bleed_pct=0.0).convert("RGBA")
        buf = io.BytesIO()
        # PNG with alpha — modern ICO readers (Win Vista+, all browsers,
        # macOS Safari) honor the alpha channel.
        frame.save(buf, format="PNG", optimize=True)
        frames.append((sz, buf.getvalue()))

    n = len(frames)
    # ICONDIR: reserved(2)=0 + type(2)=1 (ICO) + count(2)
    header = struct.pack("<HHH", 0, 1, n)
    # Each ICONDIRENTRY is 16 bytes; data region starts after header+entries
    offset = 6 + 16 * n
    entries = b""
    data = b""
    for sz, png_bytes in frames:
        # width/height bytes: 0 means 256; widths/heights >=256 not used here.
        w = sz & 0xFF
        h = sz & 0xFF
        # struct format: B(width) B(height) B(colors) B(reserved) H(planes) H(bpp) I(size) I(offset)
        entries += struct.pack(
            "<BBBBHHII", w, h, 0, 0, 1, 32, len(png_bytes), offset
        )
        data += png_bytes
        offset += len(png_bytes)

    with open(path_out, "wb") as fh:
        fh.write(header + entries + data)


# --- favicon.svg (vector) ---
# Draw the rounded white card as a vector <rect>, then composite the mark
# (on transparent) on top. The SVG itself stays small — the rasterized
# mark is 256x256 with no baked-in white background, so the corners of
# the data-URI PNG are transparent and the white rect's rounded corners
# show through.
mark = Image.open(SRC).convert("RGBA").resize((256, 256), Image.LANCZOS)
buf = io.BytesIO()
mark.save(buf, format="PNG", optimize=True)
mark_b64 = base64.b64encode(buf.getvalue()).decode("ascii")

# 18% of 256 = 46 (rounded). Matches the raster radius so SVG and PNG
# render identically.
svg_radius = int(round(256 * CORNER_RADIUS_PCT))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <rect width="256" height="256" rx="{svg_radius}" ry="{svg_radius}" fill="#FFFFFF"/>
  <image href="data:image/png;base64,{mark_b64}" width="256" height="256"/>
</svg>
'''
with open(os.path.join(PUBLIC, "favicon.svg"), "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote favicon.svg ({os.path.getsize(os.path.join(PUBLIC, 'favicon.svg'))} bytes)")

# --- favicon-32.png (modern browser tab, 32x32) ---
fav32 = load_on_white_rounded(SRC, 32, bleed_pct=0.0).convert("RGB")
fav32.save(os.path.join(PUBLIC, "favicon-32.png"), "PNG", optimize=True)
print(f"wrote favicon-32.png ({os.path.getsize(os.path.join(PUBLIC, 'favicon-32.png'))} bytes)")

# --- favicon.ico (legacy / Windows pin / some browsers) ---
save_ico(os.path.join(PUBLIC, "favicon.ico"), sizes=(16, 32, 48))
print(f"wrote favicon.ico ({os.path.getsize(os.path.join(PUBLIC, 'favicon.ico'))} bytes)")

# --- apple-touch-icon.png (iOS home screen, 180x180 with 8% bleed) ---
apple = load_on_white_rounded(SRC, 180, bleed_pct=0.08).convert("RGB")
apple.save(os.path.join(PUBLIC, "apple-touch-icon.png"), "PNG", optimize=True)
print(f"wrote apple-touch-icon.png ({os.path.getsize(os.path.join(PUBLIC, 'apple-touch-icon.png'))} bytes)")