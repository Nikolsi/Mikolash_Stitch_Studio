import sys, json
import numpy as np
from PIL import Image, ImageDraw
order = sys.argv[1].split(','); adv = list(map(float, sys.argv[2].split(','))); out = sys.argv[3]
frames = [Image.open(f'work/char/walk_side/{n}.png') for n in order]
N = len(order) * 2 + 1
x = 0.0; pos = []
for i in range(N):
    pos.append(x); x += adv[i % len(order)]
W = int(x + 340); Himg = 440
rows = []
for i in range(N - 1):
    c = Image.new('RGBA', (W, Himg), (236, 233, 222, 255))
    a = frames[i % len(order)].copy(); b = frames[(i + 1) % len(order)].copy()
    ga = np.asarray(a).copy(); ga[..., 3] = (ga[..., 3] * 0.45).astype(np.uint8)
    c.alpha_composite(Image.fromarray(ga), (int(pos[i]), 0)); c.alpha_composite(b, (int(pos[i + 1]), 0))
    d = ImageDraw.Draw(c); d.line([(0, 430), (W, 430)], fill=(0, 0, 255)); d.text((int(pos[i + 1]) + 10, 10), f'{order[i % len(order)]}->{order[(i + 1) % len(order)]}', fill=(0, 0, 0))
    rows.append(c.crop((int(pos[i]) , 300, int(pos[i + 1]) + 330, 440)))
S = Image.new('RGB', (max(r.width for r in rows), sum(r.height for r in rows)), (255, 255, 255))
y = 0
for r in rows: S.paste(r.convert('RGB'), (0, y)); y += r.height
S.save(out)
