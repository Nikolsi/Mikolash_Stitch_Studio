import json, itertools
import numpy as np
from PIL import Image
from scipy import ndimage
meta = json.load(open('work/char_meta.json'))
def comps(name):
    a = np.asarray(Image.open(f'work/char/walk_side/{name}.png')).astype(int); al = a[..., 3]
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    ys = np.nonzero(al > 128)[0]; y0, y1 = ys.min(), ys.max()
    bt = (al > 128) & (r > 120) & (r - b > 50) & (g > 70) & (r > g) & (np.arange(a.shape[0])[:, None] > y0 + 0.7 * (y1 - y0))
    bt = ndimage.binary_closing(bt, iterations=2); lab, n = ndimage.label(bt); out = []
    for i in range(1, n + 1):
        yy, xx = np.nonzero(lab == i)
        if len(yy) < 80: continue
        out.append(dict(x0=xx.min(), x1=xx.max(), ybot=yy.max(), grounded=yy.max() >= 430 - 6, n=len(yy)))
    return out
names = [f'walk_0{i}' for i in range(1, 7)]
C = {n: comps(n) for n in names}
for n in names: print(n, [(c['x0'], c['x1'], c['ybot'], 'G' if c['grounded'] else 'air') for c in C[n]])
def step(a, b):
    best = None
    for ca in C[a]:
        if not ca['grounded']: continue
        for cb in C[b]:
            if not cb['grounded']: continue
            d = ((cb['x0'] + cb['x1']) - (ca['x0'] + ca['x1'])) / 2
            if -60 <= d <= 0 and (best is None or abs(d + 22) < abs(best + 22)): best = d
    return best
res = []
for perm in itertools.permutations(names[1:]):
    order = ['walk_01'] + list(perm)
    ds = [step(order[i], order[(i + 1) % 6]) for i in range(6)]
    miss = sum(d is None for d in ds); vals = [-d for d in ds if d is not None]
    if not vals: continue
    res.append((miss, np.std(vals), order, ds))
res.sort(key=lambda r: (r[0], r[1]))
for r in res[:6]: print(r[0], round(r[1], 1), r[2], r[3])
print('sheet order:', [step(names[i], names[(i + 1) % 6]) for i in range(6)])
