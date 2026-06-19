"""Cut all product angles into transparent PNGs for the hero gallery.
Same border flood-fill + keep-component approach as the AR cutout, generalized."""
import math, os
from PIL import Image, ImageDraw, ImageFilter

SRCDIR = "assets/ring"
OUTDIR = "assets"
THRESH = 38
SENT = (255, 0, 255)

# order: front first, then angles (front is the AR/primary cutout too)
FILES = [
    "Frontal.jpeg",
    "WhatsApp Image 2026-06-19 at 13.23.49.jpeg",
    "WhatsApp Image 2026-06-19 at 13.23.49 (1).jpeg",
    "WhatsApp Image 2026-06-19 at 13.23.49 (2).jpeg",
    "WhatsApp Image 2026-06-19 at 13.23.50.jpeg",
]

def cut(path):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    work = im.copy()
    seeds = []
    for i in range(0, W, 40): seeds += [(i, 2), (i, H - 3)]
    for j in range(0, H, 40): seeds += [(2, j), (W - 3, j)]
    for sx, sy in seeds:
        x, y = min(sx, W - 1), min(sy, H - 1)
        if work.getpixel((x, y)) != SENT:
            ImageDraw.floodfill(work, (x, y), SENT, thresh=THRESH)
    # binary mask of non-background
    mask = Image.new("RGB", (W, H), (0, 0, 0)); mp = mask.load(); wp = work.load()
    sx = sy = n = 0
    for y in range(H):
        for x in range(W):
            if wp[x, y] != SENT:
                mp[x, y] = (255, 255, 255); sx += x; sy += y; n += 1
    # seed the keep-flood at the centroid of opaque pixels (falls in the solid onyx face)
    cx, cy = (int(sx / n), int(sy / n)) if n else (W // 2, H // 2)
    if mask.getpixel((cx, cy)) == (0, 0, 0): cx, cy = W // 2, H // 2
    ImageDraw.floodfill(mask, (cx, cy), (0, 255, 0), thresh=10)
    alpha = Image.new("L", (W, H), 0); ap = alpha.load(); mp = mask.load()
    for y in range(H):
        for x in range(W):
            if mp[x, y] == (0, 255, 0): ap[x, y] = 255
    alpha = alpha.filter(ImageFilter.GaussianBlur(1.0))
    out = im.convert("RGBA"); out.putalpha(alpha)
    bb = alpha.getbbox()
    if bb: out = out.crop(bb)
    if out.width > 620: out = out.resize((620, round(out.height * 620 / out.width)), Image.LANCZOS)
    return out

frames = []
for idx, f in enumerate(FILES, 1):
    p = os.path.join(SRCDIR, f)
    if not os.path.exists(p):
        print("skip missing", f); continue
    img = cut(p); img.save(os.path.join(OUTDIR, f"ring-{idx}.png"))
    frames.append(img); print("ok", f"ring-{idx}.png", img.size)

# primary cutout (front) reused by the AR overlay
frames[0].save(os.path.join(OUTDIR, "ring-cutout.png"))

# contact sheet for review (on magenta to see edges)
cell = 300
sheet = Image.new("RGB", (cell * len(frames), cell), (255, 0, 255))
for i, im in enumerate(frames):
    sc = min(cell / im.width, cell / im.height) * 0.92
    r = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    bg = Image.new("RGBA", (cell, cell), (255, 0, 255, 255))
    bg.alpha_composite(r, ((cell - r.width) // 2, (cell - r.height) // 2))
    sheet.paste(bg.convert("RGB"), (i * cell, 0))
sheet.save(os.path.join(OUTDIR, "_frames_check.png"))
print("contact sheet ->", "assets/_frames_check.png")
