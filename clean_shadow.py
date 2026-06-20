"""Remove the residual contact shadow at the bottom of the ring cutout by
fading the alpha to 0 below the ring band, then re-cropping."""
from PIL import Image

im = Image.open("assets/ring-cutout.png").convert("RGBA")
W, H = im.size
px = im.load()
y0 = int(H * 0.86)   # start fading here (just below the band rim)
y1 = int(H * 0.96)   # fully transparent from here down
for y in range(y0, H):
    f = 0.0 if y >= y1 else 1 - (y - y0) / (y1 - y0)
    for x in range(W):
        r, g, b, a = px[x, y]
        px[x, y] = (r, g, b, int(a * f))

bb = im.split()[3].getbbox()
if bb:
    im = im.crop(bb)
im.save("assets/ring-cutout.png")

# review composite
bg = Image.new("RGBA", im.size, (255, 0, 255, 255))
Image.alpha_composite(bg, im).convert("RGB").save("assets/_chk.png")
print("done", im.size)
