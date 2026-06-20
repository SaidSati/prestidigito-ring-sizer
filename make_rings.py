"""Background-remove the 3 ring finishes with rembg (local U2-Net + alpha matting),
crop, downscale, and save transparent PNGs for the AR try-on color switcher."""
import os
from rembg import remove, new_session
from PIL import Image

SRC = "assets/ring"
JOBS = [("frontal.jpeg", "assets/ring-steel.png"),
        ("fosco.jpeg",   "assets/ring-graphite.png"),
        ("preto.jpeg",   "assets/ring-black.png")]

session = new_session()  # default u2net
frames = []
for src, out in JOBS:
    im = Image.open(os.path.join(SRC, src)).convert("RGB")
    cut = remove(im, session=session, alpha_matting=True,
                 alpha_matting_foreground_threshold=240,
                 alpha_matting_background_threshold=10,
                 alpha_matting_erode_size=10).convert("RGBA")
    bb = cut.split()[3].getbbox()
    if bb:
        cut = cut.crop(bb)
    if cut.width > 600:
        cut = cut.resize((600, round(cut.height * 600 / cut.width)), Image.LANCZOS)
    cut.save(out)
    frames.append((out, cut))
    print("ok", out, cut.size)

# contact sheet on magenta to inspect edges
cell = 300
sheet = Image.new("RGB", (cell * len(frames), cell), (255, 0, 255))
for i, (n, im) in enumerate(frames):
    sc = min(cell / im.width, cell / im.height) * 0.92
    r = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    bg = Image.new("RGBA", (cell, cell), (255, 0, 255, 255))
    bg.alpha_composite(r, ((cell - r.width) // 2, (cell - r.height) // 2))
    sheet.paste(bg.convert("RGB"), (i * cell, 0))
sheet.save("assets/_rings_check.png")
print("sheet -> assets/_rings_check.png")
