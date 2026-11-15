import sys, os
import numpy as np
from PIL import Image, ImageDraw
root = sys.argv[1]; out = sys.argv[2]; names = sys.argv[3:]
tiles = []
for n in names:
    im = Image.open(os.path.join(root, n)).convert('RGBA')
    a = np.asarray(im); al = a[..., 3]
    ys, xs = np.nonzero(al > 128); y0, y1 = ys.min(), ys.max()
    t0, t1 = int(y0 + 0.25 * (y1 - y0)), int(y0 + 0.45 * (y1 - y0))
    cx = np.nonzero(al[t0:t1] > 128)[1].mean()
    W, H = 260, 320
    t = Image.new('RGBA', (W, H), (235, 235, 225, 255))
    t.alpha_composite(im.crop((int(cx) - 130, 80, int(cx) + 130, 400)))
    d = ImageDraw.Draw(t)
    for gx in range(0, W, 20): d.line([(gx, 0), (gx, H)], fill=(200, 200, 255) if gx != 130 else (255, 0, 0))
    t2 = Image.new('RGBA', (W, H), (235, 235, 225, 255)); t2.alpha_composite(im.crop((int(cx) - 130, 80, int(cx) + 130, 400)))
    t = Image.blend(t, t2, 0.6); d = ImageDraw.Draw(t); d.line([(0, 395 - 80), (W, 395 - 80)], fill=(0, 0, 255)); d.text((4, 4), os.path.basename(n), fill=(0, 0, 0))
    tiles.append(t.resize((W * 2, H * 2), Image.LANCZOS))
S = Image.new('RGB', (sum(t.width for t in tiles), tiles[0].height), (255, 255, 255))
x = 0
for t in tiles: S.paste(t.convert('RGB'), (x, 0)); x += t.width
S.save(out)
