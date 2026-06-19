"""Generate the social share image (og-image.png, 1200x630) — B&W OBVIOUS brand."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BLACK = (12, 12, 13)
WHITE = (255, 255, 255)
GRAY = (150, 150, 156)

def font(paths, size):
    for p in paths:
        try: return ImageFont.truetype(p, size)
        except Exception: pass
    return ImageFont.load_default()

black_f = ["C:/Windows/Fonts/ariblk.ttf", "C:/Windows/Fonts/Arial Black.ttf"]
bold_f = ["C:/Windows/Fonts/arialbd.ttf"]
reg_f = ["C:/Windows/Fonts/arial.ttf"]

img = Image.new("RGB", (W, H), BLACK)
d = ImageDraw.Draw(img)

# hexagon mark (white, with circular hole) on the left
cx, cy, R = 300, H // 2, 190
pts = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a in (-90, -30, 30, 90, 150, 210)]
d.polygon(pts, fill=WHITE)
hole = R * 0.56
d.ellipse([cx - hole, cy - hole, cx + hole, cy + hole], fill=BLACK)

# text block on the right
tx = 560
d.text((tx, 188), "OBVIOUS", font=font(black_f, 96), fill=WHITE)
d.text((tx, 300), "Your exact fit.", font=font(black_f, 64), fill=WHITE)
d.text((tx, 392), "Measure your ring size & try it on in AR", font=font(reg_f, 30), fill=GRAY)
d.text((tx, 432), "obviousenterprises.com", font=font(bold_f, 30), fill=WHITE)

img.save("og-image.png")
print("ok og-image.png", img.size)
