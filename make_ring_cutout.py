"""Cut the ring out of Frontal.jpeg into a transparent PNG for the AR overlay.
The background is light gray and the ring is silver (also gray), so a color key
would eat the ring. Instead we flood-fill from the borders: the fill spreads
through the connected background and stops at the ring's contrasting edge."""
from PIL import Image, ImageDraw, ImageFilter

SRC = "assets/ring/Frontal.jpeg"
OUT = "assets/ring-cutout.png"
THRESH = 38          # luminance tolerance for "this is still background"
SENT = (255, 0, 255) # sentinel marking background

im = Image.open(SRC).convert("RGB")
W, H = im.size
work = im.copy()

# seed points all around the border (gradient bg needs many seeds)
seeds = []
for i in range(0, W, 40):
    seeds += [(i, 2), (i, H - 3)]
for j in range(0, H, 40):
    seeds += [(2, j), (W - 3, j)]
for sx, sy in seeds:
    px = work.getpixel((min(sx, W - 1), min(sy, H - 1)))
    if px == SENT:
        continue
    ImageDraw.floodfill(work, (min(sx, W - 1), min(sy, H - 1)), SENT, thresh=THRESH)

# binary mask: white where NOT background, black where background
mask = Image.new("RGB", (W, H), (0, 0, 0))
mpx = mask.load(); wpx = work.load()
for y in range(H):
    for x in range(W):
        if wpx[x, y] != SENT:
            mpx[x, y] = (255, 255, 255)
# keep only the ring: flood the opaque component containing the image center
KEEP = (0, 255, 0)
ImageDraw.floodfill(mask, (W // 2, H // 2), KEEP, thresh=10)
alpha = Image.new("L", (W, H), 0)
apx = alpha.load(); mpx = mask.load()
for y in range(H):
    for x in range(W):
        if mpx[x, y] == KEEP:
            apx[x, y] = 255
# soften the matte edge a touch
alpha = alpha.filter(ImageFilter.GaussianBlur(1.0))

out = im.convert("RGBA")
out.putalpha(alpha)
bbox = alpha.getbbox()
if bbox:
    out = out.crop(bbox)
# downscale for the app (overlay never needs >600px wide)
if out.width > 600:
    out = out.resize((600, round(out.height * 600 / out.width)), Image.LANCZOS)
out.save(OUT)
print("ok", OUT, out.size)
