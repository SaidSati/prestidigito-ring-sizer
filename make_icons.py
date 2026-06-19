"""OBVIOUS PWA icons — pure black & white. Black field, white hexagon (pointy-top)
with a circular knockout. Supersampling 4x for clean edges."""
import math
from PIL import Image, ImageDraw

BLACK = (12, 12, 13)
WHITE = (255, 255, 255)
SS = 4

def hexagon(cx, cy, r):
    return [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
            for a in (-90, -30, 30, 90, 150, 210)]

def rounded_mask(size, radius):
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    return m

def build(size, maskable):
    S = size * SS
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    bg = Image.new("RGBA", (S, S), BLACK + (255,))
    if maskable:
        img = Image.alpha_composite(img, bg)
        content = 0.74
    else:
        img.paste(bg, (0, 0), rounded_mask(S, int(112 * S / 512)))
        content = 0.92

    cx = cy = S / 2
    R = S * 0.5 * content
    hole = R * 0.56

    mark = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    md = ImageDraw.Draw(mark)
    md.polygon(hexagon(cx, cy, R), fill=WHITE + (255,))
    img = Image.alpha_composite(img, mark)

    # knockout the circular hole back to the background
    hole_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hole_layer)
    hd.ellipse([cx - hole, cy - hole, cx + hole, cy + hole], fill=BLACK + (255,))
    img = Image.alpha_composite(img, hole_layer)

    return img.resize((size, size), Image.LANCZOS).convert("RGB")

for name, size, mask in [("icon-192.png", 192, False), ("icon-512.png", 512, False),
                         ("icon-180.png", 180, False), ("icon-maskable-512.png", 512, True)]:
    build(size, mask).save(name)
    print("ok", name)
