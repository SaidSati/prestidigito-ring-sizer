"""Gera os ícones PNG do PWA a partir de primitivas (anel + estrela), com
supersampling 4x para bordas suaves. Paleta igual ao app."""
import math
from PIL import Image, ImageDraw

BG = (22, 18, 15)            # #16120f
GOLD = (197, 154, 84)        # tom médio do gradiente dourado (#c59a54)
GOLD_HI = (228, 205, 151)
SS = 4                       # fator de supersampling

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def rounded_rect_mask(size, radius):
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    return m

def star_points(cx, cy, ro, ri, n=5, rot=-math.pi / 2):
    pts = []
    for i in range(n * 2):
        r = ro if i % 2 == 0 else ri
        a = rot + i * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def ring_gradient(img, cx, cy, r, width, c0, c1):
    """Desenha um anel com gradiente diagonal aproximado por arcos coloridos."""
    d = ImageDraw.Draw(img)
    steps = 180
    for k in range(steps):
        a0 = 360 * k / steps
        a1 = 360 * (k + 1) / steps + 1
        # posição angular -> t do gradiente diagonal (canto sup-esq -> inf-dir)
        ang = math.radians(a0)
        t = (math.cos(ang) + math.sin(ang) + 2) / 4
        col = lerp(c0, c1, t)
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=col, width=width)

def build(size, maskable):
    S = size * SS
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    # fundo
    bg = Image.new("RGBA", (S, S), BG + (255,))
    if maskable:
        img = Image.alpha_composite(img, bg)
        content = 0.80          # zona segura do maskable
    else:
        mask = rounded_rect_mask(S, int(112 * S / 512))
        img.paste(bg, (0, 0), mask)
        content = 1.0

    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sc = S / 512 * content
    off = S * (1 - content) / 2
    def X(v): return off + v * sc
    cx, cy = X(256), X(276)

    ring_gradient(layer, cx, cy, int(118 * sc), max(1, int(16 * sc)), GOLD_HI, (138, 106, 49))
    # anel interno fino
    d = ImageDraw.Draw(layer)
    r2 = int(82 * sc)
    d.arc([cx - r2, cy - r2, cx + r2, cy + r2], 0, 360, fill=GOLD + (130,), width=max(1, int(6 * sc)))
    # estrela
    pts = star_points(X(256), X(150), 60 * sc, 25 * sc)
    d.polygon(pts, fill=GOLD_HI)

    img = Image.alpha_composite(img, layer)
    out = img.resize((size, size), Image.LANCZOS)
    return out.convert("RGB") if not maskable else out.convert("RGB")

for name, size, mask in [("icon-192.png", 192, False), ("icon-512.png", 512, False),
                         ("icon-180.png", 180, False), ("icon-maskable-512.png", 512, True)]:
    build(size, mask).save(name)
    print("ok", name)
