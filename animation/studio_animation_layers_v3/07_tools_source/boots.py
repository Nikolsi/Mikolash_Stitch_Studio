import sys, glob, os
import numpy as np
from PIL import Image
from scipy import ndimage
root = sys.argv[1]
for f in sorted(glob.glob(os.path.join(root, '*', '*.png'))):
    a = np.asarray(Image.open(f).convert('RGBA')).astype(int); al = a[..., 3]
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    ys, xs = np.nonzero(al > 128); y0, y1 = ys.min(), ys.max()
    boot = (al > 128) & (r > 120) & (r - b > 50) & (g > 70) & (r > g) & (np.arange(a.shape[0])[:, None] > y0 + 0.7 * (y1 - y0))
    boot = ndimage.binary_closing(boot, iterations=2)
    lab, n = ndimage.label(boot)
    comps = []
    for i in range(1, n + 1):
        yy, xx = np.nonzero(lab == i)
        if len(yy) < 60: continue
        comps.append((int(xx.min()), int(xx.max()), int(yy.min()), int(yy.max()), len(yy)))
    comps.sort()
    hair = (al > 128) & (np.arange(a.shape[0])[:, None] < y0 + 40)
    hx = np.nonzero(hair)[1]
    print(f"{os.path.basename(f)[:-4]:22s} h={y1-y0+1:3d} boots=" + " ".join(f"[x{c[0]}-{c[1]} L{c[1]-c[0]+1} y{c[2]}-{c[3]} n{c[4]}]" for c in comps) + f" head_cx={hx.mean():.0f}")
