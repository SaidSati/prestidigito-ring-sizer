"""Gera os ícones PNG do PWA OBVIOUS: hexágono (pointy-top) com furo circular,
preenchido com gradiente de brasa sobre obsidiana, com leve halo incandescente.
Supersampling 4x para bordas suaves."""
import math
from PIL import Image, ImageDraw, ImageFilter

BG = (10, 10, 12)            # #0a0a0c obsidiana
EMBER_HI = (255, 210, 122)   # #ffd27a
EMBER = (255, 90, 31)        # #ff5a1f
EMBER_DEEP = (196, 26, 8)    # #c41a08
SS = 4

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def ember_color(t):
    """t 0..1 -> deep red -> ember -> hot."""
    if t < 0.5:
        return lerp(EMBER_DEEP, EMBER, t / 0.5)
    return lerp(EMBER, EMBER_HI, (t - 0.5) / 0.5)

def hexagon(cx, cy, r):
    # pointy-top: vértices em -90, -30, 30, 90, 150, 210 graus
    return [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
            for a in (-90, -30, 30, 90, 150, 210)]

def rounded_mask(size, radius):
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    return m

def build(size, maskable):
    S = size * SS
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    bg = Image.new("RGBA", (S, S), BG + (255,))
    if maskable:
        img = Image.alpha_composite(img, bg)
        content = 0.74
    else:
        img.paste(bg, (0, 0), rounded_mask(S, int(112 * S / 512)))
        content = 0.92

    cx = cy = S / 2
    R = S * 0.5 * content
    hole = R * 0.56

    # gradiente de brasa pintado em faixa diagonal e recortado pela máscara do hexágono-com-furo
    grad = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    steps = 220
    for i in range(steps):
        y0 = int(S * i / steps)
        y1 = int(S * (i + 1) / steps) + 1
        gd.rectangle([0, y0, S, y1], fill=ember_color(i / steps) + (255,))

    mask = Image.new("L", (S, S), 0)
    md = ImageDraw.Draw(mask)
    md.polygon(hexagon(cx, cy, R), fill=255)
    md.ellipse([cx - hole, cy - hole, cx + hole, cy + hole], fill=0)  # furo

    # halo incandescente atrás do anel
    halo = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    hd.ellipse([cx - R * 1.05, cy - R * 1.05, cx + R * 1.05, cy + R * 1.05], fill=EMBER + (90,))
    halo = halo.filter(ImageFilter.GaussianBlur(S * 0.06))
    img = Image.alpha_composite(img, halo)

    grad.putalpha(mask)
    img = Image.alpha_composite(img, grad)

    return img.resize((size, size), Image.LANCZOS).convert("RGB")

for name, size, mask in [("icon-192.png", 192, False), ("icon-512.png", 512, False),
                         ("icon-180.png", 180, False), ("icon-maskable-512.png", 512, True)]:
    build(size, mask).save(name)
    print("ok", name)
