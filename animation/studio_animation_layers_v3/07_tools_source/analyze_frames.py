import sys, json, glob, os
import numpy as np
from PIL import Image, ImageDraw
root = sys.argv[1]; out = sys.argv[2]
files = sorted(glob.glob(os.path.join(root, '*', '*.png')))
res = {}
tiles = []
for f in files:
    im = Image.open(f).convert('RGBA'); a = np.asarray(im).astype(int)
    al = a[..., 3]; rgb = a[..., :3]
    ys, xs = np.nonzero(al > 128)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    # tan boots: warm, fairly bright
    boot = (al > 128) & (r > 120) & (r - b > 50) & (g > 70) & (r > g) & (np.arange(a.shape[0])[:, None] > y0 + 0.7 * (y1 - y0))
    by, bx = np.nonzero(boot)
    # skin (face/hands): warm light
    skin = (al > 128) & (r > 150) & (g > 100) & (b > 70) & (r - b > 30) & (np.arange(a.shape[0])[:, None] < y0 + 0.3 * (y1 - y0))
    # torso band
    t0, t1 = int(y0 + 0.25 * (y1 - y0)), int(y0 + 0.45 * (y1 - y0))
    tx = np.nonzero(al[t0:t1] > 128)[1]
    # head width: rows in top 12% of height
    hrows = al[y0:int(y0 + 0.12 * (y1 - y0))] > 128
    hw = max((np.ptp(np.nonzero(rw)[0]) + 1) if rw.any() else 0 for rw in hrows)
    name = os.path.relpath(f, root)
    res[name] = dict(size=im.size, bbox=[int(x0), int(y0), int(x1), int(y1)], h=int(y1 - y0 + 1), w=int(x1 - x0 + 1),
                     torso_cx=float(tx.mean()), head_w=int(hw),
                     boot_px=int(boot.sum()), boot_x=[int(bx.min()), int(bx.max())] if len(bx) else None,
                     skin_px=int(skin.sum()))
    # tile
    t = Image.new('RGBA', im.size, (60, 160, 60, 255)); t.alpha_composite(im)
    d = ImageDraw.Draw(t); d.rectangle([x0, y0, x1, y1], outline=(255, 255, 0)); d.line([(tx.mean(), 0), (tx.mean(), im.height)], fill=(255, 0, 0))
    m = Image.new('RGBA', im.size, (0, 0, 0, 0)); mm = np.zeros(a.shape, np.uint8); mm[boot] = (0, 200, 255, 255); t.alpha_composite(Image.fromarray(mm))
    d.text((3, 3), os.path.basename(f)[:-4], fill=(255, 255, 255))
    tiles.append(t)
W = 240; H = 400; cols = 7
sheet = Image.new('RGB', (W * cols, H * ((len(tiles) + cols - 1) // cols)), (30, 30, 30))
for i, t in enumerate(tiles): sheet.paste(t.convert('RGB'), ((i % cols) * W, (i // cols) * H))
sheet.save(out)
for k, v in res.items(): print(k, v)
